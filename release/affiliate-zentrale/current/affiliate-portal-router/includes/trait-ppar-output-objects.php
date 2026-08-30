<?php
if (!defined('ABSPATH')) {
    exit;
}

/**
 * V4.0.0 – verbindendes Datenmodell zwischen Partner, Creative und Ausgabe.
 *
 * Grundregeln:
 * - Ein Output-Objekt gehört immer zu genau einem Creative und einem Portal.
 * - Bannerkampagne und HivePress-Listing sind getrennte Ausgabetypen.
 * - Der originale Creative-Trackinglink wird unverändert verwendet.
 * - Ein manuelles Creative-Veto ist dauerhaft vorrangig.
 * - Andere Portale werden über ein versionsgebundenes Adapterregister angebunden;
 *   unbekannte oder nicht verfügbare Adapter bleiben fail-closed.
 */
trait PPAR_Output_Objects_Trait {
    private function output_objects_table() {
        global $wpdb;
        return $wpdb->base_prefix . 'ppar_output_objects';
    }

    private function output_portal_decisions_table() {
        global $wpdb;
        return $wpdb->base_prefix . 'ppar_creative_portal_decisions';
    }

    public function maybe_install_output_objects_schema() {
        $installed = (string) get_option(self::OPTION_OUTPUT_SCHEMA_VERSION, '0');
        if ($installed === self::OUTPUT_SCHEMA_VERSION) {
            return;
        }
        require_once ABSPATH . 'wp-admin/includes/upgrade.php';
        global $wpdb;
        $table = $this->output_objects_table();
        $decisions_table = $this->output_portal_decisions_table();
        $charset = $wpdb->get_charset_collate();
        dbDelta("CREATE TABLE {$table} (
            id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
            object_key char(64) NOT NULL,
            portal_key varchar(191) NOT NULL,
            portal_adapter varchar(60) NOT NULL DEFAULT 'wordpress_local',
            creative_identity_hash char(64) NOT NULL,
            provider varchar(60) NOT NULL,
            partner_external_id varchar(191) NOT NULL DEFAULT '',
            output_type varchar(40) NOT NULL,
            target_type varchar(40) NOT NULL DEFAULT '',
            target_key varchar(191) NOT NULL DEFAULT '',
            target_label text NOT NULL,
            slot_id varchar(100) NOT NULL DEFAULT '',
            status varchar(40) NOT NULL DEFAULT 'review',
            confidence int(10) unsigned NOT NULL DEFAULT 0,
            decision_source varchar(60) NOT NULL DEFAULT '',
            decision_reason longtext NULL,
            campaign_post_id bigint(20) unsigned NOT NULL DEFAULT 0,
            listing_post_id bigint(20) unsigned NOT NULL DEFAULT 0,
            tracking_url text NOT NULL,
            image_url text NOT NULL,
            image_width int(10) unsigned NOT NULL DEFAULT 0,
            image_height int(10) unsigned NOT NULL DEFAULT 0,
            image_hash char(64) NOT NULL DEFAULT '',
            source_fingerprint char(64) NOT NULL DEFAULT '',
            payload longtext NULL,
            last_verified bigint(20) unsigned NOT NULL DEFAULT 0,
            created_at bigint(20) unsigned NOT NULL DEFAULT 0,
            updated_at bigint(20) unsigned NOT NULL DEFAULT 0,
            PRIMARY KEY  (id),
            UNIQUE KEY object_key (object_key),
            KEY portal_status (portal_key(100), status),
            KEY creative_output (creative_identity_hash, output_type),
            KEY partner_output (provider(20), partner_external_id(100), output_type)
        ) {$charset};");
        dbDelta("CREATE TABLE {$decisions_table} (
            id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
            portal_key varchar(191) NOT NULL,
            creative_identity_hash char(64) NOT NULL,
            manual_status varchar(30) NOT NULL DEFAULT 'automatic',
            reason text NOT NULL,
            created_at bigint(20) unsigned NOT NULL DEFAULT 0,
            updated_at bigint(20) unsigned NOT NULL DEFAULT 0,
            PRIMARY KEY  (id),
            UNIQUE KEY portal_creative (portal_key(120), creative_identity_hash),
            KEY portal_status (portal_key(120), manual_status)
        ) {$charset};");
        $this->output_migrate_legacy_scope_decisions($installed);
        update_option(self::OPTION_OUTPUT_SCHEMA_VERSION, self::OUTPUT_SCHEMA_VERSION, false);
        $this->output_objects_migrate_legacy_listing_state();
    }

    private function output_migrate_legacy_scope_decisions($previous_version) {
        if (version_compare((string) $previous_version, '1.1', '>=')) {
            return;
        }
        if (!method_exists($this, 'creative_library_table')) {
            return;
        }
        global $wpdb;
        $creative_table = $this->creative_library_table();
        $rows = $wpdb->get_results("SELECT identity_hash, content_scope, review_status FROM {$creative_table} WHERE identity_hash<>'' AND (content_scope IN ('horse','other','unclear') OR review_status IN ('approved','rejected'))", ARRAY_A);
        foreach ((array) $rows as $row) {
            $scope = sanitize_key((string) ($row['content_scope'] ?? ''));
            $review = sanitize_key((string) ($row['review_status'] ?? ''));
            $status = ($scope === 'other' || $review === 'rejected') ? 'veto' : ($scope === 'unclear' ? 'review' : 'approved');
            $this->output_set_portal_decision($this->output_local_portal_key(), (string) ($row['identity_hash'] ?? ''), $status, 'Aus V3.x-Bewertung für das lokale Portal übernommen.');
        }
    }

    private function output_portal_decision($portal_key, $identity_hash) {
        global $wpdb;
        $portal_key = sanitize_key((string) $portal_key);
        $identity_hash = strtolower(sanitize_text_field((string) $identity_hash));
        if ($portal_key === '' || !preg_match('/^[a-f0-9]{64}$/', $identity_hash)) {
            return array('manual_status'=>'automatic','reason'=>'','payload'=>array(),'user_id'=>0,'updated_at'=>0);
        }
        if (method_exists($this, 'control_get_decision')) {
            $control = $this->control_get_decision($portal_key, 'creative', $identity_hash);
            if (!empty($control['exists'])) {
                return array(
                    'manual_status'=>(string) ($control['status'] ?? 'automatic'),
                    'reason'=>(string) ($control['reason'] ?? ''),
                    'payload'=>is_array($control['payload'] ?? null) ? $control['payload'] : array(),
                    'user_id'=>absint($control['user_id'] ?? 0),
                    'updated_at'=>absint($control['updated_at'] ?? 0),
                );
            }
        }
        $row = $wpdb->get_row($wpdb->prepare("SELECT * FROM {$this->output_portal_decisions_table()} WHERE portal_key=%s AND creative_identity_hash=%s", $portal_key, $identity_hash), ARRAY_A);
        if (!is_array($row)) {
            return array('manual_status'=>'automatic','reason'=>'','payload'=>array(),'user_id'=>0,'updated_at'=>0);
        }
        return array_merge($row, array('payload'=>array(),'user_id'=>0));
    }

    public function output_set_portal_decision($portal_key, $identity_hash, $status, $reason = '', $payload = array()) {
        global $wpdb;
        $portal_key = sanitize_key((string) $portal_key);
        $identity_hash = strtolower(sanitize_text_field((string) $identity_hash));
        $status = sanitize_key((string) $status);
        if ($portal_key === '' || !preg_match('/^[a-f0-9]{64}$/', $identity_hash) || !in_array($status, array('automatic','approved','review','veto'), true)) {
            return new WP_Error('portal_decision_invalid', 'Portalentscheidung ist ungültig.');
        }
        $control_id = 0;
        if (method_exists($this, 'control_set_decision')) {
            $control = $this->control_set_decision($portal_key, 'creative', $identity_hash, $status, (string) $reason, is_array($payload) ? $payload : array(), 'creative_decision');
            if (is_wp_error($control)) {
                return $control;
            }
            $control_id = absint($control);
        }
        // Kompatibilitätskopie für ältere Diagnosen und sichere Rückmigration.
        $table = $this->output_portal_decisions_table();
        $existing = $wpdb->get_row($wpdb->prepare("SELECT id FROM {$table} WHERE portal_key=%s AND creative_identity_hash=%s", $portal_key, $identity_hash), ARRAY_A);
        $data = array('portal_key'=>$portal_key,'creative_identity_hash'=>$identity_hash,'manual_status'=>$status,'reason'=>sanitize_text_field((string) $reason),'updated_at'=>time());
        if ($existing) {
            $wpdb->update($table, $data, array('id'=>absint($existing['id'])));
            return $control_id > 0 ? $control_id : absint($existing['id']);
        }
        $data['created_at'] = time();
        $wpdb->insert($table, $data);
        $legacy_id = $wpdb->insert_id ? absint($wpdb->insert_id) : 0;
        return $control_id > 0 ? $control_id : ($legacy_id > 0 ? $legacy_id : new WP_Error('portal_decision_save_failed', 'Portalentscheidung konnte nicht gespeichert werden.'));
    }

    private function output_objects_migrate_legacy_listing_state() {
        if (!function_exists('get_posts') || !function_exists('update_post_meta')) {
            return;
        }
        $legacy = get_posts(array(
            'post_type' => 'hp_listing',
            'post_status' => array('draft','pending','publish','private'),
            'meta_key' => '_ppar_partner_identity',
            'posts_per_page' => 200,
            'fields' => 'ids',
        ));
        foreach ((array) $legacy as $post_id) {
            $post_id = absint($post_id);
            if ($post_id <= 0) {
                continue;
            }
            $creative_hash = (string) get_post_meta($post_id, '_ppar_creative_identity_hash', true);
            if ($creative_hash !== '') {
                continue;
            }
            update_post_meta($post_id, '_ppar_legacy_listing_blocked', 1);
            update_post_meta($post_id, '_ppar_legacy_listing_reason', 'V3.4.0-Listing ohne verknüpftes Creative; nicht automatisch freigeben.');
            $post = get_post($post_id);
            if ($post && (string) $post->post_status === 'publish' && function_exists('wp_update_post')) {
                wp_update_post(array('ID'=>$post_id, 'post_status'=>'draft'));
            }
        }
    }

    private function output_local_portal_key() {
        $host = strtolower((string) wp_parse_url(home_url('/'), PHP_URL_HOST));
        if ($host === '') {
            $host = 'local';
        }
        $blog_id = function_exists('get_current_blog_id') ? absint(get_current_blog_id()) : 1;
        return sanitize_key('wp-' . $blog_id . '-' . str_replace('.', '-', $host));
    }

    /**
     * Adaptervertrag für weitere Portale.
     *
     * Ein Adapterarray muss enthalten:
     * key, label, adapter, enabled und wahlweise blog_id oder callbacks.
     * Externe Adapter werden ausschließlich über den Filter registriert; ohne
     * vollständige callbacks werden sie als BLOCKED geführt und nie beschrieben.
     */
    public function output_portal_registry() {
        $portals = array();
        $local_key = $this->output_local_portal_key();
        $local_profile = array(
            'domain_key' => 'horse',
            'domain_terms' => array('pferd','pferde','pony','fohlen','reitsport','reiter'),
            'negative_terms' => array('hund','hunde','katze','katzen','kleintier','kleintiere','vogel','voegel','exoten'),
            'output_types' => array('portal_banner','product_campaign','hivepress_listing'),
            'listing_target_types' => array('hp_listing_category'),
            'banner_target_types' => array('page','category'),
            'product_target_types' => array('page','category'),
        );
        $local_profile = apply_filters('ppar_affiliate_local_portal_profile', $local_profile, $local_key, self::PORTAL_ADAPTER_VERSION);
        $local_profile = is_array($local_profile) ? $local_profile : array();
        $portals[$local_key] = array_merge(array(
            'key' => $local_key,
            'label' => get_bloginfo('name') ?: $local_key,
            'site_url' => home_url('/'),
            'adapter' => 'wordpress_local',
            'adapter_version' => self::PORTAL_ADAPTER_VERSION,
            'enabled' => true,
            'local' => true,
            'blog_id' => function_exists('get_current_blog_id') ? absint(get_current_blog_id()) : 1,
        ), $local_profile);

        if (function_exists('is_multisite') && is_multisite() && function_exists('get_sites')) {
            foreach ((array) get_sites(array('number'=>200, 'deleted'=>0, 'spam'=>0, 'archived'=>0)) as $site) {
                $blog_id = absint($site->blog_id ?? 0);
                if ($blog_id <= 0 || $blog_id === absint($portals[$local_key]['blog_id'])) {
                    continue;
                }
                $key = sanitize_key('wp-' . $blog_id);
                $portals[$key] = array(
                    'key'=>$key,
                    'label'=>'WordPress-Site ' . $blog_id,
                    'site_url'=>function_exists('get_home_url') ? get_home_url($blog_id, '/') : '',
                    'adapter'=>'wordpress_multisite',
                    'adapter_version'=>self::PORTAL_ADAPTER_VERSION,
                    'enabled'=>false,
                    'local'=>false,
                    'blog_id'=>$blog_id,
                );
            }
        }

        $stored = get_option(self::OPTION_PORTAL_REGISTRY, array());
        $stored = is_array($stored) ? $stored : array();
        foreach ($stored as $key => $settings) {
            $key = sanitize_key((string) $key);
            if ($key === '' || !isset($portals[$key]) || !is_array($settings)) {
                continue;
            }
            $portals[$key]['enabled'] = !empty($settings['enabled']);
            foreach (array('domain_key') as $field) {
                if (isset($settings[$field])) {
                    $portals[$key][$field] = sanitize_key((string) $settings[$field]);
                }
            }
            foreach (array('domain_terms','negative_terms','output_types','listing_target_types','banner_target_types','product_target_types') as $field) {
                if (isset($settings[$field]) && is_array($settings[$field])) {
                    $portals[$key][$field] = array_values(array_unique(array_filter(array_map($field === 'domain_terms' || $field === 'negative_terms' ? 'sanitize_text_field' : 'sanitize_key', $settings[$field]))));
                }
            }
        }

        $filtered = apply_filters('ppar_affiliate_portal_registry', $portals, self::PORTAL_ADAPTER_VERSION);
        if (!is_array($filtered)) {
            return $portals;
        }
        $safe = array();
        foreach ($filtered as $key => $portal) {
            if (!is_array($portal)) {
                continue;
            }
            $portal_key = sanitize_key((string) ($portal['key'] ?? $key));
            $adapter = sanitize_key((string) ($portal['adapter'] ?? ''));
            $version = (string) ($portal['adapter_version'] ?? '');
            if ($portal_key === '' || $adapter === '' || $version !== self::PORTAL_ADAPTER_VERSION) {
                continue;
            }
            $portal['key'] = $portal_key;
            $portal['adapter'] = $adapter;
            $portal['label'] = sanitize_text_field((string) ($portal['label'] ?? $portal_key));
            $portal['enabled'] = !empty($portal['enabled']);
            $portal['domain_key'] = sanitize_key((string) ($portal['domain_key'] ?? ''));
            foreach (array('domain_terms','negative_terms') as $field) {
                $portal[$field] = array_values(array_unique(array_filter(array_map('sanitize_text_field', (array) ($portal[$field] ?? array())))));
            }
            foreach (array('output_types','listing_target_types','banner_target_types','product_target_types') as $field) {
                $portal[$field] = array_values(array_unique(array_filter(array_map('sanitize_key', (array) ($portal[$field] ?? array())))));
            }
            $safe[$portal_key] = $portal;
        }
        return $safe;
    }

    private function output_portal_by_key($portal_key, $allow_disabled = false) {
        $portal_key = sanitize_key((string) $portal_key);
        $registry = $this->output_portal_registry();
        if (!is_array($registry[$portal_key] ?? null)) {
            return new WP_Error('portal_not_registered', 'Portaladapter ist nicht registriert.');
        }
        $portal = $registry[$portal_key];
        if (!$allow_disabled && empty($portal['enabled'])) {
            return new WP_Error('portal_disabled', 'Portal ist deaktiviert; keine Vorbereitung oder Freigabe zulässig.');
        }
        return $portal;
    }

