#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any, Callable, Dict, Iterable, Mapping, Optional


BOUNDARY_CONTRACT = "PFERDE_ATELIER_SINGLE_DOOR_EXECUTION_BOUNDARY_V1"
FUNCTION_NAME = "execute_bound_action"
TOKEN_RE = re.compile(r"^[A-Za-z0-9_.:-]{1,128}$")


class BoundaryError(RuntimeError):
    pass


@dataclass(frozen=True)
class DoorBinding:
    room_token: str
    action_token: str
    receipt_token: str
    next_room_token: str
    input_handles: tuple[str, ...]

    @classmethod
    def from_mapping(cls, raw: Mapping[str, Any]) -> "DoorBinding":
        allowed = {
            "contract",
            "room_token",
            "action_token",
            "receipt_token",
            "next_room_token",
            "input_handles",
        }
        if set(raw) != allowed:
            raise BoundaryError("BINDING_FIELDS_INVALID")
        if raw.get("contract") != BOUNDARY_CONTRACT:
            raise BoundaryError("BINDING_CONTRACT_INVALID")

        def token(name: str) -> str:
            value = raw.get(name)
            if not isinstance(value, str) or not TOKEN_RE.fullmatch(value):
                raise BoundaryError(f"BINDING_TOKEN_INVALID:{name}")
            return value

        handles = raw.get("input_handles")
        if not isinstance(handles, list) or not handles:
            raise BoundaryError("INPUT_HANDLES_INVALID")
        parsed_handles = []
        for idx, value in enumerate(handles):
            if not isinstance(value, str) or not TOKEN_RE.fullmatch(value):
                raise BoundaryError(f"INPUT_HANDLE_INVALID:{idx}")
            parsed_handles.append(value)
        if len(set(parsed_handles)) != len(parsed_handles):
            raise BoundaryError("INPUT_HANDLES_DUPLICATE")

        return cls(
            room_token=token("room_token"),
            action_token=token("action_token"),
            receipt_token=token("receipt_token"),
            next_room_token=token("next_room_token"),
            input_handles=tuple(parsed_handles),
        )


def build_worker_request(*, binding: DoorBinding, model: str, worker_input: str) -> Dict[str, Any]:
    if not isinstance(model, str) or not model.strip():
        raise BoundaryError("MODEL_INVALID")
    if not isinstance(worker_input, str):
        raise BoundaryError("WORKER_INPUT_INVALID")

    # The model gets exactly one executable capability. The action identity,
    # input handles, receipt token and next room stay server-side and are not
    # selectable by the model.
    request = {
        "model": model.strip(),
        "input": worker_input,
        "tools": [
            {
                "type": "function",
                "name": FUNCTION_NAME,
                "description": "Execute the one opaque action bound to the current room.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                    "additionalProperties": False,
                },
                "strict": True,
            }
        ],
        "tool_choice": {"type": "function", "name": FUNCTION_NAME},
        "parallel_tool_calls": False,
        "metadata": {
            "single_door_contract": BOUNDARY_CONTRACT,
            "room_token": binding.room_token,
        },
    }
    assert_single_door_request(request)
    return request


def assert_single_door_request(request: Mapping[str, Any]) -> None:
    tools = request.get("tools")
    if not isinstance(tools, list) or len(tools) != 1:
        raise BoundaryError("EXACTLY_ONE_TOOL_REQUIRED")
    tool = tools[0]
    if not isinstance(tool, Mapping):
        raise BoundaryError("TOOL_INVALID")
    if tool.get("type") != "function" or tool.get("name") != FUNCTION_NAME:
        raise BoundaryError("BOUND_TOOL_INVALID")
    if request.get("tool_choice") != {"type": "function", "name": FUNCTION_NAME}:
        raise BoundaryError("BOUND_TOOL_NOT_FORCED")
    if request.get("parallel_tool_calls") is not False:
        raise BoundaryError("PARALLEL_TOOL_CALLS_FORBIDDEN")


