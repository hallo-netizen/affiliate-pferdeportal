#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, os, re, sys, zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"CATEGORY_INTEGRATION_HOBBYRAUM"/"out"
OUT.mkdir(parents=True,exist_ok=True)

PORTAL=ROOT/"affiliate-portal-router/assets/portal-structure-v279.json"
CATALOG=ROOT/"release/affiliate-zentrale/current/affiliate-portal-router/assets/ebay-portal-catalog-v2.json"
AFF_MAIN=ROOT/"release/affiliate-zentrale/current/affiliate-portal-router/pferdeportal-affiliate-router.php"
PPM=Path(os.environ.get("PPM_ZIP","/tmp/ppm679.zip"))
PPM_EXPECTED="acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1"

families=[
 {"title":"Pferdesättel","slug":"pferdesaettel","parent_slug":"ausruestung-sattel","hub":"Sattel","hub_slug":"ausruestung-sattel","main_hub":"Ausrüstung","main_slug":"ausruestung","bucket":"sattel-zaumzeug","types":["FAQ","Beratung","Vergleich","Pflege","Kosten"]},
 {"title":"Trensen","slug":"trensen","parent_slug":"ausruestung-trensen-und-gebisse","hub":"Trensen & Gebisse","hub_slug":"ausruestung-trensen-und-gebisse","main_hub":"Ausrüstung","main_slug":"ausruestung","bucket":"sattel-zaumzeug","types":["FAQ","Beratung","Vergleich","Pflege","Kosten"]},
 {"title":"Offenstallbau","slug":"offenstallbau","parent_slug":"stall-offenstall","hub":"Offenstall","hub_slug":"stall-offenstall","main_hub":"Stall","main_slug":"stall","bucket":"stall-weide-haltung","types":["FAQ","Beratung","Vergleich","Installation","Kosten"]},
 {"title":"Paddockbau","slug":"paddockbau","parent_slug":"weide-paddock","hub":"Paddock","hub_slug":"weide-paddock","main_hub":"Weide","main_slug":"weide","bucket":"stall-weide-haltung","types":["FAQ","Beratung","Vergleich","Installation","Kosten"]},
 {"title":"Reitplatzbau","slug":"reitplatzbau","parent_slug":"weide-reitplatz","hub":"Reitplatz","hub_slug":"weide-reitplatz","main_hub":"Weide","main_slug":"weide","bucket":"stall-weide-haltung","types":["FAQ","Beratung","Vergleich","Installation","Kosten"]},
]
suffix={"FAQ":"faq","Beratung":"beratung","Vergleich":"vergleich","Pflege":"pflege","Kosten":"kosten","Installation":"installation"}

def sha(p:Path)->str: return hashlib.sha256(p.read_bytes()).hexdigest()
def stable(v)->str: return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def norm(s:str)->str:
    s=(s or "").lower()
    tr=str.maketrans("äöüß","aous")
    s=s.translate(tr)
    return " ".join(re.findall(r"[a-z0-9]+",s))

def fail(code,**extra):
    print("FAIL",code,json.dumps(extra,ensure_ascii=False,sort_keys=True))
    raise SystemExit(2)

portal=json.loads(PORTAL.read_text(encoding="utf-8"))
catalog=json.loads(CATALOG.read_text(encoding="utf-8"))

checks={}
checks["portal_sha256"]=sha(PORTAL)
checks["catalog_sha256"]=sha(CATALOG)
checks["portal_counts"]=portal.get("counts")
checks["catalog_counts"]=catalog.get("counts")
checks["portal_lengths"]={"pages":len(portal.get("pages",[])),"categories":len(portal.get("categories",[])),"menu":len(portal.get("menu",[]))}

expected_counts={"produktseiten":329,"themenkategorien":1124,"menu_items_total":1520}
for k,v in expected_counts.items():
    if int((portal.get("counts") or {}).get(k,-1))!=v: fail("BASE_PORTAL_COUNT_DRIFT",key=k,actual=(portal.get("counts") or {}).get(k),expected=v)

