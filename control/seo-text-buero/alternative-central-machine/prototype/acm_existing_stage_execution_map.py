#!/usr/bin/env python3
from __future__ import annotations
import json,re,tempfile,zipfile
from pathlib import Path

REPO=Path(__file__).resolve().parents[4]
PPM=REPO/"control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip"
PSERC=REPO/"control/startmaster0107/runtime_packages/PSERC-FIX.zip"
PSERC_INNER="PSERC-FIX/portal-seo-editorial-plan-compiler_0.28.18_ENDSTEMPEL_IMPORT_ENVELOPE_BINDING.zip"
PSTE=REPO/"PSTE_0.56.25"

STAGES={
 "research_fact_pack":["fact_pack","load_fact_pack","import_fact_pack_bundle","SOURCE_VERIFIED_PRODUCTION_READY"],
 "textmachine_article_type_structure":["Content_Generator","Content_Validator","article_type_templates","content-structure-language"],
 "table_contract":["Table_Hard_Rule_Validator","table-hard-rule","table_contract"],
 "internal_links":["WordPress_Link_Target_Validator","wordpress-link-target-validator","internal_link"],
 "languagetool":["LanguageTool","language_evidence","content-structure-language-gate"],
 "ppm":["Normal_Draft_Pipeline","execute_plan","Normal_Draft_Adapter"],
 "pserc":["PSERC_PPM_Intake_Bridge","class-pserc-ppm-intake-bridge"],
 "pste":["PSTE_PLANNING_READINESS","PSTE_PRE_TITLE_DUPLICATE","planning_readiness","keyword ownership"],
 "duplicate_cannibalization":["duplicate","cannibal","systemwide-duplicate-guard"],
 "seo":["target_keyword","TITLE_MUST_CONTAIN_TARGET_KEYWORD","keyword ownership"],
 "design_format":["Rendered_DOM","rendered-dom-validator","computed styles"],
 "publish_safety":["publish_allowed","publish-prohibition","AUTO_PUBLISH"]
}

def methods(txt:str):
    return sorted(set(re.findall(r"function\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(",txt)))

def classes(txt:str):
    return sorted(set(re.findall(r"class\s+([A-Za-z_][A-Za-z0-9_]*)\b",txt)))

def scan(root:Path,label:str):
    rows=[]
    for p in root.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in {".php",".py",".json",".md",".txt"}: continue
        try: txt=p.read_text(encoding="utf-8")
        except Exception: continue
        low=txt.lower()
        for stage,tokens in STAGES.items():
            hit=[t for t in tokens if t.lower() in low]
            if not hit: continue
            excerpts=[]
            for n,line in enumerate(txt.splitlines(),1):
                ll=line.lower()
                ht=[t for t in tokens if t.lower() in ll]
                if ht:
                    excerpts.append({"line":n,"tokens":ht,"text":line.strip()[:500]})
                    if len(excerpts)>=12: break
            rows.append({
              "stage":stage,"owner":label,"file":str(p.relative_to(root)),
              "classes":classes(txt)[:30],"methods":methods(txt)[:60],
              "hits":excerpts
            })
    return rows

def rank(rows,stage):
    preferred={
      "research_fact_pack":["storage","fact","fixture-builder"],
      "textmachine_article_type_structure":["content-generator","content-validator","structure-language"],
      "table_contract":["table-hard-rule"],
      "internal_links":["wordpress-link-target"],
      "languagetool":["content-structure-language"],
      "ppm":["normal-draft","adapter"],
      "pserc":["ppm-intake-bridge"],
      "pste":["planning","research","duplicate"],
      "duplicate_cannibalization":["duplicate"],
      "seo":["content-validator","keyword"],
      "design_format":["rendered-dom"],
      "publish_safety":["publish-prohibition","normal-draft"]
    }[stage]
    def score(r):
        f=r["file"].lower()
        s=sum(20 for x in preferred if x in f)
        if "/tests/" in "/"+f: s+=3
        if r["classes"]: s+=5
        if r["methods"]: s+=4
        return -s,f
    return sorted([r for r in rows if r["stage"]==stage],key=score)[:12]

def main():
    with tempfile.TemporaryDirectory() as td:
        t=Path(td); po=t/"ppm"; so=t/"pserc_outer"; ps=t/"pserc"
        po.mkdir();so.mkdir();ps.mkdir()
        with zipfile.ZipFile(PPM) as z:z.extractall(po)
        with zipfile.ZipFile(PSERC) as z:z.extractall(so)
        inner=so/PSERC_INNER
        if not inner.is_file():raise RuntimeError("PSERC_INNER_MISSING")
        with zipfile.ZipFile(inner) as z:z.extractall(ps)
        ppm=po/"portal-production-machine"
        pserc=ps/"portal-seo-editorial-plan-compiler"
        rows=scan(ppm,"PPM")+scan(pserc,"PSERC")+scan(PSTE,"PSTE")
        result={stage:rank(rows,stage) for stage in STAGES}
        missing=[k for k,v in result.items() if not v]
        if missing:raise RuntimeError("STAGE_EXECUTION_SOURCE_MISSING:"+",".join(missing))
        print(json.dumps({
          "status":"ACM_EXISTING_STAGE_EXECUTION_MAP_PASS",
          "new_stage_runner_created":False,
          "stages":result,
          "missing_stages":missing,
          "publish_allowed":False
        },ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
