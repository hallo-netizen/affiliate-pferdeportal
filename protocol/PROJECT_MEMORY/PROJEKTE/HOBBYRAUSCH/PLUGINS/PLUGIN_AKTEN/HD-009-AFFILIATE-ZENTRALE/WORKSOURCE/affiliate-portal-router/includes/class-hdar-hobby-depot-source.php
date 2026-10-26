<?php
/**
 * Hobby Depot portal source adapter for HD-009.
 *
 * Single truth: HD-004 read-only category registry.
 * No copied category/product master is stored in this plugin.
 */
if (!defined('ABSPATH')) { exit; }

final class HDAR_Hobby_Depot_Source {
    private static $catalog = null;

    private static function text($value) {
        $value = wp_strip_all_tags((string)$value);
        $value = remove_accents($value);
        $value = strtolower($value);
        $value = preg_replace('/[^a-z0-9]+/u', ' ', $value);
        return trim(preg_replace('/\s+/', ' ', $value));
    }

    private static function path_labels($node_id, $nodes) {
        $labels = array();
        $seen = array();
        $cursor = (string)$node_id;
        while ($cursor !== '' && isset($nodes[$cursor]) && !isset($seen[$cursor])) {
            $seen[$cursor] = true;
            $node = $nodes[$cursor];
            $label = sanitize_text_field((string)($node['display_name'] ?? $node['name'] ?? ''));
            if ($label !== '') { array_unshift($labels, $label); }
            $cursor = (string)($node['parent_id'] ?? '');
        }
        return $labels;
    }

    private static function ancestor($node_id, $nodes, $predicate) {
        $seen = array();
        $cursor = (string)$node_id;
        while ($cursor !== '' && isset($nodes[$cursor]) && !isset($seen[$cursor])) {
            $seen[$cursor] = true;
            $node = $nodes[$cursor];
            if (call_user_func($predicate, $node, $cursor)) { return $node; }
            $cursor = (string)($node['parent_id'] ?? '');
        }
        return array();
    }

