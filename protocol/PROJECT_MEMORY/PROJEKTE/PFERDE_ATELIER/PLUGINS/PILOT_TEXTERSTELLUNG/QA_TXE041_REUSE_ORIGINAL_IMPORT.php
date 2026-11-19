<?php
// Isolated QA: exercises the *modified EXISTING candidate* against unchanged PSERC methods.
error_reporting(E_ALL);
define('ABSPATH','/test/'); define('ARRAY_A','ARRAY_A');
$GLOBALS['options'] = []; $GLOBALS['wp_posts']=[]; $GLOBALS['wp_next_id']=20; $GLOBALS['ppm_mode']='ok'; $GLOBALS['ppm_calls']=0; $GLOBALS['created']=0;
class FakeDB {public $prefix='wp_';public function prepare($q,...$values){return vsprintf(str_replace('%s',"'%s'",$q),$values);}public function get_var($q){return str_contains($q,'GET_LOCK')||str_contains($q,'RELEASE_LOCK')?'1':null;}}
$GLOBALS['wpdb'] = new FakeDB();
function home_url($path='/'){return 'https://qa.example.invalid/';} function get_current_blog_id(){return 1;}
function current_user_can($cap){return true;}
function get_option($key,$default=false){return $GLOBALS['options'][$key]??$default;}
function update_option($key,$value,$autoload=false){$GLOBALS['options'][$key]=$value;return true;}
function wp_json_encode($data,$opts=0){return json_encode($data,$opts);}
function add_action(...$a){} function add_filter(...$a){} function register_activation_hook(...$a){}
function get_term_by($field,$slug,$tax){return $slug==='reitpflege'?(object)['term_id'=>7,'slug'=>'reitpflege']:false;}
function sanitize_title($s){return trim(preg_replace('/[^a-z0-9]+/','-',strtolower($s)),'-');}
function wp_slash($x){return $x;}function is_wp_error($x){return false;}
function wp_insert_post($a,$err=false){$id=$GLOBALS['wp_next_id']++;$a['ID']=$id;$GLOBALS['wp_posts'][$id]=$a;$GLOBALS['created']++;return $id;}
function get_post($id,$type=null){return $GLOBALS['wp_posts'][$id]??null;}
function get_post_meta($id,$key,$single=false){return $GLOBALS['wp_posts'][$id]['meta_input'][$key]??'';}
function wp_get_post_categories($id){return $GLOBALS['wp_posts'][$id]['post_category']??[];}
function get_posts($opts){return array_keys($GLOBALS['wp_posts']);}
function wp_delete_post($id,$force=false){unset($GLOBALS['wp_posts'][$id]);return true;}
if(($argv[1]??'')!=='no-ppm'){class PPM679_Editorial_Plan_Runtime_Gate {public static function record_readback($b,$r,$reason){$GLOBALS['ppm_calls']++;return $GLOBALS['ppm_mode']==='fail'?['ok'=>false,'status'=>'FORCED_FAIL']:['ok'=>true,'publish_allowed'=>false];}}}
require dirname(__DIR__).'/txe041_originalimport/texterstellung/texterstellung.php';
$GLOBALS['options'][TXE_Workshop::TEST_MODE_OPTION]=hash('sha256',home_url('/').'|'.get_current_blog_id());
function row($n){$id='qa-txe-'.$n;return ['article_id'=>$id,'plan_slot'=>PSERC_Plan_Slot_Identity::tokenFromCanonicalId($id),'title'=>'Qa pferdepflege '.$n,'slug'=>'qa-pferdepflege-'.$n,'target_keyword'=>'qa-pferdepflege-'.$n,'category'=>'reitpflege','article_type'=>'RATGEBER','body'=>'<p>QA nur Testinhalt.</p>'];}
function one($r){return ['contract'=>TXE_Workshop::IMPORT_CONTRACT,'articles'=>[$r]];}
function next_request(){(new ReflectionClass(PSERC_System4_Import::class))->getProperty('collisionIndex')->setValue(null,null);}
function ready($r){$o='TXE-'.$r['article_id'];$GLOBALS['options'][TXE_Workshop::OPTION]['orders'][$o]=['id'=>$o,'plan_slot'=>$r['plan_slot'],'article_id'=>$r['article_id'],'status'=>'EXPORTIERT','title'=>$r['title'],'target_keyword'=>$r['target_keyword'],'category'=>$r['category'],'article_type'=>$r['article_type'],'post_id'=>0];}
$GLOBALS['options'][TXE_Workshop::OPTION]=['orders'=>[],'last_batch'=>null,'research'=>[],'title_batches'=>[],'active_title_batch'=>''];
$checks=[];
function checkit($name,$fn){try{$ok=(bool)$fn();$GLOBALS['checks'][]=['name'=>$name,'pass'=>$ok];}catch(Throwable $e){$GLOBALS['checks'][]=['name'=>$name,'pass'=>false,'error'=>$e->getMessage()];}}
$r=row(1);ready($r);
if(($argv[1]??'')==='no-ppm'){
 checkit('missing_original_ppm_blocks_all_writes',function()use($r){try{TXE_Workshop::importDrafts(one($r));return false;}catch(RuntimeException $e){return str_contains($e->getMessage(),'PSERC_SYSTEM4_EDITORIAL_RUNTIME_GATE_UNAVAILABLE')&&$GLOBALS['created']===0;}});
}else{
 checkit('original_import_creates_exactly_one_draft',function()use($r){$x=TXE_Workshop::importDrafts(one($r));$p=$GLOBALS['wp_posts'][$x['draft_ids'][0]];return $x['created']===1&&$p['post_status']==='draft'&&($p['meta_input']['_ppm679_publish_blocked']??null)==='1'&&$GLOBALS['ppm_calls']===1;});
 checkit('original_import_preserves_txe_state',fn()=>($GLOBALS['options'][TXE_Workshop::OPTION]['orders']['TXE-'.$r['article_id']]['status']??null)==='IMPORTIERT');
 // Original index caches for one request; the same plan slot resolves from original readback.
 next_request();
 checkit('reimport_uses_original_dedup',function()use($r){$x=TXE_Workshop::importDrafts(one($r));return $x['created']===0&&count($GLOBALS['wp_posts'])===1&&$GLOBALS['ppm_calls']===2;});
 checkit('unknown_order_never_writes',function(){$r=row(99);try{TXE_Workshop::importDrafts(one($r));return false;}catch(RuntimeException $e){return $e->getMessage()==='RETURN_NOT_IN_THIS_QUEUE'&&count($GLOBALS['wp_posts'])===1;}});
 checkit('changed_keyword_never_writes',function()use($r){$x=$r;$x['target_keyword']='changed';try{TXE_Workshop::importDrafts(one($x));return false;}catch(RuntimeException $e){return $e->getMessage()==='RETURN_APPROVAL_MISMATCH:target_keyword'&&count($GLOBALS['wp_posts'])===1;}});
 next_request();$GLOBALS['ppm_mode']='fail';$new=row(2);ready($new);
 // Importer cache is per-request; test isolation: new item has distinct slot/slug/title.
 checkit('ppm_failure_rolls_back_new_draft',function()use($new){try{TXE_Workshop::importDrafts(one($new));return false;}catch(RuntimeException $e){return str_contains($e->getMessage(),'ORIGINAL_PSERC_IMPORT_BLOCKED')&&count($GLOBALS['wp_posts'])===1&&($GLOBALS['options'][TXE_Workshop::OPTION]['orders']['TXE-'.$new['article_id']]['status']??null)==='EXPORTIERT';}});
 next_request();$GLOBALS['ppm_mode']='ok';
 $twenty=array_map('row',range(100,119));foreach($twenty as $q)ready($q);
 $returnBatch=['contract'=>TXE_Workshop::IMPORT_CONTRACT,'articles'=>array_merge(array_slice($twenty,0,13),[$twenty[0]],array_slice($twenty,13))];
 checkit('twenty_unique_and_one_duplicate_independent_import',function()use($returnBatch){
   $before=count($GLOBALS['wp_posts']);$z=TXE_Workshop::importDraftsIndividually($returnBatch);
   return $z['imported']===20&&$z['created']===20&&count($z['held'])===1&&$z['held'][0]['reason']==='DUPLICATE_IN_RETURN_BATCH'
    &&count($GLOBALS['wp_posts'])===$before+20;
 });
 checkit('batch_all_original_publish_blocks_preserved',function(){
   $subset=array_filter($GLOBALS['wp_posts'],fn($p)=>str_starts_with($p['post_name'],'qa-pferdepflege-1'));
   return count($subset)===21&&count(array_filter($subset,fn($p)=>($p['meta_input']['_ppm679_publish_blocked']??'')==='1' && $p['post_status']==='draft'))===21;
 });
}
$pass=count(array_filter($checks,fn($c)=>$c['pass']));echo json_encode(['pass'=>$pass,'total'=>count($checks),'mode'=>$argv[1]??'ppm','checks'=>$checks],JSON_PRETTY_PRINT|JSON_UNESCAPED_UNICODE),"\n";exit($pass===count($checks)?0:1);