import json
import unittest
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"concept_agent"))
import durable_event_log as d

class GithubExecutorMigrationTests(unittest.TestCase):
    def test_active_author_is_github_actions(self):
        self.assertEqual(d.TRUSTED_EVENT_AUTHOR,"github-actions[bot]")
        self.assertEqual(d.LEGACY_EVENT_AUTHOR,"chatgpt-codex-connector[bot]")

    def test_legacy_hash_map_is_exact_1_to_20(self):
        m=json.loads((ROOT/"concept_agent/EVENT_AUTHOR_MIGRATION_V1.json").read_text())
        self.assertIs(m["new_legacy_events_allowed"],False)
        self.assertIs(m["future_batches_legacy_author_allowed"],False)
        self.assertEqual(set(m["legacy_event_hashes"]),{str(i) for i in range(1,21)})
        self.assertEqual(m["legacy_event_hashes"]["20"],m["legacy_last_event_sha256"])

    def test_pointer_has_no_codex_authority(self):
        p=json.loads((ROOT/"concept_agent/CONTROL_ENTRY_POINTER.json").read_text())
        self.assertEqual(p["production_event_author"],"github-actions[bot]")
        self.assertEqual(p["post_machine_ready_executor_ref"],"concept_agent/github_batch_executor.py")
        self.assertIs(p["codex_execution_allowed"],False)
        self.assertIs(p["codex_event_authority_allowed"],False)

    def test_executor_is_continuous_and_publish_false(self):
        s=(ROOT/"concept_agent/github_batch_executor.py").read_text()
        self.assertIn("MAX_STEPS=512",s)
        self.assertIn("def run()",s)
        self.assertIn("def step()",s)
        self.assertIn('"publish_allowed":False',s)
        self.assertNotIn("openai/codex-action",s)

if __name__=="__main__":
    unittest.main(verbosity=2)
