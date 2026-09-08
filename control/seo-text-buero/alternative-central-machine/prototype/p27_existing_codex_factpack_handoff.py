#!/usr/bin/env python3
from __future__ import annotations

import ast
import json
import subprocess
import tempfile
from pathlib import Path

REPO=Path(__file__).resolve().parents[4]
STEP_REL="control/startmaster0107/STEP_107007_RUN_NEW_ARTICLE_BATCH_NO_STOP.json"
ACTION_REL="control/single-door-boundary/codex_current_action.py"
HANDOFF_REL="control/startmaster0107/fachworkflow_proof_handoff.py"

REQUIRED=(
 "contract","room_token","batch_sha256","canonical_article_id","plan_slot",
 "allowed_output_root","item_receipt_ref","fachworkflow_pass_ref",
 "contract_binding_ref","contract_binding_sha256","stage_proofs","fact_pack",
 "production_plan_item","production_plan_header","workflow_release_item",
 "workflow_release_metadata"
)

def const_from_text(text:str,name:str):
    tree=ast.parse(text)
    for node in tree.body:
        if isinstance(node,(ast.Assign,ast.AnnAssign)):
            targets=node.targets if isinstance(node,ast.Assign) else [node.target]
            for t in targets:
                if isinstance(t,ast.Name) and t.id==name:
                    return ast.literal_eval(node.value)
    raise RuntimeError("CONST_MISSING:"+name)

def run(cmd,cwd):
    p=subprocess.run(cmd,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=240)
    if p.returncode!=0:
        raise RuntimeError("COMMAND_FAILED:"+" ".join(cmd)+"\n"+p.stdout[-4000:])
    return p.stdout

def main():
    # Candidate remains isolated. Read current production infrastructure only through a temporary fetched worktree.
    run(["git","fetch","--depth=1","origin","main"],REPO)
    main_sha=run(["git","rev-parse","FETCH_HEAD"],REPO).strip()

    with tempfile.TemporaryDirectory() as td:
        work=Path(td)/"main"
        run(["git","worktree","add","--detach",str(work),main_sha],REPO)
        try:
            step=json.loads((work/STEP_REL).read_text(encoding="utf-8"))
            instr=step["instruction"]
            required_phrases=[
              "der aktuelle Codex-Prozess IST der gebundene Fachworkflow-Worker",
              "Recherche/fact_pack",
              "fachworkflow_handoff.request_required_fields ist die exakte und vollständige Feldliste",
              "FACHWORKFLOW_HANDOFF_REQUEST.json exakt unter fachworkflow_handoff.request_ref erzeugen",
              "danach ausschließlich fachworkflow_handoff.command ausführen",
              "kein separater Fachworkflow-Executor",
            ]
            for phrase in required_phrases:
                if phrase not in instr:
                    raise RuntimeError("CURRENT_MAIN_107007_BINDING_MISSING:"+phrase)

            action_text=(work/ACTION_REL).read_text(encoding="utf-8")
            action_fields=tuple(const_from_text(action_text,"HANDOFF_REQUEST_REQUIRED_FIELDS"))
            if action_fields!=REQUIRED:
                raise RuntimeError("CURRENT_MAIN_HANDOFF_FIELDS_DRIFT")
            if "CURRENT_CODEX_IS_BOUND_FACHWORKFLOW_WORKER" not in action_text:
                raise RuntimeError("CURRENT_MAIN_WORKER_ROLE_NOT_BOUND")
            if "separate_fachworkflow_executor_required" not in action_text:
                raise RuntimeError("CURRENT_MAIN_SEPARATE_EXECUTOR_DENIAL_MISSING")
            if "fachworkflow_handoff" not in action_text:
                raise RuntimeError("CURRENT_MAIN_FACHWORKFLOW_HANDOFF_MISSING")

            # Run the existing tests on current main, locally inside the temporary worktree.
            action_out=run(["python3",ACTION_REL,"selftest"],work)
            handoff_out=run(["python3","-m","unittest","control.startmaster0107.test_fachworkflow_proof_handoff"],work)

            current_candidate=run(["git","rev-parse","HEAD"],REPO).strip()

            print(json.dumps({
              "status":"P27_EXISTING_CODEX_FACTPACK_HANDOFF_PASS",
              "tested_authority_ref":"main",
              "tested_main_sha":main_sha,
              "candidate_sha_unchanged":current_candidate,
              "fact_pack_producer":"CURRENT_BOUND_CODEX_FACHWORKFLOW_WORKER",
              "codex_start_reused":True,
              "new_codex_entry_required":False,
              "existing_file_handoff_reused":True,
              "new_file_handoff_required":False,
              "request_required_fields":list(REQUIRED),
              "request_field_count":len(REQUIRED),
              "field_set_runtime_selectable":False,
              "existing_current_action_selftest_tail":action_out[-1200:],
              "existing_handoff_unittest_tail":handoff_out[-1200:],
              "publish_allowed":False
            },ensure_ascii=False,indent=2))
        finally:
            subprocess.run(["git","worktree","remove","--force",str(work)],cwd=REPO,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    return 0

if __name__=="__main__":
    raise SystemExit(main())
