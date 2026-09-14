import unittest
from realcase_acceptance_gate import (
    RealcaseAcceptanceError,
    assert_equivalence,
    assert_no_prebound_production_fields,
    REALCASE_CONTRACT,
    EXPECTED_ROOT_ENTRY,
    EXPECTED_WORKER_ENTRY,
    EXPECTED_CHECKER_ENTRY,
    EXPECTED_HANDOFF,
    LT_SHA256,
    PPM_SHA256,
)


def manifest(raw="a" * 64, plan_builder="RUNTIME_FROM_RAW_INPUT"):
    return {
        "contract": REALCASE_CONTRACT,
        "raw_input_sha256": raw,
        "root_entry": EXPECTED_ROOT_ENTRY,
        "plan_builder": plan_builder,
        "worker_entry": EXPECTED_WORKER_ENTRY,
        "checker_entry": EXPECTED_CHECKER_ENTRY,
        "lt_sha256": LT_SHA256,
        "ppm_sha256": PPM_SHA256,
        "handoff_contract": EXPECTED_HANDOFF,
    }


class RealcaseAcceptanceGateTests(unittest.TestCase):
    def test_positive_exact_identity(self):
        m = manifest()
        self.assertEqual(assert_equivalence(m, dict(m))["status"], "REALCASE_EQUIVALENCE_PASS")

    def test_negative_raw_input_mismatch(self):
        with self.assertRaisesRegex(RealcaseAcceptanceError, "REALCASE_IDENTITY_MISMATCH:raw_input_sha256"):
            assert_equivalence(manifest(), manifest(raw="b" * 64))

    def test_negative_alternate_entry(self):
        real = manifest()
        real["worker_entry"] = "alternate.worker"
        with self.assertRaisesRegex(RealcaseAcceptanceError, "REALCASE_IDENTITY_MISMATCH:worker_entry"):
            assert_equivalence(manifest(), real)

    def test_negative_fixture_plan_builder(self):
        test = manifest(plan_builder="PREBUILT_FIXTURE")
        with self.assertRaisesRegex(RealcaseAcceptanceError, "REALCASE_PLAN_BUILDER_NOT_RUNTIME"):
            assert_equivalence(test, dict(test))

    def test_negative_prebound_quality_binding(self):
        context = {
            "production_plan_item": {
                "quality_binding": {"contract": "content_structure_language_binding_v2"},
                "quality_binding_hash": "0" * 64,
            }
        }
        with self.assertRaisesRegex(RealcaseAcceptanceError, "REALCASE_PREBOUND_PRODUCTION_FIELD_FORBIDDEN"):
            assert_no_prebound_production_fields(context)

    def test_positive_unbound_context(self):
        assert_no_prebound_production_fields({"production_plan_item": {"article_type": "Beratung"}})


if __name__ == "__main__":
    unittest.main(verbosity=2)
