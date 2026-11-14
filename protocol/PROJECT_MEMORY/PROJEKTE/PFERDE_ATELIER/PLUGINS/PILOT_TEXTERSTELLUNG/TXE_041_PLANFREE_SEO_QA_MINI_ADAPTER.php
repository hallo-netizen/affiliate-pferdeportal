<?php
if (!defined('ABSPATH')) { return; }
/**
 * Isolierter TEST-Zwischenweg. Keine Änderung an K0, PSERC, Beiträgen oder der
 * bisherigen Fachlogik. Die semantischen Entscheidungen kommen nur von außen.
 */
final class PSTE_Mini_Workflow {
    private const STORE = 'pste_mini_keyword_roundtrip_v1';
    private const CONTRACT = 'PSTE_RAW_KEYWORD_MINI_BATCH_V1';
    private const LIMITS = [100, 500, 1000, 2000];

    public static function init(): void {
        add_action('admin_post_pste_mini_keyword_export', [self::class, 'exportKeywords']);
        add_action('admin_post_pste_mini_keyword_import', [self::class, 'importKeywords']);
        add_action('admin_post_pste_mini_keyword_cancel', [self::class, 'cancelActive']);
        add_action('admin_post_pste_mini_results_export', [self::class, 'exportResults']);
        add_action('admin_post_pste_mini_title_repair_import', [self::class, 'importTitleCorrections']);
        add_action('admin_post_pste_mini_manual_brief', [self::class, 'manualArticleBrief']);
        add_action('admin_post_pste_mini_forward_to_plan', [self::class, 'forwardToPlan']);
        add_action('admin_post_pste_mini_batch_report', [self::class, 'exportBatchReport']);
        add_action('admin_post_pste_mini_context_evidence', [self::class, 'exportContextEvidence']);
        add_action('admin_post_pste_mini_legacy_plan_rebind', [self::class, 'legacyEmptyPlanRebind']);
    }

    /**
     * One fixed-size, read-only diagnosis of the EXISTING externally approved topics.
     * No topic-pool sweep, no context refresh, no PSERC compile, no new SEO decision,
     * no new log events. Maximum 200 exact source-key lookups in batches of 100.
     */
    public static function handoffPinpointSnapshot(): array {
        $state=self::loadState();
        $queue=get_option('pste_title_desk_reentry_state_v1',[]);
        $job=get_option('pserc_plan_compile_job_v1',[]);
        $baseline=get_option(defined('PSTE_OPTION_SITE_BASELINE')?PSTE_OPTION_SITE_BASELINE:'pste_site_baseline_v1',[]);
        return self::buildHandoffPinpointSnapshot(
            $state,is_array($queue)?$queue:[],
            self::readApprovedPoolRows((array)($state['seo_decisions']??[])),
            is_array($job)?$job:[],is_array($baseline)?$baseline:[]);
    }

    /** Query ONLY the already approved source keys. No full table fetch or scan. */
    private static function readApprovedPoolRows(array $receipts): array {
        global $wpdb;
        $keys=[];
        foreach($receipts as $key=>$receipt){
            if(!is_array($receipt)||($receipt['box']??'')!=='FREI')continue;
            $key=trim((string)$key);
            if($key!=='')$keys[$key]=true;
        }
        if(count($keys)>200)return ['__diagnostic_error'=>'PSTE_PINPOINT_MAX_200_FREI_EXCEEDED'];
        if(!$keys)return [];
        if(!isset($wpdb)||!is_object($wpdb)||!method_exists($wpdb,'get_results')||!method_exists($wpdb,'prepare')
            ||!class_exists('PSTE_Repository'))return ['__diagnostic_error'=>'PSTE_PINPOINT_DB_READER_MISSING'];
        $table=PSTE_Repository::table('topic_pool');$found=[];
        foreach(array_chunk(array_keys($keys),100) as $group){
            $marks=implode(',',array_fill(0,count($group),'%s'));
            $sql=$wpdb->prepare("SELECT pool_key,planning_suitability,context_state,structure_sha256,payload_json FROM $table WHERE pool_key IN ($marks)",...$group);
            $rows=$wpdb->get_results($sql,defined('ARRAY_A')?ARRAY_A:'ARRAY_A');
            if(!is_array($rows)||(string)($wpdb->last_error??'')!=='')
                return ['__diagnostic_error'=>'PSTE_PINPOINT_APPROVED_SOURCE_READ_FAILED'];
            foreach($rows as $row){
                $key=(string)($row['pool_key']??'');
                if($key!=='')$found[$key]=$row;
            }
        }
        return $found;
    }

    /** Pure classification; can be tested with exactly the same stored fields. */
    public static function buildHandoffPinpointSnapshot(array $state,array $queue,array $poolRows,array $job,array $baseline): array {
        $receiptList=(array)($state['seo_decisions']??[]);$completed=(array)($state['completed']??[]);
        $forwarded=(array)($state['plan_forwarded']??[]);$queued=(array)($state['plan_queued']??[]);
        $free=[];foreach($receiptList as $key=>$r)if(is_array($r)&&($r['box']??'')==='FREI')$free[(string)$key]=$r;
        $report=['contract'=>'PSTE_PINPOINT_HANDOFF_V1','read_only'=>true,'checked_frei'=>count($free),
            'source_lookup_scope'=>'EXACT_FREI_KEYS_MAX_200','source_rows_read'=>0,
            'count_by_reason'=>[],'recent_reentry_reasons'=>[],'plan_error'=>'',
            'plan_phase'=>'','examples'=>[],'status'=>'OK'];
        if(count($free)>200 || isset($poolRows['__diagnostic_error'])){
            $report['status']=count($free)>200?'PSTE_PINPOINT_TOO_MANY_FREI':(string)$poolRows['__diagnostic_error'];
            return $report;
        }
        $currentStructure=(string)($baseline['structure_sha256']??'');
        $report['source_rows_read']=count($poolRows);
        foreach($free as $key=>$proof){
            $decision=(array)($completed[$key]??[]);
            $title=trim((string)($decision['titles'][0]['title']??''));
            $raw=(string)($decision['raw_query']??'');
            $kind='';$row=$poolRows[$key]??null;
            if(trim((string)($proof['canonical_article_id']??''))===''||!preg_match('/^[a-f0-9]{64}$/D',(string)($proof['plan_slot']??'')))
                $kind='PLANPLATZ_VOR_MINI_FEHLT';
            elseif(!is_array($decision)||($decision['decision']??'')!=='JA'||$title==='')
                $kind='TITEL_NOCH_NICHT_ERSTELLT';
            elseif(!hash_equals($title,(string)($proof['approved_title']??'')))
                $kind='TITEL_BINDUNG_STIMMT_NICHT';
            elseif(!hash_equals((string)($proof['raw_query']??''),$raw))
                $kind='QUELLFRAGE_STIMMT_NICHT';
            elseif(!hash_equals(hash('sha256',$raw.'|'.$title),(string)($forwarded[$key]??''))
                ||!self::titleAlreadyQueued($queued,$key,hash('sha256',$raw.'|'.$title)))
                $kind='TITEL_NICHT_AN_PLAN_UEBERGEBEN';
            elseif(!is_array($row))$kind='FREIGEGEBENE_QUELLE_NICHT_IM_POOL';
            elseif(($row['planning_suitability']??'')!=='YES')$kind='POOL_PLANUNG_NICHT_FREIGEGEBEN';
            elseif(!in_array((string)($row['context_state']??''),['CURRENT','NOT_REQUIRED'],true))$kind='POOL_KONTEXT_NICHT_AKTUELL';
            elseif($currentStructure===''||!hash_equals($currentStructure,(string)($row['structure_sha256']??'')))$kind='POOL_STRUKTUR_VERALTET';
            else{
                $payload=json_decode((string)($row['payload_json']??''),true);
                if(!is_array($payload))$kind='POOL_DATEN_UNLESBAR';
                else{
                    try{$route=class_exists('PSTE_Repository')?PSTE_Repository::workflowRouteForCandidate($payload):'';}
                    catch(Throwable $ignored){$route='';}
                    $kind=$route==='K0'?'AN_PLAN_UEBERGABEFAEHIG':($route===''?'POOL_ROUTE_NICHT_LESBAR':'THEMA_NICHT_IM_K0_WEG');
                }
            }
            $report['count_by_reason'][$kind]=($report['count_by_reason'][$kind]??0)+1;
            if(!isset($report['examples'][$kind]))$report['examples'][$kind]=[];
            if(count($report['examples'][$kind])<3){
                $safeLabel=trim((string)($proof['raw_query']??''));
                $report['examples'][$kind][]=function_exists('mb_substr')?mb_substr($safeLabel,0,90,'UTF-8'):substr($safeLabel,0,90);
            }
            // History from existing title reentry, ONLY for these preapproved keys.
            $q=(array)($queue['outcomes'][$key]??[]);
            $recent=(string)($q['error_code']??'');
            if($recent!=='')$report['recent_reentry_reasons'][$recent]=($report['recent_reentry_reasons'][$recent]??0)+1;
        }
        arsort($report['count_by_reason']);arsort($report['recent_reentry_reasons']);
        $report['plan_error']=(string)($job['error_code']??'');
        $report['plan_phase']=(string)($job['error_phase']??$job['phase']??'');
        return $report;
    }

    /** Inline instead of the 120,000-entry download. No button, worker, or write. */
    private static function renderHandoffPinpoint(): void {
        try{$r=self::handoffPinpointSnapshot();}
        catch(Throwable $e){$r=['status'=>'PSTE_PINPOINT_READ_ERROR','read_only'=>true,'checked_frei'=>0,
            'count_by_reason'=>[],'recent_reentry_reasons'=>[],
            'plan_error'=>substr((string)preg_replace('/[^A-Za-z0-9_]+/','_',strtoupper($e->getMessage())),0,100),'examples'=>[]];}
        echo '<section class="pste-box"><h3>Gezielte Fehlerdiagnose – nur freigegebene Themen</h3>';
        echo '<p><strong>'.(int)($r['checked_frei']??0).' FREI-Themen geprüft.</strong> Kein Gesamtlauf, keine neue SEO-Prüfung, kein Download. Nur bestehende Daten gelesen.</p>';
        if(($r['status']??'')!=='OK')echo '<p><strong>Diagnose:</strong> <code>'.esc_html((string)$r['status']).'</code></p>';
        foreach((array)($r['count_by_reason']??[]) as $reason=>$count){
            echo '<p style="margin:3px 0"><strong>'.(int)$count.' ×</strong> '.esc_html(self::handoffReasonLabel((string)$reason))
                .' <code>'.esc_html((string)$reason).'</code>';
            $examples=(array)($r['examples'][$reason]??[]);
            if($examples)echo '<br><small>Beispiele: '.esc_html(implode(' · ',array_slice($examples,0,2))).'</small>';
            echo '</p>';
        }
        if(!empty($r['plan_error']))echo '<p><strong>Letzter Redaktionsplan-Stopp:</strong> <code>'.esc_html((string)$r['plan_error']).'</code>'
            .' ('.esc_html((string)($r['plan_phase']??'')).')</p>';
        if(!empty($r['recent_reentry_reasons'])){
            echo '<p><strong>Letzter Titel-Rücklauf (historisch):</strong> ';
            $parts=[];foreach((array)$r['recent_reentry_reasons'] as $reason=>$n)$parts[]=((int)$n).' × '.(string)$reason;
            echo esc_html(implode(' · ',array_slice($parts,0,5))).'</p>';
        }
        echo '<p><small>Dieser Bericht zeigt den aktuellen Zustand, er erzeugt keine neuen Arbeitsschritte und schreibt keine Protokolle.</small></p></section>';
    }

    private static function handoffReasonLabel(string $reason): string {
        $labels=[
            'PLANPLATZ_VOR_MINI_FEHLT'=>'Artikelplatz fehlt vor MINI',
            'TITEL_NOCH_NICHT_ERSTELLT'=>'Freigegeben, Titel fehlt noch',
            'TITEL_BINDUNG_STIMMT_NICHT'=>'Gespeicherter Titel passt nicht zur Freigabe',
            'QUELLFRAGE_STIMMT_NICHT'=>'Originalthema stimmt nicht überein',
            'TITEL_NICHT_AN_PLAN_UEBERGEBEN'=>'Titel vorhanden, aber Übergabe fehlt',
            'FREIGEGEBENE_QUELLE_NICHT_IM_POOL'=>'Freigegebenes Thema fehlt im Themenbestand',
            'POOL_PLANUNG_NICHT_FREIGEGEBEN'=>'Themenbestand ist nicht für Planung freigegeben',
            'POOL_KONTEXT_NICHT_AKTUELL'=>'Gespeicherter Kontext ist nicht aktuell',
            'POOL_STRUKTUR_VERALTET'=>'Gespeicherte Kategoriezuordnung ist veraltet',
            'POOL_DATEN_UNLESBAR'=>'Gespeichertes Thema beschädigt',
            'THEMA_NICHT_IM_K0_WEG'=>'Thema gehört nicht zum normalen K0-Weg',
            'POOL_ROUTE_NICHT_LESBAR'=>'Themenroute konnte nicht gelesen werden',
            'AN_PLAN_UEBERGABEFAEHIG'=>'Thema ist an den Plan übergabefähig',
        ];return (string)($labels[$reason]??$reason);
    }

    /** The unchanged existing PSTE governance is the sole source for both title desks. */
    private static function titleGovernance(): array {
        $raw=@file_get_contents(PSTE_DIR.'contracts/intent-first-title-governance-v1.json');
        if(!is_string($raw))throw new RuntimeException('PSTE_MINI_TITLE_RULES_UNAVAILABLE');
        $governance=json_decode($raw,true,128,JSON_THROW_ON_ERROR);
        if(!is_array($governance)||($governance['contract']??'')!=='PSTE_INTENT_FIRST_TITLE_GOVERNANCE_V1')
            throw new RuntimeException('PSTE_MINI_TITLE_RULES_INVALID');
        return $governance;
    }

    /** Only objective hard title checks here; linguistic naturalness belongs to the external language desk. */
    public static function validateTitleText(string $title): void {
        self::assertOneMainQuestion($title);
        $title=trim($title);
        $length=function_exists('mb_strlen')?mb_strlen($title,'UTF-8'):strlen($title);
        if($length<8||$length>110)throw new RuntimeException('PSTE_MINI_TITLE_LENGTH_INVALID');
        if(str_contains($title,':'))throw new RuntimeException('PSTE_MINI_TITLE_COLON_FORBIDDEN');
        // The original title governance permits natural German, a dash and terminal questions.
        if(preg_match('/[^\p{L}\p{N}\s,?–-]/u',$title))throw new RuntimeException('PSTE_MINI_TITLE_SPECIAL_CHARACTER_FORBIDDEN');
        $questionCount=substr_count($title,'?');
        if($questionCount>1||($questionCount===1&&!str_ends_with($title,'?')))
            throw new RuntimeException('PSTE_MINI_TITLE_QUESTION_MUST_END_TITLE');
        if(preg_match('/\s{2,}|\b([\p{L}\d]+)\s+\1\b/iu',$title))
            throw new RuntimeException('PSTE_MINI_TITLE_REPEATED_OR_WHITESPACE');
        if(PSTE_Title_Validator::hasArtificialGeneratorPhrase($title)||
            PSTE_Title_Validator::hasForbiddenTitlePhraseFamily($title)||
            PSTE_Title_Validator::isRepeatedGenericBeratungSchema($title))
            throw new RuntimeException('PSTE_MINI_TITLE_ARTIFICIAL_STYLE_FORBIDDEN');
    }

    /** One objective shape check at the ORIGINAL MINI intake, never a second SEO or WP title owner. */
    private static function assertOneMainQuestion(string $title): void {
        $q=trim($title);
        if(substr_count($q,'?')>1 || (bool)preg_match('/\b(?:woran|wie|was|warum|wieso|weshalb|wann|welch(?:e|er|es)|wer|kann|soll|muss)\b.*\b(?:und|oder)\s+(?:woran|wie|was|warum|wieso|weshalb|wann|welch(?:e|er|es)|wer|kann|soll|muss)\b/iu',$q))
            throw new RuntimeException('PSTE_MINI_TITLE_TWO_MAIN_QUESTIONS');
    }

    private static function loadState(): array {
        $state=get_option(self::STORE, []);
        if(!is_array($state))throw new RuntimeException('PSTE_MINI_STATE_DAMAGED');
        $state += ['completed'=>[], 'active'=>null, 'last_report'=>[], 'clarification'=>[]];
        if(!is_array($state['completed'])||(!is_null($state['active'])&&!is_array($state['active'])))
            throw new RuntimeException('PSTE_MINI_STATE_DAMAGED');
        return $state;
    }
    private static function storeState(array $state): void {
        if(!update_option(self::STORE, $state, false)) {
            $read=get_option(self::STORE, null);
            if($read!==$state)throw new RuntimeException('PSTE_MINI_STATE_WRITE_FAILED');
        }
        if(get_option(self::STORE, null)!==$state)throw new RuntimeException('PSTE_MINI_STATE_READBACK_FAILED');
    }
    private static function sendJson(array $document, string $name): void {
        $raw=wp_json_encode($document,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES|JSON_PRETTY_PRINT);
        if(!is_string($raw))throw new RuntimeException('PSTE_MINI_JSON_ENCODING_FAILED');
        nocache_headers();header('Content-Type: application/json; charset=utf-8');
        header('Content-Disposition: attachment; filename="'.$name.'"');
        header('Content-Length: '.strlen($raw));echo $raw;exit;
    }
    private static function fail(Throwable $e): void {wp_die('Mini-Workflow: '.esc_html($e->getMessage()));}

