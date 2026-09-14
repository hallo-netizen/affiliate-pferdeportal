import contextlib,hashlib,io,json,tempfile,unittest
from pathlib import Path
from unittest import mock

import batch_gate,controller,handoff_transport,production_checks
from live_route_test_support import start_to_context,valid_article

ROOT=Path(__file__).resolve().parent
PROOF=ROOT/'FIRST_FULL_RULE_TEST_ARTICLE_PROOF.json'

def sha_text(v):return hashlib.sha256(v.encode()).hexdigest()
def write_json(path,value):path.write_text(json.dumps(value,ensure_ascii=False,sort_keys=True),encoding='utf-8');return path
def run_main(argv):
 buf=io.StringIO()
 with contextlib.redirect_stdout(buf):rc=controller.main(argv)
 return rc,buf.getvalue()
def production_pass(state):
 d=state['draft_sha256'];return {'contract':'SYSTEM4_FULL_PRODUCTION_CHECK_V1','status':'PASS','checked_draft_sha256':d,'publish_allowed':False,'evidence':{'no_legacy':{'status':'PASS','legacy_import_count':0},'no_external_links':{'status':'PASS','external_link_count':0},'languagetool':{'status':'PASS','engine':'LanguageTool 6.8 / Bestand 43','finding_count':0},'ppm679':{'status':'PASS','ppm_version':'6.7.9','technical_status':'TECHNICAL_CHECK_OK','content_quality_status':'CONTENT_QUALITY_CHECK_OK','fail_closed_aggregate_status':'PASS','content_sha256':d,'language_evidence_source':'TEST_TRANSPORT_CHECKER_STUB_NOT_ACCEPTANCE'}}}
def handoff_from_states(states):
 rows=[]
 for index,state in enumerate(states):
  prod=state['checks']['production_evidence']['evidence'];rows.append({'index':index,'title':state['article']['title'],'target_keyword':state['article']['target_keyword'],'category':state['article']['category'],'article_type':state['article']['article_type'],'plan_slot':state['article']['plan_slot'],'final_draft_sha256':state['draft_sha256'],'revision_count':state['revision'],'body':state['draft_markdown'],'production_context':{'fact_pack':state['production_context']['fact_pack'],'production_plan_item':state['production_context']['production_plan_item']},'languagetool':prod['languagetool'],'ppm679':prod['ppm679']})
 return {'contract':handoff_transport.HANDOFF_CONTRACT,'batch_sha256':states[0]['batch_sha256'],'publish_allowed':False,'signing_deferred':True,'batch_gate_status':'SYSTEM4_BATCH_FULL_PASS_COLLECTED','no_legacy_status':'PASS','test_suite_status':'PASS','wordpress_review':{'file_format':'JSON','mime_type':'application/json','intended_next_step':'WORDPRESS_DIRECT_IMPORT','plugin_name':'Portal SEO Editorial Plan Compiler','plugin_version_verified_against':handoff_transport.DIRECT_IMPORT_PLUGIN_VERSION,'ppm_version_verified_against':'6.7.9','direct_wordpress_upload_ready':True,'direct_upload_block_reason':None,'required_downstream_components':[]},'articles':rows}

