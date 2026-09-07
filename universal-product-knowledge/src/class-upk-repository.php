<?php

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

class UPK_Repository {
    const SUBJECT_PRODUCT = 'product';
    const SUBJECT_VARIANT = 'variant';

    private $wpdb;
    private $products;
    private $variants;
    private $identifiers;
    private $facts;

    public function __construct( $wpdb ) {
        $this->wpdb        = $wpdb;
        $this->products    = $wpdb->prefix . 'upk_products';
        $this->variants    = $wpdb->prefix . 'upk_variants';
        $this->identifiers = $wpdb->prefix . 'upk_identifiers';
        $this->facts       = $wpdb->prefix . 'upk_facts';
    }

    public static function lifecycle_statuses() {
        return array( 'ACTIVE', 'TEMPORARILY_UNAVAILABLE', 'DISCONTINUED', 'UNKNOWN' );
    }

    public static function identifier_types() {
        return array( 'GTIN', 'EAN', 'MPN', 'MANUFACTURER_ARTICLE_NUMBER' );
    }

    public static function source_types() {
        return array( 'MANUFACTURER', 'OFFICIAL_DOCUMENTATION', 'APPROVED_SECONDARY' );
    }

    public static function fact_statuses() {
        return array( 'VERIFIED', 'NOT_IN_SOURCE', 'SOURCE_CONFLICT', 'CONFIGURATION_DEPENDENT' );
    }

    public function create_product( array $data ) {
        $manufacturer = isset( $data['manufacturer'] ) ? sanitize_text_field( $data['manufacturer'] ) : '';
        $model_name   = isset( $data['model_name'] ) ? sanitize_text_field( $data['model_name'] ) : '';
        $group_key    = isset( $data['product_group_key'] ) ? sanitize_key( $data['product_group_key'] ) : '';
        $source_url   = isset( $data['manufacturer_product_url'] ) ? esc_url_raw( $data['manufacturer_product_url'] ) : '';
        $status       = isset( $data['lifecycle_status'] ) ? strtoupper( sanitize_text_field( $data['lifecycle_status'] ) ) : 'UNKNOWN';

        if ( '' === $manufacturer || '' === $model_name || '' === $group_key || '' === $source_url ) {
            return new WP_Error( 'UPK_PRODUCT_IDENTITY_INCOMPLETE', 'Product identity is incomplete.' );
        }

        if ( ! in_array( $status, self::lifecycle_statuses(), true ) ) {
            return new WP_Error( 'UPK_INVALID_LIFECYCLE_STATUS', 'Invalid lifecycle status.' );
        }

        $now      = current_time( 'mysql', true );
        $verified = $this->normalize_datetime( isset( $data['last_verified_at'] ) ? $data['last_verified_at'] : $now );

        if ( is_wp_error( $verified ) ) {
            return $verified;
        }

        $inserted = $this->wpdb->insert(
            $this->products,
            array(
                'manufacturer'             => $manufacturer,
                'model_name'               => $model_name,
                'model_family'             => isset( $data['model_family'] ) ? sanitize_text_field( $data['model_family'] ) : '',
                'product_group_key'        => $group_key,
                'manufacturer_product_url' => $source_url,
                'generation'               => isset( $data['generation'] ) ? sanitize_text_field( $data['generation'] ) : '',
                'lifecycle_status'         => $status,
                'successor_product_id'      => null,
                'last_verified_at'          => $verified,
                'created_at'                => $now,
                'updated_at'                => $now,
            ),
            array( '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%d', '%s', '%s', '%s' )
        );

        if ( false === $inserted ) {
            return new WP_Error( 'UPK_PRODUCT_INSERT_FAILED', $this->wpdb->last_error ? $this->wpdb->last_error : 'Product insert failed.' );
        }

        return (int) $this->wpdb->insert_id;
    }

