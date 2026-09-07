<?php

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

class UPC_Writer {
    private $repository;

    public function __construct( $repository ) {
        $this->repository = $repository;
    }

    public function build_draft( $comparison_id, array $decision_rules = array() ) {
        $dossier = $this->repository->build_comparison_dossier( $comparison_id );
        if ( is_wp_error( $dossier ) ) {
            return $dossier;
        }

        $subjects = $dossier['subjects'];
        $missing_rules = array();
        $rows = array();
        $pros = array();
        $cons = array();
        $needs = array();

        foreach ( $subjects as $subject ) {
            $pros[ (int) $subject['position'] ] = array();
            $cons[ (int) $subject['position'] ] = array();
        }

        foreach ( $dossier['features'] as $feature ) {
            $analysis = $this->analyse_feature( $feature, $decision_rules );

            if ( is_wp_error( $analysis ) ) {
                if ( 'UPC_DECISION_RULE_MISSING' === $analysis->get_error_code() ) {
                    $missing_rules[] = $feature['fact_key'];
                    continue;
                }
                return $analysis;
            }

            $rows[] = array(
                'fact_key'    => $feature['fact_key'],
                'label'       => $feature['label'],
                'cells'       => $feature['cells'],
                'meaning'     => $analysis['meaning'],
                'explanation' => isset( $analysis['explanation'] ) ? sanitize_text_field( $analysis['explanation'] ) : '',
            );

            foreach ( isset( $analysis['pros_by_position'] ) ? $analysis['pros_by_position'] : array() as $position => $items ) {
                foreach ( (array) $items as $item ) {
                    $item = sanitize_text_field( $item );
                    if ( '' !== $item ) {
                        $pros[ (int) $position ][] = $item;
                    }
                }
            }

            foreach ( isset( $analysis['cons_by_position'] ) ? $analysis['cons_by_position'] : array() as $position => $items ) {
                foreach ( (array) $items as $item ) {
                    $item = sanitize_text_field( $item );
                    if ( '' !== $item ) {
                        $cons[ (int) $position ][] = $item;
                    }
                }
            }

            foreach ( isset( $analysis['need_fit'] ) ? $analysis['need_fit'] : array() as $need ) {
                if ( ! is_array( $need ) || empty( $need['need'] ) || empty( $need['positions'] ) || empty( $need['reason'] ) ) {
                    continue;
                }
                $needs[] = array(
                    'need'      => sanitize_text_field( $need['need'] ),
                    'positions' => array_values( array_map( 'absint', (array) $need['positions'] ) ),
                    'reason'    => sanitize_text_field( $need['reason'] ),
                );
            }
        }

        if ( ! empty( $missing_rules ) ) {
            return new WP_Error(
                'UPC_DECISION_RULE_MISSING',
                'One or more differing verified comparison facts have no approved decision rule.',
                array( 'fact_keys' => array_values( array_unique( $missing_rules ) ) )
            );
        }

        $title = ! empty( $dossier['comparison']['working_title'] )
            ? $dossier['comparison']['working_title']
            : $this->fallback_title( $subjects );

        $html = $this->render_html(
            $title,
            $dossier,
            $rows,
            $pros,
            $cons,
            $needs
        );

        return array(
            'status'              => 'DRAFT_READY_FOR_REVIEW',
            'comparison_uid'      => $dossier['comparison']['comparison_uid'],
            'title'               => $title,
            'html'                => $html,
            'decision_rows'       => $rows,
            'pros_by_position'    => $pros,
            'cons_by_position'    => $cons,
            'need_fit'            => $needs,
            'source_warnings'     => $dossier['warnings'],
            'external_link_count' => 0,
        );
    }

