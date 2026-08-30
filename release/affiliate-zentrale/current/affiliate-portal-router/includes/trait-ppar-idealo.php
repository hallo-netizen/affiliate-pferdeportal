<?php
if (!defined('ABSPATH')) { exit; }

/**
 * idealo iPN adapter V3.0 – Multi-Provider contract implementation.
 *
 * KISS boundaries:
 * - eBay remains an independent provider and keeps its existing workflow.
 * - idealo is staged, materialized and refreshed independently.
 * - only exact portal mappings and exact product identifiers are used.
 * - provider failures are local; the last good state of other providers survives.
 * - combined cards are optional and only join offers sharing an exact GTIN.
 */
trait PPAR_Idealo_Trait {
    const IDEALO_REFRESH_HOOK = 'ppar_idealo_refresh_v1';
    const IDEALO_MANUAL_REFRESH_HOOK = 'ppar_idealo_manual_refresh_v1';
    const IDEALO_MANUAL_WORKER_ACTION = 'ppar_idealo_manual_refresh_worker_v2';
    const IDEALO_REFRESH_LOCK = 'ppar_idealo_refresh_lock_v1';
    const IDEALO_SCHEMA_OPTION = 'ppar_idealo_adapter_schema_v4';

    public function idealo_register_hooks() {
        add_filter('ppar_affiliate_provider_access_snapshot', array($this, 'idealo_provider_access_snapshot'), 10, 4);
        add_filter('ppar_affiliate_provider_access_save', array($this, 'idealo_provider_access_save'), 10, 4);
        add_filter('ppar_affiliate_provider_access_test', array($this, 'idealo_provider_access_test'), 10, 3);
        add_filter('ppar_affiliate_provider_sync_dispatch', array($this, 'idealo_sync_dispatch'), 10, 4);
        add_action('ppar_affiliate_render_provider_access_card_idealo', array($this, 'idealo_render_access_card'), 10, 3);
        add_action('ppar_affiliate_render_provider_specialist_idealo', array($this, 'idealo_render_specialist_content'), 10, 3);
        add_action('ppar_affiliate_render_provider_sync_idealo', array($this, 'idealo_render_sync_card'), 10, 3);
        add_action('admin_post_ppar_idealo_import_file', array($this, 'handle_idealo_import_file'));
        add_filter('cron_schedules', array($this, 'idealo_cron_schedules'));
        add_action('init', array($this, 'idealo_maybe_upgrade_materialization'), 12);
        add_action('init', array($this, 'idealo_ensure_refresh_schedule'), 25);
        add_action(self::IDEALO_REFRESH_HOOK, array($this, 'idealo_run_scheduled_refresh'));
        add_action(self::IDEALO_MANUAL_REFRESH_HOOK, array($this, 'idealo_run_manual_refresh'));
        add_action('admin_post_' . self::IDEALO_MANUAL_WORKER_ACTION, array($this, 'handle_idealo_manual_refresh_worker'));
        add_action('admin_post_nopriv_' . self::IDEALO_MANUAL_WORKER_ACTION, array($this, 'handle_idealo_manual_refresh_worker'));
        add_action('init', array($this, 'idealo_maybe_recover_refresh_dispatch'), 26);
    }

    private function idealo_settings_defaults() {
        return array(
            'enabled' => false,
            'api_key' => '',
            'adspace_id' => '568313',
            'feed_id' => '2901',
            'feed_url' => '',
            'output_mode' => 'ebay_only',
            'link_strategy' => 'hybrid',
            'auto_refresh' => true,
            'last_feed_hash' => '',
            'feed_etag' => '',
            'feed_last_modified' => '',
            'last_download_at' => 0,
            'last_remote_file_hash' => '',
            'refresh_state' => 'idle',
            'refresh_requested_at' => 0,
            'refresh_started_at' => 0,
            'refresh_finished_at' => 0,
            'refresh_last_message' => '',
            'refresh_dispatch_token_hash' => '',
            'refresh_dispatch_token_expires' => 0,
            'refresh_dispatch_last_at' => 0,
            'refresh_dispatch_attempts' => 0,
            'refresh_dispatch_transport' => '',
            'api_last_checked_at' => 0,
            'api_last_feed_hash' => '',
            'api_last_updated_at' => '',
            'api_last_product_count' => 0,
            'api_last_advertiser_name' => '',
            'api_last_message' => '',
            'last_import_at' => 0,
            'last_import_started_at' => 0,
            'last_import_count' => 0,
            'last_materialized_at' => 0,
            'last_materialized_count' => 0,
            'last_materialized_targets' => 0,
            'last_matched_concepts' => 0,
            'last_matched_hubs' => 0,
            'last_ambiguous_count' => 0,
            'last_context_rejected_count' => 0,
            'last_message' => '',
        );
    }

    private function idealo_settings() {
        $stored = get_option(self::OPTION_NETWORK_IDEALO, array());
        $stored = is_array($stored) ? $stored : array();
        $settings = array_merge($this->idealo_settings_defaults(), $stored);
        if (defined('PPAR_IDEALO_API_KEY') && trim((string) PPAR_IDEALO_API_KEY) !== '') {
            $settings['api_key'] = trim((string) PPAR_IDEALO_API_KEY);
        }
        $settings['output_mode'] = $this->idealo_sanitize_output_mode($settings['output_mode'] ?? 'ebay_only');
        $settings['link_strategy'] = $this->idealo_sanitize_link_strategy($settings['link_strategy'] ?? 'hybrid');
        $settings['auto_refresh'] = !empty($settings['auto_refresh']);
        return $settings;
    }

    private function idealo_sanitize_output_mode($mode) {
        $mode = sanitize_key((string) $mode);
        return in_array($mode, array('ebay_only','idealo_only','separate','combined','automatic'), true) ? $mode : 'ebay_only';
    }

    public function idealo_output_mode() {
        return $this->idealo_sanitize_output_mode($this->idealo_settings()['output_mode'] ?? 'ebay_only');
    }

    private function idealo_sanitize_link_strategy($strategy) {
        $strategy = sanitize_key((string) $strategy);
        return in_array($strategy, array('hybrid','products','comparison'), true) ? $strategy : 'hybrid';
    }

    public function idealo_link_strategy() {
        return $this->idealo_sanitize_link_strategy($this->idealo_settings()['link_strategy'] ?? 'hybrid');
    }

    private function idealo_api_key_external() {
        return defined('PPAR_IDEALO_API_KEY') && trim((string) PPAR_IDEALO_API_KEY) !== '';
    }

    private function idealo_credentials_present($settings = null) {
        $settings = is_array($settings) ? $settings : $this->idealo_settings();
        return trim((string) ($settings['api_key'] ?? '')) !== ''
            && preg_match('/^\d+$/', (string) ($settings['adspace_id'] ?? ''))
            && preg_match('/^\d+$/', (string) ($settings['feed_id'] ?? ''));
    }

    private function idealo_partner_api_base() { return 'https://api.ingenious.cloud'; }

    private function idealo_api_host_allowed($url) {
        $parts = wp_parse_url((string) $url);
        if (!is_array($parts) || strtolower((string) ($parts['scheme'] ?? '')) !== 'https') { return false; }
        $host = strtolower((string) ($parts['host'] ?? ''));
        return $host === 'api.ingenious.cloud'
            || substr($host, -16) === '.ingenious.cloud'
            || $host === 'api.partner.net.ingenioustechnologies.com'
            || substr($host, -strlen('.ingenioustechnologies.com')) === '.ingenioustechnologies.com';
    }

    private function idealo_absolute_redirect_url($base, $location) {
        $location = trim((string) $location);
        if ($location === '') { return ''; }
        if (preg_match('#^https://#i', $location)) { return esc_url_raw($location); }
        $parts = wp_parse_url((string) $base);
        if (!is_array($parts) || empty($parts['scheme']) || empty($parts['host'])) { return ''; }
        if (strpos($location, '//') === 0) { return esc_url_raw($parts['scheme'] . ':' . $location); }
        $origin = $parts['scheme'] . '://' . $parts['host'] . (!empty($parts['port']) ? ':' . absint($parts['port']) : '');
        if (strpos($location, '/') === 0) { return esc_url_raw($origin . $location); }
        $dir = rtrim(str_replace('\\', '/', dirname((string) ($parts['path'] ?? '/'))), '/');
        return esc_url_raw($origin . ($dir !== '' ? $dir : '') . '/' . $location);
    }

    /** Preserve POST across the documented unified-API redirect. */
    private function idealo_partner_api_post($url, $api_key) {
        $current = esc_url_raw((string) $url);
        if (!$this->idealo_api_host_allowed($current)) {
            return new WP_Error('idealo_api_host_blocked', 'Unerwartete idealo/Ingenious-API-Domain.');
        }
        for ($hop = 0; $hop <= 4; $hop++) {
            $response = wp_remote_post($current, array(
                'timeout' => 25,
                'redirection' => 0,
                'headers' => array(
                    'Accept' => 'application/json',
                    'x-api-key' => (string) $api_key,
                    'Content-Type' => 'text/plain',
                ),
                'body' => '',
            ));
            if (is_wp_error($response)) { return $response; }
            $code = (int) wp_remote_retrieve_response_code($response);
            if (in_array($code, array(301,302,303,307,308), true)) {
                $location = wp_remote_retrieve_header($response, 'location');
                $next = $this->idealo_absolute_redirect_url($current, $location);
                if ($next === '' || !$this->idealo_api_host_allowed($next)) {
                    return new WP_Error('idealo_api_redirect_blocked', 'idealo-API lieferte eine nicht freigegebene Weiterleitung.');
                }
                $current = $next;
                continue;
            }
            return $response;
        }
        return new WP_Error('idealo_api_redirect_loop', 'idealo-API überschritt die erlaubte Zahl von Weiterleitungen.');
    }

    private function idealo_find_feed_metadata($settings = null) {
        $settings = is_array($settings) ? $settings : $this->idealo_settings();
        if (!$this->idealo_credentials_present($settings)) {
            return new WP_Error('idealo_credentials_missing', 'API-Key, Adspace-ID und Feed-ID müssen vollständig gespeichert sein.');
        }
        $api_key = trim((string) ($settings['api_key'] ?? ''));
        $adspace_id = (string) ($settings['adspace_id'] ?? '');
        $feed_id = (string) ($settings['feed_id'] ?? '');
        for ($page = 0; $page < 20; $page++) {
            $url = add_query_arg(array('adspaceId'=>$adspace_id,'page'=>$page,'rowsPerPage'=>100), $this->idealo_partner_api_base() . '/creatives/productdata/findFeeds');
            $response = $this->idealo_partner_api_post($url, $api_key);
            if (is_wp_error($response)) {
                return new WP_Error('idealo_api_transport_failed', 'idealo-Partner-API nicht erreichbar: ' . $response->get_error_message());
            }
            $code = (int) wp_remote_retrieve_response_code($response);
            if ($code !== 200) { return new WP_Error('idealo_api_http_' . $code, 'idealo-Partner-API antwortet mit HTTP ' . $code . '.'); }
            $data = json_decode((string) wp_remote_retrieve_body($response), true);
            if (!is_array($data) || !isset($data['entries']) || !is_array($data['entries'])) {
                return new WP_Error('idealo_api_response_invalid', 'idealo-Partner-API lieferte keine verwertbare Feedliste.');
            }
            foreach ($data['entries'] as $entry) {
                if (!is_array($entry) || (string) ($entry['feedId'] ?? '') !== $feed_id) { continue; }
                return array(
                    'feed_id'=>$feed_id,
                    'name'=>sanitize_text_field((string)($entry['name'] ?? '')),
                    'advertiser_id'=>sanitize_text_field((string)($entry['advertiserId'] ?? '')),
                    'advertiser_name'=>sanitize_text_field((string)($entry['advertiserName'] ?? '')),
                    'last_updated_at'=>sanitize_text_field((string)($entry['lastUpdatedAt'] ?? '')),
                    'last_modified_at'=>sanitize_text_field((string)($entry['lastModifiedAt'] ?? '')),
                    'number_of_products'=>absint($entry['numberOfProducts'] ?? 0),
                    'last_file_hash'=>sanitize_text_field((string)($entry['lastFileHash'] ?? '')),
                    'update_interval'=>sanitize_text_field((string)($entry['updateInterval'] ?? '')),
                );
            }
            $total_pages = max(1, absint($data['totalPages'] ?? 1));
            if ($page + 1 >= $total_pages) { break; }
        }
        return new WP_Error('idealo_feed_not_found', 'Feed-ID ' . $feed_id . ' wurde für Adspace-ID ' . $adspace_id . ' nicht gefunden.');
    }

