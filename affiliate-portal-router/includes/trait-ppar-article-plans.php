<?php
if (!defined('ABSPATH')) {
    exit;
}

trait PPAR_Article_Plans_Trait {
    private function article_plan_default() {
        return array(
            'schema' => self::ARTICLE_PLAN_SCHEMA,
            'status' => 'missing',
            'generated_at' => 0,
            'content_hash' => '',
            'campaign_revision' => 0,
            'banner' => array(
                'status' => 'none',
                'campaign_post_id' => 0,
                'reason' => '',
                'anchor' => array(),
            ),
            'products' => array(
                'status' => 'none',
                'campaign_post_ids' => array(),
                'reason' => '',
                'reports' => array(),
            ),
        );
    }

    private function article_plan_log_event($event, $post_id, $details = array()) {
        $log = get_option(self::OPTION_ARTICLE_PLAN_LOG, array());
        $log = is_array($log) ? $log : array();
        $log[] = array(
            'time' => time(),
            'event' => sanitize_key((string) $event),
            'post_id' => absint($post_id),
            'details' => is_array($details) ? $details : array('message' => (string) $details),
        );
        if (count($log) > 200) {
            $log = array_slice($log, -200);
        }
        update_option(self::OPTION_ARTICLE_PLAN_LOG, $log, false);
    }

    private function article_plan_campaign_revision() {
        return max(1, absint(get_option(self::OPTION_ARTICLE_PLAN_REVISION, 1)));
    }

    private function article_plan_bump_campaign_revision($reason) {
        $revision = $this->article_plan_campaign_revision() + 1;
        update_option(self::OPTION_ARTICLE_PLAN_REVISION, $revision, false);
        $this->article_plan_log_event('campaign_revision', 0, array(
            'revision' => $revision,
            'reason' => sanitize_text_field((string) $reason),
        ));
        return $revision;
    }

    private function article_plan_content_hash($post_id) {
        $post = get_post($post_id);
        if (!$post || $post->post_type !== 'post') {
            return '';
        }
        $term_ids = wp_get_post_categories($post_id, array('fields' => 'ids'));
        if (is_wp_error($term_ids)) {
            $term_ids = array();
        }
        sort($term_ids, SORT_NUMERIC);
        $payload = array(
            'title' => (string) $post->post_title,
            'content' => (string) $post->post_content,
            'terms' => array_values(array_map('intval', $term_ids)),
            'campaign_revision' => $this->article_plan_campaign_revision(),
            'schema' => self::ARTICLE_PLAN_SCHEMA,
        );
        return hash('sha256', wp_json_encode($payload, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES));
    }

    private function article_plan_get($post_id) {
        $stored = get_post_meta($post_id, self::ARTICLE_PLAN_META, true);
        return wp_parse_args(is_array($stored) ? $stored : array(), $this->article_plan_default());
    }

    private function article_plan_is_current($post_id, $plan = null) {
        $plan = is_array($plan) ? $plan : $this->article_plan_get($post_id);
        return !empty($plan['content_hash'])
            && hash_equals((string) $plan['content_hash'], (string) $this->article_plan_content_hash($post_id))
            && (int) ($plan['campaign_revision'] ?? 0) === $this->article_plan_campaign_revision()
            && (string) ($plan['schema'] ?? '') === self::ARTICLE_PLAN_SCHEMA;
    }

    private function article_plan_normalize_heading($text) {
        $text = html_entity_decode(wp_strip_all_tags((string) $text), ENT_QUOTES | ENT_HTML5, 'UTF-8');
        $text = function_exists('remove_accents') ? remove_accents($text) : $text;
        $text = strtolower(trim(preg_replace('/\s+/u', ' ', $text)));
        return preg_replace('/[^a-z0-9äöüß ]/u', '', $text);
    }

    /**
     * Sucht genau einen sicheren Anker: nach abgeschlossenem Fließtext eines
     * H2-Abschnitts und direkt vor der nächsten H2. Keine Ratio-Pflichtfenster.
     */
    private function article_plan_prepare_anchor_content($content) {
        $content = (string) $content;
        if (function_exists('do_blocks')) {
            $content = do_blocks($content);
        }
        if (function_exists('shortcode_unautop')) {
            $content = shortcode_unautop($content);
        }
        if (function_exists('do_shortcode')) {
            $content = do_shortcode($content);
        }
        if (!preg_match('/<p\b/i', $content) && function_exists('wpautop')) {
            $content = wpautop($content);
        }
        return (string) $content;
    }

