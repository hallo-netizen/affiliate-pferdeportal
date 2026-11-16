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
        if(!current_user_can('manage_options'))wp_die('Administratorrechte erforderlich.');
        echo '<div class="wrap"><h1>Wassertechnik: 81 neue Produktkandidaten – SEO</h1>';
        echo '<p>Einmaliger Rechercheauftrag im bestehenden Plugin. Gemessene Suchdaten sind <strong>noch keine Freigabe</strong> für zusätzliche WordPress-Produktseiten oder Inhaltskategorien.</p>';
        try {
            $data=self::payload();
            $report=Wassertechnik_PaidResearch::read81();
            $phase=(string)$report['state'];
            echo '<p><strong>Fachplan:</strong> '.(int)$data['anzahl'].' Produkte, '.(int)$data['rubriken'].' produktbezogene Artikelrubriken. <strong>Recherche:</strong> '.esc_html($phase).'. <strong>SEO-Owner-Freigabe:</strong> 0 von 81.</p>';
            if(!empty($report['skipped_steps'])){
                echo '<p><strong>Unvollständige Anbieterergebnisse:</strong> '.count($report['skipped_steps']).' Schritte; fehlende Zahlen bleiben unbekannt. Keine automatische Wiederholung.</p>';
            }
            echo '<table class="widefat striped"><thead><tr><th>Produkt</th><th>Hauptbereich</th><th>Suchvolumen</th><th>Suchabsicht</th><th>SEO-Schwierigkeit</th><th>Seitenfreigabe</th></tr></thead><tbody>';
            foreach($data['produkte'] as $row){
                $id=(string)$row['register_id'];
                $measured=$report['by_owner'][$id]??null;
                $volume=$measured['search_volume']??null;
                $intent=$measured['search_intent']??null;
                $difficulty=$measured['organic_keyword_difficulty']??null;
                $volumeText=$volume===null?'nicht gemessen':(string)$volume;
                $intentText=$intent===null||$intent===''?'nicht gemessen':(string)$intent;
                $difficultyText=$difficulty===null?'nicht gemessen':(string)$difficulty;
                // W29 previously identified two concrete product-subtype intent overlaps.
                // Merely show the single historical comparison; do not decide twice.
                $note=in_array($id,['W14-017','W14-077'],true)
                    ? ' – bestehende Produktunterart: Suchabsicht noch abgrenzen' : '';
                echo '<tr><td>'.esc_html((string)$row['produktname'].$note).'</td><td>'.
                    esc_html((string)$row['geplanter_hauptbereich']).'</td><td>'.
                    esc_html($volumeText).'</td><td>'.
                    esc_html($intentText).'</td><td>'.
                    esc_html($difficultyText).'</td><td>nicht freigegeben</td></tr>';
            }
            echo '</tbody></table>';
        }catch(Throwable $e){
            echo '<p><strong>GESPERRT:</strong> '.esc_html($e->getMessage()).'</p>';
        }
        Wassertechnik_PaidResearch::panel81();
        echo '</div>';
    }
}
