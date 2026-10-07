<?php
if (!class_exists('Pferdeportal_Affiliate_Router')) {
    fwrite(STDERR, "FAIL plugin_not_loaded\n");
    exit(2);
}
if (Pferdeportal_Affiliate_Router::VERSION !== '6.72.199') {
    fwrite(STDERR, "FAIL wrong_version " . Pferdeportal_Affiliate_Router::VERSION . "\n");
    exit(2);
}
$fail = static function($message) {
    fwrite(STDERR, "FAIL " . $message . "\n");
    exit(1);
};
$ok = static function($message) {
    echo "PASS " . $message . "\n";
};
$o = Pferdeportal_Affiliate_Router::instance();

$snapshots_m = new ReflectionMethod($o, 'creative_library_snapshots_for_select');
$snapshots_m->setAccessible(true);
$snapshots = $snapshots_m->invoke($o);
if (($snapshots['direct:tarifcheck']['name'] ?? '') !== 'Tarifcheck') {
    $fail('tarifcheck_preset_missing');
}
if (($snapshots['direct:check24']['name'] ?? '') !== 'CHECK24') {
    $fail('check24_preset_missing');
}
$ok('tarifcheck_and_check24_direct_partner_presets');

$manual_m = new ReflectionMethod($o, 'creative_library_manual_banner_row');
$manual_m->setAccessible(true);
$manual = $manual_m->invoke($o, array(
    'manual_banner_external_id'=>'check24-test-01',
    'manual_banner_title'=>'CHECK24 Testbanner',
    'manual_banner_image_url'=>'https://cdn.example.test/check24-banner.png',
    'manual_banner_tracking_url'=>'https://tracking.example.test/check24',
    'manual_banner_destination_url'=>'https://www.check24.de/',
    'manual_banner_description'=>'Manuell hinterlegter Testbanner',
    'manual_banner_tags'=>'CHECK24',
    'manual_banner_width'=>728,
    'manual_banner_height'=>90,
));
if (is_wp_error($manual)) {
    $fail('manual_row_' . $manual->get_error_code());
}
if (($manual['creative_id'] ?? '') !== 'check24-test-01'
    || ($manual['tracking_url'] ?? '') !== 'https://tracking.example.test/check24'
    || ($manual['destination_url'] ?? '') !== 'https://www.check24.de/'
    || ($manual['title_source'] ?? '') !== 'manual_user') {
    $fail('manual_row_fields');
}
$ok('manual_banner_row_built');

$invalid = $manual_m->invoke($o, array(
    'manual_banner_image_url'=>'https://cdn.example.test/check24-banner.png',
    'manual_banner_tracking_url'=>'',
));
if (!is_wp_error($invalid) || $invalid->get_error_code() !== 'manual_banner_tracking') {
    $fail('manual_missing_tracking_not_blocked');
}
$ok('manual_banner_missing_tracking_fails_closed');

$untitled = $manual_m->invoke($o, array(
    'manual_banner_external_id'=>'check24-test-no-title',
    'manual_banner_image_url'=>'https://cdn.example.test/check24-banner-no-title.png',
    'manual_banner_tracking_url'=>'https://tracking.example.test/check24-no-title',
));
if (is_wp_error($untitled) || ($untitled['title_source'] ?? '') !== 'manual_missing') {
    $fail('manual_missing_title_provenance');
}
$ok('manual_missing_title_marked_non_evidence');

$install = new ReflectionMethod($o, 'maybe_install_creative_library_schema');
$install->setAccessible(true);
$install->invoke($o);
$table_m = new ReflectionMethod($o, 'creative_library_table');
$table_m->setAccessible(true);
$table = $table_m->invoke($o);
global $wpdb;
$wpdb->query($wpdb->prepare(
    "DELETE FROM {$table} WHERE provider='direct' AND partner_external_id=%s",
    'check24'
));
$detect = new ReflectionMethod($o, 'creative_library_detect_mapping');
$detect->setAccessible(true);
$mapping = $detect->invoke($o, array_keys($manual));
$normalize = new ReflectionMethod($o, 'creative_library_normalize_row');
$normalize->setAccessible(true);
$creative = $normalize->invoke($o, $manual, $mapping, array(
    'provider'=>'direct',
    'partner_external_id'=>'check24',
    'partner_name'=>'CHECK24',
    'source_kind'=>'manual_banner',
    'run_uuid'=>'manual-check24-test',
));
if (is_wp_error($creative)) {
    $fail('manual_normalize_' . $creative->get_error_code());
}
$upsert = new ReflectionMethod($o, 'creative_library_upsert');
$upsert->setAccessible(true);
$result = $upsert->invoke($o, $creative);
if (!in_array($result, array('imported','updated','unchanged'), true)) {
    $fail('manual_upsert_' . $result);
}
$stored = $wpdb->get_row($wpdb->prepare(
    "SELECT * FROM {$table} WHERE provider='direct' AND partner_external_id='check24' AND external_id=%s",
    'check24-test-01'
), ARRAY_A);
if (!is_array($stored)
    || ($stored['partner_name'] ?? '') !== 'CHECK24'
    || ($stored['creative_type'] ?? '') !== 'banner') {
    $fail('manual_check24_not_stored');
}
$ok('manual_check24_banner_stored_in_creative_library');