    private function article_plan_find_anchor($content) {
        $content = (string) $content;
        $candidates = $this->article_h2_insertion_candidates($content);
        if (empty($candidates)) {
            return array();
        }
        $target = 0.50;
        usort($candidates, function($a, $b) use ($target) {
            $da = abs((float) ($a['ratio'] ?? 0) - $target);
            $db = abs((float) ($b['ratio'] ?? 0) - $target);
            if ($da === $db) {
                return (int) ($a['offset'] ?? 0) <=> (int) ($b['offset'] ?? 0);
            }
            return $da < $db ? -1 : 1;
        });
        $chosen = $candidates[0];
        $key = $this->article_plan_normalize_heading((string) ($chosen['heading'] ?? ''));
        $level = in_array((int) ($chosen['heading_level'] ?? 2), array(2, 3), true) ? (int) $chosen['heading_level'] : 2;
        if ($key === '') {
            return array();
        }
        $occurrence = 0;
        if (preg_match_all('/<h([23])\b[^>]*>(.*?)<\/h\1>/is', $content, $matches, PREG_SET_ORDER | PREG_OFFSET_CAPTURE)) {
            foreach ($matches as $match) {
                if ((int) $match[0][1] > (int) ($chosen['heading_offset'] ?? $chosen['offset'] ?? 0)) {
                    break;
                }
                if ((int) $match[1][0] === $level && $this->article_plan_normalize_heading((string) $match[2][0]) === $key) {
                    $occurrence++;
                }
            }
        }
        return array(
            'heading' => sanitize_text_field((string) ($chosen['heading'] ?? '')),
            'heading_key' => $key,
            'heading_level' => $level,
            'occurrence' => max(1, $occurrence),
            'previous_heading' => sanitize_text_field((string) ($chosen['previous_heading'] ?? '')),
            'ratio' => round((float) ($chosen['ratio'] ?? 0), 4),
        );
    }

    private function article_plan_find_render_offset($content, $anchor) {
        $content = (string) $content;
        $key = sanitize_text_field((string) ($anchor['heading_key'] ?? ''));
        $level = in_array((int) ($anchor['heading_level'] ?? 2), array(2, 3), true) ? (int) $anchor['heading_level'] : 2;
        $wanted_occurrence = max(1, absint($anchor['occurrence'] ?? 1));
        if ($key === '' || !preg_match_all('/<h([23])\b[^>]*>(.*?)<\/h\1>/is', $content, $matches, PREG_SET_ORDER | PREG_OFFSET_CAPTURE)) {
            return 0;
        }
        $seen = 0;
        $previous_heading_end = 0;
        foreach ($matches as $match) {
            $heading_start = (int) $match[0][1];
            if ((int) $match[1][0] === $level && $this->article_plan_normalize_heading((string) $match[2][0]) === $key) {
                $seen++;
                if ($seen === $wanted_occurrence) {
                    $boundary = $this->article_boundary_before_heading($content, $previous_heading_end, $heading_start);
                    return (int) ($boundary['offset'] ?? $heading_start);
                }
            }
            $previous_heading_end = $heading_start + strlen((string) $match[0][0]);
        }
        return 0;
    }

    private function article_plan_program_verified($campaign) {
        $status = sanitize_key((string) ($campaign['programme_status'] ?? 'unknown'));
        $source = trim((string) ($campaign['programme_status_source'] ?? ''));
        $checked_at = absint($campaign['programme_status_checked_at'] ?? 0);
        return $status === 'active' && $source !== '' && $checked_at > 0;
    }

