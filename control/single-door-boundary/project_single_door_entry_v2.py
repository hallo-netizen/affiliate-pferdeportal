#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, importlib.util, json, sys
from pathlib import Path
from typing import Any, Callable, Mapping

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[1]
PROJECT_ENTRY_CONTRACT = "PFERDE_ATELIER_PROJECT_SINGLE_DOOR_ENTRY_V2"
H8_BOUNDARY_CONTRACT = "PFERDE_ATELIER_H8_PREPRODUCTION_BOOTSTRAP_BOUNDARY_V1"
CODEX_BRIDGE_CONTRACT = "PFERDE_ATELIER_CODEX_CLOUD_BOUND_CAPSULE_BRIDGE_V1"
CODEX_BRIDGE_REF = "control/single-door-boundary/CODEX_CLOUD_BOUND_CAPSULE_BRIDGE_V1.json"
CAPSULE_REF = ".pferde-capsule"

class ProjectEntryBlocked(RuntimeError):
    pass

def _module(path: Path, name: str):
    if not path.is_file():
        raise ProjectEntryBlocked("MODULE_MISSING:" + path.name)
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ProjectEntryBlocked("MODULE_LOAD_FAILED:" + path.name)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    try:
        spec.loader.exec_module(mod)
    except Exception:
        sys.modules.pop(name, None)
        raise
    return mod

