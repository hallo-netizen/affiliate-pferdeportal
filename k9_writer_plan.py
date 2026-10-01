#!/usr/bin/env python3
import hashlib, json, re
from pathlib import Path

ROOT=Path(__file__).resolve().parent
RULES_PATH=ROOT/"contracts"/"K9_WRITING_RULES.json"
TABLE_RULE_PATH=ROOT/"contracts"/"K9_TABLE_RULE_V1.json"
LT_DICTIONARY_PATH=ROOT/"contracts"/"K9_LT68_DOMAIN_DICTIONARY.json"
CONTRACT="K9_WRITER_ACCEPTANCE_PLAN_V1"

class WriterPlanError(RuntimeError):
    pass

def stable(obj):
    return hashlib.sha256(json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")).hexdigest()

def load(path):
    try:
        data=json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception as exc:
        raise WriterPlanError("WRITER_PLAN_SOURCE_INVALID:"+str(path)) from exc
    if not isinstance(data,dict):
        raise WriterPlanError("WRITER_PLAN_SOURCE_OBJECT_REQUIRED:"+str(path))
    return data

def authoritative_domain_terms(metadata,research):
    """Exact tokens from authoritative metadata/portal labels only; never from free draft prose."""
    values=[
        str(metadata.get("title") or ""),
        str(metadata.get("target_keyword") or ""),
    ]
    for row in research.get("portal_links",[]) if isinstance(research,dict) else []:
        if isinstance(row,dict):
            values.append(str(row.get("anchor") or ""))
    terms=set()
    for value in values:
        for token in re.findall(r"[A-Za-zÄÖÜäöüß-]+",value):
            token=token.strip("-")
            if len(token)>=4:
                terms.add(token)
    base=load(LT_DICTIONARY_PATH)
    for token in base.get("words",[]):
        if isinstance(token,str) and token.strip():
            terms.add(token.strip())
    return sorted(terms,key=lambda x:x.casefold())

def build(metadata,research,ppm_authoring_rules):
    if not isinstance(metadata,dict) or not isinstance(research,dict) or not isinstance(ppm_authoring_rules,dict):
        raise WriterPlanError("WRITER_PLAN_INPUT_INVALID")
    rules=load(RULES_PATH)
    table=load(TABLE_RULE_PATH)
    article_type=str(metadata.get("article_type") or "")
    type_rules=(rules.get("types") or {}).get(article_type)
    if not isinstance(type_rules,dict):
        raise WriterPlanError("WRITER_PLAN_ARTICLE_TYPE_UNSUPPORTED:"+article_type)
    portal_links=research.get("portal_links")
    fact_pack=research.get("fact_pack")
    if not isinstance(portal_links,list) or len(portal_links)!=3 or not isinstance(fact_pack,dict):
        raise WriterPlanError("WRITER_PLAN_RESEARCH_BINDING_INVALID")

    additive=rules["editorial_additive"]
    balance=additive["balance_policy"]
    conclusion=additive["conclusion_policy"]
    headings=additive["heading_policy"]
    summary=(rules.get("global") or {}).get("post_table_summary_policy") or {}
    normal_blocks=[x for x in type_rules.get("required_blocks",[]) if x not in set(balance.get("exempt_blocks") or [])]
    safe_min=max(int(balance["hard_total_words_min"]),int(balance["preferred_total_words_min"]))
    safe_max=min(int(balance["hard_total_words_max"]),int(balance["preferred_total_words_max"]))
    safe_section_min=max(int(balance["normal_h2_section_min_words"]),120)
    safe_section_max=min(int(balance["normal_h2_section_max_words"]),170)
    if safe_section_min>safe_section_max:
        safe_section_min=int(balance["normal_h2_section_min_words"])
        safe_section_max=int(balance["normal_h2_section_max_words"])

    plan={
        "contract":CONTRACT,
        "article_identity":{
            "title":metadata.get("title"),
            "target_keyword":metadata.get("target_keyword"),
            "category":metadata.get("category"),
            "article_type":article_type,
            "plan_slot":metadata.get("plan_slot"),
        },
        "structure":{
            "required_blocks":list(type_rules.get("required_blocks") or []),
            "required_lists":list(type_rules.get("required_lists") or []),
            "normal_balanced_blocks":normal_blocks,
            "table_count_exact":1,
            "visible_internal_links_exact":3,
            "ai_disclosure_required":True,
        },
        "word_budget":{
            "hard_total_min":balance["hard_total_words_min"],
            "hard_total_max":balance["hard_total_words_max"],
            "preferred_total_min":balance["preferred_total_words_min"],
            "preferred_total_max":balance["preferred_total_words_max"],
            "non_table_min":balance["hard_total_words_min"] if balance.get("table_may_fill_word_budget") is False else None,
            "normal_section_min":balance["normal_h2_section_min_words"],
            "normal_section_max":balance["normal_h2_section_max_words"],
            "longest_to_shortest_max_ratio":balance["normal_h2_longest_to_shortest_max_ratio"],
            "further_information_max":balance["further_information_maximum_words"],
            "writer_safety_target_total":[safe_min,safe_max],
            "writer_safety_target_normal_section":[safe_section_min,safe_section_max],
        },
        "conclusion":{
            "target_ratio_min":conclusion["target_ratio_min"],
            "target_ratio_max":conclusion["target_ratio_max"],
            "maximum_ratio":conclusion["maximum_ratio"],
            "maximum_paragraphs":conclusion["maximum_paragraphs"],
        },
        "headings":{
            "exact_target_phrase_occurrences_max":headings["exact_target_phrase_occurrences_max"],
            "exact_target_phrase_occurrences_when_title_equals_target":headings["exact_target_phrase_occurrences_when_title_equals_target"],
            "significant_keyword_token_h2_occurrences_max":headings["significant_target_keyword_token_h2_occurrences_max"],
            "repeated_heading_lead_word_max":headings["repeated_heading_lead_word_max"],
            "hard_h2_words_max":headings["hard_h2_words_max"],
            "hard_h2_chars_max":headings["hard_h2_chars_max"],
            "keyword_staccato_forbidden":headings["keyword_staccato_forbidden"],
        },
        "table":{
            "header_max_words":table["header"]["maximum_words"],
            "first_column_max_words":table["first_column"]["maximum_words"],
            "other_cells_hard_max_words":table["other_cells"]["hard_maximum_words"],
            "sentences_forbidden":True,
            "table_words_count_toward_article_minimum":table["word_budget"]["table_words_count_toward_article_minimum"],
            "post_table_summary_paragraphs_exact":summary.get("paragraphs_exact"),
            "post_table_summary_words_min":summary.get("words_min"),
            "post_table_summary_words_max":summary.get("words_max"),
            "post_table_summary_sentences_min":summary.get("sentences_min"),
            "post_table_summary_sentences_max":summary.get("sentences_max"),
        },
        "portal_links":[{
            "role":x.get("role"),"anchor":x.get("anchor"),"href":x.get("href"),"section_id":x.get("section_id")
        } for x in portal_links],
        "fact_binding":{
            "allowed_fact_ids":list(fact_pack.get("fact_ids") or []),
            "all_facts_must_be_used":True,
            "source_trace_per_fact_exact":1,
        },
        "language":{
            "engine":"LanguageTool 6.8 / Bestand 43",
            "unresolved_findings_max":0,
            "authoritative_domain_terms":authoritative_domain_terms(metadata,research),
            "domain_terms_scope":"EXACT_GERMAN_SPELLER_RULE_ONLY",
            "other_language_rules_remain_blocking":True,
        },
        "ppm679":{
            "ppm_version":ppm_authoring_rules.get("ppm_version"),
            "global_requirements":ppm_authoring_rules.get("global_requirements"),
            "structure_requirements":ppm_authoring_rules.get("structure_requirements"),
            "type_requirements":ppm_authoring_rules.get("type_requirements"),
            "quality_change_allowed":False,
        },
        "repair_policy":"RETURN_ALL_INDEPENDENT_FINDINGS_TOGETHER_AND_REPAIR_IN_ONE_PASS",
        "publish_allowed":False,
    }
    core=dict(plan)
    plan["plan_sha256"]=stable(core)
    return plan
