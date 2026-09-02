<?php
if (!defined('ABSPATH')) { exit; }

/**
 * KISS navigation plus the single manual affiliate import entry requested by the
 * current user scope. Existing specialist pages stay registered and reachable.
 */
final class PPAR_Affiliate_Admin_KISS {
    const IMPORT_ACTION = 'ppar_universal_manual_import';
    const IMPORT_NONCE_ACTION = 'ppar_universal_manual_import';
    const IMPORT_NONCE_FIELD = 'ppar_universal_import_nonce';
    const IMPORT_LAST_OPTION = 'ppar_universal_import_last_v1';
    const DS24_INVENTORY_OPTION = 'ppar_digistore24_manual_inventory_v1';
    const DS24_MARKETPLACE_OPTION = 'ppar_digistore24_marketplace_v1';
    const MAX_SAMPLE_BYTES = 1048576;
    const MAX_DS24_DECOMPRESSED_BYTES = 33554432;
    private static $booted = false;

    public static function bootstrap() {
        if (self::$booted) { return; }
        self::$booted = true;
        add_action('admin_menu', array(__CLASS__, 'register_visible_navigation'), 10050);
        add_action('admin_head', array(__CLASS__, 'hide_legacy_navigation_css'), 10050);
        add_action('admin_post_' . self::IMPORT_ACTION, array(__CLASS__, 'handle_universal_import'));
        add_filter('pre_update_option_' . self::DS24_MARKETPLACE_OPTION, array(__CLASS__, 'preserve_manual_ds24_inventory'), 20, 3);
    }

    private static function parent_slug() { return 'affiliate-portal-zentrale'; }

    private static function hidden_legacy_slugs() {
        return array(
            'affiliate-portal-creative-library','affiliate-portal-outputs','affiliate-portal-control',
            'affiliate-portal-creatives','affiliate-portal-assignments','affiliate-portal-preview',
            'affiliate-portal-ebay-business','affiliate-portal-coverage','affiliate-portal-article-hybrid',
            'affiliate-portal-networks','affiliate-portal-provider-awin','affiliate-portal-provider-adcell',
            'affiliate-portal-ebay','affiliate-portal-provider-idealo','affiliate-portal-provider-digistore24',
            'affiliate-portal-partners','affiliate-portal-sync','affiliate-portal-automation',
            'affiliate-portal-stats','affiliate-portal-health','affiliate-portal-deals'
        );
    }

    public static function register_visible_navigation() {
        if (!function_exists('add_submenu_page')) { return; }
        $parent = self::parent_slug();
        add_submenu_page($parent,'Produkte & Deals','Produkte & Deals','manage_options','affiliate-portal-kiss-products',array(__CLASS__,'render_products'));
        add_submenu_page($parent,'Partner & Einnahmen','Partner & Einnahmen','manage_options','affiliate-portal-kiss-partners',array(__CLASS__,'render_partners'));
        add_submenu_page($parent,'Ausspielung','Ausspielung','manage_options','affiliate-portal-kiss-delivery',array(__CLASS__,'render_delivery'));
        add_submenu_page($parent,'Anbieter & APIs','Anbieter & APIs','manage_options','affiliate-portal-kiss-providers',array(__CLASS__,'render_providers'));
        add_submenu_page($parent,'Steuerung & System','Steuerung & System','manage_options','affiliate-portal-kiss-system',array(__CLASS__,'render_system'));
    }

    public static function hide_legacy_navigation_css() {
        if (!current_user_can('manage_options')) { return; }
        $selectors = array();
        foreach (self::hidden_legacy_slugs() as $slug) {
            $selectors[] = '#toplevel_page_' . self::parent_slug() . ' .wp-submenu a[href="admin.php?page=' . $slug . '"]';
            $selectors[] = '#toplevel_page_' . self::parent_slug() . ' .wp-submenu a[href$="page=' . $slug . '"]';
        }
        if (!$selectors) { return; }
        echo '<style id="ppar-kiss-legacy-nav-hide">' . implode(',', $selectors) . '{display:none!important}</style>';
    }

    private static function button($label, $slug, $primary = false) {
        $class = $primary ? 'button button-primary' : 'button';
        return '<a class="'.esc_attr($class).'" href="'.esc_url(admin_url('admin.php?page='.$slug)).'">'.esc_html($label).'</a>';
    }

    private static function header($title, $lead) {
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.'); }
        echo '<div class="wrap" style="max-width:1240px"><h1>'.esc_html($title).'</h1><p>'.esc_html($lead).'</p>';
    }

    private static function footer() { echo '</div>'; }

    private static function source_cards($sources) {
        echo '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:14px;margin:18px 0">';
        foreach ((array)$sources as $source) {
            if (!is_array($source)) { continue; }
            $state = sanitize_key((string)($source['state'] ?? 'prepared'));
            $label = (string)($source['label'] ?? 'Quelle');
            echo '<section class="postbox" style="padding:16px;margin:0"><h2 style="margin-top:0">'.esc_html($label).'</h2>';
            echo '<p><strong>'.esc_html($state === 'active' ? 'Aktiv' : 'Vorbereitet').'</strong></p>';
            if (!empty($source['purpose'])) { echo '<p>'.esc_html((string)$source['purpose']).'</p>'; }
            if (!empty($source['route'])) { echo '<p class="description">Technischer Weg: '.esc_html((string)$source['route']).'</p>'; }
            if (!empty($source['activation'])) { echo '<p class="description">Aktivierung: '.esc_html((string)$source['activation']).'</p>'; }
            if (!empty($source['note'])) { echo '<p><strong>'.esc_html((string)$source['note']).'</strong></p>'; }
            echo '</section>';
        }
        echo '</div>';
    }

