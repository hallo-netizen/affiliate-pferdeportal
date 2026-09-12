import base64, hashlib, json, tempfile, unittest
from pathlib import Path
import handoff_transport as ht

def sha(value): return hashlib.sha256(value.encode('utf-8')).hexdigest()

class HandoffTransportTests(unittest.TestCase):
    def fact_pack(self,i):
        source_id=f'src-{i}'
        source_snapshot=sha(f'Quellensnapshot {i} mit ausreichend langem konkretem Inhalt für die lokale Prüfung der Handoff-Bindung.')
        e1=f'Konkreter Beleg A für den Handoff-Testartikel {i} und seine fachliche Aussage.'
        e2=f'Konkreter Beleg B für den Handoff-Testartikel {i} und seine zweite fachliche Aussage.'
        return {
            'contract':'canonical_fact_pack_v1','status':'SOURCE_VERIFIED_PRODUCTION_READY',
            'sources':[{'source_id':source_id,'source_title':f'Fachquelle Handoff {i}','source_url':f'https://example.org/handoff-{i}','retrieved_at':'2026-09-12T20:00:00Z','snapshot_sha256':source_snapshot}],
            'claims':[
                {'fact_id':f'fact-{i}-a','source_id':source_id,'statement':f'Konkrete Aussage A für Handoff {i}.','evidence_text':e1,'evidence_text_sha256':sha(e1)},
                {'fact_id':f'fact-{i}-b','source_id':source_id,'statement':f'Konkrete Aussage B für Handoff {i}.','evidence_text':e2,'evidence_text_sha256':sha(e2)},
            ]}
    def payload(self):
        rows=[]
        for i in range(7):
            unique=' '.join(f'eigen{i}_{n}' for n in range(70))
            body=f'<article><p data-fact-ids="fact-{i}-a fact-{i}-b">Artikel {i} {unique}</p></article>'
            body_sha=hashlib.sha256(body.encode()).hexdigest()
            rows.append({
                'index':i,'title':f'Titel {i}','target_keyword':f'Keyword {i}','category':f'cat-{i}','article_type':'Beratung','plan_slot':hashlib.sha256(f'slot-{i}'.encode()).hexdigest(),
                'final_draft_sha256':body_sha,'revision_count':1,'body':body,
                'production_context':{'fact_pack':self.fact_pack(i),'production_plan_item':{'contract':'production_plan_v4'}},
                'languagetool':{'status':'PASS','finding_count':0,'engine':'LanguageTool 6.8 / Bestand 43'},
                'ppm679':{'status':'PASS','ppm_version':'6.7.9','technical_status':'TECHNICAL_CHECK_OK','content_quality_status':'CONTENT_QUALITY_CHECK_OK','fail_closed_aggregate_status':'PASS','content_sha256':body_sha},
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
    def test_negative_missing_fact_sources(self):
        p=self.payload(); p['articles'][0]['production_context']['fact_pack'].pop('sources')
        with self.assertRaisesRegex(ht.HandoffError,'HANDOFF_CONTENT_GUARD:0:FACT_PACK_SOURCES_MISSING'): ht.validate_handoff(p)
    def test_negative_template_reuse(self):
        p=self.payload()
        common='<article><p data-fact-ids="fact-{i}-a fact-{i}-b">Eine gute Entscheidung beginnt mit einer Bestandsaufnahme. Notiere wie häufig die Lösung gebraucht wird und welche Bedingungen bestehen. Eine gute Entscheidung beginnt mit einer Bestandsaufnahme. Notiere wie häufig die Lösung gebraucht wird und welche Bedingungen bestehen. Artikel {i}</p></article>'
        for i,row in enumerate(p['articles']):
            row['body']=common.format(i=i); row['final_draft_sha256']=sha(row['body']); row['ppm679']['content_sha256']=row['final_draft_sha256']
        with self.assertRaisesRegex(ht.HandoffError,'BATCH_TEMPLATE_REUSE_BLOCKED'): ht.validate_handoff(p)
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
