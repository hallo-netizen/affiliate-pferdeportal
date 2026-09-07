<?php
if ( ! defined( 'ABSPATH' ) ) {
    fwrite(STDERR, "ABSPATH_MISSING\n");
    exit(1);
}

function upk_assert($condition, $label) {
    if (!$condition) {
        fwrite(STDERR, "FAIL: {$label}\n");
        exit(1);
    }
    fwrite(STDOUT, "PASS: {$label}\n");
}

global $wpdb;
$repo = upk_repository();

$tables = array(
    $wpdb->prefix . 'upk_products',
    $wpdb->prefix . 'upk_variants',
    $wpdb->prefix . 'upk_identifiers',
    $wpdb->prefix . 'upk_facts',
);
foreach ($tables as $table) {
    $found = $wpdb->get_var($wpdb->prepare('SHOW TABLES LIKE %s', $table));
    upk_assert($found === $table, "table {$table}");
}

$product_id = $repo->create_product(array(
    'manufacturer' => 'Test Manufacturer',
    'model_name' => 'Model Alpha',
    'product_group_key' => 'test-group',
    'manufacturer_product_url' => 'https://manufacturer.example/model-alpha',
    'lifecycle_status' => 'ACTIVE',
));
upk_assert(is_int($product_id) && $product_id > 0, 'create product');

$variant_id = $repo->create_variant($product_id, array(
    'variant_name' => 'Variant 150',
    'variant_key' => 'variant-150',
    'lifecycle_status' => 'ACTIVE',
));
upk_assert(is_int($variant_id) && $variant_id > 0, 'create variant');

$identifier_id = $repo->add_identifier(
    UPK_Repository::SUBJECT_VARIANT,
    $variant_id,
    'EAN',
    '4000000000001'
);
upk_assert(is_int($identifier_id) && $identifier_id > 0, 'add exact identifier');

$fact_id = $repo->add_fact(
    UPK_Repository::SUBJECT_PRODUCT,
    $product_id,
    array(
        'fact_key' => 'weight',
        'fact_value' => '1200',
        'unit' => 'g',
        'source_url' => 'https://manufacturer.example/model-alpha',
        'source_type' => 'MANUFACTURER',
        'fact_status' => 'VERIFIED',
    )
);
upk_assert(is_int($fact_id) && $fact_id > 0, 'add source-bound fact');

$bundle = $repo->get_product_bundle($product_id);
upk_assert(!is_wp_error($bundle), 'read product bundle');
upk_assert($bundle['manufacturer'] === 'Test Manufacturer', 'read manufacturer');
upk_assert(count($bundle['variants']) === 1, 'read variant');
upk_assert($bundle['variants'][0]['identifiers'][0]['identifier_value'] === '4000000000001', 'read identifier');
upk_assert($bundle['facts'][0]['fact_key'] === 'weight' && $bundle['facts'][0]['fact_value'] === '1200', 'read fact');

$bad_product = $repo->create_product(array(
    'manufacturer' => 'Broken',
    'model_name' => '',
    'product_group_key' => 'test-group',
    'manufacturer_product_url' => 'https://manufacturer.example/broken',
));
upk_assert(is_wp_error($bad_product) && 'UPK_PRODUCT_IDENTITY_INCOMPLETE' === $bad_product->get_error_code(), 'block incomplete identity');

$orphan_variant = $repo->create_variant(99999999, array(
    'variant_name' => 'Orphan',
    'variant_key' => 'orphan',
));
upk_assert(is_wp_error($orphan_variant) && 'UPK_PRODUCT_NOT_FOUND' === $orphan_variant->get_error_code(), 'block orphan variant');

$second_product = $repo->create_product(array(
    'manufacturer' => 'Test Manufacturer B',
    'model_name' => 'Model Beta',
    'product_group_key' => 'test-group',
    'manufacturer_product_url' => 'https://manufacturer.example/model-beta',
    'lifecycle_status' => 'ACTIVE',
));
upk_assert(is_int($second_product) && $second_product > 0, 'create second product');

$identifier_conflict = $repo->add_identifier(
    UPK_Repository::SUBJECT_PRODUCT,
    $second_product,
    'EAN',
    '4000000000001'
);
upk_assert(is_wp_error($identifier_conflict) && 'UPK_IDENTIFIER_CONFLICT' === $identifier_conflict->get_error_code(), 'block identifier conflict');

$empty_verified = $repo->add_fact(
    UPK_Repository::SUBJECT_PRODUCT,
    $product_id,
    array(
        'fact_key' => 'empty_verified',
        'fact_value' => '',
        'source_url' => 'https://manufacturer.example/model-alpha',
        'source_type' => 'MANUFACTURER',
        'fact_status' => 'VERIFIED',
    )
);
upk_assert(is_wp_error($empty_verified) && 'UPK_VERIFIED_FACT_EMPTY' === $empty_verified->get_error_code(), 'block empty verified fact');

$missing_source = $repo->add_fact(
    UPK_Repository::SUBJECT_PRODUCT,
    $product_id,
    array(
        'fact_key' => 'missing_source',
        'fact_value' => 'x',
        'source_url' => '',
        'source_type' => 'MANUFACTURER',
        'fact_status' => 'VERIFIED',
    )
);
upk_assert(is_wp_error($missing_source) && 'UPK_FACT_INCOMPLETE' === $missing_source->get_error_code(), 'block missing source');

fwrite(STDOUT, "UPK_WORDPRESS_DB_GESAMT_PASS\n");
