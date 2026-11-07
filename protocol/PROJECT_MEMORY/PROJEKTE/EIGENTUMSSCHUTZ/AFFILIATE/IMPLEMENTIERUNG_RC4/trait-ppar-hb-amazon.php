<?php
/**
 * Hab & Bewahr Amazon bridge for the EXISTING affiliate product pipeline.
 * Uses feed ASINs or narrowly verified DataForSEO matches. Never imports
 * Amazon images, prices, reviews, ratings, availability or sales assertions.
 * No parallel campaigns, no separate frontend/DB engine, no affiliate redirects.
 */
if (!defined('ABSPATH')) { exit; }
trait PPAR_HB_Amazon_Trait {
    const HB_AMAZON_OPTION = 'ppar_hab_amazon_settings_v1';
    const HB_AMAZON_CONTROL = 'ppar_hab_amazon_dfs_control_v1';
    const HB_AMAZON_CRON = 'ppar_hab_amazon_dfs_tick_v1';

    public function hb_amazon_register_hooks() {
        add_action('admin_menu', array($this, 'hb_amazon_admin_menu'), 60);
        add_action('admin_post_ppar_hb_amazon_save', array($this, 'hb_amazon_save'));
        add_action('init', array($this, 'hb_amazon_ensure_cron'), 40);
        add_action(self::HB_AMAZON_CRON, array($this, 'hb_amazon_dfs_tick'));
    }

    private function hb_amazon_settings() {
        $stored = get_option(self::HB_AMAZON_OPTION, array());
        if (!is_array($stored)) { $stored = array(); }
        return array_merge(array('enabled'=>false, 'tag'=>'', 'dfs_enabled'=>false,
            'login'=>'', 'password'=>'', 'last_save'=>0), $stored);
    }

    private function hb_amazon_tag($s = null) {
        $s = is_array($s) ? $s : $this->hb_amazon_settings();
        $tag = trim((string)($s['tag'] ?? ''));
        // Only the exact, user-confirmed Hab & Bewahr tag may be used.
        return $tag === 'habundbewahr-21' ? $tag : '';
    }

    private function hb_amazon_ready($s = null) {
        $s = is_array($s) ? $s : $this->hb_amazon_settings();
        return !empty($s['enabled']) && $this->hb_amazon_tag($s) !== '';
    }

    private function hb_amazon_dfs_ready($s = null) {
        $s = is_array($s) ? $s : $this->hb_amazon_settings();
        $login = defined('PPAR_HAB_DATAFORSEO_LOGIN') ? (string)PPAR_HAB_DATAFORSEO_LOGIN : (string)$s['login'];
        $password = defined('PPAR_HAB_DATAFORSEO_PASSWORD') ? (string)PPAR_HAB_DATAFORSEO_PASSWORD : (string)$s['password'];
        return $this->hb_amazon_ready($s) && !empty($s['dfs_enabled']) && trim($login) !== '' && trim($password) !== '';
    }

    private function hb_amazon_direct_url($asin, $settings = null) {
        $asin = strtoupper(trim((string)$asin));
        $settings = is_array($settings) ? $settings : $this->hb_amazon_settings();
        if (!$this->hb_amazon_ready($settings) || !preg_match('/^[A-Z0-9]{10}$/D', $asin)) { return ''; }
        return 'https://www.amazon.de/dp/' . rawurlencode($asin) . '?tag=' . rawurlencode($this->hb_amazon_tag($settings));
    }

