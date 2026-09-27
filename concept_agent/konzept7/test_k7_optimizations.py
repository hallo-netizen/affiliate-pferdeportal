from __future__ import annotations
import json,tempfile,unittest
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(HERE/"concept_agent"))
sys.path.insert(0,str(HERE/"concept_agent"/"konzept7"))

import intake_bridge,production_bridge
import k7_execution_lock,k7_research_planner,k7_parallel_controller,k7_closeout_plan,k7_metrics

class K7OptimizationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        snap=json.loads((HERE/"concept_agent/current/PSERC_METADATA_SNAPSHOT.json").read_text(encoding="utf-8"))
        research=json.loads((HERE/"concept_agent/current/CONCEPT_AGENT_RESEARCH_BOUND.json").read_text(encoding="utf-8"))
        cls.intake=intake_bridge.prepare(snap)
        cls.research=research
        cls.binding=production_bridge.build(snap,cls.intake,research)

    def test_writer_blueprint_real16(self):
        self.assertEqual(self.binding["item_count"],16)
        self.assertEqual(self.binding["k7_execution_policy"]["default_article_lanes"],4)
        for item in self.binding["items"]:
            bp=item["writer_preflight"]["k7_first_draft_blueprint"]
            req=item["writer_preflight"]["global_requirements"]
            self.assertEqual(bp["target_min_words"],int(req["min_words"])+100)
            self.assertEqual(bp["target_min_paragraphs"],int(req["min_paragraphs"])+2)
            self.assertEqual(bp["target_min_table_body_rows"],int(req["min_table_body_rows"])+1)
            self.assertGreater(bp["target_conclusion_ratio_if_applicable"],0.10)
            self.assertGreater(bp["target_table_unique_token_ratio_if_applicable"],0.18)
            self.assertTrue(bp["repair_policy"]["all_findings_from_same_checker_one_revision"])
            self.assertFalse(bp["ppm679_changed"]); self.assertFalse(bp["languagetool68_changed"])

    def test_execution_lock_duplicate_resume_conflict_block(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"lock.json"; b=self.binding
            a=k7_execution_lock.acquire(p,b["batch_sha256"],b["binding_sha256"],b["item_count"],1)
            self.assertEqual(a["status"],"CREATED")
            r=k7_execution_lock.acquire(p,b["batch_sha256"],b["binding_sha256"],b["item_count"],1)
            self.assertEqual(r["status"],"RESUME_EXISTING")
            with self.assertRaises(k7_execution_lock.Blocked):
                k7_execution_lock.acquire(p,"0"*64,b["binding_sha256"],b["item_count"],1)

    def test_research_exact_reuse_and_parallel_miss_plan(self):
        reused=k7_research_planner.plan(self.intake,self.research,4)
        self.assertTrue(reused["exact_bound_reuse"])
        self.assertTrue(all(x["mode"]=="REUSE_EXACT_BOUND_RESEARCH" for x in reused["items"]))
        fresh=k7_research_planner.plan(self.intake,None,4)
        self.assertFalse(fresh["exact_bound_reuse"])
        self.assertEqual([x["lane"] for x in fresh["items"][:8]],[0,1,2,3,0,1,2,3])
        self.assertTrue(all(x["new_external_lookup_required"] for x in fresh["items"]))

    def test_parallel_lane_matrix_and_no_cross_article_mix(self):
        for lanes in (1,2,4,8):
            out=k7_parallel_controller.simulate(self.binding,lanes)
            self.assertEqual(out["batch_phase"],"COMPLETE")
            self.assertEqual(out["pserc"],"PASS"); self.assertEqual(out["endstempel"],"PASS")
            for i,row in enumerate(out["items"]):
                self.assertEqual(row["lane"],i%lanes)
                self.assertEqual(row["phase"],"PASS")
                self.assertEqual(row["revision_history"][0]["content_utf8"],f"<article><h2>Artikel {i}</h2><p>synthetic-{i}</p></article>")

    def test_bundled_repair_keeps_real_before_after_bytes(self):
        s=k7_parallel_controller.initial(self.binding,4)
        body1="<article><h2>A</h2><p>vorher</p></article>"
        s=k7_parallel_controller.record_draft(self.binding,s,0,body1)
        s=k7_parallel_controller.record_check(self.binding,s,0,"LT68","PASS")
        findings=[{"code":"A"},{"code":"B"},{"code":"C"}]
        s=k7_parallel_controller.record_check(self.binding,s,0,"PPM679","REPAIR_REQUIRED",findings)
        body2="<article><h2>A</h2><p>nachher sauber</p></article>"
        s=k7_parallel_controller.record_repair(self.binding,s,0,body2)
        row=s["items"][0]
        self.assertEqual(row["phase"],"LT68_REQUIRED")
        self.assertEqual(row["repair_count"],1)
        self.assertEqual(len(row["revision_history"]),2)
        self.assertEqual(row["revision_history"][0]["content_utf8"],body1)
        self.assertEqual(row["revision_history"][1]["content_utf8"],body2)
        self.assertEqual(row["revision_history"][1]["source_finding_count"],3)

    def test_closeout_preallocated_no_search(self):
        p=k7_closeout_plan.build(self.binding["batch_sha256"],self.binding["item_count"],1)
        self.assertFalse(p["route_search_after_articles"])
        self.assertEqual(p["steps"],["PSERC","ENDSTEMPEL","FINAL_WORDPRESS_JSON"])
        self.assertIn(self.binding["batch_sha256"],p["release_tag"])

    def test_metrics_exact_duration_math(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"metrics.json"
            k7_metrics.event(p,"WRITE_DRAFT",0,"START",1_000_000_000)
            x=k7_metrics.event(p,"WRITE_DRAFT",0,"END",4_500_000_000)
            sm=k7_metrics.summary(x)
            self.assertEqual(sm["WRITE_DRAFT"]["total_seconds"],3.5)

if __name__=="__main__":
    unittest.main()
