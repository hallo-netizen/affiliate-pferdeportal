#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

from p7_release_boundary import canon
from p10_batch_resume import JOB_CONTRACT
from p36_kiss_real_controller import ControllerBlocked, execute_signed_job

HERE=Path(__file__).resolve().parent
P22=HERE/"p22_signed_normal_draft_integration.py"

def parse_status(output:str,status:str)->dict:
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
    raise RuntimeError("STATUS_MISSING:"+status+"\n"+output[-4000:])

def run_p22(*args:str):
    p=subprocess.run(
        ["python3",str(P22),*args],
        cwd=HERE.parents[3],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=300,
    )
    return p.returncode,p.stdout

def keypair(root:Path):
    private=root/"private.pem"; public=root/"public.pem"
    subprocess.run(["openssl","genpkey","-algorithm","Ed25519","-out",str(private)],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    subprocess.run(["openssl","pkey","-in",str(private),"-pubout","-out",str(public)],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    return private,public

def sign(private:Path,data:Path,sig:Path):
    subprocess.run(["openssl","pkeyutl","-sign","-inkey",str(private),"-rawin","-in",str(data),"-out",str(sig)],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

def signed_job(root:Path,private:Path,item_id:str,job_id:str):
    job={
        "contract":JOB_CONTRACT,
        "job_id":job_id,
        "items":[{"item_id":item_id,"input":{"binding_test":"P37"}}],
        "publish_allowed":False,
    }
    path=root/(job_id+".json"); sig=root/(job_id+".sig")
    path.write_bytes(canon(job)); sign(private,path,sig)
    return path,sig

def main():
    # Discover the actual deterministic item identity produced by the already-bound PPM fixture.
    rc,out=run_p22()
    if rc!=0:
        raise RuntimeError("P37_BOOTSTRAP_P22_FAILED:"+out[-4000:])
    bootstrap=parse_status(out,"P22_SIGNED_NORMAL_DRAFT_BOUNDARY_PASS")
    actual_item_id=bootstrap.get("item_id")
    if not isinstance(actual_item_id,str) or not actual_item_id:
        raise RuntimeError("P37_BOOTSTRAP_ITEM_ID_MISSING")

    with tempfile.TemporaryDirectory() as td:
        root=Path(td)
        private,public=keypair(root)

        # Positive: signed job item ID equals the PPM prepared plan_item_key.
        job_path,job_sig=signed_job(root,private,actual_item_id,"P37-POSITIVE")
        receipt=execute_signed_job(job_path,job_sig,public)
        if receipt["status"]!="JOB_PASS_NO_PUBLISH":
            raise RuntimeError("P37_BOUND_CONTROLLER_NOT_PASS")
        if receipt["completed_count"]!=1 or receipt["items"][0]["item_id"]!=actual_item_id:
            raise RuntimeError("P37_BOUND_CONTROLLER_ITEM_DRIFT")
        if receipt["publish_allowed"] is not False:
            raise RuntimeError("P37_PUBLISH_NOT_FALSE")

        # Negative direct adapter: wrong signed item identity must block after no-write prepare
        # and before signing/write.
        wrong_item_id="WRONG-"+actual_item_id
        rc_bad,out_bad=run_p22("--job-id","P37-NEGATIVE","--expected-item-id",wrong_item_id)
        if rc_bad==0:
            raise RuntimeError("P37_WRONG_ITEM_NOT_BLOCKED")
        blocked=parse_status(out_bad,"P22_BOUND_ITEM_ID_BLOCKED")
        if blocked.get("prepared_item_id")!=actual_item_id:
            raise RuntimeError("P37_NEGATIVE_PREPARED_ID_UNEXPECTED")
        if blocked.get("expected_item_id")!=wrong_item_id:
            raise RuntimeError("P37_NEGATIVE_EXPECTED_ID_UNEXPECTED")
        if blocked.get("prepare_no_write") is not True:
            raise RuntimeError("P37_NEGATIVE_PREPARE_WROTE")
        if blocked.get("signing_started") is not False or blocked.get("write_started") is not False:
            raise RuntimeError("P37_NEGATIVE_BOUNDARY_TOO_LATE")

        # Negative through controller: even a correctly signed job with the wrong item ID
        # cannot push a different prepared item through the fixed adapter.
        bad_job,bad_sig=signed_job(root,private,wrong_item_id,"P37-WRONG-JOB")
        controller_blocked=False
        try:
            execute_signed_job(bad_job,bad_sig,public)
        except ControllerBlocked:
            controller_blocked=True
        if not controller_blocked:
            raise RuntimeError("P37_CONTROLLER_WRONG_ITEM_NOT_BLOCKED")

        print(json.dumps({
            "status":"P37_ITEM_IDENTITY_BINDING_PASS",
            "actual_ppm_plan_item_key":actual_item_id,
            "positive_signed_job_bound_to_exact_ppm_item":True,
            "controller_receipt_item_id_matches":True,
            "wrong_item_blocked_before_signing":True,
            "wrong_item_blocked_before_write":True,
            "prepare_remained_no_write_on_mismatch":True,
            "signed_wrong_job_blocked_by_controller":True,
            "route_runtime_selectable":False,
            "publish_allowed":False,
        },ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
