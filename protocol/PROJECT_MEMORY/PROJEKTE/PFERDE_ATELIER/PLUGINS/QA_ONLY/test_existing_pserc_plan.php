<?php
declare(strict_types=1);
define('ABSPATH','/qa/');
require_once $argv[1] ?? throw new RuntimeException('Original MINI PHP source required');

function check(bool $ok,string $label):void{if(!$ok)throw new RuntimeException('FAILED '.$label);echo 'PASS '.$label."\n";}
final class PSERC_Plan_Snapshot_Store {
    public static array $head=[];
    public static array $records=[];
    public static bool $switch=false;
    public static int $reads=0;
    public static function getActive(): array {
        self::$reads++;
        if(self::$switch && self::$reads>=2){
            $a=self::$head;$a['snapshot_sha256']=str_repeat('b',64);return $a;
        }
        return self::$head;
    }
    public static function verifyHeader(array $x):bool {return ($x['contract']??'')==='PSERC_PLAN_SNAPSHOT_V1' && preg_match('/^[a-f0-9]{64}$/D',(string)($x['snapshot_sha256']??''))===1;}
    public static function getRecord(string $generation,string $kind,int $index):?array {return self::$records[$index]??null;}
}
final class PSERC_Plan_Dependency_Fingerprint {
    public static bool $current=true;
    public static function isCurrent(array $x):bool {return self::$current;}
}
$gen=str_repeat('a',20);$sha=str_repeat('1',64);
PSERC_Plan_Snapshot_Store::$head=['contract'=>'PSERC_PLAN_SNAPSHOT_V1',
    'generation'=>$gen,'snapshot_sha256'=>$sha,
    'dependency'=>['source'=>'mock'],'counts'=>['compiled_items'=>2]];
PSERC_Plan_Snapshot_Store::$records=[
    ['status'=>'READY_FOR_METADATA_HANDOFF','seo_topic_id'=>'p1',
     'title'=>['production_title'=>'Pferdedecke'],
     'target_keyword'=>['value'=>'pferdedecke'],'canonical_slot'=>['canonical_article_id'=>'slot-a','plan_slot_sha256'=>'slot-hash'],
     'category'=>['slug'=>'regendecke'],'article_type'=>'Beratung','intent_profile'=>['search_intent'=>'Kauf']],
    ['status'=>'REVIEW_REQUIRED_SEMANTIC_OVERLAP','seo_topic_id'=>'p2',
     'title'=>['production_title'=>''],'target_keyword'=>['value'=>''],
     'category'=>['slug'=>''],'article_type'=>'FAQ','intent_profile'=>[]],
];
$a=PSTE_Mini_Workflow::readExistingPsercPlanForParkhaus();
check($a['complete']===true && $a['item_count']===2,'all PSERC final records read, not only READY');
check($a['items'][1]['status']==='REVIEW_REQUIRED_SEMANTIC_OVERLAP','existing held item preserved');
check($a['items'][1]['title']==='','untitled held plan kept, not dropped');
check($a['items'][0]['canonical_article_id']==='slot-a','existing slot identity retained');
PSERC_Plan_Snapshot_Store::$records[1]=null;
$a=PSTE_Mini_Workflow::readExistingPsercPlanForParkhaus();
check($a['complete']===false && $a['reason']==='PSERC_ACTIVE_PLAN_RECORD_MISSING','missing record blocks completeness');
PSERC_Plan_Snapshot_Store::$records[1]=['status'=>'HELD_NO_TITLE_CONTRACT'];
PSERC_Plan_Dependency_Fingerprint::$current=false;
check(PSTE_Mini_Workflow::readExistingPsercPlanForParkhaus()['complete']===false,'stale active plan not treated as complete');
PSERC_Plan_Dependency_Fingerprint::$current=true;
PSERC_Plan_Snapshot_Store::$switch=true;PSERC_Plan_Snapshot_Store::$reads=0;
check(PSTE_Mini_Workflow::readExistingPsercPlanForParkhaus()['complete']===false,'plan changed during read is rejected');
echo "QA ONLY: no SEO re-evaluation, WordPress E2E and full site inventory NOT proven\n";
