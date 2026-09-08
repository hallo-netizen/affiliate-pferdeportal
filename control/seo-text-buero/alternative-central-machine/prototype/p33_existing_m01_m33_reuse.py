#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

REPO=Path(__file__).resolve().parents[4]
RUNNER="control/startmaster0107/HOBBYRAUM_M01_M33_REGRESSION.py"

def run_raw(cmd,cwd,timeout=300):
    return subprocess.run(cmd,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=timeout)

def run(cmd,cwd,timeout=300):
    p=run_raw(cmd,cwd,timeout)
    if p.returncode!=0:
        raise RuntimeError("COMMAND_FAILED:"+" ".join(cmd)+"\n"+p.stdout[-5000:])
    return p.stdout

def main():
    # Audit current production infrastructure read-only. Never repair it here.
    run(["git","fetch","--depth=1","origin","main"],REPO)
    main_sha=run(["git","rev-parse","FETCH_HEAD"],REPO).strip()
    candidate_sha=run(["git","rev-parse","HEAD"],REPO).strip()

    with tempfile.TemporaryDirectory() as td:
        work=Path(td)/"main"
        run(["git","worktree","add","--detach",str(work),main_sha],REPO)
        try:
            results=[]
            for n in range(1,34):
                mid=f"M{n:02d}"
                p=run_raw(["python3",RUNNER,"--case",mid],work,timeout=300)
                results.append({
                    "id":mid,
                    "status":"PASS" if p.returncode==0 else "FAIL",
                    "returncode":p.returncode,
                    "output_tail":p.stdout[-1800:]
                })

            if len(results)!=33:
                raise RuntimeError("MATRIX_AUDIT_INCOMPLETE")

            failed=[r["id"] for r in results if r["status"]!="PASS"]
            print(json.dumps({
                "status":"P33_EXISTING_M01_M33_AUDIT_COMPLETE",
                "tested_main_sha":main_sha,
                "candidate_sha_unchanged":candidate_sha,
                "existing_runner_reused":RUNNER,
                "new_regression_runner_created":False,
                "cases_audited":33,
                "pass_count":33-len(failed),
                "fail_count":len(failed),
                "failed_cases":failed,
                "results":results,
                "meaning":"CURRENT_MAIN_STATUS_ONLY_NOT_ALTERNATIVE_ARCHITECTURE_VERDICT",
                "publish_allowed":False
            },ensure_ascii=False,indent=2))
        finally:
            subprocess.run(["git","worktree","remove","--force",str(work)],cwd=REPO,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    return 0

if __name__=="__main__":
    raise SystemExit(main())
