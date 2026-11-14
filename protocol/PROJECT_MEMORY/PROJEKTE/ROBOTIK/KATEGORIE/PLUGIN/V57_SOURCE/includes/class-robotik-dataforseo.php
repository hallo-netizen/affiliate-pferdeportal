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
    private const OPT_FULL_RUN = 'robotik_dfs_full_run_v1';
    private const OPT_FULL_REPORT = 'robotik_dfs_full_report_v1';
    private const OPT_FULL_LOCK = 'robotik_dfs_full_step_lock_v1';
    private const URL = 'https://api.dataforseo.com/v3/';
    public const FREE_ENDPOINT = 'appendix/user_data';
    public const OVERVIEW_ENDPOINT = 'dataforseo_labs/google/keyword_overview/live';
    public const IDEAS_ENDPOINT = 'dataforseo_labs/google/keyword_ideas/live';
    public const SUGGESTIONS_ENDPOINT = 'dataforseo_labs/google/keyword_suggestions/live';
    public const SERP_ENDPOINT = 'serp/google/organic/live/advanced';

    public static function boot(): void {
        add_action('admin_menu',[self::class,'menu'],35);
        add_action('admin_post_robotik_dfs_credentials',[self::class,'save_credentials']);
        add_action('admin_post_robotik_dfs_connection',[self::class,'test_connection']);
        add_action('admin_post_robotik_dfs_preflight',[self::class,'post_preflight']);
        add_action('admin_post_robotik_dfs_preflight_export',[self::class,'export_preflight']);
        add_action('admin_post_robotik_dfs_paid',[self::class,'post_paid']);
        add_action('admin_post_robotik_dfs_export',[self::class,'export']);
        add_action('admin_post_robotik_dfs_full_start',[self::class,'full_start']);
        add_action('wp_ajax_robotik_dfs_full_step',[self::class,'full_step']);
        add_action('admin_post_robotik_dfs_full_export',[self::class,'full_export']);
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
        if(!in_array($endpoint,[self::FREE_ENDPOINT,self::OVERVIEW_ENDPOINT,self::IDEAS_ENDPOINT,self::SUGGESTIONS_ENDPOINT,self::SERP_ENDPOINT],true))throw new RuntimeException('API-Endpunkt nicht freigegeben.');
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
        return ['schema'=>'robotik-dfs-preflight-v1','version'=>'0.4.4','source'=>'V52_SEO_CANDIDATES_NICHT_IMPORT',
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
    /** Die EINZIGE neue bezahlte Gesamtrecherche: 1 manuelle Freigabe, 1 Report, keine Writer. */
    private static function full_pairs():array {
        // Original-V52-HOLD-ID -> fachlich begruendeter Wettbewerbs-Owner ODER Zusatzsuchbegriff.
        // Gilt nur fuer SEO-Vergleich, nicht als importierte WordPress-Entscheidung.
        return [
            'v46_h03'=>['v46_p01',null,'Pflege-Telepraesenz'],
            'v46_h06'=>['hu_hu01',null,'Haushaltshumanoid'],
            'v46_h07'=>['rbt_product_0500',null,'Saugroboter'],
            'v46_h10'=>['rbt_product_0488',null,'Gewerbe-Servierroboter'],
            'v46_h12'=>['hu_hu14',null,'Humanoider Begleiter'],
            'v46_ga04'=>[null,'elektrische grillbürste','Elektrische Grillbuerste'],
            'v46_f01'=>['rbt_product_0048',null,'Bootsreiniger'],
            'v46_f02'=>['rbt_product_0479',null,'Gewerbe-Kameraroboter'],
            'v46_f03'=>['rbt_product_0536',null,'Lerndrohnen'],
            'v46_s03'=>[null,'badminton ballmaschine','Badminton-Ballmaschine'],
            'v46_s07'=>['rbt_product_0479',null,'Gewerbe-Kameraroboter'],
            'v46_b01'=>['rbt_product_0059',null,'Lernroboter'],
            'v46_b02'=>['rbt_product_0059',null,'Lernroboter'],
            'v46_b04'=>['rbt_product_0503',null,'Tischroboterarme'],
            'v46_b05'=>['rbt_product_0059',null,'Lernroboter'],
            'v46_b07'=>[null,'laborautomatisierung chemie','Laborautomatisierung'],
        ];
    }
    public static function full_plan(array $pre):array {
        if(count($pre['keywords']??[])!==437||($pre['count']['product_pages']??0)!==141
            ||($pre['count']['facets']??0)!==296||($pre['review_holds']??0)!==16) {
            throw new RuntimeException('Kein vollstaendiger V52-SEO-Plan: Gesamtlauf blockiert.');
        }
        $manifest=self::seo_manifest();
        $records=[];$worlds=[];$product_count=[];$hold=[];
        foreach($manifest['world_order'] as $w){$worlds[(string)$w]=[];$product_count[(string)$w]=0;}
        foreach($manifest['records'] as $rec){
            $records[(string)$rec['id']]=$rec;
            if($rec['type']==='product'){
                $world=(string)$rec['world'];
                if(!isset($worlds[$world]))throw new RuntimeException('Unbekannter Fachbereich: '.$world);
                $worlds[$world][]=self::normal((string)$rec['keyword']);$product_count[$world]++;
                if(!empty($rec['review_hold']))$hold[(string)$rec['id']]=$rec;
            }
        }
        if(count($worlds)!==8||count($hold)!==16)throw new RuntimeException('Acht Welten oder 16 fachliche HOLDs fehlen.');
        $pairs=self::full_pairs();
        if(count($pairs)!==16||array_diff(array_keys($hold),array_keys($pairs))||array_diff(array_keys($pairs),array_keys($hold)))
            throw new RuntimeException('HOLD-Vergleichsplan ist unvollstaendig.');
        $tasks=[];
        $tasks[]=['type'=>'overview','world'=>'alle','endpoint'=>self::OVERVIEW_ENDPOINT,
            'task'=>['keywords'=>array_column($pre['keywords'],'keyword'),'location_name'=>'Germany','language_code'=>'de','include_serp_info'=>false,'include_clickstream_data'=>false],
            'max_charge'=>0.10];
        foreach($worlds as $world=>$seeds){
            if(!$seeds||count($seeds)>200)throw new RuntimeException('Keyword-Ideen: zu viele oder keine Saatbegriffe.');
            $tasks[]=['type'=>'ideas','world'=>$world,'endpoint'=>self::IDEAS_ENDPOINT,
                'task'=>['keywords'=>array_values(array_unique($seeds)),'location_name'=>'Germany','language_code'=>'de',
                    'limit'=>300,'include_serp_info'=>false,'include_clickstream_data'=>false],
                'max_charge'=>0.065];
        }
        $serp=[];$pair_data=[];
        foreach($pairs as $hold_id=>[$rival_id,$rival_query,$rival_label]){
            $target=self::normal((string)$records[$hold_id]['keyword']);
            if($target==='')throw new RuntimeException('HOLD-Suchbegriff fehlt: '.$hold_id);
            $competitor=$rival_id!==null?($records[$rival_id]['keyword']??null):$rival_query;
            if(!is_string($competitor)||trim($competitor)==='')throw new RuntimeException('Gegenbegriff fehlt: '.$hold_id);
            $competitor=self::normal($competitor);
            $serp[$target]=$target;$serp[$competitor]=$competitor;
            $pair_data[]=['hold_id'=>$hold_id,'world'=>(string)$records[$hold_id]['world'],
                'target'=>$target,'competitor'=>$competitor,'competitor_owner'=>$rival_id,
                'competitor_label'=>$rival_label];
        }
        foreach($serp as $keyword){
            $tasks[]=['type'=>'serp','world'=>'HOLD-Vergleich','endpoint'=>self::SERP_ENDPOINT,
                'task'=>['keyword'=>$keyword,'location_name'=>'Germany','language_code'=>'de','depth'=>10,
                    'device'=>'desktop','load_async_ai_overview'=>false,'calculate_rectangles'=>false,
                    'resolve_goto_urls'=>false],'max_charge'=>0.005];
        }
        return ['tasks'=>$tasks,'pairs'=>$pair_data,'world_product_counts'=>$product_count,
            'reservation_usd'=>array_sum(array_column($tasks,'max_charge')),
            'serp_keywords'=>count($serp)];
    }
    /** Manuell einmal gestartet, nur bereits angelegte WP-Optionen; keine neue Tabelle oder Cron. */
    public static function full_start():void {
        self::authorize('robotik_dfs_full_start');
        if(empty($_POST['robotik_dfs_full_confirm']))wp_die('Kostenfreigabe fehlt.');
        try{
            $existing=get_option(self::OPT_FULL_RUN,[]);
            if(is_array($existing)&&!empty($existing['id']))throw new RuntimeException('Gesamtrecherche bereits begonnen. Kein automatischer Zweitlauf und keine weiteren Kosten.');
            $raw=isset($_POST['robotik_dfs_budget_usd'])?wp_unslash((string)$_POST['robotik_dfs_budget_usd']):'';
            if(!preg_match('/^\d{1,2}(?:[\.,]\d{1,2})?$/',$raw))throw new RuntimeException('Kostenlimit als USD-Betrag eingeben.');
            $budget=(float)str_replace(',','.',$raw);
            if($budget<0.01||$budget>20)throw new RuntimeException('Kostenlimit muss zwischen 0,01 und 20,00 USD liegen.');
            if(!self::has_credentials())throw new RuntimeException('DataForSEO-Zugangsdaten fehlen.');
            $pre=self::build_preflight();
            $stored=get_option(self::OPT_PREFLIGHT,[]);
            if(is_array($stored)&&!empty($stored['fingerprint'])&&
                !hash_equals((string)$stored['fingerprint'],(string)$pre['fingerprint']))
                throw new RuntimeException('SEO-Plan wurde geaendert. Vorabcheck erforderlich; keine Kosten.');
            update_option(self::OPT_PREFLIGHT,$pre,false);
            $plan=self::full_plan($pre);
            // Reservations sind bewusst oberhalb der geltenden Anbieterpreise.
            // Jede Anforderung wird vor dem Senden einzeln gegen das genehmigte Budget geprueft.
            if($budget+0.000001<$plan['reservation_usd'])
                throw new RuntimeException('Kostenlimit zu klein. Reservierungsrahmen fuer den Gesamtlauf: '.number_format($plan['reservation_usd'],3,'.','').' USD. Keine Kosten entstanden.');
            $connection=get_option(self::OPT_CONNECTION,[]);
            if(!is_array($connection)||empty($connection['pass'])){
                self::free_check();
                $connection=get_option(self::OPT_CONNECTION,[]);
                if(!is_array($connection)||empty($connection['pass']))throw new RuntimeException('Kostenloser Verbindungstest nicht erfolgreich. Kein Paid-Start.');
            }
            $run=['schema'=>'robotik-dfs-full-run-v1','id'=>hash('sha256',$pre['fingerprint'].'|'.microtime(true).'|'.wp_generate_uuid4()),
                'status'=>'RUNNING','plan_fingerprint'=>$pre['fingerprint'],'source_sha256'=>$pre['source_sha256'],
                'budget_usd'=>$budget,'cost_usd'=>0.0,'index'=>0,'total'=>count($plan['tasks']),
                'tasks'=>$plan['tasks'],'pairs'=>$plan['pairs'],'world_product_counts'=>$plan['world_product_counts'],
                'errors'=>[],'start_utc'=>gmdate('c')];
            if(!add_option(self::OPT_FULL_RUN,$run,'',false))throw new RuntimeException('Ein Lauf ist bereits gespeichert. Kosten blockiert.');
            self::notify(true,'Ein Gesamtauftrag freigegeben: '.count($plan['tasks']).' interne Schritte, '.count($plan['pairs']).' HOLD-Vergleiche. Der Browser fuehrt ihn ohne weitere Klicks aus.');
        }catch(Throwable $e){self::notify(false,$e->getMessage());}
        self::go();
    }
    private static function full_normal_url(string $url):string {
        $parts=parse_url($url);
        if(!is_array($parts)||empty($parts['host']))return '';
        $host=preg_replace('/^www\./','',strtolower((string)$parts['host']));
        $path=rtrim(rawurldecode((string)($parts['path']??'')),'/');
        return $host.$path;
    }
    /** Verarbeitet ausschliesslich die eine soeben erfolgreich beantwortete API-Anfrage. */
    private static function full_parse(array $data,array $task,array &$report):void {
        $groups=(array)($data['tasks'][0]['result']??[]);$type=$task['type'];
        $owner_map=$report['owner_map'];
        if($type==='overview'){
            foreach($groups as $g)foreach((array)($g['items']??[]) as $item){
                if(!is_array($item))continue;
                $word=self::normal((string)($item['keyword']??''));if($word==='')continue;
                $info=(array)($item['keyword_info']??[]);$intent=(array)($item['search_intent_info']??[]);
                $report['keywords'][$word]=['keyword'=>$word,'owners'=>$owner_map[$word]??[],
                    'search_volume'=>$info['search_volume']??null,'intent'=>$intent['main_intent']??null,
                    'competition'=>$info['competition_level']??null,'cpc'=>$info['cpc']??null,
                    'last_updated'=>$info['last_updated_time']??null];
            }
        }elseif($type==='ideas'){
            $world=$task['world'];$items=0;
            foreach($groups as $g)foreach((array)($g['items']??[]) as $item){
                if(!is_array($item))continue;
                $word=self::normal((string)($item['keyword']??''));if($word==='')continue;
                $items++;
                $info=(array)($item['keyword_info']??[]);$intent=(array)($item['search_intent_info']??[]);
                if(!isset($report['ideas'][$word])){
                    $report['ideas'][$word]=['keyword'=>$word,'existing_owners'=>$owner_map[$word]??[],
                        'found_in_worlds'=>[], 'search_volume'=>$info['search_volume']??null,
                        'intent'=>$intent['main_intent']??null,
                        'stage'=>'SUCHIDEE_KEINE_AUTO_KATEGORIE'];
                }
                if(!in_array($world,$report['ideas'][$word]['found_in_worlds'],true))
                    $report['ideas'][$word]['found_in_worlds'][]=$world;
            }
            $report['idea_worlds'][$world]=['returned_rows'=>$items,'limit'=>300,
                'possibly_truncated'=>$items>=300];
        }elseif($type==='serp'){
            $keyword=self::normal((string)$task['task']['keyword']);$urls=[];
            foreach($groups as $g)foreach((array)($g['items']??[]) as $item){
                if(!is_array($item)||($item['type']??'')!=='organic')continue;
                $rank=(int)($item['rank_group']??0);
                if($rank<1||$rank>10)continue;
                $u=self::full_normal_url((string)($item['url']??''));
                if($u!=='')$urls[$u]=['url'=>(string)$item['url'],'rank'=>$rank];
            }
            $report['serps'][$keyword]=array_values($urls);
        }
    }
    private static function full_conclude(array &$report,array $run):void {
        $missing=[];
        foreach($report['owner_map'] as $word=>$owners)if(!array_key_exists($word,$report['keywords']))$missing[]=$word;
        $report['missing_provider_keywords']=$missing;
        $reviews=[];
        foreach($run['pairs'] as $pair){
            $a=$report['serps'][$pair['target']]??[];$b=$report['serps'][$pair['competitor']]??[];
            $first=array_map(fn($r)=>self::full_normal_url($r['url']),$a);
            $second=array_map(fn($r)=>self::full_normal_url($r['url']),$b);
            $shared=array_values(array_intersect($first,$second));
            $status=(!$first||!$second)?'NICHT_PRUEFBAR':(count($shared)>=4?'UEBERSCHNEIDUNG_HOCH':(count($shared)>=2?'UEBERSCHNEIDUNG_MITTEL':'UEBERSCHNEIDUNG_GERING'));
            $reviews[]=$pair+['overlap_count'=>count($shared),'shared_urls'=>$shared,'status'=>$status,
                'decision'=>'FACHLICH_OFFEN_BIS_GESAMTENTSCHEID'];
        }
        $report['hold_reviews']=$reviews;
        $report['summary']=['known_keywords'=>count($report['owner_map']),
            'overview_returned'=>count($report['keywords']),
            'overview_missing'=>count($missing),'idea_distinct'=>count($report['ideas']),
            'new_ideas_unassigned'=>count(array_filter($report['ideas'],static fn($x)=>empty($x['existing_owners']))),
            'idea_worlds_checked'=>count($report['idea_worlds']),
            'serps_returned'=>count($report['serps']),
            'hold_pairs'=>count($reviews),'serp_undecidable'=>count(array_filter($reviews,static fn($x)=>$x['status']==='NICHT_PRUEFBAR'))];
    }
    /** 1 API-Auftrag pro Ajax-Aufruf: persistenter Sperrschritt VOR Bezahl-Anfrage, NIEMALS automatischer Wiederholungsversuch. */
    public static function full_step():void {
        if(!current_user_can('manage_options'))wp_send_json_error(['error'=>'Keine Adminrechte.']);
        check_ajax_referer('robotik_dfs_full_step');
        $run=get_option(self::OPT_FULL_RUN,[]);
        if(!is_array($run)||empty($run['id']))wp_send_json_error(['error'=>'Kein Gesamtauftrag vorhanden.']);
        if(($run['status']??'')!=='RUNNING')wp_send_json_success(self::full_status($run));
        $inflight=get_option(self::OPT_FULL_LOCK,false);
        if(is_array($inflight)){
            if((time()-(int)($inflight['at']??0))>180){
                $run['status']='BLOCKED_UNCERTAIN';$run['errors'][]='Eine bereits an DataForSEO uebergebene Anfrage hat kein sicheres Ergebnis. Kein Retry wegen moeglicher Doppelkosten.';
                update_option(self::OPT_FULL_RUN,$run,false);
                wp_send_json_success(self::full_status($run));
            }
            wp_send_json_success(self::full_status($run)+['busy'=>true]);
        }
        if(!add_option(self::OPT_FULL_LOCK,['at'=>time(),'job'=>$run['id'],'index'=>$run['index']],'',false))
            wp_send_json_success(self::full_status($run)+['busy'=>true]);
        $i=(int)$run['index'];
        try{
            if($i>=count($run['tasks']))throw new RuntimeException('Kein weiterer Auftrag vorhanden.');
            $job=$run['tasks'][$i];
            if((float)$run['cost_usd']+(float)$job['max_charge']>(float)$run['budget_usd']+0.000001)
                throw new RuntimeException('Kostenlimit vor naechster Anfrage erreicht. Keine erneute Buchung.');
            // Log zwingend VOR dem Netzaufruf schreiben: Fehler/Timeout darf NIEMALS mit Retry bezahlt werden.
            $run['last_started']=['index'=>$i,'type'=>$job['type'],'world'=>$job['world'],'at'=>gmdate('c')];
            update_option(self::OPT_FULL_RUN,$run,false);
            $data=self::request($job['endpoint'],$job['task']);
            $charge=(float)($data['tasks'][0]['cost']??$data['cost']??0);
            if($charge<0)throw new RuntimeException('Anbieterpreis unplausibel.');
            $report=get_option(self::OPT_FULL_REPORT,[]);
            if(!is_array($report)||($report['run_id']??'')!==$run['id']){
                $p=self::build_preflight();$map=[];
                foreach($p['keywords'] as $word)$map[$word['keyword']]=$word['owners'];
                $report=['schema'=>'robotik-dfs-full-report-v1','run_id'=>$run['id'],
                    'plan_fingerprint'=>$run['plan_fingerprint'],'source_sha256'=>$run['source_sha256'],
                    'owner_map'=>$map,'keywords'=>[],'ideas'=>[],'idea_worlds'=>[],'serps'=>[],
                    'hold_reviews'=>[],'charges'=>[],'warnings'=>[],
                    'world_product_counts'=>$run['world_product_counts'],'date_utc'=>gmdate('c')];
            }
            self::full_parse($data,$job,$report);
            $report['charges'][]=['type'=>$job['type'],'world'=>$job['world'],
                'cost_usd'=>$charge,'task_id'=>(string)($data['tasks'][0]['id']??'')];
            $run['cost_usd']=(float)$run['cost_usd']+$charge;
            $run['index']=$i+1;
            if($charge>(float)$job['max_charge']+0.000001){
                $run['status']='BLOCKED_UNCERTAIN';$run['errors'][]='Anbieter-Kosten groesser als Sicherheitsreserve; keine weiteren Anfragen.';
            }elseif($run['cost_usd']>(float)$run['budget_usd']+0.000001){
                $run['status']='BLOCKED_UNCERTAIN';$run['errors'][]='Anbieter-Kostenlimit ueberschritten; keine weiteren Anfragen.';
            }elseif($run['index']===count($run['tasks'])){
                self::full_conclude($report,$run);
                $run['status']='COMPLETE';$run['completed_utc']=gmdate('c');
            }
            $report['total_cost_usd']=$run['cost_usd'];
            $report['run_status']=$run['status'];
            $report['completed_steps']=$run['index'];$report['total_steps']=$run['total'];
            $report['errors']=$run['errors'];
            $report['analysis_notes']='Suchideen sind KEINE automatische Kategorie. Google-SERP-Gleichheit ist Indiz, keine Schreibfreigabe. 300 Ideen je Welt sind eine bewusste Obergrenze, kein garantierter Vollindex.';
            update_option(self::OPT_FULL_REPORT,$report,false);
            update_option(self::OPT_FULL_RUN,$run,false);
        }catch(Throwable $e){
            $run['status']='BLOCKED_UNCERTAIN';$run['errors'][]=$e->getMessage().' Kein automatischer Retry; Anfrage koennte berechnet worden sein.';
            update_option(self::OPT_FULL_RUN,$run,false);
        }finally{delete_option(self::OPT_FULL_LOCK);}
        wp_send_json_success(self::full_status($run));
    }
    private static function full_status(array $run):array {
        return ['status'=>(string)($run['status']??'BLOCKED'),'index'=>(int)($run['index']??0),
            'total'=>(int)($run['total']??0),'cost_usd'=>(float)($run['cost_usd']??0),
            'budget_usd'=>(float)($run['budget_usd']??0),'error'=>implode(' | ',(array)($run['errors']??[]))];
    }
    public static function full_export():void {
        self::authorize('robotik_dfs_full_export');
        $report=get_option(self::OPT_FULL_REPORT,[]);$run=get_option(self::OPT_FULL_RUN,[]);
        if(!is_array($report)||empty($report['run_id']))wp_die('Noch kein Ergebnisbericht vorhanden.');
        $report['current_run_status']=$run['status']??'UNBEKANNT';
        $report['current_run_error']=$run['errors']??[];
        nocache_headers();header('Content-Type: application/json; charset=UTF-8');
        header('Content-Disposition: attachment; filename="robotik-v57-seo-gesamtbericht.json"');
        echo wp_json_encode($report,JSON_PRETTY_PRINT|JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);
        exit;
    }
    private static function full_screen():void {
        $run=get_option(self::OPT_FULL_RUN,[]);$report=get_option(self::OPT_FULL_REPORT,[]);
        echo '<h2>3. Eine vollstaendige SEO-Gesamtrecherche (einmal starten)</h2>';
        echo '<p><strong>Ein zusammenhaengender Arbeitsblock:</strong> alle 437 Suchbegriffe messen; fuer jede der acht Hauptwelten Suchideen pruefen (maximal 300 pro Welt); die 16 fachlich offenen Faelle anhand der ersten 10 organischen Google-Treffer mit Konkurrenzbegriffen vergleichen. Ein Gesamtbericht. Kein WordPress-Import.</p>';
        echo '<p>Die Recherche umfasst mehrere vom Anbieter getrennt berechnete Abfragen, laeuft nach <strong>einer ausdruecklichen Kostenfreigabe</strong> ohne weitere Klicks und stoppt vor einem neuen Aufruf, wenn das Budget nicht ausreicht. Auch bereits gestartete Anfragen koennen Kosten ausloesen; bei unklarem Ergebnis wird niemals automatisch wiederholt.</p>';
        if(!is_array($run)||empty($run['id'])){
            try{$plan=self::full_plan(self::build_preflight());
                echo '<p>8 Themenwelten, 16 HOLD-Paare, '.(int)$plan['serp_keywords'].' eindeutige Google-Suchen, '.count($plan['tasks']).' interne Aufgaben. Sicherheitsreserve: <strong>'.esc_html(number_format($plan['reservation_usd'],3,'.','')).' USD</strong>, tatsaechliche Kosten meldet der Anbieter. Auch bei fehlenden Anbieter-Daten gibt es keine automatische Nachbuchung.</p>';
            }catch(Throwable $e){echo '<div class="notice notice-error"><p>'.esc_html($e->getMessage()).'</p></div>';return;}
            echo '<form method="post" action="'.esc_url(admin_url('admin-post.php')).'">';wp_nonce_field('robotik_dfs_full_start');
            echo '<input type="hidden" name="action" value="robotik_dfs_full_start">';
            echo '<p><label><strong>Maximalbudget (USD): </strong><input type="number" name="robotik_dfs_budget_usd" min="0.01" max="20" step="0.01" value="1.00" required></label></p>';
            echo '<p><label><input type="checkbox" name="robotik_dfs_full_confirm" value="1" required> Ich gebe die <strong>kostenpflichtige Gesamtpruefung</strong> bis zu diesem Budget ausdruecklich frei (mehrere gebuendelte API-Anfragen).</label></p>';
            submit_button('SEO-Gesamtrecherche EINMAL starten','primary','submit',false);echo '</form>';
        }else{
            $s=self::full_status($run);
            echo '<p id="robotik-dfs-full-status"><strong>'.esc_html($s['status']).'</strong> · '.(int)$s['index'].' / '.(int)$s['total'].' Aufgaben · Kosten '.esc_html(number_format($s['cost_usd'],4,'.','')).' / Budget '.esc_html(number_format($s['budget_usd'],2,'.','')).' USD</p>';
            if($s['error']!=='')echo '<div class="notice notice-error"><p>'.esc_html($s['error']).'</p></div>';
            if(is_array($report)&&!empty($report['run_id'])){
                echo '<form method="post" action="'.esc_url(admin_url('admin-post.php')).'">';wp_nonce_field('robotik_dfs_full_export');
                echo '<input type="hidden" name="action" value="robotik_dfs_full_export">';
                submit_button('EINEN SEO-Gesamtbericht (JSON) herunterladen','secondary','submit',false);echo '</form>';
            }
            if($s['status']==='RUNNING'){
                $nonce=wp_create_nonce('robotik_dfs_full_step');
                echo '<script>(function(){const n='.wp_json_encode($nonce).';let busy=false;async function tick(){if(busy)return;busy=true;try{const f=new FormData();f.append("action","robotik_dfs_full_step");f.append("_ajax_nonce",n);const r=await fetch(ajaxurl,{method:"POST",credentials:"same-origin",body:f});const j=await r.json();if(!j.success)throw Error(j.data?.error||"Serverfehler");const s=j.data;document.getElementById("robotik-dfs-full-status").textContent=s.status+" · "+s.index+" / "+s.total+" Aufgaben · Kosten "+s.cost_usd+" / Budget "+s.budget_usd+" USD";if(s.status==="RUNNING"){busy=false;setTimeout(tick,s.busy?1500:250);return;}location.reload();}catch(e){document.getElementById("robotik-dfs-full-status").textContent="Unterbrochen: "+e.message+". Neu laden zeigt den gespeicherten Status; unklare Anbieteranfragen werden nicht automatisch doppelt berechnet.";}busy=false;}tick();})();</script>';
            }
        }
        echo '<details><summary>Bisherige Einzelabfragen (nur falls bewusst statt Gesamtlauf benoetigt)</summary>';
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
        self::full_screen();
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
        echo '</details>';
        echo '</div>';
    }
}