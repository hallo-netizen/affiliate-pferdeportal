#!/usr/bin/env python3
# Test-only 1/3 acceptance adapter; never the production 107007 entrance.
# Merge-isolation marker: this test-only PR head must stay distinct from the permanent dispatcher head.
from __future__ import annotations

import copy
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import batch_gate
import chat_start_gate
import machine_point0
import point0_snapshot
import root_entry
import source_acquisition

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
CONTROL = REPO / "control/startmaster0107"
if str(CONTROL) not in sys.path:
    sys.path.insert(0, str(CONTROL))

import system4_107007_entry as production_entry

CURRENT_STATE = CONTROL / "CURRENT_STATE.json"
SOURCE_REQUEST_NAME = "SOURCE_REQUESTS.json"
BATCH_STATE_NAME = "SYSTEM4_107007_BATCH_STATE.json"
ALLOWED_COUNTS = {1, 3}
PROVIDER = "SYSTEM4_E2E_ACCEPTANCE_BOUND_HTTP_V1"
META_NAME = "E2E_ACCEPTANCE_META.json"
BATCH_TEMPLATE_REUSE_RE = re.compile(r"^BATCH_TEMPLATE_REUSE_BLOCKED:(\d+):(\d+):([0-9.]+)$")


class AcceptanceBlocked(RuntimeError):
    pass