    public function create_variant( $product_id, array $data ) {
        $product_id = absint( $product_id );
        if ( ! $this->product_exists( $product_id ) ) {
            return new WP_Error( 'UPK_PRODUCT_NOT_FOUND', 'Parent product does not exist.' );
        }

        $name = isset( $data['variant_name'] ) ? sanitize_text_field( $data['variant_name'] ) : '';
        $key  = isset( $data['variant_key'] ) ? sanitize_key( $data['variant_key'] ) : '';
        $status = isset( $data['lifecycle_status'] ) ? strtoupper( sanitize_text_field( $data['lifecycle_status'] ) ) : 'UNKNOWN';

        if ( '' === $name || '' === $key ) {
            return new WP_Error( 'UPK_VARIANT_IDENTITY_INCOMPLETE', 'Variant identity is incomplete.' );
        }

        if ( ! in_array( $status, self::lifecycle_statuses(), true ) ) {
            return new WP_Error( 'UPK_INVALID_LIFECYCLE_STATUS', 'Invalid lifecycle status.' );
        }

        $now      = current_time( 'mysql', true );
        $verified = $this->normalize_datetime( isset( $data['last_verified_at'] ) ? $data['last_verified_at'] : $now );
        if ( is_wp_error( $verified ) ) {
            return $verified;
        }

        $inserted = $this->wpdb->insert(
            $this->variants,
            array(
                'product_id'       => $product_id,
                'variant_name'     => $name,
                'variant_key'      => $key,
                'lifecycle_status' => $status,
                'last_verified_at' => $verified,
                'created_at'       => $now,
                'updated_at'       => $now,
            ),
            array( '%d', '%s', '%s', '%s', '%s', '%s', '%s' )
        );

        if ( false === $inserted ) {
            return new WP_Error( 'UPK_VARIANT_INSERT_FAILED', $this->wpdb->last_error ? $this->wpdb->last_error : 'Variant insert failed.' );
        }

        return (int) $this->wpdb->insert_id;
    }

    public function add_identifier( $subject_type, $subject_id, $identifier_type, $identifier_value ) {
        $subject_type     = sanitize_key( $subject_type );
        $subject_id       = absint( $subject_id );
        $identifier_type  = strtoupper( sanitize_text_field( $identifier_type ) );
        $identifier_value = trim( sanitize_text_field( $identifier_value ) );

        $valid_subject = $this->validate_subject( $subject_type, $subject_id );
        if ( is_wp_error( $valid_subject ) ) {
            return $valid_subject;
        }

        if ( ! in_array( $identifier_type, self::identifier_types(), true ) || '' === $identifier_value ) {
            return new WP_Error( 'UPK_INVALID_IDENTIFIER', 'Identifier is invalid.' );
        }

        $existing = $this->wpdb->get_row(
            $this->wpdb->prepare(
                "SELECT id, subject_type, subject_id FROM {$this->identifiers} WHERE identifier_type = %s AND identifier_value = %s LIMIT 1",
                $identifier_type,
                $identifier_value
            ),
            ARRAY_A
        );

        if ( $existing ) {
            if ( $existing['subject_type'] === $subject_type && (int) $existing['subject_id'] === $subject_id ) {
                return (int) $existing['id'];
            }
            return new WP_Error( 'UPK_IDENTIFIER_CONFLICT', 'Identifier already belongs to a different product or variant.' );
        }

        $inserted = $this->wpdb->insert(
            $this->identifiers,
            array(
                'subject_type'     => $subject_type,
                'subject_id'       => $subject_id,
                'identifier_type'  => $identifier_type,
                'identifier_value' => $identifier_value,
                'created_at'       => current_time( 'mysql', true ),
            ),
            array( '%s', '%d', '%s', '%s', '%s' )
        );

        if ( false === $inserted ) {
            return new WP_Error( 'UPK_IDENTIFIER_INSERT_FAILED', $this->wpdb->last_error ? $this->wpdb->last_error : 'Identifier insert failed.' );
        }

        return (int) $this->wpdb->insert_id;
    }

