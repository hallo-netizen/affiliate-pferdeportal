import hashlib, json, unittest
from unittest.mock import patch
from engine import k0_wordpress_export as w

ARTICLE_ID='article:95b90bd71e79833075b607c1'
PLAN_SLOT=hashlib.sha256(('pserc-plan-slot-v2|'+ARTICLE_ID).encode()).hexdigest()

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
    return {'contract':'K10_CANONICAL_ARTICLE_BINDINGS_V1','status':'PASS','bindings':{i['items'][0]['plan_slot']:ARTICLE_ID}}

class TestK0WordPressExport(unittest.TestCase):
    def test_02830_direct_shape_requires_article_id(self):
        i=intake(); ident=i['items'][0]; body='<article><p>Test</p></article>'; sha=hashlib.sha256(body.encode()).hexdigest()
        p={'contract':'K0_ARTICLE_PACKAGE_V1','identity':ident,'html':body,'final_draft_sha256':sha,'revision_count':1,'production_context':{'fact_pack':{'contract':'canonical_fact_pack_v1'},'production_plan_item':{'article_type':'Beratung'}},'writer_provenance':{'contract':'K0_WRITER_SEAL_V1'},'publish_allowed':False}
        portal={'contract':'K0_PORTAL_ASSIGNMENT_V1','status':'PASS','items':[{'portal_id':'hobby','status':'AUTO_DETECTED','job_identity':ident}]}
        gate={'contract':'K0_PRODUCTION_GATES_V1','status':'PASS','body_sha256':sha,'semantic_intent_status':'PASS','anti_boilerplate_status':'PASS','writer_contract_status':'PASS','writer_policy_sha256':'writer-policy','ppm679_status':'PASS','ppm679_rule_count':104}
        lt={'status':'PASS','finding_count':0,'html_sha256':sha}
        with patch('engine.k0_wordpress_export.verify_writer_contract', return_value={'policy_sha256':'writer-policy','total_words':800,'conclusion_ratio':0.11}):
            out=w.build(i,p,portal,gate,lt,bindings(i))
        self.assertEqual(out['contract'],'SYSTEM4_WORDPRESS_HANDOFF_V1')
        self.assertEqual(out['wordpress_review']['plugin_version_verified_against'],'0.28.30')
        self.assertEqual(out['wordpress_review']['plugin_build_verified_against'],'0.28.30-pste-v5-binding-safe')
        self.assertTrue(out['wordpress_review']['direct_wordpress_upload_ready'])
        self.assertEqual(out['articles'][0]['article_id'],ARTICLE_ID)
        self.assertEqual(hashlib.sha256(('pserc-plan-slot-v2|'+ARTICLE_ID).encode()).hexdigest(),out['articles'][0]['plan_slot'])
        self.assertEqual(w.verify_export(out,i)['status'],'PASS')

    def test_missing_canonical_article_id_blocks(self):
        i=intake(); ident=i['items'][0]; body='<article><p>Test</p></article>'; sha=hashlib.sha256(body.encode()).hexdigest()
        p={'contract':'K0_ARTICLE_PACKAGE_V1','identity':ident,'html':body,'final_draft_sha256':sha,'revision_count':1,'production_context':{'fact_pack':{},'production_plan_item':{}},'publish_allowed':False}
        portal={'contract':'K0_PORTAL_ASSIGNMENT_V1','status':'PASS','items':[{'portal_id':'hobby','status':'AUTO_DETECTED','job_identity':ident}]}
        gate={'contract':'K0_PRODUCTION_GATES_V1','status':'PASS','body_sha256':sha,'semantic_intent_status':'PASS','anti_boilerplate_status':'PASS','writer_contract_status':'PASS','writer_policy_sha256':'writer-policy','ppm679_status':'PASS','ppm679_rule_count':104}
        lt={'status':'PASS','finding_count':0,'html_sha256':sha}
        with patch('engine.k0_wordpress_export.verify_writer_contract', return_value={'policy_sha256':'writer-policy','total_words':800,'conclusion_ratio':0.11}):
            with self.assertRaisesRegex(w.Blocked,'K0_CANONICAL_ARTICLE_ID_INVALID'):
                w.build(i,p,portal,gate,lt,{'contract':'K10_CANONICAL_ARTICLE_BINDINGS_V1','status':'PASS','bindings':{}})

    def test_wrong_article_id_slot_binding_blocks(self):
        i=intake(); ident=i['items'][0]; body='<article><p>Test</p></article>'; sha=hashlib.sha256(body.encode()).hexdigest()
        p={'contract':'K0_ARTICLE_PACKAGE_V1','identity':ident,'html':body,'final_draft_sha256':sha,'revision_count':1,'production_context':{'fact_pack':{},'production_plan_item':{}},'publish_allowed':False}
        portal={'contract':'K0_PORTAL_ASSIGNMENT_V1','status':'PASS','items':[{'portal_id':'hobby','status':'AUTO_DETECTED','job_identity':ident}]}
        gate={'contract':'K0_PRODUCTION_GATES_V1','status':'PASS','body_sha256':sha,'semantic_intent_status':'PASS','anti_boilerplate_status':'PASS','writer_contract_status':'PASS','writer_policy_sha256':'writer-policy','ppm679_status':'PASS','ppm679_rule_count':104}
        lt={'status':'PASS','finding_count':0,'html_sha256':sha}
        wrong='article:000000000000000000000000'
        with patch('engine.k0_wordpress_export.verify_writer_contract', return_value={'policy_sha256':'writer-policy','total_words':800,'conclusion_ratio':0.11}):
            with self.assertRaisesRegex(w.Blocked,'K0_CANONICAL_ARTICLE_ID_PLAN_SLOT_MISMATCH'):
                w.build(i,p,portal,gate,lt,{'contract':'K10_CANONICAL_ARTICLE_BINDINGS_V1','status':'PASS','bindings':{ident['plan_slot']:wrong}})

if __name__=='__main__':
    unittest.main()
