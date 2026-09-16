import hashlib,json,tempfile,unittest,subprocess,sys
from pathlib import Path
from unittest import mock
import full_chain as full_chain_module
from full_chain import FullChainSupervisor, FullChainError
from capsule import CapsuleError

def sha(s): return hashlib.sha256(s.encode()).hexdigest()

def snapshot(path,count=2):
    items=[]
    for i in range(count):
        items.append({'title':f'Titel {i}','target_keyword':f'Keyword {i}','category':f'cat-{i}','article_type':'Beratung','plan_slot':hashlib.sha256(f'slot-{i}'.encode()).hexdigest()})
    b={'contract':'PSERC_TEXTMACHINE_METADATA_BATCH_V2','status':'READY_FOR_TEXTMACHINE_METADATA_INTAKE','batch_sha256':hashlib.sha256(b'batch').hexdigest(),'item_count':count,'items':items,'publish_allowed':False}
    path.write_text(json.dumps({'next_textmachine_metadata_batch':b})); return items

def evidence(req):
    idx=req['article']['title'].split()[-1]
    e1=f'Gesicherter konkreter Beleg A für Artikel {idx} mit eindeutiger fachlicher Aussage und sicherer Nutzung.'
    e2=f'Gesicherter konkreter Beleg B für Artikel {idx} mit einer zweiten fachlichen Aussage zur Auswahl.'
    ev=e1+'\\n'+e2+'\\n'+f'Zusätzlicher gesicherter Quellenkontext für Artikel {idx}.'
    sid=f'src-{idx}'
    src={'source_id':sid,'source_title':f'Fachquelle {idx}','source_url':f'https://example.org/source-{idx}','retrieved_at':'2026-09-13T08:00:00Z','snapshot_sha256':sha(ev),'evidence':ev}
    claims=[{'fact_id':f'f-{idx}-a','source_id':sid,'statement':f'Konkrete erste Aussage für Artikel {idx}.','evidence_text':e1,'evidence_text_sha256':sha(e1)},{'fact_id':f'f-{idx}-b','source_id':sid,'statement':f'Konkrete zweite Aussage für Artikel {idx}.','evidence_text':e2,'evidence_text_sha256':sha(e2)}]
    research={'contract':'SYSTEM4_RESEARCH_EVIDENCE_V1','sources':[src]}
    facts={'contract':'SYSTEM4_FACTS_EVIDENCE_V1','claims':claims}
    pack={'contract':'canonical_fact_pack_v1','status':'SOURCE_VERIFIED_PRODUCTION_READY','sources':[src],'claims':claims}
    plan={'article_type':req['article']['article_type'],'topic':req['article']['title'],'target_keyword':req['article']['target_keyword'],'category_binding':{'slug':req['article']['category']}}
    return research,facts,pack,plan

def article(req, repaired=False):
    a=req['article']; idx=a['title'].split()[-1]; suffix=' und nach Prüfbefund gezielt korrigiert' if repaired else ''
    unique=' '.join(f'eigen{idx}_{n}' for n in range(90)); return f'<article class="ppm-generated ppm-type-beratung" data-article-type="Beratung"><section data-block="criteria"><h2>{a["title"]}</h2><p data-fact-ids="f-{idx}-a f-{idx}-b">Inhalt {idx}{suffix} {unique} mit eindeutiger fachlicher Struktur.</p><table class="system-129-table comparison-table"><tr><th>Kriterium</th><th>Prüfung</th></tr><tr><td>{idx}</td><td>Gebundener Wert {idx}</td></tr></table></section></article>'


