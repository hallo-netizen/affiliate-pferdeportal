<?php
declare(strict_types=1);
/**
 * Entire 100-original-item MINI path simulated on unmodified source fixture.
 * Scope: REAL original queries/titles; MOCK WordPress/plan snapshot and hypothetical
 * single external SEO-owner decisions. NO real WP/K0/PSERC production assertion.
 */
define('ABSPATH','/qa/');
define('ARRAY_A','ARRAY_A');
$GLOBALS['options']=[];
function get_option(string $key,$fallback=[]){return $GLOBALS['options'][$key]??$fallback;}
function update_option(string $key,$value,bool $autoload=false):bool{$GLOBALS['options'][$key]=$value;return true;}
final class PSTE_Editorializer {
    public static function sourceQuery(array $p):string{return (string)($p['raw_query']??$p['raw_user_question']??'');}
}
final class PSTE_Normal_Metadata_Path {
    public static function canonicalInputQuery(string $s):string{return trim($s);}
}
final class PSTE_Cannibalization {
    public static int $calls=0;
    public static function decide(...$args):array{self::$calls++;return ['decision'=>'BLOCKED','reason_codes'=>['MUST_NOT_RUN_SECOND_SEO_REVIEW'],'matches'=>[]];}
}
require_once $argv[1] ?? throw new RuntimeException('MINI source missing');
require_once $argv[2] ?? throw new RuntimeException('Plan gate source missing');

function chk(bool $condition,string $message):void {
    if(!$condition)throw new RuntimeException('FAIL '.$message);
    echo "PASS $message\n";
}
$fixture=json_decode(file_get_contents($argv[3]),true,512,JSON_THROW_ON_ERROR);
chk(($fixture['count']??0)===100,'100 authentic original MINI items loaded');
$sourceCounts=['JA'=>0,'NEIN'=>0,'VIELLEICHT'=>0];$titles=0;$completed=[];
foreach((array)$fixture['items'] as $i=>$item){
    $k='mini-qa-'.str_pad((string)($i+1),3,'0',STR_PAD_LEFT);
    $status=(string)$item['decision'];$sourceCounts[$status]++;
    $titles+=count((array)($item['titles']??[]));
    $completed[$k]=$item;
}
chk($sourceCounts===['JA'=>87,'NEIN'=>4,'VIELLEICHT'=>9],
    'all 87 JA, 9 VIELLEICHT, 4 NEIN preserved without reassessment');
chk($titles===97,'all 97 externally authored titles retained unchanged');
$state=['completed'=>$completed,'active'=>null,'last_report'=>[],'seo_decisions'=>[]];
$GLOBALS['options']['pste_mini_keyword_roundtrip_v1']=$state;
$snapshot=['complete'=>true,'sha256'=>hash('sha256','synthetic WP + PSTE + PSERC inventory for simulation'),
    'items'=>[['source'=>'WORDPRESS','title'=>'2er Pferdeanhänger',
        'id'=>7,'status'=>'publish','target_keyword'=>'2er pferdeanhänger'],
        ['source'=>'PSERC_ACTIVE_PLAN','seo_topic_id'=>'qa-ungefuettert','status'=>'HELD','title'=>'Regendecken ohne Füllung']],
    'sources'=>['WORDPRESS'=>['complete'=>true],'PSTE_PLAN'=>['complete'=>true],'PSERC_ACTIVE_PLAN'=>['complete'=>true]]];
$results=[];$expected=['FREI'=>0,'BELEGT'=>0,'KLAERUNG'=>0];
$counter=0;$selectedFree='';
foreach($completed as $key=>$row){
    if($row['decision']!=='JA')continue;
    $raw=(string)$row['raw_query'];$low=function_exists('mb_strtolower')?mb_strtolower($raw,'UTF-8'):strtolower($raw);
    // Contrived scenario: the SAME EXTERNAL owner gives all semantic outcomes.
    // No PHP keyword heuristics are used to decide this inside the product;
    // the following is TEST DATA only, not a real site verdict.
    $box='KLAERUNG';$matched='';$reason='SIMULATION_LIVE_COVERAGE_NOT_KNOWN';
    if(str_contains($low,'horseware regendecken') && $selectedFree===''){
        $box='FREI';$selectedFree=$key;
    }
    if(str_contains($low,'0g')||str_contains($low,'ungefüttert')){
        $box='BELEGT';$matched='PSERC_ACTIVE_PLAN:qa-ungefuettert';
    }
    if(str_contains($low,'pferdeanhänger 2 pferde')){
        $box='BELEGT';$matched='WORDPRESS:7';
    }
    if($low==='pferd decken'){$box='KLAERUNG';$reason='MEHRDEUTIG_PFERDEZUCHT_ODER_DECKE';}
    $first=(string)($row['titles'][0]['title']??'');
    $item=['pool_key'=>$key,'raw_query'=>$raw,
        'source_sha256'=>hash('sha256',$key.'|'.$raw),'box'=>$box,
        'intent_summary'=>(string)($row['titles'][0]['intent']??'OFFEN'),
        'intent_slot'=>hash('sha256','external-authoritative-intent|'.$raw),
        'approved_title'=>$first,'matched_ref'=>$matched,'reason'=>$reason];
    $results[]=$item;$expected[$box]++;
}
chk(count($results)===87&&$selectedFree!=='','hypothetical 87-topic external decision package prepared');
$document=['contract'=>'PSTE_MINI_SEO_DECISIONS_V1','owner'=>'EXTERNAL_SINGLE_SEO_EDITOR',
    'snapshot_sha256'=>$snapshot['sha256'],'items'=>$results];