class LocalEndToEndChatHandoffTests(unittest.TestCase):
 def test_authoritative_textmachine_bindings_are_unchanged_from_proven_full_rule_pass(self):
  proof=json.loads(PROOF.read_text());self.assertEqual(production_checks.PPM_VERSION,proof['authoritative_tool_bindings']['ppm']['version']);self.assertEqual(production_checks.PPM_PACKAGE_SHA256,proof['authoritative_tool_bindings']['ppm']['package_sha256']);self.assertEqual(production_checks.LT_ENGINE,proof['authoritative_tool_bindings']['languagetool']['engine']);self.assertEqual(production_checks.LT_JAR_SHA256,proof['authoritative_tool_bindings']['languagetool']['commandline_jar_sha256']);ppm=ROOT.parent/production_checks.PPM_PACKAGE_REL;self.assertTrue(ppm.is_file());self.assertEqual(production_checks.file_sha256(ppm),production_checks.PPM_PACKAGE_SHA256)

 def test_positive_point0_to_exact_parent_chat_json_transport(self):
  with tempfile.TemporaryDirectory(prefix='system4-local-e2e-') as td:
   root=Path(td);paths=[];bodies=[];snapshot_path=None
   def checker(repo,state,fact_pack,plan):return production_pass(state)
   with mock.patch.object(controller.production_checks,'run_all',side_effect=checker):
    for index in range(7):
     workspace,snapshot,state=start_to_context(root,index);snapshot_path=snapshot;body=valid_article(state,index,f'e2e{index}');draft=root/f'article-{index}.html';draft.write_text(body,encoding='utf-8');self.assertEqual(run_main(['controller.py','draft',str(workspace),str(draft)])[0],0);self.assertEqual(run_main(['controller.py','fullcheck',str(workspace)])[0],0);final=json.loads((workspace/'state.json').read_text());self.assertEqual(final['phase'],'OUTPUT_GATE_REQUIRED');self.assertEqual(final['draft_markdown'],body);self.assertFalse(final['publish_allowed']);paths.append(workspace/'state.json');bodies.append(body)
   batch_out=root/'batch';collected=batch_gate.collect_batch(snapshot_path,paths,batch_out);self.assertEqual(collected['status'],'SYSTEM4_BATCH_FULL_PASS_COLLECTED');self.assertEqual(collected['article_count'],7);evidence=json.loads((batch_out/'system4_batch_evidence.json').read_text());self.assertFalse(evidence['content_mutation_performed']);self.assertFalse(evidence['design_mutation_performed']);self.assertEqual([r['content_utf8'] for r in evidence['articles']],bodies)
   states=[json.loads(p.read_text()) for p in paths];source=write_json(root/'handoff-source.json',handoff_from_states(states));canonical=root/handoff_transport.HANDOFF_FILENAME;canonical_bytes=handoff_transport.canonicalize_handoff(source,canonical);inline=root/handoff_transport.INLINE_FILENAME;envelope=handoff_transport.inline_pack(canonical,inline);reconstructed=handoff_transport.inline_unpack(inline,root/'parent-chat');self.assertEqual(reconstructed.read_bytes(),canonical_bytes);self.assertEqual(envelope['plaintext_sha256'],hashlib.sha256(canonical_bytes).hexdigest());payload=json.loads(reconstructed.read_text());self.assertFalse(payload['publish_allowed']);self.assertTrue(payload['wordpress_review']['direct_wordpress_upload_ready']);self.assertEqual([r['body'] for r in payload['articles']],bodies)

 def test_negative_design_drift_is_blocked_before_fullcheck(self):
  with tempfile.TemporaryDirectory(prefix='system4-local-neg-design-') as td:
   root=Path(td);workspace,_,state=start_to_context(root,0);body=valid_article(state,0);bad=body.replace('system-129-table comparison-table','comparison-table');p=root/'bad.html';p.write_text(bad,encoding='utf-8');rc,out=run_main(['controller.py','draft',str(workspace),str(p)]);self.assertEqual(rc,2);self.assertIn('ARTICLE_DESIGN_GUARD_FAIL:DESIGN_TABLE_SYSTEM129_CLASS_MISSING',out);after=json.loads((workspace/'state.json').read_text());self.assertEqual(after['phase'],'DRAFT_REQUIRED');self.assertIsNone(after['draft_markdown'])

 def test_negative_fake_fact_remains_blocked_by_content_guard(self):
  import content_guard
  evidence='Dies ist ein ausreichend langer echter Quellenbeleg für den Negativtest.';research={'contract':'SYSTEM4_RESEARCH_EVIDENCE_V1','sources':[{'source_id':'src','source_title':'Echte Fachquelle','source_url':'https://example.org/source','retrieved_at':'2026-09-14T00:00:00Z','snapshot_sha256':sha_text(evidence),'evidence':evidence}]};invented='Dieser erfundene Beleg steht nicht im gebundenen Quellenausschnitt und muss blockieren.';facts={'contract':'SYSTEM4_FACTS_EVIDENCE_V1','claims':[{'fact_id':'f1','source_id':'src','statement':'Eine ausreichend lange erste Aussage für den Test.','evidence_text':invented,'evidence_text_sha256':sha_text(invented)},{'fact_id':'f2','source_id':'src','statement':'Eine ausreichend lange zweite Aussage für den Test.','evidence_text':invented+' zwei','evidence_text_sha256':sha_text(invented+' zwei')}]}
  with self.assertRaisesRegex(content_guard.ContentGuardError,'FACT_EVIDENCE_NOT_IN_SOURCE'):content_guard.validate_facts_document(facts,research)

 def test_negative_cross_article_template_reuse_is_blocked(self):
  import content_guard
  common='<article>'+' '.join(['gleiches wiederverwendetes textmuster']*120)+'</article>'
  with self.assertRaisesRegex(content_guard.ContentGuardError,'BATCH_TEMPLATE_REUSE_BLOCKED'):content_guard.validate_batch_distinctness([common,common])

if __name__=='__main__':unittest.main(verbosity=2)
