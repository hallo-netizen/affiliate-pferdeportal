<?php
if ($argc!==2) {exit(2);} define('ABSPATH','/tmp/');
$GLOBALS['wp_options']=[];
function get_option($name,$default=[]){return $GLOBALS['wp_options'][$name]??$default;}
function sanitize_key($str){return preg_replace('/[^a-z0-9_-]/','',strtolower((string)$str));}
function absint($value){return abs((int)$value);}
require $argv[1];
class QA6Probe { use PPAR_Ebay_Run_Trait; const EBAY_RUNTIME_BUILD='6.72.319'; }
$o=new QA6Probe();$load=new ReflectionMethod(QA6Probe::class,'ebay_run_phase_state_load');
$scenarios=[
  'missing'=>[],
  'legacy'=>['schema'=>'0.9','status'=>'running','phase_state'=>['selection'=>['marker'=>'legacy']]],
  'running'=>['schema'=>'1.0','status'=>'running','phase'=>'business_select','phase_state'=>['selection'=>['marker'=>'run']]],
  'paused'=>['schema'=>'1.0','status'=>'paused','phase'=>'business_select','phase_state'=>['selection'=>['marker'=>'pause']]],
  'failed'=>['schema'=>'1.0','status'=>'failed','phase'=>'failed','phase_state'=>['selection'=>['marker'=>'fail']]],
  'completed'=>['schema'=>'1.0','status'=>'completed','phase'=>'completed','phase_state'=>['selection'=>['marker'=>'done']]],
  'malformed-phase'=>['schema'=>'1.0','status'=>'running','phase_state'=>['selection'=>'invalid']],
];
$out=[];
foreach($scenarios as $key=>$state){$GLOBALS['wp_options']=['ppar_ebay_run_state_v1'=>$state];$out[$key]=$load->invoke($o,'selection');}
echo json_encode($out,JSON_UNESCAPED_UNICODE|JSON_PRETTY_PRINT);