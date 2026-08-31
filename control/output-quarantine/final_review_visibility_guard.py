#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
POINTER = REPO / "control/CURRENT_STARTMASTER.json"


class Blocked(RuntimeError):
    pass


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(value: str) -> Path:
    p = Path(str(value or ""))
    if not value or p.is_absolute() or ".." in p.parts:
        raise Blocked("INVALID_RELATIVE_PATH")
    return p


def validate_binding(binding_path: Path) -> dict:
    if not binding_path.is_file():
        raise Blocked("PREPARED_BINDING_MISSING")
    binding = load(binding_path)
    required = {"contract", "prepared_ref", "prepared_sha256", "batch_sha256"}
    if set(binding) != required:
        raise Blocked("PREPARED_BINDING_FIELDS_INVALID")
    if binding.get("contract") != "PFERDE_ATELIER_BOUND_PREPARED_RELEASE_FOR_FINAL_REVIEW_V1":
        raise Blocked("PREPARED_BINDING_CONTRACT_INVALID")

    ptr = load(POINTER)
    policy = load(REPO / rel(ptr.get("visible_output_policy_ref")))
    if policy.get("chat_execution_authority") != "NONE" or policy.get("chat_output_authority") != "NONE":
        raise Blocked("CHAT_AUTHORITY_MUST_BE_NONE")
    if policy.get("domain_logic_authority") != "NONE" or policy.get("quality_authority") != "NONE":
        raise Blocked("FINAL_VISIBILITY_GUARD_MUST_BE_DOMAIN_BLIND")

    prepared_ref = str(binding.get("prepared_ref") or "")
    staging_root = str(policy.get("release_staging_root") or "").rstrip("/") + "/"
    if not prepared_ref.startswith(staging_root):
        raise Blocked("PREPARED_RELEASE_OUTSIDE_STAGING_ROOT")
    prepared_path = REPO / rel(prepared_ref)
    if not prepared_path.is_file() or sha256(prepared_path) != binding.get("prepared_sha256"):
        raise Blocked("PREPARED_RELEASE_HASH_MISMATCH")

    prepared = load(prepared_path)
    if prepared.get("contract") != "PFERDE_ATELIER_PREPARED_OUTPUT_RELEASE_V1":
        raise Blocked("PREPARED_RELEASE_CONTRACT_INVALID")
    if prepared.get("status") != "PREPARED_NOT_VISIBLE":
        raise Blocked("PREPARED_RELEASE_STATUS_INVALID")
    if prepared.get("source_step_id") != "RUN_NEW_ARTICLE_BATCH_NO_STOP" or int(prepared.get("source_sequence", -1)) != 107007:
        raise Blocked("PREPARED_RELEASE_SOURCE_STEP_INVALID")
    if prepared.get("batch_sha256") != binding.get("batch_sha256"):
        raise Blocked("PREPARED_BATCH_MISMATCH")
    if prepared.get("chat_execution_authority") != "NONE" or prepared.get("chat_output_authority") != "NONE":
        raise Blocked("PREPARED_CHAT_AUTHORITY_INVALID")
    if prepared.get("domain_logic_authority") != "NONE" or prepared.get("quality_authority") != "NONE":
        raise Blocked("PREPARED_GUARD_AUTHORITY_INVALID")
    if prepared.get("publish_allowed") is not False:
        raise Blocked("AUTO_PUBLISH_FORBIDDEN")

    outputs = prepared.get("staged_outputs")
    if not isinstance(outputs, list) or not outputs:
        raise Blocked("PREPARED_OUTPUTS_MISSING")
    verified = []
    seen = set()
    for row in outputs:
        if not isinstance(row, dict) or set(row) != {"source_ref", "staged_ref", "sha256"}:
            raise Blocked("PREPARED_OUTPUT_ROW_INVALID")
        ref = str(row.get("staged_ref") or "")
        if not ref.startswith(staging_root):
            raise Blocked("STAGED_OUTPUT_OUTSIDE_STAGING_ROOT")
        if ref in seen:
            raise Blocked("DUPLICATE_STAGED_OUTPUT")
        seen.add(ref)
        p = REPO / rel(ref)
        if not p.is_file() or sha256(p) != row.get("sha256"):
            raise Blocked("STAGED_OUTPUT_HASH_MISMATCH:" + ref)
        verified.append(ref)

    return {
        "ok": True,
        "status": "FINAL_REVIEW_PREPARED_VISIBILITY_PASS",
        "batch_sha256": binding["batch_sha256"],
        "prepared_ref": prepared_ref,
        "prepared_sha256": binding["prepared_sha256"],
        "staged_count": len(verified),
        "chat_output_authority": "NONE",
        "visible_project_result": False,
        "publish_allowed": False,
    }


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=["verify"])
    ap.add_argument("binding")
    args = ap.parse_args()
    try:
        result = validate_binding(Path(args.binding))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except Blocked as exc:
        print(json.dumps({"ok": False, "status": "FINAL_REVIEW_PREPARED_VISIBILITY_BLOCKED", "reason": str(exc)}, ensure_ascii=False, indent=2))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
