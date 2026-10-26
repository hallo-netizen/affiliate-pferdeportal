<?php
/**
 * Portalneutraler Zielquellen-Adapter.
 *
 * Der neutrale Stamm enthält bewusst keine Portal-, Kategorie- oder Produkt-Masterdaten.
 * Ein Projektadapter bindet seinen Katalog ausschließlich über den Filter
 * ppar_portal_source_catalog ein. Ohne Bindung bleibt die Engine fail-closed.
 */
if (!defined('ABSPATH')) { exit; }

final class PPAR_Portal_Source {
    private static $catalog = null;

    public static function catalog() {
        if (is_array(self::$catalog)) { return self::$catalog; }

        $catalog = apply_filters('ppar_portal_source_catalog', null);
        if (is_wp_error($catalog)) { return $catalog; }
        if (!is_array($catalog) || !$catalog) {
            return new WP_Error('ppar_portal_source_unbound', 'Portal-Zielquelle ist im neutralen Stamm nicht gebunden.');
        }

        foreach (array('product_targets','article_targets','search_rules','business_concepts') as $required) {
            if (empty($catalog[$required]) || !is_array($catalog[$required])) {
                return new WP_Error('ppar_portal_catalog_incomplete', 'Gebundener Portal-Zielkatalog ist unvollständig.');
            }
        }

        $catalog['private_bucket_profiles'] = isset($catalog['private_bucket_profiles']) && is_array($catalog['private_bucket_profiles'])
            ? $catalog['private_bucket_profiles']
            : array();
        $catalog['business_hub_concepts'] = isset($catalog['business_hub_concepts']) && is_array($catalog['business_hub_concepts'])
            ? $catalog['business_hub_concepts']
            : array();
        $catalog['hard_negative_markers'] = isset($catalog['hard_negative_markers']) && is_array($catalog['hard_negative_markers'])
            ? $catalog['hard_negative_markers']
            : array();
        $catalog['strong_domain_markers'] = isset($catalog['strong_domain_markers']) && is_array($catalog['strong_domain_markers'])
            ? $catalog['strong_domain_markers']
            : array();

        self::$catalog = $catalog;
        return self::$catalog;
    }

    public static function reset_request_cache() {
        self::$catalog = null;
    }
}
