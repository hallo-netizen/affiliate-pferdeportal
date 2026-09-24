from __future__ import annotations
import copy, hashlib, json, os, shutil, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PORTAL=ROOT/"affiliate-portal-router/assets/portal-structure-v279.json"
CANDIDATE=Path(os.environ.get("CATEGORY_PORTAL_CANDIDATE", str(ROOT/"release/affiliate-zentrale/current/affiliate-portal-router/assets/portal-structure-v279.json"))).resolve()
PPM=ROOT/"control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip"
PPM_SRC=Path(os.environ.get("PPM679_SOURCE","/tmp/ppm679.zip"))

sys.path.insert(0,str(ROOT/"isolated_system4"))
import machine_point0, production_checks  # noqa:E402

NEW=[
("pferdesaettel-faq","FAQ"),("pferdesaettel-beratung","Beratung"),("pferdesaettel-vergleich","Vergleich"),("pferdesaettel-pflege","Pflege"),("pferdesaettel-kosten","Kosten"),
("trensen-faq","FAQ"),("trensen-beratung","Beratung"),("trensen-vergleich","Vergleich"),("trensen-pflege","Pflege"),("trensen-kosten","Kosten"),
("offenstallbau-faq","FAQ"),("offenstallbau-beratung","Beratung"),("offenstallbau-vergleich","Vergleich"),("offenstallbau-installation","Installation"),("offenstallbau-kosten","Kosten"),
("paddockbau-faq","FAQ"),("paddockbau-beratung","Beratung"),("paddockbau-vergleich","Vergleich"),("paddockbau-installation","Installation"),("paddockbau-kosten","Kosten"),
("reitplatzbau-faq","FAQ"),("reitplatzbau-beratung","Beratung"),("reitplatzbau-vergleich","Vergleich"),("reitplatzbau-installation","Installation"),("reitplatzbau-kosten","Kosten"),
]

def fail(code,data=None):
    raise RuntimeError(code+("" if data is None else ":"+json.dumps(data,ensure_ascii=False,sort_keys=True)))

