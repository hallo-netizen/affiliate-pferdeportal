<?php

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

if ( ! class_exists( 'UPC_Feature_Key_Catalog' ) ) {
    require_once __DIR__ . '/class-upc-feature-key-catalog.php';
}
if ( ! class_exists( 'UPC_Research_Importer' ) ) {
    require_once __DIR__ . '/class-upc-research-importer.php';
}
if ( ! class_exists( 'UPC_Maintenance' ) ) {
    require_once __DIR__ . '/class-upc-maintenance.php';
}
if ( ! class_exists( 'UPC_Research_Refresh_Planner' ) ) {
    require_once __DIR__ . '/class-upc-research-refresh-planner.php';
}
if ( ! class_exists( 'UPC_Research_Refresh_Result_Validator' ) ) {
    require_once __DIR__ . '/class-upc-research-refresh-result-validator.php';
}
if ( ! class_exists( 'UPC_Research_Refresh_Applier' ) ) {
    require_once __DIR__ . '/class-upc-research-refresh-applier.php';
}
if ( ! class_exists( 'UPC_Candidate_Gate' ) ) {
    require_once __DIR__ . '/class-upc-candidate-gate.php';
}
if ( ! class_exists( 'UPC_Candidate_Applier' ) ) {
    require_once __DIR__ . '/class-upc-candidate-applier.php';
}

/**
 * Explicit runtime bridge for bound research bootstrap and refresh maintenance.
 *
 * Nothing is scheduled or executed automatically. A caller must invoke these
 * methods deliberately. Import/apply stay fail-closed; planning is read-only.
 */
