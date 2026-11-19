<?php
define('ABSPATH','/wp-mock/');
$hooks=[];
function add_action($name,$fn,$priority=10,$args=1){global $hooks;$hooks[$name][]=[$priority,$fn];}
function add_filter($name,$fn,$priority=10,$args=1){add_action($name,$fn,$priority,$args);}
function register_activation_hook($file,$callback){}
function get_option($name,$default=false){return $default;}
function get_site_option($name,$default=false){return $default;}
function is_admin(){return false;}
function get_term_by($field,$value,$taxonomy){return (object)['term_id'=>12,'slug'=>$value];}
function home_url($path='/'){return 'https://pferde-atelier.test/';}
require '/mnt/data/pferdeatelier_audit/txe041_originalresearch/texterstellung/texterstellung.php';
$rm=new ReflectionMethod('TXE_Workshop','enqueue');
$state=['orders'=>[]];
$original='PSTE-SOURCE-ARTICLE-NEW-REAL-IDENTITY';$slot=PSERC_Plan_Slot_Identity::tokenFromCanonicalId($original);
$fields=['source_id'=>'orig-id-123','target_keyword'=>'pferdedecken reinigen','title'=>'Pferdedecken schonend reinigen','category'=>'pferdedecken','article_type'=>'Beratung','article_id'=>$original,'plan_slot'=>$slot];
$id=$rm->invokeArgs(null,[&$state,$fields,'ALT_FREIGABE']);
$checks=['preexisting_original_slot_preserved'=>($state['orders'][$id]['plan_slot']??'')===$slot,'original_canonical_id_preserved'=>($state['orders'][$id]['article_id']??'')===$original,'existing_complete_free'=>($state['orders'][$id]['status']??'')==='FREI'];
$other=$fields;$other['source_id']='orig-id-456';$other['target_keyword']='pferdedecken trocknen';$other['plan_slot']='';$other['article_id']='';
$id2=$rm->invokeArgs(null,[&$state,$other,'ALT_FREIGABE']);
$checks['missing_original_slot_remains_empty']=($state['orders'][$id2]['plan_slot']??'')==='';
$checks['missing_original_id_remains_empty']=($state['orders'][$id2]['article_id']??'')==='';
$checks['missing_original_identity_on_hold']=($state['orders'][$id2]['status']??'')==='METADATEN_OFFEN';
$partial=$fields;$partial['source_id']='orig-id-777';$partial['target_keyword']='pferdedecken reinigen nach regen';$partial['plan_slot']='';
$id3=$rm->invokeArgs(null,[&$state,$partial,'ALT_FREIGABE']);
$checks['partial_original_canonical_preserved']=($state['orders'][$id3]['article_id']??'')===$original;
$checks['partial_original_identity_held']=($state['orders'][$id3]['status']??'')==='METADATEN_OFFEN';
$half=$fields;$half['source_id']='orig-id-778';$half['target_keyword']='pferdedecken reinigen im winter';$half['article_id']='';
$id4=$rm->invokeArgs(null,[&$state,$half,'ALT_FREIGABE']);
$checks['partial_original_slot_preserved']=($state['orders'][$id4]['plan_slot']??'')===$slot;
$checks['slot_without_original_article_held']=($state['orders'][$id4]['status']??'')==='METADATEN_OFFEN';

try{$bad=$fields;$bad['source_id']='orig-id-789';$bad['target_keyword']='pferdedecken neu';$bad['plan_slot']=str_repeat('b',64);$rm->invokeArgs(null,[&$state,$bad,'ALT_FREIGABE']);$checks['mismatched_identity_rejected']=false;}catch(RuntimeException $ex){$checks['mismatched_identity_rejected']=$ex->getMessage()==='SLOT_ARTICLE_ID_MISMATCH';}
$result=['pass'=>!in_array(false,$checks,true),'checks'=>$checks,'source'=>'Original PSERC_Plan_Slot_Identity and existing TXE enqueue'];
echo json_encode($result,JSON_PRETTY_PRINT|JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES),"\n";exit($result['pass']?0:1);