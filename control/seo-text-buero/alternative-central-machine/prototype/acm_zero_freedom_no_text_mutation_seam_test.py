#!/usr/bin/env python3
from __future__ import annotations

import base64
import copy
import hashlib
import json
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

REPO=Path(__file__).resolve().parents[4]
SOURCE=REPO/"control/startmaster0107/runtime_inbox/generations/000001/SOURCE_SNAPSHOT.json"
PACKAGE=REPO/"control/startmaster0107/runtime_inbox/generations/000001/PRODUCTION_PACKAGE.json"

BINDING_FIELDS=("title","target_keyword","category","article_type","plan_slot")
SIGNED_ITEM_FIELDS=(
    "canonical_article_id","plan_slot","title","target_keyword","category",
    "article_type","content_html","content_sha256"
)

class Blocked(RuntimeError):
    pass

def canon(obj):
    return json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")

def stable_hash(obj):
    return hashlib.sha256(canon(obj)).hexdigest()

def load(path):
    obj=json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(obj,dict): raise Blocked("JSON_OBJECT_REQUIRED")
    return obj

def current_bindings():
    src=load(SOURCE)
    batch=src.get("next_textmachine_metadata_batch")
    if not isinstance(batch,dict) or batch.get("status")!="READY_FOR_TEXTMACHINE_METADATA_INTAKE":
        raise Blocked("EDITORIAL_BATCH_NOT_READY")
    items=batch.get("items")
    if not isinstance(items,list) or not items:
        raise Blocked("EDITORIAL_ITEMS_MISSING")

    pkg=load(PACKAGE)
    release=(pkg.get("workflow_release") or {}).get("items")
    if not isinstance(release,list) or not release:
        raise Blocked("WORKFLOW_RELEASE_ITEMS_MISSING")
    cid_by_slot={}
    for row in release:
        if not isinstance(row,dict): continue
        slot=str(row.get("plan_slot") or "")
        cid=str(row.get("canonical_article_id") or "")
        if slot and cid: cid_by_slot[slot]=cid

    out=[]
    for src_item in items:
        if set(src_item)!=set(BINDING_FIELDS):
            raise Blocked("EDITORIAL_ITEM_SCHEMA_DRIFT")
        slot=str(src_item["plan_slot"])
        cid=cid_by_slot.get(slot)
        if not cid:
            raise Blocked("EDITORIAL_SLOT_NOT_BOUND_TO_CANONICAL_ID")
        out.append({**src_item,"canonical_article_id":cid})
    return src,batch,out

def validate_pre_sign(editorial:dict,candidate:dict):
    if set(candidate)!=set(SIGNED_ITEM_FIELDS):
        raise Blocked("SIGNED_ITEM_SCHEMA_INVALID")
    for f in BINDING_FIELDS:
        if str(candidate.get(f))!=str(editorial.get(f)):
            raise Blocked("EDITORIAL_METADATA_DRIFT:"+f)
    if str(candidate.get("canonical_article_id"))!=str(editorial.get("canonical_article_id")):
        raise Blocked("CANONICAL_ARTICLE_ID_DRIFT")
    html=candidate.get("content_html")
    if not isinstance(html,str) or not html:
        raise Blocked("CONTENT_HTML_MISSING")
    actual=hashlib.sha256(html.encode("utf-8")).hexdigest()
    if candidate.get("content_sha256")!=actual:
        raise Blocked("CONTENT_HASH_MISMATCH")
    return True

def sign_batch(batch_sha:str,items:list[dict],private):
    envelope={
      "contract":"PFERDE_ATELIER_ACM_SIGNED_ARTICLE_BATCH_V1",
      "status":"ENDSTEMPEL_PASS",
      "batch_sha256":batch_sha,
      "article_count":len(items),
      "articles":items,
      "chat_execution_authority":"NONE",
      "chat_output_authority":"NONE",
      "domain_logic_authority":"NONE",
      "quality_authority":"NONE",
      "route_selectable":False,
      "validator_selectable":False,
      "worker_selectable":False,
      "publish_allowed":False,
      "content_mutation_performed":False,
    }
    payload_hash=stable_hash(envelope)
    raw_pub=private.public_key().public_bytes(
      encoding=serialization.Encoding.Raw,
      format=serialization.PublicFormat.Raw,
    )
    envelope["package_payload_sha256"]=payload_hash
    envelope["signature_algorithm"]="ED25519"
    envelope["public_key_b64"]=base64.b64encode(raw_pub).decode("ascii")
    envelope["public_key_sha256"]=hashlib.sha256(raw_pub).hexdigest()
    envelope["signature_b64"]=base64.b64encode(private.sign(payload_hash.encode("ascii"))).decode("ascii")
    return envelope

