<?php

define( 'ABSPATH', __DIR__ . '/' );

class WP_Error {
    private $code;
    public function __construct( $code, $message = '' ) {
        $this->code = $code;
    }
    public function get_error_code() {
        return $this->code;
    }
}

function is_wp_error( $value ) {
    return $value instanceof WP_Error;
}
function absint( $value ) {
    return abs( (int) $value );
}
function sanitize_key( $value ) {
    return strtolower( preg_replace( '/[^a-z0-9_\-]/', '', (string) $value ) );
}
function sanitize_text_field( $value ) {
    return trim( strip_tags( (string) $value ) );
}
function esc_url_raw( $value ) {
    $value = trim( (string) $value );
    return filter_var( $value, FILTER_VALIDATE_URL ) ? $value : '';
}
function current_time( $type, $gmt = false ) {
    return '2026-09-12 08:00:00';
}

class UPK_Repository {
    const SUBJECT_PRODUCT = 'product';
    const SUBJECT_VARIANT = 'variant';
    public static function lifecycle_statuses() {
        return array( 'ACTIVE', 'TEMPORARILY_UNAVAILABLE', 'DISCONTINUED', 'UNKNOWN' );
    }
}

class Maintenance_Fake_WPDB {
    public $prefix = 'wp_';
    public $last_error = '';
    public $products = array( 1 => true, 2 => true );
    public $variants = array( 10 => 1, 11 => 1 );
    public $last_update = null;
    public $last_get_col_prepared = null;
    public $update_count = 0;

    public function prepare( $query, ...$args ) {
        return array( 'query' => $query, 'args' => $args );
    }

    public function get_var( $prepared ) {
        $query = $prepared['query'];
        $id = isset( $prepared['args'][0] ) ? (int) $prepared['args'][0] : 0;
        if ( false !== strpos( $query, 'wp_upk_products' ) ) {
            return isset( $this->products[ $id ] ) ? $id : null;
        }
        if ( false !== strpos( $query, 'wp_upk_variants' ) ) {
            return isset( $this->variants[ $id ] ) ? $id : null;
        }
        return null;
    }

    public function update( $table, $data, $where, $formats, $where_formats ) {
        $this->update_count++;
        $this->last_update = array(
            'table' => $table,
            'data' => $data,
            'where' => $where,
            'formats' => $formats,
            'where_formats' => $where_formats,
        );
        return 1;
    }

    public function get_col( $prepared ) {
        $this->last_get_col_prepared = $prepared;
        $query = $prepared['query'];
        $args = $prepared['args'];

        if ( false !== strpos( $query, 'manufacturer = %s' ) && false !== strpos( $query, 'model_name = %s' ) ) {
            if ( isset( $args[0] ) && 'Maker A' === $args[0] ) {
                return array( '1' );
            }
            if ( isset( $args[0] ) && 'Duplicate Maker' === $args[0] ) {
                return array( '1', '2' );
            }
            return array();
        }

        if ( false !== strpos( $query, 'SELECT id FROM wp_upk_products' ) ) {
            if ( false !== strpos( $query, 'product_group_key = %s' ) ) {
                return array( '1' );
            }
            return array( '2', '1' );
        }
        if ( false !== strpos( $query, 'SELECT DISTINCT i.comparison_id' ) ) {
            return array( '5', '3', '5' );
        }
        if ( false !== strpos( $query, 'SELECT DISTINCT comparison_id' ) ) {
            return array( '5', '5' );
        }
        return array();
    }
}

function maintenance_assert( $condition, $label ) {
    if ( ! $condition ) {
        fwrite( STDERR, "FAIL: {$label}\n" );
        exit( 1 );
    }
    fwrite( STDOUT, "PASS: {$label}\n" );
}

require_once dirname( __DIR__, 2 ) . '/universal-product-knowledge/src/class-upk-maintenance.php';
require_once dirname( __DIR__ ) . '/src/class-upc-maintenance.php';

$wpdb = new Maintenance_Fake_WPDB();
$upk = new UPK_Maintenance( $wpdb );

