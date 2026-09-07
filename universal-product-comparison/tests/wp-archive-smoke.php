<?php
if ( ! defined( 'ABSPATH' ) ) {
    fwrite( STDERR, "ABSPATH_MISSING\n" );
    exit( 1 );
}

function upc_archive_assert( $condition, $label ) {
    if ( ! $condition ) {
        fwrite( STDERR, "FAIL: {$label}\n" );
        exit( 1 );
    }
    fwrite( STDOUT, "PASS: {$label}\n" );
}

global $wpdb;

$parent = get_term_by( 'slug', 'regendecken', 'category' );
if ( ! $parent ) {
    $created = wp_insert_term( 'Regendecken', 'category', array( 'slug' => 'regendecken' ) );
    upc_archive_assert( ! is_wp_error( $created ), 'create archive parent category' );
    $parent = get_term( (int) $created['term_id'], 'category' );
}

$child = get_term_by( 'slug', 'regendecken-vergleich', 'category' );
if ( ! $child ) {
    $created = wp_insert_term(
        'Vergleich',
        'category',
        array(
            'slug'   => 'regendecken-vergleich',
            'parent' => (int) $parent->term_id,
        )
    );
    upc_archive_assert( ! is_wp_error( $created ), 'create archive comparison category' );
    $child = get_term( (int) $created['term_id'], 'category' );
}

$product_comparison_id = (int) $wpdb->get_var(
    $wpdb->prepare(
        "SELECT id FROM {$wpdb->prefix}upc_comparisons WHERE comparison_key = %s LIMIT 1",
        'pv-reg-001'
    )
);
upc_archive_assert( $product_comparison_id > 0, 'resolve real PV-REG-001 comparison' );

$product_bundle = upc_repository()->get_comparison_bundle( $product_comparison_id );
upc_archive_assert( ! is_wp_error( $product_bundle ), 'read PV-REG-001 for archive' );

$base_product_id = (int) $product_bundle['items'][0]['subject_id'];
$knowledge = upk_repository();

$variant_a = $knowledge->create_variant(
    $base_product_id,
    array(
        'variant_name'     => 'Archive Test A',
        'variant_key'      => 'archive-test-a',
        'lifecycle_status' => 'ACTIVE',
    )
);
$variant_b = $knowledge->create_variant(
    $base_product_id,
    array(
        'variant_name'     => 'Archive Test B',
        'variant_key'      => 'archive-test-b',
        'lifecycle_status' => 'ACTIVE',
    )
);
upc_archive_assert( is_int( $variant_a ) && is_int( $variant_b ), 'create archive variant fixtures' );

$variant_comparison_id = upc_repository()->create_comparison(
    array(
        'comparison_key'  => 'archive-regendecken-variants',
        'comparison_type' => 'VARIANT',
        'subject_ids'     => array( $variant_a, $variant_b ),
        'working_title'   => 'WeatherBeeta Variantenvergleich',
    )
);
upc_archive_assert( is_int( $variant_comparison_id ), 'create archive variant comparison' );

$product_post = wp_insert_post(
    array(
        'post_type'     => 'post',
        'post_status'   => 'publish',
        'post_title'    => 'WeatherBeeta und LeMieux im Produktvergleich',
        'post_content'  => 'Fixture',
        'post_category' => array( (int) $child->term_id ),
    ),
    true
);
upc_archive_assert( ! is_wp_error( $product_post ), 'create published product-comparison archive fixture' );
update_post_meta( $product_post, '_upc_comparison_id', (string) $product_comparison_id );

$variant_post = wp_insert_post(
    array(
        'post_type'     => 'post',
        'post_status'   => 'publish',
        'post_title'    => 'WeatherBeeta Varianten im Vergleich',
        'post_content'  => 'Fixture',
        'post_category' => array( (int) $child->term_id ),
    ),
    true
);
upc_archive_assert( ! is_wp_error( $variant_post ), 'create published variant-comparison archive fixture' );
update_post_meta( $variant_post, '_upc_comparison_id', (string) $variant_comparison_id );

