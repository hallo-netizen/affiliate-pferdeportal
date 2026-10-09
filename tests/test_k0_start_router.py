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

    def test_current_binds_only_k0_router(self):
        cur=json.loads(Path("K0_CURRENT_STATE.json").read_text(encoding="utf-8"))
        self.assertEqual(cur["concept"],"K0")
        self.assertEqual(cur["branch"],BRANCH)
        self.assertEqual(cur["work_binding"]["start_command"],"K0:start")
        self.assertEqual(cur["work_binding"]["start_ref"],"K0_START_HERE.md")
        self.assertFalse(cur["work_binding"]["alternate_route_allowed"])
        self.assertFalse(cur["old_chat_or_archive_authority"])

if __name__=="__main__":
    unittest.main()