    private function output_with_portal($portal, $callback) {
        if (!is_array($portal) || !is_callable($callback)) {
            return new WP_Error('portal_adapter_invalid', 'Portaladapter ist unvollständig.');
        }
        $adapter = sanitize_key((string) ($portal['adapter'] ?? ''));
        if ($adapter === 'wordpress_local') {
            return call_user_func($callback, $portal);
        }
        if ($adapter === 'wordpress_multisite') {
            $blog_id = absint($portal['blog_id'] ?? 0);
            if ($blog_id <= 0 || !function_exists('switch_to_blog') || !function_exists('restore_current_blog')) {
                return new WP_Error('portal_multisite_unavailable', 'Multisite-Portal ist nicht verfügbar.');
            }
            if (function_exists('get_current_blog_id') && absint(get_current_blog_id()) === $blog_id) {
                return call_user_func($callback, $portal);
            }
            switch_to_blog($blog_id);
            try {
                return call_user_func($callback, $portal);
            } finally {
                restore_current_blog();
            }
        }
        $callbacks = is_array($portal['callbacks'] ?? null) ? $portal['callbacks'] : array();
        if (empty($callbacks['run']) || !is_callable($callbacks['run'])) {
            return new WP_Error('portal_remote_adapter_missing', 'Externer Portaladapter ist nicht vollständig registriert.');
        }
        return call_user_func($callbacks['run'], $callback, $portal);
    }
    private function output_validate_portal_profile($portal) {
        if (!is_array($portal) || empty($portal['key']) || empty($portal['adapter']) || (string) ($portal['adapter_version'] ?? '') !== self::PORTAL_ADAPTER_VERSION) {
            return new WP_Error('portal_profile_invalid', 'Portalprofil oder Adapterversion ist ungültig.');
        }
        $domain_terms = array_values(array_filter(array_map('sanitize_text_field', (array) ($portal['domain_terms'] ?? array()))));
        if (!$domain_terms) {
            return new WP_Error('portal_domain_profile_missing', 'Für dieses Portal fehlt ein bestätigtes Fachprofil. Automatische Zuordnung bleibt gesperrt.');
        }
        $output_types = array_values(array_intersect(array_map('sanitize_key', (array) ($portal['output_types'] ?? array())), array('portal_banner','product_campaign','hivepress_listing','portal_listing')));
        if (!$output_types) {
            return new WP_Error('portal_output_types_missing', 'Für dieses Portal ist kein bestätigter Ausgabetyp registriert.');
        }
        return true;
    }
    private function output_term_path($term, $taxonomy, $by_id) {
        $parts = array(sanitize_text_field((string) ($term->name ?? '')));
        $parent = absint($term->parent ?? 0);
        $guard = 0;
        while ($parent > 0 && isset($by_id[$parent]) && $guard < 30) {
            array_unshift($parts, sanitize_text_field((string) ($by_id[$parent]->name ?? '')));
            $parent = absint($by_id[$parent]->parent ?? 0);
            $guard++;
        }
        return implode(' > ', array_filter($parts));
    }

    private function output_collect_local_targets() {
        $targets = array();
        if (function_exists('get_pages')) {
            foreach ((array) get_pages(array('post_status'=>'publish', 'sort_column'=>'menu_order,post_title')) as $page) {
                $id = absint($page->ID ?? 0);
                if ($id <= 0) { continue; }
                $parts = array(sanitize_text_field((string) ($page->post_title ?? '')));
                $parent = absint($page->post_parent ?? 0);
                $guard = 0;
                while ($parent > 0 && $guard < 30) {
                    $ancestor = get_post($parent);
                    if (!$ancestor) { break; }
                    array_unshift($parts, sanitize_text_field((string) ($ancestor->post_title ?? '')));
                    $parent = absint($ancestor->post_parent ?? 0);
                    $guard++;
                }
                $content = (string) ($page->post_content ?? '');
                $context = '';
                if (function_exists('has_shortcode') && (has_shortcode($content, 'pferde_journal') || has_shortcode($content, 'affiliate_portal_journal'))) {
                    $context = 'journal';
                } elseif (function_exists('has_shortcode') && has_shortcode($content, 'pferde_atelier_anzeigenmarkt_intro')) {
                    $context = 'anzeigenmarkt';
                } elseif (class_exists('Pferde_Template_Kit') && is_callable(array('Pferde_Template_Kit','affiliate_page_type'))) {
                    $context = sanitize_key((string) Pferde_Template_Kit::affiliate_page_type($id));
                }
                if ($context === '') { $context = 'page_unclassified'; }
                $targets[] = array(
                    'type'=>'page','key'=>'page:' . $id,'id'=>$id,
                    'slug'=>sanitize_key((string) ($page->post_name ?? '')),
                    'label'=>implode(' > ', array_filter($parts)),
                    'description'=>sanitize_text_field(wp_strip_all_tags((string) (($page->post_excerpt ?? '') . ' ' . $content))),
                    'depth'=>count(array_filter($parts)),
                    'context'=>$context,
                );
            }
        }
        foreach (array('category','hp_listing_category') as $taxonomy) {
            if (!function_exists('taxonomy_exists') || !taxonomy_exists($taxonomy) || !function_exists('get_terms')) { continue; }
            $terms = get_terms(array('taxonomy'=>$taxonomy, 'hide_empty'=>false));
            if (is_wp_error($terms) || !is_array($terms)) { continue; }
            $by_id = array(); $children = array();
            foreach ($terms as $term) {
                if (is_object($term) && !empty($term->term_id)) {
                    $id = absint($term->term_id); $by_id[$id] = $term;
                    $parent = absint($term->parent ?? 0); if ($parent > 0) { $children[$parent] = true; }
                }
            }
            foreach ($by_id as $term) {
                $id = absint($term->term_id ?? 0);
                $path = $this->output_term_path($term, $taxonomy, $by_id);
                $context = $taxonomy === 'hp_listing_category' ? 'hivepress_category' : (empty($children[$id]) ? 'leaf_category' : 'category_nonleaf');
                $targets[] = array(
                    'type'=>$taxonomy,'key'=>$taxonomy . ':' . $id,'id'=>$id,
                    'slug'=>sanitize_key((string) ($term->slug ?? '')),
                    'label'=>$path,
                    'description'=>sanitize_text_field(wp_strip_all_tags((string) ($term->description ?? ''))),
                    'depth'=>substr_count($path, ' > ') + 1,
                    'context'=>$context,
                );
            }
        }
        return $targets;
    }
    public function output_portal_targets($portal) {
        return $this->output_with_portal($portal, function($active_portal) {
            $adapter = sanitize_key((string) ($active_portal['adapter'] ?? ''));
            if (in_array($adapter, array('wordpress_local','wordpress_multisite'), true)) {
                return $this->output_collect_local_targets();
            }
            $callbacks = is_array($active_portal['callbacks'] ?? null) ? $active_portal['callbacks'] : array();
            if (empty($callbacks['targets']) || !is_callable($callbacks['targets'])) {
                return new WP_Error('portal_targets_missing', 'Portaladapter liefert keinen Zielkatalog.');
            }
            $targets = call_user_func($callbacks['targets'], $active_portal);
            return is_array($targets) ? $targets : new WP_Error('portal_targets_invalid', 'Portaladapter lieferte einen ungültigen Zielkatalog.');
        });
    }

    /**
     * Festgeschriebene aktive Slotmatrix aus dem getrennten Design–Affiliate-
     * Schnittstellenvertrag Pferde Atelier V1.50.387 / Affiliate-Vertrag 1.0.
     * Das Design wird nicht gelesen oder verändert; Vertragsabweichungen bleiben
     * fail-closed. Andere Portale liefern ihre Matrix über den bestehenden Filter.
     */
    public function output_slot_matrix($portal) {
        $adapter = sanitize_key((string) ($portal['adapter'] ?? ''));
        if (in_array($adapter, array('wordpress_local','wordpress_multisite'), true)) {
            $matrix = $this->output_with_portal($portal, function($active_portal) {
                $candidate = array();
                if (class_exists('Pferde_Template_Kit')) {
                    $contract = is_callable(array('Pferde_Template_Kit','affiliate_contract_version'))
                        ? (string) call_user_func(array('Pferde_Template_Kit','affiliate_contract_version'))
                        : (defined('Pferde_Template_Kit::AFFILIATE_CONTRACT') ? (string) constant('Pferde_Template_Kit::AFFILIATE_CONTRACT') : '');
                    $profile = is_callable(array('Pferde_Template_Kit','design_profile'))
                        ? sanitize_key((string) call_user_func(array('Pferde_Template_Kit','design_profile')))
                        : '';
                    $profile_contract = is_callable(array('Pferde_Template_Kit','design_profile_contract_version'))
                        ? (string) call_user_func(array('Pferde_Template_Kit','design_profile_contract_version'))
                        : '';
                    if ($contract === self::CONTRACT_VERSION && $profile === 'pferde_atelier' && $profile_contract === '1.0') {
                        $candidate = array(
                            'start_after_topics'=>array('creative_type'=>'banner','ratio_min'=>3.00,'ratio_max'=>12.00,'min_width'=>600,'min_height'=>60,'crop'=>'contain','target_types'=>array('page'),'target_contexts'=>array('start')),
                            'hub_grid_card'=>array('creative_type'=>'banner','ratio_min'=>0.80,'ratio_max'=>2.40,'min_width'=>240,'min_height'=>110,'crop'=>'cover','target_types'=>array('page'),'target_contexts'=>array('hub1','hub2')),
                            'hub_after_cards'=>array('creative_type'=>'banner','ratio_min'=>3.00,'ratio_max'=>12.00,'min_width'=>600,'min_height'=>60,'crop'=>'contain','target_types'=>array('page'),'target_contexts'=>array('hub1','hub2')),
                            'product_after_category_tiles'=>array('creative_type'=>'banner','ratio_min'=>3.00,'ratio_max'=>12.00,'min_width'=>600,'min_height'=>60,'crop'=>'contain','target_types'=>array('page','category'),'target_contexts'=>array('category','leaf','leaf_category')),
                            'journal_banner'=>array('creative_type'=>'banner','ratio_min'=>3.00,'ratio_max'=>12.00,'min_width'=>600,'min_height'=>60,'crop'=>'contain','target_types'=>array('page'),'target_contexts'=>array('journal')),
                            'anzeigenmarkt_top_banner'=>array('creative_type'=>'banner','ratio_min'=>3.00,'ratio_max'=>12.00,'min_width'=>600,'min_height'=>60,'crop'=>'contain','target_types'=>array('page'),'target_contexts'=>array('anzeigenmarkt')),
                            'hub_product_1'=>array('creative_type'=>'product','ratio_min'=>0.55,'ratio_max'=>2.00,'min_width'=>180,'min_height'=>180,'crop'=>'contain','target_types'=>array('page'),'target_contexts'=>array('hub1')),
                            'hub_product_2'=>array('creative_type'=>'product','ratio_min'=>0.55,'ratio_max'=>2.00,'min_width'=>180,'min_height'=>180,'crop'=>'contain','target_types'=>array('page'),'target_contexts'=>array('hub1')),
                            'hub_product_3'=>array('creative_type'=>'product','ratio_min'=>0.55,'ratio_max'=>2.00,'min_width'=>180,'min_height'=>180,'crop'=>'contain','target_types'=>array('page'),'target_contexts'=>array('hub1')),
                            'category_product_1'=>array('creative_type'=>'product','ratio_min'=>0.55,'ratio_max'=>2.00,'min_width'=>180,'min_height'=>180,'crop'=>'contain','target_types'=>array('page','category'),'target_contexts'=>array('hub2','category','leaf','leaf_category')),
                            'category_product_2'=>array('creative_type'=>'product','ratio_min'=>0.55,'ratio_max'=>2.00,'min_width'=>180,'min_height'=>180,'crop'=>'contain','target_types'=>array('page','category'),'target_contexts'=>array('hub2','category','leaf','leaf_category')),
                            'category_product_3'=>array('creative_type'=>'product','ratio_min'=>0.55,'ratio_max'=>2.00,'min_width'=>180,'min_height'=>180,'crop'=>'contain','target_types'=>array('page','category'),'target_contexts'=>array('hub2','category','leaf','leaf_category')),
                            'journal_product_1'=>array('creative_type'=>'product','ratio_min'=>0.55,'ratio_max'=>2.00,'min_width'=>180,'min_height'=>180,'crop'=>'contain','target_types'=>array('page'),'target_contexts'=>array('journal')),
                            'journal_product_2'=>array('creative_type'=>'product','ratio_min'=>0.55,'ratio_max'=>2.00,'min_width'=>180,'min_height'=>180,'crop'=>'contain','target_types'=>array('page'),'target_contexts'=>array('journal')),
                            'journal_product_3'=>array('creative_type'=>'product','ratio_min'=>0.55,'ratio_max'=>2.00,'min_width'=>180,'min_height'=>180,'crop'=>'contain','target_types'=>array('page'),'target_contexts'=>array('journal')),
                        );
                    }
                }
                $filtered = apply_filters('ppar_affiliate_slot_matrix', $candidate, $active_portal, self::PORTAL_ADAPTER_VERSION);
                return is_array($filtered) ? $filtered : array();
            });
            return is_wp_error($matrix) || !is_array($matrix) ? array() : $matrix;
        }
        $callbacks = is_array($portal['callbacks'] ?? null) ? $portal['callbacks'] : array();
        if (empty($callbacks['slots']) || !is_callable($callbacks['slots'])) { return array(); }
        $candidate = call_user_func($callbacks['slots'], $portal, self::PORTAL_ADAPTER_VERSION);
        return is_array($candidate) ? $candidate : array();
    }
    private function output_text($value) {
        $value = remove_accents(strtolower(wp_strip_all_tags((string) $value)));
        $value = str_replace(array('&','+','/'), ' ', $value);
        $value = preg_replace('/[^a-z0-9]+/', ' ', $value);
        return trim(preg_replace('/\s+/', ' ', (string) $value));
    }

    private function output_tokens($value) {
        $stop = array_flip(array('und','oder','mit','fuer','fur','von','der','die','das','ein','eine','im','in','am','auf','de','www','https','http','com','banner','angebot','partner'));
        $out = array();
        foreach (preg_split('/\s+/', $this->output_text($value)) as $token) {
            if (strlen($token) < 3 || isset($stop[$token])) {
                continue;
            }
            $out[$token] = true;
            // Kleine, sprachneutrale Normalisierung plus konservative deutsche
            // Flexionsvarianten. Dadurch werden z. B. "Versicherungen" und
            // "Versicherung" vergleichbar, ohne eine Branchenliste einzubauen.
            foreach (array('ern','en','er','es','e','n','s') as $suffix) {
                if (strlen($token) >= 7 + strlen($suffix) && substr($token, -strlen($suffix)) === $suffix) {
                    $root = substr($token, 0, -strlen($suffix));
                    if (strlen($root) >= 5 && !isset($stop[$root])) {
                        $out[$root] = true;
                    }
                }
            }
        }
        return array_keys($out);
    }

    private function output_term_present($text, $term) {
        $term = $this->output_text($term);
        if ($term === '') {
            return false;
        }
        $text_tokens = $this->output_tokens($text);
        $term_tokens = $this->output_tokens($term);
        if (!$term_tokens) {
            $term_tokens = array($term);
        }
        foreach ($text_tokens as $text_token) {
            foreach ($term_tokens as $term_token) {
                if ($text_token === $term_token) {
                    return true;
                }
                if (strlen($term_token) >= 4 && strlen($text_token) >= 5 && (strpos($text_token, $term_token) !== false || strpos($term_token, $text_token) !== false)) {
                    return true;
                }
            }
        }
        return false;
    }

    private function output_partner_evidence($row) {
        $provider = sanitize_key((string) ($row['provider'] ?? ''));
        $external_id = preg_replace('/[^0-9A-Za-z._-]/', '', (string) ($row['partner_external_id'] ?? ''));
        $profile = method_exists($this, 'partner_profile_get') ? $this->partner_profile_get($provider, $external_id) : array();
        $profile = is_array($profile) ? $profile : array();
        if (empty($profile['enabled'])) {
            $profile['business_label'] = '';
            $profile['keywords'] = array();
        }
        $snapshots = method_exists($this, 'partner_intake_snapshots') ? $this->partner_intake_snapshots() : array();
        $snapshot = is_array($snapshots[$provider . ':' . $external_id] ?? null) ? $snapshots[$provider . ':' . $external_id] : array();
        $programme = is_array($snapshot['programme'] ?? null) ? $snapshot['programme'] : array();
        return array(
            'profile'=>$profile,
            'business_label'=>sanitize_text_field((string) ($profile['business_label'] ?? '')),
            'keywords'=>array_values(array_filter(array_map('sanitize_text_field', (array) ($profile['keywords'] ?? array())))),
            'primary_sector'=>sanitize_text_field((string) ($programme['primary_sector'] ?? $programme['primarySector'] ?? '')),
            'programme_description'=>sanitize_text_field(wp_strip_all_tags((string) ($programme['description'] ?? ''))),
            'domains'=>array_values(array_filter(array_map('sanitize_text_field', (array) ($programme['valid_domains'] ?? array())))),
        );
    }

