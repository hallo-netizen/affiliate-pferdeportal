#!/usr/bin/env python3
import csv
import io
import json
import urllib.request
from functools import lru_cache

CENTRAL_CATEGORY_URL = (
    "https://raw.githubusercontent.com/hallo-netizen/affiliate-pferdeportal/"
    "category-integration-template-source-readonly-20260923/"
    "CATEGORY_INTEGRATION_HOBBYRAUM/PFERDEPORTAL_KATEGORIEN/KATEGORIEN.tsv"
)
PORTAL_STRUCTURE_URL = (
    "https://raw.githubusercontent.com/hallo-netizen/affiliate-pferdeportal/"
    "category-integration-template-source-readonly-20260923/"
    "release/affiliate-zentrale/current/affiliate-portal-router/assets/portal-structure-v279.json"
)
REQUIRED_CENTRAL_COLUMNS = {"term_id","slug","name","parent_slug"}
REQUIRED_PORTAL_FIELDS = {
    "category_slug","category_name","theme","product_slug","product",
    "main_slug","main_hub","hub_slug","hub","path"
}

class CategorySourceError(RuntimeError):
    pass

def _fetch_text(url):
    request=urllib.request.Request(url,headers={"User-Agent":"K9-central-category-reader/1"})
    try:
        with urllib.request.urlopen(request,timeout=30) as response:
            raw=response.read()
    except Exception as exc:
        raise CategorySourceError("CENTRAL_CATEGORY_SOURCE_UNAVAILABLE") from exc
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise CategorySourceError("CENTRAL_CATEGORY_SOURCE_ENCODING_INVALID") from exc

def _parse_central(text):
    reader=csv.DictReader(io.StringIO(text),delimiter="\t")
    if set(reader.fieldnames or []) != REQUIRED_CENTRAL_COLUMNS:
        raise CategorySourceError("CENTRAL_CATEGORY_HEADER_INVALID")
    by_slug={}
    for row in reader:
        slug=str(row.get("slug") or "").strip()
        name=str(row.get("name") or "").strip()
        term_id=str(row.get("term_id") or "").strip()
        if not slug or not name or not term_id:
            raise CategorySourceError("CENTRAL_CATEGORY_ROW_INVALID")
        if slug in by_slug:
            raise CategorySourceError("CENTRAL_CATEGORY_DUPLICATE:"+slug)
        by_slug[slug]=dict(row)
    if not by_slug:
        raise CategorySourceError("CENTRAL_CATEGORY_SOURCE_EMPTY")
    return by_slug

def _parse_portal(data):
    categories=data.get("categories") if isinstance(data,dict) else None
    if not isinstance(categories,list) or not categories:
        raise CategorySourceError("PORTAL_STRUCTURE_INVALID")
    by_slug={}
    for row in categories:
        if not isinstance(row,dict):
            continue
        slug=str(row.get("category_slug") or "").strip()
        if not slug:
            continue
        if slug in by_slug:
            raise CategorySourceError("PORTAL_STRUCTURE_DUPLICATE:"+slug)
        by_slug[slug]=row
    return by_slug

@lru_cache(maxsize=1)
def _live_sources():
    central=_parse_central(_fetch_text(CENTRAL_CATEGORY_URL))
    try:
        portal=json.loads(_fetch_text(PORTAL_STRUCTURE_URL))
    except json.JSONDecodeError as exc:
        raise CategorySourceError("PORTAL_STRUCTURE_JSON_INVALID") from exc
    return central,_parse_portal(portal)

def _resolve(metadata, central, portal):
    category=str(metadata.get("category") or "").strip()
    article_type=str(metadata.get("article_type") or "").strip()
    if not category:
        raise CategorySourceError("CENTRAL_CATEGORY_INPUT_MISSING")
    c=central.get(category)
    if not isinstance(c,dict):
        raise CategorySourceError("CENTRAL_CATEGORY_MISSING:"+category)
    p=portal.get(category)
    if not isinstance(p,dict):
        raise CategorySourceError("CENTRAL_CATEGORY_PORTAL_CONTEXT_MISSING:"+category)
    missing=[key for key in REQUIRED_PORTAL_FIELDS if not str(p.get(key) or "").strip()]
    if missing:
        raise CategorySourceError("CENTRAL_CATEGORY_PORTAL_FIELDS_MISSING:"+category+":"+",".join(sorted(missing)))
    if str(c.get("name") or "").strip() != str(p.get("category_name") or "").strip():
        raise CategorySourceError("CENTRAL_CATEGORY_NAME_DRIFT:"+category)
    if article_type != str(p.get("theme") or "").strip():
        raise CategorySourceError("CENTRAL_CATEGORY_ARTICLE_TYPE_MISMATCH:"+category)
    main_slug=str(p["main_slug"]).strip().strip("/")
    hub_slug=str(p["hub_slug"]).strip().strip("/")
    product_slug=str(p["product_slug"]).strip().strip("/")
    section_map={
        "Beratung":{"parent_category":"criteria","semantic_related":"decision"},
        "FAQ":{"parent_category":"answer","semantic_related":"details"},
        "Pflege":{"parent_category":"steps","semantic_related":"risks"},
        "Vergleich":{"parent_category":"options","semantic_related":"comparison"},
    }
    placements=section_map.get(article_type)
    if not isinstance(placements,dict):
        raise CategorySourceError("CENTRAL_CATEGORY_ARTICLE_TYPE_UNSUPPORTED:"+category+":"+article_type)
    links=[
        {"anchor":str(p["main_hub"]).strip(),"href":f"/{main_slug}/","role":"parent_category","section_id":placements["parent_category"]},
        {"anchor":str(p["hub"]).strip(),"href":f"/{main_slug}/{hub_slug}/","role":"semantic_related","section_id":placements["semantic_related"]},
        {"anchor":str(p["product"]).strip(),"href":f"/{main_slug}/{hub_slug}/{product_slug}/","role":"further_information","section_id":"further_information"},
    ]
    return {
        "portal_links":links,
        "category_source":{
            "authority":"CATEGORY_INTEGRATION_HOBBYRAUM/PFERDEPORTAL_KATEGORIEN/KATEGORIEN.tsv",
            "category_slug":category,
            "term_id":str(c["term_id"]).strip(),
            "portal_path":str(p["path"]).strip(),
        }
    }

def portal_context(metadata, central_text=None, portal_data=None):
    if central_text is None and portal_data is None:
        central,portal=_live_sources()
    elif isinstance(central_text,str) and isinstance(portal_data,dict):
        central,portal=_parse_central(central_text),_parse_portal(portal_data)
    else:
        raise CategorySourceError("CENTRAL_CATEGORY_TEST_SOURCE_INCOMPLETE")
    return _resolve(metadata,central,portal)

def validate_batch(metadata_rows, central_text=None, portal_data=None):
    if not isinstance(metadata_rows,list) or not metadata_rows:
        raise CategorySourceError("CENTRAL_CATEGORY_BATCH_EMPTY")
    if central_text is None and portal_data is None:
        central,portal=_live_sources()
    elif isinstance(central_text,str) and isinstance(portal_data,dict):
        central,portal=_parse_central(central_text),_parse_portal(portal_data)
    else:
        raise CategorySourceError("CENTRAL_CATEGORY_TEST_SOURCE_INCOMPLETE")
    resolved=[_resolve(row,central,portal) for row in metadata_rows]
    return {"status":"PASS","validated":len(resolved),"categories":[r["category_source"]["category_slug"] for r in resolved]}
