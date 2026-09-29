#!/usr/bin/env python3
import argparse, hashlib, json
from pathlib import Path

class Blocked(RuntimeError): pass
def stable(o): return hashlib.sha256(json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def load(p):
    x=json.loads(Path(p).read_text(encoding="utf-8"))
    if not isinstance(x,dict): raise Blocked("JSON_OBJECT_REQUIRED")
    return x

def verify(path):
    x=load(path)
    env=x.get("import_envelope")
    if x.get("contract")!="PSERC_APPROVED_PRODUCTION_PACKAGE_V1" or x.get("endstamp_contract")!="PFERDE_ATELIER_ENDSTEMPEL_RELEASE_V1" or x.get("status")!="ENDSTEMPEL_PASS": raise Blocked("OUTER_CONTRACT_INVALID")
    if not isinstance(env,dict) or env.get("contract")!="PSERC_APPROVED_PRODUCTION_PACKAGE_V1": raise Blocked("IMPORT_ENVELOPE_INVALID")
    rel=env.get("workflow_release"); plan=env.get("production_plan"); bundle=env.get("fact_pack_bundle")
    if not isinstance(rel,dict) or rel.get("contract")!="WORKFLOW_SUPERVISOR_RELEASE_V2_SIGNED" or rel.get("status")!="PASS" or rel.get("wordpress_write_performed") is not False: raise Blocked("WORKFLOW_RELEASE_INVALID")
    if not isinstance(plan,dict) or plan.get("contract")!="production_plan_v4" or not isinstance(plan.get("items"),list): raise Blocked("PRODUCTION_PLAN_INVALID")
    if not isinstance(bundle,dict) or bundle.get("contract")!="canonical_fact_pack_import_v1" or not isinstance(bundle.get("fact_packs"),list): raise Blocked("FACT_PACK_BUNDLE_INVALID")
    if stable(bundle)!=env.get("fact_pack_bundle_sha256") or stable(plan)!=env.get("production_plan_sha256") or stable(rel)!=env.get("workflow_release_sha256"): raise Blocked("IMPORT_COMPONENT_HASH_INVALID")
    manifest=x.get("article_manifest"); articles=manifest.get("articles") if isinstance(manifest,dict) else None
    release_items=rel.get("items")
    if not isinstance(articles,list) or not isinstance(release_items,list) or len(articles)!=len(release_items) or len(plan["items"])!=len(articles): raise Blocked("ARTICLE_SET_COUNT_INVALID")
    by_cid={str(i.get("canonical_article_id")):i for i in plan["items"] if isinstance(i,dict)}
    by_slot={str(i.get("plan_slot")):str(i.get("canonical_article_id")) for i in release_items if isinstance(i,dict)}
    for row in articles:
        slot=str(row.get("plan_slot") or ""); cid=by_slot.get(slot); item=by_cid.get(cid)
        if not cid or not isinstance(item,dict): raise Blocked("RELEASE_PLAN_BINDING_MISSING")
        ca=item.get("canonical_article")
        if not isinstance(ca,dict) or ca.get("body_html")!=row.get("content_utf8"): raise Blocked("WORDPRESS_ARTICLE_BODY_MISMATCH")
        raw=row["content_utf8"].encode("utf-8")
        if hashlib.sha256(raw).hexdigest()!=row.get("sha256") or len(raw)!=row.get("byte_length"): raise Blocked("WORDPRESS_ARTICLE_BYTES_INVALID")
        if item.get("target_keyword") in (None,"") or item.get("article_type") in (None,""): raise Blocked("WORDPRESS_METADATA_MISSING")
        q=item.get("quality_binding"); cat=q.get("wordpress_category") if isinstance(q,dict) else None
        if not isinstance(cat,dict) or not cat.get("slug") or cat.get("taxonomy")!="category": raise Blocked("WORDPRESS_CATEGORY_INVALID")
    if rel.get("exact_five_item_count")!=len(articles): raise Blocked("WORDPRESS_ITEM_COUNT_INVALID")
    if rel.get("exact_five_batch_sha256")!=x.get("batch_sha256"): raise Blocked("WORDPRESS_BATCH_BINDING_INVALID")
    if x.get("publish_allowed") is not False: raise Blocked("WORDPRESS_PREMATURE_PUBLISH")
    return {"contract":"K9_WORDPRESS_IMPORT_VERIFY_V1","status":"PASS","article_count":len(articles),"batch_sha256":x["batch_sha256"],"publish_allowed":False}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("final"); ap.add_argument("--output"); a=ap.parse_args()
    try: r=verify(a.final)
    except Exception as exc:
        r={"contract":"K9_WORDPRESS_IMPORT_VERIFY_V1","status":"BLOCKED","reason":str(exc),"publish_allowed":False}
        print(json.dumps(r,ensure_ascii=False,indent=2)); raise SystemExit(2)
    payload=json.dumps(r,ensure_ascii=False,indent=2)+"\n"
    if a.output: Path(a.output).write_text(payload,encoding="utf-8")
    print(payload,end="")
if __name__=="__main__": main()
