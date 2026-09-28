#!/usr/bin/env python3
from __future__ import annotations

import base64
import copy
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
REPO = HERE.parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import github_director
import progress_guard
import universal_reentry_guard

EXACT_EXISTING_BLOB_SHA1 = {
    "concept_agent/intake_bridge.py": "b857653bac827e378c5819f4387e55fa84530e9f",
    "concept_agent/production_bridge.py": "3ab8116c91be773cdf1db2a06f02c957d32ddc9c",
    "concept_agent/progress_guard.py": "aee4324f11fa8b0f4b865211359dcea0255c8d7f",
    "concept_agent/universal_reentry_guard.py": "504c7d5372eb4bfde12333fdd383198ce4d329b0",
    "concept_agent/full_workflow_gate.py": "cc78dea6c9108e30948bb36bdd82e4defcfd7f54",
    "control/startmaster0107/ZIELVERTRAG_REASONING_MEDIUM_MAX_STARTMASTER0107.json": "72631476977083d47fc5602cd02b069bf9706023",
    "concept_agent/current/CONCEPT_AGENT_RESEARCH_BOUND.json": "c5103b91f1f78013a7295a9240f8bb3811672e57",
    "concept_agent/current/PSERC_METADATA_SNAPSHOT.json": "3b3f07baf9bd12c128ccc1a6ff201ec884b4039d",
}

def git_blob_sha1(path: Path) -> str:
    raw = path.read_bytes()
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()

