<?php
// TEMPORARY TEST HARNESS ONLY: existing PSERC PHP source is required unchanged.
// No WordPress site, no plugin sources, no production data are modified.
error_reporting(E_ALL);
define('ABSPATH', '/isolated-mock-wordpress/');
define('ARRAY_A', 'ARRAY_A');
$GLOBALS['wp_posts'] = [];
$GLOBALS['wp_next_id'] = 400;
$GLOBALS['wp_deleted'] = [];
$GLOBALS['wp_insert_count'] = 0;
$GLOBALS['ppm_count'] = 0;
$GLOBALS['ppm_mode'] = 'pass';
function get_term_by($field,$slug,$taxonomy) {return $field==='slug'&&$taxonomy==='category'&&$slug==='reitpflege'?(object)['term_id'=>42,'slug'=>'reitpflege']:false;}
function sanitize_title($s) {return trim(preg_replace('/[^a-z0-9]+/','-',strtolower($s)),'-');}
function wp_slash($arr) {return $arr;}
function wp_insert_post($arr,$wp_error=false) {
   $id=$GLOBALS['wp_next_id']++;
   $GLOBALS['wp_posts'][$id]=['ID'=>$id,'post_type'=>$arr['post_type'],'post_status'=>$arr['post_status'],'post_title'=>$arr['post_title'],'post_name'=>$arr['post_name'],'post_content'=>$arr['post_content'],'post_category'=>$arr['post_category'],'meta_input'=>$arr['meta_input']];
   $GLOBALS['wp_insert_count']++;
   return $id;
}
function get_post($id,$type=null){return $GLOBALS['wp_posts'][$id] ?? null;}
function get_post_meta($id,$key,$single=false){return $GLOBALS['wp_posts'][$id]['meta_input'][$key] ?? '';}
function wp_get_post_categories($id){return $GLOBALS['wp_posts'][$id]['post_category']??[];}
function get_posts($opts){return array_keys($GLOBALS['wp_posts']);}
function wp_delete_post($id,$force=false){unset($GLOBALS['wp_posts'][$id]);$GLOBALS['wp_deleted'][]=$id;return true;}
if(($argv[1]??'')!=='no-ppm'){
  class PPM679_Editorial_Plan_Runtime_Gate {
    public static function record_readback($bindings,$readback,$reason){$GLOBALS['ppm_count']++;if($GLOBALS['ppm_mode']==='fail')return ['ok'=>false,'status'=>'TEST_PPM_FAILURE'];return ['ok'=>true,'status'=>'TEST_PPM_ACK','publish_allowed'=>false];}
  }
}
$base=dirname(__DIR__).'/source/pserc/portal-seo-editorial-plan-compiler/includes/';
require $base.'class-pserc-stable-json.php';
require $base.'class-pserc-plan-slot-identity.php';
require $base.'class-pserc-system4-import.php';
function row($id='probe-001'){
 return ['article_id'=>$id,'plan_slot'=>PSERC_Plan_Slot_Identity::tokenFromCanonicalId($id),'title'=>'Pferdepflege verstehen','slug'=>'pferdepflege-verstehen','target_keyword'=>'pferdepflege','category'=>'reitpflege','article_type'=>'RATGEBER','body'=>'<p>Pferdepflege im Alltag.</p>'];
}
function payload($row=null){return ['contract'=>PSERC_System4_Import::CONTRACT,'articles'=>[$row??row()]];}
$cases=[];
function case_run($name,$fn){try{$ok=$fn();$cases=&$GLOBALS['cases'];$cases[]=['test'=>$name,'pass'=>(bool)$ok];}catch(Throwable $e){$GLOBALS['cases'][]=['test'=>$name,'pass'=>false,'error'=>get_class($e).':'.$e->getMessage()];}}
function rejection($p,$code){$x=PSERC_System4_Import::normalizePayload($p);return empty($x['ok'])&&in_array($code,(array)($x['reason_codes']??[]),true);}
function newrow($n){
  $r=row(sprintf('qa-probe-%03d',$n));
  $r['title']='QA Pferdepflege Thema '.$n;
  $r['slug']='qa-pferdepflege-thema-'.$n;
  $r['target_keyword']='qa-pferdepflege-thema-'.$n;
  return $r;
}
function packQ($rows){return ['contract'=>PSERC_System4_Import::CONTRACT,'articles'=>$rows];}
function reset_mock_request_cache(){(new ReflectionClass(PSERC_System4_Import::class))->getProperty('collisionIndex')->setValue(null,null);}
$rows=array_map('newrow',range(1,20));
case_run('original_13_of_20_as_drafts',function()use($rows){$x=PSERC_System4_Import::importPayload(packQ(array_slice($rows,0,13)));return !empty($x['ok'])&&count($x['created_post_ids'])===13&&count($GLOBALS['wp_posts'])===13&&$GLOBALS['ppm_count']===1;});
case_run('original_remaining_7_import_without_dup',function()use($rows){reset_mock_request_cache();$x=PSERC_System4_Import::importPayload(packQ(array_slice($rows,13)));return !empty($x['ok'])&&count($x['created_post_ids'])===7&&count($GLOBALS['wp_posts'])===20&&$GLOBALS['ppm_count']===2;});
case_run('original_twenty_draft_status_not_public',fn()=>count($GLOBALS['wp_posts'])===20&&count(array_filter($GLOBALS['wp_posts'],fn($x)=>$x['post_status']==='draft'&&$x['meta_input']['_ppm679_publish_blocked']==='1'))===20);
case_run('original_full_replay_reuses_all_twenty',function()use($rows){reset_mock_request_cache();$x=PSERC_System4_Import::importPayload(packQ($rows));return !empty($x['ok'])&&count($x['created_post_ids'])===0&&count($x['existing_reused_post_ids'])===20&&count($GLOBALS['wp_posts'])===20&&$GLOBALS['wp_insert_count']===20;});
case_run('original_replay_changed_content_blocks',function()use($rows){reset_mock_request_cache();$r=$rows[0];$r['body'].='<p>Geändert!</p>';$x=PSERC_System4_Import::importPayload(packQ([$r]));return empty($x['ok'])&&in_array('PSERC_SYSTEM4_WORDPRESS_COLLISION',(array)($x['reason_codes']??[]),true)&&count($GLOBALS['wp_posts'])===20;});
case_run('original_replay_title_drift_blocks',function()use($rows){reset_mock_request_cache();$r=$rows[0];$r['title']='Andere Überschrift';$x=PSERC_System4_Import::importPayload(packQ([$r]));return empty($x['ok'])&&in_array('PSERC_SYSTEM4_WORDPRESS_COLLISION',(array)($x['reason_codes']??[]),true)&&count($GLOBALS['wp_posts'])===20;});
case_run('original_new_slug_collision_blocks',function()use($rows){reset_mock_request_cache();$r=newrow(21);$r['slug']=$rows[0]['slug'];$x=PSERC_System4_Import::importPayload(packQ([$r]));return empty($x['ok'])&&in_array('PSERC_SYSTEM4_WORDPRESS_COLLISION',(array)($x['reason_codes']??[]),true)&&count($GLOBALS['wp_posts'])===20;});
case_run('original_ppm_failure_rolls_back_21st',function(){$GLOBALS['ppm_mode']='fail';reset_mock_request_cache();$r=newrow(21);$x=PSERC_System4_Import::importPayload(packQ([$r]));return empty($x['ok'])&&in_array('PSERC_SYSTEM4_REDAKTIONSPLAN_RUNTIME_SYNC_FAILED',(array)($x['reason_codes']??[]),true)&&count($GLOBALS['wp_posts'])===20&&count($GLOBALS['wp_deleted'])===1;});
$pass=array_sum(array_map(fn($r)=>(int)$r['pass'],$cases));
$out=['kind'=>'UNCHANGED_PSERC_SYSTEM4_IMPORT_TEST_WITH_MOCK_WP_AND_MOCK_PPM_NOT_LIVE','mode'=>'20_rows_13_plus_7_replay_conflicts_rollback','pass'=>$pass,'total'=>count($cases),'results'=>$cases,'post_statuses'=>array_count_values(array_column($GLOBALS['wp_posts'],'post_status')),'insert_attempts'=>$GLOBALS['wp_insert_count'],'ppm_sync_calls'=>$GLOBALS['ppm_count'],'new_plugin_created'=>false,'real_wordpress_test'=>false,'real_ppm_source_test'=>false];
echo json_encode($out,JSON_PRETTY_PRINT|JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES),"\n";
exit($pass===count($cases)?0:1);