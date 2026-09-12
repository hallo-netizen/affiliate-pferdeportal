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
$GLOBALS['runtime_knowledge'] = (object) array( 'marker' => 'knowledge' );
$GLOBALS['runtime_comparisons'] = (object) array( 'marker' => 'comparisons' );
$GLOBALS['runtime_plan_result'] = array( 'schema_version' => '1', 'project_key' => 'pferde-atelier' );
$GLOBALS['runtime_catalog_result'] = (object) array( 'marker' => 'catalog' );
$GLOBALS['runtime_import_result'] = array( 'status' => 'RESEARCH_IMPORT_PASS' );
$GLOBALS['runtime_seen'] = array();

function upk_repository() { return $GLOBALS['runtime_knowledge']; }
function upc_repository() { return $GLOBALS['runtime_comparisons']; }

class UPK_Maintenance {
    public function __construct( $wpdb ) { $GLOBALS['runtime_seen']['maintenance_wpdb'] = $wpdb; }
}
class UPC_Feature_Key_Catalog {
    public static function load( $path ) {
        $GLOBALS['runtime_seen']['catalog_path'] = $path;
        return $GLOBALS['runtime_catalog_result'];
    }
}
class UPC_Research_Importer {
    public static function load_bound_plan( $project_key ) {
        $GLOBALS['runtime_seen']['project_key'] = $project_key;
        return $GLOBALS['runtime_plan_result'];
    }
    public function __construct( $wpdb, $knowledge, $maintenance, $comparisons, $catalog ) {
        $GLOBALS['runtime_seen']['importer'] = array( $wpdb, $knowledge, $maintenance, $comparisons, $catalog );
    }
    public function import_plan( $plan ) {
        $GLOBALS['runtime_seen']['plan'] = $plan;
        return $GLOBALS['runtime_import_result'];
    }
}

function runtime_assert( $condition, $label ) {
    if ( ! $condition ) { fwrite( STDERR, "FAIL: {$label}\n" ); exit( 1 ); }
    fwrite( STDOUT, "PASS: {$label}\n" );
}

require_once dirname( __DIR__ ) . '/src/class-upc-research-runtime.php';

$result = UPC_Research_Runtime::import_bound_plan( 'Pferde Atelier' );
runtime_assert( ! is_wp_error( $result ) && 'RESEARCH_IMPORT_PASS' === $result['status'], 'explicit runtime call returns importer result' );
runtime_assert( 'pferdeatelier' === $GLOBALS['runtime_seen']['project_key'], 'project key is sanitized and bound' );
runtime_assert( $GLOBALS['runtime_seen']['maintenance_wpdb'] === $GLOBALS['wpdb'], 'maintenance receives shared wpdb' );
runtime_assert( $GLOBALS['runtime_seen']['importer'][1] === $GLOBALS['runtime_knowledge'], 'importer receives shared product knowledge' );
runtime_assert( $GLOBALS['runtime_seen']['importer'][3] === $GLOBALS['runtime_comparisons'], 'importer receives shared comparison repository' );
runtime_assert( false !== strpos( $GLOBALS['runtime_seen']['catalog_path'], '/config/pferdeatelier/feature-key-catalog.json' ), 'catalog path is project-bound' );

$result = UPC_Research_Runtime::import_bound_plan( '' );
runtime_assert( is_wp_error( $result ) && 'UPC_RESEARCH_PROJECT_KEY_MISSING' === $result->get_error_code(), 'empty project key blocks before import' );

$GLOBALS['runtime_catalog_result'] = new WP_Error( 'UPC_FEATURE_CATALOG_MISSING', 'missing' );
$result = UPC_Research_Runtime::import_bound_plan( 'pferde-atelier' );
runtime_assert( is_wp_error( $result ) && 'UPC_FEATURE_CATALOG_MISSING' === $result->get_error_code(), 'catalog blocker propagates fail closed' );
$GLOBALS['runtime_catalog_result'] = (object) array( 'marker' => 'catalog' );

$GLOBALS['runtime_plan_result'] = new WP_Error( 'UPC_RESEARCH_PLAN_HASH_MISMATCH', 'bad' );
$result = UPC_Research_Runtime::import_bound_plan( 'pferde-atelier' );
runtime_assert( is_wp_error( $result ) && 'UPC_RESEARCH_PLAN_HASH_MISMATCH' === $result->get_error_code(), 'bound plan blocker propagates fail closed' );

$source = file_get_contents( dirname( __DIR__ ) . '/src/class-upc-research-runtime.php' );
runtime_assert( false === stripos( $source, 'add_action' ), 'runtime registers no automatic hook' );
runtime_assert( false === stripos( $source, 'wp_schedule' ), 'runtime registers no scheduler' );
runtime_assert( false === stripos( $source, 'wp_insert_post' ), 'runtime contains no article insert' );
runtime_assert( false === stripos( $source, 'wp_update_post' ), 'runtime contains no article update' );

fwrite( STDOUT, "UPC_RESEARCH_RUNTIME_GESAMT_PASS\n" );
