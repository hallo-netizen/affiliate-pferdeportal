<?php
/** Execute exact plugin due selector from original PHP trait, with saved WP storage simulated. */
error_reporting(E_ALL & ~E_DEPRECATED);
define('ABSPATH',__DIR__.'/');define('HOUR_IN_SECONDS',3600);define('MINUTE_IN_SECONDS',60);
function sanitize_key($v){return preg_replace('/[^a-z0-9_-]/','',strtolower((string)$v));}
function absint($v){return abs((int)$v);}
require $argv[1];
class Due63 {
 use PPAR_Ebay_Run_Trait;
 private $settings,$run;
 function __construct($run,$settings){$this->run=$run;$this->settings=$settings;}
 private function ebay_run_load(){return $this->run;}
 private function ebay_settings(){return $this->settings;}
 function next(){return $this->ebay_external_tick_due_operation($this->settings);}
}
$now=time();
$run=function($op,$age,$state='completed')use($now){return ['schema'=>'1.0','status'=>$state,'phase'=>$state,'operation'=>$op,'finished_at'=>$now-$age,'run_uuid'=>'same-run'];};
$settings=function($sync_age,$refresh_age,$on=true,$inventory=false)use($now){return ['enabled'=>$on,'inventory_refresh_enabled'=>$inventory,'last_sync'=>['finished_at'=>$now-$sync_age],'last_refresh'=>['finished_at'=>$now-$refresh_age]];};
$cases=[
 ['long-run-just-completed',$run('sync',60),$settings(7*3600,120), ''],
 ['three-hours-after-canonical-end',$run('sync',3*3600+60),$settings(60,120),'sync'],
 ['full-ended-near-threshold',$run('sync',3*3600-60),$settings(9*3600,120),''],
 ['refresh-due-after-long-full',$run('sync',50),$settings(8*3600,2*3600,true,true),'refresh'],
 ['no-double-refresh-just-completed',$run('refresh',60),$settings(300,2*3600,true,true),''],
 ['full-sync-due-even-after-refresh',$run('refresh',60),$settings(5*3600,2*3600,true,true),'sync'],
 ['gapfill-not-full-sync',$run('gaps',60),$settings(5*3600,2*3600),'sync'],
 ['old-terminal-migration-no-full-cycle',[], $settings(5*3600,2*3600),'sync'],
 ['disabled',$run('sync',9*3600),$settings(9*3600,2*3600,false,true),''],
 ['completed-now-even-if-nested-sync-future',$run('sync',60),$settings(-2400,120),''],
 ['completed-full-3h-even-if-nested-sync-recent',$run('sync',3*3600+60),$settings(60,120),'sync'],
];
$failed=0;
foreach($cases as [$name,$run,$s,$expected]){
 $d=new Due63($run,$s);$got=$d->next();$ok=$got===$expected;$failed+=!$ok;
 echo json_encode(['name'=>$name,'expected'=>$expected,'got'=>$got,'pass'=>$ok],JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";
}
fprintf(STDERR,"DUE_CONTRACT %d/%d PASS\n",count($cases)-$failed,count($cases));exit($failed>0?1:0);