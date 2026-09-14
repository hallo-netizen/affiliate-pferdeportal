from __future__ import annotations
import hashlib,json,os,sys,tempfile,unittest
from pathlib import Path

import full_route_start,handoff_transport
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
        self.assertEqual(SINGLE_ITEMS[0]['target_keyword'],'Pferdehaftpflicht für Fremdreiter')
        self._run(SINGLE_ITEMS,'s4-start-one-new-')

    def test_three_genuinely_new_articles_from_single_start_button_to_file(self):
        expected=['UV-Schutz bei Fliegenmasken','Pellets aus Luzerne als Heuersatz','Pferdehaftpflicht für Pferdehüter']
        self.assertEqual([x['target_keyword'] for x in THREE_ITEMS],expected)
        self.assertEqual(len({x['plan_slot'] for x in THREE_ITEMS}),3)
        self._run(THREE_ITEMS,'s4-start-three-new-')

if __name__=='__main__':unittest.main(verbosity=2)
