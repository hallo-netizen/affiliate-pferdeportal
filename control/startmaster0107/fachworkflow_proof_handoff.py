#!/usr/bin/env python3
"""Hash-bound handoff from raw Fachworkflow work to one aggregate PASS."""
from __future__ import annotations
import hashlib, json, os, re, subprocess, sys, tempfile, zipfile
from pathlib import Path
from typing import Any, Mapping

REPO = Path(__file__).resolve().parents[2]
SELF_REL = "control/startmaster0107/fachworkflow_proof_handoff.py"
ACTION_REL = "control/single-door-boundary/codex_current_action.py"
STATE_REL = "control/startmaster0107/CURRENT_STATE.json"
RUNTIME_STATE_REL = "control/startmaster0107/runtime_inbox/RUNTIME_INBOX_STATE.json"
TOOLBOX_REL = "control/startmaster0107/codex-production-runtime/RUNTIME_TOOLBOX_MANIFEST.json"
LT_RUNTIME_REL = ".pferde-environment/LANGUAGETOOL_RUNTIME.json"
CONTRACT = "PFERDE_ATELIER_FACHWORKFLOW_HANDOFF_REQUEST_V1"
PASS_CONTRACT = "PFERDE_ATELIER_FACHWORKFLOW_PASS_V1"
AGGREGATE_CONTRACT = "PFERDE_ATELIER_EXISTING_VALIDATORS_AGGREGATE_V1"
RECEIPT_CONTRACT = "PFERDE_ATELIER_BOUND_ITEM_EXECUTION_RECEIPT_V1"
PPM679_VERSION = "6.7.9"
PPM679_PACKAGE_SHA256 = "acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1"
PPM679_RULESET_SHA256 = "dc79a6d7d30fba2f7f13c80d35bf4d137669f2b3469d7bc28a5d0873858f192f"
PSERC_FIX_PACKAGE_SHA256 = "77a14aca97f46d60bc9001d66327abb68dd9cac9ad111f8ecefa1a8afd345314"
PPM679_PACKAGE_REL = "control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip"
PSERC_FIX_PACKAGE_REL = "control/startmaster0107/runtime_packages/PSERC-FIX.zip"
PSERC_INNER_ZIP = "PSERC-FIX/portal-seo-editorial-plan-compiler_0.28.18_ENDSTEMPEL_IMPORT_ENVELOPE_BINDING.zip"
LT_ENGINE = "LanguageTool 6.8 / Bestand 43"
REQUEST_FIELDS = {
    "contract", "room_token", "batch_sha256", "canonical_article_id", "plan_slot",
    "allowed_output_root", "item_receipt_ref", "fachworkflow_pass_ref",
    "contract_binding_ref", "contract_binding_sha256", "stage_proofs",
    "fact_pack", "production_plan_item", "production_plan_header",
    "workflow_release_item", "workflow_release_metadata",
}

class Blocked(RuntimeError): pass

def _load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict): raise Blocked("JSON_OBJECT_REQUIRED")
    return value

def _sha(path: Path) -> str: return hashlib.sha256(path.read_bytes()).hexdigest()

def _safe_repo(repo: Path, ref: str) -> Path:
    p = Path(str(ref or ""))
    if not str(ref or "") or p.is_absolute() or ".." in p.parts: raise Blocked("INVALID_RELATIVE_REF")
    out = (repo / p).resolve(); root = repo.resolve()
    if out != root and root not in out.parents: raise Blocked("REF_ESCAPE")
    return out

def _path(repo: Path, ref: str, root: str) -> Path:
    if not str(ref).startswith(root): raise Blocked("PROOF_REF_OUTSIDE_BOUND_OUTPUT_ROOT")
    result = _safe_repo(repo, ref); base = _safe_repo(repo, root.rstrip("/"))
    if result != base and base not in result.parents: raise Blocked("PROOF_REF_ESCAPE")
    return result

def _write_json(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True); tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"); tmp.replace(path)

def _write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True); tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(value, encoding="utf-8"); tmp.replace(path)

