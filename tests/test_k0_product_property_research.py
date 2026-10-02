import hashlib
import json
import unittest

from engine.k0_product_property_research import ARTICLE_TYPE, SEARCH_INTENT, Blocked, bind_store, validate_packet
from engine.k0_writer_station import prepare, Blocked as WriterBlocked

def stable(x):
    return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))

def identity(article_type=ARTICLE_TYPE):
    return {
        'article_type':article_type,
        'category':'schermaschinen-eigenschaftssieger',
        'plan_slot':'1'*64,
        'target_keyword':'leiseste Schermaschine für Pferde',
        'title':'Was ist die leiseste Schermaschine für Pferde?'
    }

def intake():
    x={
        'contract':'PSERC_TEXTMACHINE_METADATA_BATCH_V2',
        'status':'READY_FOR_TEXTMACHINE_METADATA_INTAKE',
        'content_or_format_payload_present':False,
        'item_count':1,
        'items':[identity()],
        'publish_allowed':False,
    }
    x['batch_sha256']=hashlib.sha256(stable(x).encode()).hexdigest()
    return x

def portal(i):
    ident=i['items'][0]
    return {
        'contract':'K0_PORTAL_ASSIGNMENT_V1','status':'PASS','source_batch_sha256':i['batch_sha256'],
        'item_count':1,'items':[{'portal_id':'pferdeatelier','portal_name':'Pferdeatelier','status':'AUTO_DETECTED','basis':'category:'+ident['category'],'job_identity':ident}],
        'publish_allowed':False
    }

def packet():
    rows=[
        ('acme:quiet-1','Acme','Quiet 1',55.0,'https://example.test/q1'),
        ('acme:quiet-2','Acme','Quiet 2',58.0,'https://example.test/q2'),
        ('clip:horse-a','Clip','Horse A',61.0,'https://example.test/a'),
        ('clip:horse-b','Clip','Horse B',64.0,'https://example.test/b'),
    ]
    return {
        'contract':'K0_PRODUCT_PROPERTY_RESEARCH_V1','status':'PASS',
        'ranking_independent_of_affiliate':True,
        'property':{'key':'noise_db','label':'Lautstärke','unit':'dB','direction':'MIN'},
        'candidates':[{'product_key':k,'brand':b,'model':m,'value':v,'source_title':'Herstellerdaten','source_url':u,'identifiers':{'mpn':k.split(':')[1]}} for k,b,m,v,u in rows],
        'winner':{'product_key':'acme:quiet-1','value':55.0,'source_url':'https://example.test/q1'}
    }

def context(with_research=True):
    ident=identity()
    pc={'fact_pack':{'contract':'canonical_fact_pack_v1'},'production_plan_item':{'article_type':ARTICLE_TYPE}}
    if with_research: pc['property_research']=packet()
    return {
        'contract':'K0_AUTHORING_CONTEXT_V1','run_instance_id':'run:1234567890abcdef12345678',
        'identity':ident,'content_profile':{'search_intent':SEARCH_INTENT},
        'production_context':pc,'publish_allowed':False
    }

class PropertyResearchTests(unittest.TestCase):
    def test_positive_numeric_property_winner_and_store(self):
        result=validate_packet(identity(),packet())
        self.assertEqual(result['status'],'PASS')
        self.assertEqual(result['winner']['model'],'Quiet 1')
        store={'contract':'K0_PRODUCT_PROPERTY_STORE_V1','status':'ACTIVE','products':{},'publish_allowed':False}
        out,receipt=bind_store(context(),store)
        self.assertEqual(receipt['store_status'],'UPDATED')
        self.assertEqual(out['products']['acme:quiet-1']['properties']['noise_db']['value'],55.0)

    def test_wrong_winner_is_blocked(self):
        p=packet(); p['winner']={'product_key':'clip:horse-b','value':64.0,'source_url':'https://example.test/b'}
        with self.assertRaisesRegex(Blocked,'WINNER_VALUE_MISMATCH'):
            validate_packet(identity(),p)

    def test_affiliate_may_not_determine_winner(self):
        p=packet(); p['ranking_independent_of_affiliate']=False
        with self.assertRaisesRegex(Blocked,'AFFILIATE_INDEPENDENCE_REQUIRED'):
            validate_packet(identity(),p)

    def test_writer_job_cannot_start_without_property_research(self):
        i=intake()
        with self.assertRaisesRegex(WriterBlocked,'PROPERTY_RESEARCH'):
            prepare(i,portal(i),context(with_research=False))

if __name__=='__main__':
    unittest.main()
