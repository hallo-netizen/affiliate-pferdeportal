from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import controller


class FactPackClaimCountReturnTests(unittest.TestCase):
    def _state(self):
        return {
            'phase': 'CONTEXT_REQUIRED',
            'immutable_core_sha256': 'a' * 64,
            'article': {'title': 'A'},
            'research': {'text': 'bound research', 'sha256': 'b' * 64},
            'facts': {'text': 'old facts', 'sha256': 'c' * 64},
            'production_context': None,
            'authoring_contract': None,
            'draft_markdown': None,
            'draft_sha256': None,
            'checks': {},
            'last_error': None,
            'release_prepared': None,
            'released': False,
        }

    def test_positive_exact_claim_count_returns_same_article_to_facts(self):
        with tempfile.TemporaryDirectory(prefix='s4-claim-return-') as td:
            workspace = Path(td)
            bound = workspace / 'MACHINE_PRODUCTION_BINDING.json'
            bound.write_text('{}', encoding='utf-8')
            state = self._state()
            before_article = json.loads(json.dumps(state['article']))
            before_research = json.loads(json.dumps(state['research']))
            with mock.patch.object(controller.core, 'load', return_value=(state, workspace/'state.json')), \
                 mock.patch.object(controller.core, 'save') as save:
                rc = controller._return_claim_count_to_facts(
                    workspace,
                    bound,
                    controller.core.Fail('AUTHORING_CONTRACT_FAIL:FACT_PACK_CLAIM_COUNT_INVALID'),
                )
            self.assertEqual(rc, 4)
            self.assertEqual(state['phase'], 'FACT_CHECK_REQUIRED')
            self.assertIsNone(state['facts'])
            self.assertEqual(state['article'], before_article)
            self.assertEqual(state['research'], before_research)
            self.assertFalse(bound.exists())
            save.assert_called_once()

    def test_negative_other_authoring_error_is_not_routed(self):
        with tempfile.TemporaryDirectory(prefix='s4-claim-no-route-') as td:
            workspace = Path(td)
            bound = workspace / 'MACHINE_PRODUCTION_BINDING.json'
            bound.write_text('{}', encoding='utf-8')
            with self.assertRaisesRegex(controller.core.Fail, 'PREWRITE_BOUND_LINK_MISSING'):
                controller._return_claim_count_to_facts(
                    workspace,
                    bound,
                    controller.core.Fail('AUTHORING_CONTRACT_FAIL:PREWRITE_BOUND_LINK_MISSING:parent_category'),
                )
            self.assertTrue(bound.exists())

    def test_positive_context_path_routes_exact_claim_count_failure(self):
        with tempfile.TemporaryDirectory(prefix='s4-context-claim-return-') as td:
            workspace = Path(td)
            fact = workspace/'fact.json'; plan = workspace/'plan.json'
            fact.write_text('{}', encoding='utf-8'); plan.write_text('{}', encoding='utf-8')
            state = self._state()
            with mock.patch.object(controller.supervisor, 'verify_controller_binding'), \
                 mock.patch.object(controller.production_binding, 'bind_plan', return_value={}), \
                 mock.patch.object(controller.core, 'load', return_value=(state, workspace/'state.json')), \
                 mock.patch.object(controller.core, 'save'), \
                 mock.patch.object(controller.core, 'cmd_context', side_effect=controller.core.Fail('AUTHORING_CONTRACT_FAIL:FACT_PACK_CLAIM_COUNT_INVALID')):
                rc = controller._guarded_context(['controller.py','context',str(workspace),str(fact),str(plan)])
            self.assertEqual(rc, 4)
            self.assertEqual(state['phase'], 'FACT_CHECK_REQUIRED')
            self.assertIsNone(state['facts'])

    def test_negative_context_path_keeps_unknown_failure_hard(self):
        with tempfile.TemporaryDirectory(prefix='s4-context-hard-') as td:
            workspace = Path(td)
            fact = workspace/'fact.json'; plan = workspace/'plan.json'
            fact.write_text('{}', encoding='utf-8'); plan.write_text('{}', encoding='utf-8')
            state = self._state()
            with mock.patch.object(controller.supervisor, 'verify_controller_binding'), \
                 mock.patch.object(controller.production_binding, 'bind_plan', return_value={}), \
                 mock.patch.object(controller.core, 'load', return_value=(state, workspace/'state.json')), \
                 mock.patch.object(controller.core, 'cmd_context', side_effect=controller.core.Fail('AUTHORING_CONTRACT_FAIL:OTHER_HARD_ERROR')):
                with self.assertRaisesRegex(controller.core.Fail, 'OTHER_HARD_ERROR'):
                    controller._guarded_context(['controller.py','context',str(workspace),str(fact),str(plan)])
            self.assertEqual(state['phase'], 'CONTEXT_REQUIRED')
            self.assertIsNotNone(state['facts'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
