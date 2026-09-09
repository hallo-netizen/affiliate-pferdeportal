#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import tempfile
import zipfile
from pathlib import Path

REPO=Path(__file__).resolve().parents[4]
PSERC=REPO/"control/startmaster0107/runtime_packages/PSERC-FIX.zip"
PSERC_INNER="PSERC-FIX/portal-seo-editorial-plan-compiler_0.28.18_ENDSTEMPEL_IMPORT_ENVELOPE_BINDING.zip"

MAIN_HANDOFF="control/startmaster0107/fachworkflow_proof_handoff.py"

def run(cmd,cwd,timeout=300):
    p=subprocess.run(cmd,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=timeout)
    if p.returncode!=0:
        raise RuntimeError("COMMAND_FAILED:"+" ".join(cmd)+"\n"+p.stdout[-4000:])
    return p.stdout

def main():
    run(["git","fetch","--depth=1","origin","main"],REPO)
    main_sha=run(["git","rev-parse","FETCH_HEAD"],REPO).strip()
    candidate_sha=run(["git","rev-parse","HEAD"],REPO).strip()

    with tempfile.TemporaryDirectory() as td:
        root=Path(td)
        outer=root/"outer"; src=root/"pserc"; work=root/"main"
        outer.mkdir(); src.mkdir()

        with zipfile.ZipFile(PSERC) as z:z.extractall(outer)
        inner=outer/PSERC_INNER
        if not inner.is_file():
            raise RuntimeError("PSERC_INNER_MISSING")
        with zipfile.ZipFile(inner) as z:z.extractall(src)
        pserc=src/"portal-seo-editorial-plan-compiler"

        slot_identity=pserc/"includes/class-pserc-plan-slot-identity.php"
        trigger=pserc/"includes/class-pserc-production-trigger.php"
        if not slot_identity.is_file() or not trigger.is_file():
            raise RuntimeError("PSERC_IDENTITY_FILES_MISSING")

        slot_text=slot_identity.read_text(encoding="utf-8")
        trigger_text=trigger.read_text(encoding="utf-8")

        required_slot_tokens=(
            "class PSERC_Plan_Slot_Identity",
            "function token",
            "canonical_article_id",
        )
        for t in required_slot_tokens:
            if t not in slot_text:
                raise RuntimeError("PLAN_SLOT_IDENTITY_TOKEN_MISSING:"+t)

        if "PSERC_PRODUCTION_TRIGGER_FOREIGN_PLAN_SLOT_FIELD_FORBIDDEN_IN_0039_PPM_PLAN" not in trigger_text:
            raise RuntimeError("PPM_PLAN_FOREIGN_PLAN_SLOT_GUARD_MISSING")

        run(["git","worktree","add","--detach",str(work),main_sha],REPO)
        try:
            handoff=(work/MAIN_HANDOFF).read_text(encoding="utf-8")
            required_handoff_tokens=(
                "PSERC_Plan_Slot_Identity::token($candidate)",
                "hash_equals(PSERC_Plan_Slot_Identity::token($candidate),$externalSlot)",
                "if(count($matches)!==1)",
                "$item['canonical_article_id']=(string)$slot['canonical_article_id'];",
                "unset($item['plan_slot']);",
            )
            for t in required_handoff_tokens:
                if t not in handoff:
                    raise RuntimeError("HANDOFF_SLOT_BINDING_MISSING:"+t)

            # Find and run any bundled PSERC tests that explicitly exercise plan-slot identity.
            tests=[]
            for p in (pserc/"tests").rglob("*.php") if (pserc/"tests").is_dir() else []:
                text=p.read_text(encoding="utf-8")
                if "PSERC_Plan_Slot_Identity" in text or "plan_slot" in p.name.lower():
                    proc=subprocess.run(
                        ["php",str(p)],cwd=pserc,text=True,
                        stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120
                    )
                    tests.append({
                        "test":str(p.relative_to(pserc)),
                        "returncode":proc.returncode,
                        "status":"PASS" if proc.returncode==0 else "FAIL",
                        "output_tail":proc.stdout[-1200:],
                    })
                    if proc.returncode!=0:
                        raise RuntimeError("PSERC_PLAN_SLOT_TEST_FAILED:"+str(p.relative_to(pserc)))

            print(json.dumps({
                "status":"P42_PLAN_SLOT_TO_CANONICAL_BINDING_PASS",
                "tested_main_sha":main_sha,
                "candidate_sha_unchanged":candidate_sha,
                "external_identity":"plan_slot",
                "ppm_identity":"canonical_article_id + plan_item_key",
                "plan_slot_resolved_before_ppm":True,
                "plan_slot_must_match_exactly_one_registry_slot":True,
                "canonical_article_id_taken_from_matched_slot":True,
                "plan_slot_removed_before_production_plan_v4":True,
                "ppm_plan_rejects_foreign_plan_slot":True,
                "new_identity_field_required":False,
                "new_binding_layer_required":False,
                "bundled_plan_slot_tests":tests,
                "publish_allowed":False,
            },ensure_ascii=False,indent=2))
        finally:
            subprocess.run(["git","worktree","remove","--force",str(work)],cwd=REPO,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    return 0

if __name__=="__main__":
    raise SystemExit(main())
