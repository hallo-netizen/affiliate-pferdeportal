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
function sanitize_text_field( $value ) { return trim( strip_tags( (string) $value ) ); }
function sanitize_textarea_field( $value ) { return trim( strip_tags( (string) $value ) ); }
function esc_url_raw( $value ) { return filter_var( trim( (string) $value ), FILTER_VALIDATE_URL ) ? trim( (string) $value ) : ''; }

class UPK_Repository {
    public static function lifecycle_statuses() { return array( 'ACTIVE', 'TEMPORARILY_UNAVAILABLE', 'DISCONTINUED', 'UNKNOWN' ); }
    public static function source_types() { return array( 'MANUFACTURER', 'OFFICIAL_DOCUMENTATION', 'APPROVED_SECONDARY' ); }
    public static function fact_statuses() { return array( 'VERIFIED', 'NOT_IN_SOURCE', 'SOURCE_CONFLICT', 'CONFIGURATION_DEPENDENT' ); }
}

class Refresh_Result_Fake_Knowledge {
    public $bundle;
    public function get_product_bundle( $id ) { return 11 === (int) $id ? $this->bundle : new WP_Error( 'UPK_PRODUCT_NOT_FOUND', 'missing' ); }
}

function result_assert( $condition, $label ) {
    if ( ! $condition ) { fwrite( STDERR, "FAIL: {$label}\n" ); exit( 1 ); }
    fwrite( STDOUT, "PASS: {$label}\n" );
}

require_once dirname( __DIR__ ) . '/src/class-upc-research-refresh-planner.php';
require_once dirname( __DIR__ ) . '/src/class-upc-research-refresh-result-validator.php';

$knowledge = new Refresh_Result_Fake_Knowledge();
$knowledge->bundle = array(
    'manufacturer' => 'Maker',
    'model_name' => 'Rain Rug',
    'product_group_key' => 'regendecken',
    'manufacturer_product_url' => 'https://maker.example/rug',
    'generation' => '2026',
    'lifecycle_status' => 'UNKNOWN',
    'last_verified_at' => '2025-08-01 00:00:00',
    'facts' => array(
        array( 'fact_key' => 'waterproofness', 'source_url' => 'https://maker.example/rug' ),
        array( 'fact_key' => 'fill_weight', 'source_url' => 'https://maker.example/rug' ),
    ),
);

$policy_sha = str_repeat( 'a', 64 );
$task = array(
    'task_type' => 'PRODUCT_REVERIFY',
    'product_id' => 11,
    'product_group_key' => 'regendecken',
    'manufacturer' => 'Maker',
    'model_name' => 'Rain Rug',
    'generation' => '2026',
    'lifecycle_status' => 'UNKNOWN',
    'manufacturer_product_url' => 'https://maker.example/rug',
    'last_verified_at' => '2025-08-01 00:00:00',
    'due_cutoff_utc' => '2025-09-12 10:00:00',
    'refresh_months' => 12,
    'required_additional_contracts' => array( 'SAFETY_FIT_ADDITIONAL_CONTRACT' ),
);
$task['task_binding_sha256'] = UPC_Research_Refresh_Planner::task_binding_sha256( $task, $policy_sha );
$task['affected_comparison_ids'] = array( 7 );
$plan = array(
    'schema_version' => '1',
    'contract' => 'UPC_PRODUCT_RESEARCH_REFRESH_PLAN_V1',
    'project_key' => 'pferde-atelier',
    'as_of_utc' => '2026-09-12 10:00:00',
    'maintenance_policy_sha256' => $policy_sha,
    'tasks' => array( $task ),
);

$good = array(
    'product_id' => 11,
    'task_binding_sha256' => $task['task_binding_sha256'],
    'verified_at' => '2026-09-12 11:00:00',
    'lifecycle_status' => 'ACTIVE',
    'manufacturer_product_url' => 'https://maker.example/rug-new',
    'completed_additional_contracts' => array( 'safety_fit_additional_contract' ),
    'facts' => array(
        array(
            'fact_key' => 'waterproofness', 'fact_value' => '3000 mm', 'unit' => 'mm',
            'fact_note' => '', 'source_url' => 'https://maker.example/rug-new',
            'source_type' => 'MANUFACTURER', 'fact_status' => 'VERIFIED',
        ),
        array(
            'fact_key' => 'fill_weight', 'fact_value' => '', 'unit' => '',
            'fact_note' => 'Hersteller nennt keine Grammzahl.', 'source_url' => 'https://maker.example/rug-new',
            'source_type' => 'MANUFACTURER', 'fact_status' => 'NOT_IN_SOURCE',
        ),
    ),
);

