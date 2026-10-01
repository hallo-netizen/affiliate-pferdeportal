#!/usr/bin/env python3
import hashlib, html as htmlmod, json, re
from collections import Counter

CONTRACT = "K9_WRITING_RULES_RESULT_V1"
REQUIRED_GROUPS = {"ppm_679","lt_68","k9_structural","editorial_additive"}
SUPPORTED_EDITORIAL_SCHEMA = {
    "heading_policy": {"contract","target_keyword_exact_phrase_mode","exact_target_phrase_occurrences_max","exact_target_phrase_occurrences_min_when_no_title_collision","exact_target_phrase_occurrences_when_title_equals_target","significant_target_keyword_token_h2_occurrences_max","keyword_staccato_forbidden","phrase_family_repetition_forbidden","duplicate_normalized_h2_forbidden","repeated_heading_lead_word_max","natural_heading_surface_required","heading_content_relation_required","significant_keyword_stop_tokens","preferred_h2_words_min","preferred_h2_words_max","hard_h2_words_max","hard_h2_chars_max","short_special_heading_exception","generic_filler_word_driven_heading_forbidden","grammatical_pattern_variety_required","section_specific_content_required"},
    "balance_policy": {"contract","hard_total_words_min","hard_total_words_max","preferred_total_words_min","preferred_total_words_max","normal_h2_section_min_words","normal_h2_section_max_words","normal_h2_longest_to_shortest_max_ratio","normal_h2_combined_minimum_ratio","exempt_blocks","table_may_fill_word_budget","further_information_maximum_words","further_information_may_fill_word_budget"},
    "conclusion_policy": {"contract","target_ratio_min","target_ratio_max","maximum_ratio","maximum_paragraphs","use_conclusion_to_fill_global_word_or_paragraph_floor"},
    "surface_policy": {"natural_german_required","artificial_generator_phrase_forbidden","keyword_staccato_forbidden","phrase_family_repetition_forbidden","template_spam_forbidden","forbidden_generator_phrases"},
    "writer_targets": {"semantics","table_unique_token_ratio_target_if_applicable","target_trace_lexical_support_ratio","trace_unit_minimum_shared_lexical_tokens","target_duplicate_sentence_ratio"}
}

class RuleGuardError(RuntimeError):
    pass

