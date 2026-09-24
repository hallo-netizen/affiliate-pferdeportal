import hashlib
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "concept_agent"))

import full_workflow_gate as fw
import progress_guard as pg
import universal_reentry_guard as urg

class InterruptionReturnToStartTests(unittest.TestCase):
    def test_every_outer_interruption_returns_to_start_and_fast_forwards_only_verified_work(self):
        batch = hashlib.sha256(b"konzept5-interruption-matrix").hexdigest()
        for completed in range(len(fw.STAGES) + 1):
            with self.subTest(completed=completed):
                state = fw.build_to(batch, 5, completed)
                proof = fw.enter(state)
                self.assertEqual(proof["workflow_entry"], "ALWAYS_FROM_STAGE_0")
                self.assertEqual(proof["fast_forward_mode"], "VALIDATE_ONLY")
                self.assertEqual(proof["validated_completed_stages"], fw.STAGES[:completed])
                expected = fw.STAGES[completed] if completed < len(fw.STAGES) else "COMPLETE"
                self.assertEqual(proof["next_stage"], expected)
                ticket = fw.stage_route_from_entry_proof(proof)
                self.assertEqual(ticket["next_stage"], expected)
                self.assertIs(ticket["chat_may_choose_stage"], False)
                self.assertIs(ticket["alternate_route_allowed"], False)
                self.assertIs(ticket["publish_allowed"], False)

    def test_cannot_skip_or_choose_outer_stage(self):
        batch = hashlib.sha256(b"konzept5-no-stage-choice").hexdigest()
        for completed in range(len(fw.STAGES) - 1):
            state = fw.build_to(batch, 3, completed)
            wrong = fw.STAGES[completed + 1]
            with self.assertRaisesRegex(fw.Blocked, "STAGE_OUT_OF_ORDER"):
                fw.complete_stage(state, wrong, {
                    "batch_sha256": batch, "item_count": 3, "publish_allowed": False
                })
            proof = fw.enter(state)
            forged = json.loads(json.dumps(proof))
            forged["next_stage"] = wrong
            with self.assertRaisesRegex(fw.Blocked, "ENTRY_PROOF_HASH_MISMATCH_FOR_ROUTE"):
                fw.stage_route_from_entry_proof(forged)

    def test_control_pointer_forbids_chat_choice_write_alternate_route_second_start_and_publish(self):
        p = json.loads((ROOT / "concept_agent/CONTROL_ENTRY_POINTER.json").read_text(encoding="utf-8"))
        self.assertIs(p["chat_may_choose_stage"], False)
        self.assertIs(p["chat_may_choose_article"], False)
        self.assertIs(p["chat_may_write_authoritative_event"], False)
        self.assertIs(p["alternate_route_allowed"], False)
        self.assertIs(p["reconstruction_allowed"], False)
        self.assertIs(p["second_text_start_after_machine_ready_allowed"], False)
        self.assertIs(p["publish_allowed"], False)
        self.assertIs(p["bound_worker_may_execute_only_machine_allowed_action"], True)

    def test_resume_workflow_is_read_only_and_has_no_alternate_executor(self):
        w = (ROOT / ".github/workflows/pferde-atelier-github-batch-executor.yml").read_text(encoding="utf-8")
        self.assertIn("contents: read", w)
        self.assertIn("issues: read", w)
        self.assertNotIn("contents: write", w)
        self.assertNotIn("issues: write", w)
        self.assertFalse((ROOT / "concept_agent/github_batch_executor.py").exists())

    def test_inner_resume_rejects_tamper_and_stale_decision(self):
        binding = {
            "contract": pg.BINDING_CONTRACT,
            "batch_sha256": hashlib.sha256(b"inner-batch").hexdigest(),
            "item_count": 2,
            "publish_allowed": False,
        }
        state = pg.initial_checkpoint(binding)
        decision = urg.build(binding, state)
        urg.verify(binding, state, decision)
        result = pg.resume(binding, state, decision)
        self.assertEqual(result["allowed_action"], pg.expected_action(binding, state))
        self.assertIs(result["publish_allowed"], False)

        tampered = json.loads(json.dumps(state))
        tampered["next_item_index"] = 1
        with self.assertRaises(pg.Blocked):
            pg.resume(binding, tampered, decision)

        forged = json.loads(json.dumps(decision))
        forged["allowed_action"] = {"action": "RUN_PSERC"}
        with self.assertRaises(urg.Blocked):
            urg.verify(binding, state, forged)

if __name__ == "__main__":
    unittest.main(verbosity=2)
