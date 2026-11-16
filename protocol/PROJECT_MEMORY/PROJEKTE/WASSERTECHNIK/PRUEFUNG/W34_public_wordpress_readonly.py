#!/usr/bin/env python3
"""W34: A single read-only WP inventory comparison: historical exported WP, W6, W27, W28, W32 and public live GET.
No WordPress writes, auth requests, plugin updates, SEO requests, or imports.
"""
import json
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[1]
WP=ROOT/"PRUEFUNG/WORDPRESS_TEST_20261114/wassertechnik-bestand.json"
W6=ROOT/"KATEGORIEKONZEPT/W6_WORDPRESS_IMPORTVORSCHAU_218_20261114.json"
W27=ROOT/"REGISTER_GLOSSAR/W27_ZENTRALES_FACHREGISTER_20261116.json"
W28=ROOT/"PRUEFUNG/W28_SEO_EINMALHANDOFF_81_20261116.json"
W32=ROOT/"PLUGINS/ASSETS/W32_wassertechnik-navigation.json"
OUT=ROOT/"PRUEFUNG/_w34_readonly_result.json"
HOST="wasser.oliver-beil.de"

def check(ok:bool, why:str)->None:
    if not ok:raise RuntimeError("W34 INTEGRITY: "+why)

def load(p:Path)->dict: return json.loads(p.read_text(encoding="utf-8"))

class SafeHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        target=urllib.parse.urlparse(newurl)
        if target.hostname!=HOST or target.scheme!="https":
            raise RuntimeError("External or insecure redirect blocked: "+str(target.hostname))
        return super().redirect_request(req,fp,code,msg,headers,newurl)

CLIENT=urllib.request.build_opener(SafeHandler())
def get(relative:str)->tuple[list[dict],dict]:
    url="https://"+HOST+relative
    parsed=urllib.parse.urlparse(url)
    check(parsed.scheme=="https" and parsed.hostname==HOST,"Only allowed target site")
    r=urllib.request.Request(url,headers={"User-Agent":"Wassertechnik-W34-read-only-audit/1.0","Accept":"application/json"},method="GET")
    with CLIENT.open(r,timeout=12) as resp:
        check(urllib.parse.urlparse(resp.url).hostname==HOST,"unexpected final location")
        raw=resp.read(3_000_000)
        try:
            v=json.loads(raw)
        except json.JSONDecodeError as exc:
            import re
            first=re.sub(r"\\s+"," ",raw[:150].decode("utf-8","replace"))
            content_type=resp.headers.get("Content-Type","unknown")
            raise RuntimeError("WP REST GET response was not JSON: HTTP "+str(resp.status)+", type="+content_type+", first="+first) from exc
        check(isinstance(v,list),"WP REST endpoint returned no record list")
        return v,dict(resp.headers)

def publicly_visible(endpoint:str,maxpages:int=30)->tuple[list[dict],dict]:
    items=[];headers_first={}
    for page in range(1,maxpages+1):
        sep="&" if "?" in endpoint else "?"
        data,heads=get(endpoint+sep+f"page={page}&per_page=100")
        if page==1:headers_first={"x_wp_total":heads.get("X-WP-Total"),"x_wp_total_pages":heads.get("X-WP-TotalPages")}
        items.extend(data)
        totalpages=int(headers_first.get("x_wp_total_pages") or 0)
        if (totalpages and page>=totalpages) or (not totalpages and len(data)<100):break
    else:raise RuntimeError("Public read limit reached before a complete inventory; incomplete by design")
    return items,headers_first

def wp_path_map(pages:list[dict])->tuple[dict[str,dict],list[int]]:
    byid={int(x["id"]):x for x in pages};paths={};orphan_parents=[]
    for p in pages:
        segments=[];seen=set();x=p
        while x:
            pid=int(x["id"])
            if pid in seen: raise RuntimeError("WordPress parent cycle")
            seen.add(pid);segments.append(str(x.get("slug") or ""))
            parent=int(x.get("parent") or 0)
            if parent and parent not in byid:
                orphan_parents.append(pid);break
            x=byid.get(parent)
        if not orphan_parents or int(p["id"]) not in orphan_parents:
            path="/".join(reversed(segments))
            if path in paths:raise RuntimeError("Public WP path collision: "+path)
            paths[path]=p
    return paths,orphan_parents

