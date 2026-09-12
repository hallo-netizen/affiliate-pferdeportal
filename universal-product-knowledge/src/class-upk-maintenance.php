<?php

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

/**
 * Minimal maintenance operations for existing product knowledge.
 *
 * No scheduler, no research provider and no new storage. This class only
 * updates already identified subjects and selects products due for review.
 */
class UPK_Maintenance {
    private $wpdb;
    private $products;
    private $variants;

    public function __construct( $wpdb ) {
        $this->wpdb     = $wpdb;
        $this->products = $wpdb->prefix . 'upk_products';
        $this->variants = $wpdb->prefix . 'upk_variants';
    }

    public function update_product( $product_id, array $data = array() ) {
        $product_id = absint( $product_id );
        if ( ! $this->product_exists( $product_id ) ) {
            return new WP_Error( 'UPK_PRODUCT_NOT_FOUND', 'Product does not exist.' );
        }

        $payload = array();
        $formats = array();

        if ( array_key_exists( 'lifecycle_status', $data ) ) {
            $status = strtoupper( sanitize_text_field( $data['lifecycle_status'] ) );
            if ( ! in_array( $status, UPK_Repository::lifecycle_statuses(), true ) ) {
                return new WP_Error( 'UPK_INVALID_LIFECYCLE_STATUS', 'Invalid lifecycle status.' );
            }
            $payload['lifecycle_status'] = $status;
            $formats[] = '%s';
        }

        if ( array_key_exists( 'manufacturer_product_url', $data ) ) {
            $url = esc_url_raw( $data['manufacturer_product_url'] );
            if ( '' === $url ) {
                return new WP_Error( 'UPK_PRODUCT_SOURCE_URL_INVALID', 'Manufacturer product URL is invalid.' );
            }
            $payload['manufacturer_product_url'] = $url;
            $formats[] = '%s';
        }

        if ( array_key_exists( 'successor_product_id', $data ) ) {
            $raw_successor = $data['successor_product_id'];
            if ( null === $raw_successor || '' === $raw_successor ) {
                $payload['successor_product_id'] = null;
                $formats[] = '%d';
            } else {
                $successor_id = absint( $raw_successor );
                if ( 0 === $successor_id || $successor_id === $product_id ) {
                    return new WP_Error( 'UPK_SUCCESSOR_PRODUCT_INVALID', 'Successor product must be a different existing product.' );
                }
                if ( ! $this->product_exists( $successor_id ) ) {
                    return new WP_Error( 'UPK_SUCCESSOR_PRODUCT_NOT_FOUND', 'Successor product does not exist.' );
                }
                $payload['successor_product_id'] = $successor_id;
                $formats[] = '%d';
            }
        }

        $now = current_time( 'mysql', true );
        $verified = $this->normalize_datetime(
            array_key_exists( 'last_verified_at', $data ) ? $data['last_verified_at'] : $now
        );
        if ( is_wp_error( $verified ) ) {
            return $verified;
        }

        $payload['last_verified_at'] = $verified;
        $formats[] = '%s';
        $payload['updated_at'] = $now;
        $formats[] = '%s';

        $updated = $this->wpdb->update(
            $this->products,
            $payload,
            array( 'id' => $product_id ),
            $formats,
            array( '%d' )
        );

        if ( false === $updated ) {
            return new WP_Error( 'UPK_PRODUCT_UPDATE_FAILED', $this->wpdb->last_error ? $this->wpdb->last_error : 'Product update failed.' );
        }

        return $product_id;
    }

    public function update_variant( $variant_id, array $data = array() ) {
        $variant_id = absint( $variant_id );
        if ( ! $this->variant_exists( $variant_id ) ) {
            return new WP_Error( 'UPK_VARIANT_NOT_FOUND', 'Variant does not exist.' );
        }

        $payload = array();
        $formats = array();

        if ( array_key_exists( 'lifecycle_status', $data ) ) {
            $status = strtoupper( sanitize_text_field( $data['lifecycle_status'] ) );
            if ( ! in_array( $status, UPK_Repository::lifecycle_statuses(), true ) ) {
                return new WP_Error( 'UPK_INVALID_LIFECYCLE_STATUS', 'Invalid lifecycle status.' );
            }
            $payload['lifecycle_status'] = $status;
            $formats[] = '%s';
        }

        $now = current_time( 'mysql', true );
        $verified = $this->normalize_datetime(
            array_key_exists( 'last_verified_at', $data ) ? $data['last_verified_at'] : $now
        );
        if ( is_wp_error( $verified ) ) {
            return $verified;
        }

        $payload['last_verified_at'] = $verified;
        $formats[] = '%s';
        $payload['updated_at'] = $now;
        $formats[] = '%s';

        $updated = $this->wpdb->update(
            $this->variants,
            $payload,
            array( 'id' => $variant_id ),
            $formats,
            array( '%d' )
        );

        if ( false === $updated ) {
            return new WP_Error( 'UPK_VARIANT_UPDATE_FAILED', $this->wpdb->last_error ? $this->wpdb->last_error : 'Variant update failed.' );
        }

        return $variant_id;
    }

