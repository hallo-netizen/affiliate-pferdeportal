#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
CONCEPT_AGENT = HERE.parent
if str(CONCEPT_AGENT) not in sys.path:
    sys.path.insert(0, str(CONCEPT_AGENT))

from .engine import k8_progress_guard as progress_guard

CONTRACT = "K8_VERBOT_COMMAND_V1"
PASS = "K8_VERBOT_EXACT_COMMAND_ALLOWED"
BLOCKED = "K8_VERBOT_BLOCKED_KEEP_SAME_CHECKPOINT"
EXACT_KEYS = {"contract", "checkpoint_sha256", "command"}

class Blocked(RuntimeError):
    pass

def _same_view(checkpoint: dict[str, Any], reason: str) -> dict[str, Any]:
    return {
        "status": BLOCKED,
        "reason": reason,
        "checkpoint_sha256": checkpoint["checkpoint_sha256"],
        "allowed_action": copy.deepcopy(checkpoint["allowed_action"]),
        "state_changed": False,
        "retry_same_action": checkpoint["allowed_action"].get("action") != "STOP",
        "publish_allowed": False,
    }

def admit(binding: dict[str, Any], checkpoint: dict[str, Any], proposal: Any) -> dict[str, Any]:
    # The authoritative state must itself be valid. A damaged checkpoint is not
    # treated as a chat mistake; it is a hard stop.
    progress_guard.verify_checkpoint(binding, checkpoint)

    if not isinstance(proposal, dict):
        return _same_view(checkpoint, "COMMAND_MISSING_OR_NOT_OBJECT")
    if set(proposal) != EXACT_KEYS:
        return _same_view(checkpoint, "COMMAND_FIELDS_NOT_EXACT")
    if proposal.get("contract") != CONTRACT:
        return _same_view(checkpoint, "COMMAND_CONTRACT_INVALID")
    if proposal.get("checkpoint_sha256") != checkpoint.get("checkpoint_sha256"):
        return _same_view(checkpoint, "COMMAND_STALE_OR_WRONG_CHECKPOINT")
    if proposal.get("command") != checkpoint.get("allowed_action"):
        return _same_view(checkpoint, "COMMAND_NOT_EXACT_CURRENT_ACTION")

    return {
        "status": PASS,
        "checkpoint_sha256": checkpoint["checkpoint_sha256"],
        "allowed_action": copy.deepcopy(checkpoint["allowed_action"]),
        "state_changed": False,
        "retry_same_action": False,
        "publish_allowed": False,
    }

def proposal_for(checkpoint: dict[str, Any]) -> dict[str, Any]:
    return {
        "contract": CONTRACT,
        "checkpoint_sha256": checkpoint["checkpoint_sha256"],
        "command": copy.deepcopy(checkpoint["allowed_action"]),
    }

def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise Blocked("JSON_OBJECT_REQUIRED:" + str(path))
    return value

def main(argv: list[str]) -> int:
    try:
        if len(argv) != 5 or argv[1] != "admit":
            raise Blocked("USE: k8_command_gate.py admit BINDING CHECKPOINT PROPOSAL")
        result = admit(load(Path(argv[2])), load(Path(argv[3])), load(Path(argv[4])))
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0 if result["status"] == PASS else 3
    except Exception as exc:
        print("K8_VERBOT_HARD_BLOCK:" + str(exc), file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
