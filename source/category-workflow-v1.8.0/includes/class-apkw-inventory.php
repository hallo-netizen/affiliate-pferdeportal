<?php
if (!defined('ABSPATH')) { exit; }

final class APKW_Inventory {
    public static function snapshot(): array {
        $objects = [];

        $pages = get_posts([
            'post_type' => 'page',
            'post_status' => ['publish', 'draft', 'pending', 'private'],
            'numberposts' => -1,
            'orderby' => 'ID',
            'order' => 'ASC',
            'suppress_filters' => true,
        ]);
        foreach ($pages as $page) {
            $objects[] = [
                'adapter' => 'wordpress_page',
                'taxonomy' => null,
                'object_id' => (int) $page->ID,
                'parent_object_id' => (int) ($page->post_parent ?? 0),
                'name' => (string) get_the_title($page),
                'slug' => (string) ($page->post_name ?? ''),
                'status' => (string) ($page->post_status ?? ''),
            ];
        }

        $taxonomies = get_taxonomies(['public' => true, 'hierarchical' => true], 'objects');
        foreach ($taxonomies as $taxonomy) {
            $taxonomy_name = (string) ($taxonomy->name ?? '');
            if ($taxonomy_name === '') { continue; }
            $terms = get_terms(['taxonomy' => $taxonomy_name, 'hide_empty' => false]);
            if (is_wp_error($terms) || !is_array($terms)) { continue; }
            foreach ($terms as $term) {
                $objects[] = [
                    'adapter' => 'wordpress_taxonomy',
                    'taxonomy' => $taxonomy_name,
                    'object_id' => (int) $term->term_id,
                    'parent_object_id' => (int) ($term->parent ?? 0),
                    'name' => (string) ($term->name ?? ''),
                    'slug' => (string) ($term->slug ?? ''),
                    'status' => 'active',
                ];
            }
        }

        return [
            'site_url' => rtrim((string) home_url('/'), '/'),
            'captured_at_utc' => gmdate('c'),
            'scope' => 'pages_plus_all_public_hierarchical_taxonomies',
            'object_count' => count($objects),
            'objects' => $objects,
        ];
    }

    public static function for_targets(array $nodes, array $package): array {
        $all = self::snapshot();
        $wanted = [];
        foreach ($nodes as $node) {
            $target = APKW_Validator::resolved_target($node, $package);
            if ($target === null) { continue; }
            $key = (string) $target['adapter'] . '|' . (string) ($target['taxonomy'] ?? '');
            $wanted[$key] = true;
        }

        $objects = array_values(array_filter($all['objects'], static function (array $object) use ($wanted): bool {
            $key = (string) $object['adapter'] . '|' . (string) ($object['taxonomy'] ?? '');
            return isset($wanted[$key]);
        }));
        $all['scope'] = 'targets_declared_in_structure_package';
        $all['object_count'] = count($objects);
        $all['objects'] = $objects;
        return $all;
    }
}
