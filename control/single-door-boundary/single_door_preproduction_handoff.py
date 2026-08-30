#!/usr/bin/env python3
from __future__ import annotations

import base64
import copy
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any, Callable, Mapping

try:
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    from cryptography.exceptions import InvalidSignature
except Exception:
    Ed25519PublicKey = None
    InvalidSignature = Exception

HERE = Path(__file__).resolve().parent
BOUNDARY_PATH = HERE / "single_door_boundary.py"
REPO_ROOT = HERE.parents[1]
PREPRODUCTION_CONTRACT = "PFERDE_ATELIER_PREPRODUCTION_SINGLE_DOOR_V1"
PACKAGE_CONTRACT = "PSERC_APPROVED_PRODUCTION_PACKAGE_V1"
RELEASE_CONTRACT = "WORKFLOW_SUPERVISOR_RELEASE_V2_SIGNED"
ROOM_TOKEN = "R_PRE_001"
ACTION_TOKEN = "A_PRE_001"
INPUT_HANDLE = "I_PRE_PACKAGE_001"
RECEIPT_TOKEN = "P_PRE_001"
NEXT_ROOM_TOKEN = "R_001"
MAX_PACKAGE_BYTES = 12 * 1024 * 1024
SHA_RE = re.compile(r"^[a-f0-9]{64}$")

# Public verification material only. Private signing keys remain outside the repository.
TRUSTED_SIGNING_KEYS = {
    "workflow-ed25519-153d2518dba7b025": {"sha256": "153d2518dba7b025c92036583fcf86e31288a2b9f9e0977fce655225446f2a59", "public_key_b64": "Mcl55V5yPSscQZjGC0BPPHoSxp2xiDNzicGDopaZDPQ="},
    "workflow-ed25519-b15660ee915a5826": {"sha256": "b15660ee915a5826e3b658c99043b448ba212596f44ad6a09add09cfbd2d48f3", "public_key_b64": "mwu5MTHnBDhZrzKxeqEnDtiDWdgIDYAoY8Gc167R7dc="},
    "workflow-ed25519-8f521756284cb375": {"sha256": "8f521756284cb375c907f508dac333f51b71b515419ee271ca68fa149db66f87", "public_key_b64": "6FCxYycU2bJysJFvtH5xZ0ia+k59ZLyK6Av8d9/ujm0="},
    "workflow-ed25519-7ba1c78405b15306": {"sha256": "7ba1c78405b15306000ed241c3de2d7ab14c23ca2a9f3a4c27da5664711c4771", "public_key_b64": "PqyrEbUTc8JlUNq07kgBBecKRWlh/LxxkBjIqlS0KNw="},
}
PACKAGE_KEYS = {"contract", "fact_pack_bundle_sha256", "production_plan_sha256", "workflow_release_sha256", "package_id", "source", "fact_pack_bundle", "production_plan", "workflow_release", "package_payload_sha256"}

class HandoffBlocked(RuntimeError): pass