    private function article_product_quality_report($campaign, $context, $rank) {
        $report = array(
            'campaign_post_id' => absint($campaign['post_id'] ?? 0),
            'name' => sanitize_text_field((string) ($campaign['name'] ?? '')),
            'overall' => 'warn',
            'checks' => array(),
        );
        $checks = array();
        $checks['technical'] = $this->campaign_is_complete($campaign) ? 'pass' : 'fail';
        $programme_status = sanitize_key((string) ($campaign['programme_status'] ?? 'unknown'));
        $checks['programme'] = $this->article_plan_program_verified($campaign) ? 'pass' : (in_array($programme_status, array('paused', 'ended'), true) ? 'fail' : 'warn');
        $specificity = (int) ($rank['specificity'] ?? 0);
        $checks['relevance'] = $specificity >= 350 ? 'pass' : ($specificity >= 200 ? 'warn' : 'fail');
        $has_title = trim((string) ($campaign['title'] ?? '')) !== '';
        $has_image = trim((string) ($campaign['image_url'] ?? '')) !== '';
        $checks['title_image'] = ($has_title && $has_image) ? 'pass' : (($has_title || $has_image) ? 'warn' : 'fail');
        $source = sanitize_key((string) ($campaign['source'] ?? $campaign['network'] ?? 'manual'));
        $last_synced = absint($campaign['last_synced'] ?? 0);
        $checks['freshness'] = in_array($source, array('manual', 'direct'), true) ? 'pass' : ($last_synced > 0 ? 'pass' : 'fail');
        $manual = sanitize_key((string) ($campaign['quality_manual_status'] ?? 'unknown'));
        $checks['manual_review'] = $manual === 'approved' ? 'pass' : ($manual === 'rejected' ? 'fail' : 'warn');

        if (in_array('fail', $checks, true)) {
            $report['overall'] = 'fail';
        } elseif ($checks['manual_review'] === 'pass' && $checks['programme'] === 'pass' && $checks['freshness'] === 'pass' && $specificity >= 200) {
            $report['overall'] = 'pass';
        } else {
            $report['overall'] = 'warn';
        }
        $report['checks'] = $checks;
        $report['specificity'] = $specificity;
        $report['reason'] = sanitize_text_field((string) ($rank['reason'] ?? ''));
        return $report;
    }

    private function article_plan_product_dedupe_key($campaign) {
        $external = trim((string) ($campaign['external_id'] ?? ''));
        if ($external !== '') {
            return 'external:' . strtolower($external);
        }
        $title = $this->article_plan_normalize_heading((string) ($campaign['title'] ?? $campaign['name'] ?? ''));
        return 'title:' . $title;
    }

    private function article_plan_product_title_is_near_duplicate($campaign, $selected_titles) {
        $title = $this->article_plan_normalize_heading((string) ($campaign['title'] ?? $campaign['name'] ?? ''));
        if ($title === '') {
            return true;
        }
        foreach ((array) $selected_titles as $selected) {
            $percent = 0.0;
            similar_text($title, (string) $selected, $percent);
            if ($percent >= 85.0) {
                return true;
            }
        }
        return false;
    }