$updated=PSTE_Mini_Workflow::acceptSingleOwnerSeoDecisions($state,$document,$snapshot);
$GLOBALS['options']['pste_mini_keyword_roundtrip_v1']=$updated;
chk(count($updated['seo_decisions'])===87,'single technical receipt import preserves 87 owner verdicts');
chk(($updated['seo_last_report']['counts']??null)===$expected,'all three carton totals preserved');
$fake=$document;
$belegtAt=-1;
foreach($fake['items'] as $i=>$v)if($v['box']==='BELEGT'){$belegtAt=$i;break;}
chk($belegtAt>=0,'simulation includes an existing-plan reference case');
$fake['items'][$belegtAt]['matched_ref']='SIMULATED_UNVERIFIED_ARTICLE';
$fakeResult=PSTE_Mini_Workflow::acceptSingleOwnerSeoDecisions($state,$fake,$snapshot);
$badRefKey=(string)$fake['items'][$belegtAt]['pool_key'];
chk(($fakeResult['seo_decisions'][$badRefKey]['box']??'')==='KLAERUNG',
    'fabricated BELEGT reference stays in existing clarification, not accepted as proof');
$verified=['FREI'=>0,'BELEGT'=>0,'KLAERUNG'=>0];
foreach($completed as $key=>$row){
    if($row['decision']!=='JA')continue;
    $candidate=['pool_key'=>$key,'raw_query'=>(string)$row['raw_query'],
        'production_title'=>(string)($row['titles'][0]['title']??''),
        'decision'=>'PASS','editorialization'=>['resolved'=>true],
        'target_category_slug'=>'regendecken'];
    $r=PSTE_Planning_Readiness_Gate::apply($candidate,$snapshot['items'],[]);
    $box=(string)($updated['seo_decisions'][$key]['box']??'KLAERUNG');
    if($box==='FREI')chk($r['planning_readiness_gate']['ok']===true,'hypothetical free receipt passed once');
    else if(($r['planning_readiness_gate']['ok']??null)!==false)throw new RuntimeException('FAIL duplicate/unclear promoted');
    chk(($r['planning_readiness_gate']['cannibalization']['decision']??'')==='NOT_RUN_ALREADY_DECIDED_EXTERNALLY',
        'no second WP keyword/semantic checker for item '.$key);
    $verified[$box]++;
}
chk($verified===$expected,'all 87 cases reached the same stored boxes without semantic rereview');
chk(PSTE_Cannibalization::$calls===0,'legacy WP semantic checker invoked ZERO times for externally decided cases');
$old=$updated;
try{
    PSTE_Mini_Workflow::acceptSingleOwnerSeoDecisions($updated,$document,
        ['complete'=>false,'sha256'=>hash('sha256','changed content')]);
    throw new RuntimeException('FAIL outdated snapshot accepted');
} catch(RuntimeException $e){
    chk(str_starts_with($e->getMessage(),'PSTE_MINI_SEO_PORTAL_PLAN_CHANGED'),
        'outdated or incomplete parkhouse blocks automatic acceptance');
}
$manipulated=$document;$manipulated['items'][0]['raw_query']='TAMPERED';
$mix=PSTE_Mini_Workflow::acceptSingleOwnerSeoDecisions($state,$manipulated,$snapshot);
chk(count($mix['seo_decisions'])===86,'one falsified item held; remaining 86 processed');
chk(isset($mix['clarification'][$results[0]['pool_key']]),'falsified item in existing clarification box');
$pending=$updated;$pending['seo_decisions']=[];$GLOBALS['options']['pste_mini_keyword_roundtrip_v1']=$pending;
$key=$selectedFree;$row=$completed[$key];
$stale=PSTE_Planning_Readiness_Gate::apply(['pool_key'=>$key,'raw_query'=>$row['raw_query'],
    'production_title'=>$row['titles'][0]['title']],[],[]);
chk(($stale['planning_readiness_gate']['ok']??null)===false,
    'missing external result is KLÄRUNG, never old second SEO gate');
chk(PSTE_Cannibalization::$calls===0,'still ZERO duplicate semantic decisions');
echo 'SUMMARY '.json_encode(['total_original'=>100,'ja'=>87,'vielleicht'=>9,'nein'=>4,
    'title_proposals'=>97,'hypothetical_boxes'=>$expected,'semantic_rechecks_in_WP'=>PSTE_Cannibalization::$calls,
    'external_seo_quality_proven'=>false,'real_wp_test'=>false,'PSERC_to_K0_real'=>false],
    JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";