$result = $upk->update_product( 1, array(
    'lifecycle_status' => 'DISCONTINUED',
    'manufacturer_product_url' => 'https://manufacturer.example/model-alpha-new',
    'successor_product_id' => 2,
    'last_verified_at' => '2026-09-01 12:00:00',
) );
maintenance_assert( 1 === $result, 'positive product update' );
maintenance_assert( 'wp_upk_products' === $wpdb->last_update['table'], 'product update uses existing product table' );
maintenance_assert( 'DISCONTINUED' === $wpdb->last_update['data']['lifecycle_status'], 'product lifecycle updated' );
maintenance_assert( 2 === $wpdb->last_update['data']['successor_product_id'], 'successor binding updated' );
maintenance_assert( '2026-09-01 12:00:00' === $wpdb->last_update['data']['last_verified_at'], 'verification timestamp updated' );

$result = $upk->update_product( 1, array( 'lifecycle_status' => 'BROKEN' ) );
maintenance_assert( is_wp_error( $result ) && 'UPK_INVALID_LIFECYCLE_STATUS' === $result->get_error_code(), 'negative invalid lifecycle blocked' );

$result = $upk->update_product( 1, array( 'successor_product_id' => 1 ) );
maintenance_assert( is_wp_error( $result ) && 'UPK_SUCCESSOR_PRODUCT_INVALID' === $result->get_error_code(), 'negative self successor blocked' );

$result = $upk->update_product( 1, array( 'successor_product_id' => 999 ) );
maintenance_assert( is_wp_error( $result ) && 'UPK_SUCCESSOR_PRODUCT_NOT_FOUND' === $result->get_error_code(), 'negative missing successor blocked' );

$result = $upk->update_product( 1, array( 'manufacturer_product_url' => 'not-a-url' ) );
maintenance_assert( is_wp_error( $result ) && 'UPK_PRODUCT_SOURCE_URL_INVALID' === $result->get_error_code(), 'negative invalid product source blocked' );

$result = $upk->update_product( 999, array( 'lifecycle_status' => 'ACTIVE' ) );
maintenance_assert( is_wp_error( $result ) && 'UPK_PRODUCT_NOT_FOUND' === $result->get_error_code(), 'negative unknown product blocked' );

$result = $upk->update_variant( 10, array(
    'lifecycle_status' => 'TEMPORARILY_UNAVAILABLE',
    'last_verified_at' => '2026-09-02',
) );
maintenance_assert( 10 === $result, 'positive variant update' );
maintenance_assert( 'wp_upk_variants' === $wpdb->last_update['table'], 'variant update uses existing variant table' );
maintenance_assert( 'TEMPORARILY_UNAVAILABLE' === $wpdb->last_update['data']['lifecycle_status'], 'variant lifecycle updated' );

$result = $upk->update_variant( 999, array( 'lifecycle_status' => 'ACTIVE' ) );
maintenance_assert( is_wp_error( $result ) && 'UPK_VARIANT_NOT_FOUND' === $result->get_error_code(), 'negative unknown variant blocked' );

$existing = $upk->find_product_id_by_identity( array(
    'manufacturer' => 'Maker A',
    'model_name' => 'Model Alpha',
    'product_group_key' => 'test-group',
    'generation' => '',
) );
maintenance_assert( 1 === $existing, 'existing exact product identity is reused' );
maintenance_assert( 'Maker A' === $wpdb->last_get_col_prepared['args'][0], 'manufacturer bound into identity lookup' );
maintenance_assert( 'Model Alpha' === $wpdb->last_get_col_prepared['args'][1], 'model bound into identity lookup' );
maintenance_assert( 'test-group' === $wpdb->last_get_col_prepared['args'][2], 'group bound into identity lookup' );
maintenance_assert( '' === $wpdb->last_get_col_prepared['args'][3], 'generation bound into identity lookup' );

$missing = $upk->find_product_id_by_identity( array(
    'manufacturer' => 'New Maker',
    'model_name' => 'New Model',
    'product_group_key' => 'test-group',
) );
maintenance_assert( 0 === $missing, 'new exact product identity remains eligible for one creation' );

$duplicate = $upk->find_product_id_by_identity( array(
    'manufacturer' => 'Duplicate Maker',
    'model_name' => 'Duplicate Model',
    'product_group_key' => 'test-group',
) );
maintenance_assert( is_wp_error( $duplicate ) && 'UPK_DUPLICATE_PRODUCT_IDENTITY' === $duplicate->get_error_code(), 'duplicate exact product identity blocks fail closed' );

