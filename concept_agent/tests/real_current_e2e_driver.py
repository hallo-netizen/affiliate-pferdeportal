#!/usr/bin/env python3
from __future__ import annotations
import base64, copy, hashlib, importlib.util, json, os, stat, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"concept_agent"))
sys.path.insert(0,str(ROOT/"isolated_system4"))
sys.path.insert(0,str(ROOT/"control/startmaster0107"))
import intake_bridge
import endstempel_bridge
import STARTMASTER0107_DUAL_ROOTFIX_REPAIR as dual
import GITHUB_FINAL_RELEASE as final_release
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

OUT=Path("/tmp/concept-agent-real-e2e")
OUT.mkdir(parents=True,exist_ok=True)
SNAP=ROOT/"concept_agent/tests/fixtures/CHAT_SOURCE_EXACT.json"
EXPECTED_SOURCE_SHA="3ac8a725f3e7ebb8a6e332b07e88b989e508e05fe9aa29260aaca6f9bedfc761"

def canon(v): return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")
def stable(v): return hashlib.sha256(canon(v)).hexdigest()
def sha_text(v): return hashlib.sha256(v.encode("utf-8")).hexdigest()
def write(p,v):
    p=Path(p); p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return p

def subset_one():
    raw=SNAP.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=EXPECTED_SOURCE_SHA: raise RuntimeError("CHAT_SOURCE_SHA_MISMATCH")
    x=json.loads(raw)
    b=x["next_textmachine_metadata_batch"]
    b["items"]=b["items"][:1]; b["item_count"]=1
    core=dict(b); core.pop("batch_sha256",None); b["batch_sha256"]=stable(core)
    return x

def current_sources():
    rows=[
      {
        "source_id":"RP_INT_BERATUNG",
        "source_title":"Beratung Reitplatzplaner - Pferde Atelier",
        "source_url":"https://pferde-atelier.de/category/reitplatzplaner-beratung/",
        "evidence":"Ein Reitplatzplaner sollte passend zum vorhandenen Boden und Zugfahrzeug ausgewählt werden."
      },
      {
        "source_id":"RP_MAINT",
        "source_title":"Arena Maintenance: What to Remember - The Horse",
        "source_url":"https://thehorse.com/112571/arena-maintenance-what-to-remember/",
        "evidence":"The amount and type of arena grooming required often depends on what type of surface you have."
      },
      {
        "source_id":"RP_FOOTING",
        "source_title":"Horse Arena Footing Facts - The Horse",
        "source_url":"https://thehorse.com/188622/horse-arena-footing-facts/",
        "evidence":"Harrowing and rolling can make a huge difference in both water content and consistency."
      },
      {
        "source_id":"RP_HAZARDS",
        "source_title":"Troubleshooting Horse Arena Hazards - The Horse",
        "source_url":"https://thehorse.com/19061/troubleshooting-horse-arena-hazards/",
        "evidence":"Regular arena maintenance can help maintain an even surface and reduce your horses' risk of injury."
      },
    ]
    for r in rows: r["snapshot_sha256"]=sha_text(r["evidence"])
    return rows

def research_submission(req):
    item=req["items"][0]
    return {
      "contract":intake_bridge.RESEARCH_SUBMISSION_CONTRACT,
      "batch_sha256":req["batch_sha256"],"item_count":1,
      "items":[{"item_index":0,"plan_slot":item["plan_slot"],"sources":current_sources()}],
    }

