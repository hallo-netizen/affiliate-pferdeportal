#!/usr/bin/env python3
from __future__ import annotations

import ast
import json
import subprocess
import tempfile
from pathlib import Path

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[3]

ACTION_REL="control/single-door-boundary/codex_current_action.py"
HANDOFF_REL="control/startmaster0107/fachworkflow_proof_handoff.py"
EXPECTED=(
    "contract","room_token","batch_sha256","canonical_article_id","plan_slot",
    "allowed_output_root","item_receipt_ref","fachworkflow_pass_ref",
    "contract_binding_ref","contract_binding_sha256","stage_proofs","fact_pack",
    "production_plan_item","production_plan_header","workflow_release_item",
    "workflow_release_metadata",
)

def run(cmd,cwd,timeout=300):
    p=subprocess.run(cmd,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=timeout)
    if p.returncode!=0:
        raise RuntimeError("COMMAND_FAILED:"+" ".join(cmd)+"\n"+p.stdout[-4000:])
    return p.stdout

def module_constant(text:str,name:str):
    tree=ast.parse(text)
    for node in tree.body:
        if isinstance(node,(ast.Assign,ast.AnnAssign)):
            targets=node.targets if isinstance(node,ast.Assign) else [node.target]
            for t in targets:
                if isinstance(t,ast.Name) and t.id==name:
                    return ast.literal_eval(node.value)
    raise RuntimeError("MODULE_CONSTANT_MISSING:"+name)

def local_required_set(text:str):
    tree=ast.parse(text)
    for node in ast.walk(tree):
        if isinstance(node,ast.FunctionDef) and node.name=="materialize":
            for child in ast.walk(node):
                if isinstance(child,ast.Assign):
                    for t in child.targets:
                        if isinstance(t,ast.Name) and t.id=="required":
                            value=ast.literal_eval(child.value)
                            if isinstance(value,set):
                                return value
    raise RuntimeError("HANDOFF_REQUIRED_SET_MISSING")

def main():
    # Read current main only; never merge or modify it.
    run(["git","fetch","--depth=1","origin","main"],REPO)
    main_sha=run(["git","rev-parse","FETCH_HEAD"],REPO).strip()
    candidate_sha=run(["git","rev-parse","HEAD"],REPO).strip()

    with tempfile.TemporaryDirectory() as td:
        work=Path(td)/"main"
        run(["git","worktree","add","--detach",str(work),main_sha],REPO)
        try:
            action=(work/ACTION_REL).read_text(encoding="utf-8")
            handoff=(work/HANDOFF_REL).read_text(encoding="utf-8")

            action_fields=tuple(module_constant(action,"HANDOFF_REQUEST_REQUIRED_FIELDS"))
            handoff_fields=local_required_set(handoff)
            handoff_contract=module_constant(handoff,"CONTRACT")

            if action_fields!=EXPECTED:
                raise RuntimeError("CURRENT_ACTION_FIELD_CONTRACT_DRIFT")
            if handoff_fields!=set(EXPECTED):
                raise RuntimeError("HANDOFF_MATERIALIZE_FIELD_CONTRACT_DRIFT")
            if handoff_contract!="PFERDE_ATELIER_FACHWORKFLOW_HANDOFF_REQUEST_V1":
                raise RuntimeError("HANDOFF_CONTRACT_DRIFT")

            required_source_checks=(
                "set(request) != required",
                "HANDOFF_REQUEST_FIELDS_OR_CONTRACT_INVALID",
                "HANDOFF_IDENTITY_HASH_INVALID",
                "HANDOFF_REQUEST_NOT_IN_BOUND_OUTPUT_ROOT",
                "HANDOFF_CONTRACT_BINDING_HASH_MISMATCH",
                "BOUND_FACHWORKFLOW_PRODUCTION_CONTEXT_MISSING",
                "BOUND_PRODUCTION_PLAN_ITEM_IDENTITY_MISMATCH",
                "BOUND_WORKFLOW_RELEASE_ITEM_IDENTITY_MISMATCH",
                "FACH_STAGE_SET_INVALID",
                "PPM679_REAL_BINDING_MISSING",
                "publish_allowed",
            )
            for token in required_source_checks:
                if token not in handoff:
                    raise RuntimeError("HANDOFF_REQUIRED_GUARD_MISSING:"+token)

            action_checks=(
                "request_ref=root+'FACHWORKFLOW_HANDOFF_REQUEST.json'",
                "'request_required_fields':HANDOFF_REQUEST_REQUIRED_FIELDS",
                "'command':'python3 '+HANDOFF_REL+' materialize '+request_ref",
                "'publish_allowed':False",
            )
            for token in action_checks:
                if token not in action:
                    raise RuntimeError("CURRENT_ACTION_HANDOFF_BINDING_MISSING:"+token)

            # The real handoff already carries the exact production identity/context.
            identity_fields=("batch_sha256","canonical_article_id","plan_slot")
            production_context=("fact_pack","production_plan_item","production_plan_header","workflow_release_item","workflow_release_metadata")
            if not all(x in EXPECTED for x in identity_fields+production_context):
                raise RuntimeError("REAL_HANDOFF_CONTEXT_INCOMPLETE")

            print(json.dumps({
                "status":"P38_EXISTING_HANDOFF_CONTRACT_REUSE_PASS",
                "tested_main_sha":main_sha,
                "candidate_sha_unchanged":candidate_sha,
                "request_contract":handoff_contract,
                "required_field_count":len(EXPECTED),
                "required_fields":list(EXPECTED),
                "real_identity_fields":list(identity_fields),
                "production_context_fields":list(production_context),
                "exact_single_runtime_request_filename":"FACHWORKFLOW_HANDOFF_REQUEST.json",
                "existing_materialize_command_reused":True,
                "new_handoff_file_required":False,
                "new_handoff_format_required":False,
                "new_job_manifest_required_for_target_architecture":False,
                "prototype_signed_job_manifest_role":"LAB_TEST_ONLY",
                "publish_allowed":False,
            },ensure_ascii=False,indent=2))
        finally:
            subprocess.run(["git","worktree","remove","--force",str(work)],cwd=REPO,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    return 0

if __name__=="__main__":
    raise SystemExit(main())
