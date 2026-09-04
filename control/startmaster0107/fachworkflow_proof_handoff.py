#!/usr/bin/env python3
"""Technical handoff for proofs emitted by the unchanged Fachworkflow.

This module has no content or quality authority.  It only verifies that every
required stage left identity-bound, hash-bound evidence of a real execution and
then writes the aggregate pass and the item receipt expected by step 107007.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Any, Mapping

REPO = Path(__file__).resolve().parents[2]
CONTRACT = "PFERDE_ATELIER_FACHWORKFLOW_HANDOFF_REQUEST_V1"
PASS_CONTRACT = "PFERDE_ATELIER_FACHWORKFLOW_PASS_V1"
STAGE_CONTRACT = "PFERDE_ATELIER_FACHWORKFLOW_STAGE_EXECUTION_PROOF_V1"
RECEIPT_CONTRACT = "PFERDE_ATELIER_BOUND_ITEM_EXECUTION_RECEIPT_V1"
STAGES = ["research_fact_pack", "textmachine_article_type_structure", "table_contract",
          "internal_links", "languagetool", "ppm", "pserc", "pste",
          "duplicate_cannibalization", "seo", "design_format", "publish_safety"]
PPM679_VERSION = "6.7.9"
PPM679_PACKAGE_SHA256 = "acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1"
PPM679_RULESET_SHA256 = "dc79a6d7d30fba2f7f13c80d35bf4d137669f2b3469d7bc28a5d0873858f192f"
PSERC_FIX_PACKAGE_SHA256 = "77a14aca97f46d60bc9001d66327abb68dd9cac9ad111f8ecefa1a8afd345314"
PSERC_INNER_ZIP = "PSERC-FIX/portal-seo-editorial-plan-compiler_0.28.18_ENDSTEMPEL_IMPORT_ENVELOPE_BINDING.zip"
PPM679_PACKAGE_REL = "control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip"
PSERC_FIX_PACKAGE_REL = "control/startmaster0107/runtime_packages/PSERC-FIX.zip"


class Blocked(RuntimeError):
    pass


def _load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise Blocked("JSON_OBJECT_REQUIRED")
    return value


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _path(repo: Path, ref: str, root: str) -> Path:
    if not ref.startswith(root):
        raise Blocked("PROOF_REF_OUTSIDE_BOUND_OUTPUT_ROOT")
    relative = Path(ref)
    if relative.is_absolute() or ".." in relative.parts:
        raise Blocked("INVALID_RELATIVE_REF")
    result = (repo / relative).resolve()
    base = (repo / root).resolve()
    if result != base and base not in result.parents:
        raise Blocked("PROOF_REF_ESCAPE")
    return result


def _write(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)



def _real_ppm_stage(repo: Path, request: Mapping[str, Any], root: str,
                    proof_path: Path, proof: dict) -> dict:
    binding = proof.get("ppm679_binding")
    if not isinstance(binding, dict):
        return proof
    final_ref = str(binding.get("final_article_ref", ""))
    final_sha = str(binding.get("final_article_sha256", ""))
    if not final_ref or not re.fullmatch(r"[0-9a-f]{64}", final_sha):
        raise Blocked("PPM679_FINAL_ARTICLE_BINDING_INVALID")
    final_path = _path(repo, final_ref, root)
    if not final_path.is_file() or _sha(final_path) != final_sha:
        raise Blocked("PPM679_FINAL_ARTICLE_HASH_MISMATCH")

    report_ref = str(binding.get("ppm_report_ref", "")).strip()
    if not report_ref:
        report_ref = str(Path(proof_path.relative_to(repo)).with_name("PPM679_REPORT.json")).replace("\\", "/")
    report_path = _path(repo, report_ref, root)
    if report_path.exists():
        raise Blocked("PPM679_PREGENERATED_REPORT_FORBIDDEN")

    ppm_env = os.environ.get("PPM679_PACKAGE_ZIP", "").strip()
    pserc_env = os.environ.get("PSERC_FIX_ZIP", "").strip()
    ppm_zip = Path(ppm_env).expanduser() if ppm_env else (repo / PPM679_PACKAGE_REL)
    pserc_zip = Path(pserc_env).expanduser() if pserc_env else (repo / PSERC_FIX_PACKAGE_REL)
    if not ppm_zip.is_file():
        raise Blocked("PPM679_PACKAGE_ZIP_MISSING")
    if not pserc_zip.is_file():
        raise Blocked("PSERC_FIX_ZIP_MISSING")
    if _sha(ppm_zip) != PPM679_PACKAGE_SHA256:
        raise Blocked("PPM679_PACKAGE_HASH_MISMATCH")
    if _sha(pserc_zip) != PSERC_FIX_PACKAGE_SHA256:
        raise Blocked("PSERC_FIX_PACKAGE_HASH_MISMATCH")

    article = final_path.read_text(encoding="utf-8")
    item = request.get("production_plan_item")
    fact_pack = request.get("fact_pack")
    header = request.get("production_plan_header")
    if not isinstance(item, dict) or not isinstance(fact_pack, dict) or not isinstance(header, dict):
        raise Blocked("PPM679_PRODUCTION_CONTEXT_INCOMPLETE")
    canonical = item.get("canonical_article")
    if not isinstance(canonical, dict) or canonical.get("body_html") != article:
        raise Blocked("PPM679_FINAL_ARTICLE_NOT_BOUND_TO_PRODUCTION_PLAN")
    if hashlib.sha256(article.encode("utf-8")).hexdigest() != final_sha:
        raise Blocked("PPM679_FINAL_ARTICLE_TEXT_HASH_MISMATCH")

    payload = {
        "canonical_article_id": request["canonical_article_id"],
        "plan_slot": request["plan_slot"],
        "production_plan_item": item,
        "production_plan_header": header,
        "fact_pack": fact_pack,
        "final_article_sha256": final_sha,
    }

    php = r'''<?php
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
foreach((array)(PPM679_Editorial_Plan_Registry::plan()['slots']??[]) as $candidate){
  if(is_array($candidate)&&hash_equals(PSERC_Plan_Slot_Identity::token($candidate),$externalSlot)){$matches[]=$candidate;}
}
if(count($matches)!==1){fwrite(STDERR,"PLAN_SLOT_REGISTRY_MATCH_NOT_UNIQUE\n");exit(2);}
$slot=$matches[0];
$item['canonical_article_id']=(string)$slot['canonical_article_id'];
$cat=(array)($item['quality_binding']['wordpress_category']??[]);
if(empty($cat['id'])||empty($cat['slug'])){fwrite(STDERR,"WORDPRESS_CATEGORY_BINDING_MISSING\n");exit(2);}
nd_seed_terms([$item]);
$bundle=['contract'=>'canonical_fact_pack_import_v1','fact_packs'=>[$pack]];
$imp=PPM679_Admin::import_fact_pack_bundle($bundle);
if(empty($imp['ok'])){echo json_encode(['ok'=>false,'status'=>'PPM_FACT_PACK_IMPORT_BLOCKED','detail'=>$imp],JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE);exit(0);}
$expectedSource=PPM679_Storage::fact_pack_hash((string)($item['source_snapshot_id']??''));
if($expectedSource===''||!in_array($expectedSource,(array)($item['source_hashes']??[]),true)){fwrite(STDERR,"SOURCE_HASH_BINDING_MISMATCH\n");exit(2);}
$plan=$header; unset($plan['items']); $plan['items']=[$item];
if((string)($plan['contract']??'')!=='production_plan_v4'){fwrite(STDERR,"PRODUCTION_PLAN_CONTRACT_INVALID\n");exit(2);}
$batch=['contract'=>'PSERC_TEXTMACHINE_METADATA_BATCH_V2','status'=>'PASS','item_count'=>1,'maximum_articles'=>0,'maximum_articles_per_type'=>0,'publish_allowed'=>false,'content_or_format_payload_present'=>false,'items'=>[[
  'title'=>(string)($item['topic']??''),'target_keyword'=>(string)($item['target_keyword']??''),
  'category'=>(string)($slot['category_slug']??''),'article_type'=>(string)($item['article_type']??''),
  'plan_slot'=>$externalSlot
]]];
$tmp=$batch; unset($tmp['batch_sha256']); $batch['batch_sha256']=PSERC_Stable_Json::hash($tmp);
$snapshot=['ok'=>true,'version'=>'6.7.9','plan'=>PPM679_Editorial_Plan_Registry::plan()];
$runtime=nd_runtime($plan,'startmaster107007-'.substr(hash('sha256',$cid.'|'.$payload['final_article_sha256'].'|'.$externalSlot),0,40));
$r=PSERC_PPM_Intake_Bridge::execute($batch,$plan,$runtime,$snapshot);
echo json_encode($r,JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE);
?>'''
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        ppm_dir = td_path / "ppm"
        pserc_outer = td_path / "pserc_outer"
        pserc_dir = td_path / "pserc"
        ppm_dir.mkdir(); pserc_outer.mkdir(); pserc_dir.mkdir()
        with zipfile.ZipFile(ppm_zip) as zf:
            zf.extractall(ppm_dir)
        with zipfile.ZipFile(pserc_zip) as zf:
            zf.extractall(pserc_outer)
        inner = pserc_outer / PSERC_INNER_ZIP
        if not inner.is_file():
            raise Blocked("PSERC_INNER_ZIP_MISSING")
        with zipfile.ZipFile(inner) as zf:
            zf.extractall(pserc_dir)
        ppm_root = ppm_dir / "portal-production-machine"
        pserc_root = pserc_dir / "portal-seo-editorial-plan-compiler"
        if not (ppm_root / "tests/normal-draft-production/fixture-builder.php").is_file():
            raise Blocked("PPM679_RUNTIME_FILES_MISSING")
        if not (pserc_root / "includes/class-pserc-ppm-intake-bridge.php").is_file():
            raise Blocked("PSERC_BRIDGE_RUNTIME_FILES_MISSING")
        payload_path = td_path / "payload.json"
        payload_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        script_path = td_path / "ppm-stage.php"
        script_path.write_text(php, encoding="utf-8")
        proc = subprocess.run(
            ["php", str(script_path), str(ppm_root), str(pserc_root), str(payload_path)],
            text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120
        )
    if proc.returncode != 0:
        raise Blocked("PPM679_REAL_EXECUTION_FAILED:" + (proc.stderr or proc.stdout).strip()[:400])
    try:
        bridge = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise Blocked("PPM679_REAL_EXECUTION_OUTPUT_INVALID") from exc
    if not isinstance(bridge, dict) or bridge.get("ok") is not True or bridge.get("status") != "PSERC_PPM_INTAKE_BRIDGE_EXECUTED":
        raise Blocked("PPM679_REAL_EXECUTION_BLOCKED")
    ppm_result = bridge.get("ppm_result")
    artifact = ppm_result.get("artifact") if isinstance(ppm_result, dict) else None
    if not isinstance(artifact, dict) or artifact.get("contract") != "ppm_action_report_v1" or artifact.get("version") != PPM679_VERSION:
        raise Blocked("PPM679_REAL_REPORT_IDENTITY_INVALID")
    if artifact.get("status") != "NORMAL_DRAFT_END_TO_END_READBACK_PASS_AWAITING_USER_CONTENT_REVIEW_NO_PUBLISH":
        raise Blocked("PPM679_REAL_REPORT_NOT_PASS")
    check_only = artifact.get("check_only")
    items = check_only.get("items") if isinstance(check_only, dict) else None
    if not isinstance(items, list) or len(items) != 1 or not isinstance(items[0], dict):
        raise Blocked("PPM679_REAL_CHECK_ITEM_INVALID")
    check_item = items[0]
    checks = check_item.get("checks")
    if check_item.get("technical_status") != "TECHNICAL_CHECK_OK":
        raise Blocked("PPM679_TECHNICAL_NOT_PASS")
    if check_item.get("content_quality_status") != "CONTENT_QUALITY_CHECK_OK":
        raise Blocked("PPM679_CONTENT_QUALITY_NOT_PASS")
    if check_item.get("content_hash") != final_sha:
        raise Blocked("PPM679_CONTENT_HASH_NOT_FINAL_ARTICLE")
    if not isinstance(checks, dict) or checks.get("content_hash") != final_sha or checks.get("fail_closed_aggregate_status") != "PASS":
        raise Blocked("PPM679_FAIL_CLOSED_NOT_PASS")

    report = dict(check_item)
    report["ok"] = True
    report["ppm_version"] = PPM679_VERSION
    report["ppm_status"] = artifact["status"]
    report["execution_path"] = "PSERC_PPM_Intake_Bridge::execute -> PPM679_Normal_Draft_Pipeline::execute_plan"
    report["raw_ppm_result"] = ppm_result
    _write(report_path, report)
    report_sha = _sha(report_path)

    proof["status"] = "PASS"
    proof["execution_performed"] = True
    proof["input_sha256"] = final_sha
    proof["execution_evidence"] = [
        "PSERC_PPM_Intake_Bridge::execute completed",
        "PPM679_Normal_Draft_Pipeline::execute_plan completed",
        artifact["status"],
    ]
    proof["artifacts"] = [
        {"ref": final_ref, "sha256": final_sha},
        {"ref": report_ref, "sha256": report_sha},
    ]
    proof["ppm679_binding"] = {
        "ppm_version": PPM679_VERSION,
        "ppm_package_sha256": PPM679_PACKAGE_SHA256,
        "article_type_templates_sha256": PPM679_RULESET_SHA256,
        "final_article_ref": final_ref,
        "final_article_sha256": final_sha,
        "ppm_report_ref": report_ref,
        "ppm_report_sha256": report_sha,
    }
    _write(proof_path, proof)
    return proof


def materialize(repo: Path, request_ref: str) -> dict:
    repo = Path(repo).resolve()
    relative_request = Path(request_ref)
    if not request_ref or relative_request.is_absolute() or ".." in relative_request.parts:
        raise Blocked("INVALID_HANDOFF_REQUEST_REF")
    request_path = (repo / relative_request).resolve()
    if repo not in request_path.parents:
        raise Blocked("HANDOFF_REQUEST_REF_ESCAPE")
    request = _load(request_path)
    required = {"contract", "room_token", "batch_sha256", "canonical_article_id", "plan_slot",
                "allowed_output_root", "item_receipt_ref", "fachworkflow_pass_ref",
                "contract_binding_ref", "contract_binding_sha256", "stage_proofs",
                "fact_pack", "production_plan_item", "production_plan_header",
                "workflow_release_item", "workflow_release_metadata"}
    if set(request) != required or request.get("contract") != CONTRACT:
        raise Blocked("HANDOFF_REQUEST_FIELDS_OR_CONTRACT_INVALID")
    batch = str(request["batch_sha256"]); slot = str(request["plan_slot"])
    if not re.fullmatch(r"[0-9a-f]{64}", batch) or not re.fullmatch(r"[0-9a-f]{64}", slot):
        raise Blocked("HANDOFF_IDENTITY_HASH_INVALID")
    root = str(request["allowed_output_root"])
    if not root.endswith("/") or request_ref.startswith(root) is False:
        raise Blocked("HANDOFF_REQUEST_NOT_IN_BOUND_OUTPUT_ROOT")
    binding = (repo / str(request["contract_binding_ref"])).resolve()
    if not binding.is_file() or _sha(binding) != request["contract_binding_sha256"]:
        raise Blocked("HANDOFF_CONTRACT_BINDING_HASH_MISMATCH")
    context_fields = ("fact_pack", "production_plan_item", "production_plan_header",
                      "workflow_release_item", "workflow_release_metadata")
    if not all(isinstance(request.get(key), dict) and bool(request.get(key)) for key in context_fields):
        raise Blocked("BOUND_FACHWORKFLOW_PRODUCTION_CONTEXT_MISSING")
    item = request["production_plan_item"]
    if item.get("canonical_article_id") != request["canonical_article_id"] or item.get("plan_slot") != slot:
        raise Blocked("BOUND_PRODUCTION_PLAN_ITEM_IDENTITY_MISMATCH")
    release_item = request["workflow_release_item"]
    if release_item.get("canonical_article_id") != request["canonical_article_id"] or release_item.get("plan_slot") != slot:
        raise Blocked("BOUND_WORKFLOW_RELEASE_ITEM_IDENTITY_MISMATCH")
    header = request["production_plan_header"]
    if header.get("contract") != "production_plan_v4" or "items" in header:
        raise Blocked("BOUND_PRODUCTION_PLAN_HEADER_INVALID")
    rows = request["stage_proofs"]
    if not isinstance(rows, list) or len(rows) != len(STAGES):
        raise Blocked("FACH_STAGE_COUNT_INVALID")
    verified = []
    seen = set()
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"stage", "ref", "sha256"}:
            raise Blocked("FACH_STAGE_ROW_INVALID")
        stage = row["stage"]
        if stage in seen or stage not in STAGES:
            raise Blocked("FACH_STAGE_SET_INVALID")
        seen.add(stage)
        proof_path = _path(repo, str(row["ref"]), root)
        if not proof_path.is_file() or _sha(proof_path) != row["sha256"]:
            raise Blocked("FACH_STAGE_HASH_MISMATCH:" + str(stage))
        proof = _load(proof_path)
        if stage == "ppm" and isinstance(proof.get("ppm679_binding"), dict):
            proof = _real_ppm_stage(repo, request, root, proof_path, proof)
            row = {"stage": stage, "ref": row["ref"], "sha256": _sha(proof_path)}
        expected = {"contract": STAGE_CONTRACT, "status": "PASS", "batch_sha256": batch,
                    "canonical_article_id": request["canonical_article_id"], "plan_slot": slot,
                    "stage": stage, "execution_performed": True,
                    "content_or_quality_rules_changed": False, "publish_allowed": False}
        if any(proof.get(key) != value for key, value in expected.items()):
            raise Blocked("FACH_STAGE_EXECUTION_BINDING_INVALID:" + str(stage))
        if not re.fullmatch(r"[0-9a-f]{64}", str(proof.get("input_sha256", ""))):
            raise Blocked("FACH_STAGE_INPUT_HASH_INVALID:" + str(stage))
        evidence = proof.get("execution_evidence")
        artifacts = proof.get("artifacts")
        if not isinstance(evidence, list) or not evidence or not all(isinstance(x, str) and x.strip() for x in evidence):
            raise Blocked("FACH_STAGE_EXECUTION_EVIDENCE_MISSING:" + str(stage))
        if not isinstance(artifacts, list) or not artifacts:
            raise Blocked("FACH_STAGE_ARTIFACTS_MISSING:" + str(stage))
        for artifact in artifacts:
            if not isinstance(artifact, dict) or set(artifact) != {"ref", "sha256"}:
                raise Blocked("FACH_STAGE_ARTIFACT_ROW_INVALID:" + str(stage))
            artifact_path = _path(repo, str(artifact["ref"]), root)
            if not artifact_path.is_file() or _sha(artifact_path) != artifact["sha256"]:
                raise Blocked("FACH_STAGE_ARTIFACT_HASH_MISMATCH:" + str(stage))
        verified.append(dict(row))
    if seen != set(STAGES):
        raise Blocked("FACH_STAGE_SET_INVALID")
    passed = {"contract": PASS_CONTRACT, "status": "PASS", "batch_sha256": batch,
              "canonical_article_id": request["canonical_article_id"], "plan_slot": slot,
              "contract_binding_ref": request["contract_binding_ref"],
              "contract_binding_sha256": request["contract_binding_sha256"],
              "required_stage_proofs": verified, "fact_pack": request["fact_pack"],
              "production_plan_item": request["production_plan_item"],
              "production_plan_header": request["production_plan_header"],
              "workflow_release_item": request["workflow_release_item"],
              "workflow_release_metadata": request["workflow_release_metadata"],
              "content_or_quality_rules_changed": False, "publish_allowed": False}
    pass_path = _path(repo, str(request["fachworkflow_pass_ref"]), root)
    _write(pass_path, passed)
    output_rows = verified + [{"stage": "fachworkflow_pass", "ref": request["fachworkflow_pass_ref"], "sha256": _sha(pass_path)}]
    outputs = [{"ref": row["ref"], "sha256": row["sha256"]} for row in output_rows]
    receipt = {"contract": RECEIPT_CONTRACT, "room_token": request["room_token"],
               "canonical_article_id": request["canonical_article_id"], "plan_slot": slot,
               "status": "PASS", "workflow_pass": True, "navigation_decision": False,
               "state_write_requested": False, "workflow_change_requested": False,
               "content_or_quality_rules_changed": False, "outputs": outputs,
               "evidence": ["REAL_FACHWORKFLOW_STAGE_EXECUTION_PROOFS_HASH_VERIFIED"],
               "fachworkflow_pass_ref": request["fachworkflow_pass_ref"],
               "fachworkflow_pass_sha256": _sha(pass_path)}
    receipt_path = _path(repo, str(request["item_receipt_ref"]), root)
    _write(receipt_path, receipt)
    return {"ok": True, "status": "FACHWORKFLOW_PROOF_HANDOFF_PASS",
            "item_receipt_ref": request["item_receipt_ref"], "item_receipt_sha256": _sha(receipt_path),
            "publish_allowed": False}


def main(argv: list[str]) -> int:
    try:
        if len(argv) != 2 or argv[0] != "materialize":
            raise Blocked("USAGE: materialize HANDOFF_REQUEST.json")
        result = materialize(REPO, argv[1])
        print(json.dumps(result, ensure_ascii=False, indent=2)); return 0
    except (Blocked, OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(json.dumps({"ok": False, "status": "FACHWORKFLOW_PROOF_HANDOFF_BLOCKED",
                          "error": str(exc), "publish_allowed": False}, ensure_ascii=False, indent=2)); return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
