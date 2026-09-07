<?php

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

class UPC_Repository {
    const TYPE_PRODUCT = 'PRODUCT';
    const TYPE_VARIANT = 'VARIANT';

    private $wpdb;
    private $knowledge;
    private $comparisons;
    private $items;

    public function __construct( $wpdb, $knowledge ) {
        $this->wpdb        = $wpdb;
        $this->knowledge   = $knowledge;
        $this->comparisons = $wpdb->prefix . 'upc_comparisons';
        $this->items       = $wpdb->prefix . 'upc_items';
    }

    public function create_comparison( array $data ) {
        $type = isset( $data['comparison_type'] ) ? strtoupper( sanitize_text_field( $data['comparison_type'] ) ) : '';
        $key  = isset( $data['comparison_key'] ) ? sanitize_key( $data['comparison_key'] ) : '';
        $ids  = isset( $data['subject_ids'] ) && is_array( $data['subject_ids'] ) ? array_values( array_map( 'absint', $data['subject_ids'] ) ) : array();

        if ( ! in_array( $type, array( self::TYPE_PRODUCT, self::TYPE_VARIANT ), true ) ) {
            return new WP_Error( 'UPC_INVALID_COMPARISON_TYPE', 'Comparison type is invalid.' );
        }

        if ( '' === $key ) {
            return new WP_Error( 'UPC_COMPARISON_KEY_MISSING', 'Comparison key is required.' );
        }

        if ( count( $ids ) < 2 || count( $ids ) > 4 ) {
            return new WP_Error( 'UPC_INVALID_ITEM_COUNT', 'A comparison requires two to four items.' );
        }

        if ( count( array_unique( $ids ) ) !== count( $ids ) || in_array( 0, $ids, true ) ) {
            return new WP_Error( 'UPC_DUPLICATE_OR_INVALID_ITEM', 'Comparison items must be unique valid IDs.' );
        }

        $validated = self::TYPE_PRODUCT === $type
            ? $this->validate_products( $ids )
            : $this->validate_variants( $ids );

        if ( is_wp_error( $validated ) ) {
            return $validated;
        }

        $canonical = $ids;
        sort( $canonical, SORT_NUMERIC );
        $set_hash = hash( 'sha256', $type . ':' . implode( ',', $canonical ) );

        $existing = $this->wpdb->get_var(
            $this->wpdb->prepare( "SELECT id FROM {$this->comparisons} WHERE set_hash = %s LIMIT 1", $set_hash )
        );
        if ( $existing ) {
            return new WP_Error( 'UPC_DUPLICATE_COMPARISON', 'The same comparison already exists regardless of item order.' );
        }

        $now = current_time( 'mysql', true );
        $inserted = $this->wpdb->insert(
            $this->comparisons,
            array(
                'comparison_key'    => $key,
                'comparison_type'   => $type,
                'product_group_key' => $validated['product_group_key'],
                'decision_intent'   => isset( $data['decision_intent'] ) ? sanitize_textarea_field( $data['decision_intent'] ) : '',
                'set_hash'          => $set_hash,
                'created_at'        => $now,
                'updated_at'        => $now,
            ),
            array( '%s', '%s', '%s', '%s', '%s', '%s', '%s' )
        );

        if ( false === $inserted ) {
            return new WP_Error( 'UPC_COMPARISON_INSERT_FAILED', $this->wpdb->last_error ? $this->wpdb->last_error : 'Comparison insert failed.' );
        }

        $comparison_id = (int) $this->wpdb->insert_id;
        $subject_type  = self::TYPE_PRODUCT === $type ? UPK_Repository::SUBJECT_PRODUCT : UPK_Repository::SUBJECT_VARIANT;

        foreach ( $ids as $index => $subject_id ) {
            $ok = $this->wpdb->insert(
                $this->items,
                array(
                    'comparison_id' => $comparison_id,
                    'subject_type'  => $subject_type,
                    'subject_id'    => $subject_id,
                    'position'      => $index + 1,
                    'created_at'    => $now,
                ),
                array( '%d', '%s', '%d', '%d', '%s' )
            );

            if ( false === $ok ) {
                $this->wpdb->delete( $this->items, array( 'comparison_id' => $comparison_id ), array( '%d' ) );
                $this->wpdb->delete( $this->comparisons, array( 'id' => $comparison_id ), array( '%d' ) );
                return new WP_Error( 'UPC_ITEM_INSERT_FAILED', $this->wpdb->last_error ? $this->wpdb->last_error : 'Comparison item insert failed.' );
            }
        }

        return $comparison_id;
    }

