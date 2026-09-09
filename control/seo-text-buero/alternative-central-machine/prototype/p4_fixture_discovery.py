#!/usr/bin/env python3
from __future__ import annotations
import json, re, tempfile, zipfile
from pathlib import Path

REPO=Path(__file__).resolve().parents[4]
PPM=REPO/"control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip"
PSERC=REPO/"control/startmaster0107/runtime_packages/PSERC-FIX.zip"
INNER="PSERC-FIX/portal-seo-editorial-plan-compiler_0.28.18_ENDSTEMPEL_IMPORT_ENVELOPE_BINDING.zip"

def functions(text):
    return sorted(set(re.findall(r"function\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(",text)))

def main():
    with tempfile.TemporaryDirectory() as td:
        root=Path(td); po=root/"ppm"; xo=root/"outer"; so=root/"pserc"
        po.mkdir(); xo.mkdir(); so.mkdir()
        with zipfile.ZipFile(PPM) as z: z.extractall(po)
        with zipfile.ZipFile(PSERC) as z: z.extractall(xo)
        with zipfile.ZipFile(xo/INNER) as z: z.extractall(so)
        pr=po/"portal-production-machine"
        sr=so/"portal-seo-editorial-plan-compiler"
        nd=pr/"tests/normal-draft-production"
        fixture=nd/"fixture-builder.php"
        files=sorted(str(p.relative_to(pr)) for p in nd.rglob("*.php"))
        ftxt=fixture.read_text(encoding="utf-8")
        candidates=[]
        for p in nd.rglob("*.php"):
            txt=p.read_text(encoding="utf-8")
            if "execute_plan" in txt or "NORMAL_DRAFT_END_TO_END_READBACK_PASS_AWAITING_USER_CONTENT_REVIEW_NO_PUBLISH" in txt:
                candidates.append({
                    "file":str(p.relative_to(pr)),
                    "has_execute_plan":"execute_plan" in txt,
                    "has_final_status":"NORMAL_DRAFT_END_TO_END_READBACK_PASS_AWAITING_USER_CONTENT_REVIEW_NO_PUBLISH" in txt,
                    "functions":functions(txt)[:40],
                })
        print(json.dumps({
            "status":"P4_FIXTURE_DISCOVERY_PASS",
            "normal_draft_files":files,
            "fixture_functions":functions(ftxt),
            "candidate_test_files":candidates,
            "bridge_functions":functions((sr/"includes/class-pserc-ppm-intake-bridge.php").read_text(encoding="utf-8")),
        },ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
