import copy,hashlib,json,tempfile,unittest
from pathlib import Path
import authoring_contract,batch_gate,design_guard,production_binding

HERE=Path(__file__).resolve().parent; REPO=HERE.parent; LIVE=HERE/'live_fixture/wordpress_snapshot.json'
def sha_text(v): return hashlib.sha256(v.encode('utf-8')).hexdigest()

class UniversalBatchGateTests(unittest.TestCase):
    def production_evidence(self,draft):
        d=sha_text(draft); return {'contract':'SYSTEM4_FULL_PRODUCTION_CHECK_V1','status':'PASS','checked_draft_sha256':d,'publish_allowed':False,'evidence':{'no_legacy':{'status':'PASS','legacy_import_count':0},'no_external_links':{'status':'PASS','external_link_count':0},'languagetool':{'status':'PASS','engine':'LanguageTool 6.8 / Bestand 43','finding_count':0},'ppm679':{'status':'PASS','ppm_version':'6.7.9','technical_status':'TECHNICAL_CHECK_OK','content_quality_status':'CONTENT_QUALITY_CHECK_OK','fail_closed_aggregate_status':'PASS','content_sha256':d,'language_evidence_source':'REAL_LT68_CURRENT_DRAFT_REFRESHED'}}}
    def evidence(self,i,source_snapshot_id):
        sid=f'src-{i}'; chunks=[f'Erster gebundener Beleg für Skalierungsartikel {i}.',f'Zweiter verschiedener gebundener Beleg für Skalierungsartikel {i}.',f'Dritter verschiedener gebundener Beleg für Skalierungsartikel {i}.']; ev='\n'.join(chunks)
        source={'source_id':sid,'source_title':f'Fachquelle {i}','source_url':f'https://example.org/source-{i}','retrieved_at':'2026-09-13T08:00:00Z','snapshot_sha256':sha_text(ev),'evidence':ev}
        claims=[{'fact_id':f'fact-{i}-{n}','source_id':sid,'statement':f'Gebundene Aussage {n+1} für Artikel {i}.','evidence_text':text,'evidence_text_sha256':sha_text(text),'claim_status':'FULLY_SUPPORTED','article_types':['Beratung']} for n,text in enumerate(chunks)]
        return {'contract':'SYSTEM4_RESEARCH_EVIDENCE_V1','sources':[copy.deepcopy(source)]},{'contract':'SYSTEM4_FACTS_EVIDENCE_V1','claims':copy.deepcopy(claims)},{'contract':'canonical_fact_pack_v1','status':'SOURCE_VERIFIED_PRODUCTION_READY','source_snapshot_id':source_snapshot_id,'fact_pack_id':source_snapshot_id,'sources':[copy.deepcopy(source)],'claims':copy.deepcopy(claims)}
    def make_fixture(self,root,count):
        real=json.loads(LIVE.read_text(encoding='utf-8'))['next_textmachine_metadata_batch']['items']; bases=[x for x in real if x['article_type']=='Beratung']
        items=[]
        for i in range(count):
            b=copy.deepcopy(bases[i%len(bases)]); b['title']=f'{b["title"]} – Skalierung {i+1}'; b['target_keyword']=f'{b["target_keyword"]} Skalierung {i+1}'; b['plan_slot']=sha_text(f'universal-slot-{i}'); items.append(b)
        batch_sha=sha_text('universal-batch-'+str(count)); snapshot={'contract':'SYSTEM4_WORDPRESS_LIVE_INPUT_FIXTURE_V1','next_textmachine_metadata_batch':{'contract':'PSERC_TEXTMACHINE_METADATA_BATCH_V2','status':'READY_FOR_TEXTMACHINE_METADATA_INTAKE','batch_sha256':batch_sha,'item_count':count,'items':items,'publish_allowed':False}}
        snap=root/'snapshot.json'; snap.write_text(json.dumps(snapshot,ensure_ascii=False,sort_keys=True,separators=(',',':')),encoding='utf-8'); snap_sha=hashlib.sha256(snap.read_bytes()).hexdigest(); paths=[]
        for i,item in enumerate(items):
            unique=' '.join(f'eigen{i}_{n}' for n in range(45)); draft=f'<article class="ppm-generated {design_guard.article_type_class(item["article_type"])}" data-article-type="{item["article_type"]}"><h2>{item["title"]}</h2><p data-fact-ids="fact-{i}-0 fact-{i}-1 fact-{i}-2">{item["target_keyword"]} {unique}</p><table class="system-129-table comparison-table"><tr><th>Kriterium</th><th>Wert</th></tr><tr><td>{i}</td><td>{i}</td></tr></table></article>'
            research,facts,pack=self.evidence(i,snap_sha); base_plan={'article_type':'Beratung','target_keyword':item['target_keyword'],'topic':item['title'],'source_snapshot_id':snap_sha,'runtime_order':{'order_id':f'universal-{i}','article_type':'Beratung','title':item['title'],'slug':f'universal-{i}','subject_scope':'universal_batch_scaling','subject_label':item['target_keyword'],'lead':'Gebundener Skalierungstest mit klarer Aussage.','conclusion':'Gebundener Abschluss des Skalierungstests.','allowed_fact_ids':[f'fact-{i}-0',f'fact-{i}-1',f'fact-{i}-2']}}
            shell={'article':copy.deepcopy(item),'source_snapshot_sha256':snap_sha}; plan=production_binding.bind_plan(REPO,shell,pack,base_plan); plan['canonical_article']={'body_html':draft}; contract=authoring_contract.build(REPO,shell,pack,plan); ctx={'fact_pack':pack,'production_plan_item':plan}; rt=json.dumps(research,ensure_ascii=False,sort_keys=True); ft=json.dumps(facts,ensure_ascii=False,sort_keys=True)
            state={'contract':batch_gate.STATE_CONTRACT,'source_snapshot_sha256':snap_sha,'batch_sha256':batch_sha,'article':copy.deepcopy(item),'immutable_core_sha256':'','publish_allowed':False,'phase':'OUTPUT_GATE_REQUIRED','revision':1,'research':{'text':rt,'sha256':sha_text(rt)},'facts':{'text':ft,'sha256':sha_text(ft)},'production_context':{'fact_pack':pack,'production_plan_item':plan,'sha256':batch_gate.stable_hash(ctx)},'authoring_contract':contract,'draft_markdown':draft,'draft_sha256':sha_text(draft),'checks':{'status':'PASS','mode':'FULL_PRODUCTION','errors':[],'checked_draft_sha256':sha_text(draft),'production_evidence':self.production_evidence(draft)},'last_error':None,'release_prepared':None,'released':False}
            state['immutable_core_sha256']=batch_gate.stable_hash(batch_gate.immutable_core(state)); p=root/f'state-{i}.json'; p.write_text(json.dumps(state,ensure_ascii=False),encoding='utf-8'); paths.append(p)
        return snap,paths
    def test_batch_gate_accepts_one_and_mixed_sizes(self):
        for count in (1,3,25):
            with self.subTest(count=count),tempfile.TemporaryDirectory() as td:
                root=Path(td); snap,states=self.make_fixture(root,count); result=batch_gate.collect_batch(snap,states,root/'out'); self.assertEqual(result['article_count'],count); self.assertEqual(result['status'],'SYSTEM4_BATCH_FULL_PASS_COLLECTED')

if __name__=='__main__': unittest.main(verbosity=2)
