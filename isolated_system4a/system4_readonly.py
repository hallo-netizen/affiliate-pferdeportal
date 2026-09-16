from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

from realcase_acceptance_gate import assert_no_prebound_production_fields, RealcaseAcceptanceError
from production_plan_binding import bind_production_plan, ProductionPlanBindingError


class System4ReadOnlyError(RuntimeError):
    pass


def _text_sha(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _load_system4_modules():
    repo = Path(__file__).resolve().parent.parent
    system4 = repo / "isolated_system4"
    if not system4.is_dir():
        raise System4ReadOnlyError("SYSTEM4_DIRECTORY_MISSING")
    path = str(system4)
    if path not in sys.path:
        sys.path.insert(0, path)
    import batch_repetition_guard  # type: ignore
    import content_guard  # type: ignore
    import design_guard  # type: ignore
    import production_checks  # type: ignore
    return repo, content_guard, design_guard, production_checks, batch_repetition_guard


class System4ReadOnlyChecks:
    """Thin adapter only. It contains no Pferde-Atelier fach/design/quality rules.

    Every substantive decision is delegated to the existing System-4 modules from the
    current comparison base. System 4A may sequence these calls, but may not replace,
    relax, normalize or reinterpret them.
    """

    def __init__(self):
        (
            self.repo,
            self.content_guard,
            self.design_guard,
            self.production_checks,
            self.batch_repetition_guard,
        ) = _load_system4_modules()

    def research(self, research_text: str) -> dict[str, Any]:
        try:
            normalized = self.content_guard.validate_research_document(research_text)
        except self.content_guard.ContentGuardError as exc:
            raise System4ReadOnlyError("RESEARCH_BLOCK:" + str(exc)) from exc
        return {"status": "PASS", "sha256": _text_sha(research_text), "normalized": normalized}

    def facts(self, facts_text: str, research_text: str) -> dict[str, Any]:
        try:
            normalized = self.content_guard.validate_facts_document(facts_text, research_text)
        except self.content_guard.ContentGuardError as exc:
            raise System4ReadOnlyError("FACTS_BLOCK:" + str(exc)) from exc
        return {"status": "PASS", "sha256": _text_sha(facts_text), "normalized": normalized}

    def context(
        self,
        context_text: str,
        *,
        article: Mapping[str, Any],
        source_snapshot_sha256: str,
        research_text: str,
        facts_text: str,
    ) -> dict[str, Any]:
        try:
            payload = json.loads(context_text)
        except Exception as exc:
            raise System4ReadOnlyError("CONTEXT_JSON_INVALID") from exc
        if not isinstance(payload, dict) or set(payload) != {"fact_pack", "production_plan_item"}:
            raise System4ReadOnlyError("CONTEXT_SCHEMA_INVALID")
        fact_pack = payload["fact_pack"]
        production_plan_item = payload["production_plan_item"]
        if not isinstance(fact_pack, dict) or not isinstance(production_plan_item, dict):
            raise System4ReadOnlyError("CONTEXT_OBJECT_REQUIRED")
        try:
            assert_no_prebound_production_fields(payload)
        except RealcaseAcceptanceError as exc:
            raise System4ReadOnlyError("CONTEXT_REALCASE_BLOCK:" + str(exc)) from exc
        try:
            production_plan_item = bind_production_plan(article, production_plan_item, fact_pack)
        except ProductionPlanBindingError as exc:
            raise System4ReadOnlyError("CONTEXT_BINDING_BLOCK:" + str(exc)) from exc
        state_view = {
            "article": dict(article),
            "source_snapshot_sha256": source_snapshot_sha256,
        }
        try:
            self.content_guard.validate_fact_pack(fact_pack, research_text, facts_text)
            self.production_checks.validate_bound_context(state_view, fact_pack, production_plan_item)
        except self.content_guard.ContentGuardError as exc:
            raise System4ReadOnlyError("CONTEXT_CONTENT_BLOCK:" + str(exc)) from exc
        except self.production_checks.ProductionCheckError as exc:
            raise System4ReadOnlyError("CONTEXT_PRODUCTION_BLOCK:" + str(exc)) from exc
        return {
            "status": "PASS",
            "sha256": _text_sha(context_text),
            "fact_pack": fact_pack,
            "production_plan_item": production_plan_item,
        }

    def draft(self, draft: str, *, article_type: str, fact_pack: Mapping[str, Any]) -> dict[str, Any]:
        try:
            content = self.content_guard.validate_single_article(draft, fact_pack)
            design = self.design_guard.validate_design_neutrality(draft, article_type)
        except self.content_guard.ContentGuardError as exc:
            raise System4ReadOnlyError("DRAFT_CONTENT_BLOCK:" + str(exc)) from exc
        except self.design_guard.DesignGuardError as exc:
            raise System4ReadOnlyError("DRAFT_DESIGN_BLOCK:" + str(exc)) from exc
        return {"status": "PASS", "sha256": _text_sha(draft), "content": content, "design": design}

    def repair(self, old_draft: str, new_draft: str, *, article_type: str, fact_pack: Mapping[str, Any]) -> dict[str, Any]:
        try:
            continuity = self.content_guard.validate_repair_continuity(old_draft, new_draft)
            content = self.content_guard.validate_single_article(new_draft, fact_pack)
            design = self.design_guard.validate_design_neutrality(new_draft, article_type)
        except self.content_guard.ContentGuardError as exc:
            raise System4ReadOnlyError("REPAIR_CONTENT_BLOCK:" + str(exc)) from exc
        except self.design_guard.DesignGuardError as exc:
            raise System4ReadOnlyError("REPAIR_DESIGN_BLOCK:" + str(exc)) from exc
        return {
            "status": "PASS",
            "sha256": _text_sha(new_draft),
            "continuity": continuity,
            "content": content,
            "design": design,
        }

    def fullcheck(
        self,
        draft: str,
        *,
        article: Mapping[str, Any],
        source_snapshot_sha256: str,
        fact_pack: Mapping[str, Any],
        production_plan_item: Mapping[str, Any],
    ) -> dict[str, Any]:
        draft_sha = _text_sha(draft)
        state_view = {
            "article": dict(article),
            "source_snapshot_sha256": source_snapshot_sha256,
            "draft_markdown": draft,
            "draft_sha256": draft_sha,
        }
        try:
            # Same fail-closed preconditions used by current System 4.
            self.content_guard.validate_single_article(draft, fact_pack)
            self.design_guard.validate_design_neutrality(draft, str(article["article_type"]))
            evidence = self.production_checks.run_all(
                self.repo, state_view, fact_pack, production_plan_item
            )
        except self.production_checks.RepairRequired as exc:
            return {
                "status": "FAIL",
                "checked_sha256": draft_sha,
                "checker": exc.checker,
                "findings": list(exc.findings),
            }
        except self.content_guard.ContentGuardError as exc:
            raise System4ReadOnlyError("FULLCHECK_CONTENT_HARD_BLOCK:" + str(exc)) from exc
        except self.design_guard.DesignGuardError as exc:
            raise System4ReadOnlyError("FULLCHECK_DESIGN_HARD_BLOCK:" + str(exc)) from exc
        except self.production_checks.ProductionCheckError as exc:
            raise System4ReadOnlyError("FULLCHECK_PRODUCTION_HARD_BLOCK:" + str(exc)) from exc
        return {
            "status": "PASS",
            "checked_sha256": draft_sha,
            "evidence": evidence,
        }

    def batch(self, bodies: Sequence[str]) -> dict[str, Any]:
        try:
            distinctness = self.content_guard.validate_batch_distinctness(bodies)
            repetition = self.batch_repetition_guard.validate_batch_repetition(bodies)
        except self.content_guard.ContentGuardError as exc:
            raise System4ReadOnlyError("BATCH_CONTENT_BLOCK:" + str(exc)) from exc
        except self.batch_repetition_guard.BatchRepetitionError as exc:
            raise System4ReadOnlyError("BATCH_REPETITION_BLOCK:" + str(exc)) from exc
        return {"status": "PASS", "distinctness": distinctness, "repetition": repetition}
