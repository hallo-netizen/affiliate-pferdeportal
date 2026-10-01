import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import k9_engine

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

    def test_intake_does_not_duplicate_receiver_start_suite(self):
        intake=self.text(".github/workflows/k9-intake.yml")
        self.assertNotIn("unittest discover",intake)
        receiver=self.text(".github/workflows/text-start-pferdeatelier.yml")
        self.assertIn("Hard tests once at explicit production entry",receiver)

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

    def test_writer_receives_exact_hash_bound_ppm679_authoring_rules(self):
        rules=json.loads(self.text("contracts/K9_WRITING_RULES.json"))
        for article_type in rules["types"]:
            bound=k9_engine.ppm_authoring_rules(article_type)
            self.assertEqual(bound["contract"],"K9_PPM679_AUTHORING_RULES_V1")
            self.assertEqual(bound["ppm_package_sha256"],k9_engine.PPM679_PACKAGE_SHA256)
            self.assertEqual(bound["structure_requirements"]["contract"],"content_structure_language_gate_v2")
            self.assertEqual(bound["article_type"],article_type)
            declared=bound["rules_sha256"]
            core=dict(bound); core.pop("rules_sha256")
            self.assertEqual(declared,k9_engine.stable(core))
            for key in (
                "min_words","min_paragraphs","min_h2","min_table_body_rows",
                "min_fact_pack_coverage_ratio","min_trace_lexical_support_ratio",
                "max_duplicate_sentence_ratio","max_intro_pair_similarity",
            ):
                self.assertIn(key,bound["global_requirements"])
        contracts=json.loads(self.text("contracts/K9_WORKER_CONTRACTS.json"))["contracts"]
        self.assertIn("PPM679_AUTHORING_RULES",contracts["write"]["input_rule"])
        self.assertIn("PPM679_AUTHORING_RULES",contracts["repair"]["input_rule"])

    def test_all_chat_switch_sensitive_states_are_route_locked(self):
        engine=self.text("k9_engine.py")
        finalizer=self.text(".github/workflows/k9-finalize.yml")
        self.assertIn('"route_lock": "SYSTEM_ROUTING_ONLY"',engine)
        self.assertIn('"repair_authorized": False',engine)
        for required in (
            "FINALIZER_BLOCKER_REPORT_ONLY",
            "REPORT_FINALIZER_BLOCKER_TO_USER_ONLY",
            "'repair_authorized':False",
            "'code_change_allowed':False",
            "'operational_mode':'TERMINAL_CHAT_DELIVERY_ONLY'",
            "'route_lock':'TERMINAL_CHAT_DELIVERY_ONLY'",
        ):
            self.assertIn(required,finalizer)

    def test_wordpress_delivery_is_actual_02827_import_contract(self):
        exporter=self.text("k9_wordpress_export.py")
        finalizer=self.text(".github/workflows/k9-finalize.yml")
        self.assertIn('CONTRACT="SYSTEM4_WORDPRESS_HANDOFF_V1"',exporter)
        self.assertIn('PLUGIN_VERSION="0.28.27"',exporter)
        self.assertIn("K9_WORDPRESS_DIRECT_IMPORT_",finalizer)
        self.assertIn("k9-wordpress-direct-import",finalizer)
        self.assertNotIn("name: k9-wordpress-final-json",finalizer)
        self.assertIn("'wordpress_contract':'SYSTEM4_WORDPRESS_HANDOFF_V1'",finalizer)

    def test_finalizer_keeps_all_real_gates_and_mandates_chat_file(self):
        wf=self.text(".github/workflows/k9-finalize.yml")
        for required in (
            "k9_pserc.py",
            "k9_endstempel.py build",
            "k9_endstempel.py verify",
            "k9_wordpress_verify.py",
            "runtime/CHAT_DELIVERY.json",
            "DELIVER_FINAL_WORDPRESS_FILE_IN_CHAT",
            "k9-wordpress-direct-import",
            "SYSTEM4_WORDPRESS_HANDOFF_V1",
            "actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02",
        ):
            self.assertIn(required,wf)

if __name__=="__main__":
    unittest.main()
