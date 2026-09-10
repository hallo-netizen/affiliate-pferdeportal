from __future__ import annotations

import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]


def module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


handoff = module(HERE / "fachworkflow_proof_handoff.py", "fachworkflow_handoff_test")
dual = module(HERE / "STARTMASTER0107_DUAL_ROOTFIX_REPAIR.py", "dual_rootfix_handoff_test")


class FachworkflowProofHandoffTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp.name)
        for rel in (dual.SELF_REL, dual.HANDOFF_REL, dual.PROMPT_REL):
            target = self.repo / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(REPO / rel, target)

    def tearDown(self):
        self.temp.cleanup()

    def write_json(self, path: Path, value: dict):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def prepare(self, batch_char: str, slot_char: str, article: str):
        batch, slot = batch_char * 64, slot_char * 64
        root = f"out/{batch_char}/"
        runtime = self.repo / dual.RUNTIME_STATE_REL
        self.write_json(runtime, {"batch_sha256": batch})
        rows = []
        for stage in handoff.STAGES:
            artifact_ref = root + stage + ".artifact"
            artifact = self.repo / artifact_ref
            artifact.parent.mkdir(parents=True, exist_ok=True)
            artifact.write_text("real output " + stage, encoding="utf-8")
            proof_ref = root + stage + ".proof.json"
            proof = {"contract": handoff.STAGE_CONTRACT, "status": "PASS", "batch_sha256": batch,
                     "canonical_article_id": article, "plan_slot": slot, "stage": stage,
                     "execution_performed": True, "input_sha256": "1" * 64,
                     "execution_evidence": ["stage runner completed with verified output"],
                     "artifacts": [{"ref": artifact_ref, "sha256": handoff._sha(artifact)}],
                     "content_or_quality_rules_changed": False, "publish_allowed": False}
            self.write_json(self.repo / proof_ref, proof)
            rows.append({"stage": stage, "ref": proof_ref, "sha256": handoff._sha(self.repo / proof_ref)})
        action = {"allowed_output_root": root, "item_receipt_schema": {}}
        item = {"canonical_article_id": article, "plan_slot": slot}
        action = dual.augment_current_action(self.repo, action, item)
        meta = {"article_origin_policy": "POST_TEXT_SIGNED_0039_ORIGIN_AND_NO_REWRITE",
                "authoring_prompt_sha256": "2" * 64, "authoring_role": "CHAT_OR_APPROVED_RESEARCH_TEXT_PROCESS",
                "content_generation_performed_by_supervisor": False, "contract": dual.RELEASE_CONTRACT,
                "created_at_utc": "2026-09-03T00:00:00+00:00", "exact_five_batch_sha256": batch,
                "exact_five_item_count": 1, "frozen_workflow_sha256": "3" * 64, "nullpunkt": {},
                "nullpunkt_sha256": "4" * 64, "ppm_baseline_sha256": "5" * 64, "ppm_version": "6.7.9",
                "research_evidence_policy": "BOUND_EXISTING_FACHWORKFLOW_ONLY", "sequence": 107008,
                "status": "PASS", "wordpress_write_performed": False}
        request = {"contract": handoff.CONTRACT, "room_token": "R_D_1_01", "batch_sha256": batch,
                   "canonical_article_id": article, "plan_slot": slot, "allowed_output_root": root,
                   "item_receipt_ref": root + "ITEM_RECEIPT.json",
                   "fachworkflow_pass_ref": action["item_receipt_schema"]["fachworkflow_pass_ref"],
                   "contract_binding_ref": dual.SELF_REL, "contract_binding_sha256": dual.binding_sha(self.repo),
                   "stage_proofs": rows, "fact_pack": {"contract": "canonical_fact_pack_v1"},
                   "production_plan_item": item, "production_plan_header": {"contract": "production_plan_v4"},
                   "workflow_release_item": item, "workflow_release_metadata": meta}
        request_ref = root + "FACHWORKFLOW_HANDOFF_REQUEST.json"
        self.write_json(self.repo / request_ref, request)
        return item, action, request_ref, rows

    def test_two_identities_use_same_handoff_and_validate(self):
        for batch, slot, article in (("a", "b", "article:synthetic-one"), ("c", "d", "article:synthetic-two")):
            item, action, request_ref, _ = self.prepare(batch, slot, article)
            result = handoff.materialize(self.repo, request_ref)
            self.assertEqual("FACHWORKFLOW_PROOF_HANDOFF_PASS", result["status"])
            receipt = handoff._load(self.repo / result["item_receipt_ref"])
            dual.validate_fachworkflow_pass(self.repo, action, item, receipt)

    def test_missing_wrong_and_tampered_stage_proofs_fail_closed(self):
        _, _, request_ref, rows = self.prepare("e", "f", "article:negative")
        request = handoff._load(self.repo / request_ref)
        request["stage_proofs"] = request["stage_proofs"][:-1]
        self.write_json(self.repo / request_ref, request)
        with self.assertRaises(handoff.Blocked): handoff.materialize(self.repo, request_ref)
        _, _, request_ref, rows = self.prepare("e", "f", "article:negative")
        proof = handoff._load(self.repo / rows[0]["ref"]); proof["canonical_article_id"] = "article:wrong"
        self.write_json(self.repo / rows[0]["ref"], proof); rows[0]["sha256"] = handoff._sha(self.repo / rows[0]["ref"])
        request = handoff._load(self.repo / request_ref); request["stage_proofs"] = rows; self.write_json(self.repo / request_ref, request)
        with self.assertRaises(handoff.Blocked): handoff.materialize(self.repo, request_ref)
        _, _, request_ref, rows = self.prepare("e", "f", "article:negative")
        (self.repo / rows[0]["ref"]).write_text("tampered", encoding="utf-8")
        with self.assertRaises(handoff.Blocked): handoff.materialize(self.repo, request_ref)


if __name__ == "__main__":
    unittest.main()
