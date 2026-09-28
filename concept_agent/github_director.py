#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
GOAL_CONTRACT_PATH = REPO / "control/startmaster0107/ZIELVERTRAG_REASONING_MEDIUM_MAX_STARTMASTER0107.json"
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import progress_guard
import universal_reentry_guard

TICKET_CONTRACT = "CONCEPT_AGENT_GITHUB_DIRECTOR_TICKET_V1"
RECEIPT_CONTRACT = "CONCEPT_AGENT_GITHUB_DIRECTOR_RECEIPT_V1"
SHA_RE = re.compile(r"^[0-9a-f]{64}$")

class Blocked(RuntimeError):
    pass

def canon(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")

def stable(value: Any) -> str:
    return hashlib.sha256(canon(value)).hexdigest()

def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise Blocked("JSON_OBJECT_REQUIRED:" + str(path))
    return value

EXPECTED_GOAL_CONTRACT = {
    "contract": "PFERDE_ATELIER_REASONING_ECONOMY_TARGET_V1",
    "startmaster": "STARTMASTER0107",
    "goal": "MAXIMIZE_MEDIUM_WITHOUT_ANY_GATE_OR_QUALITY_CHANGE",
    "default_reasoning": "medium",
    "applies_to": [
        "text_generation",
        "routine_bound_transformations",
        "deterministic_workflow_navigation",
        "routine_metadata_work",
    ],
    "escalate_above_medium_only_if": [
        "existing_bound_step_explicitly_requires_higher_reasoning",
        "rootcause_or_semantic_case_cannot_be_safely_completed_at_medium_on_same_unchanged_input",
        "existing workflow explicitly marks step high-risk",
    ],
    "never_trade_for_medium": [
        "research_completeness",
        "fact_binding",
        "title_keyword_rules",
        "duplicate_cannibalization",
        "LanguageTool",
        "PPM",
        "PSERC",
        "PSTE",
        "design",
        "publish_safety",
        "package_preflight",
    ],
    "downgrade_for_cost_or_speed_without_gate_parity": "FORBIDDEN",
    "measurement": [
        "articles_per_batch",
        "wall_clock_per_article",
        "repeated_gate_count",
        "backtrack_count",
        "quality_gate_pass_rate",
    ],
    "success": "MEDIUM_USED_WHERE_POSSIBLE_AND_OUTPUT_PASSES_IDENTICAL_EXISTING_GATES_WITH_ZERO_RULE_CHANGES",
    "hard_execution_principle": "MEDIUM_IS_EXECUTION_DEFAULT_ONLY; ALL EXISTING DOMAIN_GATES_UNCHANGED",
    "immutable_entrance_layer": "GITHUB_PULL_REQUEST_TARGET_BASE_HARDLOCK",
}

def verify_goal_contract(value: dict[str, Any]) -> None:
    if not isinstance(value, dict):
        raise Blocked("DIRECTOR_GOAL_CONTRACT_OBJECT_REQUIRED")
    if set(value) != set(EXPECTED_GOAL_CONTRACT):
        raise Blocked("DIRECTOR_GOAL_CONTRACT_KEYS_INVALID")
    for key, expected_value in EXPECTED_GOAL_CONTRACT.items():
        if value.get(key) != expected_value:
            raise Blocked("DIRECTOR_GOAL_CONTRACT_INVALID:" + key)

def current_goal_contract() -> dict[str, Any]:
    value = load(GOAL_CONTRACT_PATH)
    verify_goal_contract(value)
    return value

def _inside(root: Path, rel: str) -> Path:
    if not isinstance(rel, str) or not rel or Path(rel).is_absolute():
        raise Blocked("ARTIFACT_RELPATH_INVALID")
    root = root.resolve()
    path = (root / rel).resolve()
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise Blocked("ARTIFACT_OUTSIDE_WORK_ROOT") from exc
    if not path.is_file():
        raise Blocked("ARTIFACT_MISSING")
    return path

def _worker_role(action: dict[str, Any]) -> str | None:
    name = action.get("action")
    if name == "STOP":
        return None
    if name == "WRITE_DRAFT":
        return "WRITE_DRAFT_WORKER"
    if name == "REPAIR_DRAFT":
        return "REPAIR_DRAFT_WORKER"
    if name == "RUN_PSERC":
        return "PSERC_WORKER"
    if name == "RUN_ENDSTEMPEL":
        return "ENDSTEMPEL_WORKER"
    if name == "RUN_CHECKER":
        checker = str(action.get("checker") or "")
        if checker == "LT68":
            return "LT68_WORKER"
        if checker == "PPM679":
            return "PPM679_WORKER"
        raise Blocked("DIRECTOR_CHECKER_UNKNOWN")
    raise Blocked("DIRECTOR_ACTION_UNKNOWN")

def issue(binding: dict[str, Any], checkpoint: dict[str, Any], decision: dict[str, Any]) -> dict[str, Any]:
    progress_guard.verify_checkpoint(binding, checkpoint)
    progress_guard.verify_reentry_decision(binding, checkpoint, decision)
    goal = current_goal_contract()
    action = checkpoint["allowed_action"]
    if decision.get("allowed_action") != action:
        raise Blocked("DIRECTOR_DECISION_ACTION_MISMATCH")
    terminal = action.get("action") == "STOP"
    core = {
        "contract": TICKET_CONTRACT,
        "batch_sha256": checkpoint["batch_sha256"],
        "production_binding_sha256": binding["binding_sha256"],
        "checkpoint_sha256": checkpoint["checkpoint_sha256"],
        "decision_sha256": decision["decision_sha256"],
        "allowed_action": json.loads(json.dumps(action)),
        "allowed_action_sha256": stable(action),
        "worker_role": _worker_role(action),
        "reasoning_effort": goal["default_reasoning"],
        "quality_gate_change_allowed": False,
        "terminal": terminal,
        "exactly_once_for_checkpoint": True,
        "director_may_choose_action": False,
        "director_content_authority": "NONE",
        "director_quality_authority": "NONE",
        "alternate_route_allowed": False,
        "history_reconstruction_allowed": False,
        "publish_allowed": False,
    }
    ticket = dict(core)
    ticket["ticket_sha256"] = stable(core)
    return ticket

def verify_ticket(binding: dict[str, Any], checkpoint: dict[str, Any], decision: dict[str, Any], ticket: dict[str, Any]) -> None:
    progress_guard.verify_checkpoint(binding, checkpoint)
    progress_guard.verify_reentry_decision(binding, checkpoint, decision)
    if not isinstance(ticket, dict) or ticket.get("contract") != TICKET_CONTRACT:
        raise Blocked("DIRECTOR_TICKET_CONTRACT_INVALID")
    core = dict(ticket)
    declared = core.pop("ticket_sha256", None)
    if not isinstance(declared, str) or not SHA_RE.fullmatch(declared) or declared != stable(core):
        raise Blocked("DIRECTOR_TICKET_HASH_MISMATCH")
    expected = issue(binding, checkpoint, decision)
    if ticket != expected:
        raise Blocked("DIRECTOR_TICKET_NOT_EXACT_CURRENT")
    if ticket.get("publish_allowed") is not False or ticket.get("alternate_route_allowed") is not False:
        raise Blocked("DIRECTOR_TICKET_POLICY_INVALID")

def _verify_receipt(ticket: dict[str, Any], receipt: dict[str, Any]) -> None:
    if not isinstance(receipt, dict) or receipt.get("contract") != RECEIPT_CONTRACT:
        raise Blocked("DIRECTOR_RECEIPT_CONTRACT_INVALID")
    base_keys = {
        "contract", "status", "ticket_sha256", "checkpoint_sha256",
        "allowed_action_sha256", "worker_role", "reasoning_effort", "publish_allowed",
        "workflow_change_requested", "quality_gate_change_requested", "next_action",
    }
    action = str((ticket.get("allowed_action") or {}).get("action") or "")
    if action in {"WRITE_DRAFT", "REPAIR_DRAFT"}:
        allowed_keys = base_keys | {"artifact_relpath", "artifact_sha256", "workspace_capsule"}
    elif action == "RUN_CHECKER":
        allowed_keys = base_keys | {"artifact_relpath", "artifact_sha256", "result", "workspace_capsule"}
    elif action in {"RUN_PSERC", "RUN_ENDSTEMPEL"}:
        allowed_keys = base_keys | {"result"}
    else:
        raise Blocked("DIRECTOR_RECEIPT_ACTION_INVALID")
    extra = sorted(set(receipt) - allowed_keys)
    if extra:
        raise Blocked("DIRECTOR_RECEIPT_EXTRA_FIELDS_FORBIDDEN:" + ",".join(extra))
    if receipt.get("status") != "COMPLETED":
        raise Blocked("DIRECTOR_RECEIPT_NOT_COMPLETED")
    if receipt.get("ticket_sha256") != ticket.get("ticket_sha256"):
        raise Blocked("DIRECTOR_RECEIPT_TICKET_MISMATCH")
    if receipt.get("checkpoint_sha256") != ticket.get("checkpoint_sha256"):
        raise Blocked("DIRECTOR_RECEIPT_CHECKPOINT_MISMATCH")
    if receipt.get("allowed_action_sha256") != ticket.get("allowed_action_sha256"):
        raise Blocked("DIRECTOR_RECEIPT_ACTION_MISMATCH")
    if receipt.get("worker_role") != ticket.get("worker_role"):
        raise Blocked("DIRECTOR_RECEIPT_WORKER_MISMATCH")
    if receipt.get("reasoning_effort") != ticket.get("reasoning_effort"):
        raise Blocked("DIRECTOR_RECEIPT_REASONING_MISMATCH")
    if receipt.get("quality_gate_change_requested") is not False:
        raise Blocked("DIRECTOR_RECEIPT_QUALITY_CHANGE_FORBIDDEN")
    if receipt.get("publish_allowed") is not False:
        raise Blocked("DIRECTOR_RECEIPT_PUBLISH_INVALID")
    if receipt.get("workflow_change_requested") is not False:
        raise Blocked("DIRECTOR_RECEIPT_WORKFLOW_CHANGE_FORBIDDEN")
    if receipt.get("next_action") is not None:
        raise Blocked("DIRECTOR_RECEIPT_NEXT_ACTION_FORBIDDEN")

def accept(
    binding: dict[str, Any],
    checkpoint: dict[str, Any],
    decision: dict[str, Any],
    ticket: dict[str, Any],
    receipt: dict[str, Any],
    work_root: Path,
) -> dict[str, Any]:
    verify_ticket(binding, checkpoint, decision, ticket)
    if ticket["terminal"]:
        raise Blocked("DIRECTOR_STOP_ACCEPTS_NO_WORKER_RECEIPT")
    _verify_receipt(ticket, receipt)
    action = ticket["allowed_action"]
    name = action["action"]

    if name in {"WRITE_DRAFT", "REPAIR_DRAFT"}:
        path = _inside(work_root, str(receipt.get("artifact_relpath") or ""))
        if receipt.get("artifact_sha256") != file_sha(path):
            raise Blocked("DIRECTOR_ARTIFACT_HASH_MISMATCH")
        index = int(action["item_index"])
        if name == "WRITE_DRAFT":
            return progress_guard.record_draft(binding, checkpoint, decision, index, path)
        return progress_guard.replace_draft(binding, checkpoint, decision, index, path)

    if name == "RUN_CHECKER":
        path = _inside(work_root, str(receipt.get("artifact_relpath") or ""))
        if receipt.get("artifact_sha256") != file_sha(path):
            raise Blocked("DIRECTOR_ARTIFACT_HASH_MISMATCH")
        result = receipt.get("result")
        if not isinstance(result, dict):
            raise Blocked("DIRECTOR_CHECK_RESULT_MISSING")
        return progress_guard.record_check(
            binding,
            checkpoint,
            decision,
            int(action["item_index"]),
            str(action["checker"]),
            result,
            path,
        )

    if name in {"RUN_PSERC", "RUN_ENDSTEMPEL"}:
        result = receipt.get("result")
        if not isinstance(result, dict):
            raise Blocked("DIRECTOR_BATCH_RESULT_MISSING")
        stage = "PSERC" if name == "RUN_PSERC" else "ENDSTEMPEL"
        return progress_guard.record_batch_stage(binding, checkpoint, decision, stage, result)

    raise Blocked("DIRECTOR_ACTION_NOT_ACCEPTABLE")

def _capsule_dir(checkpoint_path: Path) -> Path:
    return checkpoint_path.parent / ".github-director-capsules"

def _capsule_path(checkpoint_path: Path, checkpoint_sha256: str) -> Path:
    if not SHA_RE.fullmatch(str(checkpoint_sha256 or "")):
        raise Blocked("DIRECTOR_CAPSULE_CHECKPOINT_HASH_INVALID")
    return _capsule_dir(checkpoint_path) / (checkpoint_sha256 + ".json")

def _persist_capsule_file(checkpoint_path: Path, checkpoint_sha256: str, capsule: dict[str, Any]) -> None:
    path = _capsule_path(checkpoint_path, checkpoint_sha256)
    path.parent.mkdir(parents=True, exist_ok=True)
    wrapper = {
        "contract": "CONCEPT_AGENT_GITHUB_DIRECTOR_CAPSULE_BINDING_V1",
        "checkpoint_sha256": checkpoint_sha256,
        "capsule": capsule,
        "capsule_sha256": stable(capsule),
        "publish_allowed": False,
    }
    progress_guard.write(path, wrapper)

def _load_capsule_file(checkpoint_path: Path, checkpoint_sha256: str) -> dict[str, Any]:
    path = _capsule_path(checkpoint_path, checkpoint_sha256)
    if not path.is_file():
        raise Blocked("DIRECTOR_BOUND_WORKSPACE_CAPSULE_MISSING")
    wrapper = load(path)
    if wrapper.get("contract") != "CONCEPT_AGENT_GITHUB_DIRECTOR_CAPSULE_BINDING_V1":
        raise Blocked("DIRECTOR_CAPSULE_BINDING_CONTRACT_INVALID")
    if wrapper.get("checkpoint_sha256") != checkpoint_sha256:
        raise Blocked("DIRECTOR_CAPSULE_BINDING_CHECKPOINT_MISMATCH")
    capsule = wrapper.get("capsule")
    if not isinstance(capsule, dict) or wrapper.get("capsule_sha256") != stable(capsule):
        raise Blocked("DIRECTOR_CAPSULE_BINDING_HASH_MISMATCH")
    if wrapper.get("publish_allowed") is not False:
        raise Blocked("DIRECTOR_CAPSULE_BINDING_PUBLISH_INVALID")
    return capsule

def persist_and_continue(
    binding: dict[str, Any],
    checkpoint: dict[str, Any],
    decision: dict[str, Any],
    ticket: dict[str, Any],
    receipt: dict[str, Any],
    work_root: Path,
    checkpoint_path: Path,
) -> dict[str, Any]:
    if not checkpoint_path.is_file():
        raise Blocked("DIRECTOR_DURABLE_CHECKPOINT_MISSING")
    current_durable = load(checkpoint_path)
    progress_guard.verify_checkpoint(binding, current_durable)
    if current_durable != checkpoint:
        raise Blocked("DIRECTOR_STALE_CHECKPOINT_REPLAY_BLOCKED")
    new_checkpoint = accept(binding, checkpoint, decision, ticket, receipt, work_root)
    progress_guard.verify_checkpoint(binding, new_checkpoint)
    next_action = new_checkpoint["allowed_action"]["action"]
    capsule = receipt.get("workspace_capsule")
    capsule_required = next_action in {"RUN_CHECKER", "REPAIR_DRAFT"}
    if capsule_required:
        if not isinstance(capsule, dict):
            raise Blocked("DIRECTOR_WORKSPACE_CAPSULE_REQUIRED")
        universal_reentry_guard.build(binding, new_checkpoint, capsule)
        _persist_capsule_file(checkpoint_path, new_checkpoint["checkpoint_sha256"], capsule)
    elif capsule is not None:
        raise Blocked("DIRECTOR_UNEXPECTED_WORKSPACE_CAPSULE")
    progress_guard.write(checkpoint_path, new_checkpoint)
    persisted = load(checkpoint_path)
    progress_guard.verify_checkpoint(binding, persisted)
    if persisted != new_checkpoint:
        raise Blocked("DIRECTOR_PERSISTED_CHECKPOINT_MISMATCH")
    return resume(binding, checkpoint_path)

def resume(
    binding: dict[str, Any],
    checkpoint_path: Path,
) -> dict[str, Any]:
    if not checkpoint_path.is_file():
        raise Blocked("DIRECTOR_DURABLE_CHECKPOINT_MISSING")
    checkpoint = load(checkpoint_path)
    progress_guard.verify_checkpoint(binding, checkpoint)
    action = checkpoint["allowed_action"]["action"]
    capsule = None
    if action in {"RUN_CHECKER", "REPAIR_DRAFT"}:
        capsule = _load_capsule_file(checkpoint_path, checkpoint["checkpoint_sha256"])
    decision = universal_reentry_guard.build(binding, checkpoint, capsule)
    ticket = issue(binding, checkpoint, decision)
    return {
        "status": "STOP" if ticket["terminal"] else "CONTINUE",
        "checkpoint": checkpoint,
        "decision": decision,
        "ticket": ticket,
        "publish_allowed": False,
    }

def main(argv: list[str]) -> int:
    try:
        if len(argv) == 6 and argv[1] == "issue":
            binding = load(Path(argv[2]))
            checkpoint = load(Path(argv[3]))
            decision = load(Path(argv[4]))
            progress_guard.write(Path(argv[5]), issue(binding, checkpoint, decision))
            print("CONCEPT_AGENT_GITHUB_DIRECTOR_TICKET_READY")
            return 0
        raise Blocked("USE: github_director.py issue BINDING CHECKPOINT DECISION OUT_TICKET")
    except Exception as exc:
        print("CONCEPT_AGENT_GITHUB_DIRECTOR_BLOCKED:" + str(exc), file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
