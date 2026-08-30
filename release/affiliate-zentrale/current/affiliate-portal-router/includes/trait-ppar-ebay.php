<?php
if (!defined('ABSPATH')) {
    exit;
}

/**
 * V5.6.0 – eBay Browse API / EPN: resumierbarer Hintergrundabruf, Pagination, Prüfbestand, Listing-Lifecycle und Backend-Filter.
 *
 * Harte Routingregeln:
 * - INDIVIDUAL wird ausschließlich als hp_listing unter der konfigurierten
 *   HivePress-Wurzel "Private Anzeigen" materialisiert.
 * - BUSINESS wird ausschließlich als reales Produkt-Creative in die bestehende
 *   Werbemittelbibliothek übernommen und danach über das zentrale Output-Modell
 *   gegen echte Portalziele und Designslots geplant.
 * - CLASSIFIED_AD, fehlende Affiliate-URLs, abgelaufene Angebote, abweichende
 *   Verkäuferkontotypen und andere Marktplätze werden fail-closed blockiert.
 */
trait PPAR_Ebay_Trait {

    /**
     * Request-local source cache. Public listing queries already resolve eBay
     * source rows in one bounded SQL query; the remote image renderer reuses
     * that evidence instead of issuing one SQL query per card.
     */
    private $ebay_public_source_row_cache = array();

    /** V4.2.0 – vollständiger, fest mitgelieferter Pferde-Atelier-Zielkatalog. */
    private function ebay_portal_catalog() {
        static $catalog = null;
        if (is_array($catalog)) { return $catalog; }
        $asset_dir = dirname(__DIR__) . '/assets/';
        $path = $asset_dir . 'ebay-portal-catalog-v2.json';
        $source_path = $asset_dir . 'portal-structure-v279.json';
        if (!is_readable($path) || !is_readable($source_path)) {
            return new WP_Error('ebay_portal_catalog_missing', 'Pferde-Atelier-eBay-Zielkatalog oder Portalquelle fehlt.');
        }
        $decoded = json_decode((string) file_get_contents($path), true);
        if (!is_array($decoded) || (string) ($decoded['schema'] ?? '') !== '2.0') {
            return new WP_Error('ebay_portal_catalog_invalid', 'Pferde-Atelier-eBay-Zielkatalog ist ungültig.');
        }
        $expected_source_hash = strtolower(sanitize_text_field((string) ($decoded['source_sha256'] ?? '')));
        $actual_source_hash = hash_file('sha256', $source_path);
        if (!preg_match('/^[a-f0-9]{64}$/', $expected_source_hash) || !is_string($actual_source_hash) || !hash_equals($expected_source_hash, strtolower($actual_source_hash))) {
            return new WP_Error('ebay_portal_catalog_source_mismatch', 'Pferde-Atelier-eBay-Zielkatalog stimmt nicht mit der mitgelieferten Portalstruktur überein.');
        }
        $counts = is_array($decoded['counts'] ?? null) ? $decoded['counts'] : array();
        $required_counts = array('main_hubs'=>8, 'hub_pages'=>59, 'product_pages'=>329, 'article_categories'=>1124);
        foreach ($required_counts as $key=>$expected) {
            if (absint($counts[$key] ?? 0) !== $expected) {
                return new WP_Error('ebay_portal_catalog_incomplete', 'Pferde-Atelier-eBay-Zielkatalog ist unvollständig: ' . sanitize_key($key));
            }
        }
        $products = array_values((array) ($decoded['product_targets'] ?? array()));
        $articles = array_values((array) ($decoded['article_targets'] ?? array()));
        $rules = array_values((array) ($decoded['search_rules'] ?? array()));
        if (count($products) !== 329 || count($articles) !== 1124 || count($rules) !== 8) {
            return new WP_Error('ebay_portal_catalog_count_mismatch', 'Pferde-Atelier-eBay-Zielkatalog stimmt nicht mit den Sollzahlen überein.');
        }
        $allowed_buckets = array('pferde-ponys','sattel-zaumzeug','decken-schutz','stall-weide-haltung','fuetterung-pflege','anhaenger-transport','reitbekleidung-zubehoer','sonstiges');
        $product_slugs = array();
        foreach ($products as $target) {
            if (!is_array($target)) { return new WP_Error('ebay_portal_product_invalid', 'Ungültiges Produktziel im Pferde-Atelier-Katalog.'); }
            $slug = sanitize_title((string) ($target['slug'] ?? ''));
            $bucket = sanitize_title((string) ($target['private_bucket_slug'] ?? ''));
            if ($slug === '' || empty($target['title']) || empty($target['hub']) || empty($target['main_hub']) || !in_array($bucket, $allowed_buckets, true) || isset($product_slugs[$slug])) {
                return new WP_Error('ebay_portal_product_invalid', 'Unvollständiges, doppeltes oder ungültig geroutetes Produktziel: ' . $slug);
            }
            $product_slugs[$slug] = true;
        }
        $article_slugs = array();
        foreach ($articles as $target) {
            if (!is_array($target)) { return new WP_Error('ebay_portal_article_invalid', 'Ungültiges WordPress-Kategorieziel im Pferde-Atelier-Katalog.'); }
            $slug = sanitize_title((string) ($target['category_slug'] ?? ''));
            $product_slug = sanitize_title((string) ($target['product_slug'] ?? ''));
            if ($slug === '' || empty($target['category_name']) || !isset($product_slugs[$product_slug]) || isset($article_slugs[$slug])) {
                return new WP_Error('ebay_portal_article_invalid', 'Unvollständige, doppelte oder verwaiste WordPress-Kategorie: ' . $slug);
            }
            $article_slugs[$slug] = true;
        }
        $rule_ids = array();
        foreach ($rules as $rule) {
            $id = sanitize_key((string) ($rule['id'] ?? ''));
            $bucket = sanitize_title((string) ($rule['target_term_slug'] ?? ''));
            if ($id === '' || empty($rule['query']) || !in_array($bucket, $allowed_buckets, true) || isset($rule_ids[$id])) {
                return new WP_Error('ebay_portal_rule_invalid', 'Ungültiges automatisches eBay-Abrufprofil: ' . $id);
            }
            $rule_ids[$id] = true;
        }
        if (count(array_values(array_filter((array) ($decoded['strong_horse_markers'] ?? array())))) < 10 || empty($decoded['hard_negative_markers'])) {
            return new WP_Error('ebay_portal_markers_incomplete', 'Fach- oder Ausschlussmarker des eBay-Zielkatalogs fehlen.');
        }
        if (count((array) ($decoded['private_bucket_profiles'] ?? array())) !== 8 || count((array) ($decoded['business_concepts'] ?? array())) < 300 || empty($decoded['content_policy']['version'])) {
            return new WP_Error('ebay_portal_workflow_contract_incomplete', 'eBay-Workflow-V2-Vertrag im Zielkatalog ist unvollständig.');
        }
        $catalog = $decoded;
        return $catalog;
    }

    private function ebay_catalog_rules() {
        $catalog = $this->ebay_portal_catalog();
        if (is_wp_error($catalog)) { return array(); }
        return $this->ebay_normalize_rules((array) ($catalog['search_rules'] ?? array()));
    }

    private function ebay_catalog_integrity() {
        $catalog = $this->ebay_portal_catalog();
        if (is_wp_error($catalog)) { return $catalog; }
        return array(
            'main_hubs'=>absint($catalog['counts']['main_hubs'] ?? 0),
            'hub_pages'=>absint($catalog['counts']['hub_pages'] ?? 0),
            'product_pages'=>absint($catalog['counts']['product_pages'] ?? 0),
            'article_categories'=>absint($catalog['counts']['article_categories'] ?? 0),
            'source_sha256'=>sanitize_text_field((string) ($catalog['source_sha256'] ?? '')),
        );
    }

    private function ebay_topic_text($value) {
        $value = wp_strip_all_tags((string) $value);
        if (function_exists('remove_accents')) { $value = remove_accents($value); }
        $value = strtolower($value);
        $value = str_replace('&', ' und ', $value);
        $value = preg_replace('/[^a-z0-9]+/', ' ', $value);
        return trim(preg_replace('/\s+/', ' ', (string) $value));
    }

    private function ebay_topic_tokens($value) {
        $stop = array_flip(array('und','oder','der','die','das','den','dem','des','ein','eine','einer','eines','fuer','mit','von','im','in','am','an','zu','zur','zum','bei','auf','aus','neu','gebraucht','set','paar','stueck','original'));
        $tokens = array();
        foreach (preg_split('/\s+/', $this->ebay_topic_text($value)) as $token) {
            if ($token === '' || strlen($token) < 3 || isset($stop[$token])) { continue; }
            $tokens[$token] = $token;
        }
        return array_values($tokens);
    }

    private function ebay_topic_stem($token) {
        $token = $this->ebay_topic_text($token);
        if (strlen($token) < 6) { return $token; }
        foreach (array('ern','em','en','er','es','e','n','s') as $suffix) {
            // A final s is lexical in common German horse-product nouns such as
            // "Gebiss". Stripping one of the double-s characters would make
            // singular "Gebiss" and plural "Gebisse" look unrelated.
            if ($suffix === 's' && substr($token, -2) === 'ss') { continue; }
            if (substr($token, -strlen($suffix)) === $suffix && strlen($token) - strlen($suffix) >= 5) {
                return substr($token, 0, -strlen($suffix));
            }
        }
        return $token;
    }

    private function ebay_topic_term_present($text, $term) {
        $text = $this->ebay_topic_text($text);
        $term = $this->ebay_topic_text($term);
        if ($text === '' || $term === '') { return false; }
        if (strpos(' ' . $text . ' ', ' ' . $term . ' ') !== false) { return true; }
        $text_tokens = $this->ebay_topic_tokens($text);
        foreach ($this->ebay_topic_tokens($term) as $term_token) {
            foreach ($text_tokens as $text_token) {
                if ($term_token === $text_token) { return true; }
                if (strlen($term_token) >= 5 && strlen($text_token) >= 5 && (strpos($term_token, $text_token) !== false || strpos($text_token, $term_token) !== false)) { return true; }
            }
        }
        return false;
    }

    /** Ausschlussmarker dürfen nur vom Angebotstoken getragen werden, nie umgekehrt. */
    private function ebay_topic_negative_present($text, $marker) {
        $text = $this->ebay_topic_text($text);
        $marker = $this->ebay_topic_text($marker);
        if ($text === '' || $marker === '') { return false; }
        if (strpos(' ' . $text . ' ', ' ' . $marker . ' ') !== false) { return true; }
        $marker_tokens = $this->ebay_topic_tokens($marker);
        if (count($marker_tokens) !== 1) { return false; }
        $needle = (string) $marker_tokens[0];
        if (strlen($needle) < 4) { return false; }
        foreach ($this->ebay_topic_tokens($text) as $token) {
            if ($token === $needle || strpos($token, $needle) !== false) { return true; }
        }
        return false;
    }

    private function ebay_item_topic_evidence($item) {
        $raw = is_array($item['raw'] ?? null) ? $item['raw'] : array();
        $category_names = array();
        foreach ((array) ($raw['categories'] ?? array()) as $category) {
            if (is_array($category) && !empty($category['categoryName'])) { $category_names[] = sanitize_text_field((string) $category['categoryName']); }
        }
        $aspects = array();
        foreach ((array) ($raw['localizedAspects'] ?? array()) as $aspect) {
            if (!is_array($aspect)) { continue; }
            $aspects[] = sanitize_text_field((string) ($aspect['name'] ?? ''));
            $aspects[] = sanitize_text_field((string) ($aspect['value'] ?? ''));
        }
        return trim(implode(' ', array_filter(array(
            (string) ($item['title'] ?? ''),
            (string) ($item['short_description'] ?? ''),
            implode(' ', $category_names),
            implode(' ', $aspects),
        ))));
    }

    /** Content-policy brands are exact tokens/phrases, never fuzzy substrings. */
    private function ebay_content_policy_exact_term_present($text, $term) {
        $text = $this->ebay_topic_text((string) $text);
        $term = $this->ebay_topic_text((string) $term);
        if ($text === '' || $term === '') { return false; }
        if (strpos(' ' . $text . ' ', ' ' . $term . ' ') !== false) { return true; }
        $term_tokens = $this->ebay_topic_tokens($term);
        if (count($term_tokens) !== 1) { return false; }
        $needle = (string) $term_tokens[0];
        foreach ($this->ebay_topic_tokens($text) as $token) {
            if ($token === $needle) { return true; }
        }
        return false;
    }

    /**
     * Catalog-driven hard media signature. German compound book categories such
     * as "Kinder- & Jugendbücher" normalize to tokens like "jugendbucher".
     * Exact phrase matching alone cannot see those compounds, so the catalog may
     * declare token suffixes. This is still deterministic token logic, not fuzzy
     * matching: "buch" matches "handbuch", but never "buchse".
     */

    /**
     * Central product-form safety. A horse/reitsport reference must never turn a
     * souvenir/decorative object into an admissible portal product. The blocked
     * forms live in the catalog and therefore apply identically to PRIVATE,
     * BUSINESS, maintenance and both public delivery gates.
     */
    private function ebay_content_policy_blocked_product_head($title, $policy) {
        $policy = is_array($policy) ? $policy : array();
        $blocked = array_values(array_unique(array_filter(array_map(array($this, 'ebay_topic_text'), (array)($policy['blocked_primary_product_terms'] ?? array())))));
        if (!$blocked) { return ''; }
        $title = $this->ebay_topic_text((string)$title);
        if ($title === '') { return ''; }
        $primary = $this->ebay_business_primary_title_section($title);
        if ($primary === '') { $primary = $title; }
        $raw_tokens = preg_split('/\s+/', $title);
        $first = $this->ebay_topic_text((string)($raw_tokens[0] ?? ''));
        foreach ($blocked as $marker) {
            if ($marker === '') { continue; }
            if (($first !== '' && $this->ebay_business_strict_token_present($first, $marker))
                || $this->ebay_business_strict_token_present($primary, $marker)) {
                return $marker;
            }
        }
        return '';
    }

    private function ebay_content_policy_media_token_present($text, $policy) {
        $tokens = $this->ebay_topic_tokens((string) $text);
        if (!$tokens) { return ''; }
        $policy = is_array($policy) ? $policy : array();
        $exact = array_values(array_unique(array_filter(array_map(array($this, 'ebay_topic_text'), (array) ($policy['blocked_exact_media_terms'] ?? array())))));
        $suffixes = array_values(array_unique(array_filter(array_map(array($this, 'ebay_topic_text'), (array) ($policy['blocked_token_suffixes'] ?? array())))));
        foreach ($tokens as $token) {
            $token = (string) $token;
            if ($token === '') { continue; }
            if (in_array($token, $exact, true)) { return $token; }
            foreach ($suffixes as $suffix) {
                $suffix = (string) $suffix;
                if ($suffix === '' || strlen($token) < strlen($suffix)) { continue; }
                if (substr($token, -strlen($suffix)) === $suffix) { return $token; }
            }
        }
        return '';
    }

    /**
     * V5.26 – providernahe Hard-Safety gegen Spielzeug/Modellware.
     * Diese Sperre liegt absichtlich VOR der fachlichen Zielklassifikation und
     * gilt identisch fuer INDIVIDUAL und BUSINESS. Damit kann ein Titel wie
     * "Playmobil Pferd mit Sattel" nicht allein wegen Pferd/Sattel durchrutschen.
     * Generische Woerter wie "Figur" werden nicht alleine gesperrt; ausschlaggebend
     * sind eindeutige Marken, Produktphrasen oder reale eBay-Spielzeugkategorien.
     */
    /**
     * Workflow V2 content policy. Policy data lives in the catalog, not in
     * version-specific PHP patches. Category/aspect evidence wins over title
     * heuristics; known toy/model signatures remain a secondary hard block.
     */
    private function ebay_content_policy_reason($item) {
        $catalog = $this->ebay_portal_catalog();
        if (is_wp_error($catalog)) { return 'Content-Policy-Katalog fehlt.'; }
        $policy = is_array($catalog['content_policy'] ?? null) ? $catalog['content_policy'] : array();
        $item = is_array($item) ? $item : array();
        $raw = is_array($item['raw'] ?? null) ? $item['raw'] : $item;
        $title = $this->ebay_topic_text((string) ($raw['title'] ?? ($item['title'] ?? '')));
        $description = $this->ebay_topic_text((string) ($raw['shortDescription'] ?? ($item['short_description'] ?? '')));
        $category_parts = array();
        foreach ((array) ($raw['categories'] ?? array()) as $category) {
            if (is_array($category)) { $category_parts[] = (string) ($category['categoryName'] ?? ''); }
        }
        foreach ((array) ($item['category_names'] ?? array()) as $category_name) { $category_parts[] = (string) $category_name; }
        $aspect_parts = array();
        foreach ((array) ($raw['localizedAspects'] ?? array()) as $aspect) {
            if (!is_array($aspect)) { continue; }
            $aspect_parts[] = (string) ($aspect['name'] ?? '');
            $aspect_parts[] = (string) ($aspect['value'] ?? '');
        }
        $category_text = $this->ebay_topic_text(implode(' ', $category_parts));
        $aspect_text = $this->ebay_topic_text(implode(' ', $aspect_parts));
        $all = trim(implode(' ', array_filter(array($title, $description, $category_text, $aspect_text))));
        if ($all === '') { return ''; }

        // V6.35: public/import safety must not depend on a trustworthy eBay
        // category. Real PRIVATE offers can be mis-categorised under Reitsport
        // while the title itself explicitly says "Spielzeug". Treat explicit
        // toy terms in title/description as a hard content block. Exact-term
        // matching avoids accidental substrings while still catching compounds
        // declared explicitly in the catalog.
        $offer_text = trim($title . ' ' . $description);
        foreach ((array) ($policy['blocked_exact_title_terms'] ?? array()) as $marker) {
            if ($this->ebay_content_policy_exact_term_present($offer_text, $marker)) {
                return 'Fachfremde Spielzeugware im Angebotstitel erkannt: ' . sanitize_text_field((string) $marker);
            }
        }
        foreach ((array) ($policy['blocked_media_title_phrases'] ?? array()) as $marker) {
            $needle = $this->ebay_topic_text((string) $marker);
            if ($needle !== '' && strpos(' ' . $offer_text . ' ', ' ' . $needle . ' ') !== false) {
                return 'Fachfremdes Buch-/Medienprodukt im Angebotstitel erkannt: ' . sanitize_text_field((string) $marker);
            }
        }
        $blocked_product_head = $this->ebay_content_policy_blocked_product_head($title, $policy);
        if ($blocked_product_head !== '') {
            return 'Angebot beschreibt primaer eine nicht freigegebene Produktform: ' . sanitize_text_field($blocked_product_head);
        }

        // V6.12: hard media gate before ordinary phrase checks. This closes the
        // live hole where eBay categories such as "Kinder- & Jugendbücher" were
        // split by "&" and therefore escaped exact phrase matching.
        $category_media_token = $this->ebay_content_policy_media_token_present(trim($category_text . ' ' . $aspect_text), $policy);
        if ($category_media_token !== '') {
            return 'eBay-Kategorie/Merkmal ist fachfremdes Buch-/Medienprodukt: ' . sanitize_text_field($category_media_token);
        }
        $offer_media_token = $this->ebay_content_policy_media_token_present(trim($title . ' ' . $description), $policy);
        if ($offer_media_token !== '') {
            return 'Fachfremdes Buch-/Medienprodukt erkannt: ' . sanitize_text_field($offer_media_token);
        }

        foreach ((array) ($policy['blocked_category_phrases'] ?? array()) as $marker) {
            $needle = $this->ebay_topic_text($marker);
            if ($needle !== '' && (
                strpos(' ' . $category_text . ' ', ' ' . $needle . ' ') !== false
                || strpos(' ' . $aspect_text . ' ', ' ' . $needle . ' ') !== false
            )) { return 'eBay-Kategorie/Merkmal ist fachfremde Spielzeug-/Modellware: ' . sanitize_text_field((string) $marker); }
        }
        foreach ((array) ($policy['blocked_brand_phrases'] ?? array()) as $marker) {
            if ($this->ebay_content_policy_exact_term_present($all, $marker)) { return 'Spielzeug-/Modellmarke erkannt: ' . sanitize_text_field((string) $marker); }
        }
        foreach ((array) ($policy['blocked_title_phrases'] ?? array()) as $marker) {
            $needle = $this->ebay_topic_text($marker);
            if ($needle !== '' && strpos(' ' . $all . ' ', ' ' . $needle . ' ') !== false) { return 'Spielzeug-/Modellprodukt erkannt: ' . sanitize_text_field((string) $marker); }
        }
        return '';
    }

    /** Compatibility wrapper for historical callers/tests. */
    private function ebay_toy_filter_reason($item) {
        return $this->ebay_content_policy_reason($item);
    }

    /**
     * Public-output safety net: re-evaluate the central policy from the stored
     * original eBay payload. This is deliberately read-only and independent of
     * maintenance/classifier cursors, so a legacy/current-contract row can never
     * stay public merely because an older pass stamped an allowed state.
     */
    private function ebay_public_content_policy_reason_from_source_row($row, $fallback_title = '') {
        $row = is_array($row) ? $row : array();
        $payload = json_decode((string)($row['source_payload'] ?? ''), true);
        $payload = is_array($payload) ? $payload : array();
        $raw = is_array($payload['raw'] ?? null) ? $payload['raw'] : array();
        if ($raw) {
            return $this->ebay_content_policy_reason(array(
                'raw'=>$raw,
                'title'=>(string)($row['title'] ?? $fallback_title),
                'short_description'=>(string)($row['short_description'] ?? ''),
            ));
        }
        return $this->ebay_content_policy_reason(array('title'=>(string)($row['title'] ?? $fallback_title)));
    }

    /** One bounded query for the PRIVATE public loop; no per-card source SQL. */
    private function ebay_public_source_rows_by_item_ids($item_ids, $seller_type = '') {
        $item_ids = array_values(array_unique(array_filter(array_map('sanitize_text_field', (array)$item_ids))));
        if (!$item_ids) { return array(); }
        global $wpdb;
        if (!is_object($wpdb) || !method_exists($wpdb, 'prepare') || !method_exists($wpdb, 'get_results')) { return array(); }
        $table = $this->ebay_items_table();
        if ($table === '') { return array(); }
        $placeholders = implode(',', array_fill(0, count($item_ids), '%s'));
        $args = $item_ids;
        $seller_type = strtoupper(sanitize_key((string)$seller_type));
        $where_seller = '';
        if (in_array($seller_type, array('INDIVIDUAL','BUSINESS'), true)) {
            $where_seller = ' AND seller_account_type=%s';
            $args[] = $seller_type;
        }
        $sql = $wpdb->prepare(
            "SELECT * FROM {$table} WHERE item_id IN ({$placeholders}){$where_seller} ORDER BY id DESC",
            $args
        );
        $rows = (array)$wpdb->get_results($sql, ARRAY_A);
        $out = array();
        foreach ($rows as $row) {
            if (!is_array($row)) { continue; }
            $item_id = sanitize_text_field((string)($row['item_id'] ?? ''));
            if ($item_id !== '' && !isset($out[$item_id])) {
                $out[$item_id] = $row;
                $this->ebay_public_source_row_cache[$item_id] = $row;
            }
        }
        return $out;
    }

    private function ebay_quarantine_filtered_row($row, $reason) {
        $row = is_array($row) ? $row : array();
        $id = absint($row['id'] ?? 0);
        if ($id <= 0) { return false; }
        $reason = sanitize_text_field((string) $reason);
        if ($reason === '') { $reason = 'Spielzeug-/Modellware ist im Pferde-Atelier nicht freigegeben.'; }
        global $wpdb;
        $quarantine_update = array(
            'status'=>'blocked_content','source_state'=>'available','policy_state'=>'blocked','route_state'=>'blocked','output_state'=>'blocked',
            'policy_version'=>self::EBAY_CONTENT_POLICY_VERSION,'rejection_reason'=>'[ebay_content_policy_blocked] ' . $reason,
            'fresh_until'=>0,'updated_at'=>time(),
        );
        $wpdb->update($this->ebay_items_table(), $quarantine_update, array('id'=>$id), $this->ebay_db_formats($quarantine_update), array('%d'));

        $seller_type = strtoupper(sanitize_key((string) ($row['seller_account_type'] ?? '')));
        if ($seller_type === 'INDIVIDUAL') {
            $listing_id = absint($row['listing_post_id'] ?? 0);
            if ($listing_id > 0) {
                if (function_exists('get_post_status') && get_post_status($listing_id) === 'publish' && function_exists('wp_update_post')) {
                    wp_update_post(array('ID'=>$listing_id,'post_status'=>'draft'));
                }
                if (function_exists('update_post_meta')) {
                    update_post_meta($listing_id, '_ppar_ebay_lifecycle_state', 'blocked_content');
                    update_post_meta($listing_id, '_ppar_ebay_block_reason', $reason);
                }
            }
        } elseif ($seller_type === 'BUSINESS') {
            $hash = strtolower(sanitize_text_field((string) ($row['creative_identity_hash'] ?? '')));
            $creative_table = method_exists($this, 'creative_library_table') ? $this->creative_library_table() : '';
            if (!preg_match('/^[a-f0-9]{64}$/', $hash) && $creative_table !== '') {
                $fallback = $wpdb->get_row($wpdb->prepare(
                    "SELECT identity_hash FROM {$creative_table} WHERE provider='ebay' AND source_kind='ebay_business_item' AND external_id=%s ORDER BY id DESC LIMIT 1",
                    (string) ($row['item_id'] ?? '')
                ), ARRAY_A);
                $fallback_hash = strtolower(sanitize_text_field((string) ($fallback['identity_hash'] ?? '')));
                if (preg_match('/^[a-f0-9]{64}$/', $fallback_hash)) { $hash = $fallback_hash; }
            }
            if (preg_match('/^[a-f0-9]{64}$/', $hash) && $creative_table !== '') {
                $creative = $wpdb->get_row($wpdb->prepare("SELECT * FROM {$creative_table} WHERE identity_hash=%s", $hash), ARRAY_A);
                if (is_array($creative)) {
                    $payload = json_decode((string) ($creative['payload'] ?? ''), true);
                    $payload = is_array($payload) ? $payload : array();
                    $payload['_content_filter_state'] = 'blocked_toy_model';
                    $payload['_content_filter_reason'] = $reason;
                    $payload['_content_filter_at'] = time();
                    $wpdb->update($creative_table, array(
                        'source_status'=>'blocked',
                        'availability_state'=>'blocked_content',
                        'review_status'=>'rejected',
                        'selected'=>0,
                        'content_scope'=>'other',
                        'scope_source'=>'ebay_content_filter',
                        'topic_status'=>'blocked',
                        'topic_score'=>0,
                        'payload'=>wp_json_encode($payload, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES),
                    ), array('id'=>absint($creative['id'] ?? 0)));
                }
                if (method_exists($this, 'output_objects_table')) {
                    $output_table = $this->output_objects_table();
                    $objects = $wpdb->get_results($wpdb->prepare("SELECT * FROM {$output_table} WHERE creative_identity_hash=%s", $hash), ARRAY_A);
                    foreach ((array) $objects as $object) {
                        if (method_exists($this, 'output_deactivate_materialized_object')) {
                            $this->output_deactivate_materialized_object($object, $reason);
                        }
                    }
                    $wpdb->update($output_table, array(
                        'status'=>'blocked_source',
                        'decision_source'=>'ebay_content_filter',
                        'decision_reason'=>$reason,
                        'updated_at'=>time(),
                    ), array('creative_identity_hash'=>$hash));
                }
            }
        }
        return true;
    }

    /**
     * Bestehende Altimporte werden lokal und ohne eBay-Request nachgeprueft.
     * Der Cursor macht die Migration wiederaufnehmbar; kein Listing/Creative wird
     * geloescht. Nur eindeutig erkannte Spielzeug-/Modellware wird deaktiviert.
     */
    public function maybe_run_ebay_content_filter_upgrade() {
        // Workflow V2 compatibility only. Historical admin-page rescans were a
        // root cause of hidden mutations. The authoritative maintenance state is
        // now produced exclusively by run_ebay_maintenance_v2().
        $state = method_exists($this,'ebay_maintenance_state_load') ? $this->ebay_maintenance_state_load() : get_option(self::OPTION_EBAY_MAINTENANCE_STATE, array());
        return is_array($state) ? $state : array();
    }

    /** Normalisierte Evidenzfelder fuer PRIVATE/BUSINESS-Klassifikation. */
    private function ebay_workflow_evidence_sections($item) {
        $item = is_array($item) ? $item : array();
        $raw = is_array($item['raw'] ?? null) ? $item['raw'] : array();
        $categories = array();
        foreach ((array) ($raw['categories'] ?? array()) as $category) {
            if (is_array($category) && !empty($category['categoryName'])) { $categories[] = (string) $category['categoryName']; }
        }
        foreach ((array) ($item['category_names'] ?? array()) as $category) { $categories[] = (string) $category; }
        $aspects = array();
        $product_type_aspects = array();
        foreach ((array) ($raw['localizedAspects'] ?? array()) as $aspect) {
            if (!is_array($aspect)) { continue; }
            $aspect_name = (string) ($aspect['name'] ?? '');
            $aspect_value = (string) ($aspect['value'] ?? '');
            $aspects[] = $aspect_name;
            $aspects[] = $aspect_value;
            $normalized_name = $this->ebay_topic_text($aspect_name);
            if (in_array($normalized_name, array('produktart','produkttyp','product type','producttype'), true)) {
                $product_type_aspects[] = $aspect_value;
            }
        }
        return array(
            'title'=>$this->ebay_topic_text((string) ($item['title'] ?? ($raw['title'] ?? ''))),
            'category'=>$this->ebay_topic_text(implode(' ', array_filter($categories))),
            'aspects'=>$this->ebay_topic_text(implode(' ', array_filter($aspects))),
            // Structured eBay Productart is stronger evidence than an arbitrary
            // aspect value. It may identify the exact product even when the
            // marketing title uses a brand/model synonym (e.g. Naturmineral).
            'product_type'=>$this->ebay_topic_text(implode(' ', array_filter($product_type_aspects))),
            'description'=>$this->ebay_topic_text((string) ($item['short_description'] ?? ($raw['shortDescription'] ?? ''))),
        );
    }

    private function ebay_private_phrase_present($text, $phrase) {
        $text = $this->ebay_topic_text((string) $text);
        $phrase = $this->ebay_topic_text((string) $phrase);
        if ($text === '' || $phrase === '') { return false; }
        if (strpos(' ' . $text . ' ', ' ' . $phrase . ' ') !== false) { return true; }
        $needle_tokens = $this->ebay_topic_tokens($phrase);
        if (count($needle_tokens) !== 1) { return false; }
        $needle = (string) $needle_tokens[0];
        if (strlen($needle) < 5) { return false; }
        $stem = $this->ebay_topic_stem($needle);
        foreach ($this->ebay_topic_tokens($text) as $token) {
            if (strlen($token) >= 5 && $this->ebay_topic_stem($token) === $stem) { return true; }
        }
        return false;
    }

    /**
     * Workflow V2 PRIVATE routing. PRIVATE has exactly eight coarse HivePress
     * destinations. It must never be classified through the 329 product pages.
     * Search profiles are only a weak prior; real title/category/aspect evidence
     * is mandatory for an automatic route.
     */
    public function ebay_classify_portal_item($item, $rule) {
        $catalog = $this->ebay_portal_catalog();
        if (is_wp_error($catalog)) { return $catalog; }
        $item = is_array($item) ? $item : array();
        $rule = is_array($rule) ? $rule : array();
        $policy_reason = $this->ebay_content_policy_reason($item);
        if ($policy_reason !== '') { return new WP_Error('ebay_content_policy_blocked', $policy_reason); }

        $evidence = $this->ebay_item_topic_evidence($item);
        $normalized = $this->ebay_topic_text($evidence);
        if ($normalized === '') { return new WP_Error('ebay_topic_evidence_missing', 'eBay-Angebot enthaelt keine verwertbare Fachinformation.'); }
        // Hard negatives always win before any positive product-domain proof.
        foreach ((array) ($catalog['hard_negative_markers'] ?? array()) as $marker) {
            if ($this->ebay_topic_negative_present($normalized, $marker)) {
                return new WP_Error('ebay_portal_topic_negative', 'Fachfremdes Ausschlusssignal im eBay-Angebot: ' . sanitize_text_field((string) $marker));
            }
        }
        $strong_horse_hits = array();
        foreach ((array) ($catalog['strong_horse_markers'] ?? array()) as $marker) {
            if ($this->ebay_topic_term_present($normalized, $marker)) { $strong_horse_hits[] = sanitize_text_field((string) $marker); }
        }
        // V6.26: controlled inherently equestrian product identities are domain
        // evidence themselves. A real listing titled simply "Damen Reitstiefel"
        // must not be rejected merely because it does not repeat "Pferd". The
        // marker list is explicit and hard negatives above still veto Cowboy/
        // Western/toy/etc. Relation references such as "Helmtasche fuer Reithelm"
        // are excluded by ebay_business_primary_title_section().
        $private_sections = $this->ebay_business_evidence_sections($item);
        foreach ($this->ebay_business_inherent_domain_hits($catalog, $private_sections) as $marker) {
            $strong_horse_hits[] = 'product:' . sanitize_text_field((string)$marker);
        }
        $strong_horse_hits = array_values(array_unique($strong_horse_hits));
        if (!$strong_horse_hits) { return new WP_Error('ebay_portal_topic_missing', 'Kein expliziter Pferde-/Reitsportbezug im realen eBay-Angebot.'); }

        // Workflow V2 root rule: if the real eBay facts identify one canonical
        // product concept unambiguously, PRIVATE uses that concept only to pick
        // one of the eight coarse HivePress buckets. It never routes through a
        // WordPress product page. Generic/unclear items fall back to the coarse
        // bucket vocabulary below.
        $concept_match = $this->ebay_business_classify_portal_item_strict($item, $rule);
        if (!is_wp_error($concept_match) && !empty($concept_match['product_concept_id'])) {
            $concept_id = sanitize_key((string) $concept_match['product_concept_id']);
            $concept_collections = array(
                (array)($catalog['business_concepts'] ?? array()),
                (array)($catalog['business_hub_concepts'] ?? array()),
            );
            foreach ($concept_collections as $concepts) {
                foreach ($concepts as $concept) {
                    if (!is_array($concept) || sanitize_key((string) ($concept['id'] ?? '')) !== $concept_id) { continue; }
                    $primary_page = is_array($concept['target_pages'][0] ?? null) ? $concept['target_pages'][0] : array();
                    // Target-page metadata is canonical. The derived top-level
                    // convenience field may be stale after taxonomy moves.
                    $concept_bucket = sanitize_title((string) ($primary_page['private_bucket_slug'] ?? $concept['private_bucket_slug'] ?? ''));
                    if ($concept_bucket !== '' && isset($catalog['private_bucket_profiles'][$concept_bucket])) {
                        $label = sanitize_text_field((string) ($catalog['private_bucket_profiles'][$concept_bucket]['label'] ?? $concept_bucket));
                        return array(
                            'status'=>'ready','score'=>min(100, max(1, absint($concept_match['score'] ?? 100))),
                            'product_slug'=>'','product_title'=>'','hub'=>'Private Anzeigen','main_hub'=>'Anzeigenmarkt',
                            'path'=>'Private Anzeigen > ' . $label,'private_bucket_slug'=>$concept_bucket,
                            'strong_horse_hits'=>$strong_horse_hits,'hits'=>(array) ($concept_match['hits'] ?? array()),
                            'evidence_hash'=>hash('sha256', $normalized . '|private-concept-v2|' . $concept_id),
                            'private_match_contract'=>'bucket_v2','private_match_source'=>'canonical_product_concept',
                            'private_product_concept_id'=>$concept_id,
                        );
                    }
                    break 2;
                }
            }
        }

        $sections = $this->ebay_workflow_evidence_sections($item);
        $profiles = is_array($catalog['private_bucket_profiles'] ?? null) ? $catalog['private_bucket_profiles'] : array();
        $rule_bucket = sanitize_title((string) ($rule['target_term_slug'] ?? $rule['id'] ?? ''));
        $ranked = array();
        foreach ($profiles as $bucket=>$profile) {
            if (!is_array($profile)) { continue; }
            $bucket = sanitize_title((string) $bucket);
            $score = 0; $hits = array(); $real_hits = 0;
            $phrases = array_values(array_unique(array_filter(array_merge((array) ($profile['strong_phrases'] ?? array()), (array) ($profile['phrases'] ?? array())))));
            $strong_map = array();
            foreach ((array) ($profile['strong_phrases'] ?? array()) as $p) { $strong_map[$this->ebay_topic_text($p)] = true; }
            foreach ($phrases as $phrase) {
                $norm_phrase = $this->ebay_topic_text($phrase);
                if ($norm_phrase === '') { continue; }
                $strong = isset($strong_map[$norm_phrase]);
                $sources = array();
                if ($this->ebay_private_phrase_present($sections['title'], $phrase)) { $score += $strong ? 60 : 35; $sources[]='title'; }
                if ($this->ebay_private_phrase_present($sections['category'], $phrase)) { $score += $strong ? 45 : 28; $sources[]='category'; }
                if ($this->ebay_private_phrase_present($sections['aspects'], $phrase)) { $score += $strong ? 35 : 22; $sources[]='aspect'; }
                if (!$sources && $this->ebay_private_phrase_present($sections['description'], $phrase)) { $score += $strong ? 8 : 4; $sources[]='description'; }
                if ($sources) { $hits[$norm_phrase] = implode('+', $sources); $real_hits++; }
            }

            if ($bucket === 'pferde-ponys') {
                $title_animal = false; $category_animal = false;
                foreach ((array) ($profile['phrases'] ?? array()) as $phrase) {
                    if ($this->ebay_private_phrase_present($sections['title'], $phrase)) { $title_animal = true; }
                    if ($this->ebay_private_phrase_present($sections['category'], $phrase)) { $category_animal = true; }
                }
                if (!$title_animal || !$category_animal) { $score = 0; $real_hits = 0; }
                else { $score += 80; }
            }

            // Search rule is deliberately not evidence; it may only break a close tie.
            if ($real_hits > 0 && $bucket === $rule_bucket) { $score += 8; }
            if ($real_hits <= 0) { continue; }
            $ranked[] = array(
                'bucket'=>$bucket,
                'label'=>sanitize_text_field((string) ($profile['label'] ?? $bucket)),
                'score'=>$score,
                'min_score'=>max(1, absint($profile['min_score'] ?? 55)),
                'min_margin'=>max(0, absint($profile['min_margin'] ?? 12)),
                'hits'=>$hits,
            );
        }
        usort($ranked, static function($a,$b){ return ((int)$b['score'] <=> (int)$a['score']) ?: strcmp((string)$a['bucket'],(string)$b['bucket']); });
        if (!$ranked) { return new WP_Error('ebay_private_bucket_missing', 'Kein belastbarer Private-Anzeigen-Fachbereich aus realen Angebotsdaten erkannt.'); }
        $best = $ranked[0]; $second = $ranked[1] ?? null;
        if ((int) $best['score'] < (int) $best['min_score']) {
            return new WP_Error('ebay_private_bucket_low_confidence', 'Private-Anzeigen-Fachbereich ist nicht belastbar genug.');
        }
        if (is_array($second) && ((int)$best['score'] - (int)$second['score']) < (int)$best['min_margin']) {
            return new WP_Error('ebay_private_bucket_ambiguous', 'Private-Anzeigen-Fachbereich ist nicht eindeutig genug: ' . sanitize_key((string)$best['bucket']) . ' / ' . sanitize_key((string)$second['bucket']) . '.');
        }
        return array(
            'status'=>'ready',
            'score'=>min(100, max(1, (int) $best['score'])),
            'product_slug'=>'',
            'product_title'=>'',
            'hub'=>'Private Anzeigen',
            'main_hub'=>'Anzeigenmarkt',
            'path'=>'Private Anzeigen > ' . (string) $best['label'],
            'private_bucket_slug'=>(string) $best['bucket'],
            'strong_horse_hits'=>$strong_horse_hits,
            'hits'=>(array) $best['hits'],
            'evidence_hash'=>hash('sha256', $normalized . '|private-v2|' . (string)$best['bucket']),
            'private_match_contract'=>'bucket_v2',
        );
    }

    /**
     * V5.28 – fail-closed BUSINESS-Zielklassifikation.
     *
     * Die allgemeine Portal-Klassifikation bleibt fuer PRIVATE unveraendert.
     * BUSINESS darf dagegen nur dann automatisch einen Produktslot gewinnen,
     * wenn der konkrete Produktbegriff im realen Angebotstitel getragen wird
     * und die uebrigen eBay-Fakten diesen Treffer nicht widersprechen.
     * Generische Pferde-/Reitsportbegriffe, Farben, "Zubehoer" oder reine
     * Beschreibungstreffer duerfen kein Produktziel mehr erzeugen.
     */
    private function ebay_business_match_stop_tokens() {
        return array_flip(array(
            'pferd','pferde','pony','ponys','fohlen','reiter','reiten','reit','reitsport','equestrian',
            'zubehor','zubehoer','artikel','angebot','angebote','produkt','produkte','set','sets','original','universal',
            'neu','gebraucht','damen','herren','kinder','schwarz','braun','blau','rot','grun','gruen','weiss','weis','beige',
            'grosse','groesse','size','cm','mm','kg','stuck','stueck','paar','fur','fuer','mit','ohne'
        ));
    }

    private function ebay_business_distinctive_tokens($text) {
        $stop = $this->ebay_business_match_stop_tokens();
        $tokens = array();
        foreach ($this->ebay_topic_tokens((string) $text) as $token) {
            $token = $this->ebay_topic_text($token);
            if ($token === '' || strlen($token) < 3 || isset($stop[$token])) { continue; }
            $tokens[$token] = $token;
        }
        return array_values($tokens);
    }

    /** Strikter Tokenvergleich: nur identisch oder derselbe Wortstamm, niemals Teilstring. */
    private function ebay_business_strict_token_present($text, $needle) {
        $needle = $this->ebay_topic_text((string) $needle);
        if ($needle === '') { return false; }
        $needle_stem = $this->ebay_topic_stem($needle);
        foreach ($this->ebay_topic_tokens((string) $text) as $token) {
            $token = $this->ebay_topic_text($token);
            if ($token === $needle) { return true; }
            if (strlen($needle) >= 5 && strlen($token) >= 5 && $this->ebay_topic_stem($token) === $needle_stem) { return true; }
        }
        return false;
    }

    /**
     * German eBay categories often carry the product family as a compound
     * (e.g. "Pferdedecken", "Sattelzubehör"). For corroboration only, a
     * sufficiently long hub token may therefore occur at the beginning/end of
     * a category/aspect token. This is never used as the primary product match.
     */
    private function ebay_business_context_token_present($text, $needle) {
        if ($this->ebay_business_strict_token_present($text, $needle)) { return true; }
        $needle = $this->ebay_topic_text((string) $needle);
        if (strlen($needle) < 5) { return false; }
        foreach ($this->ebay_topic_tokens((string) $text) as $token) {
            $token = $this->ebay_topic_text($token);
            if (strlen($token) <= strlen($needle)) { continue; }
            if (strpos($token, $needle) === 0 || substr($token, -strlen($needle)) === $needle) { return true; }
        }
        return false;
    }

    /**
     * Hub-Fallback fuer konkrete Produktfamilien, die im Portal selbst auf Ebene 2
     * routbar sind (z.B. ein normaler Sattel), aber keinen eigenen Leaf-Eintrag
     * besitzen. Der Titel muss den Hub als eigenes Wort oder als deutsches
     * Produktkompositum mit Hub-Suffix tragen; Kategorie/Aspekte muessen denselben
     * Fachbegriff unabhaengig bestaetigen. Reine Praefix-Nennungen wie
     * "Sattelgurt" gelten deshalb NICHT als "Sattel".
     */
    private function ebay_business_hub_title_token_present($text, $needle) {
        if ($this->ebay_business_strict_token_present($text, $needle)) { return true; }
        $needle = $this->ebay_topic_text((string) $needle);
        if (strlen($needle) < 5) { return false; }
        foreach ($this->ebay_topic_tokens((string) $text) as $token) {
            $token = $this->ebay_topic_text($token);
            if (strlen($token) <= strlen($needle) + 2) { continue; }
            if (substr($token, -strlen($needle)) === $needle) { return true; }
        }
        return false;
    }

    /**
     * Eindeutige Reitsport-Produktbegriffe tragen den Fachkontext selbst.
     * Ausschliesslich strikter Token-/Stammvergleich in Primaertitel, eBay-Kategorie
     * oder Aspekten. Relationelle Referenzen im Titel zaehlen nicht als Produkttyp.
     */
    private function ebay_business_inherent_domain_hits($catalog, $sections) {
        $hits = array();
        $primary = $this->ebay_business_primary_title_section((string) ($sections['title'] ?? ''));
        $context = trim((string) ($sections['category'] ?? '') . ' ' . (string) ($sections['aspects'] ?? ''));
        foreach ((array) ($catalog['business_inherent_markers'] ?? array()) as $marker) {
            $marker = sanitize_text_field((string) $marker);
            if ($marker === '') { continue; }
            if (($primary !== '' && $this->ebay_business_strict_token_present($primary, $marker))
                || $this->ebay_business_strict_token_present($context, $marker)) {
                $hits[] = $marker;
            }
        }
        return array_values(array_unique($hits));
    }

    private function ebay_business_hub_concept_candidates($catalog, $sections) {
        $ranked = array();
        foreach ((array) ($catalog['business_hub_concepts'] ?? array()) as $concept) {
            if (!is_array($concept)) { continue; }
            $tokens = $this->ebay_business_distinctive_tokens((string) ($concept['title'] ?? ''));
            if (!$tokens) { continue; }

            // Explizite Hub-Aliase sind der kontrollierte Fallback fuer reale
            // Produktfamilien ohne eigenen Leaf (z.B. Reithose -> Reiterbedarf).
            // Nur der Primaertitel darf den Alias tragen. "Tasche fuer Reithelm"
            // oder andere relationale Referenzen koennen dadurch nie gewinnen.
            $alias_hits = array();
            foreach ((array) ($concept['aliases'] ?? array()) as $alias) {
                if ($this->ebay_business_primary_title_token_present((string) ($sections['title'] ?? ''), (string) $alias)) {
                    $alias_hits[] = sanitize_text_field((string) $alias);
                }
            }
            if ($alias_hits) {
                $concept['raw_score'] = 215 + min(60, count($alias_hits) * 20);
                $concept['confidence'] = min(96, 88 + count($alias_hits) * 4);
                $concept['hits'] = array_values(array_unique($alias_hits));
                $concept['hit_sources'] = array_fill_keys($concept['hits'], 'primary_title_alias');
                $ranked[] = $concept;
                continue;
            }

            $title_hits = 0; $context_hits = 0; $hits = array();
            foreach ($tokens as $token) {
                if ($this->ebay_business_hub_title_token_present($sections['title'], $token)) {
                    $title_hits++;
                    $hits[$token] = 'title';
                }
                if ($this->ebay_business_context_token_present($sections['category'] . ' ' . $sections['aspects'], $token)) {
                    $context_hits++;
                    $hits[$token] = isset($hits[$token]) ? $hits[$token] . '+context' : 'context';
                }
            }
            // Hub-Routing ist bewusst strenger als Leaf-Routing: alle Hub-Tokens
            // muessen vom Titel getragen werden und mindestens eines davon muss
            // durch reale eBay-Kategorie/Aspekte bestaetigt sein.
            if ($title_hits !== count($tokens) || $context_hits < 1) { continue; }

            if (!empty($concept['requires_main_context'])) {
                $main_hits = 0;
                $primary = is_array($concept['target_pages'][0] ?? null) ? $concept['target_pages'][0] : array();
                foreach ($this->ebay_business_distinctive_tokens((string) ($primary['main_hub'] ?? '')) as $main_token) {
                    if ($this->ebay_business_context_token_present(
                        $sections['title'] . ' ' . $sections['category'] . ' ' . $sections['aspects'],
                        $main_token
                    )) { $main_hits++; }
                }
                if ($main_hits < 1) { continue; }
            }

            $phrase = $this->ebay_topic_text((string) ($concept['title'] ?? ''));
            $phrase_title = $phrase !== '' && strpos(' ' . $sections['title'] . ' ', ' ' . $phrase . ' ') !== false;
            $concept['raw_score'] = 180 + ($title_hits * 45) + ($context_hits * 25) + ($phrase_title ? 40 : 0);
            $concept['confidence'] = min(100, 82 + ($context_hits * 8) + ($phrase_title ? 10 : 0));
            $concept['hits'] = array_keys($hits);
            $concept['hit_sources'] = $hits;
            $ranked[] = $concept;
        }
        usort($ranked, static function($a, $b) {
            $cmp = absint($b['raw_score'] ?? 0) <=> absint($a['raw_score'] ?? 0);
            if ($cmp !== 0) { return $cmp; }
            return strnatcasecmp((string) ($a['id'] ?? ''), (string) ($b['id'] ?? ''));
        });
        return $ranked;
    }

    private function ebay_business_evidence_sections($item) {
        return $this->ebay_workflow_evidence_sections($item);
    }

    /**
     * Primaerer Produkttitel vor relationalen Zubehoer-/Kompatibilitaetsphrasen.
     * Damit ist z.B. "Reithandschuhe Damen Leder" ein belastbarer direkter
     * Produkttreffer, waehrend "Helmtasche fuer Reithelm" den Reithelm nur als
     * Bezugsobjekt nennt. Der komplette Titel bleibt fuer Corroboration und
     * Mehrdeutigkeitspruefung erhalten; diese Zone wird nur fuer die direkte
     * Ein-Wort-Leaf-Freigabe verwendet.
     */
    private function ebay_business_primary_title_section($title) {
        $title = $this->ebay_topic_text((string) $title);
        if ($title === '') { return ''; }
        $boundaries = array_flip(array(
            'fur','fuer','for','im','in','am','an','auf','bei','zur','zum','als','passend','geeignet','kompatibel','compatible','fits',
            'mit','with','ohne','without','inkl','inklusive','including',
            'zubehor','zubehoer','accessory','accessories','ersatzteil','ersatzteile'
        ));
        $tokens = preg_split('/\s+/', $title);
        $primary = array();
        foreach ((array) $tokens as $index => $token) {
            $token = trim((string) $token);
            if ($token === '') { continue; }
            if (isset($boundaries[$token])) {
                if ($index === 0) { return ''; }
                break;
            }
            $primary[] = $token;
        }
        return trim(implode(' ', $primary));
    }

    /**
     * Direkter Titelvertrag fuer eindeutige Ein-Wort-Leaf-Konzepte.
     * Singular/Plural wird ueber denselben konservativen Stammvergleich wie der
     * restliche BUSINESS-Klassifikator behandelt. Keine Teilstring-/Fuzzy-Suche.
     */
    private function ebay_business_primary_title_token_present($title, $needle) {
        $primary = $this->ebay_business_primary_title_section($title);
        if ($primary === '') { return false; }
        return $this->ebay_business_strict_token_present($primary, $needle);
    }

    /** Resolve the exact catalog concept carried by a V6.17+ BUSINESS profile. */
    private function ebay_business_expected_concept_from_rule($catalog, $rule) {
        $rule = is_array($rule) ? $rule : array();
        $concept_id = sanitize_key((string)($rule['business_concept_id'] ?? ''));
        if ($concept_id === '') { return array(); }
        foreach (array('product'=>'business_concepts','hub'=>'business_hub_concepts') as $kind=>$field) {
            foreach ((array)($catalog[$field] ?? array()) as $concept) {
                if (!is_array($concept) || sanitize_key((string)($concept['id'] ?? '')) !== $concept_id) { continue; }
                return array('kind'=>$kind,'concept'=>$concept);
            }
        }
        return array();
    }

    /**
     * An exact discovery profile may use its Pferd-scoped query only as domain
     * context after the real eBay offer independently proves the expected product.
     * The query can never create a product match by itself.
     */
    private function ebay_business_exact_profile_horse_scope($rule) {
        $rule = is_array($rule) ? $rule : array();
        if (sanitize_key((string)($rule['business_concept_id'] ?? '')) === '') { return false; }
        $query = $this->ebay_topic_text((string)($rule['query'] ?? ''));
        foreach (array('pferd','pferde','pony','ponys','fohlen','horse','horses','equine','equestrian') as $marker) {
            if ($this->ebay_topic_term_present($query, $marker)) { return true; }
        }
        return false;
    }

    /**
     * Verify an expected product concept from the offer itself. Primary title is
     * strongest; eBay Productart/aspects may substitute only together with the
     * category and never for obvious accessory-primary titles. This is the
     * fail-closed bridge for products whose real listing does not literally say
     * "Pferd" (e.g. Gebiss, Weidezaungeraet, Regendecke).
     */
    private function ebay_business_expected_concept_evidence($concept, $sections) {
        $concept = is_array($concept) ? $concept : array();
        $sections = is_array($sections) ? $sections : array();
        $concept_title = (string)($concept['title'] ?? '');
        // Product labels often contain a relational use-context ("Heunetze fuer
        // Anhaenger", "Torgriffe mit Feder"). For an exact profile the product
        // core before that relation is the identity proof; the trailing context
        // must not become a second mandatory product token.
        $concept_primary = $this->ebay_business_primary_title_section($concept_title);
        $tokens = $this->ebay_business_distinctive_tokens($concept_primary !== '' ? $concept_primary : $concept_title);
        if (!$tokens) { return array('ok'=>false); }
        $primary = $this->ebay_business_primary_title_section((string)($sections['title'] ?? ''));
        $aspects = (string)($sections['aspects'] ?? '');
        $product_type = (string)($sections['product_type'] ?? '');
        $category = (string)($sections['category'] ?? '');
        $primary_hits = $aspect_hits = $product_type_hits = $category_hits = 0;
        $direct_covered = array();
        $context_covered = array();
        foreach ($tokens as $token) {
            if ($this->ebay_business_strict_token_present($primary, $token)) { $primary_hits++; $direct_covered[$token]=true; }
            if ($this->ebay_business_strict_token_present($aspects, $token)) { $aspect_hits++; $direct_covered[$token]=true; }
            if ($this->ebay_business_strict_token_present($product_type, $token)) { $product_type_hits++; $direct_covered[$token]=true; }
            if ($this->ebay_business_strict_token_present($category, $token)) { $category_hits++; $context_covered[$token]=true; }
        }
        $required = count($tokens) <= 1 ? 1 : (int)ceil(count($tokens) * 0.67);
        $direct_count = count($direct_covered);
        $accessory_primary = false;
        foreach (array('tasche','huelle','hulle','cover','liner','innenfutter','ersatz','adapter','halterung','visier','ueberzug','uberzug','zubehoer','zubehor','accessory') as $accessory) {
            if ($this->ebay_business_strict_token_present($primary, $accessory)) { $accessory_primary = true; break; }
            // German marketplace titles frequently glue an accessory noun to the
            // referenced product (Helmtasche, Satteltasche, Deckenhalterung).
            // Exact-profile evidence must not turn that relation into the product.
            $accessory = $this->ebay_topic_text($accessory);
            if ($accessory === '' || strlen($accessory) < 4) { continue; }
            foreach ($this->ebay_topic_tokens($primary) as $primary_token) {
                $primary_token = $this->ebay_topic_text((string)$primary_token);
                if (strlen($primary_token) <= strlen($accessory)) { continue; }
                if (substr($primary_token, -strlen($accessory)) === $accessory) {
                    $accessory_primary = true;
                    break 2;
                }
            }
        }
        $ok = false;
        if ($primary_hits >= $required) {
            $ok = true;
        } elseif (!$accessory_primary && $product_type_hits >= $required) {
            // Exact eBay Productart is a direct structured product identity. The
            // profile's Pferd scope is checked separately by the caller, and hard
            // negatives/accessory-primary titles are evaluated before this can
            // authorize a BUSINESS route.
            $ok = true;
        } elseif (!$accessory_primary && $aspect_hits >= $required && $category_hits >= 1) {
            $ok = true;
        }
        return array(
            'ok'=>$ok,'tokens'=>$tokens,'required'=>$required,'primary_hits'=>$primary_hits,
            'aspect_hits'=>$aspect_hits,'product_type_hits'=>$product_type_hits,'category_hits'=>$category_hits,'direct_count'=>$direct_count,
            'accessory_primary'=>$accessory_primary,
        );
    }

    /**
     * BUSINESS-spezifische Produktklassifikation gegen den vollstaendigen
     * Portal-Zielkatalog. Sie ist absichtlich konservativ: lieber Review als
     * eine fachlich falsche Produktkarte auf einer redaktionellen Seite.
     */
    private function ebay_business_classify_portal_item_strict($item, $rule) {
        $catalog = $this->ebay_portal_catalog();
        if (is_wp_error($catalog)) { return $catalog; }
        $item = is_array($item) ? $item : array();
        $rule = is_array($rule) ? $rule : array();
        $policy_reason = $this->ebay_content_policy_reason($item);
        if ($policy_reason !== '') { return new WP_Error('ebay_content_policy_blocked', $policy_reason); }

        $evidence = $this->ebay_item_topic_evidence($item);
        $normalized = $this->ebay_topic_text($evidence);
        if ($normalized === '') { return new WP_Error('ebay_topic_evidence_missing', 'eBay-Angebot enthaelt keine verwertbare Fachinformation.'); }
        $sections = $this->ebay_business_evidence_sections($item);
        if ($sections['title'] === '') { return new WP_Error('ebay_business_title_missing', 'BUSINESS-Angebot besitzt keinen verwertbaren Produkttitel.'); }
        // Hard negatives are evaluated before any exact-profile recovery. A
        // Pferd-scoped search must never whitelist toy/book/foreign-domain items.
        foreach ((array) ($catalog['hard_negative_markers'] ?? array()) as $marker) {
            if ($this->ebay_topic_negative_present($normalized, $marker)) {
                return new WP_Error('ebay_portal_topic_negative', 'Fachfremdes Ausschlusssignal im eBay-Angebot: ' . sanitize_text_field((string) $marker));
            }
        }

        $expected = $this->ebay_business_expected_concept_from_rule($catalog, $rule);
        $expected_concept = is_array($expected['concept'] ?? null) ? $expected['concept'] : array();
        $expected_kind = sanitize_key((string)($expected['kind'] ?? ''));
        $expected_evidence = $expected_concept ? $this->ebay_business_expected_concept_evidence($expected_concept, $sections) : array('ok'=>false);
        $exact_profile_scope = $expected_concept && $this->ebay_business_exact_profile_horse_scope($rule);

        $strong_horse_hits = array();
        foreach ((array) ($catalog['strong_horse_markers'] ?? array()) as $marker) {
            if ($this->ebay_topic_term_present($normalized, $marker)) { $strong_horse_hits[] = sanitize_text_field((string) $marker); }
        }
        foreach ($this->ebay_business_inherent_domain_hits($catalog, $sections) as $marker) {
            $strong_horse_hits[] = 'product:' . sanitize_text_field((string) $marker);
        }
        // V6.18: for an exact catalog profile, the search scope may establish
        // horse-domain context only AFTER real title/aspect/category data proves
        // the expected product concept independently. This fixes the V6.17 gate
        // that rejected most ordinary horse products merely because their title
        // did not repeat the word "Pferd".
        if (!$strong_horse_hits && $exact_profile_scope && !empty($expected_evidence['ok'])) {
            $strong_horse_hits[] = 'exact_profile:' . sanitize_key((string)($expected_concept['id'] ?? ''));
        }
        $strong_horse_hits = array_values(array_unique($strong_horse_hits));
        if (!$strong_horse_hits) { return new WP_Error('ebay_portal_topic_missing', 'Kein belastbarer Pferde-/Reitsportbezug aus Angebot oder exakt bestaetigtem Pferde-Suchprofil.'); }

        $ranked = array();
        $concept_pool = ($expected_kind === 'product' && $expected_concept) ? array($expected_concept) : (array) ($catalog['business_concepts'] ?? array());
        foreach ($concept_pool as $concept) {
            if (!is_array($concept)) { continue; }
            $tokens = $this->ebay_business_distinctive_tokens((string) ($concept['title'] ?? ''));
            if (!$tokens) { continue; }
            $title_hits = $primary_title_hits = $category_hits = $aspect_hits = $description_hits = 0;
            $covered = array(); $hit_tokens = array();
            foreach ($tokens as $token) {
                $sources = array();
                if ($this->ebay_business_strict_token_present($sections['title'], $token)) { $title_hits++; $covered[$token]=true; $sources[]='title'; }
                if ($this->ebay_business_primary_title_token_present($sections['title'], $token)) { $primary_title_hits++; $sources[]='primary_title'; }
                if ($this->ebay_business_strict_token_present($sections['category'], $token)) { $category_hits++; $covered[$token]=true; $sources[]='category'; }
                if ($this->ebay_business_strict_token_present($sections['aspects'], $token)) { $aspect_hits++; $covered[$token]=true; $sources[]='aspect'; }
                if ($this->ebay_business_strict_token_present($sections['description'], $token)) { $description_hits++; $sources[]='description'; }
                if ($sources) { $hit_tokens[$token]=implode('+',array_values(array_unique($sources))); }
            }
            $token_count = count($tokens);
            $core_coverage = count($covered);
            $required_coverage = $token_count <= 1 ? 1 : (int) ceil($token_count * 0.67);
            $concept_phrase = $this->ebay_topic_text((string) ($concept['title'] ?? ''));
            $phrase_title = $concept_phrase !== '' && strpos(' ' . $sections['title'] . ' ', ' ' . $concept_phrase . ' ') !== false;
            $hub_hits = 0;
            foreach ((array) ($concept['target_pages'] ?? array()) as $page) {
                foreach (array((string) ($page['hub'] ?? ''), (string) ($page['main_hub'] ?? '')) as $context_label) {
                    foreach ($this->ebay_business_distinctive_tokens($context_label) as $hub_token) {
                        if ($this->ebay_business_context_token_present($sections['category'] . ' ' . $sections['aspects'], $hub_token)) { $hub_hits++; }
                    }
                }
            }
            $is_expected_candidate = $expected_concept
                && sanitize_key((string)($concept['id'] ?? '')) === sanitize_key((string)($expected_concept['id'] ?? ''))
                && $exact_profile_scope;
            $expected_direct_verified = $is_expected_candidate && !empty($expected_evidence['ok']);
            // Generic/fallback profiles retain full-concept coverage. An exact
            // profile may use the independently verified product-core evidence
            // above (e.g. "Heunetze fuer Anhaenger" -> real title "Heunetze").
            if (!$expected_direct_verified && $core_coverage < $required_coverage) { continue; }
            // Generic/fallback profiles retain the old conservative title rule.
            // Only the exact catalog profile may accept Productart/aspect evidence
            // instead of a literal title token, and only after the independent
            // expected-concept verifier above passed.
            if (!$expected_direct_verified && $title_hits < 1) { continue; }
            if (!$expected_direct_verified && $token_count === 1 && $primary_title_hits < 1) { continue; }
            $exact_boost = $expected_direct_verified ? 28 : 0;
            $raw_score = ($phrase_title ? 120 : 0)
                + ($title_hits * 42) + ($category_hits * 18) + ($aspect_hits * 14) + ($description_hits * 3)
                + ($core_coverage === $token_count ? 24 : 0) + min(24, $hub_hits * 8) + $exact_boost;
            $confidence = 55 + min(30, $title_hits * 15) + min(10, ($category_hits + $aspect_hits) * 5)
                + ($phrase_title ? 10 : 0) + ($core_coverage === $token_count ? 10 : 0)
                + ($expected_direct_verified ? 20 : 0);
            $confidence = min(100, $confidence);
            if ($confidence < 80) { continue; }
            $concept['raw_score']=$raw_score; $concept['confidence']=$confidence;
            $concept['hits']=array_keys($hit_tokens); $concept['hit_sources']=$hit_tokens;
            $ranked[]=$concept;
        }
        usort($ranked, static function($a,$b){
            $cmp=absint($b['raw_score']??0)<=>absint($a['raw_score']??0);
            if($cmp!==0){return $cmp;}
            $cmp=absint($b['confidence']??0)<=>absint($a['confidence']??0);
            return $cmp!==0?$cmp:strnatcasecmp((string)($a['id']??''),(string)($b['id']??''));
        });
        // Exact catalog profiles may never drift into a neighbouring product or
        // hub. Coarse fallback profiles keep the controlled hub fallback.
        if (!$ranked && $expected_kind === 'hub' && $expected_concept) {
            $hub_catalog = $catalog;
            $hub_catalog['business_hub_concepts'] = array($expected_concept);
            $ranked = $this->ebay_business_hub_concept_candidates($hub_catalog, $sections);
        } elseif (!$ranked && !$expected_concept) {
            $ranked = $this->ebay_business_hub_concept_candidates($catalog, $sections);
        }
        if (!$ranked) { return new WP_Error('ebay_business_concept_missing', 'Kein belastbarer konkreter Produktbegriff oder routbares Produktfamilien-Ziel im eBay-BUSINESS-Angebot gefunden.'); }
        $best=$ranked[0]; $second=$ranked[1]??null;
        if (is_array($second)) {
            $margin=absint($best['raw_score']??0)-absint($second['raw_score']??0);
            if ($margin < 25) {
                return new WP_Error('ebay_business_concept_ambiguous', 'BUSINESS-Produktkonzept ist nicht eindeutig genug: ' . sanitize_key((string)($best['id']??'')) . ' / ' . sanitize_key((string)($second['id']??'')) . '.');
            }
        }
        $pages=array_values(array_filter((array)($best['target_pages']??array()),'is_array'));
        if (!$pages) { return new WP_Error('ebay_business_concept_target_missing', 'Produktkonzept besitzt kein Portalziel.'); }
        $primary=$pages[0];
        $target_slugs=array_values(array_unique(array_filter(array_map(static function($p){return sanitize_title((string)($p['slug']??''));},$pages))));
        $path=implode(' > ',array_filter(array((string)($primary['main_hub']??''),(string)($primary['hub']??''),(string)($best['title']??''))));
        return array(
            'status'=>'ready','score'=>absint($best['confidence']??0),
            'product_concept_id'=>sanitize_key((string)($best['id']??'')),
            'concept_kind'=>sanitize_key((string)($best['concept_kind']??'product')),
            'product_slug'=>sanitize_title((string)($primary['slug']??'')),
            'product_target_slugs'=>$target_slugs,
            'product_title'=>sanitize_text_field((string)($best['title']??'')),
            'hub'=>sanitize_text_field((string)($primary['hub']??'')),
            'main_hub'=>sanitize_text_field((string)($primary['main_hub']??'')),
            'path'=>$path,
            'private_bucket_slug'=>sanitize_title((string)($primary['private_bucket_slug']??($best['private_bucket_slug']??''))),
            'strong_horse_hits'=>$strong_horse_hits,'hits'=>(array)($best['hits']??array()),'hit_sources'=>(array)($best['hit_sources']??array()),
            'evidence_hash'=>hash('sha256',$normalized.'|business-concept-v3|'.sanitize_key((string)($best['id']??''))),
            'business_match_contract'=>'concept_v3',
        );
    }

    private function ebay_items_table() {
        global $wpdb;
        return $wpdb->prefix . 'ppar_ebay_items';
    }

    public function ebay_settings_defaults() {
        return array(
            'schema' => '1.2',
            'enabled' => false,
            'environment' => 'production',
            'client_id' => '',
            'client_secret' => '',
            'epn_campaign_id' => '',
            'affiliate_reference_prefix' => 'pferde-atelier',
            'marketplace_id' => 'EBAY_DE',
            'delivery_country' => 'DE',
            'delivery_postal_code' => '',
            'private_enabled' => true,
            'business_enabled' => true,
            'private_parent_term_id' => 0,
            'private_root_term_id' => 0,
            'private_post_status' => 'draft',
            'private_auto_publish' => false,
            'private_listing_author_id' => 0,
            'api_terms_confirmed' => false,
            'privacy_policy_confirmed' => false,
            'stale_hours' => 6,
            'sync_interval_hours' => 3,
            'inventory_refresh_enabled' => true,
            'inventory_refresh_max_per_run' => 1200,
            'max_per_rule' => 50,
            'max_pages_per_profile' => 4,
            'max_requests_per_run' => 40,
            'run_time_budget_seconds' => 20,
            // V6.19 quality/cap layer. Same discovery/output architecture, but
            // only bounded, ranked inventories may reach public delivery.
            'private_active_cap' => 250,
            'private_leaf_cap' => 30,
            'business_active_cap' => 1000,
            'business_candidate_pool_per_concept' => 10,
            'business_reserve_per_concept' => 2,
            'business_visible_per_target' => 3,
            'business_min_feedback_percentage' => 99.0,
            'business_min_feedback_score' => 100,
            'business_preferred_feedback_percentage' => 99.5,
            'business_preferred_feedback_score' => 500,
            'business_max_same_seller_per_block' => 1,
            'rules' => $this->ebay_catalog_rules(),
            'catalog_verified_sha256' => '',
            'catalog_verified_at' => 0,
            'last_test' => array(),
            'last_sync' => array(),
            'last_refresh' => array(),
        );
    }

    public function ebay_default_rules() {
        return $this->ebay_catalog_rules();
    }

    private function ebay_settings() {
        if (isset($this->ebay_run_settings_override) && is_array($this->ebay_run_settings_override)) {
            return $this->ebay_normalize_settings($this->ebay_run_settings_override, true);
        }
        $stored = get_option(self::OPTION_NETWORK_EBAY, array());
        $stored = is_array($stored) ? $stored : array();
        $settings = $this->ebay_normalize_settings(array_merge($this->ebay_settings_defaults(), $stored), true);
        // V6.20: V6.19 shipped 300 as the global BUSINESS default. With more
        // than 100 matched product concepts that mathematically starved slot 2/3
        // (and, above 300 concepts, even slot 1). Treat exactly that old default
        // as migrated to the hard safety ceiling. The real public bound remains
        // max. three selected offers per product concept, never the raw inventory.
        if (isset($stored['business_active_cap']) && absint($stored['business_active_cap']) === 300) {
            $settings['business_active_cap'] = 1000;
        }
        // Zugangsdaten können sicherer außerhalb der Datenbank in wp-config.php
        // hinterlegt werden. Definierte Konstanten haben immer Vorrang.
        if (defined('PPAR_EBAY_CLIENT_ID') && trim((string) PPAR_EBAY_CLIENT_ID) !== '') {
            $settings['client_id'] = substr(sanitize_text_field((string) PPAR_EBAY_CLIENT_ID), 0, 255);
        }
        if (defined('PPAR_EBAY_CLIENT_SECRET') && trim((string) PPAR_EBAY_CLIENT_SECRET) !== '') {
            $settings['client_secret'] = substr(trim((string) PPAR_EBAY_CLIENT_SECRET), 0, 255);
        }
        if (defined('PPAR_EBAY_EPN_CAMPAIGN_ID')) {
            $campaign = preg_replace('/\D+/', '', (string) PPAR_EBAY_EPN_CAMPAIGN_ID);
            if (strlen($campaign) === 10) { $settings['epn_campaign_id'] = $campaign; }
        }
        return $settings;
    }

    public function ebay_normalize_settings($settings, $preserve_secret = true) {
        $defaults = $this->ebay_settings_defaults();
        $settings = is_array($settings) ? $settings : array();
        $out = $defaults;
        $out['enabled'] = !empty($settings['enabled']);
        $out['environment'] = in_array((string) ($settings['environment'] ?? ''), array('production','sandbox'), true) ? (string) $settings['environment'] : 'production';
        $out['client_id'] = substr(sanitize_text_field((string) ($settings['client_id'] ?? '')), 0, 255);
        $out['client_secret'] = $preserve_secret ? substr(trim((string) ($settings['client_secret'] ?? '')), 0, 255) : '';
        $campaign = preg_replace('/\D+/', '', (string) ($settings['epn_campaign_id'] ?? ''));
        $out['epn_campaign_id'] = strlen($campaign) === 10 ? $campaign : '';
        $prefix = sanitize_key((string) ($settings['affiliate_reference_prefix'] ?? 'pferde-atelier'));
        $out['affiliate_reference_prefix'] = $prefix !== '' ? substr($prefix, 0, 60) : 'pferde-atelier';
        $out['marketplace_id'] = 'EBAY_DE';
        $out['delivery_country'] = 'DE';
        $out['delivery_postal_code'] = substr(preg_replace('/[^0-9A-Za-z -]/', '', (string) ($settings['delivery_postal_code'] ?? '')), 0, 12);
        $out['private_enabled'] = !empty($settings['private_enabled']);
        $out['business_enabled'] = !empty($settings['business_enabled']);
        $out['private_parent_term_id'] = absint($settings['private_parent_term_id'] ?? 0);
        $out['private_root_term_id'] = absint($settings['private_root_term_id'] ?? 0);
        $out['private_post_status'] = 'draft';
        $out['private_auto_publish'] = !empty($settings['private_auto_publish']);
        $out['private_listing_author_id'] = absint($settings['private_listing_author_id'] ?? 0);
        $out['api_terms_confirmed'] = !empty($settings['api_terms_confirmed']);
        $out['privacy_policy_confirmed'] = !empty($settings['privacy_policy_confirmed']);
        $out['stale_hours'] = 6;
        $out['sync_interval_hours'] = 3;
        $out['inventory_refresh_enabled'] = array_key_exists('inventory_refresh_enabled', $settings) ? !empty($settings['inventory_refresh_enabled']) : true;
        $out['inventory_refresh_max_per_run'] = max(1200, min(2000, absint($settings['inventory_refresh_max_per_run'] ?? 1200)));
        $out['max_per_rule'] = max(1, min(50, absint($settings['max_per_rule'] ?? 50)));
        $out['max_pages_per_profile'] = max(1, min(20, absint($settings['max_pages_per_profile'] ?? 4)));
        $out['max_requests_per_run'] = max(1, min(40, absint($settings['max_requests_per_run'] ?? 40)));
        $out['run_time_budget_seconds'] = max(10, min(30, absint($settings['run_time_budget_seconds'] ?? 20)));
        $out['private_active_cap'] = max(50, min(250, absint($settings['private_active_cap'] ?? 250)));
        $out['private_leaf_cap'] = max(5, min(100, absint($settings['private_leaf_cap'] ?? 30)));
        $out['business_active_cap'] = max(30, min(1000, absint($settings['business_active_cap'] ?? 1000)));
        $out['business_candidate_pool_per_concept'] = max(5, min(20, absint($settings['business_candidate_pool_per_concept'] ?? 10)));
        $out['business_reserve_per_concept'] = max(0, min(5, absint($settings['business_reserve_per_concept'] ?? 2)));
        $out['business_visible_per_target'] = 3;
        $min_feedback_pct = is_numeric($settings['business_min_feedback_percentage'] ?? null) ? (float) $settings['business_min_feedback_percentage'] : 99.0;
        $preferred_feedback_pct = is_numeric($settings['business_preferred_feedback_percentage'] ?? null) ? (float) $settings['business_preferred_feedback_percentage'] : 99.5;
        $out['business_min_feedback_percentage'] = max(95.0, min(100.0, round($min_feedback_pct, 2)));
        $out['business_min_feedback_score'] = max(1, min(10000000, absint($settings['business_min_feedback_score'] ?? 100)));
        $out['business_preferred_feedback_percentage'] = max($out['business_min_feedback_percentage'], min(100.0, round($preferred_feedback_pct, 2)));
        $out['business_preferred_feedback_score'] = max($out['business_min_feedback_score'], min(10000000, absint($settings['business_preferred_feedback_score'] ?? 500)));
        $out['business_max_same_seller_per_block'] = 1;
        $out['rules'] = $this->ebay_catalog_rules();
        $verified_hash = strtolower(sanitize_text_field((string) ($settings['catalog_verified_sha256'] ?? '')));
        $out['catalog_verified_sha256'] = preg_match('/^[a-f0-9]{64}$/', $verified_hash) ? $verified_hash : '';
        $out['catalog_verified_at'] = absint($settings['catalog_verified_at'] ?? 0);
        $out['last_test'] = is_array($settings['last_test'] ?? null) ? $settings['last_test'] : array();
        $out['last_sync'] = is_array($settings['last_sync'] ?? null) ? $settings['last_sync'] : array();
        $out['last_refresh'] = is_array($settings['last_refresh'] ?? null) ? $settings['last_refresh'] : array();
        return $out;
    }

    public function ebay_normalize_rules($rules) {
        if (is_string($rules)) {
            $decoded = json_decode($rules, true);
            $rules = is_array($decoded) ? $decoded : array();
        }
        $safe = array();
        foreach ((array) $rules as $index => $rule) {
            if (!is_array($rule)) { continue; }
            $id = sanitize_key((string) ($rule['id'] ?? ''));
            $query = sanitize_text_field((string) ($rule['query'] ?? ''));
            $target = sanitize_title((string) ($rule['target_term_slug'] ?? ''));
            if ($id === '' || $query === '' || $target === '') { continue; }
            $categories = array();
            foreach ((array) ($rule['category_ids'] ?? array()) as $category_id) {
                $category_id = preg_replace('/\D+/', '', (string) $category_id);
                if ($category_id !== '') { $categories[$category_id] = $category_id; }
            }
            $safe[$id] = array(
                'id' => substr($id, 0, 80),
                'label' => substr(sanitize_text_field((string) ($rule['label'] ?? $id)), 0, 120),
                'query' => substr($query, 0, 100),
                'target_term_slug' => substr($target, 0, 120),
                'category_ids' => array_values(array_slice($categories, 0, 5)),
                'active' => !empty($rule['active']),
                'private' => !empty($rule['private']),
                'business' => !empty($rule['business']),
            );
            if (count($safe) >= 50) { break; }
        }
        return array_values($safe);
    }

    /**
     * Current seller-route enablement is a hard mutation boundary. A disabled
     * route may remain stored for historical/public-freshness purposes, but
     * maintenance, refresh and selection must never mutate it until re-enabled.
     */
    private function ebay_route_enabled($seller_type, $settings = null) {
        $settings = is_array($settings) ? $settings : $this->ebay_settings();
        $seller_type = strtoupper(sanitize_key((string)$seller_type));
        $private_enabled = array_key_exists('private_enabled',$settings) ? !empty($settings['private_enabled']) : true;
        $business_enabled = array_key_exists('business_enabled',$settings) ? !empty($settings['business_enabled']) : true;
        if ($seller_type === 'INDIVIDUAL') { return $private_enabled; }
        if ($seller_type === 'BUSINESS') { return $business_enabled; }
        return false;
    }

    private function ebay_selection_scope_for_enabled_routes($scope, $settings = null) {
        $settings = is_array($settings) ? $settings : $this->ebay_settings();
        $scope = sanitize_key((string)$scope);
        if (!in_array($scope, array('all','private','business'), true)) { return ''; }
        $private = array_key_exists('private_enabled',$settings) ? !empty($settings['private_enabled']) : true;
        $business = array_key_exists('business_enabled',$settings) ? !empty($settings['business_enabled']) : true;
        if ($scope === 'private') { return $private ? 'private' : ''; }
        if ($scope === 'business') { return $business ? 'business' : ''; }
        if ($private && $business) { return 'all'; }
        if ($private) { return 'private'; }
        if ($business) { return 'business'; }
        return '';
    }

    /** SQL for source-refresh candidates, built only from currently enabled routes. */
    private function ebay_refresh_enabled_route_sql($settings = null, $alias = 'e') {
        $settings = is_array($settings) ? $settings : $this->ebay_settings();
        $column = $alias === '' ? 'seller_account_type' : $alias . '.seller_account_type';
        $parts = array();
        $private_enabled = array_key_exists('private_enabled',$settings) ? !empty($settings['private_enabled']) : true;
        $business_enabled = array_key_exists('business_enabled',$settings) ? !empty($settings['business_enabled']) : true;
        if ($private_enabled) { $parts[] = "{$column}='INDIVIDUAL'"; }
        if ($business_enabled) { $parts[] = "({$column}='BUSINESS' AND COALESCE(" . ($alias === '' ? '' : $alias . '.') . "output_state,'') IN ('creative_ready','stale_wait_refresh'))"; }
        return $parts ? '(' . implode(' OR ', $parts) . ')' : '(1=0)';
    }

    private function ebay_configuration_errors($settings = null) {
        $settings = is_array($settings) ? $settings : $this->ebay_settings();
        $errors = array();
        if (empty($settings['client_id'])) { $errors[] = 'eBay Client-ID fehlt.'; }
        if (empty($settings['client_secret'])) { $errors[] = 'eBay Client-Secret fehlt.'; }
        if (!preg_match('/^\d{10}$/', (string) ($settings['epn_campaign_id'] ?? ''))) { $errors[] = 'EPN-Campaign-ID muss exakt 10 Ziffern haben.'; }
        if ((string) ($settings['marketplace_id'] ?? '') !== 'EBAY_DE') { $errors[] = 'Das aktuelle eBay-Modul unterstützt ausschließlich EBAY_DE.'; }
        if (empty($settings['rules'])) { $errors[] = 'Mindestens eine gültige eBay-Regel fehlt.'; }
        $catalog = $this->ebay_catalog_integrity();
        if (is_wp_error($catalog)) { $errors[] = $catalog->get_error_message(); }
        elseif (empty($settings['catalog_verified_at']) || !hash_equals((string) ($catalog['source_sha256'] ?? ''), (string) ($settings['catalog_verified_sha256'] ?? ''))) {
            $errors[] = 'Portal- und Themenabgleich wurde für den aktuellen Katalog noch nicht bestätigt.';
        }
        if (empty($settings['private_enabled']) && empty($settings['business_enabled'])) { $errors[] = 'Mindestens eine Verkäuferroute muss aktiviert sein.'; }
        if (empty($settings['api_terms_confirmed'])) { $errors[] = 'Bestätigung der eBay-API-/EPN-Verträge fehlt.'; }
        if (empty($settings['privacy_policy_confirmed'])) { $errors[] = 'Bestätigung der Datenschutz-/Affiliate-Hinweise fehlt.'; }
        if ((string) ($settings['environment'] ?? 'production') === 'production') {
            if (!method_exists($this, 'ebay_deletion_compliance_snapshot')) {
                $errors[] = 'eBay Marketplace Account Deletion/Closure Compliance-Modul fehlt.';
            } else {
                $compliance = $this->ebay_deletion_compliance_snapshot();
                if (empty($compliance['https'])) { $errors[] = 'eBay Notification Endpoint ist nicht per HTTPS erreichbar konfiguriert.'; }
                if (empty($compliance['challenge_answered'])) { $errors[] = 'eBay Marketplace Account Deletion/Closure Challenge wurde noch nicht beantwortet.'; }
                if (empty($compliance['signed_notification_verified'])) { $errors[] = 'Noch keine signierte eBay Marketplace Account Deletion/Closure Testbenachrichtigung erfolgreich verifiziert.'; }
            }
        }
        if (!empty($settings['private_enabled']) && absint($settings['private_root_term_id'] ?? 0) <= 0) { $errors[] = 'HivePress-Bereich „Private Anzeigen“ ist nicht eingerichtet.'; }
        return $errors;
    }

    public function maybe_install_ebay_schema() {
        $installed = (string) get_option(self::OPTION_EBAY_SCHEMA_VERSION, '0');
        if ($installed === self::EBAY_SCHEMA_VERSION) { return; }
        require_once ABSPATH . 'wp-admin/includes/upgrade.php';
        global $wpdb;
        $table = $this->ebay_items_table();
        $charset = $wpdb->get_charset_collate();
        dbDelta("CREATE TABLE {$table} (
            id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
            portal_key varchar(191) NOT NULL,
            item_id varchar(191) NOT NULL,
            legacy_item_id varchar(80) NOT NULL DEFAULT '',
            seller_account_type varchar(20) NOT NULL,
            seller_username varchar(191) NOT NULL DEFAULT '',
            route_mode varchar(40) NOT NULL,
            rule_id varchar(80) NOT NULL,
            target_term_id bigint(20) unsigned NOT NULL DEFAULT 0,
            listing_post_id bigint(20) unsigned NOT NULL DEFAULT 0,
            creative_identity_hash char(64) NOT NULL DEFAULT '',
            title text NOT NULL,
            short_description longtext NULL,
            condition_text text NOT NULL,
            price_value varchar(60) NOT NULL DEFAULT '',
            currency varchar(10) NOT NULL DEFAULT '',
            shipping_value varchar(60) NOT NULL DEFAULT '',
            location_text text NOT NULL,
            affiliate_url text NOT NULL,
            item_web_url text NOT NULL,
            image_url text NOT NULL,
            item_end_at bigint(20) unsigned NOT NULL DEFAULT 0,
            source_hash char(64) NOT NULL,
            source_payload longtext NULL,
            status varchar(30) NOT NULL DEFAULT 'active',
            source_state varchar(24) NOT NULL DEFAULT 'available',
            policy_state varchar(24) NOT NULL DEFAULT 'pending',
            route_state varchar(24) NOT NULL DEFAULT 'pending',
            output_state varchar(24) NOT NULL DEFAULT 'none',
            policy_version varchar(32) NOT NULL DEFAULT '',
            classifier_version varchar(32) NOT NULL DEFAULT '',
            source_checked_at bigint(20) unsigned NOT NULL DEFAULT 0,
            rejection_reason text NOT NULL,
            last_seen bigint(20) unsigned NOT NULL DEFAULT 0,
            fresh_until bigint(20) unsigned NOT NULL DEFAULT 0,
            created_at bigint(20) unsigned NOT NULL DEFAULT 0,
            updated_at bigint(20) unsigned NOT NULL DEFAULT 0,
            PRIMARY KEY  (id),
            UNIQUE KEY portal_item (portal_key(100), item_id(100)),
            KEY seller_status (seller_account_type, status),
            KEY business_concept (seller_account_type, rule_id, source_state, policy_state, route_state, last_seen),
            KEY private_capacity (seller_account_type, source_state, policy_state, route_state, target_term_id, last_seen),
            KEY route_status (route_mode, status),
            KEY workflow_source (source_state, source_checked_at),
            KEY workflow_policy (policy_state, policy_version),
            KEY workflow_route (route_state, classifier_version),
            KEY fresh_until (fresh_until),
            KEY listing_post_id (listing_post_id),
            KEY creative_hash (creative_identity_hash)
        ) {$charset};");
        update_option(self::OPTION_EBAY_SCHEMA_VERSION, self::EBAY_SCHEMA_VERSION, false);
    }

    public function ebay_cron_schedules($schedules) {
        if (!isset($schedules['ppar_three_hours'])) {
            $schedules['ppar_three_hours'] = array('interval'=>3 * HOUR_IN_SECONDS, 'display'=>'Alle drei Stunden');
        }
        return $schedules;
    }

    /** V6.54: eBay discovery/refresh/canonical continuation is driven solely by
     * the provider-neutral external heartbeat. Retire every old recurring/single
     * eBay transport hook so host cron behaviour can no longer affect correctness. */
    public function retire_ebay_legacy_cron_transport() {
        if (!function_exists('wp_clear_scheduled_hook')) { return; }
        $hooks=array(self::EBAY_CRON_HOOK,self::EBAY_REFRESH_CRON_HOOK,self::EBAY_REFRESH_WORKER_HOOK,self::EBAY_WORKER_HOOK);
        foreach($hooks as $hook){
            if (!function_exists('wp_next_scheduled') || wp_next_scheduled($hook)) { wp_clear_scheduled_hook($hook); }
        }
    }

    public function ensure_ebay_schedule() { $this->retire_ebay_legacy_cron_transport(); }
    public function reschedule_ebay_cron($force = false) { $this->retire_ebay_legacy_cron_transport(); }
    public function ensure_ebay_refresh_schedule() { $this->retire_ebay_legacy_cron_transport(); }
    public function reschedule_ebay_refresh_cron($force = false) { $this->retire_ebay_legacy_cron_transport(); }

    public function ensure_ebay_maintenance_schedule() {
        // V6.40 controlled ownership: maintenance has no independent cron owner.
        // Refresh is the sole hourly mutation owner and embeds bounded maintenance.
        // This compatibility cleanup only retires a schedule left by older builds.
        if (!function_exists('wp_next_scheduled')) { return; }
        $scheduled = wp_next_scheduled(self::EBAY_MAINTENANCE_CRON_HOOK);
        if ($scheduled && function_exists('wp_clear_scheduled_hook')) {
            wp_clear_scheduled_hook(self::EBAY_MAINTENANCE_CRON_HOOK);
        }
    }

    public function reschedule_ebay_maintenance_cron($force = false) {
        if ($force && function_exists('wp_clear_scheduled_hook')) { wp_clear_scheduled_hook(self::EBAY_MAINTENANCE_CRON_HOOK); }
        $this->ensure_ebay_maintenance_schedule();
    }

    /**
     * V6.12 one-time legacy-media cleanup. This is a separate bounded job so an
     * installation/update request never tries to delete thousands of attachments.
     */
    public function ensure_ebay_media_cleanup_schedule() {
        if (!function_exists('wp_next_scheduled') || !function_exists('wp_schedule_single_event')) { return; }
        $state = get_option(self::OPTION_EBAY_MEDIA_CLEANUP_STATE, array());
        $state = is_array($state) ? $state : array();
        $complete = (string) ($state['version'] ?? '') === self::EBAY_MEDIA_CLEANUP_VERSION
            && (string) ($state['status'] ?? '') === 'complete';
        if ($complete) { return; }
        if (!wp_next_scheduled(self::EBAY_MEDIA_CLEANUP_HOOK)) {
            // V6.20: legacy file deletion is deliberately low-priority. A 4s
            // cleanup every 15s competed with normal page/AJAX requests and the
            // eBay discovery worker on smaller hosting pools.
            wp_schedule_single_event(time() + 120, self::EBAY_MEDIA_CLEANUP_HOOK);
        }
    }

    public function reschedule_ebay_media_cleanup($force = false) {
        if ($force && function_exists('wp_clear_scheduled_hook')) { wp_clear_scheduled_hook(self::EBAY_MEDIA_CLEANUP_HOOK); }
        $this->ensure_ebay_media_cleanup_schedule();
    }

    /**
     * V6.22 upgrade recovery: a V6.19/V6.20 timeout or delayed Cron may have
     * left >250 PRIVATE listings published. This method performs no inventory
     * work in the page/AJAX request; it only queues/dispatches the bounded worker.
     */
    /**
     * One-time state retirement for the failed V6.40 browser/upgrade recovery
     * architecture. This is deliberately STATE-ONLY: no source row, listing,
     * campaign, taxonomy or selection plan is created/changed here.
     *
     * It prevents an already-open V6.40 recovery from surviving a source update
     * and immediately continuing the same PRIVATE loop before an operator starts
     * a new controlled job explicitly or the regular schedules do so.
     */
    public function maybe_retire_deprecated_ebay_recovery_transports() {
        $marker_key = 'ppar_ebay_controlled_rebuild_transport_retired_20260812';
        $contract_marker_key = 'ppar_ebay_controlled_rebuild_transport_retired_contract_v1';
        // One architecture retirement, never one retirement per patch build.
        // Existing V6.40.3+ markers mean the migration already ran; adopt the
        // stable marker without touching any current run/cursor/selection owner.
        if ((string)get_option($contract_marker_key, '') === 'done') { return; }
        $legacy_marker = (string)get_option($marker_key, '');
        if ($legacy_marker !== '' && $this->ebay_known_patch_state_build($legacy_marker)) {
            update_option($contract_marker_key, 'done', false);
            return;
        }
        $now = time();

        $selection = $this->ebay_selection_state_load();
        if ($this->ebay_selection_state_is_open($selection)) {
            $selection['status'] = 'failed';
            $selection['phase'] = 'retired';
            $selection['failed_at'] = $now;
            $selection['completed_at'] = $now;
            $selection['failure_reason'] = 'failed_v640_recovery_state_retired';
            $selection['error'] = 'Alter V6.40-Recovery-State wurde ohne Bestandsmutation beendet.';
            $selection['retired_by_build'] = (string)self::EBAY_RUNTIME_BUILD;
            $this->ebay_selection_state_save($selection);
        }

        // IMPORTANT: stale jobs are, by definition, runtime-INcompatible.
        // Therefore the compatibility-aware *_is_open() helpers cannot be used
        // to discover them here; doing so made the old-build retirement branch
        // unreachable. Inspect the raw lifecycle status first, then fail only
        // incompatible queued/running jobs. A valid current-build job is kept.
        $sync = $this->ebay_sync_job_load();
        $sync_status = sanitize_key((string)($sync['status'] ?? ''));
        if (in_array($sync_status, array('queued','running'), true)
            && !$this->ebay_sync_job_runtime_compatible($sync)) {
            $sync['status'] = 'failed';
            $sync['worker_phase'] = 'retired';
            $sync['finished_at'] = $now;
            $sync['failure_reason'] = 'failed_v640_runtime_retired';
            $this->ebay_sync_job_save($sync);
        }
        $refresh = $this->ebay_refresh_job_load();
        $refresh_status = sanitize_key((string)($refresh['status'] ?? ''));
        if (in_array($refresh_status, array('queued','running'), true)
            && !$this->ebay_refresh_job_runtime_compatible($refresh)) {
            $refresh['status'] = 'failed';
            $refresh['finished_at'] = $now;
            $refresh['failure_reason'] = 'failed_v640_runtime_retired';
            $this->ebay_refresh_job_save($refresh);
        }
        $local_business = $this->ebay_business_local_recovery_state_load();
        if (sanitize_key((string)($local_business['status'] ?? '')) === 'running') {
            $local_business['status'] = 'failed';
            $local_business['phase'] = 'retired';
            $local_business['failed_at'] = $now;
            $local_business['failure_reason'] = 'browser_recovery_transport_retired';
            $this->ebay_business_local_recovery_state_save($local_business);
        }

        // If no valid discovery job owns the shared worker hook, remove stale
        // single events left by the failed selection loop. Regular 3h discovery
        // remains scheduled via EBAY_CRON_HOOK and will create fresh state itself.
        $sync = $this->ebay_sync_job_load();
        if (!$this->ebay_sync_job_is_open($sync) && function_exists('wp_clear_scheduled_hook')) {
            wp_clear_scheduled_hook(self::EBAY_WORKER_HOOK);
        }
        foreach (array(
            'ppar_ebay_selection_worker_lock_',
            'ppar_ebay_sync_worker_lock_',
        ) as $prefix) {
            if (function_exists('delete_transient')) {
                delete_transient($prefix . substr(hash('sha256', (string)self::EBAY_RUNTIME_BUILD), 0, 12));
            }
        }
        update_option($marker_key, (string)self::EBAY_RUNTIME_BUILD, false);
        update_option($contract_marker_key, 'done', false);
    }

    /**
     * Deprecated compatibility method. It MUST remain a no-op. A WordPress page
     * request is never allowed to infer drift and start/continue recovery.
     */
    public function ensure_ebay_selection_recovery_schedule() {
        return $this->ebay_selection_state_load();
    }

    /**
     * Only the private eBay importer ever writes both legacy markers below.
     * A valid eBay-hosted source URL plus that marker pair is therefore the
     * ownership proof. Existing non-eBay/user attachments are never candidates.
     */
    private function ebay_legacy_attachment_cleanup_context($attachment_id) {
        $attachment_id = absint($attachment_id);
        if ($attachment_id <= 0 || !function_exists('get_post')) {
            return new WP_Error('ebay_media_cleanup_attachment_missing', 'Attachment fehlt.');
        }
        $attachment = get_post($attachment_id);
        if (!is_object($attachment) || (string) ($attachment->post_type ?? '') !== 'attachment') {
            return new WP_Error('ebay_media_cleanup_not_attachment', 'Objekt ist kein Attachment.');
        }
        $item_id = sanitize_text_field((string) get_post_meta($attachment_id, '_ppar_ebay_item_id', true));
        $source_url = $this->ebay_remote_image_url_validate((string) get_post_meta($attachment_id, '_ppar_ebay_source_url', true));
        if ($item_id === '' || $source_url === '') {
            return new WP_Error('ebay_media_cleanup_ownership_unproven', 'eBay-Bildeigentum ist nicht eindeutig nachweisbar.');
        }
        $listing_id = absint($attachment->post_parent ?? 0);
        if ($listing_id > 0) {
            $parent = get_post($listing_id);
            if (is_object($parent)) {
                if ((string) ($parent->post_type ?? '') !== 'hp_listing') {
                    return new WP_Error('ebay_media_cleanup_parent_invalid', 'Attachment gehört keinem HivePress-Listing.');
                }
                $parent_item_id = sanitize_text_field((string) get_post_meta($listing_id, '_ppar_ebay_item_id', true));
                if ($parent_item_id === '' || $parent_item_id !== $item_id) {
                    return new WP_Error('ebay_media_cleanup_item_mismatch', 'Attachment- und Listing-eBay-ID stimmen nicht überein.');
                }
            } else {
                // Orphaned attachment from a deleted importer listing. The two
                // plugin markers and eBay host still prove importer ownership.
                $listing_id = 0;
            }
        }
        return array('attachment_id'=>$attachment_id, 'listing_id'=>$listing_id, 'item_id'=>$item_id, 'source_url'=>$source_url);
    }

    public function run_ebay_media_cleanup_worker($limit = 20) {
        $limit = max(1, min(20, absint($limit)));
        $started = microtime(true);
        $state = get_option(self::OPTION_EBAY_MEDIA_CLEANUP_STATE, array());
        $state = is_array($state) ? $state : array();
        if ((string) ($state['version'] ?? '') !== self::EBAY_MEDIA_CLEANUP_VERSION) {
            $state = array(
                'version'=>self::EBAY_MEDIA_CLEANUP_VERSION, 'status'=>'running', 'cursor'=>0,
                'scanned'=>0, 'deleted'=>0, 'skipped'=>0, 'failed'=>0,
                'started_at'=>time(), 'updated_at'=>time(), 'completed_at'=>0,
            );
        }
        $state['status'] = 'running';

        // Never compete with discovery, inventory refresh or the bounded
        // selection/cap worker. Media cleanup can wait; public requests cannot.
        // Read the worker state directly here instead of calling the full job
        // loaders. That keeps cleanup independent from sync/refresh runtime
        // constants and makes the media contract testable in isolation.
        $sync_const = static::class . '::OPTION_EBAY_SYNC_JOB';
        $refresh_const = static::class . '::OPTION_EBAY_REFRESH_JOB';
        $sync_key = defined($sync_const) ? (string) constant($sync_const) : 'ppar_ebay_sync_job_v1';
        $refresh_key = defined($refresh_const) ? (string) constant($refresh_const) : 'ppar_ebay_refresh_job_v1';
        $sync_job = get_option($sync_key, array());
        $refresh_job = get_option($refresh_key, array());
        $selection = get_option($this->ebay_selection_option_key(), array());
        $sync_job = is_array($sync_job) ? $sync_job : array();
        $refresh_job = is_array($refresh_job) ? $refresh_job : array();
        $selection = is_array($selection) ? $selection : array();
        $runtime_const = static::class . '::EBAY_RUNTIME_BUILD';
        $current_build = defined($runtime_const) ? (string) constant($runtime_const) : '';
        $sync_open = in_array(sanitize_key((string)($sync_job['status'] ?? '')), array('queued','running'), true);
        $refresh_open = in_array(sanitize_key((string)($refresh_job['status'] ?? '')), array('queued','running'), true);
        // A timed-out job from an older plugin build must not block media cleanup
        // forever after upgrade. Only a current-build open job owns the worker.
        if ($sync_open && $current_build !== '' && (string)($sync_job['build'] ?? '') !== '' && !hash_equals($current_build, (string)$sync_job['build'])) { $sync_open = false; }
        if ($refresh_open && $current_build !== '' && (string)($refresh_job['build'] ?? '') !== '' && !hash_equals($current_build, (string)$refresh_job['build'])) { $refresh_open = false; }
        $busy = $sync_open || $refresh_open
            || in_array(sanitize_key((string)($selection['status'] ?? '')), array('pending','preparing','running'), true);
        if ($busy) {
            $state['status'] = 'deferred_busy';
            $state['updated_at'] = time();
            update_option(self::OPTION_EBAY_MEDIA_CLEANUP_STATE, $state, false);
            if (function_exists('wp_schedule_single_event') && function_exists('wp_next_scheduled') && !wp_next_scheduled(self::EBAY_MEDIA_CLEANUP_HOOK)) {
                wp_schedule_single_event(time() + 180, self::EBAY_MEDIA_CLEANUP_HOOK);
            }
            return $state;
        }

        global $wpdb;
        if (!is_object($wpdb) || empty($wpdb->posts) || empty($wpdb->postmeta) || !method_exists($wpdb, 'prepare') || !method_exists($wpdb, 'get_col')) {
            $state['status'] = 'deferred'; $state['updated_at'] = time();
            update_option(self::OPTION_EBAY_MEDIA_CLEANUP_STATE, $state, false);
            $this->ensure_ebay_media_cleanup_schedule();
            return $state;
        }
        $cursor = absint($state['cursor'] ?? 0);
        $ids = (array) $wpdb->get_col($wpdb->prepare(
            "SELECT DISTINCT p.ID FROM {$wpdb->posts} p INNER JOIN {$wpdb->postmeta} m ON m.post_id=p.ID AND m.meta_key='_ppar_ebay_item_id' WHERE p.post_type='attachment' AND p.ID>%d AND m.meta_value<>'' ORDER BY p.ID ASC LIMIT %d",
            $cursor, $limit
        ));
        if (!$ids) {
            $state['status'] = 'complete'; $state['updated_at'] = time(); $state['completed_at'] = time();
            update_option(self::OPTION_EBAY_MEDIA_CLEANUP_STATE, $state, false);
            return $state;
        }

        foreach ($ids as $attachment_id) {
            if ((microtime(true) - $started) >= 1.25) { break; }
            $attachment_id = absint($attachment_id);
            if ($attachment_id <= 0) { continue; }
            $state['cursor'] = max(absint($state['cursor'] ?? 0), $attachment_id);
            $state['scanned'] = absint($state['scanned'] ?? 0) + 1;
            $context = $this->ebay_legacy_attachment_cleanup_context($attachment_id);
            if (is_wp_error($context)) {
                $state['skipped'] = absint($state['skipped'] ?? 0) + 1;
                continue;
            }
            $listing_id = absint($context['listing_id'] ?? 0);
            $source_url = (string) ($context['source_url'] ?? '');
            if ($listing_id > 0) {
                $existing_remote = $this->ebay_remote_image_url_validate((string) get_post_meta($listing_id, '_ppar_ebay_remote_image_url', true));
                if ($existing_remote === '') {
                    update_post_meta($listing_id, '_ppar_ebay_remote_image_url', $source_url);
                    update_post_meta($listing_id, '_ppar_ebay_remote_image_mode', 'remote_only_v1');
                }
                if (function_exists('get_post_thumbnail_id') && absint(get_post_thumbnail_id($listing_id)) === $attachment_id && function_exists('delete_post_thumbnail')) {
                    delete_post_thumbnail($listing_id);
                }
            }
            if (!function_exists('wp_delete_attachment') || !wp_delete_attachment($attachment_id, true)) {
                $state['failed'] = absint($state['failed'] ?? 0) + 1;
                continue;
            }
            $state['deleted'] = absint($state['deleted'] ?? 0) + 1;
        }
        $state['updated_at'] = time();
        update_option(self::OPTION_EBAY_MEDIA_CLEANUP_STATE, $state, false);
        if (function_exists('wp_schedule_single_event') && function_exists('wp_next_scheduled') && !wp_next_scheduled(self::EBAY_MEDIA_CLEANUP_HOOK)) {
            wp_schedule_single_event(time() + 120, self::EBAY_MEDIA_CLEANUP_HOOK);
        }
        return $state;
    }

    private function ebay_maintenance_state_load() {
        if (method_exists($this, 'ebay_run_load') && (string)(($this->ebay_run_load())['schema'] ?? '') === '1.0') {
            $state=$this->ebay_run_phase_state_load('maintenance');
            return is_array($state)?$state:array();
        }
        $state=get_option(self::OPTION_EBAY_MAINTENANCE_STATE,array());
        return is_array($state)?$state:array();
    }

    private function ebay_maintenance_state_save($state) {
        $state=is_array($state)?$state:array();$state['updated_at']=time();
        if (method_exists($this, 'ebay_run_load') && (string)(($this->ebay_run_load())['schema'] ?? '') === '1.0') {
            $this->ebay_run_phase_state_save('maintenance',$state);
        } else {
            update_option(self::OPTION_EBAY_MAINTENANCE_STATE, $state, false);
        }
        return $state;
    }

    private function ebay_maintenance_state_is_current($state = null) {
        if (!is_array($state)) {
            $state = $this->ebay_maintenance_state_load();
        }
        $state = is_array($state) ? $state : array();
        return absint($state['completed_at'] ?? 0) > 0
            && (string) ($state['policy_version'] ?? '') === self::EBAY_CONTENT_POLICY_VERSION
            && (string) ($state['private_classifier_version'] ?? '') === self::EBAY_PRIVATE_CLASSIFIER_VERSION
            && (string) ($state['business_classifier_version'] ?? '') === self::EBAY_BUSINESS_CLASSIFIER_VERSION;
    }

    private function ebay_maintenance_classifier_version($seller_type) {
        return strtoupper(sanitize_key((string)$seller_type))==='INDIVIDUAL' ? self::EBAY_PRIVATE_CLASSIFIER_VERSION : self::EBAY_BUSINESS_CLASSIFIER_VERSION;
    }

    /** Keep PRIVATE route state independent from WordPress post_status. */
    private function ebay_private_listing_route_meta($row, $state, $reason = '') {
        $row = is_array($row) ? $row : array();
        $listing_id = absint($row['listing_post_id'] ?? 0);
        if ($listing_id <= 0 || !function_exists('update_post_meta')) { return; }
        $state = sanitize_key((string) $state);
        if ($state === '') { $state = 'review'; }
        update_post_meta($listing_id, '_ppar_ebay_lifecycle_state', $state);
        if ($reason !== '') { update_post_meta($listing_id, '_ppar_ebay_route_reason', sanitize_text_field((string) $reason)); }
        elseif (function_exists('delete_post_meta')) { delete_post_meta($listing_id, '_ppar_ebay_route_reason'); }
        if ($state === 'active' && function_exists('delete_post_meta')) {
            delete_post_meta($listing_id, '_ppar_ebay_route_review');
        }
    }

    /**
     * Eine lokale Klassifikator-Aenderung oder ein ueberfaelliger Refresh darf
     * einen bereits veroeffentlichten PRIVATE-Last-Known-Good-Bestand nicht allein
     * aus dem Frontend entfernen. Das letzte gueltige Ziel bleibt sichtbar,
     * waehrend die neue Route separat auf Review markiert wird. Harte Policy-,
     * Veto- oder eBay-Endsignale laufen NICHT durch diesen Pfad.
     */
    private function ebay_private_can_preserve_last_good_route($row) {
        $row = is_array($row) ? $row : array();
        $listing_id = absint($row['listing_post_id'] ?? 0);
        $target_term_id = absint($row['target_term_id'] ?? 0);
        if ($listing_id <= 0 || $target_term_id <= 0) { return false; }
        if (sanitize_key((string)($row['source_state'] ?? 'available')) === 'ended') { return false; }
        // Frische steuert ausschliesslich den naechsten getItem-Refresh. Ein
        // ueberfaelliger Refresh ist KEIN Endsignal und darf Last-Known-Good
        // nicht ausblenden.
        $end_at = absint($row['item_end_at'] ?? 0);
        if ($end_at > 0 && $end_at <= time()) { return false; }
        if (!function_exists('get_post_status') || (string)get_post_status($listing_id) !== 'publish') { return false; }
        return true;
    }

    private function ebay_private_preserve_last_good_route_on_soft_review($row, $error) {
        if (!$this->ebay_private_can_preserve_last_good_route($row)) { return false; }
        global $wpdb;
        $code=is_wp_error($error)?sanitize_key((string)$error->get_error_code()):'ebay_private_route_review';
        $message=is_wp_error($error)?sanitize_text_field($error->get_error_message()):sanitize_text_field((string)$error);
        $wpdb->update($this->ebay_items_table(),array(
            'policy_state'=>'allowed','route_state'=>'review_last_good','policy_version'=>self::EBAY_CONTENT_POLICY_VERSION,
            'classifier_version'=>self::EBAY_PRIVATE_CLASSIFIER_VERSION,
            'rejection_reason'=>'['.$code.'] '.$message,'updated_at'=>time(),
        ),array('id'=>absint($row['id']??0)));
        $listing_id=absint($row['listing_post_id']??0);
        if ($listing_id>0 && function_exists('update_post_meta')) {
            update_post_meta($listing_id,'_ppar_ebay_lifecycle_state','active');
            update_post_meta($listing_id,'_ppar_ebay_route_review',1);
            update_post_meta($listing_id,'_ppar_ebay_route_reason',$message);
        }
        return true;
    }

    /** BUSINESS Last-Known-Good may survive only soft routing uncertainty. */
    private function ebay_business_can_preserve_last_good_output($row) {
        $row = is_array($row) ? $row : array();
        $hash = strtolower(sanitize_text_field((string)($row['creative_identity_hash'] ?? '')));
        if (!preg_match('/^[a-f0-9]{64}$/', $hash)) { return false; }
        if (sanitize_key((string)($row['source_state'] ?? 'available')) === 'ended') { return false; }
        if (sanitize_key((string)($row['policy_state'] ?? 'allowed')) === 'blocked') { return false; }
        if ($this->ebay_public_content_policy_reason_from_source_row($row, (string)($row['title'] ?? '')) !== '') { return false; }
        $end_at = absint($row['item_end_at'] ?? 0);
        if ($end_at > 0 && $end_at <= time()) { return false; }
        if (!method_exists($this, 'get_campaigns')) { return false; }
        foreach ((array)$this->get_campaigns() as $campaign) {
            if (!is_array($campaign) || sanitize_key((string)($campaign['network'] ?? '')) !== 'ebay' || sanitize_key((string)($campaign['creative_type'] ?? '')) !== 'product') { continue; }
            $post_id = absint($campaign['post_id'] ?? 0);
            if ($post_id <= 0 || !function_exists('get_post_meta')) { continue; }
            if (absint(get_post_meta($post_id, '_ppar_ebay_business_auto', true)) !== 1) { continue; }
            $campaign_hash = strtolower(sanitize_text_field((string)get_post_meta($post_id, '_ppar_creative_identity_hash', true)));
            if ($campaign_hash === $hash) { return true; }
        }
        return false;
    }

    private function ebay_business_preserve_last_good_on_soft_review($row, $error) {
        if (!$this->ebay_business_can_preserve_last_good_output($row)) { return false; }
        global $wpdb;
        $code=is_wp_error($error)?sanitize_key((string)$error->get_error_code()):'ebay_business_route_review';
        $message=is_wp_error($error)?sanitize_text_field($error->get_error_message()):sanitize_text_field((string)$error);
        $wpdb->update($this->ebay_items_table(),array(
            'policy_state'=>'allowed','route_state'=>'review_last_good','policy_version'=>self::EBAY_CONTENT_POLICY_VERSION,
            'rejection_reason'=>'['.$code.'] '.$message,'updated_at'=>time(),
        ),array('id'=>absint($row['id']??0)));
        return true;
    }

    private function ebay_maintenance_set_review_state($row, $seller_type, $error) {
        global $wpdb;
        $code=is_wp_error($error)?sanitize_key((string)$error->get_error_code()):'ebay_route_review';
        $message=is_wp_error($error)?sanitize_text_field($error->get_error_message()):sanitize_text_field((string)$error);
        $wpdb->update($this->ebay_items_table(),array(
            'policy_state'=>'allowed','route_state'=>'review','policy_version'=>self::EBAY_CONTENT_POLICY_VERSION,
            'classifier_version'=>$this->ebay_maintenance_classifier_version($seller_type),
            'rejection_reason'=>'['.$code.'] '.$message,'updated_at'=>time(),
        ),array('id'=>absint($row['id']??0)));
        if (strtoupper(sanitize_key((string)$seller_type)) === 'INDIVIDUAL') {
            $this->ebay_private_listing_route_meta($row, 'review', $message);
        }
    }

    /**
     * V6.9: V6.8 increased the PRIVATE classifier marker from 3.0 to 4.0 even
     * though the PRIVATE classification semantics themselves did not change.
     * Treat that transition as metadata-only. Otherwise every previously valid
     * PRIVATE source row is unnecessarily reclassified/rematerialized on the
     * next manual inventory reconciliation. The update is intentionally limited
     * to the exact 3.0 -> current marker transition; older/unknown contracts stay
     * stale and continue through the normal maintenance classifier.
     */
    private function ebay_migrate_private_classifier_marker_v690() {
        global $wpdb;
        if (!is_object($wpdb) || !method_exists($wpdb, 'query') || !method_exists($wpdb, 'prepare')) { return 0; }
        $table = $this->ebay_items_table();
        $changed = $wpdb->query($wpdb->prepare(
            "UPDATE {$table} SET classifier_version=%s WHERE seller_account_type='INDIVIDUAL' AND classifier_version=%s",
            self::EBAY_PRIVATE_CLASSIFIER_VERSION,
            '3.0'
        ));
        $state = $this->ebay_maintenance_state_load();
        $state = is_array($state) ? $state : array();
        if ((string)($state['private_classifier_version'] ?? '') === '3.0') {
            $state['private_classifier_version'] = self::EBAY_PRIVATE_CLASSIFIER_VERSION;
            $this->ebay_maintenance_state_save($state);
        }
        return max(0, (int)$changed);
    }

    /**
     * Workflow-V2 maintenance is scheduled work, never an admin-page side effect.
     * It re-evaluates only rows whose independent policy/classifier contract is stale.
     * Local reclassification never refreshes source freshness timestamps.
     */
    public function run_ebay_maintenance_v2($limit = 1200, $force_business_reconcile = false, $time_budget_seconds = 12, $allow_during_refresh = false) {
        $this->maybe_install_ebay_schema();
        // Lifecycle mutual exclusion: standalone maintenance never races a sync,
        // refresh or selection owner. The refresh worker may explicitly embed its
        // bounded local reconciliation by passing $allow_during_refresh=true.
        $sync_guard=$this->ebay_sync_job_load();
        $refresh_guard=$this->ebay_refresh_job_load();
        $selection_guard=$this->ebay_selection_state_load();
        if($this->ebay_sync_job_is_open($sync_guard) || $this->ebay_selection_state_is_open($selection_guard) || (!$allow_during_refresh && $this->ebay_refresh_job_is_open($refresh_guard))){
            return array('status'=>'deferred_busy','scanned'=>0,'ready_private'=>0,'ready_business'=>0,'review'=>0,'blocked'=>0,'errors'=>0);
        }
        global $wpdb;
        $table=$this->ebay_items_table();
        $limit=max(1,min(2000,absint($limit)));
        $settings=$this->ebay_settings();
        if (empty($settings['private_enabled']) && empty($settings['business_enabled'])) {
            return array('status'=>'disabled_routes','scanned'=>0,'ready_private'=>0,'ready_business'=>0,'review'=>0,'blocked'=>0,'errors'=>0);
        }
        // Publication recovery is not a classifier migration. A disabled PRIVATE
        // route is a hard mutation boundary, so even this marker-only migration
        // is skipped until PRIVATE is explicitly re-enabled.
        if(!empty($settings['private_enabled'])){$this->ebay_migrate_private_classifier_marker_v690();}
        $state=$this->ebay_maintenance_state_load();
        $state=is_array($state)?$state:array();
        // A contract change invalidates every previous maintenance cursor. Otherwise
        // a half-finished old contract could skip low IDs under the new classifier.
        $contract_changed = (string)($state['policy_version']??'') !== self::EBAY_CONTENT_POLICY_VERSION
            || (!empty($settings['private_enabled']) && (string)($state['private_classifier_version']??'') !== self::EBAY_PRIVATE_CLASSIFIER_VERSION)
            || (!empty($settings['business_enabled']) && (string)($state['business_classifier_version']??'') !== self::EBAY_BUSINESS_CLASSIFIER_VERSION);
        if ($contract_changed) {
            $state['cursor']=0;
            $state['completed_at']=0;
            $state['cycle_stats']=array('scanned'=>0,'ready_private'=>0,'ready_business'=>0,'review'=>0,'blocked'=>0,'errors'=>0);
        }
        $cursor=absint($state['cursor']??0);
        $business_force_sql = !empty($settings['business_enabled'])
            ? ($force_business_reconcile ? " OR seller_account_type='BUSINESS'" : " OR (seller_account_type='BUSINESS' AND (COALESCE(route_state,'')<>'ready' OR COALESCE(output_state,'') IN ('','repair_pending')))")
            : '';
        $postmeta_table = isset($wpdb->postmeta) ? $wpdb->postmeta : $wpdb->prefix . 'postmeta';
        // Capacity is an output defect, not a classifier defect. Include only
        // those PRIVATE rows explicitly so they can be recovered without
        // rematerializing the entire PRIVATE source catalog. Disabled PRIVATE
        // means zero PRIVATE maintenance SQL.
        $private_capacity_sql = !empty($settings['private_enabled'])
            ? " OR (seller_account_type='INDIVIDUAL' AND listing_post_id>0 AND listing_post_id IN (SELECT post_id FROM {$postmeta_table} WHERE meta_key='_ppar_ebay_reserve_state' AND meta_value='capacity'))"
            : '';
        $private_repair_sql = !empty($settings['private_enabled'])
            ? " OR (seller_account_type='INDIVIDUAL' AND COALESCE(route_state,'')='ready' AND COALESCE(output_state,'') IN ('','repair_pending'))"
            : '';
        $enabled_route_sql = !empty($settings['private_enabled']) && !empty($settings['business_enabled'])
            ? "seller_account_type IN ('INDIVIDUAL','BUSINESS')"
            : (!empty($settings['private_enabled']) ? "seller_account_type='INDIVIDUAL'" : "seller_account_type='BUSINESS'");
        // Contract changes are background-only and time-bounded, but new strict
        // equestrian product families and newly blocked media must be recovered
        // promptly even when their row IDs are high. Pull a tiny priority prepass
        // independently of the cursor, then continue the ordinary monotonic scan.
        $priority_rows=array();
        $priority_catalog=$this->ebay_portal_catalog();
        $priority_contract_enabled=!is_wp_error($priority_catalog)
            && (string)($priority_catalog['content_policy']['version']??'')===self::EBAY_CONTENT_POLICY_VERSION
            && version_compare((string)self::EBAY_CONTENT_POLICY_VERSION,'5.0','>=');
        if($contract_changed && $priority_contract_enabled){
            $priority_limit=min(50,$limit);
            $priority_stale_sql="COALESCE(policy_version,'')<>%s";
            $priority_args=array(self::EBAY_CONTENT_POLICY_VERSION);
            if(!empty($settings['business_enabled'])){$priority_stale_sql.=" OR (seller_account_type='BUSINESS' AND COALESCE(classifier_version,'')<>%s)";$priority_args[]=self::EBAY_BUSINESS_CLASSIFIER_VERSION;}
            $priority_sql_template="SELECT * FROM {$table} WHERE {$enabled_route_sql} AND COALESCE(source_state,'available')<>'ended' AND (".$priority_stale_sql.") AND (LOWER(title) LIKE '%%reithelm%%' OR LOWER(title) LIKE '%%reithose%%' OR LOWER(title) LIKE '%%reithandsch%%' OR LOWER(title) LIKE '%%reitstief%%' OR LOWER(title) LIKE '%%reitschuh%%' OR LOWER(title) LIKE '%%reitweste%%' OR LOWER(title) LIKE '%%reitjacke%%' OR LOWER(title) LIKE '%%kinderbuch%%' OR LOWER(title) LIKE '%%pferdebuch%%' OR LOWER(title) LIKE '%%ponybuch%%' OR LOWER(title) LIKE '%%bilderbuch%%' OR LOWER(title) LIKE '%%malbuch%%' OR LOWER(title) LIKE '%%stickerbuch%%' OR LOWER(source_payload) LIKE '%%categoryname%%buech%%' OR LOWER(source_payload) LIKE '%%categoryname%%büch%%') ORDER BY id ASC LIMIT %d";
            $priority_args[]=$priority_limit;
            $priority_sql=call_user_func_array(array($wpdb,'prepare'),array_merge(array($priority_sql_template),$priority_args));
            $priority_rows=(array)$wpdb->get_results($priority_sql,ARRAY_A);
        }
        $priority_ids=array_values(array_filter(array_map(static function($r){return is_array($r)?absint($r['id']??0):0;},$priority_rows)));
        $remaining=max(0,$limit-count($priority_rows));
        $rows=array_values($priority_rows);
        if($remaining>0){
            $exclude_sql=''; $exclude_args=array();
            if($priority_ids){$exclude_sql=' AND id NOT IN ('.implode(',',array_fill(0,count($priority_ids),'%d')).')';$exclude_args=$priority_ids;}
            $stale_sql="COALESCE(policy_version,'')<>%s";
            $sql_args=array($cursor,self::EBAY_CONTENT_POLICY_VERSION);
            if(!empty($settings['private_enabled'])){$stale_sql.=" OR (seller_account_type='INDIVIDUAL' AND COALESCE(classifier_version,'')<>%s)";$sql_args[]=self::EBAY_PRIVATE_CLASSIFIER_VERSION;}
            if(!empty($settings['business_enabled'])){$stale_sql.=" OR (seller_account_type='BUSINESS' AND COALESCE(classifier_version,'')<>%s)";$sql_args[]=self::EBAY_BUSINESS_CLASSIFIER_VERSION;}
            $sql_args=array_merge($sql_args,$exclude_args,array($remaining));
            $sql_template="SELECT * FROM {$table} WHERE id>%d AND {$enabled_route_sql} AND COALESCE(source_state,'available')<>'ended' AND (" . $stale_sql . $business_force_sql . $private_capacity_sql . $private_repair_sql . ")" . $exclude_sql . " ORDER BY id ASC LIMIT %d";
            $sql=call_user_func_array(array($wpdb,'prepare'),array_merge(array($sql_template),$sql_args));
            $rows=array_merge($rows,(array)$wpdb->get_results($sql,ARRAY_A));
        }
        $stats=array('scanned'=>0,'ready_private'=>0,'ready_business'=>0,'review'=>0,'blocked'=>0,'errors'=>0,'private_touched'=>0,'business_touched'=>0);
        $priority_id_map=array_flip($priority_ids);
        $time_budget_seconds=max(1,min(30,absint($time_budget_seconds)));
        $deadline=microtime(true)+$time_budget_seconds;
        $budget_exhausted=false;
        foreach($rows as $row){
            if($stats['scanned']>0 && microtime(true)>=$deadline){$budget_exhausted=true;break;}
            $row_id=absint($row['id']??0);
            if(!isset($priority_id_map[$row_id])){$state['cursor']=max(absint($state['cursor']??0),$row_id);}
            $stats['scanned']++;
            $payload=json_decode((string)($row['source_payload']??''),true); $payload=is_array($payload)?$payload:array();
            $raw=is_array($payload['raw']??null)?$payload['raw']:array();
            $seller_type=strtoupper(sanitize_key((string)($row['seller_account_type']??'')));
            if(!$this->ebay_route_enabled($seller_type,$settings)){continue;}
            if($seller_type==='INDIVIDUAL'){$stats['private_touched']++;}elseif($seller_type==='BUSINESS'){$stats['business_touched']++;}
            if(!$raw){$this->ebay_maintenance_set_review_state($row,$seller_type,new WP_Error('ebay_maintenance_source_missing','Gespeicherter Originalpayload fehlt.'));$stats['review']++;continue;}
            $policy_reason=$this->ebay_content_policy_reason(array('raw'=>$raw,'title'=>(string)($row['title']??'')));
            if($policy_reason!==''){$this->ebay_quarantine_filtered_row($row,$policy_reason);$stats['blocked']++;continue;}
            $item=$this->ebay_accept_item($raw,$seller_type,$settings);
            if(is_wp_error($item)){
                if(in_array((string)$item->get_error_code(),array('ebay_toy_item_blocked','ebay_content_policy_blocked'),true)){$this->ebay_quarantine_filtered_row($row,$item->get_error_message());$stats['blocked']++;continue;}
                if((string)$item->get_error_code()==='ebay_item_ended'){$this->ebay_refresh_mark_ended($row,'Gespeichertes eBay-Enddatum ist erreicht.');continue;}
                $this->ebay_maintenance_set_review_state($row,$seller_type,$item);$stats['review']++;continue;
            }
            $rule=$this->ebay_rule_by_id((string)($row['rule_id']??''),$settings);
            $manual_term_id=0;
            if($seller_type==='INDIVIDUAL'){
                $manual_decision=$this->ebay_candidate_manual_decision((string)($row['item_id']??''));
                $manual_status=sanitize_key((string)($manual_decision['status']??'automatic'));
                if(in_array($manual_status,array('veto','paused'),true)){
                    $message=sanitize_text_field((string)($manual_decision['reason']??'Manuelles Chef-Veto ist aktiv.'));
                    $manual_update=array('status'=>'blocked_manual','policy_state'=>'allowed','route_state'=>'blocked','output_state'=>'none','policy_version'=>self::EBAY_CONTENT_POLICY_VERSION,'classifier_version'=>self::EBAY_PRIVATE_CLASSIFIER_VERSION,'rejection_reason'=>'[ebay_manual_veto] '.$message,'updated_at'=>time());
                    $wpdb->update($table,$manual_update,array('id'=>absint($row['id']??0)),$this->ebay_db_formats($manual_update),array('%d'));
                    $this->ebay_private_listing_route_meta($row,'review',$message);$stats['blocked']++;continue;
                }
                if($manual_status==='approved'){
                    $term=$this->ebay_target_from_candidate_decision($manual_decision,$settings);
                    if(is_wp_error($term)){$this->ebay_maintenance_set_review_state($row,$seller_type,$term);$stats['review']++;continue;}
                    $classification=$this->ebay_manual_classification($term,$item,(string)($manual_decision['reason']??'Manuell freigegeben.'));
                    $manual_term_id=absint($term->term_id??0);
                } else {
                    $classification=$this->ebay_classify_portal_item($item,$rule);
                }
            } else {
                $classification=$this->ebay_business_classify_portal_item_strict($item,$rule);
            }
            if(is_wp_error($classification)){
                if($seller_type==='INDIVIDUAL' && $this->ebay_private_preserve_last_good_route_on_soft_review($row,$classification)){
                    $stats['review']++;continue;
                }
                if($seller_type==='BUSINESS' && $this->ebay_business_preserve_last_good_on_soft_review($row,$classification)){
                    $stats['review']++;continue;
                }
                $this->ebay_maintenance_set_review_state($row,$seller_type,$classification);$stats['review']++;continue;
            }
            $item['portal_classification']=$classification;
            $payload['portal_classification']=$classification;
            $updates=array(
                'policy_state'=>'allowed','route_state'=>'ready','policy_version'=>self::EBAY_CONTENT_POLICY_VERSION,
                'classifier_version'=>$this->ebay_maintenance_classifier_version($seller_type),
                'source_payload'=>wp_json_encode($payload,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES),'rejection_reason'=>'','updated_at'=>time(),
            );
            if($seller_type==='INDIVIDUAL'){
                $target_rule=$rule; $target_rule['target_term_slug']=sanitize_title((string)($classification['private_bucket_slug']??''));
                $term_id=$manual_term_id>0?$manual_term_id:$this->ebay_rule_target_term($target_rule,$settings);
                if(is_wp_error($term_id)||absint($term_id)<=0){$this->ebay_maintenance_set_review_state($row,$seller_type,is_wp_error($term_id)?$term_id:new WP_Error('ebay_private_target_missing','Zielkategorie fehlt.'));$stats['review']++;continue;}
                // V6.19 capacity contract: maintenance only refreshes the durable
                // source/classification row. Missing, changed or capacity-reserved
                // HivePress output is repaired once by the bounded selector when
                // the maintenance cycle completes. This prevents maintenance from
                // creating listings that the 250/30 cap would immediately demote.
                $updates['target_term_id']=absint($term_id);
                $updates['output_state']='listing_pending';
                $stats['ready_private']++;
            } else {
                // V6.19: maintenance updates the same source/classifier contract,
                // but public BUSINESS materialization is decided only by the
                // bounded global quality rebalancer at cycle completion.
                $quality=$this->ebay_business_quality_assess($item,$classification,$rule,$settings,0.0);
                if(is_wp_error($quality)){
                    $this->ebay_business_pause_output_for_capacity($row,'quality_blocked',$quality->get_error_message());
                    $updates['output_state']='quality_blocked';
                    $stats['review']++;
                } else {
                    $item=$this->ebay_business_item_with_quality($item,$quality);
                    $payload['business_quality']=$quality;
                    $payload['business_selection']=array('role'=>'candidate','rank'=>0,'updated_at'=>time());
                    $updates['source_payload']=wp_json_encode($payload,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);
                    $updates['output_state']='candidate';
                    $stats['ready_business']++;
                }
            }
            $wpdb->update($table,$updates,array('id'=>absint($row['id']??0)),$this->ebay_db_formats($updates),array('%d'));
        }
        $cycle=is_array($state['cycle_stats']??null)?$state['cycle_stats']:array();
        foreach(array('scanned','ready_private','ready_business','review','blocked','errors','private_touched','business_touched') as $key){
            $cycle[$key]=absint($cycle[$key]??0)+absint($stats[$key]??0);
        }
        $normal_row_count=max(0,count($rows)-count($priority_rows));
        if(!$budget_exhausted && $normal_row_count<$remaining){
            // The ordinary cursor scan is exhausted. Priority rows are independent
            // of the cursor and therefore never make a cutover look complete early.
            $state['completed_at']=time(); $state['cursor']=0;
            $private_touched=!empty($settings['private_enabled']) && absint($cycle['private_touched']??0)>0;
            $business_touched=!empty($settings['business_enabled']) && absint($cycle['business_touched']??0)>0;
            if($private_touched || $business_touched){
                $scope=$private_touched&&$business_touched?'all':($private_touched?'private':'business');
                if ($allow_during_refresh) {
                    // Embedded maintenance is only phase 1 of the refresh owner.
                    // It must never create a competing selection owner while the
                    // refresh job is still open. Refresh-finalize queues exactly
                    // one selection after local, asset and getItem phases finish.
                    $cycle['selection']=array('status'=>'deferred_to_refresh_finalize','scope'=>$scope,'queued'=>0);
                } else {
                    // Standalone maintenance is no longer a second mutation owner.
                    // If it discovers changed rows, hand off to the one canonical
                    // refresh/selection run instead of creating a legacy selector.
                    $selection=method_exists($this,'ebay_run_start')?$this->ebay_run_start(false,'refresh'):new WP_Error('canonical_run_unavailable','Kanonischer eBay-Gesamtlauf fehlt.');
                    $cycle['selection']=array('status'=>is_wp_error($selection)?'failed':sanitize_key((string)($selection['status']??'queued')),'scope'=>$scope,'queued'=>is_wp_error($selection)?0:1);
                }
            }else{
                $cycle['selection']=array('status'=>'not_required','scope'=>'none','queued'=>0);
            }
            $state['last_stats']=$cycle;
            $state['cycle_stats']=array();
        } else {
            $state['completed_at']=0;
            $state['last_stats']=$cycle;
            $state['cycle_stats']=$cycle;
        }
        $state['policy_version']=self::EBAY_CONTENT_POLICY_VERSION;
        $state['private_classifier_version']=self::EBAY_PRIVATE_CLASSIFIER_VERSION;
        $state['business_classifier_version']=self::EBAY_BUSINESS_CLASSIFIER_VERSION;
        $state['last_run_at']=time();
        $this->ebay_maintenance_state_save($state);
        $stats['budget_exhausted']=$budget_exhausted?1:0;
        return $stats;
    }

    private function ebay_api_base($settings) {
        return (string) ($settings['environment'] ?? '') === 'sandbox' ? 'https://api.sandbox.ebay.com' : 'https://api.ebay.com';
    }

    private function ebay_token_cache_key($settings) {
        return 'ppar_ebay_token_' . substr(hash('sha256', (string) ($settings['environment'] ?? '') . '|' . (string) ($settings['client_id'] ?? '')), 0, 24);
    }

    private function ebay_access_token($settings, $force = false) {
        $cache_key = $this->ebay_token_cache_key($settings);
        if (!$force && function_exists('get_transient')) {
            $cached = get_transient($cache_key);
            if (is_string($cached) && $cached !== '') { return $cached; }
        }
        $client_id = (string) ($settings['client_id'] ?? '');
        $client_secret = (string) ($settings['client_secret'] ?? '');
        if ($client_id === '' || $client_secret === '') { return new WP_Error('ebay_credentials_missing', 'eBay-Zugangsdaten fehlen.'); }
        $response = wp_remote_post($this->ebay_api_base($settings) . '/identity/v1/oauth2/token', array(
            'timeout' => 25,
            'redirection' => 2,
            'headers' => array(
                'Authorization' => 'Basic ' . base64_encode($client_id . ':' . $client_secret),
                'Content-Type' => 'application/x-www-form-urlencoded',
                'Accept' => 'application/json',
            ),
            'body' => 'grant_type=client_credentials&scope=' . rawurlencode('https://api.ebay.com/oauth/api_scope'),
        ));
        if (is_wp_error($response)) { return $response; }
        $code = absint(wp_remote_retrieve_response_code($response));
        $body = json_decode((string) wp_remote_retrieve_body($response), true);
        if ($code < 200 || $code >= 300 || !is_array($body) || empty($body['access_token'])) {
            return new WP_Error('ebay_oauth_failed', 'eBay OAuth fehlgeschlagen (HTTP ' . $code . ').');
        }
        $token = (string) $body['access_token'];
        $ttl = max(300, absint($body['expires_in'] ?? 7200) - 300);
        if (function_exists('set_transient')) { set_transient($cache_key, $token, $ttl); }
        return $token;
    }

    private function ebay_reference_id($settings, $rule, $seller_type) {
        $portal = method_exists($this, 'output_local_portal_key') ? $this->output_local_portal_key() : 'local';
        $parts = array(
            sanitize_key((string) ($settings['affiliate_reference_prefix'] ?? 'portal')),
            sanitize_key((string) $portal),
            sanitize_key((string) ($rule['id'] ?? 'rule')),
            strtolower(sanitize_key((string) $seller_type)),
        );
        return substr(implode('-', array_filter($parts)), 0, 240);
    }

    /**
     * V5.4.0: Die acht privaten Bereiche werden nicht mehr nur über je eine
     * Sammelphrase abgefragt. Kleine, fachlich kontrollierte Varianten erhöhen
     * die reale Abdeckung, während die nachgelagerte Fachklassifikation weiter
     * allein über die tatsächlichen Angebotsdaten entscheidet.
     */
    private function ebay_private_query_variants($rule) {
        $rule = is_array($rule) ? $rule : array();
        $id = sanitize_key((string) ($rule['id'] ?? ''));
        $map = array(
            'pferde-ponys'=>array('Pferd','Pony'),
            'sattel-zaumzeug'=>array('Pferdesattel','Zaumzeug Pferd','Trense Pferd'),
            'decken-schutz'=>array('Pferdedecke','Gamaschen Pferd','Fliegendecke Pferd'),
            'stall-weide-haltung'=>array('Pferdestall','Weidezaun Pferd','Heunetz Pferd'),
            'fuetterung-pflege'=>array('Pferdefutter','Pferdepflege','Putzzeug Pferd'),
            'anhaenger-transport'=>array('Pferdeanhänger','Pferdetransport','Transportgamaschen Pferd'),
            'reitbekleidung-zubehoer'=>array('Reitbekleidung','Reithelm','Reitstiefel','Lederreitstiefel','Dressurstiefel','Reitgummistiefel','Reithose','Reithandschuhe','Reitweste'),
            'sonstiges'=>array('Pferdezubehör','Reitsport Zubehör'),
        );
        $queries = isset($map[$id]) ? $map[$id] : array((string) ($rule['query'] ?? ''));
        $safe = array();
        foreach ($queries as $query) {
            $query = substr(sanitize_text_field((string) $query), 0, 100);
            if ($query !== '') { $safe[$query] = $query; }
        }
        if (!$safe && !empty($rule['query'])) { $safe[(string) $rule['query']] = substr(sanitize_text_field((string) $rule['query']), 0, 100); }
        return array_values($safe);
    }

    /**
     * Generic BUSINESS fallback query for a coarse rule. V6.17 no longer uses
     * hand-maintained product exceptions here; exact product discovery is built
     * from the complete verified portal catalog below.
     */
    private function ebay_business_query_variants($rule) {
        $rule = is_array($rule) ? $rule : array();
        $query = substr(sanitize_text_field((string)($rule['query'] ?? '')), 0, 100);
        return $query !== '' ? array($query) : array();
    }

    /**
     * Build one conservative eBay search phrase for a verified portal product
     * concept. Generic product labels receive an explicit Pferd qualifier so
     * broad marketplace meanings do not dominate the first result page.
     */
    private function ebay_business_concept_query($concept) {
        $concept = is_array($concept) ? $concept : array();
        $title = trim(sanitize_text_field((string)($concept['title'] ?? '')));
        if ($title === '') { return ''; }

        // Keep the complete catalog identity. Removing use-context here caused
        // systematic discovery starvation (e.g. "Kameras im Stall" became
        // "Kameras Pferd"; "Desinfektionsmittel für Stall" became
        // "Desinfektionsmittel Pferd") before the strict classifier ran.
        $identity = $title;

        $topic = $this->ebay_topic_text($identity);
        $has_equine_scope = false;
        foreach (array('pferd','pferde','pony','ponys','fohlen','horse','horses','equine','equestrian') as $marker) {
            if ($this->ebay_topic_term_present($topic, $marker)) { $has_equine_scope = true; break; }
        }
        if (!$has_equine_scope) {
            $catalog = $this->ebay_portal_catalog();
            if (!is_wp_error($catalog)) {
                foreach ((array)($catalog['business_inherent_markers'] ?? array()) as $marker) {
                    if ($this->ebay_business_strict_token_present($topic, (string)$marker)) {
                        $has_equine_scope = true;
                        break;
                    }
                }
            }
        }
        $query = $identity . ($has_equine_scope ? '' : ' Pferd');
        return substr(sanitize_text_field($query), 0, 100);
    }

    /**
     * Complete BUSINESS discovery contract. Every verified product concept and
     * every verified hub-family concept is represented. Explicit hub aliases
     * (for example Reithose -> Reiterbedarf) become their own exact queries.
     * Entries are interleaved by coarse portal bucket so every work package
     * covers the whole portal instead of one alphabetic/product-family cluster.
     */
    private function ebay_business_catalog_profiles($settings) {
        $catalog = $this->ebay_portal_catalog();
        if (is_wp_error($catalog)) { return array(); }
        $settings = is_array($settings) ? $settings : array();
        if (empty($settings['business_enabled'])) { return array(); }

        $enabled_buckets = array();
        $bucket_order = array();
        foreach ((array)($settings['rules'] ?? array()) as $rule) {
            if (!is_array($rule) || empty($rule['active']) || empty($rule['business'])) { continue; }
            $bucket = sanitize_title((string)($rule['target_term_slug'] ?? $rule['id'] ?? ''));
            if ($bucket === '') { continue; }
            $enabled_buckets[$bucket] = true;
            if (!in_array($bucket, $bucket_order, true)) { $bucket_order[] = $bucket; }
        }
        if (!$enabled_buckets) { return array(); }

        $by_bucket = array();
        $collections = array(
            'product'=>(array)($catalog['business_concepts'] ?? array()),
            'hub'=>(array)($catalog['business_hub_concepts'] ?? array()),
        );
        foreach ($collections as $concept_kind => $concepts) {
            foreach ($concepts as $concept) {
                if (!is_array($concept)) { continue; }
                $concept_id = sanitize_key((string)($concept['id'] ?? ''));
                $primary = is_array($concept['target_pages'][0] ?? null) ? $concept['target_pages'][0] : array();
                $bucket = sanitize_title((string)($primary['private_bucket_slug'] ?? $concept['private_bucket_slug'] ?? ''));
                if ($concept_id === '' || $bucket === '' || empty($enabled_buckets[$bucket])) { continue; }

                $query_labels = array((string)($concept['title'] ?? ''));
                if ($concept_kind === 'hub') {
                    foreach ((array)($concept['aliases'] ?? array()) as $alias) { $query_labels[] = (string)$alias; }
                }
                $query_index = 0;
                foreach ($query_labels as $label) {
                    $query = $this->ebay_business_concept_query(array('title'=>$label));
                    if ($query === '') { continue; }
                    $query_index++;
                    if (!isset($by_bucket[$bucket])) { $by_bucket[$bucket] = array(); }
                    $by_bucket[$bucket][] = array(
                        'concept'=>$concept,'concept_kind'=>$concept_kind,'query'=>$query,'query_index'=>$query_index,
                    );
                }
            }
        }

        foreach (array_keys($by_bucket) as $bucket) {
            if (!in_array($bucket, $bucket_order, true)) { $bucket_order[] = $bucket; }
        }

        $profiles = array();
        $offset = 0;
        while (true) {
            $added = false;
            foreach ($bucket_order as $bucket) {
                if (empty($by_bucket[$bucket][$offset])) { continue; }
                $added = true;
                $entry = $by_bucket[$bucket][$offset];
                $concept = (array)$entry['concept'];
                $concept_id = sanitize_key((string)($concept['id'] ?? ''));
                $concept_kind = sanitize_key((string)($entry['concept_kind'] ?? 'product'));
                $query_index = max(1, absint($entry['query_index'] ?? 1));
                $key = 'business-' . $concept_kind . '|' . $concept_id . '|q' . $query_index;
                $profiles[$key] = array(
                    'key'=>$key,
                    'rule'=>array(
                        'id'=>$concept_id,
                        'label'=>sanitize_text_field((string)($concept['title'] ?? '')),
                        'query'=>(string)$entry['query'],
                        'target_term_slug'=>$bucket,
                        'private'=>false,
                        'business'=>true,
                        'active'=>true,
                        'business_concept_id'=>$concept_id,
                        'business_concept_kind'=>$concept_kind,
                        'request_limit'=>30,
                    ),
                    'seller_type'=>'BUSINESS',
                    'expected_business_concept_id'=>$concept_id,
                    'expected_business_concept_kind'=>$concept_kind,
                    'next'=>'',
                    'active'=>true,
                    'pages'=>0,
                    'page_limit'=>1,
                    'route_limit'=>5,
                    'profile_kind'=>'business_' . $concept_kind . '_concept',
                );
            }
            if (!$added) { break; }
            $offset++;
        }
        return $profiles;
    }

    public function ebay_build_search_request($rule, $seller_type, $settings = null, $token = 'TEST_TOKEN', $offset = 0) {
        $settings = is_array($settings) ? $this->ebay_normalize_settings($settings, true) : $this->ebay_settings();
        $rule = is_array($rule) ? $rule : array();
        $seller_type = strtoupper(sanitize_key((string) $seller_type));
        if (!in_array($seller_type, array('INDIVIDUAL','BUSINESS'), true)) {
            return new WP_Error('ebay_seller_type_invalid', 'Ungültiger Verkäuferkontotyp.');
        }
        $query = sanitize_text_field((string) ($rule['query'] ?? ''));
        if ($query === '') { return new WP_Error('ebay_query_missing', 'eBay-Suchbegriff fehlt.'); }
        $profile_limit = absint($rule['request_limit'] ?? 0);
        $limit = max(1, min(50, $profile_limit > 0 ? $profile_limit : absint($settings['max_per_rule'] ?? 20)));
        $filters = array('sellerAccountTypes:{' . $seller_type . '}', 'deliveryCountry:DE');
        $args = array(
            'q' => $query,
            'limit' => $limit,
            'offset' => max(0, absint($offset)),
            'fieldgroups' => 'EXTENDED',
            'filter' => implode(',', $filters),
        );
        $category_ids = array_values(array_filter(array_map('strval', (array) ($rule['category_ids'] ?? array()))));
        if ($category_ids) { $args['category_ids'] = implode(',', $category_ids); }
        $reference = $this->ebay_reference_id($settings, $rule, $seller_type);
        $enduser = 'affiliateCampaignId=' . (string) ($settings['epn_campaign_id'] ?? '') . ',affiliateReferenceId=' . $reference;
        $postal = trim((string) ($settings['delivery_postal_code'] ?? ''));
        if ($postal !== '') {
            $enduser .= ',contextualLocation=' . rawurlencode('country=DE,zip=' . $postal);
        }
        return array(
            'url' => add_query_arg($args, $this->ebay_api_base($settings) . '/buy/browse/v1/item_summary/search'),
            'headers' => array(
                'Authorization' => 'Bearer ' . $token,
                'Accept' => 'application/json',
                'Accept-Language' => 'de-DE',
                'X-EBAY-C-MARKETPLACE-ID' => 'EBAY_DE',
                'X-EBAY-C-ENDUSERCTX' => $enduser,
            ),
            'timeout' => 20,
            'redirection' => 2,
        );
    }

    private function ebay_search($rule, $seller_type, $settings) {
        $token = $this->ebay_access_token($settings);
        if (is_wp_error($token)) { return $token; }
        $page = $this->ebay_search_page($rule, $seller_type, $settings, $token, '');
        if (is_wp_error($page)) { return $page; }
        return (array) ($page['items'] ?? array());
    }

    /**
     * V5.4.0 – exakt eine Browse-Seite. Folgeseiten werden ausschließlich über
     * eBays `next`-URL geladen; `total` wird niemals als Pagination-Steuerung benutzt.
     */
    private function ebay_search_page($rule, $seller_type, $settings, $token, $next_url = '') {
        $request = $this->ebay_build_search_request($rule, $seller_type, $settings, $token, 0);
        if (is_wp_error($request)) { return $request; }
        $url = trim((string) $next_url);
        if ($url !== '') {
            $url = $this->ebay_validate_next_url($url, $settings);
            if (is_wp_error($url)) { return $url; }
        } else {
            $url = (string) $request['url'];
        }
        $response = wp_remote_get($url, array(
            'timeout'=>$request['timeout'],
            'redirection'=>$request['redirection'],
            'headers'=>$request['headers'],
        ));
        if (is_wp_error($response)) { return $response; }
        $code = absint(wp_remote_retrieve_response_code($response));
        $body = json_decode((string) wp_remote_retrieve_body($response), true);
        if ($code < 200 || $code >= 300 || !is_array($body)) {
            return new WP_Error('ebay_search_failed', 'eBay Browse API fehlgeschlagen (HTTP ' . $code . ').');
        }
        $next = trim((string) ($body['next'] ?? ''));
        if ($next !== '') {
            $validated = $this->ebay_validate_next_url($next, $settings);
            if (is_wp_error($validated)) { return $validated; }
            $next = $validated;
        }
        return array(
            'items'=>is_array($body['itemSummaries'] ?? null) ? array_values($body['itemSummaries']) : array(),
            'next'=>$next,
            'href'=>esc_url_raw((string) ($body['href'] ?? $url)),
            'offset'=>absint($body['offset'] ?? 0),
            'limit'=>absint($body['limit'] ?? ($settings['max_per_rule'] ?? 50)),
            'total'=>absint($body['total'] ?? 0),
        );
    }

    /** `next` darf nie als beliebige Remote-URL missbraucht werden. */
    private function ebay_validate_next_url($url, $settings) {
        $url = esc_url_raw((string) $url);
        if ($url === '' || !wp_http_validate_url($url)) {
            return new WP_Error('ebay_next_url_invalid', 'Ungültige eBay-Pagination-URL.');
        }
        $base = $this->ebay_api_base($settings);
        $base_parts = wp_parse_url($base);
        $parts = wp_parse_url($url);
        $scheme = strtolower((string) ($parts['scheme'] ?? ''));
        $host = strtolower((string) ($parts['host'] ?? ''));
        $base_host = strtolower((string) ($base_parts['host'] ?? ''));
        $path = (string) ($parts['path'] ?? '');
        if ($scheme !== 'https' || $host === '' || $host !== $base_host || $path !== '/buy/browse/v1/item_summary/search') {
            return new WP_Error('ebay_next_url_untrusted', 'eBay-Pagination verweist auf eine nicht freigegebene URL.');
        }
        return $url;
    }

    /** Vollständiger getItem-Request für die gezielte Bestandsnachprüfung. */
    private function ebay_build_item_refresh_request($row, $settings, $token) {
        $row = is_array($row) ? $row : array();
        $item_id = substr(sanitize_text_field((string) ($row['item_id'] ?? '')), 0, 191);
        if ($item_id === '') { return new WP_Error('ebay_refresh_item_id_missing', 'eBay-Item-ID für Bestandsabgleich fehlt.'); }
        $seller_type = strtoupper(sanitize_key((string) ($row['seller_account_type'] ?? '')));
        $rule = $this->ebay_rule_by_id((string) ($row['rule_id'] ?? ''));
        $reference = $this->ebay_reference_id($settings, $rule, in_array($seller_type, array('INDIVIDUAL','BUSINESS'), true) ? $seller_type : 'INDIVIDUAL');
        $enduser = 'affiliateCampaignId=' . (string) ($settings['epn_campaign_id'] ?? '') . ',affiliateReferenceId=' . $reference;
        $postal = trim((string) ($settings['delivery_postal_code'] ?? ''));
        if ($postal !== '') { $enduser .= ',contextualLocation=' . rawurlencode('country=DE,zip=' . $postal); }
        return array(
            'url'=>$this->ebay_api_base($settings) . '/buy/browse/v1/item/' . rawurlencode($item_id),
            'headers'=>array(
                'Authorization'=>'Bearer ' . (string) $token,
                'Accept'=>'application/json',
                'Accept-Language'=>'de-DE',
                'X-EBAY-C-MARKETPLACE-ID'=>'EBAY_DE',
                'X-EBAY-C-ENDUSERCTX'=>$enduser,
            ),
            // V5.24: Einzelchecks duerfen die Refresh-Queue nicht minutenlang
            // blockieren. Transiente Timeouts deaktivieren ein Listing nicht; sie
            // werden beim naechsten stündlichen Lauf erneut versucht.
            'timeout'=>8,
            'redirection'=>2,
        );
    }

    /**
     * Liefert state=active|ended. Netzwerk-/Rate-Limit-/Serverfehler bleiben
     * WP_Error und führen ausdrücklich nicht zu einem destruktiven Statuswechsel.
     */
    private function ebay_fetch_item_for_refresh($row, $settings, $token) {
        $request = $this->ebay_build_item_refresh_request($row, $settings, $token);
        if (is_wp_error($request)) { return $request; }
        $response = wp_remote_get((string) $request['url'], array(
            'timeout'=>$request['timeout'],
            'redirection'=>$request['redirection'],
            'headers'=>$request['headers'],
        ));
        if (is_wp_error($response)) { return new WP_Error('ebay_refresh_transport', $response->get_error_message()); }
        $code = absint(wp_remote_retrieve_response_code($response));
        if (in_array($code, array(404,410), true)) {
            return array('state'=>'ended','reason'=>'not_found','http_code'=>$code,'raw'=>array());
        }
        if ($code === 429 || $code >= 500) {
            return new WP_Error('ebay_refresh_transient_http', 'eBay-Bestandsabgleich vorübergehend nicht verfügbar (HTTP ' . $code . ').');
        }
        $body = json_decode((string) wp_remote_retrieve_body($response), true);
        if ($code < 200 || $code >= 300 || !is_array($body)) {
            return new WP_Error('ebay_refresh_http', 'eBay-Bestandsabgleich fehlgeschlagen (HTTP ' . $code . ').');
        }
        $end_at = 0;
        if (!empty($body['itemEndDate'])) {
            $parsed = strtotime((string) $body['itemEndDate']);
            $end_at = $parsed ? absint($parsed) : 0;
        }
        if ($end_at > 0 && $end_at <= time()) {
            return array('state'=>'ended','reason'=>'item_end_date','http_code'=>$code,'raw'=>$body);
        }
        foreach ((array) ($body['estimatedAvailabilities'] ?? array()) as $availability) {
            $status = strtoupper(sanitize_key((string) (is_array($availability) ? ($availability['estimatedAvailabilityStatus'] ?? '') : '')));
            if ($status === 'OUT_OF_STOCK') {
                return array('state'=>'ended','reason'=>'out_of_stock','http_code'=>$code,'raw'=>$body);
            }
        }
        return array('state'=>'active','reason'=>'available','http_code'=>$code,'raw'=>$body);
    }

    private function ebay_valid_http_url($value) {
        $value = esc_url_raw((string) $value);
        return $value !== '' && wp_http_validate_url($value) ? $value : '';
    }

    /** Anbieter-Kohorte für öffentlich dargestellte Produktkampagnen. */
    private function ebay_product_campaign_cohort($campaign) {
        if (!is_array($campaign) || sanitize_key((string) ($campaign['creative_type'] ?? '')) !== 'product') { return ''; }
        return sanitize_key((string) ($campaign['network'] ?? '')) === 'ebay' ? 'ebay' : 'non_ebay';
    }

    /** Eine öffentliche Produktgruppe darf ausschließlich eine Anbieter-Kohorte enthalten. */
    private function ebay_product_campaigns_share_provider_cohort($campaigns) {
        $mode = method_exists($this, 'idealo_output_mode') ? $this->idealo_output_mode() : 'ebay_only';
        if (in_array($mode, array('separate','combined','automatic'), true)) { return true; }
        $cohort = '';
        foreach ((array) $campaigns as $campaign) {
            $current = $this->ebay_product_campaign_cohort($campaign);
            if ($current === '') { continue; }
            if ($cohort === '') { $cohort = $current; continue; }
            if ($current !== $cohort) { return false; }
        }
        return true;
    }

    /**
     * Laufzeit-Sicherheitsnetz: automatische Produktpositionen folgen der
     * Kohorte der höchstrangigen Kampagne. Damit kann auch eine später manuell
     * aktivierte Altkampagne keine eBay-/Nicht-eBay-Mischung erzeugen.
     */
    private function ebay_business_campaign_source_row($campaign) {
        if (!is_array($campaign) || sanitize_key((string) ($campaign['network'] ?? '')) !== 'ebay') { return array(); }
        $post_id = absint($campaign['post_id'] ?? 0);
        if ($post_id <= 0 || !function_exists('get_post_meta')) { return array(); }
        if (absint(get_post_meta($post_id, '_ppar_ebay_business_auto', true)) !== 1) { return array(); }
        $hash = strtolower(sanitize_text_field((string) get_post_meta($post_id, '_ppar_creative_identity_hash', true)));
        if (!preg_match('/^[a-f0-9]{64}$/', $hash)) { return array(); }
        global $wpdb;
        $row = $wpdb->get_row($wpdb->prepare(
            "SELECT * FROM {$this->ebay_items_table()} WHERE creative_identity_hash=%s AND seller_account_type='BUSINESS' ORDER BY id DESC LIMIT 1",
            $hash
        ), ARRAY_A);
        return is_array($row) ? $row : array();
    }

    /**
     * Public BUSINESS delivery is fail-closed from independent source/policy/
     * route state. A missed refresh never mutates or destroys the campaign, but
     * stale source data cannot win a public product slot.
     */
    private function ebay_business_campaign_source_allows_delivery($campaign) {
        if (!$this->ebay_business_campaign_source_allows_delivery_base($campaign)) { return false; }
        if (!is_array($campaign) || sanitize_key((string)($campaign['network'] ?? '')) !== 'ebay') { return true; }
        if (sanitize_key((string)($campaign['creative_type'] ?? '')) !== 'product') { return true; }
        $post_id=absint($campaign['post_id'] ?? 0);
        return $post_id > 0 && $this->ebay_public_checkpoint_allows_business_campaign($post_id);
    }

    /** Existing fach/public safety contract without checkpoint visibility. */
    private function ebay_business_campaign_source_allows_delivery_base($campaign) {
        if (!is_array($campaign) || sanitize_key((string) ($campaign['network'] ?? '')) !== 'ebay') { return true; }
        $post_id = absint($campaign['post_id'] ?? 0);
        if ($post_id <= 0 || !function_exists('get_post_meta')) { return false; }

        // Public eBay PRODUCT slots are a provider-managed contract. A legacy or
        // orphan eBay product without the source marker must never bypass the
        // source/policy gates. Non-product/manual eBay creatives remain outside
        // this BUSINESS-product contract.
        $is_product = sanitize_key((string)($campaign['creative_type'] ?? '')) === 'product';
        if (absint(get_post_meta($post_id, '_ppar_ebay_business_auto', true)) !== 1) { return !$is_product; }
        // A published campaign is the Last-Known-Good delivery contract. A
        // classifier/policy migration must never globally blank the frontend
        // before a replacement has been materialized successfully. Legacy
        // strict_v1 and current concept_v3 contracts may remain visible while a
        // soft reclassification is pending; hard source/policy/end signals still
        // block immediately.
        $contract = sanitize_key((string) get_post_meta($post_id, '_ppar_ebay_business_match_contract', true));
        if (!in_array($contract, array('strict_v1','concept_v3'), true)) { return false; }
        $row = $this->ebay_business_campaign_source_row($campaign);
        if (!$row) { return false; }
        if (sanitize_key((string) ($row['source_state'] ?? '')) !== 'available') { return false; }
        if (sanitize_key((string) ($row['policy_state'] ?? 'allowed')) === 'blocked') { return false; }
        if ($this->ebay_public_content_policy_reason_from_source_row($row, (string)($campaign['title'] ?? '')) !== '') { return false; }
        $end_at = absint($row['item_end_at'] ?? 0);
        if ($end_at > 0 && $end_at <= time()) { return false; }
        $route_state = sanitize_key((string)($row['route_state'] ?? ''));
        if ($route_state === 'review_last_good') { return true; }
        if ($route_state !== 'ready') { return false; }
        // Classifier-Versionen steuern Reconcile-Faelligkeit, nicht die sofortige
        // Sichtbarkeit eines bereits materialisierten concept_v3 Last-Known-Good.
        // Sonst wuerde jeder semantische Klassifikator-Bump den kompletten
        // BUSINESS-Content zwischen Plugin-Update und Reconcile erneut leeren.
        // Harte Source-/Policy-/End-Gates wurden oben bereits geprueft; Maintenance
        // erkennt den Versionsdrift separat und rematerialisiert kontrolliert.
        return true;
    }

    /**
     * Laufzeit-Sicherheitsnetz: automatische Produktpositionen folgen der
     * Kohorte der höchstrangigen Kampagne. Zusätzlich darf ein automatisches
     * eBay-BUSINESS-Produkt nur mit aktivem, erlaubtem Workflow-V2-Quellstatus
     * an der öffentlichen Auswahl teilnehmen.
     */
    private function ebay_filter_ranked_product_candidates_provider_cohort($candidates) {
        $candidates = array_values((array) $candidates);
        if (!$candidates) { return array(); }
        $candidates = array_values(array_filter($candidates, function($candidate) {
            $campaign = is_array($candidate) ? ($candidate['campaign'] ?? null) : null;
            if (!is_array($campaign) || sanitize_key((string) ($campaign['network'] ?? '')) !== 'ebay') { return true; }
            return $this->ebay_business_campaign_source_allows_delivery($campaign);
        }));
        if (!$candidates) { return array(); }
        $mode = method_exists($this, 'idealo_output_mode') ? $this->idealo_output_mode() : 'ebay_only';
        if ($mode === 'idealo_only') {
            $candidates = array_values(array_filter($candidates, function($candidate) {
                $campaign = is_array($candidate) ? ($candidate['campaign'] ?? null) : null;
                return is_array($campaign) && sanitize_key((string)($campaign['network'] ?? '')) === 'idealo';
            }));
        } elseif ($mode === 'ebay_only') {
            $first = is_array($candidates[0] ?? null) ? ($candidates[0]['campaign'] ?? null) : null;
            $cohort = $this->ebay_product_campaign_cohort($first);
            if ($cohort !== '') {
                $candidates = array_values(array_filter($candidates, function($candidate) use ($cohort) {
                    $campaign = is_array($candidate) ? ($candidate['campaign'] ?? null) : null;
                    return $this->ebay_product_campaign_cohort($campaign) === $cohort;
                }));
            }
        }
        // V6.20: seller diversity is a preference, not a visibility gate.
        // Pass 1 keeps the best offer per seller. Pass 2 appends further valid
        // offers from an already represented seller if otherwise a 3-card block
        // would stay needlessly empty. Near-identical products remain suppressed.
        $out = array(); $deferred = array(); $seen_sellers = array(); $seen_titles = array();
        foreach ($candidates as $candidate) {
            $campaign = is_array($candidate) ? ($candidate['campaign'] ?? null) : null;
            if (!is_array($campaign) || sanitize_key((string) ($campaign['network'] ?? '')) !== 'ebay') {
                $out[] = $candidate; continue;
            }
            $seller = $this->ebay_business_curation_key((string) ($campaign['partner'] ?? ''));
            if (strpos($seller, 'ebay') === 0) {
                $seller = $this->ebay_business_curation_key((string) get_post_meta(absint($campaign['_post_id'] ?? $campaign['post_id'] ?? 0), '_ppar_ebay_seller_username', true));
            }
            $title = $this->ebay_topic_text((string) ($campaign['title'] ?? $campaign['name'] ?? ''));
            $duplicate = false;
            foreach ($seen_titles as $known) {
                if ($title === '' || $known === '') { continue; }
                similar_text($title, $known, $pct);
                if ($pct >= 92.0) { $duplicate = true; break; }
            }
            if ($duplicate) { continue; }
            if ($seller !== '' && isset($seen_sellers[$seller])) {
                $deferred[] = $candidate;
                continue;
            }
            if ($seller !== '') { $seen_sellers[$seller] = true; }
            if ($title !== '') { $seen_titles[] = $title; }
            $out[] = $candidate;
        }
        foreach ($deferred as $candidate) {
            $campaign = is_array($candidate) ? ($candidate['campaign'] ?? null) : null;
            if (!is_array($campaign)) { continue; }
            $title = $this->ebay_topic_text((string) ($campaign['title'] ?? $campaign['name'] ?? ''));
            $duplicate = false;
            foreach ($seen_titles as $known) {
                if ($title === '' || $known === '') { continue; }
                similar_text($title, $known, $pct);
                if ($pct >= 92.0) { $duplicate = true; break; }
            }
            if ($duplicate) { continue; }
            if ($title !== '') { $seen_titles[] = $title; }
            $out[] = $candidate;
        }
        $out = array_values($out);
        if (in_array($mode, array('separate','combined','automatic'), true) && method_exists($this, 'multiprovider_reorder_candidates')) {
            $out = $this->multiprovider_reorder_candidates($out, $mode);
        }
        return array_values($out);
    }

    public function ebay_accept_item($item, $seller_type, $settings = null) {
        $settings = is_array($settings) ? $this->ebay_normalize_settings($settings, true) : $this->ebay_settings();
        $item = is_array($item) ? $item : array();
        $seller_type = strtoupper(sanitize_key((string) $seller_type));
        $actual_type = strtoupper(sanitize_key((string) ($item['seller']['sellerAccountType'] ?? '')));
        if (!in_array($seller_type, array('INDIVIDUAL','BUSINESS'), true) || $actual_type !== $seller_type) {
            return new WP_Error('ebay_seller_type_mismatch', 'Verkäuferkontotyp stimmt nicht mit der Eingangsweiche überein.');
        }
        if ((string) ($item['listingMarketplaceId'] ?? '') !== 'EBAY_DE') {
            return new WP_Error('ebay_marketplace_mismatch', 'Angebot stammt nicht aus EBAY_DE.');
        }
        if (!empty($item['adultOnly'])) {
            return new WP_Error('ebay_adult_item_blocked', 'Erwachsenenangebot ist nicht freigegeben.');
        }
        $toy_reason = $this->ebay_toy_filter_reason($item);
        if ($toy_reason !== '') { return new WP_Error('ebay_toy_item_blocked', $toy_reason); }
        $buying_options = array_values(array_unique(array_map('strtoupper', array_map('sanitize_key', (array) ($item['buyingOptions'] ?? array())))));
        if (in_array('CLASSIFIED_AD', $buying_options, true)) {
            return new WP_Error('ebay_classified_ad_blocked', 'CLASSIFIED_AD ist nicht freigegeben.');
        }
        $affiliate_url = $this->ebay_valid_http_url($item['itemAffiliateWebUrl'] ?? '');
        if ($affiliate_url === '') {
            return new WP_Error('ebay_affiliate_url_missing', 'itemAffiliateWebUrl fehlt; Ausgabe wird blockiert.');
        }
        $item_web_url = $this->ebay_valid_http_url($item['itemWebUrl'] ?? '');
        $image_url = $this->ebay_valid_http_url($item['image']['imageUrl'] ?? '');
        if ($image_url === '') { return new WP_Error('ebay_image_missing', 'eBay-Hauptbild fehlt.'); }
        $item_id = substr(sanitize_text_field((string) ($item['itemId'] ?? '')), 0, 191);
        $title = substr(sanitize_text_field((string) ($item['title'] ?? '')), 0, 180);
        if ($item_id === '' || $title === '') { return new WP_Error('ebay_identity_missing', 'eBay-ID oder Titel fehlt.'); }
        $price_value = sanitize_text_field((string) ($item['price']['value'] ?? ''));
        $currency = strtoupper(sanitize_key((string) ($item['price']['currency'] ?? '')));
        if ($price_value === '' || !is_numeric($price_value) || (float) $price_value < 0 || $currency !== 'EUR') {
            return new WP_Error('ebay_price_invalid', 'Vollständiger EUR-Preis fehlt.');
        }
        $end_at = 0;
        if (!empty($item['itemEndDate'])) {
            $end_at = strtotime((string) $item['itemEndDate']);
            $end_at = $end_at ? absint($end_at) : 0;
            if ($end_at > 0 && $end_at <= time()) { return new WP_Error('ebay_item_ended', 'eBay-Angebot ist bereits beendet.'); }
        }
        $seller_username = substr(sanitize_text_field((string) ($item['seller']['username'] ?? '')), 0, 191);
        if ($seller_username === '') { return new WP_Error('ebay_seller_username_missing', 'eBay-Verkäufername fehlt.'); }
        $seller_feedback_percentage = is_numeric($item['seller']['feedbackPercentage'] ?? null) ? (float) $item['seller']['feedbackPercentage'] : -1.0;
        $seller_feedback_score = is_numeric($item['seller']['feedbackScore'] ?? null) ? absint($item['seller']['feedbackScore']) : -1;
        if ($seller_type === 'BUSINESS') {
            $min_pct = (float) ($settings['business_min_feedback_percentage'] ?? 99.0);
            $min_score = absint($settings['business_min_feedback_score'] ?? 100);
            if ($seller_feedback_percentage < 0 || $seller_feedback_score < 0) {
                return new WP_Error('ebay_business_seller_quality_missing', 'BUSINESS-Verkäuferbewertung fehlt; automatische Ausgabe bleibt fail-closed.');
            }
            if ($seller_feedback_percentage + 0.0001 < $min_pct) {
                return new WP_Error('ebay_business_seller_feedback_low', 'BUSINESS-Verkäufer liegt unter der Mindestquote von ' . number_format($min_pct, 2, ',', '.') . ' % positiven Bewertungen.');
            }
            if ($seller_feedback_score < $min_score) {
                return new WP_Error('ebay_business_seller_feedback_count_low', 'BUSINESS-Verkäufer hat weniger als ' . absint($min_score) . ' Bewertungen.');
            }
        }
        $shipping_value = '';
        if (!empty($item['shippingOptions'][0]['shippingCost']['value'])) {
            $shipping_value = sanitize_text_field((string) $item['shippingOptions'][0]['shippingCost']['value']);
        }
        $location = array_filter(array(
            sanitize_text_field((string) ($item['itemLocation']['city'] ?? '')),
            sanitize_text_field((string) ($item['itemLocation']['country'] ?? '')),
        ));
        $brand = sanitize_text_field((string) ($item['brand'] ?? ''));
        if ($brand === '') {
            foreach ((array) ($item['localizedAspects'] ?? array()) as $aspect) {
                if (!is_array($aspect)) { continue; }
                $name = $this->ebay_topic_text((string) ($aspect['name'] ?? ''));
                if (in_array($name, array('marke','brand','hersteller','manufacturer'), true)) {
                    $brand = substr(sanitize_text_field((string) ($aspect['value'] ?? '')), 0, 120);
                    if ($brand !== '') { break; }
                }
            }
        }
        $returns_accepted = !empty($item['returnTerms']['returnsAccepted']);
        $qualified_programs = array_values(array_unique(array_filter(array_map('sanitize_key', (array) ($item['qualifiedPrograms'] ?? array())))));
        $created_at = 0;
        foreach (array('itemCreationDate','itemOriginDate') as $date_key) {
            if (!empty($item[$date_key])) { $ts = strtotime((string) $item[$date_key]); if ($ts) { $created_at = absint($ts); break; } }
        }
        $normalized = array(
            'item_id' => $item_id,
            'legacy_item_id' => substr(sanitize_text_field((string) ($item['legacyItemId'] ?? '')), 0, 80),
            'seller_account_type' => $seller_type,
            'seller_username' => $seller_username,
            'seller_feedback_percentage' => $seller_feedback_percentage,
            'seller_feedback_score' => $seller_feedback_score,
            'brand' => $brand,
            'returns_accepted' => $returns_accepted,
            'qualified_programs' => $qualified_programs,
            'item_created_at' => $created_at,
            'title' => $title,
            'short_description' => sanitize_textarea_field((string) ($item['shortDescription'] ?? '')),
            'condition_text' => sanitize_text_field((string) ($item['condition'] ?? '')),
            'price_value' => $price_value,
            'currency' => $currency,
            'shipping_value' => $shipping_value,
            'location_text' => implode(', ', $location),
            'affiliate_url' => $affiliate_url,
            'item_web_url' => $item_web_url,
            'image_url' => $image_url,
            'item_end_at' => $end_at,
            'buying_options' => $buying_options,
            'category_ids' => array_values(array_filter(array_map('sanitize_text_field', array_map(static function($category){ return is_array($category) ? (string) ($category['categoryId'] ?? '') : ''; }, (array) ($item['categories'] ?? array()))))),
            'category_names' => array_values(array_filter(array_map('sanitize_text_field', array_map(static function($category){ return is_array($category) ? (string) ($category['categoryName'] ?? '') : ''; }, (array) ($item['categories'] ?? array()))))),
            'raw' => $item,
        );
        $fingerprint = $normalized;
        unset($fingerprint['raw']);
        $normalized['source_hash'] = hash('sha256', wp_json_encode($fingerprint, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES));
        return $normalized;
    }


    /** V6.19 – editoriale Feinsteuerung bleibt innerhalb des bestehenden eBay-Moduls. */
    private function ebay_business_curation_state() {
        $option_key = defined(static::class . '::OPTION_EBAY_CURATION') ? constant(static::class . '::OPTION_EBAY_CURATION') : 'ppar_ebay_curation_v1';
        $state = get_option($option_key, array());
        $state = is_array($state) ? $state : array();
        foreach (array('items','sellers','brands','learned_heads') as $key) {
            if (!isset($state[$key]) || !is_array($state[$key])) { $state[$key] = array(); }
        }
        $state['version'] = '1.0';
        return $state;
    }

    private function ebay_business_curation_save($state) {
        $state = is_array($state) ? $state : array();
        foreach (array('items','sellers','brands','learned_heads') as $key) {
            if (!isset($state[$key]) || !is_array($state[$key])) { $state[$key] = array(); }
        }
        $state['version'] = '1.0';
        $option_key = defined(static::class . '::OPTION_EBAY_CURATION') ? constant(static::class . '::OPTION_EBAY_CURATION') : 'ppar_ebay_curation_v1';
        update_option($option_key, $state, false);
        return $state;
    }

    private function ebay_business_curation_key($value) {
        return sanitize_key($this->ebay_topic_text((string) $value));
    }

    private function ebay_business_wrong_product_head_tokens() {
        $catalog = $this->ebay_portal_catalog();
        if (!is_wp_error($catalog)) {
            $policy = is_array($catalog['content_policy'] ?? null) ? $catalog['content_policy'] : array();
            $terms = array_values(array_unique(array_filter(array_map(array($this, 'ebay_topic_text'), (array)($policy['blocked_primary_product_terms'] ?? array())))));
            if ($terms) { return $terms; }
        }
        // Fail-safe only if the catalog cannot be loaded; normal operation uses
        // one catalog-driven policy source for both seller routes.
        return array(
            'aufkleber','sticker','spardose','sparschwein','poster','plakat','tasse','becher','figur','figurine','deko','dekoration',
            'kalender','postkarte','patch','aufnaeher','aufnaher','schluesselanhaenger','schlusselanhanger','keychain','kostuem','kostum',
            'handyhulle','handyhuelle','miniatur','modellauto','modellpferd','brosche'
        );
    }

    private function ebay_business_title_head_token($title) {
        $normalized_title = $this->ebay_topic_text((string) $title);
        $raw_title_tokens = preg_split('/\s+/', $normalized_title);
        $first_title_token = sanitize_key((string) ($raw_title_tokens[0] ?? ''));
        $primary = $this->ebay_business_primary_title_section((string) $title);
        // For "Sperren + lernen", prefer the actual false-product noun over
        // incidental leading words/brands (e.g. "Alter Aufkleber ..." learns
        // "aufkleber", never the dangerously broad token "alter"). A false
        // product noun that itself opens a compatibility boundary ("Ersatzteil
        // Reitstiefel ...") must still be learnable instead of collapsing to an
        // empty title head.
        foreach ($this->ebay_business_wrong_product_head_tokens() as $wrong_head) {
            if ($first_title_token !== '' && $this->ebay_business_strict_token_present($first_title_token, $wrong_head)) { return sanitize_key($wrong_head); }
            if ($this->ebay_business_strict_token_present($primary, $wrong_head)) { return sanitize_key($wrong_head); }
        }
        foreach ($this->ebay_topic_tokens($primary) as $token) {
            $token = sanitize_key($this->ebay_topic_text((string) $token));
            if ($token === '' || strlen($token) < 4) { continue; }
            if (in_array($token, array('neu','new','original','premium','profi','xxl','xl','set','paar','damen','herren','kinder','horse','pferd','pferde','alter','alte','altes','antik','antike','vintage'), true)) { continue; }
            return $token;
        }
        return '';
    }

    private function ebay_business_curation_decision($item, $classification) {
        $state = $this->ebay_business_curation_state();
        $item_id = sanitize_text_field((string) ($item['item_id'] ?? ''));
        $seller_key = $this->ebay_business_curation_key((string) ($item['seller_username'] ?? ''));
        $brand_key = $this->ebay_business_curation_key((string) ($item['brand'] ?? ''));
        $concept_id = sanitize_key((string) ($classification['product_concept_id'] ?? ''));
        $head = $this->ebay_business_title_head_token((string) ($item['title'] ?? ''));
        $item_rule = is_array($state['items'][$item_id] ?? null) ? $state['items'][$item_id] : array();
        $seller_rule = $seller_key !== '' && is_array($state['sellers'][$seller_key] ?? null) ? $state['sellers'][$seller_key] : array();
        $brand_rule = $brand_key !== '' && is_array($state['brands'][$brand_key] ?? null) ? $state['brands'][$brand_key] : array();
        $learned = ($concept_id !== '' && $head !== '' && is_array($state['learned_heads'][$concept_id][$head] ?? null)) ? $state['learned_heads'][$concept_id][$head] : array();
        return array(
            'item_status'=>sanitize_key((string) ($item_rule['status'] ?? 'automatic')),
            'item_reason'=>sanitize_text_field((string) ($item_rule['reason'] ?? '')),
            'seller_status'=>sanitize_key((string) ($seller_rule['status'] ?? 'automatic')),
            'seller_reason'=>sanitize_text_field((string) ($seller_rule['reason'] ?? '')),
            'brand_status'=>sanitize_key((string) ($brand_rule['status'] ?? 'automatic')),
            'brand_reason'=>sanitize_text_field((string) ($brand_rule['reason'] ?? '')),
            'learned_block'=>!empty($learned),
            'learned_reason'=>sanitize_text_field((string) ($learned['reason'] ?? '')),
            'pinned'=>sanitize_key((string) ($item_rule['status'] ?? '')) === 'pinned',
            'brand_preferred'=>sanitize_key((string) ($brand_rule['status'] ?? '')) === 'preferred',
            'head'=>$head,
        );
    }

    /**
     * Harte Produktart-Vorauswahl. Ein Bezugswort im Titel darf nicht genügen:
     * Spardose/Aufkleber/Poster etc. werden vor dem Ranking blockiert.
     */
    private function ebay_business_relevance_report($item, $classification, $rule) {
        $catalog = $this->ebay_portal_catalog();
        if (is_wp_error($catalog)) { return $catalog; }
        $concept_id = sanitize_key((string) ($classification['product_concept_id'] ?? ''));
        $concept = array();
        foreach (array('business_concepts','business_hub_concepts') as $field) {
            foreach ((array) ($catalog[$field] ?? array()) as $candidate) {
                if (is_array($candidate) && sanitize_key((string) ($candidate['id'] ?? '')) === $concept_id) { $concept = $candidate; break 2; }
            }
        }
        if (!$concept) { return new WP_Error('ebay_business_quality_concept_missing', 'Produktkonzept für Qualitätsprüfung fehlt.'); }
        $sections = $this->ebay_business_evidence_sections($item);
        if ($concept_id === 'concept-reitstiefel') {
            $primary_boot = $this->ebay_business_primary_title_section((string)($sections['title'] ?? ''));
            $structured_boot = $this->ebay_topic_text(trim((string)($sections['category'] ?? '') . ' ' . (string)($sections['product_type'] ?? '') . ' ' . (string)($sections['aspects'] ?? '')));
            $blocked_boot_heads = array('socke','socken','strumpf','struempfe','stiefeltasche','tasche','beutel','pflege','pflegemittel','pflegeset','schuhpflege','stiefelpflege','ersatzteil','zubehoer','accessory','miniatur','modell','spielzeug','figur','anhaenger','schluesselanhaenger');
            foreach ($blocked_boot_heads as $blocked_boot) {
                if ($this->ebay_business_strict_token_present($primary_boot, $blocked_boot)) {
                    return new WP_Error('ebay_business_reitstiefel_wrong_product', 'Reitstiefel-Sentinel: Titel beschreibt Zubehör/Pflege/Socken/Modell statt eines tragbaren Reitstiefels.');
                }
            }
            foreach (array('tasche','bag','socke','socks','pflege','care','accessory','zubehoer','toy','spielzeug','figur','miniatur','modell') as $blocked_structured) {
                if ($this->ebay_business_strict_token_present($structured_boot, $blocked_structured)
                    && !$this->ebay_business_strict_token_present($structured_boot, 'reitstiefel')
                    && !$this->ebay_business_strict_token_present($structured_boot, 'riding boot')) {
                    return new WP_Error('ebay_business_reitstiefel_wrong_product', 'Reitstiefel-Sentinel: eBay-Produktart bestätigt kein tragbares Reitstiefel-Produkt.');
                }
            }
            $direct_boot = false;
            foreach (array('reitstiefel','lederreitstiefel','dressurstiefel','reitgummistiefel','riding boot','equestrian boot') as $boot_term) {
                if ($this->ebay_business_strict_token_present($primary_boot, $boot_term)
                    || $this->ebay_business_strict_token_present($structured_boot, $boot_term)) { $direct_boot = true; break; }
            }
            if (!$direct_boot) {
                return new WP_Error('ebay_business_reitstiefel_identity_unconfirmed', 'Reitstiefel-Sentinel: reale Angebotsdaten bestätigen die Produktidentität Reitstiefel nicht.');
            }
        }
        $full_title = $this->ebay_topic_text((string) ($sections['title'] ?? ''));
        $full_title_tokens = preg_split('/\s+/', $full_title);
        $first_title_token = sanitize_key((string) ($full_title_tokens[0] ?? ''));
        $primary = $this->ebay_business_primary_title_section((string) ($sections['title'] ?? ''));
        $blocked_heads = $this->ebay_business_wrong_product_head_tokens();
        foreach ($blocked_heads as $blocked) {
            if (($first_title_token !== '' && $this->ebay_business_strict_token_present($first_title_token, $blocked))
                || $this->ebay_business_strict_token_present($primary, $blocked)) {
                return new WP_Error('ebay_business_wrong_product_head', 'Titel beschreibt primär „' . sanitize_text_field($blocked) . '“ statt des erwarteten Produkts.');
            }
        }
        $concept_primary = $this->ebay_business_primary_title_section((string) ($concept['title'] ?? ''));
        $tokens = $this->ebay_business_distinctive_tokens($concept_primary !== '' ? $concept_primary : (string) ($concept['title'] ?? ''));
        if (!$tokens) { return new WP_Error('ebay_business_quality_tokens_missing', 'Produktkonzept besitzt keine belastbaren Produkttokens.'); }
        $title_tokens = $this->ebay_topic_tokens($primary);
        $first_tokens = array_slice(array_values($title_tokens), 0, 4);
        $first_text = implode(' ', $first_tokens);
        $head_hits = 0; $structured_hits = 0; $all_title_hits = 0;
        foreach ($tokens as $token) {
            if ($this->ebay_business_strict_token_present($first_text, $token)) { $head_hits++; }
            if ($this->ebay_business_strict_token_present($sections['title'], $token)) { $all_title_hits++; }
            if ($this->ebay_business_strict_token_present($sections['category'], $token)
                || $this->ebay_business_strict_token_present($sections['aspects'], $token)
                || $this->ebay_business_strict_token_present($sections['product_type'], $token)) { $structured_hits++; }
        }
        // One distinctive product token in the title head is sufficient after
        // the strict concept classifier has already passed. Structured eBay facts
        // are the independent corroboration when the concept is mentioned only
        // later in a marketing/reference title. This stays broad enough for real
        // brand/model titles while blocking Spardose/Aufkleber-style false matches.
        $required = 1;
        if ($all_title_hits < 1 && $structured_hits < 1) {
            return new WP_Error('ebay_business_relevance_unconfirmed', 'Produktart wird weder im Titel noch in eBay-Kategorie/Produktmerkmalen bestätigt.');
        }
        if ($head_hits < 1 && $structured_hits < 1) {
            return new WP_Error('ebay_business_reference_only_match', 'Produktbegriff erscheint nur als spätere Referenz; eBay-Kategorie/Produktmerkmale bestätigen die Produktart nicht.');
        }
        $classification_score = max(0, min(100, absint($classification['score'] ?? 0)));
        $relevance = $classification_score;
        if ($structured_hits >= $required) { $relevance += 6; }
        if ($head_hits >= $required) { $relevance += 5; }
        if ($head_hits >= 1 && $structured_hits >= 1) { $relevance += 4; }
        return array(
            'score'=>max(0, min(100, $relevance)),
            'head_hits'=>$head_hits,'structured_hits'=>$structured_hits,'title_hits'=>$all_title_hits,'required'=>$required,
            'concept_id'=>$concept_id,
        );
    }

    private function ebay_business_seller_quality_score($item, $settings) {
        $pct = (float) ($item['seller_feedback_percentage'] ?? -1);
        $count = (int) ($item['seller_feedback_score'] ?? -1);
        $min_pct = (float) ($settings['business_min_feedback_percentage'] ?? 99.0);
        $min_count = absint($settings['business_min_feedback_score'] ?? 100);
        if ($pct < $min_pct || $count < $min_count) { return 0; }
        $preferred_pct = (float) ($settings['business_preferred_feedback_percentage'] ?? 99.5);
        $preferred_count = absint($settings['business_preferred_feedback_score'] ?? 500);
        $pct_score = $pct >= 99.9 ? 100 : ($pct >= $preferred_pct ? 90 : 72 + (int) round((($pct - $min_pct) / max(0.01, $preferred_pct - $min_pct)) * 18));
        $volume_score = $count >= 5000 ? 100 : ($count >= 1000 ? 94 : ($count >= $preferred_count ? 88 : 70 + (int) round((($count - $min_count) / max(1, $preferred_count - $min_count)) * 18)));
        return max(0, min(100, (int) round(($pct_score * 0.65) + ($volume_score * 0.35))));
    }

    private function ebay_business_offer_quality_score($item) {
        $score = 62;
        if (!empty($item['returns_accepted'])) { $score += 12; }
        $shipping = (string) ($item['shipping_value'] ?? '');
        if ($shipping !== '' && is_numeric($shipping) && (float) $shipping <= 0.01) { $score += 8; }
        if (in_array('FIXED_PRICE', (array) ($item['buying_options'] ?? array()), true) || in_array('BUY_IT_NOW', (array) ($item['buying_options'] ?? array()), true)) { $score += 6; }
        if (stripos((string) ($item['condition_text'] ?? ''), 'neu') !== false || stripos((string) ($item['condition_text'] ?? ''), 'new') !== false) { $score += 4; }
        foreach ((array) ($item['qualified_programs'] ?? array()) as $program) { if (strpos((string) $program, 'plus') !== false) { $score += 4; break; } }
        $created = absint($item['item_created_at'] ?? 0);
        if ($created > 0) {
            $age = max(0, time() - $created);
            if ($age <= 30 * DAY_IN_SECONDS) { $score += 4; }
            elseif ($age <= 90 * DAY_IN_SECONDS) { $score += 2; }
        }
        return max(0, min(100, $score));
    }

    private function ebay_business_price_plausibility_score($price, $median) {
        $price = (float) $price; $median = (float) $median;
        if ($price <= 0 || $median <= 0) { return 50; }
        $ratio = $price / $median;
        if ($ratio >= 0.60 && $ratio <= 1.65) { return 100; }
        if ($ratio >= 0.40 && $ratio <= 2.25) { return 82; }
        if ($ratio >= 0.25 && $ratio <= 3.00) { return 65; }
        if ($ratio >= 0.15 && $ratio <= 4.50) { return 45; }
        return 20;
    }

    private function ebay_business_quality_assess($item, $classification, $rule, $settings, $median_price = 0.0) {
        $item = is_array($item) ? $item : array();
        $classification = is_array($classification) ? $classification : array();
        $settings = is_array($settings) ? $settings : $this->ebay_settings();
        $curation = $this->ebay_business_curation_decision($item, $classification);
        if ($curation['item_status'] === 'blocked') { return new WP_Error('ebay_business_item_veto', $curation['item_reason'] !== '' ? $curation['item_reason'] : 'Produkt wurde manuell gesperrt.'); }
        if ($curation['seller_status'] === 'blocked') { return new WP_Error('ebay_business_seller_veto', $curation['seller_reason'] !== '' ? $curation['seller_reason'] : 'Verkäufer wurde manuell gesperrt.'); }
        if ($curation['brand_status'] === 'blocked') { return new WP_Error('ebay_business_brand_veto', $curation['brand_reason'] !== '' ? $curation['brand_reason'] : 'Marke wurde manuell gesperrt.'); }
        if (!empty($curation['learned_block'])) { return new WP_Error('ebay_business_learned_pattern_block', $curation['learned_reason'] !== '' ? $curation['learned_reason'] : 'Gelernte Fehlproduktklasse wurde erkannt.'); }
        $relevance = $this->ebay_business_relevance_report($item, $classification, $rule);
        if (is_wp_error($relevance)) { return $relevance; }
        $seller_score = $this->ebay_business_seller_quality_score($item, $settings);
        if ($seller_score <= 0) { return new WP_Error('ebay_business_seller_quality_failed', 'Verkäuferqualität erfüllt die automatische Mindestfreigabe nicht.'); }
        $offer_score = $this->ebay_business_offer_quality_score($item);
        $price_score = $this->ebay_business_price_plausibility_score((float) ($item['price_value'] ?? 0), (float) $median_price);
        $brand_bonus = !empty($curation['brand_preferred']) ? 5 : 0;
        $overall = (int) round(($relevance['score'] * 0.50) + ($seller_score * 0.25) + ($offer_score * 0.15) + ($price_score * 0.10));
        $overall = max(0, min(100, $overall + $brand_bonus));
        return array(
            'overall'=>$overall,'relevance'=>absint($relevance['score']),'seller'=>$seller_score,'offer'=>$offer_score,'price'=>$price_score,
            'brand_bonus'=>$brand_bonus,'pinned'=>!empty($curation['pinned']),'brand_preferred'=>!empty($curation['brand_preferred']),
            'seller_feedback_percentage'=>(float) ($item['seller_feedback_percentage'] ?? 0),'seller_feedback_score'=>absint($item['seller_feedback_score'] ?? 0),
            'seller_username'=>sanitize_text_field((string) ($item['seller_username'] ?? '')),'brand'=>sanitize_text_field((string) ($item['brand'] ?? '')),
            'concept_id'=>sanitize_key((string) ($classification['product_concept_id'] ?? '')),
            'reason'=>'Relevanz ' . absint($relevance['score']) . ' · Verkäufer ' . absint($seller_score) . ' · Angebot ' . absint($offer_score) . ' · Preis ' . absint($price_score) . (!empty($curation['pinned']) ? ' · angepinnt' : '') . (!empty($curation['brand_preferred']) ? ' · bevorzugte Marke' : ''),
        );
    }

    private function ebay_business_item_with_quality($item, $quality) {
        $item = is_array($item) ? $item : array();
        $item['business_quality'] = is_array($quality) ? $quality : array();
        return $item;
    }

    private function ebay_business_source_row_item($row, $settings) {
        $row = is_array($row) ? $row : array();
        $payload = json_decode((string) ($row['source_payload'] ?? ''), true);
        $payload = is_array($payload) ? $payload : array();
        $raw = is_array($payload['raw'] ?? null) ? $payload['raw'] : array();
        if (!$raw) { return new WP_Error('ebay_business_source_raw_missing', 'Gespeicherter eBay-Rohdatensatz fehlt.'); }
        $item = $this->ebay_accept_item($raw, 'BUSINESS', $settings);
        if (is_wp_error($item)) { return $item; }
        $classification = is_array($payload['portal_classification'] ?? null) ? $payload['portal_classification'] : array();
        if (!$classification) {
            $rule = $this->ebay_rule_by_id((string) ($row['rule_id'] ?? ''), $settings);
            $classification = $this->ebay_business_classify_portal_item_strict($item, $rule);
            if (is_wp_error($classification)) { return $classification; }
        }
        $item['portal_classification'] = $classification;
        return $item;
    }

    /**
     * Durable internal BUSINESS selection commit. Public output_state is owned by
     * the materialization route and MUST NOT be replaced by an internal role.
     * The write is read back and verified; any storage anomaly fails closed.
     */
    private function ebay_business_commit_selected_source_role($row, $quality, $role = 'active_selected', $rank = 0) {
        $row = is_array($row) ? $row : array();
        $id = absint($row['id'] ?? 0);
        if ($id <= 0) { return new WP_Error('business_selection_commit_failed', 'BUSINESS-Quellzeile fuer den verifizierten Auswahlcommit fehlt.'); }
        global $wpdb;
        if (!is_object($wpdb) || !method_exists($wpdb, 'get_row') || !method_exists($wpdb, 'update') || !method_exists($wpdb, 'prepare')) {
            return new WP_Error('business_selection_commit_failed', 'BUSINESS-Auswahlcommit kann nicht verifiziert gespeichert werden: Storage nicht verfuegbar.');
        }
        $table = $this->ebay_items_table();
        $current = $wpdb->get_row($wpdb->prepare("SELECT * FROM {$table} WHERE id=%d", $id), ARRAY_A);
        if (!is_array($current)) { return new WP_Error('business_selection_commit_failed', 'BUSINESS-Quellzeile ist beim Auswahlcommit nicht mehr vorhanden.'); }
        $before_output = sanitize_key((string)($current['output_state'] ?? ''));
        // Selection is an internal role layered on top of an already materialized
        // public winner. Fail closed unless that authoritative public state is
        // exactly creative_ready; this helper never writes output_state itself.
        if ($before_output !== 'creative_ready') {
            return new WP_Error('business_selection_commit_failed', 'BUSINESS-Auswahlcommit verweigert: oeffentlicher Zustand ist nicht creative_ready.');
        }
        $payload = json_decode((string)($current['source_payload'] ?? ''), true);
        $payload = is_array($payload) ? $payload : array();
        $payload['business_quality'] = is_array($quality) ? $quality : array();
        $payload['business_selection'] = array(
            'role'=>sanitize_key((string)$role),
            'rank'=>absint($rank),
            'updated_at'=>time(),
        );
        $written = $wpdb->update(
            $table,
            array(
                'source_payload'=>wp_json_encode($payload, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES),
                'updated_at'=>time(),
            ),
            array('id'=>$id),
            array('%s','%d'),
            array('%d')
        );
        if ($written === false) {
            return new WP_Error('business_selection_commit_failed', 'BUSINESS-Auswahlrolle konnte nicht gespeichert werden.');
        }
        $fresh = $wpdb->get_row($wpdb->prepare("SELECT * FROM {$table} WHERE id=%d", $id), ARRAY_A);
        if (!is_array($fresh)) { return new WP_Error('business_selection_commit_failed', 'BUSINESS-Auswahlcommit konnte nicht zur Verifikation zurueckgelesen werden.'); }
        $fresh_payload = json_decode((string)($fresh['source_payload'] ?? ''), true);
        $fresh_payload = is_array($fresh_payload) ? $fresh_payload : array();
        $fresh_role = sanitize_key((string)($fresh_payload['business_selection']['role'] ?? ''));
        $fresh_rank = absint($fresh_payload['business_selection']['rank'] ?? 0);
        $fresh_output = sanitize_key((string)($fresh['output_state'] ?? ''));
        if ($fresh_role !== sanitize_key((string)$role) || $fresh_rank !== absint($rank)) {
            return new WP_Error('business_selection_commit_failed', 'BUSINESS-Auswahlrolle ist nach dem Speichern nicht verifizierbar.');
        }
        if ($fresh_output !== 'creative_ready' || $fresh_output !== $before_output) {
            return new WP_Error('business_selection_commit_failed', 'Interner BUSINESS-Auswahlcommit hat den oeffentlichen creative_ready-Zustand veraendert.');
        }
        return true;
    }

    private function ebay_business_persist_quality_on_source_row($row, $quality, $role = 'candidate', $rank = 0) {
        $row = is_array($row) ? $row : array();
        $id = absint($row['id'] ?? 0); if ($id <= 0) { return false; }
        $payload = json_decode((string) ($row['source_payload'] ?? ''), true);
        $payload = is_array($payload) ? $payload : array();
        $payload['business_quality'] = is_array($quality) ? $quality : array();
        $payload['business_selection'] = array('role'=>sanitize_key((string) $role),'rank'=>absint($rank),'updated_at'=>time());
        global $wpdb;
        $wpdb->update($this->ebay_items_table(), array(
            'source_payload'=>wp_json_encode($payload, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES),
            'output_state'=>sanitize_key((string) $role),
            'updated_at'=>time(),
        ), array('id'=>$id), array('%s','%s','%d'), array('%d'));
        return true;
    }


    /** V6.19 – capacity pause keeps the verified creative contract intact. */
    private function ebay_business_pause_output_for_capacity($row, $role = 'candidate', $reason = '') {
        $row = is_array($row) ? $row : array();
        $role = sanitize_key((string) $role);
        $reason = sanitize_text_field((string) $reason);
        if ($reason === '') { $reason = 'V6.19 Qualitäts-/Kapazitätsauswahl: derzeit nicht unter den aktiven Top-Produkten.'; }
        $hash = strtolower(sanitize_text_field((string) ($row['creative_identity_hash'] ?? '')));
        if (preg_match('/^[a-f0-9]{64}$/', $hash) && method_exists($this, 'output_objects_table')) {
            global $wpdb;
            $table = $this->output_objects_table();
            $objects = (array) $wpdb->get_results($wpdb->prepare(
                "SELECT * FROM {$table} WHERE creative_identity_hash=%s AND output_type='product_campaign'",
                $hash
            ), ARRAY_A);
            foreach ($objects as $object) {
                if (method_exists($this, 'output_deactivate_materialized_object')) {
                    $this->output_deactivate_materialized_object($object, $reason);
                }
            }
            $wpdb->update($table, array(
                'status'=>'review','decision_source'=>'ebay_business_quality_selection','decision_reason'=>$reason,
                'last_verified'=>time(),'updated_at'=>time(),
            ), array('creative_identity_hash'=>$hash,'output_type'=>'product_campaign'));
        }
        global $wpdb;
        if (absint($row['id'] ?? 0) > 0) {
            $wpdb->update($this->ebay_items_table(), array(
                'output_state'=>$role,'status'=>'active','source_state'=>'available','policy_state'=>'allowed','route_state'=>'ready',
                'rejection_reason'=>'','updated_at'=>time(),
            ), array('id'=>absint($row['id'])), $this->ebay_db_formats(array(
                'output_state'=>$role,'status'=>'active','source_state'=>'available','policy_state'=>'allowed','route_state'=>'ready',
                'rejection_reason'=>'','updated_at'=>time(),
            )), array('%d'));
        }
        return true;
    }

    private function ebay_business_candidate_sort(&$rows) {
        usort($rows, static function($a, $b) {
            $aq = is_array($a['quality'] ?? null) ? $a['quality'] : array();
            $bq = is_array($b['quality'] ?? null) ? $b['quality'] : array();
            foreach (array('pinned','overall','relevance','seller','offer','price') as $key) {
                $av = $key === 'pinned' ? (!empty($aq[$key]) ? 1 : 0) : (int) ($aq[$key] ?? 0);
                $bv = $key === 'pinned' ? (!empty($bq[$key]) ? 1 : 0) : (int) ($bq[$key] ?? 0);
                if ($av !== $bv) { return $av > $bv ? -1 : 1; }
            }
            $al = absint($a['row']['last_seen'] ?? 0); $bl = absint($b['row']['last_seen'] ?? 0);
            if ($al !== $bl) { return $al > $bl ? -1 : 1; }
            return strcmp((string) ($a['row']['item_id'] ?? ''), (string) ($b['row']['item_id'] ?? ''));
        });
    }


    /** V6.20 shared bounded selection state; reuses the existing eBay worker hook. */
    private function ebay_selection_option_key() {
        $constant = static::class . '::OPTION_EBAY_SELECTION_STATE';
        return defined($constant) ? (string) constant($constant) : 'ppar_ebay_selection_state_v2';
    }

    private function ebay_selection_state_load() {
        if (method_exists($this, 'ebay_run_phase_state_load')) {
            $run = method_exists($this, 'ebay_run_load') ? $this->ebay_run_load() : array();
            if ((string)($run['schema'] ?? '') === '1.0') {
                $state = $this->ebay_run_phase_state_load('selection');
                return is_array($state) ? $state : array();
            }
        }
        $state = get_option($this->ebay_selection_option_key(), array());
        return is_array($state) ? $state : array();
    }

    private function ebay_selection_state_save($state) {
        $state = is_array($state) ? $state : array();
        $state['version'] = '2.0';
        $state['updated_at'] = time();
        if (method_exists($this, 'ebay_run_load') && (string)(($this->ebay_run_load())['schema'] ?? '') === '1.0') {
            $this->ebay_run_phase_state_save('selection', $state);
        } else {
            update_option($this->ebay_selection_option_key(), $state, false);
        }
        return $state;
    }

    private function ebay_selection_state_is_open($state = null) {
        if (!is_array($state)) { $state = $this->ebay_selection_state_load(); }
        return in_array(sanitize_key((string)($state['status'] ?? '')), array('pending','preparing','running'), true);
    }

    private function ebay_selection_schedule_worker($delay = 10) {
        if (method_exists($this, 'ebay_run_load') && (string)(($this->ebay_run_load())['schema'] ?? '') === '1.0') { return true; }
        if (!function_exists('wp_next_scheduled') || !function_exists('wp_schedule_single_event')) { return false; }
        if (!wp_next_scheduled(self::EBAY_WORKER_HOOK)) {
            wp_schedule_single_event(time() + max(10, absint($delay)), self::EBAY_WORKER_HOOK);
        }
        return true;
    }

    /** Token for the authenticated non-blocking standalone selection loopback. */
    private function ebay_selection_worker_token() {
        if (function_exists('wp_generate_password')) { return wp_generate_password(48, false, false); }
        return hash('sha256', microtime(true) . '|' . mt_rand() . '|' . uniqid('', true));
    }

    /**
     * V6.21 deterministic transport for the already-existing bounded selection
     * worker. WP-Cron remains a fallback only. Sync-owned selection is still
     * driven by the discovery worker and is never duplicated here.
     */
    private function ebay_selection_dispatch_worker($state = null, $force = false) {
        $state = is_array($state) ? $state : $this->ebay_selection_state_load();
        if (!$this->ebay_selection_state_is_open($state)) { return false; }
        // Controlled rebuild: exactly one transport owns standalone selection.
        // Queue the shared background worker only. No self-HTTP loopback and no
        // browser tick are launched from here.
        return $this->ebay_selection_schedule_worker($force ? 10 : 15);
    }

    /**
     * Queue a fresh selection/cap pass without doing any heavy work in the
     * caller request. This is used by refresh/maintenance/admin actions.
     */
    private function ebay_selection_request($reason = 'selection', $owner = 'system', $force = false, $scope = '') {
        $current = $this->ebay_selection_state_load();
        // Global invariant: an open selection state can never be reset/replaced.
        // 'force' may request a fresh terminal-to-new transition, but it never
        // destroys progress of a pending/preparing/running owner.
        if ($this->ebay_selection_state_is_open($current)) {
            $this->ebay_selection_schedule_worker(10);
            return $current;
        }
        $scope = sanitize_key((string)$scope);
        if (!in_array($scope, array('all','private','business'), true)) {
            return array('status'=>'failed','failure_reason'=>'invalid_selection_scope','selection_scope'=>$scope);
        }
        $recovery_build = (string)($current['recovery_build'] ?? '');
        $state = array(
            'version'=>'2.0',
            'status'=>'pending',
            'reason'=>sanitize_key((string)$reason),
            'owner'=>sanitize_text_field((string)$owner),
            'selection_scope'=>$scope,
            'recovery_build'=>$recovery_build,
            'worker_token'=>$this->ebay_selection_worker_token(),
            'last_dispatch_at'=>0,
            'started_at'=>time(),
            'prepared_at'=>0,
            'completed_at'=>0,
            'phase'=>'prepare',
            'business_cursor'=>0,
            'private_cursor'=>0,
            'private_post_sweep'=>0,
            'private_post_cursor'=>0,
            'business_active'=>array(),
            'business_reserve'=>array(),
            'private_active'=>array(),
            'private_active_row_ids'=>array(),
            'private_selected_offset'=>0,
            'private_keep_posts'=>array(),
            'worker_no_progress_count'=>0,
            'worker_last_progress_at'=>0,
            'stats'=>array(
                'business'=>array('scanned'=>0,'active'=>0,'reserve'=>0,'candidate'=>0,'deactivated'=>0,'materialized'=>0,'errors'=>array()),
                'private'=>array('scanned'=>0,'active'=>0,'reserved'=>0,'materialized'=>0,'errors'=>array()),
            ),
        );
        $this->ebay_selection_state_save($state);
        $owner_text = (string)$state['owner'];
        if (strpos($owner_text, 'sync:') === 0) {
            $this->ebay_selection_schedule_worker(10);
        } else {
            $this->ebay_selection_dispatch_worker($state, true);
        }
        return $state;
    }

    /**
     * Bounded BUSINESS candidates for exactly one durable product identity.
     *
     * This is deliberately concept-scoped. The old global LIMIT 5000 plan did
     * two unsafe things at once: high-volume concepts could crowd rare concepts
     * out of the recency window, and every one of those rows was then subjected
     * to the expensive acceptance/relevance/quality path in one request. On a
     * real WordPress host that can time out while the durable selection state is
     * already "preparing", causing every subsequent browser/cron tick to repeat
     * the same monolithic work forever.
     *
     * rule_id is the durable product-concept identity for BUSINESS discovery.
     * The schema carries an index for this exact lookup. Each concept query is
     * hard-bounded and the prepare state processes only a small number of
     * concepts per worker tick.
     */
    /**
     * Public-fresh source eligibility shared by BUSINESS selection/materialisation.
     *
     * V6.46 closes a contract gap exposed by a long-lived canonical run: the
     * selector previously accepted rows whose six-hour source freshness had
     * already expired while the public coverage gate correctly rejected those
     * same rows. Internal materialisation could therefore rise while public
     * coverage stayed at zero. Selection must never create or preserve a winner
     * that the immediately following public gate is guaranteed to reject.
     */
    private function ebay_business_source_row_is_public_fresh($row, $now = null) {
        $row = is_array($row) ? $row : array();
        $now = $now === null ? time() : absint($now);
        if (array_key_exists('source_state', $row) && sanitize_key((string)$row['source_state']) !== 'available') { return false; }
        if (array_key_exists('policy_state', $row) && sanitize_key((string)$row['policy_state']) !== 'allowed') { return false; }
        if (array_key_exists('route_state', $row) && !in_array(sanitize_key((string)$row['route_state']), array('ready','review_last_good'), true)) { return false; }
        // Real DB rows always carry fresh_until. Legacy unit fixtures that omit
        // the column are not reinterpreted here; the SQL production path still
        // requires a concrete fresh_until > now value.
        if (array_key_exists('fresh_until', $row) && absint($row['fresh_until']) <= $now) { return false; }
        $end = absint($row['item_end_at'] ?? 0);
        if ($end > 0 && $end <= $now) { return false; }
        return true;
    }

    private function ebay_business_selection_concept_rows($concept_id, $settings = null) {
        $settings = is_array($settings) ? $settings : $this->ebay_settings();
        $concept_id = sanitize_key((string)$concept_id);
        if ($concept_id === '') { return array(); }
        global $wpdb;
        if (!is_object($wpdb) || !method_exists($wpdb, 'get_results') || !method_exists($wpdb, 'prepare')) { return array(); }
        $pool_limit = max(5, min(20, absint($settings['business_candidate_pool_per_concept'] ?? 10)));
        $reserve_limit = max(0, min(10, absint($settings['business_reserve_per_concept'] ?? 2)));
        $query_limit = max(8, min(30, $pool_limit + $reserve_limit + 5));
        $table = $this->ebay_items_table();
        $now = time();
        return (array)$wpdb->get_results($wpdb->prepare(
            "SELECT * FROM {$table} WHERE seller_account_type='BUSINESS' AND rule_id=%s AND source_state='available' AND policy_state='allowed' AND route_state IN ('ready','review_last_good') AND fresh_until>%d AND (item_end_at=0 OR item_end_at>%d) AND policy_version=%s AND classifier_version=%s ORDER BY last_seen DESC,id DESC LIMIT %d",
            $concept_id,
            $now,
            $now,
            self::EBAY_CONTENT_POLICY_VERSION,
            self::EBAY_BUSINESS_CLASSIFIER_VERSION,
            $query_limit
        ), ARRAY_A);
    }

    /** Pure plan for one BUSINESS product concept. No source/campaign mutation. */
    private function ebay_business_selection_plan_concept($concept_id, $settings = null) {
        $settings = is_array($settings) ? $this->ebay_normalize_settings($settings, true) : $this->ebay_settings();
        $concept_id = sanitize_key((string)$concept_id);
        $plan = array('active'=>array(),'reserve'=>array(),'scanned'=>0,'blocked'=>0,'pool'=>0,'concepts'=>0);
        if ($concept_id === '') { return $plan; }
        $rows = $this->ebay_business_selection_concept_rows($concept_id, $settings);
        $now = time(); $group = array();
        foreach ($rows as $row) {
            if (!is_array($row)) { continue; }
            // Defense in depth for test doubles and storage anomalies: the
            // expensive source/quality path is concept-local even if a DB layer
            // ignores or mis-plans the WHERE rule_id predicate.
            if (sanitize_key((string)($row['rule_id'] ?? '')) !== $concept_id) { continue; }
            $plan['scanned']++;
            // Defense in depth: even if a DB/test layer ignores the SQL freshness
            // predicate, a stale source can never enter an active BUSINESS plan.
            if (!$this->ebay_business_source_row_is_public_fresh($row, $now)) { $plan['blocked']++; continue; }
            $item = $this->ebay_business_source_row_item($row, $settings);
            if (is_wp_error($item)) { $plan['blocked']++; continue; }
            $classification = (array)($item['portal_classification'] ?? array());
            $actual_concept = sanitize_key((string)($classification['product_concept_id'] ?? ''));
            // Durable rule identity and verified payload identity must agree.
            if ($actual_concept === '' || !hash_equals($concept_id, $actual_concept)) { $plan['blocked']++; continue; }
            $rule = $this->ebay_rule_by_id((string)($row['rule_id'] ?? ''), $settings);
            $quality = $this->ebay_business_quality_assess($item, $classification, $rule, $settings, 0.0);
            if (is_wp_error($quality)) { $plan['blocked']++; continue; }
            $group[] = array('row'=>$row,'item'=>$item,'classification'=>$classification,'rule'=>$rule,'quality'=>$quality);
        }
        if (!$group) { return $plan; }
        $plan['concepts'] = 1;
        $pool_limit = max(5, min(20, absint($settings['business_candidate_pool_per_concept'] ?? 10)));
        $visible_limit = 3;
        $reserve_limit = max(0, min(10, absint($settings['business_reserve_per_concept'] ?? 2)));
        $same_seller_limit = max(1, absint($settings['business_max_same_seller_per_block'] ?? 1));

        $this->ebay_business_candidate_sort($group);
        $group = array_slice($group, 0, $pool_limit);
        $prices = array_values(array_filter(array_map(static function($c){
            $v=(float)($c['item']['price_value']??0); return $v>0?$v:null;
        }, $group)));
        sort($prices, SORT_NUMERIC);
        $median=0.0; $n=count($prices);
        if($n){$median=$n%2?(float)$prices[(int)floor($n/2)]:(((float)$prices[$n/2-1]+(float)$prices[$n/2])/2.0);}
        foreach($group as &$candidate){
            $q=$this->ebay_business_quality_assess($candidate['item'],$candidate['classification'],$candidate['rule'],$settings,$median);
            if(!is_wp_error($q)){$candidate['quality']=$q;$candidate['item']=$this->ebay_business_item_with_quality($candidate['item'],$q);}
            else{$candidate['quality']=array('error'=>sanitize_key((string)$q->get_error_code()));}
        }
        unset($candidate);
        $group=array_values(array_filter($group,static function($c){return is_array($c['quality']??null)&&empty($c['quality']['error']);}));
        $this->ebay_business_candidate_sort($group);
        $plan['pool']=count($group);

        $seller_counts=array(); $visible=array(); $left=array(); $visible_titles=array();
        foreach($group as $candidate){
            $seller=sanitize_key((string)($candidate['item']['seller_username']??''));
            $title=$this->ebay_topic_text((string)($candidate['item']['title']??''));
            $near_duplicate=false;
            foreach($visible_titles as $known_title){
                if($title===''||$known_title===''){continue;}
                similar_text($title,$known_title,$pct);
                if($pct>=92.0){$near_duplicate=true;break;}
            }
            if(count($visible)<$visible_limit&&!$near_duplicate&&($seller===''||absint($seller_counts[$seller]??0)<$same_seller_limit)){
                $visible[]=$candidate;
                if($seller!==''){$seller_counts[$seller]=absint($seller_counts[$seller]??0)+1;}
                if($title!==''){$visible_titles[]=$title;}
            }else{$left[]=$candidate;}
        }
        if(count($visible)<$visible_limit&&$left){
            $rest=array();
            foreach($left as $candidate){
                $title=$this->ebay_topic_text((string)($candidate['item']['title']??''));
                $near_duplicate=false;
                foreach($visible_titles as $known_title){
                    if($title===''||$known_title===''){continue;}
                    similar_text($title,$known_title,$pct);
                    if($pct>=92.0){$near_duplicate=true;break;}
                }
                if(count($visible)<$visible_limit&&!$near_duplicate){
                    $visible[]=$candidate; if($title!==''){$visible_titles[]=$title;}
                }else{$rest[]=$candidate;}
            }
            $left=$rest;
        }
        foreach($visible as $i=>$candidate){
            $item_id=(string)($candidate['row']['item_id']??''); if($item_id===''){continue;}
            $plan['active'][$item_id]=array('rank'=>$i+1,'quality'=>(array)($candidate['quality']??array()),'concept'=>$concept_id);
        }
        foreach(array_slice($left,0,$reserve_limit) as $i=>$candidate){
            $item_id=(string)($candidate['row']['item_id']??''); if($item_id===''){continue;}
            $plan['reserve'][$item_id]=array('rank'=>$i+1,'quality'=>(array)($candidate['quality']??array()),'concept'=>$concept_id);
        }
        return $plan;
    }

    /** Enforce the portal-wide BUSINESS cap in rank rounds across concepts. */
    private function ebay_business_selection_apply_global_cap($active, $settings = null) {
        $settings = is_array($settings) ? $settings : $this->ebay_settings();
        $active = is_array($active) ? $active : array();
        $cap = max(30, absint($settings['business_active_cap'] ?? 1000));
        if (count($active) <= $cap) { return $active; }
        $required = array_values(array_filter(array_map('sanitize_key', $this->ebay_business_required_product_concept_ids())));
        $by = array();
        foreach($active as $item_id=>$entry){
            if(!is_array($entry)){continue;}
            $concept=sanitize_key((string)($entry['concept']??'')); $rank=max(1,absint($entry['rank']??1));
            if($concept!==''){$by[$concept][$rank][(string)$item_id]=$entry;}
        }
        $kept=array();
        for($rank=1;$rank<=3&&count($kept)<$cap;$rank++){
            foreach($required as $concept){
                if(empty($by[$concept][$rank])){continue;}
                foreach($by[$concept][$rank] as $item_id=>$entry){$kept[$item_id]=$entry;break;}
                if(count($kept)>=$cap){break;}
            }
        }
        return $kept;
    }

    /**
     * Pure complete BUSINESS planner used by diagnostics/gap analysis. Unlike
     * the historical global 5,000-row scan it is identity-fair and hard-bounded
     * per concept. The live selection worker does NOT call this monolith; it uses
     * the incremental prepare path below.
     */
    private function ebay_business_selection_plan($settings = null) {
        $settings = is_array($settings) ? $this->ebay_normalize_settings($settings, true) : $this->ebay_settings();
        $plan = array('active'=>array(),'reserve'=>array(),'concepts'=>0,'pool'=>0,'scanned'=>0,'blocked'=>0);
        foreach($this->ebay_business_required_product_concept_ids() as $concept_id){
            $part=$this->ebay_business_selection_plan_concept($concept_id,$settings);
            $plan['active']=array_replace($plan['active'],(array)($part['active']??array()));
            $plan['reserve']=array_replace($plan['reserve'],(array)($part['reserve']??array()));
            foreach(array('concepts','pool','scanned','blocked') as $k){$plan[$k]=absint($plan[$k]??0)+absint($part[$k]??0);}
        }
        $plan['active']=$this->ebay_business_selection_apply_global_cap($plan['active'],$settings);
        return $plan;
    }

    /** Authoritative BUSINESS supply manifest. The required set is data, not
     * a runtime 316-minus-N inference, so catalog changes cannot silently alter
     * the recovery contract. Unknown/malformed identities fail closed. */
    private function ebay_business_required_product_concept_ids() {
        $catalog=$this->ebay_portal_catalog(); if(is_wp_error($catalog)){return array();}
        $contract=is_array($catalog['business_supply_contract']??null)?$catalog['business_supply_contract']:array();
        $declared=(array)($contract['required_product_concept_ids']??array());
        $declared_count=absint($contract['required_count']??0);
        $known=array();
        foreach((array)($catalog['business_concepts']??array()) as $concept){
            $id=sanitize_key((string)($concept['id']??''));if($id!==''){$known[$id]=1;}
        }
        $ids=array();
        foreach($declared as $id){
            $id=sanitize_key((string)$id);
            if($id===''||!isset($known[$id])){return array();}
            $ids[$id]=1;
        }
        if(!$ids || $declared_count!==count($ids)){return array();}
        return array_keys($ids);
    }

    /** Coverage is measured by product families, not merely by total products.
     * 100 products from 10 concepts must not be treated as "portal supplied".
     */
    private function ebay_business_selection_coverage($selection_or_plan) {
        $data=is_array($selection_or_plan)?$selection_or_plan:array();
        $active=is_array($data['business_active']??null)?$data['business_active']:(array)($data['active']??array());
        $required=$this->ebay_business_required_product_concept_ids();
        $have=array();
        foreach($active as $entry){
            if(!is_array($entry)){continue;}
            $concept=sanitize_key((string)($entry['concept']??''));
            if($concept!==''){$have[$concept]=1;}
        }
        $missing=array_values(array_diff($required,array_keys($have)));
        return array(
            'required'=>count($required),'covered'=>count(array_intersect($required,array_keys($have))),
            'missing'=>count($missing),'missing_concepts'=>$missing,
        );
    }

    /**
     * Determine whether a PRIVATE source row can actually consume a visible
     * capacity slot. Drafts that were explicitly kept as drafts must not starve
     * another publishable item, and broken/stale listing pointers are treated as
     * new materialization candidates instead of permanent dead slots.
     */
    /**
     * V6.63.5 PRIVATE selector/public-gate freshness parity.
     * A source row that is stale at selection time can never become a winner.
     * The final public gate remains authoritative and can request one bounded
     * fresh PRIVATE tail if a selected row expires after selection.
     */
    private function ebay_private_source_row_is_public_fresh($row, $now = null) {
        $row=is_array($row)?$row:array();
        $now=$now===null?time():absint($now);
        if(absint($row['fresh_until']??0)<=$now){return false;}
        $end=absint($row['item_end_at']??0);
        if($end>0 && $end<=$now){return false;}
        return true;
    }

    private function ebay_private_capacity_row_publishable($row, $settings) {
        $row = is_array($row) ? $row : array();
        $settings = is_array($settings) ? $settings : $this->ebay_settings();
        $payload = json_decode((string)($row['source_payload'] ?? ''), true);
        $payload = is_array($payload) ? $payload : array();
        $raw = is_array($payload['raw'] ?? null) ? $payload['raw'] : array();
        if (!$raw) { return false; }
        $item = $this->ebay_accept_item($raw, 'INDIVIDUAL', $settings);
        if (is_wp_error($item)) { return false; }
        if ($this->ebay_remote_image_url_validate((string)($item['image_url'] ?? '')) === '') { return false; }
        // Never trust historical route_state alone for public capacity. Apply
        // current global hard negatives to the real stored offer without running
        // the expensive full catalog classifier across thousands of rows.
        $catalog = $this->ebay_portal_catalog();
        if (is_wp_error($catalog)) { return false; }
        $evidence = $this->ebay_topic_text($this->ebay_item_topic_evidence($item));
        foreach ((array)($catalog['hard_negative_markers'] ?? array()) as $marker) {
            if ($this->ebay_topic_negative_present($evidence, $marker)) { return false; }
        }

        $listing_id = absint($row['listing_post_id'] ?? 0);
        if ($listing_id <= 0) { return !empty($settings['private_auto_publish']); }
        $exists = function_exists('get_post_type') && (string)get_post_type($listing_id) === 'hp_listing';
        $owned = $exists && function_exists('get_post_meta')
            && (string)get_post_meta($listing_id, '_ppar_ebay_item_id', true) === (string)($row['item_id'] ?? '');
        if (!$exists || !$owned) { return !empty($settings['private_auto_publish']); }

        $status = function_exists('get_post_status') ? (string)get_post_status($listing_id) : '';
        if ($status === 'publish') { return true; }
        if ($status !== 'draft') { return false; }
        $reserve = sanitize_key((string)get_post_meta($listing_id, '_ppar_ebay_reserve_state', true));
        $lifecycle = sanitize_key((string)get_post_meta($listing_id, '_ppar_ebay_lifecycle_state', true));
        $intent = sanitize_key((string)get_post_meta($listing_id, '_ppar_ebay_publish_intent', true));
        if (!empty($settings['private_auto_publish']) && $reserve === 'capacity') { return true; }
        if (in_array($lifecycle, array('stale','ended'), true) && $intent === 'publish') { return true; }
        // An intentional/manual draft is valid content, but it is not a visible
        // slot and therefore must never reduce the number of public alternatives.
        return false;
    }

    /**
     * Pure PRIVATE planner; no HivePress post status is touched.
     *
     * V6.39 bounded-candidate invariant:
     * A portal cap of 250 must never trigger an unbounded walk through 10k/20k
     * historical source rows. We evaluate a deterministic recent candidate pool
     * of at most 4x the public cap (hard ceiling 1000). If that pool cannot supply
     * the public target, the existing targeted PRIVATE discovery/enrichment path
     * is responsible for adding fresh candidates; historical rows are not scanned
     * forever. The selected source row ids are retained so the apply phase touches
     * only actual winners. Non-winners are reconciled through the real published
     * HivePress-post sweep, which is the authoritative public-cap enforcement.
     */
    private function ebay_private_selection_plan($settings = null) {
        $settings=is_array($settings)?$this->ebay_normalize_settings($settings,true):$this->ebay_settings();
        global $wpdb;
        $plan=array('active'=>array(),'active_row_ids'=>array(),'keep_posts'=>array(),'eligible'=>0,'scanned'=>0,'candidate_limit'=>0);
        if(!is_object($wpdb)||!method_exists($wpdb,'get_results')){return $plan;}
        $table=$this->ebay_items_table();$now=time();
        $cap=min(250,max(1,absint($settings['private_active_cap']??250)));
        $candidate_limit=min(1000,max($cap,($cap*4)));
        $plan['candidate_limit']=$candidate_limit;
        $sql="SELECT * FROM {$table} WHERE seller_account_type='INDIVIDUAL' AND source_state='available' AND policy_state='allowed' AND route_state='ready' AND target_term_id>0 ORDER BY last_seen DESC,id DESC LIMIT ".absint($candidate_limit);
        $rows=(array)$wpdb->get_results($sql,ARRAY_A);
        $eligible=array();
        foreach($rows as $row){
            $plan['scanned']++;
            if(!$this->ebay_private_source_row_is_public_fresh($row,$now)){continue;}
            if(!$this->ebay_private_capacity_row_publishable($row,$settings)){continue;}
            $eligible[]=$row;
        }
        $plan['eligible']=count($eligible);
        $selected=$this->ebay_private_select_rows_for_capacity($eligible,$settings);
        foreach($selected as $item_id=>$row){
            $plan['active'][(string)$item_id]=1;
            $row_id=absint($row['id']??0);
            if($row_id>0){$plan['active_row_ids'][(string)$item_id]=$row_id;}
            $listing_id=absint($row['listing_post_id']??0);
            if($listing_id>0){$plan['keep_posts'][(string)$item_id]=$listing_id;}
        }
        return $plan;
    }

    /** Exact BUSINESS concept scope owned by this selection state. Normal
     * selection covers the full physical manifest; canonical gap-fill may touch
     * only the exact public-coverage missing list of the same durable run. */
    private function ebay_selection_business_target_concepts($state) {
        $required=array_values(array_filter(array_map('sanitize_key',$this->ebay_business_required_product_concept_ids())));
        if(!$required){return array();}
        $state=is_array($state)?$state:array();
        if(sanitize_key((string)($state['reason']??''))!=='canonical_gapfill'){return $required;}
        if(!method_exists($this,'ebay_run_load')){return array();}
        $run=$this->ebay_run_load();
        $uuid=sanitize_text_field((string)($run['run_uuid']??''));
        $owner=sanitize_text_field((string)($state['owner']??''));
        if((string)($run['schema']??'')!=='1.0' || sanitize_key((string)($run['phase']??''))!=='gapfill_select'
            || $uuid==='' || !hash_equals('run:'.$uuid,$owner)){return array();}
        $required_map=array_fill_keys($required,true);$out=array();
        foreach((array)($run['gapfill']['missing']??array()) as $id){$id=sanitize_key((string)$id);if($id!==''&&isset($required_map[$id])){$out[$id]=1;}}
        return array_keys($out);
    }

    /**
     * Incremental BUSINESS plan preparation. A real host must never classify
     * thousands of BUSINESS rows in one AJAX/Cron request. Each tick owns at
     * most eight product identities and persists its concept cursor.
     */
    private function ebay_selection_prepare_business_batch($settings, &$state, $concept_batch = 8) {
        $required = $this->ebay_selection_business_target_concepts($state);
        $total = count($required);
        if ($total < 1) {
            $state['status']='failed';$state['phase']='failed';$state['failed_at']=time();
            $state['failure_reason']='business_supply_contract_invalid';
            $state['error']='Der verbindliche BUSINESS-Versorgungsvertrag fehlt oder ist ungültig; Auswahl stoppt fail-closed.';
            return true;
        }
        if (empty($state['prepare_business_initialized'])) {
            $state['business_active'] = array();
            $state['business_reserve'] = array();
            $state['business_soft_failed'] = array();
            $state['business_target_concepts'] = $required;
            $state['business_target_mode'] = sanitize_key((string)($state['reason']??''))==='canonical_gapfill' ? 'gapfill' : 'full';
            $state['prepare_business_index'] = 0;
            $state['prepare_business_initialized'] = 1;
            $state['prepare_business_scanned'] = 0;
            $state['prepare_business_blocked'] = 0;
            $state['prepare_business_pool'] = 0;
            $state['prepare_business_concepts'] = 0;
        }
        $index = min($total, absint($state['prepare_business_index'] ?? 0));
        $concept_batch = max(1, min(12, absint($concept_batch)));
        $stop = min($total, $index + $concept_batch);
        for ($i=$index; $i<$stop; $i++) {
            $concept_id = $required[$i];
            // Idempotent on a retried tick: remove any old entries for this
            // concept before replacing the concept plan.
            foreach (array('business_active','business_reserve') as $bucket) {
                foreach ((array)($state[$bucket] ?? array()) as $item_id=>$entry) {
                    if (is_array($entry) && sanitize_key((string)($entry['concept'] ?? '')) === $concept_id) {
                        unset($state[$bucket][$item_id]);
                    }
                }
            }
            $part = $this->ebay_business_selection_plan_concept($concept_id, $settings);
            $state['business_active'] = array_replace((array)$state['business_active'], (array)($part['active'] ?? array()));
            $state['business_reserve'] = array_replace((array)$state['business_reserve'], (array)($part['reserve'] ?? array()));
            $state['prepare_business_scanned'] = absint($state['prepare_business_scanned'] ?? 0) + absint($part['scanned'] ?? 0);
            $state['prepare_business_blocked'] = absint($state['prepare_business_blocked'] ?? 0) + absint($part['blocked'] ?? 0);
            $state['prepare_business_pool'] = absint($state['prepare_business_pool'] ?? 0) + absint($part['pool'] ?? 0);
            $state['prepare_business_concepts'] = absint($state['prepare_business_concepts'] ?? 0) + absint($part['concepts'] ?? 0);
            $state['prepare_business_index'] = $i + 1;
        }
        $state['plan_stats']['business_prepare'] = array(
            'completed_concepts'=>absint($state['prepare_business_index'] ?? 0),
            'required_concepts'=>$total,
            'scanned'=>absint($state['prepare_business_scanned'] ?? 0),
            'pool'=>absint($state['prepare_business_pool'] ?? 0),
            'blocked'=>absint($state['prepare_business_blocked'] ?? 0),
            'target_mode'=>sanitize_key((string)($state['business_target_mode']??'full')),
            'target_concepts'=>$total,
            'active_target'=>count((array)($state['business_active'] ?? array())),
            'reserve_target'=>count((array)($state['business_reserve'] ?? array())),
        );
        if (absint($state['prepare_business_index'] ?? 0) < $total) { return false; }
        $state['business_active'] = $this->ebay_business_selection_apply_global_cap((array)$state['business_active'], $settings);
        $coverage = $this->ebay_business_selection_coverage(array('active'=>(array)$state['business_active']));
        $state['plan_stats']['business'] = array_merge(array(
            'scanned'=>absint($state['prepare_business_scanned'] ?? 0),
            'concepts'=>absint($state['prepare_business_concepts'] ?? 0),
            'pool'=>absint($state['prepare_business_pool'] ?? 0),
            'active_target'=>count((array)$state['business_active']),
            'reserve_target'=>count((array)$state['business_reserve']),
            'blocked'=>absint($state['prepare_business_blocked'] ?? 0),
        ), $coverage);
        $state['prepare_business_complete'] = 1;
        return true;
    }

    /** One bounded page of PRIVATE candidates for incremental prepare. */
    private function ebay_selection_prepare_private_batch($settings, &$state, $batch = 100) {
        global $wpdb;
        $cap=min(250,max(1,absint($settings['private_active_cap']??250)));
        $leaf_cap=min(30,max(1,absint($settings['private_leaf_cap']??30)));
        $batch=max(25,min(100,absint($batch)));
        if(!is_object($wpdb)||!method_exists($wpdb,'get_results')||!method_exists($wpdb,'prepare')){
            $state['status']='failed';$state['phase']='failed';$state['failed_at']=time();
            $state['failure_reason']='private_prepare_storage_unavailable';
            $state['error']='PRIVATE-Auswahl kann ohne Datenbankzugriff nicht vorbereitet werden.';
            return true;
        }
        $table=$this->ebay_items_table();
        if(empty($state['prepare_private_initialized'])){
            $leaf_ids=array();
            if(method_exists($wpdb,'get_col')){
                $leaf_ids=(array)$wpdb->get_col("SELECT DISTINCT target_term_id FROM {$table} WHERE seller_account_type='INDIVIDUAL' AND source_state='available' AND policy_state='allowed' AND route_state='ready' AND target_term_id>0 ORDER BY target_term_id ASC");
            }else{
                $tmp=(array)$wpdb->get_results("SELECT DISTINCT target_term_id FROM {$table} WHERE seller_account_type='INDIVIDUAL' AND source_state='available' AND policy_state='allowed' AND route_state='ready' AND target_term_id>0 ORDER BY target_term_id ASC",ARRAY_A);
                foreach($tmp as $r){$leaf_ids[]=absint($r['target_term_id']??0);}
            }
            $leaf_ids=array_values(array_unique(array_filter(array_map('absint',$leaf_ids))));
            sort($leaf_ids,SORT_NUMERIC);
            $leaf_count=max(1,count($leaf_ids));
            // Fair input basis: distribute the historical 1,000-source safety
            // ceiling BEFORE ranking instead of applying one global newest-LIMIT.
            // A sparse catalog may use up to the global PRIVATE cap from a leaf;
            // a broad catalog receives an equal bounded share per leaf.
            $candidate_budget=min(1000,max($cap,$cap*4));
            $per_leaf_limit=min($cap,max(1,(int)ceil($candidate_budget/$leaf_count)));
            $state['prepare_private_initialized']=1;
            $state['prepare_private_leaf_ids']=$leaf_ids;
            $state['prepare_private_leaf_index']=0;
            $state['prepare_private_leaf_offsets']=array();
            $state['prepare_private_scanned']=0;
            $state['prepare_private_eligible']=array();
            $state['prepare_private_per_leaf_limit']=$per_leaf_limit;
            $state['prepare_private_candidate_limit']=$per_leaf_limit*count($leaf_ids);
        }
        $leaf_ids=array_values(array_filter(array_map('absint',(array)($state['prepare_private_leaf_ids']??array()))));
        $leaf_index=min(count($leaf_ids),absint($state['prepare_private_leaf_index']??0));
        $per_leaf_limit=max(1,min($cap,absint($state['prepare_private_per_leaf_limit']??60)));
        $budget=$batch;
        while($budget>0 && $leaf_index<count($leaf_ids)){
            $leaf_id=absint($leaf_ids[$leaf_index]);
            $offset=absint($state['prepare_private_leaf_offsets'][(string)$leaf_id]??0);
            $remaining=max(0,$per_leaf_limit-$offset);
            if($remaining<=0){$leaf_index++;$state['prepare_private_leaf_index']=$leaf_index;continue;}
            $limit=min($budget,$remaining);
            $rows=(array)$wpdb->get_results($wpdb->prepare(
                "SELECT * FROM {$table} WHERE seller_account_type='INDIVIDUAL' AND source_state='available' AND policy_state='allowed' AND route_state='ready' AND target_term_id=%d ORDER BY last_seen DESC,id DESC LIMIT %d OFFSET %d",
                $leaf_id,$limit,$offset
            ),ARRAY_A);
            foreach($rows as $row){
                if(!is_array($row)){continue;}
                $state['prepare_private_scanned']=absint($state['prepare_private_scanned']??0)+1;
                if(!$this->ebay_private_source_row_is_public_fresh($row,time())){continue;}
                if(!$this->ebay_private_capacity_row_publishable($row,$settings)){continue;}
                $payload=json_decode((string)($row['source_payload']??''),true);$payload=is_array($payload)?$payload:array();
                $class=is_array($payload['portal_classification']??null)?$payload['portal_classification']:array();
                $raw=is_array($payload['raw']??null)?$payload['raw']:array();
                $light=array(
                    'id'=>absint($row['id']??0),'item_id'=>(string)($row['item_id']??''),'target_term_id'=>absint($row['target_term_id']??0),
                    'listing_post_id'=>absint($row['listing_post_id']??0),'image_url'=>(string)($row['image_url']??''),'last_seen'=>absint($row['last_seen']??0),
                    'rule_id'=>(string)($row['rule_id']??''),'title'=>(string)($row['title']??''),
                    'source_payload'=>wp_json_encode(array('portal_classification'=>$class,'raw'=>array('title'=>(string)($raw['title']??$row['title']??''))),JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES),
                );
                if($light['item_id']!==''){$state['prepare_private_eligible'][$light['item_id']]=$light;}
            }
            $advanced=count($rows);
            $offset+=$advanced;
            $state['prepare_private_leaf_offsets'][(string)$leaf_id]=$offset;
            $budget-=max(1,$advanced);
            if($advanced<$limit || $offset>=$per_leaf_limit){$leaf_index++;$state['prepare_private_leaf_index']=$leaf_index;}
            if($advanced===0 && $limit>0){continue;}
        }
        $done=$leaf_index>=count($leaf_ids);
        $state['plan_stats']['private_prepare']=array(
            'scanned'=>absint($state['prepare_private_scanned']??0),'eligible'=>count((array)($state['prepare_private_eligible']??array())),
            'leaves_complete'=>$leaf_index,'leaves_total'=>count($leaf_ids),'per_leaf_limit'=>$per_leaf_limit,
            'candidate_limit'=>absint($state['prepare_private_candidate_limit']??0),
        );
        if(!$done){return false;}
        $eligible=array_values((array)($state['prepare_private_eligible']??array()));
        $selected=$this->ebay_private_select_rows_for_capacity($eligible,$settings);
        $state['private_active']=array();$state['private_active_row_ids']=array();$state['private_keep_posts']=array();
        foreach($selected as $item_id=>$row){
            $state['private_active'][(string)$item_id]=1;
            $row_id=absint($row['id']??0);if($row_id>0){$state['private_active_row_ids'][(string)$item_id]=$row_id;}
            $listing_id=absint($row['listing_post_id']??0);if($listing_id>0){$state['private_keep_posts'][(string)$item_id]=$listing_id;}
        }
        $state['private_selected_offset']=0;
        $state['plan_stats']['private']=array(
            'scanned'=>absint($state['prepare_private_scanned']??0),'eligible'=>count($eligible),
            'active_target'=>count((array)$state['private_active']),'candidate_limit'=>absint($state['prepare_private_candidate_limit']??0),
            'leaves'=>count($leaf_ids),'per_leaf_limit'=>$per_leaf_limit,
        );
        unset($state['prepare_private_eligible']);
        $state['prepare_private_complete']=1;
        return true;
    }

    /** Prepare both plans without any monolithic BUSINESS scan. */
    private function ebay_selection_prepare_pending($settings = null, $state = null) {
        $settings=is_array($settings)?$this->ebay_normalize_settings($settings,true):$this->ebay_settings();
        $state=is_array($state)?$state:$this->ebay_selection_state_load();
        if(!in_array(sanitize_key((string)($state['status']??'')),array('pending','preparing'),true)){return $state;}
        $state['status']='preparing';$state['phase']='prepare';

        $scope=sanitize_key((string)($state['selection_scope']??''));
        if(!in_array($scope,array('all','private','business'),true)){
            $state['status']='failed';$state['phase']='failed';$state['failed_at']=time();
            $state['failure_reason']='invalid_selection_scope_prepare';
            $state['error']='Selection-Scope fehlt oder ist ungültig; fail-closed statt Fallback auf ALL.';
            return $this->ebay_selection_state_save($state);
        }
        $enabled_scope=$this->ebay_selection_scope_for_enabled_routes($scope,$settings);
        if($enabled_scope===''){
            $state['status']='failed';$state['phase']='failed';$state['failed_at']=time();
            $state['failure_reason']='selection_scope_disabled';
            $state['error']='Der angeforderte Selection-Scope ist in den aktuellen eBay-Einstellungen deaktiviert.';
            return $this->ebay_selection_state_save($state);
        }
        $scope=$enabled_scope;$state['selection_scope']=$scope;
        if(!isset($state['plan_stats'])||!is_array($state['plan_stats'])){$state['plan_stats']=array();}

        // BUSINESS is the expensive path and is always incremental.
        if($scope!=='private' && empty($state['prepare_business_complete'])){
            $done=$this->ebay_selection_prepare_business_batch($settings,$state,12);
            if(!$done){return $this->ebay_selection_state_save($state);}
        }

        // PRIVATE preparation is bounded too. A review approval can create a
        // PRIVATE-only selection, so the live admin path must never evaluate all
        // 1,000 candidates in a single request.
        if($scope!=='business' && empty($state['prepare_private_complete'])){
            $done=$this->ebay_selection_prepare_private_batch($settings,$state,100);
            if(!$done){return $this->ebay_selection_state_save($state);}
            if(sanitize_key((string)($state['status']??''))==='failed'){return $this->ebay_selection_state_save($state);}
        }
        if($scope==='business'){
            $state['private_active']=array();$state['private_active_row_ids']=array();$state['private_keep_posts']=array();
        }
        if($scope==='private'){
            $state['business_active']=array();$state['business_reserve']=array();
            $state['plan_stats']['business']=array_merge(array('scanned'=>0,'concepts'=>0,'pool'=>0,'active_target'=>0,'reserve_target'=>0,'blocked'=>0),$this->ebay_business_selection_coverage(array('active'=>array())));
        }

        $state['business_cursor']=0;$state['business_prune_cursor']=0;$state['private_cursor']=0;$state['private_selected_offset']=0;$state['private_post_sweep']=0;$state['private_post_cursor']=0;
        $state['status']='running';
        $state['phase']=$scope==='private'?'private_prune':'business_materialize';
        $state['prepared_at']=time();
        return $this->ebay_selection_state_save($state);
    }

    /** Candidate-local materialisation outcomes that coverage/gap-fill is
     * explicitly designed to replace. Infrastructure/storage/invariant errors
     * are intentionally excluded and still fail the complete run. */
    private function ebay_business_materialization_error_is_recoverable($error) {
        if(!is_wp_error($error)){return false;}
        $code=sanitize_key((string)$error->get_error_code());
        // Only a missing global subsystem is fatal here. All offer-specific
        // classification/import/materialisation failures are skipped and coverage
        // / gap-fill decides whether a replacement exists.
        return !in_array($code,array('ebay_creative_library_missing','storage_unavailable','database_unavailable'),true);
    }

    private function ebay_business_selection_record_soft_failure(&$state,&$stats,$item_id,$code,$row=array()) {
        $item_id=sanitize_text_field((string)$item_id);$code=sanitize_key((string)$code);
        if($item_id===''){return;}
        $entry=is_array($state['business_active'][$item_id]??null)?$state['business_active'][$item_id]:array();
        $concept=sanitize_key((string)($entry['concept']??($row['rule_id']??'')));
        if(!isset($state['business_soft_failed'])||!is_array($state['business_soft_failed'])){$state['business_soft_failed']=array();}
        $state['business_soft_failed'][$item_id]=array('code'=>$code,'concept'=>$concept,'row_id'=>absint($row['id']??0));
        unset($state['business_active'][$item_id]);
        if(!isset($stats['recoverable_errors'])||!is_array($stats['recoverable_errors'])){$stats['recoverable_errors']=array();}
        $stats['recoverable_errors'][]=array('item_id'=>$item_id,'code'=>$code,'concept'=>$concept);
        $stats['recoverable_failed']=absint($stats['recoverable_failed']??0)+1;
    }

    /**
     * BUSINESS phase 1: materialize every selected winner while existing valid
     * public campaigns stay untouched. This prevents a partial/failed recovery
     * from emptying category product blocks before replacements are proven.
     */
    private function ebay_selection_apply_business_batch($settings, &$state, $limit = 15) {
        global $wpdb;
        if(!is_object($wpdb)||!method_exists($wpdb,'get_results')||!method_exists($wpdb,'prepare')){
            $state['phase']='failed';$state['status']='failed';$state['completed_at']=time();
            $state['failure_reason']='storage_unavailable';
            $state['stats']['business']['errors'][]=array('code'=>'storage_unavailable');
            return 0;
        }
        $limit=max(1,min(50,absint($limit)));
        $table=$this->ebay_items_table();$cursor=absint($state['business_cursor']??0);
        $rows=(array)$wpdb->get_results($wpdb->prepare(
            "SELECT * FROM {$table} WHERE id>%d AND seller_account_type='BUSINESS' ORDER BY id ASC LIMIT %d",
            $cursor,$limit
        ),ARRAY_A);
        $stats=is_array($state['stats']['business']??null)?$state['stats']['business']:array();
        foreach($rows as $row){
            $row_id=absint($row['id']??0);if($row_id<=0){continue;}
            $state['business_cursor']=max(absint($state['business_cursor']??0),$row_id);
            $stats['scanned']=absint($stats['scanned']??0)+1;
            $item_id=(string)($row['item_id']??'');
            $now=time();$end=absint($row['item_end_at']??0);
            if(sanitize_key((string)($row['source_state']??''))==='ended'||($end>0&&$end<=$now)){
                if(isset($state['business_active'][$item_id])){
                    if((string)($row['creative_identity_hash']??'')!==''){$this->ebay_purge_item_content($row,'purged_ended','eBay-Angebot beendet; Auswahl entfernt die öffentliche Ausgabe.');}
                    $this->ebay_business_selection_record_soft_failure($state,$stats,$item_id,'business_selected_ended_during_apply',$row);
                }
                continue;
            }
            if(!isset($state['business_active'][$item_id])){continue;}
            // A source can age out between prepare and apply in a long-lived run.
            // Treat that as a bounded candidate-local soft failure so coverage /
            // gap-fill owns the replacement instead of publishing guaranteed-stale
            // data and later reporting a contradictory public 0/N state.
            if(!$this->ebay_business_source_row_is_public_fresh($row,$now)){
                $this->ebay_business_selection_record_soft_failure($state,$stats,$item_id,'business_selected_stale_during_apply',$row);
                continue;
            }
            $item=$this->ebay_business_source_row_item($row,$settings);
            if(is_wp_error($item)){
                $this->ebay_business_selection_record_soft_failure($state,$stats,$item_id,$item->get_error_code(),$row);
                continue;
            }
            $classification=(array)($item['portal_classification']??array());
            $rule=$this->ebay_rule_by_id((string)($row['rule_id']??''),$settings);
            $selection_entry=$state['business_active'][$item_id]??array();
            $rank=is_array($selection_entry)?absint($selection_entry['rank']??1):absint($selection_entry?:1);
            $quality=is_array($selection_entry)&&is_array($selection_entry['quality']??null)?$selection_entry['quality']:array();
            if(!$quality){
                $quality=$this->ebay_business_quality_assess($item,$classification,$rule,$settings,0.0);
                if(is_wp_error($quality)){$this->ebay_business_selection_record_soft_failure($state,$stats,$item_id,$quality->get_error_code(),$row);continue;}
            }
            $item=$this->ebay_business_item_with_quality($item,$quality);
            $item['business_selection']=array('role'=>'active_selected','rank'=>$rank);
            $result=$this->ebay_route_business($row,$item,$rule,'bounded-selection-'.sanitize_key((string)($state['reason']??'selection')).'-'.time(),$classification);
            if(is_wp_error($result)){
                if($this->ebay_business_materialization_error_is_recoverable($result)){
                    $this->ebay_business_selection_record_soft_failure($state,$stats,$item_id,$result->get_error_code(),$row);
                }else{$stats['errors'][]=array('item_id'=>$item_id,'code'=>$result->get_error_code());}
            }else{
                // A verified Last-Known-Good review is deliberately not promoted
                // to a new active_selected winner. Preserve it, let Public-Coverage
                // count it if still valid, and let targeted gap-fill replace only
                // a genuinely missing family.
                if(!empty($result['last_good_preserved'])){
                    $this->ebay_business_selection_record_soft_failure($state,$stats,$item_id,sanitize_key((string)($result['review_code']??'ebay_business_materialization_not_active')),$row);
                    $stats['last_good_preserved']=absint($stats['last_good_preserved']??0)+1;
                    continue;
                }
                // Public materialization owns output_state=creative_ready. Persist
                // the internal winner role separately and verify it without ever
                // replacing the public state.
                $commit=$this->ebay_business_commit_selected_source_role($row,$quality,'active_selected',$rank);
                if(is_wp_error($commit)){
                    $stats['errors'][]=array('item_id'=>$item_id,'code'=>'business_selection_commit_failed','detail_code'=>$commit->get_error_code());
                }else{
                    $stats['materialized']=absint($stats['materialized']??0)+1;
                    $stats['active']=absint($stats['active']??0)+1;
                }
            }
        }
        if(isset($state['plan_stats']['business'])&&is_array($state['plan_stats']['business'])){
            $state['plan_stats']['business']=array_merge($state['plan_stats']['business'],$this->ebay_business_selection_coverage(array('active'=>(array)($state['business_active']??array()))));
        }
        $state['stats']['business']=$stats;
        if(count($rows)<$limit){
            $expected=count((array)($state['business_active']??array()));
            $materialized=absint($stats['materialized']??0);
            $errors=(array)($stats['errors']??array());
            if(!empty($errors) || $materialized<$expected){
                // Only unexplained/infrastructure/invariant failures remain fatal.
                // Candidate-local soft failures were removed from the active plan
                // above and are owned by coverage/gap-fill.
                $state['phase']='failed';$state['status']='failed';$state['completed_at']=time();
                $state['failure_reason']='business_recovery_incomplete';
                $state['stats']['business']['verification']=array('expected'=>$expected,'materialized'=>$materialized,'errors'=>count($errors),'recoverable_errors'=>count((array)($stats['recoverable_errors']??array())));
            }else{
                $state['business_prune_cursor']=0;
                $state['phase']='business_prune';
            }
        }
        return count($rows);
    }

    /**
     * BUSINESS phase 2: only after every selected winner is materialized, prune
     * displaced public outputs and assign reserve/candidate roles. A failed
     * phase 1 therefore cannot blank portal categories.
     */
    private function ebay_selection_prune_business_batch($settings, &$state, $limit = 20, $commit_public = false, $terminal_transition = true) {
        global $wpdb;
        $staging = !$commit_public && method_exists($this,'ebay_run_checkpoint_staging_active') && $this->ebay_run_checkpoint_staging_active();
        if(!is_object($wpdb)||!method_exists($wpdb,'get_results')||!method_exists($wpdb,'prepare')){
            $state['phase']='failed';$state['status']='failed';$state['completed_at']=time();
            $state['failure_reason']='storage_unavailable_prune';
            return 0;
        }
        $limit=max(1,min(50,absint($limit)));
        $table=$this->ebay_items_table();$cursor=absint($state['business_prune_cursor']??0);
        $rows=(array)$wpdb->get_results($wpdb->prepare(
            "SELECT * FROM {$table} WHERE id>%d AND seller_account_type='BUSINESS' ORDER BY id ASC LIMIT %d",
            $cursor,$limit
        ),ARRAY_A);
        $stats=is_array($state['stats']['business']??null)?$state['stats']['business']:array();
        foreach($rows as $row){
            $row_id=absint($row['id']??0);if($row_id<=0){continue;}
            $state['business_prune_cursor']=max(absint($state['business_prune_cursor']??0),$row_id);
            $item_id=(string)($row['item_id']??'');
            $end=absint($row['item_end_at']??0);
            if(sanitize_key((string)($row['source_state']??''))==='ended'||($end>0&&$end<=time())){continue;}
            if(isset($state['business_active'][$item_id])){continue;}
            // Soft-failed candidate state (review/repair_pending or verified LKG)
            // is authoritative and must not be rewritten back to ready/candidate.
            if(isset($state['business_soft_failed'][$item_id])){continue;}
            if(sanitize_key((string)($state['business_target_mode']??''))==='gapfill'){
                $targets=array_fill_keys(array_values(array_filter(array_map('sanitize_key',(array)($state['business_target_concepts']??array())))),true);
                $concept=sanitize_key((string)($row['rule_id']??''));
                if($concept==='' || !isset($targets[$concept])){continue;}
            }
            if(isset($state['business_reserve'][$item_id])){
                $selection_entry=$state['business_reserve'][$item_id]??array();
                $rank=is_array($selection_entry)?absint($selection_entry['rank']??1):absint($selection_entry?:1);
                $quality=is_array($selection_entry)&&is_array($selection_entry['quality']??null)?$selection_entry['quality']:array();
                if($staging){
                    $stats['pending_deactivation']=absint($stats['pending_deactivation']??0)+1;
                }else{
                    $this->ebay_business_persist_quality_on_source_row($row,$quality,'reserve',$rank);
                    $this->ebay_business_pause_output_for_capacity($row,'reserve','Reserveprodukt – rückt automatisch nach, wenn ein aktiver Treffer entfällt.');
                    $stats['deactivated']=absint($stats['deactivated']??0)+1;
                }
            }else{
                $current=sanitize_key((string)($row['output_state']??''));
                if($staging){
                    $stats['pending_deactivation']=absint($stats['pending_deactivation']??0)+1;
                }else{
                    if($current==='creative_ready'||$current==='active_selected'||$current==='review_last_good'||(string)($row['creative_identity_hash']??'')!==''){
                        $this->ebay_business_pause_output_for_capacity($row,'candidate','Qualifizierter Kandidat außerhalb der aktiven Top-Auswahl.');
                        $stats['deactivated']=absint($stats['deactivated']??0)+1;
                    }elseif($current!=='candidate'){
                        $this->ebay_business_persist_quality_on_source_row($row,array(),'candidate',0);
                    }
                }
                $stats['candidate']=absint($stats['candidate']??0)+1;
            }
        }
        $state['stats']['business']=$stats;
        if(count($rows)<$limit){
            if(!$terminal_transition){
                $state['checkpoint_business_cleanup_done']=1;
            }else{
                $scope=sanitize_key((string)($state['selection_scope']??''));
                if($scope==='business'){
                    $state['phase']='complete';$state['status']='complete';$state['completed_at']=time();
                }elseif($scope==='all'){
                    $state['phase']='private_prune';
                }else{
                    $state['phase']='failed';$state['status']='failed';$state['failed_at']=time();
                    $state['failure_reason']='invalid_selection_scope_business_prune';
                }
            }
        }
        return count($rows);
    }

    private function ebay_selection_apply_private_batch($settings, &$state, $limit = 35) {
        global $wpdb;
        if(!is_object($wpdb)||!method_exists($wpdb,'get_results')){
            $state['phase']='failed';$state['status']='failed';$state['failed_at']=time();
            $state['error']='PRIVATE-Auswahl kann den gespeicherten Kandidatenbestand nicht lesen.';
            $state['stats']['private']['errors'][]=array('code'=>'storage_unavailable');
            return 0;
        }
        $limit=max(1,min(50,absint($limit)));
        $table=$this->ebay_items_table();
        $selected_map=is_array($state['private_active_row_ids']??null)?$state['private_active_row_ids']:array();
        $selected_ids=array_values(array_filter(array_map('absint',array_values($selected_map))));
        $offset=absint($state['private_selected_offset']??0);
        $batch_ids=array_slice($selected_ids,$offset,$limit);
        $stats=is_array($state['stats']['private']??null)?$state['stats']['private']:array();
        $stats['selected_total']=count($selected_ids);

        if(!$batch_ids){
            $state['phase']='private_verify';
            $state['stats']['private']=$stats;
            return 0;
        }

        $id_sql=implode(',',array_map('absint',$batch_ids));
        $rows=(array)$wpdb->get_results("SELECT * FROM {$table} WHERE id IN ({$id_sql}) AND seller_account_type='INDIVIDUAL' ORDER BY id ASC",ARRAY_A);
        $by_id=array();foreach($rows as $row){$rid=absint($row['id']??0);if($rid>0){$by_id[$rid]=$row;}}

        foreach($batch_ids as $row_id){
            $state['private_selected_offset']=absint($state['private_selected_offset']??0)+1;
            $stats['scanned']=absint($stats['scanned']??0)+1;
            $row=$by_id[$row_id]??null;
            if(!is_array($row)){
                $stats['errors'][]=array('row_id'=>$row_id,'code'=>'private_selected_source_missing');
                continue;
            }
            $state['private_cursor']=max(absint($state['private_cursor']??0),$row_id);
            $item_id=(string)($row['item_id']??'');$listing_id=absint($row['listing_post_id']??0);
            if($item_id===''||!isset($state['private_active'][$item_id])){
                $stats['errors'][]=array('row_id'=>$row_id,'code'=>'private_selected_identity_mismatch');
                continue;
            }
            $end=absint($row['item_end_at']??0);
            if(sanitize_key((string)($row['source_state']??''))==='ended'||($end>0&&$end<=time())){
                if($listing_id>0){$this->ebay_purge_item_content($row,'purged_ended','eBay-Angebot beendet; Auswahl entfernt die öffentliche Ausgabe.');}
                $stats['errors'][]=array('item_id'=>$item_id,'code'=>'private_selected_ended_during_apply');
                continue;
            }
            $healthy=false;$target_term_id=absint($row['target_term_id']??0);
            if($listing_id>0&&function_exists('get_post_status')&&function_exists('get_post_meta')){
                $owned=(string)get_post_meta($listing_id,'_ppar_ebay_item_id',true)===$item_id;
                $status=(string)get_post_status($listing_id);
                $reserve_state=sanitize_key((string)get_post_meta($listing_id,'_ppar_ebay_reserve_state',true));
                $lifecycle=sanitize_key((string)get_post_meta($listing_id,'_ppar_ebay_lifecycle_state',true));
                $listing_source_hash=strtolower(sanitize_text_field((string)get_post_meta($listing_id,'_ppar_ebay_source_hash',true)));
                $row_source_hash=strtolower(sanitize_text_field((string)($row['source_hash']??'')));
                $source_current=$row_source_hash!=='' && $listing_source_hash!=='' && hash_equals($row_source_hash,$listing_source_hash);
                $target_ok=$target_term_id>0;
                if($target_ok && function_exists('wp_get_post_terms')){
                    $term_ids=wp_get_post_terms($listing_id,'hp_listing_category',array('fields'=>'ids'));
                    $target_ok=!is_wp_error($term_ids) && in_array($target_term_id,array_map('absint',(array)$term_ids),true);
                }
                $healthy=$owned&&$status==='publish'&&$reserve_state===''&&!in_array($lifecycle,array('stale','ended'),true)&&$source_current&&$target_ok;
            }
            if(!$healthy){
                $payload=json_decode((string)($row['source_payload']??''),true);$payload=is_array($payload)?$payload:array();
                $raw=is_array($payload['raw']??null)?$payload['raw']:array();
                $item=$raw?$this->ebay_accept_item($raw,'INDIVIDUAL',$settings):new WP_Error('private_raw_missing','PRIVATE-Rohdaten fehlen.');
                if(is_wp_error($item)){$stats['errors'][]=array('item_id'=>$item_id,'code'=>$item->get_error_code());}
                else{
                    $item['portal_classification']=is_array($payload['portal_classification']??null)?$payload['portal_classification']:array();
                    $res=$this->ebay_materialize_private_listing($row,$item,$target_term_id,$settings);
                    if(is_wp_error($res)){$stats['errors'][]=array('item_id'=>$item_id,'code'=>$res->get_error_code());}
                    else{
                        $new_listing_id=is_array($res)?absint($res['listing_id']??0):0;
                        if($new_listing_id>0 && function_exists('get_post_status') && get_post_status($new_listing_id)==='publish'){
                            $stats['materialized']=absint($stats['materialized']??0)+1;
                            $state['private_keep_posts'][$item_id]=$new_listing_id;
                            $stats['active']=absint($stats['active']??0)+1;
                        }else{$stats['errors'][]=array('item_id'=>$item_id,'code'=>'private_selected_not_published');}
                    }
                }
            }else{
                $upd=array('output_state'=>'listing_published','status'=>'active','rejection_reason'=>'','updated_at'=>time());
                if(method_exists($wpdb,'update')){$wpdb->update($table,$upd,array('id'=>$row_id),$this->ebay_db_formats($upd),array('%d'));}
                $state['private_keep_posts'][$item_id]=$listing_id;
                $stats['active']=absint($stats['active']??0)+1;
            }
        }
        $state['stats']['private']=$stats;
        if(absint($state['private_selected_offset']??0)>=count($selected_ids)){$state['phase']='private_verify';}
        return count($batch_ids);
    }

    /**
     * V6.25 ownership proof for current and historical plugin-created eBay
     * PRIVATE HivePress posts. Native HivePress listings remain out of scope.
     * Current posts carry _ppar_ebay_item_id. Older plugin builds may still be
     * provable through other private eBay metadata written only by this plugin.
     */
    private function ebay_private_post_ownership($listing_id) {
        $listing_id=absint($listing_id);
        $out=array('owned'=>false,'item_id'=>'','legacy'=>false,'signals'=>array());
        if($listing_id<=0 || !function_exists('get_post_meta')){return $out;}
        $item_id=sanitize_text_field((string)get_post_meta($listing_id,'_ppar_ebay_item_id',true));
        if($item_id!==''){$out['owned']=true;$out['item_id']=$item_id;$out['signals'][]='item_id';return $out;}
        $seller_type=strtoupper(sanitize_key((string)get_post_meta($listing_id,'_ppar_ebay_seller_type',true)));
        $affiliate=(string)get_post_meta($listing_id,'_ppar_ebay_affiliate_url',true);
        $source_hash=sanitize_text_field((string)get_post_meta($listing_id,'_ppar_ebay_source_hash',true));
        $portal_path=sanitize_text_field((string)get_post_meta($listing_id,'_ppar_ebay_portal_path',true));
        $target=absint(get_post_meta($listing_id,'_ppar_ebay_target_term_id',true));
        $hp_url=(string)get_post_meta($listing_id,'hp_url',true);
        $is_ebay_url=static function($url){
            $host=strtolower((string)parse_url((string)$url,PHP_URL_HOST));
            return $host!=='' && (preg_match('/(^|\\.)ebay\\.[a-z.]+$/',$host) || preg_match('/(^|\\.)ebayimg\\.com$/',$host));
        };
        if($seller_type==='INDIVIDUAL'){$out['signals'][]='seller_type';}
        if($affiliate!=='' && $is_ebay_url($affiliate)){$out['signals'][]='affiliate_url';}
        if($source_hash!==''){$out['signals'][]='source_hash';}
        if($portal_path!=='' && stripos($portal_path,'Private Anzeigen')!==false){$out['signals'][]='portal_path';}
        if($target>0){$out['signals'][]='target_term';}
        if($hp_url!=='' && $is_ebay_url($hp_url)){$out['signals'][]='hp_url';}
        // Namespaced _ppar_ebay_* metadata is itself plugin ownership proof on
        // hp_listing. A generic hp_url alone is deliberately NOT proof, because a
        // normal HivePress user may link to eBay manually. Historical importer
        // posts therefore remain recoverable even if only one old plugin marker
        // survived a previous migration.
        $plugin_specific=($seller_type==='INDIVIDUAL')
            || ($affiliate!=='' && $is_ebay_url($affiliate))
            || $source_hash!==''
            || ($portal_path!=='' && stripos($portal_path,'Private Anzeigen')!==false)
            || $target>0;
        if($plugin_specific){$out['owned']=true;$out['legacy']=true;}
        return $out;
    }

    /** Current hard negatives must also evict historical posts with no source row. */
    private function ebay_private_post_hard_negative_reason($listing_id) {
        $listing_id=absint($listing_id);if($listing_id<=0){return '';}
        $title=function_exists('get_post_field')?(string)get_post_field('post_title',$listing_id):'';
        $path=function_exists('get_post_meta')?(string)get_post_meta($listing_id,'_ppar_ebay_portal_path',true):'';
        $slug=function_exists('get_post_meta')?(string)get_post_meta($listing_id,'_ppar_ebay_product_slug',true):'';
        $evidence=$this->ebay_topic_text(trim($title.' '.$path.' '.$slug));
        if($evidence===''){return '';}
        $catalog=$this->ebay_portal_catalog();if(is_wp_error($catalog)){return '';}
        foreach((array)($catalog['hard_negative_markers']??array()) as $marker){
            if($this->ebay_topic_negative_present($evidence,$marker)){return sanitize_text_field((string)$marker);}
        }
        return '';
    }

    /**
     * V6.25 real-post sweep. It scans every actually published hp_listing by ID,
     * proves eBay ownership post by post and keeps public only the canonical
     * selected listing IDs. Historical plugin-owned posts without current item
     * markers are drafted as legacy orphans. Native HivePress posts are untouched.
     */
    private function ebay_selection_apply_private_post_batch($settings, &$state, $limit = 50, $commit_public = false, $terminal_transition = true) {
        global $wpdb;
        $staging = !$commit_public && method_exists($this,'ebay_run_checkpoint_staging_active') && $this->ebay_run_checkpoint_staging_active();
        $limit=max(1,min(100,absint($limit)));
        if(!is_object($wpdb)||!isset($wpdb->posts)||!method_exists($wpdb,'get_col')||!method_exists($wpdb,'prepare')){
            $state['status']='failed';$state['phase']='private_posts';$state['failed_at']=time();
            $state['error']='Realer PRIVATE-Post-Reconcile kann die WordPress-Posttabelle nicht deterministisch lesen.';
            return 0;
        }
        $cursor=absint($state['private_post_cursor']??0);
        $ids=(array)$wpdb->get_col($wpdb->prepare(
            "SELECT ID FROM {$wpdb->posts} WHERE post_type='hp_listing' AND post_status='publish' AND ID>%d ORDER BY ID ASC LIMIT %d",
            $cursor,$limit
        ));
        $ids=array_values(array_filter(array_map('absint',$ids)));
        $stats=is_array($state['stats']['private']??null)?$state['stats']['private']:array();
        foreach($ids as $listing_id){
            $state['private_post_cursor']=max(absint($state['private_post_cursor']??0),$listing_id);
            $ownership=$this->ebay_private_post_ownership($listing_id);
            if(empty($ownership['owned'])){$stats['native_seen']=absint($stats['native_seen']??0)+1;continue;}
            $stats['published_owned_seen']=absint($stats['published_owned_seen']??0)+1;
            if(!empty($ownership['legacy'])){$stats['legacy_owned_seen']=absint($stats['legacy_owned_seen']??0)+1;}
            $item_id=(string)($ownership['item_id']??'');
            $canonical=$item_id!=='' && absint($state['private_keep_posts'][$item_id]??0)===$listing_id;
            $hard_negative=$this->ebay_private_post_hard_negative_reason($listing_id);
            if($canonical && $hard_negative===''){
                $stats['verified_public']=absint($stats['verified_public']??0)+1;
                continue;
            }
            if($staging){
                $stats['pending_deactivation']=absint($stats['pending_deactivation']??0)+1;
                $state['private_post_sweep']=absint($state['private_post_sweep']??0)+1;
                continue;
            }
            if(function_exists('wp_update_post')){
                $res=wp_update_post(array('ID'=>$listing_id,'post_status'=>'draft'),true);
                if(is_wp_error($res)){
                    $stats['errors'][]=array('listing_id'=>$listing_id,'code'=>$res->get_error_code());
                    $stats['post_deactivation_errors']=absint($stats['post_deactivation_errors']??0)+1;
                    continue;
                }
            }else{
                $stats['post_deactivation_errors']=absint($stats['post_deactivation_errors']??0)+1;
                $stats['errors'][]=array('listing_id'=>$listing_id,'code'=>'wp_update_post_missing');
                continue;
            }
            if(function_exists('update_post_meta')){
                update_post_meta($listing_id,'_ppar_ebay_reserve_state',$hard_negative!==''?'policy':'capacity');
                update_post_meta($listing_id,'_ppar_ebay_lifecycle_state',$hard_negative!==''?'blocked':'active');
                if($hard_negative!==''){update_post_meta($listing_id,'_ppar_ebay_recovery_block_reason',$hard_negative);}
            }
            if($hard_negative!==''){$stats['hard_negative_deactivated']=absint($stats['hard_negative_deactivated']??0)+1;}
            if(!empty($ownership['legacy'])){$stats['legacy_deactivated']=absint($stats['legacy_deactivated']??0)+1;}
            $stats['deactivated']=absint($stats['deactivated']??0)+1;
            $state['private_post_sweep']=absint($state['private_post_sweep']??0)+1;
        }
        $state['stats']['private']=$stats;
        if(count($ids)<$limit){
            if(!$terminal_transition){
                $state['checkpoint_private_cleanup_done']=1;
            }elseif(absint($stats['post_deactivation_errors']??0)>0){
                $state['phase']='private_prune';$state['status']='failed';$state['failed_at']=time();
                $state['error']='PRIVATE-Recovery konnte nicht alle überzähligen/gesperrten eBay-Anzeigen deaktivieren.';
            }else{
                // During canonical checkpoint staging the current safe public set
                // stays untouched; selected replacements are materialized next but
                // remain hidden by the checkpoint boundary until final verification.
                $state['phase']='private';
                $state['private_selected_offset']=0;
            }
        }
        return count($ids);
    }

    /** One bounded selection tick. Never scans/materializes the whole inventory. */
    /**
     * Read-only final PRIVATE invariant check after prune-first + materialize.
     * No posts are changed here. A completed selection is only possible when
     * the actual public plugin-owned count is <= the configured hard cap.
     */
    private function ebay_selection_verify_private_final($settings, &$state) {
        $cap = min(250, max(1, absint($settings['private_active_cap'] ?? 250)));
        $staging = method_exists($this,'ebay_run_checkpoint_staging_active') && $this->ebay_run_checkpoint_staging_active();
        if($staging){
            $candidate_ids=array_values(array_unique(array_filter(array_map('absint',array_values((array)($state['private_keep_posts']??array()))))));
            if(count($candidate_ids)>$cap){
                $state['status']='failed';$state['phase']='private_verify';$state['failed_at']=time();
                $state['failure_reason']='private_candidate_cap_exceeded';
                $state['error']='PRIVATE-Endverifikation meldet '.count($candidate_ids).' Kandidaten bei Cap '.$cap.'.';
                return false;
            }
            $now=time(); global $wpdb;
            foreach($candidate_ids as $listing_id){
                $post=function_exists('get_post')?get_post($listing_id):null;
                $item_id=function_exists('get_post_meta')?sanitize_text_field((string)get_post_meta($listing_id,'_ppar_ebay_item_id',true)):'';
                $source=($item_id!=='' && is_object($wpdb) && method_exists($wpdb,'get_row') && method_exists($wpdb,'prepare'))
                    ? $wpdb->get_row($wpdb->prepare("SELECT * FROM {$this->ebay_items_table()} WHERE item_id=%s AND seller_account_type='INDIVIDUAL' ORDER BY id DESC LIMIT 1",$item_id),ARRAY_A)
                    : array();
                if(!is_object($post) || (string)($post->post_status??'')!=='publish' || !$this->ebay_private_public_post_allowed_base($post,is_array($source)?$source:array(),true,$now)){
                    $state['status']='failed';$state['phase']='private_verify';$state['failed_at']=time();
                    $state['failure_reason']='private_candidate_not_safe';
                    $state['error']='PRIVATE-Endverifikation hat einen nicht sicher veröffentlichbaren Kandidaten gefunden.';
                    return false;
                }
            }
            $state['verified_public_private']=count($candidate_ids);
            $state['verified_native_public']=absint($state['stats']['private']['native_seen'] ?? 0);
            $state['status']='complete';$state['phase']='complete';$state['completed_at']=time();
            return true;
        }
        $public = $this->ebay_private_public_owned_count();
        if ($public === null) {
            $state['status']='failed';$state['phase']='private_verify';$state['failed_at']=time();
            $state['failure_reason']='private_public_count_unavailable';
            $state['error']='PRIVATE-Endverifikation konnte den realen öffentlichen Plugin-Bestand nicht bestimmen.';
            return false;
        }
        if (absint($public) > $cap) {
            $state['status']='failed';$state['phase']='private_verify';$state['failed_at']=time();
            $state['failure_reason']='private_public_cap_exceeded';
            $state['error']='PRIVATE-Endverifikation meldet '.absint($public).' öffentliche eBay-Anzeigen bei Cap '.$cap.'.';
            return false;
        }
        $state['verified_public_private']=absint($public);
        $state['verified_native_public']=absint($state['stats']['private']['native_seen'] ?? 0);
        $state['status']='complete';$state['phase']='complete';$state['completed_at']=time();
        return true;
    }

    /**
     * Stable workflow fingerprint for the standalone selection worker. Runtime
     * timestamps, scheduling metadata and the guard counter itself are excluded,
     * so only real workflow movement resets the no-progress guard.
     */
    private function ebay_selection_progress_fingerprint($state) {
        $state=is_array($state)?$state:array();
        $business=is_array($state['stats']['business']??null)?$state['stats']['business']:array();
        $private=is_array($state['stats']['private']??null)?$state['stats']['private']:array();

        // V6.42: one complete cursor contract for the bounded selector. The
        // previous fingerprint still referenced the retired global PRIVATE
        // offset and therefore treated real per-leaf cursor movement as a
        // stall. Keep every durable prepare/apply cursor that can advance a
        // bounded tick, while excluding timestamps/heartbeat bookkeeping.
        $leaf_offsets=array();
        foreach((array)($state['prepare_private_leaf_offsets']??array()) as $leaf_id=>$offset){
            $leaf_id=(string)absint($leaf_id); if($leaf_id==='0'){continue;}
            $leaf_offsets[$leaf_id]=absint($offset);
        }
        if($leaf_offsets){ksort($leaf_offsets,SORT_NUMERIC);}
        $payload=array(
            'status'=>sanitize_key((string)($state['status']??'')),
            'phase'=>sanitize_key((string)($state['phase']??'')),
            'prepare_business_index'=>absint($state['prepare_business_index']??0),
            'prepare_business_scanned'=>absint($state['prepare_business_scanned']??0),
            'prepare_business_pool'=>absint($state['prepare_business_pool']??0),
            'prepare_business_blocked'=>absint($state['prepare_business_blocked']??0),
            'prepare_business_complete'=>!empty($state['prepare_business_complete'])?1:0,
            'business_target_mode'=>sanitize_key((string)($state['business_target_mode']??'')),
            'business_target_concepts'=>count((array)($state['business_target_concepts']??array())),
            'business_soft_failed'=>count((array)($state['business_soft_failed']??array())),
            'prepare_private_initialized'=>!empty($state['prepare_private_initialized'])?1:0,
            'prepare_private_complete'=>!empty($state['prepare_private_complete'])?1:0,
            // Backward-compatible legacy cursor plus the real V6.41 fair-input
            // cursor set. Any scanned leaf page is therefore real progress even
            // when it yields zero eligible candidates.
            'prepare_private_offset'=>absint($state['prepare_private_offset']??0),
            'prepare_private_leaf_index'=>absint($state['prepare_private_leaf_index']??0),
            'prepare_private_leaf_offsets'=>$leaf_offsets,
            'prepare_private_scanned'=>absint($state['prepare_private_scanned']??0),
            'prepare_private_eligible'=>count((array)($state['prepare_private_eligible']??array())),
            'prepare_active_target'=>count((array)($state['business_active']??array())),
            'prepare_private_target'=>count((array)($state['private_active']??array())),
            'business_cursor'=>absint($state['business_cursor']??0),
            'business_prune_cursor'=>absint($state['business_prune_cursor']??0),
            'private_cursor'=>absint($state['private_cursor']??0),
            'private_selected_offset'=>absint($state['private_selected_offset']??0),
            'private_post_cursor'=>absint($state['private_post_cursor']??0),
            'private_post_sweep'=>absint($state['private_post_sweep']??0),
            'verified_public_private'=>absint($state['verified_public_private']??0),
            'business'=>array(
                'scanned'=>absint($business['scanned']??0),'active'=>absint($business['active']??0),
                'reserve'=>absint($business['reserve']??0),'candidate'=>absint($business['candidate']??0),
                'deactivated'=>absint($business['deactivated']??0),'materialized'=>absint($business['materialized']??0),
                'errors'=>count((array)($business['errors']??array())),
            ),
            'private'=>array(
                'scanned'=>absint($private['scanned']??0),'active'=>absint($private['active']??0),
                'reserved'=>absint($private['reserved']??0),'materialized'=>absint($private['materialized']??0),
                'deactivated'=>absint($private['deactivated']??0),'errors'=>count((array)($private['errors']??array())),
            ),
        );
        return hash('sha256',wp_json_encode($payload,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES));
    }

    private function ebay_selection_process_tick($settings = null, $state = null) {
        $settings=is_array($settings)?$this->ebay_normalize_settings($settings,true):$this->ebay_settings();
        $state=is_array($state)?$state:$this->ebay_selection_state_load();
        $status=sanitize_key((string)($state['status']??''));
        if($status==='pending'||$status==='preparing'){
            return $this->ebay_selection_prepare_pending($settings,$state);
        }
        if($status!=='running'){return $state;}
        $scope=sanitize_key((string)($state['selection_scope']??''));
        $enabled_scope=$this->ebay_selection_scope_for_enabled_routes($scope,$settings);
        if($enabled_scope==='' || $enabled_scope!==$scope){
            $phase=sanitize_key((string)($state['phase']??''));
            // Safe narrowing is possible only while an ALL run is still wholly
            // inside BUSINESS and PRIVATE has just been disabled. No PRIVATE
            // plan/apply step has run yet, so BUSINESS can finish independently.
            if($scope==='all' && $enabled_scope==='business' && in_array($phase,array('business_materialize','business_prune'),true)){
                $state['selection_scope']='business';
            }else{
                $state['status']='failed';$state['phase']='failed';$state['failed_at']=time();
                $state['failure_reason']='selection_route_disabled_during_run';
                $state['error']='Eine Seller-Route wurde während einer laufenden Auswahl deaktiviert; fail-closed ohne weitere Bestandsmutation.';
                return $this->ebay_selection_state_save($state);
            }
        }
        $started=microtime(true);
        if(sanitize_key((string)($state['phase']??''))==='business_materialize'){
            $this->ebay_selection_apply_business_batch($settings,$state,50);
        }elseif(sanitize_key((string)($state['phase']??''))==='business_prune'){
            $this->ebay_selection_prune_business_batch($settings,$state,50);
        }elseif(sanitize_key((string)($state['phase']??''))==='private_prune'){
            $this->ebay_selection_apply_private_post_batch($settings,$state,50);
        }elseif(sanitize_key((string)($state['phase']??''))==='private'){
            $this->ebay_selection_apply_private_batch($settings,$state,35);
        }elseif(sanitize_key((string)($state['phase']??''))==='private_verify'){
            $this->ebay_selection_verify_private_final($settings,$state);
        }
        $state['last_tick_ms']=(int)round((microtime(true)-$started)*1000);
        $this->ebay_selection_state_save($state);
        if($this->ebay_selection_state_is_open($state)){
            $owner=sanitize_text_field((string)($state['owner']??''));
            $this->ebay_selection_schedule_worker(10);
        }
        return $state;
    }


    /** Persist terminal selection acknowledgement back onto its originating
     * refresh. This closes the cross-state handshake without changing transport. */
    private function ebay_selection_ack_refresh_terminal($state) {
        $state=is_array($state)?$state:array();
        $owner=sanitize_text_field((string)($state['owner']??''));
        if(strpos($owner,'refresh:')!==0){return false;}
        $run_uuid=substr($owner,8); if($run_uuid===''){return false;}
        $refresh=$this->ebay_refresh_job_load();
        if(!is_array($refresh)||!hash_equals($run_uuid,sanitize_text_field((string)($refresh['run_uuid']??'')))){return false;}
        if(!isset($refresh['summary'])||!is_array($refresh['summary'])){$refresh['summary']=array();}
        $selection=is_array($refresh['summary']['selection']??null)?$refresh['summary']['selection']:array();
        $selection['status']=sanitize_key((string)($state['status']??''));
        $selection['phase']=sanitize_key((string)($state['phase']??''));
        $selection['scope']=sanitize_key((string)($state['selection_scope']??($selection['scope']??'')));
        $selection['owner']=$owner;
        if(!empty($state['completed_at'])){$selection['completed_at']=absint($state['completed_at']);}
        if(!empty($state['failed_at'])){$selection['failed_at']=absint($state['failed_at']);}
        if(!empty($state['failure_reason'])){$selection['failure_reason']=sanitize_key((string)$state['failure_reason']);}
        $refresh['summary']['selection']=$selection;
        $this->ebay_refresh_job_save($refresh);
        $settings=$this->ebay_settings();
        $settings['last_refresh']=$refresh['summary'];
        update_option(self::OPTION_NETWORK_EBAY,$settings,false);

        // A refresh selection may prove that the stored BUSINESS inventory does
        // not cover all required physical product concepts. V6.40 already had a
        // bounded BUSINESS-only discovery scope for exactly those missing
        // concepts, but no production path ever invoked it. That left a valid
        // selection terminal at e.g. 82/311 forever although the missing-concept
        // recovery machinery existed. Queue that existing bounded recovery only
        // after the originating refresh itself is terminal; never compete with a
        // still-open/partial refresh and never recurse from sync-owned selection.
        $this->ebay_business_gapfill_after_refresh_selection($refresh,$state,$settings);
        return true;
    }

    /** Queue at most one bounded BUSINESS-only gap-fill for a terminal refresh
     * selection. This is orchestration only: no new transport, no browser loop,
     * no source mutation in the caller request. */
    private function ebay_business_gapfill_after_refresh_selection(&$refresh,$state,$settings=null) {
        if (method_exists($this, 'ebay_run_load')) {
            $canonical = $this->ebay_run_load();
            if ((string)($canonical['schema'] ?? '') === '1.0') {
                return array('status'=>'owned_by_canonical_run','run_uuid'=>sanitize_text_field((string)($canonical['run_uuid'] ?? '')));
            }
        }
        $refresh=is_array($refresh)?$refresh:array();
        $state=is_array($state)?$state:array();
        $settings=is_array($settings)?$settings:$this->ebay_settings();
        if(sanitize_key((string)($state['status']??''))!=='complete'){return array('status'=>'not_terminal');}
        $scope=sanitize_key((string)($state['selection_scope']??''));
        if(!in_array($scope,array('all','business'),true) || empty($settings['business_enabled'])){return array('status'=>'not_required');}
        // A bounded/partial refresh must finish its own durable remote cursor
        // first. Starting discovery here would create two network owners.
        if(sanitize_key((string)($refresh['status']??''))!=='completed'){return array('status'=>'deferred_refresh_not_terminal');}

        $coverage=is_array($state['plan_stats']['business']??null)?$state['plan_stats']['business']:array();
        $required_ids=$this->ebay_business_required_product_concept_ids();
        $required=count($required_ids);$snapshot_required=absint($coverage['required']??0);
        $missing_ids=array_values(array_unique(array_filter(array_map('sanitize_key',(array)($coverage['missing_concepts']??array())))));
        if($snapshot_required!==$required){
            // Never guess from a stale/incomplete coverage snapshot. The next
            // scheduled full discovery remains the safe fallback.
            return array('status'=>'deferred_coverage_snapshot_incomplete','required'=>$required,'snapshot_required'=>$snapshot_required);
        }
        $missing=count($missing_ids);
        $owner=sanitize_text_field((string)($state['owner']??''));
        $existing=is_array($refresh['summary']['business_gapfill']??null)?$refresh['summary']['business_gapfill']:array();
        if($owner!=='' && hash_equals($owner,sanitize_text_field((string)($existing['selection_owner']??'')))
            && in_array(sanitize_key((string)($existing['status']??'')),array('queued','already_running','covered_by_existing_discovery','not_required'),true)){
            return $existing;
        }
        if($missing<=0){
            $result=array('status'=>'not_required','missing'=>0,'required'=>$required,'selection_owner'=>$owner,'recorded_at'=>time());
            $refresh['summary']['business_gapfill']=$result;$this->ebay_refresh_job_save($refresh);
            $settings['last_refresh']=$refresh['summary'];update_option(self::OPTION_NETWORK_EBAY,$settings,false);
            return $result;
        }

        $queued=$this->ebay_start_sync_job(false,'business_recovery','background');
        if(is_wp_error($queued)){
            $result=array('status'=>'failed_to_queue','missing'=>$missing,'required'=>$required,'selection_owner'=>$owner,'error_code'=>sanitize_key((string)$queued->get_error_code()),'recorded_at'=>time());
        }else{
            $sync=$this->ebay_sync_job_load();$sync_scope=sanitize_key((string)($sync['scope']??''));
            $qstatus=sanitize_key((string)($queued['status']??''));
            if($sync_scope==='business_recovery'){
                $result=array('status'=>$qstatus==='already_running'?'already_running':'queued','missing'=>$missing,'required'=>$required,'selection_owner'=>$owner,'run_uuid'=>sanitize_text_field((string)($sync['run_uuid']??$queued['run_uuid']??'')),'profiles'=>count((array)($sync['profiles']??array())),'recorded_at'=>time());
            }elseif($qstatus==='already_running' && $sync_scope==='all'){
                // A full discovery already covers every product concept, so do
                // not create a competing recovery job.
                $result=array('status'=>'covered_by_existing_discovery','missing'=>$missing,'required'=>$required,'selection_owner'=>$owner,'run_uuid'=>sanitize_text_field((string)($sync['run_uuid']??'')),'recorded_at'=>time());
            }else{
                $result=array('status'=>'failed_to_queue','missing'=>$missing,'required'=>$required,'selection_owner'=>$owner,'error_code'=>'unexpected_sync_scope','recorded_at'=>time());
            }
        }
        $refresh['summary']['business_gapfill']=$result;$this->ebay_refresh_job_save($refresh);
        $settings['last_refresh']=$refresh['summary'];update_option(self::OPTION_NETWORK_EBAY,$settings,false);
        return $result;
    }

    /**
     * Standalone bounded selection worker for recovery/maintenance/admin-owned
     * passes. It never runs concurrently with a current-build discovery or
     * refresh worker. Each request executes exactly one existing selection tick.
     */
    public function run_ebay_selection_worker($external = false) {
        $lock_key='ppar_ebay_selection_worker_lock_'.substr(hash('sha256',(string)self::EBAY_RUNTIME_BUILD),0,12);
        if(function_exists('get_transient')&&get_transient($lock_key)){return false;}
        if(function_exists('set_transient')){set_transient($lock_key,1,45);}
        $reschedule=false;
        $completed=false;
        try{
            $state=$this->ebay_selection_state_load();
            if(!$this->ebay_selection_state_is_open($state)){return false;}
            $owner=sanitize_text_field((string)($state['owner']??''));
            if(strpos($owner,'sync:')===0){return false;}

            $sync=$this->ebay_sync_job_load();
            if($this->ebay_sync_job_is_open($sync)){
                $this->ebay_selection_schedule_worker(15);
                return false;
            }
            $refresh=$this->ebay_refresh_job_load();
            if($this->ebay_refresh_job_is_open($refresh)){
                // Selection has precedence over an open refresh. The refresh
                // worker itself defers while a selection is open, so letting
                // both sides wait for each other would create a durable
                // refresh<->selection deadlock (the live 2,000/437/prepare
                // stall). Do not run concurrently with a refresh request that
                // already owns its lock; wait one tick in that narrow case.
                $refresh_lock='ppar_ebay_refresh_worker_lock_'.substr(hash('sha256',(string)self::EBAY_RUNTIME_BUILD),0,12);
                if(function_exists('get_transient')&&get_transient($refresh_lock)){
                    $this->ebay_selection_schedule_worker(10);
                    return false;
                }
            }

            $before_progress=$this->ebay_selection_progress_fingerprint($state);
            $state=$this->ebay_selection_process_tick($this->ebay_settings(),$state);
            $reschedule=$this->ebay_selection_state_is_open($state);
            if($reschedule){
                $after_progress=$this->ebay_selection_progress_fingerprint($state);
                if(hash_equals($before_progress,$after_progress)){
                    $state['worker_no_progress_count']=absint($state['worker_no_progress_count']??0)+1;
                    if(absint($state['worker_no_progress_count'])>=3){
                        $state['status']='failed';
                        $state['phase']='failed';
                        $state['failed_at']=time();
                        $state['failure_reason']='selection_worker_no_progress';
                        $state['error']='Selection-Worker hat drei aufeinanderfolgende Ticks ohne fachlichen Fortschritt erreicht.';
                        $reschedule=false;
                    }
                }else{
                    $state['worker_no_progress_count']=0;
                    $state['worker_last_progress_at']=time();
                }
                $state=$this->ebay_selection_state_save($state);
            }else{
                $state['worker_no_progress_count']=0;
                $state=$this->ebay_selection_state_save($state);
            }
            if(!$reschedule){$this->ebay_selection_ack_refresh_terminal($state);}
            $completed=!$reschedule && sanitize_key((string)($state['status']??''))==='complete';
            return $state;
        }catch(Throwable $error){
            $state=$this->ebay_selection_state_load();
            $state['status']='failed';
            $state['failed_at']=time();
            $state['error']=sanitize_text_field($error->getMessage());
            $this->ebay_selection_state_save($state);
            $this->ebay_selection_ack_refresh_terminal($state);
            return new WP_Error('ebay_selection_worker_failed',$error->getMessage());
        }finally{
            // Critical ordering: release the worker lock BEFORE dispatching the
            // next non-blocking request. Otherwise a fast loopback can arrive
            // while this request still owns the lock and silently strand the job.
            if(function_exists('delete_transient')){delete_transient($lock_key);}
            if($reschedule){
                $fresh=$this->ebay_selection_state_load();
                if($this->ebay_selection_state_is_open($fresh)){$this->ebay_selection_schedule_worker(10);}
            }elseif($completed){
                // Any completed selection that touched BUSINESS can change the
                // product set available to articles. Invalidate article plans once
                // per selection state and queue a bounded rebuild; never require
                // editors to click "Alle Ausgabepläne neu berechnen" after an eBay
                // refresh.
                $fresh=$this->ebay_selection_state_load();
                $scope=sanitize_key((string)($fresh['selection_scope']??''));
                if(in_array($scope,array('all','business'),true) && method_exists($this,'article_plan_bump_campaign_revision') && $this->article_hybrid_enabled() && empty($fresh['article_plan_revision_bumped'])){
                    $fresh['article_plan_revision_bumped']=$this->article_plan_bump_campaign_revision('ebay_business_selection_complete');
                    $this->ebay_selection_state_save($fresh);
                }
                // Cap recovery is complete. Legacy media cleanup stays bounded
                // and low-priority and is merely scheduled here.
                $this->ensure_ebay_media_cleanup_schedule();
            }
        }
    }

    /**
     * V6.19 – bounded BUSINESS inventory on top of the unchanged source/creative/
     * output architecture. Only the ranked winners are materialized publicly.
     */

    /** Pure deterministic PRIVATE cap planner; no posts/media are touched here. */
    private function ebay_private_capacity_concept_key($row, $settings) {
        $payload=json_decode((string)($row['source_payload']??''),true);$payload=is_array($payload)?$payload:array();
        $class=is_array($payload['portal_classification']??null)?$payload['portal_classification']:array();
        $raw=is_array($payload['raw']??null)?$payload['raw']:array();
        // Capacity balancing normally uses the classification persisted by the
        // discovery/maintenance workflow. Re-running the complete portal catalog
        // classifier here would make the one-time recovery itself timeout-prone.

        // A reference product in an accessory title (e.g. "Helmtasche für
        // Reithelm") must never consume a Reithelm slot. Keep the item in the
        // coarse PRIVATE bucket, but give the real accessory its own balance key.
        if($raw){
            $title=sanitize_text_field((string)($raw['title']??$row['title']??''));
            $primary=$this->ebay_business_primary_title_section($title);
            foreach(array('tasche','huelle','hulle','cover','liner','innenfutter','ersatz','adapter','halterung','visier','ueberzug','uberzug','zubehoer','zubehor','spanner','stiefelspanner','helmtasche') as $accessory){
                $a=$this->ebay_topic_text($accessory); if($a===''){continue;}
                foreach($this->ebay_topic_tokens($primary) as $token){
                    $token=$this->ebay_topic_text((string)$token);
                    if($token===$a || (strlen($token)>strlen($a) && substr($token,-strlen($a))===$a)){
                        return 'accessory-'.sanitize_key($token);
                    }
                }
            }
        }

        $concept=sanitize_key((string)($class['private_product_concept_id']??$class['product_concept_id']??''));
        if($concept!=='' && strpos($concept,'hub-concept-')!==0){return $concept;}
        // Hub concepts intentionally aggregate several real product types. For
        // PRIVATE inventory balance use the concrete matched alias/hit so that
        // Reithose, Reitjacke, Reitschuh, Reitweste, ... do not collapse into one
        // anonymous Reiterbedarf pool.
        foreach((array)($class['hits']??array()) as $hit){
            $hit=sanitize_key($this->ebay_topic_text((string)$hit));
            if($hit!==''){return 'private-hit-'.$hit;}
        }
        if($concept!==''){return $concept;}
        if($raw){
            $item=$this->ebay_accept_item($raw,'INDIVIDUAL',$settings);
            if(!is_wp_error($item)){
                $rule=$this->ebay_rule_by_id((string)($row['rule_id']??''),$settings);
                $match=$this->ebay_business_classify_portal_item_strict($item,$rule);
                if(!is_wp_error($match)){
                    $concept=sanitize_key((string)($match['product_concept_id']??''));
                    if($concept!==''){
                        if(strpos($concept,'hub-concept-')===0){
                            foreach((array)($match['hits']??array()) as $hit){$hit=sanitize_key($this->ebay_topic_text((string)$hit));if($hit!==''){return 'private-hit-'.$hit;}}
                        }
                        return $concept;
                    }
                }
            }
        }
        return 'other-'.absint($row['target_term_id']??0);
    }

    /** Pure deterministic PRIVATE cap planner; balanced by coarse leaf and product concept. */
    private function ebay_private_select_rows_for_capacity($rows, $settings = null) {
        $settings = is_array($settings) ? $this->ebay_normalize_settings($settings, true) : $this->ebay_settings();
        $leaves=array();
        foreach((array)$rows as $row){
            if(!is_array($row) || absint($row['target_term_id']??0)<=0){continue;}
            $payload=json_decode((string)($row['source_payload']??''),true); $payload=is_array($payload)?$payload:array();
            $class=is_array($payload['portal_classification']??null)?$payload['portal_classification']:array();
            $manual_bonus=!empty($class['manual_override'])?1000:0;
            $row['_rank_score']=$manual_bonus+absint($class['score']??0)+(!empty($row['image_url'])?10:0);
            $row['_capacity_concept']=$this->ebay_private_capacity_concept_key($row,$settings);
            $leaf=absint($row['target_term_id']);$concept=(string)$row['_capacity_concept'];
            $leaves[$leaf][$concept][]=$row;
        }
        $leaf_ranked=array();
        foreach($leaves as $leaf=>$concepts){
            $merged=array();
            foreach($concepts as $concept=>$group){
                usort($group,static function($a,$b){
                    if($a['_rank_score']!==$b['_rank_score'])return $a['_rank_score']>$b['_rank_score']?-1:1;
                    if(absint($a['last_seen']??0)!==absint($b['last_seen']??0))return absint($a['last_seen']??0)>absint($b['last_seen']??0)?-1:1;
                    return absint($a['id']??0)<absint($b['id']??0)?-1:1;
                });
                $size=max(1,count($group));
                foreach($group as $i=>$row){
                    // V6.28 strict breadth-first balance: every qualified product
                    // concept receives candidate 1 before any concept receives
                    // candidate 2, and candidate 2 before candidate 3. Only after
                    // three breadth rounds may larger pools gain extra depth. This
                    // prevents large helmet/hose pools from starving smaller but
                    // valid concepts such as Reitstiefel.
                    $depth=(int)$i;
                    $row['_capacity_depth']=$depth;
                    $row['_capacity_priority']=$depth < 3
                        ? (float)$depth
                        : 3.0 + (($depth - 2) / sqrt($size));
                    $merged[]=$row;
                }
            }
            usort($merged,static function($a,$b){
                $pa=(float)($a['_capacity_priority']??999999);$pb=(float)($b['_capacity_priority']??999999);
                if(abs($pa-$pb)>0.000001)return $pa<$pb?-1:1;
                if($a['_rank_score']!==$b['_rank_score'])return $a['_rank_score']>$b['_rank_score']?-1:1;
                return absint($a['id']??0)<absint($b['id']??0)?-1:1;
            });
            $leaf_ranked[$leaf]=$merged;
        }
        $global=min(250,max(50,absint($settings['private_active_cap']??250)));$per_leaf=max(5,absint($settings['private_leaf_cap']??30));
        $selected=array();
        // Fair across the eight coarse HivePress leaves; within each leaf use the
        // weighted product-concept ranking above. Thus a large helmet/boot pool
        // can receive several slots without swallowing the whole leaf.
        for($rank=0;$rank<$per_leaf && count($selected)<$global;$rank++){
            foreach($leaf_ranked as $leaf=>$group){
                if(count($selected)>=$global){break;}
                if(!isset($group[$rank])){continue;}
                $row=$group[$rank];$item=(string)($row['item_id']??'');
                if($item===''||isset($selected[$item])){continue;}
                $selected[$item]=$row;
            }
        }
        // V6.26: private_leaf_cap is the balanced first-pass target, not a
        // portal-wide starvation ceiling. If some coarse leaves are sparse, use
        // qualified leftovers from richer leaves in further fair rounds until
        // the global cap is filled. Hard quality/policy gates still apply before
        // rows reach this planner.
        $rank=$per_leaf;
        while(count($selected)<$global){
            $added=0;
            foreach($leaf_ranked as $leaf=>$group){
                if(count($selected)>=$global){break;}
                if(!isset($group[$rank])){continue;}
                $row=$group[$rank];$item=(string)($row['item_id']??'');
                if($item===''||isset($selected[$item])){continue;}
                $selected[$item]=$row;$added++;
            }
            if($added===0){break;}
            $rank++;
        }
        return $selected;
    }

    /** V6.19 – PRIVATE remains the same HivePress route, only inventory size is bounded. */


    private function ebay_rule_target_term($rule, $settings) {
        if (!function_exists('taxonomy_exists') || !taxonomy_exists('hp_listing_category') || !function_exists('get_term_by')) {
            return new WP_Error('ebay_hivepress_missing', 'HivePress-Kategorietaxonomie fehlt.');
        }
        $root_id = absint($settings['private_root_term_id'] ?? 0);
        $root = $root_id > 0 ? get_term($root_id, 'hp_listing_category') : null;
        if (!$root || is_wp_error($root)) { return new WP_Error('ebay_private_root_missing', 'Wurzel „Private Anzeigen“ fehlt.'); }
        $slug = sanitize_title((string) ($rule['target_term_slug'] ?? ''));
        $term = $slug !== '' ? get_term_by('slug', $slug, 'hp_listing_category') : false;
        if (!$term || is_wp_error($term)) { return new WP_Error('ebay_private_target_missing', 'HivePress-Zielkategorie fehlt: ' . $slug); }
        $term_id = absint($term->term_id ?? 0);
        $validated = $this->ebay_validate_private_target_term_id($term_id, $settings);
        if (is_wp_error($validated)) { return $validated; }
        return absint($validated->term_id ?? 0);
    }

    private function ebay_db_formats($data) {
        $integer_fields = array_flip(array('target_term_id','listing_post_id','item_end_at','source_checked_at','last_seen','fresh_until','created_at','updated_at'));
        $formats = array();
        foreach (array_keys((array) $data) as $field) { $formats[] = isset($integer_fields[$field]) ? '%d' : '%s'; }
        return $formats;
    }

    private function ebay_upsert_item($item, $rule, $route_mode, $target_term_id, $settings) {
        global $wpdb;
        $table = $this->ebay_items_table();
        $portal_key = method_exists($this, 'output_local_portal_key') ? $this->output_local_portal_key() : 'local';
        $now = time();
        $existing = $wpdb->get_row($wpdb->prepare("SELECT * FROM {$table} WHERE portal_key=%s AND item_id=%s", $portal_key, (string) $item['item_id']), ARRAY_A);
        $data = array(
            'portal_key'=>$portal_key,
            'item_id'=>(string) $item['item_id'],
            'legacy_item_id'=>(string) $item['legacy_item_id'],
            'seller_account_type'=>(string) $item['seller_account_type'],
            'seller_username'=>(string) $item['seller_username'],
            'route_mode'=>sanitize_key((string) $route_mode),
            'rule_id'=>sanitize_key((string) ($rule['id'] ?? '')),
            'target_term_id'=>absint($target_term_id),
            'title'=>(string) $item['title'],
            'short_description'=>(string) $item['short_description'],
            'condition_text'=>(string) $item['condition_text'],
            'price_value'=>(string) $item['price_value'],
            'currency'=>(string) $item['currency'],
            'shipping_value'=>(string) $item['shipping_value'],
            'location_text'=>(string) $item['location_text'],
            'affiliate_url'=>(string) $item['affiliate_url'],
            'item_web_url'=>(string) $item['item_web_url'],
            'image_url'=>(string) $item['image_url'],
            'item_end_at'=>absint($item['item_end_at']),
            'source_hash'=>(string) $item['source_hash'],
            'source_payload'=>wp_json_encode(array('raw'=>$item['raw'],'portal_classification'=>(array) ($item['portal_classification'] ?? array()),'business_quality'=>(array) ($item['business_quality'] ?? array()),'business_selection'=>(array) ($item['business_selection'] ?? array())), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES),
            'status'=>'active',
            'source_state'=>'available',
            'policy_state'=>'allowed',
            'route_state'=>'ready',
            'output_state'=>(strtoupper(sanitize_key((string) ($item['seller_account_type'] ?? ''))) === 'INDIVIDUAL' ? 'listing_pending' : 'creative_pending'),
            'policy_version'=>self::EBAY_CONTENT_POLICY_VERSION,
            'classifier_version'=>(strtoupper(sanitize_key((string) ($item['seller_account_type'] ?? ''))) === 'INDIVIDUAL' ? self::EBAY_PRIVATE_CLASSIFIER_VERSION : self::EBAY_BUSINESS_CLASSIFIER_VERSION),
            'source_checked_at'=>$now,
            'rejection_reason'=>'',
            'last_seen'=>$now,
            'fresh_until'=>$now + 6 * HOUR_IN_SECONDS,
            'updated_at'=>$now,
        );
        if ($existing) {
            $data['listing_post_id'] = absint($existing['listing_post_id'] ?? 0);
            $data['creative_identity_hash'] = sanitize_text_field((string) ($existing['creative_identity_hash'] ?? ''));
            $wpdb->update($table, $data, array('id'=>absint($existing['id'])), $this->ebay_db_formats($data), array('%d'));
            return $wpdb->get_row($wpdb->prepare("SELECT * FROM {$table} WHERE id=%d", absint($existing['id'])), ARRAY_A);
        }
        $data['listing_post_id'] = 0;
        $data['creative_identity_hash'] = '';
        $data['created_at'] = $now;
        $wpdb->insert($table, $data, $this->ebay_db_formats($data));
        if (!$wpdb->insert_id) { return new WP_Error('ebay_item_save_failed', 'eBay-Datensatz konnte nicht gespeichert werden.'); }
        return $wpdb->get_row($wpdb->prepare("SELECT * FROM {$table} WHERE id=%d", absint($wpdb->insert_id)), ARRAY_A);
    }

    private function ebay_listing_content($item) {
        $price = trim((string) $item['price_value'] . ' ' . (string) $item['currency']);
        $rows = array();
        if ($price !== '') { $rows[] = '<li><strong>Preis:</strong> ' . esc_html($price) . '</li>'; }
        if (!empty($item['condition_text'])) { $rows[] = '<li><strong>Zustand:</strong> ' . esc_html((string) $item['condition_text']) . '</li>'; }
        if ($item['shipping_value'] !== '') { $rows[] = '<li><strong>Versand:</strong> ' . esc_html((string) $item['shipping_value'] . ' ' . (string) $item['currency']) . '</li>'; }
        if (!empty($item['location_text'])) { $rows[] = '<li><strong>Artikelstandort:</strong> ' . esc_html((string) $item['location_text']) . '</li>'; }
        if (!empty($item['seller_username'])) { $rows[] = '<li><strong>eBay-Verkäufer:</strong> ' . esc_html((string) $item['seller_username']) . '</li>'; }
        if (!empty($item['item_end_at'])) { $rows[] = '<li><strong>Angebotsende:</strong> ' . esc_html(wp_date('d.m.Y H:i', absint($item['item_end_at']))) . '</li>'; }
        $description = trim((string) $item['short_description']);
        $out = '<p><strong>Privates eBay-Angebot</strong></p><p><small><strong>Affiliate-Anzeige:</strong> Bei einem Kauf über den Link kann das Portal eine Provision erhalten. Für Käufer entstehen keine Mehrkosten.</small></p>';
        if ($description !== '') { $out .= '<p>' . esc_html($description) . '</p>'; }
        if ($rows) { $out .= '<ul>' . implode('', $rows) . '</ul>'; }
        $out .= '<p><a href="' . esc_url((string) $item['affiliate_url']) . '" rel="sponsored nofollow noopener" target="_blank">Angebot bei eBay ansehen</a></p>';
        $out .= '<p><small>Beim Klick wechselst du zu eBay. Maßgeblich sind Preis, Verfügbarkeit und Angaben im eBay-Angebot.</small></p>';
        return $out;
    }

    /**
     * Validate eBay-hosted images without fetching them. PRIVATE eBay listings
     * render these URLs directly; they are never copied into wp-content/uploads.
     */
    private function ebay_remote_image_url_validate($url) {
        $url = esc_url_raw((string) $url);
        if ($url === '') { return ''; }
        $scheme = strtolower((string) parse_url($url, PHP_URL_SCHEME));
        $host = strtolower(rtrim((string) parse_url($url, PHP_URL_HOST), '.'));
        if ($scheme !== 'https' || $host === '') { return ''; }
        $catalog = $this->ebay_portal_catalog();
        if (is_wp_error($catalog)) { return ''; }
        $policy = is_array($catalog['content_policy'] ?? null) ? $catalog['content_policy'] : array();
        $suffixes = array_values(array_filter(array_map('strtolower', (array) ($policy['remote_image_host_suffixes'] ?? array('ebayimg.com')))));
        foreach ($suffixes as $suffix) {
            $suffix = ltrim(rtrim((string) $suffix, '.'), '.');
            if ($suffix === '') { continue; }
            if ($host === $suffix || substr($host, -strlen('.' . $suffix)) === '.' . $suffix) { return $url; }
        }
        return '';
    }

    /**
     * Compatibility name retained for old tests/callers. Since V6.12 this does
     * not sideload anything: it stores only the verified remote image URL.
     */
    private function ebay_sideload_listing_image($listing_id, $item) {
        $listing_id = absint($listing_id);
        $item = is_array($item) ? $item : array();
        $image_url = $this->ebay_remote_image_url_validate((string) ($item['image_url'] ?? ''));
        if ($listing_id <= 0 || $image_url === '') {
            return new WP_Error('ebay_listing_image_missing', 'eBay-Listingbild fehlt oder stammt nicht von einer freigegebenen eBay-Bildquelle.');
        }
        update_post_meta($listing_id, '_ppar_ebay_remote_image_url', $image_url);
        update_post_meta($listing_id, '_ppar_ebay_remote_image_mode', 'remote_only_v1');

        // Do not delete the legacy attachment in the request that materializes a
        // listing. Merely stop HivePress from using it as featured image; the
        // bounded cleanup worker removes plugin-owned legacy media safely.
        $thumb = function_exists('get_post_thumbnail_id') ? absint(get_post_thumbnail_id($listing_id)) : 0;
        if ($thumb > 0
            && (string) get_post_meta($thumb, '_ppar_ebay_item_id', true) !== ''
            && (string) get_post_meta($thumb, '_ppar_ebay_item_id', true) === sanitize_text_field((string) ($item['item_id'] ?? ''))
            && function_exists('delete_post_thumbnail')) {
            delete_post_thumbnail($listing_id);
        }
        return 0;
    }

    /** Resolve remote image for an eBay listing; frontend reads never mutate. */
    private function ebay_remote_listing_image_url($listing_id) {
        $listing_id = absint($listing_id);
        $item_id = sanitize_text_field((string) get_post_meta($listing_id, '_ppar_ebay_item_id', true));
        if ($listing_id <= 0 || $item_id === '') { return ''; }

        // Current V6.12+ listings persist the verified remote URL directly.
        $url = $this->ebay_remote_image_url_validate((string) get_post_meta($listing_id, '_ppar_ebay_remote_image_url', true));
        if ($url !== '') { return $url; }

        // Transitional fallback while a legacy attachment still exists.
        $thumb = function_exists('get_post_thumbnail_id') ? absint(get_post_thumbnail_id($listing_id)) : 0;
        if ($thumb > 0) {
            $url = $this->ebay_remote_image_url_validate((string) get_post_meta($thumb, '_ppar_ebay_source_url', true));
            if ($url !== '') { return $url; }
        }

        // V6.14 recovery: deleting old importer attachments must not blank PRIVATE
        // cards. The durable eBay source row already stores the original image URL.
        // Public archive queries populate this request-local cache in one bounded
        // query. A direct single/preview may miss that prefetch, so only then do
        // we resolve this one item explicitly. No frontend write and no sideload.
        $source_row = is_array($this->ebay_public_source_row_cache[$item_id] ?? null)
            ? $this->ebay_public_source_row_cache[$item_id]
            : array();
        if (!$source_row) {
            $resolved = $this->ebay_public_source_rows_by_item_ids(array($item_id), 'INDIVIDUAL');
            $source_row = is_array($resolved[$item_id] ?? null) ? $resolved[$item_id] : array();
        }
        if (!$source_row) { return ''; }
        if (sanitize_text_field((string)($source_row['item_id'] ?? '')) !== $item_id) { return ''; }
        if (strtoupper(sanitize_key((string)($source_row['seller_account_type'] ?? ''))) !== 'INDIVIDUAL') { return ''; }
        $source_listing_id = absint($source_row['listing_post_id'] ?? 0);
        if ($source_listing_id > 0 && $source_listing_id !== $listing_id) { return ''; }
        if (sanitize_key((string)($source_row['source_state'] ?? 'available')) === 'ended') { return ''; }
        if (sanitize_key((string)($source_row['policy_state'] ?? 'allowed')) === 'blocked') { return ''; }

        $source_url = (string)($source_row['image_url'] ?? '');
        if ($source_url === '') {
            $payload = json_decode((string)($source_row['source_payload'] ?? ''), true);
            $raw = is_array($payload) && is_array($payload['raw'] ?? null) ? $payload['raw'] : array();
            $source_url = (string)($raw['image']['imageUrl'] ?? '');
        }
        return $this->ebay_remote_image_url_validate($source_url);
    }

    private function ebay_remote_listing_image_html($listing, $context = 'block') {
        if (!is_object($listing) || !method_exists($listing, 'get_id')) { return ''; }
        $listing_id = absint($listing->get_id());
        $url = $this->ebay_remote_listing_image_url($listing_id);
        if ($url === '') { return ''; }
        $title = method_exists($listing, 'get_title') ? (string) $listing->get_title() : (function_exists('get_the_title') ? (string) get_the_title($listing_id) : 'eBay-Angebot');
        $permalink = function_exists('get_permalink') ? (string) get_permalink($listing_id) : '';
        if (function_exists('hivepress')) {
            $hp = hivepress();
            if (is_object($hp) && isset($hp->router) && is_object($hp->router) && method_exists($hp->router, 'get_url')) {
                $candidate = $hp->router->get_url('listing_view_page', array('listing_id'=>$listing_id));
                if (is_string($candidate) && $candidate !== '') { $permalink = $candidate; }
            }
        }
        $block_ratio = ''; $page_ratio = '';
        if (function_exists('hivepress')) {
            $hp = hivepress();
            if (is_object($hp) && isset($hp->asset) && is_object($hp->asset) && method_exists($hp->asset, 'get_aspect_ratio')) {
                $block_ratio = (string) $hp->asset->get_aspect_ratio('landscape_small');
                $page_ratio = (string) $hp->asset->get_aspect_ratio('landscape_large');
            }
        }
        if ($context === 'page') {
            $zoom = get_option('hp_listing_enable_image_zoom') ? ' data-zoom="' . esc_url($url) . '"' : '';
            $ratio = $page_ratio !== '' ? ' data-aspect-ratio="' . esc_attr($page_ratio) . '"' : '';
            return '<div class="hp-listing__images ppar-ebay-remote-images" data-component="carousel-slider"' . $ratio . '><img src="' . esc_url($url) . '"' . $zoom . ' alt="' . esc_attr($title) . '" loading="lazy" decoding="async"></div>';
        }
        $ratio = $block_ratio !== '' ? ' data-aspect-ratio="' . esc_attr($block_ratio) . '"' : '';
        return '<div class="hp-listing__image ppar-ebay-remote-image" data-component="carousel-slider" data-preview="false"' . $ratio . ' data-url="' . esc_url($permalink) . '"><a href="' . esc_url($permalink) . '"><img src="' . esc_url($url) . '" alt="' . esc_attr($title) . '" loading="lazy" decoding="async"></a></div>';
    }

    private function ebay_remote_image_replace_template_block($blocks, $template, $block_name, $context) {
        if (!is_array($blocks) || !is_object($template) || !method_exists($template, 'get_context')) { return $blocks; }
        $listing = $template->get_context('listing');
        if (!is_object($listing) || !method_exists($listing, 'get_id')) { return $blocks; }
        $listing_id = absint($listing->get_id());
        if ($listing_id <= 0 || (string) get_post_meta($listing_id, '_ppar_ebay_item_id', true) === '') { return $blocks; }
        $html = $this->ebay_remote_listing_image_html($listing, $context);
        if ($html === '' || !function_exists('hivepress')) { return $blocks; }
        $hp = hivepress();
        if (!is_object($hp) || !isset($hp->template) || !is_object($hp->template) || !method_exists($hp->template, 'merge_blocks')) { return $blocks; }
        return $hp->template->merge_blocks($blocks, array(
            $block_name=>array('type'=>'content','content'=>$html),
        ));
    }

    public function ebay_remote_image_listing_view_block($blocks, $template) {
        return $this->ebay_remote_image_replace_template_block($blocks, $template, 'listing_image', 'block');
    }

    public function ebay_remote_image_listing_view_page($blocks, $template) {
        return $this->ebay_remote_image_replace_template_block($blocks, $template, 'listing_images', 'page');
    }

    /**
     * V6.15 runtime fallback at HivePress' real Container boundary.
     *
     * HivePress can render listing templates through two paths: the default
     * Listing_View_* PHP template classes, or a saved hp_template handled by
     * the editor. The class-specific /templates/.../blocks filters are not a
     * sufficient public-image contract for both paths. Every final block tree,
     * however, is materialized through HivePress\Blocks\Container. At that
     * point the complete context and named child blocks are present.
     *
     * This callback only mutates the two canonical HivePress image block names
     * and only for eBay PRIVATE listings. It performs no frontend writes and it
     * never creates an attachment.
     */
    public function ebay_remote_image_container_blocks($props, $block = null) {
        if (!is_array($props)) { return $props; }
        $context = is_array($props['context'] ?? null) ? $props['context'] : array();
        $listing = $context['listing'] ?? null;
        if (!is_object($listing) || !method_exists($listing, 'get_id')) { return $props; }

        $listing_id = absint($listing->get_id());
        if ($listing_id <= 0 || (string) get_post_meta($listing_id, '_ppar_ebay_item_id', true) === '') { return $props; }
        if (strtoupper(sanitize_key((string) get_post_meta($listing_id, '_ppar_ebay_seller_type', true))) !== 'INDIVIDUAL') { return $props; }

        $replace_tree = function($tree) use (&$replace_tree, $listing) {
            if (!is_array($tree)) { return $tree; }
            foreach ($tree as $name => $args) {
                if (!is_array($args)) { continue; }
                if ($name === 'listing_image' || $name === 'listing_images') {
                    $context_name = $name === 'listing_images' ? 'page' : 'block';
                    $html = $this->ebay_remote_listing_image_html($listing, $context_name);
                    if ($html === '') { continue; }
                    $replacement = array(
                        'type' => 'content',
                        'content' => $html,
                    );
                    foreach (array('_order', '_label', '_capability') as $meta_key) {
                        if (array_key_exists($meta_key, $args)) { $replacement[$meta_key] = $args[$meta_key]; }
                    }
                    $tree[$name] = $replacement;
                    continue;
                }
                foreach (array('blocks', 'header', 'footer') as $child_key) {
                    if (isset($args[$child_key]) && is_array($args[$child_key])) {
                        $args[$child_key] = $replace_tree($args[$child_key]);
                    }
                }
                $tree[$name] = $args;
            }
            return $tree;
        };

        foreach (array('blocks', 'header', 'footer') as $tree_key) {
            if (isset($props[$tree_key]) && is_array($props[$tree_key])) {
                $props[$tree_key] = $replace_tree($props[$tree_key]);
            }
        }
        return $props;
    }

    private function ebay_private_control_gate($seller_username, $target_term_id = 0, $listing_id = 0) {
        if (!method_exists($this, 'output_local_portal_key')) { return true; }
        $portal_key = sanitize_key((string) $this->output_local_portal_key());
        if ($portal_key === '') { return new WP_Error('ebay_control_portal_missing', 'Portalkontext für Chefsteuerung fehlt.'); }
        if (method_exists($this, 'control_emergency_stop_active') && $this->control_emergency_stop_active()) {
            return new WP_Error('ebay_control_emergency_stop', 'Globale Affiliate-Notabschaltung ist aktiv.');
        }
        $seller = preg_replace('/[^0-9A-Za-z._-]/', '', (string) $seller_username);
        if ($seller === '') { return new WP_Error('ebay_control_seller_missing', 'eBay-Verkäuferidentität für Chefsteuerung fehlt.'); }
        if (method_exists($this, 'control_partner_gate')) {
            $partner_gate = $this->control_partner_gate(
                array('provider'=>'ebay','partner_external_id'=>$seller),
                array('key'=>$portal_key)
            );
            if (is_wp_error($partner_gate)) { return $partner_gate; }
        }
        if (absint($target_term_id) > 0 && method_exists($this, 'control_target_gate')) {
            $target_gate = $this->control_target_gate($portal_key, 'hp_listing_category:' . absint($target_term_id));
            if (is_wp_error($target_gate)) { return $target_gate; }
        }
        if (absint($listing_id) > 0 && method_exists($this, 'control_output_gate')) {
            $output_gate = $this->control_output_gate($portal_key, 'ebay-listing:' . absint($listing_id));
            if (is_wp_error($output_gate)) { return $output_gate; }
        }
        return true;
    }

    /**
     * HivePress requires listing.user (post_author). Background workers have no
     * logged-in user, so eBay listings need a persistent technical owner.
     */
    private function ebay_listing_author_id($settings = array()) {
        $settings = is_array($settings) ? $settings : $this->ebay_settings();
        $candidates = array(absint($settings['private_listing_author_id'] ?? 0));
        if (function_exists('get_current_user_id')) { $candidates[] = absint(get_current_user_id()); }
        foreach ($candidates as $candidate) {
            if ($candidate <= 0) { continue; }
            if (function_exists('get_userdata')) {
                $user = get_userdata($candidate);
                if (!$user) { continue; }
            }
            if (function_exists('user_can') && !user_can($candidate, 'edit_posts')) { continue; }
            return $candidate;
        }
        if (function_exists('get_users')) {
            $ids = get_users(array('role__in'=>array('administrator','editor'),'number'=>1,'fields'=>'ids','orderby'=>'ID','order'=>'ASC'));
            foreach ((array) $ids as $candidate) {
                $candidate = absint($candidate);
                if ($candidate > 0) { return $candidate; }
            }
        }
        return 0;
    }

    private function ebay_persist_listing_author_id(&$settings) {
        $author_id = $this->ebay_listing_author_id($settings);
        if ($author_id <= 0) { return new WP_Error('ebay_hivepress_owner_missing', 'Für eBay-HivePress-Listings konnte kein gültiger technischer WordPress-Besitzer ermittelt werden.'); }
        if (absint($settings['private_listing_author_id'] ?? 0) !== $author_id) {
            $settings['private_listing_author_id'] = $author_id;
            update_option(self::OPTION_NETWORK_EBAY, $settings, false);
        }
        return $author_id;
    }

    private function ebay_secure_preview_url($post_id) {
        $post_id = absint($post_id);
        if ($post_id <= 0 || !function_exists('home_url') || !function_exists('add_query_arg') || !function_exists('wp_nonce_url')) { return ''; }
        $url = add_query_arg(array('ppar_ebay_listing_preview'=>$post_id), home_url('/'));
        return wp_nonce_url($url, 'ppar_ebay_listing_preview_' . $post_id, '_ppar_ebay_preview_nonce');
    }

    private function ebay_admin_preview_url($post_id, $base_preview_link = '') {
        return $this->ebay_secure_preview_url($post_id);
    }

    /**
     * WordPress' standard draft preview is not a supported HivePress listing route.
     * For eBay listings we therefore replace only the preview URL with a secure
     * plugin endpoint that renders HivePress' real listing_view_page template.
     */
    public function ebay_filter_preview_post_link($preview_link, $post) {
        if (!is_object($post) || (string) ($post->post_type ?? '') !== 'hp_listing') { return $preview_link; }
        $post_id = absint($post->ID ?? 0);
        if ($post_id <= 0 || (string) get_post_meta($post_id, '_ppar_ebay_item_id', true) === '') { return $preview_link; }
        if (!function_exists('current_user_can') || !current_user_can('edit_post', $post_id)) { return $preview_link; }
        $url = $this->ebay_secure_preview_url($post_id);
        return $url !== '' ? $url : $preview_link;
    }

    /**
     * Resolve an eBay listing for an authenticated admin preview. Public eBay
     * freshness is deliberately not a prerequisite here: a stale/ended tombstone
     * may still be inspected by a user who can edit that post, but it remains
     * unavailable to anonymous visitors and is clearly marked in the preview.
     */
    private function ebay_admin_preview_listing_post($post_id) {
        $post_id = absint($post_id);
        if ($post_id <= 0 || !function_exists('get_post')) { return null; }
        $post = get_post($post_id);
        if (!is_object($post) || (string) ($post->post_type ?? '') !== 'hp_listing') { return null; }
        if ((string) get_post_meta($post_id, '_ppar_ebay_item_id', true) === '') { return null; }
        if (!in_array((string) ($post->post_status ?? ''), array('draft','pending','publish','private'), true)) { return null; }
        return $post;
    }

    /**
     * Resolve a publicly renderable eBay listing. This is the hard public gate:
     * only published, active, not-ended and control-approved items pass. Source
     * freshness schedules verification but never hides Last-Known-Good inventory.
     */
    private function ebay_public_listing_post($post_id) {
        $post = $this->ebay_admin_preview_listing_post($post_id);
        if (!$post || (string) ($post->post_status ?? '') !== 'publish') { return null; }
        $post_id = absint($post->ID ?? 0);

        $lifecycle = sanitize_key((string) get_post_meta($post_id, '_ppar_ebay_lifecycle_state', true));
        if ($lifecycle !== 'active') { return null; }
        $now = time();
        $end_at = absint(get_post_meta($post_id, '_ppar_ebay_item_end_at', true));
        if ($end_at > 0 && $end_at <= $now) { return null; }

        $seller = (string) get_post_meta($post_id, '_ppar_ebay_seller_username', true);
        $target_term_id = absint(get_post_meta($post_id, '_ppar_ebay_target_term_id', true));
        $control_gate = $this->ebay_private_control_gate($seller, $target_term_id, $post_id);
        if (is_wp_error($control_gate)) { return null; }
        return $post;
    }

    /** Backward-compatible internal alias for the previous public gate name. */
    private function ebay_previewable_listing_post($post_id) {
        return $this->ebay_public_listing_post($post_id);
    }

    /**
     * Render a private eBay draft with HivePress' own listing_view_page template.
     * This endpoint never changes post_status and never makes the draft public.
     */
    /**
     * Render an eBay listing with HivePress' own listing_view_page template.
     * This is used for the protected draft preview and only as a scoped 404
     * rescue for a canonical, already published eBay listing.
     */
    private function ebay_render_hivepress_listing_page($post, $preview = false) {
        if (!is_object($post) || (string) ($post->post_type ?? '') !== 'hp_listing') {
            if (function_exists('wp_die')) { wp_die('Ungültiger HivePress-Listingdatensatz.', 'eBay-Listing', array('response'=>500)); }
            exit;
        }
        $post_id = absint($post->ID ?? 0);
        if ($post_id <= 0 || !function_exists('hivepress') || !class_exists('\\HivePress\\Models\\Listing') || !class_exists('\\HivePress\\Blocks\\Template')) {
            if (function_exists('wp_die')) { wp_die('HivePress ist für diese eBay-Anzeige nicht verfügbar.', 'eBay-Listing', array('response'=>500)); }
            exit;
        }

        $listing = \HivePress\Models\Listing::query()->get_by_id($post_id);
        if (!$listing) {
            if (function_exists('wp_die')) { wp_die('Der HivePress-Datensatz für diese eBay-Anzeige konnte nicht geladen werden.', 'eBay-Listing', array('response'=>500)); }
            exit;
        }
        // Mirrors HivePress Controller_Listing::redirect_listing_view_page().
        if (method_exists($listing, 'get_images__id')) { $listing->get_images__id(); }
        $vendor = method_exists($listing, 'get_vendor') ? $listing->get_vendor() : null;
        $hp = hivepress();
        if (is_object($hp) && isset($hp->request) && is_object($hp->request) && method_exists($hp->request, 'set_context')) {
            $hp->request->set_context('listing', $listing);
            $hp->request->set_context('vendor', $vendor);
        }

        $GLOBALS['post'] = $post;
        if (function_exists('setup_postdata')) { setup_postdata($post); }
        foreach (array('wp_query','wp_the_query') as $global_name) {
            if (!isset($GLOBALS[$global_name]) || !is_object($GLOBALS[$global_name])) { continue; }
            $query = $GLOBALS[$global_name];
            $query->posts = array($post);
            $query->post = $post;
            $query->post_count = 1;
            $query->found_posts = 1;
            $query->max_num_pages = 1;
            $query->queried_object = $post;
            $query->queried_object_id = $post_id;
            foreach (array(
                'is_single'=>true,
                'is_singular'=>true,
                'is_preview'=>(bool) $preview,
                'is_404'=>false,
                'is_home'=>false,
                'is_archive'=>false,
                'is_post_type_archive'=>false,
                'is_tax'=>false,
                'is_page'=>false,
            ) as $property=>$value) {
                if (property_exists($query, $property)) { $query->{$property} = $value; }
            }
        }

        if (function_exists('status_header')) { status_header(200); }
        if ($preview && function_exists('nocache_headers')) { nocache_headers(); }
        if (function_exists('get_header')) { get_header(); }
        if ($preview) {
            $state = sanitize_key((string) get_post_meta($post_id, '_ppar_ebay_lifecycle_state', true));
            $end_at = absint(get_post_meta($post_id, '_ppar_ebay_item_end_at', true));
            $public_ok = ($state === 'active' && ($end_at <= 0 || $end_at > time()));
            $status_text = $public_ok ? 'oeffentliche Last-Known-Good-Ausgabe aktiv' : 'nur Verwaltungsansicht – Angebot nicht oeffentlich aktiv';
            echo '<div class="ppar-ebay-preview-notice" style="max-width:1200px;margin:18px auto;padding:10px 16px;border:1px solid #c3c4c7;background:#fff"><strong>eBay-Vorschau:</strong> Nur für berechtigte Administratoren sichtbar. Der Datensatz bleibt unveröffentlicht. <small>' . esc_html($status_text) . '</small></div>';
        }
        echo (new \HivePress\Blocks\Template(array(
            'template'=>'listing_view_page',
            'context'=>array('listing'=>$listing,'vendor'=>$vendor),
        )))->render();
        if (function_exists('get_footer')) { get_footer(); }
        if (function_exists('wp_reset_postdata')) { wp_reset_postdata(); }
        exit;
    }

    /**
     * Protected eBay draft preview. It accepts both the plugin-owned nonce URL
     * and WordPress' actual backend preview query-string. Neither path changes
     * the post status or exposes a draft to anonymous visitors.
     */
    public function ebay_handle_secure_listing_preview() {
        if (function_exists('is_admin') && is_admin()) { return; }

        $secure_post_id = isset($_GET['ppar_ebay_listing_preview']) ? absint($_GET['ppar_ebay_listing_preview']) : 0;
        $native_post_id = 0;
        $preview_flag = isset($_GET['preview']) ? strtolower((string) wp_unslash($_GET['preview'])) : '';
        $requested_type = isset($_GET['post_type']) ? sanitize_key((string) wp_unslash($_GET['post_type'])) : '';
        if ($secure_post_id <= 0 && in_array($preview_flag, array('1','true'), true)) {
            $candidate_id = isset($_GET['p']) ? absint($_GET['p']) : 0;
            if ($candidate_id <= 0 && isset($_GET['preview_id'])) { $candidate_id = absint($_GET['preview_id']); }
            if ($candidate_id > 0) {
                $candidate = function_exists('get_post') ? get_post($candidate_id) : null;
                if (is_object($candidate) && (string) ($candidate->post_type ?? '') === 'hp_listing' && ($requested_type === '' || $requested_type === 'hp_listing')) {
                    $native_post_id = $candidate_id;
                }
            }
        }
        $post_id = $secure_post_id > 0 ? $secure_post_id : $native_post_id;
        if ($post_id <= 0) { return; }

        // Only our eBay listings may be intercepted. Native previews of ordinary
        // HivePress listings remain entirely owned by WordPress/HivePress.
        if ((string) get_post_meta($post_id, '_ppar_ebay_item_id', true) === '') { return; }

        if (!function_exists('is_user_logged_in') || !is_user_logged_in() || !function_exists('current_user_can') || !current_user_can('edit_post', $post_id)) {
            if (function_exists('wp_die')) { wp_die('Keine Berechtigung für diese eBay-Vorschau.', 'eBay-Vorschau', array('response'=>403)); }
            exit;
        }
        if ($secure_post_id > 0) {
            $nonce = isset($_GET['_ppar_ebay_preview_nonce']) ? (string) wp_unslash($_GET['_ppar_ebay_preview_nonce']) : '';
            if ($nonce === '' || !function_exists('wp_verify_nonce') || !wp_verify_nonce($nonce, 'ppar_ebay_listing_preview_' . $post_id)) {
                if (function_exists('wp_die')) { wp_die('Ungültiger oder abgelaufener Vorschau-Link.', 'eBay-Vorschau', array('response'=>403)); }
                exit;
            }
        }

        $preview_post = $this->ebay_admin_preview_listing_post($post_id);
        if (!$preview_post) {
            if (function_exists('wp_die')) { wp_die('Dieser eBay-HivePress-Datensatz ist nicht mehr vorhanden oder nicht vorschaufähig.', 'eBay-Vorschau', array('response'=>410)); }
            exit;
        }
        $this->ebay_render_hivepress_listing_page($preview_post, true);
    }

    /** Normalize a request/permalink path without changing its URL semantics. */
    private function ebay_normalize_request_path($path) {
        $path = rawurldecode((string) $path);
        $path = '/' . ltrim($path, '/');
        if (function_exists('untrailingslashit')) { $path = untrailingslashit($path); }
        else { $path = rtrim($path, '/'); }
        return $path === '' ? '/' : $path;
    }

    /**
     * Render the exact canonical URL of a published eBay listing directly with
     * HivePress' listing template. This intentionally does not depend on the
     * current rewrite cache or on WordPress/HivePress having recognised the
     * singular query first. It is scoped to canonical eBay listing URLs only;
     * ordinary HivePress listings are never intercepted.
     */
    public function ebay_rescue_published_listing_route() {
        if (function_exists('is_admin') && is_admin()) { return; }
        $method = strtoupper((string) ($_SERVER['REQUEST_METHOD'] ?? 'GET'));
        if (!in_array($method, array('GET','HEAD'), true)) { return; }
        if (!function_exists('get_page_by_path') || !function_exists('get_permalink')) { return; }

        $request_uri = (string) ($_SERVER['REQUEST_URI'] ?? '');
        $request_path = function_exists('wp_parse_url') ? wp_parse_url($request_uri, PHP_URL_PATH) : parse_url($request_uri, PHP_URL_PATH);
        $request_path = $this->ebay_normalize_request_path((string) $request_path);
        if ($request_path === '/') { return; }

        $parts = array_values(array_filter(explode('/', trim($request_path, '/')), 'strlen'));
        $slug = $parts ? sanitize_title(rawurldecode((string) end($parts))) : '';
        if ($slug === '') { return; }

        $post = get_page_by_path($slug, defined('OBJECT') ? OBJECT : 'OBJECT', 'hp_listing');
        if (!is_object($post) || (string) ($post->post_type ?? '') !== 'hp_listing' || (string) ($post->post_status ?? '') !== 'publish') { return; }
        $post_id = absint($post->ID ?? 0);
        if ($post_id <= 0 || (string) get_post_meta($post_id, '_ppar_ebay_item_id', true) === '') { return; }

        // Exact canonical-path equality is the hard scope boundary. A coincidental
        // slug on any other path must never be intercepted.
        $canonical = (string) get_permalink($post_id);
        $canonical_path = function_exists('wp_parse_url') ? wp_parse_url($canonical, PHP_URL_PATH) : parse_url($canonical, PHP_URL_PATH);
        if ($this->ebay_normalize_request_path((string) $canonical_path) !== $request_path) { return; }

        $public_post = $this->ebay_public_listing_post($post_id);
        if (!$public_post) { return; }
        $this->ebay_render_hivepress_listing_page($public_post, false);
    }

    /**
     * Validate the WordPress object immediately after materialization against
     * the minimum HivePress Listing model contract. A malformed object must
     * never be treated as a successfully routed eBay listing.
     */
    private function ebay_validate_hivepress_listing_state($listing_id, $target_term_id, $author_id) {
        $listing_id = absint($listing_id);
        $target_term_id = absint($target_term_id);
        $author_id = absint($author_id);
        if ($listing_id <= 0) { return new WP_Error('ebay_hivepress_listing_missing', 'HivePress-Listing-ID fehlt nach dem Speichern.'); }
        if (function_exists('get_post_type') && (string) get_post_type($listing_id) !== 'hp_listing') {
            return new WP_Error('ebay_hivepress_post_type_invalid', 'Gespeicherter eBay-Datensatz ist kein HivePress-Listing.');
        }
        if (function_exists('get_post_status') && !in_array((string) get_post_status($listing_id), array('draft','pending','publish','private'), true)) {
            return new WP_Error('ebay_hivepress_status_invalid', 'Gespeichertes eBay-HivePress-Listing hat einen unzulässigen Status.');
        }
        if (function_exists('get_post_field') && absint(get_post_field('post_author', $listing_id)) !== $author_id) {
            return new WP_Error('ebay_hivepress_owner_roundtrip', 'HivePress-Listing-Besitzer wurde nicht korrekt gespeichert.');
        }
        if (function_exists('get_post_field')) {
            if (trim((string) get_post_field('post_title', $listing_id)) === '' || trim((string) get_post_field('post_content', $listing_id)) === '') {
                return new WP_Error('ebay_hivepress_required_content_missing', 'HivePress-Pflichtfelder Titel/Beschreibung fehlen nach dem Speichern.');
            }
        }
        if ($target_term_id <= 0) { return new WP_Error('ebay_hivepress_target_missing', 'HivePress-Zielkategorie fehlt nach dem Speichern.'); }
        if (function_exists('wp_get_post_terms')) {
            $term_ids = wp_get_post_terms($listing_id, 'hp_listing_category', array('fields'=>'ids'));
            if (is_wp_error($term_ids)) { return $term_ids; }
            $term_ids = array_map('absint', (array) $term_ids);
            if (!in_array($target_term_id, $term_ids, true)) {
                return new WP_Error('ebay_hivepress_target_roundtrip', 'HivePress-Zielkategorie wurde nicht korrekt gespeichert.');
            }
        }
        return true;
    }

    private function ebay_materialize_private_listing($stored, $item, $target_term_id, $settings) {
        if (!function_exists('post_type_exists') || !post_type_exists('hp_listing') || !function_exists('taxonomy_exists') || !taxonomy_exists('hp_listing_category')) {
            return new WP_Error('ebay_hivepress_missing', 'HivePress-Listingmodell ist nicht verfügbar.');
        }
        $listing_id = absint($stored['listing_post_id'] ?? 0);
        if ($listing_id > 0) {
            $valid_pointer = function_exists('get_post_type') && (string)get_post_type($listing_id) === 'hp_listing';
            if ($valid_pointer && function_exists('get_post_meta')) {
                $marker = (string)get_post_meta($listing_id, '_ppar_ebay_item_id', true);
                $valid_pointer = ($marker === '' || $marker === (string)$item['item_id']);
            }
            if (!$valid_pointer) { $listing_id = 0; }
        }
        if ($listing_id <= 0 && function_exists('get_posts')) {
            $ids = get_posts(array('post_type'=>'hp_listing','post_status'=>array('draft','pending','publish','private'),'meta_key'=>'_ppar_ebay_item_id','meta_value'=>(string) $item['item_id'],'posts_per_page'=>1,'fields'=>'ids'));
            $listing_id = $ids ? absint($ids[0]) : 0;
        }
        $control_gate = $this->ebay_private_control_gate((string)($item['seller_username'] ?? ''), absint($target_term_id), $listing_id);
        if (is_wp_error($control_gate)) { return $control_gate; }
        $author_id = $this->ebay_listing_author_id($settings);
        if ($author_id <= 0) { return new WP_Error('ebay_hivepress_owner_missing', 'HivePress verlangt einen gültigen Listing-Besitzer; der technische Besitzer fehlt.'); }
        $existing_status = $listing_id > 0 && function_exists('get_post_status') ? (string) get_post_status($listing_id) : '';
        $existing_lifecycle = $listing_id > 0 ? sanitize_key((string) get_post_meta($listing_id, '_ppar_ebay_lifecycle_state', true)) : '';
        $stored_publish_intent = $listing_id > 0 ? sanitize_key((string) get_post_meta($listing_id, '_ppar_ebay_publish_intent', true)) : '';
        $existing_reserve_state = $listing_id > 0 ? sanitize_key((string) get_post_meta($listing_id, '_ppar_ebay_reserve_state', true)) : '';
        // V6.8: publication is an output decision, not a per-child-category quota.
        // The only public card cap requested for PRIVATE is the 9-card parent teaser;
        // child archives use normal HivePress pagination. Old automatic capacity
        // reserves are therefore recoverable, while an explicitly/manual draft is
        // preserved instead of being silently republished.
        $was_published_before_stale = in_array($existing_lifecycle, array('stale','ended'), true) && $stored_publish_intent === 'publish';
        $keep_current_publish = !in_array($existing_lifecycle, array('stale','ended'), true) && $existing_status === 'publish';
        $auto_publish_new = !empty($settings['private_auto_publish']) && $listing_id <= 0;
        $recover_old_capacity_reserve = !empty($settings['private_auto_publish']) && $existing_status === 'draft' && $existing_reserve_state === 'capacity';
        $post_status = ($auto_publish_new || $recover_old_capacity_reserve || $was_published_before_stale || $keep_current_publish) ? 'publish' : 'draft';
        $post_data = array(
            'post_type'=>'hp_listing',
            'post_title'=>sanitize_text_field((string) $item['title']),
            'post_content'=>$this->ebay_listing_content($item),
            'post_excerpt'=>sanitize_text_field(trim((string) $item['price_value'] . ' ' . (string) $item['currency'] . (!empty($item['condition_text']) ? ' · ' . (string) $item['condition_text'] : ''))),
            'post_status'=>$post_status,
            'post_author'=>$author_id,
        );
        if ($listing_id > 0) { $post_data['ID'] = $listing_id; $result = wp_update_post($post_data, true); }
        else { $result = wp_insert_post($post_data, true); }
        if (is_wp_error($result) || absint($result) <= 0) { return is_wp_error($result) ? $result : new WP_Error('ebay_listing_save_failed', 'HivePress-Listing konnte nicht gespeichert werden.'); }
        $listing_id = absint($result);
        $terms = wp_set_post_terms($listing_id, array(absint($target_term_id)), 'hp_listing_category', false);
        if (is_wp_error($terms)) { return $terms; }
        $state_check = $this->ebay_validate_hivepress_listing_state($listing_id, $target_term_id, $author_id);
        if (is_wp_error($state_check)) {
            if (function_exists('get_post_status') && get_post_status($listing_id) === 'publish' && function_exists('wp_update_post')) {
                wp_update_post(array('ID'=>$listing_id,'post_status'=>'draft'));
            }
            return $state_check;
        }
        update_post_meta($listing_id, 'hp_url', (string) $item['affiliate_url']);
        if ((string) get_post_meta($listing_id, 'hp_url', true) !== (string) $item['affiliate_url']) {
            return new WP_Error('ebay_listing_url_roundtrip', 'Affiliate-Link wurde nicht zeichengetreu gespeichert.');
        }
        update_post_meta($listing_id, '_ppar_ebay_item_id', (string) $item['item_id']);
        update_post_meta($listing_id, '_ppar_ebay_seller_type', 'INDIVIDUAL');
        update_post_meta($listing_id, '_ppar_ebay_lifecycle_state', 'active');
        update_post_meta($listing_id, '_ppar_ebay_publish_intent', $post_status === 'publish' ? 'publish' : 'draft');
        // V6.8 removes the hidden per-child publication quota. Capacity is no
        // longer a public visibility state. Existing capacity reserves are cleared
        // once recovered; explicit/manual drafts keep no automatic reserve marker.
        if (function_exists('delete_post_meta')) { delete_post_meta($listing_id, '_ppar_ebay_reserve_state'); }
        update_post_meta($listing_id, '_ppar_ebay_last_seen_at', time());
        if (function_exists('delete_post_meta')) { delete_post_meta($listing_id, '_ppar_ebay_stale_since'); }
        update_post_meta($listing_id, '_ppar_ebay_seller_username', preg_replace('/[^0-9A-Za-z._-]/', '', (string)($item['seller_username'] ?? '')));
        update_post_meta($listing_id, '_ppar_ebay_target_term_id', absint($target_term_id));
        update_post_meta($listing_id, '_ppar_ebay_fresh_until', absint($stored['fresh_until'] ?? 0));
        update_post_meta($listing_id, '_ppar_ebay_source_hash', (string) $item['source_hash']);
        update_post_meta($listing_id, '_ppar_ebay_price_value', (string) $item['price_value']);
        update_post_meta($listing_id, '_ppar_ebay_currency', (string) $item['currency']);
        update_post_meta($listing_id, '_ppar_ebay_item_end_at', absint($item['item_end_at']));
        update_post_meta($listing_id, '_ppar_ebay_affiliate_url', (string) $item['affiliate_url']);
        $classification = is_array($item['portal_classification'] ?? null) ? $item['portal_classification'] : array();
        update_post_meta($listing_id, '_ppar_ebay_product_slug', sanitize_title((string) ($classification['product_slug'] ?? '')));
        update_post_meta($listing_id, '_ppar_ebay_portal_path', sanitize_text_field((string) ($classification['path'] ?? '')));
        update_post_meta($listing_id, '_ppar_ebay_topic_score', absint($classification['score'] ?? 0));
        update_post_meta($listing_id, '_ppar_ebay_evidence_hash', sanitize_text_field((string) ($classification['evidence_hash'] ?? '')));
        $image = $this->ebay_sideload_listing_image($listing_id, $item);
        if (is_wp_error($image)) {
            if (get_post_status($listing_id) === 'publish') { wp_update_post(array('ID'=>$listing_id,'post_status'=>'draft')); }
            return $image;
        }
        global $wpdb;
        $wpdb->update($this->ebay_items_table(), array(
            'listing_post_id'=>$listing_id,'status'=>'active','source_state'=>'available','policy_state'=>'allowed','route_state'=>'ready',
            'output_state'=>$post_status === 'publish' ? 'listing_published' : 'listing_draft',
            'policy_version'=>self::EBAY_CONTENT_POLICY_VERSION,'classifier_version'=>self::EBAY_PRIVATE_CLASSIFIER_VERSION,
            'rejection_reason'=>'','updated_at'=>time()
        ), array('id'=>absint($stored['id'])), $this->ebay_db_formats(array(
            'listing_post_id'=>$listing_id,'status'=>'active','source_state'=>'available','policy_state'=>'allowed','route_state'=>'ready',
            'output_state'=>$post_status === 'publish' ? 'listing_published' : 'listing_draft',
            'policy_version'=>self::EBAY_CONTENT_POLICY_VERSION,'classifier_version'=>self::EBAY_PRIVATE_CLASSIFIER_VERSION,
            'rejection_reason'=>'','updated_at'=>time()
        )), array('%d'));
        return array('listing_id'=>$listing_id,'attachment_id'=>absint($image));
    }

    private function ebay_business_creative($item, $rule, $run_uuid, $classification = array()) {
        $seller = preg_replace('/[^0-9A-Za-z._-]/', '', (string) ($item['seller_username'] ?? ''));
        if ($seller === '') { $seller = 'ebay-business'; }
        $partner_name = !empty($item['seller_username']) ? 'eBay: ' . (string) $item['seller_username'] : 'eBay Business';
        $classification = is_array($classification) ? $classification : array();
        $tags = implode(', ', array_filter(array_merge(
            array('eBay', sanitize_text_field((string) ($classification['product_title'] ?? '')), sanitize_text_field((string) ($classification['hub'] ?? '')), sanitize_text_field((string) ($classification['main_hub'] ?? ''))),
            array_values(array_filter(array_map('sanitize_text_field', (array) ($item['category_names'] ?? array())))),
            array(sanitize_text_field((string) ($item['condition_text'] ?? '')))
        )));
        $description_parts = array_filter(array(
            (string) ($item['short_description'] ?? ''),
            trim((string) ($item['price_value'] ?? '') . ' ' . (string) ($item['currency'] ?? '')),
            !empty($item['condition_text']) ? 'Zustand: ' . (string) $item['condition_text'] : '',
        ));
        $payload = array(
            '_declared_width'=>0,'_declared_height'=>0,'_dimension_state'=>'pending','_dimension_error'=>'','_image_sha256'=>'','_image_mime'=>'','_image_bytes'=>0,'_measured_at'=>0,
            '_preverify_topic_status'=>'portal_pending','_preverify_topic_score'=>0,'_preverify_topic_targets'=>array(),
            'ebay_seller_account_type'=>'BUSINESS','ebay_seller_username'=>(string) $item['seller_username'],'ebay_item_id'=>(string) $item['item_id'],
            'ebay_item_end_at'=>absint($item['item_end_at']),'ebay_buying_options'=>(array) $item['buying_options'],'ebay_rule_id'=>sanitize_key((string) ($rule['id'] ?? '')),
            'ebay_verified_product_slug'=>sanitize_title((string) ($classification['product_slug'] ?? '')),'ebay_verified_product_concept'=>sanitize_key((string) ($classification['product_concept_id'] ?? '')),'ebay_verified_concept_kind'=>sanitize_key((string) ($classification['concept_kind'] ?? 'product')),'ebay_verified_product_targets'=>array_values((array) ($classification['product_target_slugs'] ?? array())),'ebay_verified_path'=>sanitize_text_field((string) ($classification['path'] ?? '')),'ebay_verified_score'=>absint($classification['score'] ?? 0),'ebay_evidence_hash'=>sanitize_text_field((string) ($classification['evidence_hash'] ?? '')),'ebay_business_match_contract'=>sanitize_key((string) ($classification['business_match_contract'] ?? '')),
            'ebay_quality_score'=>absint($item['business_quality']['overall'] ?? 0),'ebay_quality_relevance'=>absint($item['business_quality']['relevance'] ?? 0),'ebay_quality_seller'=>absint($item['business_quality']['seller'] ?? 0),'ebay_quality_offer'=>absint($item['business_quality']['offer'] ?? 0),'ebay_quality_price'=>absint($item['business_quality']['price'] ?? 0),'ebay_quality_reason'=>sanitize_text_field((string) ($item['business_quality']['reason'] ?? '')),
            'ebay_seller_feedback_percentage'=>(float) ($item['seller_feedback_percentage'] ?? 0),'ebay_seller_feedback_score'=>absint($item['seller_feedback_score'] ?? 0),'ebay_brand'=>sanitize_text_field((string) ($item['brand'] ?? '')),
            'price'=>sanitize_text_field((string) ($item['price_value'] ?? '')),'currency'=>strtoupper(substr(sanitize_text_field((string) ($item['currency'] ?? 'EUR')),0,10)),'availability'=>'available',
        );
        $external_id = substr(preg_replace('/[^0-9A-Za-z._-]/', '-', (string) $item['item_id']), 0, 191);
        $destination_url = !empty($item['item_web_url']) ? (string) $item['item_web_url'] : (string) $item['affiliate_url'];
        $identity = hash('sha256', 'ebay|' . $seller . '|' . $external_id);
        $source = array(
            'provider'=>'ebay','partner_external_id'=>$seller,'external_id'=>$external_id,'title'=>(string) $item['title'],'description'=>implode(' · ', $description_parts),
            'tags'=>$tags,'image_url'=>(string) $item['image_url'],'destination_url'=>$destination_url,'tracking_url'=>(string) $item['affiliate_url'],
            'source_status'=>'active','source_kind'=>'ebay_business_item','item_end_at'=>absint($item['item_end_at']),
            'price'=>sanitize_text_field((string) ($item['price_value'] ?? '')),'currency'=>strtoupper(substr(sanitize_text_field((string) ($item['currency'] ?? 'EUR')),0,10)),'availability'=>'available',
        );
        return array(
            'provider'=>'ebay','partner_external_id'=>$seller,'partner_name'=>$partner_name,'external_id'=>$external_id,'identity_hash'=>$identity,
            'creative_type'=>'product','title'=>(string) $item['title'],'description'=>implode(' · ', $description_parts),'tags'=>$tags,
            'image_url'=>(string) $item['image_url'],'destination_url'=>$destination_url,'tracking_url'=>(string) $item['affiliate_url'],
            'width'=>0,'height'=>0,'source_status'=>'active','source_kind'=>'ebay_business_item','availability_state'=>'active','missing_count'=>0,
            'last_complete_run'=>substr((string) $run_uuid, 0, 36),'review_status'=>'review','selected'=>0,'content_scope'=>'unclassified','scope_source'=>'','classified_at'=>0,
            'topic_status'=>'format_pending','topic_score'=>0,'topic_targets'=>'[]','source_hash'=>hash('sha256', wp_json_encode($source, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES)),
            'payload'=>wp_json_encode($payload, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES),
        );
    }

    /**
     * V5.18 – harter Vertrag fuer automatisch ausspielbare eBay-BUSINESS-Produkte.
     * Nur ein bereits durch ebay_classify_portal_item() eindeutig verifiziertes
     * Produktziel darf den manuellen Review-Pfad verlassen. Private Zielbuckets,
     * unklare Scores oder fremde Provider fallen fail-closed heraus.
     */
    private function ebay_business_product_contract($row) {
        if (!is_array($row)
            || sanitize_key((string) ($row['provider'] ?? '')) !== 'ebay'
            || sanitize_key((string) ($row['source_kind'] ?? '')) !== 'ebay_business_item'
            || sanitize_key((string) ($row['creative_type'] ?? '')) !== 'product'
            || sanitize_key((string) ($row['source_status'] ?? 'active')) !== 'active'
            || sanitize_key((string) ($row['availability_state'] ?? 'active')) !== 'active') { return array(); }
        $payload=json_decode((string)($row['payload']??''),true); $payload=is_array($payload)?$payload:array();
        if (strtoupper(sanitize_key((string)($payload['ebay_seller_account_type']??''))) !== 'BUSINESS') { return array(); }
        $score=absint($payload['ebay_verified_score']??0);
        $evidence_hash=strtolower(sanitize_text_field((string)($payload['ebay_evidence_hash']??'')));
        $match_contract=sanitize_key((string)($payload['ebay_business_match_contract']??''));
        $concept_id=sanitize_key((string)($payload['ebay_verified_product_concept']??''));
        $target_slugs=array_values(array_unique(array_filter(array_map('sanitize_title',(array)($payload['ebay_verified_product_targets']??array())))));
        if ($score<80 || $match_contract!=='concept_v3' || $concept_id==='' || !preg_match('/^[a-f0-9]{64}$/',$evidence_hash) || !$target_slugs) { return array(); }
        $catalog=$this->ebay_portal_catalog(); if(is_wp_error($catalog)){return array();}
        $collections=array(
            'product'=>(array)($catalog['business_concepts']??array()),
            'hub'=>(array)($catalog['business_hub_concepts']??array()),
        );
        foreach($collections as $concept_kind=>$concepts){
            foreach($concepts as $concept){
                if(!is_array($concept)||sanitize_key((string)($concept['id']??''))!==$concept_id){continue;}
                $pages=array_values(array_filter((array)($concept['target_pages']??array()),'is_array'));
                $allowed=array_values(array_unique(array_filter(array_map(static function($p){return sanitize_title((string)($p['slug']??''));},$pages))));
                $target_slugs=array_values(array_intersect($target_slugs,$allowed));
                if(!$target_slugs){return array();}
                $primary=null;
                foreach($pages as $page){ if(sanitize_title((string)($page['slug']??''))===$target_slugs[0]){$primary=$page;break;} }
                if(!is_array($primary)){$primary=$pages[0]??array();}
                return array(
                    'product_concept_id'=>$concept_id,
                    'concept_kind'=>$concept_kind,
                    'product_slug'=>sanitize_title((string)($primary['slug']??'')),
                    'product_target_slugs'=>$target_slugs,
                    'product_title'=>sanitize_text_field((string)($concept['title']??'')),
                    'hub_slug'=>sanitize_title((string)($primary['hub_slug']??'')),
                    'hub'=>sanitize_text_field((string)($primary['hub']??'')),
                    'main_slug'=>sanitize_title((string)($primary['main_slug']??'')),
                    'main_hub'=>sanitize_text_field((string)($primary['main_hub']??'')),
                    'target_pages'=>$pages,'score'=>$score,'evidence_hash'=>$evidence_hash,
                );
            }
        }
        return array();
    }

    /**
     * Verwendet fuer eBay-BUSINESS ausschliesslich den verifizierten Produkt-Slug
     * als Primaerziel. Die generische Textklassifikation darf diesen harten
     * Katalogtreffer nicht auf eine benachbarte Seite umbiegen.
     */
    private function ebay_business_exact_product_classification($row, $portal, $targets) {
        $contract=$this->ebay_business_product_contract($row); if(!$contract){return array();}
        $wanted=array_flip((array)($contract['product_target_slugs']??array()));
        $matches=array();
        foreach((array)$targets as $target){
            if(!is_array($target)||sanitize_key((string)($target['type']??''))!=='page'){continue;}
            $slug=sanitize_title((string)($target['slug']??''));
            if($slug!==''&&isset($wanted[$slug])){$matches[$slug]=$target;}
        }
        if(!$matches){
            return array('status'=>'review','confidence'=>absint($contract['score']??0),'reason'=>'Kein verifiziertes Produktziel ist als veröffentlichte Portalseite vorhanden.','target'=>null,'alternatives'=>array(),'source'=>'ebay_verified_product_target_missing');
        }
        $primary=null;
        foreach((array)$contract['product_target_slugs'] as $slug){ if(isset($matches[$slug])){$primary=$matches[$slug];break;} }
        if(!is_array($primary)){$primary=reset($matches);}
        if(method_exists($this,'control_target_gate')){ $gate=$this->control_target_gate((string)($portal['key']??''),(string)($primary['key']??'')); if(is_wp_error($gate)){return $gate;} }
        return array('status'=>'ready','confidence'=>absint($contract['score']??0),'reason'=>'Verifiziertes eBay-BUSINESS-Produktkonzept stimmt mit mindestens einer echten Portalseite überein.','target'=>$primary,'alternatives'=>array_values($matches),'source'=>'ebay_verified_product_concept');
    }

    /**
     * Ein verifiziertes Produkt darf auf seiner Produktseite, dem zugehoerigen
     * Hub-2, dem Haupt-Hub und den redaktionellen Unterkategorien erscheinen.
     * Journal wird bewusst nicht global befuellt; ohne konkrete Themenkante
     * bleibt ein BUSINESS-Produkt dort fail-closed.
     */
    private function ebay_business_campaign_target_keys($row, $target = array()) {
        $contract=$this->ebay_business_product_contract($row); if(!$contract){return array();}
        $keys=array(); $product_slugs=(array)($contract['product_target_slugs']??array());
        // Hub-Konzepte sind bereits ein eigenstaendiges, exaktes Ziel. Sie duerfen
        // nicht pauschal auf Haupt-Hub oder Nachbarseiten aufgeweitet werden.
        if (sanitize_key((string)($contract['concept_kind']??'product')) === 'hub') {
            $slug=sanitize_title((string)($contract['product_slug']??''));
            return $slug!=='' ? array('page:'.$slug) : array();
        }
        $catalog=$this->ebay_portal_catalog();
        if(!is_wp_error($catalog)){
            foreach((array)($catalog['product_targets']??array()) as $page){
                if(!is_array($page)||!in_array(sanitize_title((string)($page['slug']??'')),$product_slugs,true)){continue;}
                foreach(array('slug','hub_slug','main_slug') as $field){$slug=sanitize_title((string)($page[$field]??'')); if($slug!==''){$keys[]='page:'.$slug;}}
            }
            foreach((array)($catalog['article_targets']??array()) as $article){
                if(!is_array($article)||!in_array(sanitize_title((string)($article['product_slug']??'')),$product_slugs,true)){continue;}
                $slug=sanitize_title((string)($article['category_slug']??'')); if($slug!==''){$keys[]='category:'.$slug;}
            }
        }
        return array_values(array_unique(array_filter($keys)));
    }

    private function ebay_business_campaign_placements($row) {
        return $this->ebay_business_product_contract($row) ? array(
            'hub_product_1','hub_product_2','hub_product_3',
            'category_product_1','category_product_2','category_product_3',
            'journal_product_1','journal_product_2','journal_product_3',
            // The article renderer requests this exact product placement. Target
            // keys still decide whether the product belongs to the article, so
            // enabling the slot does not broaden topical delivery.
            'post_bottom_products',
        ) : array();
    }

    /**
     * V5.18 – Preis-/Textupdates eines bereits verifizierten BUSINESS-Produkts
     * dürfen nicht unnötig den Bildstatus auf pending zurücksetzen. Solange die
     * Bild-URL bytegleich bleibt, werden ausschließlich die bereits belegten
     * Asset-Evidenzen übernommen; ändert sich das Bild, läuft die normale harte
     * Bildprüfung erneut.
     */
    private function ebay_business_reuse_verified_asset($creative) {
        if (!is_array($creative)
            || empty($creative['identity_hash'])
            || empty($creative['image_url'])
            || !method_exists($this, 'creative_library_table')) {
            return $creative;
        }
        global $wpdb;
        $existing = $wpdb->get_row($wpdb->prepare(
            "SELECT width, height, image_url, payload, topic_status, topic_score, topic_targets FROM {$this->creative_library_table()} WHERE identity_hash=%s",
            (string) $creative['identity_hash']
        ), ARRAY_A);
        if (!is_array($existing)
            || (string) ($existing['image_url'] ?? '') !== (string) ($creative['image_url'] ?? '')
            || absint($existing['width'] ?? 0) <= 0
            || absint($existing['height'] ?? 0) <= 0) {
            return $creative;
        }
        $old_payload = json_decode((string) ($existing['payload'] ?? ''), true);
        $new_payload = json_decode((string) ($creative['payload'] ?? ''), true);
        $old_payload = is_array($old_payload) ? $old_payload : array();
        $new_payload = is_array($new_payload) ? $new_payload : array();
        if (!in_array((string) ($old_payload['_dimension_state'] ?? ''), array('verified','mismatch'), true)
            || empty($old_payload['_image_sha256'])) {
            return $creative;
        }
        foreach (array('_dimension_state','_dimension_error','_image_sha256','_image_mime','_image_bytes','_measured_at') as $key) {
            if (array_key_exists($key, $old_payload)) { $new_payload[$key] = $old_payload[$key]; }
        }
        $creative['width'] = absint($existing['width']);
        $creative['height'] = absint($existing['height']);
        $creative['topic_status'] = sanitize_key((string) ($existing['topic_status'] ?? 'auto_verified'));
        $creative['topic_score'] = absint($existing['topic_score'] ?? 0);
        $creative['topic_targets'] = (string) ($existing['topic_targets'] ?? '[]');
        $creative['payload'] = wp_json_encode($new_payload, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
        return $creative;
    }

    private function ebay_business_pending_asset_count() {
        if (!method_exists($this, 'creative_library_table')) { return 0; }
        global $wpdb;
        $table = $this->creative_library_table();
        return absint($wpdb->get_var("SELECT COUNT(*) FROM {$table} WHERE provider='ebay' AND source_kind='ebay_business_item' AND creative_type='product' AND image_url<>'' AND source_status='active' AND availability_state='active' AND (payload LIKE '%\"_dimension_state\":\"pending\"%' OR ((width=0 OR height=0) AND payload NOT LIKE '%\"_dimension_state\":\"failed\"%' AND payload NOT LIKE '%\"_dimension_state\":\"verified\"%' AND payload NOT LIKE '%\"_dimension_state\":\"mismatch\"%'))"));
    }

    /**
     * Deterministische, begrenzte BUSINESS-Bildpruefung. Sie wird vom
     * Bestandsabgleich als eigene Phase ausgefuehrt; die Diagnose bleibt read-only.
     * Der normale Creative-Cron bleibt paralleler Fallback.
     */
    private function ebay_business_verify_asset_batch($limit = 1) {
        if (!method_exists($this, 'creative_library_table') || !method_exists($this, 'creative_library_verify_asset_row')) {
            return array('processed'=>0,'remaining'=>0,'verified'=>0,'blocked'=>0);
        }
        $limit = max(1, min(2, absint($limit)));
        global $wpdb;
        $table = $this->creative_library_table();
        $rows = (array) $wpdb->get_results("SELECT * FROM {$table} WHERE provider='ebay' AND source_kind='ebay_business_item' AND creative_type='product' AND image_url<>'' AND source_status='active' AND availability_state='active' AND (payload LIKE '%\"_dimension_state\":\"pending\"%' OR ((width=0 OR height=0) AND payload NOT LIKE '%\"_dimension_state\":\"failed\"%' AND payload NOT LIKE '%\"_dimension_state\":\"verified\"%' AND payload NOT LIKE '%\"_dimension_state\":\"mismatch\"%')) ORDER BY id ASC LIMIT " . absint($limit), ARRAY_A);
        $verified = 0; $blocked = 0;
        foreach ($rows as $row) {
            $result = $this->creative_library_verify_asset_row($row, false, true);
            if (is_wp_error($result)) { $blocked++; } else { $verified++; }
        }
        return array(
            'processed'=>count($rows),
            'remaining'=>$this->ebay_business_pending_asset_count(),
            'verified'=>$verified,
            'blocked'=>$blocked,
        );
    }

    public function handle_ebay_business_asset_pump() {
        wp_send_json_error(array('message'=>'Workflow V2: Diagnose ist read-only; Bildprüfung läuft ausschließlich über die reguläre Hintergrundverarbeitung.'), 410);
    }


    private function ebay_business_deactivate_existing_output($row, $reason) {
        $row = is_array($row) ? $row : array();
        $reason = sanitize_text_field((string) $reason);
        if ($reason === '') { $reason = 'BUSINESS-Produktmatch ist nicht eindeutig; Ausgabe bleibt auf Review.'; }
        global $wpdb;
        $hash = strtolower(sanitize_text_field((string) ($row['creative_identity_hash'] ?? '')));
        $creative_table = method_exists($this, 'creative_library_table') ? $this->creative_library_table() : '';
        if (!preg_match('/^[a-f0-9]{64}$/', $hash) && $creative_table !== '') {
            $found = $wpdb->get_var($wpdb->prepare("SELECT identity_hash FROM {$creative_table} WHERE provider='ebay' AND source_kind='ebay_business_item' AND external_id=%s ORDER BY id DESC LIMIT 1", (string) ($row['item_id'] ?? '')));
            $candidate = strtolower(sanitize_text_field((string) $found));
            if (preg_match('/^[a-f0-9]{64}$/', $candidate)) { $hash = $candidate; }
        }
        if (!preg_match('/^[a-f0-9]{64}$/', $hash)) { return false; }
        if ($creative_table !== '') {
            $creative = $wpdb->get_row($wpdb->prepare("SELECT * FROM {$creative_table} WHERE identity_hash=%s", $hash), ARRAY_A);
            if (is_array($creative)) {
                $payload = json_decode((string) ($creative['payload'] ?? ''), true);
                $payload = is_array($payload) ? $payload : array();
                foreach (array('ebay_verified_product_slug','ebay_verified_path','ebay_evidence_hash','ebay_business_match_contract','ebay_verified_product_concept') as $key) { $payload[$key] = ''; }
                $payload['ebay_verified_product_targets'] = array();
                $payload['ebay_verified_score'] = 0;
                $payload['_business_match_state'] = 'review';
                $payload['_business_match_reason'] = $reason;
                $payload['_business_match_at'] = time();
                $wpdb->update($creative_table, array(
                    'review_status'=>'review','selected'=>0,'content_scope'=>'unclassified','scope_source'=>'ebay_business_strict_match',
                    'topic_status'=>'review','topic_score'=>0,'topic_targets'=>'[]',
                    'payload'=>wp_json_encode($payload, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES),
                ), array('id'=>absint($creative['id'] ?? 0)));
            }
        }
        if (method_exists($this, 'output_objects_table')) {
            $output_table = $this->output_objects_table();
            $objects = $wpdb->get_results($wpdb->prepare("SELECT * FROM {$output_table} WHERE creative_identity_hash=%s AND output_type='product_campaign'", $hash), ARRAY_A);
            foreach ((array) $objects as $object) {
                if (method_exists($this, 'output_deactivate_materialized_object')) { $this->output_deactivate_materialized_object($object, $reason); }
            }
            $wpdb->update($output_table, array(
                'target_type'=>'','target_key'=>'','target_label'=>'','slot_id'=>'',
                'status'=>'review','decision_source'=>'ebay_business_strict_match','decision_reason'=>$reason,'last_verified'=>time(),'updated_at'=>time(),
            ), array('creative_identity_hash'=>$hash,'output_type'=>'product_campaign'));
        }
        return true;
    }

    /** BUSINESS-Review ersetzt eine eventuell alte Auto-Ausgabe sofort fail-closed. */
    private function ebay_business_hold_for_review($row, $item, $rule, $error, $settings = null) {
        $settings = is_array($settings) ? $settings : $this->ebay_settings();
        $item = is_array($item) ? $item : array();
        $rule = is_array($rule) ? $rule : array();
        $preserved_last_good = $this->ebay_business_preserve_last_good_on_soft_review($row, $error);
        $stored = $this->ebay_store_review_candidate($item, $rule, 'BUSINESS', $error, $settings);
        if (is_wp_error($stored)) { return $stored; }
        if (!method_exists($this, 'creative_library_upsert')) { return $stored; }
        // Leere Klassifikation ist absichtlich: Der generische Ausgabeplan darf
        // hoechstens einen inaktiven Review-Entwurf erzeugen und superseded damit
        // eine eventuell alte, falsch aktive BUSINESS-Kampagne.
        $creative = $this->ebay_business_creative($item, $rule, 'business-review-' . time(), array());
        $creative = $this->ebay_business_reuse_verified_asset($creative);
        $state = $this->creative_library_upsert($creative);
        if ($state !== 'failed' && $state !== 'blocked') {
            global $wpdb;
            $wpdb->update($this->ebay_items_table(), array('creative_identity_hash'=>(string) $creative['identity_hash'],'updated_at'=>time()), array('id'=>absint($stored['id'] ?? 0)), array('%s','%d'), array('%d'));
            // If a Last-Known-Good campaign exists, a review candidate is stored
            // diagnostically but must not supersede/deactivate that public output.
            if (!$preserved_last_good && method_exists($this, 'output_plan_creative') && method_exists($this, 'creative_library_table')) {
                $persisted = $wpdb->get_row($wpdb->prepare("SELECT * FROM {$this->creative_library_table()} WHERE identity_hash=%s", (string) $creative['identity_hash']), ARRAY_A);
                if (is_array($persisted)) { $this->output_plan_creative($persisted, true); }
            }
        }
        return $stored;
    }

    private function ebay_business_restore_local_reclass_freshness($row) {
        $row = is_array($row) ? $row : array();
        $id = absint($row['id'] ?? 0);
        if ($id <= 0) { return; }
        global $wpdb;
        $wpdb->update($this->ebay_items_table(), array(
            'last_seen'=>absint($row['last_seen'] ?? 0),
            'fresh_until'=>absint($row['fresh_until'] ?? 0),
        ), array('id'=>$id), array('%d','%d'), array('%d'));
    }

    /**
     * Einmalige lokale V5.28-Neubewertung des vorhandenen BUSINESS-Bestands.
     * Kein eBay-Request: verwendet ausschliesslich die bereits gespeicherten
     * Originalpayloads. Dadurch werden alte Fehlzuordnungen entfernt und klare
     * Treffer auf demselben Creative/Kampagnenpfad neu geplant.
     */
    public function maybe_run_ebay_business_match_upgrade($limit = 25) {
        // Deprecated read-only adapter. Opening a diagnostic/admin page must not
        // change classification, campaigns, assets or output state.
        $state = $this->ebay_maintenance_state_load();
        $state = is_array($state) ? $state : array();
        $stats = is_array($state['last_stats'] ?? null) ? $state['last_stats'] : array();
        return array(
            'completed_at'=>absint($state['completed_at'] ?? 0),
            'scanned'=>absint($stats['scanned'] ?? 0),
            'ready'=>absint($stats['ready_business'] ?? 0),
            'review'=>absint($stats['review'] ?? 0),
            'blocked'=>absint($stats['blocked'] ?? 0),
        );
    }

    public function handle_ebay_business_match_pump() {
        wp_send_json_error(array('message'=>'Workflow V2: Diagnose ist read-only; BUSINESS-Klassifikation läuft ausschließlich im geplanten Maintenance-Job.'), 410);
    }


    /** Explicit editorial veto/pin actions; ordinary page views stay read-only. */
    public function handle_ebay_business_curation() {
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.'); }
        check_admin_referer('ppar_ebay_business_curation');
        $operation = sanitize_key((string) ($_POST['operation'] ?? ''));
        $item_id = sanitize_text_field((string) ($_POST['item_id'] ?? ''));
        $seller = sanitize_text_field((string) ($_POST['seller'] ?? ''));
        $brand = sanitize_text_field((string) ($_POST['brand'] ?? ''));
        $concept = sanitize_key((string) ($_POST['concept'] ?? ''));
        $title = sanitize_text_field((string) ($_POST['title'] ?? ''));
        $reason = sanitize_text_field((string) ($_POST['reason'] ?? ''));
        $state = $this->ebay_business_curation_state();
        $now = time();
        if ($operation === 'pin' && $item_id !== '') {
            $state['items'][$item_id] = array('status'=>'pinned','reason'=>$reason !== '' ? $reason : 'Redaktionell angepinnt.','updated_at'=>$now);
        } elseif ($operation === 'block_item' && $item_id !== '') {
            if ($reason === '') { $reason = 'Redaktionell als unpassendes Produkt gesperrt.'; }
            $state['items'][$item_id] = array('status'=>'blocked','reason'=>$reason,'updated_at'=>$now);
        } elseif ($operation === 'block_item_learn' && $item_id !== '' && $concept !== '') {
            if ($reason === '') { $reason = 'Redaktionell als wiederkehrende Fehlproduktklasse gesperrt.'; }
            $state['items'][$item_id] = array('status'=>'blocked','reason'=>$reason,'updated_at'=>$now);
            $head = $this->ebay_business_title_head_token($title);
            if ($head !== '') {
                if (!isset($state['learned_heads'][$concept]) || !is_array($state['learned_heads'][$concept])) { $state['learned_heads'][$concept] = array(); }
                $state['learned_heads'][$concept][$head] = array('reason'=>$reason,'updated_at'=>$now);
            }
        } elseif ($operation === 'item_clear' && $item_id !== '') {
            unset($state['items'][$item_id]);
        } elseif ($operation === 'block_seller' && $seller !== '') {
            $key=$this->ebay_business_curation_key($seller); if($key!==''){$state['sellers'][$key]=array('status'=>'blocked','reason'=>$reason !== '' ? $reason : 'Verkäufer redaktionell gesperrt.','updated_at'=>$now);}
        } elseif ($operation === 'seller_clear' && $seller !== '') {
            unset($state['sellers'][$this->ebay_business_curation_key($seller)]);
        } elseif (in_array($operation,array('prefer_brand','block_brand'),true) && $brand !== '') {
            $key=$this->ebay_business_curation_key($brand); if($key!==''){$state['brands'][$key]=array('status'=>$operation==='prefer_brand'?'preferred':'blocked','reason'=>$reason !== '' ? $reason : ($operation==='prefer_brand'?'Marke redaktionell bevorzugt.':'Marke redaktionell gesperrt.'),'updated_at'=>$now);}
        } elseif ($operation === 'brand_clear' && $brand !== '') {
            unset($state['brands'][$this->ebay_business_curation_key($brand)]);
        } elseif ($operation === 'learned_clear' && $concept !== '') {
            $head=$this->ebay_business_title_head_token($title); if($head!=='' && isset($state['learned_heads'][$concept][$head])){unset($state['learned_heads'][$concept][$head]);}
        } else {
            wp_die('Ungültige Kurationsaktion.');
        }
        $this->ebay_business_curation_save($state);
        // Curation never creates a second BUSINESS selector. Re-evaluation is
        // queued through the one canonical durable refresh/selection run.
        if(method_exists($this,'ebay_run_start')){$this->ebay_run_start(true,'refresh');}
        $query=array('page'=>'affiliate-portal-ebay-business','curated'=>'1');
        if($concept!==''){$query['concept']=$concept;}
        wp_safe_redirect(add_query_arg($query, admin_url('admin.php')));
        exit;
    }

    private function ebay_route_business($stored, $item, $rule, $run_uuid, $classification = array()) {
        if (!method_exists($this, 'creative_library_upsert')) { return new WP_Error('ebay_creative_library_missing', 'Werbemittelbibliothek fehlt.'); }
        $classification = is_array($classification) ? $classification : array();
        if (sanitize_key((string) ($classification['business_match_contract'] ?? '')) !== 'concept_v3') {
            $classification = $this->ebay_business_classify_portal_item_strict($item, $rule);
            if (is_wp_error($classification)) { return $classification; }
            $item['portal_classification'] = $classification;
        }
        $creative = $this->ebay_business_creative($item, $rule, $run_uuid, $classification);
        $creative = $this->ebay_business_reuse_verified_asset($creative);
        $state = $this->creative_library_upsert($creative);
        if ($state === 'failed' || $state === 'blocked') { return new WP_Error('ebay_business_import_failed', 'eBay-Business-Creative wurde blockiert.'); }
        global $wpdb;
        $plan = array('created'=>0,'active'=>0,'blocked'=>0,'review'=>0,'errors'=>array());
        if (method_exists($this, 'output_plan_creative') && method_exists($this, 'creative_library_table')) {
            $persisted = $wpdb->get_row($wpdb->prepare("SELECT * FROM {$this->creative_library_table()} WHERE identity_hash=%s", (string) $creative['identity_hash']), ARRAY_A);
            if (is_array($persisted)) { $plan = $this->output_plan_creative($persisted, true); }
        }
        $plan = is_array($plan) ? $plan : array();
        if (absint($plan['active'] ?? 0) < 1) {
            $error = new WP_Error('ebay_business_materialization_not_active','BUSINESS-Ersatzroute wurde nicht aktiv materialisiert; Last-Known-Good bleibt unverändert.');
            if ($this->ebay_business_preserve_last_good_on_soft_review($stored, $error)) {
                // Structured success-with-review: callers must not run their
                // generic route-error handlers afterwards, otherwise the freshly
                // persisted review_last_good state would be overwritten again.
                return array(
                    'creative_identity_hash'=>(string) $creative['identity_hash'],
                    'state'=>'last_good_preserved','last_good_preserved'=>1,
                    'review_code'=>$error->get_error_code(),'review_reason'=>$error->get_error_message(),'plan'=>$plan,
                );
            }
            $repair = array('route_state'=>'review','output_state'=>'repair_pending','rejection_reason'=>$error->get_error_message(),'updated_at'=>time());
            $wpdb->update($this->ebay_items_table(), $repair, array('id'=>absint($stored['id'])), $this->ebay_db_formats($repair), array('%d'));
            return $error;
        }
        $route_update = array(
            'creative_identity_hash'=>(string) $creative['identity_hash'],'status'=>'active','source_state'=>'available','policy_state'=>'allowed','route_state'=>'ready',
            'output_state'=>'creative_ready','policy_version'=>self::EBAY_CONTENT_POLICY_VERSION,'classifier_version'=>self::EBAY_BUSINESS_CLASSIFIER_VERSION,
            'rejection_reason'=>'','updated_at'=>time()
        );
        $wpdb->update($this->ebay_items_table(), $route_update, array('id'=>absint($stored['id'])), $this->ebay_db_formats($route_update), array('%d'));
        if (method_exists($this, 'creative_library_schedule_asset_verification')) { $this->creative_library_schedule_asset_verification(10); }
        return array('creative_identity_hash'=>$creative['identity_hash'],'state'=>$state,'plan'=>$plan);
    }

    private function ebay_mark_route_error($stored, $error) {
        if (!is_array($stored) || empty($stored['id'])) { return; }
        global $wpdb;
        $message = is_wp_error($error) ? $error->get_error_message() : sanitize_text_field((string) $error);
        $route_update = array('status'=>'review','route_state'=>'review','output_state'=>'none','rejection_reason'=>$message,'updated_at'=>time());
        $wpdb->update($this->ebay_items_table(), $route_update, array('id'=>absint($stored['id'])), $this->ebay_db_formats($route_update), array('%d'));
    }

    /** Fach-/Zielunsicherheit ist gemäß Chef-Veto-Vertrag übersteuerbar. */
    private function ebay_is_soft_classification_error($error) {
        if (!is_wp_error($error)) { return false; }
        return in_array((string) $error->get_error_code(), array(
            'ebay_topic_evidence_missing',
            'ebay_portal_topic_missing',
            'ebay_portal_topic_negative',
            'ebay_portal_target_missing',
            'ebay_portal_target_ambiguous',
            'ebay_business_title_missing',
            'ebay_business_target_missing',
            'ebay_business_target_ambiguous',
            'ebay_business_concept_missing',
            'ebay_business_concept_ambiguous',
            'ebay_business_concept_target_missing',
            'ebay_private_bucket_missing',
            'ebay_private_bucket_low_confidence',
            'ebay_private_bucket_ambiguous',
        ), true);
    }

    private function ebay_error_code($error, $fallback = 'unknown') {
        $code = is_wp_error($error) ? sanitize_key((string) $error->get_error_code()) : sanitize_key((string) $error);
        return $code !== '' ? $code : sanitize_key((string) $fallback);
    }

    private function ebay_summary_reason_add(&$summary, $kind, $error, $rule_id, $seller_type, $profile_key = '') {
        $kind = sanitize_key((string) $kind);
        $code = $this->ebay_error_code($error, $kind . '_unknown');
        $bucket = $kind . '_reasons';
        if (!isset($summary[$bucket]) || !is_array($summary[$bucket])) { $summary[$bucket] = array(); }
        $summary[$bucket][$code] = absint($summary[$bucket][$code] ?? 0) + 1;
        $profile_key = (string) $profile_key;
        if ($profile_key === '') { $profile_key = sanitize_key((string) $rule_id) . '|' . strtoupper(sanitize_key((string) $seller_type)); }
        if (isset($summary['profile_stats'][$profile_key])) {
            if (!isset($summary['profile_stats'][$profile_key][$bucket]) || !is_array($summary['profile_stats'][$profile_key][$bucket])) {
                $summary['profile_stats'][$profile_key][$bucket] = array();
            }
            $summary['profile_stats'][$profile_key][$bucket][$code] = absint($summary['profile_stats'][$profile_key][$bucket][$code] ?? 0) + 1;
        }
        return $code;
    }

    private function ebay_candidate_scope_key($item_id) {
        return 'ebay-candidate:' . substr(sanitize_text_field((string) $item_id), 0, 191);
    }

    private function ebay_candidate_manual_decision($item_id) {
        if (!method_exists($this, 'control_get_decision') || !method_exists($this, 'output_local_portal_key')) {
            return array('exists'=>false,'status'=>'automatic','reason'=>'','payload'=>array());
        }
        $portal_key = sanitize_key((string) $this->output_local_portal_key());
        if ($portal_key === '') { return array('exists'=>false,'status'=>'automatic','reason'=>'','payload'=>array()); }
        return $this->control_get_decision($portal_key, 'output', $this->ebay_candidate_scope_key($item_id));
    }

    private function ebay_private_bucket_definitions() {
        return array(
            'pferde-ponys'=>'Pferde & Ponys',
            'sattel-zaumzeug'=>'Sattel & Zaumzeug',
            'decken-schutz'=>'Decken & Schutz',
            'stall-weide-haltung'=>'Stall, Weide & Haltung',
            'fuetterung-pflege'=>'Fütterung & Pflege',
            'anhaenger-transport'=>'Anhänger & Transport',
            'reitbekleidung-zubehoer'=>'Reitbekleidung & Zubehör',
            'sonstiges'=>'Sonstiges',
        );
    }

    /**
     * Recover a missing private target from durable evidence. This is used by the
     * stündlichen getItem refresh so older rows with target_term_id=0 are repaired
     * instead of failing their HivePress round-trip.
     */
    private function ebay_recover_private_target_term_id($row, $settings) {
        $row = is_array($row) ? $row : array();
        $settings = is_array($settings) ? $settings : $this->ebay_settings();
        $candidates = array();
        $row_target = absint($row['target_term_id'] ?? 0);
        if ($row_target > 0) { $candidates[] = $row_target; }

        $listing_id = absint($row['listing_post_id'] ?? 0);
        if ($listing_id > 0 && function_exists('get_post_meta')) {
            $meta_target = absint(get_post_meta($listing_id, '_ppar_ebay_target_term_id', true));
            if ($meta_target > 0) { $candidates[] = $meta_target; }
        }
        if ($listing_id > 0 && function_exists('wp_get_post_terms')) {
            $term_ids = wp_get_post_terms($listing_id, 'hp_listing_category', array('fields'=>'ids'));
            if (!is_wp_error($term_ids)) {
                foreach ((array) $term_ids as $term_id) { $candidates[] = absint($term_id); }
            }
        }

        $payload = json_decode((string) ($row['source_payload'] ?? ''), true);
        $classification = is_array($payload) && is_array($payload['portal_classification'] ?? null) ? $payload['portal_classification'] : array();
        $bucket_slug = sanitize_title((string) ($classification['private_bucket_slug'] ?? ''));
        if ($bucket_slug !== '' && function_exists('get_term_by')) {
            $term = get_term_by('slug', $bucket_slug, 'hp_listing_category');
            if (is_object($term)) { $candidates[] = absint($term->term_id ?? 0); }
        }

        $rule = $this->ebay_rule_by_id((string) ($row['rule_id'] ?? ''), $settings);
        $rule_slug = sanitize_title((string) ($rule['target_term_slug'] ?? ''));
        if ($rule_slug !== '' && function_exists('get_term_by')) {
            $term = get_term_by('slug', $rule_slug, 'hp_listing_category');
            if (is_object($term)) { $candidates[] = absint($term->term_id ?? 0); }
        }

        foreach (array_values(array_unique(array_filter(array_map('absint', $candidates)))) as $candidate) {
            $valid = $this->ebay_validate_private_target_term_id($candidate, $settings);
            if (!is_wp_error($valid)) { return absint($valid->term_id ?? 0); }
        }
        return 0;
    }

    private function ebay_persist_recovered_private_target($row, $term_id) {
        $row = is_array($row) ? $row : array();
        $term_id = absint($term_id);
        if ($term_id <= 0) { return false; }
        global $wpdb;
        $row_id = absint($row['id'] ?? 0);
        if ($row_id > 0 && is_object($wpdb)) {
            $wpdb->update($this->ebay_items_table(), array('target_term_id'=>$term_id,'updated_at'=>time()), array('id'=>$row_id), array('%d','%d'), array('%d'));
        }
        $listing_id = absint($row['listing_post_id'] ?? 0);
        if ($listing_id > 0 && function_exists('update_post_meta')) {
            update_post_meta($listing_id, '_ppar_ebay_target_term_id', $term_id);
        }
        return true;
    }

    private function ebay_validate_private_target_term_id($term_id, $settings) {
        $term_id = absint($term_id);
        $root_id = absint($settings['private_root_term_id'] ?? 0);
        if ($term_id <= 0 || $root_id <= 0 || !function_exists('get_term')) {
            return new WP_Error('ebay_review_target_missing', 'Gültige eBay-HivePress-Zielkategorie fehlt.');
        }
        $term = get_term($term_id, 'hp_listing_category');
        if (!$term || is_wp_error($term)) { return new WP_Error('ebay_review_target_missing', 'Gewählte HivePress-Zielkategorie existiert nicht.'); }
        if (sanitize_title((string) ($term->slug ?? '')) === 'ebay-privatanzeigen') {
            return new WP_Error('ebay_review_target_legacy_provider', 'Die frühere Provider-Kategorie „eBay-Privatanzeigen“ ist kein gültiges Ziel mehr.');
        }
        $parent = absint($term->parent ?? 0);
        if ($parent !== $root_id) {
            return new WP_Error('ebay_review_target_outside_root', 'Manuelles Ziel muss eine direkte Unterkategorie von „Private Anzeigen“ sein.');
        }
        return $term;
    }

    private function ebay_target_from_candidate_decision($decision, $settings) {
        $decision = is_array($decision) ? $decision : array();
        if (sanitize_key((string) ($decision['status'] ?? 'automatic')) !== 'approved') {
            return new WP_Error('ebay_review_decision_not_approved', 'Keine manuelle Freigabe vorhanden.');
        }
        $payload = is_array($decision['payload'] ?? null) ? $decision['payload'] : array();
        $target_key = sanitize_text_field((string) ($payload['target_key'] ?? ''));
        if (!preg_match('/^hp_listing_category:(\d+)$/', $target_key, $m)) {
            return new WP_Error('ebay_review_target_payload_invalid', 'Manuelle Freigabe enthält kein gültiges HivePress-Ziel.');
        }
        return $this->ebay_validate_private_target_term_id(absint($m[1]), $settings);
    }

    private function ebay_manual_classification($term, $item, $reason = '') {
        $term_id = absint(is_object($term) ? ($term->term_id ?? 0) : 0);
        $slug = sanitize_title(is_object($term) ? (string) ($term->slug ?? '') : '');
        $label = sanitize_text_field(is_object($term) ? (string) ($term->name ?? '') : '');
        return array(
            'status'=>'ready',
            'score'=>100,
            'product_slug'=>$slug,
            'product_title'=>$label,
            'hub'=>'Private Anzeigen',
            'main_hub'=>'Anzeigenmarkt',
            'path'=>'Private Anzeigen > ' . $label,
            'private_bucket_slug'=>$slug,
            'horse_hits'=>array(),
            'strong_horse_hits'=>array(),
            'hits'=>array(),
            'evidence_hash'=>hash('sha256', (string) ($item['source_hash'] ?? '') . '|manual|' . $term_id),
            'manual_override'=>true,
            'manual_reason'=>sanitize_text_field((string) $reason),
        );
    }

    private function ebay_store_review_candidate($item, $rule, $seller_type, $error, $settings) {
        $item = is_array($item) ? $item : array();
        $rule = is_array($rule) ? $rule : array();
        $seller_type = strtoupper(sanitize_key((string) $seller_type));
        $code = $this->ebay_error_code($error, 'ebay_review_required');
        $message = is_wp_error($error) ? (string) $error->get_error_message() : sanitize_text_field((string) $error);
        $item['portal_classification'] = array(
            'status'=>'review',
            'reason_code'=>$code,
            'reason'=>$message,
            'evidence_hash'=>hash('sha256', (string) ($item['source_hash'] ?? '') . '|review|' . $code),
        );
        $route = $seller_type === 'INDIVIDUAL' ? 'private_review' : 'business_review';
        $stored = $this->ebay_upsert_item($item, $rule, $route, 0, $settings);
        if (is_wp_error($stored)) { return $stored; }
        global $wpdb;
        $wpdb->update($this->ebay_items_table(), array(
            'status'=>'review',
            'source_state'=>'available',
            'policy_state'=>'allowed',
            'route_state'=>'review',
            'output_state'=>'none',
            'policy_version'=>self::EBAY_CONTENT_POLICY_VERSION,
            'classifier_version'=>$seller_type === 'INDIVIDUAL' ? self::EBAY_PRIVATE_CLASSIFIER_VERSION : self::EBAY_BUSINESS_CLASSIFIER_VERSION,
            'rejection_reason'=>'[' . $code . '] ' . $message,
            'updated_at'=>time(),
        ), array('id'=>absint($stored['id'])));
        $stored['status'] = 'review';
        $stored['rejection_reason'] = '[' . $code . '] ' . $message;
        if ($seller_type === 'INDIVIDUAL') {
            $this->ebay_private_listing_route_meta($stored, 'review', $message);
        }
        return $stored;
    }

    private function ebay_review_candidates($limit = 100) {
        global $wpdb;
        $limit = max(1, min(250, absint($limit)));
        return $wpdb->get_results($wpdb->prepare(
            "SELECT * FROM {$this->ebay_items_table()} WHERE status='review' ORDER BY updated_at DESC, id DESC LIMIT %d",
            $limit
        ), ARRAY_A);
    }

    private function ebay_private_review_targets($settings = null) {
        $settings = is_array($settings) ? $settings : $this->ebay_settings();
        $root_id = absint($settings['private_root_term_id'] ?? 0);
        if ($root_id <= 0 || !function_exists('get_terms')) { return array(); }
        $terms = get_terms(array(
            'taxonomy'=>'hp_listing_category',
            'parent'=>$root_id,
            'hide_empty'=>false,
            'orderby'=>'name',
            'order'=>'ASC',
        ));
        return is_wp_error($terms) ? array() : array_values(array_filter((array) $terms, 'is_object'));
    }

    /**
     * Resolve one persisted rule id without widening the BUSINESS contract.
     *
     * Static configured rules keep precedence. Persisted BUSINESS source rows,
     * however, legitimately store the concept id of one dynamically generated
     * catalog profile as rule_id. Rebuild only that exact authoritative catalog
     * rule when the corresponding BUSINESS bucket is currently enabled. Unknown
     * ids, disabled BUSINESS, disabled buckets or malformed catalog concepts stay
     * fail-closed. No fuzzy/alias inference is permitted here.
     */
    private function ebay_rule_by_id($rule_id, $settings = null) {
        $settings = is_array($settings) ? $settings : $this->ebay_settings();
        $rule_id = sanitize_key((string) $rule_id);
        if ($rule_id === '') { return array(); }
        foreach ((array) ($settings['rules'] ?? array()) as $rule) {
            if (sanitize_key((string) ($rule['id'] ?? '')) === $rule_id) { return is_array($rule) ? $rule : array(); }
        }
        return $this->ebay_dynamic_business_rule_by_id($rule_id, $settings);
    }

    private function ebay_dynamic_business_rule_by_id($rule_id, $settings) {
        $rule_id = sanitize_key((string) $rule_id);
        $settings = is_array($settings) ? $settings : array();
        if ($rule_id === '' || empty($settings['business_enabled'])) { return array(); }

        $enabled_buckets = array();
        foreach ((array) ($settings['rules'] ?? array()) as $rule) {
            if (!is_array($rule) || empty($rule['active']) || empty($rule['business'])) { continue; }
            $bucket = sanitize_title((string) ($rule['target_term_slug'] ?? $rule['id'] ?? ''));
            if ($bucket !== '') { $enabled_buckets[$bucket] = true; }
        }
        if (!$enabled_buckets) { return array(); }

        $catalog = $this->ebay_portal_catalog();
        if (is_wp_error($catalog)) { return array(); }
        $collections = array(
            'product'=>(array) ($catalog['business_concepts'] ?? array()),
            'hub'=>(array) ($catalog['business_hub_concepts'] ?? array()),
        );
        foreach ($collections as $concept_kind => $concepts) {
            foreach ($concepts as $concept) {
                if (!is_array($concept) || sanitize_key((string) ($concept['id'] ?? '')) !== $rule_id) { continue; }
                $primary = is_array($concept['target_pages'][0] ?? null) ? $concept['target_pages'][0] : array();
                $bucket = sanitize_title((string) ($primary['private_bucket_slug'] ?? $concept['private_bucket_slug'] ?? ''));
                if ($bucket === '' || empty($enabled_buckets[$bucket])) { return array(); }
                $query = $this->ebay_business_concept_query(array('title'=>(string) ($concept['title'] ?? '')));
                if ($query === '') { return array(); }
                return array(
                    'id'=>$rule_id,
                    'label'=>sanitize_text_field((string) ($concept['title'] ?? '')),
                    'query'=>$query,
                    'target_term_slug'=>$bucket,
                    'private'=>false,
                    'business'=>true,
                    'active'=>true,
                    'business_concept_id'=>$rule_id,
                    'business_concept_kind'=>$concept_kind,
                    'request_limit'=>30,
                );
            }
        }
        return array();
    }

    /** Manual approval persists only the decision/source row. Any follow-up
     * lifecycle work is owned by the same canonical durable run used everywhere
     * else; no standalone PRIVATE selector may be created from an admin action. */
    private function ebay_review_selection_after_approval($settings = null) {
        $run=method_exists($this,'ebay_run_load')?$this->ebay_run_load():array();
        if(method_exists($this,'ebay_run_is_active') && $this->ebay_run_is_active($run)){
            $this->ebay_run_schedule_worker(10);
            return array('status'=>'deferred_to_canonical_run','run_uuid'=>(string)($run['run_uuid']??''),'queued'=>0);
        }
        if(method_exists($this,'ebay_run_start')){
            return $this->ebay_run_start(true,'refresh');
        }
        return new WP_Error('canonical_run_unavailable','Kanonischer eBay-Gesamtlauf ist nicht verfügbar.');
    }

    public function handle_ebay_review_decision() {
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.'); }
        check_admin_referer('ppar_ebay_review_decision', 'ppar_ebay_nonce');
        $row_id = absint($_POST['row_id'] ?? 0);
        $decision = sanitize_key((string) ($_POST['review_decision'] ?? ''));
        $reason = sanitize_text_field(wp_unslash((string) ($_POST['reason'] ?? '')));
        $target_term_id = absint($_POST['target_term_id'] ?? 0);
        $result = null;

        if ($row_id <= 0 || !in_array($decision, array('approve','veto'), true)) {
            $result = new WP_Error('ebay_review_request_invalid', 'Prüfentscheidung ist unvollständig.');
        }
        if (!is_wp_error($result) && $reason === '') {
            $result = new WP_Error('ebay_review_reason_missing', 'Für eine Chefentscheidung ist eine Begründung erforderlich.');
        }

        global $wpdb;
        $row = !is_wp_error($result) ? $wpdb->get_row($wpdb->prepare("SELECT * FROM {$this->ebay_items_table()} WHERE id=%d", $row_id), ARRAY_A) : null;
        if (!is_wp_error($result) && (!is_array($row) || (string) ($row['status'] ?? '') !== 'review')) {
            $result = new WP_Error('ebay_review_candidate_missing', 'Prüfkandidat ist nicht mehr offen.');
        }

        $settings = $this->ebay_settings();
        if (!is_wp_error($result) && absint($row['fresh_until'] ?? 0) < time()) {
            $result = new WP_Error('ebay_review_candidate_stale', 'Prüfkandidat ist älter als sechs Stunden und darf nicht freigegeben werden. Bitte zuerst neu abrufen.');
        }
        $seller_type = !is_wp_error($result) ? strtoupper(sanitize_key((string) ($row['seller_account_type'] ?? ''))) : '';
        if (!is_wp_error($result) && $seller_type !== 'INDIVIDUAL') {
            $result = new WP_Error('ebay_review_private_only', 'Diese Prüfentscheidung ist ausschließlich für private eBay-Listings vorgesehen.');
        }

        $payload = !is_wp_error($result) ? json_decode((string) ($row['source_payload'] ?? ''), true) : array();
        $raw = is_array($payload) && is_array($payload['raw'] ?? null) ? $payload['raw'] : array();
        $item = !is_wp_error($result) ? $this->ebay_accept_item($raw, 'INDIVIDUAL', $settings) : $result;
        if (!is_wp_error($result) && is_wp_error($item)) { $result = $item; }

        $portal_key = method_exists($this, 'output_local_portal_key') ? sanitize_key((string) $this->output_local_portal_key()) : '';
        if (!is_wp_error($result) && $portal_key === '') {
            $result = new WP_Error('ebay_review_portal_missing', 'Portalkontext für Chefentscheidung fehlt.');
        }

        if (!is_wp_error($result) && $decision === 'veto') {
            $saved = $this->control_set_decision(
                $portal_key,
                'output',
                $this->ebay_candidate_scope_key((string) $item['item_id']),
                'veto',
                $reason,
                array('provider'=>'ebay'),
                'ebay_candidate_veto'
            );
            if (is_wp_error($saved)) { $result = $saved; }
            else {
                $wpdb->update($this->ebay_items_table(), array(
                    'status'=>'blocked_manual',
                    'rejection_reason'=>'[ebay_manual_veto] ' . $reason,
                    'updated_at'=>time(),
                ), array('id'=>$row_id), array('%s','%s','%d'), array('%d'));
                $result = array('status'=>'vetoed','item_id'=>(string) $item['item_id']);
            }
        }

        if (!is_wp_error($result) && $decision === 'approve') {
            $term = $this->ebay_validate_private_target_term_id($target_term_id, $settings);
            if (is_wp_error($term)) { $result = $term; }
            else {
                $target_key = 'hp_listing_category:' . absint($term->term_id ?? 0);
                $saved = $this->control_set_decision(
                    $portal_key,
                    'output',
                    $this->ebay_candidate_scope_key((string) $item['item_id']),
                    'approved',
                    $reason,
                    array(
                        'provider'=>'ebay',
                        'target_type'=>'hp_listing_category',
                        'target_key'=>$target_key,
                        'target_label'=>sanitize_text_field((string) ($term->name ?? '')),
                        'target_context'=>'ebay_private_review',
                    ),
                    'ebay_candidate_approval'
                );
                if (is_wp_error($saved)) { $result = $saved; }
                else {
                    $classification = $this->ebay_manual_classification($term, $item, $reason);
                    $item['portal_classification'] = $classification;
                    $rule = $this->ebay_rule_by_id((string) ($row['rule_id'] ?? ''), $settings);
                    if (!$rule) {
                        // Das manuelle Ziel ist maßgeblich; ein alter Regelbezug darf die
                        // Freigabe nicht verlieren. Für Audit bleibt die alte ID erhalten.
                        $rule = array('id'=>sanitize_key((string) ($row['rule_id'] ?? 'manual_review')));
                    }
                    $stored = $this->ebay_upsert_item($item, $rule, 'private', absint($term->term_id ?? 0), $settings);
                    if (is_wp_error($stored)) { $result = $stored; }
                    else {
                        // Approval changes only the durable source/manual-decision state.
                        // Publication is owned exclusively by the bounded PRIVATE selector,
                        // which prunes first and therefore can never overshoot the 250 cap.
                        $selection = $this->ebay_review_selection_after_approval($settings);
                        $result = array('status'=>'approved','item_id'=>(string) $item['item_id'],'listing_post_id'=>0,'capacity'=>array('status'=>sanitize_key((string)($selection['status']??'pending')),'queued'=>absint($selection['queued']??1)));
                    }
                }
            }
        }

        $ok = !is_wp_error($result);
        $message = $ok
            ? ($decision === 'approve' ? 'Prüfkandidat freigegeben; Veröffentlichung erfolgt ausschließlich über die bounded PRIVATE-Auswahl.' : 'Prüfkandidat per Chef-Veto gesperrt.')
            : $result->get_error_message();
        wp_safe_redirect(add_query_arg(array(
            'page'=>'affiliate-portal-ebay',
            'ppar_ebay'=>$ok ? 'review_saved' : 'review_failed',
            'message'=>rawurlencode($message),
        ), admin_url('admin.php')));
        exit;
    }

    private function ebay_sync_job_load() {
        if (method_exists($this, 'ebay_run_phase_state_load')) {
            $run = method_exists($this, 'ebay_run_load') ? $this->ebay_run_load() : array();
            if ((string)($run['schema'] ?? '') === '1.0') {
                $job = $this->ebay_run_phase_state_load('discovery');
                return is_array($job) ? $job : array();
            }
        }
        $job = get_option(self::OPTION_EBAY_SYNC_JOB, array());
        return is_array($job) ? $job : array();
    }

    private function ebay_sync_job_save($job) {
        $job = is_array($job) ? $job : array();
        if ((string)($job['schema'] ?? '') === '2.0' && (string)($job['engine'] ?? '') === 'resumable-background') {
            $job['state_contract'] = 'sync-v2';
            $job['build'] = self::EBAY_RUNTIME_BUILD;
            if (isset($job['summary']) && is_array($job['summary'])) {
                $job['summary']['state_contract'] = 'sync-v2';
                $job['summary']['build'] = self::EBAY_RUNTIME_BUILD;
            }
        }
        $job['updated_at'] = time();
        if (method_exists($this, 'ebay_run_load') && (string)(($this->ebay_run_load())['schema'] ?? '') === '1.0') {
            $this->ebay_run_phase_state_save('discovery', $job);
        } else {
            update_option(self::OPTION_EBAY_SYNC_JOB, $job, false);
        }
        return $job;
    }

    /** Narrow migration bridge for the patch states actually deployed/tested on
     * 13.08.2026. New saves move immediately onto the stable state_contract. */
    private function ebay_known_patch_state_build($build) {
        $build = (string)$build;
        if ($build === '') { return false; }
        if (hash_equals((string)self::EBAY_RUNTIME_BUILD, $build)) { return true; }
        return in_array($build, array(
            '6.40.3-consolidated-manual-orchestrator-20260813',
            '6.40.4-manual-partial-resume-20260813',
            '6.40.5-bounded-refresh-selection-handoff-20260813',
            '6.40.6-state-continuity-no-restart-20260813',
            '6.40.7-manual-chain-continuity-20260813',
        ), true);
    }

    private function ebay_sync_job_runtime_compatible($job) {
        if (!is_array($job)) { return false; }
        $build = (string) ($job['build'] ?? '');
        $schema = (string) ($job['schema'] ?? '');
        $engine = (string) ($job['engine'] ?? '');
        $contract = (string)($job['state_contract'] ?? '');
        if ($schema !== '2.0' || $engine !== 'resumable-background') { return false; }
        return $contract === 'sync-v2' || $this->ebay_known_patch_state_build($build);
    }

    private function ebay_sync_job_is_open($job) {
        return $this->ebay_sync_job_runtime_compatible($job)
            && in_array(sanitize_key((string) ($job['status'] ?? '')), array('queued','running'), true);
    }

    /**
     * Runtime-stamp an open job so an older resumable queue can be resumed safely
     * after updating the current build. This prevents a mixed-version run from being reported
     * as an unidentifiable legacy sync and carries the required HivePress owner.
     */
    private function ebay_sync_job_stamp_runtime(&$job, $author_id = 0) {
        if (!is_array($job)) { $job = array(); }
        $job['schema'] = '2.0';
        $job['engine'] = 'resumable-background';
        $job['state_contract'] = 'sync-v2';
        $job['build'] = self::EBAY_RUNTIME_BUILD;
        if (absint($author_id) > 0) { $job['listing_author_id'] = absint($author_id); }
        if (!isset($job['summary']) || !is_array($job['summary'])) { $job['summary'] = array(); }
        $job['summary']['schema'] = '2.0';
        $job['summary']['engine'] = 'resumable-background';
        $job['summary']['state_contract'] = 'sync-v2';
        $job['summary']['build'] = self::EBAY_RUNTIME_BUILD;
        return $job;
    }

    /**
     * Missing BUSINESS concepts for targeted discovery without running the
     * expensive complete selection planner inside discovery setup.
     *
     * Prefer the latest durable selection coverage because that state was
     * produced by the canonical bounded selector. If there is no trustworthy
     * completed coverage snapshot, fail safe by returning every required
     * physical concept. A recovery discovery may do extra bounded API work, but
     * it must never hide a gap because a diagnostic planner timed out.
     */
    private function ebay_business_recovery_missing_concept_ids() {
        $required = array_values(array_filter(array_map('sanitize_key', $this->ebay_business_required_product_concept_ids())));
        if (!$required) { return array(); }
        $required_map = array_fill_keys($required, true);

        // Canonical gap-fill is driven exclusively by the exact public-coverage
        // manifest of the same durable run. Never broaden this back to all
        // concepts or to an older selection snapshot.
        if (method_exists($this, 'ebay_run_load')) {
            $run = $this->ebay_run_load();
            $phase = sanitize_key((string)($run['phase'] ?? ''));
            if ((string)($run['schema'] ?? '') === '1.0'
                && in_array($phase, array('gapfill_discovery','gapfill_select'), true)) {
                // During a V6.56 churn revalidation, discovery touches only
                // families that became newly missing. Selection still owns the
                // complete monotonic gapfill.missing proof scope.
                $exact = is_array($run['gapfill']['discovery_missing'] ?? null) && $run['gapfill']['discovery_missing']
                    ? $run['gapfill']['discovery_missing']
                    : (is_array($run['gapfill']['missing'] ?? null) ? $run['gapfill']['missing'] : array());
                $out = array();
                foreach ($exact as $concept_id) {
                    $concept_id = sanitize_key((string)$concept_id);
                    if ($concept_id !== '' && isset($required_map[$concept_id])) { $out[$concept_id] = 1; }
                }
                return array_keys($out);
            }
        }

        $state = $this->ebay_selection_state_load();
        $business = is_array($state['plan_stats']['business'] ?? null) ? $state['plan_stats']['business'] : array();
        $snapshot_required = absint($business['required'] ?? 0);
        $missing = is_array($business['missing_concepts'] ?? null) ? $business['missing_concepts'] : array();
        $snapshot_status = sanitize_key((string)($state['status'] ?? ''));
        if ($snapshot_required === count($required) && in_array($snapshot_status, array('complete','running','preparing'), true)) {
            $out = array();
            foreach ($missing as $concept_id) {
                $concept_id = sanitize_key((string)$concept_id);
                if ($concept_id !== '' && isset($required_map[$concept_id])) { $out[$concept_id] = 1; }
            }
            // A complete snapshot with zero missing concepts is authoritative.
            if ($snapshot_status === 'complete' || $out) { return array_keys($out); }
        }
        return $required;
    }

    private function ebay_sync_profiles($settings, $scope = 'all') {
        $profiles = array();
        $scope = sanitize_key((string)$scope);
        if (!in_array($scope, array('all','business_recovery'), true)) { return array(); }
        // V6.17/V6.56: exact BUSINESS product coverage comes first and is generated
        // from the complete verified catalog, never from a hand-maintained list.
        if ($scope === 'all' || $scope === 'business_recovery') {
            $catalog_profiles = $this->ebay_business_catalog_profiles($settings);
            if ($scope === 'business_recovery') {
                // Gap-fill is coverage-driven. Never rescan all 300+ concepts when
                // only a subset is actually missing from the current qualified pool.
                $missing = array_fill_keys($this->ebay_business_recovery_missing_concept_ids(), true);
                foreach ($catalog_profiles as $key => $profile) {
                    $concept_id = sanitize_key((string)($profile['expected_business_concept_id'] ?? ''));
                    if ($concept_id !== '' && isset($missing[$concept_id])) { $profiles[$key] = $profile; }
                }
            } else {
                foreach ($catalog_profiles as $key => $profile) { $profiles[$key] = $profile; }
            }
        }

        // PRIVATE keeps its coarse, controlled variants. One first page per
        // profile is enough for breadth; inventory/lifecycle refresh is separate.
        if ($scope !== 'business_recovery') foreach ((array)($settings['rules'] ?? array()) as $rule) {
            if (!is_array($rule) || empty($rule['active']) || empty($settings['private_enabled']) || empty($rule['private'])) { continue; }
            $rule_id_for_supply = sanitize_key((string)($rule['id'] ?? ''));
            foreach ($this->ebay_private_query_variants($rule) as $query_index => $query_text) {
                $profile_rule = $rule;
                $profile_rule['query'] = $query_text;
                // V6.27: Reitstiefel variants are constrained to eBay DE's
                // dedicated riding-boots category. This prevents generic boot
                // noise while still allowing several independent PRIVATE pools.
                $qid = sanitize_key((string)($rule['id'] ?? ''));
                $qnorm = $this->ebay_topic_text($query_text);
                if ($qid === 'reitbekleidung-zubehoer' && in_array($qnorm, array('reitstiefel','lederreitstiefel','dressurstiefel','reitgummistiefel'), true)) {
                    $profile_rule['category_ids'] = array('183382');
                }
                $key = sanitize_key((string)($rule['id'] ?? '')) . '|INDIVIDUAL|q' . ($query_index + 1);
                $boot_profile = $qid === 'reitbekleidung-zubehoer' && in_array($qnorm, array('reitstiefel','lederreitstiefel','dressurstiefel','reitgummistiefel'), true);
                $profiles[$key] = array(
                    'key'=>$key,'rule'=>$profile_rule,'seller_type'=>'INDIVIDUAL','next'=>'','active'=>true,'pages'=>0,
                    'page_limit'=>$boot_profile ? 3 : 1,'route_limit'=>0,'profile_kind'=>'private_variant',
                );
            }
        }

        // Keep one coarse BUSINESS fallback per enabled rule after the exact
        // catalog sweep. It can discover unusual/new wording, but can no longer
        // starve exact product families because it is not the primary discovery.
        if ($scope === 'all') foreach ((array)($settings['rules'] ?? array()) as $rule) {
            if (!is_array($rule) || empty($rule['active']) || empty($settings['business_enabled']) || empty($rule['business'])) { continue; }
            foreach ($this->ebay_business_query_variants($rule) as $query_index => $query_text) {
                $profile_rule = $rule;
                $profile_rule['query'] = $query_text;
                $key = sanitize_key((string)($rule['id'] ?? '')) . '|BUSINESS|fallback-q' . ($query_index + 1);
                $profiles[$key] = array(
                    'key'=>$key,'rule'=>$profile_rule,'seller_type'=>'BUSINESS','next'=>'','active'=>true,'pages'=>0,
                    'page_limit'=>1,'route_limit'=>3,'profile_kind'=>'business_fallback',
                );
            }
        }
        return $profiles;
    }

    private function ebay_sync_summary_new($settings, $run_uuid, $profiles) {
        $max_pages = max(1, absint($settings['max_pages_per_profile'] ?? 4));
        $max_requests = max(1, absint($settings['max_requests_per_run'] ?? 40));
        $profile_stats = array();
        foreach ((array) $profiles as $key => $profile) {
            $profile_stats[$key] = array(
                'rule'=>sanitize_key((string) ($profile['rule']['id'] ?? '')),
                'query'=>sanitize_text_field((string) ($profile['rule']['query'] ?? '')),
                'seller_type'=>(string) ($profile['seller_type'] ?? ''),
                'profile_kind'=>sanitize_key((string)($profile['profile_kind'] ?? 'generic')),
                'expected_business_concept_id'=>sanitize_key((string)($profile['expected_business_concept_id'] ?? '')),
                'page_limit'=>max(1, absint($profile['page_limit'] ?? $max_pages)),
                'route_limit'=>absint($profile['route_limit'] ?? 0),
                'requests'=>0,'pages'=>0,'received'=>0,'accepted'=>0,'capacity_skipped'=>0,'review_pending'=>0,
                'hard_blocked'=>0,'technical_blocked'=>0,'manual_vetoed'=>0,'duplicates_skipped'=>0,
                'hard_reasons'=>array(),'review_reasons'=>array(),'technical_reasons'=>array(),'manual_veto_reasons'=>array(),
                'complete'=>false,'stopped_reason'=>'',
            );
        }
        return array(
            'schema'=>'2.0','engine'=>'resumable-background','build'=>self::EBAY_RUNTIME_BUILD,
            'status'=>'running','run_uuid'=>$run_uuid,'profiles'=>count($profiles),'requests'=>0,'request_batches'=>1,'pages'=>0,'received'=>0,'received_unique'=>0,
            'technically_valid'=>0,'accepted'=>0,'capacity_skipped'=>0,'duplicates_skipped'=>0,'private_candidates'=>0,'private_listings'=>0,'business_creatives'=>0,
            'review_pending'=>0,'hard_blocked'=>0,'technical_blocked'=>0,'manual_vetoed'=>0,'blocked'=>0,
            'hard_reasons'=>array(),'review_reasons'=>array(),'technical_reasons'=>array(),'manual_veto_reasons'=>array(),
            'errors'=>array(),'profile_stats'=>$profile_stats,
            'budget'=>array(
                'page_size'=>absint($settings['max_per_rule'] ?? 50),
                'max_pages_per_profile'=>$max_pages,
                'max_requests_per_run'=>$max_requests,
                'max_requests_per_batch'=>$max_requests,
                'worker_time_budget_seconds'=>max(10, min(30, absint($settings['run_time_budget_seconds'] ?? 20))),
                'segment_limit_seconds'=>600,
                'stopped_reason'=>'',
            ),
            'started_at'=>time(),'segments'=>1,
        );
    }

    private function ebay_schedule_worker_fallback($delay = 12) {
        if (method_exists($this, 'ebay_run_load') && (string)(($this->ebay_run_load())['schema'] ?? '') === '1.0') { return true; }
        if (!function_exists('wp_next_scheduled') || !function_exists('wp_schedule_single_event')) { return; }
        if (!wp_next_scheduled(self::EBAY_WORKER_HOOK)) {
            wp_schedule_single_event(time() + max(10, absint($delay)), self::EBAY_WORKER_HOOK);
        }
    }

    private function ebay_dispatch_worker($job = null) {
        $job = is_array($job) ? $job : $this->ebay_sync_job_load();
        if (!$this->ebay_sync_job_is_open($job)) { return false; }
        // Single background transport: queue the WordPress worker hook only.
        // The failed V6.21–V6.40 family used plugin-owned self-HTTP loopbacks in
        // parallel with Cron/browser ticks; that created hidden start races and
        // made host loopback behaviour part of correctness. Explicit admin start
        // can run one bounded package itself; continuation is queued here.
        $this->ebay_schedule_worker_fallback(12);
        return true;
    }

    /**
     * V5.21 – harte Segmentgrenze fuer Discovery. Ein einzelner manueller oder
     * Cron-getriebener Lauf darf die Admin-Oberflaeche nicht stundenlang binden.
     * Bereits verarbeitete Ergebnisse bleiben idempotent gespeichert; ein wegen
     * Zeitbudget partieller Job kann beim naechsten Abruf exakt fortgesetzt werden.
     */
    private function ebay_sync_segment_limit_seconds($job = array()) {
        return 600; // 10 Minuten harte Obergrenze je Segment.
    }

    private function ebay_sync_segment_expired($job) {
        if (!$this->ebay_sync_job_is_open($job)) { return false; }
        $started = absint($job['segment_started_at'] ?? ($job['created_at'] ?? 0));
        return $started > 0 && (time() - $started) >= $this->ebay_sync_segment_limit_seconds($job);
    }

    /** V6.17: roll a long full-catalog discovery into a new safe segment instead
     * of abandoning the remaining profiles. The job cursor and all accepted
     * results stay intact; only the 10-minute safety window is renewed. */
    private function ebay_sync_roll_segment(&$job) {
        if (!is_array($job)) { return; }
        $job['segment_started_at'] = time();
        $job['created_at'] = time();
        if (!isset($job['summary']) || !is_array($job['summary'])) { $job['summary'] = array(); }
        $job['summary']['segments'] = absint($job['summary']['segments'] ?? 1) + 1;
        if (!isset($job['summary']['budget']) || !is_array($job['summary']['budget'])) { $job['summary']['budget'] = array(); }
        $job['summary']['budget']['stopped_reason'] = '';
        $job['worker_phase'] = 'segment_boundary';
        $this->ebay_sync_touch_progress($job, 'segment_boundary');
    }

    private function ebay_sync_job_is_resumable_partial($job) {
        if (!$this->ebay_sync_job_runtime_compatible($job) || sanitize_key((string) ($job['status'] ?? '')) !== 'partial') { return false; }
        $reason = sanitize_key((string) (($job['summary']['budget']['stopped_reason'] ?? '')));
        if ($reason !== 'segment_time_budget') { return false; }
        if (!empty($job['current_page']) && is_array($job['current_page'])) { return true; }
        return $this->ebay_sync_active_profile_key($job) !== '';
    }

    private function ebay_sync_resume_partial_job($job, $author_id) {
        $job = is_array($job) ? $job : array();
        if (!$this->ebay_sync_job_is_resumable_partial($job)) { return array(); }
        $job['status'] = 'queued';
        $job['worker_phase'] = 'queued';
        $job['finished_at'] = 0;
        $job['created_at'] = time();
        $job['segment_started_at'] = time();
        $job['last_worker_at'] = 0;
        $job['last_progress_at'] = time();
        $this->ebay_sync_job_stamp_runtime($job, $author_id);
        if (!isset($job['summary']) || !is_array($job['summary'])) { $job['summary'] = array(); }
        $job['summary']['status'] = 'running';
        $job['summary']['finished_at'] = 0;
        if (!isset($job['summary']['budget']) || !is_array($job['summary']['budget'])) { $job['summary']['budget'] = array(); }
        $job['summary']['budget']['stopped_reason'] = '';
        $job['summary']['budget']['segment_limit_seconds'] = $this->ebay_sync_segment_limit_seconds($job);
        $job['summary']['segments'] = absint($job['summary']['segments'] ?? 1) + 1;
        return $this->ebay_sync_job_save($job);
    }

    /** Map the durable discovery scope to the only selection scope it may own. */
    private function ebay_sync_job_selection_scope($job, $settings = null) {
        $settings=is_array($settings)?$settings:$this->ebay_settings();
        $scope=sanitize_key((string)(is_array($job)?($job['scope']??''):''));
        if($scope==='all'){return $this->ebay_selection_scope_for_enabled_routes('all',$settings);}
        if($scope==='business_recovery'){return $this->ebay_selection_scope_for_enabled_routes('business',$settings);}
        return ''; // fail-closed; never widen missing/legacy scope to ALL.
    }

    private function ebay_start_sync_job($manual = false, $scope = 'all', $transport = 'background') {
        $scope = sanitize_key((string)$scope);
        if (!in_array($scope, array('all','business_recovery'), true)) { return new WP_Error('ebay_sync_scope_invalid', 'Ungültiger eBay-Discovery-Scope.'); }
        $transport = sanitize_key((string)$transport);
        if ($transport !== 'background') { return new WP_Error('ebay_sync_transport_invalid', 'eBay-Discovery darf nur über den Hintergrundworker laufen.'); }
        $settings = $this->ebay_settings();
        if (empty($settings['enabled']) && !$manual) { return array('status'=>'disabled'); }
        $errors = $this->ebay_configuration_errors($settings);
        if ($errors) { return new WP_Error('ebay_configuration_invalid', implode(' ', $errors)); }
        $this->maybe_install_ebay_schema();
        $author_id = $this->ebay_persist_listing_author_id($settings);
        if (is_wp_error($author_id)) { return $author_id; }

        $refresh_job = $this->ebay_refresh_job_load();
        if ($this->ebay_refresh_job_is_open($refresh_job)) {
            return $manual
                ? new WP_Error('ebay_sync_refresh_running', 'Der eBay-Bestandsabgleich läuft bereits. Discovery startet erst danach.')
                : array('status'=>'deferred_refresh_running');
        }
        $selection_guard=$this->ebay_selection_state_load();
        if($this->ebay_selection_state_is_open($selection_guard)){
            return $manual
                ? new WP_Error('ebay_sync_selection_running','Eine Bestandsauswahl läuft bereits. Discovery startet erst nach deren Abschluss.')
                : array('status'=>'deferred_selection_running');
        }

        $existing = $this->ebay_sync_job_load();
        if ($this->ebay_sync_job_is_open($existing)) {
            $this->ebay_sync_job_stamp_runtime($existing, $author_id);
            $existing['transport'] = $transport;
            $this->ebay_sync_job_save($existing);
            $this->ebay_dispatch_worker($existing);
            return array('status'=>'already_running','run_uuid'=>(string) ($existing['run_uuid'] ?? ''),'summary'=>(array) ($existing['summary'] ?? array()));
        }
        if ($this->ebay_sync_job_is_resumable_partial($existing)) {
            $existing_scope = sanitize_key((string)($existing['scope'] ?? ''));
            if ($existing_scope === $scope) {
                $resumed = $this->ebay_sync_resume_partial_job($existing, $author_id);
                if ($resumed) {
                    $resumed['transport'] = $transport;
                    $this->ebay_sync_job_save($resumed);
                    $this->ebay_dispatch_worker($resumed);
                    return array('status'=>'resumed','run_uuid'=>(string) ($resumed['run_uuid'] ?? ''),'summary'=>(array) ($resumed['summary'] ?? array()));
                }
            }
        }

        $profiles = $this->ebay_sync_profiles($settings, $scope);
        if (!$profiles) { return new WP_Error('ebay_profiles_empty', 'Keine aktiven eBay-Abrufprofile vorhanden.'); }
        $canonical_run = method_exists($this, 'ebay_run_load') ? $this->ebay_run_load() : array();
        $run_uuid = !empty($this->ebay_canonical_worker_active) && !empty($canonical_run['run_uuid']) ? sanitize_text_field((string)$canonical_run['run_uuid']) : (function_exists('wp_generate_uuid4') ? wp_generate_uuid4() : substr(hash('sha256', microtime(true) . '|' . mt_rand()), 0, 36));
        $worker_token = function_exists('wp_generate_password') ? wp_generate_password(48, false, false) : hash('sha256', $run_uuid . '|' . microtime(true) . '|' . mt_rand());
        $job = array(
            'schema'=>'2.0','engine'=>'resumable-background','build'=>self::EBAY_RUNTIME_BUILD,'status'=>'queued','run_uuid'=>$run_uuid,'worker_token'=>$worker_token,'manual'=>!empty($manual),'scope'=>$scope,'transport'=>$transport,'listing_author_id'=>absint($author_id),
            'created_at'=>time(),'segment_started_at'=>time(),'updated_at'=>time(),'finished_at'=>0,'worker_phase'=>'queued','last_worker_at'=>0,
            'profiles'=>$profiles,'profile_order'=>array_keys($profiles),'profile_cursor'=>0,'current_page'=>array(),'requests_in_batch'=>0,
            'summary'=>$this->ebay_sync_summary_new($settings, $run_uuid, $profiles),
            'routed_items'=>array(),'soft_pending'=>array(),'hard_seen'=>array(),'technical_valid'=>array(),'unique_received'=>array(),'manual_veto_seen'=>array(),
            'business_concept_accept_counts'=>array(),
        );
        $this->ebay_sync_job_save($job);
        $this->ebay_dispatch_worker($job);
        return array('status'=>'queued','run_uuid'=>$run_uuid,'summary'=>$job['summary']);
    }

    /**
     * V5.6.0 – Der öffentliche Einstieg startet nur noch einen fortsetzbaren
     * Hintergrundjob. Weder Admin-Request noch regulärer 3h-Cron führen den
     * kompletten paginierten Abruf synchron aus.
     */
    public function run_ebay_sync($manual = false) {
        return $this->ebay_run_start($manual, 'sync');
    }

    private function ebay_sync_active_profile_key($job) {
        $order = array_values((array) ($job['profile_order'] ?? array()));
        $profiles = (array) ($job['profiles'] ?? array());
        $count = count($order);
        if ($count <= 0) { return ''; }
        $start = absint($job['profile_cursor'] ?? 0) % $count;
        for ($offset = 0; $offset < $count; $offset++) {
            $idx = ($start + $offset) % $count;
            $key = (string) ($order[$idx] ?? '');
            if ($key !== '' && !empty($profiles[$key]['active'])) { return $key; }
        }
        return '';
    }

    private function ebay_sync_advance_cursor(&$job, $profile_key) {
        $order = array_values((array) ($job['profile_order'] ?? array()));
        $idx = array_search((string) $profile_key, $order, true);
        $job['profile_cursor'] = $idx === false || !$order ? 0 : (($idx + 1) % count($order));
    }

    private function ebay_sync_rebuild_review_summary(&$job) {
        $summary = (array) ($job['summary'] ?? array());
        $summary['review_pending'] = 0;
        $summary['review_reasons'] = array();
        foreach ((array) ($summary['profile_stats'] ?? array()) as $key => $stat) {
            $summary['profile_stats'][$key]['review_pending'] = 0;
            $summary['profile_stats'][$key]['review_reasons'] = array();
        }
        foreach ((array) ($job['soft_pending'] ?? array()) as $item_id => $pending) {
            if (isset($job['routed_items'][$item_id])) { continue; }
            $code = sanitize_key((string) ($pending['code'] ?? 'ebay_review_required'));
            if ($code === '') { $code = 'ebay_review_required'; }
            $profile_key = (string) ($pending['profile_key'] ?? '');
            $summary['review_pending']++;
            $summary['review_reasons'][$code] = absint($summary['review_reasons'][$code] ?? 0) + 1;
            if (isset($summary['profile_stats'][$profile_key])) {
                $summary['profile_stats'][$profile_key]['review_pending']++;
                $summary['profile_stats'][$profile_key]['review_reasons'][$code] = absint($summary['profile_stats'][$profile_key]['review_reasons'][$code] ?? 0) + 1;
            }
        }
        $job['summary'] = $summary;
    }

    private function ebay_sync_process_item(&$job, $raw, $profile_key, $settings) {
        if (!isset($job['profiles'][$profile_key])) { return; }
        $profile = $job['profiles'][$profile_key];
        $summary =& $job['summary'];
        $summary['profile_stats'][$profile_key] = isset($summary['profile_stats'][$profile_key]) ? $summary['profile_stats'][$profile_key] : array();
        $raw = is_array($raw) ? $raw : array();
        $raw_item_id = substr(sanitize_text_field((string) ($raw['itemId'] ?? '')), 0, 191);

        if ($raw_item_id !== '' && isset($job['routed_items'][$raw_item_id])) {
            $summary['duplicates_skipped']++;
            $summary['profile_stats'][$profile_key]['duplicates_skipped']++;
            return;
        }

        $item = $this->ebay_accept_item($raw, $profile['seller_type'], $settings);
        if (is_wp_error($item)) {
            $seen_key = $profile['seller_type'] . '|' . ($raw_item_id !== '' ? $raw_item_id : hash('sha256', wp_json_encode($raw)));
            if (!isset($job['hard_seen'][$seen_key])) {
                $job['hard_seen'][$seen_key] = true;
                $summary['hard_blocked']++;
                $summary['profile_stats'][$profile_key]['hard_blocked']++;
                $this->ebay_summary_reason_add($summary, 'hard', $item, (string) $profile['rule']['id'], $profile['seller_type'], $profile_key);
            } else {
                $summary['duplicates_skipped']++;
                $summary['profile_stats'][$profile_key]['duplicates_skipped']++;
            }
            return;
        }

        $item_id = (string) $item['item_id'];
        $job['technical_valid'][$item_id] = true;
        if (isset($job['routed_items'][$item_id])) {
            $summary['duplicates_skipped']++;
            $summary['profile_stats'][$profile_key]['duplicates_skipped']++;
            return;
        }

        $classification = null;
        if ($profile['seller_type'] === 'INDIVIDUAL') {
            $manual_decision = $this->ebay_candidate_manual_decision($item_id);
            $manual_status = sanitize_key((string) ($manual_decision['status'] ?? 'automatic'));
            if (in_array($manual_status, array('veto','paused'), true)) {
                if (!isset($job['manual_veto_seen'][$item_id])) {
                    $job['manual_veto_seen'][$item_id] = true;
                    $summary['manual_vetoed']++;
                    $summary['profile_stats'][$profile_key]['manual_vetoed']++;
                    $manual_error = new WP_Error('ebay_manual_veto', (string) ($manual_decision['reason'] ?? 'Manuelles Chef-Veto ist aktiv.'));
                    $this->ebay_summary_reason_add($summary, 'manual_veto', $manual_error, (string) $profile['rule']['id'], $profile['seller_type'], $profile_key);
                    $stored_veto = $this->ebay_store_review_candidate($item, $profile['rule'], $profile['seller_type'], $manual_error, $settings);
                    if (!is_wp_error($stored_veto)) {
                        global $wpdb;
                        $wpdb->update($this->ebay_items_table(), array('status'=>'blocked_manual','rejection_reason'=>'[ebay_manual_veto] ' . sanitize_text_field((string) ($manual_decision['reason'] ?? 'Manuelles Chef-Veto ist aktiv.')),'updated_at'=>time()), array('id'=>absint($stored_veto['id'])), array('%s','%s','%d'), array('%d'));
                    }
                }
                $job['routed_items'][$item_id] = 'manual_veto';
                unset($job['soft_pending'][$item_id]);
                return;
            }
            if ($manual_status === 'approved') {
                $term = $this->ebay_target_from_candidate_decision($manual_decision, $settings);
                if (is_wp_error($term)) {
                    $summary['technical_blocked']++;
                    $summary['profile_stats'][$profile_key]['technical_blocked']++;
                    $this->ebay_summary_reason_add($summary, 'technical', $term, (string) $profile['rule']['id'], $profile['seller_type'], $profile_key);
                    return;
                }
                $classification = $this->ebay_manual_classification($term, $item, (string) ($manual_decision['reason'] ?? 'Manuell freigegeben.'));
            }
        }

        if (!is_array($classification)) {
            $classification = $profile['seller_type'] === 'BUSINESS'
                ? $this->ebay_business_classify_portal_item_strict($item, $profile['rule'])
                : $this->ebay_classify_portal_item($item, $profile['rule']);
        }
        if (is_wp_error($classification)) {
            if ($this->ebay_is_soft_classification_error($classification)) {
                if (!isset($job['soft_pending'][$item_id])) {
                    $stored_review = $this->ebay_store_review_candidate($item, $profile['rule'], $profile['seller_type'], $classification, $settings);
                    if (is_wp_error($stored_review)) {
                        $summary['technical_blocked']++;
                        $summary['profile_stats'][$profile_key]['technical_blocked']++;
                        $this->ebay_summary_reason_add($summary, 'technical', $stored_review, (string) $profile['rule']['id'], $profile['seller_type'], $profile_key);
                        return;
                    }
                    $job['soft_pending'][$item_id] = array(
                        'code'=>$this->ebay_error_code($classification, 'ebay_review_required'),
                        'rule_id'=>(string) ($profile['rule']['id'] ?? ''),
                        'seller_type'=>$profile['seller_type'],
                        'profile_key'=>$profile_key,
                    );
                } else {
                    $summary['duplicates_skipped']++;
                    $summary['profile_stats'][$profile_key]['duplicates_skipped']++;
                }
                return;
            }
            $summary['technical_blocked']++;
            $summary['profile_stats'][$profile_key]['technical_blocked']++;
            $this->ebay_summary_reason_add($summary, 'technical', $classification, (string) $profile['rule']['id'], $profile['seller_type'], $profile_key);
            return;
        }

        $item['portal_classification'] = $classification;
        unset($job['soft_pending'][$item_id]);
        if ($profile['seller_type'] === 'BUSINESS') {
            // V6.19: every valid discovery hit enters the quality candidate pool.
            // No "first three wins" shortcut: ranking happens after the complete
            // discovery run, so better products found later can replace weaker ones.
            $quality = $this->ebay_business_quality_assess($item, $classification, $profile['rule'], $settings, 0.0);
            if (is_wp_error($quality)) {
                $summary['hard_blocked']++;
                $summary['profile_stats'][$profile_key]['hard_blocked']++;
                $this->ebay_summary_reason_add($summary, 'hard', $quality, (string) $profile['rule']['id'], $profile['seller_type'], $profile_key);
                $job['routed_items'][$item_id] = 'business_quality_blocked';
                return;
            }
            $item = $this->ebay_business_item_with_quality($item, $quality);
            $item['business_selection'] = array('role'=>'candidate','rank'=>0);
        }
        $target_term_id = 0;
        if ($profile['seller_type'] === 'INDIVIDUAL') {
            if (!empty($classification['manual_override'])) {
                $manual_decision = $this->ebay_candidate_manual_decision($item_id);
                $term = $this->ebay_target_from_candidate_decision($manual_decision, $settings);
                $target_term_id = is_wp_error($term) ? 0 : absint($term->term_id ?? 0);
            } else {
                $target_rule = $profile['rule'];
                $target_rule['target_term_slug'] = sanitize_title((string) ($classification['private_bucket_slug'] ?? ''));
                $target_term_id = $this->ebay_rule_target_term($target_rule, $settings);
                if (is_wp_error($target_term_id)) {
                    $summary['technical_blocked']++;
                    $summary['profile_stats'][$profile_key]['technical_blocked']++;
                    $this->ebay_summary_reason_add($summary, 'technical', $target_term_id, (string) $profile['rule']['id'], $profile['seller_type'], $profile_key);
                    $summary['errors'][] = array('rule'=>(string) $profile['rule']['id'],'seller_type'=>$profile['seller_type'],'item_id'=>$item_id,'error'=>$target_term_id->get_error_message(),'code'=>$target_term_id->get_error_code());
                    return;
                }
            }
            if ($target_term_id <= 0) {
                $target_error = new WP_Error('ebay_private_target_missing', 'HivePress-Zielkategorie fehlt.');
                $summary['technical_blocked']++;
                $summary['profile_stats'][$profile_key]['technical_blocked']++;
                $this->ebay_summary_reason_add($summary, 'technical', $target_error, (string) $profile['rule']['id'], $profile['seller_type'], $profile_key);
                return;
            }
        }

        $route = $profile['seller_type'] === 'INDIVIDUAL' ? 'private_hivepress' : 'business_affiliate';
        $stored = $this->ebay_upsert_item($item, $profile['rule'], $route, $target_term_id, $settings);
        if (is_wp_error($stored)) {
            $summary['technical_blocked']++;
            $summary['profile_stats'][$profile_key]['technical_blocked']++;
            $this->ebay_summary_reason_add($summary, 'technical', $stored, (string) $profile['rule']['id'], $profile['seller_type'], $profile_key);
            $summary['errors'][] = array('rule'=>(string) $profile['rule']['id'],'seller_type'=>$profile['seller_type'],'item_id'=>$item_id,'error'=>$stored->get_error_message(),'code'=>$stored->get_error_code());
            return;
        }
        if ($profile['seller_type'] === 'INDIVIDUAL') {
            // V6.19: discovery stores every valid PRIVATE offer only in the durable
            // eBay source table first. The existing HivePress materializer is called
            // later only for the bounded winners (250 portal-wide / 30 per leaf).
            // Excess offers therefore never create a new WordPress listing merely
            // to be drafted again at the end of the same full sync.
            $summary['private_candidates'] = absint($summary['private_candidates'] ?? 0) + 1;
        } else {
            // BUSINESS is intentionally not materialized per hit. The unchanged
            // creative/output route is called once by the final quality rebalancer.
            $this->ebay_business_persist_quality_on_source_row($stored, (array) ($item['business_quality'] ?? array()), 'candidate', 0);
            $summary['business_candidates'] = absint($summary['business_candidates'] ?? 0) + 1;
        }
        $job['routed_items'][$item_id] = $route;
        $summary['accepted']++;
        $summary['profile_stats'][$profile_key]['accepted']++;
    }

    /** V5.20: echter Fortschritt statt bloßem Worker-Heartbeat. */
    private function ebay_sync_touch_progress(&$job, $phase = '') {
        $job['progress_seq'] = absint($job['progress_seq'] ?? 0) + 1;
        $job['last_progress_at'] = time();
        if ($phase !== '') { $job['worker_phase'] = sanitize_key((string) $phase); }
    }

    private function ebay_sync_completion_state($job) {
        $stats = (array) (($job['summary']['profile_stats'] ?? array()));
        $partial_reasons = array();
        foreach ($stats as $stat) {
            $reason = sanitize_key((string) ($stat['stopped_reason'] ?? ''));
            $complete = !empty($stat['complete']);
            if (!$complete) {
                if ($reason === '') { $reason = 'profile_incomplete'; }
                $partial_reasons[$reason] = true;
            }
        }
        if ($partial_reasons) {
            $reasons = array_keys($partial_reasons);
            return array('status'=>'partial','reason'=>count($reasons) === 1 ? $reasons[0] : 'profile_incomplete');
        }
        return array('status'=>'completed','reason'=>'');
    }

    private function ebay_sync_finalize(&$job, $settings, $status = 'completed', $stopped_reason = '') {
        $this->ebay_sync_rebuild_review_summary($job);
        $summary =& $job['summary'];
        $summary['received_unique'] = count((array) ($job['unique_received'] ?? array()));
        $summary['technically_valid'] = count((array) ($job['technical_valid'] ?? array()));
        $summary['profiles_complete'] = 0;
        $summary['profiles_partial'] = 0;
        foreach ((array) ($summary['profile_stats'] ?? array()) as $profile_stat) {
            if (!empty($profile_stat['complete'])) { $summary['profiles_complete']++; }
            else { $summary['profiles_partial']++; }
        }
        $summary['blocked'] = absint($summary['hard_blocked'] ?? 0) + absint($summary['technical_blocked'] ?? 0) + absint($summary['manual_vetoed'] ?? 0);
        $summary['status'] = sanitize_key((string) $status);
        if ($stopped_reason !== '') { $summary['budget']['stopped_reason'] = sanitize_key((string) $stopped_reason); }
        // V5.17: Erst gezielt getItem nachprüfen, danach stale/ended fail-closed schalten.
        // Suchranking oder Pagination allein dürfen ein noch verfügbares Angebot nie beenden.
        // V5.21: Discovery und Bestandsabgleich sind echte getrennte Jobs.
        // Ein manueller Vollabruf darf nicht nach seinem Abschluss unbemerkt noch
        // bis zu 150 einzelne getItem-Requests anhängen und dadurch den Eindruck
        // eines endlosen eBay-Laufs erzeugen. Der Bestandsabgleich besitzt seinen
        // eigenen stündlichen Refresh-Cron und kann zusätzlich manuell gestartet werden.
        $summary['inventory_refresh'] = array('status'=>'separate_schedule');
        $summary['expired'] = array('status'=>'handled_by_separate_inventory_refresh');
        if ($status === 'completed') {
            // V6.20: selection/caps are already applied by the bounded worker
            // phase before finalization. Never perform a 5,000-row mutation loop
            // in the request that closes discovery.
            $selection = $this->ebay_selection_state_load();
            $summary['business_selection'] = is_array($selection['stats']['business'] ?? null) ? $selection['stats']['business'] : array();
            $summary['private_selection'] = is_array($selection['stats']['private'] ?? null) ? $selection['stats']['private'] : array();
            $summary['private_listings'] = absint($summary['private_selection']['active'] ?? 0);
            $summary['selection_duration_seconds'] = !empty($selection['completed_at']) && !empty($selection['started_at'])
                ? max(0, absint($selection['completed_at']) - absint($selection['started_at'])) : 0;
        }
        $summary['finished_at'] = time();
        $summary['duration_seconds'] = max(0, absint($summary['finished_at']) - absint($summary['started_at'] ?? $summary['finished_at']));
        $settings['last_sync'] = $summary;
        update_option(self::OPTION_NETWORK_EBAY, $settings, false);
        if ($status === 'completed' && sanitize_key((string)($job['scope'] ?? '')) === 'business_recovery') {
            update_option('ppar_ebay_business_restore_build_v1', (string)self::EBAY_RUNTIME_BUILD, false);
        }
        $job['status'] = in_array($status, array('failed','partial'), true) ? $status : 'completed';
        $job['worker_phase'] = 'finished';
        $job['finished_at'] = time();
        $this->ebay_sync_job_save($job);
        if (function_exists('wp_clear_scheduled_hook')) { wp_clear_scheduled_hook(self::EBAY_WORKER_HOOK); }
        return $summary;
    }

    private function ebay_sync_fail(&$job, $settings, $error) {
        $error = is_wp_error($error) ? $error : new WP_Error('ebay_worker_failed', sanitize_text_field((string) $error));
        $job['summary']['errors'][] = array('error'=>$error->get_error_message(),'code'=>$error->get_error_code());
        $job['summary']['technical_blocked'] = absint($job['summary']['technical_blocked'] ?? 0) + 1;
        $this->ebay_summary_reason_add($job['summary'], 'technical', $error, 'worker', 'SYSTEM', '');
        return $this->ebay_sync_finalize($job, $settings, 'failed', 'worker_error');
    }

    /**
     * V5.6.0 – Ein Worker bearbeitet höchstens eine Browse-Seite ODER ein
     * kleines Itempaket. Der Zustand wird vor/zwischen den Netzwerk- und
     * Materialisierungsschritten gespeichert. Wiederholungen sind über itemId
     * und die bestehenden Upserts idempotent.
     */
    public function run_ebay_sync_worker($manual_or_external = false) {
        $lock_key = 'ppar_ebay_sync_worker_lock_' . substr(hash('sha256', (string)self::EBAY_RUNTIME_BUILD), 0, 12);
        $use_legacy_lock = empty($this->ebay_canonical_worker_active);
        if ($use_legacy_lock && function_exists('get_transient') && get_transient($lock_key)) { return false; }
        if ($use_legacy_lock && function_exists('set_transient')) { set_transient($lock_key, 1, 45); }
        $reschedule = false;
        $job = array();
        try {
            $job = $this->ebay_sync_job_load();
            $settings = $this->ebay_settings();

            // The shared cron hook is only a transport fallback. If there is
            // no discovery owner, delegate every standalone selection tick to
            // the canonical selection worker instead of calling process_tick()
            // directly. This preserves the refresh mutation barrier, the
            // dedicated selection lock and the three-tick no-progress guard on
            // Cron, browser and manual transports alike.
            if (!$this->ebay_sync_job_is_open($job)) {
                $selection = $this->ebay_selection_state_load();
                if ($this->ebay_selection_state_is_open($selection)) {
                    return $this->run_ebay_selection_worker($manual_or_external);
                }
                return false;
            }
            $errors = $this->ebay_configuration_errors($settings);
            if ($errors) { return $this->ebay_sync_fail($job, $settings, new WP_Error('ebay_configuration_invalid', implode(' ', $errors))); }
            $author_id = $this->ebay_persist_listing_author_id($settings);
            if (is_wp_error($author_id)) { return $this->ebay_sync_fail($job, $settings, $author_id); }
            $this->ebay_sync_job_stamp_runtime($job, $author_id);
            $job['status'] = 'running';
            $job['last_worker_at'] = time();
            if (empty($job['last_progress_at'])) { $job['last_progress_at'] = absint($job['updated_at'] ?? time()); }
            $this->ebay_sync_job_save($job);

            // Dedicated bounded post-discovery selection phase. One tick does at
            // most 15 BUSINESS or 35 PRIVATE rows; no request can again mutate the
            // entire inventory and hit the gateway timeout.
            if (!empty($job['selection_pending'])) {
                $owner = 'sync:' . sanitize_text_field((string)($job['run_uuid'] ?? ''));
                $sync_selection_scope=$this->ebay_sync_job_selection_scope($job,$settings);
                if($sync_selection_scope===''){
                    return $this->ebay_sync_fail($job,$settings,new WP_Error('ebay_sync_scope_missing','Discovery-Job hat keinen gültigen Scope; fail-closed statt Fallback auf ALL.'));
                }
                $selection = $this->ebay_selection_state_load();
                if (!$this->ebay_selection_state_is_open($selection)
                    && sanitize_key((string)($selection['status'] ?? '')) !== 'complete') {
                    $selection = $this->ebay_selection_request('full_sync_finalize', $owner, true, $sync_selection_scope);
                }
                if ((string)($selection['owner'] ?? '') !== $owner) {
                    $selection = $this->ebay_selection_request('full_sync_finalize', $owner, true, $sync_selection_scope);
                }
                $job['worker_phase'] = sanitize_key((string)($selection['phase'] ?? 'selection'));
                $this->ebay_sync_job_save($job);
                $selection = $this->ebay_selection_process_tick($settings, $selection);
                $job['summary']['selection_progress'] = array(
                    'status'=>sanitize_key((string)($selection['status'] ?? '')),
                    'phase'=>sanitize_key((string)($selection['phase'] ?? '')),
                    'business_cursor'=>absint($selection['business_cursor'] ?? 0),
                    'private_cursor'=>absint($selection['private_cursor'] ?? 0),
                    'last_tick_ms'=>absint($selection['last_tick_ms'] ?? 0),
                );
                if (sanitize_key((string)($selection['status'] ?? '')) === 'complete') {
                    $job['selection_pending'] = 0;
                    $job['selection_complete'] = 1;
                    $job['worker_phase'] = 'selection_complete';
                    $this->ebay_sync_job_save($job);
                    return $this->ebay_sync_finalize($job, $settings, 'completed', '');
                }
                if (sanitize_key((string)($selection['status'] ?? '')) === 'failed') {
                    $reason = sanitize_text_field((string)($selection['failure_reason'] ?? 'Auswahl/Materialisierung konnte nicht vollständig verifiziert werden.'));
                    return $this->ebay_sync_fail($job, $settings, new WP_Error('ebay_selection_verification_failed', $reason));
                }
                $this->ebay_sync_touch_progress($job, 'selection');
                $this->ebay_sync_job_save($job);
                $reschedule = true;
                return true;
            }

            if ($this->ebay_sync_segment_expired($job)) {
                $this->ebay_sync_roll_segment($job);
                $this->ebay_sync_job_save($job);
                $reschedule = true;
                return true;
            }

            $summary =& $job['summary'];
            $max_requests = max(1, absint($settings['max_requests_per_run'] ?? 40));
            $max_pages = max(1, absint($settings['max_pages_per_profile'] ?? 4));
            $worker_budget = $manual_or_external ? 8 : max(10, min(30, absint($settings['run_time_budget_seconds'] ?? 20)));
            // Kleine Sicherheitsreserve, damit WordPress die Antwort noch sauber senden kann.
            $deadline = microtime(true) + max(8, $worker_budget - 2);
            $operations = 0;

            // V5.20: Das Zeitbudget wird vollständig genutzt. V5.18/5.19 kehrten
            // nach jedem Itempaket bzw. jedem Browse-Request zurück und erzeugten
            // dadurch hunderte voneinander abhängige HTTP-Ticks.
            while (microtime(true) < $deadline && $operations < 500) {
                $operations++;
                if ($this->ebay_sync_segment_expired($job)) {
                    $this->ebay_sync_roll_segment($job);
                    $this->ebay_sync_job_save($job);
                    $reschedule = true;
                    return true;
                }

                if (!empty($job['current_page']) && is_array($job['current_page'])) {
                    $page =& $job['current_page'];
                    $profile_key = (string) ($page['profile_key'] ?? '');
                    $profile_seller_type=strtoupper(sanitize_key((string)($job['profiles'][$profile_key]['seller_type']??'')));
                    if(!$this->ebay_route_enabled($profile_seller_type,$settings)){
                        if(isset($job['profiles'][$profile_key])){$job['profiles'][$profile_key]['active']=false;}
                        if(isset($summary['profile_stats'][$profile_key])){
                            $summary['profile_stats'][$profile_key]['complete']=true;
                            $summary['profile_stats'][$profile_key]['stopped_reason']='seller_route_disabled';
                        }
                        $summary['disabled_route_skipped_profiles']=absint($summary['disabled_route_skipped_profiles']??0)+1;
                        $job['current_page']=array();
                        $this->ebay_sync_advance_cursor($job,$profile_key);
                        $this->ebay_sync_touch_progress($job,'seller_route_disabled');
                        $this->ebay_sync_job_save($job);
                        unset($page);
                        continue;
                    }
                    $items = array_values((array) ($page['items'] ?? array()));
                    $index = absint($page['index'] ?? 0);
                    $since_save = 0;
                    $job['worker_phase'] = 'items';

                    while ($index < count($items) && microtime(true) < $deadline) {
                        $route_limit = absint($job['profiles'][$profile_key]['route_limit'] ?? 0);
                        if ($route_limit > 0 && absint($summary['profile_stats'][$profile_key]['accepted'] ?? 0) >= $route_limit) {
                            $index = count($items);
                            $job['current_page']['index'] = $index;
                            break;
                        }
                        $this->ebay_sync_process_item($job, $items[$index], $profile_key, $settings);
                        $index++;
                        $since_save++;
                        $job['current_page']['index'] = $index;
                        $this->ebay_sync_touch_progress($job, 'items');
                        if ($since_save >= 5) {
                            $this->ebay_sync_rebuild_review_summary($job);
                            $this->ebay_sync_job_save($job);
                            $since_save = 0;
                        }
                    }
                    $this->ebay_sync_rebuild_review_summary($job);
                    $this->ebay_sync_job_save($job);

                    if ($index < count($items)) {
                        $reschedule = true;
                        return true;
                    }

                    $page_next = trim((string) ($page['next'] ?? ''));
                    if (isset($job['profiles'][$profile_key])) {
                        $profile_page_limit = max(1, absint($job['profiles'][$profile_key]['page_limit'] ?? $max_pages));
                        if ($page_next === '' || absint($job['profiles'][$profile_key]['pages'] ?? 0) >= $profile_page_limit) {
                            $job['profiles'][$profile_key]['active'] = false;
                            $summary['profile_stats'][$profile_key]['complete'] = true;
                            if ($page_next !== '' && absint($job['profiles'][$profile_key]['pages'] ?? 0) >= $profile_page_limit) {
                                $summary['profile_stats'][$profile_key]['stopped_reason'] = 'profile_page_limit';
                            }
                        } else {
                            $job['profiles'][$profile_key]['next'] = $page_next;
                            $job['profiles'][$profile_key]['active'] = true;
                        }
                    }
                    $job['current_page'] = array();
                    $this->ebay_sync_advance_cursor($job, $profile_key);
                    $this->ebay_sync_touch_progress($job, 'page_done');
                    $this->ebay_sync_job_save($job);
                    unset($page);
                    continue;
                }

                // Erst pruefen, ob fachlich ueberhaupt noch ein Profil offen ist.
                // Sonst wuerde ein exakt mit dem letzten erlaubten Request fertig
                // gewordenes Profil faelschlich als PARTIAL/request_budget enden.
                $profile_key = $this->ebay_sync_active_profile_key($job);
                if ($profile_key === '') {
                    $completion = $this->ebay_sync_completion_state($job);
                    if ($completion['status'] === 'completed') {
                        if (!empty($this->ebay_canonical_worker_active)) {
                            return $this->ebay_sync_finalize($job, $settings, 'completed', '');
                        }
                        // Legacy compatibility only. Canonical V6.41 owns the
                        // downstream selection phase.
                        $owner = 'sync:' . sanitize_text_field((string)($job['run_uuid'] ?? ''));
                        $sync_selection_scope=$this->ebay_sync_job_selection_scope($job,$settings);
                        if($sync_selection_scope===''){
                            return $this->ebay_sync_fail($job,$settings,new WP_Error('ebay_sync_scope_missing','Discovery-Job hat keinen gültigen Scope; fail-closed statt Fallback auf ALL.'));
                        }
                        $this->ebay_selection_request('full_sync_finalize', $owner, true, $sync_selection_scope);
                        $job['selection_pending'] = 1;
                        $job['selection_complete'] = 0;
                        $this->ebay_sync_touch_progress($job, 'selection_prepare');
                        $this->ebay_sync_job_save($job);
                        $reschedule = true;
                        return true;
                    }
                    return $this->ebay_sync_finalize($job, $settings, $completion['status'], $completion['reason']);
                }
                if (absint($job['requests_in_batch'] ?? 0) >= $max_requests) {
                    // V6.17: 40 requests are a hard background-work-package cap,
                    // not a reason to abandon the remaining product catalog.
                    // Persist the exact job cursor and continue in a fresh worker
                    // request so one explicit full sync really covers all profiles.
                    $job['requests_in_batch'] = 0;
                    $summary['request_batches'] = absint($summary['request_batches'] ?? 1) + 1;
                    $job['worker_phase'] = 'request_batch_boundary';
                    $this->ebay_sync_touch_progress($job, 'request_batch_boundary');
                    $this->ebay_sync_job_save($job);
                    $reschedule = true;
                    return true;
                }
                $profile =& $job['profiles'][$profile_key];
                $profile_seller_type=strtoupper(sanitize_key((string)($profile['seller_type']??'')));
                if(!$this->ebay_route_enabled($profile_seller_type,$settings)){
                    $profile['active']=false;
                    $summary['profile_stats'][$profile_key]['complete']=true;
                    $summary['profile_stats'][$profile_key]['stopped_reason']='seller_route_disabled';
                    $summary['disabled_route_skipped_profiles']=absint($summary['disabled_route_skipped_profiles']??0)+1;
                    $this->ebay_sync_advance_cursor($job,$profile_key);
                    $this->ebay_sync_touch_progress($job,'seller_route_disabled');
                    $this->ebay_sync_job_save($job);
                    unset($profile);
                    continue;
                }
                $token = $this->ebay_access_token($settings);
                if (is_wp_error($token)) { return $this->ebay_sync_fail($job, $settings, $token); }

                $summary['requests']++;
                $job['requests_in_batch'] = absint($job['requests_in_batch'] ?? 0) + 1;
                $summary['profile_stats'][$profile_key]['requests']++;
                $job['worker_phase'] = 'fetch_inflight';
                $job['inflight_profile'] = $profile_key;
                $this->ebay_sync_job_save($job);

                $page_data = $this->ebay_search_page($profile['rule'], $profile['seller_type'], $settings, $token, (string) ($profile['next'] ?? ''));
                if (is_wp_error($page_data)) {
                    $summary['technical_blocked']++;
                    $summary['profile_stats'][$profile_key]['technical_blocked']++;
                    $this->ebay_summary_reason_add($summary, 'technical', $page_data, (string) $profile['rule']['id'], $profile['seller_type'], $profile_key);
                    $summary['errors'][] = array('rule'=>(string) $profile['rule']['id'],'seller_type'=>$profile['seller_type'],'error'=>$page_data->get_error_message(),'code'=>$page_data->get_error_code());
                    $summary['profile_stats'][$profile_key]['stopped_reason'] = 'request_error';
                    $profile['active'] = false;
                    unset($job['inflight_profile']);
                    $this->ebay_sync_advance_cursor($job, $profile_key);
                    $this->ebay_sync_touch_progress($job, 'request_error');
                    $this->ebay_sync_job_save($job);
                    unset($profile);
                    continue;
                }

                $items = array_values((array) ($page_data['items'] ?? array()));
                $summary['pages']++;
                $profile['pages'] = absint($profile['pages'] ?? 0) + 1;
                $summary['profile_stats'][$profile_key]['pages']++;
                $summary['received'] += count($items);
                $summary['profile_stats'][$profile_key]['received'] += count($items);
                foreach ($items as $raw) {
                    $id = substr(sanitize_text_field((string) (is_array($raw) ? ($raw['itemId'] ?? '') : '')), 0, 191);
                    if ($id !== '') { $job['unique_received'][$id] = true; }
                }
                $summary['received_unique'] = count($job['unique_received']);
                $job['current_page'] = array(
                    'profile_key'=>$profile_key,
                    'items'=>$items,
                    'index'=>0,
                    'next'=>trim((string) ($page_data['next'] ?? '')),
                    'loaded_at'=>time(),
                );
                unset($job['inflight_profile']);
                $this->ebay_sync_touch_progress($job, 'page_loaded');
                $this->ebay_sync_job_save($job);
                unset($profile);
                // Nicht zurückkehren: dieselbe Worker-Anfrage verarbeitet die eben
                // geladene Seite sofort weiter, solange Zeitbudget übrig ist.
                continue;
            }

            $reschedule = true;
            $this->ebay_sync_job_save($job);
            return true;
        } catch (Throwable $error) {
            $settings = $this->ebay_settings();
            if ($this->ebay_sync_job_is_open($job)) {
                return $this->ebay_sync_fail($job, $settings, new WP_Error('ebay_worker_runtime_error', $error->getMessage()));
            }
            return new WP_Error('ebay_worker_runtime_error', $error->getMessage());
        } finally {
            if ($use_legacy_lock && function_exists('delete_transient')) { delete_transient($lock_key); }
            if ($reschedule) {
                $fresh = $this->ebay_sync_job_load();
                if ($this->ebay_sync_job_is_open($fresh)) { $this->ebay_dispatch_worker($fresh); }
            }
        }
    }

    private function ebay_refresh_job_load() {
        if (method_exists($this, 'ebay_run_phase_state_load')) {
            $run = method_exists($this, 'ebay_run_load') ? $this->ebay_run_load() : array();
            if ((string)($run['schema'] ?? '') === '1.0') {
                $job = $this->ebay_run_phase_state_load('refresh');
                return is_array($job) ? $job : array();
            }
        }
        $job = get_option(self::OPTION_EBAY_REFRESH_JOB, array());
        return is_array($job) ? $job : array();
    }

    private function ebay_refresh_job_save($job) {
        $job = is_array($job) ? $job : array();
        if ((string)($job['schema'] ?? '') === '1.0' && (string)($job['engine'] ?? '') === 'targeted-getitem-refresh') {
            $job['state_contract'] = 'refresh-v1';
            $job['build'] = self::EBAY_RUNTIME_BUILD;
            if (isset($job['summary']) && is_array($job['summary'])) {
                $job['summary']['state_contract'] = 'refresh-v1';
                $job['summary']['build'] = self::EBAY_RUNTIME_BUILD;
            }
        }
        $job['updated_at'] = time();
        if (method_exists($this, 'ebay_run_load') && (string)(($this->ebay_run_load())['schema'] ?? '') === '1.0') {
            $this->ebay_run_phase_state_save('refresh', $job);
        } else {
            update_option(self::OPTION_EBAY_REFRESH_JOB, $job, false);
        }
        return $job;
    }

    private function ebay_refresh_job_runtime_compatible($job) {
        if (!is_array($job)) { return false; }
        $build = (string) ($job['build'] ?? '');
        $schema = (string) ($job['schema'] ?? '');
        $engine = (string) ($job['engine'] ?? '');
        $contract = (string)($job['state_contract'] ?? '');
        if ($schema !== '1.0' || $engine !== 'targeted-getitem-refresh') { return false; }
        return $contract === 'refresh-v1' || $this->ebay_known_patch_state_build($build);
    }

    private function ebay_refresh_job_is_open($job) {
        return $this->ebay_refresh_job_runtime_compatible($job)
            && in_array(sanitize_key((string) ($job['status'] ?? '')), array('queued','running'), true);
    }

    /** Resume every bounded partial that is safe to continue on the SAME
     * durable refresh identity. Segment timeouts preserve the current phase;
     * manual local/asset ceilings extend only their bounded phase budget. */
    private function ebay_refresh_job_is_resumable_partial($job) {
        if (!$this->ebay_refresh_job_runtime_compatible($job) || sanitize_key((string)($job['status'] ?? '')) !== 'partial') { return false; }
        $reason = sanitize_key((string)($job['summary']['stopped_reason'] ?? ''));
        if ($reason === 'segment_time_budget') { return true; }
        if (empty($job['manual'])) { return false; }
        return in_array($reason, array('local_reconcile_limit','asset_verification_limit'), true);
    }

    private function ebay_refresh_resume_partial_job($job) {
        $job = is_array($job) ? $job : array();
        if (!$this->ebay_refresh_job_is_resumable_partial($job)) { return array(); }
        if (!isset($job['summary']) || !is_array($job['summary'])) { $job['summary'] = array(); }
        $summary =& $job['summary'];
        $reason = sanitize_key((string)($summary['stopped_reason'] ?? ''));
        $segments = max(1, absint($summary['segments'] ?? 1));
        if ($segments >= 20) {
            $job['status'] = 'failed';
            $job['finished_at'] = time();
            $summary['status'] = 'failed';
            $summary['finished_at'] = time();
            $summary['failure_reason'] = 'partial_segment_hard_limit';
            $summary['stopped_reason'] = 'partial_segment_hard_limit';
            return $this->ebay_refresh_job_save($job);
        }
        $job['status'] = 'queued';
        $job['segment_started_at'] = time();
        $job['finished_at'] = 0;
        $job['last_worker_at'] = 0;
        $job['last_progress_at'] = time();
        $summary['status'] = 'queued';
        $summary['finished_at'] = 0;
        $summary['segments'] = $segments + 1;
        if ($reason === 'local_reconcile_limit') {
            $per = max(1, absint($summary['max_local_reconcile_rows_per_segment'] ?? $summary['max_local_reconcile_rows'] ?? 2000));
            $summary['max_local_reconcile_rows_per_segment'] = $per;
            $summary['max_local_reconcile_rows'] = min(40000, max(absint($summary['max_local_reconcile_rows'] ?? 0), absint($summary['maintenance']['scanned'] ?? 0)) + $per);
            $summary['local_segments'] = max(1, absint($summary['local_segments'] ?? 1)) + 1;
            if (!isset($summary['maintenance']) || !is_array($summary['maintenance'])) { $summary['maintenance'] = array(); }
            $summary['maintenance']['completed'] = 0;
            $summary['maintenance']['deferred'] = 0;
            $summary['phase'] = 'local_reconciliation';
        } elseif ($reason === 'asset_verification_limit') {
            $per = max(1, absint($summary['max_asset_verifications_per_segment'] ?? $summary['max_asset_verifications'] ?? 50));
            $summary['max_asset_verifications_per_segment'] = $per;
            $summary['max_asset_verifications'] = min(2000, max(absint($summary['max_asset_verifications'] ?? 0), absint($summary['asset_verification']['processed'] ?? 0)) + $per);
            $summary['asset_segments'] = max(1, absint($summary['asset_segments'] ?? 1)) + 1;
            if (!isset($summary['asset_verification']) || !is_array($summary['asset_verification'])) { $summary['asset_verification'] = array(); }
            $summary['asset_verification']['completed'] = 0;
            $summary['asset_verification']['deferred'] = 0;
            $summary['phase'] = 'asset_verification';
        }
        $summary['stopped_reason'] = '';
        return $this->ebay_refresh_job_save($job);
    }

    /** A bounded manual remote cap owes canonical selection but must never be
     * converted into a fresh last_id=0 refresh merely because a patch changed. */
    private function ebay_refresh_job_is_bounded_manual_partial($job) {
        if (!$this->ebay_refresh_job_runtime_compatible($job) || empty($job['manual'])) { return false; }
        if (sanitize_key((string)($job['status'] ?? '')) !== 'partial') { return false; }
        if (sanitize_key((string)($job['summary']['stopped_reason'] ?? '')) !== 'max_checks_limit') { return false; }
        return $this->ebay_refresh_manual_incomplete_reason($job) === '';
    }

    private function ebay_refresh_bounded_selection_complete($job) {
        $selection=is_array($job['summary']['selection']??null)?$job['summary']['selection']:array();
        return sanitize_key((string)($selection['status']??''))==='complete' && absint($selection['completed_at']??0)>0;
    }

    /** Later invocation continues only the remote cursor of the SAME refresh.
     * Each segment remains <=2,000 checks; local reconciliation is not repeated. */
    private function ebay_refresh_resume_bounded_remote_job($job) {
        $job=is_array($job)?$job:array();
        if(!$this->ebay_refresh_job_is_bounded_manual_partial($job)){return array();}
        if(empty($this->ebay_canonical_worker_active) && !$this->ebay_refresh_bounded_selection_complete($job)){return array();}
        $checked=absint($job['summary']['checked']??0);
        $per_segment=absint($job['summary']['max_checks_per_segment']??0);
        if($per_segment<=0){$per_segment=max(1,min(2000,absint($job['summary']['max_checks']??2000)));}
        $segments=max(1,absint($job['summary']['remote_segments']??1));
        if($segments>=20){
            $job['status']='failed';$job['finished_at']=time();$job['summary']['status']='failed';
            $job['summary']['failure_reason']='remote_segment_hard_limit';$job['summary']['stopped_reason']='remote_segment_hard_limit';
            $this->ebay_refresh_job_save($job);return array();
        }
        $job['status']='queued';$job['finished_at']=0;$job['segment_started_at']=time();$job['last_worker_at']=0;$job['last_progress_at']=time();
        $job['summary']['status']='queued';$job['summary']['finished_at']=0;$job['summary']['stopped_reason']='';$job['summary']['phase']='source_refresh';
        $job['summary']['remote_segments']=$segments+1;$job['summary']['max_checks_per_segment']=$per_segment;$job['summary']['max_checks']=$checked+$per_segment;
        if(isset($job['summary']['selection'])){
            if(!isset($job['summary']['selection_history'])||!is_array($job['summary']['selection_history'])){$job['summary']['selection_history']=array();}
            $job['summary']['selection_history'][]=$job['summary']['selection'];
            if(count($job['summary']['selection_history'])>20){$job['summary']['selection_history']=array_slice($job['summary']['selection_history'],-20);}
            unset($job['summary']['selection']);
        }
        return $this->ebay_refresh_job_save($job);
    }

    /** Idempotent handoff from a bounded manual refresh to the one canonical
     * selector. It never resets refresh identity/cursor and never creates a
     * competing selection owner. */
    private function ebay_refresh_ensure_manual_selection_handoff(&$job,$settings=null,$reason='inventory_refresh_remote_cap') {
        $job=is_array($job)?$job:array();$settings=is_array($settings)?$settings:$this->ebay_settings();
        $run_uuid=sanitize_text_field((string)($job['run_uuid']??''));
        if($run_uuid===''){return new WP_Error('ebay_refresh_run_uuid_missing','Bestandsabgleich kann ohne stabile Lauf-ID nicht an die Auswahl übergeben werden.');}
        $scope=$this->ebay_selection_scope_for_enabled_routes('all',$settings);
        if($scope===''){$job['summary']['selection']=array('status'=>'not_required','scope'=>'none','queued'=>0);$this->ebay_refresh_job_save($job);return array('status'=>'not_required','selection_scope'=>'none');}
        $owner='refresh:'.$run_uuid;$current=$this->ebay_selection_state_load();
        if($this->ebay_selection_state_is_open($current)){
            if(hash_equals($owner,sanitize_text_field((string)($current['owner']??'')))){$job['summary']['selection']=array('status'=>sanitize_key((string)($current['status']??'pending')),'scope'=>$scope,'queued'=>1,'reason'=>sanitize_key((string)$reason));$this->ebay_refresh_job_save($job);return $current;}
            return new WP_Error('ebay_refresh_competing_selection','Eine andere Bestandsauswahl besitzt bereits den kanonischen Selection-Worker.');
        }
        $selection=$this->ebay_selection_request($reason,$owner,false,$scope);if(is_wp_error($selection)){return $selection;}
        $job['summary']['selection']=array('status'=>sanitize_key((string)($selection['status']??'pending')),'scope'=>$scope,'queued'=>1,'reason'=>sanitize_key((string)$reason));
        if(empty($job['summary']['finished_at'])){$job['summary']['finished_at']=time();}
        $settings['last_refresh']=$job['summary'];update_option(self::OPTION_NETWORK_EBAY,$settings,false);$this->ebay_refresh_job_save($job);
        return $selection;
    }

    private function ebay_refresh_schedule_worker_fallback($delay = 12) {
        if (method_exists($this, 'ebay_run_load') && (string)(($this->ebay_run_load())['schema'] ?? '') === '1.0') { return true; }
        if (!function_exists('wp_next_scheduled') || !function_exists('wp_schedule_single_event')) { return; }
        if (!wp_next_scheduled(self::EBAY_WORKER_HOOK)) {
            wp_schedule_single_event(time() + max(10, absint($delay)), self::EBAY_WORKER_HOOK);
        }
    }

    private function ebay_refresh_dispatch_worker($job = null) {
        $job = is_array($job) ? $job : $this->ebay_refresh_job_load();
        if (!$this->ebay_refresh_job_is_open($job)) { return false; }
        // Same single-owner transport as discovery: no plugin self-HTTP loopback.
        $this->ebay_refresh_schedule_worker_fallback(12);
        return true;
    }

    /** V5.21 – auch der getrennte getItem-Bestandsjob darf nie endlos offen bleiben. */
    private function ebay_refresh_segment_limit_seconds($job = array()) {
        $configured = absint($job['summary']['segment_limit_seconds'] ?? 0);
        if ($configured > 0) { return max(30, min(2700, $configured)); }
        return !empty($job['manual']) ? 30 : 2700;
    }

    private function ebay_refresh_segment_expired($job) {
        if (!$this->ebay_refresh_job_is_open($job)) { return false; }
        $started = absint($job['segment_started_at'] ?? ($job['created_at'] ?? 0));
        return $started > 0 && (time() - $started) >= $this->ebay_refresh_segment_limit_seconds($job);
    }

    /** Bounded durable limits. Manual reconcile is a real full portal pass, not the historical 25/0/3 diagnostic sample. */
    private function ebay_refresh_job_limits($manual, $settings = null) {
        $settings = is_array($settings) ? $settings : $this->ebay_settings();
        if (!empty($manual)) {
            return array(
                'max_local_reconcile_rows'=>2000,
                // Preserve the proven V6.18 ownership boundary: a manual
                // inventory reconcile must never drain the global remote-image
                // backlog. Verified eBay BUSINESS product identity may use the
                // existing provisional remote-asset contract; the dedicated
                // asset verifier revalidates those images independently.
                'max_asset_verifications'=>0,
                'max_checks'=>2000,
                'segment_limit_seconds'=>2700,
            );
        }
        return array(
            'max_local_reconcile_rows'=>500,
            'max_asset_verifications'=>50,
            'max_checks'=>max(1200, min(2000, absint($settings['inventory_refresh_max_per_run'] ?? 1200))),
            'segment_limit_seconds'=>2700,
        );
    }

    private function ebay_start_inventory_refresh_job($manual = false, $skip_reconcile = false) {
        $settings = $this->ebay_settings();
        if (empty($settings['enabled']) && !$manual) { return array('status'=>'disabled'); }
        if (empty($settings['inventory_refresh_enabled']) && !$manual) { return array('status'=>'disabled'); }
        $errors = $this->ebay_configuration_errors($settings);
        if ($errors) { return new WP_Error('ebay_refresh_configuration_invalid', implode(' ', $errors)); }

        $sync_job = $this->ebay_sync_job_load();
        if ($this->ebay_sync_job_is_open($sync_job)) {
            return $manual
                ? new WP_Error('ebay_refresh_discovery_running', 'Der eBay-Discovery-Abruf läuft bereits. Der Bestandsabgleich startet erst danach.')
                : array('status'=>'deferred_discovery_running');
        }
        // Continuity first: an existing compatible refresh owns its cursor
        // across patch updates. Never synthesize a fresh last_id=0 run on top of
        // open/resumable/bounded durable work.
        $existing = $this->ebay_refresh_job_load();
        if ($this->ebay_refresh_job_is_open($existing)) {
            $existing=$this->ebay_refresh_job_save($existing);
            $this->ebay_refresh_dispatch_worker($existing);
            return array('status'=>'already_running','run_uuid'=>(string)($existing['run_uuid']??''),'summary'=>(array)($existing['summary']??array()));
        }
        if ($this->ebay_refresh_job_is_resumable_partial($existing)) {
            $resumed=$this->ebay_refresh_resume_partial_job($existing);
            if($resumed){$this->ebay_refresh_dispatch_worker($resumed);return array('status'=>'resumed','run_uuid'=>(string)($resumed['run_uuid']??''),'summary'=>(array)($resumed['summary']??array()));}
        }
        if($this->ebay_refresh_job_is_bounded_manual_partial($existing)){
            $existing=$this->ebay_refresh_job_save($existing);
            if($this->ebay_refresh_bounded_selection_complete($existing)){
                $resumed=$this->ebay_refresh_resume_bounded_remote_job($existing);
                if($resumed){$this->ebay_refresh_dispatch_worker($resumed);return array('status'=>'resumed_remote_segment','run_uuid'=>(string)($resumed['run_uuid']??''),'summary'=>(array)($resumed['summary']??array()));}
                return new WP_Error('ebay_refresh_remote_segment_limit','Bestandsabgleich hat die harte Segmentgrenze erreicht und wurde fail-closed beendet.');
            }
            $selection=$this->ebay_refresh_ensure_manual_selection_handoff($existing,$settings,'inventory_refresh_remote_cap');
            if(is_wp_error($selection)){return $selection;}
            return array('status'=>'selection_handoff','run_uuid'=>(string)($existing['run_uuid']??''),'summary'=>(array)($existing['summary']??array()));
        }
        $selection_guard=$this->ebay_selection_state_load();
        if($this->ebay_selection_state_is_open($selection_guard)){
            return $manual?new WP_Error('ebay_refresh_selection_running','Eine Bestandsauswahl läuft bereits. Der Bestandsabgleich startet erst nach deren Abschluss.'):array('status'=>'deferred_selection_running');
        }
        $canonical_run = method_exists($this, 'ebay_run_load') ? $this->ebay_run_load() : array();
        $run_uuid = !empty($this->ebay_canonical_worker_active) && !empty($canonical_run['run_uuid']) ? sanitize_text_field((string)$canonical_run['run_uuid']) : (function_exists('wp_generate_uuid4') ? wp_generate_uuid4() : substr(hash('sha256', microtime(true) . '|refresh|' . mt_rand()), 0, 36));
        $worker_token = function_exists('wp_generate_password') ? wp_generate_password(48, false, false) : hash('sha256', $run_uuid . '|refresh|' . microtime(true) . '|' . mt_rand());
        $now = time();
        $limits = $this->ebay_refresh_job_limits($manual, $settings);
        // Kein globaler Maintenance-Reset: der manuelle Abgleich setzt nur an
        // faelligen/fehlerhaften Datensaetzen an und bleibt hart begrenzt.
        $job = array(
            'schema'=>'1.0','engine'=>'targeted-getitem-refresh','build'=>self::EBAY_RUNTIME_BUILD,
            'status'=>'queued','run_uuid'=>$run_uuid,'worker_token'=>$worker_token,'manual'=>!empty($manual),
            'created_at'=>$now,'segment_started_at'=>$now,'updated_at'=>$now,'finished_at'=>0,'last_worker_at'=>0,'last_id'=>0,
            // Alles, was innerhalb der nächsten 30 Minuten aus der 6h-Frische fallen würde, wird jetzt direkt geprüft.
            'due_before'=>$now + 30 * MINUTE_IN_SECONDS,
            'summary'=>array(
                'status'=>'queued','phase'=>$skip_reconcile ? 'source_refresh' : 'local_reconciliation','reconcile_contracts'=>$skip_reconcile ? 0 : 1,'force_business_reconcile'=>0,'started_at'=>$now,'finished_at'=>0,'checked'=>0,'requests'=>0,'available'=>0,
                'updated'=>0,'revived'=>0,'ended'=>0,'excluded'=>0,'reviewed'=>0,'transient_errors'=>0,'technical_errors'=>0,'errors'=>array(),
                'maintenance'=>array('scanned'=>0,'ready_private'=>0,'ready_business'=>0,'review'=>0,'blocked'=>0,'errors'=>0,'completed'=>0,'deferred'=>0),
                'asset_verification'=>array('processed'=>0,'verified'=>0,'blocked'=>0,'remaining'=>0,'completed'=>0,'deferred'=>0),
                'max_local_reconcile_rows'=>absint($limits['max_local_reconcile_rows'] ?? 500),
                'max_local_reconcile_rows_per_segment'=>absint($limits['max_local_reconcile_rows'] ?? 500),'local_segments'=>1,
                'max_asset_verifications'=>absint($limits['max_asset_verifications'] ?? 50),
                'max_asset_verifications_per_segment'=>absint($limits['max_asset_verifications'] ?? 50),'asset_segments'=>1,
                'max_checks_per_segment'=>absint($limits['max_checks'] ?? 1200),
                'max_checks'=>absint($limits['max_checks'] ?? 1200),'remote_segments'=>1,
                'segment_limit_seconds'=>absint($limits['segment_limit_seconds'] ?? 2700),'stopped_reason'=>'',
            ),
        );
        $this->ebay_refresh_job_save($job);
        $this->ebay_refresh_dispatch_worker($job);
        return array('status'=>'queued','run_uuid'=>$run_uuid,'summary'=>$job['summary']);
    }

    public function run_ebay_inventory_refresh($manual = false) {
        return $this->ebay_run_start($manual, 'refresh');
    }

    private function ebay_refresh_due_rows($job, $limit = 10, $settings = null) {
        global $wpdb;
        $settings=is_array($settings)?$settings:$this->ebay_settings();
        $table = $this->ebay_items_table();
        $last_id = absint($job['last_id'] ?? 0);
        $due_before = absint($job['due_before'] ?? time());
        $now = time();
        $retry_before = $now - 15 * MINUTE_IN_SECONDS;
        $limit = max(1, min(20, absint($limit)));
        $route_sql=$this->ebay_refresh_enabled_route_sql($settings,'e');
        return (array) $wpdb->get_results($wpdb->prepare(
            "SELECT e.* FROM {$table} e WHERE e.id>%d AND {$route_sql} AND COALESCE(e.source_state,'available')<>'ended' AND COALESCE(e.policy_state,'allowed')<>'blocked' AND COALESCE(e.status,'active') NOT IN ('blocked_manual','blocked_content') AND ((e.item_end_at>0 AND e.item_end_at<=%d) OR ((e.fresh_until=0 OR e.fresh_until<=%d) AND (COALESCE(e.source_checked_at,0)=0 OR e.source_checked_at<=%d))) ORDER BY e.id ASC LIMIT %d",
            $last_id, $now, $due_before, $retry_before, $limit
        ), ARRAY_A);
    }

    private function ebay_refresh_has_more($job, $settings = null) {
        global $wpdb;
        $settings=is_array($settings)?$settings:$this->ebay_settings();
        $table = $this->ebay_items_table();
        $last_id = absint($job['last_id'] ?? 0);
        $due_before = absint($job['due_before'] ?? time());
        $now = time();
        $retry_before = $now - 15 * MINUTE_IN_SECONDS;
        $route_sql=$this->ebay_refresh_enabled_route_sql($settings,'e');
        $id = $wpdb->get_var($wpdb->prepare(
            "SELECT e.id FROM {$table} e WHERE e.id>%d AND {$route_sql} AND COALESCE(e.source_state,'available')<>'ended' AND COALESCE(e.policy_state,'allowed')<>'blocked' AND COALESCE(e.status,'active') NOT IN ('blocked_manual','blocked_content') AND ((e.item_end_at>0 AND e.item_end_at<=%d) OR ((e.fresh_until=0 OR e.fresh_until<=%d) AND (COALESCE(e.source_checked_at,0)=0 OR e.source_checked_at<=%d))) ORDER BY e.id ASC LIMIT 1",
            $last_id, $now, $due_before, $retry_before
        ));
        return absint($id) > 0;
    }

    private function ebay_refresh_reuse_classification($row, &$item) {
        $payload = json_decode((string) ($row['source_payload'] ?? ''), true);
        $classification = is_array($payload) && is_array($payload['portal_classification'] ?? null) ? $payload['portal_classification'] : array();
        if ($classification) { $item['portal_classification'] = $classification; }
        return $classification;
    }

    /** Promote one already-qualified BUSINESS reserve after a public winner ends. */
    private function ebay_business_promote_ended_replacement($ended_row, $settings = null) {
        $ended_row=is_array($ended_row)?$ended_row:array();
        if(sanitize_key((string)($ended_row['output_state']??''))!=='creative_ready'){
            return array('promoted'=>0,'status'=>'not_public');
        }
        $payload=json_decode((string)($ended_row['source_payload']??''),true);$payload=is_array($payload)?$payload:array();
        $class=is_array($payload['portal_classification']??null)?$payload['portal_classification']:array();
        $concept=sanitize_key((string)($class['product_concept_id']??''));
        if($concept===''){return array('promoted'=>0,'status'=>'concept_missing');}
        $settings=is_array($settings)?$this->ebay_normalize_settings($settings,true):$this->ebay_settings();
        global $wpdb;$table=$this->ebay_items_table();
        if(!is_object($wpdb)||!method_exists($wpdb,'get_results')){return array('promoted'=>0,'status'=>'storage_unavailable');}
        // Reserve rows were already selected by the full quality planner. Candidates
        // are only a fallback when no reserve exists. Never scan active winners.
        $rows=(array)$wpdb->get_results($wpdb->prepare(
            "SELECT * FROM {$table} WHERE seller_account_type='BUSINESS' AND rule_id=%s AND source_state='available' AND policy_state='allowed' AND route_state IN ('ready','review_last_good') AND fresh_until>%d AND (item_end_at=0 OR item_end_at>%d) AND output_state IN ('reserve','candidate','candidate_overflow') ORDER BY last_seen DESC,id DESC LIMIT 30",
            $concept, time(), time()
        ),ARRAY_A);
        $reserve=array();$fallback=array();$now=time();
        foreach($rows as $row){
            if((string)($row['item_id']??'')===(string)($ended_row['item_id']??'')){continue;}
            $role=sanitize_key((string)($row['output_state']??''));
            if(!in_array($role,array('reserve','candidate','candidate_overflow'),true)){continue;}
            if(sanitize_key((string)($row['source_state']??''))!=='available'||sanitize_key((string)($row['policy_state']??''))!=='allowed'){continue;}
            $end=absint($row['item_end_at']??0);if($end>0&&$end<=$now){continue;}
            $item=$this->ebay_business_source_row_item($row,$settings);if(is_wp_error($item)){continue;}
            $candidate_class=(array)($item['portal_classification']??array());
            if(sanitize_key((string)($candidate_class['product_concept_id']??''))!==$concept){continue;}
            $rule=$this->ebay_rule_by_id((string)($row['rule_id']??''),$settings);
            $quality=$this->ebay_business_quality_assess($item,$candidate_class,$rule,$settings,0.0);if(is_wp_error($quality)){continue;}
            $candidate=array('row'=>$row,'item'=>$this->ebay_business_item_with_quality($item,$quality),'classification'=>$candidate_class,'rule'=>$rule,'quality'=>$quality);
            if(sanitize_key((string)($row['output_state']??''))==='reserve'){$reserve[]=$candidate;}else{$fallback[]=$candidate;}
        }
        if($reserve){$this->ebay_business_candidate_sort($reserve);}if($fallback){$this->ebay_business_candidate_sort($fallback);}
        $candidates=array_merge($reserve,$fallback);
        foreach($candidates as $candidate){
            $row=$candidate['row'];$item_id=(string)($row['item_id']??'');
            $this->ebay_business_persist_quality_on_source_row($row,$candidate['quality'],'active_selected',3);
            $candidate['item']['business_selection']=array('role'=>'active_selected','rank'=>3);
            $result=$this->ebay_route_business($row,$candidate['item'],$candidate['rule'],'ended-replacement-'.time(),$candidate['classification']);
            if(!is_wp_error($result)){
                return array('promoted'=>1,'status'=>'promoted','item_id'=>$item_id,'concept_id'=>$concept,'from'=>sanitize_key((string)($row['output_state']??'')));
            }
        }
        return array('promoted'=>0,'status'=>'no_qualified_replacement','concept_id'=>$concept);
    }

    /** Promote one same-leaf PRIVATE reserve after a published listing ends. */
    private function ebay_private_promote_ended_replacement($ended_row, $settings = null) {
        $ended_row=is_array($ended_row)?$ended_row:array();
        $listing_id=absint($ended_row['listing_post_id']??0);
        $was_public=sanitize_key((string)($ended_row['output_state']??''))==='listing_published';
        if($listing_id>0&&function_exists('get_post_status')){$was_public=$was_public||((string)get_post_status($listing_id)==='publish');}
        if(!$was_public){return array('promoted'=>0,'status'=>'not_public');}
        $target=absint($ended_row['target_term_id']??0);if($target<=0){return array('promoted'=>0,'status'=>'target_missing');}
        $settings=is_array($settings)?$this->ebay_normalize_settings($settings,true):$this->ebay_settings();
        global $wpdb;$table=$this->ebay_items_table();if(!is_object($wpdb)||!method_exists($wpdb,'get_results')){return array('promoted'=>0,'status'=>'storage_unavailable');}
        $rows=(array)$wpdb->get_results($wpdb->prepare(
            "SELECT * FROM {$table} WHERE seller_account_type='INDIVIDUAL' AND source_state='available' AND policy_state='allowed' AND route_state='ready' AND target_term_id=%d AND output_state='listing_reserved' ORDER BY last_seen DESC,id DESC LIMIT 100",
            $target
        ),ARRAY_A);
        $eligible=array();$now=time();
        foreach($rows as $row){
            if(absint($row['target_term_id']??0)!==$target){continue;}
            if(sanitize_key((string)($row['output_state']??''))!=='listing_reserved'){continue;}
            if(sanitize_key((string)($row['source_state']??''))!=='available'||sanitize_key((string)($row['policy_state']??''))!=='allowed'||sanitize_key((string)($row['route_state']??''))!=='ready'){continue;}
            $end=absint($row['item_end_at']??0);if($end>0&&$end<=$now){continue;}if((string)($row['item_id']??'')===(string)($ended_row['item_id']??'')){continue;}$eligible[]=$row;
        }
        $selected=$this->ebay_private_select_rows_for_capacity($eligible,$settings);
        foreach($selected as $row){
            $payload=json_decode((string)($row['source_payload']??''),true);$payload=is_array($payload)?$payload:array();$raw=is_array($payload['raw']??null)?$payload['raw']:array();
            if(!$raw){continue;}$item=$this->ebay_accept_item($raw,'INDIVIDUAL',$settings);if(is_wp_error($item)){continue;}
            $item['portal_classification']=is_array($payload['portal_classification']??null)?$payload['portal_classification']:array();
            $result=$this->ebay_materialize_private_listing($row,$item,$target,$settings);
            if(!is_wp_error($result)){return array('promoted'=>1,'status'=>'promoted','item_id'=>(string)($row['item_id']??''),'target_term_id'=>$target);}
        }
        return array('promoted'=>0,'status'=>'no_qualified_replacement','target_term_id'=>$target);
    }

    private function ebay_refresh_mark_ended($row, $reason, $settings = null) {
        $reason = sanitize_text_field((string) $reason);
        if ($reason === '') { $reason = 'eBay-Angebot ist nicht mehr verfügbar.'; }
        // Decide replacement eligibility before tombstoning mutates source state.
        $seller_type=strtoupper(sanitize_key((string)($row['seller_account_type']??'')));
        $replacement=$seller_type==='BUSINESS'
            ? $this->ebay_business_promote_ended_replacement($row,$settings)
            : ($seller_type==='INDIVIDUAL' ? $this->ebay_private_promote_ended_replacement($row,$settings) : array('promoted'=>0,'status'=>'unsupported_seller_type'));
        $purged=$this->ebay_purge_item_content($row, 'purged_ended', $reason);
        $purged['replacement']=$replacement;
        return $purged;
    }

    private function ebay_refresh_process_row(&$job, $row, $settings, $token) {
        $summary =& $job['summary'];
        $row = is_array($row) ? $row : array();
        $row_seller_type=strtoupper(sanitize_key((string)($row['seller_account_type']??'')));
        $job['last_id'] = max(absint($job['last_id'] ?? 0), absint($row['id'] ?? 0));
        if(!$this->ebay_route_enabled($row_seller_type,$settings)){
            $summary['excluded']=absint($summary['excluded']??0)+1;
            $summary['disabled_route_skipped']=absint($summary['disabled_route_skipped']??0)+1;
            return;
        }
        $summary['checked']++;
        if($row_seller_type==='INDIVIDUAL'){$summary['private_touched']=absint($summary['private_touched']??0)+1;}
        elseif($row_seller_type==='BUSINESS'){$summary['business_touched']=absint($summary['business_touched']??0)+1;}
        $now = time();
        if (absint($row['item_end_at'] ?? 0) > 0 && absint($row['item_end_at']) <= $now) {
            $ended_result=$this->ebay_refresh_mark_ended($row, 'eBay-Angebotsende erreicht; öffentliche Ausgabe deaktiviert.', $settings);
            $summary['ended']++;
            if(!empty($ended_result['replacement']['promoted'])){$summary['replaced']=absint($summary['replaced']??0)+1;}
            return;
        }
        $summary['requests']++;
        $fresh = $this->ebay_fetch_item_for_refresh($row, $settings, $token);
        if (is_wp_error($fresh)) {
            $code = sanitize_key((string) $fresh->get_error_code());
            if ($code === 'ebay_refresh_transient_http' || $code === 'ebay_refresh_transport') { $summary['transient_errors']++; }
            else { $summary['technical_errors']++; }
            // A failed source attempt must not deactivate or extend freshness, but
            // it is timestamped so the next scheduled segment can move on to the
            // remaining inventory instead of hammering/starving on the same rows.
            global $wpdb;
            $attempt = array('source_checked_at'=>$now,'updated_at'=>$now);
            $wpdb->update($this->ebay_items_table(), $attempt, array('id'=>absint($row['id'] ?? 0)), $this->ebay_db_formats($attempt), array('%d'));
            if (count($summary['errors']) < 30) { $summary['errors'][] = array('item_id'=>(string)($row['item_id'] ?? ''),'code'=>$code,'error'=>$fresh->get_error_message()); }
            return;
        }
        if ((string) ($fresh['state'] ?? '') === 'ended') {
            $reason_code = sanitize_key((string) ($fresh['reason'] ?? 'unavailable'));
            $reason = $reason_code === 'out_of_stock' ? 'eBay meldet OUT_OF_STOCK; öffentliche Ausgabe deaktiviert.' : ($reason_code === 'item_end_date' ? 'eBay meldet ein abgelaufenes Angebotsende; öffentliche Ausgabe deaktiviert.' : 'eBay-Angebot über getItem nicht mehr verfügbar; öffentliche Ausgabe deaktiviert.');
            $ended_result=$this->ebay_refresh_mark_ended($row, $reason, $settings);
            $summary['ended']++;
            if(!empty($ended_result['replacement']['promoted'])){$summary['replaced']=absint($summary['replaced']??0)+1;}
            return;
        }
        $raw = is_array($fresh['raw'] ?? null) ? $fresh['raw'] : array();
        $seller_type = strtoupper(sanitize_key((string) ($row['seller_account_type'] ?? '')));
        $item = $this->ebay_accept_item($raw, $seller_type, $settings);
        if (is_wp_error($item)) {
            $code = sanitize_key((string) $item->get_error_code());
            if ($code === 'ebay_toy_item_blocked') {
                $this->ebay_quarantine_filtered_row($row, $item->get_error_message());
                $summary['excluded'] = absint($summary['excluded'] ?? 0) + 1;
                return;
            }
            $summary['technical_errors']++;
            if (count($summary['errors']) < 30) { $summary['errors'][] = array('item_id'=>(string)($row['item_id'] ?? ''),'code'=>$item->get_error_code(),'error'=>$item->get_error_message()); }
            return;
        }
        $rule = $this->ebay_rule_by_id((string) ($row['rule_id'] ?? ''), $settings);
        $target_term_id = 0;
        if ($seller_type === 'BUSINESS') {
            // Every successful real getItem refresh reclassifies BUSINESS from the
            // current source facts. Historical target assignments are never trusted.
            $classification = $this->ebay_business_classify_portal_item_strict($item, $rule);
            if (is_wp_error($classification)) {
                $this->ebay_business_hold_for_review($row, $item, $rule, $classification, $settings);
                $summary['excluded'] = absint($summary['excluded'] ?? 0) + 1;
                $summary['reviewed'] = absint($summary['reviewed'] ?? 0) + 1;
                return;
            }
            $item['portal_classification'] = $classification;
            $quality = $this->ebay_business_quality_assess($item, $classification, $rule, $settings, 0.0);
            if (is_wp_error($quality)) {
                $this->ebay_business_pause_output_for_capacity($row, 'quality_blocked', $quality->get_error_message());
                $summary['excluded'] = absint($summary['excluded'] ?? 0) + 1;
                $summary['reviewed'] = absint($summary['reviewed'] ?? 0) + 1;
                return;
            }
            $item = $this->ebay_business_item_with_quality($item, $quality);
            $item['business_selection'] = array('role'=>'candidate','rank'=>0);
        } else {
            // PRIVATE is reclassified from the same fresh getItem facts. Manual
            // Chef decisions remain above automation and are never overwritten.
            $manual_decision = $this->ebay_candidate_manual_decision((string)($item['item_id'] ?? $row['item_id'] ?? ''));
            $manual_status = sanitize_key((string)($manual_decision['status'] ?? 'automatic'));
            if (in_array($manual_status, array('veto','paused'), true)) {
                $manual_error = new WP_Error('ebay_manual_veto', (string)($manual_decision['reason'] ?? 'Manuelles Chef-Veto ist aktiv.'));
                $stored_block = $this->ebay_store_review_candidate($item, $rule, 'INDIVIDUAL', $manual_error, $settings);
                if (is_wp_error($stored_block)) {
                    $summary['technical_errors']++;
                    return;
                }
                global $wpdb;
                $blocked_update = array('status'=>'blocked_manual','route_state'=>'blocked','output_state'=>'none','rejection_reason'=>'[ebay_manual_veto] '.sanitize_text_field((string)($manual_decision['reason'] ?? 'Manuelles Chef-Veto ist aktiv.')),'updated_at'=>time());
                $wpdb->update($this->ebay_items_table(), $blocked_update, array('id'=>absint($stored_block['id'] ?? 0)), $this->ebay_db_formats($blocked_update), array('%d'));
                $this->ebay_private_listing_route_meta($stored_block, 'review', (string)($manual_decision['reason'] ?? 'Manuelles Chef-Veto ist aktiv.'));
                $summary['excluded'] = absint($summary['excluded'] ?? 0) + 1;
                return;
            }
            if ($manual_status === 'approved') {
                $term = $this->ebay_target_from_candidate_decision($manual_decision, $settings);
                if (is_wp_error($term)) {
                    $summary['technical_errors']++;
                    if (count($summary['errors']) < 30) { $summary['errors'][] = array('item_id'=>(string)($row['item_id'] ?? ''),'code'=>$term->get_error_code(),'error'=>$term->get_error_message()); }
                    return;
                }
                $classification = $this->ebay_manual_classification($term, $item, (string)($manual_decision['reason'] ?? 'Manuell freigegeben.'));
                $target_term_id = absint($term->term_id ?? 0);
            } else {
                $classification = $this->ebay_classify_portal_item($item, $rule);
            }
            if (is_wp_error($classification)) {
                $stored_review = $this->ebay_store_review_candidate($item, $rule, 'INDIVIDUAL', $classification, $settings);
                if (is_wp_error($stored_review)) {
                    $summary['technical_errors']++;
                    if (count($summary['errors']) < 30) { $summary['errors'][] = array('item_id'=>(string)($row['item_id'] ?? ''),'code'=>$stored_review->get_error_code(),'error'=>$stored_review->get_error_message()); }
                    return;
                }
                $summary['excluded'] = absint($summary['excluded'] ?? 0) + 1;
                $summary['reviewed'] = absint($summary['reviewed'] ?? 0) + 1;
                return;
            }
            $item['portal_classification'] = $classification;
            if ($target_term_id <= 0) {
                $target_rule = $rule;
                $target_rule['target_term_slug'] = sanitize_title((string)($classification['private_bucket_slug'] ?? ''));
                $resolved = $this->ebay_rule_target_term($target_rule, $settings);
                if (is_wp_error($resolved) || absint($resolved) <= 0) {
                    $summary['technical_errors']++;
                    $error = is_wp_error($resolved) ? $resolved : new WP_Error('ebay_private_target_missing','HivePress-Zielkategorie fehlt.');
                    if (count($summary['errors']) < 30) { $summary['errors'][] = array('item_id'=>(string)($row['item_id'] ?? ''),'code'=>$error->get_error_code(),'error'=>$error->get_error_message()); }
                    return;
                }
                $target_term_id = absint($resolved);
            }
        }
        $stored = $this->ebay_upsert_item($item, $rule, (string) ($row['route_mode'] ?? ''), $target_term_id, $settings);
        if (is_wp_error($stored)) {
            $summary['technical_errors']++;
            if (count($summary['errors']) < 30) { $summary['errors'][] = array('item_id'=>(string)($row['item_id'] ?? ''),'code'=>$stored->get_error_code(),'error'=>$stored->get_error_message()); }
            return;
        }
        if ($seller_type === 'INDIVIDUAL') {
            // Refresh updates the same durable source row only. At job completion
            // the PRIVATE selector decides whether this offer belongs to the bounded
            // 250/30 public inventory; selected changed rows are then rematerialized.
        } else {
            $this->ebay_business_persist_quality_on_source_row($stored, (array)($item['business_quality'] ?? array()), 'candidate', 0);
        }
        $summary['available']++;
        $summary['updated']++;
        if (sanitize_key((string) ($row['output_state'] ?? '')) === 'inactive' || sanitize_key((string) ($row['status'] ?? '')) === 'purged_stale') { $summary['revived']++; }
    }

    private function ebay_refresh_manual_incomplete_reason($job) {
        if (empty($job['manual'])) { return ''; }
        $summary = is_array($job['summary'] ?? null) ? $job['summary'] : array();
        $maintenance = is_array($summary['maintenance'] ?? null) ? $summary['maintenance'] : array();
        $assets = is_array($summary['asset_verification'] ?? null) ? $summary['asset_verification'] : array();
        if (!empty($maintenance['deferred'])) { return 'local_reconcile_limit'; }
        if (!empty($assets['deferred'])) { return 'asset_verification_limit'; }
        return '';
    }

    private function ebay_refresh_finalize_completed_or_partial(&$job, $settings) {
        $reason = $this->ebay_refresh_manual_incomplete_reason($job);
        if ($reason !== '') {
            $job['summary']['stopped_reason'] = $reason;
            return $this->ebay_refresh_finalize($job, $settings, 'partial');
        }
        return $this->ebay_refresh_finalize($job, $settings, 'completed');
    }

    private function ebay_refresh_finalize(&$job, $settings, $status = 'completed') {
        $summary =& $job['summary'];
        $summary['status'] = sanitize_key((string) $status);
        // V5.24: Ein verpasster/verspaeteter Refresh darf niemals selbst den
        // WordPress-Status massenhaft auf Draft umschalten. Ueberfaellige Daten
        // bleiben im Frontend weiterhin fail-closed unsichtbar; nur ein explizites
        // eBay-Endsignal (404/410, Enddatum, OUT_OF_STOCK) tombstoned das Listing.
        $summary['expired'] = array(
            'status'=>'visibility_only',
            'reason'=>'stale_items_are_hidden_but_not_tombstoned',
            'checked'=>0,
            'purged'=>0,
        );
        if ($status === 'completed' && empty($this->ebay_canonical_worker_active)) {
            // Legacy compatibility only. Canonical V6.41 owns selection after
            // the remote cursor is terminal.
            // An explicitly requested full inventory reconcile must verify the
            // complete enabled output inventory even when source contracts were
            // already current and no getItem row changed. Automatic hourly
            // refresh remains touched-route-only to avoid unnecessary replans.
            if (!empty($job['manual'])) {
                $private_selected = !empty($settings['private_enabled']);
                $business_selected = !empty($settings['business_enabled']);
                $scope = $private_selected && $business_selected ? 'all' : ($private_selected ? 'private' : ($business_selected ? 'business' : 'none'));
            } else {
                $private_touched=!empty($settings['private_enabled']) && absint($summary['private_touched']??0)>0;
                $business_touched=!empty($settings['business_enabled']) && absint($summary['business_touched']??0)>0;
                $scope=$private_touched&&$business_touched?'all':($private_touched?'private':($business_touched?'business':'none'));
            }
            if ($scope !== 'none') {
                $selection=$this->ebay_selection_request('inventory_refresh_finalize','refresh:'.sanitize_text_field((string)($job['run_uuid']??'refresh')),false,$scope);
                $summary['selection']=array('status'=>sanitize_key((string)($selection['status']??'pending')),'scope'=>$scope,'queued'=>1);
            } else {
                $summary['selection']=array('status'=>'not_required','scope'=>'none','queued'=>0);
            }
        }
        $summary['finished_at'] = time();
        $summary['duration_seconds'] = max(0, absint($summary['finished_at']) - absint($summary['started_at'] ?? $summary['finished_at']));
        $settings['last_refresh'] = $summary;
        update_option(self::OPTION_NETWORK_EBAY, $settings, false);
        $job['status'] = sanitize_key((string) $status);
        $job['finished_at'] = time();
        $this->ebay_refresh_job_save($job);

        // The same idempotent handoff is used both during the live worker
        // transition and when a compatible bounded partial is adopted after a
        // patch update. There is exactly one owner and one run_uuid.
        if (empty($this->ebay_canonical_worker_active) && $this->ebay_refresh_job_is_bounded_manual_partial($job)) {
            $handoff=$this->ebay_refresh_ensure_manual_selection_handoff($job,$settings,'inventory_refresh_remote_cap');
            if(is_wp_error($handoff)){
                $summary['selection']=array('status'=>'failed','scope'=>'none','queued'=>0,'error_code'=>sanitize_key((string)$handoff->get_error_code()));
                $settings['last_refresh']=$summary;update_option(self::OPTION_NETWORK_EBAY,$settings,false);$this->ebay_refresh_job_save($job);
            }
        }
        if (function_exists('wp_clear_scheduled_hook')) { wp_clear_scheduled_hook(self::EBAY_REFRESH_WORKER_HOOK); }
        return $summary;
    }

    /** Fortsetzbarer gezielter Bestandsabgleich. Maximal fünf getItem-Fälle pro Worker-Tick, weiterhin durch das harte Laufmaximum begrenzt. */
    public function run_ebay_inventory_refresh_worker($manual_or_external = false) {
        $lock_key = 'ppar_ebay_refresh_worker_lock_' . substr(hash('sha256', (string)self::EBAY_RUNTIME_BUILD), 0, 12);
        $use_legacy_lock = empty($this->ebay_canonical_worker_active);
        if ($use_legacy_lock && function_exists('get_transient') && get_transient($lock_key)) { return false; }
        if ($use_legacy_lock && function_exists('set_transient')) { set_transient($lock_key, 1, 45); }
        $reschedule = false;
        $job = array();
        try {
            $job = $this->ebay_refresh_job_load();
            if (!$this->ebay_refresh_job_is_open($job)) { return false; }
            // A canonical selection is a mutation barrier for refresh. The
            // selection worker gets precedence and the SAME refresh keeps its
            // run_uuid/cursors untouched until selection is terminal. This
            // prevents the live cross-lock where maintenance deferred because
            // selection was open while selection deferred because refresh was
            // open.
            $selection_guard=$this->ebay_selection_state_load();
            if($this->ebay_selection_state_is_open($selection_guard)){
                $this->ebay_selection_schedule_worker(10);
                return array('status'=>'deferred_selection_running','selection_owner'=>sanitize_text_field((string)($selection_guard['owner']??'')));
            }
            $settings = $this->ebay_settings();
            $errors = $this->ebay_configuration_errors($settings);
            if ($errors) { return $this->ebay_refresh_finalize($job, $settings, 'failed'); }
            $job['status'] = 'running';
            $job['last_worker_at'] = time();
            $job['summary']['status'] = 'running';
            if (empty($job['last_progress_at'])) { $job['last_progress_at'] = absint($job['updated_at'] ?? time()); }
            $this->ebay_refresh_job_save($job);
            if ($this->ebay_refresh_segment_expired($job)) {
                $job['summary']['stopped_reason'] = 'segment_time_budget';
                return $this->ebay_refresh_finalize($job, $settings, 'partial');
            }

            // Ein Bestandsabgleich ist ein vollstaendiger, deterministischer
            // Reconcile-Orchestrator: 1) lokale Policy/Klassifikation,
            // 2) BUSINESS-Bildpruefung/Replanung, 3) nur faellige eBay-getItem-
            // Quellen. Diagnose-Seiten bleiben dabei strikt read-only.
            $phase = sanitize_key((string)($job['summary']['phase'] ?? 'local_reconciliation'));
            if (!empty($job['summary']['reconcile_contracts']) && $phase === 'local_reconciliation') {
                $max_local = max(1, absint($job['summary']['max_local_reconcile_rows'] ?? 25));
                $already_local = absint($job['summary']['maintenance']['scanned'] ?? 0);
                $local_remaining = max(0, $max_local - $already_local);
                $maintenance = $local_remaining > 0
                    ? $this->run_ebay_maintenance_v2(min(25, $local_remaining), false, 4, true)
                    : array('scanned'=>0,'ready_private'=>0,'ready_business'=>0,'review'=>0,'blocked'=>0,'errors'=>0,'budget_exhausted'=>0);
                if (!isset($job['summary']['maintenance']) || !is_array($job['summary']['maintenance'])) {
                    $job['summary']['maintenance'] = array('scanned'=>0,'ready_private'=>0,'ready_business'=>0,'review'=>0,'blocked'=>0,'errors'=>0,'completed'=>0);
                }
                foreach (array('scanned','ready_private','ready_business','review','blocked','errors') as $key) {
                    $job['summary']['maintenance'][$key] = absint($job['summary']['maintenance'][$key] ?? 0) + absint($maintenance[$key] ?? 0);
                }
                foreach (array('private_touched','business_touched') as $key) {
                    $job['summary'][$key] = absint($job['summary'][$key] ?? 0) + absint($maintenance[$key] ?? 0);
                }
                $maintenance_state = $this->ebay_maintenance_state_load();
                $maintenance_current = $this->ebay_maintenance_state_is_current($maintenance_state);
                $local_total = absint($job['summary']['maintenance']['scanned'] ?? 0);
                if (!$maintenance_current && $local_total < $max_local) {
                    $job['progress_seq'] = absint($job['progress_seq'] ?? 0) + 1;
                    $job['last_progress_at'] = time();
                    $this->ebay_refresh_job_save($job);
                    $reschedule = true;
                    return true;
                }
                $job['summary']['maintenance']['completed'] = $maintenance_current ? 1 : 0;
                $job['summary']['maintenance']['deferred'] = $maintenance_current ? 0 : 1;
                $job['summary']['phase'] = 'asset_verification';
                $phase = 'asset_verification';
                $job['progress_seq'] = absint($job['progress_seq'] ?? 0) + 1;
                $job['last_progress_at'] = time();
                $this->ebay_refresh_job_save($job);
            }

            if (!empty($job['summary']['reconcile_contracts']) && $phase === 'asset_verification') {
                if (!isset($job['summary']['asset_verification']) || !is_array($job['summary']['asset_verification'])) {
                    $job['summary']['asset_verification'] = array('processed'=>0,'verified'=>0,'blocked'=>0,'remaining'=>0,'completed'=>0,'deferred'=>0);
                }
                $max_assets = max(0, absint($job['summary']['max_asset_verifications'] ?? 0));
                $manual_asset_delegate = !empty($job['manual']) && !empty($settings['business_enabled']) && $max_assets === 0;
                if ($manual_asset_delegate) {
                    // Manual reconcile owns source/policy/getItem + selection.
                    // It does not synchronously download hundreds of remote
                    // BUSINESS images. The existing dedicated verifier remains
                    // the single owner of that backlog and output_plan_creative()
                    // revalidates every asset after verification.
                    $remaining_assets = $this->ebay_business_pending_asset_count();
                    $job['summary']['asset_verification']['remaining'] = absint($remaining_assets);
                    $job['summary']['asset_verification']['completed'] = 1;
                    $job['summary']['asset_verification']['deferred'] = 0;
                    $job['summary']['asset_verification']['delegated'] = absint($remaining_assets) > 0 ? 1 : 0;
                    $job['summary']['asset_verification']['status'] = absint($remaining_assets) > 0 ? 'delegated_background' : 'not_required';
                    $job['progress_seq'] = absint($job['progress_seq'] ?? 0) + 1;
                    $job['last_progress_at'] = time();
                    $job['summary']['phase'] = 'source_refresh';
                    $phase = 'source_refresh';
                    $this->ebay_refresh_job_save($job);
                } else {
                    $already_assets = absint($job['summary']['asset_verification']['processed'] ?? 0);
                    $asset_remaining_budget = max(0, $max_assets - $already_assets);
                    $assets = $asset_remaining_budget > 0
                        ? $this->ebay_business_verify_asset_batch(min(2, $asset_remaining_budget))
                        : array('processed'=>0,'verified'=>0,'blocked'=>0,'remaining'=>!empty($settings['business_enabled']) ? $this->ebay_business_pending_asset_count() : 0);
                    foreach (array('processed','verified','blocked') as $key) {
                        $job['summary']['asset_verification'][$key] = absint($job['summary']['asset_verification'][$key] ?? 0) + absint($assets[$key] ?? 0);
                    }
                    if (!empty($settings['business_enabled']) && absint($assets['processed'] ?? 0) > 0) {
                        $job['summary']['business_touched'] = absint($job['summary']['business_touched'] ?? 0) + absint($assets['processed'] ?? 0);
                    }
                    $job['summary']['asset_verification']['remaining'] = absint($assets['remaining'] ?? 0);
                    $job['progress_seq'] = absint($job['progress_seq'] ?? 0) + 1;
                    $job['last_progress_at'] = time();
                    $asset_total = absint($job['summary']['asset_verification']['processed'] ?? 0);
                    if (absint($assets['remaining'] ?? 0) > 0 && $asset_total < $max_assets) {
                        $this->ebay_refresh_job_save($job);
                        $reschedule = true;
                        return true;
                    }
                    $job['summary']['asset_verification']['completed'] = absint($assets['remaining'] ?? 0) > 0 ? 0 : 1;
                    $job['summary']['asset_verification']['deferred'] = absint($assets['remaining'] ?? 0) > 0 ? 1 : 0;
                    $job['summary']['asset_verification']['delegated'] = 0;
                    $job['summary']['asset_verification']['status'] = absint($assets['remaining'] ?? 0) > 0 ? 'bounded_partial' : 'completed';
                    $job['summary']['phase'] = 'source_refresh';
                    $phase = 'source_refresh';
                    $this->ebay_refresh_job_save($job);
                }
            }

            // Cumulative ceiling for this durable generation; every individual
            // segment stays <=2,000. Do not clamp a continued 2,000/2,000 job
            // back to 2,000 or it immediately re-enters max_checks_limit.
            $segment_checks=max(1,min(2000,absint($job['summary']['max_checks_per_segment']??$settings['inventory_refresh_max_per_run']??1200)));
            $remote_segments=max(1,min(20,absint($job['summary']['remote_segments']??1)));
            $generation_hard_ceiling=min(40000,$segment_checks*$remote_segments);
            $requested_ceiling=absint($job['summary']['max_checks']??$segment_checks);
            $max_checks=max(1,min($generation_hard_ceiling,$requested_ceiling>0?$requested_ceiling:$segment_checks));
            if (absint($job['summary']['checked'] ?? 0) >= $max_checks) { $job['summary']['stopped_reason']='max_checks_limit'; return $this->ebay_refresh_finalize($job, $settings, 'partial'); }
            if (!$this->ebay_refresh_has_more($job,$settings)) { return $this->ebay_refresh_finalize_completed_or_partial($job, $settings); }
            $token = $this->ebay_access_token($settings);
            if (is_wp_error($token)) {
                $job['summary']['technical_errors']++;
                if (count($job['summary']['errors']) < 30) { $job['summary']['errors'][] = array('item_id'=>'','code'=>$token->get_error_code(),'error'=>$token->get_error_message()); }
                return $this->ebay_refresh_finalize($job, $settings, 'failed');
            }

            $worker_budget = $manual_or_external ? 8 : max(10, min(30, absint($settings['run_time_budget_seconds'] ?? 20)));
            $deadline = microtime(true) + max(8, $worker_budget - 2);
            $operations = 0;
            while (microtime(true) < $deadline && $operations < 100) {
                $operations++;
                if ($this->ebay_refresh_segment_expired($job)) {
                    $job['summary']['stopped_reason'] = 'segment_time_budget';
                    return $this->ebay_refresh_finalize($job, $settings, 'partial');
                }
                $checked = absint($job['summary']['checked'] ?? 0);
                if ($checked >= $max_checks) {
                    $has_more = $this->ebay_refresh_has_more($job,$settings);
                    if ($has_more) { $job['summary']['stopped_reason']='max_checks_limit'; }
                    return $has_more
                        ? $this->ebay_refresh_finalize($job, $settings, 'partial')
                        : $this->ebay_refresh_finalize_completed_or_partial($job, $settings);
                }
                $rows = $this->ebay_refresh_due_rows($job, min(10, $max_checks - $checked), $settings);
                if (!$rows) { return $this->ebay_refresh_finalize_completed_or_partial($job, $settings); }
                foreach ($rows as $row) {
                    if (microtime(true) >= $deadline) { break; }
                    $this->ebay_refresh_process_row($job, $row, $settings, $token);
                    $job['progress_seq'] = absint($job['progress_seq'] ?? 0) + 1;
                    $job['last_progress_at'] = time();
                    $this->ebay_refresh_job_save($job);
                    if (absint($job['summary']['checked'] ?? 0) >= $max_checks) { break; }
                }
                if (absint($job['summary']['checked'] ?? 0) >= $max_checks) {
                    $has_more = $this->ebay_refresh_has_more($job,$settings);
                    if ($has_more) { $job['summary']['stopped_reason']='max_checks_limit'; }
                    return $has_more
                        ? $this->ebay_refresh_finalize($job, $settings, 'partial')
                        : $this->ebay_refresh_finalize_completed_or_partial($job, $settings);
                }
                if (!$this->ebay_refresh_has_more($job,$settings)) { return $this->ebay_refresh_finalize_completed_or_partial($job, $settings); }
            }
            $reschedule = true;
            $this->ebay_refresh_job_save($job);
            return true;
        } catch (Throwable $error) {
            $settings = $this->ebay_settings();
            if ($this->ebay_refresh_job_is_open($job)) {
                $job['summary']['technical_errors'] = absint($job['summary']['technical_errors'] ?? 0) + 1;
                if (count((array)($job['summary']['errors'] ?? array())) < 30) { $job['summary']['errors'][] = array('item_id'=>'','code'=>'ebay_refresh_runtime_error','error'=>$error->getMessage()); }
                return $this->ebay_refresh_finalize($job, $settings, 'failed');
            }
            return new WP_Error('ebay_refresh_runtime_error', $error->getMessage());
        } finally {
            if ($use_legacy_lock && function_exists('delete_transient')) { delete_transient($lock_key); }
            if ($reschedule) {
                $fresh = $this->ebay_refresh_job_load();
                if ($this->ebay_refresh_job_is_open($fresh)) { $this->ebay_refresh_dispatch_worker($fresh); }
            }
        }
    }

    public function handle_ebay_refresh_worker_tick() {
        $job = $this->ebay_refresh_job_load();
        $provided = isset($_POST['token']) ? (string) wp_unslash($_POST['token']) : '';
        $expected = (string) ($job['worker_token'] ?? '');
        if (!$this->ebay_refresh_job_is_open($job) || $provided === '' || $expected === '' || !hash_equals($expected, $provided)) {
            status_header(403); exit;
        }
        if (function_exists('ignore_user_abort')) { ignore_user_abort(true); }
        if (function_exists('set_time_limit')) { @set_time_limit(45); }
        $this->run_ebay_inventory_refresh_worker(true);
        status_header(204); exit;
    }

    public function handle_ebay_worker_tick() {
        $job = $this->ebay_sync_job_load();
        $provided = isset($_POST['token']) ? (string) wp_unslash($_POST['token']) : '';
        $expected = (string) ($job['worker_token'] ?? '');
        if (!$this->ebay_sync_job_is_open($job) || $provided === '' || $expected === '' || !hash_equals($expected, $provided)) {
            status_header(403);
            exit;
        }
        if (function_exists('ignore_user_abort')) { ignore_user_abort(true); }
        if (function_exists('set_time_limit')) { @set_time_limit(45); }
        $this->run_ebay_sync_worker(true);
        status_header(204);
        exit;
    }

    /**
     * V5.5.0 – eBay-Inhalte nach Ablauf der Frischegrenze sicher deaktivieren.
     *
     * eBay verlangt, dass ANGEZEIGTE Listingdaten höchstens sechs Stunden alt
     * sind. Deshalb werden stale/ended Inhalte aus Frontend und Adminanzeige
     * entfernt. Der portalinterne HivePress-Datensatz bleibt jedoch als
     * Tombstone erhalten, damit Quelle, Workflow und erneute Synchronisierung
     * nachvollziehbar bleiben. Alte eBay-Titel, Preis, Verkäufer, Bild und URLs
     * werden dabei ausdrücklich nicht weiter angezeigt.
     */
    private function ebay_purge_item_content($row, $purge_status, $reason) {
        if (!is_array($row) || empty($row['id'])) { return array('listing_deleted'=>0,'listing_tombstoned'=>0,'creative_disabled'=>0); }
        global $wpdb;
        $listing_tombstoned = 0;
        $creative_disabled = 0;
        $listing_id = absint($row['listing_post_id'] ?? 0);
        $state = strpos((string) $purge_status, 'ended') !== false ? 'ended' : 'stale';

        if ($listing_id > 0) {
            $current_status = function_exists('get_post_status') ? (string) get_post_status($listing_id) : '';
            $publish_intent = $current_status === 'publish' ? 'publish' : sanitize_key((string) get_post_meta($listing_id, '_ppar_ebay_publish_intent', true));
            if (!in_array($publish_intent, array('publish','draft'), true)) { $publish_intent = 'draft'; }
            // V5.14: fail-closed means public output OFF, not source destruction.
            // Keep title/content/image and source metadata internally so an admin
            // preview and a later fresh sync can reuse the same HivePress object.
            if ($current_status === 'publish' && function_exists('wp_update_post')) {
                wp_update_post(array('ID'=>$listing_id, 'post_status'=>'draft'));
                $listing_tombstoned = 1;
            }
            update_post_meta($listing_id, '_ppar_ebay_lifecycle_state', $state);
            update_post_meta($listing_id, '_ppar_ebay_publish_intent', $publish_intent);
            update_post_meta($listing_id, '_ppar_ebay_last_seen_at', absint($row['last_seen'] ?? 0));
            update_post_meta($listing_id, '_ppar_ebay_stale_since', time());
            update_post_meta($listing_id, '_ppar_ebay_source_label', 'eBay privat');
            update_post_meta($listing_id, '_ppar_ebay_item_id', sanitize_text_field((string) ($row['item_id'] ?? '')));
            update_post_meta($listing_id, '_ppar_ebay_seller_type', 'INDIVIDUAL');
            update_post_meta($listing_id, '_ppar_ebay_target_term_id', absint($row['target_term_id'] ?? 0));
            update_post_meta($listing_id, '_ppar_ebay_fresh_until', 0);
        }

        $identity = sanitize_text_field((string) ($row['creative_identity_hash'] ?? ''));
        if ($identity !== '' && method_exists($this, 'creative_library_table')) {
            if (method_exists($this, 'output_objects_table')) {
                $output_table = $this->output_objects_table();
                $objects = $wpdb->get_results($wpdb->prepare("SELECT * FROM {$output_table} WHERE creative_identity_hash=%s", $identity), ARRAY_A);
                foreach ((array) $objects as $object) {
                    if (method_exists($this, 'output_deactivate_materialized_object')) {
                        $this->output_deactivate_materialized_object($object, $reason);
                    }
                    $campaign_id = absint($object['campaign_post_id'] ?? 0);
                    if ($campaign_id > 0 && method_exists($this, 'output_campaign_by_post_id') && method_exists($this, 'save_campaign_record')) {
                        $campaign = $this->output_campaign_by_post_id($campaign_id);
                        if (is_array($campaign)) {
                            // V5.18: Ausgabe deaktivieren, aber Produktidentitaet,
                            // Titel, Bild, Preis und URLs intern erhalten. Ein
                            // spaeter wieder verfuegbares Item kann dadurch
                            // deterministisch denselben Datensatz reaktivieren.
                            $campaign['active'] = false;
                            $campaign['availability'] = 'inactive';
                            $campaign['programme_status'] = 'inactive';
                            $campaign['programme_status_checked_at'] = time();
                            $this->save_campaign_record($campaign, $campaign_id);
                        }
                    }
                    $wpdb->update($output_table, array(
                        'status'=>'blocked_source',
                        'decision_reason'=>sanitize_text_field((string) $reason),
                        'last_verified'=>time(),
                        'updated_at'=>time(),
                    ), array('id'=>absint($object['id'])));
                }
            }
            $creative_table = $this->creative_library_table();
            $creative_row = $wpdb->get_row($wpdb->prepare("SELECT payload FROM {$creative_table} WHERE identity_hash=%s", $identity), ARRAY_A);
            $creative_payload = is_array($creative_row) ? json_decode((string) ($creative_row['payload'] ?? ''), true) : array();
            $creative_payload = is_array($creative_payload) ? $creative_payload : array();
            $creative_payload['_ebay_lifecycle_state'] = $state;
            $creative_payload['_ebay_inactive_at'] = time();
            $creative_payload['_ebay_inactive_reason'] = sanitize_text_field((string) $reason);
            $wpdb->update($creative_table, array(
                'source_status'=>'inactive',
                'availability_state'=>'inactive',
                'selected'=>0,
                'payload'=>wp_json_encode($creative_payload, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES),
            ), array('identity_hash'=>$identity));
            $creative_disabled = 1;
        }

        // V5.14: interne Quelldaten bleiben erhalten. Die öffentliche Ausgabe
        // ist durch Status + Lifecycle + Draft/freshness gate fail-closed. So wird
        // ein verpasster Sync nicht mehr zu irreversiblem Datenverlust.
        $wpdb->update($this->ebay_items_table(), array(
            'status'=>sanitize_key((string) $purge_status),
            'source_state'=>$state === 'ended' ? 'ended' : 'available',
            'output_state'=>'inactive',
            'rejection_reason'=>sanitize_text_field((string) $reason),
            'updated_at'=>time(),
        ), array('id'=>absint($row['id'])));
        return array('listing_deleted'=>0,'listing_tombstoned'=>$listing_tombstoned,'creative_disabled'=>$creative_disabled);
    }

    public function ebay_expire_stale_items() {
        $this->maybe_install_ebay_schema();
        global $wpdb;
        $table = $this->ebay_items_table();
        $now = time();
        $rows = $wpdb->get_results($wpdb->prepare("SELECT * FROM {$table} WHERE status IN ('active','review','purged_stale') AND ((fresh_until>0 AND fresh_until<%d) OR (item_end_at>0 AND item_end_at<=%d))", $now, $now), ARRAY_A);
        $summary = array('checked'=>count((array) $rows),'stale_visibility_only'=>0,'deleted_listings'=>0,'tombstoned_listings'=>0,'disabled_creatives'=>0,'purged'=>0);
        foreach ((array) $rows as $row) {
            $ended = absint($row['item_end_at'] ?? 0) > 0 && absint($row['item_end_at']) <= $now;
            if (!$ended) {
                // Last-Known-Good-Grundgesetz: fehlende Frische markiert nur
                // einen faelligen Refresh. Ohne eindeutiges Endsignal bleibt der
                // bestehende oeffentliche Bestand sichtbar und unveraendert.
                $summary['stale_visibility_only']++; // Legacy-KPI-Name bleibt kompatibel.
                continue;
            }
            $purged = $this->ebay_refresh_mark_ended($row, 'eBay-Angebot beendet; öffentliche eBay-Inhalte deaktiviert.', $this->ebay_settings());
            $summary['deleted_listings'] += absint($purged['listing_deleted'] ?? 0);
            $summary['tombstoned_listings'] += absint($purged['listing_tombstoned'] ?? 0);
            $summary['disabled_creatives'] += absint($purged['creative_disabled'] ?? 0);
            $summary['purged']++;
        }
        return $summary;
    }

    /**
     * V5.14 compatibility stub. Frontend requests are read-only with respect to
     * eBay lifecycle state. Stale data remains Last-Known-Good visible; refresh/end-state enforcement is handled by the scheduled source jobs.
     */
    public function ebay_runtime_stale_guard() {
        return;
    }

    /** True only for a real wp-admin screen, never for public AJAX requests. */
    private function ebay_is_backend_admin_screen_request() {
        if (!function_exists('is_admin') || !is_admin()) { return false; }
        if (function_exists('wp_doing_ajax') && wp_doing_ajax()) { return false; }
        if (defined('DOING_AJAX') && DOING_AJAX) { return false; }
        return true;
    }

    /** Permanent canonical redirect for the removed visible provider category. */
    public function ebay_redirect_legacy_private_category() {
        if ($this->ebay_is_backend_admin_screen_request()) { return; }
        $slug = '';
        if (function_exists('get_query_var')) { $slug = sanitize_title((string) get_query_var('hp_listing_category')); }
        if ($slug !== 'ebay-privatanzeigen') {
            $request_uri = isset($_SERVER['REQUEST_URI']) ? (string) $_SERVER['REQUEST_URI'] : '';
            $path = (string) parse_url($request_uri, PHP_URL_PATH);
            if (!preg_match('~(?:^|/)ebay-privatanzeigen/?$~i', $path)) { return; }
        }
        $parent = $this->ebay_private_parent_term();
        if (!is_object($parent) || !function_exists('get_term_link')) { return; }
        $url = get_term_link($parent, 'hp_listing_category');
        if (is_wp_error($url) || trim((string) $url) === '') { return; }
        if (function_exists('wp_safe_redirect')) { wp_safe_redirect($url, 301, 'Affiliate-Zentrale'); exit; }
    }

    /**
     * Frontend-Sicherheitsfilter für eBay-Lifecycle, Chef-Control und die harte
     * Sichtbarkeitsdecke. Private eBay-Listings dürfen ausschließlich auf ihrer
     * eigenen Single-Seite sowie innerhalb des Taxonomie-Teilbaums ab
     * `private-anzeigen` erscheinen. Der allgemeine Anzeigenmarkt und alle
     * anderen HivePress-Kategorien bleiben frei von diesen eBay-Privatanzeigen.
     */
    /** One final-boundary decision for a public HivePress listing. */
    private function ebay_private_public_post_allowed($post, $source_row, $private_context, $now) {
        if (!is_object($post) || (string)($post->post_type ?? '') !== 'hp_listing') { return true; }
        $post_id=absint($post->ID ?? 0);
        $item_id=function_exists('get_post_meta')?sanitize_text_field((string)get_post_meta($post_id,'_ppar_ebay_item_id',true)):'';
        if($item_id===''){return true;}
        if(!$this->ebay_public_checkpoint_allows_private_listing($post_id)){return false;}
        return $this->ebay_private_public_post_allowed_base($post,$source_row,$private_context,$now);
    }

    /** Existing fach/public safety contract without checkpoint visibility. */
    private function ebay_private_public_post_allowed_base($post, $source_row, $private_context, $now) {
        if (!is_object($post) || (string)($post->post_type ?? '') !== 'hp_listing') { return true; }
        $post_id = absint($post->ID ?? 0);
        $item_id = sanitize_text_field((string)get_post_meta($post_id, '_ppar_ebay_item_id', true));
        if ($item_id === '') { return true; }
        if (!$private_context) { return false; }

        $source_row = is_array($source_row) ? $source_row : array();

        // V6.13: an eBay-marked PRIVATE listing is public only when its durable
        // provider source can still be resolved and audited with the original
        // eBay payload. V6.12 fell back to a title-only check for orphan/legacy
        // listings. That was fail-open: a listing titled e.g. "Pferdegeschichten
        // fuer Kinder" could stay public even when the only book evidence lived
        // in the no-longer-resolved eBay category "Kinder- & Jugendbuecher".
        // Native HivePress listings never reach this branch because they have no
        // _ppar_ebay_item_id marker.
        if (!$source_row) { return false; }
        if (sanitize_text_field((string)($source_row['item_id'] ?? '')) !== $item_id) { return false; }
        if (strtoupper(sanitize_key((string)($source_row['seller_account_type'] ?? ''))) !== 'INDIVIDUAL') { return false; }
        $source_payload = json_decode((string)($source_row['source_payload'] ?? ''), true);
        $source_payload = is_array($source_payload) ? $source_payload : array();
        if (!is_array($source_payload['raw'] ?? null) || !$source_payload['raw']) { return false; }
        if (sanitize_key((string)($source_row['source_state'] ?? 'available')) === 'ended') { return false; }
        if (sanitize_key((string)($source_row['policy_state'] ?? 'allowed')) === 'blocked') { return false; }
        if ($this->ebay_public_content_policy_reason_from_source_row($source_row, (string)($post->post_title ?? '')) !== '') { return false; }

        $lifecycle = sanitize_key((string)get_post_meta($post_id, '_ppar_ebay_lifecycle_state', true));
        if ($lifecycle !== '' && $lifecycle !== 'active') { return false; }
        $seller = (string)get_post_meta($post_id, '_ppar_ebay_seller_username', true);
        $target_term_id = absint(get_post_meta($post_id, '_ppar_ebay_target_term_id', true));
        $control_gate = $this->ebay_private_control_gate($seller, $target_term_id, $post_id);
        if (is_wp_error($control_gate)) { return false; }

        // Refresh age is scheduling information only. A source stays visible
        // until a durable ended/policy/control signal says otherwise.
        $end_at = $source_row ? absint($source_row['item_end_at'] ?? 0) : absint(get_post_meta($post_id, '_ppar_ebay_item_end_at', true));
        return $end_at <= 0 || $end_at > $now;
    }

    /**
     * Final parent refill independent of HivePress' SQL page size.
     *
     * HivePress or another late query component may still return only its own
     * archive window even after pre_get_posts requested 45 candidates. The old
     * implementation could therefore receive 9 rows, filter two, and return 7.
     * At the last public boundary we now fetch a bounded second window from the
     * same taxonomy subtree, run the exact same policy/lifecycle/control gate,
     * and append only unique valid rows until the 3x3 contract is satisfied.
     */
    /**
     * Final parent 3x3 selection with category breadth.
     *
     * V6.34: the parent page must not simply show the nine newest listings.
     * A targeted enrichment (for example Reitstiefel) can create many fresh
     * posts at once and would otherwise monopolise the whole 3x3 overview even
     * though the underlying 250-item PRIVATE inventory is balanced. We therefore
     * build a small, policy-checked candidate pool per direct PRIVATE child and
     * select breadth-first across those children. The durable 250-item selection
     * itself is not changed here.
     */
    private function ebay_private_parent_refill_posts($safe, $query, $parent_id, $now, $limit = 9) {
        $safe = array_values((array)$safe);
        $limit = max(1, min(9, absint($limit)));
        if (!function_exists('get_posts')) { return array_slice($safe, 0, $limit); }

        static $refilling = false;
        if ($refilling) { return array_slice($safe, 0, $limit); }
        $refilling = true;
        try {
            $parent_id = absint($parent_id);
            $child_ids = array();
            if (function_exists('get_terms')) {
                $direct = get_terms(array(
                    'taxonomy'=>'hp_listing_category','hide_empty'=>false,
                    'parent'=>$parent_id,'fields'=>'ids','orderby'=>'term_id','order'=>'ASC',
                ));
                if (!is_wp_error($direct)) {
                    foreach ((array)$direct as $id) { $id=absint($id); if($id>0){$child_ids[$id]=$id;} }
                }
            }
            // Compatibility fallback for installations where get_terms is filtered
            // unusually. Keep only direct children when term objects are available.
            if (!$child_ids && function_exists('get_term_children')) {
                $desc = get_term_children($parent_id, 'hp_listing_category');
                if (!is_wp_error($desc)) {
                    foreach ((array)$desc as $id) {
                        $id=absint($id); if($id<=0){continue;}
                        if(function_exists('get_term')){
                            $term=get_term($id,'hp_listing_category');
                            if(is_object($term) && absint($term->parent??0)!==$parent_id){continue;}
                        }
                        $child_ids[$id]=$id;
                    }
                }
            }
            if (!$child_ids) { return array_slice($safe, 0, $limit); }

            $seen = array();
            $pool = array();
            foreach ($safe as $post) {
                $id=is_object($post)?absint($post->ID??0):0;
                if($id>0 && !isset($seen[$id])){$seen[$id]=true;$pool[]=$post;}
            }
            if (is_object($query) && isset($query->posts) && is_array($query->posts)) {
                foreach ($query->posts as $post) {
                    $id=is_object($post)?absint($post->ID??0):0;
                    if($id>0){$seen[$id]=true;}
                }
            }

            // Fetch a bounded window independently per direct child. This is the
            // critical difference from the old global "latest 45" refill: even if
            // all 45 newest posts are boots, the other PRIVATE areas remain eligible
            // for the overview.
            foreach ($child_ids as $child_id) {
                $candidates = get_posts(array(
                    'post_type'=>'hp_listing','post_status'=>'publish',
                    'posts_per_page'=>6,'numberposts'=>6,
                    'tax_query'=>array(array(
                        'taxonomy'=>'hp_listing_category','field'=>'term_id','terms'=>array($child_id),
                        'operator'=>'IN','include_children'=>false,
                    )),
                    'orderby'=>'date','order'=>'DESC','ignore_sticky_posts'=>true,
                    'no_found_rows'=>true,'suppress_filters'=>true,
                ));
                if(!$candidates){continue;}
                $item_ids=array();$post_item_ids=array();
                foreach((array)$candidates as $post){
                    if(!is_object($post)||(string)($post->post_type??'')!=='hp_listing'){continue;}
                    $post_id=absint($post->ID??0);if($post_id<=0||isset($seen[$post_id])){continue;}
                    $item_id=sanitize_text_field((string)get_post_meta($post_id,'_ppar_ebay_item_id',true));
                    if($item_id!==''){$post_item_ids[$post_id]=$item_id;$item_ids[]=$item_id;}
                }
                $source_rows=$this->ebay_public_source_rows_by_item_ids($item_ids,'INDIVIDUAL');
                foreach((array)$candidates as $post){
                    if(!is_object($post)){continue;}
                    $post_id=absint($post->ID??0);if($post_id<=0||isset($seen[$post_id])){continue;}
                    $item_id=(string)($post_item_ids[$post_id]??'');
                    $source_row=$item_id!==''&&is_array($source_rows[$item_id]??null)?$source_rows[$item_id]:array();
                    if(!$this->ebay_private_public_post_allowed($post,$source_row,true,$now)){continue;}
                    $pool[]=$post;$seen[$post_id]=true;
                }
            }

            // Bucket candidates by their canonical direct PRIVATE target. Native
            // HivePress listings without the plugin target marker fall back to their
            // assigned taxonomy terms and remain eligible.
            $buckets=array();$unbucketed=array();
            foreach($pool as $post){
                if(!is_object($post)){continue;}
                $post_id=absint($post->ID??0);if($post_id<=0){continue;}
                $bucket=absint(get_post_meta($post_id,'_ppar_ebay_target_term_id',true));
                if(!isset($child_ids[$bucket])){
                    $bucket=0;
                    if(function_exists('wp_get_post_terms')){
                        $terms=wp_get_post_terms($post_id,'hp_listing_category',array('fields'=>'ids'));
                        if(!is_wp_error($terms)){
                            foreach((array)$terms as $term_id){$term_id=absint($term_id);if(isset($child_ids[$term_id])){$bucket=$term_id;break;}}
                        }
                    }
                }
                if($bucket>0){$buckets[$bucket][]=$post;}else{$unbucketed[]=$post;}
            }

            // Preserve the order in which categories first appeared in the public
            // candidate set, then append any missing direct children deterministically.
            $order=array();
            foreach($pool as $post){
                $post_id=is_object($post)?absint($post->ID??0):0;if($post_id<=0){continue;}
                $bucket=absint(get_post_meta($post_id,'_ppar_ebay_target_term_id',true));
                if(isset($child_ids[$bucket])&&!isset($order[$bucket])){$order[$bucket]=$bucket;}
            }
            foreach($child_ids as $child_id){if(!isset($order[$child_id])){$order[$child_id]=$child_id;}}

            $balanced=array();$used=array();$depth=0;
            while(count($balanced)<$limit){
                $added=0;
                foreach($order as $child_id){
                    if(count($balanced)>=$limit){break;}
                    if(!isset($buckets[$child_id][$depth])){continue;}
                    $post=$buckets[$child_id][$depth];$id=absint($post->ID??0);
                    if($id<=0||isset($used[$id])){continue;}
                    $balanced[]=$post;$used[$id]=true;$added++;
                }
                if($added===0){break;}
                $depth++;
            }
            // Only if the direct-child pool cannot fill nine cards, preserve valid
            // unbucketed/native rows as a final fallback.
            foreach($unbucketed as $post){
                if(count($balanced)>=$limit){break;}
                $id=is_object($post)?absint($post->ID??0):0;
                if($id>0&&!isset($used[$id])){$balanced[]=$post;$used[$id]=true;}
            }
            return array_slice($balanced,0,$limit);
        } finally {
            $refilling = false;
        }
    }

    public function ebay_filter_stale_posts($posts, $query = null) {
        if ($this->ebay_is_backend_admin_screen_request() || !$posts) { return $posts; }
        $now = time();
        $safe = array();
        $private_context = $this->ebay_query_allows_private_ebay($query);

        // Resolve all source rows once. The public layer then re-checks the same
        // central policy used by Discovery/Maintenance.
        $post_item_ids = array();
        $source_item_ids = array();
        foreach ((array)$posts as $post) {
            if (!is_object($post) || (string)($post->post_type ?? '') !== 'hp_listing') { continue; }
            $post_id = absint($post->ID ?? 0);
            $item_id = sanitize_text_field((string)get_post_meta($post_id, '_ppar_ebay_item_id', true));
            if ($item_id === '') { continue; }
            $post_item_ids[$post_id] = $item_id;
            $source_item_ids[] = $item_id;
        }
        $source_rows = $this->ebay_public_source_rows_by_item_ids($source_item_ids, 'INDIVIDUAL');

        foreach ((array)$posts as $post) {
            if (!is_object($post) || (string)($post->post_type ?? '') !== 'hp_listing') { $safe[] = $post; continue; }
            $post_id = absint($post->ID ?? 0);
            $item_id = (string)($post_item_ids[$post_id] ?? '');
            $source_row = $item_id !== '' && is_array($source_rows[$item_id] ?? null) ? $source_rows[$item_id] : array();
            if ($this->ebay_private_public_post_allowed($post, $source_row, $private_context, $now)) { $safe[] = $post; }
        }

        $parent = $this->ebay_private_parent_term();
        $parent_id = is_object($parent) ? absint($parent->term_id ?? 0) : 0;
        if ($parent_id > 0 && $this->ebay_query_targets_private_parent($query, $parent_id)) {
            // Store the original result set only for the late refill's exclusion
            // list when a real WP_Query exposes it. Then guarantee the final 3x3
            // result independent of the SQL window HivePress actually honored.
            $safe = $this->ebay_private_parent_refill_posts($safe, $query, $parent_id, $now, 9);
        }
        return $safe;
    }

    /**
     * HivePress setzt die Taxonomieabfrage selbst. Auf der übergeordneten Kategorie
     * "Private Anzeigen" werden deshalb die komplette eBay-Wurzel und alle tieferen
     * Nachfahren explizit in dieselbe Taxonomie-Klausel aufgenommen. Andere
     * HivePress-Kategorien und normale Listings bleiben vollständig unangetastet.
     */
    /** Resolve the exact HivePress parent term without relying on global query state. */
    private function ebay_private_parent_term() {
        if (!function_exists('get_term_by')) { return null; }
        $term = get_term_by('slug', 'private-anzeigen', 'hp_listing_category');
        return is_object($term) ? $term : null;
    }

    /** Check whether the passed WP_Query actually targets Private Anzeigen. */
    private function ebay_query_targets_private_parent($query, $parent_id) {
        if (!is_object($query) || !method_exists($query, 'get')) { return false; }
        $parent_id = absint($parent_id);

        // Instance conditional is safe inside pre_get_posts; global is_tax() is not.
        if (method_exists($query, 'is_tax') && $query->is_tax('hp_listing_category', 'private-anzeigen')) { return true; }

        $direct = $query->get('hp_listing_category');
        foreach ((array) $direct as $value) {
            if (sanitize_title((string) $value) === 'private-anzeigen') { return true; }
        }
        if ((string) $query->get('taxonomy') === 'hp_listing_category') {
            $term_value = (string) $query->get('term');
            if (sanitize_title($term_value) === 'private-anzeigen') { return true; }
            if ($parent_id > 0 && absint($query->get('term_id')) === $parent_id) { return true; }
        }

        $contains_parent = function($clause) use (&$contains_parent, $parent_id) {
            if (!is_array($clause)) { return false; }
            if (isset($clause['taxonomy']) && (string) $clause['taxonomy'] === 'hp_listing_category') {
                $field = sanitize_key((string) ($clause['field'] ?? 'term_id'));
                foreach ((array) ($clause['terms'] ?? array()) as $term_value) {
                    if ($field === 'slug' || $field === 'name') {
                        if (sanitize_title((string) $term_value) === 'private-anzeigen') { return true; }
                    } elseif ($parent_id > 0 && absint($term_value) === $parent_id) {
                        return true;
                    }
                }
            }
            foreach ($clause as $value) {
                if (is_array($value) && $contains_parent($value)) { return true; }
            }
            return false;
        };
        return $contains_parent((array) $query->get('tax_query'));
    }

    /**
     * HivePress deliberately maintains category counts across descendants, while
     * its listing loop may still query only the selected term. On the exact
     * parent "Private Anzeigen" we therefore expand the tax clause to all
     * descendants. Detection uses only the passed WP_Query, never global tags.
     */
    public function ebay_expand_private_parent_listing_query($query) {
        if ($this->ebay_is_backend_admin_screen_request()) { return; }
        if (!is_object($query) || !method_exists($query, 'get') || !method_exists($query, 'set')) { return; }

        $parent = $this->ebay_private_parent_term();
        $parent_id = is_object($parent) ? absint($parent->term_id ?? 0) : 0;
        if ($parent_id <= 0 || !$this->ebay_query_targets_private_parent($query, $parent_id)) { return; }
        if (!function_exists('get_term_children')) { return; }
        $children = get_term_children($parent_id, 'hp_listing_category');
        if (is_wp_error($children)) { return; }
        $term_ids = array_values(array_unique(array_filter(array_merge(array($parent_id), array_map('absint', (array) $children)))));
        if (count($term_ids) < 2) { return; }

        $existing_tax_query = $query->get('tax_query');
        $tax_query = is_array($existing_tax_query) ? $existing_tax_query : array();
        $matched = false;
        $rewrite_clause = function($clause) use (&$rewrite_clause, &$matched, $parent_id, $term_ids) {
            if (!is_array($clause)) { return $clause; }
            if (isset($clause['taxonomy']) && (string) $clause['taxonomy'] === 'hp_listing_category') {
                $field = sanitize_key((string) ($clause['field'] ?? 'term_id'));
                $is_parent = false;
                foreach ((array) ($clause['terms'] ?? array()) as $term_value) {
                    if (($field === 'slug' || $field === 'name') && sanitize_title((string) $term_value) === 'private-anzeigen') { $is_parent = true; break; }
                    if (!in_array($field, array('slug','name'), true) && absint($term_value) === $parent_id) { $is_parent = true; break; }
                }
                if ($is_parent) {
                    $clause['field'] = 'term_id';
                    $clause['terms'] = $term_ids;
                    $clause['operator'] = 'IN';
                    // Already expanded explicitly, so never rely on another plugin's child policy.
                    $clause['include_children'] = false;
                    $matched = true;
                }
                return $clause;
            }
            foreach ($clause as $key=>$value) {
                if (is_array($value)) { $clause[$key] = $rewrite_clause($value); }
            }
            return $clause;
        };
        $tax_query = $rewrite_clause($tax_query);
        if (!$matched) {
            $tax_query[] = array(
                'taxonomy'=>'hp_listing_category',
                'field'=>'term_id',
                'terms'=>$term_ids,
                'operator'=>'IN',
                'include_children'=>false,
            );
        }
        $query->set('tax_query', $tax_query);

        // Prevent the original taxonomy query var from re-adding a second,
        // parent-only clause when WP_Query parses tax vars after pre_get_posts.
        $direct_category = $query->get('hp_listing_category');
        $clear_direct_category = false;
        foreach ((array) $direct_category as $direct_value) {
            if (sanitize_title((string) $direct_value) === 'private-anzeigen') {
                $clear_direct_category = true;
                break;
            }
        }
        if ($clear_direct_category) {
            $query->set('hp_listing_category', '');
        }
        if ((string) $query->get('taxonomy') === 'hp_listing_category') {
            $query->set('taxonomy', '');
            $query->set('term', '');
            $query->set('term_id', 0);
        }

        // Private Anzeigen is a 3x3 teaser overview, not a second full archive.
        // IMPORTANT: public visibility is filtered later at `the_posts` because
        // freshness, end state and Chef-Control cannot all be expressed safely in
        // one generic HivePress SQL meta query. Fetch a bounded refill window here
        // and cut to exactly nine only AFTER those gates. Otherwise two blocked or
        // stale rows inside the first SQL page turn a healthy 3x3 pool into 7 cards.
        $candidate_limit = 45;
        $query->set('posts_per_page', $candidate_limit);
        $query->set('posts_per_archive_page', $candidate_limit);
        $query->set('_ppar_ebay_private_public_limit', 9);
        $query->set('paged', 1);
        $query->set('no_found_rows', true);
    }


    /** Ist die konkrete WP_Query eine einzelne HivePress-Anzeige? */
    private function ebay_query_is_listing_singular($query) {
        if (!is_object($query)) { return false; }
        if (method_exists($query, 'is_singular') && $query->is_singular('hp_listing')) { return true; }
        if (!method_exists($query, 'get')) { return false; }
        $post_type = $query->get('post_type');
        $is_listing_type = $post_type === 'hp_listing' || (is_array($post_type) && in_array('hp_listing', $post_type, true));
        if (!$is_listing_type) { return false; }
        return absint($query->get('p')) > 0 || trim((string) $query->get('name')) !== '' || trim((string) $query->get('pagename')) !== '';
    }

    /** Alle explizit in der Query angesprochenen hp_listing_category-Term-IDs. */
    private function ebay_query_listing_category_term_ids($query) {
        if (!is_object($query)) { return array(); }
        $ids = array();
        $resolve = function($value, $field = 'slug') use (&$ids) {
            if ($field === 'term_id' || $field === 'id') {
                $id = absint($value);
                if ($id > 0) { $ids[$id] = $id; }
                return;
            }
            if (!function_exists('get_term_by')) { return; }
            $lookup = $field === 'name' ? 'name' : 'slug';
            $term = get_term_by($lookup, (string) $value, 'hp_listing_category');
            if (is_object($term) && absint($term->term_id ?? 0) > 0) { $ids[absint($term->term_id)] = absint($term->term_id); }
        };

        if (method_exists($query, 'get_queried_object')) {
            $queried = $query->get_queried_object();
            if (is_object($queried) && (string) ($queried->taxonomy ?? '') === 'hp_listing_category' && absint($queried->term_id ?? 0) > 0) {
                $ids[absint($queried->term_id)] = absint($queried->term_id);
            }
        }
        if (!method_exists($query, 'get')) { return array_values($ids); }

        foreach ((array) $query->get('hp_listing_category') as $value) {
            if (trim((string) $value) !== '') { $resolve($value, 'slug'); }
        }
        if ((string) $query->get('taxonomy') === 'hp_listing_category') {
            if (absint($query->get('term_id')) > 0) { $resolve($query->get('term_id'), 'term_id'); }
            elseif (trim((string) $query->get('term')) !== '') { $resolve($query->get('term'), 'slug'); }
        }
        $walk = function($node) use (&$walk, $resolve) {
            if (!is_array($node)) { return; }
            if (isset($node['taxonomy']) && (string) $node['taxonomy'] === 'hp_listing_category') {
                $field = sanitize_key((string) ($node['field'] ?? 'term_id'));
                foreach ((array) ($node['terms'] ?? array()) as $value) { $resolve($value, $field); }
            }
            foreach ($node as $value) { if (is_array($value)) { $walk($value); } }
        };
        $walk((array) $query->get('tax_query'));

        return array_values($ids);
    }

    /** Exakte Sichtbarkeitsregel: Single oder Taxonomie-Teilbaum ab Private Anzeigen. */
    private function ebay_query_allows_private_ebay($query) {
        if ($this->ebay_query_is_listing_singular($query)) { return true; }
        $parent = $this->ebay_private_parent_term();
        $parent_id = is_object($parent) ? absint($parent->term_id ?? 0) : 0;
        if ($parent_id <= 0) { return false; }
        $ids = $this->ebay_query_listing_category_term_ids($query);
        if (!$ids) { return false; }
        foreach ($ids as $term_id) {
            if ($term_id === $parent_id) { return true; }
            $ancestors = function_exists('get_ancestors') ? array_map('absint', (array) get_ancestors($term_id, 'hp_listing_category', 'taxonomy')) : array();
            if (in_array($parent_id, $ancestors, true)) { return true; }
        }
        return false;
    }

    /**
     * Query-seitige Decke, damit Pagination/Counts nicht erst nach `the_posts`
     * korrigiert werden müssen. Außerhalb des erlaubten Teilbaums werden nur
     * Posts mit unserem eBay-Item-Metafeld ausgeschlossen; native HivePress-
     * Anzeigen bleiben vollständig erhalten.
     */
    public function ebay_enforce_private_visibility_ceiling($query) {
        if ($this->ebay_is_backend_admin_screen_request()) { return; }
        if (!is_object($query) || !method_exists($query, 'get') || !method_exists($query, 'set')) { return; }
        if ($this->ebay_query_is_listing_singular($query) || $this->ebay_query_allows_private_ebay($query)) { return; }
        if ($query->get('_ppar_ebay_visibility_ceiling')) { return; }

        $post_type = $query->get('post_type');
        $listing_query = $post_type === 'hp_listing' || (is_array($post_type) && in_array('hp_listing', $post_type, true));
        if (!$listing_query) {
            $listing_query = (string) $query->get('taxonomy') === 'hp_listing_category' || !empty($query->get('hp_listing_category')) || !empty($this->ebay_query_listing_category_term_ids($query));
        }
        if (!$listing_query) { return; }

        $existing_meta_query = $query->get('meta_query');
        $meta_query = is_array($existing_meta_query) ? $existing_meta_query : array();
        $meta_query[] = array('key'=>'_ppar_ebay_item_id','compare'=>'NOT EXISTS');
        $query->set('meta_query', $meta_query);
        $query->set('_ppar_ebay_visibility_ceiling', 1);
    }


    /** Admin: Quelle und eBay-Lifecycle direkt in HivePress > Listings sichtbar. */
    public function ebay_admin_listing_columns($columns) {
        if (!is_array($columns)) { return $columns; }
        $columns['ppar_source'] = 'Quelle';
        $columns['ppar_ebay_state'] = 'eBay-Status';
        return $columns;
    }

    public function ebay_admin_listing_column_content($column, $post_id) {
        $post_id = absint($post_id);
        if ($column === 'ppar_source') {
            if ((string) get_post_meta($post_id, '_ppar_ebay_item_id', true) !== '') {
                echo '<strong>eBay privat</strong>';
            } else {
                echo 'HivePress / intern';
            }
            return;
        }
        if ($column !== 'ppar_ebay_state') { return; }
        if ((string) get_post_meta($post_id, '_ppar_ebay_item_id', true) === '') { echo '—'; return; }
        $state = sanitize_key((string) get_post_meta($post_id, '_ppar_ebay_lifecycle_state', true));
        $labels = array('active'=>'Aktiv / frisch','stale'=>'Veraltet – Frontend aus','ended'=>'Beendet – Frontend aus');
        echo esc_html($labels[$state] ?? 'eBay – Status unbekannt');
        $last_seen = absint(get_post_meta($post_id, '_ppar_ebay_last_seen_at', true));
        if ($last_seen > 0) { echo '<br><small>Letzter Abgleich: ' . esc_html(wp_date('d.m.Y H:i', $last_seen)) . '</small>'; }
        $status = function_exists('get_post_status') ? (string) get_post_status($post_id) : '';
        if ($state === 'active') {
            if ($status === 'publish' && function_exists('get_permalink')) {
                echo '<br><a href="' . esc_url(get_permalink($post_id)) . '" target="_blank" rel="noopener">Öffnen</a>';
            } elseif (in_array($status, array('draft','pending','private'), true)) {
                // Do not fall back to WordPress' native hp_listing draft URL.
                // HivePress does not provide a reliable public draft single route;
                // always use the dedicated secure renderer for eBay drafts.
                $preview_url = $this->ebay_admin_preview_url($post_id);
                if ($preview_url !== '') { echo '<br><a href="' . esc_url($preview_url) . '" target="_blank" rel="noopener">Vorschau</a>'; }
            }
        }
    }

    public function ebay_admin_listing_row_actions($actions, $post) {
        if (!is_array($actions) || !is_object($post) || (string) ($post->post_type ?? '') !== 'hp_listing') { return $actions; }
        $post_id = absint($post->ID ?? 0);
        if ($post_id <= 0 || (string) get_post_meta($post_id, '_ppar_ebay_item_id', true) === '') { return $actions; }
        if (!function_exists('current_user_can') || !current_user_can('edit_post', $post_id)) { return $actions; }
        $url = $this->ebay_secure_preview_url($post_id);
        if ($url !== '') {
            $actions['view'] = '<a href="' . esc_url($url) . '" target="_blank" rel="noopener">Vorschau</a>';
        }
        return $actions;
    }

    public function ebay_admin_listing_filters($post_type = '') {
        if ((string) $post_type !== 'hp_listing') { return; }
        $source = isset($_GET['ppar_listing_source']) ? sanitize_key(wp_unslash((string) $_GET['ppar_listing_source'])) : '';
        $state = isset($_GET['ppar_ebay_state']) ? sanitize_key(wp_unslash((string) $_GET['ppar_ebay_state'])) : '';
        echo '<select name="ppar_listing_source">';
        echo '<option value="">Alle Quellen</option>';
        echo '<option value="ebay"' . selected($source, 'ebay', false) . '>eBay privat</option>';
        echo '<option value="normal"' . selected($source, 'normal', false) . '>Normale HivePress-Listings</option>';
        echo '</select>';
        echo '<select name="ppar_ebay_state">';
        echo '<option value="">Alle eBay-Status</option>';
        echo '<option value="active"' . selected($state, 'active', false) . '>Aktiv / frisch</option>';
        echo '<option value="stale"' . selected($state, 'stale', false) . '>Veraltet</option>';
        echo '<option value="ended"' . selected($state, 'ended', false) . '>Beendet</option>';
        echo '</select>';
    }

    public function ebay_admin_filter_listing_query($query) {
        if (!is_admin() || !is_object($query) || (method_exists($query, 'is_main_query') && !$query->is_main_query())) { return; }
        $post_type = method_exists($query, 'get') ? $query->get('post_type') : '';
        if (is_array($post_type)) { $is_listing = in_array('hp_listing', $post_type, true); }
        else { $is_listing = (string) $post_type === 'hp_listing'; }
        if (!$is_listing || !method_exists($query, 'set')) { return; }
        $source = isset($_GET['ppar_listing_source']) ? sanitize_key(wp_unslash((string) $_GET['ppar_listing_source'])) : '';
        $state = isset($_GET['ppar_ebay_state']) ? sanitize_key(wp_unslash((string) $_GET['ppar_ebay_state'])) : '';
        $meta_query = method_exists($query, 'get') ? $query->get('meta_query') : array();
        $meta_query = is_array($meta_query) ? $meta_query : array();
        if ($source === 'ebay') { $meta_query[] = array('key'=>'_ppar_ebay_item_id','compare'=>'EXISTS'); }
        elseif ($source === 'normal') { $meta_query[] = array('key'=>'_ppar_ebay_item_id','compare'=>'NOT EXISTS'); }
        if (in_array($state, array('active','stale','ended'), true)) {
            $meta_query[] = array('key'=>'_ppar_ebay_lifecycle_state','value'=>$state,'compare'=>'=');
            // Ein eBay-Statusfilter impliziert eBay-Quelle.
            if ($source === '') { $meta_query[] = array('key'=>'_ppar_ebay_item_id','compare'=>'EXISTS'); }
        }
        if ($meta_query) { $query->set('meta_query', $meta_query); }
    }

    /**
     * Vor Anzeige der Backend-Liste stale Daten sicher deaktivieren und alte
     * V5.4.0-Frischdatensätze einmalig mit Lifecycle-Metadaten ergänzen.
     */
    public function ebay_admin_prepare_listing_lifecycle() {
        if (!function_exists('post_type_exists') || !post_type_exists('hp_listing')) { return; }
        // Versionierter Schlüssel: Nach dem V5.8-Update läuft die Bestandsprüfung
        // sofort und wird nicht durch einen Transient eines älteren Builds übersprungen.
        $key = 'ppar_ebay_admin_lifecycle_v580';
        if (function_exists('get_transient') && get_transient($key)) { return; }
        if (function_exists('set_transient')) { set_transient($key, 1, 60); }
        // V5.24: Backend-Aufrufe sind strikt read-only fuer den eBay-Lifecycle.
        // Stale Listings werden nicht mehr allein durch das Oeffnen der Adminliste
        // auf Draft gesetzt. Der gezielte Refresh entscheidet ausschliesslich bei
        // einem bestaetigten Endsignal ueber die Deaktivierung.
        if (!function_exists('get_posts')) { return; }
        $ids = get_posts(array(
            'post_type'=>'hp_listing',
            'post_status'=>array('draft','pending','publish','private'),
            'meta_key'=>'_ppar_ebay_item_id',
            'meta_compare'=>'EXISTS',
            'posts_per_page'=>-1,
            'fields'=>'ids',
            'suppress_filters'=>true,
        ));
        $now = time();
        $settings = $this->ebay_settings();
        // Den technischen HivePress-Besitzer nicht nur für diesen Request
        // auflösen, sondern dauerhaft speichern. Hintergrundworker und spätere
        // Reparaturen verwenden dadurch dieselbe gültige WordPress-Identität.
        $author_result = $this->ebay_persist_listing_author_id($settings);
        $author_id = is_wp_error($author_result) ? 0 : absint($author_result);
        foreach ((array) $ids as $listing_id) {
            $listing_id = absint($listing_id);
            if ($listing_id <= 0) { continue; }
            if ($author_id > 0 && function_exists('get_post_field') && absint(get_post_field('post_author', $listing_id)) <= 0 && function_exists('wp_update_post')) {
                wp_update_post(array('ID'=>$listing_id,'post_author'=>$author_id));
            }
            if ((string) get_post_meta($listing_id, '_ppar_ebay_lifecycle_state', true) !== '') { continue; }
            $fresh_until = absint(get_post_meta($listing_id, '_ppar_ebay_fresh_until', true));
            $end_at = absint(get_post_meta($listing_id, '_ppar_ebay_item_end_at', true));
            // Migration darf aus einem bloss ueberfaelligen Refresh niemals einen
            // versteckten Lifecycle-Zustand erzeugen. Nur Endsignale deaktivieren.
            $state = ($end_at > 0 && $end_at <= $now) ? 'ended' : 'active';
            update_post_meta($listing_id, '_ppar_ebay_lifecycle_state', $state);
            update_post_meta($listing_id, '_ppar_ebay_publish_intent', function_exists('get_post_status') && get_post_status($listing_id) === 'publish' ? 'publish' : 'draft');
            update_post_meta($listing_id, '_ppar_ebay_last_seen_at', max(0, $fresh_until - 6 * HOUR_IN_SECONDS));
        }
    }

    public function ebay_setup_private_categories() {
        if (!function_exists('taxonomy_exists') || !taxonomy_exists('hp_listing_category') || !function_exists('wp_insert_term') || !function_exists('wp_update_term')) {
            return new WP_Error('ebay_hivepress_missing', 'HivePress-Kategorietaxonomie fehlt.');
        }
        $parent_exists = term_exists('private-anzeigen', 'hp_listing_category');
        if (is_array($parent_exists)) { $parent_id = absint($parent_exists['term_id'] ?? 0); }
        elseif (is_numeric($parent_exists) && absint($parent_exists) > 0) { $parent_id = absint($parent_exists); }
        else {
            $created = wp_insert_term('Private Anzeigen', 'hp_listing_category', array('slug'=>'private-anzeigen','description'=>'Private Anzeigen im Anzeigenmarkt.'));
            if (is_wp_error($created)) { return $created; }
            $parent_id = absint($created['term_id'] ?? 0);
        }
        if ($parent_id <= 0) { return new WP_Error('ebay_private_parent_create_failed', 'Private-Anzeigen-Wurzel konnte nicht erstellt werden.'); }
        $parent_term = get_term($parent_id, 'hp_listing_category');
        if (!$parent_term || is_wp_error($parent_term) || absint($parent_term->parent ?? 0) !== 0) {
            return new WP_Error('ebay_private_parent_conflict', 'Der Slug private-anzeigen ist bereits außerhalb der Taxonomie-Wurzel belegt.');
        }

        $legacy_exists = term_exists('ebay-privatanzeigen', 'hp_listing_category');
        $legacy_id = is_array($legacy_exists) ? absint($legacy_exists['term_id'] ?? 0) : (is_numeric($legacy_exists) ? absint($legacy_exists) : 0);
        if ($legacy_id > 0) {
            $legacy = get_term($legacy_id, 'hp_listing_category');
            if (!$legacy || is_wp_error($legacy) || absint($legacy->parent ?? 0) !== $parent_id) {
                return new WP_Error('ebay_private_legacy_conflict', 'Die frühere Kategorie „eBay-Privatanzeigen“ liegt nicht unter „Private Anzeigen“ und wird deshalb nicht automatisch verändert.');
            }
        }

        $children = $this->ebay_private_bucket_definitions();
        $created_count = 0;
        $moved_count = 0;
        $child_ids = array();
        foreach ($children as $slug=>$label) {
            $existing = term_exists($slug, 'hp_listing_category');
            if ($existing) {
                $term_id = is_array($existing) ? absint($existing['term_id'] ?? 0) : absint($existing);
                $term = $term_id > 0 ? get_term($term_id, 'hp_listing_category') : null;
                if (!$term || is_wp_error($term)) { return new WP_Error('ebay_private_child_missing', 'HivePress-Kategorie konnte nicht gelesen werden: ' . $slug); }
                $current_parent = absint($term->parent ?? 0);
                if ($current_parent === $legacy_id && $legacy_id > 0) {
                    $updated = wp_update_term($term_id, 'hp_listing_category', array('parent'=>$parent_id));
                    if (is_wp_error($updated)) { return $updated; }
                    $moved_count++;
                } elseif ($current_parent !== $parent_id) {
                    return new WP_Error('ebay_private_child_conflict', 'Der HivePress-Slug ' . $slug . ' ist bereits außerhalb von „Private Anzeigen“ belegt.');
                }
                $child_ids[$slug] = $term_id;
                continue;
            }
            $result = wp_insert_term($label, 'hp_listing_category', array('slug'=>$slug,'parent'=>$parent_id));
            if (is_wp_error($result)) { return $result; }
            $child_ids[$slug] = absint($result['term_id'] ?? 0);
            $created_count++;
        }

        // Persist the flat structure before repairing any legacy object/root assignments.
        $settings = $this->ebay_settings();
        $settings['private_parent_term_id'] = $parent_id;
        $settings['private_root_term_id'] = $parent_id;
        update_option(self::OPTION_NETWORK_EBAY, $settings, false);

        $legacy_reassigned = 0;
        if ($legacy_id > 0 && function_exists('get_objects_in_term')) {
            $objects = get_objects_in_term($legacy_id, 'hp_listing_category');
            if (!is_wp_error($objects)) {
                foreach ((array) $objects as $object_id) {
                    $object_id = absint($object_id);
                    if ($object_id <= 0) { continue; }
                    $assigned = function_exists('wp_get_post_terms') ? wp_get_post_terms($object_id, 'hp_listing_category', array('fields'=>'ids')) : array();
                    $assigned = is_wp_error($assigned) ? array() : array_map('absint', (array) $assigned);
                    $target = 0;
                    foreach ($child_ids as $child_id) {
                        if (in_array(absint($child_id), $assigned, true)) { $target = absint($child_id); break; }
                    }
                    if ($target <= 0 && function_exists('get_post_meta')) {
                        $meta_target = absint(get_post_meta($object_id, '_ppar_ebay_target_term_id', true));
                        if (in_array($meta_target, array_map('absint', array_values($child_ids)), true)) { $target = $meta_target; }
                    }
                    if ($target <= 0) { $target = absint($child_ids['sonstiges'] ?? 0); }
                    if ($target > 0 && function_exists('wp_set_post_terms')) {
                        // Append the recovered target and remove only the obsolete provider term.
                        // Never wipe unrelated manual HivePress categories from an existing listing.
                        $set = wp_set_post_terms($object_id, array($target), 'hp_listing_category', true);
                        if (is_wp_error($set)) { return $set; }
                        if (function_exists('wp_remove_object_terms')) {
                            $removed = wp_remove_object_terms($object_id, $legacy_id, 'hp_listing_category');
                            if (is_wp_error($removed)) { return $removed; }
                        }
                        if (function_exists('update_post_meta')) { update_post_meta($object_id, '_ppar_ebay_target_term_id', $target); }
                        $legacy_reassigned++;
                    }
                }
            }
        }

        // Repair database rows that still pointed at the obsolete provider root.
        // Prefer durable listing/classification/rule evidence; use Sonstiges only as the final safe bucket.
        if ($legacy_id > 0) {
            global $wpdb;
            if (is_object($wpdb)) {
                $rows = (array) $wpdb->get_results($wpdb->prepare("SELECT * FROM {$this->ebay_items_table()} WHERE target_term_id=%d AND seller_account_type='INDIVIDUAL'", $legacy_id), ARRAY_A);
                foreach ($rows as $row) {
                    $target = $this->ebay_recover_private_target_term_id($row, $settings);
                    if ($target <= 0) { $target = absint($child_ids['sonstiges'] ?? 0); }
                    if ($target > 0) { $this->ebay_persist_recovered_private_target($row, $target); }
                }
            }
        }

        $legacy_deleted = 0;
        if ($legacy_id > 0 && function_exists('wp_delete_term')) {
            $remaining_children = function_exists('get_term_children') ? get_term_children($legacy_id, 'hp_listing_category') : array();
            $remaining_objects = function_exists('get_objects_in_term') ? get_objects_in_term($legacy_id, 'hp_listing_category') : array();
            if (!is_wp_error($remaining_children) && !is_wp_error($remaining_objects) && empty($remaining_children) && empty($remaining_objects)) {
                $deleted = wp_delete_term($legacy_id, 'hp_listing_category');
                if (is_wp_error($deleted)) { return $deleted; }
                $legacy_deleted = $deleted ? 1 : 0;
            }
        }

        if ($legacy_id > 0 && function_exists('term_exists') && term_exists('ebay-privatanzeigen', 'hp_listing_category')) {
            return new WP_Error('ebay_private_legacy_not_empty', 'Die frühere Kategorie „eBay-Privatanzeigen“ konnte noch nicht sicher entfernt werden; die Migration wird beim nächsten Lauf erneut versucht.');
        }
        update_option(self::OPTION_EBAY_PRIVATE_STRUCTURE_VERSION, '2.0', false);
        return array(
            'parent_term_id'=>$parent_id,
            'root_term_id'=>$parent_id,
            'created_children'=>$created_count,
            'moved_children'=>$moved_count,
            'legacy_reassigned'=>$legacy_reassigned,
            'legacy_deleted'=>$legacy_deleted,
        );
    }

    public function maybe_migrate_ebay_private_flat_structure() {
        if ((string) get_option(self::OPTION_EBAY_PRIVATE_STRUCTURE_VERSION, '') === '2.0') { return; }
        if (!function_exists('taxonomy_exists') || !taxonomy_exists('hp_listing_category') || !function_exists('term_exists')) { return; }
        $settings = $this->ebay_settings();
        $legacy = term_exists('ebay-privatanzeigen', 'hp_listing_category');
        // Fresh installations must not silently create a portal taxonomy. The automatic
        // migration is only for an already configured/legacy private eBay structure.
        if (!$legacy && absint($settings['private_root_term_id'] ?? 0) <= 0 && absint($settings['private_parent_term_id'] ?? 0) <= 0) { return; }
        $result = $this->ebay_setup_private_categories();
        if (is_wp_error($result)) { return; }
        update_option(self::OPTION_EBAY_PRIVATE_STRUCTURE_VERSION, '2.0', false);
    }

    public function handle_ebay_save_settings() {
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.'); }
        check_admin_referer('ppar_ebay_save_settings', 'ppar_ebay_nonce');
        $previous = $this->ebay_settings();
        $input = is_array($_POST['ppar_ebay'] ?? null) ? wp_unslash($_POST['ppar_ebay']) : array();
        $input['enabled'] = array_key_exists('enabled', $input) ? !empty($input['enabled']) : !empty($previous['enabled']);
        $input['private_enabled'] = !empty($input['private_enabled']);
        $input['private_auto_publish'] = !empty($input['private_auto_publish']);
        $input['inventory_refresh_enabled'] = !empty($input['inventory_refresh_enabled']);
        $input['business_enabled'] = !empty($input['business_enabled']);
        $input['api_terms_confirmed'] = !empty($input['api_terms_confirmed']);
        $input['privacy_policy_confirmed'] = !empty($input['privacy_policy_confirmed']);
        $secret = trim((string) ($input['client_secret'] ?? ''));
        $input['client_secret'] = $secret !== '' ? $secret : (string) ($previous['client_secret'] ?? '');
        $input['rules'] = $this->ebay_catalog_rules();
        $settings = $this->ebay_normalize_settings(array_merge($previous, $input), true);
        update_option(self::OPTION_NETWORK_EBAY, $settings, false);
        if (function_exists('delete_transient')) { delete_transient($this->ebay_token_cache_key($settings)); }
        $this->reschedule_ebay_cron(true);
        $this->reschedule_ebay_refresh_cron(true);
        wp_safe_redirect(add_query_arg(array('page'=>'affiliate-portal-ebay','ppar_ebay'=>'saved'), admin_url('admin.php')));
        exit;
    }

    public function handle_ebay_setup_categories() {
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.'); }
        check_admin_referer('ppar_ebay_setup_categories', 'ppar_ebay_nonce');
        $result = $this->ebay_setup_private_categories();
        $args = array('page'=>'affiliate-portal-ebay','ppar_ebay'=>is_wp_error($result)?'error':'categories');
        if (is_wp_error($result)) { $args['message'] = rawurlencode($result->get_error_message()); }
        wp_safe_redirect(add_query_arg($args, admin_url('admin.php')));
        exit;
    }


    public function handle_ebay_verify_catalog() {
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.'); }
        check_admin_referer('ppar_ebay_verify_catalog', 'ppar_ebay_nonce');
        $result = $this->ebay_catalog_integrity();
        $ok = !is_wp_error($result);
        $settings = $this->ebay_settings();
        if ($ok) {
            $settings['catalog_verified_sha256'] = sanitize_text_field((string) ($result['source_sha256'] ?? ''));
            $settings['catalog_verified_at'] = time();
        } else {
            $settings['catalog_verified_sha256'] = '';
            $settings['catalog_verified_at'] = 0;
        }
        update_option(self::OPTION_NETWORK_EBAY, $settings, false);
        $message = $ok
            ? sprintf('Portalabgleich PASS: %d Hauptbereiche, %d Bereichsseiten, %d Produktseiten und %d WordPress-Kategorien.', absint($result['main_hubs']), absint($result['hub_pages']), absint($result['product_pages']), absint($result['article_categories']))
            : $result->get_error_message();
        wp_safe_redirect(add_query_arg(array('page'=>'affiliate-portal-ebay','ppar_ebay'=>$ok?'catalog_passed':'error','message'=>rawurlencode($message)), admin_url('admin.php')));
        exit;
    }

    public function handle_ebay_test_connection() {
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.'); }
        check_admin_referer('ppar_ebay_test_connection', 'ppar_ebay_nonce');
        $settings = $this->ebay_settings();
        $errors = $this->ebay_configuration_errors($settings);
        if ($errors) { $result = new WP_Error('ebay_configuration_invalid', implode(' ', $errors)); }
        else {
            $result = array('tested_at'=>time(),'private'=>'disabled','business'=>'disabled');
            $seller_types = array();
            if (!empty($settings['private_enabled'])) { $seller_types[] = 'INDIVIDUAL'; }
            if (!empty($settings['business_enabled'])) { $seller_types[] = 'BUSINESS'; }
            foreach ($seller_types as $seller_type) {
                $accepted = null;
                $route_key = $seller_type === 'INDIVIDUAL' ? 'private' : 'business';
                foreach ((array) $settings['rules'] as $rule) {
                    if (empty($rule['active']) || empty($rule[$route_key])) { continue; }
                    $items = $this->ebay_search($rule, $seller_type, $settings);
                    if (is_wp_error($items)) { $result = $items; break 2; }
                    foreach ((array) $items as $raw) {
                        $candidate = $this->ebay_accept_item($raw, $seller_type, $settings);
                        if (is_wp_error($candidate)) { continue; }
                        $classification = $seller_type === 'BUSINESS'
                            ? $this->ebay_business_classify_portal_item_strict($candidate, $rule)
                            : $this->ebay_classify_portal_item($candidate, $rule);
                        if (!is_wp_error($classification)) { $accepted = array('item'=>$candidate,'classification'=>$classification,'rule'=>$rule); break 2; }
                    }
                }
                if (!$accepted) { $result = new WP_Error('ebay_no_accepted_item', 'Für ' . $seller_type . ' wurde in den automatischen Pferde-Atelier-Abrufprofilen kein fachlich eindeutig freigegebenes Angebot gefunden.'); break; }
                $result[strtolower($seller_type)] = 'pass';
            }
        }
        $settings['last_test'] = is_wp_error($result) ? array('status'=>'failed','tested_at'=>time(),'message'=>$result->get_error_message()) : array_merge(array('status'=>'pass'), $result);
        update_option(self::OPTION_NETWORK_EBAY, $settings, false);
        wp_safe_redirect(add_query_arg(array('page'=>'affiliate-portal-ebay','ppar_ebay'=>is_wp_error($result)?'test_failed':'test_passed','message'=>rawurlencode(is_wp_error($result)?$result->get_error_message():'Verbindung, Verkäuferweiche und automatischer Pferde-Atelier-Themenfilter geprüft.')), admin_url('admin.php')));
        exit;
    }

    public function handle_ebay_run_sync() {
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.'); }
        check_admin_referer('ppar_ebay_run_sync', 'ppar_ebay_nonce');
        $result = $this->run_ebay_sync(true);
        if (is_wp_error($result)) {
            $notice = 'sync_failed';
            $message = $result->get_error_message();
        } else {
            $status = sanitize_key((string) ($result['status'] ?? ''));
            $already = $status === 'already_running';
            $notice = 'sync_started';
            $message = $already
                ? 'Ein kanonischer eBay-Gesamtlauf läuft bereits; es wurde kein zweiter Lauf gestartet.'
                : 'eBay-Gesamtlauf angelegt. Der Lauf arbeitet selbstständig in begrenzten Hintergrundblöcken; die Provider-Seite kann geschlossen werden.';
        }
        wp_safe_redirect(add_query_arg(array('page'=>'affiliate-portal-ebay','ppar_ebay'=>$notice,'message'=>rawurlencode($message)), admin_url('admin.php')));
        exit;
    }

    public function handle_ebay_run_restart() {
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.'); }
        check_admin_referer('ppar_ebay_run_restart', 'ppar_ebay_nonce');
        $run=method_exists($this,'ebay_run_load')?$this->ebay_run_load():array();
        if(sanitize_key((string)($run['status']??''))!=='failed'){
            wp_safe_redirect(add_query_arg(array('page'=>'affiliate-portal-ebay','ppar_ebay'=>'error','message'=>rawurlencode('Neu starten ist nur nach einem fehlgeschlagenen Gesamtlauf möglich.')),admin_url('admin.php')));exit;
        }
        $operation=sanitize_key((string)($run['operation']??'sync'));if(!in_array($operation,array('sync','refresh'),true)){$operation='sync';}
        $result=$this->ebay_run_start(true,$operation);
        if(is_wp_error($result)){$notice='sync_failed';$message=$result->get_error_message();}
        else{$notice='sync_started';$message='Neuer Lauf gestartet. Der letzte sichere Frontend-Checkpoint bleibt aktiv, bis der neue Lauf vollständig geprüft ist.';}
        wp_safe_redirect(add_query_arg(array('page'=>'affiliate-portal-ebay','ppar_ebay'=>$notice,'message'=>rawurlencode($message)),admin_url('admin.php')));exit;
    }

    public function handle_ebay_worker_now() {
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.'); }
        check_admin_referer('ppar_ebay_worker_now', 'ppar_ebay_nonce');
        wp_safe_redirect(add_query_arg(array('page'=>'affiliate-portal-ebay','ppar_ebay'=>'sync_started','message'=>rawurlencode('Direkte Worker-Buttons sind deaktiviert. Der kanonische Hintergrundworker arbeitet selbstständig in begrenzten Blöcken.')), admin_url('admin.php')));
        exit;
    }

    /** Sequential authenticated transport for explicitly opened manual jobs; canonical workers only. */
    private function ebay_admin_manual_refresh_is_active($refresh_job = null) {
        $refresh_job = is_array($refresh_job) ? $refresh_job : $this->ebay_refresh_job_load();
        if (empty($refresh_job['manual'])) { return false; }
        return $this->ebay_refresh_job_is_open($refresh_job)
            || $this->ebay_refresh_job_is_resumable_partial($refresh_job)
            || $this->ebay_refresh_job_is_bounded_manual_partial($refresh_job);
    }

    /** Admin review approvals are explicit operator-owned selection work too.
     * They must use the same authenticated page transport instead of waiting on
     * WP-Cron while the operator is looking at a disabled/stuck status page. */
    private function ebay_admin_manual_selection_is_open($selection = null) {
        $selection = is_array($selection) ? $selection : $this->ebay_selection_state_load();
        if (!$this->ebay_selection_state_is_open($selection)) { return false; }
        $owner = sanitize_text_field((string)($selection['owner'] ?? ''));
        return $owner === 'admin' || strpos($owner, 'admin:') === 0;
    }

    private function ebay_admin_manual_refresh_selection_is_open($selection = null, $refresh_job = null) {
        $selection = is_array($selection) ? $selection : $this->ebay_selection_state_load();
        $refresh_job = is_array($refresh_job) ? $refresh_job : $this->ebay_refresh_job_load();
        if (!$this->ebay_selection_state_is_open($selection) || empty($refresh_job['manual'])) { return false; }
        $run_uuid = sanitize_text_field((string)($refresh_job['run_uuid'] ?? ''));
        $owner = sanitize_text_field((string)($selection['owner'] ?? ''));
        return $run_uuid !== '' && hash_equals('refresh:' . $run_uuid, $owner);
    }

    public function handle_ebay_run_refresh() {
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.'); }
        check_admin_referer('ppar_ebay_run_refresh', 'ppar_ebay_nonce');
        $result = $this->run_ebay_inventory_refresh(true);
        if (is_wp_error($result)) {
            $notice = 'refresh_failed';
            $message = $result->get_error_message();
        } else {
            $status = sanitize_key((string) ($result['status'] ?? ''));
            $notice = 'refresh_started';
            $message = $status === 'already_running'
                ? 'Ein eBay-Bestandsabgleich läuft bereits; es wurde kein zweiter Lauf gestartet.'
                : 'Vollständiger Bestandsabgleich gestartet: zuerst lokaler Workflow-Reconcile, danach nur fällige eBay-Angebote per getItem. Discovery bleibt aus; temporäre API-Fehler deaktivieren nichts dauerhaft.';
        }
        wp_safe_redirect(add_query_arg(array('page'=>'affiliate-portal-ebay','ppar_ebay'=>$notice,'message'=>rawurlencode($message)), admin_url('admin.php')));
        exit;
    }

    /** Authenticated same-origin transport for the one canonical eBay run.
     * The endpoint never chooses a subworker; it can only request one bounded
     * canonical tick. Lease/state-machine rules remain inside the canonical run. */
    public function handle_ebay_canonical_tick() {
        if (!current_user_can('manage_options')) { wp_send_json_error(array('message'=>'Keine Berechtigung.','code'=>'forbidden'), 403); }
        check_ajax_referer('ppar_ebay_canonical_tick', 'nonce');
        if (!method_exists($this, 'run_ebay_admin_ajax_tick')) {
            wp_send_json_error(array('message'=>'Kanonischer eBay-Transport fehlt.','code'=>'canonical_transport_missing'), 500);
        }
        $result = $this->run_ebay_admin_ajax_tick();
        if (is_wp_error($result)) {
            wp_send_json_error(array('message'=>$result->get_error_message(),'code'=>$result->get_error_code()), 409);
        }
        $run = method_exists($this,'ebay_run_load') ? $this->ebay_run_load() : array();
        $open = method_exists($this,'ebay_run_is_active') ? $this->ebay_run_is_active($run) : false;
        wp_send_json_success(array(
            'transport'=>'external_tick',
            'open'=>$open ? 1 : 0,
            'run_uuid'=>sanitize_text_field((string)($run['run_uuid'] ?? '')),
            'status'=>sanitize_key((string)($run['status'] ?? 'idle')),
            'phase'=>sanitize_key((string)($run['phase'] ?? 'idle')),
            'progress_seq'=>absint($run['progress_seq'] ?? 0),
            'last_progress_at'=>absint($run['last_progress_at'] ?? 0),
            'transport_tick_count'=>absint($run['transport_tick_count'] ?? 0),
            'no_progress_count'=>absint($run['no_progress_count'] ?? 0),
            'error_code'=>sanitize_key((string)($run['error_code'] ?? '')),
        ));
    }

    /**
     * V6.41.2 – deterministischer Seitentransport für den kanonischen Run.
     * Der Browser sendet immer erst den nächsten Request, nachdem der vorherige
     * beendet ist. Es gibt keinen Parallel-Pump, kein Self-HTTP und kein WP-Cron.
     */
    /**
     * V6.32 local-first BUSINESS recovery state. The recovery of already stored
     * BUSINESS sources must not depend on a new remote eBay discovery run. A
     * bounded local reconcile repairs source policy/classification first, then
     * the ordinary bounded BUSINESS selector rematerializes public campaigns.
     */
    private function ebay_business_local_recovery_state_load() {
        $state = get_option('ppar_ebay_business_local_recovery_state_v1', array());
        return is_array($state) ? $state : array();
    }

    private function ebay_business_local_recovery_state_save($state) {
        $state = is_array($state) ? $state : array();
        $state['updated_at'] = time();
        update_option('ppar_ebay_business_local_recovery_state_v1', $state, false);
        return $state;
    }

    private function ebay_business_local_recovery_state_current($state) {
        return is_array($state)
            && hash_equals((string) self::EBAY_RUNTIME_BUILD, (string) ($state['build'] ?? ''))
            && in_array(sanitize_key((string) ($state['status'] ?? '')), array('running','complete','failed'), true);
    }

    /** Reclassify only stored BUSINESS rows; PRIVATE is never queried or mutated. */
    private function ebay_business_local_reconcile_tick($settings = null, $limit = 25) {
        $settings = is_array($settings) ? $this->ebay_normalize_settings($settings, true) : $this->ebay_settings();
        $state = $this->ebay_business_local_recovery_state_load();
        if (!$this->ebay_business_local_recovery_state_current($state)) {
            $state = array(
                'build'=>(string) self::EBAY_RUNTIME_BUILD,
                'status'=>'running','phase'=>'reclassify','cursor'=>0,
                'scanned'=>0,'ready'=>0,'review'=>0,'blocked'=>0,'errors'=>0,
                'concepts'=>array(),'started_at'=>time(),'completed_at'=>0,
            );
            $this->ebay_business_local_recovery_state_save($state);
        }
        if (sanitize_key((string)($state['status'] ?? '')) !== 'running') { return $state; }
        global $wpdb;
        if (!is_object($wpdb) || !method_exists($wpdb,'get_results') || !method_exists($wpdb,'prepare')) {
            $state['status']='failed'; $state['phase']='failed'; $state['errors']=absint($state['errors']??0)+1;
            $state['failure_reason']='storage_unavailable';
            return $this->ebay_business_local_recovery_state_save($state);
        }
        $limit=max(1,min(50,absint($limit))); $cursor=absint($state['cursor']??0); $table=$this->ebay_items_table();
        $rows=(array)$wpdb->get_results($wpdb->prepare(
            "SELECT * FROM {$table} WHERE id>%d AND seller_account_type='BUSINESS' AND COALESCE(source_state,'available')<>'ended' ORDER BY id ASC LIMIT %d",
            $cursor,$limit
        ),ARRAY_A);
        foreach($rows as $row){
            $id=absint($row['id']??0); if($id<=0){continue;} $state['cursor']=max(absint($state['cursor']??0),$id); $state['scanned']=absint($state['scanned']??0)+1;
            $payload=json_decode((string)($row['source_payload']??''),true); $payload=is_array($payload)?$payload:array();
            $raw=is_array($payload['raw']??null)?$payload['raw']:array();
            if(!$raw){$this->ebay_maintenance_set_review_state($row,'BUSINESS',new WP_Error('ebay_business_recovery_source_missing','Gespeicherter BUSINESS-Originalpayload fehlt.'));$state['review']=absint($state['review']??0)+1;continue;}
            $policy_reason=$this->ebay_content_policy_reason(array('raw'=>$raw,'title'=>(string)($row['title']??'')));
            if($policy_reason!==''){$this->ebay_quarantine_filtered_row($row,$policy_reason);$state['blocked']=absint($state['blocked']??0)+1;continue;}
            $item=$this->ebay_accept_item($raw,'BUSINESS',$settings);
            if(is_wp_error($item)){$this->ebay_maintenance_set_review_state($row,'BUSINESS',$item);$state['review']=absint($state['review']??0)+1;continue;}
            $rule=$this->ebay_rule_by_id((string)($row['rule_id']??''),$settings);
            $classification=$this->ebay_business_classify_portal_item_strict($item,$rule);
            if(is_wp_error($classification)){
                if($this->ebay_business_preserve_last_good_on_soft_review($row,$classification)){$state['review']=absint($state['review']??0)+1;continue;}
                $this->ebay_maintenance_set_review_state($row,'BUSINESS',$classification);$state['review']=absint($state['review']??0)+1;continue;
            }
            $quality=$this->ebay_business_quality_assess($item,(array)$classification,$rule,$settings,0.0);
            if(is_wp_error($quality)){$this->ebay_business_pause_output_for_capacity($row,'quality_blocked',$quality->get_error_message());$state['review']=absint($state['review']??0)+1;continue;}
            $payload['portal_classification']=$classification; $payload['business_quality']=$quality;
            $payload['business_selection']=array('role'=>'candidate','rank'=>0,'updated_at'=>time());
            // Recovery must never tear down a currently valid public product before
            // a replacement plan has been fully materialized. Preserve a proven
            // public state here; selection performs any later displacement only
            // after all selected replacements have materialized successfully.
            $current_output=sanitize_key((string)($row['output_state']??''));
            $next_output=in_array($current_output,array('creative_ready','active_selected','review_last_good'),true)
                ? $current_output : 'candidate';
            $updates=array(
                'policy_state'=>'allowed','route_state'=>'ready','policy_version'=>self::EBAY_CONTENT_POLICY_VERSION,
                'classifier_version'=>self::EBAY_BUSINESS_CLASSIFIER_VERSION,'output_state'=>$next_output,
                'source_payload'=>wp_json_encode($payload,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES),
                'rejection_reason'=>'','updated_at'=>time(),
            );
            $wpdb->update($table,$updates,array('id'=>$id),$this->ebay_db_formats($updates),array('%d'));
            $concept=sanitize_key((string)($classification['product_concept_id']??'')); if($concept!==''){$state['concepts'][$concept]=1;}
            $state['ready']=absint($state['ready']??0)+1;
        }
        if(count($rows)<$limit){$state['status']='complete';$state['phase']='selection_needed';$state['completed_at']=time();}
        return $this->ebay_business_local_recovery_state_save($state);
    }

    private function ebay_business_local_recovery_verified($selection) {
        $selection=is_array($selection)?$selection:array();
        if(sanitize_key((string)($selection['status']??''))!=='complete' || sanitize_key((string)($selection['selection_scope']??''))!=='business'){return false;}
        $expected=absint($selection['plan_stats']['business']['active_target']??0);
        $materialized=absint($selection['stats']['business']['materialized']??0);
        $missing=absint($selection['plan_stats']['business']['missing']??0);
        // A technically successful materialization is not a supplied portal.
        // Recovery is verified only when the required physical product families
        // are represented; otherwise the next step must be targeted discovery.
        return $expected>0 && $materialized===$expected && $missing===0;
    }

    /** Hard no-progress guard for the provider-page recovery transport. */
    private function ebay_admin_progress_fingerprint($job,$refresh,$selection,$local_business,$article_rebuild=array()) {
        $payload=array(
            'job'=>array('status'=>$job['status']??'','phase'=>$job['worker_phase']??'','profile_cursor'=>absint($job['profile_cursor']??0),'requests'=>absint($job['summary']['requests']??0),'pages'=>absint($job['summary']['pages']??0),'progress'=>absint($job['progress_seq']??0)),
            'refresh'=>array('status'=>$refresh['status']??'','progress'=>absint($refresh['progress_seq']??0),'checked'=>absint($refresh['summary']['checked']??0)),
            'selection'=>array(
                'status'=>$selection['status']??'','phase'=>$selection['phase']??'',
                'bc'=>absint($selection['business_cursor']??0),'bp'=>absint($selection['business_prune_cursor']??0),'pc'=>absint($selection['private_cursor']??0),
                'bs'=>absint($selection['stats']['business']['scanned']??0),'bm'=>absint($selection['stats']['business']['materialized']??0),
                'bd'=>absint($selection['stats']['business']['deactivated']??0),'br'=>absint($selection['stats']['business']['reserve']??0),'bcan'=>absint($selection['stats']['business']['candidate']??0),
                'ps'=>absint($selection['stats']['private']['scanned']??0),'pa'=>absint($selection['stats']['private']['active']??0)
            ),
            'business_local'=>array('status'=>$local_business['status']??'','phase'=>$local_business['phase']??'','cursor'=>absint($local_business['cursor']??0),'scanned'=>absint($local_business['scanned']??0),'ready'=>absint($local_business['ready']??0)),
            'article_rebuild'=>array('status'=>$article_rebuild['status']??'','revision'=>absint($article_rebuild['revision']??0),'cursor'=>absint($article_rebuild['cursor']??0),'scanned'=>absint($article_rebuild['scanned']??0),'built'=>absint($article_rebuild['built']??0),'ready'=>absint($article_rebuild['ready']??0)),
        );
        return hash('sha256',wp_json_encode($payload));
    }

    private function ebay_admin_stall_guard($before_fingerprint,$after_fingerprint,$open_after,$kind) {
        $state=get_option('ppar_ebay_admin_stall_guard_v1',array());$state=is_array($state)?$state:array();
        if(!$open_after || $before_fingerprint!==$after_fingerprint){
            $state=array('build'=>(string)self::EBAY_RUNTIME_BUILD,'fingerprint'=>$after_fingerprint,'count'=>0,'kind'=>sanitize_key((string)$kind),'updated_at'=>time());
            update_option('ppar_ebay_admin_stall_guard_v1',$state,false);return array('stalled'=>false,'count'=>0);
        }
        $same=hash_equals((string)($state['build']??''),(string)self::EBAY_RUNTIME_BUILD) && hash_equals((string)($state['fingerprint']??''),$after_fingerprint);
        $count=$same?absint($state['count']??0)+1:1;
        $state=array('build'=>(string)self::EBAY_RUNTIME_BUILD,'fingerprint'=>$after_fingerprint,'count'=>$count,'kind'=>sanitize_key((string)$kind),'updated_at'=>time());
        update_option('ppar_ebay_admin_stall_guard_v1',$state,false);
        if($count<3){return array('stalled'=>false,'count'=>$count);}
        // Fail closed instead of reloading forever while doing zero work.
        $job=$this->ebay_sync_job_load();$refresh=$this->ebay_refresh_job_load();$selection=$this->ebay_selection_state_load();
        if($this->ebay_sync_job_is_open($job)){$job['status']='failed';$job['worker_phase']='failed_no_progress';$job['failure_reason']='admin_page_no_progress';$job['finished_at']=time();$this->ebay_sync_job_save($job);}
        elseif($this->ebay_refresh_job_is_open($refresh)){$refresh['status']='failed';$refresh['failure_reason']='admin_page_no_progress';$refresh['finished_at']=time();$this->ebay_refresh_job_save($refresh);}
        elseif($this->ebay_selection_state_is_open($selection)){$selection['status']='failed';$selection['phase']='failed';$selection['failure_reason']='admin_page_no_progress';$selection['failed_at']=time();$this->ebay_selection_state_save($selection);}
        else{$local=$this->ebay_business_local_recovery_state_load();if(sanitize_key((string)($local['status']??''))==='running'){$local['status']='failed';$local['phase']='failed';$local['failure_reason']='admin_page_no_progress';$this->ebay_business_local_recovery_state_save($local);}}
        return array('stalled'=>true,'count'=>$count);
    }

    /** V6.27 one-time BUSINESS restoration after the V6.26 scope leak. */
/**
     * V6.37 PRIVATE supply invariant for Reitstiefel. The old regression tests
     * proved classification and balancing only after synthetic boot rows already
     * existed. This live-facing invariant inspects the durable source table and
     * the actually published HivePress listings instead.
     */
    private function ebay_private_reitstiefel_supply_snapshot($settings = null) {
        $settings = is_array($settings) ? $this->ebay_normalize_settings($settings, true) : $this->ebay_settings();
        $out = array('eligible'=>0,'published'=>0,'selected'=>0,'source_item_ids'=>array(),'published_item_ids'=>array());
        global $wpdb;
        if (!is_object($wpdb) || !method_exists($wpdb,'get_results')) { return $out; }
        $table = $this->ebay_items_table();
        $rows = (array)$wpdb->get_results(
            "SELECT * FROM {$table} WHERE seller_account_type='INDIVIDUAL' AND source_state='available' AND policy_state='allowed' AND route_state='ready' AND target_term_id>0 ORDER BY last_seen DESC,id DESC LIMIT 5000",
            ARRAY_A
        );
        foreach ($rows as $row) {
            if (!is_array($row) || !$this->ebay_private_capacity_row_publishable($row,$settings)) { continue; }
            if ($this->ebay_private_capacity_concept_key($row,$settings) !== 'concept-reitstiefel') { continue; }
            $item_id = (string)($row['item_id'] ?? '');
            if ($item_id === '') { continue; }
            $out['eligible']++;
            $out['source_item_ids'][$item_id] = 1;
            $listing_id = absint($row['listing_post_id'] ?? 0);
            if ($listing_id > 0 && function_exists('get_post_status') && function_exists('get_post_meta')
                && get_post_status($listing_id) === 'publish'
                && (string)get_post_meta($listing_id,'_ppar_ebay_item_id',true) === $item_id) {
                $out['published']++;
                $out['published_item_ids'][$item_id] = $listing_id;
            }
        }
        $selection = $this->ebay_selection_state_load();
        foreach ((array)($selection['private_active'] ?? array()) as $item_id=>$flag) {
            if (isset($out['source_item_ids'][(string)$item_id])) { $out['selected']++; }
        }
        $out['source_item_ids'] = array_keys($out['source_item_ids']);
        $out['published_item_ids'] = array_keys($out['published_item_ids']);
        return $out;
    }

    private function ebay_private_reitstiefel_supply_target() { return 3; }

    private function ebay_private_reitstiefel_repair_needed($settings = null) {
        $settings = is_array($settings) ? $settings : $this->ebay_settings();
        if (empty($settings['enabled']) || empty($settings['private_enabled']) || empty($settings['private_auto_publish'])) { return false; }
        $failure = get_option('ppar_ebay_private_boot_supply_failure_v1', array());
        if (is_array($failure) && !empty($failure['build']) && hash_equals((string)self::EBAY_RUNTIME_BUILD,(string)$failure['build'])) { return false; }
        $snap = $this->ebay_private_reitstiefel_supply_snapshot($settings);
        return absint($snap['published'] ?? 0) < $this->ebay_private_reitstiefel_supply_target();
    }

    private function ebay_start_reitstiefel_supply_repair_if_needed() {
        // Deprecated symptom-repair path. Reitstiefel use the same unified
        // discovery/classification/selection model as every other product family.
        return false;
    }

    /** V6.26 one-time PRIVATE-only discovery after upgrade recovery. */
    private function ebay_private_enrichment_needed($settings = null, $selection = null) {
        return false;
    }

    private function ebay_start_private_enrichment_if_needed() {
        // Deprecated symptom-repair path. PRIVATE supply is changed only by the
        // regular 3h discovery lifecycle and explicit admin discovery.
        return false;
    }

    /** V6.31: supersede incompatible open recovery jobs from older builds.
     * A plugin update must never remain blocked behind a queued/running state
     * whose worker code and lock namespace belong to a previous runtime.
     * Manual/current-build discovery remains untouched.
     */
/** Read-only hard-cap drift check. A plugin update itself is never drift. */
    private function ebay_private_public_owned_count() {
        global $wpdb;
        if (!is_object($wpdb) || !isset($wpdb->posts) || !isset($wpdb->postmeta) || !method_exists($wpdb, 'get_var')) { return null; }
        $sql = "SELECT COUNT(DISTINCT p.ID) FROM {$wpdb->posts} p INNER JOIN {$wpdb->postmeta} pm ON pm.post_id=p.ID AND pm.meta_key='_ppar_ebay_item_id' AND pm.meta_value<>'' WHERE p.post_type='hp_listing' AND p.post_status='publish'";
        $count = $wpdb->get_var($sql);
        return $count === null ? null : max(0, (int)$count);
    }

    /** Deterministic provider-page bootstrap for the current build. */
/**
     * V6.30 deterministic provider-page driver. Executes exactly one bounded
     * workflow step in the current PHP request. This is the primary transport
     * for upgrade/recovery work and does not depend on AJAX, WP-Cron or self-HTTP.
     */
/**
     * V5.20 – Fallback-Nudge für offene Hintergrundjobs außerhalb des Browser-Pumps. Die Seite darf
     * einen offenen Job nur dann sanft erneut anstoßen, wenn seit dem letzten
     * Worker deutlich länger als ein normales Paket vergangen ist. Der
     * Transient verhindert Anstoß-Spam durch den 8s-Reload.
     */
    private function ebay_admin_nudge_open_jobs(&$job, &$refresh_job) {
        $now = time();
        $nudge_key = 'ppar_ebay_admin_nudge_v519';
        if (function_exists('get_transient') && get_transient($nudge_key)) { return; }
        $did_nudge = false;
        if ($this->ebay_sync_job_is_open($job)) {
            $last = absint($job['last_worker_at'] ?? 0);
            $updated = absint($job['updated_at'] ?? 0);
            $age = $now - max($last, $updated);
            if ($age >= 20) {
                $this->ebay_dispatch_worker($job);
                $did_nudge = true;
            }
        } elseif ($this->ebay_refresh_job_is_open($refresh_job)) {
            $last = absint($refresh_job['last_worker_at'] ?? 0);
            $updated = absint($refresh_job['updated_at'] ?? 0);
            $age = $now - max($last, $updated);
            if ($age >= 20) {
                $this->ebay_refresh_dispatch_worker($refresh_job);
                $did_nudge = true;
            }
        }
        if ($did_nudge && function_exists('set_transient')) { set_transient($nudge_key, 1, 15); }
    }

    /**
     * V5.21 – Live-Recovery fuer bereits offene V5.18–V5.20-Jobs.
     * Ein alter offener Zustand wird beim Aufruf der eBay-Adminseite terminal
     * als PARTIAL geschlossen. Bereits gespeicherte Items/Listings/Creatives
     * bleiben erhalten; es wird nichts geloescht und kein neuer Abruf gestartet.
     */
    private function ebay_admin_bound_stale_jobs(&$job, &$refresh_job, $settings) {
        if ($this->ebay_sync_job_is_open($job) && $this->ebay_sync_segment_expired($job)) {
            $this->ebay_sync_finalize($job, $settings, 'partial', 'segment_time_budget');
            $job = $this->ebay_sync_job_load();
        }
        if ($this->ebay_refresh_job_is_open($refresh_job) && $this->ebay_refresh_segment_expired($refresh_job)) {
            if (!isset($refresh_job['summary']) || !is_array($refresh_job['summary'])) { $refresh_job['summary'] = array(); }
            $refresh_job['summary']['stopped_reason'] = 'segment_time_budget';
            $this->ebay_refresh_finalize($refresh_job, $settings, 'partial');
            $refresh_job = $this->ebay_refresh_job_load();
        }
    }

    public function render_ebay_page() {
        if (!current_user_can('manage_options')) { return; }
        $settings = $this->ebay_settings();
        // Rendering is status/control only. The browser is never the canonical worker.
        $page_tick = array('kind'=>'status_transport','worker_result'=>'external_tick','stall_count'=>0);
        $canonical_run = method_exists($this,'ebay_run_load') ? $this->ebay_run_load() : array();
        $canonical_open = method_exists($this,'ebay_run_is_active') ? $this->ebay_run_is_active($canonical_run) : false;
        $canonical_status = sanitize_key((string)($canonical_run['status'] ?? 'idle'));
        $canonical_phase = sanitize_key((string)($canonical_run['phase'] ?? 'idle'));
        $canonical_coverage = is_array($canonical_run['coverage'] ?? null) ? $canonical_run['coverage'] : array();
        $canonical_routes = is_array($canonical_run['config_snapshot']['seller_routes'] ?? null) ? $canonical_run['config_snapshot']['seller_routes'] : array();
        $canonical_error_code = sanitize_key((string)($canonical_run['error_code'] ?? ''));
        $canonical_error_message = sanitize_text_field((string)($canonical_run['error_message'] ?? ''));
        $worker_transport = sanitize_key((string)($canonical_run['worker_transport'] ?? 'external_tick'));
        $external_tick_url = method_exists($this,'ebay_external_tick_url') ? $this->ebay_external_tick_url() : '';
        $worker_last_tick_at = absint($canonical_run['last_transport_tick_at'] ?? 0);
        $worker_tick_count = absint($canonical_run['transport_tick_count'] ?? 0);
        $notice = sanitize_key((string) ($_GET['ppar_ebay'] ?? ''));
        $message = sanitize_text_field(rawurldecode((string) ($_GET['message'] ?? '')));
        $rules_json = wp_json_encode($settings['rules'], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
        $test = is_array($settings['last_test'] ?? null) ? $settings['last_test'] : array();
        $sync = is_array($settings['last_sync'] ?? null) ? $settings['last_sync'] : array();
        $refresh = is_array($settings['last_refresh'] ?? null) ? $settings['last_refresh'] : array();
        $job = $this->ebay_sync_job_load();
        $refresh_job = $this->ebay_refresh_job_load();
        // Workflow V2: rendering the eBay admin page is read-only. Workers own
        // terminal state transitions; incompatible legacy jobs fail closed here.
        $job_open = $this->ebay_sync_job_is_open($job);
        $job_resumable = $this->ebay_sync_job_is_resumable_partial($job);
        $job_summary = is_array($job['summary'] ?? null) ? $job['summary'] : array();
        $refresh_open = $this->ebay_refresh_job_is_open($refresh_job);
        $refresh_resumable = $this->ebay_refresh_job_is_resumable_partial($refresh_job);
        $refresh_manual_active = $this->ebay_admin_manual_refresh_is_active($refresh_job);
        $refresh_summary = is_array($refresh_job['summary'] ?? null) ? $refresh_job['summary'] : array();
        $selection_state = $this->ebay_selection_state_load();
        $selection_open = $this->ebay_selection_state_is_open($selection_state);
        $refresh_selection_open = $this->ebay_admin_manual_refresh_selection_is_open($selection_state, $refresh_job);
        $admin_selection_open = $this->ebay_admin_manual_selection_is_open($selection_state);
        $overall_running = $canonical_open;
        $pump_running = false;
        $business_local_state=$this->ebay_business_local_recovery_state_load();
        // Page-performance invariant: normal rendering reads only bounded status
        // options. Do not rescan thousands of source rows (the old Reitstiefel
        // live snapshot alone read up to 5,000 rows on every page view).
        $media_cleanup = get_option(self::OPTION_EBAY_MEDIA_CLEANUP_STATE, array());
        $media_cleanup = is_array($media_cleanup) ? $media_cleanup : array();
        $review_candidates = $this->ebay_review_candidates(100);
        $review_targets = $this->ebay_private_review_targets($settings);
        ?>
        <div class="wrap ppar-ebay">
            <h1>eBay</h1>
            <p><strong>Runtime:</strong> <code><?php echo esc_html(self::VERSION); ?></code> · Build <code><?php echo esc_html(self::EBAY_RUNTIME_BUILD); ?></code></p>
            <p><strong>Provider-Seite: Status und Steuerung.</strong> Der Seitenaufruf führt keine BUSINESS-/PRIVATE-Fachlogik aus. Der Gesamtlauf wird ausschließlich paketweise über den Heartbeat fortgesetzt; Browser und WordPress-Cron sind dafür nicht erforderlich.</p>
            <p><strong>Automatischer Heartbeat:</strong> Für Pferde Atelier wird die vorhandene GitHub-Infrastruktur als Taktgeber verwendet; kein zusätzlicher externer Account ist erforderlich. Die Heartbeat-URL enthält keinen Geheimschlüssel und akzeptiert ausschließlich begrenzte POST-Ticks. <input type="text" class="large-text code" readonly value="<?php echo esc_attr($external_tick_url); ?>" onclick="this.select();"></p>
            <p><strong>Hintergrundarbeit:</strong> <?php echo $worker_last_tick_at ? 'letzter Block '.esc_html(wp_date('d.m.Y H:i:s',$worker_last_tick_at)) : 'noch nicht gestartet'; ?> · technische Pakete <?php echo absint($worker_tick_count); ?> · übersprungene Einzelfehler <?php echo absint($canonical_run['skipped_item_errors_count'] ?? 0); ?>. <strong>Browser kann geschlossen werden.</strong></p>
            <p><strong>Provider-Fachseite.</strong> Zugangsdaten und OAuth-Test liegen zentral unter <a href="<?php echo esc_url(admin_url('admin.php?page=affiliate-portal-networks')); ?>">Netzwerke &amp; API</a>. <?php echo $this->provider_control_badge('ebay'); ?> <a class="button button-small" href="<?php echo esc_url($this->provider_control_url('ebay')); ?>">Chefsteuerung &amp; Veto</a></p>
            <p><strong>Eingangsweiche:</strong> INDIVIDUAL → fachliche HivePress-Unterkategorien direkt unter „Private Anzeigen“ · BUSINESS → Werbemittelbibliothek und ausschließlich providerreine Produktzonen.</p>
            <p><strong>eBay-Bilder:</strong> PRIVATE-Angebote werden ab V6.12 ausschließlich über die verifizierte eBay-Bild-URL dargestellt; es werden keine neuen eBay-PRIVATE-Bilder in die WordPress-Mediathek kopiert. <strong>Legacy-Bereinigung:</strong> <?php echo esc_html((string)($media_cleanup['status'] ?? 'wartet')); ?> · gelöscht <?php echo absint($media_cleanup['deleted'] ?? 0); ?> · übersprungen <?php echo absint($media_cleanup['skipped'] ?? 0); ?> · Fehler <?php echo absint($media_cleanup['failed'] ?? 0); ?>.</p>
            <?php if ($notice === 'saved') : ?><div class="notice notice-success inline"><p>Einstellungen gespeichert.</p></div><?php endif; ?>
            <?php if (in_array($notice, array('error','test_failed','sync_failed','refresh_failed','review_failed'), true)) : ?><div class="notice notice-error inline"><p><?php echo esc_html($message ?: 'Vorgang fehlgeschlagen.'); ?></p></div><?php endif; ?>
            <?php if (in_array($notice, array('sync_started','refresh_started'), true)) : ?><div class="notice notice-info inline"><p><?php echo esc_html($message ?: 'Hintergrundvorgang gestartet.'); ?></p></div><?php endif; ?>
            <?php if (in_array($notice, array('categories','catalog_passed','test_passed','sync_passed','review_saved'), true)) : ?><div class="notice notice-success inline"><p><?php echo esc_html($message ?: 'Vorgang abgeschlossen.'); ?></p></div><?php endif; ?>

            <section class="postbox" style="padding:18px;max-width:1180px">
                <h2>1. HivePress-Bereich einrichten</h2>
                <p>Erstellt beziehungsweise prüft <strong>Private Anzeigen</strong> und darunter direkt die acht fachlichen Unterkategorien. Die frühere sichtbare Provider-Ebene „eBay-Privatanzeigen“ wird automatisch und ohne Verlust der Listing-Zuordnungen entfernt.</p>
                <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>">
                    <input type="hidden" name="action" value="ppar_ebay_setup_categories">
                    <?php wp_nonce_field('ppar_ebay_setup_categories', 'ppar_ebay_nonce'); ?>
                    <button class="button button-secondary">Private-Anzeigen-Kategorien anlegen/prüfen</button>
                    <?php if (!empty($settings['private_root_term_id'])) : ?><span style="margin-left:10px">Private-Anzeigen-ID: <?php echo absint($settings['private_root_term_id']); ?></span><?php endif; ?>
                </form>
            </section>

            <section class="postbox" style="padding:18px;max-width:1180px">
                <h2>2. Portal- und Themenabgleich prüfen</h2>
                <p>Prüft den fest mitgelieferten vollständigen Pferde-Atelier-Zielkatalog: 8 Hauptbereiche, 59 Bereichsseiten, 329 Produktseiten und 1.124 WordPress-Kategorien. Ohne positiven Abgleich bleiben Provider-Fachtest und Abruf fail-closed.</p>
                <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>">
                    <input type="hidden" name="action" value="ppar_ebay_verify_catalog">
                    <?php wp_nonce_field('ppar_ebay_verify_catalog', 'ppar_ebay_nonce'); ?>
                    <button class="button button-secondary">Portal- und Themenabgleich prüfen</button>
                    <?php if (!empty($settings['catalog_verified_at'])) : ?><span style="margin-left:10px">Status: geprüft am <?php echo esc_html(wp_date('d.m.Y H:i', absint($settings['catalog_verified_at']))); ?></span><?php endif; ?>
                </form>
            </section>

            <section class="postbox" style="padding:18px;max-width:1180px">
                <h2>3. Betriebsprofil und automatische Abrufprofile</h2>
                <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>">
                    <input type="hidden" name="action" value="ppar_ebay_save_settings">
                    <?php wp_nonce_field('ppar_ebay_save_settings', 'ppar_ebay_nonce'); ?>
                    <table class="form-table" role="presentation"><tbody>
                        <tr><th>Zentraler Zugang</th><td><?php echo !empty($settings['enabled']) ? '<strong>aktiviert</strong>' : '<strong>deaktiviert</strong>'; ?> · Umgebung: <strong><?php echo esc_html((string)$settings['environment']); ?></strong><p class="description">Client-ID, Client-Secret, EPN-Campaign-ID, Aktivierung und OAuth-Test werden ausschließlich unter <a href="<?php echo esc_url(admin_url('admin.php?page=affiliate-portal-networks')); ?>">Netzwerke &amp; API</a> verwaltet.</p></td></tr>
                        <tr><th>Liefer-PLZ</th><td><input class="small-text" name="ppar_ebay[delivery_postal_code]" value="<?php echo esc_attr((string) $settings['delivery_postal_code']); ?>"><p class="description">Optional für präzisere Versandinformationen.</p></td></tr>
                        <tr><th>Private Verkäufer</th><td><label><input type="checkbox" name="ppar_ebay[private_enabled]" value="1" <?php checked(!empty($settings['private_enabled'])); ?>> INDIVIDUAL abrufen</label><p class="description">Fachlich eindeutige Angebote werden als HivePress-Listings angelegt; weiche Unsicherheiten landen im Prüfbestand statt verworfen zu werden.</p></td></tr>
                        <tr><th>Automatische Veröffentlichung</th><td><label><input type="checkbox" name="ppar_ebay[private_auto_publish]" value="1" <?php checked(!empty($settings['private_auto_publish'])); ?>> Fachlich sichere INDIVIDUAL-Angebote direkt veröffentlichen</label><p class="description"><strong>Standard nach Update: aus.</strong> Bereits manuell veröffentlichte eBay-Listings bleiben bei späteren Abrufen veröffentlicht. Prüfbestand wird niemals automatisch veröffentlicht.</p></td></tr>
                        <tr><th>PRIVATE-Ausgabe</th><td><span class="description">Fachlich sichere automatisch veröffentlichte eBay-Privatanzeigen erscheinen in ihrer zugewiesenen HivePress-Unterkategorie mit normaler Pagination. Die Parent-Seite „Private Anzeigen“ bleibt fest auf maximal 9 Karten begrenzt.</span></td></tr>
                        <tr><th>PRIVATE-Obergrenze</th><td><input class="small-text" type="number" min="50" max="250" name="ppar_ebay[private_active_cap]" value="<?php echo absint($settings['private_active_cap']); ?>"> aktiv gesamt · <input class="small-text" type="number" min="5" max="100" name="ppar_ebay[private_leaf_cap]" value="<?php echo absint($settings['private_leaf_cap']); ?>"> je Leaf<p class="description">Standard: 250 aktiv gesamt. Der Leaf-Wert 30 ist das faire Erstverteilungsziel je unterster Kategorie; bleiben andere Bereiche unterversorgt, wird ausschließlich mit weiteren fachlich sicheren Kandidaten bis zum globalen Cap nachgefüllt. Überschuss bleibt im eBay-Rohbestand und erzeugt keinen unnötigen HivePress-Post; bereits materialisierte Überkapazität wird auf Entwurf gesetzt, nicht gelöscht.</p></td></tr>
                        <tr><th>Bestandsabgleich</th><td><label><input type="checkbox" name="ppar_ebay[inventory_refresh_enabled]" value="1" <?php checked(!empty($settings['inventory_refresh_enabled'])); ?>> Vor Ablauf der 6-Stunden-Frist vorhandene eBay-Angebote gezielt per Browse <code>getItem</code> nachprüfen</label><p class="description">Unauffindbar/verkauft/beendet → Frontend aus. Temporärer API-Fehler → keine Löschung; der Datensatz bleibt intern erhalten und wird später erneut geprüft.</p></td></tr>
                        <tr><th>Bestandschecks je Lauf</th><td><input class="small-text" type="number" min="1200" max="2000" name="ppar_ebay[inventory_refresh_max_per_run]" value="<?php echo absint($settings['inventory_refresh_max_per_run']); ?>"><p class="description">Automatisch mindestens 1.200 Checks; der Bestandsabgleich läuft stündlich, Discovery weiterhin alle drei Stunden. Keine Änderung erforderlich.</p></td></tr>
                        <tr><th>Gewerbliche Verkäufer</th><td><label><input type="checkbox" name="ppar_ebay[business_enabled]" value="1" <?php checked(!empty($settings['business_enabled'])); ?>> BUSINESS als Produkt-Creatives übernehmen</label></td></tr>
                        <tr><th>BUSINESS-Auswahl</th><td><input class="small-text" type="number" min="30" max="1000" name="ppar_ebay[business_active_cap]" value="<?php echo absint($settings['business_active_cap']); ?>"> aktiv gesamt · <strong>max. 3 je passender Seite</strong><br><input class="small-text" type="number" min="5" max="20" name="ppar_ebay[business_candidate_pool_per_concept]" value="<?php echo absint($settings['business_candidate_pool_per_concept']); ?>"> Kandidaten je Produktkonzept · <input class="small-text" type="number" min="0" max="5" name="ppar_ebay[business_reserve_per_concept]" value="<?php echo absint($settings['business_reserve_per_concept']); ?>"> Reserven<p class="description">Harte Sicherheitsgrenze: 1000 aktive BUSINESS-Produkte portalweit; durch max. 3 je Produktkonzept liegt der aktuelle Katalog rechnerisch bei höchstens 933. Top 10 je Produktkonzept, 2 interne Nachrücker. Verkäuferdiversität wird bevorzugt; freie Plätze dürfen mit weiteren unterschiedlichen qualifizierten Angeboten desselben Verkäufers gefüllt werden.</p></td></tr>
                        <tr><th>Verkäuferqualität</th><td>Minimum <input class="small-text" type="number" step="0.1" min="95" max="100" name="ppar_ebay[business_min_feedback_percentage]" value="<?php echo esc_attr((string)$settings['business_min_feedback_percentage']); ?>"> % positiv und <input class="small-text" type="number" min="1" name="ppar_ebay[business_min_feedback_score]" value="<?php echo absint($settings['business_min_feedback_score']); ?>"> Bewertungen. Bevorzugt ab <input class="small-text" type="number" step="0.1" min="95" max="100" name="ppar_ebay[business_preferred_feedback_percentage]" value="<?php echo esc_attr((string)$settings['business_preferred_feedback_percentage']); ?>"> % / <input class="small-text" type="number" min="1" name="ppar_ebay[business_preferred_feedback_score]" value="<?php echo absint($settings['business_preferred_feedback_score']); ?>"> Bewertungen.</td></tr>
                        <tr><th>Vertragsbestätigung</th><td><label><input type="checkbox" name="ppar_ebay[api_terms_confirmed]" value="1" <?php checked(!empty($settings['api_terms_confirmed'])); ?>> Aktuelle eBay-API-, Buy-API- und EPN-Verträge sind akzeptiert und das Portal ist als Anwendung/Media Property angegeben.</label></td></tr>
                        <tr><th>Datenschutz und Kennzeichnung</th><td><label><input type="checkbox" name="ppar_ebay[privacy_policy_confirmed]" value="1" <?php checked(!empty($settings['privacy_policy_confirmed'])); ?>> Datenschutzerklärung, Affiliate-Kennzeichnung und Löschpflichten sind umgesetzt.</label></td></tr>
                        <tr><th>Aktualitätsgrenze</th><td><strong>6 Stunden</strong><input type="hidden" name="ppar_ebay[stale_hours]" value="6"><p class="description">Fest erzwungen: öffentlich angezeigte eBay-Angebotsdaten dürfen höchstens sechs Stunden alt sein. Danach wird nur die öffentliche Ausgabe fail-closed ausgeblendet; der HivePress-Status bleibt unverändert. Erst ein bestätigtes eBay-Endsignal deaktiviert das Listing.</p></td></tr>
                        <tr><th>Treffer pro Seite</th><td><input class="small-text" type="number" min="1" max="50" name="ppar_ebay[max_per_rule]" value="<?php echo absint($settings['max_per_rule']); ?>"><p class="description">eBay Browse API: maximal 50 Treffer je Seite.</p></td></tr>
                        <tr><th>Max. Seiten je Abrufprofil</th><td><input class="small-text" type="number" min="1" max="20" name="ppar_ebay[max_pages_per_profile]" value="<?php echo absint($settings['max_pages_per_profile']); ?>"></td></tr>
                        <tr><th>Max. Requests je Arbeitspaket</th><td><input class="small-text" type="number" min="1" max="40" name="ppar_ebay[max_requests_per_run]" value="<?php echo absint($settings['max_requests_per_run']); ?>"><p class="description">Harte Hintergrundgrenze pro Arbeitspaket. Ein vollständiger Discovery-Lauf setzt danach automatisch am nächsten Profil fort, bis der komplette Katalog einmal abgedeckt ist.</p></td></tr>
                        <tr><th>Zeitbudget je Hintergrundpaket</th><td><input class="small-text" type="number" min="10" max="30" name="ppar_ebay[run_time_budget_seconds]" value="<?php echo absint($settings['run_time_budget_seconds']); ?>"> Sekunden<p class="description">Der Gesamtlauf hat kein synchrones Browser-Zeitlimit mehr. Dieses Budget begrenzt nur ein einzelnes fortsetzbares Arbeitspaket.</p></td></tr>
                        <tr><th>Automatische Abrufprofile</th><td><textarea rows="28" class="large-text code" readonly><?php echo esc_textarea((string) $rules_json); ?></textarea><p class="description">Nur lesbar. Die fachliche Annahme und Zielzuordnung erfolgt automatisch gegen den vollständigen Pferde-Atelier-Zielkatalog; Suchbegriffe allein reichen niemals zur Freigabe.</p></td></tr>
                    </tbody></table>
                    <?php submit_button('eBay-Betriebsprofil speichern'); ?>
                </form>
            </section>

            <?php if ((string)($canonical_run['schema'] ?? '') === '1.0') : ?>
            <section class="postbox" style="padding:18px;max-width:1180px;border-left:4px solid <?php echo $canonical_status==='completed'?'#46b450':($canonical_status==='failed'?'#d63638':'#dba617'); ?>">
                <h2>Kanonischer Gesamtworkflow</h2>
                <?php $canonical_label=$canonical_status==='running'?'Läuft':($canonical_status==='paused'?'Pausiert':($canonical_status==='failed'?'Fehlgeschlagen':($canonical_status==='completed'?(!empty($canonical_run['completed_with_skips'])?'Fertig (mit übersprungenen Fehlern)':'Fertig'):'Wartet'))); ?>
                <p><strong>Status:</strong> <strong><?php echo esc_html($canonical_label); ?></strong> · Run <code><?php echo esc_html(substr((string)($canonical_run['run_uuid'] ?? ''),0,12)); ?></code>
                · Etage <code><?php echo esc_html($canonical_phase ?: 'idle'); ?></code>
                · letzter echter Fortschritt <?php echo !empty($canonical_run['last_progress_at']) ? esc_html(wp_date('d.m.Y H:i:s',absint($canonical_run['last_progress_at']))) : '—'; ?>.</p>
                <?php if($canonical_status==='paused'): ?><p><strong>Sauber pausiert.</strong> Der sichere Frontend-Stand bleibt aktiv. Automatische Fortsetzung <?php echo !empty($canonical_run['resume_at'])?esc_html(wp_date('d.m.Y H:i:s',absint($canonical_run['resume_at']))):'in Kürze'; ?>.</p><?php endif; ?>
                <p><strong>Lease:</strong> <?php echo !empty($canonical_run['owner']) ? '<code>'.esc_html((string)$canonical_run['owner']).'</code>' : 'frei'; ?>
                · Ablauf <?php echo !empty($canonical_run['lease_expires_at']) ? esc_html(wp_date('d.m.Y H:i:s',absint($canonical_run['lease_expires_at']))) : '—'; ?>
                · Nullfortschritt <?php echo absint($canonical_run['no_progress_count'] ?? 0); ?>/3
                <?php if (!empty($canonical_run['resume_reason'])) : ?>· Checkpoint <code><?php echo esc_html((string)$canonical_run['resume_reason']); ?></code><?php endif; ?>.</p>
                <p><strong>Worker-Transport:</strong> <code><?php echo esc_html((string)($canonical_run['worker_transport'] ?? 'external_tick')); ?></code> · letzter Tick <?php echo $worker_last_tick_at ? esc_html(wp_date('d.m.Y H:i:s',$worker_last_tick_at)) : '—'; ?> · Pakete <?php echo absint($worker_tick_count); ?>.</p>
                <p><strong>Seller-Routen-Snapshot:</strong> PRIVATE <?php echo !empty($canonical_routes['private'])?'aktiv':'deaktiviert'; ?> · BUSINESS <?php echo !empty($canonical_routes['business'])?'aktiv':'deaktiviert'; ?>.</p>
                <?php if (!empty($canonical_routes['business'])) : ?><p><strong>BUSINESS-Fortschritt:</strong> <?php echo absint($canonical_coverage['covered'] ?? 0); ?>/<?php echo absint($canonical_coverage['required'] ?? 311); ?> · fehlend <?php echo count((array)($canonical_coverage['missing'] ?? array())); ?>.</p><?php endif; ?>
                <?php if ($canonical_status === 'failed') : ?><div class="notice notice-error inline"><p><strong>Gesamtlauf FEHLER:</strong> <code><?php echo esc_html($canonical_error_code ?: 'error_code_missing'); ?></code> · <?php echo esc_html($canonical_error_message ?: 'Fehlertext fehlt im persistenten Run-State.'); ?></p>
                <?php
                    // Read-only diagnostic. No workflow/state mutation. Surfaces the
                    // exact failed sub-phase and recovery history, which the short
                    // status lines elsewhere on this page intentionally omit.
                    $ppar_dbg_errors = is_array($canonical_run['errors'] ?? null) ? $canonical_run['errors'] : array();
                    $ppar_dbg_last = !empty($ppar_dbg_errors) ? end($ppar_dbg_errors) : array();
                    $ppar_dbg_phase = sanitize_key((string)(is_array($ppar_dbg_last['details'] ?? null) ? ($ppar_dbg_last['details']['phase'] ?? '') : ''));
                    $ppar_dbg_history = is_array($canonical_run['recovery_history'] ?? null) ? $canonical_run['recovery_history'] : array();
                    $ppar_dbg_details = is_array($ppar_dbg_last['details'] ?? null) ? $ppar_dbg_last['details'] : array();
                    $ppar_dbg_build = sanitize_text_field((string)($ppar_dbg_details['build'] ?? $canonical_run['build'] ?? ''));
                    $ppar_dbg_progress_contract = sanitize_text_field((string)($ppar_dbg_details['progress_contract_version'] ?? $canonical_run['progress_contract_version'] ?? ''));
                    $ppar_dbg_sel_for_errors = is_array($canonical_run['phase_state']['selection'] ?? null) ? $canonical_run['phase_state']['selection'] : array();
                    $ppar_dbg_business_errors = is_array($ppar_dbg_sel_for_errors['stats']['business']['errors'] ?? null) ? $ppar_dbg_sel_for_errors['stats']['business']['errors'] : array();
                    $ppar_dbg_business_codes = array();
                    foreach(array_slice($ppar_dbg_business_errors,0,5) as $ppar_dbg_error){$ppar_dbg_code=sanitize_key((string)($ppar_dbg_error['code']??''));if($ppar_dbg_code!==''){$ppar_dbg_business_codes[$ppar_dbg_code]=1;}}
                ?>
                <p class="description"><strong>Debug (rein lesend):</strong> fehlgeschlagene Phase <code><?php echo esc_html($ppar_dbg_phase ?: 'unbekannt'); ?></code> · Build zum Fehlzeitpunkt <code><?php echo esc_html($ppar_dbg_build ?: 'unbekannt'); ?></code> · Progress-Contract <code><?php echo esc_html($ppar_dbg_progress_contract ?: 'legacy/unbekannt'); ?></code> · Recovery-Versuche gesamt <?php echo absint(count($ppar_dbg_history)); ?><?php if (!empty($ppar_dbg_history)) : $ppar_dbg_h = end($ppar_dbg_history); ?> · letzter Recovery-Grund <code><?php echo esc_html((string)($ppar_dbg_h['reason'] ?? '')); ?></code><?php endif; ?><?php if(!empty($ppar_dbg_business_codes)): ?> · BUSINESS-Fehlercodes <code><?php echo esc_html(implode(',',array_keys($ppar_dbg_business_codes))); ?></code><?php endif; ?>.
                <?php if (!empty($canonical_run['phase_state']['selection'])) : $ppar_dbg_sel = $canonical_run['phase_state']['selection']; ?>
                · Selection-Status <code><?php echo esc_html(sanitize_key((string)($ppar_dbg_sel['status'] ?? ''))); ?></code>
                · Selection-Phase <code><?php echo esc_html(sanitize_key((string)($ppar_dbg_sel['phase'] ?? ''))); ?></code>
                · prepare_private_scanned <?php echo absint($ppar_dbg_sel['prepare_private_scanned'] ?? 0); ?>
                · prepare_private_leaf_index <?php echo absint($ppar_dbg_sel['prepare_private_leaf_index'] ?? 0); ?>
                <?php endif; ?></p>
                <?php if(!empty($canonical_run['checkpoint_safe'])): ?><p><strong>Sicherer Frontend-Stand:</strong> bleibt unverändert aktiv.</p><?php endif; ?>
                <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>" style="margin-top:10px"><input type="hidden" name="action" value="ppar_ebay_run_restart"><?php wp_nonce_field('ppar_ebay_run_restart','ppar_ebay_nonce'); ?><button class="button button-primary">Lauf neu starten</button></form>
                </div><?php endif; ?>
                <?php if ($canonical_status === 'completed') : ?><div class="notice notice-success inline"><p><strong>Gesamtlauf abgeschlossen:</strong> neue Etage vollständig geprüft und als sicherer Frontend-Checkpoint übernommen.</p></div><?php endif; ?>
                <?php if ($canonical_open) : ?><p class="description"><strong>Startaktionen gesperrt:</strong> genau dieser Run ist aktiv. Der externe Taktgeber setzt ihn paketweise fort; die Seite kann geschlossen werden.</p><?php endif; ?>
            </section>
            <?php endif; ?>

            <?php if (!empty($selection_state)) : $selection_status=sanitize_key((string)($selection_state['status'] ?? '')); $private_stats=is_array($selection_state['stats']['private']??null)?$selection_state['stats']['private']:array(); $business_stats=is_array($selection_state['stats']['business']??null)?$selection_state['stats']['business']:array(); ?>
            <section class="postbox" style="padding:18px;max-width:1180px;border-left:4px solid <?php echo $selection_status==='complete'?'#46b450':($selection_status==='failed'?'#d63638':'#dba617'); ?>">
                <h2>Auswahl-/Materialisierungs-Teilstatus</h2>
                <p><strong>Status:</strong> <span id="ppar-private-recovery-status"><?php echo esc_html((string)($selection_state['status'] ?? 'wartet')); ?></span>
                · Phase <code><?php echo esc_html((string)($selection_state['phase'] ?? '')); ?></code>
                · Kandidatenpool <?php echo absint($selection_state['plan_stats']['private']['scanned'] ?? 0); ?>/<?php echo absint($selection_state['plan_stats']['private']['candidate_limit'] ?? 0); ?> max. geprüft
                · Gewinner verarbeitet <?php echo absint($private_stats['scanned'] ?? 0); ?>/<?php echo absint($private_stats['selected_total'] ?? ($selection_state['plan_stats']['private']['active_target'] ?? 0)); ?>
                · veröffentlicht <?php echo absint($private_stats['active'] ?? 0); ?>
                · deaktiviert <?php echo absint($private_stats['deactivated'] ?? 0); ?>.</p>
                <p><strong>BUSINESS-Fortschritt:</strong> Quellen geprüft <?php echo absint($business_stats['scanned'] ?? 0); ?>
                · aktiv <?php echo absint($business_stats['active'] ?? 0); ?>
                · materialisiert <?php echo absint($business_stats['materialized'] ?? 0); ?>
                · Reserve <?php echo absint($business_stats['reserve'] ?? 0); ?>
                · deaktiviert <?php echo absint($business_stats['deactivated'] ?? 0); ?>.</p>
                <?php $business_plan_stats=is_array($selection_state['plan_stats']['business']??null)?$selection_state['plan_stats']['business']:array(); ?>
                <p><strong>BUSINESS-Katalogabdeckung:</strong> <?php echo absint($business_plan_stats['covered'] ?? 0); ?>/<?php echo absint($business_plan_stats['required'] ?? 0); ?> physische Produktfamilien versorgt
                · <?php echo absint($business_plan_stats['missing'] ?? 0); ?> fehlen.
                <span class="description">Dies ist nur der interne Auswahlplan. Verbindlich ist ausschließlich die öffentliche Coverage des kanonischen Gesamtworkflows.</span></p>
                <p><strong>Lokaler BUSINESS-Recovery:</strong> <?php echo esc_html((string)($business_local_state['status'] ?? 'wartet')); ?>
                · Phase <code><?php echo esc_html((string)($business_local_state['phase'] ?? '')); ?></code>
                · gespeicherte Quellen geprüft <?php echo absint($business_local_state['scanned'] ?? 0); ?>
                · wieder bereit <?php echo absint($business_local_state['ready'] ?? 0); ?>
                · Review <?php echo absint($business_local_state['review'] ?? 0); ?>
                · blockiert <?php echo absint($business_local_state['blocked'] ?? 0); ?>.
                <span class="description">Provider-Seite: keine eigene Recovery-Logik; ein offener Gesamt-Run wird ausschließlich über den kanonischen Admin-AJAX-Tick fortgesetzt.</span></p>
                <p class="description"><strong>Kategorieversorgung:</strong> wird ausschließlich aus dem letzten Hintergrund-Auswahlplan berichtet. Die Provider-Seite führt keine produktbezogene Sonderprüfung und keinen 5.000-Zeilen-Livescan aus.</p>
                <p><strong>Realer Post-Check:</strong> verifiziert öffentlich eBay <strong><?php echo absint($selection_state['verified_public_private'] ?? $private_stats['verified_public'] ?? 0); ?></strong>
                · normale HivePress-Anzeigen gesehen <?php echo absint($selection_state['verified_native_public'] ?? $private_stats['native_seen'] ?? 0); ?>
                · Legacy-eBay erkannt <?php echo absint($private_stats['legacy_owned_seen'] ?? 0); ?>
                · harte Negativtreffer deaktiviert <?php echo absint($private_stats['hard_negative_deactivated'] ?? 0); ?>.</p>
                <?php if ($selection_open) : ?><p><strong>Selection-Teilphase offen.</strong> Ausschließlich derselbe kanonische Gesamt-Run setzt sie über den sequenziellen Admin-AJAX-Transport fort.</p><?php endif; ?>
                <?php if ($selection_status === 'complete') : ?><div class="notice notice-info inline"><p><strong>Selection-Teilphase abgeschlossen.</strong> Das ist ausdrücklich noch kein Gesamt-PASS; Coverage und Public-Gate des kanonischen Runs sind danach verpflichtend.</p></div><?php endif; ?>
                <?php if ($selection_status === 'failed') : ?><div class="notice notice-error inline"><p><strong>Selection FEHLER:</strong> <?php echo esc_html((string)($selection_state['error'] ?? $selection_state['failure_reason'] ?? 'selection_error_code_missing')); ?></p></div><?php endif; ?>
            </section>
            <?php endif; ?>

            <section class="postbox" style="padding:18px;max-width:1180px">
                <h2>4. Provider-Fachtest und Abruf</h2>
                <p>Der reine OAuth-Zugangstest liegt zentral unter „Netzwerke &amp; API“. Dieser Fachtest prüft zusätzlich EBAY_DE, itemAffiliateWebUrl, die Verkäuferkontotypen INDIVIDUAL/BUSINESS und den Portalfilter. Der vollständige Abruf folgt eBays Pagination über <code>next</code> und läuft seit V5.6.0 ausschließlich als fortsetzbarer Hintergrundjob; der Admin-Klick wartet nicht mehr auf den Gesamtlauf.</p>
                <div style="display:flex;gap:10px;flex-wrap:wrap">
                    <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>"><input type="hidden" name="action" value="ppar_ebay_test_connection"><?php wp_nonce_field('ppar_ebay_test_connection', 'ppar_ebay_nonce'); ?><button class="button button-secondary">Provider-Fachtest starten</button></form>
                    <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>"><input type="hidden" name="action" value="ppar_ebay_run_sync"><?php wp_nonce_field('ppar_ebay_run_sync', 'ppar_ebay_nonce'); ?><button class="button button-primary" <?php disabled($canonical_open); ?>><?php echo $canonical_open ? 'Gesamtlauf läuft …' : 'Vollständigen eBay-Abruf starten'; ?></button></form>
                    <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>"><input type="hidden" name="action" value="ppar_ebay_run_refresh"><?php wp_nonce_field('ppar_ebay_run_refresh', 'ppar_ebay_nonce'); ?><button class="button button-secondary" <?php disabled($canonical_open || empty($settings['inventory_refresh_enabled'])); ?>><?php echo $canonical_open ? 'Gesamtlauf läuft …' : 'Bestand jetzt abgleichen'; ?></button></form>
                </div>
                <p class="description"><strong>Bestand jetzt abgleichen</strong> ist ein kompletter Reconcile-Lauf: zuerst lokale Policy/Klassifikation und bestehende PRIVATE/BUSINESS-Ausgaben auf den aktuellen Workflow-Vertrag bringen, danach ausschließlich fällige eBay-Angebote per <code>getItem</code> prüfen. <strong>Discovery wird dabei nicht gestartet.</strong></p>
                <?php if ($job_resumable && !$job_open && !$refresh_manual_active) : ?>
                    <p><strong>Discovery:</strong> Zeitsegment sauber beendet. Alle bereits verarbeiteten Ergebnisse sind gespeichert. Mit <em>eBay-Abruf fortsetzen</em> wird exakt am gespeicherten Cursor weitergearbeitet.</p>
                <?php endif; ?>
                <?php if ($canonical_open) : ?>
                    <p><strong>Gesamtvorgang:</strong> läuft · Run <code><?php echo esc_html(substr((string)($canonical_run['run_uuid'] ?? ''),0,12)); ?></code> · Phase <code><?php echo esc_html($canonical_phase); ?></code>. Die Seite taktet ausschließlich diesen einen kanonischen Run; es wird kein zweiter Worker erzeugt.</p>
                <?php elseif ($canonical_status === 'completed') : ?>
                    <p><strong>Gesamtvorgang:</strong> abgeschlossen – kanonischer Run hat Coverage- und Public-Gate erreicht.</p>
                <?php elseif ($canonical_status === 'failed') : ?>
                    <p><strong>Gesamtvorgang:</strong> fehlgeschlagen · <code><?php echo esc_html($canonical_error_code ?: 'error_code_missing'); ?></code>.</p>
                <?php elseif ($sync || $refresh) : ?>
                    <p><strong>Historischer Teilstatus vorhanden.</strong> Er wird nicht als aktueller Gesamtabschluss gewertet.</p>
                <?php endif; ?>
                <?php if ($job_open) : ?>
                    <p><strong>Hintergrundlauf:</strong> läuft · Phase <code><?php echo esc_html((string)($job['worker_phase'] ?? '')); ?></code> · Requests gesamt <?php echo absint($job_summary['requests'] ?? 0); ?> · aktuelles Paket <?php echo absint($job['requests_in_batch'] ?? 0); ?>/<?php echo absint($settings['max_requests_per_run']); ?> · Pakete <?php echo absint($job_summary['request_batches'] ?? 1); ?> · Seiten <?php echo absint($job_summary['pages'] ?? 0); ?> · gefunden <?php echo absint($job_summary['received'] ?? 0); ?> · fachlich sicher <?php echo absint($job_summary['accepted'] ?? 0); ?> · Prüfbestand <?php echo absint($job_summary['review_pending'] ?? 0); ?>. <span class="description">Letztes Arbeitspaket: <?php echo !empty($job['last_worker_at']) ? esc_html(wp_date('d.m.Y H:i:s', absint($job['last_worker_at']))) : 'noch nicht gestartet'; ?></span></p>
                <?php endif; ?>
                <?php if ($refresh_manual_active) : $refresh_maint = is_array($refresh_summary['maintenance'] ?? null) ? $refresh_summary['maintenance'] : array(); $refresh_phase = sanitize_key((string)($refresh_summary['phase'] ?? 'source_refresh')); ?>
                    <p><strong>Bestandsabgleich:</strong> läuft · Phase <strong><?php echo $refresh_phase === 'local_reconciliation' ? 'lokaler Workflow-Abgleich' : 'eBay-Bestandsprüfung'; ?></strong> · lokal <?php echo absint($refresh_maint['scanned'] ?? 0); ?> geprüft / <?php echo absint($refresh_maint['ready_private'] ?? 0); ?> PRIVATE / <?php echo absint($refresh_maint['ready_business'] ?? 0); ?> BUSINESS · eBay <?php echo absint($refresh_summary['checked'] ?? 0); ?> geprüft / <?php echo absint($refresh_summary['available'] ?? 0); ?> aktiv / <?php echo absint($refresh_summary['ended'] ?? 0); ?> beendet · technische Fehler <?php echo absint($refresh_summary['technical_errors'] ?? 0); ?>. <span class="description">Letztes Arbeitspaket: <?php echo !empty($refresh_job['last_worker_at']) ? esc_html(wp_date('d.m.Y H:i:s', absint($refresh_job['last_worker_at']))) : 'noch nicht gestartet'; ?></span></p>
                <?php endif; ?>
                <?php if ($refresh_selection_open || $admin_selection_open) : $sel_stats=is_array($selection_state['stats']??null)?$selection_state['stats']:array(); $sel_business=is_array($sel_stats['business']??null)?$sel_stats['business']:array(); $sel_private=is_array($sel_stats['private']??null)?$sel_stats['private']:array(); $sel_phase=sanitize_key((string)($selection_state['phase']??'')); $sel_bp=is_array($selection_state['plan_stats']['business_prepare']??null)?$selection_state['plan_stats']['business_prepare']:array(); $sel_pp=is_array($selection_state['plan_stats']['private_prepare']??null)?$selection_state['plan_stats']['private_prepare']:array(); ?>
                    <p><strong><?php echo $refresh_selection_open ? 'Bestandsabgleich – Auswahl' : 'Manuelle Auswahl'; ?>:</strong> läuft · Phase <code><?php echo esc_html((string)($selection_state['phase']??'')); ?></code><?php if($sel_phase==='prepare'): ?> · Vorbereitung BUSINESS <?php echo absint($sel_bp['completed_concepts']??0); ?>/<?php echo absint($sel_bp['required_concepts']??0); ?> Konzepte · PRIVATE geprüft <?php echo absint($sel_pp['scanned']??$selection_state['prepare_private_scanned']??0); ?> · Leafs <?php echo absint($sel_pp['leaves_complete']??$selection_state['prepare_private_leaf_index']??0); ?>/<?php echo absint($sel_pp['leaves_total']??count((array)($selection_state['prepare_private_leaf_ids']??array()))); ?> · geeignet <?php echo absint($sel_pp['eligible']??count((array)($selection_state['prepare_private_eligible']??array()))); ?>/<?php echo absint($sel_pp['candidate_limit']??$selection_state['prepare_private_candidate_limit']??0); ?><?php endif; ?> · BUSINESS geprüft <?php echo absint($sel_business['scanned']??0); ?> / materialisiert <?php echo absint($sel_business['materialized']??0); ?> · PRIVATE geprüft <?php echo absint($sel_private['scanned']??0); ?> / materialisiert <?php echo absint($sel_private['materialized']??0); ?>.</p>
                <?php endif; ?>
                <?php if ($overall_running) : ?>
                    <p class="description"><strong>Hintergrundworker aktiv:</strong> Die Seite muss nicht offen bleiben. Fortschritt und sichere Checkpoints werden persistent gespeichert.</p>
                <?php endif; ?>
                <?php if ($refresh) : $last_maint = is_array($refresh['maintenance'] ?? null) ? $refresh['maintenance'] : array(); ?>
                    <p><strong>Letzter Bestandsabgleich:</strong> <?php echo esc_html((string)($refresh['status'] ?? 'unbekannt')); ?> · lokaler Workflow <?php echo absint($last_maint['scanned'] ?? 0); ?> geprüft / <?php echo absint($last_maint['ready_private'] ?? 0); ?> PRIVATE bereit / <?php echo absint($last_maint['ready_business'] ?? 0); ?> BUSINESS bereit / <?php echo absint($last_maint['review'] ?? 0); ?> Review / <?php echo absint($last_maint['blocked'] ?? 0); ?> blockiert · eBay <?php echo absint($refresh['checked'] ?? 0); ?> geprüft / <?php echo absint($refresh['available'] ?? 0); ?> aktiv / <?php echo absint($refresh['ended'] ?? 0); ?> beendet / <?php echo absint($refresh['technical_errors'] ?? 0); ?> technische Fehler.</p>
                    <details><summary>Technische Details zum Bestandsabgleich</summary><pre style="white-space:pre-wrap"><?php echo esc_html(wp_json_encode($refresh, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES)); ?></pre></details>
                <?php else : ?><p><strong>Letzter Bestandsabgleich:</strong> noch nicht durchgeführt.</p><?php endif; ?>
                <p><strong>Letzter Provider-Fachtest:</strong> <?php echo $test ? esc_html((string)($test['status'] ?? 'unbekannt') . (!empty($test['tested_at']) ? ' · ' . wp_date('d.m.Y H:i:s', absint($test['tested_at'])) : '')) : 'noch nicht durchgeführt'; ?></p>
                <?php if ($test) : ?><details><summary>Technische Details zum Provider-Fachtest</summary><pre style="white-space:pre-wrap"><?php echo esc_html(wp_json_encode($test, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES)); ?></pre></details><?php endif; ?>
                <?php $sync_is_legacy = $sync && ((string)($sync['engine'] ?? '') !== 'resumable-background' || (string)($sync['build'] ?? '') === ''); ?>
                <?php if ($sync_is_legacy) : ?><div class="notice notice-warning inline"><p><strong>Historischer Legacy-Abruf.</strong> Diese Laufbilanz stammt nicht aus der fortsetzbaren Hintergrundengine dieses Builds und darf nicht als vollständiger aktueller Hintergrundabruf gewertet werden.</p></div><?php endif; ?>
                <p><strong>Letzter Abruf:</strong> <?php echo $sync ? esc_html((string)($sync['status'] ?? 'unbekannt') . ' · gefunden ' . absint($sync['received'] ?? 0) . ' · fachlich sicher ' . absint($sync['accepted'] ?? 0) . ' · Review ' . absint($sync['review_pending'] ?? 0) . ' · blockiert ' . (absint($sync['hard_blocked'] ?? 0) + absint($sync['technical_blocked'] ?? 0))) : 'noch nicht durchgeführt'; ?></p>
                <?php if ($sync) : ?><details><summary>Technische Details zum eBay-Abruf</summary><pre style="white-space:pre-wrap"><?php echo esc_html(wp_json_encode($sync, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES)); ?></pre></details><?php endif; ?>
                <?php if ($sync) : ?>
                    <p><strong>Lesbare Laufbilanz:</strong>
                        gefunden <?php echo absint($sync['received'] ?? 0); ?>
                        (<?php echo absint($sync['received_unique'] ?? 0); ?> eindeutig)
                        → technisch gültig <?php echo absint($sync['technically_valid'] ?? 0); ?>
                        → fachlich sicher <?php echo absint($sync['accepted'] ?? 0); ?>
                        → Prüfbestand <?php echo absint($sync['review_pending'] ?? 0); ?>
                        → hart blockiert <?php echo absint($sync['hard_blocked'] ?? 0); ?>
                        → technisch blockiert <?php echo absint($sync['technical_blocked'] ?? 0); ?>
                        → manuell gesperrt <?php echo absint($sync['manual_vetoed'] ?? 0); ?>.
                    </p>
                    <details><summary>Block- und Prüfgründe</summary><pre style="white-space:pre-wrap"><?php echo esc_html(wp_json_encode(array(
                        'hard'=>(array)($sync['hard_reasons'] ?? array()),
                        'review'=>(array)($sync['review_reasons'] ?? array()),
                        'technical'=>(array)($sync['technical_reasons'] ?? array()),
                        'manual_veto'=>(array)($sync['manual_veto_reasons'] ?? array()),
                    ), JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES)); ?></pre></details>
                <?php endif; ?>
            </section>

            <section class="postbox" style="padding:18px;max-width:1180px">
                <h2>5. eBay-Prüfbestand / Chef-Veto</h2>
                <p>Nur <strong>weiche fachliche Unsicherheiten</strong> erscheinen hier. Hard-Safety-, Provider-, Affiliate-, Ablauf- und technische Sperren bleiben nicht übersteuerbar. Ein Kandidat muss innerhalb der Sechs-Stunden-Frist entschieden werden.</p>
                <?php if (!$review_candidates) : ?>
                    <p><em>Kein offener Prüfkandidat.</em></p>
                <?php else : ?>
                    <table class="widefat striped"><thead><tr><th>Angebot</th><th>Typ</th><th>Prüfgrund</th><th>Chefentscheidung</th></tr></thead><tbody>
                    <?php foreach ($review_candidates as $candidate) : ?>
                        <tr>
                            <td><strong><?php echo esc_html((string)($candidate['title'] ?? '')); ?></strong><br><small>Item-ID <?php echo esc_html((string)($candidate['item_id'] ?? '')); ?> · <?php echo esc_html((string)($candidate['seller_username'] ?? '')); ?></small></td>
                            <td><?php echo esc_html((string)($candidate['seller_account_type'] ?? '')); ?></td>
                            <td><?php echo esc_html((string)($candidate['rejection_reason'] ?? '')); ?></td>
                            <td>
                            <?php if (strtoupper((string)($candidate['seller_account_type'] ?? '')) === 'INDIVIDUAL') : ?>
                                <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>" style="display:grid;gap:6px;min-width:320px">
                                    <input type="hidden" name="action" value="ppar_ebay_review_decision">
                                    <input type="hidden" name="row_id" value="<?php echo absint($candidate['id'] ?? 0); ?>">
                                    <?php wp_nonce_field('ppar_ebay_review_decision', 'ppar_ebay_nonce'); ?>
                                    <select name="target_term_id" required>
                                        <option value="">HivePress-Ziel wählen</option>
                                        <?php foreach ($review_targets as $target) : ?><option value="<?php echo absint($target->term_id ?? 0); ?>"><?php echo esc_html((string)($target->name ?? '')); ?></option><?php endforeach; ?>
                                    </select>
                                    <input type="text" name="reason" required maxlength="240" placeholder="Begründung der Chefentscheidung">
                                    <div style="display:flex;gap:6px;flex-wrap:wrap">
                                        <button class="button button-primary" name="review_decision" value="approve">Freigeben</button>
                                        <button class="button" name="review_decision" value="veto" formnovalidate onclick="this.form.querySelector('select[name=target_term_id]').removeAttribute('required');">Veto</button>
                                    </div>
                                </form>
                            <?php else : ?>
                                <em>BUSINESS-Prüfkandidat bleibt fail-closed; Freigabe über die Werbemittel-/Chefsteuerung wird nicht automatisch vorweggenommen.</em>
                            <?php endif; ?>
                            </td>
                        </tr>
                    <?php endforeach; ?>
                    </tbody></table>
                <?php endif; ?>
            </section>
        </div>
        <?php
    }
}
