<?php

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

class UPC_Bound_Dossier_Importer {
    const SCHEMA_VERSION = '1';

    private $repository;
    private $knowledge;
    private $wpdb;

    public function __construct( $repository, $knowledge, $wpdb ) {
        $this->repository = $repository;
        $this->knowledge  = $knowledge;
        $this->wpdb       = $wpdb;
    }

    public function import( $project_key, $dossier_id ) {
        $loaded = $this->load_bound( $project_key, $dossier_id );
        if ( is_wp_error( $loaded ) ) {
            return $loaded;
        }

        $dossier = $loaded['dossier'];
        $key     = sanitize_key( strtolower( (string) $dossier['dossier_id'] ) );

        $existing_id = $this->repository->find_comparison_id_by_key( $key );
        if ( $existing_id > 0 ) {
            $verified = $this->verify_existing( $existing_id, $dossier );
            if ( is_wp_error( $verified ) ) {
                return $verified;
            }

            return array(
                'status'        => 'BOUND_DOSSIER_REUSED',
                'comparison_id' => $existing_id,
                'dossier_sha256'=> $loaded['sha256'],
            );
        }

        $identity_check = $this->assert_no_unbound_product_identity( $dossier );
        if ( is_wp_error( $identity_check ) ) {
            return $identity_check;
        }

        $this->wpdb->query( 'START TRANSACTION' );

        $product_ids = array();

        foreach ( $dossier['products'] as $product ) {
            $product_id = $this->knowledge->create_product(
                array(
                    'manufacturer'             => $product['manufacturer'],
                    'model_name'               => $product['model_name'],
                    'product_group_key'        => $product['product_group_key'],
                    'manufacturer_product_url' => $product['manufacturer_product_url'],
                    'lifecycle_status'         => $product['lifecycle_status'],
                    'last_verified_at'         => $product['last_verified_at'],
                )
            );

            if ( is_wp_error( $product_id ) ) {
                $this->wpdb->query( 'ROLLBACK' );
                return $product_id;
            }

            foreach ( $product['facts'] as $fact ) {
                $fact_id = $this->knowledge->add_fact(
                    UPK_Repository::SUBJECT_PRODUCT,
                    $product_id,
                    array(
                        'fact_key'    => $fact['fact_key'],
                        'fact_value'  => $fact['fact_value'],
                        'source_url'  => $fact['source_url'],
                        'source_type' => $fact['source_type'],
                        'verified_at' => $fact['verified_at'],
                        'fact_status' => $fact['fact_status'],
                    )
                );

                if ( is_wp_error( $fact_id ) ) {
                    $this->wpdb->query( 'ROLLBACK' );
                    return $fact_id;
                }
            }

            $product_ids[] = (int) $product_id;
        }

        $comparison_id = $this->repository->create_comparison(
            array(
                'comparison_key'     => $key,
                'comparison_type'    => $dossier['comparison_type'],
                'subject_ids'        => $product_ids,
                'working_title'      => $dossier['working_title'],
                'decision_intent'    => isset( $dossier['decision_intent'] ) ? $dossier['decision_intent'] : '',
                'comparability_note' => $dossier['comparability_note'],
            )
        );

        if ( is_wp_error( $comparison_id ) ) {
            $this->wpdb->query( 'ROLLBACK' );
            return $comparison_id;
        }

        $feature_count = $this->repository->set_features( $comparison_id, $dossier['features'], false );
        if ( is_wp_error( $feature_count ) ) {
            $this->wpdb->query( 'ROLLBACK' );
            return $feature_count;
        }

        $valid = $this->repository->validate_required_facts( $comparison_id );
        if ( is_wp_error( $valid ) ) {
            $this->wpdb->query( 'ROLLBACK' );
            return $valid;
        }

        $verified = $this->verify_existing( $comparison_id, $dossier );
        if ( is_wp_error( $verified ) ) {
            $this->wpdb->query( 'ROLLBACK' );
            return $verified;
        }

        $this->wpdb->query( 'COMMIT' );

        return array(
            'status'        => 'BOUND_DOSSIER_IMPORTED',
            'comparison_id' => (int) $comparison_id,
            'product_ids'   => $product_ids,
            'dossier_sha256'=> $loaded['sha256'],
        );
    }

