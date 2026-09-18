from __future__ import annotations

"""System 4 production checks plus the central repair-owner classification layer.

The real LT/PPM execution engine is byte-identical to the previous production_checks.py
and lives in production_checks_engine.py. This module adds only the semantic routing
contract. Callers keep importing `production_checks`, so there is one public authority.
"""

from typing import Any, Mapping
import block_semantics
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

    # Exact integrity / execution contracts are never writer-repairable. These
    # faults mean that the checker input or its bound machine contract is invalid.
    hard_codes = {
        "BLOCKED_WAVE2_CONTRACT_MISSING",
        "BLOCKED_WAVE2_QUALITY_BINDING_MISSING",
        "BLOCKED_WAVE2_QUALITY_BINDING_HASH",
        "BLOCKED_WAVE2_INTERNAL_MARKER_MISSING",
        "BLOCKED_WAVE2_LINK_REGISTRY_HASH",
        "BLOCKED_MAINBLOCK1_LANGUAGE_DELTA_EVIDENCE",
        "BLOCKED_WAVE2_LANGUAGE_EVIDENCE",
        "BLOCKED_VALIDATION_CONTRACT_VERSION_MISSING",
        "BLOCKED_SECTION_REQUIREMENTS_HASH_MISMATCH",
        "BLOCKED_VALIDATION_CONTRACT_VERSION_UNKNOWN",
        "BLOCKED_CONTENT_TYPE_DEFINITION_MISSING",
        "BLOCKED_CONTENT_HASH_MISMATCH",
        "BLOCKED_KNOWN_ERROR_CONTRACT_MISSING",
    }
    if code in hard_codes:
        return HARD_BLOCK

    # PPM diagnostics normally prefix bound plan fields with ``item.``. Owner
    # classification is about the artifact itself, so normalise only that wrapper.
    scoped_field = field[5:] if field.startswith("item.") else field

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
    if scoped_field:
        if scoped_field in {"content.title", "canonical_article.title", "article.title", "production_plan.title", "runtime_order.title"} or scoped_field.endswith(".headline"):
            return PARENT_TITLE_MACHINE
        if scoped_field.startswith(("quality_binding.wordpress_category", "wordpress_category", "article.category", "production_plan.category")):
            return PARENT_CATEGORY_MACHINE
        if scoped_field in {"canonical_article.article_type", "article.article_type", "production_plan.article_type", "runtime_order.article_type"}:
            return PARENT_ARTICLE_TYPE_MACHINE
        if scoped_field in {"production_plan.target_keyword", "article.target_keyword", "runtime_order.target_keyword"}:
            return PARENT_KEYWORD_MACHINE
        if scoped_field in {"production_plan.slot", "production_plan.plan_slot", "article.plan_slot", "plan_slot"}:
            return PARENT_SLOT_MACHINE
        if scoped_field.startswith(("quality_binding.link_bindings", "quality_binding.portal_link_registry", "runtime_order.links", "canonical_article.link_binding", "production_plan.link")):
            return PORTAL_LINK_MACHINE
        if any(token in scoped_field for token in ("body_html", "body_text", "content_html", "article_text", "draft")):
            return DRAFT_WORKER
        if scoped_field.startswith(("production_context", "fact_pack", "production_plan.fact")):
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
    if code.startswith("BLOCKED_KNOWN_"):
        return DRAFT_WORKER
    if code.startswith(("BLOCKED_CONTENT_", "BLOCKED_WAVE2_")):
        return DRAFT_WORKER

    return HARD_BLOCK


def guard_repair_finding(checker: str, error: Any) -> dict[str, Any] | None:
    """Classify System-4 guard findings without weakening integrity/security blocks."""
    checker = _text(checker).casefold()
    code = _text(error)
    base = code.split(":", 1)[0].upper()

    if checker == "content_guard":
        if base in {"ARTICLE_UNKNOWN_FACT_ID", "ARTICLE_FACT_TRACE_MISSING"}:
            return {"error_code": code, "repair_owner": DRAFT_WORKER, "validator_id": "content_guard"}
        return None

    if checker == "design_guard":
        repairable = {
            "DESIGN_BODY_EMPTY",
            "DESIGN_CANONICAL_ARTICLE_ROOT_MISSING",
            "DESIGN_PPM_GENERATED_CLASS_MISSING",
            "DESIGN_ARTICLE_TYPE_CLASS_MISSING",
            "DESIGN_ARTICLE_TYPE_ATTRIBUTE_MISMATCH",
            "DESIGN_NESTED_ARTICLE_FORBIDDEN",
            "DESIGN_TABLE_SYSTEM129_CLASS_MISSING",
            "DESIGN_TABLE_COMPARISON_CLASS_MISSING",
            "DESIGN_BERATUNG_HEADING_LEVEL_FORBIDDEN",
        }
        if base in repairable:
            return {"error_code": code, "repair_owner": DRAFT_WORKER, "validator_id": "design_guard"}
        return None

    return None


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


def run_all(repo, state, fact_pack, production_plan_item):
    article_html = str(state.get("draft_markdown") or "")
    contract = state.get("authoring_contract") if isinstance(state.get("authoring_contract"), Mapping) else {}
    try:
        semantic_evidence = block_semantics.validate(article_html, contract)
    except block_semantics.BlockSemanticRepairRequired as exc:
        raise _engine.RepairRequired("block_semantics", exc.findings) from exc
    except block_semantics.BlockSemanticError as exc:
        raise _engine.ProductionCheckError("BLOCK_SEMANTIC_AUTHORITY_FAIL:" + str(exc)) from exc

    result = _engine.run_all(repo, state, fact_pack, production_plan_item)
    if isinstance(result, dict):
        result = dict(result)
        evidence = result.get("evidence")
        if isinstance(evidence, dict):
            evidence = dict(evidence)
            evidence["block_semantics"] = semantic_evidence
            result["evidence"] = evidence
        else:
            result["block_semantics"] = semantic_evidence
    return result


for _name in dir(_engine):
    if not _name.startswith("__") and _name not in {"_ppm_repair_findings", "run_all"}:
        globals()[_name] = getattr(_engine, _name)
