<?php
if (!defined('ABSPATH')) {
    exit;
}

/**
 * Providerunabhängige Partneraufnahme.
 *
 * V2.7.8 implementiert ausschließlich den ersten read-only Awin-Adapter.
 * Die Advertiser-ID kann direkt eingegeben werden; eine vorherige Programmlisten-
 * Synchronisierung ist ausdrücklich nicht erforderlich.
 * Es werden keine Kampagnen angelegt, keine Slots befüllt und keine Daten
 * veröffentlicht. Weitere Provider können später dieselbe Snapshot-Struktur
 * verwenden.
 */
trait PPAR_Provider_Intake_Trait {
    private function partner_intake_snapshots() {
        $value = get_option(self::OPTION_PARTNER_INTAKE, array());
        return is_array($value) ? $value : array();
    }

    private function partner_intake_store_snapshot($provider, $external_id, $snapshot) {
        $provider = sanitize_key((string) $provider);
        $external_id = preg_replace('/[^0-9A-Za-z._-]/', '', (string) $external_id);
        if ($provider === '' || $external_id === '' || !is_array($snapshot)) {
            return false;
        }
        $all = $this->partner_intake_snapshots();
        $all[$provider . ':' . $external_id] = $snapshot;
        return update_option(self::OPTION_PARTNER_INTAKE, $all, false);
    }

    private function partner_intake_api_response($response) {
        if (is_wp_error($response)) {
            return new WP_Error('provider_request_failed', $response->get_error_message());
        }
        $code = (int) wp_remote_retrieve_response_code($response);
        $body = (string) wp_remote_retrieve_body($response);
        if ($code < 200 || $code >= 300) {
            return new WP_Error('provider_http_' . $code, 'Awin-API antwortete mit HTTP ' . $code . '.');
        }
        $json = json_decode($body, true);
        if (!is_array($json)) {
            return new WP_Error('provider_invalid_json', 'Awin lieferte keine gültigen JSON-Daten.');
        }
        return $json;
    }

