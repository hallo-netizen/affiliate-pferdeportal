<?php
if (!defined('ABSPATH')) { exit; }

final class UGE_Core {
    const POST_TYPE = 'uge_term';
    const TAXONOMY = 'uge_group';
    const META_PREFIX = '_uge_';
    const REWRITE_SCHEMA_OPTION = 'uge_rewrite_schema_version';
    const REWRITE_SCHEMA_VERSION = '2';
    private static bool $collision_guard = false;

    public static function init(): void {
        add_action('init', [__CLASS__, 'register_content']);
        add_action('init', [__CLASS__, 'maybe_upgrade_rewrites'], 99);
        add_action('update_option_' . UGE_Config::OPTION, [__CLASS__, 'settings_updated'], 10, 2);
        add_filter('wp_insert_post_data', [__CLASS__, 'enforce_glossary_collision_on_save'], 20, 4);
        add_action('wp_after_insert_post', [__CLASS__, 'enforce_primary_category_after_save'], 100, 4);
        add_action('template_redirect', [__CLASS__, 'redirect_legacy_term_url'], 1);
    }

    public static function activate(): void {
        self::register_content();
        flush_rewrite_rules();
        update_option(self::REWRITE_SCHEMA_OPTION, self::REWRITE_SCHEMA_VERSION, false);
    }

    public static function deactivate(): void {
        flush_rewrite_rules();
    }

    public static function maybe_upgrade_rewrites(): void {
        if ((string)get_option(self::REWRITE_SCHEMA_OPTION, '') === self::REWRITE_SCHEMA_VERSION) { return; }
        flush_rewrite_rules(false);
        update_option(self::REWRITE_SCHEMA_OPTION, self::REWRITE_SCHEMA_VERSION, false);
    }

    public static function settings_updated($old, $new): void {
        $old_base = $old['rewrite_base'] ?? '';
        $new_base = $new['rewrite_base'] ?? '';
        $old_segment = $old['term_segment'] ?? '';
        $new_segment = $new['term_segment'] ?? '';
        if ($old_base !== $new_base || $old_segment !== $new_segment) {
            self::register_content();
            flush_rewrite_rules(false);
        }
    }

    public static function redirect_legacy_term_url(): void {
        if (is_admin() || wp_doing_ajax() || empty($_SERVER['REQUEST_URI'])) { return; }
        $cfg = UGE_Config::get();
        $base = trim((string)$cfg['rewrite_base'], '/');
        $segment = trim((string)$cfg['term_segment'], '/');
        $path = trim((string)wp_parse_url(wp_unslash($_SERVER['REQUEST_URI']), PHP_URL_PATH), '/');
        if ($base === '' || $path === '' || !preg_match('#^' . preg_quote($base, '#') . '/([^/]+)/?$#', $path, $m)) { return; }
        $slug = sanitize_title(rawurldecode((string)$m[1]));
        if ($slug === '' || $slug === $segment) { return; }
        $post = get_page_by_path($slug, OBJECT, self::POST_TYPE);
        if (!$post instanceof WP_Post || $post->post_status !== 'publish') { return; }
        $target = get_permalink($post);
        if (!$target) { return; }
        wp_safe_redirect($target, 301, 'Universal Glossary Engine');
        exit;
    }

    public static function register_content(): void {
        $cfg = UGE_Config::get();
        $base = trim((string)$cfg['rewrite_base'], '/');
        $segment = trim((string)$cfg['term_segment'], '/');
        $term = $cfg['term_label'];

        register_post_type(self::POST_TYPE, [
            'labels' => [
                'name' => $cfg['label'] . ' – Begriffe',
                'singular_name' => $term,
                'add_new_item' => 'Neuen ' . $term . ' anlegen',
                'edit_item' => $term . ' bearbeiten',
                'search_items' => $term . ' suchen',
            ],
            'public' => true,
            'publicly_queryable' => true,
            'show_ui' => true,
            'show_in_menu' => 'uge-glossary',
            'show_in_rest' => true,
            'has_archive' => false,
            'exclude_from_search' => false,
            'rewrite' => ['slug' => $base . '/' . $segment, 'with_front' => false],
            'supports' => ['title', 'editor', 'revisions'],
            'menu_icon' => 'dashicons-book-alt',
            'map_meta_cap' => true,
        ]);

        register_taxonomy(self::TAXONOMY, [self::POST_TYPE], [
            'labels' => [
                'name' => $cfg['group_label'],
                'singular_name' => 'Bereich',
                'add_new_item' => 'Bereich hinzufügen',
                'edit_item' => 'Bereich bearbeiten',
            ],
            'public' => true,
            'publicly_queryable' => true,
            'show_ui' => true,
            'show_admin_column' => true,
            'show_in_rest' => true,
            'hierarchical' => true,
            'query_var' => true,
            'rewrite' => ['slug' => $base, 'with_front' => false, 'hierarchical' => true],
        ]);
    }

