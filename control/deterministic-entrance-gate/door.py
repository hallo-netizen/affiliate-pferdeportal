#!/usr/bin/env python3
"""Deterministic Entrance Gate V1.

Pure technical routing layer. It has no domain/content/quality/design logic.
It validates one bound current step, issues an isolated execution capsule,
and validates an opaque receipt for exactly that ticket.
"""
from __future__ import annotations
import argparse, hashlib, json, os, secrets, shutil, sys, time
from pathlib import Path

class GateBlocked(RuntimeError):
    pass

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def stable_json_bytes(obj) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")

def stable_hash(obj) -> str:
    return sha256_bytes(stable_json_bytes(obj))

def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def norm(value) -> str:
    return str(value or "").strip()

def require_relpath(value: str) -> str:
    p = Path(value)
    if not value or p.is_absolute() or ".." in p.parts:
        raise GateBlocked("NON_RELATIVE_PATH_REJECTED")
    return p.as_posix()

def safe_master_path(master: Path, rel: str) -> Path:
    rel = require_relpath(rel)
    root = master.resolve()
    target = (master / rel).resolve()
    if target != root and root not in target.parents:
        raise GateBlocked("PATH_ESCAPES_MASTER")
    return target

def load_authority(master: Path):
    root_path = master / "PFERDE_ATELIER_START_HERE.json"
    if not root_path.is_file():
        raise GateBlocked("ROOT_MISSING")
    root = read_json(root_path)
    state_rel = require_relpath(norm(root.get("navigation_authority")))
    state_path = safe_master_path(master, state_rel)
    if not state_path.is_file():
        raise GateBlocked("CURRENT_STATE_MISSING")
    state_raw = state_path.read_bytes()
    state_hash = sha256_bytes(state_raw)
    state = json.loads(state_raw)
    if state_hash != norm(root.get("current_state_sha256")):
        raise GateBlocked("CURRENT_STATE_HASH_BINDING_MISMATCH")
    if norm(root.get("startmaster")) != norm(state.get("startmaster")):
        raise GateBlocked("STARTMASTER_IDENTITY_MISMATCH")
    root_step = norm(root.get("next_allowed_step"))
    state_step = norm(state.get("next_allowed_step"))
    if not root_step or root_step != state_step:
        raise GateBlocked("NEXT_ALLOWED_STEP_ROOT_STATE_MISMATCH")
    gate = state.get("execution_gate") or {}
    if gate.get("enforced") is not True:
        raise GateBlocked("EXECUTION_GATE_NOT_ENFORCED")
    if norm(gate.get("step_id")) != state_step:
        raise GateBlocked("EXECUTION_GATE_STEP_MISMATCH")
    if norm(gate.get("state_write_authority")) != "ENTRANCE_GATE_ONLY":
        raise GateBlocked("STATE_WRITE_AUTHORITY_INVALID")
    if norm(gate.get("unknown_step_policy")) != "DENY":
        raise GateBlocked("UNKNOWN_STEP_POLICY_NOT_DENY")
    if gate.get("free_chat_direct_execution_valid") is not False:
        raise GateBlocked("FREE_CHAT_DIRECT_EXECUTION_MUST_BE_INVALID")
    bundle_rel = require_relpath(norm(gate.get("bundle_ref")))
    bundle_path = safe_master_path(master, bundle_rel)
    if not bundle_path.is_file():
        raise GateBlocked("STEP_BUNDLE_MISSING")
    bundle_raw = bundle_path.read_bytes()
    bundle_hash = sha256_bytes(bundle_raw)
    if bundle_hash != norm(gate.get("bundle_sha256")):
        raise GateBlocked("STEP_BUNDLE_HASH_BINDING_MISMATCH")
    bundle = json.loads(bundle_raw)
    if norm(bundle.get("step_id")) != state_step:
        raise GateBlocked("STEP_BUNDLE_STEP_MISMATCH")
    if int(bundle.get("sequence", -1)) != int(gate.get("sequence", -2)):
        raise GateBlocked("STEP_SEQUENCE_MISMATCH")
    return {
        "root": root,
        "root_path": root_path,
        "state": state,
        "state_path": state_path,
        "state_sha256": state_hash,
        "gate": gate,
        "bundle": bundle,
        "bundle_path": bundle_path,
        "bundle_sha256": bundle_hash,
    }