$group_post = wp_insert_post(
    array(
        'post_type'     => 'post',
        'post_status'   => 'publish',
        'post_title'    => 'Regendecken-Bauarten im Vergleich',
        'post_content'  => 'Fixture',
        'post_category' => array( (int) $child->term_id ),
    ),
    true
);
upc_archive_assert( ! is_wp_error( $group_post ), 'create legacy product-group comparison archive fixture' );

$archive = upc_archive();
upc_archive_assert( ! is_wp_error( $archive ), 'archive service available' );

$view = $archive->build_view( 'test-project', 'regendecken-vergleich' );
upc_archive_assert( ! is_wp_error( $view ), 'build bound comparison archive view' );
upc_archive_assert( 3 === count( $view['items'] ), 'archive contains three comparison kinds' );
upc_archive_assert( 2 === count( $view['products'] ), 'product index lists only concrete products with comparison content' );

$types = array();
foreach ( $view['items'] as $item ) {
    $types[] = $item['archive_type'] . ':' . $item['comparison_type'];
}
upc_archive_assert( in_array( 'product_group:', $types, true ), 'archive recognizes product-group comparison without UPC meta' );
upc_archive_assert( in_array( 'product_comparison:product', $types, true ), 'archive recognizes product comparison' );
upc_archive_assert( in_array( 'product_comparison:variant', $types, true ), 'archive recognizes variant comparison' );

$html = $archive->render( 'test-project', 'regendecken-vergleich' );
upc_archive_assert( ! is_wp_error( $html ), 'render archive HTML' );
upc_archive_assert( false !== strpos( $html, 'Produktgruppenvergleiche' ), 'main product-group filter present' );
upc_archive_assert( false !== strpos( $html, 'Produktvergleiche' ), 'main product-comparison filter present' );
upc_archive_assert( false !== strpos( $html, 'data-upc-subfilter="variant"' ), 'variant subfilter present' );
upc_archive_assert( false !== strpos( $html, 'Produkte mit Vergleichen' ), 'product index present' );
upc_archive_assert( false !== strpos( $html, 'Produkt suchen' ), 'product search present' );

$shortcode_html = do_shortcode(
    '[upc_comparison_archive project="test-project" category="regendecken-vergleich"]'
);
upc_archive_assert( $shortcode_html === $html, 'shortcode uses same deterministic archive renderer' );

$wrong_group_comparison_id = (int) $wpdb->get_var(
    $wpdb->prepare(
        "SELECT id FROM {$wpdb->prefix}upc_comparisons WHERE comparison_key = %s LIMIT 1",
        'alpha-vs-beta'
    )
);
upc_archive_assert( $wrong_group_comparison_id > 0, 'resolve wrong-group comparison fixture' );

$wrong_post = wp_insert_post(
    array(
        'post_type'     => 'post',
        'post_status'   => 'publish',
        'post_title'    => 'Wrong Group Fixture',
        'post_content'  => 'Fixture',
        'post_category' => array( (int) $child->term_id ),
    ),
    true
);
upc_archive_assert( ! is_wp_error( $wrong_post ), 'create wrong-group archive fixture' );
update_post_meta( $wrong_post, '_upc_comparison_id', (string) $wrong_group_comparison_id );

$blocked = $archive->build_view( 'test-project', 'regendecken-vergleich' );
upc_archive_assert(
    is_wp_error( $blocked ) && 'UPC_ARCHIVE_PRODUCT_GROUP_MISMATCH' === $blocked->get_error_code(),
    'archive blocks comparison assigned to wrong product-group category'
);

wp_delete_post( $wrong_post, true );

$restored = $archive->build_view( 'test-project', 'regendecken-vergleich' );
upc_archive_assert( ! is_wp_error( $restored ) && 3 === count( $restored['items'] ), 'archive recovers after invalid fixture removal' );

fwrite( STDOUT, "UPC_ARCHIVE_WORDPRESS_GESAMT_PASS\n" );
