#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import single_door_boundary as m


def expect_block(fn, token):
    try:
        fn()
    except m.BoundaryError as exc:
        assert token in str(exc), (token, str(exc))
        return
    raise AssertionError(f"expected block: {token}")


def main():
    binding = m.DoorBinding.from_mapping({
        "contract": m.BOUNDARY_CONTRACT,
        "room_token": "R_TEST",
        "action_token": "A_TEST",
        "receipt_token": "P_TEST",
        "next_room_token": "R_NEXT",
        "input_handles": ["I_TEST"],
    })

    request = m.build_worker_request(binding=binding, model="gpt-5.6-sol", worker_input="opaque-test")
    assert len(request["tools"]) == 1
    assert request["tools"][0]["type"] == "function"
    assert request["tools"][0]["name"] == m.FUNCTION_NAME
    assert request["tool_choice"] == {"type": "function", "name": m.FUNCTION_NAME}
    assert request["parallel_tool_calls"] is False

    two = copy.deepcopy(request)
    two["tools"].append({"type": "function", "name": "second_action", "parameters": {"type": "object"}})
    expect_block(lambda: m.assert_single_door_request(two), "EXACTLY_ONE_TOOL_REQUIRED")

    assert all(t.get("type") not in {"shell", "computer", "mcp"} for t in request["tools"])
    expect_block(
        lambda: m.validate_single_door_response({"output": [{"type": "shell_call", "name": "shell", "arguments": "{}"}]}),
        "UNBOUND_EXECUTABLE_CALL_REJECTED",
    )

    assert all(t.get("type") not in {"web_search", "file_search"} for t in request["tools"])
    expect_block(
        lambda: m.validate_single_door_response({"output": [{"type": "web_search_call", "name": "web_search", "arguments": "{}"}]}),
        "UNBOUND_EXECUTABLE_CALL_REJECTED",
    )
    expect_block(
        lambda: m.validate_single_door_response({"output": [{"type": "file_search_call", "name": "file_search", "arguments": "{}"}]}),
        "UNBOUND_EXECUTABLE_CALL_REJECTED",
    )

    expect_block(
        lambda: m.validate_single_door_response({"output": [{"type": "function_call", "name": m.FUNCTION_NAME, "arguments": json.dumps({"next_room_token": "R_PREV"})}]}),
        "FUNCTION_ARGUMENTS_MUST_BE_EMPTY",
    )
    expect_block(
        lambda: m.validate_single_door_response({"output": [{"type": "function_call", "name": m.FUNCTION_NAME, "arguments": json.dumps({"next_room_token": "R_SIDE"})}]}),
        "FUNCTION_ARGUMENTS_MUST_BE_EMPTY",
    )

    receipt = {
        "contract": m.BOUNDARY_CONTRACT,
        "room_token": binding.room_token,
        "action_token": binding.action_token,
        "receipt_token": binding.receipt_token,
        "next_room_token": binding.next_room_token,
        "status": "PASS",
        "evidence": ["H0V_TEST"],
    }
    wrong = dict(receipt)
    wrong["next_room_token"] = "R_SIDE"
    expect_block(lambda: m.validate_action_receipt(binding, wrong), "ACTION_RECEIPT_BINDING_MISMATCH:next_room_token")

    counts = {"transport": 0, "action": 0}

    def transport(req):
        counts["transport"] += 1
        m.assert_single_door_request(req)
        return {"output": [{"type": "function_call", "name": m.FUNCTION_NAME, "arguments": "{}"}]}

    def bound_action(_binding):
        counts["action"] += 1
        return dict(receipt)

    result = m.run_single_door(
        binding=binding,
        model="gpt-5.6-sol",
        worker_input="opaque-test",
        transport=transport,
        bound_action=bound_action,
    )
    assert result["status"] == "PASS"
    assert result["next_room_token"] == "R_NEXT"
    assert counts == {"transport": 1, "action": 1}

    expect_block(
        lambda: m.validate_single_door_response({"output": [
            {"type": "function_call", "name": m.FUNCTION_NAME, "arguments": "{}"},
            {"type": "function_call", "name": m.FUNCTION_NAME, "arguments": "{}"},
        ]}),
        "EXACTLY_ONE_EXECUTABLE_CALL_REQUIRED",
    )

    print(json.dumps({
        "ok": True,
        "status": "H0V_SINGLE_DOOR_MECHANICAL_PROOF_PASS",
        "checks": 12,
        "allowed_action": "PASS",
        "second_action": "BLOCKED",
        "repo_shell_capability": "NOT_PROVISIONED_AND_FORGED_CALL_BLOCKED",
        "free_search_capability": "NOT_PROVISIONED_AND_FORGED_CALL_BLOCKED",
        "backtrack": "BLOCKED",
        "sidejump": "BLOCKED",
        "wrong_receipt": "BLOCKED",
        "valid_receipt": "EXACT_PREBOUND_NEXT_ROOM",
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
