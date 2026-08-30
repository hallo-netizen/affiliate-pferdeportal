<?php
if (!defined('ABSPATH')) { exit; }

/**
 * Provideruebergreifender Deal-Radar. Der erste oeffentliche Scope ist hart auf
 * Reithelme begrenzt. Er liest nur vorhandene Produktdaten und veraendert keinen
 * Provider-Worker. Insbesondere bleibt der eBay-Laufvertrag unangetastet.
 */
final class PPAR_Deal_Radar {
    const OPTION_SETTINGS = 'ppar_deal_radar_settings_v1';
    const OPTION_HISTORY = 'ppar_deal_radar_history_v1';
    const OPTION_STATE = 'ppar_deal_radar_state_v1';
    const OPTION_CLICK_DAILY = 'ppar_deal_click_daily_v1';
    const CRON_HOOK = 'ppar_deal_radar_hourly_v1';
    const CONTRACT_VERSION = '1.0';

    private static $booted = false;
    private static $rendered = false;

    public static function bootstrap() {
        if (self::$booted) { return; }
        self::$booted = true;
        add_action('admin_menu', array(__CLASS__, 'register_menu'), 998);
        add_action('admin_post_ppar_deal_radar_save', array(__CLASS__, 'handle_save'));
        add_action('init', array(__CLASS__, 'ensure_schedule'), 28);
        add_action(self::CRON_HOOK, array(__CLASS__, 'refresh'));
        add_filter('the_content', array(__CLASS__, 'filter_content'), 45);
        add_action('template_redirect', array(__CLASS__, 'handle_click'), -20);
    }

    private static function defaults() {
        return array(
            'enabled'=>true,
            'test_slug'=>'reithelme',
            'min_discount_pct'=>18.0,
            'min_saving_eur'=>15.0,
            'max_age_hours'=>36,
        );
    }

    private static function settings() {
        $saved = get_option(self::OPTION_SETTINGS, array());
        $saved = is_array($saved) ? $saved : array();
        $s = array_merge(self::defaults(), $saved);
        $s['enabled'] = !empty($s['enabled']);
        $s['test_slug'] = sanitize_title((string)($s['test_slug'] ?? 'reithelme')) ?: 'reithelme';
        $s['min_discount_pct'] = min(60, max(10, (float)($s['min_discount_pct'] ?? 18)));
        $s['min_saving_eur'] = min(500, max(5, (float)($s['min_saving_eur'] ?? 15)));
        $s['max_age_hours'] = min(72, max(6, absint($s['max_age_hours'] ?? 36)));
        return $s;
    }

    public static function register_menu() {
        add_submenu_page(
            'affiliate-portal-zentrale',
            'Produktquellen & Deals',
            'Produktquellen & Deals',
            'manage_options',
            'affiliate-portal-deals',
            array(__CLASS__, 'render_admin_page')
        );
    }

    public static function ensure_schedule() {
        if (!function_exists('wp_next_scheduled') || !function_exists('wp_schedule_event')) { return; }
        if (!wp_next_scheduled(self::CRON_HOOK)) {
            wp_schedule_event(time() + 15 * MINUTE_IN_SECONDS, 'hourly', self::CRON_HOOK);
        }
    }

    private static function table_name() {
        global $wpdb;
        return is_object($wpdb) ? $wpdb->prefix . 'ppar_sync_products' : '';
    }

    private static function table_exists() {
        global $wpdb;
        $table = self::table_name();
        if ($table === '' || !is_object($wpdb) || !method_exists($wpdb, 'get_var') || !method_exists($wpdb, 'prepare')) { return false; }
        return (string)$wpdb->get_var($wpdb->prepare('SHOW TABLES LIKE %s', $table)) === $table;
    }

    private static function normalize_text($value) {
        $value = wp_strip_all_tags((string)$value);
        if (function_exists('remove_accents')) { $value = remove_accents($value); }
        $value = strtolower($value);
        $value = preg_replace('/[^a-z0-9]+/', ' ', $value);
        return trim(preg_replace('/\s+/', ' ', (string)$value));
    }

