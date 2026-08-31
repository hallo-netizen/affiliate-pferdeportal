#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
POINTER = REPO / "control/CURRENT_STARTMASTER.json"
CAPSULE = REPO / ".pferde-capsule"


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


def module(path: Path, name: str):
    if not path.is_file():
        raise Blocked("MODULE_MISSING:" + str(path))
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise Blocked("MODULE_LOAD_FAILED:" + str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def authority() -> tuple[dict, dict, dict, dict]:
    if not POINTER.is_file():
        raise Blocked("STARTMASTER_POINTER_MISSING")
    ptr = load(POINTER)
    if ptr.get("execution_entrance_gate_ref") != "control/output-quarantine/runtime_entry_gate.py":
        raise Blocked("OFFICIAL_RUNTIME_ENTRY_REF_INVALID")
    if ptr.get("execution_entrance_gate_sha256") != sha256(Path(__file__).resolve()):
        raise Blocked("OFFICIAL_RUNTIME_ENTRY_HASH_MISMATCH")
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
    if sha256(statep) != root.get("current_state_sha256"):
        raise Blocked("STATE_HASH_MISMATCH")
    if root.get("execution_entrance_gate") != ptr.get("execution_entrance_gate_ref"):
        raise Blocked("ROOT_RUNTIME_ENTRY_MISMATCH")
    if sha256(policyp) != ptr.get("visible_output_policy_sha256"):
        raise Blocked("OUTPUT_POLICY_HASH_MISMATCH")
    if policy.get("chat_execution_authority") != "NONE" or policy.get("chat_output_authority") != "NONE":
        raise Blocked("CHAT_AUTHORITY_MUST_BE_NONE")
    if policy.get("domain_logic_authority") != "NONE" or policy.get("quality_authority") != "NONE":
        raise Blocked("RUNTIME_ENTRY_MUST_BE_DOMAIN_BLIND")

    gate = state.get("execution_gate") or {}
    bundlep = REPO / rel(gate.get("bundle_ref"))
    if gate.get("step_id") != state.get("next_allowed_step"):
        raise Blocked("STEP_GATE_MISMATCH")
    if not bundlep.is_file() or sha256(bundlep) != gate.get("bundle_sha256"):
        raise Blocked("BUNDLE_HASH_MISMATCH")
    bundle = load(bundlep)
    bindings = {
        str(row.get("ref") or ""): str(row.get("sha256") or "")
        for row in (bundle.get("authorized_inputs") or [])
        if isinstance(row, dict)
    }
    required = {
        "control/output-quarantine/runtime_entry_gate.py": sha256(Path(__file__).resolve()),
        str(ptr.get("visible_output_policy_ref") or ""): sha256(policyp),
        "control/output-quarantine/worker_freshness_guard.py": sha256(REPO / "control/output-quarantine/worker_freshness_guard.py"),
        "control/output-quarantine/output_release_gate.py": sha256(REPO / "control/output-quarantine/output_release_gate.py"),
    }
    for ref, digest in required.items():
        if bindings.get(ref) != digest:
            raise Blocked("RUNTIME_SECURITY_INPUT_NOT_BUNDLE_BOUND:" + ref)
    return ptr, state, gate, policy


def write_capsule_json(name: str, obj: dict) -> Path:
    if not CAPSULE.is_dir():
        raise Blocked("CAPSULE_MISSING")
    path = CAPSULE / name
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    path.chmod(0o444)
    return path


def freshness() -> dict:
    guard = module(REPO / "control/output-quarantine/worker_freshness_guard.py", "output_worker_freshness")
    result = guard.validate()
    if result.get("status") != "WORKER_FRESHNESS_PASS":
        raise Blocked("WORKER_FRESHNESS_NOT_PASS")
    return result


def cloud():
    return module(REPO / "control/cloud-entry-gate/cloud_entry.py", "immutable_cloud_entry_delegate")


def start() -> dict:
    authority()
    proof = freshness()
    result = cloud().materialize()
    if not result.get("ok"):
        raise Blocked("IMMUTABLE_CLOUD_ENTRY_START_NOT_OK")
    write_capsule_json("FRESHNESS_PROOF.json", proof)
    return {
        "ok": True,
        "status": "OFFICIAL_RUNTIME_ENTRY_PASS",
        "freshness_status": proof["status"],
        "step_id": result.get("step_id"),
        "sequence": result.get("sequence"),
        "ticket_id": result.get("ticket_id"),
        "capsule": result.get("capsule"),
        "chat_execution_authority": "NONE",
        "chat_output_authority": "NONE",
        "publish_allowed": False,
        "next_action": "EXECUTE_ONLY_CAPSULE_INSTRUCTION",
    }


def validate_107008_receipt(receipt_path: Path, binding: dict) -> None:
    if not receipt_path.is_file():
        raise Blocked("RECEIPT_MISSING")
    receipt = load(receipt_path)
    if receipt.get("status") != "PASS":
        raise Blocked("FINAL_REVIEW_RECEIPT_NOT_PASS")
    payload = receipt.get("payload")
    if not isinstance(payload, dict):
        raise Blocked("FINAL_REVIEW_RECEIPT_PAYLOAD_INVALID")
    required = {
        "reviewed_prepared_release_only": True,
        "prepared_release_ref": binding["prepared_ref"],
        "prepared_release_sha256": binding["prepared_sha256"],
        "prepared_batch_sha256": binding["batch_sha256"],
    }
    for key, expected in required.items():
        if payload.get(key) != expected:
            raise Blocked("FINAL_REVIEW_PREPARED_BINDING_MISMATCH:" + key)


def complete(receipt_path: Path) -> dict:
    _, state, gate, _ = authority()
    seq = int(gate.get("sequence", -1))
    step = str(state.get("next_allowed_step") or "")
    c = cloud()
    release_gate = module(REPO / "control/output-quarantine/output_release_gate.py", "output_release_gate_delegate")

    if seq == 107007 and step == "RUN_NEW_ARTICLE_BATCH_NO_STOP":
        ticket_path = CAPSULE / "TICKET.json"
        if not ticket_path.is_file():
            raise Blocked("CAPSULE_TICKET_MISSING")
        prepared = release_gate.prepare_107007(ticket_path, receipt_path)
        if prepared.get("status") != "OUTPUT_RELEASE_PREPARED_NOT_VISIBLE":
            raise Blocked("OUTPUT_PREPARE_NOT_PASS")

        advanced = c.complete(receipt_path)
        if advanced.get("status") != "STATE_ADVANCED_NEXT_STEP_READY":
            raise Blocked("107007_COMPLETE_DID_NOT_ADVANCE")

        post_proof = freshness()
        binding = {
            "contract": "PFERDE_ATELIER_BOUND_PREPARED_RELEASE_FOR_FINAL_REVIEW_V1",
            "prepared_ref": prepared["prepared_ref"],
            "prepared_sha256": prepared["prepared_sha256"],
            "batch_sha256": prepared["batch_sha256"],
        }
        write_capsule_json("FRESHNESS_PROOF.json", post_proof)
        write_capsule_json("BOUND_PREPARED_RELEASE_REF.json", binding)
        return {
            "ok": True,
            "status": "107007_PASS_STAGED_NOT_VISIBLE_107008_READY",
            "prepared_ref": prepared["prepared_ref"],
            "prepared_sha256": prepared["prepared_sha256"],
            "batch_sha256": prepared["batch_sha256"],
            "next_step_id": advanced.get("next_step_id"),
            "next_sequence": advanced.get("next_sequence"),
            "chat_output_authority": "NONE",
            "visible_project_result": False,
            "publish_allowed": False,
        }

    if seq == 107008 and step == "FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH":
        binding_path = CAPSULE / "BOUND_PREPARED_RELEASE_REF.json"
        final_guard = module(REPO / "control/output-quarantine/final_review_visibility_guard.py", "final_review_visibility_delegate")
        final_guard.validate_binding(binding_path)
        binding = load(binding_path)
        validate_107008_receipt(receipt_path, binding)
        ticket_path = CAPSULE / "TICKET.json"
        auth = release_gate.authorize_final_107008(
            binding["prepared_ref"],
            binding["prepared_sha256"],
            ticket_path,
            receipt_path,
        )
        if auth.get("status") != "FINAL_OUTPUT_RELEASE_AUTHORIZED_NOT_VISIBLE":
            raise Blocked("FINAL_OUTPUT_AUTH_NOT_PASS")

        finished = c.complete(receipt_path)
        if finished.get("status") != "FINAL_STEP_PASS_REARMED":
            raise Blocked("107008_COMPLETE_DID_NOT_REARM")

        try:
            committed = release_gate.commit_after_rearm(
                binding["prepared_ref"],
                binding["prepared_sha256"],
                auth["auth_ref"],
                auth["auth_sha256"],
            )
        except Exception as exc:
            raise Blocked(
                "VISIBLE_RELEASE_COMMIT_FAILED_AFTER_SAFE_REARM:"
                + binding["prepared_ref"] + ":"
                + binding["prepared_sha256"] + ":"
                + auth["auth_ref"] + ":"
                + auth["auth_sha256"] + ":"
                + str(exc)
            ) from exc
        if committed.get("status") != "OUTPUT_RELEASE_PASS_FINAL":
            raise Blocked("FINAL_VISIBLE_RELEASE_NOT_PASS")
        return {
            "ok": True,
            "status": "107008_FINAL_REVIEW_PASS_VISIBLE_RELEASE_REARMED",
            "release_receipt_ref": committed["release_receipt_ref"],
            "release_receipt_sha256": committed["release_receipt_sha256"],
            "batch_sha256": committed["batch_sha256"],
            "released_count": committed["released_count"],
            "rearmed_step_id": finished.get("rearmed_step_id"),
            "rearmed_sequence": finished.get("rearmed_sequence"),
            "chat_output_authority": "NONE",
            "publish_allowed": False,
        }

    raise Blocked("OFFICIAL_RUNTIME_ENTRY_UNSUPPORTED_STEP")


def recover_final_release(prepared_ref: str, prepared_sha256: str, auth_ref: str, auth_sha256: str) -> dict:
    _, state, gate, _ = authority()
    if state.get("next_allowed_step") != "RUN_NEW_ARTICLE_BATCH_NO_STOP" or int(gate.get("sequence", -1)) != 107007:
        raise Blocked("RECOVER_FINAL_RELEASE_REQUIRES_REARMED_107007")
    release_gate = module(REPO / "control/output-quarantine/output_release_gate.py", "output_release_gate_recover")
    committed = release_gate.commit_after_rearm(prepared_ref, prepared_sha256, auth_ref, auth_sha256)
    return {
        "ok": True,
        "status": "FINAL_VISIBLE_RELEASE_RECOVERED",
        **committed,
    }


def main() -> int:
    try:
        cmd = sys.argv[1] if len(sys.argv) > 1 else "start"
        if cmd == "start":
            result = start()
        elif cmd == "complete":
            if len(sys.argv) != 3:
                raise Blocked("COMPLETE_REQUIRES_RECEIPT_PATH")
            result = complete(Path(sys.argv[2]))
        elif cmd == "recover-final-release":
            if len(sys.argv) != 6:
                raise Blocked("RECOVER_FINAL_RELEASE_REQUIRES_PREPARED_REF_SHA_AUTH_REF_SHA")
            result = recover_final_release(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
        else:
            raise Blocked("UNKNOWN_COMMAND")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        print(json.dumps({"ok": False, "status": "OFFICIAL_RUNTIME_ENTRY_BLOCKED", "reason": str(exc)}, ensure_ascii=False, indent=2))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