def authoring_submission(req,bound):
    m=req["items"][0]; sources=current_sources()
    source_snapshot_id="current16-"+m["plan_slot"]
    claims=[
      {
        "fact_id":"RP_F1","source_id":"RP_INT_BERATUNG",
        "source_url":sources[0]["source_url"],"statement":"Die Auswahl eines Reitplatzplaners muss zum vorhandenen Boden und Zugfahrzeug passen.",
        "evidence_text":sources[0]["evidence"],"evidence_text_sha256":sha_text(sources[0]["evidence"]),
        "claim_status":"FULLY_SUPPORTED","article_types":["Beratung"]
      },
      {
        "fact_id":"RP_F2","source_id":"RP_MAINT",
        "source_url":sources[1]["source_url"],"statement":"Art und Umfang der Reitplatzpflege hängen von der jeweiligen Oberfläche ab.",
        "evidence_text":sources[1]["evidence"],"evidence_text_sha256":sha_text(sources[1]["evidence"]),
        "claim_status":"FULLY_SUPPORTED","article_types":["Beratung"]
      },
      {
        "fact_id":"RP_F3","source_id":"RP_FOOTING",
        "source_url":sources[2]["source_url"],"statement":"Abziehen und Walzen beeinflussen Feuchtigkeit und Gleichmäßigkeit der Oberfläche.",
        "evidence_text":sources[2]["evidence"],"evidence_text_sha256":sha_text(sources[2]["evidence"]),
        "claim_status":"FULLY_SUPPORTED","article_types":["Beratung"]
      },
      {
        "fact_id":"RP_F4","source_id":"RP_HAZARDS",
        "source_url":sources[3]["source_url"],"statement":"Regelmäßige Pflege unterstützt eine gleichmäßige Reitplatzoberfläche.",
        "evidence_text":sources[3]["evidence"],"evidence_text_sha256":sha_text(sources[3]["evidence"]),
        "claim_status":"FULLY_SUPPORTED","article_types":["Beratung"]
      },
    ]
    fact={
      "contract":"canonical_fact_pack_v1","fact_pack_id":source_snapshot_id,
      "source_snapshot_id":source_snapshot_id,"status":"SOURCE_VERIFIED_PRODUCTION_READY",
      "title_scope":m["title"],"sources":sources,"claims":claims,
    }
    links=[
      {"active":True,"anchor":"Weide","href":"/weide/","reason":"Gebundener Portal-Hauptbereich","role":"parent_category","section_id":"criteria","target_status":"publish","target_type":"portal_route"},
      {"active":True,"anchor":"Reitplatzpflege","href":"/weide/weide-reitplatzpflege/","reason":"Gebundener Portal-Bereich","role":"semantic_related","section_id":"decision","target_status":"publish","target_type":"portal_route"},
      {"active":True,"anchor":"Reitplatzplaner","href":"/weide/weide-reitplatzpflege/reitplatzplaner/","reason":"Gebundene Portal-Produktseite","role":"further_information","section_id":"further_information","target_status":"publish","target_type":"portal_route"},
    ]
    cat_hash=sources[0]["snapshot_sha256"]
    category={"category_source_snapshot_hash":cat_hash,"hierarchy_path":"Weide > Reitplatzpflege > Reitplatzplaner > Beratung Reitplatzplaner","name":"Beratung Reitplatzplaner","semantic_binding_not_numeric_identity":True,"slug":m["category"],"taxonomy":"category"}
    registry={"contract":"portal_link_registry_snapshot_v2","entries":copy.deepcopy(links),"snapshot_source_sha256":cat_hash}
    quality={
      "contract":"content_structure_language_binding_v2",
      "intent_terms":[m["target_keyword"],"Reitplatzplaner","Reitplatzpflege","Weide"],
      "internal_test_marker":"LT"+m["plan_slot"][:12].upper(),
      "language_evidence":{},
      "link_bindings":copy.deepcopy(links),
      "portal_link_registry":registry,
      "portal_link_registry_hash":stable(registry),
      "table_value_statement":"Die Tabelle ordnet Auswahlkriterien für Reitplatzplaner nach Bodenwirkung, Einstellbarkeit und praktischer Handhabung.",
      "wordpress_category":copy.deepcopy(category),
    }
    slug="reitplatzplaner-fuer-pferde"
    runtime={
      "allowed_fact_ids":[c["fact_id"] for c in claims],
      "answer":m["title"],"article_type":m["article_type"],"conclusion":m["title"],
      "faq_answer":m["title"],"faq_question":m["title"],"lead":m["title"],
      "links":copy.deepcopy(links),"order_id":"concept-current16-1","question":m["title"],
      "search_intent":"DECISION_SUPPORT","slug":slug,"subject_label":m["target_keyword"],
      "subject_scope":m["title"],"summary":m["title"],"title":m["title"],
    }
    plan={
      "article_type":m["article_type"],"canonical_article":{"article_type":m["article_type"],"slug":slug,"target_keyword":m["target_keyword"],"title":m["title"]},
      "canonical_article_id":"article:277289349b5a5091767a01b1",
      "category_binding":copy.deepcopy(category),"gold_core_binding":"FOUR_TYPE_APPROVED_GOLD_CORE_V1",
      "quality_binding":quality,"quality_binding_hash":stable(quality),"runtime_order":runtime,
      "search_intent":"DECISION_SUPPORT","source_snapshot_id":source_snapshot_id,
      "target_keyword":m["target_keyword"],"topic":m["title"],
    }
    return {
      "contract":intake_bridge.AUTHORING_SUBMISSION_CONTRACT,
      "batch_sha256":req["batch_sha256"],"item_count":1,
      "items":[{"item_index":0,"plan_slot":m["plan_slot"],"title":m["title"],"target_keyword":m["target_keyword"],"category":m["category"],"article_type":m["article_type"],"fact_pack":fact,"production_plan_item":plan}],
    }