$validator = new UPC_Research_Refresh_Result_Validator( $knowledge );
$validated = $validator->validate( $plan, array( $good ) );
result_assert( ! is_wp_error( $validated ), 'valid bound refresh result passes' );
result_assert( 'UPC_PRODUCT_RESEARCH_REFRESH_RESULT_VALIDATED_V1' === $validated['contract'], 'validated result contract bound' );
result_assert( 1 === $validated['result_count'], 'one result normalized' );
result_assert( 'ACTIVE' === $validated['results'][0]['lifecycle_status'], 'verified lifecycle normalized' );
result_assert( 'NOT_IN_SOURCE' === $validated['results'][0]['facts'][1]['fact_status'], 'not-in-source fact preserved' );

$bad = $good;
$bad['task_binding_sha256'] = str_repeat( 'b', 64 );
$r = $validator->validate( $plan, array( $bad ) );
result_assert( is_wp_error( $r ) && 'UPC_REFRESH_RESULT_TASK_HASH_MISMATCH' === $r->get_error_code(), 'wrong task hash blocked' );

$knowledge->bundle['lifecycle_status'] = 'ACTIVE';
$r = $validator->validate( $plan, array( $good ) );
result_assert( is_wp_error( $r ) && 'UPC_REFRESH_RESULT_STALE_TASK' === $r->get_error_code(), 'changed current product state blocks stale result' );
$knowledge->bundle['lifecycle_status'] = 'UNKNOWN';

$bad = $good;
$bad['verified_at'] = '2026-09-12 09:59:59';
$r = $validator->validate( $plan, array( $bad ) );
result_assert( is_wp_error( $r ) && 'UPC_REFRESH_RESULT_VERIFICATION_TIME_INVALID' === $r->get_error_code(), 'pre-plan research evidence blocked' );

$bad = $good;
array_pop( $bad['facts'] );
$r = $validator->validate( $plan, array( $bad ) );
result_assert( is_wp_error( $r ) && 'UPC_REFRESH_RESULT_FACT_SCOPE_INCOMPLETE' === $r->get_error_code(), 'missing existing fact key blocked' );

$bad = $good;
$bad['facts'][] = array(
    'fact_key' => 'new_unbound_fact', 'fact_value' => 'x', 'source_url' => 'https://maker.example/rug-new',
    'source_type' => 'MANUFACTURER', 'fact_status' => 'VERIFIED',
);
$r = $validator->validate( $plan, array( $bad ) );
result_assert( is_wp_error( $r ) && 'UPC_REFRESH_RESULT_FACT_SCOPE_UNKNOWN' === $r->get_error_code(), 'unbound new fact key blocked' );

$bad = $good;
$bad['facts'][] = $bad['facts'][0];
$r = $validator->validate( $plan, array( $bad ) );
result_assert( is_wp_error( $r ) && 'UPC_REFRESH_RESULT_FACT_DUPLICATE' === $r->get_error_code(), 'duplicate fact source binding blocked' );

$bad = $good;
$bad['completed_additional_contracts'] = array();
$r = $validator->validate( $plan, array( $bad ) );
result_assert( is_wp_error( $r ) && 'UPC_REFRESH_RESULT_ADDITIONAL_CONTRACT_MISSING' === $r->get_error_code(), 'required safety contract blocked when missing' );

$bad = $good;
$bad['lifecycle_status'] = 'MADE_UP';
$r = $validator->validate( $plan, array( $bad ) );
result_assert( is_wp_error( $r ) && 'UPC_REFRESH_RESULT_LIFECYCLE_INVALID' === $r->get_error_code(), 'invalid lifecycle blocked' );

$r = $validator->validate( $plan, array() );
result_assert( is_wp_error( $r ) && 'UPC_REFRESH_RESULT_EMPTY' === $r->get_error_code(), 'empty result batch blocked' );
$r = $validator->validate( $plan, array( $good, $good ) );
result_assert( is_wp_error( $r ) && 'UPC_REFRESH_RESULT_DUPLICATE' === $r->get_error_code(), 'duplicate product result blocked' );

$source = file_get_contents( dirname( __DIR__ ) . '/src/class-upc-research-refresh-result-validator.php' );
result_assert( false === stripos( $source, '->insert(' ), 'validator inserts no database rows' );
result_assert( false === stripos( $source, '->update(' ), 'validator updates no database rows' );
result_assert( false === stripos( $source, 'wp_insert_post' ), 'validator writes no article' );
result_assert( false === stripos( $source, 'add_action' ), 'validator registers no automatic hook' );

fwrite( STDOUT, "UPC_RESEARCH_REFRESH_RESULT_VALIDATOR_GESAMT_PASS\n" );
