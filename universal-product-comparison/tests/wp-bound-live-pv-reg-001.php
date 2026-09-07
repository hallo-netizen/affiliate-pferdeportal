<?php
if ( ! defined( 'ABSPATH' ) ) {
    fwrite( STDERR, "ABSPATH_MISSING\n" );
    exit( 1 );
}

function upc_bound_assert( $condition, $label ) {
    if ( ! $condition ) {
        fwrite( STDERR, "FAIL: {$label}\n" );
        exit( 1 );
    }
    fwrite( STDOUT, "PASS: {$label}\n" );
}

global $wpdb;

upc_bound_assert( function_exists( 'upc_repository' ), 'comparison repository function available' );
upc_bound_assert( class_exists( 'UPC_Bound_Dossier_Importer' ), 'bound dossier importer available' );
upc_bound_assert( class_exists( 'UPC_Admin_PV_REG_001_Test' ), 'bound admin test class available' );

$max_term = (int) $wpdb->get_var( "SELECT MAX(term_id) FROM {$wpdb->terms}" );
for ( $i = $max_term + 1; $i <= 10; $i++ ) {
    $dummy = wp_insert_term( 'Dummy ' . $i, 'category', array( 'slug' => 'dummy-' . $i ) );
    upc_bound_assert( ! is_wp_error( $dummy ), 'create term filler ' . $i );
}

$live_category = wp_insert_term(
    'Vergleich Regendecken',
    'category',
    array(
        'slug'   => 'pferdedecken-regendecken-vergleich',
        'parent' => 0,
    )
);
upc_bound_assert( ! is_wp_error( $live_category ), 'create exact live comparison category fixture' );
upc_bound_assert( 11 === (int) $live_category['term_id'], 'live comparison category fixture is exact term ID 11' );

$repository = upc_repository();
$importer   = new UPC_Bound_Dossier_Importer( $repository, upk_repository(), $wpdb );

$first = $importer->import( 'pferde-atelier', 'pv-reg-001' );
upc_bound_assert( ! is_wp_error( $first ), 'fresh bound PV-REG-001 import succeeds' );
upc_bound_assert( 'BOUND_DOSSIER_IMPORTED' === $first['status'], 'first import reports imported state' );
$comparison_id = (int) $first['comparison_id'];
upc_bound_assert( $comparison_id > 0, 'first import returns comparison id' );

upc_bound_assert( 2 === (int) $wpdb->get_var( "SELECT COUNT(*) FROM {$wpdb->prefix}upk_products" ), 'fresh import creates exactly two products' );
upc_bound_assert( 28 === (int) $wpdb->get_var( "SELECT COUNT(*) FROM {$wpdb->prefix}upk_facts" ), 'fresh import creates exactly 28 source-bound facts' );
upc_bound_assert( 1 === (int) $wpdb->get_var( "SELECT COUNT(*) FROM {$wpdb->prefix}upc_comparisons" ), 'fresh import creates exactly one comparison' );
upc_bound_assert( 2 === (int) $wpdb->get_var( "SELECT COUNT(*) FROM {$wpdb->prefix}upc_items" ), 'fresh import creates exactly two comparison items' );
upc_bound_assert( 14 === (int) $wpdb->get_var( "SELECT COUNT(*) FROM {$wpdb->prefix}upc_features" ), 'fresh import creates exactly 14 comparison features' );

$second = $importer->import( 'pferde-atelier', 'pv-reg-001' );
upc_bound_assert( ! is_wp_error( $second ), 'repeat bound import succeeds' );
upc_bound_assert( 'BOUND_DOSSIER_REUSED' === $second['status'], 'repeat import reuses exact bound comparison' );
upc_bound_assert( $comparison_id === (int) $second['comparison_id'], 'repeat import keeps same comparison id' );
upc_bound_assert( 2 === (int) $wpdb->get_var( "SELECT COUNT(*) FROM {$wpdb->prefix}upk_products" ), 'repeat import creates no duplicate products' );
upc_bound_assert( 1 === (int) $wpdb->get_var( "SELECT COUNT(*) FROM {$wpdb->prefix}upc_comparisons" ), 'repeat import creates no duplicate comparison' );

$final = upc_finalize_article( $comparison_id, 'pferde-atelier', 'pv-reg-001-v1' );
upc_bound_assert( ! is_wp_error( $final ), 'fresh live-bound final draft succeeds' );
upc_bound_assert( 'WORDPRESS_DRAFT_FINAL_VERIFIED' === $final['status'], 'final draft reaches verified state' );
upc_bound_assert( false === $final['publish_allowed'], 'final draft remains non-publishable' );

$post = get_post( (int) $final['post_id'] );
upc_bound_assert( $post && 'draft' === $post->post_status, 'real bound test creates WordPress draft only' );
upc_bound_assert( false !== strpos( $post->post_content, 'WeatherBeeta' ), 'real bound draft contains product A' );
upc_bound_assert( false !== strpos( $post->post_content, 'LeMieux' ), 'real bound draft contains product B' );
upc_bound_assert( 1 === substr_count( $post->post_content, '<figure class="upc-comparison-graphic"' ), 'real bound draft contains exactly one neutral graphic' );
upc_bound_assert( array( 11 ) === array_values( array_map( 'intval', wp_get_post_categories( $post->ID ) ) ), 'real bound draft uses exact live category term ID 11' );
upc_bound_assert( '0' === (string) get_post_meta( $post->ID, '_upc_publish_allowed', true ), 'real bound draft metadata forbids publish' );

$final_repeat = upc_finalize_article( $comparison_id, 'pferde-atelier', 'pv-reg-001-v1' );
upc_bound_assert( ! is_wp_error( $final_repeat ), 'repeat final draft succeeds' );
upc_bound_assert( (int) $final_repeat['post_id'] === (int) $final['post_id'], 'repeat finalization reuses same WordPress draft' );
upc_bound_assert( $final_repeat['final_output_hash'] === $final['final_output_hash'], 'repeat finalization is byte-identical' );

$dossier_path = dirname( __DIR__ ) . '/config/pferde-atelier/dossiers/pv-reg-001.json';
$original = file_get_contents( $dossier_path );
file_put_contents( $dossier_path, $original . " " );
$tampered = $importer->import( 'pferde-atelier', 'pv-reg-001' );
file_put_contents( $dossier_path, $original );
upc_bound_assert(
    is_wp_error( $tampered ) && 'UPC_BOUND_DOSSIER_HASH_MISMATCH' === $tampered->get_error_code(),
    'tampered bound dossier is blocked before reuse'
);

fwrite( STDOUT, "UPC_BOUND_LIVE_PV_REG_001_GESAMT_PASS\n" );