    /** Compact operator surface; existing expert actions remain, but never lead the normal path. */
    public static function renderKeywords(): void {
        $state=self::loadState();$active=$state['active'];
        $completed=(array)$state['completed'];$receipts=(array)($state['seo_decisions']??[]);
        $counts=['FREI'=>0,'BELEGT'=>0,'KLAERUNG'=>0];
        foreach($receipts as $receipt){
            $box=is_array($receipt)?(string)($receipt['box']??''):'';
            if(isset($counts[$box]))$counts[$box]++;
        }
        $unresolved=count((array)($state['clarification']??[]));
        echo '<section class="pste-box"><h3>Externe SEO-Prüfung</h3>';
        echo '<p>Bestehende Daten exportieren → extern EINMAL prüfen → Ergebnis importieren → Status.</p>';
        echo '<p><strong>Gespeicherte Stichwörter:</strong> '.esc_html((string)count($completed)).
            ' · <strong>Offener Stapel:</strong> '.esc_html((string)(is_array($active)?count((array)($active['items']??[])):0)).'</p>';
        echo '<p><strong>FREI:</strong> '.esc_html((string)$counts['FREI']).
            ' · <strong>BELEGT:</strong> '.esc_html((string)$counts['BELEGT']).
            ' · <strong>KLÄRUNG:</strong> '.esc_html((string)max($unresolved,$counts['KLAERUNG'])).'</p>';
        self::renderHandoffPinpoint();
        // The ONE normal route: external SEO decision first, title-only MINI second.
        echo '<form method="post" action="'.esc_url(admin_url('admin-post.php')).'">';
        wp_nonce_field('pste_mini_results_export');
        echo '<input type="hidden" name="action" value="pste_mini_results_export">'
            .'<input type="hidden" name="include_parkhaus" value="1">'
            .'<button class="button button-primary" type="submit">1. Offene Themen für einmalige SEO-Entscheidung exportieren</button></form>';
        echo '<form method="post" enctype="multipart/form-data" action="'.esc_url(admin_url('admin-post.php')).'" style="margin-top:10px">';
        wp_nonce_field('pste_mini_title_repair_import');
        echo '<input type="hidden" name="action" value="pste_mini_title_repair_import">'
            .'<label>2. Geprüfte SEO-Entscheidungen <input type="file" name="mini_corrected_titles_json" accept=".json,application/json" required></label> '
            .'<button class="button" type="submit">Einmalige Entscheidung übernehmen</button></form>';
        $ready=0;
        foreach($receipts as $key=>$receipt)if(is_array($receipt)
            &&($receipt['box']??'')==='FREI'&&!isset($completed[$key]))$ready++;
        if($ready||$active){
            echo '<p><small>Freigegebene Themen ohne Titel: '.(int)$ready.'</small></p>';
            echo '<form method="post" action="'.esc_url(admin_url('admin-post.php')).'">';
            wp_nonce_field('pste_mini_keyword_export');
            echo '<input type="hidden" name="action" value="pste_mini_keyword_export">'
                .'<input type="hidden" name="mini_limit" value="100">'
                .'<button class="button" type="submit">3. Nur Titelauftrag für freigegebene Themen exportieren</button></form>';
            echo '<form method="post" enctype="multipart/form-data" action="'.esc_url(admin_url('admin-post.php')).'" style="margin-top:10px">';
            wp_nonce_field('pste_mini_keyword_import');
            echo '<input type="hidden" name="action" value="pste_mini_keyword_import">'
                .'<label>MINI-Titelergebnis <input type="file" name="mini_result_json" accept=".json,application/json" required></label> '
                .'<button class="button" type="submit">Titelformulierung übernehmen</button></form>';
        }
        if($active){
            echo '<form method="post" action="'.esc_url(admin_url('admin-post.php')).'" style="margin-top:10px">';
            wp_nonce_field('pste_mini_keyword_cancel');
            echo '<input type="hidden" name="action" value="pste_mini_keyword_cancel">'
                .'<button class="button" type="submit">Offenen alten Stapel abbrechen</button></form>';
        }
        if($completed){
            echo '<form method="post" action="'.esc_url(admin_url('admin-post.php')).'" style="margin-top:10px">';
            wp_nonce_field('pste_mini_forward_to_plan');
            echo '<input type="hidden" name="action" value="pste_mini_forward_to_plan">'
                .'<button class="button" type="submit">4. Fertige Titel an bestehenden Redaktionsplan übergeben</button></form>';
        }
        echo '<p><small>Keine zweite fachliche Entscheidung in MINI oder im Redaktionsplan. Fehlende Freigabe bleibt angehalten.</small></p>';
        echo '</section>';
    }

    /** One MINI source of truth for an already imported JA. No copied relevance receipt. */
    public static function approvedRelevanceFor(string $poolKey,string $rawQuery): array {
        $state=self::loadState();
        $decision=$state['completed'][$poolKey]??null;
        if(!is_array($decision)||($decision['decision']??'')!=='JA')return [];
        $raw=PSTE_Normal_Metadata_Path::canonicalInputQuery($rawQuery);
        $source=PSTE_Normal_Metadata_Path::canonicalInputQuery((string)($decision['raw_query']??''));
        if($raw===''||$source===''||!hash_equals($raw,$source))
            throw new RuntimeException('PSTE_MINI_SOURCE_BINDING_MISMATCH');
        return PSTE_Portal_Relevance_Gate::proofFromExternal([
            'contract'=>'PSTE_MINI_RESULTS_FOR_EDITORIAL_V1',
            'status'=>'RELEVANT_FOR_PORTAL','decision_source'=>'PSTE_MINI_ADMIN_IMPORT',
            'batch_id'=>(string)($decision['batch_id']??'')],$source);
    }

    /**
     * One bounded, nonce-protected, read-only snapshot of the real WP context
     * needed for a complete offline replay. No rebuild, no SQL update, no auto-retry.
     * Every stage is isolated: a damaged/stale source is reported as an error,
     * never replaced by invented data or allowed to authorize production.
     */
    public static function contextEvidenceDocument(): array {
        $baseline=get_option(PSTE_OPTION_SITE_BASELINE,[]);
        $job=get_option(PSTE_OPTION_CONTEXT_JOB,[]);
        $manifest=get_option(PSTE_OPTION_CONTEXT_INDEX_MANIFEST,[]);
        $queue=get_option('pste_title_desk_reentry_state_v1',[]);
        $result=[
            'contract'=>'PSTE_MINI_READ_ONLY_CONTEXT_EVIDENCE_V1',
            'generated_utc'=>gmdate('c'),
            'pste_version'=>PSTE_VERSION,
            'read_only'=>true,
            'production_approval'=>false,
            'wp_posts_write_attempted'=>false,
            'wordpress_taxonomy_write_attempted'=>false,
            'baseline'=>is_array($baseline)?$baseline:[],
            'context_job'=>is_array($job)?array_intersect_key($job,array_flip([
                'contract','status','job_uuid','phase','inventory_sha256','structure_sha256',
                'editorial_plan_sha256','context_index_manifest_sha256','error_code',
                'baseline_sha256','total','processed'])):[],
            'context_manifest'=>is_array($manifest)?array_intersect_key($manifest,array_flip([
                'contract','job_uuid','baseline_sha256','inventory_sha256','structure_sha256',
                'editorial_plan_sha256','manifest_sha256','registry_stage_meta',
                'inventory_stage_meta','family_count','shard_count'])):[],
            'title_reentry'=>is_array($queue)?[
                'status'=>(string)($queue['status']??'NOT_STARTED'),
                'total'=>(int)($queue['total']??0),
                'done_count'=>count((array)($queue['done']??[])),
                'pending_keys'=>array_values(array_map('strval',(array)($queue['pending']??[]))),
                'last_error'=>(string)($queue['last_error']??'')]:[],
            'sources'=>[],
        ];
        $reads=[
            'current_editorial_plan'=>static fn()=>PSTE_Snapshot::editorialPlan(),
            'current_editorial_plan_provenance'=>static fn()=>PSTE_Snapshot::editorialPlanForParkhaus(),
            'current_category_structure'=>static fn()=>PSTE_Snapshot::structure(),
            'current_wp_inventory'=>static fn()=>PSTE_Snapshot::inventory(),
        ];
        foreach($reads as $name=>$read){
            try{
                $value=$read();
                if(!is_array($value))throw new RuntimeException('SOURCE_NOT_ARRAY');
                $result['sources'][$name]=['status'=>'PASS','value'=>$value];
            }catch(Throwable $e){
                $result['sources'][$name]=['status'=>'ERROR',
                    'error_code'=>substr((string)preg_replace('/[^A-Z0-9_:\-]/i','_',strtoupper($e->getMessage())),0,160)];
            }
        }
        foreach(['registry_stage'=>PSTE_OPTION_CONTEXT_STAGE_REGISTRY,
                  'inventory_stage'=>PSTE_OPTION_CONTEXT_STAGE_INVENTORY] as $name=>$key){
            $raw=get_option($key,null);
            if(!is_string($raw)||$raw===''){$result['sources'][$name]=['status'=>'NOT_AVAILABLE'];continue;}
            if(strlen($raw)>4000000){$result['sources'][$name]=['status'=>'TOO_LARGE','bytes'=>strlen($raw)];continue;}
            $decoded=json_decode($raw,true);
            $result['sources'][$name]=is_array($decoded)
                ? ['status'=>'PASS','raw_sha256'=>hash('sha256',$raw),'bytes'=>strlen($raw),'value'=>$decoded]
                : ['status'=>'ERROR','error_code'=>'STAGE_JSON_INVALID'];
        }
        $result['comparison']=[
            'baseline_plan_sha256'=>(string)($baseline['editorial_plan_sha256']??''),
            'bound_plan_sha256'=>(string)($manifest['editorial_plan_sha256']??''),
            'live_plan_sha256'=>(string)($result['sources']['current_editorial_plan']['value']['sha256']??''),
            'baseline_category_count'=>(int)($baseline['leaf_category_count']??0),
            'live_production_category_count'=>count((array)($result['sources']['current_category_structure']['value']['items']??[])),
        ];
        $result['comparison']['bound_plan_matches_live']=$result['comparison']['bound_plan_sha256']!==''
            &&hash_equals($result['comparison']['bound_plan_sha256'],$result['comparison']['live_plan_sha256']);
        return $result;
    }

    public static function exportContextEvidence(): void {
        try{
            PSTE_Auth::assertAdmin('pste_mini_context_evidence',(string)($_POST['_wpnonce']??''));
            self::sendJson(self::contextEvidenceDocument(),'pste-plan-kategorien-pruefstand-'.gmdate('Y-m-d').'.json');
        }catch(Throwable $e){self::fail($e);}
    }

    /** Existing read-only result owner; no 5,000-topic or 20,000-event scan. */
    public static function exportBatchReport(): void {
        try{
            PSTE_Auth::assertAdmin('pste_mini_batch_report',(string)($_POST['_wpnonce']??''));
            if(!class_exists('PSTE_Admin'))throw new RuntimeException('PSTE_MINI_REPORT_OWNER_MISSING');
            self::sendJson(['contract'=>'PSTE_MINI_CURRENT_BATCH_REPORT_V1',
                'generated_utc'=>gmdate('c'),'read_only'=>true,'pste_version'=>PSTE_VERSION,
                'title_desk_reentry'=>PSTE_Admin::titleDeskReentryDiagnostics()],
                'pste-stapelbericht-'.gmdate('Y-m-d').'.json');
        }catch(Throwable $e){self::fail($e);}
    }

    public static function exportResults(): void {
        try {
            PSTE_Auth::assertAdmin('pste_mini_results_export',(string)($_POST['_wpnonce']??''));
            $state=self::loadState();
            $out=['contract'=>'PSTE_MINI_RESULTS_FOR_EDITORIAL_V1','created_utc'=>gmdate('c'),
                'count'=>count($state['completed']),'items'=>array_values($state['completed']),
                'status'=>'STAGED_NOT_EDITORIALLY_APPROVED',
                'clarification'=>array_values((array)($state['clarification']??[])),
                'note'=>'External relevance/title ideas only; NO final SEO/slot clearance.'];
            if(!empty($_POST['include_parkhaus'])){
                // Only NEW topics that have not been decided. Source frozen at original raw query.
                $excluded=(array)$state['completed'];
                foreach((array)($state['seo_decisions']??[]) as $key=>$receipt)$excluded[$key]=true;
                $selected=self::selectNewRows(static fn(int $cursor,int $size): array=>self::readRawRows($cursor,$size),$excluded,100);
                $out['seo_subjects']=[];
                foreach($selected['items'] as $row){
                    $raw=(string)$row['raw_query'];$key=(string)$row['pool_key'];
                    $out['seo_subjects'][]=['pool_key'=>$key,'raw_query'=>$raw,
                        'source_sha256'=>hash('sha256',$key.'|'.$raw)];
                }
                $out['parkhaus_snapshot']=self::readParkhausForMini();
                $out['parkhaus_complete']=!empty($out['parkhaus_snapshot']['complete']);
                $out['status']='PARKHAUS_FOR_SINGLE_EXTERNAL_SEO_OWNER_NOT_APPROVED';
            }
            self::sendJson($out,'pferdeatelier-mini-ergebnisse-'.gmdate('Ymd-His').'.json');
        }catch(Throwable $e){self::fail($e);}
    }

    public static function cancelActive(): void {
        try {
            PSTE_Auth::assertAdmin('pste_mini_keyword_cancel',(string)($_POST['_wpnonce']??''));
            $state=self::loadState();$state['active']=null;self::storeState($state);
            wp_safe_redirect(admin_url('admin.php?page=portal-seo-topic-engine-review&pste_mini_cancelled=1'));exit;
        }catch(Throwable $e){self::fail($e);}
    }

    /** Raw source inventory for the ONE upstream SEO decision, never a MINI title batch. */
    public static function selectNewRows(callable $readPage, array $completed, int $limit): array {
        if(!in_array($limit,self::LIMITS,true))throw new RuntimeException('PSTE_MINI_LIMIT_INVALID');
        $items=[];$cursor=0;$invalid=0;$seen=[];$pages=0;
        do {
            $rows=$readPage($cursor, 500);
            if(!is_array($rows))throw new RuntimeException('PSTE_MINI_SOURCE_READ_FAILED');
            foreach($rows as $row){
                $id=(int)($row['id']??0);$key=trim((string)($row['pool_key']??''));
                if($id<=$cursor||$key==='')throw new RuntimeException('PSTE_MINI_SOURCE_ORDER_OR_ID_INVALID');
                $cursor=$id;
                if(isset($completed[$key])||isset($seen[$key]))continue;
                $seen[$key]=true;
                $payload=json_decode((string)($row['payload_json']??''),true);
                $raw=is_array($payload)?PSTE_Editorializer::sourceQuery($payload):'';
                if($raw===''){$invalid++;continue;}
                $items[]=['id'=>$id,'pool_key'=>$key,'raw_query'=>$raw,
                    'source_sha256'=>hash('sha256',$id.'|'.$key.'|'.$raw),
                    'decision'=>'','titles'=>[]];
                if(count($items)===$limit)break;
            }
            if(count($items)===$limit||count($rows)<500)break;
            $pages++;
            if($pages>20000)throw new RuntimeException('PSTE_MINI_SOURCE_SCAN_LIMIT');
        }while(true);
        return ['items'=>$items,'skipped_invalid'=>$invalid,'last_scanned_id'=>$cursor];
    }

    /** Already approved source+intent only; MINI must never receive unapproved raw questions. */
    public static function selectApprovedTitleRows(array $rows,array $completed,array $receipts,int $limit): array {
        if(!in_array($limit,self::LIMITS,true))throw new RuntimeException('PSTE_MINI_LIMIT_INVALID');
        $items=[];$seen=[];
        foreach($rows as $row){
            if(!is_array($row))throw new RuntimeException('PSTE_MINI_SOURCE_READ_FAILED');
            $key=(string)($row['pool_key']??'');
            if($key===''||isset($seen[$key]))throw new RuntimeException('PSTE_MINI_TITLE_SOURCE_DUPLICATE');
            $seen[$key]=true;
            if(isset($completed[$key]))continue;
            $proof=(array)($receipts[$key]??[]);
            if(($proof['contract']??'')!=='PSTE_MINI_SEO_DECISIONS_V1'||($proof['box']??'')!=='FREI')continue;
            $data=json_decode((string)($row['payload_json']??''),true);
            $raw=is_array($data)?PSTE_Editorializer::sourceQuery($data):'';
            $slot=(string)($proof['intent_slot']??'');
            $canonical=trim((string)($proof['canonical_article_id']??''));
            $planSlot=(string)($proof['plan_slot']??'');
            $type=(string)($proof['article_type']??'');
            $category=(string)($proof['category_slug']??'');
            $snapshot=(string)($proof['snapshot_sha256']??'');
            $intent=trim((string)($proof['intent_summary']??''));
            if($raw===''||!hash_equals($raw,(string)($proof['raw_query']??''))
                ||!hash_equals(hash('sha256',$key.'|'.$raw),(string)($proof['source_sha256']??''))
                ||!hash_equals($type,(string)($data['proposed_article_type']??''))
                ||!hash_equals($category,(string)($data['target_category_slug']??''))
                ||!preg_match('/^[a-f0-9]{64}$/D',$slot)
                ||!preg_match('/^[a-f0-9]{64}$/D',$snapshot)||$intent===''
                ||$canonical===''||!class_exists('PSERC_Plan_Slot_Identity')
                ||!hash_equals(PSERC_Plan_Slot_Identity::tokenFromCanonicalId($canonical),$planSlot)
                ||$type===''||$category===''
                ||trim((string)($proof['approved_title']??''))!=='')
                throw new RuntimeException('PSTE_MINI_PRETITLE_APPROVAL_INVALID');
            $id=(int)($row['id']??0);
            if($id<=0)throw new RuntimeException('PSTE_MINI_TITLE_SOURCE_ID_INVALID');
            $items[]=['id'=>$id,'pool_key'=>$key,'raw_query'=>$raw,
                'source_sha256'=>hash('sha256',$id.'|'.$key.'|'.$raw),
                'decision'=>'JA','titles'=>[['intent'=>$intent,'title'=>'']],
                'intent_slot'=>$slot,'seo_snapshot_sha256'=>$snapshot,
                'canonical_article_id'=>$canonical,'plan_slot'=>$planSlot,
                'article_type'=>$type,'category_slug'=>$category];
            if(count($items)>=$limit)break;
        }
        return ['items'=>$items,'skipped_invalid'=>0,'title_only'=>true];
    }

