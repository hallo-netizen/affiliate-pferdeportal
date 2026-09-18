#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import system4_107007_entry as entry

CONTRACT = "SYSTEM4_107007_PRODUCTION_BATCH_V1"
STATE_NAME = "SYSTEM4_107007_BATCH_STATE.json"
BATCH_GATE = entry.REPO / "isolated_system4/batch_gate.py"


class Blocked(RuntimeError):
    pass


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise Blocked("SYSTEM4_107007_BATCH_JSON_OBJECT_REQUIRED")
    return value


def write_atomic(path: Path, value: dict) -> None:
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(path)


def outside_repo(path: Path) -> Path:
    try:
        return entry.outside_repo(path)
    except Exception as exc:
        raise Blocked(str(exc)) from exc


def _runtime() -> tuple[dict, list[dict]]:
    try:
        runtime, _, items = entry.require_107007(0)
    except Exception as exc:
        raise Blocked(str(exc)) from exc
    if not items:
        raise Blocked("SYSTEM4_107007_BATCH_EMPTY")
    return runtime, items


def _state_path(batch_root: Path) -> Path:
    return batch_root / STATE_NAME


def _workspace(batch_root: Path, index: int) -> Path:
    return batch_root / f"item-{index:06d}"


def _validate_point0_all(point0: Path, runtime: dict, items: list[dict]) -> None:
    for index in range(len(items)):
        try:
            entry.verify_point0_binding(point0, runtime, items, index)
        except Exception as exc:
            raise Blocked("SYSTEM4_107007_BATCH_POINT0_INVALID:" + str(exc)) from exc


def _new_state(point0: Path, runtime: dict, items: list[dict]) -> dict:
    return {
        "contract": CONTRACT,
        "status": "ACTIVE",
        "sequence": 107007,
        "batch_sha256": runtime["batch_sha256"],
        "point0_sha256": sha256(point0),
        "item_count": len(items),
        "current_index": 0,
        "completed_indices": [],
        "started_indices": [],
        "batch_collect": None,
        "publish_allowed": False,
    }


def _validate_state(state: dict, point0: Path, batch_root: Path, runtime: dict, items: list[dict]) -> None:
    if state.get("contract") != CONTRACT or state.get("sequence") != 107007:
        raise Blocked("SYSTEM4_107007_BATCH_STATE_CONTRACT_INVALID")
    if state.get("publish_allowed") is not False:
        raise Blocked("SYSTEM4_107007_BATCH_PUBLISH_FLAG_INVALID")
    if state.get("batch_sha256") != runtime.get("batch_sha256"):
        raise Blocked("SYSTEM4_107007_BATCH_RUNTIME_DRIFT")
    if state.get("point0_sha256") != sha256(point0):
        raise Blocked("SYSTEM4_107007_BATCH_POINT0_DRIFT")
    if state.get("item_count") != len(items):
        raise Blocked("SYSTEM4_107007_BATCH_COUNT_DRIFT")
    completed = state.get("completed_indices")
    started = state.get("started_indices")
    if not isinstance(completed, list) or not isinstance(started, list):
        raise Blocked("SYSTEM4_107007_BATCH_PROGRESS_INVALID")
    if completed != list(range(len(completed))):
        raise Blocked("SYSTEM4_107007_BATCH_COMPLETED_SEQUENCE_INVALID")
    if started != list(range(len(started))):
        raise Blocked("SYSTEM4_107007_BATCH_STARTED_SEQUENCE_INVALID")
    if len(completed) > len(started) or len(started) > len(items):
        raise Blocked("SYSTEM4_107007_BATCH_PROGRESS_RANGE_INVALID")
    status = state.get("status")
    if status not in {"ACTIVE", "ITEMS_COMPLETE"}:
        raise Blocked("SYSTEM4_107007_BATCH_STATUS_INVALID")
    if status == "ITEMS_COMPLETE":
        if len(completed) != len(items) or len(started) != len(items):
            raise Blocked("SYSTEM4_107007_BATCH_COMPLETE_COUNT_INVALID")
        collect = state.get("batch_collect")
        expected_evidence = batch_root / "batch-collect" / "system4_batch_evidence.json"
        if (
            not isinstance(collect, dict)
            or collect.get("status") != "SYSTEM4_BATCH_FULL_PASS_COLLECTED"
            or collect.get("batch_sha256") != state.get("batch_sha256")
            or collect.get("article_count") != len(items)
            or collect.get("batch_evidence_path") != str(expected_evidence)
            or not expected_evidence.is_file()
            or collect.get("batch_evidence_sha256") != sha256(expected_evidence)
        ):
            raise Blocked("SYSTEM4_107007_BATCH_COLLECT_PROOF_INVALID")
    else:
        if state.get("batch_collect") is not None:
            raise Blocked("SYSTEM4_107007_BATCH_EARLY_COLLECT_FORBIDDEN")
        current = state.get("current_index")
        if not isinstance(current, int) or isinstance(current, bool) or current != len(completed):
            raise Blocked("SYSTEM4_107007_BATCH_CURRENT_INDEX_INVALID")
        if len(started) not in {len(completed), len(completed) + 1}:
            raise Blocked("SYSTEM4_107007_BATCH_ACTIVE_START_COUNT_INVALID")


