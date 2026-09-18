<?php
if (!defined('ABSPATH')) { exit; }

/**
 * Zentrales, provideruebergreifendes Partner-/Einnahmen-Cockpit.
 *
 * Die Backend-Statistik zeigt ausschliesslich Originaldaten, die der jeweilige
 * Partner/Provider ueber einen verifizierten Report-/API-Adapter liefert.
 * Eigene Klick-, Bestell-, Umsatz- oder Provisionserhebung ist hier verboten.
 */
final class PPAR_Partner_Analytics_Admin {
    const OPTION_REPORT_CACHE = 'ppar_partner_analytics_report_cache_v1';
    const CONTRACT_VERSION = '1.0';
    const CAMPAIGN_POST_TYPE = 'ap_campaign';

    private static $booted = false;

    public static function bootstrap() {
        if (self::$booted) { return; }
        self::$booted = true;
        add_action('admin_menu', array(__CLASS__, 'register_menu'), 999);
        add_action('ppar_partner_analytics_ingest', array(__CLASS__, 'ingest_report'), 10, 2);
    }

    public static function register_menu() {
        if (!function_exists('remove_submenu_page') || !function_exists('add_submenu_page')) { return; }
        remove_submenu_page('affiliate-portal-zentrale', 'affiliate-portal-stats');
        add_submenu_page(
            'affiliate-portal-zentrale',
            'Partner & Einnahmen',
            'Partner & Einnahmen',
            'manage_options',
            'affiliate-portal-stats',
            array(__CLASS__, 'render_page')
        );
    }

    private static function provider_defaults() {
        $providers = array(
            'amazon' => array('label'=>'Amazon','type'=>'Produktquelle','state'=>'prepared','source_network'=>'amazon'),
            'otto' => array('label'=>'OTTO','type'=>'Produktquelle','state'=>'prepared','source_network'=>'awin'),
            'kelkoo' => array('label'=>'Kelkoo','type'=>'Produkt- & Dealquelle','state'=>'prepared','source_network'=>'kelkoo'),
            'idealo' => array('label'=>'idealo','type'=>'Preisvergleich / Produktquelle','state'=>'active','source_network'=>'idealo'),
            'ebay' => array('label'=>'eBay','type'=>'Produktquelle','state'=>'active','source_network'=>'ebay'),
            'awin' => array('label'=>'Awin','type'=>'Banner-/Partnernetzwerk','state'=>'active','source_network'=>'awin'),
            'adcell' => array('label'=>'ADCELL','type'=>'Banner-/Partnernetzwerk','state'=>'active','source_network'=>'adcell'),
            'digistore24' => array('label'=>'Digistore24','type'=>'Banner-/Partnernetzwerk','state'=>'active','source_network'=>'digistore24'),
            'direct' => array('label'=>'Direktpartner','type'=>'Direktpartner','state'=>'active','source_network'=>'direct'),
        );
        $filtered = apply_filters('ppar_partner_analytics_providers', $providers, self::CONTRACT_VERSION);
        return is_array($filtered) ? $filtered : $providers;
    }

    private static function normalize_range($raw) {
        $raw = sanitize_key((string)$raw);
        return in_array($raw, array('today','7','30','all'), true) ? $raw : '30';
    }

    private static function range_label($range) {
        if ($range === 'today') { return 'Heute'; }
        if ($range === '7') { return '7 Tage'; }
        if ($range === 'all') { return 'Gesamt'; }
        return '30 Tage';
    }

    private static function report_cache() {
        $cache = get_option(self::OPTION_REPORT_CACHE, array());
        return is_array($cache) ? $cache : array();
    }

    public static function ingest_report($provider, $report) {
        $provider = sanitize_key((string)$provider);
        if ($provider === '' || !is_array($report)) { return false; }
        $periods = array();
        foreach (array('today','7','30','all') as $period) {
            $row = isset($report['periods'][$period]) && is_array($report['periods'][$period]) ? $report['periods'][$period] : array();
            if (!$row) { continue; }
            $periods[$period] = array(
                'clicks' => array_key_exists('clicks', $row) && is_numeric($row['clicks']) ? max(0, (int)$row['clicks']) : null,
                'orders' => array_key_exists('orders', $row) && is_numeric($row['orders']) ? max(0, (int)$row['orders']) : null,
                'sales' => array_key_exists('sales', $row) && is_numeric($row['sales']) ? max(0, (float)$row['sales']) : null,
                'commission' => array_key_exists('commission', $row) && is_numeric($row['commission']) ? (float)$row['commission'] : null,
            );
        }
        $currency = strtoupper((string)($report['currency'] ?? 'EUR'));
        if (!preg_match('/^[A-Z]{3}$/', $currency)) { $currency = 'EUR'; }
        $cache = self::report_cache();
        $cache[$provider] = array(
            'source' => sanitize_text_field((string)($report['source'] ?? 'provider_api')),
            'currency' => $currency,
            'updated_at' => absint($report['updated_at'] ?? time()),
            'periods' => $periods,
        );
        update_option(self::OPTION_REPORT_CACHE, $cache, false);
        return true;
    }