    public function add_fact( $subject_type, $subject_id, array $data ) {
        $subject_type = sanitize_key( $subject_type );
        $subject_id   = absint( $subject_id );

        $valid_subject = $this->validate_subject( $subject_type, $subject_id );
        if ( is_wp_error( $valid_subject ) ) {
            return $valid_subject;
        }

        $fact_key    = isset( $data['fact_key'] ) ? sanitize_key( $data['fact_key'] ) : '';
        $fact_value  = isset( $data['fact_value'] ) ? sanitize_textarea_field( $data['fact_value'] ) : '';
        $source_url  = isset( $data['source_url'] ) ? esc_url_raw( $data['source_url'] ) : '';
        $source_type = isset( $data['source_type'] ) ? strtoupper( sanitize_text_field( $data['source_type'] ) ) : '';
        $fact_status = isset( $data['fact_status'] ) ? strtoupper( sanitize_text_field( $data['fact_status'] ) ) : '';

        if ( '' === $fact_key || '' === $source_url || ! in_array( $source_type, self::source_types(), true ) || ! in_array( $fact_status, self::fact_statuses(), true ) ) {
            return new WP_Error( 'UPK_FACT_INCOMPLETE', 'Fact or source binding is incomplete.' );
        }

        if ( 'VERIFIED' === $fact_status && '' === $fact_value ) {
            return new WP_Error( 'UPK_VERIFIED_FACT_EMPTY', 'A verified fact must contain a value.' );
        }

        $now      = current_time( 'mysql', true );
        $verified = $this->normalize_datetime( isset( $data['verified_at'] ) ? $data['verified_at'] : $now );
        if ( is_wp_error( $verified ) ) {
            return $verified;
        }

        $existing_id = (int) $this->wpdb->get_var(
            $this->wpdb->prepare(
                "SELECT id FROM {$this->facts} WHERE subject_type = %s AND subject_id = %d AND fact_key = %s AND source_url = %s LIMIT 1",
                $subject_type,
                $subject_id,
                $fact_key,
                $source_url
            )
        );

        $payload = array(
            'fact_value'  => $fact_value,
            'unit'        => isset( $data['unit'] ) ? sanitize_text_field( $data['unit'] ) : '',
            'source_url'  => $source_url,
            'source_type' => $source_type,
            'verified_at' => $verified,
            'fact_status' => $fact_status,
            'updated_at'  => $now,
        );

        if ( $existing_id ) {
            $updated = $this->wpdb->update(
                $this->facts,
                $payload,
                array( 'id' => $existing_id ),
                array( '%s', '%s', '%s', '%s', '%s', '%s', '%s' ),
                array( '%d' )
            );
            if ( false === $updated ) {
                return new WP_Error( 'UPK_FACT_UPDATE_FAILED', $this->wpdb->last_error ? $this->wpdb->last_error : 'Fact update failed.' );
            }
            return $existing_id;
        }

        $payload['subject_type'] = $subject_type;
        $payload['subject_id']   = $subject_id;
        $payload['fact_key']     = $fact_key;
        $payload['created_at']   = $now;

        $inserted = $this->wpdb->insert(
            $this->facts,
            $payload,
            array( '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%d', '%s', '%s' )
        );

        if ( false === $inserted ) {
            return new WP_Error( 'UPK_FACT_INSERT_FAILED', $this->wpdb->last_error ? $this->wpdb->last_error : 'Fact insert failed.' );
        }

        return (int) $this->wpdb->insert_id;
    }

    public function get_product_bundle( $product_id ) {
        $product_id = absint( $product_id );
        $product = $this->wpdb->get_row(
            $this->wpdb->prepare( "SELECT * FROM {$this->products} WHERE id = %d", $product_id ),
            ARRAY_A
        );

        if ( ! $product ) {
            return new WP_Error( 'UPK_PRODUCT_NOT_FOUND', 'Product does not exist.' );
        }

        $variants = $this->wpdb->get_results(
            $this->wpdb->prepare( "SELECT * FROM {$this->variants} WHERE product_id = %d ORDER BY id ASC", $product_id ),
            ARRAY_A
        );

        $product['identifiers'] = $this->get_subject_identifiers( self::SUBJECT_PRODUCT, $product_id );
        $product['facts']       = $this->get_subject_facts( self::SUBJECT_PRODUCT, $product_id );

        foreach ( $variants as &$variant ) {
            $variant_id = (int) $variant['id'];
            $variant['identifiers'] = $this->get_subject_identifiers( self::SUBJECT_VARIANT, $variant_id );
            $variant['facts']       = $this->get_subject_facts( self::SUBJECT_VARIANT, $variant_id );
        }
        unset( $variant );

        $product['variants'] = $variants;
        return $product;
    }

    private function get_subject_identifiers( $subject_type, $subject_id ) {
        return $this->wpdb->get_results(
            $this->wpdb->prepare(
                "SELECT identifier_type, identifier_value FROM {$this->identifiers} WHERE subject_type = %s AND subject_id = %d ORDER BY identifier_type, id",
                $subject_type,
                $subject_id
            ),
            ARRAY_A
        );
    }

    private function get_subject_facts( $subject_type, $subject_id ) {
        return $this->wpdb->get_results(
            $this->wpdb->prepare(
                "SELECT fact_key, fact_value, unit, source_url, source_type, verified_at, fact_status FROM {$this->facts} WHERE subject_type = %s AND subject_id = %d ORDER BY fact_key, id",
                $subject_type,
                $subject_id
            ),
            ARRAY_A
        );
    }

    private function validate_subject( $subject_type, $subject_id ) {
        if ( self::SUBJECT_PRODUCT === $subject_type && $this->product_exists( $subject_id ) ) {
            return true;
        }
        if ( self::SUBJECT_VARIANT === $subject_type && $this->variant_exists( $subject_id ) ) {
            return true;
        }
        return new WP_Error( 'UPK_SUBJECT_NOT_FOUND', 'Referenced product or variant does not exist.' );
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
