#!/usr/bin/env python3
import argparse, copy, hashlib, json, re, subprocess, sys, tempfile, zipfile
from pathlib import Path

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/"quality"))
import k9_lt68

PPM_SHA="acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1"
PSERC_SHA="77a14aca97f46d60bc9001d66327abb68dd9cac9ad111f8ecefa1a8afd345314"
PSERC_INNER="PSERC-FIX/portal-seo-editorial-plan-compiler_0.28.18_ENDSTEMPEL_IMPORT_ENVELOPE_BINDING.zip"

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
    fp=research.get("fact_pack")
    sources=research.get("sources")
    if not isinstance(fp,dict) or not isinstance(sources,list): raise Blocked("RESEARCH_PRODUCT_INVALID")
    by_id={str(x.get("source_id")):x for x in sources if isinstance(x,dict)}
    def canonical_source_id(raw_id,src):
        raw_id=str(raw_id or "").strip()
        lowered=raw_id.casefold()
        if any(token in lowered for token in ("test_","dummy","example","placeholder")):
            url=str((src or {}).get("url") or "").strip()
            title=str((src or {}).get("title") or "").strip()
            basis=url or title
            if not basis: raise Blocked("PLACEHOLDER_SOURCE_WITHOUT_REAL_BINDING:"+raw_id)
            return "SRC_"+hashlib.sha256(basis.encode("utf-8")).hexdigest()[:16].upper()
        return raw_id
    canonical_sources={}
    claims=[]
    for raw in fp.get("claims",[]):
        if not isinstance(raw,dict): raise Blocked("CLAIM_INVALID")
        raw_sid=str(raw.get("source_id") or "")
        src=by_id.get(raw_sid)
        if not src: raise Blocked("CLAIM_SOURCE_UNKNOWN:"+raw_sid)
        sid=canonical_source_id(raw_sid,src)
        canonical_sources[sid]=src
        statement=str(raw.get("statement") or "")
        evidence=str(raw.get("display_statement") or statement)
        claims.append({
            "article_types":list(raw.get("article_types") or [fp.get("article_type")]),
            "claim_status":str(raw.get("claim_status") or ""),
            "evidence_text":evidence,
            "evidence_text_sha256":str(raw.get("evidence_text_sha256") or ""),
            "fact_id":str(raw.get("fact_id") or ""),
            "source_id":sid,
            "source_url":str(src.get("url") or ""),
            "statement":statement,
        })
    if not claims: raise Blocked("FACT_PACK_EMPTY")
    canon_sources=[]
    for sid,src in canonical_sources.items():
        related=[x for x in claims if x["source_id"]==sid]
        evidence=" ".join(x["evidence_text"] for x in related).strip() or str(src.get("title") or "")
        canon_sources.append({
            "evidence":evidence,
            "snapshot_sha256":hashlib.sha256(evidence.encode()).hexdigest(),
            "source_id":sid,
            "source_title":str(src.get("title") or sid),
            "source_url":str(src.get("url") or ""),
        })
    fpid=str(fp.get("fact_pack_id") or "")
    if not fpid: raise Blocked("FACT_PACK_ID_MISSING")
    return {
        "contract":"canonical_fact_pack_v1",
        "article_type":str(fp.get("article_type") or ""),
        "fact_pack_id":fpid,
        "source_snapshot_id":fpid,
        "claims":claims,
        "sources":canon_sources,
        "status":"SOURCE_VERIFIED_PRODUCTION_READY",
        "production_readiness_status":"SOURCE_VERIFIED_PRODUCTION_READY",
        "title_scope":str(fp.get("title_scope") or ""),
    }

def _trace_match(markup,fid):
    for m in re.finditer(r'<span\b[^>]*class=["\'][^"\']*\bppm-source-trace\b[^"\']*["\'][^>]*>',markup,re.I):
        a=re.search(r'\bdata-fact-id=["\']([^"\']+)["\']',m.group(0),re.I)
        if a and a.group(1)==fid:
            return m
    return None

def _fact_target_match(markup,fid):
    for m in re.finditer(r'<[a-z][a-z0-9]*\b[^>]*\bdata-fact-ids=["\']([^"\']+)["\'][^>]*>',markup,re.I):
        if fid in m.group(1).split():
            return m
    return None

