<?php
if (!defined('ABSPATH')) { exit; }
/** Additive read-only visual preview. Does not create an independent SEO decision. */
final class Wassertechnik_Seo81_Preview {
    private const PAGE = 'wassertechnik-seo81-preview';
    private const HOST = 'wasser.oliver-beil.de';
    public static function boot():void {
        add_action('admin_menu',[self::class,'menu'],40);
        add_action('admin_post_wassertechnik_dfs_w38_81_paid',['Wassertechnik_PaidResearch','paid81']);
        add_action('admin_post_wassertechnik_dfs_w38_81_export',['Wassertechnik_PaidResearch','export81']);
    }
    public static function menu():void {
        add_submenu_page('wassertechnik-kategorie','81 neue SEO-Kandidaten','81 neue SEO-Kandidaten','manage_options',self::PAGE,[self::class,'screen']);
    }
    public static function payload():array {
        if (strtolower((string)wp_parse_url(home_url('/'),PHP_URL_HOST)) !== self::HOST) {
            throw new RuntimeException('Nur auf der gebundenen Wassertechnik-Testwebsite erlaubt.');
        }
        $file=dirname(__DIR__).'/assets/wassertechnik-w28-seo-handoff.json';
        return Wassertechnik_W30_Seo_Handoff::read($file);
    }
    public static function screen():void {
        if (!current_user_can('manage_options')) wp_die('Administratorrechte erforderlich.');
        echo '<div class="wrap"><h1>81 neue Produktkandidaten: SEO-Vorschau</h1>';
        echo '<p>Die 81 Keywords werden zuerst kostenlos geprüft. Erst nach ausdrücklicher Kostenfreigabe wird ausschließlich der neue 81er-Sammelauftrag an DataForSEO übergeben. Keine automatische Seitenanlage.</p>';
        try {
            $data=self::payload();
            echo '<p><strong>Eingelesen:</strong> '.(int)$data['anzahl'].' Produkte, '.(int)$data['rubriken'].' Artikelrubriken. <strong>SEO-Status:</strong> NICHT GEMESSEN. 0 neue Freigaben.</p>';
            echo '<table class="widefat striped"><thead><tr><th>Produkt</th><th>Hauptbereich</th><th>SEO</th></tr></thead><tbody>';
            foreach ($data['produkte'] as $row) {
                echo '<tr><td>'.esc_html((string)$row['produktname']).'</td><td>'.esc_html((string)$row['geplanter_hauptbereich']).'</td><td>offen</td></tr>';
            }
            echo '</tbody></table>';
        } catch (Throwable $e) {
            echo '<p><strong>GESPERRT:</strong> '.esc_html($e->getMessage()).'</p>';
        }
        Wassertechnik_PaidResearch::panel81();
        echo '</div>';
    }
}
