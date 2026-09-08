from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass, asdict
from typing import Any


class Blocked(RuntimeError):
    pass


def canon(obj: Any) -> bytes:
    return json.dumps(
        obj,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def sha(obj: Any) -> str:
    return hashlib.sha256(canon(obj)).hexdigest()


STEP_ORDER = ("RESEARCH", "TEXT_SLOT", "FINAL_CHECK")
RESULT_KEYS = {"job_id", "step_id", "input_hash", "status", "output", "output_hash"}


@dataclass(frozen=True)
class WorkerResult:
    job_id: str
    step_id: str
    input_hash: str
    status: str
    output: Any
    output_hash: str

    def to_dict(self) -> dict:
        return asdict(self)


def _valid_research(output: Any) -> bool:
    return (
        isinstance(output, dict)
        and set(output) == {"item_id", "facts"}
        and isinstance(output["item_id"], str)
        and bool(output["item_id"])
        and isinstance(output["facts"], list)
        and all(isinstance(x, str) and bool(x) for x in output["facts"])
    )


def _passes_prototype_link_rule(draft: str) -> bool:
    """
    P1 representative hard rule only.
    This is NOT claimed to be the production link rule.
    It proves that a mandatory rule can be compiled into the machine
    instead of being runtime-configurable or worker-selectable.
    """
    lowered = draft.lower()
    return "http://" not in lowered and "https://" not in lowered


def _valid_text_slot(output: Any) -> bool:
    return (
        isinstance(output, dict)
        and set(output) == {"item_id", "facts", "draft"}
        and isinstance(output["item_id"], str)
        and bool(output["item_id"])
        and isinstance(output["facts"], list)
        and all(isinstance(x, str) and bool(x) for x in output["facts"])
        and isinstance(output["draft"], str)
        and bool(output["draft"])
        and _passes_prototype_link_rule(output["draft"])
    )


def _valid_final_check(output: Any) -> bool:
    return (
        isinstance(output, dict)
        and set(output) == {"item_id", "facts", "draft", "checks"}
        and isinstance(output["item_id"], str)
        and bool(output["item_id"])
        and isinstance(output["facts"], list)
        and all(isinstance(x, str) and bool(x) for x in output["facts"])
        and isinstance(output["draft"], str)
        and bool(output["draft"])
        and output["checks"] == {"all_required_checks_passed": True}
    )


def _validate(step_id: str, output: Any) -> bool:
    if step_id == "RESEARCH":
        return _valid_research(output)
    if step_id == "TEXT_SLOT":
        return _valid_text_slot(output)
    if step_id == "FINAL_CHECK":
        return _valid_final_check(output)
    return False


class CentralMachine:
    """
    P0 architecture prototype only.

    Fixed properties:
    - fixed step order
    - no runtime-supplied validator
    - one central owner of state
    - no worker-to-worker communication
    """

    def __init__(self, job_id: str, item_id: str):
        if not isinstance(job_id, str) or not job_id:
            raise ValueError("job_id required")
        if not isinstance(item_id, str) or not item_id:
            raise ValueError("item_id required")

        self._job_id = job_id
        self._item_id = item_id
        self._index = 0
        self._payload = {"item_id": item_id}
        self._blocked = False
        self._history: list[dict[str, str]] = []

    @property
    def current_step(self) -> str | None:
        if self._blocked or self._index >= len(STEP_ORDER):
            return None
        return STEP_ORDER[self._index]

    @property
    def finished(self) -> bool:
        return not self._blocked and self._index == len(STEP_ORDER)

    def worker_input(self) -> dict:
        step_id = self.current_step
        if step_id is None:
            raise Blocked("NO_ACTIVE_STEP")

        payload = copy.deepcopy(self._payload)
        return {
            "job_id": self._job_id,
            "step_id": step_id,
            "input_hash": sha(payload),
            "payload": payload,
        }

    def submit(self, raw_result: dict) -> None:
        step_id = self.current_step
        if step_id is None:
            raise Blocked("NO_ACTIVE_STEP")

        if not isinstance(raw_result, dict) or set(raw_result) != RESULT_KEYS:
            self._block("RESULT_SCHEMA_INVALID")

        try:
            result = WorkerResult(**raw_result)
        except TypeError:
            self._block("RESULT_SCHEMA_INVALID")

        if result.job_id != self._job_id:
            self._block("JOB_ID_MISMATCH")
        if result.step_id != step_id:
            self._block("STEP_ID_MISMATCH")
        if result.input_hash != sha(self._payload):
            self._block("INPUT_HASH_MISMATCH")
        if result.status != "PASS":
            self._block("WORKER_NONPASS")
        if result.output_hash != sha(result.output):
            self._block("OUTPUT_HASH_MISMATCH")
        if not _validate(step_id, result.output):
            self._block("VALIDATOR_FAIL")
        if result.output.get("item_id") != self._item_id:
            self._block("ITEM_ID_MISMATCH")

        self._history.append(
            {
                "step_id": step_id,
                "input_hash": result.input_hash,
                "output_hash": result.output_hash,
            }
        )
        self._payload = copy.deepcopy(result.output)
        self._index += 1

    def snapshot(self) -> dict:
        return {
            "job_id": self._job_id,
            "item_id": self._item_id,
            "current_step": self.current_step,
            "finished": self.finished,
            "blocked": self._blocked,
            "payload": copy.deepcopy(self._payload),
            "history": copy.deepcopy(self._history),
        }

    def final_output(self) -> dict:
        if not self.finished:
            raise Blocked("NOT_FINISHED")
        return copy.deepcopy(self._payload)

    def _block(self, code: str):
        self._blocked = True
        raise Blocked(code)


def make_result(worker_input: dict, output: Any, status: str = "PASS") -> dict:
    return {
        "job_id": worker_input["job_id"],
        "step_id": worker_input["step_id"],
        "input_hash": worker_input["input_hash"],
        "status": status,
        "output": output,
        "output_hash": sha(output),
    }
