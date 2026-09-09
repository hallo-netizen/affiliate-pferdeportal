#!/usr/bin/env python3
from __future__ import annotations
import json,subprocess,tempfile
from pathlib import Path

REPO=Path(__file__).resolve().parents[4]
MATRIX="control/startmaster0107/HOBBYRAUM_M01_M33_REGRESSION.py"

# Only the historical failures that directly touch the ACM integration seam.
CASES=[
 "M02", # unique article files
 "M05", # durable release/receipt
 "M06", # no fake production contract
 "M07", # recovery not automatically final
 "M13", # final content hash parity
 "M16", # signer outside worker
 "M17", # finalization fail-closed
 "M20", # delivery exact hash binding
 "M21", # no auto-publish
 "M25", # Fachworkflow remains authoritative
 "M26", # real fact_pack/production_plan context
 "M27", # current-main production identity
 "M28", # materially executable handoff
 "M29", # release metadata batch identity
 "M30", # final context batch identity
 "M31", # no synthetic executor
 "M32", # bound runtime package paths
 "M33", # ENDSTEMPEL independent from Codex git auth
 "M34", # plan_slot -> PPM canonical identity parity
 "M35", # research hash != PPM registry hash
 "M36", # provenance legacy compatibility
]

def run(cmd,cwd,timeout=300):
    return subprocess.run(cmd,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=timeout)

def main():
    fetch=run(["git","fetch","--depth=1","origin","main"],REPO)
    if fetch.returncode!=0:
        raise RuntimeError("MAIN_FETCH_FAILED:"+fetch.stdout[-2000:])
    main_sha=run(["git","rev-parse","FETCH_HEAD"],REPO).stdout.strip()
    candidate_sha=run(["git","rev-parse","HEAD"],REPO).stdout.strip()
    results=[]
    with tempfile.TemporaryDirectory() as td:
        work=Path(td)/"main"
        cp=run(["git","worktree","add","--detach",str(work),main_sha],REPO)
        if cp.returncode!=0: raise RuntimeError("WORKTREE_FAILED:"+cp.stdout[-2000:])
        try:
            matrix=work/MATRIX
            if not matrix.is_file(): raise RuntimeError("NEIGHBOR_MATRIX_MISSING")
            for case in CASES:
                cp=run(["python3",MATRIX,"--case",case],work,timeout=420)
                ok=cp.returncode==0 and ("HISTORY_MACHINE_PROOF_PASS:"+case) in cp.stdout
                results.append({"id":case,"status":"PASS" if ok else "FAIL","output_tail":cp.stdout[-1400:]})
                if not ok:
                    print(json.dumps({
                      "status":"ACM_NEIGHBOR_ERRORCHAIN_REUSE_BLOCKED",
                      "tested_main_sha":main_sha,
                      "candidate_sha_unchanged":candidate_sha,
                      "first_fail":case,
                      "results":results,
                      "new_duplicate_regression_runner_created":False,
                      "reused_existing_neighbor_runner":True,
                      "publish_allowed":False
                    },ensure_ascii=False,indent=2))
                    return 2
        finally:
            subprocess.run(["git","worktree","remove","--force",str(work)],cwd=REPO,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    print(json.dumps({
      "status":"ACM_NEIGHBOR_ERRORCHAIN_REUSE_PASS",
      "tested_main_sha":main_sha,
      "candidate_sha_unchanged":candidate_sha,
      "reused_existing_neighbor_runner":True,
      "new_duplicate_regression_runner_created":False,
      "selected_historical_seam_cases":CASES,
      "results":results,
      "all_selected_neighbor_regressions_pass":True,
      "publish_allowed":False
    },ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
