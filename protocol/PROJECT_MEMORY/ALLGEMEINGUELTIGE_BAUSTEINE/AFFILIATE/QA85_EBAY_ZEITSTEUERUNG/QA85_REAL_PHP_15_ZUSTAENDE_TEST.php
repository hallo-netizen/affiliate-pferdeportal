<?php
// Invokes the ACTUAL eBay external heartbeat trait from $argv[1].
// Only unavailable WordPress storage and provider responses are mocked.
define('ABSPATH', __DIR__.'/'); define('HOUR_IN_SECONDS',3600);
function sanitize_key($s){return preg_replace('/[^a-z0-9_-]/','',strtolower((string)$s));}
function sanitize_text_field($s){return trim(strip_tags((string)$s));}
function absint($v){return abs((int)$v);} function is_wp_error($v){return $v instanceof WP_Error;}
class WP_Error extends Exception {private $c;function __construct($c,$m=''){$this->c=$c;parent::__construct($m);}function get_error_code(){return $this->c;}}
$GLOBALS['db']=[];
function get_option($k,$d=false){return $GLOBALS['db'][$k]??$d;}
function update_option($k,$v,$autoload=false){$GLOBALS['db'][$k]=$v;return true;}
function add_option($k,$v,$d='',$a=false){if(isset($GLOBALS['db'][$k]))return false;$GLOBALS['db'][$k]=$v;return true;}
function delete_option($k){unset($GLOBALS['db'][$k]);return true;}
function rest_ensure_response($a){return $a;}
require $argv[1];
class Harness {use PPAR_Ebay_Run_Trait;
 const OPTION_EBAY_EXTERNAL_TICK_RATE_LOCK='rate';const OPTION_EBAY_RUN_STATE='run';const VERSION='test';
 public $called=0,$worker=0,$start=0,$availability_return='continuing',$worker_ends='';
 private function ebay_settings(){return ['enabled'=>true,'business_enabled'=>true,'inventory_refresh_enabled'=>true,'last_sync'=>['finished_at'=>time()],'last_refresh'=>['finished_at'=>time()]];}
 private function ebay_external_tick_due_operation($settings){return '';}
 private function ebay_run_resume_failed_family_cap($r){return $r;}
 private function ebay_run_start($a=false,$b='sync'){++$this->start;return ['status'=>'queued'];}
 public function run_ebay_canonical_worker(){++$this->worker;if($this->worker_ends!==''){$r=get_option('run',[]);$r['status']=$this->worker_ends;$r['phase']=$this->worker_ends;update_option('run',$r);return ['tick_result'=>$this->worker_ends];}return ['tick_result'=>'advanced'];}
 public function ebay_public_availability_tick($continuation=''){
   ++$this->called;
   $a=get_option('ppar_ebay_public_availability_state_v1',[]);
   $a['running']=$this->availability_return==='complete'?0:1;
   $a['next_due_at']=time()+($this->availability_return==='complete'?7200:90);
   update_option('ppar_ebay_public_availability_state_v1',$a);
   return ['status'=>$this->availability_return,'checked'=>1];
 }
 public function tick(){return $this->handle_ebay_external_tick([]);}
}
function testcase($name,$state,$due,$running,$expect,$calls,$worker,$completed=false){
 $GLOBALS['db']=['run'=>['schema'=>'1.0','run_uuid'=>'persisted-id','status'=>$state,'phase'=>$state==='completed'?'completed':($state==='failed'?'failed':'gapfill_discovery'),'resume_reason'=>$state==='paused'?'operator_stop':'','error_code'=>$state==='failed'?'original_error':''],
 'safe'=>['ids'=>[101,102,103]],
 'ppar_ebay_public_availability_state_v1'=>['running'=>$running?1:0,'next_due_at'=>$due?0:time()+90]];
 $h=new Harness();if($completed)$h->availability_return='complete';
 $result=$h->tick();$status=$result instanceof WP_Error?'ERR':($result['status']??'ERR');
 $same=$GLOBALS['db']['run']['run_uuid']==='persisted-id'&&$GLOBALS['db']['safe']['ids']===[101,102,103];
 $ok=$status===$expect&&$h->called===$calls&&$h->worker===$worker&&$h->start===0&&$same;
 return ['name'=>$name,'status'=>$status,'expected'=>$expect,'availability_calls'=>$h->called,'canonical_calls'=>$h->worker,'preserved'=>$same,'pass'=>$ok];
}
$c=[
 testcase('completed_due_running','completed',true,true,'advanced',1,0),
 testcase('completed_waiting_90s','completed',false,true,'advanced',0,0),
 testcase('paused_due_running','paused',true,true,'advanced',1,0),
 testcase('failed_due_running','failed',true,true,'advanced',1,0),
 testcase('paused_waiting_90s','paused',false,true,'advanced',0,0),
 testcase('failed_waiting_90s','failed',false,true,'advanced',0,0),
 testcase('completed_finished_availability','completed',true,true,'idle',1,0,true),
 testcase('completed_no_pending','completed',false,false,'idle',0,0),
 testcase('paused_no_pending','paused',false,false,'idle',0,0),
 testcase('failed_no_pending','failed',false,false,'failed',0,0),
 testcase('active_due','running',true,true,'advanced',1,0),
 testcase('active_waiting','running',false,true,'advanced',0,1),
];
// Cross-lane transition: a canonical worker FINISHES on this tick, while
// the previously saved availability cursor still has 90s of pending work.
foreach ([['completed',true,'advanced'],['completed',false,'completed'],['failed',true,'failed']] as $data) {
  [$terminal,$pending,$expected]=$data;
  $GLOBALS['db']=['run'=>['schema'=>'1.0','run_uuid'=>'persisted-id','status'=>'running','phase'=>'gapfill_discovery'],
   'safe'=>['ids'=>[101,102,103]],
   'ppar_ebay_public_availability_state_v1'=>['running'=>$pending?1:0,'next_due_at'=>time()+90]];
  $t=new Harness();$t->worker_ends=$terminal;
  $res=$t->tick();$status=$res instanceof WP_Error?'ERR':($res['status']??'ERR');
  $same=($GLOBALS['db']['run']['run_uuid']??'')==='persisted-id'&&$GLOBALS['db']['safe']['ids']===[101,102,103];
  $c[]=['name'=>'worker_finishes_'.$terminal.'_availability_'.($pending?'pending':'clear'),
    'status'=>$status,'expected'=>$expected,'availability_calls'=>$t->called,'canonical_calls'=>$t->worker,
    'preserved'=>$same,'pass'=>$status===$expected&&$t->worker===1&&$same];
}
echo json_encode(['tests'=>count($c),'pass'=>count(array_filter($c,fn($z)=>$z['pass'])),'results'=>$c],JSON_UNESCAPED_UNICODE|JSON_PRETTY_PRINT),"\n";
exit(count(array_filter($c,fn($z)=>$z['pass']))===count($c)?0:1);