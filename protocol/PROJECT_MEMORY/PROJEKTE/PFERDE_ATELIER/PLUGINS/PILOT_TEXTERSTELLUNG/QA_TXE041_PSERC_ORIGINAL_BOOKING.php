<?php
// Strict QA of unmodified original PSERC code; does not create WordPress posts.
define('ABSPATH','/fake-wp/');
define('PSERC_DIR', __DIR__.'/../working_pserc_booking/texterstellung/original/pserc/');
function get_option($name,$fallback=false){return $fallback;}
$files=['class-pserc-stable-json.php','class-pserc-plan-slot-identity.php','class-pserc-article-type-extension-registry.php','class-pserc-production-reader.php','class-pserc-slot-allocator.php'];
foreach($files as $n)require_once PSERC_DIR.$n;
$results=[];
$reg=PSERC_Article_Type_Extension_Registry::verified();
$results['original_signed_registry_pass']=!empty($reg['ok']);
$missing=PSERC_Production_Reader::snapshot('/definitely/nonexistent/ppm679');
$results['missing_ppm_fails_closed']=empty($missing['ok']) && ($missing['status']??'')==='PSERC_PRODUCTION_MACHINE_NOT_FOUND' || empty($missing['ok']) && str_starts_with((string)($missing['status']??''),'PSERC_PRODUCTION_');
$production=[
 'plan'=>['slots'=>[
  ['canonical_article_id'=>'ORIGINAL-SLOT-001','category_slug'=>'pflege','article_type'=>'Ratgeber','slot_number'=>1,'production_supported_by_current_engine'=>true,'draft_generation_allowed'=>true,'publish_allowed'=>false],
  ['canonical_article_id'=>'ORIGINAL-SLOT-002','category_slug'=>'pflege','article_type'=>'Ratgeber','slot_number'=>2,'production_supported_by_current_engine'=>true,'draft_generation_allowed'=>true,'publish_allowed'=>false]
 ]],
 'registered_article_types'=>['Ratgeber'],'supported_article_types'=>['Ratgeber'],
 'article_type_runtime'=>['Ratgeber'=>['status'=>'RELEASED']]
];
$topics=[
 ['pool_key'=>'ORIG-ONE','category_slug'=>'pflege','article_type'=>'Ratgeber'],
 ['pool_key'=>'ORIG-TWO','category_slug'=>'pflege','article_type'=>'Ratgeber'],
 ['pool_key'=>'ORIG-THREE','category_slug'=>'pflege','article_type'=>'Ratgeber']
];
$out=PSERC_Slot_Allocator::allocate($topics,$production,[]);
$rows=$out['items'];
$results['first_original_slot']=($rows[0]['status']??'')==='READY_FOR_METADATA_HANDOFF' && ($rows[0]['slot']['canonical_article_id']??'')==='ORIGINAL-SLOT-001';
$results['second_original_slot']=($rows[1]['status']??'')==='READY_FOR_METADATA_HANDOFF' && ($rows[1]['slot']['canonical_article_id']??'')==='ORIGINAL-SLOT-002';
$results['third_topic_held_without_slot']=($rows[2]['status']??'')==='BLOCKED_NO_FREE_CANONICAL_SLOT';
$results['no_duplicate_booking']=count(array_unique($out['reserved_ids']))===2;
$results['original_identity_token_stable']=PSERC_Plan_Slot_Identity::tokenFromCanonicalId('ORIGINAL-SLOT-001')===hash('sha256','pserc-plan-slot-v2|ORIGINAL-SLOT-001');
$blocked=PSERC_Slot_Allocator::allocate([$topics[0]],$production,['ORIGINAL-SLOT-001']);
$results['occupied_slot_not_reassigned']=($blocked['items'][0]['slot']['canonical_article_id']??'')==='ORIGINAL-SLOT-002';
$all=array_reduce($results,fn($n,$x)=>$n+(int)$x,0);
echo json_encode(['pass'=>$all,'total'=>count($results),'results'=>$results],JSON_PRETTY_PRINT|JSON_UNESCAPED_SLASHES),"\n";
exit($all===count($results)?0:1);
