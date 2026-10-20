<?php
/** Strict tests using unmodified original APKW_TargetWriter and real C2.4 manifest. */
declare(strict_types=1);
const ABSPATH='/';
define('APKW_DIR',__DIR__.'/test-base/affiliate-portal-kategorie-workflow/');
$GLOBALS['options']=[];$GLOBALS['posts']=[];$GLOBALS['terms']=[];$GLOBALS['seq']=100000;$GLOBALS['inject_at']=0;$GLOBALS['writes']=0;
function check(bool $c,string $s):void {if(!$c)throw new RuntimeException('FAIL '+$s);echo "PASS $s\n";}
function get_option($k,$default=false){return $GLOBALS['options'][$k]??$default;}
function update_option($k,$v,$x=null){$GLOBALS['options'][$k]=$v;return true;}
function delete_option($k){unset($GLOBALS['options'][$k]);return true;}
function add_option($k,$v,...$a){if(array_key_exists($k,$GLOBALS['options']))return false;$GLOBALS['options'][$k]=$v;return true;}
function add_action(...$x):void{}
function is_wp_error($x){return false;}
function get_post($id){return $GLOBALS['posts'][$id]??null;}
function get_term($id,$t){return $GLOBALS['terms'][$id]??null;}
function get_post_meta($id,$k,$single=true){return $GLOBALS['posts'][$id]->meta[$k]??'';}
function get_term_meta($id,$k,$single=true){return $GLOBALS['terms'][$id]->meta[$k]??'';}
function update_post_meta($id,$k,$v){$GLOBALS['posts'][$id]->meta[$k]=$v;return true;}
function update_term_meta($id,$k,$v){$GLOBALS['terms'][$id]->meta[$k]=$v;return true;}
function delete_post_meta($id,$k){unset($GLOBALS['posts'][$id]->meta[$k]);return true;}
function delete_term_meta($id,$k){unset($GLOBALS['terms'][$id]->meta[$k]);return true;}
function term_exists($name,$taxonomy,$parent=0){foreach($GLOBALS['terms'] as $t)if($t->name===$name&&$t->taxonomy===$taxonomy)return $t->term_id;return false;}
function get_term_by($field,$needle,$taxonomy){foreach($GLOBALS['terms'] as $t)if($t->$field===$needle&&$t->taxonomy===$taxonomy)return $t;return false;}
function get_posts($args){$out=[];foreach($GLOBALS['posts'] as $p){if($p->post_type!==($args['post_type']??'page'))continue;if(isset($args['name'])&&$p->post_name!==$args['name'])continue;if(isset($args['post_parent'])&&$p->post_parent!==$args['post_parent'])continue;$out[]=$p->ID;}return $out;}
function corrupt_at(int $step):void { $GLOBALS['inject_at']=$step;$GLOBALS['writes']=0; }
function write_event():void {$GLOBALS['writes']++;if($GLOBALS['inject_at']>0&&$GLOBALS['writes']===$GLOBALS['inject_at'])throw new RuntimeException('INJECTED WRITE FAILURE');}
function wp_insert_post($args,$error=true){write_event();$id=++$GLOBALS['seq'];$GLOBALS['posts'][$id]=(object)[
 'ID'=>$id,'post_type'=>$args['post_type'],'post_status'=>$args['post_status'],
 'post_name'=>$args['post_name'],'post_title'=>$args['post_title'],'post_parent'=>$args['post_parent'],
 'post_content'=>'','post_excerpt'=>'','meta'=>[]];return $id;}
function wp_update_post($args,$error=true){write_event();$id=(int)$args['ID'];if(!isset($GLOBALS['posts'][$id]))throw new RuntimeException('MISSING_POST');foreach($args as $k=>$v)if($k!=='ID')$GLOBALS['posts'][$id]->$k=$v;return $id;}
function wp_insert_term($name,$taxonomy,$args){write_event();$id=++$GLOBALS['seq'];$GLOBALS['terms'][$id]=(object)[
 'term_id'=>$id,'name'=>$name,'taxonomy'=>$taxonomy,'slug'=>$args['slug'],'parent'=>$args['parent'],'count'=>0,'meta'=>[]];return ['term_id'=>$id];}
