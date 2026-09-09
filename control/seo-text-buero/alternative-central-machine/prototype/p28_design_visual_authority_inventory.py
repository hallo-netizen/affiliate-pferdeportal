#!/usr/bin/env python3
from __future__ import annotations
import json,re,tempfile,zipfile
from pathlib import Path

REPO=Path(__file__).resolve().parents[4]
PPM=REPO/"control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip"
PSERC=REPO/"control/startmaster0107/runtime_packages/PSERC-FIX.zip"
PSERC_INNER="PSERC-FIX/portal-seo-editorial-plan-compiler_0.28.18_ENDSTEMPEL_IMPORT_ENVELOPE_BINDING.zip"
PSTE=REPO/"PSTE_0.56.25"

TOKENS=("design","visual","layout","render","format","dom","html","presentation")
AI=("claude","reviewer","human","manual","llm","gpt","openai","anthropic")

def lines(text):
    rows=[]
    for n,line in enumerate(text.splitlines(),1):
        low=line.lower()
        ts=[t for t in TOKENS if t in low]
        if ts:
            rows.append({
              "line":n,
              "tokens":ts,
              "ai_tokens":[a for a in AI if a in low],
              "text":line.strip()[:650],
            })
    return rows

def scan(root,label,limit=160):
    rows=[]
    for p in root.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in {".php",".json",".md",".txt",".py"}:
            continue
        try: txt=p.read_text(encoding="utf-8")
        except Exception: continue
        hs=lines(txt)
        if hs:
            rows.append({"owner":label,"file":str(p.relative_to(root)),"hits":hs[:80]})
    rows.sort(key=lambda x:(0 if any(k in x["file"].lower() for k in ("contract","test","gate","validator")) else 1,x["file"]))
    return rows[:limit]

def hard_rules(ppm):
    p=ppm/"contracts/hard-rule-registry-v1.json"
    data=json.loads(p.read_text(encoding="utf-8"))
    out=[]
    for rule in data.get("rules",[]):
        if not isinstance(rule,dict): continue
        blob=json.dumps(rule,ensure_ascii=False).lower()
        if any(t in blob for t in TOKENS):
            out.append({
              "rule_id":rule.get("rule_id"),
              "title":rule.get("title"),
              "validator_or_reviewer":rule.get("validator_or_reviewer"),
              "required_evidence":rule.get("required_evidence"),
              "error_code":rule.get("error_code"),
              "positive_test":rule.get("positive_test"),
              "negative_test":rule.get("negative_test"),
              "source_path":rule.get("source_path"),
              "ai_or_manual_reference":any(a in blob for a in AI),
            })
    return out

def main():
    with tempfile.TemporaryDirectory() as td:
        t=Path(td); po=t/"ppm"; so=t/"pserc_outer"; ps=t/"pserc"
        po.mkdir();so.mkdir();ps.mkdir()
        with zipfile.ZipFile(PPM) as z:z.extractall(po)
        with zipfile.ZipFile(PSERC) as z:z.extractall(so)
        inner=so/PSERC_INNER
        if not inner.is_file(): raise RuntimeError("PSERC_INNER_MISSING")
        with zipfile.ZipFile(inner) as z:z.extractall(ps)
        ppm=po/"portal-production-machine"
        pserc=ps/"portal-seo-editorial-plan-compiler"

        ppm_rows=scan(ppm,"PPM")
        pserc_rows=scan(pserc,"PSERC")
        pste_rows=scan(PSTE,"PSTE")

        explicit_scope=[]
        for row in ppm_rows:
            for h in row["hits"]:
                low=h["text"].lower()
                if "no final editorial or visual pass" in low or "visual pass" in low or "final visual" in low:
                    explicit_scope.append({"file":row["file"],**h})

        tests=[]
        for root,label in ((ppm,"PPM"),(pserc,"PSERC"),(PSTE,"PSTE")):
            tp=root/"tests"
            if not tp.is_dir(): continue
            for p in tp.rglob("*"):
                if not p.is_file() or p.suffix.lower() not in {".php",".py",".sh"}: continue
                try: txt=p.read_text(encoding="utf-8")
                except Exception: continue
                if any(t in (str(p.relative_to(root))+" "+txt).lower() for t in TOKENS):
                    tests.append({"owner":label,"file":str(p.relative_to(root)),"hits":lines(txt)[:40]})

        print(json.dumps({
          "status":"P28_DESIGN_VISUAL_AUTHORITY_INVENTORY_PASS",
          "ppm_hard_rules":hard_rules(ppm),
          "explicit_scope_boundaries":explicit_scope,
          "matching_tests":tests[:120],
          "ppm_matches":ppm_rows[:100],
          "pserc_matches":pserc_rows[:80],
          "pste_matches":pste_rows[:80],
        },ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
