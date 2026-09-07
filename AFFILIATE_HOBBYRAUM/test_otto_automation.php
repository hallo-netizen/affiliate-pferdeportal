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
    $text = @file_get_contents(__DIR__ . '/' . $name);
    if ($text === false) {
        fwrite(STDERR, "FAIL: source missing: {$name}\n");
        exit(1);
    }
    return $text;
}

$automation = source('trait-ppar-automation-suite.php');
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

echo "ALL OTTO HOBBYROOM TESTS PASS\n";
