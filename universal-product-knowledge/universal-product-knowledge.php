<?php
/**
 * Plugin Name: Universal Product Knowledge
 * Description: Internal, source-bound product knowledge store for comparisons, advisory content and exact affiliate matching.
 * Version: 0.1.1-prototype
 * Requires at least: 6.4
 * Requires PHP: 7.4
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

define( 'UPK_VERSION', '0.1.1-prototype' );
define( 'UPK_SCHEMA_VERSION', '2' );
define( 'UPK_PLUGIN_FILE', __FILE__ );

require_once __DIR__ . '/src/class-upk-repository.php';

function upk_install_schema() {
    global $wpdb;

    require_once ABSPATH . 'wp-admin/includes/upgrade.php';

    $charset_collate = $wpdb->get_charset_collate();
    $products         = $wpdb->prefix . 'upk_products';
    $variants         = $wpdb->prefix . 'upk_variants';
    $identifiers      = $wpdb->prefix . 'upk_identifiers';
    $facts            = $wpdb->prefix . 'upk_facts';

    $sql_products = "CREATE TABLE {$products} (
        id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
        manufacturer varchar(191) NOT NULL,
        model_name varchar(191) NOT NULL,
        model_family varchar(191) NOT NULL DEFAULT '',
        product_group_key varchar(191) NOT NULL,
        manufacturer_product_url text NOT NULL,
        generation varchar(191) NOT NULL DEFAULT '',
        lifecycle_status varchar(32) NOT NULL DEFAULT 'UNKNOWN',
        successor_product_id bigint(20) unsigned NULL,
        last_verified_at datetime NOT NULL,
        created_at datetime NOT NULL,
        updated_at datetime NOT NULL,
        PRIMARY KEY  (id),
        KEY manufacturer_model (manufacturer, model_name),
        KEY product_group_key (product_group_key),
        KEY lifecycle_status (lifecycle_status)
    ) {$charset_collate};";

    $sql_variants = "CREATE TABLE {$variants} (
        id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
        product_id bigint(20) unsigned NOT NULL,
        variant_name varchar(191) NOT NULL,
        variant_key varchar(191) NOT NULL,
        lifecycle_status varchar(32) NOT NULL DEFAULT 'UNKNOWN',
        last_verified_at datetime NOT NULL,
        created_at datetime NOT NULL,
        updated_at datetime NOT NULL,
        PRIMARY KEY  (id),
        UNIQUE KEY product_variant (product_id, variant_key),
        KEY product_id (product_id),
        KEY lifecycle_status (lifecycle_status)
    ) {$charset_collate};";

    $sql_identifiers = "CREATE TABLE {$identifiers} (
        id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
        subject_type varchar(16) NOT NULL,
        subject_id bigint(20) unsigned NOT NULL,
        identifier_type varchar(40) NOT NULL,
        identifier_value varchar(191) NOT NULL,
        created_at datetime NOT NULL,
        PRIMARY KEY  (id),
        UNIQUE KEY identifier_unique (identifier_type, identifier_value),
        KEY subject_lookup (subject_type, subject_id)
    ) {$charset_collate};";

    $sql_facts = "CREATE TABLE {$facts} (
        id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
        subject_type varchar(16) NOT NULL,
        subject_id bigint(20) unsigned NOT NULL,
        fact_key varchar(191) NOT NULL,
        fact_value longtext NOT NULL,
        fact_note text NOT NULL,
        unit varchar(64) NOT NULL DEFAULT '',
        source_url text NOT NULL,
        source_type varchar(32) NOT NULL,
        verified_at datetime NOT NULL,
        fact_status varchar(40) NOT NULL,
        created_at datetime NOT NULL,
        updated_at datetime NOT NULL,
        PRIMARY KEY  (id),
        KEY subject_fact (subject_type, subject_id, fact_key),
        KEY fact_status (fact_status)
    ) {$charset_collate};";

    dbDelta( $sql_products );
    dbDelta( $sql_variants );
    dbDelta( $sql_identifiers );
    dbDelta( $sql_facts );

    update_option( 'upk_schema_version', UPK_SCHEMA_VERSION, false );
}
register_activation_hook( __FILE__, 'upk_install_schema' );

function upk_maybe_upgrade_schema() {
    if ( (string) get_option( 'upk_schema_version', '' ) !== (string) UPK_SCHEMA_VERSION ) {
        upk_install_schema();
    }
}
add_action( 'plugins_loaded', 'upk_maybe_upgrade_schema', 20 );

/**
 * Shared repository instance for other plugins/modules.
 *
 * @return UPK_Repository
 */
function upk_repository() {
    static $repository = null;

    if ( null === $repository ) {
        global $wpdb;
        $repository = new UPK_Repository( $wpdb );
    }

    return $repository;
}
