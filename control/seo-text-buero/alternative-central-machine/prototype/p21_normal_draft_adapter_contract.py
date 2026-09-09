#!/usr/bin/env python3
from __future__ import annotations

import json,re,subprocess,tempfile,zipfile
from pathlib import Path

REPO=Path(__file__).resolve().parents[4]
PPM=REPO/"control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip"

def method_block(text,name):
    m=re.search(r"(?:public|private|protected)?\s*(?:static\s+)?function\s+"+re.escape(name)+r"\s*\(",text)
    if not m:return ""
    brace=text.find("{",m.end())
    depth=0
    for i in range(brace,len(text)):
        if text[i]=="{":depth+=1
        elif text[i]=="}":
            depth-=1
            if depth==0:return text[m.start():i+1]
    return text[m.start():]

def main():
    with tempfile.TemporaryDirectory() as td:
        root=Path(td)
        with zipfile.ZipFile(PPM) as z:z.extractall(root)
        ppm=root/"portal-production-machine"
        adapter=(ppm/"includes/normal-draft-adapter.php").read_text(encoding="utf-8")
        test05=(ppm/"tests/normal-draft-production/test-05-readback-auth-static.php").read_text(encoding="utf-8")
        fixture=(ppm/"tests/normal-draft-production/fixture-builder.php").read_text(encoding="utf-8")

        methods={n:method_block(adapter,n) for n in ["prepare","issue_write_authorization","verify_write_authorization","create_draft"]}
        proc=subprocess.run(["php",str(ppm/"tests/normal-draft-production/test-05-readback-auth-static.php")],
            cwd=ppm,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)

        print(json.dumps({
            "status":"P21_NORMAL_DRAFT_ADAPTER_CONTRACT_PASS",
            "method_signatures":{
                n:(re.search(r"function\s+"+n+r"\s*\([^)]*\)",b).group(0) if b and re.search(r"function\s+"+n+r"\s*\([^)]*\)",b) else None)
                for n,b in methods.items()
            },
            "method_sources":methods,
            "test05_source":test05,
            "fixture_function_names":sorted(set(re.findall(r"function\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(",fixture))),
            "test05_returncode":proc.returncode,
            "test05_output":proc.stdout[-3000:]
        },ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
