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
require __DIR__.'/affiliate-portal-router/includes/trait-ppar-ebay-run.php';
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
  $task['summary']['requests']++;
  if($value==='ok'){
    $task['summary']['available']++;
    return;
  }
  $task['summary']['technical_errors']++;
  if($value==='transient'){$task['summary']['technical_errors']=0;$task['summary']['transient_errors']++;}
  $task['summary']['errors'][]=array('code'=>$value==='transient'?'ebay_refresh_transient_http':(in_array($value,array('auth401','auth403'),true)?'ebay_refresh_http':$value),
      'error'=>$value==='auth401'?'eBay-Bestandsabgleich fehlgeschlagen (HTTP 401)':($value==='auth403'?'eBay-Bestandsabgleich fehlgeschlagen (HTTP 403)':'an individual offer failed'));
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
$f->verify_tick(get_option('ppar_ebay_run_state_v1'),$cfg);$s=get_option('ppar_ebay_run_state_v1');
expect($f->calls===array(101,102),'isolated item fails, next independent item still checked');
expect($s['status']==='completed'&& !empty($s['completed_with_skips']),'one item failure ends with WARN, not global FAIL');
expect(($s['checkpoint_deferred_reason']??'')==='public_source_refresh_unverified','unsafe final publication deferred');
expect(($s['public_source_refresh']['provider_errors']??0)===1,'single item cause recorded in durable state');
expect($f->commit_calls===0&&get_option('ppar_ebay_public_checkpoint_v1')['checkpoint_id']==='old-safe','old safe checkpoint preserved, unverified item never approved');
expect(count($f->calls)===2,'two-remote cap enforced including errors');
$f=setup_fixture(array(101,102),array(101=>array('transient','transient','transient'),102=>array('ok')));
$f->verify_tick(get_option('ppar_ebay_run_state_v1'),$cfg);$s=get_option('ppar_ebay_run_state_v1');
expect($s['status']==='running'&&($s['public_source_refresh']['retry_attempts']??0)===1,'first transient retries same source without losing cursor');
$f->verify_tick(get_option('ppar_ebay_run_state_v1'),$cfg);$s=get_option('ppar_ebay_run_state_v1');
expect($s['status']==='running'&&($s['public_source_refresh']['retry_attempts']??0)===2,'second transient preserves source and cursor');
$f->verify_tick(get_option('ppar_ebay_run_state_v1'),$cfg);$s=get_option('ppar_ebay_run_state_v1');
expect($f->calls===array(101,101,101,102),'after two retries the next unrelated item is checked');
expect($s['status']==='completed'&&($s['public_source_refresh']['provider_errors']??0)===1,'exhausted item retries create WARN, no global failure');
$f=setup_fixture(array(101,102,103),array(101=>array('ebay_refresh_http'),102=>array('ebay_refresh_http'),103=>array('ok')));
$f->refresh_tick(get_option('ppar_ebay_run_state_v1'),$cfg);$s=get_option('ppar_ebay_run_state_v1');
expect($f->calls===array(101,102)&&$s['public_source_refresh']['cursor']===2,'two failed remote requests do not bypass two-request cap');
$f->verify_tick(get_option('ppar_ebay_run_state_v1'),$cfg);$s=get_option('ppar_ebay_run_state_v1');
expect($f->calls===array(101,102,103)&&$s['status']==='completed','third independent item processed in next bounded tick');
$f=setup_fixture(array(101,102),array(101=>array('auth401'),102=>array('ok')));
$f->verify_tick(get_option('ppar_ebay_run_state_v1'),$cfg);$s=get_option('ppar_ebay_run_state_v1');
expect($s['status']==='failed'&&$s['error_code']==='public_source_refresh_auth_failed','401 global authorization still hard-fails (never forged as product miss)');
expect($f->calls===array(101),'global auth fault does not continue unauthorized requests');
$f=setup_fixture(array(101,102),array(101=>array('auth403'),102=>array('ok')));
$f->verify_tick(get_option('ppar_ebay_run_state_v1'),$cfg);$s=get_option('ppar_ebay_run_state_v1');
expect($s['status']==='failed'&&$s['error_code']==='public_source_refresh_auth_failed','403 global authorization still hard-fails');
expect($f->calls===array(101),'403 hard failure never continues other unauthorized requests');
$f=setup_fixture(array(101,102),array(101=>array('ok'),102=>array('ok')));
$f->verify_tick(get_option('ppar_ebay_run_state_v1'),$cfg);$s=get_option('ppar_ebay_run_state_v1');
expect($f->commit_calls===1 && $s['phase']==='completed','all-success source refresh follows original successful commit path');
expect(get_option('ppar_ebay_public_checkpoint_v1')['checkpoint_id']==='new-verified','normal verified source replaces last-good checkpoint');
$f=setup_fixture(array(101,102),array(101=>array('ebay_refresh_http'),102=>array('ok')),false);
$f->verify_tick(get_option('ppar_ebay_run_state_v1'),$cfg);$s=get_option('ppar_ebay_run_state_v1');
expect($s['status']==='completed'&&$f->commit_calls===0,'without old checkpoint error still does not forge a new public checkpoint');
expect(!get_option('ppar_ebay_public_checkpoint_v1',null),'without old checkpoint no fake safe public set is created');
$f=setup_fixture(array(101),array(101=>array('ok')));$f->token_failed=true;
$f->verify_tick(get_option('ppar_ebay_run_state_v1'),$cfg);$s=get_option('ppar_ebay_run_state_v1');
expect($s['status']==='failed'&&$s['error_code']==='public_source_refresh_auth_failed','token creation failure remains a global fail-closed error');
echo "ALL QA11 REAL TRAIT CONTRACT CASES PASS\n";

