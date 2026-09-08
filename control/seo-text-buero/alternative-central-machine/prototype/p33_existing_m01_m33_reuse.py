#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

REPO=Path(__file__).resolve().parents[4]
RUNNER="control/startmaster0107/HOBBYRAUM_M01_M33_REGRESSION.py"

def run(cmd,cwd,timeout=600):
    p=subprocess.run(cmd,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=timeout)
    if p.returncode!=0:
        raise RuntimeError("COMMAND_FAILED:"+" ".join(cmd)+"\n"+p.stdout[-6000:])
    return p.stdout

def main():
    # Current production authority is read only; candidate remains isolated.
    run(["git","fetch","--depth=1","origin","main"],REPO)
    main_sha=run(["git","rev-parse","FETCH_HEAD"],REPO).strip()
    candidate_sha=run(["git","rev-parse","HEAD"],REPO).strip()

    with tempfile.TemporaryDirectory() as td:
        work=Path(td)/"main"
        run(["git","worktree","add","--detach",str(work),main_sha],REPO)
        try:
            out=run(["python3",RUNNER],work,timeout=900)
            if '"status": "GESAMT PASS"' not in out and '"status":"GESAMT PASS"' not in out:
                raise RuntimeError("M01_M33_GESAMT_PASS_MISSING")
            for n in range(1,34):
                token=f"M{n:02d} PASS"
                if token not in out:
                    raise RuntimeError("MATRIX_CASE_PASS_MISSING:"+token)
            if "LAST_REGRESSION PASS" not in out:
                raise RuntimeError("LAST_REGRESSION_RECHECK_MISSING")

            print(json.dumps({
                "status":"P33_EXISTING_M01_M33_REUSE_PASS",
                "tested_main_sha":main_sha,
                "candidate_sha_unchanged":candidate_sha,
                "existing_runner_reused":RUNNER,
                "new_regression_runner_created":False,
                "m01_m33_all_pass":True,
                "last_regression_recheck_pass":True,
                "publish_allowed":False,
                "output_tail":out[-3500:]
            },ensure_ascii=False,indent=2))
        finally:
            subprocess.run(["git","worktree","remove","--force",str(work)],cwd=REPO,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    return 0

if __name__=="__main__":
    raise SystemExit(main())
