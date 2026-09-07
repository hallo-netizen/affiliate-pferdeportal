<?php

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

/**
 * Optional read-only SEO signal adapter.
 *
 * It never participates in renderer/production output. It is only for
 * candidate prioritisation and editorial planning outside the Zero-Freedom
 * production chain.
 */
class UPC_SEO_Signals {

    public static function for_comparison( $comparison_id ) {
        $comparison_id = absint( $comparison_id );
        if ( $comparison_id <= 0 ) {
            return new WP_Error( 'UPC_SEO_COMPARISON_ID_INVALID', 'Comparison id is invalid.' );
        }

        $repository = upc_repository();
        if ( is_wp_error( $repository ) ) {
            return $repository;
        }

        $bundle = $repository->get_comparison_bundle( $comparison_id );
        if ( is_wp_error( $bundle ) ) {
            return $bundle;
        }

        $context = array(
            'comparison_id'     => $comparison_id,
            'comparison_uid'    => (string) $bundle['comparison_uid'],
            'comparison_type'   => (string) $bundle['comparison_type'],
            'product_group_key' => (string) $bundle['product_group_key'],
            'working_title'     => (string) $bundle['working_title'],
        );

        /**
         * External SEO providers may return a signal block here.
         * No returned field can enter UPC_Production or UPC_Writer.
         */
        $signals = apply_filters( 'upc_product_comparison_seo_signals', array(), $context );
        if ( ! is_array( $signals ) ) {
            return new WP_Error( 'UPC_SEO_SIGNALS_INVALID', 'SEO signals must be an array.' );
        }

        $allowed = array(
            'target_keyword',
            'demand_score',
            'priority_score',
            'cannibalization_status',
            'provider',
            'provider_version',
        );

        $out = array();
        foreach ( $allowed as $key ) {
            if ( ! array_key_exists( $key, $signals ) ) {
                continue;
            }

            if ( in_array( $key, array( 'demand_score', 'priority_score' ), true ) ) {
                $value = is_numeric( $signals[ $key ] ) ? (float) $signals[ $key ] : null;
                if ( null !== $value ) {
                    $out[ $key ] = $value;
                }
                continue;
            }

            $value = sanitize_text_field( (string) $signals[ $key ] );
            if ( '' !== $value ) {
                $out[ $key ] = $value;
            }
        }

        return array(
            'status'  => empty( $out ) ? 'NO_SIGNALS' : 'SIGNALS_AVAILABLE',
            'context' => $context,
            'signals' => $out,
        );
    }
}
