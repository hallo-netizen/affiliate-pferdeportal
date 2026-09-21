<?php
declare(strict_types=1);
define('ABSPATH', __DIR__ . '/');
function absint($v){ return abs((int)$v); }
require __DIR__.'/affiliate-portal-router/includes/trait-ppar-ebay.php';

class PPAR_Similarity_Harness {
    use PPAR_Ebay_Trait;
    public function duplicate($a,$b){
        $m=new ReflectionMethod($this,'ebay_topic_titles_duplicate_v672146');
        $m->setAccessible(true);
        return $m->invoke($this,$a,$b);
    }
}
function old_duplicate($a,$b): bool {
    if($a===''||$b==='') return false;
    similar_text($a,$b,$pct);
    return $pct>=92.0;
}
function ok($c,$m){ if(!$c){fwrite(STDERR,"FAIL $m\n");exit(1);} echo "PASS $m\n"; }

$h=new PPAR_Similarity_Harness();
$fixed=[
 ['regendecke pferd wasserdicht atmungsaktiv','regendecke pferd wasserdicht atmungsaktiv'],
 ['regendecke pferd wasserdicht atmungsaktiv','regendecke pferd wasserdicht atmungsakti'],
 ['reithelm sicherheit modell alpha','reithelm sicherheit modell beta'],
 ['abcde12345','xabcde12345'],
 ['aaaaaaaaaaaaaaaaaaaaaaaaa','bbbbbbbbbbbbbbbbbbbbbbbbb'],
 ['', 'x'],
];
foreach($fixed as $i=>$p) ok($h->duplicate($p[0],$p[1])===old_duplicate($p[0],$p[1]),"fixed pair {$i} exact-equivalent");

$corpus=[];
for($i=0;$i<220;$i++){
    $x=hash('sha256','product-'.$i);
    $corpus[]='produkt '.substr($x,0,8).' '.substr($x,8,8).' '.substr($x,16,8).' '.substr($x,24,8).' pferd angebot';
    if($i%20===0) $corpus[]='produkt '.substr($x,0,8).' '.substr($x,8,8).' '.substr($x,16,8).' '.substr($x,24,7).' pferd angebot';
}
$checked=0;
for($i=0,$n=count($corpus);$i<$n;$i++){
    for($j=0;$j<$n;$j++){
        if(old_duplicate($corpus[$i],$corpus[$j])!==$h->duplicate($corpus[$i],$corpus[$j])){
            fwrite(STDERR,"FAIL pair mismatch {$i}/{$j}\n"); exit(1);
        }
        $checked++;
    }
}
ok($checked>50000,"{$checked} pairwise old/new decisions identical");

function old_filter($rows){
    $out=[];$deferred=[];$seenS=[];$seenT=[];
    foreach($rows as $r){
        $dup=false;
        foreach($seenT as $known){ if(old_duplicate($r['title'],$known)){$dup=true;break;} }
        if($dup) continue;
        if($r['seller']!==''&&isset($seenS[$r['seller']])){$deferred[]=$r;continue;}
        if($r['seller']!=='')$seenS[$r['seller']]=true;
        if($r['title']!=='')$seenT[]=$r['title'];
        $out[]=$r;
    }
    foreach($deferred as $r){
        $dup=false;
        foreach($seenT as $known){ if(old_duplicate($r['title'],$known)){$dup=true;break;} }
        if($dup)continue;
        if($r['title']!=='')$seenT[]=$r['title'];
        $out[]=$r;
    }
    return array_column($out,'id');
}
function new_filter($rows,$h){
    $out=[];$deferred=[];$seenS=[];$seenT=[];
    foreach($rows as $r){
        $dup=false;
        foreach($seenT as $known){ if($h->duplicate($r['title'],$known)){$dup=true;break;} }
        if($dup) continue;
        if($r['seller']!==''&&isset($seenS[$r['seller']])){$deferred[]=$r;continue;}
        if($r['seller']!=='')$seenS[$r['seller']]=true;
        if($r['title']!=='')$seenT[]=$r['title'];
        $out[]=$r;
    }
    foreach($deferred as $r){
        $dup=false;
        foreach($seenT as $known){ if($h->duplicate($r['title'],$known)){$dup=true;break;} }
        if($dup)continue;
        if($r['title']!=='')$seenT[]=$r['title'];
        $out[]=$r;
    }
    return array_column($out,'id');
}
$rows=[];
for($i=0;$i<400;$i++){
    $x=hash('sha256','row-'.$i);
    $rows[]=['id'=>$i,'seller'=>'seller'.($i%37),'title'=>'produkt '.substr($x,0,8).' '.substr($x,8,8).' '.substr($x,16,8).' '.substr($x,24,8).' pferd'];
    if($i%53===0) $rows[]=['id'=>10000+$i,'seller'=>'sellerx','title'=>$rows[count($rows)-1]['title']];
}
ok(old_filter($rows)===new_filter($rows,$h),'full two-pass seller/diversity output order identical');

// Worst-case performance shape: 792 same-length, intentionally dissimilar titles.
// Gate is deliberately loose: old quadratic similar_text path takes several seconds;
// exact-safe prefilter must stay comfortably below that without changing the decision.
$unique=[];
for($i=0;$i<792;$i++){
    $x=hash('sha256','worst-'.$i);
    $unique[]='produkt '.substr($x,0,8).' '.substr($x,8,8).' '.substr($x,16,8).' '.substr($x,24,8).' pferd angebot';
}
$t=microtime(true);
$count=0;
for($i=0;$i<count($unique);$i++){
    for($j=0;$j<$i;$j++){
        if($h->duplicate($unique[$i],$unique[$j])) $count++;
    }
}
$elapsed=microtime(true)-$t;
ok($count===0,'792 unique-title corpus has no false duplicate');
ok($elapsed<3.0,'792-title exact-safe prefilter stays below 3 seconds');
echo "CPU_SECONDS=".number_format($elapsed,6,'.','')."\n";
echo "ALL 6.72.146 CPU SIMILARITY TESTS PASS\n";
