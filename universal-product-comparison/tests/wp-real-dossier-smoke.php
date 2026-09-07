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
