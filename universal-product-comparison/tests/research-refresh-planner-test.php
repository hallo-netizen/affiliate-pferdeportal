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

class Refresh_Fake_Knowledge {
    public $products = array();
    public function get_product_bundle( $id ) {
        return isset( $this->products[ $id ] ) ? $this->products[ $id ] : new WP_Error( 'UPK_PRODUCT_NOT_FOUND', 'missing' );
    }
}

class Refresh_Fake_Product_Maintenance {
    public $due = array();
    public $calls = array();
    public function products_due_for_group_review( $key, $cutoff, $limit ) {
        $this->calls[ $key ] = array( 'cutoff' => $cutoff, 'limit' => $limit );
        return isset( $this->due[ $key ] ) ? $this->due[ $key ] : array();
    }
}

class Refresh_Fake_Comparison_Maintenance {
    public $affected = array();
    public function affected_comparisons_for_product( $id ) {
        return isset( $this->affected[ $id ] ) ? $this->affected[ $id ] : array();
    }
}

function refresh_assert( $condition, $label ) {
    if ( ! $condition ) { fwrite( STDERR, "FAIL: {$label}\n" ); exit( 1 ); }
    fwrite( STDOUT, "PASS: {$label}\n" );
}

require_once dirname( __DIR__ ) . '/src/class-upc-research-refresh-planner.php';

$knowledge = new Refresh_Fake_Knowledge();
$products = new Refresh_Fake_Product_Maintenance();
$comparisons = new Refresh_Fake_Comparison_Maintenance();

$knowledge->products[11] = array(
    'manufacturer' => 'Camera Maker',
    'model_name' => 'Stable Cam',
    'product_group_key' => 'kameras-im-stall',
    'manufacturer_product_url' => 'https://maker.example/cam',
    'generation' => '2026',
    'lifecycle_status' => 'UNKNOWN',
    'last_verified_at' => '2026-02-01 00:00:00',
);
$knowledge->products[22] = array(
    'manufacturer' => 'Rug Maker',
    'model_name' => 'Rain Rug',
    'product_group_key' => 'regendecken',
    'manufacturer_product_url' => 'https://maker.example/rug',
    'generation' => '',
    'lifecycle_status' => 'ACTIVE',
    'last_verified_at' => '2025-08-01 00:00:00',
);
$knowledge->products[33] = array(
    'manufacturer' => 'Hoof Maker',
    'model_name' => 'Hoof Boot',
    'product_group_key' => 'hufschuhe',
    'manufacturer_product_url' => 'https://maker.example/hoof',
    'generation' => '',
    'lifecycle_status' => 'UNKNOWN',
    'last_verified_at' => '2026-01-15 00:00:00',
);
$products->due['kameras-im-stall'] = array( 11 );
$products->due['regendecken'] = array( 22 );
$products->due['hufschuhe'] = array( 33 );
$comparisons->affected[11] = array( 5, 9 );
$comparisons->affected[22] = array( 7 );
$comparisons->affected[33] = array( 12, 13 );

$planner = new UPC_Research_Refresh_Planner( $knowledge, $products, $comparisons );
$plan = $planner->build( 'pferde-atelier', '2026-09-12 10:00:00', 500 );
refresh_assert( ! is_wp_error( $plan ), 'refresh plan builds' );
refresh_assert( 'UPC_PRODUCT_RESEARCH_REFRESH_PLAN_V1' === $plan['contract'], 'refresh contract bound' );
refresh_assert( 17 === $plan['group_count'], 'exactly 17 maintenance groups used' );
refresh_assert( 3 === $plan['due_product_count'], 'only due products become research tasks' );
refresh_assert( 64 === strlen( $plan['maintenance_policy_sha256'] ), 'maintenance policy bytes are hash-bound' );
refresh_assert( 4 === (int) $plan['market_gate']['minimum_independent_dossiers'], 'new-candidate market gate travels with handoff' );
refresh_assert( '2026-03-12 10:00:00' === $products->calls['kameras-im-stall']['cutoff'], '6M cutoff correct' );
refresh_assert( '2025-09-12 10:00:00' === $products->calls['regendecken']['cutoff'], '12M cutoff correct' );
refresh_assert( 500 === $products->calls['regendecken']['limit'], 'bounded per-group query' );

