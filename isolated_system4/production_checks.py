from __future__ import annotations

"""System 4 production checks plus the central repair-owner classification layer.

The real LT/PPM execution engine is byte-identical to the previous production_checks.py
and lives in production_checks_engine.py.  This module adds only the semantic routing
contract.  Callers keep importing `production_checks`, so there is one public authority.
"""

from typing import Any, Mapping
import production_checks_engine as _engine


# Owner names are the machine/worker authorities from the System-4A repair contract.
DRAFT_WORKER = "DRAFT_WORKER"
PARENT_TITLE_MACHINE = "PARENT_TITLE_MACHINE"
PARENT_CATEGORY_MACHINE = "PARENT_CATEGORY_MACHINE"
PARENT_ARTICLE_TYPE_MACHINE = "PARENT_ARTICLE_TYPE_MACHINE"
PARENT_KEYWORD_MACHINE = "PARENT_KEYWORD_MACHINE"
PARENT_SLOT_MACHINE = "PARENT_SLOT_MACHINE"
PORTAL_LINK_MACHINE = "PORTAL_LINK_MACHINE"
CONTEXT_WORKER = "CONTEXT_WORKER"
HARD_BLOCK = "HARD_BLOCK"


def _text(value: Any) -> str:
    return str(value or "").strip()


def _ppm_repair_owner(node: Mapping[str, Any]) -> str:
    """Classify the producing owner from semantics, not an exact historical-code list.

    Order is deliberate: concrete artifact/field beats validator wording; failed-rule
    semantics beat error-family fallback.  Anything not safely classifiable stays hard.
    """
    field = _text(node.get("field_path")).casefold()
    rule = _text(node.get("failed_rule")).casefold()
    code = _text(node.get("error_code")).upper()
    reason = _text(node.get("reason")).casefold()

    # 1. Concrete artifact/field ownership.
    if field:
        if any(token in field for token in ("body_html", "body_text", "content_html", "article_text", "draft")):
            return DRAFT_WORKER
        if "title" in field or "headline" in field:
            return PARENT_TITLE_MACHINE
        if "category" in field:
            return PARENT_CATEGORY_MACHINE
        if "article_type" in field or "article-type" in field:
            return PARENT_ARTICLE_TYPE_MACHINE
        if "target_keyword" in field or "keyword" in field:
            return PARENT_KEYWORD_MACHINE
        if "slot" in field:
            return PARENT_SLOT_MACHINE
        if "link" in field or "url" in field or "href" in field:
            return PORTAL_LINK_MACHINE
        if "context" in field or "fact_pack" in field or "production_plan" in field:
            return CONTEXT_WORKER

    # 2. Validator-rule semantics when a field is absent.
    combined = " ".join((rule, reason))
    if any(token in combined for token in ("known_regression_pattern", "conclusion", "fazit", "word minimum", "word_minimum", "structure", "article content", "article text")):
        return DRAFT_WORKER
    if "title" in combined or "headline" in combined:
        return PARENT_TITLE_MACHINE
    if "category" in combined:
        return PARENT_CATEGORY_MACHINE
    if "article type" in combined or "article_type" in combined:
        return PARENT_ARTICLE_TYPE_MACHINE
    if "keyword" in combined:
        return PARENT_KEYWORD_MACHINE
    if "slot" in combined:
        return PARENT_SLOT_MACHINE
    if "link" in combined or "href" in combined or "url" in combined:
        return PORTAL_LINK_MACHINE

    # 3. Stable semantic families. These are families, never exact one-off symptoms.
    # KNOWN_REGRESSION is defined by the PPM as a known article-content regression class.
    if code.startswith("BLOCKED_KNOWN_REGRESSION_"):
        return DRAFT_WORKER
    if code.startswith(("BLOCKED_CONTENT_", "BLOCKED_WAVE2_")):
        return DRAFT_WORKER
    if code.startswith("BLOCKED_CANONICAL_RUNTIME_LINK_"):
        return PORTAL_LINK_MACHINE

    return HARD_BLOCK


def _ppm_repair_findings(value: Any) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []

    def add(code: Any, node: Mapping[str, Any]) -> None:
        error_code = _text(code)
        if not error_code:
            return
        probe = dict(node)
        probe["error_code"] = error_code
        owner = _ppm_repair_owner(probe)
        if owner == HARD_BLOCK:
            return
        findings.append({
            "error_code": error_code,
            "failed_rule": node.get("failed_rule"),
            "field_path": node.get("field_path"),
            "expected": node.get("expected"),
            "actual": node.get("actual"),
            "reason": node.get("reason"),
            "validator_id": node.get("validator_id"),
            "repair_owner": owner,
        })

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            add(node.get("error_code"), node)
            for key in ("reason_codes", "errors"):
                values = node.get(key)
                if isinstance(values, list):
                    for code in values:
                        if isinstance(code, str):
                            add(code, node)
            for child in node.values():
                walk(child)
        elif isinstance(node, list):
            for child in node:
                walk(child)

    walk(value)
    unique: list[dict[str, Any]] = []
    seen: set[str] = set()
    import json
    for item in findings:
        key = json.dumps(item, ensure_ascii=False, sort_keys=True, default=str)
        if key not in seen:
            seen.add(key)
            unique.append(item)
    return unique


# Patch the byte-identical execution engine at its single repair-classification seam.
# Functions defined in that module resolve this global at runtime, so real LT/PPM execution
# remains untouched while all callers receive the central owner decision.
_engine._ppm_repair_findings = _ppm_repair_findings

# Re-export the real production engine as the single public module API.
for _name in dir(_engine):
    if not _name.startswith("__") and _name != "_ppm_repair_findings":
        globals()[_name] = getattr(_engine, _name)