    private static function is_reithelm_product($title) {
        $title = self::normalize_text($title);
        if ($title === '') { return false; }
        $positive = preg_match('/\b(?:reithelm|reithelme|reiterhelm|reiterhelme|reitsporthelm|reitschutzhelm)\b/', $title);
        if (!$positive) { return false; }
        foreach (array('tasche','helmtasche','uberzug','ueberzug','cover','halter','wandhalter','koffer','liner','polster','innenfutter','ersatz','ersatzteil','visier','zubehor','zubehoer','bezug') as $blocked) {
            if (preg_match('/\b'.preg_quote($blocked,'/').'\b/', $title)) { return false; }
        }
        return true;
    }

    private static function parse_price($raw) {
        $raw = html_entity_decode((string)$raw, ENT_QUOTES, 'UTF-8');
        $raw = preg_replace('/[^0-9,\.\-]/', '', $raw);
        if ($raw === '' || $raw === '-') { return 0.0; }
        $comma = strrpos($raw, ',');
        $dot = strrpos($raw, '.');
        if ($comma !== false && $dot !== false) {
            if ($comma > $dot) { $raw = str_replace('.', '', $raw); $raw = str_replace(',', '.', $raw); }
            else { $raw = str_replace(',', '', $raw); }
        } elseif ($comma !== false) {
            $raw = str_replace('.', '', $raw);
            $raw = str_replace(',', '.', $raw);
        }
        $value = (float)$raw;
        return $value > 0 && $value < 100000 ? round($value, 2) : 0.0;
    }

    private static function collect_gtins($value, $key = '', &$out = null, $depth = 0) {
        if ($out === null) { $out = array(); }
        if ($depth > 5) { return $out; }
        if (is_array($value)) {
            foreach ($value as $k=>$v) { self::collect_gtins($v, (string)$k, $out, $depth + 1); }
            return $out;
        }
        $key_norm = strtolower((string)$key);
        if (!preg_match('/(?:ean|gtin|upc|barcode)/', $key_norm)) { return $out; }
        foreach (preg_split('/[^0-9]+/', (string)$value) as $part) {
            $part = trim($part);
            if (in_array(strlen($part), array(8,12,13,14), true)) { $out['g:'.$part] = $part; }
        }
        return $out;
    }

    private static function provider_key($row) {
        $network = sanitize_key((string)($row['network'] ?? ''));
        if ($network === 'awin') {
            $identity = self::normalize_text((string)($row['programme_name'] ?? ''));
            if (preg_match('/\botto\b/', $identity)) { return 'otto'; }
            return '';
        }
        return in_array($network, array('idealo','amazon','kelkoo','ebay'), true) ? $network : '';
    }

    private static function candidate_rows() {
        if (!self::table_exists()) { return array(); }
        global $wpdb;
        $table = self::table_name();
        $s = self::settings();
        $min_seen = time() - absint($s['max_age_hours']) * HOUR_IN_SECONDS;
        $like = '%reithelm%';
        $sql = $wpdb->prepare(
            "SELECT id,network,external_key,programme_external_id,programme_name,title,image_url,tracking_url,destination_url,price,currency,brand,category,quality_status,payload,last_seen FROM {$table} WHERE quality_status IN ('pass','warn') AND last_seen>=%d AND (LOWER(title) LIKE %s OR LOWER(category) LIKE %s) ORDER BY last_seen DESC LIMIT 250",
            $min_seen, $like, $like
        );
        $rows = (array)$wpdb->get_results($sql, ARRAY_A);
        $out = array();
        foreach ($rows as $row) {
            if (!is_array($row) || !self::is_reithelm_product($row['title'] ?? '')) { continue; }
            $provider = self::provider_key($row);
            if ($provider === '') { continue; }
            $price = self::parse_price($row['price'] ?? '');
            if ($price <= 0) { continue; }
            $currency = strtoupper(trim((string)($row['currency'] ?? 'EUR')));
            if ($currency !== '' && $currency !== 'EUR') { continue; }
            $url = trim((string)($row['tracking_url'] ?? '')) ?: trim((string)($row['destination_url'] ?? ''));
            $image = trim((string)($row['image_url'] ?? ''));
            if (!wp_http_validate_url($url) || !wp_http_validate_url($image)) { continue; }
            $payload = json_decode((string)($row['payload'] ?? ''), true);
            $payload = is_array($payload) ? $payload : array();
            $gtins = array_values(self::collect_gtins($payload));
            sort($gtins, SORT_STRING);
            $offer_key = hash('sha256', $provider.'|'.(string)($row['external_key'] ?? '').'|'.$url);
            $out[] = array(
                'offer_key'=>$offer_key,
                'provider'=>$provider,
                'network'=>sanitize_key((string)($row['network'] ?? '')),
                'programme_name'=>sanitize_text_field((string)($row['programme_name'] ?? '')),
                'title'=>sanitize_text_field((string)($row['title'] ?? '')),
                'brand'=>sanitize_text_field((string)($row['brand'] ?? '')),
                'price'=>$price,
                'currency'=>'EUR',
                'image_url'=>esc_url_raw($image),
                'url'=>esc_url_raw($url),
                'gtins'=>$gtins,
                'last_seen'=>absint($row['last_seen'] ?? 0),
                'external_key'=>sanitize_text_field((string)($row['external_key'] ?? '')),
            );
        }
        return $out;
    }

