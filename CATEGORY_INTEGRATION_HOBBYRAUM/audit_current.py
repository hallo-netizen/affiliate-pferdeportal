#!/usr/bin/env python3
from __future__ import annotations
import base64, hashlib, json, lzma, os, re, subprocess, sys, zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"CATEGORY_INTEGRATION_HOBBYRAUM"/"out"
OUT.mkdir(parents=True,exist_ok=True)

PORTAL=ROOT/"release/affiliate-zentrale/current/affiliate-portal-router/assets/portal-structure-v279.json"
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

BASE_PORTAL_SHA="b86a160e6b8cf720077830422ca6b574203ce171fdc65d357fe9c6bed039c2e0"
BASE_CATALOG_SHA="4eecef55a3033a4691f8a832eba5fb1657cdb15826ee47d366dccbaabfbb1fa2"
APPLIED_PORTAL_SHA="ce5a312b9017e58c8968a9f0ff132df7cd8d34c7899911a522e03c49eb1a3eed"
APPLIED_CATALOG_SHA="6513ce4ea3e077ca1410ffbfa684138f688e772e07aa8aa483464a6fa8277ff2"

pair=(checks["portal_sha256"],checks["catalog_sha256"])
if pair==(BASE_PORTAL_SHA,BASE_CATALOG_SHA):
    mode="BASE"
    expected_counts={"produktseiten":329,"themenkategorien":1124,"menu_items_total":1520}
    expected_products,expected_articles=329,1124
elif pair==(APPLIED_PORTAL_SHA,APPLIED_CATALOG_SHA):
    mode="APPLIED"
    expected_counts={"produktseiten":334,"themenkategorien":1149,"menu_items_total":1550}
    expected_products,expected_articles=334,1149
else:
    fail("CATEGORY_JSON_PAIR_UNBOUND",portal_sha256=pair[0],catalog_sha256=pair[1])

checks["affiliate_category_state"]=mode
for k,v in expected_counts.items():
    if int((portal.get("counts") or {}).get(k,-1))!=v: fail("PORTAL_COUNT_DRIFT",state=mode,key=k,actual=(portal.get("counts") or {}).get(k),expected=v)

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
checks["new_nodes_absent"]={
 "pages":[s for s in new_page_slugs if s not in page_slugs],
 "categories":[s for s in new_cat_slugs if s not in cat_slugs],
}
if mode=="BASE":
    if len(checks["new_nodes_absent"]["pages"])!=5 or len(checks["new_nodes_absent"]["categories"])!=25:
        fail("BASE_NEW_NODE_COLLISION",value=checks["new_nodes_absent"])
else:
    if checks["new_nodes_absent"]["pages"] or checks["new_nodes_absent"]["categories"]:
        fail("APPLIED_NEW_NODE_MISSING",value=checks["new_nodes_absent"])

pages_by_slug={x["slug"]:x for x in portal["pages"] if isinstance(x,dict) and x.get("slug")}
for f in families:
    parent=pages_by_slug.get(f["parent_slug"])
    if not parent or int(parent.get("level") or 0)!=2 or parent.get("node_type")!="bereichs_hub":
        fail("PARENT_HUB_MISSING_OR_INVALID",family=f["slug"],parent=f["parent_slug"])

prod=catalog.get("product_targets") or []
arts=catalog.get("article_targets") or []
if len(prod)!=expected_products or len(arts)!=expected_articles:
    fail("CATALOG_TARGET_COUNT_DRIFT",state=mode,products=len(prod),articles=len(arts),expected_products=expected_products,expected_articles=expected_articles)
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

# Exact callers and full implementation around complete category source.
caller_patterns=[
 "PPM679_Three_Type_Complete_Category_Source::",
 "Three_Type_Complete_Category_Source::",
 "class PPM679_Three_Type_Complete_Category_Source",
]
callers=[]
with zipfile.ZipFile(PPM) as z:
    for member in z.namelist():
        if member.endswith("/") or not member.lower().endswith((".php",".json",".txt",".md")):
            continue
        try: txt=z.read(member).decode("utf-8")
        except Exception: continue
        lines=txt.splitlines()
        for idx,line in enumerate(lines):
            if any(pat in line for pat in caller_patterns):
                callers.append({
                    "member":member,
                    "line":idx+1,
                    "context":"\n".join(lines[max(0,idx-12):min(len(lines),idx+26)])
                })
