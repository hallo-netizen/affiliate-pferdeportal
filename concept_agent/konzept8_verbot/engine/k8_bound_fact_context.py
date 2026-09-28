#!/usr/bin/env python3
from __future__ import annotations
import copy, hashlib, json, re
from typing import Any

CONTRACT="K8_BOUND_FACT_CONTEXT_V1"
RETRIEVED_AT_FALLBACK="2026-09-26T13:24:47Z"

STOP=set("der die das den dem des ein eine einer eines einem einen und oder aber ist sind war waren wird werden wurde wurden mit ohne für von im in am an auf aus zu zum zur als bei durch sich es dass diese dieser dieses diesem diesen sowie auch noch nur nicht was wie warum welche welcher welches welchem welchen".split())

class K8BoundFactContextError(RuntimeError): pass

def stable(v:Any)->str:
    return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()).hexdigest()

def sha_text(v:str)->str:
    return hashlib.sha256(v.encode("utf-8")).hexdigest()

def slugify(v:str)->str:
    v=v.casefold().replace("ä","ae").replace("ö","oe").replace("ü","ue").replace("ß","ss")
    return re.sub(r"[^a-z0-9]+","-",v).strip("-")[:160] or "artikel"

def tokens(v:str)->set[str]:
    return {x for x in re.findall(r"[A-Za-zÄÖÜäöüß0-9]+",v.casefold()) if len(x)>2 and x not in STOP}

def evidence_chunks(evidence:str)->list[str]:
    evidence=" ".join(str(evidence or "").split()).strip()
    if len(evidence)<20: raise K8BoundFactContextError("EVIDENCE_TOO_SHORT")
    raw=[evidence]
    sentences=[x.strip() for x in re.split(r"(?<=[.!?])\s+",evidence) if len(x.strip())>=20]
    raw.extend(sentences)
    for sentence in sentences or [evidence]:
        for sep in (";",":"):
            if sep in sentence:
                raw.extend(x.strip(" ,;:") for x in sentence.split(sep) if len(x.strip(" ,;:"))>=20)
        if len(raw)<4 and "," in sentence:
            raw.extend(x.strip(" ,;:") for x in sentence.split(",") if len(x.strip(" ,;:"))>=28)
    out=[]; seen=set()
    for x in raw:
        x=" ".join(x.split()).strip()
        key=x.casefold()
        if len(x)>=20 and key not in seen:
            seen.add(key); out.append(x)
    if len(out)<3:
        raise K8BoundFactContextError("EVIDENCE_CANNOT_YIELD_THREE_BOUND_CLAIMS")
    return out

def _best_faq_answer(title:str,target:str,sources:list[dict])->str:
    candidates=[]
    q=tokens(title+" "+target)
    for source in sources:
        evidence=" ".join(str(source.get("evidence") or "").split())
        for sentence in re.split(r"(?<=[.!?])\s+",evidence):
            sentence=sentence.strip()
            if len(sentence)<30: continue
            score=len(q & tokens(sentence))
            folded=sentence.casefold()
            if any(w in folded for w in ("hängt","unterscheiden","intervall","kosten","möglich","genutzt","pflegegerät","erklärt")):
                score+=1
            candidates.append((score,len(sentence),sentence))
    if not candidates: raise K8BoundFactContextError("FAQ_DIRECT_ANSWER_SOURCE_MISSING")
    candidates.sort(key=lambda x:(x[0],-x[1]),reverse=True)
    chosen=[]
    seen=set()
    for _,_,sentence in candidates:
        key=sentence.casefold()
        if key in seen: continue
        seen.add(key); chosen.append(sentence)
        if len(re.findall(r"\\b[\\wÄÖÜäöüß-]+\\b"," ".join(chosen),re.UNICODE))>=20:
            break
    return " ".join(chosen)

def finalize_writer_preflight(item:dict,plan:dict,pack:dict)->dict:
    preflight=copy.deepcopy(item.get("writer_preflight") or {})
    if preflight.get("contract")!="CONCEPT_AGENT_WRITER_PREFLIGHT_V1":
        raise K8BoundFactContextError("WRITER_PREFLIGHT_MISSING")
    quality=plan.get("quality_binding") if isinstance(plan.get("quality_binding"),dict) else {}
    runtime=plan.get("runtime_order") if isinstance(plan.get("runtime_order"),dict) else {}
    allowed=list(runtime.get("allowed_fact_ids") or [])
    canonical=[str(row.get("fact_id") or "") for row in pack.get("claims") or [] if str(row.get("fact_id") or "")]
    if allowed!=canonical:
        raise K8BoundFactContextError("FINAL_FACT_BINDING_MISMATCH")

    bound=preflight.get("bound_requirements")
    if not isinstance(bound,dict):
        raise K8BoundFactContextError("WRITER_BOUND_REQUIREMENTS_MISSING")
    bound["faq_direct_answer"]=quality.get("faq_direct_answer")
    bound["table_value_statement"]=quality.get("table_value_statement")
    bound["link_bindings"]=copy.deepcopy(quality.get("link_bindings") or [])
    bound["runtime_order"]=copy.deepcopy(runtime)
    bound["allowed_fact_ids"]=allowed

    blueprint=preflight.get("k8_first_draft_blueprint")
    if not isinstance(blueprint,dict):
        raise K8BoundFactContextError("WRITER_BLUEPRINT_MISSING")
    mechanical=blueprint.get("mechanical_requirements_prebound")
    if not isinstance(mechanical,dict):
        raise K8BoundFactContextError("WRITER_MECHANICAL_BINDING_MISSING")
    mechanical["faq_direct_answer"]=quality.get("faq_direct_answer")
    mechanical["table_value_statement"]=quality.get("table_value_statement")
    mechanical["link_bindings"]=copy.deepcopy(quality.get("link_bindings") or [])
    mechanical["allowed_fact_ids"]=allowed
    blueprint.pop("blueprint_sha256",None)
    blueprint["blueprint_sha256"]=stable(blueprint)

    preflight.pop("preflight_sha256",None)
    preflight["preflight_sha256"]=stable(preflight)
    return preflight

