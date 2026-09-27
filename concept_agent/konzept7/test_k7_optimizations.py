from __future__ import annotations
import json,tempfile,unittest
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(HERE/"concept_agent"))
sys.path.insert(0,str(HERE/"concept_agent"/"konzept7"))

import intake_bridge,production_bridge
import k7_execution_lock,k7_research_planner,k7_parallel_controller,k7_closeout_plan,k7_metrics,k7_start_controller,k7_bound_fact_context,k7_section_balance

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
            self.assertEqual(bp["target_trace_lexical_support_ratio"],1.0)
            self.assertEqual(bp["trace_unit_minimum_shared_lexical_tokens"],2)
            self.assertEqual(bp["trace_lexical_reference"],"REFERENCED_FACT_STATEMENT_PLUS_EVIDENCE")
            title_guard=bp["existing_ppm_title_repeat_guard"]
            self.assertTrue(title_guard["normalized_title_repeat_in_visible_body_forbidden"])
            collision=item["writer_preflight"]["k7_h2_target_keyword_policy"]["title_target_normalized_equal"]
            self.assertEqual(title_guard["title_target_collision"],collision)
            self.assertEqual(title_guard["exact_target_keyword_in_visible_body_allowed"],not collision)
            self.assertEqual(title_guard["bound_table_value_statement_usage"],"PARAPHRASE_IF_VERBATIM_TEXT_WOULD_REPEAT_NORMALIZED_TITLE")
            self.assertFalse(title_guard["ppm679_changed"])
            trace_binding=bp["mechanical_requirements_prebound"]["source_trace_field_binding"]
            self.assertEqual(trace_binding["data_fact_id"],"REFERENCED_FACT_ID")
            self.assertEqual(trace_binding["data_source_title"],"REFERENCED_FACT_SOURCE_ID")
            self.assertEqual(trace_binding["data_source_hash"],"REFERENCED_FACT_EVIDENCE_TEXT_SHA256")
            self.assertFalse(trace_binding["visible_text_mutation_required"])
            self.assertTrue(bp["repair_policy"]["all_findings_from_same_checker_one_revision"])
            balance=bp["section_balance"]
            self.assertEqual(balance["contract"],"K7_SECTION_BALANCE_POLICY_V1")
            self.assertEqual(balance["minimum_words"],60)
            self.assertEqual(balance["maximum_words"],120)
            self.assertEqual(balance["exempt_block_ids"],["table","conclusion","further_information"])
            self.assertTrue(balance["apply_to_last_normal_h2"])
            self.assertEqual(item["writer_preflight"]["k7_section_balance_policy"],balance)
            self.assertNotIn("recovery_article_content",item["forbidden_inputs"])
            self.assertFalse(bp["ppm679_changed"]); self.assertFalse(bp["languagetool68_changed"])


    def test_section_balance_and_archive_isolation(self):
        self.assertFalse((HERE/"recovery/current16-input").exists())
        def words(n):
            return " ".join("wort"+str(i) for i in range(n))
        good='<section data-block="body"><h2>A</h2><p>'+words(60)+'</p><h2>B</h2><p>'+words(120)+'</p></section>'
        out=k7_section_balance.validate(good)
        self.assertEqual([row["word_count"] for row in out["sections"]],[60,120])
        with self.assertRaises(k7_section_balance.SectionBalanceError):
            k7_section_balance.validate('<section data-block="body"><h2>A</h2><p>'+words(59)+'</p></section>')
        with self.assertRaises(k7_section_balance.SectionBalanceError):
            k7_section_balance.validate('<section data-block="body"><h2>A</h2><p>'+words(121)+'</p></section>')
        special=good+'<section data-block="table"><h2>Tabelle</h2><p>kurz</p></section><section data-block="conclusion"><h2>Fazit</h2><p>kurz</p></section><section data-block="further_information"><h2>Weiterführende Informationen</h2><p>kurz</p></section>'
        self.assertEqual(len(k7_section_balance.validate(special)["sections"]),2)

    def test_start_lock_exists_before_research_and_duplicate_resumes(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            snap_path=root/"snapshot.json"
            snap_path.write_text((HERE/"concept_agent/current/PSERC_METADATA_SNAPSHOT.json").read_text(encoding="utf-8"),encoding="utf-8")
            first=k7_start_controller.start(snap_path,None,root/"run",4,1)
            self.assertEqual(first["status"],"NEW_RUN_CREATED")
            self.assertEqual(first["stage"],"RESEARCH_REQUIRED")
            self.assertTrue((root/"run"/"K7_RUN_ROOT.json").is_file())
            second=k7_start_controller.start(snap_path,None,root/"run",4,1)
            self.assertEqual(second["status"],"RESUME_EXISTING_RUN")
            prod=k7_start_controller.start(snap_path,HERE/"concept_agent/current/CONCEPT_AGENT_RESEARCH_BOUND.json",root/"run",4,1)
            self.assertEqual(prod["stage"],"ARTICLE_PRODUCTION")
            self.assertEqual(len(prod["ready_actions"]),4)

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


    def test_bound_fact_context_builds_real16_without_new_research(self):
        import authoring_contract
        out=k7_bound_fact_context.build_all(self.binding)
        self.assertEqual(out["item_count"],16)
        self.assertFalse(out["new_external_research_performed"])
        self.assertFalse(out["historical_article_content_used"])
        self.assertEqual(out["source"],"CURRENT_HASH_BOUND_RESEARCH_ONLY")
        for row in out["items"]:
            identity=row["identity"]
            state={"article":{
                "title":identity["title"],
                "target_keyword":identity["target_keyword"],
                "category":identity["category"],
                "article_type":identity["article_type"],
                "plan_slot":identity["plan_slot"],
            },"source_snapshot_sha256":row["fact_pack"]["source_snapshot_id"]}
            contract=authoring_contract.build(HERE,state,row["fact_pack"],row["production_plan_item"])
            self.assertEqual(contract["article_identity"]["article_type"],identity["article_type"])
            self.assertGreaterEqual(len(contract["bound_requirements"]["canonical_fact_ids"]),3)
            if identity["article_type"]=="FAQ":
                self.assertTrue(contract["bound_requirements"]["faq_direct_answer"])

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
