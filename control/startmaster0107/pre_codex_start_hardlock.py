from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
MANIFEST = HERE / "PRE_CODEX_START_HARDLOCK.json"
RECEIPT = HERE / "PRE_CODEX_START_RECEIPT.json"
STATE = HERE / "CURRENT_STATE.json"
ROOT = HERE / "PFERDE_ATELIER_START_HERE.json"

CONTRACT = "PFERDE_ATELIER_PRE_CODEX_START_HARDLOCK_V1"
RECEIPT_CONTRACT = "PFERDE_ATELIER_PRE_CODEX_START_RECEIPT_V1"
REQUIRED_GUARDS = {
    "STALE_MAIN_HASH",
    "DISPATCHER_HEAD_DRIFT",
    "HARDLOCK_BASE_NOT_FRESH_PASS",
    "START_HERE_STATE_HASH_DRIFT",
    "WRONG_STEP_OR_POINT0_BYPASS",
    "MANUAL_SOURCE_REQUEST_OR_WORKSPACE",
    "CODEX_BOUND_CAPSULE_MISSING",
    "OLD_OR_RECOVERY_ARTICLE_AS_NEW",
    "TEMP_WORKSPACE_LOSS",
    "NEXT_ARTICLE_BEFORE_PREVIOUS_PASS",
    "REPAIRABLE_FINDING_TERMINALIZED",
    "CODEX_USAGE_LIMIT_ACTIVE",
    "CODEX_GITHUB_AUTH_ASSUMPTION",
    "OUTPUT_ONLY_IN_TMP",
    "PUBLISH_WITHOUT_SEPARATE_APPROVAL",
}


class PreCodexStartBlocked(RuntimeError):
    pass


