<?php
if(!defined('ABSPATH')) exit(2);

function pste_proof_inventory_row(array $c,string $exclude=''): ?array {
    if(!in_array((string)($c['decision']??''),['PASS','REVIEW_REQUIRED'],true)) return null;
    if($exclude!==''&&in_array($exclude,$c['seen_in_runs']??[],true)) return null;
    $category=(string)($c['target_category_name']??'');
    return [
        'post_id'=>0,
        'title'=>PSTE_Editorializer::displayTitle($c),
        'status'=>'draft',
        'category_name'=>$category,
        'topic_family_name'=>$c['topic_family_name']??PSTE_Normalizer::categoryFamilyName($category),
        'topic_family_key'=>$c['topic_family_key']??PSTE_Normalizer::categoryFamilyKey($category),
        'headings'=>[],
        'intent_cluster_id'=>$c['intent_cluster_id']??'',
        'source'=>'PSTE_TOPIC_POOL',
    ];
}
function pste_proof_has_relation_query(array $queries): bool {
    foreach($queries as $sql){
        $x=strtolower((string)$sql);
        if(str_contains($x,'pste_topic_occurrences')||str_contains($x,'pste_topic_assignments')) return true;
    }
    return false;
}
$legacyQueries=[];
$legacyHook=static function($sql) use (&$legacyQueries){$legacyQueries[]=(string)$sql;return $sql;};
add_filter('query',$legacyHook,999);
$all=PSTE_Repository::allCandidates();
remove_filter('query',$legacyHook,999);
if(!pste_proof_has_relation_query($legacyQueries)) throw new RuntimeException('PROOF_LEGACY_ADMIN_MODEL_DID_NOT_TOUCH_RELATIONS');

$legacy=[];
foreach($all as $c){$row=pste_proof_inventory_row((array)$c);if(is_array($row))$legacy[]=$row;}
if(!$legacy) throw new RuntimeException('PROOF_NO_LEGACY_INVENTORY_ROWS');
$familyKey='';$familyName='';
foreach($legacy as $row){
    $k=trim((string)($row['topic_family_key']??''));$n=trim((string)($row['topic_family_name']??''));
    if($k!==''||$n!==''){$familyKey=$k;$familyName=$n;break;}
}
if($familyKey===''&&$familyName==='') throw new RuntimeException('PROOF_NO_FAMILY_BINDING');
$familyText=PSTE_Normalizer::text($familyName);
$expected=array_values(array_filter($legacy,static function($row) use($familyKey,$familyText){
    $rowKey=trim((string)($row['topic_family_key']??''));
    $rowText=PSTE_Normalizer::text((string)($row['topic_family_name']??''));
    return ($familyKey!==''&&$rowKey!==''&&hash_equals($familyKey,$rowKey))||($familyText!==''&&$rowText!==''&&hash_equals($familyText,$rowText));
}));

$newQueries=[];
$newHook=static function($sql) use (&$newQueries){$newQueries[]=(string)$sql;return $sql;};
add_filter('query',$newHook,999);
$actual=PSTE_Repository::previousCandidateInventory('',$familyKey,$familyName);
remove_filter('query',$newHook,999);
if(pste_proof_has_relation_query($newQueries)) throw new RuntimeException('PSTE_WORKFLOW_INVENTORY_RELATION_TABLE_READ_REGRESSION');
$enc=static fn($v)=>wp_json_encode($v,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES|JSON_PRESERVE_ZERO_FRACTION);
if(!hash_equals(hash('sha256',$enc($expected)),hash('sha256',$enc($actual)))){
    file_put_contents('/tmp/inventory-expected.json',$enc($expected));
    file_put_contents('/tmp/inventory-actual.json',$enc($actual));
    throw new RuntimeException('PSTE_WORKFLOW_INVENTORY_FAMILY_PROJECTION_SEMANTIC_DRIFT');
}
echo wp_json_encode([
    'status'=>'PASS_WORKFLOW_INVENTORY_FAMILY_PROJECTION',
    'legacy_inventory_count'=>count($legacy),
    'family_inventory_count'=>count($actual),
    'legacy_relation_queries'=>count(array_filter($legacyQueries,static fn($q)=>str_contains(strtolower((string)$q),'pste_topic_occurrences')||str_contains(strtolower((string)$q),'pste_topic_assignments'))),
    'new_relation_queries'=>0,
    'family_key'=>$familyKey,
],JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";