    private function article_plan_build($post_id, $reason = 'manual') {
        $post_id = absint($post_id);
        $post = get_post($post_id);
        if (!$post || $post->post_type !== 'post' || in_array($post->post_status, array('trash', 'auto-draft'), true)) {
            return new WP_Error('invalid_post', 'Kein gültiger Beitrag.');
        }
        $plan = $this->article_plan_default();
        $plan['generated_at'] = time();
        $plan['content_hash'] = $this->article_plan_content_hash($post_id);
        $plan['campaign_revision'] = $this->article_plan_campaign_revision();
        $context = $this->get_content_context($post_id);
        $raw_content = (string) $post->post_content;
        $anchor_content = $this->article_plan_prepare_anchor_content($raw_content);
        $anchor = $this->article_plan_find_anchor($anchor_content);

        $banner_candidates = $this->ranked_campaigns_for_slot($context, 'post_inline_banner');
        $selected_banner = null;
        foreach ($banner_candidates as $candidate) {
            if ((int) ($candidate['specificity'] ?? 0) < 200 || !$this->article_plan_program_verified((array) ($candidate['campaign'] ?? array()))) {
                continue;
            }
            $selected_banner = $candidate;
            break;
        }
        if (!$selected_banner) {
            $plan['banner']['status'] = 'none';
            $plan['banner']['reason'] = 'Kein ausreichend passendes Banner mit verifiziert aktivem Programmstatus.';
        } elseif (empty($anchor)) {
            $plan['banner'] = array(
                'status' => 'pending_anchor',
                'campaign_post_id' => absint($selected_banner['campaign']['post_id'] ?? 0),
                'reason' => 'Der sichere Anker wird einmalig am vollständig gerenderten Beitrag aufgelöst.',
                'anchor' => array(),
            );
        } else {
            $plan['banner'] = array(
                'status' => 'ready',
                'campaign_post_id' => absint($selected_banner['campaign']['post_id'] ?? 0),
                'reason' => sanitize_text_field((string) ($selected_banner['reason'] ?? 'Passende Zuordnung.')),
                'anchor' => $anchor,
            );
        }

        $reports = array();
        $product_ids = array();
        $seen = array();
        $selected_titles = array();
        foreach ($this->ranked_campaigns_for_slot($context, 'post_bottom_products') as $candidate) {
            $campaign = $candidate['campaign'] ?? null;
            if (!is_array($campaign)) {
                continue;
            }
            $report = $this->article_product_quality_report($campaign, $context, $candidate);
            $reports[] = $report;
            if ($report['overall'] !== 'pass') {
                continue;
            }
            $dedupe = $this->article_plan_product_dedupe_key($campaign);
            if ($dedupe === 'title:' || isset($seen[$dedupe]) || $this->article_plan_product_title_is_near_duplicate($campaign, $selected_titles)) {
                continue;
            }
            $seen[$dedupe] = true;
            $selected_titles[] = $this->article_plan_normalize_heading((string) ($campaign['title'] ?? $campaign['name'] ?? ''));
            $product_ids[] = absint($campaign['post_id'] ?? 0);
            if (count($product_ids) >= 3) {
                break;
            }
        }
        $plan['products']['reports'] = array_slice($reports, 0, 20);
        if (!empty($product_ids)) {
            $plan['products']['status'] = 'ready';
            $plan['products']['campaign_post_ids'] = $product_ids;
            $plan['products']['reason'] = count($product_ids) . ' freigegebene, passende und deduplizierte Produkte.';
        } else {
            $plan['products']['status'] = 'none';
            $plan['products']['reason'] = 'Keine Produkte mit PASS-Qualität.';
        }

        $has_banner = $plan['banner']['status'] === 'ready';
        $has_products = $plan['products']['status'] === 'ready';
        $plan['status'] = ($has_banner || $has_products) ? 'ready' : 'no_output';
        update_post_meta($post_id, self::ARTICLE_PLAN_META, $plan);
        $this->article_plan_log_event('plan_built', $post_id, array(
            'reason' => sanitize_text_field((string) $reason),
            'status' => $plan['status'],
            'banner_status' => $plan['banner']['status'],
            'product_count' => count($plan['products']['campaign_post_ids']),
        ));
        return $plan;
    }

    public function handle_article_plan_post_save($post_id, $post, $update) {
        if (!$post instanceof WP_Post || $post->post_type !== 'post' || wp_is_post_revision($post_id) || wp_is_post_autosave($post_id)) {
            return;
        }
        if (in_array($post->post_status, array('trash', 'auto-draft'), true)) {
            return;
        }
        if ($this->article_hybrid_enabled()) {
            $this->article_plan_build($post_id, $update ? 'post_updated' : 'post_created');
        } else {
            delete_post_meta($post_id, self::ARTICLE_PLAN_META);
        }
    }

    public function handle_rebuild_article_plans() {
        if (!current_user_can('manage_options')) {
            wp_die('Keine Berechtigung.');
        }
        check_admin_referer('ppar_rebuild_article_plans', 'ppar_article_plans_nonce');
        $posts = get_posts(array(
            'post_type' => 'post',
            'post_status' => array('publish', 'draft', 'pending', 'private'),
            'numberposts' => -1,
            'fields' => 'ids',
        ));
        $built = 0;
        foreach ((array) $posts as $post_id) {
            if (!is_wp_error($this->article_plan_build($post_id, 'bulk_rebuild'))) {
                $built++;
            }
        }
        wp_safe_redirect(add_query_arg(array(
            'page' => 'affiliate-portal-article-hybrid',
            'ppar_plans_rebuilt' => $built,
        ), admin_url('admin.php')));
        exit;
    }