    public static function render_products() {
        self::header('Produkte & Deals','Gesamtabdeckung statt eBay-Alleinabdeckung. Produktquellen bleiben strikt von Banner-Netzwerken getrennt.');
        if (class_exists('PPAR_Affiliate_Source_Plan')) { self::source_cards(PPAR_Affiliate_Source_Plan::product_sources()); }
        echo '<p style="display:flex;gap:8px;flex-wrap:wrap">';
        echo self::button('Produktquellen & Deal-Radar','affiliate-portal-deals',true);
        echo self::button('Import & Auswahl','affiliate-portal-creative-library');
        echo self::button('eBay Produktzuordnung','affiliate-portal-ebay-business');
        echo self::button('Portalabdeckung','affiliate-portal-coverage');
        echo self::button('Vorschau','affiliate-portal-preview');
        echo '</p>';
        self::footer();
    }

    public static function render_partners() {
        if (class_exists('PPAR_Partner_Analytics_Admin')) {
            PPAR_Partner_Analytics_Admin::render_page();
            return;
        }
        self::header('Partner & Einnahmen','Banner-/Partnernetzwerke, Produktquellen und echte Einnahmendaten an einer Stelle. Fehlende Werte werden nicht geschätzt.');
        if (class_exists('PPAR_Affiliate_Source_Plan')) {
            self::source_cards(array_merge((array)PPAR_Affiliate_Source_Plan::product_sources(),(array)PPAR_Affiliate_Source_Plan::banner_networks()));
        }
        echo '<p style="display:flex;gap:8px;flex-wrap:wrap">';
        echo self::button('Partner & Einnahmen','affiliate-portal-stats',true);
        echo self::button('Partner','affiliate-portal-partners');
        echo self::button('Werbemittel','affiliate-portal-creatives');
        echo self::button('Digistore24','affiliate-portal-provider-digistore24');
        echo '</p>';
        self::footer();
    }

    public static function render_delivery() {
        self::header('Ausspielung','Alle bisherigen Ausgabefunktionen bleiben erhalten; nur die Navigation ist zusammengefasst.');
        echo '<p style="display:flex;gap:8px;flex-wrap:wrap">';
        echo self::button('Ausgaben & Freigabe','affiliate-portal-outputs',true);
        echo self::button('Zuordnungen','affiliate-portal-assignments');
        echo self::button('Einzelbeiträge','affiliate-portal-article-hybrid');
        echo self::button('Vorschau','affiliate-portal-preview');
        echo '</p>';
        self::footer();
    }

    public static function render_providers() {
        self::header('Anbieter & APIs','Zugänge und technische Provider bleiben getrennt von der fachlichen Produkt-/Banner-Ausspielung.');
        self::render_import_form();
        echo '<p style="display:flex;gap:8px;flex-wrap:wrap">';
        echo self::button('Netzwerke & API','affiliate-portal-networks',true);
        echo self::button('Synchronisierung','affiliate-portal-sync');
        echo self::button('Awin','affiliate-portal-provider-awin');
        echo self::button('ADCELL','affiliate-portal-provider-adcell');
        echo self::button('eBay','affiliate-portal-ebay');
        echo self::button('idealo','affiliate-portal-provider-idealo');
        echo self::button('Digistore24','affiliate-portal-provider-digistore24');
        echo '</p>';
        echo '<p class="description">OTTO, Kelkoo, Kaufland, Amazon und ADCocktail erscheinen als vorbereitet, bis ein realer, dokumentierter Zugang vorhanden ist. Es werden keine Schnittstellen geraten.</p>';
        self::footer();
    }

    public static function render_system() {
        self::header('Steuerung & System','Chef-Veto, Automatisierung und Prüfungen bleiben vollständig verfügbar.');
        echo '<p style="display:flex;gap:8px;flex-wrap:wrap">';
        echo self::button('Steuerung & Veto','affiliate-portal-control',true);
        echo self::button('Automatisierung','affiliate-portal-automation');
        echo self::button('Prüfzentrum','affiliate-portal-health');
        echo '</p>';
        self::footer();
    }

