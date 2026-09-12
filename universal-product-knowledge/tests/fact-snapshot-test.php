<?php

define( 'ABSPATH', __DIR__ . '/' );
class WP_Error {
    private $code;
    public function __construct( $code, $message = '' ) { $this->code = $code; }
    public function get_error_code() { return $this->code; }
}
function is_wp_error( $value ) { return $value instanceof WP_Error; }
function absint( $value ) { return abs( (int) $value ); }
function sanitize_key( $value ) { $value = strtolower( (string) $value ); return preg_replace( '/[^a-z0-9_\-]/', '', $value ); }
function esc_url_raw( $value ) { return filter_var( trim( (string) $value ), FILTER_VALIDATE_URL ) ? trim( (string) $value ) : ''; }

class UPK_Repository { const SUBJECT_PRODUCT = 'product'; }

class Snapshot_Fake_WPDB {
    public $prefix = 'wp_';
    public $last_error = '';
    public $queries = array();
    public $deletes = array();
    public $delete_result = 2;
    public function query( $sql ) { $this->queries[] = $sql; return true; }
    public function delete( $table, $where, $formats ) {
        $this->deletes[] = array( $table, $where, $formats );
        return $this->delete_result;
    }
}
class Snapshot_Fake_Repository {
    public $bundle = array( 'id' => 11 );
    public $added = array();
    public $fail_key = '';
    public function get_product_bundle( $id ) { return 11 === (int) $id ? $this->bundle : new WP_Error( 'UPK_PRODUCT_NOT_FOUND', 'missing' ); }
    public function add_fact( $subject_type, $subject_id, $fact ) {
        if ( $this->fail_key !== '' && $this->fail_key === (string) $fact['fact_key'] ) {
            return new WP_Error( 'UPK_FACT_INSERT_FAILED', 'failed' );
        }
        $this->added[] = array( $subject_type, $subject_id, $fact );
        return count( $this->added );
    }
}
function snapshot_assert( $condition, $label ) {
    if ( ! $condition ) { fwrite( STDERR, "FAIL: {$label}\n" ); exit( 1 ); }
    fwrite( STDOUT, "PASS: {$label}\n" );
}

require_once dirname( __DIR__ ) . '/src/class-upk-fact-snapshot.php';

$facts = array(
    array( 'fact_key' => 'waterproofness', 'source_url' => 'https://maker.example/rug', 'fact_value' => '3000' ),
    array( 'fact_key' => 'fill_weight', 'source_url' => 'https://maker.example/rug', 'fact_value' => '0 g' ),
);
$wpdb = new Snapshot_Fake_WPDB();
$repo = new Snapshot_Fake_Repository();
$snapshot = new UPK_Fact_Snapshot( $wpdb, $repo );

$result = $snapshot->replace_product_facts( 11, $facts, true );
snapshot_assert( 2 === $result, 'complete fact snapshot replaces successfully' );
snapshot_assert( array( 'START TRANSACTION', 'COMMIT' ) === $wpdb->queries, 'standalone replacement is transactional' );
snapshot_assert( 1 === count( $wpdb->deletes ), 'old product facts deleted once' );
snapshot_assert( 'product' === $wpdb->deletes[0][1]['subject_type'] && 11 === $wpdb->deletes[0][1]['subject_id'], 'delete is scoped to one product only' );
snapshot_assert( 2 === count( $repo->added ), 'new facts written once each' );

$wpdb = new Snapshot_Fake_WPDB();
$repo = new Snapshot_Fake_Repository();
$snapshot = new UPK_Fact_Snapshot( $wpdb, $repo );
$dup = array( $facts[0], $facts[0] );
$result = $snapshot->replace_product_facts( 11, $dup, true );
snapshot_assert( is_wp_error( $result ) && 'UPK_FACT_SNAPSHOT_DUPLICATE' === $result->get_error_code(), 'duplicate fact binding blocked before mutation' );
snapshot_assert( empty( $wpdb->queries ) && empty( $wpdb->deletes ), 'duplicate blocker performs no mutation' );

$result = $snapshot->replace_product_facts( 11, array(), true );
snapshot_assert( is_wp_error( $result ) && 'UPK_FACT_SNAPSHOT_EMPTY' === $result->get_error_code(), 'empty snapshot blocked' );

$wpdb = new Snapshot_Fake_WPDB();
$wpdb->delete_result = false;
$wpdb->last_error = 'delete failed';
$repo = new Snapshot_Fake_Repository();
$snapshot = new UPK_Fact_Snapshot( $wpdb, $repo );
$result = $snapshot->replace_product_facts( 11, $facts, true );
snapshot_assert( is_wp_error( $result ) && 'UPK_FACT_SNAPSHOT_DELETE_FAILED' === $result->get_error_code(), 'delete failure blocked' );
snapshot_assert( array( 'START TRANSACTION', 'ROLLBACK' ) === $wpdb->queries, 'delete failure rolls back' );

$wpdb = new Snapshot_Fake_WPDB();
$repo = new Snapshot_Fake_Repository();
$repo->fail_key = 'fill_weight';
$snapshot = new UPK_Fact_Snapshot( $wpdb, $repo );
$result = $snapshot->replace_product_facts( 11, $facts, true );
snapshot_assert( is_wp_error( $result ) && 'UPK_FACT_INSERT_FAILED' === $result->get_error_code(), 'fact insert failure propagates' );
snapshot_assert( array( 'START TRANSACTION', 'ROLLBACK' ) === $wpdb->queries, 'fact insert failure rolls back full snapshot' );

$wpdb = new Snapshot_Fake_WPDB();
$repo = new Snapshot_Fake_Repository();
$snapshot = new UPK_Fact_Snapshot( $wpdb, $repo );
$result = $snapshot->replace_product_facts( 11, $facts, false );
snapshot_assert( 2 === $result, 'caller-owned transaction replacement passes' );
snapshot_assert( empty( $wpdb->queries ), 'caller-owned transaction emits no nested transaction commands' );

$source = file_get_contents( dirname( __DIR__ ) . '/src/class-upk-fact-snapshot.php' );
snapshot_assert( false === stripos( $source, 'CREATE TABLE' ), 'snapshot creates no table' );
snapshot_assert( false === stripos( $source, 'wp_insert_post' ), 'snapshot writes no article' );

fwrite( STDOUT, "UPK_FACT_SNAPSHOT_GESAMT_PASS\n" );
