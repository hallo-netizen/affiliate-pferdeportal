<?php
/** ONE-TIME QA against the actual, unmodified extracted PSERC-0.28.54 ZIP.
 * Not a WordPress plugin or runtime worker. Run: php this.php /path/to/extracted/portal-seo-editorial-plan-compiler
 */
declare(strict_types=1);
define('ABSPATH','/qa/');
$root=rtrim((string)($argv[1]??''),'/').'/';
if(!is_file($root.'portal-seo-editorial-plan-compiler.php'))throw new RuntimeException('ACTUAL_PSERC_ROOT_REQUIRED');
define('PSERC_DIR',$root);
define('PSERC_VERSION','0.28.54');
define('PSERC_BUILD','0.28.54-central-owner-kiss');
foreach(['stable-json','package-integrity','seo-source-binding','metadata-boundary'] as $name)
    require $root.'includes/class-pserc-'.$name.'.php';
function proved(bool $ok,string $label):void {if(!$ok)throw new RuntimeException('FAIL '.$label);echo "PASS $label\n";}
$integrity=PSERC_Package_Integrity::validate();
proved(!empty($integrity['ok'])&&(int)$integrity['required_file_count']===61,'61/61 actual PSERC QA package file bindings');
$c=json_decode(file_get_contents($root.'contracts/seo-engine-capability-binding-v2.json'),true,512,JSON_THROW_ON_ERROR);
$cap=['contract'=>$c['expected_capability_contract'],
    'capability_version'=>$c['expected_capability_version'],
    'topic_metadata_schema'=>$c['expected_topic_metadata_schema'],
    'editorial_quality_contract'=>$c['expected_editorial_quality_contract'],
    'intent_profile_contract'=>$c['expected_intent_profile_contract'],
    'target_keyword_contract'=>$c['expected_target_keyword_contract'],
    'optional_pre_handoff_ownership_fields'=>$c['expected_optional_pre_handoff_ownership_fields'],
    'ownership_gate_contract'=>$c['expected_ownership_gate_contract'],
    'ownership_gate_required_when_upstream_candidate_is_promoted'=>true,
    'question_form_has_ownership_authority'=>false,'engine_schema'=>'12',
    'handoff_fields'=>$c['exact_handoff_fields'],'intent_first'=>true,
    'intent_metadata_internal_only'=>true,'content_or_design_payload_allowed'=>false,
    'write_capability_exposed'=>false,'required_read_symbols'=>[]];
$cap['capability_sha256']=PSERC_Stable_Json::hash($cap);
proved(!empty(PSERC_SEO_Source_Binding::validate(null,$c,$cap)['ok']),
    'exact original PSERC read-contract with synthetic valid capability');
$bad=$cap;$bad['write_capability_exposed']=true;$bad['capability_sha256']=PSERC_Stable_Json::hash($bad);
proved(empty(PSERC_SEO_Source_Binding::validate(null,$c,$bad)['ok']),
    'any producer write-capability blocked');
$bad=$cap;$bad['handoff_fields'][]='body_html';$bad['capability_sha256']=PSERC_Stable_Json::hash($bad);
proved(empty(PSERC_SEO_Source_Binding::validate(null,$c,$bad)['ok']),
    'sixth handoff field blocked');
$bad=$c;$bad['expected_capability_version']='9.9.9';
proved(empty(PSERC_SEO_Source_Binding::validate(null,$bad,$cap)['ok']),
    'tampered PSERC capability contract blocked');
$item=['title'=>'Welche Regendecke passt zu meinem Pferd?','target_keyword'=>'regendecke pferd',
    'category'=>'regendecken','article_type'=>'FAQ','plan_slot'=>str_repeat('a',64)];
$batch=['contract'=>'PSERC_TEXTMACHINE_METADATA_BATCH_V2','status'=>'READY_FOR_TEXTMACHINE_METADATA_INTAKE',
    'item_count'=>1,'publish_allowed'=>false,'content_or_format_payload_present'=>false,'items'=>[$item]];
$batch['batch_sha256']=PSERC_Stable_Json::hash($batch);
proved(!empty(PSERC_Metadata_Boundary::validateBatch($batch)['ok']),'five exact scalar fields PASS');
foreach(['body_html','publish_allowed'] as $field){
    $bad=$batch;
    if($field==='body_html')$bad['items'][0][$field]='<p>forbidden</p>';
    else $bad[$field]=true;
    unset($bad['batch_sha256']);$bad['batch_sha256']=PSERC_Stable_Json::hash($bad);
    proved(empty(PSERC_Metadata_Boundary::validateBatch($bad)['ok']),$field.' protected K0 boundary');
}
echo "ACTUAL_PSERC_PACKAGE_QA_PASS; NOT A REAL WORDPRESS OR EXTERNAL SEO END-TO-END\n";
