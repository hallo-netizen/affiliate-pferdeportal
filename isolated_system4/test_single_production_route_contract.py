from __future__ import annotations
import json, unittest
from pathlib import Path

HERE=Path(__file__).resolve().parent
REPO=HERE.parent

class SingleProductionRouteContractTests(unittest.TestCase):
    def text(self, rel:str)->str:
        return (REPO/rel).read_text(encoding='utf-8')

    def test_single_start_and_no_legacy_codex_entry(self):
        override=self.text('AGENTS.override.md')
        runner=self.text('isolated_system4/production_route.py')
        self.assertIn('python3 isolated_system4/production_route.py start',override)
        self.assertIn('python3 isolated_system4/production_route.py current',override)
        self.assertIn('python3 isolated_system4/production_route.py finish',override)
        self.assertIn("'start-point0'",runner)
        self.assertIn('SYSTEM4_ROOT_POINT0_PASS:WORKER_DISPATCH_READY',runner)
        self.assertNotIn('codex_current_action.py',override)
        self.assertNotIn('fachworkflow_handoff',override)
        before=override.split('## Isolation',1)[0]
        self.assertNotIn('control/cloud-entry-gate/cloud_entry.py start',before)

    def test_one_to_n_is_owned_by_production_runner(self):
        runner=self.text('isolated_system4/production_route.py')
        for token in ('article_count','current_index',"while st['current_index'] < st['article_count']",'ITEM_INDEX_INVALID'):
            self.assertIn(token,runner)
        self.assertNotIn('== 7',runner)
        self.assertNotIn('!= 7',runner)

    def test_repair_has_one_system4_owner_path(self):
        override=self.text('AGENTS.override.md')
        controller=self.text('isolated_system4/controller.py')
        self.assertIn('controller.py fullcheck',override)
        self.assertIn('REPAIR_REQUIRED',override)
        self.assertIn('SYSTEM4_CONTROLLED_REPAIR_RETURN:',controller)
        self.assertNotIn('FACHWORKFLOW_REPAIR_REQUIRED',override)
        self.assertNotIn('submission_command',override)

    def test_batch_finish_is_mandatory_and_builds_v2(self):
        runner=self.text('isolated_system4/production_route.py')
        self.assertIn('batch_gate.collect_batch',runner)
        self.assertIn('SYSTEM4_BATCH_FULL_PASS_COLLECTED',runner)
        self.assertIn('handoff_transport.validate_handoff',runner)
        self.assertIn('SYSTEM4_PRODUCTION_HANDOFF_READY',runner)

    def test_v2_is_only_content_bridge_to_107008(self):
        bridge=self.text('control/startmaster0107/system4_v2_release_bridge.py')
        self.assertIn('handoff_transport.read_validate_handoff',bridge)
        self.assertIn('SYSTEM4_HANDOFF_RUNTIME_BATCH_MISMATCH',bridge)
        self.assertIn("'system4_handoff_contract':handoff_transport.HANDOFF_CONTRACT",bridge)
        self.assertIn("'content_mutation_performed':False", self.text('control/startmaster0107/chat_delivery_payload.py'))

    def test_107008_is_one_to_n(self):
        step=json.loads(self.text('control/startmaster0107/STEP_107008_FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH.json'))
        ins=step['instruction']
        for forbidden in ('article_count=7','sieben finalen Artikel','sieben bereits freigegebenen Artikel','sieben ARTICLE_<plan_slot>.md'):
            self.assertNotIn(forbidden,ins)
        self.assertIn('article_count>=1',ins)
        self.assertIn('SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2',ins)
        self.assertIn('system4_v2_release_bridge.py prepare',ins)

if __name__=='__main__': unittest.main()
