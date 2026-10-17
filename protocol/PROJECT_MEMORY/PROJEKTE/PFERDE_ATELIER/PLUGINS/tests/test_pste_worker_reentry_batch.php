<?php
error_reporting(E_ALL);
define('ABSPATH','/tmp/');
class PSTE_Plugin { public static function assertReady():void{} public static function isReady():bool{return true;} }
class PSTE_Semantic_Review_Sandbox {
    public static array $rows=[], $events=[];
    public static bool $remaining=false;
    public static function refreshInternalStructureBacklog(bool $x):array{return ['status'=>'SKIPPED'];}
    public static function automaticReentryEnvelopes(int $n):array{return $n===1?[]:self::$rows;}
    public static function markNormalReentryFailed(string $id,string $hash,string $error):array{
        self::$events[]=['failed',$id,$error];
        if($id==='db_bad_mark')throw new RuntimeException('PSTE_STORED_MARK_FAILED');
        return ['status'=>'REVIEW_REQUIRED'];
    }
    public static function markNormalReentryApplied(string $id,string $hash,array $r):array{
        self::$events[]=['applied',$id];
        if($id==='mark_bad')throw new RuntimeException('PSTE_STORED_APPLIED_MARK_FAILED');
        return ['status'=>'APPLIED'];
    }
}
class PSTE_Sandbox_Maintenance_Health {
    public static array $events=[];
    public static function recordAttempt(string $trigger):void{self::$events[]=['attempt',$trigger];}
    public static function recordSuccess(string $trigger,array $report):void{self::$events[]=['success',$trigger,$report];}
    public static function recordFailure(string $trigger,string $code,array $report):void{self::$events[]=['failure',$trigger,$code,$report];}
}
class PSTE_Repository {
    public static array $calls=[];
    public static function applySandboxReentryEnvelope(array $envelope,string $hash):array{
        $id=(string)$envelope['pool_key'];self::$calls[]=$id;
        if(str_starts_with($id,'db_bad'))throw new RuntimeException('PSTE_DB_SIMULATED_FAILURE');
        return ['status'=>'PASS','pool_key'=>$id];
    }
}
require (getenv('PSTE_SOURCE_DIR')?:'/mnt/data/seo_work/modified/Portal SEO Topic Engine').'/includes/class-pste-normal-reentry-coordinator.php';
foreach(['first_good','checkpoint_bad','db_bad_mark','second_good','mark_bad','third_good'] as $id){
    PSTE_Semantic_Review_Sandbox::$rows[]=['sandbox_id'=>$id,'envelope'=>['pool_key'=>$id],'envelope_sha256'=>str_repeat('a',64),'checkpoint_error_code'=>$id==='checkpoint_bad'?'PSTE_SANDBOX_REENTRY_WORKER_CHECKPOINT_INVALID':''];
}
$result=PSTE_Normal_Reentry_Coordinator::processProviderFreeExistingPotentialBatch(25);
function check($condition,$message){if(!$condition)throw new RuntimeException($message);}
check($result['status']==='PARTIAL_FAILURE','partial error falsely reported PASS');
check($result['reentry_checked']===6,'not all 6 processed');
check($result['reentry_applied']===3,'should apply first_good,second_good,third_good');
check($result['reentry_failed']===3,'should fail checkpoint_bad,db_bad_mark,mark_bad');
check(!in_array('checkpoint_bad',PSTE_Repository::$calls,true),'checkpoint mismatch reached DB');
check(in_array('third_good',PSTE_Repository::$calls,true),'later keyword not processed after prior errors');
check(count(array_filter($result['reentry_failures'],fn($e)=>$e['stage']==='SANDBOX_FAIL_MARK_PENDING_REVIEW'))===1,'failed marking not isolated');
check(count(array_filter($result['reentry_failures'],fn($e)=>$e['stage']==='SANDBOX_MARK_PENDING_RETRY'))===1,'applied marking failure not reported');
check($result['provider_calls']===0&&!$result['production_handoff_created_by_sandbox']&&!$result['article_or_taxonomy_write_attempted_by_sandbox'],'safety boundary');
PSTE_Normal_Reentry_Coordinator::processCron();
$reasons=array_map(fn($e)=>$e[2]??'',array_filter(PSTE_Sandbox_Maintenance_Health::$events,fn($e)=>$e[0]==='failure'));
check(in_array('PSTE_SANDBOX_REENTRY_PARTIAL_FAILURE',$reasons,true),'cron falsely marked partial failures as success');
// Positive control: a completely successful batch must still finish green.
PSTE_Semantic_Review_Sandbox::$rows=[['sandbox_id'=>'healthy','envelope'=>['pool_key'=>'healthy'],'envelope_sha256'=>str_repeat('a',64),'checkpoint_error_code'=>'']];
$healthy=PSTE_Normal_Reentry_Coordinator::processProviderFreeExistingPotentialBatch(25);
check($healthy['status']==='PASS'&&$healthy['reentry_applied']===1&&$healthy['reentry_failed']===0,'healthy batch regressed');
PSTE_Normal_Reentry_Coordinator::processCron();
check(count(array_filter(PSTE_Sandbox_Maintenance_Health::$events,fn($e)=>$e[0]==='success'))===1,'healthy batch cron did not succeed');
echo json_encode(['result'=>'PASS','checked'=>$result['reentry_checked'],'applied'=>$result['reentry_applied'],'failed'=>$result['reentry_failed'],'warnings'=>count($result['reentry_failures']),'later_processed'=>in_array('third_good',PSTE_Repository::$calls,true),'checkpoint_rejected_before_db'=>!in_array('checkpoint_bad',PSTE_Repository::$calls,true),'provider_calls'=>0],JSON_PRETTY_PRINT)."\n";