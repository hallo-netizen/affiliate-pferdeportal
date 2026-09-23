<?php
if (!defined('ABSPATH')) { exit; }

final class APKW_Central_Admin {
    private const PAGE_SLUG = 'apkw-central-categories';
    private const MAX_UPLOAD_BYTES = 20971520;
    private const PREVIEW_TTL = 900;

    public static function init(): void {
        add_action('admin_menu', [__CLASS__, 'menu']);
        add_action('admin_post_apkw_central_export', [__CLASS__, 'export']);
        add_action('admin_post_apkw_central_rollback', [__CLASS__, 'rollback']);
    }

    public static function menu(): void {
        add_menu_page('Kategorien', 'Kategorien', 'manage_options', self::PAGE_SLUG, [__CLASS__, 'render'], 'dashicons-category', 58);
    }

    public static function render(): void {
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.','Zugriff verweigert',['response'=>403]); }
        $notice = null; $error = null; $preview = null; $token = null;

        if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['apkw_central_preview'])) {
            check_admin_referer('apkw_central_preview','apkw_central_preview_nonce');
            try {
                [$package] = self::read_upload('central_structure_package');
                $preview = APKW_Central_Category_Registry::preview_package($package);
                $reason = sanitize_text_field(wp_unslash((string)($_POST['apkw_central_reason'] ?? '')));
                if ($reason === '') { throw new RuntimeException('Änderungsgrund fehlt.'); }
                $allow_deletions = isset($_POST['apkw_central_allow_deletions']) && (string)$_POST['apkw_central_allow_deletions'] === '1';
                if (!empty($preview['diff']['removed']) && !$allow_deletions) { throw new RuntimeException('Löschungen erkannt. Löschbestätigung fehlt.'); }
                $token = bin2hex(random_bytes(16));
                set_transient('apkw_central_preview_'.$token, [
                    'package'=>$package,
                    'expected_previous_sha256'=>$preview['expected_previous_sha256'],
                    'reason'=>$reason,
                    'allow_deletions'=>$allow_deletions,
                    'user_id'=>get_current_user_id(),
                ], self::PREVIEW_TTL);
            } catch (Throwable $e) { $error = $e->getMessage(); }
        }

        if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['apkw_central_commit'])) {
            check_admin_referer('apkw_central_commit','apkw_central_commit_nonce');
            try {
                $commit_token = sanitize_text_field(wp_unslash((string)($_POST['apkw_central_token'] ?? '')));
                $saved = get_transient('apkw_central_preview_'.$commit_token);
                if (!is_array($saved)) { throw new RuntimeException('Vorschau abgelaufen oder ungültig.'); }
                if ((int)($saved['user_id'] ?? 0) !== get_current_user_id()) { throw new RuntimeException('Vorschau gehört zu einem anderen Benutzer.'); }
                $result = APKW_Central_Category_Registry::commit_package(
                    $saved['package'],
                    (string)$saved['expected_previous_sha256'],
                    (string)$saved['reason'],
                    (bool)$saved['allow_deletions'],
                    get_current_user_id()
                );
                delete_transient('apkw_central_preview_'.$commit_token);
                $notice = 'Zentraler Kategorienstand übernommen. Generation '.(int)$result['snapshot']['generation'].'.';
            } catch (Throwable $e) { $error = $e->getMessage(); }
        }

        $status = APKW_Central_Category_Registry::status();
        $log = array_reverse(APKW_Central_Category_Registry::change_log());
        ?>
        <div class="wrap"><h1>Kategorien</h1>
        <div class="notice notice-info inline"><p><strong>Eine Wahrheit:</strong> Nur der hier freigegebene zentrale Kategorienstand ist die Sollquelle. Andere Plugins dürfen daraus ableiten, aber keine eigene Kategorien-Wahrheit führen.</p></div>
        <div class="notice notice-warning inline"><p><strong>Keine stillen Portal-Writes:</strong> Dieses Büro verwaltet und versioniert den zentralen Sollstand. WordPress-/HivePress-Inhalte und andere Plugins werden nicht heimlich beim Seitenaufruf verändert.</p></div>
        <?php if($notice):?><div class="notice notice-success inline"><p><?php echo esc_html($notice);?></p></div><?php endif;?>
        <?php if($error):?><div class="notice notice-error inline"><p><?php echo esc_html($error);?></p></div><?php endif;?>

        <h2>Aktueller zentraler Stand</h2>
        <table class="widefat striped" style="max-width:900px"><tbody>
        <tr><th>Generation</th><td><?php echo esc_html((string)$status['generation']);?></td></tr>
        <tr><th>Kategorien/Knoten</th><td><?php echo esc_html((string)$status['node_count']);?></td></tr>
        <tr><th>SHA-256</th><td><code><?php echo esc_html($status['category_set_sha256']);?></code></td></tr>
        <tr><th>Fallback</th><td><?php echo $status['fallback_available']?'vorhanden':'noch nicht vorhanden';?></td></tr>
        </tbody></table>
        <p><a class="button" href="<?php echo esc_url(wp_nonce_url(admin_url('admin-post.php?action=apkw_central_export'),'apkw_central_export'));?>">Aktuellen Stand als JSON exportieren</a></p>

        <hr><h2>Neuen Kategorienstand prüfen</h2>
        <form method="post" enctype="multipart/form-data">
        <?php wp_nonce_field('apkw_central_preview','apkw_central_preview_nonce');?>
        <input type="hidden" name="MAX_FILE_SIZE" value="<?php echo esc_attr((string)self::MAX_UPLOAD_BYTES);?>">
        <p><label><strong>FINAL_APPROVED-Strukturpaket:</strong><br><input type="file" name="central_structure_package" accept="application/json,.json" required></label></p>
        <p><label><strong>Änderungsgrund:</strong><br><input class="large-text" name="apkw_central_reason" required></label></p>
        <p><label><input type="checkbox" name="apkw_central_allow_deletions" value="1"> Ich bestätige ausdrücklich erkannte Löschungen/Entfernungen.</label></p>
        <?php submit_button('Nur prüfen – noch nichts übernehmen','secondary','apkw_central_preview');?>
        </form>

        <?php if(is_array($preview) && $token):?>
        <h3>Vorschau PASS</h3>
        <table class="widefat striped" style="max-width:900px"><tbody>
        <tr><th>Neue Generation</th><td><?php echo esc_html((string)$preview['snapshot']['generation']);?></td></tr>
        <tr><th>Neu</th><td><?php echo esc_html(implode(', ',$preview['diff']['added']) ?: '—');?></td></tr>
        <tr><th>Entfernt</th><td><?php echo esc_html(implode(', ',$preview['diff']['removed']) ?: '—');?></td></tr>
        <tr><th>Geändert</th><td><?php echo esc_html(implode(', ',$preview['diff']['changed']) ?: '—');?></td></tr>
        <tr><th>Unverändert</th><td><?php echo esc_html((string)$preview['diff']['unchanged_count']);?></td></tr>
        </tbody></table>
        <form method="post">
        <?php wp_nonce_field('apkw_central_commit','apkw_central_commit_nonce');?>
        <input type="hidden" name="apkw_central_token" value="<?php echo esc_attr($token);?>">
        <?php submit_button('Diesen geprüften Stand zentral übernehmen','primary','apkw_central_commit');?>
        </form>
        <?php endif;?>

        <?php if($status['fallback_available']):?>
        <hr><h2>Sicheres Fallback</h2>
        <form method="post" action="<?php echo esc_url(admin_url('admin-post.php'));?>">
        <input type="hidden" name="action" value="apkw_central_rollback">
        <?php wp_nonce_field('apkw_central_rollback','apkw_central_rollback_nonce');?>
        <p><label><strong>Rollback-Grund:</strong><br><input class="large-text" name="apkw_central_rollback_reason" required></label></p>
        <p><label><input type="checkbox" name="apkw_central_rollback_confirm" value="1" required> Ich bestätige das Zurückrollen auf den letzten gespeicherten Fallback.</label></p>
        <?php submit_button('Auf letzten Fallback zurückrollen','delete');?>
        </form>
        <?php endif;?>

        <hr><h2>Änderungsprotokoll</h2>
        <table class="widefat striped"><thead><tr><th>Generation</th><th>Zeit</th><th>Aktion</th><th>Grund</th><th>Neu</th><th>Entfernt</th><th>Geändert</th><th>SHA-256</th></tr></thead><tbody>
        <?php if(!$log):?><tr><td colspan="8">Noch keine zentrale Änderung.</td></tr><?php else: foreach($log as $row):?>
        <tr><td><?php echo esc_html((string)($row['generation']??''));?></td><td><?php echo esc_html((string)($row['timestamp_utc']??''));?></td><td><?php echo esc_html((string)($row['action']??''));?></td><td><?php echo esc_html((string)($row['reason']??''));?></td><td><?php echo esc_html(implode(', ',(array)($row['added']??[])));?></td><td><?php echo esc_html(implode(', ',(array)($row['removed']??[])));?></td><td><?php echo esc_html(implode(', ',(array)($row['changed']??[])));?></td><td><code><?php echo esc_html((string)($row['current_sha256']??''));?></code></td></tr>
        <?php endforeach; endif;?></tbody></table>
        </div><?php
    }

    public static function export(): void {
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.','Zugriff verweigert',['response'=>403]); }
        check_admin_referer('apkw_central_export');
        $payload = APKW_Central_Category_Registry::export_payload();
        nocache_headers();
        header('Content-Type: application/json; charset=utf-8');
        header('Content-Disposition: attachment; filename="pferde-atelier-kategorien-generation-'.(int)$payload['generation'].'.json"');
        echo wp_json_encode($payload, JSON_PRETTY_PRINT|JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);
        exit;
    }

    public static function rollback(): void {
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.','Zugriff verweigert',['response'=>403]); }
        check_admin_referer('apkw_central_rollback','apkw_central_rollback_nonce');
        if (!isset($_POST['apkw_central_rollback_confirm']) || (string)$_POST['apkw_central_rollback_confirm'] !== '1') { wp_die('Rollback-Bestätigung fehlt.','Rollback blockiert',['response'=>400]); }
        $reason = sanitize_text_field(wp_unslash((string)($_POST['apkw_central_rollback_reason'] ?? '')));
        APKW_Central_Category_Registry::rollback_to_fallback($reason, get_current_user_id());
        wp_safe_redirect(admin_url('admin.php?page='.self::PAGE_SLUG));
        exit;
    }

    private static function read_upload(string $field): array {
        if (!isset($_FILES[$field]) || !is_array($_FILES[$field])) { throw new RuntimeException('Datei fehlt.'); }
        $file = $_FILES[$field];
        if ((int)($file['error'] ?? UPLOAD_ERR_NO_FILE) !== UPLOAD_ERR_OK) { throw new RuntimeException('Upload fehlgeschlagen.'); }
        if ((int)($file['size'] ?? 0) < 1 || (int)$file['size'] > self::MAX_UPLOAD_BYTES) { throw new RuntimeException('Dateigröße ungültig.'); }
        $tmp = (string)($file['tmp_name'] ?? '');
        if ($tmp === '' || !is_uploaded_file($tmp)) { throw new RuntimeException('Uploadquelle ungültig.'); }
        $raw = file_get_contents($tmp);
        if (!is_string($raw) || $raw === '') { throw new RuntimeException('Datei leer.'); }
        $decoded = json_decode($raw, true, 512, JSON_THROW_ON_ERROR);
        if (!is_array($decoded)) { throw new RuntimeException('JSON muss ein Objekt sein.'); }
        return [$decoded, $raw];
    }
}