    /**
     * Harte Kollision nur noch zwischen Glossarbegriffen selbst.
     * Gleiche Namen wie Portal-/WordPress-/Glossar-Kategorien sind redaktionell
     * erlaubt und erzeugen lediglich einen SEO-Hinweis.
     */
    public static function collision(string $title, string $slug = '', int $exclude_post_id = 0): array {
        $name_key = sanitize_title($title);
        $slug_key = sanitize_title($slug !== '' ? $slug : $title);
        if ($name_key === '' && $slug_key === '') { return []; }

        $existing = get_posts([
            'post_type' => self::POST_TYPE,
            'post_status' => ['draft', 'pending', 'private', 'publish'],
            'numberposts' => -1,
            'exclude' => $exclude_post_id > 0 ? [$exclude_post_id] : [],
            'no_found_rows' => true,
        ]);
        foreach ($existing as $post) {
            $post_name = sanitize_title((string)$post->post_title);
            $post_slug = sanitize_title((string)$post->post_name);
            if (in_array($name_key, [$post_name, $post_slug], true) || in_array($slug_key, [$post_name, $post_slug], true)) {
                return ['type' => 'Glossarbegriff', 'label' => (string)$post->post_title, 'slug' => (string)$post->post_name];
            }
        }
        return [];
    }

    public static function category_overlap(string $title, string $slug = ''): array {
        $name_key = sanitize_title($title);
        $slug_key = sanitize_title($slug !== '' ? $slug : $title);
        if ($name_key === '' && $slug_key === '') { return []; }

        foreach ([self::TAXONOMY, 'category'] as $taxonomy) {
            if (!taxonomy_exists($taxonomy)) { continue; }
            $terms = get_terms(['taxonomy' => $taxonomy, 'hide_empty' => false]);
            if (is_wp_error($terms)) { continue; }
            foreach ($terms as $term) {
                $term_name = sanitize_title((string)$term->name);
                $term_slug = sanitize_title((string)$term->slug);
                if (in_array($name_key, [$term_name, $term_slug], true) || in_array($slug_key, [$term_name, $term_slug], true)) {
                    return [
                        'type' => $taxonomy === self::TAXONOMY ? 'Glossar-Kategorie' : 'WordPress-Kategorie',
                        'label' => (string)$term->name,
                        'slug' => (string)$term->slug,
                    ];
                }
            }
        }

        if (class_exists('Pferde_Template_Kit') && method_exists('Pferde_Template_Kit', 'affiliate_page_type')) {
            $page_ids = get_posts([
                'post_type' => 'page',
                'post_status' => 'publish',
                'numberposts' => -1,
                'fields' => 'ids',
                'no_found_rows' => true,
            ]);
            $main_page_id = (int)(UGE_Config::get()['main_page_id'] ?? 0);
            foreach ($page_ids as $page_id) {
                $page_id = (int)$page_id;
                if ($page_id === $main_page_id) { continue; }
                $page_type = (string)Pferde_Template_Kit::affiliate_page_type($page_id);
                if (!in_array($page_type, ['hub1', 'hub2', 'category', 'leaf'], true)) { continue; }
                $page = get_post($page_id);
                if (!$page instanceof WP_Post) { continue; }
                $page_name = sanitize_title((string)$page->post_title);
                $page_slug = sanitize_title((string)$page->post_name);
                if (in_array($name_key, [$page_name, $page_slug], true) || in_array($slug_key, [$page_name, $page_slug], true)) {
                    return ['type' => 'Portal-Kategorie', 'label' => (string)$page->post_title, 'slug' => (string)$page->post_name];
                }
            }
        }
        return [];
    }