    /**
     * Canonical portal product supply contract. The asset is shared structurally with
     * the existing production workflow; idealo reads it directly and never calls the
     * eBay provider runtime. Only the 311 required physical product concepts are used.
     */
    private function idealo_portal_supply_catalog() {
        static $cache = null;
        if (is_array($cache) || is_wp_error($cache)) { return $cache; }
        $path = dirname(__DIR__) . '/assets/ebay-portal-catalog-v2.json';
        if (!is_readable($path)) { return $cache = new WP_Error('idealo_portal_catalog_missing', 'Kanonischer Portal-Produktkatalog fehlt.'); }
        $data = json_decode((string) file_get_contents($path), true);
        if (!is_array($data)) { return $cache = new WP_Error('idealo_portal_catalog_invalid', 'Kanonischer Portal-Produktkatalog ist ungültig.'); }
        $contract = is_array($data['business_supply_contract'] ?? null) ? $data['business_supply_contract'] : array();
        $required_ids = array_values(array_filter(array_map('sanitize_key', (array) ($contract['required_product_concept_ids'] ?? array()))));
        $required_count = absint($contract['required_count'] ?? 0);
        if ($required_count !== 311 || count($required_ids) !== 311) {
            return $cache = new WP_Error('idealo_portal_contract_invalid', 'Portal-Produktvertrag ist nicht der gebundene 311er-Stand.');
        }
        $required = array_fill_keys($required_ids, true);
        $concepts = array();
        foreach ((array) ($data['business_concepts'] ?? array()) as $concept) {
            if (!is_array($concept)) { continue; }
            $id = sanitize_key((string) ($concept['id'] ?? ''));
            if ($id === '' || empty($required[$id])) { continue; }
            $concepts[$id] = $concept;
        }
        if (count($concepts) !== 311) {
            return $cache = new WP_Error('idealo_portal_concepts_incomplete', 'Nicht alle 311 gebundenen Produktkonzepte sind im Portal-Katalog vorhanden.');
        }
        $data['_idealo_required_concepts'] = $concepts;
        $data['_idealo_required_ids'] = $required_ids;
        $cache = $data;
        return $cache;
    }

    private function idealo_match_normalize($text) {
        $text = remove_accents(wp_strip_all_tags((string) $text));
        $text = strtolower(str_replace('&', ' und ', $text));
        $text = preg_replace('/[^a-z0-9]+/', ' ', $text);
        return trim(preg_replace('/\s+/', ' ', (string) $text));
    }

    private function idealo_match_stem($token) {
        $token = (string) $token;
        if (strlen($token) < 6) { return $token; }
        foreach (array('ern','em','en','er','es','e','n','s') as $suffix) {
            if ($suffix === 's' && substr($token, -2) === 'ss') { continue; }
            if (substr($token, -strlen($suffix)) === $suffix && strlen($token) - strlen($suffix) >= 5) {
                return substr($token, 0, -strlen($suffix));
            }
        }
        return $token;
    }

    private function idealo_match_tokens($text) {
        static $stop = null;
        if ($stop === null) {
            $stop = array_fill_keys(array('und','oder','der','die','das','den','dem','des','ein','eine','einer','eines','fuer','fur','mit','von','im','in','am','an','zu','zur','zum','bei','auf','aus','neu','gebraucht','set','paar','stueck','stuck','original'), true);
        }
        $out = array();
        foreach (preg_split('/\s+/', $this->idealo_match_normalize($text)) as $token) {
            $token = trim((string) $token);
            if (strlen($token) < 3 || isset($stop[$token])) { continue; }
            $out[] = $token;
        }
        return $out;
    }

    private function idealo_match_primary_tokens($text) {
        static $bounds = null;
        if ($bounds === null) { $bounds = array_fill_keys(array('fur','fuer','for','im','in','am','an','auf','bei','zur','zum','als','passend','geeignet','kompatibel','compatible','fits','mit','with','ohne','without','inkl','inklusive','including','zubehor','zubehoer','accessory','accessories','ersatzteil','ersatzteile'), true); }
        $tokens = $this->idealo_match_tokens($text); $out = array();
        foreach ($tokens as $idx => $token) {
            if (isset($bounds[$token])) { return $idx === 0 ? array() : $out; }
            $out[] = $token;
        }
        return $out;
    }

    private function idealo_match_distinct_tokens($text, $primary = false) {
        static $drop = null;
        if ($drop === null) { $drop = array_fill_keys(array('pferd','pferde','pony','ponys','fohlen','reiter','reiten','reit','reitsport','equestrian','zubehor','zubehoer','artikel','angebot','angebote','produkt','produkte','set','sets','original','universal','neu','gebraucht','damen','herren','kinder','schwarz','braun','blau','rot','grun','gruen','weiss','weis','beige','grosse','groesse','size','cm','mm','kg','stuck','stueck','paar','fur','fuer','mit','ohne'), true); }
        $tokens = $primary ? $this->idealo_match_primary_tokens($text) : $this->idealo_match_tokens($text);
        $out = array();
        foreach ($tokens as $token) { if (!isset($drop[$token])) { $out[$token] = true; } }
        return array_keys($out);
    }

    private function idealo_match_index() {
        static $cache = null;
        if (is_array($cache) || is_wp_error($cache)) { return $cache; }
        $catalog = $this->idealo_portal_supply_catalog();
        if (is_wp_error($catalog)) { return $cache = $catalog; }
        $concepts = array(); $index = array();
        foreach ((array) $catalog['_idealo_required_concepts'] as $id => $concept) {
            $core = $this->idealo_match_distinct_tokens((string) ($concept['title'] ?? ''), true);
            if (!$core) { $core = $this->idealo_match_distinct_tokens((string) ($concept['title'] ?? ''), false); }
            $stems = array(); foreach ($core as $token) { $stems[$this->idealo_match_stem($token)] = true; }
            $stems = array_keys($stems); if (!$stems) { continue; }
            $first_page = is_array(($concept['target_pages'] ?? null)) && !empty($concept['target_pages']) && is_array($concept['target_pages'][0]) ? $concept['target_pages'][0] : array();
            $hub = array(); foreach ($this->idealo_match_distinct_tokens((string) ($first_page['hub'] ?? '')) as $token) { $hub[$this->idealo_match_stem($token)] = true; }
            $main = array(); foreach ($this->idealo_match_distinct_tokens((string) ($first_page['main_hub'] ?? '')) as $token) { $main[$this->idealo_match_stem($token)] = true; }
            $all = array(); foreach ($this->idealo_match_distinct_tokens((string) ($concept['title'] ?? '')) as $token) { $all[$this->idealo_match_stem($token)] = true; }
            $rel = array_values(array_diff(array_keys($all), $stems));
            $entry = array('id'=>$id,'title'=>(string)($concept['title']??''),'stems'=>$stems,'hub_stems'=>array_keys($hub),'main_stems'=>array_keys($main),'rel_stems'=>$rel,'main_hub'=>(string)($first_page['main_hub']??''),'hub'=>(string)($first_page['hub']??''),'target_pages'=>(array)($concept['target_pages']??array()));
            $concepts[$id] = $entry;
            foreach ($stems as $stem) { if (!isset($index[$stem])) { $index[$stem] = array(); } $index[$stem][$id] = true; }
        }
        if (count($concepts) !== 311) { return $cache = new WP_Error('idealo_match_index_incomplete', 'Matcher konnte nicht alle 311 Produktkonzepte binden.'); }
        return $cache = array('concepts'=>$concepts,'index'=>$index,'catalog'=>$catalog);
    }

    private function idealo_text_has_root($text, $roots) {
        foreach ((array) $roots as $root) { if ($root !== '' && strpos((string)$text, (string)$root) !== false) { return true; } }
        return false;
    }

    private function idealo_match_blocked($text, $catalog) {
        static $extras = array('bettdecke','bettdecken','kuscheltier','kuscheltiere','hundefutter','katzenfutter','vogelfutter','vogelhaus','vogelhauser','vogelhaeuser','modelleisenbahn','modellfahrzeug','modellfahrzeuge','rc modellbau','kaffeekapseln','kaffeepads','sanitarinstallation','sanitarinstallationen','netzteil','netzwerkzubehor','netzwerkzubehoer','haushaltsspielzeug','badmobel','badmoebel','sneaker','garagentor','torantrieb','zahnpflege','prothesenbox','plueschtier','pluschtier','gaming und spielen',' cats ',' dogs ',' puppy ',' kitten ');
        $haystack = ' ' . (string) $text . ' ';
        foreach ((array) ($catalog['hard_negative_markers'] ?? array()) as $term) { $term=$this->idealo_match_normalize($term); if ($term!=='' && strpos($haystack, ' '.$term.' ')!==false) { return true; } }
        foreach ($extras as $term) { if (strpos($haystack, (string)$term) !== false) { return true; } }
        return false;
    }

    /** Returns 0 = reject; 1..3 = increasingly strong context evidence. */
    private function idealo_match_context_score($concept, $title_n, $main_n, $sub_n, $catalog) {
        $full = trim($title_n . ' ' . $main_n . ' ' . $sub_n);
        if ($this->idealo_match_blocked($full, $catalog)) { return 0; }
        $strong_roots = array('pferd','pony','fohlen','reit','equestrian','equine','horse','sattel','zaum','halfter','huf','longier','cavaletti','schabrack','gamasch','kappzaum','trense','gebiss','fressbremse','bollengabel','mistboy','stalltafel','pferdedeck');
        $strong = $this->idealo_text_has_root($full, $strong_roots);
        $sub_stems = array(); foreach ($this->idealo_match_tokens($sub_n) as $token) { $sub_stems[$this->idealo_match_stem($token)] = true; }
        $sub_exact = true; foreach ((array)($concept['stems']??array()) as $stem) { if (!isset($sub_stems[$stem])) { $sub_exact=false; break; } }
        $main_hub = (string) ($concept['main_hub'] ?? '');
        if (in_array($main_hub, array('Ausrüstung','Training'), true)) {
            if (!in_array($main_n, array('tierbedarf','sport und outdoor'), true)) { return 0; }
            if ($sub_exact) { return 3; }
            return ($strong || $this->idealo_text_has_root($sub_n,array('pferd','reit','sattel','zaum','tierhaar','bollensammler','stalltafel'))) ? 2 : 0;
        }
        if ($main_hub === 'Gesundheit') {
            if ($main_n === 'tierbedarf') {
                if ($sub_exact) { return 3; }
                return ($strong || $this->idealo_text_has_root($sub_n,array('pferd','tierpflege','tiergesundheit','tierhaar'))) ? 2 : 0;
            }
            if ($main_n === 'drogerie und gesundheit') { return $this->idealo_text_has_root($title_n,array('pferd','pony','fohlen','equine')) ? 2 : 0; }
            return 0;
        }
        if ($main_hub === 'Fütterung') {
            if ($this->idealo_text_has_root($title_n,array('pferd','pony','fohlen','horse','equine')) || strpos($sub_n,'pferdefutter')!==false) { return 3; }
            if ($main_n==='tierbedarf' && ($sub_exact || $this->idealo_text_has_root($title_n,array('weidetrank','thermotrank','heunetz','heubedampf','heurauf','heutasch')))) { return 2; }
            return 0;
        }
        if ($main_hub === 'Stall') {
            if (in_array($main_n,array('tierbedarf','haus und garten'),true) && $sub_exact) { return 3; }
            return ($this->idealo_text_has_root($title_n,array('pferd','pony','fohlen','stall','weideunterstand','boxen','putzplatz','offenstall','paddock')) || $this->idealo_text_has_root($sub_n,array('stalltafel','bollensammler'))) ? 2 : 0;
        }
        if ($main_hub === 'Weide') {
            if (in_array($main_n,array('tierbedarf','haus und garten'),true) && $sub_exact) { return 3; }
            return ($this->idealo_text_has_root($title_n,array('pferd','pony','fohlen','weide','elektrozaun','koppel','paddock')) || $this->idealo_text_has_root($sub_n,array('weidezaun','rasensamen'))) ? 2 : 0;
        }
        if ($main_hub === 'Transport') {
            $hub_n=$this->idealo_match_normalize((string)($concept['hub']??''));
            if ($main_n === 'tierbedarf') { return $this->idealo_text_has_root($title_n,array('pferd','pony','fohlen','reit','sattel','zaum','halfter','gamasch','horse','equine')) ? 3 : 0; }
            if (!in_array($hub_n,array('zugfahrzeug','anhangerpflege'),true)) { return $this->idealo_text_has_root($title_n,array('pferd','pony','fohlen','horse','equine')) ? 2 : 0; }
            if ($main_n === 'auto und motorrad') { return ($sub_exact || $this->idealo_text_has_root($title_n.' '.$sub_n,array('anhang','anhaeng','kupplung','reifendruck','unterlegkeil'))) ? 2 : 0; }
            return 0;
        }
        if ($main_hub === 'Wissen') { return $this->idealo_text_has_root($title_n,array('pferd','pony','fohlen','horse','equine')) ? 2 : 0; }
        return $strong ? 1 : 0;
    }

