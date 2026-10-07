<?php
/**
 * Regression gate for the ADCELL banner import basis.
 * No WordPress bootstrap required: source-contract assertions only.
 */

$root = dirname(__DIR__, 2) . '/current/affiliate-portal-router';
$auto = (string) file_get_contents($root . '/includes/trait-ppar-automation-suite.php');
$library = (string) file_get_contents($root . '/includes/trait-ppar-creative-library.php');
$output = (string) file_get_contents($root . '/includes/trait-ppar-output-objects.php');
$main = (string) file_get_contents($root . '/pferdeportal-affiliate-router.php');

$errors = array();
$must = static function ($needle, $label) use (&$errors, $auto) {
    if (strpos($auto, $needle) === false) {
        $errors[] = 'missing:' . $label;
    }
};
$mustNot = static function ($needle, $label) use (&$errors, $auto) {
    if (strpos($auto, $needle) !== false) {
        $errors[] = 'forbidden:' . $label;
    }
};

$start = strpos($auto, 'private function automation_adcell_banner_rows');
$end = strpos($auto, 'private function automation_adcell_deeplink_rows', $start === false ? 0 : $start);
if ($start === false || $end === false || $end <= $start) {
    $errors[] = 'banner_function_missing';
    $banner = '';
} else {
    $banner = substr($auto, $start, $end - $start);
}

foreach (array(
    'adcell_api_v2_promotion_categories($program_id)' => 'category_endpoint_is_used',
    "'adcell_promotion_categories_unavailable'" => 'category_failure_is_fail_closed',
    "isset(\$promotion_categories[\$category_id])" => 'category_id_is_resolved_to_name',
    "'provider_raw_json'=>\$provider_raw_json" => 'full_provider_payload_is_preserved',
    "'provider_raw_sha256'=>hash('sha256', \$provider_raw_json)" => 'raw_payload_integrity_hash',
    "'title_source'=>\$title_source" => 'title_provenance_is_preserved',
    "array('bannerName','promotionName','title','name')" => 'provider_title_fields_are_used_only_when_present',
) as $needle => $label) {
    if (strpos($banner, $needle) === false) {
        $errors[] = 'missing:' . $label;
    }
}

if (strpos($banner, "'creative_title'=>sanitize_text_field((string) \$program_name . ' Banner '") !== false) {
    $errors[] = 'forbidden:synthetic_banner_title_used_as_provider_title';
}
if (strpos($library, "'creative_import_provider_raw'") === false) {
    $errors[] = 'missing:adcell_raw_payload_fail_closed';
}
if (strpos($output, "title_evidence") === false
    || strpos($output, "provider_missing") === false) {
    $errors[] = 'missing:synthetic_display_title_excluded_from_evidence';
}

// Frontend-Hardlock: Der neue Basisnachlauf ist ausschließlich admin-/workergebunden.
// Die öffentliche Output-Schicht darf niemals direkt ADCELL-Provider-HTTP aufrufen.
if (strpos($main, "add_action('admin_init', array(\$this, 'maybe_upgrade_adcell_banner_import_basis_v672199')") === false
    || strpos($main, "add_action('ppar_v672199_adcell_banner_basis_resync', array(\$this, 'run_v672199_adcell_banner_basis_resync')") === false) {
    $errors[] = 'missing:adcell_basis_admin_worker_binding';
}
if (strpos($output, 'adcell_api_v2_') !== false
    || stripos($output, 'api.adcell') !== false) {
    $errors[] = 'forbidden:adcell_provider_http_in_output_runtime';
}

// Runtime-Hardlock: Automatische Creative-Library-Banner duerfen nur dann
// Kandidaten sein, wenn ihre bereits gespeicherte Zielkante zum Kontext passt.
// Ein unpassender/fehlender Target-Match darf weder als allgemeiner noch als
// technischer Fallback wieder in den automatischen Pool gelangen.
$rank_start = strpos($main, 'private function campaign_match_rank');
$rank_end = strpos($main, 'private function slot_required_creative_type', $rank_start === false ? 0 : $rank_start);
$rank_fn = ($rank_start !== false && $rank_end !== false && $rank_end > $rank_start)
    ? substr($main, $rank_start, $rank_end - $rank_start) : '';
