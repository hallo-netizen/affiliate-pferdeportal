#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

STATE_CONTRACT = "CONCEPT_AGENT_WORKFLOW_STATE_V1"
ENTRY_CONTRACT = "CONCEPT_AGENT_WORKFLOW_ENTRY_PROOF_V1"
PROOF_CONTRACT = "CONCEPT_AGENT_ALL_STAGE_REENTRY_PROOF_V1"
VERSION = "1.0.0"

PHASES = (
    "INTAKE_REQUIRED",
    "RESEARCH_REQUIRED",
    "RESEARCH_HASH_BOUND",
    "AUTHORING_HASH_BOUND",
    "AUTHORING_IN_PROGRESS",
    "FILE_OUTPUT_REQUIRED",
    "FILE_READY",
    "COMPLETE",
)

NEXT_ACTION = {
    "INTAKE_REQUIRED": "INTAKE_PASS",
    "RESEARCH_REQUIRED": "RESEARCH_HASH_BIND_PASS",
    "RESEARCH_HASH_BOUND": "AUTHORING_HASH_BIND_PASS",
    "AUTHORING_HASH_BOUND": "AUTHORING_START",
    "AUTHORING_IN_PROGRESS": "AUTHORING_PASS",
    "FILE_OUTPUT_REQUIRED": "FILE_OUTPUT_PASS",
    "FILE_READY": "CHAT_RETURN_PASS",
    "COMPLETE": "NONE",
}

NEXT_PHASE = {
    "INTAKE_REQUIRED": "RESEARCH_REQUIRED",
    "RESEARCH_REQUIRED": "RESEARCH_HASH_BOUND",
    "RESEARCH_HASH_BOUND": "AUTHORING_HASH_BOUND",
    "AUTHORING_HASH_BOUND": "AUTHORING_IN_PROGRESS",
    "AUTHORING_IN_PROGRESS": "FILE_OUTPUT_REQUIRED",
    "FILE_OUTPUT_REQUIRED": "FILE_READY",
    "FILE_READY": "COMPLETE",
}


class Blocked(RuntimeError):
    pass


