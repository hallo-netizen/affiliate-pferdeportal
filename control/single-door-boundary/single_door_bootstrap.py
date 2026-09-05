#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import sys
from pathlib import Path
from typing import Any, Callable, Mapping

HERE = Path(__file__).resolve().parent
BOUNDARY_PATH = HERE / "single_door_boundary.py"
ROOM_TOKEN = "R_BOOT_001"
ACTION_TOKEN = "A_BOOT_001"
INPUT_HANDLE = "I_BOOT_BATCH_001"
RECEIPT_TOKEN = "P_BOOT_001"
NEXT_ROOM_TOKEN = "R_PRE_001"
BOOTSTRAP_BINDING_CONTRACT = "PFERDE_ATELIER_H8_BOOTSTRAP_PROVENANCE_BINDING_V1"
AUTHORITATIVE_ORIGIN = "SINGLE_DOOR_BOOTSTRAP_ONLY"

class BootstrapBlocked(RuntimeError):
    pass

def _module(path: Path, name: str):
    if not path.is_file():
        raise BootstrapBlocked("MODULE_MISSING:" + path.name)
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise BootstrapBlocked("MODULE_LOAD_FAILED:" + path.name)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    try:
        spec.loader.exec_module(mod)
    except Exception:
        sys.modules.pop(name, None)
        raise
    return mod

def boundary_module():
    return _module(BOUNDARY_PATH, "single_door_boundary_h8_boot")

def bootstrap_binding(boundary=None):
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
    return boundary.build_worker_request(binding=bootstrap_binding(boundary), model=model)

def current_binding(repo: Path) -> dict[str, Any]:
    repo = Path(repo).resolve()
    guard = _module(repo / "control/startmaster0107/runtime_inbox/runtime_batch_slot_guard.py", "h8_boot_runtime_guard")
    contract = repo / "control/startmaster0107/runtime_inbox/RUNTIME_BATCH_SLOT_CONTRACT_V1.json"
    statep = repo / "control/startmaster0107/runtime_inbox/RUNTIME_INBOX_STATE.json"
    runtime = guard.validate(repo, contract, statep)
    if runtime.get("status") != "READY_WAITING_PACKAGE":
        raise BootstrapBlocked("BOOTSTRAP_REQUIRES_READY_WAITING_PACKAGE")
    state = json.loads(statep.read_text(encoding="utf-8"))
    return {
        "generation": int(state["generation"]),
        "batch_sha256": str(state["batch_sha256"]),
        "source_snapshot_ref": str(state["source_snapshot_ref"]),
        "source_snapshot_sha256": str(state["source_snapshot_sha256"]),
        "source_manifest_sha256": str(state["source_manifest_sha256"]),
    }

def expected_provenance_binding(repo: Path) -> dict[str, Any]:
    cur = current_binding(repo)
    body = {
        "contract": BOOTSTRAP_BINDING_CONTRACT,
        "room_token": ROOM_TOKEN,
        "receipt_token": RECEIPT_TOKEN,
        "generation": cur["generation"],
        "batch_sha256": cur["batch_sha256"],
        "source_snapshot_sha256": cur["source_snapshot_sha256"],
        "source_manifest_sha256": cur["source_manifest_sha256"],
        "authoritative_origin": AUTHORITATIVE_ORIGIN,
    }
    body["binding_sha256"] = hashlib.sha256(json.dumps(body, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
    return body

def incoming_path(repo: Path, generation: int) -> Path:
    return Path(repo).resolve() / "control/startmaster0107/runtime_inbox/generations" / f"{generation:06d}" / "H8_BOOTSTRAP_PRODUCTION_PACKAGE.json"

def resolve_handle(handle_map: Mapping[str, str], repo: Path) -> Path:
    if set(handle_map) != {INPUT_HANDLE}:
        raise BootstrapBlocked("BOOTSTRAP_HANDLE_MAP_INVALID")
    rel = Path(str(handle_map.get(INPUT_HANDLE) or ""))
    if not str(rel) or rel.is_absolute() or ".." in rel.parts:
        raise BootstrapBlocked("BOOTSTRAP_HANDLE_PATH_INVALID")
    full = (Path(repo).resolve() / rel).resolve()
    if Path(repo).resolve() not in full.parents:
        raise BootstrapBlocked("BOOTSTRAP_HANDLE_PATH_ESCAPE")
    return full

def execute_bound_bootstrap_action(
    *,
    handle_map: Mapping[str, str],
    repo: Path,
    producer_callable: Callable[[Path, Mapping[str, Any]], Path],
    boundary=None,
    trusted_keys=None,
) -> dict[str, Any]:
    repo = Path(repo).resolve()
    boundary = boundary or boundary_module()
    binding = bootstrap_binding(boundary)
    source = resolve_handle(handle_map, repo)
    cur = current_binding(repo)
    if source != (repo / cur["source_snapshot_ref"]).resolve():
        raise BootstrapBlocked("BOOTSTRAP_INPUT_NOT_CURRENT_BOUND_SNAPSHOT")
    expected = expected_provenance_binding(repo)
    produced = Path(producer_callable(source, expected)).resolve()
    if not produced.is_file():
        raise BootstrapBlocked("BOOTSTRAP_PRODUCER_RETURNED_NO_PACKAGE")
    prov = _module(repo / "control/single-door-boundary/preproduction_provenance_guard.py", "h8_boot_provenance")
    proof = prov.validate_package_provenance(repo, produced, trusted_keys=trusted_keys)
    if proof.get("status") != "H8_PREPRODUCTION_PROVENANCE_PASS":
        raise BootstrapBlocked("BOOTSTRAP_PROVENANCE_NOT_PASS")
    dst = incoming_path(repo, cur["generation"])
    if dst.exists():
        raise BootstrapBlocked("BOOTSTRAP_INCOMING_PACKAGE_ALREADY_EXISTS")
    shutil.copyfile(produced, dst)
    copied = prov.validate_incoming_package(repo, trusted_keys=trusted_keys)
    if copied.get("artifact_sha256") != proof.get("artifact_sha256"):
        dst.unlink(missing_ok=True)
        raise BootstrapBlocked("BOOTSTRAP_COPY_HASH_MISMATCH")
    receipt = {
        "contract": boundary.BOUNDARY_CONTRACT,
        "room_token": binding.room_token,
        "action_token": binding.action_token,
        "receipt_token": binding.receipt_token,
        "next_room_token": binding.next_room_token,
        "status": "PASS",
        "evidence": [
            "H8_BOOTSTRAP_PROVENANCE_BINDING:" + str(proof["bootstrap_authority_sha256"]),
            "H8_PACKAGE_SHA256:" + str(proof["artifact_sha256"]),
        ],
    }
    return boundary.validate_action_receipt(binding, receipt)

def main() -> int:
    try:
        req = worker_request("gpt-5.6-sol")
        print(json.dumps({
            "ok": True,
            "status": "H8_PREPRODUCTION_BOOTSTRAP_SINGLE_DOOR_READY",
            "room_token": req["input"],
            "tool_count": len(req["tools"]),
            "next_room_token": NEXT_ROOM_TOKEN,
            "free_chat_execution_authority": False,
            "content_quality_authority": "NONE",
        }, indent=2))
        return 0
    except Exception as exc:
        print(json.dumps({"ok": False, "status": "H8_BOOTSTRAP_BLOCKED", "error": str(exc)}, indent=2))
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
