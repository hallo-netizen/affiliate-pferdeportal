<?php

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

class UPC_Admin_PV_REG_001_Test {
    const PAGE = 'upc-pv-reg-001-test';

    public static function register() {
        add_action( 'admin_menu', array( __CLASS__, 'menu' ) );
        add_action( 'admin_post_upc_run_pv_reg_001_test', array( __CLASS__, 'run' ) );
    }

    public static function menu() {
        add_management_page(
            'Produktvergleich Test',
            'Produktvergleich Test',
            'manage_options',
            self::PAGE,
            array( __CLASS__, 'render' )
        );
    }

    public static function render() {
        if ( ! current_user_can( 'manage_options' ) ) {
            return;
        }

        $status  = isset( $_GET['upc_test_status'] ) ? sanitize_key( wp_unslash( $_GET['upc_test_status'] ) ) : '';
        $post_id = isset( $_GET['upc_test_post_id'] ) ? absint( $_GET['upc_test_post_id'] ) : 0;
        $error   = isset( $_GET['upc_test_error'] ) ? sanitize_key( wp_unslash( $_GET['upc_test_error'] ) ) : '';

        echo '<div class="wrap">';
        echo '<h1>Produktvergleich – gebundener PV-REG-001-Test</h1>';
        echo '<p>Version: <strong>' . esc_html( UPC_VERSION ) . '</strong></p>';
        echo '<p>Fest gebunden: PV-REG-001 → Pferde Atelier → Vergleich Regendecken (Term-ID 11). Kein Publish.</p>';

        if ( 'pass' === $status && $post_id > 0 ) {
            echo '<div class="notice notice-success"><p><strong>PASS:</strong> WordPress-Draft wurde erzeugt und vollständig rückgelesen.</p></div>';
            $edit = get_edit_post_link( $post_id, '' );
            if ( $edit ) {
                echo '<p><a class="button button-primary" href="' . esc_url( $edit ) . '">Draft öffnen</a></p>';
            }
        } elseif ( '' !== $error ) {
            echo '<div class="notice notice-error"><p><strong>BLOCKED:</strong> ' . esc_html( $error ) . '</p></div>';
        }

        echo '<form method="post" action="' . esc_url( admin_url( 'admin-post.php' ) ) . '">';
        wp_nonce_field( 'upc_run_pv_reg_001_test' );
        echo '<input type="hidden" name="action" value="upc_run_pv_reg_001_test">';
        submit_button( 'PV-REG-001 als Draft testen', 'primary', 'submit', false );
        echo '</form>';
        echo '<p>Der Knopf importiert ausschließlich das hashgebundene Dossier und erzeugt ausschließlich einen Draft. Kein freier Titel, kein freier Body, kein freies Produkt, keine freie Kategorie.</p>';
        echo '</div>';
    }

    public static function run() {
        if ( ! current_user_can( 'manage_options' ) ) {
            wp_die( 'Forbidden', 403 );
        }

        check_admin_referer( 'upc_run_pv_reg_001_test' );

        global $wpdb;

        $repository = upc_repository();
        if ( is_wp_error( $repository ) ) {
            self::redirect_error( $repository );
        }

        $importer = new UPC_Bound_Dossier_Importer( $repository, upk_repository(), $wpdb );
        $import   = $importer->import( 'pferde-atelier', 'pv-reg-001' );

        if ( is_wp_error( $import ) ) {
            self::redirect_error( $import );
        }

        $draft_materializer = upc_wordpress_draft();
        if ( is_wp_error( $draft_materializer ) ) {
            self::redirect_error( $draft_materializer );
        }

        $materialized = $draft_materializer->materialize(
            (int) $import['comparison_id'],
            'pferde-atelier',
            'pv-reg-001-v1'
        );
        if ( is_wp_error( $materialized ) ) {
            self::redirect_error( $materialized );
        }

        if ( 'WORDPRESS_DRAFT_VERIFIED' !== $materialized['status'] || false !== $materialized['publish_allowed'] ) {
            self::redirect_error( new WP_Error( 'UPC_ADMIN_TEST_DRAFT_STATE_INVALID', 'Bound draft state is invalid.' ) );
        }

        $final = upc_finalize_article( (int) $import['comparison_id'], 'pferde-atelier', 'pv-reg-001-v1' );
        if ( is_wp_error( $final ) ) {
            self::redirect_error( $final );
        }

        if ( 'WORDPRESS_DRAFT_FINAL_VERIFIED' !== $final['status'] || false !== $final['publish_allowed'] ) {
            self::redirect_error( new WP_Error( 'UPC_ADMIN_TEST_FINAL_STATE_INVALID', 'Final draft state is invalid.' ) );
        }

        wp_safe_redirect(
            add_query_arg(
                array(
                    'page'             => self::PAGE,
                    'upc_test_status'  => 'pass',
                    'upc_test_post_id' => (int) $final['post_id'],
                ),
                admin_url( 'tools.php' )
            )
        );
        exit;
    }

    private static function redirect_error( $error ) {
        $code = is_wp_error( $error ) ? $error->get_error_code() : 'UPC_UNKNOWN_ERROR';

        wp_safe_redirect(
            add_query_arg(
                array(
                    'page'           => self::PAGE,
                    'upc_test_error' => sanitize_key( $code ),
                ),
                admin_url( 'tools.php' )
            )
        );
        exit;
    }
}
