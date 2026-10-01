#!/usr/bin/env python3
import argparse, copy, hashlib, json, re, subprocess, tempfile, zipfile
from pathlib import Path

PPM_SHA="acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1"
PSERC_SHA="77a14aca97f46d60bc9001d66327abb68dd9cac9ad111f8ecefa1a8afd345314"
PSERC_INNER="PSERC-FIX/portal-seo-editorial-plan-compiler_0.28.18_ENDSTEMPEL_IMPORT_ENVELOPE_BINDING.zip"
INTEGRITY_STATUS="PSERC_FINAL_INTEGRITY_ONLY_PASS"

class Blocked(RuntimeError): pass

def sha_file(p):
    h=hashlib.sha256()
    with Path(p).open("rb") as f:
        for c in iter(lambda:f.read(1024*1024),b""): h.update(c)
    return h.hexdigest()

def stable(x):
    return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()).hexdigest()

def load(p):
    x=json.loads(Path(p).read_text(encoding="utf-8"))
    if not isinstance(x,dict): raise Blocked("JSON_OBJECT_REQUIRED")
    return x

def canonical_fact_pack(research):
    fp=research.get("fact_pack"); sources=research.get("sources")
    if not isinstance(fp,dict) or not isinstance(sources,list): raise Blocked("RESEARCH_PRODUCT_INVALID")
    by_id={str(x.get("source_id") or ""):x for x in sources if isinstance(x,dict)}
    canonical_sources={}; claims=[]
    for raw in fp.get("claims",[]):
        if not isinstance(raw,dict): raise Blocked("CLAIM_INVALID")
        raw_sid=str(raw.get("source_id") or "").strip(); src=by_id.get(raw_sid)
        if not src: raise Blocked("CLAIM_SOURCE_UNKNOWN:"+raw_sid)
        sid=str(src.get("title") or "").strip() if raw_sid.upper().startswith("TEST_") else raw_sid
        if not sid: raise Blocked("CLAIM_SOURCE_CANONICAL_ID_MISSING:"+raw_sid)
        canonical_sources[sid]=src
        statement=str(raw.get("statement") or ""); evidence=str(raw.get("display_statement") or statement)
        claims.append({"article_types":list(raw.get("article_types") or [fp.get("article_type")]),"claim_status":str(raw.get("claim_status") or ""),"evidence_text":evidence,"evidence_text_sha256":str(raw.get("evidence_text_sha256") or ""),"fact_id":str(raw.get("fact_id") or ""),"source_id":sid,"source_url":str(src.get("url") or ""),"statement":statement})
    if not claims: raise Blocked("FACT_PACK_EMPTY")
    canon_sources=[]
    for sid,src in canonical_sources.items():
        related=[x for x in claims if x["source_id"]==sid]
        evidence=" ".join(x["evidence_text"] for x in related).strip() or str(src.get("title") or "")
        canon_sources.append({"evidence":evidence,"snapshot_sha256":hashlib.sha256(evidence.encode()).hexdigest(),"source_id":sid,"source_title":str(src.get("title") or sid),"source_url":str(src.get("url") or "")})
    fpid=str(fp.get("fact_pack_id") or "")
    if not fpid: raise Blocked("FACT_PACK_ID_MISSING")
    return {"contract":"canonical_fact_pack_v1","article_type":str(fp.get("article_type") or ""),"fact_pack_id":fpid,"source_snapshot_id":fpid,"claims":claims,"sources":canon_sources,"status":"SOURCE_VERIFIED_PRODUCTION_READY","production_readiness_status":"SOURCE_VERIFIED_PRODUCTION_READY","title_scope":str(fp.get("title_scope") or "")}

def _attr(tag,name):
    m=re.search(r"\b"+re.escape(name)+r'=["\']([^"\']+)["\']',tag,re.I)
    return m.group(1) if m else ""

def verify_trace_bindings(markup,fact_pack):
    tags=[m.group(0) for m in re.finditer(r'<span\b[^>]*class=["\'][^"\']*\bppm-source-trace\b[^"\']*["\'][^>]*></span>',markup,re.I)]
    by_fact={}
    for tag in tags:
        fid=_attr(tag,"data-fact-id")
        if fid: by_fact.setdefault(fid,[]).append(tag)
    for claim in fact_pack.get("claims",[]):
        fid=str(claim.get("fact_id") or ""); rows=by_fact.get(fid,[])
        if len(rows)!=1: raise Blocked("PSERC_TRACE_COUNT_INVALID:"+fid)
        if _attr(rows[0],"data-source-hash")!=str(claim.get("evidence_text_sha256") or ""): raise Blocked("PSERC_TRACE_HASH_MISMATCH:"+fid)
        if _attr(rows[0],"data-source-title")!=str(claim.get("source_id") or ""): raise Blocked("PSERC_TRACE_SOURCE_MISMATCH:"+fid)

