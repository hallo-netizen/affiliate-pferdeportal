import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import controller
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
                self.assertEqual(
                    production_checks._ppm_repair_findings({'errors': [{'error_code': code}]}),
                    [],
                    f'{code} must remain hard/fail-closed',
                )

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
            ('BLOCKED_KNOWN_REGRESSION_PATTERN', 'canonical_article.body_html', 'DRAFT_WORKER'),
            ('BLOCKED_KNOWN_REGRESSION_PATTERN_REPEAT', '', 'DRAFT_WORKER'),
            ('BLOCKED_CONTENT_CONCLUSION_REQUIRED', 'canonical_article.body_html', 'DRAFT_WORKER'),
            ('BLOCKED_WAVE2_STRUCTURE_REQUIRED', 'canonical_article.body_html', 'DRAFT_WORKER'),
            ('BLOCKED_CANONICAL_RUNTIME_LINK_REQUIRED', 'canonical_article.link_binding', 'PORTAL_LINK_MACHINE'),
        ]
        for code, field_path, owner in variants:
            with self.subTest(code=code):
                findings = production_checks._ppm_repair_findings({'errors': [{'error_code': code, 'field_path': field_path}]})
                self.assertTrue(findings, f'{code} must route to repair owner instead of generic hard block')
                self.assertEqual(findings[0]['repair_owner'], owner)

    def test_owner_matrix_uses_artifact_semantics(self):
        cases = [
            ('canonical_article.body_html', 'DRAFT_WORKER'),
            ('canonical_article.title', 'PARENT_TITLE_MACHINE'),
            ('quality_binding.wordpress_category.slug', 'PARENT_CATEGORY_MACHINE'),
            ('canonical_article.article_type', 'PARENT_ARTICLE_TYPE_MACHINE'),
            ('production_plan.target_keyword', 'PARENT_KEYWORD_MACHINE'),
            ('production_plan.slot', 'PARENT_SLOT_MACHINE'),
            ('canonical_article.link_binding.href', 'PORTAL_LINK_MACHINE'),
            ('production_context.fact_pack.claims', 'CONTEXT_WORKER'),
        ]
        for field_path, owner in cases:
            with self.subTest(field_path=field_path):
                findings = production_checks._ppm_repair_findings({
                    'errors': [{
                        'error_code': 'BLOCKED_CONTENT_FIELD_INVALID',
                        'field_path': field_path,
                    }]
                })
                self.assertTrue(findings)
                self.assertEqual(findings[0]['repair_owner'], owner)

    @staticmethod
    def _minimal_state():
        return {
            'phase': 'CHECK_REQUIRED',
            'production_context': {'fact_pack': {}, 'production_plan_item': {}},
            'article': {'article_type': 'Beratung'},
            'draft_markdown': '<article><p>Test</p></article>',
            'draft_sha256': 'deadbeef',
            'checks': {},
            'last_error': None,
        }

    def _run_controller_repair_finding(self, finding):
        state = self._minimal_state()
        fake_path = Path('/tmp/system4-owner-contract-state.json')
        repair = production_checks.RepairRequired('ppm679', [finding])
        with mock.patch.object(controller, 'load', return_value=(state, fake_path)), \
             mock.patch.object(controller.authoring_contract, 'validate_bound', return_value={}), \
             mock.patch.object(controller.content_guard, 'validate_single_article', return_value=None), \
             mock.patch.object(controller.design_guard, 'validate_design_neutrality', return_value=None), \
             mock.patch.object(controller.production_checks, 'run_all', side_effect=repair), \
             mock.patch.object(controller._engine, 'save', return_value=None):
            rc = controller.cmd_fullcheck('/tmp/irrelevant')
        return rc, state

    def test_controller_draft_owner_enters_same_article_repair(self):
        rc, state = self._run_controller_repair_finding({
            'error_code': 'BLOCKED_KNOWN_REGRESSION_PATTERN',
            'repair_owner': 'DRAFT_WORKER',
        })
        self.assertEqual(rc, 3)
        self.assertEqual(state['phase'], 'REPAIR_REQUIRED')

    def test_controller_must_not_collapse_parent_owner_into_draft_repair(self):
        rc, state = self._run_controller_repair_finding({
            'error_code': 'BLOCKED_CONTENT_TITLE_INVALID',
            'field_path': 'canonical_article.title',
            'repair_owner': 'PARENT_TITLE_MACHINE',
        })
        self.assertNotEqual(
            state['phase'],
            'REPAIR_REQUIRED',
            'PARENT_TITLE_MACHINE finding was incorrectly collapsed into same-article DRAFT repair',
        )
        self.assertNotEqual(rc, 3, 'parent-owner return must be distinct from same-article repair return code')


if __name__ == '__main__':
    unittest.main(verbosity=2)