def verify_bound_inputs(master: Path, bundle: dict):
    verified = []
    for idx, row in enumerate(bundle.get("authorized_inputs") or []):
        if not isinstance(row, dict):
            raise GateBlocked(f"AUTHORIZED_INPUT_INVALID:{idx}")
        rel = require_relpath(norm(row.get("ref")))
        path = safe_master_path(master, rel)
        if not path.is_file():
            raise GateBlocked(f"AUTHORIZED_INPUT_MISSING:{idx}")
        actual = sha256_bytes(path.read_bytes())
        expected = norm(row.get("sha256"))
        if not expected or actual != expected:
            raise GateBlocked(f"AUTHORIZED_INPUT_HASH_MISMATCH:{idx}")
        verified.append({"ref": rel, "sha256": actual, "size": path.stat().st_size})
    return verified

def build_ticket(authority: dict):
    state = authority["state"]
    gate = authority["gate"]
    bundle = authority["bundle"]
    body = {
        "contract": "PFERDE_ATELIER_EXECUTION_TICKET_V1",
        "startmaster": state["startmaster"],
        "step_id": state["next_allowed_step"],
        "sequence": int(gate["sequence"]),
        "state_sha256": authority["state_sha256"],
        "bundle_sha256": authority["bundle_sha256"],
        "nonce": secrets.token_hex(16),
        "issued_at_unix": int(time.time()),
        "worker_profile": bundle.get("worker_profile", "OPAQUE_WORKER"),
        "limits": bundle.get("limits") or {},
    }
    body["ticket_id"] = stable_hash(body)
    return body