class UPC_Research_Runtime {
    public static function import_bound_plan( $project_key = 'pferde-atelier' ) {
        $project_key = sanitize_key( $project_key );
        if ( '' === $project_key ) {
            return new WP_Error( 'UPC_RESEARCH_PROJECT_KEY_MISSING', 'Project key is required.' );
        }

        $dependency = self::ensure_product_maintenance();
        if ( is_wp_error( $dependency ) ) {
            return $dependency;
        }

        if ( ! function_exists( 'upk_repository' )
            || ! function_exists( 'upc_repository' )
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

    public static function build_due_refresh_plan( $project_key = 'pferde-atelier', $as_of_utc = '', $limit_per_group = 500 ) {
        $project_key = sanitize_key( $project_key );
        if ( '' === $project_key ) {
            return new WP_Error( 'UPC_REFRESH_PROJECT_KEY_MISSING', 'Project key is required.' );
        }

        $dependency = self::ensure_product_maintenance();
        if ( is_wp_error( $dependency ) ) {
            return $dependency;
        }

        if ( ! function_exists( 'upk_repository' )
            || ! class_exists( 'UPC_Maintenance' )
            || ! class_exists( 'UPC_Research_Refresh_Planner' )
        ) {
            return new WP_Error( 'UPC_REFRESH_RUNTIME_DEPENDENCY_MISSING', 'Refresh planning runtime dependency is missing.' );
        }

        $knowledge = upk_repository();
        if ( is_wp_error( $knowledge ) ) {
            return $knowledge;
        }

        global $wpdb;
        $product_maintenance = new UPK_Maintenance( $wpdb );
        $comparison_maintenance = new UPC_Maintenance( $wpdb );
        $planner = new UPC_Research_Refresh_Planner( $knowledge, $product_maintenance, $comparison_maintenance );

        return $planner->build( $project_key, $as_of_utc, $limit_per_group );
    }

    public static function apply_refresh_results( array $plan, array $results ) {
        $dependency = self::ensure_product_refresh_apply_support();
        if ( is_wp_error( $dependency ) ) {
            return $dependency;
        }
        if ( ! function_exists( 'upk_repository' )
            || ! class_exists( 'UPC_Maintenance' )
            || ! class_exists( 'UPC_Research_Refresh_Result_Validator' )
            || ! class_exists( 'UPC_Research_Refresh_Applier' )
        ) {
            return new WP_Error( 'UPC_REFRESH_RUNTIME_DEPENDENCY_MISSING', 'Refresh apply runtime dependency is missing.' );
        }

        $knowledge = upk_repository();
        if ( is_wp_error( $knowledge ) ) {
            return $knowledge;
        }

        global $wpdb;
        $product_maintenance = new UPK_Maintenance( $wpdb );
        $comparison_maintenance = new UPC_Maintenance( $wpdb );
        $fact_snapshot = new UPK_Fact_Snapshot( $wpdb, $knowledge );
        $fingerprint = new UPK_Change_Fingerprint( $knowledge );
        $validator = new UPC_Research_Refresh_Result_Validator( $knowledge );
        $applier = new UPC_Research_Refresh_Applier(
            $wpdb,
            $validator,
            $product_maintenance,
            $fact_snapshot,
            $fingerprint,
            $comparison_maintenance
        );

        return $applier->apply( $plan, $results );
    }

    public static function evaluate_candidate( array $candidate, $project_key = 'pferde-atelier' ) {
        $project_key = sanitize_key( $project_key );
        if ( '' === $project_key ) {
            return new WP_Error( 'UPC_CANDIDATE_PROJECT_KEY_MISSING', 'Project key is required.' );
        }

        $dependency = self::ensure_product_maintenance();
        if ( is_wp_error( $dependency ) ) {
            return $dependency;
        }
        if ( ! class_exists( 'UPC_Feature_Key_Catalog' ) || ! class_exists( 'UPC_Candidate_Gate' ) ) {
            return new WP_Error( 'UPC_CANDIDATE_RUNTIME_DEPENDENCY_MISSING', 'Candidate runtime dependency is missing.' );
        }

        global $wpdb;
        $maintenance = new UPK_Maintenance( $wpdb );
        $base = dirname( __DIR__ ) . '/config/' . $project_key . '/';
        $catalog = UPC_Feature_Key_Catalog::load( $base . 'feature-key-catalog.json' );
        if ( is_wp_error( $catalog ) ) {
            return $catalog;
        }
        $policy = UPC_Candidate_Gate::load_policy( $base . 'maintenance-groups.json' );
        if ( is_wp_error( $policy ) ) {
            return $policy;
        }

        $gate = new UPC_Candidate_Gate( $maintenance, $catalog, $policy );
        return $gate->evaluate( $candidate );
    }

    public static function accept_candidate( array $candidate, array $release ) {
        $dependency = self::ensure_product_maintenance();
        if ( is_wp_error( $dependency ) ) {
            return $dependency;
        }
        if ( ! function_exists( 'upk_repository' ) || ! class_exists( 'UPC_Candidate_Applier' ) ) {
            return new WP_Error( 'UPC_CANDIDATE_RUNTIME_DEPENDENCY_MISSING', 'Candidate acceptance runtime dependency is missing.' );
        }

        $knowledge = upk_repository();
        if ( is_wp_error( $knowledge ) ) {
            return $knowledge;
        }

        global $wpdb;
        $maintenance = new UPK_Maintenance( $wpdb );
        $applier = new UPC_Candidate_Applier( $wpdb, $knowledge, $maintenance );
        return $applier->apply( $candidate, $release );
    }

    private static function ensure_product_maintenance() {
        if ( class_exists( 'UPK_Maintenance' ) ) {
            return true;
        }
        if ( ! defined( 'UPK_PLUGIN_FILE' ) ) {
            return new WP_Error( 'UPC_RESEARCH_RUNTIME_DEPENDENCY_MISSING', 'Universal Product Knowledge plugin path is not bound.' );
        }
        $maintenance_path = dirname( UPK_PLUGIN_FILE ) . '/src/class-upk-maintenance.php';
        if ( ! is_file( $maintenance_path ) ) {
            return new WP_Error( 'UPC_RESEARCH_RUNTIME_DEPENDENCY_MISSING', 'Product knowledge maintenance class is missing.' );
        }
        require_once $maintenance_path;
        return class_exists( 'UPK_Maintenance' )
            ? true
            : new WP_Error( 'UPC_RESEARCH_RUNTIME_DEPENDENCY_MISSING', 'Product knowledge maintenance class did not load.' );
    }

    private static function ensure_product_refresh_apply_support() {
        $maintenance = self::ensure_product_maintenance();
        if ( is_wp_error( $maintenance ) ) {
            return $maintenance;
        }
        if ( class_exists( 'UPK_Fact_Snapshot' ) && class_exists( 'UPK_Change_Fingerprint' ) ) {
            return true;
        }
        if ( ! defined( 'UPK_PLUGIN_FILE' ) ) {
            return new WP_Error( 'UPC_REFRESH_RUNTIME_DEPENDENCY_MISSING', 'Universal Product Knowledge plugin path is not bound.' );
        }

        $base = dirname( UPK_PLUGIN_FILE ) . '/src/';
        $required = array(
            'UPK_Fact_Snapshot' => 'class-upk-fact-snapshot.php',
            'UPK_Change_Fingerprint' => 'class-upk-change-fingerprint.php',
        );
        foreach ( $required as $class => $file ) {
            if ( class_exists( $class ) ) {
                continue;
            }
            $path = $base . $file;
            if ( ! is_file( $path ) ) {
                return new WP_Error( 'UPC_REFRESH_RUNTIME_DEPENDENCY_MISSING', 'Product knowledge refresh support is missing.' );
            }
            require_once $path;
            if ( ! class_exists( $class ) ) {
                return new WP_Error( 'UPC_REFRESH_RUNTIME_DEPENDENCY_MISSING', 'Product knowledge refresh support did not load.' );
            }
        }
        return true;
    }
}
