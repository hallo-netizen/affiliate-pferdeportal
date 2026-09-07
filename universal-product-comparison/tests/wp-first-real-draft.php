<?php

if ( ! defined( 'ABSPATH' ) ) {
    fwrite( STDERR, "ABSPATH_MISSING\n" );
    exit( 1 );
}

function upc_first_assert( $condition, $label ) {
    if ( ! $condition ) {
        fwrite( STDERR, "FAIL: {$label}\n" );
        exit( 1 );
    }
    fwrite( STDOUT, "PASS: {$label}\n" );
}

global $wpdb;

$max_term = (int) $wpdb->get_var( "SELECT MAX(term_id) FROM {$wpdb->terms}" );
for ( $i = $max_term + 1; $i <= 10; $i++ ) {
    $dummy = wp_insert_term( 'UPC Dummy ' . $i, 'category', array( 'slug' => 'upc-dummy-' . $i ) );
    upc_first_assert( ! is_wp_error( $dummy ), 'create category filler ' . $i );
}

$live_category = wp_insert_term(
    'Vergleich Regendecken',
    'category',
    array(
        'slug'   => 'pferdedecken-regendecken-vergleich',
        'parent' => 0,
    )
);
upc_first_assert( ! is_wp_error( $live_category ), 'create exact bound comparison category' );
upc_first_assert( 11 === (int) $live_category['term_id'], 'bound comparison category has exact term ID 11' );

upc_first_assert( 0 === (int) $wpdb->get_var( "SELECT COUNT(*) FROM {$wpdb->prefix}upk_products" ), 'product store initially empty' );
upc_first_assert( 0 === (int) $wpdb->get_var( "SELECT COUNT(*) FROM {$wpdb->prefix}upc_comparisons" ), 'comparison store initially empty' );

$first = UPC_First_Draft_Test::execute();
if ( is_wp_error( $first ) ) {
    fwrite( STDERR, 'FIRST_EXECUTION_ERROR=' . $first->get_error_code() . ':' . $first->get_error_message() . "\n" );
}
upc_first_assert( ! is_wp_error( $first ), 'first bound PV-REG-001 execution succeeds' );
upc_first_assert( 'PV_REG_001_WORDPRESS_DRAFT_PASS' === $first['status'], 'first execution reaches bound draft PASS' );
upc_first_assert( false === $first['publish_allowed'], 'first execution forbids publish' );

$post = get_post( (int) $first['post_id'] );
upc_first_assert( $post && 'draft' === $post->post_status, 'first execution creates WordPress draft only' );
upc_first_assert( false !== strpos( $post->post_content, 'WeatherBeeta' ), 'draft contains bound WeatherBeeta identity' );
upc_first_assert( false !== strpos( $post->post_content, 'LeMieux' ), 'draft contains bound LeMieux identity' );
upc_first_assert( array( 11 ) === array_values( array_map( 'intval', wp_get_post_categories( $post->ID ) ) ), 'draft is assigned only to exact category term ID 11' );
upc_first_assert( '0' === (string) get_post_meta( $post->ID, '_upc_publish_allowed', true ), 'draft metadata forbids publish' );
upc_first_assert( 1 === substr_count( $post->post_content, '<figure class="upc-comparison-graphic"' ), 'draft contains exactly one deterministic graphic' );
upc_first_assert( hash( 'sha256', $post->post_content ) === $first['final_output_hash'], 'draft hash matches exact final bytes' );

upc_first_assert( 2 === (int) $wpdb->get_var( "SELECT COUNT(*) FROM {$wpdb->prefix}upk_products" ), 'first execution creates exactly two products' );
upc_first_assert( 28 === (int) $wpdb->get_var( "SELECT COUNT(*) FROM {$wpdb->prefix}upk_facts" ), 'first execution creates exactly 28 bound facts' );
upc_first_assert( 1 === (int) $wpdb->get_var( "SELECT COUNT(*) FROM {$wpdb->prefix}upc_comparisons" ), 'first execution creates exactly one comparison' );
upc_first_assert( 2 === (int) $wpdb->get_var( "SELECT COUNT(*) FROM {$wpdb->prefix}upc_items" ), 'first execution creates exactly two comparison items' );
upc_first_assert( 14 === (int) $wpdb->get_var( "SELECT COUNT(*) FROM {$wpdb->prefix}upc_features" ), 'first execution creates exactly 14 features' );

$second = UPC_First_Draft_Test::execute();
upc_first_assert( ! is_wp_error( $second ), 'second bound execution succeeds' );
upc_first_assert( (int) $second['comparison_id'] === (int) $first['comparison_id'], 'second execution reuses same comparison' );
upc_first_assert( (int) $second['post_id'] === (int) $first['post_id'], 'second execution reuses same WordPress draft' );
upc_first_assert( $second['final_output_hash'] === $first['final_output_hash'], 'second execution is byte-identical' );
upc_first_assert( 2 === (int) $wpdb->get_var( "SELECT COUNT(*) FROM {$wpdb->prefix}upk_products" ), 'second execution creates no duplicate products' );
upc_first_assert( 1 === (int) $wpdb->get_var( "SELECT COUNT(*) FROM {$wpdb->prefix}upc_comparisons" ), 'second execution creates no duplicate comparison' );

$dossier_path = dirname( __DIR__ ) . '/config/pferde-atelier/pv-reg-001.json';
$original = file_get_contents( $dossier_path );
file_put_contents( $dossier_path, $original . " " );
$tampered = UPC_First_Draft_Test::execute();
file_put_contents( $dossier_path, $original );
upc_first_assert(
    is_wp_error( $tampered ) && 'UPC_FIRST_TEST_DOSSIER_HASH_MISMATCH' === $tampered->get_error_code(),
    'tampered bound dossier is blocked'
);

$parent = wp_insert_term( 'UPC Wrong Parent', 'category', array( 'slug' => 'upc-wrong-parent' ) );
upc_first_assert( ! is_wp_error( $parent ), 'create wrong parent fixture' );
$reparent = wp_update_term( 11, 'category', array( 'parent' => (int) $parent['term_id'] ) );
upc_first_assert( ! is_wp_error( $reparent ), 'temporarily reparent bound category' );

$wrong_parent = UPC_First_Draft_Test::execute();
upc_first_assert(
    is_wp_error( $wrong_parent ) && 'UPC_CATEGORY_PARENT_MISMATCH' === $wrong_parent->get_error_code(),
    'wrong live category parent is blocked'
);

$restore = wp_update_term( 11, 'category', array( 'parent' => 0 ) );
upc_first_assert( ! is_wp_error( $restore ), 'restore exact flat live category' );

fwrite( STDOUT, "UPC_FIRST_REAL_DRAFT_GESAMT_PASS\n" );