// Terminal recovery: exact failed last-mile state, SAME run, SAME stored cursors.
$f=setup_fixture(array(101,102),array(101=>array('ok'),102=>array('ok')));
$run=get_option('ppar_ebay_run_state_v1');
$run['status']='failed';$run['phase']='failed';$run['operation']='sync';
$run['orchestrator_contract']='self_drive_v1';
$run['error_code']='public_source_refresh_provider_failed';
$run['error_message']='final provider failure';
$run['errors']=array(array('code'=>'public_source_refresh_provider_failed','details'=>array('phase'=>'public_verify')));
$run['public_source_refresh']=array('fingerprint'=>'stored-run-fp','cursor'=>1,'checked'=>1,'refreshed'=>1);
$run['progress_seq']=571;$run['finished_at']=12345;
$run['phase_state']=array('selection'=>array('cursor'=>999,'status'=>'complete'));
$run['gapfill']=array('attempts'=>1,'missing'=>array('example-concept'));
update_option('ppar_ebay_run_state_v1',$run);
expect($f->ebay_run_failed_public_refresh_resumable($run),'exact old failed final-source error is resumable');
$before=serialize($run['checkpoint_candidate']);$previous=serialize(get_option('ppar_ebay_public_checkpoint_v1'));
$res=$f->ebay_run_resume_failed_public_refresh();$after=get_option('ppar_ebay_run_state_v1');
expect(!is_wp_error($res)&&$res['run_uuid']==='fixture-run'&&$res['cursor']===1,'resume reuses UUID and final-source cursor exactly');
expect($after['phase']==='public_verify'&&$after['status']==='running','resumes ONLY final verification; no new discovery or gapfill');
expect($after['phase_state']['selection']['cursor']===999 && $after['progress_seq']===572,'preserves verified source and previous 571 progress steps');
expect(serialize($after['checkpoint_candidate'])===$before && serialize(get_option('ppar_ebay_public_checkpoint_v1'))===$previous,'source candidates and last-good checkpoint unchanged');
expect($after['gapfill']['missing']===array('example-concept')&&$f->scheduled===array(1),'all gap-search state preserved, exactly one existing background worker scheduled');
expect($after['error_code']===''&& count($after['errors'])===1,'old terminal cause kept in audit but not shown as current failure');
expect(!$f->ebay_run_failed_public_refresh_resumable($after),'cannot resume an already running run twice');
$f=setup_fixture(array(101,102),array());$run=get_option('ppar_ebay_run_state_v1');
$run['status']='failed';$run['phase']='failed';$run['operation']='sync';$run['orchestrator_contract']='self_drive_v1';
$run['error_code']='public_source_refresh_auth_failed';
$run['errors']=array(array('code'=>'public_source_refresh_auth_failed','details'=>array('phase'=>'public_verify')));
update_option('ppar_ebay_run_state_v1',$run);
expect(!$f->ebay_run_failed_public_refresh_resumable($run),'global auth failure is never auto-qualified for same-run resume');
$r=$f->ebay_run_resume_failed_public_refresh();
expect(is_wp_error($r) && get_option('ppar_ebay_run_state_v1')['status']==='failed','wrong failure status kept intact, no new worker scheduled');
$f=setup_fixture(array(101),array());$run=get_option('ppar_ebay_run_state_v1');
$run['status']='failed';$run['phase']='failed';$run['operation']='sync';$run['orchestrator_contract']='self_drive_v1';
$run['error_code']='public_source_refresh_provider_failed';
$run['errors']=array(array('code'=>'public_source_refresh_provider_failed','details'=>array('phase'=>'public_verify')));
// First provider item can fail before any source cursor was stored.
update_option('ppar_ebay_run_state_v1',$run);
expect($f->ebay_run_failed_public_refresh_resumable($run),'first-item failure safely resumable even without initial refresh fingerprint');
$r=$f->ebay_run_resume_failed_public_refresh();$after=get_option('ppar_ebay_run_state_v1');
expect(!is_wp_error($r)&&$after['phase']==='public_verify','first-item resume recomputes source plan, not discovery');
$f=setup_fixture(array(101),array());$run=get_option('ppar_ebay_run_state_v1');
$run['status']='failed';$run['phase']='failed';$run['operation']='local';$run['orchestrator_contract']='self_drive_v1';
$run['error_code']='public_source_refresh_provider_failed';
$run['errors']=array(array('code'=>'public_source_refresh_provider_failed','details'=>array('phase'=>'public_verify')));
update_option('ppar_ebay_run_state_v1',$run);
expect(!$f->ebay_run_failed_public_refresh_resumable($run),'local-only operation can never use remote public resume');
// Read-only admin status, even if stalled: never dispatch or tick worker.
$f=setup_fixture(array(101),array());$run=get_option('ppar_ebay_run_state_v1');
$run['last_progress_at']=time()-600;$run['started_at']=time()-900;
$run['last_transport_tick_at']=time()-600;
$run['orchestrator_contract']='self_drive_v1';
update_option('ppar_ebay_run_state_v1',$run);
$before=serialize(get_option('ppar_ebay_run_state_v1'));
$view=$f->run_ebay_admin_ajax_tick();
expect($view['stalled']===1&&$view['recovery']==='none','backend shows genuine stall without triggering a worker');
expect(serialize(get_option('ppar_ebay_run_state_v1'))===$before&&$f->scheduled===array(),'admin status read is side-effect-free and did not schedule a job');
print "ALL QA11 PUBLIC SOURCE, SAFE RESUME & READ-ONLY UI TESTS PASS\n";