    private static function render_import_form() {
        $notice = sanitize_key((string)($_GET['ppar_universal_import'] ?? ''));
        $message = rawurldecode((string)($_GET['ppar_universal_message'] ?? ''));
        $last = get_option(self::IMPORT_LAST_OPTION, array());
        $last = is_array($last) ? $last : array();
        echo '<section class="postbox" style="padding:16px;margin:18px 0;max-width:900px">';
        echo '<h2 style="margin-top:0">Datei importieren</h2>';
        echo '<p>Eine Datei hochladen. Die Affiliate-Zentrale erkennt den Anbieter selbst. Unklare oder widersprüchliche Dateien werden ohne Datenänderung abgewiesen.</p>';
        if ($notice === 'success') { echo '<div class="notice notice-success inline"><p>'.esc_html($message).'</p></div>'; }
        if ($notice === 'failed') { echo '<div class="notice notice-error inline"><p>'.esc_html($message).'</p></div>'; }
        echo '<form method="post" action="'.esc_url(admin_url('admin-post.php')).'" enctype="multipart/form-data">';
        echo '<input type="hidden" name="action" value="'.esc_attr(self::IMPORT_ACTION).'">';
        wp_nonce_field(self::IMPORT_NONCE_ACTION, self::IMPORT_NONCE_FIELD);
        echo '<p><input type="file" name="affiliate_import_file" accept=".csv,.csv.gz,.json,.txt,.gz" required></p>';
        echo '<p><button class="button button-primary" type="submit">Datei prüfen &amp; importieren</button></p>';
        echo '<p class="description">Unterstützt: Digistore24-Partnerschaftsexport, idealo-Standardfeed sowie eindeutig erkennbare Awin-/ADCELL-Werbemitteldateien. eBay wird erkannt, aber nicht in einen falschen Dateiimport gezwungen.</p>';
        echo '</form>';
        if (!empty($last['provider']) && !empty($last['imported_at'])) {
            echo '<p class="description"><strong>Letzter Import:</strong> '.esc_html((string)$last['provider']).' · '.esc_html(wp_date('d.m.Y H:i',absint($last['imported_at'])));
            if (!empty($last['message'])) { echo ' · '.esc_html((string)$last['message']); }
            echo '</p>';
        }
        echo '</section>';
    }

    public static function handle_universal_import() {
        if (!current_user_can('manage_options')) { wp_die('Keine Berechtigung.'); }
        check_admin_referer(self::IMPORT_NONCE_ACTION, self::IMPORT_NONCE_FIELD);
        $file = $_FILES['affiliate_import_file'] ?? null;
        if (!is_array($file) || (int)($file['error'] ?? UPLOAD_ERR_NO_FILE) !== UPLOAD_ERR_OK || empty($file['tmp_name']) || !is_uploaded_file($file['tmp_name'])) {
            self::import_redirect('failed','Dateiupload fehlgeschlagen.');
        }
        $size = (int)($file['size'] ?? 0);
        $limit = function_exists('wp_max_upload_size') ? (int)wp_max_upload_size() : 0;
        if ($size <= 0 || ($limit > 0 && $size > $limit)) { self::import_redirect('failed','Die Datei ist leer oder größer als das Server-Uploadlimit.'); }
        $name = sanitize_file_name((string)($file['name'] ?? 'import'));
        if (!preg_match('/\.(?:csv|json|txt|csv\.gz|gz)$/i',$name)) { self::import_redirect('failed','Zulässig sind CSV, CSV.GZ, JSON oder TXT.'); }
        $sample = self::read_text((string)$file['tmp_name'],$name,self::MAX_SAMPLE_BYTES);
        if (is_wp_error($sample)) { self::import_redirect('failed',$sample->get_error_message()); }
        $detected = self::detect_provider($name,$sample);
        if (is_wp_error($detected)) { self::import_redirect('failed',$detected->get_error_message()); }
        $kind = (string)$detected['kind'];
        if ($kind === 'digistore24_partnerships') {
            $result = self::import_digistore24_partnerships((string)$file['tmp_name'],$name);
            if (is_wp_error($result)) { self::import_redirect('failed',$result->get_error_message()); }
            self::remember_import('Digistore24',(string)$result['message'],(string)$result['sha256']);
            self::import_redirect('success',(string)$result['message']);
        }
        if ($kind === 'idealo_feed') { self::delegate_idealo($file); }
        if ($kind === 'awin_creatives') { self::delegate_creatives($file,'awin',$name); }
        if ($kind === 'adcell_creatives') { self::delegate_creatives($file,'adcell',$name); }
        if ($kind === 'digistore24_creatives') { self::delegate_creatives($file,'digistore24',$name); }
        if ($kind === 'ebay_detected') { self::import_redirect('failed','eBay-Datei erkannt. Der bestehende eBay-Produktpfad ist API-basiert; die Datei wird nicht in einen falschen Importpfad umgeleitet.'); }
        self::import_redirect('failed','Anbieter erkannt, aber für dieses Dateiformat existiert kein freigegebener manueller Importpfad.');
    }

    private static function read_text($path,$name,$limit) {
        if (!is_readable($path)) { return new WP_Error('universal_import_unreadable','Importdatei ist nicht lesbar.'); }
        $gzip = preg_match('/\.gz$/i',(string)$name) === 1;
        $body = '';
        if ($gzip) {
            if (!function_exists('gzopen')) { return new WP_Error('universal_import_gzip_missing','GZIP-Unterstützung fehlt auf dem Server.'); }
            $h = @gzopen($path,'rb');
            if (!$h) { return new WP_Error('universal_import_gzip_open','GZIP-Datei konnte nicht geöffnet werden.'); }
            while (!gzeof($h) && strlen($body) < $limit) {
                $chunk = gzread($h,min(262144,$limit-strlen($body)));
                if ($chunk === false) { gzclose($h); return new WP_Error('universal_import_gzip_read','GZIP-Datei konnte nicht gelesen werden.'); }
                $body .= $chunk;
            }
            gzclose($h);
        } else {
            $body = (string)@file_get_contents($path,false,null,0,$limit);
        }
        if ($body === '') { return new WP_Error('universal_import_empty','Datei enthält keine lesbaren Daten.'); }
        return self::normalize_encoding($body);
    }

