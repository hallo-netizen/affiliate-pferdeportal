#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
POINTER = REPO / "control/CURRENT_STARTMASTER.json"
RUNTIME_STATE = REPO / "control/startmaster0107/runtime_inbox/RUNTIME_INBOX_STATE.json"
ENV_PROOF = REPO / ".pferde-environment/CODEX_PRODUCTION_PREFLIGHT.json"
PREFLIGHT_CONTRACT = "PFERDE_ATELIER_CODEX_PRODUCTION_ENVIRONMENT_PREFLIGHT_V1"
EXPECTED_REPOSITORY = "hallo-netizen/affiliate-pferdeportal"


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
    # NETWORKLESS_AGENT_RUNTIME: no network call during the agent phase.
    # Freshness is proven exclusively via the local checkout (rev-parse HEAD,
    # no remote contact) plus the environment proof that the Codex
    # setup/maintenance script already produced *before* the agent phase
    # started (control/startmaster0107/codex-production-runtime/
    # codex_environment_preflight.py). This is the same proof artifact and
    # the same field contract that worker_freshness_guard.py already relies
    # on for the identical guarantee; no new architecture is introduced here.
    head = git("rev-parse", "HEAD")
    if not ENV_PROOF.is_file():
        raise Blocked("CODEX_PRODUCTION_ENVIRONMENT_PROOF_MISSING")
    proof = load(ENV_PROOF)
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
    return head


def authority():
    if not POINTER.is_file():
        raise Blocked("STARTMASTER_POINTER_MISSING")
    ptr = load(POINTER)
    if ptr.get("free_chat_execution_authority") is not False:
        raise Blocked("FREE_CHAT_EXECUTION_MUST_BE_FALSE")
    if ptr.get("visible_output_authority") != "RELEASE_RECEIPT_ONLY":
        raise Blocked("VISIBLE_OUTPUT_AUTHORITY_INVALID")

    statep = REPO / rel(ptr.get("state_ref"))
    rootp = REPO / rel(ptr.get("root_ref"))
    policyp = REPO / rel(ptr.get("visible_output_policy_ref"))
    if not all(p.is_file() for p in (statep, rootp, policyp)):
        raise Blocked("AUTHORITY_FILE_MISSING")

    state, root, policy = load(statep), load(rootp), load(policyp)
    if ptr.get("startmaster") != state.get("startmaster") or state.get("startmaster") != root.get("startmaster"):
        raise Blocked("STARTMASTER_IDENTITY_MISMATCH")
    state_hash = sha256(statep)
    if state_hash != root.get("current_state_sha256"):
        raise Blocked("STATE_HASH_MISMATCH")
    if sha256(policyp) != ptr.get("visible_output_policy_sha256"):
        raise Blocked("OUTPUT_POLICY_HASH_MISMATCH")
    if policy.get("chat_execution_authority") != "NONE" or policy.get("chat_output_authority") != "NONE":
        raise Blocked("CHAT_AUTHORITY_MUST_BE_NONE")
    if policy.get("domain_logic_authority") != "NONE" or policy.get("quality_authority") != "NONE":
        raise Blocked("OUTPUT_GATE_MUST_BE_DOMAIN_BLIND")

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
    self_ref = "control/output-quarantine/output_release_gate.py"
    policy_ref = str(ptr.get("visible_output_policy_ref") or "")
    if bindings.get(self_ref) != sha256(Path(__file__).resolve()):
        raise Blocked("OUTPUT_GATE_NOT_BUNDLE_BOUND")
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


def validate_generic_receipt(ticket_path: Path, receipt_path: Path, expected_ticket: dict, policy: dict) -> tuple[dict, dict]:
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
    if not isinstance(receipt.get("payload"), dict):
        raise Blocked("RECEIPT_PAYLOAD_INVALID")
    return ticket, receipt


def verify_quarantine_outputs(policy, outputs):
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


