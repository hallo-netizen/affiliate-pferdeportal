<?php
error_reporting(E_ALL);define('ABSPATH','/tmp/');define('APKW_DIR','/mnt/data/hb_c23_work/affiliate-portal-kategorie-workflow/');
$GLOBALS['opt']=[];$GLOBALS['wp_terms']=[];$GLOBALS['wp_pages']=[];$GLOBALS['meta']=[];$GLOBALS['writes']=[];$GLOBALS['fail_after']=null;
function get_option($k,$v=null){return $GLOBALS['opt'][$k]??$v;}
function update_option($k,$v,$autoload=false){$GLOBALS['opt'][$k]=$v;return true;}
function delete_option($k){unset($GLOBALS['opt'][$k]);}
function add_option($k,$v,$d='',$autoload='no'){if(isset($GLOBALS['opt'][$k]))return false;$GLOBALS['opt'][$k]=$v;return true;}
function sanitize_title($s){$t=iconv('UTF-8','ASCII//TRANSLIT//IGNORE',$s);return trim(preg_replace('/[^a-z0-9]+/','-',strtolower($t)),'-');}
class WP_Error{}function is_wp_error($x){return $x instanceof WP_Error;}
function get_terms($arg){return array_values(array_filter($GLOBALS['wp_terms'],fn($t)=>in_array($t->slug,$arg['slug']??[],true)));}
function get_post($id){return $GLOBALS['wp_pages'][$id]??null;}
function get_term($id,$tax){return $GLOBALS['wp_terms'][$id]??null;}
function get_term_link($id,$tax){return isset($GLOBALS['wp_terms'][$id])?'https://hab-und-bewahr.de/category/'.$GLOBALS['wp_terms'][$id]->slug.'/':new WP_Error();}
function get_term_meta($id,$key,$single=true){return $GLOBALS['meta'][$id][$key]??'';}
function update_term_meta($id,$key,$val){$GLOBALS['meta'][$id][$key]=$val;return true;}
function delete_term_meta($id,$key){unset($GLOBALS['meta'][$id][$key]);}
function wp_specialchars_decode($s,$mode){return html_entity_decode($s,$mode|ENT_HTML5,'UTF-8');}
function add_action($x,$f){}
class APKW_TargetTreeSync{
 static function active_snapshot(){return get_option('apkw_target_tree_active_snapshot_v1',[]);}
 static function active_revision(){return get_option('apkw_target_tree_active_revision_v1','');}
 static function state(){return ['status'=>'COMPLETE'];}
}
class APKW_C22_Fachpruefung{
 static function plan(){return json_decode(file_get_contents(APKW_DIR.'profiles/hab-und-bewahr-c22-plan.json'),true);}
 static function audit($p,$live){return ['valid'=>true,'counts'=>['topic_pages'=>172,'article_categories'=>566]];}
}
class APKW_TargetWriter{
 static function target_tree_insert_term($tax,$args){$n=count($GLOBALS['writes']);if($GLOBALS['fail_after']!==null&&$n >= $GLOBALS['fail_after'])throw new RuntimeException('INJECTED_FAILURE');$id=99000+$n;$GLOBALS['wp_terms'][$id]=(object)['term_id'=>$id,'taxonomy'=>$tax,'slug'=>$args['slug'],'name'=>$args['name'],'parent'=>0,'count'=>0];$GLOBALS['writes'][]=$id;return $id;}
 static function target_tree_set_meta($r,$type,$k,$v){update_term_meta($r['id'],$k,$v);}
 static function target_tree_delete_object($r){$id=$r['id'];if(!isset($GLOBALS['wp_terms'][$id]))throw new RuntimeException('DELETE_INVALID');unset($GLOBALS['wp_terms'][$id],$GLOBALS['meta'][$id]);}
}
class APKW_FinalTargetAdmin{
 static function frontend_readback($snap=null){$x=$snap??APKW_TargetTreeSync::active_snapshot();$count=0;foreach($x['nodes'] as $n){if(!str_starts_with($n['node_id'],'core:c22:category:'))continue;$id=$x['mapping'][$n['node_id']]['object_id']??0;if(!$id||!isset($GLOBALS['wp_terms'][$id]))return ['valid'=>false,'errors'=>['MISSING_WP_TERM']];$count++;}return ['valid'=>$count===1038,'errors'=>$count===1038?[]:['BAD_'.$count]];}
}
class APKW_TargetTree { static function managed_block($x){return 'content';}}
function get_post_meta($id,$key,$single=true){return $GLOBALS['postmeta'][$id][$key]??'';}
function get_permalink($id){return 'https://hab-und-bewahr.de/topic/'.$id.'/';}
function esc_html($x){return htmlspecialchars((string)$x,ENT_QUOTES,'UTF-8');}
function esc_url($x){return htmlspecialchars((string)$x,ENT_QUOTES,'UTF-8');}
function esc_attr($x){return htmlspecialchars((string)$x,ENT_QUOTES,'UTF-8');}
require APKW_DIR.'includes/class-apkw-frontend-structure.php';
require APKW_DIR.'includes/class-apkw-c22-add-only.php';require APKW_DIR.'includes/class-apkw-c22-472-add-only.php';require APKW_DIR.'includes/class-apkw-c23-471-add-only.php';
// Real original importer job list, genuine SHA-based IDs and expected original node shape.
$old=[];$mapping=[];$wpId=1200;
$v3=json_decode(file_get_contents('/mnt/data/HAB_UND_BEWAHR_C22_EINHEITLICHER_FACHSTAND_V3.json'),true);
$legacyOwners=[];foreach($v3['legacy_285_term_protection'] as $term){$legacyOwners[(int)$term['existing_wp_page3_id']]=$term['existing_wp_page3_name'];}
foreach($legacyOwners as $physical=>$label){$key='core:subarea:historic-'.$physical;
 $old[]=['node_id'=>$key,'parent_id'=>'core:area:old','object_type'=>'page','display_name'=>$label,'slug'=>'historic-page-'.$physical,'pillar'=>'core','status'=>'active'];
 $mapping[$key]=['object_id'=>$physical,'object_type'=>'page'];
 $GLOBALS['wp_pages'][$physical]=(object)['ID'=>$physical,'post_type'=>'page','post_status'=>'publish'];
 $GLOBALS['postmeta'][$physical]['_apkw_target_node_id']=$key;
}
foreach($v3['legacy_285_term_protection'] as $v){$id=(int)$v['existing_wp_category_term_id'];$key='core:leaf:historic-'.$id;$owner='core:subarea:historic-'.(int)$v['existing_wp_page3_id'];
 $old[]=['node_id'=>$key,'parent_id'=>$owner,'object_type'=>'category','display_name'=>$v['existing_wp_category_name'],'slug'=>$v['existing_wp_category_slug'],'pillar'=>'core','status'=>'active'];
 $mapping[$key]=['object_id'=>$id,'object_type'=>'category'];
 $GLOBALS['wp_terms'][$id]=(object)['term_id'=>$id,'taxonomy'=>'category','slug'=>$v['existing_wp_category_slug'],'name'=>$v['existing_wp_category_name'],'parent'=>0,'count'=>0];
}
$oldSnapshot=['revision'=>'R0','nodes'=>$old,'mapping'=>$mapping,'project'=>['c22_add_only_base_revision'=>'R0'],'settings'=>['expected_world_count'=>6,'max_megamenu_children'=>5]];
$originalJobs=APKW_C22_AddOnly::jobs();if(count($originalJobs)!==743)throw new Exception('WRONG_ORIGINAL_JOBS');
$active=$oldSnapshot;
foreach($originalJobs as $job){$id=$wpId++;$active['nodes'][]=['node_id'=>$job['node_id'],'parent_id'=>$job['parent_id'],'display_name'=>$job['name'],'slug'=>$job['slug'],'object_type'=>$job['type'],'pillar'=>'core','status'=>'active'];$active['mapping'][$job['node_id']]=['object_id'=>$id,'object_type'=>$job['type']];if($job['type']==='page'){$GLOBALS['wp_pages'][$id]=(object)['ID'=>$id,'post_type'=>'page','post_status'=>'publish'];$GLOBALS['postmeta'][$id]['_apkw_target_node_id']=$job['node_id'];}else $GLOBALS['wp_terms'][$id]=(object)['term_id'=>$id,'slug'=>$job['slug'],'name'=>$job['name'],'parent'=>0,'count'=>0,'taxonomy'=>'category'];}
$plan=APKW_C22_Fachpruefung::plan();$digest=$plan['live_binding']['site_mapping_sha256'];$expected='R0+C22-'.substr($plan['integrity']['manifest_sha256_utf8'],0,16);$active['revision']=$expected;$active['project']['c22_add_only_base_revision']='R0';
update_option('apkw_c22_base_snapshot_backup_v1',$oldSnapshot);
update_option('apkw_c22_add_only_state_v1',['status'=>'COMPLETE','base_revision'=>'R0','base_digest'=>$digest,'base_snapshot_sha256'=>hash('sha256',serialize($oldSnapshot)),'result'=>['readback'=>'PASS','old_post_term_links_unchanged'=>4]]);
update_option('apkw_target_tree_active_snapshot_v1',$active);update_option('apkw_target_tree_active_revision_v1',$expected);
$originalAudit=APKW_C22_AddOnly::completion_audit();if(!$originalAudit['valid'])throw new Exception('ORIGINAL_C22_AUDIT_FAILED '.json_encode($originalAudit));
$dry=APKW_C22_472_AddOnly::dry_run();if(!$dry['valid']||$dry['writes']!==0)throw new Exception('DRY_RUN_FAILED');
update_option('apkw_c22_472_second_wave_base_v1',$active);
update_option('apkw_c22_472_second_wave_state_v1',['contract'=>'HB_C22_SECOND_WAVE_472_ADD_ONLY_V1','status'=>'WRITING','base_revision'=>$expected,'base_sha256'=>hash('sha256',serialize($active)),'write_index'=>0,'mapping'=>[],'created'=>[],'error'=>'','total'=>472]);
for($i=0;$i<100;$i++){$s=APKW_C22_472_AddOnly::run_batch();if(in_array($s['status'],['COMPLETE','ROLLED_BACK','ROLLBACK_FAILED'],true))break;}
if($s['status']!=='COMPLETE')throw new Exception('SECOND_WAVE_FAILED '.json_encode(['status'=>$s['status'],'error'=>$s['error']??'']));
$oldAfter=APKW_C22_AddOnly::completion_audit();$extra=APKW_C22_472_AddOnly::completion_audit();
if(!$oldAfter['valid']||!$extra['valid'])throw new Exception('INTEGRATED_AUDIT_FAILED '.json_encode([$oldAfter,$extra]));
if(count(APKW_TargetTreeSync::active_snapshot()['nodes'])!==count($old)+743+472)throw new Exception('SNAPSHOT_COUNT');
echo "PASS real original C2.2 audit before AND after second-wave completion; 743 + 472 + protected 378; exact names and parents; 0 old writes\n";

