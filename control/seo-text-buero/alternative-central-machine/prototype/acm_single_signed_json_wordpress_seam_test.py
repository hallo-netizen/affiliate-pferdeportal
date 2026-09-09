#!/usr/bin/env python3
from __future__ import annotations

import base64, copy, hashlib, importlib.util, json, subprocess, sys, tempfile, zipfile
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

REPO=Path(__file__).resolve().parents[4]
PPM=REPO/"control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip"
DUAL=REPO/"control/startmaster0107/STARTMASTER0107_DUAL_ROOTFIX_REPAIR.py"
H7=REPO/"control/single-door-boundary/single_door_preproduction_handoff.py"
WP_CAND=Path(__file__).resolve().parent/"acm_wp_signed_package_verifier_candidate.php"

def mod(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    if spec is None or spec.loader is None: raise RuntimeError("MODULE_LOAD_FAILED:"+path.name)
    m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m

def run(cmd,cwd,timeout=180):
    return subprocess.run(cmd,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=timeout)

def dump(path,obj):
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

def php_quote(path):
    return str(path).replace("\\","\\\\").replace("'","\\'")

def build_context(ppm):
    helper=ppm/"acm-single-json-context.php"
    helper.write_text(r'''<?php
require __DIR__.'/tests/normal-draft-production/fixture-builder.php';
nd_reset();
$p=nd_build_plan(1,'acm-single-json');
$item=$p['items'][0];
$pack=PPM679_Storage::load_fact_pack($item['source_snapshot_id']);
$header=$p; unset($header['items']);
echo json_encode([
  'plan'=>$p,
  'pack'=>$pack,
  'canonical_article_id'=>$item['canonical_article_id']
],JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);
?>''',encoding="utf-8")
    cp=run(["php",str(helper)],ppm)
    if cp.returncode!=0: raise RuntimeError("CONTEXT_BUILD_FAILED:"+cp.stdout[-3000:])
    return json.loads(cp.stdout)

def release_meta(dual,batch,count):
    base={
      "article_origin_policy":"POST_TEXT_SIGNED_0039_ORIGIN_AND_NO_REWRITE",
      "authoring_prompt_sha256":"b"*64,
      "authoring_role":"BOUND_EXISTING_FACHWORKFLOW_ONLY",
      "content_generation_performed_by_supervisor":False,
      "contract":"WORKFLOW_SUPERVISOR_RELEASE_V2_SIGNED",
      "created_at_utc":"2026-09-09T00:00:00+00:00",
      "exact_five_batch_sha256":batch,
      "exact_five_item_count":count,
      "frozen_workflow_sha256":"e"*64,
      "nullpunkt":{},
      "nullpunkt_sha256":"f"*64,
      "ppm_baseline_sha256":"1"*64,
      "ppm_version":"6.7.9",
      "research_evidence_policy":"BOUND_EXISTING_FACHWORKFLOW_ONLY",
      "sequence":107008,
      "status":"PASS",
      "wordpress_write_performed":False,
    }
    if set(base)!=set(dual.RELEASE_META_KEYS):
        raise RuntimeError("RELEASE_META_SCHEMA_DRIFT:"+str(sorted(set(dual.RELEASE_META_KEYS)-set(base))))
    return base

def make_package(dual,private,pub_b64,pub_sha,kid,ctx,batch,plan_slot):
    plan=ctx["plan"]
    pack=ctx["pack"]
    bundle={"contract":"canonical_fact_pack_import_v1","created_at":"2026-09-09T00:00:00+00:00","fact_packs":[pack]}
    rel_item={"plan_slot":plan_slot,"canonical_article_id":ctx["canonical_article_id"]}
    meta=release_meta(dual,batch,1)
    c={"source":"ACM_SINGLE_JSON_TEST","fact_pack_bundle":bundle,"production_plan":plan,
       "workflow_release_metadata":meta,"workflow_release_items":[rel_item]}
    signer=lambda h: base64.b64encode(private.sign(h.encode("ascii"))).decode("ascii")
    return dual.build_package(c,signer,kid,pub_sha,pub_b64,False)

def resign(dual,pkg,private):
    release=pkg["workflow_release"]
    payload=dict(release)
    for k in ("release_payload_sha256","signature_b64","release_sha256"):payload.pop(k,None)
    ph=dual.stable(payload)
    release["release_payload_sha256"]=ph
    release["signature_b64"]=base64.b64encode(private.sign(ph.encode("ascii"))).decode("ascii")
    rc=dict(release);rc.pop("release_sha256",None)
    release["release_sha256"]=dual.stable(rc)
    pkg["workflow_release_sha256"]=dual.stable(release)
    pkg["fact_pack_bundle_sha256"]=dual.stable(pkg["fact_pack_bundle"])
    pkg["production_plan_sha256"]=dual.stable(pkg["production_plan"])
    pkg["package_id"]=dual.stable({
      "contract":pkg["contract"],
      "fact_pack_bundle_sha256":pkg["fact_pack_bundle_sha256"],
      "production_plan_sha256":pkg["production_plan_sha256"],
      "workflow_release_sha256":pkg["workflow_release_sha256"],
    })
    pc=dict(pkg);pc.pop("package_payload_sha256",None)
    pkg["package_payload_sha256"]=dual.stable(pc)
    return pkg

def rehash_without_resign(dual,pkg):
    release=pkg["workflow_release"]
    pkg["fact_pack_bundle_sha256"]=dual.stable(pkg["fact_pack_bundle"])
    pkg["production_plan_sha256"]=dual.stable(pkg["production_plan"])
    release["fact_pack_bundle_sha256"]=pkg["fact_pack_bundle_sha256"]
    release["production_plan_sha256"]=pkg["production_plan_sha256"]
    payload=dict(release)
    for k in ("release_payload_sha256","signature_b64","release_sha256"):payload.pop(k,None)
    release["release_payload_sha256"]=dual.stable(payload)
    # leave signature_b64 unchanged deliberately
    rc=dict(release);rc.pop("release_sha256",None)
    release["release_sha256"]=dual.stable(rc)
    pkg["workflow_release_sha256"]=dual.stable(release)
    pkg["package_id"]=dual.stable({
      "contract":pkg["contract"],
      "fact_pack_bundle_sha256":pkg["fact_pack_bundle_sha256"],
      "production_plan_sha256":pkg["production_plan_sha256"],
      "workflow_release_sha256":pkg["workflow_release_sha256"],
    })
    pc=dict(pkg);pc.pop("package_payload_sha256",None)
    pkg["package_payload_sha256"]=dual.stable(pc)
    return pkg

def wp_verify_only(final, trusted, used=False):
    script=final.parent/"verify.php"
    trusted_json=json.dumps(trusted,separators=(",",":")).replace("\\","\\\\").replace("'","\\'")
    script.write_text(
      "<?php require '"+php_quote(WP_CAND)+"';"
      +"$trusted=json_decode('"+trusted_json+"',true);"
      +"try{$r=acm_wp_verify_signed_package($argv[1],$trusted,function($b){return "+("true" if used else "false")+";});"
      +"echo json_encode($r,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);exit(0);}"
      +"catch(Throwable $e){echo $e->getMessage();exit(2);}?>",
      encoding="utf-8")
    return run(["php",str(script),str(final)],final.parent)

def wp_full_import(final,trusted,ppm):
    script=ppm/"acm-single-json-import.php"
    trusted_json=json.dumps(trusted,separators=(",",":")).replace("\\","\\\\").replace("'","\\'")
    script.write_text(r'''<?php
require __DIR__.'/tests/normal-draft-production/fixture-builder.php';
require $argv[2];
$trusted=json_decode($argv[3],true);
nd_reset();
$beforeDraft=count(PPM679_WP::get_all_post_inventory(['draft']));
$beforePublish=count(PPM679_WP::get_all_post_inventory(['publish']));
try{
  $verified=acm_wp_verify_signed_package($argv[1],$trusted,function($b){return false;});
  $bundle=$verified['fact_pack_bundle'];$plan=$verified['production_plan'];
  nd_seed_terms($plan['items']);
  $imp=PPM679_Admin::import_fact_pack_bundle($bundle);
  if(empty($imp['ok'])){echo json_encode(['status'=>'BLOCKED_FACTPACK_IMPORT','detail'=>$imp]);exit(3);}
  $runtime=nd_runtime($plan,'acm-single-json-wp');
  $result=PPM679_Normal_Draft_Pipeline::execute_plan($plan,$runtime);
  $artifact=is_array($result)?($result['artifact']??null):null;
  $afterDraft=count(PPM679_WP::get_all_post_inventory(['draft']));
  $afterPublish=count(PPM679_WP::get_all_post_inventory(['publish']));
  echo json_encode([
    'status'=>'ACM_SINGLE_JSON_WP_RESULT',
    'verified_status'=>$verified['status'],
    'pipeline_status'=>is_array($artifact)?($artifact['status']??null):null,
    'before_draft'=>$beforeDraft,'after_draft'=>$afterDraft,
    'before_publish'=>$beforePublish,'after_publish'=>$afterPublish,
    'publish_allowed'=>false
  ],JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);
  exit(0);
}catch(Throwable $e){echo json_encode(['status'=>'ACM_SINGLE_JSON_WP_BLOCKED','reason'=>$e->getMessage(),'publish_allowed'=>false]);exit(2);}
?>''',encoding="utf-8")
    return run(["php",str(script),str(final),str(WP_CAND),json.dumps(trusted,separators=(",",":"))],ppm)

def expect_block(cp,label):
    if cp.returncode==0: raise RuntimeError("NEGATIVE_NOT_BLOCKED:"+label+":"+cp.stdout[-1000:])
    return label

def main():
    dual=mod(DUAL,"acm_single_json_dual")
    h7=mod(H7,"acm_single_json_h7")
    private=Ed25519PrivateKey.generate()
    raw_pub=private.public_key().public_bytes(encoding=serialization.Encoding.Raw,format=serialization.PublicFormat.Raw)
    pub_b64=base64.b64encode(raw_pub).decode("ascii");pub_sha=hashlib.sha256(raw_pub).hexdigest();kid="acm-test-"+pub_sha[:16]
    trusted={kid:{"sha256":pub_sha,"public_key_b64":pub_b64}}
    batch=hashlib.sha256(b"acm-single-json-batch").hexdigest();slot="a"*64

    with tempfile.TemporaryDirectory() as td:
        root=Path(td);ppm_out=root/"ppm";ppm_out.mkdir()
        with zipfile.ZipFile(PPM) as z:z.extractall(ppm_out)
        ppm=ppm_out/"portal-production-machine"
        ctx=build_context(ppm)
        pkg=make_package(dual,private,pub_b64,pub_sha,kid,ctx,batch,slot)
        final=root/"PFERDE_ATELIER_SIGNED_ARTICLE_BATCH_FINAL.json";dump(final,pkg)

        proof=h7.validate_production_package(final,trusted_keys=trusted)
        if proof.get("status")!="SIGNED_PRODUCTION_PACKAGE_HANDOFF_VALID":raise RuntimeError("H7_PACKAGE_NOT_VALID")

        positive=wp_full_import(final,trusted,ppm)
        if positive.returncode!=0:raise RuntimeError("WP_POSITIVE_FAILED:"+positive.stdout[-4000:])
        pos=json.loads(positive.stdout)
        if pos.get("verified_status")!="SIGNED_JSON_VERIFIED_FOR_EXISTING_IMPORT_HANDOFF":raise RuntimeError("WP_VERIFY_STATUS_WRONG")
        if pos.get("after_draft")!=pos.get("before_draft")+1:raise RuntimeError("WP_NOT_EXACT_ONE_DRAFT")
        if pos.get("after_publish")!=pos.get("before_publish"):raise RuntimeError("WP_PUBLISH_CHANGED")
        if pos.get("pipeline_status")!="NORMAL_DRAFT_END_TO_END_READBACK_PASS_AWAITING_USER_CONTENT_REVIEW_NO_PUBLISH":
            raise RuntimeError("WP_PIPELINE_NOT_FULL_PASS:"+str(pos.get("pipeline_status")))

        negatives=[]
        def unsigned_tamper(label,mut):
            bad=copy.deepcopy(pkg);mut(bad);rehash_without_resign(dual,bad);p=root/(label+".json");dump(p,bad)
            negatives.append(expect_block(wp_verify_only(p,trusted),label))
        unsigned_tamper("tamper_title",lambda x:x["production_plan"]["items"][0].__setitem__("topic",str(x["production_plan"]["items"][0].get("topic",""))+"X"))
        unsigned_tamper("tamper_keyword",lambda x:x["production_plan"]["items"][0].__setitem__("target_keyword",str(x["production_plan"]["items"][0].get("target_keyword",""))+"X"))
        unsigned_tamper("tamper_article_type",lambda x:x["production_plan"]["items"][0].__setitem__("article_type","FAQ" if x["production_plan"]["items"][0].get("article_type")!="FAQ" else "Beratung"))
        unsigned_tamper("tamper_plan_slot",lambda x:x["workflow_release"]["items"][0].__setitem__("plan_slot","b"*64))
        unsigned_tamper("tamper_canonical_id",lambda x:x["workflow_release"]["items"][0].__setitem__("canonical_article_id","article:tampered"))
        def tamper_body(x):
            a=x["production_plan"]["items"][0]["canonical_article"];a["body_html"]=a["body_html"]+"X";a["body_html_sha256"]=hashlib.sha256(a["body_html"].encode()).hexdigest()
        unsigned_tamper("tamper_body",tamper_body)
        def tamper_pack(x):
            x["fact_pack_bundle"]["fact_packs"][0]["facts"][0]["claim"]=str(x["fact_pack_bundle"]["fact_packs"][0]["facts"][0].get("claim",""))+"X"
        unsigned_tamper("tamper_fact_pack",tamper_pack)

        extra=copy.deepcopy(pkg);extra["route_selectable"]=True;p=root/"extra_route.json";dump(p,extra)
        negatives.append(expect_block(wp_verify_only(p,trusted),"extra_route_field"))

        wrong=Ed25519PrivateKey.generate();wrong_pub=wrong.public_key().public_bytes(encoding=serialization.Encoding.Raw,format=serialization.PublicFormat.Raw)
        wrong_trusted={kid:{"sha256":hashlib.sha256(wrong_pub).hexdigest(),"public_key_b64":base64.b64encode(wrong_pub).decode()}}
        negatives.append(expect_block(wp_verify_only(final,wrong_trusted),"wrong_public_key"))
        negatives.append(expect_block(wp_verify_only(final,trusted,used=True),"replay"))

        # Signed bad inputs: even an authorized signer cannot create publish freedom
        # or bypass the legacy M34/M35 PPM protections.
        badslot=copy.deepcopy(pkg);badslot["production_plan"]["items"][0]["plan_slot"]=slot;resign(dual,badslot,private);p=root/"signed_foreign_plan_slot.json";dump(p,badslot)
        negatives.append(expect_block(wp_verify_only(p,trusted),"signed_foreign_plan_slot"))

        badcid=copy.deepcopy(pkg);badcid["workflow_release"]["items"][0]["canonical_article_id"]="article:not-in-plan";resign(dual,badcid,private);p=root/"signed_release_plan_id_mismatch.json";dump(p,badcid)
        negatives.append(expect_block(wp_verify_only(p,trusted),"signed_release_plan_id_mismatch"))

        badsource=copy.deepcopy(pkg);badsource["production_plan"]["items"][0]["source_hashes"]=["0"*64];resign(dual,badsource,private);p=root/"signed_bad_source_hash.json";dump(p,badsource)
        cp=wp_full_import(p,trusted,ppm)
        if cp.returncode==0:
            obj=json.loads(cp.stdout)
            if not str(obj.get("pipeline_status") or "").startswith("BLOCKED_"):
                raise RuntimeError("SIGNED_BAD_SOURCE_HASH_NOT_BLOCKED:"+cp.stdout[-2000:])
        negatives.append("signed_bad_source_hash")

        pubwish=copy.deepcopy(pkg);pubwish["production_plan"]["items"][0]["post_status"]="publish";resign(dual,pubwish,private);p=root/"signed_publish_wish.json";dump(p,pubwish)
        cp=wp_full_import(p,trusted,ppm)
        if cp.returncode==0:
            obj=json.loads(cp.stdout)
            if obj.get("after_publish")!=obj.get("before_publish"):
                raise RuntimeError("SIGNED_PUBLISH_WISH_CHANGED_PUBLISH_COUNT")
            # PASS-as-draft or BLOCK are both safe: the field has zero publish authority.
            if not (obj.get("pipeline_status")=="NORMAL_DRAFT_END_TO_END_READBACK_PASS_AWAITING_USER_CONTENT_REVIEW_NO_PUBLISH" or str(obj.get("pipeline_status") or "").startswith("BLOCKED_")):
                raise RuntimeError("SIGNED_PUBLISH_WISH_UNEXPECTED:"+cp.stdout[-2000:])
        negatives.append("signed_publish_wish_no_publish_authority")

        print(json.dumps({
          "status":"ACM_SINGLE_SIGNED_JSON_WORDPRESS_SEAM_PASS",
          "package_contract":"PSERC_APPROVED_PRODUCTION_PACKAGE_V1",
          "single_json_only":True,
          "existing_wordpress_signature_entry_lock_reused":True,
          "existing_ppm_fact_pack_import_reused":True,
          "existing_ppm_normal_draft_pipeline_reused":True,
          "existing_textmachine_rules_changed":False,
          "new_import_logic_created":False,
          "new_package_contract_created":False,
          "positive":{
            "h7_signed_package_valid":True,
            "wordpress_verify_before_write":True,
            "exactly_one_draft":True,
            "readback_pipeline_pass":True,
            "publish_count_unchanged":True,
          },
          "negative_tests":negatives,
          "negative_count":len(negatives),
          "private_key_in_wordpress":False,
          "manual_user_review_after_draft":True,
          "auto_publish":False,
          "publish_allowed":False
        },ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