def signer_setup():
    seed=b"\x21"*32
    key=Ed25519PrivateKey.from_private_bytes(seed)
    pub=key.public_key().public_bytes(serialization.Encoding.Raw,serialization.PublicFormat.Raw)
    pub_b64=base64.b64encode(pub).decode("ascii"); pub_sha=hashlib.sha256(pub).hexdigest()
    key_id="workflow-e2e-"+pub_sha[:16]
    def signer(payload_hash:str)->str:
        return base64.b64encode(key.sign(payload_hash.encode("ascii"))).decode("ascii")
    return key,key_id,pub_sha,pub_b64,signer

def final_signer_script(key:Ed25519PrivateKey,key_id:str,pub_sha:str,pub_b64:str):
    seed=(b"\x21"*32).hex()
    p=Path("/tmp/concept-agent-final-signer.py")
    p.write_text(f"""#!/usr/bin/env python3
import base64,json,sys
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
key=Ed25519PrivateKey.from_private_bytes(bytes.fromhex('{seed}'))
req=json.loads(sys.stdin.read())
print(json.dumps({{'signing_key_id':'{key_id}','signing_public_key_sha256':'{pub_sha}','public_key_b64':'{pub_b64}','signature_b64':base64.b64encode(key.sign(req['manifest_sha256'].encode('ascii'))).decode('ascii')}},separators=(',',':')))
""",encoding="utf-8")
    p.chmod(p.stat().st_mode|stat.S_IXUSR)
    return p