    /** Conservative one-row matcher: no AI/fuzzy product identity and no cross-provider assumption. */
    private function idealo_match_feed_row_to_concept($row) {
        $mi = $this->idealo_match_index(); if (is_wp_error($mi)) { return $mi; }
        $title = (string) ($row['product_title'] ?? '');
        $primary = $this->idealo_match_primary_tokens($title); if (!$primary) { return array('status'=>'none'); }
        $product_stems = array(); foreach ($primary as $token) { $product_stems[$this->idealo_match_stem($token)] = true; }
        $candidate_ids = array(); foreach (array_keys($product_stems) as $stem) { foreach ((array)($mi['index'][$stem]??array()) as $id=>$true) { $candidate_ids[$id]=true; } }
        if (!$candidate_ids) { return array('status'=>'none'); }
        $title_n=$this->idealo_match_normalize($title); $main_n=$this->idealo_match_normalize((string)($row['main_category']??'')); $sub_n=$this->idealo_match_normalize((string)($row['sub_category']??''));
        $category_stems=array(); foreach ($this->idealo_match_tokens($main_n.' '.$sub_n) as $token) { $category_stems[]=$this->idealo_match_stem($token); }
        $full_title_stems=array(); foreach ($this->idealo_match_tokens($title) as $token) { $full_title_stems[]=$this->idealo_match_stem($token); }
        $scored=array(); $context_rejected=false;
        foreach (array_keys($candidate_ids) as $id) {
            $concept=$mi['concepts'][$id]??null; if (!is_array($concept)) { continue; }
            $all=true; foreach ((array)$concept['stems'] as $stem) { if (!isset($product_stems[$stem])) { $all=false; break; } } if (!$all) { continue; }
            $context=$this->idealo_match_context_score($concept,$title_n,$main_n,$sub_n,$mi['catalog']); if ($context<=0) { $context_rejected=true; continue; }
            $phrase=$this->idealo_match_normalize(implode(' ',$this->idealo_match_primary_tokens((string)$concept['title']))); $pt=$this->idealo_match_normalize(implode(' ',$primary));
            $phrase_title=$phrase!=='' && strpos(' '.$pt.' ',' '.$phrase.' ')!==false;
            $hubhits=0; foreach ((array)$concept['hub_stems'] as $stem) { if (in_array($stem,$category_stems,true)) { $hubhits++; } }
            $mainhits=0; foreach ((array)$concept['main_stems'] as $stem) { if (in_array($stem,$category_stems,true)) { $mainhits++; } }
            $relhits=0; foreach ((array)$concept['rel_stems'] as $stem) { if (in_array($stem,$full_title_stems,true)||in_array($stem,$category_stems,true)) { $relhits++; } }
            $score=($phrase_title?160:0)+(count((array)$concept['stems'])*55)+min(24,$hubhits*8)+min(12,$mainhits*4)+($relhits*20)+($context*35);
            $scored[]=array('score'=>$score,'context'=>$context,'specificity'=>count((array)$concept['stems']),'concept'=>$concept);
        }
        if (!$scored) { return array('status'=>$context_rejected?'context_rejected':'none'); }
        usort($scored,static function($a,$b){ return ($b['score']<=>$a['score']) ?: ($b['specificity']<=>$a['specificity']) ?: ($b['context']<=>$a['context']) ?: strcmp((string)$a['concept']['id'],(string)$b['concept']['id']); });
        if (count($scored)>1 && ((int)$scored[0]['score']-(int)$scored[1]['score'])<30 && (int)$scored[0]['specificity']===(int)$scored[1]['specificity']) { return array('status'=>'ambiguous'); }
        return array('status'=>'matched','concept'=>$scored[0]['concept'],'score'=>(int)$scored[0]['score'],'context'=>(int)$scored[0]['context']);
    }

    public function idealo_provider_access_snapshot($snapshot, $provider, $definition, $contract_version) {
        if ($provider !== 'idealo') { return $snapshot; }
        $settings = $this->idealo_settings(); $state = $this->provider_access_state('idealo');
        $snapshot['configured'] = $this->idealo_credentials_present($settings);
        $snapshot['enabled'] = !empty($settings['enabled']);
        $snapshot['status'] = $snapshot['configured'] ? sanitize_key((string)($state['status'] ?? 'credentials_saved')) : 'not_configured';
        if ($snapshot['configured'] && in_array($snapshot['status'], array('not_configured','prepared'), true)) { $snapshot['status'] = 'credentials_saved'; }
        $snapshot['last_checked'] = absint($state['last_checked'] ?? 0);
        $snapshot['message'] = sanitize_text_field((string)($state['message'] ?? $settings['last_message'] ?? ''));
        return $snapshot;
    }

    public function idealo_provider_access_save($handled, $provider, $raw, $contract_version) {
        if ($provider !== 'idealo') { return $handled; }
        $old = $this->idealo_settings(); $settings = $old;
        $settings['enabled'] = !empty($raw['enabled']);
        if (!$this->idealo_api_key_external()) {
            $new_key = trim((string)($raw['api_key'] ?? ''));
            if ($new_key !== '') { $settings['api_key'] = $new_key; }
            if (!empty($raw['remove_api_key'])) { $settings['api_key'] = ''; }
        }
        $settings['adspace_id'] = preg_replace('/\D+/', '', (string)($raw['adspace_id'] ?? $old['adspace_id'] ?? ''));
        $settings['feed_id'] = '2901';
        $new_feed_url = trim((string)($raw['feed_url'] ?? ''));
        if ($new_feed_url !== '') { $settings['feed_url'] = esc_url_raw($new_feed_url); }
        if (!empty($raw['remove_feed_url'])) { $settings['feed_url'] = ''; }
        $settings['output_mode'] = $this->idealo_sanitize_output_mode($raw['output_mode'] ?? $old['output_mode'] ?? 'ebay_only');
        $settings['link_strategy'] = $this->idealo_sanitize_link_strategy($raw['link_strategy'] ?? $old['link_strategy'] ?? 'hybrid');
        $settings['auto_refresh'] = !empty($raw['auto_refresh']);
        update_option(self::OPTION_NETWORK_IDEALO, $settings, false);
        $this->idealo_sync_campaign_activation();
        $this->idealo_ensure_refresh_schedule();
        $saved = $this->idealo_settings();
        if (!$this->idealo_credentials_present($saved)) {
            $this->provider_set_access_state('idealo', 'not_configured', 'idealo-Zugang noch unvollständig.');
            return $saved;
        }
        $this->provider_set_access_state('idealo', 'credentials_saved', 'idealo-Zugang gespeichert; Provider bleibt vom eBay-Workflow getrennt.');
        return $saved;
    }

    public function idealo_provider_access_test($handled, $provider, $contract_version) {
        if ($provider !== 'idealo') { return $handled; }
        $settings = $this->idealo_settings();
        if (!$this->idealo_credentials_present($settings)) { return new WP_Error('idealo_credentials_missing', 'API-Key, Adspace-ID und Feed-ID müssen vollständig gespeichert sein.'); }
        $metadata = $this->idealo_find_feed_metadata($settings);
        if (is_wp_error($metadata)) { $this->provider_set_access_state('idealo', 'failed', $metadata->get_error_message()); return $metadata; }
        $settings['api_last_checked_at'] = time();
        $settings['api_last_feed_hash'] = (string)($metadata['last_file_hash'] ?? '');
        $settings['api_last_updated_at'] = (string)($metadata['last_updated_at'] ?? '');
        $settings['api_last_product_count'] = absint($metadata['number_of_products'] ?? 0);
        $settings['api_last_advertiser_name'] = sanitize_text_field((string)($metadata['advertiser_name'] ?? ''));
        $settings['api_last_message'] = 'Partner-API PASS: Feed ' . (string)($settings['feed_id'] ?? '') . ' gefunden.';
        update_option(self::OPTION_NETWORK_IDEALO, $settings, false);
        $message = 'idealo-Partner-API PASS: Feed ' . (string)$settings['feed_id'] . ' für Adspace ' . (string)$settings['adspace_id'] . ' gefunden';
        if (!empty($metadata['number_of_products'])) { $message .= ' (' . absint($metadata['number_of_products']) . ' Produkte)'; }
        $message .= '.';
        $this->provider_set_access_state('idealo', 'connected', $message);
        return array('status'=>'connected','message'=>$message,'metadata'=>$metadata);
    }

    private function idealo_validate_feed_url($url) {
        $url = trim((string)$url);
        if ($url === '' || !wp_http_validate_url($url)) { return new WP_Error('idealo_feed_url_missing', 'Es ist noch keine vom iPN erzeugte Feed-URL gespeichert.'); }
        $parts = wp_parse_url($url);
        if (strtolower((string)($parts['scheme'] ?? '')) !== 'https' || empty($parts['host'])) { return new WP_Error('idealo_feed_url_invalid', 'Die idealo-Feed-URL muss eine gültige HTTPS-Adresse sein.'); }
        $host = strtolower((string)$parts['host']);
        $allowed = $host === 'api.net.idealo-partner.com' || substr($host, -strlen('.idealo-partner.com')) === '.idealo-partner.com' || $host === 'api.ingenious.cloud' || substr($host, -strlen('.ingenious.cloud')) === '.ingenious.cloud';
        if (!$allowed) { return new WP_Error('idealo_feed_url_blocked', 'Die Feed-Adresse muss von der offiziellen idealo/iPN-Domain stammen.'); }
        return esc_url_raw($url);
    }

    private function idealo_download_feed_to_temp($settings) {
        $url = $this->idealo_validate_feed_url((string)($settings['feed_url'] ?? ''));
        if (is_wp_error($url)) { return $url; }
        $tmp = wp_tempnam('ppar-idealo-feed');
        if (!$tmp) { return new WP_Error('idealo_temp_failed', 'Temporäre Datei konnte nicht angelegt werden.'); }
        $headers = array('Accept'=>'text/csv,application/octet-stream,application/gzip,*/*');
        if (!empty($settings['feed_etag'])) { $headers['If-None-Match'] = (string)$settings['feed_etag']; }
        if (!empty($settings['feed_last_modified'])) { $headers['If-Modified-Since'] = (string)$settings['feed_last_modified']; }
        $response = wp_safe_remote_get($url, array('timeout'=>300,'redirection'=>3,'stream'=>true,'filename'=>$tmp,'headers'=>$headers));
        if (is_wp_error($response)) { @unlink($tmp); return $response; }
        $code = (int)wp_remote_retrieve_response_code($response);
        if ($code === 304) { @unlink($tmp); return array('status'=>'not_modified','path'=>'','code'=>304,'etag'=>(string)wp_remote_retrieve_header($response,'etag'),'last_modified'=>(string)wp_remote_retrieve_header($response,'last-modified')); }
        if ($code === 429) { @unlink($tmp); return new WP_Error('idealo_feed_rate_limited', 'idealo-Feed meldet HTTP 429; Aktualisierung wird später erneut versucht.'); }
        if ($code < 200 || $code >= 300) { @unlink($tmp); return new WP_Error('idealo_feed_http_' . $code, 'idealo-Feed antwortet mit HTTP ' . $code . '.'); }
        return array('status'=>'downloaded','path'=>$tmp,'code'=>$code,'etag'=>(string)wp_remote_retrieve_header($response,'etag'),'last_modified'=>(string)wp_remote_retrieve_header($response,'last-modified'));
    }

    private function idealo_open_feed_stream($path) {
        $fh = @fopen($path, 'rb'); if (!$fh) { return new WP_Error('idealo_feed_open_failed', 'Feed-Datei konnte nicht geöffnet werden.'); }
        $magic = fread($fh, 2); fclose($fh);
        if ($magic === "\x1f\x8b") { if (!function_exists('gzopen')) { return new WP_Error('idealo_gzip_missing', 'PHP-GZIP-Unterstützung fehlt.'); } $gz=@gzopen($path,'rb'); return $gz ?: new WP_Error('idealo_gzip_open_failed','GZIP-Feed konnte nicht geöffnet werden.'); }
        $plain=@fopen($path,'rb'); return $plain ?: new WP_Error('idealo_feed_open_failed','CSV-Feed konnte nicht geöffnet werden.');
    }

    private function idealo_stream_close($stream) {
        if (!is_resource($stream)) { return; }
        $meta=stream_get_meta_data($stream); if (strtoupper((string)($meta['stream_type'] ?? '')) === 'ZLIB') { gzclose($stream); } else { fclose($stream); }
    }

    private function idealo_normalize_gtins_from_values($values) {
        // Never use a raw numeric GTIN as an array key: PHP coerces numeric-string
        // keys to integers and would therefore destroy significant leading zeroes.
        $out=array();
        foreach ((array)$values as $value) {
            foreach (preg_split('/[^0-9]+/', (string)$value) as $part) {
                $part=trim($part); if (in_array(strlen($part), array(8,12,13,14), true)) { $out['g:'.$part]=$part; }
            }
        }
        return array_values($out);
    }

    private function idealo_normalize_asins_from_values($values) {
        $out=array();
        foreach ((array)$values as $value) {
            foreach (preg_split('/[^0-9A-Za-z]+/', strtoupper((string)$value)) as $part) {
                $part=trim($part); if (preg_match('/^[A-Z0-9]{10}$/', $part)) { $out['a:'.$part]=$part; }
            }
        }
        return array_values($out);
    }

