import json
from pathlib import Path
import unittest

BRANCH="konzept0-portal-neutral-20261002"

class K0StartRouterTests(unittest.TestCase):
    def test_router_pins_fresh_k0_entry(self):
        text=Path("K0_START_HERE.md").read_text(encoding="utf-8")
        self.assertIn("K0:start", text)
        self.assertIn(BRANCH, text)
        self.assertIn("aktuellen Upload", text)
        self.assertIn("WORDPRESS_INTAKE.json", text)
        self.assertIn("AUTHORING_CONTEXT.json", text)
        self.assertIn(".github/workflows/k0-authoring-context.yml", text)
        self.assertIn("workflow_dispatch", text)
        self.assertIn("nicht erforderlich", text)
        self.assertIn("Vor dem ersten GitHub-Schreibversuch", text)

    def test_start_contract_fans_out_any_positive_batch_size(self):
        text=Path("K0_START_HERE.md").read_text(encoding="utf-8")
        self.assertIn("N >= 1", text)
        self.assertIn("item_count = 1", text)
        self.assertIn("genau einen frischen K0-Einzelrun", text)
        self.assertIn("engine/wordpress_batch_export.py", text)
        self.assertIn("ursprünglichen Upload-Reihenfolge", text)
        self.assertIn("Mehrfach-Upload direkt als einen Mehrfach-Writer-Run", text)

    def test_current_is_neutral_and_fresh(self):
        cur=json.loads(Path("K0_CURRENT_STATE.json").read_text(encoding="utf-8"))
        self.assertEqual(cur["concept"], "K0")
        self.assertEqual(cur["branch"], BRANCH)
        self.assertEqual(cur["status"], "READY_FOR_FRESH_K0_START")
        self.assertIsNone(cur["first_open_blocker"])
        self.assertEqual(cur["work_binding"]["start_command"], "K0:start")
        self.assertEqual(cur["work_binding"]["current_request_authority"], "CURRENT_VALID_UPLOAD_ONLY")
        self.assertTrue(cur["work_binding"]["fresh_run_required"])
        self.assertEqual(cur["work_binding"]["start_mechanism"]["accepted_upload_item_count"], "N>=1")
        self.assertTrue(cur["work_binding"]["start_mechanism"]["per_item_run_required"])
        self.assertEqual(cur["work_binding"]["start_mechanism"]["per_item_intake_item_count"], 1)
        self.assertEqual(cur["work_binding"]["start_mechanism"]["writer_core_mode"], "UNCHANGED_SINGLE_ITEM")
        self.assertEqual(cur["work_binding"]["start_mechanism"]["final_reassembly"], "engine/wordpress_batch_export.py")
        self.assertFalse(cur["work_binding"]["start_mechanism"]["workflow_dispatch_required"])
        self.assertTrue(cur["work_binding"]["start_mechanism"]["write_attempt_required_before_start_blocker"])
        self.assertFalse(cur["work_binding"]["alternate_route_allowed"])

    def test_goal_is_current_upload_only(self):
        goal=json.loads(Path("K0_GOAL_CONTRACT.json").read_text(encoding="utf-8"))
        h=goal["hard_rules"]
        self.assertEqual(h["assignment_authority"], "CURRENT_VALID_UPLOAD_ONLY")
        self.assertTrue(h["existing_github_file_trigger_required"])
        self.assertFalse(h["workflow_dispatch_required"])
        self.assertTrue(h["start_blocker_requires_failed_current_run_write_attempt"])
        self.assertTrue(h["content_sources_must_be_current_run_only"])

    def test_active_control_files_have_no_run_or_test_history(self):
        corpus="\n".join([
            Path("K0_START_HERE.md").read_text(encoding="utf-8"),
            Path("K0_CURRENT_STATE.json").read_text(encoding="utf-8"),
            Path("K0_GOAL_CONTRACT.json").read_text(encoding="utf-8"),
        ]).lower()
        forbidden=[
            "rewrite16",
            "latest_writer",
            "selftest_run",
            "selftest_result",
            "history_ref",
            "evidence_ref",
            "main_merge_sha",
            "regression_test",
            "fresh_regression",
            "kappzaum",
            "schabracke",
            "user3",
            "371",
            "372",
            "k8",
            "k9",
            "k10",
        ]
        for token in forbidden:
            self.assertNotIn(token, corpus, token)

if __name__=="__main__":
    unittest.main()
