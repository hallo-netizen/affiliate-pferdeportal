<?php
declare(strict_types=1);
define('ABSPATH','/qa/');
class PSTE_Editorializer {
    public static function sourceQuery(array $p): string {return (string)($p['raw_query']??'');}
}
require_once $argv[1] ?? throw new RuntimeException('Patched class path required');
function check(bool $ok,string $label):void{if(!$ok)throw new RuntimeException("FAILED: ".$label);echo "PASS ".$label."\n";}
$original=['contract'=>'PSTE_RAW_KEYWORD_MINI_BATCH_V1','batch_id'=>'mini-test-123456','items'=>[]];
$db=[];
foreach(['alpha 2er','bravo 0g','charlie horseware'] as $idx=>$q) {
    $id=$idx+1;$key='topic-'.$id;
    $source=hash('sha256',$id.'|'.$key.'|'.$q);
    $original['items'][]=['id'=>$id,'pool_key'=>$key,'raw_query'=>$q,'source_sha256'=>$source,'decision'=>'','titles'=>[]];
    $db[$key]=['id'=>$id,'pool_key'=>$key,'payload_json'=>json_encode(['raw_query'=>$q])];
}
$received=$original;
foreach($received['items'] as $n=>&$item) {
    $item['decision']='JA';
    $item['titles']=[['intent'=>'Kaufberatung','title'=>'Passende Ausstattung fuer Pferde finden']];
}
unset($item);
$received['items'][1]['titles'][0]['title']=''; // only this topic is broken
$lookup=static fn(string $key):?array=>$db[$key]??null;
$result=PSTE_Mini_Workflow::validateResult($original,$received,$lookup);
check(count($result['completed'])===2,'healthy topics survive one invalid item');
check(count($result['clarification'])===1,'broken topic put in clarification');
check(($result['clarification'][0]['pool_key']??'')==='topic-2','correct source retained');
check($result['stats']['JA']===2&&$result['stats']['clarification']===1,'transparent counts');
$received['items'][1]['titles'][0]['title']='Neuer Titel mit sinnvoller Bedeutung';
$received['items'][1]['raw_query']='manipulated source query';
$result=PSTE_Mini_Workflow::validateResult($original,$received,$lookup);
check(count($result['completed'])===2&&count($result['clarification'])===1,'tampered single row isolated without permission');
$received=$original;$received['batch_id']='wrong-batch';
try{PSTE_Mini_Workflow::validateResult($original,$received,$lookup);throw new RuntimeException('missing global blocker');}
catch(RuntimeException $e){check($e->getMessage()==='PSTE_MINI_WRONG_BATCH','wrong overall batch blocks safely');}
try{PSTE_Mini_Workflow::validateResult($original,$received=$original,static function(){throw new RuntimeException('DB_DOWN');});throw new RuntimeException('missing infrastructure blocker');}
catch(RuntimeException $e){check($e->getMessage()==='DB_DOWN','actual infrastructure failure not reclassified as editorial');}
echo "QA-only; semantics and real WordPress runtime not proved\n";
