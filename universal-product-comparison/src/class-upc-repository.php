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
    private $features;

    public function __construct( $wpdb, $knowledge ) {
        $this->wpdb        = $wpdb;
        $this->knowledge   = $knowledge;
        $this->comparisons = $wpdb->prefix . 'upc_comparisons';
        $this->items       = $wpdb->prefix . 'upc_items';
        $this->features    = $wpdb->prefix . 'upc_features';
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
                'working_title'     => isset( $data['working_title'] ) ? sanitize_text_field( $data['working_title'] ) : '',
                'decision_intent'   => isset( $data['decision_intent'] ) ? sanitize_textarea_field( $data['decision_intent'] ) : '',
                'comparability_note'=> isset( $data['comparability_note'] ) ? sanitize_textarea_field( $data['comparability_note'] ) : '',
                'set_hash'          => $set_hash,
                'created_at'        => $now,
                'updated_at'        => $now,
            ),
            array( '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s' )
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

    public function find_comparison_id_by_key( $comparison_key ) {
        $comparison_key = sanitize_key( $comparison_key );
        if ( '' === $comparison_key ) {
            return 0;
        }

        return (int) $this->wpdb->get_var(
            $this->wpdb->prepare(
                "SELECT id FROM {$this->comparisons} WHERE comparison_key = %s LIMIT 1",
                $comparison_key
            )
        );
    }

    public function set_features( $comparison_id, array $features, $manage_transaction = true ) {
        $comparison_id = absint( $comparison_id );
        if ( ! $this->comparison_exists( $comparison_id ) ) {
            return new WP_Error( 'UPC_COMPARISON_NOT_FOUND', 'Comparison does not exist.' );
        }

        if ( count( $features ) < 1 || count( $features ) > 64 ) {
            return new WP_Error( 'UPC_INVALID_FEATURE_COUNT', 'A comparison requires one to 64 declared features.' );
        }

        $normalized = array();
        $seen = array();
        foreach ( array_values( $features ) as $index => $feature ) {
            if ( ! is_array( $feature ) ) {
                return new WP_Error( 'UPC_INVALID_FEATURE', 'Feature definition is invalid.' );
            }

            $fact_key = isset( $feature['fact_key'] ) ? sanitize_key( $feature['fact_key'] ) : '';
            $label    = isset( $feature['label'] ) ? sanitize_text_field( $feature['label'] ) : '';

            if ( '' === $fact_key || '' === $label ) {
                return new WP_Error( 'UPC_INVALID_FEATURE', 'Feature key and label are required.' );
            }

            if ( isset( $seen[ $fact_key ] ) ) {
                return new WP_Error( 'UPC_DUPLICATE_FEATURE', 'Feature keys must be unique within a comparison.' );
            }
            $seen[ $fact_key ] = true;

            $normalized[] = array(
                'fact_key' => $fact_key,
                'label'    => $label,
                'position' => $index + 1,
                'required' => ! isset( $feature['required'] ) || (bool) $feature['required'] ? 1 : 0,
            );
        }

        $now = current_time( 'mysql', true );
        if ( $manage_transaction ) {
            $this->wpdb->query( 'START TRANSACTION' );
        }
        $deleted = $this->wpdb->delete( $this->features, array( 'comparison_id' => $comparison_id ), array( '%d' ) );
        if ( false === $deleted ) {
            if ( $manage_transaction ) {
                $this->wpdb->query( 'ROLLBACK' );
            }
            return new WP_Error( 'UPC_FEATURE_RESET_FAILED', 'Existing comparison features could not be reset.' );
        }

        foreach ( $normalized as $feature ) {
            $ok = $this->wpdb->insert(
                $this->features,
                array(
                    'comparison_id' => $comparison_id,
                    'fact_key'      => $feature['fact_key'],
                    'label'         => $feature['label'],
                    'position'      => $feature['position'],
                    'required'      => $feature['required'],
                    'created_at'    => $now,
                ),
                array( '%d', '%s', '%s', '%d', '%d', '%s' )
            );
            if ( false === $ok ) {
                if ( $manage_transaction ) {
                    $this->wpdb->query( 'ROLLBACK' );
                }
                return new WP_Error( 'UPC_FEATURE_INSERT_FAILED', $this->wpdb->last_error ? $this->wpdb->last_error : 'Comparison feature insert failed.' );
            }
        }

        $this->wpdb->update(
            $this->comparisons,
            array( 'updated_at' => $now ),
            array( 'id' => $comparison_id ),
            array( '%s' ),
            array( '%d' )
        );
        if ( $manage_transaction ) {
            $this->wpdb->query( 'COMMIT' );
        }

        return count( $normalized );
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

        $features = $this->wpdb->get_results(
            $this->wpdb->prepare(
                "SELECT fact_key, label, position, required FROM {$this->features} WHERE comparison_id = %d ORDER BY position ASC",
                $comparison_id
            ),
            ARRAY_A
        );

        $matrix = array();
        $missing = array();

        foreach ( $features as $feature ) {
            $row = array(
                'fact_key' => $feature['fact_key'],
                'label'    => $feature['label'],
                'position' => (int) $feature['position'],
                'required' => (bool) $feature['required'],
                'cells'    => array(),
            );

            foreach ( $resolved as $item ) {
                $facts = isset( $item['knowledge']['facts'] ) && is_array( $item['knowledge']['facts'] )
                    ? $item['knowledge']['facts']
                    : array();

                $matches = array_values( array_filter(
                    $facts,
                    function( $fact ) use ( $feature ) {
                        return isset( $fact['fact_key'] ) && $fact['fact_key'] === $feature['fact_key'];
                    }
                ) );

                if ( empty( $matches ) && (bool) $feature['required'] ) {
                    $missing[] = array(
                        'fact_key'      => $feature['fact_key'],
                        'subject_type'  => $item['subject_type'],
                        'subject_id'    => $item['subject_id'],
                    );
                }

                $row['cells'][] = array(
                    'subject_type' => $item['subject_type'],
                    'subject_id'   => $item['subject_id'],
                    'status'       => empty( $matches ) ? 'MISSING' : 'PRESENT',
                    'facts'        => $matches,
                );
            }

            $matrix[] = $row;
        }

        $comparison['comparison_uid'] = 'UPC-' . str_pad( (string) $comparison_id, 6, '0', STR_PAD_LEFT );
        $comparison['items'] = $resolved;
        $comparison['features'] = $features;
        $comparison['feature_matrix'] = $matrix;
        $comparison['required_facts_complete'] = empty( $missing );
        $comparison['missing_required_facts'] = $missing;

        return $comparison;
    }

    public function validate_required_facts( $comparison_id ) {
        $bundle = $this->get_comparison_bundle( $comparison_id );
        if ( is_wp_error( $bundle ) ) {
            return $bundle;
        }

        if ( ! $bundle['required_facts_complete'] ) {
            return new WP_Error(
                'UPC_REQUIRED_FACT_MISSING',
                'One or more required comparison facts are missing.',
                array( 'missing' => $bundle['missing_required_facts'] )
            );
        }

        return true;
    }

    public function build_comparison_dossier( $comparison_id ) {
        $bundle = $this->get_comparison_bundle( $comparison_id );
        if ( is_wp_error( $bundle ) ) {
            return $bundle;
        }

        if ( empty( $bundle['features'] ) ) {
            return new WP_Error( 'UPC_FEATURES_MISSING', 'Comparison features must be declared before a dossier can be built.' );
        }

        if ( ! $bundle['required_facts_complete'] ) {
            return new WP_Error(
                'UPC_REQUIRED_FACT_MISSING',
                'One or more required comparison facts are missing.',
                array( 'missing' => $bundle['missing_required_facts'] )
            );
        }

        $subjects = array();
        foreach ( $bundle['items'] as $item ) {
            $knowledge = $item['knowledge'];
            if ( UPK_Repository::SUBJECT_PRODUCT === $item['subject_type'] ) {
                $subjects[] = array(
                    'position'        => $item['position'],
                    'subject_type'    => $item['subject_type'],
                    'subject_id'      => $item['subject_id'],
                    'manufacturer'    => $knowledge['manufacturer'],
                    'model_name'      => $knowledge['model_name'],
                    'product_group_key' => $knowledge['product_group_key'],
                    'lifecycle_status'=> $knowledge['lifecycle_status'],
                    'identifiers'     => $knowledge['identifiers'],
                );
            } else {
                $subjects[] = array(
                    'position'        => $item['position'],
                    'subject_type'    => $item['subject_type'],
                    'subject_id'      => $item['subject_id'],
                    'variant_name'    => $knowledge['variant_name'],
                    'variant_key'     => $knowledge['variant_key'],
                    'base_product_id' => (int) $knowledge['product_id'],
                    'manufacturer'    => $knowledge['product']['manufacturer'],
                    'model_name'      => $knowledge['product']['model_name'],
                    'product_group_key' => $knowledge['product']['product_group_key'],
                    'lifecycle_status'=> $knowledge['lifecycle_status'],
                    'identifiers'     => $knowledge['identifiers'],
                );
            }
        }

        $rows = array();
        $warnings = array();

        foreach ( $bundle['feature_matrix'] as $feature ) {
            $cells = array();

            foreach ( $feature['cells'] as $cell ) {
                $facts = isset( $cell['facts'] ) && is_array( $cell['facts'] ) ? $cell['facts'] : array();

                if ( count( $facts ) > 1 ) {
                    $warnings[] = array(
                        'code'         => 'MULTIPLE_FACT_RECORDS',
                        'fact_key'     => $feature['fact_key'],
                        'subject_type' => $cell['subject_type'],
                        'subject_id'   => $cell['subject_id'],
                    );
                }

                foreach ( $facts as $fact ) {
                    if ( isset( $fact['fact_status'] ) && 'VERIFIED' !== $fact['fact_status'] ) {
                        $warnings[] = array(
                            'code'         => $fact['fact_status'],
                            'fact_key'     => $feature['fact_key'],
                            'subject_type' => $cell['subject_type'],
                            'subject_id'   => $cell['subject_id'],
                            'source_url'   => isset( $fact['source_url'] ) ? $fact['source_url'] : '',
                        );
                    }
                }

                $cells[] = array(
                    'subject_type' => $cell['subject_type'],
                    'subject_id'   => $cell['subject_id'],
                    'facts'        => $facts,
                );
            }

            $rows[] = array(
                'fact_key' => $feature['fact_key'],
                'label'    => $feature['label'],
                'position' => $feature['position'],
                'required' => $feature['required'],
                'cells'    => $cells,
            );
        }

        return array(
            'schema_version' => '1',
            'status'         => empty( $warnings ) ? 'READY' : 'READY_WITH_WARNINGS',
            'comparison'     => array(
                'comparison_id'     => (int) $bundle['id'],
                'comparison_uid'    => $bundle['comparison_uid'],
                'comparison_key'    => $bundle['comparison_key'],
                'comparison_type'   => $bundle['comparison_type'],
                'product_group_key' => $bundle['product_group_key'],
                'working_title'     => $bundle['working_title'],
                'decision_intent'   => $bundle['decision_intent'],
                'comparability_note'=> $bundle['comparability_note'],
            ),
            'subjects'       => $subjects,
            'features'       => $rows,
            'warnings'       => $warnings,
        );
    }

    private function comparison_exists( $comparison_id ) {
        return (bool) $this->wpdb->get_var(
            $this->wpdb->prepare( "SELECT id FROM {$this->comparisons} WHERE id = %d LIMIT 1", absint( $comparison_id ) )
        );
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

            $manufacturers[] = strtolower( remove_accents( trim( $product['manufacturer'] ) ) );
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
