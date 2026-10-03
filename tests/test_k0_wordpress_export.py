import hashlib, json, unittest
from unittest.mock import patch
from engine import k0_wordpress_export as w

CANONICAL_ID='article:95b90bd71e79833075b607c1'
PLAN_SLOT=hashlib.sha256(('pserc-plan-slot-v2|'+CANONICAL_ID).encode()).hexdigest()

def stable(x):
    return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))

def intake():
    x={
      'contract':'PSERC_TEXTMACHINE_METADATA_BATCH_V2',
      'status':'READY_FOR_TEXTMACHINE_METADATA_INTAKE',
      'content_or_format_payload_present':False,
      'item_count':1,
      'items':[{
        'article_type':'Beratung','category':'discgolf-beratung',
        'plan_slot':PLAN_SLOT,
        'target_keyword':'Discgolf Ausrüstung','title':'Was braucht man für Discgolf?'
      }],
      'publish_allowed':False,
    }
    x['batch_sha256']=hashlib.sha256(stable(x).encode()).hexdigest()
    return x

def bindings(i):
    return {'contract':'K10_CANONICAL_ARTICLE_BINDINGS_V1','status':'PASS','bindings':{i['items'][0]['plan_slot']:CANONICAL_ID}}

def deps(i):
    ident=i['items'][0]; body='<article class="ppm-generated ppm-type-beratung" data-article-type="Beratung"><section data-block="intro"><p>Testinhalt mit ausreichender Struktur.</p></section><section data-block="conclusion"><h2>Fazit</h2><p>Abschluss.</p></section></article>'; sha=hashlib.sha256(body.encode()).hexdigest()
    p={'contract':'K0_ARTICLE_PACKAGE_V1','identity':ident,'html':body,'final_draft_sha256':sha,'revision_count':1,'production_context':{'fact_pack':{'contract':'canonical_fact_pack_v1','status':'SOURCE_VERIFIED_PRODUCTION_READY','sources':[],'claims':[]},'production_plan_item':{'article_type':'Beratung','target_keyword':ident['target_keyword'],'topic':ident['title'],'quality_binding':{'wordpress_category':{'slug':ident['category'],'taxonomy':'category'}}}},'writer_provenance':{'contract':'K0_WRITER_SEAL_V1'},'publish_allowed':False}
    portal={'contract':'K0_PORTAL_ASSIGNMENT_V1','status':'PASS','items':[{'portal_id':'hobby','status':'AUTO_DETECTED','job_identity':ident}]}
    gate={'contract':'K0_PRODUCTION_GATES_V1','status':'PASS','body_sha256':sha,'semantic_intent_status':'PASS','anti_boilerplate_status':'PASS','writer_contract_status':'PASS','writer_policy_sha256':'writer-policy','ppm679_status':'PASS','ppm679_rule_count':104}
    lt={'status':'PASS','finding_count':0,'html_sha256':sha}
    full_rules={'contract':'K0_FULL_RULE_FINAL_V1','status':'PASS','html_sha256':sha}
    category=[{'id':321,'slug':ident['category']}]
    return p,portal,gate,lt,full_rules,category

class TestK0WordPressExport(unittest.TestCase):
    def test_exact_proven_system4_shape(self):
        i=intake(); p,portal,gate,lt,full_rules,category=deps(i)
        with patch('engine.k0_wordpress_export.verify_writer_contract', return_value={'policy_sha256':'writer-policy','total_words':800,'conclusion_ratio':0.11}):
            out=w.build(i,p,portal,gate,lt,full_rules,bindings(i),category)
        self.assertEqual(out['contract'],'SYSTEM4_WORDPRESS_HANDOFF_V1')
        a=out['articles'][0]
        self.assertEqual(set(a),set(w.ARTICLE_FIELDS))
        self.assertEqual(a['article_id'],CANONICAL_ID)
        self.assertEqual(hashlib.sha256(('pserc-plan-slot-v2|'+a['article_id']).encode()).hexdigest(),a['plan_slot'])
        self.assertEqual(set(a['production_context']),{'fact_pack','production_plan_item'})
        pi=a['production_context']['production_plan_item']
        self.assertEqual(pi['canonical_article_id'],CANONICAL_ID)
        self.assertEqual(pi['canonical_article']['body_html'],a['body'])
        self.assertEqual(pi['canonical_article']['body_html_sha256'],a['final_draft_sha256'])
        self.assertEqual(pi['quality_binding']['wordpress_category'],{'id':321,'slug':'discgolf-beratung','taxonomy':'category'})
        self.assertEqual(w.verify_export(out,i)['status'],'PASS')

    def test_wrong_internal_canonical_binding_blocks(self):
        i=intake(); p,portal,gate,lt,category=deps(i)
        wrong='article:000000000000000000000000'
        with patch('engine.k0_wordpress_export.verify_writer_contract', return_value={'policy_sha256':'writer-policy','total_words':800,'conclusion_ratio':0.11}):
            with self.assertRaisesRegex(w.Blocked,'K0_CANONICAL_ARTICLE_ID_PLAN_SLOT_MISMATCH'):
                w.build(i,p,portal,gate,lt,full_rules,{'contract':'K10_CANONICAL_ARTICLE_BINDINGS_V1','status':'PASS','bindings':{PLAN_SLOT:wrong}},category)

    def test_missing_live_category_blocks(self):
        i=intake(); p,portal,gate,lt,category=deps(i)
        with patch('engine.k0_wordpress_export.verify_writer_contract', return_value={'policy_sha256':'writer-policy','total_words':800,'conclusion_ratio':0.11}):
            with self.assertRaisesRegex(w.Blocked,'K0_WORDPRESS_CATEGORY_ID_NOT_UNIQUE'):
                w.build(i,p,portal,gate,lt,full_rules,bindings(i),[])

    def test_nested_id_mismatch_blocks_verification(self):
        i=intake(); p,portal,gate,lt,category=deps(i)
        with patch('engine.k0_wordpress_export.verify_writer_contract', return_value={'policy_sha256':'writer-policy','total_words':800,'conclusion_ratio':0.11}):
            out=w.build(i,p,portal,gate,lt,bindings(i),category)
        out['articles'][0]['production_context']['production_plan_item']['canonical_article_id']='article:000000000000000000000000'
        with self.assertRaisesRegex(w.Blocked,'NESTED_CANONICAL_ID_MISMATCH'):
            w.verify_export(out,i)

if __name__=='__main__':
    unittest.main()
