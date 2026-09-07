<?php
/**
 * Plugin Name: Universal Product Comparison
 * Description: Minimal comparison core on top of Universal Product Knowledge.
 * Version: 0.2.2-prototype
 * Requires at least: 6.4
 * Requires PHP: 7.4
 * Requires Plugins: universal-product-knowledge
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

define( 'UPC_VERSION', '0.2.2-prototype' );
define( 'UPC_SCHEMA_VERSION', '2' );
define( 'UPC_PLUGIN_FILE', __FILE__ );

require_once __DIR__ . '/src/class-upc-repository.php';
require_once __DIR__ . '/src/class-upc-rulebook.php';
require_once __DIR__ . '/src/class-upc-writer.php';
require_once __DIR__ . '/src/class-upc-validator.php';
require_once __DIR__ . '/src/class-upc-production.php';
require_once __DIR__ . '/src/class-upc-project-config.php';
require_once __DIR__ . '/src/class-upc-wordpress-draft.php';
require_once __DIR__ . '/src/class-upc-affiliate-bridge.php';
require_once __DIR__ . '/src/class-upc-seo-signals.php';
require_once __DIR__ . '/src/class-upc-link-manifest.php';
require_once __DIR__ . '/src/class-upc-link-finalizer.php';
require_once __DIR__ . '/src/class-upc-comparison-graphic.php';
require_once __DIR__ . '/src/class-upc-article-finalizer.php';
require_once __DIR__ . '/src/class-upc-bound-dossier-importer.php';
require_once __DIR__ . '/src/class-upc-admin-pv-reg-001-test.php';
require_once __DIR__ . '/src/class-upc-archive.php';

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
    $features        = $wpdb->prefix . 'upc_features';

    $sql_comparisons = "CREATE TABLE {$comparisons} (
        id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
        comparison_key varchar(191) NOT NULL,
        comparison_type varchar(16) NOT NULL,
        product_group_key varchar(191) NOT NULL,
        working_title text NOT NULL,
        decision_intent text NOT NULL,
        comparability_note text NOT NULL,
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

    $sql_features = "CREATE TABLE {$features} (
        id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
        comparison_id bigint(20) unsigned NOT NULL,
        fact_key varchar(191) NOT NULL,
        label varchar(191) NOT NULL,
        position smallint(5) unsigned NOT NULL,
        required tinyint(1) unsigned NOT NULL DEFAULT 1,
        created_at datetime NOT NULL,
        PRIMARY KEY  (id),
        UNIQUE KEY comparison_fact (comparison_id, fact_key),
        UNIQUE KEY comparison_position (comparison_id, position)
    ) {$charset_collate};";

    dbDelta( $sql_comparisons );
    dbDelta( $sql_items );
    dbDelta( $sql_features );

    update_option( 'upc_schema_version', UPC_SCHEMA_VERSION, false );
}
register_activation_hook( __FILE__, 'upc_install_schema' );

function upc_maybe_upgrade_schema() {
    if ( (string) get_option( 'upc_schema_version', '' ) !== (string) UPC_SCHEMA_VERSION ) {
        upc_install_schema();
    }
}
add_action( 'plugins_loaded', 'upc_maybe_upgrade_schema', 20 );
add_action( 'plugins_loaded', array( 'UPC_Affiliate_Bridge', 'register' ), 25 );
if ( is_admin() ) {
    UPC_Admin_PV_REG_001_Test::register();
}

function upc_seo_signals( $comparison_id ) {
    return UPC_SEO_Signals::for_comparison( $comparison_id );
}

function upc_comparison_graphic( $comparison_id ) {
    $repository = upc_repository();
    if ( is_wp_error( $repository ) ) {
        return $repository;
    }
    $graphic = new UPC_Comparison_Graphic( $repository );
    return $graphic->build( $comparison_id );
}

function upc_link_manifest( $comparison_id, $project_key ) {
    $repository = upc_repository();
    if ( is_wp_error( $repository ) ) {
        return $repository;
    }
    $resolver = new UPC_Link_Manifest( $repository );
    return $resolver->build( $comparison_id, $project_key );
}

function upc_finalize_internal_links( $comparison_id, $project_key, $ruleset_id ) {
    $repository = upc_repository();
    $production = upc_production();
    if ( is_wp_error( $repository ) ) {
        return $repository;
    }
    if ( is_wp_error( $production ) ) {
        return $production;
    }
    $finalizer = new UPC_Link_Finalizer( $production, $repository );
    return $finalizer->finalize( $comparison_id, $project_key, $ruleset_id );
}

function upc_finalize_article( $comparison_id, $project_key, $ruleset_id ) {
    $repository = upc_repository();
    $production = upc_production();
    if ( is_wp_error( $repository ) ) {
        return $repository;
    }
    if ( is_wp_error( $production ) ) {
        return $production;
    }

    $links   = new UPC_Link_Finalizer( $production, $repository );
    $graphic = new UPC_Comparison_Graphic( $repository );
    $final   = new UPC_Article_Finalizer( $links, $graphic );

    return $final->finalize( $comparison_id, $project_key, $ruleset_id );
}

function upc_archive() {
    $repository = upc_repository();
    if ( is_wp_error( $repository ) ) {
        return $repository;
    }
    return new UPC_Archive( $repository );
}

function upc_wordpress_draft() {
    $production = upc_production();
    if ( is_wp_error( $production ) ) {
        return $production;
    }
    return new UPC_WordPress_Draft( $production );
}

function upc_production() {
    $repository = upc_repository();
    if ( is_wp_error( $repository ) ) {
        return $repository;
    }
    return new UPC_Production( $repository );
}

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

function upc_comparison_archive_shortcode( $atts ) {
    $atts = shortcode_atts(
        array(
            'project'  => '',
            'category' => '',
        ),
        $atts,
        'upc_comparison_archive'
    );

    $archive = upc_archive();
    if ( is_wp_error( $archive ) ) {
        return '';
    }

    $html = $archive->render(
        sanitize_key( $atts['project'] ),
        sanitize_title( $atts['category'] )
    );

    return is_wp_error( $html ) ? '' : $html;
}
add_shortcode( 'upc_comparison_archive', 'upc_comparison_archive_shortcode' );
