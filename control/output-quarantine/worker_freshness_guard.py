#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
POINTER = REPO / "control/CURRENT_STARTMASTER.json"
ENV_PROOF = REPO / ".pferde-environment/CODEX_PRODUCTION_PREFLIGHT.json"
PREFLIGHT_CONTRACT = "PFERDE_ATELIER_CODEX_PRODUCTION_ENVIRONMENT_PREFLIGHT_V1"
EXPECTED_REPOSITORY = "hallo-netizen/affiliate-pferdeportal"
EXPECTED_GATE_DIRTY_107008 = {
    "control/startmaster0107/CURRENT_STATE.json",
    "control/startmaster0107/PFERDE_ATELIER_START_HERE.json",
}


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


def tracked_dirty_paths() -> set[str]:
    try:
        cp = subprocess.run(
            ["git", "status", "--porcelain", "--untracked-files=no"],
            cwd=REPO,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except Exception as exc:
        raise Blocked("GIT_CHECK_FAILED:status --porcelain --untracked-files=no") from exc
    raw = cp.stdout
    paths: set[str] = set()
    for line in raw.splitlines():
        if len(line) < 4:
            continue
        value = line[3:].strip()
        if " -> " in value:
            value = value.split(" -> ", 1)[1]
        if value:
            paths.add(value)
    return paths


def local_checkout_identity() -> tuple[str, str, set[str]]:
    return git("rev-parse", "HEAD"), git("branch", "--show-current"), tracked_dirty_paths()


def validate_environment_proof(
    proof: dict,
    *,
    head: str,
    state: dict,
    statep: Path,
    bundlep: Path,
    runtime: dict,
) -> None:
    if proof.get("contract") != PREFLIGHT_CONTRACT:
        raise Blocked("CODEX_ENVIRONMENT_PROOF_CONTRACT_INVALID")
    if proof.get("status") != "CODEX_PRODUCTION_PREFLIGHT_PASS":
        raise Blocked("CODEX_ENVIRONMENT_PREFLIGHT_NOT_PASS")
    if proof.get("repository") != EXPECTED_REPOSITORY:
        raise Blocked("CODEX_ENVIRONMENT_REPOSITORY_INVALID")
    if proof.get("main_authority_source") not in {
        "GITHUB_PUBLIC_BRANCH_API",
        "CODEX_CHECKOUT_REMOTE_TRACKING_MAIN",
    }:
        raise Blocked("CODEX_MAIN_AUTHORITY_SOURCE_INVALID")
    if proof.get("expected_main_sha") != head or proof.get("local_head_sha") != head:
        raise Blocked("CODEX_CHECKOUT_NOT_PROVEN_CURRENT_MAIN")
    if proof.get("ed25519_runtime") is not True:
        raise Blocked("ED25519_RUNTIME_NOT_PROVEN")
    if proof.get("chat_execution_authority") != "NONE" or proof.get("chat_output_authority") != "NONE":
        raise Blocked("CODEX_ENVIRONMENT_CHAT_AUTHORITY_INVALID")
    if proof.get("domain_logic_authority") != "NONE" or proof.get("quality_authority") != "NONE":
        raise Blocked("CODEX_ENVIRONMENT_MUST_BE_DOMAIN_BLIND")
    if proof.get("content_semantics_inspected") is not False:
        raise Blocked("CODEX_ENVIRONMENT_CONTENT_INSPECTION_FORBIDDEN")
    if proof.get("workflow_navigation_decision") is not False:
        raise Blocked("CODEX_ENVIRONMENT_NAVIGATION_DECISION_FORBIDDEN")
    if proof.get("publish_allowed") is not False:
        raise Blocked("CODEX_ENVIRONMENT_PUBLISH_MUST_BE_FALSE")

    if runtime.get("status") != "EXECUTION_READY":
        raise Blocked("RUNTIME_NOT_EXECUTION_READY")
    if proof.get("runtime_status") != "EXECUTION_READY":
        raise Blocked("CODEX_ENVIRONMENT_RUNTIME_NOT_EXECUTION_READY")
    if proof.get("generation") != runtime.get("generation"):
        raise Blocked("CODEX_ENVIRONMENT_GENERATION_MISMATCH")
    if proof.get("batch_sha256") != runtime.get("batch_sha256"):
        raise Blocked("CODEX_ENVIRONMENT_BATCH_MISMATCH")
    if proof.get("production_package_ref") != runtime.get("production_package_ref"):
        raise Blocked("CODEX_ENVIRONMENT_PACKAGE_REF_MISMATCH")
    if proof.get("production_package_sha256") != runtime.get("production_package_sha256"):
        raise Blocked("CODEX_ENVIRONMENT_PACKAGE_HASH_MISMATCH")

    current_step = str(state.get("next_allowed_step") or "")
    current_seq = int((state.get("execution_gate") or {}).get("sequence", -1))
    proof_step = str(proof.get("step_id") or "")
    proof_seq = int(proof.get("sequence", -1))
    exact_same_step = proof_step == current_step and proof_seq == current_seq
    exact_bound_progression = (
        proof_step == "RUN_NEW_ARTICLE_BATCH_NO_STOP"
        and proof_seq == 107007
        and current_step == "FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH"
        and current_seq == 107008
    )
    if not exact_same_step and not exact_bound_progression:
        raise Blocked("CODEX_ENVIRONMENT_STEP_PROOF_NOT_CURRENT_OR_PREBOUND_NEXT")
    if exact_same_step:
        if proof.get("state_sha256") != sha256(statep):
            raise Blocked("CODEX_ENVIRONMENT_STATE_HASH_MISMATCH")
        if proof.get("bundle_sha256") != sha256(bundlep):
            raise Blocked("CODEX_ENVIRONMENT_BUNDLE_HASH_MISMATCH")


def validate() -> dict:
    head, branch, dirty = local_checkout_identity()
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
    runtimep = REPO / "control/startmaster0107/runtime_inbox/RUNTIME_INBOX_STATE.json"
    if not all(p.is_file() for p in (statep, rootp, policyp, runtime_entryp, runtimep)):
        raise Blocked("AUTHORITY_FILE_MISSING")

    state = load(statep)
    root = load(rootp)
    policy = load(policyp)
    runtime = load(runtimep)
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

    gate = state.get("execution_gate") or {}
    if gate.get("step_id") != state.get("next_allowed_step"):
        raise Blocked("STEP_GATE_MISMATCH")
    sequence = int(gate.get("sequence", -1))
    step_id = str(state.get("next_allowed_step") or "")
    if (step_id, sequence) not in {
        ("RUN_NEW_ARTICLE_BATCH_NO_STOP", 107007),
        ("FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH", 107008),
    }:
        raise Blocked("CODEX_PRODUCTION_STEP_NOT_ALLOWED")

    if sequence == 107007:
        if dirty:
            raise Blocked("TRACKED_WORKTREE_NOT_CLEAN")
    else:
        unexpected = dirty - EXPECTED_GATE_DIRTY_107008
        if unexpected:
            raise Blocked("UNEXPECTED_TRACKED_DIRTY_PATH:" + sorted(unexpected)[0])
        if dirty and not dirty.issubset(EXPECTED_GATE_DIRTY_107008):
            raise Blocked("TRACKED_DIRTY_PATH_SET_INVALID")

    bundlep = REPO / rel(gate.get("bundle_ref"))
    if not bundlep.is_file() or sha256(bundlep) != gate.get("bundle_sha256"):
        raise Blocked("BUNDLE_HASH_MISMATCH")
    bundle = load(bundlep)
    bindings = {
        str(row.get("ref") or ""): str(row.get("sha256") or "")
        for row in (bundle.get("authorized_inputs") or [])
        if isinstance(row, dict)
    }
    preflightp = REPO / "control/startmaster0107/codex-production-runtime/codex_environment_preflight.py"
    required = {
        "control/output-quarantine/worker_freshness_guard.py": sha256(Path(__file__).resolve()),
        "control/output-quarantine/OUTPUT_VISIBILITY_POLICY.json": sha256(policyp),
        ptr.get("execution_entrance_gate_ref"): sha256(runtime_entryp),
        "control/startmaster0107/codex-production-runtime/codex_environment_preflight.py": sha256(preflightp),
    }
    for ref, digest in required.items():
        if bindings.get(ref) != digest:
            raise Blocked("REQUIRED_SECURITY_INPUT_NOT_BUNDLE_BOUND:" + str(ref))

    if not ENV_PROOF.is_file():
        raise Blocked("CODEX_PRODUCTION_ENVIRONMENT_PROOF_MISSING")
    proof = load(ENV_PROOF)
    validate_environment_proof(
        proof,
        head=head,
        state=state,
        statep=statep,
        bundlep=bundlep,
        runtime=runtime,
    )

    package_ref = str(runtime.get("production_package_ref") or "")
    package_sha = str(runtime.get("production_package_sha256") or "")
    packagep = REPO / rel(package_ref)
    if runtime.get("contract") != "PFERDE_ATELIER_RUNTIME_BATCH_SLOT_STATE_V1":
        raise Blocked("RUNTIME_CONTRACT_INVALID")
    if runtime.get("status") != "EXECUTION_READY":
        raise Blocked("RUNTIME_NOT_EXECUTION_READY")
    if runtime.get("publish_allowed") is not False:
        raise Blocked("RUNTIME_PUBLISH_MUST_BE_FALSE")
    if not packagep.is_file() or len(package_sha) != 64 or sha256(packagep) != package_sha:
        raise Blocked("RUNTIME_PRODUCTION_PACKAGE_HASH_MISMATCH")

    return {
        "ok": True,
        "status": "WORKER_FRESHNESS_PASS",
        "verification_mode": "EXACT_CURRENT_MAIN_ENVIRONMENT_PROOF_PLUS_HASH_BOUND_STARTMASTER",
        "head": head,
        "local_branch": branch,
        "tracked_dirty_paths": sorted(dirty),
        "startmaster": state["startmaster"],
        "step_id": step_id,
        "sequence": sequence,
        "state_sha256": sha256(statep),
        "bundle_sha256": sha256(bundlep),
        "environment_proof_status": proof["status"],
        "runtime_status": runtime["status"],
        "chat_execution_authority": "NONE",
        "chat_output_authority": "NONE",
        "content_semantics_inspected": False,
        "domain_logic_authority": "NONE",
        "quality_authority": "NONE",
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
