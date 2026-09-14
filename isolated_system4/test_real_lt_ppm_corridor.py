import json,os,tempfile,unittest
from pathlib import Path

import controller,production_checks
from live_route_test_support import REPO,start_to_context,valid_article


@unittest.skipUnless(os.environ.get('SYSTEM4_REAL_TOOL_CORRIDOR')=='1','real tool corridor is an explicit CI stage')
class RealLtPpmCorridorTests(unittest.TestCase):
    def test_one_article_reaches_real_lt68_and_real_ppm679(self):
        jar=Path(os.environ.get('SYSTEM4_LANGUAGETOOL_JAR',''))
        self.assertTrue(jar.is_file(),'exact LanguageTool jar missing')
        with tempfile.TemporaryDirectory(prefix='system4-real-tools-') as td:
            root=Path(td)
            workspace,_,state=start_to_context(root,0)
            body=valid_article(state,0,'realpruefung')
            try:
                production_checks.run_languagetool(REPO,body)
            except production_checks.RepairRequired as exc:
                self.fail('REAL_LT68_FINDINGS:'+json.dumps(exc.findings,ensure_ascii=False,sort_keys=True))
            draft=root/'article.html'; draft.write_text(body,encoding='utf-8')
            self.assertEqual(controller.main(['controller.py','draft',str(workspace),str(draft)]),0)
            rc=controller.main(['controller.py','fullcheck',str(workspace)])
            final=json.loads((workspace/'state.json').read_text(encoding='utf-8'))
            if rc==3:
                self.fail('REAL_TOOL_CORRIDOR_REPAIR_REQUIRED:'+json.dumps(final.get('last_error'),ensure_ascii=False,sort_keys=True))
            self.assertEqual(rc,0,'REAL_TOOL_CORRIDOR_HARD_BLOCK:'+str(final.get('last_error')))
            self.assertEqual(final['phase'],'OUTPUT_GATE_REQUIRED')
            evidence=final['checks']['production_evidence']['evidence']
            self.assertEqual(evidence['languagetool']['engine'],'LanguageTool 6.8 / Bestand 43')
            self.assertEqual(evidence['languagetool']['finding_count'],0)
            self.assertEqual(evidence['ppm679']['ppm_version'],'6.7.9')
            self.assertEqual(evidence['ppm679']['technical_status'],'TECHNICAL_CHECK_OK')
            self.assertEqual(evidence['ppm679']['content_quality_status'],'CONTENT_QUALITY_CHECK_OK')
            self.assertEqual(evidence['ppm679']['fail_closed_aggregate_status'],'PASS')
            self.assertEqual(evidence['ppm679']['content_sha256'],final['draft_sha256'])

if __name__=='__main__':unittest.main(verbosity=2)
