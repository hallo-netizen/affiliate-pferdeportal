#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SYSTEM4 = REPO / "isolated_system4"
BATCH_STATE = "SYSTEM4_107007_BATCH_STATE.json"
HANDOFF_NAME = "SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2.json"
BINDING_NAME = "SYSTEM4_107008_V2_INPUT_BINDING.json"
RUNTIME_ENTRY = REPO / "control/output-quarantine/runtime_entry_gate.py"

if str(SYSTEM4) not in sys.path:
    sys.path.insert(0, str(SYSTEM4))
import handoff_transport  # noqa: E402


class Blocked(RuntimeError):
    pass


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise Blocked("SYSTEM4_107008_JSON_OBJECT_REQUIRED:" + str(path))
    return value


def outside_repo(path: Path) -> Path:
    p = path.expanduser().resolve()
    root = REPO.resolve()
    if p == root or root in p.parents:
        raise Blocked("SYSTEM4_107008_RUNTIME_PATH_MUST_BE_OUTSIDE_REPO")
    return p


def _state_paths(batch_root: Path, count: int) -> list[Path]:
    return [batch_root / f"item-{i:06d}" / "state.json" for i in range(count)]


def build_payload(batch_root: Path) -> tuple[dict, dict]:
    state_path = batch_root / BATCH_STATE
    if not state_path.is_file():
        raise Blocked("SYSTEM4_107008_BATCH_STATE_MISSING")
    batch = load(state_path)
    if batch.get("contract") != "SYSTEM4_107007_PRODUCTION_BATCH_V1":
        raise Blocked("SYSTEM4_107008_BATCH_STATE_CONTRACT_INVALID")
    if batch.get("status") != "ITEMS_COMPLETE":
        raise Blocked("SYSTEM4_107008_BATCH_NOT_COMPLETE")
    if batch.get("publish_allowed") is not False:
        raise Blocked("SYSTEM4_107008_PUBLISH_MUST_BE_FALSE")
    count = batch.get("item_count")
    if not isinstance(count, int) or isinstance(count, bool) or count < 1:
        raise Blocked("SYSTEM4_107008_ITEM_COUNT_INVALID")
    if batch.get("completed_indices") != list(range(count)) or batch.get("started_indices") != list(range(count)):
        raise Blocked("SYSTEM4_107008_BATCH_SEQUENCE_INCOMPLETE")
    collect = batch.get("batch_collect")
    evidence_path = batch_root / "batch-collect" / "system4_batch_evidence.json"
    if (
        not isinstance(collect, dict)
        or collect.get("status") != "SYSTEM4_BATCH_FULL_PASS_COLLECTED"
        or collect.get("batch_sha256") != batch.get("batch_sha256")
        or collect.get("article_count") != count
        or collect.get("batch_evidence_path") != str(evidence_path)
        or not evidence_path.is_file()
        or collect.get("batch_evidence_sha256") != sha256(evidence_path)
    ):
        raise Blocked("SYSTEM4_107008_BATCH_COLLECT_PROOF_INVALID")

    rows = []
    for index, path in enumerate(_state_paths(batch_root, count)):
        if not path.is_file():
            raise Blocked("SYSTEM4_107008_ARTICLE_STATE_MISSING:" + str(index))
        state = load(path)
        article = state.get("article")
        checks = state.get("checks")
        if state.get("phase") != "OUTPUT_GATE_REQUIRED" or not isinstance(checks, dict) or checks.get("status") != "PASS":
            raise Blocked("SYSTEM4_107008_ARTICLE_NOT_PASS:" + str(index))
        if not isinstance(article, dict):
            raise Blocked("SYSTEM4_107008_ARTICLE_BINDING_MISSING:" + str(index))
        prod = checks.get("production_evidence")
        ev = prod.get("evidence") if isinstance(prod, dict) else None
        if not isinstance(ev, dict):
            raise Blocked("SYSTEM4_107008_PRODUCTION_EVIDENCE_MISSING:" + str(index))
        row = {
            "index": index,
            "title": article.get("title"),
            "target_keyword": article.get("target_keyword"),
            "category": article.get("category"),
            "article_type": article.get("article_type"),
            "plan_slot": article.get("plan_slot"),
            "final_draft_sha256": state.get("draft_sha256"),
            "revision_count": state.get("revision"),
            "body": state.get("draft_markdown"),
            "production_context": state.get("production_context"),
            "languagetool": ev.get("languagetool"),
            "ppm679": ev.get("ppm679"),
        }
        rows.append(row)

    payload = {
        "contract": handoff_transport.HANDOFF_CONTRACT,
        "batch_sha256": batch["batch_sha256"],
        "publish_allowed": False,
        "signing_deferred": True,
        "batch_gate_status": "SYSTEM4_BATCH_FULL_PASS_COLLECTED",
        "no_legacy_status": "PASS",
        "test_suite_status": "PASS",
        "wordpress_review": handoff_transport.wordpress_review(),
        "articles": rows,
    }
    handoff_transport.validate_handoff(payload)
    return payload, batch


