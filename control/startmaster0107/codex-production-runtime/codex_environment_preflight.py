#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
import urllib.request
from pathlib import Path
from typing import Callable

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
POINTER = REPO / "control/CURRENT_STARTMASTER.json"
RUNTIME_STATE = REPO / "control/startmaster0107/runtime_inbox/RUNTIME_INBOX_STATE.json"
PROOF_DIR = REPO / ".pferde-environment"
PROOF_PATH = PROOF_DIR / "CODEX_PRODUCTION_PREFLIGHT.json"
CONTRACT = "PFERDE_ATELIER_CODEX_PRODUCTION_ENVIRONMENT_PREFLIGHT_V1"
REPO_FULL_NAME = "hallo-netizen/affiliate-pferdeportal"
MAIN_API = f"https://api.github.com/repos/{REPO_FULL_NAME}/branches/main"
ALLOWED_STEPS = {
    ("RUN_NEW_ARTICLE_BATCH_NO_STOP", 107007),
    ("FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH", 107008),
}


class PreflightBlocked(RuntimeError):
    pass


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(repo: Path, value: str) -> Path:
    p = Path(str(value or ""))
    if not value or p.is_absolute() or ".." in p.parts:
        raise PreflightBlocked("INVALID_RELATIVE_PATH")
    full = (repo / p).resolve()
    root = repo.resolve()
    if full != root and root not in full.parents:
        raise PreflightBlocked("RELATIVE_PATH_ESCAPE")
    return full