    private function idealo_import_feed_file($path, $source_label = 'iPN Standard Datafeed 2901') {
        if (!file_exists($path)) { return new WP_Error('idealo_feed_missing', 'Feed-Datei fehlt.'); }
        @set_time_limit(0); if (function_exists('ignore_user_abort')) { @ignore_user_abort(true); }
        $stream=$this->idealo_open_feed_stream($path); if (is_wp_error($stream)) { return $stream; }
        $headers=fgetcsv($stream,0,',','"','\\');
        if (!is_array($headers)) { $this->idealo_stream_close($stream); return new WP_Error('idealo_header_missing','Feed hat keine Kopfzeile.'); }
        if (isset($headers[0])) { $headers[0]=preg_replace('/^\xEF\xBB\xBF/','',(string)$headers[0]); }
        $headers=array_map('trim',$headers);
        $required=array('id','product_title','product_deeplink','ean','gtins_product','asins_product','main_category','sub_category','brand_name');
        $missing=array_values(array_diff($required,$headers));
        $image_field=in_array('image_url',$headers,true)?'image_url':(in_array('image_url_1',$headers,true)?'image_url_1':'');
        if ($image_field==='') { $missing[]='image_url|image_url_1'; }
        if ($missing) { $this->idealo_stream_close($stream); return new WP_Error('idealo_required_columns_missing','idealo-Feedspalten fehlen: '.implode(', ',$missing)); }
        $mi=$this->idealo_match_index(); if (is_wp_error($mi)) { $this->idealo_stream_close($stream); return $mi; }
        $rows=array(); $seen=0; $malformed=0; $ambiguous=0; $context_rejected=0; $matched_concepts=array(); $matched_hubs=array();
        while (($values=fgetcsv($stream,0,',','"','\\')) !== false) {
            $seen++; if (count($values)!==count($headers)) { $malformed++; continue; }
            $row=array_combine($headers,$values); if (!$row) { $malformed++; continue; }
            if (trim((string)($row['product_title']??''))==='' || trim((string)($row['product_deeplink']??''))==='' || trim((string)($row[$image_field]??''))==='') { continue; }
            $gtins=$this->idealo_normalize_gtins_from_values(array($row['ean']??'',$row['gtins_product']??'')); if (!$gtins) { continue; }
            $match=$this->idealo_match_feed_row_to_concept($row); if (is_wp_error($match)) { $this->idealo_stream_close($stream); return $match; }
            $status=(string)($match['status']??'none'); if ($status==='ambiguous') { $ambiguous++; continue; } if ($status==='context_rejected') { $context_rejected++; continue; } if ($status!=='matched' || !is_array($match['concept']??null)) { continue; }
            $concept=$match['concept']; $concept_id=sanitize_key((string)($concept['id']??'')); if ($concept_id==='') { continue; }
            $row['__idealo_concept_id']=$concept_id; $row['__idealo_match_score']=(string)absint($match['score']??0); $row['__idealo_context_score']=(string)absint($match['context']??0); $row['__currency_eur']='EUR'; $row['__programme_external_id']='84749'; $row['__programme_name']='idealo DE'; $row['__price']=isset($row['price'])?(string)$row['price']:''; $row['__image_url']=$this->idealo_direct_image_url((string)$row[$image_field]); if ($row['__image_url']==='') { continue; }
            $rows[]=$row; $matched_concepts[$concept_id]=true; $matched_hubs[(string)($concept['main_hub']??'').'|'.(string)($concept['hub']??'')]=true;
        }
        $this->idealo_stream_close($stream);
        if (!$rows) { return new WP_Error('idealo_no_matching_rows','Standardfeed enthält nach dem 311er-Portalabgleich keine sicher zuordenbaren Produkte.'); }
        $mapping=array(
            'external_id'=>array('source'=>'id'),'programme_external_id'=>array('source'=>'__programme_external_id'),'programme_name'=>array('source'=>'__programme_name'),
            'title'=>array('source'=>'product_title'),'image_url'=>array('source'=>'__image_url'),'tracking_url'=>array('source'=>'product_deeplink'),
            'destination_url'=>array('source'=>'product_deeplink'),'price'=>array('source'=>'__price'),'currency'=>array('source'=>'__currency_eur'),
            'brand'=>array('source'=>'brand_name'),'category'=>array('source'=>'__idealo_concept_id'),
        );
        $parsed=array('headers'=>array_merge($headers,array('__idealo_concept_id','__idealo_match_score','__idealo_context_score','__currency_eur','__programme_external_id','__programme_name','__price','__image_url')),'mapping'=>$mapping,'delimiter'=>',','rows'=>$rows);
        $import_started_at=time(); $counts=$this->network_sync_upsert_products('idealo',$parsed); $hash=hash_file('sha256',$path); $settings=$this->idealo_settings();
        $settings['last_feed_hash']=$hash?:''; $settings['last_import_started_at']=$import_started_at; $settings['last_import_at']=time(); $settings['last_import_count']=count($rows); $settings['last_matched_concepts']=count($matched_concepts); $settings['last_matched_hubs']=count(array_filter(array_keys($matched_hubs),static function($v){return trim((string)$v,'|')!=='';})); $settings['last_ambiguous_count']=$ambiguous; $settings['last_context_rejected_count']=$context_rejected;
        $settings['last_message']=sprintf('%s: %d sichere Produkte, %d/311 Produktkonzepte und %d/59 Hub-Familien; %d Feedzeilen geprüft; %d fehlerhaft; %d mehrdeutig verworfen.',$source_label,count($rows),count($matched_concepts),absint($settings['last_matched_hubs']),$seen,$malformed,$ambiguous);
        update_option(self::OPTION_NETWORK_IDEALO,$settings,false);
        $materialized=$this->idealo_materialize_campaigns(); $settings=$this->idealo_settings();
        if (!is_wp_error($materialized)) { $settings['last_materialized_at']=time(); $settings['last_materialized_count']=absint($materialized['campaigns']??0); $settings['last_materialized_targets']=absint($materialized['targets']??0); update_option(self::OPTION_NETWORK_IDEALO,$settings,false); }
        $this->provider_set_access_state('idealo',$this->idealo_credentials_present($settings)?'connected':'not_configured',$settings['last_message']);
        return array('status'=>'success','message'=>'idealo-Standardfeed wurde providerisoliert gegen den vollständigen 311er-Portalvertrag geprüft.','counts'=>$counts,'details'=>array('feed_rows_seen'=>$seen,'matching_rows'=>count($rows),'matched_concepts'=>count($matched_concepts),'matched_hubs'=>absint($settings['last_matched_hubs']),'ambiguous_rows'=>$ambiguous,'context_rejected_rows'=>$context_rejected,'malformed_rows'=>$malformed,'source_headers'=>$headers,'required_columns'=>$required,'feed_sha256'=>$hash,'public_activation'=>$this->idealo_campaigns_should_be_active(),'materialized'=>is_wp_error($materialized)?array('error'=>$materialized->get_error_message()):$materialized));
    }

    private function idealo_target_keys_for_product_slug($product_slug) {
        $product_slug=sanitize_title((string)$product_slug); if ($product_slug==='') { return array(); }
        $keys=array('page:'.$product_slug); $catalog=$this->idealo_portal_supply_catalog();
        if (!is_wp_error($catalog)) {
            foreach ((array)($catalog['product_targets']??array()) as $page) {
                if (!is_array($page)||sanitize_title((string)($page['slug']??''))!==$product_slug) { continue; }
                foreach (array('slug','hub_slug','main_slug') as $field) { $slug=sanitize_title((string)($page[$field]??'')); if ($slug!=='') { $keys[]='page:'.$slug; } }
            }
            foreach ((array)($catalog['article_targets']??array()) as $article) {
                if (!is_array($article)||sanitize_title((string)($article['product_slug']??''))!==$product_slug) { continue; }
                $slug=sanitize_title((string)($article['category_slug']??'')); if ($slug!=='') { $keys[]='category:'.$slug; }
            }
        }
        return array_values(array_unique($keys));
    }

    private function idealo_target_keys_for_concept($concept) {
        $keys=array();
        foreach ((array)($concept['target_pages']??array()) as $page) {
            if (!is_array($page)) { continue; }
            $slug=sanitize_title((string)($page['slug']??'')); if ($slug==='') { continue; }
            $keys=array_merge($keys,$this->idealo_target_keys_for_product_slug($slug));
            foreach (array('hub_slug','main_slug') as $field) { $v=sanitize_title((string)($page[$field]??'')); if ($v!=='') { $keys[]='page:'.$v; } }
        }
        return array_values(array_unique($keys));
    }

    private function idealo_comparison_query_for_concept($concept) {
        $title = trim((string)($concept['title'] ?? ''));
        if ($title === '') { return ''; }
        $main = trim((string)($concept['main_hub'] ?? ''));
        $normalized = $this->idealo_match_normalize($title);
        $horse_roots = array('pferd','pony','fohlen','reit','sattel','trense','halfter','huf','weide','stall','longier','cavaletti','schabrack','gamasch','zaum');
        if ($this->idealo_text_has_root($normalized, $horse_roots)) { return $title; }
        if ($main === 'Stall') { return $title . ' Pferdestall'; }
        if ($main === 'Weide') { return $title . ' Pferdeweide'; }
        if ($main === 'Transport') { return $title . ' Pferdeanhänger'; }
        if (in_array($main, array('Ausrüstung','Fütterung','Gesundheit','Training'), true)) { return $title . ' Pferd'; }
        return $title;
    }

    private function idealo_comparison_target_url($concept) {
        $query = $this->idealo_comparison_query_for_concept($concept);
        if ($query === '') { return ''; }
        return 'https://www.idealo.de/preisvergleich/MainSearchProductCategory.html?q=' . rawurlencode($query);
    }

    private function idealo_comparison_deeplink_from_product_url($product_url, $concept) {
        $product_url = (string)$product_url;
        $parts = wp_parse_url($product_url);
        if (!is_array($parts) || strtolower((string)($parts['scheme'] ?? '')) !== 'https' || strtolower((string)($parts['host'] ?? '')) !== 'ipn.idealo.de') { return ''; }
        $target = $this->idealo_comparison_target_url($concept); if ($target === '') { return ''; }
        $query = array(); if (!empty($parts['query'])) { parse_str((string)$parts['query'], $query); }
        // Feed product links carry pid=<product-id>. A family/search deeplink is
        // deliberately not a product claim, so remove that product-specific
        // parameter and keep the partner/adspace tracking part intact.
        unset($query['pid']);
        $query['rmd'] = '3'; $query['trg'] = $target;
        $path = (string)($parts['path'] ?? ''); if ($path === '') { return ''; }
        return esc_url_raw('https://ipn.idealo.de' . $path . '?' . http_build_query($query, '', '&', PHP_QUERY_RFC3986));
    }

    private function idealo_campaign_surface_kind($campaign) {
        if (!is_array($campaign) || sanitize_key((string)($campaign['network'] ?? '')) !== 'idealo') { return ''; }
        $source = sanitize_key((string)($campaign['source'] ?? ''));
        if ($source === 'idealo_family_deeplink_v1') { return 'comparison'; }
        if ($source === 'idealo_product_feed_v1') { return 'product'; }
        return sanitize_key((string)($campaign['idealo_surface_kind'] ?? ''));
    }

    public function idealo_standalone_campaign_allowed($campaign, $slot_type = '') {
        if (!is_array($campaign) || sanitize_key((string)($campaign['network'] ?? '')) !== 'idealo') { return true; }
        $kind = $this->idealo_campaign_surface_kind($campaign); $strategy = $this->idealo_link_strategy();
        if ($strategy === 'products') { return $kind === 'product'; }
        if ($strategy === 'comparison') { return $kind === 'comparison'; }
        // Hybrid: idealo is a family/category comparison when it stands alone.
        // Exact concrete idealo offers remain available only as an additional
        // button on an already selected concrete product via exact GTIN.
        return $kind === 'comparison';
    }

    private function idealo_campaigns_should_be_active() {
        $s=$this->idealo_settings();
        return !empty($s['enabled']) && in_array($this->idealo_sanitize_output_mode($s['output_mode'] ?? ''),array('idealo_only','separate','combined','automatic'),true);
    }

    public function idealo_campaign_publicly_allowed($campaign) {
        if (!is_array($campaign) || sanitize_key((string)($campaign['network'] ?? ''))!=='idealo') { return false; }
        $source=sanitize_key((string)($campaign['source'] ?? '')); $kind=$this->idealo_campaign_surface_kind($campaign);
        $strategy=$this->idealo_link_strategy(); $mode=$this->idealo_output_mode();
        if ($source==='idealo_product_feed_v1') {
            if ($strategy==='comparison' || ($strategy==='hybrid' && $mode==='idealo_only')) { return false; }
            if (sanitize_key((string)($campaign['product_provider'] ?? '')) !== 'idealo' || sanitize_key((string)($campaign['product_identity_source'] ?? '')) !== 'gtin') { return false; }
            if (!$this->idealo_normalize_gtins_from_values((array)($campaign['product_gtins'] ?? array()))) { return false; }
        } elseif ($source==='idealo_family_deeplink_v1') {
            if ($strategy==='products') { return false; }
            if ($kind!=='comparison' || sanitize_key((string)($campaign['product_provider'] ?? ''))!=='idealo') { return false; }
            $url=(string)($campaign['url']??''); $parts=wp_parse_url($url); if (!is_array($parts) || strtolower((string)($parts['host']??''))!=='ipn.idealo.de') { return false; }
            $q=array(); if (!empty($parts['query'])) { parse_str((string)$parts['query'],$q); } $target=wp_parse_url((string)($q['trg']??'')); if (!is_array($target) || strtolower((string)($target['scheme']??''))!=='https' || !in_array(strtolower((string)($target['host']??'')),array('idealo.de','www.idealo.de'),true)) { return false; }
        } else { return false; }
        if (empty($campaign['automation_target_keys']) || empty($campaign['placements'])) { return false; }
        $s=$this->idealo_settings(); if (!$this->idealo_campaigns_should_be_active()) { return false; }
        $last=absint($s['last_import_at'] ?? 0); if ($last<=0 || (time()-$last) > 48*HOUR_IN_SECONDS) { return false; }
        return true;
    }

