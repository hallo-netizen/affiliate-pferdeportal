#!/usr/bin/env python3
from __future__ import annotations

import ast
import json
import subprocess
from pathlib import Path

REPO=Path(__file__).resolve().parents[4]
STEP=REPO/"control/startmaster0107/STEP_107007_RUN_NEW_ARTICLE_BATCH_NO_STOP.json"
ACTION=REPO/"control/single-door-boundary/codex_current_action.py"
HANDOFF=REPO/"control/startmaster0107/fachworkflow_proof_handoff.py"

REQUIRED=(
 "contract","room_token","batch_sha256","canonical_article_id","plan_slot",
 "allowed_output_root","item_receipt_ref","fachworkflow_pass_ref",
 "contract_binding_ref","contract_binding_sha256","stage_proofs","fact_pack",
 "production_plan_item","production_plan_header","workflow_release_item",
 "workflow_release_metadata"
)

def const_from_py(path:Path,name:str):
    tree=ast.parse(path.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node,(ast.Assign,ast.AnnAssign)):
            targets=node.targets if isinstance(node,ast.Assign) else [node.target]
            for t in targets:
                if isinstance(t,ast.Name) and t.id==name:
                    return ast.literal_eval(node.value)
    raise RuntimeError("CONST_MISSING:"+name)

def main():
    step=json.loads(STEP.read_text(encoding="utf-8"))
    instr=step["instruction"]

    must=[
      "als gebundener Worker die realen aktuellen Fachworkflow-Ausgaben selbst erzeugen: Recherche/fact_pack",
      "FACHWORKFLOW_HANDOFF_REQUEST.json exakt unter fachworkflow_handoff.request_ref erzeugen",
      "fachworkflow_handoff.request_required_fields ist die exakte und vollständige Feldliste",
      "danach ausschließlich fachworkflow_handoff.command ausführen",
      "kein separater Fachworkflow-Executor",
    ]
    for phrase in must:
        if phrase not in instr:
            raise RuntimeError("AUTHORITATIVE_107007_BINDING_MISSING:"+phrase)

    action_fields=tuple(const_from_py(ACTION,"HANDOFF_REQUEST_REQUIRED_FIELDS"))
    handoff_contract=const_from_py(HANDOFF,"CONTRACT")
    if action_fields!=REQUIRED:
        raise RuntimeError("CURRENT_ACTION_HANDOFF_FIELDS_DRIFT")

    # Existing selftests only; no new handoff implementation.
    tests=[
      ["python3",str(ACTION),"selftest"],
      ["python3","-m","unittest","control.startmaster0107.test_fachworkflow_proof_handoff"],
    ]
    results=[]
    for cmd in tests:
        p=subprocess.run(cmd,cwd=REPO,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=180)
        results.append({"cmd":" ".join(cmd),"returncode":p.returncode,"output_tail":p.stdout[-3000:]})
        if p.returncode!=0:
            raise RuntimeError("EXISTING_HANDOFF_TEST_FAIL:"+p.stdout[-1200:])

    print(json.dumps({
      "status":"P27_EXISTING_CODEX_FACTPACK_HANDOFF_PASS",
      "fact_pack_producer":"CURRENT_BOUND_CODEX_FACHWORKFLOW_WORKER",
      "new_codex_entry_required":False,
      "new_file_handoff_required":False,
      "request_contract":handoff_contract,
      "required_field_count":len(REQUIRED),
      "required_fields":list(REQUIRED),
      "field_set_runtime_selectable":False,
      "existing_selftests":results,
      "publish_allowed":False
    },ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
