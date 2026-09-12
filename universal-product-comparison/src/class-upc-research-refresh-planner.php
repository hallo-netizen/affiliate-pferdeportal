<?php

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

/**
 * Read-only research handoff for due product re-verification.
 *
 * No scheduler, provider, queue table or data mutation. The plan is rebuilt
 * from current product knowledge + the project maintenance policy on demand.
 */
class UPC_Research_Refresh_Planner {
    private $knowledge;
    private $product_maintenance;
    private $comparison_maintenance;

    public function __construct( $knowledge, $product_maintenance, $comparison_maintenance ) {
        $this->knowledge = $knowledge;
        $this->product_maintenance = $product_maintenance;
        $this->comparison_maintenance = $comparison_maintenance;
    }

    public function build( $project_key = 'pferde-atelier', $as_of_utc = '', $limit_per_group = 500 ) {
        $project_key = sanitize_key( $project_key );
        if ( '' === $project_key ) {
            return new WP_Error( 'UPC_REFRESH_PROJECT_KEY_MISSING', 'Project key is required.' );
        }

        $policy_path = dirname( __DIR__ ) . '/config/' . $project_key . '/maintenance-groups.json';
        $policy = $this->load_policy( $policy_path, $project_key );
        if ( is_wp_error( $policy ) ) {
            return $policy;
        }

        $as_of = $this->normalize_datetime( '' === trim( (string) $as_of_utc ) ? gmdate( 'Y-m-d H:i:s' ) : $as_of_utc );
        if ( is_wp_error( $as_of ) ) {
            return $as_of;
        }

        $limit_per_group = max( 1, min( 500, absint( $limit_per_group ) ) );
        $tasks = array();
        $group_summaries = array();

        foreach ( $policy['groups'] as $group ) {
            $key = (string) $group['product_group_key'];
            $months = (int) $group['refresh_months'];
            $cutoff = $this->subtract_calendar_months( $as_of, $months );
            if ( is_wp_error( $cutoff ) ) {
                return $cutoff;
            }

            $ids = $this->product_maintenance->products_due_for_group_review( $key, $cutoff, $limit_per_group );
            if ( is_wp_error( $ids ) ) {
                return $ids;
            }

            $ids = array_values( array_map( 'absint', (array) $ids ) );
            $group_due = 0;
            foreach ( $ids as $product_id ) {
                $bundle = $this->knowledge->get_product_bundle( $product_id );
                if ( is_wp_error( $bundle ) ) {
                    return $bundle;
                }

                if ( $key !== (string) ( $bundle['product_group_key'] ?? '' ) ) {
                    return new WP_Error( 'UPC_REFRESH_PRODUCT_GROUP_MISMATCH', 'Due product does not match the maintenance group.' );
                }

                $manufacturer = trim( (string) ( $bundle['manufacturer'] ?? '' ) );
                $model_name = trim( (string) ( $bundle['model_name'] ?? '' ) );
                $source_url = trim( (string) ( $bundle['manufacturer_product_url'] ?? '' ) );
                $last_verified_at = trim( (string) ( $bundle['last_verified_at'] ?? '' ) );
                if ( '' === $manufacturer || '' === $model_name || '' === $source_url || '' === $last_verified_at ) {
                    return new WP_Error( 'UPC_REFRESH_PRODUCT_BINDING_INCOMPLETE', 'Due product identity or manufacturer source is incomplete.' );
                }

                $affected = $this->comparison_maintenance->affected_comparisons_for_product( $product_id );
                if ( is_wp_error( $affected ) ) {
                    return $affected;
                }

                $tasks[] = array(
                    'task_type' => 'PRODUCT_REVERIFY',
                    'product_id' => $product_id,
                    'product_group_key' => $key,
                    'manufacturer' => $manufacturer,
                    'model_name' => $model_name,
                    'generation' => (string) ( $bundle['generation'] ?? '' ),
                    'lifecycle_status' => (string) ( $bundle['lifecycle_status'] ?? 'UNKNOWN' ),
                    'manufacturer_product_url' => $source_url,
                    'last_verified_at' => $last_verified_at,
                    'due_cutoff_utc' => $cutoff,
                    'refresh_months' => $months,
                    'required_additional_contracts' => array_values( (array) ( $group['required_additional_contracts'] ?? array() ) ),
                    'affected_comparison_ids' => array_values( array_map( 'intval', (array) $affected ) ),
                );
                $group_due++;
            }

            $group_summaries[] = array(
                'product_group_key' => $key,
                'refresh_months' => $months,
                'due_cutoff_utc' => $cutoff,
                'due_product_count' => $group_due,
                'possibly_truncated' => count( $ids ) >= $limit_per_group,
            );
        }

        usort( $tasks, function( $a, $b ) {
            $cmp = strcmp( (string) $a['last_verified_at'], (string) $b['last_verified_at'] );
            return 0 !== $cmp ? $cmp : ( (int) $a['product_id'] <=> (int) $b['product_id'] );
        } );

        return array(
            'schema_version' => '1',
            'contract' => 'UPC_PRODUCT_RESEARCH_REFRESH_PLAN_V1',
            'project_key' => $project_key,
            'as_of_utc' => $as_of,
            'maintenance_policy_sha256' => hash_file( 'sha256', $policy_path ),
            'market_gate' => $policy['market_gate'],
            'limit_per_group' => $limit_per_group,
            'group_count' => count( $policy['groups'] ),
            'due_product_count' => count( $tasks ),
            'groups' => $group_summaries,
            'tasks' => $tasks,
        );
    }

