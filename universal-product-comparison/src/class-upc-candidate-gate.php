<?php
if ( ! defined( 'ABSPATH' ) ) { exit; }

/**
 * Read-only routing for newly discovered product candidates.
 *
 * Candidate signals are never persisted here. Existing products go to the
 * refresh path; new products in approved groups must first be researched;
 * unknown groups go through the group market gate.
 */
class UPC_Candidate_Gate {
    private $maintenance;
    private $catalog;
    private $policy;

    public function __construct( $maintenance, $catalog, array $policy ) {
        $this->maintenance = $maintenance;
        $this->catalog     = $catalog;
        $this->policy      = $policy;
    }

    public static function load_policy( $path ) {
        if ( ! is_file( $path ) ) {
            return new WP_Error( 'UPC_CANDIDATE_POLICY_MISSING', 'Candidate policy is missing.' );
        }
        $data = json_decode( file_get_contents( $path ), true );
        if ( ! is_array( $data ) || '1' !== (string) ( $data['schema_version'] ?? '' ) || empty( $data['market_gate'] ) || empty( $data['groups'] ) || ! is_array( $data['groups'] ) ) {
            return new WP_Error( 'UPC_CANDIDATE_POLICY_INVALID', 'Candidate policy is invalid.' );
        }
        return $data;
    }