    private function hb_amazon_campaign_verified_asin($campaign) {
        if (!is_array($campaign) || empty($campaign['active'])
            || sanitize_key((string)($campaign['creative_type'] ?? '')) !== 'product') { return ''; }
        $network = sanitize_key((string)($campaign['network'] ?? ''));
        $source = sanitize_key((string)($campaign['source'] ?? ''));
        $asins = array_values(array_unique(array_filter(array_map('strtoupper', (array)($campaign['product_asins'] ?? array())),
            static function($a){ return is_string($a) && preg_match('/^[A-Z0-9]{10}$/D', $a); })));
        if (count($asins) !== 1) { return ''; }
        $asin = $asins[0];
        if ($network === 'idealo' && $source === 'idealo_product_feed_v1'
            && sanitize_key((string)($campaign['product_identity_source'] ?? '')) === 'gtin'
            && !empty($campaign['product_gtins'])) { return $asin; }
        // Only a current verified result for exactly this source title is reusable.
        $id = absint($campaign['post_id'] ?? 0);
        if (!$id || !in_array($network, array('ebay','idealo'), true)) { return ''; }
        $m = get_post_meta($id, '_ppar_hb_amazon_exact_match_v1', true);
        $title = (string)($campaign['title'] ?? '');
        if (is_array($m) && $asin === (string)($m['asin'] ?? '')
            && hash_equals((string)($m['title_hash'] ?? ''), hash('sha256', $this->hb_amazon_normalize_title($title)))
            && absint($m['verified_at'] ?? 0) > time() - 30 * DAY_IN_SECONDS) { return $asin; }
        return '';
    }

    /** Add only an additional Amazon CTA to an already valid existing product card. */
    private function hb_amazon_add_offer($offers, $campaign, $context, $slot_type) {
        $offers = array_values((array)$offers);
        if (!$this->hb_amazon_ready() || !is_array($campaign) || !$offers) { return $offers; }
        foreach ($offers as $offer) { if (sanitize_key((string)($offer['network'] ?? '')) === 'amazon') { return $offers; } }
        $asin = $this->hb_amazon_campaign_verified_asin($campaign);
        if ($asin === '') { return $offers; }
        $url = $this->hb_amazon_direct_url($asin);
        if ($url !== '') { $offers[] = array('network'=>'amazon','url'=>$url,'label'=>'Bei Amazon ansehen'); }
        return $offers;
    }

    public function hb_amazon_admin_menu() {
        if (function_exists('add_submenu_page')) {
            add_submenu_page('affiliate-portal-zentrale', 'Amazon-Automatik', 'Amazon-Automatik',
                'manage_options', 'affiliate-portal-hab-amazon', array($this, 'hb_amazon_render_settings'));
        }
    }

