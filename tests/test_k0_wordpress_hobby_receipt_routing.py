import copy,hashlib,json,unittest
from pathlib import Path
from engine.k0_portal_resolver import resolve,Blocked

def sha(x):
    return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def make(site='www.hobby-depot.de',category='3d-bogenschiessen-regeln'):
    order='TXE-'+'d'*32
    aid='article:'+hashlib.sha256(('texterstellung-k0-v1|'+site+'|'+order).encode()).hexdigest()[:24]
    slot=hashlib.sha256(('pserc-plan-slot-v2|'+aid).encode()).hexdigest()
    row={'article_type':'FAQ','category':category,'plan_slot':slot,
         'target_keyword':'3D-Bogenschießen Regeln','title':'Welche Regeln gelten beim 3D-Bogenschießen?'}
    batch={'contract':'PSERC_TEXTMACHINE_METADATA_BATCH_V2',
           'status':'READY_FOR_TEXTMACHINE_METADATA_INTAKE',
           'content_or_format_payload_present':False,'item_count':1,'items':[row],'publish_allowed':False}
    batch['batch_sha256']=sha(batch)
    receipt={'contract':'WP_K0_SOURCE_RECEIPT_V1','source':'CENTRAL_WORDPRESS_ORDER_REGISTRY',
        'site_host':site,'publish_allowed':False,'next_textmachine_metadata_batch':batch,
        'items':[{'metadata_binding':row,'order_id':order,'article_id':aid,
                  'search_intent':'INFORMATIONAL_DIRECT_QUESTION'}]}
    receipt['manifest_sha256']=sha(receipt)
    return batch,receipt

class SourceHostRouting(unittest.TestCase):
    def setUp(self):
        self.registry=json.loads(Path('K0_PORTAL_REGISTRY.json').read_text())
    def test_hobby_wordpress_receipt_assigns_non_discgolf_category(self):
        batch,receipt=make()
        result=resolve(batch,self.registry,receipt)
        self.assertEqual(result['status'],'PASS')
        self.assertEqual(result['items'][0]['portal_id'],'hobby')
        self.assertTrue(result['items'][0]['basis'].startswith('verified_wp_source_host:'))
        self.assertEqual(result['items'][0]['job_identity'],batch['items'][0])
    def test_horse_wordpress_receipt_keeps_working(self):
        batch,receipt=make('pferde-atelier.de','sattelgurte-faq')
        self.assertEqual(resolve(batch,self.registry,receipt)['items'][0]['portal_id'],'pferdeatelier')
    def test_unknown_host_blocked(self):
        batch,receipt=make('unknown.example')
        with self.assertRaisesRegex(Blocked,'WP_SOURCE_PORTAL_HOST_NOT_UNIQUE'):
            resolve(batch,self.registry,receipt)
    def test_receipt_identity_tamper_blocked(self):
        batch,receipt=make()
        receipt['items'][0]['article_id']='article:'+'a'*24
        with self.assertRaisesRegex(Blocked,'WP_SOURCE_RECEIPT_INVALID'):
            resolve(batch,self.registry,receipt)
    def test_batch_drift_blocked(self):
        batch,receipt=make()
        batch['items'][0]['title']='Geänderter Titel'
        batch['batch_sha256']=sha({k:v for k,v in batch.items() if k!='batch_sha256'})
        with self.assertRaisesRegex(Blocked,'WP_SOURCE_RECEIPT_INVALID'):
            resolve(batch,self.registry,receipt)
    def test_legacy_discgolf_without_receipt_still_works(self):
        batch,receipt=make(category='discgolf-beratung')
        self.assertEqual(resolve(batch,self.registry)['items'][0]['portal_id'],'hobby')

if __name__=='__main__':
    unittest.main()
