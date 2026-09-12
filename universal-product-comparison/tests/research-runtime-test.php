<?php

define( 'ABSPATH', __DIR__ . '/' );
class WP_Error {
    private $code;
    public function __construct( $code, $message = '' ) { $this->code = $code; }
    public function get_error_code() { return $this->code; }
}
function is_wp_error( $value ) { return $value instanceof WP_Error; }
function sanitize_key( $value ) { $value = strtolower( (string) $value ); return preg_replace( '/[^a-z0-9_\-]/', '', $value ); }

$GLOBALS['wpdb'] = (object) array( 'marker' => 'wpdb' );
$GLOBALS['knowledge'] = (object) array( 'marker' => 'knowledge' );
$GLOBALS['comparisons'] = (object) array( 'marker' => 'comparisons' );
$GLOBALS['seen'] = array();
$GLOBALS['import_result'] = array( 'status' => 'RESEARCH_IMPORT_PASS' );
$GLOBALS['refresh_result'] = array( 'contract' => 'UPC_PRODUCT_RESEARCH_REFRESH_PLAN_V1' );
$GLOBALS['apply_result'] = array( 'contract' => 'UPC_PRODUCT_RESEARCH_REFRESH_APPLY_V1', 'changed_product_count' => 1 );
$GLOBALS['candidate_result'] = array( 'status' => 'RESEARCH_REQUIRED', 'persisted' => false );

function upk_repository() { return $GLOBALS['knowledge']; }
function upc_repository() { return $GLOBALS['comparisons']; }
class UPK_Maintenance { public function __construct( $wpdb ) { $GLOBALS['seen']['upk_maintenance'] = $wpdb; } }
class UPC_Maintenance { public function __construct( $wpdb ) { $GLOBALS['seen']['upc_maintenance'] = $wpdb; } }
class UPK_Fact_Snapshot { public function __construct( $wpdb, $knowledge ) { $GLOBALS['seen']['snapshot'] = array( $wpdb, $knowledge ); } }
class UPK_Change_Fingerprint { public function __construct( $knowledge ) { $GLOBALS['seen']['fingerprint'] = $knowledge; } }
class UPC_Feature_Key_Catalog {
    public static function load( $path ) { $GLOBALS['seen']['catalog_path'] = $path; return (object) array( 'ok' => true ); }
}
class UPC_Candidate_Gate {
    public static function load_policy( $path ) { $GLOBALS['seen']['candidate_policy_path'] = $path; return array( 'schema_version' => '1', 'market_gate' => array(), 'groups' => array( array( 'product_group_key' => 'regendecken' ) ) ); }
    public function __construct( $maintenance, $catalog, $policy ) { $GLOBALS['seen']['candidate_ctor'] = array( $maintenance, $catalog, $policy ); }
    public function evaluate( $candidate ) { $GLOBALS['seen']['candidate_input'] = $candidate; return $GLOBALS['candidate_result']; }
}
class UPC_Research_Importer {
    public static function load_bound_plan( $project_key ) { $GLOBALS['seen']['import_project'] = $project_key; return array( 'project_key' => $project_key ); }
    public function __construct( $wpdb, $knowledge, $maintenance, $comparisons, $catalog ) { $GLOBALS['seen']['import_ctor'] = array( $wpdb, $knowledge, $comparisons ); }
    public function import_plan( $plan ) { return $GLOBALS['import_result']; }
}
class UPC_Research_Refresh_Planner {
    public function __construct( $knowledge, $product_maintenance, $comparison_maintenance ) { $GLOBALS['seen']['planner_ctor'] = array( $knowledge, $product_maintenance, $comparison_maintenance ); }
    public function build( $project_key, $as_of_utc, $limit ) { $GLOBALS['seen']['planner_args'] = array( $project_key, $as_of_utc, $limit ); return $GLOBALS['refresh_result']; }
}
class UPC_Research_Refresh_Result_Validator { public function __construct( $knowledge ) { $GLOBALS['seen']['validator'] = $knowledge; } }
class UPC_Research_Refresh_Applier {
    public function __construct( $wpdb, $validator, $product_maintenance, $snapshot, $fingerprint, $comparison_maintenance ) { $GLOBALS['seen']['applier_ctor'] = array( $wpdb, $validator, $product_maintenance, $snapshot, $fingerprint, $comparison_maintenance ); }
    public function apply( $plan, $results ) { $GLOBALS['seen']['apply_args'] = array( $plan, $results ); return $GLOBALS['apply_result']; }
}

function runtime_assert( $condition, $label ) {
    if ( ! $condition ) { fwrite( STDERR, "FAIL: {$label}\n" ); exit( 1 ); }
    fwrite( STDOUT, "PASS: {$label}\n" );
}

require_once dirname( __DIR__ ) . '/src/class-upc-research-runtime.php';

