<?php
declare(strict_types=1);

if (!defined('ABSPATH')) { define('ABSPATH', __DIR__ . '/'); }

$root = getenv('PSERC_EXTRACTED_ROOT');
$portalPath = getenv('CATEGORY_PORTAL_CANDIDATE');
$tsvPath = getenv('CATEGORY_TSV');
if (!$root || !is_dir($root)) { fwrite(STDERR, "PSERC_ROOT_MISSING\n"); exit(2); }
if (!$portalPath || !is_file($portalPath)) { fwrite(STDERR, "PORTAL_CANDIDATE_MISSING\n"); exit(2); }
if (!$tsvPath || !is_file($tsvPath)) { fwrite(STDERR, "CATEGORY_TSV_MISSING\n"); exit(2); }

require_once $root . '/includes/class-pserc-stable-json.php';
require_once $root . '/includes/class-pserc-portal-structure-gate.php';

function fail_hard(string $code, $data=null): void {
    fwrite(STDERR, $code . ($data===null ? '' : ' '.json_encode($data, JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)) . "\n");
    exit(3);
}
function with_hash(array $value,string $field): array {
    unset($value[$field]);
    $value[$field]=PSERC_Stable_Json::hash($value);
    return $value;
}

$portal=json_decode((string)file_get_contents($portalPath),true,512,JSON_THROW_ON_ERROR);
$registry=json_decode((string)file_get_contents($root.'/contracts/portal-structure-registry-v1.json'),true,512,JSON_THROW_ON_ERROR);
if((int)($registry['category_count']??-1)!==1124 || count((array)($registry['entries']??[]))!==1124) fail_hard('PSERC_STATIC_REGISTRY_NOT_1124');

$terms=[];
$fh=fopen($tsvPath,'rb');
$header=fgetcsv($fh,0,"\t");
if($header!==['term_id','slug','name','parent_slug']) fail_hard('TSV_HEADER_INVALID',$header);
while(($row=fgetcsv($fh,0,"\t"))!==false){
    if(count($row)!==4) continue;
    [$termId,$slug,$name,$parent]=$row;
    $terms[$slug]=['term_id'=>(int)$termId,'name'=>$name,'parent_slug'=>$parent];
}
fclose($fh);

$pagesBySlug=[];
foreach((array)($portal['pages']??[]) as $p){ if(is_array($p)&&isset($p['slug'])) $pagesBySlug[(string)$p['slug']]=$p; }
$newProductIds=[
 'pferdesaettel'=>972134,
 'trensen'=>972141,
 'offenstallbau'=>972148,
 'paddockbau'=>972155,
 'reitplatzbau'=>972162,
];
$pageId=function(string $slug) use($pagesBySlug,$newProductIds): int {
    if(isset($newProductIds[$slug])) return $newProductIds[$slug];
    $id=(string)($pagesBySlug[$slug]['id']??'');
    if(preg_match('/^p(\d+)$/',$id,$m)) return (int)$m[1];
    fail_hard('PORTAL_PAGE_ID_INVALID',['slug'=>$slug,'id'=>$id]);
    return 0;
};

$leaf=[];
foreach((array)($portal['categories']??[]) as $c){
    if(!is_array($c)) continue;
    $slug=(string)($c['category_slug']??'');
    if(!isset($terms[$slug])) fail_hard('CATEGORY_NOT_IN_AUTHORITATIVE_TSV',$slug);
    if((string)$terms[$slug]['parent_slug']!=='') fail_hard('CATEGORY_NOT_FLAT',$slug);
    $mainSlug=(string)($c['main_slug']??'');
    $hubSlug=(string)($c['hub_slug']??'');
    $productSlug=(string)($c['product_slug']??'');
    $mainName=(string)($c['main_hub']??'');
    $hubName=(string)($c['hub']??'');
    $productName=(string)($c['product']??'');
    $family=$productName;
    $type=(string)($c['theme']??'');
    $productId=$pageId($productSlug);
    $ancestors=[$pageId($mainSlug),$pageId($hubSlug),$productId];
    $leaf[]=[
      'term_id'=>(int)$terms[$slug]['term_id'],
      'slug'=>$slug,
      'name'=>(string)$terms[$slug]['name'],
      'article_type'=>$type,
      'canonical_article_type'=>$type,
      'topic_family_name'=>$family,
      'topic_family'=>$family,
      'topic_family_key'=>hash('sha256',$productSlug.'|'.$family),
      'full_path'=>implode(' > ',[$mainName,$hubName,$productName,(string)$terms[$slug]['name']]),
      'wp_parent_id'=>0,
      'parent_id'=>0,
      'parent'=>0,
      'ancestor_ids'=>[],
      'portal_ancestor_page_ids'=>$ancestors,
      'portal_ancestor_page_names'=>[$mainName,$hubName,$productName],
      'product_page_id'=>$productId,
      'product_page_slug'=>$productSlug,
      'branch_hash'=>hash('sha256',$slug.'|'.implode('|',$ancestors)),
    ];
}
if(count($leaf)!==1149) fail_hard('FULL_BASELINE_COUNT_WRONG',count($leaf));