def verify_wp_input(envelope:dict,public):
    required={
      "contract","status","batch_sha256","article_count","articles",
      "chat_execution_authority","chat_output_authority","domain_logic_authority",
      "quality_authority","route_selectable","validator_selectable","worker_selectable",
      "publish_allowed","content_mutation_performed","package_payload_sha256",
      "signature_algorithm","public_key_b64","public_key_sha256","signature_b64"
    }
    if set(envelope)!=required:
        raise Blocked("WORDPRESS_FINAL_SCHEMA_INVALID")
    if envelope["contract"]!="PFERDE_ATELIER_ACM_SIGNED_ARTICLE_BATCH_V1":
        raise Blocked("WORDPRESS_CONTRACT_INVALID")
    if envelope["status"]!="ENDSTEMPEL_PASS":
        raise Blocked("WORDPRESS_ENDSTAMP_NOT_PASS")
    for k in ("chat_execution_authority","chat_output_authority","domain_logic_authority","quality_authority"):
        if envelope[k]!="NONE": raise Blocked("WORDPRESS_AUTHORITY_NOT_NONE:"+k)
    for k in ("route_selectable","validator_selectable","worker_selectable","publish_allowed","content_mutation_performed"):
        if envelope[k] is not False: raise Blocked("WORDPRESS_FREEDOM_OR_PUBLISH_FORBIDDEN:"+k)
    items=envelope["articles"]
    if not isinstance(items,list) or len(items)!=envelope["article_count"] or not items:
        raise Blocked("WORDPRESS_ARTICLE_COUNT_INVALID")
    for item in items:
        if set(item)!=set(SIGNED_ITEM_FIELDS):
            raise Blocked("WORDPRESS_SIGNED_ITEM_SCHEMA_INVALID")
        html=item.get("content_html")
        if hashlib.sha256(str(html).encode("utf-8")).hexdigest()!=item.get("content_sha256"):
            raise Blocked("WORDPRESS_CONTENT_HASH_MISMATCH")
    payload={k:v for k,v in envelope.items() if k not in {
      "package_payload_sha256","signature_algorithm","public_key_b64","public_key_sha256","signature_b64"
    }}
    ph=stable_hash(payload)
    if ph!=envelope["package_payload_sha256"]:
        raise Blocked("WORDPRESS_PACKAGE_HASH_MISMATCH")
    pubraw=public.public_bytes(encoding=serialization.Encoding.Raw,format=serialization.PublicFormat.Raw)
    if hashlib.sha256(pubraw).hexdigest()!=envelope["public_key_sha256"]:
        raise Blocked("WORDPRESS_PUBLIC_KEY_SHA_MISMATCH")
    if base64.b64encode(pubraw).decode("ascii")!=envelope["public_key_b64"]:
        raise Blocked("WORDPRESS_PUBLIC_KEY_MISMATCH")
    try:
        public.verify(base64.b64decode(envelope["signature_b64"]),ph.encode("ascii"))
    except Exception as exc:
        raise Blocked("WORDPRESS_SIGNATURE_INVALID") from exc
    return {
      "status":"ACM_WORDPRESS_INPUT_VERIFIED_FOR_DRAFT_ONLY",
      "articles":copy.deepcopy(items),
      "post_status":"draft",
      "publish_allowed":False,
      "content_mutation_performed":False,
    }

def must_block(fn,label):
    try:
        fn()
    except Blocked:
        return label
    raise RuntimeError("NEGATIVE_NOT_BLOCKED:"+label)

