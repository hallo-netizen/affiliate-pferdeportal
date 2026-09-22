#!/usr/bin/env python3
from __future__ import annotations
import copy, hashlib, json, re, sys, unicodedata
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"CATEGORY_INTEGRATION_HOBBYRAUM"/"candidate"
OUT.mkdir(parents=True,exist_ok=True)
PORTAL=ROOT/"affiliate-portal-router/assets/portal-structure-v279.json"
CATALOG=ROOT/"release/affiliate-zentrale/current/affiliate-portal-router/assets/ebay-portal-catalog-v2.json"

FAMILIES=[
 {"title":"Pferdesättel","slug":"pferdesaettel","hub":"Sattel & Zubehör","hub_slug":"ausruestung-sattel","main_hub":"Ausrüstung","main_slug":"ausruestung","bucket":"sattel-zaumzeug","types":["FAQ","Beratung","Vergleich","Pflege","Kosten"]},
 {"title":"Trensen","slug":"trensen","hub":"Trensen & Gebisse","hub_slug":"ausruestung-trensen-und-gebisse","main_hub":"Ausrüstung","main_slug":"ausruestung","bucket":"sattel-zaumzeug","types":["FAQ","Beratung","Vergleich","Pflege","Kosten"]},
 {"title":"Offenstallbau","slug":"offenstallbau","hub":"Offenstall","hub_slug":"stall-offenstall","main_hub":"Stall","main_slug":"stall","bucket":"stall-weide-haltung","types":["FAQ","Beratung","Vergleich","Installation","Kosten"]},
 {"title":"Paddockbau","slug":"paddockbau","hub":"Paddock","hub_slug":"weide-paddock","main_hub":"Weide","main_slug":"weide","bucket":"stall-weide-haltung","types":["FAQ","Beratung","Vergleich","Installation","Kosten"]},
 {"title":"Reitplatzbau","slug":"reitplatzbau","hub":"Reitplatz","hub_slug":"weide-reitplatz","main_hub":"Weide","main_slug":"weide","bucket":"stall-weide-haltung","types":["FAQ","Beratung","Vergleich","Installation","Kosten"]},
]
SUFFIX={"FAQ":"faq","Beratung":"beratung","Vergleich":"vergleich","Pflege":"pflege","Kosten":"kosten","Installation":"installation"}
AUSR_ORDER=[
 ("ausruestung-sattel","Sattel & Zubehör"),
 ("ausruestung-trensen-und-gebisse","Trensen & Gebisse"),
 ("ausruestung-decken","Decken"),
 ("ausruestung-reiterbedarf","Reiterbedarf"),
 ("ausruestung-halfter-und-stricke","Halfter & Stricke"),
 ("ausruestung-deckenzubehoer","Deckenzubehör"),
 ("ausruestung-pflegezubehoer","Pflegezubehör"),
]
EXPECTED_BASE_PORTAL_SHA="b86a160e6b8cf720077830422ca6b574203ce171fdc65d357fe9c6bed039c2e0"
EXPECTED_BASE_CATALOG_SHA="4eecef55a3033a4691f8a832eba5fb1657cdb15826ee47d366dccbaabfbb1fa2"

def raw_sha(p:Path): return hashlib.sha256(p.read_bytes()).hexdigest()
def bytes_json(v): return (json.dumps(v,ensure_ascii=False,indent=2)+"\n").encode("utf-8")
def fail(code,**data):
    raise RuntimeError(code+" "+json.dumps(data,ensure_ascii=False,sort_keys=True))

def num_id(v,prefix):
    m=re.fullmatch(re.escape(prefix)+r"(\d+)",str(v or ""))
    return int(m.group(1)) if m else -1

def ascii_text(s):
    s=str(s or "").replace("ß","ss").replace("&"," und ")
    s=unicodedata.normalize("NFKD",s)
    s="".join(ch for ch in s if not unicodedata.combining(ch))
    s=s.lower()
    return " ".join(re.findall(r"[a-z0-9]+",s))