def _assert_bound_adapters(repo: Path) -> None:
    state = _load(repo / STATE_REL); gate = state.get("execution_gate") or {}
    step_ref = str(gate.get("bundle_ref") or ""); step_sha = str(gate.get("bundle_sha256") or "")
    step_path = _safe_repo(repo, step_ref)
    if not step_path.is_file() or _sha(step_path) != step_sha: raise Blocked("CURRENT_107007_BUNDLE_HASH_MISMATCH")
    step = _load(step_path)
    bindings = {str(x.get("ref") or ""): str(x.get("sha256") or "") for x in (step.get("authorized_inputs") or []) if isinstance(x, dict)}
    for ref in (SELF_REL, ACTION_REL):
        p = repo / ref
        if not p.is_file() or bindings.get(ref) != _sha(p): raise Blocked("AUTHORIZED_INPUT_HASH_MISMATCH:" + ref)

def _runtime_context(repo: Path, batch: str) -> dict:
    state = _load(repo / RUNTIME_STATE_REL)
    if state.get("status") != "EXECUTION_READY" or state.get("publish_allowed") is not False: raise Blocked("RUNTIME_NOT_EXECUTION_READY")
    if state.get("batch_sha256") != batch: raise Blocked("RUNTIME_BATCH_MISMATCH")
    source_ref = str(state.get("source_snapshot_ref") or ""); source_path = _safe_repo(repo, source_ref)
    source_sha = str(state.get("source_snapshot_sha256") or "")
    if not source_path.is_file() or _sha(source_path) != source_sha: raise Blocked("RUNTIME_SOURCE_SNAPSHOT_HASH_MISMATCH")
    source = _load(source_path)
    package_ref = str(state.get("production_package_ref") or ""); package_path = _safe_repo(repo, package_ref)
    package_sha = str(state.get("production_package_sha256") or "")
    if not package_path.is_file() or _sha(package_path) != package_sha: raise Blocked("RUNTIME_PRODUCTION_PACKAGE_HASH_MISMATCH")
    package = _load(package_path); release = package.get("workflow_release")
    release_items = release.get("items") if isinstance(release, dict) else None
    if not isinstance(release, dict) or not isinstance(release_items, list) or not release_items: raise Blocked("RUNTIME_WORKFLOW_RELEASE_INVALID")
    if release.get("exact_five_batch_sha256") != batch: raise Blocked("RUNTIME_RELEASE_BATCH_MISMATCH")
    if int(release.get("exact_five_item_count") or -1) != len(release_items): raise Blocked("RUNTIME_RELEASE_COUNT_MISMATCH")
    if release.get("wordpress_write_performed") is not False: raise Blocked("RUNTIME_RELEASE_WORDPRESS_WRITE_FORBIDDEN")
    meta_batch = source.get("next_textmachine_metadata_batch"); meta_items = meta_batch.get("items") if isinstance(meta_batch, dict) else None
    if not isinstance(meta_batch, dict) or meta_batch.get("batch_sha256") != batch or not isinstance(meta_items, list): raise Blocked("RUNTIME_METADATA_BATCH_INVALID")
    if len(meta_items) != len(release_items): raise Blocked("RUNTIME_METADATA_COUNT_MISMATCH")
    plan = package.get("production_plan")
    if not isinstance(plan, dict) or plan.get("contract") != "production_plan_v4": raise Blocked("RUNTIME_PRODUCTION_PLAN_HEADER_INVALID")
    plan_header = dict(plan); plan_header.pop("items", None)
    release_metadata = dict(release); release_metadata.pop("items", None)
    return {"state":state,"release_items":release_items,"meta_items":meta_items,"plan_header":plan_header,"release_metadata":release_metadata,"source_sha256":source_sha,"package_sha256":package_sha}

def _bound_item(ctx: Mapping[str, Any], canonical_id: str, slot: str) -> tuple[dict, dict]:
    metas=[x for x in ctx["meta_items"] if isinstance(x,dict) and str(x.get("plan_slot") or "")==slot]
    rels=[x for x in ctx["release_items"] if isinstance(x,dict) and str(x.get("plan_slot") or "")==slot]
    if len(metas)!=1 or len(rels)!=1: raise Blocked("BOUND_RUNTIME_ITEM_NOT_UNIQUE")
    meta=dict(metas[0]); rel=dict(rels[0])
    if rel.get("canonical_article_id")!=canonical_id: raise Blocked("BOUND_RUNTIME_CANONICAL_ID_MISMATCH")
    return meta,rel