class Checks:
    def __init__(self, fail_first=False, wrong_hash=False, reject_batch=False, reject_repair=False): self.fail_first=fail_first; self.wrong_hash=wrong_hash; self.reject_batch=reject_batch; self.reject_repair=reject_repair; self.seen_fail=set()
    def research(self,t):
        if 'BAD_RESEARCH' in t: raise RuntimeError('RESEARCH_BLOCK')
        return {'status':'PASS','sha256':sha(t)}
    def facts(self,t,r):
        if 'BAD_FACTS' in t: raise RuntimeError('FACTS_BLOCK')
        return {'status':'PASS','sha256':sha(t)}
    def context(self,t,**kw):
        if 'BAD_CONTEXT' in t: raise RuntimeError('CONTEXT_BLOCK')
        p=json.loads(t); return {'status':'PASS','sha256':sha(t),'fact_pack':p['fact_pack'],'production_plan_item':p['production_plan_item']}
    def draft(self,t,**kw):
        if 'DESIGN_DRIFT' in t: raise RuntimeError('DESIGN_BLOCK')
        return {'status':'PASS','sha256':sha(t)}
    def repair(self,old,new,**kw):
        if self.reject_repair or len(new)>len(old)*2: raise RuntimeError('REPAIR_SCOPE_TOO_LARGE')
        return {'status':'PASS','sha256':sha(new)}
    def fullcheck(self,t,**kw):
        h=sha(t)
        if self.wrong_hash: return {'status':'PASS','checked_sha256':'0'*64,'evidence':{}}
        key=kw['article']['plan_slot']
        if self.fail_first and key not in self.seen_fail:
            self.seen_fail.add(key); return {'status':'FAIL','checked_sha256':h,'checker':'realish','findings':[{'error_code':'FIX_ONE'}]}
        ev={'contract':'SYSTEM4_FULL_PRODUCTION_CHECK_V1','status':'PASS','checked_draft_sha256':h,'publish_allowed':False,'evidence':{'no_legacy':{'status':'PASS','legacy_import_count':0},'no_external_links':{'status':'PASS','external_link_count':0},'languagetool':{'status':'PASS','engine':'LanguageTool 6.8 / Bestand 43','finding_count':0},'ppm679':{'status':'PASS','ppm_version':'6.7.9','technical_status':'TECHNICAL_CHECK_OK','content_quality_status':'CONTENT_QUALITY_CHECK_OK','fail_closed_aggregate_status':'PASS','content_sha256':h,'language_evidence_source':'TEST_ONLY'}}}
        return {'status':'PASS','checked_sha256':h,'evidence':ev}
    def batch(self,bodies):
        if self.reject_batch or len(set(bodies))!=len(bodies): raise RuntimeError('BATCH_BLOCK')
        return {'status':'PASS','article_count':len(bodies)}

def good_worker(req):
    task=req['task']; research,facts,pack,plan=evidence(req)
    if task=='research': return {'content':json.dumps(research,ensure_ascii=False,sort_keys=True)}
    if task=='facts': return {'content':json.dumps(facts,ensure_ascii=False,sort_keys=True)}
    if task=='context': return {'content':json.dumps({'fact_pack':pack,'production_plan_item':plan},ensure_ascii=False,sort_keys=True)}
    if task=='draft': return {'content':article(req)}
    if task=='repair': return {'content':article(req,True)}
    raise AssertionError(task)