    private static function median($values) {
        $values = array_values(array_filter(array_map('floatval', (array)$values), static function($v){ return $v > 0; }));
        if (!$values) { return 0.0; }
        sort($values, SORT_NUMERIC);
        $n = count($values); $mid = (int)floor($n/2);
        return $n % 2 ? (float)$values[$mid] : ((float)$values[$mid-1] + (float)$values[$mid]) / 2;
    }

    private static function history() {
        $h = get_option(self::OPTION_HISTORY, array());
        return is_array($h) ? $h : array();
    }

    private static function save_history($history) {
        update_option(self::OPTION_HISTORY, is_array($history) ? $history : array(), false);
    }

    private static function snapshot_candidates($candidates) {
        $history = self::history();
        $now = time();
        $seen = array();
        foreach ((array)$candidates as $candidate) {
            $key = (string)($candidate['offer_key'] ?? '');
            if ($key === '') { continue; }
            $seen[$key] = true;
            $entry = isset($history[$key]) && is_array($history[$key]) ? $history[$key] : array('samples'=>array(),'last_seen'=>0,'provider'=>'','title'=>'');
            $samples = is_array($entry['samples'] ?? null) ? $entry['samples'] : array();
            $last = $samples ? end($samples) : null;
            $last_at = is_array($last) ? absint($last['at'] ?? 0) : 0;
            $last_price = is_array($last) ? (float)($last['price'] ?? 0) : 0;
            if ($last_at === 0 || ($now - $last_at) >= 30 * MINUTE_IN_SECONDS || abs($last_price - (float)$candidate['price']) >= 0.01) {
                $samples[] = array('at'=>$now,'price'=>(float)$candidate['price']);
            }
            if (count($samples) > 48) { $samples = array_slice($samples, -48); }
            $history[$key] = array(
                'samples'=>$samples,
                'last_seen'=>$now,
                'provider'=>sanitize_key((string)$candidate['provider']),
                'title'=>sanitize_text_field((string)$candidate['title']),
            );
        }
        foreach ($history as $key=>$entry) {
            if (!isset($seen[$key]) && $now - absint($entry['last_seen'] ?? 0) > 60 * DAY_IN_SECONDS) { unset($history[$key]); }
        }
        self::save_history($history);
        return $history;
    }

    private static function history_reference($candidate, $history) {
        $key = (string)($candidate['offer_key'] ?? '');
        $samples = isset($history[$key]['samples']) && is_array($history[$key]['samples']) ? $history[$key]['samples'] : array();
        $current = (float)($candidate['price'] ?? 0);
        $prior = array(); $oldest = 0;
        foreach ($samples as $sample) {
            if (!is_array($sample)) { continue; }
            $at = absint($sample['at'] ?? 0); $price = (float)($sample['price'] ?? 0);
            if ($price <= 0) { continue; }
            if ($at > 0 && (time() - $at) >= 6 * HOUR_IN_SECONDS) { $prior[] = $price; if ($oldest === 0 || $at < $oldest) { $oldest = $at; } }
        }
        if (count($prior) < 4 || $oldest === 0 || time() - $oldest < DAY_IN_SECONDS) { return 0.0; }
        $ref = self::median($prior);
        return $ref > $current ? $ref : 0.0;
    }