def _validate_raw_context(request: Mapping[str, Any], ctx: Mapping[str, Any], meta: Mapping[str, Any], release_item: Mapping[str, Any]) -> dict:
    fact_pack=request.get("fact_pack"); item=request.get("production_plan_item")
    if not isinstance(fact_pack,dict) or not fact_pack: raise Blocked("BOUND_FACT_PACK_MISSING")
    if not isinstance(item,dict) or not item: raise Blocked("BOUND_PRODUCTION_PLAN_ITEM_MISSING")
    if request.get("production_plan_header")!=ctx["plan_header"]: raise Blocked("BOUND_PRODUCTION_PLAN_HEADER_MISMATCH")
    if request.get("workflow_release_item")!=release_item: raise Blocked("BOUND_WORKFLOW_RELEASE_ITEM_MISMATCH")
    if request.get("workflow_release_metadata")!=ctx["release_metadata"]: raise Blocked("BOUND_WORKFLOW_RELEASE_METADATA_MISMATCH")
    expected={"canonical_article_id":request["canonical_article_id"],"plan_slot":request["plan_slot"],"article_type":meta.get("article_type"),"target_keyword":meta.get("target_keyword"),"topic":meta.get("title")}
    for k,v in expected.items():
        if item.get(k)!=v: raise Blocked("BOUND_PRODUCTION_PLAN_ITEM_MISMATCH:"+k)
    quality=item.get("quality_binding"); category=quality.get("wordpress_category") if isinstance(quality,dict) else None
    if not isinstance(category,dict) or category.get("slug")!=meta.get("category") or category.get("taxonomy")!="category": raise Blocked("BOUND_WORDPRESS_CATEGORY_MISMATCH")
    return dict(item)

def _validate_worker_stage_proofs(value: Any) -> None:
    if value != []: raise Blocked("WORKER_STAGE_PASS_PROOFS_FORBIDDEN")

def _run_languagetool(repo: Path, final_path: Path, root: str, item: Mapping[str, Any]) -> tuple[dict,dict,str,str]:
    proof_path=repo/LT_RUNTIME_REL
    if not proof_path.is_file(): raise Blocked("LANGUAGETOOL_RUNTIME_PROOF_MISSING")
    runtime=_load(proof_path)
    if runtime.get("contract")!="PFERDE_ATELIER_LANGUAGETOOL_RUNTIME_BINDING_V2" or runtime.get("status")!="LANGUAGETOOL_RUNTIME_READY" or runtime.get("engine")!=LT_ENGINE: raise Blocked("LANGUAGETOOL_RUNTIME_NOT_READY")
    toolbox_ref=str(runtime.get("toolbox_manifest_ref") or ""); toolbox=_safe_repo(repo,toolbox_ref)
    if toolbox_ref!=TOOLBOX_REL or not toolbox.is_file() or _sha(toolbox)!=runtime.get("toolbox_manifest_sha256"): raise Blocked("LANGUAGETOOL_TOOLBOX_HASH_MISMATCH")
    manifest=_load(toolbox); lt=manifest.get("languagetool") or {}
    if lt.get("engine")!=LT_ENGINE or lt.get("real_execution_required") is not True: raise Blocked("LANGUAGETOOL_MANIFEST_IDENTITY_INVALID")
    jar=Path(str(runtime.get("executed_commandline_jar_ref") or ""))
    if not jar.is_absolute() or not jar.is_file(): raise Blocked("LANGUAGETOOL_JAR_MISSING")
    if _sha(jar)!=runtime.get("executed_commandline_jar_sha256") or _sha(jar)!=lt.get("commandline_jar_sha256"): raise Blocked("LANGUAGETOOL_JAR_HASH_MISMATCH")
    proc=subprocess.run(["java","-Xmx1024m","-jar",str(jar),"--json","-l","de-DE",str(final_path)],text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=120)
    if proc.returncode!=0: raise Blocked("LANGUAGETOOL_REAL_EXECUTION_FAILED:"+(proc.stderr or proc.stdout).strip()[:300])
    try: report=json.loads(proc.stdout)
    except json.JSONDecodeError as exc: raise Blocked("LANGUAGETOOL_REPORT_INVALID") from exc
    matches=report.get("matches") if isinstance(report,dict) else None
    if not isinstance(matches,list): raise Blocked("LANGUAGETOOL_MATCHES_INVALID")
    if matches: raise Blocked("LANGUAGETOOL_UNRESOLVED_FINDINGS:"+str(len(matches)))
    ref=root+"LANGUAGETOOL_REPORT.json"; path=_path(repo,ref,root)
    if path.exists(): raise Blocked("LANGUAGETOOL_PREGENERATED_REPORT_FORBIDDEN")
    _write_text(path,proc.stdout); raw_sha=_sha(path)
    quality=item.get("quality_binding"); existing=quality.get("language_evidence") if isinstance(quality,dict) else None
    if existing is not None and not isinstance(existing,dict): raise Blocked("LANGUAGETOOL_BOUND_EVIDENCE_INVALID")
    existing=dict(existing or {})
    for forbidden in ("evidence_mode","claude_review","independent_claude_review"):
        if forbidden in existing: raise Blocked("LANGUAGETOOL_EXTERNAL_REVIEW_AUTHORITY_FORBIDDEN")
    actual=dict(existing)
    actual.update({"engine":LT_ENGINE,"raw_finding_count":0,"unresolved_finding_count":0,"return_code":0,"raw_report_sha256":raw_sha,"outer_dependency_sha256":runtime.get("outer_dependency_sha256"),"inner_dependency_sha256":runtime.get("inner_dependency_sha256")})
    summary={"engine":LT_ENGINE,"return_code":0,"raw_finding_count":0,"unresolved_finding_count":0,"raw_report_ref":ref,"raw_report_sha256":raw_sha,"toolbox_manifest_sha256":runtime.get("toolbox_manifest_sha256"),"commandline_jar_sha256":runtime.get("executed_commandline_jar_sha256")}
    return actual,summary,ref,raw_sha

