#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import tempfile
import zipfile
from pathlib import Path

REPO=Path(__file__).resolve().parents[4]
PPM=REPO/"control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip"

TARGETS=(
    ("PPM679_Editorial_Plan_Runtime_Gate","preflight"),
    ("PPM679_Live_State_Gate","verify_live_state_or_abort"),
    ("PPM679_Plan_Validator","validate"),
    ("PPM679_Content_Generator","generate"),
    ("PPM679_Content_Validator","check"),
    ("PPM679_Normal_Draft_Adapter","prepare"),
)

WRITE_TOKENS=(
    "insert_draft","wp_insert_post","wp_update_post","set_post_status",
    "publish_post","transition_post_status","create_draft("
)

def class_block(text:str,name:str)->str:
    m=re.search(r"class\s+"+re.escape(name)+r"\b",text)
    if not m:return ""
    brace=text.find("{",m.end())
    if brace<0:return ""
    depth=0
    for i in range(brace,len(text)):
        if text[i]=="{":depth+=1
        elif text[i]=="}":
            depth-=1
            if depth==0:return text[m.start():i+1]
    return text[m.start():]

def method_block(cls:str,name:str):
    pat=r"((?:public|private|protected)?\s*(?:static\s+)?function\s+"+re.escape(name)+r"\s*\([^)]*\))"
    m=re.search(pat,cls)
    if not m:return None
    brace=cls.find("{",m.end())
    if brace<0:return None
    depth=0
    for i in range(brace,len(cls)):
        if cls[i]=="{":depth+=1
        elif cls[i]=="}":
            depth-=1
            if depth==0:
                src=cls[m.start():i+1]
                return {"signature":m.group(1).strip(),"source":src}
    return None

def main():
    with tempfile.TemporaryDirectory() as td:
        out=Path(td)
        with zipfile.ZipFile(PPM) as z:z.extractall(out)
        root=out/"portal-production-machine"

        rows=[]
        for cname,mname in TARGETS:
            found=None
            for p in (root/"includes").rglob("*.php"):
                txt=p.read_text(encoding="utf-8")
                cls=class_block(txt,cname)
                if not cls:continue
                mb=method_block(cls,mname)
                if mb:
                    low=mb["source"].lower()
                    found={
                        "class":cname,
                        "method":mname,
                        "file":str(p.relative_to(root)),
                        "signature":mb["signature"],
                        "visibility":"public" if mb["signature"].lstrip().startswith("public") or mb["signature"].lstrip().startswith("static") or mb["signature"].lstrip().startswith("function") else mb["signature"].split()[0],
                        "static":"static" in mb["signature"],
                        "wordpress_write_tokens":[t for t in WRITE_TOKENS if t in low],
                    }
                    break
            if not found:
                raise RuntimeError("PREWRITE_API_MISSING:"+cname+"::"+mname)
            rows.append(found)

        if any(r["visibility"]!="public" or not r["static"] for r in rows):
            raise RuntimeError("PREWRITE_API_NOT_PUBLIC_STATIC")
        if any(r["wordpress_write_tokens"] for r in rows):
            raise RuntimeError("PREWRITE_API_CONTAINS_DRAFT_WRITE")

        print(json.dumps({
            "status":"P44_PREWRITE_API_INVENTORY_PASS",
            "apis":rows,
            "all_required_apis_public_static":True,
            "direct_wordpress_draft_write_found":False,
            "new_ppm_api_required":False,
            "new_fachlogic_required":False,
            "publish_allowed":False,
        },ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