    private function output_creative_specific_text($row) {
        return implode(' ', array_filter(array(
            (string) ($row['title'] ?? ''),
            (string) ($row['description'] ?? ''),
            (string) ($row['tags'] ?? ''),
            (string) ($row['destination_url'] ?? ''),
        )));
    }

    /**
     * Creative-spezifische Evidenz darf durch einen Portaladapter ergänzt werden,
     * etwa durch eine lokal freigegebene Bildklassifikation. Partnerdaten allein
     * reichen bewusst nicht als Creative-Beweis. Ohne belastbare Creative-Evidenz
     * bleibt die automatische Ausgabe in der Prüfliste.
     */
    private function output_creative_evidence_text($row, $portal, $output_type) {
        $evidence = array($this->output_creative_specific_text($row));
        $adapter = sanitize_key((string) ($portal['adapter'] ?? ''));
        if (!in_array($adapter, array('wordpress_local','wordpress_multisite'), true)) {
            $callbacks = is_array($portal['callbacks'] ?? null) ? $portal['callbacks'] : array();
            if (!empty($callbacks['creative_evidence']) && is_callable($callbacks['creative_evidence'])) {
                $extra = call_user_func($callbacks['creative_evidence'], $row, $portal, sanitize_key((string) $output_type), self::PORTAL_ADAPTER_VERSION);
                if (is_wp_error($extra)) {
                    return $extra;
                }
                $evidence = array_merge($evidence, is_array($extra) ? $extra : array($extra));
            }
        }
        $filtered = apply_filters('ppar_affiliate_creative_evidence', $evidence, $row, $portal, sanitize_key((string) $output_type), self::PORTAL_ADAPTER_VERSION);
        if (is_wp_error($filtered)) {
            return $filtered;
        }
        $filtered = is_array($filtered) ? $filtered : array($filtered);
        return implode(' ', array_filter(array_map('sanitize_text_field', $filtered)));
    }

    private function output_classify_for_portal($row, $portal, $output_type) {
        if (!is_array($row) || empty($row['identity_hash'])) {
            return new WP_Error('output_creative_missing', 'Creative-Datensatz fehlt.');
        }
        $profile_valid = $this->output_validate_portal_profile($portal);
        if (is_wp_error($profile_valid)) { return $profile_valid; }
        $portal_key = sanitize_key((string) ($portal['key'] ?? ''));
        $manual = $this->output_portal_decision($portal_key, (string) ($row['identity_hash'] ?? ''));
        $manual_status = sanitize_key((string) ($manual['manual_status'] ?? 'automatic'));
        $manual_payload = is_array($manual['payload'] ?? null) ? $manual['payload'] : array();

        // Vertragsreihenfolge: erst unverrückbare technische/rechtliche
        // Sicherheitsblocker, danach die Chefentscheidung, erst danach Automatik.
        // Dadurch kann ein Veto zwar immer stoppen, aber niemals einen realen
        // Sicherheitsfehler verdecken oder eine Freigabe ihn überstimmen.
        if (method_exists($this, 'control_creative_safety_check')) {
            $safety = $this->control_creative_safety_check($row, $portal, 'plan');
            if (is_wp_error($safety)) {
                return $safety;
            }
        } elseif ((string) ($row['source_status'] ?? 'active') !== 'active' || (string) ($row['availability_state'] ?? 'active') !== 'active') {
            return array('status'=>'blocked','confidence'=>100,'reason'=>'Creative-Quelle ist nicht aktiv.','target'=>null,'source'=>'source_state');
        }
        if ($manual_status === 'veto') {
            return array('status'=>'blocked','confidence'=>100,'reason'=>(string) ($manual['reason'] ?? 'Manuelles Creative-Veto ist für dieses Portal vorrangig.'),'target'=>null,'source'=>'manual_veto');
        }
        if ($manual_status === 'review') {
            return array('status'=>'review','confidence'=>0,'reason'=>(string) ($manual['reason'] ?? 'Creative wurde für dieses Portal zur Prüfung markiert.'),'target'=>null,'source'=>'manual_review');
        }
        $fixed_target_key = sanitize_text_field((string) ($manual_payload['target_key'] ?? ''));
        if ($manual_status === 'approved' && $fixed_target_key !== '') {
            $targets = $this->output_portal_targets($portal);
            if (is_wp_error($targets)) {
                return $targets;
            }
            $is_listing = in_array($output_type, array('hivepress_listing','portal_listing'), true);
            if ($is_listing) {
                $wanted_types = array_values(array_filter(array_map('sanitize_key', (array) ($portal['listing_target_types'] ?? array('hp_listing_category')))));
            } elseif ($output_type === 'product_campaign') {
                $wanted_types = array_values(array_filter(array_map('sanitize_key', (array) ($portal['product_target_types'] ?? array('page','category')))));
            } else {
                $wanted_types = array_values(array_filter(array_map('sanitize_key', (array) ($portal['banner_target_types'] ?? array('page','category')))));
            }
            foreach ((array) $targets as $target) {
                if (!is_array($target)) { continue; }
                if ((string) ($target['key'] ?? '') !== $fixed_target_key) { continue; }
                if (!in_array(sanitize_key((string) ($target['type'] ?? '')), $wanted_types, true)) {
                    return new WP_Error('control_fixed_target_type_invalid', 'Festes Portalziel ist für diesen Ausgabetyp nicht zulässig.');
                }
                if (method_exists($this, 'control_target_gate')) {
                    $target_gate = $this->control_target_gate($portal_key, (string) ($target['key'] ?? ''));
                    if (is_wp_error($target_gate)) { return $target_gate; }
                }
                return array(
                    'status'=>'ready',
                    'confidence'=>100,
                    'reason'=>(string) ($manual['reason'] ?? 'Chefentscheidung mit festem Portalziel.'),
                    'target'=>$target,
                    'alternatives'=>array(),
                    'source'=>'manual_fixed_target',
                );
            }
            return new WP_Error('control_fixed_target_missing', 'Fest vorgegebenes Portalziel existiert nicht mehr oder ist nicht erreichbar.');
        }
        // eBay-BUSINESS ist ein harter eigener Zielvertrag. Nach Veto/Review bzw.
        // einem expliziten Chefziel darf die Automatik NIEMALS in die generische
        // Textklassifikation zurueckfallen. Entweder existiert ein verifiziertes
        // Produkt-/Hub-Konzept oder der Datensatz bleibt targetless auf Review.
        $is_ebay_business_product = $output_type === 'product_campaign'
            && sanitize_key((string)($row['provider'] ?? '')) === 'ebay'
            && sanitize_key((string)($row['source_kind'] ?? '')) === 'ebay_business_item'
            && sanitize_key((string)($row['creative_type'] ?? '')) === 'product';
        if ($is_ebay_business_product) {
            $ebay_payload = json_decode((string)($row['payload'] ?? ''), true);
            $ebay_payload = is_array($ebay_payload) ? $ebay_payload : array();
            $is_ebay_business_product = strtoupper(sanitize_key((string)($ebay_payload['ebay_seller_account_type'] ?? ''))) === 'BUSINESS';
        }
        if ($is_ebay_business_product && method_exists($this, 'ebay_business_exact_product_classification')) {
            $targets = $this->output_portal_targets($portal);
            if (is_wp_error($targets)) { return $targets; }
            $ebay_exact = $this->ebay_business_exact_product_classification($row, $portal, $targets);
            if (is_wp_error($ebay_exact)) { return $ebay_exact; }
            if (is_array($ebay_exact) && !empty($ebay_exact)) { return $ebay_exact; }
            return array(
                'status'=>'review','confidence'=>0,
                'reason'=>'eBay-BUSINESS besitzt keinen aktuell verifizierten Produktvertrag; generische Portalzuordnung ist gesperrt.',
                'target'=>null,'alternatives'=>array(),'source'=>'ebay_business_contract_missing',
            );
        }
        $specific_evidence = $this->output_creative_evidence_text($row, $portal, $output_type);
        if (is_wp_error($specific_evidence)) {
            return $specific_evidence;
        }
        $specific = $this->output_text($specific_evidence);
        $domain_terms = array_values(array_filter(array_map(array($this, 'output_text'), (array) ($portal['domain_terms'] ?? array()))));
        $negative_terms = array_values(array_filter(array_map(array($this, 'output_text'), (array) ($portal['negative_terms'] ?? array()))));
        $specific_has_domain = false;
        foreach ($domain_terms as $term) { if ($term !== '' && $this->output_term_present($specific, $term)) { $specific_has_domain = true; break; } }
        $specific_has_negative = false;
        foreach ($negative_terms as $term) { if ($term !== '' && $this->output_term_present($specific, $term)) { $specific_has_negative = true; break; } }
        if ($specific_has_negative && !$specific_has_domain && $manual_status !== 'approved') {
            return array('status'=>'blocked','confidence'=>100,'reason'=>'Creative-spezifischer fachfremder Inhalt für dieses Portal erkannt.','target'=>null,'source'=>'creative_negative');
        }
        if ($specific_has_negative && $specific_has_domain && $manual_status !== 'approved') {
            return array('status'=>'review','confidence'=>50,'reason'=>'Creative enthält widersprüchliche Fachsignale und benötigt eine Sichtprüfung.','target'=>null,'source'=>'creative_conflict');
        }
        if (!$specific_has_domain && $manual_status !== 'approved') {
            return array('status'=>'review','confidence'=>0,'reason'=>'Das Partnerprofil passt, aber das konkrete Creative besitzt noch keinen belastbaren Fachbezug.','target'=>null,'source'=>'creative_domain_signal_missing');
        }
        $partner = $this->output_partner_evidence($row);
        $partner_text = implode(' ', array_filter(array(
            (string) ($row['partner_name'] ?? ''),
            (string) $partner['business_label'],
            implode(' ', (array) $partner['keywords']),
            (string) $partner['primary_sector'],
            (string) $partner['programme_description'],
            implode(' ', (array) $partner['domains']),
        )));
        $combined = trim($specific . ' ' . $this->output_text($partner_text));
        $combined_has_domain = false;
        foreach ($domain_terms as $term) { if ($term !== '' && $this->output_term_present($combined, $term)) { $combined_has_domain = true; break; } }
        if (!$combined_has_domain && $manual_status !== 'approved') {
            return array('status'=>'review','confidence'=>0,'reason'=>'Kein belastbarer Bezug zum Fachprofil dieses Portals.','target'=>null,'source'=>'portal_domain_signal_missing');
        }
        $source_tokens = $this->output_tokens($combined);
        if (!$source_tokens) {
            return array('status'=>'review','confidence'=>0,'reason'=>'Keine verwertbaren Klassifikationssignale.','target'=>null,'source'=>'insufficient_data');
        }
        $targets = $this->output_portal_targets($portal);
        if (is_wp_error($targets)) {
            return $targets;
        }
        $is_listing = in_array($output_type, array('hivepress_listing','portal_listing'), true);
        if ($is_listing) {
            $wanted_types = array_values(array_filter(array_map('sanitize_key', (array) ($portal['listing_target_types'] ?? array('hp_listing_category')))));
        } elseif ($output_type === 'product_campaign') {
            $wanted_types = array_values(array_filter(array_map('sanitize_key', (array) ($portal['product_target_types'] ?? array('page','category')))));
        } else {
            $wanted_types = array_values(array_filter(array_map('sanitize_key', (array) ($portal['banner_target_types'] ?? array('page','category')))));
        }
        $ranked = array();
        foreach ((array) $targets as $target) {
            if (!is_array($target)) {
                continue;
            }
            $type = sanitize_key((string) ($target['type'] ?? ''));
            if (!in_array($type, $wanted_types, true)) {
                continue;
            }
            if (method_exists($this, 'control_target_gate')) {
                $target_gate = $this->control_target_gate($portal_key, (string) ($target['key'] ?? ''));
                if (is_wp_error($target_gate)) { continue; }
            }
            $target_text = implode(' ', array((string) ($target['label'] ?? ''), (string) ($target['slug'] ?? ''), (string) ($target['description'] ?? '')));
            $target_tokens = $this->output_tokens($target_text);
            $hits = array_values(array_intersect($source_tokens, $target_tokens));
            foreach ($source_tokens as $source_token) {
                foreach ($target_tokens as $target_token) {
                    if (strlen($source_token) >= 5 && strlen($target_token) >= 5 && (strpos($source_token, $target_token) !== false || strpos($target_token, $source_token) !== false)) {
                        $hits[] = $target_token;
                    }
                }
            }
            $hits = array_values(array_unique($hits));
            $score = min(60, count($hits) * 12);
            $label_norm = $this->output_text((string) ($target['label'] ?? ''));
            $label_parts = preg_split('/\s+>\s+/', (string) ($target['label'] ?? ''));
            $leaf_norm = $this->output_text($label_parts ? end($label_parts) : $label_norm);
            $business_norm = $this->output_text((string) $partner['business_label']);
            if ($business_norm !== '' && (strpos(' ' . $label_norm . ' ', ' ' . $business_norm . ' ') !== false || strpos($business_norm, $leaf_norm) !== false || strpos($leaf_norm, $business_norm) !== false)) {
                $score += 45;
            }
            // Providerunabhängiger Geschäftsbereichsabgleich: zusammengesetzte
            // Bezeichnungen wie „Tierversicherung“ dürfen ein eindeutiges Ziel
            // „Versicherungen & Recht“ erkennen, ohne eine Branchen-Sonderliste.
            $business_tokens = $this->output_tokens($business_norm);
            $business_hits = array();
            foreach ($business_tokens as $business_token) {
                foreach ($target_tokens as $target_token) {
                    if ($business_token === $target_token || (strlen($business_token) >= 5 && strlen($target_token) >= 5 && (strpos($business_token, $target_token) !== false || strpos($target_token, $business_token) !== false))) {
                        $business_hits[$target_token] = true;
                    }
                }
            }
            if ($business_hits) {
                $score += min(90, count($business_hits) * 60);
            }
            foreach ((array) $partner['keywords'] as $keyword) {
                $keyword = $this->output_text($keyword);
                if ($keyword === '') {
                    continue;
                }
                if ($keyword === $leaf_norm || strpos(' ' . $label_norm . ' ', ' ' . $keyword . ' ') !== false) {
                    $score += 70;
                } elseif (strpos($keyword, $leaf_norm) !== false || strpos($leaf_norm, $keyword) !== false) {
                    $score += 55;
                } else {
                    $keyword_tokens = $this->output_tokens($keyword);
                    $score += min(30, count(array_intersect($keyword_tokens, $target_tokens)) * 15);
                }
            }
            if ($specific !== '') {
                $specific_tokens = $this->output_tokens($specific);
                $specific_hits = array_values(array_intersect($specific_tokens, $target_tokens));
                $score += min(30, count($specific_hits) * 15);
                if ($specific === $leaf_norm || strpos(' ' . $specific . ' ', ' ' . $leaf_norm . ' ') !== false) {
                    $score += 55;
                }
            }
            foreach ($domain_terms as $domain_term) {
                if ($domain_term !== '' && $this->output_term_present($combined, $domain_term) && $this->output_term_present($label_norm, $domain_term)) {
                    $score += $hits ? 35 : 15;
                    break;
                }
            }
            if ($score >= 55) {
                // Für die Rangfolge den Rohwert behalten. Ein frühes Kappen auf
                // 100 würde einen exakten Creative-Treffer und einen nur grob
                // passenden Partnertreffer künstlich gleichsetzen.
                $target['raw_score'] = $score;
                $target['score'] = min(100, $score);
                $target['hits'] = $hits;
                $ranked[] = $target;
            }
        }
        usort($ranked, static function($a, $b) {
            $cmp = (int) ($b['raw_score'] ?? $b['score'] ?? 0) <=> (int) ($a['raw_score'] ?? $a['score'] ?? 0);
            if ($cmp !== 0) {
                return $cmp;
            }
            $depth_cmp = absint($b['depth'] ?? 0) <=> absint($a['depth'] ?? 0);
            if ($depth_cmp !== 0) { return $depth_cmp; }
            return strnatcasecmp((string) ($a['label'] ?? ''), (string) ($b['label'] ?? ''));
        });
        if (!$ranked) {
            return array('status'=>'review','confidence'=>0,'reason'=>'Kein sicherer Zieltreffer im Portal.','target'=>null,'source'=>'automatic');
        }
        $best = $ranked[0];
        $best_raw = absint($best['raw_score'] ?? $best['score'] ?? 0);
        $second_raw = isset($ranked[1]) ? absint($ranked[1]['raw_score'] ?? $ranked[1]['score'] ?? 0) : 0;
        $best_score = min(100, $best_raw);
        $hierarchy_safe = false;
        if (isset($ranked[1]) && ($best_raw - $second_raw) < 15) {
            $best_label = $this->output_text((string) ($best['label'] ?? ''));
            $second_label = $this->output_text((string) ($ranked[1]['label'] ?? ''));
            $hierarchy_safe = absint($best['depth'] ?? 0) > absint($ranked[1]['depth'] ?? 0)
                && strpos($best_label, $second_label) !== false;
        }
        if ($best_raw < 72 || ($second_raw > 0 && ($best_raw - $second_raw) < 15 && !$hierarchy_safe)) {
            return array('status'=>'review','confidence'=>$best_score,'reason'=>'Mehrere oder zu schwache Portalziele.','target'=>$best,'alternatives'=>array_slice($ranked, 0, 5),'source'=>'automatic');
        }
        return array('status'=>'ready','confidence'=>$best_score,'reason'=>'Eindeutiger mehrquelliger Zieltreffer.','target'=>$best,'alternatives'=>array_slice($ranked, 1, 4),'source'=>$manual_status === 'approved' ? 'manual_approved_plus_automatic_target' : 'automatic');
    }

