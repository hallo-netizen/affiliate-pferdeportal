<?php
/**
 * Hab & Bewahr project adapter for the existing, unmodified Affiliate engine.
 *
 * Reads ONLY the active, revision-bound WordPress category snapshot from the
 * Hab & Bewahr category workflow. No horse/hobby catalog, sample URLs, or
 * credentials are bundled. A missing/inconsistent snapshot fails CLOSED.
 */
if (!defined('ABSPATH')) { exit; }

final class PPAR_HB_Design_Contract {
    const VERSION = '0.1.189';
    public static function design_profile() { return 'portal'; }
    public static function affiliate_contract_version() { return '1.0'; }
    public static function affiliate_page_type($page_id) {
        $page_id = absint($page_id);
        if ($page_id < 1) { return ''; }
        foreach (PPAR_HB_Integration::verified_nodes() as $node) {
            if (($node['type'] ?? '') !== 'page' || (int)($node['wp_id'] ?? 0) !== $page_id) { continue; }
            $key = (string)($node['id'] ?? '');
            if ($key === 'core:hub') { return 'start'; }
            if (strpos($key, 'core:world:') === 0) { return 'hub1'; }
            if (strpos($key, 'core:area:') === 0 || strpos($key, 'core:c22:area:') === 0) { return 'hub2'; }
            if (strpos($key, 'editorial:') === 0) { return 'journal'; }
            return 'leaf';
        }
        return '';
    }
}

final class PPAR_HB_Integration {
    private static $nodes = null;
    private static $catalog = null;

    public static function bootstrap() {
        add_filter('ppar_portal_source_catalog', array(__CLASS__, 'catalog'), 10, 1);
        add_filter('ppar_affiliate_slot_matrix', array(__CLASS__, 'slot_matrix'), 10, 3);
        add_filter('hbdp_article_product_cards_html', array(__CLASS__, 'article_products'), 10, 3);
        add_filter('hbdp_article_auto_banner_html', array(__CLASS__, 'article_banner'), 10, 3);
        add_filter('hbdp_area_product_cards_html', array(__CLASS__, 'area_products'), 10, 2);
        add_filter('hbdp_area_auto_banner_html', array(__CLASS__, 'area_banner'), 10, 2);
    }

    public static function verified_nodes() {
        if (self::$nodes !== null) { return self::$nodes; }
        self::$nodes = array();
        $revision = (string) get_option('apkw_target_tree_active_revision_v1', '');
        $snapshot = get_option('apkw_target_tree_active_snapshot_v1', array());
        if ($revision === '' || !is_array($snapshot)
            || (string)($snapshot['revision'] ?? '') !== $revision
            || !is_array($snapshot['nodes'] ?? null)
            || !is_array($snapshot['mapping'] ?? null)) {
            return self::$nodes;
        }

        foreach ($snapshot['nodes'] as $entry) {
            if (!is_array($entry)) { continue; }
            $key = (string)($entry['node_id'] ?? '');
            if ($key === '' || (string)($entry['pillar'] ?? 'core') !== 'core') { continue; }
            $mapping = $snapshot['mapping'][$key] ?? null;
            if (!is_array($mapping)) { continue; }
            $type = (string)($mapping['object_type'] ?? $entry['object_type'] ?? '');
            $id = absint($mapping['object_id'] ?? 0);
            if ($id < 1 || !in_array($type, array('page','category'), true)) { continue; }
            $label = sanitize_text_field((string)($entry['display_name'] ?? $entry['name'] ?? ''));
            $slug = sanitize_title((string)($entry['slug'] ?? ''));
            if ($label === '' || $slug === '') { continue; }
            self::$nodes[$key] = array(
                'id'=>$key, 'type'=>$type, 'wp_id'=>$id, 'name'=>$label,
                'slug'=>$slug, 'parent'=>(string)($entry['parent_id'] ?? ''),
            );
        }
        $pages = 0; $categories = 0;
        foreach (self::$nodes as $row) {
            if ($row['type'] === 'page') { $pages++; }
            if ($row['type'] === 'category') { $categories++; }
        }
        // Reject a broken/unimported tree, never fall back to an archived graph.
        if ($pages < 30 || $categories < 30) { self::$nodes = array(); }
        return self::$nodes;
    }

