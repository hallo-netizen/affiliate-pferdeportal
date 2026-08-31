#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
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


def current_main_head() -> tuple[str, str]:
    head = git("rev-parse", "HEAD")
    raw = git("ls-remote", "origin", "refs/heads/main")
    parts = raw.split()
    if not parts:
        raise Blocked("REMOTE_MAIN_UNVERIFIABLE")
    main = parts[0]
    if head != main:
        raise Blocked("STALE_WORKER_HEAD")
    return head, main


def validate() -> dict:
    head, main = current_main_head()
    if not POINTER.is_file():
        raise Blocked("STARTMASTER_POINTER_MISSING")
    ptr = load(POINTER)
    if ptr.get("free_chat_execution_authority") is not False:
        raise Blocked("FREE_CHAT_AUTHORITY_MUST_BE_FALSE")
    if ptr.get("hard_worker") != "CODEX_CLOUD":
        raise Blocked("HARD_WORKER_MUST_BE_CODEX_CLOUD")
    statep = REPO / rel(ptr.get("state_ref"))
    rootp = REPO / rel(ptr.get("root_ref"))
    if not statep.is_file() or not rootp.is_file():
        raise Blocked("ROOT_OR_STATE_MISSING")
    state = load(statep)
    root = load(rootp)
    if ptr.get("startmaster") != state.get("startmaster") or state.get("startmaster") != root.get("startmaster"):
        raise Blocked("STARTMASTER_IDENTITY_MISMATCH")
    if sha256(statep) != root.get("current_state_sha256"):
        raise Blocked("STATE_HASH_MISMATCH")
    if state.get("next_allowed_step") != (state.get("execution_gate") or {}).get("step_id"):
        raise Blocked("STEP_GATE_MISMATCH")
    bundle_ref = str((state.get("execution_gate") or {}).get("bundle_ref") or "")
    bundle_sha = str((state.get("execution_gate") or {}).get("bundle_sha256") or "")
    bundlep = REPO / rel(bundle_ref)
    if not bundlep.is_file() or sha256(bundlep) != bundle_sha:
        raise Blocked("BUNDLE_HASH_MISMATCH")
    bundle = load(bundlep)
    bindings = {str(row.get("ref") or ""): str(row.get("sha256") or "") for row in (bundle.get("authorized_inputs") or []) if isinstance(row, dict)}
    self_ref = "control/output-quarantine/worker_freshness_guard.py"
    if bindings.get(self_ref) != sha256(Path(__file__).resolve()):
        raise Blocked("FRESHNESS_GUARD_NOT_BUNDLE_BOUND")
    policy_ref = str(ptr.get("visible_output_policy_ref") or "")
    policy_sha = str(ptr.get("visible_output_policy_sha256") or "")
    policyp = REPO / rel(policy_ref)
    if not policyp.is_file() or sha256(policyp) != policy_sha:
        raise Blocked("OUTPUT_POLICY_HASH_MISMATCH")
    policy = load(policyp)
    if policy.get("chat_output_authority") != "NONE":
        raise Blocked("CHAT_OUTPUT_AUTHORITY_MUST_BE_NONE")
    if policy.get("domain_logic_authority") != "NONE" or policy.get("quality_authority") != "NONE":
        raise Blocked("FRESHNESS_GUARD_MUST_BE_DOMAIN_BLIND")
    return {
        "ok": True,
        "status": "WORKER_FRESHNESS_PASS",
        "head": head,
        "main": main,
        "startmaster": state["startmaster"],
        "step_id": state["next_allowed_step"],
        "sequence": int((state.get("execution_gate") or {})["sequence"]),
        "chat_output_authority": "NONE",
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