    /**
     * Marketplace product cards use contain rendering and a stable provider image
     * URL. For verified eBay BUSINESS products, remote dimension measurement is a
     * quality/health signal, not a prerequisite for public availability. Banners,
     * manual creatives and every other provider keep the strict dimension gate.
     */
    private function output_allows_provisional_ebay_product_asset($row) {
        if (!is_array($row)
            || sanitize_key((string)($row['provider'] ?? '')) !== 'ebay'
            || sanitize_key((string)($row['source_kind'] ?? '')) !== 'ebay_business_item'
            || sanitize_key((string)($row['creative_type'] ?? '')) !== 'product'
            || sanitize_key((string)($row['source_status'] ?? 'active')) !== 'active'
            || sanitize_key((string)($row['availability_state'] ?? 'active')) !== 'active') { return false; }
        $image_url = esc_url_raw((string)($row['image_url'] ?? ''));
        if ($image_url === '' || stripos($image_url, 'https://') !== 0 || (function_exists('wp_http_validate_url') && !wp_http_validate_url($image_url))) { return false; }
        $payload = json_decode((string)($row['payload'] ?? ''), true);
        $payload = is_array($payload) ? $payload : array();
        if (strtoupper(sanitize_key((string)($payload['ebay_seller_account_type'] ?? ''))) !== 'BUSINESS') { return false; }
        if (sanitize_key((string)($payload['ebay_business_match_contract'] ?? '')) !== 'concept_v3') { return false; }
        if (sanitize_key((string)($payload['ebay_verified_product_concept'] ?? '')) === '') { return false; }
        return true;
    }

    private function output_format_slot($row, $portal, $target, $creative_type = 'banner') {
        $matrix = $this->output_slot_matrix($portal);
        $width = absint($row['width'] ?? 0);
        $height = absint($row['height'] ?? 0);
        $creative_type = sanitize_key((string) $creative_type) === 'product' ? 'product' : 'banner';
        $provisional_ebay_product = $creative_type === 'product' && $this->output_allows_provisional_ebay_product_asset($row) && ($width <= 0 || $height <= 0);
        if (($width <= 0 || $height <= 0) && !$provisional_ebay_product) {
            return new WP_Error('output_dimensions_unverified', 'Reale Bildmaße sind nicht verifiziert.');
        }
        $ratio = ($width > 0 && $height > 0) ? ($width / $height) : 0.0;
        $target_type = sanitize_key((string) ($target['type'] ?? ''));
        $target_context = sanitize_key((string) ($target['context'] ?? ''));
        $matches = array();
        foreach ($matrix as $slot_id => $rule) {
            if (!is_array($rule) || sanitize_key((string) ($rule['creative_type'] ?? '')) !== $creative_type) { continue; }
            if (!in_array($target_type, array_map('sanitize_key', (array) ($rule['target_types'] ?? array())), true)) { continue; }
            $contexts = array_map('sanitize_key', (array) ($rule['target_contexts'] ?? array()));
            if (!$contexts || $target_context === '' || !in_array($target_context, $contexts, true)) { continue; }
            if (!$provisional_ebay_product) {
                if ($width < absint($rule['min_width'] ?? 0) || $height < absint($rule['min_height'] ?? 0)) { continue; }
                if ($ratio < (float) ($rule['ratio_min'] ?? 0) || $ratio > (float) ($rule['ratio_max'] ?? 999)) { continue; }
            } elseif (sanitize_key((string)($rule['crop'] ?? '')) !== 'contain') {
                // Provisional remote product images are only safe in contain slots.
                continue;
            }
            if (method_exists($this, 'control_slot_gate')) {
                $slot_gate = $this->control_slot_gate((string) ($portal['key'] ?? ''), (string) $slot_id);
                if (is_wp_error($slot_gate)) { continue; }
            }
            $matches[$slot_id] = $rule;
        }
        $manual = $this->output_portal_decision((string) ($portal['key'] ?? ''), (string) ($row['identity_hash'] ?? ''));
        $manual_payload = is_array($manual['payload'] ?? null) ? $manual['payload'] : array();
        $fixed_slot_id = sanitize_key((string) ($manual_payload['slot_id'] ?? ''));
        if ((string) ($manual['manual_status'] ?? 'automatic') === 'approved' && $fixed_slot_id !== '') {
            if (method_exists($this, 'control_slot_gate')) {
                $fixed_slot_gate = $this->control_slot_gate((string) ($portal['key'] ?? ''), $fixed_slot_id);
                if (is_wp_error($fixed_slot_gate)) { return $fixed_slot_gate; }
            }
            if (!isset($matches[$fixed_slot_id])) {
                return new WP_Error('control_fixed_slot_invalid', 'Fest vorgegebener Designslot passt nicht zu Zielkontext oder realem Bildformat.');
            }
            return array('slot_id'=>$fixed_slot_id,'rule'=>$matches[$fixed_slot_id]);
        }
        if (!$matches) {
            return new WP_Error('output_no_design_slot', 'Kein realer Designslot passt zu Zielkontext und Bildformat.');
        }
        $priority = $creative_type === 'product'
            ? array('hub_product_1','category_product_1','journal_product_1','hub_product_2','category_product_2','journal_product_2','hub_product_3','category_product_3','journal_product_3')
            : array('start_after_topics','product_after_category_tiles','journal_banner','anzeigenmarkt_top_banner','hub_after_cards','hub_grid_card');
        foreach ($priority as $slot_id) { if (isset($matches[$slot_id])) { return array('slot_id'=>$slot_id,'rule'=>$matches[$slot_id]); } }
        $slot_id = array_key_first($matches);
        return array('slot_id'=>$slot_id,'rule'=>$matches[$slot_id]);
    }
    private function output_source_fingerprint($row, $portal, $output_type, $target, $slot_id = '') {
        $partner = $this->output_partner_evidence($row);
        $profile = is_array($partner['profile'] ?? null) ? $partner['profile'] : array();
        $data = array(
            'creative_source_hash'=>(string) ($row['source_hash'] ?? ''),
            'creative_identity'=>(string) ($row['identity_hash'] ?? ''),
            'creative_type'=>(string) ($row['creative_type'] ?? ''),
            'title'=>(string) ($row['title'] ?? ''),'description'=>(string) ($row['description'] ?? ''),'tags'=>(string) ($row['tags'] ?? ''),
            'destination_url'=>(string) ($row['destination_url'] ?? ''),'tracking_url'=>(string) ($row['tracking_url'] ?? ''),'image_url'=>(string) ($row['image_url'] ?? ''),
            'image_hash'=>$this->output_row_image_hash($row),'width'=>absint($row['width'] ?? 0),'height'=>absint($row['height'] ?? 0),
            'partner_business'=>(string) ($partner['business_label'] ?? ''),'partner_keywords'=>array_values((array) ($partner['keywords'] ?? array())),
            'partner_sector'=>(string) ($partner['primary_sector'] ?? ''),'partner_description'=>(string) ($partner['programme_description'] ?? ''),'partner_domains'=>array_values((array) ($partner['domains'] ?? array())),
            'profile_enabled'=>!empty($profile['enabled']),'profile_updated'=>absint($profile['updated_at'] ?? 0),
            'portal_key'=>(string) ($portal['key'] ?? ''),'adapter'=>(string) ($portal['adapter'] ?? ''),'adapter_version'=>(string) ($portal['adapter_version'] ?? ''),
            'domain_terms'=>array_values((array) ($portal['domain_terms'] ?? array())),'negative_terms'=>array_values((array) ($portal['negative_terms'] ?? array())),
            'output_type'=>sanitize_key((string) $output_type),'target_key'=>(string) ($target['key'] ?? ''),'target_context'=>(string) ($target['context'] ?? ''),'slot_id'=>sanitize_key((string) $slot_id),
        );
        foreach (array('partner_keywords','partner_domains','domain_terms','negative_terms') as $key) { sort($data[$key], SORT_STRING); }
        return hash('sha256', wp_json_encode($data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES));
    }

    public function output_portal_status_summary($identity_hash) {
        global $wpdb;
        $identity_hash = strtolower(sanitize_text_field((string) $identity_hash));
        if (!preg_match('/^[a-f0-9]{64}$/', $identity_hash)) { return 'Noch keine portalbezogene Planung'; }
        $rows = $wpdb->get_results($wpdb->prepare("SELECT portal_key, output_type, target_label, status FROM {$this->output_objects_table()} WHERE creative_identity_hash=%s ORDER BY portal_key, output_type", $identity_hash), ARRAY_A);
        if (!$rows) { return 'Noch keine portalbezogene Planung'; }
        $registry = $this->output_portal_registry(); $parts = array();
        foreach ((array) $rows as $row) {
            $key = sanitize_key((string) ($row['portal_key'] ?? '')); $label = sanitize_text_field((string) ($registry[$key]['label'] ?? $key));
            $parts[] = $label . ': ' . sanitize_text_field((string) ($row['output_type'] ?? '')) . ' · ' . sanitize_text_field((string) ($row['status'] ?? 'review')) . (!empty($row['target_label']) ? ' · ' . sanitize_text_field((string) $row['target_label']) : '');
        }
        return implode(' | ', $parts);
    }
    private function output_object_key($portal_key, $creative_hash, $output_type, $target_key, $slot_id = '') {
        return hash('sha256', implode('|', array($portal_key, $creative_hash, $output_type, $target_key, $slot_id)));
    }

    private function output_deactivate_materialized_object($row, $reason = 'Ausgabe ersetzt oder gesperrt.') {
        if (!is_array($row)) {
            return;
        }
        $portal = $this->output_portal_by_key((string) ($row['portal_key'] ?? ''), true);
        if (is_wp_error($portal)) {
            return;
        }
        $adapter = sanitize_key((string) ($portal['adapter'] ?? ''));
        if (in_array($adapter, array('wordpress_local','wordpress_multisite'), true)) {
            $this->output_with_portal($portal, function() use ($row) {
                $campaign_id = absint($row['campaign_post_id'] ?? 0);
                if ($campaign_id > 0) {
                    $campaign = $this->output_campaign_by_post_id($campaign_id);
                    if (is_array($campaign)) {
                        $campaign['active'] = false;
                        $this->save_campaign_record($campaign, $campaign_id);
                    }
                }
                $listing_id = absint($row['listing_post_id'] ?? 0);
                if ($listing_id > 0 && function_exists('get_post') && function_exists('wp_update_post')) {
                    $listing = get_post($listing_id);
                    if ($listing && (string) $listing->post_status === 'publish') {
                        wp_update_post(array('ID'=>$listing_id,'post_status'=>'draft'));
                    }
                }
                return true;
            });
        } else {
            $callbacks = is_array($portal['callbacks'] ?? null) ? $portal['callbacks'] : array();
            if (!empty($callbacks['deactivate']) && is_callable($callbacks['deactivate'])) {
                call_user_func($callbacks['deactivate'], $row, $portal, $reason);
            }
        }
    }

    private function output_supersede_conflicting_objects($data, $object_key) {
        global $wpdb;
        $table = $this->output_objects_table();
        $rows = $wpdb->get_results($wpdb->prepare(
            "SELECT * FROM {$table} WHERE portal_key=%s AND creative_identity_hash=%s AND output_type=%s AND object_key<>%s AND status NOT IN ('superseded','blocked_manual')",
            (string) ($data['portal_key'] ?? ''),
            (string) ($data['creative_identity_hash'] ?? ''),
            (string) ($data['output_type'] ?? ''),
            (string) $object_key
        ), ARRAY_A);
        foreach ((array) $rows as $row) {
            $this->output_deactivate_materialized_object($row, 'Durch neu bewertetes Ausgabeobjekt ersetzt.');
            $wpdb->update($table, array(
                'status'=>'superseded',
                'decision_reason'=>'Durch neu bewertetes Ziel, Format oder Creative ersetzt.',
                'updated_at'=>time(),
            ), array('id'=>absint($row['id'])));
        }
    }

    private function output_object_upsert($data) {
        global $wpdb;
        $table = $this->output_objects_table(); $now = time();
        $data = wp_parse_args((array) $data, array(
            'portal_key'=>'','portal_adapter'=>'','creative_identity_hash'=>'','provider'=>'','partner_external_id'=>'','output_type'=>'','target_type'=>'','target_key'=>'','target_label'=>'','slot_id'=>'','status'=>'review','confidence'=>0,'decision_source'=>'','decision_reason'=>'','campaign_post_id'=>0,'listing_post_id'=>0,'tracking_url'=>'','image_url'=>'','image_width'=>0,'image_height'=>0,'image_hash'=>'','source_fingerprint'=>'','payload'=>'','last_verified'=>0,'created_at'=>$now,'updated_at'=>$now,
        ));
        $data['object_key'] = $this->output_object_key($data['portal_key'], $data['creative_identity_hash'], $data['output_type'], $data['target_key'], $data['slot_id']);
        // Atomic replacement: conflicting published output is superseded only
        // AFTER the new object has been materialized successfully.
        $existing = $wpdb->get_row($wpdb->prepare("SELECT * FROM {$table} WHERE object_key=%s", $data['object_key']), ARRAY_A);
        if ($existing) {
            $data['created_at'] = absint($existing['created_at'] ?? $now);
            $content_changed = (string) ($existing['source_fingerprint'] ?? '') === '' || !hash_equals((string) ($existing['source_fingerprint'] ?? ''), (string) ($data['source_fingerprint'] ?? ''));
            $incoming_status = sanitize_key((string) ($data['status'] ?? 'review'));
            $incoming_blocked = strpos($incoming_status, 'blocked') === 0 || in_array($incoming_status, array('quarantine','stale','ended'), true);
            if (in_array((string) ($existing['status'] ?? ''), array('blocked_manual','paused_manual'), true)) {
                $data['status'] = (string) $existing['status'];
            } elseif ((string) ($existing['status'] ?? '') === 'published' && $incoming_blocked) {
                $this->output_deactivate_materialized_object($existing, (string) ($data['decision_reason'] ?? 'Creative-Quelle wurde gesperrt.'));
                $data['status'] = $incoming_status;
            } elseif ((string) ($existing['status'] ?? '') === 'published' && !$content_changed) {
                $data['status'] = 'published';
            } elseif ((string) ($existing['status'] ?? '') === 'published' && $content_changed) {
                // Keep the currently published campaign live while the same
                // object is updated. The materializer writes the replacement to
                // the same campaign; a failure therefore leaves Last-Known-Good
                // visible instead of creating a frontend outage.
                $data['status'] = 'published';
                $data['decision_reason'] = 'Quelldaten geändert; Last-Known-Good bleibt bis zur erfolgreichen atomaren Aktualisierung veröffentlicht.';
            }
            $data['campaign_post_id'] = absint($existing['campaign_post_id'] ?? ($data['campaign_post_id'] ?? 0));
            $data['listing_post_id'] = absint($existing['listing_post_id'] ?? ($data['listing_post_id'] ?? 0));
            $wpdb->update($table, $data, array('id'=>absint($existing['id'])));
            return absint($existing['id']);
        }
        $wpdb->insert($table, $data);
        return absint($wpdb->insert_id);
    }
    private function output_campaign_by_post_id($post_id) {
        $post_id = absint($post_id);
        if ($post_id <= 0 || !method_exists($this, 'get_campaigns')) {
            return null;
        }
        foreach ((array) $this->get_campaigns() as $campaign) {
            if (is_array($campaign) && absint($campaign['post_id'] ?? 0) === $post_id) {
                return $campaign;
            }
        }
        return null;
    }

