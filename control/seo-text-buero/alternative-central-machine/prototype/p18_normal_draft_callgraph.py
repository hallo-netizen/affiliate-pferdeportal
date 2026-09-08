#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import tempfile
import zipfile
from collections import deque
from pathlib import Path

REPO=Path(__file__).resolve().parents[4]
PPM=REPO/"control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip"

GROUPS={
    "article_type_structure":["article_type","template","structure","content_contract"],
    "table":["table","PPM679_Table_Hard_Rule_Validator"],
    "links":["internal_link","link_target","PPM679_WordPress_Link_Target_Validator"],
    "language":["languagetool","language_evidence","language_tool","language"],
    "duplicate_cannibalization":["duplicate","cannibal","ownership_collision"],
    "seo":["target_keyword","keyword","seo"],
    "design_format":["design","format","rendered","dom"],
    "publish_safety":["publish_allowed","no_publish","publish"],
}

def class_block(text:str,name:str)->str:
    m=re.search(r"class\s+"+re.escape(name)+r"\b",text)
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

def method_blocks(cls:str):
    methods={}
    pat=re.compile(r"(?:public|private|protected)?\s*(?:static\s+)?function\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(")
    for m in pat.finditer(cls):
        name=m.group(1)
        brace=cls.find("{",m.end())
        if brace<0:
            continue
        depth=0
        end=None
        for i in range(brace,len(cls)):
            if cls[i]=="{": depth+=1
            elif cls[i]=="}":
                depth-=1
                if depth==0:
                    end=i+1
                    break
        if end is not None:
            methods[name]=cls[m.start():end]
    return methods

def token_hits(text:str):
    out={}
    for group,tokens in GROUPS.items():
        rows=[]
        for n,line in enumerate(text.splitlines(),1):
            low=line.lower()
            if any(tok.lower() in low for tok in tokens):
                rows.append({"line":n,"text":line.strip()[:400]})
        out[group]=rows[:40]
    return out

def main():
    with tempfile.TemporaryDirectory() as td:
        root=Path(td)
        with zipfile.ZipFile(PPM) as z:
            z.extractall(root)
        ppm=root/"portal-production-machine"
        src=(ppm/"includes/normal-draft-pipeline.php").read_text(encoding="utf-8")
        cls=class_block(src,"PPM679_Normal_Draft_Pipeline")
        if not cls:
            raise RuntimeError("NORMAL_DRAFT_CLASS_MISSING")
        methods=method_blocks(cls)
        if "execute_plan" not in methods:
            raise RuntimeError("EXECUTE_PLAN_MISSING")

        reachable=[]
        seen=set()
        q=deque(["execute_plan"])
        edges=[]
        while q:
            name=q.popleft()
            if name in seen:
                continue
            seen.add(name)
            reachable.append(name)
            body=methods.get(name,"")
            self_calls=sorted(set(re.findall(r"self::([A-Za-z_][A-Za-z0-9_]*)\s*\(",body)))
            for callee in self_calls:
                edges.append({"from":name,"to":callee})
                if callee in methods and callee not in seen:
                    q.append(callee)

        details={}
        external_classes=set()
        for name in reachable:
            body=methods[name]
            external=sorted(set(
                (a,b) for a,b in re.findall(r"([A-Za-z_][A-Za-z0-9_]*)::([A-Za-z_][A-Za-z0-9_]*)\s*\(",body)
                if a not in {"self","static","parent"}
            ))
            external_classes.update(a for a,_ in external)
            details[name]={
                "chars":len(body),
                "self_calls":sorted(set(re.findall(r"self::([A-Za-z_][A-Za-z0-9_]*)\s*\(",body))),
                "external_calls":[{"class":a,"method":b} for a,b in external],
                "gate_token_hits":token_hits(body),
            }

        definitions={}
        for clsname in sorted(external_classes):
            rows=[]
            for p in (ppm/"includes").rglob("*.php"):
                txt=p.read_text(encoding="utf-8")
                if re.search(r"class\s+"+re.escape(clsname)+r"\b",txt):
                    rows.append(str(p.relative_to(ppm)))
            definitions[clsname]=rows

        expected={"execute_plan","bootstrap","generate_all","check_all","create_drafts","readback"}
        missing=sorted(expected-set(reachable))
        if missing:
            raise RuntimeError("EXPECTED_PIPELINE_METHOD_NOT_REACHABLE:"+",".join(missing))

        print(json.dumps({
            "status":"P18_NORMAL_DRAFT_CALLGRAPH_PASS",
            "reachable_methods":reachable,
            "self_edges":edges,
            "details":details,
            "external_class_definitions":definitions,
        },ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