def concept_norm(s):
    s=str(s or "").replace("ß","ss").replace("&"," ")
    s=unicodedata.normalize("NFKD",s)
    s="".join(ch for ch in s if not unicodedata.combining(ch))
    return " ".join(re.findall(r"[a-z0-9]+",s.lower()))

def concept_id(title):
    return "concept-"+concept_norm(title).replace(" ","-")

def product_normalized(p):
    return ascii_text(" ".join([p["title"],p["description"],p["hub"],p["main_hub"]]))

def page_menu(p,order):
    return {"menu_order":order,"depth":int(p["level"]),"item_type":"page","title":p["title"],"slug":p["slug"],"parent_slug":p["parent_slug"],"path":p["path"]}

def cat_menu(c,order):
    return {"menu_order":order,"depth":4,"item_type":"category","title":c["category_name"],"slug":c["category_slug"],"parent_slug":c["product_slug"],"path":c["path"]}

def rebuild_menu(portal):
    pages=list(portal["pages"]); cats=list(portal["categories"])
    by_parent={}
    for p in pages: by_parent.setdefault(p.get("parent_slug",""),[]).append(p)
    cat_index={id(c):i for i,c in enumerate(cats)}
    order=0; out=[]
    def add_page(p):
        nonlocal order
        order+=1; out.append(page_menu(p,order))
        if int(p["level"])==3:
            cc=[c for c in cats if c.get("product_slug")==p["slug"]]
            cc.sort(key=lambda c:cat_index[id(c)])
            for c in cc:
                order+=1; out.append(cat_menu(c,order))
            return
        children=sorted(by_parent.get(p["slug"],[]),key=lambda x:(int(x.get("sort_order",999999)),num_id(x.get("id"),"p")))
        for child in children: add_page(child)
    roots=sorted([p for p in pages if int(p["level"])==1],key=lambda x:(int(x.get("sort_order",999999)),num_id(x.get("id"),"p")))
    for p in roots:add_page(p)
    return out

def reason(t):
    if t=="FAQ": return "FAQ als produktbezogener Nutzerfragen-Hub."
    if t=="Kosten": return "Konservativ behalten: genügend Varianten, Preisbreite, Technik-, Zubehör-, Wartungs- oder Folgekosten-Potenzial."
    return "Themenkategorie nur gesetzt, wenn eigenständiges Beitragspotenzial ohne künstliche Doppelung besteht."

def product_target_from_page(p,bucket):
    out={
      "slug":p["slug"],"title":p["title"],"description":p["description"],
      "hub":None,"hub_slug":p["parent_slug"],"main_hub":None,"main_slug":None,
      "private_bucket_slug":bucket,
    }
    return out

