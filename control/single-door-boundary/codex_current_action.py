#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
BRIDGE = REPO / "control/single-door-boundary/codex_current_room_bridge.py"
CONTRACT = "PFERDE_ATELIER_CODEX_CURRENT_ACTION_VIEW_V1"


class ViewError(RuntimeError):
    pass


def _run_bridge(args: list[str]) -> dict:
    proc = subprocess.run(
        [sys.executable, str(BRIDGE), *args],
        cwd=REPO,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    text = (proc.stdout or "").strip()
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ViewError("BOUND_BRIDGE_OUTPUT_INVALID") from exc
    if proc.returncode != 0:
        return data
    return data


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
            "submission_command",
        )
        if any(key not in data for key in required):
            raise ViewError("CURRENT_ACTION_FIELDS_MISSING")
        submit = str(data["submission_command"])
        bridge_prefix = "python3 control/single-door-boundary/codex_current_room_bridge.py submit "
        if not submit.startswith(bridge_prefix):
            raise ViewError("CURRENT_ACTION_SUBMISSION_NOT_BOUND")
        receipt_ref = submit[len(bridge_prefix):]
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
            "submission_command": "python3 control/single-door-boundary/codex_current_action.py submit " + receipt_ref,
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


def selftest() -> dict:
    sample = {
        "status": "CURRENT_BOUND_ACTION_READY",
        "room_token": "R_D_1_01",
        "current_item": {"canonical_article_id": "article:test"},
        "fachworkflow_authority": "EXISTING_UNCHANGED_BOUND_FACHWORKFLOW_ONLY",
        "fachworkflow_prompt_ref": "bound.txt",
        "allowed_output_root": ".pferde-quarantine/test/",
        "item_receipt_ref": ".pferde-quarantine/test/ITEM_RECEIPT.json",
        "item_receipt_schema": {"contract": "X"},
        "submission_command": "python3 control/single-door-boundary/codex_current_room_bridge.py submit .pferde-quarantine/test/ITEM_RECEIPT.json",
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
    if view.get("publish_allowed") is not False:
        raise AssertionError("PUBLISH_NOT_BLOCKED")
    return {
        "ok": True,
        "status": "CODEX_CURRENT_ACTION_VIEW_SELFTEST_PASS",
        "current_action_only": True,
        "server_side_deny_preserved": True,
        "future_route_exposed": False,
        "content_or_quality_authority": "NONE",
        "publish_allowed": False,
    }


def main(argv: list[str]) -> int:
    try:
        if argv == ["current"]:
            result = _current_only(_run_bridge(["current"]))
        elif len(argv) == 2 and argv[0] == "submit":
            result = _current_only(_run_bridge(["submit", argv[1]]))
        elif argv == ["selftest"]:
            result = selftest()
        else:
            raise ViewError("USAGE: current | submit ITEM_RECEIPT.json | selftest")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result.get("status") not in {"BLOCKED"} else 2
    except (ViewError, KeyError, TypeError, ValueError) as exc:
        print(json.dumps({"contract": CONTRACT, "status": "BLOCKED", "error": str(exc), "publish_allowed": False}, ensure_ascii=False, indent=2))
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
