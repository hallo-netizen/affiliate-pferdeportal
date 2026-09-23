#!/usr/bin/env python3
from __future__ import annotations
import argparse, copy, hashlib, json, pathlib, zipfile

MAP="Portal SEO Topic Engine/fixtures/portal-category-map-v1.json"
CENTRAL=pathlib.Path("CATEGORY_INTEGRATION_HOBBYRAUM/PFERDEPORTAL_KATEGORIEN/KATEGORIEN.tsv")
PORTAL=pathlib.Path("release/affiliate-zentrale/current/affiliate-portal-router/assets/portal-structure-v279.json")
CENTRAL_SHA="3e5f32755e09b79c3ac266d5987716dd91866dd21f77b3a522099eae7f962d69"
BASE_ZIP_SHA="71bae2436fc1c3d52c06cefe551517af32a89eeb005457331e2c44136a1c888f"

def sha_bytes(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def sha_file(p:pathlib.Path)->str:return sha_bytes(p.read_bytes())
def fail(code,**data): raise RuntimeError(code+" "+json.dumps(data,ensure_ascii=False,sort_keys=True))
def canonical_hash(v:dict)->str:
    q=copy.deepcopy(v);q.pop("map_sha256",None)
    raw=json.dumps(q,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()
    return sha_bytes(raw)

def central_rows():
    raw=CENTRAL.read_bytes()
    if sha_bytes(raw)!=CENTRAL_SHA: fail("CENTRAL_CATEGORY_SHA_DRIFT",actual=sha_bytes(raw))
    lines=raw.decode("utf-8").splitlines()
    head=lines[0].split("\t")
    rows=[]
    for line in lines[1:]:
        vals=line.split("\t")
        row=dict(zip(head,vals))
        tid=int(row["term_id"])
        if 1577<=tid<=1601: rows.append(row)
    rows.sort(key=lambda x:int(x["term_id"]))
    if len(rows)!=25 or [int(x["term_id"]) for x in rows]!=list(range(1577,1602)):
        fail("CENTRAL_DELTA25_TERM_IDS",count=len(rows),ids=[x["term_id"] for x in rows])
    return rows

def build(base:pathlib.Path,out:pathlib.Path,report:pathlib.Path):
    if sha_file(base)!=BASE_ZIP_SHA: fail("PSTE_BASE_ZIP_SHA",actual=sha_file(base),expected=BASE_ZIP_SHA)
    portal=json.loads(PORTAL.read_text(encoding="utf-8"))
    portal_by_slug={x["category_slug"]:x for x in portal.get("categories",[]) if isinstance(x,dict) and x.get("category_slug")}
    rows=central_rows()
    wanted=[x["slug"] for x in rows]
    if len(set(wanted))!=25: fail("DELTA25_DUPLICATE_SLUG")
    with zipfile.ZipFile(base) as zin:
        names=[n for n in zin.namelist() if not n.endswith("/")]
        if MAP not in names: fail("PSTE_MAP_MISSING")
        base_hash={n:sha_bytes(zin.read(n)) for n in names}
        data=json.loads(zin.read(MAP).decode("utf-8"))
        if data.get("contract")!="PSTE_PORTAL_CATEGORY_MAP_V1": fail("PSTE_MAP_CONTRACT")
        if int(data.get("source_category_count",-1))!=1124 or len(data.get("entries") or [])!=1124: fail("PSTE_MAP_BASE_COUNT")
        old_entries=copy.deepcopy(data["entries"])
        old_by_slug={x["category_slug"]:x for x in old_entries}
        if any(s in old_by_slug for s in wanted): fail("PSTE_MAP_DELTA_ALREADY_PRESENT")
        added=[]
        for row in rows:
            slug=row["slug"]; c=portal_by_slug.get(slug)
            if not c: fail("PORTAL_CATEGORY_MISSING",slug=slug)
            if c.get("category_name")!=row["name"]: fail("CATEGORY_NAME_DRIFT",slug=slug,central=row["name"],portal=c.get("category_name"))
            e={
              "stable_category_id":"portal-category:"+slug,
              "category_slug":slug,
              "category_name":row["name"],
              "article_type":c["theme"],
              "product_page_slug":c["product_slug"],
              "product_page_name":c["product"],
              "main_hub_slug":c["main_slug"],
              "main_hub_name":c["main_hub"],
              "section_hub_slug":c["hub_slug"],
              "section_hub_name":c["hub"],
              "full_path":c["path"],
              "portal_level":4,
              "source_status":"DERIVED_FROM_VALIDATED_PORTAL_EXPORT_AND_EXACT_PRODUCT_SLUG_MATCH",
            }
            added.append(e)
        data["entries"]=sorted(old_entries+added,key=lambda x:x["category_slug"])
        data["source_category_count"]=1149
        data["category_integration_source_ref"]="CATEGORY_INTEGRATION_HOBBYRAUM/PFERDEPORTAL_KATEGORIEN/KATEGORIEN.tsv"
        data["category_integration_source_sha256"]=CENTRAL_SHA
        data["category_integration_delta_count"]=25
        data["category_integration_term_id_range"]="1577-1601"
        data["map_sha256"]=canonical_hash(data)
        new_map=(json.dumps(data,ensure_ascii=False,indent=2)+"\n").encode("utf-8")
        if len(data["entries"])!=1149: fail("PSTE_MAP_TARGET_COUNT")
        slugs=[x["category_slug"] for x in data["entries"]]
        if len(slugs)!=len(set(slugs)): fail("PSTE_MAP_DUPLICATE_SLUG")
        if [s for s in wanted if s not in slugs]: fail("PSTE_MAP_NEW_SLUG_MISSING")
        if any("term_id" in x for x in data["entries"]): fail("PSTE_MAP_TERM_ID_PERSISTED")
        if canonical_hash(data)!=data["map_sha256"]: fail("PSTE_MAP_SELF_HASH")
        with zipfile.ZipFile(out,"w",compression=zipfile.ZIP_DEFLATED) as zout:
            for info in zin.infolist():
                zout.writestr(info,new_map if info.filename==MAP else zin.read(info.filename))
    with zipfile.ZipFile(out) as z:
        new_names=[n for n in z.namelist() if not n.endswith("/")]
        if new_names!=names: fail("PSTE_FILE_LIST_CHANGED")
        changed=[n for n in names if sha_bytes(z.read(n))!=base_hash[n]]
        if changed!=[MAP]: fail("PSTE_CHANGE_SCOPE",changed=changed)
        fresh=json.loads(z.read(MAP).decode("utf-8"))
        if fresh["map_sha256"]!=data["map_sha256"] or len(fresh["entries"])!=1149: fail("PSTE_FRESH_UNPACK")
    old_by_slug={x["category_slug"]:x for x in old_entries}
    new_by_slug={x["category_slug"]:x for x in data["entries"]}
    if any(new_by_slug.get(s)!=v for s,v in old_by_slug.items()): fail("PSTE_OLD_ENTRY_REGRESSION")
    neg=copy.deepcopy(data);neg["map_sha256"]="0"*64
    if canonical_hash(neg)==neg["map_sha256"]: fail("NEGATIVE_HASH_DID_NOT_FAIL")
    neg2=copy.deepcopy(data);neg2["entries"]=neg2["entries"][:-1]
    if int(neg2["source_category_count"])==len(neg2["entries"]): fail("NEGATIVE_COUNT_DID_NOT_FAIL")
    result={
      "status":"PASS",
      "base_zip_sha256":BASE_ZIP_SHA,
      "base_file_count":len(names),
      "changed_files":[MAP],
      "unchanged_files":len(names)-1,
      "target_entry_count":1149,
      "delta_count":25,
      "central_category_sha256":CENTRAL_SHA,
      "map_sha256":data["map_sha256"],
      "map_file_sha256":sha_bytes(new_map),
      "candidate_zip_sha256":sha_file(out),
      "positive_new_slug_count":25,
      "negative_hash":"PASS_FAIL_CLOSED",
      "negative_count":"PASS_FAIL_CLOSED",
      "old_entries_regression":"1124_OF_1124_IDENTICAL",
      "wordpress_write":False,
    }
    report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,ensure_ascii=False,indent=2))
    print("PSTE_0576_CATEGORY_MAP_DELTA_PASS")

if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.add_argument("--base",required=True);ap.add_argument("--out",required=True);ap.add_argument("--report",required=True)
    a=ap.parse_args();build(pathlib.Path(a.base),pathlib.Path(a.out),pathlib.Path(a.report))
