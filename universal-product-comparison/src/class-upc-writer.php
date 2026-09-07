<?php

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

/**
 * Deterministic renderer, deliberately not a generative writer.
 *
 * Hard rule:
 * identical bound input + identical versions = byte-identical HTML.
 */
class UPC_Writer {
    const RENDERER_VERSION = '2';

    private $repository;

    public function __construct( $repository ) {
        $this->repository = $repository;
    }

    public function render_quarantined( $comparison_id, array $rulebook ) {
        $dossier = $this->repository->build_comparison_dossier( $comparison_id );
        if ( is_wp_error( $dossier ) ) {
            return $dossier;
        }

        $rulebook_valid = UPC_Rulebook::validate_for_dossier( $rulebook, $dossier );
        if ( is_wp_error( $rulebook_valid ) ) {
            return $rulebook_valid;
        }

        $subjects = $dossier['subjects'];
        $rows     = array();
        $pros     = array();
        $cons     = array();
        $needs    = array();

        foreach ( $subjects as $subject ) {
            $position = (int) $subject['position'];
            $pros[ $position ] = array();
            $cons[ $position ] = array();
        }

        foreach ( $dossier['features'] as $feature ) {
            $analysis = $this->analyse_feature( $feature, $rulebook );
            if ( is_wp_error( $analysis ) ) {
                return $analysis;
            }

            $rows[] = array(
                'fact_key'    => $feature['fact_key'],
                'label'       => $feature['label'],
                'cells'       => $feature['cells'],
                'meaning'     => $analysis['meaning'],
                'explanation' => isset( $analysis['explanation'] ) ? $analysis['explanation'] : '',
            );

            foreach ( isset( $analysis['pros_by_position'] ) ? $analysis['pros_by_position'] : array() as $position => $values ) {
                foreach ( (array) $values as $value ) {
                    $pros[ (int) $position ][] = $value;
                }
            }

            foreach ( isset( $analysis['cons_by_position'] ) ? $analysis['cons_by_position'] : array() as $position => $values ) {
                foreach ( (array) $values as $value ) {
                    $cons[ (int) $position ][] = $value;
                }
            }

            foreach ( isset( $analysis['need_fit'] ) ? $analysis['need_fit'] : array() as $need ) {
                $needs[] = $need;
            }
        }

        $title = sanitize_text_field( $dossier['comparison']['working_title'] );
        if ( '' === $title ) {
            return new WP_Error( 'UPC_WORKING_TITLE_MISSING', 'Article title is not explicitly bound.' );
        }

        $input_payload = array(
            'renderer_version'         => self::RENDERER_VERSION,
            'article_contract_version' => UPC_Rulebook::ARTICLE_CONTRACT_VERSION,
            'dossier'                  => $dossier,
            'rulebook'                 => $rulebook,
        );
        $input_hash = hash( 'sha256', $this->canonical_json( $input_payload ) );

        $html = $this->render_html( $dossier, $rows, $pros, $cons, $needs );
        $output_hash = hash( 'sha256', $html );

        return array(
            'status'                   => 'QUARANTINED_RENDERED',
            'comparison_uid'           => $dossier['comparison']['comparison_uid'],
            'title'                    => $title,
            'html'                     => $html,
            'input_hash'               => $input_hash,
            'output_hash'              => $output_hash,
            'renderer_version'         => self::RENDERER_VERSION,
            'article_contract_version' => UPC_Rulebook::ARTICLE_CONTRACT_VERSION,
            'ruleset_id'               => (string) $rulebook['ruleset_id'],
            'ruleset_version'          => (string) $rulebook['ruleset_version'],
            'ruleset_sha256'           => (string) $rulebook['_binding']['sha256'],
            'source_warnings'          => $dossier['warnings'],
        );
    }

