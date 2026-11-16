from __future__ import annotations
import hashlib, json, re, sys
from pathlib import Path

from .html_design import validate_canonical_html, DesignBlocked
from .k0_wordpress_export import CONTRACT, ARTICLE_FIELDS

class BatchBlocked(RuntimeError): pass

def _load(path: str|Path):
    x=json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(x,dict):
        raise BatchBlocked("JSON_OBJECT_REQUIRED:"+str(path))
    return x

def _slot(article_id: str) -> str:
    return hashlib.sha256(("pserc-plan-slot-v2|"+article_id).encode("utf-8")).hexdigest()

def combine(intake: dict, singles: list[dict]) -> dict:
    items=intake.get("items")
    if intake.get("contract")!="PSERC_TEXTMACHINE_METADATA_BATCH_V2" or not isinstance(items,list) or not items:
        raise BatchBlocked("BATCH_INTAKE_INVALID")
    if intake.get("item_count")!=len(items):
        raise BatchBlocked("BATCH_ITEM_COUNT_MISMATCH")
    slots=[str(item.get("plan_slot") or "") for item in items if isinstance(item,dict)]
    if len(slots)!=len(items) or len(set(slots))!=len(items):
        raise BatchBlocked("BATCH_INTAKE_DUPLICATE_OR_INVALID")
    if len(singles)!=len(items):
        raise BatchBlocked("BATCH_SINGLE_COUNT_MISMATCH")
    batch_sha=str(intake.get("batch_sha256") or "")
    if not re.fullmatch(r"[0-9a-f]{64}",batch_sha):
        raise BatchBlocked("BATCH_SHA256_INVALID")

    rows_by_slot={}
    review=None
    for doc in singles:
        if doc.get("contract")!=CONTRACT or doc.get("article_count")!=1 or doc.get("publish_allowed") is not False:
            raise BatchBlocked("SINGLE_WORDPRESS_DOCUMENT_INVALID")
        if any(doc.get(key)!=value for key,value in (
            ("batch_gate_status","SYSTEM4_BATCH_FULL_PASS_COLLECTED"),
            ("no_legacy_status","PASS"),
            ("test_suite_status","PASS"),
        )):
            raise BatchBlocked("SINGLE_WORDPRESS_QUALITY_NOT_PASS")
        wp=doc.get("wordpress_review")
        if not isinstance(wp,dict) or any(wp.get(key)!=value for key,value in (
            ("file_format","JSON"),
            ("mime_type","application/json"),
            ("intended_next_step","WORDPRESS_DIRECT_IMPORT"),
            ("direct_wordpress_upload_ready",True),
            ("direct_upload_block_reason",None),
        )) or wp.get("required_downstream_components")!=[]:
            raise BatchBlocked("SINGLE_WORDPRESS_IMPORT_NOT_READY")
        rows=doc.get("articles")
        if not isinstance(rows,list) or len(rows)!=1 or not isinstance(rows[0],dict):
            raise BatchBlocked("SINGLE_WORDPRESS_ARTICLE_INVALID")
        row=rows[0]
        if set(row)!=set(ARTICLE_FIELDS):
            raise BatchBlocked("SINGLE_ARTICLE_FIELDS_INVALID")
        slot=str(row.get("plan_slot") or "")
        aid=str(row.get("article_id") or "")
        if not re.fullmatch(r"[0-9a-f]{64}",slot):
            raise BatchBlocked("SINGLE_PLAN_SLOT_INVALID")
        if not re.fullmatch(r"article:[0-9a-f]{24}",aid):
            raise BatchBlocked("SINGLE_ARTICLE_ID_INVALID:"+slot)
        if _slot(aid)!=slot:
            raise BatchBlocked("SINGLE_ARTICLE_ID_PLAN_SLOT_MISMATCH:"+slot)
        if slot in rows_by_slot:
            raise BatchBlocked("SINGLE_PLAN_SLOT_DUPLICATE:"+slot)

        body=str(row.get("body") or "")
        if hashlib.sha256(body.encode("utf-8")).hexdigest()!=str(row.get("final_draft_sha256") or ""):
            raise BatchBlocked("SINGLE_BODY_SHA256_MISMATCH:"+slot)
        lt=row.get("languagetool") if isinstance(row.get("languagetool"),dict) else {}
        ppm=row.get("ppm679") if isinstance(row.get("ppm679"),dict) else {}
        if lt.get("status")!="PASS" or lt.get("engine")!="LanguageTool 6.8" or lt.get("finding_count")!=0:
            raise BatchBlocked("SINGLE_LANGUAGETOOL_NOT_PASS:"+slot)
        if (ppm.get("status")!="PASS" or ppm.get("ppm_version")!="6.7.9"
            or ppm.get("technical_status")!="TECHNICAL_CHECK_OK"
            or ppm.get("content_quality_status")!="CONTENT_QUALITY_CHECK_OK"
            or ppm.get("fail_closed_aggregate_status")!="PASS"
            or ppm.get("content_sha256")!=row.get("final_draft_sha256")):
            raise BatchBlocked("SINGLE_PPM679_NOT_PASS:"+slot)
        try:
            validate_canonical_html({"article_type":str(row.get("article_type") or ""),"html":body})
        except DesignBlocked as exc:
            raise BatchBlocked("SINGLE_HTML_INVALID:"+slot+":"+str(exc)) from exc

        pc=row.get("production_context") if isinstance(row.get("production_context"),dict) else {}
        if set(pc)!={"fact_pack","production_plan_item"}:
            raise BatchBlocked("SINGLE_PRODUCTION_CONTEXT_INVALID:"+slot)
        pi=pc.get("production_plan_item") if isinstance(pc.get("production_plan_item"),dict) else {}
        if str(pi.get("canonical_article_id") or "")!=aid:
            raise BatchBlocked("SINGLE_NESTED_CANONICAL_ID_MISMATCH:"+slot)
        ca=pi.get("canonical_article") if isinstance(pi.get("canonical_article"),dict) else {}
        if ca.get("body_html")!=body or ca.get("body_html_sha256")!=row.get("final_draft_sha256"):
            raise BatchBlocked("SINGLE_CANONICAL_ARTICLE_BODY_BINDING_INVALID:"+slot)
        category=(pi.get("quality_binding") or {}).get("wordpress_category") or {}
        if (not isinstance(category,dict) or category.get("slug")!=row.get("category")
            or category.get("taxonomy")!="category" or type(category.get("id")) is not int
            or category["id"]<1):
            raise BatchBlocked("SINGLE_CATEGORY_BINDING_INVALID:"+slot)

        if review is None:
            review=dict(doc.get("wordpress_review") or {})
        rows_by_slot[slot]=row

    ordered=[]
    for idx,item in enumerate(items):
        if not isinstance(item,dict):
            raise BatchBlocked("BATCH_ITEM_INVALID:"+str(idx))
        slot=str(item.get("plan_slot") or "")
        row=rows_by_slot.get(slot)
        if row is None:
            raise BatchBlocked("BATCH_ARTICLE_MISSING:"+slot)
        for key in ("title","target_keyword","category","article_type","plan_slot"):
            if str(row.get(key) or "")!=str(item.get(key) or ""):
                raise BatchBlocked("BATCH_IDENTITY_MISMATCH:"+slot+":"+key)
        row=dict(row); row["index"]=idx
        ordered.append(row)

    if set(rows_by_slot)!=set(str(x.get("plan_slot") or "") for x in items if isinstance(x,dict)):
        raise BatchBlocked("BATCH_EXTRA_OR_MISSING_ARTICLE")
    if review is None:
        raise BatchBlocked("BATCH_WORDPRESS_REVIEW_MISSING")

    review["direct_wordpress_upload_ready"]=True
    review["direct_upload_block_reason"]=None
    return {
        "contract":CONTRACT,
        "batch_sha256":batch_sha,
        "article_count":len(ordered),
        "publish_allowed":False,
        "signing_deferred":True,
        "batch_gate_status":"SYSTEM4_BATCH_FULL_PASS_COLLECTED",
        "no_legacy_status":"PASS",
        "test_suite_status":"PASS",
        "wordpress_review":review,
        "articles":ordered,
    }

