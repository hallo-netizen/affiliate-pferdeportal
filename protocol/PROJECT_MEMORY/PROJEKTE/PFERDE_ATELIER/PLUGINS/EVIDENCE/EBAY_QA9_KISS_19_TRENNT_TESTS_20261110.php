<?php
error_reporting(E_ALL);
define('HOUR_IN_SECONDS',3600);define('MINUTE_IN_SECONDS',60);define('ARRAY_A','ARRAY_A');
$GLOBALS['options']=[];$GLOBALS['transients']=[];$GLOBALS['events']=[];
function get_option($k,$default=null){return $GLOBALS['options'][$k]??$default;}
function update_option($k,$v,$autoload=false){$GLOBALS['options'][$k]=$v;return true;}
function get_transient($k){return $GLOBALS['transients'][$k]??false;}
function set_transient($k,$v,$ttl){$GLOBALS['transients'][$k]=$v;return true;}
function delete_transient($k){unset($GLOBALS['transients'][$k]);}
function wp_next_scheduled($hook,$args=[]){foreach($GLOBALS['events'] as $ev){if($ev['hook']===$hook&&$ev['args']===$args)return $ev['time'];}return false;}
function wp_schedule_single_event($time,$hook,$args=[]){$GLOBALS['events'][]=compact('time','hook','args');return true;}
function wp_schedule_event($time,$recurrence,$hook,$args=[]){$GLOBALS['events'][]=compact('time','hook','args','recurrence');return true;}
function sanitize_key($s){return preg_replace('/[^a-z0-9_\-]/','',strtolower((string)$s));}
function sanitize_text_field($s){return (string)$s;}
function absint($v){return abs((int)$v);}
function wp_json_encode($v,$flags=0){return json_encode($v,$flags);}
function is_wp_error($v){return $v instanceof WP_Error;}
class WP_Error{private $c;function __construct($c){$this->c=$c;}function get_error_code(){return $this->c;}}
function ok($p,$s){if(!$p){fwrite(STDERR,"FAIL: $s\n");exit(1);}echo "PASS: $s\n";}
class FakeDB{
 public $last_error=''; public $rows=[];public $objects=[];public $queries=[];
 function prepare($q,...$args){foreach($args as $a){$pos=strpos($q,'%');if($pos!==false)$q=substr_replace($q,is_numeric($a)?(string)$a:"'".$a."'",$pos,2);}return $q;}
 function get_results($q,$fmt){$this->queries[]=$q;preg_match('/e\.id>(\d+)/',$q,$m);$cursor=(int)($m[1]??0);$out=[];
  foreach($this->rows as $row){if($row['id']<=$cursor)continue;if(($row['source_state']??'')!=='available')continue;
  if($row['fresh_until']>time()+7200)continue;if($row['source_checked_at']>time()-900)continue;
  $id=$row['creative_identity_hash'];if(!in_array($id,array_column($this->objects,'creative_identity_hash'),true))continue;$out[]=$row;}
  usort($out,fn($a,$b)=>$a['id']<=>$b['id']);return array_slice($out,0,5);
 }
 function get_col($q){$this->queries[]=$q;return array_column($this->objects,'campaign_post_id');}
 function get_var($q){$this->queries[]=$q;preg_match('/campaign_post_id=(\d+)/',$q,$m);$id=(int)($m[1]??0);foreach($this->objects as $row){if($row['campaign_post_id']===$id&&$row['status']==='published')return $row['id'];}return null;}
}
function extract_methods($file,$start,$end){$content=file_get_contents($file);$a=strpos($content,$start);$b=strpos($content,$end,$a);if($a===false||$b===false)throw new Exception('cannot extract '.$start);return substr($content,$a,$b-$a);}
$root=__DIR__.'/affiliate-portal-router/includes/';
$availability=extract_methods($root.'trait-ppar-ebay.php','    private function ebay_public_availability_state_save(', '    private function ebay_refresh_due_rows(');
$append=extract_methods($root.'trait-ppar-ebay-run.php','    private function ebay_public_checkpoint_add_verified_business_ids(', '    /** Incremental public release of ONLY');
$inc=extract_methods($root.'trait-ppar-ebay-run.php','    private function ebay_run_publish_ready_business_subset(', '    private function ebay_run_checkpoint_capture_selection(');
$availability.="\n".$append."\n".$inc;
$cls='class QA9Probe { public $refreshes=0; public $rebuilds=0; public $remoteFail=false; public $rules=[]; public $selected=[]; public $checkpoint=[]; public $run=[]; const EBAY_REFRESH_CRON_HOOK="ppar_ebay_inventory_refresh";
private function ebay_settings(){return ["enabled"=>1,"business_enabled"=>1,"environment"=>"sandbox"];}
private function ebay_deletion_compliance_complete(){return true;}
private function ebay_items_table(){return "items";}
private function output_objects_table(){return "objects";}
private function ebay_access_token($settings){return $this->remoteFail?new WP_Error("auth_error"):"token";}
private function ebay_refresh_process_row(&$job,$row,$settings,$token){$this->refreshes++;$job["summary"]["available"]++;}
private function ebay_public_checkpoint_load(){return $this->checkpoint;}
private function ebay_public_checkpoint_is_safe($c){return ($c["status"]??"")==="safe" && ($c["schema"]??"")==="1.0";}
private function ebay_public_checkpoint_business_ids($c){return $c["business_campaign_ids"]??[];}
private function ebay_public_checkpoint_save($c){$this->checkpoint=$c;return $c;}
private function output_campaign_by_post_id($id){return ["post_id"=>$id,"network"=>"ebay","active"=>isset($this->rules[$id])];}
private function ebay_business_campaign_source_allows_delivery_base($c){return $this->rules[$c["post_id"]]??false;}
private function article_hybrid_enabled(){return true;}
private function article_plan_rebuild_request($reason,$revision,$mode){$this->rebuilds++;}
private function article_plan_campaign_revision(){return 0;}
private function ebay_run_load(){return $this->run;}
private function ebay_run_is_open($r){return ($r["status"]??"")==="paused" || ($r["status"]??"")==="running";}
private function ebay_run_checkpoint_business_ids_from_selection($s,$old,$mode){return $this->selected;}
'.$availability.'}';
eval($cls);
$GLOBALS['wpdb']=new FakeDB();
$x=new QA9Probe();$x->checkpoint=['status'=>'safe','schema'=>'1.0','checkpoint_id'=>'old','business_campaign_ids'=>[101],'verification'=>[]];$x->rules=[102=>true,103=>false,104=>true];
$GLOBALS['wpdb']->objects=[['id'=>1,'campaign_post_id'=>102,'creative_identity_hash'=>str_repeat('a',64),'status'=>'published'],['id'=>2,'campaign_post_id'=>103,'creative_identity_hash'=>str_repeat('b',64),'status'=>'published'],['id'=>3,'campaign_post_id'=>104,'creative_identity_hash'=>str_repeat('c',64),'status'=>'draft']];
$added=(new ReflectionMethod(QA9Probe::class,'ebay_public_checkpoint_add_verified_business_ids'))->invoke($x,[101,102,103,104],'availability_refresh');
ok($added===1,'only published, active and verified campaign added');
ok($x->checkpoint['business_campaign_ids']===[101,102],'old last-good retained');
ok($x->rebuilds===1,'product-only rebuild scheduled exactly once');
ok((new ReflectionMethod(QA9Probe::class,'ebay_public_checkpoint_add_verified_business_ids'))->invoke($x,[102,103,104],'selection')===false,'second same publish does not write or rebuild');
ok($x->rebuilds===1,'idempotent public checkpoint append');
$x->run=['status'=>'paused','operation'=>'sync'];$x->selected=[104];
ok((new ReflectionMethod(QA9Probe::class,'ebay_run_publish_ready_business_subset'))->invoke($x,['business_active'=>[104=>[]]])===false,'draft product does not pass incremental publication');
$x->selected=[102];
ok((new ReflectionMethod(QA9Probe::class,'ebay_run_publish_ready_business_subset'))->invoke($x,['business_active'=>[102=>[]]])===false,'paused run retains already approved product without repetition');
$hashes=[str_repeat('a',64),str_repeat('b',64),str_repeat('c',64),str_repeat('d',64),str_repeat('e',64),str_repeat('f',64)];
$GLOBALS['wpdb']->objects=[];$GLOBALS['wpdb']->rows=[];
foreach($hashes as $i=>$h){$GLOBALS['wpdb']->rows[]=['id'=>$i+1,'seller_account_type'=>'BUSINESS','source_state'=>'available','creative_identity_hash'=>$h,'fresh_until'=>time()-600,'source_checked_at'=>time()-10000];$GLOBALS['wpdb']->objects[]=['id'=>$i+10,'creative_identity_hash'=>$h,'campaign_post_id'=>$i+201,'status'=>'published'];}
$beforeRun=$x->run;
$r=$x->ebay_public_availability_tick('');
ok(($r['status']??'')==='continuing' && $x->refreshes===5,'first background batch checks 5 stored public products');
ok((get_option('ppar_ebay_public_availability_state_v1')['cursor']??0)===5,'availability cursor durably saved');
ok(count($GLOBALS['events'])===1,'exactly one continuation scheduled');
$r=$x->ebay_public_availability_tick('continuation');
ok(($r['status']??'')==='complete' && $x->refreshes===6,'second batch finishes remaining existing products');
ok((get_option('ppar_ebay_public_availability_state_v1')['cursor']??-1)===0,'new availability cycle starts with zero cursor');
ok($x->run===$beforeRun,'paused discovery run and cursor never mutated');
ok(($x->checkpoint['business_campaign_ids']??[])===[101,102],'never lose previous public ids');
$r=$x->ebay_public_availability_tick();
ok(($r['status']??'')==='not_due' && $x->refreshes===6,'no duplicate refresh before two hours');
// Authentication error must retain cursor and never invent a valid availability proof.
update_option('ppar_ebay_public_availability_state_v1',['running'=>1,'cursor'=>0,'next_due_at'=>0]);$x->remoteFail=true;
$r=$x->ebay_public_availability_tick('heartbeat');
ok(($r['status']??'')==='auth_unavailable' && $x->refreshes===6,'failed eBay token does not refresh or publish');
ok((get_option('ppar_ebay_public_availability_state_v1')['cursor']??-1)===0,'auth failure keeps retry position');
// First product creates a verifiable initial checkpoint without requiring a
// completed discovery run; a malformed existing snapshot is NEVER overwritten.
$x->checkpoint=[];$x->rebuilds=0;$x->rules[102]=true;
$GLOBALS['wpdb']->objects=[['id'=>80,'campaign_post_id'=>102,'status'=>'published']];
$added=(new ReflectionMethod(QA9Probe::class,'ebay_public_checkpoint_add_verified_business_ids'))->invoke($x,[102],'selection');
ok($added===1 && $x->checkpoint['business_campaign_ids']===[102], 'first qualified published product creates safe foundation');
$x->checkpoint=['status'=>'corrupted','schema'=>'0','business_campaign_ids'=>[101]];
$added=(new ReflectionMethod(QA9Probe::class,'ebay_public_checkpoint_add_verified_business_ids'))->invoke($x,[102],'selection');
ok($added===false && $x->checkpoint['business_campaign_ids']===[101], 'invalid old checkpoint is never overwritten');
print "QA9 functional cases passed\n";