    public function hb_amazon_render_settings() {
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.'); }
        $s = $this->hb_amazon_settings();
        $c = get_option(self::HB_AMAZON_CONTROL, array()); if (!is_array($c)) { $c = array(); }
        $status = $this->hb_amazon_ready($s) ? 'Amazon-Links eingeschaltet' : 'Noch nicht eingeschaltet';
        if ($this->hb_amazon_dfs_ready($s)) { $status .= ' · DataForSEO-Automatik eingeschaltet'; }
        $day = gmdate('Y-m-d');
        $count = ($c['day'] ?? '') === $day ? min(5, absint($c['count'] ?? 0)) : 0;
        echo '<div class="wrap"><h1>Hab &amp; Bewahr – Amazon-Automatik</h1>';
        echo '<p>Vorhandene Produkt- und Kategorienzuordnung wird weiterverwendet. Keine manuelle Einzel-Linkanlage.</p>';
        echo '<p><strong>Status:</strong> '.esc_html($status).'</p>';
        echo '<form method="post" action="'.esc_url(admin_url('admin-post.php')).'">';
        wp_nonce_field('ppar_hb_amazon_save','ppar_hb_amazon_nonce');
        echo '<input type="hidden" name="action" value="ppar_hb_amazon_save">';
        echo '<table class="form-table" role="presentation">';
        echo '<tr><th>Amazon-Tracking-ID</th><td><input type="text" class="regular-text" name="amazon_tag" value="'.esc_attr($s['tag']).'" placeholder="habundbewahr-21"><p class="description">Nur die eigene Hab-&amp;-Bewahr-Tracking-ID wird akzeptiert.</p></td></tr>';
        echo '<tr><th>Amazon-Produktbuttons</th><td><label><input type="checkbox" name="amazon_enabled" value="1" '.checked(!empty($s['enabled']),true,false).'> Automatisch bei eindeutig geprüfter ASIN anzeigen</label></td></tr>';
        $external = defined('PPAR_HAB_DATAFORSEO_LOGIN') && defined('PPAR_HAB_DATAFORSEO_PASSWORD');
        echo '<tr><th>DataForSEO</th><td><label><input type="checkbox" name="dfs_enabled" value="1" '.checked(!empty($s['dfs_enabled']),true,false).'> Automatische ASIN-Recherche aktivieren (kostenpflichtig, max. 5 neue Suchaufträge pro UTC-Tag)</label></td></tr>';
        echo '<tr><th>DataForSEO API-Login</th><td><input type="text" name="dfs_login" autocomplete="off" value="'.esc_attr($external ? '' : $s['login']).'" placeholder="'.($external?'über wp-config.php':'API-Login').'"></td></tr>';
        echo '<tr><th>DataForSEO API-Passwort</th><td><input type="password" name="dfs_password" autocomplete="new-password" value="" placeholder="'.($external?'über wp-config.php':($s['password']!==''?'bereits gespeichert':'API-Passwort')).'"><p class="description">Leer lassen = gespeichertes Passwort beibehalten.</p></td></tr>';
        echo '</table><p><button type="submit" class="button button-primary">Speichern</button></p></form>';
        echo '<h2>Automatischer Ablauf</h2><p>Nur vorhandene, freigegebene idealo-/eBay-Produkte werden nach eindeutiger Identität ergänzt. Keine Amazon-Bilder, Preise oder Bewertungen aus DataForSEO.</p>';
        echo '<p><strong>Bezahlte Suchaufträge heute:</strong> '.esc_html((string)$count).' von 5</p>';
        echo '<p><strong>Offener Auftrag:</strong> '.(!empty($c['pending_id'])?'ja':'nein').'</p>';
        echo '<p><strong>Letzte Meldung:</strong> '.esc_html((string)($c['message'] ?? 'Noch keine Recherche')).'</p>';
        echo '<p><strong>Letzte eindeutige ASIN:</strong> '.(!empty($c['last_match_at'])?esc_html(wp_date('d.m.Y H:i',absint($c['last_match_at']))):'noch keine').'</p>';
        echo '<p><strong>Nächste automatische Prüfung:</strong> '.esc_html($this->hb_amazon_dfs_ready($s) && wp_next_scheduled(self::HB_AMAZON_CRON) ? 'geplant' : 'nicht geplant').'</p>';
        echo '<p class="description">Idealo ist ein getrenntes Netzwerk. Es muss mit eigenen Hab-&amp;-Bewahr-Zugangsdaten aktiviert werden.</p></div>';
    }

    public function hb_amazon_save() {
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.'); }
        check_admin_referer('ppar_hb_amazon_save', 'ppar_hb_amazon_nonce');
        $s = $this->hb_amazon_settings();
        $tag = sanitize_text_field(wp_unslash((string)($_POST['amazon_tag'] ?? '')));
        $s['tag'] = ($tag === 'habundbewahr-21') ? $tag : '';
        $s['enabled'] = !empty($_POST['amazon_enabled']) && $s['tag'] !== '';
        $s['dfs_enabled'] = !empty($_POST['dfs_enabled']);
        if (!defined('PPAR_HAB_DATAFORSEO_LOGIN')) {
            $login = trim(sanitize_text_field(wp_unslash((string)($_POST['dfs_login'] ?? ''))));
            if ($login !== '') { $s['login'] = $login; }
        }
        if (!defined('PPAR_HAB_DATAFORSEO_PASSWORD')) {
            $password = wp_unslash((string)($_POST['dfs_password'] ?? ''));
            if ($password !== '') { $s['password'] = $password; }
        }
        $s['last_save'] = time();
        update_option(self::HB_AMAZON_OPTION, $s, false);
        $this->hb_amazon_ensure_cron();
        wp_safe_redirect(admin_url('admin.php?page=affiliate-portal-hab-amazon'));
        exit;
    }

    public function hb_amazon_ensure_cron() {
        if (!function_exists('wp_next_scheduled') || !function_exists('wp_schedule_event')) { return; }
        $next = wp_next_scheduled(self::HB_AMAZON_CRON);
        if (!$this->hb_amazon_dfs_ready()) {
            if ($next && function_exists('wp_clear_scheduled_hook')) { wp_clear_scheduled_hook(self::HB_AMAZON_CRON); }
            return;
        }
        if (!$next) { wp_schedule_event(time()+300,'hourly',self::HB_AMAZON_CRON); }
    }