def main():
    if len(sys.argv)<4:
        raise SystemExit("usage: wordpress_batch_export.py INTAKE OUT SINGLE1 [SINGLE2 ...]")
    try:
        if Path(sys.argv[2]).name!="WORDPRESS_BATCH.json":
            raise BatchBlocked("BATCH_OUTPUT_FILENAME_INVALID")
        intake=_load(sys.argv[1]); singles=[_load(p) for p in sys.argv[3:]]
        out=combine(intake,singles)
    except (BatchBlocked,DesignBlocked) as exc:
        print(json.dumps({"contract":"K0_WORDPRESS_BATCH_EXPORT_V3","status":"BLOCKED","reason":str(exc),"publish_allowed":False},ensure_ascii=False))
        raise SystemExit(2)
    output_bytes=(json.dumps(out,ensure_ascii=False,indent=2)+"\n").encode("utf-8")
    output_path=Path(sys.argv[2])
    output_path.write_bytes(output_bytes)
    if output_path.read_bytes()!=output_bytes:
        raise BatchBlocked("BATCH_OUTPUT_WRITE_VERIFICATION_FAILED")
    print(json.dumps({"contract":"K0_WORDPRESS_BATCH_EXPORT_V3","status":"PASS","article_count":out["article_count"],"batch_sha256":out["batch_sha256"],"publish_allowed":False},ensure_ascii=False))

if __name__=="__main__":
    main()
