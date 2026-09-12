<?php
if (!defined('ABSPATH')) { exit; }

final class UGE_Admin {
    public static function init(): void {
        add_action('admin_menu', [__CLASS__, 'menu']);
        add_action('add_meta_boxes', [__CLASS__, 'meta_boxes']);
        add_action('save_post_' . UGE_Core::POST_TYPE, [__CLASS__, 'save_meta'], 10, 2);
        add_action('admin_init', [__CLASS__, 'settings']);
    }

    public static function menu(): void {
        $cfg = UGE_Config::get();
        add_menu_page($cfg['label'], $cfg['label'], 'edit_posts', 'uge-glossary', [__CLASS__, 'dashboard'], 'dashicons-book-alt', 26);
        add_submenu_page('uge-glossary', 'Alle Begriffe', 'Alle Begriffe', 'edit_posts', 'edit.php?post_type=' . UGE_Core::POST_TYPE);
        add_submenu_page('uge-glossary', 'Neuer Begriff', 'Neuer Begriff', 'edit_posts', 'post-new.php?post_type=' . UGE_Core::POST_TYPE);
        add_submenu_page('uge-glossary', 'Oberbereiche', 'Oberbereiche', 'manage_categories', 'edit-tags.php?taxonomy=' . UGE_Core::TAXONOMY . '&post_type=' . UGE_Core::POST_TYPE);
        add_submenu_page('uge-glossary', 'Einstellungen', 'Einstellungen', 'manage_options', 'uge-settings', [__CLASS__, 'settings_page']);
    }

    public static function dashboard(): void {
        if (!current_user_can('edit_posts')) { wp_die('Keine Berechtigung.'); }
        echo '<div class="wrap"><h1>' . esc_html(UGE_Config::get()['label']) . '</h1><p>Begriffe, Oberbereiche und Ausgabe werden hier getrennt von normalen Beiträgen verwaltet.</p></div>';
    }

    public static function settings(): void {
        register_setting('uge_settings', UGE_Config::OPTION, ['sanitize_callback' => [UGE_Config::class, 'sanitize']]);
    }

    public static function settings_page(): void {
        if (!current_user_can('manage_options')) { return; }
        $c = UGE_Config::get();
        echo '<div class="wrap"><h1>Glossar – Einstellungen</h1><form method="post" action="options.php">';
        settings_fields('uge_settings');
        self::input('label', 'Bezeichnung', $c['label']);
        self::input('term_label', 'Bezeichnung einzelner Datensatz', $c['term_label']);
        self::input('group_label', 'Bezeichnung Oberbereiche', $c['group_label']);
        self::input('main_page_id', 'ID der vorhandenen Glossar-Hauptseite', (string)$c['main_page_id'], 'number');
        self::input('rewrite_base', 'URL-Basis', $c['rewrite_base']);
        self::input('seo_title_pattern', 'SEO-Titel-Schema', $c['seo_title_pattern']);
        self::textarea('seo_description_pattern', 'Meta-Description-Schema', $c['seo_description_pattern']);
        self::input('accordion_excerpt_words', 'Wörter in Kurzansicht', (string)$c['accordion_excerpt_words'], 'number');
        self::checkbox('show_search', 'Suche anzeigen', $c['show_search']);
        self::checkbox('show_az', 'A–Z anzeigen', $c['show_az']);
        self::checkbox('show_groups', 'Oberbereiche anzeigen', $c['show_groups']);
        submit_button();
        echo '</form></div>';
    }

    private static function input(string $key, string $label, string $value, string $type='text'): void {
        printf('<p><label><strong>%s</strong><br><input class="regular-text" type="%s" name="%s[%s]" value="%s"></label></p>', esc_html($label), esc_attr($type), esc_attr(UGE_Config::OPTION), esc_attr($key), esc_attr($value));
    }
    private static function textarea(string $key, string $label, string $value): void {
        printf('<p><label><strong>%s</strong><br><textarea class="large-text" rows="3" name="%s[%s]">%s</textarea></label></p>', esc_html($label), esc_attr(UGE_Config::OPTION), esc_attr($key), esc_textarea($value));
    }
    private static function checkbox(string $key, string $label, $value): void {
        printf('<p><label><input type="checkbox" name="%s[%s]" value="1" %s> %s</label></p>', esc_attr(UGE_Config::OPTION), esc_attr($key), checked(1, (int)$value, false), esc_html($label));
    }

    public static function meta_boxes(): void {
        add_meta_box('uge_term_data', 'Glossar-Daten', [__CLASS__, 'meta_box'], UGE_Core::POST_TYPE, 'normal', 'high');
    }

    public static function meta_box(WP_Post $post): void {
        wp_nonce_field('uge_save_term', 'uge_nonce');
        foreach (UGE_Config::field_schema() as $key => $field) {
            $value = UGE_Core::term_value($post->ID, $key);
            echo '<p><label><strong>' . esc_html($field['label']) . '</strong><br>';
            if (($field['type'] ?? '') === 'textarea') {
                printf('<textarea class="large-text" rows="4" name="uge_fields[%s]">%s</textarea>', esc_attr($key), esc_textarea($value));
            } elseif (($field['type'] ?? '') === 'select') {
                printf('<select name="uge_fields[%s]">', esc_attr($key));
                foreach (($field['options'] ?? []) as $opt => $label) {
                    printf('<option value="%s" %s>%s</option>', esc_attr($opt), selected($value, $opt, false), esc_html($label));
                }
                echo '</select>';
            } else {
                $type = ($field['type'] ?? '') === 'url' ? 'url' : 'text';
                printf('<input class="large-text" type="%s" name="uge_fields[%s]" value="%s">', esc_attr($type), esc_attr($key), esc_attr($value));
            }
            echo '</label></p>';
        }
    }

    public static function save_meta(int $post_id, WP_Post $post): void {
        if (defined('DOING_AUTOSAVE') && DOING_AUTOSAVE) { return; }
        if (!isset($_POST['uge_nonce']) || !wp_verify_nonce(sanitize_text_field(wp_unslash($_POST['uge_nonce'])), 'uge_save_term')) { return; }
        if (!current_user_can('edit_post', $post_id)) { return; }
        if ($post->post_type !== UGE_Core::POST_TYPE) { return; }
        $submitted = isset($_POST['uge_fields']) && is_array($_POST['uge_fields']) ? wp_unslash($_POST['uge_fields']) : [];
        foreach (UGE_Config::field_schema() as $key => $field) {
            $raw = $submitted[$key] ?? '';
            $type = $field['type'] ?? 'text';
            if ($type === 'textarea') { $value = sanitize_textarea_field($raw); }
            elseif ($type === 'url') { $value = esc_url_raw($raw); }
            elseif ($type === 'select') {
                $allowed = array_keys($field['options'] ?? []);
                $value = in_array($raw, $allowed, true) ? $raw : '';
            } else { $value = sanitize_text_field($raw); }
            update_post_meta($post_id, UGE_Core::meta_key($key), $value);
        }
    }
}