checks["ppm_complete_category_source_callers"]=callers


# Read-only historical PPA-013 evidence audit.
# This reconstructs the exact stored V1.50.469 fixture only as historical evidence.
# It is NOT a substitute/current source for 1.50.559 and is never written back to WordPress.
HIST_DESIGN_COMMIT="e4c5decc28e292cd1349bd5fc59e8cecfa2db5cd"
HIST_DESIGN_BRANCH="hobbyroom/design-journal-wissen-v150477-20260913"
HIST_FIXTURE="protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/GLOSSAR/fixtures/design-1.50.469"
HIST_SOURCE_SHA="580fa6c7f5566f29df9254ce92f687a4831554e1d84bf03fbd936bb7577edfe5"
HIST_SOURCE_BYTES=1650857

try:
    subprocess.run(
        ["git","fetch","origin",HIST_DESIGN_BRANCH,"--no-tags","--depth=1"],
        cwd=ROOT, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    fetched=subprocess.check_output(["git","rev-parse","FETCH_HEAD"],cwd=ROOT,text=True).strip()
except Exception as exc:
    fail("PPA013_HISTORICAL_FIXTURE_FETCH_FAILED",error=str(exc))
if fetched != HIST_DESIGN_COMMIT:
    fail("PPA013_HISTORICAL_FIXTURE_HEAD_DRIFT",actual=fetched,expected=HIST_DESIGN_COMMIT)

parts=[]
for i in range(22):
    rel=f"{HIST_FIXTURE}/pferde-template-kit.php.xz.b64.part{i:02d}"
    try:
        raw=subprocess.check_output(["git","show",f"{HIST_DESIGN_COMMIT}:{rel}"],cwd=ROOT)
    except Exception as exc:
        fail("PPA013_HISTORICAL_FIXTURE_PART_MISSING",part=i,path=rel,error=str(exc))
    parts.append(raw)
try:
    packed=base64.b64decode(b"".join(parts),validate=False)
    source=lzma.decompress(packed)
except Exception as exc:
    fail("PPA013_HISTORICAL_FIXTURE_DECODE_FAILED",error=str(exc))
hist_sha=hashlib.sha256(source).hexdigest()
if len(source)!=HIST_SOURCE_BYTES:
    fail("PPA013_HISTORICAL_SOURCE_SIZE_DRIFT",actual=len(source),expected=HIST_SOURCE_BYTES)
if hist_sha!=HIST_SOURCE_SHA:
    fail("PPA013_HISTORICAL_SOURCE_SHA_DRIFT",actual=hist_sha,expected=HIST_SOURCE_SHA)
try:
    hist_txt=source.decode("utf-8")
except UnicodeDecodeError as exc:
    fail("PPA013_HISTORICAL_SOURCE_UTF8_INVALID",error=str(exc))
if "Version: 1.50.469" not in hist_txt or "final class Pferde_Template_Kit" not in hist_txt:
    fail("PPA013_HISTORICAL_SOURCE_IDENTITY_INVALID")

tsv=ROOT/"CATEGORY_INTEGRATION_HOBBYRAUM/PFERDEPORTAL_KATEGORIEN/KATEGORIEN.tsv"
tsv_rows=[]
for idx,line in enumerate(tsv.read_text(encoding="utf-8").splitlines()):
    if idx==0 or not line.strip():
        continue
    cols=line.split("\t")
    if len(cols)<3:
        fail("CENTRAL_TSV_ROW_INVALID",line=idx+1)
    tsv_rows.append({"term_id":cols[0],"slug":cols[1],"name":cols[2],"parent_slug":cols[3] if len(cols)>3 else ""})

quoted_slug_hits=[]
arrow_slug_hits=[]
for row in tsv_rows:
    slug=row["slug"]
    if not slug:
        continue
    # Exact quoted literal only, so incidental prose fragments do not count.
    qpat=re.compile(r"(['\"])" + re.escape(slug) + r"\1")
    if qpat.search(hist_txt):
        quoted_slug_hits.append(slug)
    apat=re.compile(r"(['\"])" + re.escape(slug) + r"\1\s*=>")
    if apat.search(hist_txt):
        arrow_slug_hits.append(slug)

structure_terms=[
    "portal-structure-v279.json",
    "ebay-portal-catalog-v2.json",
    "complete-portal-category-source-v1.json",
    "category-hierarchy-snapshot",
    "wordpress-link-target-snapshot",
    "KATEGORIEN.tsv",
    "parent_slug",
    "parent_id",
    "term_id",
    "portal_structure",
    "category_map",
    "breadcrumb-portal-map-v150310.json",
    "breadcrumb_portal_map",
    "v150310",
]
structure_term_counts={term:hist_txt.lower().count(term.lower()) for term in structure_terms}

wp_structure_calls=[
    "wp_insert_term",
    "wp_update_term",
    "wp_delete_term",
    "wp_set_object_terms",
    "get_terms",
    "get_term_by",
    "get_term",
    "get_categories",
]
wp_structure_call_counts={term:len(re.findall(r"\b"+re.escape(term)+r"\s*\(",hist_txt)) for term in wp_structure_calls}

json_refs=sorted(set(re.findall(r"['\"]([^'\"]+\.json)['\"]",hist_txt)))
category_json_refs=[x for x in json_refs if re.search(r"category|kategorie|portal|taxonomy|hierarchy|link-target",x,re.I)]

json_ref_contexts=[]
for ref in category_json_refs:
    for m in list(re.finditer(re.escape(ref),hist_txt))[:8]:
        lo=max(0,hist_txt.rfind("\n",0,m.start()-5000))
        hi=hist_txt.find("\n",m.end()+5000)
        if hi<0: hi=min(len(hist_txt),m.end()+8000)
        json_ref_contexts.append({"ref":ref,"context":hist_txt[lo:hi].strip()[:12000]})

# Extract compact contexts for any structural-key occurrence; capped to keep evidence readable.
struct_contexts=[]
for term,count in structure_term_counts.items():
    if count<=0:
        continue
    for m in list(re.finditer(re.escape(term),hist_txt,re.I))[:8]:
        lo=max(0,hist_txt.rfind("\n",0,m.start()-250))
        hi=hist_txt.find("\n",m.end()+250)
        if hi<0: hi=min(len(hist_txt),m.end()+500)
        struct_contexts.append({"term":term,"context":hist_txt[lo:hi].strip()[:1200]})

checks["ppa013_historical_150469"]={
    "role":"HISTORICAL_READ_ONLY_EVIDENCE_NOT_CURRENT_SOURCE",
    "source_commit":HIST_DESIGN_COMMIT,
    "source_sha256":hist_sha,
    "source_bytes":len(source),
    "central_tsv_rows":len(tsv_rows),
    "quoted_central_tsv_slug_hits_count":len(quoted_slug_hits),
    "quoted_central_tsv_slug_hits_sample":quoted_slug_hits[:80],
    "array_key_central_tsv_slug_hits_count":len(arrow_slug_hits),
    "array_key_central_tsv_slug_hits_sample":arrow_slug_hits[:80],
    "structure_term_counts":structure_term_counts,
    "wp_structure_call_counts":wp_structure_call_counts,
    "category_or_portal_json_refs":category_json_refs,
    "category_or_portal_json_ref_contexts":json_ref_contexts[:20],
    "structure_contexts":struct_contexts[:100],
    "hard_boundary":"Historical evidence only. Never use this source as a reconstructed substitute for current 1.50.559."
}
print("PPA013_HISTORICAL_150469_SOURCE_SHA_PASS",hist_sha)

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
