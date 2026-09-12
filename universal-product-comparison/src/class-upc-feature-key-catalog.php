<?php

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

/**
 * Canonical, fail-closed mapping from researched feature labels to fact keys.
 * Unknown labels never create new keys implicitly.
 */
class UPC_Feature_Key_Catalog {
    private $meta;
    private $by_label;

    private function __construct( array $meta, array $by_label ) {
        $this->meta = $meta;
        $this->by_label = $by_label;
    }

    public static function load( $path ) {
        if ( ! is_file( $path ) ) {
            return new WP_Error( 'UPC_FEATURE_CATALOG_MISSING', 'Feature key catalog is missing.' );
        }

        $data = json_decode( file_get_contents( $path ), true );
        if ( ! is_array( $data )
            || '1' !== (string) ( $data['schema_version'] ?? '' )
            || empty( $data['project_key'] )
            || empty( $data['features'] )
            || ! is_array( $data['features'] )
        ) {
            return new WP_Error( 'UPC_FEATURE_CATALOG_INVALID', 'Feature key catalog is invalid.' );
        }

        $by_label = array();
        $used_keys = array();

        foreach ( $data['features'] as $row ) {
            if ( ! is_array( $row ) ) {
                return new WP_Error( 'UPC_FEATURE_CATALOG_ROW_INVALID', 'Feature catalog row is invalid.' );
            }

            $label = trim( (string) ( $row['label'] ?? '' ) );
            $key = trim( (string) ( $row['fact_key'] ?? '' ) );

            if ( '' === $label || '' === $key || strlen( $key ) > 191 || ! preg_match( '/^[a-z0-9_]+$/', $key ) ) {
                return new WP_Error( 'UPC_FEATURE_CATALOG_ROW_INVALID', 'Feature catalog label or key is invalid.' );
            }
            if ( isset( $by_label[ $label ] ) ) {
                return new WP_Error( 'UPC_FEATURE_LABEL_DUPLICATE', 'Feature label occurs more than once.' );
            }
            if ( isset( $used_keys[ $key ] ) ) {
                return new WP_Error( 'UPC_FEATURE_KEY_DUPLICATE', 'Feature key occurs more than once.' );
            }

            $by_label[ $label ] = $key;
            $used_keys[ $key ] = true;
        }

        if ( (int) ( $data['feature_count'] ?? -1 ) !== count( $by_label ) ) {
            return new WP_Error( 'UPC_FEATURE_CATALOG_COUNT_MISMATCH', 'Feature catalog count does not match contents.' );
        }

        return new self( $data, $by_label );
    }

    public function resolve( $label ) {
        $label = trim( (string) $label );
        if ( '' === $label ) {
            return new WP_Error( 'UPC_FEATURE_LABEL_MISSING', 'Feature label is required.' );
        }
        if ( ! isset( $this->by_label[ $label ] ) ) {
            return new WP_Error( 'UPC_FEATURE_LABEL_UNKNOWN', 'Feature label is not bound in the canonical catalog.' );
        }
        return $this->by_label[ $label ];
    }

    public function count() {
        return count( $this->by_label );
    }

    public function metadata() {
        return $this->meta;
    }
}
