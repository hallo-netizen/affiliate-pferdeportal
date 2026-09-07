#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]

def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod

def expect_block(fn, token: str):
    try:
        fn()
    except Exception as exc:
        assert token in str(exc), (token, str(exc))
        return
    raise AssertionError("expected block: " + token)

entry = load(HERE / "project_single_door_entry_v2.py", "h8_test_entry")
boot = load(HERE / "single_door_bootstrap.py", "h8_test_boot")
prov = load(HERE / "preproduction_provenance_guard.py", "h8_test_prov")

# 1. Pending state without an incoming package must enter the bootstrap door.
real = entry.resolve_entry(
    repo=REPO,
    runtime_provider=lambda repo: {"status": "READY_WAITING_PACKAGE", "generation": 999999},
)
assert real["status"] == "PREPRODUCTION_BOOTSTRAP_SINGLE_DOOR_REQUIRED", real
assert real["room_token"] == "R_BOOT_001"
assert real["worker_request"]["input"] == "R_BOOT_001"
assert len(real["worker_request"]["tools"]) == 1
assert real["worker_request"]["parallel_tool_calls"] is False

# 2. Idle remains inert.
idle = entry.resolve_entry(repo=REPO, runtime_provider=lambda repo: {"status": "READY_IDLE"})
assert idle["status"] == "PROJECT_ARMED_NO_ACTIVE_BATCH" and idle["worker_request"] is None

# 3. A provenanced incoming package may advance only to R_PRE.
pre = entry.resolve_entry(
    repo=REPO,
    runtime_provider=lambda repo: {"status": "READY_WAITING_PACKAGE", "generation": 1},
    incoming_provenance_provider=lambda repo: {
        "status": "H8_PREPRODUCTION_PROVENANCE_PASS",
        "bootstrap_authority_sha256": "a" * 64,
    },
)
assert pre["status"] == "PREPRODUCTION_PROVENANCE_PACKAGE_SINGLE_DOOR_REQUIRED"
assert pre["room_token"] == "R_PRE_001"
assert pre["worker_request"]["input"] == "R_PRE_001"
assert len(pre["worker_request"]["tools"]) == 1

# 4. Productive route requires explicit H8 provenance PASS.
productive = entry.resolve_entry(
    repo=REPO,
    runtime_provider=lambda repo: {"status": "RUNTIME_INPUTS_BOUND", "selected_item_count": 7},
    attached_provenance_provider=lambda repo: {
        "status": "H8_PREPRODUCTION_PROVENANCE_PASS",
        "bootstrap_authority_sha256": "b" * 64,
    },
    route_provider=lambda repo, count, model: {
        "room_token": "R_001",
        "worker_request": {"input": "R_001", "tools": [{}]},
    },
    codex_capsule_provider=lambda repo: {"status": "CODEX_CLOUD_BOUND_CAPSULE_PASS"},
)
assert productive["status"] == "PRODUCTIVE_SINGLE_DOOR_READY"
assert productive["room_token"] == "R_001" and productive["item_count"] == 7

# 5. Missing/failed provenance cannot reach R_001.
expect_block(
    lambda: entry.resolve_entry(
        repo=REPO,
        runtime_provider=lambda repo: {"status": "RUNTIME_INPUTS_BOUND", "selected_item_count": 7},
        attached_provenance_provider=lambda repo: {"status": "NOPE"},
        route_provider=lambda repo, count, model: {"room_token": "R_001", "worker_request": {}},
    ),
    "ATTACHED_PACKAGE_PROVENANCE_NOT_PASS",
)

# 6. Old package/release shape without H8 provenance binding is mechanically rejected.
expect_block(lambda: prov._binding_from_release({}), "H8_BOOTSTRAP_PROVENANCE_BINDING_MISSING")

# 7. H8 binding itself is exact-key and hash bound.
expected = prov.expected_binding(REPO)
checked = dict(prov._binding_from_release({"h8_bootstrap_binding": expected}))
assert checked == expected
wrong = dict(expected); wrong["generation"] = int(wrong["generation"]) + 1
expect_block(lambda: prov._binding_from_release({"h8_bootstrap_binding": wrong}), "H8_BOOTSTRAP_PROVENANCE_BINDING_HASH_INVALID")

# 8. Door 0 remains domain blind and exposes only one forced no-argument action.
req = boot.worker_request("gpt-5.6-sol")
assert req["input"] == "R_BOOT_001"
assert len(req["tools"]) == 1
assert req["tools"][0]["parameters"] == {"type": "object", "properties": {}, "required": [], "additionalProperties": False}
assert req["tool_choice"] == {"type": "function", "name": "execute_bound_action"}
assert req["parallel_tool_calls"] is False

print(json.dumps({
    "ok": True,
    "status": "H8_PREPRODUCTION_BOOTSTRAP_POSITIVE_NEGATIVE_PASS",
    "cases": 8,
    "real_current_room": real["room_token"],
    "quality_authority": "NONE",
    "content_semantics_inspected": False,
}, ensure_ascii=False, indent=2))