$partner_m = new ReflectionMethod($o, 'output_comparison_banner_partner');
$partner_m->setAccessible(true);
if ($partner_m->invoke($o, $stored) !== 'check24') {
    $fail('check24_comparison_partner_not_detected');
}
$ok('check24_detected_as_separate_direct_comparison_partner');

// Vollständiger CHECK24-Vertrag: derselbe bewährte Vergleichsportalweg wie
// Tarifcheck, aber mit eigener Partneridentität. Vor erfolgreicher realer
// Bildprüfung keine Zielkarte; danach ausschließlich gespeicherte feste Ziele.
$catalog = json_decode((string) file_get_contents(
    WP_PLUGIN_DIR . '/affiliate-portal-router/assets/ebay-portal-catalog-v2.json'
), true);
if (!is_array($catalog) || !is_array($catalog['article_targets'] ?? null)) {
    $fail('portal_catalog_missing');
}
$cost_records = array_values(array_filter($catalog['article_targets'], static function($x) {
    return is_array($x) && sanitize_key((string)($x['theme'] ?? '')) === 'kosten';
}));
$unique_cost_paths = array();
foreach ($cost_records as $x) {
    $p = (string)($x['path'] ?? '');
    if ($p !== '' && !isset($unique_cost_paths[$p])) {
        $unique_cost_paths[$p] = $x;
    }
}
$insurance_records = array_values(array_filter($catalog['article_targets'], static function($x) {
    return is_array($x) && strpos((string)($x['path'] ?? ''), 'Wissen > Versicherungen & Recht >') === 0;
}));
if (count($cost_records) !== 67 || count($unique_cost_paths) !== 66 || count($insurance_records) !== 14) {
    $fail('portal_catalog_comparison_target_counts');
}
$ok('real_portal_catalog_66_cost_paths_and_14_insurance_leaves');

$term = static function($name, $slug, $parent = 0) use ($fail) {
    $existing = get_term_by('slug', $slug, 'category');
    if ($existing && !is_wp_error($existing)) {
        return (int)$existing->term_id;
    }
    $made = wp_insert_term($name, 'category', array('slug'=>$slug, 'parent'=>$parent));
    if (is_wp_error($made)) {
        $fail('term_fixture_' . $slug . '_' . $made->get_error_code());
    }
    return (int)$made['term_id'];
};
$seed_path = static function($path_string, $leaf_slug) use ($term) {
    $parts = array_values(array_filter(array_map('trim', explode(' > ', $path_string)), 'strlen'));
    $parent = 0;
    $seen = array();
    foreach ($parts as $i=>$name) {
        $seen[] = $name;
        $slug = $i === count($parts)-1
            ? $leaf_slug
            : 'check24-199-parent-' . substr(hash('sha256', implode(' > ', $seen)), 0, 18);
        $parent = $term($name, $slug, $parent);
    }
    return $parent;
};
$cost_ids = array();
foreach ($unique_cost_paths as $x) {
    $slug = sanitize_key((string)$x['category_slug']);
    $cost_ids[$slug] = $seed_path((string)$x['path'], $slug);
}
$insurance_ids = array();
foreach ($insurance_records as $x) {
    $slug = sanitize_key((string)$x['category_slug']);
    $insurance_ids[$slug] = $seed_path((string)$x['path'], $slug);
}
if (count($cost_ids) !== 66 || count($insurance_ids) !== 14) {
    $fail('wordpress_comparison_target_fixture_counts');
}
$ok('wordpress_real_comparison_target_tree_seeded');

$png = base64_decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAusB9Wl+0iAAAAAASUVORK5CYII=');
add_filter('pre_http_request', static function($pre, $args, $url) use ($png) {
    if (strpos((string)$url, 'https://cdn.example.test/check24-') === 0) {
        if (strpos((string)$url, 'broken') !== false) {
            return new WP_Error('check24_image_broken', 'simulated broken CHECK24 image');
        }
        return array(
            'headers'=>array('content-type'=>'image/png', 'content-length'=>strlen($png)),
            'body'=>$png,
            'response'=>array('code'=>200, 'message'=>'OK'),
            'cookies'=>array(),
            'filename'=>null,
        );
    }
    return $pre;
}, 40, 3);