    private static function read_full_ds24($path,$name) {
        if (!preg_match('/\.gz$/i',(string)$name)) {
            $size = @filesize($path);
            if ($size !== false && $size > self::MAX_DS24_DECOMPRESSED_BYTES) { return new WP_Error('universal_import_too_large','Digistore24-Partnerschaftsdatei überschreitet 32 MiB.'); }
            $body = (string)@file_get_contents($path);
            return $body === '' ? new WP_Error('universal_import_empty','Datei ist leer.') : self::normalize_encoding($body);
        }
        if (!function_exists('gzopen')) { return new WP_Error('universal_import_gzip_missing','GZIP-Unterstützung fehlt auf dem Server.'); }
        $h = @gzopen($path,'rb');
        if (!$h) { return new WP_Error('universal_import_gzip_open','GZIP-Datei konnte nicht geöffnet werden.'); }
        $body = '';
        $hard = self::MAX_DS24_DECOMPRESSED_BYTES;
        while (!gzeof($h) && strlen($body) <= $hard) {
            $remaining = ($hard + 1) - strlen($body);
            $chunk = gzread($h,min(262144,$remaining));
            if ($chunk === false) { gzclose($h); return new WP_Error('universal_import_gzip_read','GZIP-Datei konnte nicht gelesen werden.'); }
            $body .= $chunk;
        }
        gzclose($h);
        if (strlen($body) > $hard) { return new WP_Error('universal_import_too_large','Digistore24-Partnerschaftsdatei überschreitet dekomprimiert 32 MiB.'); }
        if ($body === '') { return new WP_Error('universal_import_empty','Datei ist leer.'); }
        return self::normalize_encoding($body);
    }

    private static function normalize_encoding($body) {
        $body = preg_replace('/^\xEF\xBB\xBF/','',(string)$body);
        if (function_exists('mb_check_encoding') && !mb_check_encoding($body,'UTF-8') && function_exists('mb_convert_encoding')) {
            $body = mb_convert_encoding($body,'UTF-8','Windows-1252,ISO-8859-1,UTF-8');
        }
        return $body;
    }

    private static function import_key($value) {
        $value = trim((string)$value);
        if (function_exists('remove_accents')) { $value = remove_accents($value); }
        else { $value = strtr($value,array('Ä'=>'A','Ö'=>'O','Ü'=>'U','ä'=>'a','ö'=>'o','ü'=>'u','ß'=>'ss')); }
        return trim((string)preg_replace('/[^a-z0-9]+/','_',strtolower($value)),'_');
    }

    private static function delimiter($line) {
        $best = ','; $score = -1;
        foreach (array(';',',',"\t",'|') as $d) {
            $count = substr_count((string)$line,$d);
            if ($count > $score) { $score = $count; $best = $d; }
        }
        return $best;
    }

    private static function headers($sample) {
        $first = preg_split('/\r\n|\r|\n/',(string)$sample,2);
        $raw = str_getcsv((string)($first[0] ?? ''),self::delimiter($first[0] ?? ''),'"','\\');
        return array_values(array_filter(array_map(array(__CLASS__,'import_key'),(array)$raw),'strlen'));
    }

    private static function has_header($headers,$aliases) {
        $set = array_fill_keys((array)$headers,true);
        foreach ((array)$aliases as $alias) { if (isset($set[self::import_key($alias)])) { return true; } }
        return false;
    }

    private static function ds24_headers($headers) {
        return self::has_header($headers,array('vendor','vendorname','anbieter'))
            && self::has_header($headers,array('produkt-id','produkt_id','product_id','productid'))
            && self::has_header($headers,array('produkt','produktname','product','product_name'))
            && self::has_header($headers,array('werbemittel-id','werbemittel_id','marketplace_entry_id','entry_id'))
            && self::has_header($headers,array('status der partnerschaft','partnerschaftsstatus','status','approval_status'))
            && self::has_header($headers,array('provision','affiliate-provision','affiliate_provision','commission','commission_rate'));
    }

    private static function idealo_headers($headers) {
        foreach (array('id','product_title','product_deeplink','ean','gtins_product','asins_product','main_category','sub_category','brand_name') as $required) {
            if (!in_array($required,$headers,true)) { return false; }
        }
        return in_array('image_url',$headers,true) || in_array('image_url_1',$headers,true);
    }

