#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import tempfile
import zipfile
from pathlib import Path

from p40_handoff_controller import _load_exact_handoff

REPO = Path(__file__).resolve().parents[4]
PPM = REPO / "control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip"

BUILD_HANDOFF_PHP = r'''<?php
require __DIR__.'/tests/normal-draft-production/fixture-builder.php';
nd_reset();
$p=nd_build_plan(1,'p47-handoff-source');
$item=$p['items'][0];
$pack=PPM679_Storage::load_fact_pack($item['source_snapshot_id']);
$slot=str_repeat('a',64);
$request_item=$item;
$request_item['plan_slot']=$slot;
$header=$p;
unset($header['items']);
$request=array(
  'contract'=>'PFERDE_ATELIER_FACHWORKFLOW_HANDOFF_REQUEST_V1',
  'room_token'=>'P47-ISOLATED-LAB',
  'batch_sha256'=>hash('sha256','p47-existing-handoff'),
  'canonical_article_id'=>(string)$item['canonical_article_id'],
  'plan_slot'=>$slot,
  'allowed_output_root'=>'.pferde-quarantine/p47/',
  'item_receipt_ref'=>'.pferde-quarantine/p47/ITEM_RECEIPT.json',
  'fachworkflow_pass_ref'=>'.pferde-quarantine/p47/FACHWORKFLOW_PASS.json',
  'contract_binding_ref'=>'control/startmaster0107/FACHWORKFLOW_CONTRACT_BINDING.json',
  'contract_binding_sha256'=>str_repeat('c',64),
  'stage_proofs'=>array_map(function($i){return array('stage'=>'s'.$i,'ref'=>'x'.$i,'sha256'=>str_repeat('d',64));},range(0,11)),
  'fact_pack'=>$pack,
  'production_plan_item'=>$request_item,
  'production_plan_header'=>$header,
  'workflow_release_item'=>array(
    'canonical_article_id'=>(string)$item['canonical_article_id'],
    'plan_slot'=>$slot
  ),
  'workflow_release_metadata'=>array('contract'=>'P47_EXISTING_RELEASE_METADATA_FIXTURE_V1')
);
file_put_contents($argv[1],json_encode($request,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES));
echo json_encode(array(
  'status'=>'P47_HANDOFF_FIXTURE_READY',
  'canonical_article_id'=>$request['canonical_article_id'],
  'plan_item_key'=>$request_item['plan_item_key'],
  'publish_allowed'=>false
),JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";
'''

PUBLIC_PREWRITE_PHP = r'''<?php
require __DIR__.'/tests/normal-draft-production/fixture-builder.php';
nd_reset();
/* Seed only the existing bundled lab registry/inventory. The production input below remains the handoff file. */
nd_build_plan(1,'p47-live-state-seed');
$request=json_decode(file_get_contents($argv[1]),true);
if(!is_array($request)){throw new RuntimeException('HANDOFF_JSON_INVALID');}

$item=$request['production_plan_item'];
unset($item['plan_slot']);
$plan=$request['production_plan_header'];
$plan['items']=array($item);
$pack=$request['fact_pack'];
$runtime=nd_runtime($plan,'p47-existing-handoff');

$statuses=array('publish','draft','trash','private','pending','future');
$before=count(PPM679_WP::get_all_post_inventory($statuses));
$plan_hash=PPM679_Diagnostic::stable_hash($plan);
$scope=PPM679_Normal_Draft_Release_Validator::expected_scope($plan,$runtime);
$requirements=array('article_type_release_scope'=>$scope);

$editorial_candidates=array();
foreach($plan['items'] as $editorial_item){
  $editorial_candidates[]=array(
    'plan_item_key'=>(string)($editorial_item['plan_item_key']??''),
    'canonical_article_id'=>(string)($editorial_item['canonical_article_id']??$editorial_item['plan_item_key']??''),
    'title'=>(string)($editorial_item['title']??$editorial_item['topic']??''),
    'article_type'=>(string)($editorial_item['article_type']??'')
  );
}

$editorial_gate=PPM679_Editorial_Plan_Runtime_Gate::preflight($editorial_candidates,'normal_plan_preflight','production');
if(empty($editorial_gate['ok'])){
  echo json_encode(array('status'=>'P47_BLOCKED_EDITORIAL_PREFLIGHT','detail'=>$editorial_gate,'publish_allowed'=>false),JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";
  exit(2);
}

$gate=PPM679_Live_State_Gate::verify_live_state_or_abort('normal_plan_preflight',$plan_hash,null,null,$requirements);
if(empty($gate['ok'])){
  echo json_encode(array('status'=>'P47_BLOCKED_LIVE_STATE_PREFLIGHT','detail'=>$gate,'publish_allowed'=>false),JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";
  exit(2);
}

PPM679_Storage::ensure_schema();
$initial_gate=PPM679_Live_State_Gate::verify_live_state_or_abort('normal_plan_pre_accept',$plan_hash,null,null,$requirements);
if(empty($initial_gate['ok'])){
  echo json_encode(array('status'=>'P47_BLOCKED_LIVE_STATE_PRE_ACCEPT','detail'=>$initial_gate,'publish_allowed'=>false),JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";
  exit(2);
}

$state_hash=(string)($initial_gate['state']['server_state_hash']??'');
$validated=PPM679_Plan_Validator::validate($plan,'normal_plan_validation',$state_hash);
if(empty($validated['ok'])){
  echo json_encode(array('status'=>'P47_BLOCKED_PLAN_VALIDATE','detail'=>$validated,'publish_allowed'=>false),JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";
  exit(2);
}

$generated=PPM679_Content_Generator::generate($item,$pack);
$checked=PPM679_Content_Validator::check($generated,$item,'p47-public-check',$state_hash);
if(empty($checked['ok'])||($checked['technical_status']??'')!=='TECHNICAL_CHECK_OK'||($checked['content_quality_status']??'')!=='CONTENT_QUALITY_CHECK_OK'){
  echo json_encode(array('status'=>'P47_BLOCKED_CONTENT_CHECK','detail'=>$checked,'publish_allowed'=>false),JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";
  exit(2);
}

$prepared=PPM679_Normal_Draft_Adapter::prepare(
  $generated,
  $item,
  array(
    'technical_status'=>$checked['technical_status'],
    'content_quality_status'=>$checked['content_quality_status'],
    'content_hash'=>$checked['content_hash']
  ),
  $runtime,
  'p47-run',
  $plan_hash,
  $state_hash
);

$after=count(PPM679_WP::get_all_post_inventory($statuses));
$identity_ok=
  !empty($prepared['ok']) &&
  (string)($prepared['canonical_article_id']??'')===(string)$request['canonical_article_id'] &&
  (string)($prepared['plan_item_key']??'')===(string)$request['production_plan_item']['plan_item_key'];

echo json_encode(array(
  'status'=>($identity_ok&&$before===$after)?'P47_EXISTING_HANDOFF_PUBLIC_PREWRITE_PASS':'P47_PUBLIC_PREWRITE_BLOCKED',
  'input_truth'=>'FACHWORKFLOW_HANDOFF_REQUEST.json',
  'editorial_preflight_pass'=>!empty($editorial_gate['ok']),
  'live_state_pass'=>!empty($initial_gate['ok']),
  'plan_validation_pass'=>!empty($validated['ok']),
  'content_generation_used_public_api'=>true,
  'content_validation_used_public_api'=>true,
  'prepare_used_public_api'=>true,
  'prepare_no_write'=>$before===$after,
  'identity_bound'=>$identity_ok,
  'prepared'=>$prepared,
  'private_helper_used'=>false,
  'new_ppm_api_used'=>false,
  'new_handoff_used'=>false,
  'new_controller_used'=>false,
  'publish_allowed'=>false
),JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";
exit(($identity_ok&&$before===$after)?0:2);
'''

