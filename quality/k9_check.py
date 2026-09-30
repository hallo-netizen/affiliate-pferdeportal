#!/usr/bin/env python3
import argparse, hashlib, json, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import k9_lt68
import k9_ppm679
import k9_rule_guard

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
        fact_pack=research.get("fact_pack")
        if not html or not title or not isinstance(ppm_item,dict) or not isinstance(fact_pack,dict):
            raise CheckError("K9_CHECK_BOUND_INPUT_INCOMPLETE")

        rules_path=HERE.parent/"contracts"/"K9_WRITING_RULES.json"
        rules=load_json(rules_path)
        writing_result=k9_rule_guard.evaluate(html,item.get("metadata") or {},rules)
        if article.get("writing_rules_sha256")!=writing_result.get("writing_rules_sha256"):
            raise CheckError("K9_CHECK_WRITING_RULES_BINDING_MISMATCH")

        with tempfile.TemporaryDirectory(prefix="k9-check-") as td:
            root=Path(td)
            article_path=root/"article.html"
            article_path.write_text(html,encoding="utf-8")
            lt_result=k9_lt68.run(Path(jar_path),article_path)
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
