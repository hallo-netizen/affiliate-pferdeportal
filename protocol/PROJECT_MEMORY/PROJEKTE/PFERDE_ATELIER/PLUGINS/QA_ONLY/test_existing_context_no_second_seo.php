<?php
declare(strict_types=1);
define('ABSPATH','/qa/');
function qa(bool $ok,string $message):void{if(!$ok)throw new RuntimeException('FAILED '.$message);echo "PASS $message\n";}
final class PSTE_Mini_Workflow {
    public static function isMiniTopicAwaitingSeo(string $poolKey):bool{return $poolKey==='mini-approved';}
}
final class PSTE_Normalizer {
    public static int $similarityCalls=0;
    public static function categoryFamilyKey(string $value):string{return 'regendecken';}
    public static function categoryFamilyName(string $value):string{return $value;}
    public static function categoryArticleType(string $value):string{return 'Beratung';}
    public static function similarity(string $a,string $b):float {self::$similarityCalls++;return 0.88;}
}
require_once $argv[1] ?? throw new RuntimeException('original existing context evaluator source missing');
$payload=[
    'canonical_query'=>'regendecke pferd 0g',
    'topic_family_key'=>'regendecken',
    'reason_codes'=>['ANSWER_EQUIVALENT_PLANNED','CONTEXT_REFRESH_STALE','INDEPENDENT_CATEGORY_REVIEW'],
];
$existing=[
    'title'=>'Regendecke ohne Füllung','status'=>'publish',
    'post_id'=>17,'category_name'=>'Regendecken','category_id'=>55,
    'topic_family_key'=>'regendecken',
    'headings'=>['Ungefütterte Regendecken im Stall'],
];
$inventory=['sha256'=>str_repeat('a',64),'items'=>[$existing]];
$plan=['sha256'=>str_repeat('b',64),'status'=>'AVAILABLE','items'=>[]];
$index=['WORDPRESS'=>['regendecken'=>[$existing]],'EDITORIAL_PLAN'=>[]];

$mini=PSTE_Context_Evaluator::evaluate($payload,$inventory,$plan,$index,'mini-approved');
qa($mini['state']==='CURRENT','existing MINI context source is current');
qa(PSTE_Normalizer::$similarityCalls===0,'ZERO title/heading semantic similarity recheck for external owner');
qa(($mini['payload']['portal_context']['semantic_comparison']??'')==='NOT_RUN_SINGLE_EXTERNAL_SEO_OWNER',
    'existing context version recorded without new semantic decision');
qa($mini['payload']['portal_context']['inventory_snapshot_sha256']===$inventory['sha256']
    &&$mini['payload']['portal_context']['editorial_plan_snapshot_sha256']===$plan['sha256'],
    'original WP/editorial-plan version binding retained');
qa(in_array('INDEPENDENT_CATEGORY_REVIEW',$mini['payload']['reason_codes'],true),
    'independent missing category is NOT waived');
qa(!in_array('ANSWER_EQUIVALENT_PLANNED',$mini['payload']['reason_codes'],true),
    'outdated context-only semantic veto does not survive one authoritative verdict');
qa($mini['matches']===[],'no new context semantic assignment for external MINI topic');

$legacy=PSTE_Context_Evaluator::evaluate($payload,$inventory,$plan,$index,'legacy-topic');
qa($legacy['state']==='CURRENT'&&PSTE_Normalizer::$similarityCalls>0,
    'legacy topics keep existing separate context behavior and their protection');
echo "CONTEXT_SINGLE_SEO_OWNER_QA_ONLY_PASS\n";
