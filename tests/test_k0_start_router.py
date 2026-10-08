import json
from pathlib import Path
import unittest

BRANCH="konzept0-portal-neutral-20261002"

class K0StartRouterTests(unittest.TestCase):
    def test_router_pins_fresh_k0_entry_without_broad_presearch(self):
        text=Path("K0_START_HERE.md").read_text(encoding="utf-8")
        self.assertIn("K0:start", text)
        self.assertIn(BRANCH, text)
        self.assertIn("aktuellen Upload", text)
        self.assertIn("Keine andere Repository-Datei", text)
        self.assertIn("keine breite Repository-/Campus-Suche", text)
        self.assertIn("WORDPRESS_INTAKE.json", text)
        self.assertIn("AUTHORING_CONTEXT.json", text)
        self.assertIn(".github/workflows/k0-authoring-context.yml", text)
        self.assertIn("workflow_dispatch", text)
        self.assertIn("nicht erforderlich", text)
        self.assertIn("Vor dem ersten tatsächlichen GitHub-Schreibversuch", text)

    def test_start_processes_every_upload_item_through_existing_single_run_contract(self):
        text=Path("K0_START_HERE.md").read_text(encoding="utf-8")
        self.assertIn("Alle Einträge des aktuellen Uploads werden bearbeitet", text)
        self.assertIn("eigenen frischen K0-Einzelrun", text)
        self.assertIn("item_count = 1", text)
        self.assertIn("keine Begrenzung des Gesamtauftrags", text)
        self.assertIn("Mehrfach-Upload direkt als Mehrfach-Writer-Run", text)
        self.assertIn("engine/wordpress_batch_export.py", text)
        self.assertIn("ursprünglichen Upload-Reihenfolge", text)

    def test_intake_to_authoring_context_is_mandatory_no_stop_transition(self):
        text=Path("K0_START_HERE.md").read_text(encoding="utf-8")
        self.assertIn("Intake → Authoring Context — NO-STOP-HARDLOCK", text)
        self.assertIn("niemals** ein Abschluss, Statuspunkt, Wartepunkt oder Blocker", text)
        self.assertIn("ohne Rückgabe an den Nutzer", text)
        self.assertIn("erwartete Zwischenzustand", text)
        self.assertIn("muss den fehlenden Kontext selbst erzeugen", text)
        self.assertIn("Recherche- und Regelkontext fehlt", text)
        self.assertIn("nächster Schritt: Kontext erstellen", text)
        self.assertIn("Beenden des Chats nach dem Intake-Commit", text)
        self.assertIn("tatsächlich versucht wurde und gescheitert ist", text)

    def test_start_has_no_total_quantity_cap_logic(self):
        corpus="\n".join([
            Path("K0_START_HERE.md").read_text(encoding="utf-8"),
            Path("K0_CURRENT_STATE.json").read_text(encoding="utf-8"),
            Path("K0_GOAL_CONTRACT.json").read_text(encoding="utf-8"),
        ])
        self.assertNotIn("N >= 1", corpus)
        self.assertNotIn("accepted_upload_item_count", corpus)
        self.assertNotIn("maximum_articles", corpus)
        self.assertNotIn("maximum_articles_per_type", corpus)

    def test_current_binds_complete_fresh_file_start(self):
        cur=json.loads(Path("K0_CURRENT_STATE.json").read_text(encoding="utf-8"))
        self.assertEqual(cur["concept"], "K0")
        self.assertEqual(cur["branch"], BRANCH)
        self.assertEqual(cur["status"], "READY_FOR_FRESH_K0_START")
        self.assertIsNone(cur["first_open_blocker"])
        self.assertEqual(cur["work_binding"]["current_request_authority"], "CURRENT_VALID_UPLOAD_ONLY")
        self.assertTrue(cur["work_binding"]["fresh_run_required"])
        mech=cur["work_binding"]["start_mechanism"]
        self.assertEqual(mech["work_scope"], "ALL_ITEMS_FROM_CURRENT_VALID_UPLOAD")
        self.assertTrue(mech["per_item_run_required"])
        self.assertEqual(mech["per_item_write_order"], ["WORDPRESS_INTAKE.json","AUTHORING_CONTEXT.json"])
        self.assertEqual(mech["writer_core_mode"], "UNCHANGED_SINGLE_ITEM")
        self.assertFalse(mech["direct_multi_item_writer_run_allowed"])
        self.assertEqual(mech["final_reassembly"], "engine/wordpress_batch_export.py")
        self.assertEqual(mech["final_order"], "ORIGINAL_UPLOAD_ORDER")
        self.assertFalse(mech["workflow_dispatch_required"])
        self.assertTrue(mech["write_attempt_required_before_start_blocker"])
        self.assertFalse(cur["active_read_scope"]["broad_repository_or_campus_search_before_binding_allowed"])
        self.assertFalse(cur["work_binding"]["alternate_route_allowed"])

    def test_goal_preserves_start_hardlocks_without_quantity_cap(self):
        goal=json.loads(Path("K0_GOAL_CONTRACT.json").read_text(encoding="utf-8"))
        h=goal["hard_rules"]
        self.assertEqual(h["assignment_authority"], "CURRENT_VALID_UPLOAD_ONLY")
        self.assertTrue(h["all_current_upload_items_must_be_processed"])
        self.assertFalse(h["additional_quantity_field_may_reduce_or_select_work"])
        self.assertFalse(h["broad_repository_or_campus_search_before_current_upload_binding_allowed"])
        self.assertTrue(h["existing_github_file_trigger_required"])
        self.assertFalse(h["workflow_dispatch_required"])
        self.assertTrue(h["start_blocker_requires_failed_current_run_write_attempt"])
        self.assertTrue(h["per_upload_item_fresh_single_item_run_required"])
        self.assertFalse(h["direct_multi_item_writer_run_allowed"])
        self.assertTrue(h["writer_single_item_contract_must_remain_unchanged"])
        self.assertTrue(h["final_batch_reassembly_required"])
        self.assertTrue(h["final_batch_order_must_match_input"])
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
