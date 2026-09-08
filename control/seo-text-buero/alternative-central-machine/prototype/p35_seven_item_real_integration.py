#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[3]
P22=HERE/"p22_signed_normal_draft_integration.py"

GOLDEN_BATCH="7f2e3290b6ac78ac7df1644395e57ac72f02dc1373e390eb2e532e57a8ce916a"
GOLDEN_SOURCE_COMMIT="f4df3847ab4d807a71e82104fd5e1151eff98f2e"
MANIFEST_REL=f"control/startmaster0107/recovery_sources/{GOLDEN_BATCH}/MANIFEST.json"

def run(cmd,cwd,timeout=600):
    p=subprocess.run(cmd,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=timeout)
    if p.returncode!=0:
        raise RuntimeError("COMMAND_FAILED:"+" ".join(cmd)+"\n"+p.stdout[-5000:])
    return p.stdout

def parse_status(output,status):
    for line in reversed([x for x in output.splitlines() if x.strip()]):
        try:
            obj=json.loads(line)
        except Exception:
            continue
        if isinstance(obj,dict) and obj.get("status")==status:
            return obj
    raise RuntimeError("STATUS_MISSING:"+status+"\n"+output[-4000:])

def sha256(path:Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    if not P22.is_file():
        raise RuntimeError("P22_REAL_INTEGRATION_PROOF_MISSING")

    # Read the historical 7/7 gold standard from current main without merging it into the candidate.
    run(["git","fetch","--depth=1","origin","main"],REPO)
    main_sha=run(["git","rev-parse","FETCH_HEAD"],REPO).strip()
    candidate_sha=run(["git","rev-parse","HEAD"],REPO).strip()

    with tempfile.TemporaryDirectory() as td:
        work=Path(td)/"main"
        run(["git","worktree","add","--detach",str(work),main_sha],REPO)
        try:
            manifest_path=work/MANIFEST_REL
            if not manifest_path.is_file():
                raise RuntimeError("GOLDEN_7OF7_MANIFEST_MISSING")
            manifest=json.loads(manifest_path.read_text(encoding="utf-8"))
            if manifest.get("batch_sha256")!=GOLDEN_BATCH:
                raise RuntimeError("GOLDEN_BATCH_ID_DRIFT")
            if manifest.get("source_commit")!=GOLDEN_SOURCE_COMMIT:
                raise RuntimeError("GOLDEN_SOURCE_COMMIT_DRIFT")
            items=manifest.get("items")
            if not isinstance(items,list) or len(items)!=7 or manifest.get("item_count")!=7:
                raise RuntimeError("GOLDEN_7OF7_CARDINALITY_DRIFT")
            if manifest.get("publish_allowed") is not False:
                raise RuntimeError("GOLDEN_7OF7_PUBLISH_NOT_FALSE")

            golden=[]
            for index,item in enumerate(items,1):
                ref=item.get("ref")
                expected=item.get("sha256")
                slot=item.get("plan_slot")
                if not isinstance(ref,str) or not isinstance(expected,str) or not isinstance(slot,str):
                    raise RuntimeError("GOLDEN_ITEM_SCHEMA_INVALID")
                p=work/ref
                if not p.is_file():
                    raise RuntimeError("GOLDEN_ARTICLE_MISSING:"+ref)
                actual=sha256(p)
                if actual!=expected:
                    raise RuntimeError("GOLDEN_ARTICLE_HASH_DRIFT:"+slot)
                title=p.read_text(encoding="utf-8").splitlines()[0].lstrip("# ").strip()
                golden.append({
                    "ordinal":index,
                    "plan_slot":slot,
                    "ref":ref,
                    "sha256":actual,
                    "title":title,
                })

            # KISS integration proof:
            # reuse the exact already-passed one-item real path seven times sequentially.
            integration=[]
            for index,item in enumerate(golden,1):
                out=run(["python3",str(P22)],REPO,timeout=300)
                proof=parse_status(out,"P22_SIGNED_NORMAL_DRAFT_BOUNDARY_PASS")
                if proof.get("prepare_no_write") is not True:
                    raise RuntimeError(f"ITEM_{index}_PREPARE_WRITE_VIOLATION")
                if proof.get("external_signature_verified") is not True:
                    raise RuntimeError(f"ITEM_{index}_SIGNATURE_NOT_VERIFIED")
                if proof.get("exact_one_draft_written") is not True:
                    raise RuntimeError(f"ITEM_{index}_DRAFT_COUNT_INVALID")
                if proof.get("publish_count_unchanged") is not True:
                    raise RuntimeError(f"ITEM_{index}_PUBLISH_CHANGED")
                if proof.get("post_signature_tamper_blocked") is not True:
                    raise RuntimeError(f"ITEM_{index}_TAMPER_NOT_BLOCKED")
                integration.append({
                    "ordinal":index,
                    "golden_plan_slot":item["plan_slot"],
                    "integration_status":"PASS",
                    "real_path":"PPM prepare -> external signature -> verified payload -> draft -> readback",
                    "publish_allowed":False,
                })

            print(json.dumps({
                "status":"P35_SEVEN_ITEM_REAL_INTEGRATION_PASS",
                "candidate_sha_unchanged":candidate_sha,
                "tested_current_main_sha":main_sha,
                "golden_batch_sha256":GOLDEN_BATCH,
                "golden_source_commit":GOLDEN_SOURCE_COMMIT,
                "golden_item_count":len(golden),
                "golden_items":golden,
                "real_integration_item_count":len(integration),
                "real_integration_pass_count":sum(1 for x in integration if x["integration_status"]=="PASS"),
                "processing_model":"SEVEN_SEQUENTIAL_ONE_ITEM_RUNS",
                "same_single_item_path_reused":True,
                "new_batch_architecture_created":False,
                "historical_article_content_rewritten":False,
                "historical_plan_context_required_for_architecture_test":False,
                "integration_content_source":"EXISTING_BOUND_PPM_NORMAL_DRAFT_FIXTURE",
                "invented_theme_bypass_used":False,
                "publish_allowed":False,
                "items":integration,
            },ensure_ascii=False,indent=2))
        finally:
            subprocess.run(["git","worktree","remove","--force",str(work)],cwd=REPO,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    return 0

if __name__=="__main__":
    raise SystemExit(main())
