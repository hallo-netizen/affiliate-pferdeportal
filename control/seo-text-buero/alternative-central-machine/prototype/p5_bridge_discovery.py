#!/usr/bin/env python3
from __future__ import annotations
import json, re, tempfile, zipfile
from pathlib import Path

REPO=Path(__file__).resolve().parents[4]
PSERC=REPO/"control/startmaster0107/runtime_packages/PSERC-FIX.zip"
INNER="PSERC-FIX/portal-seo-editorial-plan-compiler_0.28.18_ENDSTEMPEL_IMPORT_ENVELOPE_BINDING.zip"

def funcs(text):
    return sorted(set(re.findall(r"function\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(",text)))

def main():
    with tempfile.TemporaryDirectory() as td:
        root=Path(td); outer=root/"outer"; src=root/"src"; outer.mkdir(); src.mkdir()
        with zipfile.ZipFile(PSERC) as z: z.extractall(outer)
        inner=outer/INNER
        if not inner.is_file():
            raise RuntimeError("PSERC_INNER_ZIP_MISSING")
        with zipfile.ZipFile(inner) as z: z.extractall(src)
        pr=src/"portal-seo-editorial-plan-compiler"
        candidates=[]
        for p in pr.rglob("*.php"):
            txt=p.read_text(encoding="utf-8")
            if "PSERC_PPM_Intake_Bridge::execute" in txt or "PSERC_PPM_INTAKE_BRIDGE_EXECUTED" in txt:
                candidates.append({
                    "file":str(p.relative_to(pr)),
                    "has_execute_call":"PSERC_PPM_Intake_Bridge::execute" in txt,
                    "has_success_status":"PSERC_PPM_INTAKE_BRIDGE_EXECUTED" in txt,
                    "functions":funcs(txt)[:40],
                })
        print(json.dumps({
            "status":"P5_BRIDGE_DISCOVERY_PASS",
            "candidate_test_files":candidates,
        },ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
