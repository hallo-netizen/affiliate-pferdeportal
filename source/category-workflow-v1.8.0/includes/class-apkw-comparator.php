<?php
if (!defined('ABSPATH')) { exit; }

final class APKW_Comparator {
    private const IGNORED_STATUSES = ['BLOCKED', 'DEPRECATED', 'REJECTED'];

    public static function compare(array $package, array $validation): array {
        $counts = ['UNCHANGED'=>0, 'CREATE_PREVIEW'=>0, 'UPDATE_PREVIEW'=>0, 'CONFLICT'=>0, 'BLOCKED'=>0, 'IGNORED_STATUS'=>0];
        $rows = [];
        if (!$validation['valid']) {
            return ['status'=>'BLOCKED_SCHEMA', 'summary'=>$counts, 'rows'=>[], 'live_inventory'=>['object_count'=>0,'objects'=>[]]];
        }

        $nodes = $validation['nodes'];
        $live = APKW_Inventory::for_targets($nodes, $package);
        $live_names = [];
        foreach ($live['objects'] as $object) {
            $key = APKW_Validator::visible_name_key((string) $object['name']);
            if ($key !== '') { $live_names[$key][] = $object; }
        }

        usort($nodes, static fn(array $a, array $b): int => ((int)$a['level'] <=> (int)$b['level']) ?: strcmp((string)$a['concept_id'], (string)$b['concept_id']));
        foreach ($nodes as $node) {
            if (in_array((string) $node['status'], self::IGNORED_STATUSES, true) || (isset($node['active']) && $node['active'] === false)) {
                $rows[] = self::row($node, 'IGNORE', 'IGNORED_STATUS', 'Knoten ist nicht zur Umsetzung freigegeben.');
                $counts['IGNORED_STATUS']++;
                continue;
            }

            $target = APKW_Validator::resolved_target($node, $package);
            if ($target === null || ($target['adapter'] ?? '') === '') {
                $rows[] = self::row($node, 'BLOCK', 'TARGET_MISSING', 'Kein Zieladapter definiert.');
                $counts['BLOCKED']++;
                continue;
            }
            if (($target['adapter'] ?? '') === 'wordpress_taxonomy' && !taxonomy_exists((string) ($target['taxonomy'] ?? ''))) {
                $rows[] = self::row($node, 'BLOCK', 'TAXONOMY_UNAVAILABLE', 'Zieltaxonomie ist nicht verfügbar.');
                $counts['BLOCKED']++;
                continue;
            }

            $matched = self::resolve_object($node, $target);
            $name_key = APKW_Validator::visible_name_key((string) $node['name']);
            $live_duplicates = $live_names[$name_key] ?? [];
            foreach ($live_duplicates as $existing) {
                if ($matched !== null && (int) $existing['object_id'] === (int) $matched['object_id'] && (string)$existing['adapter'] === (string)$matched['adapter'] && (string)($existing['taxonomy'] ?? '') === (string)($matched['taxonomy'] ?? '')) {
                    continue;
                }
                $rows[] = self::row($node, 'CONFLICT', 'LIVE_VISIBLE_NAME_DUPLICATE', 'Identische sichtbare Bezeichnung existiert bereits im Zielbereich: ' . $existing['name'] . ' (#' . $existing['object_id'] . ').');
                $counts['CONFLICT']++;
                continue 2;
            }

            if ($matched === null) {
                $rows[] = self::row($node, 'CREATE_PREVIEW', 'NOT_FOUND', 'Kein bestehendes Zielobjekt gefunden; nur Vorschau, keine Anlage.');
                $counts['CREATE_PREVIEW']++;
                continue;
            }

            $diff = [];
            if (APKW_Validator::visible_name_key((string) $matched['name']) !== APKW_Validator::visible_name_key((string) $node['name'])) { $diff[] = 'name'; }
            if ((string) $matched['slug'] !== (string) $node['slug']) { $diff[] = 'slug'; }
            if ($diff) {
                $rows[] = self::row($node, 'UPDATE_PREVIEW', 'DIFFERENT', 'Bestehendes Zielobjekt unterscheidet sich: ' . implode(', ', $diff) . '.', (int) $matched['object_id']);
                $counts['UPDATE_PREVIEW']++;
            } else {
                $rows[] = self::row($node, 'UNCHANGED', 'EXACT_MATCH', 'Bestehendes Zielobjekt stimmt bei Name und Slug überein.', (int) $matched['object_id']);
                $counts['UNCHANGED']++;
            }
        }

        $status = ($counts['BLOCKED'] > 0 || $counts['CONFLICT'] > 0) ? 'BLOCKED_PREVIEW' : 'PASS_READ_ONLY_PREVIEW';
        return ['status'=>$status, 'summary'=>$counts, 'rows'=>$rows, 'live_inventory'=>$live];
    }

