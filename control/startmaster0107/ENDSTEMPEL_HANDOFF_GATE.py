#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[2]
LOCK_PATH = REPO / "control/startmaster0107/ENDSTEMPEL_HANDOFF_LOCK_V1.json"

LOCK_CONTRACT = "PFERDE_ATELIER_ENDSTEMPEL_HANDOFF_LOCK_V1"
RECEIPT_CONTRACT = "PFERDE_ATELIER_OUTPUT_RELEASE_RECEIPT_V2"
RECEIPT_STATUS = "OUTPUT_RELEASE_PASS_FINAL_REVIEW_AND_REARM_CONFIRMED"
ALLOWED_ACTION = "PERSIST_EXISTING_107008_RELEASE_SET_BYTE_IDENTICAL_TO_GITHUB"
NEXT_ACTION = "RUN_EXISTING_ENDSTEMPEL_ONLY"


class Blocked(RuntimeError):
    pass


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise Blocked("JSON_INVALID:" + str(path)) from exc
    if not isinstance(value, dict):
        raise Blocked("JSON_OBJECT_REQUIRED:" + str(path))
    return value


def load_lock() -> dict[str, Any]:
    if not LOCK_PATH.is_file():
        raise Blocked("HANDOFF_LOCK_MISSING")
    lock = load_json(LOCK_PATH)
    required = {
        "contract", "status", "scope", "batch_sha256", "source_receipt_ref",
        "expected_receipt_sha256", "expected_articles", "allowed_action",
        "next_action_on_pass", "denied_actions", "publish_allowed",
        "content_mutation_allowed", "workflow_navigation_authority",
    }
    if set(lock) != required:
        raise Blocked("HANDOFF_LOCK_FIELDS_INVALID")
    if lock["contract"] != LOCK_CONTRACT or lock["status"] != "LOCKED":
        raise Blocked("HANDOFF_LOCK_CONTRACT_OR_STATUS_INVALID")
    if lock["scope"] != "107008_PASS_TO_ENDSTEMPEL_ONLY":
        raise Blocked("HANDOFF_LOCK_SCOPE_INVALID")
    if lock["allowed_action"] != ALLOWED_ACTION or lock["next_action_on_pass"] != NEXT_ACTION:
        raise Blocked("HANDOFF_LOCK_ACTION_INVALID")
    if lock["publish_allowed"] is not False or lock["content_mutation_allowed"] is not False:
        raise Blocked("HANDOFF_LOCK_MUTATION_OR_PUBLISH_INVALID")
    if lock["workflow_navigation_authority"] != "NONE":
        raise Blocked("HANDOFF_LOCK_NAVIGATION_AUTHORITY_INVALID")
    if not re.fullmatch(r"[0-9a-f]{64}", str(lock["batch_sha256"])):
        raise Blocked("HANDOFF_LOCK_BATCH_INVALID")
    if not re.fullmatch(r"[0-9a-f]{64}", str(lock["expected_receipt_sha256"])):
        raise Blocked("HANDOFF_LOCK_RECEIPT_HASH_INVALID")
    articles = lock["expected_articles"]
    if not isinstance(articles, list) or len(articles) != 7:
        raise Blocked("HANDOFF_LOCK_ARTICLE_COUNT_INVALID")
    seen = set()
    for row in articles:
        if not isinstance(row, dict) or set(row) != {"name", "sha256"}:
            raise Blocked("HANDOFF_LOCK_ARTICLE_ROW_INVALID")
        name = str(row["name"])
        digest = str(row["sha256"])
        if not re.fullmatch(r"ARTICLE_[0-9a-f]{64}\.md", name):
            raise Blocked("HANDOFF_LOCK_ARTICLE_NAME_INVALID")
        if not re.fullmatch(r"[0-9a-f]{64}", digest) or name in seen:
            raise Blocked("HANDOFF_LOCK_ARTICLE_HASH_OR_DUPLICATE_INVALID")
        seen.add(name)
    return lock


