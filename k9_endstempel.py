#!/usr/bin/env python3
import argparse, base64, hashlib, json, os, re
from pathlib import Path
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey

PACKAGE_CONTRACT="PSERC_APPROVED_PRODUCTION_PACKAGE_V1"
ENDSTAMP_CONTRACT="PFERDE_ATELIER_ENDSTEMPEL_RELEASE_V1"
MANIFEST_CONTRACT="PFERDE_ATELIER_ENDSTEMPEL_ARTICLE_MANIFEST_V1"
FINAL_FILENAME="GEN1_7_ARTIKEL_PSERC_APPROVED_PRODUCTION_PACKAGE_107008_FINAL.json"

class Blocked(RuntimeError): pass

def canonical(o): return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")
def stable(o): return hashlib.sha256(canonical(o)).hexdigest()
def file_sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):
    x=json.loads(Path(p).read_text(encoding="utf-8"))
    if not isinstance(x,dict): raise Blocked("JSON_OBJECT_REQUIRED:"+str(p))
    return x

def load_private():
    raw=os.environ.get("ENDSTEMPEL_PRIVATE_KEY","").encode()
    if not raw: raise Blocked("ENDSTEMPEL_SECRET_MISSING")
    try:
        key=serialization.load_ssh_private_key(raw,password=None) if b"OPENSSH PRIVATE KEY" in raw else serialization.load_pem_private_key(raw,password=None)
    except Exception as exc: raise Blocked("ENDSTEMPEL_PRIVATE_KEY_INVALID") from exc
    if not isinstance(key,Ed25519PrivateKey): raise Blocked("ENDSTEMPEL_PRIVATE_KEY_NOT_ED25519")
    return key