    public function handle_rebuild_single_article_plan() {
        if (!current_user_can('manage_options')) {
            wp_die('Keine Berechtigung.');
        }
        $post_id = absint($_POST['post_id'] ?? 0);
        check_admin_referer('ppar_rebuild_single_article_plan_' . $post_id, 'ppar_single_plan_nonce');
        $result = $this->article_plan_build($post_id, 'single_rebuild');
        wp_safe_redirect(add_query_arg(array(
            'page' => 'affiliate-portal-article-hybrid',
            'ppar_plan_rebuilt' => is_wp_error($result) ? '0' : '1',
            'post_id' => $post_id,
        ), admin_url('admin.php')));
        exit;
    }

    private function article_plan_campaign_publicly_usable($campaign, $slot_type, $creative_type) {
        if (!is_array($campaign) || sanitize_key((string) ($campaign['creative_type'] ?? 'banner')) !== $creative_type) {
            return false;
        }
        return $this->campaign_is_complete($campaign)
            && !empty($campaign['active'])
            && $this->rule_is_current($campaign)
            && $this->campaign_program_allows_delivery($campaign)
            && $this->campaign_control_allows_delivery($campaign, $slot_type)
            && $this->campaign_health_allows_delivery($campaign)
            && $this->campaign_slot_allowed($campaign, $slot_type);
    }

    /**
     * V2.7.5: Fällt ein fest geplanter Beitragsplatz wegen Link-Quarantäne oder
     * kritischer Sperre aus, wird nur innerhalb desselben vorhandenen Slots ein
     * bereits freigegebenes, passendes Ersatzwerbemittel gewählt. Position und
     * Design bleiben unverändert.
     */
    private function article_plan_find_fallback_campaign($post_id, $slot_type, $creative_type, $excluded_post_ids = array()) {
        $excluded_post_ids = array_values(array_unique(array_filter(array_map('absint', (array) $excluded_post_ids))));
        $context = $this->get_content_context($post_id);
        foreach ($this->ranked_campaigns_for_slot($context, $slot_type) as $candidate) {
            $campaign = $candidate['campaign'] ?? null;
            $candidate_id = absint(is_array($campaign) ? ($campaign['post_id'] ?? 0) : 0);
            if ($candidate_id <= 0 || in_array($candidate_id, $excluded_post_ids, true)) {
                continue;
            }
            if (!$this->article_plan_campaign_publicly_usable($campaign, $slot_type, $creative_type)) {
                continue;
            }
            if ($creative_type === 'banner') {
                if ((int) ($candidate['specificity'] ?? 0) < 200 || !$this->article_plan_program_verified($campaign)) {
                    continue;
                }
            } else {
                $report = $this->article_product_quality_report($campaign, $context, $candidate);
                if (($report['overall'] ?? 'fail') !== 'pass') {
                    continue;
                }
            }
            return $campaign;
        }
        return null;
    }

    private function article_plan_render_banner_campaign($post_id, $campaign_post_id, $admin_test = false) {
        $campaign_post_id = absint($campaign_post_id);
        $campaign = $this->campaign_from_post(get_post($campaign_post_id));
        // Der Administrator-Test prüft ausschließlich Position und dynamische
        // Bannerfläche. Er darf nicht an Gruppen-Konvertierung, Aktivstatus oder
        // öffentlicher Auslieferungsfreigabe scheitern.
        if ($admin_test) {
            if (!$campaign || sanitize_key((string) ($campaign['creative_type'] ?? 'banner')) !== 'banner') {
                return '';
            }
            return $this->render_article_banner_test_surface(array(
                'dimensions' => (string) ($campaign['dimensions'] ?? ''),
                'html' => (string) ($campaign['html'] ?? ''),
                'image_url' => (string) ($campaign['image_url'] ?? ''),
            ), 1);
        }
        if (!$this->article_plan_campaign_publicly_usable($campaign, 'post_inline_banner', 'banner')) {
            $campaign = $this->article_plan_find_fallback_campaign($post_id, 'post_inline_banner', 'banner', array($campaign_post_id));
            if (!$campaign) {
                return '';
            }
        }
        list($group, $banner) = $this->campaign_to_group_banner($campaign);
        if (!$group || !$banner) {
            return '';
        }
        $resolved_campaign_post_id = absint($campaign['post_id'] ?? 0);
        $banner['url'] = $this->build_click_tracking_url($resolved_campaign_post_id, $post_id, 'post_inline_banner');
        $html = $this->render_banner($banner, $post_id, $this->get_content_context($post_id), $group, 'post_inline_banner');
        if (trim((string) $html) === '') {
            return '';
        }
        return '<div class="ppar-affiliate-slot ppar-slot-post_inline_banner ppar-article-inline-banner ppar-article-inline-banner-1" data-ppar-slot="post_inline_banner">'
            . $this->get_disclosure_html($post_id)
            . '<div class="ppar-affiliate-content">' . $html . '</div></div>';
    }

