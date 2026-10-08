<?php
if (!defined('ABSPATH')) { exit; }

/**
 * Zentrales, provideruebergreifendes Partner-/Einnahmen-Cockpit.
 *
 * Provider-Kennzahlen werden niemals geschaetzt. Sie stammen ausschliesslich
 * aus verifizierten Provider-Reports/APIs. Die vorhandenen lokalen Redirect-
 * Klickzaehler werden separat als Portal-Klicks ausgewiesen und nie mit
 * Provider-Klicks, Umsatz, Bestellungen oder Provisionen vermischt.
 */
final class PPAR_Partner_Analytics_Admin {
    const OPTION_REPORT_CACHE = 'ppar_partner_analytics_report_cache_v1';
    const CONTRACT_VERSION = '1.0';
    const CAMPAIGN_POST_TYPE = 'ap_campaign';

    private static $booted = false;

    public static function bootstrap() {
        if (self::$booted) { return; }
        self::$booted = true;
        if (!((function_exists('wp_doing_ajax') && wp_doing_ajax()) || (defined('DOING_AJAX') && DOING_AJAX))) {
            add_action('admin_menu', array(__CLASS__, 'register_menu'), 999);
        }
        add_action('ppar_partner_analytics_ingest', array(__CLASS__, 'ingest_report'), 10, 2);
    }