def prepare_107007(ticket_path: Path, receipt_path: Path) -> dict:
    main_head = require_current_main()
    _, state, gate, policy, expected_ticket = authority()
    if expected_ticket.get("step_id") != "RUN_NEW_ARTICLE_BATCH_NO_STOP" or int(expected_ticket.get("sequence", -1)) != 107007:
        raise Blocked("PREPARE_RELEASE_ONLY_ALLOWED_FOR_107007")
    ticket, receipt = validate_generic_receipt(ticket_path, receipt_path, expected_ticket, policy)

    payload = receipt["payload"]
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
    verified = verify_quarantine_outputs(policy, outputs)

    staging_root = REPO / ".pferde-release-staging" / batch_sha / ticket["ticket_id"]
    staging_root.mkdir(parents=True, exist_ok=True)
    staged = []
    for source_ref, src, digest in verified:
        dst = staging_root / src.name
        if dst.exists() and sha256(dst) != digest:
            raise Blocked("STAGING_DESTINATION_COLLISION:" + dst.name)
        if not dst.exists():
            shutil.copyfile(src, dst)
        if sha256(dst) != digest:
            raise Blocked("STAGING_COPY_HASH_MISMATCH:" + dst.name)
        staged.append({"source_ref": source_ref, "staged_ref": str(dst.relative_to(REPO)), "sha256": digest})

    prepared = {
        "contract": "PFERDE_ATELIER_PREPARED_OUTPUT_RELEASE_V1",
        "status": "PREPARED_NOT_VISIBLE",
        "startmaster": state["startmaster"],
        "source_step_id": ticket["step_id"],
        "source_sequence": ticket["sequence"],
        "source_ticket_id": ticket["ticket_id"],
        "source_state_sha256": ticket["state_sha256"],
        "source_bundle_sha256": ticket["bundle_sha256"],
        "batch_sha256": batch_sha,
        "worker_receipt_sha256": sha256(receipt_path),
        "main_head": main_head,
        "staged_outputs": staged,
        "chat_execution_authority": "NONE",
        "chat_output_authority": "NONE",
        "domain_logic_authority": "NONE",
        "quality_authority": "NONE",
        "publish_allowed": False,
    }
    prepared_path = staging_root / "PREPARED_RELEASE.json"
    prepared_path.write_text(json.dumps(prepared, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {
        "ok": True,
        "status": "OUTPUT_RELEASE_PREPARED_NOT_VISIBLE",
        "prepared_ref": str(prepared_path.relative_to(REPO)),
        "prepared_sha256": sha256(prepared_path),
        "batch_sha256": batch_sha,
        "publish_allowed": False,
    }


def validate_prepared(prepared_ref: str, prepared_sha256: str) -> tuple[Path, dict]:
    prepared_path = REPO / rel(prepared_ref)
    if not prepared_path.is_file() or sha256(prepared_path) != prepared_sha256:
        raise Blocked("PREPARED_RELEASE_HASH_MISMATCH")
    prepared = load(prepared_path)
    if prepared.get("contract") != "PFERDE_ATELIER_PREPARED_OUTPUT_RELEASE_V1":
        raise Blocked("PREPARED_RELEASE_CONTRACT_INVALID")
    if prepared.get("status") != "PREPARED_NOT_VISIBLE":
        raise Blocked("PREPARED_RELEASE_STATUS_INVALID")
    if prepared.get("source_step_id") != "RUN_NEW_ARTICLE_BATCH_NO_STOP" or int(prepared.get("source_sequence", -1)) != 107007:
        raise Blocked("PREPARED_RELEASE_SOURCE_STEP_INVALID")
    if prepared.get("publish_allowed") is not False:
        raise Blocked("AUTO_PUBLISH_FORBIDDEN")
    rows = prepared.get("staged_outputs")
    if not isinstance(rows, list) or not rows:
        raise Blocked("PREPARED_OUTPUTS_MISSING")
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"source_ref", "staged_ref", "sha256"}:
            raise Blocked("PREPARED_OUTPUT_ROW_INVALID")
        p = REPO / rel(row["staged_ref"])
        if not p.is_file() or sha256(p) != row["sha256"]:
            raise Blocked("STAGED_OUTPUT_HASH_MISMATCH:" + row["staged_ref"])
    return prepared_path, prepared


def authorize_final_107008(prepared_ref: str, prepared_sha256: str, ticket_path: Path, receipt_path: Path) -> dict:
    main_head = require_current_main()
    _, state, gate, policy, expected_ticket = authority()
    if expected_ticket.get("step_id") != "FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH" or int(expected_ticket.get("sequence", -1)) != 107008:
        raise Blocked("FINAL_AUTH_ONLY_ALLOWED_FOR_107008")
    ticket, receipt = validate_generic_receipt(ticket_path, receipt_path, expected_ticket, policy)
    prepared_path, prepared = validate_prepared(prepared_ref, prepared_sha256)
    payload = receipt["payload"]
    required = {
        "reviewed_prepared_release_only": True,
        "prepared_release_ref": prepared_ref,
        "prepared_release_sha256": prepared_sha256,
        "prepared_batch_sha256": prepared["batch_sha256"],
    }
    for key, expected in required.items():
        if payload.get(key) != expected:
            raise Blocked("FINAL_REVIEW_PREPARED_BINDING_MISMATCH:" + key)

    auth = {
        "contract": "PFERDE_ATELIER_FINAL_OUTPUT_RELEASE_AUTH_V1",
        "status": "FINAL_REVIEW_PASS_AUTHORIZED_NOT_VISIBLE",
        "prepared_ref": prepared_ref,
        "prepared_sha256": prepared_sha256,
        "batch_sha256": prepared["batch_sha256"],
        "final_review_step_id": ticket["step_id"],
        "final_review_sequence": ticket["sequence"],
        "final_review_ticket_id": ticket["ticket_id"],
        "final_review_state_sha256": ticket["state_sha256"],
        "final_review_bundle_sha256": ticket["bundle_sha256"],
        "final_review_receipt_sha256": sha256(receipt_path),
        "main_head": main_head,
        "chat_execution_authority": "NONE",
        "chat_output_authority": "NONE",
        "domain_logic_authority": "NONE",
        "quality_authority": "NONE",
        "publish_allowed": False,
    }
    auth_path = prepared_path.parent / "FINAL_REVIEW_RELEASE_AUTH.json"
    auth_path.write_text(json.dumps(auth, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {
        "ok": True,
        "status": "FINAL_OUTPUT_RELEASE_AUTHORIZED_NOT_VISIBLE",
        "auth_ref": str(auth_path.relative_to(REPO)),
        "auth_sha256": sha256(auth_path),
        "batch_sha256": prepared["batch_sha256"],
        "publish_allowed": False,
    }


def commit_after_rearm(prepared_ref: str, prepared_sha256: str, auth_ref: str, auth_sha256: str) -> dict:
    main_head = require_current_main()
    prepared_path, prepared = validate_prepared(prepared_ref, prepared_sha256)
    auth_path = REPO / rel(auth_ref)
    if not auth_path.is_file() or sha256(auth_path) != auth_sha256:
        raise Blocked("FINAL_AUTH_HASH_MISMATCH")
    auth = load(auth_path)
    if auth.get("contract") != "PFERDE_ATELIER_FINAL_OUTPUT_RELEASE_AUTH_V1":
        raise Blocked("FINAL_AUTH_CONTRACT_INVALID")
    if auth.get("status") != "FINAL_REVIEW_PASS_AUTHORIZED_NOT_VISIBLE":
        raise Blocked("FINAL_AUTH_STATUS_INVALID")
    if auth.get("prepared_ref") != prepared_ref or auth.get("prepared_sha256") != prepared_sha256:
        raise Blocked("FINAL_AUTH_PREPARED_MISMATCH")
    if auth.get("batch_sha256") != prepared.get("batch_sha256"):
        raise Blocked("FINAL_AUTH_BATCH_MISMATCH")
    if auth.get("main_head") != main_head or prepared.get("main_head") != main_head:
        raise Blocked("MAIN_HEAD_CHANGED_DURING_BATCH")
    if auth.get("publish_allowed") is not False:
        raise Blocked("AUTO_PUBLISH_FORBIDDEN")

    ptr = load(POINTER)
    state = load(REPO / rel(ptr.get("state_ref")))
    runtime = load(RUNTIME_STATE)
    if state.get("next_allowed_step") != "RUN_NEW_ARTICLE_BATCH_NO_STOP" or int((state.get("execution_gate") or {}).get("sequence", -1)) != 107007:
        raise Blocked("VISIBLE_RELEASE_REQUIRES_SUCCESSFUL_107008_REARM")
    if runtime.get("status") != "NO_ACTIVE_BATCH" or runtime.get("publish_allowed") is not False:
        raise Blocked("VISIBLE_RELEASE_REQUIRES_IDLE_RUNTIME")

    policy = load(REPO / rel(ptr.get("visible_output_policy_ref")))
    release_root = REPO / rel(policy.get("visible_release_root"))
    destination = release_root / prepared["batch_sha256"]
    destination.mkdir(parents=True, exist_ok=True)

    released = []
    for row in prepared["staged_outputs"]:
        src = REPO / rel(row["staged_ref"])
        if not src.is_file() or sha256(src) != row["sha256"]:
            raise Blocked("STAGED_OUTPUT_HASH_MISMATCH:" + row["staged_ref"])
        dst = destination / src.name
        if dst.exists() and sha256(dst) != row["sha256"]:
            raise Blocked("VISIBLE_DESTINATION_COLLISION:" + dst.name)
        if not dst.exists():
            shutil.copyfile(src, dst)
        if sha256(dst) != row["sha256"]:
            raise Blocked("VISIBLE_COPY_HASH_MISMATCH:" + dst.name)
        released.append({"source_ref": row["source_ref"], "released_ref": str(dst.relative_to(REPO)), "sha256": row["sha256"]})

    release_receipt = {
        "contract": "PFERDE_ATELIER_OUTPUT_RELEASE_RECEIPT_V2",
        "status": "OUTPUT_RELEASE_PASS_FINAL_REVIEW_AND_REARM_CONFIRMED",
        "startmaster": prepared["startmaster"],
        "source_step_id": prepared["source_step_id"],
        "source_sequence": prepared["source_sequence"],
        "source_ticket_id": prepared["source_ticket_id"],
        "source_state_sha256": prepared["source_state_sha256"],
        "source_bundle_sha256": prepared["source_bundle_sha256"],
        "batch_sha256": prepared["batch_sha256"],
        "worker_receipt_sha256": prepared["worker_receipt_sha256"],
        "final_review_step_id": auth["final_review_step_id"],
        "final_review_sequence": auth["final_review_sequence"],
        "final_review_ticket_id": auth["final_review_ticket_id"],
        "final_review_receipt_sha256": auth["final_review_receipt_sha256"],
        "main_head": main_head,
        "outputs": released,
        "chat_execution_authority": "NONE",
        "chat_output_authority": "NONE",
        "domain_logic_authority": "NONE",
        "quality_authority": "NONE",
        "publish_allowed": False,
    }
    receipt_name = str(policy.get("release_receipt_name") or "RELEASE_RECEIPT.json")
    release_receipt_path = destination / receipt_name
    release_receipt_path.write_text(json.dumps(release_receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    durable_destination = REPO / "control/startmaster0107/durable_release_archive" / prepared["batch_sha256"]
    durable_destination.mkdir(parents=True, exist_ok=True)
    durable_outputs = []
    for row in released:
        src = REPO / rel(row["released_ref"])
        dst = durable_destination / src.name
        if dst.exists() and sha256(dst) != row["sha256"]:
            raise Blocked("DURABLE_DESTINATION_COLLISION:" + dst.name)
        if not dst.exists():
            shutil.copyfile(src, dst)
        if sha256(dst) != row["sha256"]:
            raise Blocked("DURABLE_COPY_HASH_MISMATCH:" + dst.name)
        durable_outputs.append({"source_ref": row["source_ref"], "released_ref": str(dst.relative_to(REPO)), "sha256": row["sha256"]})
    durable_receipt = dict(release_receipt)
    durable_receipt["outputs"] = durable_outputs
    durable_receipt_path = durable_destination / receipt_name
    durable_receipt_path.write_text(json.dumps(durable_receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    return {
        "ok": True,
        "status": "OUTPUT_RELEASE_PASS_FINAL",
        "release_receipt_ref": str(durable_receipt_path.relative_to(REPO)),
        "release_receipt_sha256": sha256(durable_receipt_path),
        "batch_sha256": prepared["batch_sha256"],
        "released_count": len(released),
        "publish_allowed": False,
    }


if __name__ == "__main__":
    raise SystemExit("DIRECT_CLI_DISABLED_USE_OFFICIAL_RUNTIME_ENTRY")