    private static function market_reference($candidate, $candidates) {
        $gtins = (array)($candidate['gtins'] ?? array());
        if (!$gtins) { return array('reference'=>0.0,'peer_count'=>0,'provider_count'=>0); }
        $prices = array(); $providers = array();
        foreach ($candidates as $peer) {
            if ((string)($peer['offer_key'] ?? '') === (string)($candidate['offer_key'] ?? '')) { continue; }
            if (!array_intersect($gtins, (array)($peer['gtins'] ?? array()))) { continue; }
            $price = (float)($peer['price'] ?? 0); if ($price <= 0) { continue; }
            $prices[] = $price; $providers[sanitize_key((string)($peer['provider'] ?? ''))] = true;
        }
        return array('reference'=>self::median($prices),'peer_count'=>count($prices),'provider_count'=>count(array_filter(array_keys($providers))));
    }

    private static function qualify($candidate, $candidates, $history) {
        $s = self::settings();
        $price = (float)$candidate['price'];
        $market = self::market_reference($candidate, $candidates);
        $history_ref = self::history_reference($candidate, $history);
        $reference = 0.0; $basis = ''; $confidence = 0;
        if ($market['reference'] > $price && $market['provider_count'] >= 2) {
            $reference = (float)$market['reference']; $basis = 'Marktvergleich'; $confidence = 3;
        } elseif ($market['reference'] > $price && $market['provider_count'] >= 1) {
            $reference = (float)$market['reference']; $basis = 'Marktvergleich'; $confidence = 2;
        }
        if ($history_ref > $reference) { $reference = $history_ref; $basis = 'eigener Preisverlauf'; $confidence = max($confidence, 3); }
        if ($reference <= $price) { return null; }
        $saving = $reference - $price;
        $pct = ($saving / $reference) * 100;
        $min_pct = (float)$s['min_discount_pct']; $min_save = (float)$s['min_saving_eur'];
        if ($confidence === 2) { $min_pct = max($min_pct, 25); $min_save = max($min_save, 20); }
        if ($pct + 0.0001 < $min_pct || $saving + 0.0001 < $min_save) { return null; }
        $candidate['reference_price'] = round($reference, 2);
        $candidate['saving_eur'] = round($saving, 2);
        $candidate['discount_pct'] = round($pct, 1);
        $candidate['evidence_basis'] = $basis;
        $candidate['confidence'] = $confidence;
        $candidate['score'] = round($pct * 2 + min(50, $saving) + $confidence * 10, 2);
        $candidate['checked_at'] = time();
        return $candidate;
    }

    private static function compute_best($write_history = false) {
        $candidates = self::candidate_rows();
        $history = $write_history ? self::snapshot_candidates($candidates) : self::history();
        $qualified = array();
        foreach ($candidates as $candidate) {
            $q = self::qualify($candidate, $candidates, $history);
            if ($q) { $qualified[] = $q; }
        }
        usort($qualified, static function($a,$b){
            $cmp = ((float)($b['score'] ?? 0) <=> (float)($a['score'] ?? 0));
            if ($cmp !== 0) { return $cmp; }
            return ((float)($a['price'] ?? 0) <=> (float)($b['price'] ?? 0));
        });
        return array('best'=>$qualified[0] ?? null,'candidate_count'=>count($candidates),'qualified_count'=>count($qualified),'updated_at'=>time());
    }

    public static function refresh() {
        $state = self::compute_best(true);
        update_option(self::OPTION_STATE, $state, false);
        delete_transient('ppar_deal_best_reithelm_v1');
        return $state;
    }

    private static function best_current() {
        $cached = get_transient('ppar_deal_best_reithelm_v1');
        if (is_array($cached)) { return $cached; }
        $state = self::compute_best(false);
        set_transient('ppar_deal_best_reithelm_v1', $state, 5 * MINUTE_IN_SECONDS);
        return $state;
    }

    private static function page_is_test_scope() {
        $s = self::settings();
        if (empty($s['enabled']) || !is_singular()) { return false; }
        $post = get_post();
        if (!$post instanceof WP_Post || (string)$post->post_status !== 'publish') { return false; }
        $slug = sanitize_title((string)$post->post_name);
        $title = self::normalize_text((string)$post->post_title);
        if ($slug === (string)$s['test_slug']) { return true; }
        return preg_match('/\breithelme?\b/', $title) === 1;
    }