    private function idealo_payload_rank_tuple($payload,$external_key) {
        $context=is_numeric($payload['__idealo_context_score']??null)?(float)$payload['__idealo_context_score']:0.0;
        $match=is_numeric($payload['__idealo_match_score']??null)?(float)$payload['__idealo_match_score']:0.0;
        $top=isset($payload['top10_in_category']) && is_numeric($payload['top10_in_category']) ? (float)$payload['top10_in_category'] : 999999.0;
        $pop=isset($payload['popularity_value']) && is_numeric($payload['popularity_value']) ? (float)$payload['popularity_value'] : 0.0;
        return array(-$context,-$match,$top,-$pop,(string)$external_key);
    }

    private function idealo_materialize_campaigns($limit_per_target=12) {
        if (!function_exists('get_posts')) { return new WP_Error('idealo_campaign_runtime_missing','WordPress-Kampagnenruntime fehlt.'); }
        $mi=$this->idealo_match_index(); if (is_wp_error($mi)) { return $mi; }
        $concept_map=$mi['concepts']; global $wpdb; $table=$this->network_sync_table('products'); $settings=$this->idealo_settings(); $snapshot_started=absint($settings['last_import_started_at']??0);
        $sql="SELECT * FROM {$table} WHERE network='idealo' AND quality_status='pass'"; $args=array(); if ($snapshot_started>0) { $sql.=' AND last_seen >= %d'; $args[]=$snapshot_started; } $sql.=' ORDER BY category ASC, id ASC';
        $prepared=$args?call_user_func_array(array($wpdb,'prepare'),array_merge(array($sql),$args)):$sql; $rows=(array)$wpdb->get_results($prepared,ARRAY_A); $groups=array();
        foreach ($rows as $row) { $concept_id=sanitize_key((string)($row['category']??'')); if (!isset($concept_map[$concept_id])) { continue; } $payload=json_decode((string)($row['payload']??''),true); $payload=is_array($payload)?$payload:array(); if (sanitize_key((string)($payload['__idealo_concept_id']??''))!==$concept_id) { continue; } $row['_payload']=$payload; $row['_rank']=$this->idealo_payload_rank_tuple($payload,(string)($row['external_key']??'')); $groups[$concept_id][]=$row; }
        $selected_keys=array(); $saved_count=0; $targets=0; $should_active=$this->idealo_campaigns_should_be_active();
        foreach ($groups as $concept_id=>$items) {
            $concept=$concept_map[$concept_id]; usort($items,static function($a,$b){ return $a['_rank']<=>$b['_rank']; }); if (!$items) { continue; }
            $target_keys=$this->idealo_target_keys_for_concept($concept); if (!$target_keys) { continue; } $targets++;
            // One family/search comparison campaign per safe concept. It uses a
            // real iPN click URL from the same concept and only overrides trg,
            // exactly as the documented deeplink mechanism permits.
            $family_row=array();
            foreach ($items as $family_candidate) {
                $candidate_image=esc_url_raw((string)($family_candidate['image_url']??''));
                $candidate_tracking=esc_url_raw((string)($family_candidate['tracking_url']??''));
                if ($candidate_image!=='' && stripos($candidate_image,'https://')===0 && $candidate_tracking!=='') { $family_row=(array)$family_candidate; break; }
            }
            if (!$family_row) { continue; }
            $family_payload=(array)($family_row['_payload']??array());
            $family_image=esc_url_raw((string)($family_row['image_url']??''));
            $family_url=$this->idealo_comparison_deeplink_from_product_url((string)($family_row['tracking_url']??''),$concept);
            if ($family_url!=='' && $family_image!=='') {
                $family_key='family:'.$concept_id; $ids=get_posts(array('post_type'=>self::CAMPAIGN_POST_TYPE,'post_status'=>array('publish','draft','private'),'meta_key'=>'_ppar_idealo_external_key','meta_value'=>$family_key,'posts_per_page'=>1,'fields'=>'ids')); $family_post_id=$ids?absint($ids[0]):0;
                $family=$this->central_blank_campaign(); $family['id']=sanitize_key('idealo-family-'.substr(hash('sha256',$concept_id),0,20)); $family['name']='idealo Vergleich – '.(string)$concept['title']; $family['partner']='idealo'; $family['creative_type']='product'; $family['network']='idealo';
                $family['advertiser_id']='84749'; $family['programme_name']='idealo DE'; $family['programme_status']='active'; $family['programme_status_source']='idealo_ipn_feed'; $family['programme_status_checked_at']=time(); $family['quality_manual_status']='auto_verified'; $family['quality_note']='Familien-/Kategorievergleich aus sicher gemapptem Standardfeed-Konzept; repräsentatives Bild aus derselben Produktfamilie, kein konkretes Produktversprechen.'; $family['render_mode']='image_link';
                $family['active']=$should_active; $family['assignment_mode']='page_tree'; $family['match_descendants']=false; $family['automation_target_keys']=$target_keys; $family['placements']=array('hub_product_1','hub_product_2','hub_product_3','category_product_1','category_product_2','category_product_3','post_bottom_products');
                $family['priority']=97; $family['label']='idealo · Affiliate'; $family['title']=(string)$concept['title']; $family['description']='Preise und Angebote bei idealo vergleichen'; $family['button_text']='Bei idealo vergleichen'; $family['image_url']=$family_image; $family['url']=$family_url; $family['target']='_blank'; $family['price']=''; $family['currency']='EUR'; $family['availability']=''; $family['health_check_enabled']=false; $family['source']='idealo_family_deeplink_v1'; $family['last_synced']=absint($family_row['last_seen']??time()); $family['external_id']=$family_key; $family['product_gtins']=array(); $family['product_asins']=array(); $family['product_identity_source']='family'; $family['product_provider']='idealo'; $family['idealo_surface_kind']='comparison';
                $saved=$this->save_campaign_record($family,$family_post_id); if (!is_wp_error($saved)&&$saved) { $family_post_id=absint($saved); update_post_meta($family_post_id,'_ppar_idealo_auto',1); update_post_meta($family_post_id,'_ppar_idealo_external_key',$family_key); update_post_meta($family_post_id,'_ppar_idealo_concept_id',$concept_id); $selected_keys[$family_key]=true; $saved_count++; }
            }
            $target_limit=max(1,min(25,absint($limit_per_target))); $target_saved=0; $seen_target_gtins=array();
            foreach ($items as $row) {
                if ($target_saved >= $target_limit) { break; }
                $payload=(array)$row['_payload']; $external_key=substr(sanitize_text_field((string)($row['external_key']??'')),0,191); if ($external_key==='') { continue; }
                $tracking=esc_url_raw((string)($row['tracking_url']??'')); $title=sanitize_text_field((string)($row['title']??'')); $image=esc_url_raw((string)($row['image_url']??'')); if ($tracking===''||$title===''||$image==='') { continue; }
                $gtins=$this->idealo_normalize_gtins_from_values(array($payload['ean']??'',$payload['gtins_product']??'')); $asins=$this->idealo_normalize_asins_from_values(array($payload['asins_product']??'')); if (!$gtins) { continue; }
                if (array_intersect($gtins,array_keys($seen_target_gtins))) { continue; }
                $ids=get_posts(array('post_type'=>self::CAMPAIGN_POST_TYPE,'post_status'=>array('publish','draft','private'),'meta_key'=>'_ppar_idealo_external_key','meta_value'=>$external_key,'posts_per_page'=>1,'fields'=>'ids')); $post_id=$ids?absint($ids[0]):0;
                $campaign=$this->central_blank_campaign(); $campaign['id']=sanitize_key('idealo-'.substr(hash('sha256',$external_key),0,20)); $campaign['name']='idealo – '.$title; $campaign['partner']='idealo'; $campaign['creative_type']='product'; $campaign['network']='idealo';
                $campaign['advertiser_id']='84749'; $campaign['programme_name']='idealo DE'; $campaign['programme_status']='active'; $campaign['programme_status_source']='idealo_ipn_feed'; $campaign['programme_status_checked_at']=time(); $campaign['quality_manual_status']='auto_verified'; $campaign['quality_note']='311er-Portalvertrag + konservatives Kontextmatching + GTIN.'; $campaign['render_mode']='image_link';
                $campaign['active']=$should_active; $campaign['assignment_mode']='page_tree'; $campaign['match_descendants']=false; $campaign['automation_target_keys']=$target_keys; $campaign['placements']=array('hub_product_1','hub_product_2','hub_product_3','category_product_1','category_product_2','category_product_3','post_bottom_products');
                $rank=$row['_rank']; $match_score=isset($payload['__idealo_match_score'])?(int)$payload['__idealo_match_score']:0; $campaign['priority']=max(40,min(95,55+(int)min(40,floor($match_score/10)))); $campaign['label']='idealo · Affiliate'; $campaign['title']=$title; $campaign['description']=''; $campaign['button_text']='Bei idealo vergleichen';
                $campaign['image_url']=$image; $campaign['url']=$tracking; $campaign['target']='_blank'; $campaign['price']=sanitize_text_field((string)($row['price']??'')); $campaign['currency']='EUR'; $campaign['availability']='available'; $campaign['health_check_enabled']=false; $campaign['source']='idealo_product_feed_v1'; $campaign['last_synced']=absint($row['last_seen']??time()); $campaign['external_id']=$external_key; $campaign['product_gtins']=$gtins; $campaign['product_asins']=$asins; $campaign['product_identity_source']='gtin'; $campaign['product_provider']='idealo'; $campaign['idealo_surface_kind']='product';
                $saved=$this->save_campaign_record($campaign,$post_id); if (is_wp_error($saved)||!$saved) { continue; }
                $post_id=absint($saved); update_post_meta($post_id,'_ppar_idealo_auto',1); update_post_meta($post_id,'_ppar_idealo_external_key',$external_key); update_post_meta($post_id,'_ppar_idealo_concept_id',$concept_id); update_post_meta($post_id,'_ppar_idealo_target_slugs',wp_json_encode(array_values(array_unique(array_filter(array_map(static function($p){return is_array($p)?sanitize_title((string)($p['slug']??'')):'';},(array)($concept['target_pages']??array())))))));
                delete_post_meta($post_id,'_ppar_product_gtin'); foreach ($gtins as $gtin) { add_post_meta($post_id,'_ppar_product_gtin',$gtin,false); } delete_post_meta($post_id,'_ppar_product_asin'); foreach ($asins as $asin) { add_post_meta($post_id,'_ppar_product_asin',$asin,false); }
                foreach ($gtins as $gtin) { $seen_target_gtins[$gtin]=true; } $selected_keys[$external_key]=true; $saved_count++; $target_saved++;
            }
        }
        $existing=get_posts(array('post_type'=>self::CAMPAIGN_POST_TYPE,'post_status'=>array('publish','draft','private'),'meta_key'=>'_ppar_idealo_auto','meta_value'=>'1','posts_per_page'=>-1,'fields'=>'ids')); $retired=0;
        foreach ((array)$existing as $id) { $id=absint($id); $key=(string)get_post_meta($id,'_ppar_idealo_external_key',true); $campaign=$this->campaign_from_post(get_post($id)); if (!$campaign) { continue; } $desired=!empty($selected_keys[$key])&&$should_active; if ((bool)$campaign['active']!==$desired) { $campaign['active']=$desired; $this->save_campaign_record($campaign,$id); if (!$desired) { $retired++; } } }
        $this->idealo_sync_campaign_activation();
        if ($saved_count>0 && method_exists($this,'article_plan_bump_campaign_revision')) { $this->article_plan_bump_campaign_revision('idealo_materialized'); }
        return array('campaigns'=>$saved_count,'targets'=>$targets,'retired'=>$retired,'contract_concepts'=>311,'strategy'=>$this->idealo_link_strategy());
    }

    private function idealo_sync_campaign_activation() {
        if (!function_exists('get_posts')) { return; }
        $active=$this->idealo_campaigns_should_be_active();
        $ids=get_posts(array('post_type'=>self::CAMPAIGN_POST_TYPE,'post_status'=>array('publish','draft','private'),'meta_key'=>'_ppar_idealo_auto','meta_value'=>'1','posts_per_page'=>-1,'fields'=>'ids'));
        foreach ((array)$ids as $id) { $campaign=$this->campaign_from_post(get_post(absint($id))); if (!$campaign) { continue; } $desired=$active && $this->idealo_campaign_publicly_allowed(array_merge($campaign,array('active'=>true))); if ((bool)$campaign['active']!==$desired) { $campaign['active']=$desired; $this->save_campaign_record($campaign,absint($id)); } }
    }

    public function idealo_maybe_upgrade_materialization() {
        if ((string)get_option(self::IDEALO_SCHEMA_OPTION,'0')==='5') { return; }
        $s=$this->idealo_settings();
        if ((string)($s['feed_id']??'')==='2747' || trim((string)($s['feed_id']??''))==='') { $s['feed_id']='2901'; }
        if (strpos((string)($s['feed_url']??''),'feedId=2747')!==false || strpos((string)($s['feed_url']??''),'feedid=2747')!==false) { $s['feed_url']=''; }
        $s['link_strategy']=$this->idealo_sanitize_link_strategy($s['link_strategy']??'hybrid');
        update_option(self::OPTION_NETWORK_IDEALO,$s,false);
        // Re-materialize the existing last-good idealo snapshot once so an upgrade
        // to the hybrid strategy does not create an avoidable visibility gap while
        // the first full 2901 refresh is still pending.
        $mat=$this->idealo_materialize_campaigns();
        update_option(self::IDEALO_SCHEMA_OPTION,'5',false); $this->idealo_sync_campaign_activation();
    }


