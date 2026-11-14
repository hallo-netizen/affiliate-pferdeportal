<?php
/* Original PSTE WordPress/PSTE inventory scan without any planned PSERC/PPM source.
 * Distinguishes truly missing history from a corrupt legacy plan (must fail closed). */
define('ABSPATH','/empty/');define('ARRAY_A','ARRAY_A');
define('TXE_PLANFREE_KISS_V1',true);define('PSTE_OPTION_EDITORIAL_PLAN_IMPORT','pste_editorial_plan_import_v1');
const ROOT='/mnt/data/pferdeatelier_audit/working_planfree_seo/texterstellung/';
$GLOBALS['opts']=[];
class QA_DB {
 public $prefix='wp_', $last_error='', $posts='wp_posts', $postmeta='wp_postmeta', $term_relationships='wp_term_relationships', $term_taxonomy='wp_term_taxonomy', $terms='wp_terms';
 function prepare($q,...$vals){return $q;}
 function get_var($q){return 0;}
 function get_results($q,$fmt=null){return [];}
}
$GLOBALS['wpdb']=new QA_DB();
function get_option($key,$default=null){return $GLOBALS['opts'][$key]??$default;}
function get_post_types($q=[],$return='names'){return ['post'=>'post','page'=>'page'];}
function apply_filters($hook,$v){return $v;}
function wp_json_encode($x,$flags=0){return json_encode($x,$flags);}
require ROOT.'original/pste/includes/class-pste-repository.php';
require ROOT.'original/pste/includes/class-pste-snapshot.php';
require ROOT.'original/pste/includes/class-pste-mini-workflow.php';
require ROOT.'original/pserc/includes/class-pserc-stable-json.php';
require ROOT.'original/pserc/includes/class-pserc-plan-snapshot-store.php';
require ROOT.'original/pserc/includes/class-pserc-plan-slot-identity.php';
$checks=[];$errors=[];
function qa($key,$fn){global $checks,$errors;try{$checks[$key]=(bool)$fn();}catch(Throwable $e){$checks[$key]=false;$errors[$key]=$e->getMessage();}}
qa('empty_wp_pste_without_ppm_yields_complete_snapshot',static function(){global $snapshot;$snapshot=PSTE_Mini_Workflow::readParkhausForMini();return ($snapshot['complete']??false)===true && preg_match('/^[a-f0-9]{64}$/D',$snapshot['sha256']??'');});
qa('original_wp_inventory_is_checked',static fn()=>($GLOBALS['snapshot']['sources']['WORDPRESS']['complete']??false)===true);
qa('original_pste_pool_is_checked',static fn()=>($GLOBALS['snapshot']['sources']['PSTE_PLAN']['complete']??false)===true);
qa('no_ppm_source_is_optional_not_created',static fn()=>($GLOBALS['snapshot']['sources']['PPM679_EXISTING_EDITORIAL_RUNTIME']['status']??'')==='NO_HISTORICAL_PLAN_REQUIRED' && !array_key_exists('ppm679_editorial_plan_runtime_state_v1',$GLOBALS['opts']));
qa('no_pserc_plan_is_optional_not_created',static fn()=>($GLOBALS['snapshot']['sources']['PSERC_ACTIVE_PLAN']['status']??'')==='NO_HISTORICAL_PLAN_REQUIRED' && !array_key_exists('pserc_plan_active_snapshot_v1',$GLOBALS['opts']));
$original=$GLOBALS['snapshot']??null;
$GLOBALS['opts']['ppm679_editorial_plan_runtime_state_v1']=['items'=>[]];
qa('corrupt_existing_ppm_history_still_fails_closed',static fn()=>!PSTE_Mini_Workflow::readParkhausForMini()['complete']);
$GLOBALS['opts']['ppm679_editorial_plan_runtime_state_v1']=null;
$GLOBALS['opts']['pserc_plan_active_snapshot_v1']=['contract'=>'INVALID'];
qa('corrupt_existing_pserc_history_still_fails_closed',static fn()=>!PSTE_Mini_Workflow::readParkhausForMini()['complete']);
$pass=count(array_filter($checks));echo json_encode(['pass'=>$pass,'total'=>count($checks),'checks'=>$checks,'errors'=>$errors],JSON_PRETTY_PRINT|JSON_UNESCAPED_SLASHES),"\n";exit($pass===count($checks)?0:1);