    public static function createBatch(array $selected, string $batchId): array {
        if(!is_array($selected['items']??null)||!$selected['items'])throw new RuntimeException('PSTE_MINI_NO_OPEN_KEYWORDS');
        if(!preg_match('/^[a-zA-Z0-9_-]{6,100}$/',$batchId))throw new RuntimeException('PSTE_MINI_BATCH_ID_INVALID');
        if(empty($selected['title_only']))throw new RuntimeException('PSTE_MINI_FINAL_SEO_DECISION_REQUIRED_BEFORE_TITLE');
        foreach($selected['items'] as $item)if(($item['decision']??'')!=='JA'
            ||count((array)($item['titles']??[]))!==1
            ||trim((string)($item['titles'][0]['intent']??''))===''
            ||(string)($item['titles'][0]['title']??'')!=='')
            throw new RuntimeException('PSTE_MINI_TITLE_ONLY_SOURCE_INVALID');
        return ['contract'=>self::CONTRACT,'batch_id'=>$batchId,'created_utc'=>gmdate('c'),
            'title_only'=>true,
            'instruction'=>'Nur einen natuerlichen deutschen Titel fuer die fest freigegebene Suchabsicht schreiben. AUSSCHLIESSLICH items[*].titles[0].title aendern. Fachentscheid, Suchintention, Kategorie, Beitragsart und Reservierung sind bereits entschieden und du darfst sie NICHT aendern. Titel ohne Doppelpunkte oder Keyword-Schablonen, genau eine Hauptfrage. Keine neue SEO- oder Doppelungsentscheidung.',
            'title_governance'=>self::titleGovernance(),
            'skipped_invalid_source_count'=>(int)($selected['skipped_invalid']??0),
            'items'=>$selected['items']];
    }

    private static function readRawRows(int $cursor,int $limit): array {
        global $wpdb;$table=PSTE_Repository::table('topic_pool');
        $query=$wpdb->prepare("SELECT id,pool_key,payload_json FROM $table WHERE id>%d ORDER BY id ASC LIMIT %d",$cursor,$limit);
        $rows=$wpdb->get_results($query,ARRAY_A);
        if(!is_array($rows)||(string)($wpdb->last_error??'')!=='')throw new RuntimeException('PSTE_MINI_SOURCE_READ_FAILED');
        return $rows;
    }
    public static function exportKeywords(): void {
        try {
            PSTE_Auth::assertAdmin('pste_mini_keyword_export',(string)($_POST['_wpnonce']??''));
            $limit=(int)($_POST['mini_limit']??0);
            if(!in_array($limit,self::LIMITS,true))throw new RuntimeException('PSTE_MINI_LIMIT_INVALID');
            $state=self::loadState();
            if(is_array($state['active'])){
                if(empty($state['active']['title_only']))throw new RuntimeException('PSTE_MINI_OLD_RELEVANCE_BATCH_MUST_BE_CANCELLED');
                $batch=$state['active'];
            }
            else {
                // Existing SEO decisions are the only source for a new MINI title batch.
                // Read approved pool keys, not the first arbitrary N raw keywords.
                global $wpdb;$table=PSTE_Repository::table('topic_pool');$rows=[];
                $keys=[];
                foreach((array)($state['seo_decisions']??[]) as $key=>$proof){
                    if(is_array($proof)&&($proof['box']??'')==='FREI'&&!isset($state['completed'][$key]))$keys[]=(string)$key;
                }
                foreach(array_chunk($keys,100) as $chunk){
                    $marks=implode(',',array_fill(0,count($chunk),'%s'));
                    $found=$wpdb->get_results($wpdb->prepare("SELECT id,pool_key,payload_json FROM $table WHERE pool_key IN ($marks)",...$chunk),ARRAY_A);
                    if(!is_array($found)||(string)($wpdb->last_error??'')!=='')throw new RuntimeException('PSTE_MINI_TITLE_DB_READ_FAILED');
                    foreach($found as $row)$rows[]=$row;
                }
                if(count($rows)!==count($keys))throw new RuntimeException('PSTE_MINI_PREAPPROVED_SOURCE_MISSING');
                usort($rows,static fn($a,$b)=>(int)$a['id']<=>(int)$b['id']);
                $selected=self::selectApprovedTitleRows($rows,(array)$state['completed'],(array)($state['seo_decisions']??[]),$limit);
                $batch=self::createBatch($selected,'mini-'.gmdate('YmdHis').'-'.substr(bin2hex(random_bytes(6)),0,12));
                $state['active']=$batch;self::storeState($state); // Retry the identical batch.
            }
            self::sendJson($batch,'pferdeatelier-rohkeywords-'.$batch['batch_id'].'.json');
        } catch(Throwable $e){self::fail($e);}
    }

    /** Pure preflight: the stored export is the sole source of truth, not the uploaded file. */
    public static function validateResult(array $original,array $received,callable $loadCurrent): array {
        if(($original['contract']??'')!==self::CONTRACT||($received['contract']??'')!==self::CONTRACT||
            ($original['batch_id']??'')!==($received['batch_id']??''))throw new RuntimeException('PSTE_MINI_WRONG_BATCH');
        // Compare to the rules actually exported with THIS frozen batch. New
        // governance must not retrospectively invalidate an older active batch.
        if(array_key_exists('title_governance',$received)
            &&$received['title_governance']!==($original['title_governance']??self::titleGovernance()))
            throw new RuntimeException('PSTE_MINI_TITLE_RULES_CHANGED');
        if(!empty($original['title_only'])&&($received['title_only']??null)!==true)
            throw new RuntimeException('PSTE_MINI_TITLE_ONLY_CONTRACT_CHANGED');
        $before=$original['items']??null;$after=$received['items']??null;
        if(!is_array($before)||!is_array($after)||count($before)!==count($after)||!array_is_list($after))
            throw new RuntimeException('PSTE_MINI_ITEM_COUNT_CHANGED');

        // KISS: one transport owner. An individual broken answer goes into the existing
        // option's clarification box; other source-bound answers are not re-judged.
        $finished=[];$held=[];$stats=['JA'=>0,'NEIN'=>0,'VIELLEICHT'=>0,'titles'=>0,'clarification'=>0];
        foreach($before as $i=>$frozen){
            if(!is_array($frozen)||trim((string)($frozen['pool_key']??''))==='')
                throw new RuntimeException('PSTE_MINI_ORIGINAL_BATCH_INVALID');
            // The existing DB reader owns infrastructure failures. A database outage is
            // NOT an editorial issue and must still stop safe writes for this batch.
            $current=$loadCurrent((string)$frozen['pool_key']);
            try {
                $item=$after[$i]??null;
                if(!is_array($item))throw new RuntimeException('PSTE_MINI_ITEM_INVALID');
                $keys=array_keys($item);sort($keys);$allowed=array_keys($frozen);sort($allowed);
                if($keys!==$allowed)throw new RuntimeException('PSTE_MINI_ITEM_FIELDS_CHANGED');
                foreach(['id','pool_key','raw_query','source_sha256'] as $field){
                    if(!array_key_exists($field,$item)||$item[$field]!==$frozen[$field])
                        throw new RuntimeException('PSTE_MINI_SOURCE_CHANGED_'.$field);
                }
                $payload=is_array($current)?json_decode((string)($current['payload_json']??''),true):null;
                $raw=is_array($payload)?PSTE_Editorializer::sourceQuery($payload):'';
                $actual=hash('sha256',(int)($current['id']??0).'|'.(string)($current['pool_key']??'').'|'.$raw);
                if(!is_array($current)||!hash_equals((string)$frozen['source_sha256'],$actual))
                    throw new RuntimeException('PSTE_MINI_DATABASE_SOURCE_CHANGED');
                if(!empty($original['title_only'])){
                    // Compare every frozen field, not only key names. MINI may
                    // change exactly one title string and nothing else.
                    $frozenBrief=$frozen;$incomingBrief=$item;
                    unset($frozenBrief['titles'][0]['title'],$incomingBrief['titles'][0]['title']);
                    if($frozenBrief!==$incomingBrief)
                        throw new RuntimeException('PSTE_MINI_TITLE_ONLY_FROZEN_FIELDS_CHANGED');
                    if(($item['decision']??null)!=='JA'
                        ||$item['titles']===null||!is_array($item['titles'])||count($item['titles'])!==1
                        ||(string)($item['titles'][0]['intent']??'')!==(string)($frozen['titles'][0]['intent']??'')
                        ||(string)($frozen['titles'][0]['title']??'')!=='')
                        throw new RuntimeException('PSTE_MINI_TITLE_ONLY_DECISION_OR_INTENT_CHANGED');
                    // Pure title format and hard quality; never an additional SEO judgement.
                    self::validateTitleText((string)($item['titles'][0]['title']??''));
                }
                $decision=$item['decision']??null;
                if(!is_string($decision)||!in_array($decision,['JA','NEIN','VIELLEICHT'],true))
                    throw new RuntimeException('PSTE_MINI_DECISION_REQUIRED');
                $titles=$item['titles']??null;
                if(!is_array($titles)||!array_is_list($titles))throw new RuntimeException('PSTE_MINI_TITLES_INVALID');
                if($decision!=='JA'&&$titles)throw new RuntimeException('PSTE_MINI_NON_JA_HAS_TITLES');
                if($decision==='JA'&&!$titles)throw new RuntimeException('PSTE_MINI_JA_WITHOUT_TITLE');
                $clean=[];
                foreach($titles as $title){
                    if(!is_array($title)||count($title)!==2||!array_key_exists('intent',$title)||!array_key_exists('title',$title)||!is_string($title['intent'])||!is_string($title['title']))
                        throw new RuntimeException('PSTE_MINI_TITLE_SHAPE_INVALID');
                    $intent=trim($title['intent']);$text=trim($title['title']);
                    // Only transport format, not a second linguistic/SEO/title decision.
                    if($intent===''||$text===''||strlen($intent)>240||strlen($text)>300||
                        preg_match('/[<>\x00-\x1f\x7f]/u',$intent.$text))
                        throw new RuntimeException('PSTE_MINI_TITLE_TEXT_INVALID');
                    self::assertOneMainQuestion($text);
                    $clean[]=['intent'=>$intent,'title'=>$text];
                }
                $finished[(string)$frozen['pool_key']]=['raw_query'=>$frozen['raw_query'],
                    'decision'=>$decision,'titles'=>$clean,'batch_id'=>$original['batch_id'],
                    'recorded_utc'=>gmdate('c')];
                $stats[$decision]++;$stats['titles']+=count($clean);
            } catch(RuntimeException $e) {
                $code=(string)$e->getMessage();
                // Source/answer mismatch is isolated; unknown exceptions or broken
                // infrastructure are not silently reclassified as editorial outcomes.
                $itemErrors=['PSTE_MINI_ITEM_INVALID','PSTE_MINI_ITEM_FIELDS_CHANGED',
                    'PSTE_MINI_SOURCE_CHANGED_','PSTE_MINI_DATABASE_SOURCE_CHANGED',
                    'PSTE_MINI_DECISION_REQUIRED','PSTE_MINI_TITLES_INVALID',
                    'PSTE_MINI_NON_JA_HAS_TITLES','PSTE_MINI_JA_WITHOUT_TITLE',
                    'PSTE_MINI_TITLE_SHAPE_INVALID','PSTE_MINI_TITLE_TEXT_INVALID',
                    'PSTE_MINI_TITLE_TWO_MAIN_QUESTIONS'];
                $known=false;
                foreach($itemErrors as $prefix)if(str_starts_with($code,$prefix)){$known=true;break;}
                if(!$known)throw $e;
                $held[]=['pool_key'=>(string)$frozen['pool_key'],
                    'reason_code'=>$code,'next_action'=>'RETRY_SAME_EXTERNAL_OWNER'];
                $stats['clarification']++;
            }
        }
        return ['completed'=>$finished,'clarification'=>$held,'stats'=>$stats];
    }

    /** Replaces only title strings for an already imported batch; everything else stays frozen. */
    public static function validateTitleCorrections(array $completed,array $document): array {
        if(($document['contract']??'')!=='PSTE_MINI_RESULTS_FOR_EDITORIAL_V1')
            throw new RuntimeException('PSTE_MINI_TITLE_REPAIR_WRONG_CONTRACT');
        $rows=$document['items']??null;$original=array_values($completed);
        if(!is_array($rows)||!array_is_list($rows)||count($rows)!==count($original)||
           ($document['count']??null)!==count($original))
            throw new RuntimeException('PSTE_MINI_TITLE_REPAIR_COUNT_CHANGED');
        $new=$completed;$keys=array_keys($completed);$updated=0;
        foreach($rows as $i=>$candidate){
            $saved=$original[$i];
            if(!is_array($candidate)||!array_is_list($candidate['titles']??null))
                throw new RuntimeException('PSTE_MINI_TITLE_REPAIR_SHAPE_INVALID');
            $skeleton=$saved;$proposed=$candidate;
            unset($skeleton['titles'],$proposed['titles']);
            if($skeleton!==$proposed)throw new RuntimeException('PSTE_MINI_TITLE_REPAIR_FROZEN_FIELDS_CHANGED');
            if(count($candidate['titles'])!==count($saved['titles']))
                throw new RuntimeException('PSTE_MINI_TITLE_REPAIR_INTENT_COUNT_CHANGED');
            $repaired=[];
            foreach($candidate['titles'] as $j=>$piece){
                if(!is_array($piece)||array_keys($piece)!==array_keys($saved['titles'][$j])||
                   !is_string($piece['title']??null)||($piece['intent']??null)!==$saved['titles'][$j]['intent'])
                    throw new RuntimeException('PSTE_MINI_TITLE_REPAIR_INTENT_CHANGED');
                $title=trim($piece['title']);
                if($title===''||strlen($title)>300||preg_match('/[<>\x00-\x1f\x7f]/u',$title))
                    throw new RuntimeException('PSTE_MINI_TITLE_REPAIR_TRANSPORT_INVALID');
                self::assertOneMainQuestion($title);
                if($title!==$saved['titles'][$j]['title'])$updated++;
                $repaired[]=['intent'=>$piece['intent'],'title'=>$title];
            }
            $new[$keys[$i]]['titles']=$repaired;
        }
        return ['completed'=>$new,'title_changes'=>$updated];
    }

    public static function importTitleCorrections(): void {
        try {
            PSTE_Auth::assertAdmin('pste_mini_title_repair_import',(string)($_POST['_wpnonce']??''));
            $upload=(array)($_FILES['mini_corrected_titles_json']??[]);$path=(string)($upload['tmp_name']??'');
            if((int)($upload['error']??UPLOAD_ERR_NO_FILE)!==UPLOAD_ERR_OK||$path===''||!is_uploaded_file($path)||
                (int)($upload['size']??0)>5000000)throw new RuntimeException('PSTE_MINI_TITLE_REPAIR_UPLOAD_INVALID');
            $raw=file_get_contents($path);if(!is_string($raw))throw new RuntimeException('PSTE_MINI_TITLE_REPAIR_READ_FAILED');
            $doc=json_decode($raw,true,128,JSON_THROW_ON_ERROR);
            if(!is_array($doc))throw new RuntimeException('PSTE_MINI_TITLE_REPAIR_INVALID');
            $state=self::loadState();
            if(($doc['contract']??'')==='PSTE_MINI_SEO_DECISIONS_V1'){
                $snapshot=self::readParkhausForMini(); // one technical freshness check per entire batch
                $before=$state;
                // An external SEO owner can decide raw source topics BEFORE MINI.
                // Current identity comes from the existing topic_pool, not user-uploaded fields.
                $sourceRows=[];$keys=[];
                foreach((array)$doc['items'] as $entry){
                    if(!is_array($entry))continue;
                    $key=(string)($entry['pool_key']??'');
                    if($key!=='')$keys[$key]=true;
                }
                if($keys){
                    global $wpdb;$table=PSTE_Repository::table('topic_pool');
                    foreach(array_chunk(array_keys($keys),100) as $chunk){
                        $marks=implode(',',array_fill(0,count($chunk),'%s'));
                        $found=$wpdb->get_results($wpdb->prepare("SELECT id,pool_key,payload_json FROM $table WHERE pool_key IN ($marks)",...$chunk),ARRAY_A);
                        if(!is_array($found)||(string)($wpdb->last_error??'')!=='')throw new RuntimeException('PSTE_MINI_SEO_SOURCE_DB_READ_FAILED');
                        foreach($found as $row){
                            $key=(string)($row['pool_key']??'');
                            if(isset($sourceRows[$key]))throw new RuntimeException('PSTE_MINI_SEO_SOURCE_DB_DUPLICATE');
                            $sourceRows[$key]=$row;
                        }
                    }
                }
                // Reuse the EXISTING signed PPM plan reader and slot allocator.
                // One technical allocation, no new semantic SEO review.
                $production=defined('TXE_PLANFREE_KISS_V1') && TXE_PLANFREE_KISS_V1
                    ? [] : (class_exists('PSERC_Production_Reader') ? PSERC_Production_Reader::snapshot() : []);
                $state=self::acceptSingleOwnerSeoDecisions($state,$doc,$snapshot,$sourceRows,$production);
                self::storeSeoDecisionsIfUnchanged($before,$state); // one original WP option, atomic
                wp_safe_redirect(admin_url('admin.php?page=portal-seo-topic-engine-review&pste_mini_seo_imported=1'));exit;
            }
            $result=self::validateTitleCorrections($state['completed'],$doc);
            $state['completed']=$result['completed'];
            $state['last_title_repair']=['changes'=>$result['title_changes'],'recorded_utc'=>gmdate('c')];
            self::storeState($state);
            wp_safe_redirect(admin_url('admin.php?page=portal-seo-topic-engine-review&pste_mini_title_repaired=1'));exit;
        }catch(Throwable $e){self::fail($e);}
    }

