<?php
if ( ! defined( 'ABSPATH' ) ) {
    fwrite( STDERR, "ABSPATH_MISSING\n" );
    exit( 1 );
}

function upc_real_assert( $condition, $label ) {
    if ( ! $condition ) {
        fwrite( STDERR, "FAIL: {$label}\n" );
        exit( 1 );
    }
    fwrite( STDOUT, "PASS: {$label}\n" );
}

$fixture_path = __DIR__ . '/fixtures/pv-reg-001.json';
$fixture = json_decode( file_get_contents( $fixture_path ), true );
upc_real_assert( is_array( $fixture ), 'load PV-REG-001 fixture' );

$knowledge = upk_repository();
$compare   = upc_repository();
upc_real_assert( ! is_wp_error( $compare ), 'comparison repository available' );

$product_ids = array();

foreach ( $fixture['products'] as $product ) {
    $product_id = $knowledge->create_product(
        array(
            'manufacturer'             => $product['manufacturer'],
            'model_name'               => $product['model_name'],
            'product_group_key'        => $product['product_group_key'],
            'manufacturer_product_url' => $product['manufacturer_product_url'],
            'lifecycle_status'         => $product['lifecycle_status'],
            'last_verified_at'         => $product['last_verified_at'],
        )
    );
    upc_real_assert( is_int( $product_id ) && $product_id > 0, 'create real product ' . $product['manufacturer'] );

    foreach ( $product['facts'] as $fact ) {
        $fact_id = $knowledge->add_fact(
            UPK_Repository::SUBJECT_PRODUCT,
            $product_id,
            array(
                'fact_key'     => $fact['fact_key'],
                'fact_value'   => $fact['fact_value'],
                'source_url'   => $fact['source_url'],
                'source_type'  => $fact['source_type'],
                'verified_at'  => $fact['verified_at'],
                'fact_status'  => $fact['fact_status'],
            )
        );
        upc_real_assert( is_int( $fact_id ) && $fact_id > 0, 'store real fact ' . $product['manufacturer'] . ' / ' . $fact['fact_key'] );
    }

    $product_ids[] = $product_id;
}

$comparison_id = $compare->create_comparison(
    array(
        'comparison_key'     => strtolower( $fixture['dossier_id'] ),
        'comparison_type'    => $fixture['comparison_type'],
        'subject_ids'        => $product_ids,
        'working_title'      => $fixture['working_title'],
        'comparability_note' => $fixture['comparability_note'],
    )
);
upc_real_assert( is_int( $comparison_id ) && $comparison_id > 0, 'create PV-REG-001 comparison' );

$feature_count = $compare->set_features( $comparison_id, $fixture['features'] );
upc_real_assert( 14 === $feature_count, 'bind all 14 required dossier features' );

$valid = $compare->validate_required_facts( $comparison_id );
upc_real_assert( true === $valid, 'required facts complete including explicit NOT_IN_SOURCE / SOURCE_CONFLICT states' );

$bundle = $compare->get_comparison_bundle( $comparison_id );
upc_real_assert( ! is_wp_error( $bundle ), 'read full real dossier bundle' );
upc_real_assert( 14 === count( $bundle['feature_matrix'] ), 'read 14-row feature matrix' );
upc_real_assert( 2 === count( $bundle['items'] ), 'read two real products' );
upc_real_assert( 'WeatherBeeta' === $bundle['items'][0]['knowledge']['manufacturer'], 'preserve WeatherBeeta identity' );
upc_real_assert( 'LeMieux' === $bundle['items'][1]['knowledge']['manufacturer'], 'preserve LeMieux identity' );

$matrix_by_key = array();
foreach ( $bundle['feature_matrix'] as $row ) {
    $matrix_by_key[ $row['fact_key'] ] = $row;
}

