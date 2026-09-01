#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
ENTRY = HERE / "project_single_door_entry_v2.py"

spec = importlib.util.spec_from_file_location("project_entry_v2_codex_bridge_test", ENTRY)
if spec is None or spec.loader is None:
    raise SystemExit("ENTRY_IMPORT_FAILED")
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)


def must_block(fn, token: str) -> None:
    try:
        fn()
    except Exception as exc:
        if token not in str(exc):
            raise AssertionError((token, str(exc)))
        return
    raise AssertionError("EXPECTED_BLOCK:" + token)


def runtime(_repo: Path):
    return {"status": "RUNTIME_INPUTS_BOUND", "selected_item_count": 7, "generation": 1}


def provenance(_repo: Path):
    return {"status": "H8_PREPRODUCTION_PROVENANCE_PASS", "bootstrap_authority_sha256": "b" * 64}


def route_ok(_repo: Path, count: int, _model: str):
    assert count == 7
    return {"room_token": "R_001", "worker_request": {"legacy": "must-not-be-used"}}


def capsule_ok(_repo: Path):
    return {
        "contract": "PFERDE_ATELIER_CODEX_CLOUD_BOUND_CAPSULE_BRIDGE_V1",
        "status": "CODEX_CLOUD_BOUND_CAPSULE_PASS",
        "authority_mode": "CURRENT_HASH_BOUND_CODEX_CAPSULE_IS_BOUND_ACTION",
        "step_id": "RUN_NEW_ARTICLE_BATCH_NO_STOP",
        "sequence": 107007,
        "navigation_decision": False,
        "content_semantics_inspected": False,
        "quality_authority": "NONE",
        "publish_allowed": False,
    }


def main() -> int:
    out = m.resolve_entry(
        repo=REPO,
        runtime_provider=runtime,
        route_provider=route_ok,
        attached_provenance_provider=provenance,
        codex_capsule_provider=capsule_ok,
    )
    assert out["status"] == "PRODUCTIVE_SINGLE_DOOR_READY"
    assert out["room_token"] == "R_001"
    assert out["worker_request"] is None
    assert out["custom_function_capability_required"] is False
    assert out["authoritative_execution_origin"] == "CODEX_CLOUD_BOUND_CAPSULE_ONLY"
    assert out["codex_bound_action"]["status"] == "CODEX_CLOUD_BOUND_CAPSULE_PASS"
    assert out["workflow_navigation_decision"] is False
    assert out["content_semantics_inspected"] is False
    assert out["quality_authority"] == "NONE"
    assert out["publish_allowed"] is False

    must_block(
        lambda: m.resolve_entry(
            repo=REPO,
            runtime_provider=runtime,
            route_provider=lambda _r, _c, _m: {"room_token": "R_002"},
            attached_provenance_provider=provenance,
            codex_capsule_provider=capsule_ok,
        ),
        "PRODUCTIVE_ROUTE_ENTRY_INVALID",
    )
    must_block(
        lambda: m.resolve_entry(
            repo=REPO,
            runtime_provider=runtime,
            route_provider=route_ok,
            attached_provenance_provider=provenance,
            codex_capsule_provider=lambda _r: {"status": "BLOCKED"},
        ),
        "CODEX_BOUND_CAPSULE_NOT_PASS",
    )

    source = ENTRY.read_text(encoding="utf-8")
    productive = source.split('if status == "RUNTIME_INPUTS_BOUND":', 1)[1]
    assert "worker_request_for(bound" not in productive
    assert '"worker_request": None' in productive
    assert '"custom_function_capability_required": False' in productive

    print(json.dumps({
        "ok": True,
        "status": "H8_CODEX_CLOUD_BOUND_CAPSULE_BRIDGE_POSITIVE_NEGATIVE_PASS",
        "positive": 1,
        "negative": 2,
        "custom_function_capability_required": False,
        "content_semantics_inspected": False,
        "quality_authority": "NONE",
        "publish_allowed": False
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
