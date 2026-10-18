<?php
/**
 * Plugin Name: Hobby Depot Template Kit Update 1.50.690
 * Description: Einmaliger Rollout des abgenommenen Detail-Level-Layouts aus 1.50.689 auf die gesamte gleiche Seitenebene.
 * Version: 1.0.0
 * Author: OpenAI
 */
if (!defined('ABSPATH')) { exit; }

function hd690_fail($msg) {
    wp_die('<h1>Update nicht ausgefuehrt</h1><p>'.esc_html($msg).'</p><p>Das bestehende Template Kit wurde nicht umgestellt.</p>');
}

function hd690_write_atomic($path, $content) {
    $dir = dirname($path);
    if (!is_dir($dir) || !is_writable($dir)) { return false; }
    $tmp = $path . '.hd690.tmp';
    if (file_put_contents($tmp, $content, LOCK_EX) === false) { return false; }
    @chmod($tmp, file_exists($path) ? (fileperms($path) & 0777) : 0644);
    if (!@rename($tmp, $path)) { @unlink($tmp); return false; }
    return true;
}

function hd690_apply_update() {
    if (!current_user_can('activate_plugins')) { hd690_fail('Keine Berechtigung.'); }

    $root = WP_PLUGIN_DIR . '/affiliate-portal-template-kit';
    $main_path = $root . '/pferde-template-kit.php';
    $profile_old = $root . '/includes/class-hobby-depot-profile-v150689.php';
    $profile_new = $root . '/includes/class-hobby-depot-profile-v150690.php';
    $front_old = $root . '/templates/hobby-depot-front-v150689.php';
    $front_new = $root . '/templates/hobby-depot-front-v150690.php';
    $content_old = $root . '/templates/hobby-depot-content-v150689.php';
    $content_new = $root . '/templates/hobby-depot-content-v150690.php';

    foreach ([$main_path,$profile_old,$front_old,$content_old] as $p) {
        if (!is_file($p) || !is_readable($p)) { hd690_fail('Erwartete 1.50.689-Datei fehlt: ' . basename($p)); }
    }

    $main = file_get_contents($main_path);
    $profile = file_get_contents($profile_old);
    $front = file_get_contents($front_old);
    $content = file_get_contents($content_old);
    if ($main === false || $profile === false || $front === false || $content === false) { hd690_fail('Quelldateien konnten nicht gelesen werden.'); }

    $checks = [
        [strpos($main, 'Version: 1.50.689') !== false, 'Main ist nicht exakt 1.50.689.'],
        [strpos($main, 'Hobby_Depot_Profile_V150689') !== false, 'Aktive Profilklasse V150689 fehlt.'],
        [strpos($profile, 'final class Hobby_Depot_Profile_V150689') !== false, 'Profil V150689 fehlt.'],
        [strpos($profile, "const RELEASE = '1.50.689';") !== false, 'Release 1.50.689 im Profil fehlt.'],
        [strpos($profile, "private static function render_category_level_body_v150687") !== false, 'Detail-Body-Funktion fehlt.'],
        [strpos($profile, "if (\$slug_v150689 === 'kettenhemdflechten') {") !== false, 'Abgenommener 1.50.689-Pilotzweig fehlt.'],
        [strpos($profile, 'hd-catlevel-banner-first-v150689') !== false, 'Banner-first-Pilot fehlt.'],
        [strpos($profile, 'hd-catlevel-grid-all-v150689') !== false, 'Geschlossener Kategorienblock aus 1.50.689 fehlt.'],
        [strpos($profile, 'render_category_level_post_previews_v150687($page, 4)') !== false, 'Vierer-Beitragsvorschau aus 1.50.689 fehlt.'],
        [strpos($front, 'Hobby_Depot_Profile_V150689') !== false, 'Fronttemplate V150689 passt nicht.'],
        [strpos($content, 'Hobby_Depot_Profile_V150689') !== false, 'Contenttemplate V150689 passt nicht.'],
    ];
    foreach ($checks as $c) { if (!$c[0]) { hd690_fail($c[1]); } }

    $profile690 = str_replace(
        ['final class Hobby_Depot_Profile_V150689',"const RELEASE = '1.50.689';",'/templates/hobby-depot-front-v150689.php','/templates/hobby-depot-content-v150689.php'],
        ['final class Hobby_Depot_Profile_V150690',"const RELEASE = '1.50.690';",'/templates/hobby-depot-front-v150690.php','/templates/hobby-depot-content-v150690.php'],
        $profile
    );

    $old_prefix = <<<'PHP'
        // V1.50.689 - Kettenhemd-Pilot: Banner direkt nach Intro; Kategorien geschlossen; Produkte danach; Beitraege danach.
        $slug_v150689 = sanitize_title((string) $page->post_name);
        if ($slug_v150689 === 'kettenhemdflechten') {
PHP;
    $new_prefix = <<<'PHP'
        // V1.50.690 - abgenommener Detail-Level-Standard fuer die gesamte gleiche Seitenebene:
        // Banner direkt nach Intro; Kategorien geschlossen; Produkte danach; bis zu 4 Beitraege danach.
        if ($page instanceof WP_Post) {
PHP;
    $profile690 = str_replace($old_prefix, $new_prefix, $profile690, $rollout_count);
    if ($rollout_count !== 1) { hd690_fail('Pilotzweig konnte nicht eindeutig auf die gesamte Detail-Seitenebene ausgerollt werden.'); }

    $profile690 = str_replace(
        ['hd-catlevel-banner-first-v150689','hd-catlevel-topics-all-v150689','hd-catlevel-grid-all-v150689'],
        ['hd-catlevel-banner-first-v150690','hd-catlevel-topics-all-v150690','hd-catlevel-grid-all-v150690'],
        $profile690
    );

    if (strpos($profile690, "if (\$slug_v150689 === 'kettenhemdflechten') {") !== false) {
        hd690_fail('Alter Kettenhemd-Sonderzweig ist nach Rollout noch aktiv.');
    }

    $front690 = str_replace('Hobby_Depot_Profile_V150689', 'Hobby_Depot_Profile_V150690', $front);
    $content690 = str_replace('Hobby_Depot_Profile_V150689', 'Hobby_Depot_Profile_V150690', $content);

    $main690 = str_replace(
        ['Version: 1.50.689',"const VERSION = '1.50.689';",'class-hobby-depot-profile-v150689.php','Hobby_Depot_Profile_V150689'],
        ['Version: 1.50.690',"const VERSION = '1.50.690';",'class-hobby-depot-profile-v150690.php','Hobby_Depot_Profile_V150690'],
        $main
    );

    if (
        strpos($main690, 'Version: 1.50.690') === false ||
        strpos($main690, 'Hobby_Depot_Profile_V150690') === false ||
        strpos($profile690, 'hd-catlevel-banner-first-v150690') === false ||
        strpos($profile690, 'hd-catlevel-grid-all-v150690') === false ||
        strpos($profile690, 'render_category_level_post_previews_v150687($page, 4)') === false
    ) {
        hd690_fail('Neue Release-/Layoutkette konnte nicht eindeutig hergestellt werden.');
    }

    $backup = WP_CONTENT_DIR . '/hd-template-kit-backups/1.50.689-' . gmdate('Ymd-His');
    if (!wp_mkdir_p($backup)) { hd690_fail('Backup-Verzeichnis konnte nicht erstellt werden.'); }
    foreach ([$main_path,$profile_old,$front_old,$content_old] as $p) {
        if (!@copy($p, $backup . '/' . basename($p))) { hd690_fail('Sicherungsdatei konnte nicht geschrieben werden: ' . basename($p)); }
    }

    if (!hd690_write_atomic($profile_new, $profile690)) { hd690_fail('Profil V150690 konnte nicht geschrieben werden.'); }
    if (!hd690_write_atomic($front_new, $front690)) { hd690_fail('Fronttemplate V150690 konnte nicht geschrieben werden.'); }
    if (!hd690_write_atomic($content_new, $content690)) { hd690_fail('Contenttemplate V150690 konnte nicht geschrieben werden.'); }
    if (!hd690_write_atomic($main_path, $main690)) { hd690_fail('Main konnte nicht auf V150690 umgestellt werden.'); }

    $read_main = file_get_contents($main_path);
    $read_profile = file_get_contents($profile_new);
    if (
        $read_main === false || $read_profile === false ||
        strpos($read_main, 'Version: 1.50.690') === false ||
        strpos($read_main, 'Hobby_Depot_Profile_V150690') === false ||
        strpos($read_profile, 'hd-catlevel-banner-first-v150690') === false ||
        strpos($read_profile, 'hd-catlevel-grid-all-v150690') === false ||
        strpos($read_profile, "if (\$slug_v150689 === 'kettenhemdflechten') {") !== false
    ) {
        @copy($backup . '/' . basename($main_path), $main_path);
        hd690_fail('Readback fehlgeschlagen. Main wurde auf 1.50.689 zurueckgestellt.');
    }

    update_option('hd_template_kit_update_150690_result', [
        'ok'=>1,
        'at'=>gmdate('c'),
        'backup'=>$backup,
        'scope'=>'all page-based detail hubs using render_category_level_body_v150687'
    ], false);
    deactivate_plugins(plugin_basename(__FILE__), true);
}
register_activation_hook(__FILE__, 'hd690_apply_update');