$targets_of = static function($row) {
    $records = json_decode((string)($row['topic_targets'] ?? ''), true);
    return is_array($records) ? array_values(array_filter($records, 'is_array')) : array();
};
$build_check24 = static function($external, $destination, $family, $image_suffix) use (
    $o, $manual_m, $detect, $normalize, $upsert, $table, $wpdb, $fail, $targets_of
) {
    $raw = $manual_m->invoke($o, array(
        'manual_banner_external_id'=>$external,
        'manual_banner_title'=>'CHECK24 ' . ucfirst($family),
        'manual_banner_image_url'=>'https://cdn.example.test/check24-' . $image_suffix . '.png',
        'manual_banner_tracking_url'=>'https://tracking.example.test/' . $external,
        'manual_banner_destination_url'=>$destination,
        'manual_banner_width'=>1,
        'manual_banner_height'=>1,
    ));
    if (is_wp_error($raw)) {
        $fail('check24_manual_build_' . $external . '_' . $raw->get_error_code());
    }
    $map = $detect->invoke($o, array_keys($raw));
    $normalized = $normalize->invoke($o, $raw, $map, array(
        'provider'=>'direct',
        'partner_external_id'=>'check24',
        'partner_name'=>'CHECK24',
        'target_family'=>$family,
        'source_kind'=>'manual_banner',
        'run_uuid'=>'check24-v672199-e2e',
    ));
    if (is_wp_error($normalized)) {
        $fail('check24_manual_normalize_' . $external . '_' . $normalized->get_error_code());
    }
    $payload = json_decode((string)($normalized['payload'] ?? ''), true);
    if (!is_array($payload) || (string)($payload['_manual_target_family'] ?? '') !== $family) {
        $fail('check24_family_not_persisted_in_normalized_payload_' . $external);
    }
    $result = $upsert->invoke($o, $normalized);
    if (!in_array($result, array('imported','updated','unchanged'), true)) {
        $fail('check24_manual_upsert_' . $external . '_' . $result);
    }
    $row = $wpdb->get_row($wpdb->prepare(
        "SELECT * FROM {$table} WHERE identity_hash=%s",
        (string)$normalized['identity_hash']
    ), ARRAY_A);
    if (!is_array($row)) {
        $fail('check24_manual_stored_' . $external);
    }
    if (count($targets_of($row)) !== 0) {
        $fail('check24_target_created_before_image_verification_' . $external);
    }
    return $row;
};

$verify_m = new ReflectionMethod($o, 'creative_library_verify_asset_row');
$verify_m->setAccessible(true);

// CHECK24 Kosten: erst technische Prüfung, danach exakt alle 66 Kostenpfade.
$cost_pending = $build_check24(
    'check24-cost-v672199',
    'https://www.check24.de/kredit/',
    'kosten',
    'cost'
);
$cost_verified = $verify_m->invoke($o, $cost_pending, true, false);
if (is_wp_error($cost_verified)) {
    $fail('check24_cost_image_verification_' . $cost_verified->get_error_code());
}
$cost_row = $wpdb->get_row($wpdb->prepare(
    "SELECT * FROM {$table} WHERE id=%d",
    (int)$cost_pending['id']
), ARRAY_A);
$cost_targets = $targets_of($cost_row);
$cost_keys = array_values(array_map(static function($x) {
    return (string)($x['target_key'] ?? '');
}, $cost_targets));
if (count($cost_targets) !== 66) {
    $fail('check24_cost_target_count_' . count($cost_targets));
}
foreach ($cost_ids as $slug=>$id) {
    if (!in_array('category:' . $id, $cost_keys, true)) {
        $fail('check24_cost_missing_' . $slug);
    }
}
foreach ($insurance_ids as $slug=>$id) {
    if (in_array('category:' . $id, $cost_keys, true)) {
        $fail('check24_cost_contains_insurance_' . $slug);
    }
}
$ok('check24_manual_cost_verified_then_66_fixed_cost_targets');

// CHECK24 Versicherung: ausschließlich die 14 echten Versicherungsblätter.
$insurance_pending = $build_check24(
    'check24-insurance-v672199',
    'https://www.check24.de/versicherungen/',
    'versicherung',
    'insurance'
);
$insurance_verified = $verify_m->invoke($o, $insurance_pending, true, false);
if (is_wp_error($insurance_verified)) {
    $fail('check24_insurance_image_verification_' . $insurance_verified->get_error_code());
}
$insurance_row = $wpdb->get_row($wpdb->prepare(
    "SELECT * FROM {$table} WHERE id=%d",
    (int)$insurance_pending['id']
), ARRAY_A);
$insurance_targets = $targets_of($insurance_row);
$insurance_keys = array_values(array_map(static function($x) {
    return (string)($x['target_key'] ?? '');
}, $insurance_targets));
if (count($insurance_targets) !== 14) {
    $fail('check24_insurance_target_count_' . count($insurance_targets));
}
foreach ($insurance_ids as $slug=>$id) {
    if (!in_array('category:' . $id, $insurance_keys, true)) {
        $fail('check24_insurance_missing_' . $slug);
    }
}
foreach ($cost_ids as $slug=>$id) {
    if (in_array('category:' . $id, $insurance_keys, true)) {
        $fail('check24_insurance_contains_cost_' . $slug);
    }
}
$ok('check24_manual_insurance_verified_then_14_fixed_insurance_targets');