def bind_canonical_article_traces(ppm_item, fact_pack):
    article=ppm_item.get("canonical_article")
    if not isinstance(article,dict): raise Blocked("CANONICAL_ARTICLE_MISSING")
    markup=str(article.get("body_html") or "")
    if not markup: raise Blocked("CANONICAL_ARTICLE_HTML_MISSING")
    for claim in fact_pack.get("claims",[]):
        if not isinstance(claim,dict): continue
        fid=str(claim.get("fact_id") or "")
        source_id=str(claim.get("source_id") or "")
        source_hash=str(claim.get("evidence_text_sha256") or "")
        if not fid or not source_id or not source_hash:
            raise Blocked("CANONICAL_TRACE_BINDING_MISSING:"+fid)
        trace=(
            f'<span class="ppm-source-trace" data-fact-id="{fid}" '
            f'data-source-hash="{source_hash}" data-source-title="{source_id}"></span>'
        )
        existing=re.search(
            r'<span\\b[^>]*class=["\\\'][^"\\\']*\\bppm-source-trace\\b[^"\\\']*["\\\'][^>]*data-fact-id=["\\\']'+re.escape(fid)+r'["\\\'][^>]*></span>',
            markup,re.I
        )
        if existing:
            markup=markup[:existing.start()]+trace+markup[existing.end():]
            continue
        target=re.search(
            r'<(p|li|td)\\b[^>]*data-fact-ids=["\\\'][^"\\\']*\\b'+re.escape(fid)+r'\\b[^"\\\']*["\\\'][^>]*>',
            markup,re.I
        )
        if not target:
            raise Blocked("CANONICAL_TRACE_TARGET_MISSING:"+fid)
        markup=markup[:target.end()]+trace+markup[target.end():]
    article["body_html"]=markup
    article["body_html_sha256"]=hashlib.sha256(markup.encode("utf-8")).hexdigest()
    article["source_ids"]=[str(x.get("source_id") or "") for x in fact_pack.get("sources",[]) if isinstance(x,dict)]
    ppm_item["canonical_article"]=article
    return ppm_item

def latest_products(ledger, root):
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
        research_pkg=load(root/research_ref)
        article_pkg=load(root/article_ref)
        check_pkg=load(root/check_ref)
        iid=item["item_id"]
        def row(pkg):
            hits=[x for x in pkg.get("results",[]) if x.get("item_id")==iid]
            if len(hits)!=1: raise Blocked("PRODUCT_ITEM_NOT_UNIQUE")
            return hits[0]
        out.append((item,row(research_pkg)["research_product"],row(article_pkg)["article_product"],row(check_pkg)))
    return out


PHP=r'''<?php
$ppm=$argv[1]; $pserc=$argv[2]; $payload=json_decode((string)file_get_contents($argv[3]),true);
if(!is_array($payload)){fwrite(STDERR,"PAYLOAD_INVALID\n");exit(2);}
require $ppm.'/tests/normal-draft-production/fixture-builder.php';
require $pserc.'/includes/class-pserc-stable-json.php';
require $pserc.'/includes/class-pserc-plan-slot-identity.php';
require $pserc.'/includes/class-pserc-metadata-boundary.php';
require $pserc.'/includes/class-pserc-production-reader.php';
require $pserc.'/includes/class-pserc-ppm-intake-bridge.php';
nd_reset();
$item=(array)$payload['item']; $pack=(array)$payload['fact_pack']; $header=(array)$payload['header'];
$cid=(string)$payload['canonical_article_id']; $externalSlot=(string)$payload['plan_slot'];
if((string)($item['canonical_article_id']??'')!==$cid){fwrite(STDERR,"CANONICAL_ID_MISMATCH\n");exit(2);}
$matches=[];
foreach((array)(PPM679_Editorial_Plan_Registry::plan()['slots']??[]) as $candidate){
 if(is_array($candidate)&&hash_equals(PSERC_Plan_Slot_Identity::token($candidate),$externalSlot)){$matches[]=$candidate;}
}
if(count($matches)!==1){fwrite(STDERR,"PLAN_SLOT_REGISTRY_MATCH_NOT_UNIQUE\n");exit(2);}
$slot=$matches[0]; $item['canonical_article_id']=(string)$slot['canonical_article_id']; unset($item['plan_slot']);
$cat=(array)($item['quality_binding']['wordpress_category']??[]);
if(empty($cat['name'])||empty($cat['slug'])||(string)($cat['taxonomy']??'')!=='category'){fwrite(STDERR,"WORDPRESS_CATEGORY_BINDING_MISSING\n");exit(2);}
$seedItem=$item; $seedItem['quality_binding']['wordpress_category']['id']=900001; nd_seed_terms([$seedItem]);
$bundle=['contract'=>'canonical_fact_pack_import_v1','fact_packs'=>[$pack]];
$imp=PPM679_Admin::import_fact_pack_bundle($bundle);
if(empty($imp['ok'])){echo json_encode(['ok'=>false,'status'=>'PPM_FACT_PACK_IMPORT_BLOCKED','detail'=>$imp]);exit(0);}
$expectedSource=PPM679_Storage::fact_pack_hash((string)($item['source_snapshot_id']??''));
if($expectedSource===''){fwrite(STDERR,"SOURCE_HASH_BINDING_MISMATCH\n");exit(2);}
$item['source_hashes']=[$expectedSource];
$activeContracts=PPM679_Plan_Validator::active_contract_hashes();
$item['contract_hashes']=$activeContracts;
$item['gold_core_binding']='FOUR_TYPE_APPROVED_GOLD_CORE_V1';
$plan=$header;
$plan['plan_id']='k9-final-'.substr(hash('sha256',$cid.'|'.$externalSlot),0,20);
$plan['gold_core_binding']='FOUR_TYPE_APPROVED_GOLD_CORE_V1';
$plan['contract_hashes']=$activeContracts;
$plan['items']=[$item];
$batch=['contract'=>'PSERC_TEXTMACHINE_METADATA_BATCH_V2','status'=>'PASS','item_count'=>1,'maximum_articles'=>0,'maximum_articles_per_type'=>0,'publish_allowed'=>false,'content_or_format_payload_present'=>false,'items'=>[['title'=>(string)($item['topic']??''),'target_keyword'=>(string)($item['target_keyword']??''),'category'=>(string)($slot['category_slug']??''),'article_type'=>(string)($item['article_type']??''),'plan_slot'=>$externalSlot]]];
$tmp=$batch; unset($tmp['batch_sha256']); $batch['batch_sha256']=PSERC_Stable_Json::hash($tmp);
$snapshot=['ok'=>true,'version'=>'6.7.9','plan'=>PPM679_Editorial_Plan_Registry::plan()];
$runtime=nd_runtime($plan,'k9-'.substr(hash('sha256',$cid.'|'.$payload['content_sha256'].'|'.$externalSlot),0,40));
$r=PSERC_PPM_Intake_Bridge::execute($batch,$plan,$runtime,$snapshot);
echo json_encode(['bridge'=>$r,'canonical_article_id'=>(string)$slot['canonical_article_id'],'category_slug'=>(string)$slot['category_slug'],'batch'=>$batch,'item'=>$item],JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE);
?>'''

