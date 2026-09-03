#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
BRIDGE = REPO / "control/single-door-boundary/codex_current_room_bridge.py"
CONTRACT = "PFERDE_ATELIER_CODEX_CURRENT_ACTION_VIEW_V1"


class ViewError(RuntimeError):
    pass


def _run_json(cmd: list[str]) -> dict:
    proc = subprocess.run(
        cmd,
        cwd=REPO,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    text = (proc.stdout or "").strip()
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ViewError("BOUND_COMMAND_OUTPUT_INVALID") from exc
    if not isinstance(data, dict):
        raise ViewError("BOUND_COMMAND_OUTPUT_NOT_OBJECT")
    return data


def _run_bridge(args: list[str]) -> dict:
    return _run_json([sys.executable, str(BRIDGE), *args])


def _safe_repo_ref(ref: str) -> Path:
    rel = Path(str(ref or ""))
    if not str(ref or "") or rel.is_absolute() or ".." in rel.parts:
        raise ViewError("BOUND_REF_INVALID")
    path = (REPO / rel).resolve()
    if path != REPO and REPO not in path.parents:
        raise ViewError("BOUND_REF_ESCAPE")
    return path


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _run_bound_handoff(adapter_ref: str, request_ref: str) -> dict:
    adapter = _safe_repo_ref(adapter_ref)
    return _run_json([sys.executable, str(adapter), "materialize", request_ref])


def _current_only(data: dict) -> dict:
    status = data.get("status")
    if status == "CURRENT_BOUND_ACTION_READY":
        required = (
            "room_token",
            "current_item",
            "fachworkflow_authority",
            "fachworkflow_prompt_ref",
            "allowed_output_root",
            "item_receipt_ref",
            "item_receipt_schema",
            "fachworkflow_handoff",
            "submission_command",
        )
        if any(key not in data for key in required):
            raise ViewError("CURRENT_ACTION_FIELDS_MISSING")
        handoff = data["fachworkflow_handoff"]
        if not isinstance(handoff, dict):
            raise ViewError("FACHWORKFLOW_HANDOFF_BINDING_MISSING")
        handoff_required = (
            "request_ref",
            "request_contract",
            "adapter_ref",
            "adapter_sha256",
            "accepts_only_real_stage_execution_proofs",
            "content_or_quality_rules_changed",
            "publish_allowed",
        )
        if any(key not in handoff for key in handoff_required):
            raise ViewError("FACHWORKFLOW_HANDOFF_FIELDS_MISSING")
        request_ref = str(handoff["request_ref"])
        if not request_ref.startswith(str(data["allowed_output_root"])):
            raise ViewError("FACHWORKFLOW_REQUEST_OUTSIDE_BOUND_OUTPUT_ROOT")
        if handoff.get("accepts_only_real_stage_execution_proofs") is not True:
            raise ViewError("FACHWORKFLOW_REAL_PROOF_REQUIREMENT_MISSING")
        if handoff.get("content_or_quality_rules_changed") is not False or handoff.get("publish_allowed") is not False:
            raise ViewError("FACHWORKFLOW_HANDOFF_AUTHORITY_INVALID")
        return {
            "contract": CONTRACT,
            "status": "CURRENT_BOUND_ACTION_READY",
            "room_token": data["room_token"],
            "instruction": "EXECUTE_CURRENT_BOUND_ITEM_NOW",
            "current_item": data["current_item"],
            "fachworkflow_authority": data["fachworkflow_authority"],
            "fachworkflow_prompt_ref": data["fachworkflow_prompt_ref"],
            "allowed_output_root": data["allowed_output_root"],
            "item_receipt_ref": data["item_receipt_ref"],
            "item_receipt_schema": data["item_receipt_schema"],
            "fachworkflow_handoff": handoff,
            "existing_article_source_binding": data.get("existing_article_source_binding"),
            "submission_command": "python3 control/single-door-boundary/codex_current_action.py submit-request " + shlex.quote(request_ref),
            "publish_allowed": False,
        }
    if status in {"BLOCKED", "USER_ACTION_REQUIRED", "FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH"}:
        return {
            "contract": CONTRACT,
            "status": status,
            "room_token": data.get("room_token"),
            "error": data.get("error"),
            "evidence": data.get("evidence"),
            "outer_step": data.get("outer_step"),
            "publish_allowed": False,
        }
    if data.get("ok") is False:
        return {
            "contract": CONTRACT,
            "status": "BLOCKED",
            "error": data.get("error") or status or "BOUND_BRIDGE_BLOCKED",
            "publish_allowed": False,
        }
    raise ViewError("BOUND_BRIDGE_STATUS_NOT_WORKER_VISIBLE")


def _submit_request(
    request_ref: str,
    *,
    bridge_runner=None,
    handoff_runner=None,
) -> dict:
    bridge_runner = bridge_runner or _run_bridge
    handoff_runner = handoff_runner or _run_bound_handoff
    raw = bridge_runner(["current"])
    current = _current_only(raw)
    if current.get("status") != "CURRENT_BOUND_ACTION_READY":
        return current
    handoff = current["fachworkflow_handoff"]
    expected_request = str(handoff["request_ref"])
    if request_ref != expected_request:
        raise ViewError("FACHWORKFLOW_HANDOFF_REQUEST_NOT_CURRENT_BOUND_REQUEST")
    request_path = _safe_repo_ref(request_ref)
    if not request_path.is_file():
        raise ViewError("FACHWORKFLOW_HANDOFF_REQUEST_MISSING")
    adapter_ref = str(handoff["adapter_ref"])
    adapter_path = _safe_repo_ref(adapter_ref)
    if not adapter_path.is_file():
        raise ViewError("FACHWORKFLOW_HANDOFF_ADAPTER_MISSING")
    expected_adapter_sha = str(handoff["adapter_sha256"])
    if not re.fullmatch(r"[0-9a-f]{64}", expected_adapter_sha) or _sha256(adapter_path) != expected_adapter_sha:
        raise ViewError("FACHWORKFLOW_HANDOFF_ADAPTER_HASH_MISMATCH")
    result = handoff_runner(adapter_ref, request_ref)
    if result.get("status") != "FACHWORKFLOW_PROOF_HANDOFF_PASS":
        return {
            "contract": CONTRACT,
            "status": "BLOCKED",
            "room_token": current.get("room_token"),
            "error": result.get("error") or result.get("status") or "FACHWORKFLOW_PROOF_HANDOFF_BLOCKED",
            "evidence": None,
            "outer_step": None,
            "publish_allowed": False,
        }
    receipt_ref = str(result.get("item_receipt_ref") or "")
    if receipt_ref != current["item_receipt_ref"]:
        raise ViewError("FACHWORKFLOW_HANDOFF_RECEIPT_NOT_CURRENT_BOUND_RECEIPT")
    receipt_sha = str(result.get("item_receipt_sha256") or "")
    if not re.fullmatch(r"[0-9a-f]{64}", receipt_sha):
        raise ViewError("FACHWORKFLOW_HANDOFF_RECEIPT_HASH_INVALID")
    receipt_path = _safe_repo_ref(receipt_ref)
    if not receipt_path.is_file() or _sha256(receipt_path) != receipt_sha:
        raise ViewError("FACHWORKFLOW_HANDOFF_RECEIPT_HASH_MISMATCH")
    return _current_only(bridge_runner(["submit", receipt_ref]))


def selftest() -> dict:
    with tempfile.TemporaryDirectory() as td:
        global REPO
        old_repo = REPO
        REPO = Path(td).resolve()
        try:
            adapter_ref = "control/startmaster0107/fachworkflow_proof_handoff.py"
            adapter = _safe_repo_ref(adapter_ref)
            adapter.parent.mkdir(parents=True, exist_ok=True)
            adapter.write_text("# test adapter\n", encoding="utf-8")
            request_ref = ".pferde-quarantine/test/FACHWORKFLOW_HANDOFF_REQUEST.json"
            request = _safe_repo_ref(request_ref)
            request.parent.mkdir(parents=True, exist_ok=True)
            request.write_text("{}\n", encoding="utf-8")
            receipt_ref = ".pferde-quarantine/test/ITEM_RECEIPT.json"
            receipt = _safe_repo_ref(receipt_ref)
            receipt.write_text("{}\n", encoding="utf-8")
            sample = {
                "status": "CURRENT_BOUND_ACTION_READY",
                "room_token": "R_D_1_01",
                "current_item": {"canonical_article_id": "article:test"},
                "fachworkflow_authority": "EXISTING_UNCHANGED_BOUND_FACHWORKFLOW_ONLY",
                "fachworkflow_prompt_ref": "bound.txt",
                "allowed_output_root": ".pferde-quarantine/test/",
                "item_receipt_ref": receipt_ref,
                "item_receipt_schema": {"contract": "X"},
                "fachworkflow_handoff": {
                    "contract": "PFERDE_ATELIER_FACHWORKFLOW_PROOF_HANDOFF_BINDING_V1",
                    "request_ref": request_ref,
                    "request_contract": "PFERDE_ATELIER_FACHWORKFLOW_HANDOFF_REQUEST_V1",
                    "adapter_ref": adapter_ref,
                    "adapter_sha256": _sha256(adapter),
                    "accepts_only_real_stage_execution_proofs": True,
                    "content_or_quality_rules_changed": False,
                    "publish_allowed": False,
                },
                "existing_article_source_binding": {
                    "contract": "PFERDE_ATELIER_EXISTING_ARTICLE_SOURCE_BINDING_V1",
                    "ref": "control/startmaster0107/recovery_sources/test/ARTICLE_test.md",
                    "sha256": "a" * 64,
                },
                "submission_command": "python3 control/single-door-boundary/codex_current_room_bridge.py submit " + receipt_ref,
                "all_other_actions": "DENY",
                "next_room_token": "SECRET",
                "server_executor": "SECRET",
            }
            view = _current_only(sample)
            forbidden = {"all_other_actions", "next_room_token", "server_executor", "route", "rooms", "future_items", "bound_item_ids"}
            if forbidden.intersection(view):
                raise AssertionError("WORKER_VIEW_LEAK")
            if view.get("instruction") != "EXECUTE_CURRENT_BOUND_ITEM_NOW":
                raise AssertionError("CURRENT_ACTION_NOT_EXPLICIT")
            if " submit-request " not in view.get("submission_command", ""):
                raise AssertionError("REQUEST_FIRST_SUBMISSION_NOT_BOUND")
            if view.get("publish_allowed") is not False:
                raise AssertionError("PUBLISH_NOT_BLOCKED")
            calls = []
            def fake_bridge(args):
                calls.append(("bridge", tuple(args)))
                if args == ["current"]:
                    return sample
                if args == ["submit", receipt_ref]:
                    return {"status": "FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH", "room_token": "R_006"}
                raise AssertionError("UNEXPECTED_BRIDGE_CALL")
            def fake_handoff(adapter_ref_value, request_ref_value):
                calls.append(("handoff", adapter_ref_value, request_ref_value))
                return {
                    "status": "FACHWORKFLOW_PROOF_HANDOFF_PASS",
                    "item_receipt_ref": receipt_ref,
                    "item_receipt_sha256": _sha256(receipt),
                }
            result = _submit_request(request_ref, bridge_runner=fake_bridge, handoff_runner=fake_handoff)
            if result.get("status") != "FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH":
                raise AssertionError("REQUEST_HANDOFF_SUBMISSION_POSITIVE_FAILED")
            if calls != [
                ("bridge", ("current",)),
                ("handoff", adapter_ref, request_ref),
                ("bridge", ("submit", receipt_ref)),
            ]:
                raise AssertionError("REQUEST_HANDOFF_ORDER_INVALID")
            blocked_calls = []
            def blocked_bridge(args):
                blocked_calls.append(("bridge", tuple(args)))
                return sample
            def blocked_handoff(adapter_ref_value, request_ref_value):
                blocked_calls.append(("handoff", adapter_ref_value, request_ref_value))
                return {"status": "FACHWORKFLOW_PROOF_HANDOFF_BLOCKED", "error": "TEST_BLOCK"}
            blocked = _submit_request(request_ref, bridge_runner=blocked_bridge, handoff_runner=blocked_handoff)
            if blocked.get("status") != "BLOCKED" or blocked.get("error") != "TEST_BLOCK":
                raise AssertionError("HANDOFF_NEGATIVE_NOT_FAIL_CLOSED")
            if blocked_calls != [
                ("bridge", ("current",)),
                ("handoff", adapter_ref, request_ref),
            ]:
                raise AssertionError("HANDOFF_NEGATIVE_ADVANCED")
            try:
                _submit_request(".pferde-quarantine/test/WRONG.json", bridge_runner=fake_bridge, handoff_runner=fake_handoff)
            except ViewError as exc:
                if str(exc) != "FACHWORKFLOW_HANDOFF_REQUEST_NOT_CURRENT_BOUND_REQUEST":
                    raise
            else:
                raise AssertionError("WRONG_REQUEST_NOT_BLOCKED")
            return {
                "ok": True,
                "status": "CODEX_CURRENT_ACTION_REQUEST_HANDOFF_SELFTEST_PASS",
                "request_first": True,
                "handoff_after_request_only": True,
                "handoff_failure_fail_closed": True,
                "direct_receipt_submission_not_emitted": True,
                "content_or_quality_authority": "NONE",
                "publish_allowed": False,
            }
        finally:
            REPO = old_repo


def main(argv: list[str]) -> int:
    try:
        if argv == ["current"]:
            result = _current_only(_run_bridge(["current"]))
        elif len(argv) == 2 and argv[0] == "submit-request":
            result = _submit_request(argv[1])
        elif argv == ["selftest"]:
            result = selftest()
        else:
            raise ViewError("USAGE: current | submit-request FACHWORKFLOW_HANDOFF_REQUEST.json | selftest")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result.get("status") not in {"BLOCKED"} else 2
    except (ViewError, KeyError, TypeError, ValueError, OSError) as exc:
        print(json.dumps({"contract": CONTRACT, "status": "BLOCKED", "error": str(exc), "publish_allowed": False}, ensure_ascii=False, indent=2))
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