def stable_hash(obj: Any) -> str:
    return hashlib.sha256(json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()

def file_sha(path: Path) -> str: return hashlib.sha256(path.read_bytes()).hexdigest()

def _load_module(path: Path, name: str):
    if not path.is_file(): raise HandoffBlocked(f"MODULE_MISSING:{path.name}")
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None: raise HandoffBlocked(f"MODULE_LOAD_FAILED:{path.name}")
    mod = importlib.util.module_from_spec(spec); sys.modules[name] = mod
    try: spec.loader.exec_module(mod)
    except Exception:
        sys.modules.pop(name, None); raise
    return mod

def boundary_module(): return _load_module(BOUNDARY_PATH, "single_door_boundary_h7")

def preproduction_binding(boundary=None):
    boundary = boundary or boundary_module()
    return boundary.DoorBinding.from_mapping({"contract": boundary.BOUNDARY_CONTRACT, "room_token": ROOM_TOKEN, "action_token": ACTION_TOKEN, "receipt_token": RECEIPT_TOKEN, "next_room_token": NEXT_ROOM_TOKEN, "input_handles": [INPUT_HANDLE]})

def worker_request(model: str, boundary=None) -> dict[str, Any]:
    boundary = boundary or boundary_module()
    return boundary.build_worker_request(binding=preproduction_binding(boundary), model=model)

def _verify_release_signature(release: Mapping[str, Any], trusted_keys: Mapping[str, Mapping[str, str]]) -> None:
    if Ed25519PublicKey is None: raise HandoffBlocked("ED25519_RUNTIME_UNAVAILABLE")
    if release.get("contract") != RELEASE_CONTRACT or release.get("status") != "PASS": raise HandoffBlocked("WORKFLOW_RELEASE_SHAPE_INVALID")
    if release.get("signature_algorithm") != "ED25519": raise HandoffBlocked("WORKFLOW_RELEASE_SIGNATURE_ALGORITHM_INVALID")
    key_id = release.get("signing_key_id"); trusted = trusted_keys.get(str(key_id))
    if not trusted: raise HandoffBlocked("WORKFLOW_RELEASE_SIGNING_KEY_UNTRUSTED")
    if release.get("signing_public_key_sha256") != trusted.get("sha256"): raise HandoffBlocked("WORKFLOW_RELEASE_SIGNING_KEY_IDENTITY_MISMATCH")
    payload = dict(release)
    payload.pop("release_payload_sha256", None); payload.pop("signature_b64", None); payload.pop("release_sha256", None)
    payload_sha = stable_hash(payload); declared = release.get("release_payload_sha256")
    if not isinstance(declared, str) or not SHA_RE.fullmatch(declared) or declared != payload_sha: raise HandoffBlocked("WORKFLOW_RELEASE_PAYLOAD_HASH_MISMATCH")
    try:
        sig = base64.b64decode(str(release.get("signature_b64") or ""), validate=True)
        public = base64.b64decode(str(trusted.get("public_key_b64") or ""), validate=True)
    except Exception as exc: raise HandoffBlocked("WORKFLOW_RELEASE_SIGNATURE_ENCODING_INVALID") from exc
    try: Ed25519PublicKey.from_public_bytes(public).verify(sig, payload_sha.encode("ascii"))
    except (InvalidSignature, ValueError) as exc: raise HandoffBlocked("WORKFLOW_RELEASE_SIGNATURE_INVALID") from exc
    release_copy = dict(release); release_copy.pop("release_sha256", None)
    expected = stable_hash(release_copy); declared_release = release.get("release_sha256")
    if not isinstance(declared_release, str) or not SHA_RE.fullmatch(declared_release) or declared_release != expected: raise HandoffBlocked("WORKFLOW_RELEASE_HASH_MISMATCH")

def validate_production_package(path: Path, *, trusted_keys: Mapping[str, Mapping[str, str]] | None = None) -> dict[str, Any]:
    path = Path(path)
    if path.suffix.lower() != ".json": raise HandoffBlocked("HANDOFF_FILE_MUST_BE_JSON")
    if not path.is_file(): raise HandoffBlocked("HANDOFF_FILE_MISSING")
    size = path.stat().st_size
    if size < 1 or size > MAX_PACKAGE_BYTES: raise HandoffBlocked("HANDOFF_FILE_SIZE_INVALID")
    try: env = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc: raise HandoffBlocked("HANDOFF_JSON_INVALID") from exc
    if not isinstance(env, dict) or set(env) != PACKAGE_KEYS: raise HandoffBlocked("HANDOFF_PACKAGE_SCHEMA_INVALID")
    if env.get("contract") != PACKAGE_CONTRACT: raise HandoffBlocked("HANDOFF_PACKAGE_CONTRACT_INVALID")
    bundle, plan, release = env.get("fact_pack_bundle"), env.get("production_plan"), env.get("workflow_release")
    if not all(isinstance(x, dict) for x in (bundle, plan, release)): raise HandoffBlocked("HANDOFF_PACKAGE_COMPONENT_INVALID")
    hashes = {"fact_pack_bundle_sha256": stable_hash(bundle), "production_plan_sha256": stable_hash(plan), "workflow_release_sha256": stable_hash(release)}
    for field, actual in hashes.items():
        declared = env.get(field)
        if not isinstance(declared, str) or not SHA_RE.fullmatch(declared) or declared != actual: raise HandoffBlocked(f"HANDOFF_COMPONENT_HASH_MISMATCH:{field}")
    expected_id = stable_hash({"contract": PACKAGE_CONTRACT, **hashes})
    if env.get("package_id") != expected_id: raise HandoffBlocked("HANDOFF_PACKAGE_ID_MISMATCH")
    payload = copy.deepcopy(env); declared_payload = payload.pop("package_payload_sha256", None)
    if not isinstance(declared_payload, str) or not SHA_RE.fullmatch(declared_payload) or stable_hash(payload) != declared_payload: raise HandoffBlocked("HANDOFF_PACKAGE_PAYLOAD_HASH_MISMATCH")
    _verify_release_signature(release, trusted_keys or TRUSTED_SIGNING_KEYS)
    return {"ok": True, "status": "SIGNED_PRODUCTION_PACKAGE_HANDOFF_VALID", "package_id": expected_id, "artifact_sha256": file_sha(path), "bytes": size, "content_semantics_inspected": False, "publish_allowed": False}

def resolve_handle(handle_map: Mapping[str, str], handle: str, repo: Path) -> Path:
    if set(handle_map) != {INPUT_HANDLE}: raise HandoffBlocked("HANDLE_MAP_MUST_CONTAIN_EXACTLY_BOUND_HANDLE")
    value = handle_map.get(handle)
    if not isinstance(value, str) or not value: raise HandoffBlocked("BOUND_HANDLE_MISSING")
    rel = Path(value)
    if rel.is_absolute() or ".." in rel.parts: raise HandoffBlocked("BOUND_HANDLE_PATH_INVALID")
    full = (repo / rel).resolve(); root = repo.resolve()
    if root not in full.parents and full != root: raise HandoffBlocked("BOUND_HANDLE_PATH_ESCAPE")
    return full

def execute_bound_preproduction_action(*, handle_map: Mapping[str, str], repo: Path, attach_callable: Callable[[Path], Mapping[str, Any]], boundary=None, trusted_keys: Mapping[str, Mapping[str, str]] | None = None) -> dict[str, Any]:
    boundary = boundary or boundary_module(); binding = preproduction_binding(boundary)
    package_path = resolve_handle(handle_map, binding.input_handles[0], Path(repo))
    proof = validate_production_package(package_path, trusted_keys=trusted_keys)
    result = attach_callable(package_path)
    if not isinstance(result, Mapping) or result.get("status") != "RUNTIME_BATCH_EXECUTION_READY": raise HandoffBlocked("ATTACH_PACKAGE_DID_NOT_REACH_EXECUTION_READY")
    receipt = {"contract": boundary.BOUNDARY_CONTRACT, "room_token": binding.room_token, "action_token": binding.action_token, "receipt_token": binding.receipt_token, "next_room_token": binding.next_room_token, "status": "PASS", "evidence": ["SIGNED_PACKAGE_VALID:" + proof["artifact_sha256"], "RUNTIME_BATCH_EXECUTION_READY"]}
    return boundary.validate_action_receipt(binding, receipt)

def attach_via_current_lifecycle(*, repo: Path, handle_map: Mapping[str, str], boundary=None) -> dict[str, Any]:
    repo = Path(repo).resolve(); lifecycle = _load_module(repo / "control/startmaster0107/runtime_inbox/runtime_batch_slot_lifecycle.py", "runtime_batch_slot_lifecycle_h7")
    contract_path = repo / "control/startmaster0107/runtime_inbox/RUNTIME_BATCH_SLOT_CONTRACT_V1.json"
    return execute_bound_preproduction_action(handle_map=handle_map, repo=repo, attach_callable=lambda p: lifecycle.attach_package(repo, contract_path, str(p)), boundary=boundary)

def authoritative_handoff(receipt: Mapping[str, Any] | None, boundary=None) -> dict[str, Any]:
    if not isinstance(receipt, Mapping): raise HandoffBlocked("SINGLE_DOOR_RECEIPT_REQUIRED")
    boundary = boundary or boundary_module(); checked = boundary.validate_action_receipt(preproduction_binding(boundary), receipt)
    if checked.get("status") != "PASS": raise HandoffBlocked("SINGLE_DOOR_PASS_RECEIPT_REQUIRED")
    return {"ok": True, "status": "PROJECT_HANDOFF_AUTHORITY_PASS", "authoritative_origin": "SINGLE_DOOR_EXECUTOR_ONLY", "next_room_token": NEXT_ROOM_TOKEN}

def main() -> int:
    try:
        req = worker_request("gpt-5.6-sol")
        print(json.dumps({"ok": True, "status": "H7_PREPRODUCTION_SINGLE_DOOR_READY", "room_token": req["input"], "tool_count": len(req["tools"]), "parallel_tool_calls": req["parallel_tool_calls"], "next_room_token": NEXT_ROOM_TOKEN, "free_chat_execution_authority": False}, indent=2)); return 0
    except Exception as exc:
        print(json.dumps({"ok": False, "status": "H7_BLOCKED", "error": str(exc)}, indent=2)); return 2
if __name__ == "__main__": raise SystemExit(main())
