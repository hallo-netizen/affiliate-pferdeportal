<?php
/* Isolated functional QA: executes the original PSTE one-owner SEO decision method
   with the smallest technical slot removal in the isolated 0.4.1 candidate. */
error_reporting(E_ALL);
define('ABSPATH','/var/empty/');
define('TXE_PLANFREE_KISS_V1',true);
const ROOT='/mnt/data/pferdeatelier_audit/working_planfree_seo/texterstellung/';
$opts=[];
function get_option($k,$def=[]){global $opts; return $opts[$k]??$def;}
require ROOT.'original/pste/includes/class-pste-editorializer.php';
require ROOT.'original/pserc/includes/class-pserc-plan-slot-identity.php';
require ROOT.'original/pserc/includes/class-pserc-slot-allocator.php';
require ROOT.'original/pste/includes/class-pste-mini-workflow.php';
$key=str_repeat('a',64);$other=str_repeat('b',64);$snapHash=str_repeat('c',64);$intentSlot=str_repeat('d',64);$raw='Welche Trense passt?';
$payload=['raw_user_question'=>$raw,'proposed_article_type'=>'FAQ','target_category_slug'=>'trensen'];
$rows=[$key=>['pool_key'=>$key,'id'=>5,'payload_json'=>json_encode($payload)]];
$row=['pool_key'=>$key,'raw_query'=>$raw,'source_sha256'=>hash('sha256',$key.'|'.$raw),
 'box'=>'FREI','intent_slot'=>$intentSlot,'intent_summary'=>'Frage nach einer Trense','approved_title'=>''];
$doc=['contract'=>'PSTE_MINI_SEO_DECISIONS_V1','snapshot_sha256'=>$snapHash,'owner'=>'EXTERNAL_SINGLE_SEO_EDITOR','items'=>[$row]];
$snapshot=['complete'=>true,'sha256'=>$snapHash,'items'=>[]];
$state=['seo_decisions'=>[]];
$cases=[];
function qa($name,$truth){global $cases; $cases[$name]=$truth?'PASS':'FAIL';}
$first=PSTE_Mini_Workflow::acceptSingleOwnerSeoDecisions($state,$doc,$snapshot,$rows,[]);
$receipt=$first['seo_decisions'][$key]??[];
qa('new_FREI_no_PPM_is_FREI',($receipt['box']??'')==='FREI');
qa('canonical_uses_original_PSTE_pool_key',($receipt['canonical_article_id']??'')===$key);
qa('slot_from_UNCHANGED_PSERC_method',($receipt['plan_slot']??'')===PSERC_Plan_Slot_Identity::tokenFromCanonicalId($key));
qa('original_article_type_and_category',($receipt['article_type']??'')==='FAQ' && ($receipt['category_slug']??'')==='trensen');
$second=PSTE_Mini_Workflow::acceptSingleOwnerSeoDecisions($first,$doc,$snapshot,$rows,[]);
qa('repeat_keeps_original_identity',($second['seo_decisions'][$key]['canonical_article_id']??'')===$key && ($second['seo_decisions'][$key]['plan_slot']??'')===$receipt['plan_slot']);
$broken=$receipt;$broken['canonical_article_id']='';$broken['plan_slot']='';
$statePartial=['seo_decisions'=>[$key=>$broken]];
$held=PSTE_Mini_Workflow::acceptSingleOwnerSeoDecisions($statePartial,$doc,$snapshot,$rows,[]);
qa('legacy_FREI_unbooked_remains_unchanged',($held['seo_decisions'][$key]??null)===$broken);
qa('legacy_FREI_unbooked_is_technical_hold',($held['clarification'][$key]['reason_code']??'')==='PRETITLE_CANONICAL_PLAN_NOT_READY');
$occupied=PSTE_Mini_Workflow::acceptSingleOwnerSeoDecisions(['seo_decisions'=>[$other=>['box'=>'FREI','canonical_article_id'=>$key]]],$doc,$snapshot,$rows,[]);
qa('existing_identity_collision_rejected',($occupied['seo_decisions'][$key]['box']??'')==='KLAERUNG');
$spoof=$doc;$spoof['items'][0]['raw_query']='Andere Frage';
$fail=PSTE_Mini_Workflow::acceptSingleOwnerSeoDecisions($state,$spoof,$snapshot,$rows,[]);
qa('mismatched_original_query_cannot_be_FREI',($fail['seo_decisions'][$key]['box']??'')!=='FREI');
$badSnapshot=$snapshot;$badSnapshot['complete']=false;
try{PSTE_Mini_Workflow::acceptSingleOwnerSeoDecisions($state,$doc,$badSnapshot,$rows,[]);qa('incomplete_source_snapshot_fails_closed',false);}catch(RuntimeException $e){qa('incomplete_source_snapshot_fails_closed',true);}
$twice=$doc;$twice['items'][]=$row;
$duplicate=PSTE_Mini_Workflow::acceptSingleOwnerSeoDecisions($state,$twice,$snapshot,$rows,[]);
qa('duplicate_source_rows_not_approved',!isset($duplicate['seo_decisions'][$key]));
$unlisted=$doc;$unlisted['items'][0]['pool_key']=$other;$unlisted['items'][0]['source_sha256']=hash('sha256',$other.'|'.$raw);
$unknown=PSTE_Mini_Workflow::acceptSingleOwnerSeoDecisions($state,$unlisted,$snapshot,$rows,[]);
qa('missing_source_row_not_approved',($unknown['seo_decisions'][$other]['box']??'')!=='FREI');
$belegt=$doc;$belegt['items'][0]['box']='BELEGT';$belegt['items'][0]['matched_ref']='SOME:missing';
$missing=PSTE_Mini_Workflow::acceptSingleOwnerSeoDecisions($state,$belegt,$snapshot,$rows,[]);
qa('BELEGT_unknown_reference_blocked',($missing['seo_decisions'][$key]['box']??'')==='KLAERUNG');
$pass=count(array_filter($cases,fn($x)=>$x==='PASS'));
echo json_encode(['pass'=>$pass,'total'=>count($cases),'checks'=>$cases],JSON_PRETTY_PRINT|JSON_UNESCAPED_SLASHES),"\n";
exit($pass===count($cases)?0:1);
