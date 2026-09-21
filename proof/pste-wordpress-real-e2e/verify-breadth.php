<?php
$q=PSTE_Breadth_Research_Queue::peek();
if(!is_array($q))throw new RuntimeException('BREADTH_QUEUE_MISSING');
if((string)($q['status']??'')!=='COMPLETE')throw new RuntimeException('BREADTH_NOT_COMPLETE_'.(string)($q['status']??''));
if((string)($q['completion_reason']??'')!=='TARGET_REACHED')throw new RuntimeException('BREADTH_REASON_'.(string)($q['completion_reason']??''));
$usable=(int)($q['usable_candidate_count']??0);
$completed=(int)($q['completed_count']??0);
if($usable<40)throw new RuntimeException('BREADTH_USABLE_LT_40_'.$usable);
if($completed<1)throw new RuntimeException('BREADTH_COMPLETED_ZERO');
$counts=get_option('pste_e2e_provider_counts',[]);
if(!is_array($counts))throw new RuntimeException('PROVIDER_COUNTS_INVALID');
foreach(['/v3/dataforseo_labs/google/keyword_suggestions/live','/v3/dataforseo_labs/google/related_keywords/live','/v3/dataforseo_labs/google/keyword_ideas/live','/v3/serp/google/organic/task_post'] as $p){
    if((int)($counts[$p]??0)!==$completed)throw new RuntimeException('PROVIDER_COUNT_MISMATCH_'.$p.'_'.(int)($counts[$p]??0).'_'.$completed);
}
$get=0;foreach($counts as $p=>$n)if(str_contains((string)$p,'/task_get/advanced/'))$get+=(int)$n;
if($get!==$completed)throw new RuntimeException('PAA_GET_COUNT_MISMATCH_'.$get.'_'.$completed);
echo wp_json_encode(['status'=>'PASS_REAL_WORDPRESS_BREADTH','completion_reason'=>$q['completion_reason'],'families'=>$completed,'usable'=>$usable,'provider_counts'=>$counts],JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";
