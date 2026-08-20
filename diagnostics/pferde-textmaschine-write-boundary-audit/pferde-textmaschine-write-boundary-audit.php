<?php
/**
 * Plugin Name: Pferde Textmaschine Write-Boundary Audit
 * Description: Read-only/hash-only live audit for the WordPress draft insertion boundary used by Portal-Produktionsmaschine. Does not alter filter values, posts, terms, article content, design or production rules.
 * Version: 0.1.0
 * Requires PHP: 8.0
 * Author: Workflow Audit
 */

if (!defined('ABSPATH')) { return; }

final class Pferde_Textmaschine_Write_Boundary_Audit {
    const VERSION = '0.1.0';
    const OPTION_RESULT = 'ptm_write_boundary_audit_result_v1';
    const OPTION_ARMED = 'ptm_write_boundary_audit_armed_v1';
    const NONCE = 'ptm_write_boundary_audit_admin_v1';
    const PAGE = 'ptm-write-boundary-audit';
    const CONTRACT = 'PTM_WRITE_BOUNDARY_AUDIT_V1_HASH_ONLY';

    private static array $events = [];
    private static bool $ppm_seen = false;
    private static bool $persisted = false;
    private static int $seq = 0;
    private static array $hooks = [
        'pre_post_title',
        'title_save_pre',
        'pre_post_content',
        'content_save_pre',
        'pre_post_excerpt',
        'excerpt_save_pre',
        'wp_insert_post_empty_content',
    ];

    public static function boot(): void {
        add_action('admin_menu', [__CLASS__, 'admin_menu']);
        add_action('admin_post_ptm_write_audit_download', [__CLASS__, 'download']);
        add_action('admin_post_ptm_write_audit_rearm', [__CLASS__, 'rearm']);

        if (!self::armed()) { return; }

        $early = -PHP_INT_MAX;
        $late  = PHP_INT_MAX;
        foreach (['pre_post_title','title_save_pre','pre_post_content','content_save_pre','pre_post_excerpt','excerpt_save_pre'] as $hook) {
            add_filter($hook, [__CLASS__, 'observe_string_early'], $early, 1);
            add_filter($hook, [__CLASS__, 'observe_string_late'], $late, 1);
        }
        add_filter('wp_insert_post_empty_content', [__CLASS__, 'observe_empty_early'], $early, 2);
        add_filter('wp_insert_post_empty_content', [__CLASS__, 'observe_empty_late'], $late, 2);
        add_action('shutdown', [__CLASS__, 'shutdown'], PHP_INT_MAX);
    }

    public static function activate(): void {
        update_option(self::OPTION_ARMED, '1', false);
        delete_option(self::OPTION_RESULT);
    }

    private static function armed(): bool {
        return (string)get_option(self::OPTION_ARMED, '0') === '1';
    }

    public static function observe_string_early($value) {
        self::capture_string((string)current_filter(), 'EARLY', $value);
        return $value;
    }

    public static function observe_string_late($value) {
        self::capture_string((string)current_filter(), 'LATE', $value);
        return $value;
    }

    public static function observe_empty_early($maybe_empty, $postarr) {
        self::capture_empty('EARLY', $maybe_empty, $postarr);
        return $maybe_empty;
    }

    public static function observe_empty_late($maybe_empty, $postarr) {
        self::capture_empty('LATE', $maybe_empty, $postarr);
        return $maybe_empty;
    }

    private static function capture_string(string $hook, string $phase, $value): void {
        $trace = self::trace();
        if (!$trace['ppm_insert_draft_path']) { return; }
        self::$ppm_seen = true;
        self::$events[] = [
            'seq' => ++self::$seq,
            'hook' => $hook,
            'phase' => $phase,
            'value' => self::value_fingerprint($value),
            'trace' => $trace,
        ];
    }