    private function load_policy( $path, $project_key ) {
        if ( ! is_file( $path ) ) {
            return new WP_Error( 'UPC_MAINTENANCE_POLICY_MISSING', 'Maintenance policy is missing.' );
        }
        $data = json_decode( file_get_contents( $path ), true );
        if ( ! is_array( $data )
            || '1' !== (string) ( $data['schema_version'] ?? '' )
            || $project_key !== (string) ( $data['project_key'] ?? '' )
            || ! isset( $data['market_gate'] )
            || ! is_array( $data['market_gate'] )
            || empty( $data['groups'] )
            || ! is_array( $data['groups'] )
        ) {
            return new WP_Error( 'UPC_MAINTENANCE_POLICY_INVALID', 'Maintenance policy is invalid.' );
        }

        $seen = array();
        foreach ( $data['groups'] as $group ) {
            $key = sanitize_key( (string) ( $group['product_group_key'] ?? '' ) );
            $months = (int) ( $group['refresh_months'] ?? 0 );
            if ( '' === $key || ! in_array( $months, array( 6, 12 ), true ) || isset( $seen[ $key ] ) ) {
                return new WP_Error( 'UPC_MAINTENANCE_POLICY_GROUP_INVALID', 'Maintenance group is invalid or duplicated.' );
            }
            $seen[ $key ] = true;
        }

        return $data;
    }

    private function normalize_datetime( $value ) {
        $timestamp = strtotime( (string) $value );
        if ( false === $timestamp ) {
            return new WP_Error( 'UPC_REFRESH_DATETIME_INVALID', 'Refresh reference datetime is invalid.' );
        }
        return gmdate( 'Y-m-d H:i:s', $timestamp );
    }

    private function subtract_calendar_months( $datetime, $months ) {
        try {
            $dt = new DateTimeImmutable( $datetime, new DateTimeZone( 'UTC' ) );
            $months = absint( $months );
            $year = (int) $dt->format( 'Y' );
            $month = (int) $dt->format( 'n' );
            $day = (int) $dt->format( 'j' );

            $index = ( $year * 12 + ( $month - 1 ) ) - $months;
            $target_year = (int) floor( $index / 12 );
            $target_month = ( $index % 12 ) + 1;
            if ( $target_month <= 0 ) {
                $target_month += 12;
                $target_year--;
            }

            $last_day = cal_days_in_month( CAL_GREGORIAN, $target_month, $target_year );
            $target_day = min( $day, $last_day );

            return $dt
                ->setDate( $target_year, $target_month, $target_day )
                ->format( 'Y-m-d H:i:s' );
        } catch ( Exception $e ) {
            return new WP_Error( 'UPC_REFRESH_DATETIME_INVALID', 'Refresh cutoff could not be calculated.' );
        }
    }
}
