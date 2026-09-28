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

def verify_goal_contract(value: dict[str, Any]) -> None:
    expected = {
        "contract": "PFERDE_ATELIER_REASONING_ECONOMY_TARGET_V1",
        "startmaster": "STARTMASTER0107",
        "goal": "MAXIMIZE_MEDIUM_WITHOUT_ANY_GATE_OR_QUALITY_CHANGE",
        "default_reasoning": "medium",
        "downgrade_for_cost_or_speed_without_gate_parity": "FORBIDDEN",
        "success": "MEDIUM_USED_WHERE_POSSIBLE_AND_OUTPUT_PASSES_IDENTICAL_EXISTING_GATES_WITH_ZERO_RULE_CHANGES",
        "hard_execution_principle": "MEDIUM_IS_EXECUTION_DEFAULT_ONLY; ALL EXISTING DOMAIN_GATES_UNCHANGED",
        "immutable_entrance_layer": "GITHUB_PULL_REQUEST_TARGET_BASE_HARDLOCK",
    }
    for key, expected_value in expected.items():
        if value.get(key) != expected_value:
            raise Blocked("DIRECTOR_GOAL_CONTRACT_INVALID:" + key)
    never = value.get("never_trade_for_medium")
    required_never = {
        "research_completeness", "fact_binding", "title_keyword_rules",
        "duplicate_cannibalization", "LanguageTool", "PPM", "PSERC", "PSTE",
        "design", "publish_safety", "package_preflight",
    }
    if not isinstance(never, list) or set(never) != required_never:
        raise Blocked("DIRECTOR_GOAL_NEVER_TRADE_INVALID")
    allowed_escalations = value.get("escalate_above_medium_only_if")
    if not isinstance(allowed_escalations, list) or set(allowed_escalations) != {
        "existing_bound_step_explicitly_requires_higher_reasoning",
        "rootcause_or_semantic_case_cannot_be_safely_completed_at_medium_on_same_unchanged_input",
        "existing workflow explicitly marks step high-risk",
    }:
        raise Blocked("DIRECTOR_GOAL_ESCALATION_POLICY_INVALID")

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
    if name not in {"WRITE_DRAFT", "RUN_CHECKER", "REPAIR_DRAFT", "RUN_PSERC", "RUN_ENDSTEMPEL"}:
        raise Blocked("DIRECTOR_ACTION_UNKNOWN")
    if name == "RUN_CHECKER" and str(action.get("checker") or "") not in {"LT68", "PPM679"}:
        raise Blocked("DIRECTOR_CHECKER_UNKNOWN")
    return "BOUND_STEP_WORKER"

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
    progress_guard.write(checkpoint_path, new_checkpoint)
    persisted = load(checkpoint_path)
    progress_guard.verify_checkpoint(binding, persisted)
    if persisted != new_checkpoint:
        raise Blocked("DIRECTOR_PERSISTED_CHECKPOINT_MISMATCH")
    capsule = receipt.get("workspace_capsule")
    if capsule is not None and not isinstance(capsule, dict):
        raise Blocked("DIRECTOR_WORKSPACE_CAPSULE_INVALID")
    next_decision = universal_reentry_guard.build(binding, persisted, capsule)
    next_ticket = issue(binding, persisted, next_decision)
    return {
        "status": "STOP" if next_ticket["terminal"] else "CONTINUE",
        "checkpoint": persisted,
        "decision": next_decision,
        "ticket": next_ticket,
        "publish_allowed": False,
    }

def resume(
    binding: dict[str, Any],
    checkpoint_path: Path,
    capsule: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not checkpoint_path.is_file():
        raise Blocked("DIRECTOR_DURABLE_CHECKPOINT_MISSING")
    checkpoint = load(checkpoint_path)
    progress_guard.verify_checkpoint(binding, checkpoint)
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