    private static function provider_label($provider) {
        $map = array('otto'=>'OTTO','idealo'=>'idealo','amazon'=>'Amazon','kelkoo'=>'Kelkoo','ebay'=>'eBay');
        return $map[$provider] ?? strtoupper((string)$provider);
    }

    private static function click_signature($offer_key) {
        return hash_hmac('sha256', (string)$offer_key.'|reithelme|'.self::CONTRACT_VERSION, wp_salt('auth'));
    }

    private static function click_url($candidate) {
        $key = (string)($candidate['offer_key'] ?? '');
        if ($key === '') { return ''; }
        return add_query_arg(array('ppar_deal_click'=>'1','offer'=>$key,'sig'=>self::click_signature($key)), home_url('/'));
    }

    private static function record_click($provider) {
        $provider = sanitize_key((string)$provider); if ($provider === '') { return; }
        $all = get_option(self::OPTION_CLICK_DAILY, array()); $all = is_array($all) ? $all : array();
        $record = isset($all[$provider]) && is_array($all[$provider]) ? $all[$provider] : array('total'=>0,'daily'=>array());
        $record['total'] = absint($record['total'] ?? 0) + 1;
        $daily = is_array($record['daily'] ?? null) ? $record['daily'] : array();
        $day = current_time('Y-m-d'); $daily[$day] = absint($daily[$day] ?? 0) + 1;
        ksort($daily); if (count($daily) > 120) { $daily = array_slice($daily, -120, null, true); }
        $record['daily'] = $daily; $all[$provider] = $record;
        update_option(self::OPTION_CLICK_DAILY, $all, false);
    }

    public static function handle_click() {
        if (empty($_GET['ppar_deal_click'])) { return; }
        $key = isset($_GET['offer']) ? sanitize_text_field(wp_unslash((string)$_GET['offer'])) : '';
        $sig = isset($_GET['sig']) ? sanitize_text_field(wp_unslash((string)$_GET['sig'])) : '';
        if ($key === '' || $sig === '' || !hash_equals(self::click_signature($key), $sig)) {
            wp_die('Ungültiger Angebotslink.', 'Top-Angebot', array('response'=>400));
        }
        delete_transient('ppar_deal_best_reithelm_v1');
        $state = self::best_current(); $best = is_array($state['best'] ?? null) ? $state['best'] : array();
        if (!$best || !hash_equals((string)($best['offer_key'] ?? ''), $key) || empty($best['url'])) {
            wp_die('Dieses Angebot ist nicht mehr aktuell.', 'Top-Angebot', array('response'=>410));
        }
        self::record_click((string)($best['provider'] ?? ''));
        nocache_headers();
        wp_redirect(esc_url_raw((string)$best['url']), 302, 'Affiliate-Zentrale Deal-Radar');
        exit;
    }