    private function analyse_feature( array $feature, array $rulebook ) {
        $facts    = array();
        $statuses = array();

        foreach ( $feature['cells'] as $cell ) {
            foreach ( isset( $cell['facts'] ) ? (array) $cell['facts'] : array() as $fact ) {
                $facts[] = $fact;
                $statuses[] = isset( $fact['fact_status'] ) ? (string) $fact['fact_status'] : '';
            }
        }

        if ( empty( $facts ) ) {
            return new WP_Error( 'UPC_FEATURE_FACTS_EMPTY', 'Declared comparison feature has no facts.' );
        }

        if ( in_array( 'SOURCE_CONFLICT', $statuses, true ) ) {
            return array(
                'meaning' => 'Für dieses Merkmal ist keine belastbare Eignungsableitung möglich, weil mindestens eine Herstellerquelle widersprüchliche Angaben enthält.',
                'explanation' => '',
                'pros_by_position' => array(),
                'cons_by_position' => array(),
                'need_fit' => array(),
            );
        }

        if ( in_array( 'CONFIGURATION_DEPENDENT', $statuses, true ) ) {
            return array(
                'meaning' => 'Dieses Merkmal hängt laut Quellenlage von der konkreten Konfiguration ab. Daraus wird keine pauschale Präferenz abgeleitet.',
                'explanation' => '',
                'pros_by_position' => array(),
                'cons_by_position' => array(),
                'need_fit' => array(),
            );
        }

        if ( in_array( 'NOT_IN_SOURCE', $statuses, true ) ) {
            return array(
                'meaning' => 'Für mindestens ein Produkt fehlt die Angabe in der verwendeten Herstellerquelle. Deshalb wird daraus kein Vorteil oder Nachteil abgeleitet.',
                'explanation' => '',
                'pros_by_position' => array(),
                'cons_by_position' => array(),
                'need_fit' => array(),
            );
        }

        $signatures = array();
        foreach ( $feature['cells'] as $cell ) {
            $signatures[] = UPC_Rulebook::cell_signature( $cell );
        }

        if ( count( array_unique( $signatures ) ) === 1 ) {
            return array(
                'meaning' => 'Nach den dokumentierten Herstellerangaben ergibt sich bei diesem Merkmal kein relevanter Unterschied.',
                'explanation' => '',
                'pros_by_position' => array(),
                'cons_by_position' => array(),
                'need_fit' => array(),
            );
        }

        return UPC_Rulebook::resolve_exact( $rulebook, $feature );
    }

