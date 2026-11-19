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
case_run('compact_original_valid',$fn=fn()=>!empty(PSERC_System4_Import::normalizePayload(payload())['ok']));
case_run('wrong_contract_rejected',fn()=>rejection(['contract'=>'UNKNOWN','articles'=>[row()]],'PSERC_SYSTEM4_CONTRACT_INVALID'));
case_run('missing_keyword_rejected',function(){$r=row();$r['target_keyword']='';return rejection(payload($r),'PSERC_SYSTEM4_ARTICLE_FIELD_INVALID');});
case_run('invalid_slot_rejected',function(){$r=row();$r['plan_slot']='notasha';return rejection(payload($r),'PSERC_SYSTEM4_PLAN_SLOT_INVALID');});
case_run('wrong_article_identity_rejected',function(){$r=row();$r['plan_slot']=PSERC_Plan_Slot_Identity::tokenFromCanonicalId('other');return rejection(payload($r),'PSERC_SYSTEM4_CANONICAL_PLAN_SLOT_MISMATCH');});
case_run('unsafe_slug_rejected',function(){$r=row();$r['slug']='Pferdepflege Verstehen';return rejection(payload($r),'PSERC_SYSTEM4_POST_SLUG_NOT_CANONICAL');});
case_run('duplicate_batch_slot_rejected',function(){$r=row();return rejection(['contract'=>PSERC_System4_Import::CONTRACT,'articles'=>[$r,$r]],'PSERC_SYSTEM4_PLAN_SLOT_DUPLICATE');});
if(($argv[1]??'')==='no-ppm'){
  case_run('missing_ppm_blocks_no_wp_writes',function(){$res=PSERC_System4_Import::importPayload(payload());return empty($res['ok'])&&in_array('PSERC_SYSTEM4_EDITORIAL_RUNTIME_GATE_UNAVAILABLE',(array)($res['reason_codes']??[]),true)&&$GLOBALS['wp_insert_count']===0;});
}else{
  case_run('unknown_category_blocks_before_write',function(){$r=row();$r['category']='does-not-exist';$res=PSERC_System4_Import::importPayload(payload($r));return empty($res['ok'])&&$GLOBALS['wp_insert_count']===0;});
  case_run('draft_created_only_and_ppm_synced',function(){$res=PSERC_System4_Import::importPayload(payload());return !empty($res['ok'])&&count($res['created_post_ids'])===1&&$GLOBALS['wp_insert_count']===1&&$GLOBALS['ppm_count']===1&&$GLOBALS['wp_posts'][$res['created_post_ids'][0]]['post_status']==='draft'&&($res['publish_allowed']??null)===false;});
  case_run('same_payload_no_second_post_reuse',function(){ $p=(new ReflectionClass(PSERC_System4_Import::class))->getProperty('collisionIndex');$p->setAccessible(true);$p->setValue(null,null);$res=PSERC_System4_Import::importPayload(payload());return !empty($res['ok'])&&$GLOBALS['wp_insert_count']===1&&count($res['existing_reused_post_ids'])===1&&($res['publish_allowed']??null)===false;});
  case_run('ppm_failure_rolls_back_new_draft',function(){ $GLOBALS['ppm_mode']='fail';$p=(new ReflectionClass(PSERC_System4_Import::class))->getProperty('collisionIndex');$p->setAccessible(true);$p->setValue(null,null);$r=row('probe-002');$r['title']='Richtige Halfter';$r['slug']='richtige-halfter';$res=PSERC_System4_Import::importPayload(payload($r));return empty($res['ok'])&&in_array('PSERC_SYSTEM4_REDAKTIONSPLAN_RUNTIME_SYNC_FAILED',(array)($res['reason_codes']??[]),true)&&count($GLOBALS['wp_deleted'])===1&&count($GLOBALS['wp_posts'])===1;});
}
$ok=array_sum(array_map(fn($r)=>(int)$r['pass'],$cases));$ret=['kind'=>'ORIGINAL_PSERC_IMPORT_WITH_ISOLATED_WP_AND_PPM_MOCKS_ONLY','mode'=>$argv[1]??'normal','pass'=>$ok,'total'=>count($cases),'results'=>$cases,'source_files'=>['class-pserc-stable-json.php','class-pserc-plan-slot-identity.php','class-pserc-system4-import.php'],'wp_live_test'=>false,'ppm_real_source_test'=>false,'new_plugin_created'=>false];
echo json_encode($ret,JSON_UNESCAPED_UNICODE|JSON_PRETTY_PRINT|JSON_UNESCAPED_SLASHES),"\n";
exit($ok===count($cases)?0:1);