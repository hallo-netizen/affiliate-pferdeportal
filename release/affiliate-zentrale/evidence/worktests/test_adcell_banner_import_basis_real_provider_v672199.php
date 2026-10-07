<?php
/**
 * REQUIRED real-provider gate for the 6.72.199 ADCELL banner import basis.
 *
 * Must run only on an isolated WordPress/MariaDB test host with real ADCELL
 * credentials supplied through environment variables. Never runs on live.
 * All test-row and credential DB mutations are wrapped in one transaction and
 * rolled back before exit.
 */

if (!class_exists('Pferdeportal_Affiliate_Router')) {
    fwrite(STDERR, "FAIL plugin_not_loaded\n");
    exit(2);
}
if (Pferdeportal_Affiliate_Router::VERSION !== '6.72.199') {
    fwrite(STDERR, "FAIL wrong_version " . Pferdeportal_Affiliate_Router::VERSION . "\n");
    exit(2);
}
if ((string)getenv('PPAR_REAL_PROVIDER_GATE') !== '1') {
    fwrite(STDERR, "FAIL real_provider_gate_not_explicitly_enabled\n");
    exit(2);
}

$host = strtolower((string)wp_parse_url(home_url('/'), PHP_URL_HOST));
if ($host === 'pferde-atelier.de' || $host === 'www.pferde-atelier.de') {
    fwrite(STDERR, "FAIL real_provider_gate_forbidden_on_live_host\n");
    exit(2);
}

$username = trim((string)getenv('PPAR_ADCELL_USERNAME'));
$password = (string)getenv('PPAR_ADCELL_PASSWORD');
$program_csv = trim((string)getenv('PPAR_ADCELL_PROGRAM_IDS'));
$program_ids = array_values(array_unique(array_filter(array_map('absint', preg_split('/[,;\s]+/', $program_csv)))));
if ($username === '' || $password === '' || !$program_ids) {
    fwrite(STDERR, "FAIL real_adcell_credentials_or_program_ids_missing\n");
    exit(2);
}

global $wpdb;
$in_tx = false;
$rollback = static function() use (&$in_tx, $wpdb) {
    if ($in_tx) {
        $wpdb->query('ROLLBACK');
        $in_tx = false;
    }
};
$fail = static function($message) use ($rollback) {
    $rollback();
    fwrite(STDERR, "FAIL " . $message . "\n");
    exit(1);
};
$ok = static function($message) {
    echo "PASS " . $message . "\n";
};

$o = Pferdeportal_Affiliate_Router::instance();
foreach (array('maybe_install_creative_library_schema','maybe_install_automation_schema') as $method_name) {
    if (!method_exists($o, $method_name)) {
        $fail('missing_schema_method_' . $method_name);
    }
    $m = new ReflectionMethod($o, $method_name);
    $m->setAccessible(true);
    $m->invoke($o);
}

if ($wpdb->query('START TRANSACTION') === false) {
    $fail('transaction_start_' . $wpdb->last_error);
}
$in_tx = true;

update_option('ppar_network_adcell_v1', array(
    'enabled'=>true,
    'username'=>$username,
    'password'=>$password,
), false);
update_option('ppar_adcell_program_id_allowlist_v1', $program_ids, false);

$raw_items_m = new ReflectionMethod($o, 'adcell_api_v2_promotion_items');
$raw_items_m->setAccessible(true);
$programme_m = new ReflectionMethod($o, 'adcell_api_v2_programme');
$programme_m->setAccessible(true);
$banner_rows_m = new ReflectionMethod($o, 'automation_adcell_banner_rows');
$banner_rows_m->setAccessible(true);

$chosen_program = 0;
$chosen_partner = '';
$chosen_row = null;
$chosen_raw = null;

