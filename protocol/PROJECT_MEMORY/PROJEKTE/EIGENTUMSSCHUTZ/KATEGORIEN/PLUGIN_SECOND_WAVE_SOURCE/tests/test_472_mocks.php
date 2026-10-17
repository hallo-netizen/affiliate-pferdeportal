<?php
error_reporting(E_ALL);
define('ABSPATH','/tmp/');define('APKW_DIR',__DIR__.'/affiliate-portal-kategorie-workflow/');
$GLOBALS['opt']=[];$GLOBALS['wp_terms']=[];$GLOBALS['wp_pages']=[];$GLOBALS['meta']=[];$GLOBALS['writes']=[];$GLOBALS['fail_after']=null;
function get_option($k,$fallback=null){return $GLOBALS['opt'][$k]??$fallback;}
function update_option($k,$v,$aut=false){$GLOBALS['opt'][$k]=$v;return true;}
function delete_option($k){unset($GLOBALS['opt'][$k]);}
function add_option($k,$v,$dep='',$autoload='no'){if(isset($GLOBALS['opt'][$k]))return false;$GLOBALS['opt'][$k]=$v;return true;}
function sanitize_title($s){$t=iconv('UTF-8','ASCII//TRANSLIT//IGNORE',$s);return trim(preg_replace('/[^a-z0-9]+/','-',strtolower($t)),'-');}
function is_wp_error($x){return $x instanceof WP_Error;}
class WP_Error{}
function get_terms($args){$slugs=$args['slug']??[];return array_values(array_filter($GLOBALS['wp_terms'],fn($t)=>in_array($t->slug,$slugs,true)));}
function get_post($id){return $GLOBALS['wp_pages'][$id]??null;}
function get_term($id,$tax){return $GLOBALS['wp_terms'][$id]??null;}
function get_term_link($id,$tax){return isset($GLOBALS['wp_terms'][$id])?'https://hab-und-bewahr.de/category/'.$GLOBALS['wp_terms'][$id]->slug.'/':new WP_Error();}
function update_term_meta($id,$key,$value){$GLOBALS['meta'][$id][$key]=$value;return true;}
function delete_term_meta($id,$key){unset($GLOBALS['meta'][$id][$key]);}
function get_term_meta($id,$key,$single=true){return $GLOBALS['meta'][$id][$key]??'';}
function wp_specialchars_decode($s,$mode){return html_entity_decode($s,$mode|ENT_HTML5,'UTF-8');}
function is_multisite(){return false;}
class APKW_TargetTreeSync {
 public static function active_snapshot(){return get_option('apkw_target_tree_active_snapshot_v1',[]);}
 public static function active_revision(){return get_option('apkw_target_tree_active_revision_v1','');}
 public static function state(){return ['status'=>'COMPLETE'];}
}
class APKW_C22_AddOnly {
 public static function completion_audit(){return ['valid'=>true,'errors'=>[],'new_objects_verified_in_snapshot'=>743];}
 public static function owns_runtime(){return true;}
 public static function state(){return ['status'=>'COMPLETE'];}
}
class APKW_TargetWriter {
 public static function target_tree_insert_term($tax,$args){
  $count=count($GLOBALS['writes']);if($GLOBALS['fail_after']!==null && $count >= $GLOBALS['fail_after'])throw new RuntimeException('INJECTED_WRITE_FAILURE');
  $id=90000+$count; $GLOBALS['wp_terms'][$id]=(object)['term_id'=>$id,'taxonomy'=>$tax,'slug'=>$args['slug'],'name'=>$args['name'],'parent'=>$args['parent'],'count'=>0];
  $GLOBALS['writes'][]=$id;return $id;
 }
 public static function target_tree_set_meta($ref,$type,$key,$value){update_term_meta($ref['id'],$key,$value);}
 public static function target_tree_delete_object($ref){$id=$ref['id'];if(!isset($GLOBALS['wp_terms'][$id]))throw new RuntimeException('MOCK_DELETE_INVALID');unset($GLOBALS['wp_terms'][$id],$GLOBALS['meta'][$id]);}
}
class APKW_FinalTargetAdmin {
 public static function frontend_readback($stage=null){$snap=$stage??APKW_TargetTreeSync::active_snapshot();$ids=[];foreach($snap['nodes'] as $node){if(!str_starts_with($node['node_id'],'core:c22:category:'))continue;
  $tid=$snap['mapping'][$node['node_id']]['object_id']??0;if(!$tid||!isset($GLOBALS['wp_terms'][$tid]))return ['valid'=>false,'errors'=>['TERM_MISSING']];$ids[$node['node_id']]=true;
 }return ['valid'=>count($ids)===1038,'errors'=>count($ids)===1038?[]:['WRONG_CAT_COUNT_'.count($ids)]];}
}
class APKW_FrontendStructure {public static function invalidate_cache(){} }
function add_action($k,$f){}
require APKW_DIR.'includes/class-apkw-c22-472-add-only.php';
$profile=json_decode(file_get_contents(APKW_DIR.'profiles/hab-und-bewahr-c22-plan.json'),true);
$nodes=[];$mapping=[];$nid=10000;
function id($kind,$key){return 'core:c22:'.$kind.':'.substr(hash('sha256',$key),0,20);}
foreach($profile['worlds'] as $w){
 foreach($w['areas'] as $a){
  $path=$w['name'].'|'.$a['name'];foreach($a['topics'] as $t){
   $key=$path.'|'.$t['name'];$tid=id('topic',$key);$wp=$nid++;$nodes[]=['node_id'=>$tid,'parent_id'=>id('area',$path),'display_name'=>$t['name'],'object_type'=>'page','slug'=>'old-topic'];$mapping[$tid]=['object_id'=>$wp,'object_type'=>'page'];
   $GLOBALS['wp_pages'][$wp]=(object)['ID'=>$wp,'post_type'=>'page','post_status'=>'publish'];
   foreach($t['categories'] as $c){$ckey=$key.'|'.$c['name'];$catId=id('category',$ckey);$cid=$nid++;
    $nodes[]=['node_id'=>$catId,'parent_id'=>$tid,'display_name'=>$c['name'],'object_type'=>'category','slug'=>'old-cat'];
    $mapping[$catId]=['object_id'=>$cid,'object_type'=>'category'];
    $GLOBALS['wp_terms'][$cid]=(object)['term_id'=>$cid,'name'=>$c['name'],'slug'=>'old-cat','taxonomy'=>'category','parent'=>0,'count'=>0];
   }
  }
 }
}
assert(count($nodes)===738);
for($i=0;$i<285;$i++){ $id='core:leaf:'.$i;$nodes[]=['node_id'=>$id,'parent_id'=>'legacy','display_name'=>'Historic','object_type'=>'category','slug'=>'legacy'];$mapping[$id]=['object_id'=>$nid++,'object_type'=>'category'];}
$base=['revision'=>'HB-TEST-BASE+C22-TEST','nodes'=>$nodes,'mapping'=>$mapping,'project'=>['c22_add_only_base_revision'=>'HB-TEST-BASE']];
update_option('apkw_target_tree_active_snapshot_v1',$base);update_option('apkw_target_tree_active_revision_v1',$base['revision']);
$manifest=APKW_C22_472_AddOnly::jobs();if(count($manifest)!==472)throw new Exception('INVALID_MANIFEST');
$dry=APKW_C22_472_AddOnly::dry_run();if(!$dry['valid']||$dry['writes']!==0)throw new Exception('DRY_RUN_FAILED');
$baseHash=hash('sha256',serialize($base));
update_option('apkw_c22_472_second_wave_base_v1',$base);
update_option('apkw_c22_472_second_wave_state_v1',['contract'=>'HB_C22_SECOND_WAVE_472_ADD_ONLY_V1','status'=>'WRITING','base_revision'=>$base['revision'],'base_sha256'=>$baseHash,'write_index'=>0,'mapping'=>[],'created'=>[],'error'=>'','total'=>472]);
for($i=0;$i<100;$i++){ $s=APKW_C22_472_AddOnly::run_batch();if(in_array($s['status'],['COMPLETE','ROLLED_BACK','ROLLBACK_FAILED'],true))break;}
if($s['status']!=='COMPLETE')throw new Exception('POSITIVE_472_RUN_FAILED: '.json_encode($s));
$after=APKW_TargetTreeSync::active_snapshot();if(count($after['nodes'])!==count($base['nodes'])+472||count($GLOBALS['writes'])!==472)throw new Exception('POSITIVE_CATEGORIES_INVALID');
foreach($base['nodes'] as $i=>$node)if($after['nodes'][$i]!==$node)throw new Exception('HISTORICAL_NODE_CHANGE');
if(!APKW_C22_472_AddOnly::completion_audit()['valid'])throw new Exception('COMPLETION_AUDIT_FALSE');
echo "PASS: 472/472 WP category INSERTS, same 738 original nodes and 285 legacy terms, 472 bound, 0 pages, completion PASS\n";
// Independent failure simulation from the original protected baseline (fail after 30 writes).
$GLOBALS['opt']=[];$GLOBALS['writes']=[];$GLOBALS['meta']=[];$GLOBALS['fail_after']=30;
foreach(array_keys($GLOBALS['wp_terms']) as $termid)if($termid>=90000)unset($GLOBALS['wp_terms'][$termid]);
update_option('apkw_target_tree_active_snapshot_v1',$base);update_option('apkw_target_tree_active_revision_v1',$base['revision']);
update_option('apkw_c22_472_second_wave_base_v1',$base);
update_option('apkw_c22_472_second_wave_state_v1',['contract'=>'HB_C22_SECOND_WAVE_472_ADD_ONLY_V1','status'=>'WRITING','base_revision'=>$base['revision'],'base_sha256'=>$baseHash,'write_index'=>0,'mapping'=>[],'created'=>[],'error'=>'','total'=>472]);
for($i=0;$i<100;$i++){ $s=APKW_C22_472_AddOnly::run_batch();if(in_array($s['status'],['COMPLETE','ROLLED_BACK','ROLLBACK_FAILED'],true))break;}
if($s['status']!=='ROLLED_BACK'||count($GLOBALS['writes'])!==30||count(array_filter(array_keys($GLOBALS['wp_terms']),fn($id)=>$id>=90000))!==0||APKW_TargetTreeSync::active_snapshot()!==$base)throw new Exception('NEGATIVE_ROLLBACK_FAILED: '.json_encode(['state'=>$s['status'],'old'=>APKW_TargetTreeSync::active_revision(),'left'=>count(array_filter(array_keys($GLOBALS['wp_terms']),fn($id)=>$id>=90000))]));
echo "PASS: INJECTED_FAILURE after 30 writes -> safe 30-term rollback, unchanged original snapshot, no historic deletion\n";
// Missing owner -> fail closed before creating anything.
$GLOBALS['fail_after']=null;delete_option('apkw_c22_472_second_wave_state_v1');delete_option('apkw_c22_472_second_wave_base_v1');
$broken=$base;unset($broken['mapping'][$manifest[0]['parent_id']]);update_option('apkw_target_tree_active_snapshot_v1',$broken);
try{APKW_C22_472_AddOnly::dry_run();throw new Exception('NEGATIVE_PARENT_NOT_BLOCKED');}catch(RuntimeException $e){if(!str_contains($e->getMessage(),'Snapshot')&&!str_contains($e->getMessage(),'Themenseite'))throw $e;}
echo "PASS: MISSING_PARENT mapping -> blocked before any write\n";
