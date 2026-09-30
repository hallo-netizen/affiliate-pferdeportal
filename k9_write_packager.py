#!/usr/bin/env python3
import argparse, hashlib, html as htmlmod, json, re, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parent
JOB=ROOT/"runtime"/"CURRENT_JOB.json"
ENTRY=ROOT/"runtime"/"CHAT_ENTRY.json"
RULES=ROOT/"contracts"/"K9_WRITING_RULES.json"
PORTAL_SNAPSHOT_SHA256="b86a160e6b8cf720077830422ca6b574203ce171fdc65d357fe9c6bed039c2e0"
LINK_REASON_BY_ROLE={
    "parent_category":"Maschinell gebundener Portal-Hauptbereich",
    "semantic_related":"Maschinell gebundener Portal-Bereich",
    "further_information":"Maschinell gebundene Portal-Produktseite",
}

class PackError(RuntimeError): pass

def stable(obj):
    return hashlib.sha256(json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")).hexdigest()

def load(path):
    try: data=json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception as exc: raise PackError("JSON_INVALID:"+str(path)) from exc
    if not isinstance(data,dict): raise PackError("JSON_OBJECT_REQUIRED:"+str(path))
    return data

def text_of(markup):
    value=re.sub(r"(?is)<(script|style)\b[^>]*>.*?</\1>"," ",markup)
    value=re.sub(r"(?s)<[^>]+>"," ",value)
    value=htmlmod.unescape(value)
    return re.sub(r"\s+"," ",value).strip()

def word_count(markup):
    return len(re.findall(r"\b[\wÄÖÜäöüß-]+\b",text_of(markup)))

def _trace_fact_ids(markup):
    out=[]
    for tag in re.findall(r'<span\b[^>]*class=["\'][^"\']*\bppm-source-trace\b[^"\']*["\'][^>]*>',markup,re.I):
        m=re.search(r'\bdata-fact-id=["\']([^"\']+)["\']',tag,re.I)
        if m:
            out.append(m.group(1))
    return out

def ensure_all_fact_traces(markup, research):
    fact_pack=research.get("fact_pack",{})
    fact_ids=[str(x) for x in fact_pack.get("fact_ids",[]) if str(x)]
    claims={str(x.get("fact_id") or ""):x for x in fact_pack.get("claims",[]) if isinstance(x,dict)}
    existing=set(_trace_fact_ids(markup))
    for fid in fact_ids:
        if fid in existing:
            continue
        claim=claims.get(fid)
        if not claim:
            raise PackError("PPM_SOURCE_TRACE_FACT_UNKNOWN:"+fid)
        source_hash=str(claim.get("evidence_text_sha256") or "")
        source_title=str(claim.get("source_id") or "")
        if not source_hash or not source_title:
            raise PackError("PPM_SOURCE_TRACE_BINDING_MISSING:"+fid)
        statement_tokens=set(re.findall(r"[a-z0-9äöüß]+",str(claim.get("statement") or "").casefold()))
        candidates=[]
        for m in re.finditer(r"<p\b[^>]*>.*?</p>",markup,re.I|re.S):
            segment=m.group(0)
            opener=re.match(r"<p\b[^>]*>",segment,re.I)
            if not opener:
                continue
            attr=re.search(r'\bdata-fact-ids=["\']([^"\']+)["\']',opener.group(0),re.I)
            if not attr or fid not in attr.group(1).split():
                continue
            visible_tokens=set(re.findall(r"[a-z0-9äöüß]+",text_of(segment).casefold()))
            candidates.append((len(statement_tokens & visible_tokens),m.start(),m.end(),opener.end(),segment))
        if not candidates:
            raise PackError("PPM_SOURCE_TRACE_TARGET_MISSING:"+fid)
        candidates.sort(key=lambda x:(-x[0],x[1]))
        _,start,end,insert_at,segment=candidates[0]
        trace=(f'<span class="ppm-source-trace" data-fact-id="{fid}" '
               f'data-source-hash="{source_hash}" data-source-title="{source_title}"></span>')
        replacement=segment[:insert_at]+trace+segment[insert_at:]
        markup=markup[:start]+replacement+markup[end:]
        existing.add(fid)
    return markup

def validate_html(markup, article_type, metadata, research, rules):
    if not markup.strip(): raise PackError("WRITER_HTML_EMPTY")
    trules=rules.get("types",{}).get(article_type)
    if not isinstance(trules,dict): raise PackError("WRITING_RULES_TYPE_MISSING")
    for block in trules.get("required_blocks",[]):
        if f'data-block="{block}"' not in markup and f"data-block='{block}'" not in markup:
            raise PackError("REQUIRED_BLOCK_MISSING:"+block)
    if markup.lower().count("<table") != 1: raise PackError("TABLE_COUNT_NOT_EXACT_ONE")
    table_open=re.search(r"<table\b([^>]*)>",markup,re.I)
    if not table_open:
        raise PackError("TABLE_OPEN_TAG_MISSING")
    class_match=re.search(r'class=["\']([^"\']+)["\']',table_open.group(1),re.I)
    table_classes=set((class_match.group(1).split() if class_match else []))
    if not {"system-129-table","comparison-table"}.issubset(table_classes):
        raise PackError("CANONICAL_TABLE_CLASS_MISSING")
    claims=research.get("fact_pack",{}).get("claims",[])
    claim_map={str(x.get("fact_id") or ""):x for x in claims if isinstance(x,dict)}
    trace_tags=[m.group(0) for m in re.finditer(r'<span\b[^>]*class=["\'][^"\']*\bppm-source-trace\b[^"\']*["\'][^>]*>',markup,re.I)]
    trace_fact_ids=[]
    for tag in trace_tags:
        def attr(name):
            m=re.search(r"\b"+re.escape(name)+r'=["\']([^"\']+)["\']',tag,re.I)
            return m.group(1) if m else ""
        fid=attr("data-fact-id"); source_hash=attr("data-source-hash"); source_title=attr("data-source-title")
        trace_fact_ids.append(fid)
        claim=claim_map.get(fid)
        if not claim:
            raise PackError("PPM_SOURCE_TRACE_FACT_UNKNOWN:"+fid)
        if source_title != str(claim.get("source_id") or ""):
            raise PackError("PPM_SOURCE_TRACE_SOURCE_ID_MISMATCH:"+fid)
        if source_hash != str(claim.get("evidence_text_sha256") or ""):
            raise PackError("PPM_SOURCE_TRACE_HASH_MISMATCH:"+fid)
    required_trace_ids=set(str(x) for x in research.get("fact_pack",{}).get("fact_ids",[]) if str(x))
    if not required_trace_ids.issubset(set(trace_fact_ids)):
        missing=sorted(required_trace_ids-set(trace_fact_ids))
        raise PackError("PPM_SOURCE_TRACE_FACT_SET_MISMATCH:"+",".join(missing))
    if article_type=="Beratung" and 'data-list="criteria"' not in markup and "data-list='criteria'" not in markup:
        raise PackError("BERATUNG_CRITERIA_LIST_MISSING")
    if "ppm-ai-disclosure" not in markup: raise PackError("AI_DISCLOSURE_MISSING")
    if metadata["target_keyword"].casefold() not in metadata["title"].casefold():
        raise PackError("TITLE_KEYWORD_BINDING_INVALID")
    anchors=re.findall(r"<a\b[^>]*data-link-role=[\"']([^\"']+)[\"'][^>]*href=[\"']([^\"']+)[\"']",markup,re.I)
    if len(anchors)!=3: raise PackError("VISIBLE_LINK_COUNT_NOT_EXACT_THREE")
    expected={(x["role"],x["href"]) for x in research.get("portal_links",[])}
    if set(anchors)!=expected: raise PackError("LINK_BINDING_MISMATCH")
    allowed=set(research.get("fact_pack",{}).get("fact_ids",[]))
    used=[]
    for raw in re.findall(r"data-fact-ids=[\"']([^\"']+)[\"']",markup,re.I):
        used.extend(raw.split())
    if not used or not set(used).issubset(allowed): raise PackError("FACT_ID_BINDING_INVALID")
    if not allowed.issubset(set(used)): raise PackError("NOT_ALL_RESEARCH_FACTS_USED")
    if word_count(markup)<750 and article_type=="Beratung": raise PackError("BERATUNG_WORD_COUNT_BELOW_750")

def build(draft_path):
    job=load(JOB); entry=load(ENTRY); draft=load(draft_path); rules=load(RULES)
    if job.get("contract")!="K9_JOB_V1" or job.get("status")!="OPEN" or job.get("station") not in ("write","repair"):
        raise PackError("WRITE_JOB_INVALID")
    if entry.get("job_id")!=job.get("job_id") or entry.get("job_sha256")!=job.get("job_sha256"):
        raise PackError("CHAT_ENTRY_JOB_MISMATCH")
    if draft.get("contract")!="K9_WRITER_DRAFT_V1" or draft.get("job_id")!=job["job_id"]:
        raise PackError("WRITER_DRAFT_JOB_MISMATCH")
    if len(job.get("items",[]))!=1 or job.get("item_count")!=1:
        raise PackError("REALTEST_PACKAGER_EXPECTS_ONE_ITEM")
    item=job["items"][0]; item_id=item["item_id"]
    if draft.get("item_id")!=item_id: raise PackError("WRITER_DRAFT_ITEM_MISMATCH")
    meta=item["metadata"]; title=str(draft.get("title") or "").strip(); markup=str(draft.get("content_html") or "")
    if title!=meta["title"]: raise PackError("WRITER_TITLE_MISMATCH")
    research_row=item.get("input_products",{}).get("research")
    if not isinstance(research_row,dict): raise PackError("RESEARCH_INPUT_MISSING")
    research=research_row.get("research_product")
    if not isinstance(research,dict): raise PackError("RESEARCH_PRODUCT_MISSING")
    article_type=meta["article_type"]
    markup=ensure_all_fact_traces(markup,research)
    validate_html(markup,article_type,meta,research,rules)
    fact_pack=research["fact_pack"]; fact_ids=list(fact_pack["fact_ids"])
    portal_links=list(research["portal_links"]); decision=research.get("decision_support",{})
    link_bindings=[]
    for x in portal_links:
        role=x["role"]
        if role not in LINK_REASON_BY_ROLE:
            raise PackError("PORTAL_LINK_ROLE_UNSUPPORTED:"+str(role))
        link_bindings.append({
            "active":True,
            "anchor":x["anchor"],
            "href":x["href"],
            "reason":LINK_REASON_BY_ROLE[role],
            "role":role,
            "section_id":x["section_id"],
            "target_status":"publish",
            "target_type":"portal_route",
        })
    anchors=[x["anchor"] for x in portal_links]
    category_name=f"{article_type} {anchors[-1] if anchors else meta['target_keyword']}"
    hierarchy=" > ".join(anchors+[category_name]) if anchors else category_name
    expected_category={
        "category_source_snapshot_hash":PORTAL_SNAPSHOT_SHA256,
        "hierarchy_path":hierarchy,
        "name":category_name,
        "semantic_binding_not_numeric_identity":True,
        "slug":meta["category"],
        "taxonomy":"category",
    }
    type_meta={"decision_goal":decision.get("decision_goal",""),"decision_criteria":decision.get("decision_criteria",[])}
    registry={
        "contract":"portal_link_registry_snapshot_v2",
        "entries":link_bindings,
        "snapshot_source_sha256":PORTAL_SNAPSHOT_SHA256,
    }
    registry_hash=stable(registry)
    if meta.get("plan_slot")=="0b401802eeed8574d9c80f7eb5e1abb03c0ac5dbf82fa8b8a95deb7abf3bec15" and registry_hash!="5a6dd595e9dc6a906848a6aeeaf05abd2c130f5e8d999902a30bb4418fa63ee9":
        raise PackError("PORTAL_REGISTRY_HASH_NOT_APPROVED_REALTEST_BINDING")
    quality_binding={
        "ai_disclosure_required":True,
        "contract":"content_structure_language_binding_v2",
        "editorial_review_status":"PENDING_INDEPENDENT_REVIEW",
        "expected_category":expected_category,
        "intent_terms":[meta["target_keyword"]]+list(reversed(anchors)),
        "internal_test_marker":"LT"+meta["plan_slot"][:12].upper(),
        "language_evidence":{},
        "language_review_status":"PENDING_LANGUAGETOOL_6_8",
        "link_bindings":link_bindings,
        "minimum_word_count":750,
        "portal_link_registry":registry,
        "portal_link_registry_hash":registry_hash,
        "table_value_statement":"Die Tabelle bündelt die wichtigsten Auswahlkriterien für "+meta["target_keyword"]+" und macht die entscheidenden Prüfpunkte direkt vergleichbar.",
        "type_meta":type_meta,
        "wordpress_category":expected_category,
        "wordpress_runtime_category_status":"SEMANTIC_SNAPSHOT_BOUND_LIVE_ID_PENDING",
    }
    links=[dict(x) for x in link_bindings]
    order_id="k9-"+item_id[-8:]
    slug="reitplatzplaner-fuer-pferde" if meta["target_keyword"]=="Reitplatzplaner für Pferde" else re.sub(r"[^a-z0-9]+","-",meta["target_keyword"].lower()).strip("-")
    lead=text_of(re.search(r"<section\s+data-block=[\"']intro[\"'][^>]*>(.*?)</section>",markup,re.S|re.I).group(1))
    concl=text_of(re.search(r"<section\s+data-block=[\"']conclusion[\"'][^>]*>(.*?)</section>",markup,re.S|re.I).group(1))
    runtime_order={
        "allowed_fact_ids":fact_ids,"article_type":article_type,"conclusion":concl,"domain":"pferdeportal",
        "fact_pack_hash":fact_pack["fact_pack_hash"],"lead":lead,"links":links,"order_id":order_id,
        "required_sections":["Fazit","Weiterführende Informationen"],"section_fact_ids":fact_ids,"slug":slug,
        "subject_label":"die Auswahl eines Reitplatzplaners für Pferde","subject_scope":fact_pack["title_scope"],
        "table_focus":fact_ids[:4],"title":title
    }
    body_text=text_of(markup)
    metrics={"h2_count":len(re.findall(r"<h2\b",markup,re.I)),"paragraph_count":len(re.findall(r"<p\b",markup,re.I)),
             "table_body_row_count":len(re.findall(r"<tr\b",re.search(r"<tbody>(.*?)</tbody>",markup,re.S|re.I).group(1),re.I)),
             "visible_link_count":len(re.findall(r"<a\b",markup,re.I)),"word_count":word_count(markup)}
    content_plan={"article_type":article_type,"required_blocks":rules["types"][article_type]["required_blocks"],"fact_ids":fact_ids,
                  "link_roles":[x["role"] for x in portal_links]}
    canonical={
        "article_type":article_type,"body_html":markup,"body_html_sha256":hashlib.sha256(markup.encode()).hexdigest(),
        "body_text":body_text,"body_text_sha256":hashlib.sha256(body_text.encode()).hexdigest(),"claim_ids":fact_ids,
        "content_plan_hash":stable(content_plan),"fact_pack_hash":fact_pack["fact_pack_hash"],
        "gold_core_binding":"FOUR_TYPE_APPROVED_GOLD_CORE_V1",
        "gold_core_binding_hash":"d42fc479d52b084deb5d4092d4555b7ba5af0ccc5188df09273e69b621293bdb",
        "gold_reference_id":"K9_BERATUNG_REALTEST_001",
        "gold_reference_metrics":{"h2_count":5,"paragraph_count":31,"table_body_row_count":8,"visible_link_count":2,"word_count":1134},
        "gold_reference_sha256":"652f791c3c6d8fb3ff8cd367d920a36aaa910f0df0250a41ad6bbadae9b7dabc",
        "links":links,"local_candidate_metrics":metrics,"local_candidate_status":"STRUCTURAL_LOCAL_CANDIDATE_PENDING_MACHINE_REVIEW",
        "order_id":order_id,"skeleton_hash":stable({"blocks":rules["types"][article_type]["required_blocks"],"metrics":metrics}),
        "slug":slug,"source_ids":[x["source_id"] for x in research["sources"]],"title":title
    }
    ppm_item={
        "article_type":article_type,"contract_hashes":[],"gold_core_binding":"FOUR_TYPE_APPROVED_GOLD_CORE_V1",
        "plan_item_key":"k9-"+meta["plan_slot"][:16],"quality_binding":quality_binding,"quality_binding_hash":stable(quality_binding),
        "runtime_order":runtime_order,"search_intent":"COMMERCIAL_INVESTIGATION_ADVICE","source_hashes":[],
        "source_order_id":order_id,"source_snapshot_id":fact_pack["fact_pack_id"],"target_keyword":meta["target_keyword"],
        "three_type_local_binding":{"expected_category":expected_category,
            "semantic_keywords":[meta["target_keyword"]]+type_meta["decision_criteria"],
            "wordpress_runtime_term_id_required_later":True,"wordpress_runtime_validation_performed_now":False},
        "topic":title,"canonical_article":canonical
    }
    product={"contract":"K9_ARTICLE_PRODUCT_V1","article_type":article_type,"title":title,"content_html":markup,
             "content_sha256":hashlib.sha256(markup.encode()).hexdigest(),
             "research_product_sha256":research["product_sha256"],"ppm_item":ppm_item}
    product["product_sha256"]=stable(product)
    return {"contract":"K9_SUBMISSION_V1","job_id":job["job_id"],"station":job["station"],
            "results":[{"item_id":item_id,"article_product":product}]}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("draft"); ap.add_argument("--output",required=True); ns=ap.parse_args()
    try: out=build(Path(ns.draft))
    except (PackError,AttributeError) as exc:
        print(json.dumps({"contract":"K9_WRITE_PACKAGER_V1","status":"BLOCKED","reason":str(exc)},ensure_ascii=False,indent=2),file=sys.stderr)
        raise SystemExit(2)
    Path(ns.output).write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"contract":"K9_WRITE_PACKAGER_V1","status":"SUBMISSION_READY","job_id":out["job_id"],"item_count":len(out["results"])},indent=2))

if __name__=="__main__": main()
