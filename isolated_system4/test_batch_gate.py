import hashlib,json,tempfile,unittest,shutil
from pathlib import Path
import authoring_contract
import batch_gate
import e2e_acceptance_subset
import production_checks

REPO=Path(__file__).resolve().parent.parent

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
    e3=f'Dritter konkreter Beleg für Testartikel {i} bestätigt einen weiteren eigenständigen fachlichen Prüfpunkt.'
    evidence=e1+'\n'+e2+'\n'+e3+'\n'+f'Zusätzlicher gesicherter Quellenkontext für Testartikel {i}.'
    source_id=f'src-test-{i}'
    source={'source_id':source_id,'source_title':f'Fachquelle Test {i}','source_url':f'https://example.org/source-{i}','retrieved_at':'2026-09-12T20:00:00Z','snapshot_sha256':sha_text(evidence),'evidence':evidence}
    claims=[
        {'fact_id':f'fact-{i}-a','source_id':source_id,'statement':f'Konkrete erste Aussage für Artikel {i}.','evidence_text':e1,'evidence_text_sha256':sha_text(e1)},
        {'fact_id':f'fact-{i}-b','source_id':source_id,'statement':f'Konkrete zweite Aussage für Artikel {i}.','evidence_text':e2,'evidence_text_sha256':sha_text(e2)},
        {'fact_id':f'fact-{i}-c','source_id':source_id,'statement':f'Konkrete dritte Aussage für Artikel {i}.','evidence_text':e3,'evidence_text_sha256':sha_text(e3)},
    ]
    research={'contract':'SYSTEM4_RESEARCH_EVIDENCE_V1','sources':[dict(source)]}
    facts={'contract':'SYSTEM4_FACTS_EVIDENCE_V1','claims':claims}
    pack={'contract':'canonical_fact_pack_v1','status':'SOURCE_VERIFIED_PRODUCTION_READY','sources':[dict(source)],'claims':[dict(row) for row in claims]}
    return research,facts,pack

def bind_authoring_contract(state):
    article=state['article']; context=state['production_context']; pack=context['fact_pack']; source=state['source_snapshot_sha256']
    pack['source_snapshot_id']=source; pack['fact_pack_id']=source
    for claim in pack['claims']:
        claim['claim_status']='FULLY_SUPPORTED'; claim['article_types']=[article['article_type']]
    package=(REPO/production_checks.PPM_PACKAGE_REL).resolve()
    static=authoring_contract._static_ppm_rules(package); structure=static['structure']
    required_roles=[str(v) for v in ((structure.get('links') or {}).get('required_roles') or []) if isinstance(v,str) and v]
    links=[]
    for index,role in enumerate(required_roles):
        links.append({'role':role,'section_id':f'test-section-{index}','anchor':f'Interner Testverweis {index+1}','href':f'/system4-test-{article["plan_slot"][:8]}-{index+1}/','active':True,'reason':f'Gebundener interner Testverweis für Rolle {role}.'})
    registry={'contract':'SYSTEM4_TEST_LINK_REGISTRY_V1','entries':[dict(row) for row in links]}
    quality={
        'contract':'content_structure_language_binding_v2',
        'internal_test_marker':'LT2-FAQ-001',
        'portal_link_registry':registry,
        'portal_link_registry_hash':authoring_contract._stable(registry),
        'link_bindings':[dict(row) for row in links],
        'wordpress_category':{'id':1000,'slug':article['category'],'name':'Testkategorie '+article['category']},
        'intent_terms':[article['target_keyword'],article['title'],'Kontrolle'],
        'table_value_statement':'Diese Tabelle ordnet den Prüfpunkt, den sichtbaren Zustand und die daraus folgende notwendige Kontrolle vor der Nutzung eindeutig und nachvollziehbar ein.',
    }
    allowed=[row['fact_id'] for row in pack['claims']]
    plan={
        'article_type':article['article_type'],'target_keyword':article['target_keyword'],'topic':article['title'],
        'source_snapshot_id':source,'quality_binding':quality,'quality_binding_hash':authoring_contract._stable(quality),
        'runtime_order':{
            'order_id':'system4-batch-test-'+article['plan_slot'][:12],'article_type':article['article_type'],'title':article['title'],
            'slug':'system4-test-'+article['plan_slot'][:12],'subject_scope':article['title'],'subject_label':article['target_keyword'],
            'lead':'Gebundener Testeinleitungssatz für den Batch-Gate-Vertrag.','conclusion':'Gebundener Testabschlusssatz für den Batch-Gate-Vertrag.',
            'links':[dict(row) for row in links],'allowed_fact_ids':allowed,
        },
        'canonical_article':{'title':article['title'],'article_type':article['article_type'],'slug':'system4-test-'+article['plan_slot'][:12]},
        'validation_contract_version':'system4-test-fixture-v1',
    }
    context['fact_pack']=pack; context['production_plan_item']=plan; context['sha256']=batch_gate.stable_hash({'fact_pack':pack,'production_plan_item':plan})
    state['authoring_contract']=authoring_contract.build(REPO,state,pack,plan)
    return state

