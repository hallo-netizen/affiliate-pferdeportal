import copy
import unittest
from pathlib import Path
from unittest import mock

import content_guard
import controller
import design_guard


class FullcheckGuardRepairContractTests(unittest.TestCase):
    @staticmethod
    def state():
        return {
            'phase': 'CHECK_REQUIRED',
            'production_context': {'fact_pack': {}, 'production_plan_item': {}},
            'article': {'article_type': 'Beratung', 'title': 'Testartikel'},
            'draft_markdown': '<article><p>Alt</p></article>',
            'draft_sha256': 'draft-old',
            'checks': {},
            'last_error': None,
            'route_contract': None,
        }

    def run_fullcheck(self, state, *, content_error=None, design_error=None, production_result=None):
        path = Path('/tmp/system4-guard-repair-state.json')
        content_side = content_guard.ContentGuardError(content_error) if content_error else None
        design_side = design_guard.DesignGuardError(design_error) if design_error else None
        with mock.patch.object(controller, 'load', return_value=(state, path)), \
             mock.patch.object(controller.authoring_contract, 'validate_bound', return_value={}), \
             mock.patch.object(controller.content_guard, 'validate_single_article', side_effect=content_side), \
             mock.patch.object(controller.design_guard, 'validate_design_neutrality', side_effect=design_side), \
             mock.patch.object(controller.production_checks, 'run_all', return_value=production_result or {'status': 'PASS'}), \
             mock.patch.object(controller._engine, 'save', return_value=None):
            return controller.cmd_fullcheck('/tmp/irrelevant')

    def test_repairable_content_guard_finding_enters_same_article_repair(self):
        state = self.state()
        article_before = copy.deepcopy(state['article'])
        rc = self.run_fullcheck(state, content_error='ARTICLE_UNKNOWN_FACT_ID:fact-x')
        self.assertEqual(rc, 3)
        self.assertEqual(state['phase'], 'REPAIR_REQUIRED')
        self.assertEqual(state['checks']['repair_owner'], 'DRAFT_WORKER')
        self.assertEqual(state['article'], article_before)

    def test_repairable_design_guard_finding_enters_same_article_repair(self):
        state = self.state()
        article_before = copy.deepcopy(state['article'])
        rc = self.run_fullcheck(state, design_error='DESIGN_PPM_GENERATED_CLASS_MISSING')
        self.assertEqual(rc, 3)
        self.assertEqual(state['phase'], 'REPAIR_REQUIRED')
        self.assertEqual(state['checks']['repair_owner'], 'DRAFT_WORKER')
        self.assertEqual(state['article'], article_before)

    def test_content_integrity_error_remains_terminal_hard_block(self):
        state = self.state()
        with self.assertRaisesRegex(controller.Fail, 'FULL_CHECK_HARD_BLOCK:CONTENT_GUARD:FACT_PACK_CONTRACT_INVALID'):
            self.run_fullcheck(state, content_error='FACT_PACK_CONTRACT_INVALID')
        self.assertEqual(state['phase'], 'CHECK_REQUIRED')

    def test_design_security_error_remains_terminal_hard_block(self):
        state = self.state()
        with self.assertRaisesRegex(controller.Fail, 'FULL_CHECK_HARD_BLOCK:DESIGN_GUARD:DESIGN_INLINE_STYLE_FORBIDDEN'):
            self.run_fullcheck(state, design_error='DESIGN_INLINE_STYLE_FORBIDDEN')
        self.assertEqual(state['phase'], 'CHECK_REQUIRED')

    def test_repaired_same_article_reenters_fullcheck_and_passes(self):
        state = self.state()
        article_before = copy.deepcopy(state['article'])
        rc = self.run_fullcheck(state, content_error='ARTICLE_FACT_TRACE_MISSING')
        self.assertEqual(rc, 3)
        self.assertEqual(state['phase'], 'REPAIR_REQUIRED')

        # Same article identity; only the draft realization is repaired.
        state['draft_markdown'] = '<article><p data-fact-id="fact-a">Repariert</p></article>'
        state['draft_sha256'] = 'draft-repaired'
        state['phase'] = 'CHECK_REQUIRED'
        rc = self.run_fullcheck(state, production_result={'status': 'PASS'})
        self.assertEqual(rc, 0)
        self.assertEqual(state['phase'], 'OUTPUT_GATE_REQUIRED')
        self.assertEqual(state['article'], article_before)
        self.assertEqual(state['checks']['status'], 'PASS')


if __name__ == '__main__':
    unittest.main(verbosity=2)