    public function output_block_creative($identity_hash, $reason = 'Creative gesperrt.', $portal_key = '') {
        $identity_hash = strtolower(sanitize_text_field((string) $identity_hash));
        $portal_key = sanitize_key((string) ($portal_key !== '' ? $portal_key : $this->output_local_portal_key()));
        if (!preg_match('/^[a-f0-9]{64}$/', $identity_hash) || $portal_key === '') {
            return 0;
        }
        $decision = $this->output_set_portal_decision($portal_key, $identity_hash, 'veto', $reason);
        if (is_wp_error($decision)) {
            return 0;
        }
        global $wpdb;
        $table = $this->output_objects_table();
        $rows = $wpdb->get_results($wpdb->prepare("SELECT * FROM {$table} WHERE portal_key=%s AND creative_identity_hash=%s", $portal_key, $identity_hash), ARRAY_A);
        foreach ((array) $rows as $row) {
            $this->output_deactivate_materialized_object($row, $reason);
        }
        $wpdb->update($table, array('status'=>'blocked_manual','decision_source'=>'manual_veto','decision_reason'=>sanitize_text_field((string) $reason),'updated_at'=>time()), array('portal_key'=>$portal_key,'creative_identity_hash'=>$identity_hash));
        return count((array) $rows);
    }

    private function output_creative_row($identity_hash) {
        global $wpdb;
        $table = $this->creative_library_table();
        return $wpdb->get_row($wpdb->prepare("SELECT * FROM {$table} WHERE identity_hash=%s", sanitize_text_field((string) $identity_hash)), ARRAY_A);
    }

    private function output_listing_image_size() {
        if (!function_exists('wp_get_registered_image_subsizes')) {
            return new WP_Error('listing_image_sizes_unavailable', 'WordPress-Bildgrößen sind nicht verfügbar.');
        }
        $sizes = wp_get_registered_image_subsizes();
        foreach (array('hp_landscape_large','hp_landscape_small','hp_listing_image','hp_large') as $name) {
            if (!empty($sizes[$name]['width']) && !empty($sizes[$name]['height'])) {
                return array('name'=>$name,'width'=>absint($sizes[$name]['width']),'height'=>absint($sizes[$name]['height']));
            }
        }
        return new WP_Error('listing_image_size_missing', 'Keine registrierte HivePress-Listingbildgröße gefunden.');
    }
    private function output_listing_asset_compatibility($row, $portal = null) {
        if (is_array($portal)) {
            $adapter = sanitize_key((string) ($portal['adapter'] ?? ''));
            if (!in_array($adapter, array('wordpress_local','wordpress_multisite'), true)) {
                $callbacks = is_array($portal['callbacks'] ?? null) ? $portal['callbacks'] : array();
                if (empty($callbacks['validate_listing_asset']) || !is_callable($callbacks['validate_listing_asset'])) {
                    return new WP_Error('portal_listing_asset_validator_missing', 'Externer Portaladapter besitzt keine bestätigte Listing-Bildprüfung.');
                }
                $checked = call_user_func($callbacks['validate_listing_asset'], $row, $portal, self::PORTAL_ADAPTER_VERSION);
                return is_array($checked) ? $checked : (is_wp_error($checked) ? $checked : new WP_Error('portal_listing_asset_invalid', 'Externe Listing-Bildprüfung lieferte kein belastbares Ergebnis.'));
            }
            $result = $this->output_with_portal($portal, function() use ($row) { return $this->output_listing_asset_compatibility($row, null); });
            return $result;
        }
        $size = $this->output_listing_image_size();
        if (is_wp_error($size)) { return $size; }
        $width = absint($row['width'] ?? 0); $height = absint($row['height'] ?? 0);
        $payload = json_decode((string) ($row['payload'] ?? ''), true); $payload = is_array($payload) ? $payload : array();
        if (!in_array((string) ($payload['_dimension_state'] ?? ''), array('verified','mismatch'), true) || $width <= 0 || $height <= 0 || $this->output_row_image_hash($row) === '') {
            return new WP_Error('listing_image_unverified', 'Listingbild ist nicht real vermessen und verifiziert.');
        }
        $target_width = absint($size['width'] ?? 0); $target_height = absint($size['height'] ?? 0);
        if ($target_width <= 0 || $target_height <= 0) { return new WP_Error('listing_image_size_invalid', 'HivePress-Listingbildgröße ist ungültig.'); }
        $source_ratio = $width / $height; $target_ratio = $target_width / $target_height;
        $ratio_deviation = abs($source_ratio - $target_ratio) / $target_ratio;
        if ($source_ratio < 0.70 || $source_ratio > 2.40 || $ratio_deviation > 0.30) {
            return new WP_Error('listing_image_format_incompatible', 'Creative-Format passt nicht sicher zum registrierten HivePress-Listingbild. Ein passendes Kartenformat ist erforderlich.');
        }
        if ($width < min(300, $target_width) || $height < min(180, $target_height)) {
            return new WP_Error('listing_image_resolution_too_small', 'Creative-Auflösung ist für ein HivePress-Listing zu klein.');
        }
        return array('size'=>$size,'source_width'=>$width,'source_height'=>$height,'ratio_deviation'=>$ratio_deviation);
    }
    private function output_sideload_creative_image($listing_id, $row) {
        $listing_id = absint($listing_id);
        $image_url = esc_url_raw((string) ($row['image_url'] ?? ''));
        if ($listing_id <= 0 || $image_url === '') {
            return new WP_Error('listing_creative_image_missing', 'Creative-Bild fehlt.');
        }
        $compatibility = $this->output_listing_asset_compatibility($row, null);
        if (is_wp_error($compatibility)) {
            return $compatibility;
        }
        $size = $compatibility['size'];
        if (!function_exists('media_sideload_image')) {
            foreach (array('file.php','media.php','image.php') as $file) {
                $path = ABSPATH . 'wp-admin/includes/' . $file;
                if (is_readable($path)) {
                    require_once $path;
                }
            }
        }
        if (!function_exists('media_sideload_image') || !function_exists('set_post_thumbnail')) {
            return new WP_Error('listing_media_api_missing', 'WordPress-Medienfunktionen sind nicht verfügbar.');
        }
        $expected_image_hash = $this->output_row_image_hash($row);
        $thumb = function_exists('get_post_thumbnail_id') ? absint(get_post_thumbnail_id($listing_id)) : 0;
        $old_source = $thumb > 0 ? (string) get_post_meta($thumb, '_ppar_creative_source_url', true) : '';
        $old_image_hash = $thumb > 0 ? (string) get_post_meta($thumb, '_ppar_creative_image_hash', true) : '';
        if ($thumb > 0 && $old_source === $image_url && $expected_image_hash !== '' && hash_equals($expected_image_hash, $old_image_hash)) {
            return array('attachment_id'=>$thumb,'size'=>$size,'reused'=>true);
        }
        $attachment_id = media_sideload_image($image_url, $listing_id, sanitize_text_field((string) ($row['title'] ?? $row['partner_name'] ?? 'Affiliate-Creative')), 'id');
        if (is_wp_error($attachment_id)) {
            return $attachment_id;
        }
        if (!set_post_thumbnail($listing_id, absint($attachment_id))) {
            return new WP_Error('listing_thumbnail_failed', 'Creative-Bild konnte nicht als Listingbild gesetzt werden.');
        }
        update_post_meta(absint($attachment_id), '_ppar_creative_source_url', $image_url);
        update_post_meta(absint($attachment_id), '_ppar_creative_identity_hash', sanitize_text_field((string) ($row['identity_hash'] ?? '')));
        update_post_meta(absint($attachment_id), '_ppar_creative_image_hash', $expected_image_hash);
        return array('attachment_id'=>absint($attachment_id),'size'=>$size);
    }

    private function output_materialize_listing($object_id, $portal, $row, $classification) {
        $target = is_array($classification['target'] ?? null) ? $classification['target'] : array();
        if ((string) ($target['type'] ?? '') !== 'hp_listing_category' || absint($target['id'] ?? 0) <= 0) {
            return new WP_Error('listing_target_invalid', 'Eindeutige HivePress-Kategorie fehlt.');
        }
        if (!function_exists('post_type_exists') || !post_type_exists('hp_listing') || !function_exists('taxonomy_exists') || !taxonomy_exists('hp_listing_category')) {
            return new WP_Error('listing_hivepress_missing', 'HivePress-Listingmodell ist nicht verfügbar.');
        }
        $tracking_url = esc_url_raw((string) ($row['tracking_url'] ?? ''));
        if ($tracking_url === '' || !wp_http_validate_url($tracking_url)) {
            return new WP_Error('listing_tracking_invalid', 'Originaler Creative-Trackinglink fehlt oder ist ungültig.');
        }
        $partner = $this->output_partner_evidence($row);
        $business = sanitize_text_field((string) $partner['business_label']);
        if ($business === '') {
            return new WP_Error('listing_business_missing', 'Bestätigter Geschäftsbereich fehlt.');
        }
        $title = trim(sanitize_text_field((string) ($row['partner_name'] ?? '')) . ' – ' . $business, " –\t\n\r\0\x0B");
        $description = sanitize_textarea_field((string) ($row['description'] ?? ''));
        $content = '<p><strong>Angebot:</strong> ' . esc_html($business) . '</p>';
        if ($description !== '' && $description !== (string) ($row['title'] ?? '')) {
            $content .= '<p>' . esc_html($description) . '</p>';
        }
        $content .= '<p class="ppar-listing-creative"><a href="' . esc_url($tracking_url) . '" rel="sponsored nofollow noopener" target="_blank"><img src="' . esc_url((string) ($row['image_url'] ?? '')) . '" alt="' . esc_attr((string) ($row['title'] ?? $business)) . '" loading="lazy" decoding="async"></a></p>';
        global $wpdb;
        $table = $this->output_objects_table();
        $stored = $wpdb->get_row($wpdb->prepare("SELECT * FROM {$table} WHERE id=%d", absint($object_id)), ARRAY_A);
        $listing_id = absint($stored['listing_post_id'] ?? 0);
        if ($listing_id <= 0 && function_exists('get_posts')) {
            $ids = get_posts(array('post_type'=>'hp_listing','post_status'=>array('draft','pending','publish','private'),'meta_key'=>'_ppar_output_object_key','meta_value'=>(string) ($stored['object_key'] ?? ''),'posts_per_page'=>1,'fields'=>'ids'));
            $listing_id = $ids ? absint($ids[0]) : 0;
        }
        $post_data = array(
            'post_type'=>'hp_listing',
            'post_title'=>$title,
            'post_content'=>$content,
            'post_excerpt'=>$business,
            'post_status'=>'draft',
        );
        if ($listing_id > 0) {
            $current = get_post($listing_id);
            if ($current && (string) $current->post_status === 'publish' && (string) ($stored['status'] ?? '') === 'published') {
                $post_data['post_status'] = 'publish';
            }
            $post_data['ID'] = $listing_id;
            $result = wp_update_post($post_data, true);
        } else {
            $result = wp_insert_post($post_data, true);
        }
        if (is_wp_error($result) || absint($result) <= 0) {
            return is_wp_error($result) ? $result : new WP_Error('listing_save_failed', 'HivePress-Listing konnte nicht gespeichert werden.');
        }
        $listing_id = absint($result);
        $term_result = wp_set_post_terms($listing_id, array(absint($target['id'])), 'hp_listing_category', false);
        if (is_wp_error($term_result)) {
            return $term_result;
        }
        update_post_meta($listing_id, 'hp_url', $tracking_url);
        $read_back = (string) get_post_meta($listing_id, 'hp_url', true);
        if ($read_back !== $tracking_url) {
            return new WP_Error('listing_tracking_roundtrip', 'Der originale Trackinglink wurde nicht zeichengetreu gespeichert.');
        }
        update_post_meta($listing_id, '_ppar_output_object_key', sanitize_text_field((string) ($stored['object_key'] ?? '')));
        update_post_meta($listing_id, '_ppar_creative_identity_hash', sanitize_text_field((string) ($row['identity_hash'] ?? '')));
        update_post_meta($listing_id, '_ppar_partner_identity', sanitize_key((string) ($row['provider'] ?? '')) . ':' . sanitize_text_field((string) ($row['partner_external_id'] ?? '')));
        update_post_meta($listing_id, '_ppar_tracking_source', 'creative_original');
        $image = $this->output_sideload_creative_image($listing_id, $row);
        if (is_wp_error($image)) {
            return $image;
        }
        $preview = function_exists('get_preview_post_link') ? get_preview_post_link($listing_id) : add_query_arg('preview', 'true', get_permalink($listing_id));
        $wpdb->update($table, array(
            'listing_post_id'=>$listing_id,
            'status'=>get_post_status($listing_id) === 'publish' ? 'published' : 'draft',
            'decision_reason'=>'Listing aus dem verknüpften Creative erzeugt; Original-Trackinglink gespeichert.',
            'payload'=>wp_json_encode(array('preview_url'=>$preview,'image_size'=>$image['size'] ?? array()), JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES),
            'last_verified'=>time(),
            'updated_at'=>time(),
        ), array('id'=>absint($object_id)));
        return array('listing_id'=>$listing_id,'preview_url'=>$preview);
    }

    private function output_campaign_target_key($target) {
        $slug = sanitize_key((string) ($target['slug'] ?? ''));
        $type = sanitize_key((string) ($target['type'] ?? ''));
        $context = sanitize_key((string) ($target['context'] ?? ''));
        if ($context === 'journal') { return $slug !== '' ? 'journal:' . $slug : ''; }
        if ($context === 'anzeigenmarkt') { return 'market:anzeigenmarkt'; }
        if ($type === 'category') { return $slug !== '' ? 'category:' . $slug : ''; }
        if ($type === 'page') { return $slug !== '' ? 'page:' . $slug : ''; }
        return '';
    }