    private function render_html( array $dossier, array $rows, array $pros, array $cons, array $needs ) {
        $subjects = $dossier['subjects'];
        $out = array();

        $out[] = '<p class="upc-intro">Dieser Vergleich stellt ausschließlich die gebundenen Herstellerfakten und die vorab freigegebenen Entscheidungszuordnungen gegenüber.</p>';

        $out[] = '<h2>Vergleich auf einen Blick</h2>';
        $out[] = '<table class="upc-comparison-table">';
        $out[] = '<thead><tr><th>Merkmal</th>';
        foreach ( $subjects as $subject ) {
            $out[] = '<th>' . esc_html( $this->subject_name( $subject ) ) . '</th>';
        }
        $out[] = '<th>Bedeutung für die Entscheidung</th></tr></thead><tbody>';

        foreach ( $rows as $row ) {
            $out[] = '<tr><th scope="row">' . esc_html( $row['label'] ) . '</th>';
            foreach ( $row['cells'] as $cell ) {
                $out[] = '<td>' . esc_html( $this->display_cell( $cell ) ) . '</td>';
            }
            $out[] = '<td>' . esc_html( $row['meaning'] ) . '</td></tr>';
        }
        $out[] = '</tbody></table>';

        $out[] = '<h2>Die entscheidenden Unterschiede</h2>';
        $has_explanation = false;
        foreach ( $rows as $row ) {
            if ( '' === trim( $row['explanation'] ) ) {
                continue;
            }
            $has_explanation = true;
            $out[] = '<h3>' . esc_html( $row['label'] ) . '</h3>';
            $out[] = '<p>' . esc_html( $row['explanation'] ) . '</p>';
        }
        if ( ! $has_explanation ) {
            $out[] = '<p>Alle freigegebenen Entscheidungszuordnungen stehen bereits vollständig in der Vergleichstabelle. Zusätzliche Deutungen werden nicht ergänzt.</p>';
        }

        $out[] = '<h2>Vor- und Nachteile im direkten Vergleich</h2>';
        $out[] = '<table class="upc-pros-cons-table"><thead><tr><th>Produkt</th><th>Vorteile</th><th>Nachteile</th></tr></thead><tbody>';
        foreach ( $subjects as $subject ) {
            $position = (int) $subject['position'];
            $out[] = '<tr>';
            $out[] = '<th scope="row">' . esc_html( $this->subject_name( $subject ) ) . '</th>';
            $out[] = '<td>' . esc_html( empty( $pros[ $position ] ) ? 'Keine freigegebenen Vorteile vorhanden.' : implode( '; ', array_unique( $pros[ $position ] ) ) ) . '</td>';
            $out[] = '<td>' . esc_html( empty( $cons[ $position ] ) ? 'Keine freigegebenen Nachteile vorhanden.' : implode( '; ', array_unique( $cons[ $position ] ) ) ) . '</td>';
            $out[] = '</tr>';
        }
        $out[] = '</tbody></table>';

        $out[] = '<h2>Welches Produkt passt zu welchem Bedarf?</h2>';
        if ( empty( $needs ) ) {
            $out[] = '<p>Für diesen Vergleich sind keine freigegebenen Bedarfszuordnungen vorhanden.</p>';
        } else {
            $out[] = '<ul>';
            foreach ( $needs as $need ) {
                $names = array();
                foreach ( $need['positions'] as $position ) {
                    foreach ( $subjects as $subject ) {
                        if ( (int) $subject['position'] === (int) $position ) {
                            $names[] = $this->subject_name( $subject );
                        }
                    }
                }
                $out[] = '<li><strong>' . esc_html( $need['need'] ) . ':</strong> ' . esc_html( implode( ', ', $names ) ) . ' – ' . esc_html( $need['reason'] ) . '</li>';
            }
            $out[] = '</ul>';
        }

        $out[] = '<h2>Hinweise zur Quellenlage</h2>';
        $warning_labels = array();
        foreach ( $dossier['warnings'] as $warning ) {
            if ( empty( $warning['fact_key'] ) ) {
                continue;
            }
            foreach ( $rows as $row ) {
                if ( $row['fact_key'] === $warning['fact_key'] ) {
                    $warning_labels[ $warning['fact_key'] ] = $row['label'];
                }
            }
        }

        if ( empty( $warning_labels ) ) {
            $out[] = '<p>Für die gebundenen Pflichtmerkmale liegen keine dokumentierten Quellenwarnungen vor.</p>';
        } else {
            $out[] = '<p>Bei folgenden Merkmalen ist die Herstellerquellenlage unvollständig, widersprüchlich oder konfigurationsabhängig: ' . esc_html( implode( ', ', array_values( $warning_labels ) ) ) . '. Diese Punkte werden nicht als Vorteil oder Nachteil gewertet.</p>';
        }

        $out[] = '<h2>Fazit</h2>';
        if ( empty( $needs ) ) {
            $out[] = '<p>Es gibt keinen pauschalen Sieger. Für diesen Vergleich sind keine freigegebenen Bedarfszuordnungen vorhanden.</p>';
        } else {
            $summary = array();
            foreach ( $needs as $need ) {
                $names = array();
                foreach ( $need['positions'] as $position ) {
                    foreach ( $subjects as $subject ) {
                        if ( (int) $subject['position'] === (int) $position ) {
                            $names[] = $this->subject_name( $subject );
                        }
                    }
                }
                $summary[] = $need['need'] . ': ' . implode( ', ', $names );
            }
            $out[] = '<p>Es gibt keinen pauschalen Sieger. Die freigegebenen Bedarfszuordnungen lauten: ' . esc_html( implode( '; ', $summary ) ) . '.</p>';
        }

        return implode( "\n", $out );
    }

    private function subject_name( array $subject ) {
        if ( UPK_Repository::SUBJECT_VARIANT === $subject['subject_type'] ) {
            return trim( $subject['manufacturer'] . ' ' . $subject['model_name'] . ' – ' . $subject['variant_name'] );
        }
        return trim( $subject['manufacturer'] . ' ' . $subject['model_name'] );
    }

    private function display_cell( array $cell ) {
        $facts = isset( $cell['facts'] ) ? (array) $cell['facts'] : array();
        $parts = array();

        foreach ( $facts as $fact ) {
            $status = isset( $fact['fact_status'] ) ? (string) $fact['fact_status'] : '';
            $value  = isset( $fact['fact_value'] ) ? trim( (string) $fact['fact_value'] ) : '';
            $unit   = isset( $fact['unit'] ) ? trim( (string) $fact['unit'] ) : '';

            if ( 'NOT_IN_SOURCE' === $status ) {
                $parts[] = 'In der verwendeten Herstellerquelle nicht angegeben';
            } elseif ( 'SOURCE_CONFLICT' === $status ) {
                $parts[] = 'Quellenkonflikt: ' . $value;
            } elseif ( 'CONFIGURATION_DEPENDENT' === $status ) {
                $parts[] = 'Konfigurationsabhängig: ' . $value;
            } elseif ( 'VERIFIED' === $status ) {
                $parts[] = trim( $value . ( '' !== $unit ? ' ' . $unit : '' ) );
            } else {
                return 'BLOCKED: Unbekannter Faktenstatus';
            }
        }

        return implode( ' / ', $parts );
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
