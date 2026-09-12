<?php

define( 'ABSPATH', __DIR__ . '/' );

class WP_Error {
    private $code;
    public function __construct( $code, $message = '' ) { $this->code = $code; }
    public function get_error_code() { return $this->code; }
}
function is_wp_error( $value ) { return $value instanceof WP_Error; }
function absint( $value ) { return abs( (int) $value ); }
function sanitize_text_field( $value ) { return trim( strip_tags( (string) $value ) ); }
function sanitize_textarea_field( $value ) { return trim( strip_tags( (string) $value ) ); }
function sanitize_key( $value ) { return strtolower( preg_replace( '/[^a-z0-9_\-]/', '', (string) $value ) ); }
function current_time( $type, $gmt = false ) { return '2026-09-12 09:30:00'; }

class UPK_Repository {
    const SUBJECT_PRODUCT = 'product';
    const SUBJECT_VARIANT = 'variant';
}

class Research_Core_Fake_Knowledge {
    public $products = array();
    public function get_product_bundle( $id ) {
        if ( ! isset( $this->products[ $id ] ) ) {
            return new WP_Error( 'UPK_PRODUCT_NOT_FOUND', 'missing' );
        }
        return $this->products[ $id ];
    }
    public function get_variant_bundle( $id ) { return new WP_Error( 'UPK_VARIANT_NOT_FOUND', 'missing' ); }
}

class Research_Core_Fake_WPDB {
    public $prefix = 'wp_';
    public $last_error = '';
    public $insert_id = 0;
    public $comparisons = array();
    public $items = array();

    public function prepare( $query, ...$args ) { return array( 'query' => $query, 'args' => $args ); }
    public function get_var( $prepared ) {
        if ( false !== strpos( $prepared['query'], 'WHERE set_hash = %s' ) ) {
            $hash = (string) $prepared['args'][0];
            foreach ( $this->comparisons as $id => $row ) {
                if ( $row['set_hash'] === $hash ) { return $id; }
            }
        }
        return null;
    }
    public function insert( $table, $data, $formats ) {
        if ( 'wp_upc_comparisons' === $table ) {
            $this->insert_id++;
            $this->comparisons[ $this->insert_id ] = $data;
            return 1;
        }
        if ( 'wp_upc_items' === $table ) {
            $this->items[] = $data;
            return 1;
        }
        return false;
    }
    public function delete( $table, $where, $formats ) { return 1; }
}

function research_core_assert( $condition, $label ) {
    if ( ! $condition ) {
        fwrite( STDERR, "FAIL: {$label}\n" );
        exit( 1 );
    }
    fwrite( STDOUT, "PASS: {$label}\n" );
}

require_once dirname( __DIR__ ) . '/src/class-upc-repository.php';

$knowledge = new Research_Core_Fake_Knowledge();
foreach ( array( 1, 2, 3, 4 ) as $id ) {
    $knowledge->products[ $id ] = array(
        'manufacturer' => 'Same Brand',
        'model_name' => 'Model ' . $id,
        'product_group_key' => 'regendecken',
    );
}
$knowledge->products[5] = array(
    'manufacturer' => 'Other Brand',
    'model_name' => 'Other Group',
    'product_group_key' => 'winterdecken',
);
$knowledge->products[6] = array(
    'manufacturer' => 'Other Brand',
    'model_name' => 'Cross Brand',
    'product_group_key' => 'regendecken',
);

$wpdb = new Research_Core_Fake_WPDB();
$repo = new UPC_Repository( $wpdb, $knowledge );

$id = $repo->create_comparison( array(
    'comparison_key' => 'same-brand-two',
    'comparison_type' => 'PRODUCT',
    'comparison_mode' => 'TIER_SAME_BRAND',
    'subject_ids' => array( 1, 2 ),
    'working_title' => 'Same Brand 1 vs 2',
) );
research_core_assert( is_int( $id ) && $id > 0, 'same-brand product comparison allowed' );
research_core_assert( 'TIER_SAME_BRAND' === $wpdb->comparisons[ $id ]['comparison_mode'], 'research comparison mode stored separately' );

$id4 = $repo->create_comparison( array(
    'comparison_key' => 'same-brand-four',
    'comparison_type' => 'PRODUCT',
    'comparison_mode' => 'DIRECT_EXACT_MULTI',
    'subject_ids' => array( 1, 2, 3, 4 ),
) );
research_core_assert( is_int( $id4 ) && $id4 > 0, 'four-product researched comparison allowed' );

$cross = $repo->create_comparison( array(
    'comparison_key' => 'cross-brand',
    'comparison_type' => 'PRODUCT',
    'comparison_mode' => 'DIRECT_EXACT',
    'subject_ids' => array( 3, 6 ),
) );
research_core_assert( is_int( $cross ) && $cross > 0, 'cross-brand comparison regression pass' );

$legacy = $repo->create_comparison( array(
    'comparison_key' => 'legacy-no-mode',
    'comparison_type' => 'PRODUCT',
    'subject_ids' => array( 2, 6 ),
) );
research_core_assert( is_int( $legacy ) && '' === $wpdb->comparisons[ $legacy ]['comparison_mode'], 'legacy comparison without mode stays backward compatible' );

$bad_mode = $repo->create_comparison( array(
    'comparison_key' => 'bad-mode',
    'comparison_type' => 'PRODUCT',
    'comparison_mode' => 'DIRECT EXACT',
    'subject_ids' => array( 1, 6 ),
) );
research_core_assert( is_wp_error( $bad_mode ) && 'UPC_INVALID_COMPARISON_MODE' === $bad_mode->get_error_code(), 'invalid comparison mode blocked' );

$group_mismatch = $repo->create_comparison( array(
    'comparison_key' => 'group-mismatch',
    'comparison_type' => 'PRODUCT',
    'comparison_mode' => 'DIRECT_EXACT',
    'subject_ids' => array( 1, 5 ),
) );
research_core_assert( is_wp_error( $group_mismatch ) && 'UPC_PRODUCT_GROUP_MISMATCH' === $group_mismatch->get_error_code(), 'different product groups still blocked' );

$duplicate_item = $repo->create_comparison( array(
    'comparison_key' => 'duplicate-item',
    'comparison_type' => 'PRODUCT',
    'subject_ids' => array( 1, 1 ),
) );
research_core_assert( is_wp_error( $duplicate_item ) && 'UPC_DUPLICATE_OR_INVALID_ITEM' === $duplicate_item->get_error_code(), 'duplicate product inside comparison blocked' );

$too_many = $repo->create_comparison( array(
    'comparison_key' => 'too-many',
    'comparison_type' => 'PRODUCT',
    'subject_ids' => array( 1, 2, 3, 4, 6 ),
) );
research_core_assert( is_wp_error( $too_many ) && 'UPC_INVALID_ITEM_COUNT' === $too_many->get_error_code(), 'more than four products blocked' );

$reordered_duplicate = $repo->create_comparison( array(
    'comparison_key' => 'same-brand-two-reordered',
    'comparison_type' => 'PRODUCT',
    'comparison_mode' => 'DIRECT_SAME_BRAND',
    'subject_ids' => array( 2, 1 ),
) );
research_core_assert( is_wp_error( $reordered_duplicate ) && 'UPC_DUPLICATE_COMPARISON' === $reordered_duplicate->get_error_code(), 'same product set remains duplicate regardless mode or order' );

fwrite( STDOUT, "UPC_RESEARCH_COMPARISON_CORE_GESAMT_PASS\n" );
