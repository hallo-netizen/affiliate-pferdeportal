<?php
declare(strict_types=1);

function pass_or_fail(bool $ok, string $name): void {
    if (!$ok) {
        fwrite(STDERR, "FAIL: {$name}\n");
        exit(1);
    }
    echo "PASS: {$name}\n";
}

function source(string $name): string {
    $sandbox = __DIR__ . '/' . $name;
    $text = @file_get_contents($sandbox);
    if ($text !== false) {
        return $text;
    }
    $repoRoot = dirname(__DIR__);
    $map = [
        'pferdeportal-affiliate-router.php' => 'release/affiliate-zentrale/current/affiliate-portal-router/pferdeportal-affiliate-router.php',
        'trait-ppar-automation-suite.php' => 'release/affiliate-zentrale/current/affiliate-portal-router/includes/trait-ppar-automation-suite.php',
        'trait-ppar-awin-programme-gate.php' => 'release/affiliate-zentrale/current/affiliate-portal-router/includes/trait-ppar-awin-programme-gate.php',
        'trait-ppar-provider-registry.php' => 'release/affiliate-zentrale/current/affiliate-portal-router/includes/trait-ppar-provider-registry.php',
        'trait-ppar-output-objects.php' => 'release/affiliate-zentrale/current/affiliate-portal-router/includes/trait-ppar-output-objects.php',
        'trait-ppar-article-plans.php' => 'release/affiliate-zentrale/current/affiliate-portal-router/includes/trait-ppar-article-plans.php',
        'trait-ppar-creative-library.php' => 'release/affiliate-zentrale/current/affiliate-portal-router/includes/trait-ppar-creative-library.php',
        'trait-ppar-ebay.php' => 'release/affiliate-zentrale/current/affiliate-portal-router/includes/trait-ppar-ebay.php',
        'class-ppar-product-source-plan.php' => 'release/affiliate-zentrale/current/affiliate-portal-router/includes/class-ppar-product-source-plan.php',
        'class-ppar-partner-analytics.php' => 'release/affiliate-zentrale/current/affiliate-portal-router/includes/class-ppar-partner-analytics.php',
        'class-ppar-deal-radar.php' => 'release/affiliate-zentrale/current/affiliate-portal-router/includes/class-ppar-deal-radar.php',
    ];
    if (isset($map[$name])) {
        $direct = $repoRoot . '/' . $map[$name];
        $text = @file_get_contents($direct);
        if ($text !== false) {
            return $text;
        }
    }
    fwrite(STDERR, "FAIL: source missing: {$name}\n");
    exit(1);
}

$automation = source('trait-ppar-automation-suite.php');
$awin_gate = source('trait-ppar-awin-programme-gate.php');
$provider_registry = source('trait-ppar-provider-registry.php');
$output = source('trait-ppar-output-objects.php');
$articles = source('trait-ppar-article-plans.php');
$creative = source('trait-ppar-creative-library.php');
$ebay = source('trait-ppar-ebay.php');
$router = source('pferdeportal-affiliate-router.php');
$source_plan = source('class-ppar-product-source-plan.php');
$analytics = source('class-ppar-partner-analytics.php');
$radar = source('class-ppar-deal-radar.php');

pass_or_fail(
    str_contains($source_plan, 'const OTTO_AWIN_ADVERTISER_ID = 14336')
    && str_contains($router, 'OTTO_AWIN_ADVERTISER_ID = PPAR_Affiliate_Source_Plan::OTTO_AWIN_ADVERTISER_ID')
    && str_contains($output, 'self::OTTO_AWIN_ADVERTISER_ID')
    && str_contains($source_plan, "'awin_advertiser_id'=>self::OTTO_AWIN_ADVERTISER_ID")
    && str_contains($analytics, 'PPAR_Affiliate_Source_Plan::OTTO_AWIN_ADVERTISER_ID')
    && str_contains($radar, 'PPAR_Affiliate_Source_Plan::OTTO_AWIN_ADVERTISER_ID'),
    'OTTO identity has one canonical Awin advertiser 14336 authority'
);

