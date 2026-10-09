import json
from pathlib import Path
import unittest

BRANCH="konzept0-portal-neutral-20261002"

class K0StartRouterTests(unittest.TestCase):
    def test_local_k0_router_is_present_and_pins_k0(self):
        p=Path("K0_START_HERE.md")
        self.assertTrue(p.is_file(),"K0_START_HERE.md missing")
        text=p.read_text(encoding="utf-8")
        self.assertIn("K0:start",text)
        self.assertIn(BRANCH,text)
        self.assertIn("K0_CURRENT_STATE.json",text)
        self.assertNotIn("control/startmaster0107/CURRENT_STATE.json",text)

    def test_goal_contract_makes_current_upload_the_general_assignment_authority(self):
        g=json.loads(Path("K0_GOAL_CONTRACT.json").read_text(encoding="utf-8"))
        h=g["hard_rules"]
        self.assertTrue(h["current_valid_upload_is_assignment_authority"])
        self.assertFalse(h["stale_current_history_or_prior_run_may_select_or_block_current_upload"])
        self.assertTrue(h["terminal_blocker_requires_current_run_evidence"])
        self.assertTrue(h["fresh_research_required_for_every_new_upload"])
        self.assertTrue(h["historical_text_or_research_artifact_as_content_source_forbidden"])
        self.assertTrue(h["historical_information_blacklist_forbidden"])
        self.assertTrue(h["independently_rediscovered_same_facts_or_sources_allowed"])
        self.assertTrue(h["topic_specific_start_logic_forbidden"])

    def test_start_hardlock_forbids_stale_status_as_terminal_blocker(self):
        text=Path("K0_START_HERE.md").read_text(encoding="utf-8")
        self.assertIn("allgemein für jeden gültigen K0-Upload",text)
        self.assertIn("dürfen den aktuellen Upload weder auswählen, ersetzen noch blockieren",text)
        self.assertIn("nach Bindung des aktuellen Uploads",text)
        self.assertIn("historische Informationen sind **keine Ausschlussliste**",text)

    def test_existing_github_file_start_mechanism_is_bound(self):
        text=Path("K0_START_HERE.md").read_text(encoding="utf-8")
        self.assertIn("bestehende GitHub-Dateistart",text)
        self.assertIn("`WORDPRESS_INTAKE.json` mit `create_file` schreiben",text)
        self.assertIn("`AUTHORING_CONTEXT.json` mit `create_file` schreiben",text)
        self.assertIn("fehlender `workflow_dispatch`-/Run-Button ist **kein Blocker**",text)
        self.assertIn("GitHub-Schreibversuch",text)

    def test_start_blocker_requires_real_github_write_attempt(self):
        text=Path("K0_START_HERE.md").read_text(encoding="utf-8")
        self.assertIn("niemals aus Vermutung als nicht verfügbar erklärt werden",text)
        self.assertIn("tatsächlichen Aufruf der vorhandenen GitHub-Dateischreibfunktion",text)
        self.assertIn("ein Chat darf nicht mit `0 von N produziert` abbrechen",text)

    def test_hidden_github_tools_must_be_discovered_before_unavailable(self):
        text=Path("K0_START_HERE.md").read_text(encoding="utf-8")
        self.assertIn("kein Nichtverfügbarkeitsnachweis",text)
        self.assertIn("Tool-Router/Code-Mode",text)
        self.assertIn("mcp__GitHub__create_file",text)
        self.assertIn("mcp__GitHub__update_file",text)
        self.assertIn("GITHUB_WRITE_UNAVAILABLE",text)

    def test_fresh_start_uses_current_upload_without_extra_release(self):
        text=Path("K0_START_HERE.md").read_text(encoding="utf-8")
        self.assertIn("gültige aktuelle Upload startet die frischen Einzelruns direkt",text)
        self.assertIn("keine zusätzliche Batch-Freigabe wird gelesen oder benötigt",text)
        self.assertIn("WRITER_JOB.json",text)
        self.assertNotIn("1er-/3er-/7er-",text)

    def test_current_upload_fans_out_only_to_existing_single_item_k0_runs(self):
        text=Path("K0_START_HERE.md").read_text(encoding="utf-8")
        self.assertIn("N >= 1",text)
        self.assertIn("genau N-mal",text)
        self.assertIn("item_count = 1",text)
        self.assertIn("unveränderten Fünf-Felder-Eintrag",text)
        self.assertIn(".github/workflows/k0-authoring-context.yml",text)
        self.assertIn("engine/wordpress_batch_export.py",text)
        self.assertIn("ursprünglicher Upload-Reihenfolge",text)
        self.assertIn("control/startmaster0107/**",text)
        self.assertIn("keine K0-Auftrags- oder Batch-Autorität",text)

    def test_after_intake_continues_same_run_without_legacy_lookup(self):
        text=Path("K0_START_HERE.md").read_text(encoding="utf-8")
        self.assertIn("unmittelbar nächste Schritt",text)
        self.assertIn("AUTHORING_CONTEXT.json",text)
        self.assertIn("keine** alten Aufträge".replace("keine**","keine"),text.replace("**",""))
        self.assertIn("Testanbindungen",text)
        self.assertIn("control/startmaster0107/**",text)
        self.assertIn("nicht überschrieben",text)

    def test_current_binds_only_k0_router(self):
        cur=json.loads(Path("K0_CURRENT_STATE.json").read_text(encoding="utf-8"))
        self.assertEqual(cur["concept"],"K0")
        self.assertEqual(cur["branch"],BRANCH)
        self.assertEqual(cur["work_binding"]["start_command"],"K0:start")
        self.assertEqual(cur["work_binding"]["start_ref"],"K0_START_HERE.md")
        self.assertFalse(cur["work_binding"]["alternate_route_allowed"])
        self.assertFalse(cur["old_chat_or_archive_authority"])
        self.assertNotIn("scope_lock",cur["work_binding"])
        self.assertNotIn("plugin_version",cur["wordpress_export"])
        self.assertNotIn("plugin_build",cur["wordpress_export"])
        goal=json.loads(Path("K0_GOAL_CONTRACT.json").read_text(encoding="utf-8"))
        self.assertNotIn("wordpress_plugin_binding",goal["hard_rules"])
        self.assertEqual(cur["work_binding"]["start_mechanism"]["accepted_upload_item_count"],"N>=1")
        self.assertTrue(cur["work_binding"]["start_mechanism"]["per_item_run_required"])
        self.assertEqual(cur["work_binding"]["start_mechanism"]["per_item_intake_item_count"],1)
        self.assertEqual(cur["work_binding"]["start_mechanism"]["writer_core_mode"],"UNCHANGED_SINGLE_ITEM")
        self.assertEqual(cur["work_binding"]["start_mechanism"]["final_reassembly"],"engine/wordpress_batch_export.py")
        self.assertIn("control/startmaster0107",cur["work_binding"]["start_mechanism"]["forbidden_assignment_roots"])
        self.assertTrue(goal["hard_rules"]["batch_item_count_independent"])
        self.assertTrue(goal["hard_rules"]["batch_fanout_to_existing_single_item_runs_required"])
        self.assertTrue(goal["hard_rules"]["writer_single_item_contract_must_remain_unchanged"])
        self.assertTrue(goal["hard_rules"]["final_batch_reassembly_required"])
        self.assertTrue(goal["hard_rules"]["final_batch_order_must_match_input"])
        self.assertTrue(goal["hard_rules"]["startmaster0107_as_k0_assignment_authority_forbidden"])
        self.assertEqual(cur["work_binding"]["start_mechanism"]["after_each_intake"],"RESEARCH_THEN_WRITE_AUTHORING_CONTEXT_IN_SAME_RUN")
        self.assertFalse(cur["work_binding"]["start_mechanism"]["legacy_release_lookup_allowed"])
        self.assertTrue(cur["work_binding"]["start_mechanism"]["resume_identical_current_intake_at_first_missing_artifact"])

if __name__=="__main__":
    unittest.main()
