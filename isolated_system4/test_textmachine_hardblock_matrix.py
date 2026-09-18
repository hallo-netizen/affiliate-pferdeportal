import unittest
from pathlib import Path
from unittest import mock

import content_guard
import controller
import design_guard
import production_checks


PPM_HARD_RULES = [
    ('CODE_WAVE2_CONTRACT', 'BLOCKED_WAVE2_CONTRACT_MISSING'),
    ('CODE_WAVE2_QUALITY_BINDING', 'BLOCKED_WAVE2_QUALITY_BINDING_MISSING'),
    ('CODE_WAVE2_QUALITY_BINDING_HASH', 'BLOCKED_WAVE2_QUALITY_BINDING_HASH'),
    ('CODE_WAVE2_INTERNAL_MARKER', 'BLOCKED_WAVE2_INTERNAL_MARKER_MISSING'),
    ('CODE_WAVE2_LINK_REGISTRY_HASH', 'BLOCKED_WAVE2_LINK_REGISTRY_HASH'),
    ('CODE_MAINBLOCK1_LANGUAGE_DELTA', 'BLOCKED_MAINBLOCK1_LANGUAGE_DELTA_EVIDENCE'),
    ('CODE_WAVE2_LANGUAGE_EVIDENCE', 'BLOCKED_WAVE2_LANGUAGE_EVIDENCE'),
    ('CODE_VALIDATION_CONTRACT_VERSION_MISSING', 'BLOCKED_VALIDATION_CONTRACT_VERSION_MISSING'),
    ('CODE_SECTION_REQUIREMENTS_HASH', 'BLOCKED_SECTION_REQUIREMENTS_HASH_MISMATCH'),
    ('CODE_VALIDATION_CONTRACT_VERSION_UNKNOWN_A', 'BLOCKED_VALIDATION_CONTRACT_VERSION_UNKNOWN'),
    ('CODE_VALIDATION_CONTRACT_VERSION_UNKNOWN_B', 'BLOCKED_VALIDATION_CONTRACT_VERSION_UNKNOWN'),
    ('CODE_CONTENT_TYPE_DEFINITION', 'BLOCKED_CONTENT_TYPE_DEFINITION_MISSING'),
    ('CODE_CONTENT_HASH', 'BLOCKED_CONTENT_HASH_MISMATCH'),
    ('CODE_KNOWN_ERROR_CONTRACT', 'BLOCKED_KNOWN_ERROR_CONTRACT_MISSING'),
    ('W4::R8-0790', 'W4_R8_0790_LOCAL_EXECUTED_TEST_EVIDENCE_MISSING'),
]

CONTENT_GUARD_HARD = [
    'FACT_PACK_OBJECT_REQUIRED','FACT_PACK_CONTRACT_INVALID','FACT_PACK_NOT_PRODUCTION_READY','FACT_PACK_SOURCES_MISSING',
    'FACT_PACK_SOURCE_OBJECT_REQUIRED','FACT_PACK_SOURCE_ID_INVALID','FACT_PACK_SOURCE_TITLE_INVALID','FACT_PACK_SOURCE_URL_INVALID',
    'FACT_PACK_SOURCE_RETRIEVED_AT_INVALID','FACT_PACK_SOURCE_HASH_INVALID','FACT_PACK_SOURCE_TITLE_SYNTHETIC',
    'FACT_PACK_SOURCE_EVIDENCE_INVALID','FACT_PACK_SOURCE_HASH_MISMATCH','FACT_PACK_SOURCE_ID_DUPLICATE','FACT_PACK_CLAIMS_TOO_LOW',
    'FACT_PACK_CLAIM_OBJECT_REQUIRED','FACT_ID_INVALID','FACT_SOURCE_ID_INVALID','FACT_STATEMENT_INVALID','FACT_EVIDENCE_TEXT_INVALID',
    'FACT_EVIDENCE_HASH_INVALID','FACT_SOURCE_NOT_IN_RESEARCH','FACT_EVIDENCE_HASH_MISMATCH','FACT_EVIDENCE_NOT_IN_SOURCE',
    'FACT_PACK_FACT_ID_DUPLICATE','FACT_PACK_CLAIM_SOURCE_URL_MISMATCH','ARTICLE_FACT_PACK_CLAIMS_MISSING','ARTICLE_FACT_IDS_MISSING',
]

DESIGN_GUARD_HARD = [
    'DESIGN_ARTICLE_TYPE_TOKEN_INVALID',
    'DESIGN_ARTICLE_TYPE_MISSING',
    'DESIGN_ACTIVE_OR_GLOBAL_HTML_FORBIDDEN',
    'DESIGN_INLINE_STYLE_FORBIDDEN',
    'DESIGN_EVENT_HANDLER_FORBIDDEN',
    'DESIGN_JAVASCRIPT_URL_FORBIDDEN',
]


