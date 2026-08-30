#!/usr/bin/env python3
from __future__ import annotations

import copy
import json

import single_door_boundary as boundary
import single_door_route_binding as route_binding

BATCH_SIZES = (1, 2, 7, 40)


def must_raise(exc_type, fn, contains: str):
    try:
        fn()
    except exc_type as exc:
        if contains not in str(exc):
            raise AssertionError(f"WRONG_ERROR:{exc}")
        return
    raise AssertionError("EXPECTED_EXCEPTION_NOT_RAISED")


def binding_from_view(view):
    return boundary.DoorBinding.from_mapping({
        "contract": boundary.BOUNDARY_CONTRACT,
        "room_token": view["room_token"],
        "action_token": view["action_token"],
        "receipt_token": view["receipt_token"],
        "next_room_token": view["next_room_token"],
        "input_handles": view["input_handles"],
    })


def run():
    routes = {n: route_binding.materialize(n) for n in BATCH_SIZES}
    checks = []

    def ok(name, fn):
        fn()
        checks.append({"name": name, "status": "PASS"})

    def c01():
        for route in routes.values():
            rows = route["rooms"]
            tokens = [r["worker_view"]["room_token"] for r in rows]
            assert len(tokens) == len(set(tokens)) == route["room_count"]
    ok("EACH_ROOM_EXACTLY_ONCE", c01)

    def c02():
        for route in routes.values():
            for row in route["rooms"]:
                ex = row["server_executor"]
                assert set(ex) == {"executor_ref", "operation"}
                assert all(isinstance(ex[k], str) and ex[k] for k in ex)
    ok("EXACTLY_ONE_EXECUTOR_BINDING_PER_ROOM", c02)

    def c03():
        for route in routes.values():
            for row in route["rooms"]:
                assert len(row["worker_view"]["input_handles"]) == 1
    ok("EXACTLY_ONE_INPUT_HANDLE_PER_ROOM", c03)

    def c04():
        for route in routes.values():
            for row in route["rooms"]:
                assert isinstance(row["worker_view"]["receipt_token"], str)
    ok("EXACTLY_ONE_RECEIPT_TOKEN_PER_ROOM", c04)

    def c05():
        for route in routes.values():
            for row in route["rooms"]:
                assert isinstance(row["worker_view"]["next_room_token"], str)
    ok("EXACTLY_ONE_BOUND_NEXT_ROOM_PER_ROOM", c05)

    def c06():
        for route in routes.values():
            known = {r["worker_view"]["room_token"] for r in route["rooms"]}
            for row in route["rooms"]:
                assert row["worker_view"]["next_room_token"] in known
    ok("EVERY_NEXT_ROOM_EXISTS", c06)

    def c07():
        for route in routes.values():
            for row in route["rooms"]:
                token = row["worker_view"]["room_token"]
                req = route_binding.worker_request_for(route, token, model="gpt-5.6-sol", worker_input="opaque")
                assert len(req["tools"]) == 1
                bad = copy.deepcopy(req)
                bad["tools"].append({"type": "function", "name": "second"})
                must_raise(boundary.BoundaryError, lambda b=bad: boundary.assert_single_door_request(b), "EXACTLY_ONE_TOOL_REQUIRED")
    ok("SECOND_CAPABILITY_REJECTED", c07)

    def c08():
        route = routes[7]
        row = route["rooms"][5]
        view = row["worker_view"]
        b = binding_from_view(view)
        wrong_targets = [route["rooms"][0]["worker_view"]["room_token"], route["rooms"][-1]["worker_view"]["room_token"], "R_FAKE"]
        for wrong in wrong_targets:
            if wrong == view["next_room_token"]:
                continue
            receipt = {
                "contract": boundary.BOUNDARY_CONTRACT,
                "room_token": view["room_token"],
                "action_token": view["action_token"],
                "receipt_token": view["receipt_token"],
                "next_room_token": wrong,
                "status": "PASS",
                "evidence": ["negative"],
            }
            must_raise(boundary.BoundaryError, lambda r=receipt: boundary.validate_action_receipt(b, r), "ACTION_RECEIPT_BINDING_MISMATCH:next_room_token")
    ok("BACKTRACK_AND_SIDEJUMP_REJECTED", c08)

    def c09():
        route = routes[7]
        view = route["rooms"][3]["worker_view"]
        b = binding_from_view(view)
        receipt = {
            "contract": boundary.BOUNDARY_CONTRACT,
            "room_token": view["room_token"],
            "action_token": view["action_token"],
            "receipt_token": "P_WRONG",
            "next_room_token": view["next_room_token"],
            "status": "PASS",
            "evidence": ["negative"],
        }
        must_raise(boundary.BoundaryError, lambda: boundary.validate_action_receipt(b, receipt), "ACTION_RECEIPT_BINDING_MISMATCH:receipt_token")
    ok("WRONG_RECEIPT_REJECTED", c09)

    def c10():
        for n, route in routes.items():
            assert route["item_count"] == n
            assert route["room_count"] == 12 + (2 * n)
            by = {r["worker_view"]["room_token"]: r for r in route["rooms"]}
            assert by["R_004"]["worker_view"]["next_room_token"] == "R_D_1_01"
            assert by[f"R_D_{n}_02"]["worker_view"]["next_room_token"] == "R_006"
    ok("VARIABLE_CHAIN_UNIQUE_FOR_MULTIPLE_BATCH_SIZES", c10)

    def c11():
        route = routes[7]
        for row in route["rooms"]:
            view = row["worker_view"]
            b = binding_from_view(view)
            receipt = {
                "contract": boundary.BOUNDARY_CONTRACT,
                "room_token": view["room_token"],
                "action_token": view["action_token"],
                "receipt_token": view["receipt_token"],
                "next_room_token": view["next_room_token"],
                "status": "PASS",
                "evidence": ["positive"],
            }
            accepted = boundary.validate_action_receipt(b, receipt)
            assert accepted["next_room_token"] == view["next_room_token"]
    ok("VALID_RECEIPT_OPENS_ONLY_BOUND_NEXT_ROOM", c11)

    def c12():
        route = routes[7]
        must_raise(route_binding.RouteBindingError, lambda: route_binding.resolve_room(route, "R_UNKNOWN"), "ROOM_NOT_EXACTLY_ONCE")
        bad = copy.deepcopy(route)
        bad["rooms"].append(copy.deepcopy(bad["rooms"][0]))
        token = bad["rooms"][0]["worker_view"]["room_token"]
        must_raise(route_binding.RouteBindingError, lambda: route_binding.resolve_room(bad, token), "ROOM_NOT_EXACTLY_ONCE")
    ok("UNKNOWN_OR_DUPLICATE_ROOM_REJECTED", c12)

    return {
        "contract": "SINGLE_DOOR_H4_MECHANICAL_PROOF_V1",
        "status": "PASS",
        "checks_passed": len(checks),
        "checks_total": 12,
        "batch_sizes": list(BATCH_SIZES),
        "checks": checks,
    }


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
