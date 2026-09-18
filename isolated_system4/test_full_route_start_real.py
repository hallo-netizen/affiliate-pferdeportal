from __future__ import annotations
import hashlib,json,os,re,sys,tempfile,unittest
from pathlib import Path
from unittest import mock

import batch_repetition_guard,full_route_start,full_route_test_worker,handoff_transport,production_checks
from full_route_test_fixture import FOUR_ITEMS,SINGLE_ITEMS,THREE_ITEMS,write_start_fixture

HERE=Path(__file__).resolve().parent
WORKER=[sys.executable,str(HERE/'full_route_test_worker.py')]

@unittest.skipUnless(os.environ.get('SYSTEM4_REAL_TOOL_CORRIDOR')=='1','real tool corridor is an explicit CI stage')
class FullRouteStartRealTests(unittest.TestCase):
    def _run(self,items,prefix,expect_batch_workshop=False,expect_block_workshop=False):
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
            evidence_path=out/'batch/system4_batch_evidence.json'
            self.assertTrue(evidence_path.is_file())
            evidence=json.loads(evidence_path.read_text(encoding='utf-8'))
            if expect_block_workshop:
                request_path=out/'item-0/GLOBAL_WORKSHOP_REQUEST.json'
                self.assertTrue(request_path.is_file())
                request=json.loads(request_path.read_text(encoding='utf-8'))
                self.assertTrue(request['repairable'])
                self.assertEqual(request['origin_stage'],'DRAFT_BLOCK_SEMANTICS')
                self.assertEqual(request['findings'][0]['error_code'],'BLOCK_CONTENT_SEMANTIC_HEADING_MISMATCH')
                self.assertEqual(request['findings'][0]['field_path'],'content.blocks.conclusion')
                self.assertTrue((out/'worker-draft-workshop-repair-0.html').is_file())
                body=payload['articles'][0]['body']
                conclusion=re.search(r'(?is)<section data-block="conclusion">.*?<h2[^>]*>(.*?)</h2>',body)
                self.assertIsNotNone(conclusion)
                repaired_heading=re.sub(r'(?is)<[^>]+>',' ',conclusion.group(1)).strip()
                self.assertTrue(repaired_heading.startswith('Abschließende Bewertung zu '),repaired_heading)
                self.assertGreaterEqual(payload['articles'][0]['revision_count'],2)
            if expect_batch_workshop:
                request_path=out/'batch/GLOBAL_WORKSHOP_REQUEST.json'
                if not request_path.is_file():
                    bodies=[row['body'] for row in payload['articles']]
                    findings=batch_repetition_guard.repeated_sentence_findings(bodies)
                    presence=[
                        [sentence in body for sentence in full_route_test_worker.BATCH_REPEAT_SENTENCES]
                        for body in bodies
                    ]
                    diagnostic={
                        'majority_repeated_sentence_count':len(findings),
                        'finding_sentences':[row.get('sentence') for row in findings],
                        'forced_sentence_presence_by_article':presence,
                        'revision_counts':[row.get('revision_count') for row in payload['articles']],
                    }
                    self.fail('BATCH_WORKSHOP_REQUEST_MISSING:'+json.dumps(diagnostic,ensure_ascii=False,sort_keys=True,separators=(',',':')))
                request=json.loads(request_path.read_text(encoding='utf-8'))
                self.assertTrue(request['repairable'])
                self.assertEqual(request['origin_stage'],'BATCH')
                self.assertTrue(str(request['error_code']).startswith('BATCH_REPEATED_SENTENCE_TEMPLATE_BLOCKED:'))
                self.assertGreaterEqual(request['finding_count'],7)
                self.assertEqual(set(request['repair_targets']),{'3'})
                self.assertTrue((out/'worker-batch-repair-3-1.html').is_file())
                self.assertEqual(evidence['batch_repetition']['status'],'PASS')
                self.assertLessEqual(evidence['batch_repetition']['majority_repeated_sentence_count'],6)
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

    def test_wrong_conclusion_heading_goes_workshop_worker_repair_fullcheck_pass(self):
        old=os.environ.get('SYSTEM4_TEST_FORCE_BLOCK_SEMANTIC_ERROR_INDEX')
        os.environ['SYSTEM4_TEST_FORCE_BLOCK_SEMANTIC_ERROR_INDEX']='0'
        try:
            payload=self._run(SINGLE_ITEMS,'s4-start-block-semantic-repair-',expect_block_workshop=True)
        finally:
            if old is None: os.environ.pop('SYSTEM4_TEST_FORCE_BLOCK_SEMANTIC_ERROR_INDEX',None)
            else: os.environ['SYSTEM4_TEST_FORCE_BLOCK_SEMANTIC_ERROR_INDEX']=old
        row=payload['articles'][0]
        self.assertEqual(row['languagetool']['finding_count'],0)
        self.assertEqual(row['ppm679']['fail_closed_aggregate_status'],'PASS')

    def test_four_article_batch_repetition_goes_workshop_repair_fullcheck_batch_pass(self):
        old=os.environ.get('SYSTEM4_TEST_FORCE_BATCH_REPETITION_COUNT')
        os.environ['SYSTEM4_TEST_FORCE_BATCH_REPETITION_COUNT']='4'
        try:
            payload=self._run(FOUR_ITEMS,'s4-start-four-batch-repair-',expect_batch_workshop=True)
        finally:
            if old is None: os.environ.pop('SYSTEM4_TEST_FORCE_BATCH_REPETITION_COUNT',None)
            else: os.environ['SYSTEM4_TEST_FORCE_BATCH_REPETITION_COUNT']=old
        self.assertEqual(len(payload['articles']),4)
        self.assertGreaterEqual(payload['articles'][3]['revision_count'],2)

    def test_true_languagetool_execution_failure_stays_terminal_and_never_invokes_repair_worker(self):
        with tempfile.TemporaryDirectory(prefix='s4-start-lt-hard-fail-') as td:
            root=Path(td);snap,sources=write_start_fixture(root,SINGLE_ITEMS);out=root/'out'
            with mock.patch.object(production_checks,'_run_languagetool_text',side_effect=production_checks.ProductionCheckError('LANGUAGETOOL_REAL_EXECUTION_FAILED:TEST')):
                with self.assertRaisesRegex(full_route_start.FullRouteError,'START_FULLCHECK_NOT_PASS:0:2'):
                    full_route_start.run(snap,sources,WORKER,out)
            self.assertEqual(list(out.glob('worker-repair-*.html')),[])

if __name__=='__main__':unittest.main(verbosity=2)
