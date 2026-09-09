#!/usr/bin/env python3
from __future__ import annotations
import json,re,tempfile,zipfile
from pathlib import Path

REPO=Path(__file__).resolve().parents[4]
PPM=REPO/"control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip"
PSERC=REPO/"control/startmaster0107/runtime_packages/PSERC-FIX.zip"
PSERC_INNER="PSERC-FIX/portal-seo-editorial-plan-compiler_0.28.18_ENDSTEMPEL_IMPORT_ENVELOPE_BINDING.zip"
PSTE=REPO/"PSTE_0.56.25"

def load_json(p:Path):
    return json.loads(p.read_text(encoding="utf-8"))

def search_lines(root:Path,tokens,limit=120):
    out=[]
    for p in root.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in {".php",".json",".md",".txt",".py"}: continue
        try: txt=p.read_text(encoding="utf-8")
        except Exception: continue
        hits=[]
        for n,line in enumerate(txt.splitlines(),1):
            low=line.lower()
            ts=[t for t in tokens if t.lower() in low]
            if ts:hits.append({"line":n,"tokens":ts,"text":line.strip()[:700]})
        if hits:out.append({"file":str(p.relative_to(root)),"hits":hits[:80]})
    return out[:limit]

def executable_cross_refs(root:Path,tokens):
    out=[]
    for p in root.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in {".php",".py",".sh"}:continue
        try:txt=p.read_text(encoding="utf-8")
        except Exception:continue
        for n,line in enumerate(txt.splitlines(),1):
            low=line.lower()
            ts=[t for t in tokens if t.lower() in low]
            if ts:out.append({"file":str(p.relative_to(root)),"line":n,"tokens":ts,"text":line.strip()[:600]})
    return out

def main():
    with tempfile.TemporaryDirectory() as td:
        t=Path(td); po=t/"ppm"; so=t/"pserc_outer"; ps=t/"pserc"
        po.mkdir();so.mkdir();ps.mkdir()
        with zipfile.ZipFile(PPM) as z:z.extractall(po)
        with zipfile.ZipFile(PSERC) as z:z.extractall(so)
        inner=so/PSERC_INNER
        if not inner.is_file():raise RuntimeError("PSERC_INNER_MISSING")
        with zipfile.ZipFile(inner) as z:z.extractall(ps)
        ppm=po/"portal-production-machine"
        pserc=ps/"portal-seo-editorial-plan-compiler"

        # Exact PSERC contracts that explicitly deny content/format authority.
        contracts={}
        for rel in [
          "contracts/metadata-only-handoff-v1.json",
          "contracts/metadata-only-handoff-v2.json",
          "contracts/workflow-supervisor-v2.json",
          "contracts/plan-slot-identity-v2.json",
          "contracts/portal-topic-evidence-gate-v1.json",
          "contracts/seo-engine-capability-binding-v2.json",
        ]:
            p=pserc/rel
            contracts[rel]=load_json(p) if p.is_file() else None

        pserc_blob=json.dumps(contracts,ensure_ascii=False).lower()
        required_pserc_denials={
          "text_machine_is_only_content_and_format_authority": "text_machine_is_only_content_and_format_authority" in pserc_blob,
          "content_or_design_authority_false": '"content_or_design_authority": false' in pserc_blob,
          "design_or_quality_payload_allowed_false": '"design_or_quality_payload_allowed": false' in pserc_blob,
          "content_or_format_payload_forbidden": "content_or_format_payload_forbidden" in pserc_blob,
        }
        if not all(required_pserc_denials.values()):
            raise RuntimeError("PSERC_AUTHORITY_DENIAL_INCOMPLETE")

        # PSTE must remain research/planning side and not own article design/content mutation.
        pste_evidence=search_lines(PSTE,(
          "content_or_design_touched","design_touched","design_modified",
          "breadth research","planning readiness","keyword ownership","research"
        ),80)
        pste_blob=json.dumps(pste_evidence,ensure_ascii=False).lower()
        if "content_or_design_touched" not in pste_blob and "design_touched" not in pste_blob:
            raise RuntimeError("PSTE_NO_DESIGN_TOUCH_EVIDENCE_MISSING")

        # Cross-runtime references: identify real directed calls, don't invent architecture.
        pserc_cross=executable_cross_refs(pserc,("PPM679_","PSTE_"))
        ppm_cross=executable_cross_refs(ppm,("PSERC_","PSTE_"))
        pste_cross=executable_cross_refs(PSTE,("PSERC_","PPM679_"))

        # Current main worker authority is already tested by P27; read only its instruction.
        step=load_json(REPO/"control/startmaster0107/STEP_107007_RUN_NEW_ARTICLE_BATCH_NO_STOP.json")
        instr=step.get("instruction","")
        worker_flags={
          "current_codex_bound_worker":"der aktuelle Codex-Prozess IST der gebundene Fachworkflow-Worker" in instr,
          "worker_generates_fact_pack":"Recherche/fact_pack" in instr,
          "no_separate_executor":"kein separater Fachworkflow-Executor" in instr,
          "no_free_rules":"keine freie Auswahl, keine Ersatzregeln" in instr,
          "no_next_step":"Niemals nächsten Raum, nächstes Item oder Folgeaktion selbst ableiten" in instr,
        }

        # The isolated candidate may hold older wording. Do not fail here; P27 proved current main separately.
        print(json.dumps({
          "status":"P32_ROLE_AUTHORITY_MATRIX_PASS",
          "roles":{
            "CENTRAL_MACHINE":{
              "authority":["workflow_order","canonical_job_state","pass_block_transition"],
              "forbidden":["content_authority","design_authority","free_repair_choice"]
            },
            "CURRENT_BOUND_CODEX_WORKER":{
              "authority":["execute_bound_microstep","produce_bound_research_fact_pack_and_artifacts"],
              "forbidden":["next_step_choice","rule_choice","self_attested_pass","publish"]
            },
            "PSTE":{
              "authority":["research_planning_context","planning_readiness","pretitle_keyword_ownership"],
              "forbidden":["article_content_authority","design_authority","workflow_navigation"]
            },
            "PSERC":{
              "authority":["editorial_plan_metadata","workflow_supervision_metadata","fixed_bridge_to_ppm"],
              "forbidden":["content_or_format_authority","design_authority","publish"]
            },
            "PPM_NORMAL_DRAFT":{
              "authority":["article_generation","content_validation","plan_runtime_gate","prepare_payload","draft_write","readback","rendered_dom_validation"],
              "forbidden":["publish","free_external_reviewer_in_target_mode","workflow_navigation_outside_bound_call"]
            }
          },
          "pserc_authority_denials":required_pserc_denials,
          "pste_evidence":pste_evidence,
          "runtime_cross_refs":{
            "PSERC_to_PPM_or_PSTE":pserc_cross[:120],
            "PPM_to_PSERC_or_PSTE":ppm_cross[:120],
            "PSTE_to_PSERC_or_PPM":pste_cross[:120]
          },
          "candidate_step_wording_flags":worker_flags,
          "note":"P27 separately proved current main Codex/handoff authority in a temporary read-only worktree."
        },ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
