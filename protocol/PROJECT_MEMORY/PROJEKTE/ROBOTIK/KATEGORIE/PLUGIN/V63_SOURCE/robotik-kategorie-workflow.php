<?php
/**
 * Plugin Name: Robotik Kategorie-Workflow (Neutralstart)
 * Description: Eigenstaendige Robotik-Planungsoberflaeche mit Produktseiten- und Inhaltskategorie-Pruefung; mit kontrolliertem Erstimport fuer Entwurfsseiten und Produktkategorien.
 * Version: 0.4.9
 * Requires at least: 6.4
 * Requires PHP: 8.1
 * Text Domain: robotik-kategorie-workflow
 */
if (!defined('ABSPATH')) { exit; }
require_once __DIR__ . '/includes/class-robotik-inventory.php';
require_once __DIR__ . '/includes/class-robotik-first-import.php';
require_once __DIR__ . '/includes/class-robotik-publish.php';
require_once __DIR__ . '/includes/class-robotik-dataforseo.php';
require_once __DIR__ . '/includes/class-robotik-gesamtvorschau.php';
require_once __DIR__ . '/includes/class-robotik-v63-delta.php';

final class Robotik_Kategorie_Workflow {
    private const OPTION = 'robotik_kategorie_entwurf_v1'; // Bestehende Entwuerfe bei Update erhalten.
    public const VERSION = '0.4.9';

    public static function boot(): void {
        add_action('admin_menu', [self::class, 'menu']);
        add_action('admin_post_robotik_inventory_export', [self::class, 'export_inventory']);
        Robotik_First_Import::boot();
        Robotik_Publish::boot();
        Robotik_DataForSEO::boot();
        Robotik_Kategorie_Gesamtvorschau::boot();
        Robotik_V63_Delta::boot();
    }

    public static function menu(): void {
        add_menu_page('Robotik Kategorie', 'Robotik Kategorie', 'manage_options', 'robotik-kategorie', [self::class, 'screen'], 'dashicons-networking', 58);
    }

