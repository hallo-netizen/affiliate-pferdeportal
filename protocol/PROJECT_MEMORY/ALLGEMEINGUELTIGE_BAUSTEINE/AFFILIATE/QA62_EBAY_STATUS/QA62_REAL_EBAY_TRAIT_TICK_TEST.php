<?php
// QA62: executes the actual production trait; only WordPress storage and
// the single canonical worker's return are simulated. No eBay API is called.
define('ABSPATH', __DIR__ . '/');
define('HOUR_IN_SECONDS',3600);
function sanitize_key($s){return preg_replace('/[^a-z0-9_-]/','',strtolower((string)$s));}
function sanitize_text_field($s){return trim(strip_tags((string)$s));}
function absint($v){return abs((int)$v);}
function is_wp_error($x){return $x instanceof WP_Error;}
class WP_Error extends Exception {
    private $wp_code='';
    public function __construct($code, $message='') { $this->wp_code=(string)$code;parent::__construct($message); }
    public function get_error_code(){return $this->wp_code;}
    public function get_error_message(){return $this->getMessage();}
}
$GLOBALS['qa62_storage']=[];
function get_option($k,$d=false){return $GLOBALS['qa62_storage'][$k]??$d;}
function update_option($k,$v,$autoload=false){$GLOBALS['qa62_storage'][$k]=$v;return true;}
function add_option($k,$v,$deprecated='',$autoload=false){if(array_key_exists($k,$GLOBALS['qa62_storage']))return false;$GLOBALS['qa62_storage'][$k]=$v;return true;}
function delete_option($k){unset($GLOBALS['qa62_storage'][$k]);return true;}
function rest_ensure_response($x){return $x;}
require $argv[1];
class QA62Runner {
  use PPAR_Ebay_Run_Trait;
  const OPTION_EBAY_EXTERNAL_TICK_RATE_LOCK='qa62_rate';
  const OPTION_EBAY_RUN_STATE='qa62_run';
  const VERSION='qa62-production-trait-test';
  public $workerCalls=0,$startCalls=0,$due='',$reply='advanced',$after=null;
  private function ebay_settings(){return ['enabled'=>true,'last_sync'=>['finished_at'=>time()],'last_refresh'=>['finished_at'=>time()]];}
  private function ebay_external_tick_due_operation($settings){return $this->due;}
  private function ebay_run_resume_failed_family_cap($run){return $run;}
  private function ebay_run_start($manual=false,$operation='sync'){
    $this->startCalls++;
    $GLOBALS['qa62_storage']['qa62_run']=['schema'=>'1.0','status'=>'running','phase'=>'reconcile_local','run_uuid'=>'new-from-start','progress_seq'=>0];
    return ['status'=>'queued'];
  }
  public function run_ebay_canonical_worker(){
    $this->workerCalls++;
    if($this->after!==null)$GLOBALS['qa62_storage']['qa62_run']=$this->after;
    return ['tick_result'=>$this->reply,'reason'=>'test_worker','progress_before'=>5,'progress_after'=>6];
  }
  public function tick(){return $this->handle_ebay_external_tick([]);}
}
function run_case($name,$run,$due,$reply,$after=null){
  $GLOBALS['qa62_storage']=['qa62_run'=>$run,'qa62_safe_public'=>['checkpoint_id'=>'safe-578','ids'=>[1,2,3]]];
  $x=new QA62Runner();$x->due=$due;$x->reply=$reply;$x->after=$after;
  $out=$x->tick();
  return ['name'=>$name,'response'=>is_wp_error($out)?['WP_ERROR'=>$out->get_error_code()]:$out,
    'worker_calls'=>$x->workerCalls,'new_run_calls'=>$x->startCalls,
    'saved_run'=>$GLOBALS['qa62_storage']['qa62_run'],
    'old_safe_untouched'=>$GLOBALS['qa62_storage']['qa62_safe_public']===['checkpoint_id'=>'safe-578','ids'=>[1,2,3]]];
}
$r=['schema'=>'1.0','status'=>'running','phase'=>'gapfill_discovery','run_uuid'=>'97507628-4f4','progress_seq'=>475,'resume_reason'=>''];
$results=[
 run_case('real_running_advanced',$r,'sync','advanced'),
 run_case('real_running_wrong_worker_idle',$r,'sync','idle'),
 run_case('real_running_wrong_worker_completed',$r,'sync','completed'),
 run_case('real_running_worker_failed_unstored',$r,'sync','failed'),
 run_case('saved_incoherent_running_terminal_phase',array_merge($r,['phase'=>'completed']),'sync','advanced'),
 run_case('saved_invalid_schema_running',array_merge($r,['schema'=>'old-0.9']),'sync','advanced'),
 run_case('paused_by_operator',array_merge($r,['status'=>'paused','resume_reason'=>'operator_stop']),'sync','advanced'),
 run_case('paused_by_system',array_merge($r,['status'=>'paused','resume_reason'=>'pending_work','resume_at'=>time()+300]),'sync','busy'),
 run_case('old_failed_not_restarted',array_merge($r,['status'=>'failed','phase'=>'failed','error_code'=>'provider_failure']),'sync','advanced'),
 run_case('completed_not_yet_due',array_merge($r,['status'=>'completed','phase'=>'completed']),'','advanced'),
 run_case('completed_now_due',array_merge($r,['status'=>'completed','phase'=>'completed']),'sync','advanced'),
 run_case('empty_run_no_due',[],'','advanced'),
 run_case('bad_status_no_auto_overwrite',array_merge($r,['status'=>'broken']),'sync','advanced'),
 run_case('worker_state_regresses', $r,'sync','advanced',array_merge($r,['status'=>'running','phase'=>'failed'])),
 run_case('worker_finishes', $r,'sync','completed',array_merge($r,['status'=>'completed','phase'=>'completed'])),
 run_case('worker_fails_safely', $r,'sync','failed',array_merge($r,['status'=>'failed','phase'=>'failed'])),
 ];
foreach($results as $row)echo json_encode($row,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";