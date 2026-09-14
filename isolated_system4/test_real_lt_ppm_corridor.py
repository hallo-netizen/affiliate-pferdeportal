import hashlib,json,os,tempfile,unittest
from pathlib import Path

import batch_gate,controller,handoff_transport,production_checks
from live_route_test_support import REPO,start_to_context,valid_article,write_json


def handoff_from_states(states):
    rows=[]
    for index,state in enumerate(states):
        prod=state['checks']['production_evidence']['evidence']
        rows.append({
            'index':index,
            'title':state['article']['title'],
            'target_keyword':state['article']['target_keyword'],
            'category':state['article']['category'],
            'article_type':state['article']['article_type'],
            'plan_slot':state['article']['plan_slot'],
            'final_draft_sha256':state['draft_sha256'],
            'revision_count':state['revision'],
            'body':state['draft_markdown'],
            'production_context':{
                'fact_pack':state['production_context']['fact_pack'],
                'production_plan_item':state['production_context']['production_plan_item'],
            },
            'languagetool':prod['languagetool'],
            'ppm679':prod['ppm679'],
        })
    return {
        'contract':handoff_transport.HANDOFF_CONTRACT,
        'batch_sha256':states[0]['batch_sha256'],
        'publish_allowed':False,
        'signing_deferred':True,
        'batch_gate_status':'SYSTEM4_BATCH_FULL_PASS_COLLECTED',
        'no_legacy_status':'PASS',
        'test_suite_status':'PASS',
        'wordpress_review':{
            'file_format':'JSON',
            'mime_type':'application/json',
            'intended_next_step':'WORDPRESS_DIRECT_IMPORT',
            'plugin_name':'Portal SEO Editorial Plan Compiler',
            'plugin_version_verified_against':handoff_transport.DIRECT_IMPORT_PLUGIN_VERSION,
            'ppm_version_verified_against':'6.7.9',
            'direct_wordpress_upload_ready':True,
            'direct_upload_block_reason':None,
            'required_downstream_components':[],
        },
        'articles':rows,
    }


@unittest.skipUnless(os.environ.get('SYSTEM4_REAL_TOOL_CORRIDOR')=='1','real tool corridor is an explicit CI stage')
class RealLtPpmCorridorTests(unittest.TestCase):
    def test_three_articles_real_lt68_ppm679_batch_handoff_byte_equal(self):
        jar=Path(os.environ.get('SYSTEM4_LANGUAGETOOL_JAR',''))
        self.assertTrue(jar.is_file(),'exact LanguageTool jar missing')
        with tempfile.TemporaryDirectory(prefix='system4-real-tools-') as td:
            root=Path(td)
            state_paths=[]
            states=[]
            bodies=[]
            snapshot_path=None
            for index in range(3):
                workspace,snapshot,state=start_to_context(root,index)
                snapshot_path=snapshot
                body=valid_article(state,index,f'Praxis{index}')
                try:
                    production_checks.run_languagetool(REPO,body)
                except production_checks.RepairRequired as exc:
                    self.fail(f'ARTICLE_{index}_REAL_LT68_FINDINGS:'+json.dumps(exc.findings,ensure_ascii=False,sort_keys=True))
                draft=root/f'article-{index}.html';draft.write_text(body,encoding='utf-8')
                self.assertEqual(controller.main(['controller.py','draft',str(workspace),str(draft)]),0)
                rc=controller.main(['controller.py','fullcheck',str(workspace)])
                final=json.loads((workspace/'state.json').read_text(encoding='utf-8'))
                if rc==3:
                    self.fail(f'ARTICLE_{index}_REAL_TOOL_REPAIR_REQUIRED:'+json.dumps(final.get('last_error'),ensure_ascii=False,sort_keys=True))
                self.assertEqual(rc,0,f'ARTICLE_{index}_REAL_TOOL_HARD_BLOCK:'+str(final.get('last_error')))
                self.assertEqual(final['phase'],'OUTPUT_GATE_REQUIRED')
                evidence=final['checks']['production_evidence']['evidence']
                self.assertEqual(evidence['languagetool']['engine'],'LanguageTool 6.8 / Bestand 43')
                self.assertEqual(evidence['languagetool']['finding_count'],0)
                self.assertEqual(evidence['ppm679']['ppm_version'],'6.7.9')
                self.assertEqual(evidence['ppm679']['technical_status'],'TECHNICAL_CHECK_OK')
                self.assertEqual(evidence['ppm679']['content_quality_status'],'CONTENT_QUALITY_CHECK_OK')
                self.assertEqual(evidence['ppm679']['fail_closed_aggregate_status'],'PASS')
                self.assertEqual(evidence['ppm679']['content_sha256'],final['draft_sha256'])
                self.assertEqual(final['draft_markdown'],body)
                self.assertFalse(final['publish_allowed'])
                state_paths.append(workspace/'state.json')
                states.append(final)
                bodies.append(body)

            self.assertIsNotNone(snapshot_path)
            batch_out=root/'batch'
            collected=batch_gate.collect_batch(snapshot_path,state_paths,batch_out)
            self.assertEqual(collected['status'],'SYSTEM4_BATCH_FULL_PASS_COLLECTED')
            self.assertEqual(collected['article_count'],3)
            batch_evidence=json.loads((batch_out/'system4_batch_evidence.json').read_text(encoding='utf-8'))
            self.assertFalse(batch_evidence['content_mutation_performed'])
            self.assertFalse(batch_evidence['design_mutation_performed'])
            self.assertEqual([row['content_utf8'] for row in batch_evidence['articles']],bodies)

            source=write_json(root/'handoff-source.json',handoff_from_states(states))
            canonical=root/handoff_transport.HANDOFF_FILENAME
            canonical_bytes=handoff_transport.canonicalize_handoff(source,canonical)
            inline=root/handoff_transport.INLINE_FILENAME
            envelope=handoff_transport.inline_pack(canonical,inline)
            reconstructed=handoff_transport.inline_unpack(inline,root/'parent-chat')
            self.assertEqual(reconstructed.read_bytes(),canonical_bytes)
            self.assertEqual(envelope['plaintext_sha256'],hashlib.sha256(canonical_bytes).hexdigest())
            payload=json.loads(reconstructed.read_text(encoding='utf-8'))
            self.assertFalse(payload['publish_allowed'])
            self.assertTrue(payload['wordpress_review']['direct_wordpress_upload_ready'])
            self.assertEqual(len(payload['articles']),3)
            self.assertEqual([row['body'] for row in payload['articles']],bodies)
            self.assertEqual(
                [row['final_draft_sha256'] for row in payload['articles']],
                [hashlib.sha256(body.encode('utf-8')).hexdigest() for body in bodies],
            )

if __name__=='__main__':unittest.main(verbosity=2)