    private static function render_block($best) {
        $provider = self::provider_label((string)($best['provider'] ?? ''));
        $cta = $provider === 'idealo' ? 'Bei idealo vergleichen' : 'Bei '.$provider.' ansehen';
        $click = self::click_url($best); if ($click === '') { return ''; }
        ob_start(); ?>
        <aside class="ppar-deal-kracher" aria-label="Aktuell besonders günstiges Angebot">
            <style>
                .ppar-deal-kracher{max-width:1200px;margin:34px auto;padding:22px;border:1px solid #d7d9d1;border-radius:14px;background:#fbfaf6;display:grid;grid-template-columns:minmax(190px,260px) 1fr;gap:26px;align-items:center;box-sizing:border-box}
                .ppar-deal-kracher__img{width:100%;height:210px;object-fit:contain;background:#fff;border-radius:10px}
                .ppar-deal-kracher__eyebrow{font-size:13px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;margin:0 0 8px;color:#7b5a18}
                .ppar-deal-kracher h2{margin:0 0 10px;font-size:clamp(22px,2.2vw,31px);line-height:1.15}
                .ppar-deal-kracher__price{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;margin:12px 0}
                .ppar-deal-kracher__now{font-size:30px;font-weight:800}
                .ppar-deal-kracher__ref{font-size:15px;color:#687066}
                .ppar-deal-kracher__badge{display:inline-block;padding:6px 10px;border-radius:999px;background:#35422a;color:#fff;font-weight:700}
                .ppar-deal-kracher__meta{margin:8px 0 16px;color:#687066}
                .ppar-deal-kracher__cta{display:inline-block;padding:11px 18px;border-radius:6px;background:#35422a;color:#fff!important;text-decoration:none!important;font-weight:700}
                .ppar-deal-kracher__cta:hover,.ppar-deal-kracher__cta:focus{background:#c89214;color:#fff!important}
                @media(max-width:700px){.ppar-deal-kracher{grid-template-columns:1fr;padding:16px}.ppar-deal-kracher__img{height:190px}}
            </style>
            <div><img class="ppar-deal-kracher__img" src="<?php echo esc_url((string)$best['image_url']); ?>" alt="<?php echo esc_attr((string)$best['title']); ?>" loading="lazy"></div>
            <div>
                <p class="ppar-deal-kracher__eyebrow">Aktuell besonders günstig</p>
                <h2><?php echo esc_html((string)$best['title']); ?></h2>
                <div class="ppar-deal-kracher__price"><span class="ppar-deal-kracher__now"><?php echo esc_html(number_format_i18n((float)$best['price'],2)); ?> €</span><span class="ppar-deal-kracher__ref">Vergleich <?php echo esc_html(number_format_i18n((float)$best['reference_price'],2)); ?> €</span><span class="ppar-deal-kracher__badge">−<?php echo esc_html(number_format_i18n((float)$best['discount_pct'],1)); ?> %</span></div>
                <p class="ppar-deal-kracher__meta"><?php echo esc_html((string)$best['evidence_basis']); ?> · <?php echo esc_html($provider); ?> · automatisch geprüft</p>
                <a class="ppar-deal-kracher__cta" href="<?php echo esc_url($click); ?>" rel="sponsored nofollow noopener" target="_blank"><?php echo esc_html($cta); ?></a>
            </div>
        </aside>
        <?php return (string)ob_get_clean();
    }

    public static function filter_content($content) {
        if (self::$rendered || is_admin() || (function_exists('wp_doing_ajax') && wp_doing_ajax()) || !self::page_is_test_scope()) { return $content; }
        self::$rendered = true;
        $state = self::best_current(); $best = is_array($state['best'] ?? null) ? $state['best'] : array();
        if (!$best) { return $content; }
        return (string)$content . self::render_block($best);
    }

    private static function source_statuses() {
        $statuses = array(
            'Amazon'=>array('key'=>'amazon','note'=>'fest eingeplant; Adapter noch nicht aktiv'),
            'OTTO'=>array('key'=>'otto','note'=>'Produktfeed kann technisch über Awin laufen'),
            'Kelkoo'=>array('key'=>'kelkoo','note'=>'Publisher-Zugang beantragt; API/Feed nach Freischaltung anbinden'),
            'idealo'=>array('key'=>'idealo','note'=>'bestehende Produkt-/Preisquelle'),
            'eBay'=>array('key'=>'ebay','note'=>'ergänzende Produktquelle; laufender Worker bleibt unangetastet'),
        );
        if (!self::table_exists()) { return $statuses; }
        global $wpdb; $table=self::table_name();
        $rows=(array)$wpdb->get_results("SELECT network,programme_name,COUNT(*) AS cnt,MAX(last_seen) AS last_seen FROM {$table} GROUP BY network,programme_name",ARRAY_A);
        foreach ($rows as $row) {
            $network=sanitize_key((string)($row['network']??'')); $programme=self::normalize_text((string)($row['programme_name']??''));
            $key=$network; if($network==='awin' && preg_match('/\botto\b/',$programme)){$key='otto';}
            foreach($statuses as $label=>&$status){if($status['key']!==$key){continue;} $status['count']=absint($status['count']??0)+absint($row['cnt']??0);$status['last_seen']=max(absint($status['last_seen']??0),absint($row['last_seen']??0));}
            unset($status);
        }
        return $statuses;
    }

    public static function handle_save() {
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.'); }
        check_admin_referer('ppar_deal_radar_save','ppar_deal_radar_nonce');
        $raw=isset($_POST['ppar_deal'])&&is_array($_POST['ppar_deal'])?wp_unslash($_POST['ppar_deal']):array();
        $s=self::settings();
        $s['enabled']=!empty($raw['enabled']);
        $s['min_discount_pct']=min(60,max(10,(float)str_replace(',','.',(string)($raw['min_discount_pct']??$s['min_discount_pct']))));
        $s['min_saving_eur']=min(500,max(5,(float)str_replace(',','.',(string)($raw['min_saving_eur']??$s['min_saving_eur']))));
        $s['max_age_hours']=min(72,max(6,absint($raw['max_age_hours']??$s['max_age_hours'])));
        update_option(self::OPTION_SETTINGS,$s,false); self::refresh();
        wp_safe_redirect(add_query_arg(array('page'=>'affiliate-portal-deals','saved'=>'1'),admin_url('admin.php'))); exit;
    }

    public static function render_admin_page() {
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.'); }
        $s=self::settings(); $state=self::refresh(); $best=is_array($state['best']??null)?$state['best']:array(); $sources=self::source_statuses();
        ?>
        <div class="wrap" style="max-width:1180px"><h1>Produktquellen &amp; Deals</h1>
            <p><strong>Erster Testscope: nur Reithelme.</strong> Kein belastbarer Preisvorteil = kein öffentlicher Angebotsblock.</p>
            <?php if (!empty($_GET['saved'])) : ?><div class="notice notice-success"><p>Einstellungen gespeichert und Deal-Radar neu geprüft.</p></div><?php endif; ?>
            <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:12px;margin:18px 0">
                <?php foreach($sources as $label=>$status): ?><div class="postbox" style="padding:14px"><strong><?php echo esc_html($label); ?></strong><div style="margin-top:6px"><?php echo isset($status['count'])?esc_html(number_format_i18n($status['count']).' Produktzeilen'):'<span class="description">noch keine Produktdaten</span>'; ?></div><?php if(!empty($status['last_seen'])):?><div class="description">zuletzt <?php echo esc_html(wp_date('d.m.Y H:i',$status['last_seen'])); ?></div><?php endif; ?><p class="description"><?php echo esc_html($status['note']); ?></p></div><?php endforeach; ?>
            </div>
            <section class="postbox" style="padding:18px"><h2>Aktueller Reithelm-Kracher</h2><?php if($best): ?><p><strong><?php echo esc_html($best['title']); ?></strong><br><?php echo esc_html(number_format_i18n($best['price'],2).' € statt Vergleich '.number_format_i18n($best['reference_price'],2).' € · -'.number_format_i18n($best['discount_pct'],1).' % · '.self::provider_label($best['provider'])); ?></p><p class="description">Beleg: <?php echo esc_html($best['evidence_basis']); ?>. Öffentliche Ausgabe nur solange der Kandidat aktuell qualifiziert bleibt.</p><?php else: ?><p><strong>Aktuell kein belastbarer Kracher.</strong></p><p class="description"><?php echo esc_html(number_format_i18n($state['candidate_count']??0).' passende Reithelm-Kandidaten geprüft; '.number_format_i18n($state['qualified_count']??0).' erfüllen die harte Deal-Schwelle.'); ?></p><?php endif; ?></section>
            <section class="postbox" style="padding:18px"><h2>Testregeln</h2><form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>"><input type="hidden" name="action" value="ppar_deal_radar_save"><?php wp_nonce_field('ppar_deal_radar_save','ppar_deal_radar_nonce'); ?><p><label><input type="checkbox" name="ppar_deal[enabled]" value="1" <?php checked(!empty($s['enabled'])); ?>> Kracher-Test auf Reithelme aktiv</label></p><p><label>Mindestvorteil in % <input type="number" min="10" max="60" step="0.5" name="ppar_deal[min_discount_pct]" value="<?php echo esc_attr((string)$s['min_discount_pct']); ?>"></label></p><p><label>Mindestersparnis in € <input type="number" min="5" max="500" step="1" name="ppar_deal[min_saving_eur]" value="<?php echo esc_attr((string)$s['min_saving_eur']); ?>"></label></p><p><label>Maximales Datenalter in Stunden <input type="number" min="6" max="72" step="1" name="ppar_deal[max_age_hours]" value="<?php echo esc_attr((string)$s['max_age_hours']); ?>"></label></p><?php submit_button('Speichern & neu prüfen'); ?></form></section>
        </div>
        <?php
    }
}