    public static function importKeywords(): void {
        try {
            PSTE_Auth::assertAdmin('pste_mini_keyword_import',(string)($_POST['_wpnonce']??''));
            $state=self::loadState();$batch=$state['active'];
            if(!is_array($batch))throw new RuntimeException('PSTE_MINI_NO_ACTIVE_BATCH');
            $upload=(array)($_FILES['mini_result_json']??[]);$path=(string)($upload['tmp_name']??'');
            if((int)($upload['error']??UPLOAD_ERR_NO_FILE)!==UPLOAD_ERR_OK||$path===''||!is_uploaded_file($path)||
                (int)($upload['size']??0)>2500000)throw new RuntimeException('PSTE_MINI_UPLOAD_INVALID');
            $raw=file_get_contents($path);if(!is_string($raw))throw new RuntimeException('PSTE_MINI_UPLOAD_FAILED');
            $result=json_decode($raw,true,128,JSON_THROW_ON_ERROR);
            if(!is_array($result))throw new RuntimeException('PSTE_MINI_RESULT_INVALID');
            global $wpdb;$table=PSTE_Repository::table('topic_pool');
            // Max. 20 kurze SQL-Abfragen statt bis zu 2.000 Einzelabfragen.
            $currentRows=[];
            foreach(array_chunk((array)$batch['items'],100) as $part){
                $ids=array_map(static fn(array $item): int=>(int)$item['id'],$part);
                $placeholders=implode(',',array_fill(0,count($ids),'%d'));
                $sql=$wpdb->prepare("SELECT id,pool_key,payload_json FROM $table WHERE id IN ($placeholders)",...$ids);
                $rows=$wpdb->get_results($sql,ARRAY_A);
                if(!is_array($rows)||(string)($wpdb->last_error??'')!=='')throw new RuntimeException('PSTE_MINI_DATABASE_READ_FAILED');
                foreach($rows as $row){
                    $key=(string)$row['pool_key'];
                    if(isset($currentRows[$key]))throw new RuntimeException('PSTE_MINI_SOURCE_DUPLICATE');
                    $currentRows[$key]=$row;
                }
            }
            $beforeState=$state;
            $checked=self::validateResult($batch,$result,static fn(string $key): ?array=>$currentRows[$key]??null);
            if(!empty($batch['title_only']))foreach($checked['completed'] as $key=>$value){
                $proof=(array)($state['seo_decisions'][$key]??[]);
                $originalItem=null;
                foreach((array)$batch['items'] as $frozen)if(($frozen['pool_key']??'')===$key){$originalItem=$frozen;break;}
                if(!is_array($originalItem)||($proof['box']??'')!=='FREI'
                    ||(string)($proof['approved_title']??'')!==''
                    ||!hash_equals((string)($proof['intent_slot']??''),(string)($originalItem['intent_slot']??''))
                    ||!hash_equals((string)($proof['snapshot_sha256']??''),(string)($originalItem['seo_snapshot_sha256']??''))
                    ||!hash_equals((string)($proof['intent_summary']??''),(string)($originalItem['titles'][0]['intent']??''))
                    ||!hash_equals((string)($proof['canonical_article_id']??''),(string)($originalItem['canonical_article_id']??''))
                    ||!hash_equals((string)($proof['plan_slot']??''),(string)($originalItem['plan_slot']??''))
                    ||!hash_equals((string)($proof['article_type']??''),(string)($originalItem['article_type']??''))
                    ||!hash_equals((string)($proof['category_slug']??''),(string)($originalItem['category_slug']??''))
                    ||(string)($proof['raw_query']??'')!==(string)($value['raw_query']??''))
                    throw new RuntimeException('PSTE_MINI_TITLE_OWNER_RECEIPT_CHANGED');
                // Fill only the title on the same already approved receipt, never decide SEO again.
                $state['seo_decisions'][$key]['approved_title']=(string)$value['titles'][0]['title'];
            }
            foreach($checked['completed'] as $key=>$value){
                if(isset($state['completed'][$key]))throw new RuntimeException('PSTE_MINI_KEY_ALREADY_COMPLETED');
                $state['completed'][$key]=$value;
                unset($state['clarification'][$key]);
            }
            foreach($checked['clarification'] as $entry){
                $key=(string)($entry['pool_key']??'');
                if($key!=='')$state['clarification'][$key]=$entry;
            }
            $state['active']=null; // Clarification topics remain exportable: only completed is excluded.
            $state['last_report']=['keywords'=>count($checked['completed']),
                'clarification'=>count($checked['clarification']),
                'titles'=>(int)$checked['stats']['titles'],
                'breakdown'=>$checked['stats'],'recorded_utc'=>gmdate('c')];
            if(!empty($batch['title_only']))self::storeSeoDecisionsIfUnchanged($beforeState,$state);
            else self::storeState($state); // Historical active batch; no new decision owner.
            // Titles staged only. Existing plan owner not invoked.
            wp_safe_redirect(admin_url('admin.php?page=portal-seo-topic-engine-review&pste_mini_imported=1'));exit;
        } catch(Throwable $e){self::fail($e);}
    }

    /**
     * No second quality or SEO decision. One existing pool row has one language title;
     * extra distinct intent suggestions stay in the MINI result until the existing
     * editorial owner creates a distinct plan identity. Nothing is lost or fanned out.
     * This preflight MUST finish before the first write.
     */
    public static function planHandoffPreflight(array $completed, callable $loadCurrent): array {
        $selected=[];$additional=0;$nonYes=0;
        foreach($completed as $poolKey=>$result){
            if(!is_array($result)||!in_array($result['decision']??null,['JA','NEIN','VIELLEICHT'],true))
                throw new RuntimeException('PSTE_MINI_PLAN_DECISION_MISSING');
            if($result['decision']!=='JA'){$nonYes++;continue;}
            if(!is_array($result['titles']??null)||!array_is_list($result['titles'])||!$result['titles'])
                throw new RuntimeException('PSTE_MINI_PLAN_TITLE_MISSING');
            $row=$loadCurrent((string)$poolKey);
            if(!is_array($row)||(string)($row['pool_key']??'')!==(string)$poolKey)
                throw new RuntimeException('PSTE_MINI_PLAN_SOURCE_MISSING');
            $payload=json_decode((string)($row['payload_json']??''),true);
            $raw=is_array($payload)?PSTE_Editorializer::sourceQuery($payload):'';
            if($raw===''||!hash_equals((string)($result['raw_query']??''),$raw))
                throw new RuntimeException('PSTE_MINI_PLAN_RAW_QUERY_CHANGED');
            $first=$result['titles'][0];
            if(!is_array($first)||!is_string($first['title']??null)||trim($first['title'])===''||
               preg_match('/[<>\x00-\x1f\x7f]/u',(string)$first['title']))
                throw new RuntimeException('PSTE_MINI_PLAN_TRANSPORT_INVALID');
            $selected[]=['pool_key'=>(string)$poolKey,'raw_query'=>$raw,
                'title'=>(string)$first['title'],
                'batch_id'=>(string)($result['batch_id']??''),
                'source_hash'=>hash('sha256',$raw.'|'.(string)$first['title'])];
            $additional+=count($result['titles'])-1;
        }
        if(!$selected)throw new RuntimeException('PSTE_MINI_PLAN_NO_YES_TITLES');
        return ['selected'=>$selected,'additional'=>$additional,'not_yes'=>$nonYes];
    }

    /**
     * A plugin version change does NOT change an already approved SEO/title
     * decision. This is a transport checkpoint, not a second opinion.
     * Accept the older source-hash|plugin-version checkpoint without replaying.
     */
    private static function titleAlreadyQueued(array $queued,string $key,string $sourceHash): bool {
        $stamp=(string)($queued[$key]??'');
        if(!preg_match('/^[a-f0-9]{64}(?:\|[0-9.]+)?$/D',$stamp))return false;
        return hash_equals(substr($stamp,0,64),$sourceHash);
    }

    /** Hand-off to EXISTING PSTE title-storage and its ONE category/SEO owner. */
    public static function forwardToPlan(): void {
        try {
            PSTE_Auth::assertAdmin('pste_mini_forward_to_plan',(string)($_POST['_wpnonce']??''));
            if(!class_exists('PSTE_Admin')||!class_exists('PSTE_Repository'))
                throw new RuntimeException('PSTE_MINI_PLAN_OWNER_MISSING');
            $state=self::loadState();
            if(is_array($state['active'])||!$state['completed'])
                throw new RuntimeException('PSTE_MINI_PLAN_UNFINISHED_BATCH');
            global $wpdb;
            $table=PSTE_Repository::table('topic_pool');
            $keys=array_keys($state['completed']);$current=[];
            foreach(array_chunk($keys,100) as $part){
                $placeholder=implode(',',array_fill(0,count($part),'%s'));
                $rows=$wpdb->get_results($wpdb->prepare(
                    "SELECT pool_key,payload_json FROM $table WHERE pool_key IN ($placeholder)",...$part),ARRAY_A);
                if(!is_array($rows)||(string)($wpdb->last_error??'')!=='')
                    throw new RuntimeException('PSTE_MINI_PLAN_DATABASE_READ_FAILED');
                foreach($rows as $row){
                    $key=(string)($row['pool_key']??'');
                    if($key===''||isset($current[$key]))throw new RuntimeException('PSTE_MINI_PLAN_SOURCE_DUPLICATE');
                    $current[$key]=$row;
                }
            }
            // Transport only: BELEGT/KLAERUNG have no article claim.
            $eligible=[];
            foreach((array)$state['completed'] as $key=>$topic){
                $proof=self::singleOwnerSeoFor((string)$key,(string)($topic['raw_query']??''));
                if(($proof['box']??'')!=='FREI')continue;
                $eligible[$key]=$topic;
            }
            $parkhaus=self::readParkhausForMini();
            $ready=[];$technicalHeld=[];
            foreach($eligible as $key=>$topic){
                $receipt=self::singleOwnerSeoFor((string)$key,(string)($topic['raw_query']??''));
                if(empty($parkhaus['complete'])||!hash_equals(
                    (string)($parkhaus['sha256']??''),
                    (string)($receipt['snapshot_sha256']??''))){
                    $technicalHeld[]=['pool_key'=>(string)$key,
                        'reason_code'=>'PSTE_MINI_PARKHAUS_CHANGED_SINCE_ONE_SEO_DECISION'];
                    $state['clarification'][$key]=[
                        'pool_key'=>(string)$key,'reason_code'=>'PSTE_MINI_PARKHAUS_CHANGED',
                        'next_action'=>'SAME_EXTERNAL_SEO_OWNER_NEW_SNAPSHOT'];
                    continue;
                }
                // Existing technical preflight only; failure of one topic
                // never takes down the whole import batch.
                try {
                    $part=self::planHandoffPreflight([$key=>$topic],
                        static fn(string $id): ?array=>$current[$id]??null);
                    foreach($part['selected'] as $entry)$ready[]=$entry;
                }catch(Throwable $e){
                    $code=substr((string)$e->getMessage(),0,160);
                    $technicalHeld[]=['pool_key'=>(string)$key,'reason_code'=>$code];
                    $state['clarification'][$key]=[
                        'pool_key'=>(string)$key,'reason_code'=>$code,
                        'next_action'=>'RETRY_EXISTING_TECHNICAL_HANDOFF'];
                }
            }
            $pre=['selected'=>$ready,'additional'=>0,'not_yes'=>0];
            if(!$ready){
                $state['last_plan_report']=['forwarded'=>0,'blocked'=>count($technicalHeld),
                    'held'=>$technicalHeld,'additional'=>0,'not_yes'=>0,
                    'scheduled'=>0,'recorded_utc'=>gmdate('c'),
                    'production_approval'=>false];
                self::storeState($state);
                wp_safe_redirect(admin_url('admin.php?page=portal-seo-topic-engine-review&pste_mini_to_plan=0'));exit;
            }
            $previous=is_array($state['plan_forwarded']??null)?$state['plan_forwarded']:[];
            $queued=is_array($state['plan_queued']??null)?$state['plan_queued']:[];
            $toQueue=[];$forwarded=0;$blocked=[];
            foreach($pre['selected'] as $item){
                $key=$item['pool_key'];
                try {
                    // The language desk writes only its title. The current MINI JA is read
                    // directly from the original completed decision by the relevance owner.
                    $out=PSTE_Repository::saveManualTitleOverride($key,$item['title'],get_current_user_id());
                    if(($out['contract']??'')!=='PSTE_MANUAL_TITLE_OVERRIDE_RESULT_V1'||($out['status']??'')!=='PASS')
                        throw new RuntimeException('PSTE_MINI_PLAN_TITLE_WRITE_NOT_CONFIRMED');
                    if(($previous[$key]??'')!==$item['source_hash']){
                        $previous[$key]=$item['source_hash'];
                        $state['plan_forwarded']=$previous;
                        self::storeState($state); // checkpoint BEFORE queuing; retry resumes
                        $forwarded++;
                    }
                    // No hidden re-evaluation merely because the plugin was updated.
                    // A fresh owner run requires a new title hash or the explicit,
                    // preflight-proven context-rebind worker, never PSTE_VERSION.
                    if(!self::titleAlreadyQueued($queued,$key,$item['source_hash']))
                        $toQueue[$key]=$item['source_hash'];
                }catch(Throwable $e){$blocked[]=['pool_key'=>$key,
                    'reason_code'=>substr((string)preg_replace('/[^A-Z0-9_:\-]/i','_',strtoupper($e->getMessage())),0,140)];}
            }
            $scheduled=0;
            if($toQueue){
                $scheduled=PSTE_Admin::scheduleTitleDeskReentry(array_keys($toQueue),true);
                if($scheduled<=0)throw new RuntimeException('PSTE_MINI_PLAN_REENTRY_NOT_QUEUED');
                foreach($toQueue as $key=>$hash)$queued[$key]=$hash;
                $state['plan_queued']=$queued;
                self::storeState($state);
            }
            $state['last_plan_report']=['forwarded'=>$forwarded,'blocked'=>count($blocked),
                'held'=>$blocked,'additional'=>$pre['additional'],
                'not_yes'=>$pre['not_yes'],'scheduled'=>$scheduled,
                'recorded_utc'=>gmdate('c'),'production_approval'=>false];
            self::storeState($state);
            if($scheduled)PSTE_Admin::processTitleDeskReentry();
            wp_safe_redirect(admin_url('admin.php?page=portal-seo-topic-engine-review&pste_mini_to_plan=1'));exit;
        }catch(Throwable $e){self::fail($e);}
    }

