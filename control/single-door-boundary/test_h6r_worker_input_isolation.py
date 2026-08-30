#!/usr/bin/env python3
from __future__ import annotations

import copy
import inspect
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import single_door_boundary as m


def must_block(name, fn, expected=None):
    try:
        fn()
    except Exception as exc:
        if expected is not None and expected not in str(exc):
            raise AssertionError(f"{name}:WRONG_ERROR:{exc}") from exc
        return {"name": name, "status": "PASS", "blocked_by": type(exc).__name__, "detail": str(exc)}
    raise AssertionError(f"{name}:NOT_BLOCKED")


def main():
    checks = []
    binding = m.DoorBinding.from_mapping({
        "contract": m.BOUNDARY_CONTRACT,
        "room_token": "R_TEST",
        "action_token": "A_TEST",
        "receipt_token": "P_TEST",
        "next_room_token": "R_NEXT",
        "input_handles": ["I_TEST"],
    })

    request = m.build_worker_request(binding=binding, model="gpt-5.6-sol")
    assert request["input"] == "R_TEST"
    assert request["metadata"]["room_token"] == "R_TEST"
    assert len(request["tools"]) == 1
    assert request["tools"][0]["name"] == m.FUNCTION_NAME
    assert request["tool_choice"] == {"type": "function", "name": m.FUNCTION_NAME}
    assert request["parallel_tool_calls"] is False
    m.assert_single_door_request(request)
    checks.append({"name": "OPAQUE_TOKEN_POSITIVE", "status": "PASS"})

    for fn in (m.build_worker_request, m.run_single_door):
        assert "worker_input" not in inspect.signature(fn).parameters
    checks.append({"name": "WORKER_INPUT_PARAMETER_REMOVED", "status": "PASS"})

    checks.append(must_block(
        "ARTICLE_TEXT_AS_WORKER_INPUT_REJECTED",
        lambda: m.build_worker_request(
            binding=binding,
            model="gpt-5.6-sol",
            worker_input="Artikeltext über Fliegenmasken"
        ),
        "unexpected keyword argument 'worker_input'",
    ))

    fach = copy.deepcopy(request)
    fach["input"] = "Fliegenmasken"
    fach["metadata"]["room_token"] = "Fliegenmasken"
    checks.append(must_block(
        "FACHBEGRIFF_AS_MODEL_INPUT_REJECTED",
        lambda: m.assert_single_door_request(fach),
        "OPAQUE_ROOM_INPUT_REQUIRED",
    ))

    second = copy.deepcopy(request)
    second["tools"].append({
        "type": "function",
        "name": "second_action",
        "description": "second",
        "parameters": dict(m.EMPTY_PARAMETERS),
        "strict": True,
    })
    checks.append(must_block(
        "SECOND_CAPABILITY_REJECTED",
        lambda: m.assert_single_door_request(second),
        "EXACTLY_ONE_TOOL_REQUIRED",
    ))

    for tool_type in ("web_search", "file_search", "github", "shell"):
        bad = copy.deepcopy(request)
        bad["tools"].append({"type": tool_type, "name": tool_type})
        checks.append(must_block(
            f"ADDITIONAL_{tool_type.upper()}_CAPABILITY_REJECTED",
            lambda b=bad: m.assert_single_door_request(b),
            "EXACTLY_ONE_TOOL_REQUIRED",
        ))

    for call_type in ("web_search_call", "file_search_call", "github_call", "shell_call"):
        checks.append(must_block(
            f"FORGED_{call_type.upper()}_REJECTED",
            lambda t=call_type: m.validate_single_door_response({
                "output": [{"type": t, "name": t, "arguments": "{}"}]
            }),
            "UNBOUND_EXECUTABLE_CALL_REJECTED",
        ))

    receipt = {
        "contract": m.BOUNDARY_CONTRACT,
        "room_token": binding.room_token,
        "action_token": binding.action_token,
        "receipt_token": binding.receipt_token,
        "next_room_token": "R_WRONG",
        "status": "PASS",
        "evidence": ["H6R_LOCAL"],
    }
    checks.append(must_block(
        "WRONG_NEXT_ROOM_REJECTED",
        lambda: m.validate_action_receipt(binding, receipt),
        "ACTION_RECEIPT_BINDING_MISMATCH:next_room_token",
    ))

    good_receipt = dict(receipt)
    good_receipt["next_room_token"] = binding.next_room_token
    accepted = m.validate_action_receipt(binding, good_receipt)
    assert accepted["next_room_token"] == "R_NEXT"
    checks.append({"name": "BOUND_NEXT_ROOM_POSITIVE", "status": "PASS"})

    counts = {"transport": 0, "action": 0}
    def transport(req):
        counts["transport"] += 1
        m.assert_single_door_request(req)
        assert req["input"] == "R_TEST"
        return {"output": [{"type": "function_call", "name": m.FUNCTION_NAME, "arguments": "{}"}]}
    def bound_action(_binding):
        counts["action"] += 1
        return good_receipt
    result = m.run_single_door(
        binding=binding,
        model="gpt-5.6-sol",
        transport=transport,
        bound_action=bound_action,
    )
    assert result["status"] == "PASS"
    assert result["next_room_token"] == "R_NEXT"
    assert counts == {"transport": 1, "action": 1}
    checks.append({"name": "FULL_SINGLE_DOOR_POSITIVE", "status": "PASS"})

    out = {
        "contract": "H6R_WORKER_INPUT_ISOLATION_LOCAL_PROOF_V1",
        "status": "PASS",
        "checks_passed": len(checks),
        "checks_total": len(checks),
        "worker_visible_input": "OPAQUE_ROOM_TOKEN_ONLY",
        "capability_count": 1,
        "worker_input_parameter": "ABSENT",
        "checks": checks,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
