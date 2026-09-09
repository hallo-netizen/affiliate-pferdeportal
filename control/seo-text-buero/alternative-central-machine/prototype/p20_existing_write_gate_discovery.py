#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import tempfile
import zipfile
from pathlib import Path

REPO=Path(__file__).resolve().parents[4]
PPM=REPO/"control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip"

NEEDLES=(
    "PASS_V31_WRITE_PLAN_PREPARED_NO_WRITE",
    "planned_write_fingerprint",
    "DRY_RUN_AND_WRITE_MUST_USE_IDENTICAL_PLANNED_WRITE_FINGERPRINT",
    "stateful_write_gate",
    "Stateful_Write_Gate",
)

def class_names(text:str):
    return sorted(set(re.findall(r"class\s+([A-Za-z_][A-Za-z0-9_]*)\b",text)))

def methods(text:str):
    return sorted(set(re.findall(r"function\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(",text)))

def hit_lines(text:str,needles=NEEDLES):
    rows=[]
    for n,line in enumerate(text.splitlines(),1):
        low=line.lower()
        ms=[x for x in needles if x.lower() in low]
        if ms:
            rows.append({"line":n,"needles":ms,"text":line.strip()[:600]})
    return rows

def main():
    with tempfile.TemporaryDirectory() as td:
        root=Path(td)
        with zipfile.ZipFile(PPM) as z:
            z.extractall(root)
        ppm=root/"portal-production-machine"

        candidates=[]
        for p in ppm.rglob("*"):
            if not p.is_file() or p.suffix.lower() not in {".php",".json",".md",".txt"}:
                continue
            try:
                txt=p.read_text(encoding="utf-8")
            except Exception:
                continue
            hs=hit_lines(txt)
            if hs:
                candidates.append({
                    "file":str(p.relative_to(ppm)),
                    "classes":class_names(txt),
                    "methods":methods(txt),
                    "hits":hs[:80],
                })

        normal_refs={}
        for rel in ["includes/normal-draft-pipeline.php","includes/normal-draft-adapter.php"]:
            p=ppm/rel
            txt=p.read_text(encoding="utf-8")
            normal_refs[rel]={
                "write_gate_refs":hit_lines(txt),
                "planned_write_mentions":[
                    {"line":n,"text":line.strip()[:600]}
                    for n,line in enumerate(txt.splitlines(),1)
                    if "planned_write" in line.lower() or "fingerprint" in line.lower()
                ][:80],
            }

        test_candidates=[]
        for p in (ppm/"tests").rglob("*.php"):
            txt=p.read_text(encoding="utf-8")
            if any(x.lower() in txt.lower() for x in NEEDLES):
                test_candidates.append({
                    "file":str(p.relative_to(ppm)),
                    "classes":class_names(txt),
                    "methods":methods(txt),
                    "hits":hit_lines(txt)[:80],
                })

        print(json.dumps({
            "status":"P20_EXISTING_WRITE_GATE_DISCOVERY_PASS",
            "candidates":candidates,
            "normal_draft_refs":normal_refs,
            "test_candidates":test_candidates,
        },ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