def make_fixture(root,count=7):
    items=[]
    for i in range(count):
        slot=hashlib.sha256(f'slot-{i}'.encode()).hexdigest(); items.append({'title':f'Titel {i}','target_keyword':f'Keyword {i}','category':f'kategorie-{i}','article_type':'Beratung','plan_slot':slot})
    snapshot={'contract':'SYSTEM4_WORDPRESS_LIVE_INPUT_FIXTURE_V1','next_textmachine_metadata_batch':{'contract':'PSERC_TEXTMACHINE_METADATA_BATCH_V2','status':'READY_FOR_TEXTMACHINE_METADATA_INTAKE','batch_sha256':hashlib.sha256(b'batch').hexdigest(),'item_count':count,'items':items,'publish_allowed':False}}
    snap=root/'snapshot.json'; snap.write_text(json.dumps(snapshot,ensure_ascii=False),encoding='utf-8'); snap_sha=hashlib.sha256(snap.read_bytes()).hexdigest(); batch_sha=snapshot['next_textmachine_metadata_batch']['batch_sha256']; paths=[]
    bound_snapshot={'contract':'SYSTEM4_WORDPRESS_LIVE_INPUT_FIXTURE_V1','next_textmachine_metadata_batch':snapshot['next_textmachine_metadata_batch'],'system4_root_manifest_sha256':'1'*64}
    bound_raw=json.dumps(bound_snapshot,ensure_ascii=False).encode('utf-8')
    bound_sha=hashlib.sha256(bound_raw).hexdigest()
    if bound_sha==snap_sha: raise AssertionError('FIXTURE_MUST_MODEL_DISTINCT_RUNTIME_AND_BOUND_SNAPSHOT_HASHES')
    for i,item in enumerate(items):
        unique=' '.join(f'eigen{i}_{n}' for n in range(90))
        draft=f'<article class="ppm-generated ppm-type-beratung" data-article-type="Beratung"><h2>{item["title"]}</h2><p data-fact-ids="fact-{i}-a fact-{i}-b fact-{i}-c">{item["target_keyword"]} {unique}</p><table class="system-129-table comparison-table"><tr><th>Kriterium</th><th>Wert</th></tr><tr><td>A</td><td>B</td></tr></table></article>'
        research,facts,fact=evidence_payloads(i); plan={'canonical_article':{'body_html':draft}}; context={'fact_pack':fact,'production_plan_item':plan}
        research_text=json.dumps(research,ensure_ascii=False,sort_keys=True); facts_text=json.dumps(facts,ensure_ascii=False,sort_keys=True)
        state={'contract':batch_gate.STATE_CONTRACT,'source_snapshot_sha256':bound_sha,'batch_sha256':batch_sha,'article':item,'immutable_core_sha256':'','publish_allowed':False,'phase':'OUTPUT_GATE_REQUIRED','revision':1,'research':{'text':research_text,'sha256':sha_text(research_text)},'facts':{'text':facts_text,'sha256':sha_text(facts_text)},'production_context':{'fact_pack':fact,'production_plan_item':plan,'sha256':batch_gate.stable_hash(context)},'draft_markdown':draft,'draft_sha256':sha_text(draft),'checks':{'status':'PASS','mode':'FULL_PRODUCTION','errors':[],'checked_draft_sha256':sha_text(draft),'production_evidence':production_evidence(draft)},'last_error':None,'release_prepared':None,'released':False}
        bind_authoring_contract(state)
        state['immutable_core_sha256']=batch_gate.stable_hash(batch_gate.immutable_core(state)); w=root/f'item-{i:06d}'; w.mkdir(); (w/'bound_snapshot.json').write_bytes(bound_raw); p=w/'state.json'; p.write_text(json.dumps(state,ensure_ascii=False),encoding='utf-8'); paths.append(p)
    return snap,paths
