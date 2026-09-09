#!/usr/bin/env python3
from __future__ import annotations
import json,re,tempfile,zipfile
from pathlib import Path

REPO=Path(__file__).resolve().parents[4]
PPM=REPO/"control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip"

TERMS=(
 "visual_acceptance","capture_request","capture_executed","visual review",
 "visual_review","user_visual","screenshot","browser","playwright","chromium",
 "puppeteer","capture"
)
FREEDOM=("claude","anthropic","openai","chatgpt","gpt","llm","human","manual","reviewer","user visual","user_visual")
NETWORK=("wp_remote_post","wp_remote_get","curl_init","curl_exec","requests.post","httpx","urllib.request","api.")

def scan(root:Path):
    rows=[]
    for p in root.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in {".php",".json",".md",".txt",".py",".sh",".js"}:
            continue
        try: txt=p.read_text(encoding="utf-8")
        except Exception: continue
        hits=[]
        for n,line in enumerate(txt.splitlines(),1):
            low=line.lower()
            ts=[t for t in TERMS if t in low]
            if ts:
                hits.append({
                    "line":n,
                    "terms":ts,
                    "freedom_tokens":[x for x in FREEDOM if x in low],
                    "network_tokens":[x for x in NETWORK if x in low],
                    "text":line.strip()[:750]
                })
        if hits:
            rows.append({"file":str(p.relative_to(root)),"hits":hits[:120]})
    return rows

def main():
    with tempfile.TemporaryDirectory() as td:
        out=Path(td)
        with zipfile.ZipFile(PPM) as z:z.extractall(out)
        root=out/"portal-production-machine"
        rows=scan(root)

        critical=[]
        for row in rows:
            for h in row["hits"]:
                blob=(h["text"]+" "+" ".join(h["terms"])).lower()
                if "visual_acceptance" in blob or "capture_request" in blob or "capture_executed" in blob or "user_visual" in blob:
                    critical.append({"file":row["file"],**h})

        print(json.dumps({
          "status":"P30_VISUAL_ACCEPTANCE_AUDIT_PASS",
          "critical_hits":critical,
          "all_matching_files":rows[:200]
        },ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
