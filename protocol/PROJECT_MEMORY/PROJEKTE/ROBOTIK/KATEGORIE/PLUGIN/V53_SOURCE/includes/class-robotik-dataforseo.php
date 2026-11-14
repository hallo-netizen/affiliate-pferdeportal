<?php
if (!defined('ABSPATH')) { exit; }
/** DataForSEO gateway for the existing Robotik category plugin. No writes to site content. */
final class Robotik_DataForSEO {
    private const PAGE = 'robotik-dataforseo';
    private const OPT_LOGIN = 'robotik_dataforseo_login_v1';
    private const OPT_PASSWORD = 'robotik_dataforseo_password_v1';
    private const OPT_NOTICE = 'robotik_dataforseo_notice_v1';
    private const OPT_PREFLIGHT = 'robotik_dataforseo_preflight_v1';
    private const OPT_REPORT = 'robotik_dataforseo_report_v1';
    private const OPT_CONNECTION = 'robotik_dataforseo_connection_v1';
    private const LOCK = 'robotik_dataforseo_request_lock_v1';
    private const URL = 'https://api.dataforseo.com/v3/';
    public const FREE_ENDPOINT = 'appendix/user_data';
    public const OVERVIEW_ENDPOINT = 'dataforseo_labs/google/keyword_overview/live';
    public const IDEAS_ENDPOINT = 'dataforseo_labs/google/keyword_ideas/live';
    public const SUGGESTIONS_ENDPOINT = 'dataforseo_labs/google/keyword_suggestions/live';

