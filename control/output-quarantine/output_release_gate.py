#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
POINTER = REPO / "control/CURRENT_STARTMASTER.json"
RUNTIME_STATE = REPO / "control/startmaster0107/runtime_inbox/RUNTIME_INBOX_STATE.json"


class Blocked(RuntimeError):
    pass


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def stable_hash(obj) -> str:
    raw = json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


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


def require_current_main() -> str:
    head = git("rev-parse", "HEAD")
    raw = git("ls-remote", "origin", "refs/heads/main")
    parts = raw.split()
    if not parts:
        raise Blocked("REMOTE_MAIN_UNVERIFIABLE")
    if head != parts[0]:
        raise Blocked("STALE_WORKER_HEAD")
    return head


def authority():
    if not POINTER.is_file():
        raise Blocked("STARTMASTER_POINTER_MISSING")
    ptr = load(POINTER)
    if ptr.get("free_chat_execution_authority") is not False:
        raise Blocked("FREE_CHAT_AUTHORITY_MUST_BE_FALSE")
    if ptr.get("visible_output_authority") != "RELEASE_RECEIPT_ONLY":
        raise Blocked("VISIBLE_OUTPUT_AUTHORITY_INVALID")
    statep = REPO / rel(ptr.get("state_ref"))
    rootp = REPO / rel(ptr.get("root_ref"))
    policyp = REPO / rel(ptr.get("visible_output_policy_ref"))
    if not statep.is_file() or not rootp.is_file() or not policyp.is_file():
        raise Blocked("AUTHORITY_FILE_MISSING")
    state, root, policy = load(statep), load(rootp), load(policyp)
    if ptr.get("startmaster") != state.get("startmaster") or state.get("startmaster") != root.get("startmaster"):
        raise Blocked("STARTMASTER_IDENTITY_MISMATCH")
    state_hash = sha256(statep)
    if state_hash != root.get("current_state_sha256"):
        raise Blocked("STATE_HASH_MISMATCH")
    if sha256(policyp) != ptr.get("visible_output_policy_sha256"):
        raise Blocked("OUTPUT_POLICY_HASH_MISMATCH")
    if policy.get("chat_output_authority") != "NONE":
        raise Blocked("CHAT_OUTPUT_AUTHORITY_MUST_BE_NONE")
    if policy.get("domain_logic_authority") != "NONE" or policy.get("quality_authority") != "NONE":
        raise Blocked("OUTPUT_GATE_MUST_BE_DOMAIN_BLIND")
    gate = state.get("execution_gate") or {}
    bundlep = REPO / rel(gate.get("bundle_ref"))
    if not bundlep.is_file() or sha256(bundlep) != gate.get("bundle_sha256"):
        raise Blocked("BUNDLE_HASH_MISMATCH")
    bundle = load(bundlep)
    bindings = {str(row.get("ref") or ""): str(row.get("sha256") or "") for row in (bundle.get("authorized_inputs") or []) if isinstance(row, dict)}
    self_ref = "control/output-quarantine/output_release_gate.py"
    if bindings.get(self_ref) != sha256(Path(__file__).resolve()):
        raise Blocked("OUTPUT_GATE_NOT_BUNDLE_BOUND")
    policy_ref = str(ptr.get("visible_output_policy_ref") or "")
    if bindings.get(policy_ref) != sha256(policyp):
        raise Blocked("OUTPUT_POLICY_NOT_BUNDLE_BOUND")
    ticket_body = {
        "contract": "PFERDE_ATELIER_EXECUTION_TICKET_V2",
        "startmaster": state["startmaster"],
        "step_id": state["next_allowed_step"],
        "sequence": int(gate["sequence"]),
        "state_sha256": state_hash,
        "bundle_sha256": gate["bundle_sha256"],
    }
    ticket_body["ticket_id"] = stable_hash(ticket_body)
    return ptr, state, gate, policy, ticket_body


