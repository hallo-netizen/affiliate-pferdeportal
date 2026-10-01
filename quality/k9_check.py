#!/usr/bin/env python3
import argparse, hashlib, json, re, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import k9_lt68
import k9_ppm679
import k9_rule_guard
import k9_table_guard
sys.path.insert(0,str(HERE.parent.resolve()))
import k9_writer_plan

class CheckError(RuntimeError):
    pass

def stable(obj):
    raw=json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(",",":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()

def load_json(path):
    try:
        value=json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception as exc:
        raise CheckError("K9_CHECK_JSON_INVALID") from exc
    if not isinstance(value,dict):
        raise CheckError("K9_CHECK_OBJECT_REQUIRED")
    return value

def one_product(job_item, key, contract):
    row=job_item.get("input_products",{}).get(key)
    if not isinstance(row,dict):
        raise CheckError("K9_CHECK_INPUT_MISSING:"+key)
    product=row.get(contract)
    if not isinstance(product,dict):
        raise CheckError("K9_CHECK_PRODUCT_MISSING:"+contract)
    return product


def source_trace_count_findings(html, fact_pack):
    fact_ids=[str(x) for x in fact_pack.get("fact_ids",[]) if str(x)]
    counts={fid:0 for fid in fact_ids}
    for tag in re.findall(r'<span\b[^>]*class=["\'][^"\']*\bppm-source-trace\b[^"\']*["\'][^>]*>',html,re.I):
        m=re.search(r'\bdata-fact-id=["\']([^"\']+)["\']',tag,re.I)
        if m and m.group(1) in counts:
            counts[m.group(1)]+=1
    return [
        {"code":"K9_RULE_SOURCE_TRACE_COUNT_INVALID","fact_id":fid,"actual":counts[fid],"expected":1}
        for fid in fact_ids if counts[fid]!=1
    ]


def reuse_or_run_lt(article, html, jar_path, authoritative_words=None):
    preflight=article.get("lt68_preflight_result")
    if not isinstance(preflight,dict):
        with tempfile.TemporaryDirectory(prefix="k9-check-lt68-") as td:
            p=Path(td)/"article.html"
            p.write_text(html,encoding="utf-8")
            return k9_lt68.run(Path(jar_path),p,authoritative_words=authoritative_words)
    article_sha=hashlib.sha256(html.encode("utf-8")).hexdigest()
    evidence=preflight.get("language_evidence")
    checked=k9_lt68.ppm_visible_language_text(html)
    checked_sha=hashlib.sha256(checked.encode("utf-8")).hexdigest()
    if preflight.get("contract")!="K9_LT68_RESULT_V1":
        raise CheckError("K9_CHECK_LT_PREFLIGHT_CONTRACT_INVALID")
    if preflight.get("status")!="PASS" or int(preflight.get("finding_count") or 0)!=0:
        raise CheckError("K9_CHECK_LT_PREFLIGHT_NOT_PASS")
    if preflight.get("engine")!=k9_lt68.ENGINE or preflight.get("jar_sha256")!=k9_lt68.LT_JAR_SHA256:
        raise CheckError("K9_CHECK_LT_PREFLIGHT_ENGINE_INVALID")
    if preflight.get("article_sha256")!=article_sha or preflight.get("checked_text_sha256")!=checked_sha:
        raise CheckError("K9_CHECK_LT_PREFLIGHT_CONTENT_BINDING_INVALID")
    if not isinstance(evidence,dict):
        raise CheckError("K9_CHECK_LT_PREFLIGHT_EVIDENCE_MISSING")
    if evidence.get("content_hash")!=article_sha or evidence.get("checked_text_sha256")!=checked_sha:
        raise CheckError("K9_CHECK_LT_PREFLIGHT_EVIDENCE_BINDING_INVALID")
    if evidence.get("engine")!=k9_lt68.ENGINE or int(evidence.get("unresolved_finding_count") or 0)!=0:
        raise CheckError("K9_CHECK_LT_PREFLIGHT_EVIDENCE_STATUS_INVALID")
    return json.loads(json.dumps(preflight))

def run_job(job_path, jar_path, ppm_path):
    job=load_json(job_path)
    if job.get("contract")!="K9_JOB_V1" or job.get("status")!="OPEN" or job.get("station")!="check":
        raise CheckError("K9_CHECK_JOB_INVALID")
    rows=[]
    for item in job.get("items",[]):
        item_id=str(item.get("item_id") or "")
        if not item_id:
            raise CheckError("K9_CHECK_ITEM_ID_MISSING")
        research=one_product(item,"research","research_product")
        article=one_product(item,"article","article_product")
        html=str(article.get("content_html") or "")
        title=str(article.get("title") or "")
        ppm_item=json.loads(json.dumps(article.get("ppm_item")))
        fact_pack=json.loads(json.dumps(research.get("fact_pack")))
        if isinstance(fact_pack,dict):
            source_titles={str(x.get("source_id") or "").strip():str(x.get("title") or "").strip() for x in research.get("sources",[]) if isinstance(x,dict)}
            for claim in fact_pack.get("claims",[]) if isinstance(fact_pack.get("claims"),list) else []:
                if not isinstance(claim,dict):
                    continue
                sid=str(claim.get("source_id") or "").strip()
                if sid.upper().startswith("TEST_") and source_titles.get(sid):
                    claim["source_id"]=source_titles[sid]
        if not html or not title or not isinstance(ppm_item,dict) or not isinstance(fact_pack,dict):
            raise CheckError("K9_CHECK_BOUND_INPUT_INCOMPLETE")

        rules_path=HERE.parent/"contracts"/"K9_WRITING_RULES.json"
        rules=load_json(rules_path)
        writing_result=k9_rule_guard.evaluate(html,item.get("metadata") or {},rules)
        table_result=k9_table_guard.evaluate(html)
        table_rule=k9_table_guard.load_rule()
        table_findings=list(table_result.get("findings") or [])
        if table_rule.get("word_budget",{}).get("table_words_count_toward_article_minimum") is False:
            minimum=int((rules.get("editorial_additive",{}).get("balance_policy",{}) or {}).get("hard_total_words_min") or 0)
            if minimum and int(table_result.get("non_table_word_count") or 0)<minimum:
                table_findings.append({"code":"K9_RULE_TABLE_CANNOT_FILL_ARTICLE_WORD_FLOOR","actual_non_table_words":int(table_result.get("non_table_word_count") or 0),"minimum":minimum})
        trace_findings=source_trace_count_findings(html,fact_pack)
        writing_result["findings"]=list(writing_result.get("findings") or [])+table_findings+trace_findings
        writing_result["table_rule_contract"]=table_result.get("rule_contract")
        if table_findings or trace_findings:
            writing_result["status"]="REPAIR_REQUIRED"
        if article.get("writing_rules_sha256")!=writing_result.get("writing_rules_sha256"):
            raise CheckError("K9_CHECK_WRITING_RULES_BINDING_MISMATCH")

        lt_result=reuse_or_run_lt(
            article,html,jar_path,
            authoritative_words=k9_writer_plan.authoritative_domain_terms(item.get("metadata") or {},research)
        )
        with tempfile.TemporaryDirectory(prefix="k9-check-") as td:
            root=Path(td)
            binding=ppm_item.get("quality_binding")
            if not isinstance(binding,dict):
                raise CheckError("K9_CHECK_QUALITY_BINDING_MISSING")
            evidence=lt_result.get("language_evidence")
            if not isinstance(evidence,dict):
                raise CheckError("K9_CHECK_LT_EVIDENCE_MISSING")
            binding["language_evidence"]=evidence
            ppm_item["quality_binding_hash"]=stable(binding)
            ppm_input={
                "contract":"K9_PPM679_INPUT_V1",
                "generated":{
                    "article_type":str(ppm_item.get("article_type") or article.get("article_type") or ""),
                    "title":title,
                    "content_html":html,
                    "content_hash":article.get("content_sha256")
                },
                "item":ppm_item,
                "fact_pack":fact_pack
            }
            ppm_input_path=root/"ppm-input.json"
            ppm_input_path.write_text(json.dumps(ppm_input,ensure_ascii=False),encoding="utf-8")
            ppm_result=k9_ppm679.run(Path(ppm_path),ppm_input_path)

        if ppm_result.get("status")=="BLOCKED":
            raise CheckError("K9_CHECK_PPM_BLOCKED")
        if lt_result.get("status") not in ("PASS","REPAIR_REQUIRED"):
            raise CheckError("K9_CHECK_LT_STATUS_INVALID")
        if ppm_result.get("status") not in ("PASS","REPAIR_REQUIRED"):
            raise CheckError("K9_CHECK_PPM_STATUS_INVALID")
        rows.append({
            "item_id":item_id,
            "lt68_result":lt_result,
            "ppm679_result":ppm_result,
            "writing_rules_result":writing_result
        })
    if len(rows)!=job.get("item_count"):
        raise CheckError("K9_CHECK_ITEM_COUNT_MISMATCH")
    return {
        "contract":"K9_SUBMISSION_V1",
        "job_id":job["job_id"],
        "station":"check",
        "results":rows
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("job")
    ap.add_argument("lt_jar")
    ap.add_argument("ppm_package")
    ap.add_argument("--output",required=True)
    args=ap.parse_args()
    try:
        result=run_job(args.job,args.lt_jar,args.ppm_package)
    except Exception as exc:
        print(json.dumps({"contract":"K9_CHECK_EXECUTION_V1","status":"BLOCKED","reason":str(exc)},ensure_ascii=False,indent=2))
        raise SystemExit(2)
    Path(args.output).write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"contract":"K9_CHECK_EXECUTION_V1","status":"SUBMISSION_READY","job_id":result["job_id"],"item_count":len(result["results"])},indent=2))

if __name__=="__main__":
    main()