    public static function validate($plan): array {
        if (!is_array($plan) || ($plan['project'] ?? null) !== 'robotik' || !isset($plan['nodes']) || !is_array($plan['nodes']) || !array_is_list($plan['nodes'])) {
            return ['Projekt muss "robotik" sein und "nodes" eine Liste.'];
        }
        $errors = []; $by_id = []; $seen_slug = []; $global_category_slugs = [];
        $phase = ($plan['phase'] ?? 'draft');
        if (!in_array($phase, ['draft', 'final'], true)) { $errors[] = 'phase ungueltig (draft oder final).'; }
        $kinds = ['core' => ['page', 'content_category'], 'editorial' => ['magazine_category'], 'directory' => ['listing_category']];
        foreach ($plan['nodes'] as $i => $n) {
            if (!is_array($n)) { $errors[] = 'Knoten ' . ($i + 1) . ': kein Objekt.'; continue; }
            $id = $n['id'] ?? null;
            $pillar = $n['pillar'] ?? null;
            $kind = $n['kind'] ?? null;
            $title = $n['title'] ?? null;
            $slug = $n['slug'] ?? null;
            $parent = $n['parent'] ?? null;
            if (!is_string($id) || !preg_match('/^[a-z0-9_-]{2,80}$/', $id) || isset($by_id[$id])) {
                $errors[] = 'Knoten ' . ($i + 1) . ': ID fehlt, ungueltig oder doppelt.'; continue;
            }
            $by_id[$id] = $n;
            if (!is_string($pillar) || !isset($kinds[$pillar]) || !in_array($kind, $kinds[$pillar], true)) { $errors[] = $id . ': Saeule oder Typ ungueltig.'; }
            if (!is_string($title) || trim($title) === '' || strlen($title) > 160) { $errors[] = $id . ': Titel ungueltig.'; }
            if (!is_string($slug) || !preg_match('/^[a-z0-9]+(?:-[a-z0-9]+)*$/', $slug)) { $errors[] = $id . ': Slug ungueltig.'; }
            if ($parent !== null && (!is_string($parent) || $parent === $id)) { $errors[] = $id . ': Eltern-ID ungueltig.'; }
            // Das letzte WordPress-Seitenziel muss ein bestimmter Robotertyp sein.
            // Alte Entwuerfe bleiben lesbar; neue Produktrollen sind Pflicht fuer CORE-Seiten.
            if ($pillar === 'core' && $kind === 'page') {
                if (!in_array($n['role'] ?? '', ['group', 'product'], true)) {
                    $errors[] = $id . ': Seite braucht role=group oder role=product.';
                }
            }
            if ($pillar === 'core' && $kind === 'content_category') {
                if (array_key_exists('role', $n)) { $errors[] = $id . ': Inhaltskategorie darf keine Seitenrolle haben.'; }
                // Ein Inhalts-Leaf benoetigt grobe Stoffrichtungen, nicht vorgegebene Artikeltitel.
                if (isset($n['topic_directions'])) {
                    if (!is_array($n['topic_directions']) || !array_is_list($n['topic_directions'])) {
                        $errors[] = $id . ': topic_directions muss eine Liste sein.';
                    } else {
                        if ($phase === 'final' && count($n['topic_directions']) < 3) { $errors[] = $id . ': mindestens 3 verschiedene Stoffrichtungen erforderlich.'; }
                        $uniq = [];
                        foreach ($n['topic_directions'] as $direction) {
                            if (!is_string($direction) || trim($direction) === '' || strlen($direction) > 250) {
                                $errors[] = $id . ': Stoffrichtung ungueltig.'; continue;
                            }
                            $k = function_exists('mb_strtolower') ? mb_strtolower(trim($direction), 'UTF-8') : strtolower(trim($direction));
                            if (isset($uniq[$k])) { $errors[] = $id . ': doppelte Stoffrichtung.'; }
                            $uniq[$k] = true;
                        }
                    }
                } elseif ($phase === 'final') { $errors[] = $id . ': final fehlen 3 Stoffrichtungen.'; }
                if (is_string($slug)) {
                    if (isset($global_category_slugs[$slug])) { $errors[] = $id . ': global doppelter WordPress-Kategorie-Slug (' . $slug . ').'; }
                    $global_category_slugs[$slug] = true;
                }
            }
            $key = (string)$pillar . '|' . (string)$kind . '|' . (string)$parent . '|' . (string)$slug;
            if (isset($seen_slug[$key])) { $errors[] = $id . ': doppelter Name/Slug im gleichen Zweig.'; }
            $seen_slug[$key] = true;
        }
        foreach ($by_id as $id => $n) {
            $parent = $n['parent'] ?? null;
            if ($parent === null) {
                if (($n['kind'] ?? '') === 'content_category') { $errors[] = $id . ': Inhaltskategorie braucht eine Elternseite.'; }
                if (($n['kind'] ?? '') === 'page' && ($n['role'] ?? '') === 'product') { $errors[] = $id . ': Produktseite darf keine Hauptwelt sein.'; }
                continue;
            }
            if (!isset($by_id[$parent])) { $errors[] = $id . ': Elternknoten fehlt.'; continue; }
            $p = $by_id[$parent];
            if (($p['pillar'] ?? '') !== ($n['pillar'] ?? '')) { $errors[] = $id . ': Saeulen duerfen nicht vermischt werden.'; }
            if (($n['kind'] ?? '') === 'page' && ($p['kind'] ?? '') !== 'page') { $errors[] = $id . ': Seite braucht eine Elternseite.'; }
            if (($n['kind'] ?? '') === 'content_category' && ($p['kind'] ?? '') !== 'page') { $errors[] = $id . ': Inhaltskategorie braucht eine Elternseite.'; }
            if (($n['kind'] ?? '') === 'content_category' && ($p['role'] ?? '') !== 'product') { $errors[] = $id . ': Inhaltskategorie darf nur unter einer konkreten Produktseite liegen.'; }
            if (($n['kind'] ?? '') === 'page' && ($p['role'] ?? '') === 'product') { $errors[] = $id . ': Produktseite darf keine weitere Unterseite haben.'; }
            if (($n['kind'] ?? '') === 'magazine_category' && ($p['kind'] ?? '') !== 'magazine_category') { $errors[] = $id . ': Magazin-Elternknoten ungueltig.'; }
            if (($n['kind'] ?? '') === 'listing_category' && ($p['kind'] ?? '') !== 'listing_category') { $errors[] = $id . ': Anzeigen-Elternknoten ungueltig.'; }
            $visited = [$id => true]; $walk = $parent;
            while (isset($by_id[$walk])) {
                if (isset($visited[$walk])) { $errors[] = $id . ': Kreis in der Hierarchie.'; break; }
                $visited[$walk] = true; $walk = $by_id[$walk]['parent'] ?? null;
                if ($walk === null) { break; }
            }
        }
        return array_values(array_unique($errors));
    }