    public function idealo_cron_schedules($schedules) {
        if (!isset($schedules['ppar_twelve_hours'])) { $schedules['ppar_twelve_hours']=array('interval'=>12*HOUR_IN_SECONDS,'display'=>'Alle zwölf Stunden'); }
        return $schedules;
    }

    public function idealo_ensure_refresh_schedule() {
        if (!function_exists('wp_next_scheduled')||!function_exists('wp_schedule_event')) { return; }
        $s=$this->idealo_settings(); $wanted=!empty($s['enabled'])&&!empty($s['auto_refresh'])&&trim((string)$s['feed_url'])!==''&&$this->idealo_credentials_present($s);
        $next=wp_next_scheduled(self::IDEALO_REFRESH_HOOK);
        if (!$wanted) { if ($next&&function_exists('wp_clear_scheduled_hook')) { wp_clear_scheduled_hook(self::IDEALO_REFRESH_HOOK); } return; }
        if (!$next) { wp_schedule_event(time()+300,'ppar_twelve_hours',self::IDEALO_REFRESH_HOOK); }
    }

    private function idealo_refresh_lock_acquire() {
        if (get_transient(self::IDEALO_REFRESH_LOCK)) { return false; }
        set_transient(self::IDEALO_REFRESH_LOCK, (string)time(), 45 * MINUTE_IN_SECONDS);
        return true;
    }

    private function idealo_refresh_lock_release() {
        delete_transient(self::IDEALO_REFRESH_LOCK);
    }

    private function idealo_set_refresh_state($state, $message = '') {
        $s=$this->idealo_settings();
        $previous=sanitize_key((string)($s['refresh_state']??'idle'));
        $s['refresh_state']=sanitize_key((string)$state);
        $s['refresh_last_message']=sanitize_text_field((string)$message);
        if ($state==='queued' && ($previous!=='queued' || empty($s['refresh_requested_at']))) { $s['refresh_requested_at']=time(); }
        if ($state==='running') { $s['refresh_started_at']=time(); }
        if (in_array($state,array('success','unchanged','failed'),true)) {
            $s['refresh_finished_at']=time();
            $s['refresh_dispatch_token_hash']='';
            $s['refresh_dispatch_token_expires']=0;
            $s['refresh_dispatch_transport']='';
        }
        update_option(self::OPTION_NETWORK_IDEALO,$s,false);
    }

    private function idealo_issue_worker_token() {
        $token=function_exists('wp_generate_password') ? wp_generate_password(48,false,false) : bin2hex(random_bytes(24));
        $s=$this->idealo_settings();
        $s['refresh_dispatch_token_hash']=hash('sha256',(string)$token);
        $s['refresh_dispatch_token_expires']=time()+15*MINUTE_IN_SECONDS;
        update_option(self::OPTION_NETWORK_IDEALO,$s,false);
        return (string)$token;
    }

    private function idealo_consume_worker_token($token) {
        $token=(string)$token; if ($token==='') { return false; }
        $s=$this->idealo_settings();
        $expected=(string)($s['refresh_dispatch_token_hash']??'');
        $expires=absint($s['refresh_dispatch_token_expires']??0);
        if ($expected==='' || $expires<time() || !hash_equals($expected,hash('sha256',$token))) { return false; }
        $s['refresh_dispatch_token_hash']=''; $s['refresh_dispatch_token_expires']=0;
        update_option(self::OPTION_NETWORK_IDEALO,$s,false);
        return true;
    }

    private function idealo_record_dispatch_attempt($transport, $message='') {
        $s=$this->idealo_settings();
        $s['refresh_dispatch_last_at']=time();
        $s['refresh_dispatch_attempts']=absint($s['refresh_dispatch_attempts']??0)+1;
        $s['refresh_dispatch_transport']=sanitize_key((string)$transport);
        if ($message!=='') { $s['refresh_last_message']=sanitize_text_field((string)$message); }
        update_option(self::OPTION_NETWORK_IDEALO,$s,false);
    }

    private function idealo_dispatch_manual_worker($reason='manual') {
        if (get_transient(self::IDEALO_REFRESH_LOCK)) { return array('transport'=>'locked','dispatched'=>false); }
        if (function_exists('wp_next_scheduled') && function_exists('wp_schedule_single_event') && !wp_next_scheduled(self::IDEALO_MANUAL_REFRESH_HOOK)) {
            // Cron is only a fallback. The primary transport below does not depend
            // on WP-Cron and therefore also works on hosts with DISABLE_WP_CRON.
            wp_schedule_single_event(time()+30,self::IDEALO_MANUAL_REFRESH_HOOK);
        }
        $token=$this->idealo_issue_worker_token();
        $endpoint=admin_url('admin-post.php');
        $args=array(
            'timeout'=>1,
            'blocking'=>false,
            'redirection'=>0,
            'sslverify'=>apply_filters('https_local_ssl_verify',false),
            'headers'=>array('Cache-Control'=>'no-cache'),
            'body'=>array('action'=>self::IDEALO_MANUAL_WORKER_ACTION,'token'=>$token),
            'user-agent'=>'Affiliate-Zentrale/'.self::VERSION.'; '.home_url('/'),
        );
        $response=wp_remote_post($endpoint,$args);
        if (is_wp_error($response)) {
            $this->idealo_record_dispatch_attempt('cron_fallback','Direkter Hintergrundstart nicht erreichbar; Cron-Fallback bleibt eingereiht.');
            return array('transport'=>'cron_fallback','dispatched'=>false,'error'=>$response->get_error_message());
        }
        $this->idealo_record_dispatch_attempt('loopback','Hintergrundstart gesendet; Cron bleibt nur als Fallback bestehen.');
        return array('transport'=>'loopback','dispatched'=>true);
    }

    private function idealo_execute_background_refresh($origin='scheduled') {
        if (!$this->idealo_refresh_lock_acquire()) {
            return array('status'=>'queued','message'=>'idealo-Aktualisierung läuft bereits; kein paralleler Vollfeed-Lauf gestartet.');
        }
        if ($origin==='manual' && function_exists('wp_clear_scheduled_hook')) { wp_clear_scheduled_hook(self::IDEALO_MANUAL_REFRESH_HOOK); }
        $this->idealo_set_refresh_state('running', $origin==='manual' ? 'Manuelle idealo-Aktualisierung läuft im Hintergrund.' : 'Automatische idealo-Aktualisierung läuft im Hintergrund.');
        try {
            $result=$this->idealo_refresh_remote_feed(true);
            if (is_wp_error($result)) {
                $message='idealo-Aktualisierung fehlgeschlagen; Last-Good bleibt erhalten: '.$result->get_error_message();
                $this->idealo_set_refresh_state('failed',$message);
                $this->provider_set_access_state('idealo','degraded',$message);
                return $result;
            }
            $status=sanitize_key((string)($result['status']??'success'));
            if ($status==='unchanged') {
                $this->idealo_set_refresh_state('unchanged',(string)($result['message']??'Feed unverändert.'));
            } else {
                $this->idealo_set_refresh_state('success','idealo-Vollfeed wurde im Hintergrund erfolgreich aktualisiert.');
            }
            return $result;
        } finally {
            $this->idealo_refresh_lock_release();
        }
    }

    public function idealo_run_scheduled_refresh() {
        $this->idealo_execute_background_refresh('scheduled');
    }

    public function idealo_run_manual_refresh() {
        $this->idealo_execute_background_refresh('manual');
    }

    public function handle_idealo_manual_refresh_worker() {
        $token=isset($_POST['token']) ? (string)wp_unslash($_POST['token']) : '';
        if (!$this->idealo_consume_worker_token($token)) {
            if (function_exists('status_header')) { status_header(403); }
            exit;
        }
        @set_time_limit(0); if (function_exists('ignore_user_abort')) { @ignore_user_abort(true); }
        if (function_exists('session_write_close')) { @session_write_close(); }
        $completed=false;
        register_shutdown_function(function() use (&$completed) {
            if ($completed) { return; }
            $last=error_get_last();
            if (!is_array($last) || !in_array((int)($last['type']??0),array(E_ERROR,E_PARSE,E_CORE_ERROR,E_COMPILE_ERROR,E_USER_ERROR),true)) { return; }
            $this->idealo_refresh_lock_release();
            $this->idealo_set_refresh_state('failed','idealo-Hintergrundworker wurde durch einen PHP-Fehler beendet; Last-Good bleibt erhalten.');
        });
        $this->idealo_execute_background_refresh('manual');
        $completed=true;
        if (function_exists('status_header')) { status_header(204); }
        exit;
    }

    public function idealo_maybe_recover_refresh_dispatch() {
        $action=isset($_REQUEST['action']) ? sanitize_key((string)wp_unslash($_REQUEST['action'])) : '';
        if ($action===self::IDEALO_MANUAL_WORKER_ACTION) { return; }
        $s=$this->idealo_settings(); $state=sanitize_key((string)($s['refresh_state']??'idle')); $now=time();
        if ($state==='queued') {
            if (get_transient(self::IDEALO_REFRESH_LOCK)) { return; }
            $last=absint($s['refresh_dispatch_last_at']??0);
            if ($last===0 || ($now-$last)>=45) { $this->idealo_dispatch_manual_worker('queued_recovery'); }
            return;
        }
        if ($state==='running') {
            $started=absint($s['refresh_started_at']??0);
            if ($started>0 && ($now-$started)>45*MINUTE_IN_SECONDS && !get_transient(self::IDEALO_REFRESH_LOCK)) {
                $this->idealo_set_refresh_state('queued','Vorheriger Hintergrundworker ist ohne aktiven Lock abgebrochen; sicherer Neustart wird ausgelöst.');
                $this->idealo_dispatch_manual_worker('running_recovery');
            }
        }
    }

    private function idealo_queue_manual_refresh() {
        $s=$this->idealo_settings();
        if (trim((string)($s['feed_url']??''))==='') { return new WP_Error('idealo_feed_url_missing','Es ist noch keine vom iPN erzeugte Feed-URL gespeichert.'); }
        if (get_transient(self::IDEALO_REFRESH_LOCK) || sanitize_key((string)($s['refresh_state']??''))==='running') {
            return array('status'=>'success','message'=>'idealo-Aktualisierung läuft bereits im Hintergrund. Es wurde kein zweiter Vollfeed-Lauf gestartet.','counts'=>array(),'details'=>array('queued'=>true));
        }
        if (sanitize_key((string)($s['refresh_state']??''))!=='queued') {
            $this->idealo_set_refresh_state('queued','idealo-Vollfeed wurde zur Hintergrundaktualisierung eingereiht. Die Admin-Seite kann geschlossen werden.');
        }
        $dispatch=$this->idealo_dispatch_manual_worker('manual');
        return array('status'=>'success','message'=>'idealo-Vollfeed wurde im Hintergrund eingereiht. Direkter Workerstart ist aktiv; WordPress-Cron dient nur noch als Fallback.','counts'=>array(),'details'=>array('queued'=>true,'transport'=>(string)($dispatch['transport']??'')));
    }

    private function idealo_refresh_remote_feed($metadata_first=true) {
        $s=$this->idealo_settings();
        if ($metadata_first) {
            $metadata=$this->idealo_find_feed_metadata($s); if (is_wp_error($metadata)) { return $metadata; }
            $s['api_last_checked_at']=time(); $s['api_last_feed_hash']=(string)($metadata['last_file_hash']??''); $s['api_last_updated_at']=(string)($metadata['last_updated_at']??''); $s['api_last_product_count']=absint($metadata['number_of_products']??0); $s['api_last_advertiser_name']=sanitize_text_field((string)($metadata['advertiser_name']??''));
            update_option(self::OPTION_NETWORK_IDEALO,$s,false);
            if (!empty($s['last_remote_file_hash']) && $s['last_remote_file_hash']===(string)($metadata['last_file_hash']??'') && absint($s['last_import_at']??0)>0) { return array('status'=>'unchanged','message'=>'Feed-Hash unverändert; kein Download.'); }
        }
        $download=$this->idealo_download_feed_to_temp($s); if (is_wp_error($download)) { return $download; }
        if (($download['status']??'')==='not_modified') { $s['feed_etag']=(string)($download['etag']??$s['feed_etag']); $s['feed_last_modified']=(string)($download['last_modified']??$s['feed_last_modified']); update_option(self::OPTION_NETWORK_IDEALO,$s,false); return array('status'=>'unchanged','message'=>'HTTP 304: Feed unverändert.'); }
        $path=(string)($download['path']??''); $result=$this->idealo_import_feed_file($path,'Automatischer iPN-Remote-Feed'); @unlink($path); if (is_wp_error($result)) { return $result; }
        $s=$this->idealo_settings(); $s['feed_etag']=(string)($download['etag']??''); $s['feed_last_modified']=(string)($download['last_modified']??''); $s['last_download_at']=time(); $s['last_remote_file_hash']=(string)($s['api_last_feed_hash']??''); update_option(self::OPTION_NETWORK_IDEALO,$s,false);
        return $result;
    }

