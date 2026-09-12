<?php

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

/**
 * Read-only impact lookup for product/variant maintenance.
 *
 * No queue table and no scheduler. The caller can immediately re-evaluate only
 * the comparisons that reference the changed product or one of its variants.
 */
class UPC_Maintenance {
    private $wpdb;
    private $products;
    private $variants;
    private $items;
    private $comparisons;

    public function __construct( $wpdb ) {
        $this->wpdb        = $wpdb;
        $this->products    = $wpdb->prefix . 'upk_products';
        $this->variants    = $wpdb->prefix . 'upk_variants';
        $this->items       = $wpdb->prefix . 'upc_items';
        $this->comparisons = $wpdb->prefix . 'upc_comparisons';
    }

    public function affected_comparisons_for_product( $product_id ) {
        $product_id = absint( $product_id );
        if ( ! $this->product_exists( $product_id ) ) {
            return new WP_Error( 'UPC_PRODUCT_NOT_FOUND', 'Product does not exist.' );
        }

        $ids = $this->wpdb->get_col(
            $this->wpdb->prepare(
                "SELECT DISTINCT i.comparison_id
                 FROM {$this->items} i
                 LEFT JOIN {$this->variants} v
                   ON i.subject_type = %s AND i.subject_id = v.id
                 WHERE (i.subject_type = %s AND i.subject_id = %d)
                    OR (i.subject_type = %s AND v.product_id = %d)
                 ORDER BY i.comparison_id ASC",
                UPK_Repository::SUBJECT_VARIANT,
                UPK_Repository::SUBJECT_PRODUCT,
                $product_id,
                UPK_Repository::SUBJECT_VARIANT,
                $product_id
            )
        );

        return $this->normalize_ids( $ids );
    }

    public function affected_comparisons_for_variant( $variant_id ) {
        $variant_id = absint( $variant_id );
        if ( ! $this->variant_exists( $variant_id ) ) {
            return new WP_Error( 'UPC_VARIANT_NOT_FOUND', 'Variant does not exist.' );
        }

        $ids = $this->wpdb->get_col(
            $this->wpdb->prepare(
                "SELECT DISTINCT comparison_id
                 FROM {$this->items}
                 WHERE subject_type = %s AND subject_id = %d
                 ORDER BY comparison_id ASC",
                UPK_Repository::SUBJECT_VARIANT,
                $variant_id
            )
        );

        return $this->normalize_ids( $ids );
    }

    public function reevaluation_scope_for_new_product( $product_id ) {
        $product_id = absint( $product_id );
        if ( ! $this->product_exists( $product_id ) ) {
            return new WP_Error( 'UPC_PRODUCT_NOT_FOUND', 'Product does not exist.' );
        }

        $group_key = (string) $this->wpdb->get_var(
            $this->wpdb->prepare(
                "SELECT product_group_key FROM {$this->products} WHERE id = %d LIMIT 1",
                $product_id
            )
        );
        $group_key = sanitize_key( $group_key );
        if ( '' === $group_key ) {
            return new WP_Error( 'UPC_PRODUCT_GROUP_MISSING', 'Product group is missing.' );
        }

        $peer_ids = $this->wpdb->get_col(
            $this->wpdb->prepare(
                "SELECT id FROM {$this->products}
                 WHERE product_group_key = %s
                   AND id <> %d
                   AND lifecycle_status IN ('ACTIVE','TEMPORARILY_UNAVAILABLE','UNKNOWN')
                 ORDER BY id ASC",
                $group_key,
                $product_id
            )
        );

        $comparison_ids = $this->wpdb->get_col(
            $this->wpdb->prepare(
                "SELECT id FROM {$this->comparisons}
                 WHERE product_group_key = %s
                 ORDER BY id ASC",
                $group_key
            )
        );

        return array(
            'product_id' => $product_id,
            'product_group_key' => $group_key,
            'peer_product_ids' => $this->normalize_ids( $peer_ids ),
            'existing_comparison_ids' => $this->normalize_ids( $comparison_ids ),
            'automatic_comparison_created' => false,
        );
    }

    private function normalize_ids( $ids ) {
        $ids = array_values( array_unique( array_map( 'intval', is_array( $ids ) ? $ids : array() ) ) );
        sort( $ids, SORT_NUMERIC );
        return $ids;
    }

    private function product_exists( $product_id ) {
        return (bool) $this->wpdb->get_var(
            $this->wpdb->prepare( "SELECT id FROM {$this->products} WHERE id = %d LIMIT 1", absint( $product_id ) )
        );
    }

    private function variant_exists( $variant_id ) {
        return (bool) $this->wpdb->get_var(
            $this->wpdb->prepare( "SELECT id FROM {$this->variants} WHERE id = %d LIMIT 1", absint( $variant_id ) )
        );
    }
}
