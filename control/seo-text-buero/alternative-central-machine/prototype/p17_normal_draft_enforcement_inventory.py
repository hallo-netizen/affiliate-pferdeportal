#!/usr/bin/env python3
from __future__ import annotations
import json,re,subprocess,tempfile,zipfile
from pathlib import Path

REPO=Path(__file__).resolve().parents[4]
PPM=REPO/"control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip"

GROUPS={
    "article_type_structure":["article_type","template","structure"],
    "table":["table","PPM679_Table_Hard_Rule_Validator"],
    "links":["link","PPM679_WordPress_Link_Target_Validator"],
    "language":["languagetool","language_evidence","language"],
    "duplicate_cannibalization":["duplicate","cannibal"],
    "seo":["target_keyword","seo","keyword"],
    "design_format":["design","format","render"],
    "publish_safety":["publish_allowed","no_publish","publish"],
}

TESTS=[
    "tests/test-mainblock1-table-hard-rules.php",
    "tests/test-mainblock1-link-targets.php",
    "tests/test-wave2-content-mutations.php",
    "tests/test-v38-editorial-plan-journal-dedup.php",
    "tests/qf03-wordpress-draft-readback-dom/test-qf03-publish-prohibition.php",
]

def class_block(text:str,name:str)->str:
    m=re.search(r"class\s+"+re.escape(name)+r"\b",text)
    if not m:return ""
    brace=text.find("{",m.end())
    if brace<0:return ""
    depth=0
    for i in range(brace,len(text)):
        ch=text[i]
        if ch=="{": depth+=1
        elif ch=="}":
            depth-=1
            if depth==0:return text[m.start():i+1]
    return text[m.start():]

def function_block(text:str,name:str)->str:
    m=re.search(r"function\s+"+re.escape(name)+r"\s*\(",text)
    if not m:return ""
    brace=text.find("{",m.end())
    if brace<0:return ""
    depth=0
    for i in range(brace,len(text)):
        ch=text[i]
        if ch=="{": depth+=1
        elif ch=="}":
            depth-=1
            if depth==0:return text[m.start():i+1]
    return text[m.start():]

def excerpts(text:str,tokens):
    rows=[]
    for n,line in enumerate(text.splitlines(),1):
        low=line.lower()
        if any(t.lower() in low for t in tokens):
            rows.append({"line":n,"text":line.strip()[:500]})
    return rows[:60]

def main():
    with tempfile.TemporaryDirectory() as td:
        root=Path(td)
        with zipfile.ZipFile(PPM) as z:z.extractall(root)
        ppm=root/"portal-production-machine"
        pipeline_file=None
        pipeline=""
        for p in (ppm/"includes").rglob("*.php"):
            txt=p.read_text(encoding="utf-8")
            block=class_block(txt,"PPM679_Normal_Draft_Pipeline")
            if block:
                pipeline_file=p
                pipeline=block
                break
        if not pipeline_file:
            raise RuntimeError("NORMAL_DRAFT_PIPELINE_CLASS_NOT_FOUND")

        execute=function_block(pipeline,"execute_plan")
        calls=sorted(set(re.findall(r"([A-Za-z_][A-Za-z0-9_]*)::([A-Za-z_][A-Za-z0-9_]*)\s*\(",execute)))
        group_hits={k:excerpts(execute,v) for k,v in GROUPS.items()}

        tests=[]
        for rel in TESTS:
            p=ppm/rel
            if not p.is_file():
                tests.append({"test":rel,"status":"MISSING"})
                continue
            proc=subprocess.run(["php",str(p)],cwd=ppm,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            tests.append({
                "test":rel,
                "status":"PASS" if proc.returncode==0 else "FAIL",
                "returncode":proc.returncode,
                "output_tail":proc.stdout[-900:],
            })

        print(json.dumps({
            "status":"P17_NORMAL_DRAFT_ENFORCEMENT_INVENTORY_PASS",
            "pipeline_file":str(pipeline_file.relative_to(ppm)),
            "pipeline_class_chars":len(pipeline),
            "execute_plan_chars":len(execute),
            "execute_plan_calls":[{"class":a,"method":b} for a,b in calls],
            "execute_plan_group_hits":group_hits,
            "existing_rule_test_results":tests,
        },ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
