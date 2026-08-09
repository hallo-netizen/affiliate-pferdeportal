<?php
/**
 * V1.50.408 – gruppierte Relevanssi-Live-Suche des Portal-Headers.
 * Relevanssi bleibt die Suchmaschine; dieses Template veraendert nur Abfrage-Scope
 * und Darstellung des bereits vorhandenen Live-AJAX-Pfads.
 */
if (!defined('ABSPATH')) { exit; }
global $wp_query;
if (class_exists('Pferde_Template_Kit') && method_exists('Pferde_Template_Kit', 'render_grouped_live_search_v150408')) {
    Pferde_Template_Kit::render_grouped_live_search_v150408($wp_query);
}
