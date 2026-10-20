<?php
/** PHP 8.4, original unmodified APKW_TargetWriter + actual 1.14.8.36 profile. */
error_reporting(E_ALL);
ini_set('display_errors','1');
define('ABSPATH','/mock-wp/');
define('APKW_DIR',dirname(__DIR__).'/affiliate-portal-kategorie-workflow/');
$scenario=$argv[1]??'success';
$GLOBALS['db']=['options'=>[],'terms'=>[],'posts'=>[],'termmeta'=>[],'postmeta'=>[],'write_count'=>0,'insert_count'=>0,'fail_insert'=>0,'fail_stage'=>false,'readback'=>0,'snap_base'=>[]];
class WP_Error {}function is_wp_error($x):bool{return $x instanceof WP_Error;}
function add_action($name,$fn,$priority=10):void{}
function add_submenu_page(...$args):void{}
function get_option($key,$def=null){return $GLOBALS['db']['options'][$key]??$def;}
function update_option($key,$val,$a=false):bool{$GLOBALS['db']['options'][$key]=$val;$GLOBALS['db']['write_count']++;return true;}
function delete_option($key):bool{unset($GLOBALS['db']['options'][$key]);return true;}
function add_option($key,$val,$a='',$autoload='no'):bool{if(array_key_exists($key,$GLOBALS['db']['options']))return false;$GLOBALS['db']['options'][$key]=$val;return true;}
function get_post($id){return $GLOBALS['db']['posts'][$id]??null;}
function get_post_meta($id,$k,$single=true):string{return (string)($GLOBALS['db']['postmeta'][$id][$k]??'');}
function get_term_meta($id,$k,$single=true):string{return (string)($GLOBALS['db']['termmeta'][$id][$k]??'');}
function update_post_meta($id,$key,$val):bool{$GLOBALS['db']['postmeta'][$id][$key]=(string)$val;return true;}
function update_term_meta($id,$key,$val):bool{$GLOBALS['db']['termmeta'][$id][$key]=(string)$val;return true;}
function delete_post_meta($id,$key):bool{unset($GLOBALS['db']['postmeta'][$id][$key]);return true;}
function delete_term_meta($id,$key):bool{unset($GLOBALS['db']['termmeta'][$id][$key]);return true;}
function get_term($id,$taxonomy){return $GLOBALS['db']['terms'][$id]??null;}
function get_term_by($field,$value,$taxonomy){foreach($GLOBALS['db']['terms'] as $t)if((string)$t->$field===$value)return $t;return false;}
function term_exists($name,$taxonomy,$parent=0){foreach($GLOBALS['db']['terms'] as $t)if($t->name===$name&&$t->parent===$parent)return ['term_id'=>$t->term_id];return null;}
function wp_insert_term($name,$taxonomy,$args){$GLOBALS['db']['insert_count']++;if($GLOBALS['db']['fail_insert']&&$GLOBALS['db']['insert_count']===$GLOBALS['db']['fail_insert'])return new WP_Error;
 $id=12000+count($GLOBALS['db']['terms']);$GLOBALS['db']['terms'][$id]=(object)['term_id'=>$id,'taxonomy'=>'category','name'=>$name,'slug'=>$args['slug'],'parent'=>0,'count'=>0];return ['term_id'=>$id];}
function wp_delete_term($id,$tax){unset($GLOBALS['db']['terms'][$id],$GLOBALS['db']['termmeta'][$id]);return true;}
function wp_insert_post($args,$wpError=false){return 10001;}function wp_update_post($args,$wpError=false){return $args['ID']??1;}
function wp_update_term($id,$tax,$args){return ['term_id'=>$id];}function wp_delete_post($id,$force=false){return true;}
function current_user_can($permission):bool{return true;}function check_admin_referer($n){}function check_ajax_referer($n,$key){}
function admin_url($s):string{return 'http://mock.local/'.$s;}function esc_html($x){return htmlspecialchars((string)$x);}function esc_url($x){return $x;}function wp_create_nonce($x):string{return 'fake';}function wp_nonce_field($x){}
function wp_json_encode($x):string{return json_encode($x);}function wp_send_json_success($x){return $x;}function wp_send_json_error($x,$code=409){return $x;}function wp_safe_redirect($to){}
function wp_die($message,$title='',$args=[]){throw new RuntimeException($message);}
class APKW_TargetTreeSync {public static function active_snapshot():array{return get_option('apkw_target_tree_active_snapshot_v1',[]);}public static function active_revision():string{return (string)get_option('apkw_target_tree_active_revision_v1','');}}
class APKW_Insurance_SEO_Repair {public static function state():array{return get_option('apkw_ins_seo_repair_state_v1',[]);}}
class APKW_FrontendStructure {public static $invalidations=0;public static function invalidate_cache(){self::$invalidations++;}}
class APKW_FinalTargetAdmin {public const PAGE_SLUG='apkw-final-target';public static function frontend_readback(?array $snap=null):array{
 $GLOBALS['db']['readback']++;
 if($GLOBALS['db']['fail_stage']&&$snap!==null)return ['valid'=>false,'errors'=>['SIMULATED_FRONTEND_STAGE_FAILURE']];
 $snap=$snap??APKW_TargetTreeSync::active_snapshot();
 $n=0;foreach($snap['nodes'] as $e)if(($e['insurance_c26_depth']??false)===true){$n++;$nid=$e['node_id'];$tid=$snap['mapping'][$nid]['object_id']??0;
 if(!is_object(get_term($tid,'category'))||get_term_meta($tid,'_apkw_target_node_id',true)!==$nid||get_term_meta($tid,'_apkw_parent_concept_id',true)!==$e['parent_id'])return ['valid'=>false,'errors'=>['TERM_META_FAIL']];}
 return ['valid'=>$n===185,'errors'=>$n===185?[]:['WRONG_NEW_TERM_COUNT']];}}