    private function analyse_feature( array $feature, array $decision_rules ) {
        $facts = array();
        $statuses = array();

        foreach ( $feature['cells'] as $cell ) {
            $cell_facts = isset( $cell['facts'] ) ? (array) $cell['facts'] : array();
            foreach ( $cell_facts as $fact ) {
                $facts[] = $fact;
                $statuses[] = isset( $fact['fact_status'] ) ? $fact['fact_status'] : '';
            }
        }

        if ( in_array( 'SOURCE_CONFLICT', $statuses, true ) ) {
            return array(
                'meaning' => 'Für dieses Merkmal ist keine belastbare Eignungsableitung möglich, weil mindestens eine Herstellerquelle widersprüchliche Angaben enthält.',
            );
        }

        if ( in_array( 'CONFIGURATION_DEPENDENT', $statuses, true ) ) {
            return array(
                'meaning' => 'Dieses Merkmal hängt laut Quellenlage von der konkreten Konfiguration ab; daraus wird keine pauschale Präferenz abgeleitet.',
            );
        }

        if ( in_array( 'NOT_IN_SOURCE', $statuses, true ) ) {
            return array(
                'meaning' => 'Für mindestens ein Produkt fehlt die Angabe in der verwendeten Herstellerquelle. Deshalb wird daraus kein Vorteil oder Nachteil abgeleitet.',
            );
        }

        if ( empty( $facts ) ) {
            return new WP_Error( 'UPC_FEATURE_FACTS_EMPTY', 'Comparison feature has no bound facts.' );
        }

        $normalized = array();
        foreach ( $feature['cells'] as $cell ) {
            $cell_facts = isset( $cell['facts'] ) ? (array) $cell['facts'] : array();
            $normalized[] = $this->normalize_fact_set( $cell_facts );
        }

        if ( count( array_unique( $normalized ) ) === 1 ) {
            return array(
                'meaning' => 'Nach den dokumentierten Herstellerangaben ergibt sich bei diesem Merkmal kein relevanter Unterschied.',
            );
        }

        $fact_key = $feature['fact_key'];
        if ( ! isset( $decision_rules[ $fact_key ] ) || ! is_callable( $decision_rules[ $fact_key ] ) ) {
            return new WP_Error(
                'UPC_DECISION_RULE_MISSING',
                'Differing verified values require an approved decision rule.',
                array( 'fact_key' => $fact_key )
            );
        }

        $result = call_user_func( $decision_rules[ $fact_key ], $feature );
        if ( ! is_array( $result ) || empty( $result['meaning'] ) ) {
            return new WP_Error(
                'UPC_DECISION_RULE_INVALID',
                'Approved decision rule returned no usable decision meaning.',
                array( 'fact_key' => $fact_key )
            );
        }

        $result['meaning'] = sanitize_text_field( $result['meaning'] );
        return $result;
    }

    private function normalize_fact_set( array $facts ) {
        $values = array();
        foreach ( $facts as $fact ) {
            if ( 'VERIFIED' !== ( isset( $fact['fact_status'] ) ? $fact['fact_status'] : '' ) ) {
                continue;
            }
            $values[] = strtolower(
                trim(
                    ( isset( $fact['fact_value'] ) ? $fact['fact_value'] : '' ) . '|' .
                    ( isset( $fact['unit'] ) ? $fact['unit'] : '' )
                )
            );
        }
        sort( $values, SORT_STRING );
        return implode( '||', $values );
    }

    private function fallback_title( array $subjects ) {
        $names = array();
        foreach ( $subjects as $subject ) {
            $names[] = trim( $subject['manufacturer'] . ' ' . $subject['model_name'] );
        }
        return implode( ' vs. ', $names );
    }

