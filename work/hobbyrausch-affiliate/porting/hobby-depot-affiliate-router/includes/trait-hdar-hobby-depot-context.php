<?php
if (!defined('ABSPATH')) { exit; }

/**
 * Hobby Depot runtime context bridge.
 *
 * Single source for categories: HD-004 read-only registry.
 * No copied category master and no source-portal fallback.
 */
trait HDAR_Hobby_Depot_Context_Trait {
    private function hd_affiliate_registry_ready() {
        return function_exists('hd_category_registry_ready') && (bool) hd_category_registry_ready();
    }

    private function hd_affiliate_registry_node_for_object($object_id, $object_type = '') {
        $object_id = absint($object_id);
        if ($object_id <= 0 || !$this->hd_affiliate_registry_ready()
            || !function_exists('hd_category_registry_find_node_by_object')) {
            return null;
        }
        $node = hd_category_registry_find_node_by_object($object_id, (string) $object_type);
        return is_array($node) ? $node : null;
    }

    private function hd_affiliate_registry_parent($node) {
        if (!is_array($node) || !function_exists('hd_category_registry_node')) { return null; }
        $parent_id = trim((string)($node['parent_id'] ?? ''));
        if ($parent_id === '') { return null; }
        $parent = hd_category_registry_node($parent_id);
        return is_array($parent) ? $parent : null;
    }

    private function hd_affiliate_context_chain($object_id, $object_type = '') {
        $node = $this->hd_affiliate_registry_node_for_object($object_id, $object_type);
        if (!$node) { return array(); }
        $chain = array($node);
        $seen = array();
        for ($i = 0; $i < 8; $i++) {
            $id = trim((string)($node['node_id'] ?? ''));
            if ($id !== '') {
                if (isset($seen[$id])) { break; }
                $seen[$id] = true;
            }
            $node = $this->hd_affiliate_registry_parent($node);
            if (!$node) { break; }
            $chain[] = $node;
        }
        return $chain;
    }

    private function hd_affiliate_context_terms($object_id, $object_type = '') {
        $terms = array();
        foreach ($this->hd_affiliate_context_chain($object_id, $object_type) as $node) {
            foreach (array('name','slug') as $key) {
                $value = trim((string)($node[$key] ?? ''));
                if ($value !== '') { $terms[] = $value; }
            }
        }
        return array_values(array_unique($terms));
    }

    private function hd_affiliate_product_query_for_object($object_id, $object_type = '') {
        $chain = $this->hd_affiliate_context_chain($object_id, $object_type);
        $names = array();
        foreach ($chain as $node) {
            $name = trim((string)($node['name'] ?? ''));
            if ($name !== '') { $names[] = $name; }
        }
        $query = trim(implode(' ', array_slice(array_values(array_unique($names)), 0, 3)));
        if (function_exists('apply_filters')) {
            $query = (string) apply_filters('hobby_depot_affiliate_product_query', $query, absint($object_id), $chain);
        }
        return sanitize_text_field($query);
    }

    private function hd_affiliate_target_key_for_object($object_id, $object_type = '') {
        $node = $this->hd_affiliate_registry_node_for_object($object_id, $object_type);
        $key = is_array($node) ? trim((string)($node['node_id'] ?? '')) : '';
        if (function_exists('apply_filters')) {
            $key = (string) apply_filters('hobby_depot_affiliate_target_key', $key, absint($object_id), $node);
        }
        return sanitize_text_field($key);
    }

    private function hd_affiliate_page_type($object_id) {
        $object_id = absint($object_id);
        $type = '';
        if (function_exists('apply_filters')) {
            $type = sanitize_key((string) apply_filters('hobby_depot_affiliate_page_type', '', $object_id));
        }
        if ($type !== '') { return $type; }

        $node = $this->hd_affiliate_registry_node_for_object($object_id);
        if (!is_array($node)) { return ''; }
        $node_id = (string)($node['node_id'] ?? '');
        if (strpos($node_id, ':content:') !== false) { return 'leaf'; }
        if (strpos($node_id, 'core:entity:') === 0) { return 'hobby'; }
        return '';
    }
}