    public function idealo_sync_dispatch($handled,$network,$operation,$contract_version) {
        if ($network!=='idealo') { return $handled; }
        if ($operation==='connection') { $test=$this->idealo_provider_access_test(null,'idealo',$contract_version); if (is_wp_error($test)) { return $test; } return array('status'=>'success','message'=>(string)($test['message']??'idealo-Zugang geprüft.'),'counts'=>array(),'details'=>array('public_activation'=>$this->idealo_campaigns_should_be_active())); }
        if ($operation!=='products') { return new WP_Error('idealo_sync_operation_unknown','Unbekannte idealo-Synchronisationsaktion.'); }
        return $this->idealo_queue_manual_refresh();
    }

    public function handle_idealo_import_file() {
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.'); }
        check_admin_referer('ppar_idealo_import_file','ppar_idealo_nonce');
        if (empty($_FILES['idealo_feed'])||!is_array($_FILES['idealo_feed'])) { wp_die('Keine Feed-Datei hochgeladen.'); }
        $file=$_FILES['idealo_feed']; if ((int)($file['error']??UPLOAD_ERR_NO_FILE)!==UPLOAD_ERR_OK||empty($file['tmp_name'])) { wp_die('Upload fehlgeschlagen.'); }
        $name=sanitize_file_name((string)($file['name']??'')); if (!preg_match('/\.csv(?:\.gz)?$/i',$name)) { wp_die('Erlaubt sind ausschließlich .csv oder .csv.gz.'); }
        $result=$this->idealo_import_feed_file((string)$file['tmp_name'],'Manueller iPN-Testfeed'); $args=array('page'=>'affiliate-portal-provider-idealo');
        if (is_wp_error($result)) { $args['ppar_idealo_error']=rawurlencode($result->get_error_message()); } else { $args['ppar_idealo_imported']=absint($result['details']['matching_rows']??0); }
        wp_safe_redirect(add_query_arg($args,admin_url('admin.php'))); exit;
    }

    /** Exact product identity helpers shared by category and article renderers. */
    public function multiprovider_campaign_gtins($campaign) {
        if (!is_array($campaign)) { return array(); }
        $gtins=$this->idealo_normalize_gtins_from_values((array)($campaign['product_gtins']??array()));
        $post_id=absint($campaign['post_id']??0); if ($post_id>0) { $gtins=array_values(array_unique(array_merge($gtins,$this->idealo_normalize_gtins_from_values((array)get_post_meta($post_id,'_ppar_product_gtin',false))))); }
        if (sanitize_key((string)($campaign['network']??''))==='ebay' && method_exists($this,'ebay_business_campaign_source_row')) {
            static $cache=array(); $ck=$post_id>0?$post_id:md5(wp_json_encode($campaign));
            if (!isset($cache[$ck])) {
                $row=$this->ebay_business_campaign_source_row($campaign); $payload=is_array($row)?json_decode((string)($row['source_payload']??''),true):array(); $payload=is_array($payload)?$payload:array(); $raw=is_array($payload['raw']??null)?$payload['raw']:array(); $values=array($raw['gtin']??'',$raw['ean']??'',$raw['upc']??'');
                foreach ((array)($raw['localizedAspects']??array()) as $aspect) { if (!is_array($aspect)) { continue; } $name=strtolower(trim((string)($aspect['name']??''))); if (in_array($name,array('ean','gtin','upc','ean/gtin'),true)) { $values[]=(string)($aspect['value']??''); } }
                $cache[$ck]=$this->idealo_normalize_gtins_from_values($values);
            }
            $gtins=array_values(array_unique(array_merge($gtins,$cache[$ck])));
        }
        sort($gtins,SORT_STRING); return $gtins;
    }

    public function multiprovider_campaign_identity_key($campaign) {
        $gtins=$this->multiprovider_campaign_gtins($campaign); return $gtins ? 'gtin:'.$gtins[0] : '';
    }

    public function multiprovider_campaigns_share_exact_gtin($left,$right) {
        $a=$this->multiprovider_campaign_gtins($left); $b=$this->multiprovider_campaign_gtins($right);
        return !empty($a) && !empty($b) && !empty(array_intersect($a,$b));
    }

    /**
     * V6.61.4: iPN image_url is a tracking wrapper. Product cards must load the
     * real HTTPS image target, not the tracking endpoint. Current feed 2901 wraps
     * the real cdn.idealo.com path in trg (sometimes through gfx.productsup.io).
     */
    private function idealo_direct_image_url($url) {
        $url=html_entity_decode(trim((string)$url),ENT_QUOTES,'UTF-8');
        if ($url==='') { return ''; }
        $parts=wp_parse_url($url);
        if (is_array($parts) && strtolower((string)($parts['scheme']??''))==='https' && strtolower((string)($parts['host']??''))==='cdn.idealo.com') {
            return esc_url_raw($url);
        }
        if (!is_array($parts) || strtolower((string)($parts['scheme']??''))!=='https') { return ''; }
        $query=array(); parse_str((string)($parts['query']??''),$query);
        $target=isset($query['trg'])?rawurldecode((string)$query['trg']):'';
        $target=html_entity_decode($target,ENT_QUOTES,'UTF-8');
        if ($target==='') { return ''; }
        $target_parts=wp_parse_url($target);
        if (is_array($target_parts) && strtolower((string)($target_parts['scheme']??''))==='https' && strtolower((string)($target_parts['host']??''))==='cdn.idealo.com') {
            return esc_url_raw($target);
        }
        if (is_array($target_parts) && strtolower((string)($target_parts['scheme']??''))==='https' && strtolower((string)($target_parts['host']??''))==='gfx.productsup.io') {
            $path=(string)($target_parts['path']??'');
            $needle='/src/cdn.idealo.com/';
            $pos=strpos($path,$needle);
            if ($pos!==false) {
                $cdn_path=substr($path,$pos+strlen('/src/cdn.idealo.com'));
                if ($cdn_path!=='' && $cdn_path[0]==='/') {
                    return esc_url_raw('https://cdn.idealo.com'.$cdn_path);
                }
            }
        }
        return '';
    }

    private function idealo_cached_image_url($url,$campaign_post_id=0,$allow_fetch=true) {
        $direct=$this->idealo_direct_image_url($url);
        if ($direct==='' || !function_exists('wp_upload_dir')) { return ''; }
        $uploads=wp_upload_dir(null,false);
        if (!is_array($uploads) || !empty($uploads['error']) || empty($uploads['basedir']) || empty($uploads['baseurl'])) { return ''; }
        $dir=rtrim((string)$uploads['basedir'],'/\\').'/ppar-affiliate-product-images';
        $baseurl=rtrim((string)$uploads['baseurl'],'/').'/ppar-affiliate-product-images';
        $url_hash=hash('sha256',$direct);
        $stem='idealo-'.absint($campaign_post_id).'-'.substr($url_hash,0,32);
        foreach (array('jpg','png','webp','gif') as $ext) {
            $file=$dir.'/'.$stem.'.'.$ext;
            if (is_file($file) && filesize($file)>0) { return esc_url_raw($baseurl.'/'.basename($file)); }
        }
        if (!$allow_fetch || !function_exists('wp_safe_remote_get')) { return ''; }
        $failure_key='ppar_idealo_img_fail_'.substr($url_hash,0,32);
        if (function_exists('get_transient') && get_transient($failure_key)) { return ''; }
        $response=wp_safe_remote_get($direct,array('timeout'=>5,'redirection'=>2,'headers'=>array('Accept'=>'image/avif,image/webp,image/apng,image/*,*/*;q=0.8'),'limit_response_size'=>4194304));
        if (function_exists('is_wp_error') && is_wp_error($response)) { if (function_exists('set_transient')) { set_transient($failure_key,1,HOUR_IN_SECONDS); } return ''; }
        $code=function_exists('wp_remote_retrieve_response_code')?absint(wp_remote_retrieve_response_code($response)):0;
        $body=function_exists('wp_remote_retrieve_body')?(string)wp_remote_retrieve_body($response):'';
        if ($code<200 || $code>=300 || $body==='' || strlen($body)>4194304) { if (function_exists('set_transient')) { set_transient($failure_key,1,HOUR_IN_SECONDS); } return ''; }
        $size=function_exists('getimagesizefromstring')?@getimagesizefromstring($body):false;
        if (!is_array($size) || absint($size[0]??0)<=0 || absint($size[1]??0)<=0) { if (function_exists('set_transient')) { set_transient($failure_key,1,HOUR_IN_SECONDS); } return ''; }
        $mime=strtolower((string)($size['mime']??''));
        $map=array('image/jpeg'=>'jpg','image/jpg'=>'jpg','image/png'=>'png','image/webp'=>'webp','image/gif'=>'gif');
        $ext=$map[$mime]??''; if ($ext==='') { if (function_exists('set_transient')) { set_transient($failure_key,1,HOUR_IN_SECONDS); } return ''; }
        if (!is_dir($dir) && (!function_exists('wp_mkdir_p') || !wp_mkdir_p($dir))) { return ''; }
        $file=$dir.'/'.$stem.'.'.$ext; $tmp=$file.'.tmp-'.substr(hash('sha256',uniqid('',true)),0,12);
        $written=@file_put_contents($tmp,$body,LOCK_EX);
        if ($written!==strlen($body) || !@rename($tmp,$file)) { @unlink($tmp); return ''; }
        @chmod($file,0644); if (function_exists('delete_transient')) { delete_transient($failure_key); }
        return esc_url_raw($baseurl.'/'.basename($file));
    }

    private function idealo_runtime_timestamp_url($url) {
        $url=(string)$url;
        if ($url==='') { return ''; }
        $stamp=(string)time();
        return esc_url_raw(str_replace(array('!!TIME_STAMP!!','!!TIMESTAMP!!','%21%21TIME_STAMP%21%21','%21%21TIMESTAMP%21%21'),$stamp,$url));
    }

    public function multiprovider_runtime_tracking_url($url,$network='') {
        $url=(string)$url;
        if (sanitize_key((string)$network)==='idealo') { return $this->idealo_runtime_timestamp_url($url); }
        return esc_url_raw($url);
    }

    /**
     * Provider image URLs have their own runtime contract. idealo tracked image
     * wrappers are unwrapped to the real cdn.idealo.com image and cached locally.
     * eBay BUSINESS likewise renders from the current verified local cache.
     * Provider click URLs keep their tracking/timestamp contract independently.
     */
    public function multiprovider_runtime_image_url($url,$network='',$campaign_post_id=0) {
        $url=(string)$url;
        $network=sanitize_key((string)$network);
        // V6.61.5: Frontend rendering is deliberately network-I/O free. idealo
        // feeds are already normalized to a real cdn.idealo.com target; resolve
        // that target directly instead of creating a local file during a page hit.
        if ($network==='idealo') { return $this->idealo_direct_image_url($url); }
        // eBay uses the current active BUSINESS source row rather than a stale
        // materialized campaign URL. No wp_remote_get() is allowed in this path.
        if ($network==='ebay' && absint($campaign_post_id)>0 && method_exists($this,'campaign_from_post') && method_exists($this,'ebay_product_public_image_url')) {
            $campaign=$this->campaign_from_post(get_post(absint($campaign_post_id)));
            if (is_array($campaign)) {
                $current=$this->ebay_product_public_image_url($campaign);
                if ($current!=='') { return $current; }
            }
        }
        return esc_url_raw($url);
    }

    private function multiprovider_offer_label($network) {
        $network=sanitize_key((string)$network); if ($network==='ebay') { return 'Bei eBay ansehen'; } if ($network==='idealo') { return 'Bei idealo vergleichen'; } if ($network==='amazon') { return 'Bei Amazon ansehen'; } return 'Angebot ansehen';
    }

    public function multiprovider_matching_offers_for_banner($banner,$context,$slot_type) {
        $post_id=absint($banner['campaign_post_id']??0); $campaign=$post_id>0?$this->campaign_from_post(get_post($post_id)):null;
        if (!is_array($campaign)) { return array(); }
        $source_post_id=absint($context['post_id'] ?? 0);
        $current_url=(string)($banner['url'] ?? '');
        if ($current_url==='') { $current_url=$this->multiprovider_runtime_tracking_url((string)($campaign['url']??''),(string)($campaign['network']??'')); }
        $base=array('network'=>sanitize_key((string)($campaign['network']??'')),'url'=>$current_url,'label'=>$this->multiprovider_offer_label($campaign['network']??''));
        if (!in_array($this->idealo_output_mode(), array('combined','automatic'), true)) { return $current_url!==''?array($base):array(); }
        if (!$this->multiprovider_campaign_gtins($campaign)) { return $current_url!==''?array($base):array(); }
        $offers=array();
        foreach ($this->get_campaigns() as $candidate) {
            if (!is_array($candidate)||empty($candidate['active'])||sanitize_key((string)($candidate['creative_type']??''))!=='product'||!$this->campaign_is_complete($candidate)||!$this->campaign_program_allows_delivery($candidate)||!$this->campaign_source_allows_delivery($candidate)||!$this->campaign_slot_allowed($candidate,$slot_type)) { continue; }
            $rank_context=$context; $rank_context['slot_type']=sanitize_key((string)$slot_type); if (!$this->campaign_match_rank($candidate,$rank_context)) { continue; }
            if (!$this->campaign_control_allows_delivery($candidate,$slot_type)||!$this->campaign_health_allows_delivery($candidate)) { continue; }
            if (!$this->multiprovider_campaigns_share_exact_gtin($campaign,$candidate)) { continue; }
            $network=sanitize_key((string)($candidate['network']??'')); if ($network===''||isset($offers[$network])) { continue; }
            if ($network==='idealo' && $this->idealo_link_strategy()==='comparison') { continue; }
            $candidate_post_id=absint($candidate['post_id']??0);
            $url=($source_post_id>0 && $candidate_post_id>0)
                ? $this->build_click_tracking_url($candidate_post_id,$source_post_id,$slot_type)
                : $this->multiprovider_runtime_tracking_url((string)($candidate['url']??''),$network);
            if ($url==='') { continue; }
            $offers[$network]=array('network'=>$network,'url'=>$url,'label'=>$this->multiprovider_offer_label($network));
        }
        if (!$offers && $current_url!=='') { $offers[$base['network']]=$base; }
        $order=array('ebay','idealo','amazon'); uksort($offers,static function($a,$b)use($order){$ia=array_search($a,$order,true);$ib=array_search($b,$order,true);$ia=$ia===false?99:$ia;$ib=$ib===false?99:$ib;return $ia<=>$ib;});
        return array_values($offers);
    }

