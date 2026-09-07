<?php

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

/**
 * Pure data-rule handling. No callbacks, no AI, no network, no fallback rules.
 */
class UPC_Rulebook {
    const ARTICLE_CONTRACT_VERSION = '1';
    const RULEBOOK_SCHEMA_VERSION  = '1';

    public static function load_bound( $project_key, $ruleset_id ) {
        $project_key = sanitize_key( $project_key );
        $ruleset_id  = sanitize_key( $ruleset_id );

        if ( '' === $project_key || '' === $ruleset_id ) {
            return new WP_Error( 'UPC_RULESET_IDENTITY_MISSING', 'Project and ruleset identity are required.' );
        }

        $base = dirname( __DIR__ ) . '/config/' . $project_key;
        $manifest_path = $base . '/rulesets/manifest.json';

        if ( ! is_file( $manifest_path ) ) {
            return new WP_Error( 'UPC_RULESET_MANIFEST_MISSING', 'Bound ruleset manifest does not exist.' );
        }

        $manifest = json_decode( file_get_contents( $manifest_path ), true );
        if ( ! is_array( $manifest ) || empty( $manifest['rulesets'][ $ruleset_id ] ) ) {
            return new WP_Error( 'UPC_RULESET_NOT_BOUND', 'Ruleset is not bound in the project manifest.' );
        }

        $binding = $manifest['rulesets'][ $ruleset_id ];
        if ( empty( $binding['file'] ) || empty( $binding['sha256'] ) ) {
            return new WP_Error( 'UPC_RULESET_BINDING_INVALID', 'Ruleset binding is incomplete.' );
        }

        $path = $base . '/rulesets/' . basename( $binding['file'] );
        if ( ! is_file( $path ) ) {
            return new WP_Error( 'UPC_RULESET_FILE_MISSING', 'Bound ruleset file does not exist.' );
        }

        $actual_hash = hash_file( 'sha256', $path );
        if ( ! hash_equals( strtolower( (string) $binding['sha256'] ), strtolower( $actual_hash ) ) ) {
            return new WP_Error( 'UPC_RULESET_HASH_MISMATCH', 'Ruleset file does not match its bound hash.' );
        }

        $rulebook = json_decode( file_get_contents( $path ), true );
        if ( ! is_array( $rulebook ) ) {
            return new WP_Error( 'UPC_RULESET_JSON_INVALID', 'Ruleset JSON is invalid.' );
        }

        $rulebook['_binding'] = array(
            'project_key' => $project_key,
            'ruleset_id'  => $ruleset_id,
            'sha256'      => $actual_hash,
        );

        return $rulebook;
    }

    public static function validate_for_dossier( array $rulebook, array $dossier ) {
        $required = array(
            'schema_version',
            'ruleset_id',
            'ruleset_version',
            'article_contract_version',
            'comparison_key',
            'rules',
            '_binding',
        );

        foreach ( $required as $key ) {
            if ( ! array_key_exists( $key, $rulebook ) ) {
                return new WP_Error( 'UPC_RULEBOOK_INCOMPLETE', 'Bound rulebook is incomplete.', array( 'field' => $key ) );
            }
        }

        if ( self::RULEBOOK_SCHEMA_VERSION !== (string) $rulebook['schema_version'] ) {
            return new WP_Error( 'UPC_RULEBOOK_SCHEMA_VERSION_MISMATCH', 'Unsupported rulebook schema version.' );
        }

        if ( self::ARTICLE_CONTRACT_VERSION !== (string) $rulebook['article_contract_version'] ) {
            return new WP_Error( 'UPC_ARTICLE_CONTRACT_VERSION_MISMATCH', 'Unsupported article contract version.' );
        }

        if ( (string) $rulebook['ruleset_id'] !== (string) $rulebook['_binding']['ruleset_id'] ) {
            return new WP_Error( 'UPC_RULESET_ID_MISMATCH', 'Ruleset identity differs from manifest binding.' );
        }

        if ( (string) $rulebook['comparison_key'] !== (string) $dossier['comparison']['comparison_key'] ) {
            return new WP_Error( 'UPC_RULEBOOK_COMPARISON_MISMATCH', 'Ruleset is bound to a different comparison.' );
        }

        if ( empty( $dossier['comparison']['working_title'] ) ) {
            return new WP_Error( 'UPC_WORKING_TITLE_MISSING', 'Article title must be explicitly bound; no fallback title is allowed.' );
        }

        if ( ! is_array( $rulebook['rules'] ) ) {
            return new WP_Error( 'UPC_RULEBOOK_RULES_INVALID', 'Rules must be declarative data.' );
        }

        $known = array();
        foreach ( $dossier['features'] as $feature ) {
            $known[ $feature['fact_key'] ] = true;
        }

        foreach ( $rulebook['rules'] as $fact_key => $rule ) {
            if ( ! isset( $known[ $fact_key ] ) ) {
                return new WP_Error( 'UPC_RULEBOOK_UNKNOWN_FEATURE', 'Ruleset contains an undeclared feature.', array( 'fact_key' => $fact_key ) );
            }

            if ( ! is_array( $rule )
                || empty( $rule['expected_cell_signatures'] )
                || ! is_array( $rule['expected_cell_signatures'] )
                || empty( $rule['meaning'] )
            ) {
                return new WP_Error( 'UPC_RULEBOOK_RULE_INVALID', 'Declarative rule is incomplete.', array( 'fact_key' => $fact_key ) );
            }
        }

        return true;
    }

