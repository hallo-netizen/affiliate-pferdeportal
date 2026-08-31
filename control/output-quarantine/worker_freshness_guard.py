#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
POINTER = REPO / "control/CURRENT_STARTMASTER.json"


class Blocked(RuntimeError):
    pass


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(value: str) -> Path:
    p = Path(str(value or ""))
    if not value or p.is_absolute() or ".." in p.parts:
        raise Blocked("INVALID_RELATIVE_PATH")
    return p


def git(*args: str) -> str:
    try:
        cp = subprocess.run(
            ["git", *args],
            cwd=REPO,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except Exception as exc:
        raise Blocked("GIT_CHECK_FAILED:" + " ".join(args)) from exc
    return cp.stdout.strip()


def local_checkout_identity() -> tuple[str, str]:
    head = git("rev-parse", "HEAD")
    branch = git("branch", "--show-current")
    dirty = git("status", "--porcelain", "--untracked-files=no")
    if dirty:
        raise Blocked("TRACKED_WORKTREE_NOT_CLEAN")
    return head, branch


def validate() -> dict:
    head, branch = local_checkout_identity()
    if not POINTER.is_file():
        raise Blocked("STARTMASTER_POINTER_MISSING")
    ptr = load(POINTER)
    if ptr.get("contract") != "PFERDE_ATELIER_CURRENT_STARTMASTER_POINTER_V2":
        raise Blocked("STARTMASTER_POINTER_CONTRACT_INVALID")
    if ptr.get("free_chat_execution_authority") is not False:
        raise Blocked("FREE_CHAT_EXECUTION_MUST_BE_FALSE")
    if ptr.get("hard_worker") != "CODEX_CLOUD":
        raise Blocked("HARD_WORKER_MUST_BE_CODEX_CLOUD")
    if ptr.get("visible_output_authority") != "RELEASE_RECEIPT_ONLY":
        raise Blocked("VISIBLE_OUTPUT_AUTHORITY_INVALID")

    statep = REPO / rel(ptr.get("state_ref"))
    rootp = REPO / rel(ptr.get("root_ref"))
    policyp = REPO / rel(ptr.get("visible_output_policy_ref"))
    runtime_entryp = REPO / rel(ptr.get("execution_entrance_gate_ref"))
    if not all(p.is_file() for p in (statep, rootp, policyp, runtime_entryp)):
        raise Blocked("AUTHORITY_FILE_MISSING")

    state = load(statep)
    root = load(rootp)
    policy = load(policyp)
    if ptr.get("startmaster") != state.get("startmaster") or state.get("startmaster") != root.get("startmaster"):
        raise Blocked("STARTMASTER_IDENTITY_MISMATCH")
    if sha256(statep) != root.get("current_state_sha256"):
        raise Blocked("STATE_HASH_MISMATCH")
    if root.get("next_allowed_step") != state.get("next_allowed_step"):
        raise Blocked("ROOT_STATE_STEP_MISMATCH")
    if root.get("execution_entrance_gate") != ptr.get("execution_entrance_gate_ref"):
        raise Blocked("OFFICIAL_RUNTIME_ENTRY_MISMATCH")
    if sha256(policyp) != ptr.get("visible_output_policy_sha256"):
        raise Blocked("OUTPUT_POLICY_HASH_MISMATCH")
    if sha256(runtime_entryp) != ptr.get("execution_entrance_gate_sha256"):
        raise Blocked("RUNTIME_ENTRY_HASH_MISMATCH")

    if policy.get("chat_execution_authority") != "NONE" or policy.get("chat_output_authority") != "NONE":
        raise Blocked("CHAT_AUTHORITY_MUST_BE_NONE")
    if policy.get("domain_logic_authority") != "NONE" or policy.get("quality_authority") != "NONE":
        raise Blocked("FRESHNESS_GUARD_MUST_BE_DOMAIN_BLIND")
    if policy.get("visible_project_result_authority") != "RELEASE_RECEIPT_ONLY":
        raise Blocked("POLICY_VISIBLE_RESULT_AUTHORITY_INVALID")
    if policy.get("require_current_bound_checkout_before_start") is not True:
        raise Blocked("BOUND_CHECKOUT_REQUIREMENT_MISSING")
    if policy.get("codex_cloud_offline_freshness") is not True:
        raise Blocked("OFFLINE_FRESHNESS_POLICY_MISSING")

    gate = state.get("execution_gate") or {}
    if gate.get("step_id") != state.get("next_allowed_step"):
        raise Blocked("STEP_GATE_MISMATCH")
    bundlep = REPO / rel(gate.get("bundle_ref"))
    if not bundlep.is_file() or sha256(bundlep) != gate.get("bundle_sha256"):
        raise Blocked("BUNDLE_HASH_MISMATCH")
    bundle = load(bundlep)
    bindings = {
        str(row.get("ref") or ""): str(row.get("sha256") or "")
        for row in (bundle.get("authorized_inputs") or [])
        if isinstance(row, dict)
    }
    required = {
        "control/output-quarantine/worker_freshness_guard.py": sha256(Path(__file__).resolve()),
        "control/output-quarantine/OUTPUT_VISIBILITY_POLICY.json": sha256(policyp),
        ptr.get("execution_entrance_gate_ref"): sha256(runtime_entryp),
    }
    for ref, digest in required.items():
        if bindings.get(ref) != digest:
            raise Blocked("REQUIRED_SECURITY_INPUT_NOT_BUNDLE_BOUND:" + str(ref))

    return {
        "ok": True,
        "status": "WORKER_FRESHNESS_PASS",
        "verification_mode": "OFFLINE_HASH_BOUND_STARTMASTER_AUTHORITY",
        "head": head,
        "local_branch": branch,
        "startmaster": state["startmaster"],
        "step_id": state["next_allowed_step"],
        "sequence": int(gate["sequence"]),
        "state_sha256": sha256(statep),
        "bundle_sha256": sha256(bundlep),
        "chat_execution_authority": "NONE",
        "chat_output_authority": "NONE",
        "network_required": False,
        "publish_allowed": False,
    }


def main() -> int:
    try:
        print(json.dumps(validate(), ensure_ascii=False, indent=2))
        return 0
    except Blocked as exc:
        print(json.dumps({"ok": False, "status": "WORKER_FRESHNESS_BLOCKED", "reason": str(exc)}, ensure_ascii=False, indent=2))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