def validate_receipt(ticket_path: Path, receipt_path: Path):
    _, state, gate, policy, expected_ticket = authority()
    if not ticket_path.is_file() or not receipt_path.is_file():
        raise Blocked("TICKET_OR_RECEIPT_MISSING")
    ticket = load(ticket_path)
    receipt = load(receipt_path)
    if ticket != expected_ticket:
        raise Blocked("TICKET_BINDING_MISMATCH")
    allowed = {
        "contract", "ticket_id", "step_id", "sequence", "state_sha256",
        "bundle_sha256", "status", "navigation_decision",
        "state_write_requested", "workflow_change_requested", "payload", "evidence"
    }
    if set(receipt) != allowed:
        raise Blocked("RECEIPT_FIELDS_INVALID")
    if receipt.get("contract") != policy.get("required_step_receipt_contract"):
        raise Blocked("RECEIPT_CONTRACT_INVALID")
    for key in ("ticket_id", "step_id", "sequence", "state_sha256", "bundle_sha256"):
        if receipt.get(key) != ticket.get(key):
            raise Blocked("RECEIPT_BINDING_MISMATCH:" + key)
    if receipt.get("status") != "PASS":
        raise Blocked("RECEIPT_NOT_PASS")
    if receipt.get("navigation_decision") is not False:
        raise Blocked("NAVIGATION_AUTHORITY_FORBIDDEN")
    if receipt.get("state_write_requested") is not False:
        raise Blocked("STATE_WRITE_AUTHORITY_FORBIDDEN")
    if receipt.get("workflow_change_requested") is not False:
        raise Blocked("WORKFLOW_CHANGE_AUTHORITY_FORBIDDEN")
    payload = receipt.get("payload")
    if not isinstance(payload, dict):
        raise Blocked("RECEIPT_PAYLOAD_INVALID")
    if payload.get("execution_origin") != policy.get("bound_worker_origin"):
        raise Blocked("UNBOUND_EXECUTION_ORIGIN")
    if payload.get("workflow_pass") is not True:
        raise Blocked("FULL_WORKFLOW_PASS_REQUIRED")
    if not RUNTIME_STATE.is_file():
        raise Blocked("RUNTIME_STATE_MISSING")
    runtime = load(RUNTIME_STATE)
    if runtime.get("publish_allowed") is not False:
        raise Blocked("AUTO_PUBLISH_FORBIDDEN")
    batch_sha = str(runtime.get("batch_sha256") or "")
    if len(batch_sha) != 64 or payload.get("batch_sha256") != batch_sha:
        raise Blocked("CURRENT_BATCH_BINDING_MISMATCH")
    outputs = payload.get("outputs")
    if not isinstance(outputs, list) or not outputs:
        raise Blocked("OUTPUT_BINDING_MISSING")
    return state, gate, policy, ticket, receipt, runtime, outputs


def verify_outputs(policy, outputs):
    quarantine_root = str(policy.get("worker_quarantine_root") or "")
    if not quarantine_root:
        raise Blocked("QUARANTINE_ROOT_INVALID")
    prefix = quarantine_root.rstrip("/") + "/"
    seen = set()
    verified = []
    for i, row in enumerate(outputs):
        if not isinstance(row, dict) or set(row) != {"ref", "sha256"}:
            raise Blocked("OUTPUT_ROW_INVALID:" + str(i))
        ref = str(row.get("ref") or "")
        if not ref.startswith(prefix):
            raise Blocked("OUTPUT_OUTSIDE_QUARANTINE:" + ref)
        if ref in seen:
            raise Blocked("DUPLICATE_OUTPUT_REF:" + ref)
        seen.add(ref)
        path = REPO / rel(ref)
        if not path.is_file():
            raise Blocked("OUTPUT_MISSING:" + ref)
        actual = sha256(path)
        if actual != row.get("sha256"):
            raise Blocked("OUTPUT_HASH_MISMATCH:" + ref)
        verified.append((ref, path, actual))
    return verified


def release(ticket_path: Path, receipt_path: Path):
    main_head = require_current_main()
    state, gate, policy, ticket, receipt, runtime, outputs = validate_receipt(ticket_path, receipt_path)
    verified = verify_outputs(policy, outputs)
    release_root = REPO / rel(policy.get("visible_release_root"))
    batch_sha = runtime["batch_sha256"]
    destination = release_root / batch_sha
    destination.mkdir(parents=True, exist_ok=True)
    released = []
    for source_ref, src, digest in verified:
        dst = destination / src.name
        if dst.exists():
            if sha256(dst) != digest:
                raise Blocked("RELEASE_DESTINATION_COLLISION:" + dst.name)
        else:
            shutil.copyfile(src, dst)
        if sha256(dst) != digest:
            raise Blocked("RELEASE_COPY_HASH_MISMATCH:" + dst.name)
        released.append({
            "source_ref": source_ref,
            "released_ref": str(dst.relative_to(REPO)),
            "sha256": digest,
        })
    release_receipt = {
        "contract": "PFERDE_ATELIER_OUTPUT_RELEASE_RECEIPT_V1",
        "status": "OUTPUT_RELEASE_PASS",
        "startmaster": state["startmaster"],
        "step_id": ticket["step_id"],
        "sequence": ticket["sequence"],
        "ticket_id": ticket["ticket_id"],
        "state_sha256": ticket["state_sha256"],
        "bundle_sha256": ticket["bundle_sha256"],
        "batch_sha256": batch_sha,
        "worker_receipt_sha256": sha256(receipt_path),
        "main_head": main_head,
        "outputs": released,
        "chat_output_authority": "NONE",
        "domain_logic_authority": "NONE",
        "quality_authority": "NONE",
        "publish_allowed": False,
    }
    receipt_name = str(policy.get("release_receipt_name") or "RELEASE_RECEIPT.json")
    release_receipt_path = destination / receipt_name
    release_receipt_path.write_text(json.dumps(release_receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {
        "ok": True,
        "status": "OUTPUT_RELEASE_PASS",
        "release_receipt_ref": str(release_receipt_path.relative_to(REPO)),
        "batch_sha256": batch_sha,
        "released_count": len(released),
        "publish_allowed": False,
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=["release"])
    ap.add_argument("ticket")
    ap.add_argument("receipt")
    args = ap.parse_args(argv)
    try:
        result = release(Path(args.ticket), Path(args.receipt))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except Blocked as exc:
        print(json.dumps({"ok": False, "status": "OUTPUT_RELEASE_BLOCKED", "reason": str(exc)}, ensure_ascii=False, indent=2))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
