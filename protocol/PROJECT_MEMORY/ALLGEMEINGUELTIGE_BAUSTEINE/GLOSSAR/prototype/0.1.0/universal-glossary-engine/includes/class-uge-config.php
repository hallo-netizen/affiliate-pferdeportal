<?php
if (!defined('ABSPATH')) { exit; }

final class UGE_Config {
    const OPTION = 'uge_settings_v1';

    public static function defaults(): array {
        return [
            'label' => 'Glossar',
            'term_label' => 'Begriff',
            'group_label' => 'Oberbereiche',
            'main_page_id' => 0,
            'rewrite_base' => 'glossar',
            'seo_title_pattern' => '{term} – Bedeutung & Erklärung | {site}',
            'seo_description_pattern' => '{term}: kurze und verständliche Erklärung im {glossary_label}.',
            'index_mode' => 'index',
            'show_az' => 1,
            'show_search' => 1,
            'show_groups' => 1,
            'accordion_excerpt_words' => 45,
            'design_profile' => 'auto',
        ];
    }

    public static function get(): array {
        $saved = get_option(self::OPTION, []);
        if (!is_array($saved)) { $saved = []; }
        $cfg = array_merge(self::defaults(), $saved);
        return apply_filters('uge_config', $cfg);
    }

    public static function sanitize(array $input): array {
        $d = self::defaults();
        $out = [];
        $out['label'] = sanitize_text_field($input['label'] ?? $d['label']);
        $out['term_label'] = sanitize_text_field($input['term_label'] ?? $d['term_label']);
        $out['group_label'] = sanitize_text_field($input['group_label'] ?? $d['group_label']);
        $out['main_page_id'] = absint($input['main_page_id'] ?? 0);
        $base = sanitize_title($input['rewrite_base'] ?? $d['rewrite_base']);
        $out['rewrite_base'] = $base !== '' ? $base : $d['rewrite_base'];
        $out['seo_title_pattern'] = sanitize_text_field($input['seo_title_pattern'] ?? $d['seo_title_pattern']);
        $out['seo_description_pattern'] = sanitize_text_field($input['seo_description_pattern'] ?? $d['seo_description_pattern']);
        $out['index_mode'] = in_array(($input['index_mode'] ?? 'index'), ['index','noindex'], true) ? $input['index_mode'] : 'index';
        $out['show_az'] = empty($input['show_az']) ? 0 : 1;
        $out['show_search'] = empty($input['show_search']) ? 0 : 1;
        $out['show_groups'] = empty($input['show_groups']) ? 0 : 1;
        $out['accordion_excerpt_words'] = max(10, min(120, absint($input['accordion_excerpt_words'] ?? $d['accordion_excerpt_words'])));
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
            'accent' => '#2f6f55',
            'secondary' => '#3b82b8',
            'ink' => '#1f2522',
            'muted' => '#65706a',
            'line' => '#e4e8e5',
            'surface' => '#ffffff',
            'radius' => '18px',
            'font_size' => '16px',
            'line_height' => '1.55',
        ];
        $profile = self::get()['design_profile'] ?? 'auto';
        if ($profile === 'auto' && class_exists('Pferde_Template_Kit') && method_exists('Pferde_Template_Kit', 'design_profile')) {
            $profile = (string) Pferde_Template_Kit::design_profile();
        }
        if ($profile === 'pferde_atelier') {
            $tokens = array_merge($tokens, [
                'accent' => '#27a653',
                'secondary' => '#37abf2',
                'ink' => '#172018',
                'muted' => '#5e665f',
                'line' => '#e7ebe7',
                'surface' => '#ffffff',
                'radius' => '22px',
                'font_size' => '16px',
                'line_height' => '1.55',
            ]);
        }
        return apply_filters('uge_design_tokens', $tokens, $profile);
    }
}