def _run_existing_pipeline(repo: Path, request: Mapping[str, Any], root: str, final_ref: str, final_sha: str, report_ref: str, item: Mapping[str, Any]) -> dict:
    final_path=_path(repo,final_ref,root); report_path=_path(repo,report_ref,root)
    if report_path.exists(): raise Blocked("PPM679_PREGENERATED_REPORT_FORBIDDEN")
    ppm_env=os.environ.get("PPM679_PACKAGE_ZIP","").strip(); pserc_env=os.environ.get("PSERC_FIX_ZIP","").strip()
    ppm_zip=Path(ppm_env).expanduser() if ppm_env else (repo/PPM679_PACKAGE_REL); pserc_zip=Path(pserc_env).expanduser() if pserc_env else (repo/PSERC_FIX_PACKAGE_REL)
    if not ppm_zip.is_file(): raise Blocked("PPM679_PACKAGE_ZIP_MISSING")
    if not pserc_zip.is_file(): raise Blocked("PSERC_FIX_ZIP_MISSING")
    if _sha(ppm_zip)!=PPM679_PACKAGE_SHA256: raise Blocked("PPM679_PACKAGE_HASH_MISMATCH")
    if _sha(pserc_zip)!=PSERC_FIX_PACKAGE_SHA256: raise Blocked("PSERC_FIX_PACKAGE_HASH_MISMATCH")
    article=final_path.read_text(encoding="utf-8"); canonical=item.get("canonical_article")
    if not isinstance(canonical,dict) or canonical.get("body_html")!=article: raise Blocked("PPM679_FINAL_ARTICLE_NOT_BOUND_TO_PRODUCTION_PLAN")
    if hashlib.sha256(article.encode("utf-8")).hexdigest()!=final_sha: raise Blocked("PPM679_FINAL_ARTICLE_TEXT_HASH_MISMATCH")
    payload={"canonical_article_id":request["canonical_article_id"],"plan_slot":request["plan_slot"],"production_plan_item":item,"production_plan_header":request["production_plan_header"],"fact_pack":request["fact_pack"],"final_article_sha256":final_sha}
    php=r'''<?php
$ppm=$argv[1]; $pserc=$argv[2]; $payload=json_decode((string)file_get_contents($argv[3]),true);
if(!is_array($payload)){fwrite(STDERR,"PAYLOAD_INVALID\n");exit(2);}
require $ppm.'/tests/normal-draft-production/fixture-builder.php';
require $pserc.'/includes/class-pserc-stable-json.php';
require $pserc.'/includes/class-pserc-plan-slot-identity.php';
require $pserc.'/includes/class-pserc-metadata-boundary.php';
require $pserc.'/includes/class-pserc-production-reader.php';
require $pserc.'/includes/class-pserc-ppm-intake-bridge.php';
nd_reset();
$item=(array)$payload['production_plan_item']; $pack=(array)$payload['fact_pack']; $header=(array)$payload['production_plan_header'];
$cid=(string)$payload['canonical_article_id']; $externalSlot=(string)$payload['plan_slot'];
if((string)($item['canonical_article_id']??'')!==$cid){fwrite(STDERR,"CANONICAL_ID_MISMATCH\n");exit(2);}
$matches=[];
foreach((array)(PPM679_Editorial_Plan_Registry::plan()['slots']??[]) as $candidate){if(is_array($candidate)&&hash_equals(PSERC_Plan_Slot_Identity::token($candidate),$externalSlot)){$matches[]=$candidate;}}
if(count($matches)!==1){fwrite(STDERR,"PLAN_SLOT_REGISTRY_MATCH_NOT_UNIQUE\n");exit(2);}
$slot=$matches[0]; $item['canonical_article_id']=(string)$slot['canonical_article_id']; unset($item['plan_slot']);
$cat=(array)($item['quality_binding']['wordpress_category']??[]);
if(empty($cat['name'])||empty($cat['slug'])||(string)($cat['taxonomy']??'')!=='category'){fwrite(STDERR,"WORDPRESS_CATEGORY_BINDING_MISSING\n");exit(2);}
$seedItem=$item; $seedItem['quality_binding']['wordpress_category']['id']=900001; nd_seed_terms([$seedItem]);
$bundle=['contract'=>'canonical_fact_pack_import_v1','fact_packs'=>[$pack]]; $imp=PPM679_Admin::import_fact_pack_bundle($bundle);
if(empty($imp['ok'])){echo json_encode(['ok'=>false,'status'=>'PPM_FACT_PACK_IMPORT_BLOCKED','detail'=>$imp],JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE);exit(0);}
$expectedSource=PPM679_Storage::fact_pack_hash((string)($item['source_snapshot_id']??'')); if($expectedSource===''){fwrite(STDERR,"SOURCE_HASH_BINDING_MISMATCH\n");exit(2);} $item['source_hashes']=[$expectedSource];
$plan=$header; unset($plan['items']); $plan['items']=[$item]; if((string)($plan['contract']??'')!=='production_plan_v4'){fwrite(STDERR,"PRODUCTION_PLAN_CONTRACT_INVALID\n");exit(2);}
$batch=['contract'=>'PSERC_TEXTMACHINE_METADATA_BATCH_V2','status'=>'PASS','item_count'=>1,'maximum_articles'=>0,'maximum_articles_per_type'=>0,'publish_allowed'=>false,'content_or_format_payload_present'=>false,'items'=>[['title'=>(string)($item['topic']??''),'target_keyword'=>(string)($item['target_keyword']??''),'category'=>(string)($slot['category_slug']??''),'article_type'=>(string)($item['article_type']??''),'plan_slot'=>$externalSlot]]];
$tmp=$batch; unset($tmp['batch_sha256']); $batch['batch_sha256']=PSERC_Stable_Json::hash($tmp); $snapshot=['ok'=>true,'version'=>'6.7.9','plan'=>PPM679_Editorial_Plan_Registry::plan()];
$runtime=nd_runtime($plan,'startmaster107007-'.substr(hash('sha256',$cid.'|'.$payload['final_article_sha256'].'|'.$externalSlot),0,40)); $r=PSERC_PPM_Intake_Bridge::execute($batch,$plan,$runtime,$snapshot); echo json_encode($r,JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE);
?>'''
    with tempfile.TemporaryDirectory() as td:
        t=Path(td); ppm_dir=t/"ppm"; pserc_outer=t/"pserc_outer"; pserc_dir=t/"pserc"; ppm_dir.mkdir(); pserc_outer.mkdir(); pserc_dir.mkdir()
        with zipfile.ZipFile(ppm_zip) as zf: zf.extractall(ppm_dir)
        with zipfile.ZipFile(pserc_zip) as zf: zf.extractall(pserc_outer)
        inner=pserc_outer/PSERC_INNER_ZIP
        if not inner.is_file(): raise Blocked("PSERC_INNER_ZIP_MISSING")
        with zipfile.ZipFile(inner) as zf: zf.extractall(pserc_dir)
        ppm_root=ppm_dir/"portal-production-machine"; pserc_root=pserc_dir/"portal-seo-editorial-plan-compiler"
        if not (ppm_root/"tests/normal-draft-production/fixture-builder.php").is_file(): raise Blocked("PPM679_RUNTIME_FILES_MISSING")
        if not (pserc_root/"includes/class-pserc-ppm-intake-bridge.php").is_file(): raise Blocked("PSERC_BRIDGE_RUNTIME_FILES_MISSING")
        payload_path=t/"payload.json"; payload_path.write_text(json.dumps(payload,ensure_ascii=False),encoding="utf-8")
        script=t/"ppm-stage.php"; script.write_text(php,encoding="utf-8")
        proc=subprocess.run(["php",str(script),str(ppm_root),str(pserc_root),str(payload_path)],text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=120)
    if proc.returncode!=0: raise Blocked("PPM679_REAL_EXECUTION_FAILED:"+(proc.stderr or proc.stdout).strip()[:400])
    try: bridge=json.loads(proc.stdout)
    except json.JSONDecodeError as exc: raise Blocked("PPM679_REAL_EXECUTION_OUTPUT_INVALID") from exc
    if not isinstance(bridge,dict) or bridge.get("ok") is not True or bridge.get("status")!="PSERC_PPM_INTAKE_BRIDGE_EXECUTED": raise Blocked("PPM679_REAL_EXECUTION_BLOCKED")
    ppm_result=bridge.get("ppm_result"); artifact=ppm_result.get("artifact") if isinstance(ppm_result,dict) else None
    if not isinstance(artifact,dict) or artifact.get("contract")!="ppm_action_report_v1" or artifact.get("version")!=PPM679_VERSION: raise Blocked("PPM679_REAL_REPORT_IDENTITY_INVALID")
    if artifact.get("status")!="NORMAL_DRAFT_END_TO_END_READBACK_PASS_AWAITING_USER_CONTENT_REVIEW_NO_PUBLISH": raise Blocked("PPM679_REAL_REPORT_NOT_PASS")
    check_only=artifact.get("check_only"); items=check_only.get("items") if isinstance(check_only,dict) else None
    if not isinstance(items,list) or len(items)!=1 or not isinstance(items[0],dict): raise Blocked("PPM679_REAL_CHECK_ITEM_INVALID")
    check=items[0]; checks=check.get("checks")
    if check.get("technical_status")!="TECHNICAL_CHECK_OK": raise Blocked("PPM679_TECHNICAL_NOT_PASS")
    if check.get("content_quality_status")!="CONTENT_QUALITY_CHECK_OK": raise Blocked("PPM679_CONTENT_QUALITY_NOT_PASS")
    if check.get("content_hash")!=final_sha: raise Blocked("PPM679_CONTENT_HASH_NOT_FINAL_ARTICLE")
    if not isinstance(checks,dict) or checks.get("content_hash")!=final_sha or checks.get("fail_closed_aggregate_status")!="PASS": raise Blocked("PPM679_FAIL_CLOSED_NOT_PASS")
    report=dict(check); report.update(ok=True,ppm_version=PPM679_VERSION,ppm_status=artifact["status"],execution_path="PSERC_PPM_Intake_Bridge::execute -> PPM679_Normal_Draft_Pipeline::execute_plan",raw_ppm_result=ppm_result)
    _write_json(report_path,report)
    return {"report_ref":report_ref,"report_sha256":_sha(report_path),"technical_status":check["technical_status"],"content_quality_status":check["content_quality_status"],"fail_closed_aggregate_status":checks["fail_closed_aggregate_status"],"execution_path":report["execution_path"],"ppm_status":artifact["status"]}

