import copy
import tempfile
import unittest
from pathlib import Path

from p11_workflow_contract import (
    Blocked,
    REQUIRED_STAGES,
    canonical_pass_results,
    verify_authoritative_stage_source,
    verify_stage_results,
)

class P11WorkflowContractTests(unittest.TestCase):
    def test_positive_authoritative_stage_set_exact_independent_of_order(self):
        values=list(REQUIRED_STAGES)
        values[1],values[9]=values[9],values[1]
        with tempfile.TemporaryDirectory() as td:
            source=Path(td)/"stage_source.py"
            source.write_text("STAGES="+repr(values)+"\n",encoding="utf-8")
            verify_authoritative_stage_source(source)

    def test_positive_all_twelve_exactly_once(self):
        rows=canonical_pass_results()
        verify_stage_results(rows)
        self.assertEqual(len(rows),12)
        self.assertEqual(set(r["stage"] for r in rows),set(REQUIRED_STAGES))

    def test_positive_checklist_does_not_control_runtime_order(self):
        rows=canonical_pass_results()
        rows[2],rows[10]=rows[10],rows[2]
        rows[0],rows[11]=rows[11],rows[0]
        verify_stage_results(rows)
        self.assertEqual(set(r["stage"] for r in rows),set(REQUIRED_STAGES))

    def test_negative_missing_stage(self):
        rows=canonical_pass_results()[:-1]
        with self.assertRaisesRegex(Blocked,"STAGE_COUNT_INVALID"):
            verify_stage_results(rows)

    def test_negative_duplicate_replacing_stage(self):
        rows=canonical_pass_results()
        rows[-1]=copy.deepcopy(rows[-2])
        with self.assertRaisesRegex(Blocked,"STAGE_DUPLICATE"):
            verify_stage_results(rows)

    def test_negative_unknown_stage(self):
        rows=canonical_pass_results()
        rows[-1]["stage"]="free_chat_review"
        with self.assertRaisesRegex(Blocked,"STAGE_SET_DRIFT"):
            verify_stage_results(rows)

    def test_negative_stage_fail(self):
        rows=canonical_pass_results()
        rows[4]["status"]="FAIL"
        with self.assertRaisesRegex(Blocked,"STAGE_NONPASS:languagetool"):
            verify_stage_results(rows)

    def test_negative_stage_not_executed(self):
        rows=canonical_pass_results()
        rows[5]["execution_performed"]=False
        with self.assertRaisesRegex(Blocked,"STAGE_NOT_EXECUTED:ppm"):
            verify_stage_results(rows)

    def test_negative_rule_change_claim(self):
        rows=canonical_pass_results()
        rows[1]["content_or_quality_rules_changed"]=True
        with self.assertRaisesRegex(Blocked,"RULE_CHANGE_FORBIDDEN"):
            verify_stage_results(rows)

    def test_negative_publish_allowed(self):
        rows=canonical_pass_results()
        rows[-1]["publish_allowed"]=True
        with self.assertRaisesRegex(Blocked,"PUBLISH_FORBIDDEN"):
            verify_stage_results(rows)

    def test_negative_runtime_disable_field_not_accepted(self):
        rows=canonical_pass_results()
        rows[2]["enabled"]=False
        with self.assertRaisesRegex(Blocked,"STAGE_RESULT_SCHEMA_INVALID"):
            verify_stage_results(rows)

    def test_negative_runtime_optional_field_not_accepted(self):
        rows=canonical_pass_results()
        rows[3]["optional"]=True
        with self.assertRaisesRegex(Blocked,"STAGE_RESULT_SCHEMA_INVALID"):
            verify_stage_results(rows)

if __name__=="__main__":
    unittest.main(verbosity=2)
