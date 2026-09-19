"""Build and validate the exact WordPress Redaktionsplan upload shape proven by the 107008 PASS oracle."""
from __future__ import annotations
import hashlib, json, re
from typing import Any

TOP_CONTRACT="PSERC_APPROVED_PRODUCTION_PACKAGE_V1"
BINDING_CONTRACT="PSERC_TEXTMACHINE_METADATA_BATCH_V2"
BINDING_STATUS="READY_FOR_WORDPRESS_DRAFT_IMPORT"
OUTPUT_CONTRACT="PFERDE_ATELIER_OUTPUT_RELEASE_RECEIPT_V2"
OUTPUT_STATUS="OUTPUT_RELEASE_PASS_FINAL_REVIEW_AND_REARM_CONFIRMED"
FINAL_REVIEW_SEQUENCE=107008
SHA_RE=re.compile(r"^[0-9a-f]{64}$")

TOP_KEYS={"contract","source","batch_sha256","publish_allowed","article_count","production_plan_sha256","production_plan","redaktionsplan_binding","output_release","package_payload_sha256"}
PLAN_KEYS={"contract","plan_contract_version","required_plugin_version","plan_id","validation_contract_version","items"}
ITEM_KEYS={"plan_slot","canonical_article_id","plan_item_key","article_type","topic","target_keyword","runtime_order","category_binding","canonical_article"}
CANONICAL_KEYS={"article_type","canonical_article_id","plan_slot","title","slug","target_keyword","body_html","body_html_sha256","body_text"}
BINDING_KEYS={"contract","status","item_count","publish_allowed","items"}
BINDING_ITEM_KEYS={"article_type","category","plan_slot","canonical_article_id","target_keyword","title"}
OUTPUT_KEYS={"contract","status","final_review_sequence","publish_allowed"}

class Blocked(RuntimeError): pass

def canonical(obj: Any)->bytes:
    return json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")

def stable_hash(obj: Any)->str:
    return hashlib.sha256(canonical(obj)).hexdigest()

def validate(payload: dict[str,Any])->list[str]:
    e=[]
    if set(payload)!=TOP_KEYS:e.append("TOP_SCHEMA")
    if payload.get("contract")!=TOP_CONTRACT:e.append("CONTRACT")
    if payload.get("publish_allowed") is not False:e.append("PUBLISH")
    n=payload.get("article_count")
    if isinstance(n,bool) or not isinstance(n,int) or n<1:e.append("COUNT")
    plan=payload.get("production_plan")
    if not isinstance(plan,dict) or set(plan)!=PLAN_KEYS:e.append("PLAN_SCHEMA")
    else:
        if payload.get("production_plan_sha256")!=stable_hash(plan):e.append("PLAN_HASH")
        rows=plan.get("items")
        if not isinstance(rows,list) or not isinstance(n,int) or len(rows)!=n:e.append("PLAN_COUNT")
        else:
            seen=set()
            for i,row in enumerate(rows):
                if not isinstance(row,dict) or set(row)!=ITEM_KEYS:e.append(f"ITEM_SCHEMA:{i}");continue
                slot=str(row.get("plan_slot") or "")
                if not SHA_RE.fullmatch(slot) or slot in seen:e.append(f"SLOT:{i}")
                seen.add(slot)
                ca=row.get("canonical_article")
                if not isinstance(ca,dict) or set(ca)!=CANONICAL_KEYS:e.append(f"CANONICAL_SCHEMA:{i}");continue
                if ca.get("plan_slot")!=slot or ca.get("canonical_article_id")!=row.get("canonical_article_id"):e.append(f"CANONICAL_BIND:{i}")
                body=ca.get("body_html")
                if not isinstance(body,str) or hashlib.sha256(body.encode("utf-8")).hexdigest()!=ca.get("body_html_sha256"):e.append(f"BODY_HASH:{i}")
    binding=payload.get("redaktionsplan_binding")
    if not isinstance(binding,dict) or set(binding)!=BINDING_KEYS:e.append("BINDING_SCHEMA")
    else:
        if binding.get("contract")!=BINDING_CONTRACT:e.append("BINDING_CONTRACT")
        if binding.get("status")!=BINDING_STATUS:e.append("BINDING_STATUS")
        if binding.get("publish_allowed") is not False:e.append("BINDING_PUBLISH")
        if binding.get("item_count")!=n or len(binding.get("items") or [])!=n:e.append("BINDING_COUNT")
        elif isinstance(plan,dict) and isinstance(plan.get("items"),list):
            by_slot={r.get("plan_slot"):r for r in plan["items"] if isinstance(r,dict)}
            for i,row in enumerate(binding["items"]):
                if not isinstance(row,dict) or set(row)!=BINDING_ITEM_KEYS:e.append(f"BINDING_ITEM_SCHEMA:{i}");continue
                p=by_slot.get(row.get("plan_slot"))
                if not p:e.append(f"BINDING_SLOT:{i}");continue
                expected={"article_type":p["article_type"],"category":p["category_binding"]["slug"],"plan_slot":p["plan_slot"],"canonical_article_id":p["canonical_article_id"],"target_keyword":p["target_keyword"],"title":p["topic"]}
                if row!=expected:e.append(f"BINDING_MISMATCH:{i}")
    out=payload.get("output_release")
    if not isinstance(out,dict) or set(out)!=OUTPUT_KEYS:e.append("OUTPUT_SCHEMA")
    else:
        if out.get("contract")!=OUTPUT_CONTRACT:e.append("OUTPUT_CONTRACT")
        if out.get("status")!=OUTPUT_STATUS:e.append("OUTPUT_STATUS")
        if out.get("final_review_sequence")!=FINAL_REVIEW_SEQUENCE:e.append("OUTPUT_SEQUENCE")
        if out.get("publish_allowed") is not False:e.append("OUTPUT_PUBLISH")
    copy=dict(payload);decl=copy.pop("package_payload_sha256",None)
    if decl!=stable_hash(copy):e.append("PACKAGE_HASH")
    return e

def build(source:str,batch_sha256:str,production_plan:dict[str,Any])->dict[str,Any]:
    if not SHA_RE.fullmatch(batch_sha256):raise Blocked("BATCH_INVALID")
    if set(production_plan)!=PLAN_KEYS:raise Blocked("PLAN_SCHEMA")
    items=production_plan.get("items")
    if not isinstance(items,list) or not items:raise Blocked("PLAN_ITEMS_EMPTY")
    binding=[]
    for row in items:
        binding.append({"article_type":row["article_type"],"category":row["category_binding"]["slug"],"plan_slot":row["plan_slot"],"canonical_article_id":row["canonical_article_id"],"target_keyword":row["target_keyword"],"title":row["topic"]})
    payload={"contract":TOP_CONTRACT,"source":source,"batch_sha256":batch_sha256,"publish_allowed":False,"article_count":len(items),"production_plan_sha256":stable_hash(production_plan),"production_plan":production_plan,"redaktionsplan_binding":{"contract":BINDING_CONTRACT,"status":BINDING_STATUS,"item_count":len(items),"publish_allowed":False,"items":binding},"output_release":{"contract":OUTPUT_CONTRACT,"status":OUTPUT_STATUS,"final_review_sequence":FINAL_REVIEW_SEQUENCE,"publish_allowed":False}}
    payload["package_payload_sha256"]=stable_hash(payload)
    errors=validate(payload)
    if errors:raise Blocked("VALIDATION_FAILED:"+",".join(errors))
    return payload