    /**
     * READ-ONLY parkhouse source from the already-existing PSERC plan snapshot.
     * No new semantic gate and no compiler invocation. Include READY and HELD
     * records, so a held intended article cannot silently disappear from inventory.
     */
    public static function readExistingPsercPlanForParkhaus(): array {
        $empty=['complete'=>false,'source'=>'PSERC_EXISTING_ACTIVE_PLAN','items'=>[],
            'generation'=>'','snapshot_sha256'=>'','reason'=>'PSERC_ACTIVE_PLAN_NOT_AVAILABLE'];
        if(!class_exists('PSERC_Plan_Snapshot_Store')
            ||!class_exists('PSERC_Plan_Dependency_Fingerprint'))return $empty;
        $head=PSERC_Plan_Snapshot_Store::getActive();
        if(!is_array($head)||!PSERC_Plan_Snapshot_Store::verifyHeader($head)
            ||!PSERC_Plan_Dependency_Fingerprint::isCurrent((array)($head['dependency']??[]))){
            $empty['reason']='PSERC_ACTIVE_PLAN_INCOMPLETE_OR_STALE';
            return $empty;
        }
        $generation=(string)($head['generation']??'');
        $count=$head['counts']['compiled_items']??null;
        if(!preg_match('/^[a-f0-9]{20}$/D',$generation)
            ||!is_int($count)||$count<0||$count>100000){
            $empty['reason']='PSERC_ACTIVE_PLAN_INVALID_GENERATION_OR_COUNT';
            return $empty;
        }
        $items=[];
        for($i=0;$i<$count;$i++){
            $row=PSERC_Plan_Snapshot_Store::getRecord($generation,'final_item',$i);
            if(!is_array($row)||($row['status']??'')===''){
                $empty['reason']='PSERC_ACTIVE_PLAN_RECORD_MISSING';
                return $empty;
            }
            $title=trim((string)($row['title']['production_title']??''));
            $keyword=trim((string)($row['target_keyword']['value']??''));
            $identity=trim((string)($row['seo_topic_id']??''));
            // An unfinished article title remains a valid *occupied or uncertain*
            // planning record; never hide it merely because the title is blank.
            $items[]=[
                'source'=>'PSERC_ACTIVE_PLAN','record_index'=>$i,'seo_topic_id'=>$identity,
                'title'=>$title,'target_keyword'=>$keyword,
                'article_type'=>(string)($row['article_type']??''),
                'category_slug'=>(string)($row['category']['slug']??''),
                'status'=>(string)$row['status'],
                'canonical_article_id'=>(string)($row['canonical_slot']['canonical_article_id']??''),
                'plan_slot'=>(string)($row['canonical_slot']['plan_slot_sha256']??''),
                'intent_profile'=>(array)($row['intent_profile']??[]),
            ];
        }
        $again=PSERC_Plan_Snapshot_Store::getActive();
        if(!PSERC_Plan_Snapshot_Store::verifyHeader((array)$again)
           ||!hash_equals((string)($head['snapshot_sha256']??''),
               (string)($again['snapshot_sha256']??''))
           ||!PSERC_Plan_Dependency_Fingerprint::isCurrent((array)($again['dependency']??[]))){
            $empty['reason']='PSERC_ACTIVE_PLAN_CHANGED_WHILE_READING';
            return $empty;
        }
        return ['complete'=>true,'source'=>'PSERC_EXISTING_ACTIVE_PLAN',
            'generation'=>$generation,
            'snapshot_sha256'=>(string)$head['snapshot_sha256'],
            'item_count'=>count($items),'items'=>$items,'reason'=>''];
    }

    /**
     * SINGLE read-only parkhouse export for the existing MINI batch.
     * Collects data, never performs or re-performs an SEO/intent decision.
     * Fail closed: missing WP, PSTE, editorial-plan or PSERC data never becomes FREI.
     */
    public static function readParkhausForMini(): array {
        $result=['contract'=>'PSTE_MINI_PARKHAUS_SNAPSHOT_V1','complete'=>false,
            'created_at_utc'=>gmdate('c'),'items'=>[],'sources'=>[],
            'sha256'=>'','reason'=>'PORTAL_INVENTORY_INCOMPLETE'];
        try {
            global $wpdb;
            if(!isset($wpdb)||!is_object($wpdb)||!method_exists($wpdb,'prepare')
                ||!method_exists($wpdb,'get_results')||!method_exists($wpdb,'get_var')
                ||!function_exists('get_post_types'))
                throw new RuntimeException('WP_READ_API_MISSING');
            $types=array_values(array_unique(array_filter(array_merge(['post','page'],
                array_values((array)get_post_types(['public'=>true],'names')),
                array_values((array)get_post_types(['publicly_queryable'=>true],'names'))),
                static fn($x)=>is_string($x)&&$x!==''&&$x!=='attachment')));
            sort($types,SORT_STRING);
            if(!$types)throw new RuntimeException('WP_PUBLIC_TYPES_MISSING');
            $states=['publish','draft','future','pending','private'];
            $placeholderTypes=implode(',',array_fill(0,count($types),'%s'));
            $placeholderStates=implode(',',array_fill(0,count($states),'%s'));
            $criteria="post_type IN ($placeholderTypes) AND post_status IN ($placeholderStates)";
            $params=array_merge($types,$states);
            $countSql=$wpdb->prepare("SELECT COUNT(*) FROM {$wpdb->posts} WHERE ".$criteria,...$params);
            $before=(int)$wpdb->get_var($countSql);
            if((string)($wpdb->last_error??'')!=='')throw new RuntimeException('WP_COUNT_FAILED');
            $items=[];$cursor=0;
            while(true){
                $pageSql=$wpdb->prepare(
                    "SELECT ID,post_title,post_type,post_status,post_name,post_content,post_modified_gmt ".
                    "FROM {$wpdb->posts} WHERE ID>%d AND ".$criteria." ORDER BY ID ASC LIMIT 200",
                    $cursor,...$params);
                $rows=$wpdb->get_results($pageSql,defined('ARRAY_A')?ARRAY_A:'ARRAY_A');
                if(!is_array($rows)||(string)($wpdb->last_error??'')!=='')throw new RuntimeException('WP_PAGE_READ_FAILED');
                if(!$rows)break;
                $ids=[];$index=[];
                foreach($rows as $row){
                    if(!is_array($row))$row=(array)$row;
                    $id=(int)($row['ID']??0);
                    if($id<=$cursor)throw new RuntimeException('WP_CURSOR_INVALID');
                    $cursor=$id;$ids[]=$id;
                    $content=(string)($row['post_content']??'');
                    preg_match_all('/<h[1-6][^>]*>(.*?)<\/h[1-6]>/isu',$content,$match);
                    $headings=array_values(array_map(static fn($h)=>trim(wp_strip_all_tags($h)),
                        (array)($match[1]??[])));
                    $items[]=['source'=>'WORDPRESS','id'=>$id,'title'=>(string)($row['post_title']??''),
                        'type'=>(string)($row['post_type']??''),'status'=>(string)($row['post_status']??''),
                        'slug'=>(string)($row['post_name']??''),'modified_gmt'=>(string)($row['post_modified_gmt']??''),
                        'headings'=>$headings,'content_sha256'=>hash('sha256',$content),
                        'target_keyword'=>'','canonical_article_id'=>'','plan_slot'=>'','categories'=>[]];
                    $index[$id]=count($items)-1;
                }
                $idList=implode(',',array_map('intval',$ids));
                $meta=$wpdb->get_results("SELECT post_id,meta_key,meta_value FROM {$wpdb->postmeta} ".
                    "WHERE meta_key IN ('_yoast_wpseo_focuskw','_ppm679_canonical_article_id','_ppm679_plan_slot_sha256') ".
                    "AND post_id IN ($idList) ORDER BY post_id ASC",
                    defined('ARRAY_A')?ARRAY_A:'ARRAY_A');
                if(!is_array($meta)||(string)($wpdb->last_error??'')!=='')throw new RuntimeException('WP_SEO_META_READ_FAILED');
                foreach($meta as $row){if(!is_array($row))$row=(array)$row;$id=(int)($row['post_id']??0);
                    if(!isset($index[$id]))continue;
                    $metaKey=(string)($row['meta_key']??'');
                    if($metaKey==='_yoast_wpseo_focuskw')$items[$index[$id]]['target_keyword']=(string)($row['meta_value']??'');
                    elseif($metaKey==='_ppm679_canonical_article_id')$items[$index[$id]]['canonical_article_id']=(string)($row['meta_value']??'');
                    elseif($metaKey==='_ppm679_plan_slot_sha256')$items[$index[$id]]['plan_slot']=(string)($row['meta_value']??'');}
                $categories=$wpdb->get_results(
                    "SELECT tr.object_id AS post_id,tt.term_id AS category_id,t.name AS category_name ".
                    "FROM {$wpdb->term_relationships} tr ".
                    "INNER JOIN {$wpdb->term_taxonomy} tt ON tt.term_taxonomy_id=tr.term_taxonomy_id ".
                    "INNER JOIN {$wpdb->terms} t ON t.term_id=tt.term_id ".
                    "WHERE tt.taxonomy='category' AND tr.object_id IN ($idList) ORDER BY tr.object_id,tt.term_id",
                    defined('ARRAY_A')?ARRAY_A:'ARRAY_A');
                if(!is_array($categories)||(string)($wpdb->last_error??'')!=='')
                    throw new RuntimeException('WP_CATEGORY_READ_FAILED');
                foreach($categories as $row){if(!is_array($row))$row=(array)$row;$id=(int)($row['post_id']??0);
                    if(isset($index[$id]))$items[$index[$id]]['categories'][]=[
                        'id'=>(int)($row['category_id']??0),'name'=>(string)($row['category_name']??'')];}
            }
            $after=(int)$wpdb->get_var($countSql);
            if((string)($wpdb->last_error??'')!==''||$before!==$after||count($items)!==$before)
                throw new RuntimeException('WP_INVENTORY_CHANGED_DURING_SCAN');
            $result['sources']['WORDPRESS']=['complete'=>true,'item_count'=>count($items),
                'post_types'=>$types,'statuses'=>$states];
            // Reuse this already-read inventory for the existing PPM679 slot linkage.
            $wordpressById=[];
            $wordpressByCanonical=[];
            foreach($items as $wpRow){
                $wordpressById[(int)$wpRow['id']]=$wpRow;
                $id=trim((string)($wpRow['canonical_article_id']??''));
                if($id!=='')$wordpressByCanonical[$id][]=$wpRow;
            }
            // Record every duplicate WP metadata identity. A legacy stray
            // canonical tag is not a second existing editorial plan slot, but
            // it must be visible for a one-time source-side metadata repair.
            $canonicalCollisions=[];
            foreach($wordpressByCanonical as $identity=>$matches){
                if(count($matches)<2)continue;
                $canonicalCollisions[]=['canonical_article_id'=>$identity,
                    'post_ids'=>array_values(array_map(static fn($x)=>(int)$x['id'],$matches)),
                    'plan_slots'=>array_values(array_map(static fn($x)=>(string)($x['plan_slot']??''),$matches))];
            }
            $result['sources']['WORDPRESS']['canonical_collision_count']=count($canonicalCollisions);
            $result['sources']['WORDPRESS']['canonical_collisions']=$canonicalCollisions;
            $result['items']=$items;

            $pool=PSTE_Repository::table('topic_pool');
            $planCountSql="SELECT COUNT(*) FROM $pool WHERE planning_suitability IN ('YES','PROVISIONAL')";
            $planBefore=(int)$wpdb->get_var($planCountSql);
            if((string)($wpdb->last_error??'')!=='')throw new RuntimeException('PSTE_PLAN_COUNT_FAILED');
            $psteCount=0;$last=0;
            while(true){
                $q=$wpdb->prepare("SELECT id,pool_key,candidate_id,payload_json,planning_suitability,automatic_pool_status ".
                    "FROM $pool WHERE id>%d AND planning_suitability IN ('YES','PROVISIONAL') ".
                    "ORDER BY id ASC LIMIT 200",$last);
                $rows=$wpdb->get_results($q,defined('ARRAY_A')?ARRAY_A:'ARRAY_A');
                if(!is_array($rows)||(string)($wpdb->last_error??'')!=='')throw new RuntimeException('PSTE_PLAN_READ_FAILED');
                if(!$rows)break;
                foreach($rows as $row){if(!is_array($row))$row=(array)$row;
                    $id=(int)($row['id']??0);if($id<=$last)throw new RuntimeException('PSTE_PLAN_CURSOR_INVALID');$last=$id;
                    $data=json_decode((string)($row['payload_json']??''),true);
                    if(!is_array($data))throw new RuntimeException('PSTE_PLAN_INVALID_JSON');
                    $result['items'][]=['source'=>'PSTE_PLAN','pool_key'=>(string)($row['pool_key']??''),
                        'seo_topic_id'=>(string)($row['candidate_id']??$data['candidate_id']??''),
                        'raw_query'=>PSTE_Editorializer::sourceQuery($data),
                        'title'=>(string)($data['production_title']??$data['editorial_title']??''),
                        'target_keyword'=>(string)($data['target_keyword']??''),
                        'category'=>(string)($data['target_category_name']??''),
                        'article_type'=>(string)($data['proposed_article_type']??''),
                        'planning_suitability'=>(string)($row['planning_suitability']??''),
                        'status'=>(string)($row['automatic_pool_status']??''),
                        'plan_slot'=>(string)($data['plan_slot']??''),
                        'intent_profile'=>(array)($data['intent_profile']??[])];
                    $psteCount++;
                }
            }
            $planAfter=(int)$wpdb->get_var($planCountSql);
            if((string)($wpdb->last_error??'')!==''||$planBefore!==$planAfter||$psteCount!==$planBefore)
                throw new RuntimeException('PSTE_PLAN_CHANGED_DURING_SCAN');
            $result['sources']['PSTE_PLAN']=['complete'=>true,'item_count'=>$psteCount];

            // Even corrupt historical editorial rows belong in the single
            // read-only export. Missing titles must not hide PSERC/PPM679 plans.
            $sourceProblems=[];
            $editorial=PSTE_Snapshot::editorialPlanForParkhaus();
            $editorialUnknown=(int)($editorial['unresolved_count']??0);
            $editorialConflict=!empty($editorial['source_conflict']);
            $result['sources']['EDITORIAL_PLAN']=[
                'complete'=>$editorialUnknown===0&&!$editorialConflict,
                'status'=>(string)($editorial['status']??'NOT_AVAILABLE'),
                'sha256'=>(string)($editorial['sha256']??'NOT_AVAILABLE'),
                'item_count'=>count((array)($editorial['items']??[])),
                'unresolved_count'=>$editorialUnknown,
                'unresolved_indices'=>(array)($editorial['unresolved_indices']??[]),
                'legacy_empty_count'=>(int)($editorial['legacy_empty_count']??0),
                'legacy_empty_indices'=>(array)($editorial['legacy_empty_indices']??[]),
                'source_origin'=>(string)($editorial['source_origin']??'NONE'),
                'source_conflict'=>$editorialConflict,
                'filter_sha256'=>(string)($editorial['filter_sha256']??''),
                'option_sha256'=>(string)($editorial['option_sha256']??''),
                'filter_item_count'=>(int)($editorial['filter_item_count']??0),
                'option_item_count'=>(int)($editorial['option_item_count']??0)];
            foreach((array)($editorial['items']??[]) as $row){
                if(!is_array($row))throw new RuntimeException('EDITORIAL_PLAN_ROW_NOT_ARRAY');
                if(in_array(($row['status']??''),['UNRESOLVED_SOURCE_TITLE','LEGACY_EMPTY_PLACEHOLDER'],true)){
                    $result['items'][]=array_merge(['source'=>'EDITORIAL_PLAN'], $row);
                    continue;
                }
                if(!is_string($row['title']??null)
                    ||trim($row['title'])===''||trim($row['title'])==='Array')
                    throw new RuntimeException('EDITORIAL_PLAN_ROW_INCONSISTENT');
                $result['items'][]=['source'=>'EDITORIAL_PLAN','status'=>(string)($row['status']??'PLANNED'),
                    'title'=>$row['title'],'target_keyword'=>(string)($row['target_keyword']??''),
                    'plan_slot'=>(string)($row['plan_slot']??''),'article_type'=>(string)($row['article_type']??''),
                    'category'=>(string)($row['category_name']??'')];
            }
            if($editorialUnknown>0)$sourceProblems[]='EDITORIAL_PLAN_UNRESOLVED:'.$editorialUnknown;
            if($editorialConflict)$sourceProblems[]='EDITORIAL_PLAN_SOURCE_CONFLICT';

            // This legacy plan is read ONLY when it already exists; it is not created for new articles.
            $planFree=defined('TXE_PLANFREE_KISS_V1') && TXE_PLANFREE_KISS_V1;
            $historicalPlan=$planFree && class_exists('PSERC_Plan_Snapshot_Store')
                ?get_option(PSERC_Plan_Snapshot_Store::ACTIVE_OPTION, null):null;
            if($planFree && ($historicalPlan===null || $historicalPlan===false)){
                $result['sources']['PSERC_ACTIVE_PLAN']=['complete'=>true,
                    'status'=>'NO_HISTORICAL_PLAN_REQUIRED','item_count'=>0];
            }else{
                $pserc=self::readExistingPsercPlanForParkhaus();
                $result['sources']['PSERC_ACTIVE_PLAN']=[
                    'complete'=>!empty($pserc['complete']),'reason'=>(string)($pserc['reason']??''),
                    'snapshot_sha256'=>(string)($pserc['snapshot_sha256']??''),
                    'item_count'=>(int)($pserc['item_count']??0)];
                foreach((array)($pserc['items']??[]) as $item)if(is_array($item))$result['items'][]=$item;
                if(empty($pserc['complete']))throw new RuntimeException('PSERC_PLAN_NOT_PROVEN_COMPLETE');
            }

            // The PPM679 runtime Redaktionsplan is ALREADY in WordPress. Read
            // only its occupied canonical IDs, never write or create a second plan.
            // PSERC_Slot_Allocator::occupiedCanonicalIds() uses this SAME option.
            $runtimeOriginal=get_option('ppm679_editorial_plan_runtime_state_v1',null);
            if($planFree && ($runtimeOriginal===null || $runtimeOriginal===false)){
                $result['sources']['PPM679_EXISTING_EDITORIAL_RUNTIME']=[
                    'complete'=>true,'status'=>'NO_HISTORICAL_PLAN_REQUIRED','item_count'=>0];
            }else{
    
                // Source completeness belongs HERE, once per full parkhouse export.
                // Missing/empty saved PPM679 plan cannot mean "all article slots free".
                if(!is_array($runtimeOriginal)||!is_array($runtimeOriginal['items']??null))
                    throw new RuntimeException('EXISTING_RUNTIME_EDITORIAL_PLAN_MISSING_OR_INVALID');
                $runtimeItems=$runtimeOriginal['items'];
                if(!$runtimeItems)
                    throw new RuntimeException('EXISTING_RUNTIME_EDITORIAL_PLAN_EMPTY');
                $runtimeMissingTitles=[];$historicalOrphans=[];$migratedPostIds=[];
                $seenCanonicals=[];$seenSlots=[];
                foreach($runtimeItems as $itemId=>$item){
                    if(!is_array($item))throw new RuntimeException('EXISTING_RUNTIME_EDITORIAL_PLAN_ITEM_INVALID');
                    $canonical=trim((string)($item['canonical_article_id']??$itemId));
                    if($canonical==='')throw new RuntimeException('EXISTING_RUNTIME_EDITORIAL_PLAN_SLOT_ID_MISSING');
                    $slot=trim((string)($item['plan_slot_sha256']??$item['plan_slot']??''));
                    if(isset($seenCanonicals[$canonical]))throw new RuntimeException('EXISTING_RUNTIME_DUPLICATE_CANONICAL');
                    $seenCanonicals[$canonical]=true;
                    if(!preg_match('/^[a-f0-9]{64}$/D',$slot))
                        throw new RuntimeException('EXISTING_RUNTIME_INVALID_PLAN_SLOT');
                    if(isset($seenSlots[$slot]))throw new RuntimeException('EXISTING_RUNTIME_DUPLICATE_PLAN_SLOT');
                    $seenSlots[$slot]=true;
                    $postId=(int)($item['post_id']??0);
                    $wpRow=$wordpressById[$postId]??null;
                    $matchingCanonical=(array)($wordpressByCanonical[$canonical]??[]);
                    $matchingIdentityAndSlot=array_values(array_filter($matchingCanonical,
                        static fn($x)=>(string)($x['plan_slot']??'')===$slot));
                    // A reused post ID with a DIFFERENT recorded identity must not
                    // lend its unrelated title to an older reservation.
                    $directIdentityMismatch=is_array($wpRow)
                        &&trim((string)($wpRow['canonical_article_id']??''))!==''
                        &&trim((string)$wpRow['canonical_article_id'])!==$canonical;
                    if($directIdentityMismatch)$wpRow=null;
                    // Canonical alias pollution exists in the ACTUAL user's WP
                    // metadata: two unrelated posts share one canonical, but only
                    // one possesses the matching plan slot. That exact slot owns
                    // the plan identity; the other post remains a separate WP
                    // article and is reported as an alias collision.
                    $directSlotConflict=is_array($wpRow)
                        &&trim((string)($wpRow['plan_slot']??''))!==''
                        &&(string)$wpRow['plan_slot']!==$slot;
                    $migrationSlotConflict=!is_array($wpRow)&&count($matchingCanonical)>0
                        &&count($matchingIdentityAndSlot)!==1;
                    $identityConflict=$directIdentityMismatch||$directSlotConflict
                        ||count($matchingIdentityAndSlot)>1||$migrationSlotConflict;
                    $relinkedPostId=0;
                    // Search the already-scanned WP inventory by BOTH immutable
                    // identity and slot; never match by title or canonical alone.
                    if(!is_array($wpRow)&&!$identityConflict&&count($matchingIdentityAndSlot)===1){
                        $wpRow=$matchingIdentityAndSlot[0];
                        $relinkedPostId=(int)($wpRow['id']??0);
                        $migratedPostIds[]=$postId;
                    }
                    $postLookupAttempted=false;$postConfirmedMissing=false;
                    if($postId>0&&!is_array($wpRow)&&!$identityConflict&&function_exists('get_post')){
                        $postLookupAttempted=true;$post=get_post($postId);
                        $postConfirmedMissing=!is_object($post);
                        if(is_object($post)&&isset($post->ID))
                            $wpRow=['id'=>(int)$post->ID,'title'=>(string)($post->post_title??''),
                                'status'=>(string)($post->post_status??''),'target_keyword'=>'','categories'=>[]];
                    }
                    $storedTitleValue=$item['title']??null;
                    $ambiguousStoredTitle=is_array($storedTitleValue)&&$storedTitleValue!==[]
                        &&PSTE_Snapshot::editorialSafeText($storedTitleValue)==='';
                    $runtimeTitle=PSTE_Snapshot::editorialSafeText($storedTitleValue);
                    $title=$runtimeTitle!==''&&$runtimeTitle!=='Array'?$runtimeTitle:
                        (is_array($wpRow)?trim((string)($wpRow['title']??'')):'');
                    $titleUnresolved=$identityConflict||$title===''||$title==='Array';
                    $historicalOrphan=$titleUnresolved&&!$ambiguousStoredTitle&&$postId>0&&$postLookupAttempted
                        &&$postConfirmedMissing&&!$identityConflict&&count($matchingCanonical)===0
                        &&$slot!==''&&(string)($item['status']??'')==='DRAFT_CREATED_READBACK_PASS'
                        &&trim((string)($item['target_keyword']??''))===''
                        &&trim((string)($item['category_slug']??''))===''
                        &&trim((string)($item['article_type']??''))==='';
                    if($titleUnresolved){
                        $title='';
                        if($historicalOrphan)$historicalOrphans[]=$postId;
                        else $runtimeMissingTitles[]=$postId;
                    }
                    $targetKeyword=is_string($item['target_keyword']??null)?trim($item['target_keyword']):'';
                    if($targetKeyword===''&&is_array($wpRow))$targetKeyword=(string)($wpRow['target_keyword']??'');
                    $category=trim((string)($item['category_slug']??''));
                    $wpCategories=is_array($wpRow)?(array)($wpRow['categories']??[]):[];
                    $result['items'][]=['source'=>'PPM679_EXISTING_EDITORIAL_RUNTIME',
                        'canonical_article_id'=>$canonical,
                        'plan_slot'=>$slot,
                        'post_id'=>$postId,
                        'resolved_post_id'=>$relinkedPostId>0?$relinkedPostId:$postId,
                        'post_link_status'=>$historicalOrphan?'HISTORICAL_POST_MISSING_SLOT_STILL_RESERVED':($relinkedPostId>0?'RELINKED_BY_EXACT_CANONICAL_AND_SLOT':(count($matchingCanonical)>1?'EXACT_SLOT_OWNER_WITH_DUPLICATE_CANONICAL_ALIAS':'UNCHANGED')),
                        'technical_reservation'=>true,
                        'semantic_occupancy'=>$historicalOrphan?'NONE':($titleUnresolved?'UNKNOWN':'PRESENT'),
                        'post_status'=>is_array($wpRow)?(string)($wpRow['status']??''):'',
                        'status'=>(string)($item['status']??'PLANNED'),
                        'category'=>$category,
                        'categories'=>$wpCategories,
                        'article_type'=>(string)($item['article_type']??''),
                        'target_keyword'=>$targetKeyword,
                        'title'=>$title,
                        'title_status'=>$historicalOrphan?'HISTORICAL_ORPHAN_RESERVATION':($titleUnresolved?'UNRESOLVED_SOURCE_TITLE':'RESOLVED')];
                }
                $runtimeAfter=get_option('ppm679_editorial_plan_runtime_state_v1',null);
                $beforeRuntime=wp_json_encode($runtimeOriginal,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);
                $afterRuntime=wp_json_encode($runtimeAfter,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);
                if(!is_string($beforeRuntime)||!is_string($afterRuntime)
                    ||!hash_equals(hash('sha256',$beforeRuntime),hash('sha256',$afterRuntime)))
                    throw new RuntimeException('EXISTING_RUNTIME_EDITORIAL_PLAN_CHANGED_DURING_SCAN');
                $result['sources']['PPM679_EXISTING_EDITORIAL_RUNTIME']=[
                    'complete'=>count($runtimeMissingTitles)===0,
                    'status'=>$runtimeOriginal===null||$runtimeOriginal===false?'NOT_PRESENT':'PRESENT',
                    'item_count'=>count($runtimeItems),
                    'unresolved_count'=>count($runtimeMissingTitles),
                    'unresolved_post_ids'=>$runtimeMissingTitles,
                    'historical_orphan_count'=>count($historicalOrphans),
                    'historical_orphan_post_ids'=>$historicalOrphans,
                    'migrated_post_count'=>count($migratedPostIds),
                    'migrated_original_post_ids'=>$migratedPostIds,
                    'sha256'=>hash('sha256',$beforeRuntime)];
                if($runtimeMissingTitles)
                    $sourceProblems[]='PPM679_RUNTIME_TITLE_UNRESOLVED:'.count($runtimeMissingTitles);
            }

            // Earlier externally approved slots live in the existing MINI option.
            // Show them to the same owner on later batches; no shadow database.
            $mini=self::loadState();$reservations=0;
            foreach((array)($mini['seo_decisions']??[]) as $key=>$receipt){
                if(!is_array($receipt)||($receipt['box']??'')!=='FREI')continue;
                $result['items'][]=['source'=>'MINI_RESERVED',
                    'pool_key'=>(string)$key,'title'=>(string)($receipt['approved_title']??''),
                    'raw_query'=>(string)($receipt['raw_query']??''),
                    'intent_slot'=>(string)($receipt['intent_slot']??''),
                    'canonical_article_id'=>(string)($receipt['canonical_article_id']??''),
                    'plan_slot'=>(string)($receipt['plan_slot']??''),
                    'status'=>'PLANNED','intent_summary'=>(string)($receipt['intent_summary']??'')];
                $reservations++;
            }
            $result['sources']['MINI_RESERVED']=['complete'=>true,'item_count'=>$reservations];
            // Version only the original WP/PSTE/PSERC sources. Our own
            // MINI reservations are transported separately and checked by
            // existing slot uniqueness. Otherwise importing a FREI decision
            // would invalidate the very snapshot it just accepted.
            $sourceRevisions=(array)$result['sources'];
            unset($sourceRevisions['MINI_RESERVED']);
            $sourceItems=array_values(array_filter($result['items'],
                static fn($x)=>is_array($x)&&($x['source']??'')!=='MINI_RESERVED'));
            $encoded=wp_json_encode(['sources'=>$sourceRevisions,'items'=>$sourceItems],
                JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);
            if(!is_string($encoded))throw new RuntimeException('PARKHAUS_ENCODING_FAILED');
            if($sourceProblems){
                // A full diagnostic snapshot is usable to repair existing data,
                // but can NEVER be used as an external FREI/slot approval.
                $result['diagnostic_sha256']=hash('sha256',$encoded);
                $result['sha256']='';
                $result['complete']=false;
                $result['reason']=implode(';',$sourceProblems);
                return $result;
            }
            $result['sha256']=hash('sha256',$encoded);
            $result['complete']=true;$result['reason']='';
            return $result;
        } catch(Throwable $e) {
            // Incomplete source is NEVER semantic clearance. Keep the partial data
            // available for a technical diagnostic but no automatic FREI.
            $result['reason']=substr((string)$e->getMessage(),0,180);
            $result['sha256']='';
            $result['complete']=false;
            return $result;
        }
    }

