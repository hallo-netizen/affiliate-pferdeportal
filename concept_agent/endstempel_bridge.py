#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,re,sys
from pathlib import Path

REPO=Path(__file__).resolve().parents[1]
REQ_CONTRACT="CONCEPT_AGENT_ENDSTEMPEL_AUTO_REQUEST_V1"
PACKAGE_CONTRACT="PSERC_APPROVED_PRODUCTION_PACKAGE_V1"
SOURCE_CONTRACT="PFERDE_ATELIER_EXISTING_ARTICLE_RECOVERY_SOURCE_V1"
SHA_RE=re.compile(r"^[0-9a-f]{64}$")

class Blocked(RuntimeError): pass

def canon(o): return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")
def h(raw:bytes): return hashlib.sha256(raw).hexdigest()
def stable(o): return h(canon(o))

def load(path:Path):
    x=json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(x,dict): raise Blocked("REQUEST_OBJECT_REQUIRED")
    return x

def build(request_ref:str)->str:
    p=(REPO/request_ref).resolve()
    if REPO.resolve() not in p.parents or not p.is_file(): raise Blocked("REQUEST_REF_INVALID")
    req=load(p)
    if req.get("contract")!=REQ_CONTRACT: raise Blocked("REQUEST_CONTRACT_INVALID")
    if req.get("publish_allowed") is not False or req.get("content_mutation_performed") is not False:
        raise Blocked("REQUEST_FLAGS_INVALID")
    batch=str(req.get("batch_sha256") or "")
    generation=req.get("runtime_generation")
    if not SHA_RE.fullmatch(batch): raise Blocked("BATCH_INVALID")
    if isinstance(generation,bool) or not isinstance(generation,int) or generation<1: raise Blocked("GENERATION_INVALID")
    env=req.get("import_envelope")
    articles=req.get("articles")
    if not isinstance(env,dict) or env.get("contract")!=PACKAGE_CONTRACT: raise Blocked("IMPORT_ENVELOPE_INVALID")
    if not isinstance(articles,list) or not articles: raise Blocked("ARTICLES_INVALID")
    release=env.get("workflow_release") or {}
    if release.get("contract")!="WORKFLOW_SUPERVISOR_RELEASE_V2_SIGNED" or release.get("status")!="PASS":
        raise Blocked("WORKFLOW_RELEASE_INVALID")
    if release.get("exact_five_batch_sha256")!=batch or release.get("wordpress_write_performed") is not False:
        raise Blocked("WORKFLOW_RELEASE_BINDING_INVALID")
    release_by_slot={str(r.get("plan_slot") or ""):str(r.get("canonical_article_id") or "") for r in release.get("items") or [] if isinstance(r,dict)}
    plan_by_id={str(r.get("canonical_article_id") or ""):r for r in (env.get("production_plan") or {}).get("items") or [] if isinstance(r,dict)}
    if len(release_by_slot)!=len(articles): raise Blocked("ARTICLE_COUNT_BINDING_INVALID")
    outdir=REPO/"control/startmaster0107/recovery_sources"/batch/f"generation-{generation:06d}"
    if outdir.exists(): raise Blocked("GENERATION_ALREADY_EXISTS")
    outdir.mkdir(parents=True)
    items=[]
    seen=set()
    try:
        for row in articles:
            if not isinstance(row,dict): raise Blocked("ARTICLE_ROW_INVALID")
            slot=str(row.get("plan_slot") or ""); body=row.get("content_utf8")
            if not SHA_RE.fullmatch(slot) or slot in seen or not isinstance(body,str): raise Blocked("ARTICLE_BINDING_INVALID")
            cid=release_by_slot.get(slot); plan=plan_by_id.get(cid) if cid else None
            if not plan or (plan.get("canonical_article") or {}).get("body_html")!=body:
                raise Blocked("IMPORT_ENVELOPE_ARTICLE_MISMATCH:"+slot)
            raw=body.encode("utf-8"); digest=h(raw)
            name=f"ARTICLE_{slot}.md"; ap=outdir/name; ap.write_bytes(raw)
            ref=str(ap.relative_to(REPO))
            items.append({"ref":ref,"sha256":digest,"plan_slot":slot})
            seen.add(slot)
        env_raw=canon(env); env_sha=h(env_raw)
        ep=outdir/"PSERC_IMPORT_ENVELOPE.json"; ep.write_bytes(env_raw)
        manifest={
            "contract":SOURCE_CONTRACT,"batch_sha256":batch,"runtime_generation":generation,
            "item_count":len(items),"import_envelope_ref":str(ep.relative_to(REPO)),
            "import_envelope_sha256":env_sha,"publish_allowed":False,"content_mutation_performed":False,
            "items":sorted(items,key=lambda x:x["ref"])
        }
        mp=outdir/"MANIFEST.json"; mp.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        return str(mp.relative_to(REPO))
    except Exception:
        import shutil; shutil.rmtree(outdir,ignore_errors=True); raise

def main():
    try:
        if len(sys.argv)!=3 or sys.argv[1]!="build": raise Blocked("USE: endstempel_bridge.py build REQUEST_REF")
        print(build(sys.argv[2])); return 0
    except Exception as exc:
        print("CONCEPT_AGENT_ENDSTEMPEL_BRIDGE_BLOCKED:"+str(exc),file=sys.stderr); return 2

if __name__=="__main__": raise SystemExit(main())