$library_gate_pos = strpos($rank_fn, "\$library_banner =");
$breed_fallback_pos = strpos($rank_fn, "Pferderassen ohne exakte Zielkante");
if ($rank_fn === ''
    || $library_gate_pos === false
    || strpos($rank_fn, "sanitize_key((string)(\$campaign['source']??'')) === 'output_object_v4'", $library_gate_pos) === false
    || strpos($rank_fn, 'if (is_array($automation_rank)) { return $automation_rank; }', $library_gate_pos) === false
    || strpos($rank_fn, 'return null;', $library_gate_pos) === false
    || ($breed_fallback_pos !== false && $library_gate_pos > $breed_fallback_pos)) {
    $errors[] = 'missing:stored_target_match_is_automatic_banner_eligibility_gate';
}
$library_gate_end = $breed_fallback_pos !== false ? $breed_fallback_pos : strlen($rank_fn);
$library_gate = $library_gate_pos !== false ? substr($rank_fn, $library_gate_pos, max(0, $library_gate_end - $library_gate_pos)) : '';
if (strpos($library_gate, 'Gespeicherter allgemeiner Banner-Fallback') !== false
    || strpos($library_gate, 'technisch gueltiger letzter Fallback') !== false) {
    $errors[] = 'forbidden:library_banner_wrong_target_fallback';
}
$resolver_start = strpos($library, 'private function creative_library_resolve_tracking_destination_import');
$resolver_end = strpos($library, 'private function creative_library_normalize_row', $resolver_start === false ? 0 : $resolver_start);
$resolver = ($resolver_start !== false && $resolver_end !== false && $resolver_end > $resolver_start)
    ? substr($library, $resolver_start, $resolver_end - $resolver_start) : '';
if ($resolver === ''
    || strpos($resolver, '$import_context') === false
    || strpos($resolver, "defined('WP_CLI')") === false
    || strpos($resolver, 'if (!$import_context') === false) {
    $errors[] = 'missing:destination_resolution_import_context_guard';
}

// Reihenfolge-Hardlock: Für JEDEN Banner muss technische Asset-Evidence
// vor der ersten festen Zielkarte stehen.
$verify_gate_start = strpos($library, 'private function creative_library_verify_before_assign_banner');
$verify_gate_end = strpos($library, 'private function creative_library_verify_asset_row', $verify_gate_start === false ? 0 : $verify_gate_start);
$verify_gate = ($verify_gate_start !== false && $verify_gate_end !== false && $verify_gate_end > $verify_gate_start)
    ? substr($library, $verify_gate_start, $verify_gate_end - $verify_gate_start) : '';
if ($verify_gate === ''
    || strpos($verify_gate, "creative_type'] ?? '')) === 'banner'") === false
    || strpos($verify_gate, "array('direct','manual')") !== false) {
    $errors[] = 'missing:all_banners_verify_before_assign';
}

$import_start = strpos($auto, 'private function automation_import_rows');
$import_end = strpos($auto, 'private function automation_merge_counts', $import_start === false ? 0 : $import_start);
$import_fn = ($import_start !== false && $import_end !== false && $import_end > $import_start)
    ? substr($auto, $import_start, $import_end - $import_start) : '';
$import_verify_pos = strpos($import_fn, '$dimension_state=');
$import_assign_pos = strpos($import_fn, 'output_assign_banner_targets_from_destination_once($stored_row)');
if ($import_fn === '' || $import_verify_pos === false || $import_assign_pos === false || $import_verify_pos > $import_assign_pos) {
    $errors[] = 'missing:automation_asset_gate_before_target_assignment';
}

$reconcile_start = strpos($auto, 'public function run_v672195_banner_reconcile');
$reconcile_end = strpos($auto, 'public function maybe_upgrade_adcell_banner_import_basis_v672199', $reconcile_start === false ? 0 : $reconcile_start);
$reconcile_fn = ($reconcile_start !== false && $reconcile_end !== false && $reconcile_end > $reconcile_start)
    ? substr($auto, $reconcile_start, $reconcile_end - $reconcile_start) : '';
$reconcile_verify_pos = strpos($reconcile_fn, '$verified =');
$reconcile_gate_pos = strpos($reconcile_fn, 'if (!$verified)');
$reconcile_assign_pos = strpos($reconcile_fn, '$mapped = $this->output_assign_banner_targets_from_destination_once($row)');
if ($reconcile_fn === '' || $reconcile_verify_pos === false || $reconcile_gate_pos === false || $reconcile_assign_pos === false
    || $reconcile_verify_pos > $reconcile_gate_pos || $reconcile_gate_pos > $reconcile_assign_pos) {
    $errors[] = 'missing:reconcile_asset_gate_before_target_assignment';
}

