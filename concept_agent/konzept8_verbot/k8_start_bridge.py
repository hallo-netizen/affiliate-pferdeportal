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

import intake_bridge  # type: ignore
import production_bridge  # type: ignore
import progress_guard  # type: ignore
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import k8_command_gate  # type: ignore
import k8_entry  # type: ignore

START_READY = "K8_VERBOT_START_READY"

class Blocked(RuntimeError):
    pass

def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise Blocked("JSON_OBJECT_REQUIRED:" + str(path))
    return value

def _write_once_or_identical(path: Path, value: dict[str, Any], identity_key: str) -> None:
    if path.is_file():
        existing = load(path)
        if existing.get(identity_key) != value.get(identity_key) or existing != value:
            raise Blocked("K8_EXISTING_STATE_CONFLICT:" + path.name)
        return
    progress_guard.write(path, value)

def start(
    snapshot: dict[str, Any],
    research_bound: dict[str, Any],
    state_dir: Path,
    proposal: Any = None,
) -> dict[str, Any]:
    intake = intake_bridge.prepare(snapshot)
    binding = production_bridge.build(snapshot, intake, research_bound)

    state_dir.mkdir(parents=True, exist_ok=True)
    binding_path = state_dir / "K8_PRODUCTION_BINDING.json"
    checkpoint_path = state_dir / "K8_PROGRESS.json"

    _write_once_or_identical(binding_path, binding, "binding_sha256")

    if checkpoint_path.is_file():
        checkpoint = load(checkpoint_path)
        progress_guard.verify_checkpoint(binding, checkpoint)
        resumed = True
    else:
        checkpoint = production_bridge.initial_checkpoint(binding)
        progress_guard.write(checkpoint_path, checkpoint)
        resumed = False

    if proposal is None:
        return {
            "status": START_READY,
            "resumed_existing_checkpoint": resumed,
            "batch_sha256": binding["batch_sha256"],
            "binding_sha256": binding["binding_sha256"],
            "checkpoint_sha256": checkpoint["checkpoint_sha256"],
            "allowed_action": copy.deepcopy(checkpoint["allowed_action"]),
            "required_command": k8_command_gate.proposal_for(checkpoint),
            "state_changed": not resumed,
            "publish_allowed": False,
        }

    result = k8_entry.attempt(binding, checkpoint, proposal)
    return {
        **result,
        "resumed_existing_checkpoint": resumed,
        "batch_sha256": binding["batch_sha256"],
        "binding_sha256": binding["binding_sha256"],
        "required_command": k8_command_gate.proposal_for(checkpoint),
        "publish_allowed": False,
    }

def main(argv: list[str]) -> int:
    try:
        if len(argv) not in {5, 6} or argv[1] != "start":
            raise Blocked("USE: k8_start_bridge.py start SNAPSHOT RESEARCH_BOUND STATE_DIR [PROPOSAL]")
        proposal = load(Path(argv[5])) if len(argv) == 6 else None
        result = start(load(Path(argv[2])), load(Path(argv[3])), Path(argv[4]), proposal)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        if result["status"] in {START_READY, k8_entry.EXECUTE}:
            return 0
        return 3
    except Exception as exc:
        print("K8_VERBOT_START_BLOCKED:" + str(exc), file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
