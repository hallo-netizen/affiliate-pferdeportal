import hashlib
import json
import unittest
from unittest import mock

from system4_readonly import System4ReadOnlyChecks, System4ReadOnlyError


def sha(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


E1 = "Die konkrete Auswahl richtet sich nach dem tatsächlichen Einsatzzweck und der sicheren Handhabung."
E2 = "Materialzustand und passende Nutzung müssen vor dem Einsatz konkret geprüft werden."
SOURCE_EVIDENCE = E1 + "\n" + E2 + "\nZusätzlicher Quellenkontext für den lokalen Nachweis."
SOURCE_SNAPSHOT = "b" * 64


def research_obj():
    return {
        "contract": "SYSTEM4_RESEARCH_EVIDENCE_V1",
        "sources": [{
            "source_id": "src-official-1",
            "source_title": "Fachquelle – konkrete Anleitung",
            "source_url": "https://example.org/fachquelle",
            "retrieved_at": "2026-09-13T08:00:00Z",
            "snapshot_sha256": sha(SOURCE_EVIDENCE),
            "evidence": SOURCE_EVIDENCE,
        }],
    }


def facts_obj():
    return {
        "contract": "SYSTEM4_FACTS_EVIDENCE_V1",
        "claims": [
            {
                "fact_id": "fact-a",
                "source_id": "src-official-1",
                "statement": "Der Einsatzzweck ist ein konkretes Auswahlkriterium.",
                "evidence_text": E1,
                "evidence_text_sha256": sha(E1),
            },
            {
                "fact_id": "fact-b",
                "source_id": "src-official-1",
                "statement": "Der Materialzustand ist vor der Nutzung zu prüfen.",
                "evidence_text": E2,
                "evidence_text_sha256": sha(E2),
            },
        ],
    }


def fact_pack():
    return {
        "contract": "canonical_fact_pack_v1",
        "status": "SOURCE_VERIFIED_PRODUCTION_READY",
        "source_snapshot_id": SOURCE_SNAPSHOT,
        "fact_pack_id": SOURCE_SNAPSHOT,
        "sources": research_obj()["sources"],
        "claims": facts_obj()["claims"],
    }


def plan_item():
    return {
        "article_type": "Beratung",
        "target_keyword": "Keyword",
        "topic": "Titel",
        "category_binding": {"slug": "kategorie"},
    }


def context_text():
    return json.dumps(
        {"fact_pack": fact_pack(), "production_plan_item": plan_item()},
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def article(extra: str = ""):
    return (
        '<article class="ppm-generated ppm-type-beratung" data-article-type="Beratung">'
        '<section data-block="criteria"><h2>Auswahl</h2>'
        '<p data-fact-ids="fact-a fact-b">Konkreter Artikelinhalt mit belegten Aussagen.</p>'
        '<table class="system-129-table comparison-table">'
        '<tr><th>Kriterium</th><th>Wert</th></tr><tr><td>A</td><td>B</td></tr>'
        '</table>' + extra + '</section></article>'
    )


class ExistingSystem4ReuseTests(unittest.TestCase):
    def setUp(self):
        self.checks = System4ReadOnlyChecks()
        self.research = json.dumps(research_obj(), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        self.facts = json.dumps(facts_obj(), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        self.article_binding = {
            "title": "Titel",
            "target_keyword": "Keyword",
            "category": "kategorie",
            "article_type": "Beratung",
            "plan_slot": "a" * 64,
        }

    def test_existing_research_facts_context_and_design_guards_pass(self):
        self.assertEqual(self.checks.research(self.research)["status"], "PASS")
        self.assertEqual(self.checks.facts(self.facts, self.research)["status"], "PASS")
        context = self.checks.context(
            context_text(),
            article=self.article_binding,
            source_snapshot_sha256=SOURCE_SNAPSHOT,
            research_text=self.research,
            facts_text=self.facts,
        )
        self.assertEqual(context["status"], "PASS")
        self.assertEqual(
            self.checks.draft(article(), article_type="Beratung", fact_pack=context["fact_pack"])["status"],
            "PASS",
        )

    def test_historical_plain_research_is_still_blocked_by_system4_guard(self):
        with self.assertRaisesRegex(System4ReadOnlyError, "RESEARCH_BLOCK:RESEARCH_JSON_INVALID"):
            self.checks.research("unstructured research text")

    def test_facts_not_bound_to_research_are_still_blocked(self):
        bad = facts_obj()
        bad["claims"][0]["source_id"] = "not-in-research"
        text = json.dumps(bad, ensure_ascii=False)
        with self.assertRaisesRegex(System4ReadOnlyError, "FACTS_BLOCK:FACT_SOURCE_NOT_IN_RESEARCH"):
            self.checks.facts(text, self.research)

    def test_context_fact_pack_must_match_research_and_facts(self):
        payload = json.loads(context_text())
        payload["fact_pack"]["claims"][0]["statement"] = "Abweichende Behauptung mit ausreichender Länge für den Test."
        with self.assertRaisesRegex(System4ReadOnlyError, "CONTEXT_CONTENT_BLOCK:FACT_PACK_FACTS_BINDING_MISMATCH"):
            self.checks.context(
                json.dumps(payload, ensure_ascii=False),
                article=self.article_binding,
                source_snapshot_sha256=SOURCE_SNAPSHOT,
                research_text=self.research,
                facts_text=self.facts,
            )

    def test_context_identity_must_match_bound_article(self):
        payload = json.loads(context_text())
        payload["production_plan_item"]["target_keyword"] = "Fremdes Keyword"
        with self.assertRaisesRegex(System4ReadOnlyError, "CONTEXT_PRODUCTION_BLOCK:PRODUCTION_PLAN_IDENTITY_MISMATCH:target_keyword"):
            self.checks.context(
                json.dumps(payload, ensure_ascii=False),
                article=self.article_binding,
                source_snapshot_sha256=SOURCE_SNAPSHOT,
                research_text=self.research,
                facts_text=self.facts,
            )

    def test_design_drift_is_blocked_not_repaired(self):
        bad = article("<h3>Abweichende Zwischenüberschrift</h3>")
        with self.assertRaisesRegex(System4ReadOnlyError, "DRAFT_DESIGN_BLOCK:DESIGN_BERATUNG_HEADING_LEVEL_FORBIDDEN"):
            self.checks.draft(bad, article_type="Beratung", fact_pack=fact_pack())
        self.assertIn("<h3>", bad)

    def test_repair_uses_existing_continuity_guard(self):
        old = article().replace("Konkreter Artikelinhalt", "Konkreter fachlicher Artikelinhalt")
        new = old.replace("belegten Aussagen.", "belegten Aussagen!")
        self.assertEqual(
            self.checks.repair(old, new, article_type="Beratung", fact_pack=fact_pack())["status"],
            "PASS",
        )
        rewrite = article().replace(
            "Konkreter Artikelinhalt mit belegten Aussagen.",
            "Völlig anderer Inhalt ohne sachlichen Zusammenhang. " * 20,
        )
        with self.assertRaisesRegex(System4ReadOnlyError, "REPAIR_CONTENT_BLOCK:REPAIR_SCOPE_TOO_LARGE"):
            self.checks.repair(old, rewrite, article_type="Beratung", fact_pack=fact_pack())

    def test_fullcheck_delegates_to_existing_production_checks_without_reimplementing(self):
        evidence = {"contract": "SYSTEM4_FULL_PRODUCTION_CHECK_V1", "status": "PASS"}
        with mock.patch.object(self.checks.production_checks, "run_all", return_value=evidence) as real:
            result = self.checks.fullcheck(
                article(),
                article=self.article_binding,
                source_snapshot_sha256=SOURCE_SNAPSHOT,
                fact_pack=fact_pack(),
                production_plan_item=plan_item(),
            )
        real.assert_called_once()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["evidence"], evidence)

    def test_existing_repair_required_result_returns_exact_findings(self):
        findings = [{"error_code": "LT_FINDING", "message": "Beispiel"}]
        failure = self.checks.production_checks.RepairRequired("languagetool", findings)
        with mock.patch.object(self.checks.production_checks, "run_all", side_effect=failure):
            result = self.checks.fullcheck(
                article(),
                article=self.article_binding,
                source_snapshot_sha256=SOURCE_SNAPSHOT,
                fact_pack=fact_pack(),
                production_plan_item=plan_item(),
            )
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["checker"], "languagetool")
        self.assertEqual(result["findings"], findings)

    def test_batch_calls_existing_distinctness_and_repetition_guards(self):
        bodies = [
            '<article><p>' + " ".join(f"eigen{i}_{n}" for n in range(100)) + '</p></article>'
            for i in range(3)
        ]
        result = self.checks.batch(bodies)
        self.assertEqual(result["status"], "PASS")


if __name__ == "__main__":
    unittest.main(verbosity=2)
