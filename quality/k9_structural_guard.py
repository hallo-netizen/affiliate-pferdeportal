#!/usr/bin/env python3
import html as htmlmod, json, re

CONTRACT="K9_STRUCTURAL_PREFLIGHT_RESULT_V1"

def text_of(markup):
    value=re.sub(r"(?is)<(script|style)\b[^>]*>.*?</\1>"," ",str(markup or ""))
    value=re.sub(r"(?s)<[^>]+>"," ",value)
    value=htmlmod.unescape(value)
    return re.sub(r"\s+"," ",value).strip()

def word_count(markup):
    return len(re.findall(r"\b[\wÄÖÜäöüß-]+\b",text_of(markup),re.UNICODE))

def _attr(tag,name):
    m=re.search(r"\b"+re.escape(name)+r'=["\']([^"\']+)["\']',tag,re.I)
    return m.group(1) if m else ""

def _placeholder_source_id(value):
    value=str(value or "").strip().casefold()
    return any(token in value for token in ("test_","dummy","example","placeholder"))

def _trace_source_label(research,source_id):
    source_id=str(source_id or "").strip()
    if _placeholder_source_id(source_id):
        for source in research.get("sources",[]) if isinstance(research,dict) else []:
            if isinstance(source,dict) and str(source.get("source_id") or "").strip()==source_id:
                return str(source.get("title") or "").strip()
    return source_id

