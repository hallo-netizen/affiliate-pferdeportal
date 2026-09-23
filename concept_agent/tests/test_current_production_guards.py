import hashlib
import json
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

SYSTEM4 = HERE.parent / "isolated_system4"
if str(SYSTEM4) not in sys.path:
    sys.path.insert(0, str(SYSTEM4))
import content_guard
import source_acquisition


class CurrentProductionGuardTests(unittest.TestCase):
    def test_own_domain_is_always_forbidden(self):
        self.assertTrue(intake_bridge._forbidden_research_url("https://pferde-atelier.de/test"))
        self.assertTrue(intake_bridge._forbidden_research_url("https://www.pferde-atelier.de/test"))
        self.assertTrue(production_bridge._forbidden_own_domain("https://pferde-atelier.de/"))
        self.assertFalse(intake_bridge._forbidden_research_url("https://example.org/test"))
        research = {
            "contract": "SYSTEM4_RESEARCH_EVIDENCE_V1",
            "sources": [{
                "source_id": "s1",
                "source_title": "Eigene Domain",
                "source_url": "https://pferde-atelier.de/test",
                "retrieved_at": "2026-09-23T00:00:00Z",
                "snapshot_sha256": hashlib.sha256(("x" * 50).encode()).hexdigest(),
                "evidence": "x" * 50,
            }],
        }
        with self.assertRaisesRegex(content_guard.ContentGuardError, "SOURCE_OWN_DOMAIN_FORBIDDEN"):
            content_guard.validate_research_document(research)
        request = {
            "contract": source_acquisition.CONTRACT,
            "item_count": 1,
            "items": [{
                "item_index": 0,
                "plan_slot": "a" * 64,
                "sources": [{
                    "source_id": "s1",
                    "source_url": "https://pferde-atelier.de/test",
                    "source_title": "Eigene Domain",
                }],
            }],
        }
        called = {"fetch": False}
        def fail_fetch(*args, **kwargs):
            called["fetch"] = True
            return {"http_status": 200, "body": b"x" * 50, "content_type": "text/plain"}
        with self.assertRaisesRegex(source_acquisition.SourceAcquisitionError, "OWN_DOMAIN_FORBIDDEN"):
            source_acquisition.acquire_batch(request, fetcher=fail_fetch)
        self.assertFalse(called["fetch"])

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
            "phase": "AUTHORING_READY",
            "next_item_index": 0,
            "completed_items": [],
            "current_item": None,
            "previous_checkpoint_sha256": None,
            "publish_allowed": False,
        }
        state["checkpoint_sha256"] = progress_guard.stable(state)
        return state

    def test_checkpoint_chain_and_checker_order(self):
        binding = self._binding()
        state = self._checkpoint(binding)
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            for row in binding["items"]:
                p = root / f"{row['item_index']:02d}_{row['identity']['plan_slot']}.md"
                p.write_text(f"draft-{row['item_index']}", encoding="utf-8")
            state2 = progress_guard.attach_drafts(binding, state, root)
            self.assertEqual(state2["previous_checkpoint_sha256"], state["checkpoint_sha256"])
            draft0 = root / state2["drafts"][0]["filename"]
            sha0 = progress_guard.file_sha(draft0)
            lt = {"status": "PASS", "content_sha256": sha0}
            state3 = progress_guard.record_check(binding, state2, 0, "LT68", lt, draft0)
            self.assertEqual(state3["phase"], "CHECKING")
            with self.assertRaisesRegex(progress_guard.Blocked, "RECORD_CHECK_WRONG_ITEM"):
                progress_guard.record_check(binding, state3, 1, "PPM679", {"status":"PASS","content_sha256":sha0}, draft0)
            ppm = {"status": "PASS", "content_sha256": sha0}
            state4 = progress_guard.record_check(binding, state3, 0, "PPM679", ppm, draft0)
            self.assertEqual(state4["next_item_index"], 1)
            self.assertEqual(state4["completed_items"][0]["ppm679"], "PASS")

    def test_repair_cannot_advance_article(self):
        binding = self._binding()
        state = self._checkpoint(binding)
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            for row in binding["items"]:
                p = root / f"{row['item_index']:02d}_{row['identity']['plan_slot']}.md"
                p.write_text(f"draft-{row['item_index']}", encoding="utf-8")
            state = progress_guard.attach_drafts(binding, state, root)
            draft0 = root / state["drafts"][0]["filename"]
            sha0 = progress_guard.file_sha(draft0)
            repair = {"status": "REPAIR_REQUIRED", "content_sha256": sha0, "findings":[{"code":"x"}]}
            state = progress_guard.record_check(binding, state, 0, "LT68", repair, draft0)
            self.assertEqual(state["phase"], "REPAIR_REQUIRED")
            self.assertEqual(state["next_item_index"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
