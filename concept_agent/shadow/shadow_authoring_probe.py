#!/usr/bin/env python3
from __future__ import annotations
import copy, hashlib, json, os, re, sys
from pathlib import Path

REPO=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(REPO/"concept_agent"))
sys.path.insert(0,str(REPO/"isolated_system4"))
import intake_bridge as intake
import production_checks_engine as checks

TITLE="Hindernisstangen sicher aufbauen und vor dem Training prüfen"
KEYWORD="Hindernisstangen sicher aufbauen"
CATEGORY="hindernisstangen-beratung"
ARTICLE_TYPE="Beratung"
SLOT=hashlib.sha256(b"CONCEPT_AGENT_SHADOW_HINDERNISSTANGEN_001").hexdigest()
OUT=Path(os.environ.get("CONCEPT_AGENT_SHADOW_OUTPUT","/tmp/concept-agent-shadow-output"))

def stable(v):
    return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()).hexdigest()

def writej(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")

def section_words(html,name):
    m=re.search(r'<section data-block="'+re.escape(name)+r'">([\s\S]*?)</section>',html)
    if not m:
        raise RuntimeError("SHADOW_SECTION_MISSING:"+name)
    text=re.sub(r'<[^>]+>',' ',m.group(1))
    text=' '.join(text.split())
    return len(text.split()),text

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    article=(REPO/"concept_agent/shadow/SHADOW_HINDERNISSTANGEN_001.html").read_text(encoding="utf-8").strip()
    real7=json.loads((REPO/"concept_agent/production_ready/REAL7_CHATGPT_RUN_001.json").read_text(encoding="utf-8"))
    env=real7["import_envelope"]
    fps=env["fact_pack_bundle"]["fact_packs"]
    fact_pack=next(fp for fp in fps if any(c.get("fact_id")=="HIND_F1" for c in fp.get("claims",[])))
    plans=env["production_plan"]["items"]
    source_plan=next(p for p in plans if p.get("target_keyword")=="Hindernisstangen für Pferde")
    old_body=source_plan["canonical_article"]["body_html"]

    item={"title":TITLE,"target_keyword":KEYWORD,"category":CATEGORY,"article_type":ARTICLE_TYPE,"plan_slot":SLOT}
    batch={
        "contract":intake.BATCH_CONTRACT,
        "status":intake.READY_STATUS,
        "item_count":1,
        "maximum_articles":0,
        "maximum_articles_per_type":0,
        "publish_allowed":False,
        "content_or_format_payload_present":False,
        "items":[item],
    }
    batch["batch_sha256"]=stable(batch)
    snapshot={
        "contract":intake.SNAPSHOT_CONTRACT,
        "hard_rules":{
            "approved_research_text_process_required":True,
            "text_machine_is_only_content_and_format_authority":True,
            "metadata_handoff_exact_scalar_fields":list(intake.EXACT_FIELDS),
        },
        "next_step":intake.NEXT_STEP,
        "next_textmachine_metadata_batch":batch,
    }
    intake_req=intake.prepare(snapshot)
    research_submission={
        "contract":intake.RESEARCH_SUBMISSION_CONTRACT,
        "batch_sha256":batch["batch_sha256"],
        "item_count":1,
        "items":[{
            "item_index":0,
            "plan_slot":SLOT,
            "sources":[{
                "source_id":s["source_id"],
                "source_title":s["source_title"],
                "source_url":s["source_url"],
                "evidence":s["evidence"],
                "snapshot_sha256":s["snapshot_sha256"],
            } for s in fact_pack["sources"]],
        }],
    }
    research_bound=intake.bind_research(intake_req,research_submission)

    plan=copy.deepcopy(source_plan)
    plan["topic"]=TITLE
    plan["target_keyword"]=KEYWORD
    plan["canonical_article"]={"title":TITLE,"article_type":ARTICLE_TYPE,"slug":"hindernisstangen-sicher-aufbauen"}
    quality=plan["quality_binding"]
    quality["intent_terms"]=[KEYWORD,"Hindernisstangen","Reitplatz Training","Training"]
    quality["table_value_statement"]="Die Tabelle bündelt die wichtigsten Prüfpunkte für einen sicheren Aufbau von Hindernisstangen und macht sichtbar, was vor dem ersten Durchreiten kontrolliert werden sollte."
    quality["language_evidence"]={}
    plan["quality_binding_hash"]=checks.stable_hash(quality)
    runtime=plan["runtime_order"]
    runtime.update({
        "order_id":"shadow-hind-001",
        "title":TITLE,
        "slug":"hindernisstangen-sicher-aufbauen",
        "subject_scope":TITLE,
        "subject_label":KEYWORD,
        "lead":TITLE,
        "conclusion":TITLE,
        "question":TITLE,
        "answer":TITLE,
        "faq_question":TITLE,
        "faq_answer":TITLE,
        "summary":TITLE,
        "article_type":ARTICLE_TYPE,
    })

    required_sections=["intro","criteria","decision","table","conclusion","further_information"]
    profile={name:section_words(article,name)[0] for name in required_sections}
    if not (95 <= profile["conclusion"] <= 135):
        raise RuntimeError("SHADOW_CONCLUSION_PROFILE_OUTSIDE_REAL7:"+str(profile["conclusion"]))
    if not (55 <= profile["further_information"] <= 85):
        raise RuntimeError("SHADOW_FURTHER_INFO_PROFILE_OUTSIDE_REAL7:"+str(profile["further_information"]))
    if profile["conclusion"] <= profile["further_information"]:
        raise RuntimeError("SHADOW_SECTION_WEIGHTING_INVALID")
    if checks.text_sha256(article)==checks.text_sha256(old_body):
        raise RuntimeError("SHADOW_REUSED_REAL7_BODY_FORBIDDEN")

    try:
        lt=checks.run_languagetool(REPO,article)
    except checks.RepairRequired as exc:
        failure={"contract":"CONCEPT_AGENT_SHADOW_AUTHORING_FAILURE_V1","stage":exc.checker,"findings":exc.findings,"publish_allowed":False}
        writej(OUT/"SHADOW_FAILURE.json",failure)
        print(json.dumps(failure,ensure_ascii=False,indent=2,sort_keys=True))
        raise
    try:
        ppm=checks.run_ppm_content_validator(REPO,article,fact_pack,plan,lt)
    except checks.RepairRequired as exc:
        failure={"contract":"CONCEPT_AGENT_SHADOW_AUTHORING_FAILURE_V1","stage":exc.checker,"findings":exc.findings,"publish_allowed":False}
        writej(OUT/"SHADOW_FAILURE.json",failure)
        print(json.dumps(failure,ensure_ascii=False,indent=2,sort_keys=True))
        raise
    links=checks.no_external_links(article)

    proof={
        "contract":"CONCEPT_AGENT_SHADOW_AUTHORING_PROOF_V1",
        "status":"PASS",
        "title":TITLE,
        "target_keyword":KEYWORD,
        "plan_slot":SLOT,
        "batch_sha256":batch["batch_sha256"],
        "intake_sha256":intake_req["intake_sha256"],
        "research_binding_sha256":research_bound["research_binding_sha256"],
        "research_source_ids":[s["source_id"] for s in fact_pack["sources"]],
        "article_sha256":checks.text_sha256(article),
        "article_bytes":len(article.encode("utf-8")),
        "section_words":profile,
        "old_real7_body_reused":False,
        "languagetool":{k:v for k,v in lt.items() if not k.startswith("_")},
        "ppm679":ppm,
        "internal_links":links,
        "redaktionsplan_mutated":False,
        "production_runtime_mutated":False,
        "wordpress_write_performed":False,
        "publish_allowed":False,
        "endstempel_invoked":False,
        "endstempel_reason":"SHADOW_RUN_NOT_A_PRODUCTION_RELEASE",
    }
    (OUT/"SHADOW_HINDERNISSTANGEN_001.html").write_text(article+"\n",encoding="utf-8")
    writej(OUT/"CONCEPT_AGENT_INTAKE.json",intake_req)
    writej(OUT/"CONCEPT_AGENT_RESEARCH_BOUND.json",research_bound)
    writej(OUT/"SHADOW_PRODUCTION_PLAN.json",plan)
    writej(OUT/"SHADOW_FACT_PACK.json",fact_pack)
    writej(OUT/"SHADOW_PROOF.json",proof)
    print(json.dumps(proof,ensure_ascii=False,indent=2,sort_keys=True))
    return 0

if __name__=="__main__":
    raise SystemExit(main())

# diagnostic rerun marker
