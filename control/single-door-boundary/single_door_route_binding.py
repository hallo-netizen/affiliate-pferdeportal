#!/usr/bin/env python3
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping, Optional

import single_door_boundary as boundary

HERE = Path(__file__).resolve().parent
H1_PATH = HERE / "H1_TECHNICAL_PRODUCTION_STREET.json"
H2_PATH = HERE / "H2_OPAQUE_ROUTE.json"
ROUTE_CONTRACT = "SINGLE_DOOR_BOUND_ROUTE_V1"
H1_BLOB_SHA = "abab6c01f5be81372e294d079043cdd8596773c5"
H2_BLOB_SHA = "175a8556191d65b89934b296f91a39ee1971ba1f"
BOUNDARY_BLOB_SHA = "13d72055313e70540d872236182df1df07dd0095"


class RouteBindingError(RuntimeError):
    pass


@dataclass(frozen=True)
class ExecutorSpec:
    executor_ref: str
    operation: str


@dataclass(frozen=True)
class BoundRoom:
    ordinal: str
    binding: boundary.DoorBinding
    executor: ExecutorSpec

    def worker_view(self) -> Dict[str, Any]:
        # The worker never receives executor_ref/operation or any route registry.
        return {
            "contract": ROUTE_CONTRACT,
            "room_token": self.binding.room_token,
            "action_token": self.binding.action_token,
            "input_handles": list(self.binding.input_handles),
            "receipt_token": self.binding.receipt_token,
            "next_room_token": self.binding.next_room_token,
        }


def _load(path: Path) -> Mapping[str, Any]:
    obj = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(obj, Mapping):
        raise RouteBindingError("SOURCE_NOT_OBJECT")
    return obj


def _sources() -> tuple[Mapping[str, Any], Mapping[str, Any]]:
    h1 = _load(H1_PATH)
    h2 = _load(H2_PATH)
    if h1.get("contract") != "PFERDE_ATELIER_TECHNICAL_PRODUCTION_STREET_MAP_V1":
        raise RouteBindingError("H1_CONTRACT_INVALID")
    if h2.get("contract") != "SINGLE_DOOR_OPAQUE_ROUTE_V1":
        raise RouteBindingError("H2_CONTRACT_INVALID")
    if h2.get("source_sha") != H1_BLOB_SHA:
        raise RouteBindingError("H2_NOT_BOUND_TO_H1")
    h1_route = h1.get("route")
    h2_route = h2.get("route")
    if not isinstance(h1_route, list) or not isinstance(h2_route, list):
        raise RouteBindingError("ROUTE_MISSING")
    if len(h1_route) != 13 or len(h2_route) != 13:
        raise RouteBindingError("OUTER_ROUTE_COUNT_INVALID")
    return h1, h2


def _executor_from_h1(row: Mapping[str, Any]) -> ExecutorSpec:
    ref = row.get("executor_ref")
    op = row.get("operation")
    if not isinstance(ref, str) or not ref or not isinstance(op, str) or not op:
        raise RouteBindingError("EXECUTOR_BINDING_INVALID")
    return ExecutorSpec(executor_ref=ref, operation=op)


def _door(
    *, room: str, action: str, handle: str, receipt: str, next_room: str
) -> boundary.DoorBinding:
    return boundary.DoorBinding.from_mapping(
        {
            "contract": boundary.BOUNDARY_CONTRACT,
            "room_token": room,
            "action_token": action,
            "receipt_token": receipt,
            "next_room_token": next_room,
            "input_handles": [handle],
        }
    )


def _outer_rows(h1: Mapping[str, Any], h2: Mapping[str, Any]) -> tuple[dict[int, Mapping[str, Any]], dict[int, Mapping[str, Any]]]:
    h1_rows = {int(x["order"]): x for x in h1["route"]}
    h2_rows = {int(x["ordinal"]): x for x in h2["route"]}
    if set(h1_rows) != set(range(1, 14)) or set(h2_rows) != set(range(1, 14)):
        raise RouteBindingError("OUTER_ORDINALS_INVALID")
    return h1_rows, h2_rows


