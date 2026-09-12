import base64, copy, hashlib, json, tempfile, unittest
from pathlib import Path
import handoff_transport as ht

class HandoffTransportTests(unittest.TestCase):
    def payload(self):
        rows=[]
        for i in range(7):
            body=f'<article><p>Artikel {i}</p></article>'
            sha=hashlib.sha256(body.encode()).hexdigest()
            rows.append({
                'index':i,'title':f'Titel {i}','target_keyword':f'Keyword {i}','category':f'cat-{i}','article_type':'Beratung','plan_slot':hashlib.sha256(f'slot-{i}'.encode()).hexdigest(),
                'final_draft_sha256':sha,'revision_count':1,'body':body,
                'production_context':{'fact_pack':{'contract':'canonical_fact_pack_v1'},'production_plan_item':{'contract':'production_plan_v4'}},
                'languagetool':{'status':'PASS','finding_count':0,'engine':'LanguageTool 6.8 / Bestand 43'},
                'ppm679':{'status':'PASS','ppm_version':'6.7.9','technical_status':'TECHNICAL_CHECK_OK','content_quality_status':'CONTENT_QUALITY_CHECK_OK','fail_closed_aggregate_status':'PASS','content_sha256':sha},
            })
        return {
            'contract':ht.HANDOFF_CONTRACT,'batch_sha256':hashlib.sha256(b'batch').hexdigest(),'publish_allowed':False,'signing_deferred':True,
            'batch_gate_status':'SYSTEM4_BATCH_FULL_PASS_COLLECTED','no_legacy_status':'PASS','test_suite_status':'PASS',
            'wordpress_review':{
                'file_format':'JSON','mime_type':'application/json','intended_next_step':'WORDPRESS_PREIMPORT_REVIEW','plugin_name':'Portal SEO Editorial Plan Compiler',
                'plugin_version_verified_against':'0.28.22','ppm_version_verified_against':'6.7.9','direct_wordpress_upload_ready':False,
                'direct_upload_block_reason':'REQUIRES_PSERC_IMPORT_ENVELOPE_AND_SUPERVISOR_AUTHENTICITY','required_downstream_components':['fact_pack_bundle','production_plan','workflow_release']
            },
            'articles':rows,
        }
    def write(self,p,obj):
        p.write_text(json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    def test_positive_pack_unpack_exact_bytes(self):
        with tempfile.TemporaryDirectory() as td:
            td=Path(td); src=td/ht.HANDOFF_FILENAME; tr=td/ht.TRANSPORT_FILENAME; out=td/'out'
            self.write(src,self.payload()); raw=src.read_bytes(); env=ht.pack(src,tr); dst=ht.unpack(tr,out)
            self.assertEqual(raw,dst.read_bytes()); self.assertEqual(env['plaintext_sha256'],hashlib.sha256(raw).hexdigest())
    def test_negative_transport_tamper(self):
        with tempfile.TemporaryDirectory() as td:
            td=Path(td); src=td/ht.HANDOFF_FILENAME; tr=td/ht.TRANSPORT_FILENAME
            self.write(src,self.payload()); ht.pack(src,tr); env=json.loads(tr.read_text()); raw=base64.b64decode(env['payload_base64']); raw=raw+b'X'; env['payload_base64']=base64.b64encode(raw).decode(); tr.write_text(json.dumps(env))
            with self.assertRaisesRegex(ht.HandoffError,'TRANSPORT_LENGTH_MISMATCH'): ht.unpack(tr,td/'out')
    def test_negative_body_hash(self):
        p=self.payload(); p['articles'][0]['body']+='x'
        with self.assertRaisesRegex(ht.HandoffError,'HANDOFF_BODY_SHA_MISMATCH:0'): ht.validate_handoff(p)
    def test_negative_wordpress_review_missing(self):
        p=self.payload(); del p['wordpress_review']
        with self.assertRaisesRegex(ht.HandoffError,'HANDOFF_SCHEMA_INVALID'): ht.validate_handoff(p)
    def test_negative_false_upload_ready_claim(self):
        p=self.payload(); p['wordpress_review']['direct_wordpress_upload_ready']=True
        with self.assertRaisesRegex(ht.HandoffError,'HANDOFF_MUST_NOT_FALSELY_CLAIM_UPLOAD_READY'): ht.validate_handoff(p)
    def test_negative_article_count(self):
        p=self.payload(); p['articles'].pop()
        with self.assertRaisesRegex(ht.HandoffError,'HANDOFF_ARTICLE_COUNT_INVALID'): ht.validate_handoff(p)

if __name__=='__main__': unittest.main(verbosity=2)