page_slugs=[str(x.get("slug") or "") for x in portal.get("pages",[]) if isinstance(x,dict)]
cat_slugs=[str(x.get("category_slug") or "") for x in portal.get("categories",[]) if isinstance(x,dict)]
menu_keys=[(str(x.get("item_type") or ""),str(x.get("slug") or "")) for x in portal.get("menu",[]) if isinstance(x,dict)]
if len(page_slugs)!=len(set(page_slugs)): fail("BASE_DUPLICATE_PAGE_SLUG")
if len(cat_slugs)!=len(set(cat_slugs)): fail("BASE_DUPLICATE_CATEGORY_SLUG")
if len(menu_keys)!=len(set(menu_keys)): fail("BASE_DUPLICATE_MENU_KEY")

new_page_slugs=[f["slug"] for f in families]
new_cat_slugs=[f["slug"]+"-"+suffix[t] for f in families for t in f["types"]]
checks["new_page_slugs"]=new_page_slugs
checks["new_category_slugs"]=new_cat_slugs
checks["new_nodes_absent_in_base"]={
 "pages":[s for s in new_page_slugs if s not in page_slugs],
 "categories":[s for s in new_cat_slugs if s not in cat_slugs],
}
if len(checks["new_nodes_absent_in_base"]["pages"])!=5: fail("NEW_PAGE_ALREADY_PRESENT_OR_COLLISION",value=checks["new_nodes_absent_in_base"])
if len(checks["new_nodes_absent_in_base"]["categories"])!=25: fail("NEW_CATEGORY_ALREADY_PRESENT_OR_COLLISION",value=checks["new_nodes_absent_in_base"])

pages_by_slug={x["slug"]:x for x in portal["pages"] if isinstance(x,dict) and x.get("slug")}
for f in families:
    parent=pages_by_slug.get(f["parent_slug"])
    if not parent or int(parent.get("level") or 0)!=2 or parent.get("node_type")!="bereichs_hub":
        fail("PARENT_HUB_MISSING_OR_INVALID",family=f["slug"],parent=f["parent_slug"])

prod=catalog.get("product_targets") or []
arts=catalog.get("article_targets") or []
if len(prod)!=329 or len(arts)!=1124: fail("BASE_CATALOG_TARGET_COUNT_DRIFT",products=len(prod),articles=len(arts))
if len({x.get("slug") for x in prod})!=len(prod): fail("BASE_CATALOG_DUPLICATE_PRODUCT")
if len({x.get("category_slug") for x in arts})!=len(arts): fail("BASE_CATALOG_DUPLICATE_ARTICLE")

concepts=catalog.get("business_concepts") or []
covered=set()
for c in concepts:
    for p in c.get("target_pages") or []:
        if isinstance(p,dict) and p.get("slug"): covered.add(p["slug"])
missing=[x.get("slug") for x in prod if x.get("slug") not in covered]
if missing: fail("BASE_BUSINESS_CONCEPT_COVERAGE_GAP",missing=missing[:20],count=len(missing))

existing_norm={}
for c in concepts:
    k=str(c.get("normalized_title") or "")
    if k: existing_norm.setdefault(k,[]).append(c.get("id"))
collisions={f["slug"]:existing_norm.get(norm(f["title"]),[]) for f in families}
checks["business_concept_title_collisions"]=collisions

m=re.search(r"Version:\s*([^\r\n]+)",AFF_MAIN.read_text(encoding="utf-8"))
checks["affiliate_repo_release_current_header_version"]=m.group(1).strip() if m else None

if not PPM.is_file(): fail("PPM_ZIP_MISSING",path=str(PPM))
checks["ppm_zip_sha256"]=sha(PPM)
if checks["ppm_zip_sha256"]!=PPM_EXPECTED: fail("PPM_ZIP_SHA_MISMATCH",actual=checks["ppm_zip_sha256"],expected=PPM_EXPECTED)