$conflict = $matrix_by_key['waterproofness']['cells'][1]['facts'][0];
upc_real_assert( 'SOURCE_CONFLICT' === $conflict['fact_status'], 'preserve manufacturer source conflict' );
upc_real_assert(
    false !== strpos( $conflict['fact_value'], '10k/10.000 mm' )
    && false !== strpos( $conflict['fact_value'], '3.000 mm' ),
    'preserve conflicting values without smoothing'
);

$not_in_source_a = $matrix_by_key['care']['cells'][0]['facts'][0];
$not_in_source_b = $matrix_by_key['tail_flap']['cells'][1]['facts'][0];
upc_real_assert( 'NOT_IN_SOURCE' === $not_in_source_a['fact_status'], 'preserve WeatherBeeta NOT_IN_SOURCE' );
upc_real_assert( 'NOT_IN_SOURCE' === $not_in_source_b['fact_status'], 'preserve LeMieux NOT_IN_SOURCE' );

$writer_dossier = $compare->build_comparison_dossier( $comparison_id );
upc_real_assert( ! is_wp_error( $writer_dossier ), 'build deterministic writer dossier' );
upc_real_assert( 'READY_WITH_WARNINGS' === $writer_dossier['status'], 'real dossier exposes warnings instead of smoothing them' );
upc_real_assert( 14 === count( $writer_dossier['features'] ), 'writer dossier contains only 14 declared comparison features' );
upc_real_assert( 4 === count( $writer_dossier['warnings'] ), 'writer dossier exposes four real source warnings' );
$warning_codes = array_column( $writer_dossier['warnings'], 'code' );
upc_real_assert( in_array( 'SOURCE_CONFLICT', $warning_codes, true ), 'writer dossier exposes SOURCE_CONFLICT' );
upc_real_assert( in_array( 'NOT_IN_SOURCE', $warning_codes, true ), 'writer dossier exposes NOT_IN_SOURCE' );
upc_real_assert( ! isset( $writer_dossier['subjects'][0]['facts'] ), 'writer identity block does not duplicate product facts' );

upc_real_assert( ! function_exists( 'upc_writer' ), 'no public direct writer entry point' );

$production = upc_production();
upc_real_assert( ! is_wp_error( $production ), 'single-door production available' );

$unknown_ruleset = $production->execute( $comparison_id, 'pferde-atelier', 'not-bound' );
upc_real_assert(
    is_wp_error( $unknown_ruleset ) && 'UPC_RULESET_NOT_BOUND' === $unknown_ruleset->get_error_code(),
    'single door blocks unbound ruleset'
);

$draft = $production->execute( $comparison_id, 'pferde-atelier', 'pv-reg-001-v1' );
upc_real_assert( ! is_wp_error( $draft ), 'single door builds bound deterministic draft' );
upc_real_assert( 'DRAFT_READY_FOR_REVIEW' === $draft['status'], 'validated output becomes review-only draft' );
upc_real_assert( false === $draft['publish_allowed'], 'publish remains forbidden' );
upc_real_assert( false !== strpos( $draft['html'], '<h2>Vergleich auf einen Blick</h2>' ), 'comparison table placed high in draft' );
upc_real_assert( false !== strpos( $draft['html'], 'Bedeutung für die Entscheidung' ), 'table contains decision meaning column' );
upc_real_assert( false !== strpos( $draft['html'], 'Quellenkonflikt:' ), 'SOURCE_CONFLICT visible in article table' );
upc_real_assert( false !== strpos( $draft['html'], 'In der verwendeten Herstellerquelle nicht angegeben' ), 'NOT_IN_SOURCE visible in article table' );
upc_real_assert( false !== strpos( $draft['html'], '<h2>Vor- und Nachteile im direkten Vergleich</h2>' ), 'pros-cons section present' );
upc_real_assert( false !== strpos( $draft['html'], '<h2>Welches Produkt passt zu welchem Bedarf?</h2>' ), 'need-fit section present' );
upc_real_assert( false !== strpos( $draft['html'], 'Es gibt keinen pauschalen Sieger.' ), 'no universal winner in conclusion' );
upc_real_assert( false === strpos( $draft['html'], 'href=' ), 'article body contains no links' );

