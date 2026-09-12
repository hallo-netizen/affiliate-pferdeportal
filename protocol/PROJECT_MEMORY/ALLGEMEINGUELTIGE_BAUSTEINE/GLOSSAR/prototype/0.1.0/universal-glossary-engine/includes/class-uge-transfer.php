<?php
if (!defined('ABSPATH')) { exit; }

final class UGE_Transfer {
    const FORMAT = 'uge-json-v1';
    const MAX_BYTES = 5242880;

    public static function init(): void {
        add_action('admin_post_uge_export', [__CLASS__, 'export']);
        add_action('admin_post_uge_import', [__CLASS__, 'import']);
    }

    public static function page(): void {
        if (!current_user_can('manage_options')) { return; }
        $notice = isset($_GET['uge_notice']) ? sanitize_text_field(wp_unslash($_GET['uge_notice'])) : '';
        echo '<div class="wrap"><h1>Glossar – Import / Export</h1>';
        if ($notice !== '') { echo '<div class="notice notice-info"><p>' . esc_html($notice) . '</p></div>'; }
        echo '<h2>Export</h2><p>Exportiert Begriffe, Oberbereiche und Glossar-Felder als JSON.</p>';
        echo '<form method="post" action="' . esc_url(admin_url('admin-post.php')) . '"><input type="hidden" name="action" value="uge_export">';
        wp_nonce_field('uge_export', 'uge_transfer_nonce');
        submit_button('JSON exportieren', 'secondary');
        echo '</form>';
        echo '<hr><h2>Import</h2><p>Importierte Begriffe werden immer als Entwurf angelegt oder aktualisiert. Veröffentlichung bleibt manuell.</p>';
        echo '<form method="post" enctype="multipart/form-data" action="' . esc_url(admin_url('admin-post.php')) . '"><input type="hidden" name="action" value="uge_import">';
        wp_nonce_field('uge_import', 'uge_transfer_nonce');
        echo '<input type="file" name="uge_json" accept="application/json,.json" required>';
        submit_button('JSON als Entwürfe importieren');
        echo '</form></div>';
    }

    public static function export(): void {
        self::guard('uge_export');
        $posts = get_posts(['post_type'=>UGE_Core::POST_TYPE,'post_status'=>['draft','pending','private','publish'],'numberposts'=>-1,'orderby'=>'title','order'=>'ASC']);
        $items = [];
        foreach ($posts as $post) {
            $groups = wp_get_post_terms($post->ID, UGE_Core::TAXONOMY, ['fields'=>'names']);
            if (is_wp_error($groups)) { $groups = []; }
            $fields = [];
            foreach (UGE_Config::field_schema() as $key => $_field) { $fields[$key] = UGE_Core::term_value($post->ID, $key); }
            $items[] = [
                'external_id' => 'wp-' . $post->ID,
                'title' => $post->post_title,
                'slug' => $post->post_name,
                'content' => $post->post_content,
                'groups' => array_values($groups),
                'fields' => $fields,
            ];
        }
        $payload = ['format'=>self::FORMAT,'exported_at'=>gmdate('c'),'items'=>$items];
        nocache_headers();
        header('Content-Type: application/json; charset=utf-8');
        header('Content-Disposition: attachment; filename="glossary-export-' . gmdate('Ymd-His') . '.json"');
        echo wp_json_encode($payload, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
        exit;
    }

    public static function import(): void {
        self::guard('uge_import');
        if (empty($_FILES['uge_json']) || !isset($_FILES['uge_json']['tmp_name'], $_FILES['uge_json']['size']) || (int)$_FILES['uge_json']['size'] <= 0 || (int)$_FILES['uge_json']['size'] > self::MAX_BYTES) {
            self::back('Import abgelehnt: ungültige oder zu große Datei.');
        }
        $raw = file_get_contents($_FILES['uge_json']['tmp_name']);
        $data = json_decode((string)$raw, true);
        if (!is_array($data) || ($data['format'] ?? '') !== self::FORMAT || !isset($data['items']) || !is_array($data['items'])) {
            self::back('Import abgelehnt: ungültiges Format.');
        }
        $count = 0;
        foreach ($data['items'] as $row) {
            if (!is_array($row)) { continue; }
            $title = sanitize_text_field($row['title'] ?? '');
            if ($title === '') { continue; }
            $slug = sanitize_title($row['slug'] ?? $title);
            $existing = get_page_by_path($slug, OBJECT, UGE_Core::POST_TYPE);
            $postarr = [
                'post_type' => UGE_Core::POST_TYPE,
                'post_status' => 'draft',
                'post_title' => $title,
                'post_name' => $slug,
                'post_content' => wp_kses_post($row['content'] ?? ''),
            ];
            if ($existing instanceof WP_Post) { $postarr['ID'] = $existing->ID; }
            $post_id = wp_insert_post($postarr, true);
            if (is_wp_error($post_id)) { continue; }
            foreach (($row['groups'] ?? []) as $group_name) {
                $group_name = sanitize_text_field($group_name);
                if ($group_name !== '') { wp_set_object_terms($post_id, $group_name, UGE_Core::TAXONOMY, true); }
            }
            $allowed = UGE_Config::field_schema();
            foreach (($row['fields'] ?? []) as $key => $raw_value) {
                if (!isset($allowed[$key])) { continue; }
                $type = $allowed[$key]['type'] ?? 'text';
                if ($type === 'textarea') { $value = sanitize_textarea_field($raw_value); }
                elseif ($type === 'url') { $value = esc_url_raw($raw_value); }
                elseif ($type === 'select') {
                    $opts = array_keys($allowed[$key]['options'] ?? []);
                    $value = in_array($raw_value, $opts, true) ? $raw_value : '';
                } else { $value = sanitize_text_field($raw_value); }
                update_post_meta($post_id, UGE_Core::meta_key($key), $value);
            }
            $count++;
        }
        self::back($count . ' Begriff(e) als Entwurf importiert/aktualisiert.');
    }

    private static function guard(string $action): void {
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.'); }
        $nonce = isset($_REQUEST['uge_transfer_nonce']) ? sanitize_text_field(wp_unslash($_REQUEST['uge_transfer_nonce'])) : '';
        if (!wp_verify_nonce($nonce, $action)) { wp_die('Ungültige Sicherheitsprüfung.'); }
    }

    private static function back(string $notice): void {
        wp_safe_redirect(add_query_arg(['page'=>'uge-transfer','uge_notice'=>$notice], admin_url('admin.php')));
        exit;
    }
}