pass_or_fail(
    str_contains($automation, 'creative_library_schedule_asset_verification(10)'),
    'automated imports enter asset verification'
);
pass_or_fail(
    str_contains($awin_gate, 'function awin_programme_gate_allowed_advertiser_ids')
    && str_contains($awin_gate, "'allow_local'")
    && str_contains($awin_gate, 'awin_programme_gate_current_joined'),
    'scheduled Awin bootstrap enumerates only explicitly allowed and currently joined programmes'
);
pass_or_fail(
    str_contains($automation, 'awin_programme_gate_allowed_advertiser_ids')
    && !str_contains(substr(
        $automation,
        strpos($automation, 'function automation_scheduled_sources'),
        strpos($automation, 'function automation_scheduled_source_batch') - strpos($automation, 'function automation_scheduled_sources')
    ), 'partner_intake_snapshots()'),
    'scheduled Awin sources do not require pre-existing Partner-Intake snapshots'
);
pass_or_fail(
    str_contains($automation, 'function automation_refresh_awin_programme_list')
    && str_contains($automation, "/programmes?relationship=joined")
    && str_contains($automation, 'Last-Known-Good bleibt erhalten.'),
    'joined Awin programme list refreshes automatically with Last-Known-Good fallback'
);
pass_or_fail(
    str_contains($automation, 'function automation_refresh_awin_feed_list')
    && str_contains($automation, 'https://productdata.awin.com/datafeed/list/apikey/')
    && str_contains($automation, 'ppar_awin_feed_list_refresh_warning_v1'),
    'official Awin product-feed list refreshes once per new automation cycle'
);
pass_or_fail(
    str_contains($automation, 'ppar_affiliate_awin_product_seller')
    && str_contains($automation, "'seller_name' => \$seller_name"),
    'Awin product seller is explicit and fail-closed'
);
pass_or_fail(
    str_contains($automation, "'exact_mpn' =>")
    && str_contains($automation, "automation_awin_field(\$row, array('mpn'))"),
    'exact MPN never falls back to merchant SKU'
);
pass_or_fail(
    str_contains($output, 'function output_is_otto_awin_product')
    && str_contains($output, 'function output_otto_awin_auto_allowed')
    && str_contains($output, 'output_otto_seller_name($row)'),
    'OTTO remains a logical Awin product source with seller gate'
);
pass_or_fail(
    str_contains($output, "'category_product'")
    && str_contains($output, "'post_bottom_products'")
    && str_contains($output, "'hub_product_1'")
    && str_contains($output, "'journal_product_1'"),
    'OTTO uses existing category hub journal and article product placements'
);
pass_or_fail(
    str_contains($output, "'product_identifiers'")
    && str_contains($output, "'product_identity_source'] = \$campaign['product_identifiers'] ? 'awin_otto_feed'")
    && str_contains($router, "'product_identifiers' => array()"),
    'OTTO exact product identifiers survive materialization'
);
pass_or_fail(
    str_contains($articles, 'ppar_affiliate_exact_product_requirements')
    && str_contains($router, "exact_product_identifiers")
    && str_contains($articles, 'kein Ersatzprodukt')
    && str_contains($router, 'Exakte Produktidentität aus fachlicher Produktbindung.'),
    'Productwissen exact-product contract is read-only and fail-closed'
);
pass_or_fail(
    !str_contains($articles, 'upk_products')
    && !str_contains($output, 'upk_products')
    && !str_contains($router, 'upk_products')
    && !str_contains($automation, 'upk_products'),
    'Affiliate does not couple directly to Productwissen tables'
);
pass_or_fail(
    str_contains($router, 'if (!$exact_mode &&')
    && str_contains($router, 'ebay_filter_ranked_product_candidates_provider_cohort')
    && str_contains($router, 'multiprovider_filter_candidates_by_strategy'),
    'exact fach identity outranks generic provider cohort strategy'
);
pass_or_fail(
    str_contains($output, "'_ppar_otto_awin_auto'")
    && str_contains($output, "'otto_awin_verified_product'"),
    'only centrally verified OTTO campaigns receive auto marker'
);
pass_or_fail(
    str_contains($articles, '$trusted_awin_auto')
    && str_contains($articles, 'auto_verified_otto_awin')
    && str_contains($articles, '_ppar_otto_awin_auto'),
    'article plans trust only centrally verified OTTO Awin products'
);
pass_or_fail(
    str_contains($creative, 'creative_asset_verification_complete')
    && str_contains($creative, 'product_payload_hash')
    && str_contains($creative, 'source_payload_for_hash'),
    'verification wave rebuilds articles and product payload changes alter freshness'
);
pass_or_fail(
    str_contains($ebay, 'ebay_verified_otto_awin_campaign')
    && str_contains($ebay, '$verified_otto_awin_present')
    && str_contains($ebay, "&& !\$verified_otto_awin_present"),
    'legacy eBay cohort cannot silently suppress verified OTTO'
);
pass_or_fail(
    str_contains($router, 'otto_awin_product_campaign_seller_ready')
    && substr_count($router, 'Verkauf durch ') >= 1
    && str_contains($articles, 'Verkauf durch '),
    'seller is a public-output gate and rendered on product cards'
);
pass_or_fail(
    str_contains($source_plan, 'activate_verified_banner_candidates')
    && str_contains($source_plan, "output_type='portal_banner'")
    && str_contains($source_plan, "'decision_source'=>'automatic_banner_network'")
    && !str_contains($output, 'product_image_as_banner')
    && !str_contains($automation, 'product_image_as_banner'),
    'real imported Awin banners are auto-assigned; no product-image banner fallback'
);