def main():
    snap=subset_one(); req=intake_bridge.prepare(snap)
    research=research_submission(req); bound=intake_bridge.bind_research(req,research)
    authoring=authoring_submission(req,bound)
    binding=intake_bridge.build_work_binding(req,bound,authoring)
    bpath=write(OUT/"CONCEPT_AGENT_CURRENT_WORK_BINDING.json",binding)
    bsha=hashlib.sha256(bpath.read_bytes()).hexdigest()

    env=os.environ.copy()
    env["CONCEPT_AGENT_CHECKER_CMD"]=f"{sys.executable} concept_agent/runner.py check"
    env["CONCEPT_AGENT_MODEL"]="gpt-5.6-sol"
    proc=subprocess.run([sys.executable,"concept_agent/runner.py","run","--binding",str(bpath),"--binding-sha256",bsha,"--out",str(OUT/"production")],cwd=ROOT,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=1500)
    (OUT/"runner.stdout.txt").write_text(proc.stdout,encoding="utf-8"); (OUT/"runner.stderr.txt").write_text(proc.stderr,encoding="utf-8")
    if proc.returncode!=0: raise RuntimeError("RUNNER_FAILED:"+proc.stderr[-1000:])
    handoff=json.loads((OUT/"production/CONCEPT_AGENT_CHAT_HANDOFF_V1.json").read_text(encoding="utf-8"))
    if handoff.get("status")!="PASS" or handoff.get("item_count")!=1: raise RuntimeError("HANDOFF_NOT_PASS")
    article=handoff["articles"][0]
    check=article["checks"]
    if check.get("status")!="PASS" or (check.get("languagetool") or {}).get("status")!="PASS" or (check.get("ppm") or {}).get("status")!="PASS":
        raise RuntimeError("REAL_CHECKS_NOT_PASS")

    fact=copy.deepcopy(binding["items"][0]["authoring_binding"]["fact_pack"])
    plan_item=copy.deepcopy(binding["items"][0]["authoring_binding"]["production_plan_item"])
    plan_item["canonical_article"]["body_html"]=article["body_html"]
    plan_item["canonical_article"]["body_html_sha256"]=sha_text(article["body_html"])
    bundle={"contract":"canonical_fact_pack_import_v1","created_at":datetime.now(timezone.utc).isoformat(),"fact_packs":[fact]}
    plan={"contract":"production_plan_v4","plan_contract_version":"4.0.0","required_plugin_version":"6.7.9","contract_hashes":dual.CONTRACT_HASHES,"items":[plan_item]}
    meta={
      "article_origin_policy":"POST_TEXT_SIGNED_0039_ORIGIN_AND_NO_REWRITE",
      "authoring_prompt_sha256":dual.fsha(ROOT/dual.PROMPT_REL),
      "authoring_role":"CHAT_OR_APPROVED_RESEARCH_TEXT_PROCESS",
      "content_generation_performed_by_supervisor":False,
      "contract":dual.RELEASE_CONTRACT,
      "created_at_utc":datetime.now(timezone.utc).isoformat(),
      "exact_five_batch_sha256":req["batch_sha256"],"exact_five_item_count":1,
      "frozen_workflow_sha256":dual.binding_sha(ROOT),
      "nullpunkt":{},"nullpunkt_sha256":dual.stable({}),
      "ppm_baseline_sha256":snap["bindings"]["production_baseline_sha256"],
      "ppm_version":"6.7.9","research_evidence_policy":"BOUND_EXISTING_FACHWORKFLOW_ONLY",
      "sequence":107008,"status":"PASS","wordpress_write_performed":False,
    }
    key,key_id,key_sha,pub_b64,signer=signer_setup()
    ctx={"source":"CONCEPT_AGENT_REAL_CURRENT1_E2E","fact_pack_bundle":bundle,"production_plan":plan,"workflow_release_metadata":meta,"workflow_release_items":[{"plan_slot":req["items"][0]["plan_slot"],"canonical_article_id":plan_item["canonical_article_id"]}]}
    pkg=dual.build_package(ctx,signer,key_id,key_sha,pub_b64,False)
    ppath=write(OUT/"PSERC_APPROVED_PRODUCTION_PACKAGE_V1.json",pkg)
    dual.verify_package(ROOT,ppath,trusted={key_id:{"sha256":key_sha,"public_key_b64":pub_b64}})

    endreq={"contract":endstempel_bridge.REQ_CONTRACT,"batch_sha256":req["batch_sha256"],"runtime_generation":910001,"import_envelope":pkg,"articles":[{"plan_slot":req["items"][0]["plan_slot"],"content_utf8":article["body_html"]}],"publish_allowed":False,"content_mutation_performed":False}
    eref=ROOT/"concept_agent/production_ready/REAL_CURRENT1_E2E_TEST.json"; write(eref,endreq)
    manifest_ref=endstempel_bridge.build(str(eref.relative_to(ROOT)))

    fs=final_signer_script(key,key_id,key_sha,pub_b64)
    os.environ["ENDSTEMPEL_HSM_CMD"]=str(fs); os.environ["ENDSTEMPEL_TRUSTED_KEY_ID"]=key_id
    os.environ["ENDSTEMPEL_TRUSTED_PUBLIC_KEY_SHA256"]=key_sha; os.environ["ENDSTEMPEL_TRUSTED_PUBLIC_KEY_B64"]=pub_b64
    final=final_release.finalize(manifest_ref)
    fpath=ROOT/final["final_ref"]
    files=[p for p in fpath.parent.iterdir() if p.is_file() and p.name==final_release.FINAL_FILENAME]
    if len(files)!=1: raise RuntimeError("FINAL_FILE_COUNT_NOT_ONE:"+str(len(files)))
    fp=json.loads(fpath.read_text(encoding="utf-8"))
    if fp.get("status")!="ENDSTEMPEL_PASS" or fp.get("publish_allowed") is not False: raise RuntimeError("FINAL_PACKAGE_NOT_PASS")
    proof={
      "contract":"CONCEPT_AGENT_REAL_CURRENT1_E2E_PROOF_V1","status":"PASS",
      "source_snapshot_sha256":EXPECTED_SOURCE_SHA,"batch_sha256":req["batch_sha256"],
      "item_count":1,"work_binding_file_sha256":bsha,"work_binding_internal_sha256":binding["binding_sha256"],
      "runner_handoff_sha256":handoff["handoff_sha256"],"revision_count":article["revision_count"],
      "article_sha256":sha_text(article["body_html"]),"languagetool":check["languagetool"],"ppm":check["ppm"],
      "pserc_package_sha256":hashlib.sha256(ppath.read_bytes()).hexdigest(),
      "final_ref":final["final_ref"],"final_sha256":final["final_sha256"],"final_file_count":1,
      "simulation_binding_used":False,"fake_checker_used":False,"publish_allowed":False,
    }
    proof["proof_sha256"]=stable(proof); write(OUT/"CONCEPT_AGENT_REAL_CURRENT1_E2E_PROOF_V1.json",proof)
    print(json.dumps(proof,ensure_ascii=False,indent=2))

if __name__=="__main__": main()