    private static function detect_provider($name,$sample) {
        $headers = self::headers($sample);
        if (self::ds24_headers($headers)) { return array('provider'=>'digistore24','kind'=>'digistore24_partnerships','confidence'=>'exact_headers'); }
        $lower = strtolower((string)$sample);
        $signals = array();
        if (preg_match('/^productdata_[0-9]+\.csv(?:\.gz)?$/i',basename(strtolower((string)$name))) && self::idealo_headers($headers)) { $signals[] = 'idealo_feed'; }
        if (strpos($lower,'awin1.com') !== false || strpos($lower,'zenaps.com') !== false) { $signals[] = 'awin_creatives'; }
        if (strpos($lower,'adcell.de') !== false || strpos($lower,'t.adcell.com') !== false) { $signals[] = 'adcell_creatives'; }
        $ds24_link = strpos($lower,'checkout-ds24.com') !== false || strpos($lower,'digistore24.com') !== false;
        $ds24_creative = strpos($lower,'<img') !== false || preg_match('/(?:banner_url|image_url|image_source|tracking_url|affiliate_url|click_url)/i',$sample);
        if ($ds24_link && $ds24_creative) { $signals[] = 'digistore24_creatives'; }
        if (strpos($lower,'ebay.') !== false && (strpos($lower,'itemid') !== false || strpos($lower,'item_id') !== false || strpos($lower,'epn') !== false)) { $signals[] = 'ebay_detected'; }
        $signals = array_values(array_unique($signals));
        if (count($signals) === 1) { return array('kind'=>$signals[0],'confidence'=>'strong_signature'); }
        if (count($signals) > 1) { return new WP_Error('universal_import_ambiguous','Datei enthält widersprüchliche Provider-Signaturen und wird nicht geraten.'); }
        return new WP_Error('universal_import_unknown','Anbieter konnte aus dieser Datei nicht sicher erkannt werden. Keine Daten wurden verändert.');
    }

    private static function ds24_aliases() {
        return array(
            'vendor'=>array('vendor','vendorname','anbieter'),
            'product_id'=>array('produkt-id','produkt_id','produktid','product-id','product_id','productid'),
            'product'=>array('produkt','produktname','product','product_name'),
            'entry_id'=>array('werbemittel-id','werbemittel_id','werbemittelid','marketplace_entry_id','entry_id'),
            'status'=>array('status der partnerschaft','partnerschaftsstatus','status','approval_status'),
            'commission'=>array('provision','affiliate-provision','affiliate_provision','commission','commission_rate'),
            'support_url'=>array('werbemittelseite','werbemittel-seite','werbemittel_url','support_url','affiliate_support_url'),
            'promolink'=>array('promolink','promo-link','promo_link','affiliate_link','tracking_link')
        );
    }

    private static function ds24_columns($headers) {
        $normalized = array();
        foreach ((array)$headers as $index=>$header) { $normalized[self::import_key($header)] = $index; }
        $out = array();
        foreach (self::ds24_aliases() as $field=>$aliases) {
            foreach ($aliases as $alias) {
                $key = self::import_key($alias);
                if (array_key_exists($key,$normalized)) { $out[$field] = $normalized[$key]; break; }
            }
        }
        return $out;
    }

    private static function parse_ds24_csv($body) {
        $body = self::normalize_encoding($body);
        $first = preg_split('/\r\n|\r|\n/',$body,2);
        $delimiter = self::delimiter($first[0] ?? '');
        $fh = fopen('php://temp','r+');
        if (!$fh) { return new WP_Error('ds24_csv_stream','CSV konnte nicht verarbeitet werden.'); }
        fwrite($fh,$body); rewind($fh);
        $headers = fgetcsv($fh,0,$delimiter,'"','\\');
        if (!is_array($headers)) { fclose($fh); return new WP_Error('ds24_csv_headers','CSV-Kopfzeile fehlt.'); }
        $cols = self::ds24_columns($headers);
        foreach (array('vendor','product_id','product','entry_id','status','commission') as $required) {
            if (!array_key_exists($required,$cols)) { fclose($fh); return new WP_Error('ds24_csv_schema','Digistore24-CSV hat nicht die erwarteten Partnerschaftsspalten.'); }
        }
        $rows = array(); $blocked = 0; $seen = 0;
        while (($values = fgetcsv($fh,0,$delimiter,'"','\\')) !== false) {
            if (++$seen > 5000) { fclose($fh); return new WP_Error('ds24_csv_row_limit','Mehr als 5.000 Partnerschaftszeilen werden nicht in einem Lauf verarbeitet.'); }
            if (!array_filter($values,static function($x){ return trim((string)$x) !== ''; })) { continue; }
            $get = static function($field) use ($cols,$values) { return array_key_exists($field,$cols) ? trim((string)($values[$cols[$field]] ?? '')) : ''; };
            $status = self::import_key($get('status'));
            if (!in_array($status,array('genehmigt','approved'),true)) { $blocked++; continue; }
            $vendor = sanitize_text_field($get('vendor'));
            $product_id = preg_replace('/\s+/','',$get('product_id'));
            $product = sanitize_text_field($get('product'));
            $entry_id = preg_replace('/\s+/','',$get('entry_id'));
            if ($vendor === '' || $product === '' || !ctype_digit($product_id) || !ctype_digit($entry_id)) { $blocked++; continue; }
            if (isset($rows[$product_id])) { fclose($fh); return new WP_Error('ds24_csv_product_id_duplicate','Dieselbe Digistore24-Produkt-ID kommt mehrfach in der Bestandsdatei vor. Import wird vollständig abgebrochen.'); }
            $support = $get('support_url');
            $promo = $get('promolink');
            if ($support !== '' && (!filter_var($support,FILTER_VALIDATE_URL) || stripos($support,'https://') !== 0)) { $support = ''; }
            if ($promo !== '' && (!filter_var($promo,FILTER_VALIDATE_URL) || stripos($promo,'https://') !== 0)) { $promo = ''; }
            $rows[$product_id] = array('vendor'=>$vendor,'product_id'=>$product_id,'product'=>$product,'entry_id'=>$entry_id,'status'=>'approved','commission'=>sanitize_text_field($get('commission')),'support_url'=>$support,'promolink'=>$promo);
        }
        fclose($fh);
        if (!$rows) { return new WP_Error('ds24_csv_no_approved','Keine genehmigte Digistore24-Partnerschaft erkannt.'); }
        return array('rows'=>$rows,'blocked'=>$blocked);
    }