    public static function unavailable_taxonomy_requirements(array $package, array $validation): array {
        if (!$validation['valid']) { return []; }
        $requirements = [];
        foreach ($validation['nodes'] as $node) {
            if (in_array((string) ($node['status'] ?? ''), self::IGNORED_STATUSES, true) || (isset($node['active']) && $node['active'] === false)) { continue; }
            $target = APKW_Validator::normalized_target($node, $package);
            if ($target === null || (string) ($target['adapter'] ?? '') !== 'wordpress_taxonomy') { continue; }
            $taxonomy = (string) ($target['taxonomy'] ?? '');
            if ($taxonomy === '' || taxonomy_exists($taxonomy)) { continue; }
            $block = (string) ($node['block'] ?? '');
            $key = $block . '|wordpress_taxonomy|' . $taxonomy;
            if (!isset($requirements[$key])) {
                $requirements[$key] = [
                    'block' => $block,
                    'original_adapter' => 'wordpress_taxonomy',
                    'original_taxonomy' => $taxonomy,
                    'affected_node_count' => 0,
                    'affected_examples' => [],
                ];
            }
            $requirements[$key]['affected_node_count']++;
            if (count($requirements[$key]['affected_examples']) < 5) { $requirements[$key]['affected_examples'][] = (string) ($node['name'] ?? ''); }
        }
        ksort($requirements, SORT_STRING);
        return array_values($requirements);
    }

    public static function blocked_only_by_unavailable_taxonomies(array $comparison): bool {
        if (($comparison['status'] ?? '') !== 'BLOCKED_PREVIEW') { return false; }
        $has = false;
        foreach ($comparison['rows'] ?? [] as $row) {
            $action = (string) ($row['action'] ?? '');
            if ($action === 'BLOCK') {
                $has = true;
                if ((string) ($row['code'] ?? '') !== 'TAXONOMY_UNAVAILABLE') { return false; }
            }
            if ($action === 'CONFLICT') { return false; }
        }
        return $has;
    }

    private static function resolve_object(array $node, array $target): ?array {
        $object_id = (int) ($target['object_id'] ?? 0);
        if ($target['adapter'] === 'wordpress_page') {
            if ($object_id > 0) {
                $page = get_post($object_id);
                if ($page && (string) ($page->post_type ?? '') === 'page') {
                    return ['adapter'=>'wordpress_page','taxonomy'=>null,'object_id'=>(int)$page->ID,'name'=>(string)get_the_title($page),'slug'=>(string)$page->post_name];
                }
            }
            $pages = get_posts(['post_type'=>'page','name'=>(string)$node['slug'],'post_status'=>['publish','draft','pending','private'],'numberposts'=>2,'suppress_filters'=>true]);
            if (count($pages) === 1) {
                $page = $pages[0];
                return ['adapter'=>'wordpress_page','taxonomy'=>null,'object_id'=>(int)$page->ID,'name'=>(string)get_the_title($page),'slug'=>(string)$page->post_name];
            }
            return null;
        }

        $taxonomy = (string) ($target['taxonomy'] ?? '');
        if ($object_id > 0) {
            $term = get_term($object_id, $taxonomy);
            if ($term && !is_wp_error($term)) {
                return ['adapter'=>'wordpress_taxonomy','taxonomy'=>$taxonomy,'object_id'=>(int)$term->term_id,'name'=>(string)$term->name,'slug'=>(string)$term->slug];
            }
        }
        $term = get_term_by('slug', (string)$node['slug'], $taxonomy);
        if ($term && !is_wp_error($term)) {
            return ['adapter'=>'wordpress_taxonomy','taxonomy'=>$taxonomy,'object_id'=>(int)$term->term_id,'name'=>(string)$term->name,'slug'=>(string)$term->slug];
        }
        return null;
    }

    private static function row(array $node, string $action, string $code, string $message, ?int $matched = null): array {
        $row = ['concept_id'=>(string)$node['concept_id'],'block'=>(string)$node['block'],'level'=>(int)$node['level'],'name'=>(string)$node['name'],'slug'=>(string)$node['slug'],'action'=>$action,'code'=>$code,'message'=>$message];
        if ($matched !== null) { $row['matched_object_id'] = $matched; }
        return $row;
    }
}