    /**
     * Same existing MINI admin import, not a new worker or review.
     * Receives the ONE external SEO decision; validates only source, time,
     * completeness, and that no two writes reserve the same slot.
     * No similarity calculation or title quality judgement.
     */
    public static function acceptSingleOwnerSeoDecisions(array $state,array $document,array $snapshot,array $sourceRows=[],array $production=[]): array {
        if(($document['contract']??'')!=='PSTE_MINI_SEO_DECISIONS_V1'
            ||!is_array($document['items']??null)||!array_is_list($document['items']))
            throw new RuntimeException('PSTE_MINI_SEO_WRONG_DOCUMENT');
        if(empty($snapshot['complete'])||!preg_match('/^[a-f0-9]{64}$/D',(string)($snapshot['sha256']??''))
            ||!hash_equals((string)$snapshot['sha256'],(string)($document['snapshot_sha256']??'')))
            throw new RuntimeException('PSTE_MINI_SEO_PORTAL_PLAN_CHANGED_OR_INCOMPLETE');
        if(!isset($document['owner'])||$document['owner']!=='EXTERNAL_SINGLE_SEO_EDITOR')
            throw new RuntimeException('PSTE_MINI_SEO_OWNER_REQUIRED');
        $completed=(array)($state['completed']??[]);
        // Only check that an external BELEGT reference really identifies an
        // item in the original, read-only parkhouse. Never re-evaluate its
        // semantic similarity; that belongs to the ONE external owner.
        $existingReferences=[];
        foreach((array)($snapshot['items']??[]) as $existing){
            if(!is_array($existing))continue;
            // Proven legacy debris and old no-longer-existing drafts have no
            // semantic article to cite as BELEGT; their slots stay reserved.
            if(($existing['status']??'')==='LEGACY_EMPTY_PLACEHOLDER'
                ||($existing['title_status']??'')==='HISTORICAL_ORPHAN_RESERVATION')continue;
            $source=(string)($existing['source']??'');
            if($source==='')continue;
            foreach(['id','post_id','pool_key','seo_topic_id','canonical_article_id',
                'record_index','intent_slot','plan_slot'] as $field){
                if(!is_scalar($existing[$field]??null))continue;
                $identifier=trim((string)$existing[$field]);
                if($identifier!=='')$existingReferences[$source.':'.$identifier]=true;
            }
        }
        // One technical uniqueness check for the whole file, BEFORE any
        // approval is staged. Two rows for one source must never leave the
        // first FREI alive just because the second was skipped.
        $occurrences=[];
        foreach($document['items'] as $row){
            if(!is_array($row))continue;
            $id=(string)($row['pool_key']??'');
            if($id!=='')$occurrences[$id]=($occurrences[$id]??0)+1;
        }
        // Reserved real article/plan slots are immutable input, not another
        // intent/SEO evaluator. MINI reservations are handled separately below.
        $occupiedPlanSlots=[];
        foreach((array)($snapshot['items']??[]) as $existing){
            if(!is_array($existing)||($existing['source']??'')==='MINI_RESERVED')continue;
            foreach(['intent_slot','plan_slot'] as $field){
                $occupied=trim((string)($existing[$field]??''));
                if($occupied!==''&&preg_match('/^[a-f0-9]{64}$/D',$occupied)){
                    $occupiedPlanSlots[$occupied]=true;
                }
            }
        }
        $updates=[];$clarification=[];$reserved=[];$seen=[];
        $occupiedCanonical=[];
        if(class_exists('PSERC_Slot_Allocator'))foreach(PSERC_Slot_Allocator::occupiedCanonicalIds(false) as $id){
            $id=trim((string)$id);if($id!=='')$occupiedCanonical[$id]=true;
        }
        foreach((array)($state['seo_decisions']??[]) as $old){
            if(!is_array($old)||($old['box']??'')!=='FREI')continue;
            $id=trim((string)($old['canonical_article_id']??''));
            if($id!=='')$occupiedCanonical[$id]=true;
        }
        foreach((array)($state['seo_decisions']??[]) as $key=>$old){
            if(!is_array($old)||($old['box']??'')!=='FREI')continue;
            $oldSlot=(string)($old['intent_slot']??'');
            if($oldSlot!=='')$reserved[$oldSlot]=(string)$key;
        }
        foreach($document['items'] as $index=>$item){
            if(!is_array($item)){
                $clarification['UNKNOWN_ROW_'.$index]=[
                    'pool_key'=>'','reason_code'=>'SEO_RESULT_SHAPE_INVALID',
                    'next_action'=>'REVIEW_BY_SAME_EXTERNAL_SEO_OWNER'];
                continue;
            }
            $key=(string)($item['pool_key']??'');
            if($key!==''&&($occurrences[$key]??0)>1){
                $clarification[$key]=[
                    'pool_key'=>$key,'reason_code'=>'SEO_DUPLICATE_SOURCE_ROWS',
                    'next_action'=>'REVIEW_BY_SAME_EXTERNAL_SEO_OWNER'];
                // Invalidating a previous receipt is safer than reusing it
                // after a contradictory new upload. No semantic judgement.
                unset($state['seo_decisions'][$key]);
                continue;
            }
            if($key===''){
                $clarification['UNKNOWN_ROW_'.count($seen)]=[
                    'pool_key'=>'','reason_code'=>'SEO_UNKNOWN_SOURCE',
                    'next_action'=>'REVIEW_BY_SAME_EXTERNAL_SEO_OWNER'];
                continue;
            }
            $seen[$key]=true;
            $hasTitle=is_array($completed[$key]??null);
            $saved=$hasTitle?$completed[$key]:null;
            $source=(array)($sourceRows[$key]??[]);
            $sourcePayload=json_decode((string)($source['payload_json']??''),true);
            $raw=$hasTitle?(string)($saved['raw_query']??''):
                (is_array($sourcePayload)?PSTE_Editorializer::sourceQuery($sourcePayload):'');
            if($raw===''||($hasTitle&&($saved['decision']??'')!=='JA')
                ||(!$hasTitle&&((string)($source['pool_key']??'')!==$key||(int)($source['id']??0)<=0))
                ||!hash_equals($raw,(string)($item['raw_query']??''))
                ||!hash_equals(hash('sha256',$key.'|'.$raw),(string)($item['source_sha256']??''))){
                $clarification[$key]=['pool_key'=>$key,
                    'reason_code'=>'SEO_ORIGINAL_SOURCE_BINDING_FAILED',
                    'next_action'=>'REVIEW_BY_SAME_EXTERNAL_SEO_OWNER'];
                unset($state['seo_decisions'][$key]);
                continue;
            }
            $box=(string)($item['box']??'');
            if(!in_array($box,['FREI','BELEGT','KLAERUNG'],true)){
                $box='KLAERUNG';$item['reason']='EDITORIAL_OUTCOME_MISSING';
            }
            $selected=$hasTitle?(string)($saved['titles'][0]['title']??''):'';
            $intent=(string)($item['intent_summary']??'');
            $slot=(string)($item['intent_slot']??'');
            $match=(string)($item['matched_ref']??'');
            if($box==='FREI'&&(($hasTitle&&($selected===''||($item['approved_title']??'')!==$selected))
                ||(!$hasTitle&&trim((string)($item['approved_title']??''))!=='')
                ||trim($intent)===''||!preg_match('/^[a-f0-9]{64}$/D',$slot)
                ||isset($occupiedPlanSlots[$slot])
                ||(isset($reserved[$slot])&&$reserved[$slot]!==$key))){
                $box='KLAERUNG';$item['reason']='FREI_MISSING_OR_CONFLICTING_SOURCE_SLOT';
            }
            if($box==='BELEGT'&&($match===''||!isset($existingReferences[$match]))){
                $box='KLAERUNG';
                $item['reason']='BELEGT_REFERENCE_NOT_IN_EXISTING_PARKHAUS';
            }
            // Bind the REAL canonical article place in the same EXISTING SEO receipt,
            // before MINI. The signed PSERC allocator is the sole technical slot authority.
            $canonical='';$planSlot='';$articleType='';$categorySlug='';
            if($box==='FREI'){
                // An already approved topic retains its original booked position
                // even when MINI has not written the title yet. No second
                // allocation for a repeated import of the same SEO decision.
                $articleType=trim((string)($sourcePayload['proposed_article_type']??''));
                $categorySlug=trim((string)($sourcePayload['target_category_slug']??''));
                $prior=(array)($state['seo_decisions'][$key]??[]);
                $priorCanonical=trim((string)($prior['canonical_article_id']??''));
                if($priorCanonical!==''){
                    $priorPlanSlot=(string)($prior['plan_slot']??'');
                    if(($prior['contract']??'')!=='PSTE_MINI_SEO_DECISIONS_V1'
                        ||($prior['box']??'')!=='FREI'
                        ||!hash_equals((string)($prior['source_sha256']??''),hash('sha256',$key.'|'.$raw))
                        ||!hash_equals((string)($prior['intent_slot']??''),$slot)
                        ||!hash_equals((string)($prior['approved_title']??''),$selected)
                        ||$articleType===''||$categorySlug===''
                        ||!hash_equals((string)($prior['article_type']??''),$articleType)
                        ||!hash_equals((string)($prior['category_slug']??''),$categorySlug)
                        ||!class_exists('PSERC_Plan_Slot_Identity')
                        ||!hash_equals(PSERC_Plan_Slot_Identity::tokenFromCanonicalId($priorCanonical),$priorPlanSlot)){
                        $box='KLAERUNG';$item['reason']='EXISTING_PREBOOKING_SOURCE_BINDING_CHANGED';
                    }else{
                        $canonical=$priorCanonical;$planSlot=$priorPlanSlot;
                    }
                }elseif(defined('TXE_PLANFREE_KISS_V1') && TXE_PLANFREE_KISS_V1){
                    // A historic FREI without original binding is never assigned a new identity.
                    if(($prior['box']??'')==='FREI'){
                        $box='KLAERUNG';$item['reason']='PRETITLE_CANONICAL_PLAN_NOT_READY';
                    }elseif($articleType==='' || $categorySlug===''
                        ||!preg_match('/^[a-f0-9]{64}$/D',$key)
                        ||!class_exists('PSERC_Plan_Slot_Identity')){
                        $box='KLAERUNG';$item['reason']='PRETITLE_CANONICAL_PLAN_NOT_READY';
                    }else{
                        // The ORIGINAL PSTE topic UUID is the one immutable article identity;
                        // the original PSERC function derives the required five-field K0 token.
                        $proposedSlot=PSERC_Plan_Slot_Identity::tokenFromCanonicalId($key);
                        if(isset($occupiedCanonical[$key]) || isset($occupiedPlanSlots[$proposedSlot])){
                            $box='KLAERUNG';$item['reason']='PRETITLE_CANONICAL_SLOT_ALREADY_RESERVED';
                        }else{
                            $canonical=$key;$planSlot=$proposedSlot;$occupiedCanonical[$key]=true;
                        }
                    }
                }elseif($articleType===''||$categorySlug===''
                    ||empty($production['ok'])||!class_exists('PSERC_Slot_Allocator')
                    ||!class_exists('PSERC_Plan_Slot_Identity')){
                    $box='KLAERUNG';$item['reason']='PRETITLE_CANONICAL_PLAN_NOT_READY';
                }else{
                    // New approvals reserve BEFORE MINI; historical FREI receipts
                    // with a completed title can be technically booked without
                    // making another editorial decision.
                    $allocation=PSERC_Slot_Allocator::allocate([
                        ['pool_key'=>$key,'article_type'=>$articleType,'category_slug'=>$categorySlug]
                    ],$production,array_keys($occupiedCanonical));
                    $allocated=(array)($allocation['items'][0]??[]);
                    $place=(array)($allocated['slot']??[]);
                    if(($allocated['status']??'')!=='READY_FOR_METADATA_HANDOFF'
                        ||trim((string)($place['canonical_article_id']??''))===''){
                        $box='KLAERUNG';$item['reason']='PRETITLE_CANONICAL_SLOT_NOT_AVAILABLE';
                    }else{
                        $canonical=(string)$place['canonical_article_id'];
                        $planSlot=PSERC_Plan_Slot_Identity::token($place);
                        if(isset($occupiedCanonical[$canonical])){
                            $box='KLAERUNG';$item['reason']='PRETITLE_CANONICAL_SLOT_ALREADY_RESERVED';
                            $canonical='';$planSlot='';
                        }else $occupiedCanonical[$canonical]=true;
                    }
                }
            }
            if($box==='FREI')$reserved[$slot]=$key;
            $receipt=['contract'=>'PSTE_MINI_SEO_DECISIONS_V1','pool_key'=>$key,
                'raw_query'=>$raw,'source_sha256'=>hash('sha256',$key.'|'.$raw),
                'snapshot_sha256'=>(string)$snapshot['sha256'],'box'=>$box,
                'intent_slot'=>$box==='FREI'?$slot:'',
                'canonical_article_id'=>$box==='FREI'?$canonical:'',
                'plan_slot'=>$box==='FREI'?$planSlot:'',
                'article_type'=>$box==='FREI'?$articleType:'',
                'category_slug'=>$box==='FREI'?$categorySlug:'',
                'matched_ref'=>$box==='BELEGT'?$match:'',
                'approved_title'=>$box==='FREI'?$selected:'',
                'intent_summary'=>$intent,
                'reason'=>$box==='KLAERUNG'?(string)($item['reason']??'EXTERNAL_UNCERTAIN'):'',
                'received_utc'=>gmdate('c')];
            // A technical inability to book an already approved historical
            // title must NEVER rewrite its existing SEO decision as KLARUNG.
            // Leave the original receipt unchanged and make the technical
            // booking unavailable until source category/type/PPM are proven.
            $previousReceipt=(array)($state['seo_decisions'][$key]??[]);
            if($box==='KLAERUNG'&&($previousReceipt['box']??'')==='FREI'
                &&hash_equals((string)($previousReceipt['source_sha256']??''),hash('sha256',$key.'|'.$raw))
                &&hash_equals((string)($previousReceipt['approved_title']??''),$selected)
                &&in_array((string)($item['reason']??''),[
                    'PRETITLE_CANONICAL_PLAN_NOT_READY',
                    'PRETITLE_CANONICAL_SLOT_NOT_AVAILABLE',
                    'PRETITLE_CANONICAL_SLOT_ALREADY_RESERVED',
                    'EXISTING_PREBOOKING_SOURCE_BINDING_CHANGED'],true)){
                $clarification[$key]=['pool_key'=>$key,
                    'reason_code'=>(string)$item['reason'],
                    'next_action'=>'RETRY_EXISTING_TECHNICAL_SLOT_BINDING'];
                continue;
            }
            $updates[$key]=$receipt;
            if($box==='KLAERUNG')$clarification[$key]=[
                'pool_key'=>$key,'reason_code'=>$receipt['reason'],
                'next_action'=>'REVIEW_BY_SAME_EXTERNAL_SEO_OWNER'];
        }
        $state['seo_decisions']=array_replace((array)($state['seo_decisions']??[]),$updates);
        $state['clarification']=array_replace((array)($state['clarification']??[]),$clarification);
        foreach($updates as $key=>$receipt)if($receipt['box']!=='KLAERUNG')unset($state['clarification'][$key]);
        $count=['FREI'=>0,'BELEGT'=>0,'KLAERUNG'=>0];
        foreach($updates as $receipt)$count[$receipt['box']]++;
        foreach($clarification as $key=>$item)if(!isset($updates[$key]))$count['KLAERUNG']++;
        $state['seo_last_report']=['counts'=>$count,'snapshot_sha256'=>(string)$snapshot['sha256'],
            'received_utc'=>gmdate('c'),'semantic_evaluation_in_wordpress'=>false,
            'eligible_for_article_handoff'=>false];
        return $state;
    }

