from __future__ import annotations

import json
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
STEP = REPO / "control/startmaster0107/STEP_107007_RUN_NEW_ARTICLE_BATCH_NO_STOP.json"
CODEX = REPO / "isolated_system4/codex_entry.py"
BATCH = REPO / "control/startmaster0107/system4_107007_batch.py"
CONTROLLER = REPO / "isolated_system4/controller.py"

LEGACY_REPAIR_REFS = {
    "control/single-door-boundary/codex_current_room_bridge.py",
    "control/single-door-boundary/codex_current_action.py",
    "control/startmaster0107/fachworkflow_proof_handoff.py",
    "control/startmaster0107/STARTMASTER0107_DUAL_ROOTFIX_REPAIR.py",
}


class System4OnlyRepairAuthorityTest(unittest.TestCase):
    def test_107007_has_no_legacy_repair_authority(self):
        step = json.loads(STEP.read_text(encoding="utf-8"))
        refs = {row.get("ref") for row in step.get("authorized_inputs", []) if isinstance(row, dict)}
        self.assertTrue(LEGACY_REPAIR_REFS.isdisjoint(refs), refs & LEGACY_REPAIR_REFS)
        instruction = step.get("instruction", "")
        self.assertIn("HARD RULE — REPAIR NUR SYSTEM 4", instruction)
        self.assertIn("controller.py repair", instruction)
        self.assertIn("Keine zweite Repair-Wahrheit", instruction)
        for ref in LEGACY_REPAIR_REFS:
            self.assertIn(ref, instruction)

    def test_codex_repair_is_same_workspace_controller_repair(self):
        text = CODEX.read_text(encoding="utf-8")
        self.assertIn("'REPAIR_REQUIRED'", text)
        self.assertIn("controller repair", text)
        self.assertIn("same draft body", text)
        self.assertNotIn("fachworkflow_proof_handoff", text)
        self.assertNotIn("codex_current_room_bridge", text)

    def test_batch_cannot_route_repair_or_skip_current_item(self):
        text = BATCH.read_text(encoding="utf-8")
        self.assertIn("OUTPUT_GATE_REQUIRED", text)
        self.assertIn("checks.get(\"status\") == \"PASS\"", text)
        self.assertIn("SYSTEM4_107007_BATCH_CURRENT_ITEM_NOT_PASS", text)
        self.assertNotIn("FACHWORKFLOW_REPAIR_REQUIRED", text)
        self.assertNotIn("submission_command", text)
        self.assertNotIn("fachworkflow_proof_handoff", text)
        self.assertNotIn("codex_current_room_bridge", text)

    def test_system4_controller_owns_repair_command(self):
        text = CONTROLLER.read_text(encoding="utf-8")
        self.assertIn("REPAIR_REQUIRED", text)
        self.assertIn("repair", text)
        self.assertIn("fullcheck", text)


if __name__ == "__main__":
    unittest.main()