def audit() -> dict:
    wp,w6,w27,w28,w32=map(load,(WP,W6,W27,W28,W32))
    check(wp["schema"]=="wassertechnik-wp-inventory-v1" and wp["mode"]=="READ_ONLY_INVENTORY","Original user-export schema")
    check(wp["site_url"]=="https://"+HOST+"/","original snapshot belongs to bound site")
    check(wp["created_utc"]=="2026-11-14T12:28:47+00:00","original snapshot date")
    counts={key:wp[key]["count"] for key in ("pages","posts","categories")}
    check(counts=={"pages":2,"posts":1,"categories":1},"original inventory not as documented")
    check(all(wp[k]["complete"] for k in ("pages","posts","categories")),"historical WP inventory incomplete")
    p=w6["proposed_owner_targets"]
    check(len(p)==218 and len(set(r["owner_id"] for r in p))==218,"W6 owner count/uniqueness")
    pages=[x for x in p if x["wp_object"]=="page"]
    cats=[x for x in p if x["wp_object"]=="category"]
    check(len(pages)==113 and len(cats)==105,"W6 original plan counts")
    paths={x["proposed_page_path"] for x in pages}
    slugs={x["proposed_category_slug"] for x in cats}
    check(len(paths)==113 and len(slugs)==105,"W6 duplicate destination paths")
    check(all(not x["parent_page_path"] or x["parent_page_path"] in paths for x in pages),"W6 orphan page")
    check(all(x["parent_page_path"] in paths for x in cats),"W6 orphan category")
    wp_paths={x["slug"] for x in wp["pages"]["items"] if x["parent_id"]==0}
    wp_slugs={x["slug"] for x in wp["categories"]["items"]}
    check(not (wp_paths & paths) and not (wp_slugs & slugs),"historical WP has naming conflicts")
    check(w27["version"]=="W27_2026-11-16_v1","latest master revision")
    check(len(w28["produkte"])==81 and w28["anzahl"]==81,"W28 81 candidate handoff")
    check(all(x["seo_owner_freigabe"] is False and x["wp_seitenfreigabe"] is False for x in w28["produkte"]),"unexpected 81er approval")
    check(len(w32["existing_w4_pages"])==79 and w32["wp_buy_menu_count"]==71 and w32["wp_industry_count"]==8,"W32 map")
    check(len(w32["hauptbereiche"])==7,"current navigation areas")
    check(not any(a["id"]=="POOL" and a["existing_menu"]!=0 for a in w32["hauptbereiche"]),"no old WP pool owners")
    old_matches=[x for x in pages if x["proposed_page_path"] in wp_paths]
    output={
        "version":"W34_2026-11-16", "site":"https://"+HOST+"/",
        "strict_read_only":True, "api_post_calls":0,"wp_write_calls":0,
        "historical":{"created_utc":wp["created_utc"],"snapshot_plugin_version":wp["plugin_version"],
          "pages":counts["pages"],"posts":counts["posts"],"categories":counts["categories"],
          "pages_detail":[{"id":x["id"],"title":x["title"],"slug":x["slug"],"status":x["status"]} for x in wp["pages"]["items"]],
          "historic_wp_water_owner_matches":len(old_matches), "historic_slug_conflicts":0},
        "plan":{"old_w6_owners":218,"legacy_w6_pages":113,"legacy_w6_categories":105,"legacy_w6_root_count":sum(not x["parent_page_path"] for x in pages),
          "current_w27_visible_areas":7,"w32_existing_w4_product_pages":79,
          "w32_consumer_menu":71,"w32_industry":8,
          "w28_new_products":81,"w28_new_wp_approvals":0,
          "old_9_root_import_enabled":False},
        "public_now":{"state":"NOT_CHECKED","public_only":True,"includes_drafts":False},
        "conclusion":"Historical user-export proven; a current read-only WordPress inventory is not equivalent to the archived export."
    }
    try:
        public_pages,hp=publicly_visible("/wp-json/wp/v2/pages?_fields=id,slug,parent,status,link")
        public_posts,hposts=publicly_visible("/wp-json/wp/v2/posts?_fields=id,slug,status,link")
        public_categories,hcats=publicly_visible("/wp-json/wp/v2/categories?_fields=id,slug,count")
        public_paths,orphans=wp_path_map(public_pages)
        published_path_collisions=sorted(paths&set(public_paths))
        published_category_slug_collisions=sorted(slugs&{x["slug"] for x in public_categories})
        output["public_now"]={
            "state":"PUBLIC_WP_REST_READ_OK",
            "public_only":True,"includes_drafts":False,"includes_private":False,
            "pages":len(public_pages),"posts":len(public_posts),"categories":len(public_categories),
            "page_reported_total":hp["x_wp_total"],"post_reported_total":hposts["x_wp_total"],
            "category_reported_total":hcats["x_wp_total"],
            "missing_published_parent_pages":len(orphans),
            "w6_matching_published_paths":len(published_path_collisions),
            "w6_matching_published_category_slugs":len(published_category_slug_collisions),
            "sample_published_paths":sorted(public_paths)[:25],
            "sample_w6_path_matches":published_path_collisions[:25],
            "sample_w6_category_slug_matches":published_category_slug_collisions[:25],
            "owner_metadata_checked":False,
            "can_confirm_full_wordpress_inventory":False
        }
        output["conclusion"]="Current PUBLIC WordPress content read; owner metadata/drafts require authenticated read, so do NOT infer complete inventory or release import."
    except Exception as e:
        output["public_now"]={"state":"PUBLIC_REST_NOT_VERIFIED","public_only":True,"includes_drafts":False,
                              "details":type(e).__name__+": "+str(e)[:350],
                              "can_confirm_full_wordpress_inventory":False}
        output["conclusion"]="Public WordPress could not be verified; historical 2026-11-14 snapshot remains the ONLY actual inventory. No import."
    return output

if __name__=="__main__":
    result=audit()
    OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,ensure_ascii=False,indent=2))