class GithubDirectorAcceptanceTests(unittest.TestCase):
    def _binding(self, count=2):
        items = []
        for i in range(count):
            slot = hashlib.sha256(f"slot-{i}".encode()).hexdigest()
            items.append({
                "item_index": i,
                "identity": {
                    "item_index": i,
                    "title": f"Artikel {i}",
                    "target_keyword": f"Keyword {i}",
                    "category": f"kategorie-{i}",
                    "article_type": "Beratung",
                    "plan_slot": slot,
                    "identity_sha256": hashlib.sha256(f"identity-{i}".encode()).hexdigest(),
                },
                "research_bound": {"item_index": i, "plan_slot": slot},
                "bound_work_sha256": hashlib.sha256(f"work-{i}".encode()).hexdigest(),
            })
        binding = {
            "contract": progress_guard.BINDING_CONTRACT,
            "status": "AUTHORING_READY",
            "batch_sha256": hashlib.sha256(b"batch").hexdigest(),
            "item_count": count,
            "source_intake_sha256": hashlib.sha256(b"intake").hexdigest(),
            "source_research_binding_sha256": hashlib.sha256(b"research").hexdigest(),
            "quality_authority": {"source": "UNCHANGED_TEST_BINDING"},
            "route_policy": {"publish_allowed": False},
            "progress_policy": {"checkpoint_required_before_every_action": True},
            "items": items,
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
            "phase": "AUTHORING_REQUIRED",
            "next_item_index": 0,
            "completed_items": [],
            "current_item": None,
            "previous_checkpoint_sha256": None,
            "drafts": [],
            "publish_allowed": False,
        }
        state["allowed_action"] = progress_guard.expected_action(binding, state)
        state["checkpoint_sha256"] = progress_guard.stable(state)
        return state

    def _capsule(self, binding, state, phase):
        index = state["next_item_index"]
        item = binding["items"][index]
        row = next(x for x in state["drafts"] if x["item_index"] == index)
        research = "research"
        facts = "facts"
        context_core = {"fact_pack": {"facts": []}, "production_plan_item": {"plan_slot": item["identity"]["plan_slot"]}}
        article = {
            "canonical_article_id": f"article:{index}",
            "item_index": index,
            **{k: item["identity"][k] for k in ("title", "target_keyword", "category", "article_type", "plan_slot")},
        }
        checks = {}
        last_error = None
        if phase == "REPAIR_REQUIRED":
            checks = {"status": "FAIL", "checked_draft_sha256": row["draft_sha256"]}
            last_error = "TEST_REPAIR_REQUIRED"
        inner = {
            "contract": universal_reentry_guard.STATE_CONTRACT,
            "source_snapshot_sha256": hashlib.sha256(b"snapshot").hexdigest(),
            "batch_sha256": binding["batch_sha256"],
            "article": article,
            "immutable_core_sha256": "",
            "publish_allowed": False,
            "phase": phase,
            "revision": row["revision"],
            "research": {"text": research, "sha256": hashlib.sha256(research.encode()).hexdigest()},
            "facts": {"text": facts, "sha256": hashlib.sha256(facts.encode()).hexdigest()},
            "production_context": {**context_core, "sha256": universal_reentry_guard.stable(context_core)},
            "authoring_contract": {"contract": "UNCHANGED_TEST_BOUND"},
            "draft_markdown": row["content_utf8"],
            "draft_sha256": row["draft_sha256"],
            "checks": checks,
            "last_error": last_error,
            "release_prepared": None,
            "released": False,
        }
        inner["immutable_core_sha256"] = universal_reentry_guard.stable({
            "contract": inner["contract"],
            "source_snapshot_sha256": inner["source_snapshot_sha256"],
            "batch_sha256": inner["batch_sha256"],
            "article": inner["article"],
        })
        raw = (json.dumps(inner, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()
        file_row = {
            "path": "state.json",
            "size": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "base64": base64.b64encode(raw).decode(),
        }
        normalized = [{"path": "state.json", "size": len(raw), "sha256": file_row["sha256"]}]
        return {
            "contract": universal_reentry_guard.CAPSULE_CONTRACT,
            "status": "RECOVERY_CAPSULE_READY",
            "workspace_identity": universal_reentry_guard._capsule_identity(inner),
            "file_count": 1,
            "tree_sha256": universal_reentry_guard._tree_hash(normalized),
            "files": [file_row],
            "publish_allowed": False,
        }

    def _receipt(self, ticket, **extra):
        value = {
            "contract": github_director.RECEIPT_CONTRACT,
            "status": "COMPLETED",
            "ticket_sha256": ticket["ticket_sha256"],
            "checkpoint_sha256": ticket["checkpoint_sha256"],
            "allowed_action_sha256": ticket["allowed_action_sha256"],
            "worker_role": ticket["worker_role"],
            "reasoning_effort": ticket["reasoning_effort"],
            "publish_allowed": False,
            "workflow_change_requested": False,
            "quality_gate_change_requested": False,
            "next_action": None,
        }
        value.update(extra)
        return value

    def _artifact_receipt(self, ticket, path, **extra):
        return self._receipt(
            ticket,
            artifact_relpath=path.name,
            artifact_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
            **extra,
        )

    def _next_capsule(self, binding, new_state):
        action = new_state["allowed_action"]["action"]
        if action == "RUN_CHECKER":
            return self._capsule(binding, new_state, "CHECK_REQUIRED")
        if action == "REPAIR_DRAFT":
            return self._capsule(binding, new_state, "REPAIR_REQUIRED")
        return None

    def test_00_existing_workflow_and_goal_contract_are_byte_identical(self):
        for rel, expected in EXACT_EXISTING_BLOB_SHA1.items():
            self.assertEqual(git_blob_sha1(REPO / rel), expected, rel)

    def test_01_goal_contract_positive_and_negative(self):
        goal = json.loads((REPO / "control/startmaster0107/ZIELVERTRAG_REASONING_MEDIUM_MAX_STARTMASTER0107.json").read_text())
        github_director.verify_goal_contract(goal)
        self.assertEqual(set(goal), {
            "contract", "startmaster", "goal", "default_reasoning", "applies_to",
            "escalate_above_medium_only_if", "never_trade_for_medium",
            "downgrade_for_cost_or_speed_without_gate_parity", "measurement",
            "success", "hard_execution_principle", "immutable_entrance_layer",
        })
        for key in goal:
            broken = copy.deepcopy(goal)
            value = broken[key]
            if isinstance(value, list):
                broken[key] = value[:-1]
            elif isinstance(value, str):
                broken[key] = value + "_BROKEN"
            else:
                broken[key] = None
            with self.assertRaises(github_director.Blocked, msg=key):
                github_director.verify_goal_contract(broken)
        broken = copy.deepcopy(goal)
        broken["unexpected_clause"] = True
        with self.assertRaises(github_director.Blocked):
            github_director.verify_goal_contract(broken)

    def test_02_restart_before_result_reissues_exact_same_action(self):
        binding = self._binding(1)
        checkpoint = self._checkpoint(binding)
        with tempfile.TemporaryDirectory() as td:
            cp = Path(td) / "checkpoint.json"
            progress_guard.write(cp, checkpoint)
            first = github_director.resume(binding, cp)
            second = github_director.resume(binding, cp)
            self.assertEqual(first["ticket"], second["ticket"])
            self.assertEqual(first["checkpoint"], second["checkpoint"])
            self.assertEqual(first["ticket"]["reasoning_effort"], "medium")
            self.assertIs(first["ticket"]["director_may_choose_action"], False)
            self.assertEqual(first["ticket"]["director_content_authority"], "NONE")
            self.assertEqual(first["ticket"]["director_quality_authority"], "NONE")

    def test_03_forward_repair_second_article_pserc_endstempel_stop(self):
        binding = self._binding(2)
        checkpoint = self._checkpoint(binding)
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            cp = root / "checkpoint.json"
            progress_guard.write(cp, checkpoint)
            current = github_director.resume(binding, cp)

            # Article 0 draft.
            state, decision, ticket = current["checkpoint"], current["decision"], current["ticket"]
            slot = binding["items"][0]["identity"]["plan_slot"]
            draft0 = root / f"00_{slot}.md"
            draft0.write_text("Artikel 0 v1", encoding="utf-8")
            predicted = progress_guard.record_draft(binding, state, decision, 0, draft0)
            current = github_director.persist_and_continue(
                binding, state, decision, ticket,
                self._artifact_receipt(ticket, draft0, workspace_capsule=self._next_capsule(binding, predicted)),
                root, cp,
            )

            # LT PASS.
            state, decision, ticket = current["checkpoint"], current["decision"], current["ticket"]
            sha0 = hashlib.sha256(draft0.read_bytes()).hexdigest()
            result = {"status": "PASS", "content_sha256": sha0}
            predicted = progress_guard.record_check(binding, state, decision, 0, "LT68", result, draft0)
            current = github_director.persist_and_continue(
                binding, state, decision, ticket,
                self._artifact_receipt(ticket, draft0, result=result, workspace_capsule=self._next_capsule(binding, predicted)),
                root, cp,
            )

            # PPM -> Repair.
            state, decision, ticket = current["checkpoint"], current["decision"], current["ticket"]
            result = {"status": "REPAIR_REQUIRED", "content_sha256": sha0, "findings": ["test"]}
            predicted = progress_guard.record_check(binding, state, decision, 0, "PPM679", result, draft0)
            current = github_director.persist_and_continue(
                binding, state, decision, ticket,
                self._artifact_receipt(ticket, draft0, result=result, workspace_capsule=self._next_capsule(binding, predicted)),
                root, cp,
            )
            self.assertEqual(current["ticket"]["allowed_action"]["action"], "REPAIR_DRAFT")
            self.assertEqual(current["ticket"]["allowed_action"]["item_index"], 0)

            # Same article repair -> LT -> PPM.
            state, decision, ticket = current["checkpoint"], current["decision"], current["ticket"]
            draft0.write_text("Artikel 0 v2", encoding="utf-8")
            predicted = progress_guard.replace_draft(binding, state, decision, 0, draft0)
            current = github_director.persist_and_continue(
                binding, state, decision, ticket,
                self._artifact_receipt(ticket, draft0, workspace_capsule=self._next_capsule(binding, predicted)),
                root, cp,
            )
            for checker in ("LT68", "PPM679"):
                state, decision, ticket = current["checkpoint"], current["decision"], current["ticket"]
                sha0 = hashlib.sha256(draft0.read_bytes()).hexdigest()
                result = {"status": "PASS", "content_sha256": sha0}
                predicted = progress_guard.record_check(binding, state, decision, 0, checker, result, draft0)
                current = github_director.persist_and_continue(
                    binding, state, decision, ticket,
                    self._artifact_receipt(ticket, draft0, result=result, workspace_capsule=self._next_capsule(binding, predicted)),
                    root, cp,
                )
            self.assertEqual(current["ticket"]["allowed_action"]["action"], "WRITE_DRAFT")
            self.assertEqual(current["ticket"]["allowed_action"]["item_index"], 1)

            # Article 1 clean pass.
            state, decision, ticket = current["checkpoint"], current["decision"], current["ticket"]
            slot = binding["items"][1]["identity"]["plan_slot"]
            draft1 = root / f"01_{slot}.md"
            draft1.write_text("Artikel 1 v1", encoding="utf-8")
            predicted = progress_guard.record_draft(binding, state, decision, 1, draft1)
            current = github_director.persist_and_continue(
                binding, state, decision, ticket,
                self._artifact_receipt(ticket, draft1, workspace_capsule=self._next_capsule(binding, predicted)),
                root, cp,
            )
            for checker in ("LT68", "PPM679"):
                state, decision, ticket = current["checkpoint"], current["decision"], current["ticket"]
                sha1 = hashlib.sha256(draft1.read_bytes()).hexdigest()
                result = {"status": "PASS", "content_sha256": sha1}
                predicted = progress_guard.record_check(binding, state, decision, 1, checker, result, draft1)
                current = github_director.persist_and_continue(
                    binding, state, decision, ticket,
                    self._artifact_receipt(ticket, draft1, result=result, workspace_capsule=self._next_capsule(binding, predicted)),
                    root, cp,
                )

            # Existing PSERC / ENDSTEMPEL result contracts.
            state, decision, ticket = current["checkpoint"], current["decision"], current["ticket"]
            pserc = {
                "contract": progress_guard.BATCH_STAGE_RESULT_CONTRACT,
                "stage": "PSERC",
                "status": "PASS",
                "batch_sha256": state["batch_sha256"],
                "source_checkpoint_sha256": state["checkpoint_sha256"],
                "evidence_sha256": "1" * 64,
                "pserc_package_sha256": "2" * 64,
                "publish_allowed": False,
            }
            current = github_director.persist_and_continue(
                binding, state, decision, ticket, self._receipt(ticket, result=pserc), root, cp
            )
            state, decision, ticket = current["checkpoint"], current["decision"], current["ticket"]
            end = {
                "contract": progress_guard.BATCH_STAGE_RESULT_CONTRACT,
                "stage": "ENDSTEMPEL",
                "status": "PASS",
                "batch_sha256": state["batch_sha256"],
                "source_checkpoint_sha256": state["checkpoint_sha256"],
                "evidence_sha256": "3" * 64,
                "final_file_sha256": "4" * 64,
                "publish_allowed": False,
            }
            current = github_director.persist_and_continue(
                binding, state, decision, ticket, self._receipt(ticket, result=end), root, cp
            )
            self.assertEqual(current["status"], "STOP")
            self.assertTrue(current["ticket"]["terminal"])
            self.assertEqual(current["ticket"]["allowed_action"]["action"], "STOP")

            # Fresh process after any pause sees exact terminal state.
            restarted = github_director.resume(binding, cp)
            self.assertEqual(restarted["status"], "STOP")
            self.assertEqual(restarted["checkpoint"], current["checkpoint"])
            self.assertEqual(restarted["ticket"], current["ticket"])

    def test_04_negative_freedom_matrix(self):
        binding = self._binding(1)
        checkpoint = self._checkpoint(binding)
        decision = universal_reentry_guard.build(binding, checkpoint)
        ticket = github_director.issue(binding, checkpoint, decision)
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            slot = binding["items"][0]["identity"]["plan_slot"]
            draft = root / f"00_{slot}.md"
            draft.write_text("x", encoding="utf-8")
            base = self._artifact_receipt(ticket, draft)
            for key, value in (
                ("publish_allowed", True),
                ("workflow_change_requested", True),
                ("quality_gate_change_requested", True),
                ("reasoning_effort", "low"),
                ("next_action", {"action": "RUN_PSERC"}),
                ("allowed_action_sha256", "0" * 64),
                ("checkpoint_sha256", "0" * 64),
                ("worker_role", "OTHER"),
                ("ticket_sha256", "0" * 64),
            ):
                row = copy.deepcopy(base)
                row[key] = value
                with self.assertRaises(github_director.Blocked, msg=key):
                    github_director.accept(binding, checkpoint, decision, ticket, row, root)

            extra = copy.deepcopy(base)
            extra["shell_command"] = "anything"
            with self.assertRaisesRegex(github_director.Blocked, "EXTRA_FIELDS_FORBIDDEN"):
                github_director.accept(binding, checkpoint, decision, ticket, extra, root)

            bad_hash = copy.deepcopy(base)
            bad_hash["artifact_sha256"] = "0" * 64
            with self.assertRaisesRegex(github_director.Blocked, "ARTIFACT_HASH_MISMATCH"):
                github_director.accept(binding, checkpoint, decision, ticket, bad_hash, root)

            bad_ticket = copy.deepcopy(ticket)
            bad_ticket["allowed_action"] = {"action": "RUN_PSERC", "item_count": 1}
            with self.assertRaises(github_director.Blocked):
                github_director.verify_ticket(binding, checkpoint, decision, bad_ticket)

            outside = root.parent / "outside-director-test.md"
            outside.write_text("outside", encoding="utf-8")
            escape = self._receipt(
                ticket,
                artifact_relpath="../outside-director-test.md",
                artifact_sha256=hashlib.sha256(outside.read_bytes()).hexdigest(),
            )
            with self.assertRaises(github_director.Blocked):
                github_director.accept(binding, checkpoint, decision, ticket, escape, root)

    def test_05_stale_replay_missing_checkpoint_and_stop_fail_closed(self):
        binding = self._binding(1)
        checkpoint = self._checkpoint(binding)
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            cp = root / "checkpoint.json"
            progress_guard.write(cp, checkpoint)
            current = github_director.resume(binding, cp)
            state, decision, ticket = current["checkpoint"], current["decision"], current["ticket"]
            slot = binding["items"][0]["identity"]["plan_slot"]
            draft = root / f"00_{slot}.md"
            draft.write_text("first", encoding="utf-8")
            predicted = progress_guard.record_draft(binding, state, decision, 0, draft)
            receipt = self._artifact_receipt(ticket, draft, workspace_capsule=self._next_capsule(binding, predicted))
            github_director.persist_and_continue(binding, state, decision, ticket, receipt, root, cp)
            with self.assertRaisesRegex(github_director.Blocked, "STALE_CHECKPOINT_REPLAY_BLOCKED"):
                github_director.persist_and_continue(binding, state, decision, ticket, receipt, root, cp)
            cp.unlink()
            with self.assertRaisesRegex(github_director.Blocked, "DURABLE_CHECKPOINT_MISSING"):
                github_director.resume(binding, cp)

    def test_06_restart_inside_article_and_repair_uses_only_saved_checkpoint(self):
        binding = self._binding(1)
        checkpoint = self._checkpoint(binding)
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            cp = root / "checkpoint.json"
            progress_guard.write(cp, checkpoint)
            current = github_director.resume(binding, cp)

            # Persist a draft, then simulate a completely fresh process before LT.
            state, decision, ticket = current["checkpoint"], current["decision"], current["ticket"]
            slot = binding["items"][0]["identity"]["plan_slot"]
            draft = root / f"00_{slot}.md"
            draft.write_text("Artikel vor Unterbrechung", encoding="utf-8")
            predicted = progress_guard.record_draft(binding, state, decision, 0, draft)
            capsule = self._next_capsule(binding, predicted)
            current = github_director.persist_and_continue(
                binding, state, decision, ticket,
                self._artifact_receipt(ticket, draft, workspace_capsule=capsule),
                root, cp,
            )
            restarted = github_director.resume(binding, cp)
            self.assertEqual(restarted["checkpoint"], current["checkpoint"])
            self.assertEqual(restarted["ticket"], current["ticket"])
            self.assertEqual(restarted["ticket"]["allowed_action"]["checker"], "LT68")

            # Move to PPM and force repair.
            state, decision, ticket = restarted["checkpoint"], restarted["decision"], restarted["ticket"]
            draft_sha = hashlib.sha256(draft.read_bytes()).hexdigest()
            lt = {"status": "PASS", "content_sha256": draft_sha}
            predicted = progress_guard.record_check(binding, state, decision, 0, "LT68", lt, draft)
            capsule = self._next_capsule(binding, predicted)
            current = github_director.persist_and_continue(
                binding, state, decision, ticket,
                self._artifact_receipt(ticket, draft, result=lt, workspace_capsule=capsule),
                root, cp,
            )
            state, decision, ticket = current["checkpoint"], current["decision"], current["ticket"]
            ppm = {"status": "REPAIR_REQUIRED", "content_sha256": draft_sha, "findings": ["test"]}
            predicted = progress_guard.record_check(binding, state, decision, 0, "PPM679", ppm, draft)
            repair_capsule = self._next_capsule(binding, predicted)
            current = github_director.persist_and_continue(
                binding, state, decision, ticket,
                self._artifact_receipt(ticket, draft, result=ppm, workspace_capsule=repair_capsule),
                root, cp,
            )

            # Fresh process in REPAIR_REQUIRED must stay on the same article and repair.
            restarted = github_director.resume(binding, cp)
            self.assertEqual(restarted["checkpoint"], current["checkpoint"])
            self.assertEqual(restarted["ticket"], current["ticket"])
            self.assertEqual(restarted["ticket"]["allowed_action"]["action"], "REPAIR_DRAFT")
            self.assertEqual(restarted["ticket"]["allowed_action"]["item_index"], 0)

    def test_065_missing_or_tampered_checkpoint_capsule_blocks(self):
        binding = self._binding(1)
        checkpoint = self._checkpoint(binding)
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            cp = root / "checkpoint.json"
            progress_guard.write(cp, checkpoint)
            current = github_director.resume(binding, cp)

            state, decision, ticket = current["checkpoint"], current["decision"], current["ticket"]
            slot = binding["items"][0]["identity"]["plan_slot"]
            draft = root / f"00_{slot}.md"
            draft.write_text("Artikel", encoding="utf-8")
            predicted = progress_guard.record_draft(binding, state, decision, 0, draft)
            capsule = self._next_capsule(binding, predicted)
            current = github_director.persist_and_continue(
                binding, state, decision, ticket,
                self._artifact_receipt(ticket, draft, workspace_capsule=capsule),
                root, cp,
            )

            sidecar = github_director._capsule_path(cp, current["checkpoint"]["checkpoint_sha256"])
            self.assertTrue(sidecar.is_file())

            saved = sidecar.read_bytes()
            sidecar.unlink()
            with self.assertRaisesRegex(github_director.Blocked, "BOUND_WORKSPACE_CAPSULE_MISSING"):
                github_director.resume(binding, cp)

            sidecar.write_bytes(saved)
            wrapper = json.loads(sidecar.read_text(encoding="utf-8"))
            wrapper["capsule_sha256"] = "0" * 64
            progress_guard.write(sidecar, wrapper)
            with self.assertRaisesRegex(github_director.Blocked, "CAPSULE_BINDING_HASH_MISMATCH"):
                github_director.resume(binding, cp)


    def test_066_full16_restart_repair_matrix(self):
        binding = self._binding(16)
        checkpoint = self._checkpoint(binding)
        repair_indices = {1, 5, 9, 13, 15}
        repaired = set()
        steps = 0

        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            cp = root / "checkpoint.json"
            progress_guard.write(cp, checkpoint)
            current = github_director.resume(binding, cp)

            while current["ticket"]["allowed_action"]["action"] != "STOP":
                # Any interruption before the current worker result must reissue exactly the same ticket.
                before = github_director.resume(binding, cp)
                self.assertEqual(before["ticket"], current["ticket"])
                self.assertEqual(before["checkpoint"], current["checkpoint"])

                state, decision, ticket = current["checkpoint"], current["decision"], current["ticket"]
                action = ticket["allowed_action"]
                name = action["action"]

                if name == "WRITE_DRAFT":
                    index = action["item_index"]
                    slot = binding["items"][index]["identity"]["plan_slot"]
                    draft = root / f"{index:02d}_{slot}.md"
                    draft.write_text(f"Artikel {index} v1", encoding="utf-8")
                    predicted = progress_guard.record_draft(binding, state, decision, index, draft)
                    receipt = self._artifact_receipt(
                        ticket, draft, workspace_capsule=self._next_capsule(binding, predicted)
                    )
                elif name == "RUN_CHECKER":
                    index = action["item_index"]
                    slot = binding["items"][index]["identity"]["plan_slot"]
                    draft = root / f"{index:02d}_{slot}.md"
                    digest = hashlib.sha256(draft.read_bytes()).hexdigest()
                    if action["checker"] == "PPM679" and index in repair_indices and index not in repaired:
                        result = {"status": "REPAIR_REQUIRED", "content_sha256": digest, "findings": ["matrix"]}
                    else:
                        result = {"status": "PASS", "content_sha256": digest}
                    predicted = progress_guard.record_check(
                        binding, state, decision, index, action["checker"], result, draft
                    )
                    receipt = self._artifact_receipt(
                        ticket, draft, result=result, workspace_capsule=self._next_capsule(binding, predicted)
                    )
                elif name == "REPAIR_DRAFT":
                    index = action["item_index"]
                    slot = binding["items"][index]["identity"]["plan_slot"]
                    draft = root / f"{index:02d}_{slot}.md"
                    draft.write_text(f"Artikel {index} v2", encoding="utf-8")
                    repaired.add(index)
                    predicted = progress_guard.replace_draft(binding, state, decision, index, draft)
                    receipt = self._artifact_receipt(
                        ticket, draft, workspace_capsule=self._next_capsule(binding, predicted)
                    )
                elif name == "RUN_PSERC":
                    result = {
                        "contract": progress_guard.BATCH_STAGE_RESULT_CONTRACT,
                        "stage": "PSERC", "status": "PASS",
                        "batch_sha256": state["batch_sha256"],
                        "source_checkpoint_sha256": state["checkpoint_sha256"],
                        "evidence_sha256": "5" * 64,
                        "pserc_package_sha256": "6" * 64,
                        "publish_allowed": False,
                    }
                    receipt = self._receipt(ticket, result=result)
                elif name == "RUN_ENDSTEMPEL":
                    result = {
                        "contract": progress_guard.BATCH_STAGE_RESULT_CONTRACT,
                        "stage": "ENDSTEMPEL", "status": "PASS",
                        "batch_sha256": state["batch_sha256"],
                        "source_checkpoint_sha256": state["checkpoint_sha256"],
                        "evidence_sha256": "7" * 64,
                        "final_file_sha256": "8" * 64,
                        "publish_allowed": False,
                    }
                    receipt = self._receipt(ticket, result=result)
                else:
                    self.fail("unexpected action: " + name)

                current = github_director.persist_and_continue(
                    binding, state, decision, ticket, receipt, root, cp
                )
                steps += 1

                # Any interruption after the accepted transition must resume exactly from the new saved point.
                after = github_director.resume(binding, cp)
                self.assertEqual(after["ticket"], current["ticket"])
                self.assertEqual(after["checkpoint"], current["checkpoint"])

                # The old ticket/result can never be accepted twice.
                with self.assertRaisesRegex(github_director.Blocked, "STALE_CHECKPOINT_REPLAY_BLOCKED"):
                    github_director.persist_and_continue(
                        binding, state, decision, ticket, receipt, root, cp
                    )

            self.assertEqual(steps, 65)
            self.assertEqual(repaired, repair_indices)
            self.assertEqual(len(current["checkpoint"]["completed_items"]), 16)
            self.assertEqual(current["status"], "STOP")
            self.assertEqual(current["ticket"]["allowed_action"]["action"], "STOP")
            self.assertTrue(current["ticket"]["terminal"])


    def test_07_stop_is_the_only_terminal_exit(self):
        binding = self._binding(1)
        checkpoint = self._checkpoint(binding)
        decision = universal_reentry_guard.build(binding, checkpoint)
        ticket = github_director.issue(binding, checkpoint, decision)
        self.assertFalse(ticket["terminal"])
        self.assertIsNotNone(ticket["worker_role"])
        with self.assertRaises(github_director.Blocked):
            github_director._worker_role({"action": "SOMETHING_ELSE"})
        with self.assertRaisesRegex(github_director.Blocked, "CHECKER_UNKNOWN"):
            github_director._worker_role({"action": "RUN_CHECKER", "checker": "OTHER"})

    def test_08_each_existing_step_has_one_fixed_worker_role(self):
        cases = (
            ({"action": "WRITE_DRAFT"}, "WRITE_DRAFT_WORKER"),
            ({"action": "RUN_CHECKER", "checker": "LT68"}, "LT68_WORKER"),
            ({"action": "RUN_CHECKER", "checker": "PPM679"}, "PPM679_WORKER"),
            ({"action": "REPAIR_DRAFT"}, "REPAIR_DRAFT_WORKER"),
            ({"action": "RUN_PSERC"}, "PSERC_WORKER"),
            ({"action": "RUN_ENDSTEMPEL"}, "ENDSTEMPEL_WORKER"),
            ({"action": "STOP"}, None),
        )
        roles = []
        for action, expected in cases:
            actual = github_director._worker_role(action)
            self.assertEqual(actual, expected)
            if actual is not None:
                roles.append(actual)
        self.assertEqual(len(roles), len(set(roles)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
