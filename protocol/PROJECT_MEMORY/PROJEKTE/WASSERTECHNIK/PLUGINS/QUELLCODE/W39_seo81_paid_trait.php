<?php
if (!defined('ABSPATH')) { exit; }
/**
 * W38: additive methods inside the ORIGINAL WT001 PaidResearch class via a PHP trait.
 * The original 218-keyword flow, original provider client and WP option keys stay unchanged.
 * Only one new 81-keyword paid job, explicitly approved, never retried automatically.
 */
trait Wassertechnik_W38_Seo81_Trait {
    private const W38_LOCK='wassertechnik_dfs_w38_81_paid_lock';
    private const W38_REPORT='wassertechnik_dfs_w38_81_paid_report';
    private const W38_MAX_USD=0.25;

    public static function planned81():array {
        self::verify_site();
        [$legacy,$oldTerms]=self::planned(); // original 218 SEO master, unchanged
        $file=dirname(__DIR__).'/assets/wassertechnik-w28-seo-handoff.json';
        $data=Wassertechnik_W30_Seo_Handoff::read($file);
        if(count((array)$data['produkte'])!==81 || ($legacy['unique_keywords']??0)!==218)
            throw new RuntimeException('Alter/neuer einmaliger SEO-Plan unvollständig.');
        $old=array_fill_keys($oldTerms,true);
        $terms=[];$owners=[];$unique=[];
        foreach($data['produkte'] as $item) {
            $raw=(string)($item['keyword_vorschlag_ungeprueft']??'');
            $kw=self::normal($raw); // ONE original DataForSEO-normalization
            $id=(string)($item['register_id']??'');
            if($kw===''||strlen($kw)>80||count(preg_split('/\s+/u',$kw))>10
               ||isset($unique[$kw])||isset($old[$kw])||$id==='')
                throw new RuntimeException('W28-Keyword-/Altowner-Konflikt, keine Kosten: '.$id);
            $unique[$kw]=true;
            $terms[]=$kw;
            $owners[$kw]=['id'=>$id,'type'=>'product','label'=>(string)$item['produktname'],
                'original_keyword'=>$raw,'source'=>'W27/W28','seo_approved'=>false];
        }
        if(count($terms)!==81||count($owners)!==81)
            throw new RuntimeException('81er Plan unvollständig.');
        $source=hash_file('sha256',$file);
        $fingerprint=hash('sha256',wp_json_encode([$terms,$owners,$source,$legacy['fingerprint']],JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES));
        return [['schema'=>'wassertechnik-dfs-w38-81-preflight-v1','fingerprint'=>$fingerprint,
                    'source_sha256'=>$source,'legacy_fingerprint'=>$legacy['fingerprint'],
                    'unique_keywords'=>81,'paid_research_approved'=>false],$terms,$owners];
    }
    /**
     * Single read-only result lookup for the existing W28 candidates.
     * A provider measurement is NEVER an approval for a new WordPress page.
     */
    public static function read81():array {
        [$plan,$terms,$owners]=self::planned81();
        $report=get_option(self::W38_REPORT,[]);
        if(!is_array($report)||empty($report['request_id']))
            return ['state'=>'NOT_STARTED','by_owner'=>[],'cost_usd'=>0.0,
                    'skipped_steps'=>[],'completed'=>[]];
        if(($report['keywords_requested']??null)!==81
           || ($report['schema']??'')!=='wassertechnik-dfs-w38-81-research-v1'
           || !hash_equals((string)$plan['fingerprint'],(string)($report['source_fingerprint']??''))
           || !hash_equals((string)$plan['legacy_fingerprint'],(string)($report['legacy_fingerprint']??'')))
            throw new RuntimeException('81er-Ergebnis gehört nicht zum aktuellen Fach-/SEO-Plan. Kein Überschreiben.');
        $rows=(array)($report['rows']??[]);
        if(count($rows)!==81)throw new RuntimeException('81er-Bericht enthält nicht alle ursprünglichen Kandidaten.');
        $byOwner=[];$seen=[];
        foreach($rows as $row) {
            if(!is_array($row))throw new RuntimeException('81er-Berichtszeile beschädigt.');
            $kw=self::normal((string)($row['keyword']??''));
            if($kw===''||!isset($owners[$kw])||isset($seen[$kw])
                ||(string)($row['owner']['id']??'')!==(string)$owners[$kw]['id'])
                throw new RuntimeException('81er-Berichts-Owner weicht vom Fachmaster ab.');
            $seen[$kw]=true;
            $byOwner[$owners[$kw]['id']]=$row;
        }
        return ['state'=>(string)($report['state']??'UNKNOWN'),
                'by_owner'=>$byOwner,'cost_usd'=>(float)($report['cost_usd']??0.0),
                'skipped_steps'=>(array)($report['skipped_steps']??[]),
                'completed'=>(array)($report['completed']??[])];
    }

