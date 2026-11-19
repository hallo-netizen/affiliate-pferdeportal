<?php
// Reproduce actual PPAR_Ebay_Run_Trait::handle_ebay_external_tick.
// The surrounding WordPress state and eBay requests are deliberately mocked;
// this is NOT a WordPress/MariaDB/eBay live end-to-end test.
error_reporting(E_ALL);
define('ABSPATH','/tmp/');
function sanitize_key($s){return preg_replace('/[^a-z0-9_\-]/','',strtolower((string)$s));}
function sanitize_text_field($s){return (string)$s;}
function absint($n){return abs((int)$n);}
function is_wp_error($v){return false;}
require $argv[1];
class QA16Test {
  use PPAR_Ebay_Run_Trait;
  private $state;
  public $availability_calls=0;
  public $worker_calls=0;
  public $dispatcher_calls=0;
  public $start_calls=0;
  private $settings_enabled=true;
  public function __construct($state,$enabled=true){$this->state=$state;$this->settings_enabled=$enabled;}
  private function ebay_external_tick_admit(){return true;}
  private function ebay_settings(){return ['enabled'=>$this->settings_enabled];}
  private function ebay_run_load(){return $this->state;}
  private function ebay_run_is_active($state=null){$state=$state?:$this->state;return ($state['status']??'')==='running';}
  private function ebay_external_tick_due_operation($settings){return '';}
  private function ebay_run_dispatch_self_drive($run,$reason){$this->dispatcher_calls++;return true;}
  public function ebay_public_availability_tick($continuation=''){$this->availability_calls++;if($continuation!=='heartbeat')throw new Exception('Wrong continuation');return ['status'=>'not_due'];}
  public function run_ebay_canonical_worker(){$this->worker_calls++;return ['tick_result'=>'advanced','progress_before'=>3,'progress_after'=>4];}
}
$base=['schema'=>'1.0','run_uuid'=>'qa16-existing-run','phase'=>'business_select','progress_seq'=>4,'transport_tick_count'=>8];
$tests=[
 ['running',array_merge($base,['status'=>'running']),'advanced',1,1],
 ['paused',array_merge($base,['status'=>'paused','resume_reason'=>'operator_stop']),'idle',1,0],
 ['failed',array_merge($base,['status'=>'failed','phase'=>'public_verify','error_code'=>'public_source_refresh_provider_failed']),'failed',1,0],
 ['completed',array_merge($base,['status'=>'completed','phase'=>'completed']),'idle',1,0],
 ['fresh_idle',[],'idle',1,0],
 ['stale_recovery',array_merge($base,['status'=>'running','resume_reason'=>'business_gap_proof_recovery']),'idle',0,0],
];
$failed=0;
foreach($tests as [$name,$state,$expected_status,$availability,$workers]) {
 $test=new QA16Test($state);
 $request=$name==='stale_recovery'?['recovery_run'=>'another-run']:[];
 $result=$test->handle_ebay_external_tick($request);
 $ok=($result['status']===$expected_status && $test->availability_calls===$availability && $test->worker_calls===$workers);
 if ($name==='paused')$ok=$ok && ($result['availability_status']??null)==='not_due';
 if ($name==='running')$ok=$ok && $test->dispatcher_calls===1;
 printf("%s status=%s availability=%d worker=%d dispatch=%d expected=%d/%d %s\n",$name,$result['status'],$test->availability_calls,$test->worker_calls,$test->dispatcher_calls,$availability,$workers,$ok?'PASS':'FAIL');
 if(!$ok)$failed++;
}
$test=new QA16Test(array_merge($base,['status'=>'running']),false);
$result=$test->handle_ebay_external_tick([]);
$ok=$result['status']==='disabled' && $test->availability_calls===0;
printf("disabled availability=%d %s\n",$test->availability_calls,$ok?'PASS':'FAIL');
if(!$ok)$failed++;
printf("TOTAL 7 FAILED %d\n",$failed);
exit($failed?1:0);