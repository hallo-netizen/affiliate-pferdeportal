#!/usr/bin/env python3
import html as htmlmod
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
RULE_PATH=ROOT/"contracts"/"K9_TABLE_RULE_V1.json"

class TableRuleError(RuntimeError):
    pass

def _plain(value):
    value=re.sub(r"(?is)<(script|style)\b[^>]*>.*?</\1>"," ",str(value or ""))
    value=re.sub(r"(?s)<[^>]+>"," ",value)
    return re.sub(r"\s+"," ",htmlmod.unescape(value)).strip()

def _words(value):
    return re.findall(r"\b[\wÄÖÜäöüß-]+\b",_plain(value),re.UNICODE)

def load_rule():
    rule=json.loads(RULE_PATH.read_text(encoding="utf-8"))
    if rule.get("contract")!="K9_MOBILE_COMPACT_TABLE_POLICY_V1" or rule.get("status")!="ACTIVE":
        raise TableRuleError("K9_TABLE_RULE_INVALID")
    expected_top={"contract","status","purpose","header","first_column","other_cells","word_budget","publish_allowed"}
    if set(rule)!=expected_top:
        raise TableRuleError("K9_TABLE_RULE_SCHEMA_DRIFT")
    expected_label={"preferred_words","maximum_words","multiword_exception","sentences_forbidden"}
    if set(rule.get("header") or {})!=expected_label or set(rule.get("first_column") or {})!=expected_label:
        raise TableRuleError("K9_TABLE_LABEL_RULE_SCHEMA_DRIFT")
    if set(rule.get("other_cells") or {})!={"preferred_maximum_words","hard_maximum_words","sentences_forbidden","flow_text_forbidden"}:
        raise TableRuleError("K9_TABLE_CELL_RULE_SCHEMA_DRIFT")
    if set(rule.get("word_budget") or {})!={"table_words_count_toward_article_minimum","missing_article_words_must_be_added_to_normal_prose"}:
        raise TableRuleError("K9_TABLE_WORD_BUDGET_RULE_SCHEMA_DRIFT")
    return rule

def _table(article_html):
    m=re.search(r"(?is)<table\b[^>]*>.*?</table>",str(article_html or ""))
    return m.group(0) if m else ""

def evaluate(article_html):
    rule=load_rule()
    table=_table(article_html)
    findings=[]
    if not table:
        return {"status":"PASS","findings":[]}
    headers=[_plain(x) for x in re.findall(r"(?is)<th\b[^>]*>(.*?)</th>",table)]
    rows=[]
    for tr in re.findall(r"(?is)<tr\b[^>]*>(.*?)</tr>",table):
        cells=[_plain(x) for x in re.findall(r"(?is)<td\b[^>]*>(.*?)</td>",tr)]
        if cells:
            rows.append(cells)
    hmax=int(rule["header"]["maximum_words"])
    fmax=int(rule["first_column"]["maximum_words"])
    dmax=int(rule["other_cells"]["hard_maximum_words"])
    for ci,value in enumerate(headers,1):
        if len(_words(value))>hmax:
            findings.append({"code":"K9_RULE_TABLE_HEADER_TOO_LONG","column":ci,"maximum_words":hmax})
        if re.search(r"[.!?;:]\s*$",value):
            findings.append({"code":"K9_RULE_TABLE_HEADER_SENTENCE_FORBIDDEN","column":ci})
    for ri,row in enumerate(rows,1):
        for ci,value in enumerate(row,1):
            maximum=fmax if ci==1 else dmax
            if len(_words(value))>maximum:
                findings.append({"code":"K9_RULE_TABLE_FIRST_COLUMN_TOO_LONG" if ci==1 else "K9_RULE_TABLE_CELL_TOO_LONG","row":ri,"column":ci,"maximum_words":maximum})
            if re.search(r"[.!?;:]\s*$",value):
                findings.append({"code":"K9_RULE_TABLE_SENTENCE_FORBIDDEN","row":ri,"column":ci})
    no_table=re.sub(r"(?is)<section\b[^>]*data-block\s*=\s*([\"'])table\1[^>]*>.*?</section>"," ",str(article_html or ""),count=1)
    return {"status":"PASS" if not findings else "REPAIR_REQUIRED","findings":findings,"non_table_word_count":len(_words(no_table)),"rule_contract":rule["contract"]}

if __name__=="__main__":
    raise SystemExit(0)
