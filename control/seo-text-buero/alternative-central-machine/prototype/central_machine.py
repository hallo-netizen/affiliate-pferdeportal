from __future__ import annotations
import copy, hashlib, json
from dataclasses import dataclass, asdict
from typing import Any, Callable

class Blocked(RuntimeError):
    pass

def canon(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

def sha(obj: Any) -> str:
    return hashlib.sha256(canon(obj)).hexdigest()

RESULT_KEYS = {"job_id","step_id","input_hash","status","output","output_hash"}

@dataclass(frozen=True)
class WorkerResult:
    job_id: str
    step_id: str
    input_hash: str
    status: str
    output: Any
    output_hash: str
    def to_dict(self):
        return asdict(self)

class CentralMachine:
    """Architecture POC only. No production/text-machine logic."""

    def __init__(self, job_id: str, initial_payload: Any, steps: list[str]):
        if not job_id or not steps:
            raise ValueError("job_id and steps required")
        self._job_id = job_id
        self._steps = tuple(steps)
        self._index = 0
        self._payload = copy.deepcopy(initial_payload)
        self._history = []
        self._blocked = False

    @property
    def current_step(self):
        if self._blocked or self._index >= len(self._steps):
            return None
        return self._steps[self._index]

    @property
    def finished(self):
        return not self._blocked and self._index == len(self._steps)

    def worker_input(self):
        if self.current_step is None:
            raise Blocked("NO_ACTIVE_STEP")
        payload = copy.deepcopy(self._payload)
        return {
            "job_id": self._job_id,
            "step_id": self.current_step,
            "input_hash": sha(payload),
            "payload": payload,
        }

    def submit(self, raw_result: dict, validator: Callable[[Any], bool]):
        if self.current_step is None:
            raise Blocked("NO_ACTIVE_STEP")
        if set(raw_result.keys()) != RESULT_KEYS:
            self._blocked = True
            raise Blocked("RESULT_SCHEMA_INVALID")
        try:
            result = WorkerResult(**raw_result)
        except TypeError as exc:
            self._blocked = True
            raise Blocked("RESULT_SCHEMA_INVALID") from exc

        if result.job_id != self._job_id:
            self._blocked = True
            raise Blocked("JOB_ID_MISMATCH")
        if result.step_id != self.current_step:
            self._blocked = True
            raise Blocked("STEP_ID_MISMATCH")
        if result.input_hash != sha(self._payload):
            self._blocked = True
            raise Blocked("INPUT_HASH_MISMATCH")
        if result.status != "PASS":
            self._blocked = True
            raise Blocked("WORKER_NONPASS")
        if result.output_hash != sha(result.output):
            self._blocked = True
            raise Blocked("OUTPUT_HASH_MISMATCH")
        if validator(result.output) is not True:
            self._blocked = True
            raise Blocked("VALIDATOR_FAIL")

        self._history.append({
            "step_id": result.step_id,
            "input_hash": result.input_hash,
            "output_hash": result.output_hash,
        })
        self._payload = copy.deepcopy(result.output)
        self._index += 1

    def checkpoint(self):
        return {
            "job_id": self._job_id,
            "steps": list(self._steps),
            "index": self._index,
            "payload": copy.deepcopy(self._payload),
            "history": copy.deepcopy(self._history),
            "blocked": self._blocked,
        }

    @classmethod
    def restore(cls, cp: dict):
        required = {"job_id","steps","index","payload","history","blocked"}
        if set(cp.keys()) != required:
            raise Blocked("CHECKPOINT_SCHEMA_INVALID")
        obj = cls(cp["job_id"], cp["payload"], cp["steps"])
        obj._index = cp["index"]
        obj._history = copy.deepcopy(cp["history"])
        obj._blocked = cp["blocked"]
        if not isinstance(obj._index, int) or not 0 <= obj._index <= len(obj._steps):
            raise Blocked("CHECKPOINT_INDEX_INVALID")
        if len(obj._history) != obj._index:
            raise Blocked("CHECKPOINT_HISTORY_INVALID")
        for i, rec in enumerate(obj._history):
            if set(rec.keys()) != {"step_id","input_hash","output_hash"}:
                raise Blocked("CHECKPOINT_HISTORY_INVALID")
            if rec["step_id"] != obj._steps[i]:
                raise Blocked("CHECKPOINT_STEP_ORDER_INVALID")
        return obj

    def final_package(self):
        if not self.finished:
            raise Blocked("NOT_FINISHED")
        body = {
            "job_id": self._job_id,
            "final_payload": copy.deepcopy(self._payload),
            "history": copy.deepcopy(self._history),
        }
        return {"body": body, "package_hash": sha(body)}

def make_result(worker_input: dict, output: Any, status: str="PASS"):
    return {
        "job_id": worker_input["job_id"],
        "step_id": worker_input["step_id"],
        "input_hash": worker_input["input_hash"],
        "status": status,
        "output": output,
        "output_hash": sha(output),
    }
