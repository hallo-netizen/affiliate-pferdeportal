<?php

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

/**
 * Stable semantic fingerprint for product knowledge.
 *
 * Verification timestamps are intentionally excluded: a periodic re-check with
 * unchanged facts must not trigger comparison/article work.
 */
class UPK_Change_Fingerprint {
    private $knowledge;

    public function __construct( $knowledge ) {
        $this->knowledge = $knowledge;
    }

    public function product( $product_id ) {
        $bundle = $this->knowledge->get_product_bundle( absint( $product_id ) );
        if ( is_wp_error( $bundle ) ) {
            return $bundle;
        }

        $payload = array(
            'subject_type' => UPK_Repository::SUBJECT_PRODUCT,
            'subject_id'   => (int) $product_id,
            'identity'     => $this->pick( $bundle, array(
                'manufacturer',
                'model_name',
                'model_family',
                'product_group_key',
                'manufacturer_product_url',
                'generation',
                'lifecycle_status',
                'successor_product_id',
            ) ),
            'identifiers'  => $this->normalize_records(
                isset( $bundle['identifiers'] ) ? $bundle['identifiers'] : array(),
                array( 'identifier_type', 'identifier_value' )
            ),
            'facts'        => $this->normalize_records(
                isset( $bundle['facts'] ) ? $bundle['facts'] : array(),
                array( 'fact_key', 'fact_value', 'fact_note', 'unit', 'source_url', 'source_type', 'fact_status' )
            ),
        );

        return hash( 'sha256', json_encode( $payload, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE ) );
    }

    public function variant( $variant_id ) {
        $bundle = $this->knowledge->get_variant_bundle( absint( $variant_id ) );
        if ( is_wp_error( $bundle ) ) {
            return $bundle;
        }

        $product = isset( $bundle['product'] ) && is_array( $bundle['product'] ) ? $bundle['product'] : array();
        $payload = array(
            'subject_type' => UPK_Repository::SUBJECT_VARIANT,
            'subject_id'   => (int) $variant_id,
            'identity'     => $this->pick( $bundle, array(
                'product_id',
                'variant_name',
                'variant_key',
                'lifecycle_status',
            ) ),
            'base_product_identity' => $this->pick( $product, array(
                'manufacturer',
                'model_name',
                'product_group_key',
                'generation',
                'lifecycle_status',
            ) ),
            'identifiers'  => $this->normalize_records(
                isset( $bundle['identifiers'] ) ? $bundle['identifiers'] : array(),
                array( 'identifier_type', 'identifier_value' )
            ),
            'facts'        => $this->normalize_records(
                isset( $bundle['facts'] ) ? $bundle['facts'] : array(),
                array( 'fact_key', 'fact_value', 'fact_note', 'unit', 'source_url', 'source_type', 'fact_status' )
            ),
        );

        return hash( 'sha256', json_encode( $payload, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE ) );
    }

    private function pick( array $record, array $keys ) {
        $picked = array();
        foreach ( $keys as $key ) {
            $picked[ $key ] = array_key_exists( $key, $record ) ? $record[ $key ] : null;
        }
        return $picked;
    }

    private function normalize_records( $records, array $keys ) {
        $normalized = array();
        foreach ( is_array( $records ) ? $records : array() as $record ) {
            if ( is_array( $record ) ) {
                $normalized[] = $this->pick( $record, $keys );
            }
        }
        usort(
            $normalized,
            function( $a, $b ) {
                return strcmp(
                    json_encode( $a, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE ),
                    json_encode( $b, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE )
                );
            }
        );
        return $normalized;
    }
}
