import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import production_checks


def current_language_evidence(body: str) -> dict:
    checked = production_checks._ppm_visible_language_text(body)
    raw = '{"matches":[]}'
    checked_hash = production_checks.text_sha256(checked)
    raw_hash = production_checks.text_sha256(raw)
    return {
        "engine": production_checks.LT_ENGINE,
        "outer_dependency_sha256": production_checks.LT_OUTER_DEPENDENCY_SHA256,
        "inner_dependency_sha256": production_checks.LT_INNER_DEPENDENCY_SHA256,
        "content_hash": production_checks.text_sha256(body),
        "checked_text": checked,
        "checked_text_sha256": checked_hash,
        "raw_report_json": raw,
        "raw_report_sha256": raw_hash,
        "raw_finding_count": 0,
        "unresolved_finding_count": 0,
        "return_code": 0,
        "approved_exceptions": [],
        "execution_record": {
            "input_sha256": checked_hash,
            "raw_stdout_sha256": raw_hash,
            "return_code": 0,
        },
    }


def plan_for(body: str) -> dict:
    quality = {
        "contract": "content_structure_language_binding_v2",
        "wordpress_category": {"slug": "test-beratung"},
        "table_value_statement": "Unveränderte fachliche Tabellenbindung bleibt bestehen.",
        "language_evidence": current_language_evidence(body),
    }
    return {
        "article_type": "Beratung",
        "topic": "Testberatung auswählen",
        "target_keyword": "Testberatung",
        "canonical_article": {
            "title": "Testberatung auswählen",
            "body_html": body,
            "body_html_sha256": production_checks.text_sha256(body),
            "body_text": production_checks._canonical_body_text(body),
        },
        "quality_binding": quality,
        "quality_binding_hash": production_checks.stable_hash(quality),
    }


