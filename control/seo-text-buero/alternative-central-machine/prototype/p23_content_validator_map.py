#!/usr/bin/env python3
from __future__ import annotations
import json,re,subprocess,tempfile,zipfile
from pathlib import Path

REPO=Path(__file__).resolve().parents[4]
PPM=REPO/"control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip"

GROUPS={
    "article_type_structure":["article_type","template","structure","heading","intro","section"],
    "table":["table","tbody","thead","td","th"],
    "links":["internal_link","link_target","href","link"],
    "language":["languagetool","language_evidence","language","forbidden_phrase"],
    "duplicate_cannibalization":["duplicate","cannibal","collision","ownership"],
    "seo":["target_keyword","keyword","seo","title"],
    "design_format":["design","format","html","render","dom"],
    "publish_safety":["publish_allowed","publish","draft"],
    "fact_pack":["fact_pack","source_snapshot","fact"],
}

TESTS=[
    "tests/normal-draft-production/test-04-content-source-link-negative.php",
    "tests/test-wave2-content-mutations.php",
    "tests/test-mainblock1-table-hard-rules.php",
    "tests/test-mainblock1-link-targets.php",
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
                rows.append({"line":n,"text":line.strip()[:500]})
        out[g]=rows[:80]
    return out

def main():
    with tempfile.TemporaryDirectory() as td:
        root=Path(td)
        with zipfile.ZipFile(PPM) as z:z.extractall(root)
        ppm=root/"portal-production-machine"
        src=(ppm/"includes/content-validator.php").read_text(encoding="utf-8")
        cls=class_block(src,"PPM679_Content_Validator")
        check=method_block(cls,"check")
        if not check: raise RuntimeError("CONTENT_VALIDATOR_CHECK_MISSING")

        external=sorted(set(
            (a,b) for a,b in re.findall(r"([A-Za-z_][A-Za-z0-9_]*)::([A-Za-z_][A-Za-z0-9_]*)\s*\(",check)
            if a not in {"self","static","parent"}
        ))
        defs=[]
        for cname,method in external:
            found=[]
            for p in (ppm/"includes").rglob("*.php"):
                txt=p.read_text(encoding="utf-8")
                cb=class_block(txt,cname)
                if cb:
                    mb=method_block(cb,method)
                    found.append({
                        "file":str(p.relative_to(ppm)),
                        "class":cname,
                        "method":method,
                        "method_chars":len(mb),
                        "gate_hits":hits(mb),
                    })
            defs.extend(found)

        results=[]
        for rel in TESTS:
            p=ppm/rel
            if not p.is_file():
                results.append({"test":rel,"status":"MISSING"}); continue
            proc=subprocess.run(["php",str(p)],cwd=ppm,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            results.append({"test":rel,"status":"PASS" if proc.returncode==0 else "FAIL","returncode":proc.returncode,"output_tail":proc.stdout[-1800:]})

        print(json.dumps({
            "status":"P23_CONTENT_VALIDATOR_MAP_PASS",
            "check_chars":len(check),
            "check_gate_hits":hits(check),
            "external_calls":[{"class":a,"method":b} for a,b in external],
            "external_definitions":defs,
            "target_test_results":results,
        },ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