foreach ($program_ids as $program_id) {
    $programme = $programme_m->invoke($o, $program_id);
    if (is_wp_error($programme)) {
        $fail('real_programme_' . $program_id . '_' . $programme->get_error_code());
    }
    $partner_name = sanitize_text_field((string)($programme['name'] ?? ('ADCELL ' . $program_id)));

    $raw_items = $raw_items_m->invoke($o, $program_id, 'banner');
    if (is_wp_error($raw_items)) {
        $fail('real_banner_items_' . $program_id . '_' . $raw_items->get_error_code());
    }
    if (!(array)$raw_items) {
        continue;
    }

    $result = $banner_rows_m->invoke($o, $program_id, $partner_name, 'real-provider-gate-' . $program_id);
    if (is_wp_error($result)) {
        $fail('real_banner_rows_' . $program_id . '_' . $result->get_error_code());
    }
    $rows = array_values(array_filter((array)($result['rows'] ?? array()), 'is_array'));
    if (!$rows) {
        continue;
    }

    foreach ($rows as $row) {
        // Der Kategorien-Pflichtnachweis muss einen echten Banner verwenden,
        // fuer den ADCELL tatsaechlich eine Kategorie-ID liefert UND der
        // belegte Kategorienendpunkt den Namen aufloest. Ein zufaelliger
        // kategorieloser erster Banner darf den Real-Provider-Gate nicht
        // falsch negativ machen.
        $row_category_id = absint($row['promotion_category_id'] ?? 0);
        $row_category_name = trim((string)($row['promotion_category_name'] ?? ''));
        if ($row_category_id <= 0 || $row_category_name === '') {
            continue;
        }

        $raw_json = (string)($row['provider_raw_json'] ?? '');
        $decoded = json_decode($raw_json, true);
        if (!is_array($decoded)) {
            continue;
        }
        $promotion_id = absint($decoded['promotionId'] ?? 0);
        foreach ((array)$raw_items as $raw_item) {
            if (is_array($raw_item) && absint($raw_item['promotionId'] ?? 0) === $promotion_id) {
                $chosen_program = $program_id;
                $chosen_partner = $partner_name;
                $chosen_row = $row;
                $chosen_raw = $raw_item;
                // Erster geeigneter realer Kategorien-Banner genuegt fuer den
                // Basisbeweis; keine weiteren Provideraufrufe noetig.
                break 3;
            }
        }
    }
}

if ($chosen_program <= 0 || !is_array($chosen_row) || !is_array($chosen_raw)) {
    $fail('no_real_adcell_banner_with_resolved_category_found_in_configured_programs');
}
$ok('real_adcell_banner_with_resolved_category_received_from_configured_provider');

$raw_json = (string)($chosen_row['provider_raw_json'] ?? '');
$raw_sha = strtolower((string)($chosen_row['provider_raw_sha256'] ?? ''));
$decoded_raw = json_decode($raw_json, true);
if (!is_array($decoded_raw)
    || $decoded_raw !== $chosen_raw
    || !preg_match('/^[a-f0-9]{64}$/', $raw_sha)
    || !hash_equals(hash('sha256', $raw_json), $raw_sha)) {
    $fail('real_provider_object_not_preserved_value_type_and_hash');
}
$ok('real_provider_object_preserved_value_type_identical_with_sha256');

$category_id = absint($chosen_row['promotion_category_id'] ?? 0);
$category_name = trim((string)($chosen_row['promotion_category_name'] ?? ''));
if ($category_id <= 0 || $category_name === '') {
    $fail('real_provider_category_not_resolved');
}
$ok('real_provider_category_id_and_name_resolved');

$title_source = sanitize_key((string)($chosen_row['title_source'] ?? ''));
$title = trim((string)($chosen_row['creative_title'] ?? ''));
if ($title_source === 'provider_missing') {
    if ($title !== '') {
        $fail('synthetic_title_present_when_real_provider_title_missing');
    }
} elseif ($title_source === '' || $title === '') {
    $fail('real_provider_title_provenance_invalid');
}
$ok('real_provider_title_or_explicit_missing_provenance_preserved');

$install = new ReflectionMethod($o, 'creative_library_table');
$install->setAccessible(true);
$table = $install->invoke($o);
$external_id = sanitize_text_field((string)($chosen_row['creative_id'] ?? ''));
$identity_hash = hash('sha256', 'adcell|' . $chosen_program . '|' . $external_id);
$wpdb->delete($table, array('identity_hash'=>$identity_hash));

$import_m = new ReflectionMethod($o, 'automation_import_rows');
$import_m->setAccessible(true);
$counts = $import_m->invoke($o, array($chosen_row), array(
    'provider'=>'adcell',
    'partner_external_id'=>(string)$chosen_program,
    'partner_name'=>$chosen_partner,
    'source_kind'=>'banner',
    'run_uuid'=>'real-provider-gate',
));
if ((int)($counts['imported'] ?? 0) !== 1) {
    $fail('real_provider_library_import_' . wp_json_encode($counts));
}

