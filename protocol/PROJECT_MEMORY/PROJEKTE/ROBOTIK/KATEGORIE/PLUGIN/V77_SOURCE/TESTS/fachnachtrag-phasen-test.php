<?php
/** Lightweight CLI fixture: V77 preflight against the immutable real V62 manifest. */
declare(strict_types=1);
define('ABSPATH','/test/');
$source=json_decode(file_get_contents($argv[1]??''),true,512,JSON_THROW_ON_ERROR);
if(count($source['pages'])!==188||count($source['content_categories'])!==296)throw new Exception('unexpected original manifest');
$options=[];$posts=[];$terms=[];$postmeta=[];$termmeta=[];
function current_user_can($cap){return true;}
function get_option($key,$fallback=[]){global $options;return $options[$key]??$fallback;}
function is_wp_error($value){return false;}
function sanitize_title($value){$v=strtolower(trim((string)$value));$v=preg_replace('/[^a-z0-9]+/','-',$v);return trim((string)$v,'-');}
function get_post($id){global $posts;return $posts[$id]??null;}
function get_term($id,$taxonomy){global $terms;return $terms[$id]??null;}
function get_post_meta($id,$key,$single=true){global $postmeta;return $postmeta[$id][$key]??'';}
function get_term_meta($id,$key,$single=true){global $termmeta;return $termmeta[$id][$key]??'';}
class Robotik_Kategorie_Gesamtvorschau { public static function source():array {global $source;return $source;} }
class Robotik_V63_Delta {
    public static array $stub=[];
    public static function prepare():array {return self::$stub;}
    public static function createOne(array $task,array &$pages,array &$terms):string {throw new Exception('fixture must not write');}
}
require dirname(__DIR__).'/includes/class-robotik-v77-fachnachtrag.php';
function check(bool $yes,string $msg):void {if(!$yes)throw new Exception('FAIL: '.$msg);}
function mustBlock(string $name):void {
    try{Robotik_V77_Fachnachtrag::plan();}catch(RuntimeException $e){echo "PASS $name: ".$e->getMessage()."\n";return;}
    throw new Exception("FAIL $name should block");
}
mustBlock('no prior import');
$options['robotik_v63_delta_state']=['status'=>'WRITING','index'=>16,'verified'=>0];
mustBlock('incomplete 227 import');
$options['robotik_v63_delta_state']=['status'=>'COMPLETE_SAFE_DELTA_WITH_16_HOLDS','index'=>227,'verified'=>227];
mustBlock('missing 68 publication');
$options['robotik_v65_publication_state']=['status'=>'COMPLETE','index'=>68,'verified'=>68];
$pageId=1000;$termId=5000;$ids=[];$rowPages=[];$rowCats=[];$wpPages=[];$wpCats=[];
foreach($source['pages'] as $item) {
    $id=(string)$item['source_id'];
    if(!empty($item['review_hold'])){$rowPages[$id]=['status'=>'NEW_PAGE_PROPOSAL_NOT_WRITTEN'];continue;}
    $ids[$id]=++$pageId;
}
$termIds=[];
foreach($source['content_categories'] as $item) {
    $id=(string)$item['source_id'];
    if(!empty($item['review_hold'])){$rowCats[$id]=['status'=>'NEW_TERM_PROPOSAL_NOT_WRITTEN'];continue;}
    $termIds[$id]=++$termId;
}
check(count($ids)===172,'baseline page IDs 172');
check(count($termIds)===248,'baseline term IDs 248');
Robotik_V63_Delta::$stub=['errors'=>[],'task_done'=>227,'task_remaining'=>0,
    'page_ids'=>$ids,'term_ids'=>$termIds,'page_rows'=>$rowPages,'term_rows'=>$rowCats,
    'inventory'=>['pages'=>['items'=>[]],'categories'=>['items'=>[]]],
    'token'=>'test-token','prior_wp_page_ids'=>array_values($ids),'prior_wp_term_ids'=>array_values($termIds)];
$plan=Robotik_V77_Fachnachtrag::plan();
check(count($plan['tasks'])===64,'64 deterministic tasks');
check(count(array_filter($plan['tasks'],fn($x)=>$x['kind']==='page'))===16,'16 type pages');
check(count(array_filter($plan['tasks'],fn($x)=>$x['kind']==='category'))===48,'48 content categories');
check(!$plan['errors']&&$plan['remaining']===64&&$plan['done']===0,'initial safe preflight');
echo "PASS 16+48 prepare no duplicates\n";
$byPath=[];foreach($source['pages'] as $item)$byPath[implode(' / ',$item['path'])]=$item;
foreach($source['pages'] as $item){
    if(empty($item['review_hold']))continue;
    $key=(string)$item['source_id'];$parentPath=array_slice($item['path'],0,-1);
    $parent=$byPath[implode(' / ',$parentPath)]['source_id'];
    $wpid=++$pageId;$ids[$key]=$wpid;
    $posts[$wpid]=(object)['post_type'=>'page','post_title'=>$item['title'],
      'post_name'=>sanitize_title($item['title']),'post_parent'=>$ids[$parent],'post_status'=>'publish'];
    $postmeta[$wpid]=['_robotik_kategorie_node_id'=>$key,'_robotik_page_role'=>$item['role']];
    $rowPages[$key]=['status'=>'CONFIRMED_META_AND_PATH'];
}
foreach($source['content_categories'] as $item){
    if(empty($item['review_hold']))continue;
    $key=(string)$item['source_id'];$wpid=++$termId;$termIds[$key]=$wpid;
    $name=implode(' / ',$item['owner_path']).' – '.$item['short_label'];
    $slug=sanitize_title(implode(' ',$item['owner_path']).' '.$item['short_label']);
    $terms[$wpid]=(object)['slug'=>$slug,'name'=>$name,'parent'=>0];
    $termmeta[$wpid]=['_robotik_kategorie_node_id'=>$key,'_robotik_product_page_id'=>$ids[$item['owner_id']]];
    $rowCats[$key]=['status'=>'CONFIRMED_TERM_META'];
}
Robotik_V63_Delta::$stub['page_ids']=$ids;
Robotik_V63_Delta::$stub['term_ids']=$termIds;
Robotik_V63_Delta::$stub['page_rows']=$rowPages;
Robotik_V63_Delta::$stub['term_rows']=$rowCats;
$done=Robotik_V77_Fachnachtrag::plan();
check(!$done['errors']&&$done['done']===64&&$done['remaining']===0,'completed readback');
check(count($done['page_ids'])===188&&count($done['term_ids'])===296,'full final owner counts');
echo "PASS 188 pages / 296 categories independently identified\n";
$victim=$source['content_categories'];
foreach($victim as $x)if(!empty($x['review_hold'])){ $tid=$termIds[$x['source_id']];break; }
$termmeta[$tid]['_robotik_product_page_id']=123456789;
$bad=Robotik_V77_Fachnachtrag::plan();
check(count($bad['errors'])>0,'wrong term owner stops readback');
echo "PASS changed owner blocked; no false completion\n";
echo "V77 MOCK PASS\n";