def main():
    src,batch,bindings=current_bindings()
    editorial=bindings[0]
    html="<article><p>ACM Übergabetest – unveränderte Artikelbytes.</p></article>"
    candidate={
      "canonical_article_id":editorial["canonical_article_id"],
      "plan_slot":editorial["plan_slot"],
      "title":editorial["title"],
      "target_keyword":editorial["target_keyword"],
      "category":editorial["category"],
      "article_type":editorial["article_type"],
      "content_html":html,
      "content_sha256":hashlib.sha256(html.encode("utf-8")).hexdigest(),
    }

    validate_pre_sign(editorial,candidate)
    negatives=[]

    for field in BINDING_FIELDS:
        bad=copy.deepcopy(candidate)
        bad[field]=str(bad[field])+"__DRIFT"
        negatives.append(must_block(lambda b=bad: validate_pre_sign(editorial,b),"pre_sign_"+field+"_drift"))

    bad=copy.deepcopy(candidate);bad["canonical_article_id"]="article:wrong"
    negatives.append(must_block(lambda: validate_pre_sign(editorial,bad),"pre_sign_canonical_id_drift"))

    bad=copy.deepcopy(candidate);bad["content_html"]+="X"
    negatives.append(must_block(lambda: validate_pre_sign(editorial,bad),"pre_sign_content_change_without_hash"))

    bad=copy.deepcopy(candidate);bad["unexpected_route"]="alternate"
    negatives.append(must_block(lambda: validate_pre_sign(editorial,bad),"pre_sign_extra_field_route"))

    private=Ed25519PrivateKey.generate()
    envelope=sign_batch(str(batch["batch_sha256"]),[candidate],private)
    wp=verify_wp_input(envelope,private.public_key())

    # Post-signature tampering: every editorial binding and content must fail.
    for field in ("title","target_keyword","category","article_type","plan_slot","canonical_article_id","content_html"):
        bad=copy.deepcopy(envelope)
        bad["articles"][0][field]=str(bad["articles"][0][field])+"__TAMPER"
        negatives.append(must_block(lambda b=bad: verify_wp_input(b,private.public_key()),"post_sign_"+field+"_tamper"))

    for field,value in (
      ("publish_allowed",True),
      ("route_selectable",True),
      ("validator_selectable",True),
      ("worker_selectable",True),
      ("chat_execution_authority","ALLOW"),
      ("quality_authority","CHAT"),
    ):
        bad=copy.deepcopy(envelope);bad[field]=value
        negatives.append(must_block(lambda b=bad: verify_wp_input(b,private.public_key()),"wp_"+field+"_freedom"))

    bad=copy.deepcopy(envelope);bad["new_runtime_choice"]="anything"
    negatives.append(must_block(lambda: verify_wp_input(bad,private.public_key()),"wp_unknown_extra_field"))

    # Determinism / no text mutation: verified draft input must be byte-identical.
    if wp["articles"][0]["content_html"]!=candidate["content_html"]:
        raise RuntimeError("CONTENT_MUTATED_ACROSS_SEAM")
    if hashlib.sha256(wp["articles"][0]["content_html"].encode("utf-8")).hexdigest()!=candidate["content_sha256"]:
        raise RuntimeError("CONTENT_HASH_DRIFT_ACROSS_SEAM")
    for f in ("title","target_keyword","category","article_type","plan_slot","canonical_article_id"):
        if wp["articles"][0][f]!=candidate[f]:
            raise RuntimeError("METADATA_MUTATED_ACROSS_SEAM:"+f)

    print(json.dumps({
      "status":"ACM_ZERO_FREEDOM_NO_TEXT_MUTATION_SEAM_PASS",
      "real_editorial_source_snapshot":src.get("source_snapshot_filename"),
      "real_editorial_batch_sha256":batch.get("batch_sha256"),
      "tested_real_binding":{
        k:editorial[k] for k in ("canonical_article_id","plan_slot","title","target_keyword","category","article_type")
      },
      "positive":{
        "pre_sign_editorial_binding_exact":True,
        "signed_metadata_and_content_exact":True,
        "wordpress_input_verified":True,
        "wordpress_target_status":"draft",
        "text_byte_identical_across_seam":True,
        "metadata_identical_across_seam":True,
        "new_route_choice":False,
        "new_validator_choice":False,
        "new_worker_choice":False,
        "chat_authority":"NONE",
        "quality_authority":"NONE",
        "publish_allowed":False,
      },
      "negative_tests":negatives,
      "negative_count":len(negatives),
      "content_mutation_performed":False,
      "publish_allowed":False
    },ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())

# workflow-trigger: zero-freedom-seam-v1