    private function hb_amazon_dfs_api($method, $url, $payload = null, $s = null) {
        $s = is_array($s) ? $s : $this->hb_amazon_settings();
        if (!$this->hb_amazon_dfs_ready($s)) { return new WP_Error('hb_amazon_not_ready', 'Amazon/DataForSEO noch nicht vollständig freigegeben.'); }
        $login = defined('PPAR_HAB_DATAFORSEO_LOGIN') ? (string)PPAR_HAB_DATAFORSEO_LOGIN : (string)$s['login'];
        $pass = defined('PPAR_HAB_DATAFORSEO_PASSWORD') ? (string)PPAR_HAB_DATAFORSEO_PASSWORD : (string)$s['password'];
        // Fixed HTTPS allowlist: no user-provided URL or redirect, no credentials leak.
        if (!preg_match('#^https://api\.dataforseo\.com/v3/merchant/amazon/products/(?:task_post|task_get/advanced/[0-9a-f-]{36})$#D', $url)) {
            return new WP_Error('hb_amazon_endpoint', 'Unerwarteter DataForSEO-Endpunkt.');
        }
        $args = array('method'=>$method,'timeout'=>25,'redirection'=>0,
            'headers'=>array('Authorization'=>'Basic '.base64_encode($login.':'.$pass),'Content-Type'=>'application/json'));
        if ($payload !== null) { $args['body'] = wp_json_encode($payload); }
        $response = wp_remote_request($url, $args);
        if (is_wp_error($response)) { return $response; }
        if ((int)wp_remote_retrieve_response_code($response) !== 200) {
            return new WP_Error('hb_amazon_http', 'DataForSEO HTTP '.(int)wp_remote_retrieve_response_code($response));
        }
        $data = json_decode((string)wp_remote_retrieve_body($response), true);
        if (!is_array($data) || (int)($data['status_code'] ?? 0) !== 20000 || empty($data['tasks']) || !is_array($data['tasks'])) {
            return new WP_Error('hb_amazon_api', 'Ungültige oder fehlerhafte DataForSEO-Antwort.');
        }
        return $data;
    }

    private function hb_amazon_normalize_title($title) {
        $title = strtolower(str_replace(array('Ä','Ö','Ü'), array('ä','ö','ü'), trim((string)$title)));
        $title = str_replace(array('ä','ö','ü','ß'),array('ae','oe','ue','ss'),$title);
        $title = preg_replace('/[^a-z0-9]+/',' ',$title);
        $terms = array_values(array_filter(explode(' ',trim($title)),static function($s){ return strlen($s) > 1; }));
        sort($terms, SORT_STRING);
        return implode(' ', $terms);
    }

    /** Conservative identity: identical complete title token multiset, not fuzzy resemblance. */
    private function hb_amazon_exact_match_asin($title, $items) {
        $needle = $this->hb_amazon_normalize_title($title);
        if ($needle === '' || count(explode(' ', $needle)) < 2) { return ''; }
        $matched = array();
        foreach ((array)$items as $item) {
            if (!is_array($item)) { continue; }
            $type = (string)($item['type'] ?? '');
            if (!in_array($type,array('amazon_serp','amazon_serp_element'),true)) { continue; }
            $url = (string)($item['url'] ?? '');
            $host = strtolower((string)wp_parse_url($url, PHP_URL_HOST));
            if (!in_array($host,array('amazon.de','www.amazon.de'),true)) { continue; }
            if ($this->hb_amazon_normalize_title((string)($item['title'] ?? '')) !== $needle) { continue; }
            $asin = strtoupper(trim((string)($item['asin'] ?? '')));
            if (!preg_match('/^[A-Z0-9]{10}$/D',$asin)) {
                $asin = preg_match('#/(?:dp|gp/product)/([A-Z0-9]{10})(?:[/?]|$)#i',$url,$m) ? strtoupper($m[1]) : '';
            }
            if ($asin !== '' && preg_match('/^[A-Z0-9]{10}$/D',$asin)) { $matched[$asin] = true; }
        }
        return count($matched) === 1 ? (string)array_keys($matched)[0] : '';
    }