class FullChainTests(unittest.TestCase):
    def test_positive_complete_entry_to_exact_exit_with_same_article_repair(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); snap=root/'snapshot.json'; snapshot(snap,2); out=root/'SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2.json'; s=FullChainSupervisor(mode='test',checks=Checks(fail_first=True)); result=s.run_full(snap,good_worker,out); self.assertEqual(result['status'],'SYSTEM4A_FULL_CHAIN_ARCHITECTURE_PASS'); self.assertTrue(out.is_file()); payload=json.loads(out.read_text()); self.assertEqual(len(payload['articles']),2); self.assertTrue(all(r['revision_count']==2 for r in payload['articles'])); self.assertEqual(s.verify_output(out)['status'],'SYSTEM4A_OUTPUT_VERIFY_PASS'); parent=root/'parent-chat'; roundtrip=s.simulate_parent_chat_roundtrip(Path(result['parent_chat_inline']['path']),parent); self.assertEqual(roundtrip['sha256'],result['output']['sha256']); self.assertEqual((parent/'SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2.json').read_bytes(),out.read_bytes())

    def test_positive_full_chain_scale_1_3_25_1000(self):
        for count in (1,3,25,1000):
            with self.subTest(count=count), tempfile.TemporaryDirectory() as td:
                root=Path(td); snap=root/'s.json'; snapshot(snap,count); out=root/'o.json'; sup=FullChainSupervisor(mode='test',checks=Checks()); result=sup.run_full(snap,good_worker,out); self.assertEqual(result['article_count'],count); self.assertEqual(sup.verify_output(out)['article_count'],count)

    def test_positive_worker_is_separate_process_and_sees_no_state(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); snap=root/'s.json'; snapshot(snap,1); out=root/'o.json'; script=root/'worker.py'
            script.write_text("""import json,sys,hashlib\nr=json.load(sys.stdin); a=r['article']; i=a['title'].split()[-1]; t=r['task']\ndef sh(x): return hashlib.sha256(x.encode()).hexdigest()\ne1=f'Gesicherter konkreter Beleg A für Artikel {i} mit eindeutiger fachlicher Aussage und sicherer Nutzung.'; e2=f'Gesicherter konkreter Beleg B für Artikel {i} mit einer zweiten fachlichen Aussage zur Auswahl.'; ev=e1+'\\n'+e2+'\\nZusatz'; sid=f'src-{i}'; src={'source_id':sid,'source_title':f'Fachquelle {i}','source_url':f'https://example.org/source-{i}','retrieved_at':'2026-09-13T08:00:00Z','snapshot_sha256':sh(ev),'evidence':ev}; claims=[{'fact_id':f'f-{i}-a','source_id':sid,'statement':f'Konkrete erste Aussage für Artikel {i}.','evidence_text':e1,'evidence_text_sha256':sh(e1)},{'fact_id':f'f-{i}-b','source_id':sid,'statement':f'Konkrete zweite Aussage für Artikel {i}.','evidence_text':e2,'evidence_text_sha256':sh(e2)}]\nif t=='research': c=json.dumps({'contract':'SYSTEM4_RESEARCH_EVIDENCE_V1','sources':[src]},ensure_ascii=False)\nelif t=='facts': c=json.dumps({'contract':'SYSTEM4_FACTS_EVIDENCE_V1','claims':claims},ensure_ascii=False)\nelif t=='context': c=json.dumps({'fact_pack':{'contract':'canonical_fact_pack_v1','status':'SOURCE_VERIFIED_PRODUCTION_READY','sources':[src],'claims':claims},'production_plan_item':{'article_type':a['article_type'],'topic':a['title'],'target_keyword':a['target_keyword'],'category_binding':{'slug':a['category']}}},ensure_ascii=False)\nelse: c=f'<article class=\"ppm-generated ppm-type-beratung\" data-article-type=\"Beratung\"><h2>{a[\"title\"]}</h2><p data-fact-ids=\"f-{i}-a f-{i}-b\">eigen{i}_0 eigen{i}_1 eigen{i}_2 eigen{i}_3 eigen{i}_4 eigen{i}_5 eigen{i}_6 eigen{i}_7 eigen{i}_8 eigen{i}_9 eindeutige fachliche Struktur für sichere Auswahl.</p><table class=\"system-129-table comparison-table\"><tr><th>A</th><th>B</th></tr><tr><td>{i}</td><td>Wert</td></tr></table></article>'\njson.dump({'content':c},sys.stdout,ensure_ascii=False)\n""")
            def process_worker(req):
                proc=subprocess.run([sys.executable,str(script)],input=json.dumps(req,ensure_ascii=False),text=True,capture_output=True,check=True); return json.loads(proc.stdout)
            sup=FullChainSupervisor(mode='test',checks=Checks()); result=sup.run_full(snap,process_worker,out); self.assertEqual(result['status'],'SYSTEM4A_FULL_CHAIN_ARCHITECTURE_PASS'); self.assertFalse(any(root.rglob('state.json')))

    def test_negative_empty_ingress_no_output(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); snap=root/'s.json'; snap.write_text(json.dumps({'next_textmachine_metadata_batch':{'contract':'PSERC_TEXTMACHINE_METADATA_BATCH_V2','status':'READY_FOR_TEXTMACHINE_METADATA_INTAKE','batch_sha256':'a'*64,'item_count':0,'items':[],'publish_allowed':False}})); out=root/'o.json'; s=FullChainSupervisor(mode='test',checks=Checks());
            with self.assertRaises(Exception): s.run_full(snap,good_worker,out)
            self.assertFalse(out.exists())
    def test_negative_worker_state_injection_no_output(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); snap=root/'s.json'; snapshot(snap,1); out=root/'o.json'; s=FullChainSupervisor(mode='test',checks=Checks())
            def bad(req): return {'content':'x','phase':'ARTICLE_PASS'}
            with self.assertRaisesRegex(CapsuleError,'WORKER_RESULT_SCHEMA_INVALID'): s.run_full(snap,bad,out)
            self.assertFalse(out.exists())
    def test_negative_worker_cannot_inject_lt_ppm_or_pass_evidence(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); snap=root/'s.json'; snapshot(snap,1); out=root/'o.json'; sup=FullChainSupervisor(mode='test',checks=Checks())
            def bad(req): return {'content':'x','languagetool':{'status':'PASS'},'ppm679':{'status':'PASS'},'production_evidence':{'status':'PASS'},'PASS':True}
            with self.assertRaisesRegex(CapsuleError,'WORKER_RESULT_SCHEMA_INVALID'): sup.run_full(snap,bad,out)
            self.assertFalse(out.exists())

    def test_negative_research_no_output(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); snap=root/'s.json'; snapshot(snap,1); out=root/'o.json'; s=FullChainSupervisor(mode='test',checks=Checks())
            def w(req): return {'content':'BAD_RESEARCH'} if req['task']=='research' else good_worker(req)
            with self.assertRaisesRegex(RuntimeError,'RESEARCH_BLOCK'): s.run_full(snap,w,out)
            self.assertFalse(out.exists())
    def test_negative_facts_no_output(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); snap=root/'s.json'; snapshot(snap,1); out=root/'o.json'; s=FullChainSupervisor(mode='test',checks=Checks())
            def w(req): return {'content':'BAD_FACTS'} if req['task']=='facts' else good_worker(req)
            with self.assertRaisesRegex(RuntimeError,'FACTS_BLOCK'): s.run_full(snap,w,out)
            self.assertFalse(out.exists())
    def test_negative_context_no_output(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); snap=root/'s.json'; snapshot(snap,1); out=root/'o.json'; s=FullChainSupervisor(mode='test',checks=Checks())
            def w(req): return {'content':'BAD_CONTEXT'} if req['task']=='context' else good_worker(req)
            with self.assertRaisesRegex(RuntimeError,'CONTEXT_BLOCK'): s.run_full(snap,w,out)
            self.assertFalse(out.exists())
    def test_negative_design_no_output(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); snap=root/'s.json'; snapshot(snap,1); out=root/'o.json'; s=FullChainSupervisor(mode='test',checks=Checks())
            def w(req): return {'content':'DESIGN_DRIFT'} if req['task']=='draft' else good_worker(req)
            with self.assertRaisesRegex(RuntimeError,'DESIGN_BLOCK'): s.run_full(snap,w,out)
            self.assertFalse(out.exists())
    def test_negative_wrong_checker_hash_no_output(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); snap=root/'s.json'; snapshot(snap,1); out=root/'o.json'; s=FullChainSupervisor(mode='test',checks=Checks(wrong_hash=True))
            with self.assertRaisesRegex(CapsuleError,'FULLCHECK_HASH_MISMATCH'): s.run_full(snap,good_worker,out)
            self.assertFalse(out.exists())
    def test_negative_broad_repair_no_output(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); snap=root/'s.json'; snapshot(snap,1); out=root/'o.json'; s=FullChainSupervisor(mode='test',checks=Checks(fail_first=True,reject_repair=True))
            with self.assertRaisesRegex(RuntimeError,'REPAIR_SCOPE_TOO_LARGE'): s.run_full(snap,good_worker,out)
            self.assertFalse(out.exists())
    def test_negative_batch_no_output(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); snap=root/'s.json'; snapshot(snap,2); out=root/'o.json'; s=FullChainSupervisor(mode='test',checks=Checks(reject_batch=True))
            with self.assertRaisesRegex(RuntimeError,'BATCH_BLOCK'): s.run_full(snap,good_worker,out)
            self.assertFalse(out.exists())
    def test_negative_parent_chat_inline_tamper_blocks_reconstruction(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); snap=root/'s.json'; snapshot(snap,1); out=root/'o.json'; sup=FullChainSupervisor(mode='test',checks=Checks()); result=sup.run_full(snap,good_worker,out); inline=Path(result['parent_chat_inline']['path']); text=inline.read_text(); inline.write_text(text.replace('payload_base64', 'payload_base64_TAMPER', 1))
            with self.assertRaises(Exception): sup.simulate_parent_chat_roundtrip(inline,root/'parent')

    def test_negative_output_tamper_fails_readback(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); snap=root/'s.json'; snapshot(snap,1); out=root/'o.json'; s=FullChainSupervisor(mode='test',checks=Checks()); s.run_full(snap,good_worker,out); p=json.loads(out.read_text()); p['articles'][0]['body']+='tamper'; out.write_text(json.dumps(p));
            with self.assertRaises(Exception): s.verify_output(out)
    def test_negative_second_run_side_entry_blocked(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); snap=root/'s.json'; snapshot(snap,1); out=root/'o.json'; s=FullChainSupervisor(mode='test',checks=Checks()); s.run_full(snap,good_worker,out)
            with self.assertRaisesRegex(FullChainError,'FULL_CHAIN_ALREADY_STARTED'): s.run_full(snap,good_worker,root/'o2.json')
    def test_production_backend_injection_forbidden(self):
        with self.assertRaisesRegex(FullChainError,'PRODUCTION_CHECK_BACKEND_INJECTION_FORBIDDEN'): FullChainSupervisor(mode='production',checks=Checks())
    def test_production_backend_is_lazy_and_loaded_before_snapshot_ingress(self):
        sup=FullChainSupervisor(mode='production')
        self.assertIsNone(sup._controller)
        with mock.patch.object(full_chain_module,'System4ReadOnlyChecks',side_effect=RuntimeError('BACKEND_SENTINEL')):
            with self.assertRaisesRegex(RuntimeError,'BACKEND_SENTINEL'):
                sup._run_external_production(Path('not-needed-before-backend.json'),lambda _:{'content':'x'},Path('no-output.json'))
        self.assertFalse(sup.status()['started'])
        self.assertIsNone(sup._controller)
    def test_full_chain_source_has_no_checker_mock_escape(self):
        text=Path(__file__).with_name('full_chain.py').read_text(); self.assertNotIn('mock.patch',text); self.assertNotIn('run_languagetool =',text); self.assertNotIn('run_ppm_content_validator =',text); self.assertNotIn('production_checks.run_all =',text)

if __name__=='__main__': unittest.main(verbosity=2)
