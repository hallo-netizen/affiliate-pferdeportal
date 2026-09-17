#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
STATE = REPO / "control/startmaster0107/CURRENT_STATE.json"
RUNTIME = REPO / "control/startmaster0107/runtime_inbox/RUNTIME_INBOX_STATE.json"
ROOT_ENTRY = REPO / "isolated_system4/root_entry.py"
CODEX_ENTRY = REPO / "isolated_system4/codex_entry.py"
SHA_RE = re.compile(r"^[0-9a-f]{64}$")


class Blocked(RuntimeError):
    pass


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise Blocked("JSON_OBJECT_REQUIRED:" + str(path))
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def outside_repo(path: Path) -> Path:
    p = path.expanduser().resolve()
    root = REPO.resolve()
    if p == root or root in p.parents:
        raise Blocked("SYSTEM4_RUNTIME_PATH_MUST_BE_OUTSIDE_REPO")
    return p


def require_107007(item_index: int) -> tuple[dict, dict]:
    if not STATE.is_file() or not RUNTIME.is_file():
        raise Blocked("107007_STATE_OR_RUNTIME_MISSING")
    state = load(STATE)
    gate = state.get("execution_gate") or {}
    if state.get("next_allowed_step") != "RUN_NEW_ARTICLE_BATCH_NO_STOP" or int(gate.get("sequence", -1)) != 107007:
        raise Blocked("SYSTEM4_107007_NOT_CURRENT")
    runtime = load(RUNTIME)
    if runtime.get("status") != "EXECUTION_READY" or runtime.get("publish_allowed") is not False:
        raise Blocked("SYSTEM4_107007_RUNTIME_NOT_READY")
    count = int(runtime.get("item_count") or 0)
    if count < 1:
        raise Blocked("SYSTEM4_107007_ITEM_COUNT_INVALID")
    if item_index < 0 or item_index >= count:
        raise Blocked("SYSTEM4_107007_ITEM_INDEX_INVALID")
    batch = str(runtime.get("batch_sha256") or "")
    if not SHA_RE.fullmatch(batch):
        raise Blocked("SYSTEM4_107007_BATCH_SHA_INVALID")
    return state, runtime


def verify_point0_binding(point0: Path, runtime: dict, item_index: int) -> None:
    if not point0.is_file():
        raise Blocked("SYSTEM4_107007_POINT0_MISSING")
    value = load(point0)
    if value.get("contract") != "SYSTEM4_POINT0_SNAPSHOT_V2":
        raise Blocked("SYSTEM4_107007_POINT0_CONTRACT_INVALID")
    production = value.get("production_snapshot")
    if not isinstance(production, dict):
        raise Blocked("SYSTEM4_107007_POINT0_PRODUCTION_SNAPSHOT_MISSING")
    batch = production.get("next_textmachine_metadata_batch")
    if not isinstance(batch, dict):
        raise Blocked("SYSTEM4_107007_POINT0_BATCH_MISSING")
    if batch.get("batch_sha256") != runtime.get("batch_sha256"):
        raise Blocked("SYSTEM4_107007_POINT0_BATCH_MISMATCH")
    items = batch.get("items")
    if not isinstance(items, list) or len(items) != int(runtime.get("item_count") or -1):
        raise Blocked("SYSTEM4_107007_POINT0_COUNT_MISMATCH")
    if item_index >= len(items):
        raise Blocked("SYSTEM4_107007_POINT0_INDEX_MISMATCH")


def run_checked(args: list[str], marker: str) -> str:
    cp = subprocess.run(args, cwd=REPO, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    output = (cp.stdout or "") + (cp.stderr or "")
    if cp.returncode != 0 or marker not in output:
        raise Blocked("SYSTEM4_107007_CHILD_FAIL:" + output.strip())
    return output.strip()


def start(point0_path: str, workspace_path: str, item_index: int) -> dict:
    _, runtime = require_107007(item_index)
    point0 = outside_repo(Path(point0_path))
    workspace = outside_repo(Path(workspace_path))
    if workspace.exists() and any(workspace.iterdir()):
        raise Blocked("SYSTEM4_107007_WORKSPACE_NOT_EMPTY")
    verify_point0_binding(point0, runtime, item_index)

    root_output = run_checked(
        [sys.executable, str(ROOT_ENTRY), "start-point0", str(point0), str(workspace), str(item_index)],
        "SYSTEM4_ROOT_POINT0_PASS:WORKER_DISPATCH_READY",
    )
    worker_output = run_checked(
        [sys.executable, str(CODEX_ENTRY), "worker-start", str(workspace)],
        "SYSTEM4_CODEX_ENTRY_PASS:",
    )
    return {
        "ok": True,
        "status": "SYSTEM4_107007_ROOT_BOUND_WORKER_READY",
        "sequence": 107007,
        "batch_sha256": runtime["batch_sha256"],
        "item_index": item_index,
        "point0_sha256": sha256(point0),
        "workspace": str(workspace),
        "root_marker": "SYSTEM4_ROOT_POINT0_PASS:WORKER_DISPATCH_READY",
        "worker_marker": worker_output.splitlines()[0] if worker_output else "",
        "old_cloud_entry_used_before_root": False,
        "publish_allowed": False,
    }


def main() -> int:
    try:
        if len(sys.argv) != 4:
            raise Blocked("USE: system4_107007_entry.py POINT0_OUTSIDE_REPO WORKSPACE_OUTSIDE_REPO ITEM_INDEX")
        try:
            index = int(sys.argv[3])
        except ValueError as exc:
            raise Blocked("SYSTEM4_107007_ITEM_INDEX_INVALID") from exc
        result = start(sys.argv[1], sys.argv[2], index)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    except Exception as exc:
        print(json.dumps({"ok": False, "status": "SYSTEM4_107007_ENTRY_BLOCKED", "reason": str(exc), "publish_allowed": False}, ensure_ascii=False, sort_keys=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
