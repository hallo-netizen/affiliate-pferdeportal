<?php
/**
 * Plugin Name: Pferde Atelier – Komplettsicherung
 * Description: Admin-Download der letzten geprüften Komplettsicherung. Erzeugt selbst keine Backups.
 * Version: 1.0.0
 */
if (!defined('ABSPATH')) exit;

function pa_backup_dir(): string {
    return defined('PA_BACKUP_OUTPUT_DIR') ? rtrim((string) PA_BACKUP_OUTPUT_DIR, '/') : '';
}
function pa_backup_manifest(): array {
    $dir = pa_backup_dir();
    if ($dir === '' || !is_readable($dir . '/latest.json')) return ['status'=>'BACKUP_FAIL:MANIFEST_MISSING'];
    $data = json_decode((string) file_get_contents($dir . '/latest.json'), true);
    return is_array($data) ? $data : ['status'=>'BACKUP_FAIL:MANIFEST_INVALID'];
}
add_action('admin_menu', function () {
    add_management_page('Pferde-Atelier Komplettsicherung','Komplettsicherung','manage_options','pferde-atelier-komplettsicherung','pa_backup_page');
});
function pa_backup_page(): void {
    if (!current_user_can('manage_options')) wp_die('Nicht erlaubt.',403);
    $m=pa_backup_manifest();
    $status=(string)($m['status']??'BACKUP_FAIL:STATUS_MISSING');
    $url=wp_nonce_url(admin_url('admin-post.php?action=pa_backup_download'),'pa_backup_download');
    echo '<div class="wrap"><h1>Pferde-Atelier Komplettsicherung</h1>';
    echo '<p><strong>Status:</strong> '.esc_html($status).'</p>';
    echo '<p><strong>Letzte Sicherung:</strong> '.esc_html((string)($m['created_at']??'–')).'</p>';
    echo '<p><strong>Dateigröße:</strong> '.esc_html(isset($m['size_bytes'])?size_format((int)$m['size_bytes'],2):'–').'</p>';
    if ($status==='BACKUP_PASS') {
        echo '<p><a class="button button-primary button-hero" href="'.esc_url($url).'">Komplettsicherung herunterladen</a></p>';
    } else {
        echo '<p><button class="button button-primary button-hero" disabled>Kein gültiges Komplettbackup verfügbar</button></p>';
    }
    echo '</div>';
}
add_action('admin_post_pa_backup_download', function () {
    if (!current_user_can('manage_options')) wp_die('Nicht erlaubt.',403);
    check_admin_referer('pa_backup_download');
    $m=pa_backup_manifest();
    if (($m['status']??'')!=='BACKUP_PASS') wp_die('Kein gültiges Komplettbackup.',409);
    $dir=realpath(pa_backup_dir());
    $name=basename((string)($m['filename']??''));
    $file=$dir ? realpath($dir.'/'.$name) : false;
    if (!$dir || !$file || !is_file($file) || strpos($file,rtrim($dir,DIRECTORY_SEPARATOR).DIRECTORY_SEPARATOR)!==0) wp_die('Backup-Datei fehlt.',404);
    $expected=strtolower((string)($m['sha256']??''));
    $actual=hash_file('sha256',$file);
    if (!preg_match('/^[a-f0-9]{64}$/',$expected) || !is_string($actual) || !hash_equals($expected,strtolower($actual))) wp_die('Backup-Prüfsumme stimmt nicht. Download blockiert.',409);
    while (ob_get_level()>0) ob_end_clean();
    @set_time_limit(0);
    nocache_headers();
    header('Content-Type: application/octet-stream');
    header('Content-Disposition: attachment; filename="'.rawurlencode($name).'"');
    $size=filesize($file); if ($size!==false) header('Content-Length: '.(string)$size);
    header('X-Content-Type-Options: nosniff');
    $fh=fopen($file,'rb'); if (!$fh) wp_die('Backup-Datei konnte nicht geöffnet werden.',500);
    while (!feof($fh)) { $chunk=fread($fh,8*1024*1024); if ($chunk===false) break; echo $chunk; flush(); if (connection_aborted()) break; }
    fclose($fh); exit;
});
