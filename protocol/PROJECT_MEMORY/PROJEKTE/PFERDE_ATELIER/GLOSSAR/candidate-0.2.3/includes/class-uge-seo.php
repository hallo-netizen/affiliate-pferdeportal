<?php
if (!defined('ABSPATH')) { exit; }

final class UGE_SEO {
    public static function init(): void {
        add_filter('document_title_parts', [__CLASS__, 'document_title_parts'], 20);
        add_action('wp_head', [__CLASS__, 'fallback_meta'], 1);
        add_filter('get_canonical_url', [__CLASS__, 'core_canonical'], 20, 2);
        add_filter('wp_robots', [__CLASS__, 'core_robots'], 20);
        add_filter('wpseo_title', [__CLASS__, 'yoast_title'], 20);
        add_filter('wpseo_metadesc', [__CLASS__, 'yoast_description'], 20);
        add_filter('wpseo_canonical', [__CLASS__, 'yoast_canonical'], 20);
        add_filter('wpseo_robots', [__CLASS__, 'yoast_robots'], 20);
    }

    public static function document_title_parts(array $parts): array {
        if (!is_singular(UGE_Core::POST_TYPE)) { return $parts; }
        $parts['title'] = self::title(get_queried_object_id());
        return $parts;
    }

    public static function title(int $post_id): string {
        $custom = UGE_Core::term_value($post_id, 'seo_title');
        return $custom !== '' ? $custom : self::pattern(UGE_Config::get()['seo_title_pattern'], $post_id);
    }

    public static function description(int $post_id): string {
        $custom = UGE_Core::term_value($post_id, 'seo_description');
        return $custom !== '' ? $custom : self::pattern(UGE_Config::get()['seo_description_pattern'], $post_id);
    }

    public static function canonical(int $post_id): string {
        $custom = UGE_Core::term_value($post_id, 'canonical');
        return $custom !== '' ? $custom : get_permalink($post_id);
    }

    public static function index_mode(int $post_id): string {
        $mode = UGE_Core::term_value($post_id, 'index_mode');
        return in_array($mode, ['index','noindex'], true) ? $mode : UGE_Config::get()['index_mode'];
    }

    public static function pattern(string $pattern, int $post_id): string {
        $repl = [
            '{term}' => get_the_title($post_id),
            '{site}' => get_bloginfo('name'),
            '{glossary_label}' => UGE_Config::get()['label'],
        ];
        return trim(strtr($pattern, $repl));
    }

    public static function fallback_meta(): void {
        if (!is_singular(UGE_Core::POST_TYPE)) { return; }
        if (defined('WPSEO_VERSION')) { return; }
        $id = get_queried_object_id();
        printf("\n<meta name=\"description\" content=\"%s\">", esc_attr(self::description($id)));
    }

    public static function core_canonical(string $canonical, $post): string {
        if (!is_singular(UGE_Core::POST_TYPE)) { return $canonical; }
        $id = is_object($post) && isset($post->ID) ? (int)$post->ID : get_queried_object_id();
        return self::canonical($id);
    }

    public static function core_robots(array $robots): array {
        if (is_tax(UGE_Core::TAXONOMY)) {
            $robots['noindex'] = true;
            unset($robots['index']);
            return $robots;
        }
        if (is_singular(UGE_Core::POST_TYPE) && self::index_mode(get_queried_object_id()) === 'noindex') {
            $robots['noindex'] = true;
            unset($robots['index']);
        }
        return $robots;
    }

    public static function yoast_title(string $value): string {
        return is_singular(UGE_Core::POST_TYPE) ? self::title(get_queried_object_id()) : $value;
    }
    public static function yoast_description(string $value): string {
        return is_singular(UGE_Core::POST_TYPE) ? self::description(get_queried_object_id()) : $value;
    }
    public static function yoast_canonical(string $value): string {
        return is_singular(UGE_Core::POST_TYPE) ? self::canonical(get_queried_object_id()) : $value;
    }
    public static function yoast_robots($robots) {
        if (is_tax(UGE_Core::TAXONOMY)) {
            if (is_array($robots)) { $robots['index'] = 'noindex'; return $robots; }
            return 'noindex,follow';
        }
        if (!is_singular(UGE_Core::POST_TYPE) || self::index_mode(get_queried_object_id()) !== 'noindex') { return $robots; }
        if (is_array($robots)) { $robots['index'] = 'noindex'; return $robots; }
        return 'noindex,follow';
    }
}
