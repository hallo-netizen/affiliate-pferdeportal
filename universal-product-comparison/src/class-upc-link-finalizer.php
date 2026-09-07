<?php

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

/**
 * Deterministic internal-link finalizer for already validated WordPress drafts.
 * No editorial link choice, no free text and no publish capability.
 */
class UPC_Link_Finalizer {
    const CONTRACT_VERSION = '1';

    private $production;
    private $repository;

    public function __construct( $production, $repository ) {
        $this->production = $production;
        $this->repository = $repository;
    }

    public function finalize( $comparison_id, $project_key, $ruleset_id ) {
        $comparison_id = absint( $comparison_id );
        $project_key   = sanitize_key( $project_key );
        $ruleset_id    = sanitize_key( $ruleset_id );

        if ( $comparison_id <= 0 || '' === $project_key || '' === $ruleset_id ) {
            return new WP_Error( 'UPC_LINK_FINALIZER_INPUT_INVALID', 'Bound comparison, project and ruleset are required.' );
        }

        $core = $this->production->execute( $comparison_id, $project_key, $ruleset_id );
        if ( is_wp_error( $core ) ) {
            return $core;
        }

        if ( 'DRAFT_READY_FOR_REVIEW' !== $core['status'] || false !== $core['publish_allowed'] ) {
            return new WP_Error( 'UPC_LINK_FINALIZER_CORE_INVALID', 'Only validated non-publishable core output may be finalized.' );
        }

        $post_id = $this->find_source_draft( $comparison_id, $project_key );
        if ( is_wp_error( $post_id ) ) {
            return $post_id;
        }

        if ( (string) get_post_meta( $post_id, '_upc_output_hash', true ) !== (string) $core['output_hash']
            || (string) get_post_meta( $post_id, '_upc_receipt_hash', true ) !== (string) $core['receipt_hash']
        ) {
            return new WP_Error( 'UPC_LINK_FINALIZER_CORE_BINDING_MISMATCH', 'WordPress draft is not bound to the regenerated core output.' );
        }

        $resolver = new UPC_Link_Manifest( $this->repository );
        $manifest = $resolver->build( $comparison_id, $project_key );
        if ( is_wp_error( $manifest ) ) {
            return $manifest;
        }

        $link_section = $this->render_link_section( $manifest );
        if ( is_wp_error( $link_section ) ) {
            return $link_section;
        }

        $linked_html = $this->insert_before_fazit( $core['html'], $link_section );
        if ( is_wp_error( $linked_html ) ) {
            return $linked_html;
        }

        $validation = $this->validate_linked_html( $linked_html, $core['html'], $manifest );
        if ( is_wp_error( $validation ) ) {
            return $validation;
        }

        $linked_output_hash = hash( 'sha256', $linked_html );

        $updated = wp_update_post(
            wp_slash(
                array(
                    'ID'           => $post_id,
                    'post_status'  => 'draft',
                    'post_content' => $linked_html,
                )
            ),
            true
        );
        if ( is_wp_error( $updated ) ) {
            return $updated;
        }

        update_post_meta( $post_id, '_upc_link_contract_version', self::CONTRACT_VERSION );
        update_post_meta( $post_id, '_upc_link_manifest_sha256', $manifest['manifest_sha256'] );
        update_post_meta( $post_id, '_upc_linked_output_hash', $linked_output_hash );

        $post = get_post( $post_id );
        if ( ! $post
            || 'draft' !== $post->post_status
            || (string) $post->post_content !== (string) $linked_html
            || hash( 'sha256', (string) $post->post_content ) !== $linked_output_hash
            || (string) get_post_meta( $post_id, '_upc_link_manifest_sha256', true ) !== (string) $manifest['manifest_sha256']
            || (string) get_post_meta( $post_id, '_upc_linked_output_hash', true ) !== $linked_output_hash
        ) {
            return new WP_Error( 'UPC_LINK_FINALIZER_READBACK_MISMATCH', 'Linked WordPress draft differs from the bound finalization output.' );
        }

        return array(
            'status'               => 'WORDPRESS_DRAFT_LINKS_VERIFIED',
            'post_id'              => $post_id,
            'core_output_hash'     => $core['output_hash'],
            'link_manifest_sha256' => $manifest['manifest_sha256'],
            'linked_output_hash'   => $linked_output_hash,
            'link_count'           => count( $manifest['entries'] ),
            'publish_allowed'      => false,
        );
    }