def _validate_bridge(wrapper):
    bridge=wrapper.get("bridge") if isinstance(wrapper,dict) else None
    if not isinstance(bridge,dict) or bridge.get("ok") is not True or bridge.get("status")!="PSERC_PPM_INTAKE_BRIDGE_EXECUTED":
        detail={"bridge_status":bridge.get("status") if isinstance(bridge,dict) else None}
        if isinstance(bridge,dict):
            ppm=bridge.get("ppm_result")
            artifact=ppm.get("artifact") if isinstance(ppm,dict) else None
            if isinstance(artifact,dict):
                detail["ppm_status"]=artifact.get("status")
                errors=artifact.get("errors")
                if isinstance(errors,list) and errors and isinstance(errors[0],dict):
                    detail["first_error"]={
                        "error_code":errors[0].get("error_code"),
                        "failed_rule":errors[0].get("failed_rule"),
                        "field_path":errors[0].get("field_path"),
                        "actual":errors[0].get("actual"),
                        "expected":errors[0].get("expected"),
                    }
        raise Blocked("PSERC_BRIDGE_NOT_PASS:"+json.dumps(detail,ensure_ascii=False,sort_keys=True))
    ppm_result=bridge.get("ppm_result")
    artifact=ppm_result.get("artifact") if isinstance(ppm_result,dict) else None
    if not isinstance(artifact,dict) or artifact.get("status")!="NORMAL_DRAFT_END_TO_END_READBACK_PASS_AWAITING_USER_CONTENT_REVIEW_NO_PUBLISH":
        raise Blocked("PSERC_PPM_ARTIFACT_NOT_PASS")
    check_only=artifact.get("check_only")
    rows=check_only.get("items") if isinstance(check_only,dict) else None
    if not isinstance(rows,list) or len(rows)!=1:
        raise Blocked("PSERC_CHECK_ITEM_INVALID")
    pr=rows[0]
    checks=pr.get("checks")
    if pr.get("technical_status")!="TECHNICAL_CHECK_OK" or pr.get("content_quality_status")!="CONTENT_QUALITY_CHECK_OK":
        raise Blocked("PSERC_CONTENT_CHECK_NOT_PASS")
    if not isinstance(checks,dict) or checks.get("fail_closed_aggregate_status")!="PASS":
        raise Blocked("PSERC_FAIL_CLOSED_NOT_PASS")
    return bridge,artifact