    private static function ancestors($node, $nodes) {
        $result = array(); $seen = array(); $cursor = (string)($node['parent'] ?? '');
        for ($i=0; $i<12 && $cursor !== '' && isset($nodes[$cursor]) && !isset($seen[$cursor]); $i++) {
            $seen[$cursor]=true; $result[]=$nodes[$cursor]; $cursor=(string)($nodes[$cursor]['parent'] ?? '');
        }
        return $result;
    }

    private static function product_topic($label) {
        // Narrow, concrete PRODUCT families only. Security intents such as
        // "Was tun nach Einbruch" and broad categories are never products.
        $phrase = strtolower(remove_accents((string)$label));
        $allowed = array(
            'wassermelder','wasserstopp','leckmelder','rauchmelder','co-melder',
            'kohlenmonoxidmelder','gaswarnmelder','alarmmelder','alarmanlage',
            'tresor','sicherheitskamera','uberwachungskamera','videokamera',
            'turkamera','videotursprechanlage','bewegungsmelder','fensterkontakt',
            'turschloss','schliesszylinder','feuerloscher','ruckstauklappe',
            'rueckstauklappe','stromausfallmelder','gps-tracker','gps tracker',
            'einbruchmelder','fenstersicherung','tursicherung','garagentorschloss',
        );
        foreach ($allowed as $needle) {
            if (strpos($phrase, $needle) !== false) { return true; }
        }
        return false;
    }

