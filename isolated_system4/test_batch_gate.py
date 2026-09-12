import hashlib,json,tempfile,unittest
from pathlib import Path
import batch_gate

def sha_text(value): return hashlib.sha256(value.encode('utf-8')).hexdigest()
def production_evidence(draft):
    d=sha_text(draft)
    return {
      'contract':'SYSTEM4_FULL_PRODUCTION_CHECK_V1','status':'PASS','checked_draft_sha256':d,'publish_allowed':False,
      'evidence':{
        'no_legacy':{'status':'PASS','legacy_import_count':0},
        'no_external_links':{'status':'PASS','external_link_count':0},
        'languagetool':{'status':'PASS','engine':'LanguageTool 6.8 / Bestand 43','finding_count':0},
        'ppm679':{'status':'PASS','ppm_version':'6.7.9','technical_status':'TECHNICAL_CHECK_OK','content_quality_status':'CONTENT_QUALITY_CHECK_OK','fail_closed_aggregate_status':'PASS','content_sha256':d,'language_evidence_source':'REAL_LT68_CURRENT_DRAFT_REFRESHED'},
      }
    }
def evidence_payloads(i):
    e1=f'Erster konkreter Beleg für Testartikel {i} mit fachlicher Aussage und eindeutiger Bindung.'
    e2=f'Zweiter konkreter Beleg für Testartikel {i} mit einer davon verschiedenen fachlichen Aussage.'
    evidence=e1+'\n'+e2+'\n'+f'Zusätzlicher gesicherter Quellenkontext für Testartikel {i}.'
    source_id=f'src-test-{i}'
    source={'source_id':source_id,'source_title':f'Fachquelle Test {i}','source_url':f'https://example.org/source-{i}','retrieved_at':'2026-09-12T20:00:00Z','snapshot_sha256':sha_text(evidence),'evidence':evidence}
    claims=[
        {'fact_id':f'fact-{i}-a','source_id':source_id,'statement':f'Konkrete erste Aussage für Artikel {i}.','evidence_text':e1,'evidence_text_sha256':sha_text(e1)},
        {'fact_id':f'fact-{i}-b','source_id':source_id,'statement':f'Konkrete zweite Aussage für Artikel {i}.','evidence_text':e2,'evidence_text_sha256':sha_text(e2)},
    ]
    research={'contract':'SYSTEM4_RESEARCH_EVIDENCE_V1','sources':[dict(source)]}
    facts={'contract':'SYSTEM4_FACTS_EVIDENCE_V1','claims':claims}
    pack={'contract':'canonical_fact_pack_v1','status':'SOURCE_VERIFIED_PRODUCTION_READY','sources':[dict(source)],'claims':claims}
    return research,facts,pack
def make_fixture(root,count=7):
    items=[]
    for i in range(count):
        slot=hashlib.sha256(f'slot-{i}'.encode()).hexdigest(); items.append({'title':f'Titel {i}','target_keyword':f'Keyword {i}','category':f'kategorie-{i}','article_type':'Beratung','plan_slot':slot})
    snapshot={'contract':'SYSTEM4_WORDPRESS_LIVE_INPUT_FIXTURE_V1','next_textmachine_metadata_batch':{'contract':'PSERC_TEXTMACHINE_METADATA_BATCH_V2','status':'READY_FOR_TEXTMACHINE_METADATA_INTAKE','batch_sha256':hashlib.sha256(b'batch').hexdigest(),'item_count':count,'items':items,'publish_allowed':False}}
    snap=root/'snapshot.json'; snap.write_text(json.dumps(snapshot,ensure_ascii=False),encoding='utf-8'); snap_sha=hashlib.sha256(snap.read_bytes()).hexdigest(); batch_sha=snapshot['next_textmachine_metadata_batch']['batch_sha256']; paths=[]
    for i,item in enumerate(items):
        unique=' '.join(f'eigen{i}_{n}' for n in range(90))
        draft=f'<article class="ppm-generated ppm-type-beratung" data-article-type="Beratung"><h2>{item["title"]}</h2><p data-fact-ids="fact-{i}-a fact-{i}-b">{item["target_keyword"]} {unique}</p><table class="system-129-table comparison-table"><tr><th>Kriterium</th><th>Wert</th></tr><tr><td>A</td><td>B</td></tr></table></article>'
        research,facts,fact=evidence_payloads(i); plan={'canonical_article':{'body_html':draft}}; context={'fact_pack':fact,'production_plan_item':plan}
        research_text=json.dumps(research,ensure_ascii=False,sort_keys=True); facts_text=json.dumps(facts,ensure_ascii=False,sort_keys=True)
        state={'contract':batch_gate.STATE_CONTRACT,'source_snapshot_sha256':snap_sha,'batch_sha256':batch_sha,'article':item,'immutable_core_sha256':'','publish_allowed':False,'phase':'OUTPUT_GATE_REQUIRED','revision':1,'research':{'text':research_text,'sha256':sha_text(research_text)},'facts':{'text':facts_text,'sha256':sha_text(facts_text)},'production_context':{'fact_pack':fact,'production_plan_item':plan,'sha256':batch_gate.stable_hash(context)},'draft_markdown':draft,'draft_sha256':sha_text(draft),'checks':{'status':'PASS','mode':'FULL_PRODUCTION','errors':[],'checked_draft_sha256':sha_text(draft),'production_evidence':production_evidence(draft)},'last_error':None,'release_prepared':None,'released':False}
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
            self.assertEqual(result['status'],'SYSTEM4_BATCH_FULL_PASS_COLLECTED'); self.assertEqual(result['article_count'],7); self.assertEqual(result['next_required'],'SIGNED_WORKFLOW_RELEASE'); self.assertFalse(result['publish_allowed']); self.assertEqual(len(list(out.glob('ARTICLE_*.md'))),7)
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
        def m(r,s,p): x=json.loads(p[2].read_text()); f=json.loads(x['facts']['text']); invented='Erfundener Belegtext, der nicht aus dem gesicherten Quellenausschnitt stammt.'; f['claims'][0]['evidence_text']=invented; f['claims'][0]['evidence_text_sha256']=sha_text(invented); x['facts']['text']=json.dumps(f,ensure_ascii=False,sort_keys=True); x['facts']['sha256']=sha_text(x['facts']['text']); p[2].write_text(json.dumps(x))
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