def _load(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise AcceptanceBlocked("ACCEPTANCE_JSON_INVALID:" + str(path)) from exc
    if not isinstance(value, dict):
        raise AcceptanceBlocked("ACCEPTANCE_JSON_OBJECT_REQUIRED:" + str(path))
    return value


def _write(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(path)


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _head() -> str:
    return subprocess.check_output(["git", "rev-parse", "--verify", "HEAD"], cwd=REPO, text=True).strip()


def _outside(path: Path) -> Path:
    value = path.expanduser().resolve()
    repo = REPO.resolve()
    if value == repo or repo in value.parents:
        raise AcceptanceBlocked("ACCEPTANCE_RUNTIME_MUST_BE_OUTSIDE_REPO")
    return value


def _approval(count: int) -> dict:
    if count not in ALLOWED_COUNTS:
        raise AcceptanceBlocked("ACCEPTANCE_COUNT_NOT_AUTHORIZED:" + str(count))
    state = _load(CURRENT_STATE)
    blocker = state.get("current_execution_blocker")
    if not isinstance(blocker, dict):
        raise AcceptanceBlocked("ACCEPTANCE_CURRENT_BLOCKER_MISSING")
    if blocker.get("code") != "E2E_ONE_AND_THREE_ARTICLE_CHAT_FILE_ACCEPTANCE_PENDING":
        raise AcceptanceBlocked("ACCEPTANCE_NOT_CURRENTLY_AUTHORIZED")
    counts = blocker.get("test_counts")
    if counts != [1, 3] or count not in counts:
        raise AcceptanceBlocked("ACCEPTANCE_COUNT_BINDING_INVALID")
    if blocker.get("codex_start_allowed") is not True:
        raise AcceptanceBlocked("ACCEPTANCE_CODEX_NOT_ALLOWED")
    if blocker.get("fresh_user_codex_approval_required") is not False:
        raise AcceptanceBlocked("ACCEPTANCE_FRESH_APPROVAL_REQUIRED")
    if blocker.get("publish_allowed") is not False or state.get("publish_allowed") is not False:
        raise AcceptanceBlocked("ACCEPTANCE_PUBLISH_MUST_BE_FALSE")
    return state


def _subset_batch(full_batch: dict, count: int) -> dict:
    items = full_batch.get("items")
    if not isinstance(items, list) or len(items) < count:
        raise AcceptanceBlocked("ACCEPTANCE_SOURCE_BATCH_TOO_SMALL")
    out = copy.deepcopy(full_batch)
    out["items"] = copy.deepcopy(items[:count])
    out["item_count"] = count
    out["publish_allowed"] = False
    out.pop("batch_sha256", None)
    out["batch_sha256"] = point0_snapshot.stable(out)
    return out


def _bound_source_requests(runtime: dict, full_items: list[dict], count: int, subset_sha: str) -> dict:
    generation = runtime.get("generation")
    if isinstance(generation, bool) or not isinstance(generation, int) or generation < 1:
        raise AcceptanceBlocked("ACCEPTANCE_RUNTIME_GENERATION_INVALID")
    expected = f"control/startmaster0107/runtime_inbox/generations/{generation:06d}/{SOURCE_REQUEST_NAME}"
    ref = str(runtime.get("source_requests_ref") or "")
    declared_sha = str(runtime.get("source_requests_sha256") or "")
    if ref != expected:
        raise AcceptanceBlocked("ACCEPTANCE_SOURCE_REQUEST_REF_DRIFT")
    source_path = production_entry.safe_repo_ref(ref)
    if not source_path.is_file() or _sha(source_path) != declared_sha:
        raise AcceptanceBlocked("ACCEPTANCE_SOURCE_REQUEST_HASH_DRIFT")
    source = _load(source_path)
    rows = source.get("items")
    if (
        source.get("contract") != "SYSTEM4_MACHINE_SOURCE_REQUEST_BATCH_V1"
        or source.get("publish_allowed") is not False
        or source.get("item_count") != len(full_items)
        or not isinstance(rows, list)
        or len(rows) != len(full_items)
    ):
        raise AcceptanceBlocked("ACCEPTANCE_SOURCE_REQUEST_BINDING_INVALID")
    selected = copy.deepcopy(rows[:count])
    for index, (request, item) in enumerate(zip(selected, full_items[:count])):
        if request.get("item_index") != index or request.get("plan_slot") != item.get("plan_slot"):
            raise AcceptanceBlocked("ACCEPTANCE_SOURCE_REQUEST_ITEM_DRIFT:" + str(index))
        if not isinstance(request.get("sources"), list) or not request["sources"]:
            raise AcceptanceBlocked("ACCEPTANCE_SOURCE_REQUEST_POOL_EMPTY:" + str(index))
    return {
        "contract": "SYSTEM4_MACHINE_SOURCE_REQUEST_BATCH_V1",
        "batch_sha256": subset_sha,
        "item_count": count,
        "items": selected,
        "publish_allowed": False,
        "runtime_generation": generation,
    }


def _assert_current(meta: dict) -> None:
    if meta.get("head_sha") != _head():
        raise AcceptanceBlocked("ACCEPTANCE_HEAD_DRIFT")
    if meta.get("root_manifest_sha256") != root_entry._critical_manifest_sha256():
        raise AcceptanceBlocked("ACCEPTANCE_MANIFEST_DRIFT")
    count = meta.get("article_count")
    if count not in ALLOWED_COUNTS:
        raise AcceptanceBlocked("ACCEPTANCE_META_COUNT_INVALID")
    _approval(int(count))


def prepare(count: int, run_root: Path | None = None) -> dict:
    _approval(count)
    manifest = root_entry._critical_manifest_sha256()
    head = _head()
    runtime, _, full_items = production_entry.runtime_binding()
    if len(full_items) < 3:
        raise AcceptanceBlocked("ACCEPTANCE_BOUND_BATCH_TOO_SMALL")

    full_raw, full_plans = machine_point0._current_snapshot_and_plans(REPO, manifest)
    production = json.loads(full_raw.decode("utf-8"))
    full_batch = production.get("next_textmachine_metadata_batch")
    if not isinstance(full_batch, dict) or full_batch.get("items") != full_items:
        raise AcceptanceBlocked("ACCEPTANCE_CURRENT_SNAPSHOT_ITEM_DRIFT")

    subset = _subset_batch(full_batch, count)
    production["next_textmachine_metadata_batch"] = subset
    production.pop("system4_chat_start", None)
    event = {
        "contract": chat_start_gate.START_EVENT_CONTRACT,
        "button_id": chat_start_gate.START_BUTTON_ID,
        "action": chat_start_gate.START_ACTION,
        "route": chat_start_gate.START_ROUTE,
        "article_count": count,
        "batch_sha256": subset["batch_sha256"],
        "publish_allowed": False,
    }
    production = chat_start_gate.bind(production, event)
    snapshot_bytes = point0_snapshot.canon(production)

    plan_rows = full_plans.get("items")
    if not isinstance(plan_rows, list) or len(plan_rows) != len(full_items):
        raise AcceptanceBlocked("ACCEPTANCE_PREWRITE_PLAN_SOURCE_INVALID")
    plans = {
        "contract": "SYSTEM4_MACHINE_PREWRITE_PLAN_BATCH_V1",
        "item_count": count,
        "authority": full_plans.get("authority"),
        "items": copy.deepcopy(plan_rows[:count]),
    }
    requests = _bound_source_requests(runtime, full_items, count, subset["batch_sha256"])

    if run_root is None:
        root = Path(tempfile.mkdtemp(prefix=f"pferde-atelier-system4-e2e-{count}-")).resolve()
    else:
        root = _outside(run_root)
        if root.exists():
            raise AcceptanceBlocked("ACCEPTANCE_RUN_ROOT_ALREADY_EXISTS")
        root.mkdir(parents=True, exist_ok=False)

    (root / "snapshot.json").write_bytes(snapshot_bytes)
    _write(root / "plans.json", plans)
    _write(root / "source_requests.json", requests)
    meta = {
        "contract": "SYSTEM4_E2E_SUBSET_ACCEPTANCE_V1",
        "status": "PREPARED",
        "article_count": count,
        "original_bound_batch_sha256": runtime["batch_sha256"],
        "acceptance_batch_sha256": subset["batch_sha256"],
        "runtime_generation": runtime["generation"],
        "head_sha": head,
        "root_manifest_sha256": manifest,
        "snapshot_sha256": _sha(root / "snapshot.json"),
        "source_requests_sha256": _sha(root / "source_requests.json"),
        "plans_sha256": _sha(root / "plans.json"),
        "source_item_plan_slots": [item["plan_slot"] for item in full_items[:count]],
        "production_route_changed": False,
        "test_only": True,
        "publish_allowed": False,
    }
    _write(root / META_NAME, meta)
    return {**meta, "run_root": str(root)}


def acquire(run_root: Path) -> dict:
    root = _outside(run_root)
    meta = _load(root / META_NAME)
    _assert_current(meta)
    if meta.get("status") not in {"PREPARED", "ACQUIRED"}:
        raise AcceptanceBlocked("ACCEPTANCE_ACQUIRE_PHASE_INVALID")
    requests = _load(root / "source_requests.json")
    acquired = source_acquisition.acquire_batch(requests)
    _write(root / "acquired.json", acquired)
    meta["status"] = "ACQUIRED"
    meta["acquired_sha256"] = _sha(root / "acquired.json")
    _write(root / META_NAME, meta)
    return {
        "contract": meta["contract"],
        "status": "ACQUIRED",
        "article_count": meta["article_count"],
        "run_root": str(root),
        "acquired_sha256": meta["acquired_sha256"],
        "publish_allowed": False,
    }


def _run_root(point0: Path, workspace: Path, index: int) -> None:
    cp = subprocess.run(
        [sys.executable, str(HERE / "root_entry.py"), "start-point0", str(point0), str(workspace), str(index)],
        cwd=REPO,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    output = ((cp.stdout or "") + (cp.stderr or "")).strip()
    if cp.returncode != 0 or "SYSTEM4_ROOT_POINT0_PASS:WORKER_DISPATCH_READY" not in output:
        raise AcceptanceBlocked("ACCEPTANCE_ROOT_START_FAIL:" + output)


def _batch_state(root: Path) -> tuple[Path, Path, dict]:
    batch_root = root / "batch"
    path = batch_root / BATCH_STATE_NAME
    if not path.is_file():
        raise AcceptanceBlocked("ACCEPTANCE_BATCH_STATE_MISSING")
    return batch_root, path, _load(path)


def bind_acquired(run_root: Path) -> dict:
    root = _outside(run_root)
    meta = _load(root / META_NAME)
    _assert_current(meta)
    if meta.get("status") != "ACQUIRED":
        raise AcceptanceBlocked("ACCEPTANCE_BIND_PHASE_INVALID")
    acquired_path = root / "acquired.json"
    if not acquired_path.is_file() or _sha(acquired_path) != meta.get("acquired_sha256"):
        raise AcceptanceBlocked("ACCEPTANCE_ACQUIRED_HASH_INVALID")

    snapshot_bytes = (root / "snapshot.json").read_bytes()
    plans = _load(root / "plans.json")
    acquired_value = _load(acquired_path)
    point0 = machine_point0.build_from_acquired(
        snapshot_bytes=snapshot_bytes,
        acquired_batch=acquired_value,
        prewrite_plan_batch=plans,
        provider=PROVIDER,
        manifest=meta["root_manifest_sha256"],
        head=meta["head_sha"],
    )
    point0_path = root / "point0.json"
    point0_path.write_bytes(point0_snapshot.canon(point0))

    batch_root = root / "batch"
    if batch_root.exists():
        raise AcceptanceBlocked("ACCEPTANCE_BATCH_ROOT_ALREADY_EXISTS")
    batch_root.mkdir(parents=True, exist_ok=False)
    workspace = batch_root / "item-000000"
    _run_root(point0_path, workspace, 0)
    state = {
        "contract": "SYSTEM4_107007_PRODUCTION_BATCH_V1",
        "status": "ACTIVE",
        "sequence": 107007,
        "batch_sha256": meta["acceptance_batch_sha256"],
        "point0_sha256": _sha(point0_path),
        "item_count": meta["article_count"],
        "current_index": 0,
        "completed_indices": [],
        "started_indices": [0],
        "batch_collect": None,
        "publish_allowed": False,
    }
    _write(batch_root / BATCH_STATE_NAME, state)
    meta["status"] = "BOUND"
    meta["point0_sha256"] = state["point0_sha256"]
    meta["batch_root"] = str(batch_root)
    _write(root / META_NAME, meta)
    return {
        "contract": meta["contract"],
        "status": "SYSTEM4_E2E_ACCEPTANCE_ROOT_READY_STOP",
        "article_count": meta["article_count"],
        "item_index": 0,
        "workspace": str(workspace),
        "point0": str(point0_path),
        "batch_root": str(batch_root),
        "worker_started": False,
        "advance_invoked": False,
        "publish_allowed": False,
    }


def _current_item_passed(root: Path, state: dict, index: int) -> bool:
    snapshot = _load(root / "snapshot.json")
    items = snapshot["next_textmachine_metadata_batch"]["items"]
    workspace_state = root / "batch" / f"item-{index:06d}" / "state.json"
    if not workspace_state.is_file():
        return False
    value = _load(workspace_state)
    checks = value.get("checks")
    article = value.get("article")
    expected = items[index]
    return bool(
        value.get("phase") == "OUTPUT_GATE_REQUIRED"
        and isinstance(checks, dict)
        and checks.get("status") == "PASS"
        and checks.get("mode") == "FULL_PRODUCTION"
        and isinstance(article, dict)
        and article.get("plan_slot") == expected.get("plan_slot")
        and article.get("target_keyword") == expected.get("target_keyword")
        and article.get("title") == expected.get("title")
    )


def _collect(root: Path, state: dict) -> dict:
    count = int(state["item_count"])
    paths = [root / "batch" / f"item-{index:06d}" / "state.json" for index in range(count)]
    out = root / "batch" / "batch-collect"
    result = batch_gate.collect_batch(root / "snapshot.json", paths, out)
    evidence = out / "system4_batch_evidence.json"
    return {
        "status": result["status"],
        "batch_sha256": result["batch_sha256"],
        "article_count": result["article_count"],
        "batch_evidence_path": str(evidence),
        "batch_evidence_sha256": _sha(evidence),
        "publish_allowed": False,
    }


def _batch_repair_record(root: Path, state: dict, reason: str) -> dict | None:
    match = BATCH_TEMPLATE_REUSE_RE.fullmatch(str(reason or "").strip())
    if not match:
        return None
    left = int(match.group(1))
    right = int(match.group(2))
    score = float(match.group(3))
    count = int(state["item_count"])
    if left < 0 or right < 0 or left >= count or right >= count or left >= right:
        raise AcceptanceBlocked("ACCEPTANCE_BATCH_REPAIR_PAIR_INVALID")
    repair_index = right
    state_path = root / "batch" / f"item-{repair_index:06d}" / "state.json"
    article_state = _load(state_path)
    if not _current_item_passed(root, state, repair_index):
        raise AcceptanceBlocked("ACCEPTANCE_BATCH_REPAIR_TARGET_NOT_PASS:" + str(repair_index))
    revision = int(article_state.get("revision") or 0)
    draft_sha = str(article_state.get("draft_sha256") or "")
    if revision < 1 or len(draft_sha) != 64:
        raise AcceptanceBlocked("ACCEPTANCE_BATCH_REPAIR_TARGET_EVIDENCE_INVALID")
    return {
        "contract": "SYSTEM4_E2E_BATCH_REPAIR_REQUEST_V1",
        "error_code": "BATCH_TEMPLATE_REUSE_BLOCKED",
        "detail": reason,
        "left_index": left,
        "right_index": right,
        "similarity": score,
        "threshold": 0.20,
        "repair_owner": "DRAFT_WORKER",
        "repair_index": repair_index,
        "workspace": str(state_path.parent),
        "same_article_required": True,
        "terminal_block": False,
        "required_revision_gt": revision,
        "required_draft_sha256_change_from": draft_sha,
        "publish_allowed": False,
    }


def _enter_batch_repair(root: Path, state_path: Path, state: dict, reason: str) -> dict | None:
    record = _batch_repair_record(root, state, reason)
    if record is None:
        return None
    history = state.get("batch_repair_history")
    if not isinstance(history, list):
        history = []
    history.append(record)
    count = int(state["item_count"])
    state["status"] = "BATCH_REPAIR_REQUIRED"
    state["current_index"] = count
    state["completed_indices"] = list(range(count))
    state["started_indices"] = list(range(count))
    state["batch_collect"] = None
    state["batch_repair"] = record
    state["batch_repair_history"] = history
    _write(state_path, state)
    return {
        "contract": "SYSTEM4_E2E_SUBSET_ACCEPTANCE_V1",
        "status": "SYSTEM4_E2E_ACCEPTANCE_BATCH_REPAIR_REQUIRED",
        "article_count": count,
        "repair_owner": "DRAFT_WORKER",
        "repair_index": record["repair_index"],
        "workspace": record["workspace"],
        "finding": record,
        "same_article_required": True,
        "terminal_block": False,
        "publish_allowed": False,
    }


def _retry_batch_after_repair(root: Path, state_path: Path, state: dict) -> dict:
    record = state.get("batch_repair")
    if not isinstance(record, dict) or record.get("error_code") != "BATCH_TEMPLATE_REUSE_BLOCKED":
        raise AcceptanceBlocked("ACCEPTANCE_BATCH_REPAIR_STATE_INVALID")
    repair_index = record.get("repair_index")
    if not isinstance(repair_index, int) or isinstance(repair_index, bool):
        raise AcceptanceBlocked("ACCEPTANCE_BATCH_REPAIR_INDEX_INVALID")
    if not _current_item_passed(root, state, repair_index):
        raise AcceptanceBlocked("ACCEPTANCE_BATCH_REPAIR_TARGET_NOT_PASS:" + str(repair_index))
    article_state = _load(root / "batch" / f"item-{repair_index:06d}" / "state.json")
    revision = int(article_state.get("revision") or 0)
    draft_sha = str(article_state.get("draft_sha256") or "")
    if revision <= int(record.get("required_revision_gt") or 0):
        raise AcceptanceBlocked("ACCEPTANCE_BATCH_REPAIR_REVISION_NOT_ADVANCED")
    if draft_sha == record.get("required_draft_sha256_change_from"):
        raise AcceptanceBlocked("ACCEPTANCE_BATCH_REPAIR_DRAFT_UNCHANGED")
    try:
        collected = _collect(root, state)
    except batch_gate.BatchGateError as exc:
        returned = _enter_batch_repair(root, state_path, state, str(exc))
        if returned is not None:
            return returned
        raise
    count = int(state["item_count"])
    state["batch_collect"] = collected
    state["status"] = "ITEMS_COMPLETE"
    state["current_index"] = count
    state["batch_repair"] = None
    _write(state_path, state)
    meta = _load(root / META_NAME)
    meta["status"] = "ITEMS_COMPLETE"
    _write(root / META_NAME, meta)
    return summary(root)


def advance(run_root: Path) -> dict:
    root = _outside(run_root)
    meta = _load(root / META_NAME)
    _assert_current(meta)
    batch_root, state_path, state = _batch_state(root)
    if state.get("status") == "ITEMS_COMPLETE":
        return summary(root)
    if state.get("status") == "BATCH_REPAIR_REQUIRED":
        return _retry_batch_after_repair(root, state_path, state)
    if state.get("contract") != "SYSTEM4_107007_PRODUCTION_BATCH_V1" or state.get("publish_allowed") is not False:
        raise AcceptanceBlocked("ACCEPTANCE_BATCH_STATE_INVALID")
    count = int(meta["article_count"])
    if state.get("item_count") != count or state.get("batch_sha256") != meta.get("acceptance_batch_sha256"):
        raise AcceptanceBlocked("ACCEPTANCE_BATCH_STATE_DRIFT")
    index = state.get("current_index")
    if not isinstance(index, int) or isinstance(index, bool) or index < 0 or index >= count:
        raise AcceptanceBlocked("ACCEPTANCE_CURRENT_INDEX_INVALID")
    if state.get("started_indices") != list(range(index + 1)) or state.get("completed_indices") != list(range(index)):
        raise AcceptanceBlocked("ACCEPTANCE_SEQUENCE_DRIFT")
    if not _current_item_passed(root, state, index):
        raise AcceptanceBlocked("ACCEPTANCE_CURRENT_ITEM_NOT_PASS:" + str(index))

    state["completed_indices"].append(index)
    next_index = index + 1
    if next_index == count:
        state["completed_indices"] = list(range(count))
        state["started_indices"] = list(range(count))
        try:
            state["batch_collect"] = _collect(root, state)
        except batch_gate.BatchGateError as exc:
            returned = _enter_batch_repair(root, state_path, state, str(exc))
            if returned is not None:
                return returned
            raise
        state["status"] = "ITEMS_COMPLETE"
        state["current_index"] = count
        state["batch_repair"] = None
        _write(state_path, state)
        meta["status"] = "ITEMS_COMPLETE"
        _write(root / META_NAME, meta)
        return summary(root)

    workspace = batch_root / f"item-{next_index:06d}"
    _run_root(root / "point0.json", workspace, next_index)
    state["current_index"] = next_index
    state["started_indices"].append(next_index)
    _write(state_path, state)
    return {
        "contract": meta["contract"],
        "status": "SYSTEM4_E2E_ACCEPTANCE_ROOT_READY_STOP",
        "article_count": count,
        "item_index": next_index,
        "workspace": str(workspace),
        "completed_indices": list(state["completed_indices"]),
        "started_indices": list(state["started_indices"]),
        "publish_allowed": False,
    }


def summary(run_root: Path) -> dict:
    root = _outside(run_root)
    meta = _load(root / META_NAME)
    _assert_current(meta)
    batch_root, _, state = _batch_state(root)
    index = state.get("current_index")
    workspace = None
    if isinstance(index, int) and 0 <= index < int(meta["article_count"]):
        workspace = str(batch_root / f"item-{index:06d}")
    return {
        "contract": meta["contract"],
        "status": state["status"],
        "article_count": meta["article_count"],
        "current_index": index,
        "completed_indices": state["completed_indices"],
        "started_indices": state["started_indices"],
        "current_workspace": workspace,
        "batch_root": str(batch_root),
        "batch_collect": state.get("batch_collect"),
        "publish_allowed": False,
    }


def prepare_107008(run_root: Path) -> dict:
    # The isolated acceptance route is intentionally not an authority for the
    # canonical 107008 / PSERC / ENDSTEMPEL production closeout. Keeping this
    # command as an explicit fail-closed surface prevents a future caller from
    # turning the test adapter into a production bypass.
    root = _outside(run_root)
    meta = _load(root / META_NAME)
    _assert_current(meta)
    raise AcceptanceBlocked(
        "ACCEPTANCE_107008_CANONICAL_BOUNDARY:"
        "ISOLATED_TEST_ROUTE_MUST_NOT_REPLACE_OFFICIAL_PRODUCTION_INTAKE"
    )


def main(argv: list[str]) -> int:
    try:
        if len(argv) == 3 and argv[1] == "prepare":
            result = prepare(int(argv[2]))
        elif len(argv) == 3 and argv[1] == "acquire":
            result = acquire(Path(argv[2]))
        elif len(argv) == 3 and argv[1] == "bind-acquired":
            result = bind_acquired(Path(argv[2]))
        elif len(argv) == 3 and argv[1] == "advance":
            result = advance(Path(argv[2]))
        elif len(argv) == 3 and argv[1] == "status":
            result = summary(Path(argv[2]))
        elif len(argv) == 3 and argv[1] == "prepare-107008":
            result = prepare_107008(Path(argv[2]))
        else:
            raise AcceptanceBlocked(
                "USE: e2e_acceptance_subset.py prepare 1|3 | acquire RUN_ROOT | "
                "bind-acquired RUN_ROOT | advance RUN_ROOT | status RUN_ROOT | prepare-107008 RUN_ROOT"
            )
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    except Exception as exc:
        print(json.dumps({
            "ok": False,
            "status": "SYSTEM4_E2E_ACCEPTANCE_BLOCKED",
            "reason": str(exc),
            "publish_allowed": False,
        }, ensure_ascii=False, sort_keys=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
