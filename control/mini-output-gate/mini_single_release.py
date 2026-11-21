#!/usr/bin/env python3
"""MINI single-file release. Reuses the one existing technical gate, no domain re-decisions.

Workers only write CATEGORY.json, EDITORIAL.json, TITLE.json. This command is the
only supported release writer. It invokes the existing gate in an isolated
scratch directory and publishes precisely one final MINI JSON after PASS.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

from mini_release_gate import gate as previous_gate, write as write_json

ORIGINAL = "ORIGINAL_MINI.json"
HASH = "ORIGINAL_SHA256.txt"
STAGES = ("CATEGORY", "EDITORIAL", "TITLE")
STAGE_KEYS = {
    "CATEGORY": ("route", "category_slug", "article_type"),
    "EDITORIAL": ("box", "intent_summary", "matched_ref", "reason"),
    "TITLE": ("approved_title",),
}
RELEASE_DIR = "FREIGABE"
RELEASE_NAME = "MINI_EINMAL_REIMPORT.json"
REPAIR_NAME = "REPARATUR.json"
STATUS_NAME = "STAND.json"
CONTRACT = "MINI_SINGLE_FILE_REIMPORT_V1"


def read(path: Path):
    with path.open(encoding="utf-8") as fd:
        return json.load(fd)


def canonical(obj) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def atomic(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name("." + path.name + ".tmp")
    temp.write_bytes(json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8") + b"\n")
    os.replace(temp, path)


def _clear_public_release(workspace: Path):
    path = workspace / RELEASE_DIR
    if path.exists():
        shutil.rmtree(path)


def _stage_data(workspace: Path, stage: str):
    path = workspace / (stage + ".json")
    return read(path)["items"] if path.is_file() else None


def _decision_from_old(checkpoint, stage):
    name = stage.lower()
    x = checkpoint.get(name)
    if stage == "TITLE" and isinstance(x, str):
        return {"approved_title": x}
    if isinstance(x, dict):
        if "values" in x and isinstance(x["values"], dict):
            x = x["values"]
        return {k: str(x.get(k) or "") for k in STAGE_KEYS[stage]}
    return None


def _locked_or_new(original, loaded, index: int, stage: str):
    stored = _decision_from_old(original["resume_checkpoints"][index], stage)
    if stored is not None:
        return None  # WP already has this owner's locked decision. Never resend.
    if loaded[stage] is None:
        return None
    row = loaded[stage][index]
    allowed = STAGE_KEYS[stage]
    vals = {k: str(row.get(k) or "") for k in allowed}
    if not any(v for v in vals.values()):
        return None
    return vals


def _published_file(workspace: Path, original):
    stages = {stage: _stage_data(workspace, stage) for stage in STAGES}
    rows = []
    source_items = original["items"]
    cp = original["resume_checkpoints"]
    for index, item in enumerate(source_items):
        row = {
            "index": index,
            "pool_key": str(item.get("pool_key") or ""),
            "original_item_sha256": digest(canonical(item)),
        }
        for stage in STAGES:
            row[stage.lower()] = _locked_or_new(original, stages, index, stage)
        if cp[index].get("next") == "DONE":
            if any(row[s.lower()] is not None for s in STAGES):
                raise ValueError("DONE-THEMA DARF KEINE NEUE ENTSCHEIDUNG ENTHALTEN")
        rows.append(row)
    payload = {
        "contract": CONTRACT,
        "source_contract": original["contract"],
        "batch_id": original["batch_id"],
        "source_sha256": original["source_sha256"],
        "original_export_sha256": digest((workspace / ORIGINAL).read_bytes()),
        "item_count": len(rows),
        "decisions": rows,
        "release": {
            "state": "PASS",
            "gate": "EXISTING_MINI_TECHNICAL_FINAL_GATE_V1",
            "workers_in_order": list(STAGES),
            "finished": True,
            "k0_unmodified": True,
        },
    }
    payload["release"]["payload_sha256"] = digest(canonical(payload))
    return payload


def run(workspace: Path):
    workspace = workspace.resolve()
    output = workspace / RELEASE_DIR
    source = workspace / ORIGINAL
    source_digest_file = workspace / HASH
    # In every invalid case remove an earlier release before touching input.
    _clear_public_release(workspace)
    if not source.is_file() or not source_digest_file.is_file():
        return _fail(workspace, "UNGUELTIGER_ORIGINALAUFTRAG", "MINI-Original oder Prüfsumme fehlt")
    if digest(source.read_bytes()) != source_digest_file.read_text(encoding="utf-8").strip():
        return _fail(workspace, "UNGUELTIGER_ORIGINALAUFTRAG", "Original wurde verändert")
    try:
        original = read(source)
        with tempfile.TemporaryDirectory(prefix="mini-gate-") as scratch:
            scratch_dir = Path(scratch)
            shutil.copyfile(source, scratch_dir / ORIGINAL)
            shutil.copyfile(source_digest_file, scratch_dir / HASH)
            for stage in STAGES:
                f = workspace / (stage + ".json")
                if f.is_file():
                    shutil.copyfile(f, scratch_dir / f.name)
            result = previous_gate(scratch_dir)
            if result.get("status") != "FREIGEGEBEN_FUER_WP_IMPORTE":
                ticket = read(scratch_dir / REPAIR_NAME)
                write_json(workspace / REPAIR_NAME, ticket)
                write_json(workspace / STATUS_NAME, {
                    "status": "REPARATUR", "batch_id": original.get("batch_id"),
                    "release_available": False, "next_worker": ticket.get("next_worker"),
                    "pending": len(ticket.get("fix_only", [])),
                })
                return ticket
            package = _published_file(workspace, original)
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        return _fail(workspace, "UNGUELTIGER_ARBEITSRAUM", str(exc))
    # Never distribute the internal stage files: the public folder has ONLY
    # the single import JSON and a separate audit receipt.
    output.mkdir(parents=True, exist_ok=False)
    atomic(output / RELEASE_NAME, package)
    report = {
        "status": "FREIGEGEBEN", "contract": CONTRACT,
        "batch_id": original["batch_id"], "topic_count": len(original["items"]),
        "import_file": RELEASE_NAME,
        "import_sha256": digest((output / RELEASE_NAME).read_bytes()),
        "release_count": 1, "wordpress_live_verified": False,
        "domain_redecision_performed": False,
    }
    write_json(output / "NACHWEIS.json", report)
    (workspace / REPAIR_NAME).unlink(missing_ok=True)
    write_json(workspace / STATUS_NAME, {
        "status": "FREIGEGEBEN", "batch_id": original["batch_id"],
        "release_available": True, "release_count": 1,
        "wordpress_live_verified": False,
    })
    return report


def _fail(workspace, state, why):
    ticket = {
        "status": "REPARATUR", "code": state, "reason": why,
        "release_available": False,
    }
    write_json(workspace / REPAIR_NAME, ticket)
    write_json(workspace / STATUS_NAME, ticket)
    return ticket



def deliver(workspace: Path, output_file: Path, candidate: Path | None = None):
    """The ONLY supported chat-file emission: revalidate the whole MINI batch.

    Reject a directly created CATEGORY/EDITORIAL/TITLE checkpoint even if its
    WordPress MINI-Import accepts it as a legitimate intermediate stage. Never
    expose partial files, and remove an older output if the gate now fails.
    """
    workspace = workspace.resolve()
    output_file = output_file.resolve()
    reserved = {workspace / ORIGINAL, workspace / HASH}
    reserved.update(workspace / (stage + ".json") for stage in STAGES)
    reserved.update({workspace / REPAIR_NAME, workspace / STATUS_NAME,
                     workspace / RELEASE_DIR / RELEASE_NAME,
                     workspace / RELEASE_DIR / "NACHWEIS.json"})
    if output_file.suffix.lower() != ".json" or output_file in reserved:
        raise ValueError("MINI_OUTPUT_DESTINATION_INVALID")
    if candidate is not None and candidate.resolve() == output_file:
        raise ValueError("MINI_OUTPUT_CANDIDATE_MUST_DIFFER")
    # A stale success must never remain downloadable after a failed repeat.
    output_file.unlink(missing_ok=True)
    result = run(workspace)
    if result.get("status") != "FREIGEGEBEN":
        return {"status": "GESPERRT", "release_available": False,
                "reason": "MINI_NOT_COMPLETE", "next_worker": result.get("next_worker")}

    approved = workspace / RELEASE_DIR / RELEASE_NAME
    receipt = workspace / RELEASE_DIR / "NACHWEIS.json"
    if not approved.is_file() or not receipt.is_file():
        return {"status": "GESPERRT", "release_available": False,
                "reason": "MINI_RELEASE_PROOF_MISSING"}
    binary = approved.read_bytes()
    report = read(receipt)
    if (report.get("status") != "FREIGEGEBEN"
            or report.get("contract") != CONTRACT
            or report.get("import_sha256") != digest(binary)
            or report.get("release_count") != 1):
        return {"status": "GESPERRT", "release_available": False,
                "reason": "MINI_RELEASE_PROOF_INVALID"}
    if candidate is not None:
        # This is the path that blocked the real 2026-11-21 CATEGORY-only file.
        if not candidate.is_file() or candidate.read_bytes() != binary:
            return {"status": "GESPERRT", "release_available": False,
                    "reason": "MINI_DIRECT_FILE_NOT_APPROVED"}
    # No user-visible JSON is written before the final verification.
    output_file.parent.mkdir(parents=True, exist_ok=True)
    temporary = output_file.with_name("." + output_file.name + ".tmp")
    try:
        temporary.write_bytes(binary)
        os.replace(temporary, output_file)
    finally:
        temporary.unlink(missing_ok=True)
    return {"status": "FREIGEGEBEN", "release_available": True,
            "filename": str(output_file), "import_sha256": digest(binary),
            "batch_id": report["batch_id"], "topic_count": report["topic_count"],
            "verification": str(receipt)}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace", type=Path, required=True)
    ap.add_argument("--deliver", type=Path,
                    help="Chat output path: only the full verified MINI file may be emitted")
    ap.add_argument("--candidate", type=Path,
                    help="Optional candidate file; rejected unless byte-identical to full release")
    args = ap.parse_args(argv)
    if args.candidate is not None and args.deliver is None:
        ap.error("--candidate requires --deliver")
    try:
        outcome = (deliver(args.workspace, args.deliver, args.candidate)
                   if args.deliver is not None else run(args.workspace))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        outcome = {"status": "GESPERRT", "release_available": False,
                   "reason": "MINI_OUTPUT_ERROR", "detail": str(exc)}
    print(json.dumps(outcome, ensure_ascii=False))
    return 0 if outcome.get("status") == "FREIGEGEBEN" else 2


if __name__ == "__main__":
    sys.exit(main())