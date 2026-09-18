from __future__ import annotations

# HARD RULE: the final article may complete only after batch_gate.py collect passes.
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("system4_107007_batch_tested", HERE / "system4_107007_batch.py")
assert SPEC and SPEC.loader
batch = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(batch)


class ProductiveOneToNTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.point0 = self.root / "point0.json"
        self.point0.write_text("{}\n", encoding="utf-8")
        self.batch_root = self.root / "run"
        self.items = []
        for i in range(1000):
            token = f"{i:064x}"[-64:]
            self.items.append({
                "plan_slot": token,
                "canonical_article_id": "article-" + str(i),
                "target_keyword": "keyword-" + str(i),
            })
        self.runtime = {"batch_sha256": "a" * 64, "source_snapshot_ref": "unused-in-unit-test"}
        self.collect_calls = 0

    def tearDown(self):
        self.tmp.cleanup()

    def fake_start(self, point0: str, workspace: str, index: int):
        w = Path(workspace)
        w.mkdir(parents=True, exist_ok=False)
        return {"status": "SYSTEM4_107007_ROOT_READY_STOP", "item_index": index}

    def fake_collect(self, batch_root: Path, runtime: dict, items: list[dict]):
        self.collect_calls += 1
        evidence = Path(batch_root) / "batch-collect" / "system4_batch_evidence.json"
        evidence.parent.mkdir(parents=True, exist_ok=True)
        evidence.write_text(json.dumps({"status": "FULL_PASS_BATCH_COLLECTED", "count": len(items)}) + "\n", encoding="utf-8")
        return {
            "status": "SYSTEM4_BATCH_FULL_PASS_COLLECTED",
            "batch_sha256": runtime["batch_sha256"],
            "article_count": len(items),
            "batch_evidence_path": str(evidence),
            "batch_evidence_sha256": batch.sha256(evidence),
            "publish_allowed": False,
        }

    def mark_pass(self, index: int):
        item = self.items[index]
        w = self.batch_root / f"item-{index:06d}"
        state = {
            "phase": "OUTPUT_GATE_REQUIRED",
            "article": dict(item),
            "checks": {"status": "PASS"},
        }
        (w / "state.json").write_text(json.dumps(state) + "\n", encoding="utf-8")

    def run_count(self, count: int):
        items = self.items[:count]
        self.collect_calls = 0
        with mock.patch.object(batch, "outside_repo", side_effect=lambda p: Path(p).resolve()), \
             mock.patch.object(batch, "_runtime", return_value=(self.runtime, items)), \
             mock.patch.object(batch, "_validate_point0_all", return_value=None), \
             mock.patch.object(batch, "_collect_batch", side_effect=self.fake_collect), \
             mock.patch.object(batch.entry, "start", side_effect=self.fake_start):
            first = batch.start(str(self.point0), str(self.batch_root))
            self.assertEqual(first["item_index"], 0)
            self.assertEqual(first["item_count"], count)
            with self.assertRaisesRegex(batch.Blocked, "CURRENT_ITEM_NOT_PASS:0"):
                batch.advance(str(self.point0), str(self.batch_root))
            for i in range(count):
                self.mark_pass(i)
                out = batch.advance(str(self.point0), str(self.batch_root))
                if i + 1 < count:
                    self.assertEqual(out["status"], "SYSTEM4_107007_BATCH_ROOT_READY_STOP")
                    self.assertEqual(out["item_index"], i + 1)
                    self.assertEqual(self.collect_calls, 0)
                else:
                    self.assertEqual(out["status"], "SYSTEM4_107007_BATCH_ITEMS_COMPLETE")
                    self.assertEqual(out["completed_indices"], list(range(count)))
                    self.assertEqual(out["started_indices"], list(range(count)))
                    self.assertEqual(out["batch_collect"]["status"], "SYSTEM4_BATCH_FULL_PASS_COLLECTED")
                    self.assertEqual(self.collect_calls, 1)
            again = batch.advance(str(self.point0), str(self.batch_root))
            self.assertEqual(again["status"], "SYSTEM4_107007_BATCH_ITEMS_COMPLETE")
            self.assertEqual(again["started_indices"], list(range(count)))
            self.assertEqual(self.collect_calls, 1)

    def test_1_article(self):
        self.run_count(1)

    def test_3_articles(self):
        self.run_count(3)

    def test_25_articles(self):
        self.run_count(25)

    def test_1000_articles(self):
        self.run_count(1000)

    def test_collect_failure_blocks_items_complete(self):
        items = self.items[:1]
        with mock.patch.object(batch, "outside_repo", side_effect=lambda p: Path(p).resolve()), \
             mock.patch.object(batch, "_runtime", return_value=(self.runtime, items)), \
             mock.patch.object(batch, "_validate_point0_all", return_value=None), \
             mock.patch.object(batch, "_collect_batch", side_effect=batch.Blocked("COLLECT_FAIL")), \
             mock.patch.object(batch.entry, "start", side_effect=self.fake_start):
            batch.start(str(self.point0), str(self.batch_root))
            self.mark_pass(0)
            with self.assertRaisesRegex(batch.Blocked, "COLLECT_FAIL"):
                batch.advance(str(self.point0), str(self.batch_root))
            state = json.loads((self.batch_root / batch.STATE_NAME).read_text(encoding="utf-8"))
            self.assertEqual(state["status"], "ACTIVE")
            self.assertIsNone(state["batch_collect"])

    def test_completed_state_without_collect_proof_blocks(self):
        items = self.items[:1]
        with mock.patch.object(batch, "outside_repo", side_effect=lambda p: Path(p).resolve()), \
             mock.patch.object(batch, "_runtime", return_value=(self.runtime, items)), \
             mock.patch.object(batch, "_validate_point0_all", return_value=None), \
             mock.patch.object(batch.entry, "start", side_effect=self.fake_start):
            batch.start(str(self.point0), str(self.batch_root))
            state_path = self.batch_root / batch.STATE_NAME
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state["status"] = "ITEMS_COMPLETE"
            state["current_index"] = 1
            state["completed_indices"] = [0]
            state_path.write_text(json.dumps(state) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(batch.Blocked, "COLLECT_PROOF_INVALID"):
                batch.status(str(self.point0), str(self.batch_root))

    def test_runtime_drift_blocks(self):
        items = self.items[:3]
        with mock.patch.object(batch, "outside_repo", side_effect=lambda p: Path(p).resolve()), \
             mock.patch.object(batch, "_runtime", return_value=(self.runtime, items)), \
             mock.patch.object(batch, "_validate_point0_all", return_value=None), \
             mock.patch.object(batch.entry, "start", side_effect=self.fake_start):
            batch.start(str(self.point0), str(self.batch_root))
        drift = {"batch_sha256": "b" * 64, "source_snapshot_ref": "unused-in-unit-test"}
        with mock.patch.object(batch, "outside_repo", side_effect=lambda p: Path(p).resolve()), \
             mock.patch.object(batch, "_runtime", return_value=(drift, items)), \
             mock.patch.object(batch, "_validate_point0_all", return_value=None):
            with self.assertRaisesRegex(batch.Blocked, "RUNTIME_DRIFT"):
                batch.status(str(self.point0), str(self.batch_root))

    def test_nonsequential_state_blocks(self):
        items = self.items[:3]
        with mock.patch.object(batch, "outside_repo", side_effect=lambda p: Path(p).resolve()), \
             mock.patch.object(batch, "_runtime", return_value=(self.runtime, items)), \
             mock.patch.object(batch, "_validate_point0_all", return_value=None), \
             mock.patch.object(batch.entry, "start", side_effect=self.fake_start):
            batch.start(str(self.point0), str(self.batch_root))
            state_path = self.batch_root / batch.STATE_NAME
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state["started_indices"] = [0, 2]
            state_path.write_text(json.dumps(state) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(batch.Blocked, "STARTED_SEQUENCE_INVALID"):
                batch.status(str(self.point0), str(self.batch_root))


if __name__ == "__main__":
    unittest.main()
