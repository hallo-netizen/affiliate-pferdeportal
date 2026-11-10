<?php
/* Reproduce/compare the REAL external heartbeat handler in QA7 vs the isolated edit. */
define('ABSPATH','/tmp/');
function sanitize_key($value){return preg_replace('/[^a-z0-9_-]/','',strtolower((string)$value));}
function sanitize_text_field($value){return (string)$value;}
function absint($value){return abs((int)$value);}
function nocache_headers(){}
$source=$argv[1]??'';
if(!is_file($source)){fwrite(STDERR,"Source not found\n");exit(2);}
require $source;
class TestWorker {
    use PPAR_Ebay_Run_Trait;
    public $run = [];
    public $worker_result = [];
    public $self_drive_count = 0;
    private function ebay_external_tick_admit(){return true;}
    private function ebay_settings(){return ['enabled'=>true];}
    private function ebay_run_load(){return $this->run;}
    public function run_ebay_canonical_worker(){return $this->worker_result;}
    private function ebay_run_dispatch_self_drive($uuid,$reason=''){ $this->self_drive_count++;return true; }
}
function run_probe($status,$reason,$result){
    $x=new TestWorker();
    $x->run=['schema'=>'1.0','run_uuid'=>'known-run-uuid','status'=>$status,'phase'=>'gapfill_select','resume_reason'=>$reason,'progress_seq'=>774,'transport_tick_count'=>771];
    $x->worker_result=['tick_result'=>$result,'reason'=> $result==='paused'?'operator_paused':'progress','progress_before'=>774,'progress_after'=>774];
    $out=$x->handle_ebay_external_tick([]);
    return ['status'=>$out['status']??'', 'run_status'=>$out['run_status']??'', 'reason'=>$out['reason']??'', 'phase'=>$out['phase']??'', 'self_drive_handoff'=>$out['self_drive_handoff']??null, 'actual_dispatches'=>$x->self_drive_count, 'progress_seq'=>$out['progress_seq']??-1, 'contract'=>$out['contract']??''];
}
$result=[
  'paused_manual'=>run_probe('paused','operator_stop','paused'),
  'running_advanced'=>run_probe('running','','advanced'),
  'running_retryable_error'=>run_probe('running','','retryable_error'),
  'running_busy'=>run_probe('running','','busy'),
  'running_local_checked'=>run_probe('running','','local_checked'),
];
echo json_encode($result,JSON_PRETTY_PRINT|JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE),"\n";
