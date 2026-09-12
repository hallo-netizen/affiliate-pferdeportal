<?php
if (!defined('ABSPATH')) { exit; }

final class UGE_Policy {
    public static function init(): void {
        add_action('template_redirect', [__CLASS__, 'protect_group_route'], 0);
        add_filter('the_content', [__CLASS__, 'append_primary_category_link'], 30);
    }

    public static function protect_group_route(): void {
        if (is_tax(UGE_Core::TAXONOMY)) {
            remove_action('template_redirect', [UGE_Core::class, 'redirect_legacy_term_url'], 1);
        }
    }

    public static function append_primary_category_link(string $content): string {
        if (!is_singular(UGE_Core::POST_TYPE) || !in_the_loop() || !is_main_query()) { return $content; }
        $post_id = get_the_ID();
        if ($post_id <= 0) { return $content; }
        $target = UGE_Core::primary_category_target($post_id);
        if (!$target) { return $content; }

        $link = sprintf(
            '<p class="uge-primary-category">Zum Themenbereich: <a href="%s">%s</a></p>',
            esc_url((string)$target['url']),
            esc_html((string)$target['label'])
        );
        return $content . $link;
    }
}
