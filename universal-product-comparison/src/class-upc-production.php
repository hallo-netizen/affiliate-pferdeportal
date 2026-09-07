<?php

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

/**
 * Single Door: the only supported production entry point.
 *
 * PREPARED -> QUARANTINED_RENDERED -> VALIDATED -> DRAFT_READY_FOR_REVIEW.
 * No alternate route and no publish action.
 */
class UPC_Production {
    const CONTRACT = 'UPC_SINGLE_DOOR_V1';

    private $repository;

    public function __construct( $repository ) {
        $this->repository = $repository;
    }

    public function execute( $comparison_id, $project_key, $ruleset_id ) {
        $rulebook = UPC_Rulebook::load_bound( $project_key, $ruleset_id );
        if ( is_wp_error( $rulebook ) ) {
            return $rulebook;
        }

        $renderer = new UPC_Writer( $this->repository );
        $quarantined = $renderer->render_quarantined( $comparison_id, $rulebook );
        if ( is_wp_error( $quarantined ) ) {
            return $quarantined;
        }

        $validation = UPC_Validator::validate_quarantined_draft( $quarantined );
        if ( is_wp_error( $validation ) ) {
            return $validation;
        }

        $receipt_payload = array(
            'contract'                 => self::CONTRACT,
            'comparison_uid'           => $quarantined['comparison_uid'],
            'input_hash'               => $quarantined['input_hash'],
            'output_hash'              => $quarantined['output_hash'],
            'renderer_version'         => $quarantined['renderer_version'],
            'article_contract_version' => $quarantined['article_contract_version'],
            'ruleset_id'               => $quarantined['ruleset_id'],
            'ruleset_version'          => $quarantined['ruleset_version'],
            'ruleset_sha256'           => $quarantined['ruleset_sha256'],
            'publish_allowed'          => false,
        );

        $receipt_hash = hash( 'sha256', $this->canonical_json( $receipt_payload ) );

        $quarantined['status'] = 'DRAFT_READY_FOR_REVIEW';
        $quarantined['production_contract'] = self::CONTRACT;
        $quarantined['receipt_hash'] = $receipt_hash;
        $quarantined['publish_allowed'] = false;

        return $quarantined;
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