require APKW_DIR.'includes/class-apkw-target-writer.php';
require APKW_DIR.'includes/class-apkw-insurance-c26-depth.php';
$seo=json_decode(file_get_contents(APKW_DIR.'profiles/hab-und-bewahr-insurance-seo-repair.json'),true);
// Build exactly same node IDs and mapping fields as real C2.5 active snapshot, and 6 protected worlds.
$nodes=[];$mapping=[];$pageByKey=[];$r3=[];
for($i=1;$i<=6;$i++){ $node='core:world:old-'.$i;
 $nodes[]=['node_id'=>$node,'parent_id'=>'','status'=>'active','display_name'=>'OLD WORLD '.$i,'object_type'=>'page','pillar'=>'core'];$mapping[$node]=['object_id'=>$i,'object_type'=>'page'];
 $GLOBALS['db']['posts'][$i]=(object)['ID'=>$i,'post_type'=>'page','post_status'=>'publish','post_name'=>'old-'.$i,'post_title'=>'OLD WORLD '.$i,'post_parent'=>0];}
foreach($seo['pages'] as $p){
 $id=100+count($pageByKey);$pageByKey[$p['key']]=$id;
 $node=match($p['level']){'R1'=>'core:world:insurance','R2'=>'core:area:insurance:'.$p['slug'],'R3'=>'core:subarea:insurance:'.$p['slug']};
 $parentNode= $p['level']==='R1'?'':(str_starts_with($p['parent'],'INS-SEO:R2:')?'core:area:insurance:'.substr($p['parent'],strlen('INS-SEO:R2:')):'core:world:insurance');
 $nodes[]=['node_id'=>$node,'parent_id'=>$parentNode,'status'=>'active','display_name'=>$p['title'],'slug'=>$p['slug'],'object_type'=>'page','pillar'=>'core','insurance_seo_repair'=>true];
 $mapping[$node]=['object_id'=>$id,'object_type'=>'page'];
 $GLOBALS['db']['posts'][$id]=(object)['ID'=>$id,'post_type'=>'page','post_status'=>'publish','post_name'=>$p['slug'],'post_title'=>$p['title'],'post_parent'=>($p['parent']?($pageByKey[$p['parent']]??0):0)];
 $GLOBALS['db']['postmeta'][$id]['_apkw_target_node_id']=$node;
 if($p['level']==='R3')$r3[$p['key']]=$node;
}
foreach($seo['flat_categories'] as $c){
 $nid='core:leaf:insurance:'.$c['slug'];$id=1000+count($GLOBALS['db']['terms']);
 $nodes[]=['node_id'=>$nid,'parent_id'=>$r3[$c['parent']],'status'=>'active','display_name'=>$c['name'],'slug'=>$c['slug'],'object_type'=>'category','pillar'=>'core','insurance_seo_repair'=>true];
 $mapping[$nid]=['object_id'=>$id,'object_type'=>'category','taxonomy'=>'category'];
 $GLOBALS['db']['terms'][$id]=(object)['term_id'=>$id,'taxonomy'=>'category','name'=>$c['name'],'slug'=>$c['slug'],'parent'=>0,'count'=>0];
 $GLOBALS['db']['termmeta'][$id]['_apkw_target_node_id']=$nid;
}
$base=['revision'=>'BASE-WP+INS-SEO-REFERENCE','settings'=>['expected_world_count'=>7],
 'project'=>['header_navigation'=>['roots'=>[]]],'nodes'=>$nodes,'mapping'=>$mapping];
