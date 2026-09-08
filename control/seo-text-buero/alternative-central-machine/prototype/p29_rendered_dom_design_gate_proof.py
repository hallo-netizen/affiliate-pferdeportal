#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,re,subprocess,tempfile,zipfile
from pathlib import Path

REPO=Path(__file__).resolve().parents[4]
PPM=REPO/"control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip"
PPM_SHA="acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1"

AI=("claude","anthropic","openai","chatgpt"," gpt","llm")
NETWORK=("api.anthropic","api.openai","wp_remote_post","wp_remote_get","curl_init","curl_exec","requests.post","urllib.request")

TESTS=(
 "tests/qf03-wordpress-draft-readback-dom/test-qf03-rendered-dom-positive.php",
 "tests/qf03-wordpress-draft-readback-dom/test-qf03-rendered-dom-mutations.php",
 "tests/test-mainblock1-rendered-table-dom-evidence.php",
)

def sha(p:Path):return hashlib.sha256(p.read_bytes()).hexdigest()

def scan(path:Path):
    txt=path.read_text(encoding="utf-8")
    hits=[]
    for n,line in enumerate(txt.splitlines(),1):
        low=" "+line.lower()
        ts=[x for x in AI+NETWORK if x in low]
        if ts:hits.append({"line":n,"tokens":ts,"text":line.strip()[:500]})
    return hits

def run_php(root:Path,rel:str):
    p=root/rel
    if not p.is_file():raise RuntimeError("TEST_MISSING:"+rel)
    proc=subprocess.run(["php",str(p)],cwd=root,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=180)
    if proc.returncode!=0:
        raise RuntimeError("TEST_FAILED:"+rel+"\n"+proc.stdout[-4000:])
    return {"test":rel,"status":"PASS","output_tail":proc.stdout[-2500:]}

def main():
    if not PPM.is_file() or sha(PPM)!=PPM_SHA:raise RuntimeError("PPM_IDENTITY_BLOCKED")
    with tempfile.TemporaryDirectory() as td:
        out=Path(td)/"ppm";out.mkdir()
        with zipfile.ZipFile(PPM) as z:z.extractall(out)
        root=out/"portal-production-machine"

        rv=root/"includes/rendered-dom-validator.php"
        tv=root/"includes/table-hard-rule-validator.php"
        if not rv.is_file():raise RuntimeError("RENDERED_DOM_VALIDATOR_MISSING")
        if not tv.is_file():raise RuntimeError("TABLE_HARD_RULE_VALIDATOR_MISSING")

        rv_hits=scan(rv); tv_hits=scan(tv)
        runtime_network=[x for x in rv_hits+tv_hits if any(t in x["tokens"] for t in NETWORK)]
        runtime_ai=[x for x in rv_hits+tv_hits if any(t in x["tokens"] for t in AI)]
        if runtime_network:raise RuntimeError("DESIGN_GATE_NETWORK_DEPENDENCY_FOUND")
        if runtime_ai:raise RuntimeError("DESIGN_GATE_AI_DEPENDENCY_FOUND")

        results=[run_php(root,x) for x in TESTS]

        registry=json.loads((root/"contracts/hard-rule-registry-v1.json").read_text(encoding="utf-8"))
        wanted={"HR-DOM-001","HR-DOM-002","HR-TABLE-001","HR-TABLE-002","HR-TABLE-003","HR-TABLE-004"}
        found={}
        for r in registry.get("rules",[]):
            if isinstance(r,dict) and r.get("rule_id") in wanted:
                found[r["rule_id"]]={
                    "title":r.get("title"),
                    "validator_or_reviewer":r.get("validator_or_reviewer"),
                    "required_evidence":r.get("required_evidence"),
                    "positive_test":r.get("positive_test"),
                    "negative_test":r.get("negative_test"),
                }
        if set(found)!=wanted:raise RuntimeError("DESIGN_HARD_RULE_SET_INCOMPLETE")

        print(json.dumps({
          "status":"P29_RENDERED_DOM_DESIGN_GATE_PASS",
          "ppm_sha256":PPM_SHA,
          "runtime_ai_dependency":False,
          "runtime_network_dependency":False,
          "hard_rules":found,
          "tests":results,
          "design_decision_mode":"DETERMINISTIC_FAIL_CLOSED_VALIDATORS",
          "free_visual_reviewer_required":False,
          "publish_allowed":False
        },ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
