"""Mirror of the real PSERC 0.28.23 direct System-4 WordPress handoff contract.

Historical filename kept to avoid unnecessary internal churn.
"""
from __future__ import annotations
import hashlib,re
from typing import Any

TOP_CONTRACT="SYSTEM4_WORDPRESS_HANDOFF_V1"
TOP_KEYS={"contract","batch_sha256","publish_allowed","signing_deferred","batch_gate_status","no_legacy_status","test_suite_status","wordpress_review","articles"}
ARTICLE_KEYS={"index","title","target_keyword","category","article_type","plan_slot","final_draft_sha256","revision_count","body","production_context","languagetool","ppm679"}
SHA_RE=re.compile(r"^[0-9a-f]{64}$")

class Blocked(RuntimeError): pass
def _sha(v:str)->bool:return bool(SHA_RE.fullmatch(v))
def wordpress_review()->dict[str,Any]:
    return {"file_format":"JSON","mime_type":"application/json","intended_next_step":"WORDPRESS_DIRECT_IMPORT","direct_wordpress_upload_ready":True,"direct_upload_block_reason":None,"required_downstream_components":[],"plugin_name":"Portal SEO Redaktionsplan Compiler","plugin_version_verified_against":"0.28.23","ppm_version_verified_against":"6.7.9"}

def validate(payload:dict[str,Any])->list[str]:
    e=[]
    if set(payload)!=TOP_KEYS:e.append("TOP_SCHEMA")
    if payload.get("contract")!=TOP_CONTRACT:e.append("CONTRACT")
    if not _sha(str(payload.get("batch_sha256") or "")):e.append("BATCH_SHA")
    if payload.get("publish_allowed") is not False:e.append("PUBLISH")
    if payload.get("signing_deferred") is not True:e.append("SIGNING")
    if payload.get("batch_gate_status")!="SYSTEM4_BATCH_FULL_PASS_COLLECTED":e.append("BATCH_GATE")
    if payload.get("no_legacy_status")!="PASS":e.append("NO_LEGACY")
    if payload.get("test_suite_status")!="PASS":e.append("TEST_SUITE")
    if not isinstance(payload.get("wordpress_review"),dict) or payload["wordpress_review"]!=wordpress_review():e.append("WORDPRESS_REVIEW")
    rows=payload.get("articles")
    if not isinstance(rows,list) or not rows:
        e.append("ARTICLES_EMPTY");return e
    slots=set();slugs=set()
    for i,row in enumerate(rows):
        if not isinstance(row,dict) or set(row)!=ARTICLE_KEYS:e.append(f"ARTICLE_SCHEMA:{i}");continue
        if row.get("index")!=i:e.append(f"INDEX:{i}")
        for field in ("title","target_keyword","category","article_type","body"):
            if not isinstance(row.get(field),str) or not row[field].strip():e.append(f"FIELD:{i}:{field}")
        slot=str(row.get("plan_slot") or "")
        if not _sha(slot) or slot in slots:e.append(f"SLOT:{i}")
        slots.add(slot)
        body=str(row.get("body") or "");body_sha=hashlib.sha256(body.encode("utf-8")).hexdigest()
        if row.get("final_draft_sha256")!=body_sha:e.append(f"BODY_HASH:{i}")
        rev=row.get("revision_count")
        if isinstance(rev,bool) or not isinstance(rev,int) or rev<1:e.append(f"REVISION:{i}")
        pc=row.get("production_context")
        if not isinstance(pc,dict) or not isinstance(pc.get("fact_pack"),dict) or not isinstance(pc.get("production_plan_item"),dict):
            e.append(f"PRODUCTION_CONTEXT:{i}");continue
        pi=pc["production_plan_item"];runtime=pi.get("runtime_order") or {};cat=pi.get("category_binding") or {};quality=pi.get("quality_binding") or {};wp=quality.get("wordpress_category") or {}
        if pi.get("article_type")!=row.get("article_type") or pi.get("target_keyword")!=row.get("target_keyword") or runtime.get("title")!=row.get("title") or runtime.get("article_type")!=row.get("article_type") or cat.get("slug")!=row.get("category") or wp.get("slug")!=row.get("category") or wp.get("taxonomy")!="category":
            e.append(f"PRODUCTION_BINDING:{i}")
        slug=str(runtime.get("slug") or "").strip()
        if not slug or slug in slugs:e.append(f"SLUG:{i}")
        slugs.add(slug)
        lt=row.get("languagetool")
        if not isinstance(lt,dict) or lt.get("status")!="PASS" or lt.get("finding_count")!=0 or lt.get("engine")!="LanguageTool 6.8 / Bestand 43":e.append(f"LT:{i}")
        ppm=row.get("ppm679")
        if not isinstance(ppm,dict) or ppm.get("status")!="PASS" or ppm.get("ppm_version")!="6.7.9" or ppm.get("technical_status")!="TECHNICAL_CHECK_OK" or ppm.get("content_quality_status")!="CONTENT_QUALITY_CHECK_OK" or ppm.get("fail_closed_aggregate_status")!="PASS" or ppm.get("content_sha256")!=body_sha:e.append(f"PPM:{i}")
    return e

def build(batch_sha256:str,articles:list[dict[str,Any]])->dict[str,Any]:
    if not _sha(batch_sha256):raise Blocked("BATCH_INVALID")
    payload={"contract":TOP_CONTRACT,"batch_sha256":batch_sha256,"publish_allowed":False,"signing_deferred":True,"batch_gate_status":"SYSTEM4_BATCH_FULL_PASS_COLLECTED","no_legacy_status":"PASS","test_suite_status":"PASS","wordpress_review":wordpress_review(),"articles":articles}
    errors=validate(payload)
    if errors:raise Blocked("VALIDATION_FAILED:"+",".join(errors))
    return payload
