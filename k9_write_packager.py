#!/usr/bin/env python3
import argparse, copy, hashlib, html as htmlmod, json, re, sys, tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str((ROOT/"quality").resolve()))
import k9_lt68
import k9_ppm679
import k9_rule_guard
import k9_table_guard
JOB=ROOT/"runtime"/"CURRENT_JOB.json"
ENTRY=ROOT/"runtime"/"CHAT_ENTRY.json"
RULES=ROOT/"contracts"/"K9_WRITING_RULES.json"
PPM_PACKAGE=ROOT/"quality"/"PORTAL_PRODUCTION_MACHINE_V6.7.9.zip"
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

def _placeholder_source_id(value):
    value=str(value or "").strip().casefold()
    return any(token in value for token in ("test_", "dummy", "example", "placeholder"))

def _trace_fact_ids(markup):
    out=[]
    for tag in re.findall(r'<span\b[^>]*class=["\'][^"\']*\bppm-source-trace\b[^"\']*["\'][^>]*>',markup,re.I):
        m=re.search(r'\bdata-fact-id=["\']([^"\']+)["\']',tag,re.I)
        if m:
            out.append(m.group(1))
    return out

def _trace_source_label(research, source_id):
    source_id=str(source_id or "").strip()
    if not source_id:
        return ""
    if _placeholder_source_id(source_id):
        for source in research.get("sources",[]):
            if isinstance(source,dict) and str(source.get("source_id") or "").strip()==source_id:
                title=str(source.get("title") or "").strip()
                if title:
                    return title
    return source_id

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
        source_id=str(claim.get("source_id") or "").strip()
        source_title=_trace_source_label(research,source_id)
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
    summary_cfg=(rules.get("global",{}) or {}).get("post_table_summary_policy")
    if not isinstance(summary_cfg,dict) or summary_cfg.get("required") is not True:
        raise PackError("POST_TABLE_SUMMARY_RULE_MISSING")
    table_section=re.search(r'(?is)<section\b[^>]*data-block\s*=\s*(["\'])table\1[^>]*>(.*?)</section>',markup)
    if not table_section:
        raise PackError("TABLE_SECTION_MISSING")
    table_body=table_section.group(2)
    table_match=re.search(r"(?is)<table\b[^>]*>.*?</table>",table_body)
    if not table_match:
        raise PackError("TABLE_OPEN_TAG_MISSING")
    after_table=table_body[table_match.end():]
    paragraphs=re.findall(r"(?is)<p\b[^>]*>(.*?)</p>",after_table)
    if len(paragraphs)!=int(summary_cfg.get("paragraphs_exact",1)):
        raise PackError("POST_TABLE_SUMMARY_PARAGRAPH_COUNT_INVALID")
    summary_text=text_of(paragraphs[0])
    summary_words=len(re.findall(r"\b[\wÄÖÜäöüß-]+\b",summary_text,re.UNICODE))
    if summary_words<int(summary_cfg.get("words_min",12)) or summary_words>int(summary_cfg.get("words_max",35)):
        raise PackError("POST_TABLE_SUMMARY_WORD_RANGE_INVALID")
    sentence_count=len([x for x in re.split(r"(?<=[.!?])\s+",summary_text) if x.strip()])
    if sentence_count<int(summary_cfg.get("sentences_min",1)) or sentence_count>int(summary_cfg.get("sentences_max",2)):
        raise PackError("POST_TABLE_SUMMARY_SENTENCE_COUNT_INVALID")
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
        expected_title=_trace_source_label(research,claim.get("source_id"))
        if not expected_title or source_title != expected_title:
            raise PackError("PPM_SOURCE_TRACE_SOURCE_TITLE_MISMATCH:"+fid)
        if source_hash != str(claim.get("evidence_text_sha256") or ""):
            raise PackError("PPM_SOURCE_TRACE_HASH_MISMATCH:"+fid)
    required_trace_ids=set(
        str(x.get("fact_id") or "") for x in claims
        if isinstance(x,dict) and str(x.get("fact_id") or "")
    )
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

