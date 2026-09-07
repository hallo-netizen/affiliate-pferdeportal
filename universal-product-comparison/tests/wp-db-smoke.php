<?php
if ( ! defined( 'ABSPATH' ) ) {
    fwrite(STDERR, "ABSPATH_MISSING\n");
    exit(1);
}

function upc_assert($condition, $label) {
    if (!$condition) {
        fwrite(STDERR, "FAIL: {$label}\n");
        exit(1);
    }
    fwrite(STDOUT, "PASS: {$label}\n");
}

global $wpdb;
$knowledge = upk_repository();
$compare   = upc_repository();
upc_assert(!is_wp_error($compare), 'comparison repository available');

foreach (array($wpdb->prefix . 'upc_comparisons', $wpdb->prefix . 'upc_items') as $table) {
    $found = $wpdb->get_var($wpdb->prepare('SHOW TABLES LIKE %s', $table));
    upc_assert($found === $table, "table {$table}");
}

function upc_make_product($knowledge, $manufacturer, $model, $group) {
    return $knowledge->create_product(array(
        'manufacturer' => $manufacturer,
        'model_name' => $model,
        'product_group_key' => $group,
        'manufacturer_product_url' => 'https://manufacturer.example/' . sanitize_title($model),
        'lifecycle_status' => 'ACTIVE',
    ));
}

$a = upc_make_product($knowledge, 'Maker A', 'Alpha', 'boots');
$b = upc_make_product($knowledge, 'Maker B', 'Beta', 'boots');
$c = upc_make_product($knowledge, 'Maker A', 'Gamma', 'boots');
$d = upc_make_product($knowledge, 'Maker D', 'Delta', 'blankets');
upc_assert(is_int($a) && is_int($b) && is_int($c) && is_int($d), 'create comparison products');

$knowledge->add_fact(UPK_Repository::SUBJECT_PRODUCT, $a, array(
    'fact_key' => 'weight',
    'fact_value' => '1000',
    'unit' => 'g',
    'source_url' => 'https://manufacturer.example/alpha',
    'source_type' => 'MANUFACTURER',
    'fact_status' => 'VERIFIED',
));

$comparison_id = $compare->create_comparison(array(
    'comparison_key' => 'alpha-vs-beta',
    'comparison_type' => 'PRODUCT',
    'subject_ids' => array($a, $b),
    'decision_intent' => 'Which boot better fits the documented use case?',
    'working_title' => 'Bound Alpha vs Beta Title',
));
upc_assert(is_int($comparison_id) && $comparison_id > 0, 'create valid product comparison');

$bundle = $compare->get_comparison_bundle($comparison_id);
upc_assert(!is_wp_error($bundle), 'read comparison bundle');
upc_assert($bundle['comparison_uid'] === 'UPC-' . str_pad((string)$comparison_id, 6, '0', STR_PAD_LEFT), 'stable comparison uid');
upc_assert(count($bundle['items']) === 2, 'read two comparison items');
upc_assert($bundle['items'][0]['knowledge']['facts'][0]['fact_value'] === '1000', 'facts resolved from product knowledge');

$knowledge->add_fact(UPK_Repository::SUBJECT_PRODUCT, $a, array(
    'fact_key' => 'weight',
    'fact_value' => '1050',
    'unit' => 'g',
    'source_url' => 'https://manufacturer.example/alpha',
    'source_type' => 'MANUFACTURER',
    'fact_status' => 'VERIFIED',
));
$bundle_after_update = $compare->get_comparison_bundle($comparison_id);
upc_assert($bundle_after_update['items'][0]['knowledge']['facts'][0]['fact_value'] === '1050', 'comparison reads updated fact without copy');

$ean_a = $knowledge->add_identifier(
    UPK_Repository::SUBJECT_PRODUCT,
    $a,
    'EAN',
    '4000000000100'
);
$mpn_b = $knowledge->add_identifier(
    UPK_Repository::SUBJECT_PRODUCT,
    $b,
    'MPN',
    'TEST-BETA-MPN'
);
upc_assert(is_int($ean_a) && is_int($mpn_b), 'bind exact Affiliate test identifiers');