pass_or_fail(
    str_contains($router, "const OPTION_BANNER_DISTRIBUTION = 'ppar_banner_distribution_v1'")
    && str_contains($router, "'otto'=>40")
    && str_contains($router, "'awin_other'=>25")
    && str_contains($router, "'adcell'=>20")
    && str_contains($router, "'direct'=>15")
    && str_contains($router, "'digistore24'=>0"),
    'banner distribution has explicit configurable starting shares'
);
pass_or_fail(
    str_contains($router, 'banner_distribution_relevance_band')
    && str_contains($router, 'best_band')
    && str_contains($router, 'Banneranteil ')
    && str_contains($router, "gmdate('o-W')"),
    'banner share applies only inside best relevance tier and stays weekly deterministic'
);
pass_or_fail(
    str_contains($router, 'function banner_distribution_slot')
    && str_contains($router, "'start_after_topics'")
    && str_contains($router, "'hub_grid_card'")
    && str_contains($router, "'hub_after_cards'")
    && str_contains($router, "'product_after_category_tiles'")
    && str_contains($router, "'journal_banner'")
    && str_contains($router, "'anzeigenmarkt_top_banner'"),
    'banner share covers all real banner placement families'
);
pass_or_fail(
    str_contains($router, 'Weight 0 is an automatic exclusion')
    && str_contains($router, "absint(\$settings['weights'][\$key] ?? 0) <= 0")
    && str_contains($router, 'return array();'),
    'zero banner share is a true automatic exclusion'
);
pass_or_fail(
    str_contains($automation, 'ppar_affiliate_awin_static_creatives')
    && str_contains($automation, 'automation_import_awin_static_creatives')
    && str_contains($automation, 'not_bound_real_source_required')
    && str_contains($automation, 'bound_real_source'),
    'real Awin banner source seam is fail-closed and automation-ready'
);
pass_or_fail(
    str_contains($automation, "array_key_exists('bound', \$raw)")
    && str_contains($automation, 'awin_static_creative_rows_invalid')
    && str_contains($automation, "\$raw_rows = \$raw['rows']"),
    'bound-empty real Awin creative source is distinguishable from unbound'
);
pass_or_fail(
    str_contains($router, "banner_distribution_position")
    && str_contains($router, "\$rank_context['banner_distribution_position'] = \$position"),
    'multi-position banner slots use independent distribution seeds'
);
pass_or_fail(
    str_contains($router, 'Position 2 receives its own weighted decision')
    && str_contains($router, "\$candidate_key !== \$first_key"),
    'second banner place uses independent share decision without duplicate creative'
);
pass_or_fail(
    str_contains($router, 'Für eine manuelle Affiliate-Reparatur ist eine Begründung erforderlich.')
    && str_contains($router, "'repair_reason'=>\$manual_repair ? \$repair_reason : ''")
    && str_contains($router, "'updated_by'=>get_current_user_id()"),
    'manual page repair stores reason actor and timestamp'
);
pass_or_fail(
    str_contains($router, 'handle_save_banner_distribution')
    && str_contains($router, 'Banneranteile speichern')
    && str_contains($router, 'Diese Seite ist zugleich die interne Reparaturinstanz'),
    'banner share settings and manual repair UI are available'
);
pass_or_fail(
    str_contains($articles, "assignment_selection_for_slot(\$context, 'post_inline_banner')")
    && str_contains($articles, "\$assigned_banner['handled']")
    && str_contains($articles, "\$assigned_banner['disabled']"),
    'manual repair overrides automatic article banner planning'
);

