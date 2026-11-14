<?php
/**
 * Plugin Name: Texterstellung
 * Description: Prüfkandidat: Originalmodule PSTE und PSERC ohne fachliche Änderungen, kein Live-Release.
 * Version: 0.0.0-source-proof
 * Requires PHP: 8.1
 */
if (!defined('ABSPATH')) { return; }
// WordPress may load plugins in any order. Check the active list before loading originals.
$oldPlugins = function_exists('get_option') ? (array)get_option('active_plugins', []) : [];
if (function_exists('get_site_option')) {
    $oldPlugins = array_merge($oldPlugins, array_keys((array)get_site_option('active_sitewide_plugins', [])));
}
$oldActive = false;
foreach ($oldPlugins as $oldPlugin) {
    $name = basename((string)$oldPlugin);
    if ($name === 'portal-seo-topic-engine.php' || $name === 'portal-seo-editorial-plan-compiler.php') {
        $oldActive = true;
        break;
    }
}
if ($oldActive || defined('PSTE_VERSION') || defined('PSERC_VERSION')) {
    add_action('admin_notices', static function () {
        echo '<div class="notice notice-error"><p>Texterstellung: alte PSTE-/PSERC-Plugins sind aktiv; kein zweiter Schreibpfad wird gestartet.</p></div>';
    });
    return;
}
require_once __DIR__ . '/unchanged/pste/portal-seo-topic-engine.php';
require_once __DIR__ . '/unchanged/pserc/portal-seo-editorial-plan-compiler.php';
register_activation_hook(__FILE__, ['PSTE_Plugin', 'activate']);
add_action('admin_menu', static function () {
    global $menu;
    if (!is_array($menu)) { return; }
    foreach ($menu as &$entry) {
        if (is_array($entry) && ($entry[2] ?? '') === 'portal-seo-topic-engine') {
            $entry[0] = 'Texterstellung';
            break;
        }
    }
    unset($entry);
}, 1001);
