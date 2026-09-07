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

$existing_product_posts = get_posts(
    array(
        'post_type'      => 'post',
        'post_status'    => 'any',
        'posts_per_page' => 2,
        'fields'         => 'ids',
        'meta_query'     => array(
            'relation' => 'AND',
            array(
                'key'   => '_upc_comparison_id',
                'value' => (string) $product_comparison_id,
            ),
            array(
                'key'   => '_upc_project_key',
                'value' => 'test-project',
            ),
        ),
    )
);
upc_archive_assert( count( $existing_product_posts ) <= 1, 'at most one pre-existing bound product-comparison post' );

if ( empty( $existing_product_posts ) ) {
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
    update_post_meta( $product_post, '_upc_project_key', 'test-project' );
} else {
    $product_post = (int) $existing_product_posts[0];
    $updated_product_post = wp_update_post(
        array(
            'ID'            => $product_post,
            'post_status'   => 'publish',
            'post_title'    => 'WeatherBeeta und LeMieux im Produktvergleich',
            'post_category' => array( (int) $child->term_id ),
        ),
        true
    );
    upc_archive_assert( ! is_wp_error( $updated_product_post ), 'reuse pre-existing bound product-comparison post' );
}

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
update_post_meta( $variant_post, '_upc_project_key', 'test-project' );

$product_link_manifest = upc_link_manifest( $product_comparison_id, 'test-project' );
upc_archive_assert( ! is_wp_error( $product_link_manifest ), 'build product-to-variant link manifest' );
upc_archive_assert( 1 === count( $product_link_manifest['entries'] ), 'product comparison resolves exactly one related variant comparison' );
upc_archive_assert( 'variant_comparison_for_product' === $product_link_manifest['entries'][0]['relation'], 'product comparison relation is variant comparison for product' );
upc_archive_assert( (int) $variant_comparison_id === (int) $product_link_manifest['entries'][0]['target_comparison_id'], 'product comparison links to exact variant comparison id' );

$variant_link_manifest = upc_link_manifest( $variant_comparison_id, 'test-project' );
upc_archive_assert( ! is_wp_error( $variant_link_manifest ), 'build variant-to-product link manifest' );
upc_archive_assert( 1 === count( $variant_link_manifest['entries'] ), 'variant comparison resolves exactly one related product comparison' );
upc_archive_assert( 'product_comparison_for_variant' === $variant_link_manifest['entries'][0]['relation'], 'variant comparison relation is product comparison for variant' );
upc_archive_assert( (int) $product_comparison_id === (int) $variant_link_manifest['entries'][0]['target_comparison_id'], 'variant comparison links back to exact product comparison id' );

$product_link_manifest_repeat = upc_link_manifest( $product_comparison_id, 'test-project' );
upc_archive_assert( $product_link_manifest_repeat['manifest_sha256'] === $product_link_manifest['manifest_sha256'], 'same project state produces identical link-manifest hash' );

$duplicate_variant_post = wp_insert_post(
    array(
        'post_type'     => 'post',
        'post_status'   => 'draft',
        'post_title'    => 'Duplicate Variant Target',
        'post_content'  => 'Fixture',
        'post_category' => array( (int) $child->term_id ),
    ),
    true
);
upc_archive_assert( ! is_wp_error( $duplicate_variant_post ), 'create duplicate target fixture' );
update_post_meta( $duplicate_variant_post, '_upc_comparison_id', (string) $variant_comparison_id );
update_post_meta( $duplicate_variant_post, '_upc_project_key', 'test-project' );

$duplicate_target_blocked = upc_link_manifest( $product_comparison_id, 'test-project' );
upc_archive_assert( is_wp_error( $duplicate_target_blocked ) && 'UPC_LINK_MANIFEST_DUPLICATE_TARGET_POST' === $duplicate_target_blocked->get_error_code(), 'link manifest blocks duplicate WordPress targets for same comparison' );
wp_delete_post( $duplicate_variant_post, true );

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