def _sha256(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def _git_blob_sha1(path: Path) -> str:
    raw = Path(path).read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()

def _load(path: Path) -> Mapping[str, Any]:
    obj = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(obj, Mapping):
        raise ProjectEntryBlocked("JSON_OBJECT_REQUIRED:" + path.name)
    return obj

def _pointer_authority(repo: Path) -> tuple[Mapping[str, Any], Mapping[str, Any]]:
    repo = Path(repo).resolve()
    p = repo / "control/CURRENT_STARTMASTER.json"
    obj = _load(p)
    if obj.get("startmaster") != "STARTMASTER0107":
        raise ProjectEntryBlocked("STARTMASTER_NOT_0107")
    if obj.get("free_chat_execution_authority") is not False:
        raise ProjectEntryBlocked("FREE_CHAT_AUTHORITY_MUST_BE_FALSE")
    if obj.get("hard_worker") != "CODEX_CLOUD":
        raise ProjectEntryBlocked("HARD_WORKER_MUST_BE_CODEX_CLOUD")
    expected = "control/single-door-boundary/project_single_door_entry_v2.py"
    if str(obj.get("gate_ref") or "") != expected:
        raise ProjectEntryBlocked("PROJECT_GATE_REF_INVALID")
    manifest_ref = str(obj.get("h8_boundary_ref") or "")
    manifest_blob = str(obj.get("h8_boundary_git_blob_sha1") or "")
    if manifest_ref != "control/single-door-boundary/H8_PREPRODUCTION_BOOTSTRAP_BOUNDARY.json":
        raise ProjectEntryBlocked("H8_BOUNDARY_REF_INVALID")
    mp = repo / manifest_ref
    if not mp.is_file() or _git_blob_sha1(mp) != manifest_blob:
        raise ProjectEntryBlocked("H8_BOUNDARY_HASH_MISMATCH")
    manifest = _load(mp)
    if manifest.get("contract") != H8_BOUNDARY_CONTRACT:
        raise ProjectEntryBlocked("H8_BOUNDARY_CONTRACT_INVALID")
    if manifest.get("domain_blind") is not True or manifest.get("quality_authority") != "NONE" or manifest.get("content_semantics_authority") != "NONE":
        raise ProjectEntryBlocked("H8_BOUNDARY_NOT_DOMAIN_BLIND")
    bindings = manifest.get("file_bindings")
    if not isinstance(bindings, list) or not bindings:
        raise ProjectEntryBlocked("H8_FILE_BINDINGS_MISSING")
    seen = set()
    for row in bindings:
        if not isinstance(row, dict) or set(row) != {"ref", "git_blob_sha1"}:
            raise ProjectEntryBlocked("H8_FILE_BINDING_INVALID")
        ref = str(row.get("ref") or "")
        if ref in seen or not ref.startswith("control/") or ".." in Path(ref).parts:
            raise ProjectEntryBlocked("H8_FILE_BINDING_REF_INVALID")
        seen.add(ref)
        fp = repo / ref
        if not fp.is_file() or _git_blob_sha1(fp) != str(row.get("git_blob_sha1") or ""):
            raise ProjectEntryBlocked("H8_FILE_BINDING_HASH_MISMATCH:" + ref)
    if expected not in seen:
        raise ProjectEntryBlocked("H8_PROJECT_ENTRY_NOT_HASH_BOUND")
    if CODEX_BRIDGE_REF not in seen:
        raise ProjectEntryBlocked("CODEX_BRIDGE_NOT_HASH_BOUND")
    return obj, manifest

def current_runtime(repo: Path) -> Mapping[str, Any]:
    guard = _module(
        Path(repo) / "control/startmaster0107/runtime_inbox/runtime_batch_slot_guard_h8.py",
        "runtime_guard_h8_entry",
    )
    return guard.validate(
        Path(repo),
        Path(repo) / "control/startmaster0107/runtime_inbox/RUNTIME_BATCH_SLOT_CONTRACT_V1.json",
        Path(repo) / "control/startmaster0107/runtime_inbox/RUNTIME_INBOX_STATE.json",
    )

def _validate_codex_bound_capsule(repo: Path) -> dict[str, Any]:
    repo = Path(repo).resolve()
    bridge = _load(repo / CODEX_BRIDGE_REF)
    if bridge.get("contract") != CODEX_BRIDGE_CONTRACT:
        raise ProjectEntryBlocked("CODEX_BRIDGE_CONTRACT_INVALID")
    if bridge.get("hard_worker") != "CODEX_CLOUD":
        raise ProjectEntryBlocked("CODEX_BRIDGE_HARD_WORKER_INVALID")
    if bridge.get("domain_blind") is not True:
        raise ProjectEntryBlocked("CODEX_BRIDGE_NOT_DOMAIN_BLIND")
    for key in (
        "content_semantics_authority",
        "quality_authority",
        "design_authority",
        "workflow_navigation_authority",
        "publish_authority",
    ):
        if bridge.get(key) != "NONE":
            raise ProjectEntryBlocked("CODEX_BRIDGE_AUTHORITY_INVALID:" + key)
    if bridge.get("authority_mode") != "CURRENT_HASH_BOUND_CODEX_CAPSULE_IS_BOUND_ACTION":
        raise ProjectEntryBlocked("CODEX_BRIDGE_MODE_INVALID")
    if bridge.get("forbidden_host_capability") != "execute_bound_action":
        raise ProjectEntryBlocked("CODEX_BRIDGE_FORBIDDEN_CAPABILITY_INVALID")
    if bridge.get("publish_allowed") is not False:
        raise ProjectEntryBlocked("CODEX_BRIDGE_PUBLISH_MUST_BE_FALSE")

    capsule = repo / CAPSULE_REF
    ticketp = capsule / "TICKET.json"
    manifestp = capsule / "CAPSULE_MANIFEST.json"
    instructionp = capsule / "INSTRUCTION.txt"
    if not ticketp.is_file() or not manifestp.is_file() or not instructionp.is_file():
        raise ProjectEntryBlocked("CODEX_BOUND_CAPSULE_MISSING")
    ticket = _load(ticketp)
    cap = _load(manifestp)
    if ticket.get("contract") != "PFERDE_ATELIER_EXECUTION_TICKET_V2":
        raise ProjectEntryBlocked("CODEX_CAPSULE_TICKET_CONTRACT_INVALID")
    if ticket.get("startmaster") != "STARTMASTER0107":
        raise ProjectEntryBlocked("CODEX_CAPSULE_STARTMASTER_INVALID")
    if ticket.get("step_id") != bridge.get("required_outer_step_id") or int(ticket.get("sequence", -1)) != int(bridge.get("required_outer_sequence", -2)):
        raise ProjectEntryBlocked("CODEX_CAPSULE_NOT_BOUND_107007")
    if cap.get("contract") != "PFERDE_ATELIER_CODEX_CLOUD_CAPSULE_V2":
        raise ProjectEntryBlocked("CODEX_CAPSULE_MANIFEST_CONTRACT_INVALID")
    if cap.get("ticket_id") != ticket.get("ticket_id"):
        raise ProjectEntryBlocked("CODEX_CAPSULE_TICKET_MISMATCH")
    if cap.get("step_id") != ticket.get("step_id") or int(cap.get("sequence", -1)) != int(ticket.get("sequence", -2)):
        raise ProjectEntryBlocked("CODEX_CAPSULE_STEP_MISMATCH")
    if cap.get("navigation_authority_exposed_to_worker") is not False:
        raise ProjectEntryBlocked("CODEX_CAPSULE_NAVIGATION_AUTHORITY_INVALID")
    if cap.get("worker_may_choose_next_step") is not False:
        raise ProjectEntryBlocked("CODEX_CAPSULE_NEXT_STEP_AUTHORITY_INVALID")
    if cap.get("worker_state_write_authority") is not False:
        raise ProjectEntryBlocked("CODEX_CAPSULE_STATE_WRITE_AUTHORITY_INVALID")
    if cap.get("workflow_change_authority") is not False:
        raise ProjectEntryBlocked("CODEX_CAPSULE_WORKFLOW_CHANGE_AUTHORITY_INVALID")
    if cap.get("repo_worktree_available_for_bound_step") is not True:
        raise ProjectEntryBlocked("CODEX_CAPSULE_WORKTREE_NOT_BOUND")
    if cap.get("api_required") is not False:
        raise ProjectEntryBlocked("CODEX_CAPSULE_API_DEPENDENCY_INVALID")

    ptr = _load(repo / "control/CURRENT_STARTMASTER.json")
    statep = repo / str(ptr.get("state_ref") or "")
    rootp = repo / str(ptr.get("root_ref") or "")
    state = _load(statep)
    root = _load(rootp)
    gate = state.get("execution_gate") or {}
    bundlep = repo / str(gate.get("bundle_ref") or "")
    if not bundlep.is_file():
        raise ProjectEntryBlocked("CODEX_CAPSULE_BUNDLE_MISSING")
    bundle = _load(bundlep)
    if ticket.get("state_sha256") != _sha256(statep):
        raise ProjectEntryBlocked("CODEX_CAPSULE_STATE_HASH_MISMATCH")
    if root.get("current_state_sha256") != ticket.get("state_sha256"):
        raise ProjectEntryBlocked("CODEX_CAPSULE_ROOT_HASH_MISMATCH")
    if ticket.get("bundle_sha256") != _sha256(bundlep):
        raise ProjectEntryBlocked("CODEX_CAPSULE_BUNDLE_HASH_MISMATCH")
    if gate.get("bundle_sha256") != ticket.get("bundle_sha256"):
        raise ProjectEntryBlocked("CODEX_CAPSULE_GATE_BUNDLE_HASH_MISMATCH")
    expected_instruction = str(bundle.get("instruction") or "").strip() + "\n"
    if instructionp.read_text(encoding="utf-8") != expected_instruction:
        raise ProjectEntryBlocked("CODEX_CAPSULE_INSTRUCTION_MISMATCH")

    return {
        "contract": CODEX_BRIDGE_CONTRACT,
        "status": "CODEX_CLOUD_BOUND_CAPSULE_PASS",
        "authority_mode": bridge["authority_mode"],
        "step_id": ticket["step_id"],
        "sequence": int(ticket["sequence"]),
        "ticket_id": ticket["ticket_id"],
        "state_sha256": ticket["state_sha256"],
        "bundle_sha256": ticket["bundle_sha256"],
        "instruction_ref": ".pferde-capsule/INSTRUCTION.txt",
        "receipt_schema_ref": ".pferde-capsule/RECEIPT_SCHEMA.json",
        "completion_command": "python3 control/output-quarantine/runtime_entry_gate.py complete .pferde-capsule/RECEIPT.json",
        "navigation_decision": False,
        "content_semantics_inspected": False,
        "quality_authority": "NONE",
        "publish_allowed": False,
    }

def resolve_entry(
    *,
    repo: Path,
    model: str = "gpt-5.6-sol",
    runtime_provider: Callable[[Path], Mapping[str, Any]] | None = None,
    route_provider: Callable[[Path, int, str], Mapping[str, Any]] | None = None,
    incoming_provenance_provider: Callable[[Path], Mapping[str, Any]] | None = None,
    attached_provenance_provider: Callable[[Path], Mapping[str, Any]] | None = None,
    codex_capsule_provider: Callable[[Path], Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    repo = Path(repo).resolve()
    _pointer_authority(repo)
    runtime = dict((runtime_provider or current_runtime)(repo))
    status = runtime.get("status")
    if status == "READY_IDLE":
        return {"ok": True, "contract": PROJECT_ENTRY_CONTRACT, "status": "PROJECT_ARMED_NO_ACTIVE_BATCH", "worker_request": None, "authoritative_execution_origin": "SINGLE_DOOR_EXECUTOR_ONLY", "publish_allowed": False}
    if status == "READY_WAITING_PACKAGE":
        boot = _module(repo / "control/single-door-boundary/single_door_bootstrap.py", "h8_boot_entry")
        prov = _module(repo / "control/single-door-boundary/preproduction_provenance_guard.py", "h8_prov_entry")
        provider = incoming_provenance_provider or prov.validate_incoming_package
        incoming = prov.incoming_package_path(repo, int(runtime.get("generation") or 0))
        if incoming_provenance_provider is None and not incoming.exists():
            req = boot.worker_request(model)
            return {"ok": True, "contract": PROJECT_ENTRY_CONTRACT, "status": "PREPRODUCTION_BOOTSTRAP_SINGLE_DOOR_REQUIRED", "room_token": boot.ROOM_TOKEN, "worker_request": req, "next_room_after_pass": boot.NEXT_ROOM_TOKEN, "authoritative_execution_origin": "SINGLE_DOOR_EXECUTOR_ONLY", "publish_allowed": False}
        try:
            proof = dict(provider(repo))
        except Exception as exc:
            raise ProjectEntryBlocked("INCOMING_PACKAGE_PROVENANCE_INVALID:" + str(exc)) from exc
        pre = _module(repo / "control/single-door-boundary/single_door_preproduction_handoff.py", "h8_pre_entry")
        req = pre.worker_request(model)
        return {"ok": True, "contract": PROJECT_ENTRY_CONTRACT, "status": "PREPRODUCTION_SIGNED_PACKAGE_SINGLE_DOOR_REQUIRED", "room_token": pre.ROOM_TOKEN, "worker_request": req, "next_room_after_pass": pre.NEXT_ROOM_TOKEN, "bootstrap_authority_sha256": proof.get("bootstrap_authority_sha256"), "authoritative_execution_origin": "SINGLE_DOOR_EXECUTOR_ONLY", "publish_allowed": False}
    if status == "RUNTIME_INPUTS_BOUND":
        prov = _module(repo / "control/single-door-boundary/preproduction_provenance_guard.py", "h8_prov_bound")
        provider = attached_provenance_provider or prov.validate_attached_package
        proof = dict(provider(repo))
        if proof.get("status") != "H8_PREPRODUCTION_PROVENANCE_PASS":
            raise ProjectEntryBlocked("ATTACHED_PACKAGE_PROVENANCE_NOT_PASS")
        count = runtime.get("selected_item_count")
        if not isinstance(count, int) or count < 1:
            raise ProjectEntryBlocked("BOUND_ITEM_COUNT_INVALID")
        if route_provider is not None:
            routed = dict(route_provider(repo, count, model))
            room = routed.get("room_token")
        else:
            route = _module(repo / "control/single-door-boundary/single_door_route_binding.py", "h8_route_entry")
            bound = route.materialize(count)
            room = bound.get("first_room_token")
        if room != "R_001":
            raise ProjectEntryBlocked("PRODUCTIVE_ROUTE_ENTRY_INVALID")
        capsule_proof = dict((codex_capsule_provider or _validate_codex_bound_capsule)(repo))
        if capsule_proof.get("status") != "CODEX_CLOUD_BOUND_CAPSULE_PASS":
            raise ProjectEntryBlocked("CODEX_BOUND_CAPSULE_NOT_PASS")
        return {
            "ok": True,
            "contract": PROJECT_ENTRY_CONTRACT,
            "status": "PRODUCTIVE_SINGLE_DOOR_READY",
            "room_token": room,
            "worker_request": None,
            "codex_bound_action": capsule_proof,
            "item_count": count,
            "bootstrap_authority_sha256": proof.get("bootstrap_authority_sha256"),
            "authoritative_execution_origin": "CODEX_CLOUD_BOUND_CAPSULE_ONLY",
            "custom_function_capability_required": False,
            "workflow_navigation_decision": False,
            "content_semantics_inspected": False,
            "quality_authority": "NONE",
            "publish_allowed": False,
        }
    raise ProjectEntryBlocked("RUNTIME_STATUS_NOT_ROUTABLE:" + str(status))

def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("command", nargs="?", default="status", choices=["status"])
    ap.add_argument("--repo", default=str(REPO_ROOT))
    args = ap.parse_args(argv)
    try:
        print(json.dumps(resolve_entry(repo=Path(args.repo)), ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        print(json.dumps({"ok": False, "status": "PROJECT_SINGLE_DOOR_ENTRY_BLOCKED", "error": str(exc), "publish_allowed": False}, ensure_ascii=False, indent=2))
        return 2

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
