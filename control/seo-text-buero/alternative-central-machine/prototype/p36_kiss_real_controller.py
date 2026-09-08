#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from p10_batch_resume import verify_job_manifest

HERE=Path(__file__).resolve().parent
LAB_ITEM_ADAPTER=HERE/"p22_signed_normal_draft_integration.py"
ITEM_PASS_STATUS="P22_SIGNED_NORMAL_DRAFT_BOUNDARY_PASS"

class ControllerBlocked(RuntimeError):
    pass

def _parse_status(output:str,status:str)->dict:
    decoder=json.JSONDecoder()
    for index,ch in enumerate(output):
        if ch!="{":
            continue
        try:
            obj,_=decoder.raw_decode(output[index:])
        except Exception:
            continue
        if isinstance(obj,dict) and obj.get("status")==status:
            return obj
    raise ControllerBlocked("ITEM_ADAPTER_PASS_MISSING")

def _run_fixed_item(job_id:str,item_id:str)->dict:
    if not LAB_ITEM_ADAPTER.is_file():
        raise ControllerBlocked("FIXED_ITEM_ADAPTER_MISSING")
    proc=subprocess.run(
        [sys.executable,str(LAB_ITEM_ADAPTER),"--job-id",job_id,"--expected-item-id",item_id],
        cwd=HERE.parents[3],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=300,
    )
    if proc.returncode!=0:
        raise ControllerBlocked("FIXED_ITEM_ADAPTER_FAILED")
    proof=_parse_status(proc.stdout,ITEM_PASS_STATUS)
    required_true=(
        "prepare_no_write",
        "external_signature_verified",
        "exact_one_draft_written",
        "publish_count_unchanged",
        "post_signature_tamper_blocked",
        "post_signature_rehash_tamper_blocked",
    )
    if any(proof.get(k) is not True for k in required_true):
        raise ControllerBlocked("FIXED_ITEM_ADAPTER_INVARIANT_FAILED")
    return proof

def execute_signed_job(
    job_path:Path,
    signature_path:Path,
    public_key_path:Path,
)->dict:
    job=verify_job_manifest(job_path,signature_path,public_key_path)

    # No route selection and no parallel branch: exact manifest order only.
    completed=[]
    for ordinal,item in enumerate(job["items"],1):
        proof=_run_fixed_item(job["job_id"],item["item_id"])
        if proof.get("job_id")!=job["job_id"] or proof.get("item_id")!=item["item_id"]:
            raise ControllerBlocked("ITEM_ADAPTER_IDENTITY_MISMATCH")
        completed.append({
            "ordinal":ordinal,
            "item_id":item["item_id"],
            "status":"PASS",
            "prepared_fingerprint":proof["planned_write_fingerprint"],
            "release_content_sha256":proof["release_content_sha256"],
            "publish_allowed":False,
        })

    return {
        "contract":"ALT_KISS_REAL_CONTROLLER_RECEIPT_V1",
        "status":"JOB_PASS_NO_PUBLISH",
        "job_id":job["job_id"],
        "item_count":len(job["items"]),
        "completed_count":len(completed),
        "processing_model":"FIXED_SEQUENTIAL_ITEM_ORDER",
        "route_runtime_selectable":False,
        "worker_runtime_selectable":False,
        "validator_runtime_selectable":False,
        "repair_path_runtime_selectable":False,
        "publish_allowed":False,
        "items":completed,
    }

def main(argv:list[str])->int:
    if len(argv)!=4:
        raise SystemExit("usage: p36_kiss_real_controller.py JOB.json JOB.sig PUBLIC.pem")
    receipt=execute_signed_job(Path(argv[1]),Path(argv[2]),Path(argv[3]))
    print(json.dumps(receipt,ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main(sys.argv))
