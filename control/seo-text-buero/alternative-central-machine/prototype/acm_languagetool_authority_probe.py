#!/usr/bin/env python3
from __future__ import annotations
import json,re,subprocess,tempfile,zipfile
from pathlib import Path

REPO=Path(__file__).resolve().parents[4]
PPM=REPO/"control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip"

PHP=r'''<?php
require __DIR__.'/tests/normal-draft-production/fixture-builder.php';
nd_reset();
$p=nd_build_plan(4,'acm-lt-authority');
$item=null;
foreach($p['items'] as $x){if((string)($x['article_type']??'')==='Beratung'){$item=$x;break;}}
if(!is_array($item)){fwrite(STDERR,"BERATUNG_ITEM_MISSING\n");exit(2);}
$pack=PPM679_Storage::load_fact_pack((string)$item['source_snapshot_id']);
$g=PPM679_Content_Generator::generate($item,$pack);
$state='acm-lt-authority-state';
$check=PPM679_Content_Validator::check($g,$item,'acm-lt-authority',$state);
$ev=(array)($item['quality_binding']['language_evidence']??array());
echo json_encode(array(
 'status'=>'ACM_LANGUAGETOOL_AUTHORITY_RUNTIME',
 'validator_ok'=>!empty($check['ok']),
 'technical_status'=>$check['technical_status']??null,
 'content_quality_status'=>$check['content_quality_status']??null,
 'engine'=>$ev['engine']??null,
 'raw_finding_count'=>$ev['raw_finding_count']??null,
 'unresolved_finding_count'=>$ev['unresolved_finding_count']??null,
 'return_code'=>$ev['return_code']??null,
 'raw_report_sha256'=>$ev['raw_report_sha256']??null,
 'has_evidence_mode'=>array_key_exists('evidence_mode',$ev),
 'evidence_mode'=>$ev['evidence_mode']??null,
 'has_claude_field'=>array_key_exists('claude_review',$ev)||array_key_exists('independent_claude_review',$ev),
 'publish_allowed'=>false
),JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES|JSON_PRETTY_PRINT)."\n";
?>''';

def method_block(txt:str,name:str)->str:
    m=re.search(r"(?:public|private|protected)?\s*(?:static\s+)?function\s+"+re.escape(name)+r"\s*\(",txt)
    if not m:return ""
    b=txt.find("{",m.end());d=0
    for i in range(b,len(txt)):
        if txt[i]=="{":d+=1
        elif txt[i]=="}":
            d-=1
            if d==0:return txt[m.start():i+1]
    return ""

def main():
    with tempfile.TemporaryDirectory() as td:
        out=Path(td)/"ppm";out.mkdir()
        with zipfile.ZipFile(PPM) as z:z.extractall(out)
        root=out/"portal-production-machine"
        gate=root/"includes/content-structure-language-gate.php"
        contract=root/"contracts/content-structure-language-gate-v2.json"
        if not gate.is_file() or not contract.is_file():raise RuntimeError("LANGUAGE_GATE_FILES_MISSING")
        src=gate.read_text(encoding="utf-8")
        method=method_block(src,"check_language_evidence")
        if not method:raise RuntimeError("LANGUAGE_EVIDENCE_METHOD_MISSING")
        c=json.loads(contract.read_text(encoding="utf-8"))
        probe=root/"acm-lt-authority.php";probe.write_text(PHP,encoding="utf-8")
        cp=subprocess.run(["php",str(probe)],cwd=root,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        if cp.returncode!=0:raise RuntimeError("LANGUAGE_RUNTIME_FAILED:"+cp.stdout[-3000:])
        runtime=json.loads(cp.stdout)
        if runtime.get("validator_ok") is not True:raise RuntimeError("BERATUNG_VALIDATOR_NOT_PASS")
        if runtime.get("technical_status")!="TECHNICAL_CHECK_OK":raise RuntimeError("BERATUNG_TECHNICAL_NOT_PASS")
        if runtime.get("content_quality_status")!="CONTENT_QUALITY_CHECK_OK":raise RuntimeError("BERATUNG_QUALITY_NOT_PASS")
        if runtime.get("engine")!="LanguageTool 6.8 / Bestand 43":raise RuntimeError("LANGUAGETOOL_ENGINE_DRIFT")
        if runtime.get("raw_finding_count")!=0 or runtime.get("unresolved_finding_count")!=0 or runtime.get("return_code")!=0:
            raise RuntimeError("LANGUAGETOOL_ZERO_FINDING_INVARIANT_FAILED")
        if runtime.get("has_evidence_mode") is not False or runtime.get("has_claude_field") is not False:
            raise RuntimeError("BERATUNG_EXTERNAL_REVIEW_MODE_BOUND")
        special="FULL_LANGUAGETOOL43_BASELINE_PLUS_HASHED_MAINBLOCK1_DELTA_REQUIRES_INDEPENDENT_CLAUDE_REVIEW"
        print(json.dumps({
          "status":"ACM_LANGUAGETOOL_NO_EXTERNAL_AUTHORITY_PASS",
          "runtime":runtime,
          "normal_beratung_uses_special_claude_mode":False,
          "special_legacy_branch_present":special in method,
          "special_branch_conditioned_on_explicit_evidence_mode":special in method and "evidence_mode" in method,
          "contract_language_evidence":c.get("language_evidence"),
          "existing_content_validator_reused":True,
          "new_language_gate_created":False,
          "publish_allowed":False
        },ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())

# workflow-trigger: lt-no-external-authority-v1