    public static function catalog($previous = null) {
        if ($previous instanceof WP_Error) { return $previous; }
        // Never mix externally injected target objects with the local catalog.
        if (is_array($previous) && !empty($previous)) {
            return new WP_Error('hb_multiple_catalogs', 'Mehrere Portal-Zielquellen sind gleichzeitig aktiv.');
        }
        if (self::$catalog !== null) { return self::$catalog; }
        $nodes = self::verified_nodes();
        if (!$nodes) {
            return new WP_Error('hb_active_tree_missing', 'Aktueller Hab-&-Bewahr-Kategoriebaum fehlt oder ist unvollständig.');
        }

        $worlds = array(); $products = array(); $concepts = array(); $articles = array(); $rules = array();
        foreach ($nodes as $n) {
            if ($n['type'] === 'page' && strpos($n['id'],'core:world:') === 0) {
                $worlds[$n['id']] = array(
                    'label'=>$n['name'], 'phrases'=>array(), 'strong_phrases'=>array(),
                    'slug'=>$n['slug'],
                );
            }
        }
        if (count($worlds) < 6 || count($worlds) > 8) {
            return new WP_Error('hb_worlds_unexpected','Der aktiv zugeordnete Schutzweltbestand ist nicht plausibel.');
        }
        foreach ($nodes as $n) {
            $chain = self::ancestors($n, $nodes);
            $parent = $chain[0] ?? array();
            $world = array();
            foreach ($chain as $ancestor) {
                if (isset($worlds[$ancestor['id']])) { $world=$ancestor; break; }
            }
            if (!$world) { continue; }
            $world_slug = (string)$world['slug'];
            if ($n['type'] === 'page' && count($chain) >= 2
                && $parent && $parent['type'] === 'page'
                && self::product_topic($n['name'])) {
                // No guessed URL: only a real mapped, publicly visible page.
                if (function_exists('get_post_status') && get_post_status($n['wp_id']) !== 'publish') { continue; }
                $target = array(
                    'slug'=>$n['slug'], 'title'=>$n['name'],
                    'description'=>'Sicherheitstechnik zum Thema '.$n['name'],
                    'hub'=>$parent['name'], 'hub_slug'=>$parent['slug'],
                    'main_hub'=>$world['name'], 'main_slug'=>$world_slug,
                    'private_bucket_slug'=>$world_slug,
                    'normalized'=>sanitize_title($n['name'].' '.$parent['name']),
                    'node_id'=>$n['id']
                );
                $products[]=$target;
                $cid='hb-'.sanitize_key($n['slug']);
                $concepts[] = array(
                    'id'=>$cid, 'title'=>$n['name'],
                    'normalized_title'=>sanitize_title($n['name']),
                    'target_pages'=>array($target),
                    'private_bucket_slugs'=>array($world_slug),
                    'hub_slugs'=>array($parent['slug']),
                    'main_slugs'=>array($world_slug),
                    'private_bucket_slug'=>$world_slug,
                );
                $rules[] = array(
                    'id'=>$cid,'label'=>$n['name'],'query'=>$n['name'],
                    'business_concept_id'=>$cid,
                    'target_term_slug'=>$world_slug,
                    'candidate_main_slugs'=>array($world_slug),
                    'candidate_buckets'=>array($world_slug),
                    'private'=>true,'business'=>true,'active'=>true,
                );
                $worlds[$world['id']]['phrases'][]=$n['name'];
                $worlds[$world['id']]['strong_phrases'][]=$n['name'];
            }
        }
        $by_slug = array();
        foreach ($products as $p) { $by_slug[$p['slug']] = $p; }
        foreach ($nodes as $n) {
            if ($n['type'] !== 'category') { continue; }
            $chain = self::ancestors($n,$nodes);
            $parent=$chain[0] ?? array();
            $world=array();
            foreach ($chain as $ancestor) {
                if (isset($worlds[$ancestor['id']])) { $world=$ancestor; break; }
            }
            if (!$parent || !$world) { continue; }
            $product = $by_slug[(string)($parent['slug'] ?? '')] ?? array();
            $articles[] = array(
                'category_slug'=>$n['slug'], 'category_name'=>$n['name'],
                'product'=>(string)($product['title'] ?? ''),
                'product_slug'=>(string)($product['slug'] ?? ''),
                'hub'=>$parent['name'], 'hub_slug'=>$parent['slug'],
                'main_hub'=>$world['name'], 'main_slug'=>$world['slug'],
                'theme'=>$n['name'],
                'path'=>$world['name'].' > '.$parent['name'].' > '.$n['name'],
                'node_id'=>$n['id'],
            );
        }
        if (count($products) < 3 || count($articles) < 30 || !$rules || !$concepts) {
            return new WP_Error('hb_catalog_requires_review', 'Noch nicht genügend eindeutig zugeordnete, veröffentlichte Produktseiten für automatische eBay-Auswahl.');
        }
        $profiles=array();
        foreach ($worlds as $entry) {
            $profiles[$entry['slug']] = array(
                'label'=>$entry['label'],
                'phrases'=>array_values(array_unique($entry['phrases'])),
                'strong_phrases'=>array_values(array_unique($entry['strong_phrases'])),
            );
        }
        $revision = (string) get_option('apkw_target_tree_active_revision_v1', '');
        self::$catalog = array(
            'schema'=>'hb-verified-wp-catalog-v1', 'source_revision'=>$revision,
            'source_sha256'=>hash('sha256',$revision.'|'.count($nodes).'|'.count($articles)),
            'counts'=>array(
                'worlds'=>count($worlds),'main_hubs'=>count($worlds),
                'hub_pages'=>count($nodes)-count($articles),
                'product_pages'=>count($products),'article_categories'=>count($articles),
                'business_concepts'=>count($concepts),
            ),
            'product_targets'=>$products, 'article_targets'=>$articles,
            'search_rules'=>$rules,'business_concepts'=>$concepts,
            'business_hub_concepts'=>array(),'private_bucket_profiles'=>$profiles,
            'hard_negative_markers'=>array(), 'strong_domain_markers'=>array(),
            'content_policy'=>array(
                'version'=>'hb-v1','mode'=>'EXACT_OR_STRONG_TARGET_EVIDENCE_FAIL_CLOSED',
            ),
            'business_supply_contract'=>array(
                'version'=>'hb-v1','required_count'=>count($concepts),
                'required_product_concept_ids'=>array_column($concepts,'id'),
            ),
        );
        return self::$catalog;
    }

