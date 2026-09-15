from __future__ import annotations
import copy, hashlib, json, unittest
import chat_start_gate, point0_snapshot, source_acquisition

def stable(v): return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def fixture():
    article={'title':'Testartikel Pferdepflege','target_keyword':'Pferdepflege Test','category':'test-beratung','article_type':'Beratung','plan_slot':'slot-test-001'}
    link={'active':True,'anchor':'Test Beratung','hierarchy_path':['Test'],'href':'/test-beratung/','reason':'Test','role':'parent_category','section_id':'criteria','snapshot_contract':'WORDPRESS_LINK_TARGET_SNAPSHOT_V1','target_status':'publish','target_type':'page'}
    registry={'contract':'portal_link_registry_snapshot_v2','entries':[copy.deepcopy(link)]}
    quality={'contract':'content_structure_language_binding_v2','link_bindings':[copy.deepcopy(link)],'portal_link_registry':registry,'portal_link_registry_hash':stable(registry),'wordpress_category':{'slug':'test-beratung'}}
    plan={'article_type':'Beratung','target_keyword':'Pferdepflege Test','topic':'Testartikel Pferdepflege','search_intent':'DECISION_SUPPORT','gold_core_binding':'TEST','category_binding':{'slug':'test-beratung'},'quality_binding':quality,'quality_binding_hash':stable(quality)}
    pre=point0_snapshot.prewrite_from_plan(article,0,plan)
    evidence='Dies ist ausreichend langer Evidenztext für den gebundenen System-4-Testartikel.'
    src={'source_id':'s1','source_title':'Testquelle','source_url':'https://example.test/a','retrieved_at':'2026-09-14T00:00:00Z','evidence':evidence,'snapshot_sha256':hashlib.sha256(evidence.encode()).hexdigest(),'http_status':200,'source_kind':'WEB'}
    manifest='1'*64; snap={'contract':'SYSTEM4_WORDPRESS_LIVE_INPUT_FIXTURE_V1','next_textmachine_metadata_batch':{'contract':'PSERC_TEXTMACHINE_METADATA_BATCH_V2','status':'READY_FOR_TEXTMACHINE_METADATA_INTAKE','batch_sha256':'2'*64,'item_count':1,'items':[article],'publish_allowed':False},'system4_root_manifest_sha256':manifest}
    event={'contract':chat_start_gate.START_EVENT_CONTRACT,'button_id':chat_start_gate.START_BUTTON_ID,'action':chat_start_gate.START_ACTION,'route':chat_start_gate.START_ROUTE,'article_count':1,'batch_sha256':'2'*64,'publish_allowed':False}
    snap=chat_start_gate.bind(snap,event); raw=(json.dumps(snap,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode()
    p0=point0_snapshot.build(production_snapshot_bytes=raw,root_manifest_sha256=manifest,head_sha='3'*40,research_provider='TEST',source_pools=[[src]],prewrite_bindings=[pre])
    return p0

def verified_snapshot(p0):
    raw=point0_snapshot.verify(p0)
    return json.loads(raw.decode('utf-8'))

class Point0V2Tests(unittest.TestCase):
    def test_source_acquisition_200_401_403(self):
        req={'contract':source_acquisition.CONTRACT,'item_count':1,'items':[{'item_index':0,'plan_slot':'slot-x','sources':[{'source_id':'s1','source_url':'https://example.test/a','source_title':'Quelle'}]}]}
        def ok(url,timeout,max_bytes): return {'http_status':200,'body':b'<html><title>T</title><body><p>Dies ist ausreichend langer echter Evidenztext fuer den Vertrag.</p></body></html>','content_type':'text/html; charset=utf-8'}
        out=source_acquisition.acquire_batch(req,fetcher=ok,retrieved_at='2026-09-14T00:00:00Z'); self.assertEqual(out['items'][0]['sources'][0]['http_status'],200)
        for code in (401,403):
            def bad(url,timeout,max_bytes,c=code): return {'http_status':c,'body':b'','content_type':'text/plain'}
            with self.assertRaisesRegex(source_acquisition.SourceAcquisitionError,rf'SOURCE_HTTP_FAIL:0:0:{code}'): source_acquisition.acquire_batch(req,fetcher=bad,retrieved_at='2026-09-14T00:00:00Z')
    def test_chat_start_required_tamper_and_dataforseo_blocked(self):
        p0=fixture(); snap=verified_snapshot(p0); receipt=chat_start_gate.validate(snap); self.assertEqual(receipt['contract'],chat_start_gate.START_RECEIPT_CONTRACT)
        missing=copy.deepcopy(snap); missing.pop('system4_chat_start')
        with self.assertRaisesRegex(chat_start_gate.ChatStartError,'CHAT_START_RECEIPT_REQUIRED'): chat_start_gate.validate(missing)
        tampered=copy.deepcopy(snap); tampered['system4_chat_start']['batch_sha256']='f'*64
        with self.assertRaisesRegex(chat_start_gate.ChatStartError,'CHAT_START_RECEIPT_INTEGRITY_FAIL'): chat_start_gate.validate(tampered)
        poisoned=copy.deepcopy(snap); poisoned['research_provider']='DataForSEO'
        with self.assertRaisesRegex(chat_start_gate.ChatStartError,'DATAFORSEO_FORBIDDEN_IN_SYSTEM4A'): chat_start_gate.validate(poisoned)
        with self.assertRaisesRegex(chat_start_gate.ChatStartError,'DATAFORSEO_FORBIDDEN_IN_SYSTEM4A'): chat_start_gate.forbid_dataforseo({'source_url':'https://api.dataforseo.com/v3/test'})
    def test_point0_and_prewrite_tamper_fail_closed(self):
        p0=fixture(); snap=verified_snapshot(p0); chat_start_gate.validate(snap)
        bad=copy.deepcopy(p0); bad['research_runtime']['item_pools'][0]['sources'][0]['source_title']+=' X'
        with self.assertRaisesRegex(point0_snapshot.Point0Error,'POINT0_INTEGRITY_FAIL'): point0_snapshot.verify(bad)
        bad=copy.deepcopy(p0); pre=bad['machine_prewrite']['items'][0]; pre['production_plan_rails']['quality_binding']['link_bindings'][0]['anchor']='Manipuliert'; core=dict(bad); core.pop('point0_core_sha256',None); bad['point0_core_sha256']=point0_snapshot.sha256(point0_snapshot.canon(core))
        with self.assertRaisesRegex(point0_snapshot.Point0Error,'PREWRITE_INTEGRITY_FAIL:0'): point0_snapshot.verify(bad)
if __name__=='__main__': unittest.main()
