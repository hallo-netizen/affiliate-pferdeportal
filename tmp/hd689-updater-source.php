<?php
/**
 * Plugin Name: Hobby Depot Template Kit Update 1.50.689
 * Description: Einmaliger, hart gepruefter Pilot-Updater fuer Kettenhemd flechten. Aktualisiert ausschliesslich das vorhandene Affiliate Portal Template Kit 1.50.688 auf 1.50.689.
 * Version: 1.0.0
 * Author: OpenAI
 */
if (!defined('ABSPATH')) { exit; }

function hd689_fail($msg) {
    wp_die('<h1>Update nicht ausgefuehrt</h1><p>'.esc_html($msg).'</p><p>Das bestehende Template Kit wurde nicht umgestellt.</p>');
}

function hd689_write_atomic($path, $content) {
    $dir = dirname($path);
    if (!is_dir($dir) || !is_writable($dir)) { return false; }
    $tmp = $path . '.hd689.tmp';
    if (file_put_contents($tmp, $content, LOCK_EX) === false) { return false; }
    @chmod($tmp, file_exists($path) ? (fileperms($path) & 0777) : 0644);
    if (!@rename($tmp, $path)) { @unlink($tmp); return false; }
    return true;
}

function hd689_apply_update() {
    if (!current_user_can('activate_plugins')) { hd689_fail('Keine Berechtigung.'); }

    $root = WP_PLUGIN_DIR . '/affiliate-portal-template-kit';
    $main_path = $root . '/pferde-template-kit.php';
    $profile_old = $root . '/includes/class-hobby-depot-profile-v150688.php';
    $profile_new = $root . '/includes/class-hobby-depot-profile-v150689.php';
    $front_old = $root . '/templates/hobby-depot-front-v150688.php';
    $front_new = $root . '/templates/hobby-depot-front-v150689.php';
    $content_old = $root . '/templates/hobby-depot-content-v150688.php';
    $content_new = $root . '/templates/hobby-depot-content-v150689.php';

    foreach ([$main_path,$profile_old,$front_old,$content_old] as $p) {
        if (!is_file($p) || !is_readable($p)) { hd689_fail('Erwartete 1.50.688-Datei fehlt: ' . basename($p)); }
    }

    $main = file_get_contents($main_path);
    $profile = file_get_contents($profile_old);
    $front = file_get_contents($front_old);
    $content = file_get_contents($content_old);
    if ($main === false || $profile === false || $front === false || $content === false) { hd689_fail('Quelldateien konnten nicht gelesen werden.'); }

    $checks = [
        [strpos($main, 'Version: 1.50.688') !== false, 'Main ist nicht exakt 1.50.688.'],
        [strpos($main, 'Hobby_Depot_Profile_V150688') !== false, 'Aktive Profilklasse V150688 fehlt.'],
        [strpos($profile, 'final class Hobby_Depot_Profile_V150688') !== false, 'Profil V150688 fehlt.'],
        [strpos($profile, "const RELEASE = '1.50.688';") !== false, 'Release 1.50.688 im Profil fehlt.'],
        [strpos($profile, "private static function render_category_level_body_v150687") !== false, 'Detail-Body-Funktion fehlt.'],
        [strpos($profile, 'Kettenhemd<br><span class="hd-catlevel-title-second">flechten</span>') !== false, 'Erwarteter Kettenhemd-H1 aus 1.50.688 fehlt.'],
        [strpos($profile, "Rund ums Kettenhemd") !== false, 'Erwartete Kettenhemd-Zwischenueberschrift fehlt.'],
        [strpos($profile, "<h2>Empfehlungen</h2>") !== false, 'Erwartete Empfehlungen-Ueberschrift fehlt.'],
        [strpos($front, 'Hobby_Depot_Profile_V150688') !== false, 'Fronttemplate V150688 passt nicht.'],
        [strpos($content, 'Hobby_Depot_Profile_V150688') !== false, 'Contenttemplate V150688 passt nicht.'],
    ];
    foreach ($checks as $c) { if (!$c[0]) { hd689_fail($c[1]); } }

    $profile689 = str_replace(
        ['final class Hobby_Depot_Profile_V150688',"const RELEASE = '1.50.688';","/templates/hobby-depot-front-v150688.php","/templates/hobby-depot-content-v150688.php"],
        ['final class Hobby_Depot_Profile_V150689',"const RELEASE = '1.50.689';","/templates/hobby-depot-front-v150689.php","/templates/hobby-depot-content-v150689.php"],
        $profile
    );

    $old_h1 = 'Kettenhemd<br><span class="hd-catlevel-title-second">flechten</span>';
    $new_h1 = '<span class="hd-kettenhemd-title-v150689" style="display:inline-block;white-space:nowrap;font-size:clamp(28px,8.5vw,50px);letter-spacing:-.02em">Kettenhemd&nbsp;flechten</span>';
    $profile689 = str_replace($old_h1, $new_h1, $profile689, $h1_count);
    if ($h1_count !== 1) { hd689_fail('H1 konnte nicht eindeutig auf einzeilig umgestellt werden.'); }

    $function_pos = strpos($profile689, 'private static function render_category_level_body_v150687');
    if ($function_pos === false) { hd689_fail('Detail-Body-Funktion nicht gefunden.'); }
    $marker = "if (!\$page instanceof WP_Post) { return ''; }";
    $marker_pos = strpos($profile689, $marker, $function_pos);
    if ($marker_pos === false) { hd689_fail('Einstieg der Detail-Body-Funktion nicht gefunden.'); }
    $insert_pos = $marker_pos + strlen($marker);
    $branch = <<<'PHP'

        // V1.50.689 - Kettenhemd-Pilot: Banner direkt nach Intro; Kategorien geschlossen; Produkte danach; Beitraege danach.
        $slug_v150689 = sanitize_title((string) $page->post_name);
        if ($slug_v150689 === 'kettenhemdflechten') {
            $terms = self::direct_category_children_for_page($page);
            $parts = self::integrated_affiliate_components('category', get_the_title($page));
            $out = '';

            $banner = self::inline_partner_banner($parts, 3);
            if ($banner !== '') {
                $out .= '<section class="hd-portal-section hd-catlevel-banner hd-catlevel-banner-first-v150689">'.$banner.'</section>';
            }

            if ($terms) {
                $out .= '<section class="hd-portal-section hd-catlevel-topics hd-catlevel-topics-all-v150689"><header><h2>'.esc_html(self::category_level_topics_heading_v150688($page)).'</h2></header>';
                $out .= self::render_category_level_term_cards_v150687($terms, $page, $world_slug, 'hd-catlevel-grid-all-v150689');
                $out .= '</section>';
            }

            $out .= self::render_category_level_product_row_v150687($parts);
            $out .= self::render_category_level_post_previews_v150687($page, 4);
            $out .= self::render_rental_for('category');
            return $out;
        }
PHP;
    $profile689 = substr($profile689, 0, $insert_pos) . $branch . substr($profile689, $insert_pos);

    $front689 = str_replace('Hobby_Depot_Profile_V150688', 'Hobby_Depot_Profile_V150689', $front);
    $content689 = str_replace('Hobby_Depot_Profile_V150688', 'Hobby_Depot_Profile_V150689', $content);

    $main689 = str_replace(
        ['Version: 1.50.688',"const VERSION = '1.50.688';",'class-hobby-depot-profile-v150688.php','Hobby_Depot_Profile_V150688'],
        ['Version: 1.50.689',"const VERSION = '1.50.689';",'class-hobby-depot-profile-v150689.php','Hobby_Depot_Profile_V150689'],
        $main
    );

    if (strpos($main689, 'Version: 1.50.689') === false || strpos($main689, 'Hobby_Depot_Profile_V150689') === false) {
        hd689_fail('Neue Main-Releasekette konnte nicht eindeutig hergestellt werden.');
    }

    $backup = WP_CONTENT_DIR . '/hd-template-kit-backups/1.50.688-' . gmdate('Ymd-His');
    if (!wp_mkdir_p($backup)) { hd689_fail('Backup-Verzeichnis konnte nicht erstellt werden.'); }
    foreach ([$main_path,$profile_old,$front_old,$content_old] as $p) {
        if (!@copy($p, $backup . '/' . basename($p))) { hd689_fail('Sicherungsdatei konnte nicht geschrieben werden: ' . basename($p)); }
    }

    if (!hd689_write_atomic($profile_new, $profile689)) { hd689_fail('Profil V150689 konnte nicht geschrieben werden.'); }
    if (!hd689_write_atomic($front_new, $front689)) { hd689_fail('Fronttemplate V150689 konnte nicht geschrieben werden.'); }
    if (!hd689_write_atomic($content_new, $content689)) { hd689_fail('Contenttemplate V150689 konnte nicht geschrieben werden.'); }
    if (!hd689_write_atomic($main_path, $main689)) { hd689_fail('Main konnte nicht auf V150689 umgestellt werden.'); }

    $read_main = file_get_contents($main_path);
    $read_profile = file_get_contents($profile_new);
    if (
        $read_main === false || $read_profile === false ||
        strpos($read_main, 'Version: 1.50.689') === false ||
        strpos($read_main, 'Hobby_Depot_Profile_V150689') === false ||
        strpos($read_profile, "Kettenhemd&nbsp;flechten") === false ||
        strpos($read_profile, "hd-catlevel-banner-first-v150689") === false ||
        strpos($read_profile, "hd-catlevel-grid-all-v150689") === false
    ) {
        @copy($backup . '/' . basename($main_path), $main_path);
        hd689_fail('Readback fehlgeschlagen. Main wurde auf 1.50.688 zurueckgestellt.');
    }

    update_option('hd_template_kit_update_150689_result', ['ok'=>1,'at'=>gmdate('c'),'backup'=>$backup], false);
    deactivate_plugins(plugin_basename(__FILE__), true);
}
register_activation_hook(__FILE__, 'hd689_apply_update');