    /**
     * One existing WordPress option, atomically replaced only if it is still
     * the exact state read before the external verdict was accepted.
     * Prevents parallel receipts from claiming the same slot without adding
     * a lock table, second store, or any SEO check.
     */
    private static function storeSeoDecisionsIfUnchanged(array $before,array $after): void {
        global $wpdb;
        if(!is_object($wpdb)||empty($wpdb->options)
            ||!method_exists($wpdb,'prepare')||!method_exists($wpdb,'get_row')
            ||!method_exists($wpdb,'query')||!function_exists('maybe_serialize')
            ||!function_exists('maybe_unserialize'))
            throw new RuntimeException('PSTE_MINI_ATOMIC_OPTION_STORAGE_UNAVAILABLE');

        // Compare to the *actual serialized database value*, not a newly
        // serialized get_option() result. WordPress state normalization, e.g.
        // missing legacy default keys, need not recreate the original bytes.
        // A genuine concurrent change must still block the entire import.
        $row=$wpdb->get_row($wpdb->prepare(
            "SELECT option_value FROM {$wpdb->options} WHERE option_name=%s",
            self::STORE),ARRAY_A);
        if(!is_array($row)||!isset($row['option_value'])
            ||((string)($wpdb->last_error??''))!=='')
            throw new RuntimeException('PSTE_MINI_ATOMIC_OPTION_SOURCE_READ_FAILED');
        $old=(string)$row['option_value'];
        $source=maybe_unserialize($old);
        if(!is_array($source))
            throw new RuntimeException('PSTE_MINI_ATOMIC_OPTION_SOURCE_INVALID');
        $source+=['completed'=>[], 'active'=>null, 'last_report'=>[], 'clarification'=>[]];
        if($source!==$before)
            throw new RuntimeException('PSTE_MINI_ATOMIC_OPTION_CHANGED_RELOAD_REQUIRED');
        $next=maybe_serialize($after);
        if(!is_string($next))
            throw new RuntimeException('PSTE_MINI_ATOMIC_OPTION_SERIALIZATION_FAILED');
        if(hash_equals($old,$next))
            throw new RuntimeException('PSTE_MINI_ATOMIC_OPTION_NO_CHANGE');

        // Exact compare-and-swap. A second write between SELECT and UPDATE
        // causes 0 affected rows, so no external SEO verdict is overwritten.
        $changed=$wpdb->query($wpdb->prepare(
            "UPDATE {$wpdb->options} SET option_value=%s WHERE option_name=%s AND BINARY option_value=BINARY %s",
            $next,self::STORE,$old));
        if($changed===false||((string)($wpdb->last_error??''))!=='')
            throw new RuntimeException('PSTE_MINI_ATOMIC_OPTION_DATABASE_WRITE_FAILED');
        if($changed!==1)
            throw new RuntimeException('PSTE_MINI_ATOMIC_OPTION_CHANGED_RELOAD_REQUIRED');
        if(function_exists('wp_cache_delete')){
            wp_cache_delete(self::STORE,'options');
            wp_cache_delete('alloptions','options');
        }
        if(get_option(self::STORE,null)!==$after)
            throw new RuntimeException('PSTE_MINI_ATOMIC_OPTION_READBACK_FAILED');
    }

    public static function isMiniTopicAwaitingSeo(string $poolKey): bool {
        $state=self::loadState();
        $v=$state['completed'][$poolKey]??null;
        return is_array($v)&&($v['decision']??'')==='JA';
    }

    /**
     * The only technical proof reader for later WP/PSERC consumers.
     * No SEO evaluation, no new article decision.
     */
    /**
     * Recognize the original FINAL FREI verdict even if its technical booking
     * is incomplete. This does NOT make the topic production-ready.
     * Prevents a second semantic owner from running on a previously approved
     * topic while its missing source/slot bindings are repaired.
     */
    public static function hasStoredFinalFrei(string $poolKey,string $rawQuery): bool {
        if($poolKey===''||$rawQuery==='')return false;
        $state=self::loadState();
        $proof=(array)($state['seo_decisions'][$poolKey]??[]);
        return ($proof['contract']??'')==='PSTE_MINI_SEO_DECISIONS_V1'
            &&($proof['box']??'')==='FREI'
            &&hash_equals((string)($proof['raw_query']??''),$rawQuery)
            &&hash_equals((string)($proof['source_sha256']??''),hash('sha256',$poolKey.'|'.$rawQuery));
    }

    public static function singleOwnerSeoFor(string $poolKey,string $rawQuery,bool $requireForwarded=false): array {
        $state=self::loadState();$data=(array)($state['seo_decisions'][$poolKey]??[]);
        $saved=(array)($state['completed'][$poolKey]??[]);
        // The original FREI verdict remains stored if its technical booking
        // cannot be proven, but a held receipt must not enter the plan.
        $technicalHold=(string)($state['clarification'][$poolKey]['reason_code']??'');
        if(in_array($technicalHold,[
            'PRETITLE_CANONICAL_PLAN_NOT_READY',
            'PRETITLE_CANONICAL_SLOT_NOT_AVAILABLE',
            'PRETITLE_CANONICAL_SLOT_ALREADY_RESERVED',
            'EXISTING_PREBOOKING_SOURCE_BINDING_CHANGED'],true))return [];
        if(($data['contract']??'')!=='PSTE_MINI_SEO_DECISIONS_V1'
            ||(string)($saved['decision']??'')!=='JA'||$poolKey===''||$rawQuery===''
            ||!hash_equals((string)($data['raw_query']??''),$rawQuery)
            ||!hash_equals((string)($saved['raw_query']??''),$rawQuery)
            ||!hash_equals(hash('sha256',$poolKey.'|'.$rawQuery),(string)($data['source_sha256']??''))
            ||(($data['box']??'')==='FREI'&&!hash_equals((string)($data['approved_title']??''),(string)($saved['titles'][0]['title']??''))))
            return [];
        // FREI is the ONE editorial verdict, not permission to skip the
        // mandatory PRE-MINI article-place binding. An old verdict may stay
        // stored without being presented as technically ready.
        if(($data['box']??'')==='FREI'){
            $id=trim((string)($data['canonical_article_id']??''));
            if($id===''||!class_exists('PSERC_Plan_Slot_Identity')
                ||!hash_equals(PSERC_Plan_Slot_Identity::tokenFromCanonicalId($id),
                    (string)($data['plan_slot']??'')))return [];
        }
        if($requireForwarded&&($data['box']??'')==='FREI'){
            // Existing MINI forwardToPlan checkpoints, not a new reviewer.
            // A newly imported external opinion is NOT yet a plan approval.
            $title=(string)($data['approved_title']??'');
            $sourceHash=hash('sha256',$rawQuery.'|'.$title);
            if(!hash_equals($sourceHash,(string)($state['plan_forwarded'][$poolKey]??''))
                ||!self::titleAlreadyQueued((array)($state['plan_queued']??[]),$poolKey,$sourceHash))
                return [];
        }
        return $data;
    }


