import unittest
from unittest import mock

import production_checks


class RepairOwnerRoutingContractTests(unittest.TestCase):
    """Causal contract: repairability is a semantic owner decision, never a one-off symptom list."""

    def test_known_regression_pattern_is_not_allowed_to_fall_through_to_hard_block(self):
        payload = {
            'ok': False,
            'errors': [{
                'error_code': 'BLOCKED_KNOWN_REGRESSION_PATTERN',
                'failed_rule': 'known_regression_pattern',
                'field_path': 'canonical_article.body_html',
                'expected': 'no known regression pattern',
                'actual': 'known regression pattern present',
                'reason': 'article text is repairable by its producing worker',
                'validator_id': 'ppm679',
            }],
        }
        findings = production_checks._ppm_repair_findings(payload)
        self.assertTrue(findings, 'repairable PPM content finding fell through to terminal hard block')

    def test_unknown_ppm_blocker_remains_fail_closed(self):
        payload = {'ok': False, 'errors': [{'error_code': 'BLOCKED_FUTURE_UNKNOWN_FAILURE'}]}
        self.assertEqual(production_checks._ppm_repair_findings(payload), [])

    def test_integrity_and_execution_failures_are_not_reclassified_as_repair(self):
        hard_codes = [
            'PPM679_PACKAGE_HASH_MISMATCH',
            'PPM679_VALIDATOR_EXECUTION_FAILED',
            'PPM679_VALIDATOR_RESULT_INVALID',
            'PPM679_CONTENT_HASH_MISMATCH',
            'SYSTEM4_DRAFT_BINDING_INVALID',
        ]
        for code in hard_codes:
            with self.subTest(code=code):
                self.assertFalse(code.startswith(('BLOCKED_CONTENT_', 'BLOCKED_WAVE2_', 'BLOCKED_CANONICAL_RUNTIME_LINK_')))

    def test_repair_routing_contract_must_expose_owner_metadata(self):
        payload = {
            'errors': [{
                'error_code': 'BLOCKED_KNOWN_REGRESSION_PATTERN',
                'field_path': 'canonical_article.body_html',
                'failed_rule': 'known_regression_pattern',
            }]
        }
        findings = production_checks._ppm_repair_findings(payload)
        self.assertTrue(findings, 'repairable validator finding must exist')
        self.assertIn('repair_owner', findings[0], 'repair routing must name the producing owner, not only the symptom code')
        self.assertEqual(findings[0]['repair_owner'], 'DRAFT_WORKER')

    def test_repairable_family_is_classified_by_semantics_not_exact_single_code(self):
        variants = [
            'BLOCKED_KNOWN_REGRESSION_PATTERN',
            'BLOCKED_KNOWN_REGRESSION_PATTERN_REPEAT',
            'BLOCKED_CONTENT_CONCLUSION_REQUIRED',
            'BLOCKED_WAVE2_STRUCTURE_REQUIRED',
            'BLOCKED_CANONICAL_RUNTIME_LINK_REQUIRED',
        ]
        for code in variants:
            with self.subTest(code=code):
                findings = production_checks._ppm_repair_findings({'errors': [{'error_code': code, 'field_path': 'canonical_article.body_html'}]})
                self.assertTrue(findings, f'{code} must route to repair owner instead of generic hard block')


if __name__ == '__main__':
    unittest.main(verbosity=2)
