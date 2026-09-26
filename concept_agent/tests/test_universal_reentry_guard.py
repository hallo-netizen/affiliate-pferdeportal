import base64, hashlib, json, sys, unittest
from pathlib import Path

HERE=Path(__file__).resolve().parents[1]
if str(HERE) not in sys.path:
    sys.path.insert(0,str(HERE))

import progress_guard
import universal_reentry_guard as guard

class UniversalReentryGuardTests(unittest.TestCase):
    def setUp(self):
        self.slot=hashlib.sha256(b"slot0").hexdigest()
        self.identity={
            "item_index":0,"title":"T","target_keyword":"K","category":"C",
            "article_type":"Beratung","plan_slot":self.slot,
            "identity_sha256":hashlib.sha256(b"id").hexdigest(),
        }
        self.binding={
            "contract":progress_guard.BINDING_CONTRACT,
            "status":"AUTHORING_READY",
            "batch_sha256":hashlib.sha256(b"batch").hexdigest(),
            "item_count":1,
            "source_intake_sha256":hashlib.sha256(b"intake").hexdigest(),
            "source_research_binding_sha256":hashlib.sha256(b"research-bound").hexdigest(),
            "items":[{
                "item_index":0,
                "identity":self.identity,
                "research_bound":{
                    "item_index":0,
                    "plan_slot":self.slot,
                    "source_pool_sha256":hashlib.sha256(b"sources").hexdigest(),
                },
            }],
            "publish_allowed":False,
        }
        self.binding["binding_sha256"]=progress_guard.stable(self.binding)

    def outer(self,phase):
        state={
            "contract":progress_guard.CHECKPOINT_CONTRACT,
            "batch_sha256":self.binding["batch_sha256"],
            "production_binding_sha256":self.binding["binding_sha256"],
            "item_count":1,"status":"IN_PROGRESS","phase":phase,
            "next_item_index":0,"completed_items":[],"current_item":None,
            "previous_checkpoint_sha256":None,"drafts":[],"publish_allowed":False,
        }
        if phase in {"LT68_REQUIRED","PPM679_REQUIRED","REPAIR_REQUIRED"}:
            d=hashlib.sha256(b"draft").hexdigest()
            state["drafts"]=[{"item_index":0,"plan_slot":self.slot,"filename":f"00_{self.slot}.md","draft_sha256":d,"size_bytes":5,"content_utf8":"draft","revision":1,"lt68":"PENDING","ppm679":"PENDING"}]
            state["current_item"]={"item_index":0,"draft_sha256":d}
            if phase=="REPAIR_REQUIRED":
                state["current_item"].update({"checker":"LT68","finding_sha256":hashlib.sha256(b"finding").hexdigest()})
        if phase in {"ALL_ARTICLES_LT_PPM_PASS","PSERC_PASS_ENDSTEMPEL_REQUIRED","ENDSTEMPEL_PASS_STOP"}:
            d=hashlib.sha256(b"draft").hexdigest()
            state["drafts"]=[{
                "item_index":0,"plan_slot":self.slot,"filename":f"00_{self.slot}.md",
                "draft_sha256":d,"size_bytes":5,"content_utf8":"draft","revision":1,
                "lt68":"PASS","ppm679":"PASS",
            }]
            state["completed_items"]=[{
                "item_index":0,"plan_slot":self.slot,"draft_sha256":d,"revision":1,
                "lt68":"PASS","ppm679":"PASS",
            }]
            state["next_item_index"]=1
            state["status"]="PASS" if phase!="PSERC_PASS_ENDSTEMPEL_REQUIRED" else "IN_PROGRESS"
            if phase in {"PSERC_PASS_ENDSTEMPEL_REQUIRED","ENDSTEMPEL_PASS_STOP"}:
                state["pserc_package_sha256"]=hashlib.sha256(b"pserc").hexdigest()
            if phase=="ENDSTEMPEL_PASS_STOP":
                state["endstempel_final_file_sha256"]=hashlib.sha256(b"final").hexdigest()
        state["allowed_action"]=progress_guard.expected_action(self.binding,state)
        state["checkpoint_sha256"]=progress_guard.stable(state)
        return state

    def canonical_state(self,phase):
        research=facts=context=authoring=draft=last=release=None
        checks={}
        revision=0
        released=False
        if phase in {"FACT_CHECK_REQUIRED","CONTEXT_REQUIRED","DRAFT_REQUIRED","CHECK_REQUIRED","REPAIR_REQUIRED","OUTPUT_GATE_REQUIRED","SIGNATURE_REQUIRED","RELEASED"}:
            research={"text":"research","sha256":hashlib.sha256(b"research").hexdigest()}
        if phase in {"CONTEXT_REQUIRED","DRAFT_REQUIRED","CHECK_REQUIRED","REPAIR_REQUIRED","OUTPUT_GATE_REQUIRED","SIGNATURE_REQUIRED","RELEASED"}:
            facts={"text":"facts","sha256":hashlib.sha256(b"facts").hexdigest()}
        if phase in {"DRAFT_REQUIRED","CHECK_REQUIRED","REPAIR_REQUIRED","OUTPUT_GATE_REQUIRED","SIGNATURE_REQUIRED","RELEASED"}:
            fp={"a":1}; pi={"b":2}
            context={"fact_pack":fp,"production_plan_item":pi,"sha256":guard.stable({"fact_pack":fp,"production_plan_item":pi})}
            authoring={"contract":"bound"}
        if phase in {"CHECK_REQUIRED","REPAIR_REQUIRED","OUTPUT_GATE_REQUIRED","SIGNATURE_REQUIRED","RELEASED"}:
            draft="draft"; revision=1
        if phase=="REPAIR_REQUIRED":
            checks={"status":"FAIL"}; last="ERR"
        if phase in {"OUTPUT_GATE_REQUIRED","SIGNATURE_REQUIRED","RELEASED"}:
            checks={"status":"PASS","checked_draft_sha256":hashlib.sha256(draft.encode()).hexdigest()}
        if phase=="SIGNATURE_REQUIRED": release={"status":"READY"}
        if phase=="RELEASED": released=True
        article={"canonical_article_id":"article:0","item_index":0,**{k:self.identity[k] for k in ("title","target_keyword","category","article_type","plan_slot")}}
        state={
            "contract":guard.STATE_CONTRACT,
            "source_snapshot_sha256":hashlib.sha256(b"source").hexdigest(),
            "batch_sha256":self.binding["batch_sha256"],
            "article":article,"immutable_core_sha256":"","publish_allowed":False,
            "phase":phase,"revision":revision,"research":research,"facts":facts,
            "production_context":context,"authoring_contract":authoring,
            "draft_markdown":draft,
            "draft_sha256":hashlib.sha256(draft.encode()).hexdigest() if draft else None,
            "checks":checks,"last_error":last,"release_prepared":release,"released":released,
        }
        state["immutable_core_sha256"]=guard.stable({
            "contract":state["contract"],"source_snapshot_sha256":state["source_snapshot_sha256"],
            "batch_sha256":state["batch_sha256"],"article":state["article"],
        })
        return state

    def capsule(self,state):
        raw=(json.dumps(state,ensure_ascii=False,indent=2,sort_keys=True)+"\n").encode()
        row={"path":"state.json","size":len(raw),"sha256":hashlib.sha256(raw).hexdigest(),"base64":base64.b64encode(raw).decode()}
        normalized=[{"path":"state.json","size":row["size"],"sha256":row["sha256"]}]
        return {
            "contract":guard.CAPSULE_CONTRACT,"status":"RECOVERY_CAPSULE_READY",
            "workspace_identity":guard._capsule_identity(state),"file_count":1,
            "tree_sha256":guard._tree_hash(normalized),"files":[row],"publish_allowed":False,
        }

    def test_every_inner_phase_resumes_only_from_capsule(self):
        outer=self.outer("AUTHORING_REQUIRED")
        for phase in guard.INNER_PHASE_ACTIONS:
            result=guard.build(self.binding,outer,self.capsule(self.canonical_state(phase)))
            verified=guard.verify(self.binding,outer,result)
            self.assertEqual("UNIVERSAL_REENTRY_ALLOWED",verified["status"])
            self.assertEqual(phase,result["workspace_action"]["inner_phase"])

    def test_all_allowed_transitions_and_illegal_jumps(self):
        outer=self.outer("AUTHORING_REQUIRED")
        for before,afters in guard.INNER_TRANSITIONS.items():
            for after in afters:
                previous=guard.build(self.binding,outer,self.capsule(self.canonical_state(before)))
                current=guard.build(self.binding,outer,self.capsule(self.canonical_state(after)),previous)
                guard.validate_transition(previous,current)
        for before,after in (("RESEARCH_REQUIRED","DRAFT_REQUIRED"),("REPAIR_REQUIRED","OUTPUT_GATE_REQUIRED"),("RELEASED","RESEARCH_REQUIRED")):
            previous=guard.build(self.binding,outer,self.capsule(self.canonical_state(before)))
            with self.assertRaises(guard.Blocked):
                guard.build(self.binding,outer,self.capsule(self.canonical_state(after)),previous)

    def test_tamper_wrong_article_and_missing_capsule_block(self):
        outer=self.outer("AUTHORING_REQUIRED")
        capsule=self.capsule(self.canonical_state("CHECK_REQUIRED"))
        capsule["files"][0]["base64"]=base64.b64encode(b"{}").decode()
        with self.assertRaises(guard.Blocked):
            guard.build(self.binding,outer,capsule)
        state=self.canonical_state("DRAFT_REQUIRED")
        state["article"]["title"]="WRONG"
        state["immutable_core_sha256"]=guard.stable({
            "contract":state["contract"],"source_snapshot_sha256":state["source_snapshot_sha256"],
            "batch_sha256":state["batch_sha256"],"article":state["article"],
        })
        with self.assertRaises(guard.Blocked):
            guard.build(self.binding,outer,self.capsule(state))
        for phase in ("LT68_REQUIRED","PPM679_REQUIRED","REPAIR_REQUIRED"):
            with self.assertRaisesRegex(guard.Blocked,"WORKSPACE_CAPSULE_REQUIRED_FOR_ACTIVE_ARTICLE"):
                guard.build(self.binding,self.outer(phase),None)

    def test_pserc_endstempel_stop_and_no_free_chat_paths(self):
        expected=(("ALL_ARTICLES_LT_PPM_PASS","RUN_PSERC"),("PSERC_PASS_ENDSTEMPEL_REQUIRED","RUN_ENDSTEMPEL"),("ENDSTEMPEL_PASS_STOP","STOP"))
        for phase,action in expected:
            result=guard.build(self.binding,self.outer(phase),None)
            self.assertEqual(action,result["allowed_action"]["action"])
        result=guard.build(self.binding,self.outer("AUTHORING_REQUIRED"),self.capsule(self.canonical_state("RESEARCH_REQUIRED")))
        self.assertFalse(result["policy"]["free_chat_execution"])
        self.assertFalse(result["policy"]["free_repo_search"])
        self.assertFalse(result["policy"]["free_binary_lookup"])
        self.assertEqual("STOP",result["policy"]["missing_canonical_execution_environment"])

if __name__=="__main__":
    unittest.main(verbosity=2)
