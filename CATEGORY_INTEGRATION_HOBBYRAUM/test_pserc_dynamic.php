<?php
declare(strict_types=1);

if (!defined('ABSPATH')) { define('ABSPATH', __DIR__ . '/'); }
$root = getenv('PSERC_EXTRACTED_ROOT');
if (!$root || !is_dir($root)) { fwrite(STDERR, "PSERC_ROOT_MISSING\n"); exit(2); }
require_once $root . '/includes/class-pserc-stable-json.php';
require_once $root . '/includes/class-pserc-portal-structure-gate.php';

function stable_hash(array $value): string {
    return PSERC_Stable_Json::hash($value);
}
function with_hash(array $value, string $field): array {
    unset($value[$field]);
    $value[$field] = stable_hash($value);
    return $value;
}
function assert_true($cond, string $code, $data=null): void {
    if (!$cond) {
        fwrite(STDERR, $code . ' ' . json_encode($data, JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES) . "\n");
        exit(3);
    }
}

$leaf = [
    'term_id' => 990001,
    'slug' => 'pferdesaettel-faq',
    'name' => 'FAQ Pferdesättel',
    'article_type' => 'FAQ',
    'canonical_article_type' => 'FAQ',
    'topic_family_name' => 'Pferdesättel',
    'topic_family' => 'Pferdesättel',
    'topic_family_key' => hash('sha256', 'Pferdesättel'),
    'full_path' => 'Ausrüstung > Sattel & Zubehör > Pferdesättel > FAQ Pferdesättel',
    'wp_parent_id' => 0,
    'parent_id' => 0,
    'parent' => 0,
    'ancestor_ids' => [],
    'portal_ancestor_page_ids' => [95,108,972134],
    'portal_ancestor_page_names' => ['Ausrüstung','Sattel & Zubehör','Pferdesättel'],
    'product_page_id' => 972134,
    'product_page_slug' => 'pferdesaettel',
    'branch_hash' => hash('sha256','pferdesaettel-faq-branch'),
];

$baseline = [
    'contract' => 'PSTE_SITE_BASELINE_V1',
    'taxonomy_contract' => 'PSTE_PORTAL_TAXONOMY_SNAPSHOT_V3',
    'status' => 'CURRENT',
    'unclassified_leaf_count' => 0,
    'taxonomy_validation' => ['ok'=>true],
    'leaf_categories' => [$leaf],
    'leaf_category_count' => 1,
    'quarantined_category_count' => 0,
    'structure_hash' => hash('sha256','test-structure'),
];
$baseline = with_hash($baseline, 'baseline_sha256');

$registry = [
    'contract' => 'PSERC_PORTAL_STRUCTURE_REGISTRY_V1',
    'version' => '1.2.0',
    'source' => ['raw_sha256'=>str_repeat('a',64)],
    'rules' => ['read_only'=>true],
    'category_count' => 0,
    'entries' => [],
    'capitalization_vocabulary' => [],
];
$registry = with_hash($registry, 'registry_sha256');

$pos = PSERC_Portal_Structure_Gate::validate($baseline, $registry);
assert_true(!empty($pos['ok']), 'POS_DYNAMIC_CATEGORY_BLOCKED', $pos);
assert_true(($pos['status'] ?? '') === 'PSERC_PORTAL_STRUCTURE_PASS', 'POS_STATUS_WRONG', $pos);
assert_true((int)($pos['dynamic_live_category_count'] ?? -1) === 1, 'POS_DYNAMIC_COUNT_WRONG', $pos);
assert_true((int)($pos['category_count'] ?? -1) === 1, 'POS_CATEGORY_COUNT_WRONG', $pos);
$entry = PSERC_Portal_Structure_Gate::entry($pos, 'pferdesaettel-faq');
assert_true(is_array($entry), 'POS_ENTRY_MISSING', $pos);
assert_true(($entry['runtime_registry_status'] ?? '') === 'LIVE_DYNAMIC_REGISTERED', 'POS_DYNAMIC_STATUS_WRONG', $entry);

$badParent = $baseline;
$badParent['leaf_categories'][0]['wp_parent_id'] = 123;
$badParent['leaf_categories'][0]['parent_id'] = 123;
$badParent['leaf_categories'][0]['parent'] = 123;
$badParent = with_hash($badParent, 'baseline_sha256');
$neg1 = PSERC_Portal_Structure_Gate::validate($badParent, $registry);
assert_true(empty($neg1['ok']), 'NEG_BAD_PARENT_NOT_BLOCKED', $neg1);
assert_true(in_array('PORTAL_STRUCTURE_LIVE_CATEGORY_NOT_FLAT', (array)($neg1['reason_codes'] ?? []), true), 'NEG_BAD_PARENT_CODE_WRONG', $neg1);

$badChain = $baseline;
$badChain['leaf_categories'][0]['portal_ancestor_page_ids'] = [95,108,999999];
$badChain = with_hash($badChain, 'baseline_sha256');
$neg2 = PSERC_Portal_Structure_Gate::validate($badChain, $registry);
assert_true(empty($neg2['ok']), 'NEG_BAD_CHAIN_NOT_BLOCKED', $neg2);
assert_true(in_array('PORTAL_STRUCTURE_LIVE_PRODUCT_PAGE_CHAIN_MISMATCH', (array)($neg2['reason_codes'] ?? []), true), 'NEG_BAD_CHAIN_CODE_WRONG', $neg2);

$duplicate = $baseline;
$dupLeaf = $leaf; $dupLeaf['term_id']=990002;
$duplicate['leaf_categories'][] = $dupLeaf;
$duplicate['leaf_category_count'] = 2;
$duplicate = with_hash($duplicate, 'baseline_sha256');
$neg3 = PSERC_Portal_Structure_Gate::validate($duplicate, $registry);
assert_true(empty($neg3['ok']), 'NEG_DUPLICATE_NOT_BLOCKED', $neg3);
assert_true(in_array('PORTAL_STRUCTURE_LIVE_DUPLICATE_SLUG', (array)($neg3['reason_codes'] ?? []), true), 'NEG_DUPLICATE_CODE_WRONG', $neg3);

echo json_encode([
    'ok'=>true,
    'positive_status'=>$pos['status'],
    'positive_runtime_registry_status'=>$entry['runtime_registry_status'],
    'positive_dynamic_count'=>$pos['dynamic_live_category_count'],
    'negative_bad_parent'=>$neg1['reason_codes'],
    'negative_bad_chain'=>$neg2['reason_codes'],
    'negative_duplicate'=>$neg3['reason_codes'],
], JSON_PRETTY_PRINT|JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES), "\n";
echo "PSERC_DYNAMIC_CATEGORY_POSITIVE_NEGATIVE_PASS\n";
