from __future__ import annotations

import copy
import json
import math
import re
import sys
from pathlib import Path

ARTICLE_TYPE = "Eigenschaftssieger"
RESEARCH_CONTRACT = "K0_PRODUCT_PROPERTY_RESEARCH_V1"
STORE_CONTRACT = "K0_PRODUCT_PROPERTY_STORE_V1"
SEARCH_INTENT = "PRODUCT_PROPERTY_SUPERLATIVE"
DIRECTIONS = {"MIN", "MAX"}
MIN_CANDIDATES = 4

class Blocked(RuntimeError):
    pass

def _load(path):
    value=json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value,dict):
        raise Blocked("JSON_OBJECT_REQUIRED:"+str(path))
    return value

def _text(value, code):
    value=str(value or "").strip()
    if not value:
        raise Blocked(code)
    return value

def _product_key(row):
    key=_text(row.get("product_key"),"PROPERTY_PRODUCT_KEY_MISSING")
    if not re.fullmatch(r"[A-Za-z0-9._:-]{3,160}",key):
        raise Blocked("PROPERTY_PRODUCT_KEY_INVALID:"+key)
    return key

def validate_packet(identity, packet):
    if str(identity.get("article_type") or "")!=ARTICLE_TYPE:
        return {"contract":RESEARCH_CONTRACT,"status":"NOT_REQUIRED","article_type":str(identity.get("article_type") or "")}

    if not isinstance(packet,dict) or packet.get("contract")!=RESEARCH_CONTRACT or packet.get("status")!="PASS":
        raise Blocked("PROPERTY_RESEARCH_PACKET_REQUIRED")
    if packet.get("ranking_independent_of_affiliate") is not True:
        raise Blocked("PROPERTY_RESEARCH_AFFILIATE_INDEPENDENCE_REQUIRED")

    prop=packet.get("property")
    if not isinstance(prop,dict):
        raise Blocked("PROPERTY_RESEARCH_PROPERTY_MISSING")
    pkey=_text(prop.get("key"),"PROPERTY_RESEARCH_KEY_MISSING")
    label=_text(prop.get("label"),"PROPERTY_RESEARCH_LABEL_MISSING")
    unit=_text(prop.get("unit"),"PROPERTY_RESEARCH_UNIT_MISSING")
    direction=_text(prop.get("direction"),"PROPERTY_RESEARCH_DIRECTION_MISSING").upper()
    if direction not in DIRECTIONS:
        raise Blocked("PROPERTY_RESEARCH_DIRECTION_INVALID:"+direction)

    rows=packet.get("candidates")
    if not isinstance(rows,list) or len(rows)<MIN_CANDIDATES:
        raise Blocked("PROPERTY_RESEARCH_MINIMUM_COMPARABLE_CANDIDATES:"+str(len(rows) if isinstance(rows,list) else 0))

    candidates=[]
    keys=set()
    for idx,row in enumerate(rows):
        if not isinstance(row,dict):
            raise Blocked("PROPERTY_RESEARCH_CANDIDATE_INVALID:"+str(idx))
        product_key=_product_key(row)
        if product_key in keys:
            raise Blocked("PROPERTY_RESEARCH_PRODUCT_DUPLICATE:"+product_key)
        keys.add(product_key)
        brand=_text(row.get("brand"),"PROPERTY_RESEARCH_BRAND_MISSING:"+str(idx))
        model=_text(row.get("model"),"PROPERTY_RESEARCH_MODEL_MISSING:"+str(idx))
        value=row.get("value")
        if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(float(value)):
            raise Blocked("PROPERTY_RESEARCH_VALUE_INVALID:"+str(idx))
        source_title=_text(row.get("source_title"),"PROPERTY_RESEARCH_SOURCE_TITLE_MISSING:"+str(idx))
        source_url=_text(row.get("source_url"),"PROPERTY_RESEARCH_SOURCE_URL_MISSING:"+str(idx))
        if not source_url.startswith(("https://","http://")):
            raise Blocked("PROPERTY_RESEARCH_SOURCE_URL_INVALID:"+str(idx))
        ids=row.get("identifiers") if isinstance(row.get("identifiers"),dict) else {}
        identifiers={k:str(v).strip() for k,v in ids.items() if k in {"ean","gtin","mpn","sku"} and str(v).strip()}
        candidates.append({
            "product_key":product_key,
            "brand":brand,
            "model":model,
            "value":float(value),
            "source_title":source_title,
            "source_url":source_url,
            "identifiers":identifiers,
        })

    winner=packet.get("winner")
    if not isinstance(winner,dict):
        raise Blocked("PROPERTY_RESEARCH_WINNER_MISSING")
    winner_key=_product_key(winner)
    match=[row for row in candidates if row["product_key"]==winner_key]
    if len(match)!=1:
        raise Blocked("PROPERTY_RESEARCH_WINNER_NOT_CANDIDATE")
    winner_row=match[0]
    expected=min(row["value"] for row in candidates) if direction=="MIN" else max(row["value"] for row in candidates)
    winners=[row for row in candidates if row["value"]==expected]
    if len(winners)!=1:
        raise Blocked("PROPERTY_RESEARCH_WINNER_NOT_UNIQUE")
    if winner_row["value"]!=expected:
        raise Blocked("PROPERTY_RESEARCH_WINNER_VALUE_MISMATCH")
    if "value" in winner and float(winner["value"])!=expected:
        raise Blocked("PROPERTY_RESEARCH_DECLARED_WINNER_VALUE_MISMATCH")
    if str(winner.get("source_url") or winner_row["source_url"]).strip()!=winner_row["source_url"]:
        raise Blocked("PROPERTY_RESEARCH_WINNER_SOURCE_MISMATCH")

    return {
        "contract":RESEARCH_CONTRACT,
        "status":"PASS",
        "article_type":ARTICLE_TYPE,
        "property_key":pkey,
        "property_label":label,
        "unit":unit,
        "direction":direction,
        "candidate_count":len(candidates),
        "winner":winner_row,
        "candidates":candidates,
        "search_intent":SEARCH_INTENT,
        "ranking_independent_of_affiliate":True,
    }