def materialize(repo: Path, request_ref: str) -> dict:
    repo=Path(repo).resolve(); _assert_bound_adapters(repo)
    rp=Path(request_ref)
    if not request_ref or rp.is_absolute() or ".." in rp.parts: raise Blocked("INVALID_HANDOFF_REQUEST_REF")
    request_path=(repo/rp).resolve()
    if repo not in request_path.parents: raise Blocked("HANDOFF_REQUEST_REF_ESCAPE")
    request=_load(request_path)
    if set(request)!=REQUEST_FIELDS or request.get("contract")!=CONTRACT: raise Blocked("HANDOFF_REQUEST_FIELDS_OR_CONTRACT_INVALID")
    batch=str(request["batch_sha256"]); slot=str(request["plan_slot"]); canonical_id=str(request["canonical_article_id"])
    if not re.fullmatch(r"[0-9a-f]{64}",batch) or not re.fullmatch(r"[0-9a-f]{64}",slot) or not canonical_id.startswith("article:"): raise Blocked("HANDOFF_IDENTITY_INVALID")
    root=str(request["allowed_output_root"])
    if not root.endswith("/") or not request_ref.startswith(root): raise Blocked("HANDOFF_REQUEST_NOT_IN_BOUND_OUTPUT_ROOT")
    _validate_worker_stage_proofs(request.get("stage_proofs"))
    binding_ref=str(request["contract_binding_ref"]); binding=_safe_repo(repo,binding_ref)
    if binding_ref!=ACTION_REL or not binding.is_file() or _sha(binding)!=request["contract_binding_sha256"]: raise Blocked("HANDOFF_CONTRACT_BINDING_HASH_MISMATCH")
    ctx=_runtime_context(repo,batch); meta,release_item=_bound_item(ctx,canonical_id,slot); item=_validate_raw_context(request,ctx,meta,release_item)
    final_ref=root+"ARTICLE_"+slot+".md"; final_path=_path(repo,final_ref,root)
    if not final_path.is_file(): raise Blocked("BOUND_FINAL_ARTICLE_MISSING")
    final_sha=_sha(final_path); canonical=item.get("canonical_article")
    if not isinstance(canonical,dict) or canonical.get("body_html")!=final_path.read_text(encoding="utf-8"): raise Blocked("BOUND_FINAL_ARTICLE_BODY_MISMATCH")
    pass_path=_path(repo,str(request["fachworkflow_pass_ref"]),root); receipt_path=_path(repo,str(request["item_receipt_ref"]),root)
    report_ref=root+"PPM679_REPORT.json"; report_path=_path(repo,report_ref,root); lt_ref=root+"LANGUAGETOOL_REPORT.json"; lt_path=_path(repo,lt_ref,root)
    if pass_path.exists() or receipt_path.exists() or report_path.exists() or lt_path.exists(): raise Blocked("PREGENERATED_PASS_OR_REPORT_FORBIDDEN")
    lt_evidence,lt,lt_ref,lt_sha=_run_languagetool(repo,final_path,root,item)
    item=json.loads(json.dumps(item,ensure_ascii=False))
    quality=dict(item.get("quality_binding") or {}); quality["language_evidence"]=lt_evidence; item["quality_binding"]=quality
    canonical=item.get("canonical_article")
    if not isinstance(canonical,dict) or canonical.get("body_html")!=final_path.read_text(encoding="utf-8"): raise Blocked("BOUND_FINAL_ARTICLE_BODY_MISMATCH_AFTER_LT_BINDING")
    request_for_ppm=dict(request); request_for_ppm["production_plan_item"]=item
    ppm=_run_existing_pipeline(repo,request_for_ppm,root,final_ref,final_sha,report_ref,item)
    aggregate={"contract":AGGREGATE_CONTRACT,"status":"PASS","batch_sha256":batch,"canonical_article_id":canonical_id,"plan_slot":slot,"article_type":meta.get("article_type"),"article_type_templates_sha256":PPM679_RULESET_SHA256,"runtime_source_snapshot_sha256":ctx["source_sha256"],"runtime_production_package_sha256":ctx["package_sha256"],"handoff_adapter_ref":SELF_REL,"handoff_adapter_sha256":_sha(repo/SELF_REL),"current_action_ref":ACTION_REL,"current_action_sha256":_sha(repo/ACTION_REL),"final_article_ref":final_ref,"final_article_sha256":final_sha,"languagetool":lt,"ppm_version":PPM679_VERSION,"ppm_package_sha256":PPM679_PACKAGE_SHA256,"pserc_package_sha256":PSERC_FIX_PACKAGE_SHA256,"ppm_report_ref":ppm["report_ref"],"ppm_report_sha256":ppm["report_sha256"],"execution_path":ppm["execution_path"],"ppm_status":ppm["ppm_status"],"technical_status":ppm["technical_status"],"content_quality_status":ppm["content_quality_status"],"fail_closed_aggregate_status":ppm["fail_closed_aggregate_status"],"worker_pass_authority":"NONE","worker_stage_proofs_accepted":False,"content_or_quality_rules_changed":False,"publish_allowed":False}
    passed={"contract":PASS_CONTRACT,"status":"PASS","batch_sha256":batch,"canonical_article_id":canonical_id,"plan_slot":slot,"article_type":meta.get("article_type"),"article_type_templates_sha256":PPM679_RULESET_SHA256,"contract_binding_ref":request["contract_binding_ref"],"contract_binding_sha256":request["contract_binding_sha256"],"aggregate_check":aggregate,"fact_pack":request["fact_pack"],"production_plan_item":item,"production_plan_header":request["production_plan_header"],"workflow_release_item":request["workflow_release_item"],"workflow_release_metadata":request["workflow_release_metadata"],"content_or_quality_rules_changed":False,"publish_allowed":False}
    _write_json(pass_path,passed); pass_sha=_sha(pass_path)
    outputs=[{"ref":final_ref,"sha256":final_sha},{"ref":lt_ref,"sha256":lt_sha},{"ref":ppm["report_ref"],"sha256":ppm["report_sha256"]},{"ref":request["fachworkflow_pass_ref"],"sha256":pass_sha}]
    receipt={"contract":RECEIPT_CONTRACT,"room_token":request["room_token"],"canonical_article_id":canonical_id,"plan_slot":slot,"status":"PASS","workflow_pass":True,"navigation_decision":False,"state_write_requested":False,"workflow_change_requested":False,"content_or_quality_rules_changed":False,"outputs":outputs,"evidence":["EXISTING_VALIDATORS_SINGLE_AGGREGATE_PASS"],"fachworkflow_pass_ref":request["fachworkflow_pass_ref"],"fachworkflow_pass_sha256":pass_sha}
    _write_json(receipt_path,receipt)
    return {"ok":True,"status":"FACHWORKFLOW_PROOF_HANDOFF_PASS","item_receipt_ref":request["item_receipt_ref"],"item_receipt_sha256":_sha(receipt_path),"aggregate_pass_ref":request["fachworkflow_pass_ref"],"aggregate_pass_sha256":pass_sha,"publish_allowed":False}

