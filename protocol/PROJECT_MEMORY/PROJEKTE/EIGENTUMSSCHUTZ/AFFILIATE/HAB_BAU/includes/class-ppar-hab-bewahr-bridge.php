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
        $node = PPAR_HB_Integration::page_for_id($page_id);
        if ($node) {
            $key = (string)($node['id'] ?? '');
            if ($key === 'core:hub') { return 'start'; }
            if (strpos($key, 'core:world:') === 0) { return 'hub1'; }
            if (strpos($key, 'core:area:') === 0 || strpos($key, 'core:c22:area:') === 0) { return 'hub2'; }
            if (strpos($key, 'editorial:') === 0) { return 'journal'; }
            if (strpos($key, 'directory:') === 0) { return 'anzeigenmarkt'; }
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
        add_filter('hbdp_world_auto_banner_html', array(__CLASS__, 'world_banner'), 10, 2);
        add_filter('hbdp_editorial_banner_html', array(__CLASS__, 'editorial_banner'), 10, 3);
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
            if ($key === '' || !in_array((string)($entry['pillar'] ?? 'core'), array('core','editorial','directory'), true)) { continue; }
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
                'pillar'=>(string)($entry['pillar'] ?? ''),
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

    /** O(1) lookup: avoid a full 500+-node scan on every banner candidate. */
    public static function page_for_id($wp_id) {
        static $index = null;
        if ($index === null) {
            $index = array();
            foreach (self::verified_nodes() as $node) {
                if ($node['type'] !== 'page') { continue; }
                $key = (int)$node['wp_id'];
                if (!isset($index[$key])) { $index[$key] = $node; }
                elseif (strpos($node['id'], 'core:c22:') === 0) { $index[$key] = $node; }
            }
        }
        return $index[absint($wp_id)] ?? array();
    }

    private static function ancestors($node, $nodes) {
        $result = array(); $seen = array(); $cursor = (string)($node['parent'] ?? '');
        for ($i=0; $i<12 && $cursor !== '' && isset($nodes[$cursor]) && !isset($seen[$cursor]); $i++) {
            $seen[$cursor]=true; $result[]=$nodes[$cursor]; $cursor=(string)($nodes[$cursor]['parent'] ?? '');
        }
        return $result;
    }

    /**
     * Extract actual, concrete product families from live WordPress CATEGORY names.
     * Never turn broad topic pages (e.g. "Einbruch & Diebstahl") into products.
     * This is a guarded noun recognizer, NOT a list of invented target pages.
     */
    private static function product_family($name) {
        $text = strtolower(remove_accents(sanitize_text_field((string)$name)));
        $products = array(
            'wassermelder'=>'Wassermelder','wasserstopp'=>'Wasserstopp',
            'rauchmelder'=>'Rauchmelder','gaswarnmelder'=>'Gaswarnmelder',
            'kohlenmonoxidmelder'=>'Kohlenmonoxidmelder',
            'co-melder'=>'CO-Melder','stromausfallmelder'=>'Stromausfallmelder',
            'alarmmelder'=>'Alarmmelder','alarmanlage'=>'Alarmanlage',
            'bewegungsmelder'=>'Bewegungsmelder','fensterkontakt'=>'Fensterkontakt',
            'rueckstauklappe'=>'Rückstauklappe','ruckstauklappe'=>'Rückstauklappe',
            'hebeanlage'=>'Hebeanlage','sumpfpumpe'=>'Sumpfpumpe',
            'tresor'=>'Tresor','feuerloscher'=>'Feuerlöscher',
            'gps-tracker'=>'GPS-Tracker','leckmelder'=>'Leckmelder',
            'sicherheitskamera'=>'Sicherheitskamera','videotursprechanlage'=>'Video-Türsprechanlage',
            'turschloss'=>'Türschloss','schliesszylinder'=>'Schließzylinder',
            'usv'=>'USV','powerstation'=>'Powerstation',
            'notstrom'=>'Notstromgerät','luftentfeuchter'=>'Luftentfeuchter',
            'frostwachter'=>'Frostwächter','schwimmerschalter'=>'Schwimmerschalter',
            'ruckschlagventil'=>'Rückschlagventil','ueberspannungsschutz'=>'Überspannungsschutz',
        );
        // Longest literal words first, so "Stromausfallmelder" does not also
        // match a broader "Alarmmelder" and generate duplicate product profiles.
        uksort($products, static function($a,$b){ return strlen($b) <=> strlen($a); });
        foreach ($products as $needle=>$canonical) {
            $needle = strtolower(remove_accents((string)$needle));
            if (strpos($text, $needle) !== false) {
                // Word boundaries prevent matching advice/brand fragments.
                $pattern='~(?<![a-z])'.preg_quote($needle,'~').'(?![a-z])~';
                if (preg_match($pattern,$text)) { return $canonical; }
            }
        }
        return '';
    }

    private static function nearest_page($node, $nodes) {
        foreach (self::ancestors($node, $nodes) as $parent) {
            if (($parent['type'] ?? '') === 'page') { return $parent; }
        }
        return array();
    }

    public static function catalog($previous = null) {
        if ($previous instanceof WP_Error) { return $previous; }
        if (is_array($previous) && !empty($previous)) {
            return new WP_Error('hb_multiple_catalogs', 'Mehrere Portal-Zielquellen sind gleichzeitig aktiv.');
        }
        if (self::$catalog !== null) { return self::$catalog; }
        $nodes = self::verified_nodes();
        if (!$nodes || !isset($nodes['core:hub'])) {
            return new WP_Error('hb_active_tree_missing', 'Aktueller Hab-&-Bewahr-Kategoriebaum fehlt oder ist unvollständig.');
        }

        $worlds = array(); $products = array(); $concepts = array(); $articles = array(); $rules = array();
        foreach ($nodes as $n) {
            if (($n['pillar'] ?? '') === 'core' && $n['type'] === 'page'
                && strpos($n['id'], 'core:world:') === 0) {
                $worlds[$n['id']] = array(
                    'name'=>$n['name'], 'label'=>$n['name'], 'id'=>$n['id'],
                    'slug'=>$n['slug'], 'phrases'=>array(), 'strong_phrases'=>array(),
                );
            }
        }
        if (count($worlds) !== 6) {
            return new WP_Error('hb_worlds_unexpected', 'Der aktive Hab-&-Bewahr-Bestand muss sechs Schutzwelten enthalten.');
        }

        $seen_concepts = array();
        foreach ($nodes as $n) {
            if (($n['pillar'] ?? '') !== 'core' || $n['type'] !== 'category') { continue; }
            $chain = self::ancestors($n,$nodes);
            $world = array(); $parent = self::nearest_page($n,$nodes);
            foreach ($chain as $ancestor) {
                if (isset($worlds[$ancestor['id']])) { $world=$worlds[$ancestor['id']]; break; }
            }
            if (!$parent || !$world) { continue; }
            $category_label = (string)$n['name'];
            $family = self::product_family($category_label);
            $target_slug = '';
            // Use only real, already mapped PUBLISHED WordPress pages. The
            // category itself is the product identity; the page is its parent.
            if ($family !== '' && $parent['id'] !== $world['id']
                && function_exists('get_post_status')
                && get_post_status((int)$parent['wp_id']) === 'publish') {
                $cid = 'hb-' . sanitize_key($world['slug'] . '-' . $n['slug']);
                $target_slug = (string)$parent['slug'];
                // A product concept is category-specific and unambiguous; another
                // category that shares the parent page does not inherit it.
                $unique = $world['slug'].'|'.$family.'|'.$target_slug;
                if (!isset($seen_concepts[$unique]) && count($rules) < 50) {
                    $seen_concepts[$unique] = true;
                    $target = array(
                        'slug'=>$target_slug, 'title'=>$family,
                        'description'=>'Produktkontext: ' . $category_label,
                        'hub'=>$parent['name'], 'hub_slug'=>$parent['slug'],
                        'main_hub'=>$world['name'], 'main_slug'=>$world['slug'],
                        'private_bucket_slug'=>$world['slug'],
                        'normalized'=>sanitize_title($family.' '.$category_label),
                        'node_id'=>$parent['id'], 'category_slug'=>$n['slug'],
                    );
                    $products[]=$target;
                    $concepts[] = array(
                        'id'=>$cid, 'title'=>$family,
                        'normalized_title'=>sanitize_title($family),
                        'target_pages'=>array($target),
                        'private_bucket_slugs'=>array($world['slug']),
                        'hub_slugs'=>array($parent['slug']),
                        'main_slugs'=>array($world['slug']),
                        'private_bucket_slug'=>$world['slug'],
                    );
                    $rules[] = array(
                        'id'=>$cid,'label'=>$family,'query'=>$family,
                        'business_concept_id'=>$cid,
                        'target_term_slug'=>$world['slug'],
                        'candidate_main_slugs'=>array($world['slug']),
                        'candidate_buckets'=>array($world['slug']),
                        'private'=>true, 'business'=>true, 'active'=>true,
                    );
                    $worlds[$world['id']]['phrases'][]=$family;
                    $worlds[$world['id']]['strong_phrases'][]=$family;
                }
            }
            // ALL existing article categories remain reachable, whether or
            // not they carry a concretely identifiable product family.
            $articles[] = array(
                'category_slug'=>$n['slug'],'category_name'=>$category_label,
                'product'=>$family, 'product_slug'=>$target_slug,
                'hub'=>$parent['name'],'hub_slug'=>$parent['slug'],
                'main_hub'=>$world['name'],'main_slug'=>$world['slug'],
                'theme'=>$category_label,
                'path'=>$world['name'].' > '.$parent['name'].' > '.$category_label,
                'node_id'=>$n['id'],
            );
        }
        if (!$rules || !$products || count($articles) < 30) {
            return new WP_Error('hb_catalog_requires_review','Keine eindeutig zuordenbaren Produktkategorien oder zu wenige echte Artikelkategorien im aktuellen Hab-&-Bewahr-Baum.');
        }
        $profiles=array();
        foreach ($worlds as $entry) {
            $profiles[$entry['slug']] = array(
                'label'=>$entry['label'],
                'phrases'=>array_values(array_unique($entry['phrases'])),
                'strong_phrases'=>array_values(array_unique($entry['strong_phrases'])),
            );
        }
        $revision=(string)get_option('apkw_target_tree_active_revision_v1','');
        $pages=0;
        foreach($nodes as $n) { if(($n['pillar'] ?? '')==='core' && $n['type']==='page') $pages++; }
        self::$catalog=array(
            'schema'=>'hb-active-wp-category-products-v2', 'source_revision'=>$revision,
            'source_sha256'=>hash('sha256',$revision.'|'.wp_json_encode(array_keys($nodes)).'|'.wp_json_encode($rules)),
            'counts'=>array(
                'worlds'=>6, 'main_hubs'=>6,
                'hub_pages'=>max(0,$pages-7),
                'product_pages'=>count($products),
                'article_categories'=>count($articles),
                'business_concepts'=>count($concepts),
            ),
            'product_targets'=>$products,'article_targets'=>$articles,
            'search_rules'=>$rules,'business_concepts'=>$concepts,
            'business_hub_concepts'=>array(),
            'private_bucket_profiles'=>$profiles,
            'hard_negative_markers'=>array(),'strong_domain_markers'=>array(),
            'content_policy'=>array(
                'version'=>'hb-v2','mode'=>'EXACT_OR_STRONG_TARGET_EVIDENCE_FAIL_CLOSED',
            ),
            'business_supply_contract'=>array(
                'version'=>'hb-v2','required_count'=>count($concepts),
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
