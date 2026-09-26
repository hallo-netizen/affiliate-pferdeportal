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

    def _workspace_capsule(self, binding, state):
        action = state["allowed_action"]
        if action.get("action") not in {"RUN_CHECKER", "REPAIR_DRAFT"}:
            return None
        index = int(action["item_index"])
        item = binding["items"][index]
        row = next(x for x in state["drafts"] if x["item_index"] == index)
        text = row["content_utf8"]
        research_text = "research"
        facts_text = "facts"
        fact_pack = {"facts": []}
        plan_item = {"plan_slot": item["identity"]["plan_slot"]}
        context_core = {"fact_pack": fact_pack, "production_plan_item": plan_item}
        phase = "REPAIR_REQUIRED" if action["action"] == "REPAIR_DRAFT" else "CHECK_REQUIRED"
        checks = {}
        last_error = None
        if phase == "REPAIR_REQUIRED":
            checks = {
                "status": "FAIL",
                "checked_draft_sha256": row["draft_sha256"],
            }
            last_error = "TEST_REPAIR_REQUIRED"
        article = {
            "canonical_article_id": f"article:{index}",
            "item_index": index,
            **{k: item["identity"][k] for k in ("title", "target_keyword", "category", "article_type", "plan_slot")},
        }
        inner = {
            "contract": universal_reentry_guard.STATE_CONTRACT,
            "source_snapshot_sha256": hashlib.sha256(b"current-snapshot").hexdigest(),
            "batch_sha256": binding["batch_sha256"],
            "article": article,
            "immutable_core_sha256": "",
            "publish_allowed": False,
            "phase": phase,
            "revision": row["revision"],
            "research": {"text": research_text, "sha256": hashlib.sha256(research_text.encode()).hexdigest()},
            "facts": {"text": facts_text, "sha256": hashlib.sha256(facts_text.encode()).hexdigest()},
            "production_context": {
                **context_core,
                "sha256": universal_reentry_guard.stable(context_core),
            },
            "authoring_contract": {"contract": "TEST_BOUND"},
            "draft_markdown": text,
            "draft_sha256": row["draft_sha256"],
            "checks": checks,
            "last_error": last_error,
            "release_prepared": None,
            "released": False,
        }
        inner["immutable_core_sha256"] = universal_reentry_guard.stable({
            "contract": inner["contract"],
            "source_snapshot_sha256": inner["source_snapshot_sha256"],
            "batch_sha256": inner["batch_sha256"],
            "article": inner["article"],
        })
        raw = (json.dumps(inner, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()
        file_row = {
            "path": "state.json",
            "size": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "base64": __import__("base64").b64encode(raw).decode(),
        }
        normalized = [{"path": "state.json", "size": len(raw), "sha256": file_row["sha256"]}]
        return {
            "contract": universal_reentry_guard.CAPSULE_CONTRACT,
            "status": "RECOVERY_CAPSULE_READY",
            "workspace_identity": universal_reentry_guard._capsule_identity(inner),
            "file_count": 1,
            "tree_sha256": universal_reentry_guard._tree_hash(normalized),
            "files": [file_row],
            "publish_allowed": False,
        }

    def _decision(self, binding, state):
        capsule = self._workspace_capsule(binding, state)
        return universal_reentry_guard.build(binding, state, capsule)

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
            "handoff_is_terminal": result["process_trigger"]["handoff_is_terminal"],
            "same_bound_worker_must_continue_without_return": result["process_trigger"]["same_bound_worker_must_continue_without_return"],
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

    def test_start_button_to_final_file_consumes_every_handoff_16_items(self):
        # One regression test for the complete existing handoff chain. This is test-only:
        # no production runner, route, checker, quality rule or publish behavior is added.
        door = (HERE / "START_HERE.md").read_text(encoding="utf-8")
        receiver = (HERE.parent / ".github/workflows/text-start-pferdeatelier.yml").read_text(encoding="utf-8")
        self.assertIn("niemals ein Stop oder Antwortpunkt", door)
        self.assertIn("ohne Nutzer-Zwischenmeldung unmittelbar", door)
        self.assertIn("python3 concept_agent/intake_bridge.py prepare", receiver)
        self.assertIn("CONCEPT_AGENT_INTAKE_RECEIPT.json", receiver)

        binding = self._binding(16)
        batch = binding["batch_sha256"]
        count = binding["item_count"]

        # Start-button receiver output: the active chat must consume this immediately.
        receipt = intake_bridge._start_receipt({
            "batch_sha256": batch,
            "item_count": count,
            "intake_sha256": binding["source_intake_sha256"],
        })
        self.assertEqual(receipt["status"], "CONCEPT_AGENT_INTAKE_READY")
        self.assertEqual(receipt["bound_worker"], "BOUND_CHAT_WORKER")
        self.assertIs(receipt["continuation_required"], True)
        self.assertIs(receipt["worker_must_execute_allowed_operation_immediately"], True)
        self.assertIs(receipt["worker_return_must_reenter_full_workflow_gate"], True)
        self.assertIs(receipt["handoff_is_terminal"], False)
        self.assertIs(receipt["same_bound_worker_must_continue_without_return"], True)
        self.assertEqual(receipt["process_trigger"]["fresh_batch_first_action"], "RESEARCH_REQUIRED")
        self.assertEqual(receipt["process_trigger"]["worker"], "BOUND_CHAT_WORKER")
        self.assertIs(receipt["process_trigger"]["return_required"], True)

        consumed_handoffs = ["START:RESEARCH_REQUIRED"]

        # Consume every existing outer-stage handoff, not just assert that a trigger exists.
        outer = full_workflow_gate.initial_state(batch, count)
        outer = full_workflow_gate.complete_stage(
            outer, "INTAKE", full_workflow_gate.payload_for("INTAKE", outer)
        )

        def consume_outer(expected_stage):
            nonlocal outer
            proof = full_workflow_gate.enter(outer)
            route = full_workflow_gate.stage_route_from_entry_proof(proof)
            self.assertEqual(route["next_stage"], expected_stage)
            self.assertEqual(route["bound_worker"], "BOUND_CHAT_WORKER")
            self.assertIs(route["continuation_required"], True)
            self.assertIs(route["worker_must_execute_allowed_operation_immediately"], True)
            self.assertIs(route["worker_return_must_reenter_full_workflow_gate"], True)
            self.assertIs(route["handoff_is_terminal"], False)
            self.assertIs(route["same_bound_worker_must_continue_without_return"], True)
            self.assertIsNotNone(route["process_trigger"])
            self.assertEqual(route["process_trigger"]["worker"], "BOUND_CHAT_WORKER")
            self.assertIs(route["process_trigger"]["return_required"], True)
            consumed_handoffs.append("OUTER:" + expected_stage)
            return route

        consume_outer("RESEARCH")
        outer = full_workflow_gate.complete_stage(
            outer, "RESEARCH", full_workflow_gate.payload_for("RESEARCH", outer)
        )
        consume_outer("RESEARCH_BOUND")
        outer = full_workflow_gate.complete_stage(
            outer, "RESEARCH_BOUND", full_workflow_gate.payload_for("RESEARCH_BOUND", outer)
        )
        consume_outer("AUTHORING_BOUND")
        outer = full_workflow_gate.complete_stage(
            outer, "AUTHORING_BOUND", full_workflow_gate.payload_for("AUTHORING_BOUND", outer)
        )
        consume_outer("ARTICLE_PRODUCTION")

        state = self._checkpoint(binding)
        progress_actions = []

        with tempfile.TemporaryDirectory() as td:
            root = Path(td)

            def consume_progress(expected_action, expected_checker=None):
                decision = self._decision(binding, state)
                result = progress_guard.resume(binding, state, decision)
                self.assertEqual(result["status"], "RESUME_ALLOWED")
                self.assertEqual(result["bound_worker"], "BOUND_CHAT_WORKER")
                self.assertEqual(result["allowed_action"]["action"], expected_action)
                if expected_checker is not None:
                    self.assertEqual(result["allowed_action"].get("checker"), expected_checker)
                self.assertIs(result["continuation_required"], True)
                self.assertIs(result["worker_must_execute_allowed_action_immediately"], True)
                self.assertIs(result["worker_return_must_reenter_progress_guard"], True)
                self.assertIs(result["handoff_is_terminal"], False)
                self.assertIs(result["same_bound_worker_must_continue_without_return"], True)
                self.assertIsNotNone(result["process_trigger"])
                self.assertEqual(result["process_trigger"]["worker"], "BOUND_CHAT_WORKER")
                self.assertEqual(result["process_trigger"]["allowed_action"], result["allowed_action"])
                self.assertIs(result["process_trigger"]["exactly_once_for_checkpoint"], True)
                self.assertIs(result["process_trigger"]["return_required"], True)
                progress_actions.append(
                    expected_action + (":" + expected_checker if expected_checker else "")
                )
                consumed_handoffs.append("PROGRESS:" + progress_actions[-1])
                return decision, result

            # Article 0: prove both backward paths and automatic re-check continuation.
            decision, result = consume_progress("WRITE_DRAFT")
            self.assertEqual(result["process_trigger"]["bound_work_item"], binding["items"][0])
            draft = self._draft(root, binding, 0, "article-0-v1")
            state = progress_guard.record_draft(binding, state, decision, 0, draft)

            decision, _ = consume_progress("RUN_CHECKER", "LT68")
            sha = progress_guard.file_sha(draft)
            state = progress_guard.record_check(
                binding, state, decision, 0, "LT68",
                {"status": "REPAIR_REQUIRED", "content_sha256": sha, "findings": [{"code": "lt"}]},
                draft,
            )

            decision, _ = consume_progress("REPAIR_DRAFT", "LT68")
            draft.write_text("article-0-v2", encoding="utf-8")
            state = progress_guard.replace_draft(binding, state, decision, 0, draft)

            decision, _ = consume_progress("RUN_CHECKER", "LT68")
            sha = progress_guard.file_sha(draft)
            state = progress_guard.record_check(
                binding, state, decision, 0, "LT68",
                {"status": "PASS", "content_sha256": sha}, draft,
            )

            decision, _ = consume_progress("RUN_CHECKER", "PPM679")
            state = progress_guard.record_check(
                binding, state, decision, 0, "PPM679",
                {"status": "REPAIR_REQUIRED", "content_sha256": sha, "findings": [{"code": "ppm"}]},
                draft,
            )

            decision, _ = consume_progress("REPAIR_DRAFT", "PPM679")
            draft.write_text("article-0-v3", encoding="utf-8")
            state = progress_guard.replace_draft(binding, state, decision, 0, draft)

            decision, _ = consume_progress("RUN_CHECKER", "LT68")
            sha = progress_guard.file_sha(draft)
            state = progress_guard.record_check(
                binding, state, decision, 0, "LT68",
                {"status": "PASS", "content_sha256": sha}, draft,
            )

            decision, _ = consume_progress("RUN_CHECKER", "PPM679")
            state = progress_guard.record_check(
                binding, state, decision, 0, "PPM679",
                {"status": "PASS", "content_sha256": sha}, draft,
            )

            # Articles 1..15: consume every forward handoff.
            for index in range(1, 16):
                decision, result = consume_progress("WRITE_DRAFT")
                self.assertEqual(result["process_trigger"]["bound_work_item"], binding["items"][index])
                draft = self._draft(root, binding, index, f"article-{index}-v1")
                state = progress_guard.record_draft(binding, state, decision, index, draft)

                decision, _ = consume_progress("RUN_CHECKER", "LT68")
                sha = progress_guard.file_sha(draft)
                state = progress_guard.record_check(
                    binding, state, decision, index, "LT68",
                    {"status": "PASS", "content_sha256": sha}, draft,
                )

                decision, _ = consume_progress("RUN_CHECKER", "PPM679")
                state = progress_guard.record_check(
                    binding, state, decision, index, "PPM679",
                    {"status": "PASS", "content_sha256": sha}, draft,
                )

            self.assertEqual(state["phase"], "ALL_ARTICLES_LT_PPM_PASS")
            self.assertEqual(len(state["completed_items"]), 16)

            outer = full_workflow_gate.complete_stage(
                outer, "ARTICLE_PRODUCTION",
                full_workflow_gate.payload_for("ARTICLE_PRODUCTION", outer),
            )
            consume_outer("PSERC_PACKAGE")

            decision, _ = consume_progress("RUN_PSERC")
            pserc = {
                "contract": progress_guard.BATCH_STAGE_RESULT_CONTRACT,
                "stage": "PSERC",
                "status": "PASS",
                "batch_sha256": batch,
                "source_checkpoint_sha256": state["checkpoint_sha256"],
                "evidence_sha256": hashlib.sha256(b"pserc-evidence").hexdigest(),
                "pserc_package_sha256": hashlib.sha256(b"pserc-package").hexdigest(),
                "publish_allowed": False,
            }
            state = progress_guard.record_batch_stage(binding, state, decision, "PSERC", pserc)

            outer = full_workflow_gate.complete_stage(
                outer, "PSERC_PACKAGE", full_workflow_gate.payload_for("PSERC_PACKAGE", outer)
            )
            consume_outer("ENDSTEMPEL")

            decision, _ = consume_progress("RUN_ENDSTEMPEL")
            final_file = root / "FINAL_WORDPRESS_IMPORT.json"
            final_file.write_text('{"status":"final-test-file"}\n', encoding="utf-8")
            final_sha = progress_guard.file_sha(final_file)
            end = {
                "contract": progress_guard.BATCH_STAGE_RESULT_CONTRACT,
                "stage": "ENDSTEMPEL",
                "status": "PASS",
                "batch_sha256": batch,
                "source_checkpoint_sha256": state["checkpoint_sha256"],
                "evidence_sha256": hashlib.sha256(b"end-evidence").hexdigest(),
                "final_file_sha256": final_sha,
                "publish_allowed": False,
            }
            state = progress_guard.record_batch_stage(binding, state, decision, "ENDSTEMPEL", end)

            outer = full_workflow_gate.complete_stage(
                outer, "ENDSTEMPEL", full_workflow_gate.payload_for("ENDSTEMPEL", outer)
            )
            proof = full_workflow_gate.enter(outer)
            terminal_route = full_workflow_gate.stage_route_from_entry_proof(proof)
            self.assertEqual(terminal_route["next_stage"], "COMPLETE")
            self.assertIs(terminal_route["handoff_is_terminal"], True)
            self.assertIs(terminal_route["continuation_required"], False)
            self.assertIsNone(terminal_route["process_trigger"])

            decision = self._decision(binding, state)
            stop = progress_guard.resume(binding, state, decision)
            self.assertEqual(stop["status"], "STOP")
            self.assertEqual(stop["allowed_action"]["action"], "STOP")
            self.assertIs(stop["terminal"], True)
            self.assertIs(stop["continuation_required"], False)
            self.assertIsNone(stop["process_trigger"])
            self.assertTrue(final_file.is_file())
            self.assertEqual(progress_guard.file_sha(final_file), state["endstempel_final_file_sha256"])

        # 1 start handoff + 6 outer handoffs + 55 progress handoffs.
        self.assertEqual(len(progress_actions), 55)
        self.assertEqual(len(consumed_handoffs), 62)
        self.assertEqual(progress_actions.count("REPAIR_DRAFT:LT68"), 1)
        self.assertEqual(progress_actions.count("REPAIR_DRAFT:PPM679"), 1)

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