    public function multiprovider_render_offer_buttons($offers,$surface='article') {
        $offers=array_values((array)$offers); if (!$offers) { return ''; }
        $wrap=$surface==='article'?'ppar-article-product-actions':'ppar-banner-actions'; $button=$surface==='article'?'ppar-article-product-offer-button':'ppar-banner-offer-button';
        $out='<span class="'.esc_attr($wrap).'">'; foreach ($offers as $offer) { $url=esc_url((string)($offer['url']??'')); if ($url==='') { continue; } $out.='<a class="'.esc_attr($button).'" href="'.$url.'" target="_blank" rel="sponsored nofollow noopener noreferrer">'.esc_html((string)($offer['label']??'Angebot ansehen')).'</a>'; } return $out.'</span>';
    }

    public function multiprovider_filter_candidates_by_strategy($candidates) {
        return array_values(array_filter(array_values((array)$candidates),function($candidate){
            $campaign=is_array($candidate)?($candidate['campaign']??null):null;
            return !is_array($campaign) || sanitize_key((string)($campaign['network']??''))!=='idealo' || $this->idealo_standalone_campaign_allowed($campaign);
        }));
    }

    public function multiprovider_reorder_candidates($candidates,$mode='separate') {
        $candidates=array_values((array)$candidates); $mode=$this->idealo_sanitize_output_mode($mode); if (!$candidates) { return array(); }
        $candidates=$this->multiprovider_filter_candidates_by_strategy($candidates);
        if (!$candidates) { return array(); }
        if (in_array($mode,array('combined','automatic'),true)) {
            $seen_gtins=array(); $dedup=array();
            foreach ($candidates as $candidate) {
                $campaign=is_array($candidate)?($candidate['campaign']??null):null; $gtins=is_array($campaign)?$this->multiprovider_campaign_gtins($campaign):array();
                if ($gtins && array_intersect($gtins,array_keys($seen_gtins))) { continue; }
                foreach ($gtins as $gtin) { $seen_gtins[$gtin]=true; }
                $dedup[]=$candidate;
            }
            $candidates=$dedup;
        }
        $queues=array(); $order=array(); foreach ($candidates as $candidate) { $campaign=is_array($candidate)?($candidate['campaign']??null):null; $network=is_array($campaign)?sanitize_key((string)($campaign['network']??'manual')):'manual'; if (!isset($queues[$network])) { $queues[$network]=array(); $order[]=$network; } $queues[$network][]=$candidate; }
        if (count($order)<2) { return $candidates; }
        $out=array(); do { $added=false; foreach ($order as $network) { if (!empty($queues[$network])) { $out[]=array_shift($queues[$network]); $added=true; } } } while ($added);
        return $out;
    }

    public function idealo_render_access_card($provider,$definition,$contract_version) {
        $s=$this->idealo_settings(); $external=$this->idealo_api_key_external(); ?>
        <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>">
            <input type="hidden" name="action" value="ppar_provider_access_save"><input type="hidden" name="provider" value="idealo"><?php wp_nonce_field('ppar_provider_access_idealo','ppar_provider_nonce'); ?>
            <p><label><input type="checkbox" name="ppar_provider[idealo][enabled]" value="1" <?php checked(!empty($s['enabled'])); ?>> idealo-Verbindung verwenden</label></p>
            <p><label>iPN API-Key <span class="ppar-saved"><?php echo $external?'über wp-config.php':(trim((string)$s['api_key'])!==''?'gespeichert':'nicht gespeichert'); ?></span><br><input type="password" autocomplete="new-password" name="ppar_provider[idealo][api_key]" value="" placeholder="leer lassen zum Beibehalten" <?php disabled($external); ?>></label></p>
            <p><label>Adspace-ID<br><input type="text" inputmode="numeric" name="ppar_provider[idealo][adspace_id]" value="<?php echo esc_attr((string)$s['adspace_id']); ?>"></label> <span class="description">Pferde Atelier: 568313.</span></p>
            <p><strong>Feed-ID:</strong> <code>2901</code><input type="hidden" name="ppar_provider[idealo][feed_id]" value="2901"> <span class="description">Gebundener Standardfeed; portalweiter Superset-Feed.</span></p>
            <p><label>Offizielle iPN-Download-URL für Feed 2901 <span class="ppar-saved"><?php echo trim((string)$s['feed_url'])!==''?'gespeichert':'noch nicht gespeichert'; ?></span><br><input class="large-text" type="password" autocomplete="new-password" name="ppar_provider[idealo][feed_url]" value="" placeholder="leer lassen zum Beibehalten"></label></p><?php if (trim((string)$s['feed_url'])!==''): ?><details><summary>Feed-URL entfernen</summary><p><label><input type="checkbox" name="ppar_provider[idealo][remove_feed_url]" value="1"> gespeicherte Feed-URL entfernen</label></p></details><?php endif; ?>
            <p><label>Portalweite Affiliate-Ausgabe<br><select name="ppar_provider[idealo][output_mode]"><option value="ebay_only" <?php selected($s['output_mode'],'ebay_only'); ?>>Nur bestehende eBay-/Bestandslogik</option><option value="idealo_only" <?php selected($s['output_mode'],'idealo_only'); ?>>Nur idealo-Ausgabe</option><option value="separate" <?php selected($s['output_mode'],'separate'); ?>>Provider getrennt als Karten</option><option value="combined" <?php selected($s['output_mode'],'combined'); ?>>Gemeinsame Karte bei exakter GTIN, sonst getrennt</option><option value="automatic" <?php selected($s['output_mode'],'automatic'); ?>>Automatisch: gemeinsam bei exakter GTIN, sonst getrennt</option></select></label></p>
            <p><label>idealo-Linkstrategie<br><select name="ppar_provider[idealo][link_strategy]"><option value="hybrid" <?php selected($s['link_strategy'],'hybrid'); ?>>Hybrid (empfohlen): Preisvergleich allein, konkrete idealo-Angebote nur als GTIN-Zusatzbutton</option><option value="products" <?php selected($s['link_strategy'],'products'); ?>>Konkrete idealo-Produkte als eigene Karten</option><option value="comparison" <?php selected($s['link_strategy'],'comparison'); ?>>Nur idealo-Preisvergleichs-/Suchlinks</option></select></label></p>
            <p><label><input type="checkbox" name="ppar_provider[idealo][auto_refresh]" value="1" <?php checked(!empty($s['auto_refresh'])); ?>> Feed automatisch alle zwölf Stunden auf Änderungen prüfen (nur bei gespeicherter Download-URL)</label></p>
            <p class="description"><strong>Portalabgleich:</strong> Feed 2901 wird streamend gegen den gebundenen 311er-Produktvertrag / 59 Hub-Familien geprüft. Im Hybridmodus wird idealo eigenständig als Produktfamilien-/Preisvergleich verlinkt; konkrete idealo-Angebote erscheinen zusätzlich nur bei exakter GTIN auf einer bereits konkreten Produktkarte.</p>
            <?php if (!$external): ?><details><summary>Zugangsdaten entfernen</summary><p><label><input type="checkbox" name="ppar_provider[idealo][remove_api_key]" value="1"> API-Key entfernen</label></p></details><?php endif; ?>
            <p><button class="button button-primary" name="ppar_provider_action" value="save">Speichern</button> <button class="button" name="ppar_provider_action" value="save_test">Speichern &amp; API prüfen</button></p>
        </form><?php
    }

    public function idealo_render_specialist_content($provider,$definition,$contract_version) {
        $s=$this->idealo_settings(); $counts=$this->network_sync_counts('idealo'); ?>
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px;margin-top:18px">
            <section class="postbox" style="padding:18px"><h2>Providerbestand</h2><p><strong>Staged:</strong> <?php echo absint($counts['products']); ?> Produkte<br><strong>PASS:</strong> <?php echo absint($counts['pass']); ?><br><strong>WARN:</strong> <?php echo absint($counts['warn']); ?><br><strong>Materialisiert:</strong> <?php echo absint($s['last_materialized_count']??0); ?> / Ziele <?php echo absint($s['last_materialized_targets']??0); ?><br><strong>Portalabdeckung:</strong> <?php echo absint($s['last_matched_concepts']??0); ?>/311 Konzepte · <?php echo absint($s['last_matched_hubs']??0); ?>/59 Hub-Familien</p></section>
            <section class="postbox" style="padding:18px"><h2>Partner-API</h2><p><strong>Letzte Prüfung:</strong> <?php echo !empty($s['api_last_checked_at'])?esc_html(wp_date('d.m.Y H:i',(int)$s['api_last_checked_at'])):'noch nicht geprüft'; ?><br><strong>Feedprodukte:</strong> <?php echo absint($s['api_last_product_count']??0); ?><br><strong>Feed-Hash:</strong> <?php echo esc_html((string)($s['api_last_feed_hash']??'')); ?></p><p><?php echo esc_html((string)($s['api_last_message']??'')); ?></p></section>
            <section class="postbox" style="padding:18px"><h2>Ausgabe</h2><p><strong>Modus:</strong> <?php echo esc_html($this->idealo_output_mode()); ?><br><strong>Linkstrategie:</strong> <?php echo esc_html($this->idealo_link_strategy()); ?><br><strong>idealo aktiv:</strong> <?php echo $this->idealo_campaigns_should_be_active()?'ja':'nein'; ?><br><strong>Auto-Refresh:</strong> <?php echo (!empty($s['auto_refresh'])&&trim((string)$s['feed_url'])!=='')?'bereit':'wartet auf Feed-URL'; ?><br><strong>Refresh-Status:</strong> <?php echo esc_html((string)($s['refresh_state']??'idle')); ?><?php if (!empty($s['refresh_last_message'])): ?><br><?php echo esc_html((string)$s['refresh_last_message']); ?><?php endif; ?></p></section>
        </div>
        <section class="postbox" style="padding:18px;margin-top:18px;max-width:900px"><h2>Feed-Test / Fallback</h2><p>Eine echte <code>.csv.gz</code>-Datei kann für Diagnosezwecke erneut eingelesen werden. Produktiv ist Feed 2901 für den serverseitigen Stream-Abruf vorgesehen. Der Import ersetzt nicht den eBay-Workflow und veröffentlicht nur exakt gemappte idealo-Produkte, wenn idealo und ein entsprechender Ausgabemodus ausdrücklich aktiviert sind.</p><form method="post" enctype="multipart/form-data" action="<?php echo esc_url(admin_url('admin-post.php')); ?>"><input type="hidden" name="action" value="ppar_idealo_import_file"><?php wp_nonce_field('ppar_idealo_import_file','ppar_idealo_nonce'); ?><input type="file" name="idealo_feed" accept=".csv,.gz,.csv.gz" required> <?php submit_button('Feed prüfen und staged aktualisieren','secondary','',false); ?></form></section><?php
    }

    public function idealo_render_sync_card($provider,$definition,$contract_version) {
        $s=$this->idealo_settings(); $counts=$this->network_sync_counts('idealo'); ?>
        <p><strong>Prüfstufe:</strong> <?php echo absint($counts['products']); ?> Produkte (PASS <?php echo absint($counts['pass']); ?> / WARN <?php echo absint($counts['warn']); ?>)<br><strong>API:</strong> <?php echo !empty($s['api_last_checked_at'])?'geprüft':'noch nicht geprüft'; ?><br><strong>Ausgabe:</strong> <?php echo esc_html($this->idealo_output_mode()); ?> / <?php echo esc_html($this->idealo_link_strategy()); ?><br><strong>Vollfeed:</strong> <?php echo trim((string)$s['feed_url'])!==''?'automatisierbar':'Download-URL noch offen'; ?><br><strong>Refresh:</strong> <?php echo esc_html((string)($s['refresh_state']??'idle')); ?><?php if (!empty($s['refresh_last_message'])): ?> – <?php echo esc_html((string)$s['refresh_last_message']); ?><?php endif; ?></p>
        <p><a class="button" href="<?php echo esc_url(admin_url('admin.php?page=affiliate-portal-provider-idealo')); ?>">idealo-Fachseite öffnen</a><?php if (trim((string)$s['feed_url'])!==''): ?> <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>" style="display:inline"><input type="hidden" name="action" value="ppar_run_network_sync"><input type="hidden" name="network" value="idealo"><input type="hidden" name="operation" value="products"><?php wp_nonce_field('ppar_run_network_sync','ppar_sync_nonce'); ?><button class="button button-primary">Feed jetzt aktualisieren</button></form><?php endif; ?></p><?php
    }
}