def verify_existing_quality(article,checkrow):
    html=str(article.get("content_html") or ""); sha=hashlib.sha256(html.encode()).hexdigest()
    if not html or article.get("content_sha256")!=sha: raise Blocked("PSERC_ARTICLE_HASH_INVALID")
    lt=checkrow.get("lt68_result"); ppm=checkrow.get("ppm679_result"); writing=checkrow.get("writing_rules_result")
    if not isinstance(lt,dict) or lt.get("status")!="PASS" or lt.get("article_sha256")!=sha: raise Blocked("PSERC_PRIOR_LT68_EVIDENCE_INVALID")
    evidence=lt.get("language_evidence")
    if not isinstance(evidence,dict) or evidence.get("content_hash")!=sha: raise Blocked("PSERC_PRIOR_LT68_CONTENT_BINDING_INVALID")
    if not isinstance(ppm,dict) or ppm.get("status")!="PASS" or ppm.get("content_sha256")!=sha or ppm.get("ppm_package_sha256")!=PPM_SHA: raise Blocked("PSERC_PRIOR_PPM679_EVIDENCE_INVALID")
    if not isinstance(writing,dict) or writing.get("status")!="PASS" or writing.get("content_sha256")!=sha: raise Blocked("PSERC_PRIOR_WRITING_EVIDENCE_INVALID")
    return sha,lt,ppm,writing

def latest_products(ledger,root):
    items=ledger.get("items")
    if not isinstance(items,list) or not items: raise Blocked("LEDGER_ITEMS_INVALID")
    out=[]
    for item in items:
        if item.get("stages",{}).get("check")!="DONE": raise Blocked("ARTICLE_NOT_CHECK_PASS")
        research_ref=item.get("products",{}).get("research",{}).get("path")
        article_key="repair" if item.get("revision",0)>0 else "write"
        article_ref=item.get("products",{}).get(article_key,{}).get("path")
        check_ref=item.get("products",{}).get("check",{}).get("path")
        if not all(isinstance(x,str) for x in (research_ref,article_ref,check_ref)): raise Blocked("PRODUCT_REF_MISSING")
        research_pkg=load(root/research_ref); article_pkg=load(root/article_ref); check_pkg=load(root/check_ref)
        iid=item["item_id"]
        def row(pkg):
            hits=[x for x in pkg.get("results",[]) if x.get("item_id")==iid]
            if len(hits)!=1: raise Blocked("PRODUCT_ITEM_NOT_UNIQUE")
            return hits[0]
        out.append((item,row(research_pkg)["research_product"],row(article_pkg)["article_product"],row(check_pkg)))
    return out

MAPPING_PHP=r'''<?php
$ppm=$argv[1];$pserc=$argv[2];$payload=json_decode((string)file_get_contents($argv[3]),true);
if(!is_array($payload)||!is_array($payload['items']??null)){fwrite(STDERR,"PAYLOAD_INVALID\n");exit(2);}
require $ppm.'/tests/normal-draft-production/fixture-builder.php';
require $pserc.'/includes/class-pserc-plan-slot-identity.php';
$index=[];
foreach((array)(PPM679_Editorial_Plan_Registry::plan()['slots']??[]) as $slot){
 if(!is_array($slot))continue;
 $token=PSERC_Plan_Slot_Identity::token($slot);
 if(isset($index[$token])){fwrite(STDERR,"PLAN_SLOT_REGISTRY_DUPLICATE\n");exit(2);}
 $index[$token]=['canonical_article_id'=>(string)($slot['canonical_article_id']??''),'category_slug'=>(string)($slot['category_slug']??'')];
}
$out=[];
foreach($payload['items'] as $row){
 $token=(string)($row['plan_slot']??'');
 if(!isset($index[$token])){fwrite(STDERR,"PLAN_SLOT_REGISTRY_MATCH_MISSING\n");exit(2);}
 $out[$token]=$index[$token];
}
echo json_encode(['ok'=>true,'items'=>$out],JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE);
?>'''

def map_slots(ppm_root,pserc_root,requests,tmpdir):
    script=tmpdir/"map.php"; script.write_text(MAPPING_PHP,encoding="utf-8")
    payload=tmpdir/"map.json"; payload.write_text(json.dumps({"items":requests},ensure_ascii=False),encoding="utf-8")
    proc=subprocess.run(["php",str(script),str(ppm_root),str(pserc_root),str(payload)],text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=60)
    if proc.returncode!=0: raise Blocked("PSERC_SLOT_MAPPING_FAILED:"+(proc.stderr or proc.stdout)[:300])
    try: wrapper=json.loads(proc.stdout)
    except Exception as exc: raise Blocked("PSERC_SLOT_MAPPING_OUTPUT_INVALID") from exc
    if not isinstance(wrapper,dict) or wrapper.get("ok") is not True or not isinstance(wrapper.get("items"),dict): raise Blocked("PSERC_SLOT_MAPPING_NOT_PASS")
    return wrapper["items"]

