<?php

define( 'ABSPATH', __DIR__ . '/' );

class WP_Error {
    private $code;
    public function __construct( $code, $message = '' ) { $this->code = $code; }
    public function get_error_code() { return $this->code; }
}
function is_wp_error( $value ) { return $value instanceof WP_Error; }
function absint( $value ) { return abs( (int) $value ); }

class UPK_Repository {
    const SUBJECT_PRODUCT = 'product';
    const SUBJECT_VARIANT = 'variant';
}

class Fingerprint_Fake_Knowledge {
    public $product_bundle;
    public $variant_bundle;
    public function get_product_bundle( $id ) { return $this->product_bundle; }
    public function get_variant_bundle( $id ) { return $this->variant_bundle; }
}

function fingerprint_assert( $condition, $label ) {
    if ( ! $condition ) {
        fwrite( STDERR, "FAIL: {$label}\n" );
        exit( 1 );
    }
    fwrite( STDOUT, "PASS: {$label}\n" );
}

require_once dirname( __DIR__ ) . '/src/class-upk-change-fingerprint.php';

$knowledge = new Fingerprint_Fake_Knowledge();
$knowledge->product_bundle = array(
    'manufacturer' => 'Maker A',
    'model_name' => 'Model One',
    'model_family' => 'Family One',
    'product_group_key' => 'rain-rug',
    'manufacturer_product_url' => 'https://maker.example/model-one',
    'generation' => '2026',
    'lifecycle_status' => 'ACTIVE',
    'successor_product_id' => null,
    'identifiers' => array(
        array( 'identifier_type' => 'MPN', 'identifier_value' => 'M-1' ),
        array( 'identifier_type' => 'EAN', 'identifier_value' => '4000000000001' ),
    ),
    'facts' => array(
        array(
            'fact_key' => 'denier', 'fact_value' => '1200', 'fact_note' => '', 'unit' => 'D',
            'source_url' => 'https://maker.example/model-one', 'source_type' => 'MANUFACTURER',
            'verified_at' => '2026-09-01 10:00:00', 'fact_status' => 'VERIFIED',
        ),
        array(
            'fact_key' => 'fill', 'fact_value' => '0', 'fact_note' => '', 'unit' => 'g',
            'source_url' => 'https://maker.example/model-one', 'source_type' => 'MANUFACTURER',
            'verified_at' => '2026-09-01 10:00:00', 'fact_status' => 'VERIFIED',
        ),
    ),
);

$fingerprint = new UPK_Change_Fingerprint( $knowledge );
$hash_a = $fingerprint->product( 1 );
fingerprint_assert( is_string( $hash_a ) && 64 === strlen( $hash_a ), 'positive product fingerprint' );

$knowledge->product_bundle['facts'][0]['verified_at'] = '2027-03-01 10:00:00';
$knowledge->product_bundle['facts'][1]['verified_at'] = '2027-03-01 10:00:00';
$hash_reverified = $fingerprint->product( 1 );
fingerprint_assert( $hash_a === $hash_reverified, 'reverification timestamp alone does not trigger change' );

$knowledge->product_bundle['identifiers'] = array_reverse( $knowledge->product_bundle['identifiers'] );
$knowledge->product_bundle['facts'] = array_reverse( $knowledge->product_bundle['facts'] );
$hash_reordered = $fingerprint->product( 1 );
fingerprint_assert( $hash_a === $hash_reordered, 'source record order does not trigger change' );

$knowledge->product_bundle['facts'][0]['fact_value'] = '50';
$hash_fact_changed = $fingerprint->product( 1 );
fingerprint_assert( $hash_a !== $hash_fact_changed, 'fact value change triggers fingerprint change' );

$knowledge->product_bundle['facts'][0]['fact_value'] = '0';
$knowledge->product_bundle['facts'][0]['fact_note'] = 'Nicht glätten.';
$hash_note_changed = $fingerprint->product( 1 );
fingerprint_assert( $hash_a !== $hash_note_changed, 'fact note change triggers fingerprint change' );

$knowledge->product_bundle['facts'][0]['fact_note'] = '';
$knowledge->product_bundle['lifecycle_status'] = 'DISCONTINUED';
$hash_lifecycle_changed = $fingerprint->product( 1 );
fingerprint_assert( $hash_a !== $hash_lifecycle_changed, 'lifecycle change triggers fingerprint change' );

$knowledge->variant_bundle = array(
    'product_id' => 1,
    'variant_name' => '0 g',
    'variant_key' => '0g',
    'lifecycle_status' => 'ACTIVE',
    'identifiers' => array( array( 'identifier_type' => 'EAN', 'identifier_value' => '4000000000018' ) ),
    'facts' => array(
        array(
            'fact_key' => 'fill', 'fact_value' => '0', 'fact_note' => '', 'unit' => 'g',
            'source_url' => 'https://maker.example/model-one-0g', 'source_type' => 'MANUFACTURER',
            'verified_at' => '2026-09-01 10:00:00', 'fact_status' => 'VERIFIED',
        ),
    ),
    'product' => array(
        'manufacturer' => 'Maker A',
        'model_name' => 'Model One',
        'product_group_key' => 'rain-rug',
        'generation' => '2026',
        'lifecycle_status' => 'ACTIVE',
    ),
);

$variant_hash_a = $fingerprint->variant( 10 );
$knowledge->variant_bundle['facts'][0]['verified_at'] = '2027-03-01 10:00:00';
$variant_hash_reverified = $fingerprint->variant( 10 );
fingerprint_assert( $variant_hash_a === $variant_hash_reverified, 'variant reverification timestamp alone does not trigger change' );

$knowledge->variant_bundle['product']['model_name'] = 'Model One New Generation';
$variant_hash_product_identity_changed = $fingerprint->variant( 10 );
fingerprint_assert( $variant_hash_a !== $variant_hash_product_identity_changed, 'base product identity change triggers variant comparison review' );

fwrite( STDOUT, "UPK_CHANGE_FINGERPRINT_GESAMT_PASS\n" );