$shortcode_html = do_shortcode( '[upc_comparison_archive project="test-project" category="regendecken-vergleich"]' );
upc_archive_assert( $shortcode_html === $html, 'shortcode uses same deterministic archive renderer' );

$wrong_group_comparison_id = (int) $wpdb->get_var( $wpdb->prepare( "SELECT id FROM {$wpdb->prefix}upc_comparisons WHERE comparison_key = %s LIMIT 1", 'alpha-vs-beta' ) );
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
upc_archive_assert( is_wp_error( $blocked ) && 'UPC_ARCHIVE_PRODUCT_GROUP_MISMATCH' === $blocked->get_error_code(), 'archive blocks comparison assigned to wrong product-group category' );
wp_delete_post( $wrong_post, true );

$restored = $archive->build_view( 'test-project', 'regendecken-vergleich' );
upc_archive_assert( ! is_wp_error( $restored ) && 3 === count( $restored['items'] ), 'archive recovers after invalid fixture removal' );

$restored_fact_id = $knowledge->add_fact(
    UPK_Repository::SUBJECT_PRODUCT,
    $base_product_id,
    array(
        'fact_key'    => 'outer_material_denier',
        'fact_value'  => '1200D Ripstop; PFC-freie Guard-Tec-Beschichtung',
        'source_url'  => 'https://www.weatherbeetaeu.com/weatherbeeta-comfitec-plus-dynamic-turnout-0g-1029009000-950a5b',
        'source_type' => 'MANUFACTURER',
        'verified_at' => '2026-08-07',
        'fact_status' => 'VERIFIED',
    )
);
upc_archive_assert( is_int( $restored_fact_id ) && $restored_fact_id > 0, 'restore original manufacturer fact after prior negative test' );

$restored_core = upc_production()->execute( $product_comparison_id, 'pferde-atelier', 'pv-reg-001-v1' );
upc_archive_assert( ! is_wp_error( $restored_core ), 'restored manufacturer fact revalidates bound core before link finalization' );
upc_archive_assert( '994d20136cebd169daa8a09f38248ee315552f8f63ea5f25c14995a01344828f' === $restored_core['output_hash'], 'restored manufacturer fact returns to golden core output' );

$source_back_to_draft = wp_update_post( array( 'ID' => (int) $product_post, 'post_status' => 'draft' ), true );
upc_archive_assert( ! is_wp_error( $source_back_to_draft ), 'return bound product comparison to draft for link finalization test' );

$link_finalized = upc_finalize_internal_links( $product_comparison_id, 'test-project', 'pv-reg-001-v1' );
if ( is_wp_error( $link_finalized ) ) {
    fwrite( STDERR, 'LINK_FINALIZER_ERROR_CODE=' . $link_finalized->get_error_code() . "\n" );
    fwrite( STDERR, 'LINK_FINALIZER_ERROR_MESSAGE=' . $link_finalized->get_error_message() . "\n" );
    fwrite( STDERR, 'LINK_FINALIZER_ERROR_DATA=' . wp_json_encode( $link_finalized->get_error_data(), JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE ) . "\n" );
}
upc_archive_assert( ! is_wp_error( $link_finalized ), 'finalize bound internal links on validated draft' );
upc_archive_assert( 'WORDPRESS_DRAFT_LINKS_VERIFIED' === $link_finalized['status'], 'linked draft readback verified' );
upc_archive_assert( 1 === $link_finalized['link_count'], 'linked draft contains exactly one manifest-approved relation' );
upc_archive_assert( false === $link_finalized['publish_allowed'], 'link finalizer keeps publish forbidden' );