$resync_start = strpos($auto, 'public function run_v672199_adcell_banner_basis_resync');
$resync_end = strpos($auto, 'public function maybe_upgrade_adcell_destination_url_v672189', $resync_start === false ? 0 : $resync_start);
$resync_fn = ($resync_start !== false && $resync_end !== false && $resync_end > $resync_start)
    ? substr($auto, $resync_start, $resync_end - $resync_start) : '';
if ($resync_fn === ''
    || strpos($resync_fn, "'waiting_assets'") === false
    || strpos($resync_fn, 'automation_has_pending_adcell_assets()') === false
    || strpos($resync_fn, "'ready_reconcile'") === false) {
    $errors[] = 'missing:basis_resync_waits_for_assets';
}

if (strpos($library, 'payload NOT LIKE \'%\"_dimension_state\":\"failed\"%\'') === false
    || strpos($auto, 'payload NOT LIKE \'%\"_dimension_state\":\"failed\"%\'') === false) {
    $errors[] = 'missing:failed_assets_are_terminal_not_pending_forever';
}

$selection_start = strpos($library, 'public function handle_creative_library_selection');
$selection_end = strpos($library, 'private function creative_library_slot_filter_options', $selection_start === false ? 0 : $selection_start);
$selection_fn = ($selection_start !== false && $selection_end !== false && $selection_end > $selection_start)
    ? substr($library, $selection_start, $selection_end - $selection_start) : '';
$selection_verify_pos = strpos($selection_fn, '$asset_verified =');
$selection_assign_pos = strpos($selection_fn, 'output_assign_banner_targets_from_destination_once($row)');
if ($selection_fn === '' || $selection_verify_pos === false || $selection_assign_pos === false || $selection_verify_pos > $selection_assign_pos) {
    $errors[] = 'missing:manual_family_asset_gate_before_target_assignment';
}

$upsert_start = strpos($library, 'private function creative_library_upsert');
$upsert_end = strpos($library, 'private function creative_library_import_body', $upsert_start === false ? 0 : $upsert_start);
$upsert_fn = ($upsert_start !== false && $upsert_end !== false && $upsert_end > $upsert_start)
    ? substr($library, $upsert_start, $upsert_end - $upsert_start) : '';
if ($upsert_fn === ''
    || strpos($upsert_fn, "\$existing_dimension_state === 'failed'") === false
    || strpos($upsert_fn, "\$incoming_payload['_dimension_state'] = 'pending'") === false
    || strpos($upsert_fn, "\$asset_retry_reset = true") === false
    || strpos($upsert_fn, "return (\$destination_changed || \$asset_retry_reset) ? 'updated' : 'unchanged'") === false) {
    $errors[] = 'missing:failed_asset_reopened_only_by_fresh_reimport';
}

if ($errors) {
    fwrite(STDERR, "ADCELL_BANNER_IMPORT_BASIS_FAIL\n" . implode("\n", $errors) . "\n");
    exit(1);
}
echo "PASS category endpoint used once per programme\n";
echo "PASS category id resolved to authoritative category name\n";
echo "PASS full provider banner payload preserved\n";
echo "PASS provider title provenance preserved\n";
echo "PASS synthetic banner title no longer used as provider evidence\n";
echo "PASS missing or corrupt ADCELL raw provider basis is fail-closed\n";
echo "PASS synthetic display fallback is excluded from banner evidence\n";
echo "PASS ADCELL basis sync is admin-worker bound and output runtime contains no provider HTTP\n";
echo "PASS automatic Creative-Library banners require a matching stored target before distribution\n";
echo "PASS destination resolver is guarded to import/background contexts\n";
echo "PASS every banner path verifies the asset before target assignment\n";
echo "PASS 6.72.199 basis resync waits for asset verification before reconcile\n";
echo "PASS failed assets stay fail-closed without endless pending loop\n";
echo "PASS later provider reimport reopens a failed asset for a new technical check\n";
echo "ADCELL_BANNER_IMPORT_BASIS_COMPLETE\n";
