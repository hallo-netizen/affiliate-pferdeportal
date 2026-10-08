import copy, hashlib, json, unittest
from pathlib import Path
from engine.k0_portal_resolver import resolve, Blocked

def stable(x):
    return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))

def intake(category='discgolf-beratung'):
    x={
      'contract':'PSERC_TEXTMACHINE_METADATA_BATCH_V2',
      'status':'READY_FOR_TEXTMACHINE_METADATA_INTAKE',
      'content_or_format_payload_present':False,
      'item_count':1,
      'items':[{
        'article_type':'Beratung',
        'category':category,
        'plan_slot':'5d3d43eebb1f755c178415b811fb1241a0ef022739ca7f7896a491792ca126e9',
        'target_keyword':'Discgolf Ausrüstung',
        'title':'Was braucht man für Discgolf?'
      }],
      'publish_allowed':False
    }
    x['batch_sha256']=hashlib.sha256(stable(x).encode()).hexdigest()
    return x

REG={
 'contract':'K0_PORTAL_REGISTRY_V1',
 'profiles':[{'portal_id':'hobby','display_name':'Hobby','category_exact':['discgolf-beratung'],'category_prefixes':[]}]
}

class K0PortalResolverTest(unittest.TestCase):
    def test_hobby_auto_detected_without_portal_field(self):
        x=intake()
        self.assertNotIn('portal',x['items'][0])
        r=resolve(x,REG)
        self.assertEqual(r['status'],'PASS')
        self.assertEqual(r['items'][0]['portal_id'],'hobby')
        self.assertEqual(r['items'][0]['status'],'AUTO_DETECTED')


    def test_current_17_item_batch_resolves_to_pferdeatelier(self):
        categories=[
          'mash-faq','schermaschinen-faq','schabracken-faq','sattelgurte-faq',
          'sattelgurte-faq','schubkarren-faq','schabracken-faq','mueslis-fuer-pferde-faq',
          'reitplatzboden-faq','traenken-und-wasser-frostsichere-pferdetraenken-faq',
          'longierpeitschen-faq','schermaschinen-faq','schubkarren-faq','striegel-faq',
          'schubkarren-faq','schubkarren-faq','schabracken-faq'
        ]
        rows=[]
        for idx,category in enumerate(categories):
            rows.append({
              'article_type':'FAQ',
              'category':category,
              'plan_slot':hashlib.sha256(f'slot-{idx}'.encode()).hexdigest(),
              'target_keyword':f'Keyword {idx}',
              'title':f'Titel {idx}?'
            })
        x={
          'contract':'PSERC_TEXTMACHINE_METADATA_BATCH_V2',
          'status':'READY_FOR_TEXTMACHINE_METADATA_INTAKE',
          'content_or_format_payload_present':False,
          'item_count':len(rows),
          'items':rows,
          'publish_allowed':False
        }
        x['batch_sha256']=hashlib.sha256(stable(x).encode()).hexdigest()
        reg=json.loads(Path('K0_PORTAL_REGISTRY.json').read_text(encoding='utf-8'))
        r=resolve(x,reg)
        self.assertEqual(r['status'],'PASS')
        self.assertEqual(r['item_count'],17)
        self.assertTrue(all(row['portal_id']=='pferdeatelier' for row in r['items']))
        self.assertTrue(all(row['status']=='AUTO_DETECTED' for row in r['items']))

    def test_unknown_category_blocks(self):
        with self.assertRaises(Blocked):
            resolve(intake('unbekannt-beratung'),REG)

    def test_ambiguous_category_blocks(self):
        reg=copy.deepcopy(REG)
        reg['profiles'].append({'portal_id':'other','display_name':'Other','category_exact':['discgolf-beratung'],'category_prefixes':[]})
        with self.assertRaises(Blocked):
            resolve(intake(),reg)

    def test_portal_field_is_rejected_by_exact_five_field_gate(self):
        x=intake(); x['items'][0]['portal']='Hobby'
        core=dict(x); core.pop('batch_sha256')
        x['batch_sha256']=hashlib.sha256(stable(core).encode()).hexdigest()
        with self.assertRaises(Blocked):
            resolve(x,REG)

if __name__=='__main__':
    unittest.main()
