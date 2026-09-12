<?php

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

/**
 * Read-only validator for research results returned against a bound refresh plan.
 *
 * It does not mutate product knowledge. Stale product state, unknown fact scope,
 * missing safety contracts or pre-plan evidence fail closed.
 */
class UPC_Research_Refresh_Result_Validator {
    private $knowledge;

    public function __construct( $knowledge ) {
        $this->knowledge = $knowledge;
    }

    public function validate( array $plan, array $results ) {
        if ( '1' !== (string) ( $plan['schema_version'] ?? '' )
            || 'UPC_PRODUCT_RESEARCH_REFRESH_PLAN_V1' !== (string) ( $plan['contract'] ?? '' )
            || empty( $plan['project_key'] )
            || ! isset( $plan['tasks'] )
            || ! is_array( $plan['tasks'] )
            || 64 !== strlen( (string) ( $plan['maintenance_policy_sha256'] ?? '' ) )
        ) {
            return new WP_Error( 'UPC_REFRESH_RESULT_PLAN_INVALID', 'Refresh plan is invalid.' );
        }
        if ( empty( $results ) ) {
            return new WP_Error( 'UPC_REFRESH_RESULT_EMPTY', 'At least one refresh result is required.' );
        }

        $as_of = $this->normalize_datetime( (string) ( $plan['as_of_utc'] ?? '' ) );
        if ( is_wp_error( $as_of ) ) {
            return new WP_Error( 'UPC_REFRESH_RESULT_PLAN_INVALID', 'Refresh plan timestamp is invalid.' );
        }

        $tasks = array();
        foreach ( $plan['tasks'] as $task ) {
            if ( ! is_array( $task ) ) {
                return new WP_Error( 'UPC_REFRESH_RESULT_PLAN_INVALID', 'Refresh task is invalid.' );
            }
            $product_id = absint( $task['product_id'] ?? 0 );
            if ( 0 === $product_id || isset( $tasks[ $product_id ] ) ) {
                return new WP_Error( 'UPC_REFRESH_RESULT_PLAN_INVALID', 'Refresh task product binding is invalid or duplicated.' );
            }
            $expected_hash = UPC_Research_Refresh_Planner::task_binding_sha256(
                $task,
                (string) $plan['maintenance_policy_sha256']
            );
            if ( ! hash_equals( $expected_hash, (string) ( $task['task_binding_sha256'] ?? '' ) ) ) {
                return new WP_Error( 'UPC_REFRESH_RESULT_TASK_HASH_INVALID', 'Refresh task binding hash is invalid.' );
            }
            $tasks[ $product_id ] = $task;
        }

        $seen = array();
        $normalized = array();
        foreach ( $results as $result ) {
            if ( ! is_array( $result ) ) {
                return new WP_Error( 'UPC_REFRESH_RESULT_INVALID', 'Refresh result is invalid.' );
            }
            $product_id = absint( $result['product_id'] ?? 0 );
            if ( 0 === $product_id || ! isset( $tasks[ $product_id ] ) ) {
                return new WP_Error( 'UPC_REFRESH_RESULT_TASK_NOT_FOUND', 'Refresh result does not belong to this plan.' );
            }
            if ( isset( $seen[ $product_id ] ) ) {
                return new WP_Error( 'UPC_REFRESH_RESULT_DUPLICATE', 'Product occurs more than once in refresh results.' );
            }
            $seen[ $product_id ] = true;
            $task = $tasks[ $product_id ];

            if ( ! hash_equals( (string) $task['task_binding_sha256'], (string) ( $result['task_binding_sha256'] ?? '' ) ) ) {
                return new WP_Error( 'UPC_REFRESH_RESULT_TASK_HASH_MISMATCH', 'Refresh result task binding does not match the plan.' );
            }

            $bundle = $this->knowledge->get_product_bundle( $product_id );
            if ( is_wp_error( $bundle ) ) {
                return $bundle;
            }
            $current_task = $task;
            $current_task['product_group_key'] = (string) ( $bundle['product_group_key'] ?? '' );
            $current_task['manufacturer'] = (string) ( $bundle['manufacturer'] ?? '' );
            $current_task['model_name'] = (string) ( $bundle['model_name'] ?? '' );
            $current_task['generation'] = (string) ( $bundle['generation'] ?? '' );
            $current_task['lifecycle_status'] = (string) ( $bundle['lifecycle_status'] ?? 'UNKNOWN' );
            $current_task['manufacturer_product_url'] = (string) ( $bundle['manufacturer_product_url'] ?? '' );
            $current_task['last_verified_at'] = (string) ( $bundle['last_verified_at'] ?? '' );
            $current_hash = UPC_Research_Refresh_Planner::task_binding_sha256(
                $current_task,
                (string) $plan['maintenance_policy_sha256']
            );
            if ( ! hash_equals( (string) $task['task_binding_sha256'], $current_hash ) ) {
                return new WP_Error( 'UPC_REFRESH_RESULT_STALE_TASK', 'Product state changed after the refresh task was created.' );
            }

            $verified_at = $this->normalize_datetime( (string) ( $result['verified_at'] ?? '' ) );
            if ( is_wp_error( $verified_at ) || strcmp( $verified_at, $as_of ) < 0 ) {
                return new WP_Error( 'UPC_REFRESH_RESULT_VERIFICATION_TIME_INVALID', 'Refresh evidence predates the bound plan.' );
            }

            $lifecycle = strtoupper( sanitize_text_field( (string) ( $result['lifecycle_status'] ?? '' ) ) );
            if ( ! in_array( $lifecycle, UPK_Repository::lifecycle_statuses(), true ) ) {
                return new WP_Error( 'UPC_REFRESH_RESULT_LIFECYCLE_INVALID', 'Refresh lifecycle status is invalid.' );
            }

            $product_source = esc_url_raw( (string) ( $result['manufacturer_product_url'] ?? '' ) );
            if ( '' === $product_source ) {
                return new WP_Error( 'UPC_REFRESH_RESULT_PRODUCT_SOURCE_INVALID', 'Refresh manufacturer product URL is invalid.' );
            }

            $required_contracts = array_values( (array) ( $task['required_additional_contracts'] ?? array() ) );
            $completed_contracts = array_values( array_unique( array_map( 'sanitize_key', (array) ( $result['completed_additional_contracts'] ?? array() ) ) ) );
            foreach ( $required_contracts as $required ) {
                if ( ! in_array( sanitize_key( $required ), $completed_contracts, true ) ) {
                    return new WP_Error( 'UPC_REFRESH_RESULT_ADDITIONAL_CONTRACT_MISSING', 'Required safety/fit research contract is missing.' );
                }
            }

            $current_fact_keys = array();
            foreach ( (array) ( $bundle['facts'] ?? array() ) as $fact ) {
                $key = sanitize_key( (string) ( $fact['fact_key'] ?? '' ) );
                if ( '' !== $key ) {
                    $current_fact_keys[ $key ] = true;
                }
            }
            if ( empty( $current_fact_keys ) ) {
                return new WP_Error( 'UPC_REFRESH_RESULT_FACT_SCOPE_EMPTY', 'Current product has no fact scope to re-verify.' );
            }

            $facts = (array) ( $result['facts'] ?? array() );
            if ( empty( $facts ) ) {
                return new WP_Error( 'UPC_REFRESH_RESULT_FACTS_MISSING', 'Refresh result contains no facts.' );
            }
            $covered = array();
            $fact_identity = array();
            $normalized_facts = array();
            foreach ( $facts as $fact ) {
                if ( ! is_array( $fact ) ) {
                    return new WP_Error( 'UPC_REFRESH_RESULT_FACT_INVALID', 'Refresh fact is invalid.' );
                }
                $key = sanitize_key( (string) ( $fact['fact_key'] ?? '' ) );
                if ( '' === $key || ! isset( $current_fact_keys[ $key ] ) ) {
                    return new WP_Error( 'UPC_REFRESH_RESULT_FACT_SCOPE_UNKNOWN', 'Refresh fact is outside the product fact scope.' );
                }
                $source_url = esc_url_raw( (string) ( $fact['source_url'] ?? '' ) );
                $source_type = strtoupper( sanitize_text_field( (string) ( $fact['source_type'] ?? '' ) ) );
                $status = strtoupper( sanitize_text_field( (string) ( $fact['fact_status'] ?? '' ) ) );
                $value = sanitize_textarea_field( (string) ( $fact['fact_value'] ?? '' ) );
                if ( '' === $source_url
                    || ! in_array( $source_type, UPK_Repository::source_types(), true )
                    || ! in_array( $status, UPK_Repository::fact_statuses(), true )
                    || ( 'VERIFIED' === $status && '' === $value )
                ) {
                    return new WP_Error( 'UPC_REFRESH_RESULT_FACT_INVALID', 'Refresh fact or source binding is invalid.' );
                }
                $identity = $key . '|' . $source_url;
                if ( isset( $fact_identity[ $identity ] ) ) {
                    return new WP_Error( 'UPC_REFRESH_RESULT_FACT_DUPLICATE', 'Refresh fact source binding is duplicated.' );
                }
                $fact_identity[ $identity ] = true;
                $covered[ $key ] = true;
                $normalized_facts[] = array(
                    'fact_key' => $key,
                    'fact_value' => $value,
                    'unit' => sanitize_text_field( (string) ( $fact['unit'] ?? '' ) ),
                    'fact_note' => sanitize_textarea_field( (string) ( $fact['fact_note'] ?? '' ) ),
                    'source_url' => $source_url,
                    'source_type' => $source_type,
                    'verified_at' => $verified_at,
                    'fact_status' => $status,
                );
            }
            foreach ( array_keys( $current_fact_keys ) as $key ) {
                if ( ! isset( $covered[ $key ] ) ) {
                    return new WP_Error( 'UPC_REFRESH_RESULT_FACT_SCOPE_INCOMPLETE', 'Refresh result does not cover every current product fact key.' );
                }
            }

            $normalized[] = array(
                'product_id' => $product_id,
                'task_binding_sha256' => (string) $task['task_binding_sha256'],
                'verified_at' => $verified_at,
                'lifecycle_status' => $lifecycle,
                'manufacturer_product_url' => $product_source,
                'completed_additional_contracts' => $completed_contracts,
                'facts' => $normalized_facts,
            );
        }

        return array(
            'schema_version' => '1',
            'contract' => 'UPC_PRODUCT_RESEARCH_REFRESH_RESULT_VALIDATED_V1',
            'project_key' => (string) $plan['project_key'],
            'maintenance_policy_sha256' => (string) $plan['maintenance_policy_sha256'],
            'result_count' => count( $normalized ),
            'results' => $normalized,
        );
    }

    private function normalize_datetime( $value ) {
        $timestamp = strtotime( (string) $value );
        if ( false === $timestamp ) {
            return new WP_Error( 'UPC_REFRESH_RESULT_DATETIME_INVALID', 'Refresh datetime is invalid.' );
        }
        return gmdate( 'Y-m-d H:i:s', $timestamp );
    }
}