    private function output_save_local_campaign($object_id, $row, $classification, $slot, $output_type) {
        global $wpdb;
        $object = $wpdb->get_row($wpdb->prepare("SELECT * FROM {$this->output_objects_table()} WHERE id=%d", absint($object_id)), ARRAY_A);
        if (!is_array($object)) { return new WP_Error('output_object_missing', 'Ausgabeobjekt fehlt.'); }
        $target = is_array($classification['target'] ?? null) ? $classification['target'] : array();
        $target_key = $this->output_campaign_target_key($target);
        $slot_id = sanitize_key((string) ($slot['slot_id'] ?? ''));
        if ($target_key === '' || $slot_id === '') { return new WP_Error('campaign_exact_target_missing', 'Exaktes Portalziel oder Designslot fehlt.'); }
        $tracking_url = esc_url_raw((string) ($row['tracking_url'] ?? ''));
        if ($tracking_url === '' || !wp_http_validate_url($tracking_url)) { return new WP_Error('campaign_tracking_missing', 'Originaler Trackinglink fehlt.'); }
        $campaign_id = absint($object['campaign_post_id'] ?? 0);
        if ($campaign_id <= 0 && function_exists('get_posts')) {
            $ids = get_posts(array('post_type'=>self::CAMPAIGN_POST_TYPE,'post_status'=>array('publish','draft','private'),'meta_key'=>'_ppar_output_object_key','meta_value'=>(string) ($object['object_key'] ?? ''),'posts_per_page'=>1,'fields'=>'ids'));
            $campaign_id = $ids ? absint($ids[0]) : 0;
        }
        $payload = json_decode((string) ($row['payload'] ?? ''), true); $payload = is_array($payload) ? $payload : array();
        $campaign = $this->central_blank_campaign();
        $campaign['id'] = sanitize_key('output-' . substr((string) ($object['object_key'] ?? ''), 0, 24));
        $campaign['name'] = sanitize_text_field(trim((string) ($row['partner_name'] ?? '') . ' – ' . (string) ($row['title'] ?? ''), " –\t\n\r\0\x0B"));
        $campaign['partner'] = sanitize_text_field((string) ($row['partner_name'] ?? ''));
        $campaign['creative_type'] = $output_type === 'product_campaign' ? 'product' : 'banner';
        $campaign['network'] = sanitize_key((string) ($row['provider'] ?? 'manual'));
        $campaign['advertiser_id'] = sanitize_text_field((string) ($row['partner_external_id'] ?? ''));
        $campaign['programme_name'] = sanitize_text_field((string) ($row['partner_name'] ?? ''));
        $campaign['programme_status'] = 'active'; $campaign['programme_status_source'] = 'output_object'; $campaign['programme_status_checked_at'] = time();
        $campaign['quality_manual_status'] = 'auto_verified'; $campaign['render_mode'] = 'image_link';
        $campaign['dimensions'] = absint($row['width'] ?? 0) . 'x' . absint($row['height'] ?? 0);
        $is_ebay_campaign = sanitize_key((string) ($row['provider'] ?? '')) === 'ebay';
        $auto_ebay_business = $output_type === 'product_campaign'
            && $is_ebay_campaign
            && sanitize_key((string) ($row['source_kind'] ?? '')) === 'ebay_business_item'
            && in_array(sanitize_key((string) ($classification['source'] ?? '')), array('ebay_verified_product_concept','ebay_verified_product_target'), true)
            && method_exists($this, 'ebay_business_product_contract')
            && !empty($this->ebay_business_product_contract($row));
        $campaign['active'] = $auto_ebay_business; $campaign['assignment_mode'] = 'page_tree'; $campaign['match_descendants'] = false;
        $auto_targets = $auto_ebay_business && method_exists($this, 'ebay_business_campaign_target_keys') ? $this->ebay_business_campaign_target_keys($row, $target) : array();
        $auto_placements = $auto_ebay_business && method_exists($this, 'ebay_business_campaign_placements') ? $this->ebay_business_campaign_placements($row) : array();
        $campaign['automation_target_keys'] = $auto_targets ? $auto_targets : array($target_key);
        $campaign['placements'] = $auto_placements ? $auto_placements : array($slot_id);
        $campaign['priority'] = $auto_ebay_business ? absint($payload['ebay_quality_score'] ?? ($classification['confidence'] ?? 0)) : absint($campaign['priority'] ?? 0);
        $campaign['auto_topic_label'] = sanitize_text_field((string) ($target['label'] ?? '')); $campaign['auto_topic_score'] = absint($classification['confidence'] ?? 0); $campaign['auto_topic_reason'] = sanitize_text_field((string) ($classification['reason'] ?? ''));
        $campaign['label'] = $output_type === 'product_campaign' ? ($is_ebay_campaign ? 'eBay-Angebot · Affiliate' : 'Produktvorschlag') : 'Ausgewählter Partner';
        $campaign['ebay_content_isolated'] = $is_ebay_campaign && $output_type === 'product_campaign';
        $campaign['title'] = sanitize_text_field((string) ($row['title'] ?? '')); $campaign['description'] = sanitize_textarea_field((string) ($row['description'] ?? ''));
        $campaign['price'] = sanitize_text_field((string) ($payload['price'] ?? '')); $campaign['currency'] = strtoupper(substr(sanitize_text_field((string) ($payload['currency'] ?? 'EUR')), 0, 10)); $campaign['availability'] = sanitize_text_field((string) ($payload['availability'] ?? ''));
        $campaign['voucher_code'] = sanitize_text_field((string) ($payload['voucher_code'] ?? '')); $campaign['start_date'] = method_exists($this,'automation_normalize_date') ? $this->automation_normalize_date($payload['start_date'] ?? '') : ''; $campaign['end_date'] = method_exists($this,'automation_normalize_date') ? $this->automation_normalize_date($payload['end_date'] ?? '') : '';
        $campaign['image_url'] = esc_url_raw((string) ($row['image_url'] ?? '')); $campaign['url'] = $tracking_url; $campaign['destination_url'] = esc_url_raw((string) ($row['destination_url'] ?? '')); $campaign['subid_param'] = ''; $campaign['target'] = '_blank'; $campaign['required_url_fragment'] = ''; $campaign['health_check_enabled'] = true; $campaign['source'] = 'output_object_v4'; $campaign['last_synced'] = time(); $campaign['external_id'] = sanitize_text_field((string) ($row['external_id'] ?? ''));
        $saved = $this->save_campaign_record($campaign, $campaign_id);
        if (is_wp_error($saved) || !$saved) { return is_wp_error($saved) ? $saved : new WP_Error('campaign_save_failed', 'Kampagne konnte nicht gespeichert werden.'); }
        $campaign_id = absint($saved);
        update_post_meta($campaign_id, '_ppar_output_object_key', sanitize_text_field((string) ($object['object_key'] ?? '')));
        update_post_meta($campaign_id, 'ppar_output_object_id', absint($object_id));
        update_post_meta($campaign_id, '_ppar_creative_identity_hash', sanitize_text_field((string) ($row['identity_hash'] ?? '')));
        if ($auto_ebay_business) {
            update_post_meta($campaign_id, '_ppar_ebay_business_auto', 1);
            update_post_meta($campaign_id, '_ppar_ebay_product_slug', sanitize_title((string) ($payload['ebay_verified_product_slug'] ?? '')));
            update_post_meta($campaign_id, '_ppar_ebay_business_match_contract', 'concept_v3');
            update_post_meta($campaign_id, '_ppar_ebay_quality_score', absint($payload['ebay_quality_score'] ?? 0));
            update_post_meta($campaign_id, '_ppar_ebay_quality_reason', sanitize_text_field((string) ($payload['ebay_quality_reason'] ?? '')));
            update_post_meta($campaign_id, '_ppar_ebay_seller_username', sanitize_text_field((string) ($payload['ebay_seller_username'] ?? '')));
            update_post_meta($campaign_id, '_ppar_ebay_brand', sanitize_text_field((string) ($payload['ebay_brand'] ?? '')));
        } elseif ($is_ebay_campaign && $output_type === 'product_campaign') {
            delete_post_meta($campaign_id, '_ppar_ebay_business_match_contract');
        }
        $wpdb->update($this->output_objects_table(), array(
            'campaign_post_id'=>$campaign_id,
            'status'=>$auto_ebay_business ? 'published' : 'draft',
            'decision_source'=>$auto_ebay_business ? 'ebay_verified_product_concept' : (string) ($object['decision_source'] ?? 'automatic'),
            'decision_reason'=>$auto_ebay_business ? 'Verifiziertes eBay-BUSINESS-Produkt automatisch in den freigegebenen Produktslots aktiviert.' : 'Inaktive Kampagne aus exakt verknüpftem Creative, Ziel und Designslot vorbereitet.',
            'last_verified'=>time(),'updated_at'=>time()
        ), array('id'=>absint($object_id)));
        return array('campaign_id'=>$campaign_id,'active'=>$auto_ebay_business);
    }
    private function output_materialize_banner($object_id, $portal, $row, $classification, $slot) {
        return $this->output_save_local_campaign($object_id, $row, $classification, $slot, 'portal_banner');
    }
    private function output_materialize_product($object_id, $portal, $row, $classification, $slot) {
        return $this->output_save_local_campaign($object_id, $row, $classification, $slot, 'product_campaign');
    }
    private function output_materialize_external($object_id, $portal, $row, $classification, $slot, $output_type) {
        $callbacks = is_array($portal['callbacks'] ?? null) ? $portal['callbacks'] : array();
        $callback_name = $output_type === 'portal_banner' ? 'materialize_banner' : ($output_type === 'product_campaign' ? 'materialize_product' : 'materialize_listing');
        if (empty($callbacks[$callback_name]) || !is_callable($callbacks[$callback_name])) {
            return new WP_Error('portal_materializer_missing', 'Externer Portaladapter besitzt keinen freigegebenen Materialisierer für diesen Ausgabetyp.');
        }
        $result = call_user_func($callbacks[$callback_name], array(
            'object_id'=>absint($object_id),
            'portal'=>$portal,
            'creative'=>$row,
            'classification'=>$classification,
            'slot'=>$slot,
            'tracking_url'=>(string) ($row['tracking_url'] ?? ''),
            'image_url'=>(string) ($row['image_url'] ?? ''),
        ));
        if (is_wp_error($result)) {
            return $result;
        }
        if (!is_array($result) || empty($result['external_reference'])) {
            return new WP_Error('portal_materializer_invalid', 'Externer Portaladapter lieferte keine eindeutige Referenz.');
        }
        global $wpdb;
        $wpdb->update($this->output_objects_table(), array(
            'status'=>'draft',
            'decision_reason'=>'Entwurf über freigegebenen externen Portaladapter vorbereitet.',
            'payload'=>wp_json_encode(array(
                'external_reference'=>sanitize_text_field((string) $result['external_reference']),
                'preview_url'=>esc_url_raw((string) ($result['preview_url'] ?? '')),
                'slot_rule'=>$slot['rule'] ?? array(),
            ), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES),
            'last_verified'=>time(),
            'updated_at'=>time(),
        ), array('id'=>absint($object_id)));
        return $result;
    }

    public function output_plan_creative($row, $materialize = true) {
        global $wpdb;
        $this->maybe_install_output_objects_schema();
        $portals = $this->output_portal_registry();
        $result = array('created'=>0,'drafts'=>0,'active'=>0,'blocked'=>0,'review'=>0,'errors'=>array());
        // Digistore24 tracking is credential-bound. Reject a stale, foreign or
        // otherwise invalid vendor link before classification/upsert/materialization
        // so a bad refresh cannot overwrite a Last-Known-Good banner draft/campaign.
        // Other providers do not enter this provider-specific gate.
        if (sanitize_key((string) ($row['provider'] ?? '')) === 'digistore24') {
            if (!method_exists($this, 'digistore24_tracking_url_allowed') || !$this->digistore24_tracking_url_allowed((string) ($row['tracking_url'] ?? ''))) {
                $result['blocked'] = 1;
                $result['errors']['output_digistore24_tracking_invalid'] = 'Digistore24-Ausgabe besitzt keinen aktuell geprüften, provisionssicheren Trackinglink.';
                return $result;
            }
            if (!method_exists($this, 'digistore24_is_https_url') || !$this->digistore24_is_https_url((string) ($row['image_url'] ?? ''))) {
                $result['blocked'] = 1;
                $result['errors']['output_digistore24_image_invalid'] = 'Digistore24-Banner besitzt keine verifizierbare HTTPS-Bildquelle.';
                return $result;
            }
        }
        foreach ($portals as $portal) {
            if (empty($portal['enabled'])) { continue; }
            if (method_exists($this, 'control_partner_gate')) {
                $gate = $this->control_partner_gate($row, $portal);
                if (is_wp_error($gate)) { $result['blocked']++; $result['errors'][$gate->get_error_code()]=$gate->get_error_message(); continue; }
            }
            $valid = $this->output_validate_portal_profile($portal);
            if (is_wp_error($valid)) { $result['blocked']++; $result['errors'][$valid->get_error_code()]=$valid->get_error_message(); continue; }
            $output_types = array_values(array_intersect(array_unique(array_filter(array_map('sanitize_key', (array) ($portal['output_types'] ?? array())))), array('portal_banner','product_campaign','hivepress_listing','portal_listing')));
            $creative_type = sanitize_key((string) ($row['creative_type'] ?? 'banner'));
            if ($creative_type === 'product') { $output_types = array_values(array_intersect($output_types, array('product_campaign'))); }
            elseif ($creative_type === 'banner') { $output_types = array_values(array_intersect($output_types, array('portal_banner','hivepress_listing','portal_listing'))); }
            else { $result['review']++; $result['errors']['output_type_unsupported']='Creative-Typ besitzt noch keinen bestätigten Ausgabeweg.'; continue; }
            // Digistore24 is contractually banner-only. This provider-specific
            // hardlock must not alter any output path for other providers.
            if (sanitize_key((string) ($row['provider'] ?? '')) === 'digistore24') {
                $output_types = array_values(array_intersect($output_types, array('portal_banner')));
            }
            foreach ($output_types as $output_type) {
                $classification = $this->output_classify_for_portal($row, $portal, $output_type);
                if (is_wp_error($classification)) { $result['blocked']++; $result['errors'][$classification->get_error_code()]=$classification->get_error_message(); continue; }
                $target = is_array($classification['target'] ?? null) ? $classification['target'] : array();
                $slot = array('slot_id'=>''); $status = sanitize_key((string) ($classification['status'] ?? 'review'));
                if ($status === 'blocked' && sanitize_key((string) ($classification['source'] ?? '')) === 'source_state') { $status = 'blocked_source'; }
                if (in_array($output_type, array('portal_banner','product_campaign'), true) && $status === 'ready') {
                    $slot = $this->output_format_slot($row, $portal, $target, $output_type === 'product_campaign' ? 'product' : 'banner');
                    if (is_wp_error($slot)) { $status='blocked_format'; $classification['reason']=$slot->get_error_message(); $slot=array('slot_id'=>''); }
                }
                if (in_array($output_type, array('hivepress_listing','portal_listing'), true) && $status === 'ready') {
                    $listing_format = $this->output_listing_asset_compatibility($row, $portal);
                    if (is_wp_error($listing_format)) { $status='blocked_format'; $classification['reason']=$listing_format->get_error_message(); }
                }
                $fingerprint = $this->output_source_fingerprint($row, $portal, $output_type, $target, (string) ($slot['slot_id'] ?? ''));
                $object_data = array(
                    'portal_key'=>(string) ($portal['key'] ?? ''),'portal_adapter'=>(string) ($portal['adapter'] ?? ''),'creative_identity_hash'=>(string) ($row['identity_hash'] ?? ''),'provider'=>(string) ($row['provider'] ?? ''),'partner_external_id'=>(string) ($row['partner_external_id'] ?? ''),'output_type'=>$output_type,'target_type'=>(string) ($target['type'] ?? ''),'target_key'=>(string) ($target['key'] ?? ''),'target_label'=>(string) ($target['label'] ?? ''),'slot_id'=>(string) ($slot['slot_id'] ?? ''),'status'=>$status,'confidence'=>absint($classification['confidence'] ?? 0),'decision_source'=>(string) ($classification['source'] ?? 'automatic'),'decision_reason'=>(string) ($classification['reason'] ?? ''),'tracking_url'=>(string) ($row['tracking_url'] ?? ''),'image_url'=>(string) ($row['image_url'] ?? ''),'image_width'=>absint($row['width'] ?? 0),'image_height'=>absint($row['height'] ?? 0),'image_hash'=>$this->output_row_image_hash($row),'source_fingerprint'=>$fingerprint,'payload'=>wp_json_encode(array('alternatives'=>$classification['alternatives'] ?? array(),'slot_rule'=>$slot['rule'] ?? array(),'target_context'=>$target['context'] ?? ''), JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES),'last_verified'=>time(),
                );
                $object_id = $this->output_object_upsert($object_data);
                $result['created']++;
                if ($status !== 'ready') { if (strpos($status,'blocked')===0) {$result['blocked']++;} else {$result['review']++;} continue; }
                if (!$materialize) { $result['review']++; continue; }
                $adapter = sanitize_key((string) ($portal['adapter'] ?? ''));
                if (in_array($adapter, array('wordpress_local','wordpress_multisite'), true)) {
                    $made = $this->output_with_portal($portal, function() use ($object_id,$portal,$row,$classification,$slot,$output_type) {
                        if ($output_type === 'portal_banner') { return $this->output_materialize_banner($object_id,$portal,$row,$classification,$slot); }
                        if ($output_type === 'product_campaign') { return $this->output_materialize_product($object_id,$portal,$row,$classification,$slot); }
                        if ($output_type !== 'hivepress_listing') { return new WP_Error('local_listing_adapter_unsupported','Lokaler WordPress-Adapter unterstützt nur bestätigte Kampagnen und HivePress-Listings.'); }
                        return $this->output_materialize_listing($object_id,$portal,$row,$classification);
                    });
                } else {
                    $made = $this->output_materialize_external($object_id,$portal,$row,$classification,$slot,$output_type);
                }
                if (is_wp_error($made)) {
                    global $wpdb;
                    $current_object = $wpdb->get_row($wpdb->prepare("SELECT * FROM {$this->output_objects_table()} WHERE id=%d", absint($object_id)), ARRAY_A);
                    $has_last_good = is_array($current_object) && (string)($current_object['status'] ?? '') === 'published' && absint($current_object['campaign_post_id'] ?? 0) > 0;
                    $wpdb->update($this->output_objects_table(), array(
                        'status'=>$has_last_good ? 'published' : 'blocked_runtime',
                        'decision_reason'=>$has_last_good ? 'Aktualisierung fehlgeschlagen; Last-Known-Good bleibt veröffentlicht: ' . $made->get_error_message() : $made->get_error_message(),
                        'updated_at'=>time(),
                    ), array('id'=>absint($object_id)));
                    $result['blocked']++; $result['errors'][$made->get_error_code()]=$made->get_error_message();
                } else {
                    $result['drafts']++;
                    if (is_array($made) && !empty($made['active'])) { $result['active']++; }
                    // Only now may an older object for another target/slot be
                    // retired. This is the commit point of the atomic swap.
                    $materialized_object = $wpdb->get_row($wpdb->prepare("SELECT * FROM {$this->output_objects_table()} WHERE id=%d", absint($object_id)), ARRAY_A);
                    if (is_array($materialized_object)) {
                        $this->output_supersede_conflicting_objects($materialized_object, (string)($materialized_object['object_key'] ?? ''));
                    }
                }
            }
        }
        return $result;
    }
    private function output_row_image_hash($row) {
        $payload = json_decode((string) ($row['payload'] ?? ''), true);
        if (is_array($payload) && !empty($payload['_image_sha256'])) {
            return sanitize_text_field((string) $payload['_image_sha256']);
        }
        return '';
    }