    public function get_comparison_bundle( $comparison_id ) {
        $comparison_id = absint( $comparison_id );
        $comparison = $this->wpdb->get_row(
            $this->wpdb->prepare( "SELECT * FROM {$this->comparisons} WHERE id = %d", $comparison_id ),
            ARRAY_A
        );

        if ( ! $comparison ) {
            return new WP_Error( 'UPC_COMPARISON_NOT_FOUND', 'Comparison does not exist.' );
        }

        $items = $this->wpdb->get_results(
            $this->wpdb->prepare(
                "SELECT subject_type, subject_id, position FROM {$this->items} WHERE comparison_id = %d ORDER BY position ASC",
                $comparison_id
            ),
            ARRAY_A
        );

        $resolved = array();
        foreach ( $items as $item ) {
            if ( UPK_Repository::SUBJECT_PRODUCT === $item['subject_type'] ) {
                $bundle = $this->knowledge->get_product_bundle( (int) $item['subject_id'] );
            } else {
                $bundle = $this->knowledge->get_variant_bundle( (int) $item['subject_id'] );
            }

            if ( is_wp_error( $bundle ) ) {
                return new WP_Error( 'UPC_KNOWLEDGE_REFERENCE_BROKEN', 'A referenced product or variant no longer resolves.' );
            }

            $resolved[] = array(
                'position'     => (int) $item['position'],
                'subject_type' => $item['subject_type'],
                'subject_id'   => (int) $item['subject_id'],
                'knowledge'    => $bundle,
            );
        }

        $comparison['comparison_uid'] = 'UPC-' . str_pad( (string) $comparison_id, 6, '0', STR_PAD_LEFT );
        $comparison['items'] = $resolved;

        return $comparison;
    }

    private function validate_products( array $ids ) {
        $manufacturers = array();
        $group_key = null;

        foreach ( $ids as $id ) {
            $product = $this->knowledge->get_product_bundle( $id );
            if ( is_wp_error( $product ) ) {
                return new WP_Error( 'UPC_PRODUCT_NOT_FOUND', 'A comparison product does not exist.' );
            }

            if ( null === $group_key ) {
                $group_key = $product['product_group_key'];
            } elseif ( $group_key !== $product['product_group_key'] ) {
                return new WP_Error( 'UPC_PRODUCT_GROUP_MISMATCH', 'Product comparisons require the same product group.' );
            }

            $manufacturers[] = mb_strtolower( trim( $product['manufacturer'] ) );
        }

        if ( count( array_unique( $manufacturers ) ) < 2 ) {
            return new WP_Error( 'UPC_MIN_TWO_MANUFACTURERS', 'Product comparisons require at least two manufacturers.' );
        }

        return array( 'product_group_key' => $group_key );
    }

    private function validate_variants( array $ids ) {
        $product_id = null;
        $group_key  = null;

        foreach ( $ids as $id ) {
            $variant = $this->knowledge->get_variant_bundle( $id );
            if ( is_wp_error( $variant ) ) {
                return new WP_Error( 'UPC_VARIANT_NOT_FOUND', 'A comparison variant does not exist.' );
            }

            if ( null === $product_id ) {
                $product_id = (int) $variant['product_id'];
                $group_key  = $variant['product']['product_group_key'];
            } elseif ( $product_id !== (int) $variant['product_id'] ) {
                return new WP_Error( 'UPC_VARIANT_PARENT_MISMATCH', 'Variant comparisons require the same base product.' );
            }
        }

        return array( 'product_group_key' => $group_key );
    }
}
