#!/usr/bin/env python3
from __future__ import annotations

import ast
import json
import re
import subprocess
import tempfile
from pathlib import Path

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[3]
P22=HERE/"p22_signed_normal_draft_integration.py"

ACTION_REL="control/single-door-boundary/codex_current_action.py"
HANDOFF_REL="control/startmaster0107/fachworkflow_proof_handoff.py"

EXPECTED=(
    "contract","room_token","batch_sha256","canonical_article_id","plan_slot",
    "allowed_output_root","item_receipt_ref","fachworkflow_pass_ref",
    "contract_binding_ref","contract_binding_sha256","stage_proofs","fact_pack",
    "production_plan_item","production_plan_header","workflow_release_item",
    "workflow_release_metadata",
)

class Blocked(RuntimeError):
    pass

def run(cmd,cwd,timeout=600):
    p=subprocess.run(cmd,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=timeout)
    if p.returncode!=0:
        raise Blocked("COMMAND_FAILED:"+" ".join(cmd)+"\n"+p.stdout[-5000:])
    return p.stdout

def const_from_text(text:str,name:str):
    tree=ast.parse(text)
    for node in tree.body:
        if isinstance(node,(ast.Assign,ast.AnnAssign)):
            targets=node.targets if isinstance(node,ast.Assign) else [node.target]
            for t in targets:
                if isinstance(t,ast.Name) and t.id==name:
                    return ast.literal_eval(node.value)
    raise Blocked("CONST_MISSING:"+name)

def parse_status(output:str,status:str):
    dec=json.JSONDecoder()
    for i,ch in enumerate(output):
        if ch!="{":
            continue
        try:
            obj,_=dec.raw_decode(output[i:])
        except Exception:
            continue
        if isinstance(obj,dict) and obj.get("status")==status:
            return obj
    raise Blocked("STATUS_MISSING:"+status)

def main():
    # Current production infrastructure is inspected read-only.
    run(["git","fetch","--depth=1","origin","main"],REPO)
    main_sha=run(["git","rev-parse","FETCH_HEAD"],REPO).strip()
    candidate_sha=run(["git","rev-parse","HEAD"],REPO).strip()

    with tempfile.TemporaryDirectory() as td:
        work=Path(td)/"main"
        run(["git","worktree","add","--detach",str(work),main_sha],REPO)
        try:
            action=(work/ACTION_REL).read_text(encoding="utf-8")
            handoff=(work/HANDOFF_REL).read_text(encoding="utf-8")
            fields=tuple(const_from_text(action,"HANDOFF_REQUEST_REQUIRED_FIELDS"))
            if fields!=EXPECTED:
                raise Blocked("HANDOFF_FIELD_CONTRACT_DRIFT")

            # Prove current materialize is NOT the pre-signature entry:
            # it calls the real bridge / full Normal-Draft pipeline, whose tested path reaches draft creation.
            required_current_tokens=(
                "PSERC_PPM_Intake_Bridge::execute",
                "PPM679_Normal_Draft_Pipeline::execute_plan",
                "_real_ppm_stage(repo, request",
                "NORMAL_DRAFT_END_TO_END_READBACK_PASS_AWAITING_USER_CONTENT_REVIEW_NO_PUBLISH",
            )
            for token in required_current_tokens:
                if token not in handoff:
                    raise Blocked("CURRENT_MATERIALIZE_BINDING_MISSING:"+token)

            current_materialize_reaches_full_pipeline=True

            # The same request already contains all identity/context needed BEFORE PPM execution.
            required_prepare_inputs=(
                "canonical_article_id","plan_slot","fact_pack",
                "production_plan_item","production_plan_header",
                "workflow_release_item","workflow_release_metadata",
            )
            if not all(x in EXPECTED for x in required_prepare_inputs):
                raise Blocked("HANDOFF_PREPARE_CONTEXT_INCOMPLETE")

            # Reuse the already-proven real prepare->external-signature->write boundary.
            if not P22.is_file():
                raise Blocked("P22_BOUNDARY_PROOF_MISSING")
            out=run(["python3",str(P22)],REPO,timeout=300)
            proof=parse_status(out,"P22_SIGNED_NORMAL_DRAFT_BOUNDARY_PASS")
            required_true=(
                "prepare_no_write","prepared_fingerprint_bound",
                "external_signature_verified","exact_one_draft_written",
                "publish_count_unchanged","post_signature_tamper_blocked",
                "post_signature_rehash_tamper_blocked",
            )
            if any(proof.get(k) is not True for k in required_true):
                raise Blocked("P22_BOUNDARY_INVARIANT_FAILED")

            # KISS target: no new file/format/controller.
            print(json.dumps({
                "status":"P39_EXISTING_HANDOFF_TO_PREPARE_BOUNDARY_PASS",
                "tested_main_sha":main_sha,
                "candidate_sha_unchanged":candidate_sha,
                "existing_request_filename":"FACHWORKFLOW_HANDOFF_REQUEST.json",
                "existing_request_contract":"PFERDE_ATELIER_FACHWORKFLOW_HANDOFF_REQUEST_V1",
                "required_field_count":len(EXPECTED),
                "same_existing_handoff_reused":True,
                "new_handoff_file_required":False,
                "new_handoff_format_required":False,
                "new_job_manifest_required":False,
                "current_materialize_reaches_full_pipeline":current_materialize_reaches_full_pipeline,
                "current_materialize_safe_as_pre_signature_entry":False,
                "handoff_contains_all_prepare_identity_context":True,
                "target_processing_change":"SAME_HANDOFF -> EXISTING_PPM_PREPARE -> EXTERNAL_SIGNATURE -> EXISTING_CREATE_DRAFT",
                "prepare_no_write_proven":True,
                "external_signature_boundary_proven":True,
                "post_signature_tamper_blocked":True,
                "publish_allowed":False,
            },ensure_ascii=False,indent=2))
        finally:
            subprocess.run(["git","worktree","remove","--force",str(work)],cwd=REPO,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    return 0

if __name__=="__main__":
    raise SystemExit(main())