$stored = $wpdb->get_row($wpdb->prepare(
    "SELECT * FROM {$table} WHERE identity_hash=%s",
    $identity_hash
), ARRAY_A);
$payload = json_decode((string)($stored['payload'] ?? ''), true);
if (!is_array($stored) || !is_array($payload)) {
    $fail('real_provider_library_row_missing');
}
if ((string)($payload['_provider_raw_json'] ?? '') !== $raw_json
    || (string)($payload['_provider_raw_sha256'] ?? '') !== $raw_sha
    || absint($payload['promotion_category_id'] ?? 0) !== $category_id
    || (string)($payload['promotion_category_name'] ?? '') !== $category_name) {
    $fail('real_provider_evidence_changed_before_library');
}

$expected_external_id = sanitize_text_field((string)($chosen_row['creative_id'] ?? ''));
$expected_image = esc_url_raw((string)($chosen_row['image_source'] ?? ''));
$expected_title_source = sanitize_key((string)($chosen_row['title_source'] ?? ''));
$expected_information = sanitize_text_field((string)($chosen_row['information'] ?? ''));
if ((string)($stored['provider'] ?? '') !== 'adcell'
    || (string)($stored['partner_external_id'] ?? '') !== (string)$chosen_program
    || (string)($stored['partner_name'] ?? '') !== $chosen_partner
    || (string)($stored['external_id'] ?? '') !== $expected_external_id
    || $expected_image === ''
    || esc_url_raw((string)($stored['image_url'] ?? '')) !== $expected_image
    || sanitize_key((string)($payload['title_source'] ?? '')) !== $expected_title_source) {
    $fail('real_provider_identity_image_or_title_provenance_changed_before_library');
}
if ($expected_information !== ''
    && sanitize_text_field((string)($payload['information'] ?? '')) !== $expected_information) {
    $fail('real_provider_information_not_preserved_in_library_payload');
}
$ok('real_provider_identity_raw_category_image_title_and_information_reach_library');

$tracking = esc_url_raw((string)($stored['tracking_url'] ?? ''));
$destination = esc_url_raw((string)($stored['destination_url'] ?? ''));
$destination_source = sanitize_key((string)($payload['_destination_source'] ?? ''));
if ($tracking === '' || $destination === ''
    || !in_array($destination_source, array(
        'provider_explicit','decoded_tracking','resolved_redirect',
        'tracking_checked','tracking_fallback'
    ), true)) {
    $fail('real_tracking_or_destination_provenance_missing');
}
if (in_array($destination_source, array('decoded_tracking','resolved_redirect'), true)
    && $destination === $tracking) {
    $fail('real_resolved_destination_equals_tracking_url');
}
if (in_array($destination_source, array('tracking_checked','tracking_fallback'), true)
    && $destination !== $tracking) {
    $fail('opaque_tracking_provenance_inconsistent');
}
$ok('real_tracking_and_destination_provenance_preserved');

$targets_before = json_decode((string)($stored['topic_targets'] ?? ''), true);
if (is_array($targets_before) && count($targets_before) !== 0) {
    $fail('real_banner_target_created_before_asset_verification');
}
$ok('real_banner_has_zero_targets_before_asset_verification');

$verify_m = new ReflectionMethod($o, 'creative_library_verify_asset_row');
$verify_m->setAccessible(true);
$verified = $verify_m->invoke($o, $stored, true, false);
if (is_wp_error($verified)) {
    $fail('real_banner_asset_verification_' . $verified->get_error_code() . '_' . $verified->get_error_message());
}
$after = $wpdb->get_row($wpdb->prepare(
    "SELECT * FROM {$table} WHERE identity_hash=%s",
    $identity_hash
), ARRAY_A);
$after_payload = json_decode((string)($after['payload'] ?? ''), true);
if (!is_array($after_payload)
    || absint($after['width'] ?? 0) <= 0
    || absint($after['height'] ?? 0) <= 0
    || !in_array(sanitize_key((string)($after_payload['_dimension_state'] ?? '')), array('verified','mismatch'), true)
    || !preg_match('/^[a-f0-9]{64}$/', (string)($after_payload['_image_sha256'] ?? ''))
    || absint($after_payload['_image_bytes'] ?? 0) <= 0) {
    $fail('real_banner_asset_evidence_not_persisted');
}
$ok('real_banner_image_bytes_and_dimensions_verified');

$rollback();
echo "PASS transaction_rolled_back_no_test_rows_or_credentials_persisted\n";
echo "ADCELL_BANNER_IMPORT_BASIS_REAL_PROVIDER_COMPLETE\n";
