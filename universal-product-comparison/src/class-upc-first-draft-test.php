<?php

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

/**
 * One bound admin test:
 * PV-REG-001 -> Pferde Atelier -> exact category 11 -> draft only.
 */
class UPC_First_Draft_Test {
    const DOSSIER_ID     = 'pv-reg-001';
    const DOSSIER_SHA256 = '39c69113bc57d057b002c1a612470f9944446bd414006b9ebe1c8d09f40f5fe5';
    const PROJECT_KEY    = 'pferde-atelier';
    const RULESET_ID     = 'pv-reg-001-v1';
    const MENU_SLUG      = 'upc-first-draft-test';

    public static function register() {
        add_action( 'admin_menu', array( __CLASS__, 'register_menu' ) );
        add_action( 'admin_post_upc_run_first_draft_test', array( __CLASS__, 'handle_admin_run' ) );
    }

    public static function register_menu() {
        add_management_page(
            'Produktvergleich Test',
            'Produktvergleich Test',
            'manage_options',
            self::MENU_SLUG,
            array( __CLASS__, 'render_page' )
        );
    }

    public static function render_page() {
        if ( ! current_user_can( 'manage_options' ) ) {
            return;
        }

        $status  = isset( $_GET['upc_status'] ) ? sanitize_key( wp_unslash( $_GET['upc_status'] ) ) : '';
        $error   = isset( $_GET['upc_error'] ) ? sanitize_key( wp_unslash( $_GET['upc_error'] ) ) : '';
        $post_id = isset( $_GET['upc_post_id'] ) ? absint( $_GET['upc_post_id'] ) : 0;

        echo '<div class="wrap">';
        echo '<h1>Produktvergleich Test</h1>';
        echo '<p><strong>Fest gebunden:</strong> PV-REG-001 → Vergleich Regendecken (Term-ID 11) → WordPress-Draft.</p>';
        echo '<p><strong>Version:</strong> ' . esc_html( UPC_VERSION ) . '</p>';

        if ( 'pass' === $status && $post_id > 0 ) {
            echo '<div class="notice notice-success"><p><strong>PASS:</strong> Der gebundene Test-Draft wurde erzeugt und rückgeprüft.</p></div>';
            $edit_link = get_edit_post_link( $post_id, '' );
            if ( $edit_link ) {
                echo '<p><a class="button button-primary" href="' . esc_url( $edit_link ) . '">Draft öffnen</a></p>';
            }
        } elseif ( '' !== $error ) {
            echo '<div class="notice notice-error"><p><strong>BLOCKED:</strong> ' . esc_html( $error ) . '</p></div>';
        }

        echo '<form method="post" action="' . esc_url( admin_url( 'admin-post.php' ) ) . '">';
        wp_nonce_field( 'upc_run_first_draft_test' );
        echo '<input type="hidden" name="action" value="upc_run_first_draft_test">';
        submit_button( 'PV-REG-001 als Draft testen', 'primary', 'submit', false );
        echo '</form>';

        echo '<p>Kein freier Titel, kein freier Text, kein freies Produkt, keine freie Kategorie, kein Publish.</p>';
        echo '</div>';
    }

    public static function handle_admin_run() {
        if ( ! current_user_can( 'manage_options' ) ) {
            wp_die( 'Forbidden', 403 );
        }

        check_admin_referer( 'upc_run_first_draft_test' );

        $result = self::execute();

        if ( is_wp_error( $result ) ) {
            wp_safe_redirect(
                add_query_arg(
                    array(
                        'page'      => self::MENU_SLUG,
                        'upc_error' => sanitize_key( $result->get_error_code() ),
                    ),
                    admin_url( 'tools.php' )
                )
            );
            exit;
        }

        wp_safe_redirect(
            add_query_arg(
                array(
                    'page'        => self::MENU_SLUG,
                    'upc_status'  => 'pass',
                    'upc_post_id' => (int) $result['post_id'],
                ),
                admin_url( 'tools.php' )
            )
        );
        exit;
    }