    public static function catalog() {
        if (is_array(self::$catalog)) { return self::$catalog; }
        if (!function_exists('hd_category_registry_ready') || !hd_category_registry_ready()
            || !function_exists('hd_category_registry_snapshot')) {
            return new WP_Error('hdar_category_registry_unavailable', 'Hobby-Depot-Kategorie-Registry ist nicht bereit.');
        }

        $snapshot = hd_category_registry_snapshot();
        if (!is_array($snapshot) || empty($snapshot['nodes']) || !is_array($snapshot['nodes'])) {
            return new WP_Error('hdar_category_snapshot_invalid', 'Hobby-Depot-Kategorie-Snapshot ist leer oder ungültig.');
        }

        $nodes = array();
        foreach ($snapshot['nodes'] as $node) {
            if (!is_array($node)) { continue; }
            $id = (string)($node['node_id'] ?? '');
            if ($id === '' || (string)($node['pillar'] ?? '') !== 'core' || (string)($node['status'] ?? 'active') !== 'active') { continue; }
            $nodes[$id] = $node;
        }
        if (!$nodes) {
            return new WP_Error('hdar_category_snapshot_no_core', 'Hobby-Depot-Snapshot enthält keine aktiven CORE-Knoten.');
        }

        $worlds = array();
        $hobbies = array();
        foreach ($nodes as $id => $node) {
            if (preg_match('/^core:world:[^:]+$/', $id)) { $worlds[$id] = $node; }
            if (preg_match('/^core:hobby:[^:]+$/', $id) && (string)($node['object_type'] ?? '') === 'page') { $hobbies[$id] = $node; }
        }
        if (count($worlds) !== 8) {
            return new WP_Error('hdar_world_count_invalid', 'Hobby Depot muss exakt acht aktive CORE-Welten liefern.');
        }
        if (!$hobbies) {
            return new WP_Error('hdar_hobby_targets_missing', 'Hobby-Depot-Snapshot enthält keine aktiven CORE-Hobbyseiten.');
        }

        $product_targets = array();
        $business_concepts = array();
        $world_profiles = array();
        foreach ($worlds as $world_id => $world) {
            $world_slug = sanitize_title((string)($world['slug'] ?? ''));
            $world_label = sanitize_text_field((string)($world['display_name'] ?? ''));
            if ($world_slug === '' || $world_label === '') { continue; }
            $world_profiles[$world_slug] = array(
                'label' => $world_label,
                'phrases' => array(),
                'strong_phrases' => array(),
            );
        }

        foreach ($hobbies as $id => $node) {
            $slug = sanitize_title((string)($node['slug'] ?? ''));
            $title = sanitize_text_field((string)($node['display_name'] ?? ''));
            if ($slug === '' || $title === '') { continue; }
            $world = self::ancestor($id, $nodes, static function($n, $nid){ return preg_match('/^core:world:[^:]+$/', (string)$nid) === 1; });
            $world_slug = sanitize_title((string)($world['slug'] ?? ''));
            $world_label = sanitize_text_field((string)($world['display_name'] ?? ''));
            if ($world_slug === '' || !isset($world_profiles[$world_slug])) { continue; }

            $parent_id = (string)($node['parent_id'] ?? '');
            $parent = isset($nodes[$parent_id]) ? $nodes[$parent_id] : array();
            $hub = sanitize_text_field((string)($parent['display_name'] ?? $world_label));
            $hub_slug = sanitize_title((string)($parent['slug'] ?? $world_slug));
            $normalized = self::text($title . ' ' . $hub . ' ' . $world_label);

            $target = array(
                'slug'=>$slug,
                'title'=>$title,
                'description'=>'Produkt- und Zubehörrecherche für das Hobby ' . $title . '.',
                'hub'=>$hub,
                'hub_slug'=>$hub_slug,
                'main_hub'=>$world_label,
                'main_slug'=>$world_slug,
                'private_bucket_slug'=>$world_slug,
                'normalized'=>$normalized,
                'node_id'=>$id,
            );
            $product_targets[] = $target;
            $business_concepts[] = array(
                'id'=>'concept-' . sanitize_key($slug),
                'title'=>$title,
                'normalized_title'=>self::text($title),
                'target_pages'=>array($target),
                'private_bucket_slugs'=>array($world_slug),
                'hub_slugs'=>array($hub_slug),
                'main_slugs'=>array($world_slug),
                'private_bucket_slug'=>$world_slug,
            );
            $world_profiles[$world_slug]['phrases'][] = $title;
            $world_profiles[$world_slug]['strong_phrases'][] = $title;
        }

        $article_targets = array();
        foreach ($nodes as $id => $node) {
            if ((string)($node['object_type'] ?? '') !== 'category') { continue; }
            $hobby = self::ancestor($id, $nodes, static function($n, $nid){ return preg_match('/^core:hobby:[^:]+$/', (string)$nid) === 1; });
            if (!$hobby) { continue; }
            $hobby_slug = sanitize_title((string)($hobby['slug'] ?? ''));
            $hobby_title = sanitize_text_field((string)($hobby['display_name'] ?? ''));
            $slug = sanitize_title((string)($node['slug'] ?? ''));
            $name = sanitize_text_field((string)($node['display_name'] ?? ''));
            if ($hobby_slug === '' || $slug === '' || $name === '') { continue; }
            $world = self::ancestor($id, $nodes, static function($n, $nid){ return preg_match('/^core:world:[^:]+$/', (string)$nid) === 1; });
            $parent_id = (string)($hobby['parent_id'] ?? '');
            $parent = isset($nodes[$parent_id]) ? $nodes[$parent_id] : array();
            $article_targets[] = array(
                'category_slug'=>$slug,
                'category_name'=>$name,
                'product'=>$hobby_title,
                'product_slug'=>$hobby_slug,
                'hub'=>sanitize_text_field((string)($parent['display_name'] ?? '')),
                'hub_slug'=>sanitize_title((string)($parent['slug'] ?? '')),
                'main_hub'=>sanitize_text_field((string)($world['display_name'] ?? '')),
                'main_slug'=>sanitize_title((string)($world['slug'] ?? '')),
                'theme'=>$name,
                'path'=>implode(' > ', self::path_labels($id, $nodes)),
                'node_id'=>$id,
            );
        }

        $search_rules = array();
        foreach ($worlds as $id => $world) {
            $slug = sanitize_title((string)($world['slug'] ?? ''));
            $label = sanitize_text_field((string)($world['display_name'] ?? ''));
            if ($slug === '' || $label === '') { continue; }
            $search_rules[] = array(
                'id'=>$slug,
                'label'=>$label,
                'query'=>$label,
                'target_term_slug'=>$slug,
                'candidate_main_slugs'=>array($slug),
                'candidate_buckets'=>array($slug),
                'private'=>true,
                'business'=>true,
                'active'=>true,
            );
        }

        foreach ($world_profiles as $slug => &$profile) {
            $profile['phrases'] = array_values(array_unique(array_filter($profile['phrases'])));
            $profile['strong_phrases'] = array_values(array_unique(array_filter($profile['strong_phrases'])));
        }
        unset($profile);

        self::$catalog = array(
            'schema'=>'hdar-hobby-depot-catalog-v1',
            'source_revision'=>(string)($snapshot['revision'] ?? (function_exists('hd_category_registry_revision') ? hd_category_registry_revision() : '')),
            'counts'=>array(
                'worlds'=>count($worlds),
                'product_pages'=>count($product_targets),
                'article_categories'=>count($article_targets),
                'business_concepts'=>count($business_concepts),
            ),
            'search_rules'=>$search_rules,
            'product_targets'=>$product_targets,
            'article_targets'=>$article_targets,
            'private_bucket_profiles'=>$world_profiles,
            'business_concepts'=>$business_concepts,
            'business_hub_concepts'=>array(),
            'hard_negative_markers'=>array(),
            'strong_domain_markers'=>array(),
            'content_policy'=>array(
                'version'=>'hdar-1',
                'mode'=>'EXACT_OR_STRONG_TARGET_EVIDENCE_FAIL_CLOSED',
            ),
            'business_supply_contract'=>array(
                'version'=>'hdar-1',
                'required_product_concept_ids'=>array_values(array_map(static function($c){ return (string)$c['id']; }, $business_concepts)),
            ),
        );
        return self::$catalog;
    }
}