    public static function export_inventory(): void {
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.'); }
        check_admin_referer('robotik_inventory_export');
        $result = Robotik_Kategorie_Inventory::collect();
        nocache_headers();
        header('Content-Type: application/json; charset=UTF-8');
        header('Content-Disposition: attachment; filename="robotik-gesamtbestand-' . gmdate('Ymd-His') . '.json"');
        echo wp_json_encode($result, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT);
        exit;
    }

    public static function screen(): void {
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.'); }
        $saved = get_option(self::OPTION, ['project' => 'robotik', 'nodes' => []]);
        $notice = ''; $errors = [];
        $value = wp_json_encode($saved, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
        $inventory = null;
        if (isset($_POST['robotik_inventory_check'])) {
            check_admin_referer('robotik_inventory_scan');
            $inventory = Robotik_Kategorie_Inventory::collect();
        }
        if (isset($_POST['robotik_check'])) {
            check_admin_referer('robotik_kategorie_plan');
            $value = isset($_POST['robotik_json']) && is_string($_POST['robotik_json']) ? wp_unslash($_POST['robotik_json']) : '';
            $plan = json_decode($value, true);
            $errors = self::validate($plan);
            if (!$errors) {
                $notice = 'Plan ist formal geprueft. Keine WordPress-Seite, Kategorie oder Anzeige wurde angelegt.';
                if ($_POST['robotik_check'] === 'save') {
                    update_option(self::OPTION, $plan, false);
                    $notice = 'Entwurf gespeichert. Keine Seiten, Kategorien oder Anzeigen wurden angelegt.';
                }
            }
        }
        echo '<div class="wrap"><h1>Robotik – Kategorie</h1>';
        echo '<p>Neutralstart: drei getrennte Saeulen, keine Vorbelegung, kein automatischer Import oder Hintergrundlauf.</p>';
        echo '<p><strong>CORE-Regel:</strong> Seiten mit role=group / role=product. Nur die letzte Seite hat role=product. Darunter nur flache Inhaltskategorien und spaeter zugeordnete Beitraege. topic_directions speichert freiwillige grobe Stoffrichtungen (keine Artikeltitel).</p>'; 
        echo '<ul><li><strong>Hauptkategorien:</strong> Seiten und darunter Inhaltskategorien.</li>';
        echo '<li><strong>Magazin / Journal:</strong> eigene Themen und Ratgeber.</li>';
        echo '<li><strong>Anzeigenmarkt:</strong> Anbieter und Inserate; spaeter ueber HivePress.</li></ul>';
        if ($notice) { echo '<div class="notice notice-success"><p>' . esc_html($notice) . '</p></div>'; }
        if ($errors) { echo '<div class="notice notice-error"><p>' . esc_html(implode(' | ', $errors)) . '</p></div>'; }
        echo '<h2>Bestandsaufnahme</h2><p>Ein Klick liest vorhandene WordPress-Seiten, Beitraege, Kategorien und – falls installiert – HivePress-Daten. Kein Upload von Einzeldateien.</p>';
        echo '<form method="post">'; wp_nonce_field('robotik_inventory_scan');
        echo '<button class="button button-primary" type="submit" name="robotik_inventory_check" value="1">Bestand pruefen</button></form>';
        echo '<form method="post" action="' . esc_url(admin_url('admin-post.php')) . '">'; wp_nonce_field('robotik_inventory_export');
        echo '<input type="hidden" name="action" value="robotik_inventory_export">';
        echo '<p><button class="button" type="submit">EINEN Gesamtbericht (JSON) herunterladen</button></p></form>';
        if ($inventory !== null) { Robotik_Kategorie_Inventory::show($inventory); }
        echo '<hr><h2>Kategorie-Entwurf</h2><p>Erst gemeinsam den Baum entwickeln, danach den Entwurf pruefen und speichern. Dies ist kein Live-Importer.</p>';
        echo '<form method="post">'; wp_nonce_field('robotik_kategorie_plan');
        echo '<textarea name="robotik_json" rows="17" style="width:100%;font-family:monospace" spellcheck="false">' . esc_textarea($value) . '</textarea>';
        echo '<p><button class="button" type="submit" name="robotik_check" value="check">Nur pruefen</button> ';
        echo '<button class="button button-primary" type="submit" name="robotik_check" value="save">Geprueften Entwurf speichern</button></p>';
        echo '</form><p><strong>Schreibgrenze:</strong> Nur ein WordPress-Entwurf wird gespeichert. Keine Inhalte, Kategorien, Menues oder HivePress-Eintraege werden veraendert.</p></div>';
    }
}
Robotik_Kategorie_Workflow::boot();