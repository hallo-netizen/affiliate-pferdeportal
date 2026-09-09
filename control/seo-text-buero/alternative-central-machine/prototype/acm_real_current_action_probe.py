#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

REPO=Path(__file__).resolve().parents[4]

def run(cmd:list[str],cwd:Path,timeout:int=300)->subprocess.CompletedProcess:
    return subprocess.run(cmd,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=timeout)

def parse_last_json(text:str)->dict:
    dec=json.JSONDecoder()
    found=[]
    for i,ch in enumerate(text):
        if ch!="{":
            continue
        try:
            obj,_=dec.raw_decode(text[i:])
        except Exception:
            continue
        if isinstance(obj,dict):
            found.append(obj)
    if not found:
        raise RuntimeError("CURRENT_ACTION_JSON_MISSING")
    return found[-1]

def main()->int:
    cp=run(["git","fetch","--depth=1","origin","main"],REPO)
    if cp.returncode!=0:
        raise RuntimeError("MAIN_FETCH_FAILED:"+cp.stdout[-2000:])
    sha=run(["git","rev-parse","FETCH_HEAD"],REPO).stdout.strip()
    candidate=run(["git","rev-parse","HEAD"],REPO).stdout.strip()

    with tempfile.TemporaryDirectory() as td:
        work=Path(td)/"main"
        cp=run(["git","worktree","add","--detach",str(work),sha],REPO)
        if cp.returncode!=0:
            raise RuntimeError("WORKTREE_FAILED:"+cp.stdout[-2000:])
        try:
            # Exact existing production entrance sequence:
            # 1) current-main Codex environment preflight,
            # 2) official runtime entry materializes the bound capsule,
            # 3) ask only for the current bound action.
            pre=run(["python3","control/startmaster0107/codex-production-runtime/codex_environment_preflight.py"],work)
            pre_data=parse_last_json(pre.stdout)
            if pre.returncode!=0 or pre_data.get("status")!="CODEX_PRODUCTION_PREFLIGHT_PASS":
                raise RuntimeError("REAL_CODEX_PREFLIGHT_NOT_PASS:"+str(pre_data))
            start=run(["python3","control/output-quarantine/runtime_entry_gate.py","start"],work)
            start_data=parse_last_json(start.stdout)
            if start.returncode!=0 or start_data.get("status")!="OFFICIAL_RUNTIME_ENTRY_PASS":
                raise RuntimeError("REAL_OFFICIAL_RUNTIME_ENTRY_NOT_PASS:"+str(start_data))
            cur=run(["python3","control/single-door-boundary/codex_current_action.py","current"],work)
            data=parse_last_json(cur.stdout)
            status=str(data.get("status") or "")
            if status=="CURRENT_BOUND_ACTION_READY":
                handoff=data.get("fachworkflow_handoff")
                item=data.get("current_item")
                if not isinstance(handoff,dict) or not isinstance(item,dict):
                    raise RuntimeError("REAL_CURRENT_BINDING_INCOMPLETE")
                req=str(handoff.get("request_ref") or "")
                if not req.endswith("FACHWORKFLOW_HANDOFF_REQUEST.json"):
                    raise RuntimeError("REAL_HANDOFF_REQUEST_REF_INVALID")
                required=handoff.get("request_required_fields")
                if not isinstance(required,list) or len(required)!=16:
                    raise RuntimeError("REAL_HANDOFF_FIELD_SET_INVALID")
                out={
                    "status":"ACM_REAL_CURRENT_ACTION_READY_PASS",
                    "tested_main_sha":sha,
                    "candidate_sha_unchanged":candidate,
                    "current_item":item,
                    "allowed_output_root":data.get("allowed_output_root"),
                    "handoff_request_ref":req,
                    "handoff_required_fields":required,
                    "worker_role":data.get("worker_role"),
                    "publish_allowed":False,
                }
            elif status in {"BLOCKED","USER_ACTION_REQUIRED","FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH"}:
                out={
                    "status":"ACM_REAL_CURRENT_ACTION_BOUND_HALT",
                    "tested_main_sha":sha,
                    "candidate_sha_unchanged":candidate,
                    "real_runtime_status":status,
                    "error":data.get("error"),
                    "evidence":data.get("evidence"),
                    "publish_allowed":False,
                }
            else:
                raise RuntimeError("REAL_CURRENT_ACTION_UNEXPECTED:"+status)
            print(json.dumps(out,ensure_ascii=False,indent=2))
            return 0
        finally:
            subprocess.run(["git","worktree","remove","--force",str(work)],cwd=REPO,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

if __name__=="__main__":
    raise SystemExit(main())