def canon(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def stable(value: Any) -> str:
    return hashlib.sha256(canon(value)).hexdigest()


def seal(state: dict[str, Any]) -> dict[str, Any]:
    out = dict(state)
    out.pop("state_sha256", None)
    out["state_sha256"] = stable(out)
    return out


def initial(batch_sha256: str, item_count: int) -> dict[str, Any]:
    if len(batch_sha256) != 64 or any(c not in "0123456789abcdef" for c in batch_sha256):
        raise Blocked("BATCH_SHA_INVALID")
    if not isinstance(item_count, int) or item_count < 1:
        raise Blocked("ITEM_COUNT_INVALID")
    return seal({
        "contract": STATE_CONTRACT,
        "version": VERSION,
        "status": "IN_PROGRESS",
        "phase": "INTAKE_REQUIRED",
        "allowed_action": "INTAKE_PASS",
        "batch_sha256": batch_sha256,
        "item_count": item_count,
        "evidence": {},
        "transition_log": [],
        "publish_allowed": False,
    })


def validate(state: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(state, dict):
        raise Blocked("STATE_OBJECT_REQUIRED")
    if state.get("contract") != STATE_CONTRACT:
        raise Blocked("STATE_CONTRACT_INVALID")
    if state.get("version") != VERSION:
        raise Blocked("STATE_VERSION_INVALID")
    if state.get("publish_allowed") is not False:
        raise Blocked("STATE_PUBLISH_MUST_BE_FALSE")
    declared = state.get("state_sha256")
    core = dict(state)
    core.pop("state_sha256", None)
    if declared != stable(core):
        raise Blocked("STATE_HASH_MISMATCH")
    phase = state.get("phase")
    if phase not in PHASES:
        raise Blocked("STATE_PHASE_INVALID")
    if state.get("allowed_action") != NEXT_ACTION[phase]:
        raise Blocked("STATE_ALLOWED_ACTION_MISMATCH")
    if not isinstance(state.get("evidence"), dict):
        raise Blocked("STATE_EVIDENCE_INVALID")
    if not isinstance(state.get("transition_log"), list):
        raise Blocked("STATE_LOG_INVALID")
    if phase == "COMPLETE":
        if state.get("status") != "PASS":
            raise Blocked("STATE_COMPLETE_STATUS_INVALID")
    elif state.get("status") != "IN_PROGRESS":
        raise Blocked("STATE_IN_PROGRESS_STATUS_INVALID")
    return state


def entry_proof(state: dict[str, Any]) -> dict[str, Any]:
    state = validate(state)
    proof = {
        "contract": ENTRY_CONTRACT,
        "status": "PASS",
        "batch_sha256": state["batch_sha256"],
        "state_sha256": state["state_sha256"],
        "phase": state["phase"],
        "allowed_action": state["allowed_action"],
        "resume_exact_phase": True,
        "workflow_control_authority": "GITHUB_WORKFLOW_GUARD_ONLY",
        "chat_execution_authority": "NONE",
        "publish_allowed": False,
    }
    proof["proof_sha256"] = stable(proof)
    return proof


def advance(state: dict[str, Any], action: str, evidence_sha256: str) -> dict[str, Any]:
    state = validate(state)
    if state["phase"] == "COMPLETE":
        raise Blocked("WORKFLOW_ALREADY_COMPLETE")
    if action != state["allowed_action"]:
        raise Blocked("ACTION_NOT_ALLOWED:" + str(action))
    if len(evidence_sha256) != 64 or any(c not in "0123456789abcdef" for c in evidence_sha256):
        raise Blocked("EVIDENCE_SHA_INVALID")

    old = state["phase"]
    new = NEXT_PHASE[old]
    out = json.loads(json.dumps(state))
    out["evidence"][old] = {"action": action, "sha256": evidence_sha256}
    out["transition_log"].append({
        "from": old,
        "action": action,
        "evidence_sha256": evidence_sha256,
        "to": new,
    })
    out["phase"] = new
    out["allowed_action"] = NEXT_ACTION[new]
    if new == "COMPLETE":
        out["status"] = "PASS"
    return seal(out)


def _github_request(method: str, url: str, token: str, payload: dict[str, Any] | None = None) -> Any:
    data = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = {
        "Authorization": "Bearer " + token,
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            raw = response.read()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        if exc.code == 404 and method == "GET":
            return None
        raise Blocked("GITHUB_STATE_HTTP_ERROR:" + str(exc.code)) from exc
    except Exception as exc:
        raise Blocked("GITHUB_STATE_CALL_FAILED") from exc


def persist(state: dict[str, Any]) -> None:
    if os.getenv("CONCEPT_AGENT_WORKFLOW_PERSIST_GITHUB_STATE", "").strip() != "1":
        return
    token = os.getenv("GITHUB_TOKEN", "").strip()
    repo = os.getenv("GITHUB_REPOSITORY", "").strip()
    branch = os.getenv("CONCEPT_AGENT_STATE_BRANCH", "concept-agent/production-control").strip()
    path = os.getenv("CONCEPT_AGENT_WORKFLOW_STATE_PATH", "concept_agent/runtime/WORKFLOW_CURRENT_STATE.json").strip()
    if not token or not repo or not branch or not path:
        raise Blocked("GITHUB_STATE_CONFIG_MISSING")

    quoted = "/".join(urllib.parse.quote(x, safe="") for x in path.split("/"))
    url = f"https://api.github.com/repos/{repo}/contents/{quoted}"
    existing = _github_request("GET", url + "?ref=" + urllib.parse.quote(branch, safe=""), token)
    payload: dict[str, Any] = {
        "message": f"Concept Agent workflow state: {state['phase']}",
        "content": base64.b64encode((json.dumps(state, ensure_ascii=False, indent=2) + "\n").encode("utf-8")).decode("ascii"),
        "branch": branch,
    }
    if isinstance(existing, dict) and isinstance(existing.get("sha"), str):
        payload["sha"] = existing["sha"]
    _github_request("PUT", url, token, payload)


def write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if isinstance(value, dict) and value.get("contract") == STATE_CONTRACT:
        persist(value)


def read(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise Blocked("STATE_OBJECT_REQUIRED")
    return value


def test_hash(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def simulate_positive(outdir: Path) -> dict[str, Any]:
    state = initial(test_hash("all-stage-batch"), 3)
    entries = []
    while state["phase"] != "COMPLETE":
        entries.append(entry_proof(state))
        state = advance(state, state["allowed_action"], test_hash("evidence:" + state["phase"]))
    entries.append(entry_proof(state))
    if [x["phase"] for x in entries] != list(PHASES):
        raise Blocked("POSITIVE_PHASE_COVERAGE_FAIL")
    proof = {
        "contract": PROOF_CONTRACT,
        "status": "PASS",
        "kind": "POSITIVE",
        "entry_phases": [x["phase"] for x in entries],
        "entries": entries,
        "final_state_sha256": state["state_sha256"],
        "publish_allowed": False,
    }
    proof["proof_sha256"] = stable(proof)
    write(outdir / "ALL_STAGE_REENTRY_POSITIVE.json", proof)
    write(outdir / "FINAL_STATE.json", state)
    return proof


def simulate_negative(outdir: Path) -> dict[str, Any]:
    cases = []

    def expect_block(name: str, fn) -> None:
        try:
            fn()
        except Blocked as exc:
            cases.append({"case": name, "blocked": True, "reason": str(exc)})
        else:
            raise Blocked("NEGATIVE_NOT_BLOCKED:" + name)

    state = initial(test_hash("negative-batch"), 2)
    for phase in PHASES[:-1]:
        if state["phase"] != phase:
            raise Blocked("NEGATIVE_SETUP_PHASE_FAIL")
        wrong = "FILE_OUTPUT_PASS" if state["allowed_action"] != "FILE_OUTPUT_PASS" else "RESEARCH_HASH_BIND_PASS"
        snapshot = json.loads(json.dumps(state))
        expect_block("wrong-action-" + phase, lambda snap=snapshot, wrong_action=wrong: advance(snap, wrong_action, test_hash("wrong")))
        state = advance(state, state["allowed_action"], test_hash("ok:" + phase))

    base = initial(test_hash("tamper-batch"), 1)
    tampered = json.loads(json.dumps(base))
    tampered["phase"] = "FILE_READY"
    expect_block("phase-tamper-without-reseal", lambda: entry_proof(tampered))

    tampered2 = json.loads(json.dumps(base))
    tampered2["allowed_action"] = "AUTHORING_START"
    tampered2 = seal(tampered2)
    expect_block("allowed-action-tamper", lambda: entry_proof(tampered2))

    proof = {
        "contract": PROOF_CONTRACT,
        "status": "PASS",
        "kind": "NEGATIVE",
        "cases": cases,
        "publish_allowed": False,
    }
    proof["proof_sha256"] = stable(proof)
    write(outdir / "ALL_STAGE_REENTRY_NEGATIVE.json", proof)
    return proof


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("init")
    p.add_argument("--batch", required=True)
    p.add_argument("--item-count", type=int, required=True)
    p.add_argument("--out", required=True)

    p = sub.add_parser("entry")
    p.add_argument("--state", required=True)
    p.add_argument("--out", required=True)

    p = sub.add_parser("advance")
    p.add_argument("--state", required=True)
    p.add_argument("--action", required=True)
    p.add_argument("--evidence-sha256", required=True)
    p.add_argument("--out", required=True)

    for name in ("simulate-positive", "simulate-negative"):
        p = sub.add_parser(name)
        p.add_argument("--out", required=True)

    args = parser.parse_args(argv)
    try:
        out = Path(args.out)
        if args.command == "init":
            write(out, initial(args.batch, args.item_count))
        elif args.command == "entry":
            write(out, entry_proof(read(Path(args.state))))
        elif args.command == "advance":
            write(out, advance(read(Path(args.state)), args.action, args.evidence_sha256))
        elif args.command == "simulate-positive":
            simulate_positive(out)
        elif args.command == "simulate-negative":
            simulate_negative(out)
        return 0
    except (Blocked, ValueError, json.JSONDecodeError, OSError) as exc:
        print("CONCEPT_AGENT_WORKFLOW_GUARD_BLOCKED:" + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
