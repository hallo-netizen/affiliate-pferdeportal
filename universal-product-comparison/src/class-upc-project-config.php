<?php

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

class UPC_Project_Config {
    const SCHEMA_VERSION = '1';

    public static function load_publishing( $project_key ) {
        $project_key = sanitize_key( $project_key );
        if ( '' === $project_key ) {
            return new WP_Error( 'UPC_PROJECT_KEY_MISSING', 'Project key is required.' );
        }

        $base = dirname( __DIR__ ) . '/config/' . $project_key;
        $manifest_path = $base . '/project-manifest.json';

        if ( ! is_file( $manifest_path ) ) {
            return new WP_Error( 'UPC_PROJECT_MANIFEST_MISSING', 'Project manifest is missing.' );
        }

        $manifest = json_decode( file_get_contents( $manifest_path ), true );
        if ( ! is_array( $manifest )
            || self::SCHEMA_VERSION !== (string) ( $manifest['schema_version'] ?? '' )
            || $project_key !== (string) ( $manifest['project_key'] ?? '' )
            || empty( $manifest['publishing']['file'] )
            || empty( $manifest['publishing']['sha256'] )
        ) {
            return new WP_Error( 'UPC_PROJECT_MANIFEST_INVALID', 'Project manifest is invalid.' );
        }

        $path = $base . '/' . basename( $manifest['publishing']['file'] );
        if ( ! is_file( $path ) ) {
            return new WP_Error( 'UPC_PUBLISHING_CONFIG_MISSING', 'Publishing config is missing.' );
        }

        $actual = hash_file( 'sha256', $path );
        if ( ! hash_equals( strtolower( (string) $manifest['publishing']['sha256'] ), strtolower( $actual ) ) ) {
            return new WP_Error( 'UPC_PUBLISHING_CONFIG_HASH_MISMATCH', 'Publishing config hash does not match manifest.' );
        }

        $config = json_decode( file_get_contents( $path ), true );
        if ( ! is_array( $config )
            || self::SCHEMA_VERSION !== (string) ( $config['schema_version'] ?? '' )
            || $project_key !== (string) ( $config['project_key'] ?? '' )
            || 'post' !== (string) ( $config['post_type'] ?? '' )
            || empty( $config['category_map'] )
            || ! is_array( $config['category_map'] )
        ) {
            return new WP_Error( 'UPC_PUBLISHING_CONFIG_INVALID', 'Publishing config is invalid.' );
        }

        $config['_binding_sha256'] = $actual;
        return $config;
    }
}