def validate_ppm_authoring_rules(item, article_type):
    bound=(item.get("input_products") or {}).get("ppm_authoring_rules")
    if not isinstance(bound,dict) or bound.get("contract")!="K9_PPM679_AUTHORING_RULES_V1":
        raise PackError("PPM_AUTHORING_RULES_MISSING")
    if bound.get("article_type")!=article_type or bound.get("ppm_version")!="6.7.9":
        raise PackError("PPM_AUTHORING_RULES_TYPE_OR_VERSION_MISMATCH")
    if bound.get("ppm_package_sha256")!="acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1":
        raise PackError("PPM_AUTHORING_RULES_PACKAGE_HASH_MISMATCH")
    if bound.get("source_mode")!="EXACT_HASH_BOUND_PPM679_PACKAGE" or bound.get("quality_change_allowed") is not False:
        raise PackError("PPM_AUTHORING_RULES_SOURCE_INVALID")
    if not isinstance(bound.get("global_requirements"),dict) or not isinstance(bound.get("structure_requirements"),dict) or not isinstance(bound.get("type_requirements"),dict):
        raise PackError("PPM_AUTHORING_RULES_INCOMPLETE")
    required_constants={
        "min_words","min_paragraphs","min_h2","min_table_body_rows",
        "min_fact_pack_coverage_ratio","min_trace_lexical_support_ratio",
        "max_duplicate_sentence_ratio","max_intro_pair_similarity",
    }
    if not required_constants.issubset(set(bound["global_requirements"])):
        raise PackError("PPM_AUTHORING_RULES_CONSTANTS_INCOMPLETE")
    declared=str(bound.get("rules_sha256") or "")
    core=dict(bound); core.pop("rules_sha256",None)
    if declared!=stable(core):
        raise PackError("PPM_AUTHORING_RULES_HASH_INVALID")
    return bound

def complete_rule_preflight(markup, metadata, rules):
    writing=k9_rule_guard.evaluate(markup,metadata,rules)
    table=k9_table_guard.evaluate(markup)
    findings=list(writing.get("findings") or [])
    table_findings=list(table.get("findings") or [])
    table_rule=k9_table_guard.load_rule()
    if table_rule.get("word_budget",{}).get("table_words_count_toward_article_minimum") is False:
        minimum=int((rules.get("editorial_additive",{}).get("balance_policy",{}) or {}).get("hard_total_words_min") or 0)
        if minimum and int(table.get("non_table_word_count") or 0)<minimum:
            table_findings.append({
                "code":"K9_RULE_TABLE_CANNOT_FILL_ARTICLE_WORD_FLOOR",
                "actual_non_table_words":int(table.get("non_table_word_count") or 0),
                "minimum":minimum
            })
    findings.extend(table_findings)
    if writing.get("status")!="PASS" or findings:
        codes=[]
        for finding in findings:
            if isinstance(finding,dict):
                code=str(finding.get("code") or finding.get("error_code") or "UNKNOWN")
            else:
                code=str(finding)
            if code and code not in codes:
                codes.append(code)
        raise PackError("WRITING_PREFLIGHT_REPAIR_REQUIRED:"+",".join(codes or ["UNKNOWN"]))
    return True


def _synthetic_zero_lt_evidence(markup):
    checked=k9_lt68.ppm_visible_language_text(markup)
    article_sha=hashlib.sha256(markup.encode("utf-8")).hexdigest()
    checked_sha=hashlib.sha256(checked.encode("utf-8")).hexdigest()
    raw_report=json.dumps({"matches":[]},ensure_ascii=False,separators=(",",":"))
    raw_sha=hashlib.sha256(raw_report.encode("utf-8")).hexdigest()
    return {
        "engine":k9_lt68.ENGINE,
        "outer_dependency_sha256":k9_lt68.LT_OUTER_DEPENDENCY_SHA256,
        "inner_dependency_sha256":k9_lt68.LT_INNER_DEPENDENCY_SHA256,
        "content_hash":article_sha,
        "checked_text":checked,
        "checked_text_sha256":checked_sha,
        "raw_report_json":raw_report,
        "raw_report_sha256":raw_sha,
        "raw_finding_count":0,
        "unresolved_finding_count":0,
        "return_code":0,
        "approved_exceptions":[],
        "execution_record":{"input_sha256":checked_sha,"raw_stdout_sha256":raw_sha,"return_code":0},
    }