    public static function panel81():void {
        if(!current_user_can('manage_options'))return;
        echo '<h2>81 neue Kaufprodukte – SEO-Sammelauftrag</h2>';
        echo '<p>Die alten 218 Keywords bleiben unangetastet. Neue Produkte werden hier nicht als WordPress-Seiten angelegt.</p>';
        $report=get_option(self::W38_REPORT,[]);
        $lock=get_option(self::W38_LOCK,false);
        if(is_array($report)&&!empty($report['request_id'])){
            echo '<p><strong>81er-Auftrag:</strong> '.esc_html((string)$report['state']).
                 ' · Kosten laut Anbieter '.esc_html(number_format((float)($report['cost_usd']??0),5,'.','')).
                 ' USD · keine automatische Wiederholung.</p>';
            if(!empty($report['error']))echo '<p><strong>Offen:</strong> '.esc_html((string)$report['error']).'</p>';
            echo '<form method="post" action="'.esc_url(admin_url('admin-post.php')).'">';
            wp_nonce_field('wassertechnik_dfs_w38_81_export');
            echo '<input type="hidden" name="action" value="wassertechnik_dfs_w38_81_export">';
            submit_button('81er-SEO-Bericht herunterladen','secondary','submit',false);
            echo '</form>';
        }
        if($lock!==false || (is_array($report)&&!empty($report["request_id"]))){
            echo '<p><strong>Dieser 81er-Auftrag ist bereits gesperrt oder ausgeführt. Keine zweite kostenpflichtige Anfrage.</strong></p>';
            return;
        }
        try{
            [$pre,$terms]=self::planned81();
            if(!Wassertechnik_DataForSEO::has_credentials())
                throw new RuntimeException('DataForSEO-Zugang im vorhandenen Wassertechnik-Plugin noch nicht vorhanden.');
            echo '<p><strong>Vorbereitet:</strong> '.count($terms).' eindeutige Keywords; separater Höchstbetrag 0,25 USD. Anbieterpreise können abweichen.</p>';
            echo '<form method="post" action="'.esc_url(admin_url('admin-post.php')).'">';
            wp_nonce_field('wassertechnik_dfs_w38_81_paid');
            echo '<input type="hidden" name="action" value="wassertechnik_dfs_w38_81_paid">';
            echo '<input type="hidden" name="plan_fingerprint" value="'.esc_attr($pre['fingerprint']).'">';
            echo '<p><label><input type="checkbox" required name="explicit_paid_approval" value="1"> Ich genehmige genau einen DataForSEO-Sammelauftrag für ausschließlich 81 neue Keywords, maximal 0,25 USD; keine erneute Abfrage der 218 bisherigen Begriffe.</label></p>';
            submit_button('81 Keywords EINMAL kostenpflichtig recherchieren','primary','submit',false);
            echo '</form>';
        }catch(Throwable $e){echo '<p><strong>Start gesperrt:</strong> '.esc_html($e->getMessage()).'</p>';}
    }
    public static function paid81():void {
        self::auth('wassertechnik_dfs_w38_81_paid');
        if((string)($_POST['explicit_paid_approval']??'')!=='1')wp_die('81er-Kostenfreigabe fehlt.');
        $report=null;
        try{
            [$pre,$terms,$owners]=self::planned81();
            $posted=isset($_POST['plan_fingerprint'])&&is_string($_POST['plan_fingerprint'])
                ?wp_unslash($_POST['plan_fingerprint']):'';
            if(!hash_equals($pre['fingerprint'],$posted))throw new RuntimeException('81er-Datenplan verändert. Keine Kosten.');
            if(!Wassertechnik_DataForSEO::has_credentials())throw new RuntimeException('DataForSEO-Zugang fehlt.');
            // No new 81er request if old 218 report/owner plan is not consistent.
            $legacyReport=get_option(self::REPORT,[]);
            if(is_array($legacyReport) && !empty($legacyReport['source_fingerprint']) &&
                !hash_equals((string)$legacyReport['source_fingerprint'],(string)$pre['legacy_fingerprint']))
                throw new RuntimeException('Alter 218er-Bericht stimmt nicht mit Originalplanung überein.');
            // A present report is a permanent deduplication receipt even if an
            // administrator accidentally deleted the separate start lock.
            $existing81=get_option(self::W38_REPORT,[]);
            if((is_array($existing81)&&!empty($existing81['request_id']))
                ||get_option(self::W38_LOCK,false)!==false)
                throw new RuntimeException('81er-Auftrag bereits begonnen oder abgeschlossen. Keine zweite Berechnung.');
            $requestId=hash('sha256','wt38:81:'.$pre['fingerprint'].':Germany:de');
            if(!add_option(self::W38_LOCK,['request_id'=>$requestId,'utc'=>gmdate('c'),'fingerprint'=>$pre['fingerprint']],'',false))
                throw new RuntimeException('81er-Lauf bereits reserviert. Keine doppelte Abrechnung.');
            $rows=[];
            foreach($terms as $kw)$rows[$kw]=[
                'keyword'=>$kw,'owner'=>$owners[$kw],'search_volume'=>null,
                'google_ads_competition'=>null,'google_ads_competition_index'=>null,
                'cpc_usd'=>null,'monthly_searches'=>null,'organic_keyword_difficulty'=>null,
                'search_intent'=>null,'search_intent_probability'=>null,'secondary_intents'=>null
            ];
            $report=[
                'schema'=>'wassertechnik-dfs-w38-81-research-v1','plugin_version'=>'0.1.9',
                'request_id'=>$requestId,'source_fingerprint'=>$pre['fingerprint'],
                'legacy_fingerprint'=>$pre['legacy_fingerprint'],'source_sha256'=>$pre['source_sha256'],
                'state'=>'RUNNING','cost_usd'=>0.0,'max_usd'=>self::W38_MAX_USD,
                'keywords_requested'=>81,'location'=>'Germany','language'=>'de',
                'completed'=>[],'attempted'=>[],'skipped_steps'=>[],'warnings'=>[],
                'rows'=>array_values($rows),'started_utc'=>gmdate('c'),'error'=>null,
                'notes'=>'Dieser Auftrag ist getrennt vom ursprünglichen 218er-Lauf. Unbekannte Werte bleiben null.'
            ];
            update_option(self::W38_REPORT,$report,false);
            $reserve=0.0;
            foreach(self::ENDPOINTS as $kind=>$endpoint){
                $estimate=(float)(self::PRICES[$kind]??self::W38_MAX_USD);
                if($reserve+(float)$report['cost_usd']+$estimate>self::W38_MAX_USD+0.0000001)
                    throw new RuntimeException('81er-Restbudget reicht nicht, Folgeaufruf gesperrt.');
                $task=['keywords'=>$terms];
                if($kind!=='intent'){$task['location_name']='Germany';$task['language_code']='de';}
                if($kind==='volume')$task['search_partners']=false;
                $report['attempted'][]=['kind'=>$kind,'endpoint'=>$endpoint,'utc'=>gmdate('c'),'result'=>'BEGONNEN'];
                update_option(self::W38_REPORT,$report,false); // Before paid call, no retry after uncertainty.
                $response=self::fetch($endpoint,$task); // SAME original provider client
                $spent=self::cost($response);            // SAME original actual cost accounting
                $report['cost_usd']+=$spent;
                $last=count($report['attempted'])-1;
                $report['attempted'][$last]['cost_usd']=$spent;
                $report['attempted'][$last]['provider_task_id']=$response['tasks'][0]['id']??null;
                $report['attempted'][$last]['provider_status']=self::provider_status($response);
                $report['attempted'][$last]['result']='ANTWORT_ERHALTEN';
                update_option(self::W38_REPORT,$report,false);
                if(self::is_provider_failure($response)){
                    $report['attempted'][$last]['result']='ANBIETERFEHLER_NICHT_WIEDERHOLT';
                    $report['skipped_steps'][]=['kind'=>$kind,'status'=>'NICHT_GEPRUEFT',
                        'provider_status'=>self::provider_status($response),'repeat_allowed'=>false];
                    if($spent<=0.0)$reserve+=$estimate;
                    $report['warnings'][]=$kind.' nicht geliefert; keine Wiederholung.';
                    update_option(self::W38_REPORT,$report,false);
                    continue;
                }
                $items=self::items($response,$endpoint);
                $matched=self::apply($kind,$items,$rows); // SAME original result parser
                // One genuine unique provider keyword per intended W28 keyword.
                // Duplicates, unrelated keywords and partial replies are NOT a completed SEO measurement.
                $uniqueMatched=[];
                foreach($items as $item){
                    if(!is_array($item))continue;
                    $kw=self::normal((string)($item['keyword']??''));
                    if(isset($rows[$kw]))$uniqueMatched[$kw]=true;
                }
                $countUnique=count($uniqueMatched);
                $report['completed'][]=['kind'=>$kind,'received_rows'=>count($items),
                    'matched_rows'=>$matched,'unique_matched_rows'=>$countUnique,'cost_usd'=>$spent];
                if($countUnique!==81){
                    $report['skipped_steps'][]=['kind'=>$kind,'status'=>'UNVOLLSTAENDIGE_ANTWORT',
                        'unique_matched_rows'=>$countUnique,'expected_rows'=>81,'repeat_allowed'=>false];
                    $report['warnings'][]=$kind.': nur '.$countUnique.' von 81 einmalig zugeordnet; fehlende Werte bleiben leer. Keine Wiederholung.';
                }
                $report['rows']=array_values($rows);
                update_option(self::W38_REPORT,$report,false);
                if($report['cost_usd']+$reserve>self::W38_MAX_USD+0.0000001)
                    throw new RuntimeException('81er-Anbieterpreis über Sicherheitslimit, Folgeschritte gestoppt.');
            }
            $report['state']=count($report['skipped_steps'])?'COMPLETE_WITH_GAPS':'COMPLETED';
            $report['finished_utc']=gmdate('c');
            update_option(self::W38_REPORT,$report,false);
        }catch(Throwable $e){
            if(is_array($report)){
                $report['state']='PARTIAL_STOPPED_NO_AUTO_RETRY';
                $report['error']=$e->getMessage();$report['finished_utc']=gmdate('c');
                update_option(self::W38_REPORT,$report,false);
            }
            // No credentials, provider responses or stack traces are displayed.
        }
        wp_safe_redirect(admin_url('admin.php?page=wassertechnik-seo81-preview'));
        exit;
    }
    public static function export81():void {
        self::auth('wassertechnik_dfs_w38_81_export');
        $report=get_option(self::W38_REPORT,[]);
        if(!is_array($report)||empty($report['request_id']))wp_die('Noch kein 81er-SEO-Bericht vorhanden.');
        nocache_headers();
        header('Content-Type: application/json; charset=UTF-8');
        header('Content-Disposition: attachment; filename="wassertechnik-dataforseo-81-seo-ergebnis.json"');
        echo wp_json_encode($report,JSON_PRETTY_PRINT|JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);
        exit;
    }
}
