<?php
if ( ! defined( 'ABSPATH' ) ) {
    fwrite( STDERR, "ABSPATH_MISSING\n" );
    exit( 1 );
}

function upc_seo_assert( $condition, $label ) {
    if ( ! $condition ) {
        fwrite( STDERR, "FAIL: {$label}\n" );
        exit( 1 );
    }
    fwrite( STDOUT, "PASS: {$label}\n" );
}

$knowledge = upk_repository();
$compare   = upc_repository();

$a = $knowledge->create_product(
    array(
        'manufacturer' => 'SEO Maker A',
        'model_name' => 'SEO A',
        'product_group_key' => 'seo-smoke',
        'manufacturer_product_url' => 'https://manufacturer.example/seo-a',
        'lifecycle_status' => 'ACTIVE',
    )
);
$b = $knowledge->create_product(
    array(
        'manufacturer' => 'SEO Maker B',
        'model_name' => 'SEO B',
        'product_group_key' => 'seo-smoke',
        'manufacturer_product_url' => 'https://manufacturer.example/seo-b',
        'lifecycle_status' => 'ACTIVE',
    )
);
upc_seo_assert( is_int( $a ) && is_int( $b ), 'create SEO signal test products' );

$comparison_id = $compare->create_comparison(
    array(
        'comparison_key' => 'seo-smoke-a-vs-b',
        'comparison_type' => 'PRODUCT',
        'subject_ids' => array( $a, $b ),
        'working_title' => 'Bound comparison title',
    )
);
upc_seo_assert( is_int( $comparison_id ) && $comparison_id > 0, 'create SEO signal test comparison' );

$malicious_provider = function( $signals, $context ) {
    return array(
        'target_keyword' => 'seo a vs seo b',
        'demand_score' => 77.5,
        'priority_score' => 88,
        'cannibalization_status' => 'CLEAR',
        'provider' => 'seo-smoke',
        'provider_version' => '1',
        // Deliberately forbidden/unrecognized attempts:
        'title' => 'MALICIOUS TITLE OVERRIDE',
        'html' => '<p>MALICIOUS BODY</p>',
        'ruleset_id' => 'evil-ruleset',
        'product_id' => 999999,
    );
};
add_filter( 'upc_product_comparison_seo_signals', $malicious_provider, 10, 2 );

$payload = upc_seo_signals( $comparison_id );
remove_filter( 'upc_product_comparison_seo_signals', $malicious_provider, 10 );

upc_seo_assert( ! is_wp_error( $payload ), 'read optional SEO signals' );
upc_seo_assert( 'SIGNALS_AVAILABLE' === $payload['status'], 'SEO signal status available' );
upc_seo_assert( 'seo a vs seo b' === $payload['signals']['target_keyword'], 'allowed target keyword passes through' );
upc_seo_assert( 77.5 === $payload['signals']['demand_score'], 'allowed demand score passes through' );
upc_seo_assert( 'Bound comparison title' === $payload['context']['working_title'], 'SEO cannot rewrite bound comparison title in context' );
upc_seo_assert( ! array_key_exists( 'title', $payload['signals'] ), 'SEO title override is discarded' );
upc_seo_assert( ! array_key_exists( 'html', $payload['signals'] ), 'SEO body override is discarded' );
upc_seo_assert( ! array_key_exists( 'ruleset_id', $payload['signals'] ), 'SEO ruleset override is discarded' );
upc_seo_assert( ! array_key_exists( 'product_id', $payload['signals'] ), 'SEO product override is discarded' );

fwrite( STDOUT, "UPC_SEO_SIGNALS_READ_ONLY_PASS\n" );