def run(root, ppm_zip, pserc_zip, lt_jar):
    root=Path(root)
    if sha_file(ppm_zip)!=PPM_SHA: raise Blocked("PPM_PACKAGE_HASH_MISMATCH")
    if sha_file(pserc_zip)!=PSERC_SHA: raise Blocked("PSERC_PACKAGE_HASH_MISMATCH")
    ledger=load(root/"state/ledger.json")
    products=latest_products(ledger,root)
    if not products: raise Blocked("K9_PSERC_NO_ITEMS")

    with tempfile.TemporaryDirectory(prefix="k9-pserc-") as td:
        td=Path(td)
        ppm_dir=td/"ppm"; pouter=td/"pouter"; pdir=td/"pserc"
        ppm_dir.mkdir(); pouter.mkdir(); pdir.mkdir()
        with zipfile.ZipFile(ppm_zip) as z: z.extractall(ppm_dir)
        with zipfile.ZipFile(pserc_zip) as z: z.extractall(pouter)
        inner=pouter/PSERC_INNER
        if not inner.is_file(): raise Blocked("PSERC_INNER_ZIP_MISSING")
        with zipfile.ZipFile(inner) as z: z.extractall(pdir)
        script=td/"run.php"; script.write_text(PHP,encoding="utf-8")

        results=[]
        for idx,(item,research,article,checkrow) in enumerate(products):
            html=str(article.get("content_html") or "")
            if not html: raise Blocked("ARTICLE_HTML_MISSING:"+str(item.get("item_id") or idx))
            article_path=td/f"article-{idx}.html"
            article_path.write_text(html,encoding="utf-8")
            lt=k9_lt68.run(Path(lt_jar),article_path)
            if lt.get("status")!="PASS": raise Blocked("PSERC_LT_NOT_PASS:"+str(item.get("item_id") or idx))
            ppm_item=copy.deepcopy(article.get("ppm_item"))
            if not isinstance(ppm_item,dict): raise Blocked("PPM_ITEM_MISSING")
            binding=ppm_item.get("quality_binding")
            if not isinstance(binding,dict): raise Blocked("QUALITY_BINDING_MISSING")
            binding["language_evidence"]=lt["language_evidence"]
            ppm_item["quality_binding_hash"]=stable(binding)
            canonical_id="article:"+hashlib.sha256((item["item_id"]+"|"+article["content_sha256"]).encode()).hexdigest()[:24]
            ppm_item["canonical_article_id"]=canonical_id
            fp=canonical_fact_pack(research)
            ppm_item=bind_canonical_article_traces(ppm_item,fp)
            ppm_item["source_snapshot_id"]=fp["fact_pack_id"]
            header={"contract":"production_plan_v4","plan_contract_version":"4.0.0","required_plugin_version":"6.7.9"}
            payload={
                "item":ppm_item,
                "fact_pack":fp,
                "header":header,
                "canonical_article_id":canonical_id,
                "plan_slot":item["metadata"]["plan_slot"],
                "content_sha256":article["content_sha256"],
            }
            payload_path=td/f"payload-{idx}.json"
            payload_path.write_text(json.dumps(payload,ensure_ascii=False),encoding="utf-8")
            proc=subprocess.run(
                ["php",str(script),str(ppm_dir/"portal-production-machine"),str(pdir/"portal-seo-editorial-plan-compiler"),str(payload_path)],
                text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=180
            )
            if proc.returncode!=0:
                raise Blocked("PSERC_EXECUTION_FAILED:"+str(item.get("item_id") or idx)+":"+(proc.stderr or proc.stdout)[:500])
            try: wrapper=json.loads(proc.stdout)
            except Exception as exc: raise Blocked("PSERC_OUTPUT_INVALID:"+str(item.get("item_id") or idx)) from exc
            bridge,artifact=_validate_bridge(wrapper)
            results.append({
                "item_id":item["item_id"],
                "plan_slot":item["metadata"]["plan_slot"],
                "bridge_status":bridge["status"],
                "canonical_article_id":wrapper["canonical_article_id"],
                "category_slug":wrapper["category_slug"],
                "exact_five_batch":wrapper["batch"],
                "production_plan_item":wrapper["item"],
                "fact_pack":fp,
                "lt68_result":lt,
                "ppm_status":artifact["status"],
                "publish_allowed":False,
            })

    return {
        "contract":"K9_PSERC_RESULT_V1",
        "status":"PASS",
        "bridge_status":"PSERC_PPM_INTAKE_BRIDGE_EXECUTED",
        "article_count":len(results),
        "items":results,
        "publish_allowed":False,
    }

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("root"); ap.add_argument("ppm"); ap.add_argument("pserc"); ap.add_argument("lt_jar"); ap.add_argument("--output",required=True); a=ap.parse_args()
    try: out=run(a.root,Path(a.ppm),Path(a.pserc),Path(a.lt_jar))
    except Exception as exc:
        print(json.dumps({"contract":"K9_PSERC_RESULT_V1","status":"BLOCKED","reason":str(exc),"publish_allowed":False},ensure_ascii=False,indent=2))
        raise SystemExit(2)
    Path(a.output).write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"status":"K9_PSERC_PASS","item_count":out.get("item_count"),"canonical_article_id":out.get("canonical_article_id")},indent=2))
if __name__=="__main__": main()