    public static function execute() {
        global $wpdb;

        $repository = upc_repository();
        if ( is_wp_error( $repository ) ) {
            return $repository;
        }

        $dossier = self::load_bound_dossier();
        if ( is_wp_error( $dossier ) ) {
            return $dossier;
        }

        $comparison_key = sanitize_key( strtolower( $dossier['dossier_id'] ) );
        $comparison_id  = $repository->find_comparison_id_by_key( $comparison_key );

        if ( $comparison_id > 0 ) {
            $verified = self::verify_existing_comparison( $repository, $comparison_id, $dossier );
            if ( is_wp_error( $verified ) ) {
                return $verified;
            }

            return self::finalize_and_verify( $comparison_id );
        }

        $empty = self::assert_empty_first_test_store();
        if ( is_wp_error( $empty ) ) {
            return $empty;
        }

        $wpdb->query( 'START TRANSACTION' );

        $product_ids = array();

        foreach ( $dossier['products'] as $product ) {
            $product_id = upk_repository()->create_product(
                array(
                    'manufacturer'             => $product['manufacturer'],
                    'model_name'               => $product['model_name'],
                    'product_group_key'        => $product['product_group_key'],
                    'manufacturer_product_url' => $product['manufacturer_product_url'],
                    'lifecycle_status'         => $product['lifecycle_status'],
                    'last_verified_at'         => $product['last_verified_at'],
                )
            );

            if ( is_wp_error( $product_id ) ) {
                $wpdb->query( 'ROLLBACK' );
                return $product_id;
            }

            foreach ( $product['facts'] as $fact ) {
                $fact_id = upk_repository()->add_fact(
                    UPK_Repository::SUBJECT_PRODUCT,
                    $product_id,
                    array(
                        'fact_key'    => $fact['fact_key'],
                        'fact_value'  => $fact['fact_value'],
                        'source_url'  => $fact['source_url'],
                        'source_type' => $fact['source_type'],
                        'verified_at' => $fact['verified_at'],
                        'fact_status' => $fact['fact_status'],
                    )
                );

                if ( is_wp_error( $fact_id ) ) {
                    $wpdb->query( 'ROLLBACK' );
                    return $fact_id;
                }
            }

            $product_ids[] = (int) $product_id;
        }

        $comparison_id = $repository->create_comparison(
            array(
                'comparison_key'     => $comparison_key,
                'comparison_type'    => $dossier['comparison_type'],
                'subject_ids'        => $product_ids,
                'working_title'      => $dossier['working_title'],
                'decision_intent'    => isset( $dossier['decision_intent'] ) ? $dossier['decision_intent'] : '',
                'comparability_note' => $dossier['comparability_note'],
            )
        );

        if ( is_wp_error( $comparison_id ) ) {
            $wpdb->query( 'ROLLBACK' );
            return $comparison_id;
        }

        $feature_count = $repository->set_features( $comparison_id, $dossier['features'], false );
        if ( is_wp_error( $feature_count ) ) {
            $wpdb->query( 'ROLLBACK' );
            return $feature_count;
        }

        $required = $repository->validate_required_facts( $comparison_id );
        if ( is_wp_error( $required ) ) {
            $wpdb->query( 'ROLLBACK' );
            return $required;
        }

        $verified = self::verify_existing_comparison( $repository, $comparison_id, $dossier );
        if ( is_wp_error( $verified ) ) {
            $wpdb->query( 'ROLLBACK' );
            return $verified;
        }

        $wpdb->query( 'COMMIT' );

        return self::finalize_and_verify( $comparison_id );
    }

