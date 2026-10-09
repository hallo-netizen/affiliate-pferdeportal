import json
from pathlib import Path
import unittest

BRANCH="konzept0-portal-neutral-20261002"

class K0StartRouterTests(unittest.TestCase):
    def setUp(self):
        self.start=Path("K0_START_HERE.md").read_text(encoding="utf-8")
        self.current=json.loads(Path("K0_CURRENT_STATE.json").read_text(encoding="utf-8"))
        self.goal=json.loads(Path("K0_GOAL_CONTRACT.json").read_text(encoding="utf-8"))

    def test_router_is_ready_for_current_upload(self):
        self.assertIn("K0:start",self.start)
        self.assertIn(BRANCH,self.start)
        self.assertEqual(self.current["concept"],"K0")
        self.assertEqual(self.current["branch"],BRANCH)
        self.assertEqual(self.current["status"],"READY_FOR_FRESH_K0_START")
        self.assertEqual(self.current["next_action"],"K0:start")
        self.assertFalse(self.current["old_chat_or_archive_authority"])

    def test_current_upload_is_only_assignment_authority(self):
        hard=self.goal["hard_rules"]
        sm=self.current["work_binding"]["start_mechanism"]
        self.assertTrue(hard["current_valid_upload_is_assignment_authority"])
        self.assertFalse(hard["stale_current_history_or_prior_run_may_select_or_block_current_upload"])
        self.assertEqual(sm["assignment_authority"],"CURRENT_VALID_UPLOAD_ONLY")
        self.assertTrue(sm["process_every_current_upload_entry"])
        self.assertFalse(sm["fixed_upload_item_limit"])
        self.assertFalse(sm["prior_state_may_assign_or_block_current_upload"])

    def test_current_contains_no_bound_production_batch(self):
        self.assertNotIn("active_batch",self.current["work_binding"])
        sm=self.current["work_binding"]["start_mechanism"]
        self.assertNotIn("accepted_upload_item_count",sm)
        self.assertNotIn("expected_item_count",sm)

    def test_existing_single_item_production_path_is_unchanged(self):
        sm=self.current["work_binding"]["start_mechanism"]
        self.assertTrue(sm["per_item_run_required"])
        self.assertEqual(sm["writer_core_mode"],"UNCHANGED_SINGLE_ITEM")
        self.assertEqual(sm["trigger_workflow"],".github/workflows/k0-authoring-context.yml")
        self.assertEqual(sm["after_each_intake"],"RESEARCH_THEN_WRITE_AUTHORING_CONTEXT_IN_SAME_RUN")
        self.assertEqual(sm["final_reassembly"],"engine/wordpress_batch_export.py")
        self.assertEqual(sm["final_order"],"ORIGINAL_UPLOAD_ORDER")
        self.assertFalse(sm["workflow_dispatch_required"])

    def test_start_finds_research_and_production_path(self):
        for token in (
            "WORDPRESS_INTAKE.json",
            "Recherche",
            "AUTHORING_CONTEXT.json",
            ".github/workflows/k0-authoring-context.yml",
            "WRITER_JOB.json",
            "engine/wordpress_batch_export.py",
        ):
            self.assertIn(token,self.start)

    def test_quality_and_publish_locks_unchanged(self):
        self.assertFalse(self.goal["hard_rules"]["quality_reduction_allowed"])
        self.assertTrue(self.goal["hard_rules"]["language_tool_6_8_required"])
        self.assertTrue(self.goal["hard_rules"]["ppm_6_7_9_parity_required"])
        self.assertFalse(self.goal["hard_rules"]["publish_allowed"])
        self.assertFalse(self.current["publish_allowed"])

    def test_start_binds_real_github_write_action_before_completion(self):
        text=Path("K0_START_HERE.md").read_text(encoding="utf-8")
        self.assertIn("mcp__GitHub__create_file",text)
        self.assertIn("ALL_TOOLS",text)
        self.assertIn("kein Abschluss",text)

    def test_active_k0_workflows_do_not_depend_on_legacy_runtime_paths(self):
        for path in (
            ".github/workflows/k0-writer-accept.yml",
            ".github/workflows/k0-rewrite16-bind.yml",
        ):
            text=Path(path).read_text(encoding="utf-8")
            self.assertNotIn("startmaster0107",text)
            self.assertNotIn("runtime_packages",text)

    def test_k0_runtime_packages_are_exact_bound_bytes(self):
        import hashlib
        bound={
            "runtime/k0/canonical/PPM_6.7.9.zip":"acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1",
            "runtime/k0/canonical/PSERC_BINDING.zip":"77a14aca97f46d60bc9001d66327abb68dd9cac9ad111f8ecefa1a8afd345314",
        }
        for path,expected in bound.items():
            p=Path(path)
            self.assertTrue(p.is_file(),path)
            self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),expected,path)

if __name__=="__main__":
    unittest.main()