def selftest() -> dict:
    _validate_worker_stage_proofs([]); blocked=0
    for bad in ([{"stage":"ppm"}],[{"stage":"seo","status":"PASS"}],None,{}):
        try: _validate_worker_stage_proofs(bad)
        except Blocked: blocked+=1
        else: raise AssertionError("WORKER_STAGE_PROOF_NEGATIVE_NOT_BLOCKED")
    if blocked!=4: raise AssertionError("WORKER_STAGE_PROOF_NEGATIVE_COUNT_INVALID")
    return {"ok":True,"status":"FACHWORKFLOW_AGGREGATE_SELFTEST_PASS","positive":1,"negative":blocked,"worker_stage_pass_proofs_allowed":False,"aggregate_pass_generated_by_adapter_only":True,"content_or_quality_rules_changed":False,"publish_allowed":False}

def main(argv:list[str])->int:
    try:
        if argv==["selftest"]: result=selftest()
        elif len(argv)==2 and argv[0]=="materialize": result=materialize(REPO,argv[1])
        else: raise Blocked("USAGE: materialize HANDOFF_REQUEST.json | selftest")
        print(json.dumps(result,ensure_ascii=False,indent=2)); return 0
    except (Blocked,OSError,ValueError,KeyError,TypeError,json.JSONDecodeError) as exc:
        print(json.dumps({"ok":False,"status":"FACHWORKFLOW_PROOF_HANDOFF_BLOCKED","error":str(exc),"publish_allowed":False},ensure_ascii=False,indent=2)); return 2

if __name__=="__main__": raise SystemExit(main(sys.argv[1:]))
