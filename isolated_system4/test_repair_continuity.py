import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import batch_gate
import controller


def sha_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def bind_minimal_context(workspace: Path, index: int) -> None:
    state_path = workspace / "state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    context = {
        "fact_pack": {"test_index": index},
        "production_plan_item": {"test_index": index},
    }
    state["production_context"] = {
        **context,
        "sha256": controller.sha(context),
    }
    controller.save(state, state_path)


def write_stage_file(root: Path, name: str, text: str) -> Path:
    path = root / name
    path.write_text(text, encoding="utf-8")
    return path


class RepairContinuityTests(unittest.TestCase):
    def test_repairable_languagetool_finding_stays_same_draft_flow(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            snapshot = Path(__file__).resolve().parent / "live_fixture" / "wordpress_snapshot.json"
            workspace = root / "item0"
            controller.cmd_ingress(snapshot, workspace, 0)
            research = write_stage_file(root, "research.txt", "R" * 80)
            facts = write_stage_file(root, "facts.txt", "F" * 80)
            draft = write_stage_file(root, "draft.md", "# Test\n\nErster Entwurf")
            controller.cmd_research(workspace, research)
            controller.cmd_facts(workspace, facts)
            bind_minimal_context(workspace, 0)
            controller.cmd_draft(workspace, draft)

            repair = controller.production_checks.RepairRequired(
                "languagetool",
                [{"error_code": "LANGUAGETOOL_FINDING", "rule_id": "GERMAN_SPELLER_RULE"}],
            )
            passed = {"contract": "SYSTEM4_FULL_PRODUCTION_CHECK_V1", "status": "PASS"}
            with mock.patch.object(controller.production_checks, "run_all", side_effect=[repair, passed]) as run_all:
                self.assertEqual(controller.cmd_fullcheck(workspace), 3)
                state = json.loads((workspace / "state.json").read_text(encoding="utf-8"))
                self.assertEqual(state["phase"], "REPAIR_REQUIRED")
                self.assertEqual(state["last_error"], "FULL:languagetool:LANGUAGETOOL_FINDING")
                self.assertEqual(state["revision"], 1)

                draft.write_text("# Test\n\nKorrigierter Entwurf", encoding="utf-8")
                controller.cmd_draft(workspace, draft)
                self.assertEqual(controller.cmd_fullcheck(workspace), 0)
                state = json.loads((workspace / "state.json").read_text(encoding="utf-8"))
                self.assertEqual(state["phase"], "OUTPUT_GATE_REQUIRED")
                self.assertEqual(state["checks"]["status"], "PASS")
                self.assertEqual(state["checks"]["mode"], "FULL_PRODUCTION")
                self.assertEqual(state["revision"], 2)
                self.assertEqual(run_all.call_count, 2)

    def test_real_tool_failure_remains_hard_fail_closed(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            snapshot = Path(__file__).resolve().parent / "live_fixture" / "wordpress_snapshot.json"
            workspace = root / "item0"
            controller.cmd_ingress(snapshot, workspace, 0)
            controller.cmd_research(workspace, write_stage_file(root, "research.txt", "R" * 80))
            controller.cmd_facts(workspace, write_stage_file(root, "facts.txt", "F" * 80))
            bind_minimal_context(workspace, 0)
            controller.cmd_draft(workspace, write_stage_file(root, "draft.md", "# Test\n\nEntwurf"))

            hard = controller.production_checks.ProductionCheckError("LANGUAGETOOL_REAL_EXECUTION_FAILED")
            with mock.patch.object(controller.production_checks, "run_all", side_effect=hard):
                with self.assertRaisesRegex(controller.Fail, "FULL_CHECK_HARD_BLOCK:LANGUAGETOOL_REAL_EXECUTION_FAILED"):
                    controller.cmd_fullcheck(workspace)

            state = json.loads((workspace / "state.json").read_text(encoding="utf-8"))
            self.assertEqual(state["phase"], "CHECK_REQUIRED")
            self.assertNotEqual(state.get("checks", {}).get("status"), "PASS")

    def test_seven_item_batch_repairs_only_failed_item_and_collects_once(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            snapshot = Path(__file__).resolve().parent / "live_fixture" / "wordpress_snapshot.json"
            state_paths = []
            per_slot_calls = {}

            def fake_run_all(repo, state, fact_pack, production_plan_item):
                slot = state["article"]["plan_slot"]
                count = per_slot_calls.get(slot, 0) + 1
                per_slot_calls[slot] = count
                if state["article"]["title"] == "Mistcontainer mit Deckel wählen" and count == 1:
                    raise controller.production_checks.RepairRequired(
                        "languagetool",
                        [{"error_code": "LANGUAGETOOL_FINDING", "rule_id": "GERMAN_SPELLER_RULE"}],
                    )
                return {"contract": "SYSTEM4_FULL_PRODUCTION_CHECK_V1", "status": "PASS"}

            with mock.patch.object(controller.production_checks, "run_all", side_effect=fake_run_all) as run_all:
                for index in range(7):
                    workspace = root / f"item{index}"
                    controller.cmd_ingress(snapshot, workspace, index)
                    controller.cmd_research(
                        workspace,
                        write_stage_file(root, f"research-{index}.txt", (f"Research {index} ") * 8),
                    )
                    controller.cmd_facts(
                        workspace,
                        write_stage_file(root, f"facts-{index}.txt", (f"Facts {index} ") * 8),
                    )
                    bind_minimal_context(workspace, index)
                    draft = write_stage_file(root, f"draft-{index}.md", f"# Artikel {index}\n\nEntwurf {index}")
                    controller.cmd_draft(workspace, draft)
                    result = controller.cmd_fullcheck(workspace)
                    if result == 3:
                        draft.write_text(f"# Artikel {index}\n\nKorrigierter Entwurf {index}", encoding="utf-8")
                        controller.cmd_draft(workspace, draft)
                        self.assertEqual(controller.cmd_fullcheck(workspace), 0)
                    else:
                        self.assertEqual(result, 0)
                    state_paths.append(workspace / "state.json")

                self.assertEqual(run_all.call_count, 8)

            revisions = [json.loads(path.read_text(encoding="utf-8"))["revision"] for path in state_paths]
            self.assertEqual(revisions, [1, 1, 2, 1, 1, 1, 1])
            self.assertEqual(sum(per_slot_calls.values()), 8)

            out = root / "batch"
            result = batch_gate.collect_batch(snapshot, state_paths, out)
            self.assertEqual(result["status"], "SYSTEM4_BATCH_FULL_PASS_COLLECTED")
            self.assertEqual(result["article_count"], 7)
            self.assertEqual(
                result["batch_sha256"],
                "7f2e3290b6ac78ac7df1644395e57ac72f02dc1373e390eb2e532e57a8ce916a",
            )
            self.assertFalse(result["publish_allowed"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
