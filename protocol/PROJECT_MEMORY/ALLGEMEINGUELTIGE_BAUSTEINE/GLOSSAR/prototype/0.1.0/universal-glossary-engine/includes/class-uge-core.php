<?php
if (!defined('ABSPATH')) { exit; }

final class UGE_Core {
    const POST_TYPE = 'uge_term';
    const TAXONOMY = 'uge_group';
    const META_PREFIX = '_uge_';

    public static function init(): void {
        add_action('init', [__CLASS__, 'register_content']);
        add_action('update_option_' . UGE_Config::OPTION, [__CLASS__, 'settings_updated'], 10, 2);
    }

    public static function activate(): void {
        self::register_content();
        flush_rewrite_rules();
    }

    public static function deactivate(): void {
        flush_rewrite_rules();
    }

    public static function settings_updated($old, $new): void {
        if (($old['rewrite_base'] ?? '') !== ($new['rewrite_base'] ?? '')) {
            self::register_content();
            flush_rewrite_rules(false);
        }
    }

    public static function register_content(): void {
        $cfg = UGE_Config::get();
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
            'rewrite' => ['slug' => $cfg['rewrite_base'], 'with_front' => false],
            'supports' => ['title', 'editor', 'revisions'],
            'menu_icon' => 'dashicons-book-alt',
        ]);

        register_taxonomy(self::TAXONOMY, [self::POST_TYPE], [
            'labels' => [
                'name' => $cfg['group_label'],
                'singular_name' => 'Oberbereich',
                'add_new_item' => 'Oberbereich hinzufügen',
                'edit_item' => 'Oberbereich bearbeiten',
            ],
            'public' => false,
            'show_ui' => true,
            'show_admin_column' => true,
            'show_in_rest' => true,
            'hierarchical' => true,
            'rewrite' => false,
        ]);
    }

    public static function meta_key(string $field): string {
        return self::META_PREFIX . sanitize_key($field);
    }

    public static function term_value(int $post_id, string $field): string {
        return (string) get_post_meta($post_id, self::meta_key($field), true);
    }
}