    private function article_plan_render_products($post_id, $campaign_post_ids, $admin_test = false, $preview_count = 0) {
        $campaign_post_ids = array_slice(array_values(array_unique(array_filter(array_map('absint', (array) $campaign_post_ids)))), 0, 3);
        $desired_count = count($campaign_post_ids);
        $campaigns = array();
        $excluded_ids = $campaign_post_ids;
        $seen = array();
        $selected_titles = array();

        foreach ($campaign_post_ids as $campaign_post_id) {
            $campaign = $this->campaign_from_post(get_post($campaign_post_id));
            if (!$campaign || sanitize_key((string) ($campaign['creative_type'] ?? 'banner')) !== 'product' || !$this->campaign_is_complete($campaign)) {
                continue;
            }
            if (!$admin_test && !$this->article_plan_campaign_publicly_usable($campaign, 'post_bottom_products', 'product')) {
                continue;
            }
            $dedupe = $this->article_plan_product_dedupe_key($campaign);
            if ($dedupe === 'title:' || isset($seen[$dedupe]) || $this->article_plan_product_title_is_near_duplicate($campaign, $selected_titles)) {
                continue;
            }
            $seen[$dedupe] = true;
            $selected_titles[] = $this->article_plan_normalize_heading((string) ($campaign['title'] ?? $campaign['name'] ?? ''));
            $campaigns[] = $campaign;
        }

        if (!$admin_test && count($campaigns) < $desired_count) {
            $context = $this->get_content_context($post_id);
            $required_cohort = !empty($campaigns) && method_exists($this, 'ebay_product_campaign_cohort') ? $this->ebay_product_campaign_cohort($campaigns[0]) : '';
            foreach ($this->ranked_campaigns_for_slot($context, 'post_bottom_products') as $candidate) {
                $campaign = $candidate['campaign'] ?? null;
                if ($required_cohort !== '' && method_exists($this, 'ebay_product_campaign_cohort') && $this->ebay_product_campaign_cohort($campaign) !== $required_cohort) { continue; }
                $candidate_id = absint(is_array($campaign) ? ($campaign['post_id'] ?? 0) : 0);
                if ($candidate_id <= 0 || in_array($candidate_id, $excluded_ids, true)) {
                    continue;
                }
                $excluded_ids[] = $candidate_id;
                if (!$this->article_plan_campaign_publicly_usable($campaign, 'post_bottom_products', 'product')) {
                    continue;
                }
                $report = $this->article_product_quality_report($campaign, $context, $candidate);
                if (($report['overall'] ?? 'fail') !== 'pass') {
                    continue;
                }
                $dedupe = $this->article_plan_product_dedupe_key($campaign);
                if ($dedupe === 'title:' || isset($seen[$dedupe]) || $this->article_plan_product_title_is_near_duplicate($campaign, $selected_titles)) {
                    continue;
                }
                $seen[$dedupe] = true;
                $selected_titles[] = $this->article_plan_normalize_heading((string) ($campaign['title'] ?? $campaign['name'] ?? ''));
                $campaigns[] = $campaign;
                if (count($campaigns) >= $desired_count) {
                    break;
                }
            }
        }

        if (!$admin_test && method_exists($this, 'ebay_product_campaigns_share_provider_cohort') && !$this->ebay_product_campaigns_share_provider_cohort($campaigns)) {
            return '';
        }
        $cards = array();
        foreach ($campaigns as $campaign) {
            list($group, $banner) = $this->campaign_to_group_banner($campaign);
            if (!$group || !$banner) {
                continue;
            }
            $resolved_campaign_post_id = absint($campaign['post_id'] ?? 0);
            $banner['url'] = $this->build_click_tracking_url($resolved_campaign_post_id, $post_id, 'post_bottom_products');
            $html = $this->render_banner($banner, $post_id, $this->get_content_context($post_id), $group, 'post_bottom_products');
            if (trim((string) $html) !== '') {
                $cards[] = '<div class="ppar-article-product-card">' . $html . '</div>';
            }
        }
        if ($admin_test && $preview_count > count($cards)) {
            while (count($cards) < min(3, max(0, (int) $preview_count))) {
                $cards[] = '<div class="ppar-article-product-card ppar-article-product-test-surface" aria-hidden="true"></div>';
            }
        }
        if (empty($cards)) {
            return '';
        }
        $count = count($cards);
        $out = '<section class="ppar-article-product-block" data-ppar-product-count="' . $count . '">';
        if (!$admin_test) {
            $out .= $this->get_disclosure_html($post_id);
        }
        $out .= '<div class="ppar-article-section-label">Produktvorschläge</div>';
        $out .= '<div class="ppar-article-product-grid ppar-article-product-count-' . $count . '">' . implode('', $cards) . '</div></section>';
        return $out;
    }

