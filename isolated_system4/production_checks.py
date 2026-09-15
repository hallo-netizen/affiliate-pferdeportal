from __future__ import annotations

"""System 4 production checks plus the central repair-owner classification layer.

The real LT/PPM execution engine is byte-identical to the previous production_checks.py
and lives in production_checks_engine.py. This module adds only the semantic routing
contract. Callers keep importing `production_checks`, so there is one public authority.
"""

from typing import Any, Mapping
import production_checks_engine as _engine


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
    """Return the owner of the defective artifact, fail-closed when ambiguous.

    A validator field path may contain words such as ``title`` or ``category`` inside a
    *rendered article artifact* (for example ``source-title`` or a link role named
    ``parent_category``). Those words must never promote a draft-realisation defect to
    a Parent metadata repair. Artifact scope is therefore resolved before token names.
    """
    field = _text(node.get("field_path")).casefold()
    rule = _text(node.get("failed_rule")).casefold()
    code = _text(node.get("error_code")).upper()
    reason = _text(node.get("reason")).casefold()

    # 1. Rendered article/content artefacts are owned by the writer. Immutable link,
    # metadata and source bindings have already been validated before the draft stage.
    if field.startswith(("content.source_traces", "content.factual_units", "content.links.")):
        return DRAFT_WORKER
    if field in {
        "content.link_blocks",
        "content.links_clustered_at_end",
        "content.duplicate_sentence_ratio",
        "content.heading_intent_terms",
        "content.lists",
        "content.table",
    }:
        return DRAFT_WORKER
    if field.startswith(("content.table.", "content.heading", "content.list", "content.body")):
        return DRAFT_WORKER

    # 2. True parent-owned identity/prewrite artefacts. Match scoped fields, not loose
    # substrings such as source-title or parent_category inside a rendered link path.
    if field:
        if field in {"content.title", "canonical_article.title", "article.title", "production_plan.title", "runtime_order.title"} or field.endswith(".headline"):
            return PARENT_TITLE_MACHINE
        if field.startswith(("quality_binding.wordpress_category", "wordpress_category", "article.category", "production_plan.category")):
            return PARENT_CATEGORY_MACHINE
        if field in {"canonical_article.article_type", "article.article_type", "production_plan.article_type", "runtime_order.article_type"}:
            return PARENT_ARTICLE_TYPE_MACHINE
        if field in {"production_plan.target_keyword", "article.target_keyword", "runtime_order.target_keyword"}:
            return PARENT_KEYWORD_MACHINE
        if field in {"production_plan.slot", "production_plan.plan_slot", "article.plan_slot", "plan_slot"}:
            return PARENT_SLOT_MACHINE
        if field.startswith(("quality_binding.link_bindings", "quality_binding.portal_link_registry", "runtime_order.links", "canonical_article.link_binding", "production_plan.link")):
            return PORTAL_LINK_MACHINE
        if any(token in field for token in ("body_html", "body_text", "content_html", "article_text", "draft")):
            return DRAFT_WORKER
        if field.startswith(("production_context", "fact_pack", "production_plan.fact")):
            return CONTEXT_WORKER

    # 3. Exact semantic rule families only where the artifact path did not already own
    # the decision. The target-keyword/title rule is a parent title defect.
    if code.startswith("BLOCKED_CONTENT_TARGET_KEYWORD_TITLE"):
        return PARENT_TITLE_MACHINE
    if code.startswith("BLOCKED_CANONICAL_RUNTIME_LINK_"):
        return PORTAL_LINK_MACHINE

    combined = " ".join((rule, reason))
    if any(token in combined for token in (
        "known_regression_pattern", "conclusion", "fazit", "word minimum",
        "word_minimum", "article content", "article text", "duplicate sentence",
        "heading intent", "required list", "table value",
    )):
        return DRAFT_WORKER
    if any(token in combined for token in ("target keyword", "title must contain target keyword")):
        return PARENT_TITLE_MACHINE

    # 4. PPM content/wave2 findings are writer-repairable only when no parent/prewrite
    # artifact was identified above. Unknown families remain hard/fail-closed.
    if code.startswith("BLOCKED_KNOWN_REGRESSION_"):
        return DRAFT_WORKER
    if code.startswith(("BLOCKED_CONTENT_", "BLOCKED_WAVE2_", "BLOCKED_KNOWN_LINKS_CLUSTERED_")):
        return DRAFT_WORKER

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


_engine._ppm_repair_findings = _ppm_repair_findings

for _name in dir(_engine):
    if not _name.startswith("__") and _name != "_ppm_repair_findings":
        globals()[_name] = getattr(_engine, _name)