def validate_context(context):
    if context.get("contract")!="K0_AUTHORING_CONTEXT_V1":
        raise Blocked("PROPERTY_CONTEXT_CONTRACT_INVALID")
    identity=context.get("identity")
    if not isinstance(identity,dict):
        raise Blocked("PROPERTY_CONTEXT_IDENTITY_MISSING")
    production=context.get("production_context")
    if not isinstance(production,dict):
        raise Blocked("PROPERTY_CONTEXT_PRODUCTION_MISSING")
    return validate_packet(identity,production.get("property_research"))

def bind_store(context, store):
    result=validate_context(context)
    if result["status"]=="NOT_REQUIRED":
        return copy.deepcopy(store),result
    if not isinstance(store,dict) or store.get("contract")!=STORE_CONTRACT:
        raise Blocked("PROPERTY_STORE_CONTRACT_INVALID")
    products=copy.deepcopy(store.get("products") if isinstance(store.get("products"),dict) else {})
    pkey=result["property_key"]
    for row in result["candidates"]:
        product=products.get(row["product_key"]) if isinstance(products.get(row["product_key"]),dict) else {}
        properties=copy.deepcopy(product.get("properties") if isinstance(product.get("properties"),dict) else {})
        properties[pkey]={
            "label":result["property_label"],
            "unit":result["unit"],
            "value":row["value"],
            "source_title":row["source_title"],
            "source_url":row["source_url"],
        }
        products[row["product_key"]]={
            "brand":row["brand"],
            "model":row["model"],
            "identifiers":row["identifiers"],
            "properties":properties,
        }
    out={
        "contract":STORE_CONTRACT,
        "status":"ACTIVE",
        "products":products,
        "publish_allowed":False,
    }
    return out,{**result,"store_status":"UPDATED"}

def main():
    try:
        if len(sys.argv)==3 and sys.argv[1]=="validate":
            result=validate_context(_load(sys.argv[2]))
            print(json.dumps(result,ensure_ascii=False,indent=2))
            return
        if len(sys.argv)==5 and sys.argv[1]=="bind":
            out,result=bind_store(_load(sys.argv[2]),_load(sys.argv[3]))
            Path(sys.argv[4]).write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
            print(json.dumps(result,ensure_ascii=False,indent=2))
            return
        raise Blocked("PROPERTY_RESEARCH_USAGE_INVALID")
    except Exception as exc:
        print(json.dumps({"contract":RESEARCH_CONTRACT,"status":"BLOCKED","reason":str(exc),"publish_allowed":False},ensure_ascii=False))
        raise SystemExit(2)

if __name__=="__main__":
    main()