$link_finalized_post = get_post( (int) $product_post );
upc_archive_assert( $link_finalized_post && 'draft' === $link_finalized_post->post_status, 'link-finalized source remains draft' );
upc_archive_assert( false !== strpos( $link_finalized_post->post_content, '<h2>Passende Variantenvergleiche</h2>' ), 'fixed related-variant heading inserted' );
upc_archive_assert( 1 === substr_count( $link_finalized_post->post_content, '<a href=' ), 'exactly one internal anchor inserted' );
upc_archive_assert( false !== strpos( $link_finalized_post->post_content, get_permalink( (int) $variant_post ) ), 'anchor target equals manifest WordPress target' );

$link_finalized_repeat = upc_finalize_internal_links( $product_comparison_id, 'test-project', 'pv-reg-001-v1' );
upc_archive_assert( ! is_wp_error( $link_finalized_repeat ), 'repeat link finalization succeeds' );
upc_archive_assert( $link_finalized_repeat['linked_output_hash'] === $link_finalized['linked_output_hash'], 'repeat link finalization is byte-identical' );
upc_archive_assert( $link_finalized_repeat['link_manifest_sha256'] === $link_finalized['link_manifest_sha256'], 'repeat link finalization uses identical bound manifest' );

$article_finalized = upc_finalize_article( $product_comparison_id, 'test-project', 'pv-reg-001-v1' );
upc_archive_assert( ! is_wp_error( $article_finalized ), 'finalize bound article with links and neutral graphic' );
upc_archive_assert( 'WORDPRESS_DRAFT_FINAL_VERIFIED' === $article_finalized['status'], 'final article reaches verified draft state' );
upc_archive_assert( false === $article_finalized['publish_allowed'], 'final article remains non-publishable' );
upc_archive_assert( 1 === $article_finalized['link_count'], 'final article preserves exactly one bound internal relation' );
upc_archive_assert( 'pv-reg-001.svg' === $article_finalized['graphic_filename'], 'final article binds stable comparison graphic filename' );

$article_final_post = get_post( (int) $product_post );
upc_archive_assert( $article_final_post && 'draft' === $article_final_post->post_status, 'finalized article remains WordPress draft' );
upc_archive_assert( 1 === substr_count( $article_final_post->post_content, '<figure class="upc-comparison-graphic"' ), 'final article contains exactly one neutral comparison graphic' );
upc_archive_assert( false !== strpos( $article_final_post->post_content, '<h2>Passende Variantenvergleiche</h2>' ), 'final article preserves bound internal-link section' );
upc_archive_assert( 1 === substr_count( $article_final_post->post_content, '<a href=' ), 'final article contains only manifest-approved internal anchor' );
upc_archive_assert(
    $article_finalized['final_output_hash'] === hash( 'sha256', $article_final_post->post_content ),
    'final article hash matches exact WordPress draft bytes'
);
upc_archive_assert(
    $article_finalized['graphic_sha256'] === (string) get_post_meta( (int) $product_post, '_upc_graphic_sha256', true ),
    'final article stores exact bound graphic hash'
);
upc_archive_assert(
    '0' === (string) get_post_meta( (int) $product_post, '_upc_publish_allowed', true ),
    'final article metadata still forbids publish'
);

$article_finalized_repeat = upc_finalize_article( $product_comparison_id, 'test-project', 'pv-reg-001-v1' );
upc_archive_assert( ! is_wp_error( $article_finalized_repeat ), 'repeat full article finalization succeeds' );
upc_archive_assert(
    $article_finalized_repeat['final_output_hash'] === $article_finalized['final_output_hash'],
    'repeat full article finalization is byte-identical'
);
upc_archive_assert(
    $article_finalized_repeat['graphic_sha256'] === $article_finalized['graphic_sha256'],
    'repeat full article finalization uses identical graphic binding'
);

fwrite( STDOUT, "UPC_LINK_MANIFEST_WORDPRESS_GESAMT_PASS\n" );
fwrite( STDOUT, "UPC_LINK_FINALIZER_WORDPRESS_GESAMT_PASS\n" );
fwrite( STDOUT, "UPC_ARCHIVE_WORDPRESS_GESAMT_PASS\n" );
