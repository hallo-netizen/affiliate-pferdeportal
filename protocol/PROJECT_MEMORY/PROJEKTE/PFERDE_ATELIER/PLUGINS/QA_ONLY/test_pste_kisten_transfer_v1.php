<?php
declare(strict_types=1);
require_once __DIR__.'/pste_kisten_transfer_v1.php';
function must(bool $condition,string $name):void{ if(!$condition)throw new RuntimeException('FAIL '.$name);echo 'PASS '.$name."\n"; }
$hash=hash('sha256','complete-pferdeatelier-v22-simulated-snapshot');
$origin=[];
foreach(['a'=>'pferdeanhänger 2 pferde','b'=>'regendecke pferd 0g','c'=>'horseware regendecken','d'=>'falscher Eintrag','e'=>'regendecke pferd ungefüttert','f'=>'neue Anfrage'] as $id=>$raw){
    $origin[$id]=['raw_query'=>$raw,'source_sha256'=>hash('sha256',$id.'|'.$raw)];
}
$snapshot=['complete'=>true,'sha256'=>$hash,'current_sha256'=>$hash,'originals'=>$origin];
function item(array $snapshot,string $id,string $box,array $fields=[]):array{
    return array_merge(['pool_key'=>$id,'raw_query'=>$snapshot['originals'][$id]['raw_query'],
        'source_sha256'=>$snapshot['originals'][$id]['source_sha256'],
        'snapshot_sha256'=>$snapshot['sha256'],'box'=>$box],$fields);
}
$items=[
    item($snapshot,'a','BELEGT',['matched_ref'=>'WP-2er-Pferdeanhaenger']),
    item($snapshot,'b','BELEGT',['matched_ref'=>'PLAN-ungefuettert']),
    item($snapshot,'c','FREI',['intent_slot'=>'Horseware:Passform','approved_title'=>'Horseware Regendecken auswählen','editorial_receipt'=>'external-editor-1']),
    item($snapshot,'d','KLAERUNG',['reason'=>'INTENT_UNCLEAR','alternative_intent'=>'neues Fachthema statt umformulierter Titel']),
    item($snapshot,'e','FREI',['intent_slot'=>'Horseware:Passform','approved_title'=>'Falsche doppelte Reservierung','editorial_receipt'=>'external-editor-1']),
    item($snapshot,'f','FREI',['intent_slot'=>'F:NeueFrage','approved_title'=>'Eigenständiger Titel','editorial_receipt'=>'external-editor-1']),
];
$slots=[];$calls=0;
$reserve=function(string $slot,array $item)use(&$slots,&$calls):bool {
    $calls++;
    if(isset($slots[$slot]))return false;
    $slots[$slot]=$item['pool_key'];return true;
};
$result=PsteKistenTransferV1::distribute($snapshot,$items,$reserve);
must(!$result['system_blocked'],'valid snapshot enables item routing');
must(count($result['FREI'])===2,'only two distinct reserved slots accepted');
must(count($result['BELEGT'])===2,'proven duplicates retained without new article');
must(count($result['KLAERUNG'])===2,'unclear item and concurrent slot isolated');
must($calls===3,'no second semantic decision or lookup in receipt router');
$changed=$snapshot;$changed['current_sha256']=hash('sha256','edited portal meanwhile');
$blocked=PsteKistenTransferV1::distribute($changed,$items,$reserve);
must($blocked['system_blocked']===true&&count($blocked['FREI'])===0,'stale complete plan cannot silently approve');
$missing=$snapshot;$missing['complete']=false;
must(PsteKistenTransferV1::distribute($missing,$items,$reserve)['system_blocked']===true,'missing portal plans prevent false approval');
$bad=item($snapshot,'f','FREI',['source_sha256'=>hash('sha256','tamper'),'intent_slot'=>'F:Other','approved_title'=>'test','editorial_receipt'=>'external']);
$good=item($snapshot,'c','FREI',['intent_slot'=>'C:New','approved_title'=>'Horseware Regendecken','editorial_receipt'=>'external']);
$slots=[];$res=PsteKistenTransferV1::distribute($snapshot,[$bad,$good],$reserve);
must(count($res['KLAERUNG'])===1&&count($res['FREI'])===1,'tampered single item does not block healthy sibling');
$empty=item($snapshot,'f','BELEGT');$slots=[];
$res=PsteKistenTransferV1::distribute($snapshot,[$empty,$good],$reserve);
must(count($res['KLAERUNG'])===1&&count($res['FREI'])===1,'missing evidence goes to clarification box');
echo "QA_ONLY PASS – semantic quality NOT tested; 1:1 WordPress end-to-end NOT tested\n";
