#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

from central_machine import CentralMachine
from p7_release_boundary import canon
from p10_batch_resume import JOB_CONTRACT, next_incomplete_item

HERE=Path(__file__).resolve().parent

def sign(private:Path,data:Path,sig:Path):
    subprocess.run(
        ["openssl","pkeyutl","-sign","-inkey",str(private),"-rawin","-in",str(data),"-out",str(sig)],
        check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
    )

def main():
    # 1. No architectural article-count cap: verify a large signed job using the existing P10 mechanism.
    with tempfile.TemporaryDirectory() as td:
        root=Path(td)
        releases=root/"releases"; releases.mkdir()
        private=root/"private.pem"; public=root/"public.pem"
        subprocess.run(["openssl","genpkey","-algorithm","Ed25519","-out",str(private)],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        subprocess.run(["openssl","pkey","-in",str(private),"-pubout","-out",str(public)],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

        count=1000
        job={
            "contract":JOB_CONTRACT,
            "job_id":"P34-BATCH",
            "items":[{"item_id":f"ITEM-{i:04d}","input":{"topic":f"topic-{i}"}} for i in range(count)],
            "publish_allowed":False,
        }
        job_path=root/"job.json"; job_sig=root/"job.sig"
        job_path.write_bytes(canon(job)); sign(private,job_path,job_sig)
        nxt=next_incomplete_item(job_path,job_sig,public,releases)
        if nxt is None or nxt["item_id"]!="ITEM-0000":
            raise RuntimeError("LARGE_BATCH_NOT_ACCEPTED")

    p10=(HERE/"p10_batch_resume.py").read_text(encoding="utf-8")
    forbidden_caps=("MAX_ITEMS","MAX_ARTICLES","ARTICLE_LIMIT","BATCH_LIMIT","count >","len(items) >")
    if any(x in p10 for x in forbidden_caps):
        raise RuntimeError("ARCHITECTURAL_BATCH_LIMIT_FOUND")

    # 2. Controller itself must not contain portal/domain decisions.
    core=(HERE/"central_machine.py").read_text(encoding="utf-8").lower()
    domain_tokens=("pferdeanhänger","pferdedecke","reitsport","horse","equine")
    if any(x.lower() in core for x in domain_tokens):
        raise RuntimeError("DOMAIN_LOGIC_IN_CENTRAL_CONTROLLER")

    # 3. Fixed controller API: no caller-selected route/validator/next-step hooks.
    m=CentralMachine("P34-JOB","P34-ITEM")
    for attr in ("set_next_step","set_validator","set_route","choose_worker","set_engine"):
        if hasattr(m,attr):
            raise RuntimeError("FREE_CONTROL_API_FOUND:"+attr)

    print(json.dumps({
        "status":"P34_MACRO_INVARIANTS_PASS",
        "large_signed_batch_items":1000,
        "architectural_batch_limit_found":False,
        "processing_model":"SEQUENTIAL_ITEMS_NO_FIXED_COUNT_LIMIT",
        "central_controller_domain_specific_logic":False,
        "caller_selected_route_or_validator":False,
        "physical_infinity_claimed":False,
        "meaning":"ARBITRARY_FINITE_BATCH_SIZE_SUBJECT_ONLY_TO_REAL_RESOURCE_LIMITS",
        "publish_allowed":False,
    },ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
