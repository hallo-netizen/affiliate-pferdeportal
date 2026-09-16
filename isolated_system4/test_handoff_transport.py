import base64, hashlib, json, tempfile, unittest
from pathlib import Path
import design_guard
import handoff_transport as ht

def sha(value): return hashlib.sha256(value.encode('utf-8')).hexdigest()

class HandoffTransportTests(unittest.TestCase):
    def fact_pack(self,i):
        source_id=f'src-{i}'
        e1=f'Konkreter Beleg A für den Handoff-Testartikel {i} und seine fachliche Aussage.'
        e2=f'Konkreter Beleg B für den Handoff-Testartikel {i} und seine zweite fachliche Aussage.'
        source_evidence=e1+'\n'+e2+'\n'+f'Zusätzlicher gesicherter Quellenkontext für Handoff-Testartikel {i}.'
        return {
            'contract':'canonical_fact_pack_v1','status':'SOURCE_VERIFIED_PRODUCTION_READY',
            'sources':[{'source_id':source_id,'source_title':f'Fachquelle Handoff {i}','source_url':f'https://example.org/handoff-{i}','retrieved_at':'2026-09-12T20:00:00Z','snapshot_sha256':sha(source_evidence),'evidence':source_evidence}],
            'claims':[
                {'fact_id':f'fact-{i}-a','source_id':source_id,'statement':f'Konkrete Aussage A für Handoff {i}.','evidence_text':e1,'evidence_text_sha256':sha(e1)},
                {'fact_id':f'fact-{i}-b','source_id':source_id,'statement':f'Konkrete Aussage B für Handoff {i}.','evidence_text':e2,'evidence_text_sha256':sha(e2)},
            ]}
    def payload(self,count=7,types=None):
        rows=[]; types=types or ['Beratung']
        for i in range(count):
            article_type=types[i%len(types)]
            type_class=design_guard.article_type_class(article_type)
            unique=' '.join(f'eigen{i}_{n}' for n in range(70))
            body=f'<article class="ppm-generated {type_class}" data-article-type="{article_type}"><h2>Abschnitt {i}</h2><p data-fact-ids="fact-{i}-a fact-{i}-b">Artikel {i} {unique}</p><table class="system-129-table comparison-table"><tr><th>A</th><th>B</th></tr><tr><td>{i}</td><td>Wert</td></tr></table></article>'
            body_sha=hashlib.sha256(body.encode()).hexdigest()
            rows.append({
                'index':i,'title':f'Titel {i}','target_keyword':f'Keyword {i}','category':f'cat-{i}','article_type':article_type,'plan_slot':hashlib.sha256(f'slot-{i}'.encode()).hexdigest(),
                'final_draft_sha256':body_sha,'revision_count':1,'body':body,
                'production_context':{'fact_pack':self.fact_pack(i),'production_plan_item':{'contract':'production_plan_v4'}},
                'languagetool':{'status':'PASS','finding_count':0,'engine':'LanguageTool 6.8 / Bestand 43'},
                'ppm679':{'status':'PASS','ppm_version':'6.7.9','technical_status':'TECHNICAL_CHECK_OK','content_quality_status':'CONTENT_QUALITY_CHECK_OK','fail_closed_aggregate_status':'PASS','content_sha256':body_sha},
            })
        return {
            'contract':ht.HANDOFF_CONTRACT,'batch_sha256':hashlib.sha256(f'batch-{count}'.encode()).hexdigest(),'publish_allowed':False,'signing_deferred':True,
            'batch_gate_status':'SYSTEM4_BATCH_FULL_PASS_COLLECTED','no_legacy_status':'PASS','test_suite_status':'PASS',
            'wordpress_review':ht.wordpress_review(),
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
            self.assertGreaterEqual(env['part_count'],1)

    def test_positive_one_article_and_mixed_types(self):
        self.assertEqual(len(ht.validate_handoff(self.payload(1))['articles']),1)
        types=['Beratung','Produktvergleich','Pferderasse','Glossar Begriff']
        p=self.payload(len(types),types)
        ht.validate_handoff(p)
        self.assertEqual([row['article_type'] for row in p['articles']],types)

    def test_negative_inline_tamper(self):
        with tempfile.TemporaryDirectory() as td:
            td=Path(td); src=td/'source.json'; canonical=td/ht.HANDOFF_FILENAME; inline=td/ht.INLINE_FILENAME
            self.write(src,self.payload()); ht.canonicalize_handoff(src,canonical); ht.inline_pack(canonical,inline)
            text=inline.read_text(encoding='utf-8')
            envs=ht._parse_inline_text(text)
            envs[0]['payload_base64']=envs[0]['payload_base64'][:-1] + ('A' if envs[0]['payload_base64'][-1:]!='A' else 'B')
            inline.write_text(ht.INLINE_BEGIN+'\n'+'\n'.join(json.dumps(env,separators=(',',':')) for env in envs)+'\n'+ht.INLINE_END+'\n',encoding='utf-8')
            with self.assertRaisesRegex(ht.HandoffError,'INLINE_(BASE64_INVALID|COMPRESSED_SHA_MISMATCH|XZ_INVALID)'): ht.inline_unpack(inline,td/'out')

    def test_negative_body_hash(self):
        p=self.payload(); p['articles'][0]['body']+='x'
        with self.assertRaisesRegex(ht.HandoffError,'HANDOFF_BODY_SHA_MISMATCH:0'): ht.validate_handoff(p)
    def test_negative_missing_fact_sources(self):
        p=self.payload(); p['articles'][0]['production_context']['fact_pack'].pop('sources')
        with self.assertRaisesRegex(ht.HandoffError,'HANDOFF_CONTENT_GUARD:0:FACT_PACK_SOURCES_MISSING'): ht.validate_handoff(p)
    def test_negative_claim_not_in_source_evidence(self):
        p=self.payload(); row=p['articles'][0]; invented='Ein erfundener Beleg, der nicht im gespeicherten Quellenausschnitt steht.'; row['production_context']['fact_pack']['claims'][0]['evidence_text']=invented; row['production_context']['fact_pack']['claims'][0]['evidence_text_sha256']=sha(invented)
        with self.assertRaisesRegex(ht.HandoffError,'HANDOFF_CONTENT_GUARD:0:FACT_EVIDENCE_NOT_IN_SOURCE'): ht.validate_handoff(p)
    def test_negative_design_drift(self):
        p=self.payload(); row=p['articles'][0]; row['body']=row['body'].replace('system-129-table comparison-table','comparison-table'); row['final_draft_sha256']=sha(row['body']); row['ppm679']['content_sha256']=row['final_draft_sha256']
        with self.assertRaisesRegex(ht.HandoffError,'HANDOFF_DESIGN_GUARD:0:DESIGN_TABLE_SYSTEM129_CLASS_MISSING'): ht.validate_handoff(p)
    def test_negative_template_reuse(self):
        p=self.payload()
        common='<article class="ppm-generated ppm-type-beratung" data-article-type="Beratung"><h2>Auswahl</h2><p data-fact-ids="fact-{i}-a fact-{i}-b">Eine gute Entscheidung beginnt mit einer Bestandsaufnahme. Notiere wie häufig die Lösung gebraucht wird und welche Bedingungen bestehen. Eine gute Entscheidung beginnt mit einer Bestandsaufnahme. Notiere wie häufig die Lösung gebraucht wird und welche Bedingungen bestehen. Artikel {i}</p><table class="system-129-table comparison-table"><tr><th>A</th><th>B</th></tr><tr><td>X</td><td>Y</td></tr></table></article>'
        for i,row in enumerate(p['articles']):
            row['body']=common.format(i=i); row['final_draft_sha256']=sha(row['body']); row['ppm679']['content_sha256']=row['final_draft_sha256']
        with self.assertRaisesRegex(ht.HandoffError,'BATCH_TEMPLATE_REUSE_BLOCKED'): ht.validate_handoff(p)
    def test_negative_wordpress_review_missing(self):
        p=self.payload(); del p['wordpress_review']
        with self.assertRaisesRegex(ht.HandoffError,'HANDOFF_SCHEMA_INVALID'): ht.validate_handoff(p)
    def test_negative_false_direct_upload_ready(self):
        p=self.payload(); p['wordpress_review']['direct_wordpress_upload_ready']=True
        with self.assertRaisesRegex(ht.HandoffError,'HANDOFF_WORDPRESS_DIRECT_UPLOAD_MUST_BE_BLOCKED'): ht.validate_handoff(p)
    def test_negative_direct_import_route(self):
        p=self.payload(); p['wordpress_review']['intended_next_step']='WORDPRESS_DIRECT_IMPORT'
        with self.assertRaisesRegex(ht.HandoffError,'HANDOFF_WORDPRESS_NEXT_STEP_INVALID'): ht.validate_handoff(p)
    def test_negative_block_reason_missing(self):
        p=self.payload(); p['wordpress_review']['direct_upload_block_reason']=None
        with self.assertRaisesRegex(ht.HandoffError,'HANDOFF_WORDPRESS_BLOCK_REASON_INVALID'): ht.validate_handoff(p)
    def test_negative_downstream_components_missing(self):
        p=self.payload(); p['wordpress_review']['required_downstream_components']=[]
        with self.assertRaisesRegex(ht.HandoffError,'HANDOFF_WORDPRESS_DOWNSTREAM_INVALID'): ht.validate_handoff(p)
    def test_negative_fake_direct_import_plugin_version(self):
        p=self.payload(); p['wordpress_review']['plugin_version_verified_against']='0.28.23'
        with self.assertRaisesRegex(ht.HandoffError,'HANDOFF_WORDPRESS_PLUGIN_VERSION_INVALID'): ht.validate_handoff(p)
    def test_negative_zero_article_count(self):
        p=self.payload(1); p['articles']=[]
        with self.assertRaisesRegex(ht.HandoffError,'HANDOFF_ARTICLE_COUNT_INVALID'): ht.validate_handoff(p)
    def test_negative_missing_inline_end_marker(self):
        with tempfile.TemporaryDirectory() as td:
            td=Path(td); p=td/'bad.txt'; p.write_text(ht.INLINE_BEGIN+'\n{}\n',encoding='utf-8')
            with self.assertRaisesRegex(ht.HandoffError,'INLINE_END_MISSING'): ht.inline_unpack(p,td/'out')

if __name__=='__main__': unittest.main(verbosity=2)