    private static function capture_empty(string $phase, $maybe_empty, $postarr): void {
        $trace = self::trace();
        if (!$trace['ppm_insert_draft_path']) { return; }
        self::$ppm_seen = true;
        $postarr = is_array($postarr) ? $postarr : [];
        self::$events[] = [
            'seq' => ++self::$seq,
            'hook' => 'wp_insert_post_empty_content',
            'phase' => $phase,
            'maybe_empty' => (bool)$maybe_empty,
            'postarr' => [
                'post_type' => (string)($postarr['post_type'] ?? ''),
                'post_status' => (string)($postarr['post_status'] ?? ''),
                'post_title' => self::value_fingerprint($postarr['post_title'] ?? ''),
                'post_content' => self::value_fingerprint($postarr['post_content'] ?? ''),
                'post_excerpt' => self::value_fingerprint($postarr['post_excerpt'] ?? ''),
                'post_name' => self::value_fingerprint($postarr['post_name'] ?? ''),
                'canonical_article_id_sha256' => isset($postarr['meta_input']['_ppm679_canonical_article_id'])
                    ? hash('sha256', (string)$postarr['meta_input']['_ppm679_canonical_article_id']) : '',
                'article_type_sha256' => isset($postarr['meta_input']['_ppm679_article_type'])
                    ? hash('sha256', (string)$postarr['meta_input']['_ppm679_article_type']) : '',
            ],
            'trace' => $trace,
        ];
    }

    public static function value_fingerprint($value): array {
        if (!is_string($value)) {
            return ['type' => gettype($value), 'length' => null, 'sha256' => '', 'is_empty' => empty($value)];
        }
        return [
            'type' => 'string',
            'length' => strlen($value),
            'sha256' => hash('sha256', $value),
            'is_empty' => $value === '',
        ];
    }

    private static function trace(): array {
        $frames = debug_backtrace(DEBUG_BACKTRACE_IGNORE_ARGS, 32);
        $out = [];
        $ppm = false;
        foreach ($frames as $frame) {
            $file = (string)($frame['file'] ?? '');
            $class = (string)($frame['class'] ?? '');
            $function = (string)($frame['function'] ?? '');
            if (str_contains($file, 'portal-production-machine') || str_starts_with($class, 'PPM679_')) { $ppm = true; }
            if (count($out) < 14) {
                $out[] = [
                    'file' => self::relative_path($file),
                    'line' => (int)($frame['line'] ?? 0),
                    'call' => trim($class . (isset($frame['type']) ? (string)$frame['type'] : '') . $function),
                ];
            }
        }
        return ['ppm_insert_draft_path' => $ppm, 'frames' => $out];
    }

    public static function shutdown(): void {
        if (self::$persisted || !self::$ppm_seen || !self::$events) { return; }
        self::$persisted = true;
        $result = [
            'contract' => self::CONTRACT,
            'version' => self::VERSION,
            'status' => 'CAPTURED',
            'captured_at_utc' => gmdate('c'),
            'wordpress_version' => isset($GLOBALS['wp_version']) ? (string)$GLOBALS['wp_version'] : '',
            'php_version' => PHP_VERSION,
            'request' => [
                'action' => isset($_REQUEST['action']) ? sanitize_key((string)wp_unslash($_REQUEST['action'])) : '',
                'is_admin' => is_admin(),
                'doing_ajax' => function_exists('wp_doing_ajax') ? wp_doing_ajax() : false,
            ],
            'scope' => [
                'hash_only' => true,
                'raw_article_text_stored' => false,
                'filter_values_modified' => false,
                'post_write_performed_by_audit' => false,
                'term_write_performed_by_audit' => false,
                'design_write_performed_by_audit' => false,
                'production_rule_modified' => false,
            ],
            'hook_inventory' => self::hook_inventory(),
            'events' => self::$events,
            'diagnosis' => self::diagnosis(self::$events),
        ];
        $body = $result;
        $body['result_sha256'] = hash('sha256', wp_json_encode($body, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE));
        update_option(self::OPTION_RESULT, $body, false);
        update_option(self::OPTION_ARMED, '0', false);
    }

