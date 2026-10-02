import hashlib, json, unittest
from unittest.mock import patch
from engine import k0_wordpress_export as w

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
        'plan_slot':'5d3d43eebb1f755c178415b811fb1241a0ef022739ca7f7896a491792ca126e9',
        'target_keyword':'Discgolf Ausrüstung','title':'Was braucht man für Discgolf?'
      }],
      'publish_allowed':False,
    }
    x['batch_sha256']=hashlib.sha256(stable(x).encode()).hexdigest()
    return x

class TestK0WordPressExport(unittest.TestCase):
    def test_proven_02827_direct_shape(self):
        i=intake(); ident=i['items'][0]; body='<article><p>Test</p></article>'; sha=hashlib.sha256(body.encode()).hexdigest()
        p={'contract':'K0_ARTICLE_PACKAGE_V1','identity':ident,'html':body,'final_draft_sha256':sha,'revision_count':1,'production_context':{'fact_pack':{'contract':'canonical_fact_pack_v1'},'production_plan_item':{'article_type':'Beratung'}},'publish_allowed':False}
        portal={'contract':'K0_PORTAL_ASSIGNMENT_V1','status':'PASS','items':[{'portal_id':'hobby','status':'AUTO_DETECTED','job_identity':ident}]}
        gate={'contract':'K0_PRODUCTION_GATES_V1','status':'PASS','body_sha256':sha,'semantic_intent_status':'PASS','anti_boilerplate_status':'PASS','writer_contract_status':'PASS','writer_policy_sha256':'writer-policy','ppm679_status':'PASS','ppm679_rule_count':104}
        lt={'status':'PASS','finding_count':0,'html_sha256':sha}
        with patch('engine.k0_wordpress_export.verify_writer_contract', return_value={'policy_sha256':'writer-policy','total_words':800,'conclusion_ratio':0.11}):
            out=w.build(i,p,portal,gate,lt)
        self.assertEqual(out['contract'],'SYSTEM4_WORDPRESS_HANDOFF_V1')
        self.assertEqual(out['wordpress_review']['plugin_version_verified_against'],'0.28.27')
        self.assertTrue(out['wordpress_review']['direct_wordpress_upload_ready'])
        self.assertEqual(set(out['articles'][0]),{'index','title','target_keyword','category','article_type','plan_slot','final_draft_sha256','revision_count','body','production_context','languagetool','ppm679'})
        self.assertEqual(w.verify_export(out,i)['status'],'PASS')

    def test_lt_failure_blocks(self):
        i=intake(); ident=i['items'][0]; body='<article><p>Test</p></article>'; sha=hashlib.sha256(body.encode()).hexdigest()
        p={'contract':'K0_ARTICLE_PACKAGE_V1','identity':ident,'html':body,'final_draft_sha256':sha,'production_context':{'fact_pack':{},'production_plan_item':{}},'publish_allowed':False}
        portal={'contract':'K0_PORTAL_ASSIGNMENT_V1','status':'PASS','items':[{'portal_id':'hobby','status':'AUTO_DETECTED','job_identity':ident}]}
        gate={'contract':'K0_PRODUCTION_GATES_V1','status':'PASS','body_sha256':sha,'ppm679_status':'PASS','ppm679_rule_count':104}
        gate['semantic_intent_status']='PASS'; gate['anti_boilerplate_status']='PASS'; gate['writer_contract_status']='PASS'; gate['writer_policy_sha256']='writer-policy'
        with patch('engine.k0_wordpress_export.verify_writer_contract', return_value={'policy_sha256':'writer-policy','total_words':800,'conclusion_ratio':0.11}):
            with self.assertRaises(w.Blocked):
                w.build(i,p,portal,gate,{'status':'REPAIR_REQUIRED','finding_count':1,'html_sha256':sha})

if __name__=='__main__':
    unittest.main()
