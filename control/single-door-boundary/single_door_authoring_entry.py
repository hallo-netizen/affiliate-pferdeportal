#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
BOUNDARY_PATH = HERE / "single_door_boundary.py"
ROOM_TOKEN = "R_AUTHOR_001"
ACTION_TOKEN = "A_AUTHOR_001"
INPUT_HANDLE = "I_AUTHOR_CURRENT_BATCH_001"
RECEIPT_TOKEN = "P_AUTHOR_001"
NEXT_ROOM_TOKEN = "R_PRE_001"
ENTRY_RECEIPT_CONTRACT = "PFERDE_ATELIER_H81_PREPRODUCTION_ENTRY_RECEIPT_V1"
BOUND_EXECUTOR = "STARTMASTER_0039_CHAT_OR_APPROVED_RESEARCH_TEXT_PROCESS"

class AuthoringEntryBlocked(RuntimeError):
    pass

def _module(path: Path, name: str):
    if not path.is_file():
        raise AuthoringEntryBlocked("MODULE_MISSING:" + path.name)
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AuthoringEntryBlocked("MODULE_LOAD_FAILED:" + path.name)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod

def boundary_module():
    return _module(BOUNDARY_PATH, "single_door_boundary_h81_author")

def authoring_binding(boundary=None):
    boundary = boundary or boundary_module()
    return boundary.DoorBinding.from_mapping({
        "contract": boundary.BOUNDARY_CONTRACT,
        "room_token": ROOM_TOKEN,
        "action_token": ACTION_TOKEN,
        "receipt_token": RECEIPT_TOKEN,
        "next_room_token": NEXT_ROOM_TOKEN,
        "input_handles": [INPUT_HANDLE],
    })

def worker_request(model: str, boundary=None) -> dict[str, Any]:
    boundary = boundary or boundary_module()
    return boundary.build_worker_request(binding=authoring_binding(boundary), model=model)

def _stable_hash(obj: Any) -> str:
    return hashlib.sha256(json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()

def current_binding(repo: Path) -> dict[str, Any]:
    repo = Path(repo).resolve()
    guard = _module(repo / "control/startmaster0107/runtime_inbox/runtime_batch_slot_guard.py", "h81_author_runtime_guard")
    contract = repo / "control/startmaster0107/runtime_inbox/RUNTIME_BATCH_SLOT_CONTRACT_V1.json"
    statep = repo / "control/startmaster0107/runtime_inbox/RUNTIME_INBOX_STATE.json"
    runtime = guard.validate(repo, contract, statep)
    if runtime.get("status") != "READY_WAITING_PACKAGE":
        raise AuthoringEntryBlocked("AUTHORING_ENTRY_REQUIRES_READY_WAITING_PACKAGE")
    state = json.loads(statep.read_text(encoding="utf-8"))
    return {
        "generation": int(state["generation"]),
        "batch_sha256": str(state["batch_sha256"]),
        "source_snapshot_ref": str(state["source_snapshot_ref"]),
        "source_snapshot_sha256": str(state["source_snapshot_sha256"]),
        "source_manifest_sha256": str(state["source_manifest_sha256"]),
    }

def entry_receipt_path(repo: Path, generation: int) -> Path:
    return Path(repo).resolve() / "control/startmaster0107/runtime_inbox/generations" / f"{generation:06d}" / "H81_PREPRODUCTION_ENTRY_RECEIPT.json"

def build_entry_receipt(repo: Path, *, created_at_utc: str | None = None) -> dict[str, Any]:
    cur = current_binding(repo)
    body = {
        "contract": ENTRY_RECEIPT_CONTRACT,
        "status": "PREPRODUCTION_ENTRY_AUTHORIZED",
        "room_token": ROOM_TOKEN,
        "receipt_token": RECEIPT_TOKEN,
        "bound_executor": BOUND_EXECUTOR,
        "generation": cur["generation"],
        "batch_sha256": cur["batch_sha256"],
        "source_snapshot_sha256": cur["source_snapshot_sha256"],
        "source_manifest_sha256": cur["source_manifest_sha256"],
        "created_at_utc": created_at_utc or datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "quality_authority": "NONE",
        "content_semantics_authority": "NONE",
        "publish_allowed": False,
    }
    body["receipt_sha256"] = _stable_hash(body)
    return body

def validate_entry_receipt(repo: Path, receipt: dict[str, Any]) -> dict[str, Any]:
    expected_keys = {
        "contract", "status", "room_token", "receipt_token", "bound_executor", "generation",
        "batch_sha256", "source_snapshot_sha256", "source_manifest_sha256", "created_at_utc",
        "quality_authority", "content_semantics_authority", "publish_allowed", "receipt_sha256",
    }
    if not isinstance(receipt, dict) or set(receipt) != expected_keys:
        raise AuthoringEntryBlocked("AUTHORING_ENTRY_RECEIPT_SCHEMA_INVALID")
    payload = dict(receipt)
    declared = payload.pop("receipt_sha256", None)
    if declared != _stable_hash(payload):
        raise AuthoringEntryBlocked("AUTHORING_ENTRY_RECEIPT_HASH_INVALID")
    cur = current_binding(repo)
    checks = {
        "contract": ENTRY_RECEIPT_CONTRACT,
        "status": "PREPRODUCTION_ENTRY_AUTHORIZED",
        "room_token": ROOM_TOKEN,
        "receipt_token": RECEIPT_TOKEN,
        "bound_executor": BOUND_EXECUTOR,
        "generation": cur["generation"],
        "batch_sha256": cur["batch_sha256"],
        "source_snapshot_sha256": cur["source_snapshot_sha256"],
        "source_manifest_sha256": cur["source_manifest_sha256"],
        "quality_authority": "NONE",
        "content_semantics_authority": "NONE",
        "publish_allowed": False,
    }
    for key, value in checks.items():
        if receipt.get(key) != value:
            raise AuthoringEntryBlocked("AUTHORING_ENTRY_RECEIPT_BINDING_MISMATCH:" + key)
    try:
        datetime.fromisoformat(str(receipt["created_at_utc"]).replace("Z", "+00:00"))
    except Exception as exc:
        raise AuthoringEntryBlocked("AUTHORING_ENTRY_RECEIPT_TIME_INVALID") from exc
    return dict(receipt)

def main() -> int:
    try:
        req = worker_request("gpt-5.6-sol")
        print(json.dumps({
            "ok": True,
            "status": "H81_PREPRODUCTION_AUTHORING_SINGLE_DOOR_READY",
            "room_token": req["input"],
            "tool_count": len(req["tools"]),
            "parallel_tool_calls": req["parallel_tool_calls"],
            "bound_executor": BOUND_EXECUTOR,
            "next_room_token": NEXT_ROOM_TOKEN,
            "free_chat_execution_authority": False,
            "quality_authority": "NONE",
            "content_semantics_authority": "NONE",
        }, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        print(json.dumps({"ok": False, "status": "H81_AUTHORING_ENTRY_BLOCKED", "error": str(exc), "publish_allowed": False}, ensure_ascii=False, indent=2))
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