$by_id = array();
foreach ( $plan['tasks'] as $task ) { $by_id[ $task['product_id'] ] = $task; }
refresh_assert( array( 5, 9 ) === $by_id[11]['affected_comparison_ids'], 'affected comparisons bound to due product' );
refresh_assert( 'https://maker.example/cam' === $by_id[11]['manufacturer_product_url'], 'manufacturer source bound' );
refresh_assert( array( 'SAFETY_FIT_ADDITIONAL_CONTRACT' ) === $by_id[33]['required_additional_contracts'], 'safety-fit contract preserved for hufschuhe' );
refresh_assert( 64 === strlen( $by_id[11]['task_binding_sha256'] ), 'research task has stable binding hash' );
$task_hash = $by_id[11]['task_binding_sha256'];

$comparisons->affected[11] = array( 5, 9, 14 );
$comparison_only_change = $planner->build( 'pferde-atelier', '2026-09-12 10:00:00', 500 );
$comparison_only_by_id = array();
foreach ( $comparison_only_change['tasks'] as $task ) { $comparison_only_by_id[ $task['product_id'] ] = $task; }
refresh_assert( $task_hash === $comparison_only_by_id[11]['task_binding_sha256'], 'comparison attachment change does not invalidate product research task' );
refresh_assert( array( 5, 9, 14 ) === $comparison_only_by_id[11]['affected_comparison_ids'], 'current affected comparisons still update in plan' );

$knowledge->products[11]['lifecycle_status'] = 'ACTIVE';
$product_state_change = $planner->build( 'pferde-atelier', '2026-09-12 10:00:00', 500 );
$product_state_by_id = array();
foreach ( $product_state_change['tasks'] as $task ) { $product_state_by_id[ $task['product_id'] ] = $task; }
refresh_assert( $task_hash !== $product_state_by_id[11]['task_binding_sha256'], 'product state change invalidates old research task binding' );
$knowledge->products[11]['lifecycle_status'] = 'UNKNOWN';
$comparisons->affected[11] = array( 5, 9 );

$end_month = $planner->build( 'pferde-atelier', '2026-08-31 10:00:00', 500 );
refresh_assert( ! is_wp_error( $end_month ), 'end-of-month refresh plan builds' );
refresh_assert( '2026-02-28 10:00:00' === $products->calls['kameras-im-stall']['cutoff'], 'calendar month cutoff clamps to February end' );
refresh_assert( '2025-08-31 10:00:00' === $products->calls['regendecken']['cutoff'], '12M end-of-month cutoff preserved' );

$knowledge->products[11]['manufacturer_product_url'] = '';
$bad = $planner->build( 'pferde-atelier', '2026-09-12 10:00:00', 500 );
refresh_assert( is_wp_error( $bad ) && 'UPC_REFRESH_PRODUCT_BINDING_INCOMPLETE' === $bad->get_error_code(), 'missing manufacturer source blocks fail closed' );
$knowledge->products[11]['manufacturer_product_url'] = 'https://maker.example/cam';

$knowledge->products[11]['product_group_key'] = 'regendecken';
$bad = $planner->build( 'pferde-atelier', '2026-09-12 10:00:00', 500 );
refresh_assert( is_wp_error( $bad ) && 'UPC_REFRESH_PRODUCT_GROUP_MISMATCH' === $bad->get_error_code(), 'wrong product group blocks fail closed' );
$knowledge->products[11]['product_group_key'] = 'kameras-im-stall';

$bad = $planner->build( '', '2026-09-12 10:00:00', 500 );
refresh_assert( is_wp_error( $bad ) && 'UPC_REFRESH_PROJECT_KEY_MISSING' === $bad->get_error_code(), 'empty project key blocked' );
$bad = $planner->build( 'pferde-atelier', 'not-a-date', 500 );
refresh_assert( is_wp_error( $bad ) && 'UPC_REFRESH_DATETIME_INVALID' === $bad->get_error_code(), 'invalid as-of time blocked' );

$source = file_get_contents( dirname( __DIR__ ) . '/src/class-upc-research-refresh-planner.php' );
refresh_assert( false === stripos( $source, 'add_action' ), 'planner registers no automatic hook' );
refresh_assert( false === stripos( $source, 'wp_schedule' ), 'planner registers no scheduler' );
refresh_assert( false === stripos( $source, '->insert(' ), 'planner inserts no database rows' );
refresh_assert( false === stripos( $source, '->update(' ), 'planner updates no database rows' );
refresh_assert( false === stripos( $source, 'wp_insert_post' ), 'planner writes no article' );

fwrite( STDOUT, "UPC_RESEARCH_REFRESH_PLANNER_GESAMT_PASS\n" );
