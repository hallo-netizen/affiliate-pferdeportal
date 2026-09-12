<?php

$path = dirname( __DIR__ ) . '/config/pferde-atelier/maintenance-groups.json';
if ( ! is_file( $path ) ) {
    fwrite( STDERR, "FAIL: maintenance policy missing\n" );
    exit( 1 );
}

$data = json_decode( file_get_contents( $path ), true );
if ( ! is_array( $data ) ) {
    fwrite( STDERR, "FAIL: maintenance policy invalid json\n" );
    exit( 1 );
}

function policy_assert( $condition, $label ) {
    if ( ! $condition ) {
        fwrite( STDERR, "FAIL: {$label}\n" );
        exit( 1 );
    }
    fwrite( STDOUT, "PASS: {$label}\n" );
}

policy_assert( '1' === (string) ( $data['schema_version'] ?? '' ), 'schema version bound' );
policy_assert( 'pferde-atelier' === (string) ( $data['project_key'] ?? '' ), 'project key bound' );
policy_assert( 4 === (int) ( $data['market_gate']['minimum_independent_dossiers'] ?? 0 ), 'four independent dossier market gate bound' );
policy_assert( true === ( $data['market_gate']['exact_product_identity_required'] ?? null ), 'exact identity required' );
policy_assert( true === ( $data['market_gate']['official_manufacturer_sources_required'] ?? null ), 'official manufacturer source required' );
policy_assert( true === ( $data['market_gate']['comparability_gate_required'] ?? null ), 'comparability gate required' );
policy_assert( false === ( $data['market_gate']['rejected_candidate_signals_persisted'] ?? null ), 'rejected candidate signals are not persisted' );

$groups = isset( $data['groups'] ) && is_array( $data['groups'] ) ? $data['groups'] : array();
policy_assert( 17 === count( $groups ), 'exactly 17 released research groups bound' );

$keys = array();
$six = 0;
$twelve = 0;
$extra = 0;
$regendecken = null;

foreach ( $groups as $group ) {
    $key = isset( $group['product_group_key'] ) ? (string) $group['product_group_key'] : '';
    policy_assert( '' !== $key, 'group key present: ' . (string) ( $group['product_page'] ?? '?' ) );
    policy_assert( ! isset( $keys[ $key ] ), 'group key unique: ' . $key );
    $keys[ $key ] = true;

    $refresh = (int) ( $group['refresh_months'] ?? 0 );
    policy_assert( in_array( $refresh, array( 6, 12 ), true ), 'refresh only 6M or 12M: ' . $key );
    if ( 6 === $refresh ) {
        $six++;
    } else {
        $twelve++;
    }

    $contracts = isset( $group['required_additional_contracts'] ) && is_array( $group['required_additional_contracts'] )
        ? $group['required_additional_contracts']
        : array();
    if ( ! empty( $contracts ) ) {
        policy_assert( array( 'SAFETY_FIT_ADDITIONAL_CONTRACT' ) === array_values( $contracts ), 'only approved safety/fit additional contract used: ' . $key );
        $extra++;
    }

    if ( 'regendecken' === $key ) {
        $regendecken = $group;
    }
}

policy_assert( 4 === $six, 'four research groups use 6M refresh' );
policy_assert( 13 === $twelve, 'thirteen research groups use 12M refresh' );
policy_assert( 2 === $extra, 'two groups require safety/fit additional contract' );
policy_assert( is_array( $regendecken ), 'existing regendecken group key preserved' );
policy_assert( 12 === (int) $regendecken['refresh_months'], 'regendecken research refresh is 12M' );
policy_assert( 'Produktvergleiche Regendecken' === (string) $regendecken['level4_category'], 'regendecken level-4 category bound' );

fwrite( STDOUT, "UPC_MAINTENANCE_POLICY_GESAMT_PASS\n" );
