import copy, hashlib, json, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'concept_agent'))
import intake_bridge as b

def stable(v):
    return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def item(i):
    return {
        'title':f'Testtitel {i}',
        'target_keyword':f'Testkeyword {i}',
        'category':'test-beratung',
        'article_type':'Beratung',
        'plan_slot':hashlib.sha256(f'slot-{i}'.encode()).hexdigest(),
    }

def snapshot(n):
    batch={
        'contract':b.BATCH_CONTRACT,'status':b.READY_STATUS,'item_count':n,
        'maximum_articles':0,'maximum_articles_per_type':0,'publish_allowed':False,
        'content_or_format_payload_present':False,'items':[item(i) for i in range(n)]
    }
    batch['batch_sha256']=stable(batch)
    return {
        'contract':b.SNAPSHOT_CONTRACT,
        'hard_rules':{
            'approved_research_text_process_required':True,
            'text_machine_is_only_content_and_format_authority':True,
            'metadata_handoff_exact_scalar_fields':list(b.EXACT_FIELDS),
        },
        'next_step':b.NEXT_STEP,
        'next_textmachine_metadata_batch':batch,
    }

def research(req):
    rows=[]
    for row in req['items']:
        evidence=f'Gebundene Testevidenz für Artikel {row["item_index"]}; ausreichend lang und eindeutig.'
        rows.append({'item_index':row['item_index'],'plan_slot':row['plan_slot'],'sources':[{
            'source_id':f'src-{row["item_index"]}','source_title':'Lokale Testquelle',
            'source_url':f'https://example.test/{row["item_index"]}','evidence':evidence,
            'snapshot_sha256':hashlib.sha256(evidence.encode()).hexdigest(),
        }]})
    return {'contract':b.RESEARCH_SUBMISSION_CONTRACT,'batch_sha256':req['batch_sha256'],'item_count':req['item_count'],'items':rows}

class IntakeTests(unittest.TestCase):
    def test_positive_one_article(self):
        req=b.prepare(snapshot(1)); self.assertEqual(req['item_count'],1)
        self.assertFalse(req['research']['legacy_system4_source_requests_required'])
        bound=b.bind_research(req,research(req)); self.assertTrue(bound['draft_allowed'])

    def test_positive_three_articles(self):
        req=b.prepare(snapshot(3)); self.assertEqual([r['item_index'] for r in req['items']],[0,1,2])
        bound=b.bind_research(req,research(req)); self.assertEqual(bound['item_count'],3)
        self.assertEqual(len({r['source_pool_sha256'] for r in bound['items']}),3)

    def test_negative_extra_sixth_metadata_field(self):
        s=snapshot(1); s['next_textmachine_metadata_batch']['items'][0]['body_html']='<p>x</p>'
        core=dict(s['next_textmachine_metadata_batch']); core.pop('batch_sha256',None); s['next_textmachine_metadata_batch']['batch_sha256']=stable(core)
        with self.assertRaisesRegex(b.Blocked,'EXACT_FIVE_FIELDS_REQUIRED'): b.prepare(s)

    def test_negative_batch_tamper(self):
        s=snapshot(1); s['next_textmachine_metadata_batch']['items'][0]['title']='manipuliert'
        with self.assertRaisesRegex(b.Blocked,'BATCH_SHA_MISMATCH'): b.prepare(s)

    def test_negative_research_wrong_batch(self):
        req=b.prepare(snapshot(1)); r=research(req); r['batch_sha256']='0'*64
        with self.assertRaisesRegex(b.Blocked,'RESEARCH_BATCH_MISMATCH'): b.bind_research(req,r)

    def test_negative_research_wrong_slot(self):
        req=b.prepare(snapshot(1)); r=research(req); r['items'][0]['plan_slot']='f'*64
        with self.assertRaisesRegex(b.Blocked,'RESEARCH_ITEM_BINDING_MISMATCH'): b.bind_research(req,r)

    def test_negative_evidence_mutation(self):
        req=b.prepare(snapshot(1)); r=research(req); r['items'][0]['sources'][0]['evidence']+=' MUTATION'
        with self.assertRaisesRegex(b.Blocked,'RESEARCH_EVIDENCE_HASH_MISMATCH'): b.bind_research(req,r)

if __name__=='__main__': unittest.main(verbosity=2)