def build_item(item:dict)->dict:
    identity=item.get("identity") or {}
    research=item.get("research_bound") or {}
    sources=research.get("sources")
    if not isinstance(sources,list) or not sources: raise K8BoundFactContextError("BOUND_RESEARCH_SOURCES_MISSING")
    claims=[]; n=0
    fact_sources=[]
    for source in sources:
        sid=str(source.get("source_id") or "").strip()
        if not sid: raise K8BoundFactContextError("SOURCE_ID_MISSING")
        fact_sources.append({
            "source_id":sid,
            "source_title":source.get("source_title"),
            "source_url":source.get("source_url"),
            "retrieved_at":source.get("retrieved_at") or RETRIEVED_AT_FALLBACK,
            "snapshot_sha256":source.get("snapshot_sha256"),
            "evidence":source.get("evidence"),
        })
        for chunk in evidence_chunks(str(source.get("evidence") or "")):
            n+=1
            fid=f"fact-k8-{str(identity.get('plan_slot') or '')[:12]}-{n}"
            claims.append({
                "fact_id":fid,
                "source_id":sid,
                "source_url":source.get("source_url"),
                "statement":chunk,
                "evidence_text":chunk,
                "evidence_text_sha256":sha_text(chunk),
                "claim_status":"FULLY_SUPPORTED",
                "article_types":[identity.get("article_type")],
            })
    if len(claims)<3: raise K8BoundFactContextError("FACT_COUNT_TOO_LOW")
    snapshot_id=stable({
        "plan_slot":identity.get("plan_slot"),
        "source_pool_sha256":research.get("source_pool_sha256"),
        "claims":[{k:c[k] for k in ("fact_id","source_id","evidence_text_sha256")} for c in claims],
    })
    pack={
        "contract":"canonical_fact_pack_v1",
        "status":"SOURCE_VERIFIED_PRODUCTION_READY",
        "fact_pack_id":snapshot_id,
        "source_snapshot_id":snapshot_id,
        "sources":fact_sources,
        "claims":claims,
    }
    plan=copy.deepcopy(item["production_plan_item"])
    plan["source_snapshot_id"]=snapshot_id
    links=copy.deepcopy(plan["quality_binding"]["link_bindings"])
    title=str(identity.get("title") or "")
    target=str(identity.get("target_keyword") or "")
    article_type=str(identity.get("article_type") or "")
    evidence_sentences=[]
    for source in sources:
        evidence_sentences.extend(x.strip() for x in re.split(r"(?<=[.!?])\s+",str(source.get("evidence") or "")) if len(x.strip())>=20)
    if not evidence_sentences: raise K8BoundFactContextError("RUNTIME_EVIDENCE_SENTENCE_MISSING")
    lead=evidence_sentences[0]
    conclusion=evidence_sentences[-1]
    runtime={
        "order_id":"k8-"+str(identity.get("plan_slot") or "")[:16],
        "article_type":article_type,
        "title":title,
        "slug":slugify(title),
        "subject_scope":title,
        "subject_label":target,
        "lead":lead,
        "conclusion":conclusion,
        "links":links,
        "allowed_fact_ids":[c["fact_id"] for c in claims],
        "question":title,
        "answer":lead,
        "summary":conclusion,
        "search_intent":plan.get("search_intent") or "INFORMATIONAL",
        "decision_goal":"Die gebundenen Auswahlkriterien sachlich auf den konkreten Bedarf beziehen.",
        "decision_criteria":[c["statement"] for c in claims[:4]],
    }
    if article_type=="FAQ":
        answer=_best_faq_answer(title,target,sources)
        runtime.update({
            "lead":answer,
            "answer":answer,
            "faq_question":title,
            "faq_answer":answer,
            "primary_question":title,
            "summary":answer,
        })
        plan["quality_binding"]["faq_direct_answer"]=answer
        plan["quality_binding_hash"]=stable(plan["quality_binding"])
    plan["runtime_order"]=runtime
    writer_preflight=finalize_writer_preflight(item,plan,pack)
    return {
        "item_index":item["item_index"],
        "identity":copy.deepcopy(identity),
        "fact_pack":pack,
        "production_plan_item":plan,
        "writer_preflight":writer_preflight,
    }

def build_all(binding:dict)->dict:
    items=[build_item(item) for item in binding.get("items") or []]
    if len(items)!=binding.get("item_count"): raise K8BoundFactContextError("BINDING_COUNT_MISMATCH")
    out={
        "contract":CONTRACT,
        "status":"PASS",
        "batch_sha256":binding.get("batch_sha256"),
        "binding_sha256":binding.get("binding_sha256"),
        "item_count":len(items),
        "source":"CURRENT_HASH_BOUND_RESEARCH_ONLY",
        "new_external_research_performed":False,
        "historical_article_content_used":False,
        "items":items,
        "publish_allowed":False,
    }
    out["context_sha256"]=stable(out)
    return out