$first_html = $draft['html'];
$first_input_hash = $draft['input_hash'];
$first_output_hash = $draft['output_hash'];
$first_receipt_hash = $draft['receipt_hash'];
$golden_output_hash = '994d20136cebd169daa8a09f38248ee315552f8f63ea5f25c14995a01344828f';
upc_real_assert( $first_output_hash === $golden_output_hash, 'golden output hash matches approved article contract V1' );

$graphic = upc_comparison_graphic( $comparison_id );
upc_real_assert( ! is_wp_error( $graphic ), 'build deterministic neutral comparison graphic' );
upc_real_assert( 'GRAPHIC_READY' === $graphic['status'], 'comparison graphic reaches GRAPHIC_READY only from bound dossier' );
upc_real_assert( 'pv-reg-001.svg' === $graphic['filename'], 'comparison graphic filename is derived from stable comparison key' );
upc_real_assert( 'image/svg+xml' === $graphic['mime_type'], 'comparison graphic uses explicit SVG mime type' );
upc_real_assert( false !== strpos( $graphic['svg'], '<svg ' ), 'comparison graphic renders SVG root' );
upc_real_assert( false !== strpos( $graphic['svg'], 'WeatherBeeta' ), 'comparison graphic contains bound product A identity' );
upc_real_assert( false !== strpos( $graphic['svg'], 'LeMieux' ), 'comparison graphic contains bound product B identity' );
upc_real_assert( false === strpos( $graphic['svg'], '<image' ), 'comparison graphic contains no product image element' );
upc_real_assert( false === strpos( $graphic['svg'], '<script' ), 'comparison graphic contains no script' );
upc_real_assert( false === strpos( $graphic['svg'], 'href=' ), 'comparison graphic contains no link or external asset reference' );
upc_real_assert( false !== strpos( $graphic['svg'], 'Keine Rangliste' ), 'comparison graphic explicitly avoids ranking language' );
upc_real_assert( $graphic['svg_sha256'] === hash( 'sha256', $graphic['svg'] ), 'comparison graphic hash matches exact SVG bytes' );

for ( $i = 0; $i < 20; $i++ ) {
    $graphic_repeat = upc_comparison_graphic( $comparison_id );
    upc_real_assert( ! is_wp_error( $graphic_repeat ), 'deterministic graphic repeat ' . ( $i + 1 ) );
    if ( $graphic_repeat['svg'] !== $graphic['svg']
        || $graphic_repeat['input_hash'] !== $graphic['input_hash']
        || $graphic_repeat['svg_sha256'] !== $graphic['svg_sha256']
        || $graphic_repeat['filename'] !== $graphic['filename']
    ) {
        fwrite( STDERR, "FAIL: deterministic graphic repeat mismatch " . ( $i + 1 ) . "\n" );
        exit( 1 );
    }
}
fwrite( STDOUT, "PASS: 20/20 byte-identical deterministic comparison graphics\n" );

$invalid_graphic = upc_comparison_graphic( 0 );
upc_real_assert(
    is_wp_error( $invalid_graphic ) && 'UPC_GRAPHIC_COMPARISON_INVALID' === $invalid_graphic->get_error_code(),
    'comparison graphic blocks invalid unbound comparison id'
);

for ( $i = 0; $i < 100; $i++ ) {
    $repeat = $production->execute( $comparison_id, 'pferde-atelier', 'pv-reg-001-v1' );
    upc_real_assert( ! is_wp_error( $repeat ), 'deterministic repeat ' . ( $i + 1 ) );
    if ( $repeat['html'] !== $first_html
        || $repeat['input_hash'] !== $first_input_hash
        || $repeat['output_hash'] !== $first_output_hash
        || $repeat['receipt_hash'] !== $first_receipt_hash
    ) {
        fwrite( STDERR, "FAIL: deterministic repeat mismatch " . ( $i + 1 ) . "\n" );
        exit( 1 );
    }
}
fwrite( STDOUT, "PASS: 100/100 byte-identical deterministic renders\n" );