    private static function load_bound_dossier() {
        $path = dirname( __DIR__ ) . '/config/pferde-atelier/pv-reg-001.json';

        if ( ! is_file( $path ) ) {
            return new WP_Error( 'UPC_FIRST_TEST_DOSSIER_MISSING', 'Bound PV-REG-001 dossier file is missing.' );
        }

        $actual_hash = hash_file( 'sha256', $path );
        if ( ! hash_equals( self::DOSSIER_SHA256, strtolower( $actual_hash ) ) ) {
            return new WP_Error( 'UPC_FIRST_TEST_DOSSIER_HASH_MISMATCH', 'Bound PV-REG-001 dossier hash does not match.' );
        }

        $dossier = json_decode( file_get_contents( $path ), true );
        if ( ! is_array( $dossier ) ) {
            return new WP_Error( 'UPC_FIRST_TEST_DOSSIER_JSON_INVALID', 'Bound PV-REG-001 dossier is invalid JSON.' );
        }

        if ( 'PV-REG-001' !== (string) ( $dossier['dossier_id'] ?? '' )
            || 'PRODUCT' !== (string) ( $dossier['comparison_type'] ?? '' )
            || 'regendecken' !== sanitize_key( $dossier['product_group_key'] ?? '' )
            || 2 !== count( $dossier['products'] ?? array() )
            || 14 !== count( $dossier['features'] ?? array() )
        ) {
            return new WP_Error( 'UPC_FIRST_TEST_DOSSIER_CONTRACT_INVALID', 'Bound PV-REG-001 dossier violates the fixed first-test contract.' );
        }

        return $dossier;
    }

    private static function assert_empty_first_test_store() {
        global $wpdb;

        $counts = array(
            'products'    => (int) $wpdb->get_var( "SELECT COUNT(*) FROM {$wpdb->prefix}upk_products" ),
            'variants'    => (int) $wpdb->get_var( "SELECT COUNT(*) FROM {$wpdb->prefix}upk_variants" ),
            'identifiers' => (int) $wpdb->get_var( "SELECT COUNT(*) FROM {$wpdb->prefix}upk_identifiers" ),
            'facts'       => (int) $wpdb->get_var( "SELECT COUNT(*) FROM {$wpdb->prefix}upk_facts" ),
            'comparisons' => (int) $wpdb->get_var( "SELECT COUNT(*) FROM {$wpdb->prefix}upc_comparisons" ),
            'items'       => (int) $wpdb->get_var( "SELECT COUNT(*) FROM {$wpdb->prefix}upc_items" ),
            'features'    => (int) $wpdb->get_var( "SELECT COUNT(*) FROM {$wpdb->prefix}upc_features" ),
        );

        foreach ( $counts as $name => $count ) {
            if ( 0 !== $count ) {
                return new WP_Error(
                    'UPC_FIRST_TEST_STORE_NOT_EMPTY',
                    'First bound draft test requires empty product/comparison stores.',
                    array( 'table_group' => $name, 'count' => $count )
                );
            }
        }

        return true;
    }

