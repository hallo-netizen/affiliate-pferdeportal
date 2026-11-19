<?php
// Integration simulation: executes real start, canonical worker, durable state, lease,
// stop/resume and audit methods from the shipped plugin. External eBay/WP phase
// handlers are deterministic stand-ins and MUST NOT be called a real WP E2E test.
error_reporting(E_ALL & ~E_DEPRECATED);
define('ABSPATH','/tmp'); define('DAY_IN_SECONDS',86400); define('MINUTE_IN_SECONDS',60);
$GLOBALS['opts']=[];$GLOBALS['deny']='';$GLOBALS['log']=[];
function get_option($k,$d=false){return array_key_exists($k,$GLOBALS['opts'])?$GLOBALS['opts'][$k]:$d;}
function update_option($k,$v,$autoload=false){if($k===$GLOBALS['deny'])return false;$a=$GLOBALS['opts'][$k]??null;$GLOBALS['opts'][$k]=$v;return serialize($a)!==serialize($v);}
function delete_option($k){unset($GLOBALS['opts'][$k]);return true;}
function absint($v){return abs((int)$v);}function sanitize_key($v){return preg_replace('/[^a-z0-9_\-]/','',strtolower((string)$v));}
function sanitize_text_field($v){return trim(strip_tags((string)$v));}function wp_json_encode($a,$flags=0){return json_encode($a,$flags);}function is_wp_error($a){return $a instanceof WP_Error;}
class WP_Error {public function __construct(private $code,private $message){}public function get_error_code(){return $this->code;}public function get_error_message(){return $this->message;}}
require __DIR__.'/affiliate-portal-router/includes/trait-ppar-ebay-run.php';
class IntegratedRun {
  use PPAR_Ebay_Run_Trait;
  const VERSION='6.72.325',EBAY_RUNTIME_BUILD='6.63.8-self-driven-canonical-orchestrator-rootfix-20260829';
  const EBAY_CONTENT_POLICY_VERSION='6.4',EBAY_PRIVATE_CLASSIFIER_VERSION='4.1',EBAY_BUSINESS_CLASSIFIER_VERSION='6.2',EBAY_PROGRESS_CONTRACT_VERSION='3.1';
  const OPTION_EBAY_RUN_STATE='ppar_ebay_run_state_v1', OPTION_EBAY_PUBLIC_CHECKPOINT='ppar_ebay_public_checkpoint_v1';
  const EBAY_WORK_BLOCK_TICK_LIMIT=60, EBAY_WORK_BLOCK_SECONDS=600, EBAY_WORK_BLOCK_PAUSE_SECONDS=1;
  public $ebay_canonical_worker_active=false,$ebay_run_settings_override=null,$items=['good'=>['verified'=>0,'visible'=>0],'bad'=>['verified'=>0,'visible'=>0]],$phase_calls=[], $dispatches=0;
  public function start(){return $this->ebay_run_start(true,'sync');} public function tick(){return $this->run_ebay_canonical_worker();}
  public function stop(){return $this->ebay_run_request_stop();} public function resume(){return $this->ebay_run_resume_operator_stop();}
  public function state(){return $this->ebay_run_load();} public function checkpoint(){return $this->ebay_public_checkpoint_load();}
  public function store($r){return $this->ebay_run_save($r);} public function auditkey($r){return $this->ebay_audit_key($r);}
  private function ebay_settings(){return ['environment'=>'staging','enabled'=>true,'business_enabled'=>true,'private_enabled'=>false];}
  private function ebay_configuration_errors($settings){return [];}
  private function ebay_deletion_compliance_complete(){return true;}
  private function ebay_run_new_uuid(){static $i=0;return 'integration-run-'.++$i;}
  private function ebay_selection_scope_for_enabled_routes($scope,$settings){return 'business';}
  private function ebay_run_settings_snapshot($settings){return $settings;}
  private function ebay_run_effective_settings($run){return $this->ebay_settings();}
  private function ebay_run_progress_contract_version(){return self::EBAY_PROGRESS_CONTRACT_VERSION;}
  private function ebay_run_selection_prepare_guard_active($run){return false;}
  private function ebay_run_selection_prepare_regression($before,$after){return false;}
  private function ebay_run_dispatch_self_drive($uuid,$reason=''){++$this->dispatches;return true;}
  private function ebay_public_checkpoint_bootstrap($settings){return ['status'=>'safe','checkpoint_id'=>'initial-safe','business_campaign_ids'=>[501],'private_listing_ids'=>[]];}
  private function ebay_public_checkpoint_business_ids($cp=null){return (array)($cp['business_campaign_ids']??[501]);}
  private function ebay_public_checkpoint_private_ids($cp=null){return (array)($cp['private_listing_ids']??[]);}
  private function advance($phase,$work){$r=$this->ebay_run_load();$r['phase_state']['simulated_external'][$phase]=$work;$this->ebay_run_save($r);$this->phase_calls[]=$phase;$this->ebay_run_set_phase($phase==='checkpoint_cleanup_business'?'completed':$phase,'simulated_external_phase');}
  private function ebay_run_tick_reconcile($r,$settings){$this->advance('refresh_remote',['local_items'=>2]);}
  private function ebay_run_tick_remote($r,$settings){$this->advance('selection_prepare',['ebay_queries'=>2,'received'=>2]);}
  private function ebay_run_tick_selection($r,$settings){$next=['selection_prepare'=>'business_select','business_select'=>'business_materialize','business_materialize'=>'coverage_verify'][$r['phase']]??'coverage_verify';$this->advance($next,['candidates'=>2,'safely_selected'=>1]);}
  private function ebay_run_tick_coverage($r,$settings){$this->advance('gapfill_discovery',['covered'=>1,'missing'=>1,'excluded_non_goods'=>26]);}
  private function ebay_run_tick_gapfill($r,$settings){$this->advance('gapfill_select',['retries'=>1,'no_infinite_search'=>1]);}
  private function ebay_run_tick_gapfill_select($r,$settings){$this->advance('public_verify',['safe_candidate_ids'=>[501],'unverified_candidate_ids'=>[502]]);}
  private function ebay_run_tick_public_verify($r,$settings){$this->items['good']['verified']=1;$this->items['good']['visible']=1;$this->items['bad']['visible']=0;$this->ebay_run_set_phase('checkpoint_cleanup_business','verification_complete');}
  private function ebay_run_tick_checkpoint_cleanup($r,$settings,$route){$this->ebay_run_complete(['simulated_public_good'=>1,'simulated_public_bad'=>0]);}
}
function truth($c,$m){if(!$c){fwrite(STDERR,"FAIL: $m\n");exit(1);}echo "PASS: $m\n";}
$x=new IntegratedRun();$s=$x->start();truth(($s['status']??'')==='queued','one real canonical run created');$first=$x->state();$id=$first['run_uuid'];truth($first['phase']==='reconcile_local','starts at reconcile_local');
for($i=0;$i<3;$i++){$result=$x->tick();truth(($result['tick_result']??'')==='advanced','real worker ticks early phase '.($i+1));}
$prev=$x->state();$pc=$prev['progress_seq'];$GLOBALS['deny']='ppar_ebay_run_state_v1';$blocked=$x->store(array_merge($prev,['progress_seq'=>$pc+11]));truth($blocked===false && $x->state()['progress_seq']===$pc,'DB state write fails closed without losing cursor');$GLOBALS['deny']='';
$stop=$x->stop();truth(($stop['status']??'')==='stop_requested','operator stop requests same run');$res=$x->tick();truth(($res['tick_result']??'')==='paused','stop acknowledged at package edge');$at_pause=$x->state();truth($at_pause['run_uuid']===$id && $at_pause['status']==='paused','same UUID and cursor at pause');
$continue=$x->resume();truth(($continue['status']??'')==='resumed','same run resumed');truth($x->state()['run_uuid']===$id && $x->state()['progress_seq']===$at_pause['progress_seq'],'no restart or cursor reset after resume');
for($i=0;$i<30;$i++){$r=$x->tick();if(($r['tick_result']??'')==='completed')break;if(!in_array($r['tick_result'],['advanced','completed'],true)){throw new Exception('tick stopped '.json_encode($r));}}
truth($x->state()['status']==='completed','real worker dispatcher reaches terminal complete without second run');truth($x->items['good']['visible']===1 && $x->items['bad']['visible']===0,'only verified simulated offer visible');
$events=get_option($x->auditkey($id).'_meta',[]);truth(($events['count']??0)>10,'full sequence in permanent per-run journal');$oldcount=$events['count'];
$new=$x->start();truth(($new['status']??'')==='queued','new run after completed possible');truth($x->state()['run_uuid']!==$id,'new run ID differs');truth((get_option($x->auditkey($id).'_meta',[])['count']??0)>=$oldcount,'old run journal survives a new run');
truth($x->dispatches>=3,'only existing dispatch call used');echo 'INTEGRATED_SCENARIO_PASSED with simulated external WordPress/eBay phases; real canonical dispatcher, save, lease, stop, resume, journal executed.\n';