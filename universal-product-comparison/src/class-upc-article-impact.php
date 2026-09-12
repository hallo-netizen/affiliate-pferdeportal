<?php

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

/**
 * Read-only classification of a regenerated comparison against WordPress.
 *
 * It never writes a post. Draft updates stay delegated to UPC_WordPress_Draft;
 * non-draft posts are only reported for review.
 */
class UPC_Article_Impact {
    private $production;

    public function __construct( $production ) {
        $this->production = $production;
    }

    public function evaluate( $comparison_id, $project_key, $ruleset_id ) {
        $candidate = $this->production->execute( $comparison_id, $project_key, $ruleset_id );
        if ( is_wp_error( $candidate ) ) {
            return $candidate;
        }

        if ( empty( $candidate['comparison_uid'] ) || empty( $candidate['output_hash'] ) ) {
            return new WP_Error( 'UPC_MAINTENANCE_OUTPUT_INVALID', 'Regenerated comparison output is incomplete.' );
        }

        $ids = get_posts(
            array(
                'post_type'      => 'post',
                'post_status'    => 'any',
                'posts_per_page' => 2,
                'fields'         => 'ids',
                'meta_query'     => array(
                    'relation' => 'AND',
                    array(
                        'key'   => '_upc_comparison_uid',
                        'value' => (string) $candidate['comparison_uid'],
                    ),
                    array(
                        'key'   => '_upc_project_key',
                        'value' => sanitize_key( $project_key ),
                    ),
                ),
            )
        );

        if ( count( $ids ) > 1 ) {
            return new WP_Error( 'UPC_DUPLICATE_WORDPRESS_TARGET', 'More than one WordPress post is bound to this comparison.' );
        }

        if ( empty( $ids ) ) {
            return array(
                'status'          => 'ARTICLE_MISSING',
                'comparison_uid'  => $candidate['comparison_uid'],
                'new_output_hash' => $candidate['output_hash'],
                'post_id'         => 0,
            );
        }

        $post = get_post( (int) $ids[0] );
        if ( ! $post ) {
            return new WP_Error( 'UPC_WORDPRESS_TARGET_NOT_FOUND', 'Bound WordPress post could not be read.' );
        }

        $old_hash = (string) get_post_meta( (int) $post->ID, '_upc_output_hash', true );
        if ( '' !== $old_hash && hash_equals( $old_hash, (string) $candidate['output_hash'] ) ) {
            return array(
                'status'          => 'ARTICLE_CURRENT',
                'comparison_uid'  => $candidate['comparison_uid'],
                'new_output_hash' => $candidate['output_hash'],
                'old_output_hash' => $old_hash,
                'post_id'         => (int) $post->ID,
                'post_status'     => (string) $post->post_status,
            );
        }

        return array(
            'status'          => 'draft' === (string) $post->post_status ? 'DRAFT_UPDATE_REQUIRED' : 'PUBLISHED_REVIEW_REQUIRED',
            'comparison_uid'  => $candidate['comparison_uid'],
            'new_output_hash' => $candidate['output_hash'],
            'old_output_hash' => $old_hash,
            'post_id'         => (int) $post->ID,
            'post_status'     => (string) $post->post_status,
        );
    }
}
