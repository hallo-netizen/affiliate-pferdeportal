import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

import controller


FIXTURE = Path(__file__).resolve().parent / "live_fixture" / "wordpress_snapshot.json"


class IndexedIngressTests(unittest.TestCase):
    def test_all_seven_items_use_same_snapshot_and_batch(self):
        snapshot = json.loads(FIXTURE.read_text(encoding="utf-8"))
        batch = snapshot["next_textmachine_metadata_batch"]
        expected_source_sha = hashlib.sha256(FIXTURE.read_bytes()).hexdigest()
        with tempfile.TemporaryDirectory(prefix="system4-indexed-ingress-") as td:
            root = Path(td)
            for index, expected in enumerate(batch["items"]):
                workspace = root / f"item-{index}"
                controller.cmd_ingress(FIXTURE, workspace, index)
                state = json.loads((workspace / "state.json").read_text(encoding="utf-8"))
                controller.verify_state(state)
                self.assertEqual(state["article"], expected)
                self.assertEqual(state["batch_sha256"], batch["batch_sha256"])
                self.assertEqual(state["source_snapshot_sha256"], expected_source_sha)
                self.assertEqual(state["phase"], "RESEARCH_REQUIRED")
                self.assertFalse(state["publish_allowed"])

    def test_default_ingress_remains_first_item(self):
        snapshot = json.loads(FIXTURE.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory(prefix="system4-default-ingress-") as td:
            controller.cmd_ingress(FIXTURE, Path(td))
            state = json.loads((Path(td) / "state.json").read_text(encoding="utf-8"))
            self.assertEqual(state["article"], snapshot["next_textmachine_metadata_batch"]["items"][0])

    def test_out_of_range_item_is_blocked(self):
        snapshot = json.loads(FIXTURE.read_text(encoding="utf-8"))
        count = len(snapshot["next_textmachine_metadata_batch"]["items"])
        with tempfile.TemporaryDirectory(prefix="system4-indexed-negative-") as td:
            with self.assertRaisesRegex(controller.Fail, "WORDPRESS_ITEM_INDEX_INVALID"):
                controller.cmd_ingress(FIXTURE, Path(td), count)

    def test_negative_index_is_blocked(self):
        with tempfile.TemporaryDirectory(prefix="system4-indexed-negative-") as td:
            with self.assertRaisesRegex(controller.Fail, "WORDPRESS_ITEM_INDEX_INVALID"):
                controller.cmd_ingress(FIXTURE, Path(td), -1)

    def test_publish_true_snapshot_is_blocked(self):
        snapshot = json.loads(FIXTURE.read_text(encoding="utf-8"))
        snapshot["next_textmachine_metadata_batch"]["publish_allowed"] = True
        with tempfile.TemporaryDirectory(prefix="system4-publish-negative-") as td:
            bad = Path(td) / "bad.json"
            bad.write_text(json.dumps(snapshot, ensure_ascii=False), encoding="utf-8")
            with self.assertRaisesRegex(controller.Fail, "WORDPRESS_PUBLISH_AUTHORITY_FAIL"):
                controller.cmd_ingress(bad, Path(td) / "workspace", 0)

    def test_item_count_drift_is_blocked(self):
        snapshot = json.loads(FIXTURE.read_text(encoding="utf-8"))
        snapshot["next_textmachine_metadata_batch"]["item_count"] += 1
        with tempfile.TemporaryDirectory(prefix="system4-count-negative-") as td:
            bad = Path(td) / "bad.json"
            bad.write_text(json.dumps(snapshot, ensure_ascii=False), encoding="utf-8")
            with self.assertRaisesRegex(controller.Fail, "WORDPRESS_BATCH_COUNT_MISMATCH"):
                controller.cmd_ingress(bad, Path(td) / "workspace", 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
