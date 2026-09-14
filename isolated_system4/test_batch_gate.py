import copy,hashlib,json,tempfile,unittest
from pathlib import Path
import authoring_contract,batch_gate,production_binding

HERE=Path(__file__).resolve().parent
REPO=HERE.parent
LIVE=HERE/'live_fixture/wordpress_snapshot.json'

def sha_text(value): return hashlib.sha256(value.encode('utf-8')).hexdigest()
def production_evidence(draft):
    d=sha_text(draft)
    return {'contract':'SYSTEM4_FULL_PRODUCTION_CHECK_V1','status':'PASS','checked_draft_sha256':d,'publish_allowed':False,'evidence':{'no_legacy':{'status':'PASS','legacy_import_count':0},'no_external_links':{'status':'PASS','external_link_count':0},'languagetool':{'status':'PASS','engine':'LanguageTool 6.8 / Bestand 43','finding_count':0},'ppm679':{'status':'PASS','ppm_version':'6.7.9','technical_status':'TECHNICAL_CHECK_OK','content_quality_status':'CONTENT_QUALITY_CHECK_OK','fail_closed_aggregate_status':'PASS','content_sha256':d,'language_evidence_source':'REAL_LT68_CURRENT_DRAFT_REFRESHED'}}}
def evidence_payloads(i,source_snapshot_id):
    chunks=[f'Erster konkreter Beleg für Testartikel {i} mit fachlicher Aussage und eindeutiger Bindung.',f'Zweiter konkreter Beleg für Testartikel {i} mit einer davon verschiedenen fachlichen Aussage.',f'Dritter gesicherter Beleg für Testartikel {i} mit eigenständiger fachlicher Aussage.']
    evidence='\n'.join(chunks); source_id=f'src-test-{i}'
    source={'source_id':source_id,'source_title':f'Fachquelle Test {i}','source_url':f'https://example.org/source-{i}','retrieved_at':'2026-09-12T20:00:00Z','snapshot_sha256':sha_text(evidence),'evidence':evidence}
    claims=[]
    for n,text in enumerate(chunks): claims.append({'fact_id':f'fact-{i}-{n}','source_id':source_id,'statement':f'Konkrete Aussage {n+1} für Artikel {i}.','evidence_text':text,'evidence_text_sha256':sha_text(text),'claim_status':'FULLY_SUPPORTED','article_types':['Beratung']})
    research={'contract':'SYSTEM4_RESEARCH_EVIDENCE_V1','sources':[dict(source)]}; facts={'contract':'SYSTEM4_FACTS_EVIDENCE_V1','claims':copy.deepcopy(claims)}
    pack={'contract':'canonical_fact_pack_v1','status':'SOURCE_VERIFIED_PRODUCTION_READY','source_snapshot_id':source_snapshot_id,'fact_pack_id':source_snapshot_id,'sources':[dict(source)],'claims':copy.deepcopy(claims)}
    return research,facts,pack

