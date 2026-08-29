#!/usr/bin/env python3
"""Compatibility shim: current worktree-aware entrance + verified V3 capsule handoff.

This shim changes no domain/content/quality/design/publish logic. It only lets
the previously verified V3 runtime controller run behind the newer entrance
policy CAPSULE_NAVIGATION_REPO_BOUND_STEP while the issued worker capsule
remains isolated by runtime_gate_v3.py.
"""
from __future__ import annotations
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = HERE / "runtime_gate_v3.py"

spec = importlib.util.spec_from_file_location("pferde_runtime_gate_v3", TARGET)
if spec is None or spec.loader is None:
    raise SystemExit("RUNTIME_V3_IMPORT_FAILED")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def compat_authority(master: Path):
    pointer_path = master / "control" / "CURRENT_STARTMASTER.json"
    if not pointer_path.is_file():
        raise mod.Blocked("STARTMASTER_POINTER_MISSING")
    pointer = mod.load(pointer_path)
    rootp = mod.safe(master, pointer.get("root_ref"))
    statep = mod.safe(master, pointer.get("state_ref"))
    if not rootp.is_file() or not statep.is_file():
        raise mod.Blocked("ROOT_OR_STATE_MISSING")
    root, state = mod.load(rootp), mod.load(statep)
    if pointer.get("startmaster") != root.get("startmaster") or root.get("startmaster") != state.get("startmaster"):
        raise mod.Blocked("STARTMASTER_IDENTITY_MISMATCH")
    if mod.sha(statep) != root.get("current_state_sha256"):
        raise mod.Blocked("STATE_HASH_MISMATCH")
    if root.get("next_allowed_step") != state.get("next_allowed_step"):
        raise mod.Blocked("STEP_ROOT_STATE_MISMATCH")
    if state.get("publish_allowed") is not False or root.get("publish_allowed") is not False:
        raise mod.Blocked("AUTO_PUBLISH_FORBIDDEN")
    gate = state.get("execution_gate") or {}
    if gate.get("enforced") is not True:
        raise mod.Blocked("GATE_NOT_ENFORCED")
    if gate.get("step_id") != state.get("next_allowed_step"):
        raise mod.Blocked("GATE_STEP_MISMATCH")
    if gate.get("state_write_authority") != "ENTRANCE_GATE_ONLY":
        raise mod.Blocked("STATE_WRITE_AUTHORITY_INVALID")
    if gate.get("unknown_step_policy") != "DENY":
        raise mod.Blocked("UNKNOWN_STEP_POLICY_INVALID")
    if gate.get("free_chat_direct_execution_valid") is not False:
        raise mod.Blocked("FREE_CHAT_MUST_BE_INVALID")
    if gate.get("domain_logic_authority") != "NONE" or gate.get("content_quality_design_authority") != "NONE":
        raise mod.Blocked("DOMAIN_AUTHORITY_MUST_BE_NONE")
    if gate.get("worker_context_policy") != "CAPSULE_NAVIGATION_REPO_BOUND_STEP":
        raise mod.Blocked("WORKER_CONTEXT_POLICY_INVALID")
    if gate.get("repeat_or_backtrack_policy") != "DENY_UNLESS_PREBOUND_NEXT_BINDING":
        raise mod.Blocked("BACKTRACK_POLICY_INVALID")
    if gate.get("api_dependency") != "NONE":
        raise mod.Blocked("API_DEPENDENCY_FORBIDDEN")
    if gate.get("hard_worker_target") != "CODEX_CLOUD":
        raise mod.Blocked("HARD_WORKER_NOT_CODEX_CLOUD")
    controller_ref = mod.rel(gate.get("runtime_controller_ref"))
    controller_path = mod.safe(master, controller_ref)
    if not controller_path.is_file():
        raise mod.Blocked("RUNTIME_CONTROLLER_MISSING")
    if mod.sha(controller_path) != gate.get("runtime_controller_sha256"):
        raise mod.Blocked("RUNTIME_CONTROLLER_HASH_MISMATCH")
    bp = mod.safe(master, gate.get("bundle_ref"))
    if not bp.is_file():
        raise mod.Blocked("BUNDLE_MISSING")
    if mod.sha(bp) != gate.get("bundle_sha256"):
        raise mod.Blocked("BUNDLE_HASH_MISMATCH")
    bundle = mod.load(bp)
    if bundle.get("step_id") != gate.get("step_id") or int(bundle.get("sequence", -1)) != int(gate.get("sequence", -2)):
        raise mod.Blocked("BUNDLE_IDENTITY_MISMATCH")
    return pointer, rootp, statep, root, state, gate, bundle, bp

mod.authority = compat_authority

if __name__ == "__main__":
    raise SystemExit(mod.main())