    private static function verify_existing_comparison( $repository, $comparison_id, array $dossier ) {
        $bundle = $repository->get_comparison_bundle( $comparison_id );
        if ( is_wp_error( $bundle ) ) {
            return $bundle;
        }

        if ( 'pv-reg-001' !== (string) $bundle['comparison_key']
            || 'PRODUCT' !== (string) $bundle['comparison_type']
            || 'regendecken' !== (string) $bundle['product_group_key']
            || (string) $dossier['working_title'] !== (string) $bundle['working_title']
            || 2 !== count( $bundle['items'] )
            || 14 !== count( $bundle['features'] )
        ) {
            return new WP_Error( 'UPC_FIRST_TEST_EXISTING_COMPARISON_MISMATCH', 'Existing PV-REG-001 comparison differs from the bound dossier.' );
        }

        foreach ( array_values( $dossier['products'] ) as $index => $expected_product ) {
            $actual_product = $bundle['items'][ $index ]['knowledge'];

            if ( (string) $expected_product['manufacturer'] !== (string) $actual_product['manufacturer']
                || (string) $expected_product['model_name'] !== (string) $actual_product['model_name']
                || sanitize_key( $expected_product['product_group_key'] ) !== (string) $actual_product['product_group_key']
            ) {
                return new WP_Error( 'UPC_FIRST_TEST_PRODUCT_IDENTITY_MISMATCH', 'Existing PV-REG-001 product identity differs from the bound dossier.' );
            }

            $actual_by_key = array();
            foreach ( $actual_product['facts'] as $actual_fact ) {
                $actual_by_key[ $actual_fact['fact_key'] ][] = $actual_fact;
            }

            foreach ( $expected_product['facts'] as $expected_fact ) {
                $key = sanitize_key( $expected_fact['fact_key'] );
                if ( ! isset( $actual_by_key[ $key ] ) || 1 !== count( $actual_by_key[ $key ] ) ) {
                    return new WP_Error( 'UPC_FIRST_TEST_FACT_COUNT_MISMATCH', 'Existing PV-REG-001 fact count differs from the bound dossier.' );
                }

                $actual_fact = $actual_by_key[ $key ][0];
                if ( (string) $expected_fact['fact_value'] !== (string) $actual_fact['fact_value']
                    || (string) $expected_fact['fact_status'] !== (string) $actual_fact['fact_status']
                    || (string) $expected_fact['source_url'] !== (string) $actual_fact['source_url']
                    || (string) $expected_fact['source_type'] !== (string) $actual_fact['source_type']
                ) {
                    return new WP_Error( 'UPC_FIRST_TEST_FACT_MISMATCH', 'Existing PV-REG-001 fact differs from the bound dossier.' );
                }
            }
        }

        foreach ( array_values( $dossier['features'] ) as $index => $expected_feature ) {
            $actual_feature = $bundle['features'][ $index ];
            if ( sanitize_key( $expected_feature['fact_key'] ) !== (string) $actual_feature['fact_key']
                || (string) $expected_feature['label'] !== (string) $actual_feature['label']
            ) {
                return new WP_Error( 'UPC_FIRST_TEST_FEATURE_MISMATCH', 'Existing PV-REG-001 feature differs from the bound dossier.' );
            }
        }

        return true;
    }

    private static function finalize_and_verify( $comparison_id ) {
        $draft_layer = upc_wordpress_draft();
        if ( is_wp_error( $draft_layer ) ) {
            return $draft_layer;
        }

        $materialized = $draft_layer->materialize(
            $comparison_id,
            self::PROJECT_KEY,
            self::RULESET_ID
        );

        if ( is_wp_error( $materialized ) ) {
            return $materialized;
        }

        if ( 'WORDPRESS_DRAFT_VERIFIED' !== $materialized['status']
            || false !== $materialized['publish_allowed']
        ) {
            return new WP_Error( 'UPC_FIRST_TEST_MATERIALIZED_STATE_INVALID', 'Initial PV-REG-001 WordPress draft state is invalid.' );
        }

        $final = upc_finalize_article(
            $comparison_id,
            self::PROJECT_KEY,
            self::RULESET_ID
        );

        if ( is_wp_error( $final ) ) {
            return $final;
        }

        if ( 'WORDPRESS_DRAFT_FINAL_VERIFIED' !== $final['status']
            || false !== $final['publish_allowed']
            || empty( $final['post_id'] )
        ) {
            return new WP_Error( 'UPC_FIRST_TEST_FINAL_STATE_INVALID', 'Final PV-REG-001 draft state is invalid.' );
        }

        $post = get_post( (int) $final['post_id'] );
        if ( ! $post
            || 'draft' !== $post->post_status
            || array( 11 ) !== array_values( array_map( 'intval', wp_get_post_categories( $post->ID ) ) )
            || '0' !== (string) get_post_meta( $post->ID, '_upc_publish_allowed', true )
            || hash( 'sha256', (string) $post->post_content ) !== (string) $final['final_output_hash']
        ) {
            return new WP_Error( 'UPC_FIRST_TEST_WORDPRESS_READBACK_MISMATCH', 'Final PV-REG-001 WordPress draft readback failed.' );
        }

        return array(
            'status'            => 'PV_REG_001_WORDPRESS_DRAFT_PASS',
            'comparison_id'     => (int) $comparison_id,
            'post_id'           => (int) $post->ID,
            'final_output_hash' => (string) $final['final_output_hash'],
            'publish_allowed'   => false,
        );
    }
}
