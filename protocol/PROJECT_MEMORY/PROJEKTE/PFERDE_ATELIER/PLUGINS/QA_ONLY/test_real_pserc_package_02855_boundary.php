<?php
/** One-time QA of exact existing PSERC 0.28.55 source package, original PSTE capability and K0 firewall.
 * php this.php EXTRACTED_PSERC_ROOT QA_ONLY/PSTE_V22_REAL_READ_CAPABILITY_20261108.json
 */
declare(strict_types=1);
define('ABSPATH','/qa/');
$root=rtrim((string)($argv[1]??''),'/').'/';$capPath=(string)($argv[2]??'');
if(!is_file($root.'includes/class-pserc-seo-reader.php')||!is_file($capPath))
    throw new RuntimeException('EXACT_PSERC_QA_AND_PSTE_CAPABILITY_REQUIRED');
define('PSERC_DIR',$root);
define('PSERC_VERSION','0.28.55');
define('PSERC_BUILD','0.28.55-one-owner-no-fallback');
foreach(['stable-json','package-integrity','seo-source-binding','metadata-boundary'] as $n)
    require $root.'includes/class-pserc-'.$n.'.php';
function passed(bool $ok,string $msg):void {if(!$ok)throw new RuntimeException('FAIL '.$msg);echo "PASS $msg\n";}
$integrity=PSERC_Package_Integrity::validate();
passed(!empty($integrity['ok'])&&(int)$integrity['required_file_count']===61,
    '61/61 real PSERC 0.28.55 package file bindings');
$cap=json_decode(file_get_contents($capPath),true,512,JSON_THROW_ON_ERROR);
$source=PSERC_SEO_Source_Binding::validate(null,null,$cap);
passed(!empty($source['ok'])&&hash_equals((string)$source['capability_sha256'],(string)$cap['capability_sha256']),
    'actual original PSTE v22 read provider accepted by real PSERC 0.28.55');
$bad=$cap;$bad['write_capability_exposed']=true;
unset($bad['capability_sha256']);$bad['capability_sha256']=PSERC_Stable_Json::hash($bad);
$blocked=PSERC_SEO_Source_Binding::validate(null,null,$bad);
passed(empty($blocked['ok'])&&in_array('PSERC_SEO_CAPABILITY_FIREWALL_VIOLATION',$blocked['reason_codes']??[],true),
    'any upstream write capability blocked');
$item=['title'=>'Wie finde ich eine passende Pferdedecke?','target_keyword'=>'pferdedecke finden',
    'category'=>'pferdedecken','article_type'=>'FAQ','plan_slot'=>str_repeat('c',64)];
$batch=['contract'=>'PSERC_TEXTMACHINE_METADATA_BATCH_V2',
    'status'=>'READY_FOR_TEXTMACHINE_METADATA_INTAKE','item_count'=>1,'publish_allowed'=>false,
    'content_or_format_payload_present'=>false,'items'=>[$item]];
$batch['batch_sha256']=PSERC_Stable_Json::hash($batch);
passed(!empty(PSERC_Metadata_Boundary::validateBatch($batch)['ok']),
    'unchanged K0 accepts exactly five planning metadata fields');
foreach(['body_html','publish_allowed'] as $attack){
    $bad=$batch;
    if($attack==='body_html')$bad['items'][0]['body_html']='<p>not allowed</p>';
    else $bad['publish_allowed']=true;
    unset($bad['batch_sha256']);$bad['batch_sha256']=PSERC_Stable_Json::hash($bad);
    passed(empty(PSERC_Metadata_Boundary::validateBatch($bad)['ok']),
        'protected K0 rejects '.$attack);
}
echo "REAL_PSERC_02855_SOURCE_BOUNDARY_QA_PASS; NO_WORDPRESS_TEST\n";
