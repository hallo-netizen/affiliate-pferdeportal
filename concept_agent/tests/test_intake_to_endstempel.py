import hashlib,json,sys,tempfile,unittest
from pathlib import Path
OFFICE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(OFFICE))
import intake_bridge as intake
import endstempel_bridge as end

def stable(v):
    return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def snapshot(n):
    items=[]
    for i in range(n):
        items.append({'title':f'Fiktiver Testartikel {i}','target_keyword':f'Testkeyword {i}','category':'test-beratung','article_type':'Beratung','plan_slot':hashlib.sha256(f'flow-slot-{i}'.encode()).hexdigest()})
    batch={'contract':intake.BATCH_CONTRACT,'status':intake.READY_STATUS,'item_count':n,'maximum_articles':0,'maximum_articles_per_type':0,'publish_allowed':False,'content_or_format_payload_present':False,'items':items}
    batch['batch_sha256']=stable(batch)
    return {'contract':intake.SNAPSHOT_CONTRACT,'hard_rules':{'approved_research_text_process_required':True,'text_machine_is_only_content_and_format_authority':True,'metadata_handoff_exact_scalar_fields':list(intake.EXACT_FIELDS)},'next_step':intake.NEXT_STEP,'next_textmachine_metadata_batch':batch}

def research(req):
    rows=[]
    for a in req['items']:
        ev=f'Lokale, hashgebundene Evidenz für Testartikel {a["item_index"]}; keine freie Nachmutation.'
        rows.append({'item_index':a['item_index'],'plan_slot':a['plan_slot'],'sources':[{'source_id':f'local-{a["item_index"]}','source_title':'Hobbyraum-Testquelle','source_url':f'https://example.test/flow/{a["item_index"]}','evidence':ev,'snapshot_sha256':hashlib.sha256(ev.encode()).hexdigest()}]})
    return {'contract':intake.RESEARCH_SUBMISSION_CONTRACT,'batch_sha256':req['batch_sha256'],'item_count':req['item_count'],'items':rows}

def approved_request(req,bound):
    release_items=[]; plan_items=[]; articles=[]
    for a,r in zip(req['items'],bound['items']):
        cid=f'article:test-{a["item_index"]}'
        fact=f'fact-{a["item_index"]}'
        src=r['sources'][0]
        body=(f'<article class="ppm-generated ppm-type-beratung" data-article-type="Beratung">'
              f'<section data-block="intro"><p data-fact-ids="{fact}">{a["title"]}: gebundener lokaler Integrationstest.'
              f'<span class="ppm-source-trace" data-fact-id="{fact}" data-source-hash="{src["snapshot_sha256"]}" data-source-title="{src["source_id"]}"></span>'
              f'</p></section></article>')
        release_items.append({'plan_slot':a['plan_slot'],'canonical_article_id':cid})
        plan_items.append({'canonical_article_id':cid,'canonical_article':{'body_html':body}})
        articles.append({'plan_slot':a['plan_slot'],'content_utf8':body})
    env={'contract':end.PACKAGE_CONTRACT,'fact_pack_bundle':{},'production_plan':{'items':plan_items},'workflow_release':{'contract':'WORKFLOW_SUPERVISOR_RELEASE_V2_SIGNED','status':'PASS','wordpress_write_performed':False,'exact_five_batch_sha256':req['batch_sha256'],'items':release_items}}
    return {'contract':end.REQ_CONTRACT,'batch_sha256':req['batch_sha256'],'runtime_generation':1,'import_envelope':env,'articles':articles,'publish_allowed':False,'content_mutation_performed':False}

class FullFlow(unittest.TestCase):
    def run_flow(self,n):
        req=intake.prepare(snapshot(n)); bound=intake.bind_research(req,research(req)); package=approved_request(req,bound)
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); p=root/'concept_agent/production_ready/run.json'; p.parent.mkdir(parents=True); p.write_text(json.dumps(package),encoding='utf-8')
            old=end.REPO; end.REPO=root
            try:
                ref=end.build(str(p.relative_to(root)))
                manifest=json.loads((root/ref).read_text())
                self.assertEqual(manifest['item_count'],n)
                for row in manifest['items']:
                    self.assertTrue((root/row['ref']).is_file())
                return manifest
            finally: end.REPO=old

    def test_positive_one_article_end_to_end(self): self.run_flow(1)
    def test_positive_three_articles_end_to_end(self): self.run_flow(3)

    def test_negative_postapproval_html_mutation_blocks(self):
        req=intake.prepare(snapshot(1)); bound=intake.bind_research(req,research(req)); package=approved_request(req,bound)
        package['articles'][0]['content_utf8']+='<p>mutiert</p>'
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); p=root/'concept_agent/production_ready/run.json'; p.parent.mkdir(parents=True); p.write_text(json.dumps(package),encoding='utf-8')
            old=end.REPO; end.REPO=root
            try:
                with self.assertRaisesRegex(end.Blocked,'IMPORT_ENVELOPE_ARTICLE_MISMATCH'): end.build(str(p.relative_to(root)))
            finally: end.REPO=old

if __name__=='__main__': unittest.main(verbosity=2)