$ids=array_column($leaf,'term_id');
$slugs=array_column($leaf,'slug');
if(count($ids)!==count(array_unique($ids))) fail_hard('DUPLICATE_TERM_ID');
if(count($slugs)!==count(array_unique($slugs))) fail_hard('DUPLICATE_SLUG');

$baseline=[
 'contract'=>'PSTE_SITE_BASELINE_V1',
 'taxonomy_contract'=>'PSTE_PORTAL_TAXONOMY_SNAPSHOT_V3',
 'status'=>'CURRENT',
 'unclassified_leaf_count'=>0,
 'taxonomy_validation'=>['ok'=>true],
 'leaf_categories'=>$leaf,
 'leaf_category_count'=>1149,
 'quarantined_category_count'=>0,
 'structure_hash'=>hash_file('sha256',$portalPath),
];
$baseline=with_hash($baseline,'baseline_sha256');

$result=PSERC_Portal_Structure_Gate::validate($baseline,$registry);
if(empty($result['ok'])) fail_hard('PSERC_FULL_1149_GATE_BLOCKED',$result);
$expect=[
 'category_count'=>1149,
 'live_total_leaf_category_count'=>1149,
 'protected_live_category_count'=>1124,
 'dynamic_live_category_count'=>25,
 'missing_protected_category_count'=>0,
];
foreach($expect as $k=>$v){ if((int)($result[$k]??-1)!==$v) fail_hard('PSERC_FULL_1149_COUNT_MISMATCH',['field'=>$k,'actual'=>$result[$k]??null,'expected'=>$v]); }

$newSlugs=[
 'pferdesaettel-faq','pferdesaettel-beratung','pferdesaettel-vergleich','pferdesaettel-pflege','pferdesaettel-kosten',
 'trensen-faq','trensen-beratung','trensen-vergleich','trensen-pflege','trensen-kosten',
 'offenstallbau-faq','offenstallbau-beratung','offenstallbau-vergleich','offenstallbau-installation','offenstallbau-kosten',
 'paddockbau-faq','paddockbau-beratung','paddockbau-vergleich','paddockbau-installation','paddockbau-kosten',
 'reitplatzbau-faq','reitplatzbau-beratung','reitplatzbau-vergleich','reitplatzbau-installation','reitplatzbau-kosten'
];
foreach($newSlugs as $slug){
    $entry=PSERC_Portal_Structure_Gate::entry($result,$slug);
    if(!is_array($entry)) fail_hard('PSERC_NEW_ENTRY_MISSING',$slug);
    if(($entry['runtime_registry_status']??'')!=='LIVE_DYNAMIC_REGISTERED') fail_hard('PSERC_NEW_ENTRY_NOT_DYNAMIC',['slug'=>$slug,'status'=>$entry['runtime_registry_status']??null]);
    if(($entry['term_id']??0)<1577 || ($entry['term_id']??0)>1601) fail_hard('PSERC_NEW_ENTRY_TERM_ID_WRONG',['slug'=>$slug,'term_id'=>$entry['term_id']??null]);
}

$out=[
 'status'=>'PASS',
 'result_status'=>$result['status'],
 'category_count'=>$result['category_count'],
 'protected_live_category_count'=>$result['protected_live_category_count'],
 'dynamic_live_category_count'=>$result['dynamic_live_category_count'],
 'missing_protected_category_count'=>$result['missing_protected_category_count'],
 'static_drift_count'=>$result['static_drift_count'],
 'baseline_sha256'=>$baseline['baseline_sha256'],
 'structure_hash'=>$baseline['structure_hash'],
 'write_attempted'=>$result['write_attempted'],
 'new_term_id_min'=>min(array_map(fn($s)=>$result['by_slug'][$s]['term_id'],$newSlugs)),
 'new_term_id_max'=>max(array_map(fn($s)=>$result['by_slug'][$s]['term_id'],$newSlugs)),
];
echo json_encode($out,JSON_PRETTY_PRINT|JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES),"\n";
echo "PSERC_FULL_1149_RUNTIME_GATE_PASS\n";
