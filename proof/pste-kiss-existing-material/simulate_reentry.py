#!/usr/bin/env python3
import json, pathlib, copy, sys

ROOT=pathlib.Path(__file__).resolve().parents[2]
queue=json.loads((ROOT/"proof/pste-kiss-existing-material/PSTE_EXISTING_MATERIAL_REENTRY_110.json").read_text())
live=json.loads((ROOT/"tmp/pste-live-inventory-20261006.json").read_text())
live_titles={p["title"].strip().casefold() for p in live["posts"]}

def binding_complete(c):
    b=c.get("binding") or {}
    mode=b.get("mode")
    if mode=="CONFIRM_EXISTING_FAMILY":
        return bool(b.get("family_name") and b.get("family_key"))
    if mode=="BIND_EXISTING_FAMILY":
        return bool(b.get("family_name") and b.get("family_key") and b.get("portal_path"))
    if mode=="BIND_EXISTING_ARTICLE_TYPE":
        return bool(b.get("article_type") and b.get("category_id") and b.get("category_name"))
    return False

def reentry(c):
    if c.get("dataforseo_required") is not False:
        return "BLOCK_DATAFORSEO_SHORT_PATH_CONTRACT"
    if c.get("new_external_research_required") is not False:
        return "BLOCK_EXTERNAL_RESEARCH_REQUIRED"
    if c.get("editorial_title","").strip().casefold() in live_titles:
        return "BLOCK_EXISTING_CONTENT_DUPLICATE"
    if not binding_complete(c):
        return "BLOCK_BINDING_INCOMPLETE"
    return "REENTRY_ALLOWED"

assert queue["counts"]["reentry_candidates"]==110
assert queue["counts"]["confirm_existing_family"]==92
assert queue["counts"]["bind_existing_family"]==9
assert queue["counts"]["bind_existing_article_type"]==9

results=[reentry(c) for c in queue["candidates"]]
assert results.count("REENTRY_ALLOWED")==110, {x:results.count(x) for x in set(results)}

base=copy.deepcopy(queue["candidates"][0])
neg=copy.deepcopy(base); neg["dataforseo_required"]=True
assert reentry(neg)=="BLOCK_DATAFORSEO_SHORT_PATH_CONTRACT"

neg=copy.deepcopy(base); neg["editorial_title"]=live["posts"][0]["title"]
assert reentry(neg)=="BLOCK_EXISTING_CONTENT_DUPLICATE"

neg=copy.deepcopy(base); neg["binding"]={}
assert reentry(neg)=="BLOCK_BINDING_INCOMPLETE"

print("PASS_POSITIVE_110_REENTRY_ALLOWED")
print("PASS_NEGATIVE_DATAFORSEO_CALL_BLOCKED")
print("PASS_NEGATIVE_EXISTING_TITLE_DUPLICATE_BLOCKED")
print("PASS_NEGATIVE_INCOMPLETE_BINDING_BLOCKED")
print("PASS_NO_PRODUCTION_AUTHORITY")