// Kaputtes Bild: trotz expliziter Familie niemals Zielkarte.
$broken_pending = $build_check24(
    'check24-broken-v672199',
    'https://www.check24.de/kredit/',
    'kosten',
    'broken'
);
$broken_verified = $verify_m->invoke($o, $broken_pending, true, false);
if (!is_wp_error($broken_verified)) {
    $fail('check24_broken_image_not_blocked');
}
$broken_row = $wpdb->get_row($wpdb->prepare(
    "SELECT * FROM {$table} WHERE id=%d",
    (int)$broken_pending['id']
), ARRAY_A);
if (count($targets_of($broken_row)) !== 0
    || sanitize_key((string)($broken_row['topic_status'] ?? '')) !== 'format_blocked') {
    $fail('check24_broken_image_received_target');
}
$ok('check24_broken_image_fail_closed_without_target');

// Runtime darf nur die bereits gespeicherte Zielkarte lesen.
$portal_key_m = new ReflectionMethod($o, 'output_local_portal_key');
$portal_key_m->setAccessible(true);
$portal_key = sanitize_key((string)$portal_key_m->invoke($o));
$registry_m = new ReflectionMethod($o, 'output_portal_registry');
$registry_m->setAccessible(true);
$portal = null;
foreach ((array)$registry_m->invoke($o) as $candidate) {
    if (is_array($candidate)
        && !empty($candidate['enabled'])
        && sanitize_key((string)($candidate['key'] ?? '')) === $portal_key) {
        $portal = $candidate;
        break;
    }
}
if (!is_array($portal)) {
    $fail('check24_local_portal_missing');
}
$runtime_m = new ReflectionMethod($o, 'output_banner_destination_classification');
$runtime_m->setAccessible(true);
$cost_runtime = $runtime_m->invoke($o, $cost_row, $portal);
if (!is_array($cost_runtime)
    || sanitize_key((string)($cost_runtime['source'] ?? '')) !== 'check24_credit_all_cost_categories'
    || count(array_values(array_unique(array_filter((array)($cost_runtime['_ppar_banner_target_keys'] ?? array()))))) !== 66) {
    $fail('check24_runtime_not_using_stored_cost_map');
}
$insurance_runtime = $runtime_m->invoke($o, $insurance_row, $portal);
if (!is_array($insurance_runtime)
    || sanitize_key((string)($insurance_runtime['source'] ?? '')) !== 'check24_insurance_all_insurance_categories'
    || count(array_values(array_unique(array_filter((array)($insurance_runtime['_ppar_banner_target_keys'] ?? array()))))) !== 14) {
    $fail('check24_runtime_not_using_stored_insurance_map');
}
$ok('check24_runtime_reads_only_persisted_comparison_target_maps');

$admins = get_users(array('role'=>'administrator','number'=>1));
if (!$admins) {
    $uid = wp_create_user('banner-gate-admin', 'ci-banner-gate-pass!', 'banner-gate@example.test');
    if (is_wp_error($uid)) { $fail('admin_fixture_create'); }
    $user = new WP_User($uid);
    $user->set_role('administrator');
    $admins = array($user);
}
wp_set_current_user(absint($admins[0]->ID));
$_GET = array('page'=>'affiliate-portal-creative-library');
ob_start();
$o->render_creative_library_page();
$html = ob_get_clean();
foreach (array(
    'value="direct:tarifcheck"',
    '>Tarifcheck</option>',
    'value="direct:check24"',
    '>CHECK24</option>',
    'Banner händisch einfügen',
    'Vergleichsportal-Zielgruppe',
    'name="manual_banner_image_url"',
    'name="manual_banner_tracking_url"',
    'name="manual_banner_destination_url"'
) as $needle) {
    if (strpos($html, $needle) === false) {
        $fail('rendered_ui_missing_' . md5($needle));
    }
}
$ok('rendered_backend_ui_contains_tarifcheck_check24_and_manual_banner_form');
echo "DIRECT_PARTNER_MANUAL_BANNER_V672199_E2E_COMPLETE\n";