    private function output_tracking_health($url, $destination_url = '') {
        $url = esc_url_raw((string) $url);
        if ($url === '' || !wp_http_validate_url($url) || !in_array(strtolower((string) wp_parse_url($url, PHP_URL_SCHEME)), array('http','https'), true)) {
            return new WP_Error('output_tracking_invalid', 'Trackinglink ist ungültig.');
        }
        // Affiliate-Trackinglinks werden niemals automatisiert aufgerufen. HEAD
        // oder GET kann beim Netzwerk als künstlicher Klick gewertet werden.
        // Technisch geprüft wird nur eine separat bekannte Zielseite.
        $destination_url = esc_url_raw((string) $destination_url);
        if ($destination_url === '' || !wp_http_validate_url($destination_url) || $destination_url === $url) {
            return array('mode'=>'tracking_syntax_only','http_code'=>0,'checked_at'=>time());
        }
        $tracking_host = strtolower((string) wp_parse_url($url, PHP_URL_HOST));
        $destination_host = strtolower((string) wp_parse_url($destination_url, PHP_URL_HOST));
        if ($destination_host === '' || $destination_host === $tracking_host) {
            return array('mode'=>'tracking_syntax_only','http_code'=>0,'checked_at'=>time());
        }
        $args = array('timeout'=>8, 'redirection'=>5, 'limit_response_size'=>2048, 'headers'=>array('Accept'=>'text/html,*/*;q=0.8'));
        $response = function_exists('wp_safe_remote_head') ? wp_safe_remote_head($destination_url, $args) : new WP_Error('head_unavailable', 'HEAD nicht verfügbar.');
        $code = is_wp_error($response) ? 0 : absint(wp_remote_retrieve_response_code($response));
        if (is_wp_error($response) || $code === 405 || $code === 403 || $code === 0) {
            $response = wp_safe_remote_get($destination_url, $args);
            $code = is_wp_error($response) ? 0 : absint(wp_remote_retrieve_response_code($response));
        }
        if (is_wp_error($response)) {
            return $response;
        }
        if ($code < 200 || $code >= 400) {
            return new WP_Error('output_destination_http', 'Zielseite antwortet mit HTTP ' . $code . '.');
        }
        return array('mode'=>'destination_http','http_code'=>$code,'checked_at'=>time());
    }

    private function output_object_health_payload($object) {
        $payload = json_decode((string) ($object['payload'] ?? ''), true);
        return is_array($payload) ? $payload : array();
    }

    public function output_run_health_batch($limit = 10) {
        $this->maybe_install_output_objects_schema();
        if (method_exists($this, 'control_emergency_stop_active') && $this->control_emergency_stop_active()) {
            return array('checked'=>0,'ok'=>0,'warning'=>0,'quarantine'=>0,'skipped'=>1,'reason'=>'Globale Affiliate-Notabschaltung ist aktiv; gespeicherte Ausgabezustände bleiben unverändert.');
        }
        global $wpdb;
        $table = $this->output_objects_table();
        $limit = max(1, min(25, absint($limit)));
        $rows = $wpdb->get_results("SELECT * FROM {$table} WHERE status IN ('draft','published','warning') ORDER BY last_verified ASC, id ASC LIMIT {$limit}", ARRAY_A);
        $summary = array('checked'=>0,'ok'=>0,'warning'=>0,'quarantine'=>0);
        foreach ((array) $rows as $object) {
            $summary['checked']++;
            $payload = $this->output_object_health_payload($object);
            $creative = $this->output_creative_row((string) ($object['creative_identity_hash'] ?? ''));
            $error = null;
            if (!is_array($creative)) {
                $error = new WP_Error('output_creative_missing', 'Verknüpftes Creative fehlt.');
            } else {
                $provisional_product = $this->output_allows_provisional_ebay_product_asset($creative)
                    && (absint($creative['width'] ?? 0) <= 0 || absint($creative['height'] ?? 0) <= 0 || $this->output_row_image_hash($creative) === '');
                $verified = $provisional_product
                    ? $creative
                    : (method_exists($this, 'creative_library_verify_asset_row')
                        ? $this->creative_library_verify_asset_row($creative, true, false)
                        : new WP_Error('asset_verifier_missing', 'Bildprüfung fehlt.'));
                if (is_wp_error($verified)) {
                    $error = $verified;
                } else {
                    $creative = $verified;
                    $link = $this->output_tracking_health((string) ($creative['tracking_url'] ?? ''), (string) ($creative['destination_url'] ?? ''));
                    if (is_wp_error($link)) {
                        $error = $link;
                    } else {
                        $valid = $this->output_object_revalidate($object);
                        if (is_wp_error($valid)) {
                            $error = $valid;
                        }
                    }
                }
            }
            if (!$error) {
                $payload['health_failures'] = 0;
                $payload['last_health_error'] = '';
                $payload['last_health_ok'] = time();
                $restore_status = sanitize_key((string) ($payload['health_previous_status'] ?? ($object['status'] ?? 'draft')));
                if (!in_array($restore_status, array('draft','published'), true)) {
                    $restore_status = 'draft';
                }
                unset($payload['health_previous_status']);
                $wpdb->update($table, array(
                    'status'=>$restore_status,
                    'payload'=>wp_json_encode($payload, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES),
                    'last_verified'=>time(),
                    'updated_at'=>time(),
                ), array('id'=>absint($object['id'])));
                $summary['ok']++;
                continue;
            }
            $code = $error->get_error_code();
            $deterministic = in_array($code, array(
                'output_creative_missing','output_veto_active','output_source_inactive','output_tracking_changed',
                'output_image_changed','output_image_hash_changed','output_dimensions_missing','output_target_changed',
                'output_slot_changed','output_target_no_longer_safe','output_no_design_slot','output_source_fingerprint_changed','portal_domain_profile_missing','portal_listing_asset_validator_missing',
                'awin_partner_id_missing','awin_partner_portal_missing','awin_partner_not_approved','awin_partner_other_portal','awin_partner_test_blocked','awin_partner_excluded','awin_partner_portal_mismatch','awin_partner_not_joined_current'
            ), true);
            $failures = $deterministic ? 3 : absint($payload['health_failures'] ?? 0) + 1;
            if (!isset($payload['health_previous_status']) && in_array((string) ($object['status'] ?? ''), array('draft','published'), true)) {
                $payload['health_previous_status'] = (string) $object['status'];
            }
            $payload['health_failures'] = $failures;
            $payload['last_health_error'] = $error->get_error_message();
            $payload['last_health_error_code'] = $code;
            $payload['last_health_failed_at'] = time();
            if ($failures >= 3) {
                $this->output_deactivate_materialized_object($object, $error->get_error_message());
                $status = 'quarantine';
                $summary['quarantine']++;
            } else {
                $status = 'warning';
                $summary['warning']++;
            }
            $wpdb->update($table, array(
                'status'=>$status,
                'decision_reason'=>'Automatische Gesamtprüfung: ' . $error->get_error_message(),
                'payload'=>wp_json_encode($payload, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES),
                'last_verified'=>time(),
                'updated_at'=>time(),
            ), array('id'=>absint($object['id'])));
        }
        return $summary;
    }

    private function output_object_by_id($id) {
        global $wpdb;
        return $wpdb->get_row($wpdb->prepare("SELECT * FROM {$this->output_objects_table()} WHERE id=%d", absint($id)), ARRAY_A);
    }

    private function output_object_revalidate($object) {
        if (!is_array($object)) { return new WP_Error('output_object_missing','Ausgabeobjekt fehlt.'); }
        if (method_exists($this, 'control_get_decision')) {
            $output_decision = $this->control_get_decision((string) ($object['portal_key'] ?? ''), 'output', (string) absint($object['id'] ?? 0));
            if (!empty($output_decision['exists']) && (string) ($output_decision['status'] ?? '') === 'veto') {
                return new WP_Error('output_manual_veto_active', (string) ($output_decision['reason'] ?? 'Ausgabeobjekt ist manuell gesperrt.'));
            }
            if (!empty($output_decision['exists']) && (string) ($output_decision['status'] ?? '') === 'paused') {
                return new WP_Error('output_manual_pause_active', (string) ($output_decision['reason'] ?? 'Ausgabeobjekt ist manuell pausiert.'));
            }
        }
        $row = $this->output_creative_row((string) ($object['creative_identity_hash'] ?? ''));
        if (!is_array($row)) { return new WP_Error('output_creative_missing','Verknüpftes Creative fehlt.'); }
        if (method_exists($this, 'control_emergency_stop_active') && $this->control_emergency_stop_active()) {
            return new WP_Error('control_emergency_stop_active', 'Globale Affiliate-Notabschaltung ist aktiv.');
        }
        $portal_for_gate = $this->output_portal_by_key((string) ($object['portal_key'] ?? ''), true);
        if (is_wp_error($portal_for_gate)) { return $portal_for_gate; }
        if (method_exists($this, 'control_partner_gate')) {
            $gate = $this->control_partner_gate($row, $portal_for_gate);
            if (is_wp_error($gate)) { return $gate; }
        }
        $manual = $this->output_portal_decision((string) ($object['portal_key'] ?? ''),(string) ($row['identity_hash'] ?? ''));
        if ((string) ($manual['manual_status'] ?? '') === 'veto') { return new WP_Error('output_veto_active','Manuelles Creative-Veto ist für dieses Portal aktiv.'); }
        if ((string) ($row['source_status'] ?? 'active') !== 'active' || (string) ($row['availability_state'] ?? 'active') !== 'active') { return new WP_Error('output_source_inactive','Creative-Quelle ist nicht mehr aktiv.'); }
        if ((string) ($row['tracking_url'] ?? '') !== (string) ($object['tracking_url'] ?? '')) { return new WP_Error('output_tracking_changed','Trackinglink hat sich seit der Vorbereitung geändert.'); }
        if ((string) ($row['image_url'] ?? '') !== (string) ($object['image_url'] ?? '')) { return new WP_Error('output_image_changed','Bildquelle hat sich seit der Vorbereitung geändert.'); }
        $row_image_hash = $this->output_row_image_hash($row);
        $provisional_product = $this->output_allows_provisional_ebay_product_asset($row)
            && (absint($row['width'] ?? 0) <= 0 || absint($row['height'] ?? 0) <= 0 || $row_image_hash === '');
        if (!$provisional_product && ($row_image_hash === '' || !hash_equals($row_image_hash,(string) ($object['image_hash'] ?? '')))) { return new WP_Error('output_image_hash_changed','Verifiziertes Bannerbild hat sich seit der Vorbereitung geändert.'); }
        $payload=json_decode((string) ($row['payload'] ?? ''),true); $payload=is_array($payload)?$payload:array();
        if (!$provisional_product && (!in_array((string) ($payload['_dimension_state'] ?? ''),array('verified','mismatch'),true) || absint($row['width'] ?? 0)<=0 || absint($row['height'] ?? 0)<=0)) { return new WP_Error('output_dimensions_missing','Reale Bildmaße fehlen.'); }
        $portal=$this->output_portal_by_key((string) ($object['portal_key'] ?? '')); if (is_wp_error($portal)) { return $portal; }
        $valid=$this->output_validate_portal_profile($portal); if (is_wp_error($valid)) { return $valid; }
        $classification=$this->output_classify_for_portal($row,$portal,(string) ($object['output_type'] ?? ''));
        if (is_wp_error($classification) || (string) ($classification['status'] ?? '') !== 'ready') { return is_wp_error($classification)?$classification:new WP_Error('output_target_no_longer_safe','Portalziel ist nicht mehr eindeutig freigabefähig.'); }
        $target=is_array($classification['target'] ?? null)?$classification['target']:array();
        if ((string) ($target['key'] ?? '') !== (string) ($object['target_key'] ?? '')) { return new WP_Error('output_target_changed','Automatisch ermitteltes Portalziel hat sich geändert.'); }
        $slot_id='';
        if (in_array((string) ($object['output_type'] ?? ''),array('portal_banner','product_campaign'),true)) {
            $slot=$this->output_format_slot($row,$portal,$target,(string) ($object['output_type'] ?? '')==='product_campaign'?'product':'banner');
            if (is_wp_error($slot)) { return $slot; }
            $slot_id=(string) ($slot['slot_id'] ?? '');
            if ($slot_id !== (string) ($object['slot_id'] ?? '')) { return new WP_Error('output_slot_changed','Passender Designslot hat sich geändert.'); }
        } else {
            $listing=$this->output_listing_asset_compatibility($row,$portal); if (is_wp_error($listing)) { return $listing; }
        }
        $fingerprint=$this->output_source_fingerprint($row,$portal,(string) ($object['output_type'] ?? ''),$target,$slot_id);
        if ((string) ($object['source_fingerprint'] ?? '') === '' || !hash_equals((string) ($object['source_fingerprint'] ?? ''),$fingerprint)) { return new WP_Error('output_source_fingerprint_changed','Quelldaten, Portalprofil, Ziel oder Adapterstand haben sich seit der Vorbereitung geändert.'); }
        return $row;
    }
    /**
     * eBay-Produktinhalte dürfen in einer öffentlichen Produktzone nicht mit
     * Nicht-eBay-Produkten vermischt werden. Die Prüfung gilt in beide
     * Richtungen und blockiert die Aktivierung fail-closed.
     */
    private function output_product_provider_isolation($object) {
        if (!is_array($object) || sanitize_key((string) ($object['output_type'] ?? '')) !== 'product_campaign') { return true; }
        $provider = sanitize_key((string) ($object['provider'] ?? ''));
        $is_ebay = $provider === 'ebay';
        global $wpdb;
        $table = $this->output_objects_table();
        $rows = $wpdb->get_results($wpdb->prepare(
            "SELECT * FROM {$table} WHERE portal_key=%s AND target_key=%s AND output_type='product_campaign' AND status='published'",
            (string) ($object['portal_key'] ?? ''),
            (string) ($object['target_key'] ?? '')
        ), ARRAY_A);
        foreach ((array) $rows as $row) {
            if (absint($row['id'] ?? 0) === absint($object['id'] ?? 0)) { continue; }
            $other_is_ebay = sanitize_key((string) ($row['provider'] ?? '')) === 'ebay';
            if ($other_is_ebay !== $is_ebay) {
                return new WP_Error('output_ebay_content_isolation_conflict', 'eBay- und Nicht-eBay-Produkte dürfen am selben Portalziel nicht gemeinsam öffentlich sein.');
            }
        }

        if (!method_exists($this, 'get_campaigns')) { return true; }
        $campaign_id = absint($object['campaign_post_id'] ?? 0);
        $incoming = $campaign_id > 0 ? $this->output_campaign_by_post_id($campaign_id) : null;
        if (!is_array($incoming)) { return new WP_Error('output_campaign_missing', 'Produktkampagne fehlt.'); }
        $incoming_targets = array_values(array_filter(array_map('sanitize_text_field', (array) ($incoming['automation_target_keys'] ?? array()))));
        if (!$incoming_targets) { return new WP_Error('output_campaign_target_missing', 'Produktkampagne besitzt kein exaktes Portalziel.'); }
        foreach ((array) $this->get_campaigns() as $campaign) {
            if (!is_array($campaign) || empty($campaign['active']) || absint($campaign['post_id'] ?? 0) === $campaign_id) { continue; }
            if (sanitize_key((string) ($campaign['creative_type'] ?? '')) !== 'product') { continue; }
            $targets = array_values(array_filter(array_map('sanitize_text_field', (array) ($campaign['automation_target_keys'] ?? array()))));
            if (!$targets || !array_intersect($incoming_targets, $targets)) { continue; }
            $other_is_ebay = sanitize_key((string) ($campaign['network'] ?? '')) === 'ebay';
            if ($other_is_ebay !== $is_ebay) {
                return new WP_Error('output_ebay_content_isolation_conflict', 'Am selben Portalziel ist bereits eine Produktkampagne des anderen Anbieter-Kohorts aktiv.');
            }
        }
        return true;
    }