$parent_term = wp_insert_term(
    'Regendecken',
    'category',
    array( 'slug' => 'regendecken' )
);
upc_real_assert( ! is_wp_error( $parent_term ), 'create bound parent category for draft smoke' );

$child_term = wp_insert_term(
    'Vergleich',
    'category',
    array(
        'slug'   => 'regendecken-vergleich',
        'parent' => (int) $parent_term['term_id'],
    )
);
upc_real_assert( ! is_wp_error( $child_term ), 'create bound comparison category for draft smoke' );

$wp_draft = upc_wordpress_draft();
upc_real_assert( ! is_wp_error( $wp_draft ), 'WordPress draft materializer available' );

$materialized = $wp_draft->materialize( $comparison_id, 'test-project', 'pv-reg-001-v1' );
upc_real_assert( ! is_wp_error( $materialized ), 'materialize validated WordPress draft' );
upc_real_assert( 'WORDPRESS_DRAFT_VERIFIED' === $materialized['status'], 'WordPress draft readback verified' );
upc_real_assert( false === $materialized['publish_allowed'], 'WordPress materializer keeps publish forbidden' );
upc_real_assert( $golden_output_hash === $materialized['output_hash'], 'WordPress draft preserves golden output hash' );

$saved_post = get_post( (int) $materialized['post_id'] );
upc_real_assert( $saved_post && 'draft' === $saved_post->post_status, 'saved WordPress post status is exactly draft' );
upc_real_assert( $first_html === $saved_post->post_content, 'saved WordPress body is byte-identical renderer HTML' );
upc_real_assert( $first_output_hash === hash( 'sha256', $saved_post->post_content ), 'saved WordPress body hash matches renderer' );
upc_real_assert( '0' === (string) get_post_meta( $saved_post->ID, '_upc_publish_allowed', true ), 'saved WordPress metadata forbids publish' );

$materialized_again = $wp_draft->materialize( $comparison_id, 'test-project', 'pv-reg-001-v1' );
upc_real_assert( ! is_wp_error( $materialized_again ), 'repeat WordPress draft materialization succeeds' );
upc_real_assert( (int) $materialized_again['post_id'] === (int) $materialized['post_id'], 'repeat materialization reuses same bound draft' );
upc_real_assert(
    1 === count(
        get_posts(
            array(
                'post_type'      => 'post',
                'post_status'    => 'any',
                'posts_per_page' => -1,
                'fields'         => 'ids',
                'meta_key'       => '_upc_comparison_uid',
                'meta_value'     => $draft['comparison_uid'],
            )
        )
    ),
    'no duplicate WordPress comparison post created'
);

$publishing_path = dirname( __DIR__ ) . '/config/test-project/publishing.json';
$publishing_original = file_get_contents( $publishing_path );
file_put_contents( $publishing_path, $publishing_original . " " );
$tampered_publishing = $wp_draft->materialize( $comparison_id, 'test-project', 'pv-reg-001-v1' );
file_put_contents( $publishing_path, $publishing_original );
upc_real_assert(
    is_wp_error( $tampered_publishing ) && 'UPC_PUBLISHING_CONFIG_HASH_MISMATCH' === $tampered_publishing->get_error_code(),
    'tampered publishing config is blocked'
);

$ruleset_path = dirname( __DIR__ ) . '/config/pferde-atelier/rulesets/pv-reg-001-v1.json';
$ruleset_original = file_get_contents( $ruleset_path );
file_put_contents( $ruleset_path, $ruleset_original . " " );
$tampered_ruleset = $production->execute( $comparison_id, 'pferde-atelier', 'pv-reg-001-v1' );
file_put_contents( $ruleset_path, $ruleset_original );
upc_real_assert(
    is_wp_error( $tampered_ruleset ) && 'UPC_RULESET_HASH_MISMATCH' === $tampered_ruleset->get_error_code(),
    'tampered ruleset is blocked by manifest hash'
);

