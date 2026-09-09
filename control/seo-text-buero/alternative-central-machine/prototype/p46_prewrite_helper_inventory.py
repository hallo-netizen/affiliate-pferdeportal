#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import tempfile
import zipfile
from pathlib import Path

REPO=Path(__file__).resolve().parents[4]
PPM=REPO/"control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip"

HELPERS=("bootstrap","generate_all","check_all","create_drafts")

def class_block(text:str,name:str)->str:
    m=re.search(r"class\s+"+re.escape(name)+r"\b",text)
    if not m:return ""
    brace=text.find("{",m.end()); depth=0
    for i in range(brace,len(text)):
        if text[i]=="{":depth+=1
        elif text[i]=="}":
            depth-=1
            if depth==0:return text[m.start():i+1]
    return text[m.start():]

def method_info(cls:str,name:str):
    pat=r"((?:public|private|protected)?\s*(?:static\s+)?function\s+"+re.escape(name)+r"\s*\([^)]*\))"
    m=re.search(pat,cls)
    if not m:return None
    brace=cls.find("{",m.end()); depth=0
    end=None
    for i in range(brace,len(cls)):
        if cls[i]=="{":depth+=1
        elif cls[i]=="}":
            depth-=1
            if depth==0:
                end=i+1; break
    if end is None:return None
    sig=m.group(1).strip()
    visibility="public"
    stripped=sig.lstrip()
    if stripped.startswith("private"):visibility="private"
    elif stripped.startswith("protected"):visibility="protected"
    return {"signature":sig,"visibility":visibility,"static":"static" in sig,"source":cls[m.start():end]}

def main():
    with tempfile.TemporaryDirectory() as td:
        out=Path(td)
        with zipfile.ZipFile(PPM) as z:z.extractall(out)
        root=out/"portal-production-machine"
        src=(root/"includes/normal-draft-pipeline.php").read_text(encoding="utf-8")
        cls=class_block(src,"PPM679_Normal_Draft_Pipeline")
        execute=method_info(cls,"execute_plan")
        if not execute:raise RuntimeError("EXECUTE_PLAN_MISSING")

        cutoff=execute["source"].find("$drafts=self::create_drafts")
        if cutoff<0:raise RuntimeError("CREATE_DRAFT_BOUNDARY_MISSING")
        prewrite=execute["source"][:cutoff]

        helpers={}
        for name in HELPERS:
            info=method_info(cls,name)
            if not info:raise RuntimeError("HELPER_MISSING:"+name)
            helpers[name]={
                "signature":info["signature"],
                "visibility":info["visibility"],
                "static":info["static"],
            }

        # Keep only executable lines needed to reproduce existing orchestration,
        # not prose or new interpretation.
        lines=[]
        for n,line in enumerate(prewrite.splitlines(),1):
            stripped=line.strip()
            if not stripped:continue
            if any(tok in stripped for tok in (
                "$plan_hash=","$scope=","$editorial_candidates=","$requirements=",
                "Editorial_Plan_Runtime_Gate::preflight",
                "Live_State_Gate::verify_live_state_or_abort",
                "Plan_Validator::validate",
                "Storage::","$run_id=","$run=",
                "self::bootstrap","$workspace_hash=",
                "self::generate_all","$generated_hash=",
                "self::check_all","$check_hash="
            )):
                lines.append({"line":n,"source":stripped[:1800]})

        print(json.dumps({
            "status":"P46_PREWRITE_HELPER_INVENTORY_PASS",
            "helpers":helpers,
            "existing_prewrite_orchestration_lines":lines,
            "create_drafts_boundary_found":True,
            "new_helper_required":False,
            "publish_allowed":False,
        },ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