// Behavioral mini-contracts.
function is_otto(array $row): bool {
    return ($row['provider'] ?? '') === 'awin'
        && ($row['source_kind'] ?? '') === 'product'
        && (int)($row['partner_external_id'] ?? 0) === 14336;
}
function auto_allowed(array $row): bool {
    return is_otto($row)
        && ($row['classification'] ?? '') === 'ready'
        && ($row['image_verified'] ?? false) === true
        && ($row['programme_allowed'] ?? false) === true
        && ($row['tracking_ok'] ?? false) === true
        && trim((string)($row['seller_name'] ?? '')) !== '';
}
$good = [
    'provider'=>'awin','source_kind'=>'product','partner_external_id'=>14336,
    'classification'=>'ready','image_verified'=>true,'programme_allowed'=>true,
    'tracking_ok'=>true,'seller_name'=>'Reitsport Händler GmbH'
];
pass_or_fail(auto_allowed($good), 'positive OTTO auto contract');
$bad = $good; $bad['seller_name'] = '';
pass_or_fail(!auto_allowed($bad), 'missing seller blocks OTTO');
$bad = $good; $bad['programme_allowed'] = false;
pass_or_fail(!auto_allowed($bad), 'unapproved Awin programme blocks OTTO');
$bad = $good; $bad['image_verified'] = false;
pass_or_fail(!auto_allowed($bad), 'unverified image blocks OTTO');
$bad = $good; $bad['partner_external_id'] = 99999;
pass_or_fail(!auto_allowed($bad), 'non-OTTO Awin cannot be enabled by OTTO rule');

$normalize = static function(array $ids): array {
    $out = [];
    foreach ($ids as $id) {
        $type = strtoupper((string)($id['type'] ?? ''));
        if ($type === 'EAN') $type = 'GTIN';
        $value = trim((string)($id['value'] ?? ''));
        if ($type === 'GTIN') $value = preg_replace('/[^0-9]/', '', $value);
        if ($type === '' || $value === '') continue;
        $out[$type . ':' . $value] = true;
    }
    return array_keys($out);
};
$exact_match = static function(array $wanted, array $candidate) use ($normalize): bool {
    return (bool)array_intersect($normalize($wanted), $normalize($candidate));
};
pass_or_fail(
    $exact_match([['type'=>'EAN','value'=>'4001234567890']], [['type'=>'GTIN','value'=>'4001234567890']]),
    'EAN and GTIN resolve to same exact product identity'
);
pass_or_fail(
    !$exact_match([['type'=>'GTIN','value'=>'4001234567890']], [['type'=>'GTIN','value'=>'4001234567891']]),
    'similar but different product identifier is never substituted'
);

$choose_provider = static function(array $eligible, int $bucket): string {
    $total = array_sum($eligible);
    if ($total <= 0) return '';
    $bucket %= $total;
    $cursor = 0;
    foreach ($eligible as $key=>$weight) {
        $cursor += $weight;
        if ($bucket < $cursor) return (string)$key;
    }
    return '';
};
pass_or_fail($choose_provider(['otto'=>40,'awin_other'=>25,'adcell'=>20,'direct'=>15], 0) === 'otto', 'weighted banner bucket starts in OTTO share');
pass_or_fail($choose_provider(['otto'=>40,'awin_other'=>25,'adcell'=>20,'direct'=>15], 40) === 'awin_other', 'weighted banner bucket moves to next share at boundary');
pass_or_fail($choose_provider(['otto'=>40,'adcell'=>20], 45) === 'adcell', 'missing banner sources are redistributed by normalization');
pass_or_fail(
    str_contains($router, "if (\$this->banner_distribution_relevance_band((int) (\$candidate['specificity'] ?? 0)) !== \$best_band)")
    && str_contains($router, "if (!\$exact_mode &&"),
    'share cannot outrank stronger relevance and product exact logic stays separate'
);

