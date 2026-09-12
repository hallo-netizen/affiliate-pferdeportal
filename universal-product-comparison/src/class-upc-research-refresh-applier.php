<?php

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

/**
 * Atomic application of already validated product refresh research.
 *
 * Updates product knowledge only. It never writes WordPress posts. Semantic
 * changes return affected comparison IDs for later explicit re-evaluation.
 */
class UPC_Research_Refresh_Applier {
    private $wpdb;
    private $validator;
    private $product_maintenance;
    private $fact_snapshot;
    private $fingerprint;
    private $comparison_maintenance;

    public function __construct( $wpdb, $validator, $product_maintenance, $fact_snapshot, $fingerprint, $comparison_maintenance ) {
        $this->wpdb = $wpdb;
        $this->validator = $validator;
        $this->product_maintenance = $product_maintenance;
        $this->fact_snapshot = $fact_snapshot;
        $this->fingerprint = $fingerprint;
        $this->comparison_maintenance = $comparison_maintenance;
    }

    public function apply( array $plan, array $results ) {
        $this->wpdb->query( 'START TRANSACTION' );

        $validated = $this->validator->validate( $plan, $results );
        if ( is_wp_error( $validated ) ) {
            $this->wpdb->query( 'ROLLBACK' );
            return $validated;
        }

        $changed_products = array();
        $unchanged_products = array();
        $affected_comparisons = array();

        foreach ( $validated['results'] as $result ) {
            $product_id = absint( $result['product_id'] );
            $before = $this->fingerprint->product( $product_id );
            if ( is_wp_error( $before ) ) {
                $this->wpdb->query( 'ROLLBACK' );
                return $before;
            }

            $updated = $this->product_maintenance->update_product(
                $product_id,
                array(
                    'lifecycle_status' => $result['lifecycle_status'],
                    'manufacturer_product_url' => $result['manufacturer_product_url'],
                    'last_verified_at' => $result['verified_at'],
                )
            );
            if ( is_wp_error( $updated ) ) {
                $this->wpdb->query( 'ROLLBACK' );
                return $updated;
            }

            $replaced = $this->fact_snapshot->replace_product_facts(
                $product_id,
                $result['facts'],
                false
            );
            if ( is_wp_error( $replaced ) ) {
                $this->wpdb->query( 'ROLLBACK' );
                return $replaced;
            }

            $after = $this->fingerprint->product( $product_id );
            if ( is_wp_error( $after ) ) {
                $this->wpdb->query( 'ROLLBACK' );
                return $after;
            }

            if ( hash_equals( (string) $before, (string) $after ) ) {
                $unchanged_products[] = $product_id;
                continue;
            }

            $changed_products[] = $product_id;
            $affected = $this->comparison_maintenance->affected_comparisons_for_product( $product_id );
            if ( is_wp_error( $affected ) ) {
                $this->wpdb->query( 'ROLLBACK' );
                return $affected;
            }
            foreach ( (array) $affected as $comparison_id ) {
                $comparison_id = absint( $comparison_id );
                if ( $comparison_id > 0 ) {
                    $affected_comparisons[ $comparison_id ] = true;
                }
            }
        }

        $this->wpdb->query( 'COMMIT' );
        $affected_ids = array_keys( $affected_comparisons );
        sort( $affected_ids, SORT_NUMERIC );
        sort( $changed_products, SORT_NUMERIC );
        sort( $unchanged_products, SORT_NUMERIC );

        return array(
            'schema_version' => '1',
            'contract' => 'UPC_PRODUCT_RESEARCH_REFRESH_APPLIED_V1',
            'project_key' => (string) $validated['project_key'],
            'maintenance_policy_sha256' => (string) $validated['maintenance_policy_sha256'],
            'result_count' => (int) $validated['result_count'],
            'changed_product_ids' => $changed_products,
            'unchanged_product_ids' => $unchanged_products,
            'affected_comparison_ids' => $affected_ids,
        );
    }
}