    private static function current_ds24_identity() {
        $settings = get_option('ppar_network_digistore24_v1',array());
        $settings = is_array($settings) ? $settings : array();
        $key = defined('PPAR_DIGISTORE24_API_KEY') && trim((string)PPAR_DIGISTORE24_API_KEY) !== '' ? trim((string)PPAR_DIGISTORE24_API_KEY) : trim((string)($settings['api_key'] ?? ''));
        $fingerprint = strtolower(trim((string)($settings['tested_key_fingerprint'] ?? '')));
        $affiliate = trim((string)($settings['affiliate_id'] ?? ''));
        if ($key === '' || !preg_match('/^[a-f0-9]{64}$/',$fingerprint) || !hash_equals($fingerprint,hash('sha256',$key)) || !preg_match('/^[0-9A-Za-z._-]+$/',$affiliate)) {
            return new WP_Error('ds24_manual_identity_required','Digistore24-Datei erkannt. Vor dem Import muss derselbe Digistore24-Zugang unter Anbieter & APIs einmal erfolgreich read-only geprüft sein.');
        }
        return array('key_fingerprint'=>$fingerprint,'affiliate_id'=>$affiliate);
    }

    private static function group_ds24_rows($rows) {
        $groups = array();
        foreach ((array)$rows as $product_id=>$row) {
            $entry_id = (string)$row['entry_id'];
            if (!isset($groups[$entry_id])) {
                $groups[$entry_id] = array('vendor'=>(string)$row['vendor'],'product_ids'=>array(),'products'=>array(),'commissions'=>array(),'support_url'=>(string)$row['support_url'],'promolink'=>(string)$row['promolink']);
            }
            if ($groups[$entry_id]['vendor'] !== (string)$row['vendor']) { return new WP_Error('ds24_csv_entry_vendor_conflict','Dieselbe Werbemittel-ID ist mehreren Vendoren zugeordnet. Import wird vollständig abgebrochen.'); }
            $groups[$entry_id]['product_ids'][(string)$product_id] = (string)$product_id;
            $groups[$entry_id]['products'][(string)$product_id] = (string)$row['product'];
            $groups[$entry_id]['commissions'][(string)$product_id] = (string)$row['commission'];
            if ($groups[$entry_id]['support_url'] === '' && !empty($row['support_url'])) { $groups[$entry_id]['support_url'] = (string)$row['support_url']; }
            if ($groups[$entry_id]['promolink'] === '' && !empty($row['promolink'])) { $groups[$entry_id]['promolink'] = (string)$row['promolink']; }
        }
        return $groups;
    }

    private static function commission_number($value) {
        $value = str_replace(array('%',' '),'',(string)$value);
        $value = str_replace(',','.',$value);
        return is_numeric($value) ? (float)$value : null;
    }

