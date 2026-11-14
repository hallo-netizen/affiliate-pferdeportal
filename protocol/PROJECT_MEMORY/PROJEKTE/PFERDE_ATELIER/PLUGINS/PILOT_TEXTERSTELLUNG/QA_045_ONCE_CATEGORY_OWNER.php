<?php
declare(strict_types=1);
/** Verify that the actual TXE source makes no repeated category decision.
 * The original user topic IDs and labels are injected from the uploaded diagnosis;
 * database answer is deliberately MISSING (no fabricated categories).
 */
define('ABSPATH','/qa/'); define('ARRAY_A','ARRAY_A'); define('DOING_CRON',true);
$GLOBALS['options']=[]; $GLOBALS['calls']=[]; $GLOBALS['hooks']=[];
function home_url($p='/'){return 'https://oliver-beil.de/';}
function get_current_blog_id(){return 1;}
function get_option($k,$d=false){return $GLOBALS['options'][$k]??$d;}
function get_site_option($k,$d=false){return $d;}
function update_option($k,$v,$auto=false){$GLOBALS['options'][$k]=$v;return true;}
function current_user_can($cap){return $cap==='manage_options';}
function user_can($id,$cap){return $id===7 && $cap==='manage_options';}
function get_current_user_id(){return 7;}
function add_action($n,$cb,$p=10,$a=1){$GLOBALS['hooks'][$n][]=$cb;}
function add_filter($n,$cb,$p=10,$a=1){}function register_activation_hook(...$v){}function register_deactivation_hook(...$v){}
function wp_json_encode($x,$f=0){return json_encode($x,$f);} function wp_strip_all_tags($s){return strip_tags($s);}function is_admin(){return false;}
function is_wp_error($x){return false;}
class DB {
 public string $last_error=''; public string $prefix='wp_';
 function prepare($q,...$v){foreach($v as $x){$pos=strpos($q,'%s');if($pos===false)throw new RuntimeException('PREPARE_BAD');$q=substr_replace($q,"'".$x."'",$pos,2);}return $q;}
 function get_results($q,$format=ARRAY_A){return [];}
 function get_var($q){return str_contains($q,'GET_LOCK')||str_contains($q,'RELEASE_LOCK')?'1':null;}
}
$GLOBALS['wpdb']=new DB();
class PSTE_Repository{static function table($t){return 'wp_pste_topic_pool';}}
class PSTE_Mini_Workflow{
 static function hasStoredFinalFrei(string $key,string $raw):bool{
  $x=$GLOBALS['options']['pste_mini_keyword_roundtrip_v1']['seo_decisions'][$key]??[];
  return ($x['box']??'')==='FREI' && ($x['raw_query']??'')===$raw && ($x['source_sha256']??'')===hash('sha256',$key.'|'.$raw);
 }
}
class PSTE_Admin{
 static function completeExistingCategoryRoom(array $keys,int $reviewer):array{
  $GLOBALS['calls'][]=$keys;
  if($reviewer!==7)throw new RuntimeException('REVIEWER_NOT_AUTHORIZED');
  return ['considered'=>count($keys),'assigned'=>0,'still_open'=>count($keys)];
 }
}
// Deliberately do not confirm before loading; so no nested PSTE module is used.
require __DIR__.'/texterstellung/texterstellung.php';
$GLOBALS['options'][TXE_Workshop::TEST_MODE_OPTION]=hash('sha256',home_url('/').'|'.get_current_blog_id());
$diag=json_decode((string)file_get_contents(__DIR__.'/tests/inputs/texterstellung-diagnose-20261114-143548.json'),true,512,JSON_THROW_ON_ERROR);
if(count($diag['orders']??[])!==61)throw new RuntimeException('REAL_61_MISSING');
$proofs=[];
foreach($diag['orders'] as $a){
 $k=$a['source_id'];$raw=$a['keyword'];
 $proofs[$k]=['contract'=>'PSTE_MINI_SEO_DECISIONS_V1','box'=>'FREI','raw_query'=>$raw,'approved_title'=>$a['title'],'intent_summary'=>$a['intent'],'source_sha256'=>hash('sha256',$k.'|'.$raw)];
}
$GLOBALS['options']['pste_mini_keyword_roundtrip_v1']=['seo_decisions'=>$proofs,'completed'=>[]];
$checks=[];function ck($name,bool $ok){$GLOBALS['checks'][$name]=$ok;}
$first=TXE_Workshop::loadLegacyApprovals();
$firstState=get_option(TXE_Workshop::OPTION);
ck('first_pass_sends_61_real_ids_to_same_category_owner',count($GLOBALS['calls'])===1 && count($GLOBALS['calls'][0])===61);
ck('61_real_topics_marked_exactly_once',count($firstState['orders'])===61 && count(array_filter($firstState['orders'],fn($o)=>!empty($o['category_owner_visited'])))===61);
ck('61_topics_stay_held_without_real_source_category',count(array_filter($firstState['orders'],fn($o)=>$o['status']==='METADATEN_OFFEN' && $o['category']==='' && $o['article_type']===''))===61);
$again=TXE_Workshop::loadLegacyApprovals();
ck('repeat_import_does_not_run_category_owner',count($GLOBALS['calls'])===1 && $again['total']===61);
TXE_Workshop::reconcileExistingCategoryBindings();
ck('daily_cron_never_runs_category_owner',count($GLOBALS['calls'])===1);
$thirdState=get_option(TXE_Workshop::OPTION);
ck('existing_order_marks_survive_repeat_and_cron',count(array_filter($thirdState['orders'],fn($o)=>!empty($o['category_owner_visited'])))===61);
ck('no_categories_or_types_fabricated',count(array_filter($thirdState['orders'],fn($o)=>$o['category']!==''||$o['article_type']!==''||$o['plan_slot']!==''||$o['article_id']!==''))===0);
$missing=($diag['orders'][0]['source_id']??'');unset($GLOBALS['options']['pste_mini_keyword_roundtrip_v1']['seo_decisions'][$missing]);
$newKey='89fe3dc2-59d3-49ac-8ddb-fde3b6b16a36';$raw='Echter zukünftiger Testfall ohne Kategorie';
$GLOBALS['options']['pste_mini_keyword_roundtrip_v1']['seo_decisions'][$newKey]=['contract'=>'PSTE_MINI_SEO_DECISIONS_V1','box'=>'FREI','raw_query'=>$raw,'source_sha256'=>hash('sha256',$newKey.'|'.$raw),'approved_title'=>'','intent_summary'=>''];
TXE_Workshop::reconcileExistingCategoryBindings();
ck('future_topic_recovered_by_technical_sync_without_second_decision',count($GLOBALS['calls'])===1 && count(get_option(TXE_Workshop::OPTION)['orders'])===62);
$news=array_values(array_filter(get_option(TXE_Workshop::OPTION)['orders'],fn($o)=>$o['source_id']===$newKey));
ck('future_topic_not_prematurely_marked_decided',count($news)===1 && empty($news[0]['category_owner_visited']));
TXE_Workshop::loadLegacyApprovals();
ck('new_topic_gets_first_and_only_owner_turn',count($GLOBALS['calls'])===2 && $GLOBALS['calls'][1]===[$newKey]);
TXE_Workshop::loadLegacyApprovals();
ck('new_topic_repeat_does_not_restart_owner',count($GLOBALS['calls'])===2);
$pass=count(array_filter($checks));echo json_encode(['pass'=>$pass,'total'=>count($checks),'checks'=>$checks,'category_owner_invocation_lengths'=>array_map('count',$GLOBALS['calls']),'real_data_source'=>'user 61 diagnostics, no DB category rows or artificial metadata'],JSON_PRETTY_PRINT|JSON_UNESCAPED_UNICODE),"\n";exit($pass===count($checks)?0:1);
