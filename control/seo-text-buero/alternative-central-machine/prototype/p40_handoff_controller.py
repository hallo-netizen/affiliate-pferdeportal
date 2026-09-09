#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
P22=HERE/"p22_signed_normal_draft_integration.py"

CONTRACT="PFERDE_ATELIER_FACHWORKFLOW_HANDOFF_REQUEST_V1"
REQUIRED=(
    "contract","room_token","batch_sha256","canonical_article_id","plan_slot",
    "allowed_output_root","item_receipt_ref","fachworkflow_pass_ref",
    "contract_binding_ref","contract_binding_sha256","stage_proofs","fact_pack",
    "production_plan_item","production_plan_header","workflow_release_item",
    "workflow_release_metadata",
)

class HandoffBlocked(RuntimeError):
    pass

def _parse_status(output:str,status:str)->dict:
    decoder=json.JSONDecoder()
    for i,ch in enumerate(output):
        if ch!="{":
            continue
        try:
            obj,_=decoder.raw_decode(output[i:])
        except Exception:
            continue
        if isinstance(obj,dict) and obj.get("status")==status:
            return obj
    raise HandoffBlocked("BOUND_ITEM_PASS_MISSING")

def _load_exact_handoff(path:Path)->dict:
    if not path.is_file():
        raise HandoffBlocked("HANDOFF_REQUEST_MISSING")
    value=json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value,dict) or set(value)!=set(REQUIRED):
        raise HandoffBlocked("HANDOFF_REQUEST_FIELDS_INVALID")
    if value.get("contract")!=CONTRACT:
        raise HandoffBlocked("HANDOFF_REQUEST_CONTRACT_INVALID")

    batch=str(value.get("batch_sha256",""))
    slot=str(value.get("plan_slot",""))
    if not re.fullmatch(r"[0-9a-f]{64}",batch):
        raise HandoffBlocked("HANDOFF_BATCH_SHA_INVALID")
    if not re.fullmatch(r"[0-9a-f]{64}",slot):
        raise HandoffBlocked("HANDOFF_PLAN_SLOT_INVALID")

    cid=value.get("canonical_article_id")
    if not isinstance(cid,str) or not cid:
        raise HandoffBlocked("HANDOFF_CANONICAL_ID_INVALID")

    item=value.get("production_plan_item")
    release=value.get("workflow_release_item")
    header=value.get("production_plan_header")
    if not isinstance(item,dict) or not isinstance(release,dict) or not isinstance(header,dict):
        raise HandoffBlocked("HANDOFF_PRODUCTION_CONTEXT_INVALID")
    if item.get("canonical_article_id")!=cid or item.get("plan_slot")!=slot:
        raise HandoffBlocked("HANDOFF_PLAN_ITEM_IDENTITY_MISMATCH")
    if release.get("canonical_article_id")!=cid or release.get("plan_slot")!=slot:
        raise HandoffBlocked("HANDOFF_RELEASE_ITEM_IDENTITY_MISMATCH")
    if header.get("contract")!="production_plan_v4" or "items" in header:
        raise HandoffBlocked("HANDOFF_PLAN_HEADER_INVALID")

    if not isinstance(value.get("fact_pack"),dict) or not value["fact_pack"]:
        raise HandoffBlocked("HANDOFF_FACT_PACK_MISSING")
    if not isinstance(value.get("workflow_release_metadata"),dict) or not value["workflow_release_metadata"]:
        raise HandoffBlocked("HANDOFF_RELEASE_METADATA_MISSING")
    if not isinstance(value.get("stage_proofs"),list) or len(value["stage_proofs"])!=12:
        raise HandoffBlocked("HANDOFF_STAGE_PROOFS_INVALID")

    return value

def execute_handoff(path:Path)->dict:
    request=_load_exact_handoff(path)

    # KISS: the existing canonical_article_id is the one bound item identity.
    # The fixed P22 adapter independently verifies it against PPM prepare() before signing/write.
    proc=subprocess.run(
        [
            sys.executable,str(P22),
            "--job-id",request["batch_sha256"],
            "--expected-item-id",request["canonical_article_id"],
        ],
        cwd=HERE.parents[3],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=300,
    )
    if proc.returncode!=0:
        # If identity is wrong, P22 blocks after no-write prepare and before signing/write.
        try:
            blocked=_parse_status(proc.stdout,"P22_BOUND_ITEM_ID_BLOCKED")
        except HandoffBlocked:
            blocked=None
        if isinstance(blocked,dict):
            raise HandoffBlocked("HANDOFF_ITEM_NOT_BOUND_TO_PPM_PREPARE")
        raise HandoffBlocked("FIXED_ITEM_ADAPTER_FAILED")

    proof=_parse_status(proc.stdout,"P22_SIGNED_NORMAL_DRAFT_BOUNDARY_PASS")
    if proof.get("job_id")!=request["batch_sha256"]:
        raise HandoffBlocked("HANDOFF_BATCH_IDENTITY_DRIFT")
    if proof.get("item_id")!=request["canonical_article_id"]:
        raise HandoffBlocked("HANDOFF_ITEM_IDENTITY_DRIFT")

    required_true=(
        "prepare_no_write","external_signature_verified",
        "exact_one_draft_written","publish_count_unchanged",
        "post_signature_tamper_blocked","post_signature_rehash_tamper_blocked",
    )
    if any(proof.get(k) is not True for k in required_true):
        raise HandoffBlocked("BOUND_ITEM_INVARIANT_FAILED")

    return {
        "contract":"ALT_HANDOFF_CONTROLLER_RECEIPT_V1",
        "status":"HANDOFF_ITEM_PASS_NO_PUBLISH",
        "batch_sha256":request["batch_sha256"],
        "canonical_article_id":request["canonical_article_id"],
        "plan_slot":request["plan_slot"],
        "input_truth":"FACHWORKFLOW_HANDOFF_REQUEST.json",
        "new_job_manifest_used":False,
        "new_handoff_format_used":False,
        "route_runtime_selectable":False,
        "publish_allowed":False,
        "prepared_fingerprint":proof["planned_write_fingerprint"],
        "release_content_sha256":proof["release_content_sha256"],
    }

def main(argv:list[str])->int:
    if len(argv)!=1:
        raise SystemExit("usage: p40_handoff_controller.py FACHWORKFLOW_HANDOFF_REQUEST.json")
    try:
        receipt=execute_handoff(Path(argv[0]))
        print(json.dumps(receipt,ensure_ascii=False,indent=2))
        return 0
    except (HandoffBlocked,OSError,ValueError,TypeError,json.JSONDecodeError) as exc:
        print(json.dumps({
            "status":"P40_HANDOFF_CONTROLLER_BLOCKED",
            "error":str(exc),
            "publish_allowed":False,
        },ensure_ascii=False,indent=2))
        return 2

if __name__=="__main__":
    raise SystemExit(main(sys.argv[1:]))