    public static function cell_signature( array $cell ) {
        $parts = array();

        foreach ( isset( $cell['facts'] ) ? (array) $cell['facts'] : array() as $fact ) {
            $parts[] = implode(
                '|',
                array(
                    isset( $fact['fact_status'] ) ? (string) $fact['fact_status'] : '',
                    isset( $fact['fact_value'] ) ? trim( (string) $fact['fact_value'] ) : '',
                    isset( $fact['unit'] ) ? trim( (string) $fact['unit'] ) : '',
                )
            );
        }

        sort( $parts, SORT_STRING );
        return implode( '||', $parts );
    }

    public static function resolve_exact( array $rulebook, array $feature ) {
        $fact_key = $feature['fact_key'];

        if ( ! isset( $rulebook['rules'][ $fact_key ] ) ) {
            return new WP_Error(
                'UPC_DECISION_RULE_MISSING',
                'Differing verified facts have no bound declarative rule.',
                array( 'fact_key' => $fact_key )
            );
        }

        $rule = $rulebook['rules'][ $fact_key ];
        $expected = array_values( $rule['expected_cell_signatures'] );
        $actual = array();

        foreach ( $feature['cells'] as $cell ) {
            $actual[] = self::cell_signature( $cell );
        }

        if ( $expected !== $actual ) {
            return new WP_Error(
                'UPC_DECISION_RULE_FACT_BINDING_MISMATCH',
                'Facts changed after the decision rule was approved.',
                array( 'fact_key' => $fact_key, 'expected' => $expected, 'actual' => $actual )
            );
        }

        return array(
            'meaning'          => sanitize_text_field( $rule['meaning'] ),
            'explanation'      => isset( $rule['explanation'] ) ? sanitize_text_field( $rule['explanation'] ) : '',
            'pros_by_position' => isset( $rule['pros_by_position'] ) ? self::sanitize_position_texts( $rule['pros_by_position'] ) : array(),
            'cons_by_position' => isset( $rule['cons_by_position'] ) ? self::sanitize_position_texts( $rule['cons_by_position'] ) : array(),
            'need_fit'         => isset( $rule['need_fit'] ) ? self::sanitize_need_fit( $rule['need_fit'] ) : array(),
        );
    }

    private static function sanitize_position_texts( array $input ) {
        $out = array();
        foreach ( $input as $position => $texts ) {
            $position = absint( $position );
            if ( $position < 1 ) {
                continue;
            }
            foreach ( (array) $texts as $value ) {
                $value = sanitize_text_field( $value );
                if ( '' !== $value ) {
                    $out[ $position ][] = $value;
                }
            }
        }
        return $out;
    }

    private static function sanitize_need_fit( array $input ) {
        $out = array();
        foreach ( $input as $row ) {
            if ( ! is_array( $row ) || empty( $row['need'] ) || empty( $row['positions'] ) || empty( $row['reason'] ) ) {
                continue;
            }
            $out[] = array(
                'need'      => sanitize_text_field( $row['need'] ),
                'positions' => array_values( array_map( 'absint', (array) $row['positions'] ) ),
                'reason'    => sanitize_text_field( $row['reason'] ),
            );
        }
        return $out;
    }
}
