#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import tempfile
import zipfile
from pathlib import Path

REPO=Path(__file__).resolve().parents[4]
PPM=REPO/"control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip"

NEEDED=(
    "PPM679_Editorial_Plan_Runtime_Gate::preflight",
    "PPM679_Live_State_Gate::verify_live_state_or_abort",
    "PPM679_Plan_Validator::validate",
    "self::bootstrap",
    "self::generate_all",
    "self::check_all",
    "self::create_drafts",
)

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

def method_block(text:str,name:str)->str:
    m=re.search(r"(?:public|private|protected)?\s*(?:static\s+)?function\s+"+re.escape(name)+r"\s*\(",text)
    if not m:return ""
    brace=text.find("{",m.end()); depth=0
    for i in range(brace,len(text)):
        if text[i]=="{":depth+=1
        elif text[i]=="}":
            depth-=1
            if depth==0:return text[m.start():i+1]
    return text[m.start():]

def main():
    with tempfile.TemporaryDirectory() as td:
        out=Path(td)
        with zipfile.ZipFile(PPM) as z:z.extractall(out)
        root=out/"portal-production-machine"
        src=(root/"includes/normal-draft-pipeline.php").read_text(encoding="utf-8")
        cls=class_block(src,"PPM679_Normal_Draft_Pipeline")
        execute=method_block(cls,"execute_plan")
        if not execute:
            raise RuntimeError("EXECUTE_PLAN_MISSING")

        rows=[]
        positions={}
        for n,line in enumerate(execute.splitlines(),1):
            for token in NEEDED:
                if token in line:
                    positions[token]=execute.find(token)
                    rows.append({"line":n,"token":token,"source":line.strip()[:1200]})

        missing=[x for x in NEEDED if x not in positions]
        if missing:
            raise RuntimeError("PREWRITE_SEQUENCE_TOKEN_MISSING:"+",".join(missing))

        ordered=sorted(positions,key=positions.get)
        expected=[
            "PPM679_Editorial_Plan_Runtime_Gate::preflight",
            "PPM679_Live_State_Gate::verify_live_state_or_abort",
            "PPM679_Plan_Validator::validate",
            "self::bootstrap",
            "self::generate_all",
            "self::check_all",
            "self::create_drafts",
        ]
        if ordered!=expected:
            raise RuntimeError("EXECUTE_PLAN_ORDER_DRIFT:"+json.dumps(ordered))

        cutoff=positions["self::create_drafts"]
        prewrite=execute[:cutoff]
        forbidden=("PPM679_Normal_Draft_Adapter::create_draft","PPM679_WP::insert_draft","wp_insert_post","publish_post")
        found=[x for x in forbidden if x in prewrite]
        if found:
            raise RuntimeError("WRITE_BEFORE_CREATE_DRAFTS_FOUND:"+",".join(found))

        print(json.dumps({
            "status":"P45_EXECUTE_PLAN_PREWRITE_SEQUENCE_PASS",
            "sequence":ordered[:-1],
            "write_boundary":"self::create_drafts",
            "exact_call_lines":rows,
            "prewrite_contains_wordpress_draft_write":False,
            "new_sequence_invented":False,
            "source_of_sequence":"PPM679_Normal_Draft_Pipeline::execute_plan",
            "publish_allowed":False,
        },ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
