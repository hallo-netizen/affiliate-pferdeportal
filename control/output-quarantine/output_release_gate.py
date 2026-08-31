#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
POINTER = REPO / "control/CURRENT_STARTMASTER.json"


class Blocked(RuntimeError):
    pass


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def rel(value: str) -> Path:
    p = Path(str(value or ""))
    if not value or p.is_absolute() or ".." in p.parts:
        raise Blocked("INVALID_RELATIVE_PATH")
    return p


def git(*args: str) -> str:
    try:
        cp = subprocess.run(
            ["git", *args], cwd=REPO, check=True, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
    except Exception as exc:
        raise Blocked(f"GIT_CHECK_FAILED:{' '.join(args)}") from exc
    return cp.stdout.strip()


def require_head_is_current_main() -> str:
    head = git("rev-parse", "HEAD")
    remote_line = git("ls-remote", "origin", "refs/heads/main")
    parts = remote_line.split()
    if not parts:
        raise Blocked("REMOTE_MAIN_UNVERIFIABLE")
    remote = parts[0]
    if head != remote:
        raise Blocked(f"STALE_WORKER_HEAD:HEAD={head}:MAIN={remote}")
    return head


def authority():
    if not POINTER.is_file():
        raise Blocked("STARTMASTER_POINTER_MISSING")
    ptr = load(POINTER)
    statep = REPO / rel(ptr.get("state_ref"))
    rootp = REPO / rel(ptr.get("root_ref"))
    if not statep.is_file() or not rootp.is_file():
        raise Blocked("ROOT_OR_STATE_MISSING")
    state = load(statep)
    root = load(rootp)
    if ptr.get("startmaster") != state.get("startmaster") or state.get("startmaster") != root.get("startmaster"):
        raise Blocked("STARTMASTER_IDENTITY_MISMATCH")
    if sha256(statep) != root.get("current_state_sha256"):
        raise Blocked("STATE_HASH_MISMATCH")
    if ptr.get("free_chat_execution_authority") is not False:
        raise Blocked("FREE_CHAT_AUTHORITY_MUST_BE_FALSE")
    gate = state.get("execution_gate") or {}
    if gate.get("domain_logic_authority") != "NONE" or gate.get("content_quality_design_authority") != "NONE":
        raise Blocked("OUTPUT_GATE_MUST_BE_DOMAIN_BLIND")
    return ptr, root, state, gate


def validate_release_manifest(manifest_path: Path, receipt_path: Path):
    _, _, state, gate = authority()
    manifest = load(manifest_path)
    receipt = load(receipt_path)

    required_manifest = {
        "contract", "startmaster", "step_id", "sequence", "batch_sha256",
        "receipt_sha256", "workflow_pass", "outputs", "publish_allowed",
        "created_by", "content_quality_decision_authority"
    }
    if set(manifest) != required_manifest:
        raise Blocked("RELEASE_MANIFEST_FIELDS_INVALID")
    if manifest.get("contract") != "PFERDE_ATELIER_OUTPUT_RELEASE_MANIFEST_V1":
        raise Blocked("RELEASE_MANIFEST_CONTRACT_INVALID")
    if manifest.get("startmaster") != state.get("startmaster"):
        raise Blocked("RELEASE_STARTMASTER_MISMATCH")
    if manifest.get("step_id") != gate.get("step_id") or int(manifest.get("sequence", -1)) != int(gate.get("sequence", -2)):
        raise Blocked("RELEASE_STEP_MISMATCH")
    if manifest.get("workflow_pass") is not True:
        raise Blocked("FULL_WORKFLOW_PASS_REQUIRED")
    if manifest.get("publish_allowed") is not False:
        raise Blocked("AUTO_PUBLISH_FORBIDDEN")
    if manifest.get("created_by") != "BOUND_WORKER":
        raise Blocked("CHAT_OR_UNBOUND_OUTPUT_FORBIDDEN")
    if manifest.get("content_quality_decision_authority") != "NONE":
        raise Blocked("OUTPUT_GATE_MUST_NOT_DECIDE_CONTENT_OR_QUALITY")

    actual_receipt_hash = sha256(receipt_path)
    if manifest.get("receipt_sha256") != actual_receipt_hash:
        raise Blocked("RECEIPT_HASH_MISMATCH")
    if receipt.get("contract") != "PFERDE_ATELIER_STEP_RECEIPT_V2":
        raise Blocked("STEP_RECEIPT_CONTRACT_INVALID")
    if receipt.get("status") != "PASS":
        raise Blocked("STEP_RECEIPT_NOT_PASS")
    if receipt.get("step_id") != manifest.get("step_id") or int(receipt.get("sequence", -1)) != int(manifest.get("sequence", -2)):
        raise Blocked("RECEIPT_STEP_MISMATCH")
    if receipt.get("workflow_change_requested") is not False or receipt.get("navigation_decision") is not False:
        raise Blocked("RECEIPT_AUTHORITY_VIOLATION")

    batch = str(manifest.get("batch_sha256") or "")
    if len(batch) != 64:
        raise Blocked("BATCH_SHA_INVALID")
    payload = receipt.get("payload") or {}
    if payload.get("batch_sha256") != batch:
        raise Blocked("RECEIPT_BATCH_MISMATCH")
    if payload.get("workflow_pass") is not True:
        raise Blocked("RECEIPT_FULL_WORKFLOW_PASS_REQUIRED")
    receipt_outputs = payload.get("outputs")
    if not isinstance(receipt_outputs, list) or not receipt_outputs:
        raise Blocked("RECEIPT_OUTPUT_BINDING_MISSING")

    outputs = manifest.get("outputs")
    if not isinstance(outputs, list) or not outputs:
        raise Blocked("NO_RELEASE_OUTPUTS")
    if outputs != receipt_outputs:
        raise Blocked("MANIFEST_RECEIPT_OUTPUT_BINDING_MISMATCH")

    seen = set()
    verified = []
    for i, row in enumerate(outputs):
        if not isinstance(row, dict) or set(row) != {"ref", "sha256"}:
            raise Blocked(f"OUTPUT_ROW_INVALID:{i}")
        r = str(row.get("ref") or "")
        if r in seen:
            raise Blocked(f"DUPLICATE_OUTPUT_REF:{r}")
        seen.add(r)
        p = REPO / rel(r)
        if not p.is_file():
            raise Blocked(f"OUTPUT_MISSING:{r}")
        actual = sha256(p)
        if actual != row.get("sha256"):
            raise Blocked(f"OUTPUT_HASH_MISMATCH:{r}")
        verified.append((p, r, actual))
    return manifest, verified


def release(manifest_path: Path, receipt_path: Path, destination: Path):
    main_head = require_head_is_current_main()
    manifest, verified = validate_release_manifest(manifest_path, receipt_path)
    destination.mkdir(parents=True, exist_ok=True)
    released = []
    for src, ref, digest in verified:
        dst = destination / src.name
        if dst.exists():
            if sha256(dst) != digest:
                raise Blocked(f"DESTINATION_COLLISION:{dst.name}")
        else:
            shutil.copyfile(src, dst)
        released.append({"source_ref": ref, "released_path": str(dst), "sha256": digest})
    return {
        "ok": True,
        "status": "OUTPUT_RELEASE_PASS",
        "main_head": main_head,
        "startmaster": manifest["startmaster"],
        "step_id": manifest["step_id"],
        "sequence": manifest["sequence"],
        "batch_sha256": manifest["batch_sha256"],
        "released": released,
        "publish_allowed": False,
    }


def main(argv=None):
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("release")
    p.add_argument("manifest")
    p.add_argument("receipt")
    p.add_argument("destination")
    args = parser.parse_args(argv)
    try:
        result = release(Path(args.manifest), Path(args.receipt), Path(args.destination))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except Blocked as exc:
        print(json.dumps({"ok": False, "status": "BLOCKED", "reason": str(exc)}, ensure_ascii=False, indent=2))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
