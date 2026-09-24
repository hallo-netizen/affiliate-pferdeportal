import inspect
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "concept_agent"))

import durable_event_log as d


class OriginalWorkflowResumeButtonTests(unittest.TestCase):
    BATCH = "df59b8428c5e3f0750c5523091c00a1172975109823ee816d2234cf9052505d0"

    def test_bound_chat_worker_is_future_event_author(self):
        self.assertEqual(d.TRUSTED_EVENT_AUTHOR, "hallo-netizen")
        pointer = json.loads(
            (ROOT / "concept_agent/CONTROL_ENTRY_POINTER.json").read_text(encoding="utf-8")
        )
        self.assertEqual(pointer["production_event_author"], "hallo-netizen")
        self.assertEqual(pointer["production_worker"], "BOUND_CHAT_WORKER")
        self.assertIs(pointer["bound_worker_may_execute_only_machine_allowed_action"], True)
        self.assertIs(pointer["chat_may_choose_stage"], False)
        self.assertIs(pointer["chat_may_choose_article"], False)
        self.assertIs(pointer["alternate_route_allowed"], False)
        self.assertNotIn("post_machine_ready_executor_ref", pointer)

    def test_legacy_events_are_frozen_by_exact_comment_id(self):
        migration = json.loads(
            (ROOT / "concept_agent/EVENT_AUTHOR_MIGRATION_V1.json").read_text(encoding="utf-8")
        )
        self.assertEqual(migration["contract"], "CONCEPT_AGENT_EVENT_AUTHOR_MIGRATION_V2")
        self.assertEqual(migration["current_event_author"], "hallo-netizen")
        self.assertEqual(migration["frozen_legacy_max_sequence"], 60)
        self.assertEqual(set(migration["frozen_legacy_comment_ids"]), {str(i) for i in range(1, 61)})
        self.assertIs(migration["new_legacy_events_allowed"], False)
        self.assertIs(migration["future_batches_legacy_events_allowed"], False)

        row = {"id": migration["frozen_legacy_comment_ids"]["60"], "user": {"login": "anything"}}
        self.assertTrue(d._event_author_allowed(row, {"sequence": 60}, self.BATCH))
        wrong = {"id": row["id"] + 1, "user": {"login": "anything"}}
        self.assertFalse(d._event_author_allowed(wrong, {"sequence": 60}, self.BATCH))

    def test_negative_github_cannot_author_next_repair_event(self):
        row = {"user": {"login": "github-actions[bot]"}}
        self.assertFalse(d._event_author_allowed(row, {"sequence": 61}, self.BATCH))

    def test_negative_obsolete_worker_cannot_author_future_event(self):
        obsolete = "chatgpt-" + "co" + "dex-connector[bot]"
        row = {"user": {"login": obsolete}}
        self.assertFalse(d._event_author_allowed(row, {"sequence": 61}, self.BATCH))

    def test_positive_bound_chat_worker_can_author_next_event(self):
        row = {"user": {"login": "hallo-netizen"}}
        self.assertTrue(d._event_author_allowed(row, {"sequence": 61}, self.BATCH))

    def test_no_per_error_github_trigger_or_alternate_executor(self):
        workflow = (
            ROOT / ".github/workflows/pferde-atelier-github-batch-executor.yml"
        ).read_text(encoding="utf-8")
        self.assertIn("concept_agent/RESUME_TRIGGER", workflow)
        trigger_block = workflow.split("jobs:", 1)[0]
        self.assertNotIn("recovery/current16-input", trigger_block)
        self.assertEqual(trigger_block.count("concept_agent/RESUME_TRIGGER"), 1)
        self.assertIn("concept_agent/durable_event_log.py current", workflow)
        self.assertIn("concept_agent/universal_reentry_guard.py build", workflow)
        self.assertIn("concept_agent/progress_guard.py resume", workflow)
        self.assertFalse((ROOT / "concept_agent/github_batch_executor.py").exists())

    def test_active_route_has_no_obsolete_worker_product_binding(self):
        forbidden = ("co" + "dex").lower()
        active = [
            "concept_agent/durable_event_log.py",
            "concept_agent/CONTROL_ENTRY_POINTER.json",
            "concept_agent/START_HERE.md",
            ".github/workflows/pferde-atelier-github-batch-executor.yml",
            "AGENTS.override.md",
            "isolated_system4/AGENTS.md",
            "isolated_system4/supervisor.py",
            "isolated_system4/worker_dispatch.py",
            "isolated_system4/root_entry.py",
            "isolated_system4/parent_start.py",
            "control/startmaster0107/bound_start_hardlock.py",
            "control/startmaster0107/BOUND_START_HARDLOCK.json",
            "control/startmaster0107/BOUND_START_RECEIPT.json",
            "control/startmaster0107/CURRENT_STATE.json",
            "control/startmaster0107/PFERDE_ATELIER_START_HERE.json",
            "control/startmaster0107/STEP_107007_RUN_NEW_ARTICLE_BATCH_NO_STOP.json",
            "control/CURRENT_STARTMASTER.json",
        ]
        for rel in active:
            with self.subTest(path=rel):
                self.assertNotIn(forbidden, (ROOT / rel).read_text(encoding="utf-8").lower())

    def test_active_current_state_worker_gate_is_neutral_and_fail_closed(self):
        state = json.loads(
            (ROOT / "control/startmaster0107/CURRENT_STATE.json").read_text(encoding="utf-8")
        )
        gate = state["execution_gate"]
        forbidden = ("co" + "dex").lower()
        self.assertEqual(gate["hard_worker_target"], "BOUND_CHAT_WORKER")
        self.assertEqual(gate["worker_selection_policy"], "MACHINE_BOUND_NO_CHAT_CHOICE")
        self.assertNotIn(forbidden, gate["contract"].lower())
        self.assertNotIn(forbidden, gate["hard_worker_target"].lower())
        blocker = state["external_execution_blocker"]
        self.assertIs(blocker["resolved"], True)
        self.assertIs(blocker["applies_to_concept_agent"], False)
        self.assertNotIn(forbidden, blocker["code"].lower())

    def test_system4_dispatch_contract_is_neutral(self):
        sup = (ROOT / "isolated_system4/supervisor.py").read_text(encoding="utf-8")
        disp = (ROOT / "isolated_system4/worker_dispatch.py").read_text(encoding="utf-8")
        self.assertIn("SYSTEM4_BOUND_WORKER_DISPATCH_V2", sup)
        self.assertIn("SYSTEM4_BOUND_WORKER_DISPATCH_V2", disp)

    def test_resume_is_generic_1_to_n_not_current_16_hardcoded(self):
        source = inspect.getsource(d._current_batch)
        self.assertIn('count = intake.get("item_count")', source)
        workflow = (
            ROOT / ".github/workflows/pferde-atelier-github-batch-executor.yml"
        ).read_text(encoding="utf-8")
        self.assertNotIn("current16", workflow.lower())
        self.assertNotIn("item_count = 16", source.lower())


    def test_future_batch_event_one_uses_generic_bound_worker(self):
        future_batch = "f" * 64
        bound = {"user": {"login": "hallo-netizen"}}
        other = {"user": {"login": "github-actions[bot]"}}
        self.assertTrue(d._event_author_allowed(bound, {"sequence": 1}, future_batch))
        self.assertFalse(d._event_author_allowed(other, {"sequence": 1}, future_batch))


if __name__ == "__main__":
    unittest.main(verbosity=2)
