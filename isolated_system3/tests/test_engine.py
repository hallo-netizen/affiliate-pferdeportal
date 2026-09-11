import copy
import unittest

from isolated_system3.engine import ArticleProfile, System3Engine, System3Fail


PROFILES = {
    "ratgeber": ArticleProfile(article_type="ratgeber", profile_ref="PROFILE_RATGEBER_TEST_V1"),
    "produktvergleich": ArticleProfile(article_type="produktvergleich", profile_ref="PROFILE_PRODUKTVERGLEICH_TEST_V1"),
}


def valid_input(article_id="A-1"):
    return {
        "article_id": article_id,
        "article_type": "ratgeber",
        "source_payload": {"topic": "Testthema", "facts": [{"name": "x", "value": "y"}]},
        "ruleset_ref": "RULESET_EXTERNAL_IMMUTABLE_TEST_V1",
        "toolchain_ref": "TOOLCHAIN_LOCKED_TEST_V1",
    }


def valid_evidence(article="Ein eigenständig formulierter Testartikel."):
    return {
        "RESEARCH": {"status": "PASS"},
        "FACT_CHECK": {"status": "PASS"},
        "DRAFT": {"status": "PASS", "article": article},
        "LANGUAGE": {"status": "PASS"},
        "RULE_CHECK": {"status": "PASS", "all_rules_exact": True},
        "QUALITY_CHECK": {"status": "PASS", "quality_floor_pass": True},
    }


class System3FirstTest(unittest.TestCase):
    def setUp(self):
        self.engine = System3Engine(PROFILES)

    def test_positive_valid_article_reaches_done(self):
        capsule = self.engine.ingress(valid_input())
        result = self.engine.run(capsule, valid_evidence())
        self.assertEqual(result["trace"], list(self.engine.states))
        self.assertTrue(result["rule_conformity"])
        self.assertTrue(result["quality_floor_pass"])
        self.assertFalse(result["publish_allowed"])

    def test_negative_unknown_article_type_fails_closed(self):
        raw = valid_input()
        raw["article_type"] = "frei_erfunden"
        with self.assertRaisesRegex(System3Fail, "UNKNOWN_ARTICLE_TYPE"):
            self.engine.ingress(raw)

    def test_negative_external_routing_injection_fails_closed(self):
        raw = valid_input()
        raw["source_payload"]["nested"] = {"next_state": "DONE"}
        with self.assertRaisesRegex(System3Fail, "EXTERNAL_CONTROL_FIELD_BLOCKED"):
            self.engine.ingress(raw)

    def test_negative_stage_cannot_choose_route(self):
        capsule = self.engine.ingress(valid_input())
        evidence = valid_evidence()
        evidence["RESEARCH"]["route"] = "DONE"
        with self.assertRaisesRegex(System3Fail, "ROUTING_AUTHORITY_BLOCKED"):
            self.engine.run(capsule, evidence)

    def test_negative_tampered_capsule_fails_closed(self):
        capsule = self.engine.ingress(valid_input())
        capsule.payload["article_type"] = "produktvergleich"
        with self.assertRaisesRegex(System3Fail, "CAPSULE_INTEGRITY_FAIL"):
            self.engine.run(capsule, valid_evidence())

    def test_negative_missing_rule_conformity_blocks_output(self):
        capsule = self.engine.ingress(valid_input())
        evidence = valid_evidence()
        evidence["RULE_CHECK"]["all_rules_exact"] = False
        with self.assertRaisesRegex(System3Fail, "RULE_CONFORMITY_FAIL"):
            self.engine.run(capsule, evidence)

    def test_negative_quality_floor_blocks_output(self):
        capsule = self.engine.ingress(valid_input())
        evidence = valid_evidence()
        evidence["QUALITY_CHECK"]["quality_floor_pass"] = False
        with self.assertRaisesRegex(System3Fail, "QUALITY_FLOOR_FAIL"):
            self.engine.run(capsule, evidence)

    def test_1000_articles_have_independent_capsules_and_results(self):
        hashes = set()
        output_hashes = set()
        for i in range(1000):
            capsule = self.engine.ingress(valid_input(article_id=f"A-{i}"))
            result = self.engine.run(capsule, valid_evidence(article=f"Artikel {i}"))
            hashes.add(capsule.capsule_hash)
            output_hashes.add(result["output_hash"])
            self.assertEqual(result["article_id"], f"A-{i}")
            self.assertFalse(result["publish_allowed"])
        self.assertEqual(len(hashes), 1000)
        self.assertEqual(len(output_hashes), 1000)


if __name__ == "__main__":
    unittest.main()
