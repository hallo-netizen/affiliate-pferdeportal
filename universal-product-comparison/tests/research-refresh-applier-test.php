<?php

define( 'ABSPATH', __DIR__ . '/' );
class WP_Error {
    private $code;
    public function __construct( $code, $message = '' ) { $this->code = $code; }
    public function get_error_code() { return $this->code; }
}
function is_wp_error( $value ) { return $value instanceof WP_Error; }
function absint( $value ) { return abs( (int) $value ); }

class Apply_Fake_WPDB {
    public $queries = array();
    public function query( $sql ) { $this->queries[] = $sql; return true; }
}
class Apply_Fake_Knowledge {
    public $bundle;
}
class Apply_Fake_Validator {
    public $result;
    public function validate( $plan, $results ) { return $this->result; }
}
class Apply_Fake_Product_Maintenance {
    public $knowledge;
    public $error = null;
    public $calls = 0;
    public function __construct( $knowledge ) { $this->knowledge = $knowledge; }
    public function update_product( $product_id, $data ) {
        $this->calls++;
        if ( $this->error ) { return $this->error; }
        $this->knowledge->bundle['lifecycle_status'] = $data['lifecycle_status'];
        $this->knowledge->bundle['manufacturer_product_url'] = $data['manufacturer_product_url'];
        $this->knowledge->bundle['last_verified_at'] = $data['last_verified_at'];
        return $product_id;
    }
}
class Apply_Fake_Fact_Snapshot {
    public $knowledge;
    public $error = null;
    public $calls = 0;
    public function __construct( $knowledge ) { $this->knowledge = $knowledge; }
    public function replace_product_facts( $product_id, $facts, $manage_transaction ) {
        $this->calls++;
        if ( $this->error ) { return $this->error; }
        $this->knowledge->bundle['facts'] = $facts;
        return count( $facts );
    }
}
class Apply_Fake_Fingerprint {
    public $knowledge;
    public function __construct( $knowledge ) { $this->knowledge = $knowledge; }
    public function product( $product_id ) {
        $facts = array();
        foreach ( (array) $this->knowledge->bundle['facts'] as $fact ) {
            $facts[] = array(
                'fact_key' => $fact['fact_key'],
                'fact_value' => $fact['fact_value'],
                'fact_note' => isset( $fact['fact_note'] ) ? $fact['fact_note'] : '',
                'source_url' => $fact['source_url'],
                'source_type' => $fact['source_type'],
                'fact_status' => $fact['fact_status'],
            );
        }
        return hash( 'sha256', json_encode( array(
            'lifecycle_status' => $this->knowledge->bundle['lifecycle_status'],
            'manufacturer_product_url' => $this->knowledge->bundle['manufacturer_product_url'],
            'facts' => $facts,
        ) ) );
    }
}
class Apply_Fake_Comparison_Maintenance {
    public $affected = array( 9, 7, 9 );
    public $error = null;
    public $calls = 0;
    public function affected_comparisons_for_product( $product_id ) {
        $this->calls++;
        return $this->error ? $this->error : $this->affected;
    }
}
function apply_assert( $condition, $label ) {
    if ( ! $condition ) { fwrite( STDERR, "FAIL: {$label}\n" ); exit( 1 ); }
    fwrite( STDOUT, "PASS: {$label}\n" );
}

require_once dirname( __DIR__ ) . '/src/class-upc-research-refresh-applier.php';

function apply_fixture( $changed = false ) {
    $knowledge = new Apply_Fake_Knowledge();
    $knowledge->bundle = array(
        'lifecycle_status' => 'UNKNOWN',
        'manufacturer_product_url' => 'https://maker.example/rug',
        'last_verified_at' => '2025-08-01 00:00:00',
        'facts' => array(
            array(
                'fact_key' => 'waterproofness', 'fact_value' => '3000 mm', 'fact_note' => '',
                'source_url' => 'https://maker.example/rug', 'source_type' => 'MANUFACTURER',
                'fact_status' => 'VERIFIED', 'verified_at' => '2025-08-01 00:00:00',
            ),
        ),
    );
    $validated_fact = array(
        'fact_key' => 'waterproofness',
        'fact_value' => $changed ? '5000 mm' : '3000 mm',
        'fact_note' => '',
        'source_url' => 'https://maker.example/rug',
        'source_type' => 'MANUFACTURER',
        'fact_status' => 'VERIFIED',
        'verified_at' => '2026-09-12 11:00:00',
        'unit' => 'mm',
    );
    $validator = new Apply_Fake_Validator();
    $validator->result = array(
        'schema_version' => '1',
        'contract' => 'UPC_PRODUCT_RESEARCH_REFRESH_RESULT_VALIDATED_V1',
        'project_key' => 'pferde-atelier',
        'maintenance_policy_sha256' => str_repeat( 'a', 64 ),
        'result_count' => 1,
        'results' => array(
            array(
                'product_id' => 11,
                'verified_at' => '2026-09-12 11:00:00',
                'lifecycle_status' => 'UNKNOWN',
                'manufacturer_product_url' => 'https://maker.example/rug',
                'facts' => array( $validated_fact ),
            ),
        ),
    );
    $wpdb = new Apply_Fake_WPDB();
    $product_maintenance = new Apply_Fake_Product_Maintenance( $knowledge );
    $snapshot = new Apply_Fake_Fact_Snapshot( $knowledge );
    $fingerprint = new Apply_Fake_Fingerprint( $knowledge );
    $comparison = new Apply_Fake_Comparison_Maintenance();
    $applier = new UPC_Research_Refresh_Applier( $wpdb, $validator, $product_maintenance, $snapshot, $fingerprint, $comparison );
    return array( $applier, $wpdb, $validator, $product_maintenance, $snapshot, $comparison );
}

