import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import full_workflow_gate
import intake_bridge
import production_bridge
import progress_guard
import universal_reentry_guard


class CurrentProductionGuardTests(unittest.TestCase):
    def test_own_domain_is_always_forbidden(self):
        self.assertTrue(intake_bridge._forbidden_research_url("https://pferde-atelier.de/test"))
        self.assertTrue(intake_bridge._forbidden_research_url("https://www.pferde-atelier.de/test"))
        self.assertTrue(production_bridge._forbidden_own_domain("https://pferde-atelier.de/"))
        self.assertFalse(intake_bridge._forbidden_research_url("https://example.org/test"))

    def _binding(self, count=2):
        items = []
        for i in range(count):
            slot = hashlib.sha256(f"slot-{i}".encode()).hexdigest()
            source_pool = hashlib.sha256(f"sources-{i}".encode()).hexdigest()
            items.append({
                "item_index": i,
                "identity": {
                    "item_index": i,
                    "title": f"Artikel {i}",
                    "target_keyword": f"Keyword {i}",
                    "category": f"kategorie-{i}",
                    "article_type": "FAQ" if i % 2 else "Beratung",
                    "plan_slot": slot,
                    "identity_sha256": hashlib.sha256(f"identity-{i}".encode()).hexdigest(),
                },
                "research_bound": {
                    "item_index": i,
                    "plan_slot": slot,
                    "source_pool_sha256": source_pool,
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

    def _decision(self, binding, state):
        return universal_reentry_guard.build(binding, state)

    def _draft(self, root, binding, index, text=None):
        slot = binding["items"][index]["identity"]["plan_slot"]
        path = root / f"{index:02d}_{slot}.md"
        path.write_text(text or f"draft-{index}", encoding="utf-8")
        return path

    def _pass_article(self, binding, state, root, index):
        decision = self._decision(binding, state)
        draft = self._draft(root, binding, index, f"article-{index}-v1")
        state = progress_guard.record_draft(binding, state, decision, index, draft)

        decision = self._decision(binding, state)
        sha = progress_guard.file_sha(draft)
        state = progress_guard.record_check(
            binding, state, decision, index, "LT68",
            {"status": "PASS", "content_sha256": sha}, draft
        )

        decision = self._decision(binding, state)
        state = progress_guard.record_check(
            binding, state, decision, index, "PPM679",
            {"status": "PASS", "content_sha256": sha}, draft
        )
        return state, draft

    def test_proven_outer_route_matrix_has_no_free_stage_choice(self):
        with tempfile.TemporaryDirectory() as td:
            proof = full_workflow_gate.simulate_route_matrix(Path(td))
        self.assertEqual(proof["status"], "PASS")
        self.assertEqual(proof["positive_count"], len(full_workflow_gate.STAGES) + 1)
        self.assertEqual(proof["negative_count"], len(full_workflow_gate.STAGES) + 1)
        self.assertNotIn("CHAT_FILE_RETURN", full_workflow_gate.STAGES)
        self.assertEqual(
            full_workflow_gate.STAGE_ROUTES["ARTICLE_PRODUCTION"]["entry_ref"],
            "concept_agent/progress_guard.py",
        )
        self.assertNotIn("resumable_runner", json.dumps(full_workflow_gate.STAGE_ROUTES))

    def test_resume_requires_exact_universal_reentry_decision(self):
        binding = self._binding()
        state = self._checkpoint(binding)
        decision = self._decision(binding, state)
        result = progress_guard.resume(binding, state, decision)
        self.assertEqual(result["allowed_action"]["action"], "WRITE_DRAFT")
        self.assertEqual(result["bound_worker"], "BOUND_CHAT_WORKER")
        self.assertEqual(result["process_trigger"]["worker"], "BOUND_CHAT_WORKER")
        self.assertEqual(result["process_trigger"]["allowed_action"], result["allowed_action"])
        self.assertEqual(result["process_trigger"]["checkpoint_sha256"], state["checkpoint_sha256"])
        self.assertEqual(result["process_trigger"]["bound_work_item"], binding["items"][0])
        self.assertEqual(result["process_trigger"]["bound_work_item"]["item_index"], 0)
        self.assertEqual(
            result["process_trigger"]["bound_work_item"]["identity"]["plan_slot"],
            result["allowed_action"]["plan_slot"],
        )
        self.assertIs(result["process_trigger"]["exactly_once_for_checkpoint"], True)
        self.assertIs(result["process_trigger"]["return_required"], True)
        trigger_core = {
            "batch_sha256": result["process_trigger"]["batch_sha256"],
            "checkpoint_sha256": result["process_trigger"]["checkpoint_sha256"],
            "worker": result["process_trigger"]["worker"],
            "allowed_action": result["process_trigger"]["allowed_action"],
            "return_to": result["process_trigger"]["return_to"],
            "bound_work_item": result["process_trigger"]["bound_work_item"],
        }
        self.assertEqual(result["process_trigger"]["trigger_sha256"], progress_guard.stable(trigger_core))
        self.assertIs(result["continuation_required"], True)
        self.assertIs(result["worker_must_execute_allowed_action_immediately"], True)
        self.assertIs(result["worker_return_must_reenter_progress_guard"], True)
        self.assertIs(result["terminal"], False)
        self.assertEqual(decision["outer_stage"], "ARTICLE_PRODUCTION")

        with self.assertRaisesRegex(progress_guard.Blocked, "REENTRY_DECISION_CONTRACT_INVALID"):
            progress_guard.resume(binding, state, {})

        tampered = json.loads(json.dumps(decision))
        tampered["allowed_action"]["item_index"] = 1
        core = dict(tampered)
        core.pop("decision_sha256", None)
        tampered["decision_sha256"] = progress_guard.stable(core)
        with self.assertRaisesRegex(progress_guard.Blocked, "REENTRY_DECISION_ACTION_MISMATCH"):
            progress_guard.resume(binding, state, tampered)

    def test_write_trigger_exposes_only_checkpoint_selected_bound_work_item(self):
        binding = self._binding(2)
        state = self._checkpoint(binding)
        decision = self._decision(binding, state)
        result = progress_guard.resume(binding, state, decision)
        payload = result["process_trigger"]["bound_work_item"]
        self.assertEqual(payload, binding["items"][0])
        self.assertNotEqual(payload, binding["items"][1])
        self.assertEqual(payload["identity"]["plan_slot"], state["allowed_action"]["plan_slot"])

    def test_stale_decision_dies_immediately_after_checkpoint_changes(self):
        binding = self._binding()
        state = self._checkpoint(binding)
        stale = self._decision(binding, state)
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            draft = self._draft(root, binding, 0)
            state2 = progress_guard.record_draft(binding, state, stale, 0, draft)
            with self.assertRaisesRegex(progress_guard.Blocked, "REENTRY_DECISION_CHECKPOINT_MISMATCH"):
                progress_guard.resume(binding, state2, stale)

    def test_only_checkpoint_selected_article_can_enter(self):
        binding = self._binding()
        state = self._checkpoint(binding)
        decision = self._decision(binding, state)
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            draft1 = self._draft(root, binding, 1)
            with self.assertRaisesRegex(progress_guard.Blocked, "RECORD_DRAFT_NOT_ALLOWED"):
                progress_guard.record_draft(binding, state, decision, 1, draft1)

    def test_draft_bytes_are_durable_and_recoverable_after_local_file_loss(self):
        binding = self._binding()
        state = self._checkpoint(binding)
        decision = self._decision(binding, state)
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            draft = self._draft(root, binding, 0, "exact-current-article-bytes")
            state2 = progress_guard.record_draft(binding, state, decision, 0, draft)
            self.assertEqual(state2["drafts"][0]["content_utf8"], "exact-current-article-bytes")
            expected = state2["drafts"][0]["draft_sha256"]
            draft.unlink()

            decision2 = self._decision(binding, state2)
            restored_dir = root / "restored"
            result = progress_guard.materialize_current_draft(binding, state2, decision2, restored_dir)
            restored = Path(result["path"])
            self.assertTrue(restored.is_file())
            self.assertEqual(progress_guard.file_sha(restored), expected)
            self.assertEqual(restored.read_text(encoding="utf-8"), "exact-current-article-bytes")

    def test_tampered_durable_article_bytes_invalidate_checkpoint(self):
        binding = self._binding()
        state = self._checkpoint(binding)
        decision = self._decision(binding, state)
        with tempfile.TemporaryDirectory() as td:
            draft = self._draft(Path(td), binding, 0, "original")
            state2 = progress_guard.record_draft(binding, state, decision, 0, draft)

        broken = json.loads(json.dumps(state2))
        broken["drafts"][0]["content_utf8"] = "tampered"
        core = dict(broken)
        core.pop("checkpoint_sha256", None)
        broken["checkpoint_sha256"] = progress_guard.stable(core)
        with self.assertRaisesRegex(progress_guard.Blocked, "CHECKPOINT_DRAFT_HASH_MISMATCH"):
            self._decision(binding, broken)

    def test_lt_then_ppm_order_is_forced(self):
        binding = self._binding()
        state = self._checkpoint(binding)
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            decision = self._decision(binding, state)
            draft = self._draft(root, binding, 0)
            state = progress_guard.record_draft(binding, state, decision, 0, draft)
            sha = progress_guard.file_sha(draft)
            decision = self._decision(binding, state)

            with self.assertRaisesRegex(progress_guard.Blocked, "RECORD_CHECK_NOT_ALLOWED"):
                progress_guard.record_check(
                    binding, state, decision, 0, "PPM679",
                    {"status": "PASS", "content_sha256": sha}, draft
                )

            state = progress_guard.record_check(
                binding, state, decision, 0, "LT68",
                {"status": "PASS", "content_sha256": sha}, draft
            )
            self.assertEqual(state["phase"], "PPM679_REQUIRED")
            self.assertEqual(self._decision(binding, state)["allowed_action"]["checker"], "PPM679")

    def test_repair_stays_same_article_and_returns_to_lt(self):
        binding = self._binding()
        state = self._checkpoint(binding)
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            decision = self._decision(binding, state)
            draft = self._draft(root, binding, 0, "before-repair")
            state = progress_guard.record_draft(binding, state, decision, 0, draft)
            sha = progress_guard.file_sha(draft)

            decision = self._decision(binding, state)
            state = progress_guard.record_check(
                binding, state, decision, 0, "LT68",
                {"status": "REPAIR_REQUIRED", "content_sha256": sha, "findings": [{"code": "x"}]},
                draft,
            )
            self.assertEqual(state["phase"], "REPAIR_REQUIRED")
            self.assertEqual(state["next_item_index"], 0)

            decision = self._decision(binding, state)
            draft.write_text("after-repair", encoding="utf-8")
            state = progress_guard.replace_draft(binding, state, decision, 0, draft)
            self.assertEqual(state["phase"], "LT68_REQUIRED")
            self.assertEqual(state["next_item_index"], 0)
            self.assertEqual(state["allowed_action"]["checker"], "LT68")
            self.assertEqual(state["drafts"][0]["content_utf8"], "after-repair")

    def test_all_articles_then_pserc_endstempel_stop(self):
        binding = self._binding(2)
        state = self._checkpoint(binding)
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            state, _ = self._pass_article(binding, state, root, 0)
            self.assertEqual(state["phase"], "AUTHORING_REQUIRED")
            state, _ = self._pass_article(binding, state, root, 1)

        self.assertEqual(state["phase"], "ALL_ARTICLES_LT_PPM_PASS")
        decision = self._decision(binding, state)
        self.assertEqual(decision["outer_stage"], "PSERC_PACKAGE")
        self.assertEqual(decision["allowed_action"]["action"], "RUN_PSERC")

        pserc = {
            "contract": progress_guard.BATCH_STAGE_RESULT_CONTRACT,
            "stage": "PSERC",
            "status": "PASS",
            "batch_sha256": binding["batch_sha256"],
            "source_checkpoint_sha256": state["checkpoint_sha256"],
            "evidence_sha256": hashlib.sha256(b"pserc-evidence").hexdigest(),
            "pserc_package_sha256": hashlib.sha256(b"pserc-package").hexdigest(),
            "publish_allowed": False,
        }
        state = progress_guard.record_batch_stage(binding, state, decision, "PSERC", pserc)

        decision = self._decision(binding, state)
        self.assertEqual(decision["outer_stage"], "ENDSTEMPEL")
        self.assertEqual(decision["allowed_action"]["action"], "RUN_ENDSTEMPEL")
        end = {
            "contract": progress_guard.BATCH_STAGE_RESULT_CONTRACT,
            "stage": "ENDSTEMPEL",
            "status": "PASS",
            "batch_sha256": binding["batch_sha256"],
            "source_checkpoint_sha256": state["checkpoint_sha256"],
            "evidence_sha256": hashlib.sha256(b"end-evidence").hexdigest(),
            "final_file_sha256": hashlib.sha256(b"final-file").hexdigest(),
            "publish_allowed": False,
        }
        state = progress_guard.record_batch_stage(binding, state, decision, "ENDSTEMPEL", end)

        decision = self._decision(binding, state)
        self.assertEqual(decision["outer_stage"], "COMPLETE")
        self.assertEqual(decision["allowed_action"]["action"], "STOP")
        result = progress_guard.resume(binding, state, decision)
        self.assertEqual(result["allowed_action"]["action"], "STOP")
        self.assertEqual(result["status"], "STOP")
        self.assertIsNone(result["process_trigger"])
        self.assertIs(result["continuation_required"], False)
        self.assertIs(result["worker_must_execute_allowed_action_immediately"], False)
        self.assertIs(result["worker_return_must_reenter_progress_guard"], False)
        self.assertIs(result["terminal"], True)

    def test_missing_or_wrong_checkpoint_stops_before_decision(self):
        binding = self._binding()
        state = self._checkpoint(binding)

        wrong_batch = dict(state)
        wrong_batch["batch_sha256"] = "0" * 64
        core = dict(wrong_batch)
        core.pop("checkpoint_sha256", None)
        wrong_batch["checkpoint_sha256"] = progress_guard.stable(core)
        with self.assertRaisesRegex(progress_guard.Blocked, "CHECKPOINT_BATCH_MISMATCH"):
            self._decision(binding, wrong_batch)

        broken = dict(state)
        broken["checkpoint_sha256"] = "0" * 64
        with self.assertRaisesRegex(progress_guard.Blocked, "CHECKPOINT_HASH_MISMATCH"):
            self._decision(binding, broken)


if __name__ == "__main__":
    unittest.main(verbosity=2)