    public function handle_output_object_action() {
        if (!current_user_can('manage_options')) {
            wp_die('Keine Berechtigung.');
        }
        check_admin_referer('ppar_output_object_action', 'ppar_output_nonce');
        $id = absint($_POST['output_id'] ?? 0);
        $action = sanitize_key((string) ($_POST['output_action'] ?? ''));
        $object = $this->output_object_by_id($id);
        if (!is_array($object)) {
            $this->output_redirect('failed', 'Ausgabeobjekt wurde nicht gefunden.');
        }
        global $wpdb;
        $table = $this->output_objects_table();
        $reason = sanitize_text_field((string) wp_unslash($_POST['output_reason'] ?? ''));
        if ($action === 'veto') { $action = 'veto_output'; }
        if ($action === 'veto_output') {
            if ($reason === '') { $reason = 'Ausgabeobjekt durch Chefentscheidung gesperrt.'; }
            $this->output_deactivate_materialized_object($object, $reason);
            $wpdb->update($table, array('status'=>'blocked_manual','decision_source'=>'manual_output_veto','decision_reason'=>$reason,'updated_at'=>time()), array('id'=>$id));
            if (method_exists($this, 'control_set_decision')) {
                $this->control_set_decision((string) ($object['portal_key'] ?? ''), 'output', (string) $id, 'veto', $reason, array('output_id'=>$id), 'output_veto');
            }
            $this->output_redirect('success', 'Diese Ausgabe wurde gesperrt. Das Creative bleibt für andere Ziele verfügbar.');
        }
        if ($action === 'pause_output') {
            if ($reason === '') { $reason = 'Ausgabeobjekt durch Chefentscheidung pausiert.'; }
            $this->output_deactivate_materialized_object($object, $reason);
            $wpdb->update($table, array('status'=>'paused_manual','decision_source'=>'manual_output_pause','decision_reason'=>$reason,'updated_at'=>time()), array('id'=>$id));
            if (method_exists($this, 'control_set_decision')) {
                $this->control_set_decision((string) ($object['portal_key'] ?? ''), 'output', (string) $id, 'paused', $reason, array('output_id'=>$id), 'output_pause');
            }
            $this->output_redirect('success', 'Diese Ausgabe wurde pausiert.');
        }
        if ($action === 'restore_output') {
            if ($reason === '') { $reason = 'Manuelle Ausgabeentscheidung zurückgenommen; erneute Freigabe erforderlich.'; }
            if (method_exists($this, 'control_reset_decision')) {
                $this->control_reset_decision((string) ($object['portal_key'] ?? ''), 'output', (string) $id, $reason);
            }
            $restored_status = (absint($object['campaign_post_id'] ?? 0) > 0 || absint($object['listing_post_id'] ?? 0) > 0) ? 'draft' : 'ready';
            $wpdb->update($table, array('status'=>$restored_status,'decision_source'=>'manual_output_restore','decision_reason'=>$reason,'updated_at'=>time()), array('id'=>$id));
            $this->output_redirect('success', 'Manuelle Ausgabeentscheidung wurde zurückgenommen.');
        }
        if (method_exists($this, 'control_emergency_stop_active') && $this->control_emergency_stop_active()) {
            $this->output_redirect('failed', 'Globale Affiliate-Notabschaltung ist aktiv.');
        }
        $row = $this->output_object_revalidate($object);
        if (is_wp_error($row)) {
            $wpdb->update($table, array('status'=>'blocked_runtime','decision_reason'=>$row->get_error_message(),'updated_at'=>time()), array('id'=>$id));
            $this->output_redirect('failed', $row->get_error_message());
        }
        $portal = $this->output_portal_by_key((string) ($object['portal_key'] ?? ''));
        if (is_wp_error($portal)) {
            $this->output_redirect('failed', $portal->get_error_message());
        }
        $adapter = sanitize_key((string) ($portal['adapter'] ?? ''));
        if ($action === 'publish_listing' && in_array((string) ($object['output_type'] ?? ''), array('hivepress_listing','portal_listing'), true)) {
            if (in_array($adapter, array('wordpress_local','wordpress_multisite'), true)) {
                $published = $this->output_with_portal($portal, function() use ($object) {
                    $post_id = absint($object['listing_post_id'] ?? 0);
                    if ($post_id <= 0 || !get_post($post_id)) {
                        return new WP_Error('listing_draft_missing', 'Listing-Entwurf fehlt.');
                    }
                    return wp_update_post(array('ID'=>$post_id,'post_status'=>'publish'), true);
                });
            } else {
                $callbacks = is_array($portal['callbacks'] ?? null) ? $portal['callbacks'] : array();
                $published = (!empty($callbacks['publish_listing']) && is_callable($callbacks['publish_listing']))
                    ? call_user_func($callbacks['publish_listing'], $object, $portal)
                    : new WP_Error('portal_publish_missing', 'Externer Portaladapter besitzt keine Listing-Freigabe.');
            }
            if (is_wp_error($published)) {
                $this->output_redirect('failed', $published->get_error_message());
            }
            $wpdb->update($table, array('status'=>'published','updated_at'=>time(),'last_verified'=>time()), array('id'=>$id));
            if (method_exists($this, 'control_set_decision')) {
                $this->control_set_decision((string) ($object['portal_key'] ?? ''), 'output', (string) $id, 'approved', 'HivePress-Listing durch Chefentscheidung veröffentlicht.', array('output_id'=>$id), 'output_publish');
            }
            $this->output_redirect('success', 'HivePress-Listing veröffentlicht.');
        }
        if ($action === 'activate_campaign' && in_array((string) ($object['output_type'] ?? ''), array('portal_banner','product_campaign'), true)) {
            if ((string) ($object['output_type'] ?? '') === 'product_campaign') {
                $isolation = $this->output_product_provider_isolation($object);
                if (is_wp_error($isolation)) {
                    $wpdb->update($table, array('status'=>'blocked_runtime','decision_reason'=>$isolation->get_error_message(),'updated_at'=>time()), array('id'=>$id));
                    $this->output_redirect('failed', $isolation->get_error_message());
                }
            }
            if (in_array($adapter, array('wordpress_local','wordpress_multisite'), true)) {
                $activated = $this->output_with_portal($portal, function() use ($object) {
                    $campaign_id = absint($object['campaign_post_id'] ?? 0);
                    $campaign = $this->output_campaign_by_post_id($campaign_id);
                    if (!is_array($campaign)) {
                        return new WP_Error('banner_campaign_missing', 'Bannerkampagne fehlt.');
                    }
                    $campaign['active'] = true;
                    return $this->save_campaign_record($campaign, $campaign_id) ? true : new WP_Error('banner_activation_failed', 'Bannerkampagne konnte nicht aktiviert werden.');
                });
            } else {
                $callbacks = is_array($portal['callbacks'] ?? null) ? $portal['callbacks'] : array();
                $activated = (!empty($callbacks[(string) ($object['output_type'] ?? '') === 'product_campaign' ? 'activate_product' : 'activate_banner']) && is_callable($callbacks[(string) ($object['output_type'] ?? '') === 'product_campaign' ? 'activate_product' : 'activate_banner']))
                    ? call_user_func($callbacks[(string) ($object['output_type'] ?? '') === 'product_campaign' ? 'activate_product' : 'activate_banner'], $object, $portal)
                    : new WP_Error('portal_activate_missing', 'Externer Portaladapter besitzt keine Kampagnenfreigabe.');
            }
            if (is_wp_error($activated)) {
                $this->output_redirect('failed', $activated->get_error_message());
            }
            $wpdb->update($table, array('status'=>'published','updated_at'=>time(),'last_verified'=>time()), array('id'=>$id));
            if (method_exists($this, 'control_set_decision')) {
                $this->control_set_decision((string) ($object['portal_key'] ?? ''), 'output', (string) $id, 'approved', (string) ($object['output_type'] ?? '') === 'product_campaign' ? 'Produktkampagne durch Chefentscheidung aktiviert.' : 'Bannerkampagne durch Chefentscheidung aktiviert.', array('output_id'=>$id), 'output_publish');
            }
            $this->output_redirect('success', (string) ($object['output_type'] ?? '') === 'product_campaign' ? 'Produktkampagne aktiviert.' : 'Bannerkampagne aktiviert.');
        }
        $this->output_redirect('failed', 'Unzulässige Aktion.');
    }

    private function output_redirect($status, $message) {
        wp_safe_redirect(add_query_arg(array('page'=>'affiliate-portal-outputs','ppar_output'=>$status,'ppar_message'=>rawurlencode((string) $message)), admin_url('admin.php')));
        exit;
    }

    public function render_output_objects_page() {
        if (!current_user_can('manage_options')) {
            return;
        }
        $this->maybe_install_output_objects_schema();
        global $wpdb;
        $rows = $wpdb->get_results("SELECT * FROM {$this->output_objects_table()} ORDER BY updated_at DESC, id DESC LIMIT 300", ARRAY_A);
        $notice = sanitize_key((string) ($_GET['ppar_output'] ?? ''));
        $message = rawurldecode((string) ($_GET['ppar_message'] ?? ''));
        ?>
        <div class="wrap">
            <h1>Ausgaben &amp; Freigabe</h1>
            <p>Jede Zeile verbindet genau ein Creative mit einem Portalziel. Bannerkampagne und HivePress-Listing bleiben getrennt. Ohne eindeutigen Treffer oder verifizierte Bildmaße gibt es keine Freigabe.</p>
            <?php if ($notice === 'success') : ?><div class="notice notice-success inline"><p><?php echo esc_html($message); ?></p></div><?php endif; ?>
            <?php if ($notice === 'failed') : ?><div class="notice notice-error inline"><p><?php echo esc_html($message); ?></p></div><?php endif; ?>
            <table class="widefat striped"><thead><tr><th>Partner / Creative</th><th>Portal / Ausgabe</th><th>Ziel</th><th>Status</th><th>Prüfung</th><th>Aktion</th></tr></thead><tbody>
            <?php if (!$rows) : ?><tr><td colspan="6">Noch keine Ausgabeobjekte.</td></tr><?php endif; ?>
            <?php foreach ((array) $rows as $row) :
                $creative = $this->output_creative_row((string) ($row['creative_identity_hash'] ?? ''));
                $payload = json_decode((string) ($row['payload'] ?? ''), true);
                $payload = is_array($payload) ? $payload : array();
                ?>
                <tr>
                    <td><strong><?php echo esc_html((string) ($creative['partner_name'] ?? $row['partner_external_id'])); ?></strong><br><?php echo esc_html((string) ($creative['title'] ?? 'Creative fehlt')); ?><br><small><?php echo esc_html(absint($row['image_width']) . ' × ' . absint($row['image_height'])); ?></small></td>
                    <td><?php echo esc_html((string) $row['portal_key']); ?><br><strong><?php echo esc_html((string) $row['output_type']); ?></strong><?php if (!empty($row['slot_id'])) : ?><br><?php echo esc_html((string) $row['slot_id']); ?><?php endif; ?></td>
                    <td><?php echo esc_html((string) $row['target_label']); ?><br><small><?php echo esc_html((string) $row['target_key']); ?></small></td>
                    <td><strong><?php echo esc_html((string) $row['status']); ?></strong><br><?php echo absint($row['confidence']); ?> %</td>
                    <td><?php echo esc_html((string) $row['decision_reason']); ?><?php if (!empty($payload['preview_url'])) : ?><br><a href="<?php echo esc_url((string) $payload['preview_url']); ?>">Entwurfsvorschau öffnen</a><?php endif; ?></td>
                    <td>
                        <?php $status = (string) $row['status']; ?>
                        <?php if ($status === 'draft') : ?>
                        <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>" style="margin-bottom:8px">
                            <input type="hidden" name="action" value="ppar_output_object_action"><input type="hidden" name="output_id" value="<?php echo absint($row['id']); ?>">
                            <?php wp_nonce_field('ppar_output_object_action', 'ppar_output_nonce'); ?>
                            <?php if (in_array((string) $row['output_type'], array('hivepress_listing','portal_listing'), true)) : ?><button class="button button-primary" name="output_action" value="publish_listing">Listing veröffentlichen</button><?php endif; ?>
                            <?php if (in_array((string) $row['output_type'], array('portal_banner','product_campaign'), true)) : ?><button class="button button-primary" name="output_action" value="activate_campaign"><?php echo (string) $row['output_type'] === 'product_campaign' ? 'Produktkampagne aktivieren' : 'Banner aktivieren'; ?></button><?php endif; ?>
                        </form>
                        <?php elseif ($status === 'published') : ?>
                        <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>" style="margin-bottom:8px"><input type="hidden" name="action" value="ppar_output_object_action"><input type="hidden" name="output_id" value="<?php echo absint($row['id']); ?>"><?php wp_nonce_field('ppar_output_object_action', 'ppar_output_nonce'); ?><input type="text" name="output_reason" required placeholder="Begründung für Pause" style="max-width:210px"> <button class="button" name="output_action" value="pause_output">Ausgabe pausieren</button></form>
                        <?php elseif (in_array($status, array('paused_manual','blocked_manual'), true)) : ?>
                        <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>" style="margin-bottom:8px"><input type="hidden" name="action" value="ppar_output_object_action"><input type="hidden" name="output_id" value="<?php echo absint($row['id']); ?>"><?php wp_nonce_field('ppar_output_object_action', 'ppar_output_nonce'); ?><input type="text" name="output_reason" required placeholder="Begründung für Rücknahme" style="max-width:210px"> <button class="button" name="output_action" value="restore_output">Zur Automatik zurückkehren</button></form>
                        <?php endif; ?>
                        <?php if (!in_array($status, array('blocked_manual','superseded'), true)) : ?>
                        <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>"><input type="hidden" name="action" value="ppar_output_object_action"><input type="hidden" name="output_id" value="<?php echo absint($row['id']); ?>"><?php wp_nonce_field('ppar_output_object_action', 'ppar_output_nonce'); ?><input type="text" name="output_reason" required placeholder="Begründung für Veto" style="max-width:210px"> <button class="button" name="output_action" value="veto_output">Nur diese Ausgabe sperren</button></form>
                        <?php endif; ?>
                    </td>
                </tr>
            <?php endforeach; ?>
            </tbody></table>
        </div>
        <?php
    }
}