def prepare(batch_root_path: str) -> dict:
    batch_root = outside_repo(Path(batch_root_path))
    payload, batch = build_payload(batch_root)
    out = batch_root / "107008-handoff"
    out.mkdir(parents=True, exist_ok=True)
    raw_path = out / HANDOFF_NAME
    raw_path.write_text(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    canonical_path = out / ("CANONICAL_" + HANDOFF_NAME)
    handoff_transport.canonicalize_handoff(raw_path, canonical_path)
    inline_path = out / handoff_transport.INLINE_FILENAME
    packed = handoff_transport.inline_pack(canonical_path, inline_path)
    rebuilt_dir = out / "parent-chat-reconstructed"
    rebuilt = handoff_transport.inline_unpack(inline_path, rebuilt_dir)
    canonical_sha = sha256(canonical_path)
    if sha256(rebuilt) != canonical_sha or rebuilt.read_bytes() != canonical_path.read_bytes():
        raise Blocked("SYSTEM4_107008_PARENT_CHAT_BYTE_MISMATCH")
    count = len(payload["articles"])
    binding = {
        "contract": "SYSTEM4_107008_V2_INPUT_BINDING_V1",
        "status": "SYSTEM4_107008_V2_HANDOFF_BOUND",
        "batch_sha256": batch["batch_sha256"],
        "article_count": count,
        "handoff_ref": str(canonical_path),
        "handoff_sha256": canonical_sha,
        "inline_ref": str(inline_path),
        "inline_plaintext_sha256": packed["plaintext_sha256"],
        "reconstructed_ref": str(rebuilt),
        "reconstructed_sha256": sha256(rebuilt),
        "batch_evidence_ref": batch["batch_collect"]["batch_evidence_path"],
        "batch_evidence_sha256": batch["batch_collect"]["batch_evidence_sha256"],
        "publish_allowed": False,
        "next_sequence": 107008,
    }
    binding_path = batch_root / BINDING_NAME
    binding_path.write_text(json.dumps(binding, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {**binding, "binding_ref": str(binding_path), "binding_sha256": sha256(binding_path)}


def validate_binding(binding_path: Path) -> dict:
    binding_path = outside_repo(binding_path)
    if not binding_path.is_file():
        raise Blocked("SYSTEM4_107008_BINDING_MISSING")
    b = load(binding_path)
    required = {
        "contract", "status", "batch_sha256", "article_count", "handoff_ref", "handoff_sha256",
        "inline_ref", "inline_plaintext_sha256", "reconstructed_ref", "reconstructed_sha256",
        "batch_evidence_ref", "batch_evidence_sha256", "publish_allowed", "next_sequence"
    }
    if set(b) != required or b.get("contract") != "SYSTEM4_107008_V2_INPUT_BINDING_V1" or b.get("status") != "SYSTEM4_107008_V2_HANDOFF_BOUND":
        raise Blocked("SYSTEM4_107008_BINDING_INVALID")
    if b.get("publish_allowed") is not False or b.get("next_sequence") != 107008:
        raise Blocked("SYSTEM4_107008_BINDING_POLICY_INVALID")
    handoff = outside_repo(Path(b["handoff_ref"]))
    rebuilt = outside_repo(Path(b["reconstructed_ref"]))
    inline = outside_repo(Path(b["inline_ref"]))
    evidence = outside_repo(Path(b["batch_evidence_ref"]))
    for p in (handoff, rebuilt, inline, evidence):
        if not p.is_file():
            raise Blocked("SYSTEM4_107008_BINDING_FILE_MISSING:" + str(p))
    if sha256(handoff) != b.get("handoff_sha256") or sha256(rebuilt) != b.get("reconstructed_sha256"):
        raise Blocked("SYSTEM4_107008_HANDOFF_HASH_MISMATCH")
    if handoff.read_bytes() != rebuilt.read_bytes():
        raise Blocked("SYSTEM4_107008_HANDOFF_RECONSTRUCT_MISMATCH")
    if sha256(evidence) != b.get("batch_evidence_sha256"):
        raise Blocked("SYSTEM4_107008_BATCH_EVIDENCE_HASH_MISMATCH")
    payload, _ = handoff_transport.read_validate_handoff(handoff)
    if payload.get("batch_sha256") != b.get("batch_sha256") or len(payload.get("articles") or []) != b.get("article_count"):
        raise Blocked("SYSTEM4_107008_HANDOFF_BINDING_MISMATCH")
    return b


def start(batch_root_path: str) -> dict:
    prepared = prepare(batch_root_path)
    binding = validate_binding(Path(prepared["binding_ref"]))
    cp = subprocess.run([sys.executable, str(RUNTIME_ENTRY), "start"], cwd=REPO, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    output = (cp.stdout or "") + (cp.stderr or "")
    if cp.returncode != 0:
        raise Blocked("SYSTEM4_107008_RUNTIME_START_FAIL:" + output.strip())
    try:
        runtime = json.loads(cp.stdout)
    except Exception as exc:
        raise Blocked("SYSTEM4_107008_RUNTIME_START_OUTPUT_INVALID") from exc
    if runtime.get("status") != "OFFICIAL_RUNTIME_ENTRY_PASS" or int(runtime.get("sequence", -1)) != 107008:
        raise Blocked("SYSTEM4_107008_RUNTIME_START_NOT_107008")
    return {
        "ok": True,
        "status": "SYSTEM4_107008_V2_HANDOFF_ENTRY_PASS",
        "binding_ref": prepared["binding_ref"],
        "binding_sha256": prepared["binding_sha256"],
        "batch_sha256": binding["batch_sha256"],
        "article_count": binding["article_count"],
        "handoff_sha256": binding["handoff_sha256"],
        "runtime_status": runtime["status"],
        "publish_allowed": False,
    }


def main() -> int:
    try:
        if len(sys.argv) != 3 or sys.argv[1] not in {"prepare", "validate", "start"}:
            raise Blocked("USE: system4_107008_handoff.py prepare|validate|start BATCH_ROOT_OR_BINDING")
        if sys.argv[1] == "prepare":
            result = prepare(sys.argv[2])
        elif sys.argv[1] == "validate":
            result = validate_binding(Path(sys.argv[2]))
        else:
            result = start(sys.argv[2])
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    except Exception as exc:
        print(json.dumps({"ok": False, "status": "SYSTEM4_107008_V2_HANDOFF_BLOCKED", "reason": str(exc), "publish_allowed": False}, ensure_ascii=False, sort_keys=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
