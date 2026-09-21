<?php
$uuid=(string)get_option('pste_e2e_single_job_uuid','');
if($uuid==='')throw new RuntimeException('SINGLE_UUID_MISSING');
$driver=PSTE_Research_Driver::status();
$active=PSTE_Research_Job::peek();
$run=PSTE_Repository::runByUuid($uuid);
$counts=get_option('pste_e2e_provider_counts',[]);
if(!is_array($run))throw new RuntimeException('RUN_MISSING');
if(is_array($active))throw new RuntimeException('ACTIVE_JOB_STILL_PRESENT');
if((string)($driver['status']??'')!=='IDLE')throw new RuntimeException('DRIVER_NOT_IDLE_'.($driver['health_code']??''));
if((string)($run['status']??'')!=='ANALYZED' && (string)($run['status']??'')!=='ANALYZED_NO_ELIGIBLE_CANDIDATE')throw new RuntimeException('RUN_NOT_TERMINAL_'.($run['status']??''));
foreach(['/v3/dataforseo_labs/google/keyword_suggestions/live','/v3/dataforseo_labs/google/related_keywords/live','/v3/dataforseo_labs/google/keyword_ideas/live','/v3/serp/google/organic/task_post','/v3/serp/google/organic/tasks_ready'] as $p){
    if((int)($counts[$p]??0)<1)throw new RuntimeException('PROVIDER_PATH_MISSING_'.$p);
}
$getCount=0;foreach($counts as $p=>$n)if(str_contains((string)$p,'/task_get/advanced/'))$getCount+=(int)$n;
if($getCount<1)throw new RuntimeException('PAA_GET_MISSING');
echo wp_json_encode([
 'status'=>'PASS_REAL_WORDPRESS_SINGLE',
 'run_status'=>$run['status'],
 'candidate_count'=>(int)($run['payload']['candidate_count']??0),
 'usable_candidate_count'=>(int)($run['payload']['usable_candidate_count']??0),
 'driver'=>$driver,
 'provider_counts'=>$counts
],JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";