    private function hb_amazon_dfs_candidate(&$control) {
        $offset = max(0,absint($control['scan_offset'] ?? 0));
        $posts = get_posts(array('post_type'=>self::CAMPAIGN_POST_TYPE,'post_status'=>'publish',
            'posts_per_page'=>100, 'offset'=>$offset, 'orderby'=>'ID','order'=>'ASC','suppress_filters'=>true));
        if (!$posts && $offset>0) {
            $offset=0;
            $posts=get_posts(array('post_type'=>self::CAMPAIGN_POST_TYPE,'post_status'=>'publish',
                'posts_per_page'=>100,'offset'=>0,'orderby'=>'ID','order'=>'ASC','suppress_filters'=>true));
        }
        // Resume scanning after this bounded page if no match is found.
        $control['scan_offset']=$offset+(count((array)$posts)<100?0:100);
        if (count((array)$posts)<100) { $control['scan_offset']=0; }
        $checked = (array)($control['checked'] ?? array());
        foreach ((array)$posts as $post) {
            $campaign = $this->campaign_from_post($post);
            if (!is_array($campaign) || empty($campaign['active']) ||
                sanitize_key((string)($campaign['creative_type'] ?? ''))!=='product') { continue; }
            $net = sanitize_key((string)($campaign['network'] ?? ''));
            $source = sanitize_key((string)($campaign['source'] ?? ''));
            if (!(($net==='idealo' && $source==='idealo_product_feed_v1' && !empty($campaign['product_gtins'])) ||
                  ($net==='ebay' && $source==='output_object_v4' && !empty($campaign['product_gtins'])))) { continue; }
            if ($this->hb_amazon_campaign_verified_asin($campaign) !== '') { continue; }
            $title = trim((string)($campaign['title'] ?? ''));
            if (strlen($title) < 8 || !preg_match('/[a-zA-Z]{3}/',$title)) { continue; }
            $id = absint($post->ID);
            $fingerprint = hash('sha256',$this->hb_amazon_normalize_title($title));
            if (isset($checked[$id]) && ($checked[$id]['hash'] ?? '') === $fingerprint &&
                absint($checked[$id]['at'] ?? 0) > time()-7*DAY_IN_SECONDS) { continue; }
            return array('id'=>$id,'title'=>$title,'hash'=>$fingerprint);
        }
        return null;
    }

    public function hb_amazon_dfs_tick() {
        $s = $this->hb_amazon_settings();
        if (!$this->hb_amazon_dfs_ready($s)) { return; }
        $lock = 'ppar_hb_amazon_dfs_worker_lock';
        if (get_transient($lock)) { return; }
        set_transient($lock,1,180);
        try { $this->hb_amazon_dfs_do_tick($s); }
        finally { delete_transient($lock); }
    }