def materialize(item_count: int) -> Dict[str, Any]:
    """Materialize one deterministic route before any room is activated."""
    if not isinstance(item_count, int) or item_count < 1:
        raise RouteBindingError("ITEM_COUNT_INVALID")
    h1, h2 = _sources()
    h1_rows, h2_rows = _outer_rows(h1, h2)
    segment = h2.get("segment")
    if not isinstance(segment, Mapping) or segment.get("anchor_room_token") != "R_005":
        raise RouteBindingError("SEGMENT_BINDING_INVALID")
    if (segment.get("binding_rule") or {}).get("materialize_all_before_activation") is not True:
        raise RouteBindingError("SEGMENT_MUST_PREBIND")

    rooms: list[BoundRoom] = []

    # Outer rooms 1..4. R_004 enters the fully materialized item segment.
    for order in range(1, 5):
        token = h2_rows[order]
        next_room = token["next_room_token"]
        if order == 4:
            next_room = "R_D_1_01"
        if not isinstance(next_room, str):
            raise RouteBindingError(f"NEXT_ROOM_INVALID:{order}")
        rooms.append(
            BoundRoom(
                ordinal=f"O_{order:03d}",
                binding=_door(
                    room=token["room_token"],
                    action=token["action_token"],
                    handle=token["input_handle"],
                    receipt=token["receipt_token"],
                    next_room=next_room,
                ),
                executor=_executor_from_h1(h1_rows[order]),
            )
        )

    # H2 R_005 is an expansion anchor, not a separately activated worker room.
    # H1 order 5 remains exactly one logical production stage, expanded into a
    # prebound execution/checkpoint pair for each already-bound item.
    item_exec = _executor_from_h1(h1_rows[5])
    checkpoint_ref = h1_rows[5].get("checkpoint_guard_ref")
    if not isinstance(checkpoint_ref, str) or not checkpoint_ref:
        raise RouteBindingError("CHECKPOINT_EXECUTOR_INVALID")
    checkpoint_exec = ExecutorSpec(executor_ref=checkpoint_ref, operation="validate")

    for n in range(1, item_count + 1):
        exec_room = f"R_D_{n}_01"
        check_room = f"R_D_{n}_02"
        next_exec = f"R_D_{n + 1}_01" if n < item_count else "R_006"
        rooms.append(
            BoundRoom(
                ordinal=f"D_{n:06d}_01",
                binding=_door(
                    room=exec_room,
                    action=f"A_D_{n}_01",
                    handle=f"I_D_{n}_01",
                    receipt=f"P_D_{n}_01",
                    next_room=check_room,
                ),
                executor=item_exec,
            )
        )
        rooms.append(
            BoundRoom(
                ordinal=f"D_{n:06d}_02",
                binding=_door(
                    room=check_room,
                    action=f"A_D_{n}_02",
                    handle=f"I_D_{n}_02",
                    receipt=f"P_D_{n}_02",
                    next_room=next_exec,
                ),
                executor=checkpoint_exec,
            )
        )

    # Outer rooms 6..13. H1 already binds the final rearm from 107008 back to
    # the permanent 107007 entry; therefore the final concrete successor is
    # the existing first room R_001, not a new route.
    for order in range(6, 14):
        token = h2_rows[order]
        next_room: Optional[str] = token.get("next_room_token")
        if order == 13:
            final_rearm = h1.get("final_rearm") or {}
            if final_rearm.get("from_step") != 107008 or final_rearm.get("to_step") != 107007:
                raise RouteBindingError("FINAL_REARM_SOURCE_INVALID")
            next_room = h2.get("first_room_token")
        if not isinstance(next_room, str):
            raise RouteBindingError(f"NEXT_ROOM_INVALID:{order}")
        rooms.append(
            BoundRoom(
                ordinal=f"O_{order:03d}",
                binding=_door(
                    room=token["room_token"],
                    action=token["action_token"],
                    handle=token["input_handle"],
                    receipt=token["receipt_token"],
                    next_room=next_room,
                ),
                executor=_executor_from_h1(h1_rows[order]),
            )
        )

    by_room = {r.binding.room_token: r for r in rooms}
    if len(by_room) != len(rooms):
        raise RouteBindingError("DUPLICATE_ROOM_TOKEN")
    for room in rooms:
        if room.binding.next_room_token not in by_room:
            raise RouteBindingError(f"UNBOUND_NEXT_ROOM:{room.binding.room_token}")

    return {
        "contract": ROUTE_CONTRACT,
        "h1_blob_sha": H1_BLOB_SHA,
        "h2_blob_sha": H2_BLOB_SHA,
        "boundary_blob_sha": BOUNDARY_BLOB_SHA,
        "item_count": item_count,
        "first_room_token": h2["first_room_token"],
        "room_count": len(rooms),
        "rooms": [
            {
                "ordinal": r.ordinal,
                "worker_view": r.worker_view(),
                "server_executor": {
                    "executor_ref": r.executor.executor_ref,
                    "operation": r.executor.operation,
                },
            }
            for r in rooms
        ],
        "all_other_actions": "DENY",
    }


def resolve_room(route: Mapping[str, Any], room_token: str) -> Mapping[str, Any]:
    rows = route.get("rooms")
    if not isinstance(rows, list):
        raise RouteBindingError("BOUND_ROOMS_MISSING")
    hits = [r for r in rows if isinstance(r, Mapping) and (r.get("worker_view") or {}).get("room_token") == room_token]
    if len(hits) != 1:
        raise RouteBindingError("ROOM_NOT_EXACTLY_ONCE")
    return hits[0]


def worker_request_for(route: Mapping[str, Any], room_token: str, *, model: str, worker_input: str) -> Dict[str, Any]:
    row = resolve_room(route, room_token)
    view = row["worker_view"]
    binding = boundary.DoorBinding.from_mapping(
        {
            "contract": boundary.BOUNDARY_CONTRACT,
            "room_token": view["room_token"],
            "action_token": view["action_token"],
            "receipt_token": view["receipt_token"],
            "next_room_token": view["next_room_token"],
            "input_handles": view["input_handles"],
        }
    )
    return boundary.build_worker_request(binding=binding, model=model, worker_input=worker_input)


def main(argv: Iterable[str]) -> int:
    args = list(argv)
    if len(args) == 2 and args[0] == "materialize":
        route = materialize(int(args[1]))
        print(json.dumps(route, ensure_ascii=False, indent=2))
        return 0
    print("usage: single_door_route_binding.py materialize ITEM_COUNT")
    return 2


if __name__ == "__main__":
    import sys
    raise SystemExit(main(sys.argv[1:]))
