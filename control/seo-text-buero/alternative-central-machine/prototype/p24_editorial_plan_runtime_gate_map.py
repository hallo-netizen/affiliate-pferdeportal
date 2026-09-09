#!/usr/bin/env python3
from __future__ import annotations
import json,re,subprocess,tempfile,zipfile
from pathlib import Path

REPO=Path(__file__).resolve().parents[4]
PPM=REPO/"control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip"

GROUPS={
    "duplicate_cannibalization":["duplicate","cannibal","collision","ownership","unused","inventory"],
    "seo":["keyword","seo","title","slug"],
    "canonical_plan":["canonical","plan_item","slot","editorial_plan"],
    "wordpress_inventory":["wordpress","inventory","publish","draft","trash","pending","future"],
    "category":["category","taxonomy","term"],
}

TESTS=[
    "tests/test-v38-editorial-plan-journal-dedup.php",
    "tests/test-v38-editorial-plan-negative-controls.php",
    "tests/normal-draft-production/test-03-identity-replay-negative.php",
    "tests/normal-draft-production/test-02-cardinality-types-negative.php",
]

def class_block(text,name):
    m=re.search(r"class\s+"+re.escape(name)+r"\b",text)
    if not m:return ""
    brace=text.find("{",m.end()); depth=0
    for i in range(brace,len(text)):
        if text[i]=="{":depth+=1
        elif text[i]=="}":
            depth-=1
            if depth==0:return text[m.start():i+1]
    return text[m.start():]

def method_block(text,name):
    m=re.search(r"(?:public|private|protected)?\s*(?:static\s+)?function\s+"+re.escape(name)+r"\s*\(",text)
    if not m:return ""
    brace=text.find("{",m.end()); depth=0
    for i in range(brace,len(text)):
        if text[i]=="{":depth+=1
        elif text[i]=="}":
            depth-=1
            if depth==0:return text[m.start():i+1]
    return text[m.start():]

def hits(text):
    out={}
    for g,toks in GROUPS.items():
        rows=[]
        for n,line in enumerate(text.splitlines(),1):
            low=line.lower()
            if any(t.lower() in low for t in toks):
                rows.append({"line":n,"text":line.strip()[:550]})
        out[g]=rows[:100]
    return out

def main():
    with tempfile.TemporaryDirectory() as td:
        root=Path(td)
        with zipfile.ZipFile(PPM) as z:z.extractall(root)
        ppm=root/"portal-production-machine"

        src=(ppm/"includes/editorial-plan-runtime-gate.php").read_text(encoding="utf-8")
        cls=class_block(src,"PPM679_Editorial_Plan_Runtime_Gate")
        preflight=method_block(cls,"preflight")
        if not preflight: raise RuntimeError("EDITORIAL_PLAN_PREFLIGHT_MISSING")

        external=sorted(set(
            (a,b) for a,b in re.findall(r"([A-Za-z_][A-Za-z0-9_]*)::([A-Za-z_][A-Za-z0-9_]*)\s*\(",preflight)
            if a not in {"self","static","parent"}
        ))

        defs=[]
        for cname,method in external:
            for p in (ppm/"includes").rglob("*.php"):
                txt=p.read_text(encoding="utf-8")
                cb=class_block(txt,cname)
                if cb:
                    mb=method_block(cb,method)
                    defs.append({
                        "file":str(p.relative_to(ppm)),
                        "class":cname,
                        "method":method,
                        "chars":len(mb),
                        "hits":hits(mb),
                    })

        tests=[]
        for rel in TESTS:
            p=ppm/rel
            if not p.is_file():
                tests.append({"test":rel,"status":"MISSING"}); continue
            proc=subprocess.run(["php",str(p)],cwd=ppm,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            tests.append({"test":rel,"status":"PASS" if proc.returncode==0 else "FAIL","returncode":proc.returncode,"output_tail":proc.stdout[-2200:]})

        print(json.dumps({
            "status":"P24_EDITORIAL_PLAN_RUNTIME_GATE_MAP_PASS",
            "preflight_chars":len(preflight),
            "preflight_hits":hits(preflight),
            "external_calls":[{"class":a,"method":b} for a,b in external],
            "external_definitions":defs,
            "target_test_results":tests,
        },ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
