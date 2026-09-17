from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

import batch_repetition_guard
import global_workshop


class GlobalWorkshopTests(unittest.TestCase):
    def _state(self, root: Path, index: int) -> Path:
        body = f"body {index}"
        path = root / f"state-{index}.json"
        path.write_text(json.dumps({
            "phase": "OUTPUT_GATE_REQUIRED",
            "draft_sha256": hashlib.sha256(body.encode()).hexdigest(),
            "checks": {"status": "PASS"},
            "last_error": None,
            "release_prepared": None,
            "released": False,
        }), encoding="utf-8")
        return path

    def test_batch_findings_are_preserved_and_routed_to_workshop(self):
        sentences = [
            f"dies ist ein ausreichend langer wiederholter testsatz nummer {i} mit vielen woertern fuer den sicheren batch test."
            for i in range(7)
        ]
        common = " ".join(sentences)
        bodies = [common for _ in range(4)] + [
            "dieser artikel ist komplett anders und besitzt ausreichend viele unterschiedliche woerter fuer einen test ohne wiederholung.",
            "noch ein eigenstaendiger artikel mit bewusst anderen woertern und eigener struktur fuer den lokalen test.",
            "dritter eigenstaendiger artikel mit anderer aussage und mehreren worten fuer die pruefung des batch verhaltens.",
        ]
        with self.assertRaises(batch_repetition_guard.BatchRepetitionError) as caught:
            batch_repetition_guard.validate_batch_repetition(bodies)
        exc = caught.exception
        self.assertEqual(len(exc.findings), 7)
        request = global_workshop.build_request("BATCH", exc)
        self.assertTrue(request["workshop_required"])
        self.assertTrue(request["repairable"])
        self.assertFalse(request["terminal_at_origin"])
        self.assertEqual(request["finding_count"], 7)
        self.assertEqual(set(request["repair_targets"]), {"3"})

        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            states = [self._state(root, i) for i in range(7)]
            changed = global_workshop.route_article_states(request, states)
            self.assertEqual(changed, [3])
            routed = json.loads(states[3].read_text(encoding="utf-8"))
            self.assertEqual(routed["phase"], "REPAIR_REQUIRED")
            self.assertEqual(routed["checks"]["mode"], "GLOBAL_WORKSHOP")
            self.assertEqual(len(routed["checks"]["findings"]), 7)
            untouched = json.loads(states[2].read_text(encoding="utf-8"))
            self.assertEqual(untouched["phase"], "OUTPUT_GATE_REQUIRED")

    def test_nonrepairable_error_still_enters_workshop_before_block(self):
        request = global_workshop.build_request("BATCH", RuntimeError("STATE_DRAFT_HASH_MISMATCH"))
        self.assertTrue(request["workshop_required"])
        self.assertFalse(request["terminal_at_origin"])
        self.assertFalse(request["repairable"])
        self.assertEqual(request["status"], "BLOCKED_NON_REPAIRABLE")

    def test_multiple_findings_are_never_reduced_to_first(self):
        findings = [
            {"error_code": "LANGUAGETOOL_FINDING", "article_index": 0, "rule_id": "A"},
            {"error_code": "LANGUAGETOOL_FINDING", "article_index": 0, "rule_id": "B"},
            {"error_code": "LANGUAGETOOL_FINDING", "article_index": 0, "rule_id": "C"},
        ]
        request = global_workshop.build_request("FULLCHECK", RuntimeError("LANGUAGETOOL_FINDING"), findings=findings)
        self.assertEqual(request["finding_count"], 3)
        self.assertEqual(request["findings"], findings)
        self.assertEqual(len(request["repair_targets"]["0"]), 3)


if __name__ == "__main__":
    unittest.main(verbosity=2)