    private function partner_intake_awin_request($method, $path, $body = null) {
        $settings = $this->network_settings('awin');
        $publisher_id = preg_replace('/[^0-9]/', '', (string) ($settings['publisher_id'] ?? ''));
        $token = $this->network_secret('awin', 'access_token', $settings);
        if ($publisher_id === '' || $token === '') {
            return new WP_Error('awin_not_configured', 'Awin Publisher-ID oder API-Token fehlt.');
        }
        $path = (string) $path;
        $allowed_prefixes = array(
            '/publishers/' . $publisher_id . '/',
            '/publisher/' . $publisher_id . '/',
        );
        $allowed = false;
        foreach ($allowed_prefixes as $prefix) {
            if (strpos($path, $prefix) === 0) {
                $allowed = true;
                break;
            }
        }
        if (!$allowed) {
            return new WP_Error('awin_path_blocked', 'Der Awin-API-Pfad ist nicht für dieses Publisherkonto freigegeben.');
        }

        $args = array(
            'method' => strtoupper((string) $method),
            'timeout' => 25,
            'redirection' => 1,
            'headers' => array(
                'Accept' => 'application/json',
                'Authorization' => 'Bearer ' . $token,
            ),
            'limit_response_size' => 4194304,
        );
        if ($body !== null) {
            $args['headers']['Content-Type'] = 'application/json';
            $args['body'] = wp_json_encode($body, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
        }
        $response = wp_remote_request('https://api.awin.com' . $path, $args);
        return $this->partner_intake_api_response($response);
    }

    private function partner_intake_awin_programme_details($advertiser_id) {
        $settings = $this->network_settings('awin');
        $publisher_id = preg_replace('/[^0-9]/', '', (string) ($settings['publisher_id'] ?? ''));
        $advertiser_id = absint($advertiser_id);
        if ($publisher_id === '' || $advertiser_id <= 0) {
            return new WP_Error('awin_invalid_partner', 'Ungültige Publisher- oder Advertiser-ID.');
        }
        $path = '/publishers/' . $publisher_id . '/programmedetails?advertiserId=' . $advertiser_id . '&relationship=joined';
        return $this->partner_intake_awin_request('GET', $path);
    }

    private function partner_intake_awin_offers($advertiser_id, $page = 1, $page_size = 200) {
        $settings = $this->network_settings('awin');
        $publisher_id = preg_replace('/[^0-9]/', '', (string) ($settings['publisher_id'] ?? ''));
        $advertiser_id = absint($advertiser_id);
        $page = max(1, absint($page));
        $page_size = max(1, min(200, absint($page_size)));
        if ($publisher_id === '' || $advertiser_id <= 0) {
            return new WP_Error('awin_invalid_partner', 'Ungültige Publisher- oder Advertiser-ID.');
        }
        $body = array(
            'filters' => array(
                'advertiserIds' => array($advertiser_id),
                'membership' => 'joined',
                'regionCodes' => array('DE'),
                'status' => 'active',
                'type' => 'all',
            ),
            'pagination' => array(
                'page' => $page,
                'pageSize' => $page_size,
            ),
        );
        return $this->partner_intake_awin_request('POST', '/publisher/' . $publisher_id . '/promotions', $body);
    }

    private function partner_intake_is_list_array($value) {
        if (!is_array($value)) {
            return false;
        }
        $index = 0;
        foreach (array_keys($value) as $key) {
            if ($key !== $index) {
                return false;
            }
            $index++;
        }
        return true;
    }

    private function partner_intake_extract_programme_object($raw) {
        if (!is_array($raw)) {
            return array();
        }
        if (isset($raw['programmeInfo']) && is_array($raw['programmeInfo'])) {
            return $raw;
        }
        foreach (array('data', 'result', 'programme', 'program') as $key) {
            if (isset($raw[$key]) && is_array($raw[$key])) {
                $candidate = $this->partner_intake_extract_programme_object($raw[$key]);
                if ($candidate) {
                    return $candidate;
                }
            }
        }
        if ($this->partner_intake_is_list_array($raw)) {
            foreach ($raw as $row) {
                $candidate = $this->partner_intake_extract_programme_object($row);
                if ($candidate) {
                    return $candidate;
                }
            }
        }
        return array();
    }

    private function partner_intake_normalize_domains($domains) {
        $safe = array();
        if (!is_array($domains)) {
            return $safe;
        }
        foreach ($domains as $domain) {
            if (is_array($domain)) {
                $domain = $domain['domain'] ?? '';
            }
            $domain = strtolower(trim((string) $domain));
            $domain = preg_replace('#^https?://#', '', $domain);
            $domain = trim($domain, " \t\n\r\0\x0B/");
            if ($domain !== '' && preg_match('/^[a-z0-9.-]+$/', $domain)) {
                $safe[$domain] = $domain;
            }
        }
        return array_values($safe);
    }

    private function partner_intake_normalize_programme($raw, $advertiser_id) {
        $object = $this->partner_intake_extract_programme_object($raw);
        $info = isset($object['programmeInfo']) && is_array($object['programmeInfo']) ? $object['programmeInfo'] : array();
        $region = isset($info['primaryRegion']) && is_array($info['primaryRegion']) ? $info['primaryRegion'] : array();
        $commission_raw = isset($object['commissionRange']) && is_array($object['commissionRange']) ? $object['commissionRange'] : array();
        $commission_rows = $this->partner_intake_is_list_array($commission_raw) ? $commission_raw : array($commission_raw);
        $commission = array();
        foreach ($commission_rows as $row) {
            if (!is_array($row)) {
                continue;
            }
            $commission[] = array(
                'min' => isset($row['min']) ? (float) $row['min'] : null,
                'max' => isset($row['max']) ? (float) $row['max'] : null,
                'type' => sanitize_key((string) ($row['type'] ?? '')),
            );
        }
        $kpi = isset($object['kpi']) && is_array($object['kpi']) ? $object['kpi'] : array();
        $tracking_raw = isset($info['trackingTransparency']) && is_array($info['trackingTransparency']) ? $info['trackingTransparency'] : array();
        $tracking = array();
        foreach ($tracking_raw as $method) {
            if (is_scalar($method)) {
                $method = sanitize_text_field((string) $method);
                if ($method !== '') {
                    $tracking[] = $method;
                }
            }
        }
        return array(
            'external_id' => absint($info['id'] ?? $advertiser_id),
            'name' => sanitize_text_field((string) ($info['name'] ?? '')),
            'membership_status' => sanitize_key((string) ($info['membershipStatus'] ?? '')),
            'link_status' => sanitize_key((string) ($info['linkStatus'] ?? 'unknown')),
            'description' => wp_kses_post((string) ($info['description'] ?? '')),
            'display_url' => esc_url_raw((string) ($info['displayUrl'] ?? '')),
            'click_through_url' => esc_url_raw((string) ($info['clickThroughUrl'] ?? '')),
            'logo_url' => esc_url_raw((string) ($info['logoUrl'] ?? '')),
            'deeplink_enabled' => !empty($info['deeplinkEnabled']),
            'primary_sector' => sanitize_text_field((string) ($info['primarySector'] ?? '')),
            'primary_region_name' => sanitize_text_field((string) ($region['name'] ?? '')),
            'primary_region_code' => strtoupper(sanitize_text_field((string) ($region['countryCode'] ?? ''))),
            'currency_code' => strtoupper(sanitize_text_field((string) ($info['currencyCode'] ?? ''))),
            'valid_domains' => $this->partner_intake_normalize_domains($info['validDomains'] ?? array()),
            'tracking_transparency' => array_values(array_unique($tracking)),
            'commission_range' => $commission,
            'kpi' => array(
                'approval_percentage' => isset($kpi['approvalPercentage']) ? (float) $kpi['approvalPercentage'] : null,
                'average_payment_time' => sanitize_text_field((string) ($kpi['averagePaymentTime'] ?? '')),
                'awin_index' => isset($kpi['awinIndex']) ? (float) $kpi['awinIndex'] : null,
                'conversion_rate' => isset($kpi['conversionRate']) ? (float) $kpi['conversionRate'] : null,
                'epc' => isset($kpi['epc']) ? (float) $kpi['epc'] : null,
                'validation_days' => isset($kpi['validationDays']) ? absint($kpi['validationDays']) : null,
            ),
        );
    }

    private function partner_intake_extract_offer_rows($raw) {
        if (!is_array($raw)) {
            return array();
        }
        if ($this->partner_intake_is_list_array($raw)) {
            return $raw;
        }
        foreach (array('offers', 'data', 'items', 'promotions', 'results', 'content') as $key) {
            if (isset($raw[$key]) && is_array($raw[$key]) && $this->partner_intake_is_list_array($raw[$key])) {
                return $raw[$key];
            }
        }
        return array();
    }

    private function partner_intake_normalize_offer($row, $advertiser_id) {
        if (!is_array($row)) {
            return array();
        }
        $advertiser = isset($row['advertiser']) && is_array($row['advertiser']) ? $row['advertiser'] : array();
        $row_advertiser_id = absint($advertiser['id'] ?? $row['advertiserId'] ?? 0);
        if ($row_advertiser_id > 0 && $row_advertiser_id !== absint($advertiser_id)) {
            return array();
        }
        $regions = isset($row['regions']) && is_array($row['regions']) ? $row['regions'] : array();
        $region_codes = array();
        if (!empty($regions['all'])) {
            $region_codes[] = 'ALL';
        }
        if (isset($regions['list']) && is_array($regions['list'])) {
            foreach ($regions['list'] as $region) {
                if (!is_array($region)) {
                    continue;
                }
                $code = strtoupper(sanitize_text_field((string) ($region['countryCode'] ?? '')));
                if ($code !== '') {
                    $region_codes[$code] = $code;
                }
            }
        }
        $voucher = isset($row['voucher']) && is_array($row['voucher']) ? $row['voucher'] : array();
        return array(
            'external_id' => absint($row['promotionId'] ?? $row['id'] ?? 0),
            'type' => sanitize_key((string) ($row['type'] ?? 'promotion')),
            'advertiser_id' => $row_advertiser_id ?: absint($advertiser_id),
            'advertiser_name' => sanitize_text_field((string) ($advertiser['name'] ?? '')),
            'joined' => isset($advertiser['joined']) ? (bool) $advertiser['joined'] : true,
            'title' => sanitize_text_field((string) ($row['title'] ?? '')),
            'description' => wp_kses_post((string) ($row['description'] ?? '')),
            'terms' => wp_kses_post((string) ($row['terms'] ?? '')),
            'start_date' => sanitize_text_field((string) ($row['startDate'] ?? '')),
            'end_date' => sanitize_text_field((string) ($row['endDate'] ?? '')),
            'date_added' => sanitize_text_field((string) ($row['dateAdded'] ?? '')),
            'destination_url' => esc_url_raw((string) ($row['url'] ?? '')),
            'tracking_url' => esc_url_raw((string) ($row['urlTracking'] ?? '')),
            'region_codes' => array_values($region_codes),
            'voucher_code' => sanitize_text_field((string) ($voucher['code'] ?? '')),
            'voucher_exclusive' => !empty($voucher['exclusive']),
            'voucher_attributable' => !empty($voucher['attributable']),
        );
    }

    private function partner_intake_normalize_offers($raw, $advertiser_id) {
        $offers = array();
        foreach ($this->partner_intake_extract_offer_rows($raw) as $row) {
            $offer = $this->partner_intake_normalize_offer($row, $advertiser_id);
            if ($offer && $offer['external_id'] > 0 && $offer['title'] !== '') {
                $offers[(string) $offer['external_id']] = $offer;
            }
        }
        return array_values($offers);
    }

    private function partner_intake_feed_row_id($row) {
        if (!is_array($row)) {
            return 0;
        }
        foreach (array('merchant_id', 'advertiser_id') as $key) {
            if (isset($row[$key])) {
                $id = absint($row[$key]);
                if ($id > 0) {
                    return $id;
                }
            }
        }
        return 0;
    }

    private function partner_intake_matching_awin_feeds($advertiser_id) {
        $feeds = get_option(self::OPTION_NETWORK_AWIN_FEEDS, array());
        $feeds = is_array($feeds) ? $feeds : array();
        $matching = array();
        foreach ($feeds as $row) {
            if (!is_array($row) || $this->partner_intake_feed_row_id($row) !== absint($advertiser_id)) {
                continue;
            }
            $safe = array();
            foreach ($row as $key => $value) {
                if (!is_scalar($value)) {
                    continue;
                }
                $normalized_key = sanitize_key((string) $key);
                if ($normalized_key === '') {
                    continue;
                }
                if (strpos($normalized_key, 'url') !== false || strpos($normalized_key, 'link') !== false) {
                    $safe[$normalized_key] = esc_url_raw((string) $value);
                } else {
                    $safe[$normalized_key] = sanitize_text_field((string) $value);
                }
            }
            $matching[] = $safe;
        }
        return $matching;
    }

    private function partner_intake_joined_awin_programmes() {
        $programmes = get_option(self::OPTION_NETWORK_AWIN_PROGRAMMES, array());
        $programmes = is_array($programmes) ? $programmes : array();
        $safe = array();
        foreach ($programmes as $row) {
            if (!is_array($row)) {
                continue;
            }
            $id = absint($row['id'] ?? 0);
            $name = sanitize_text_field((string) ($row['name'] ?? ''));
            $relationship = sanitize_key((string) ($row['relationship'] ?? 'joined'));
            if ($id > 0 && $name !== '' && $relationship === 'joined') {
                $safe[$id] = $name;
            }
        }
        asort($safe, SORT_NATURAL | SORT_FLAG_CASE);
        return $safe;
    }

    private function partner_intake_requested_partner($source) {
        $source = is_array($source) ? $source : array();
        $provider = sanitize_key((string) ($source['provider'] ?? 'awin'));
        $advertiser_id = absint($source['advertiser_id'] ?? 0);
        $partner_name = sanitize_text_field((string) ($source['partner_name'] ?? ''));
        if ($provider !== 'awin') {
            return new WP_Error('provider_not_supported', 'Dieser Provider ist in der Partneraufnahme noch nicht freigeschaltet.');
        }
        if ($advertiser_id <= 0) {
            return new WP_Error('awin_invalid_partner', 'Bitte eine gültige Awin-Advertiser-ID eingeben.');
        }
        return array(
            'provider' => $provider,
            'advertiser_id' => $advertiser_id,
            'partner_name' => $partner_name,
        );
    }

    private function partner_intake_probe_partner($provider, $advertiser_id, $submitted_name = '', $include_offers = true) {
        $provider = sanitize_key((string) $provider);
        $advertiser_id = absint($advertiser_id);
        $submitted_name = sanitize_text_field((string) $submitted_name);
        if ($provider !== 'awin' || $advertiser_id <= 0) {
            return new WP_Error('awin_invalid_partner', 'Ungültige Awin-Advertiser-ID.');
        }

        $joined = $this->partner_intake_joined_awin_programmes();
        $known_name = $submitted_name !== '' ? $submitted_name : (isset($joined[$advertiser_id]) ? $joined[$advertiser_id] : '');
        $programme_raw = $this->partner_intake_awin_programme_details($advertiser_id);
        if (is_wp_error($programme_raw)) {
            return $programme_raw;
        }

        $raw_object = $this->partner_intake_extract_programme_object($programme_raw);
        $raw_info = isset($raw_object['programmeInfo']) && is_array($raw_object['programmeInfo']) ? $raw_object['programmeInfo'] : array();
        $raw_id = absint($raw_info['id'] ?? 0);
        if ($raw_id > 0 && $raw_id !== $advertiser_id) {
            return new WP_Error('awin_partner_mismatch', 'Awin lieferte Daten zu einer anderen Advertiser-ID.');
        }

        $programme = $this->partner_intake_normalize_programme($programme_raw, $advertiser_id);
        if ($programme['name'] === '' && $known_name !== '') {
            $programme['name'] = $known_name;
        }
        if ($programme['name'] === '') {
            return new WP_Error('awin_empty_programme', 'Awin lieferte für diese Advertiser-ID keine eindeutigen Programmdaten.');
        }
        $membership = strtolower((string) $programme['membership_status']);
        if ($membership !== '' && $membership !== 'joined') {
            return new WP_Error('awin_not_joined', 'Das Programm ist für dieses Publisherkonto nicht als „joined“ bestätigt.');
        }

        $offers_raw = $include_offers ? $this->partner_intake_awin_offers($advertiser_id, 1, 200) : array();
        $offers_error = is_wp_error($offers_raw) ? $offers_raw->get_error_message() : '';
        $offers = is_wp_error($offers_raw) ? array() : $this->partner_intake_normalize_offers($offers_raw, $advertiser_id);
        $offers_partial = is_wp_error($offers_raw);
        $feeds = $this->partner_intake_matching_awin_feeds($advertiser_id);
        return array(
            'schema' => '1.1',
            'provider' => 'awin',
            'external_id' => $advertiser_id,
            'entered_name' => $submitted_name,
            'captured_at' => time(),
            'status' => $offers_partial ? 'partial' : 'complete',
            'programme' => $programme,
            'offers' => $offers,
            'feeds' => $feeds,
            'capabilities' => array(
                'programme_details' => true,
                'offers' => !$offers_partial,
                'product_feed_list' => count($feeds) > 0,
                'creative_catalogue' => false,
                'creative_catalogue_reason' => 'Kein dokumentierter Awin-Publisher-Endpunkt für den vollständigen Creative-Katalog.',
                'public_activation' => false,
            ),
            'errors' => $offers_error !== '' ? array($offers_error) : array(),
        );
    }

    public function handle_partner_intake_probe() {
        if (!current_user_can('manage_options')) {
            wp_die('Keine Berechtigung.');
        }
        check_admin_referer('ppar_partner_intake_probe', 'ppar_partner_intake_nonce');
        $requested = $this->partner_intake_requested_partner($_POST);
        if (is_wp_error($requested)) {
            wp_safe_redirect(add_query_arg(array(
                'page' => 'affiliate-portal-partner-intake',
                'ppar_intake' => 'invalid',
                'ppar_message' => rawurlencode($requested->get_error_message()),
            ), admin_url('admin.php')));
            exit;
        }

        $provider = $requested['provider'];
        $advertiser_id = $requested['advertiser_id'];
        $partner_name = $requested['partner_name'];
        $snapshot = $this->partner_intake_probe_partner($provider, $advertiser_id, $partner_name);
        if (is_wp_error($snapshot)) {
            $code = method_exists($snapshot, 'get_error_code') ? (string) $snapshot->get_error_code() : '';
            wp_safe_redirect(add_query_arg(array(
                'page' => 'affiliate-portal-partner-intake',
                'ppar_intake' => $code === 'awin_not_joined' ? 'not_joined' : 'failed',
                'advertiser_id' => $advertiser_id,
                'partner_name' => rawurlencode($partner_name),
                'ppar_message' => rawurlencode($snapshot->get_error_message()),
            ), admin_url('admin.php')));
            exit;
        }

        $this->partner_intake_store_snapshot($provider, (string) $advertiser_id, $snapshot);
        wp_safe_redirect(add_query_arg(array(
            'page' => 'affiliate-portal-partner-intake',
            'ppar_intake' => $snapshot['status'] === 'partial' ? 'partial' : 'success',
            'advertiser_id' => $advertiser_id,
        ), admin_url('admin.php')));
        exit;
    }

    private function partner_intake_display_date($value) {
        $value = trim((string) $value);
        if ($value === '') {
            return '—';
        }
        $time = strtotime($value);
        return $time ? wp_date('d.m.Y', $time) : $value;
    }


    private function partner_profiles() {
        $value = get_option(self::OPTION_PARTNER_PROFILES, array());
        return is_array($value) ? $value : array();
    }

    private function partner_profile_key($provider, $external_id) {
        $provider = sanitize_key((string) $provider);
        $external_id = preg_replace('/[^0-9A-Za-z._-]/', '', (string) $external_id);
        return $provider !== '' && $external_id !== '' ? $provider . ':' . $external_id : '';
    }

    public function partner_profile_get($provider, $external_id) {
        $key = $this->partner_profile_key($provider, $external_id);
        $profiles = $this->partner_profiles();
        $profile = $key !== '' && isset($profiles[$key]) && is_array($profiles[$key]) ? $profiles[$key] : array();
        return wp_parse_args($profile, array(
            'schema' => '1.0',
            'provider' => sanitize_key((string) $provider),
            'external_id' => preg_replace('/[^0-9A-Za-z._-]/', '', (string) $external_id),
            'enabled' => false,
            'business_label' => '',
            'keywords' => array(),
            'portal_roots' => array(),
            'market_home' => false,
            'market_terms' => array(),
            'listing_id' => 0,
            'listing_state' => 'not_requested',
            'listing_link' => '',
            'listing_error' => '',
            'listing_logo_source' => '',
            'updated_at' => 0,
        ));
    }

    private function partner_profile_store($profile) {
        if (!is_array($profile)) {
            return false;
        }
        $key = $this->partner_profile_key($profile['provider'] ?? '', $profile['external_id'] ?? '');
        if ($key === '') {
            return false;
        }
        $profiles = $this->partner_profiles();
        $profiles[$key] = $profile;
        return update_option(self::OPTION_PARTNER_PROFILES, $profiles, false);
    }

    private function partner_profile_sanitize_keywords($value) {
        $items = is_array($value) ? $value : preg_split('/[\r\n,;]+/', (string) $value);
        $safe = array();
        foreach ((array) $items as $item) {
            $item = sanitize_text_field((string) $item);
            if ($item !== '') {
                $safe[strtolower($item)] = $item;
            }
        }
        return array_values(array_slice($safe, 0, 100));
    }


    public function handle_partner_profile_save() {
        if (!current_user_can('manage_options')) {
            wp_die('Keine Berechtigung.');
        }
        check_admin_referer('ppar_partner_profile_save', 'ppar_partner_profile_nonce');
        $provider = sanitize_key((string) ($_POST['provider'] ?? ''));
        $external_id = preg_replace('/[^0-9A-Za-z._-]/', '', (string) ($_POST['external_id'] ?? ''));
        $key = $this->partner_profile_key($provider, $external_id);
        $snapshots = $this->partner_intake_snapshots();
        if ($key === '' || !isset($snapshots[$key]) || !is_array($snapshots[$key])) {
            wp_safe_redirect(add_query_arg(array('page'=>'affiliate-portal-partner-intake','ppar_profile'=>'failed','ppar_message'=>rawurlencode('Partnerprofil kann nur für einen aufgenommenen Partner gespeichert werden.')), admin_url('admin.php')));
            exit;
        }
        $previous = $this->partner_profile_get($provider, $external_id);
        $profile = array(
            'schema' => '2.0',
            'provider' => $provider,
            'external_id' => $external_id,
            'enabled' => !empty($_POST['profile_enabled']),
            'business_label' => sanitize_text_field((string) ($_POST['business_label'] ?? '')),
            'keywords' => $this->partner_profile_sanitize_keywords(wp_unslash($_POST['keywords'] ?? '')),
            // Alte manuelle Zielauswahlen werden aus Kompatibilitätsgründen
            // erhalten, aber seit V4.0.0 nicht mehr als Automatisierung benutzt.
            'legacy_portal_roots' => array_values(array_filter(array_map('sanitize_key', (array) ($previous['portal_roots'] ?? array())))),
            'legacy_market_terms' => array_values(array_filter(array_map('sanitize_key', (array) ($previous['market_terms'] ?? array())))),
            'portal_roots' => array(),
            'market_home' => false,
            'market_terms' => array(),
            'listing_id' => absint($previous['listing_id'] ?? 0),
            'listing_state' => 'managed_by_output_objects',
            'listing_link' => '',
            'listing_error' => '',
            'listing_logo_source' => '',
            'updated_at' => time(),
        );
        if (!empty($profile['enabled']) && $profile['business_label'] === '') {
            wp_safe_redirect(add_query_arg(array('page'=>'affiliate-portal-partner-intake','ppar_profile'=>'failed','advertiser_id'=>$external_id,'ppar_message'=>rawurlencode('Für die automatische Zuordnung ist ein bestätigter Geschäftsbereich erforderlich.')), admin_url('admin.php')));
            exit;
        }
        $this->partner_profile_store($profile);
        $reapplied = method_exists($this, 'creative_library_reapply_partner_profile')
            ? $this->creative_library_reapply_partner_profile($provider, $external_id)
            : array('updated'=>0,'blocked'=>0,'unchanged'=>0);
        $message = sprintf(
            'Partnerprofil gespeichert · %d bestehende Werbemittel neu bewertet · %d blockiert. Listings und Banner werden nur aus einem verknüpften Creative als Entwurf erzeugt.',
            absint($reapplied['updated'] ?? 0),
            absint($reapplied['blocked'] ?? 0)
        );
        wp_safe_redirect(add_query_arg(array('page'=>'affiliate-portal-partner-intake','ppar_profile'=>'success','advertiser_id'=>$external_id,'ppar_message'=>rawurlencode($message)), admin_url('admin.php')));
        exit;
    }

    private function partner_profile_render_form($snapshot) {
        if (!is_array($snapshot)) {
            return;
        }
        $provider = sanitize_key((string) ($snapshot['provider'] ?? ''));
        $external_id = preg_replace('/[^0-9A-Za-z._-]/', '', (string) ($snapshot['external_id'] ?? ''));
        if ($provider === '' || $external_id === '') {
            return;
        }
        $programme = is_array($snapshot['programme'] ?? null) ? $snapshot['programme'] : array();
        $profile = $this->partner_profile_get($provider, $external_id);
        $business_default = (string) ($profile['business_label'] ?? '');
        if ($business_default === '') {
            $business_default = sanitize_text_field((string) ($programme['primary_sector'] ?? $programme['primarySector'] ?? ''));
        }
        ?>
        <details style="margin-top:16px" <?php echo !empty($profile['enabled']) ? 'open' : ''; ?>>
            <summary><strong>Partnerprofil für automatische Zuordnung</strong></summary>
            <div style="max-width:1000px;padding:12px 0 2px">
                <p>Der Geschäftsbereich wird einmal bestätigt. Danach bewertet das System jedes Creative automatisch gegen alle registrierten Portale, deren Kategorien und deren reale Designslots. Lange manuelle Kategorienlisten werden nicht mehr verwendet.</p>
                <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>">
                    <input type="hidden" name="action" value="ppar_partner_profile_save">
                    <input type="hidden" name="provider" value="<?php echo esc_attr($provider); ?>">
                    <input type="hidden" name="external_id" value="<?php echo esc_attr($external_id); ?>">
                    <?php wp_nonce_field('ppar_partner_profile_save', 'ppar_partner_profile_nonce'); ?>
                    <p><label><input type="checkbox" name="profile_enabled" value="1" <?php checked(!empty($profile['enabled'])); ?>> <strong>Profil für automatische Zuordnung verwenden</strong></label></p>
                    <p><label><strong>Bestätigter Geschäftsbereich</strong><br><input type="text" name="business_label" value="<?php echo esc_attr($business_default); ?>" maxlength="180" style="width:620px;max-width:100%"></label><br><span class="description">Awin-Sektor: <?php echo esc_html((string) ($programme['primary_sector'] ?? $programme['primarySector'] ?? 'nicht geliefert')); ?>. Das Partnerprofil darf ein einzelnes unpassendes Creative niemals überstimmen.</span></p>
                    <p><label><strong>Zusätzliche eindeutige Fachbegriffe</strong><br><textarea name="keywords" rows="3" style="width:620px;max-width:100%" placeholder="z. B. konkrete Produkt- oder Leistungsbegriffe"><?php echo esc_textarea(implode("\n", (array) ($profile['keywords'] ?? array()))); ?></textarea></label></p>
                    <p><button class="button button-primary">Profil speichern und vorhandene Creatives neu bewerten</button></p>
                </form>
                <?php if (!empty($profile['listing_id'])) : ?><p class="description">Ein älteres V3.4.0-Listing (ID <?php echo absint($profile['listing_id']); ?>) bleibt als Legacy-Entwurf erhalten und wird nicht automatisch freigegeben. V4.0.0 erzeugt neue Ausgaben ausschließlich aus einem konkreten Creative.</p><?php endif; ?>
            </div>
        </details>
        <?php
    }

    public function render_partner_intake_page() {
        if (!current_user_can('manage_options')) {
            return;
        }
        $joined = $this->partner_intake_joined_awin_programmes();
        $snapshots = $this->partner_intake_snapshots();
        $selected_id = absint($_GET['advertiser_id'] ?? 0);
        if (!$selected_id && $joined) {
            $selected_id = absint(array_key_first($joined));
        }
        $selected_name = sanitize_text_field(rawurldecode((string) ($_GET['partner_name'] ?? '')));
        if ($selected_name === '' && $selected_id > 0 && isset($joined[$selected_id])) {
            $selected_name = $joined[$selected_id];
        }
        $notice = sanitize_key((string) ($_GET['ppar_intake'] ?? ''));
        ?>
        <div class="wrap ppar-partner-intake">
            <h1>Awin-Partneraufnahme</h1>
            <p>Partnerdaten werden ausschließlich read-only in eine lokale Prüfstufe geladen. Es wird nichts veröffentlicht und kein Werbemittel angelegt.</p>
            <?php if ($notice === 'success') : ?><div class="notice notice-success inline"><p>Partnerdaten vollständig abgerufen.</p></div><?php endif; ?>
            <?php if ($notice === 'partial') : ?><div class="notice notice-warning inline"><p>Programmdaten wurden abgerufen; Angebote waren vorübergehend nicht erreichbar.</p></div><?php endif; ?>
            <?php if ($notice === 'failed') : ?><div class="notice notice-error inline"><p><?php echo esc_html(rawurldecode((string) ($_GET['ppar_message'] ?? 'Awin-Abfrage fehlgeschlagen.'))); ?></p></div><?php endif; ?>
            <?php if ($notice === 'not_joined') : ?><div class="notice notice-error inline"><p>Das Programm ist für dieses Publisherkonto nicht als „joined“ bestätigt.</p></div><?php endif; ?>
            <?php if ($notice === 'invalid') : ?><div class="notice notice-error inline"><p><?php echo esc_html(rawurldecode((string) ($_GET['ppar_message'] ?? 'Bitte eine gültige Advertiser-ID eingeben.'))); ?></p></div><?php endif; ?>
            <?php if (sanitize_key((string) ($_GET['ppar_profile'] ?? '')) === 'success') : ?><div class="notice notice-success inline"><p><?php echo esc_html(rawurldecode((string) ($_GET['ppar_message'] ?? 'Partnerprofil gespeichert.'))); ?></p></div><?php endif; ?>
            <?php if (sanitize_key((string) ($_GET['ppar_profile'] ?? '')) === 'failed') : ?><div class="notice notice-error inline"><p><?php echo esc_html(rawurldecode((string) ($_GET['ppar_message'] ?? 'Partnerprofil konnte nicht gespeichert werden.'))); ?></p></div><?php endif; ?>

            <section class="postbox" style="padding:18px;max-width:1100px">
                <h2>Awin-Partner direkt abrufen</h2>
                <form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>">
                    <input type="hidden" name="action" value="ppar_partner_intake_probe">
                    <input type="hidden" name="provider" value="awin">
                    <?php wp_nonce_field('ppar_partner_intake_probe', 'ppar_partner_intake_nonce'); ?>
                    <p><label><strong>Awin-Advertiser-ID</strong><br>
                        <input type="number" min="1" step="1" required name="advertiser_id" value="<?php echo $selected_id > 0 ? absint($selected_id) : ''; ?>" list="ppar-awin-known-programmes" style="width:240px;max-width:100%">
                    </label></p>
                    <?php if ($joined) : ?>
                        <datalist id="ppar-awin-known-programmes">
                            <?php foreach ($joined as $id => $name) : ?><option value="<?php echo absint($id); ?>"><?php echo esc_html($name); ?></option><?php endforeach; ?>
                        </datalist>
                    <?php endif; ?>
                    <p><label><strong>Partnername</strong> <span style="font-weight:400">(optional)</span><br>
                        <input type="text" name="partner_name" value="<?php echo esc_attr($selected_name); ?>" maxlength="180" placeholder="z. B. Cleos DE" style="width:360px;max-width:100%">
                    </label></p>
                    <p><button class="button button-primary">Jetzt direkt über Awin abrufen</button></p>
                    <p class="description">Eine vorherige Programmlisten-Synchronisierung ist nicht erforderlich.</p>
                </form>
            </section>

            <?php if (!$snapshots) : ?>
                <p>Noch kein Partner in der lokalen Prüfstufe.</p>
            <?php else : ?>
                <?php foreach (array_reverse($snapshots, true) as $snapshot) :
                    if (!is_array($snapshot)) { continue; }
                    $programme = is_array($snapshot['programme'] ?? null) ? $snapshot['programme'] : array();
                    $offers = is_array($snapshot['offers'] ?? null) ? $snapshot['offers'] : array();
                    $feeds = is_array($snapshot['feeds'] ?? null) ? $snapshot['feeds'] : array();
                    $capabilities = is_array($snapshot['capabilities'] ?? null) ? $snapshot['capabilities'] : array();
                    $gate_entry = $this->awin_programme_gate_entry(absint($snapshot['external_id'] ?? 0));
                    $gate_labels = $this->awin_programme_gate_statuses();
                    $gate_allowed = $this->awin_programme_gate_is_allowed(absint($snapshot['external_id'] ?? 0));
                    ?>
                    <section class="postbox" style="padding:18px;max-width:1200px">
                        <div style="display:flex;gap:18px;align-items:center;flex-wrap:wrap">
                            <?php if (!empty($programme['logo_url'])) : ?><img src="<?php echo esc_url($programme['logo_url']); ?>" alt="" style="max-width:150px;max-height:80px;object-fit:contain"><?php endif; ?>
                            <div><h2 style="margin:0 0 4px"><?php echo esc_html((string) ($programme['name'] ?? 'Awin-Partner')); ?></h2><p style="margin:0">Awin-ID <?php echo absint($snapshot['external_id'] ?? 0); ?> · Status <?php echo esc_html((string) ($programme['membership_status'] ?? 'joined')); ?> · Abruf <?php echo esc_html(wp_date('d.m.Y H:i', absint($snapshot['captured_at'] ?? 0))); ?></p></div>
                        </div>
                        <p style="margin-top:16px"><?php if ($gate_allowed) : ?><a class="button button-primary" href="<?php echo esc_url(add_query_arg(array('page'=>'affiliate-portal-automation','provider'=>(string)($snapshot['provider'] ?? 'awin'),'partner_external_id'=>(string)($snapshot['external_id'] ?? '')), admin_url('admin.php'))); ?>">Datenlauf für diesen Partner öffnen</a><?php else : ?><button class="button" disabled>Datenlauf gesperrt</button> <span class="description">Zuerst unter „Netzwerke &amp; API“ für dieses Portal aktivieren.</span><?php endif; ?></p>
                        <table class="widefat striped" style="margin-top:16px"><tbody>
                            <tr><th style="width:220px">Awin-Eingangsweiche</th><td><strong><?php echo esc_html($gate_labels[$gate_entry['status']] ?? $gate_labels['pending']); ?></strong></td></tr>
                            <tr><th style="width:220px">Zieldomains</th><td><?php echo esc_html(implode(', ', (array) ($programme['valid_domains'] ?? array())) ?: '—'); ?></td></tr>
                            <tr><th>Deeplinks</th><td><?php echo !empty($programme['deeplink_enabled']) ? 'verfügbar' : 'nicht bestätigt'; ?></td></tr>
                            <tr><th>Aktive Angebote</th><td><?php echo count($offers); ?></td></tr>
                            <tr><th>Passende Produktfeeds</th><td><?php echo count($feeds); ?></td></tr>
                            <tr><th>Bannerkatalog per API</th><td><?php echo !empty($capabilities['creative_catalogue']) ? 'verfügbar' : 'nicht dokumentiert'; ?></td></tr>
                            <tr><th>Öffentliche Ausgabe</th><td><strong>gesperrt</strong></td></tr>
                        </tbody></table>
                        <?php if (!empty($programme['description'])) : ?><details style="margin-top:14px"><summary>Programmbeschreibung</summary><div style="max-width:900px;padding:10px 0"><?php echo wp_kses_post((string) $programme['description']); ?></div></details><?php endif; ?>
                        <?php $this->partner_profile_render_form($snapshot); ?>
                        <?php if ($offers) : ?>
                            <h3>Aktive Angebote</h3>
                            <table class="widefat striped"><thead><tr><th>Titel</th><th>Art</th><th>Gültig bis</th><th>Trackinglink</th></tr></thead><tbody>
                            <?php foreach (array_slice($offers, 0, 50) as $offer) : ?>
                                <tr><td><?php echo esc_html((string) ($offer['title'] ?? '')); ?></td><td><?php echo esc_html((string) ($offer['type'] ?? 'promotion')); ?></td><td><?php echo esc_html($this->partner_intake_display_date($offer['end_date'] ?? '')); ?></td><td><?php echo !empty($offer['tracking_url']) ? 'vorhanden' : 'fehlt'; ?></td></tr>
                            <?php endforeach; ?>
                            </tbody></table>
                        <?php endif; ?>
                        <?php if ($feeds) : ?>
                            <h3>Gefundene Feedquellen</h3>
                            <ul><?php foreach ($feeds as $feed) : ?><li><?php echo esc_html((string) ($feed['feed_name'] ?? $feed['advertiser_name'] ?? $feed['merchant_name'] ?? 'Awin-Produktfeed')); ?></li><?php endforeach; ?></ul>
                        <?php endif; ?>
                    </section>
                <?php endforeach; ?>
            <?php endif; ?>
        </div>
        <?php
    }
}