    private function find_source_draft( $comparison_id, $project_key ) {
        $ids = get_posts(
            array(
                'post_type'      => 'post',
                'post_status'    => 'any',
                'posts_per_page' => 2,
                'fields'         => 'ids',
                'meta_query'     => array(
                    'relation' => 'AND',
                    array(
                        'key'   => '_upc_comparison_id',
                        'value' => (string) $comparison_id,
                    ),
                    array(
                        'key'   => '_upc_project_key',
                        'value' => $project_key,
                    ),
                ),
            )
        );

        if ( 1 !== count( $ids ) ) {
            return new WP_Error( 'UPC_LINK_FINALIZER_SOURCE_NOT_UNIQUE', 'Exactly one bound WordPress source post is required.' );
        }

        $post = get_post( (int) $ids[0] );
        if ( ! $post || 'draft' !== $post->post_status ) {
            return new WP_Error( 'UPC_LINK_FINALIZER_SOURCE_NOT_DRAFT', 'Internal links may only be finalized on a draft.' );
        }

        return (int) $post->ID;
    }

    private function render_link_section( array $manifest ) {
        if ( empty( $manifest['entries'] ) ) {
            return '';
        }

        $source_type = (string) $manifest['source_type'];
        if ( 'product' === $source_type ) {
            $heading = 'Passende Variantenvergleiche';
        } elseif ( 'variant' === $source_type ) {
            $heading = 'Passende Produktvergleiche';
        } else {
            return new WP_Error( 'UPC_LINK_FINALIZER_SOURCE_TYPE_INVALID', 'Unsupported link-manifest source type.' );
        }

        $home_host = strtolower( (string) wp_parse_url( home_url( '/' ), PHP_URL_HOST ) );
        $out = array( '<h2>' . esc_html( $heading ) . '</h2>', '<ul class="upc-related-comparisons">' );

        foreach ( $manifest['entries'] as $entry ) {
            $target_url = (string) $entry['target_url'];
            $target_host = strtolower( (string) wp_parse_url( $target_url, PHP_URL_HOST ) );

            if ( '' === $target_url || '' === $target_host || $target_host !== $home_host ) {
                return new WP_Error( 'UPC_LINK_FINALIZER_EXTERNAL_TARGET', 'Only bound same-site WordPress targets are allowed.' );
            }

            if ( ! in_array( (string) $entry['target_post_status'], array( 'draft', 'publish' ), true ) ) {
                return new WP_Error( 'UPC_LINK_FINALIZER_TARGET_STATUS_INVALID', 'Target post has an unsupported status.' );
            }

            $relation_label = 'variant_comparison_for_product' === $entry['relation']
                ? 'Variantenvergleich'
                : 'Produktvergleich';

            $out[] = '<li><a href="' . esc_url( $target_url ) . '">' .
                esc_html( $relation_label . ': ' . $entry['target_title'] ) . '</a></li>';
        }

        $out[] = '</ul>';
        return implode( "\n", $out );
    }

    private function insert_before_fazit( $core_html, $link_section ) {
        if ( '' === $link_section ) {
            return $core_html;
        }

        $marker = '<h2>Fazit</h2>';
        if ( 1 !== substr_count( $core_html, $marker ) ) {
            return new WP_Error( 'UPC_LINK_FINALIZER_FAZIT_MARKER_INVALID', 'Core article must contain exactly one bound Fazit marker.' );
        }

        return str_replace( $marker, $link_section . "\n" . $marker, $core_html );
    }

    private function validate_linked_html( $linked_html, $core_html, array $manifest ) {
        $expected_hrefs = array();
        foreach ( $manifest['entries'] as $entry ) {
            $expected_hrefs[] = esc_url( (string) $entry['target_url'] );
        }

        preg_match_all( '/<a\s+href="([^"]+)"[^>]*>/', $linked_html, $matches );
        $actual_hrefs = isset( $matches[1] ) ? array_values( $matches[1] ) : array();

        if ( $expected_hrefs !== $actual_hrefs ) {
            return new WP_Error( 'UPC_LINK_FINALIZER_LINK_SET_MISMATCH', 'Rendered internal links differ from the bound manifest.' );
        }

        $without_links = preg_replace(
            '/<h2>Passende (?:Varianten|Produkt)vergleiche<\/h2>\n<ul class="upc-related-comparisons">.*?<\/ul>\n/s',
            '',
            $linked_html,
            1
        );

        if ( ! empty( $manifest['entries'] ) && $without_links !== $core_html ) {
            return new WP_Error( 'UPC_LINK_FINALIZER_CORE_MUTATED', 'Link finalization changed content outside the fixed link section.' );
        }

        if ( empty( $manifest['entries'] ) && $linked_html !== $core_html ) {
            return new WP_Error( 'UPC_LINK_FINALIZER_EMPTY_MANIFEST_MUTATED_CORE', 'Empty link manifest must leave core output unchanged.' );
        }

        return true;
    }
}