    public static function enforce_glossary_collision_on_save(array $data, array $postarr, array $unsanitized_postarr, bool $update): array {
        if (($data['post_type'] ?? '') !== self::POST_TYPE || self::$collision_guard) { return $data; }
        if (in_array(($data['post_status'] ?? ''), ['auto-draft', 'trash', 'inherit'], true)) { return $data; }
        $post_id = isset($postarr['ID']) ? (int)$postarr['ID'] : 0;

        $duplicate = self::collision((string)($data['post_title'] ?? ''), (string)($data['post_name'] ?? ''), $post_id);
        if ($duplicate) {
            $data['post_status'] = 'draft';
            self::set_collision_notice(sprintf('SEO-Sperre: „%s“ existiert bereits als Glossarbegriff. Der neue Begriff bleibt Entwurf.', $duplicate['label']));
            return $data;
        }

        $overlap = self::category_overlap((string)($data['post_title'] ?? ''), (string)($data['post_name'] ?? ''));
        if ($overlap) {
            self::set_collision_notice(sprintf('SEO-Hinweis: „%s“ existiert auch als %s. Der Glossarbegriff ist erlaubt; redaktionell nur veröffentlichen, wenn er eine eigenständige definitorische Aufgabe erfüllt.', $overlap['label'], $overlap['type']));
        }
        return $data;
    }

    /**
     * Jeder veröffentlichte Glossarbegriff benötigt genau eine passende
     * Portal-Kategorie. Der gespeicherte Wert ist nur die Ziel-ID; Linktext und
     * URL werden immer live aus dem Zielobjekt abgeleitet.
     */
    public static function primary_category_target(int $post_id): array {
        $target_id = absint(self::term_value($post_id, 'primary_category_id'));
        $target = [];
        if ($target_id > 0) {
            $page = get_post($target_id);
            if ($page instanceof WP_Post && $page->post_type === 'page' && $page->post_status === 'publish') {
                $allowed = true;
                if (class_exists('Pferde_Template_Kit') && method_exists('Pferde_Template_Kit', 'affiliate_page_type')) {
                    $type = (string)Pferde_Template_Kit::affiliate_page_type($target_id);
                    $allowed = in_array($type, ['hub1', 'hub2', 'category', 'leaf'], true);
                }
                if ($allowed) {
                    $url = get_permalink($target_id);
                    if ($url) {
                        $target = [
                            'id' => $target_id,
                            'label' => get_the_title($target_id),
                            'url' => (string)$url,
                            'type' => 'page',
                        ];
                    }
                }
            }
        }
        $target = apply_filters('uge_primary_category_target', $target, $post_id, $target_id);
        if (!is_array($target)) { return []; }
        $label = trim((string)($target['label'] ?? ''));
        $url = esc_url_raw((string)($target['url'] ?? ''));
        if ($label === '' || $url === '') { return []; }
        $target['label'] = $label;
        $target['url'] = $url;
        return $target;
    }

    public static function enforce_primary_category_after_save(int $post_id, WP_Post $post, bool $update, ?WP_Post $post_before = null): void {
        if (self::$collision_guard || $post->post_type !== self::POST_TYPE || $post->post_status !== 'publish') { return; }
        if (!apply_filters('uge_require_primary_category', true, $post_id)) { return; }
        if (self::primary_category_target($post_id)) { return; }

        self::$collision_guard = true;
        wp_update_post(['ID' => $post_id, 'post_status' => 'draft']);
        self::$collision_guard = false;
        self::set_collision_notice('Veröffentlichung gestoppt: Für jeden Glossarbegriff muss eine gültige passende Portal-Kategorie hinterlegt sein.');
    }

    public static function set_collision_notice(string $message): void {
        $user_id = get_current_user_id();
        if ($user_id > 0) { set_transient('uge_collision_notice_' . $user_id, $message, 120); }
    }

    public static function pull_collision_notice(): string {
        $user_id = get_current_user_id();
        if ($user_id <= 0) { return ''; }
        $key = 'uge_collision_notice_' . $user_id;
        $value = (string)get_transient($key);
        if ($value !== '') { delete_transient($key); }
        return $value;
    }

    public static function meta_key(string $field): string {
        return self::META_PREFIX . sanitize_key($field);
    }

    public static function term_value(int $post_id, string $field): string {
        return (string)get_post_meta($post_id, self::meta_key($field), true);
    }
}