    private static function provider_report($provider, $range) {
        $cache = self::report_cache();
        $provider = sanitize_key((string)$provider);
        $entry = isset($cache[$provider]) && is_array($cache[$provider]) ? $cache[$provider] : array();
        $period = isset($entry['periods'][$range]) && is_array($entry['periods'][$range]) ? $entry['periods'][$range] : array();
        return array(
            'clicks' => array_key_exists('clicks', $period) ? $period['clicks'] : null,
            'orders' => array_key_exists('orders', $period) ? $period['orders'] : null,
            'sales' => array_key_exists('sales', $period) ? $period['sales'] : null,
            'commission' => array_key_exists('commission', $period) ? $period['commission'] : null,
            'currency' => (string)($entry['currency'] ?? 'EUR'),
            'source' => (string)($entry['source'] ?? ''),
            'updated_at' => absint($entry['updated_at'] ?? 0),
        );
    }

    private static function na($value, $format = 'number', $currency = '') {
        if ($value === null) { return '<span class="description">nicht verfügbar</span>'; }
        if ($format === 'money') {
            $currency = strtoupper((string) $currency);
            if (!preg_match('/^[A-Z]{3}$/', $currency)) { $currency = ''; }
            return esc_html(number_format_i18n((float)$value, 2) . ($currency !== '' ? ' ' . $currency : ''));
        }
        return esc_html(number_format_i18n((float)$value, 0));
    }

    public static function render_page() {
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.'); }
        $range = self::normalize_range($_GET['range'] ?? '30');
        $providers = self::provider_defaults();
        $rows = array();
        $reports_available = 0;
        $reports_missing = 0;
        foreach ($providers as $key => $provider) {
            $report = self::provider_report($key, $range);
            $has_report = $report['updated_at'] > 0 && $report['source'] !== '';
            if ($has_report) { $reports_available++; } else { $reports_missing++; }
            $conversion = null;
            if ($report['orders'] !== null && $report['clicks'] !== null && (int)$report['clicks'] > 0) {
                $conversion = ((float)$report['orders'] / (float)$report['clicks']) * 100;
            }
            $rows[$key] = array('provider'=>$provider,'report'=>$report,'conversion'=>$conversion,'has_report'=>$has_report);
        }
        $base = admin_url('admin.php?page=affiliate-portal-stats');
        ?>
        <div class="wrap" style="max-width:1240px">
            <h1>Partner &amp; Einnahmen</h1>
            <p><strong>Originaldaten:</strong> Diese Statistik verwendet ausschließlich verifizierte Reports/API-Daten der jeweiligen Partner bzw. Provider. Eigene WordPress-Klickzahlen oder andere lokale Ersatzmessungen fließen nicht ein.</p>
            <p class="subsubsub" style="float:none;margin:12px 0 18px">
                <?php foreach (array('today'=>'Heute','7'=>'7 Tage','30'=>'30 Tage','all'=>'Gesamt') as $value=>$label) : ?>
                    <a href="<?php echo esc_url(add_query_arg('range',$value,$base)); ?>" <?php echo $range===$value?'style="font-weight:700"':''; ?>><?php echo esc_html($label); ?></a><?php echo $value!=='all'?' &nbsp;|&nbsp; ':''; ?>
                <?php endforeach; ?>
            </p>
            <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:14px;margin:0 0 18px">
                <div class="postbox" style="padding:16px"><strong>Providerreports verfügbar</strong><div style="font-size:28px;margin-top:6px"><?php echo absint($reports_available); ?></div></div>
                <div class="postbox" style="padding:16px"><strong>Providerreports fehlen</strong><div style="font-size:28px;margin-top:6px"><?php echo absint($reports_missing); ?></div></div>
                <div class="postbox" style="padding:16px"><strong>Geldwerte</strong><div style="font-size:16px;margin-top:8px">je Provider in Originalwährung</div></div>
            </div>
            <h2><?php echo esc_html(self::range_label($range)); ?></h2>
            <table class="widefat striped"><thead><tr><th>Partner / Quelle</th><th>Rolle</th><th>Partner-Klicks</th><th>Verkäufe/Leads</th><th>Umsatz</th><th>Provision</th><th>Conversion</th><th>Datenstand / Quelle</th></tr></thead><tbody>
            <?php foreach ($rows as $row) : $p=$row['provider']; $r=$row['report']; ?>
                <tr>
                    <td><strong><?php echo esc_html((string)$p['label']); ?></strong><?php if (($p['label']??'')==='OTTO') : ?><br><span class="description">technisch über Awin möglich</span><?php endif; ?></td>
                    <td><?php echo esc_html((string)$p['type']); ?></td>
                    <td><?php echo self::na($r['clicks']); ?></td>
                    <td><?php echo self::na($r['orders']); ?></td>
                    <td><?php echo self::na($r['sales'],'money',$r['currency']); ?></td>
                    <td><?php echo self::na($r['commission'],'money',$r['currency']); ?></td>
                    <td><?php echo $row['conversion']===null?'<span class="description">nicht verfügbar</span>':esc_html(number_format_i18n($row['conversion'],2).' %'); ?></td>
                    <td><?php if ($row['has_report']) { echo esc_html(wp_date('d.m.Y H:i',$r['updated_at'])); echo '<br><span class="description">'.esc_html($r['source']).'</span>'; } else { echo '<span class="description">noch kein Originalreport</span>'; } ?></td>
                </tr>
            <?php endforeach; ?>
            </tbody></table>
            <p class="description" style="margin-top:12px">Fehlende Providerdaten bleiben „nicht verfügbar“. Es werden keine lokalen Ersatzwerte erzeugt und keine unterschiedlichen Währungen zu einer Gesamtsumme vermischt.</p>
        </div>
        <?php
    }

}
