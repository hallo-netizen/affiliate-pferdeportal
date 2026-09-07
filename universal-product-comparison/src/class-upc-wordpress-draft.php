<?php

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

/**
 * WordPress draft materializer.
 * It accepts no free title, body or category input.
 */
class UPC_WordPress_Draft {
    private $production;

    public function __construct( $production ) {
        $this->production = $production;
    }

    public function materialize( $comparison_id, $project_key, $ruleset_id ) {
        $project_config = UPC_Project_Config::load_publishing( $project_key );
        if ( is_wp_error( $project_config ) ) {
            return $project_config;
        }

        $draft = $this->production->execute( $comparison_id, $project_key, $ruleset_id );
        if ( is_wp_error( $draft ) ) {
            return $draft;
        }

        if ( 'DRAFT_READY_FOR_REVIEW' !== $draft['status']
            || ! array_key_exists( 'publish_allowed', $draft )
            || false !== $draft['publish_allowed']
            || empty( $draft['receipt_hash'] )
        ) {
            return new WP_Error( 'UPC_PRODUCTION_RECEIPT_INVALID', 'Production output is not eligible for WordPress draft materialization.' );
        }

        if ( false !== $draft['publish_allowed'] ) {
            return new WP_Error( 'UPC_PUBLISH_NOT_ALLOWED', 'Production contract forbids publishing.' );
        }

        $comparison = upc_repository()->get_comparison_bundle( $comparison_id );
        if ( is_wp_error( $comparison ) ) {
            return $comparison;
        }

        $group_key = (string) $comparison['product_group_key'];
        if ( empty( $project_config['category_map'][ $group_key ] ) ) {
            return new WP_Error( 'UPC_CATEGORY_MAPPING_MISSING', 'No bound WordPress category mapping exists for the product group.' );
        }

        $category = $this->resolve_category( $project_config['category_map'][ $group_key ] );
        if ( is_wp_error( $category ) ) {
            return $category;
        }

        $existing_id = $this->find_existing_draft( $draft['comparison_uid'], $project_key );
        if ( is_wp_error( $existing_id ) ) {
            return $existing_id;
        }

        $postarr = array(
            'post_type'     => 'post',
            'post_status'   => 'draft',
            'post_title'    => $draft['title'],
            'post_content'  => $draft['html'],
            'post_category' => array( (int) $category->term_id ),
        );

        if ( $existing_id ) {
            $postarr['ID'] = $existing_id;
        }

        $post_id = wp_insert_post( wp_slash( $postarr ), true );
        if ( is_wp_error( $post_id ) ) {
            return $post_id;
        }

        $meta = array(
            '_upc_project_key'              => sanitize_key( $project_key ),
            '_upc_comparison_id'            => (string) absint( $comparison_id ),
            '_upc_comparison_uid'           => $draft['comparison_uid'],
            '_upc_input_hash'               => $draft['input_hash'],
            '_upc_output_hash'              => $draft['output_hash'],
            '_upc_receipt_hash'             => $draft['receipt_hash'],
            '_upc_renderer_version'         => $draft['renderer_version'],
            '_upc_article_contract_version' => $draft['article_contract_version'],
            '_upc_ruleset_id'               => $draft['ruleset_id'],
            '_upc_ruleset_version'          => $draft['ruleset_version'],
            '_upc_ruleset_sha256'           => $draft['ruleset_sha256'],
            '_upc_publish_allowed'           => '0',
            '_upc_publishing_config_sha256' => $project_config['_binding_sha256'],
        );

        foreach ( $meta as $key => $value ) {
            update_post_meta( $post_id, $key, $value );
        }

        $verified = $this->verify_saved_draft( $post_id, $draft, $category, $meta );
        if ( is_wp_error( $verified ) ) {
            wp_delete_post( $post_id, true );
            return $verified;
        }

        return array(
            'status'        => 'WORDPRESS_DRAFT_VERIFIED',
            'post_id'       => (int) $post_id,
            'comparison_uid'=> $draft['comparison_uid'],
            'output_hash'   => $draft['output_hash'],
            'receipt_hash'  => $draft['receipt_hash'],
            'publish_allowed'=> false,
        );
    }

    private function resolve_category( array $binding ) {
        $required = array( 'name', 'slug', 'parent_slug' );
        foreach ( $required as $field ) {
            if ( ! isset( $binding[ $field ] ) || '' === trim( (string) $binding[ $field ] ) ) {
                return new WP_Error( 'UPC_CATEGORY_BINDING_INVALID', 'Category binding is incomplete.', array( 'field' => $field ) );
            }
        }

        $term = get_term_by( 'slug', sanitize_title( $binding['slug'] ), 'category' );
        if ( ! $term || is_wp_error( $term ) ) {
            return new WP_Error( 'UPC_CATEGORY_NOT_FOUND', 'Bound category slug does not exist.' );
        }

        if ( (string) $term->name !== (string) $binding['name'] ) {
            return new WP_Error( 'UPC_CATEGORY_NAME_MISMATCH', 'Bound category name does not match WordPress.' );
        }

        $parent = get_term( (int) $term->parent, 'category' );
        if ( ! $parent || is_wp_error( $parent ) || (string) $parent->slug !== sanitize_title( $binding['parent_slug'] ) ) {
            return new WP_Error( 'UPC_CATEGORY_PARENT_MISMATCH', 'Bound category parent does not match WordPress.' );
        }

        return $term;
    }

    private function find_existing_draft( $comparison_uid, $project_key ) {
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
                        'value' => (string) $comparison_uid,
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
            return 0;
        }

        $post = get_post( (int) $ids[0] );
        if ( ! $post || 'draft' !== $post->post_status ) {
            return new WP_Error( 'UPC_EXISTING_POST_NOT_DRAFT', 'Existing bound post is not a draft and may not be overwritten.' );
        }

        return (int) $post->ID;
    }

    private function verify_saved_draft( $post_id, array $draft, $category, array $meta ) {
        $post = get_post( $post_id );
        if ( ! $post
            || 'post' !== $post->post_type
            || 'draft' !== $post->post_status
            || (string) $post->post_title !== (string) $draft['title']
            || (string) $post->post_content !== (string) $draft['html']
            || hash( 'sha256', (string) $post->post_content ) !== (string) $draft['output_hash']
        ) {
            return new WP_Error( 'UPC_WORDPRESS_DRAFT_READBACK_MISMATCH', 'Saved WordPress draft differs from validated renderer output.' );
        }

        $categories = wp_get_post_categories( $post_id );
        if ( array( (int) $category->term_id ) !== array_values( array_map( 'intval', $categories ) ) ) {
            return new WP_Error( 'UPC_WORDPRESS_CATEGORY_READBACK_MISMATCH', 'Saved WordPress category differs from bound category.' );
        }

        foreach ( $meta as $key => $expected ) {
            if ( (string) get_post_meta( $post_id, $key, true ) !== (string) $expected ) {
                return new WP_Error( 'UPC_WORDPRESS_META_READBACK_MISMATCH', 'Saved WordPress metadata differs from production receipt.', array( 'meta_key' => $key ) );
            }
        }

        return true;
    }
}