def verify_persisted_release(lock: dict[str, Any]) -> dict[str, Any]:
    batch = lock["batch_sha256"]
    expected_receipt_ref = f".pferde-release/{batch}/RELEASE_RECEIPT.json"
    if lock["source_receipt_ref"] != expected_receipt_ref:
        raise Blocked("HANDOFF_LOCK_RECEIPT_REF_INVALID")
    receipt_path = REPO / expected_receipt_ref
    if not receipt_path.is_file():
        raise Blocked("HANDOFF_RECEIPT_NOT_PERSISTED")
    actual_receipt_sha = file_sha256(receipt_path)
    if actual_receipt_sha != lock["expected_receipt_sha256"]:
        raise Blocked("HANDOFF_RECEIPT_HASH_MISMATCH")
    receipt = load_json(receipt_path)
    if receipt.get("contract") != RECEIPT_CONTRACT:
        raise Blocked("HANDOFF_RECEIPT_CONTRACT_INVALID")
    if receipt.get("status") != RECEIPT_STATUS:
        raise Blocked("HANDOFF_RECEIPT_STATUS_INVALID")
    if int(receipt.get("final_review_sequence") or -1) != 107008:
        raise Blocked("HANDOFF_RECEIPT_SEQUENCE_INVALID")
    if receipt.get("batch_sha256") != batch:
        raise Blocked("HANDOFF_RECEIPT_BATCH_INVALID")
    if receipt.get("publish_allowed") is not False:
        raise Blocked("HANDOFF_RECEIPT_PUBLISH_INVALID")

    outputs = receipt.get("outputs")
    if not isinstance(outputs, list):
        raise Blocked("HANDOFF_RECEIPT_OUTPUTS_INVALID")

    expected = {row["name"]: row["sha256"] for row in lock["expected_articles"]}
    found: dict[str, str] = {}
    release_dir = REPO / ".pferde-release" / batch
    for row in outputs:
        if not isinstance(row, dict):
            continue
        ref = str(row.get("released_ref") or "")
        digest = str(row.get("sha256") or "")
        name = Path(ref).name
        if name not in expected:
            continue
        if ref != f".pferde-release/{batch}/{name}":
            raise Blocked("HANDOFF_ARTICLE_REF_INVALID:" + name)
        if name in found:
            raise Blocked("HANDOFF_ARTICLE_DUPLICATE:" + name)
        if digest != expected[name]:
            raise Blocked("HANDOFF_ARTICLE_RECEIPT_HASH_MISMATCH:" + name)
        found[name] = digest

    if found != expected:
        raise Blocked("HANDOFF_ARTICLE_SET_NOT_BOUND")

    disk_names = {p.name for p in release_dir.glob("ARTICLE_*.md") if p.is_file()}
    if disk_names != set(expected):
        raise Blocked("HANDOFF_DISK_ARTICLE_SET_MISMATCH")
    for name, digest in expected.items():
        path = release_dir / name
        if file_sha256(path) != digest:
            raise Blocked("HANDOFF_ARTICLE_BYTE_HASH_MISMATCH:" + name)

    return {
        "ok": True,
        "status": "ENDSTEMPEL_HANDOFF_PASS",
        "batch_sha256": batch,
        "receipt_sha256": actual_receipt_sha,
        "article_count": 7,
        "next_authorized_action": NEXT_ACTION,
        "publish_allowed": False,
        "content_mutation_performed": False,
        "all_other_actions": "DENY",
    }


def main() -> int:
    try:
        lock = load_lock()
        if len(sys.argv) != 2:
            raise Blocked("HANDOFF_LOCK_COMMAND_DENIED")
        command = sys.argv[1]
        if command == "status":
            result = {
                "ok": True,
                "status": "ENDSTEMPEL_HANDOFF_LOCK_ACTIVE",
                "scope": lock["scope"],
                "batch_sha256": lock["batch_sha256"],
                "only_authorized_action": lock["allowed_action"],
                "next_action_on_pass": lock["next_action_on_pass"],
                "publish_allowed": False,
                "all_other_actions": "DENY",
            }
        elif command == "verify":
            result = verify_persisted_release(lock)
        else:
            raise Blocked("HANDOFF_LOCK_COMMAND_DENIED")
        print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))
        return 0
    except Blocked as exc:
        print(json.dumps({
            "ok": False,
            "status": "ENDSTEMPEL_HANDOFF_BLOCKED",
            "error": str(exc),
            "publish_allowed": False,
            "all_other_actions": "DENY",
        }, ensure_ascii=False, separators=(",", ":")))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
