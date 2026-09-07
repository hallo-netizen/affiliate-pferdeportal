<?php

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

/**
 * Deterministic, neutral comparison graphic.
 *
 * No external images, no logos, no remote calls and no random state.
 * Same bound comparison identity = byte-identical SVG.
 */
class UPC_Comparison_Graphic {
    const CONTRACT_VERSION = '1';
    const WIDTH  = 1200;
    const HEIGHT = 630;

    private $repository;

    public function __construct( $repository ) {
        $this->repository = $repository;
    }

    public function build( $comparison_id ) {
        $comparison_id = absint( $comparison_id );
        if ( $comparison_id <= 0 ) {
            return new WP_Error( 'UPC_GRAPHIC_COMPARISON_INVALID', 'A valid bound comparison is required.' );
        }

        $dossier = $this->repository->build_comparison_dossier( $comparison_id );
        if ( is_wp_error( $dossier ) ) {
            return $dossier;
        }

        $comparison = $dossier['comparison'];
        $subjects   = $dossier['subjects'];

        if ( empty( $comparison['comparison_key'] ) || empty( $comparison['comparison_uid'] ) ) {
            return new WP_Error( 'UPC_GRAPHIC_IDENTITY_MISSING', 'Comparison graphic requires a stable comparison identity.' );
        }

        if ( empty( $comparison['working_title'] ) ) {
            return new WP_Error( 'UPC_GRAPHIC_TITLE_MISSING', 'Comparison graphic requires the bound article title.' );
        }

        if ( count( $subjects ) < 2 || count( $subjects ) > 4 ) {
            return new WP_Error( 'UPC_GRAPHIC_SUBJECT_COUNT_INVALID', 'Comparison graphic supports two to four bound subjects.' );
        }

        $subject_rows = array();
        foreach ( $subjects as $subject ) {
            $name = $this->subject_name( $subject );
            if ( '' === $name ) {
                return new WP_Error( 'UPC_GRAPHIC_SUBJECT_NAME_MISSING', 'Every graphic subject requires a bound display name.' );
            }

            $subject_rows[] = array(
                'position'     => (int) $subject['position'],
                'subject_type' => (string) $subject['subject_type'],
                'subject_id'   => (int) $subject['subject_id'],
                'name'         => $name,
            );
        }

        $payload = array(
            'contract_version' => self::CONTRACT_VERSION,
            'comparison_uid'   => (string) $comparison['comparison_uid'],
            'comparison_key'   => (string) $comparison['comparison_key'],
            'comparison_type'  => (string) $comparison['comparison_type'],
            'working_title'    => (string) $comparison['working_title'],
            'subjects'         => $subject_rows,
        );

        $input_hash = hash( 'sha256', $this->canonical_json( $payload ) );
        $svg        = $this->render_svg( $payload );
        $svg_hash   = hash( 'sha256', $svg );
        $filename   = sanitize_file_name( strtolower( (string) $comparison['comparison_key'] ) ) . '.svg';

        if ( '.svg' === $filename ) {
            return new WP_Error( 'UPC_GRAPHIC_FILENAME_INVALID', 'Comparison graphic filename could not be derived from the bound comparison key.' );
        }

        return array(
            'status'           => 'GRAPHIC_READY',
            'contract_version' => self::CONTRACT_VERSION,
            'comparison_uid'   => (string) $comparison['comparison_uid'],
            'comparison_key'   => (string) $comparison['comparison_key'],
            'filename'         => $filename,
            'mime_type'        => 'image/svg+xml',
            'input_hash'       => $input_hash,
            'svg_sha256'       => $svg_hash,
            'svg'              => $svg,
        );
    }

    private function render_svg( array $payload ) {
        $subjects = $payload['subjects'];
        $count    = count( $subjects );
        $gap      = 24;
        $margin   = 72;
        $usable   = self::WIDTH - ( 2 * $margin ) - ( ( $count - 1 ) * $gap );
        $card_w   = (int) floor( $usable / $count );
        $card_y   = 286;
        $card_h   = 190;

        $type_label = 'VARIANT' === strtoupper( (string) $payload['comparison_type'] )
            ? 'Variantenvergleich'
            : 'Produktvergleich';

        $out = array();
        $out[] = '<svg xmlns="http://www.w3.org/2000/svg" width="' . self::WIDTH . '" height="' . self::HEIGHT . '" viewBox="0 0 ' . self::WIDTH . ' ' . self::HEIGHT . '" role="img" aria-labelledby="upc-title upc-desc">';
        $out[] = '<title id="upc-title">' . esc_html( $payload['working_title'] ) . '</title>';
        $out[] = '<desc id="upc-desc">Neutrale Vergleichsgrafik ohne Produktbilder oder Herstellerlogos.</desc>';
        $out[] = '<rect width="1200" height="630" fill="#ffffff"/>';
        $out[] = '<rect x="0" y="0" width="1200" height="14" fill="#1f2937"/>';
        $out[] = '<text x="72" y="86" font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="700" fill="#1f2937">' . esc_html( $type_label ) . '</text>';
        $out[] = '<text x="72" y="148" font-family="Arial, Helvetica, sans-serif" font-size="42" font-weight="700" fill="#111827">' . esc_html( $payload['working_title'] ) . '</text>';
        $out[] = '<text x="72" y="205" font-family="Arial, Helvetica, sans-serif" font-size="20" fill="#4b5563">Neutrale Gegenüberstellung auf Basis gebundener Produktidentitäten</text>';

        foreach ( $subjects as $index => $subject ) {
            $x      = $margin + $index * ( $card_w + $gap );
            $center = $x + (int) floor( $card_w / 2 );
            $number = $index + 1;

            $out[] = '<rect x="' . $x . '" y="' . $card_y . '" width="' . $card_w . '" height="' . $card_h . '" rx="18" fill="#f3f4f6" stroke="#d1d5db" stroke-width="2"/>';
            $out[] = '<circle cx="' . $center . '" cy="' . ( $card_y + 52 ) . '" r="24" fill="#1f2937"/>';
            $out[] = '<text x="' . $center . '" y="' . ( $card_y + 60 ) . '" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="22" font-weight="700" fill="#ffffff">' . $number . '</text>';
            $out[] = '<text x="' . $center . '" y="' . ( $card_y + 116 ) . '" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="21" font-weight="700" fill="#111827">' . esc_html( $subject['name'] ) . '</text>';
            $out[] = '<text x="' . $center . '" y="' . ( $card_y + 152 ) . '" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="16" fill="#4b5563">Position ' . (int) $subject['position'] . '</text>';
        }

        $out[] = '<text x="72" y="562" font-family="Arial, Helvetica, sans-serif" font-size="16" fill="#6b7280">ID: ' . esc_html( $payload['comparison_uid'] ) . '</text>';
        $out[] = '<text x="1128" y="562" text-anchor="end" font-family="Arial, Helvetica, sans-serif" font-size="16" fill="#6b7280">Keine Rangliste · kein Testsieger</text>';
        $out[] = '</svg>';

        return implode( "\n", $out );
    }

    private function subject_name( array $subject ) {
        if ( UPK_Repository::SUBJECT_VARIANT === $subject['subject_type'] ) {
            return trim( $subject['manufacturer'] . ' ' . $subject['model_name'] . ' – ' . $subject['variant_name'] );
        }

        return trim( $subject['manufacturer'] . ' ' . $subject['model_name'] );
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
