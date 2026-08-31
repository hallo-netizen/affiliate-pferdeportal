#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any, Mapping

HERE = Path(__file__).resolve().parent
BOOTSTRAP_BINDING_CONTRACT = "PFERDE_ATELIER_H8_BOOTSTRAP_SIGNED_BINDING_V1"
AUTHORITATIVE_ORIGIN = "SINGLE_DOOR_BOOTSTRAP_ONLY"
ROOM_TOKEN = "R_BOOT_001"
RECEIPT_TOKEN = "P_BOOT_001"

class ProvenanceBlocked(RuntimeError):
    pass

def _module(path: Path, name: str):
    if not path.is_file():
        raise ProvenanceBlocked("MODULE_MISSING:" + path.name)
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ProvenanceBlocked("MODULE_LOAD_FAILED:" + path.name)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    try:
        spec.loader.exec_module(mod)
    except Exception:
        sys.modules.pop(name, None)
        raise
    return mod

def stable_hash(obj: Any) -> str:
    return hashlib.sha256(json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()

def file_sha(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def _state(repo: Path) -> dict[str, Any]:
    p = Path(repo).resolve() / "control/startmaster0107/runtime_inbox/RUNTIME_INBOX_STATE.json"
    obj = json.loads(p.read_text(encoding="utf-8"))
    if obj.get("contract") != "PFERDE_ATELIER_RUNTIME_BATCH_SLOT_STATE_V1":
        raise ProvenanceBlocked("RUNTIME_STATE_CONTRACT_INVALID")
    return obj

def expected_binding(repo: Path) -> dict[str, Any]:
    s = _state(repo)
    if s.get("status") not in {"BATCH_READY_PACKAGE_PENDING", "EXECUTION_READY"}:
        raise ProvenanceBlocked("RUNTIME_STATE_NOT_ACTIVE_FOR_PROVENANCE")
    body = {
        "contract": BOOTSTRAP_BINDING_CONTRACT,
        "room_token": ROOM_TOKEN,
        "receipt_token": RECEIPT_TOKEN,
        "generation": int(s["generation"]),
        "batch_sha256": str(s["batch_sha256"]),
        "source_snapshot_sha256": str(s["source_snapshot_sha256"]),
        "source_manifest_sha256": str(s["source_manifest_sha256"]),
        "authoritative_origin": AUTHORITATIVE_ORIGIN,
    }
    body["binding_sha256"] = stable_hash(body)
    return body

def incoming_package_path(repo: Path, generation: int) -> Path:
    return Path(repo).resolve() / "control/startmaster0107/runtime_inbox/generations" / f"{generation:06d}" / "H8_BOOTSTRAP_PRODUCTION_PACKAGE.json"

def _binding_from_release(release: Mapping[str, Any]) -> Mapping[str, Any]:
    binding = release.get("h8_bootstrap_binding")
    if not isinstance(binding, Mapping):
        raise ProvenanceBlocked("H8_SIGNED_BOOTSTRAP_BINDING_MISSING")
    expected_keys = {
        "contract", "room_token", "receipt_token", "generation", "batch_sha256",
        "source_snapshot_sha256", "source_manifest_sha256", "authoritative_origin", "binding_sha256",
    }
    if set(binding) != expected_keys:
        raise ProvenanceBlocked("H8_SIGNED_BOOTSTRAP_BINDING_FIELDS_INVALID")
    payload = dict(binding)
    declared = payload.pop("binding_sha256", None)
    if declared != stable_hash(payload):
        raise ProvenanceBlocked("H8_SIGNED_BOOTSTRAP_BINDING_HASH_INVALID")
    return binding

def validate_package_provenance(repo: Path, package_path: Path, *, trusted_keys=None) -> dict[str, Any]:
    repo = Path(repo).resolve()
    package_path = Path(package_path).resolve()
    pre = _module(repo / "control/single-door-boundary/single_door_preproduction_handoff.py", "h8_provenance_pre")
    package_proof = pre.validate_production_package(package_path, trusted_keys=trusted_keys) if trusted_keys is not None else pre.validate_production_package(package_path)
    env = json.loads(package_path.read_text(encoding="utf-8"))
    release = env.get("workflow_release")
    if not isinstance(release, Mapping):
        raise ProvenanceBlocked("WORKFLOW_RELEASE_MISSING")
    actual = dict(_binding_from_release(release))
    expected = expected_binding(repo)
    if actual != expected:
        raise ProvenanceBlocked("H8_SIGNED_BOOTSTRAP_BINDING_NOT_CURRENT")
    return {
        "ok": True,
        "status": "H8_PREPRODUCTION_PROVENANCE_PASS",
        "artifact_sha256": package_proof["artifact_sha256"],
        "package_id": package_proof["package_id"],
        "bootstrap_authority_sha256": actual["binding_sha256"],
        "authoritative_origin": AUTHORITATIVE_ORIGIN,
        "content_semantics_inspected": False,
        "quality_authority": "NONE",
        "publish_allowed": False,
    }

def validate_incoming_package(repo: Path, *, trusted_keys=None) -> dict[str, Any]:
    s = _state(repo)
    if s.get("status") != "BATCH_READY_PACKAGE_PENDING":
        raise ProvenanceBlocked("INCOMING_PROVENANCE_REQUIRES_PENDING_STATE")
    p = incoming_package_path(repo, int(s["generation"]))
    if not p.is_file():
        raise ProvenanceBlocked("H8_BOOTSTRAP_INCOMING_PACKAGE_MISSING")
    return validate_package_provenance(repo, p, trusted_keys=trusted_keys)

def validate_attached_package(repo: Path, *, trusted_keys=None) -> dict[str, Any]:
    repo = Path(repo).resolve()
    s = _state(repo)
    if s.get("status") != "EXECUTION_READY":
        raise ProvenanceBlocked("ATTACHED_PROVENANCE_REQUIRES_EXECUTION_READY")
    ref = Path(str(s.get("production_package_ref") or ""))
    if not str(ref) or ref.is_absolute() or ".." in ref.parts:
        raise ProvenanceBlocked("ATTACHED_PACKAGE_REF_INVALID")
    p = (repo / ref).resolve()
    if repo not in p.parents:
        raise ProvenanceBlocked("ATTACHED_PACKAGE_REF_ESCAPE")
    if not p.is_file() or file_sha(p) != str(s.get("production_package_sha256") or ""):
        raise ProvenanceBlocked("ATTACHED_PACKAGE_HASH_MISMATCH")
    return validate_package_provenance(repo, p, trusted_keys=trusted_keys)

def main() -> int:
    try:
        print(json.dumps(validate_attached_package(HERE.parents[1]), ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        print(json.dumps({"ok": False, "status": "H8_PREPRODUCTION_PROVENANCE_BLOCKED", "error": str(exc), "publish_allowed": False}, ensure_ascii=False, indent=2))
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