class RuntimeDraftRebindTests(unittest.TestCase):
    def test_current_bound_language_evidence_is_reused_without_extra_lt(self):
        body = "<article><p>Sauberer Text.</p><h2>Prüfung</h2><p>Weiterer Text.</p></article>"
        plan = plan_for(body)
        original = copy.deepcopy(plan)
        with mock.patch.object(production_checks, "_fresh_ppm_language_evidence") as fresh:
            rebound, source = production_checks._runtime_rebound_plan(Path("."), body, plan)
        fresh.assert_not_called()
        self.assertEqual(source, "BOUND_CURRENT_REUSED")
        self.assertEqual(plan, original)
        self.assertEqual(rebound["quality_binding_hash"], production_checks.stable_hash(rebound["quality_binding"]))

    def test_repaired_draft_refreshes_only_draft_derived_fields(self):
        old_body = "<article><p>Alter Text.</p><h2>Prüfung</h2><p>Bindung.</p></article>"
        new_body = "<article><p>Neuer Text.</p><h2>Prüfung</h2><p>Bindung.</p></article>"
        plan = plan_for(old_body)
        original = copy.deepcopy(plan)
        fresh_evidence = current_language_evidence(new_body)
        with mock.patch.object(production_checks, "_fresh_ppm_language_evidence", return_value=(fresh_evidence, "REAL_LT68_CURRENT_DRAFT_REFRESHED")) as fresh:
            rebound, source = production_checks._runtime_rebound_plan(Path("."), new_body, plan)
        fresh.assert_called_once()
        self.assertEqual(source, "REAL_LT68_CURRENT_DRAFT_REFRESHED")
        self.assertEqual(plan, original, "bound production context must remain immutable")
        self.assertEqual(rebound["canonical_article"]["body_html"], new_body)
        self.assertEqual(rebound["canonical_article"]["body_html_sha256"], production_checks.text_sha256(new_body))
        self.assertEqual(rebound["canonical_article"]["body_text"], production_checks._canonical_body_text(new_body))
        self.assertEqual(rebound["quality_binding"]["language_evidence"], fresh_evidence)
        self.assertEqual(rebound["quality_binding"]["table_value_statement"], original["quality_binding"]["table_value_statement"])
        self.assertEqual(rebound["quality_binding_hash"], production_checks.stable_hash(rebound["quality_binding"]))

    def test_same_exact_lt_checked_text_is_reused_for_ppm_without_second_lt(self):
        body = "<article><p>Sauberer Text.</p><h2>Prüfung</h2><p>Weiterer Text.</p></article>"
        checked = production_checks._plain_text(body).rstrip("\n")
        self.assertEqual(checked, production_checks._ppm_visible_language_text(body))
        raw = '{"matches":[]}'
        lt_pass = {
            "status": "PASS", "engine": production_checks.LT_ENGINE, "finding_count": 0,
            "_checked_text": checked, "_raw_report_json": raw, "_return_code": 0,
        }
        with mock.patch.object(production_checks, "_run_languagetool_text") as second:
            evidence, source = production_checks._fresh_ppm_language_evidence(Path("."), body, lt_pass)
        second.assert_not_called()
        self.assertEqual(source, "REAL_LT68_FULLCHECK_REUSED")
        self.assertEqual(evidence["checked_text"], checked)
        self.assertEqual(evidence["raw_report_json"], raw)
        self.assertEqual(evidence["unresolved_finding_count"], 0)

    def test_different_lt_checked_text_must_run_second_real_check(self):
        body = "<article><p>Sauberer Text.</p><h2>Prüfung</h2><p>Weiterer Text.</p></article>"
        lt_pass = {"_checked_text": "NICHT IDENTISCH", "_raw_report_json": '{"matches":[]}', "_return_code": 0}
        with mock.patch.object(production_checks, "_run_languagetool_text", return_value=({"matches": []}, '{"matches":[]}', 0)) as second:
            evidence, source = production_checks._fresh_ppm_language_evidence(Path("."), body, lt_pass)
        second.assert_called_once()
        self.assertEqual(source, "REAL_LT68_CURRENT_DRAFT_REFRESHED")
        self.assertEqual(evidence["unresolved_finding_count"], 0)

    def test_tampered_bound_quality_hash_is_not_normalized(self):
        body = "<article><p>Sauberer Text.</p><h2>Prüfung</h2><p>Weiterer Text.</p></article>"
        plan = plan_for(body)
        plan["quality_binding_hash"] = "0" * 64
        with self.assertRaisesRegex(production_checks.ProductionCheckError, "PPM679_BOUND_QUALITY_BINDING_HASH_INVALID"):
            production_checks._runtime_rebound_plan(Path("."), body, plan)

    def test_wrong_quality_contract_is_not_synthesized(self):
        body = "<article><p>Sauberer Text.</p><h2>Prüfung</h2><p>Weiterer Text.</p></article>"
        plan = plan_for(body)
        plan["quality_binding"]["contract"] = "wrong"
        plan["quality_binding_hash"] = production_checks.stable_hash(plan["quality_binding"])
        with self.assertRaisesRegex(production_checks.ProductionCheckError, "PPM679_QUALITY_BINDING_MISSING"):
            production_checks._runtime_rebound_plan(Path("."), body, plan)

    def test_ppm_visible_text_contract_excludes_h3_but_keeps_bound_visible_units(self):
        body = "<article><h3>Nicht im PPM-Sprachbeleg</h3><h2>Auswahl</h2><p>Hallo <strong>Welt</strong> !</p><td>Wert ; gut</td></article>"
        self.assertEqual(production_checks._ppm_visible_language_text(body), "Auswahl\n\nHallo Welt!\n\nWert; gut")

    def test_explicit_lt_path_fails_closed_instead_of_falling_back(self):
        with tempfile.TemporaryDirectory() as td:
            fake = Path(td) / "languagetool-commandline.jar"
            fake.write_bytes(b"not-the-bound-jar")
            with mock.patch.dict("os.environ", {"SYSTEM4_LANGUAGETOOL_JAR": str(fake)}, clear=False):
                with self.assertRaisesRegex(production_checks.ProductionCheckError, "LANGUAGETOOL_6_8_EXPLICIT_JAR_INVALID"):
                    production_checks._find_languagetool_jar(Path(td))


if __name__ == "__main__":
    unittest.main(verbosity=2)