def evaluate(markup,article_type,metadata,research,rules):
    findings=[]
    def add(code,**detail):
        row={"code":code}; row.update(detail); findings.append(row)

    trules=(rules.get("types") or {}).get(article_type) if isinstance(rules,dict) else None
    if not isinstance(trules,dict):
        return {"contract":CONTRACT,"status":"BLOCKED","findings":[{"code":"WRITING_RULES_TYPE_MISSING"}]}

    if not str(markup or "").strip():
        add("WRITER_HTML_EMPTY")
    for block in trules.get("required_blocks",[]):
        if f'data-block="{block}"' not in markup and f"data-block='{block}'" not in markup:
            add("REQUIRED_BLOCK_MISSING",block=block)

    table_count=markup.lower().count("<table")
    if table_count!=1:
        add("TABLE_COUNT_NOT_EXACT_ONE",actual=table_count,expected=1)

    summary_cfg=(rules.get("global") or {}).get("post_table_summary_policy") or {}
    table_section=re.search(r'(?is)<section\b[^>]*data-block\s*=\s*(["\'])table\1[^>]*>(.*?)</section>',markup)
    if not table_section:
        add("TABLE_SECTION_MISSING")
    else:
        table_body=table_section.group(2)
        table_match=re.search(r"(?is)<table\b[^>]*>.*?</table>",table_body)
        if not table_match:
            add("TABLE_OPEN_TAG_MISSING")
        else:
            after=table_body[table_match.end():]
            paragraphs=re.findall(r"(?is)<p\b[^>]*>(.*?)</p>",after)
            expected=int(summary_cfg.get("paragraphs_exact",1))
            if len(paragraphs)!=expected:
                add("POST_TABLE_SUMMARY_PARAGRAPH_COUNT_INVALID",actual=len(paragraphs),expected=expected)
            elif paragraphs:
                summary=text_of(paragraphs[0])
                words=word_count(summary)
                lo=int(summary_cfg.get("words_min",12)); hi=int(summary_cfg.get("words_max",35))
                if words<lo or words>hi:
                    add("POST_TABLE_SUMMARY_WORD_RANGE_INVALID",actual=words,minimum=lo,maximum=hi)
                sentences=len([x for x in re.split(r"(?<=[.!?])\s+",summary) if x.strip()])
                slo=int(summary_cfg.get("sentences_min",1)); shi=int(summary_cfg.get("sentences_max",2))
                if sentences<slo or sentences>shi:
                    add("POST_TABLE_SUMMARY_SENTENCE_COUNT_INVALID",actual=sentences,minimum=slo,maximum=shi)

    table_open=re.search(r"<table\b([^>]*)>",markup,re.I)
    if table_open:
        cm=re.search(r'class=["\']([^"\']+)["\']',table_open.group(1),re.I)
        classes=set(cm.group(1).split() if cm else [])
        if not {"system-129-table","comparison-table"}.issubset(classes):
            add("CANONICAL_TABLE_CLASS_MISSING")
    elif not any(x["code"]=="TABLE_OPEN_TAG_MISSING" for x in findings):
        add("TABLE_OPEN_TAG_MISSING")

    fact_pack=research.get("fact_pack") if isinstance(research,dict) else {}
    claims=fact_pack.get("claims",[]) if isinstance(fact_pack,dict) else []
    claim_map={str(x.get("fact_id") or ""):x for x in claims if isinstance(x,dict)}
    trace_ids=[]
    tags=re.findall(r'<span\b[^>]*class=["\'][^"\']*\bppm-source-trace\b[^"\']*["\'][^>]*>',markup,re.I)
    for tag in tags:
        fid=_attr(tag,"data-fact-id"); trace_ids.append(fid)
        claim=claim_map.get(fid)
        if not claim:
            add("PPM_SOURCE_TRACE_FACT_UNKNOWN",fact_id=fid)
            continue
        expected_title=_trace_source_label(research,claim.get("source_id"))
        actual_title=_attr(tag,"data-source-title")
        if actual_title!=expected_title:
            add("PPM_SOURCE_TRACE_SOURCE_TITLE_MISMATCH",fact_id=fid,expected=expected_title,actual=actual_title)
        expected_hash=str(claim.get("evidence_text_sha256") or "")
        actual_hash=_attr(tag,"data-source-hash")
        if actual_hash!=expected_hash:
            add("PPM_SOURCE_TRACE_HASH_MISMATCH",fact_id=fid,expected=expected_hash,actual=actual_hash)

    required={str(x.get("fact_id") or "") for x in claims if isinstance(x,dict) and str(x.get("fact_id") or "")}
    missing=sorted(required-set(trace_ids))
    if missing:
        add("PPM_SOURCE_TRACE_FACT_SET_MISMATCH",missing=missing)
    invalid={fid:trace_ids.count(fid) for fid in sorted(required) if trace_ids.count(fid)!=1}
    if invalid:
        add("PPM_SOURCE_TRACE_COUNT_INVALID",counts=invalid,expected_each=1)

    if article_type=="Beratung" and 'data-list="criteria"' not in markup and "data-list='criteria'" not in markup:
        add("BERATUNG_CRITERIA_LIST_MISSING")
    if "ppm-ai-disclosure" not in markup:
        add("AI_DISCLOSURE_MISSING")
    target=str(metadata.get("target_keyword") or "")
    title=str(metadata.get("title") or "")
    if target.casefold() not in title.casefold():
        add("TITLE_KEYWORD_BINDING_INVALID")

    anchors=re.findall(r"<a\b[^>]*data-link-role=[\"']([^\"']+)[\"'][^>]*href=[\"']([^\"']+)[\"']",markup,re.I)
    if len(anchors)!=3:
        add("VISIBLE_LINK_COUNT_NOT_EXACT_THREE",actual=len(anchors),expected=3)
    expected={(x.get("role"),x.get("href")) for x in research.get("portal_links",[]) if isinstance(x,dict)}
    if set(anchors)!=expected:
        add("LINK_BINDING_MISMATCH")

    allowed=set(fact_pack.get("fact_ids",[]) if isinstance(fact_pack,dict) else [])
    used=[]
    for raw in re.findall(r"data-fact-ids=[\"']([^\"']+)[\"']",markup,re.I):
        used.extend(raw.split())
    unknown=sorted(set(used)-allowed)
    if not used or unknown:
        add("FACT_ID_BINDING_INVALID",unknown=unknown)
    unused=sorted(allowed-set(used))
    if unused:
        add("NOT_ALL_RESEARCH_FACTS_USED",missing=unused)
    if article_type=="Beratung" and word_count(markup)<750:
        add("BERATUNG_WORD_COUNT_BELOW_750",actual=word_count(markup),minimum=750)

    return {
        "contract":CONTRACT,
        "status":"PASS" if not findings else "REPAIR_REQUIRED",
        "findings":findings,
        "publish_allowed":False,
    }
