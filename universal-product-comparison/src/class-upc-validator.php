<?php

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

/**
 * Independent deterministic output acceptance gate.
 */
class UPC_Validator {
    public static function validate_quarantined_draft( array $draft ) {
        $required = array(
            'status',
            'comparison_uid',
            'title',
            'html',
            'input_hash',
            'output_hash',
            'renderer_version',
            'article_contract_version',
            'ruleset_id',
            'ruleset_version',
            'ruleset_sha256',
        );

        foreach ( $required as $field ) {
            if ( ! isset( $draft[ $field ] ) || '' === (string) $draft[ $field ] ) {
                return new WP_Error( 'UPC_DRAFT_FIELD_MISSING', 'Quarantined draft field is missing.', array( 'field' => $field ) );
            }
        }

        if ( 'QUARANTINED_RENDERED' !== $draft['status'] ) {
            return new WP_Error( 'UPC_DRAFT_STATUS_INVALID', 'Only quarantined renderer output may enter validation.' );
        }

        if ( hash( 'sha256', $draft['html'] ) !== $draft['output_hash'] ) {
            return new WP_Error( 'UPC_OUTPUT_HASH_MISMATCH', 'Rendered HTML hash does not match.' );
        }

        $forbidden = array(
            '<a ', '<a>', 'href=', 'http://', 'https://',
            '<script', '<iframe', '<form', '<style',
        );
        foreach ( $forbidden as $needle ) {
            if ( false !== stripos( $draft['html'], $needle ) ) {
                return new WP_Error( 'UPC_FORBIDDEN_OUTPUT_TOKEN', 'Rendered HTML contains a forbidden token.', array( 'token' => $needle ) );
            }
        }

        $sections = array(
            '<h2>Vergleich auf einen Blick</h2>',
            '<h2>Die entscheidenden Unterschiede</h2>',
            '<h2>Vor- und Nachteile im direkten Vergleich</h2>',
            '<h2>Welches Produkt passt zu welchem Bedarf?</h2>',
            '<h2>Hinweise zur Quellenlage</h2>',
            '<h2>Fazit</h2>',
        );

        $last_position = -1;
        foreach ( $sections as $section ) {
            $position = strpos( $draft['html'], $section );
            if ( false === $position || $position <= $last_position ) {
                return new WP_Error(
                    'UPC_ARTICLE_CONTRACT_SECTION_ORDER_INVALID',
                    'Article section is missing or out of order.',
                    array( 'section' => $section )
                );
            }
            $last_position = $position;
        }

        if ( false === strpos( $draft['html'], 'Bedeutung für die Entscheidung' ) ) {
            return new WP_Error( 'UPC_DECISION_COLUMN_MISSING', 'Comparison table has no decision meaning column.' );
        }

        if ( false === strpos( $draft['html'], 'Es gibt keinen pauschalen Sieger.' ) ) {
            return new WP_Error( 'UPC_NO_WINNER_RULE_MISSING', 'Conclusion violates the no-universal-winner contract.' );
        }

        return true;
    }
}