    private function render_html( $title, array $dossier, array $rows, array $pros, array $cons, array $needs ) {
        $subjects = $dossier['subjects'];
        $out = array();

        $out[] = '<p class="upc-intro">Dieser Vergleich stellt die dokumentierten Unterschiede der ausgewählten Produkte gegenüber und ordnet sie nur dort für die Kaufentscheidung ein, wo dafür eine freigegebene Entscheidungsregel vorliegt.</p>';

        $out[] = '<h2>Vergleich auf einen Blick</h2>';
        $out[] = '<table class="upc-comparison-table">';
        $out[] = '<thead><tr><th>Merkmal</th>';
        foreach ( $subjects as $subject ) {
            $out[] = '<th>' . esc_html( trim( $subject['manufacturer'] . ' ' . $subject['model_name'] ) ) . '</th>';
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

        $explanations = array_values(
            array_filter(
                $rows,
                function( $row ) {
                    return ! empty( $row['explanation'] )
                        && trim( $row['explanation'] ) !== trim( $row['meaning'] );
                }
            )
        );

        $out[] = '<h2>Die entscheidenden Unterschiede</h2>';
        if ( empty( $explanations ) ) {
            $out[] = '<p>Die für die Entscheidung belastbar ableitbaren Unterschiede sind bereits in der Vergleichstabelle zusammengefasst. Zusätzliche Deutungen werden nicht ergänzt.</p>';
        } else {
            foreach ( $explanations as $row ) {
                $out[] = '<h3>' . esc_html( $row['label'] ) . '</h3>';
                $out[] = '<p>' . esc_html( $row['explanation'] ) . '</p>';
            }
        }

        $out[] = '<h2>Vor- und Nachteile im direkten Vergleich</h2>';
        $out[] = '<table class="upc-pros-cons-table"><thead><tr><th>Produkt</th><th>Vorteile</th><th>Nachteile</th></tr></thead><tbody>';
        foreach ( $subjects as $subject ) {
            $position = (int) $subject['position'];
            $name = trim( $subject['manufacturer'] . ' ' . $subject['model_name'] );
            $out[] = '<tr>';
            $out[] = '<th scope="row">' . esc_html( $name ) . '</th>';
            $out[] = '<td>' . esc_html( empty( $pros[ $position ] ) ? 'Keine belastbaren Vorteile aus den freigegebenen Entscheidungsregeln ableitbar.' : implode( '; ', array_unique( $pros[ $position ] ) ) ) . '</td>';
            $out[] = '<td>' . esc_html( empty( $cons[ $position ] ) ? 'Keine belastbaren Nachteile aus den freigegebenen Entscheidungsregeln ableitbar.' : implode( '; ', array_unique( $cons[ $position ] ) ) ) . '</td>';
            $out[] = '</tr>';
        }
        $out[] = '</tbody></table>';

        $out[] = '<h2>Welches Produkt passt zu welchem Bedarf?</h2>';
        if ( empty( $needs ) ) {
            $out[] = '<p>Aus den derzeit freigegebenen Entscheidungsregeln lässt sich keine belastbare Bedarfspräferenz ableiten. Die Entscheidung sollte deshalb anhand der oben dokumentierten Unterschiede erfolgen.</p>';
        } else {
            $out[] = '<ul>';
            foreach ( $needs as $need ) {
                $names = array();
                foreach ( $need['positions'] as $position ) {
                    foreach ( $subjects as $subject ) {
                        if ( (int) $subject['position'] === (int) $position ) {
                            $names[] = trim( $subject['manufacturer'] . ' ' . $subject['model_name'] );
                        }
                    }
                }
                $out[] = '<li><strong>' . esc_html( $need['need'] ) . ':</strong> ' . esc_html( implode( ', ', $names ) ) . ' – ' . esc_html( $need['reason'] ) . '</li>';
            }
            $out[] = '</ul>';
        }

        if ( ! empty( $dossier['warnings'] ) ) {
            $labels = array();
            foreach ( $dossier['warnings'] as $warning ) {
                if ( ! isset( $warning['fact_key'] ) ) {
                    continue;
                }
                foreach ( $rows as $row ) {
                    if ( $row['fact_key'] === $warning['fact_key'] ) {
                        $labels[ $warning['fact_key'] ] = $row['label'];
                    }
                }
            }
            if ( ! empty( $labels ) ) {
                $out[] = '<h2>Hinweise zur Quellenlage</h2>';
                $out[] = '<p>Bei folgenden Merkmalen ist die Herstellerquellenlage unvollständig, widersprüchlich oder konfigurationsabhängig: ' . esc_html( implode( ', ', array_values( $labels ) ) ) . '. Diese Punkte werden nicht als Vorteil oder Nachteil gewertet.</p>';
            }
        }

        $out[] = '<h2>Fazit</h2>';
        if ( empty( $needs ) ) {
            $out[] = '<p>Es gibt keinen pauschalen Sieger. Aus den derzeit freigegebenen Entscheidungsregeln ergibt sich keine belastbare Bedarfspräferenz; maßgeblich bleiben die dokumentierten Unterschiede in der Tabelle.</p>';
        } else {
            $summary = array();
            foreach ( $needs as $need ) {
                $names = array();
                foreach ( $need['positions'] as $position ) {
                    foreach ( $subjects as $subject ) {
                        if ( (int) $subject['position'] === (int) $position ) {
                            $names[] = trim( $subject['manufacturer'] . ' ' . $subject['model_name'] );
                        }
                    }
                }
                $summary[] = $need['need'] . ': ' . implode( ', ', $names );
            }
            $out[] = '<p>Es gibt keinen pauschalen Sieger. Die belastbar ableitbare Zuordnung lautet: ' . esc_html( implode( '; ', $summary ) ) . '. Für andere Anforderungen entscheidet die dokumentierte Merkmalslage.</p>';
        }

        return implode( "\n", $out );
    }

    private function display_cell( array $cell ) {
        $facts = isset( $cell['facts'] ) ? (array) $cell['facts'] : array();
        if ( empty( $facts ) ) {
            return 'Keine Angabe';
        }

        $parts = array();
        foreach ( $facts as $fact ) {
            $value = isset( $fact['fact_value'] ) ? trim( $fact['fact_value'] ) : '';
            $unit  = isset( $fact['unit'] ) ? trim( $fact['unit'] ) : '';
            $status = isset( $fact['fact_status'] ) ? $fact['fact_status'] : '';

            if ( 'NOT_IN_SOURCE' === $status ) {
                $parts[] = 'In der verwendeten Herstellerquelle nicht angegeben';
            } elseif ( 'SOURCE_CONFLICT' === $status ) {
                $parts[] = 'Quellenkonflikt: ' . $value;
            } elseif ( 'CONFIGURATION_DEPENDENT' === $status ) {
                $parts[] = 'Konfigurationsabhängig: ' . $value;
            } else {
                $parts[] = trim( $value . ( '' !== $unit ? ' ' . $unit : '' ) );
            }
        }

        return implode( ' / ', array_filter( $parts ) );
    }
}