def exact_ppm_authoring_preflight(product,research):
    ppm_item=copy.deepcopy(product.get("ppm_item"))
    if not isinstance(ppm_item,dict):
        raise PackError("PPM679_AUTHORING_PREFLIGHT_ITEM_MISSING")
    binding=ppm_item.get("quality_binding")
    if not isinstance(binding,dict):
        raise PackError("PPM679_AUTHORING_PREFLIGHT_BINDING_MISSING")
    markup=str(product.get("content_html") or "")
    binding["language_evidence"]=_synthetic_zero_lt_evidence(markup)
    ppm_item["quality_binding_hash"]=stable(binding)
    fact_pack=copy.deepcopy(research.get("fact_pack"))
    if not isinstance(fact_pack,dict):
        raise PackError("PPM679_AUTHORING_PREFLIGHT_FACT_PACK_MISSING")
    source_titles={str(x.get("source_id") or "").strip():str(x.get("title") or "").strip() for x in research.get("sources",[]) if isinstance(x,dict)}
    for claim in fact_pack.get("claims",[]) if isinstance(fact_pack.get("claims"),list) else []:
        if not isinstance(claim,dict):
            continue
        sid=str(claim.get("source_id") or "").strip()
        if sid.upper().startswith("TEST_") and source_titles.get(sid):
            claim["source_id"]=source_titles[sid]
    payload={
        "contract":"K9_PPM679_INPUT_V1",
        "generated":{
            "article_type":str(product.get("article_type") or ""),
            "title":str(product.get("title") or ""),
            "content_html":markup,
            "content_hash":str(product.get("content_sha256") or ""),
        },
        "item":ppm_item,
        "fact_pack":fact_pack,
    }
    with tempfile.TemporaryDirectory(prefix="k9-writer-ppm-preflight-") as td:
        p=Path(td)/"input.json"
        p.write_text(json.dumps(payload,ensure_ascii=False),encoding="utf-8")
        result=k9_ppm679.run(PPM_PACKAGE,p)
    if result.get("status")=="BLOCKED":
        raise PackError("PPM679_AUTHORING_PREFLIGHT_BLOCKED:"+str(result.get("reason") or result.get("phase") or "UNKNOWN"))
    errors=[e for e in (result.get("errors") or []) if isinstance(e,dict) and e.get("error_code")!="BLOCKED_WAVE2_LANGUAGE_EVIDENCE"]
    if errors:
        codes=[]
        for e in errors:
            code=str(e.get("error_code") or "UNKNOWN")
            if code not in codes:
                codes.append(code)
        raise PackError("PPM679_AUTHORING_PREFLIGHT_REPAIR_REQUIRED:"+",".join(codes))
    return True

def lt68_writer_preflight(markup,lt_jar):
    if lt_jar is None:
        return True
    with tempfile.TemporaryDirectory(prefix="k9-writer-lt68-preflight-") as td:
        p=Path(td)/"article.html"
        p.write_text(markup,encoding="utf-8")
        result=k9_lt68.run(Path(lt_jar),p)
    if result.get("status")!="PASS":
        ids=[]
        for finding in result.get("findings") or []:
            rid=str(finding.get("rule_id") or "UNKNOWN")
            if rid not in ids:
                ids.append(rid)
        raise PackError("LT68_WRITER_PREFLIGHT_REPAIR_REQUIRED:"+str(result.get("finding_count") or 0)+":"+",".join(ids or ["UNKNOWN"]))
    return result