    private function article_plan_apply_to_content($content, $post_id) {
        $preview = $this->article_preview_for_post($post_id);
        if ($preview) {
            $anchor = $this->article_plan_find_anchor((string) $content);
            $banner_id = absint($preview['banner_campaign_ids'][0] ?? 0);
            if ($banner_id > 0 && !empty($anchor)) {
                $offset = $this->article_plan_find_render_offset($content, $anchor);
                $banner_html = $this->article_plan_render_banner_campaign($post_id, $banner_id, true);
                if ($offset > 0 && $banner_html !== '') {
                    $content = $this->insert_at_offset($content, $banner_html, $offset);
                }
            }
            $product_html = $this->article_plan_render_products(
                $post_id,
                (array) ($preview['product_campaign_ids'] ?? array()),
                true,
                (int) ($preview['product_preview_count'] ?? 0)
            );
            return $product_html !== '' ? $content . "\n" . $product_html : $content;
        }

        $plan = $this->article_plan_get($post_id);
        if (!$this->article_plan_is_current($post_id, $plan)) {
            $this->article_plan_log_event('render_skipped_stale', $post_id, array('status' => $plan['status'] ?? 'missing'));
            return $content;
        }
        if (in_array((string) ($plan['banner']['status'] ?? ''), array('ready', 'pending_anchor'), true)) {
            $anchor = (array) ($plan['banner']['anchor'] ?? array());
            $offset = !empty($anchor) ? $this->article_plan_find_render_offset($content, $anchor) : 0;
            if ($offset <= 0) {
                $anchor = $this->article_plan_find_anchor((string) $content);
                $offset = !empty($anchor) ? $this->article_plan_find_render_offset($content, $anchor) : 0;
                if ($offset > 0) {
                    $plan['banner']['status'] = 'ready';
                    $plan['banner']['anchor'] = $anchor;
                    $plan['banner']['reason'] = 'Sicherer Anker am vollständig gerenderten Beitrag gespeichert.';
                    update_post_meta($post_id, self::ARTICLE_PLAN_META, $plan);
                    $this->article_plan_log_event('banner_anchor_resolved', $post_id, array('heading' => $anchor['heading'] ?? '', 'level' => $anchor['heading_level'] ?? 0));
                }
            }
            $banner_html = $this->article_plan_render_banner_campaign($post_id, absint($plan['banner']['campaign_post_id'] ?? 0), false);
            if ($offset > 0 && $banner_html !== '') {
                $content = $this->insert_at_offset($content, $banner_html, $offset);
            } else {
                $this->article_plan_log_event('banner_render_skipped', $post_id, array('offset' => $offset, 'has_html' => $banner_html !== ''));
            }
        }
        if (($plan['products']['status'] ?? '') === 'ready') {
            $product_html = $this->article_plan_render_products($post_id, (array) ($plan['products']['campaign_post_ids'] ?? array()), false, 0);
            if ($product_html !== '') {
                $content .= "\n" . $product_html;
            }
        }
        return $content;
    }
}