// Render REAL frontend PHP for all 172 topic pages, not a mocked approximation.
$pages=0;$found=0;$missing=[];$after=APKW_TargetTreeSync::active_snapshot();
foreach($originalJobs as $job)if(str_starts_with($job['node_id'],'core:c22:topic:')){
  $id=(int)$after['mapping'][$job['node_id']]['object_id'];$html=APKW_FrontendStructure::render_page_structure($id);$pages++;
  foreach(APKW_C22_472_AddOnly::jobs() as $new)if($new['parent_id']===$job['node_id']){
    $label=htmlspecialchars($new['name'],ENT_QUOTES,'UTF-8');
    if(strpos($html,'>'.$label.'</a>')===false)$missing[]=$job['name'].' > '.$new['name'];else $found++;
  }
}
if($pages!==172||$found!==472||$missing)throw new Exception('REAL_FRONTEND_RENDERER_FAILED '.json_encode(['pages'=>$pages,'found'=>$found,'miss'=>array_slice($missing,0,5)]));
echo "PASS real original FrontendStructure::render_page_structure: all 472 new categories linked across 172 pages, no new page level\n";

$third=APKW_C23_471_AddOnly::dry_run();if(empty($third['valid'])||$third['writes']!==0)throw new Exception('THIRD_PREFLIGHT_FAIL');
$before3=APKW_TargetTreeSync::active_snapshot();$rev3=APKW_TargetTreeSync::active_revision();
$permit=APKW_C23_471_AddOnly::preflight();
update_option('apkw_c23_471_add_backup_v1',$before3);
update_option('apkw_c23_471_add_state_v1',['contract'=>'HB_C23_THIRD_WAVE_471_ADD_ONLY_V1','status'=>'WRITING',
 'base_revision'=>$rev3,'base_sha256'=>hash('sha256',serialize($before3)),
 'owner_node_ids'=>$permit['owner_ids'],'write_index'=>0,'mapping'=>[],'created'=>[],'error'=>'','total'=>471]);