def _function_calls(response: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    output = response.get("output")
    if not isinstance(output, list):
        raise BoundaryError("RESPONSE_OUTPUT_INVALID")
    calls: list[Mapping[str, Any]] = []
    for item in output:
        if isinstance(item, Mapping) and item.get("type") in {
            "function_call",
            "custom_tool_call",
            "mcp_call",
            "computer_call",
            "shell_call",
            "file_search_call",
            "web_search_call",
        }:
            calls.append(item)
    return calls


def validate_single_door_response(response: Mapping[str, Any]) -> Mapping[str, Any]:
    calls = _function_calls(response)
    if len(calls) != 1:
        raise BoundaryError("EXACTLY_ONE_EXECUTABLE_CALL_REQUIRED")
    call = calls[0]
    if call.get("type") != "function_call" or call.get("name") != FUNCTION_NAME:
        raise BoundaryError("UNBOUND_EXECUTABLE_CALL_REJECTED")
    args = call.get("arguments", "{}")
    if isinstance(args, str):
        try:
            args_obj = json.loads(args)
        except json.JSONDecodeError as exc:
            raise BoundaryError("FUNCTION_ARGUMENTS_INVALID") from exc
    elif isinstance(args, Mapping):
        args_obj = dict(args)
    else:
        raise BoundaryError("FUNCTION_ARGUMENTS_INVALID")
    if args_obj != {}:
        raise BoundaryError("FUNCTION_ARGUMENTS_MUST_BE_EMPTY")
    return call


def validate_action_receipt(binding: DoorBinding, receipt: Mapping[str, Any]) -> Dict[str, Any]:
    allowed = {
        "contract",
        "room_token",
        "action_token",
        "receipt_token",
        "next_room_token",
        "status",
        "evidence",
    }
    if set(receipt) != allowed:
        raise BoundaryError("ACTION_RECEIPT_FIELDS_INVALID")
    if receipt.get("contract") != BOUNDARY_CONTRACT:
        raise BoundaryError("ACTION_RECEIPT_CONTRACT_INVALID")
    expected = {
        "room_token": binding.room_token,
        "action_token": binding.action_token,
        "receipt_token": binding.receipt_token,
        "next_room_token": binding.next_room_token,
    }
    for key, value in expected.items():
        if receipt.get(key) != value:
            raise BoundaryError(f"ACTION_RECEIPT_BINDING_MISMATCH:{key}")
    if receipt.get("status") not in {"PASS", "BLOCKED", "USER_ACTION_REQUIRED"}:
        raise BoundaryError("ACTION_RECEIPT_STATUS_INVALID")
    evidence = receipt.get("evidence")
    if not isinstance(evidence, list) or not evidence or not all(isinstance(x, str) and x.strip() for x in evidence):
        raise BoundaryError("ACTION_RECEIPT_EVIDENCE_INVALID")
    return dict(receipt)


def run_single_door(
    *,
    binding: DoorBinding,
    model: str,
    worker_input: str,
    transport: Callable[[Mapping[str, Any]], Mapping[str, Any]],
    bound_action: Callable[[DoorBinding], Mapping[str, Any]],
) -> Dict[str, Any]:
    request = build_worker_request(binding=binding, model=model, worker_input=worker_input)
    response = transport(request)
    if not isinstance(response, Mapping):
        raise BoundaryError("TRANSPORT_RESPONSE_INVALID")
    validate_single_door_response(response)

    # There is exactly one server-side action reference in this invocation:
    # the callable supplied as bound_action. No registry or alternate action
    # lookup exists in this boundary.
    receipt = bound_action(binding)
    if not isinstance(receipt, Mapping):
        raise BoundaryError("BOUND_ACTION_RECEIPT_INVALID")
    return validate_action_receipt(binding, receipt)


def openai_responses_transport(
    request_payload: Mapping[str, Any],
    *,
    api_key: Optional[str] = None,
    endpoint: str = "https://api.openai.com/v1/responses",
    timeout_seconds: int = 120,
) -> Mapping[str, Any]:
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise BoundaryError("OPENAI_API_KEY_MISSING")
    body = json.dumps(request_payload, separators=(",", ":")).encode("utf-8")
    req = urllib.request.Request(
        endpoint,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout_seconds) as resp:
            raw = resp.read()
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise BoundaryError(f"OPENAI_HTTP_ERROR:{exc.code}:{detail[:500]}") from exc
    except urllib.error.URLError as exc:
        raise BoundaryError(f"OPENAI_TRANSPORT_ERROR:{exc.reason}") from exc
    try:
        parsed = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise BoundaryError("OPENAI_RESPONSE_INVALID_JSON") from exc
    if not isinstance(parsed, Mapping):
        raise BoundaryError("OPENAI_RESPONSE_INVALID")
    return parsed


def selfcheck() -> Dict[str, Any]:
    binding = DoorBinding.from_mapping(
        {
            "contract": BOUNDARY_CONTRACT,
            "room_token": "R_TEST",
            "action_token": "A_TEST",
            "receipt_token": "P_TEST",
            "next_room_token": "R_NEXT",
            "input_handles": ["I_TEST"],
        }
    )
    request = build_worker_request(binding=binding, model="gpt-5.6-sol", worker_input="opaque-test")
    assert_single_door_request(request)
    return {
        "ok": True,
        "status": "H0S_SINGLE_DOOR_BOUNDARY_IMPLEMENTED",
        "contract": BOUNDARY_CONTRACT,
        "tool_count": len(request["tools"]),
        "forced_tool": request["tool_choice"],
        "parallel_tool_calls": request["parallel_tool_calls"],
        "content_semantics_authority": "NONE",
    }


def main(argv: Iterable[str]) -> int:
    args = list(argv)
    if args == ["selfcheck"]:
        print(json.dumps(selfcheck(), ensure_ascii=False, indent=2))
        return 0
    print("usage: single_door_boundary.py selfcheck", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