def hard_validate_portal(p):
    if len(p["pages"])!=401: fail("PORTAL_PAGES_COUNT",actual=len(p["pages"]))
    if len(p["categories"])!=1149: fail("PORTAL_CATEGORIES_COUNT",actual=len(p["categories"]))
    if len(p["menu"])!=1550: fail("PORTAL_MENU_COUNT",actual=len(p["menu"]))
    c=p["counts"]
    expected={"haupt_hubs":8,"bereichs_hubs":59,"produktseiten":334,"themenkategorien":1149,"menu_level_1_pages":8,"menu_level_2_pages":59,"menu_level_3_pages":334,"menu_level_4_categories":1149,"menu_items_total":1550,"produktseiten_ohne_themenebene":78}
    for k,v in expected.items():
        if int(c.get(k,-1))!=v: fail("PORTAL_COUNT_FIELD",key=k,actual=c.get(k),expected=v)
    page_slugs=[x["slug"] for x in p["pages"]]
    cat_slugs=[x["category_slug"] for x in p["categories"]]
    if len(page_slugs)!=len(set(page_slugs)): fail("DUPLICATE_PAGE_SLUG")
    if len(cat_slugs)!=len(set(cat_slugs)): fail("DUPLICATE_CATEGORY_SLUG")
    byslug={x["slug"]:x for x in p["pages"]}
    for f in FAMILIES:
        q=byslug.get(f["slug"])
        if not q: fail("NEW_PAGE_MISSING",slug=f["slug"])
        if q["parent_slug"]!=f["hub_slug"] or int(q["sort_order"])!=1: fail("NEW_PAGE_PARENT_ORDER",slug=f["slug"],page=q)
        cs=[x for x in p["categories"] if x["product_slug"]==f["slug"]]
        if len(cs)!=5: fail("NEW_CATEGORY_FIVE_REQUIRED",slug=f["slug"],actual=len(cs))
        for t in f["types"]:
            slug=f["slug"]+"-"+SUFFIX[t]
            rows=[x for x in cs if x["category_slug"]==slug and x["theme"]==t]
            if len(rows)!=1: fail("NEW_CATEGORY_BINDING",slug=slug,type=t,count=len(rows))
    actual_order=[x["slug"] for x in sorted([x for x in p["pages"] if x.get("parent_slug")=="ausruestung" and int(x["level"])==2],key=lambda x:x["sort_order"])]
    wanted=[x[0] for x in AUSR_ORDER]
    if actual_order!=wanted: fail("AUSRUESTUNG_ORDER",actual=actual_order,expected=wanted)
    sattel=byslug["ausruestung-sattel"]
    if sattel["title"]!="Sattel & Zubehör": fail("SATTEL_RENAME",actual=sattel["title"])
    if p["menu"]!=rebuild_menu(p): fail("MENU_NOT_DERIVED_FROM_STRUCTURE")
    return True

def hard_validate_catalog(c,portal_sha):
    counts=c["counts"]
    expected={"main_hubs":8,"hub_pages":59,"product_pages":334,"article_categories":1149,"business_concepts":321,"business_hub_concepts":59,"business_routable_concepts":380}
    for k,v in expected.items():
        if int(counts.get(k,-1))!=v: fail("CATALOG_COUNT",key=k,actual=counts.get(k),expected=v)
    if c.get("source_sha256")!=portal_sha: fail("CATALOG_SOURCE_SHA",actual=c.get("source_sha256"),expected=portal_sha)
    if len(c["product_targets"])!=334 or len(c["article_targets"])!=1149: fail("CATALOG_TARGET_LENGTHS")
    prod={x["slug"]:x for x in c["product_targets"]}
    arts={x["category_slug"]:x for x in c["article_targets"]}
    if len(prod)!=334 or len(arts)!=1149: fail("CATALOG_DUPLICATE_TARGET")
    concepts=c["business_concepts"]
    covered={}
    for x in concepts:
        for t in x.get("target_pages",[]): covered.setdefault(t.get("slug"),[]).append(x.get("id"))
    gaps=[s for s in prod if s not in covered]
    if gaps: fail("CATALOG_CONCEPT_COVERAGE_GAP",gaps=gaps)
    required=set(c["business_supply_contract"]["required_product_concept_ids"])
    if int(c["business_supply_contract"]["required_count"])!=316 or len(required)!=316: fail("SUPPLY_REQUIRED_COUNT",field=c["business_supply_contract"]["required_count"],unique=len(required))
    for f in FAMILIES:
        if f["slug"] not in prod: fail("NEW_PRODUCT_TARGET_MISSING",slug=f["slug"])
        for t in f["types"]:
            s=f["slug"]+"-"+SUFFIX[t]
            if s not in arts: fail("NEW_ARTICLE_TARGET_MISSING",slug=s)
        cid=concept_id(f["title"])
        if cid not in required: fail("NEW_CONCEPT_NOT_SUPPLY_BOUND",id=cid)
        if covered.get(f["slug"])!=[cid]: fail("NEW_CONCEPT_ROUTING",slug=f["slug"],covered=covered.get(f["slug"]),expected=cid)
    if len(c.get("search_rules") or [])!=8: fail("SEARCH_RULE_COUNT_CHANGED")
    return True