def issue_capsule(master: Path, out_dir: Path):
    authority = load_authority(master)
    verified = verify_bound_inputs(master, authority["bundle"])
    ticket = build_ticket(authority)
    if out_dir.exists():
        if any(out_dir.iterdir()):
            raise GateBlocked("CAPSULE_OUTPUT_NOT_EMPTY")
    else:
        out_dir.mkdir(parents=True)
    (out_dir / "inputs").mkdir()
    copied = []
    for idx, row in enumerate(verified, 1):
        src = safe_master_path(master, row["ref"])
        dst = out_dir / "inputs" / f"{idx:03d}_{src.name}"
        shutil.copyfile(src, dst)
        copied.append({"capsule_path": f"inputs/{dst.name}", **row})
    instruction = authority["bundle"].get("instruction")
    if not isinstance(instruction, str) or not instruction.strip():
        raise GateBlocked("STEP_INSTRUCTION_MISSING")
    (out_dir / "INSTRUCTION.txt").write_text(instruction.strip() + "\n", encoding="utf-8")
    receipt_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "contract": {"type": "string", "const": "PFERDE_ATELIER_STEP_RECEIPT_V1"},
            "ticket_id": {"type": "string", "const": ticket["ticket_id"]},
            "step_id": {"type": "string", "const": ticket["step_id"]},
            "sequence": {"type": "integer", "const": ticket["sequence"]},
            "state_sha256": {"type": "string", "const": ticket["state_sha256"]},
            "bundle_sha256": {"type": "string", "const": ticket["bundle_sha256"]},
            "status": {"type": "string", "enum": ["PASS", "BLOCKED", "USER_ACTION_REQUIRED"]},
            "navigation_decision": {"type": "boolean", "const": False},
            "state_write_requested": {"type": "boolean", "const": False},
            "workflow_change_requested": {"type": "boolean", "const": False},
            "payload": {},
            "evidence": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["contract", "ticket_id", "step_id", "sequence", "state_sha256", "bundle_sha256", "status", "navigation_decision", "state_write_requested", "workflow_change_requested", "payload", "evidence"],
    }
    manifest = {
        "contract": "PFERDE_ATELIER_EXECUTION_CAPSULE_V1",
        "ticket": ticket,
        "inputs": copied,
        "isolation_policy": {
            "context": "CAPSULE_ONLY",
            "master_tree_exposed": False,
            "history_exposed": False,
            "navigation_authority_exposed_to_worker": False,
            "worker_may_choose_next_step": False,
        },
        "limits": authority["bundle"].get("limits") or {},
    }
    (out_dir / "TICKET.json").write_text(json.dumps(ticket, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (out_dir / "CAPSULE_MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (out_dir / "RECEIPT_SCHEMA.json").write_text(json.dumps(receipt_schema, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"ok": True, "status": "EXECUTION_CAPSULE_ISSUED", "ticket_id": ticket["ticket_id"], "step_id": ticket["step_id"], "sequence": ticket["sequence"], "input_count": len(copied), "capsule": str(out_dir)}

def validate_receipt(ticket_path: Path, receipt_path: Path):
    ticket = read_json(ticket_path)
    receipt = read_json(receipt_path)
    allowed = {"contract", "ticket_id", "step_id", "sequence", "state_sha256", "bundle_sha256", "status", "navigation_decision", "state_write_requested", "workflow_change_requested", "payload", "evidence"}
    required = allowed
    extra = set(receipt) - allowed
    missing = required - set(receipt)
    if extra:
        raise GateBlocked("RECEIPT_EXTRA_FIELDS:" + ",".join(sorted(extra)))
    if missing:
        raise GateBlocked("RECEIPT_MISSING_FIELDS:" + ",".join(sorted(missing)))
    if receipt.get("contract") != "PFERDE_ATELIER_STEP_RECEIPT_V1":
        raise GateBlocked("RECEIPT_CONTRACT_INVALID")
    for key in ("ticket_id", "step_id", "sequence", "state_sha256", "bundle_sha256"):
        if receipt.get(key) != ticket.get(key):
            raise GateBlocked("RECEIPT_BINDING_MISMATCH:" + key)
    if receipt.get("status") not in {"PASS", "BLOCKED", "USER_ACTION_REQUIRED"}:
        raise GateBlocked("RECEIPT_STATUS_INVALID")
    if receipt.get("navigation_decision") is not False:
        raise GateBlocked("WORKER_NAVIGATION_DECISION_REJECTED")
    if receipt.get("state_write_requested") is not False:
        raise GateBlocked("WORKER_STATE_WRITE_REJECTED")
    if receipt.get("workflow_change_requested") is not False:
        raise GateBlocked("WORKER_WORKFLOW_CHANGE_REJECTED")
    if not isinstance(receipt.get("evidence"), list):
        raise GateBlocked("RECEIPT_EVIDENCE_INVALID")
    return {"ok": True, "status": "RECEIPT_VALID", "step_status": receipt["status"], "ticket_id": ticket["ticket_id"], "receipt_sha256": sha256_bytes(receipt_path.read_bytes())}

def advance_state(master: Path, ticket_path: Path, receipt_path: Path):
    authority = load_authority(master)
    ticket = read_json(ticket_path)
    if ticket.get("state_sha256") != authority["state_sha256"] or ticket.get("bundle_sha256") != authority["bundle_sha256"] or ticket.get("step_id") != authority["state"].get("next_allowed_step"):
        raise GateBlocked("ADVANCE_TICKET_NOT_CURRENT")
    receipt_result = validate_receipt(ticket_path, receipt_path)
    receipt = read_json(receipt_path)
    if receipt.get("status") != "PASS":
        raise GateBlocked("ADVANCE_REQUIRES_PASS_RECEIPT")
    nb = authority["bundle"].get("next_binding")
    if not isinstance(nb, dict):
        raise GateBlocked("NEXT_BINDING_NOT_PREBOUND")
    next_step = norm(nb.get("step_id"))
    next_seq = int(nb.get("sequence", -1))
    next_rel = require_relpath(norm(nb.get("bundle_ref")))
    next_path = safe_master_path(master, next_rel)
    if not next_path.is_file():
        raise GateBlocked("NEXT_BUNDLE_MISSING")
    next_hash = sha256_bytes(next_path.read_bytes())
    if next_hash != norm(nb.get("bundle_sha256")):
        raise GateBlocked("NEXT_BUNDLE_HASH_MISMATCH")
    next_bundle = read_json(next_path)
    if norm(next_bundle.get("step_id")) != next_step or int(next_bundle.get("sequence", -2)) != next_seq:
        raise GateBlocked("NEXT_BINDING_IDENTITY_MISMATCH")
    if next_seq <= int(authority["gate"].get("sequence", -1)):
        raise GateBlocked("NON_MONOTONIC_SEQUENCE_REJECTED")
    state = authority["state"]
    state["next_allowed_step"] = next_step
    state["generated_at_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    gate = state["execution_gate"]
    gate["step_id"] = next_step
    gate["sequence"] = next_seq
    gate["bundle_ref"] = next_rel
    gate["bundle_sha256"] = next_hash
    hist = state.setdefault("execution_gate_receipts", [])
    hist.append({"completed_step_id": ticket["step_id"], "sequence": ticket["sequence"], "ticket_id": ticket["ticket_id"], "receipt_sha256": receipt_result["receipt_sha256"]})
    state_path = authority["state_path"]
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    state_hash = sha256_bytes(state_path.read_bytes())
    root = authority["root"]
    root["current_state_sha256"] = state_hash
    root["next_allowed_step"] = next_step
    authority["root_path"].write_text(json.dumps(root, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"ok": True, "status": "STATE_ADVANCED_BY_PREBOUND_TRANSITION", "completed_step_id": ticket["step_id"], "next_step_id": next_step, "sequence": next_seq, "current_state_sha256": state_hash}

def validate_only(master: Path):
    authority = load_authority(master)
    verified = verify_bound_inputs(master, authority["bundle"])
    return {
        "ok": True,
        "status": "ENTRANCE_GATE_AUTHORITY_PASS",
        "startmaster": authority["state"]["startmaster"],
        "step_id": authority["state"]["next_allowed_step"],
        "sequence": authority["gate"]["sequence"],
        "state_sha256": authority["state_sha256"],
        "bundle_sha256": authority["bundle_sha256"],
        "authorized_input_count": len(verified),
        "free_chat_direct_execution_valid": False,
        "domain_logic_authority": "NONE",
    }

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    v = sub.add_parser("validate")
    v.add_argument("--master", required=True)
    i = sub.add_parser("issue")
    i.add_argument("--master", required=True)
    i.add_argument("--out", required=True)
    r = sub.add_parser("validate-receipt")
    r.add_argument("--ticket", required=True)
    r.add_argument("--receipt", required=True)
    a = sub.add_parser("advance")
    a.add_argument("--master", required=True)
    a.add_argument("--ticket", required=True)
    a.add_argument("--receipt", required=True)
    args = ap.parse_args()
    try:
        if args.cmd == "validate":
            result = validate_only(Path(args.master))
        elif args.cmd == "issue":
            result = issue_capsule(Path(args.master), Path(args.out))
        elif args.cmd == "validate-receipt":
            result = validate_receipt(Path(args.ticket), Path(args.receipt))
        else:
            result = advance_state(Path(args.master), Path(args.ticket), Path(args.receipt))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except GateBlocked as exc:
        print(json.dumps({"ok": False, "status": "ENTRANCE_GATE_BLOCKED", "reason": str(exc)}, ensure_ascii=False, indent=2))
        return 2

if __name__ == "__main__":
    sys.exit(main())