    public static function diagnosis(array $events): array {
        $string = [];
        $empty = [];
        foreach ($events as $event) {
            if (($event['hook'] ?? '') === 'wp_insert_post_empty_content') {
                $empty[(string)($event['phase'] ?? '')] = $event;
            } else {
                $string[(string)($event['hook'] ?? '')][(string)($event['phase'] ?? '')] = $event;
            }
        }
        $blanked = [];
        foreach ($string as $hook => $pair) {
            $a = $pair['EARLY']['value'] ?? null;
            $b = $pair['LATE']['value'] ?? null;
            if (is_array($a) && is_array($b) && empty($a['is_empty']) && !empty($b['is_empty'])) { $blanked[] = $hook; }
        }
        $forced = false;
        if (isset($empty['EARLY'], $empty['LATE'])) {
            $forced = empty($empty['EARLY']['maybe_empty']) && !empty($empty['LATE']['maybe_empty']);
        }
        $postarr_nonempty_at_empty_gate = false;
        if (isset($empty['EARLY']['postarr'])) {
            $p = $empty['EARLY']['postarr'];
            $postarr_nonempty_at_empty_gate = empty($p['post_title']['is_empty']) || empty($p['post_content']['is_empty']) || empty($p['post_excerpt']['is_empty']);
        }
        return [
            'save_pre_or_pre_post_blanked_hooks' => $blanked,
            'wp_insert_post_empty_content_forced_false_to_true' => $forced,
            'postarr_has_nonempty_title_content_or_excerpt_at_empty_gate' => $postarr_nonempty_at_empty_gate,
            'interpretation' => $forced
                ? 'DIRECT_EMPTY_CONTENT_FILTER_OVERRIDE_DETECTED'
                : ($blanked ? 'SANITIZATION_FILTER_BLANKING_DETECTED' : 'NO_VALUE_MUTATION_PROVEN_BY_AUDIT_YET'),
        ];
    }

    public static function hook_inventory(): array {
        global $wp_filter;
        $result = [];
        foreach (self::$hooks as $hook) {
            $rows = [];
            $obj = $wp_filter[$hook] ?? null;
            if (is_object($obj) && isset($obj->callbacks) && is_array($obj->callbacks)) {
                foreach ($obj->callbacks as $priority => $callbacks) {
                    foreach ((array)$callbacks as $id => $entry) {
                        $fn = $entry['function'] ?? null;
                        $meta = self::callback_meta($fn);
                        $rows[] = [
                            'priority' => (int)$priority,
                            'id' => (string)$id,
                            'accepted_args' => (int)($entry['accepted_args'] ?? 1),
                            'callback' => $meta,
                            'is_audit_callback' => self::is_audit_callback($fn),
                        ];
                    }
                }
            }
            $result[$hook] = $rows;
        }
        return $result;
    }

    private static function is_audit_callback($fn): bool {
        return is_array($fn) && isset($fn[0], $fn[1]) && $fn[0] === __CLASS__;
    }

    private static function callback_meta($fn): array {
        $name = 'unknown'; $file = ''; $start = 0; $end = 0;
        try {
            if (is_string($fn)) {
                $name = $fn; $r = new ReflectionFunction($fn);
            } elseif (is_array($fn) && count($fn) === 2) {
                $target = $fn[0]; $method = (string)$fn[1];
                $class = is_object($target) ? get_class($target) : (string)$target;
                $name = $class . '::' . $method; $r = new ReflectionMethod($target, $method);
            } elseif ($fn instanceof Closure) {
                $name = 'Closure'; $r = new ReflectionFunction($fn);
            } elseif (is_object($fn) && is_callable($fn)) {
                $name = get_class($fn) . '::__invoke'; $r = new ReflectionMethod($fn, '__invoke');
            } else {
                return ['name' => $name, 'source_file' => '', 'start_line' => 0, 'end_line' => 0, 'source_scope' => 'UNKNOWN'];
            }
            $file = (string)$r->getFileName(); $start = (int)$r->getStartLine(); $end = (int)$r->getEndLine();
        } catch (Throwable $e) {
            return ['name' => $name, 'source_file' => '', 'start_line' => 0, 'end_line' => 0, 'source_scope' => 'REFLECTION_FAILED'];
        }
        return [
            'name' => $name,
            'source_file' => self::relative_path($file),
            'start_line' => $start,
            'end_line' => $end,
            'source_scope' => self::source_scope($file),
        ];
    }

    private static function source_scope(string $file): string {
        if ($file === '') { return 'INTERNAL_OR_UNKNOWN'; }
        if (defined('WP_PLUGIN_DIR') && str_starts_with($file, rtrim((string)WP_PLUGIN_DIR, '/\\') . DIRECTORY_SEPARATOR)) { return 'PLUGIN'; }
        if (defined('WPMU_PLUGIN_DIR') && str_starts_with($file, rtrim((string)WPMU_PLUGIN_DIR, '/\\') . DIRECTORY_SEPARATOR)) { return 'MU_PLUGIN'; }
        if (defined('WP_CONTENT_DIR') && str_starts_with($file, rtrim((string)WP_CONTENT_DIR, '/\\') . DIRECTORY_SEPARATOR)) { return 'WP_CONTENT'; }
        if (defined('ABSPATH') && str_starts_with($file, rtrim((string)ABSPATH, '/\\') . DIRECTORY_SEPARATOR)) { return 'WORDPRESS_CORE_OR_ROOT'; }
        return 'EXTERNAL';
    }