$incomplete = $upk->find_product_id_by_identity( array(
    'manufacturer' => 'Maker A',
    'model_name' => '',
    'product_group_key' => 'test-group',
) );
maintenance_assert( is_wp_error( $incomplete ) && 'UPK_PRODUCT_IDENTITY_INCOMPLETE' === $incomplete->get_error_code(), 'incomplete candidate identity blocked' );

$due = $upk->products_due_for_review( '2026-03-12 00:00:00', 999 );
maintenance_assert( array( 2, 1 ) === $due, 'positive due-product selection' );
maintenance_assert( 500 === $wpdb->last_get_col_prepared['args'][1], 'review batch hard capped at 500' );
maintenance_assert( false !== strpos( $wpdb->last_get_col_prepared['query'], "lifecycle_status IN ('ACTIVE','TEMPORARILY_UNAVAILABLE','UNKNOWN')" ), 'discontinued products excluded from periodic queue' );

$group_due = $upk->products_due_for_group_review( 'regendecken', '2025-09-12 00:00:00', 100 );
maintenance_assert( array( 1 ) === $group_due, 'positive product-group due selection' );
maintenance_assert( 'regendecken' === $wpdb->last_get_col_prepared['args'][0], 'product-group key bound into query' );
maintenance_assert( '2025-09-12 00:00:00' === $wpdb->last_get_col_prepared['args'][1], 'product-group refresh cutoff bound into query' );
maintenance_assert( 100 === $wpdb->last_get_col_prepared['args'][2], 'product-group review limit bound into query' );
maintenance_assert( false !== strpos( $wpdb->last_get_col_prepared['query'], 'product_group_key = %s' ), 'group-specific refresh avoids global full scan' );

$result = $upk->products_due_for_group_review( '', '2025-09-12 00:00:00', 100 );
maintenance_assert( is_wp_error( $result ) && 'UPK_PRODUCT_GROUP_KEY_MISSING' === $result->get_error_code(), 'negative empty product-group blocked' );

$result = $upk->products_due_for_review( 'definitely-not-a-date', 100 );
maintenance_assert( is_wp_error( $result ) && 'UPK_INVALID_DATETIME' === $result->get_error_code(), 'negative invalid review cutoff blocked' );

$before_upc_writes = $wpdb->update_count;
$upc = new UPC_Maintenance( $wpdb );

$affected = $upc->affected_comparisons_for_product( 1 );
maintenance_assert( array( 3, 5 ) === $affected, 'product update resolves exact affected comparisons without duplicates' );
maintenance_assert( false !== strpos( $wpdb->last_get_col_prepared['query'], 'LEFT JOIN wp_upk_variants' ), 'product impact includes variant comparisons' );
maintenance_assert( false !== strpos( $wpdb->last_get_col_prepared['query'], 'v.product_id = %d' ), 'variant parent binding used for impact lookup' );

$result = $upc->affected_comparisons_for_product( 999 );
maintenance_assert( is_wp_error( $result ) && 'UPC_PRODUCT_NOT_FOUND' === $result->get_error_code(), 'negative unknown product impact blocked' );

$affected = $upc->affected_comparisons_for_variant( 10 );
maintenance_assert( array( 5 ) === $affected, 'variant update resolves exact affected comparisons' );

$result = $upc->affected_comparisons_for_variant( 999 );
maintenance_assert( is_wp_error( $result ) && 'UPC_VARIANT_NOT_FOUND' === $result->get_error_code(), 'negative unknown variant impact blocked' );
maintenance_assert( $before_upc_writes === $wpdb->update_count, 'comparison impact lookup is read only' );

$upk_source = file_get_contents( dirname( __DIR__, 2 ) . '/universal-product-knowledge/src/class-upk-maintenance.php' );
$upc_source = file_get_contents( dirname( __DIR__ ) . '/src/class-upc-maintenance.php' );
$combined_source = $upk_source . "\n" . $upc_source;
maintenance_assert( false === stripos( $combined_source, 'CREATE TABLE' ), 'no new database table' );
maintenance_assert( false === stripos( $combined_source, 'wp_schedule_' ), 'no scheduler introduced' );
maintenance_assert( false === stripos( $combined_source, 'wp_insert_post' ), 'maintenance core cannot write articles' );

fwrite( STDOUT, "PRODUCT_MAINTENANCE_KISS_GESAMT_PASS\n" );
