#!/usr/bin/env python3
from __future__ import annotations

import json, tempfile, zipfile
from pathlib import Path
from typing import Any

REPO=Path(__file__).resolve().parents[4]
PPM=REPO/"control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip"

FILES=[
    "contracts/hard-rule-registry-v1.json",
    "contracts/hard-rule-coverage-matrix-v1.json",
    "contracts/content-structure-language-gate-v2.json",
    "contracts/content-validation-contract-v2.json",
    "contracts/article-type-templates.json",
    "contracts/normal-draft-release-v1.json",
    "contracts/system-inventory-v3-1.json",
]

TOKENS={
    "table":["table","tabelle"],
    "link":["link","internal_link","external_link"],
    "languagetool":["languagetool","language_tool","language tool"],
    "duplicate_cannibalization":["duplicate","cannibal"],
    "seo":["seo","target_keyword","keyword"],
    "design_format":["design","format"],
    "publish_safety":["publish_allowed","no_publish","publish"],
    "article_type_structure":["article_type","template","structure"],
}

def walk(value:Any,path="$"):
    if isinstance(value,dict):
        for k,v in value.items():
            yield from walk(v,f"{path}.{k}")
    elif isinstance(value,list):
        for i,v in enumerate(value):
            yield from walk(v,f"{path}[{i}]")
    else:
        yield path,value

def main():
    with tempfile.TemporaryDirectory() as td:
        root=Path(td)
        with zipfile.ZipFile(PPM) as z:
            z.extractall(root)
        ppm=root/"portal-production-machine"

        report={}
        for rel in FILES:
            p=ppm/rel
            if not p.is_file():
                report[rel]={"status":"MISSING"}
                continue
            data=json.loads(p.read_text(encoding="utf-8"))
            flat=list(walk(data))
            matches={}
            for gate,tokens in TOKENS.items():
                rows=[]
                for jp,val in flat:
                    s=(jp+" "+str(val)).lower()
                    if any(tok in s for tok in tokens):
                        rows.append({"path":jp,"value":val})
                matches[gate]=rows[:40]
            report[rel]={
                "status":"FOUND",
                "top_level_keys":sorted(data.keys()) if isinstance(data,dict) else [],
                "matches":matches,
            }

        print(json.dumps({
            "status":"P13_RULE_REGISTRY_EXTRACT_PASS",
            "files":report,
        },ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