    private static function relative_path(string $file): string {
        if ($file === '') { return ''; }
        $file = str_replace('\\', '/', $file);
        $roots = [];
        if (defined('ABSPATH')) $roots['ABSPATH'] = str_replace('\\', '/', rtrim((string)ABSPATH, '/\\'));
        if (defined('WP_CONTENT_DIR')) $roots['WP_CONTENT_DIR'] = str_replace('\\', '/', rtrim((string)WP_CONTENT_DIR, '/\\'));
        if (defined('WP_PLUGIN_DIR')) $roots['WP_PLUGIN_DIR'] = str_replace('\\', '/', rtrim((string)WP_PLUGIN_DIR, '/\\'));
        if (defined('WPMU_PLUGIN_DIR')) $roots['WPMU_PLUGIN_DIR'] = str_replace('\\', '/', rtrim((string)WPMU_PLUGIN_DIR, '/\\'));
        uasort($roots, fn($a,$b) => strlen($b) <=> strlen($a));
        foreach ($roots as $label => $root) {
            if ($root !== '' && ($file === $root || str_starts_with($file, $root . '/'))) {
                return $label . substr($file, strlen($root));
            }
        }
        return basename($file);
    }

    public static function admin_menu(): void {
        add_management_page('Textmaschinen Write-Audit', 'Textmaschinen Write-Audit', 'manage_options', self::PAGE, [__CLASS__, 'render']);
    }

    public static function render(): void {
        if (!current_user_can('manage_options')) { wp_die('Forbidden'); }
        $result = get_option(self::OPTION_RESULT, []);
        echo '<div class="wrap"><h1>Textmaschinen Write-Audit</h1>';
        echo '<p><strong>Status:</strong> ' . esc_html(self::armed() ? 'WARTET AUF NÄCHSTEN PPM-DRAFTVERSUCH' : (is_array($result) && !empty($result) ? 'ERGEBNIS ERFASST' : 'NICHT SCHARF')) . '</p>';
        echo '<p>Der Audit verändert keine Filterwerte und speichert nur Längen, SHA-256-Hashes, Hook-/Callback-Metadaten und technische Ablaufdaten. Kein Artikeltext wird gespeichert.</p>';
        if (is_array($result) && !empty($result)) {
            $diag = is_array($result['diagnosis'] ?? null) ? $result['diagnosis'] : [];
            echo '<p><strong>Diagnose:</strong> ' . esc_html((string)($diag['interpretation'] ?? '')) . '</p>';
            $url = wp_nonce_url(admin_url('admin-post.php?action=ptm_write_audit_download'), self::NONCE);
            echo '<p><a class="button button-primary" href="' . esc_url($url) . '">Audit-JSON herunterladen</a></p>';
        }
        $rearm = wp_nonce_url(admin_url('admin-post.php?action=ptm_write_audit_rearm'), self::NONCE);
        echo '<p><a class="button" href="' . esc_url($rearm) . '">Audit zurücksetzen und erneut scharfstellen</a></p>';
        echo '</div>';
    }

    public static function download(): void {
        if (!current_user_can('manage_options')) { wp_die('Forbidden'); }
        check_admin_referer(self::NONCE);
        $result = get_option(self::OPTION_RESULT, []);
        if (!is_array($result) || empty($result)) { wp_die('Kein Audit-Ergebnis vorhanden.'); }
        nocache_headers();
        header('Content-Type: application/json; charset=utf-8');
        header('Content-Disposition: attachment; filename="ptm-write-boundary-audit-' . gmdate('Ymd-His') . '-utc.json"');
        echo wp_json_encode($result, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
        exit;
    }

    public static function rearm(): void {
        if (!current_user_can('manage_options')) { wp_die('Forbidden'); }
        check_admin_referer(self::NONCE);
        delete_option(self::OPTION_RESULT);
        update_option(self::OPTION_ARMED, '1', false);
        wp_safe_redirect(admin_url('tools.php?page=' . self::PAGE));
        exit;
    }
}

register_activation_hook(__FILE__, ['Pferde_Textmaschine_Write_Boundary_Audit', 'activate']);
Pferde_Textmaschine_Write_Boundary_Audit::boot();
