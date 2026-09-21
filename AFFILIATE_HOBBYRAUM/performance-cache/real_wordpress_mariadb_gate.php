<?php
/**
 * Plugin Name: Affiliate Performance Cache RealDB Gate
 * Description: Ephemeral GitHub-Hobbyraum gate. Never installed on production.
 * Version: 1.0.0
 * Ephemeral GitHub-Hobbyraum gate. Never installed on production.
 * Runs only for ?ppar_perf_cache_gate=1 on the isolated CI WordPress.
 */
if (!defined('ABSPATH')) { exit; }

add_action('template_redirect', static function () {
    if ((string) ($_GET['ppar_perf_cache_gate'] ?? '') !== '1') { return; }
    header('Content-Type: text/plain; charset=utf-8');
    global $wpdb;

    $fail = static function (string $m): void {
        status_header(500);
        echo "FAIL {$m}\n";
        exit;
    };
    $pass = static function (string $m): void { echo "PASS {$m}\n"; };
    $assert = static function ($condition, string $m) use ($fail, $pass): void {
        if (!$condition) { $fail($m); }
        $pass($m);
    };

    if (!class_exists('Pferdeportal_Affiliate_Router')) { $fail('affiliate plugin class missing'); }
    $o = Pferdeportal_Affiliate_Router::instance();
    $o->maybe_install_control_contract_schema();
    $o->maybe_install_ebay_schema();
    $o->maybe_install_creative_library_schema();

    $portal = 'pferde-atelier';
    $scope = 'creative';
    $scope_key = 'perf-cache-control-a';

    $id = $o->control_set_decision($portal, $scope, $scope_key, 'approved', 'CI fixture approved');
    $assert(!is_wp_error($id) && (int) $id > 0, 'control fixture created');

    $before = (int) $wpdb->num_queries;
    $last = null;
    for ($i = 0; $i < 11297; $i++) {
        $last = $o->control_get_decision($portal, $scope, $scope_key);
    }
    $delta = (int) $wpdb->num_queries - $before;
    $assert($delta === 1, '11297 identical control reads collapse to exactly 1 DB query');
    $assert(is_array($last) && ($last['status'] ?? '') === 'approved', 'control result remains approved');

    $before = (int) $wpdb->num_queries;
    $missing = null;
    for ($i = 0; $i < 1000; $i++) {
        $missing = $o->control_get_decision($portal, 'creative', 'perf-cache-missing-control');
    }
    $delta = (int) $wpdb->num_queries - $before;
    $assert($delta === 1, '1000 missing control reads collapse to exactly 1 DB query');
    $assert(is_array($missing) && empty($missing['exists']) && ($missing['status'] ?? '') === 'automatic', 'missing control semantics unchanged');

    $before = (int) $wpdb->num_queries;
    foreach (array('slot-a','slot-b','slot-c') as $slot) {
        for ($i = 0; $i < 20; $i++) { $o->control_get_decision($portal, 'slot', $slot); }
    }
    $delta = (int) $wpdb->num_queries - $before;
    $assert($delta === 3, 'different control keys never collide');

    $o->control_get_decision($portal, $scope, $scope_key);
    $write = $o->control_set_decision($portal, $scope, $scope_key, 'veto', 'CI veto');
    $assert(!is_wp_error($write), 'control veto write succeeds');
    $before = (int) $wpdb->num_queries;
    $fresh = $o->control_get_decision($portal, $scope, $scope_key);
    $delta = (int) $wpdb->num_queries - $before;
    $assert($delta === 1 && ($fresh['status'] ?? '') === 'veto', 'write invalidates cache and fresh veto is read');

    $reset = $o->control_reset_decision($portal, $scope, $scope_key);
    $assert(!is_wp_error($reset), 'control reset succeeds');
    $fresh = $o->control_get_decision($portal, $scope, $scope_key);
    $assert(($fresh['status'] ?? '') === 'automatic', 'reset returns to automatic');

    $pid = $o->control_set_decision($portal, 'provider', 'ebay', 'paused', 'CI paused');
    $assert(!is_wp_error($pid), 'provider paused state can be stored');
    $paused = $o->control_get_decision($portal, 'provider', 'ebay');
    $assert(($paused['status'] ?? '') === 'paused', 'provider paused state remains paused');
    update_option(Pferdeportal_Affiliate_Router::OPTION_CONTROL_SETTINGS, array('emergency_stop'=>1,'emergency_reason'=>'CI','updated_at'=>time(),'updated_by'=>0), false);
    $assert($o->control_emergency_stop_active() === true, 'emergency stop remains active');
    update_option(Pferdeportal_Affiliate_Router::OPTION_CONTROL_SETTINGS, array('emergency_stop'=>0,'emergency_reason'=>'','updated_at'=>time(),'updated_by'=>0), false);
    $assert($o->control_emergency_stop_active() === false, 'emergency stop can be released');

    $delkey = 'perf-cache-delete-me';
    $did = $o->control_set_decision($portal, $scope, $delkey, 'approved', 'CI delete fixture');
    $assert(!is_wp_error($did), 'delete fixture created');
    $o->control_get_decision($portal, $scope, $delkey);
    $rmDelete = new ReflectionMethod($o, 'ebay_deletion_delete_control_scope');
    $rmDelete->setAccessible(true);
    $rmDelete->invoke($o, $scope, $delkey);
    $before = (int) $wpdb->num_queries;
    $gone = $o->control_get_decision($portal, $scope, $delkey);
    $delta = (int) $wpdb->num_queries - $before;
    $assert($delta === 1 && empty($gone['exists']), 'direct control deletion clears request cache');

    $hashA = str_repeat('a', 64);
    $postA = wp_insert_post(array('post_type'=>'post','post_status'=>'draft','post_title'=>'CI eBay A'));
    $assert(!is_wp_error($postA) && (int) $postA > 0, 'eBay fixture post created');
    update_post_meta((int) $postA, '_ppar_ebay_business_auto', 1);
    update_post_meta((int) $postA, '_ppar_creative_identity_hash', $hashA);
    get_post_meta((int) $postA);

    $ebayTable = $wpdb->prefix . 'ppar_ebay_items';
    $now = time();
    $inserted = $wpdb->insert($ebayTable, array(
        'portal_key'=>$portal,'item_id'=>'ci-business-a','legacy_item_id'=>'','seller_account_type'=>'BUSINESS','seller_username'=>'ci',
        'route_mode'=>'product','rule_id'=>'ci','target_term_id'=>0,'listing_post_id'=>0,'creative_identity_hash'=>$hashA,
        'title'=>'CI BUSINESS','short_description'=>'','condition_text'=>'New','price_value'=>'10','currency'=>'EUR','shipping_value'=>'0',
        'location_text'=>'DE','affiliate_url'=>'https://example.test/a','item_web_url'=>'https://example.test/a','image_url'=>'https://example.test/a.jpg',
        'item_end_at'=>0,'source_hash'=>hash('sha256','ci-business-a'),'source_payload'=>'{}','status'=>'active','source_state'=>'available',
        'policy_state'=>'allowed','route_state'=>'ready','output_state'=>'candidate','policy_version'=>'ci','classifier_version'=>'ci',
        'source_checked_at'=>$now,'rejection_reason'=>'','last_seen'=>$now,'fresh_until'=>$now+3600,'created_at'=>$now,'updated_at'=>$now,
    ));
    $assert($inserted === 1, 'eBay BUSINESS DB fixture inserted');

    $rmEbay = new ReflectionMethod($o, 'ebay_business_campaign_source_row');
    $rmEbay->setAccessible(true);
    $campaign = array('network'=>'ebay','post_id'=>(int) $postA);
    $before = (int) $wpdb->num_queries;
    $row = array();
    for ($i = 0; $i < 1484; $i++) { $row = $rmEbay->invoke($o, $campaign); }
    $delta = (int) $wpdb->num_queries - $before;
    $assert($delta === 1, '1484 identical eBay BUSINESS reads collapse to exactly 1 DB query');
    $assert(is_array($row) && ($row['item_id'] ?? '') === 'ci-business-a' && ($row['seller_account_type'] ?? '') === 'BUSINESS', 'eBay BUSINESS result unchanged');

    $hashMissing = str_repeat('c', 64);
    $postMissing = wp_insert_post(array('post_type'=>'post','post_status'=>'draft','post_title'=>'CI eBay missing'));
    update_post_meta((int) $postMissing, '_ppar_ebay_business_auto', 1);
    update_post_meta((int) $postMissing, '_ppar_creative_identity_hash', $hashMissing);
    get_post_meta((int) $postMissing);
    $before = (int) $wpdb->num_queries;
    $empty = null;
    for ($i = 0; $i < 100; $i++) { $empty = $rmEbay->invoke($o, array('network'=>'ebay','post_id'=>(int) $postMissing)); }
    $delta = (int) $wpdb->num_queries - $before;
    $assert($delta === 1 && $empty === array(), 'missing eBay BUSINESS row cached safely');

    $hashPrivate = str_repeat('e', 64);
    $postPrivate = wp_insert_post(array('post_type'=>'post','post_status'=>'draft','post_title'=>'CI eBay private'));
    update_post_meta((int) $postPrivate, '_ppar_ebay_business_auto', 1);
    update_post_meta((int) $postPrivate, '_ppar_creative_identity_hash', $hashPrivate);
    get_post_meta((int) $postPrivate);
    $wpdb->insert($ebayTable, array(
        'portal_key'=>$portal,'item_id'=>'ci-private','legacy_item_id'=>'','seller_account_type'=>'INDIVIDUAL','seller_username'=>'ci',
        'route_mode'=>'listing','rule_id'=>'ci','target_term_id'=>0,'listing_post_id'=>0,'creative_identity_hash'=>$hashPrivate,
        'title'=>'CI PRIVATE','short_description'=>'','condition_text'=>'Used','price_value'=>'10','currency'=>'EUR','shipping_value'=>'0',
        'location_text'=>'DE','affiliate_url'=>'https://example.test/p','item_web_url'=>'https://example.test/p','image_url'=>'https://example.test/p.jpg',
        'item_end_at'=>0,'source_hash'=>hash('sha256','ci-private'),'source_payload'=>'{}','status'=>'active','source_state'=>'available',
        'policy_state'=>'allowed','route_state'=>'ready','output_state'=>'listing_pending','policy_version'=>'ci','classifier_version'=>'ci',
        'source_checked_at'=>$now,'rejection_reason'=>'','last_seen'=>$now,'fresh_until'=>$now+3600,'created_at'=>$now,'updated_at'=>$now,
    ));
    $private = $rmEbay->invoke($o, array('network'=>'ebay','post_id'=>(int) $postPrivate));
    $assert($private === array(), 'PRIVATE seller cannot satisfy BUSINESS lookup');

    $creativeTable = $wpdb->prefix . 'ppar_creative_library';
    $creativeInserted = $wpdb->insert($creativeTable, array(
        'provider'=>'awin','partner_external_id'=>'ci','partner_name'=>'CI','external_id'=>'ci-a','identity_hash'=>$hashA,
        'creative_type'=>'banner','title'=>'CI Creative A','description'=>'','tags'=>'horse','image_url'=>'https://example.test/banner.jpg',
        'destination_url'=>'https://example.test/horse','tracking_url'=>'https://example.test/track','width'=>728,'height'=>90,
        'source_status'=>'active','source_kind'=>'banner','availability_state'=>'active','missing_count'=>0,'last_complete_run'=>'',
        'review_status'=>'approved','selected'=>1,'content_scope'=>'horse','scope_source'=>'ci','classified_at'=>$now,
        'topic_status'=>'auto_verified','topic_score'=>100,'topic_targets'=>'[]','source_hash'=>hash('sha256','ci-creative-a'),
        'payload'=>'{}','first_seen'=>$now,'last_seen'=>$now,
    ));
    $assert($creativeInserted === 1, 'creative DB fixture inserted');

    $rmCreative = new ReflectionMethod($o, 'output_creative_row');
    $rmCreative->setAccessible(true);
    $before = (int) $wpdb->num_queries;
    $creative = null;
    for ($i = 0; $i < 305; $i++) { $creative = $rmCreative->invoke($o, $hashA); }
    $delta = (int) $wpdb->num_queries - $before;
    $assert($delta === 1, '305 identical creative reads collapse to exactly 1 DB query');
    $assert(is_array($creative) && ($creative['title'] ?? '') === 'CI Creative A', 'creative result unchanged');

    $hashCreativeMissing = str_repeat('d', 64);
    $before = (int) $wpdb->num_queries;
    $creativeMissing = 'sentinel';
    for ($i = 0; $i < 100; $i++) { $creativeMissing = $rmCreative->invoke($o, $hashCreativeMissing); }
    $delta = (int) $wpdb->num_queries - $before;
    $assert($delta === 1 && $creativeMissing === null, 'missing creative row cached safely');

    echo "REAL_WORDPRESS_MARIADB_PERFORMANCE_CACHE_PASS\n";
    exit;
}, 0);
