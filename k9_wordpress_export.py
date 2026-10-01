#!/usr/bin/env python3
import argparse, hashlib, json
from pathlib import Path

CONTRACT="PFERDE_ATELIER_WORDPRESS_IMPORT_V1"
PLUGIN_VERSION="0.28.28"
ARTICLE_KEYS={"article_id","plan_slot","title","slug","target_keyword","category","article_type","body"}

class Blocked(RuntimeError): pass

def load(path):
    value=json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value,dict): raise Blocked("JSON_OBJECT_REQUIRED:"+str(path))
    return value

def sha_text(value): return hashlib.sha256(value.encode("utf-8")).hexdigest()

def ledger_article_done(row):
    if not isinstance(row,dict):
        return False
    stages=row.get("stages")
    if not isinstance(stages,dict) or stages.get("check")!="DONE":
        return False
    repair=stages.get("repair")
    if repair=="NOT_REQUIRED":
        return True
    if repair!="DONE":
        return False
    products=row.get("products")
    if not isinstance(products,dict):
        return False
    if int(row.get("revision") or 0)<1:
        return False
    return isinstance(products.get("repair"),dict) and isinstance(products.get("check"),dict)

def build(final_package,ledger):
    if final_package.get("contract")!="PSERC_APPROVED_PRODUCTION_PACKAGE_V1" or final_package.get("endstamp_contract")!="PFERDE_ATELIER_ENDSTEMPEL_RELEASE_V1" or final_package.get("status")!="ENDSTEMPEL_PASS":
        raise Blocked("ENDSTEMPEL_NOT_PASS")
    if final_package.get("publish_allowed") is not False or final_package.get("content_mutation_performed") is not False:
        raise Blocked("ENDSTEMPEL_FLAGS_INVALID")
    env=final_package.get("import_envelope"); manifest=final_package.get("article_manifest")
    if not isinstance(env,dict) or not isinstance(manifest,dict): raise Blocked("ENDSTEMPEL_COMPONENTS_MISSING")
    plan=env.get("production_plan"); release=env.get("workflow_release")
    if not isinstance(plan,dict) or plan.get("contract")!="production_plan_v4" or not isinstance(plan.get("items"),list): raise Blocked("PRODUCTION_PLAN_INVALID")
    if not isinstance(release,dict) or release.get("contract")!="WORKFLOW_SUPERVISOR_RELEASE_V2_SIGNED" or release.get("status")!="PASS" or release.get("wordpress_write_performed") is not False:
        raise Blocked("WORKFLOW_RELEASE_INVALID")
    rows=manifest.get("articles"); release_rows=release.get("items"); ledger_rows=ledger.get("items") if isinstance(ledger,dict) else None
    if not isinstance(rows,list) or not isinstance(release_rows,list) or not isinstance(ledger_rows,list): raise Blocked("ARTICLE_SET_INVALID")
    count=len(rows)
    if count<1 or len(plan["items"])!=count or len(release_rows)!=count: raise Blocked("ARTICLE_SET_COUNT_INVALID")
    if manifest.get("article_count")!=count or release.get("exact_five_item_count")!=count: raise Blocked("ARTICLE_COUNT_BINDING_INVALID")
    if release.get("exact_five_batch_sha256")!=final_package.get("batch_sha256"): raise Blocked("BATCH_BINDING_INVALID")
    plan_by_cid={}
    for item in plan["items"]:
        cid=str(item.get("canonical_article_id") or "") if isinstance(item,dict) else ""
        if not cid or cid in plan_by_cid: raise Blocked("PRODUCTION_PLAN_CANONICAL_ID_INVALID")
        plan_by_cid[cid]=item
    slot_to_cid={}
    for item in release_rows:
        slot=str(item.get("plan_slot") or "") if isinstance(item,dict) else ""; cid=str(item.get("canonical_article_id") or "") if isinstance(item,dict) else ""
        if not slot or not cid or slot in slot_to_cid: raise Blocked("WORKFLOW_RELEASE_SLOT_INVALID")
        slot_to_cid[slot]=cid
    ledger_by_slot={}
    for row in ledger_rows:
        meta=row.get("metadata") if isinstance(row,dict) else None; slot=str(meta.get("plan_slot") or "") if isinstance(meta,dict) else ""
        if not slot or slot in ledger_by_slot: raise Blocked("LEDGER_SLOT_INVALID")
        if not ledger_article_done(row): raise Blocked("LEDGER_ARTICLE_NOT_DONE:"+slot)
        ledger_by_slot[slot]=row
    articles=[]; seen=set()
    for index,row in enumerate(rows):
        slot=str(row.get("plan_slot") or "") if isinstance(row,dict) else ""; cid=slot_to_cid.get(slot); item=plan_by_cid.get(cid); ledger_item=ledger_by_slot.get(slot)
        if not slot or slot in seen or not isinstance(item,dict) or not isinstance(ledger_item,dict): raise Blocked("ARTICLE_BINDING_MISSING:"+str(index))
        seen.add(slot)
        body=row.get("content_utf8")
        if not isinstance(body,str) or not body: raise Blocked("ARTICLE_BODY_MISSING:"+str(index))
        body_sha=sha_text(body)
        if row.get("sha256")!=body_sha or row.get("byte_length")!=len(body.encode("utf-8")): raise Blocked("ARTICLE_BYTES_INVALID:"+str(index))
        canonical=item.get("canonical_article"); quality=item.get("quality_binding"); runtime=item.get("runtime_order") if isinstance(item.get("runtime_order"),dict) else {}
        category=quality.get("wordpress_category") if isinstance(quality,dict) else None
        slug=str(canonical.get("slug") or runtime.get("slug") or "") if isinstance(canonical,dict) else ""
        if not isinstance(canonical,dict) or canonical.get("body_html")!=body or canonical.get("body_html_sha256")!=body_sha: raise Blocked("CANONICAL_ARTICLE_BINDING_INVALID:"+str(index))
        if not slug: raise Blocked("WORDPRESS_SLUG_MISSING:"+str(index))
        if not isinstance(category,dict) or category.get("taxonomy")!="category" or not category.get("slug"): raise Blocked("WORDPRESS_CATEGORY_BINDING_INVALID:"+str(index))
        meta=ledger_item.get("metadata")
        expected={"title":canonical.get("title"),"target_keyword":item.get("target_keyword"),"category":category.get("slug"),"article_type":item.get("article_type"),"plan_slot":slot}
        for key,value in expected.items():
            if not isinstance(meta,dict) or meta.get(key)!=value: raise Blocked("LEDGER_METADATA_MISMATCH:"+str(index)+":"+key)
        articles.append({"article_id":cid,"plan_slot":slot,"title":expected["title"],"slug":slug,"target_keyword":expected["target_keyword"],"category":expected["category"],"article_type":expected["article_type"],"body":body})
    return {"contract":CONTRACT,"source_batch_sha256":final_package["batch_sha256"],"article_count":len(articles),"publish_allowed":False,"articles":articles}

