import copy
import unittest
from pathlib import Path
from unittest import mock

import controller
import production_checks


class RepairOwnerFailClosedContractTests(unittest.TestCase):
    @staticmethod
    def _state():
        return {
            'phase': 'CHECK_REQUIRED',
            'production_context': {'fact_pack': {}, 'production_plan_item': {}},
            'article': {'article_type': 'Beratung'},
            'draft_markdown': '<article><p>gebundener unveraenderter Draft</p></article>',
            'draft_sha256': 'deadbeef',
            'checks': {},
            'last_error': None,
        }

    def _run(self, findings, checker='ppm679'):
        state = self._state()
        before = copy.deepcopy(state)
        exc = production_checks.RepairRequired(checker, findings)
        with mock.patch.object(controller, 'load', return_value=(state, Path('/tmp/owner-return-state.json'))), \
             mock.patch.object(controller.authoring_contract, 'validate_bound', return_value={}), \
             mock.patch.object(controller.content_guard, 'validate_single_article', return_value=None), \
             mock.patch.object(controller.design_guard, 'validate_design_neutrality', return_value=None), \
             mock.patch.object(controller.production_checks, 'run_all', side_effect=exc), \
             mock.patch.object(controller._engine, 'save', return_value=None):
            rc = controller.cmd_fullcheck('/tmp/irrelevant')
        return rc, before, state

    def test_parent_owner_returns_exact_rc4_and_freezes_bound_payload(self):
        rc, before, after = self._run([{
            'error_code': 'BLOCKED_CONTENT_TITLE_INVALID',
            'field_path': 'canonical_article.title',
            'repair_owner': 'PARENT_TITLE_MACHINE',
        }])
        self.assertEqual(rc, 4)
        self.assertEqual(after['phase'], 'CHECK_REQUIRED')
        self.assertEqual(after['checks']['repair_owner'], 'PARENT_TITLE_MACHINE')
        self.assertEqual(after['checks']['repair_owners'], ['PARENT_TITLE_MACHINE'])
        self.assertEqual(after['checks']['return_route'], 'PARENT_LAUNCH')
        self.assertIs(after['checks']['return_required'], True)
        self.assertEqual(after['draft_markdown'], before['draft_markdown'])
        self.assertEqual(after['draft_sha256'], before['draft_sha256'])
        self.assertEqual(after['article'], before['article'])
        self.assertEqual(after['production_context'], before['production_context'])

    def test_ppm_repair_without_owner_is_fail_closed(self):
        with self.assertRaisesRegex(controller.Fail, 'REPAIR_OWNER_MISSING:ppm679'):
            self._run([{'error_code': 'BLOCKED_CONTENT_SOMETHING'}])

    def test_multiple_repairable_owners_must_return_not_block(self):
        rc, before, after = self._run([
            {'error_code': 'BLOCKED_CONTENT_TITLE_INVALID', 'repair_owner': 'PARENT_TITLE_MACHINE'},
            {'error_code': 'BLOCKED_CONTENT_BODY_INVALID', 'repair_owner': 'DRAFT_WORKER'},
        ])
        self.assertEqual(rc, 4)
        self.assertEqual(after['phase'], 'CHECK_REQUIRED')
        self.assertEqual(after['checks']['repair_owner'], 'MULTI_OWNER_RETURN')
        self.assertEqual(after['checks']['repair_owners'], ['DRAFT_WORKER', 'PARENT_TITLE_MACHINE'])
        self.assertIs(after['checks']['return_required'], True)
        self.assertEqual(after['checks']['return_route'], 'PARENT_LAUNCH')
        self.assertEqual(after['draft_markdown'], before['draft_markdown'])
        self.assertEqual(after['article'], before['article'])
        self.assertEqual(after['production_context'], before['production_context'])

    def test_languagetool_without_explicit_owner_remains_draft_repair(self):
        rc, _, after = self._run([{'error_code': 'LANGUAGETOOL_FINDING'}], checker='languagetool')
        self.assertEqual(rc, 3)
        self.assertEqual(after['phase'], 'REPAIR_REQUIRED')
        self.assertEqual(after['checks']['repair_owner'], 'DRAFT_WORKER')
        self.assertEqual(after['checks']['repair_owners'], ['DRAFT_WORKER'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