    /**
     * Pure preflight: a former plan containing ONLY identity-less legacy debris must
     * not remain the owner of a stale baseline forever. Never infer semantic emptiness
     * from a generic missing hash; require the raw source audit and the COMPLETE queue.
     * No writes, no source rename, no SEO owner rerun.
     */
    public static function legacyEmptyPlanRebindPreflight(
        array $baseline,array $inventory,array $structure,array $plan,array $origin,
        array $job,array $manifest,array $queue,array $state,array $parkhaus
    ): array {
        if(($baseline['contract']??'')!=='PSTE_SITE_BASELINE_V1'
            ||($baseline['taxonomy_contract']??'')!=='PSTE_PORTAL_TAXONOMY_SNAPSHOT_V3'
            ||($baseline['status']??'')!=='CURRENT')
            throw new RuntimeException('PSTE_MINI_REBIND_BASELINE_INVALID');
        if(($plan['contract']??'')!=='PSTE_EDITORIAL_PLAN_SNAPSHOT_V1'
            ||($plan['status']??'')!=='NOT_AVAILABLE'
            ||($plan['sha256']??'')!=='NOT_AVAILABLE'
            ||(array)($plan['items']??[])!==[])
            throw new RuntimeException('PSTE_MINI_REBIND_LIVE_PLAN_NOT_EMPTY');
        if(($origin['contract']??'')!=='PSTE_EDITORIAL_PLAN_SNAPSHOT_V1'
            ||($origin['source_origin']??'')!=='OPTION'||!empty($origin['source_conflict'])
            ||(int)($origin['unresolved_count']??-1)!==0)
            throw new RuntimeException('PSTE_MINI_REBIND_PLAN_SOURCE_UNPROVEN');
        $rows=(array)($origin['items']??[]);
        if(!$rows||(int)($origin['legacy_empty_count']??0)!==count($rows))
            throw new RuntimeException('PSTE_MINI_REBIND_PLAN_NOT_LEGACY_ONLY');
        foreach($rows as $row)if(!is_array($row)
            ||($row['status']??'')!=='LEGACY_EMPTY_PLACEHOLDER'
            ||($row['semantic_occupancy']??'')!=='NONE'
            ||trim((string)($row['title']??''))!=='')
            throw new RuntimeException('PSTE_MINI_REBIND_PLAN_HAS_SEMANTIC_SOURCE');
        if(($inventory['contract']??'')!=='PSTE_INVENTORY_SNAPSHOT_V2'
            ||!hash_equals((string)($baseline['inventory_sha256']??''),(string)($inventory['sha256']??'')))
            throw new RuntimeException('PSTE_MINI_REBIND_INVENTORY_CHANGED');
        if(($structure['contract']??'')!=='PSTE_PORTAL_TAXONOMY_SNAPSHOT_V3'
            ||empty($structure['validation']['ok'])
            ||!hash_equals((string)($baseline['structure_sha256']??''),(string)($structure['sha256']??''))
            ||(int)($baseline['leaf_category_count']??-1)!==count((array)($structure['items']??[])))
            throw new RuntimeException('PSTE_MINI_REBIND_PRODUCTION_STRUCTURE_CHANGED');
        if(($job['status']??'')!=='COMPLETE'||($job['contract']??'')!==
            'PSTE_CONTEXT_REFRESH_JOB_V9_EQUIVALENT_STRUCTURE_RESUME')
            throw new RuntimeException('PSTE_MINI_REBIND_CONTEXT_NOT_COMPLETE');
        if(($manifest['contract']??'')!==PSTE_Context_Index_Store::CONTRACT
            ||!hash_equals((string)($manifest['job_uuid']??''),(string)($job['job_uuid']??''))
            ||!hash_equals((string)($manifest['structure_sha256']??''),(string)($baseline['structure_sha256']??''))
            ||!hash_equals((string)($manifest['inventory_sha256']??''),(string)($baseline['inventory_sha256']??''))
            ||!hash_equals((string)($manifest['editorial_plan_sha256']??''),(string)($baseline['editorial_plan_sha256']??''))
            ||!hash_equals((string)($manifest['baseline_sha256']??''),(string)($baseline['baseline_sha256']??'')))
            throw new RuntimeException('PSTE_MINI_REBIND_CONTEXT_MANIFEST_MISMATCH');
        if((string)($baseline['editorial_plan_sha256']??'')==='' 
            ||(string)$baseline['editorial_plan_sha256']==='NOT_AVAILABLE')
            throw new RuntimeException('PSTE_MINI_REBIND_ALREADY_REBOUND_OR_MISSING');
        if(!preg_match('/^[a-f0-9]{64}$/D',(string)$baseline['editorial_plan_sha256']))
            throw new RuntimeException('PSTE_MINI_REBIND_PRIOR_PLAN_HASH_INVALID');
        if(($queue['status']??'')!=='COMPLETE'
            ||!is_array($queue['done']??null)||!is_array($queue['outcomes']??null)
            ||(array)($queue['pending']??[])!==[])
            throw new RuntimeException('PSTE_MINI_REBIND_OLD_QUEUE_NOT_PROVEN');
        if(!is_array($state['completed']??null)||!is_array($state['seo_decisions']??null)
            ||!is_array($state['plan_forwarded']??null)||!is_array($state['plan_queued']??null))
            throw new RuntimeException('PSTE_MINI_REBIND_MINI_STATE_INVALID');
        // A prior SEO opinion may be replayed only against its identical original
        // six-source parkhouse. MINI reservations are excluded by the existing reader.
        $parkhausSha=(string)($parkhaus['sha256']??'');
        if(empty($parkhaus['complete'])||($parkhaus['contract']??'')!=='PSTE_MINI_PARKHAUS_SNAPSHOT_V1'
            ||!preg_match('/^[a-f0-9]{64}$/D',$parkhausSha))
            throw new RuntimeException('PSTE_MINI_REBIND_ORIGINAL_PARKHAUS_NOT_AVAILABLE');
        $eligible=[];$slots=[];
        foreach($state['completed'] as $key=>$topic){
            if(!is_array($topic)||($topic['decision']??'')!=='JA')continue;
            $raw=(string)($topic['raw_query']??'');
            $seo=(array)($state['seo_decisions'][$key]??[]);
            if(($seo['box']??'')!=='FREI')continue;
            $title=(string)($topic['titles'][0]['title']??'');
            $slot=(string)($seo['intent_slot']??'');
            $hash=hash('sha256',$raw.'|'.$title);
            if(!hash_equals($parkhausSha,(string)($seo['snapshot_sha256']??'')))
                throw new RuntimeException('PSTE_MINI_REBIND_SEO_SNAPSHOT_CHANGED');
            if(($seo['contract']??'')!=='PSTE_MINI_SEO_DECISIONS_V1'
                ||!hash_equals((string)($seo['raw_query']??''),$raw)
                ||!hash_equals((string)($seo['source_sha256']??''),hash('sha256',$key.'|'.$raw))
                ||!hash_equals((string)($seo['approved_title']??''),$title)
                ||!preg_match('/^[a-f0-9]{64}$/D',$slot)||isset($slots[$slot])
                ||!hash_equals($hash,(string)($state['plan_forwarded'][$key]??''))
                ||!self::titleAlreadyQueued((array)$state['plan_queued'],(string)$key,$hash))
                throw new RuntimeException('PSTE_MINI_REBIND_ORIGINAL_SEO_OR_TITLE_CHANGED');
            $slots[$slot]=true;$eligible[]=(string)$key;
        }
        if(!$eligible||count($eligible)>100)
            throw new RuntimeException('PSTE_MINI_REBIND_ELIGIBLE_COUNT_INVALID');
        $done=array_values(array_map('strval',(array)$queue['done']));
        $outcomes=array_keys((array)$queue['outcomes']);
        sort($eligible,SORT_STRING);sort($done,SORT_STRING);sort($outcomes,SORT_STRING);
        if($eligible!==$done||$eligible!==$outcomes||count($done)!==(int)($queue['total']??-1))
            throw new RuntimeException('PSTE_MINI_REBIND_REENTRY_KEYS_CHANGED');
        $technical=0;$manual=0;
        foreach($eligible as $key){
            $code=(string)($queue['outcomes'][$key]['error_code']??'');
            if($code==='PSTE_RETAINED_EDITORIAL_PLAN_SNAPSHOT_CHANGED')$technical++;
            elseif($code==='PSTE_TITLE_DESK_REENTRY_MANUAL_REVIEW_UNCHANGED')$manual++;
            else throw new RuntimeException('PSTE_MINI_REBIND_PRIOR_OUTCOME_NOT_TECHNICAL');
        }
        if($technical<1)
            throw new RuntimeException('PSTE_MINI_REBIND_NO_STALE_PLAN_OUTCOME');
        return ['contract'=>'PSTE_MINI_LEGACY_EMPTY_PLAN_REBIND_PREFLIGHT_V1',
            'status'=>'PASS','eligible_keys'=>$eligible,'technical_stale'=>$technical,
            'preexisting_manual_review'=>$manual,'old_baseline_plan_sha256'=>(string)$baseline['editorial_plan_sha256'],
            'new_plan_sha256'=>'NOT_AVAILABLE','read_only'=>true,'article_or_taxonomy_write_attempted'=>false,
            'seo_owner_rerun'=>false,'production_approval'=>false];
    }

    /** Commit only the exact preflight already read from the real live source options. */
    private static function commitLegacyEmptyPlanRebind(array $pre,array $baseline,array $job,array $inventory,array $structure): void {
        if(($pre['contract']??'')!=='PSTE_MINI_LEGACY_EMPTY_PLAN_REBIND_PREFLIGHT_V1'
            ||($pre['status']??'')!=='PASS'||empty($pre['eligible_keys'])
            ||!hash_equals((string)($pre['old_baseline_plan_sha256']??''),(string)($baseline['editorial_plan_sha256']??'')))
            throw new RuntimeException('PSTE_MINI_REBIND_COMMIT_PREFLIGHT_INVALID');
        // Verify the old immutable context and the 11-type registry BEFORE writing the baseline.
        $oldBinding=PSTE_Context_Index_Store::runtimeBinding($job,$baseline);
        $oldRegistry=PSTE_Context_Index_Store::registrySnapshot($oldBinding);
        if(empty($oldRegistry['types'])||empty($oldRegistry['families']))
            throw new RuntimeException('PSTE_MINI_REBIND_REGISTRY_NOT_PROVEN');
        $rebased=PSTE_Snapshot::rebaseResearchBaselineIfSafe($baseline);
        if(empty($rebased['ok'])||empty($rebased['changed'])
            ||($rebased['mode']??'')!=='SAFE_DYNAMIC_CONTEXT_REBASE')
            throw new RuntimeException('PSTE_MINI_REBIND_BASELINE_CHANGE_NOT_VERIFIED');
        $fresh=(array)($rebased['baseline']??[]);
        if((string)($fresh['editorial_plan_sha256']??'')!=='NOT_AVAILABLE'
            ||!hash_equals((string)($fresh['inventory_sha256']??''),(string)($inventory['sha256']??''))
            ||!hash_equals((string)($fresh['structure_sha256']??''),(string)($structure['sha256']??'')))
            throw new RuntimeException('PSTE_MINI_REBIND_BASELINE_READBACK_FAILED');
        // The normal existing runtime index is rehydrated from current source snapshots.
        // Never make up an old plan hash or rewrite the nine raw legacy rows.
        $binding=PSTE_Context_Index_Store::rebuildCompletedRuntimeIndexForExplicitOwner($job,$fresh);
        if(($binding['editorial_plan_sha256']??'')!=='NOT_AVAILABLE')
            throw new RuntimeException('PSTE_MINI_REBIND_CONTEXT_READBACK_FAILED');
        $registry=PSTE_Context_Index_Store::registrySnapshot($binding);
        if(empty($registry['types'])||empty($registry['families']))
            throw new RuntimeException('PSTE_MINI_REBIND_REBUILT_REGISTRY_INVALID');
        $n=PSTE_Admin::scheduleTitleDeskReentry((array)$pre['eligible_keys'],true);
        if($n!==count((array)$pre['eligible_keys']))
            throw new RuntimeException('PSTE_MINI_REBIND_REENTRY_QUEUE_READBACK_FAILED');
        PSTE_Admin::processTitleDeskReentry();
    }

    /** The operator explicitly requests an internal TEST recheck; never run on activation. */
    public static function legacyEmptyPlanRebind(): void {
        try {
            PSTE_Auth::assertAdmin('pste_mini_legacy_plan_rebind',(string)($_POST['_wpnonce']??''));
            if(!PSTE_Plugin::isReady())throw new RuntimeException('PSTE_MINI_REBIND_PLUGIN_NOT_READY');
            $baseline=get_option(PSTE_OPTION_SITE_BASELINE,[]);
            $job=PSTE_Context_Refresh::status();
            $manifest=get_option(PSTE_OPTION_CONTEXT_INDEX_MANIFEST,[]);
            $queue=get_option('pste_title_desk_reentry_state_v1',[]);
            $mini=self::loadState();
            $inventory=PSTE_Snapshot::inventory();
            $structure=PSTE_Snapshot::structure();
            $plan=PSTE_Snapshot::editorialPlan();
            $origin=PSTE_Snapshot::editorialPlanForParkhaus();
            $parkhaus=self::readParkhausForMini();
            $pre=self::legacyEmptyPlanRebindPreflight(
                $baseline,$inventory,$structure,$plan,$origin,$job,$manifest,$queue,$mini,$parkhaus);
            self::commitLegacyEmptyPlanRebind($pre,$baseline,$job,$inventory,$structure);
            wp_safe_redirect(admin_url('admin.php?page=portal-seo-topic-engine-review&pste_mini_rebound=1'));
            exit;
        }catch(Throwable $e){self::fail($e);}
    }

    public static function renderManualBrief(): void {
        echo '<section class="pste-box"><h3>NEU · Manueller Schreibauftrag (Übergang, ohne K0)</h3>';
        echo '<p>Ein einzelnes Thema für die externe Artikelerstellung ausgeben – mit einer Bestandsübersicht für den redaktionellen Abgleich. Noch keine automatische Planfreigabe und kein WordPress-Beitrag.</p>';
        echo '<form method="post" action="'.esc_url(admin_url('admin-post.php')).'">';wp_nonce_field('pste_mini_manual_brief');
        echo '<input type="hidden" name="action" value="pste_mini_manual_brief">';
        echo '<p><label>Thema / gewünschter Titel<br><input type="text" name="manual_topic" style="width:100%;max-width:580px" maxlength="250" required></label></p>';
        echo '<p><label>Zielkeyword<br><input type="text" name="manual_keyword" style="width:100%;max-width:580px" maxlength="200" required></label></p>';
        echo '<p><button class="button" type="submit">Schreibauftrag mit Artikelbestand exportieren</button></p></form></section>';
    }

    /** Read-only inventory: never claim semantic duplicate clearance. */
    public static function manualArticleBrief(): void {
        try {
            PSTE_Auth::assertAdmin('pste_mini_manual_brief',(string)($_POST['_wpnonce']??''));
            $topic=trim(sanitize_text_field((string)($_POST['manual_topic']??'')));
            $keyword=trim(sanitize_text_field((string)($_POST['manual_keyword']??'')));
            if($topic===''||$keyword===''||strlen($topic)>250||strlen($keyword)>200)
                throw new RuntimeException('PSTE_MINI_MANUAL_TOPIC_REQUIRED');
            global $wpdb;
            $postsTable=$wpdb->posts;$pool=PSTE_Repository::table('topic_pool');
            $posts=$wpdb->get_results("SELECT ID,post_title,post_status FROM $postsTable WHERE post_type='post' AND post_status IN ('publish','future','draft','pending','private') ORDER BY ID DESC LIMIT 1201",ARRAY_A);
            if(!is_array($posts))throw new RuntimeException('PSTE_MINI_MANUAL_POSTS_UNAVAILABLE');
            $plans=$wpdb->get_results("SELECT pool_key,payload_json FROM $pool WHERE planning_suitability='YES' ORDER BY id DESC LIMIT 1201",ARRAY_A);
            if(!is_array($plans))throw new RuntimeException('PSTE_MINI_MANUAL_PLAN_UNAVAILABLE');
            $postComplete=count($posts)<=1200;$planComplete=count($plans)<=1200;
            $existing=[];
            foreach(array_slice($posts,0,1200) as $p){$existing[]=['post_id'=>(int)$p['ID'],'title'=>(string)$p['post_title'],'status'=>(string)$p['post_status']];}
            $scheduled=[];$missingPlanTitles=0;
            foreach(array_slice($plans,0,1200) as $p){
                $meta=json_decode((string)($p['payload_json']??''),true);
                if(!is_array($meta))throw new RuntimeException('PSTE_MINI_MANUAL_PLAN_PAYLOAD_INVALID');
                $title=PSTE_Editorializer::displayTitle($meta);
                if($title!=='')$scheduled[]=['pool_key'=>(string)$p['pool_key'],'title'=>$title];
                else $missingPlanTitles++;
            }
            self::sendJson(['contract'=>'PSTE_MANUAL_ARTICLE_BRIEF_V1','created_utc'=>gmdate('c'),
                'manual_request'=>['topic'=>$topic,'target_keyword'=>$keyword],
                'existing_wordpress_posts'=>$existing,'planned_pste_titles'=>$scheduled,
                'inventory_complete'=>['posts'=>$postComplete,'pste_plan'=>$planComplete&&$missingPlanTitles===0],
                'planned_rows_without_titles'=>$missingPlanTitles,
                'coverage_note'=>'PSERC-eigene Planstaende und semantische Doppelungen sind mit diesen Listen NICHT abschliessend geprueft.', 
                'status'=>'EDITORIAL_CHECK_REQUIRED',
                'instruction'=>'Vor der Artikelerstellung bestehende und geplante Texte auf dieselbe Suchabsicht pruefen. Dies ist ein manueller Zwischenweg ohne K0, keine automatische Dubletten-/Planfreigabe. Nur bei freiem eigenstaendigem Thema Artikel nach den bestehenden redaktionellen Regeln erstellen. WordPress-Aufnahme erfolgt manuell als Entwurf.',
                'no_k0_write'=>true,'no_posts_written'=>true], 'pferdeatelier-kurzauftrag-'.gmdate('Ymd-His').'.json');
        } catch(Throwable $e){self::fail($e);}
    }
}