def build(root,pserc_path,outdir):
    root=Path(root); pserc=load(pserc_path)
    if pserc.get("contract")!="K9_PSERC_RESULT_V1" or pserc.get("status")!="PASS": raise Blocked("PSERC_RESULT_NOT_PASS")
    if pserc.get("publish_allowed") is not False: raise Blocked("PSERC_PUBLISH_FLAG_INVALID")
    ledger=load(root/"state/ledger.json")
    if ledger.get("generation",0)<1: raise Blocked("LEDGER_GENERATION_INVALID")
    items=ledger.get("items")
    if not isinstance(items,list) or not items or any(x.get("stages",{}).get("check")!="DONE" for x in items): raise Blocked("LEDGER_NOT_FULLY_CHECKED")

    pserc_rows=pserc.get("results")
    if isinstance(pserc_rows,list):
        by_item={str(x.get("item_id") or ""):x for x in pserc_rows if isinstance(x,dict)}
        if len(by_item)!=len(items): raise Blocked("PSERC_ITEM_SET_COUNT_INVALID")
    elif len(items)==1:
        by_item={str(items[0].get("item_id") or ""):pserc}
    else:
        raise Blocked("PSERC_BATCH_RESULTS_MISSING")

    intake_candidates=[]
    for candidate in sorted((root/"warehouse/intake").glob("K9-INTAKE-*.json")):
        candidate_data=load(candidate)
        candidate_items=candidate_data.get("items")
        if isinstance(candidate_items,list):
            intake_candidates.append((candidate,candidate_items))
    intake_paths=[]
    for item in items:
        slot=item["metadata"]["plan_slot"]
        hits=[]
        for candidate,candidate_items in intake_candidates:
            if any(isinstance(row,dict) and isinstance(row.get("metadata"),dict) and row["metadata"].get("plan_slot")==slot for row in candidate_items):
                hits.append(candidate)
        if len(hits)!=1: raise Blocked("ACTIVE_INTAKE_NOT_UNIQUE:"+str(slot))
        intake_paths.append(hits[0])
    unique_intakes={str(x) for x in intake_paths}
    if len(unique_intakes)!=1: raise Blocked("ACTIVE_INTAKE_BATCH_NOT_UNIQUE")
    intake_path=intake_paths[0]
    intake=load(intake_path)
    batch=str(intake.get("source_batch_sha256") or "")
    if not re.fullmatch(r"[0-9a-f]{64}",batch): raise Blocked("SOURCE_BATCH_SHA_INVALID")

    fact_packs=[]
    plan_items=[]
    release_items=[]
    article_rows=[]
    for item in items:
        iid=str(item.get("item_id") or "")
        slot=item["metadata"]["plan_slot"]
        article_key="repair" if item.get("revision",0)>0 else "write"
        apath=root/item["products"][article_key]["path"]
        apkg=load(apath)
        rows=[x for x in apkg.get("results",[]) if x.get("item_id")==iid]
        if len(rows)!=1: raise Blocked("LATEST_ARTICLE_NOT_UNIQUE:"+iid)
        article=rows[0].get("article_product")
        if not isinstance(article,dict): raise Blocked("ARTICLE_PRODUCT_MISSING:"+iid)
        html=str(article.get("content_html") or "")
        raw=html.encode("utf-8")
        if hashlib.sha256(raw).hexdigest()!=article.get("content_sha256"): raise Blocked("ARTICLE_HASH_INVALID:"+iid)

        pr=by_item.get(iid)
        if not isinstance(pr,dict): raise Blocked("PSERC_ITEM_RESULT_MISSING:"+iid)
        fact_pack=pr.get("fact_pack"); plan_item=pr.get("production_plan_item")
        cid=str(pr.get("canonical_article_id") or "")
        if not isinstance(fact_pack,dict) or not isinstance(plan_item,dict) or not cid.startswith("article:"):
            raise Blocked("PSERC_COMPONENTS_INVALID:"+iid)
        plan_item=json.loads(json.dumps(plan_item,ensure_ascii=False))
        plan_item["canonical_article_id"]=cid
        canonical_article=plan_item.get("canonical_article")
        if not isinstance(canonical_article,dict): raise Blocked("CANONICAL_ARTICLE_MISSING:"+iid)
        canonical_article["body_html"]=html
        canonical_article["body_html_sha256"]=hashlib.sha256(raw).hexdigest()
        plan_item["canonical_article"]=canonical_article

        fact_packs.append(fact_pack)
        plan_items.append(plan_item)
        release_items.append({"canonical_article_id":cid,"plan_slot":slot})
        article_rows.append({
            "name":f"ARTICLE_{slot}.md",
            "plan_slot":slot,
            "sha256":hashlib.sha256(raw).hexdigest(),
            "byte_length":len(raw),
            "content_utf8":html
        })

    bundle={"contract":"canonical_fact_pack_import_v1","fact_packs":fact_packs}
    plan={"contract":"production_plan_v4","plan_contract_version":"4.0.0","required_plugin_version":"6.7.9","items":plan_items}
    bh,ph=stable(bundle),stable(plan)
    release={
        "content_generation_performed_by_supervisor":False,
        "contract":"WORKFLOW_SUPERVISOR_RELEASE_V2_SIGNED",
        "exact_five_batch_sha256":batch,
        "exact_five_item_count":len(items),
        "fact_pack_bundle_sha256":bh,
        "items":release_items,
        "production_plan_sha256":ph,
        "status":"PASS",
        "wordpress_write_performed":False
    }
    rh=stable(release)
    envelope={
        "contract":PACKAGE_CONTRACT,
        "fact_pack_bundle":bundle,
        "fact_pack_bundle_sha256":bh,
        "production_plan":plan,
        "production_plan_sha256":ph,
        "source":"KONZEPT9_ISOLATED_REAL_PSERC_LT68_PPM679_PASS",
        "workflow_release":release,
        "workflow_release_sha256":rh
    }
    envelope["package_id"]=stable({"contract":PACKAGE_CONTRACT,"fact_pack_bundle_sha256":bh,"production_plan_sha256":ph,"workflow_release_sha256":rh})
    envelope["package_payload_sha256"]=stable(envelope)
    env_sha=stable(envelope)

    manifest={
        "contract":MANIFEST_CONTRACT,
        "batch_sha256":batch,
        "runtime_generation":ledger["generation"],
        "source_manifest_ref":str(intake_path.relative_to(root)),
        "source_manifest_sha256":file_sha(intake_path),
        "article_count":len(article_rows),
        "articles":article_rows,
        "import_envelope_sha256":env_sha,
        "publish_allowed":False,
        "content_mutation_performed":False
    }
    mh=stable(manifest)
    key=load_private(); pub=key.public_key().public_bytes(serialization.Encoding.Raw,serialization.PublicFormat.Raw)
    pub_sha=hashlib.sha256(pub).hexdigest(); pub_b64=base64.b64encode(pub).decode("ascii")
    sig=key.sign(mh.encode("ascii")); sig_b64=base64.b64encode(sig).decode("ascii")
    Ed25519PublicKey.from_public_bytes(pub).verify(sig,mh.encode("ascii"))
    pkg={
        "contract":PACKAGE_CONTRACT,"endstamp_contract":ENDSTAMP_CONTRACT,"status":"ENDSTEMPEL_PASS","batch_sha256":batch,
        "article_manifest":manifest,"article_manifest_sha256":mh,"import_envelope":envelope,"import_envelope_sha256":env_sha,
        "signature_algorithm":"ED25519","signing_key_id":"github-secret-ed25519-"+pub_sha[:16],
        "signing_public_key_sha256":pub_sha,"public_key_b64":pub_b64,"signature_b64":sig_b64,
        "publish_allowed":False,"content_mutation_performed":False
    }
    pkg["package_payload_sha256"]=stable(pkg)
    outdir=Path(outdir); outdir.mkdir(parents=True,exist_ok=True); out=outdir/FINAL_FILENAME
    out.write_text(json.dumps(pkg,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return out,pkg

def verify(path):
    x=load(path)
    if x.get("contract")!=PACKAGE_CONTRACT or x.get("endstamp_contract")!=ENDSTAMP_CONTRACT or x.get("status")!="ENDSTEMPEL_PASS": raise Blocked("FINAL_CONTRACT_INVALID")
    if x.get("publish_allowed") is not False or x.get("content_mutation_performed") is not False: raise Blocked("FINAL_FLAGS_INVALID")
    cp=dict(x); ph=cp.pop("package_payload_sha256",None)
    if ph!=stable(cp): raise Blocked("FINAL_PAYLOAD_HASH_INVALID")
    m=x.get("article_manifest"); mh=stable(m)
    if mh!=x.get("article_manifest_sha256"): raise Blocked("MANIFEST_HASH_INVALID")
    if m.get("article_count")!=len(m.get("articles",[])) or m.get("article_count")<1: raise Blocked("ARTICLE_COUNT_INVALID")
    for row in m["articles"]:
        raw=row["content_utf8"].encode("utf-8")
        if row["name"]!="ARTICLE_"+row["plan_slot"]+".md" or hashlib.sha256(raw).hexdigest()!=row["sha256"] or len(raw)!=row["byte_length"]: raise Blocked("ARTICLE_BYTES_INVALID")
    env=x.get("import_envelope")
    if stable(env)!=x.get("import_envelope_sha256"): raise Blocked("IMPORT_ENVELOPE_HASH_INVALID")
    required={"contract","package_id","package_payload_sha256","source","fact_pack_bundle","fact_pack_bundle_sha256","production_plan","production_plan_sha256","workflow_release","workflow_release_sha256"}
    if set(env)!=required: raise Blocked("IMPORT_ENVELOPE_SCHEMA_INVALID")
    pub=base64.b64decode(x["public_key_b64"],validate=True)
    if hashlib.sha256(pub).hexdigest()!=x["signing_public_key_sha256"]: raise Blocked("PUBLIC_KEY_HASH_INVALID")
    Ed25519PublicKey.from_public_bytes(pub).verify(base64.b64decode(x["signature_b64"],validate=True),mh.encode("ascii"))
    return {"contract":"K9_ENDSTEMPEL_VERIFY_V1","status":"PASS","final_sha256":file_sha(path),"article_count":m["article_count"],"batch_sha256":x["batch_sha256"],"publish_allowed":False}

def main():
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest="cmd",required=True)
    p=sub.add_parser("build"); p.add_argument("root"); p.add_argument("pserc"); p.add_argument("outdir")
    p=sub.add_parser("verify"); p.add_argument("path")
    a=ap.parse_args()
    try:
        if a.cmd=="build":
            path,_=build(a.root,a.pserc,a.outdir); result=verify(path); result["final_ref"]=str(path)
        else: result=verify(a.path)
    except Exception as exc:
        print(json.dumps({"contract":"K9_ENDSTEMPEL_VERIFY_V1","status":"BLOCKED","reason":str(exc)},ensure_ascii=False,indent=2))
        raise SystemExit(2)
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=="__main__": main()
