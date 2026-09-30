import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class KissWorkflowOptimizationTests(unittest.TestCase):
    def text(self,path):
        return (ROOT/path).read_text(encoding="utf-8")

    def test_quality_and_concept_gates_unchanged(self):
        contract=json.loads(self.text("K9_CONTRACT.json"))
        self.assertEqual(contract["transitions"],{
            "research_pass":"write",
            "write_pass":"check",
            "check_fail":"repair",
            "repair_pass":"check",
            "check_pass_terminal":"pserc_endstempel_wordpress_stop",
        })
        self.assertEqual(contract["quality"],{
            "language_tool":"6.8",
            "ppm":"6.7.9",
            "pserc_required":True,
            "endstempel_required":True,
            "wordpress_final_verify_required":True,
        })
        self.assertFalse(contract["publish_allowed"])

    def test_selftest_runs_for_code_not_runtime_state_churn(self):
        wf=self.text(".github/workflows/k9-selftest.yml")
        self.assertIn("paths:",wf)
        for required in ("'k9_*.py'","'quality/**'","'contracts/**'","'tests/**'"):
            self.assertIn(required,wf)
        for forbidden in ("'runtime/**'","'state/**'","'warehouse/**'","'writer_drafts/**'","'submissions/**'","'final/**'"):
            self.assertNotIn(forbidden,wf)

    def test_runtime_hops_do_not_repeat_full_software_suite(self):
        receiver=self.text(".github/workflows/text-start-pferdeatelier.yml")
        accept=self.text(".github/workflows/k9-accept-submission.yml")
        finalizer=self.text(".github/workflows/k9-finalize.yml")
        self.assertIn("Hard tests once at explicit production entry",receiver)
        self.assertIn("inputs.run_mode != 'inherit'",receiver)
        self.assertNotIn("unittest discover",accept)
        self.assertNotIn("unittest discover",finalizer)

    def test_writer_preflight_and_one_pass_repair_are_hard_bound(self):
        engine=self.text("k9_engine.py")
        packager=self.text("k9_write_packager.py")
        contracts=json.loads(self.text("contracts/K9_WORKER_CONTRACTS.json"))
        self.assertIn("EXACT_RUNTIME_CHAT_ENTRY_ONLY",engine)
        self.assertIn('"all_other_actions": "DENY"',engine)
        self.assertIn("CHAT_ENTRY_WRITER_PREFLIGHT_GUARD_INVALID",engine)
        self.assertIn("complete_rule_preflight",packager)
        self.assertIn("WRITING_PREFLIGHT_REPAIR_REQUIRED",packager)
        self.assertIn("REPAIR_ALL_REPORTED_FAILURES_IN_ONE_PASS",contracts["contracts"]["repair"]["must"])
        self.assertIn("DO_NOT_STOP_AFTER_FIRST_REPORTED_FINDING",contracts["contracts"]["repair"]["must"])

    def test_finalizer_keeps_all_real_gates_and_mandates_chat_file(self):
        wf=self.text(".github/workflows/k9-finalize.yml")
        for required in (
            "k9_pserc.py",
            "k9_endstempel.py build",
            "k9_endstempel.py verify",
            "k9_wordpress_verify.py",
            "runtime/CHAT_DELIVERY.json",
            "DELIVER_FINAL_WORDPRESS_FILE_IN_CHAT",
            "k9-wordpress-final-json",
            "actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02",
        ):
            self.assertIn(required,wf)

if __name__=="__main__":
    unittest.main()
