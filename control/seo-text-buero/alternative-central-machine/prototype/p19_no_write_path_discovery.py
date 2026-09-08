#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import tempfile
import zipfile
from pathlib import Path

REPO=Path(__file__).resolve().parents[4]
PPM=REPO/"control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip"

TOKENS=(
    "check_only",
    "check-only",
    "draft_allowed",
    "create_draft",
    "create_drafts",
    "no_write",
    "no-write",
    "dry_run",
    "dry-run",
    "live_write",
    "write_attempt",
)

def block(text:str,kind:str,name:str)->str:
    if kind=="class":
        m=re.search(r"class\s+"+re.escape(name)+r"\b",text)
    else:
        m=re.search(r"function\s+"+re.escape(name)+r"\s*\(",text)
    if not m:
        return ""
    brace=text.find("{",m.end())
    if brace<0:
        return ""
    depth=0
    for i in range(brace,len(text)):
        if text[i]=="{": depth+=1
        elif text[i]=="}":
            depth-=1
            if depth==0:
                return text[m.start():i+1]
    return text[m.start():]

def hits(text:str):
    rows=[]
    for n,line in enumerate(text.splitlines(),1):
        low=line.lower()
        matched=[t for t in TOKENS if t in low]
        if matched:
            rows.append({"line":n,"tokens":matched,"text":line.strip()[:500]})
    return rows

def main():
    with tempfile.TemporaryDirectory() as td:
        root=Path(td)
        with zipfile.ZipFile(PPM) as z:
            z.extractall(root)
        ppm=root/"portal-production-machine"

        pipeline_path=ppm/"includes/normal-draft-pipeline.php"
        pipeline_src=pipeline_path.read_text(encoding="utf-8")
        pipeline_cls=block(pipeline_src,"class","PPM679_Normal_Draft_Pipeline")
        execute=block(pipeline_cls,"function","execute_plan")
        create=block(pipeline_cls,"function","create_drafts")

        adapter_files=[]
        adapter_details=[]
        for p in (ppm/"includes").rglob("*.php"):
            txt=p.read_text(encoding="utf-8")
            cls=block(txt,"class","PPM679_Normal_Draft_Adapter")
            if cls:
                adapter_files.append(str(p.relative_to(ppm)))
                adapter_details.append({
                    "file":str(p.relative_to(ppm)),
                    "hits":hits(cls),
                    "methods":sorted(set(re.findall(r"function\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(",cls))),
                })

        candidates=[]
        for p in ppm.rglob("*"):
            if not p.is_file() or p.suffix.lower() not in {".php",".json",".md",".txt"}:
                continue
            try:
                txt=p.read_text(encoding="utf-8")
            except Exception:
                continue
            hs=hits(txt)
            if hs:
                candidates.append({
                    "file":str(p.relative_to(ppm)),
                    "hits":hs[:40],
                })

        normal_tests=[]
        nd=ppm/"tests/normal-draft-production"
        if nd.is_dir():
            for p in sorted(nd.rglob("*.php")):
                txt=p.read_text(encoding="utf-8")
                normal_tests.append({
                    "file":str(p.relative_to(ppm)),
                    "hits":hits(txt),
                    "mentions_create_draft":"create_draft" in txt,
                    "mentions_check_only":"check_only" in txt.lower(),
                })

        print(json.dumps({
            "status":"P19_NO_WRITE_PATH_DISCOVERY_PASS",
            "execute_plan_hits":hits(execute),
            "create_drafts_hits":hits(create),
            "adapter_files":adapter_files,
            "adapter_details":adapter_details,
            "normal_draft_tests":normal_tests,
            "all_candidates":candidates[:120],
        },ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
