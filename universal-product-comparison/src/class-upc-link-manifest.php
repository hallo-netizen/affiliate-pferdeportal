<?php

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

/**
 * Read-only relation resolver for Product Comparison <-> Variant Comparison.
 * It selects no editorial link freely; relations come only from bound product IDs.
 */
class UPC_Link_Manifest {
    const SCHEMA_VERSION = '1';

    private $repository;

    public function __construct( $repository ) {
        $this->repository = $repository;
    }

    public function build( $source_comparison_id, $project_key ) {
        $source_comparison_id = absint( $source_comparison_id );
        $project_key = sanitize_key( $project_key );

        if ( $source_comparison_id <= 0 || '' === $project_key ) {
            return new WP_Error( 'UPC_LINK_MANIFEST_INPUT_INVALID', 'Source comparison and project are required.' );
        }

        $source = $this->repository->get_comparison_bundle( $source_comparison_id );
        if ( is_wp_error( $source ) ) {
            return $source;
        }

        $source_type = strtoupper( (string) $source['comparison_type'] );
        if ( ! in_array( $source_type, array( UPC_Repository::TYPE_PRODUCT, UPC_Repository::TYPE_VARIANT ), true ) ) {
            return new WP_Error( 'UPC_LINK_MANIFEST_SOURCE_TYPE_INVALID', 'Unsupported source comparison type.' );
        }

        $source_product_ids = $this->base_product_ids( $source );
        if ( is_wp_error( $source_product_ids ) ) {
            return $source_product_ids;
        }

        $posts = get_posts(
            array(
                'post_type'      => 'post',
                'post_status'    => array( 'draft', 'publish' ),
                'posts_per_page' => -1,
                'orderby'        => 'ID',
                'order'          => 'ASC',
                'fields'         => 'ids',
                'meta_query'     => array(
                    'relation' => 'AND',
                    array(
                        'key'   => '_upc_project_key',
                        'value' => $project_key,
                    ),
                    array(
                        'key'     => '_upc_comparison_id',
                        'compare' => 'EXISTS',
                    ),
                ),
            )
        );

        $seen_comparisons = array();
        $entries = array();

        foreach ( $posts as $post_id ) {
            $post_id = absint( $post_id );
            $target_comparison_id = absint( get_post_meta( $post_id, '_upc_comparison_id', true ) );

            if ( $target_comparison_id <= 0 || $target_comparison_id === $source_comparison_id ) {
                continue;
            }

            if ( isset( $seen_comparisons[ $target_comparison_id ] ) ) {
                return new WP_Error(
                    'UPC_LINK_MANIFEST_DUPLICATE_TARGET_POST',
                    'More than one WordPress post is bound to a target comparison.',
                    array( 'comparison_id' => $target_comparison_id )
                );
            }
            $seen_comparisons[ $target_comparison_id ] = $post_id;

            $target = $this->repository->get_comparison_bundle( $target_comparison_id );
            if ( is_wp_error( $target ) ) {
                return new WP_Error(
                    'UPC_LINK_MANIFEST_BROKEN_TARGET',
                    'A bound WordPress post references an invalid comparison.',
                    array( 'post_id' => $post_id, 'comparison_id' => $target_comparison_id )
                );
            }

            $target_type = strtoupper( (string) $target['comparison_type'] );
            $target_product_ids = $this->base_product_ids( $target );
            if ( is_wp_error( $target_product_ids ) ) {
                return $target_product_ids;
            }

            $relation = '';
            $matched_product_ids = array_values( array_intersect( $source_product_ids, $target_product_ids ) );

            if ( UPC_Repository::TYPE_PRODUCT === $source_type
                && UPC_Repository::TYPE_VARIANT === $target_type
                && ! empty( $matched_product_ids )
            ) {
                $relation = 'variant_comparison_for_product';
            }

            if ( UPC_Repository::TYPE_VARIANT === $source_type
                && UPC_Repository::TYPE_PRODUCT === $target_type
                && ! empty( $matched_product_ids )
            ) {
                $relation = 'product_comparison_for_variant';
            }

            if ( '' === $relation ) {
                continue;
            }

            $post = get_post( $post_id );
            if ( ! $post ) {
                return new WP_Error( 'UPC_LINK_MANIFEST_TARGET_POST_MISSING', 'Target WordPress post is missing.' );
            }

            $entries[] = array(
                'relation'             => $relation,
                'source_comparison_id' => $source_comparison_id,
                'target_comparison_id' => $target_comparison_id,
                'target_post_id'       => $post_id,
                'target_post_status'   => (string) $post->post_status,
                'target_title'         => (string) get_the_title( $post ),
                'target_url'           => (string) get_permalink( $post ),
                'matched_product_ids'  => array_values( array_map( 'intval', $matched_product_ids ) ),
            );
        }

        usort(
            $entries,
            function( $left, $right ) {
                if ( $left['target_comparison_id'] === $right['target_comparison_id'] ) {
                    return $left['target_post_id'] <=> $right['target_post_id'];
                }
                return $left['target_comparison_id'] <=> $right['target_comparison_id'];
            }
        );

        $payload = array(
            'schema_version'       => self::SCHEMA_VERSION,
            'project_key'          => $project_key,
            'source_comparison_id' => $source_comparison_id,
            'source_type'          => strtolower( $source_type ),
            'entries'              => $entries,
        );

        $payload['manifest_sha256'] = hash( 'sha256', $this->canonical_json( $payload ) );
        return $payload;
    }

    private function base_product_ids( array $bundle ) {
        $ids = array();

        foreach ( $bundle['items'] as $item ) {
            if ( UPK_Repository::SUBJECT_PRODUCT === $item['subject_type'] ) {
                $ids[] = absint( $item['subject_id'] );
                continue;
            }

            if ( UPK_Repository::SUBJECT_VARIANT === $item['subject_type'] ) {
                $product_id = absint( $item['knowledge']['product_id'] ?? 0 );
                if ( $product_id <= 0 ) {
                    return new WP_Error( 'UPC_LINK_MANIFEST_BASE_PRODUCT_MISSING', 'Variant has no bound base product.' );
                }
                $ids[] = $product_id;
                continue;
            }

            return new WP_Error( 'UPC_LINK_MANIFEST_SUBJECT_TYPE_INVALID', 'Unsupported comparison subject type.' );
        }

        $ids = array_values( array_unique( array_filter( $ids ) ) );
        sort( $ids, SORT_NUMERIC );
        return $ids;
    }

    private function canonical_json( $value ) {
        return wp_json_encode( $this->sort_recursive( $value ), JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE );
    }

    private function sort_recursive( $value ) {
        if ( ! is_array( $value ) ) {
            return $value;
        }

        if ( array_keys( $value ) !== range( 0, count( $value ) - 1 ) ) {
            ksort( $value, SORT_STRING );
        }

        foreach ( $value as $key => $child ) {
            $value[ $key ] = $this->sort_recursive( $child );
        }

        return $value;
    }
}
