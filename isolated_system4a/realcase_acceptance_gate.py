from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping

REALCASE_CONTRACT = "SYSTEM4A_REALCASE_ACCEPTANCE_V1"
EXPECTED_ROOT_ENTRY = "isolated_system4/root_entry.py:start-stdin"
EXPECTED_WORKER_ENTRY = "isolated_system4a.codex_worker_entry.build_codex_production_worker_pool"
EXPECTED_CHECKER_ENTRY = "isolated_system4a.system4_readonly.System4ReadOnlyChecks"
EXPECTED_HANDOFF = "SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2"
LT_SHA256 = "2122882e800d312a0543d895c56c0a84a9bb131c9b9846efd8fc033129353ae8"
PPM_SHA256 = "acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1"


class RealcaseAcceptanceError(RuntimeError):
    pass


def _require(ok: bool, code: str) -> None:
    if not ok:
        raise RealcaseAcceptanceError(code)


def canonical_sha(value: Mapping[str, Any]) -> str:
    raw = json.dumps(dict(value), ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def assert_no_prebound_production_fields(context: Mapping[str, Any]) -> None:
    """Acceptance starts before production binding. Pre-bound PPM authority is forbidden."""
    _require(isinstance(context, Mapping), "REALCASE_CONTEXT_OBJECT_REQUIRED")
    plan = context.get("production_plan_item")
    _require(isinstance(plan, Mapping), "REALCASE_PLAN_OBJECT_REQUIRED")
    forbidden = [key for key in ("quality_binding", "quality_binding_hash") if key in plan]
    _require(not forbidden, "REALCASE_PREBOUND_PRODUCTION_FIELD_FORBIDDEN:" + ",".join(forbidden))


def assert_equivalence(test: Mapping[str, Any], real: Mapping[str, Any]) -> dict[str, Any]:
    """Hard 1:1 acceptance identity. No semantic/approximate equivalence exists."""
    _require(test.get("contract") == REALCASE_CONTRACT, "TEST_REALCASE_CONTRACT_INVALID")
    _require(real.get("contract") == REALCASE_CONTRACT, "REAL_REALCASE_CONTRACT_INVALID")
    keys = (
        "raw_input_sha256",
        "root_entry",
        "plan_builder",
        "worker_entry",
        "checker_entry",
        "lt_sha256",
        "ppm_sha256",
        "handoff_contract",
    )
    mismatches = [key for key in keys if test.get(key) != real.get(key)]
    _require(not mismatches, "REALCASE_IDENTITY_MISMATCH:" + ",".join(mismatches))
    _require(test.get("root_entry") == EXPECTED_ROOT_ENTRY, "REALCASE_ROOT_ENTRY_NOT_CANONICAL")
    _require(test.get("worker_entry") == EXPECTED_WORKER_ENTRY, "REALCASE_WORKER_ENTRY_NOT_CANONICAL")
    _require(test.get("checker_entry") == EXPECTED_CHECKER_ENTRY, "REALCASE_CHECKER_ENTRY_NOT_CANONICAL")
    _require(test.get("lt_sha256") == LT_SHA256, "REALCASE_LT_HASH_INVALID")
    _require(test.get("ppm_sha256") == PPM_SHA256, "REALCASE_PPM_HASH_INVALID")
    _require(test.get("handoff_contract") == EXPECTED_HANDOFF, "REALCASE_HANDOFF_NOT_CANONICAL")
    _require(test.get("plan_builder") == "RUNTIME_FROM_RAW_INPUT", "REALCASE_PLAN_BUILDER_NOT_RUNTIME")
    return {"status": "REALCASE_EQUIVALENCE_PASS", "identity_sha256": canonical_sha(test)}
