from __future__ import annotations
import copy, hashlib, importlib.util, json, unittest
from pathlib import Path
from contextlib import contextmanager

HERE=Path(__file__).resolve().parent; REPO=HERE.parents[1]
STATE=REPO/'control/startmaster0107/runtime_inbox/RUNTIME_INBOX_STATE.json'
PACKAGE=REPO/'control/startmaster0107/runtime_inbox/generations/000001/PRODUCTION_PACKAGE.json'
SOURCE=REPO/'control/startmaster0107/runtime_inbox/generations/000001/SOURCE_SNAPSHOT.json'
CONTRACT=REPO/'control/startmaster0107/runtime_inbox/RUNTIME_BATCH_SLOT_CONTRACT_V1.json'
def mod(path,name):
    s=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
guard=mod(REPO/'control/startmaster0107/runtime_inbox/runtime_batch_slot_guard.py','pr221_guard')
action=mod(REPO/'control/single-door-boundary/codex_current_action.py','pr221_action')
handoff=mod(REPO/'control/startmaster0107/fachworkflow_proof_handoff.py','pr221_handoff')
def dump(p,o): p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

class DirectPackageBindingTest(unittest.TestCase):
    def setUp(self): self.state_bytes=STATE.read_bytes(); self.package_bytes=PACKAGE.read_bytes()
    def tearDown(self): STATE.write_bytes(self.state_bytes); PACKAGE.write_bytes(self.package_bytes)
    def package(self,version='production_plan_v5'):
        state=json.loads(self.state_bytes); source=json.loads(SOURCE.read_text(encoding='utf-8')); old=json.loads(self.package_bytes)
        metas=source['next_textmachine_metadata_batch']['items']; oldrels=old['workflow_release']['items']
        plans=[]; facts=[]; rels=[]
        for i,(meta,oldrel) in enumerate(zip(metas,oldrels)):
            sid=f'fresh-source-{i+1}'; cid=oldrel['canonical_article_id']
            pi={'canonical_article_id':cid,'source_snapshot_id':sid,'article_type':meta['article_type'],'target_keyword':meta['target_keyword'],'topic':meta['title'],'canonical_article':{'body_html':'test body'}}
            if version=='production_plan_v5': pi['category_binding']={'slug':meta['category']}
            else: pi['quality_binding']={'wordpress_category':{'slug':meta['category'],'taxonomy':'category'}}
            plans.append(pi); facts.append({'contract':'canonical_fact_pack_v1','source_snapshot_id':sid,'fact_pack_id':f'fp-{i+1}'})
            rels.append({'plan_slot':meta['plan_slot'],'canonical_article_id':cid,'source_snapshot_id':sid})
        bundle={'contract':'canonical_fact_pack_import_v1','fact_packs':facts}
        plan={'contract':version,'items':plans}
        bsha=guard.stable_hash(bundle); psha=guard.stable_hash(plan)
        release={'contract':'WORKFLOW_SUPERVISOR_RELEASE_V2_SIGNED','status':'PASS','exact_five_batch_sha256':state['batch_sha256'],'exact_five_item_count':len(rels),'items':rels,'production_plan_sha256':psha,'fact_pack_bundle_sha256':bsha,'content_generation_performed_by_supervisor':False,'wordpress_write_performed':False,'signature_algorithm':'ED25519','signature_b64':'test-signature'}
        rsha=guard.stable_hash(release)
        env={'contract':'PSERC_APPROVED_PRODUCTION_PACKAGE_V1','fact_pack_bundle_sha256':bsha,'production_plan_sha256':psha,'workflow_release_sha256':rsha,'package_id':guard.stable_hash({'contract':'PSERC_APPROVED_PRODUCTION_PACKAGE_V1','fact_pack_bundle_sha256':bsha,'production_plan_sha256':psha,'workflow_release_sha256':rsha}),'source':'FRESH_TEST_ONLY','fact_pack_bundle':bundle,'production_plan':plan,'workflow_release':release}
        env['package_payload_sha256']=guard.stable_hash(env)
        return env
    def install(self,env):
        dump(PACKAGE,env); st=json.loads(self.state_bytes); st['production_package_sha256']=sha(PACKAGE); dump(STATE,st)
    def current_item(self):
        c=action._runtime_context(); meta=dict(c['meta_items'][0]); rel=next(x for x in c['release_items'] if x['plan_slot']==meta['plan_slot'])
        return {'canonical_article_id':rel['canonical_article_id'],'plan_slot':meta['plan_slot'],'title':meta['title'],'target_keyword':meta['target_keyword'],'category':meta['category'],'article_type':meta['article_type']}
    def test_v4_v5_positive_and_slotless(self):
        for version in ('production_plan_v4','production_plan_v5'):
            self.install(self.package(version)); out=guard.validate(REPO,CONTRACT,STATE); self.assertEqual('RUNTIME_INPUTS_BOUND',out['status'])
            item=self.current_item(); bound=action._bound_expected(item); self.assertNotIn('plan_slot',bound['production_plan_item'])
            view=action.augment_current_action(REPO,{'allowed_output_root':'.pferde-quarantine/test/','item_receipt_schema':{}},item)
            pc=view['fachworkflow_handoff']['production_package_context']; self.assertEqual(bound['fact_pack'],pc['fact_pack']); self.assertEqual(bound['production_plan_item'],pc['production_plan_item'])
            ctx=handoff._runtime_context(REPO,action._runtime_context()['batch']); meta,rel,pi,fp=handoff._bound_item(ctx,item['canonical_article_id'],item['plan_slot'])
            req={'canonical_article_id':item['canonical_article_id'],'plan_slot':item['plan_slot'],'fact_pack':fp,'production_plan_item':pi,'production_plan_header':ctx['plan_header'],'workflow_release_item':rel,'workflow_release_metadata':ctx['release_metadata']}
            self.assertEqual(pi,handoff._validate_raw_context(req,ctx,meta,rel,pi,fp))
    def test_package_and_identity_negatives(self):
        env=self.package(); self.install(env); item=self.current_item()
        st=json.loads(STATE.read_text()); st['production_package_sha256']='0'*64; dump(STATE,st)
        with self.assertRaises(action.ViewError): action._runtime_context()
        self.install(env); st=json.loads(STATE.read_text()); st['generation']=2; dump(STATE,st)
        with self.assertRaises(action.ViewError): action._runtime_context()
        for mut in ('empty_plan','empty_facts','dup_plan','dup_fact','synthetic_slot','source_mismatch'):
            x=copy.deepcopy(env)
            if mut=='empty_plan': x['production_plan']['items']=[]
            elif mut=='empty_facts': x['fact_pack_bundle']['fact_packs']=[]
            elif mut=='dup_plan': x['production_plan']['items'].append(copy.deepcopy(x['production_plan']['items'][0]))
            elif mut=='dup_fact': x['fact_pack_bundle']['fact_packs'].append(copy.deepcopy(x['fact_pack_bundle']['fact_packs'][0]))
            elif mut=='synthetic_slot': x['production_plan']['items'][0]['plan_slot']=x['workflow_release']['items'][0]['plan_slot']
            elif mut=='source_mismatch': x['production_plan']['items'][0]['source_snapshot_id']='wrong-source'
            self.install(x)
            with self.assertRaises(action.ViewError): action._bound_expected(item)
        self.install(env); c=action._runtime_context(); meta=dict(c['meta_items'][0]); rel=dict(c['release_items'][0]); rel['canonical_article_id']='article:wrong'
        c['release_items'][0]=rel
        with self.assertRaises(handoff.Blocked): handoff._bound_item(c,item['canonical_article_id'],item['plan_slot'])
    def test_all_five_request_context_tamper_and_stage_proofs(self):
        self.install(self.package()); item=self.current_item(); ctx=handoff._runtime_context(REPO,action._runtime_context()['batch']); meta,rel,pi,fp=handoff._bound_item(ctx,item['canonical_article_id'],item['plan_slot'])
        base={'canonical_article_id':item['canonical_article_id'],'plan_slot':item['plan_slot'],'fact_pack':fp,'production_plan_item':pi,'production_plan_header':ctx['plan_header'],'workflow_release_item':rel,'workflow_release_metadata':ctx['release_metadata']}
        for field in ('fact_pack','production_plan_item','production_plan_header','workflow_release_item','workflow_release_metadata'):
            bad=copy.deepcopy(base); bad[field]=copy.deepcopy(bad[field]); bad[field]['tampered']=True
            with self.assertRaises(handoff.Blocked): handoff._validate_raw_context(bad,ctx,meta,rel,pi,fp)
        handoff._validate_worker_stage_proofs([])
        for bad in ([{'stage':'x'}],None,{}):
            with self.assertRaises(handoff.Blocked): handoff._validate_worker_stage_proofs(bad)
if __name__=='__main__': unittest.main()