def _item_passed(batch_root: Path, index: int, item: dict) -> bool:
    state_path = _workspace(batch_root, index) / "state.json"
    if not state_path.is_file():
        return False
    state = load(state_path)
    article = state.get("article")
    checks = state.get("checks")
    if not isinstance(article, dict) or not isinstance(checks, dict):
        return False
    return (
        state.get("phase") == "OUTPUT_GATE_REQUIRED"
        and checks.get("status") == "PASS"
        and article.get("plan_slot") == item.get("plan_slot")
        and article.get("canonical_article_id") == item.get("canonical_article_id")
        and article.get("target_keyword") == item.get("target_keyword")
    )


def _collect_batch(batch_root: Path, runtime: dict, items: list[dict]) -> dict:
    source_ref = str(runtime.get("source_snapshot_ref") or "")
    try:
        snapshot = entry.safe_repo_ref(source_ref)
    except Exception as exc:
        raise Blocked("SYSTEM4_107007_BATCH_COLLECT_SOURCE_INVALID:" + str(exc)) from exc
    if not snapshot.is_file():
        raise Blocked("SYSTEM4_107007_BATCH_COLLECT_SOURCE_MISSING")
    state_paths = [_workspace(batch_root, index) / "state.json" for index in range(len(items))]
    if any(not path.is_file() for path in state_paths):
        raise Blocked("SYSTEM4_107007_BATCH_COLLECT_STATE_MISSING")
    out_dir = batch_root / "batch-collect"
    cp = subprocess.run(
        [sys.executable, str(BATCH_GATE), "collect", str(snapshot), str(out_dir), *[str(path) for path in state_paths]],
        cwd=entry.REPO,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    output = ((cp.stdout or "") + (cp.stderr or "")).strip()
    if cp.returncode != 0:
        raise Blocked("SYSTEM4_107007_BATCH_COLLECT_FAIL:" + output)
    try:
        result = json.loads((cp.stdout or "").strip().splitlines()[-1])
    except Exception as exc:
        raise Blocked("SYSTEM4_107007_BATCH_COLLECT_OUTPUT_INVALID") from exc
    evidence = out_dir / "system4_batch_evidence.json"
    if (
        result.get("status") != "SYSTEM4_BATCH_FULL_PASS_COLLECTED"
        or result.get("batch_sha256") != runtime.get("batch_sha256")
        or result.get("article_count") != len(items)
        or result.get("publish_allowed") is not False
        or result.get("batch_evidence_path") != str(evidence)
        or not evidence.is_file()
        or result.get("batch_evidence_sha256") != sha256(evidence)
    ):
        raise Blocked("SYSTEM4_107007_BATCH_COLLECT_RESULT_INVALID")
    return {
        "status": result["status"],
        "batch_sha256": result["batch_sha256"],
        "article_count": result["article_count"],
        "batch_evidence_path": result["batch_evidence_path"],
        "batch_evidence_sha256": result["batch_evidence_sha256"],
        "publish_allowed": False,
    }


def _launch(batch_root: Path, point0: Path, state: dict, items: list[dict], index: int) -> dict:
    if index != len(state["completed_indices"]):
        raise Blocked("SYSTEM4_107007_BATCH_NONSEQUENTIAL_LAUNCH_BLOCKED")
    if index in state["started_indices"]:
        raise Blocked("SYSTEM4_107007_BATCH_ITEM_ALREADY_STARTED")
    workspace = _workspace(batch_root, index)
    result = entry.start(str(point0), str(workspace), index)
    if result.get("status") != "SYSTEM4_107007_ROOT_READY_STOP":
        raise Blocked("SYSTEM4_107007_BATCH_ENTRY_NOT_READY")
    state["started_indices"].append(index)
    state["current_index"] = index
    write_atomic(_state_path(batch_root), state)
    return {
        "ok": True,
        "status": "SYSTEM4_107007_BATCH_ROOT_READY_STOP",
        "sequence": 107007,
        "batch_sha256": state["batch_sha256"],
        "item_count": state["item_count"],
        "item_index": index,
        "plan_slot": items[index].get("plan_slot"),
        "workspace": str(workspace),
        "completed_count": len(state["completed_indices"]),
        "publish_allowed": False,
    }


def start(point0_path: str, batch_root_path: str) -> dict:
    point0 = outside_repo(Path(point0_path))
    batch_root = outside_repo(Path(batch_root_path))
    if not point0.is_file():
        raise Blocked("SYSTEM4_107007_BATCH_POINT0_MISSING")
    if batch_root.exists() and any(batch_root.iterdir()):
        raise Blocked("SYSTEM4_107007_BATCH_ROOT_NOT_EMPTY")
    batch_root.mkdir(parents=True, exist_ok=True)
    runtime, items = _runtime()
    _validate_point0_all(point0, runtime, items)
    state = _new_state(point0, runtime, items)
    write_atomic(_state_path(batch_root), state)
    try:
        return _launch(batch_root, point0, state, items, 0)
    except Exception:
        state["status"] = "ACTIVE"
        write_atomic(_state_path(batch_root), state)
        raise


def _bound_existing(point0_path: str, batch_root_path: str) -> tuple[Path, Path, dict, dict, list[dict]]:
    point0 = outside_repo(Path(point0_path))
    batch_root = outside_repo(Path(batch_root_path))
    state_path = _state_path(batch_root)
    if not point0.is_file() or not state_path.is_file():
        raise Blocked("SYSTEM4_107007_BATCH_BINDING_MISSING")
    runtime, items = _runtime()
    _validate_point0_all(point0, runtime, items)
    state = load(state_path)
    _validate_state(state, point0, batch_root, runtime, items)
    return point0, batch_root, state, runtime, items


def advance(point0_path: str, batch_root_path: str) -> dict:
    point0, batch_root, state, runtime, items = _bound_existing(point0_path, batch_root_path)
    if state["status"] == "ITEMS_COMPLETE":
        return summary(state, batch_root, items)
    index = state["current_index"]
    if index >= len(items):
        raise Blocked("SYSTEM4_107007_BATCH_CURRENT_INDEX_RANGE_INVALID")
    if index not in state["started_indices"]:
        return _launch(batch_root, point0, state, items, index)
    if not _item_passed(batch_root, index, items[index]):
        raise Blocked("SYSTEM4_107007_BATCH_CURRENT_ITEM_NOT_PASS:" + str(index))
    if index not in state["completed_indices"]:
        state["completed_indices"].append(index)
    next_index = index + 1
    if next_index == len(items):
        collect = _collect_batch(batch_root, runtime, items)
        state["batch_collect"] = collect
        state["status"] = "ITEMS_COMPLETE"
        state["current_index"] = next_index
        write_atomic(_state_path(batch_root), state)
        return summary(state, batch_root, items)
    state["current_index"] = next_index
    write_atomic(_state_path(batch_root), state)
    return _launch(batch_root, point0, state, items, next_index)


def summary(state: dict, batch_root: Path, items: list[dict]) -> dict:
    result = {
        "ok": True,
        "status": "SYSTEM4_107007_BATCH_ITEMS_COMPLETE" if state["status"] == "ITEMS_COMPLETE" else "SYSTEM4_107007_BATCH_ACTIVE",
        "sequence": 107007,
        "batch_sha256": state["batch_sha256"],
        "item_count": len(items),
        "completed_count": len(state["completed_indices"]),
        "completed_indices": state["completed_indices"],
        "started_indices": state["started_indices"],
        "current_index": state["current_index"],
        "batch_root": str(batch_root),
        "publish_allowed": False,
    }
    if state.get("batch_collect") is not None:
        result["batch_collect"] = state["batch_collect"]
    return result


def status(point0_path: str, batch_root_path: str) -> dict:
    _, batch_root, state, _, items = _bound_existing(point0_path, batch_root_path)
    return summary(state, batch_root, items)


def main() -> int:
    try:
        if len(sys.argv) != 4 or sys.argv[1] not in {"start", "advance", "status"}:
            raise Blocked("USE: system4_107007_batch.py start|advance|status POINT0_OUTSIDE_REPO BATCH_ROOT_OUTSIDE_REPO")
        command = sys.argv[1]
        if command == "start":
            result = start(sys.argv[2], sys.argv[3])
        elif command == "advance":
            result = advance(sys.argv[2], sys.argv[3])
        else:
            result = status(sys.argv[2], sys.argv[3])
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    except Exception as exc:
        print(json.dumps({"ok": False, "status": "SYSTEM4_107007_BATCH_BLOCKED", "reason": str(exc), "publish_allowed": False}, ensure_ascii=False, sort_keys=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