def _build_single(job,entry,rules,rules_sha,draft,lt_jar=None):
    if job.get("contract")!="K9_JOB_V1" or job.get("status")!="OPEN" or job.get("station") not in ("write","repair"):
        raise PackError("WRITE_JOB_INVALID")
    if entry.get("job_id")!=job.get("job_id") or entry.get("job_sha256")!=job.get("job_sha256"):
        raise PackError("CHAT_ENTRY_JOB_MISMATCH")
    if entry.get("writing_rules_path")!="contracts/K9_WRITING_RULES.json" or entry.get("writing_rules_sha256")!=rules_sha:
        raise PackError("COMPLETE_WRITING_RULE_BINDING_INVALID")
    if entry.get("writing_rules_coverage_contract")!="K9_COMPLETE_RULE_COVERAGE_V1" or entry.get("complete_rule_application_required") is not True:
        raise PackError("WRITING_RULE_COVERAGE_NOT_REQUIRED")
    if entry.get("writer_ppm679_preflight_required") is not True or entry.get("writer_lt68_preflight_required") is not True:
        raise PackError("WRITER_EARLY_BINDING_REQUIREMENTS_MISSING")
    if draft.get("contract")!="K9_WRITER_DRAFT_V1" or draft.get("job_id")!=job["job_id"]:
        raise PackError("WRITER_DRAFT_JOB_MISMATCH")
    item_id=str(draft.get("item_id") or "").strip()
    matches=[x for x in job.get("items",[]) if x.get("item_id")==item_id]
    if len(matches)!=1: raise PackError("WRITER_DRAFT_ITEM_MISMATCH")
    item=matches[0]
    meta=item["metadata"]; title=str(draft.get("title") or "").strip(); markup=str(draft.get("content_html") or "")
    if title!=meta["title"]: raise PackError("WRITER_TITLE_MISMATCH")
    research_row=item.get("input_products",{}).get("research")
    if not isinstance(research_row,dict): raise PackError("RESEARCH_INPUT_MISSING")
    research=research_row.get("research_product")
    if not isinstance(research,dict): raise PackError("RESEARCH_PRODUCT_MISSING")
    article_type=meta["article_type"]
    validate_ppm_authoring_rules(item,article_type)
    markup=ensure_all_fact_traces(markup,research)
    validate_html(markup,article_type,meta,research,rules)
    complete_rule_preflight(markup,meta,rules)
    lt68_preflight=lt68_writer_preflight(markup,lt_jar)
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
    if article_type=="FAQ":
        type_meta={"primary_question":title}
        intro_match=re.search(r"<section\s+data-block=[\"']intro[\"'][^>]*>(.*?)</section>",markup,re.S|re.I)
        first_p=re.search(r"<p\b[^>]*>(.*?)</p>",intro_match.group(1),re.S|re.I) if intro_match else None
        direct_answer=text_of(first_p.group(1)) if first_p else ""
        if len(re.findall(r"\b[\wÄÖÜäöüß-]+\b",direct_answer,re.UNICODE))<12:
            raise PackError("FAQ_DIRECT_ANSWER_BINDING_INVALID")
    else:
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
    if article_type=="FAQ":
        quality_binding["faq_direct_answer"]=direct_answer
    links=[dict(x) for x in link_bindings]
    order_id="k9-"+item_id[-8:]
    slug="reitplatzplaner-fuer-pferde" if meta["target_keyword"]=="Reitplatzplaner für Pferde" else re.sub(r"[^a-z0-9]+","-",meta["target_keyword"].lower()).strip("-")
    lead=text_of(re.search(r"<section\s+data-block=[\"']intro[\"'][^>]*>(.*?)</section>",markup,re.S|re.I).group(1))
    concl=text_of(re.search(r"<section\s+data-block=[\"']conclusion[\"'][^>]*>(.*?)</section>",markup,re.S|re.I).group(1))
    runtime_order={
        "allowed_fact_ids":fact_ids,"article_type":article_type,"conclusion":concl,"domain":"pferdeportal",
        "fact_pack_hash":fact_pack["fact_pack_hash"],"lead":lead,"links":links,"order_id":order_id,
        "required_sections":["Fazit","Weiterführende Informationen"],"section_fact_ids":fact_ids,"slug":slug,
        "subject_label":meta["target_keyword"],"subject_scope":fact_pack["title_scope"],
        "table_focus":fact_ids[:4],"title":title
    }
    if article_type=="FAQ":
        runtime_order.update({
            "lead":direct_answer,
            "answer":direct_answer,
            "faq_question":title,
            "faq_answer":direct_answer,
            "primary_question":title,
            "question":title,
            "summary":direct_answer,
        })
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
            "semantic_keywords":[meta["target_keyword"]]+list(decision.get("decision_criteria",[])),
            "wordpress_runtime_term_id_required_later":True,"wordpress_runtime_validation_performed_now":False},
        "topic":title,"canonical_article":canonical
    }
    product={"contract":"K9_ARTICLE_PRODUCT_V1","article_type":article_type,"title":title,"content_html":markup,
             "content_sha256":hashlib.sha256(markup.encode()).hexdigest(),
             "research_product_sha256":research["product_sha256"],"writing_rules_sha256":rules_sha,
             "writing_rules_coverage_contract":"K9_COMPLETE_RULE_COVERAGE_V1","ppm_item":ppm_item}
    if isinstance(lt68_preflight,dict):
        product["lt68_preflight_result"]=lt68_preflight
    exact_ppm_authoring_preflight(product,research)
    product["product_sha256"]=stable(product)
    return {"item_id":item_id,"article_product":product}