    private static function import_digistore24_partnerships($path,$name) {
        $identity = self::current_ds24_identity();
        if (is_wp_error($identity)) { return $identity; }
        $body = self::read_full_ds24($path,$name);
        if (is_wp_error($body)) { return $body; }
        $parsed = self::parse_ds24_csv($body);
        if (is_wp_error($parsed)) { return $parsed; }
        $groups = self::group_ds24_rows($parsed['rows']);
        if (is_wp_error($groups)) { return $groups; }

        $sha = hash('sha256',$body); $now = time();
        $old_store = get_option(self::DS24_MARKETPLACE_OPTION,array());
        $old_store = is_array($old_store) ? $old_store : array();
        $old_items = array();
        foreach ((array)($old_store['items'] ?? array()) as $item) { if (is_array($item) && !empty($item['id'])) { $old_items[(string)$item['id']] = $item; } }
        $new_ids = array_fill_keys(array_keys($groups),true);
        $items = array(); $removed = 0;
        foreach ($old_items as $entry_id=>$item) {
            if ((string)($item['source_kind'] ?? '') === 'digistore24_manual_csv' && !isset($new_ids[$entry_id])) { $removed++; continue; }
            if ((string)($item['source_kind'] ?? '') !== 'digistore24_manual_csv' && !isset($new_ids[$entry_id])) { $items[$entry_id] = $item; }
        }
        foreach ($groups as $entry_id=>$group) {
            $old = $old_items[$entry_id] ?? array();
            $product_ids = array_values($group['product_ids']); sort($product_ids,SORT_STRING);
            $products = $group['products']; ksort($products,SORT_STRING);
            $support = (string)$group['support_url'];
            if ($support === '' && !empty($old['support_url']) && filter_var($old['support_url'],FILTER_VALIDATE_URL) && stripos((string)$old['support_url'],'https://') === 0) { $support = (string)$old['support_url']; }
            $promo = (string)$group['promolink'];
            if ($promo === '' && !empty($old['promolink']) && filter_var($old['promolink'],FILTER_VALIDATE_URL) && stripos((string)$old['promolink'],'https://') === 0) { $promo = (string)$old['promolink']; }
            $description = array(); foreach ($products as $product_id=>$title) { $description[] = $product_id.' · '.$title; }
            $items[$entry_id] = array(
                'id'=>(string)$entry_id,'main_product_id'=>(string)$product_ids[0],'all_product_ids'=>$product_ids,
                'approval_status'=>'approved','approval_status_msg'=>'Genehmigt · manueller Digistore24-CSV-Import',
                'headline'=>count($product_ids) === 1 ? (string)reset($products) : (string)$group['vendor'].' · '.count($product_ids).' Produkte',
                'description'=>implode("\n",$description),'product_category'=>'','product_category_id'=>0,'affiliate_share'=>null,
                'stats_stars'=>null,'stats_count_orders'=>0,'vendor'=>(string)$group['vendor'],'commissions'=>$group['commissions'],
                'support_url'=>$support,'promolink'=>$promo,'source_kind'=>'digistore24_manual_csv','manual_import_sha256'=>$sha,'manual_imported_at'=>$now
            );
        }
        ksort($items,SORT_STRING);

        $partnerships = get_option('ppar_digistore24_partnerships_v1',array());
        $partnerships = is_array($partnerships) ? $partnerships : array();
        foreach ($partnerships as $entry_id=>$record) {
            if (is_array($record) && (string)($record['source'] ?? '') === 'manual_csv' && !isset($new_ids[(string)$entry_id])) { unset($partnerships[$entry_id]); }
        }
        foreach ($groups as $entry_id=>$group) {
            $old = is_array($partnerships[$entry_id] ?? null) ? $partnerships[$entry_id] : array();
            $product_ids = array_values($group['product_ids']); sort($product_ids,SORT_STRING);
            $partnerships[$entry_id] = array(
                'confirmed'=>1,'confirmed_at'=>absint($old['confirmed_at'] ?? 0) ?: $now,
                'key_fingerprint'=>$identity['key_fingerprint'],'affiliate_id'=>$identity['affiliate_id'],'source'=>'manual_csv',
                'approval_status'=>'approved','product_ids'=>$product_ids,'vendor'=>$group['vendor'],'products'=>$group['products'],
                'commissions'=>$group['commissions'],'imported_at'=>$now,'import_sha256'=>$sha
            );
        }

        $affiliations = get_option('ppar_digistore24_affiliations_v1',array());
        $affiliations = is_array($affiliations) ? $affiliations : array();
        $current_products = array_fill_keys(array_keys($parsed['rows']),true);
        foreach ($affiliations as $product_id=>$proof) {
            if (is_array($proof) && (string)($proof['source'] ?? '') === 'manual_csv' && !isset($current_products[(string)$product_id])) { unset($affiliations[$product_id]); }
        }
        foreach ($parsed['rows'] as $product_id=>$row) {
            $affiliations[$product_id] = array(
                'product_id'=>(string)$product_id,'product_is_active'=>true,'approval_status'=>'approved',
                'commission_rate'=>self::commission_number($row['commission']),'checked_at'=>$now,
                'key_fingerprint'=>$identity['key_fingerprint'],'affiliate_id'=>$identity['affiliate_id'],
                'source'=>'manual_csv','import_sha256'=>$sha
            );
        }

        $vendors = array_values(array_unique(array_map(static function($row){ return (string)$row['vendor']; },array_values($parsed['rows']))));
        sort($vendors,SORT_NATURAL|SORT_FLAG_CASE);
        $inventory = array(
            'rows'=>$parsed['rows'],'product_count'=>count($parsed['rows']),'source_count'=>count($groups),'vendors'=>$vendors,
            'blocked'=>absint($parsed['blocked'] ?? 0),'imported_at'=>$now,'sha256'=>$sha,
            'key_fingerprint'=>$identity['key_fingerprint'],'affiliate_id'=>$identity['affiliate_id']
        );
        $store = array_merge($old_store,array(
            'items'=>array_values($items),'last_checked'=>$now,'last_status'=>'manual_import',
            'last_message'=>count($parsed['rows']).' genehmigte Produktpartnerschaften aus Digistore24-CSV übernommen; '.count($groups).' Werbemittelquellen; '.count($vendors).' Vendoren.',
            'blocked'=>absint($parsed['blocked'] ?? 0),'key_fingerprint'=>$identity['key_fingerprint'],'affiliate_id'=>$identity['affiliate_id']
        ));

        update_option(self::DS24_INVENTORY_OPTION,$inventory,false);
        update_option(self::DS24_MARKETPLACE_OPTION,$store,false);
        update_option('ppar_digistore24_partnerships_v1',$partnerships,false);
        update_option('ppar_digistore24_affiliations_v1',$affiliations,false);

        $message = 'Digistore24 erkannt · '.count($parsed['rows']).' genehmigte Produktpartnerschaften · '.count($groups).' Werbemittelquellen · '.count($vendors).' Vendoren';
        if (!empty($parsed['blocked'])) { $message .= ' · '.absint($parsed['blocked']).' nicht genehmigte/ungültige Zeilen blockiert'; }
        if ($removed > 0) { $message .= ' · '.$removed.' alte manuelle Quelle(n) aus der Inventur entfernt'; }
        $message .= '. Bestehende veröffentlichte LKG-Ausgaben wurden nicht verändert.';
        return array('status'=>'success','message'=>$message,'sha256'=>$sha,'product_count'=>count($parsed['rows']),'source_count'=>count($groups),'vendor_count'=>count($vendors));
    }

