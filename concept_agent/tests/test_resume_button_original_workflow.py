import json
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "concept_agent"))

import durable_event_log as d


class OriginalWorkflowResumeButtonTests(unittest.TestCase):
    def test_original_worker_is_future_event_author(self):
        self.assertEqual(d.TRUSTED_EVENT_AUTHOR, "chatgpt-codex-connector[bot]")
        self.assertEqual(d.LEGACY_EVENT_AUTHOR, "github-actions[bot]")
        pointer = json.loads(
            (ROOT / "concept_agent/CONTROL_ENTRY_POINTER.json").read_text(encoding="utf-8")
        )
        self.assertEqual(pointer["production_event_author"], "chatgpt-codex-connector[bot]")
        self.assertNotIn("post_machine_ready_executor_ref", pointer)

    def test_github_events_are_frozen_at_60(self):
        migration = json.loads(
            (ROOT / "concept_agent/EVENT_AUTHOR_MIGRATION_V1.json").read_text(encoding="utf-8")
        )
        self.assertEqual(migration["current_event_author"], "chatgpt-codex-connector[bot]")
        self.assertEqual(migration["legacy_event_author"], "github-actions[bot]")
        self.assertEqual(migration["legacy_max_sequence"], 60)
        self.assertEqual(set(migration["legacy_event_hashes"]), {str(i) for i in range(21, 61)})
        self.assertEqual(
            migration["legacy_event_hashes"]["60"],
            migration["legacy_last_event_sha256"],
        )
        self.assertIs(migration["new_legacy_events_allowed"], False)
        self.assertIs(migration["future_batches_legacy_author_allowed"], False)

    def test_negative_github_cannot_author_next_repair_event(self):
        row = {"user": {"login": "github-actions[bot]"}}
        event61 = {
            "sequence": 61,
            "event_sha256": "a" * 64,
        }
        self.assertFalse(
            d._event_author_allowed(
                row,
                event61,
                "df59b8428c5e3f0750c5523091c00a1172975109823ee816d2234cf9052505d0",
            )
        )

    def test_positive_original_worker_can_author_next_event(self):
        row = {"user": {"login": "chatgpt-codex-connector[bot]"}}
        event61 = {
            "sequence": 61,
            "event_sha256": "b" * 64,
        }
        self.assertTrue(
            d._event_author_allowed(
                row,
                event61,
                "df59b8428c5e3f0750c5523091c00a1172975109823ee816d2234cf9052505d0",
            )
        )

    def test_no_per_error_github_trigger_or_alternate_executor(self):
        workflow = (
            ROOT / ".github/workflows/pferde-atelier-github-batch-executor.yml"
        ).read_text(encoding="utf-8")
        self.assertIn("concept_agent/RESUME_TRIGGER", workflow)
        self.assertNotIn("recovery/current16-input", workflow)
        self.assertNotIn("github_batch_executor.py", workflow)
        self.assertIn("concept_agent/durable_event_log.py current", workflow)
        self.assertIn("concept_agent/universal_reentry_guard.py build", workflow)
        self.assertIn("concept_agent/progress_guard.py resume", workflow)
        self.assertFalse((ROOT / "concept_agent/github_batch_executor.py").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
