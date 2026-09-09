import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from p40_handoff_controller import HandoffBlocked, REQUIRED, execute_handoff

SLOT="a"*64
BATCH="b"*64
CID="article:b94aa30f3f4063cb5f140a3e"
PLAN_ITEM_KEY="canonical-faq-001"

def request():
    return {
        "contract":"PFERDE_ATELIER_FACHWORKFLOW_HANDOFF_REQUEST_V1",
        "room_token":"ROOM",
        "batch_sha256":BATCH,
        "canonical_article_id":CID,
        "plan_slot":SLOT,
        "allowed_output_root":".pferde-quarantine/test/",
        "item_receipt_ref":".pferde-quarantine/test/ITEM_RECEIPT.json",
        "fachworkflow_pass_ref":".pferde-quarantine/test/FACHWORKFLOW_PASS.json",
        "contract_binding_ref":"control/startmaster0107/FACHWORKFLOW_CONTRACT_BINDING.json",
        "contract_binding_sha256":"c"*64,
        "stage_proofs":[{"stage":f"s{i}","ref":f"x{i}","sha256":"d"*64} for i in range(12)],
        "fact_pack":{"contract":"fixture"},
        "production_plan_item":{
            "canonical_article_id":CID,
            "plan_slot":SLOT,
            "plan_item_key":PLAN_ITEM_KEY,
        },
        "production_plan_header":{"contract":"production_plan_v4"},
        "workflow_release_item":{
            "canonical_article_id":CID,
            "plan_slot":SLOT,
        },
        "workflow_release_metadata":{"contract":"fixture"},
    }

def write(root,obj):
    p=root/"FACHWORKFLOW_HANDOFF_REQUEST.json"
    p.write_text(json.dumps(obj),encoding="utf-8")
    return p

class P40Tests(unittest.TestCase):
    def test_positive_existing_handoff_is_only_input(self):
        with tempfile.TemporaryDirectory() as td:
            p=write(Path(td),request())
            r=execute_handoff(p)
            self.assertEqual(r["status"],"HANDOFF_ITEM_PASS_NO_PUBLISH")
            self.assertEqual(r["input_truth"],"FACHWORKFLOW_HANDOFF_REQUEST.json")
            self.assertFalse(r["new_job_manifest_used"])
            self.assertEqual(r["canonical_article_id"],CID)
            self.assertEqual(r["plan_item_key"],PLAN_ITEM_KEY)
            self.assertFalse(r["publish_allowed"])

    def test_negative_extra_field(self):
        with tempfile.TemporaryDirectory() as td:
            x=request(); x["next_step"]="FREE"
            with self.assertRaisesRegex(HandoffBlocked,"FIELDS_INVALID"):
                execute_handoff(write(Path(td),x))

    def test_negative_missing_field(self):
        with tempfile.TemporaryDirectory() as td:
            x=request(); del x["fact_pack"]
            with self.assertRaisesRegex(HandoffBlocked,"FIELDS_INVALID"):
                execute_handoff(write(Path(td),x))

    def test_negative_plan_item_identity_mismatch_before_adapter(self):
        with tempfile.TemporaryDirectory() as td:
            x=request(); x["production_plan_item"]["canonical_article_id"]="OTHER"
            with self.assertRaisesRegex(HandoffBlocked,"PLAN_ITEM_IDENTITY_MISMATCH"):
                execute_handoff(write(Path(td),x))

    def test_negative_release_item_identity_mismatch_before_adapter(self):
        with tempfile.TemporaryDirectory() as td:
            x=request(); x["workflow_release_item"]["plan_slot"]="e"*64
            with self.assertRaisesRegex(HandoffBlocked,"RELEASE_ITEM_IDENTITY_MISMATCH"):
                execute_handoff(write(Path(td),x))

    def test_negative_wrong_plan_item_key_blocks_after_no_write_prepare(self):
        with tempfile.TemporaryDirectory() as td:
            x=request()
            x["production_plan_item"]["plan_item_key"]="WRONG-"+PLAN_ITEM_KEY
            with self.assertRaisesRegex(HandoffBlocked,"HANDOFF_PLAN_ITEM_KEY_NOT_BOUND_TO_PPM_PREPARE"):
                execute_handoff(write(Path(td),x))

    def test_negative_wrong_canonical_id_blocks_after_no_write_prepare(self):
        with tempfile.TemporaryDirectory() as td:
            x=request()
            wrong="article:wrong"
            x["canonical_article_id"]=wrong
            x["production_plan_item"]["canonical_article_id"]=wrong
            x["workflow_release_item"]["canonical_article_id"]=wrong
            with self.assertRaisesRegex(HandoffBlocked,"HANDOFF_CANONICAL_ID_NOT_BOUND_TO_PPM_PREPARE"):
                execute_handoff(write(Path(td),x))

    def test_negative_missing_plan_item_key_before_adapter(self):
        with tempfile.TemporaryDirectory() as td:
            x=request()
            del x["production_plan_item"]["plan_item_key"]
            with self.assertRaisesRegex(HandoffBlocked,"PLAN_ITEM_KEY_MISSING"):
                execute_handoff(write(Path(td),x))

    def test_no_manifest_or_route_api(self):
        source=Path(__file__).with_name("p40_handoff_controller.py").read_text(encoding="utf-8")
        self.assertNotIn("verify_job_manifest",source)
        self.assertNotIn("JOB_CONTRACT",source)
        self.assertNotIn("set_next_step",source)
        self.assertNotIn("choose_worker",source)
        self.assertNotIn("set_validator",source)
        self.assertNotIn("set_route",source)
        self.assertNotIn("set_engine",source)

if __name__=="__main__":
    unittest.main(verbosity=2)