    public static function preserve_manual_ds24_inventory($value,$old_value,$option='') {
        if (!is_array($value) || !is_array($old_value)) { return $value; }
        $inventory = get_option(self::DS24_INVENTORY_OPTION,array());
        if (!is_array($inventory) || empty($inventory['rows']) || !is_array($inventory['rows'])) { return $value; }
        $inventory_fp = strtolower(trim((string)($inventory['key_fingerprint'] ?? '')));
        $inventory_affiliate = trim((string)($inventory['affiliate_id'] ?? ''));
        $incoming_fp = strtolower(trim((string)($value['key_fingerprint'] ?? '')));
        $incoming_affiliate = trim((string)($value['affiliate_id'] ?? ''));
        if ($inventory_fp === '' || $inventory_affiliate === '' || $incoming_fp === '' || $incoming_affiliate === '') { return $value; }
        if (!hash_equals($inventory_fp,$incoming_fp) || !hash_equals($inventory_affiliate,$incoming_affiliate)) { return $value; }
        $allowed = array();
        foreach ($inventory['rows'] as $row) {
            if (!is_array($row)) { continue; }
            $entry_id = preg_replace('/[^0-9]/','',(string)($row['entry_id'] ?? ''));
            if ($entry_id !== '') { $allowed[$entry_id] = true; }
        }
        if (!$allowed) { return $value; }
        $incoming = array();
        foreach ((array)($value['items'] ?? array()) as $item) { if (is_array($item) && !empty($item['id'])) { $incoming[(string)$item['id']] = $item; } }
        foreach ((array)($old_value['items'] ?? array()) as $item) {
            if (!is_array($item) || empty($item['id'])) { continue; }
            $entry_id = (string)$item['id'];
            if ((string)($item['source_kind'] ?? '') !== 'digistore24_manual_csv' || !isset($allowed[$entry_id]) || isset($incoming[$entry_id])) { continue; }
            $incoming[$entry_id] = $item;
        }
        if ($incoming) { ksort($incoming,SORT_STRING); $value['items'] = array_values($incoming); }
        return $value;
    }

    private static function delegate_idealo($file) {
        if (!class_exists('Pferdeportal_Affiliate_Router')) { self::import_redirect('failed','Affiliate-Router ist nicht geladen.'); }
        $_FILES['idealo_feed'] = $file;
        $_POST['ppar_idealo_nonce'] = wp_create_nonce('ppar_idealo_import_file');
        $_REQUEST['ppar_idealo_nonce'] = $_POST['ppar_idealo_nonce'];
        Pferdeportal_Affiliate_Router::instance()->handle_idealo_import_file();
        exit;
    }

    private static function delegate_creatives($file,$provider,$name) {
        if (!class_exists('Pferdeportal_Affiliate_Router')) { self::import_redirect('failed','Affiliate-Router ist nicht geladen.'); }
        $hash = is_readable((string)$file['tmp_name']) ? hash_file('sha256',(string)$file['tmp_name']) : '';
        $_FILES['creative_file'] = $file;
        $_POST['provider'] = sanitize_key($provider);
        $_POST['partner_external_id'] = 'manual-'.substr((string)$hash,0,20);
        $_POST['partner_name'] = ucfirst($provider).' · Dateiimport '.sanitize_file_name($name);
        $_POST['creative_codes'] = '';
        $_POST['ppar_creative_library_nonce'] = wp_create_nonce('ppar_creative_library_import');
        $_REQUEST['ppar_creative_library_nonce'] = $_POST['ppar_creative_library_nonce'];
        Pferdeportal_Affiliate_Router::instance()->handle_creative_library_import();
        exit;
    }

    private static function remember_import($provider,$message,$sha) {
        update_option(self::IMPORT_LAST_OPTION,array('provider'=>sanitize_text_field($provider),'message'=>sanitize_text_field($message),'sha256'=>preg_replace('/[^a-f0-9]/','',strtolower($sha)),'imported_at'=>time()),false);
    }

    private static function import_redirect($status,$message) {
        wp_safe_redirect(add_query_arg(array('page'=>'affiliate-portal-kiss-providers','ppar_universal_import'=>sanitize_key($status),'ppar_universal_message'=>rawurlencode(sanitize_text_field($message))),admin_url('admin.php')));
        exit;
    }
}