    private function load_bound( $project_key, $dossier_id ) {
        $project_key = sanitize_key( $project_key );
        $dossier_id  = sanitize_key( $dossier_id );

        if ( '' === $project_key || '' === $dossier_id ) {
            return new WP_Error( 'UPC_BOUND_DOSSIER_IDENTITY_MISSING', 'Project and dossier identity are required.' );
        }

        $base          = dirname( __DIR__ ) . '/config/' . $project_key . '/dossiers';
        $manifest_path = $base . '/manifest.json';

        if ( ! is_file( $manifest_path ) ) {
            return new WP_Error( 'UPC_BOUND_DOSSIER_MANIFEST_MISSING', 'Bound dossier manifest is missing.' );
        }

        $manifest = json_decode( file_get_contents( $manifest_path ), true );
        if ( ! is_array( $manifest )
            || self::SCHEMA_VERSION !== (string) ( $manifest['schema_version'] ?? '' )
            || $project_key !== (string) ( $manifest['project_key'] ?? '' )
            || empty( $manifest['dossiers'][ $dossier_id ]['file'] )
            || empty( $manifest['dossiers'][ $dossier_id ]['sha256'] )
        ) {
            return new WP_Error( 'UPC_BOUND_DOSSIER_NOT_BOUND', 'Dossier is not bound for this project.' );
        }

        $binding = $manifest['dossiers'][ $dossier_id ];
        $path    = $base . '/' . basename( $binding['file'] );

        if ( ! is_file( $path ) ) {
            return new WP_Error( 'UPC_BOUND_DOSSIER_FILE_MISSING', 'Bound dossier file is missing.' );
        }

        $actual = hash_file( 'sha256', $path );
        if ( ! hash_equals( strtolower( (string) $binding['sha256'] ), strtolower( $actual ) ) ) {
            return new WP_Error( 'UPC_BOUND_DOSSIER_HASH_MISMATCH', 'Bound dossier hash does not match manifest.' );
        }

        $dossier = json_decode( file_get_contents( $path ), true );
        if ( ! is_array( $dossier ) ) {
            return new WP_Error( 'UPC_BOUND_DOSSIER_JSON_INVALID', 'Bound dossier JSON is invalid.' );
        }

        $required = array( 'dossier_id', 'working_title', 'comparison_type', 'product_group_key', 'comparability_note', 'features', 'products' );
        foreach ( $required as $field ) {
            if ( ! array_key_exists( $field, $dossier ) ) {
                return new WP_Error( 'UPC_BOUND_DOSSIER_INCOMPLETE', 'Bound dossier is incomplete.', array( 'field' => $field ) );
            }
        }

        if ( sanitize_key( strtolower( (string) $dossier['dossier_id'] ) ) !== $dossier_id
            || count( $dossier['products'] ) < 2
            || count( $dossier['products'] ) > 4
            || empty( $dossier['features'] )
        ) {
            return new WP_Error( 'UPC_BOUND_DOSSIER_CONTRACT_INVALID', 'Bound dossier violates the import contract.' );
        }

        return array(
            'dossier' => $dossier,
            'sha256'  => $actual,
        );
    }

    private function assert_no_unbound_product_identity( array $dossier ) {
        $table = $this->wpdb->prefix . 'upk_products';

        foreach ( $dossier['products'] as $product ) {
            $count = (int) $this->wpdb->get_var(
                $this->wpdb->prepare(
                    "SELECT COUNT(*) FROM {$table} WHERE manufacturer = %s AND model_name = %s AND product_group_key = %s",
                    $product['manufacturer'],
                    $product['model_name'],
                    sanitize_key( $product['product_group_key'] )
                )
            );

            if ( $count > 0 ) {
                return new WP_Error(
                    'UPC_BOUND_DOSSIER_PRODUCT_ALREADY_EXISTS_UNBOUND',
                    'A bound dossier product already exists without the bound comparison. Import is blocked.'
                );
            }
        }

        return true;
    }

    private function verify_existing( $comparison_id, array $dossier ) {
        $bundle = $this->repository->get_comparison_bundle( $comparison_id );
        if ( is_wp_error( $bundle ) ) {
            return $bundle;
        }

        if ( sanitize_key( $bundle['comparison_key'] ) !== sanitize_key( strtolower( $dossier['dossier_id'] ) )
            || strtoupper( (string) $bundle['comparison_type'] ) !== strtoupper( (string) $dossier['comparison_type'] )
            || (string) $bundle['product_group_key'] !== sanitize_key( $dossier['product_group_key'] )
            || (string) $bundle['working_title'] !== (string) $dossier['working_title']
            || count( $bundle['items'] ) !== count( $dossier['products'] )
            || count( $bundle['features'] ) !== count( $dossier['features'] )
        ) {
            return new WP_Error( 'UPC_BOUND_DOSSIER_EXISTING_MISMATCH', 'Existing comparison does not match the bound dossier.' );
        }

        foreach ( array_values( $dossier['features'] ) as $index => $feature ) {
            $actual = $bundle['features'][ $index ];
            if ( (string) $actual['fact_key'] !== sanitize_key( $feature['fact_key'] )
                || (string) $actual['label'] !== (string) $feature['label']
            ) {
                return new WP_Error( 'UPC_BOUND_DOSSIER_FEATURE_MISMATCH', 'Existing comparison features differ from the bound dossier.' );
            }
        }

        foreach ( array_values( $dossier['products'] ) as $index => $expected ) {
            $knowledge = $bundle['items'][ $index ]['knowledge'];

            if ( (string) $knowledge['manufacturer'] !== (string) $expected['manufacturer']
                || (string) $knowledge['model_name'] !== (string) $expected['model_name']
                || (string) $knowledge['product_group_key'] !== sanitize_key( $expected['product_group_key'] )
            ) {
                return new WP_Error( 'UPC_BOUND_DOSSIER_PRODUCT_MISMATCH', 'Existing product identity differs from the bound dossier.' );
            }

            $actual_facts = array();
            foreach ( (array) $knowledge['facts'] as $fact ) {
                $actual_facts[ $fact['fact_key'] ][] = $fact;
            }

            foreach ( $expected['facts'] as $fact ) {
                $matches = isset( $actual_facts[ sanitize_key( $fact['fact_key'] ) ] )
                    ? $actual_facts[ sanitize_key( $fact['fact_key'] ) ]
                    : array();

                if ( 1 !== count( $matches ) ) {
                    return new WP_Error( 'UPC_BOUND_DOSSIER_FACT_COUNT_MISMATCH', 'Existing fact count differs from the bound dossier.' );
                }

                $actual = $matches[0];
                if ( (string) $actual['fact_value'] !== (string) $fact['fact_value']
                    || (string) $actual['fact_status'] !== (string) $fact['fact_status']
                    || (string) $actual['source_url'] !== (string) $fact['source_url']
                    || (string) $actual['source_type'] !== (string) $fact['source_type']
                ) {
                    return new WP_Error( 'UPC_BOUND_DOSSIER_FACT_MISMATCH', 'Existing fact differs from the bound dossier.' );
                }
            }
        }

        return true;
    }
}