$knowledge->add_fact(
    UPK_Repository::SUBJECT_PRODUCT,
    $product_ids[0],
    array(
        'fact_key'    => 'outer_material_denier',
        'fact_value'  => '999D changed test value',
        'source_url'  => 'https://www.weatherbeetaeu.com/weatherbeeta-comfitec-plus-dynamic-turnout-0g-1029009000-950a5b',
        'source_type' => 'MANUFACTURER',
        'verified_at' => '2026-08-07',
        'fact_status' => 'VERIFIED',
    )
);
$changed_fact = $production->execute( $comparison_id, 'pferde-atelier', 'pv-reg-001-v1' );
upc_real_assert(
    is_wp_error( $changed_fact ) && 'UPC_DECISION_RULE_FACT_BINDING_MISMATCH' === $changed_fact->get_error_code(),
    'changed source fact blocks old approved decision rule'
);

$changed_fact_wp = $wp_draft->materialize( $comparison_id, 'test-project', 'pv-reg-001-v1' );
upc_real_assert(
    is_wp_error( $changed_fact_wp ) && 'UPC_DECISION_RULE_FACT_BINDING_MISMATCH' === $changed_fact_wp->get_error_code(),
    'WordPress draft layer cannot bypass changed-fact rule binding'
);

$missing_id = $compare->create_comparison(
    array(
        'comparison_key'     => 'pv-reg-001-missing-test',
        'comparison_type'    => 'PRODUCT',
        'subject_ids'        => $product_ids,
        'working_title'      => 'Missing required fact negative test',
        'comparability_note' => $fixture['comparability_note'],
    )
);
upc_real_assert( is_wp_error( $missing_id ) && 'UPC_DUPLICATE_COMPARISON' === $missing_id->get_error_code(), 'block duplicate real pair under another key' );

$second_a = $knowledge->create_product(
    array(
        'manufacturer'             => 'Fixture Maker A',
        'model_name'               => 'Missing A',
        'product_group_key'        => 'fixture-missing',
        'manufacturer_product_url' => 'https://manufacturer.example/missing-a',
        'lifecycle_status'         => 'ACTIVE',
    )
);
$second_b = $knowledge->create_product(
    array(
        'manufacturer'             => 'Fixture Maker B',
        'model_name'               => 'Missing B',
        'product_group_key'        => 'fixture-missing',
        'manufacturer_product_url' => 'https://manufacturer.example/missing-b',
        'lifecycle_status'         => 'ACTIVE',
    )
);
$missing_comparison = $compare->create_comparison(
    array(
        'comparison_key'  => 'missing-required-fact',
        'comparison_type' => 'PRODUCT',
        'subject_ids'     => array( $second_a, $second_b ),
    )
);
upc_real_assert( is_int( $missing_comparison ) && $missing_comparison > 0, 'create negative missing-fact comparison' );
$compare->set_features(
    $missing_comparison,
    array(
        array(
            'fact_key' => 'required_missing',
            'label'    => 'Required missing',
            'required' => true,
        ),
    )
);
$missing_validation = $compare->validate_required_facts( $missing_comparison );
upc_real_assert(
    is_wp_error( $missing_validation ) && 'UPC_REQUIRED_FACT_MISSING' === $missing_validation->get_error_code(),
    'block truly missing required fact'
);

$missing_dossier = $compare->build_comparison_dossier( $missing_comparison );
upc_real_assert(
    is_wp_error( $missing_dossier ) && 'UPC_REQUIRED_FACT_MISSING' === $missing_dossier->get_error_code(),
    'writer dossier fails closed on missing required fact'
);

fwrite( STDOUT, "UPC_REAL_DOSSIER_PV_REG_001_PASS\n" );
