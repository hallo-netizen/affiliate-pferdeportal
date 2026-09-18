from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
CONTROL = REPO / "control/startmaster0107"
if str(CONTROL) not in sys.path:
    sys.path.insert(0, str(CONTROL))

import system4_107007_entry as entry

MACHINE_POINT0 = HERE / "machine_point0.py"
BATCH_START = CONTROL / "system4_107007_batch.py"
SOURCE_CONTRACT = "SYSTEM4_MACHINE_SOURCE_REQUEST_BATCH_V1"
ROOT_STOP_STATUS = "SYSTEM4_107007_BATCH_ROOT_READY_STOP"
BOUND_PROVIDER = "SYSTEM4_PARENT_MACHINE_HTTP_V3"
SOURCE_REQUEST_NAME = "SOURCE_REQUESTS.json"


class ParentStartError(RuntimeError):
    pass


def _outside_repo(path: Path) -> Path:
    resolved = path.expanduser().resolve()
    root = REPO.resolve()
    if resolved == root or root in resolved.parents:
        raise ParentStartError("PARENT_RUNTIME_PATH_MUST_BE_OUTSIDE_REPO")
    return resolved


def _load(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ParentStartError("PARENT_SOURCE_REQUEST_JSON_INVALID") from exc
    if not isinstance(value, dict):
        raise ParentStartError("PARENT_SOURCE_REQUEST_OBJECT_REQUIRED")
    return value


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _repo_ref(ref: str) -> Path:
    rel = Path(str(ref or ""))
    if not ref or rel.is_absolute() or ".." in rel.parts:
        raise ParentStartError("PARENT_SOURCE_REQUEST_REF_INVALID")
    path = (REPO / rel).resolve()
    root = REPO.resolve()
    if path != root and root not in path.parents:
        raise ParentStartError("PARENT_SOURCE_REQUEST_REF_ESCAPE")
    return path


def _validate_source_request_value(
    value: dict,
    runtime: dict,
    runtime_items: list[dict],
    *,
    require_runtime_identity: bool,
) -> None:
    if value.get("contract") != SOURCE_CONTRACT:
        raise ParentStartError("PARENT_SOURCE_REQUEST_CONTRACT_INVALID")
    request_items = value.get("items")
    if (
        not isinstance(request_items, list)
        or value.get("item_count") != len(request_items)
        or len(request_items) != len(runtime_items)
    ):
        raise ParentStartError("PARENT_SOURCE_REQUEST_COUNT_MISMATCH")
    if require_runtime_identity:
        if value.get("batch_sha256") != runtime.get("batch_sha256"):
            raise ParentStartError("PARENT_SOURCE_REQUEST_BATCH_MISMATCH")
        if value.get("runtime_generation") != runtime.get("generation"):
            raise ParentStartError("PARENT_SOURCE_REQUEST_GENERATION_MISMATCH")
        if value.get("publish_allowed") is not False:
            raise ParentStartError("PARENT_SOURCE_REQUEST_PUBLISH_FORBIDDEN")
    for index, (request_item, runtime_item) in enumerate(zip(request_items, runtime_items)):
        if not isinstance(request_item, dict) or request_item.get("item_index") != index:
            raise ParentStartError("PARENT_SOURCE_REQUEST_INDEX_INVALID:" + str(index))
        if request_item.get("plan_slot") != runtime_item.get("plan_slot"):
            raise ParentStartError("PARENT_SOURCE_REQUEST_PLAN_SLOT_MISMATCH:" + str(index))
        sources = request_item.get("sources")
        if not isinstance(sources, list) or not sources:
            raise ParentStartError("PARENT_SOURCE_REQUEST_POOL_EMPTY:" + str(index))


def _current_bound_source_requests() -> tuple[dict, list[dict], Path]:
    runtime, _, runtime_items = entry.runtime_binding()
    generation = runtime.get("generation")
    if isinstance(generation, bool) or not isinstance(generation, int) or generation < 1:
        raise ParentStartError("PARENT_RUNTIME_GENERATION_INVALID")
    expected_ref = (
        "control/startmaster0107/runtime_inbox/generations/"
        + f"{generation:06d}/"
        + SOURCE_REQUEST_NAME
    )
    ref = str(runtime.get("source_requests_ref") or "")
    declared = str(runtime.get("source_requests_sha256") or "")
    if ref != expected_ref:
        raise ParentStartError("PARENT_SOURCE_REQUEST_BOUND_REF_MISMATCH")
    if not declared or len(declared) != 64:
        raise ParentStartError("PARENT_SOURCE_REQUEST_BOUND_HASH_INVALID")
    path = _repo_ref(ref)
    if not path.is_file():
        raise ParentStartError("PARENT_SOURCE_REQUEST_BOUND_FILE_MISSING")
    if _sha256(path) != declared:
        raise ParentStartError("PARENT_SOURCE_REQUEST_BOUND_HASH_MISMATCH")
    value = _load(path)
    _validate_source_request_value(
        value,
        runtime,
        runtime_items,
        require_runtime_identity=True,
    )
    return runtime, runtime_items, path


def _validate_current_source_requests(path: Path) -> tuple[dict, list[dict]]:
    if not path.is_file():
        raise ParentStartError("PARENT_SOURCE_REQUEST_MISSING")
    value = _load(path)
    runtime, _, runtime_items = entry.runtime_binding()
    _validate_source_request_value(
        value,
        runtime,
        runtime_items,
        require_runtime_identity=False,
    )
    return runtime, runtime_items


def _run_checked(args: list[str], marker: str) -> str:
    cp = subprocess.run(
        args,
        cwd=REPO,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    output = ((cp.stdout or "") + (cp.stderr or "")).strip()
    if cp.returncode != 0 or marker not in output:
        raise ParentStartError("PARENT_CHILD_FAIL:" + output)
    return output


def _last_json_line(output: str) -> dict:
    for line in reversed(output.splitlines()):
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            return value
    raise ParentStartError("PARENT_BATCH_RESULT_MISSING")


def start(source_requests_path: str, runtime_root_path: str, provider: str) -> dict:
    source_requests = _outside_repo(Path(source_requests_path))
    runtime_root = _outside_repo(Path(runtime_root_path))
    if runtime_root.exists():
        raise ParentStartError("PARENT_RUNTIME_ROOT_MUST_NOT_EXIST")
    runtime, runtime_items = _validate_current_source_requests(source_requests)
    if len(runtime_items) < 1:
        raise ParentStartError("PARENT_RUNTIME_BATCH_EMPTY")

    runtime_root.mkdir(parents=True, exist_ok=False)
    point0 = runtime_root / "point0.json"
    batch_root = runtime_root / "batch"

    _run_checked(
        [
            sys.executable,
            str(MACHINE_POINT0),
            "build-current-fetch",
            str(source_requests),
            str(point0),
            provider,
        ],
        "SYSTEM4_MACHINE_POINT0_CURRENT_PASS:",
    )
    batch_output = _run_checked(
        [
            sys.executable,
            str(BATCH_START),
            "start",
            str(point0),
            str(batch_root),
        ],
        ROOT_STOP_STATUS,
    )
    result = _last_json_line(batch_output)
    if (
        result.get("status") != ROOT_STOP_STATUS
        or result.get("item_index") != 0
        or result.get("completed_count") != 0
        or result.get("batch_sha256") != runtime.get("batch_sha256")
        or result.get("item_count") != len(runtime_items)
        or result.get("publish_allowed") is not False
    ):
        raise ParentStartError("PARENT_ROOT_STOP_RESULT_INVALID")

    receipt = {
        "contract": "SYSTEM4_PARENT_START_RECEIPT_V2",
        "status": "SYSTEM4_PARENT_ROOT_READY_STOP",
        "batch_sha256": runtime["batch_sha256"],
        "item_count": len(runtime_items),
        "started_item_index": 0,
        "point0": str(point0),
        "batch_root": str(batch_root),
        "root_only": True,
        "codex_invoked": False,
        "advance_invoked": False,
        "publish_allowed": False,
    }
    (runtime_root / "parent_start_receipt.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return receipt


def start_bound() -> dict:
    runtime, runtime_items, bound_source_requests = _current_bound_source_requests()
    batch = str(runtime.get("batch_sha256") or "")
    generation = int(runtime["generation"])
    run_root = Path(
        tempfile.mkdtemp(
            prefix=f"pferde-atelier-system4-{batch[:12]}-g{generation:06d}-"
        )
    ).resolve()
    source_requests = run_root / "source_requests.json"
    runtime_root = run_root / "runtime"
    source_requests.write_bytes(bound_source_requests.read_bytes())
    if _sha256(source_requests) != runtime.get("source_requests_sha256"):
        raise ParentStartError("PARENT_SOURCE_REQUEST_EXTERNAL_COPY_HASH_MISMATCH")
    receipt = start(str(source_requests), str(runtime_root), BOUND_PROVIDER)
    receipt.update(
        {
            "runtime_generation": generation,
            "run_root": str(run_root),
            "source_requests": str(source_requests),
            "source_requests_bound_ref": str(runtime["source_requests_ref"]),
            "source_requests_bound_sha256": str(runtime["source_requests_sha256"]),
            "source_requests_item_count": len(runtime_items),
            "external_paths_auto_created": True,
        }
    )
    (runtime_root / "parent_start_receipt.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return receipt


def main(argv: list[str]) -> int:
    try:
        if len(argv) == 2 and argv[1] == "start-current-bound":
            result = start_bound()
        elif len(argv) == 5 and argv[1] == "start-current":
            result = start(argv[2], argv[3], argv[4])
        else:
            raise ParentStartError(
                "USE: parent_start.py start-current-bound | "
                "start-current SOURCE_REQUESTS_OUTSIDE_REPO RUNTIME_ROOT_OUTSIDE_REPO PROVIDER"
            )
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    except Exception as exc:
        print(
            json.dumps(
                {
                    "ok": False,
                    "status": "SYSTEM4_PARENT_START_BLOCKED",
                    "reason": str(exc),
                    "publish_allowed": False,
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
