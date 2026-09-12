<?php

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

/**
 * Read-only coverage report for Affiliate exact identifiers.
 *
 * A product counts as covered only when at least one GTIN/EAN/MPN is bound to
 * an official source and verification timestamp. Legacy/unbound identifiers do
 * not count.
 */
class UPC_Affiliate_Identifier_Coverage {
    private $wpdb;
    private $products;
    private $identifiers;

    public function __construct( $wpdb ) {
        $this->wpdb        = $wpdb;
        $this->products    = $wpdb->prefix . 'upk_products';
        $this->identifiers = $wpdb->prefix . 'upk_identifiers';
    }

    public function missing_products( $limit = 500, $product_group_key = '' ) {
        $limit = max( 1, min( 500, absint( $limit ) ) );
        $group = sanitize_key( $product_group_key );

        $where_group = '';
        $args = array(
            UPK_Repository::SUBJECT_PRODUCT,
            'GTIN',
            'EAN',
            'MPN',
            'MANUFACTURER',
            'OFFICIAL_DOCUMENTATION',
        );

        if ( '' !== $group ) {
            $where_group = ' AND p.product_group_key = %s';
            $args[] = $group;
        }
        $args[] = $limit;

        $sql = "SELECT p.id, p.manufacturer, p.model_name, p.product_group_key,
                       p.manufacturer_product_url, p.last_verified_at
                FROM {$this->products} p
                WHERE p.lifecycle_status IN ('ACTIVE','TEMPORARILY_UNAVAILABLE','UNKNOWN')
                  {$where_group}
                  AND NOT EXISTS (
                      SELECT 1
                      FROM {$this->identifiers} i
                      WHERE i.subject_type = %s
                        AND i.subject_id = p.id
                        AND i.identifier_type IN (%s,%s,%s)
                        AND i.source_type IN (%s,%s)
                        AND i.source_url IS NOT NULL
                        AND i.source_url <> ''
                        AND i.verified_at IS NOT NULL
                  )
                ORDER BY p.product_group_key ASC, p.id ASC
                LIMIT %d";

        // Keep placeholder order deterministic when an optional group filter is
        // present: group belongs before the subquery arguments.
        if ( '' !== $group ) {
            $args = array(
                $group,
                UPK_Repository::SUBJECT_PRODUCT,
                'GTIN',
                'EAN',
                'MPN',
                'MANUFACTURER',
                'OFFICIAL_DOCUMENTATION',
                $limit,
            );
        }

        $rows = $this->wpdb->get_results(
            $this->wpdb->prepare( $sql, ...$args ),
            ARRAY_A
        );

        $out = array();
        foreach ( is_array( $rows ) ? $rows : array() as $row ) {
            $product_id = absint( $row['id'] ?? 0 );
            $manufacturer = sanitize_text_field( $row['manufacturer'] ?? '' );
            $model_name = sanitize_text_field( $row['model_name'] ?? '' );
            $group_key = sanitize_key( $row['product_group_key'] ?? '' );
            $source_url = esc_url_raw( $row['manufacturer_product_url'] ?? '' );

            if ( 0 === $product_id || '' === $manufacturer || '' === $model_name || '' === $group_key || '' === $source_url ) {
                return new WP_Error( 'UPC_IDENTIFIER_COVERAGE_PRODUCT_INVALID', 'Identifier coverage row contains incomplete product identity.' );
            }

            $out[] = array(
                'product_id' => $product_id,
                'manufacturer' => $manufacturer,
                'model_name' => $model_name,
                'product_group_key' => $group_key,
                'manufacturer_product_url' => $source_url,
                'requested_identifier_types' => array( 'GTIN', 'EAN', 'MPN' ),
            );
        }

        return array(
            'status' => 'AFFILIATE_IDENTIFIER_RESEARCH_REQUIRED',
            'count' => count( $out ),
            'products' => $out,
            'persisted' => false,
        );
    }
}
