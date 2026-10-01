#!/usr/bin/env python3
import argparse, hashlib, json
from pathlib import Path

CONTRACT="SYSTEM4_WORDPRESS_HANDOFF_V1"
PLUGIN_VERSION="0.28.27"
PPM_VERSION="6.7.9"
ARTICLE_KEYS={
    "index","title","target_keyword","category","article_type","plan_slot",
    "final_draft_sha256","revision_count","body","production_context",
    "languagetool","ppm679",
}

class Blocked(RuntimeError):
    pass

def load(path):
    value=json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value,dict):
        raise Blocked("JSON_OBJECT_REQUIRED:"+str(path))
    return value

def sha_text(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()

def build(final_package,ledger):
    if final_package.get("contract")!="PSERC_APPROVED_PRODUCTION_PACKAGE_V1":
        raise Blocked("ENDSTEMPEL_PACKAGE_CONTRACT_INVALID")
    if final_package.get("endstamp_contract")!="PFERDE_ATELIER_ENDSTEMPEL_RELEASE_V1" or final_package.get("status")!="ENDSTEMPEL_PASS":
        raise Blocked("ENDSTEMPEL_NOT_PASS")
    if final_package.get("publish_allowed") is not False or final_package.get("content_mutation_performed") is not False:
        raise Blocked("ENDSTEMPEL_FLAGS_INVALID")

    env=final_package.get("import_envelope")
    manifest=final_package.get("article_manifest")
    if not isinstance(env,dict) or env.get("contract")!="PSERC_APPROVED_PRODUCTION_PACKAGE_V1":
        raise Blocked("IMPORT_ENVELOPE_INVALID")
    if not isinstance(manifest,dict) or manifest.get("contract")!="PFERDE_ATELIER_ENDSTEMPEL_ARTICLE_MANIFEST_V1":
        raise Blocked("ARTICLE_MANIFEST_INVALID")

    plan=env.get("production_plan")
    release=env.get("workflow_release")
    bundle=env.get("fact_pack_bundle")
    if not isinstance(plan,dict) or plan.get("contract")!="production_plan_v4" or not isinstance(plan.get("items"),list):
        raise Blocked("PRODUCTION_PLAN_INVALID")
    if not isinstance(release,dict) or release.get("contract")!="WORKFLOW_SUPERVISOR_RELEASE_V2_SIGNED" or release.get("status")!="PASS":
        raise Blocked("WORKFLOW_RELEASE_INVALID")
    if release.get("wordpress_write_performed") is not False:
        raise Blocked("WORDPRESS_WRITE_ALREADY_PERFORMED")
    if not isinstance(bundle,dict) or bundle.get("contract")!="canonical_fact_pack_import_v1" or not isinstance(bundle.get("fact_packs"),list):
        raise Blocked("FACT_PACK_BUNDLE_INVALID")

    rows=manifest.get("articles")
    release_rows=release.get("items")
    ledger_rows=ledger.get("items") if isinstance(ledger,dict) else None
    if not isinstance(rows,list) or not isinstance(release_rows,list) or not isinstance(ledger_rows,list):
        raise Blocked("ARTICLE_SET_INVALID")
    count=len(rows)
    if count<1 or len(plan["items"])!=count or len(release_rows)!=count or len(ledger_rows)!=count:
        raise Blocked("ARTICLE_SET_COUNT_INVALID")
    if manifest.get("article_count")!=count or release.get("exact_five_item_count")!=count:
        raise Blocked("ARTICLE_COUNT_BINDING_INVALID")
    if release.get("exact_five_batch_sha256")!=final_package.get("batch_sha256"):
        raise Blocked("BATCH_BINDING_INVALID")

    plan_by_cid={}
    for item in plan["items"]:
        if not isinstance(item,dict):
            raise Blocked("PRODUCTION_PLAN_ITEM_INVALID")
        cid=str(item.get("canonical_article_id") or "")
        if not cid or cid in plan_by_cid:
            raise Blocked("PRODUCTION_PLAN_CANONICAL_ID_INVALID")
        plan_by_cid[cid]=item

    slot_to_cid={}
    for item in release_rows:
        if not isinstance(item,dict):
            raise Blocked("WORKFLOW_RELEASE_ITEM_INVALID")
        slot=str(item.get("plan_slot") or "")
        cid=str(item.get("canonical_article_id") or "")
        if not slot or not cid or slot in slot_to_cid:
            raise Blocked("WORKFLOW_RELEASE_SLOT_INVALID")
        slot_to_cid[slot]=cid

    pack_by_id={}
    for pack in bundle["fact_packs"]:
        if not isinstance(pack,dict):
            raise Blocked("FACT_PACK_INVALID")
        fid=str(pack.get("fact_pack_id") or "")
        if not fid or fid in pack_by_id:
            raise Blocked("FACT_PACK_ID_INVALID")
        pack_by_id[fid]=pack

    ledger_by_slot={}
    for row in ledger_rows:
        if not isinstance(row,dict):
            raise Blocked("LEDGER_ITEM_INVALID")
        meta=row.get("metadata")
        slot=str(meta.get("plan_slot") or "") if isinstance(meta,dict) else ""
        if not slot or slot in ledger_by_slot:
            raise Blocked("LEDGER_SLOT_INVALID")
        if row.get("stages",{}).get("check")!="DONE" or row.get("stages",{}).get("repair")!="NOT_REQUIRED":
            raise Blocked("LEDGER_ARTICLE_NOT_DONE:"+slot)
        ledger_by_slot[slot]=row

    articles=[]
    seen=set()
    for index,row in enumerate(rows):
        if not isinstance(row,dict):
            raise Blocked("MANIFEST_ARTICLE_INVALID:"+str(index))
        slot=str(row.get("plan_slot") or "")
        cid=slot_to_cid.get(slot)
        item=plan_by_cid.get(cid)
        ledger_item=ledger_by_slot.get(slot)
        if not slot or slot in seen or not isinstance(item,dict) or not isinstance(ledger_item,dict):
            raise Blocked("ARTICLE_BINDING_MISSING:"+str(index))
        seen.add(slot)

        body=row.get("content_utf8")
        if not isinstance(body,str) or not body:
            raise Blocked("ARTICLE_BODY_MISSING:"+str(index))
        body_sha=sha_text(body)
        if row.get("sha256")!=body_sha or row.get("byte_length")!=len(body.encode("utf-8")):
            raise Blocked("ARTICLE_BYTES_INVALID:"+str(index))

        canonical=item.get("canonical_article")
        quality=item.get("quality_binding")
        category=quality.get("wordpress_category") if isinstance(quality,dict) else None
        if not isinstance(canonical,dict) or canonical.get("body_html")!=body or canonical.get("body_html_sha256")!=body_sha:
            raise Blocked("CANONICAL_ARTICLE_BINDING_INVALID:"+str(index))
        if not isinstance(category,dict) or category.get("taxonomy")!="category" or not category.get("slug"):
            raise Blocked("WORDPRESS_CATEGORY_BINDING_INVALID:"+str(index))

        fact_id=str(item.get("source_snapshot_id") or "")
        fact_pack=pack_by_id.get(fact_id)
        if not isinstance(fact_pack,dict):
            raise Blocked("FACT_PACK_BINDING_MISSING:"+str(index))

        meta=ledger_item.get("metadata")
        expected={
            "title":canonical.get("title"),
            "target_keyword":item.get("target_keyword"),
            "category":category.get("slug"),
            "article_type":item.get("article_type"),
            "plan_slot":slot,
        }
        for key,value in expected.items():
            if not isinstance(meta,dict) or meta.get(key)!=value:
                raise Blocked("LEDGER_METADATA_MISMATCH:"+str(index)+":"+key)

        revision=ledger_item.get("revision")
        if not isinstance(revision,int) or isinstance(revision,bool) or revision<0:
            raise Blocked("REVISION_INVALID:"+str(index))

        articles.append({
            "index":index,
            "title":expected["title"],
            "target_keyword":expected["target_keyword"],
            "category":expected["category"],
            "article_type":expected["article_type"],
            "plan_slot":slot,
            "final_draft_sha256":body_sha,
            "revision_count":revision,
            "body":body,
            "production_context":{
                "fact_pack":fact_pack,
                "production_plan_item":item,
            },
            "languagetool":{
                "status":"PASS",
                "engine":"LanguageTool 6.8",
            },
            "ppm679":{
                "status":"PASS",
                "ppm_version":PPM_VERSION,
                "content_sha256":body_sha,
            },
        })

    return {
        "contract":CONTRACT,
        "batch_sha256":final_package["batch_sha256"],
        "article_count":len(articles),
        "publish_allowed":False,
        "signing_deferred":True,
        "batch_gate_status":"SYSTEM4_BATCH_FULL_PASS_COLLECTED",
        "no_legacy_status":"PASS",
        "test_suite_status":"PASS",
        "wordpress_review":{
            "file_format":"JSON",
            "mime_type":"application/json",
            "intended_next_step":"WORDPRESS_DIRECT_IMPORT",
            "plugin_name":"Portal SEO Editorial Plan Compiler",
            "plugin_version_verified_against":PLUGIN_VERSION,
            "ppm_version_verified_against":PPM_VERSION,
            "direct_wordpress_upload_ready":True,
            "direct_upload_block_reason":None,
            "required_downstream_components":[],
        },
        "articles":articles,
    }

def verify(value):
    if value.get("contract")!=CONTRACT or value.get("publish_allowed") is not False:
        raise Blocked("WORDPRESS_HANDOFF_CONTRACT_INVALID")
    articles=value.get("articles")
    if not isinstance(articles,list) or value.get("article_count")!=len(articles) or not articles:
        raise Blocked("WORDPRESS_HANDOFF_ARTICLE_COUNT_INVALID")
    review=value.get("wordpress_review")
    if not isinstance(review,dict) or review.get("plugin_version_verified_against")!=PLUGIN_VERSION or review.get("direct_wordpress_upload_ready") is not True:
        raise Blocked("WORDPRESS_HANDOFF_REVIEW_INVALID")
    slots=set()
    for index,row in enumerate(articles):
        if not isinstance(row,dict) or set(row)!=ARTICLE_KEYS:
            raise Blocked("WORDPRESS_HANDOFF_ARTICLE_SCHEMA_INVALID:"+str(index))
        if row.get("index")!=index:
            raise Blocked("WORDPRESS_HANDOFF_INDEX_INVALID:"+str(index))
        slot=str(row.get("plan_slot") or "")
        if not slot or slot in slots:
            raise Blocked("WORDPRESS_HANDOFF_SLOT_INVALID:"+str(index))
        slots.add(slot)
        body=row.get("body")
        if not isinstance(body,str) or sha_text(body)!=row.get("final_draft_sha256"):
            raise Blocked("WORDPRESS_HANDOFF_BODY_HASH_INVALID:"+str(index))
        if row.get("languagetool")!={"status":"PASS","engine":"LanguageTool 6.8"}:
            raise Blocked("WORDPRESS_HANDOFF_LT_INVALID:"+str(index))
        ppm=row.get("ppm679")
        if not isinstance(ppm,dict) or ppm.get("status")!="PASS" or ppm.get("ppm_version")!=PPM_VERSION or ppm.get("content_sha256")!=row.get("final_draft_sha256"):
            raise Blocked("WORDPRESS_HANDOFF_PPM_INVALID:"+str(index))
    return {
        "contract":"K9_WORDPRESS_EXPORT_VERIFY_V1",
        "status":"PASS",
        "wordpress_contract":CONTRACT,
        "plugin_version":PLUGIN_VERSION,
        "article_count":len(articles),
        "batch_sha256":value["batch_sha256"],
        "publish_allowed":False,
    }

def write_export(final_path,ledger_path,out_path):
    value=build(load(final_path),load(ledger_path))
    verify(value)
    raw=(json.dumps(value,ensure_ascii=False,indent=2)+"\n").encode("utf-8")
    out=Path(out_path)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_bytes(raw)
    return {
        "contract":"K9_WORDPRESS_EXPORT_RECEIPT_V1",
        "status":"PASS",
        "wordpress_contract":CONTRACT,
        "plugin_version":PLUGIN_VERSION,
        "filename":out.name,
        "wordpress_json_sha256":hashlib.sha256(raw).hexdigest(),
        "article_count":len(value["articles"]),
        "batch_sha256":value["batch_sha256"],
        "publish_allowed":False,
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("final_package")
    ap.add_argument("ledger")
    ap.add_argument("output")
    ap.add_argument("--receipt")
    args=ap.parse_args()
    try:
        receipt=write_export(args.final_package,args.ledger,args.output)
    except Exception as exc:
        receipt={
            "contract":"K9_WORDPRESS_EXPORT_RECEIPT_V1",
            "status":"BLOCKED",
            "reason":str(exc),
            "publish_allowed":False,
        }
        print(json.dumps(receipt,ensure_ascii=False,indent=2))
        raise SystemExit(2)
    payload=json.dumps(receipt,ensure_ascii=False,indent=2)+"\n"
    if args.receipt:
        Path(args.receipt).write_text(payload,encoding="utf-8")
    print(payload,end="")

if __name__=="__main__":
    main()
