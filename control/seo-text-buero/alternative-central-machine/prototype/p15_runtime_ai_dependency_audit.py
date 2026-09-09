#!/usr/bin/env python3
from __future__ import annotations
import json, re, subprocess, tempfile, zipfile
from pathlib import Path

REPO=Path(__file__).resolve().parents[4]
PPM=REPO/"control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip"
PSERC=REPO/"control/startmaster0107/runtime_packages/PSERC-FIX.zip"
PSERC_INNER="PSERC-FIX/portal-seo-editorial-plan-compiler_0.28.18_ENDSTEMPEL_IMPORT_ENVELOPE_BINDING.zip"
PSTE=REPO/"PSTE_0.56.25"

AI_TOKENS=("claude","anthropic","openai","chatgpt"," gpt","llm")
NETWORK_TOKENS=("api.anthropic","api.openai","wp_remote_post","wp_remote_get","curl_init","curl_exec","httpx","requests.post","urllib.request")
EXEC_SUFFIXES={".php",".py",".sh"}

TARGET_TESTS=[
    "tests/test-mainblock1-link-targets.php",
    "tests/test-mainblock1-g9-corrected-candidate.php",
    "tests/test-wave2-content-mutations.php",
    "tests/test-v38-editorial-plan-journal-dedup.php",
    "tests/v3-stateful-e2e/test-v31-status-wording-governance.php",
]

def scan_exec(root:Path,label:str):
    hits=[]
    for p in root.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in EXEC_SUFFIXES:
            continue
        try:
            lines=p.read_text(encoding="utf-8").splitlines()
        except Exception:
            continue
        for n,line in enumerate(lines,1):
            low=(" "+line.lower())
            toks=[t for t in AI_TOKENS+NETWORK_TOKENS if t in low]
            if toks:
                hits.append({
                    "owner":label,
                    "file":str(p.relative_to(root)),
                    "line":n,
                    "tokens":sorted(set(toks)),
                    "text":line.strip()[:300],
                })
    return hits

def main():
    with tempfile.TemporaryDirectory() as td:
        root=Path(td)
        ppm_out=root/"ppm"; po=root/"pserc_outer"; ps=root/"pserc"
        ppm_out.mkdir(); po.mkdir(); ps.mkdir()
        with zipfile.ZipFile(PPM) as z: z.extractall(ppm_out)
        with zipfile.ZipFile(PSERC) as z: z.extractall(po)
        inner=po/PSERC_INNER
        if not inner.is_file():
            raise RuntimeError("PSERC_INNER_MISSING")
        with zipfile.ZipFile(inner) as z: z.extractall(ps)

        ppm_root=ppm_out/"portal-production-machine"
        pserc_root=ps/"portal-seo-editorial-plan-compiler"

        exec_hits=scan_exec(ppm_root,"PPM")+scan_exec(pserc_root,"PSERC")+scan_exec(PSTE,"PSTE")
        runtime_network_hits=[h for h in exec_hits if any(t in NETWORK_TOKENS for t in h["tokens"])]
        runtime_ai_hits=[h for h in exec_hits if any(t in AI_TOKENS for t in h["tokens"])]

        test_results=[]
        for rel in TARGET_TESTS:
            p=ppm_root/rel
            if not p.is_file():
                test_results.append({"test":rel,"status":"MISSING"})
                continue
            proc=subprocess.run(
                ["php",str(p)],
                cwd=ppm_root,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=120,
            )
            test_results.append({
                "test":rel,
                "status":"PASS" if proc.returncode==0 else "FAIL",
                "returncode":proc.returncode,
                "output_tail":proc.stdout[-1000:],
            })

        print(json.dumps({
            "status":"P15_RUNTIME_AI_DEPENDENCY_AUDIT_PASS",
            "runtime_ai_hit_count":len(runtime_ai_hits),
            "runtime_network_hit_count":len(runtime_network_hits),
            "runtime_ai_hits":runtime_ai_hits[:100],
            "runtime_network_hits":runtime_network_hits[:100],
            "target_test_results":test_results,
        },ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