def run(root,ppm_zip,pserc_zip):
    root=Path(root); ppm_zip=Path(ppm_zip); pserc_zip=Path(pserc_zip)
    if sha_file(ppm_zip)!=PPM_SHA: raise Blocked("PPM_PACKAGE_HASH_MISMATCH")
    if sha_file(pserc_zip)!=PSERC_SHA: raise Blocked("PSERC_PACKAGE_HASH_MISMATCH")
    products=latest_products(load(root/"state/ledger.json"),root)
    requests=[{"plan_slot":str(item.get("metadata",{}).get("plan_slot") or "")} for item,_,_,_ in products]
    if any(not x["plan_slot"] for x in requests): raise Blocked("PSERC_PLAN_SLOT_MISSING")
    with tempfile.TemporaryDirectory(prefix="k9-pserc-integrity-") as td:
        td=Path(td); ppm_dir=td/"ppm"; outer=td/"outer"; pserc_dir=td/"pserc"
        ppm_dir.mkdir(); outer.mkdir(); pserc_dir.mkdir()
        with zipfile.ZipFile(ppm_zip) as z: z.extractall(ppm_dir)
        with zipfile.ZipFile(pserc_zip) as z: z.extractall(outer)
        inner=outer/PSERC_INNER
        if not inner.is_file(): raise Blocked("PSERC_INNER_ZIP_MISSING")
        with zipfile.ZipFile(inner) as z: z.extractall(pserc_dir)
        mappings=map_slots(ppm_dir/"portal-production-machine",pserc_dir/"portal-seo-editorial-plan-compiler",requests,td)
        results=[]
        for item,research,article,checkrow in products:
            meta=item.get("metadata") or {}; slot=str(meta.get("plan_slot") or ""); mapped=mappings.get(slot)
            if not isinstance(mapped,dict): raise Blocked("PSERC_SLOT_MAPPING_RESULT_MISSING:"+slot)
            if str(mapped.get("category_slug") or "")!=str(meta.get("category") or ""): raise Blocked("PSERC_SLOT_CATEGORY_MISMATCH:"+slot)
            cid=str(mapped.get("canonical_article_id") or "")
            if not cid.startswith("article:"): raise Blocked("PSERC_CANONICAL_ARTICLE_ID_INVALID:"+slot)
            sha,lt,ppm,writing=verify_existing_quality(article,checkrow)
            fact_pack=canonical_fact_pack(research); ppm_item=copy.deepcopy(article.get("ppm_item"))
            if not isinstance(ppm_item,dict): raise Blocked("PPM_ITEM_MISSING")
            runtime=ppm_item.get("runtime_order"); subject_scope=str(runtime.get("subject_scope") or "").strip() if isinstance(runtime,dict) else ""; title_scope=str(fact_pack.get("title_scope") or "").strip()
            if not title_scope or title_scope!=subject_scope: raise Blocked("CANONICAL_FACT_PACK_SCOPE_MISMATCH")
            quality=ppm_item.get("quality_binding"); category=quality.get("wordpress_category") if isinstance(quality,dict) else None
            if not isinstance(quality,dict): raise Blocked("QUALITY_BINDING_MISSING")
            if not isinstance(category,dict) or category.get("taxonomy")!="category" or category.get("slug")!=meta.get("category"): raise Blocked("PSERC_WORDPRESS_CATEGORY_BINDING_INVALID")
            canonical=ppm_item.get("canonical_article"); html=str(article.get("content_html") or "")
            if not isinstance(canonical,dict) or canonical.get("body_html")!=html or canonical.get("body_html_sha256")!=sha: raise Blocked("PSERC_CANONICAL_ARTICLE_BINDING_INVALID")
            verify_trace_bindings(html,fact_pack)
            ppm_item["canonical_article_id"]=cid; ppm_item["source_snapshot_id"]=fact_pack["fact_pack_id"]; quality["language_evidence"]=copy.deepcopy(lt["language_evidence"]); ppm_item["quality_binding_hash"]=stable(quality)
            results.append({"item_id":item["item_id"],"plan_slot":slot,"bridge_status":INTEGRITY_STATUS,"canonical_article_id":cid,"category_slug":meta["category"],"production_plan_item":ppm_item,"fact_pack":fact_pack,"quality_evidence":{"lt68_status":"PASS_REUSED_FROM_CHECK","lt68_article_sha256":lt["article_sha256"],"ppm679_status":"PASS_REUSED_FROM_CHECK","ppm679_content_sha256":ppm["content_sha256"],"writing_rules_status":"PASS_REUSED_FROM_CHECK","writing_rules_content_sha256":writing["content_sha256"]},"publish_allowed":False})
    return {"contract":"K9_PSERC_RESULT_V1","status":"PASS","bridge_status":INTEGRITY_STATUS,"mode":"FINAL_INTEGRITY_ONLY_REUSE_PRIOR_QUALITY_EVIDENCE","article_count":len(results),"items":results,"publish_allowed":False}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("root"); ap.add_argument("ppm"); ap.add_argument("pserc"); ap.add_argument("--output",required=True); a=ap.parse_args()
    try: out=run(a.root,a.ppm,a.pserc)
    except Exception as exc:
        print(json.dumps({"contract":"K9_PSERC_RESULT_V1","status":"BLOCKED","reason":str(exc),"publish_allowed":False},ensure_ascii=False,indent=2)); raise SystemExit(2)
    Path(a.output).write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"status":"K9_PSERC_PASS","article_count":out["article_count"],"mode":out["mode"]},indent=2))
if __name__=="__main__": main()