def git(repo: Path, *args: str) -> str:
    try:
        cp = subprocess.run(
            ["git", *args],
            cwd=repo,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except Exception as exc:
        raise PreflightBlocked("GIT_CHECK_FAILED:" + " ".join(args)) from exc
    return cp.stdout.strip()


def live_main_sha() -> tuple[str, str]:
    try:
        req = urllib.request.Request(
            MAIN_API,
            headers={
                "Accept": "application/vnd.github+json",
                "User-Agent": "pferde-atelier-codex-preflight",
            },
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = json.loads(resp.read().decode("utf-8"))
        value = str(((raw.get("commit") or {}).get("sha")) or "")
        if len(value) == 40:
            return value, "GITHUB_PUBLIC_BRANCH_API"
    except Exception:
        pass

    # Cached Codex containers may run maintenance without public internet.
    # Codex itself checks out the selected branch before maintenance; in that
    # case the remote-tracking main ref is the only accepted local fallback.
    try:
        value = git(REPO, "rev-parse", "--verify", "refs/remotes/origin/main")
        if len(value) == 40:
            return value, "CODEX_CHECKOUT_REMOTE_TRACKING_MAIN"
    except Exception:
        pass
    raise PreflightBlocked("AUTHORITATIVE_MAIN_SHA_UNAVAILABLE")


def ed25519_available() -> bool:
    try:
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey  # noqa: F401
    except Exception as exc:
        raise PreflightBlocked("ED25519_RUNTIME_UNAVAILABLE") from exc
    return True


def validate(
    repo: Path = REPO,
    *,
    main_sha_provider: Callable[[], tuple[str, str]] | None = None,
    ed25519_provider: Callable[[], bool] | None = None,
) -> dict:
    repo = Path(repo).resolve()
    head = git(repo, "rev-parse", "HEAD")
    expected_main, authority_source = (main_sha_provider or live_main_sha)()
    if head != expected_main:
        raise PreflightBlocked(
            "CODEX_CHECKOUT_NOT_CURRENT_MAIN:"
            + head
            + ":EXPECTED:"
            + expected_main
        )

    pointer_path = repo / "control/CURRENT_STARTMASTER.json"
    if not pointer_path.is_file():
        raise PreflightBlocked("STARTMASTER_POINTER_MISSING")
    ptr = load(pointer_path)
    if ptr.get("contract") != "PFERDE_ATELIER_CURRENT_STARTMASTER_POINTER_V2":
        raise PreflightBlocked("STARTMASTER_POINTER_CONTRACT_INVALID")
    if ptr.get("startmaster") != "STARTMASTER0107":
        raise PreflightBlocked("STARTMASTER_NOT_0107")
    if ptr.get("free_chat_execution_authority") is not False:
        raise PreflightBlocked("FREE_CHAT_EXECUTION_MUST_BE_FALSE")
    if ptr.get("chat_project_result_authority") != "NONE":
        raise PreflightBlocked("CHAT_PROJECT_RESULT_AUTHORITY_MUST_BE_NONE")
    if ptr.get("hard_worker") != "CODEX_CLOUD":
        raise PreflightBlocked("HARD_WORKER_MUST_BE_CODEX_CLOUD")
    if ptr.get("visible_output_authority") != "RELEASE_RECEIPT_ONLY":
        raise PreflightBlocked("VISIBLE_OUTPUT_AUTHORITY_INVALID")

    rootp = rel(repo, ptr.get("root_ref"))
    statep = rel(repo, ptr.get("state_ref"))
    policyp = rel(repo, ptr.get("visible_output_policy_ref"))
    runtime_entryp = rel(repo, ptr.get("execution_entrance_gate_ref"))
    for path in (rootp, statep, policyp, runtime_entryp):
        if not path.is_file():
            raise PreflightBlocked("AUTHORITY_FILE_MISSING:" + str(path.relative_to(repo)))

    root = load(rootp)
    state = load(statep)
    policy = load(policyp)
    if root.get("startmaster") != "STARTMASTER0107" or state.get("startmaster") != "STARTMASTER0107":
        raise PreflightBlocked("STARTMASTER_IDENTITY_MISMATCH")
    if sha256(statep) != root.get("current_state_sha256"):
        raise PreflightBlocked("STATE_HASH_MISMATCH")
    if root.get("next_allowed_step") != state.get("next_allowed_step"):
        raise PreflightBlocked("ROOT_STATE_STEP_MISMATCH")
    if sha256(policyp) != ptr.get("visible_output_policy_sha256"):
        raise PreflightBlocked("OUTPUT_POLICY_HASH_MISMATCH")
    if sha256(runtime_entryp) != ptr.get("execution_entrance_gate_sha256"):
        raise PreflightBlocked("RUNTIME_ENTRY_HASH_MISMATCH")

    if policy.get("chat_execution_authority") != "NONE" or policy.get("chat_output_authority") != "NONE":
        raise PreflightBlocked("CHAT_AUTHORITY_MUST_BE_NONE")
    for key in (
        "domain_logic_authority",
        "content_semantics_authority",
        "quality_authority",
        "design_authority",
        "seo_authority",
    ):
        if policy.get(key) != "NONE":
            raise PreflightBlocked("POLICY_MUST_BE_DOMAIN_BLIND:" + key)
    if policy.get("publish_allowed") is not False:
        raise PreflightBlocked("PUBLISH_MUST_BE_FALSE")

    gate = state.get("execution_gate") or {}
    step_id = str(state.get("next_allowed_step") or "")
    sequence = int(gate.get("sequence", -1))
    if gate.get("step_id") != step_id:
        raise PreflightBlocked("STEP_GATE_MISMATCH")
    if (step_id, sequence) not in ALLOWED_STEPS:
        raise PreflightBlocked("CODEX_PRODUCTION_STEP_NOT_ALLOWED")
    if gate.get("domain_logic_authority") != "NONE":
        raise PreflightBlocked("DOMAIN_LOGIC_AUTHORITY_MUST_BE_NONE")
    if gate.get("content_quality_design_authority") != "NONE":
        raise PreflightBlocked("CONTENT_QUALITY_DESIGN_AUTHORITY_MUST_BE_NONE")
    if gate.get("hard_worker_target") != "CODEX_CLOUD":
        raise PreflightBlocked("HARD_WORKER_TARGET_INVALID")

    bundlep = rel(repo, gate.get("bundle_ref"))
    if not bundlep.is_file() or sha256(bundlep) != gate.get("bundle_sha256"):
        raise PreflightBlocked("BUNDLE_HASH_MISMATCH")

    runtimep = repo / "control/startmaster0107/runtime_inbox/RUNTIME_INBOX_STATE.json"
    if not runtimep.is_file():
        raise PreflightBlocked("RUNTIME_INBOX_STATE_MISSING")
    runtime = load(runtimep)
    if runtime.get("contract") != "PFERDE_ATELIER_RUNTIME_BATCH_SLOT_STATE_V1":
        raise PreflightBlocked("RUNTIME_CONTRACT_INVALID")
    if runtime.get("status") != "EXECUTION_READY":
        raise PreflightBlocked("RUNTIME_NOT_EXECUTION_READY")
    if runtime.get("publish_allowed") is not False:
        raise PreflightBlocked("RUNTIME_PUBLISH_MUST_BE_FALSE")
    package_ref = str(runtime.get("production_package_ref") or "")
    package_sha = str(runtime.get("production_package_sha256") or "")
    packagep = rel(repo, package_ref)
    if not packagep.is_file():
        raise PreflightBlocked("PRODUCTION_PACKAGE_MISSING")
    if len(package_sha) != 64 or sha256(packagep) != package_sha:
        raise PreflightBlocked("PRODUCTION_PACKAGE_HASH_MISMATCH")

    if (ed25519_provider or ed25519_available)() is not True:
        raise PreflightBlocked("ED25519_RUNTIME_UNAVAILABLE")

    return {
        "contract": CONTRACT,
        "status": "CODEX_PRODUCTION_PREFLIGHT_PASS",
        "repository": REPO_FULL_NAME,
        "main_authority_source": authority_source,
        "expected_main_sha": expected_main,
        "local_head_sha": head,
        "startmaster": "STARTMASTER0107",
        "step_id": step_id,
        "sequence": sequence,
        "runtime_status": "EXECUTION_READY",
        "generation": int(runtime.get("generation") or 0),
        "batch_sha256": str(runtime.get("batch_sha256") or ""),
        "production_package_ref": package_ref,
        "production_package_sha256": package_sha,
        "state_sha256": sha256(statep),
        "bundle_sha256": sha256(bundlep),
        "ed25519_runtime": True,
        "chat_execution_authority": "NONE",
        "chat_output_authority": "NONE",
        "domain_logic_authority": "NONE",
        "quality_authority": "NONE",
        "content_semantics_inspected": False,
        "workflow_navigation_decision": False,
        "publish_allowed": False,
    }


def write_proof(repo: Path, proof: dict) -> Path:
    target = Path(repo).resolve() / ".pferde-environment/CODEX_PRODUCTION_PREFLIGHT.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(proof, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(target)
    return target


def main() -> int:
    try:
        proof = validate(REPO)
        path = write_proof(REPO, proof)
        print(
            json.dumps(
                {
                    "ok": True,
                    "status": proof["status"],
                    "proof": str(path.relative_to(REPO)),
                    "expected_main_sha": proof["expected_main_sha"],
                    "local_head_sha": proof["local_head_sha"],
                    "runtime_status": proof["runtime_status"],
                    "content_semantics_inspected": False,
                    "quality_authority": "NONE",
                    "publish_allowed": False,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0
    except Exception as exc:
        print(
            json.dumps(
                {
                    "ok": False,
                    "status": "CODEX_PRODUCTION_PREFLIGHT_BLOCKED",
                    "reason": str(exc),
                    "content_semantics_inspected": False,
                    "quality_authority": "NONE",
                    "publish_allowed": False,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
