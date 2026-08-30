<?php
if (!defined('ABSPATH')) { exit; }

/**
 * Zentrales, provideruebergreifendes Partner-/Einnahmen-Cockpit.
 *
 * Es werden niemals Umsatz, Bestellungen oder Provisionen geschaetzt. Lokale
 * Klicks stammen aus der bestehenden Affiliate-Zentrale; externe Kennzahlen
 * duerfen nur ueber den normierten Report-Adapter eingespeist werden.
 */
final class PPAR_Partner_Analytics_Admin {
    const OPTION_REPORT_CACHE = 'ppar_partner_analytics_report_cache_v1';
    const CONTRACT_VERSION = '1.0';
    const CAMPAIGN_POST_TYPE = 'ap_campaign';
    const DEAL_CLICK_DAILY_OPTION = 'ppar_deal_click_daily_v1';

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

    private static function campaign_posts() {
        if (!function_exists('get_posts')) { return array(); }
        return get_posts(array(
            'post_type' => self::CAMPAIGN_POST_TYPE,
            'post_status' => array('publish','draft','private'),
            'numberposts' => -1,
            'orderby' => 'ID',
            'order' => 'ASC',
            'suppress_filters' => true,
        ));
    }

    private static function campaign_data($post_id) {
        $data = get_post_meta(absint($post_id), 'ppar_campaign_data', true);
        return is_array($data) ? $data : array();
    }

    private static function text_contains($haystack, $needle) {
        $haystack = (string)$haystack;
        $needle = (string)$needle;
        if ($haystack === '' || $needle === '') { return false; }
        if (function_exists('mb_stripos')) { return mb_stripos($haystack, $needle, 0, 'UTF-8') !== false; }
        return stripos($haystack, $needle) !== false;
    }

    private static function campaign_provider_key($campaign) {
        $network = sanitize_key((string)($campaign['network'] ?? 'manual'));
        if ($network === 'awin') {
            $identity = implode(' ', array_filter(array_map('strval', array(
                $campaign['name'] ?? '',
                $campaign['title'] ?? '',
                $campaign['partner_name'] ?? '',
                $campaign['merchant_name'] ?? '',
                $campaign['advertiser_name'] ?? '',
                $campaign['programme_name'] ?? '',
            ))));
            if (self::text_contains($identity, 'otto')) { return 'otto'; }
        }
        $key = $network === 'manual' ? 'direct' : $network;
        $key = apply_filters('ppar_partner_analytics_campaign_provider_key', $key, $campaign, self::CONTRACT_VERSION);
        return sanitize_key((string)$key);
    }

    private static function local_clicks_for_post($post_id, $range) {
        $post_id = absint($post_id);
        if ($post_id <= 0) { return 0; }
        if ($range === 'all') { return absint(get_post_meta($post_id, 'ppar_click_total', true)); }
        $daily = get_post_meta($post_id, 'ppar_click_daily', true);
        if (!is_array($daily)) { return 0; }
        $days = $range === 'today' ? 1 : max(1, absint($range));
        $now = current_time('timestamp');
        $min = strtotime('-' . max(0, $days - 1) . ' days', $now);
        $sum = 0;
        foreach ($daily as $date => $count) {
            $ts = strtotime((string)$date);
            if ($ts !== false && $ts >= $min) { $sum += absint($count); }
        }
        return $sum;
    }

    private static function local_deal_clicks_by_provider($range) {
        $stored = get_option(self::DEAL_CLICK_DAILY_OPTION, array());
        $stored = is_array($stored) ? $stored : array();
        $out = array();
        $days = $range === 'today' ? 1 : ($range === 'all' ? 0 : max(1, absint($range)));
        $min = $days > 0 ? strtotime('-' . max(0, $days - 1) . ' days', current_time('timestamp')) : 0;
        foreach ($stored as $provider => $record) {
            $provider = sanitize_key((string)$provider);
            if ($provider === '' || !is_array($record)) { continue; }
            if ($range === 'all') {
                $out[$provider] = absint($record['total'] ?? 0);
                continue;
            }
            $sum = 0;
            foreach ((array)($record['daily'] ?? array()) as $date => $count) {
                $ts = strtotime((string)$date);
                if ($ts !== false && $ts >= $min) { $sum += absint($count); }
            }
            $out[$provider] = $sum;
        }
        return $out;
    }

