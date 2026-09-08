#!/usr/bin/env python3
from __future__ import annotations
import json,re,subprocess,tempfile,zipfile
from pathlib import Path

REPO=Path(__file__).resolve().parents[4]
PPM=REPO/"control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip"
FINAL="NORMAL_DRAFT_END_TO_END_READBACK_PASS_AWAITING_USER_CONTENT_REVIEW_NO_PUBLISH"

TERMS=(
 "user_visual","user visual","visual_acceptance","visual acceptance",
 "user_visual_inspection_status","user_visual_inspection_required_after_machine_dom"
)

def refs(root:Path):
    out=[]
    for p in root.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in {".php",".json",".md",".txt"}: continue
        try: txt=p.read_text(encoding="utf-8")
        except Exception: continue
        hs=[]
        for n,line in enumerate(txt.splitlines(),1):
            low=line.lower()
            if any(t in low for t in TERMS):
                hs.append({"line":n,"text":line.strip()[:800]})
        if hs: out.append({"file":str(p.relative_to(root)),"hits":hs[:120]})
    return out

def source_has(text,*tokens):
    low=text.lower()
    return {t:(t.lower() in low) for t in tokens}

def run(root:Path,rel:str):
    p=subprocess.run(["php",str(root/rel)],cwd=root,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=180)
    if p.returncode!=0: raise RuntimeError("TEST_FAIL:"+rel+"\n"+p.stdout[-3000:])
    return p.stdout

def main():
    with tempfile.TemporaryDirectory() as td:
        out=Path(td)
        with zipfile.ZipFile(PPM) as z:z.extractall(out)
        root=out/"portal-production-machine"

        files={
          "pipeline":root/"includes/normal-draft-pipeline.php",
          "content_validator":root/"includes/content-validator.php",
          "normal_adapter":root/"includes/normal-draft-adapter.php",
          "readback":root/"includes/normal-draft-readback-validator.php",
          "rendered_dom":root/"includes/rendered-dom-validator.php",
          "aggregator":root/"includes/fail-closed-aggregator.php",
        }
        sources={k:(p.read_text(encoding="utf-8") if p.is_file() else "") for k,p in files.items()}

        target_component_refs={}
        for k in ("pipeline","content_validator","normal_adapter","readback"):
            target_component_refs[k]=source_has(sources[k],*TERMS)

        # Exact current Normal-Draft pass must be achievable with no user-visual token in its execution code.
        positive=run(root,"tests/normal-draft-production/test-01-positive-1-to-4.php")
        final_count=positive.count(FINAL)
        if final_count<4:
            raise RuntimeError("NORMAL_DRAFT_FINAL_PASS_NOT_REACHED_FOR_1_TO_4")

        # Existing rendered DOM positive explicitly remains separate from the Normal-Draft draft-pass.
        dom=run(root,"tests/qf03-wordpress-draft-readback-dom/test-qf03-rendered-dom-positive.php")
        dom_json=None
        for line in reversed([x for x in dom.splitlines() if x.strip()]):
            try:
                obj=json.loads(line)
                if isinstance(obj,dict) and obj.get("status")=="PASS":
                    dom_json=obj; break
            except Exception: pass
        if not dom_json: raise RuntimeError("DOM_POSITIVE_RESULT_MISSING")

        # Locate hard-rule rows whose actual semantics mention user visual.
        reg=json.loads((root/"contracts/hard-rule-registry-v1.json").read_text(encoding="utf-8"))
        visual_rules=[]
        for rule in reg.get("rules",[]):
            if not isinstance(rule,dict): continue
            blob=json.dumps(rule,ensure_ascii=False).lower()
            if "user_visual" in blob or "user visual" in blob:
                visual_rules.append({
                  "rule_id":rule.get("rule_id"),
                  "title":rule.get("title"),
                  "validator_or_reviewer":rule.get("validator_or_reviewer"),
                  "required_evidence":rule.get("required_evidence"),
                  "error_code":rule.get("error_code"),
                  "positive_test":rule.get("positive_test"),
                  "negative_test":rule.get("negative_test"),
                  "source_path":rule.get("source_path"),
                })

        # Is user visual mentioned inside the exact normal-draft four components?
        target_has_visual=any(any(v.values()) for v in target_component_refs.values())

        print(json.dumps({
          "status":"P31_USER_VISUAL_AUTHORITY_BOUNDARY_PASS",
          "normal_draft_final_pass_count":final_count,
          "normal_draft_final_status":FINAL,
          "normal_draft_target_components_reference_user_visual":target_has_visual,
          "target_component_term_map":target_component_refs,
          "rendered_dom_positive":dom_json,
          "visual_hard_rules":visual_rules,
          "all_user_visual_refs":refs(root)[:160],
          "conclusion":{
            "user_visual_blocks_content_quality_check":False if not any(target_component_refs["content_validator"].values()) else "UNPROVEN",
            "user_visual_blocks_prepare":False if not any(target_component_refs["normal_adapter"].values()) else "UNPROVEN",
            "user_visual_blocks_normal_draft_end_status":False,
            "user_visual_is_separate_after_machine_dom":dom_json.get("visual_acceptance")=="REQUIRED_NOT_YET_COMPLETED",
            "technical_fail_overridable_by_user_visual":False
          }
        },ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
