#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
CONCEPT_AGENT = HERE.parent
if str(CONCEPT_AGENT) not in sys.path:
    sys.path.insert(0, str(CONCEPT_AGENT))

from .engine import k8_progress_guard as progress_guard
from .engine import k8_universal_reentry_guard as universal_reentry_guard
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
from . import k8_command_gate

EXECUTE = "K8_VERBOT_EXECUTE_EXACT_CURRENT_ACTION"

class Blocked(RuntimeError):
    pass

def attempt(
    binding: dict[str, Any],
    checkpoint: dict[str, Any],
    proposal: Any,
    capsule: dict[str, Any] | None = None,
) -> dict[str, Any]:
    verdict = k8_command_gate.admit(binding, checkpoint, proposal)
    if verdict["status"] != k8_command_gate.PASS:
        return {
            **verdict,
            "execution": None,
            "continuation_required": verdict["allowed_action"].get("action") != "STOP",
        }

    decision = universal_reentry_guard.build(binding, checkpoint, capsule)
    resumed = progress_guard.resume(binding, checkpoint, decision)

    if resumed.get("checkpoint_sha256") != checkpoint.get("checkpoint_sha256"):
        raise Blocked("K8_RESUME_CHECKPOINT_DRIFT")
    if resumed.get("allowed_action") != checkpoint.get("allowed_action"):
        raise Blocked("K8_RESUME_ACTION_DRIFT")
    if resumed.get("publish_allowed") is not False:
        raise Blocked("K8_RESUME_PUBLISH_INVALID")

    return {
        "status": EXECUTE,
        "checkpoint_sha256": checkpoint["checkpoint_sha256"],
        "allowed_action": resumed["allowed_action"],
        "execution": resumed,
        "continuation_required": resumed["continuation_required"],
        "state_changed": False,
        "publish_allowed": False,
    }

def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise Blocked("JSON_OBJECT_REQUIRED:" + str(path))
    return value

def main(argv: list[str]) -> int:
    try:
        if len(argv) not in {5, 6} or argv[1] != "attempt":
            raise Blocked("USE: k8_entry.py attempt BINDING CHECKPOINT PROPOSAL [CAPSULE]")
        binding = load(Path(argv[2]))
        checkpoint = load(Path(argv[3]))
        proposal = load(Path(argv[4]))
        capsule = load(Path(argv[5])) if len(argv) == 6 else None
        result = attempt(binding, checkpoint, proposal, capsule)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0 if result["status"] == EXECUTE else 3
    except Exception as exc:
        print("K8_VERBOT_ENTRY_HARD_BLOCK:" + str(exc), file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