$GLOBALS['db']['snap_base']=$base;
update_option('apkw_target_tree_active_snapshot_v1',$base);update_option('apkw_target_tree_active_revision_v1',$base['revision']);
update_option('apkw_ins_seo_repair_state_v1',['status'=>'COMPLETE']);
function verify($ok,$what){if(!$ok)throw new RuntimeException('ASSERTION FAILED: '.$what);}
function blocked($what,callable $cb){try{$cb();throw new RuntimeException('SHOULD BLOCK BUT DID NOT: '.$what);}catch(RuntimeException $e){if(str_starts_with($e->getMessage(),'SHOULD BLOCK'))throw $e;echo 'NEGATIVE PASS: '.$what.' ['.$e->getMessage()."]\n";}}
function raw_fingerprint($db){return hash('sha256',serialize([$db['posts'],$db['postmeta']]));}
$beforePages=raw_fingerprint($GLOBALS['db']);
$beforeTerms=$GLOBALS['db']['terms'];$beforeTermMeta=$GLOBALS['db']['termmeta'];$beforeNodes=$base['nodes'];$beforeMapping=$base['mapping'];
if($scenario==='missing_status'){
 update_option('apkw_ins_seo_repair_state_v1',['status'=>'WRITING']);blocked('C2.5 incomplete',fn()=>APKW_Insurance_C26_Depth::preflight());exit;
}
if($scenario==='missing_owner'){
 unset($GLOBALS['db']['postmeta'][106]);blocked('missing owner identity',fn()=>APKW_Insurance_C26_Depth::preflight());exit;
}
if($scenario==='collision'){
 $GLOBALS['db']['terms'][11150]=(object)['term_id'=>11150,'taxonomy'=>'category','name'=>'FOREIGN','slug'=>'vs-hausratversicherung-versicherungssumme-und-unterversicherung','parent'=>0,'count'=>0];
 blocked('occupied foreign term slug',fn()=>APKW_Insurance_C26_Depth::preflight());exit;
}
if($scenario==='stale_revision'){
 update_option('apkw_target_tree_active_revision_v1','OTHER-REV');blocked('changed live revision',fn()=>APKW_Insurance_C26_Depth::preflight());exit;
}
$start=APKW_Insurance_C26_Depth::dry_run();verify($start['valid']&&$start['writes']===0&&$start['new_terms']===185&&$start['new_pages']===0,'read-only preflight');
verify(count($GLOBALS['db']['terms'])===138,'no WP writes in preflight');
echo "PREFLIGHT PASS 185 new, 0 writes, 46 R3 preserved\n";
if($scenario==='insert_failure')$GLOBALS['db']['fail_insert']=37;
if($scenario==='stage_failure')$GLOBALS['db']['fail_stage']=true;
// Mimic explicit approval by setting import state as start() does after successful preflight, without PHP exit/HTTP redirect.
// preflight returns all jobs and snapshot and must run before creating backup.
$p=APKW_Insurance_C26_Depth::preflight();
update_option('apkw_ins_c26_depth_base_v1',$p['snapshot']);
update_option('apkw_ins_c26_depth_state_v1',['status'=>'WRITING','base_revision'=>$p['revision'],'base_sha'=>hash('sha256',serialize($p['snapshot'])),
'jobs'=>$p['jobs'],'i'=>0,'new_mapping'=>[],'created'=>[],'error'=>'']);
$rounds=0;
do{$state=APKW_Insurance_C26_Depth::batch();$rounds++;if($rounds>60)throw new RuntimeException('Infinite loop state: '.$state['status']);}while(in_array($state['status'],['WRITING','VERIFY','ROLLBACK'],true));
if(in_array($scenario,['insert_failure','stage_failure'],true)){
 verify($state['status']==='ROLLED_BACK','rollback when deliberately failing');
 verify(count($GLOBALS['db']['terms'])===138,'none of 185 novel terms survive rollback');
 verify($GLOBALS['db']['terms']===$beforeTerms&&$GLOBALS['db']['termmeta']===$beforeTermMeta,'original 138 terms/meta unchanged');
 verify(raw_fingerprint($GLOBALS['db'])===$beforePages,'no old page write');
 verify(APKW_TargetTreeSync::active_snapshot()===$base,'original active snapshot/restoration');
 echo 'ROLLBACK PASS: '.$scenario.' / '.$rounds." rounds.\n";exit;
}
verify($state['status']==='COMPLETE','import fully complete');
verify(count($GLOBALS['db']['terms'])===323,'323 total insurance categories');
verify(raw_fingerprint($GLOBALS['db'])===$beforePages,'six old worlds and 46 R3 identical');
foreach($beforeTerms as $id=>$v){verify($GLOBALS['db']['terms'][$id]===$v,'old category changed '.$id);verify($GLOBALS['db']['termmeta'][$id]===$beforeTermMeta[$id],'old category meta changed '.$id);}
$final=APKW_TargetTreeSync::active_snapshot();verify(count($final['nodes'])===count($base['nodes'])+185,'185 new nodes only');
foreach($beforeNodes as $idx=>$v)verify($final['nodes'][$idx]===$v,'original node touched '.$idx);
foreach($beforeMapping as $id=>$v)verify($final['mapping'][$id]===$v,'original mapping touched '.$id);
verify(APKW_FrontendStructure::$invalidations===1,'frontend cache invalidation');
blocked('repeated import forbidden',fn()=>APKW_Insurance_C26_Depth::preflight());
echo 'FULL PASS: new 185/185, total 323, preserved old pages, 138 old terms and 6 worlds; batches '.$rounds.'; local stage & active readback pass' ."\n";