def _load(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise PreCodexStartBlocked("PRECODEX_JSON_INVALID:" + path.name) from exc
    if not isinstance(value, dict):
        raise PreCodexStartBlocked("PRECODEX_OBJECT_REQUIRED:" + path.name)
    return value


def _sha_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _git_head(repo: Path) -> str:
    try:
        cp = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except Exception as exc:
        raise PreCodexStartBlocked("PRECODEX_GIT_HEAD_UNAVAILABLE") from exc
    value = cp.stdout.strip()
    if len(value) != 40:
        raise PreCodexStartBlocked("PRECODEX_GIT_HEAD_INVALID")
    return value


def validate_payload(
    *,
    head: str,
    manifest: dict,
    receipt: dict,
    state: dict,
    root: dict,
    state_sha256: str,
) -> dict:
    if manifest.get("contract") != CONTRACT or manifest.get("status") != "ACTIVE_FAIL_CLOSED":
        raise PreCodexStartBlocked("PRECODEX_MANIFEST_INVALID")
    guard_ids = {
        str(row.get("id") or "")
        for row in (manifest.get("required_historical_guards") or [])
        if isinstance(row, dict)
    }
    missing = sorted(REQUIRED_GUARDS - guard_ids)
    if missing:
        raise PreCodexStartBlocked("PRECODEX_HISTORICAL_GUARD_MISSING:" + ",".join(missing))
    if manifest.get("canonical_start_command") != "python3 isolated_system4/parent_start.py start-current-bound":
        raise PreCodexStartBlocked("PRECODEX_CANONICAL_START_DRIFT")
    if manifest.get("canonical_step_id") != "RUN_NEW_ARTICLE_BATCH_NO_STOP" or int(manifest.get("canonical_sequence", -1)) != 107007:
        raise PreCodexStartBlocked("PRECODEX_CANONICAL_STEP_DRIFT")
    immutable = manifest.get("immutable_expectations") or {}
    if immutable.get("article_bodies") != "NEW":
        raise PreCodexStartBlocked("PRECODEX_NEW_ARTICLE_POLICY_INVALID")
    if immutable.get("article_advance") != "ONLY_AFTER_REAL_PASS":
        raise PreCodexStartBlocked("PRECODEX_ADVANCE_POLICY_INVALID")
    if immutable.get("repair") != "SAME_ARTICLE_SAME_WORKSPACE_UNTIL_PASS":
        raise PreCodexStartBlocked("PRECODEX_REPAIR_POLICY_INVALID")
    if immutable.get("quality_threshold_changes_allowed") is not False:
        raise PreCodexStartBlocked("PRECODEX_QUALITY_CHANGE_POLICY_INVALID")
    if immutable.get("codex_side_github_write_required") is not False:
        raise PreCodexStartBlocked("PRECODEX_CODEX_GITHUB_POLICY_INVALID")
    if immutable.get("publish_allowed") is not False:
        raise PreCodexStartBlocked("PRECODEX_PUBLISH_POLICY_INVALID")

    if root.get("current_state_sha256") != state_sha256:
        raise PreCodexStartBlocked("PRECODEX_STATE_HASH_BINDING_MISMATCH")
    if root.get("next_allowed_step") != state.get("next_allowed_step"):
        raise PreCodexStartBlocked("PRECODEX_ROOT_STATE_STEP_MISMATCH")
    gate = state.get("execution_gate") or {}
    if state.get("next_allowed_step") != "RUN_NEW_ARTICLE_BATCH_NO_STOP":
        raise PreCodexStartBlocked("PRECODEX_STEP_NOT_107007")
    if gate.get("step_id") != "RUN_NEW_ARTICLE_BATCH_NO_STOP" or int(gate.get("sequence", -1)) != 107007:
        raise PreCodexStartBlocked("PRECODEX_GATE_NOT_107007")
    if state.get("publish_allowed") is not False:
        raise PreCodexStartBlocked("PRECODEX_STATE_PUBLISH_NOT_FALSE")

    blocker = state.get("current_execution_blocker") or {}
    if blocker.get("codex_start_allowed") is not True:
        raise PreCodexStartBlocked("PRECODEX_CURRENT_STATE_START_NOT_ALLOWED")
    external = state.get("external_execution_blocker")
    if isinstance(external, dict) and external:
        if external.get("resolved") is not True:
            raise PreCodexStartBlocked("PRECODEX_EXTERNAL_BLOCKER_NOT_RESOLVED")

    if receipt.get("contract") != RECEIPT_CONTRACT or receipt.get("status") != "PASS":
        raise PreCodexStartBlocked("PRECODEX_RECEIPT_NOT_PASS")
    if receipt.get("authorized_head_sha") != head:
        raise PreCodexStartBlocked("PRECODEX_RECEIPT_HEAD_STALE")
    if receipt.get("dispatcher_head_sha") != head:
        raise PreCodexStartBlocked("PRECODEX_DISPATCHER_HEAD_DRIFT")
    if receipt.get("hardlock_base_status") != "PASS" or receipt.get("hardlock_base_head_sha") != head:
        raise PreCodexStartBlocked("PRECODEX_HARDLOCK_BASE_NOT_FRESH_PASS")
    if receipt.get("user_approval") is not True:
        raise PreCodexStartBlocked("PRECODEX_USER_APPROVAL_MISSING")
    if receipt.get("codex_capacity_status") != "AVAILABLE":
        raise PreCodexStartBlocked("PRECODEX_CODEX_CAPACITY_NOT_AVAILABLE")
    if int(receipt.get("approved_article_count") or 0) < 1:
        raise PreCodexStartBlocked("PRECODEX_ARTICLE_COUNT_NOT_APPROVED")
    if receipt.get("new_article_policy") != "COMPLETELY_NEW_NO_RECOVERY_BODY":
        raise PreCodexStartBlocked("PRECODEX_RECEIPT_NEW_ARTICLE_POLICY_INVALID")
    if receipt.get("sequential_advance_policy") != "PASS_ONLY":
        raise PreCodexStartBlocked("PRECODEX_RECEIPT_ADVANCE_POLICY_INVALID")
    if receipt.get("repair_policy") != "SAME_ARTICLE_SAME_WORKSPACE_UNTIL_PASS":
        raise PreCodexStartBlocked("PRECODEX_RECEIPT_REPAIR_POLICY_INVALID")
    if receipt.get("restart_recovery_status") != "PASS_CROSS_PROCESS_AND_DURABLE_TRANSPORT_READY":
        raise PreCodexStartBlocked("PRECODEX_RESTART_RECOVERY_NOT_READY")
    if receipt.get("durable_evidence_transport_status") != "PASS":
        raise PreCodexStartBlocked("PRECODEX_DURABLE_EVIDENCE_TRANSPORT_NOT_PASS")
    if receipt.get("codex_side_github_write_required") is not False:
        raise PreCodexStartBlocked("PRECODEX_RECEIPT_CODEX_GITHUB_POLICY_INVALID")
    if receipt.get("publish_allowed") is not False:
        raise PreCodexStartBlocked("PRECODEX_RECEIPT_PUBLISH_NOT_FALSE")

    return {
        "contract": CONTRACT,
        "status": "PRE_CODEX_START_HARDLOCK_PASS",
        "head": head,
        "approved_article_count": int(receipt["approved_article_count"]),
        "dispatcher_pr": receipt.get("dispatcher_pr"),
        "hardlock_base_run": receipt.get("hardlock_base_run"),
        "restart_recovery_status": receipt.get("restart_recovery_status"),
        "durable_evidence_transport_status": receipt.get("durable_evidence_transport_status"),
        "publish_allowed": False,
    }


def validate(repo: Path = REPO) -> dict:
    repo = Path(repo).resolve()
    state_raw = STATE.read_bytes()
    return validate_payload(
        head=_git_head(repo),
        manifest=_load(MANIFEST),
        receipt=_load(RECEIPT),
        state=json.loads(state_raw),
        root=_load(ROOT),
        state_sha256=_sha_bytes(state_raw),
    )


if __name__ == "__main__":
    try:
        print(json.dumps(validate(), ensure_ascii=False, sort_keys=True))
        raise SystemExit(0)
    except Exception as exc:
        print(json.dumps({
            "ok": False,
            "status": "PRE_CODEX_START_HARDLOCK_BLOCKED",
            "reason": str(exc),
            "publish_allowed": False,
        }, ensure_ascii=False, sort_keys=True))
        raise SystemExit(2)
