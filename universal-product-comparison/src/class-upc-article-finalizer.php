<?php

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

/**
 * Final deterministic WordPress-DRAFT layer.
 *
 * Order:
 * validated core -> bound internal links -> bound neutral graphic -> final draft hash.
 * No publish capability.
 */
class UPC_Article_Finalizer {
    const CONTRACT_VERSION = '1';

    private $link_finalizer;
    private $graphic;

    public function __construct( $link_finalizer, $graphic ) {
        $this->link_finalizer = $link_finalizer;
        $this->graphic        = $graphic;
    }

    public function finalize( $comparison_id, $project_key, $ruleset_id ) {
        $linked = $this->link_finalizer->finalize( $comparison_id, $project_key, $ruleset_id );
        if ( is_wp_error( $linked ) ) {
            return $linked;
        }

        if ( 'WORDPRESS_DRAFT_LINKS_VERIFIED' !== $linked['status'] || false !== $linked['publish_allowed'] ) {
            return new WP_Error( 'UPC_ARTICLE_FINALIZER_LINK_STAGE_INVALID', 'Only a verified non-publishable linked draft may be finalized.' );
        }

        $post_id = (int) $linked['post_id'];
        $post    = get_post( $post_id );

        if ( ! $post || 'draft' !== $post->post_status ) {
            return new WP_Error( 'UPC_ARTICLE_FINALIZER_SOURCE_NOT_DRAFT', 'Final article graphic may only be added to a draft.' );
        }

        if ( hash( 'sha256', (string) $post->post_content ) !== (string) $linked['linked_output_hash']
            || (string) get_post_meta( $post_id, '_upc_linked_output_hash', true ) !== (string) $linked['linked_output_hash']
        ) {
            return new WP_Error( 'UPC_ARTICLE_FINALIZER_LINK_BINDING_MISMATCH', 'Draft content is not bound to the verified link-finalization output.' );
        }

        $graphic = $this->graphic->build( $comparison_id );
        if ( is_wp_error( $graphic ) ) {
            return $graphic;
        }

        $figure = $this->render_figure( $graphic );
        $final_html = $this->insert_before_overview( (string) $post->post_content, $figure );
        if ( is_wp_error( $final_html ) ) {
            return $final_html;
        }

        $valid = $this->validate_final_html( $final_html, (string) $post->post_content, $figure );
        if ( is_wp_error( $valid ) ) {
            return $valid;
        }

        $final_hash = hash( 'sha256', $final_html );

        $updated = wp_update_post(
            wp_slash(
                array(
                    'ID'           => $post_id,
                    'post_status'  => 'draft',
                    'post_content' => $final_html,
                )
            ),
            true
        );
        if ( is_wp_error( $updated ) ) {
            return $updated;
        }

        update_post_meta( $post_id, '_upc_graphic_contract_version', self::CONTRACT_VERSION );
        update_post_meta( $post_id, '_upc_graphic_filename', $graphic['filename'] );
        update_post_meta( $post_id, '_upc_graphic_input_hash', $graphic['input_hash'] );
        update_post_meta( $post_id, '_upc_graphic_sha256', $graphic['svg_sha256'] );
        update_post_meta( $post_id, '_upc_final_output_hash', $final_hash );
        update_post_meta( $post_id, '_upc_publish_allowed', '0' );

        $readback = get_post( $post_id );
        if ( ! $readback
            || 'draft' !== $readback->post_status
            || (string) $readback->post_content !== $final_html
            || hash( 'sha256', (string) $readback->post_content ) !== $final_hash
            || (string) get_post_meta( $post_id, '_upc_graphic_filename', true ) !== (string) $graphic['filename']
            || (string) get_post_meta( $post_id, '_upc_graphic_sha256', true ) !== (string) $graphic['svg_sha256']
            || (string) get_post_meta( $post_id, '_upc_final_output_hash', true ) !== $final_hash
            || '0' !== (string) get_post_meta( $post_id, '_upc_publish_allowed', true )
        ) {
            return new WP_Error( 'UPC_ARTICLE_FINALIZER_READBACK_MISMATCH', 'Final WordPress draft differs from the bound article-finalization output.' );
        }

        return array(
            'status'               => 'WORDPRESS_DRAFT_FINAL_VERIFIED',
            'post_id'              => $post_id,
            'core_output_hash'     => $linked['core_output_hash'],
            'link_manifest_sha256' => $linked['link_manifest_sha256'],
            'linked_output_hash'   => $linked['linked_output_hash'],
            'graphic_filename'     => $graphic['filename'],
            'graphic_sha256'       => $graphic['svg_sha256'],
            'final_output_hash'    => $final_hash,
            'link_count'           => (int) $linked['link_count'],
            'publish_allowed'      => false,
        );
    }

    private function render_figure( array $graphic ) {
        return '<figure class="upc-comparison-graphic" data-upc-graphic-sha256="' .
            esc_attr( $graphic['svg_sha256'] ) . '">' . "\n" .
            $graphic['svg'] . "\n" .
            '<figcaption>Neutrale Vergleichsgrafik ohne Produktbilder oder Herstellerlogos.</figcaption>' . "\n" .
            '</figure>';
    }

    private function insert_before_overview( $html, $figure ) {
        $marker = '<h2>Vergleich auf einen Blick</h2>';
        if ( 1 !== substr_count( $html, $marker ) ) {
            return new WP_Error( 'UPC_ARTICLE_FINALIZER_OVERVIEW_MARKER_INVALID', 'Linked article must contain exactly one bound comparison-overview marker.' );
        }

        return str_replace( $marker, $figure . "\n" . $marker, $html );
    }

    private function validate_final_html( $final_html, $linked_html, $figure ) {
        if ( 1 !== substr_count( $final_html, '<figure class="upc-comparison-graphic"' ) ) {
            return new WP_Error( 'UPC_ARTICLE_FINALIZER_GRAPHIC_COUNT_INVALID', 'Final article must contain exactly one bound comparison graphic.' );
        }

        if ( false === strpos( $final_html, $figure ) ) {
            return new WP_Error( 'UPC_ARTICLE_FINALIZER_GRAPHIC_MISMATCH', 'Final article graphic differs from the bound graphic output.' );
        }

        $without_figure = str_replace( $figure . "\n", '', $final_html );
        if ( $without_figure !== $linked_html ) {
            return new WP_Error( 'UPC_ARTICLE_FINALIZER_LINKED_CONTENT_MUTATED', 'Article finalization changed content outside the bound graphic figure.' );
        }

        return true;
    }
}