$bridge_post_id = wp_insert_post(array(
    'post_type' => 'post',
    'post_status' => 'draft',
    'post_title' => 'Bridge Test',
    'post_content' => 'Bridge Test',
), true);
upc_assert(!is_wp_error($bridge_post_id), 'create Affiliate bridge test post');
update_post_meta($bridge_post_id, '_upc_comparison_id', (string)$comparison_id);

$exact_requirements = UPC_Affiliate_Bridge::exact_product_requirements(array(), $bridge_post_id, array(), '');
upc_assert(count($exact_requirements) === 2, 'Affiliate bridge emits one exact requirement per identified comparison subject');
upc_assert($exact_requirements[0]['identifiers'][0]['type'] === 'EAN', 'Affiliate bridge emits EAN');
upc_assert($exact_requirements[0]['identifiers'][0]['value'] === '4000000000100', 'Affiliate bridge preserves exact EAN value');
upc_assert($exact_requirements[1]['identifiers'][0]['type'] === 'MPN', 'Affiliate bridge emits exact MPN');
upc_assert($exact_requirements[1]['identifiers'][0]['value'] === 'TEST-BETA-MPN', 'Affiliate bridge preserves exact MPN value');

$e = upc_make_product($knowledge, 'Maker E', 'Epsilon', 'boots');
upc_assert(is_int($e), 'create no-Affiliate-exact-identifier product');
$manufacturer_article = $knowledge->add_identifier(
    UPK_Repository::SUBJECT_PRODUCT,
    $e,
    'MANUFACTURER_ARTICLE_NUMBER',
    'MANUFACTURER-ONLY-123'
);
upc_assert(is_int($manufacturer_article), 'bind manufacturer article number as product knowledge only');

$no_identifier_comparison = $compare->create_comparison(array(
    'comparison_key' => 'beta-vs-epsilon',
    'comparison_type' => 'PRODUCT',
    'subject_ids' => array($b, $e),
));
upc_assert(is_int($no_identifier_comparison), 'create comparison with one subject lacking Affiliate exact identifier');

$no_identifier_post = wp_insert_post(array(
    'post_type' => 'post',
    'post_status' => 'draft',
    'post_title' => 'No Identifier Test',
    'post_content' => 'No Identifier Test',
), true);
upc_assert(!is_wp_error($no_identifier_post), 'create no-identifier bridge test post');
update_post_meta($no_identifier_post, '_upc_comparison_id', (string)$no_identifier_comparison);

$partial_requirements = UPC_Affiliate_Bridge::exact_product_requirements(array(), $no_identifier_post, array(), '');
upc_assert(count($partial_requirements) === 1, 'manufacturer article number does not become Affiliate exact requirement');
upc_assert($partial_requirements[0]['identifiers'][0]['value'] === 'TEST-BETA-MPN', 'identified subject remains available without substitute for missing subject');

$seo_provider = function($signals, $context) {
    return array(
        'target_keyword' => 'alpha vs beta',
        'demand_score' => 77.5,
        'priority_score' => 88,
        'cannibalization_status' => 'CLEAR',
        'provider' => 'seo-smoke',
        'provider_version' => '1',
        'title' => 'MALICIOUS TITLE OVERRIDE',
        'html' => '<p>MALICIOUS BODY</p>',
        'ruleset_id' => 'evil-ruleset',
        'product_id' => 999999,
    );
};
add_filter('upc_product_comparison_seo_signals', $seo_provider, 10, 2);
$seo_payload = upc_seo_signals($comparison_id);
remove_filter('upc_product_comparison_seo_signals', $seo_provider, 10);

