import base64, hashlib, json, tempfile, unittest
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
                'file_format':'JSON','mime_type':'application/json','intended_next_step':'WORDPRESS_DIRECT_IMPORT','plugin_name':'Portal SEO Editorial Plan Compiler',
                'plugin_version_verified_against':'0.28.22','ppm_version_verified_against':'6.7.9','direct_wordpress_upload_ready':True,
                'direct_upload_block_reason':None,'required_downstream_components':[]
            },
            'articles':rows,
        }
    def write(self,p,obj):
        p.write_text(json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')

    def test_positive_inline_roundtrip_exact_canonical_bytes(self):
        with tempfile.TemporaryDirectory() as td:
            td=Path(td); src=td/'source.json'; canonical=td/ht.HANDOFF_FILENAME; inline=td/ht.INLINE_FILENAME; out=td/'out'
            self.write(src,self.payload())
            expected=ht.canonicalize_handoff(src,canonical)
            env=ht.inline_pack(canonical,inline)
            dst=ht.inline_unpack(inline,out)
            self.assertEqual(expected,dst.read_bytes())
            self.assertEqual(env['plaintext_sha256'],hashlib.sha256(expected).hexdigest())
            self.assertLessEqual(len(inline.read_text(encoding='utf-8')),ht.INLINE_MAX_CHARS)

    def test_negative_inline_tamper(self):
        with tempfile.TemporaryDirectory() as td:
            td=Path(td); src=td/'source.json'; canonical=td/ht.HANDOFF_FILENAME; inline=td/ht.INLINE_FILENAME
            self.write(src,self.payload()); ht.canonicalize_handoff(src,canonical); ht.inline_pack(canonical,inline)
            text=inline.read_text(encoding='utf-8')
            start=text.index(ht.INLINE_BEGIN)+len(ht.INLINE_BEGIN)
            end=text.index(ht.INLINE_END,start)
            env=json.loads(text[start:end].strip())
            raw=base64.b64decode(env['payload_base64']); env['payload_base64']=base64.b64encode(raw+b'X').decode()
            inline.write_text(ht.INLINE_BEGIN+'\n'+json.dumps(env,separators=(',',':'))+'\n'+ht.INLINE_END+'\n',encoding='utf-8')
            with self.assertRaisesRegex(ht.HandoffError,'INLINE_XZ_INVALID'): ht.inline_unpack(inline,td/'out')

    def test_negative_body_hash(self):
        p=self.payload(); p['articles'][0]['body']+='x'
        with self.assertRaisesRegex(ht.HandoffError,'HANDOFF_BODY_SHA_MISMATCH:0'): ht.validate_handoff(p)
    def test_negative_wordpress_review_missing(self):
        p=self.payload(); del p['wordpress_review']
        with self.assertRaisesRegex(ht.HandoffError,'HANDOFF_SCHEMA_INVALID'): ht.validate_handoff(p)
    def test_negative_direct_upload_not_ready(self):
        p=self.payload(); p['wordpress_review']['direct_wordpress_upload_ready']=False
        with self.assertRaisesRegex(ht.HandoffError,'HANDOFF_WORDPRESS_DIRECT_UPLOAD_REQUIRED'): ht.validate_handoff(p)
    def test_negative_preimport_route(self):
        p=self.payload(); p['wordpress_review']['intended_next_step']='WORDPRESS_PREIMPORT_REVIEW'
        with self.assertRaisesRegex(ht.HandoffError,'HANDOFF_WORDPRESS_NEXT_STEP_INVALID'): ht.validate_handoff(p)
    def test_negative_block_reason_present(self):
        p=self.payload(); p['wordpress_review']['direct_upload_block_reason']='ANY_BLOCK'
        with self.assertRaisesRegex(ht.HandoffError,'HANDOFF_WORDPRESS_BLOCK_REASON_MUST_BE_EMPTY'): ht.validate_handoff(p)
    def test_negative_downstream_components_present(self):
        p=self.payload(); p['wordpress_review']['required_downstream_components']=['workflow_release']
        with self.assertRaisesRegex(ht.HandoffError,'HANDOFF_WORDPRESS_DOWNSTREAM_MUST_BE_EMPTY'): ht.validate_handoff(p)
    def test_negative_article_count(self):
        p=self.payload(); p['articles'].pop()
        with self.assertRaisesRegex(ht.HandoffError,'HANDOFF_ARTICLE_COUNT_INVALID'): ht.validate_handoff(p)
    def test_negative_missing_inline_end_marker(self):
        with tempfile.TemporaryDirectory() as td:
            td=Path(td); p=td/'bad.txt'; p.write_text(ht.INLINE_BEGIN+'\n{}\n',encoding='utf-8')
            with self.assertRaisesRegex(ht.HandoffError,'INLINE_END_MISSING'): ht.inline_unpack(p,td/'out')

if __name__=='__main__': unittest.main(verbosity=2)
