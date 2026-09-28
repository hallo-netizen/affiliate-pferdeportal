#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONCEPT_AGENT = HERE.parent
if str(CONCEPT_AGENT) not in sys.path:
    sys.path.insert(0, str(CONCEPT_AGENT))

import progress_guard  # type: ignore
import universal_reentry_guard  # type: ignore
import k8_command_gate as gate  # type: ignore


class K8VerbotGateTests(unittest.TestCase):
    def _binding(self, count=2):
        items = []
        for i in range(count):
            slot = hashlib.sha256(f"slot-{i}".encode()).hexdigest()
            items.append({
                "item_index": i,
                "identity": {
                    "item_index": i,
                    "title": f"Artikel {i}",
                    "target_keyword": f"Keyword {i}",
                    "category": f"kategorie-{i}",
                    "article_type": "Beratung",
                    "plan_slot": slot,
                    "identity_sha256": hashlib.sha256(f"identity-{i}".encode()).hexdigest(),
                },
                "research_bound": {
                    "item_index": i,
                    "plan_slot": slot,
                    "source_pool_sha256": hashlib.sha256(f"sources-{i}".encode()).hexdigest(),
                    "sources": [{
                        "source_id": f"s{i}",
                        "source_title": "Quelle",
                        "source_url": "https://example.org/",
                        "evidence": "Beleg",
                        "snapshot_sha256": hashlib.sha256(b"Beleg").hexdigest(),
                    }],
                },
                "bound_work_sha256": hashlib.sha256(f"work-{i}".encode()).hexdigest(),
            })
        binding = {
            "contract": progress_guard.BINDING_CONTRACT,
            "status": "AUTHORING_READY",
            "batch_sha256": hashlib.sha256(b"batch").hexdigest(),
            "item_count": count,
            "source_intake_sha256": hashlib.sha256(b"intake").hexdigest(),
            "source_research_binding_sha256": hashlib.sha256(b"research-bound").hexdigest(),
            "quality_authority": {"source": "TEST_ONLY"},
            "route_policy": {"publish_allowed": False},
            "progress_policy": {"checkpoint_required_before_every_action": True},
            "items": items,
            "publish_allowed": False,
        }
        binding["binding_sha256"] = progress_guard.stable(binding)
        return binding

    def _checkpoint(self, binding):
        state = {
            "contract": progress_guard.CHECKPOINT_CONTRACT,
            "batch_sha256": binding["batch_sha256"],
            "production_binding_sha256": binding["binding_sha256"],
            "item_count": binding["item_count"],
            "status": "IN_PROGRESS",
            "phase": "AUTHORING_REQUIRED",
            "next_item_index": 0,
            "completed_items": [],
            "current_item": None,
            "previous_checkpoint_sha256": None,
            "drafts": [],
            "publish_allowed": False,
        }
        state["allowed_action"] = progress_guard.expected_action(binding, state)
        state["checkpoint_sha256"] = progress_guard.stable(state)
        return state

    def _decision(self, binding, checkpoint):
        return universal_reentry_guard.build(binding, checkpoint)

    def test_exact_current_command_passes_without_changing_state(self):
        binding = self._binding()
        checkpoint = self._checkpoint(binding)
        before = copy.deepcopy(checkpoint)
        result = gate.admit(binding, checkpoint, gate.proposal_for(checkpoint))
        self.assertEqual(result["status"], gate.PASS)
        self.assertEqual(checkpoint, before)
        self.assertIs(result["state_changed"], False)
        self.assertEqual(result["allowed_action"], checkpoint["allowed_action"])

    def test_wrong_missing_stale_or_extra_command_keeps_exact_same_state(self):
        binding = self._binding()
        checkpoint = self._checkpoint(binding)
        before = copy.deepcopy(checkpoint)
        valid = gate.proposal_for(checkpoint)
        cases = [
            None,
            {},
            {"contract": gate.CONTRACT},
            {**valid, "checkpoint_sha256": "0" * 64},
            {**valid, "command": {"action": "RUN_PSERC", "item_count": 2}},
            {**valid, "command": {**valid["command"], "item_index": 1}},
            {**valid, "free_choice": "ANYTHING"},
            {**valid, "contract": "OTHER"},
        ]
        for proposal in cases:
            result = gate.admit(binding, checkpoint, proposal)
            self.assertEqual(result["status"], gate.BLOCKED)
            self.assertEqual(result["checkpoint_sha256"], before["checkpoint_sha256"])
            self.assertEqual(result["allowed_action"], before["allowed_action"])
            self.assertIs(result["state_changed"], False)
            self.assertIs(result["retry_same_action"], True)
            self.assertEqual(checkpoint, before)

    def test_all_known_wrong_action_names_are_ineffective(self):
        binding = self._binding()
        checkpoint = self._checkpoint(binding)
        before = copy.deepcopy(checkpoint)
        for name in ("RUN_CHECKER", "REPAIR_DRAFT", "RUN_PSERC", "RUN_ENDSTEMPEL", "STOP", "RESEARCH", "SKIP", "BACKTRACK"):
            proposal = gate.proposal_for(checkpoint)
            proposal["command"] = {"action": name}
            result = gate.admit(binding, checkpoint, proposal)
            self.assertEqual(result["status"], gate.BLOCKED, name)
            self.assertEqual(checkpoint, before, name)

    def test_existing_state_mutators_also_reject_wrong_door(self):
        binding = self._binding()
        checkpoint = self._checkpoint(binding)
        decision = self._decision(binding, checkpoint)
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            wrong_draft = root / f"01_{binding['items'][1]['identity']['plan_slot']}.md"
            wrong_draft.write_text("wrong article", encoding="utf-8")
            with self.assertRaisesRegex(progress_guard.Blocked, "RECORD_DRAFT_NOT_ALLOWED"):
                progress_guard.record_draft(binding, checkpoint, decision, 1, wrong_draft)
            with self.assertRaisesRegex(progress_guard.Blocked, "RECORD_CHECK_NOT_ALLOWED"):
                progress_guard.record_check(
                    binding, checkpoint, decision, 0, "LT68",
                    {"status": "PASS", "content_sha256": "0" * 64}, wrong_draft
                )
            with self.assertRaisesRegex(progress_guard.Blocked, "REPAIR_DRAFT_NOT_ALLOWED"):
                progress_guard.replace_draft(binding, checkpoint, decision, 0, wrong_draft)
            with self.assertRaisesRegex(progress_guard.Blocked, "PSERC_NOT_ALLOWED"):
                progress_guard.record_batch_stage(
                    binding, checkpoint, decision, "PSERC",
                    {
                        "status": "PASS",
                        "batch_sha256": checkpoint["batch_sha256"],
                        "source_checkpoint_sha256": checkpoint["checkpoint_sha256"],
                        "publish_allowed": False,
                        "evidence_sha256": "0" * 64,
                        "pserc_package_sha256": "0" * 64,
                    },
                )

    def test_damaged_authoritative_checkpoint_hard_blocks_instead_of_guessing(self):
        binding = self._binding()
        checkpoint = self._checkpoint(binding)
        bad = copy.deepcopy(checkpoint)
        bad["phase"] = "PPM679_REQUIRED"
        with self.assertRaises(progress_guard.Blocked):
            gate.admit(binding, bad, gate.proposal_for(checkpoint))

    def test_terminal_stop_requires_exact_stop_and_never_retries(self):
        binding = self._binding(1)
        draft = "done"
        draft_sha = hashlib.sha256(draft.encode()).hexdigest()
        slot = binding["items"][0]["identity"]["plan_slot"]
        state = {
            "contract": progress_guard.CHECKPOINT_CONTRACT,
            "batch_sha256": binding["batch_sha256"],
            "production_binding_sha256": binding["binding_sha256"],
            "item_count": 1,
            "status": "PASS",
            "phase": "ENDSTEMPEL_PASS_STOP",
            "next_item_index": 1,
            "completed_items": [{
                "item_index": 0,
                "plan_slot": slot,
                "draft_sha256": draft_sha,
                "revision": 1,
                "lt68": "PASS",
                "ppm679": "PASS",
            }],
            "current_item": None,
            "previous_checkpoint_sha256": "0" * 64,
            "drafts": [{
                "item_index": 0,
                "plan_slot": slot,
                "filename": f"00_{slot}.md",
                "draft_sha256": draft_sha,
                "size_bytes": len(draft.encode()),
                "content_utf8": draft,
                "revision": 1,
                "lt68": "PASS",
                "ppm679": "PASS",
            }],
            "publish_allowed": False,
        }
        state["allowed_action"] = progress_guard.expected_action(binding, state)
        state["checkpoint_sha256"] = progress_guard.stable(state)
        ok = gate.admit(binding, state, gate.proposal_for(state))
        self.assertEqual(ok["status"], gate.PASS)
        self.assertEqual(ok["allowed_action"]["action"], "STOP")
        wrong = gate.proposal_for(state)
        wrong["command"] = {"action": "WRITE_DRAFT", "item_index": 0}
        blocked = gate.admit(binding, state, wrong)
        self.assertEqual(blocked["status"], gate.BLOCKED)
        self.assertIs(blocked["retry_same_action"], False)
        self.assertEqual(blocked["allowed_action"]["action"], "STOP")


if __name__ == "__main__":
    unittest.main(verbosity=2)