upc_assert(!is_wp_error($seo_payload), 'read optional SEO signals');
upc_assert($seo_payload['status'] === 'SIGNALS_AVAILABLE', 'SEO signals available');
upc_assert($seo_payload['signals']['target_keyword'] === 'alpha vs beta', 'allowed SEO target keyword passes through');
upc_assert($seo_payload['signals']['demand_score'] === 77.5, 'allowed SEO demand score passes through');
upc_assert($seo_payload['context']['working_title'] === 'Bound Alpha vs Beta Title', 'SEO cannot rewrite bound comparison title');
upc_assert(!array_key_exists('title', $seo_payload['signals']), 'SEO title override discarded');
upc_assert(!array_key_exists('html', $seo_payload['signals']), 'SEO body override discarded');
upc_assert(!array_key_exists('ruleset_id', $seo_payload['signals']), 'SEO ruleset override discarded');
upc_assert(!array_key_exists('product_id', $seo_payload['signals']), 'SEO product override discarded');

$reverse = $compare->create_comparison(array(
    'comparison_key' => 'beta-vs-alpha',
    'comparison_type' => 'PRODUCT',
    'subject_ids' => array($b, $a),
));
upc_assert(is_wp_error($reverse) && 'UPC_DUPLICATE_COMPARISON' === $reverse->get_error_code(), 'block reversed duplicate');

$same_maker = $compare->create_comparison(array(
    'comparison_key' => 'alpha-vs-gamma',
    'comparison_type' => 'PRODUCT',
    'subject_ids' => array($a, $c),
));
upc_assert(is_wp_error($same_maker) && 'UPC_MIN_TWO_MANUFACTURERS' === $same_maker->get_error_code(), 'block same-manufacturer comparison');

$cross_group = $compare->create_comparison(array(
    'comparison_key' => 'alpha-vs-delta',
    'comparison_type' => 'PRODUCT',
    'subject_ids' => array($a, $d),
));
upc_assert(is_wp_error($cross_group) && 'UPC_PRODUCT_GROUP_MISMATCH' === $cross_group->get_error_code(), 'block cross-group comparison');

$too_many = $compare->create_comparison(array(
    'comparison_key' => 'too-many',
    'comparison_type' => 'PRODUCT',
    'subject_ids' => array($a, $b, $c, $d, 999),
));
upc_assert(is_wp_error($too_many) && 'UPC_INVALID_ITEM_COUNT' === $too_many->get_error_code(), 'block more than four products');

$v1 = $knowledge->create_variant($a, array('variant_name' => 'Wide', 'variant_key' => 'wide', 'lifecycle_status' => 'ACTIVE'));
$v2 = $knowledge->create_variant($a, array('variant_name' => 'Regular', 'variant_key' => 'regular', 'lifecycle_status' => 'ACTIVE'));
$v3 = $knowledge->create_variant($b, array('variant_name' => 'Wide', 'variant_key' => 'wide', 'lifecycle_status' => 'ACTIVE'));
upc_assert(is_int($v1) && is_int($v2) && is_int($v3), 'create variants');

$variant_comparison = $compare->create_comparison(array(
    'comparison_key' => 'alpha-wide-vs-regular',
    'comparison_type' => 'VARIANT',
    'subject_ids' => array($v1, $v2),
));
upc_assert(is_int($variant_comparison) && $variant_comparison > 0, 'create valid variant comparison');

$variant_bundle = $compare->get_comparison_bundle($variant_comparison);
upc_assert(!is_wp_error($variant_bundle) && $variant_bundle['items'][0]['knowledge']['product']['id'] === (string)$a, 'variant readback resolves base product');

$wrong_parent = $compare->create_comparison(array(
    'comparison_key' => 'wrong-parent',
    'comparison_type' => 'VARIANT',
    'subject_ids' => array($v1, $v3),
));
upc_assert(is_wp_error($wrong_parent) && 'UPC_VARIANT_PARENT_MISMATCH' === $wrong_parent->get_error_code(), 'block variants from different base products');

fwrite(STDOUT, "UPC_SEO_SIGNALS_READ_ONLY_PASS\n");
fwrite(STDOUT, "UPC_AFFILIATE_EXACT_IDENTIFIER_POLICY_PASS\n");
fwrite(STDOUT, "UPC_WORDPRESS_DB_GESAMT_PASS\n");