    public static function slot_matrix($matrix, $portal = array(), $version = '') {
        $matrix = is_array($matrix) ? $matrix : array();
        // This site only. An external/multisite adapter keeps its own contract.
        if (($portal['adapter'] ?? '') !== 'wordpress_local' || !self::verified_nodes()) { return $matrix; }
        $wide = array(
            'creative_type'=>'banner','ratio_min'=>2.5,'ratio_max'=>12,
            'min_width'=>300,'min_height'=>60,'crop'=>'contain',
            'target_types'=>array('page','category'),
            'target_contexts'=>array(),'upscale_max'=>1.1,'min_fill'=>0.6,
        );
        $card = array(
            'creative_type'=>'product','ratio_min'=>0.55,'ratio_max'=>2,
            'min_width'=>160,'min_height'=>160,'crop'=>'contain',
            'target_types'=>array('page','post','category'),
            'target_contexts'=>array(),
        );
        $slots = array(
            'start_after_topics'=>$wide,
            'hub_after_cards'=>$wide,
            'product_after_category_tiles'=>$wide,
            'journal_banner'=>$wide,
            'anzeigenmarkt_top_banner'=>$wide,
            'anzeigenmarkt_category_banner'=>array_merge($wide,array('target_types'=>array('hp_listing_category'))),
            'post_inline_banner'=>array_merge($wide,array('target_types'=>array('post'))),
            'glossary_single_desktop_banner'=>array_merge($wide,array('target_types'=>array('hbdp_glossar_term'),'device'=>'desktop')),
            'glossary_single_mobile_banner'=>array_merge($wide,array('target_types'=>array('hbdp_glossar_term'),'device'=>'mobile')),
            'glossary_overview_banner'=>$wide,
            'post_bottom_products'=>array_merge($card,array('target_types'=>array('post'))),
        );
        foreach (array('hub_product_1','hub_product_2','hub_product_3',
                       'category_product_1','category_product_2','category_product_3',
                       'journal_product_1','journal_product_2','journal_product_3') as $slot) {
            $slots[$slot]=$card;
        }
        // Never override a separately approved slot rule with a conflicting rule.
        return array_merge($slots,$matrix);
    }

    private static function eligible_post($post_id) {
        if (!function_exists('get_post_type') || get_post_type($post_id) !== 'post'
            || !function_exists('get_post_status') || get_post_status($post_id) !== 'publish') { return false; }
        if ((string)get_post_meta($post_id,'_hbdp_article_no_ads',true) === '1') { return false; }
        $post=function_exists('get_post')?get_post($post_id):null;
        if ($post && function_exists('hbdp_article_is_urgent') && hbdp_article_is_urgent($post)) { return false; }
        return true;
    }
    public static function article_products($html, $post_id = 0, $categories = array()) {
        if (is_string($html) && trim($html) !== '') { return $html; }
        $post_id=absint($post_id);
        if (!self::eligible_post($post_id) || !class_exists('Portal_Affiliate_Router')) { return ''; }
        return Portal_Affiliate_Router::instance()->hab_bw_article_slot($post_id,'products');
    }
    public static function article_banner($html, $post_id = 0, $categories = array()) {
        if (is_string($html) && trim($html) !== '') { return $html; }
        $post_id=absint($post_id);
        if (!self::eligible_post($post_id) || !class_exists('Portal_Affiliate_Router')) { return ''; }
        return Portal_Affiliate_Router::instance()->hab_bw_article_slot($post_id,'banner');
    }
    private static function area($html, $node_id, $kind) {
        if (is_string($html) && trim($html) !== '') { return $html; }
        $nodes=self::verified_nodes(); $node=$nodes[(string)$node_id] ?? array();
        if (($node['type'] ?? '') !== 'page' || !class_exists('Portal_Affiliate_Router')) { return ''; }
        $id=(int)$node['wp_id'];
        if (function_exists('get_post_status') && get_post_status($id) !== 'publish') { return ''; }
        return Portal_Affiliate_Router::instance()->hab_bw_area_slot($id,$kind);
    }
    public static function area_products($html, $node_id = '') { return self::area($html,$node_id,'products'); }
    public static function area_banner($html, $node_id = '') { return self::area($html,$node_id,'banner'); }
}