if not CANDIDATE.is_file(): fail("PORTAL_CANDIDATE_MISSING")
if not PPM_SRC.is_file(): fail("PPM_SOURCE_MISSING")
if hashlib.sha256(PPM_SRC.read_bytes()).hexdigest()!=production_checks.PPM_PACKAGE_SHA256: fail("PPM_SOURCE_SHA_MISMATCH")
PPM.parent.mkdir(parents=True,exist_ok=True)
backup=PPM.read_bytes() if PPM.is_file() else None
portal_backup=PORTAL.read_bytes() if PORTAL.is_file() else None
try:
    shutil.copyfile(PPM_SRC,PPM)
    PORTAL.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(CANDIDATE,PORTAL)
    portal_sha=hashlib.sha256(PORTAL.read_bytes()).hexdigest()

    supported={"FAQ","Beratung","Vergleich","Pflege"}
    category_only={"Kosten","Installation"}
    # Prove the article-type boundary first. Kosten/Installation are category intents,
    # but are not current PPM authoring types. That must not be misreported as a link failure.
    for t in sorted(supported):
        if not machine_point0.authoring_contract._type_definition(PPM,t):
            fail("SUPPORTED_PPM_TYPE_MISSING",t)
    for t in sorted(category_only):
        if machine_point0.authoring_contract._type_definition(PPM,t):
            fail("CATEGORY_ONLY_TYPE_UNEXPECTEDLY_AUTHORABLE",t)

    checks=[]
    full_prewrite_count=0
    category_link_only_count=0
    original_type_authority=machine_point0._type_authority
    for slug,article_type in NEW:
        plan_slot=hashlib.sha256(("link-proof|"+slug).encode()).hexdigest()
        article={"title":"Linkproof "+slug,"target_keyword":slug.replace("-"," "),"category":slug,"article_type":article_type,"plan_slot":plan_slot}

        if article_type in supported:
            plan=machine_point0._prewrite_plan(ROOT,article)
            full_prewrite_count+=1
        else:
            # First prove the untouched production route blocks only on the missing PPM
            # authoring type, after hierarchy/link construction has passed.
            try:
                machine_point0._prewrite_plan(ROOT,article)
            except Exception as exc:
                expected="PPM679_PREWRITE_TYPE_AUTHORITY_MISSING:"+article_type
                if str(exc)!=expected: fail("CATEGORY_ONLY_PREWRITE_WRONG_BLOCK",{"slug":slug,"actual":str(exc),"expected":expected})
            else:
                fail("CATEGORY_ONLY_PREWRITE_DID_NOT_BLOCK",slug)

            # Link-only proof: run the exact same production prewrite function with only
            # the unrelated type-authority lookup replaced by an inert sentinel.
            machine_point0._type_authority=lambda _repo,_type: ("CATEGORY_LINK_ONLY_PROBE","CATEGORY_LINK_ONLY_PROBE")
            try:
                plan=machine_point0._prewrite_plan(ROOT,article)
            finally:
                machine_point0._type_authority=original_type_authority
            category_link_only_count+=1

        q=plan["quality_binding"]
        links=q["link_bindings"]
        reg=q["portal_link_registry"]
        if reg.get("contract")!="portal_link_registry_snapshot_v2": fail("REGISTRY_CONTRACT",slug)
        if reg.get("snapshot_source_sha256")!=portal_sha: fail("REGISTRY_SOURCE_SHA",slug)
        if len(links)!=3 or len(reg.get("entries") or [])!=3: fail("LINK_COUNT",slug)
        roles=[x.get("role") for x in links]
        if roles!=["parent_category","semantic_related","further_information"]: fail("LINK_ROLES",{"slug":slug,"roles":roles})
        for row in links:
            if row.get("active") is not True or row.get("target_status")!="publish" or row.get("target_type")!="portal_route": fail("LINK_NOT_PUBLISHED",{"slug":slug,"row":row})
            href=str(row.get("href") or "")
            if not href.startswith("/") or href.startswith("//"): fail("LINK_HREF_INVALID",{"slug":slug,"href":href})
        machine_point0.point0_snapshot.prewrite_from_plan(article,0,plan)
        checks.append({"category":slug,"article_type":article_type,"links":copy.deepcopy(links),"registry_hash":q["portal_link_registry_hash"]})

    # Negative: category absent from portal structure must fail closed before type authority.
    bad={"title":"bad","target_keyword":"bad","category":"definitely-not-a-real-category","article_type":"FAQ","plan_slot":"a"*64}
    try:
        machine_point0._prewrite_plan(ROOT,bad)
    except Exception as exc:
        if "PORTAL_CATEGORY_NOT_UNIQUE" not in str(exc): fail("NEGATIVE_WRONG_ERROR",str(exc))
    else:
        fail("NEGATIVE_UNKNOWN_CATEGORY_DID_NOT_FAIL")

    out={
      "status":"PASS",
      "portal_structure_sha256":portal_sha,
      "new_categories_checked":len(checks),
      "full_supported_prewrite_categories":full_prewrite_count,
      "category_link_only_categories":category_link_only_count,
      "category_only_types":sorted(category_only),
      "links_per_category":3,
      "total_links_checked":len(checks)*3,
      "negative_unknown_category":"PASS_FAIL_CLOSED",
      "write_attempted":False
    }
    if len(checks)!=25 or full_prewrite_count!=17 or category_link_only_count!=8:
        fail("LINK_PROOF_COUNTS_WRONG",out)
    print(json.dumps(out,ensure_ascii=False,indent=2))
    print("CATEGORY_LINK_REGISTRY_NEW25_PASS")
finally:
    if backup is None:
        try: PPM.unlink()
        except FileNotFoundError: pass
    else:
        PPM.write_bytes(backup)
    if portal_backup is None:
        try: PORTAL.unlink()
        except FileNotFoundError: pass
    else:
        PORTAL.write_bytes(portal_backup)
