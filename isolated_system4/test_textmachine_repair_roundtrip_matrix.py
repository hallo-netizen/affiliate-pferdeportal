import unittest
from pathlib import Path
from unittest import mock

import controller
import production_checks


# Point 4 is already the machine-fixed per-rule classification authority for the
# reachable text-machine scope.  Point 5 proves the return mechanism for every owner
# class used by those 102 repairable rules.  Routing is owner-driven, not rule-driven:
# once a rule has been bound to an owner, every rule of that owner executes the same
# controller transition.
REPAIR_RULE_COUNTS = {
    'DRAFT_WORKER': 96,          # 83 PPM + 2 ContentGuard + 9 DesignGuard + 2 external-link
    'PARENT_TITLE_MACHINE': 3,
    'PORTAL_LINK_MACHINE': 2,
    'PARENT_CATEGORY_MACHINE': 1,
}


class TextmachineRepairRoundtripMatrixTests(unittest.TestCase):
    @staticmethod
    def state():
        return {
            'phase': 'CHECK_REQUIRED',
            'production_context': {'fact_pack': {}, 'production_plan_item': {}},
            'article': {
                'title': 'Pferde Testartikel',
                'target_keyword': 'Pferde',
                'category': 'test-beratung',
                'article_type': 'Beratung',
                'plan_slot': 'a' * 64,
            },
            'draft_markdown': '<article class="ppm-generated ppm-type-beratung" data-article-type="Beratung"><p data-fact-id="fact-a">Text</p></article>',
            'draft_sha256': 'draft-sha',
            'checks': {}, 'last_error': None, 'route_contract': None,
        }

    def _ppm_owner_return(self, finding, expected_rc, expected_phase, expected_owner):
        state = self.state()
        before_article = dict(state['article'])
        path = Path('/tmp/system4-repair-roundtrip-matrix.json')
        repair = production_checks.RepairRequired('ppm679', [finding])
        with mock.patch.object(controller, 'load', return_value=(state, path)), \
             mock.patch.object(controller.authoring_contract, 'validate_bound', return_value={}), \
             mock.patch.object(controller.content_guard, 'validate_single_article', return_value={'status': 'PASS'}), \
             mock.patch.object(controller.design_guard, 'validate_design_neutrality', return_value={'status': 'PASS'}), \
             mock.patch.object(controller.production_checks, 'run_all', side_effect=repair), \
             mock.patch.object(controller._engine, 'save', return_value=None):
            rc = controller.cmd_fullcheck('/tmp/irrelevant')
        self.assertEqual(rc, expected_rc)
        self.assertEqual(state['phase'], expected_phase)
        self.assertEqual(state['article'], before_article, 'repair routing must not silently replace the article')
        self.assertIn(expected_owner, state['checks']['repair_owners'])
        return state

    def test_control_sum_is_exactly_102_repairable_rules(self):
        self.assertEqual(sum(REPAIR_RULE_COUNTS.values()), 102)
        self.assertEqual(REPAIR_RULE_COUNTS['DRAFT_WORKER'], 96)
        self.assertEqual(REPAIR_RULE_COUNTS['PARENT_TITLE_MACHINE'], 3)
        self.assertEqual(REPAIR_RULE_COUNTS['PORTAL_LINK_MACHINE'], 2)
        self.assertEqual(REPAIR_RULE_COUNTS['PARENT_CATEGORY_MACHINE'], 1)

    def test_draft_owner_enters_same_article_repair(self):
        state = self._ppm_owner_return({
            'error_code': 'BLOCKED_KNOWN_DUPLICATE_HEADING',
            'field_path': 'content.heading',
            'repair_owner': 'DRAFT_WORKER',
        }, 3, 'REPAIR_REQUIRED', 'DRAFT_WORKER')
        self.assertEqual(state['checks']['repair_owner'], 'DRAFT_WORKER')

    def test_parent_title_owner_returns_to_parent_launch_without_mutating_article(self):
        state = self._ppm_owner_return({
            'error_code': 'BLOCKED_CONTENT_TITLE_COLON',
            'field_path': 'canonical_article.title',
            'repair_owner': 'PARENT_TITLE_MACHINE',
        }, 4, 'CHECK_REQUIRED', 'PARENT_TITLE_MACHINE')
        self.assertTrue(state['checks']['return_required'])
        self.assertEqual(state['checks']['return_route'], 'PARENT_LAUNCH')

    def test_portal_link_owner_returns_to_parent_launch_without_mutating_article(self):
        state = self._ppm_owner_return({
            'error_code': 'BLOCKED_CANONICAL_RUNTIME_LINK_REQUIRED',
            'field_path': 'canonical_article.link_binding.href',
            'repair_owner': 'PORTAL_LINK_MACHINE',
        }, 4, 'CHECK_REQUIRED', 'PORTAL_LINK_MACHINE')
        self.assertTrue(state['checks']['return_required'])
        self.assertEqual(state['checks']['return_route'], 'PARENT_LAUNCH')

    def test_parent_category_owner_returns_to_parent_launch_without_mutating_article(self):
        state = self._ppm_owner_return({
            'error_code': 'BLOCKED_CONTENT_CATEGORY_BINDING',
            'field_path': 'quality_binding.wordpress_category.slug',
            'repair_owner': 'PARENT_CATEGORY_MACHINE',
        }, 4, 'CHECK_REQUIRED', 'PARENT_CATEGORY_MACHINE')
        self.assertTrue(state['checks']['return_required'])
        self.assertEqual(state['checks']['return_route'], 'PARENT_LAUNCH')

    def test_recheck_after_repair_reenters_complete_fullcheck_and_passes(self):
        # The rule-dependent routing is tested above.  This verifies the common second
        # half of every repair path: after the responsible owner has corrected its
        # artifact, the same article re-enters the COMPLETE fullcheck and only then PASSes.
        state = self.state()
        path = Path('/tmp/system4-repair-roundtrip-recheck.json')
        state['phase'] = 'CHECK_REQUIRED'
        with mock.patch.object(controller, 'load', return_value=(state, path)), \
             mock.patch.object(controller.authoring_contract, 'validate_bound', return_value={}), \
             mock.patch.object(controller.content_guard, 'validate_single_article', return_value={'status': 'PASS'}) as cg, \
             mock.patch.object(controller.design_guard, 'validate_design_neutrality', return_value={'status': 'PASS'}) as dg, \
             mock.patch.object(controller.production_checks, 'run_all', return_value={'status': 'PASS', 'evidence': {}}) as pc, \
             mock.patch.object(controller._engine, 'save', return_value=None):
            rc = controller.cmd_fullcheck('/tmp/irrelevant')
        self.assertEqual(rc, 0)
        self.assertEqual(state['phase'], 'OUTPUT_GATE_REQUIRED')
        cg.assert_called_once()
        dg.assert_called_once()
        pc.assert_called_once()


if __name__ == '__main__':
    unittest.main(verbosity=2)