for($i=0;$i<100;$i++){$s=APKW_C23_471_AddOnly::run_batch();if(in_array($s['status'],['COMPLETE','ROLLED_BACK','ROLLBACK_FAILED'],true))break;}
if($s['status']!=='COMPLETE')throw new Exception('THIRD_WAVE_FAILED '.json_encode(['status'=>$s['status'],'error'=>$s['error']??'']));
$a=APKW_C22_AddOnly::completion_audit();$b=APKW_C22_472_AddOnly::completion_audit();$c=APKW_C23_471_AddOnly::completion_audit();
if(!$a['valid']||!$b['valid']||!$c['valid'])throw new Exception('ALL_THREE_ORIGINAL_AUDITS_FAILED '.json_encode([$a,$b,$c]));
$last=APKW_TargetTreeSync::active_snapshot();foreach($before3['nodes'] as $i=>$n)if($last['nodes'][$i]!==$n)throw new Exception('OLD_NODE_TAMPERED');
foreach($before3['mapping'] as $id=>$m)if($last['mapping'][$id]!==$m)throw new Exception('OLD_MAPPING_TAMPERED');
if(count($last['nodes'])!==count($before3['nodes'])+471)throw new Exception('THIRD_COUNT_MISMATCH');
echo "PASS original C22 743 audit + second 472 audit + third 471 audit after third wave; 0 original nodes or mappings modified\n";
$matched=0;$owners=[];$bad=[];
foreach(APKW_C23_471_AddOnly::jobs() as $j){
 $owner=$s['owner_node_ids'][$j['owner_key']];$id=$last['mapping'][$owner]['object_id'];$owners[$id]=true;
 $html=APKW_FrontendStructure::render_page_structure($id);
 $label=htmlspecialchars($j['name'],ENT_QUOTES,'UTF-8');
 if(strpos($html,'>'.$label.'</a>')===false)$bad[]=$j['owner_key'].'::'.$j['name'];else $matched++;
}
if($matched!==471||count($owners)!==220||$bad)throw new Exception('REAL_FRONTEND_C23_FAILED '.json_encode(['seen'=>$matched,'owners'=>count($owners),'missing'=>array_slice($bad,0,5)],JSON_UNESCAPED_UNICODE));
echo "PASS real APKW_FrontendStructure renders all 471 new categories across 220 old/new owners; 0 forced new pages\n";