    private static function local_clicks_by_provider($range) {
        $totals = array();
        foreach (self::campaign_posts() as $post) {
            if (!is_object($post) || empty($post->ID)) { continue; }
            $campaign = self::campaign_data($post->ID);
            if (!$campaign) { continue; }
            $provider = self::campaign_provider_key($campaign);
            if ($provider === '') { $provider = 'direct'; }
            if (!isset($totals[$provider])) { $totals[$provider] = 0; }
            $totals[$provider] += self::local_clicks_for_post($post->ID, $range);
        }
        foreach (self::local_deal_clicks_by_provider($range) as $provider => $count) {
            if (!isset($totals[$provider])) { $totals[$provider] = 0; }
            $totals[$provider] += absint($count);
        }
        return $totals;
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

    private static function na($value, $format = 'number') {
        if ($value === null) { return '<span class="description">nicht verfügbar</span>'; }
        if ($format === 'money') { return esc_html(number_format_i18n((float)$value, 2) . ' €'); }
        return esc_html(number_format_i18n((float)$value, 0));
    }

    public static function render_page() {
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.'); }
        $range = self::normalize_range($_GET['range'] ?? '30');
        $providers = self::provider_defaults();
        $local = self::local_clicks_by_provider($range);
        $rows = array();
        $totals = array('local_clicks'=>0,'orders'=>0,'sales'=>0.0,'commission'=>0.0);
        $best = array('provider'=>'','commission'=>null);
        foreach ($providers as $key => $provider) {
            $report = self::provider_report($key, $range);
            $local_clicks = absint($local[$key] ?? 0);
            $conversion = null;
            if ($report['orders'] !== null && $report['clicks'] !== null && (int)$report['clicks'] > 0) {
                $conversion = ((float)$report['orders'] / (float)$report['clicks']) * 100;
            }
            $rows[$key] = array('provider'=>$provider,'local_clicks'=>$local_clicks,'report'=>$report,'conversion'=>$conversion);
            $totals['local_clicks'] += $local_clicks;
            if ($report['orders'] !== null) { $totals['orders'] += (int)$report['orders']; }
            if ($report['sales'] !== null) { $totals['sales'] += (float)$report['sales']; }
            if ($report['commission'] !== null) {
                $totals['commission'] += (float)$report['commission'];
                if ($best['commission'] === null || (float)$report['commission'] > (float)$best['commission']) {
                    $best = array('provider'=>(string)$provider['label'],'commission'=>(float)$report['commission']);
                }
            }
        }
        $base = admin_url('admin.php?page=affiliate-portal-stats');
        ?>
        <div class="wrap" style="max-width:1240px">
            <h1>Partner &amp; Einnahmen</h1>
            <p>Eine zentrale Sicht auf alle Affiliate-Quellen. Fehlende Netzwerkdaten werden nicht geschätzt.</p>
            <p class="subsubsub" style="float:none;margin:12px 0 18px">
                <?php foreach (array('today'=>'Heute','7'=>'7 Tage','30'=>'30 Tage','all'=>'Gesamt') as $value=>$label) : ?>
                    <a href="<?php echo esc_url(add_query_arg('range',$value,$base)); ?>" <?php echo $range===$value?'style="font-weight:700"':''; ?>><?php echo esc_html($label); ?></a><?php echo $value!=='all'?' &nbsp;|&nbsp; ':''; ?>
                <?php endforeach; ?>
            </p>
            <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:14px;margin:0 0 18px">
                <div class="postbox" style="padding:16px"><strong>Lokale Klicks</strong><div style="font-size:28px;margin-top:6px"><?php echo esc_html(number_format_i18n($totals['local_clicks'])); ?></div></div>
                <div class="postbox" style="padding:16px"><strong>Verkäufe/Leads gemeldet</strong><div style="font-size:28px;margin-top:6px"><?php echo esc_html(number_format_i18n($totals['orders'])); ?></div></div>
                <div class="postbox" style="padding:16px"><strong>Provision gemeldet</strong><div style="font-size:28px;margin-top:6px"><?php echo esc_html(number_format_i18n($totals['commission'],2)); ?> €</div></div>
                <div class="postbox" style="padding:16px"><strong>Bester Partner</strong><div style="font-size:20px;margin-top:8px"><?php echo esc_html($best['provider'] !== '' ? $best['provider'] : 'noch keine Daten'); ?></div></div>
            </div>
            <h2><?php echo esc_html(self::range_label($range)); ?></h2>
            <table class="widefat striped"><thead><tr><th>Partner / Quelle</th><th>Rolle</th><th>Lokale Klicks</th><th>Partner-Klicks</th><th>Verkäufe/Leads</th><th>Umsatz</th><th>Provision</th><th>Conversion</th><th>Datenstand</th></tr></thead><tbody>
            <?php foreach ($rows as $row) : $p=$row['provider']; $r=$row['report']; ?>
                <tr>
                    <td><strong><?php echo esc_html((string)$p['label']); ?></strong><?php if (($p['label']??'')==='OTTO') : ?><br><span class="description">technisch über Awin möglich</span><?php endif; ?></td>
                    <td><?php echo esc_html((string)$p['type']); ?></td>
                    <td><?php echo esc_html(number_format_i18n($row['local_clicks'])); ?></td>
                    <td><?php echo self::na($r['clicks']); ?></td>
                    <td><?php echo self::na($r['orders']); ?></td>
                    <td><?php echo self::na($r['sales'],'money'); ?></td>
                    <td><?php echo self::na($r['commission'],'money'); ?></td>
                    <td><?php echo $row['conversion']===null?'<span class="description">nicht verfügbar</span>':esc_html(number_format_i18n($row['conversion'],2).' %'); ?></td>
                    <td><?php if ($r['updated_at']>0) { echo esc_html(wp_date('d.m.Y H:i',$r['updated_at'])); if ($r['source']!=='') { echo '<br><span class="description">'.esc_html($r['source']).'</span>'; } } else { echo '<span class="description">noch kein Report</span>'; } ?></td>
                </tr>
            <?php endforeach; ?>
            </tbody></table>
            <p class="description" style="margin-top:12px">Verkäufe, Umsatz und Provision erscheinen erst, wenn der jeweilige Provider einen verifizierten Report über den zentralen Adapter liefert.</p>
        </div>
        <?php
    }
}
