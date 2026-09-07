<?php
/**
 * Plugin Name: Universal Product Comparison
 * Description: Minimal comparison core on top of Universal Product Knowledge.
 * Version: 0.1.0-prototype
 * Requires at least: 6.4
 * Requires PHP: 7.4
 * Requires Plugins: universal-product-knowledge
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

define( 'UPC_VERSION', '0.1.0-prototype' );
define( 'UPC_SCHEMA_VERSION', '1' );
define( 'UPC_PLUGIN_FILE', __FILE__ );

require_once __DIR__ . '/src/class-upc-repository.php';

function upc_dependency_ready() {
    return function_exists( 'upk_repository' ) && class_exists( 'UPK_Repository' );
}

function upc_install_schema() {
    global $wpdb;

    if ( ! upc_dependency_ready() ) {
        return;
    }

    require_once ABSPATH . 'wp-admin/includes/upgrade.php';

    $charset_collate = $wpdb->get_charset_collate();
    $comparisons     = $wpdb->prefix . 'upc_comparisons';
    $items           = $wpdb->prefix . 'upc_items';

    $sql_comparisons = "CREATE TABLE {$comparisons} (
        id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
        comparison_key varchar(191) NOT NULL,
        comparison_type varchar(16) NOT NULL,
        product_group_key varchar(191) NOT NULL,
        decision_intent text NOT NULL,
        set_hash char(64) NOT NULL,
        created_at datetime NOT NULL,
        updated_at datetime NOT NULL,
        PRIMARY KEY  (id),
        UNIQUE KEY comparison_key (comparison_key),
        UNIQUE KEY set_hash (set_hash),
        KEY comparison_type (comparison_type),
        KEY product_group_key (product_group_key)
    ) {$charset_collate};";

    $sql_items = "CREATE TABLE {$items} (
        id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
        comparison_id bigint(20) unsigned NOT NULL,
        subject_type varchar(16) NOT NULL,
        subject_id bigint(20) unsigned NOT NULL,
        position tinyint(3) unsigned NOT NULL,
        created_at datetime NOT NULL,
        PRIMARY KEY  (id),
        UNIQUE KEY comparison_subject (comparison_id, subject_type, subject_id),
        UNIQUE KEY comparison_position (comparison_id, position),
        KEY subject_lookup (subject_type, subject_id)
    ) {$charset_collate};";

    dbDelta( $sql_comparisons );
    dbDelta( $sql_items );

    update_option( 'upc_schema_version', UPC_SCHEMA_VERSION, false );
}
register_activation_hook( __FILE__, 'upc_install_schema' );

function upc_repository() {
    static $repository = null;

    if ( ! upc_dependency_ready() ) {
        return new WP_Error( 'UPC_PRODUCT_KNOWLEDGE_MISSING', 'Universal Product Knowledge is required.' );
    }

    if ( null === $repository ) {
        global $wpdb;
        $repository = new UPC_Repository( $wpdb, upk_repository() );
    }

    return $repository;
}
