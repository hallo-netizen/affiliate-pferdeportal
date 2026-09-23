import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parents[1]
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import full_workflow_gate
import progress_guard
import runtime_environment_guard
import universal_reentry_guard as guard


class UniversalReentryV2Tests(unittest.TestCase):
    def setUp(self):
        runtime = {
            "contract": runtime_environment_guard.CONTRACT,
            "status": "PASS",
            "validator_ref": "test-validator",
            "validator_sha256": hashlib.sha256(b"validator").hexdigest(),
            "toolbox_manifest_ref": "test-toolbox",
            "toolbox_manifest_sha256": hashlib.sha256(b"toolbox").hexdigest(),
            "runtime_tools_sha256": hashlib.sha256(b"runtime-tools").hexdigest(),
            "languagetool_engine": "LanguageTool 6.8 / Bestand 43",
            "languagetool_jar_sha256": hashlib.sha256(b"lt").hexdigest(),
            "ppm679_package_sha256": hashlib.sha256(b"ppm").hexdigest(),
            "pserc_fix_package_sha256": hashlib.sha256(b"pserc").hexdigest(),
            "free_tool_selection": False,
            "free_binary_lookup": False,
            "fallback_runtime_allowed": False,
            "publish_allowed": False,
        }
        runtime["binding_sha256"] = runtime_environment_guard.stable(runtime)
        self.runtime = runtime
        patcher = mock.patch.object(runtime_environment_guard, "current_binding", return_value=runtime)
        patcher.start()
        self.addCleanup(patcher.stop)

    def binding(self, count=1):
        items = []
        for i in range(count):
            slot = hashlib.sha256(f"slot-{i}".encode()).hexdigest()
            items.append({
                "item_index": i,
                "identity": {
                    "item_index": i,
                    "title": f"Artikel {i}",
                    "target_keyword": f"Keyword {i}",
                    "category": "test",
                    "article_type": "Beratung",
                    "plan_slot": slot,
                    "identity_sha256": hashlib.sha256(f"id-{i}".encode()).hexdigest(),
                },
                "research_bound": {
                    "item_index": i,
                    "plan_slot": slot,
                    "source_pool_sha256": hashlib.sha256(f"pool-{i}".encode()).hexdigest(),
                },
            })
        value = {
            "contract": progress_guard.BINDING_CONTRACT,
            "status": "AUTHORING_READY",
            "batch_sha256": hashlib.sha256(b"batch").hexdigest(),
            "item_count": count,
            "source_intake_sha256": hashlib.sha256(b"intake").hexdigest(),
            "source_research_binding_sha256": hashlib.sha256(b"research-bound").hexdigest(),
            "items": items,
            "publish_allowed": False,
        }
        value["binding_sha256"] = progress_guard.stable(value)
        return value

    def draft_row(self, binding, index=0, content="durable-current-draft", revision=1, lt="PENDING", ppm="PENDING"):
        raw = content.encode("utf-8")
        slot = binding["items"][index]["identity"]["plan_slot"]
        return {
            "item_index": index,
            "plan_slot": slot,
            "filename": f"{index:02d}_{slot}.md",
            "draft_sha256": hashlib.sha256(raw).hexdigest(),
            "size_bytes": len(raw),
            "content_utf8": content,
            "revision": revision,
            "lt68": lt,
            "ppm679": ppm,
        }

    def checkpoint(self, binding, phase):
        state = {
            "contract": progress_guard.CHECKPOINT_CONTRACT,
            "batch_sha256": binding["batch_sha256"],
            "production_binding_sha256": binding["binding_sha256"],
            "item_count": binding["item_count"],
            "status": "IN_PROGRESS",
            "phase": phase,
            "next_item_index": 0,
            "completed_items": [],
            "current_item": None,
            "previous_checkpoint_sha256": None,
            "drafts": [],
            "publish_allowed": False,
        }
        if phase in {"LT68_REQUIRED", "PPM679_REQUIRED", "REPAIR_REQUIRED"}:
            lt = "PASS" if phase == "PPM679_REQUIRED" else ("REPAIR_REQUIRED" if phase == "REPAIR_REQUIRED" else "PENDING")
            row = self.draft_row(binding, lt=lt)
            state["drafts"] = [row]
            state["current_item"] = {"item_index": 0, "draft_sha256": row["draft_sha256"]}
            if phase == "REPAIR_REQUIRED":
                state["current_item"].update({
                    "checker": "LT68",
                    "finding_sha256": hashlib.sha256(b"finding").hexdigest(),
                })
        if phase in {"ALL_ARTICLES_LT_PPM_PASS", "PSERC_PASS_ENDSTEMPEL_REQUIRED", "ENDSTEMPEL_PASS_STOP"}:
            rows = []
            completed = []
            for i in range(binding["item_count"]):
                row = self.draft_row(binding, i, f"final-{i}", i + 1, "PASS", "PASS")
                rows.append(row)
                completed.append({
                    "item_index": i,
                    "plan_slot": row["plan_slot"],
                    "draft_sha256": row["draft_sha256"],
                    "revision": row["revision"],
                    "lt68": "PASS",
                    "ppm679": "PASS",
                })
            state["drafts"] = rows
            state["completed_items"] = completed
            state["next_item_index"] = binding["item_count"]
            state["status"] = "PASS" if phase != "PSERC_PASS_ENDSTEMPEL_REQUIRED" else "IN_PROGRESS"
            if phase in {"PSERC_PASS_ENDSTEMPEL_REQUIRED", "ENDSTEMPEL_PASS_STOP"}:
                state["pserc_package_sha256"] = hashlib.sha256(b"pserc-package").hexdigest()
            if phase == "ENDSTEMPEL_PASS_STOP":
                state["endstempel_final_file_sha256"] = hashlib.sha256(b"final-file").hexdigest()
        state["allowed_action"] = progress_guard.expected_action(binding, state)
        state["checkpoint_sha256"] = progress_guard.stable(state)
        return state

    def test_route_is_derived_for_every_current_production_stage(self):
        binding = self.binding()
        cases = {
            "AUTHORING_REQUIRED": "ARTICLE_PRODUCTION",
            "LT68_REQUIRED": "ARTICLE_PRODUCTION",
            "PPM679_REQUIRED": "ARTICLE_PRODUCTION",
            "REPAIR_REQUIRED": "ARTICLE_PRODUCTION",
            "ALL_ARTICLES_LT_PPM_PASS": "PSERC_PACKAGE",
            "PSERC_PASS_ENDSTEMPEL_REQUIRED": "ENDSTEMPEL",
            "ENDSTEMPEL_PASS_STOP": "COMPLETE",
        }
        for phase, expected_stage in cases.items():
            state = self.checkpoint(binding, phase)
            decision = guard.build(binding, state)
            self.assertEqual(decision["outer_stage"], expected_stage)
            self.assertEqual(guard.verify(binding, state, decision)["status"], "UNIVERSAL_REENTRY_ALLOWED")
            self.assertEqual(decision["runtime_binding"], self.runtime)
            self.assertFalse(decision["policy"]["free_chat_execution"])
            self.assertFalse(decision["policy"]["free_repo_search"])
            self.assertFalse(decision["policy"]["free_binary_lookup"])
            self.assertFalse(decision["policy"]["alternate_route_allowed"])
            self.assertEqual(decision["policy"]["missing_canonical_execution_environment"], "STOP")

    def test_full_outer_workflow_reentry_matrix_is_fail_closed(self):
        with tempfile.TemporaryDirectory() as td:
            proof = full_workflow_gate.simulate_all_entries(Path(td))
        self.assertEqual(proof["status"], "PASS")
        self.assertEqual(proof["positive_entry_count"], len(full_workflow_gate.STAGES) + 1)
        self.assertGreater(proof["negative_case_count"], 0)

    def test_tampered_decision_and_stale_checkpoint_are_blocked(self):
        binding = self.binding()
        state = self.checkpoint(binding, "AUTHORING_REQUIRED")
        decision = guard.build(binding, state)

        tampered = json.loads(json.dumps(decision))
        tampered["policy"]["free_repo_search"] = True
        core = dict(tampered)
        core.pop("decision_sha256", None)
        tampered["decision_sha256"] = guard.stable(core)
        with self.assertRaises(guard.Blocked):
            guard.verify(binding, state, tampered)
        with self.assertRaises(progress_guard.Blocked):
            progress_guard.resume(binding, state, tampered)

        stale = json.loads(json.dumps(state))
        stale["checkpoint_sha256"] = "0" * 64
        with self.assertRaises(progress_guard.Blocked):
            guard.build(binding, stale)

    def test_every_mutating_entry_rejects_missing_decision(self):
        binding = self.binding()
        authoring = self.checkpoint(binding, "AUTHORING_REQUIRED")
        lt = self.checkpoint(binding, "LT68_REQUIRED")
        repair = self.checkpoint(binding, "REPAIR_REQUIRED")
        batch = self.checkpoint(binding, "ALL_ARTICLES_LT_PPM_PASS")

        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            slot = binding["items"][0]["identity"]["plan_slot"]
            draft = root / f"00_{slot}.md"
            draft.write_text("durable-current-draft", encoding="utf-8")
            with self.assertRaises(progress_guard.Blocked):
                progress_guard.record_draft(binding, authoring, {}, 0, draft)
            with self.assertRaises(progress_guard.Blocked):
                progress_guard.record_check(binding, lt, {}, 0, "LT68", {}, draft)
            with self.assertRaises(progress_guard.Blocked):
                progress_guard.replace_draft(binding, repair, {}, 0, draft)
            with self.assertRaises(progress_guard.Blocked):
                progress_guard.materialize_current_draft(binding, lt, {}, root / "restore")
            with self.assertRaises(progress_guard.Blocked):
                progress_guard.record_batch_stage(binding, batch, {}, "PSERC", {})

    def test_durable_draft_restores_exact_bytes(self):
        binding = self.binding()
        state = self.checkpoint(binding, "LT68_REQUIRED")
        decision = guard.build(binding, state)
        with tempfile.TemporaryDirectory() as td:
            result = progress_guard.materialize_current_draft(binding, state, decision, Path(td))
            path = Path(result["path"])
            self.assertEqual(path.read_text(encoding="utf-8"), state["drafts"][0]["content_utf8"])
            self.assertEqual(progress_guard.file_sha(path), state["drafts"][0]["draft_sha256"])

    def test_missing_or_corrupt_draft_bytes_block_reentry(self):
        binding = self.binding()
        state = self.checkpoint(binding, "ALL_ARTICLES_LT_PPM_PASS")
        broken = json.loads(json.dumps(state))
        broken["drafts"][0].pop("content_utf8")
        core = dict(broken)
        core.pop("checkpoint_sha256", None)
        broken["checkpoint_sha256"] = progress_guard.stable(core)
        with self.assertRaises(progress_guard.Blocked):
            guard.build(binding, broken)

    def test_missing_runtime_is_hard_stop(self):
        binding = self.binding()
        state = self.checkpoint(binding, "AUTHORING_REQUIRED")
        with mock.patch.object(
            runtime_environment_guard,
            "current_binding",
            side_effect=runtime_environment_guard.Blocked("CANONICAL_EXECUTION_ENVIRONMENT_NOT_READY"),
        ):
            with self.assertRaises(runtime_environment_guard.Blocked):
                guard.build(binding, state)


if __name__ == "__main__":
    unittest.main(verbosity=2)