def build():
    if raw_sha(PORTAL)!=EXPECTED_BASE_PORTAL_SHA: fail("BASE_PORTAL_SHA_DRIFT",actual=raw_sha(PORTAL))
    if raw_sha(CATALOG)!=EXPECTED_BASE_CATALOG_SHA: fail("BASE_CATALOG_SHA_DRIFT",actual=raw_sha(CATALOG))
    basep=json.loads(PORTAL.read_text(encoding="utf-8"))
    basec=json.loads(CATALOG.read_text(encoding="utf-8"))
    if rebuild_menu(basep)!=basep["menu"]: fail("BASE_MENU_REBUILD_NOT_IDENTICAL")

    p=copy.deepcopy(basep); c=copy.deepcopy(basec)

    # Synchronize already-confirmed live hub title/order.
    page_by_slug={x["slug"]:x for x in p["pages"]}
    order_map={slug:i+1 for i,(slug,_) in enumerate(AUSR_ORDER)}
    title_map=dict(AUSR_ORDER)
    for q in p["pages"]:
        if q.get("parent_slug")=="ausruestung" and q.get("slug") in order_map:
            q["sort_order"]=order_map[q["slug"]]
        if q.get("slug")=="ausruestung-sattel":
            q["title"]="Sattel & Zubehör"; q["path"]="Ausrüstung > Sattel & Zubehör"; q["description"]="Sattel & Zubehör im Bereich Ausrüstung."
        elif q.get("parent_slug")=="ausruestung-sattel":
            q["sort_order"]=int(q["sort_order"])+1
            q["path"]="Ausrüstung > Sattel & Zubehör > "+q["title"]
            q["description"]="Produktseite zu "+q["title"]+" im Bereich Ausrüstung / Sattel & Zubehör. Beiträge werden nicht importiert."
        elif q.get("parent_slug") in {f["hub_slug"] for f in FAMILIES if f["hub_slug"]!="ausruestung-sattel"}:
            q["sort_order"]=int(q["sort_order"])+1

    for q in p["categories"]:
        if q.get("hub_slug")=="ausruestung-sattel":
            q["hub"]="Sattel & Zubehör"
            q["path"]="Ausrüstung > Sattel & Zubehör > "+q["product"]+" > "+q["category_name"]

    maxp=max(num_id(x["id"],"p") for x in p["pages"])
    maxc=max(num_id(x["id"],"c") for x in p["categories"])
    if maxp!=396 or maxc!=1124: fail("BASE_ID_MAX_DRIFT",maxp=maxp,maxc=maxc)

    for i,f in enumerate(FAMILIES,1):
        page={
          "id":"p"+str(maxp+i),"level":3,"node_type":"produktseite","title":f["title"],"slug":f["slug"],
          "parent_slug":f["hub_slug"],"sort_order":1,
          "path":f["main_hub"]+" > "+f["hub"]+" > "+f["title"],
          "description":"Produktseite zu "+f["title"]+" im Bereich "+f["main_hub"]+" / "+f["hub"]+". Beiträge werden nicht importiert.",
          "import_as":"page","show_in_main_menu":True,
        }
        p["pages"].append(page)
        for t in f["types"]:
            maxc+=1
            name=t+" "+f["title"]
            p["categories"].append({
              "id":"c"+str(maxc),"taxonomy":"category","level":4,"node_type":"themenkategorie",
              "category_name":name,"category_slug":f["slug"]+"-"+SUFFIX[t],"parent_slug":"",
              "product":f["title"],"product_slug":f["slug"],"hub":f["hub"],"hub_slug":f["hub_slug"],
              "main_hub":f["main_hub"],"main_slug":f["main_slug"],"theme":t,
              "path":f["main_hub"]+" > "+f["hub"]+" > "+f["title"]+" > "+name,
              "show_in_main_menu":True,"reason":reason(t),
            })

    p["counts"].update({"produktseiten":334,"themenkategorien":1149,"menu_level_3_pages":334,"menu_level_4_categories":1149,"menu_items_total":1550})
    p["menu"]=rebuild_menu(p)
    hard_validate_portal(p)
    portal_raw=bytes_json(p); portal_sha=hashlib.sha256(portal_raw).hexdigest()

    # Catalog: synchronize renamed hub in existing targets/concepts.
    for q in c["product_targets"]:
        if q.get("hub_slug")=="ausruestung-sattel":
            q["hub"]="Sattel & Zubehör"
            q["description"]=q["description"].replace(" / Sattel."," / Sattel & Zubehör.")
            q["normalized"]=product_normalized(q)
    for q in c["article_targets"]:
        if q.get("hub_slug")=="ausruestung-sattel":
            q["hub"]="Sattel & Zubehör"
            q["path"]=q["path"].replace("Ausrüstung > Sattel >","Ausrüstung > Sattel & Zubehör >")
    for q in c["business_concepts"]:
        for t in q.get("target_pages",[]):
            if t.get("hub_slug")=="ausruestung-sattel": t["hub"]="Sattel & Zubehör"
    for q in c["business_hub_concepts"]:
        if q.get("hub_slug")=="ausruestung-sattel":
            q["title"]="Sattel & Zubehör"; q["normalized_title"]=concept_norm(q["title"])
            for t in q.get("target_pages",[]):
                t["title"]="Sattel & Zubehör"; t["hub"]="Sattel & Zubehör"

    # Add new product/article targets and one exact concept per new page.
    for f in FAMILIES:
        page=next(x for x in p["pages"] if x["slug"]==f["slug"])
        pt={
          "slug":f["slug"],"title":f["title"],"description":page["description"],
          "hub":f["hub"],"hub_slug":f["hub_slug"],"main_hub":f["main_hub"],"main_slug":f["main_slug"],
          "private_bucket_slug":f["bucket"],
        }
        pt["normalized"]=product_normalized(pt)
        c["product_targets"].append(pt)
        for t in f["types"]:
            nm=t+" "+f["title"]
            c["article_targets"].append({
              "category_slug":f["slug"]+"-"+SUFFIX[t],"category_name":nm,
              "product":f["title"],"product_slug":f["slug"],"hub":f["hub"],"hub_slug":f["hub_slug"],
              "main_hub":f["main_hub"],"main_slug":f["main_slug"],"theme":t,
              "path":f["main_hub"]+" > "+f["hub"]+" > "+f["title"]+" > "+nm,
            })
        cid=concept_id(f["title"])
        c["business_concepts"].append({
          "id":cid,"title":f["title"],"normalized_title":concept_norm(f["title"]),
          "target_pages":[{"slug":f["slug"],"title":f["title"],"hub":f["hub"],"hub_slug":f["hub_slug"],"main_hub":f["main_hub"],"main_slug":f["main_slug"],"private_bucket_slug":f["bucket"]}],
          "private_bucket_slugs":[f["bucket"]],"hub_slugs":[f["hub_slug"]],"main_slugs":[f["main_slug"]],"private_bucket_slug":f["bucket"],
        })
        c["business_supply_contract"]["required_product_concept_ids"].append(cid)

    c["business_concepts"].sort(key=lambda x:x["id"])
    c["business_supply_contract"]["required_product_concept_ids"]=sorted(set(c["business_supply_contract"]["required_product_concept_ids"]))
    c["business_supply_contract"]["required_count"]=316
    c["counts"].update({"product_pages":334,"article_categories":1149,"business_concepts":321,"business_routable_concepts":380})
    c["source_sha256"]=portal_sha
    hard_validate_catalog(c,portal_sha)

    # Strong old-row preservation check: remove intentional Sattel-title sync and new rows, compare exact.
    old_prod={x["slug"]:x for x in basec["product_targets"]}
    new_prod={x["slug"]:x for x in c["product_targets"]}
    for slug,old in old_prod.items():
        if old.get("hub_slug")=="ausruestung-sattel": continue
        if new_prod.get(slug)!=old: fail("UNRELATED_PRODUCT_TARGET_CHANGED",slug=slug)
    old_art={x["category_slug"]:x for x in basec["article_targets"]}
    new_art={x["category_slug"]:x for x in c["article_targets"]}
    for slug,old in old_art.items():
        if old.get("hub_slug")=="ausruestung-sattel": continue
        if new_art.get(slug)!=old: fail("UNRELATED_ARTICLE_TARGET_CHANGED",slug=slug)

    # Negative mutation suite.
    neg=[]
    def expect_fail(label,fn):
        try: fn()
        except Exception as e: neg.append({"case":label,"pass":True,"error":str(e).split(" ",1)[0]}); return
        fail("NEGATIVE_DID_NOT_FAIL",case=label)
    def vportal(mut):
        q=copy.deepcopy(p); mut(q); hard_validate_portal(q)
    def vcatalog(mut):
        q=copy.deepcopy(c); mut(q); hard_validate_catalog(q,portal_sha)
    expect_fail("duplicate_new_page_slug",lambda:vportal(lambda q:q["pages"].append(copy.deepcopy(next(x for x in q["pages"] if x["slug"]=="pferdesaettel")))))
    expect_fail("wrong_new_parent",lambda:vportal(lambda q:next(x for x in q["pages"] if x["slug"]=="pferdesaettel").update({"parent_slug":"ausruestung-decken"})))
    expect_fail("wrong_article_type",lambda:vportal(lambda q:next(x for x in q["categories"] if x["category_slug"]=="pferdesaettel-faq").update({"theme":"Kosten"})))
    expect_fail("wrong_ausruestung_order",lambda:vportal(lambda q:next(x for x in q["pages"] if x["slug"]=="ausruestung-sattel").update({"sort_order":7})))
    expect_fail("stale_catalog_source_sha",lambda:vcatalog(lambda q:q.update({"source_sha256":EXPECTED_BASE_PORTAL_SHA})))
    expect_fail("missing_business_concept",lambda:vcatalog(lambda q:q.update({"business_concepts":[x for x in q["business_concepts"] if x["id"]!=concept_id("Pferdesättel")]})))
    expect_fail("wrong_private_bucket",lambda:vcatalog(lambda q:next(x for x in q["product_targets"] if x["slug"]=="pferdesaettel").update({"private_bucket_slug":"decken-schutz"})))
    expect_fail("wrong_catalog_count",lambda:vcatalog(lambda q:q["counts"].update({"product_pages":333})))

    (OUT/"portal-structure-v279.CANDIDATE.json").write_bytes(portal_raw)
    (OUT/"ebay-portal-catalog-v2.CANDIDATE.json").write_bytes(bytes_json(c))
    report={
      "status":"PASS",
      "base":{"portal_sha256":EXPECTED_BASE_PORTAL_SHA,"catalog_sha256":EXPECTED_BASE_CATALOG_SHA},
      "candidate":{
        "portal_sha256":portal_sha,
        "catalog_sha256":hashlib.sha256(bytes_json(c)).hexdigest(),
        "counts":p["counts"],
        "catalog_counts":c["counts"],
        "supply_required_count":c["business_supply_contract"]["required_count"],
      },
      "delta":{"new_pages":[f["slug"] for f in FAMILIES],"new_categories":[f["slug"]+"-"+SUFFIX[t] for f in FAMILIES for t in f["types"]],"sattel_parent_title":"Sattel & Zubehör","ausruestung_order":[x[0] for x in AUSR_ORDER]},
      "negative_tests":neg,
      "unchanged_guards":{"search_rules":8,"main_hubs":8,"section_hubs":59,"product_without_topic":78},
    }
    (OUT/"candidate-hardtest-report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report,ensure_ascii=False,indent=2))
    print("CATEGORY_INTEGRATION_CANDIDATE_HARDTEST_PASS")

if __name__=="__main__":
    build()
