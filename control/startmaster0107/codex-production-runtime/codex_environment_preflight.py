#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
import urllib.request
from pathlib import Path
from typing import Callable

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2] if len(HERE.parents) > 2 else HERE
PROOF_DIR = REPO / ".pferde-environment"
PROOF_PATH = PROOF_DIR / "CODEX_PRODUCTION_PREFLIGHT.json"
CONTRACT = "PFERDE_ATELIER_CODEX_PRODUCTION_ENVIRONMENT_PREFLIGHT_V1"
REPO_FULL_NAME = "hallo-netizen/affiliate-pferdeportal"
MAIN_API = f"https://api.github.com/repos/{REPO_FULL_NAME}/branches/main"
MAIN_TRACKING_REF = "refs/remotes/origin/main"
ALLOWED_STEPS = {
    ("RUN_NEW_ARTICLE_BATCH_NO_STOP", 107007),
    ("FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH", 107008),
}
PPM679_PACKAGE_REL = "control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip"
PPM679_PACKAGE_SHA256 = "acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1"
PSERC_FIX_PACKAGE_REL = "control/startmaster0107/runtime_packages/PSERC-FIX.zip"
PSERC_FIX_PACKAGE_SHA256 = "77a14aca97f46d60bc9001d66327abb68dd9cac9ad111f8ecefa1a8afd345314"


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


def authoritative_main_sha(repo: Path = REPO) -> tuple[str, str]:
    # The Codex setup/maintenance script refreshes this exact ref from GitHub
    # before every agent phase. Agent internet access is therefore unnecessary.
    try:
        value = git(repo, "rev-parse", "--verify", MAIN_TRACKING_REF)
        if len(value) == 40:
            return value, "CODEX_CHECKOUT_REMOTE_TRACKING_MAIN"
    except Exception:
        pass

    # Fallback for a fresh environment if the tracking ref was not materialized
    # but setup still has public internet. This is fail-closed on any error.
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
    raise PreflightBlocked("AUTHORITATIVE_MAIN_SHA_UNAVAILABLE")


def validate(
    repo: Path = REPO,
    *,
    main_sha_provider: Callable[[], tuple[str, str]] | None = None,
) -> dict:
    repo = Path(repo).resolve()
    head = git(repo, "rev-parse", "HEAD")
    expected_main, authority_source = (
        main_sha_provider() if main_sha_provider is not None else authoritative_main_sha(repo)
    )
    if head != expected_main:
        raise PreflightBlocked(
            "CODEX_CHECKOUT_NOT_CURRENT_MAIN:" + head + ":EXPECTED:" + expected_main
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

    ppm_package = repo / PPM679_PACKAGE_REL
    pserc_package = repo / PSERC_FIX_PACKAGE_REL
    if not ppm_package.is_file():
        raise PreflightBlocked("PPM679_PACKAGE_ZIP_MISSING")
    if sha256(ppm_package) != PPM679_PACKAGE_SHA256:
        raise PreflightBlocked("PPM679_PACKAGE_ZIP_HASH_MISMATCH")
    if not pserc_package.is_file():
        raise PreflightBlocked("PSERC_FIX_ZIP_MISSING")
    if sha256(pserc_package) != PSERC_FIX_PACKAGE_SHA256:
        raise PreflightBlocked("PSERC_FIX_ZIP_HASH_MISMATCH")

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
        "ppm679_package_ref": PPM679_PACKAGE_REL,
        "ppm679_package_sha256": PPM679_PACKAGE_SHA256,
        "pserc_fix_package_ref": PSERC_FIX_PACKAGE_REL,
        "pserc_fix_package_sha256": PSERC_FIX_PACKAGE_SHA256,
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