    public function find_product_id_by_identity( array $data ) {
        $manufacturer = isset( $data['manufacturer'] ) ? sanitize_text_field( $data['manufacturer'] ) : '';
        $model_name   = isset( $data['model_name'] ) ? sanitize_text_field( $data['model_name'] ) : '';
        $group_key    = isset( $data['product_group_key'] ) ? sanitize_key( $data['product_group_key'] ) : '';
        $generation   = isset( $data['generation'] ) ? sanitize_text_field( $data['generation'] ) : '';

        if ( '' === $manufacturer || '' === $model_name || '' === $group_key ) {
            return new WP_Error( 'UPK_PRODUCT_IDENTITY_INCOMPLETE', 'Product identity is incomplete.' );
        }

        $ids = $this->wpdb->get_col(
            $this->wpdb->prepare(
                "SELECT id FROM {$this->products}
                 WHERE manufacturer = %s
                   AND model_name = %s
                   AND product_group_key = %s
                   AND generation = %s
                 ORDER BY id ASC
                 LIMIT 2",
                $manufacturer,
                $model_name,
                $group_key,
                $generation
            )
        );

        $ids = array_values( array_map( 'intval', is_array( $ids ) ? $ids : array() ) );
        if ( count( $ids ) > 1 ) {
            return new WP_Error( 'UPK_DUPLICATE_PRODUCT_IDENTITY', 'More than one product matches the exact product identity.' );
        }

        return empty( $ids ) ? 0 : (int) $ids[0];
    }

    public function products_due_for_review( $verified_before, $limit = 100 ) {
        return $this->select_due_products( '', $verified_before, $limit );
    }

    public function products_due_for_group_review( $product_group_key, $verified_before, $limit = 100 ) {
        $product_group_key = sanitize_key( $product_group_key );
        if ( '' === $product_group_key ) {
            return new WP_Error( 'UPK_PRODUCT_GROUP_KEY_MISSING', 'Product group key is required.' );
        }

        return $this->select_due_products( $product_group_key, $verified_before, $limit );
    }

    private function select_due_products( $product_group_key, $verified_before, $limit ) {
        $cutoff = $this->normalize_datetime( $verified_before );
        if ( is_wp_error( $cutoff ) ) {
            return $cutoff;
        }

        $limit = max( 1, min( 500, absint( $limit ) ) );

        if ( '' !== $product_group_key ) {
            $ids = $this->wpdb->get_col(
                $this->wpdb->prepare(
                    "SELECT id FROM {$this->products}
                     WHERE product_group_key = %s
                       AND last_verified_at <= %s
                       AND lifecycle_status IN ('ACTIVE','TEMPORARILY_UNAVAILABLE','UNKNOWN')
                     ORDER BY last_verified_at ASC, id ASC
                     LIMIT %d",
                    $product_group_key,
                    $cutoff,
                    $limit
                )
            );
        } else {
            $ids = $this->wpdb->get_col(
                $this->wpdb->prepare(
                    "SELECT id FROM {$this->products}
                     WHERE last_verified_at <= %s
                       AND lifecycle_status IN ('ACTIVE','TEMPORARILY_UNAVAILABLE','UNKNOWN')
                     ORDER BY last_verified_at ASC, id ASC
                     LIMIT %d",
                    $cutoff,
                    $limit
                )
            );
        }

        return array_values( array_map( 'intval', is_array( $ids ) ? $ids : array() ) );
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

    private function normalize_datetime( $value ) {
        $timestamp = strtotime( (string) $value );
        if ( false === $timestamp ) {
            return new WP_Error( 'UPK_INVALID_DATETIME', 'Invalid verification timestamp.' );
        }
        return gmdate( 'Y-m-d H:i:s', $timestamp );
    }
}
