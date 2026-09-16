import hashlib,json,os,tempfile,unittest
from pathlib import Path
from unittest import mock

import batch_gate,controller,handoff_transport,no_codex_test_repair,production_checks,repair_router
from live_route_test_support import REPO,write_json
from real_route_test_support import start_to_context_real,valid_real_article


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
    def _fullcheck_with_existing_same_article_repair(self,root,workspace,index):
        before=json.loads((workspace/'state.json').read_text(encoding='utf-8'))
        article_identity=dict(before['article'])
        immutable_identity=before['immutable_core_sha256']
        repairs=0
        while True:
            rc=controller.main(['controller.py','fullcheck',str(workspace)])
            current=json.loads((workspace/'state.json').read_text(encoding='utf-8'))
            if rc==0:
                self.assertEqual(current['article'],article_identity)
                self.assertEqual(current['immutable_core_sha256'],immutable_identity)
                return current,repairs
            self.assertEqual(rc,3,f'ARTICLE_{index}_REAL_TOOL_HARD_BLOCK:'+str(current.get('last_error')))
            request_path=workspace/'machine_repair_request.json'
            self.assertTrue(request_path.is_file(),f'ARTICLE_{index}_REPAIR_REQUEST_MISSING')
            request=json.loads(request_path.read_text(encoding='utf-8'))
            repair_router.verify_continuation_result(workspace,request)
            self.assertEqual(request['status'],'SAME_ARTICLE_BODY_REPAIR')
            self.assertEqual(request['owner'],'DRAFT_BODY')
            self.assertEqual(request['target'],'SAME_ARTICLE_BODY')
            self.assertEqual(request['article'],article_identity)
            candidate=no_codex_test_repair.candidate_for_current_failure(REPO,workspace)
            repair_path=root/f'article-{index}-repair-{repairs+1}.html'
            repair_path.write_text(candidate,encoding='utf-8')
            self.assertEqual(controller.main(['controller.py','repair',str(workspace),str(repair_path)]),0)
            repaired=json.loads((workspace/'state.json').read_text(encoding='utf-8'))
            self.assertEqual(repaired['article'],article_identity)
            self.assertEqual(repaired['immutable_core_sha256'],immutable_identity)
            self.assertEqual(repaired['phase'],'CHECK_REQUIRED')
            repairs+=1
            self.assertLessEqual(repairs,repair_router.MAX_MACHINE_REPAIR_CYCLES,'REAL_TOOL_REPAIR_CYCLE_LIMIT_EXCEEDED')

    def test_three_articles_real_sources_lt68_ppm679_batch_handoff_byte_equal(self):
        jar=Path(os.environ.get('SYSTEM4_LANGUAGETOOL_JAR',''))
        self.assertTrue(jar.is_file(),'exact LanguageTool jar missing')
        with tempfile.TemporaryDirectory(prefix='system4-real-tools-') as td:
            root=Path(td)
            state_paths=[]
            states=[]
            bodies=[]
            snapshot_path=None
            total_repairs=0
            for index in range(3):
                workspace,snapshot,state=start_to_context_real(root,index)
                snapshot_path=snapshot
                source=state['production_context']['fact_pack']['sources'][0]
                self.assertTrue(source['source_url'].startswith('https://'))
                self.assertNotIn('example.org',source['source_url'])
                self.assertEqual(source['source_kind'],'PARENT_CHAT_REAL_WEB_SNAPSHOT')
                body=valid_real_article(state,index)
                draft=root/f'article-{index}.html';draft.write_text(body,encoding='utf-8')
                self.assertEqual(controller.main(['controller.py','draft',str(workspace),str(draft)]),0)
                final,repairs=self._fullcheck_with_existing_same_article_repair(root,workspace,index)
                total_repairs+=repairs
                self.assertEqual(final['phase'],'OUTPUT_GATE_REQUIRED')
                evidence=final['checks']['production_evidence']['evidence']
                self.assertEqual(evidence['languagetool']['engine'],'LanguageTool 6.8 / Bestand 43')
                self.assertEqual(evidence['languagetool']['finding_count'],0)
                self.assertEqual(evidence['ppm679']['ppm_version'],'6.7.9')
                self.assertEqual(evidence['ppm679']['technical_status'],'TECHNICAL_CHECK_OK')
                self.assertEqual(evidence['ppm679']['content_quality_status'],'CONTENT_QUALITY_CHECK_OK')
                self.assertEqual(evidence['ppm679']['fail_closed_aggregate_status'],'PASS')
                self.assertEqual(evidence['ppm679']['content_sha256'],final['draft_sha256'])
                self.assertFalse(final['publish_allowed'])
                state_paths.append(workspace/'state.json')
                states.append(final)
                bodies.append(final['draft_markdown'])

            self.assertGreater(total_repairs,0,'REAL_REPAIRABLE_LT_PPM_FINDING_WAS_NOT_EXERCISED')
            self.assertIsNotNone(snapshot_path)
            self.assertEqual(len({state['batch_sha256'] for state in states}),1)
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

    def test_real_invalid_lt_jar_remains_terminal_block(self):
        with tempfile.TemporaryDirectory(prefix='system4-real-lt-hard-block-') as td:
            root=Path(td)
            workspace,_,state=start_to_context_real(root,0)
            body=valid_real_article(state,0)
            draft=root/'article.html';draft.write_text(body,encoding='utf-8')
            self.assertEqual(controller.main(['controller.py','draft',str(workspace),str(draft)]),0)
            fake=root/'invalid-languagetool.jar';fake.write_bytes(b'not-the-bound-languagetool-6.8-jar')
            with mock.patch.dict(os.environ,{'SYSTEM4_LANGUAGETOOL_JAR':str(fake)},clear=False):
                rc=controller.main(['controller.py','fullcheck',str(workspace)])
            final=json.loads((workspace/'state.json').read_text(encoding='utf-8'))
            self.assertEqual(rc,2)
            self.assertEqual(final['phase'],'CHECK_REQUIRED')
            self.assertNotEqual(final.get('checks',{}).get('status'),'PASS')
            self.assertFalse((workspace/'machine_repair_request.json').exists())

if __name__=='__main__':unittest.main(verbosity=2)