    public static function boot(): void {
        add_action('admin_menu',[self::class,'menu'],35);
        add_action('admin_post_robotik_dfs_credentials',[self::class,'save_credentials']);
        add_action('admin_post_robotik_dfs_connection',[self::class,'test_connection']);
        add_action('admin_post_robotik_dfs_preflight',[self::class,'post_preflight']);
        add_action('admin_post_robotik_dfs_preflight_export',[self::class,'export_preflight']);
        add_action('admin_post_robotik_dfs_paid',[self::class,'post_paid']);
        add_action('admin_post_robotik_dfs_export',[self::class,'export']);
    }
    public static function menu():void {
        add_submenu_page('robotik-kategorie','Robotik DataForSEO','DataForSEO','manage_options',self::PAGE,[self::class,'screen']);
    }
    private static function authorize(string $nonce):void {
        if (!current_user_can('manage_options')) wp_die('Administratorrechte erforderlich.');
        check_admin_referer($nonce);
    }
    private static function credentials():array {
        $login=defined('ROBOTIK_DFS_LOGIN')?(string)ROBOTIK_DFS_LOGIN:(string)get_option(self::OPT_LOGIN,'');
        $password=defined('ROBOTIK_DFS_PASSWORD')?(string)ROBOTIK_DFS_PASSWORD:(string)get_option(self::OPT_PASSWORD,'');
        return [trim($login),trim($password)];
    }
    public static function has_credentials():bool {
        [$a,$b]=self::credentials();return $a!==''&&$b!=='';
    }
    private static function go():void {wp_safe_redirect(admin_url('admin.php?page='.self::PAGE));exit;}
    private static function notify(bool $pass,string $message):void {
        update_option(self::OPT_NOTICE,['pass'=>$pass,'text'=>$message,'utc'=>gmdate('c')],false);
    }
    public static function save_credentials():void {
        self::authorize('robotik_dfs_credentials');
        if(!defined('ROBOTIK_DFS_LOGIN')) {
            $login=isset($_POST['dfs_login'])&&is_string($_POST['dfs_login'])?trim(sanitize_text_field(wp_unslash($_POST['dfs_login']))):'';
            if($login!=='')update_option(self::OPT_LOGIN,$login,false);
        }
        if(!defined('ROBOTIK_DFS_PASSWORD')) {
            $password=isset($_POST['dfs_password'])&&is_string($_POST['dfs_password'])?trim(wp_unslash($_POST['dfs_password'])):'';
            if($password!=='')update_option(self::OPT_PASSWORD,$password,false);
        }
        self::free_check('Zugang gespeichert. '); self::go();
    }
    /** Single transport; no API activity except from explicit admin actions. */
    public static function request(string $endpoint,?array $task=null):array {
        if(!in_array($endpoint,[self::FREE_ENDPOINT,self::OVERVIEW_ENDPOINT,self::IDEAS_ENDPOINT,self::SUGGESTIONS_ENDPOINT],true))throw new RuntimeException('API-Endpunkt nicht freigegeben.');
        [$login,$password]=self::credentials();if($login===''||$password==='')throw new RuntimeException('DataForSEO-Zugangsdaten fehlen.');
        $headers=['Authorization'=>'Basic '.base64_encode($login.':'.$password),'Accept'=>'application/json'];
        $args=['timeout'=>55,'redirection'=>0,'sslverify'=>true,'headers'=>$headers];
        if($task!==null){
            if($endpoint===self::FREE_ENDPOINT)throw new RuntimeException('Kostenfreier Endpunkt darf keine POST-Daten erhalten.');
            $args['headers']['Content-Type']='application/json; charset=utf-8';
            $args['body']=wp_json_encode([$task],JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);
            $res=wp_remote_post(self::URL.$endpoint,$args);
        }else{
            if($endpoint!==self::FREE_ENDPOINT)throw new RuntimeException('Kostenpflichtige Abfrage ohne Auftragsdaten gesperrt.');
            $res=wp_remote_get(self::URL.$endpoint,$args);
        }
        if(is_wp_error($res))throw new RuntimeException('DataForSEO nicht erreichbar: '.$res->get_error_message());
        $status=(int)wp_remote_retrieve_response_code($res);
        $data=json_decode((string)wp_remote_retrieve_body($res),true);
        if($status!==200||!is_array($data))throw new RuntimeException('DataForSEO: HTTP '.$status.' oder ungültige Antwort.');
        if((int)($data['status_code']??0)!==20000)throw new RuntimeException('DataForSEO: '.(string)($data['status_message']??'unbekannter API-Fehler'));
        if($task!==null){
            $first=$data['tasks'][0]??null;
            if(!is_array($first)||(int)($first['status_code']??0)!==20000)throw new RuntimeException('DataForSEO-Abfrage: '.(string)($first['status_message']??'Task-Fehler'));
        }
        return $data;
    }
    private static function free_check(string $prefix=''):void {
        try{
            $r=self::request(self::FREE_ENDPOINT);
            if(abs((float)($r['cost']??0))>0.00000001)throw new RuntimeException('Unerwartete Kosten beim kostenlosen Verbindungstest.');
            $p=self::build_preflight();
            update_option(self::OPT_PREFLIGHT,$p,false);
            update_option(self::OPT_CONNECTION,['pass'=>true,'utc'=>gmdate('c')],false);
            self::notify(true,$prefix.'DataForSEO-Verbindung PASS (0 USD). '.(int)$p['unique_keywords'].' SEO-Begriffe kostenfrei vorbereitet; '.count($p['rejected']).' zu lange Begriffe.');
        }catch(Throwable $e){
            update_option(self::OPT_CONNECTION,['pass'=>false,'utc'=>gmdate('c')],false);
            self::notify(false,$prefix.$e->getMessage());
        }
    }
    public static function test_connection():void {
        self::authorize('robotik_dfs_connection');
        self::free_check();self::go();
    }
    private static function normal(string $x):string {
        $x=trim(preg_replace('/\s+/u',' ',$x));return function_exists('mb_strtolower')?mb_strtolower($x,'UTF-8'):strtolower($x);
    }
    /** V52 SEO candidate pool: independent from the UNCHANGED legacy WP first-import plan. */
    private static function seo_manifest():array {
        $file=dirname(__DIR__).'/assets/robotik-v52-seo-candidates.json';
        if(!is_readable($file))throw new RuntimeException('V52-SEO-Fachentwurf fehlt. Keine alte Keywordliste als Ersatz.');
        $data=json_decode((string)file_get_contents($file),true);
        if(!is_array($data)||($data['schema']??'')!=='robotik-seo-candidates-v52-v1'
            ||($data['status']??'')!=='SEO_RECHERCHE_NUR_KEIN_WP_IMPORT_KEINE_SEO_FREIGABE'
            ||count((array)($data['records']??[]))!==437
            ||(int)($data['counts']['product_pages']??0)!==141
            ||(int)($data['counts']['facets']??0)!==296
            ||(int)($data['counts']['review_holds']??0)!==16)
            throw new RuntimeException('V52-SEO-Fachentwurf fehlerhaft oder unvollständig.');
        return $data;
    }
    public static function build_preflight():array {
        $manifest=self::seo_manifest();
        $keywords=[];$rejected=[];$count=['product_pages'=>0,'facets'=>0];
        $seen=[];$holdcount=0;
        foreach($manifest['records'] as $record){
            if(!is_array($record))throw new RuntimeException('Ungültiger V52-SEO-Datensatz.');
            $owner=(string)($record['id']??'');$kind=(string)($record['type']??'');
            $raw=(string)($record['keyword']??'');
            if($owner===''||isset($seen[$owner])||!in_array($kind,['product','category'],true))
                throw new RuntimeException('Mehrfache oder ungültige V52-SEO-ID.');
            $seen[$owner]=true;
            if($kind==='product'){
                $count['product_pages']++;
                if(!empty($record['review_hold']))$holdcount++;
            }else $count['facets']++;
            $k=self::normal($raw);
            if($k===''||strlen($k)>80||count(preg_split('/\s+/u',$k))>10){
                $rejected[]=['owner'=>$owner,'keyword'=>$raw,'reason'=>'DataForSEO-Limit: 80 Zeichen oder 10 Wörter'];
                continue;
            }
            if(!isset($keywords[$k]))$keywords[$k]=['keyword'=>$k,'owners'=>[]];
            $keywords[$k]['owners'][]=['id'=>$owner,'type'=>$kind,'label'=>$raw,
                'world'=>(string)($record['world']??''),'review_hold'=>!empty($record['review_hold']),
                'source'=>(string)($record['source']??'')];
        }
        if($count['product_pages']!==141||$count['facets']!==296||$holdcount!==16)
            throw new RuntimeException('V52-Mengenprüfung gescheitert. Kein Rückfall zum alten Profil.');
        $keywords=array_values($keywords);
        $fp=hash('sha256',wp_json_encode([$keywords,$rejected,$count,$manifest['source_sha256']],JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES));
        return ['schema'=>'robotik-dfs-preflight-v1','version'=>'0.4.3','source'=>'V52_SEO_CANDIDATES_NICHT_IMPORT',
            'source_sha256'=>$manifest['source_sha256'],'review_holds'=>$holdcount,
            'location_name'=>'Germany','language_code'=>'de','count'=>$count,
            'unique_keywords'=>count($keywords),'keywords'=>$keywords,'rejected'=>$rejected,
            'fingerprint'=>$fp,'generated_at_utc'=>gmdate('c')];
    }
    public static function post_preflight():void {
        self::authorize('robotik_dfs_preflight');
        try{
            $p=self::build_preflight();
            update_option(self::OPT_PREFLIGHT,$p,false);
            self::notify(true,$p['unique_keywords'].' eindeutige Begriffe aus dem vorhandenen Kategoriebaum geprüft. 0 API-Aufrufe, 0 Kosten. '.count($p['rejected']).' zu lange Begriffe.');
        }catch(Throwable $e){self::notify(false,$e->getMessage());}
        self::go();
    }
    public static function export_preflight():void {
        self::authorize('robotik_dfs_preflight_export');
        try{$preflight=self::build_preflight();}
        catch(Throwable $e){wp_die('Keyword-Export blockiert: '.$e->getMessage());}
        nocache_headers();
        header('Content-Type: application/json; charset=UTF-8');
        header('Content-Disposition: attachment; filename="robotik-v52-seo-vorabcheck-kostenlos.json"');
        echo wp_json_encode($preflight,JSON_PRETTY_PRINT|JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);
        exit;
    }
    private static function choose_task(array $p,string $type,string $scope):array {
        $k=array_column($p['keywords'],'keyword');
        if($type==='overview'){
            if($scope==='test')$k=array_slice($k,0,10);
            if(!$k||count($k)>700)throw new RuntimeException('Keyword Overview benötigt 1 bis 700 Begriffe.');
            return [self::OVERVIEW_ENDPOINT,['keywords'=>$k,'location_name'=>'Germany','language_code'=>'de','include_serp_info'=>false,'include_clickstream_data'=>false],$k];
        }
        $products=[];foreach($p['keywords'] as $item){foreach($item['owners'] as $owner){if($owner['type']==='product'){$products[]=$item['keyword'];break;}}}
        if(!$products)throw new RuntimeException('Keine Produkte für Keyword-Ideen vorhanden.');
        if($type==='ideas'){
            $seed=array_slice($products,0,$scope==='test'?3:10);
            return [self::IDEAS_ENDPOINT,['keywords'=>$seed,'location_name'=>'Germany','language_code'=>'de','limit'=>25,'include_serp_info'=>false],$seed];
        }
        if($type==='suggestions'){
            $seed=$products[0];
            return [self::SUGGESTIONS_ENDPOINT,['keyword'=>$seed,'location_name'=>'Germany','language_code'=>'de','limit'=>25,'include_seed_keyword'=>true,'include_serp_info'=>false],[$seed]];
        }
        throw new RuntimeException('Unbekannte DataForSEO-Abfrage.');
    }
    /** Priceable API tasks require per-request manual confirmation. There is no cron, silent retry or auto-loop. */
    public static function post_paid():void {
        self::authorize('robotik_dfs_paid');
        if(empty($_POST['robotik_dfs_paid_confirm']))wp_die('Kostenpflichtige Abfrage nicht freigegeben.');
        $type=isset($_POST['dfs_type'])?sanitize_key(wp_unslash((string)$_POST['dfs_type'])):'';
        $scope=isset($_POST['dfs_scope'])?sanitize_key(wp_unslash((string)$_POST['dfs_scope'])):'';
        if(!in_array($scope,['test','all'],true))wp_die('Ungültiger Umfang.');
        $prev=get_option(self::OPT_PREFLIGHT,[]);
        if(!is_array($prev)||empty($prev['fingerprint']))wp_die('Zuerst den kostenlosen Prüfplan erstellen.');
        try{
            $conn=get_option(self::OPT_CONNECTION,[]);
            if(!is_array($conn)||empty($conn['pass']))throw new RuntimeException('Zuerst Zugang kostenlos testen.');
            $now=self::build_preflight();
            if(!hash_equals((string)$prev['fingerprint'],$now['fingerprint']))throw new RuntimeException('Kategorieplan verändert. Erst kostenlosen Prüfplan aktualisieren.');
            [$endpoint,$task,$terms]=self::choose_task($now,$type,$scope);
            $request_id=hash('sha256',wp_json_encode([$endpoint,$task],JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES));
            $old=get_option(self::OPT_REPORT,[]);
            if(is_array($old)&&($old['request_id']??'')===$request_id)throw new RuntimeException('Dieser exakte Auftrag wurde bereits ausgeführt. Keine doppelten Kosten.');
            // add_option is an atomic insert: two admin clicks cannot both start the same paid call.
            $locked=get_option(self::LOCK,null);
            if(is_array($locked)&&time()-(int)($locked['at']??0)>180){delete_option(self::LOCK);}
            if(!add_option(self::LOCK,['at'=>time(),'request_id'=>$request_id],'',false))
                throw new RuntimeException('Eine DataForSEO-Abfrage läuft bereits. Keine zweite Berechnung.');
            try{
                $data=self::request($endpoint,$task);
                $out=[];$result=(array)($data['tasks'][0]['result']??[]);
                $owner_index=[];foreach($now['keywords'] as $record)$owner_index[$record['keyword']]=$record['owners'];
                foreach($result as $group){if(!is_array($group))continue;foreach((array)($group['items']??[]) as $item){
                    if(!is_array($item))continue;
                    $info=is_array($item['keyword_info']??null)?$item['keyword_info']:[];
                    $intent=is_array($item['search_intent_info']??null)?$item['search_intent_info']:[];
                    $result_keyword=self::normal((string)($item['keyword']??''));
                    $out[]=['keyword'=>(string)($item['keyword']??''),'linked_owners'=>$owner_index[$result_keyword]??[],
                        'search_volume'=>$info['search_volume']??null,
                        'competition'=>$info['competition_level']??null,'cpc'=>$info['cpc']??null,
                        'intent'=>$intent['main_intent']??null,'updated_at'=>$info['last_updated_time']??null];
                }}
                $report=['schema'=>'robotik-dfs-report-v1','request_id'=>$request_id,'source_plan'=>$now['fingerprint'],
                    'mode'=>$type,'scope'=>$scope,'seeds'=>$terms,'location'=>'Germany','language'=>'de',
                    'cost_usd'=>(float)($data['tasks'][0]['cost']??$data['cost']??0),'reported_rows'=>count($out),
                    'provider_task_id'=>$data['tasks'][0]['id']??'','utc'=>gmdate('c'),'rows'=>$out,
                    'notes'=>'Anbieterergebnis, kein automatischer Kategorienentscheid. Exakte Eigentümer stehen in linked_owners; freie Ideen besitzen noch keine Kategoriebindung. Fehlende Werte bedeuten nicht kein Suchvolumen.'];
                update_option(self::OPT_REPORT,$report,false);
                self::notify(true,'DataForSEO: '.count($out).' Ergebniszeilen. Anbieter-Kosten: '.number_format($report['cost_usd'],4,'.','').' USD. Keine WordPress-Inhalte verändert.');
            }finally{delete_option(self::LOCK);}
        }catch(Throwable $e){self::notify(false,$e->getMessage());}
        self::go();
    }
    public static function export():void {
        self::authorize('robotik_dfs_export');$report=get_option(self::OPT_REPORT,[]);
        if(!is_array($report)||empty($report['request_id']))wp_die('Noch kein kostenpflichtiger Keywordbericht vorhanden.');
        nocache_headers();header('Content-Type: application/json; charset=UTF-8');
        header('Content-Disposition: attachment; filename="robotik-dataforseo-ergebnis.json"');
        echo wp_json_encode($report,JSON_PRETTY_PRINT|JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);exit;
    }
    public static function screen():void {
        if(!current_user_can('manage_options'))wp_die('Administratorrechte erforderlich.');
        $notice=get_option(self::OPT_NOTICE,[]);$pre=get_option(self::OPT_PREFLIGHT,[]);$report=get_option(self::OPT_REPORT,[]);
        echo '<div class="wrap"><h1>Robotik – DataForSEO</h1>';
        echo '<p>Einmalige Verbindung und gesammelte Keywordprüfung für den vorhandenen Robotik-Baum. <strong>Keine automatischen Kosten, keine Seitenänderungen.</strong></p>';
        if(is_array($notice)&&!empty($notice['text']))echo '<div class="notice '.(!empty($notice['pass'])?'notice-success':'notice-error').'"><p>'.esc_html($notice['text']).'</p></div>';
        echo '<h2>1. Zugang und kostenloser Verbindungstest</h2>';
        echo '<p>Status: <strong>'.(self::has_credentials()?'Zugang vorhanden':'Zugang fehlt').'</strong> · Markt: Deutschland · Sprache: Deutsch.</p>';
        echo '<form method="post" action="'.esc_url(admin_url('admin-post.php')).'">';wp_nonce_field('robotik_dfs_credentials');
        echo '<input type="hidden" name="action" value="robotik_dfs_credentials">';
        echo '<p><label>API-Login <input type="text" name="dfs_login" autocomplete="username" style="min-width:240px"'.(defined('ROBOTIK_DFS_LOGIN')?' disabled':'').'></label> ';
        echo '<label>API-Passwort <input type="password" name="dfs_password" autocomplete="new-password" style="min-width:240px"'.(defined('ROBOTIK_DFS_PASSWORD')?' disabled':'').'></label> ';
        submit_button('Zugang speichern + kostenlos prüfen','secondary','submit',false);echo '</p></form>';
        echo '<form method="post" action="'.esc_url(admin_url('admin-post.php')).'">';wp_nonce_field('robotik_dfs_connection');
        echo '<input type="hidden" name="action" value="robotik_dfs_connection">';submit_button('Verbindung kostenlos prüfen','secondary','submit',false);echo '</form>';
        echo '<h2>2. Kostenloser SEO-Sammelprüfplan</h2><p>Der aktuelle V52-Fachentwurf umfasst 141 mögliche Robotertyp-Seiten und 296 Rubriken. 16 fachlich offene Fälle werden für die Keywordprüfung mitgeführt. <strong>Keine WordPress-Übernahme; alter 104er-Import bleibt unverändert.</strong></p>';
        echo '<form method="post" action="'.esc_url(admin_url('admin-post.php')).'">';wp_nonce_field('robotik_dfs_preflight');
        echo '<input type="hidden" name="action" value="robotik_dfs_preflight">';submit_button('Gesamte Keywordliste prüfen (kostenlos)','secondary','submit',false);echo '</form>';
        echo '<form method="post" action="'.esc_url(admin_url('admin-post.php')).'">';
        wp_nonce_field('robotik_dfs_preflight_export');
        echo '<input type="hidden" name="action" value="robotik_dfs_preflight_export">';
        submit_button('SEO-Keywordliste als JSON herunterladen (kostenlos)','secondary','submit',false);
        echo '</form>';
        if(is_array($pre)&&!empty($pre['fingerprint']))echo '<p><strong>Letzte Vorbereitung:</strong> '.(int)$pre['unique_keywords'].' eindeutige Keywords · '.count((array)($pre['rejected']??[])).' ausgelassen · 0 USD.</p>';
        echo '<h2>3. Bezahlte Recherche nur mit ausdrücklicher Freigabe</h2><p>Der Anbieter berechnet nach seiner gültigen Preisliste. <strong>Keine Abfrage ohne Bestätigung und Klick.</strong> Eine identische Abfrage wird nicht automatisch wiederholt.</p>';
        echo '<p><a href="https://dataforseo.com/pricing" target="_blank" rel="noopener noreferrer">Aktuelle Anbieterpreise prüfen</a></p>';
        echo '<form method="post" action="'.esc_url(admin_url('admin-post.php')).'">';wp_nonce_field('robotik_dfs_paid');
        echo '<input type="hidden" name="action" value="robotik_dfs_paid">';
        echo '<p><label>Abfrage <select name="dfs_type"><option value="overview">Suchvolumen und Suchabsicht (Keyword Overview)</option><option value="ideas">Weitere Suchbegriffe (Keyword Ideas)</option><option value="suggestions">Vertiefte Keyword-Vorschläge (Keyword Suggestions)</option></select></label> ';
        echo '<label>Umfang <select name="dfs_scope"><option value="test">Kleine Testmenge</option><option value="all">Erweiterter Umfang (Overview alle; Ideen bis 10 Produkte)</option></select></label></p>';
        echo '<p><small>Keyword Suggestions nutzt bewusst nur eine Roboterart pro Aufruf, damit keine kostenpflichtigen Serienstarts entstehen.</small></p>';
        echo '<p><label><input type="checkbox" name="robotik_dfs_paid_confirm" value="1" required> Ich gebe diesen <strong>kostenpflichtigen API-Aufruf</strong> ausdrücklich frei.</label></p>';
        submit_button('Kostenpflichtige Recherche einmal ausführen','primary','submit',false);echo '</form>';
        if(is_array($report)&&!empty($report['request_id'])){
            echo '<h2>4. Letztes Ergebnis</h2><p>Modus: '.esc_html((string)$report['mode']).' · '.(int)$report['reported_rows'].' Ergebnisse · tatsächlich gemeldete API-Kosten: '.esc_html(number_format((float)$report['cost_usd'],4,'.','')).' USD</p>';
            echo '<form method="post" action="'.esc_url(admin_url('admin-post.php')).'">';wp_nonce_field('robotik_dfs_export');
            echo '<input type="hidden" name="action" value="robotik_dfs_export">';submit_button('Gesamter SEO-Bericht als JSON','secondary','submit',false);echo '</form>';
            echo '<table class="widefat striped"><thead><tr><th>Suchbegriff</th><th>Monatliche Suche</th><th>Absicht</th><th>Wettbewerb</th></tr></thead><tbody>';
            foreach(array_slice((array)$report['rows'],0,25) as $row){echo '<tr><td>'.esc_html((string)$row['keyword']).'</td><td>'.esc_html($row['search_volume']===null?'nicht vorhanden':(string)$row['search_volume']).'</td><td>'.esc_html((string)($row['intent']??'nicht vorhanden')).'</td><td>'.esc_html((string)($row['competition']??'nicht vorhanden')).'</td></tr>';}
            echo '</tbody></table><p>Die komplette Ergebnisliste steht im JSON-Bericht; hier werden höchstens 25 Zeilen angezeigt.</p>';
        }
        echo '</div>';
    }
}