def run_json(cmd, cwd, timeout=180):
    p = subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
    lines = [x for x in p.stdout.splitlines() if x.strip()]
    decoder = json.JSONDecoder()
    obj = None
    for line in reversed(lines):
        try:
            candidate, _ = decoder.raw_decode(line.lstrip())
        except Exception:
            continue
        if isinstance(candidate, dict):
            obj = candidate
            break
    if obj is None:
        raise RuntimeError("P47_JSON_RESULT_MISSING:" + p.stdout[-4000:])
    if p.returncode != 0:
        raise RuntimeError("P47_COMMAND_FAILED:" + json.dumps(obj, ensure_ascii=False))
    return obj

def main():
    forbidden = ("self::bootstrap", "self::generate_all", "self::check_all", "Reflection", "create_drafts")
    if any(token in PUBLIC_PREWRITE_PHP for token in forbidden):
        raise RuntimeError("P47_PRIVATE_OR_WRITE_HELPER_REFERENCED")

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        ppm_out = root / "ppm"
        ppm_out.mkdir()
        with zipfile.ZipFile(PPM) as z:
            z.extractall(ppm_out)
        ppm = ppm_out / "portal-production-machine"

        handoff = root / "FACHWORKFLOW_HANDOFF_REQUEST.json"
        build = ppm / "p47-build-handoff.php"
        prewrite = ppm / "p47-public-prewrite.php"
        build.write_text(BUILD_HANDOFF_PHP, encoding="utf-8")
        prewrite.write_text(PUBLIC_PREWRITE_PHP, encoding="utf-8")

        ready = run_json(["php", str(build), str(handoff)], ppm)
        if ready.get("status") != "P47_HANDOFF_FIXTURE_READY":
            raise RuntimeError("P47_HANDOFF_FIXTURE_FAILED")

        request = _load_exact_handoff(handoff)
        before = handoff.read_bytes()

        result = run_json(["php", str(prewrite), str(handoff)], ppm)
        if result.get("status") != "P47_EXISTING_HANDOFF_PUBLIC_PREWRITE_PASS":
            raise RuntimeError("P47_PUBLIC_PREWRITE_NOT_PASS")
        if handoff.read_bytes() != before:
            raise RuntimeError("P47_HANDOFF_MUTATED")
        if result.get("prepare_no_write") is not True or result.get("identity_bound") is not True:
            raise RuntimeError("P47_CORE_INVARIANT_FAILED")

        print(json.dumps({
            "status": "P47_EXISTING_HANDOFF_PUBLIC_PREWRITE_PASS",
            "input_truth": "FACHWORKFLOW_HANDOFF_REQUEST.json",
            "contract": request["contract"],
            "public_sequence": [
                "Editorial_Plan_Runtime_Gate::preflight",
                "Live_State_Gate::verify_live_state_or_abort",
                "Plan_Validator::validate",
                "Content_Generator::generate",
                "Content_Validator::check",
                "Normal_Draft_Adapter::prepare",
            ],
            "prepare_no_write": True,
            "identity_bound": True,
            "handoff_unchanged": True,
            "private_helper_used": False,
            "new_ppm_api_used": False,
            "new_handoff_used": False,
            "new_controller_used": False,
            "publish_allowed": False,
        }, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