    public static function register_menu() {
        if (!function_exists('add_submenu_page')) { return; }
        add_submenu_page(
            null,
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

    private static function campaign_provider_key($campaign) {
        $network = sanitize_key((string)($campaign['network'] ?? 'manual'));
        if ($network === 'awin' && absint($campaign['advertiser_id'] ?? 0) === PPAR_Affiliate_Source_Plan::OTTO_AWIN_ADVERTISER_ID) {
            return 'otto';
        }
        $key = $network === 'manual' ? 'direct' : $network;
        $key = apply_filters('ppar_partner_analytics_campaign_provider_key', $key, $campaign, self::CONTRACT_VERSION);
        return sanitize_key((string)$key);
    }


    /**
     * Separate portal-side click evidence from the existing signed redirect path.
     * This is deliberately admin-only and reads existing campaign meta; it never
     * changes frontend selection and is never presented as provider reporting.
     */
    private static function portal_clicks_by_provider($range) {
        $range = self::normalize_range($range);
        $providers = self::provider_defaults();
        $out = array();
        foreach ($providers as $key=>$unused) { $out[sanitize_key((string)$key)] = 0; }
        $days = $range === 'today' ? 1 : ($range === '7' ? 7 : ($range === '30' ? 30 : 0));
        $today_ts = function_exists('current_time') ? current_time('timestamp') : time();
        $today_midnight = strtotime((function_exists('wp_date') ? wp_date('Y-m-d', $today_ts) : date('Y-m-d', $today_ts)) . ' 00:00:00');
        if ($today_midnight === false) { $today_midnight = $today_ts - ($today_ts % 86400); }
        $min_ts = $days > 0 ? strtotime('-' . max(0,$days-1) . ' days', $today_midnight) : 0;
        foreach (self::campaign_posts() as $post) {
            $post_id = absint(is_object($post) ? ($post->ID ?? 0) : $post);
            if ($post_id <= 0) { continue; }
            $campaign = self::campaign_data($post_id);
            if (!$campaign) { continue; }
            $provider = self::campaign_provider_key($campaign);
            if ($provider === '') { continue; }
            if (!array_key_exists($provider,$out)) { $out[$provider] = 0; }
            if ($days <= 0) {
                $out[$provider] += max(0,(int)get_post_meta($post_id,'ppar_click_total',true));
                continue;
            }
            $daily = get_post_meta($post_id,'ppar_click_daily',true);
            if (!is_array($daily)) { continue; }
            foreach ($daily as $date=>$count) {
                $ts = strtotime((string)$date);
                if ($ts !== false && $ts >= $min_ts) { $out[$provider] += max(0,(int)$count); }
            }
        }
        return $out;
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
            $details = array();
            foreach ((array)($row['details'] ?? array()) as $detail) {
                if (!is_array($detail)) { continue; }
                $details[] = array(
                    'label'=>sanitize_text_field((string)($detail['label'] ?? 'Originalzeile')),
                    'external_id'=>sanitize_text_field((string)($detail['external_id'] ?? '')),
                    'clicks'=>array_key_exists('clicks',$detail) && is_numeric($detail['clicks']) ? max(0,(int)$detail['clicks']) : null,
                    'orders'=>array_key_exists('orders',$detail) && is_numeric($detail['orders']) ? max(0,(int)$detail['orders']) : null,
                    'sales'=>array_key_exists('sales',$detail) && is_numeric($detail['sales']) ? (float)$detail['sales'] : null,
                    'commission'=>array_key_exists('commission',$detail) && is_numeric($detail['commission']) ? (float)$detail['commission'] : null,
                    'conversion'=>array_key_exists('conversion',$detail) && is_numeric($detail['conversion']) ? (float)$detail['conversion'] : null,
                    'currency'=>preg_match('/^[A-Z]{3}$/',strtoupper((string)($detail['currency'] ?? 'EUR'))) ? strtoupper((string)$detail['currency']) : 'EUR',
                );
            }
            $periods[$period] = array(
                'clicks' => array_key_exists('clicks', $row) && is_numeric($row['clicks']) ? max(0, (int)$row['clicks']) : null,
                'orders' => array_key_exists('orders', $row) && is_numeric($row['orders']) ? max(0, (int)$row['orders']) : null,
                'sales' => array_key_exists('sales', $row) && is_numeric($row['sales']) ? max(0, (float)$row['sales']) : null,
                'commission' => array_key_exists('commission', $row) && is_numeric($row['commission']) ? (float)$row['commission'] : null,
                'conversion' => array_key_exists('conversion', $row) && is_numeric($row['conversion']) ? (float)$row['conversion'] : null,
                'details' => $details,
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
            'conversion' => array_key_exists('conversion', $period) ? $period['conversion'] : null,
            'currency' => (string)($entry['currency'] ?? 'EUR'),
            'source' => (string)($entry['source'] ?? ''),
            'updated_at' => absint($entry['updated_at'] ?? 0),
            'details' => isset($period['details']) && is_array($period['details']) ? $period['details'] : array(),
        );
    }

    private static function na($value, $format = 'number', $currency = 'EUR') {
        if ($value === null) { return '<span class="description">nicht verfügbar</span>'; }
        if ($format === 'percent') {
            return esc_html(number_format_i18n((float)$value, 2) . ' %');
        }
        if ($format === 'money') {
            $currency = strtoupper((string)$currency);
            if (!preg_match('/^[A-Z]{3}$/', $currency)) { $currency = 'EUR'; }
            return esc_html(number_format_i18n((float)$value, 2) . ' ' . $currency);
        }
        return esc_html(number_format_i18n((float)$value, 0));
    }

    public static function render_page() {
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.'); }
        $range = self::normalize_range($_GET['range'] ?? '30');
        $providers = self::provider_defaults();
        $rows = array();
        $portal_clicks = self::portal_clicks_by_provider($range);
        $refresh_state = get_option('ppar_partner_analytics_refresh_state_v1', array());
        $refresh_state = is_array($refresh_state) ? $refresh_state : array();
        foreach ($providers as $key => $provider) {
            $report = self::provider_report($key, $range);
            $has_report = $report['updated_at'] > 0 && (
                $report['clicks'] !== null || $report['orders'] !== null ||
                $report['sales'] !== null || $report['commission'] !== null ||
                $report['conversion'] !== null
            );
            $rows[$key] = array('provider'=>$provider,'report'=>$report,'has_report'=>$has_report,'portal_clicks'=>max(0,(int)($portal_clicks[$key] ?? 0)),'refresh'=>is_array($refresh_state[$key] ?? null)?$refresh_state[$key]:array());
        }
        // Die sichtbare KISS-Seite ist die kanonische Navigation. Zeitraumlinks
        // duerfen nicht auf den historischen, aus dem Menue entfernten Stats-Slug springen.
        $base = admin_url('admin.php?page=affiliate-portal-kiss-partners');
        ?>
        <div class="wrap" style="max-width:1240px">
            <h1>Partner &amp; Einnahmen</h1>
            <p><strong>Zwei getrennte Klickquellen:</strong> Portal-Klicks stammen ausschließlich aus dem vorhandenen eigenen Redirect-Zähler. Provider-Klicks, Verkäufe/Leads, Umsatz, Provision und Conversion erscheinen nur aus verifizierten Originalreports/APIs. Beide Quellen werden niemals vermischt oder gegeneinander hochgerechnet.</p>
            <?php if (!empty($_GET['ppar_stats_refreshed'])) : ?><div class="notice notice-success inline"><p>Originalreports wurden neu abgefragt. Der Datenstand unten ist der direkte Provider-/Adapterstand.</p></div><?php endif; ?>
            <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>" style="margin:12px 0 18px">
                <input type="hidden" name="action" value="ppar_partner_analytics_refresh_now">
                <?php wp_nonce_field('ppar_partner_analytics_refresh_now'); ?>
                <?php submit_button('Originalzahlen jetzt aktualisieren','secondary','submit',false); ?>
            </form>
            <p class="subsubsub" style="float:none;margin:12px 0 18px">
                <?php foreach (array('today'=>'Heute','7'=>'7 Tage','30'=>'30 Tage','all'=>'Gesamt') as $value=>$label) : ?>
                    <a href="<?php echo esc_url(add_query_arg('range',$value,$base)); ?>" <?php echo $range===$value?'style="font-weight:700"':''; ?>><?php echo esc_html($label); ?></a><?php echo $value!=='all'?' &nbsp;|&nbsp; ':''; ?>
                <?php endforeach; ?>
            </p>
            <h2><?php echo esc_html(self::range_label($range)); ?></h2>
            <table class="widefat striped"><thead><tr><th>Partner / Quelle</th><th>Rolle</th><th>Portal-Klicks</th><th>Provider-Klicks</th><th>Verkäufe/Leads</th><th>Umsatz</th><th>Provision</th><th>Conversion</th><th>Datenstand</th></tr></thead><tbody>
            <?php foreach ($rows as $row) : $p=$row['provider']; $r=$row['report']; $state=$row['refresh']; $portal_click_count=max(0,(int)($row['portal_clicks']??0)); ?>
                <tr>
                    <td><strong><?php echo esc_html((string)$p['label']); ?></strong><?php if (($p['label']??'')==='OTTO') : ?><br><span class="description">über Awin-Advertiserreport</span><?php endif; ?></td>
                    <td><?php echo esc_html((string)$p['type']); ?></td>
                    <td><strong><?php echo esc_html(number_format_i18n($portal_click_count,0)); ?></strong><br><span class="description">Pferdeatelier-Redirect</span></td>
                    <?php $multi_original = !empty($r['details']) && count((array)$r['details']) > 1; ?>
                    <td><?php echo $multi_original ? '<span class="description">siehe Originalzeilen</span>' : self::na($r['clicks']); ?></td>
                    <td><?php echo $multi_original ? '<span class="description">siehe Originalzeilen</span>' : self::na($r['orders']); ?></td>
                    <td><?php echo $multi_original ? '<span class="description">siehe Originalzeilen</span>' : self::na($r['sales'],'money',$r['currency']); ?></td>
                    <td><?php echo $multi_original ? '<span class="description">siehe Originalzeilen</span>' : self::na($r['commission'],'money',$r['currency']); ?></td>
                    <td><?php echo $multi_original ? '<span class="description">siehe Originalzeilen</span>' : self::na($r['conversion'],'percent'); ?></td>
                    <td><?php if ($r['updated_at']>0) { echo esc_html(wp_date('d.m.Y H:i',$r['updated_at'])); if ($r['source']!=='') { echo '<br><span class="description">'.esc_html($r['source']).'</span>'; } } else { echo '<span class="description">noch kein Report</span>'; } if (!empty($state['checked_at'])) { echo '<br><span class="description">Prüfung '.esc_html(wp_date('d.m.Y H:i',absint($state['checked_at']))).': '.esc_html((string)($state['status']??'')).'</span>'; } if (!empty($state['message'])) { echo '<br><span class="description">'.esc_html((string)$state['message']).'</span>'; } ?></td>
                </tr>
                <?php if (!empty($r['details'])) : foreach ((array)$r['details'] as $detail) : ?>
                <tr>
                    <td style="padding-left:28px">↳ <?php echo esc_html((string)($detail['label'] ?? 'Originalzeile')); ?><?php if (!empty($detail['external_id'])) : ?><br><span class="description">ID <?php echo esc_html((string)$detail['external_id']); ?></span><?php endif; ?></td>
                    <td><span class="description">Provider-Originalzeile</span></td>
                    <td><span class="description">—</span></td>
                    <td><?php echo self::na($detail['clicks'] ?? null); ?></td>
                    <td><?php echo self::na($detail['orders'] ?? null); ?></td>
                    <td><?php echo self::na($detail['sales'] ?? null,'money',(string)($detail['currency'] ?? $r['currency'])); ?></td>
                    <td><?php echo self::na($detail['commission'] ?? null,'money',(string)($detail['currency'] ?? $r['currency'])); ?></td>
                    <td><?php echo self::na($detail['conversion'] ?? null,'percent'); ?></td>
                    <td><span class="description">nicht lokal summiert</span></td>
                </tr>
                <?php endforeach; endif; ?>
            <?php endforeach; ?>
            </tbody></table>
            <p class="description" style="margin-top:12px">Wichtig: Portal-Klicks sind das vorhandene interne Klicktracking und deshalb für alle tatsächlich geklickten Partner sichtbar. Providerwerte bleiben davon strikt getrennt; fehlende Providerwerte werden nicht als Null oder durch Portal-Klicks ersetzt.</p>
        </div>
        <?php
    }
}
