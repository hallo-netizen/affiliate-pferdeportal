<?php
if ( ! defined( 'ABSPATH' ) ) { exit; }

/**
 * Explicit acceptance of a fully researched product candidate after external
 * SEO and comparability release. No comparison or article is created here.
 */
class UPC_Candidate_Applier {
    private $wpdb;
    private $knowledge;
    private $maintenance;

    public function __construct( $wpdb, $knowledge, $maintenance ) {
        $this->wpdb = $wpdb;
        $this->knowledge = $knowledge;
        $this->maintenance = $maintenance;
    }

    public function apply( array $candidate, array $release ) {
        if ( 'CANDIDATE_RESEARCH_READY' !== (string) ( $candidate['status'] ?? '' ) || ! empty( $candidate['persisted'] ) ) {
            return new WP_Error( 'UPC_CANDIDATE_NOT_READY', 'Candidate is not a released research-ready candidate.' );
        }
        if ( 'PASS' !== strtoupper( sanitize_text_field( $release['seo_status'] ?? '' ) ) ) {
            return new WP_Error( 'UPC_CANDIDATE_SEO_NOT_PASS', 'SEO release must be PASS before candidate acceptance.' );
        }
        if ( 'PASS' !== strtoupper( sanitize_text_field( $release['comparability_status'] ?? '' ) ) ) {
            return new WP_Error( 'UPC_CANDIDATE_COMPARABILITY_NOT_PASS', 'Comparability release must be PASS before candidate acceptance.' );
        }

        $identity = isset( $candidate['identity'] ) && is_array( $candidate['identity'] ) ? $candidate['identity'] : array();
        $manufacturer = sanitize_text_field( $identity['manufacturer'] ?? '' );
        $model_name = sanitize_text_field( $identity['model_name'] ?? '' );
        $group_key = sanitize_key( $identity['product_group_key'] ?? '' );
        $generation = sanitize_text_field( $identity['generation'] ?? '' );
        $source_url = esc_url_raw( $candidate['manufacturer_product_url'] ?? '' );
        $verified_at = sanitize_text_field( $candidate['verified_at'] ?? '' );
        $facts = isset( $candidate['facts'] ) && is_array( $candidate['facts'] ) ? array_values( $candidate['facts'] ) : array();

        if ( '' === $manufacturer || '' === $model_name || '' === $group_key || '' === $source_url || '' === $verified_at || empty( $facts ) ) {
            return new WP_Error( 'UPC_CANDIDATE_ACCEPTANCE_PAYLOAD_INCOMPLETE', 'Candidate acceptance payload is incomplete.' );
        }
        if ( isset( $release['product_group_key'] ) && sanitize_key( $release['product_group_key'] ) !== $group_key ) {
            return new WP_Error( 'UPC_CANDIDATE_RELEASE_GROUP_MISMATCH', 'Release product group does not match candidate.' );
        }

        $existing = $this->maintenance->find_product_id_by_identity( array(
            'manufacturer' => $manufacturer,
            'model_name' => $model_name,
            'product_group_key' => $group_key,
            'generation' => $generation,
        ) );
        if ( is_wp_error( $existing ) ) {
            return $existing;
        }
        if ( (int) $existing > 0 ) {
            return array(
                'status' => 'EXISTING_PRODUCT_USE_REFRESH',
                'product_id' => (int) $existing,
                'product_group_key' => $group_key,
                'reevaluate_product_group' => false,
                'automatic_comparison_created' => false,
            );
        }

        $this->wpdb->query( 'START TRANSACTION' );
        $product_id = $this->knowledge->create_product( array(
            'manufacturer' => $manufacturer,
            'model_name' => $model_name,
            'product_group_key' => $group_key,
            'generation' => $generation,
            'manufacturer_product_url' => $source_url,
            'lifecycle_status' => 'UNKNOWN',
            'last_verified_at' => $verified_at,
        ) );
        if ( is_wp_error( $product_id ) ) {
            $this->wpdb->query( 'ROLLBACK' );
            return $product_id;
        }

        foreach ( $facts as $fact ) {
            $payload = array(
                'fact_key' => sanitize_key( $fact['fact_key'] ?? '' ),
                'fact_value' => sanitize_textarea_field( $fact['fact_value'] ?? '' ),
                'fact_note' => sanitize_textarea_field( $fact['fact_note'] ?? '' ),
                'unit' => sanitize_text_field( $fact['unit'] ?? '' ),
                'source_url' => esc_url_raw( $fact['source_url'] ?? '' ),
                'source_type' => strtoupper( sanitize_text_field( $fact['source_type'] ?? '' ) ),
                'verified_at' => sanitize_text_field( $fact['verified_at'] ?? '' ),
                'fact_status' => strtoupper( sanitize_text_field( $fact['fact_status'] ?? '' ) ),
            );
            $fact_id = $this->knowledge->add_fact( UPK_Repository::SUBJECT_PRODUCT, (int) $product_id, $payload );
            if ( is_wp_error( $fact_id ) ) {
                $this->wpdb->query( 'ROLLBACK' );
                return $fact_id;
            }
        }

        $this->wpdb->query( 'COMMIT' );
        return array(
            'status' => 'NEW_PRODUCT_ACCEPTED',
            'product_id' => (int) $product_id,
            'product_group_key' => $group_key,
            'reevaluate_product_group' => true,
            'automatic_comparison_created' => false,
            'article_write' => false,
        );
    }
}