class TextmachineHardBlockMatrixTests(unittest.TestCase):
    @staticmethod
    def state():
        return {
            'phase': 'CHECK_REQUIRED',
            'production_context': {'fact_pack': {}, 'production_plan_item': {}},
            'article': {'article_type': 'Beratung', 'title': 'Testartikel'},
            'draft_markdown': '<article class="ppm-generated ppm-type-beratung" data-article-type="Beratung"><p data-fact-id="fact-a">Text</p></article>',
            'draft_sha256': 'draft-sha', 'checks': {}, 'last_error': None, 'route_contract': None,
        }

    def _controller_with_content_error(self, code):
        state = self.state(); path = Path('/tmp/system4-hardblock-content.json')
        with mock.patch.object(controller, 'load', return_value=(state, path)), mock.patch.object(controller.authoring_contract, 'validate_bound', return_value={}), mock.patch.object(controller.content_guard, 'validate_single_article', side_effect=content_guard.ContentGuardError(code)), mock.patch.object(controller._engine, 'save', return_value=None):
            with self.assertRaisesRegex(controller.Fail, 'FULL_CHECK_HARD_BLOCK:CONTENT_GUARD:'):
                controller.cmd_fullcheck('/tmp/irrelevant')
        self.assertNotEqual(state['phase'], 'REPAIR_REQUIRED')

    def _controller_with_design_error(self, code):
        state = self.state(); path = Path('/tmp/system4-hardblock-design.json')
        with mock.patch.object(controller, 'load', return_value=(state, path)), mock.patch.object(controller.authoring_contract, 'validate_bound', return_value={}), mock.patch.object(controller.content_guard, 'validate_single_article', return_value={'status': 'PASS'}), mock.patch.object(controller.design_guard, 'validate_design_neutrality', side_effect=design_guard.DesignGuardError(code)), mock.patch.object(controller._engine, 'save', return_value=None):
            with self.assertRaisesRegex(controller.Fail, 'FULL_CHECK_HARD_BLOCK:DESIGN_GUARD:'):
                controller.cmd_fullcheck('/tmp/irrelevant')
        self.assertNotEqual(state['phase'], 'REPAIR_REQUIRED')

    def _controller_with_production_hard_error(self, code):
        state = self.state(); path = Path('/tmp/system4-hardblock-ppm.json')
        with mock.patch.object(controller, 'load', return_value=(state, path)), mock.patch.object(controller.authoring_contract, 'validate_bound', return_value={}), mock.patch.object(controller.content_guard, 'validate_single_article', return_value={'status': 'PASS'}), mock.patch.object(controller.design_guard, 'validate_design_neutrality', return_value={'status': 'PASS'}), mock.patch.object(controller.production_checks, 'run_all', side_effect=production_checks.ProductionCheckError(code)), mock.patch.object(controller._engine, 'save', return_value=None):
            with self.assertRaisesRegex(controller.Fail, 'FULL_CHECK_HARD_BLOCK:'):
                controller.cmd_fullcheck('/tmp/irrelevant')
        self.assertNotEqual(state['phase'], 'REPAIR_REQUIRED')

    def test_all_15_ppm_hard_rules_never_become_repair(self):
        self.assertEqual(len(PPM_HARD_RULES), 15)
        for rule_id, code in PPM_HARD_RULES:
            with self.subTest(rule_id=rule_id, code=code):
                if rule_id != 'W4::R8-0790':
                    self.assertEqual(production_checks._ppm_repair_findings({'errors': [{'error_code': code}]}), [])
                self._controller_with_production_hard_error(code)

    def test_all_28_content_guard_hard_rules_never_become_repair(self):
        self.assertEqual(len(CONTENT_GUARD_HARD), 28)
        for code in CONTENT_GUARD_HARD:
            with self.subTest(code=code):
                self.assertIsNone(production_checks.guard_repair_finding('content_guard', code)); self._controller_with_content_error(code)

    def test_all_6_reachable_design_guard_hard_rules_never_become_repair(self):
        self.assertEqual(len(DESIGN_GUARD_HARD), 6)
        for code in DESIGN_GUARD_HARD:
            with self.subTest(code=code):
                self.assertIsNone(production_checks.guard_repair_finding('design_guard', code)); self._controller_with_design_error(code)

    def test_matrix_control_sum_is_exactly_49(self):
        self.assertEqual(len(PPM_HARD_RULES) + len(CONTENT_GUARD_HARD) + len(DESIGN_GUARD_HARD), 49)


if __name__ == '__main__':
    unittest.main(verbosity=2)