def verify(value):
    if value.get("contract")!=CONTRACT or value.get("publish_allowed") is not False: raise Blocked("WORDPRESS_HANDOFF_CONTRACT_INVALID")
    articles=value.get("articles")
    if not isinstance(articles,list) or value.get("article_count")!=len(articles) or not articles: raise Blocked("WORDPRESS_HANDOFF_ARTICLE_COUNT_INVALID")
    slots=set(); ids=set(); slugs=set()
    for index,row in enumerate(articles):
        if not isinstance(row,dict) or set(row)!=ARTICLE_KEYS: raise Blocked("WORDPRESS_HANDOFF_ARTICLE_SCHEMA_INVALID:"+str(index))
        for field in ARTICLE_KEYS:
            if not str(row.get(field) or "").strip(): raise Blocked("WORDPRESS_HANDOFF_FIELD_EMPTY:"+str(index)+":"+field)
        if row["plan_slot"] in slots or row["article_id"] in ids or row["slug"] in slugs: raise Blocked("WORDPRESS_HANDOFF_IDENTITY_DUPLICATE:"+str(index))
        slots.add(row["plan_slot"]); ids.add(row["article_id"]); slugs.add(row["slug"])
    return {"contract":"K9_WORDPRESS_EXPORT_VERIFY_V2","status":"PASS","wordpress_contract":CONTRACT,"plugin_version":PLUGIN_VERSION,"article_count":len(articles),"source_batch_sha256":value["source_batch_sha256"],"publish_allowed":False}

def write_export(final_path,ledger_path,out_path):
    value=build(load(final_path),load(ledger_path)); verify(value)
    raw=(json.dumps(value,ensure_ascii=False,indent=2)+"\n").encode("utf-8")
    out=Path(out_path); out.parent.mkdir(parents=True,exist_ok=True); out.write_bytes(raw)
    return {"contract":"K9_WORDPRESS_EXPORT_RECEIPT_V2","status":"PASS","wordpress_contract":CONTRACT,"plugin_version":PLUGIN_VERSION,"filename":out.name,"wordpress_json_sha256":hashlib.sha256(raw).hexdigest(),"article_count":len(value["articles"]),"batch_sha256":value["source_batch_sha256"],"publish_allowed":False}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("final_package"); ap.add_argument("ledger"); ap.add_argument("output"); ap.add_argument("--receipt"); args=ap.parse_args()
    try: receipt=write_export(args.final_package,args.ledger,args.output)
    except Exception as exc:
        print(json.dumps({"contract":"K9_WORDPRESS_EXPORT_RECEIPT_V2","status":"BLOCKED","reason":str(exc),"publish_allowed":False},ensure_ascii=False,indent=2)); raise SystemExit(2)
    payload=json.dumps(receipt,ensure_ascii=False,indent=2)+"\n"
    if args.receipt: Path(args.receipt).write_text(payload,encoding="utf-8")
    print(payload,end="")

if __name__=="__main__":
    main()
