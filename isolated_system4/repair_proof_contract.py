from __future__ import annotations

import hashlib
import re
from typing import Any, Mapping

PROOF_BLOCKED = "REPAIR_PROOF_BLOCKED"
ROUTING_PROVEN = "REPAIR_ROUTING_PROVEN"
REAL_CODEX_PROVEN = "REAL_CODEX_REPAIR_PROVEN"
QUALITY_REFERENCE_CONTRACT = "SYSTEM4_HUMAN_TEXT_QUALITY_REFERENCE_V1"
_SHA256 = re.compile(r"^[0-9a-f]{64}$")


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def validate_quality_reference(body: str, metadata: Mapping[str, Any]) -> dict[str, Any]:
    if metadata.get("contract") != QUALITY_REFERENCE_CONTRACT:
        raise ValueError("QUALITY_REFERENCE_CONTRACT_INVALID")
    actual_sha = sha256_text(body)
    expected_sha = str(metadata.get("article_sha256") or "").lower().strip()
    if not _SHA256.fullmatch(expected_sha) or actual_sha != expected_sha:
        raise ValueError("QUALITY_REFERENCE_SHA256_MISMATCH")
    if metadata.get("content_quality_user_approved") is not True:
        raise ValueError("QUALITY_REFERENCE_USER_APPROVAL_MISSING")
    if metadata.get("approval_scope") != "CONTENT_ONLY":
        raise ValueError("QUALITY_REFERENCE_SCOPE_INVALID")
    for field in (
        "structural_compliance_claimed",
        "fullcheck_pass_claimed",
        "production_pass_claimed",
        "allowed_as_repair_fixture",
        "allowed_as_fullcheck_pass_fixture",
        "allowed_as_production_article",
    ):
        if metadata.get(field) is not False:
            raise ValueError("QUALITY_REFERENCE_MUST_NOT_CLAIM_" + field.upper())
    if int(metadata.get("word_count") or -1) != len(body.split()):
        raise ValueError("QUALITY_REFERENCE_WORD_COUNT_MISMATCH")
    if int(metadata.get("byte_count") or -1) != len(body.encode("utf-8")):
        raise ValueError("QUALITY_REFERENCE_BYTE_COUNT_MISMATCH")
    if int(metadata.get("line_count") or -1) != body.count("\n") + 1:
        raise ValueError("QUALITY_REFERENCE_LINE_COUNT_MISMATCH")
    return {
        "contract": QUALITY_REFERENCE_CONTRACT,
        "article_sha256": actual_sha,
        "content_quality_reference": "USER_APPROVED_POSITIVE_REFERENCE",
        "structural_compliance": "NOT_ASSERTED",
        "fullcheck_status": "NOT_ASSERTED",
        "production_pass": False,
    }


def classify_repair_proof(evidence: Mapping[str, Any]) -> dict[str, Any]:
    routing_fields = ("repair_routing_proven", "same_article_repair", "recheck_executed")
    routing_proven = all(evidence.get(field) is True for field in routing_fields)

    required_real = {
        "worker": evidence.get("worker") == "CODEX_CLOUD",
        "codex_used": evidence.get("codex_used") is True,
        "mocks_used": evidence.get("mocks_used") is False,
        "prepared_final_fixture_used": evidence.get("prepared_final_fixture_used") is False,
        "pre_repair_sha256": bool(_SHA256.fullmatch(str(evidence.get("pre_repair_sha256") or ""))),
        "post_repair_sha256": bool(_SHA256.fullmatch(str(evidence.get("post_repair_sha256") or ""))),
        "findings_sha256": bool(_SHA256.fullmatch(str(evidence.get("findings_sha256") or ""))),
        "durable_before_ref": bool(str(evidence.get("durable_before_ref") or "").strip()),
        "durable_after_ref": bool(str(evidence.get("durable_after_ref") or "").strip()),
        "durable_findings_ref": bool(str(evidence.get("durable_findings_ref") or "").strip()),
        "fullcheck_status": evidence.get("fullcheck_status") == "PASS",
        "languagetool_status": evidence.get("languagetool_status") == "PASS",
        "ppm_status": evidence.get("ppm_status") == "PASS",
        "ppm_content_quality_status": evidence.get("ppm_content_quality_status") == "CONTENT_QUALITY_CHECK_OK",
    }
    try:
        pre_revision = int(evidence.get("pre_revision"))
        post_revision = int(evidence.get("post_revision"))
        required_real["revision_advanced"] = pre_revision >= 1 and post_revision > pre_revision
    except (TypeError, ValueError):
        required_real["revision_advanced"] = False

    before_sha = str(evidence.get("pre_repair_sha256") or "")
    after_sha = str(evidence.get("post_repair_sha256") or "")
    required_real["article_changed"] = (
        required_real["pre_repair_sha256"]
        and required_real["post_repair_sha256"]
        and before_sha != after_sha
    )

    missing = sorted(name for name, ok in required_real.items() if not ok)
    real_codex = routing_proven and not missing
    if real_codex:
        level = REAL_CODEX_PROVEN
    elif routing_proven:
        level = ROUTING_PROVEN
    else:
        level = PROOF_BLOCKED

    return {
        "repair_proof_level": level,
        "repair_routing_proven": routing_proven,
        "real_codex_repair_proven": real_codex,
        "missing_real_codex_evidence": missing,
    }
