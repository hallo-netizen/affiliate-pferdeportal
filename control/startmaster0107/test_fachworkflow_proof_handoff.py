from __future__ import annotations
import copy, importlib.util, re, unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent; REPO=HERE.parents[1]
def mod(path,name):
    s=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
action=mod(REPO/"control/single-door-boundary/codex_current_action.py","simple_entry_action_test")
handoff=mod(HERE/"fachworkflow_proof_handoff.py","simple_entry_handoff_test")
class SimpleEntryAggregateTest(unittest.TestCase):
    def item(self,c):
        meta=next(dict(x) for x in c["meta_items"] if isinstance(x,dict) and x.get("plan_slot")); rel=next(dict(x) for x in c["release_items"] if x.get("plan_slot")==meta["plan_slot"]); return meta,rel,{"canonical_article_id":rel["canonical_article_id"],"plan_slot":meta["plan_slot"],"title":meta["title"],"target_keyword":meta["target_keyword"],"category":meta["category"],"article_type":meta["article_type"]}
    def test_real_empty_generation_one_reaches_current_action(self):
        c=action._runtime_context(); self.assertEqual([],c["plan_items"]); self.assertEqual([],c["fact_packs"]); meta,rel,item=self.item(c); action._bound_expected(item); out=action.augment_current_action(REPO,{"allowed_output_root":".pferde-quarantine/test/","item_receipt_schema":{}},item); raw=out["fachworkflow_handoff"]["raw_context_binding"]; self.assertEqual(c["source_sha256"],raw["source_snapshot_id"]); self.assertNotIn("production_plan_header",raw); self.assertEqual(["fact_pack","production_plan_item","production_plan_header"],out["fachworkflow_handoff"]["worker_generated_raw_fields"])
    def test_current_item_identity_negatives(self):
        c=action._runtime_context(); meta,rel,item=self.item(c)
        for key,val in (("plan_slot","0"*64),("canonical_article_id","article:wrong"),("title","wrong"),("target_keyword","wrong"),("category","wrong"),("article_type","wrong")):
            bad=dict(item); bad[key]=val
            with self.assertRaises(action.ViewError): action._bound_expected(bad)
    def test_worker_raw_context_positive_and_negatives(self):
        c=action._runtime_context(); meta,rel,item0=self.item(c); ctx=handoff._runtime_context(REPO,c["batch"]); source=ctx["source_sha256"]; plan={"canonical_article_id":rel["canonical_article_id"],"source_snapshot_id":source,"article_type":meta["article_type"],"target_keyword":meta["target_keyword"],"topic":meta["title"],"quality_binding":{"wordpress_category":{"name":meta["category"],"slug":meta["category"],"taxonomy":"category"}},"canonical_article":{"body_html":"test"}}; fact={"contract":"canonical_fact_pack_v1","source_snapshot_id":source,"fact_pack_id":"test"}; header={"contract":"production_plan_v4","current_fachworkflow":True}; req={"batch_sha256":c["batch"],"canonical_article_id":rel["canonical_article_id"],"plan_slot":meta["plan_slot"],"fact_pack":fact,"production_plan_item":plan,"production_plan_header":header,"workflow_release_item":rel,"workflow_release_metadata":ctx["release_metadata"]}; self.assertEqual(plan,handoff._validate_raw_context(req,ctx,meta,rel))
        for field in ("fact_pack","production_plan_item"):
            bad=copy.deepcopy(req); bad[field]["source_snapshot_id"]="0"*64
            with self.assertRaises(handoff.Blocked): handoff._validate_raw_context(bad,ctx,meta,rel)
        bad=copy.deepcopy(req); bad["production_plan_item"]["plan_slot"]=meta["plan_slot"]
        with self.assertRaises(handoff.Blocked): handoff._validate_raw_context(bad,ctx,meta,rel)
        bad=copy.deepcopy(req); bad["plan_slot"]="0"*64
        with self.assertRaises(handoff.Blocked): handoff._validate_raw_context(bad,ctx,meta,rel)
        for field in ("workflow_release_item","workflow_release_metadata"):
            bad=copy.deepcopy(req); bad[field]["tampered"]=True
            with self.assertRaises(handoff.Blocked): handoff._validate_raw_context(bad,ctx,meta,rel)
        for bad_header in (ctx["plan_header"],None,{}, {"contract":"production_plan_v5"}, {"contract":"production_plan_v4","items":[]}):
            bad=copy.deepcopy(req); bad["production_plan_header"]=bad_header
            with self.assertRaises(handoff.Blocked): handoff._validate_raw_context(bad,ctx,meta,rel)
        for bad in ([{"stage":"fake"}],None,{}):
            with self.assertRaises(handoff.Blocked): handoff._validate_worker_stage_proofs(bad)
if __name__=="__main__": unittest.main()