$r = UPC_Research_Runtime::import_bound_plan( 'Pferde Atelier' );
runtime_assert( ! is_wp_error( $r ) && 'RESEARCH_IMPORT_PASS' === $r['status'], 'import runtime positive' );
runtime_assert( 'pferdeatelier' === $GLOBALS['seen']['import_project'], 'import project key sanitized' );
runtime_assert( $GLOBALS['seen']['import_ctor'][1] === $GLOBALS['knowledge'] && $GLOBALS['seen']['import_ctor'][2] === $GLOBALS['comparisons'], 'import receives bound repositories' );
$r = UPC_Research_Runtime::import_bound_plan( '' );
runtime_assert( is_wp_error( $r ) && 'UPC_RESEARCH_PROJECT_KEY_MISSING' === $r->get_error_code(), 'import empty project blocked' );

$r = UPC_Research_Runtime::build_due_refresh_plan( 'Pferde Atelier', '2026-09-12 10:00:00', 123 );
runtime_assert( ! is_wp_error( $r ) && 'UPC_PRODUCT_RESEARCH_REFRESH_PLAN_V1' === $r['contract'], 'refresh planner runtime positive' );
runtime_assert( array( 'pferdeatelier', '2026-09-12 10:00:00', 123 ) === $GLOBALS['seen']['planner_args'], 'refresh planner arguments bound' );
$r = UPC_Research_Runtime::build_due_refresh_plan( '', '2026-09-12 10:00:00', 500 );
runtime_assert( is_wp_error( $r ) && 'UPC_REFRESH_PROJECT_KEY_MISSING' === $r->get_error_code(), 'refresh empty project blocked' );

$plan = array( 'contract' => 'UPC_PRODUCT_RESEARCH_REFRESH_PLAN_V1', 'tasks' => array( array( 'product_id' => 11 ) ) );
$results = array( array( 'product_id' => 11 ) );
$r = UPC_Research_Runtime::apply_refresh_results( $plan, $results );
runtime_assert( ! is_wp_error( $r ) && 1 === $r['changed_product_count'], 'apply runtime positive' );
runtime_assert( $GLOBALS['seen']['snapshot'][0] === $GLOBALS['wpdb'] && $GLOBALS['seen']['snapshot'][1] === $GLOBALS['knowledge'], 'apply snapshot bound to shared state' );
runtime_assert( $GLOBALS['seen']['fingerprint'] === $GLOBALS['knowledge'] && $GLOBALS['seen']['validator'] === $GLOBALS['knowledge'], 'apply fingerprint and validator bound' );
runtime_assert( array( $plan, $results ) === $GLOBALS['seen']['apply_args'], 'apply inputs delegated unchanged' );
$GLOBALS['apply_result'] = new WP_Error( 'UPC_REFRESH_RESULT_TASK_STALE', 'stale' );
$r = UPC_Research_Runtime::apply_refresh_results( $plan, $results );
runtime_assert( is_wp_error( $r ) && 'UPC_REFRESH_RESULT_TASK_STALE' === $r->get_error_code(), 'apply stale blocker propagates fail closed' );

$candidate = array( 'manufacturer' => 'Acme', 'model_name' => 'Rain 1' );
$r = UPC_Research_Runtime::evaluate_candidate( $candidate, 'Pferde Atelier' );
runtime_assert( ! is_wp_error( $r ) && 'RESEARCH_REQUIRED' === $r['status'] && false === $r['persisted'], 'candidate runtime stays read-only' );
runtime_assert( $candidate === $GLOBALS['seen']['candidate_input'], 'candidate input delegated unchanged' );
runtime_assert( false !== strpos( $GLOBALS['seen']['candidate_policy_path'], '/config/pferdeatelier/maintenance-groups.json' ), 'candidate policy bound to project config' );
$r = UPC_Research_Runtime::evaluate_candidate( $candidate, '' );
runtime_assert( is_wp_error( $r ) && 'UPC_CANDIDATE_PROJECT_KEY_MISSING' === $r->get_error_code(), 'candidate empty project blocked' );

$runtime_source = file_get_contents( dirname( __DIR__ ) . '/src/class-upc-research-runtime.php' );
runtime_assert( false === stripos( $runtime_source, 'add_action' ), 'runtime registers no automatic hook' );
runtime_assert( false === stripos( $runtime_source, 'wp_schedule' ), 'runtime registers no scheduler' );
runtime_assert( false === stripos( $runtime_source, 'wp_insert_post' ) && false === stripos( $runtime_source, 'wp_update_post' ), 'runtime writes no article' );

$plugin_source = file_get_contents( dirname( __DIR__ ) . '/universal-product-comparison.php' );
runtime_assert( false !== strpos( $plugin_source, 'function upc_apply_research_refresh_results' ), 'main plugin exposes explicit apply function' );
runtime_assert( false !== strpos( $plugin_source, 'function upc_evaluate_product_candidate' ), 'main plugin exposes explicit candidate function' );
runtime_assert( 0 === preg_match( '/add_action\s*\([^\n]*upc_apply_research_refresh_results/i', $plugin_source ), 'apply function is not hook-driven' );
runtime_assert( 0 === preg_match( '/add_action\s*\([^\n]*upc_evaluate_product_candidate/i', $plugin_source ), 'candidate function is not hook-driven' );
runtime_assert( false === stripos( $plugin_source, 'wp_schedule_event' ), 'main plugin adds no refresh scheduler' );

fwrite( STDOUT, "UPC_RESEARCH_RUNTIME_GESAMT_PASS\n" );