$fp = static function(array $row): string {
    ksort($row);
    return hash('sha256', json_encode($row, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES));
};
$a = $fp(['price'=>'49.99','availability'=>'active','seller_name'=>'A']);
$b = $fp(['price'=>'54.99','availability'=>'active','seller_name'=>'A']);
$c = $fp(['price'=>'49.99','availability'=>'active','seller_name'=>'B']);
pass_or_fail($a !== $b && $a !== $c, 'price and seller changes alter product freshness');


pass_or_fail(
    str_contains($automation, 'function automation_cleanup_legacy_unfiltered_otto_imports')
    && str_contains($automation, "last_complete_run=%s")
    && str_contains($automation, "absint(\$run['updated'] ?? 0) !== 0")
    && str_contains($automation, 'row-count-exceeds-imported'),
    'legacy OTTO cleanup is exact-run scoped and fails closed on provenance mismatch'
);
pass_or_fail(
    str_contains($automation, 'output_deactivate_materialized_object')
    && str_contains($automation, "'_ppar_creative_identity_hash'")
    && str_contains($automation, "'_ppar_output_object_key'")
    && !str_contains($automation, 'DELETE FROM {$library_table} WHERE provider='),
    'legacy OTTO cleanup removes only exact linked output and never broad-deletes partner library'
);
pass_or_fail(
    str_contains($automation, "update_option('ppar_otto_legacy_cleanup_v6727'")
    && str_contains($automation, 'OTTO-Sicherheitsbereinigung:')
    && str_contains($automation, "\$target = '4.1.2'"),
    'cleanup is idempotently version-bound and visible in automation readback'
);
pass_or_fail(
    str_contains($automation, 'function automation_otto_filtered_feed_binding')
    && str_contains($automation, "'portal_filtered'")
    && str_contains($provider_registry, 'Create-a-Feed')
    && str_contains($provider_registry, 'portal_filtered'),
    'OTTO requires explicit source-side filtered Awin feed before enqueue'
);
$batch_start = strpos($automation, 'private function automation_process_awin_product_batch');
$batch_end = strpos($automation, 'private function automation_process_adcell_product_batch', $batch_start);
$batch = substr($automation, $batch_start, $batch_end - $batch_start);
pass_or_fail(
    strpos($batch, 'automation_otto_product_relevance_gate') < strpos($batch, 'automation_import_rows(array($normalized)'),
    'OTTO local relevance gate executes before creative library persistence'
);

pass_or_fail(
    str_contains($automation, "FROM {$runs_table}")
    && str_contains($automation, "operation='queued_partner_sync'")
    && str_contains($automation, "message LIKE %s")
    && str_contains($automation, "first_seen>=%d AND first_seen<=%d")
    && str_contains($automation, '$row_count !== $imported'),
    '6.72.8 cleanup uses durable failed-run provenance and exact new-row count'
);
pass_or_fail(
    str_contains($automation, '// Full preflight before the first destructive write')
    && str_contains($automation, "'status'=>'blocked_source'")
    && !str_contains($automation, '$wpdb->delete($output_table'),
    '6.72.8 cleanup preflights all rows and deactivates output fail-closed'
);
pass_or_fail(
    str_contains($automation, "ppar_otto_legacy_cleanup_v6728")
    && str_contains($automation, "'no_candidate'")
    && str_contains($automation, "'already_cleaned'")
    && str_contains($automation, "'nicht ausgeführt'")
    && !str_contains($automation, "if (!empty($otto_cleanup['matched_runs']))"),
    '6.72.8 cleanup readback is always observable and idempotence-aware'
);
pass_or_fail(
    str_contains($automation, "$target = '4.1.3';")
    && str_contains($automation, "absint($cleanup['candidate_runs'] ?? 0) > 0"),
    '6.72.8 safety migration uses candidate-run contract'
);

echo "ALL OTTO HOBBYROOM TESTS PASS\n";
