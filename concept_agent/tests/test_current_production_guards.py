import hashlib
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import intake_bridge
import production_bridge
import progress_guard


class CurrentProductionGuardTests(unittest.TestCase):
    def test_own_domain_is_always_forbidden(self):
        self.assertTrue(intake_bridge._forbidden_research_url("https://pferde-atelier.de/test"))
        self.assertTrue(intake_bridge._forbidden_research_url("https://www.pferde-atelier.de/test"))
        self.assertTrue(production_bridge._forbidden_own_domain("https://pferde-atelier.de/"))
        self.assertFalse(intake_bridge._forbidden_research_url("https://example.org/test"))

    def _binding(self):
        rows = []
        for i in range(2):
            slot = hashlib.sha256(f"slot-{i}".encode()).hexdigest()
            rows.append({
                "item_index": i,
                "identity": {"plan_slot": slot},
            })
        binding = {
            "contract": progress_guard.BINDING_CONTRACT,
            "batch_sha256": hashlib.sha256(b"batch").hexdigest(),
            "item_count": 2,
            "items": rows,
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

    def _draft(self, root, binding, index, text=None):
        slot = binding["items"][index]["identity"]["plan_slot"]
        path = root / f"{index:02d}_{slot}.md"
        path.write_text(text or f"draft-{index}", encoding="utf-8")
        return path

    def test_resume_requires_exact_hash_bound_allowed_action(self):
        binding = self._binding()
        state = self._checkpoint(binding)
        result = progress_guard.resume(binding, state)
        self.assertEqual(result["allowed_action"]["action"], "WRITE_DRAFT")
        self.assertEqual(result["allowed_action"]["item_index"], 0)

        tampered = dict(state)
        tampered["allowed_action"] = dict(state["allowed_action"], item_index=1)
        tampered["checkpoint_sha256"] = progress_guard.stable(
            {k: v for k, v in tampered.items() if k != "checkpoint_sha256"}
        )
        with self.assertRaisesRegex(progress_guard.Blocked, "CHECKPOINT_ALLOWED_ACTION_MISMATCH"):
            progress_guard.resume(binding, tampered)

        old_style = dict(state)
        old_style.pop("allowed_action")
        old_style["checkpoint_sha256"] = progress_guard.stable(
            {k: v for k, v in old_style.items() if k != "checkpoint_sha256"}
        )
        with self.assertRaisesRegex(progress_guard.Blocked, "CHECKPOINT_ALLOWED_ACTION_MISMATCH"):
            progress_guard.resume(binding, old_style)

    def test_batch_attach_is_hard_blocked(self):
        binding = self._binding()
        state = self._checkpoint(binding)
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaisesRegex(progress_guard.Blocked, "BATCH_DRAFT_ATTACH_FORBIDDEN"):
                progress_guard.attach_drafts(binding, state, Path(td))

    def test_only_checkpoint_selected_article_can_enter(self):
        binding = self._binding()
        state = self._checkpoint(binding)
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            draft0 = self._draft(root, binding, 0)
            draft1 = self._draft(root, binding, 1)

            with self.assertRaisesRegex(progress_guard.Blocked, "RECORD_DRAFT_NOT_ALLOWED"):
                progress_guard.record_draft(binding, state, 1, draft1)

            state2 = progress_guard.record_draft(binding, state, 0, draft0)
            self.assertEqual(state2["phase"], "LT68_REQUIRED")
            self.assertEqual(state2["allowed_action"]["checker"], "LT68")
            self.assertEqual(state2["allowed_action"]["item_index"], 0)

    def test_checkpoint_chain_and_checker_order(self):
        binding = self._binding()
        state = self._checkpoint(binding)
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            draft0 = self._draft(root, binding, 0)
            state2 = progress_guard.record_draft(binding, state, 0, draft0)
            self.assertEqual(state2["previous_checkpoint_sha256"], state["checkpoint_sha256"])

            sha0 = progress_guard.file_sha(draft0)
            with self.assertRaisesRegex(progress_guard.Blocked, "RECORD_CHECK_NOT_ALLOWED"):
                progress_guard.record_check(
                    binding, state2, 0, "PPM679",
                    {"status": "PASS", "content_sha256": sha0}, draft0
                )

            state3 = progress_guard.record_check(
                binding, state2, 0, "LT68",
                {"status": "PASS", "content_sha256": sha0}, draft0
            )
            self.assertEqual(state3["phase"], "PPM679_REQUIRED")
            self.assertEqual(state3["allowed_action"]["checker"], "PPM679")

            state4 = progress_guard.record_check(
                binding, state3, 0, "PPM679",
                {"status": "PASS", "content_sha256": sha0}, draft0
            )
            self.assertEqual(state4["next_item_index"], 1)
            self.assertEqual(state4["phase"], "AUTHORING_REQUIRED")
            self.assertEqual(state4["allowed_action"]["action"], "WRITE_DRAFT")
            self.assertEqual(state4["allowed_action"]["item_index"], 1)
            self.assertEqual(state4["completed_items"][0]["ppm679"], "PASS")

    def test_repair_cannot_advance_article(self):
        binding = self._binding()
        state = self._checkpoint(binding)
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            draft0 = self._draft(root, binding, 0)
            state = progress_guard.record_draft(binding, state, 0, draft0)
            sha0 = progress_guard.file_sha(draft0)
            repair = {
                "status": "REPAIR_REQUIRED",
                "content_sha256": sha0,
                "findings": [{"code": "x"}],
            }
            state = progress_guard.record_check(binding, state, 0, "LT68", repair, draft0)
            self.assertEqual(state["phase"], "REPAIR_REQUIRED")
            self.assertEqual(state["next_item_index"], 0)
            self.assertEqual(state["allowed_action"]["action"], "REPAIR_DRAFT")
            self.assertEqual(state["allowed_action"]["item_index"], 0)

            draft0.write_text("repaired-draft-0", encoding="utf-8")
            state = progress_guard.replace_draft(binding, state, 0, draft0)
            self.assertEqual(state["phase"], "LT68_REQUIRED")
            self.assertEqual(state["next_item_index"], 0)
            self.assertEqual(state["allowed_action"]["checker"], "LT68")

    def test_missing_or_wrong_checkpoint_stops_resume(self):
        binding = self._binding()
        state = self._checkpoint(binding)

        wrong_batch = dict(state)
        wrong_batch["batch_sha256"] = "0" * 64
        wrong_batch["checkpoint_sha256"] = progress_guard.stable(
            {k: v for k, v in wrong_batch.items() if k != "checkpoint_sha256"}
        )
        with self.assertRaisesRegex(progress_guard.Blocked, "CHECKPOINT_BATCH_MISMATCH"):
            progress_guard.resume(binding, wrong_batch)

        broken = dict(state)
        broken["checkpoint_sha256"] = "0" * 64
        with self.assertRaisesRegex(progress_guard.Blocked, "CHECKPOINT_HASH_MISMATCH"):
            progress_guard.resume(binding, broken)


if __name__ == "__main__":
    unittest.main(verbosity=2)
