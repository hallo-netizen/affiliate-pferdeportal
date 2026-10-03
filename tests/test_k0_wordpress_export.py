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
    ident=i['items'][0]; body='<article><p>Test</p></article>'; sha=hashlib.sha256(body.encode()).hexdigest()
    p={'contract':'K0_ARTICLE_PACKAGE_V1','identity':ident,'html':body,'final_draft_sha256':sha,'revision_count':1,'production_context':{'fact_pack':{'contract':'canonical_fact_pack_v1'},'production_plan_item':{'article_type':'Beratung'}},'writer_provenance':{'contract':'K0_WRITER_SEAL_V1'},'publish_allowed':False}
    portal={'contract':'K0_PORTAL_ASSIGNMENT_V1','status':'PASS','items':[{'portal_id':'hobby','status':'AUTO_DETECTED','job_identity':ident}]}
    gate={'contract':'K0_PRODUCTION_GATES_V1','status':'PASS','body_sha256':sha,'semantic_intent_status':'PASS','anti_boilerplate_status':'PASS','writer_contract_status':'PASS','writer_policy_sha256':'writer-policy','ppm679_status':'PASS','ppm679_rule_count':104}
    lt={'status':'PASS','finding_count':0,'html_sha256':sha}
    return p,portal,gate,lt

class TestK0WordPressExport(unittest.TestCase):
    def test_exact_proven_k10_import_shape(self):
        i=intake(); p,portal,gate,lt=deps(i)
        with patch('engine.k0_wordpress_export.verify_writer_contract', return_value={'policy_sha256':'writer-policy','total_words':800,'conclusion_ratio':0.11}):
            out=w.build(i,p,portal,gate,lt,bindings(i))
        self.assertEqual(out['contract'],'PFERDE_ATELIER_WORDPRESS_IMPORT_V1')
        self.assertEqual(out['source'],'K0_CANONICAL_WORKFLOW')
        a=out['articles'][0]
        self.assertEqual(set(a),set(w.WORDPRESS_ARTICLE_FIELDS))
        self.assertEqual(a['article_id'],CANONICAL_ID)
        self.assertEqual(a['plan_slot'],PLAN_SLOT)
        self.assertEqual(a['slug'],'was-braucht-man-fuer-discgolf')
        self.assertNotIn('production_context',a)
        self.assertNotIn('final_draft_sha256',a)
        self.assertEqual(w.verify_export(out,i)['status'],'PASS')

    def test_missing_internal_canonical_binding_blocks_before_export(self):
        i=intake(); p,portal,gate,lt=deps(i)
        with patch('engine.k0_wordpress_export.verify_writer_contract', return_value={'policy_sha256':'writer-policy','total_words':800,'conclusion_ratio':0.11}):
            with self.assertRaisesRegex(w.Blocked,'K0_CANONICAL_ARTICLE_ID_INVALID'):
                w.build(i,p,portal,gate,lt,{'contract':'K10_CANONICAL_ARTICLE_BINDINGS_V1','status':'PASS','bindings':{}})

    def test_wrong_internal_canonical_binding_blocks_before_export(self):
        i=intake(); p,portal,gate,lt=deps(i)
        wrong='article:000000000000000000000000'
        with patch('engine.k0_wordpress_export.verify_writer_contract', return_value={'policy_sha256':'writer-policy','total_words':800,'conclusion_ratio':0.11}):
            with self.assertRaisesRegex(w.Blocked,'K0_CANONICAL_ARTICLE_ID_PLAN_SLOT_MISMATCH'):
                w.build(i,p,portal,gate,lt,{'contract':'K10_CANONICAL_ARTICLE_BINDINGS_V1','status':'PASS','bindings':{PLAN_SLOT:wrong}})

    def test_wordpress_article_id_must_bind_to_plan_slot(self):
        i=intake(); p,portal,gate,lt=deps(i)
        with patch('engine.k0_wordpress_export.verify_writer_contract', return_value={'policy_sha256':'writer-policy','total_words':800,'conclusion_ratio':0.11}):
            out=w.build(i,p,portal,gate,lt,bindings(i))
        out['articles'][0]['article_id']='article:000000000000000000000000'
        with self.assertRaisesRegex(w.Blocked,'CANONICAL_PLAN_SLOT_MISMATCH'):
            w.verify_export(out,i)

    def test_wordpress_article_id_format_blocks(self):
        i=intake(); p,portal,gate,lt=deps(i)
        with patch('engine.k0_wordpress_export.verify_writer_contract', return_value={'policy_sha256':'writer-policy','total_words':800,'conclusion_ratio':0.11}):
            out=w.build(i,p,portal,gate,lt,bindings(i))
        out['articles'][0]['article_id']=PLAN_SLOT
        with self.assertRaisesRegex(w.Blocked,'ARTICLE_ID_INVALID'):
            w.verify_export(out,i)

if __name__=='__main__':
    unittest.main()
