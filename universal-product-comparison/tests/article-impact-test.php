<?php

define( 'ABSPATH', __DIR__ . '/' );

class WP_Error {
    private $code;
    public function __construct( $code, $message = '' ) { $this->code = $code; }
    public function get_error_code() { return $this->code; }
}
function is_wp_error( $value ) { return $value instanceof WP_Error; }
function sanitize_key( $value ) { return strtolower( preg_replace( '/[^a-z0-9_\-]/', '', (string) $value ) ); }

$GLOBALS['impact_post_ids'] = array();
$GLOBALS['impact_posts'] = array();
$GLOBALS['impact_meta'] = array();

function get_posts( $args ) { return $GLOBALS['impact_post_ids']; }
function get_post( $post_id ) { return isset( $GLOBALS['impact_posts'][ $post_id ] ) ? $GLOBALS['impact_posts'][ $post_id ] : null; }
function get_post_meta( $post_id, $key, $single ) {
    return isset( $GLOBALS['impact_meta'][ $post_id ][ $key ] ) ? $GLOBALS['impact_meta'][ $post_id ][ $key ] : '';
}

class Impact_Fake_Production {
    public $result;
    public function execute( $comparison_id, $project_key, $ruleset_id ) { return $this->result; }
}

function impact_assert( $condition, $label ) {
    if ( ! $condition ) {
        fwrite( STDERR, "FAIL: {$label}\n" );
        exit( 1 );
    }
    fwrite( STDOUT, "PASS: {$label}\n" );
}

require_once dirname( __DIR__ ) . '/src/class-upc-article-impact.php';

$production = new Impact_Fake_Production();
$impact = new UPC_Article_Impact( $production );
$production->result = array(
    'comparison_uid' => 'UPC-000001',
    'output_hash' => str_repeat( 'a', 64 ),
);

$GLOBALS['impact_post_ids'] = array();
$result = $impact->evaluate( 1, 'pferde-atelier', 'rules-v1' );
impact_assert( 'ARTICLE_MISSING' === $result['status'] && 0 === $result['post_id'], 'missing article classified without write' );

$post = new stdClass();
$post->ID = 77;
$post->post_status = 'draft';
$GLOBALS['impact_post_ids'] = array( 77 );
$GLOBALS['impact_posts'][77] = $post;
$GLOBALS['impact_meta'][77]['_upc_output_hash'] = str_repeat( 'a', 64 );
$result = $impact->evaluate( 1, 'pferde-atelier', 'rules-v1' );
impact_assert( 'ARTICLE_CURRENT' === $result['status'], 'unchanged draft classified current' );

$GLOBALS['impact_meta'][77]['_upc_output_hash'] = str_repeat( 'b', 64 );
$result = $impact->evaluate( 1, 'pferde-atelier', 'rules-v1' );
impact_assert( 'DRAFT_UPDATE_REQUIRED' === $result['status'], 'changed draft classified for safe refresh' );

$post->post_status = 'publish';
$result = $impact->evaluate( 1, 'pferde-atelier', 'rules-v1' );
impact_assert( 'PUBLISHED_REVIEW_REQUIRED' === $result['status'], 'changed published article never auto-overwritten' );

$post->post_status = 'private';
$result = $impact->evaluate( 1, 'pferde-atelier', 'rules-v1' );
impact_assert( 'PUBLISHED_REVIEW_REQUIRED' === $result['status'], 'changed non-draft article remains review-only' );

$GLOBALS['impact_post_ids'] = array( 77, 88 );
$result = $impact->evaluate( 1, 'pferde-atelier', 'rules-v1' );
impact_assert( is_wp_error( $result ) && 'UPC_DUPLICATE_WORDPRESS_TARGET' === $result->get_error_code(), 'duplicate WordPress targets blocked' );

$GLOBALS['impact_post_ids'] = array();
$production->result = new WP_Error( 'UPC_PRODUCTION_BLOCKED', 'blocked' );
$result = $impact->evaluate( 1, 'pferde-atelier', 'rules-v1' );
impact_assert( is_wp_error( $result ) && 'UPC_PRODUCTION_BLOCKED' === $result->get_error_code(), 'production blocker propagated fail closed' );

$production->result = array( 'comparison_uid' => '', 'output_hash' => '' );
$result = $impact->evaluate( 1, 'pferde-atelier', 'rules-v1' );
impact_assert( is_wp_error( $result ) && 'UPC_MAINTENANCE_OUTPUT_INVALID' === $result->get_error_code(), 'incomplete regenerated output blocked' );

$source = file_get_contents( dirname( __DIR__ ) . '/src/class-upc-article-impact.php' );
impact_assert( false === stripos( $source, 'wp_insert_post' ), 'impact classifier contains no post writer' );
impact_assert( false === stripos( $source, 'wp_update_post' ), 'impact classifier contains no post updater' );
impact_assert( false === stripos( $source, 'update_post_meta' ), 'impact classifier contains no meta writer' );

fwrite( STDOUT, "UPC_ARTICLE_IMPACT_GESAMT_PASS\n" );
