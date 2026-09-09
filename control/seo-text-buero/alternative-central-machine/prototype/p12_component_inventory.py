#!/usr/bin/env python3
from __future__ import annotations

import json, tempfile, zipfile
from pathlib import Path

REPO=Path(__file__).resolve().parents[4]
PPM=REPO/"control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip"
PSERC=REPO/"control/startmaster0107/runtime_packages/PSERC-FIX.zip"
PSERC_INNER="PSERC-FIX/portal-seo-editorial-plan-compiler_0.28.18_ENDSTEMPEL_IMPORT_ENVELOPE_BINDING.zip"
PSTE=REPO/"PSTE_0.56.25"

TOKENS={
    "research_fact_pack":["fact_pack","research","source_hash"],
    "textmachine_article_type_structure":["textmachine","article_type","template"],
    "table_contract":["table_contract","table","exact-five"],
    "internal_links":["internal_link","internal links","link"],
    "languagetool":["languagetool","language_tool","language tool"],
    "ppm":["ppm679","ppm_action_report_v1","execute_plan"],
    "pserc":["pserc","workflow supervisor"],
    "pste":["pste","planning readiness","breadth research"],
    "duplicate_cannibalization":["duplicate","cannibal"],
    "seo":["seo","target_keyword","keyword"],
    "design_format":["design","format"],
    "publish_safety":["publish_allowed","no_publish","awaiting_user_content_review_no_publish"],
}

def scan(root: Path, label: str):
    hits={k:[] for k in TOKENS}
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if p.suffix.lower() not in {".php",".py",".json",".md",".txt"}:
            continue
        try:
            text=p.read_text(encoding="utf-8").lower()
        except Exception:
            continue
        rel=str(p.relative_to(root))
        for gate,tokens in TOKENS.items():
            if any(tok in text or tok in rel.lower() for tok in tokens):
                hits[gate].append(f"{label}:{rel}")
    return hits

def merge(*maps):
    out={k:[] for k in TOKENS}
    for m in maps:
        for k,v in m.items():
            out[k].extend(v)
    for k in out:
        out[k]=sorted(dict.fromkeys(out[k]))
    return out

def main():
    with tempfile.TemporaryDirectory() as td:
        root=Path(td)
        ppm_out=root/"ppm"; pserc_outer=root/"pserc_outer"; pserc_out=root/"pserc"
        ppm_out.mkdir(); pserc_outer.mkdir(); pserc_out.mkdir()
        with zipfile.ZipFile(PPM) as z: z.extractall(ppm_out)
        with zipfile.ZipFile(PSERC) as z: z.extractall(pserc_outer)
        inner=pserc_outer/PSERC_INNER
        if not inner.is_file():
            raise RuntimeError("PSERC_INNER_MISSING")
        with zipfile.ZipFile(inner) as z: z.extractall(pserc_out)

        ppm_root=ppm_out/"portal-production-machine"
        pserc_root=pserc_out/"portal-seo-editorial-plan-compiler"

        result=merge(
            scan(ppm_root,"PPM"),
            scan(pserc_root,"PSERC"),
            scan(PSTE,"PSTE"),
        )

        summary={}
        for gate,paths in result.items():
            owners=sorted(set(p.split(":",1)[0] for p in paths))
            summary[gate]={
                "owners":owners,
                "match_count":len(paths),
                "samples":paths[:12],
            }

        print(json.dumps({
            "status":"P12_COMPONENT_INVENTORY_PASS",
            "summary":summary,
        },ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
