<?php
if (!defined('ABSPATH')) { exit; }

final class UGE_Config {
    const OPTION = 'uge_settings_v1';

    public static function defaults(): array {
        return [
            'label' => 'Glossar',
            'term_label' => 'Begriff',
            'group_label' => 'Bereiche',
            'main_page_id' => 0,
            'rewrite_base' => 'glossar',
            'term_segment' => 'begriff',
            'seo_title_pattern' => '{term} – Bedeutung & Erklärung | {site}',
            'seo_description_pattern' => '{term}: kurze und verständliche Erklärung im {glossary_label}.',
            'index_mode' => 'index',
            'show_az' => 1,
            'show_search' => 1,
            'show_groups' => 1,
            'home_term_count' => 6,
            'category_per_page' => 24,
            'design_profile' => 'auto',
        ];
    }

    public static function get(): array {
        $saved = get_option(self::OPTION, []);
        if (!is_array($saved)) { $saved = []; }
        return apply_filters('uge_config', array_merge(self::defaults(), $saved));
    }

    public static function sanitize(array $input): array {
        $d = self::defaults();
        $out = [];
        $out['label'] = sanitize_text_field($input['label'] ?? $d['label']);
        $out['term_label'] = sanitize_text_field($input['term_label'] ?? $d['term_label']);
        $out['group_label'] = sanitize_text_field($input['group_label'] ?? $d['group_label']);
        $out['main_page_id'] = absint($input['main_page_id'] ?? 0);
        $base = sanitize_title($input['rewrite_base'] ?? $d['rewrite_base']);
        $segment = sanitize_title($input['term_segment'] ?? $d['term_segment']);
        $out['rewrite_base'] = $base !== '' ? $base : $d['rewrite_base'];
        $out['term_segment'] = $segment !== '' ? $segment : $d['term_segment'];
        $out['seo_title_pattern'] = sanitize_text_field($input['seo_title_pattern'] ?? $d['seo_title_pattern']);
        $out['seo_description_pattern'] = sanitize_text_field($input['seo_description_pattern'] ?? $d['seo_description_pattern']);
        $out['index_mode'] = in_array(($input['index_mode'] ?? 'index'), ['index','noindex'], true) ? $input['index_mode'] : 'index';
        $out['show_az'] = empty($input['show_az']) ? 0 : 1;
        $out['show_search'] = empty($input['show_search']) ? 0 : 1;
        $out['show_groups'] = empty($input['show_groups']) ? 0 : 1;
        $out['home_term_count'] = max(3, min(12, absint($input['home_term_count'] ?? $d['home_term_count'])));
        $out['category_per_page'] = max(12, min(60, absint($input['category_per_page'] ?? $d['category_per_page'])));
        $out['design_profile'] = sanitize_key($input['design_profile'] ?? 'auto') ?: 'auto';
        return apply_filters('uge_sanitized_config', $out, $input);
    }

    public static function field_schema(): array {
        $schema = [
            'short_definition' => ['label' => 'Kurzdefinition', 'type' => 'textarea', 'required' => true],
            'synonyms' => ['label' => 'Synonyme', 'type' => 'text', 'required' => false],
            'related_terms' => ['label' => 'Verwandte Begriffe', 'type' => 'text', 'required' => false],
            'seo_title' => ['label' => 'SEO-Titel', 'type' => 'text', 'required' => false],
            'seo_description' => ['label' => 'Meta-Description', 'type' => 'textarea', 'required' => false],
            'canonical' => ['label' => 'Canonical URL', 'type' => 'url', 'required' => false],
            'index_mode' => ['label' => 'Indexierung', 'type' => 'select', 'options' => ['inherit'=>'Standard','index'=>'Index','noindex'=>'Noindex'], 'required' => false],
        ];
        return apply_filters('uge_field_schema', $schema);
    }

    public static function design_tokens(): array {
        $tokens = [
            'olive' => '#303B31',
            'olive2' => '#667564',
            'ochre' => '#A97916',
            'paper' => '#F7F4ED',
            'text' => '#4E554E',
            'muted' => '#626A62',
            'line' => 'rgba(48,59,49,.18)',
            'surface' => '#FFFFFF',
        ];
        $profile = self::get()['design_profile'] ?? 'auto';
        if ($profile === 'auto' && class_exists('Pferde_Template_Kit')) {
            $profile = method_exists('Pferde_Template_Kit', 'design_profile')
                ? (string) Pferde_Template_Kit::design_profile()
                : 'pferde_atelier';
        }
        if ($profile === 'pferde_atelier') {
            // Werte aus dem aktuellen V104-Designvertrag / Live-Designplugin.
            $tokens = [
                'olive' => '#35422A',
                'olive2' => '#6A7F4A',
                'ochre' => '#C89214',
                'paper' => '#F7F2E8',
                'text' => '#4F564D',
                'muted' => '#5D645B',
                'line' => 'rgba(53,66,42,.18)',
                'surface' => '#FFFFFF',
            ];
        }
        return apply_filters('uge_design_tokens', $tokens, $profile);
    }
}
