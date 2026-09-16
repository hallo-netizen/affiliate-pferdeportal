from __future__ import annotations
import hashlib,json,os,sys,tempfile,unittest
from pathlib import Path
from unittest import mock

import full_route_start,handoff_transport,production_checks
from full_route_test_fixture import SINGLE_ITEMS,THREE_ITEMS,write_start_fixture

HERE=Path(__file__).resolve().parent
WORKER=[sys.executable,str(HERE/'full_route_test_worker.py')]

@unittest.skipUnless(os.environ.get('SYSTEM4_REAL_TOOL_CORRIDOR')=='1','real tool corridor is an explicit CI stage')
class FullRouteStartRealTests(unittest.TestCase):
    def _run(self,items,prefix):
        with tempfile.TemporaryDirectory(prefix=prefix) as td:
            root=Path(td);snap,sources=write_start_fixture(root,items);out=root/'out'
            final=full_route_start.run(snap,sources,WORKER,out)
            self.assertTrue(final.is_file())
            payload=json.loads(final.read_text(encoding='utf-8'))
            self.assertFalse(payload['publish_allowed'])
            self.assertEqual(len(payload['articles']),len(items))
            self.assertEqual([row['target_keyword'] for row in payload['articles']],[row['target_keyword'] for row in items])
            self.assertEqual([row['plan_slot'] for row in payload['articles']],[row['plan_slot'] for row in items])
            for row in payload['articles']:
                self.assertEqual(row['languagetool']['engine'],'LanguageTool 6.8 / Bestand 43')
                self.assertEqual(row['languagetool']['finding_count'],0)
                self.assertEqual(row['ppm679']['ppm_version'],'6.7.9')
                self.assertEqual(row['ppm679']['technical_status'],'TECHNICAL_CHECK_OK')
                self.assertEqual(row['ppm679']['content_quality_status'],'CONTENT_QUALITY_CHECK_OK')
                self.assertEqual(row['ppm679']['fail_closed_aggregate_status'],'PASS')
                self.assertEqual(row['final_draft_sha256'],hashlib.sha256(row['body'].encode('utf-8')).hexdigest())
            canonical=(out/handoff_transport.HANDOFF_FILENAME).read_bytes()
            self.assertEqual(final.read_bytes(),canonical)
            self.assertTrue((out/'batch/system4_batch_evidence.json').is_file())
            return payload

    def test_one_genuinely_new_article_from_single_start_button_to_file(self):
        self.assertEqual(SINGLE_ITEMS[0]['target_keyword'],'Haftpflicht für Pferde bei Pflegebeteiligung')
        self._run(SINGLE_ITEMS,'s4-start-one-fresh-')

    def test_three_genuinely_new_articles_from_single_start_button_to_file(self):
        expected=['Fliegenmasken für Pferde an sonnigen Tagen','Pellets aus Luzerne für Pferde im Winter','Haftpflicht für Pferde bei Betreuung im Urlaub']
        self.assertEqual([x['target_keyword'] for x in THREE_ITEMS],expected)
        self.assertEqual(len({x['plan_slot'] for x in THREE_ITEMS}),3)
        self._run(THREE_ITEMS,'s4-start-three-fresh-')

    def test_repairable_languagetool_finding_returns_same_article_to_worker_then_passes(self):
        old=os.environ.get('SYSTEM4_TEST_FORCE_REPAIR_INDEX')
        os.environ['SYSTEM4_TEST_FORCE_REPAIR_INDEX']='0'
        try:
            payload=self._run(SINGLE_ITEMS,'s4-start-real-repair-')
        finally:
            if old is None: os.environ.pop('SYSTEM4_TEST_FORCE_REPAIR_INDEX',None)
            else: os.environ['SYSTEM4_TEST_FORCE_REPAIR_INDEX']=old
        self.assertGreaterEqual(payload['articles'][0]['revision_count'],2)

    def test_true_languagetool_execution_failure_stays_terminal_and_never_invokes_repair_worker(self):
        with tempfile.TemporaryDirectory(prefix='s4-start-lt-hard-fail-') as td:
            root=Path(td);snap,sources=write_start_fixture(root,SINGLE_ITEMS);out=root/'out'
            with mock.patch.object(production_checks,'_run_languagetool_text',side_effect=production_checks.ProductionCheckError('LANGUAGETOOL_REAL_EXECUTION_FAILED:TEST')):
                with self.assertRaisesRegex(full_route_start.FullRouteError,'START_FULLCHECK_NOT_PASS:0:2'):
                    full_route_start.run(snap,sources,WORKER,out)
            self.assertEqual(list(out.glob('worker-repair-*.html')),[])

if __name__=='__main__':unittest.main(verbosity=2)
