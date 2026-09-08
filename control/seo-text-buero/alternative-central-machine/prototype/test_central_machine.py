import unittest

from central_machine import Blocked, CentralMachine, STEP_ORDER, make_result


class P0CentralMachineTests(unittest.TestCase):
    def good_research(self, m):
        wi = m.worker_input()
        self.assertEqual(wi["step_id"], "RESEARCH")
        m.submit(make_result(wi, {"item_id": wi["payload"]["item_id"], "facts": ["f1", "f2"]}))

    def good_text(self, m):
        wi = m.worker_input()
        self.assertEqual(wi["step_id"], "TEXT_SLOT")
        m.submit(make_result(wi, {
            "item_id": wi["payload"]["item_id"],
            "facts": wi["payload"]["facts"],
            "draft": "Draft",
        }))

    def good_final(self, m):
        wi = m.worker_input()
        self.assertEqual(wi["step_id"], "FINAL_CHECK")
        m.submit(make_result(wi, {
            "item_id": wi["payload"]["item_id"],
            "facts": wi["payload"]["facts"],
            "draft": wi["payload"]["draft"],
            "checks": {"all_required_checks_passed": True},
        }))

    def test_positive_exact_three_step_flow(self):
        m = CentralMachine("JOB-1", "ITEM-1")
        self.good_research(m)
        self.good_text(m)
        self.good_final(m)
        self.assertTrue(m.finished)
        self.assertEqual([x["step_id"] for x in m.snapshot()["history"]], list(STEP_ORDER))

    def test_negative_caller_cannot_supply_validator(self):
        m = CentralMachine("JOB-1", "ITEM-1")
        wi = m.worker_input()
        result = make_result(wi, {"item_id": "ITEM-1", "facts": ["f1"]})
        with self.assertRaises(TypeError):
            m.submit(result, lambda _: True)

    def test_negative_worker_cannot_skip_step(self):
        m = CentralMachine("JOB-1", "ITEM-1")
        wi = m.worker_input()
        result = make_result(wi, {"item_id": "ITEM-1", "facts": ["f1"]})
        result["step_id"] = "FINAL_CHECK"
        with self.assertRaisesRegex(Blocked, "STEP_ID_MISMATCH"):
            m.submit(result)

    def test_negative_worker_cannot_inject_next_step(self):
        m = CentralMachine("JOB-1", "ITEM-1")
        wi = m.worker_input()
        result = make_result(wi, {"item_id": "ITEM-1", "facts": ["f1"]})
        result["next_step"] = "FINAL_CHECK"
        with self.assertRaisesRegex(Blocked, "RESULT_SCHEMA_INVALID"):
            m.submit(result)

    def test_negative_wrong_job_is_blocked(self):
        m = CentralMachine("JOB-1", "ITEM-1")
        wi = m.worker_input()
        result = make_result(wi, {"item_id": "ITEM-1", "facts": ["f1"]})
        result["job_id"] = "OTHER"
        with self.assertRaisesRegex(Blocked, "JOB_ID_MISMATCH"):
            m.submit(result)

    def test_negative_wrong_item_is_blocked(self):
        m = CentralMachine("JOB-1", "ITEM-1")
        wi = m.worker_input()
        result = make_result(wi, {"item_id": "ITEM-2", "facts": ["f1"]})
        with self.assertRaisesRegex(Blocked, "ITEM_ID_MISMATCH|VALIDATOR_FAIL"):
            m.submit(result)

    def test_negative_input_hash_tampering_is_blocked(self):
        m = CentralMachine("JOB-1", "ITEM-1")
        wi = m.worker_input()
        result = make_result(wi, {"item_id": "ITEM-1", "facts": ["f1"]})
        result["input_hash"] = "0" * 64
        with self.assertRaisesRegex(Blocked, "INPUT_HASH_MISMATCH"):
            m.submit(result)

    def test_negative_output_tampering_is_blocked(self):
        m = CentralMachine("JOB-1", "ITEM-1")
        wi = m.worker_input()
        result = make_result(wi, {"item_id": "ITEM-1", "facts": ["f1"]})
        result["output"]["facts"].append("tampered")
        with self.assertRaisesRegex(Blocked, "OUTPUT_HASH_MISMATCH"):
            m.submit(result)

    def test_negative_extra_rule_field_is_blocked(self):
        m = CentralMachine("JOB-1", "ITEM-1")
        wi = m.worker_input()
        result = make_result(wi, {
            "item_id": "ITEM-1",
            "facts": ["f1"],
            "disable_link_rule": True,
        })
        with self.assertRaisesRegex(Blocked, "VALIDATOR_FAIL"):
            m.submit(result)

    def test_negative_worker_fail_blocks_machine(self):
        m = CentralMachine("JOB-1", "ITEM-1")
        wi = m.worker_input()
        result = make_result(wi, {"item_id": "ITEM-1", "facts": ["f1"]}, status="FAIL")
        with self.assertRaisesRegex(Blocked, "WORKER_NONPASS"):
            m.submit(result)
        self.assertIsNone(m.current_step)

    def test_negative_final_check_cannot_claim_partial_pass(self):
        m = CentralMachine("JOB-1", "ITEM-1")
        self.good_research(m)
        self.good_text(m)
        wi = m.worker_input()
        result = make_result(wi, {
            "item_id": "ITEM-1",
            "facts": wi["payload"]["facts"],
            "draft": wi["payload"]["draft"],
            "checks": {"all_required_checks_passed": False},
        })
        with self.assertRaisesRegex(Blocked, "VALIDATOR_FAIL"):
            m.submit(result)

    def test_positive_no_fixed_article_count(self):
        for i in range(1000):
            m = CentralMachine(f"JOB-{i}", f"ITEM-{i}")
            self.good_research(m)
            self.good_text(m)
            self.good_final(m)
            self.assertTrue(m.finished)


if __name__ == "__main__":
    unittest.main(verbosity=2)