class E2ESubsetAcceptanceTests(unittest.TestCase):
    def _cleanup(self, result):
        root=Path(result['run_root'])
        if root.exists(): shutil.rmtree(root)

    def test_subset_prepare_allows_only_bound_one_and_three_without_live_mutation(self):
        live_snapshot=REPO/'control/startmaster0107/runtime_inbox/generations/000001/SOURCE_SNAPSHOT.json'
        live_requests=REPO/'control/startmaster0107/runtime_inbox/generations/000001/SOURCE_REQUESTS.json'
        before_snapshot=hashlib.sha256(live_snapshot.read_bytes()).hexdigest()
        before_requests=hashlib.sha256(live_requests.read_bytes()).hexdigest()
        results=[]
        try:
            for count in (1,3):
                result=e2e_acceptance_subset.prepare(count)
                results.append(result)
                root=Path(result['run_root'])
                snapshot=json.loads((root/'snapshot.json').read_text(encoding='utf-8'))
                request=json.loads((root/'source_requests.json').read_text(encoding='utf-8'))
                batch=snapshot['next_textmachine_metadata_batch']
                self.assertEqual(batch['item_count'],count)
                self.assertEqual(len(batch['items']),count)
                self.assertEqual(request['item_count'],count)
                self.assertEqual(len(request['items']),count)
                self.assertEqual(batch['batch_sha256'],request['batch_sha256'])
                self.assertNotEqual(batch['batch_sha256'],result['original_bound_batch_sha256'])
                self.assertFalse(batch['publish_allowed'])
                self.assertFalse(request['publish_allowed'])
                self.assertTrue(result['test_only'])
                self.assertFalse(result['production_route_changed'])
                self.assertFalse(result['publish_allowed'])
            for bad in (0,2,7):
                with self.assertRaisesRegex(e2e_acceptance_subset.AcceptanceBlocked,'ACCEPTANCE_COUNT_NOT_AUTHORIZED'):
                    e2e_acceptance_subset.prepare(bad)
            self.assertEqual(hashlib.sha256(live_snapshot.read_bytes()).hexdigest(),before_snapshot)
            self.assertEqual(hashlib.sha256(live_requests.read_bytes()).hexdigest(),before_requests)
        finally:
            for result in results: self._cleanup(result)

    def test_subset_root_starts_index_zero_and_advance_before_pass_blocks(self):
        result=e2e_acceptance_subset.prepare(1)
        root=Path(result['run_root'])
        try:
            with self.assertRaisesRegex(
                e2e_acceptance_subset.AcceptanceBlocked,
                'ACCEPTANCE_107008_CANONICAL_BOUNDARY',
            ):
                e2e_acceptance_subset.prepare_107008(root)
            requests=json.loads((root/'source_requests.json').read_text(encoding='utf-8'))
            rows=[]
            for item in requests['items']:
                sources=[]
                for source in item['sources']:
                    evidence=(
                        'Frisch gebundener Acceptance-Quellenbeleg mit genügend konkretem Inhalt '
                        'für die unveränderte Point-0-Validierung dieses aktuellen Artikels.'
                    )
                    sources.append({
                        'source_id':source['source_id'],
                        'source_title':source['source_title'],
                        'source_url':source['source_url'],
                        'retrieved_at':'2026-09-18T20:00:00+00:00',
                        'evidence':evidence,
                        'snapshot_sha256':hashlib.sha256(evidence.encode('utf-8')).hexdigest(),
                        'http_status':200,
                        'source_kind':source.get('source_kind') or 'WEB',
                    })
                rows.append({'item_index':item['item_index'],'plan_slot':item['plan_slot'],'sources':sources})
            acquired={'contract':'SYSTEM4_MACHINE_ACQUIRED_SOURCE_BATCH_V1','item_count':1,'items':rows}
            (root/'acquired.json').write_text(json.dumps(acquired,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
            meta=json.loads((root/e2e_acceptance_subset.META_NAME).read_text(encoding='utf-8'))
            meta['status']='ACQUIRED'
            meta['acquired_sha256']=hashlib.sha256((root/'acquired.json').read_bytes()).hexdigest()
            (root/e2e_acceptance_subset.META_NAME).write_text(json.dumps(meta,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')

            bound=e2e_acceptance_subset.bind_acquired(root)
            self.assertEqual(bound['status'],'SYSTEM4_E2E_ACCEPTANCE_ROOT_READY_STOP')
            self.assertEqual(bound['article_count'],1)
            self.assertEqual(bound['item_index'],0)
            self.assertFalse(bound['worker_started'])
            self.assertFalse(bound['advance_invoked'])
            self.assertFalse(bound['publish_allowed'])
            workspace=Path(bound['workspace'])
            state=json.loads((workspace/'state.json').read_text(encoding='utf-8'))
            self.assertEqual(state['phase'],'RESEARCH_REQUIRED')
            batch_state=json.loads((Path(bound['batch_root'])/e2e_acceptance_subset.BATCH_STATE_NAME).read_text(encoding='utf-8'))
            self.assertEqual(batch_state['started_indices'],[0])
            self.assertEqual(batch_state['completed_indices'],[])
            with self.assertRaisesRegex(e2e_acceptance_subset.AcceptanceBlocked,'ACCEPTANCE_CURRENT_ITEM_NOT_PASS:0'):
                e2e_acceptance_subset.advance(root)
        finally:
            self._cleanup(result)

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
            self.assertEqual(result['status'],'SYSTEM4_BATCH_FULL_PASS_COLLECTED'); self.assertEqual(result['article_count'],7); self.assertEqual(result['next_required'],batch_gate.NEXT_REQUIRED); self.assertEqual(result['next_required'],'PARENT_CHAT_WORDPRESS_HANDOFF_REQUIRED'); self.assertFalse(result['publish_allowed']); self.assertEqual(len(list(out.glob('ARTICLE_*.md'))),7)
            self.assertNotEqual(json.loads(paths[0].read_text())['source_snapshot_sha256'], hashlib.sha256(snap.read_bytes()).hexdigest())
            evidence=json.loads((out/'system4_batch_evidence.json').read_text()); self.assertEqual(evidence['article_count'],7); self.assertEqual(evidence['next_required'],batch_gate.NEXT_REQUIRED); self.assertTrue(all(row['quality']['languagetool']['status']=='PASS' for row in evidence['articles'])); self.assertTrue(all(row['design']['status']=='PASS' for row in evidence['articles'])); self.assertFalse(evidence['design_mutation_performed']); self.assertEqual(evidence['batch_distinctness']['status'],'PASS')
        finally: td.cleanup()
    def test_missing_state(self): self.assert_blocked('STATE_COUNT_MISMATCH',path_count=6)
    def test_order_mismatch_blocked(self):
        def m(r,s,p): p[0],p[1]=p[1],p[0]
        self.assert_blocked('STATE_ORDER_MISMATCH:0',m)
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
    def test_bound_snapshot_missing_blocked(self):
        def m(r,s,p): (p[2].parent/'bound_snapshot.json').unlink()
        self.assert_blocked('STATE_BOUND_SNAPSHOT_MISSING',m)
    def test_bound_snapshot_batch_drift_blocked(self):
        def m(r,s,p):
            bp=p[2].parent/'bound_snapshot.json'; x=json.loads(bp.read_text()); x['next_textmachine_metadata_batch']['items'][2]['title']='Falsch'; bp.write_text(json.dumps(x,ensure_ascii=False))
            st=json.loads(p[2].read_text()); st['source_snapshot_sha256']=hashlib.sha256(bp.read_bytes()).hexdigest(); st['immutable_core_sha256']=batch_gate.stable_hash(batch_gate.immutable_core(st)); p[2].write_text(json.dumps(st,ensure_ascii=False))
        self.assert_blocked('STATE_BOUND_SNAPSHOT_BATCH_MISMATCH',m)
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
    def test_authoring_contract_missing_blocked(self):
        def m(r,s,p): x=json.loads(p[2].read_text()); x.pop('authoring_contract'); p[2].write_text(json.dumps(x))
        self.assert_blocked('AUTHORING_CONTRACT_NOT_PASS:AUTHORING_CONTRACT_MISSING',m)
    def test_design_drift_is_blocked_even_after_full_pass(self):
        def m(r,s,p):
            x=json.loads(p[2].read_text()); old=x['draft_markdown']; new=old.replace('system-129-table comparison-table','comparison-table'); x['draft_markdown']=new; x['draft_sha256']=sha_text(new); x['checks']['checked_draft_sha256']=sha_text(new); x['checks']['production_evidence']=production_evidence(new); p[2].write_text(json.dumps(x))
        self.assert_blocked('DESIGN_GUARD_NOT_PASS:DESIGN_TABLE_SYSTEM129_CLASS_MISSING',m)
if __name__=='__main__': unittest.main(verbosity=2)