def stable(obj):
    return hashlib.sha256(json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")).hexdigest()

def _plain(value):
    value=re.sub(r"(?is)<(script|style)\b[^>]*>.*?</\1>"," ",str(value or ""))
    value=re.sub(r"(?s)<[^>]+>"," ",value)
    return re.sub(r"\s+"," ",htmlmod.unescape(value)).strip()

def _norm(value):
    value=_plain(value).casefold()
    value=re.sub(r"[^a-z0-9äöüß]+"," ",value)
    return re.sub(r"\s+"," ",value).strip()

def _words(value):
    return re.findall(r"\b[\wÄÖÜäöüß-]+\b",_plain(value),re.UNICODE)

def validate_coverage(rules):
    if not isinstance(rules,dict) or rules.get("contract")!="K9_WRITING_RULES_V1":
        raise RuleGuardError("K9_WRITING_RULES_CONTRACT_INVALID")
    coverage=rules.get("coverage")
    if not isinstance(coverage,dict) or coverage.get("contract")!="K9_COMPLETE_RULE_COVERAGE_V1" or coverage.get("fail_closed") is not True:
        raise RuleGuardError("K9_RULE_COVERAGE_CONTRACT_MISSING")
    groups=coverage.get("rule_groups")
    required=set(coverage.get("required_rule_groups") or [])
    if required!=REQUIRED_GROUPS:
        raise RuleGuardError("K9_RULE_COVERAGE_REQUIRED_GROUPS_DRIFT")
    if not isinstance(groups,dict) or set(groups)!=REQUIRED_GROUPS:
        raise RuleGuardError("K9_RULE_COVERAGE_GROUP_SET_INCOMPLETE")
    for name in sorted(REQUIRED_GROUPS):
        owners=groups[name].get("enforced_by") if isinstance(groups.get(name),dict) else None
        if not isinstance(owners,list) or not owners or any(not str(x).strip() for x in owners):
            raise RuleGuardError("K9_RULE_GROUP_WITHOUT_ENFORCEMENT_OWNER:"+name)
    additive=rules.get("editorial_additive")
    if not isinstance(additive,dict) or additive.get("contract")!="K9_EDITORIAL_ADDITIVE_RULES_V1":
        raise RuleGuardError("K9_EDITORIAL_ADDITIVE_RULES_MISSING")
    expected_groups=set(SUPPORTED_EDITORIAL_SCHEMA)
    actual_groups=set(additive)-{"contract"}
    if actual_groups!=expected_groups:
        raise RuleGuardError("K9_EDITORIAL_RULE_GROUP_SCHEMA_DRIFT")
    for key,expected_keys in SUPPORTED_EDITORIAL_SCHEMA.items():
        value=additive.get(key)
        if not isinstance(value,dict):
            raise RuleGuardError("K9_EDITORIAL_RULE_GROUP_MISSING:"+key)
        if set(value)!=expected_keys:
            raise RuleGuardError("K9_EDITORIAL_RULE_FIELD_SCHEMA_DRIFT:"+key)
    return {"status":"PASS","contract":"K9_COMPLETE_RULE_COVERAGE_V1","rules_sha256":stable(rules)}

def _h2_rows(article_html):
    rows=[]
    for m in re.finditer(r"(?is)<h2\b[^>]*>(.*?)</h2>",article_html):
        heading=_plain(m.group(1))
        rows.append({"heading":heading,"normalized":_norm(heading)})
    return rows

def heading_findings(article_html,metadata,rules):
    validate_coverage(rules)
    cfg=rules["editorial_additive"]["heading_policy"]
    rows=_h2_rows(article_html)
    findings=[]
    if not rows:
        return [{"code":"K9_RULE_H2_MISSING"}]
    target=_norm(metadata.get("target_keyword"))
    title=_norm(metadata.get("title"))
    collision=bool(target and title==target)
    exact=sum(1 for row in rows if target and target in row["normalized"])
    expected=0 if collision else int(cfg.get("exact_target_phrase_occurrences_min_when_no_title_collision",0))
    maximum=0 if collision else int(cfg.get("exact_target_phrase_occurrences_max",2))
    if exact<expected or exact>maximum:
        findings.append({"code":"K9_RULE_H2_EXACT_TARGET_OCCURRENCES","actual":exact,"minimum":expected,"maximum":maximum})
    stop={_norm(x) for x in cfg.get("significant_keyword_stop_tokens",[]) if _norm(x)}
    significant=[x for x in target.split() if len(x)>=4 and x not in stop]
    max_token=int(cfg.get("significant_target_keyword_token_h2_occurrences_max",2))
    for token in sorted(set(significant)):
        count=sum(1 for row in rows if token in row["normalized"].split())
        if count>max_token:
            findings.append({"code":"K9_RULE_H2_KEYWORD_STACCATO","token":token,"actual":count,"maximum":max_token})
    hard_words=int(cfg.get("hard_h2_words_max",9))
    hard_chars=int(cfg.get("hard_h2_chars_max",65))
    for row in rows:
        heading=row["heading"]
        word_count=len(_words(heading))
        char_count=len(heading)
        if word_count>hard_words or char_count>hard_chars:
            findings.append({
                "code":"K9_RULE_H2_TOO_LONG",
                "heading":heading,
                "word_count":word_count,
                "maximum_words":hard_words,
                "char_count":char_count,
                "maximum_chars":hard_chars
            })
    normalized=[row["normalized"] for row in rows if row["normalized"]]
    if cfg.get("duplicate_normalized_h2_forbidden") and len(normalized)!=len(set(normalized)):
        findings.append({"code":"K9_RULE_H2_DUPLICATE_NORMALIZED"})
    if cfg.get("phrase_family_repetition_forbidden"):
        ignore={"fazit","weitere","weiterführende","weiterfuehrende"}
        leads=[row["normalized"].split()[0] for row in rows if row["normalized"].split() and row["normalized"].split()[0] not in ignore]
        limit=int(cfg.get("repeated_heading_lead_word_max",2))
        for lead,count in Counter(leads).items():
            if count>limit:
                findings.append({"code":"K9_RULE_H2_PHRASE_FAMILY_REPETITION","lead":lead,"actual":count,"maximum":limit})
    return findings

def _section_rows(article_html):
    rows=[]
    for m in re.finditer(r'(?is)<section\b[^>]*data-block\s*=\s*(["\'])([^"\']+)\1[^>]*>(.*?)</section>',article_html):
        block=m.group(2)
        body=m.group(3)
        h2=re.search(r"(?is)<h2\b[^>]*>(.*?)</h2>",body)
        if h2 is None:
            continue
        content=body[h2.end():]
        rows.append({
            "block_id":block,
            "heading":_plain(h2.group(1)),
            "word_count":len(_words(content)),
            "paragraph_count":len(re.findall(r"(?is)<p\b[^>]*>",content))
        })
    return rows

def balance_findings(article_html,rules):
    validate_coverage(rules)
    cfg=rules["editorial_additive"]["balance_policy"]
    ccfg=rules["editorial_additive"]["conclusion_policy"]
    findings=[]
    total=len(_words(article_html))
    hard_min=int(cfg["hard_total_words_min"]); hard_max=int(cfg["hard_total_words_max"])
    if total<hard_min or total>hard_max:
        findings.append({"code":"K9_RULE_TOTAL_WORD_RANGE","actual":total,"minimum":hard_min,"maximum":hard_max})
    rows=_section_rows(article_html)
    exempt=set(cfg.get("exempt_blocks") or [])
    normal=[x for x in rows if x["block_id"] not in exempt]
    minw=int(cfg["normal_h2_section_min_words"]); maxw=int(cfg["normal_h2_section_max_words"])
    for row in normal:
        if row["word_count"]<minw or row["word_count"]>maxw:
            findings.append({"code":"K9_RULE_H2_SECTION_WORD_RANGE","block_id":row["block_id"],"actual":row["word_count"],"minimum":minw,"maximum":maxw})
    if normal:
        counts=[x["word_count"] for x in normal]
        if min(counts)<=0 or max(counts)/min(counts)>float(cfg["normal_h2_longest_to_shortest_max_ratio"]):
            findings.append({"code":"K9_RULE_H2_SECTION_IMBALANCE","shortest":min(counts),"longest":max(counts),"maximum_ratio":cfg["normal_h2_longest_to_shortest_max_ratio"]})
        main=sum(counts)
        ratio=(main/total) if total else 0.0
        if ratio<float(cfg["normal_h2_combined_minimum_ratio"]):
            findings.append({"code":"K9_RULE_MAIN_TEXT_RATIO_TOO_LOW","actual":ratio,"minimum":cfg["normal_h2_combined_minimum_ratio"]})
    conclusions=[x for x in rows if x["block_id"]=="conclusion"]
    if len(conclusions)==1 and total:
        row=conclusions[0]; ratio=row["word_count"]/total
        if ratio>float(ccfg["maximum_ratio"]):
            findings.append({"code":"K9_RULE_CONCLUSION_RATIO_TOO_HIGH","actual":ratio,"maximum":ccfg["maximum_ratio"]})
        if row["paragraph_count"]>int(ccfg["maximum_paragraphs"]):
            findings.append({"code":"K9_RULE_CONCLUSION_PARAGRAPHS_TOO_HIGH","actual":row["paragraph_count"],"maximum":ccfg["maximum_paragraphs"]})
    further=[x for x in rows if x["block_id"]=="further_information"]
    if len(further)==1 and further[0]["word_count"]>int(cfg["further_information_maximum_words"]):
        findings.append({"code":"K9_RULE_FURTHER_INFORMATION_TOO_LONG","actual":further[0]["word_count"],"maximum":cfg["further_information_maximum_words"]})
    return findings

def surface_findings(article_html,rules):
    validate_coverage(rules)
    cfg=rules["editorial_additive"]["surface_policy"]
    text=_plain(article_html)
    findings=[]
    if cfg.get("artificial_generator_phrase_forbidden"):
        for phrase in cfg.get("forbidden_generator_phrases",[]):
            if str(phrase) and str(phrase).casefold() in text.casefold():
                findings.append({"code":"K9_RULE_ARTIFICIAL_GENERATOR_PHRASE","phrase":phrase})
    return findings

def evaluate(article_html,metadata,rules):
    coverage=validate_coverage(rules)
    findings=[]
    findings.extend(heading_findings(article_html,metadata,rules))
    findings.extend(balance_findings(article_html,rules))
    findings.extend(surface_findings(article_html,rules))
    content_sha=hashlib.sha256(str(article_html).encode("utf-8")).hexdigest()
    return {
        "contract":CONTRACT,
        "status":"PASS" if not findings else "REPAIR_REQUIRED",
        "content_sha256":content_sha,
        "writing_rules_sha256":coverage["rules_sha256"],
        "coverage_contract":coverage["contract"],
        "findings":findings,
        "publish_allowed":False
    }