function wp_update_term($id,$taxonomy,$args){write_event();if(!isset($GLOBALS['terms'][$id]))throw new RuntimeException('MISSING_TERM');foreach($args as $k=>$v)$GLOBALS['terms'][$id]->$k=$v;return ['term_id'=>$id];}
function wp_delete_post($id,$force=true){unset($GLOBALS['posts'][$id]);return true;}
function wp_delete_term($id,$taxonomy){unset($GLOBALS['terms'][$id]);return true;}
class APKW_TargetTreeSync {static function active_snapshot():array{return get_option('apkw_target_tree_active_snapshot_v1',[]);}static function active_revision():string{return get_option('apkw_target_tree_active_revision_v1','');}}
class APKW_FinalTargetAdmin {const PAGE_SLUG='apkw-final-target';static function frontend_readback(?array $s=null):array{$s=$s??APKW_TargetTreeSync::active_snapshot();$worlds=array_filter($s['nodes'],fn($n)=>str_starts_with($n['node_id'],'core:world:'));$ins=array_filter($s['nodes'],fn($n)=>!empty($n['insurance_seo_repair']));$count=(int)($s['settings']['expected_world_count']??0);$ok=$count===7&&count($worlds)===7&&count($ins)===190&&count($s['nodes'])===196&&count($s['mapping'])===196;return ['valid'=>$ok,'errors'=>$ok?[]:['COUNT_7_190_196_FAILED']];}}
class APKW_FrontendStructure {static function invalidate_cache():void{}}
require_once APKW_DIR.'includes/class-apkw-target-writer.php';
require_once APKW_DIR.'includes/class-apkw-insurance-94-add-only.php';
require_once APKW_DIR.'includes/class-apkw-insurance-seo-repair.php';
function seed():array{
 $GLOBALS['posts']=[];$GLOBALS['terms']=[];$GLOBALS['options']=[];$GLOBALS['seq']=100000;$GLOBALS['writes']=0;$GLOBALS['inject_at']=0;
 $nodes=[];$mapping=[];$ids=[];
 for($i=0;$i<6;$i++){
  $id='core:world:preserved-'.$i;$nodes[]=['node_id'=>$id,'object_type'=>'page','parent_id'=>'','display_name'=>'Altbestand '.$i,'slug'=>'bestandswelt-'.$i,'status'=>'active'];
  $pid=300+$i;$mapping[$id]=['object_id'=>$pid,'object_type'=>'page'];$GLOBALS['posts'][$pid]=(object)['ID'=>$pid,'post_type'=>'page','post_status'=>'publish','post_title'=>'Altbestand '.$i,'post_name'=>'bestandswelt-'.$i,'post_parent'=>0,'post_content'=>'Uralt unverändert','post_excerpt'=>'','meta'=>[]];
 }
 $jobs=APKW_Insurance_94_AddOnly::jobs();check(count($jobs)===94,'Originalversicherung genau 94 echte Profiljobs');
 foreach($jobs as $j){
  $id=++$GLOBALS['seq'];$ids[$j['key']]=$id;$pkey=$j['parent']??null;$par=$pkey===null?0:($ids[$pkey]??0);
  if($j['type']==='page')$GLOBALS['posts'][$id]=(object)[
    'ID'=>$id,'post_type'=>'page','post_status'=>'publish','post_title'=>$j['name'],'post_name'=>$j['slug'],'post_parent'=>$par,'post_content'=>'','post_excerpt'=>'','meta'=>['_apkw_target_node_id'=>$j['node_id'],'_apkw_concept_id'=>$j['node_id'],'_apkw_parent_concept_id'=>'','_apkw_target_revision'=>'R1+INS']];
  else $GLOBALS['terms'][$id]=(object)['term_id'=>$id,'name'=>$j['name'],'slug'=>$j['slug'],'taxonomy'=>'category','parent'=>0,'count'=>0,'meta'=>['_apkw_target_node_id'=>$j['node_id'],'_apkw_concept_id'=>$j['node_id'],'_apkw_parent_concept_id'=>'','_apkw_target_revision'=>'R1+INS']];
  $nodes[]=['node_id'=>$j['node_id'],'parent_id'=>$pkey===null?'':$jobs[array_search($pkey,array_column($jobs,'key'),true)]['node_id'],
    'display_name'=>$j['name'],'slug'=>$j['slug'],'status'=>'active','object_type'=>$j['type'],'insurance_add_only'=>true];
  $mapping[$j['node_id']]=['object_id'=>$id,'object_type'=>$j['type']];
 }
 $snap=['revision'=>'BASE-INS-94','settings'=>['expected_world_count'=>7],
  'nodes'=>$nodes,'mapping'=>$mapping,'project'=>['header_navigation'=>['roots'=>[]]]];
 update_option('apkw_target_tree_active_snapshot_v1',$snap);update_option('apkw_target_tree_active_revision_v1','BASE-INS-94');update_option('apkw_ins_94_state_v1',['status'=>'COMPLETE']);
 return $snap;
}
function begin(array $p):void{
 update_option('apkw_ins_seo_repair_backup_v1',['snap'=>$p['snapshot'],'old_objects'=>$p['old_objects']]);
 update_option('apkw_ins_seo_repair_state_v1',['status'=>'WRITING','base_revision'=>$p['old_revision'],'base_sha256'=>hash('sha256',serialize($p['snapshot'])),
 'jobs'=>$p['jobs'],'i'=>0,'new_mapping'=>[],'created'=>[],'error'=>'']);
}
function batches():array{for($i=0;$i<80;$i++){$s=APKW_Insurance_SEO_Repair::batch();if(in_array($s['status']??'',['COMPLETE','ROLLED_BACK','BLOCKED'],true))return $s;}throw new RuntimeException('Batch did not finish: '.$s['status']);}
$base=seed();$fingerprint=hash('sha256',serialize([$GLOBALS['posts'], $GLOBALS['terms']]));
$pass=APKW_Insurance_SEO_Repair::dry_run();check($pass['valid']&&$pass['writes']===0&&$pass['additional_pages']===26&&$pass['additional_terms']===70,'Real 94er bestandsgebundener read-only Preflight');
check(hash('sha256',serialize([$GLOBALS['posts'],$GLOBALS['terms']]))===$fingerprint,'Preflight physisch 0 Writes');
$id=array_key_first($GLOBALS['terms']);$GLOBALS['terms'][$id]->count=1;
try{APKW_Insurance_SEO_Repair::dry_run();throw new RuntimeException('Term assignment was not detected');}catch(RuntimeException $e){check(str_contains($e->getMessage(),'Kategorie hat Inhalte'),'Negative: befüllte Kategorie sperrt Migration');}
$GLOBALS['terms'][$id]->count=0;
$id=100006;$GLOBALS['posts'][$id]->post_content='Individuell hinzugefügt';
try{APKW_Insurance_SEO_Repair::dry_run();throw new RuntimeException('Page content was not detected');}catch(RuntimeException $e){check(str_contains($e->getMessage(),'Seite inzwischen bearbeitet'),'Negative: bearbeitete Versicherungsseite sperrt Migration');}
$GLOBALS['posts'][$id]->post_content='';
$foreign=105000;$GLOBALS['posts'][$foreign]=(object)['ID'=>$foreign,'post_type'=>'page','post_status'=>'publish','post_title'=>'Fremd','post_name'=>'hausratversicherung','post_parent'=>0,'post_content'=>'Belegt','post_excerpt'=>'','meta'=>[]];
try{APKW_Insurance_SEO_Repair::dry_run();throw new RuntimeException('Slug collision was not detected');}catch(RuntimeException $e){check(str_contains($e->getMessage(),'Seitenslug fremd'),'Negative: fremder WP-Seitenslug blockiert');}
unset($GLOBALS['posts'][$foreign]);
$p=APKW_Insurance_SEO_Repair::preflight();begin($p);$result=batches();
check($result['status']==='COMPLETE','Positive: echtes Originalwriter-API, kompletter 190er SEO-Korrekturlauf');
check(count($GLOBALS['posts'])===6+52&&count($GLOBALS['terms'])===138,'Physisch 52 WordPress-Seiten + 138 flache Terms plus 6 Altwelt-Seiten');
for($i=0;$i<6;$i++)check($GLOBALS['posts'][300+$i]->post_content==='Uralt unverändert','Alte Welt '.$i.' unberührt');
check(count(array_filter(APKW_TargetTreeSync::active_snapshot()['nodes'],fn($n)=>!empty($n['insurance_seo_repair'])))===190,'Neuer aktiver SEO-Snapshot 190 Objekte');
$metaBad=0;foreach(APKW_TargetTreeSync::active_snapshot()['nodes'] as $node){if(empty($node['insurance_seo_repair']))continue;$id=(int)APKW_TargetTreeSync::active_snapshot()['mapping'][$node['node_id']]['object_id'];$m=$node['object_type']==='category'?get_term_meta($id,'_apkw_target_active',true):get_post_meta($id,'_apkw_target_active',true);$pillar=$node['object_type']==='category'?get_term_meta($id,'_apkw_target_pillar',true):get_post_meta($id,'_apkw_target_pillar',true);if($m!=='1'||$pillar!=='core')$metaBad++;}check($metaBad===0,'Alle 190 Versicherungsobjekte mit echten Original-Metadaten');
seed();$base=APKW_TargetTreeSync::active_snapshot();$p=APKW_Insurance_SEO_Repair::preflight();begin($p);
corrupt_at(74);$result=batches();
check($result['status']==='ROLLED_BACK','Negative: erzwungener Originalwriter-Ausfall rollt zurück');
check(count($GLOBALS['posts'])===6+26&&count($GLOBALS['terms'])===68,'Rollback: ursprüngliche 94 Versicherungsobjekte genau wiederhergestellt');
check(APKW_TargetTreeSync::active_revision()==='BASE-INS-94','Rollback: ursprünglicher Snapshot/Revision unverändert');
check($GLOBALS['posts'][300]->post_content==='Uralt unverändert','Rollback: älteste Welt völlig unberührt');
echo "ALL KEYWORD REPAIR REAL SOURCE + REAL ORIGINAL TARGET WRITER TESTS PASS\n";
