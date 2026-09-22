import tempfile
import unittest
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE))
import runner

class RunnerTests(unittest.TestCase):
    def test_positive_one_article(self):
        with tempfile.TemporaryDirectory() as td:
            result=runner.execute(runner.simulation_binding(1),Path(td),'simulation')
            self.assertEqual(result['item_count'],1)
            self.assertEqual(result['articles'][0]['revision_count'],1)
            self.assertEqual(result['articles'][0]['checks']['languagetool']['status'],'PASS')
            self.assertEqual(result['articles'][0]['checks']['ppm']['status'],'PASS')
            self.assertTrue((Path(td)/'CONCEPT_AGENT_CHAT_HANDOFF_V1.json').is_file())

    def test_positive_three_articles_repair_isolated(self):
        with tempfile.TemporaryDirectory() as td:
            result=runner.execute(runner.simulation_binding(3),Path(td),'simulation',force_repair_index=1)
            self.assertEqual([x['revision_count'] for x in result['articles']],[1,2,1])
            events=result['event_log']
            item0_pass=next(i for i,e in enumerate(events) if e['event']=='ITEM_PASS' and e['item_index']==0)
            item1_start=next(i for i,e in enumerate(events) if e['event']=='ITEM_START' and e['item_index']==1)
            item1_pass=next(i for i,e in enumerate(events) if e['event']=='ITEM_PASS' and e['item_index']==1)
            item2_start=next(i for i,e in enumerate(events) if e['event']=='ITEM_START' and e['item_index']==2)
            self.assertLess(item0_pass,item1_start)
            self.assertLess(item1_pass,item2_start)

    def test_negative_binding_tamper(self):
        binding=runner.simulation_binding(1)
        binding['publish_allowed']=True
        with self.assertRaisesRegex(runner.Blocked,'PUBLISH_MUST_BE_FALSE'):
            runner.normalize_binding(binding)

    def test_negative_order_tamper(self):
        binding=runner.simulation_binding(3)
        binding['items'][1]['item_index']=2
        with self.assertRaisesRegex(runner.Blocked,'ITEM_ORDER_MISMATCH'):
            runner.normalize_binding(binding)

    def test_negative_duplicate_slot(self):
        binding=runner.simulation_binding(2)
        binding['items'][1]['plan_slot']=binding['items'][0]['plan_slot']
        with self.assertRaisesRegex(runner.Blocked,'PLAN_SLOT_DUPLICATE'):
            runner.normalize_binding(binding)

    def test_negative_premature_next_proof(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaisesRegex(runner.Blocked,'PREMATURE_NEXT_ITEM_BLOCKED'):
                runner.execute(runner.simulation_binding(3),Path(td),'simulation',negative_case='premature-next')

    def test_handoff_hash_is_self_consistent(self):
        with tempfile.TemporaryDirectory() as td:
            result=runner.execute(runner.simulation_binding(1),Path(td),'simulation')
            copy=dict(result); declared=copy.pop('handoff_sha256')
            self.assertEqual(declared,runner.stable(copy))

if __name__=='__main__': unittest.main(verbosity=2)
