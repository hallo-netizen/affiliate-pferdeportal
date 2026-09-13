import json
import unittest

from system4_readonly import System4ReadOnlyChecks, System4ReadOnlyError


class DummyContentGuard:
    class ContentGuardError(RuntimeError):
        pass

    @staticmethod
    def validate_fact_pack(*args, **kwargs):
        return None


class DummyProductionChecks:
    class ProductionCheckError(RuntimeError):
        pass

    @staticmethod
    def validate_bound_context(*args, **kwargs):
        return None


class RealcaseContextGateTests(unittest.TestCase):
    def checks(self):
        obj = System4ReadOnlyChecks.__new__(System4ReadOnlyChecks)
        obj.content_guard = DummyContentGuard
        obj.production_checks = DummyProductionChecks
        return obj

    def test_positive_unbound_context_reaches_normal_validation(self):
        article = {
            "title": "Checklisten für Pferdeanhänger auswählen die wichtigsten Entscheidungskriterien",
            "target_keyword": "Checklisten für Pferdeanhänger",
            "category": "checklisten-fuer-pferdeanhaenger-beratung",
            "article_type": "Beratung",
            "plan_slot": "a" * 64,
        }
        payload = {
            "fact_pack": {"contract": "canonical_fact_pack_v1"},
            "production_plan_item": {
                "article_type": article["article_type"],
                "target_keyword": article["target_keyword"],
                "topic": article["title"],
                "runtime_order": {},
            },
        }
        out = self.checks().context(
            json.dumps(payload),
            article=article,
            source_snapshot_sha256="a" * 64,
            research_text="{}",
            facts_text="{}",
        )
        self.assertEqual(out["status"], "PASS")

    def test_negative_prebound_quality_binding_is_blocked_before_normal_validation(self):
        payload = {
            "fact_pack": {"contract": "canonical_fact_pack_v1"},
            "production_plan_item": {
                "article_type": "Beratung",
                "quality_binding": {"contract": "content_structure_language_binding_v2"},
                "quality_binding_hash": "0" * 64,
            },
        }
        with self.assertRaisesRegex(
            System4ReadOnlyError,
            "CONTEXT_REALCASE_BLOCK:REALCASE_PREBOUND_PRODUCTION_FIELD_FORBIDDEN:quality_binding,quality_binding_hash",
        ):
            self.checks().context(
                json.dumps(payload),
                article={"article_type": "Beratung"},
                source_snapshot_sha256="a" * 64,
                research_text="{}",
                facts_text="{}",
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
