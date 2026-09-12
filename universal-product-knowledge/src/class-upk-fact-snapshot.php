<?php

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

/**
 * Atomic replacement of the complete fact snapshot for one existing product.
 *
 * Uses the existing upk_facts table. No history table and no duplicate snapshot
 * storage. Callers can own the surrounding transaction when updating more state.
 */
class UPK_Fact_Snapshot {
    private $wpdb;
    private $repository;
    private $facts;

    public function __construct( $wpdb, $repository ) {
        $this->wpdb = $wpdb;
        $this->repository = $repository;
        $this->facts = $wpdb->prefix . 'upk_facts';
    }

    public function replace_product_facts( $product_id, array $facts, $manage_transaction = true ) {
        $product_id = absint( $product_id );
        if ( 0 === $product_id ) {
            return new WP_Error( 'UPK_FACT_SNAPSHOT_PRODUCT_INVALID', 'Product ID is invalid.' );
        }
        $bundle = $this->repository->get_product_bundle( $product_id );
        if ( is_wp_error( $bundle ) ) {
            return $bundle;
        }
        if ( empty( $facts ) ) {
            return new WP_Error( 'UPK_FACT_SNAPSHOT_EMPTY', 'A product fact snapshot cannot be empty.' );
        }

        $seen = array();
        foreach ( $facts as $fact ) {
            if ( ! is_array( $fact ) ) {
                return new WP_Error( 'UPK_FACT_SNAPSHOT_FACT_INVALID', 'Fact snapshot contains an invalid row.' );
            }
            $key = sanitize_key( (string) ( $fact['fact_key'] ?? '' ) );
            $source_url = esc_url_raw( (string) ( $fact['source_url'] ?? '' ) );
            if ( '' === $key || '' === $source_url ) {
                return new WP_Error( 'UPK_FACT_SNAPSHOT_FACT_INVALID', 'Fact snapshot key or source URL is invalid.' );
            }
            $identity = $key . '|' . $source_url;
            if ( isset( $seen[ $identity ] ) ) {
                return new WP_Error( 'UPK_FACT_SNAPSHOT_DUPLICATE', 'Fact snapshot contains a duplicate key/source binding.' );
            }
            $seen[ $identity ] = true;
        }

        if ( $manage_transaction ) {
            $this->wpdb->query( 'START TRANSACTION' );
        }

        $deleted = $this->wpdb->delete(
            $this->facts,
            array(
                'subject_type' => UPK_Repository::SUBJECT_PRODUCT,
                'subject_id' => $product_id,
            ),
            array( '%s', '%d' )
        );
        if ( false === $deleted ) {
            if ( $manage_transaction ) {
                $this->wpdb->query( 'ROLLBACK' );
            }
            return new WP_Error( 'UPK_FACT_SNAPSHOT_DELETE_FAILED', $this->wpdb->last_error ? $this->wpdb->last_error : 'Existing product facts could not be replaced.' );
        }

        foreach ( $facts as $fact ) {
            $fact_id = $this->repository->add_fact(
                UPK_Repository::SUBJECT_PRODUCT,
                $product_id,
                $fact
            );
            if ( is_wp_error( $fact_id ) ) {
                if ( $manage_transaction ) {
                    $this->wpdb->query( 'ROLLBACK' );
                }
                return $fact_id;
            }
        }

        if ( $manage_transaction ) {
            $this->wpdb->query( 'COMMIT' );
        }
        return count( $facts );
    }
}
