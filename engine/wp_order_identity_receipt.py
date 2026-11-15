"""Single technical identity source: the existing WordPress order registry.

No editorial or text decision. K0's writing, validation and publish locks remain
unchanged. Only WordPress-issued order IDs are valid technical identities.
"""
from __future__ import annotations
import hashlib
import json
import re

CONTRACT = "WP_K0_SOURCE_RECEIPT_V1"
FIVE = ("title", "target_keyword", "category", "article_type", "plan_slot")

class Blocked(RuntimeError):
    pass

def stable_sha(obj):
    return hashlib.sha256(json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(",", ":")).encode("utf-8")).hexdigest()

def _article_id(site, order_id):
    if not isinstance(site,str) or not re.fullmatch(r"[a-z0-9.-]+",site) or not isinstance(order_id,str) or not re.fullmatch(r"TXE-[a-f0-9]{32}",order_id):
        raise Blocked("WP_ORDER_ID_INVALID")
    return "article:"+hashlib.sha256(("texterstellung-k0-v1|"+site+"|"+order_id).encode()).hexdigest()[:24]

def _slot(article_id):
    return hashlib.sha256(("pserc-plan-slot-v2|"+article_id).encode()).hexdigest()

def inspect(receipt):
    if not isinstance(receipt,dict) or receipt.get("contract")!=CONTRACT or receipt.get("source")!="CENTRAL_WORDPRESS_ORDER_REGISTRY" or receipt.get("publish_allowed") is not False:
        raise Blocked("WP_RECEIPT_CONTRACT_INVALID")
    h=receipt.get("manifest_sha256")
    if not isinstance(h,str) or stable_sha({k:v for k,v in receipt.items() if k!="manifest_sha256"})!=h:
        raise Blocked("WP_RECEIPT_HASH_INVALID")
    source_batch=receipt.get("next_textmachine_metadata_batch")
    from .k0_portal_resolver import validate_intake
    try:
        items=validate_intake(source_batch)
    except Exception as exc:
        raise Blocked("WP_RECEIPT_SOURCE_BATCH_INVALID:"+str(exc)) from exc
    detail=receipt.get("items")
    if not isinstance(detail,list) or len(detail)!=len(items):
        raise Blocked("WP_RECEIPT_COUNT_MISMATCH")
    site=receipt.get("site_host")
    profiles={}
    article_ids={}
    seen_orders=set()
    for row,record in zip(items,detail):
        if not isinstance(record,dict) or set(record)!={"metadata_binding","order_id","article_id","search_intent"}:
            raise Blocked("WP_RECEIPT_ITEM_FIELDS_INVALID")
        if record["metadata_binding"]!=row or set(record["metadata_binding"])!=set(FIVE):
            raise Blocked("WP_RECEIPT_METADATA_DRIFT")
        oid=record["order_id"]
        aid=_article_id(site,oid)
        slot=row["plan_slot"]
        if record["article_id"]!=aid or _slot(aid)!=slot or slot in article_ids or oid in seen_orders:
            raise Blocked("WP_RECEIPT_ORDER_IDENTITY_MISMATCH")
        intent=record["search_intent"]
        if not isinstance(intent,str) or not intent.strip():
            raise Blocked("WP_RECEIPT_APPROVED_INTENT_MISSING")
        article_ids[slot]=aid
        profiles[slot]={"search_intent":intent,"profile_sha256":stable_sha({"original_wp_order_id":oid,"article_id":aid,"search_intent":intent})}
        seen_orders.add(oid)
    return source_batch,profiles,article_ids

def resolve_current_intake(intake,receipt):
    source, _, ids=inspect(receipt)
    from .k0_portal_resolver import validate_intake
    items=validate_intake(intake)
    original={row["plan_slot"]:row for row in source["items"]}
    result={}
    for row in items:
        slot=row["plan_slot"]
        if slot not in original or row!=original[slot]:
            raise Blocked("WP_RECEIPT_CURRENT_INTAKE_NOT_SOURCE")
        result[slot]=ids[slot]
    return {"contract":"K10_CANONICAL_ARTICLE_BINDINGS_V1","status":"PASS","bindings":result}
