<?php
/** One-time bounded QA of existing PSERC 0.28.55 real compiler class.
 * php this.php /path/to/extracted/portal-seo-editorial-plan-compiler
 * No WordPress, no K0, no new runtime worker; isolated WP/DB mocks.
 */
declare(strict_types=1);
define('ABSPATH','/qa/');
$root=rtrim((string)($argv[1]??''),'/').'/';
$path=$root.'includes/class-pserc-plan-compile-job.php';
if(!is_file($path))throw new RuntimeException('ORIGINAL_PSERC_REAL_CLASS_REQUIRED');
final class PSERC_Plan_Snapshot_Store {
    public static array $records=[];
    public static int $namedReads=0;
    public static function getRecord($gen,$kind,$idx){return self::$records[$kind][$idx]??null;}
    public static function putRecord($gen,$kind,$idx,$record){self::$records[$kind][$idx]=$record;}
    public static function deleteRecord($gen,$kind,$idx){unset(self::$records[$kind][$idx]);}
    public static function nextCandidateIndex($gen,$cursor){return ['source_seq'=>0,'priority_score'=>2.0,'cursor'=>['id'=>42]];}
    public static function getNamed($gen,$a,$b){self::$namedReads++;return null;}
}
final class PSERC_Technical_Strand {
    public static function evaluate($topic,$production,$structure,$baseline){
        return ['ok'=>true,'target_keyword_gate'=>['status'=>'PASS']];
    }
}
final class PSERC_Editorial_Strand {
    public static function evaluate($topic){return ['ok'=>true,'editorial_outcome_gate'=>['status'=>'PASS']];}
}
final class PSERC_Semantic_Duplicate_Gate {
    public static int $scans=0;
    public static int $finalizations=0;
    public static function projectTopic($topic){return ['family'=>'horseware','family_tokens'=>['horseware']];}
    public static function newAggregateState($scope){return ['decision'=>'PASS','scope'=>$scope];}
    public static function finalizeAggregateState($aggregate){self::$finalizations++;return ['decision'=>'PASS','reason_codes'=>[]];}
    public static function scanExistingProjectedChunk(...$args){self::$scans++;return [];}
    public static function scanPreparedProjectedChunk(...$args){self::$scans++;return [];}
    public static function familyBucketForProjection($projection){return 'horseware-1';}
}
final class PSERC_Portal_Topic_Evidence_Gate {
    public static function evaluate($topic,$structure){return ['ok'=>true];}
}
final class PSERC_Compiler {
    public static function evidenceView($topic){return [];}
}
require $path;
$gen='abcdefghijklmnopqrst';
$topic=[
    'pool_key'=>'horseware-qa-1','priority_score'=>2.0,
    'title'=>'Horseware Regendecken',
    'single_external_seo_owner_receipt'=>[
        'contract'=>'PSTE_MINI_SEO_DECISIONS_V1','box'=>'FREI'],
];
PSERC_Plan_Snapshot_Store::putRecord($gen,'eligible',0,
    ['topic'=>$topic,'structure'=>[],'baseline'=>[]]);
PSERC_Plan_Snapshot_Store::putRecord($gen,'bootstrap',0,['production'=>[]]);
$job=[
    'generation'=>$gen,'candidate_index'=>0,'eligible_count'=>1,
    'candidate_sort_cursor'=>null,'prepared_count'=>0,
    'prepared_families'=>[],'existing_families'=>[],
];
$method=(new ReflectionClass(PSERC_Plan_Compile_Job::class))->getMethod('tickCandidate');
[$job,$reads,$writes,$bytes]=$method->invoke(null,$job);
$work=PSERC_Plan_Snapshot_Store::getRecord($gen,'candidate_work',0);
if(($work['stage']??'')!=='PREPARED'||($work['buckets']??null)!==[]
    ||$reads!==2||$writes!==1)
    throw new RuntimeException('FAIL first bounded candidate tick');
echo "PASS existing first PSERC tick: PREPARED, zero content buckets\n";
[$job,$reads,$writes,$bytes]=$method->invoke(null,$job);
if($job['prepared_count']!==1||$job['candidate_index']!==1
    ||PSERC_Semantic_Duplicate_Gate::$scans!==0
    ||PSERC_Plan_Snapshot_Store::$namedReads!==0
    ||PSERC_Plan_Snapshot_Store::getRecord($gen,'candidate_work',0)!==null)
    throw new RuntimeException('FAIL second bounded candidate tick');
echo "PASS second PSERC tick: one prepared, zero semantic scans / duplicate lookups\n";
[$job,$reads,$writes,$bytes]=$method->invoke(null,$job);
if(($job['phase']??'')!=='SLOT'||$job['prepared_count']!==1)
    throw new RuntimeException('FAIL existing slot stage was not reached');
echo "PASS third PSERC tick: existing SLOT phase, no new reviewer\n";
echo "PSERC_REAL_EXISTING_THREE_TICK_QA_PASS; MOCK STORE; NO WORDPRESS/K0 END-TO-END\n";
