<?php

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

/**
 * Explicit runtime bridge for the bound research bootstrap.
 *
 * Nothing is scheduled or executed automatically. A caller must invoke the
 * bridge deliberately; the importer remains fail-closed and transactional.
 */
class UPC_Research_Runtime {
    public static function import_bound_plan( $project_key = 'pferde-atelier' ) {
        $project_key = sanitize_key( $project_key );
        if ( '' === $project_key ) {
            return new WP_Error( 'UPC_RESEARCH_PROJECT_KEY_MISSING', 'Project key is required.' );
        }

        if ( ! function_exists( 'upk_repository' )
            || ! function_exists( 'upc_repository' )
            || ! class_exists( 'UPK_Maintenance' )
            || ! class_exists( 'UPC_Feature_Key_Catalog' )
            || ! class_exists( 'UPC_Research_Importer' )
        ) {
            return new WP_Error( 'UPC_RESEARCH_RUNTIME_DEPENDENCY_MISSING', 'Research import runtime dependency is missing.' );
        }

        $knowledge = upk_repository();
        if ( is_wp_error( $knowledge ) ) {
            return $knowledge;
        }

        $comparisons = upc_repository();
        if ( is_wp_error( $comparisons ) ) {
            return $comparisons;
        }

        global $wpdb;
        $maintenance = new UPK_Maintenance( $wpdb );

        $catalog_path = dirname( __DIR__ ) . '/config/' . $project_key . '/feature-key-catalog.json';
        $catalog = UPC_Feature_Key_Catalog::load( $catalog_path );
        if ( is_wp_error( $catalog ) ) {
            return $catalog;
        }

        $plan = UPC_Research_Importer::load_bound_plan( $project_key );
        if ( is_wp_error( $plan ) ) {
            return $plan;
        }

        $importer = new UPC_Research_Importer( $wpdb, $knowledge, $maintenance, $comparisons, $catalog );
        return $importer->import_plan( $plan );
    }
}
