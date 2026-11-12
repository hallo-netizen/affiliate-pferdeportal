<?php
// Executes actual QA11 run trait, with bounded fake WordPress storage/provider.
define('ABSPATH','/tmp/');define('ARRAY_A','ARRAY_A');define('MINUTE_IN_SECONDS',60);define('HOUR_IN_SECONDS',3600);
$GLOBALS['fake_options']=array();$GLOBALS['fake_post_hashes']=array();
function sanitize_text_field($x){return trim((string)$x);}
function sanitize_key($x){return preg_replace('/[^a-z0-9_\-]/','',strtolower((string)$x));}
function absint($x){return abs((int)$x);}
function wp_json_encode($x,$opts=0){return json_encode($x,$opts);}
function get_option($key,$default=null){return array_key_exists($key,$GLOBALS['fake_options'])?$GLOBALS['fake_options'][$key]:$default;}
function update_option($key,$value,$autoload=false){$GLOBALS['fake_options'][$key]=$value;return true;}
function get_post_meta($id,$key,$single=false){return $GLOBALS['fake_post_hashes'][(int)$id]??'';}
function is_wp_error($x){return $x instanceof WP_Error;}
class WP_Error {private $code;private $message;function __construct($code,$message){$this->code=$code;$this->message=$message;} function get_error_code(){return $this->code;}function get_error_message(){return $this->message;}}
class FakeDB {
 public $last_error=''; public $rows=array();
 public function prepare($query,...$args){return str_replace('%s',"'".(string)($args[0]??'')."'",$query);}
 public function get_row($sql,$mode=''){
   if(!preg_match("/creative_identity_hash='([a-f0-9]{64})'/",$sql,$m)){return null;}
   return $this->rows[$m[1]]??null;
 }
}
require '/mnt/data/qa10_stage/affiliate-portal-router/includes/trait-ppar-ebay-run.php';
class RunFixture {
 use PPAR_Ebay_Run_Trait {
   ebay_run_public_source_refresh_tick as public refresh_tick;
   ebay_run_tick_public_verify as public verify_tick;
 }
 const EBAY_RUNTIME_BUILD='qa11_real_run_trait';
 const VERSION='6.72.322';
 public $response_codes=array();public $calls=array();public $commit_calls=0;public $token_failed=false;public $scheduled=array();
 public function ebay_run_schedule_worker($delay=10){$this->scheduled[]=$delay;return true;}
 public function ebay_items_table(){return 'fake_ebay_items';}
 public function ebay_access_token($s){return $this->token_failed?new WP_Error('auth','auth denied'):'fake-token';}
 public function ebay_refresh_process_row(&$task,$row,$settings,$token){
  $id=(int)$row['campaign_id'];$this->calls[]=$id;
  $queue=$this->response_codes[$id]??array('ok');
  $value=array_shift($queue);$this->response_codes[$id]=$queue;
  $task['summary']['checked']++;
  if($value==='ok'){
    $task['summary']['available']++;
    return;
  }
  $task['summary']['technical_errors']++;
  if($value==='transient'){$task['summary']['technical_errors']=0;$task['summary']['transient_errors']++;}
  $task['summary']['errors'][]=array('code'=>$value==='transient'?'ebay_refresh_transient_http':($value==='auth401'?'ebay_refresh_http':$value),
      'error'=>$value==='auth401'?'eBay-Bestandsabgleich fehlgeschlagen (HTTP 401)':'an individual offer failed');
 }
 public function ebay_run_public_business_coverage($ids=null){return array('required'=>298,'covered'=>count((array)$ids),'missing'=>array(),'counts'=>array());}
 public function ebay_run_private_public_revalidation_required($run,$settings){return false;}
 public function ebay_run_verify_private_public($settings,$ids){return array('status'=>'pass');}
 public function ebay_run_commit_public_checkpoint($run,$business,$private){
  $this->commit_calls++;
  return $this->ebay_public_checkpoint_save(array('checkpoint_id'=>'new-verified','schema'=>'1.0','status'=>'safe',
      'business_campaign_ids'=>(array)($run['checkpoint_candidate']['business_campaign_ids']??array())));
 }
}
function setup_fixture($ids,$responses,$last_good=true){
 $GLOBALS['fake_options']=array();$GLOBALS['fake_post_hashes']=array();
 $GLOBALS['wpdb']=new FakeDB();$f=new RunFixture();$f->response_codes=$responses;
 foreach($ids as $id){
  $hash=hash('sha256','campaign-'.$id);$GLOBALS['fake_post_hashes'][$id]=$hash;
  $GLOBALS['wpdb']->rows[$hash]=array('id'=>$id,'campaign_id'=>$id,'source_state'=>'available',
   'policy_state'=>'allowed','status'=>'published','fresh_until'=>time()-10);
 }
 update_option('ppar_ebay_run_state_v1',array('schema'=>'1.0','run_uuid'=>'fixture-run','status'=>'running','phase'=>'public_verify',
    'operation'=>'sync','gapfill'=>array('attempts'=>1),'checkpoint_candidate'=>array('business_campaign_ids'=>$ids,'private_listing_ids'=>array()),
    'config_snapshot'=>array('seller_routes'=>array('business'=>false))));
 if($last_good)update_option('ppar_ebay_public_checkpoint_v1',array('schema'=>'1.0','status'=>'safe',
  'checkpoint_id'=>'old-safe','business_campaign_ids'=>array(501)));
 return $f;
}
function expect($ok,$message){if(!$ok){fwrite(STDERR,"FAIL $message\n");exit(1);}echo "PASS $message\n";}
$cfg=array('business_enabled'=>1);
$f=setup_fixture(array(101,102),array(101=>array('ebay_refresh_http'),102=>array('ok')));
$f->verify_tick(get_option('ppar_ebay_run_state_v1'),$cfg);
$run=get_option('ppar_ebay_run_state_v1');
expect(($run['error_code']??'')==='public_source_refresh_provider_failed'&&($run['status']??'')==='failed','QA9 original: one per-item failure aborts entire run');
expect($f->calls===array(101),'QA9 original: healthy second item never checked');
expect(get_option('ppar_ebay_public_checkpoint_v1')['checkpoint_id']==='old-safe','QA9 original: old public checkpoint stays safe');
echo "BASELINE QA9 REPRODUCED ACTUAL ORIGINAL BUG\n";