    private function hb_amazon_dfs_do_tick($s) {
        $control = get_option(self::HB_AMAZON_CONTROL, array());
        if (!is_array($control)) { $control = array(); }
        $day = gmdate('Y-m-d');
        if (($control['day'] ?? '') !== $day) { $control['day'] = $day; $control['count'] = 0; }
        $pending = (string)($control['pending_id'] ?? '');
        if ($pending !== '') {
            // Never pay again while a GET result for a prior paid task is pending.
            if (!preg_match('/^[0-9a-f-]{36}$/D',$pending)) { $control['pending_id']=''; $control['message']='Ungültige offene Auftrag-ID'; }
            elseif (absint($control['pending_at'] ?? 0) < time()-48*HOUR_IN_SECONDS) {
                $control['pending_id']=''; $control['message']='Alter DataForSEO-Auftrag ohne Ergebnis abgelaufen';
            } else {
                $response = $this->hb_amazon_dfs_api('GET', 'https://api.dataforseo.com/v3/merchant/amazon/products/task_get/advanced/'.$pending, null, $s);
                if (is_wp_error($response)) { $control['message']='Ergebnisabruf fehlgeschlagen: '.$response->get_error_message(); update_option(self::HB_AMAZON_CONTROL,$control,false); return; }
                $task = (array)($response['tasks'][0] ?? array());
                $result = (array)($task['result'] ?? array());
                if (!$result) { $control['message']='DataForSEO-Auftrag noch in Bearbeitung'; update_option(self::HB_AMAZON_CONTROL,$control,false); return; }
                $items = (array)($result[0]['items'] ?? array());
                $source = $this->campaign_from_post(get_post(absint($control['pending_post_id'] ?? 0)));
                $expected = (string)($control['pending_hash'] ?? '');
                $title = is_array($source) ? (string)($source['title'] ?? '') : '';
                $asin = ($title!=='' && hash_equals($expected, hash('sha256',$this->hb_amazon_normalize_title($title))))
                    ? $this->hb_amazon_exact_match_asin($title,$items) : '';
                $cid = absint($control['pending_post_id'] ?? 0);
                if ($asin!=='' && $cid>0 && is_array($source) && !empty($source['active'])) {
                    $source['product_asins'] = array($asin);
                    $saved=$this->save_campaign_record($source,$cid);
                    if (!is_wp_error($saved) && $saved) {
                        update_post_meta($cid, '_ppar_hb_amazon_exact_match_v1', array('asin'=>$asin,'title_hash'=>$expected,'verified_at'=>time()));
                        $control['last_match_at']=time();
                        $control['message']='Eindeutige ASIN zugeordnet';
                    } else { $control['message']='ASIN-Speicherung fehlgeschlagen; keine Freigabe'; }
                } else { $control['message']='Kein eindeutiges identisches Amazon-Produkt gefunden'; }
                $checked=(array)($control['checked'] ?? array());
                if ($cid>0) { $checked[$cid]=array('hash'=>$expected,'at'=>time()); }
                $control['checked']=array_slice($checked,-200,null,true);
                unset($control['pending_id'],$control['pending_post_id'],$control['pending_hash'],$control['pending_at']);
                update_option(self::HB_AMAZON_CONTROL,$control,false);
                return;
            }
        }
        if (absint($control['count'] ?? 0)>=5) { $control['message']='Tagesgrenze: 5 bezahlte Suchaufträge erreicht'; update_option(self::HB_AMAZON_CONTROL,$control,false); return; }
        $candidate = $this->hb_amazon_dfs_candidate($control);
        if (!$candidate) { $control['message']='Keine neuen freigegebenen Produktkandidaten'; update_option(self::HB_AMAZON_CONTROL,$control,false); return; }
        // The counter is reserved BEFORE the paid POST; a timeout can still be billable.
        $control['count']=absint($control['count'] ?? 0)+1;
        $control['last_attempt_at']=time();
        $control['message']='Bezahlte Suche gestartet';
        update_option(self::HB_AMAZON_CONTROL,$control,false);
        $payload = array(array('keyword'=>$candidate['title'], 'location_name'=>'Germany',
            'language_code'=>'de_DE', 'se_domain'=>'amazon.de', 'depth'=>20));
        $response = $this->hb_amazon_dfs_api('POST','https://api.dataforseo.com/v3/merchant/amazon/products/task_post',$payload,$s);
        if (is_wp_error($response)) { $control['message']='Suchauftrag fehlgeschlagen (Tagesbudget reserviert): '.$response->get_error_message(); update_option(self::HB_AMAZON_CONTROL,$control,false); return; }
        $task = (array)($response['tasks'][0] ?? array());
        $id = (string)($task['id'] ?? '');
        if ((int)($task['status_code'] ?? 0)!==20100 && (int)($task['status_code'] ?? 0)!==20000) { $id=''; }
        if (!preg_match('/^[0-9a-f-]{36}$/D',$id)) {
            $control['message']='Keine gültige Auftrag-ID in API-Antwort'; update_option(self::HB_AMAZON_CONTROL,$control,false); return;
        }
        $control['pending_id']=$id; $control['pending_post_id']=$candidate['id'];
        $control['pending_hash']=$candidate['hash']; $control['pending_at']=time();
        $control['message']='Amazon-ASIN-Suchauftrag angelegt; Ergebnisabfrage beim nächsten Lauf';
        update_option(self::HB_AMAZON_CONTROL,$control,false);
    }
}