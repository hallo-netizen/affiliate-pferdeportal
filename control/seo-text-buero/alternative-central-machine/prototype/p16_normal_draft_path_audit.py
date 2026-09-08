#!/usr/bin/env python3
from __future__ import annotations
import json,re,subprocess,tempfile,zipfile
from pathlib import Path

REPO=Path(__file__).resolve().parents[4]
PPM=REPO/"control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip"
AI=("claude","anthropic","openai","chatgpt","llm")
FINAL="NORMAL_DRAFT_END_TO_END_READBACK_PASS_AWAITING_USER_CONTENT_REVIEW_NO_PUBLISH"

def lines_with(text,tokens):
    out=[]
    for i,line in enumerate(text.splitlines(),1):
        low=line.lower()
        if any(t in low for t in tokens):
            out.append({"line":i,"text":line.strip()[:400]})
    return out

def function_block(text,name):
    m=re.search(r"function\s+"+re.escape(name)+r"\s*\(",text)
    if not m:
        return ""
    start=m.start()
    nxt=re.search(r"\n\s*(?:public|private|protected)?\s*(?:static\s+)?function\s+[A-Za-z_]",text[m.end():])
    end=len(text) if not nxt else m.end()+nxt.start()
    return text[start:end]

def class_block(text,name):
    m=re.search(r"class\s+"+re.escape(name)+r"\b",text)
    if not m:
        return ""
    start=m.start()
    nxt=re.search(r"\nclass\s+PPM679_[A-Za-z0-9_]+\b",text[m.end():])
    end=len(text) if not nxt else m.end()+nxt.start()
    return text[start:end]

def main():
    with tempfile.TemporaryDirectory() as td:
        root=Path(td)
        with zipfile.ZipFile(PPM) as z:z.extractall(root)
        ppm=root/"portal-production-machine"
        nd=ppm/"tests/normal-draft-production"
        fixture=(nd/"fixture-builder.php").read_text(encoding="utf-8")
        positive=(nd/"test-01-positive-1-to-4.php").read_text(encoding="utf-8")
        admin=(ppm/"includes/admin.php").read_text(encoding="utf-8")
        pipeline=class_block(admin,"PPM679_Normal_Draft_Pipeline")

        normal_file_hits={}
        for p in sorted(nd.rglob("*.php")):
            txt=p.read_text(encoding="utf-8")
            hits=lines_with(txt,AI)
            if hits: normal_file_hits[str(p.relative_to(ppm))]=hits

        pipeline_ai=lines_with(pipeline,AI)
        language=function_block(fixture,"nd_language_evidence")
        quality=function_block(fixture,"nd_quality_binding")
        called=sorted(set(re.findall(r"(PPM679_[A-Za-z0-9_]+)::([A-Za-z0-9_]+)\s*\(",pipeline)))

        call_files=[]
        for cls,method in called:
            found=[]
            for p in (ppm/"includes").rglob("*.php"):
                txt=p.read_text(encoding="utf-8")
                if re.search(r"class\s+"+re.escape(cls)+r"\b",txt):
                    found.append({
                        "file":str(p.relative_to(ppm)),
                        "ai_hits":lines_with(txt,AI)[:30],
                    })
            call_files.append({"class":cls,"method":method,"definitions":found})

        proc=subprocess.run(
            ["php",str(nd/"test-01-positive-1-to-4.php")],
            cwd=ppm,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120
        )
        out=proc.stdout
        print(json.dumps({
            "status":"P16_NORMAL_DRAFT_PATH_AUDIT_PASS",
            "normal_draft_files_ai_hits":normal_file_hits,
            "pipeline_ai_hits":pipeline_ai,
            "nd_language_evidence_ai_hits":lines_with(language,AI),
            "nd_quality_binding_ai_hits":lines_with(quality,AI),
            "pipeline_called_components":call_files,
            "positive_test_returncode":proc.returncode,
            "positive_test_final_status_present":FINAL in out,
            "positive_test_output_tail":out[-1200:],
        },ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