contracts=[
 "portal-production-machine/contracts/complete-portal-category-source-v1.json",
 "portal-production-machine/contracts/category-hierarchy-snapshot-v1.json",
 "portal-production-machine/contracts/wordpress-link-target-snapshot-v1.json",
]
ppm={}
with zipfile.ZipFile(PPM) as z:
    names=set(z.namelist())
    for member in contracts:
        if member not in names: fail("PPM_CONTRACT_MISSING",member=member)
        raw=z.read(member)
        value=json.loads(raw.decode("utf-8"))
        summary={"sha256":hashlib.sha256(raw).hexdigest(),"bytes":len(raw),"top_keys":list(value.keys())}
        summary["contract"]=value.get("contract")
        summary["version"]=value.get("version")
        for meta_key in ("scope","source_type","source_reference","source_export_filename","source_export_sha256","counts","mapping_rule","absolute_completeness_claimed","known_limits","required_roles","runtime_read_only_revalidation_required_before_any_write","automatic_replacement_forbidden","portal_structure_contract","portal_structure_snapshot_hash","wordpress_taxonomy_contract","wordpress_taxonomy_snapshot_hash"):
            if meta_key in value:
                summary[meta_key]=value.get(meta_key)
        if "categories" in value and isinstance(value["categories"],list):
            summary["categories_count"]=len(value["categories"])
            summary["category_sample"]=value["categories"][:2]
            summary["category_slugs"]=[
              str(x.get("slug") or x.get("category_slug") or "") for x in value["categories"] if isinstance(x,dict)
            ]
            summary["new_category_hits"]=[
              x for x in value["categories"] if isinstance(x,dict) and (x.get("slug") in new_cat_slugs or x.get("category_slug") in new_cat_slugs)
            ]
        if "targets" in value and isinstance(value["targets"],list):
            summary["targets_count"]=len(value["targets"])
            summary["target_sample"]=value["targets"][:3]
            summary["targets_all"]=value["targets"]
            summary["new_page_hits"]=[
              x for x in value["targets"] if isinstance(x,dict) and x.get("slug") in new_page_slugs
            ]
        ppm[member]=summary
checks["ppm_contracts"]=ppm

# Hard audit: how PPM runtime references/replaces the three category/link authorities.
search_terms=[
 "complete-portal-category-source-v1.json",
 "category-hierarchy-snapshot-v1.json",
 "wordpress-link-target-snapshot-v1.json",
 "USER_SUPPLIED_CATEGORY_HIERARCHY_FILE_COMPATIBLE",
 "external category",
 "user supplied",
 "source_export",
 "load($override",
 "EXPECTED_SOURCE_COUNT",
 "Three_Type_Complete_Category_Source::load",
 "PPM679_Three_Type_Complete_Category_Source::load",
 "override",
]
references={term:[] for term in search_terms}
with zipfile.ZipFile(PPM) as z:
    for member in z.namelist():
        if member.endswith("/") or member.lower().endswith((".png",".jpg",".jpeg",".gif",".webp",".zip",".woff",".woff2",".ttf",".ico")):
            continue
        try:
            raw=z.read(member)
        except Exception:
            continue
        if len(raw)>3_000_000:
            continue
        try:
            txt=raw.decode("utf-8")
        except Exception:
            continue
        lines=txt.splitlines()
        low=txt.lower()
        for term in search_terms:
            if term.lower() not in low:
                continue
            for idx,line in enumerate(lines):
                if term.lower() in line.lower():
                    references[term].append({
                        "member":member,
                        "line":idx+1,
                        "context":"\n".join(lines[max(0,idx-4):min(len(lines),idx+5)])
                    })
                    if len(references[term])>=30:
                        break
checks["ppm_runtime_references"]=references

out={
 "status":"PASS_READ_ONLY_BASELINE_AUDIT",
 "rules":{
  "no_writes":True,
  "new_nodes":{"pages":5,"article_categories":25,"total":30},
  "wordpress_apply_requires_dry_run":True,
 },
 "checks":checks
}
(OUT/"current_audit.json").write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
print(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True))
print("CATEGORY_INTEGRATION_READ_ONLY_BASELINE_PASS")