def make_fixture(root,count=7):
    live=json.loads(LIVE.read_text(encoding='utf-8')); source_items=live['next_textmachine_metadata_batch']['items']
    if count<1 or count>len(source_items): raise ValueError('count outside real bound metadata fixture')
    snapshot=copy.deepcopy(live); snapshot['next_textmachine_metadata_batch']['items']=copy.deepcopy(source_items[:count]); snapshot['next_textmachine_metadata_batch']['item_count']=count
    batch_sha=hashlib.sha256(json.dumps(snapshot['next_textmachine_metadata_batch']['items'],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest(); snapshot['next_textmachine_metadata_batch']['batch_sha256']=batch_sha
    snap=root/'snapshot.json'; snap.write_text(json.dumps(snapshot,ensure_ascii=False,sort_keys=True,separators=(',',':')),encoding='utf-8'); snap_sha=hashlib.sha256(snap.read_bytes()).hexdigest(); paths=[]
    for i,item in enumerate(snapshot['next_textmachine_metadata_batch']['items']):
        unique=' '.join(f'eigen{i}_{n}' for n in range(90)); draft=f'<article class="ppm-generated ppm-type-beratung" data-article-type="Beratung"><h2>{item["title"]}</h2><p data-fact-ids="fact-{i}-0 fact-{i}-1 fact-{i}-2">{item["target_keyword"]} {unique}</p><table class="system-129-table comparison-table"><tr><th>Kriterium</th><th>Wert</th></tr><tr><td>A</td><td>B</td></tr></table></article>'
        research,facts,fact=evidence_payloads(i,snap_sha)
        base_plan={'article_type':item['article_type'],'target_keyword':item['target_keyword'],'topic':item['title'],'source_snapshot_id':snap_sha,'runtime_order':{'order_id':f'batch-test-{i}','article_type':item['article_type'],'title':item['title'],'slug':f'batch-test-{i}','subject_scope':'batch_test','subject_label':item['target_keyword'],'lead':'Gebundener Testwert mit ausreichender Aussage.','conclusion':'Gebundener Abschlusswert mit ausreichender Aussage.','allowed_fact_ids':[f'fact-{i}-0',f'fact-{i}-1',f'fact-{i}-2']}}
        shell={'article':copy.deepcopy(item),'source_snapshot_sha256':snap_sha}; bound=production_binding.bind_plan(REPO,shell,fact,base_plan); bound['canonical_article']={'body_html':draft}
        contract=authoring_contract.build(REPO,shell,fact,bound); context={'fact_pack':fact,'production_plan_item':bound}
        research_text=json.dumps(research,ensure_ascii=False,sort_keys=True); facts_text=json.dumps(facts,ensure_ascii=False,sort_keys=True)
        state={'contract':batch_gate.STATE_CONTRACT,'source_snapshot_sha256':snap_sha,'batch_sha256':batch_sha,'article':copy.deepcopy(item),'immutable_core_sha256':'','publish_allowed':False,'phase':'OUTPUT_GATE_REQUIRED','revision':1,'research':{'text':research_text,'sha256':sha_text(research_text)},'facts':{'text':facts_text,'sha256':sha_text(facts_text)},'production_context':{'fact_pack':fact,'production_plan_item':bound,'sha256':batch_gate.stable_hash(context)},'authoring_contract':contract,'draft_markdown':draft,'draft_sha256':sha_text(draft),'checks':{'status':'PASS','mode':'FULL_PRODUCTION','errors':[],'checked_draft_sha256':sha_text(draft),'production_evidence':production_evidence(draft)},'last_error':None,'release_prepared':None,'released':False}
        state['immutable_core_sha256']=batch_gate.stable_hash(batch_gate.immutable_core(state)); p=root/f'state-{i}.json'; p.write_text(json.dumps(state,ensure_ascii=False),encoding='utf-8'); paths.append(p)
    return snap,paths

class BatchGateTests(unittest.TestCase):
    def run_collect(self,mutate=None,count=7,path_count=None):
        td=tempfile.TemporaryDirectory(); root=Path(td.name); snap,paths=make_fixture(root,count=count)
        if mutate: mutate(root,snap,paths)
        if path_count is not None: paths=paths[:path_count]
        out=root/'out'
        try: return td,batch_gate.collect_batch(snap,paths,out),out,paths,snap
        except Exception: td.cleanup(); raise
    def assert_blocked(self,code,mutate=None,path_count=None):
        with self.assertRaisesRegex(batch_gate.BatchGateError,code): self.run_collect(mutate=mutate,path_count=path_count)
    def test_positive(self):
        td,result,out,paths,snap=self.run_collect()
        try:
            self.assertEqual(result['status'],'SYSTEM4_BATCH_FULL_PASS_COLLECTED'); self.assertEqual(result['article_count'],7); self.assertEqual(result['next_required'],batch_gate.NEXT_REQUIRED); self.assertFalse(result['publish_allowed']); self.assertEqual(len(list(out.glob('ARTICLE_*.md'))),7)
            evidence=json.loads((out/'system4_batch_evidence.json').read_text()); self.assertEqual(evidence['article_count'],7); self.assertTrue(all(row['quality']['languagetool']['status']=='PASS' for row in evidence['articles'])); self.assertTrue(all(row['design']['status']=='PASS' for row in evidence['articles'])); self.assertFalse(evidence['design_mutation_performed']); self.assertEqual(evidence['batch_distinctness']['status'],'PASS')
        finally: td.cleanup()
    def test_missing_state(self): self.assert_blocked('STATE_COUNT_MISMATCH',path_count=6)
    def test_basic_check_blocked(self):
        def m(r,s,p): x=json.loads(p[2].read_text()); x['checks']['mode']='BASIC_ARCHITECTURE'; p[2].write_text(json.dumps(x))
        self.assert_blocked('FULL_PRODUCTION_PASS_REQUIRED',m)
    def test_failed_check_blocked(self):
        def m(r,s,p): x=json.loads(p[2].read_text()); x['checks']['status']='FAIL'; p[2].write_text(json.dumps(x))
        self.assert_blocked('FULL_PRODUCTION_PASS_REQUIRED',m)
    def test_draft_tamper_blocked(self):
        def m(r,s,p): x=json.loads(p[2].read_text()); x['draft_markdown']+='x'; p[2].write_text(json.dumps(x))
        self.assert_blocked('STATE_DRAFT_HASH_INVALID',m)
    def test_publish_true_blocked(self):
        def m(r,s,p): x=json.loads(p[2].read_text()); x['publish_allowed']=True; p[2].write_text(json.dumps(x))
        self.assert_blocked('STATE_PUBLISH_MUST_BE_FALSE',m)
    def test_wrong_batch_blocked(self):
        def m(r,s,p): x=json.loads(p[2].read_text()); x['batch_sha256']='0'*64; x['immutable_core_sha256']=batch_gate.stable_hash(batch_gate.immutable_core(x)); p[2].write_text(json.dumps(x))
        self.assert_blocked('STATE_BATCH_MISMATCH',m)
    def test_wrong_snapshot_blocked(self):
        def m(r,s,p): x=json.loads(p[2].read_text()); x['source_snapshot_sha256']='0'*64; x['immutable_core_sha256']=batch_gate.stable_hash(batch_gate.immutable_core(x)); p[2].write_text(json.dumps(x))
        self.assert_blocked('STATE_SOURCE_SNAPSHOT_MISMATCH',m)
    def test_metadata_tamper_blocked(self):
        def m(r,s,p): x=json.loads(p[2].read_text()); x['article']['title']='Falsch'; x['immutable_core_sha256']=batch_gate.stable_hash(batch_gate.immutable_core(x)); p[2].write_text(json.dumps(x))
        self.assert_blocked('STATE_ARTICLE_BINDING_MISMATCH',m)
    def test_per_article_release_blocked(self):
        def m(r,s,p): x=json.loads(p[2].read_text()); x['release_prepared']={'x':1}; p[2].write_text(json.dumps(x))
        self.assert_blocked('PER_ARTICLE_RELEASE_PREPARED_FORBIDDEN',m)
    def test_context_hash_blocked(self):
        def m(r,s,p): x=json.loads(p[2].read_text()); x['production_context']['sha256']='0'*64; p[2].write_text(json.dumps(x))
        self.assert_blocked('PRODUCTION_CONTEXT_HASH_INVALID',m)
    def test_research_context_binding_tamper_blocked(self):
        def m(r,s,p): f=json.loads(json.loads(p[2].read_text())['facts']['text']); invented='Erfundener Belegtext, der nicht aus dem gesicherten Quellenausschnitt stammt.'; f['claims'][0]['evidence_text']=invented; f['claims'][0]['evidence_text_sha256']=sha_text(invented); x=json.loads(p[2].read_text()); x['facts']['text']=json.dumps(f,ensure_ascii=False,sort_keys=True); x['facts']['sha256']=sha_text(x['facts']['text']); p[2].write_text(json.dumps(x))
        self.assert_blocked('CONTENT_CONTEXT_NOT_PASS:FACT_EVIDENCE_NOT_IN_SOURCE',m)
    def test_duplicate_state_slot_blocked(self):
        def m(r,s,p): x0=json.loads(p[0].read_text()); x1=json.loads(p[1].read_text()); x1['article']['plan_slot']=x0['article']['plan_slot']; x1['immutable_core_sha256']=batch_gate.stable_hash(batch_gate.immutable_core(x1)); p[1].write_text(json.dumps(x1))
        self.assert_blocked('STATE_PLAN_SLOT_DUPLICATE',m)
    def test_lt_pass_evidence_tamper_blocked(self):
        def m(r,s,p): x=json.loads(p[2].read_text()); x['checks']['production_evidence']['evidence']['languagetool']['finding_count']=1; p[2].write_text(json.dumps(x))
        self.assert_blocked('LANGUAGETOOL_EVIDENCE_NOT_PASS',m)
    def test_ppm_pass_evidence_tamper_blocked(self):
        def m(r,s,p): x=json.loads(p[2].read_text()); x['checks']['production_evidence']['evidence']['ppm679']['technical_status']='FAIL'; p[2].write_text(json.dumps(x))
        self.assert_blocked('PPM679_EVIDENCE_NOT_PASS',m)
    def test_missing_production_evidence_blocked(self):
        def m(r,s,p): x=json.loads(p[2].read_text()); x['checks'].pop('production_evidence'); p[2].write_text(json.dumps(x))
        self.assert_blocked('FULL_PRODUCTION_EVIDENCE_MISSING',m)
    def test_design_drift_is_blocked_even_after_full_pass(self):
        def m(r,s,p):
            x=json.loads(p[2].read_text()); old=x['draft_markdown']; new=old.replace('system-129-table comparison-table','comparison-table'); x['draft_markdown']=new; x['draft_sha256']=sha_text(new); x['checks']['checked_draft_sha256']=sha_text(new); x['checks']['production_evidence']=production_evidence(new); x['production_context']['production_plan_item']['canonical_article']['body_html']=new; x['production_context']['sha256']=batch_gate.stable_hash({'fact_pack':x['production_context']['fact_pack'],'production_plan_item':x['production_context']['production_plan_item']}); p[2].write_text(json.dumps(x))
        self.assert_blocked('DESIGN_GUARD_NOT_PASS:DESIGN_TABLE_SYSTEM129_CLASS_MISSING',m)
if __name__=='__main__': unittest.main(verbosity=2)