    public function evaluate( array $candidate ) {
        $identity = array(
            'manufacturer'      => isset( $candidate['manufacturer'] ) ? sanitize_text_field( $candidate['manufacturer'] ) : '',
            'model_name'        => isset( $candidate['model_name'] ) ? sanitize_text_field( $candidate['model_name'] ) : '',
            'product_group_key' => isset( $candidate['product_group_key'] ) ? sanitize_key( $candidate['product_group_key'] ) : '',
            'generation'        => isset( $candidate['generation'] ) ? sanitize_text_field( $candidate['generation'] ) : '',
        );
        $url = isset( $candidate['manufacturer_product_url'] ) ? esc_url_raw( $candidate['manufacturer_product_url'] ) : '';

        if ( '' === $identity['manufacturer'] || '' === $identity['model_name'] || '' === $identity['product_group_key'] || '' === $url ) {
            return new WP_Error( 'UPC_CANDIDATE_IDENTITY_INCOMPLETE', 'Candidate identity and manufacturer URL are required.' );
        }

        $group = $this->group_policy( $identity['product_group_key'] );
        if ( null === $group ) {
            $market = isset( $this->policy['market_gate'] ) && is_array( $this->policy['market_gate'] ) ? $this->policy['market_gate'] : array();
            return array(
                'status' => 'GROUP_MARKET_GATE_REQUIRED',
                'persisted' => false,
                'automatic_comparison_created' => false,
                'product_group_key' => $identity['product_group_key'],
                'minimum_independent_dossiers' => max( 1, (int) ( $market['minimum_independent_dossiers'] ?? 4 ) ),
                'exact_product_identity_required' => ! empty( $market['exact_product_identity_required'] ),
                'official_manufacturer_sources_required' => ! empty( $market['official_manufacturer_sources_required'] ),
                'comparability_gate_required' => ! empty( $market['comparability_gate_required'] ),
            );
        }

        $existing = $this->maintenance->find_product_id_by_identity( $identity );
        if ( is_wp_error( $existing ) ) {
            return $existing;
        }
        if ( (int) $existing > 0 ) {
            return array(
                'status' => 'EXISTING_PRODUCT',
                'action' => 'USE_REFRESH_PATH',
                'product_id' => (int) $existing,
                'persisted' => false,
                'automatic_comparison_created' => false,
            );
        }

        $facts = isset( $candidate['facts'] ) && is_array( $candidate['facts'] ) ? array_values( $candidate['facts'] ) : array();
        if ( empty( $facts ) ) {
            return array(
                'status' => 'RESEARCH_REQUIRED',
                'action' => 'RESEARCH_PRODUCT_THEN_REEVALUATE',
                'persisted' => false,
                'automatic_comparison_created' => false,
                'product_group_key' => $identity['product_group_key'],
                'required_additional_contracts' => array_values( $group['required_additional_contracts'] ?? array() ),
            );
        }

        $normalized_facts = array();
        foreach ( $facts as $row ) {
            if ( ! is_array( $row ) ) {
                return new WP_Error( 'UPC_CANDIDATE_FACT_INVALID', 'Candidate fact row is invalid.' );
            }
            $label = trim( (string) ( $row['label'] ?? '' ) );
            $key = $this->catalog->resolve( $label );
            if ( is_wp_error( $key ) ) {
                return $key;
            }
            $source_type = strtoupper( sanitize_text_field( $row['source_type'] ?? '' ) );
            if ( ! in_array( $source_type, array( 'MANUFACTURER', 'OFFICIAL_DOCUMENTATION' ), true ) ) {
                return new WP_Error( 'UPC_CANDIDATE_SOURCE_NOT_OFFICIAL', 'Candidate facts require official manufacturer sources.' );
            }
            $source_url = esc_url_raw( $row['source_url'] ?? '' );
            if ( '' === $source_url ) {
                return new WP_Error( 'UPC_CANDIDATE_SOURCE_URL_MISSING', 'Candidate fact source URL is required.' );
            }
            $status = strtoupper( sanitize_text_field( $row['fact_status'] ?? '' ) );
            if ( ! in_array( $status, array( 'VERIFIED', 'NOT_IN_SOURCE', 'SOURCE_CONFLICT', 'CONFIGURATION_DEPENDENT' ), true ) ) {
                return new WP_Error( 'UPC_CANDIDATE_FACT_STATUS_INVALID', 'Candidate fact status is invalid.' );
            }
            $value = isset( $row['fact_value'] ) ? sanitize_textarea_field( $row['fact_value'] ) : '';
            if ( 'VERIFIED' === $status && '' === $value ) {
                return new WP_Error( 'UPC_CANDIDATE_VERIFIED_FACT_EMPTY', 'Verified candidate fact requires a value.' );
            }
            $normalized_facts[] = array(
                'fact_key' => $key,
                'label' => $label,
                'fact_value' => $value,
                'fact_note' => isset( $row['fact_note'] ) ? sanitize_textarea_field( $row['fact_note'] ) : '',
                'unit' => isset( $row['unit'] ) ? sanitize_text_field( $row['unit'] ) : '',
                'source_url' => $source_url,
                'source_type' => $source_type,
                'fact_status' => $status,
                'verified_at' => isset( $row['verified_at'] ) ? sanitize_text_field( $row['verified_at'] ) : '',
            );
        }

        $required = array_values( $group['required_additional_contracts'] ?? array() );
        $completed = isset( $candidate['completed_contracts'] ) && is_array( $candidate['completed_contracts'] ) ? array_values( array_unique( array_map( 'sanitize_text_field', $candidate['completed_contracts'] ) ) ) : array();
        $missing_contracts = array_values( array_diff( $required, $completed ) );
        if ( ! empty( $missing_contracts ) ) {
            return new WP_Error( 'UPC_CANDIDATE_ADDITIONAL_CONTRACT_MISSING', 'Required candidate safety/fit contract is missing.', array( 'missing' => $missing_contracts ) );
        }

        return array(
            'status' => 'CANDIDATE_RESEARCH_READY',
            'action' => 'RUN_SEO_AND_COMPARABILITY_REVIEW',
            'persisted' => false,
            'automatic_comparison_created' => false,
            'identity' => $identity,
            'manufacturer_product_url' => $url,
            'facts' => $normalized_facts,
            'product_group_key' => $identity['product_group_key'],
            'required_additional_contracts' => $required,
        );
    }

    private function group_policy( $key ) {
        foreach ( $this->policy['groups'] as $group ) {
            if ( is_array( $group ) && (string) ( $group['product_group_key'] ?? '' ) === $key ) {
                return $group;
            }
        }
        return null;
    }
}