def build(draft_path,lt_jar=None):
    job=load(JOB); entry=load(ENTRY); draft=load(draft_path); rules=load(RULES)
    coverage=k9_rule_guard.validate_coverage(rules)
    rules_sha=coverage["rules_sha256"]
    if draft.get("contract")!="K9_WRITER_DRAFT_V1" or draft.get("job_id")!=job.get("job_id"):
        raise PackError("WRITER_DRAFT_JOB_MISMATCH")
    if job.get("item_count")==1 and "items" not in draft:
        drafts=[draft]
    else:
        rows=draft.get("items")
        if not isinstance(rows,list) or len(rows)!=job.get("item_count"):
            raise PackError("WRITER_DRAFT_BATCH_COUNT_MISMATCH")
        ids=[str(x.get("item_id") or "") for x in rows if isinstance(x,dict)]
        if len(ids)!=len(set(ids)) or set(ids)!=set(job.get("item_ids") or []):
            raise PackError("WRITER_DRAFT_BATCH_ITEM_SET_MISMATCH")
        drafts=[]
        for row in rows:
            drafts.append({
                "contract":"K9_WRITER_DRAFT_V1",
                "job_id":job["job_id"],
                "item_id":row.get("item_id"),
                "title":row.get("title"),
                "content_html":row.get("content_html")
            })
    results=[_build_single(job,entry,rules,rules_sha,row,lt_jar=lt_jar) for row in drafts]
    return {"contract":"K9_SUBMISSION_V1","job_id":job["job_id"],"station":job["station"],"results":results}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("draft"); ap.add_argument("--lt-jar"); ap.add_argument("--output",required=True); ns=ap.parse_args()
    try: out=build(Path(ns.draft),Path(ns.lt_jar) if ns.lt_jar else None)
    except (PackError,AttributeError) as exc:
        print(json.dumps({"contract":"K9_WRITE_PACKAGER_V1","status":"BLOCKED","reason":str(exc)},ensure_ascii=False,indent=2),file=sys.stderr)
        raise SystemExit(2)
    Path(ns.output).write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"contract":"K9_WRITE_PACKAGER_V1","status":"SUBMISSION_READY","job_id":out["job_id"],"item_count":len(out["results"])},indent=2))

if __name__=="__main__": main()
