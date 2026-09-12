<?php

define( 'ABSPATH', __DIR__ . '/' );
define( 'ARRAY_A', 'ARRAY_A' );

class WP_Error {
    private $code;
    public function __construct( $code, $message = '' ) { $this->code = $code; }
    public function get_error_code() { return $this->code; }
}
function is_wp_error( $value ) { return $value instanceof WP_Error; }
function absint( $value ) { return abs( (int) $value ); }
function sanitize_key( $value ) { return strtolower( preg_replace( '/[^a-z0-9_\-]/', '', (string) $value ) ); }
function sanitize_text_field( $value ) { return trim( strip_tags( (string) $value ) ); }
function sanitize_textarea_field( $value ) { return trim( strip_tags( (string) $value ) ); }
function esc_url_raw( $value ) { return filter_var( trim( (string) $value ), FILTER_VALIDATE_URL ) ? trim( (string) $value ) : ''; }
function current_time( $type, $gmt = false ) { return '2026-09-12 09:40:00'; }

class Fact_Note_Fake_WPDB {
    public $prefix = 'wp_';
    public $last_error = '';
    public $insert_id = 10;
    public $last_insert = null;
    public $last_update = null;
    public $last_results_query = null;
    public $existing_fact_id = 0;

    public function prepare( $query, ...$args ) { return array( 'query' => $query, 'args' => $args ); }
    public function get_var( $prepared ) {
        $q = $prepared['query'];
        if ( false !== strpos( $q, 'FROM wp_upk_products' ) ) { return 1; }
        if ( false !== strpos( $q, 'FROM wp_upk_facts' ) ) { return $this->existing_fact_id; }
        return null;
    }
    public function insert( $table, $data, $formats ) {
        $this->last_insert = array( 'table' => $table, 'data' => $data, 'formats' => $formats );
        return 1;
    }
    public function update( $table, $data, $where, $formats, $where_formats ) {
        $this->last_update = array( 'table' => $table, 'data' => $data, 'where' => $where, 'formats' => $formats );
        return 1;
    }
    public function get_results( $prepared, $format = null ) {
        $this->last_results_query = $prepared['query'];
        return array();
    }
    public function get_row( $prepared, $format = null ) {
        if ( false !== strpos( $prepared['query'], 'FROM wp_upk_products' ) ) {
            return array( 'id' => 1, 'manufacturer' => 'Maker', 'model_name' => 'Model', 'product_group_key' => 'group' );
        }
        return null;
    }
}

function note_assert( $condition, $label ) {
    if ( ! $condition ) {
        fwrite( STDERR, "FAIL: {$label}\n" );
        exit( 1 );
    }
    fwrite( STDOUT, "PASS: {$label}\n" );
}

require_once dirname( __DIR__ ) . '/src/class-upk-repository.php';

$wpdb = new Fact_Note_Fake_WPDB();
$repo = new UPK_Repository( $wpdb );

$id = $repo->add_fact( UPK_Repository::SUBJECT_PRODUCT, 1, array(
    'fact_key' => 'waterproofness',
    'fact_value' => 'Herstellerseite widersprüchlich',
    'fact_note' => 'Numerischen Wert nicht glätten.',
    'source_url' => 'https://maker.example/model',
    'source_type' => 'MANUFACTURER',
    'verified_at' => '2026-08-07',
    'fact_status' => 'SOURCE_CONFLICT',
) );
note_assert( 10 === $id, 'fact with note inserts' );
note_assert( 'Numerischen Wert nicht glätten.' === $wpdb->last_insert['data']['fact_note'], 'fact note preserved on insert' );

$wpdb->existing_fact_id = 7;
$id = $repo->add_fact( UPK_Repository::SUBJECT_PRODUCT, 1, array(
    'fact_key' => 'waterproofness',
    'fact_value' => 'Herstellerseite widersprüchlich',
    'fact_note' => 'Aktualisierter Konflikthinweis.',
    'source_url' => 'https://maker.example/model',
    'source_type' => 'MANUFACTURER',
    'verified_at' => '2026-09-12',
    'fact_status' => 'SOURCE_CONFLICT',
) );
note_assert( 7 === $id, 'existing source-bound fact updates instead of duplicating' );
note_assert( 'Aktualisierter Konflikthinweis.' === $wpdb->last_update['data']['fact_note'], 'fact note preserved on update' );

$wpdb->existing_fact_id = 0;
$id = $repo->add_fact( UPK_Repository::SUBJECT_PRODUCT, 1, array(
    'fact_key' => 'fill_weight',
    'fact_value' => '0 g',
    'source_url' => 'https://maker.example/model',
    'source_type' => 'MANUFACTURER',
    'verified_at' => '2026-09-12',
    'fact_status' => 'VERIFIED',
) );
note_assert( 10 === $id && '' === $wpdb->last_insert['data']['fact_note'], 'legacy fact without note remains compatible' );

$repo->get_product_bundle( 1 );
note_assert( false !== strpos( $wpdb->last_results_query, 'fact_note' ), 'fact readback query includes note' );

$plugin_source = file_get_contents( dirname( __DIR__ ) . '/universal-product-knowledge.php' );
note_assert( false !== strpos( $plugin_source, "UPK_SCHEMA_VERSION', '3" ), 'schema version upgraded' );
note_assert( false !== strpos( $plugin_source, 'fact_note text NOT NULL' ), 'existing facts table receives note column' );
note_assert( false !== strpos( $plugin_source, "add_action( 'plugins_loaded', 'upk_maybe_upgrade_schema'" ), 'active installs receive schema upgrade path' );

fwrite( STDOUT, "UPK_FACT_NOTE_STORAGE_GESAMT_PASS\n" );