list( $applier, $wpdb, $validator, $maintenance, $snapshot, $comparison ) = apply_fixture( false );
$result = $applier->apply( array(), array() );
apply_assert( ! is_wp_error( $result ) && 'UPC_PRODUCT_RESEARCH_REFRESH_APPLIED_V1' === $result['contract'], 'unchanged refresh applies' );
apply_assert( array( 11 ) === $result['unchanged_product_ids'] && empty( $result['changed_product_ids'] ), 'timestamp-only reverification remains semantically unchanged' );
apply_assert( empty( $result['affected_comparison_ids'] ) && 0 === $comparison->calls, 'unchanged product triggers no comparison work' );
apply_assert( array( 'START TRANSACTION', 'COMMIT' ) === $wpdb->queries, 'unchanged refresh commits atomically' );
apply_assert( 1 === $maintenance->calls && 1 === $snapshot->calls, 'product and complete fact snapshot updated once' );

list( $applier, $wpdb, $validator, $maintenance, $snapshot, $comparison ) = apply_fixture( true );
$result = $applier->apply( array(), array() );
apply_assert( array( 11 ) === $result['changed_product_ids'] && empty( $result['unchanged_product_ids'] ), 'semantic fact change detected' );
apply_assert( array( 7, 9 ) === $result['affected_comparison_ids'], 'only affected comparison IDs returned uniquely sorted' );
apply_assert( 1 === $comparison->calls, 'changed product queries impact once' );
apply_assert( array( 'START TRANSACTION', 'COMMIT' ) === $wpdb->queries, 'changed refresh commits atomically' );

list( $applier, $wpdb, $validator, $maintenance, $snapshot, $comparison ) = apply_fixture( false );
$validator->result = new WP_Error( 'UPC_REFRESH_RESULT_STALE_TASK', 'stale' );
$result = $applier->apply( array(), array() );
apply_assert( is_wp_error( $result ) && 'UPC_REFRESH_RESULT_STALE_TASK' === $result->get_error_code(), 'validator blocker propagates' );
apply_assert( array( 'START TRANSACTION', 'ROLLBACK' ) === $wpdb->queries, 'validator blocker rolls back' );
apply_assert( 0 === $maintenance->calls && 0 === $snapshot->calls, 'validator blocker mutates nothing' );

list( $applier, $wpdb, $validator, $maintenance, $snapshot, $comparison ) = apply_fixture( false );
$maintenance->error = new WP_Error( 'UPK_PRODUCT_UPDATE_FAILED', 'failed' );
$result = $applier->apply( array(), array() );
apply_assert( is_wp_error( $result ) && 'UPK_PRODUCT_UPDATE_FAILED' === $result->get_error_code(), 'product update failure propagates' );
apply_assert( array( 'START TRANSACTION', 'ROLLBACK' ) === $wpdb->queries && 0 === $snapshot->calls, 'product failure rolls back before fact replacement' );

list( $applier, $wpdb, $validator, $maintenance, $snapshot, $comparison ) = apply_fixture( false );
$snapshot->error = new WP_Error( 'UPK_FACT_SNAPSHOT_DELETE_FAILED', 'failed' );
$result = $applier->apply( array(), array() );
apply_assert( is_wp_error( $result ) && 'UPK_FACT_SNAPSHOT_DELETE_FAILED' === $result->get_error_code(), 'fact snapshot failure propagates' );
apply_assert( array( 'START TRANSACTION', 'ROLLBACK' ) === $wpdb->queries, 'fact snapshot failure rolls back product update' );

list( $applier, $wpdb, $validator, $maintenance, $snapshot, $comparison ) = apply_fixture( true );
$comparison->error = new WP_Error( 'UPC_PRODUCT_NOT_FOUND', 'failed' );
$result = $applier->apply( array(), array() );
apply_assert( is_wp_error( $result ) && 'UPC_PRODUCT_NOT_FOUND' === $result->get_error_code(), 'impact lookup failure propagates' );
apply_assert( array( 'START TRANSACTION', 'ROLLBACK' ) === $wpdb->queries, 'impact failure rolls back knowledge update' );

$source = file_get_contents( dirname( __DIR__ ) . '/src/class-upc-research-refresh-applier.php' );
apply_assert( false === stripos( $source, 'wp_insert_post' ), 'applier writes no article' );
apply_assert( false === stripos( $source, 'wp_update_post' ), 'applier updates no article' );
apply_assert( false === stripos( $source, 'add_action' ), 'applier registers no automatic hook' );
apply_assert( false === stripos( $source, 'wp_schedule' ), 'applier registers no scheduler' );

fwrite( STDOUT, "UPC_RESEARCH_REFRESH_APPLIER_GESAMT_PASS\n" );
