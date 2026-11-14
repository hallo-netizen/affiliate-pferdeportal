<?php
/**
 * Plugin Name: Texterstellung
 * Description: Portalneutrale Texterstellung mit integrierter Fehlerdiagnose: Recherche, Freigaberegal, Sofortartikel, Titeldateien, K0-Export, Entwurfsimport. Isolierte Testinstallation.
 * Version: 0.4.1-original-k0-sync-qa
 * Requires PHP: 8.1
 */
if (!defined('ABSPATH')) { exit; }
require_once __DIR__.'/includes/class-txe-normalizer.php';
require_once __DIR__.'/includes/class-txe-secret-store.php';
require_once __DIR__.'/includes/class-txe-credentials.php';
require_once __DIR__.'/includes/class-txe-dataforseo-client.php';
require_once __DIR__.'/includes/class-txe-diagnose.php';
// Reuse the whole PSTE original source unchanged (search, PAA, editorial rules and pool).
// Do not activate both the standalone PSTE plugin and this consolidated candidate.
$txeOldActive = false;
$txeActivePlugins = function_exists('get_option') ? (array)get_option('active_plugins', []) : [];
if (function_exists('get_site_option')) {
    $txeActivePlugins = array_merge($txeActivePlugins, array_keys((array)get_site_option('active_sitewide_plugins', [])));
}
foreach ($txeActivePlugins as $txePluginPath) {
    if (basename((string)$txePluginPath) === 'portal-seo-topic-engine.php') { $txeOldActive = true; break; }
}
if ($txeOldActive || class_exists('PSTE_Plugin', false)) {
    add_action('admin_notices', static function () {
        echo '<div class="notice notice-error"><p>Texterstellung: alte Themenengine noch aktiv. Keine zweite Recherche gestartet.</p></div>';
    });
    return;
}
require_once __DIR__.'/original/pste/portal-seo-topic-engine.php';
// The WordPress backend has one top-level entry. Existing PSTE admin functions remain intact.
add_action('admin_menu', static function () { remove_menu_page('portal-seo-topic-engine'); }, 1001);
// Existing PSERC import functions: unchanged originals. No second importer implementation.
require_once __DIR__.'/original/pserc/class-pserc-stable-json.php';
require_once __DIR__.'/original/pserc/class-pserc-plan-slot-identity.php';
require_once __DIR__.'/original/pserc/class-pserc-system4-import.php';
// Original PSERC K0 batch encoder and technical five-field boundary (unchanged).
require_once __DIR__.'/original/pserc/class-pserc-plan-snapshot-store.php';
require_once __DIR__.'/original/pserc/class-pserc-metadata-boundary.php';


final class TXE_Workshop {
    const OPTION = 'texterstellung_orders_v1';
    const SLUG = 'texterstellung';
    const K0_CONTRACT = 'PSERC_TEXTMACHINE_METADATA_BATCH_V2';
    const IMPORT_CONTRACT = 'PFERDE_ATELIER_WORDPRESS_IMPORT_V1';
    const MAX_UPLOAD = 12582912;
    const TEST_MODE_OPTION = 'texterstellung_testsite_confirmation_v1';

    /**
     * The administrator confirms the exact site, not a server setting or URL guess.
     * This keeps the plugin inert after an accidental install or a site clone.
     */
    private static function siteFingerprint(): string {
        return hash('sha256', (string)home_url('/') . '|' . (string)get_current_blog_id());
    }
    public static function permitted(): bool {
        return hash_equals(self::siteFingerprint(), (string)get_option(self::TEST_MODE_OPTION, ''));
    }
    public static function activate(): void {
        // Activation itself does not run jobs, change data, or require wp-config edits.
        // Until the administrator confirms the isolated test site, all actions are blocked.
    }
    public static function confirmTestMode(): void {
        if (!function_exists('current_user_can') || !current_user_can('manage_options')) {
            wp_die('TEXTERSTELLUNG_ADMIN_ONLY');
        }
        check_admin_referer('txe_testmode_confirm');
        if ((string)($_POST['isolated_test_site'] ?? '') !== '1') {
            wp_die('TESTSITE_CONFIRMATION_REQUIRED');
        }
        update_option(self::TEST_MODE_OPTION, self::siteFingerprint(), false);
        if (!self::permitted()) {
            wp_die('TESTSITE_CONFIRMATION_NOT_SAVED');
        }
        // The nested unchanged PSTE source cannot receive the WordPress plugin
        // activation callback itself. Reuse its dormant status-only activation
        // ONLY after the administrator confirms the isolated test site.
        PSTE_Plugin::activate();
        wp_safe_redirect(add_query_arg(['page'=>self::SLUG, 'txe_testmode'=>'enabled'], admin_url('admin.php')));
        exit;
    }
    public static function init(): void {
        add_action('admin_menu', [self::class,'menu']);
        add_action('admin_post_txe_testmode_confirm', [self::class,'confirmTestMode']);
        TXE_Diagnose::init();
        foreach (['quick','import_queue','title_return','export','redownload','redownload_batch','import_drafts','research','approve_research','export_titles','import_titles','load_legacy','seo_export','seo_import','credentials_save'] as $action) {
            add_action('admin_post_txe_'.$action, [self::class,'handle']);
        }
        add_filter('wp_insert_post_data', [self::class,'preventPilotPublish'], 20, 2);
    }
    public static function preventPilotPublish(array $data, array $postarr): array {
        $id=(int)($postarr['ID']??0);
        $ownNew=is_array($postarr['meta_input']??null) && !empty($postarr['meta_input']['_texterstellung_order_id']);
        $ownExisting=$id>0 && function_exists('get_post_meta') && (string)get_post_meta($id,'_texterstellung_order_id',true)!=='';
        if (($ownNew||$ownExisting) && ($data['post_type']??'post')==='post') { $data['post_status']='draft'; }
        return $data;
    }
    private static function access(): void {
        if (!self::permitted()) { throw new RuntimeException('TESTENVIRONMENT_REQUIRED'); }
        if (!function_exists('current_user_can') || !current_user_can('manage_options')) { throw new RuntimeException('ADMIN_ONLY'); }
    }
    private static function state(): array {
        $s=get_option(self::OPTION, []);
        return is_array($s) && isset($s['orders']) && is_array($s['orders']) ? $s : ['version'=>1,'orders'=>[],'last_batch'=>null,'research'=>[],'title_batches'=>[],'active_title_batch'=>''];
    }
    private static function mutate(callable $callback) {
        self::access();
        global $wpdb;
        if (!isset($wpdb) || !method_exists($wpdb,'get_var') || !method_exists($wpdb,'prepare')) { throw new RuntimeException('DATABASE_LOCK_UNAVAILABLE'); }
        $name='txe_pilot_'.substr(hash('sha256',(string)get_current_blog_id().'|'.(string)home_url('/')),0,26);
        $locked=$wpdb->get_var($wpdb->prepare('SELECT GET_LOCK(%s, 5)', $name));
        if ((string)$locked!=='1') { throw new RuntimeException('QUEUE_BUSY_RETRY'); }
        try {
            $state=self::state();
            $result=$callback($state);
            if (!is_array($result) || !isset($result['state'])) { throw new RuntimeException('MUTATION_INVALID'); }
            $ok=update_option(self::OPTION,$result['state'],false);
            // WordPress update_option returns false for identical state. All mutations contain changed_at.
            if (!$ok && get_option(self::OPTION, null)!==$result['state']) { throw new RuntimeException('STATE_NOT_SAVED'); }
            if (get_option(self::OPTION, null)!==$result['state']) { throw new RuntimeException('STATE_READBACK_FAILED'); }
            TXE_Diagnose::stateChange($state, $result['state']);
            return $result['result']??null;
        } finally {
            $wpdb->get_var($wpdb->prepare('SELECT RELEASE_LOCK(%s)', $name));
        }
    }
    private static function changed(array &$s): void {$s['changed_at']=gmdate('c').'-'.bin2hex(random_bytes(3));}
    private static function text($v): string {return trim((string)$v);}
    private static function slot(string $id): string {return hash('sha256','pserc-plan-slot-v2|'.$id);}
    private static function orderId(string $portal,string $source): string {return 'TXE-'.substr(hash('sha256',$portal.'|'.$source),0,32);}
    private static function portal(): string {return strtolower((string)parse_url(home_url('/'),PHP_URL_HOST));}
    private static function listArray(array $value): bool {
        $i=0;foreach($value as $k=>$_)if($k!==$i++)return false;return true;
    }
    private static function stable($v) {
        if (!is_array($v)) return $v;
        if (self::listArray($v)) return array_map([self::class,'stable'],$v);
        ksort($v,SORT_STRING);foreach($v as $k=>$item){$v[$k]=self::stable($item);}return $v;
    }
    private static function digest(array $value): string {
        return hash('sha256',(string)wp_json_encode(self::stable($value),JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE|JSON_PRESERVE_ZERO_FRACTION));
    }
    private static function ready(array $o): bool {
        if (($o['status']??'')!=='FREI') return false;
        foreach (['title','target_keyword','category','article_type','plan_slot'] as $k)if(self::text($o[$k]??'')==='')return false;
        // Historical canonical identities are owned by PSTE; never mint one here.
        if (($o['origin']??'')==='ALT_FREIGABE' && self::text($o['article_id']??'')==='')return false;
        return true;
    }
    private static function checkedCategory(string $slug): string {
        $t=function_exists('get_term_by')?get_term_by('slug',$slug,'category'):false;
        if (!is_object($t) || !isset($t->term_id) || (int)$t->term_id<=0 || (string)($t->slug??'')!==$slug) throw new RuntimeException('CATEGORY_NOT_IN_THIS_PORTAL:'.$slug);
        return $slug;
    }
    private static function enqueue(array &$s,array $item,string $kind): string {
        $source=self::text($item['source_id']??'');
        if ($source==='') {throw new RuntimeException('SOURCE_ID_REQUIRED');}
        $id=self::orderId(self::portal(),$source);
        if(isset($s['orders'][$id])) {
            $prior=$s['orders'][$id];
            foreach (['source_id','target_keyword','category','article_type','title'] as $k) {
                $incoming=self::text($item[$k]??'');
                if ($incoming!=='' && self::text($prior[$k]??'')!=='' && $incoming!==self::text($prior[$k])) throw new RuntimeException('EXISTING_APPROVAL_CHANGED:'.$id.':'.$k);
            }
            // The same unchanged PSTE approval can later acquire its missing
            // original technical bindings. Fill ONLY previously empty fields;
            // never reevaluate the original SEO decision or replace an identity.
            if ($kind==='ALT_FREIGABE' && ($prior['origin']??'')==='ALT_FREIGABE'
                && ($prior['status']??'')==='METADATEN_OFFEN') {
                $updated=$prior;
                foreach (['title','category','article_type','intent','article_id','plan_slot'] as $k) {
                    $incoming=self::text($item[$k]??'');
                    if ($incoming==='')continue;
                    $current=self::text($updated[$k]??'');
                    if ($current!=='' && $incoming!==$current)throw new RuntimeException('ORIGINAL_BINDING_CHANGED:'.$id.':'.$k);
                    if ($current==='') {
                        if($k==='category')self::checkedCategory($incoming);
                        $updated[$k]=$incoming;
                    }
                }
                if (self::text($updated['article_id']??'')!=='' && self::text($updated['plan_slot']??'')!==''
                    && !hash_equals(self::slot((string)$updated['article_id']),(string)$updated['plan_slot']))
                    throw new RuntimeException('SLOT_ARTICLE_ID_MISMATCH');
                $complete=true;
                foreach(['title','target_keyword','category','article_type','article_id','plan_slot'] as $k)
                    if(self::text($updated[$k]??'')===''){$complete=false;break;}
                $updated['status']=$complete?'FREI':'METADATEN_OFFEN';
                if($complete)$updated['slot_origin']='PROVIDED_IN_APPROVAL';
                $s['orders'][$id]=$updated;
            }
            return $id;
        }
        $keyword=self::text($item['target_keyword']??'');
        $title=self::text($item['title']??'');
        $category=self::text($item['category']??'');
        $type=self::text($item['article_type']??'');
        if ($category!=='')self::checkedCategory($category);
        if ($keyword==='')throw new RuntimeException('KEYWORD_REQUIRED');
        foreach($s['orders'] as $existingId=>$previous) {
            $left=function_exists('mb_strtolower')?mb_strtolower(self::text($previous['target_keyword']??''),'UTF-8'):strtolower(self::text($previous['target_keyword']??''));
            $right=function_exists('mb_strtolower')?mb_strtolower($keyword,'UTF-8'):strtolower($keyword);
            if($left!==$right)continue;
            // The signed five-field handoff may complete an older incomplete PSTE approval.
            // This is strictly a binding of an existing decision, NOT a second SEO review.
            if($kind==='BESTEHENDE_FREIGABE' && ($previous['origin']??'')==='ALT_FREIGABE'
                && ($previous['status']??'')==='METADATEN_OFFEN'
                && self::text($previous['category']??'')==='' && self::text($previous['article_type']??'')===''
                && self::text($previous['title']??'')===$title) {
                $incomingSlot=self::text($item['plan_slot']??'');
                if(!preg_match('/^[a-f0-9]{64}$/D',$incomingSlot))throw new RuntimeException('COMPLETION_SLOT_MISSING');
                $s['orders'][$existingId]['category']=$category;
                $s['orders'][$existingId]['article_type']=$type;
                $s['orders'][$existingId]['target_keyword']=$keyword;
                $s['orders'][$existingId]['plan_slot']=$incomingSlot;
                $s['orders'][$existingId]['slot_origin']='PROVIDED_BY_ORIGINAL_K0';
                $s['orders'][$existingId]['article_id']=self::text($item['article_id']??'');
                $s['orders'][$existingId]['status']='FREI';
                return $existingId;
            }
            throw new RuntimeException('KEYWORD_ALREADY_IN_QUEUE:'.$keyword);
        }
        $slot=self::text($item['plan_slot']??'');
        $canonical=self::text($item['article_id']??'');
        if ($slot!=='' && !preg_match('/^[a-f0-9]{64}$/D',$slot))throw new RuntimeException('PLAN_SLOT_INVALID');
        if ($canonical!=='' && $slot!=='' && !hash_equals(self::slot($canonical),$slot))throw new RuntimeException('SLOT_ARTICLE_ID_MISMATCH');
        // Partially recorded old identities stay visible and unchanged, but remain held.
        // Never generate or clear an original canonical ID or slot on import.
        $slotOrigin=($slot!=='' ? 'PROVIDED_IN_APPROVAL' : 'GENERATED_LOCALLY');
        // Historical FREI decisions keep their original article identity. A missing
        // original booking is a technical HOLD, not permission to invent a new slot.
        if ($canonical==='' && $slot==='') {
            if ($kind!=='ALT_FREIGABE') { $canonical=$id;$slot=self::slot($id); }
        }
        $ready=$keyword!==''&&$title!==''&&$category!==''&&$type!==''&&$slot!==''
            &&($kind!=='ALT_FREIGABE'||$canonical!=='');
        $s['orders'][$id]=[
            'id'=>$id,'source_id'=>$source,'origin'=>$kind,'intent'=>self::text($item['intent']??''),
            'target_keyword'=>$keyword,'title'=>$title,'category'=>$category,'article_type'=>$type,
            'article_id'=>$canonical,'plan_slot'=>$slot,'slot_origin'=>$slotOrigin,'status'=>$ready?'FREI':'METADATEN_OFFEN',
            'batch'=>'','post_id'=>0,
        ];
        return $id;
    }
    public static function quick(array $entry): string {
        return self::mutate(static function(array $s)use($entry) {
            $entry['source_id']='SHORT-'.bin2hex(random_bytes(12));
            $id=self::enqueue($s,$entry,'SOFORTARTIKEL');
            self::changed($s);return ['state'=>$s,'result'=>$id];
        });
    }
    public static function titleReturn(string $id,string $title): void {
        self::mutate(static function(array $s)use($id,$title){
            $id=self::text($id);$title=self::text($title);
            if(!isset($s['orders'][$id]))throw new RuntimeException('TITLE_ORDER_NOT_FOUND');
            if($title==='')throw new RuntimeException('TITLE_REQUIRED');
            $old=$s['orders'][$id];
            if((string)$old['title']!=='' && !hash_equals((string)$old['title'],$title))throw new RuntimeException('TITLE_ALREADY_FIXED');
            if($old['status']!=='METADATEN_OFFEN' && !hash_equals((string)$old['title'],$title))throw new RuntimeException('TITLE_ORDER_NOT_PENDING');
            $s['orders'][$id]['title']=$title;
            $o=$s['orders'][$id];
            if(self::text($o['category'])!=='' && self::text($o['article_type'])!=='' && self::text($o['plan_slot'])!=='')$s['orders'][$id]['status']='FREI';
            self::changed($s);return ['state'=>$s,'result'=>true];
        });
    }
    public static function ingest(array $json): array {
        return self::mutate(static function(array $s)use($json){
            $contract=self::text($json['contract']??'');$new=[];$held=0;$issues=[];
            if ($contract===self::K0_CONTRACT) {
                PSERC_Metadata_Boundary::requireReadyBatchForExport($json);
                $items=(array)$json['items'];
                foreach($items as $i=>$v){
                    try {if(!is_array($v))throw new RuntimeException('ITEM_INVALID');
                    $keys=array_keys($v);sort($keys);$want=['title','target_keyword','category','article_type','plan_slot'];sort($want);
                    if($keys!==$want)throw new RuntimeException('K0_ITEM_FIELDS_CHANGED');
                    $v['source_id']='K0-SLOT-'.(string)$v['plan_slot'];
                    $new[]=self::enqueue($s,$v,'BESTEHENDE_FREIGABE'); }catch(RuntimeException $e){$issues[]=['index'=>$i,'reason'=>$e->getMessage()];TXE_Diagnose::record('APPROVAL_ITEM_HELD',['index'=>$i,'code'=>TXE_Diagnose::errorCode($e)]);}
                }
            } elseif($contract==='PSTE_MINI_SEO_DECISIONS_V1') {
                foreach((array)($json['items']??[]) as $i=>$v) {
                    if(!is_array($v)||self::text($v['box']??'')!=='FREI')continue;
                    try{$new[]=self::enqueue($s,['source_id'=>self::text($v['pool_key']??''),
                        'target_keyword'=>self::text($v['raw_query']??''),'title'=>self::text($v['approved_title']??''),
                        'category'=>self::text($v['category']??$v['category_slug']??''),
                        'article_type'=>self::text($v['article_type']??''),'intent'=>self::text($v['intent_summary']??''),
                        'article_id'=>self::text($v['canonical_article_id']??''),
                        'plan_slot'=>self::text($v['plan_slot']??'')], 'ALT_FREIGABE');}catch(RuntimeException $e){$issues[]=['index'=>$i,'reason'=>$e->getMessage()];TXE_Diagnose::record('APPROVAL_ITEM_HELD',['index'=>$i,'code'=>TXE_Diagnose::errorCode($e)]);}
                }
            } else {throw new RuntimeException('UNSUPPORTED_APPROVAL_FORMAT');}
            foreach($new as $id)if(($s['orders'][$id]['status']??'')==='METADATEN_OFFEN')$held++;
            self::changed($s);return ['state'=>$s,'result'=>['total'=>count($new),'held'=>$held,'ready'=>count($new)-$held,'issues'=>$issues]];
        });
    }
    private static function assemble(array $items): array {
        $out=[];foreach($items as $order){$out[]=[
            'title'=>(string)$order['title'],'target_keyword'=>(string)$order['target_keyword'],
            'category'=>(string)$order['category'],'article_type'=>(string)$order['article_type'],
            'plan_slot'=>(string)$order['plan_slot']];}
        // Unchanged PSERC source now builds AND validates the exact K0 handoff.
        // No second editorial or title decision is made here.
        $batch=PSERC_Plan_Snapshot_Store::batchFromItems($out);
        PSERC_Metadata_Boundary::requireReadyBatchForExport($batch);
        return $batch;
    }
    public static function export(int $n): array {
        self::syncOriginalFrei();
        $n=min(50,max(1,$n));
        return self::mutate(static function(array $s)use($n){
            $selection=[];
            foreach($s['orders'] as $id=>$order){if(count($selection)>=$n)break;if(self::ready($order))$selection[$id]=$order;}
            if(!$selection)throw new RuntimeException('NO_APPROVED_READY_ARTICLES');
            $batch=self::assemble(array_values($selection));
            foreach($selection as $id=>$_){$s['orders'][$id]['status']='EXPORTIERT';$s['orders'][$id]['batch']=$batch['batch_sha256'];}
            $s['last_batch']=$batch;
            self::changed($s);return ['state'=>$s,'result'=>$batch];
        });
    }
    public static function redownloadBatch(string $batchHash): array {
        self::access();
        if(!preg_match('/^[a-f0-9]{64}$/D',$batchHash))throw new RuntimeException('BATCH_HASH_INVALID');
        $s=self::state();$orders=[];
        foreach($s['orders'] as $o) {
            if(($o['batch']??'')===$batchHash && in_array(($o['status']??''),['EXPORTIERT','IMPORTIERT'],true))$orders[]=$o;
        }
        if(!$orders)throw new RuntimeException('BATCH_NOT_FOUND');
        $batch=self::assemble($orders);
        if(!hash_equals($batchHash,$batch['batch_sha256']))throw new RuntimeException('BATCH_SOURCE_CHANGED');
        return $batch;
    }
    public static function lastBatch(): array {self::access();$s=self::state();if(!is_array($s['last_batch']??null))throw new RuntimeException('NO_PREVIOUS_BATCH');return $s['last_batch'];}

    /** Keep the existing TXE order reservation, but delegate WordPress writes
     *  to the unchanged PSERC importer and its original PPM publish protection.
     *  No own content assessment, no own replacement importer.
     */
    public static function importDrafts(array $json): array {
        $verified=PSERC_System4_Import::normalizePayload($json);
        if(empty($verified['ok']))throw new RuntimeException('ORIGINAL_PSERC_IMPORT_BLOCKED:'.(string)($verified['reason_codes'][0]??$verified['status']??'UNKNOWN'));
        $rows=(array)$verified['rows'];
        return self::mutate(static function(array $s)use($rows,$json){
            $orderBySlot=[];
            foreach($s['orders'] as $id=>$o){
                $slot=(string)($o['plan_slot']??'');
                if($slot!=='' && isset($orderBySlot[$slot]))throw new RuntimeException('ORDER_SLOT_DUPLICATE');
                if($slot!=='')$orderBySlot[$slot]=(string)$id;
            }
            foreach($rows as $v){
                $slot=$v['plan_slot'];
                if(!isset($orderBySlot[$slot]))throw new RuntimeException('RETURN_NOT_IN_THIS_QUEUE');
                $o=$s['orders'][$orderBySlot[$slot]];
                if(!in_array((string)($o['status']??''),['EXPORTIERT','IMPORTIERT'],true))throw new RuntimeException('RETURN_NOT_EXPORTED');
                foreach(['title','target_keyword','category','article_type'] as $key){
                    if((string)($o[$key]??'')!==$v[$key])throw new RuntimeException('RETURN_APPROVAL_MISMATCH:'.$key);
                }
                if(($o['article_id']??'')!==''&&!hash_equals((string)$o['article_id'],$v['article_id']))throw new RuntimeException('RETURN_ARTICLE_ID_MISMATCH');
            }
            $result=PSERC_System4_Import::importPayload($json);
            if(empty($result['ok'])){
                $codes=(array)($result['reason_codes']??[]);
                throw new RuntimeException('ORIGINAL_PSERC_IMPORT_BLOCKED:'.(string)($codes[0]??$result['status']??'UNKNOWN'));
            }
            $readback=[];
            foreach((array)($result['readback']??[]) as $rb){
                if(!empty($rb['ok']))$readback[(string)($rb['plan_slot']??'')]=(int)($rb['post_id']??0);
            }
            foreach($rows as $v){
                $postId=$readback[$v['plan_slot']]??0;
                if($postId<=0)throw new RuntimeException('ORIGINAL_IMPORT_READBACK_MISSING');
                $id=$orderBySlot[$v['plan_slot']];
                $s['orders'][$id]['status']='IMPORTIERT';
                $s['orders'][$id]['post_id']=$postId;
            }
            self::changed($s);
            return ['state'=>$s,'result'=>['imported'=>count($rows),'draft_ids'=>array_values($readback),'created'=>count((array)($result['created_post_ids']??[]))]];
        });
    }
    /** Original PSTE owns DataForSEO, Google questions, SEO decisions, costs and saved pool. */
    public static function runResearch(string $seed,int $categoryId): array {
        self::access();
        $seed=self::text($seed);
        if($seed===''||(function_exists('mb_strlen')?mb_strlen($seed,'UTF-8'):strlen($seed))>160)
            throw new RuntimeException('RESEARCH_SEED_INVALID');
        if($categoryId<=0)throw new RuntimeException('CATEGORY_REQUIRED_FOR_ORIGINAL_RESEARCH');
        if(!PSTE_Plugin::isReady())throw new RuntimeException('ORIGINAL_PSTE_MIGRATION_REQUIRED');
        $job=PSTE_Research_Job::start($categoryId,$seed,PSTE_Plugin::settings());
        $driver=PSTE_Research_Driver::kick(0,'START_SINGLE');
        return ['job_uuid'=>(string)($job['job_uuid']??''),'status'=>(string)($driver['status']??'STARTED')];
    }

    /** Source-of-truth read: use the actual PSTE topic pool, do not clone its decisions. */
    public static function originalTopicPool(): array {
        self::access();
        if(!PSTE_Plugin::isReady())throw new RuntimeException('ORIGINAL_PSTE_MIGRATION_REQUIRED');
        return ['total'=>PSTE_Repository::topicPoolCount(),
            'page'=>PSTE_Repository::adminTopicPoolPage(null,40),
            'job'=>PSTE_Research_Job::peek()];
    }

    /** The one editorial owner decides portal relevance, intent, category and article type. */
    public static function approveResearch(string $key,string $category,string $type,string $intent): string {
        return self::mutate(static function(array $s)use($key,$category,$type,$intent) {
            $key=self::text($key);$category=self::text($category);$type=self::text($type);$intent=self::text($intent);
            if(!isset($s['research'][$key])||!is_array($s['research'][$key]))throw new RuntimeException('RESEARCH_ITEM_UNKNOWN');
            if($category===''||$type===''||$intent==='')throw new RuntimeException('ONE_OWNER_APPROVAL_FIELDS_REQUIRED');
            self::checkedCategory($category);
            $row=$s['research'][$key];
            if(($row['status']??'')!=='RECHERCHIERT')throw new RuntimeException('SEO_SINGLE_OWNER_DECISION_ALREADY_IN_PROGRESS_OR_FINAL');
            $id=self::enqueue($s,[
                'source_id'=>'RESEARCH-'.$key,'target_keyword'=>$row['keyword'],
                'category'=>$category,'article_type'=>$type,'intent'=>$intent,'title'=>'',
            ],'RECHERCHE_FREIGEGEBEN');
            $s['research'][$key]['status']='FREIGEGEBEN';
            $s['research'][$key]['order_id']=$id;
            self::changed($s);return ['state'=>$s,'result'=>$id];
        });
    }

    /** Exactly one frozen research handoff to the existing external SEO-editor role. */
    public static function seoExport(int $n=20): array {
        $n=max(1,min(50,$n));
        return self::mutate(static function(array $s)use($n) {
            if(!empty($s['active_seo_batch']) && isset($s['seo_batches'][$s['active_seo_batch']])) {
                self::changed($s);
                return ['state'=>$s,'result'=>$s['seo_batches'][$s['active_seo_batch']]];
            }
            $items=[];
            foreach((array)($s['research']??[]) as $key=>$r) {
                if(count($items)>=$n)break;
                if(($r['status']??'')!=='RECHERCHIERT')continue;
                $kw=self::text($r['keyword']??'');
                if($kw==='')continue;
                $items[]=['pool_key'=>(string)$key,'raw_query'=>$kw,
                    'seed'=>self::text($r['seed']??''),
                    'search_volume'=>$r['search_volume']??null,
                    'source_sha256'=>hash('sha256',$key.'|'.$kw)];
            }
            if(!$items)throw new RuntimeException('NO_UNDECIDED_RESEARCH_TOPICS');
            $categories=[];
            foreach((array)get_categories(['hide_empty'=>false]) as $term){
                $categories[]=['slug'=>(string)$term->slug,'name'=>(string)$term->name,
                    'existing_posts'=>(int)($term->count??0)];
            }
            // The single editorial owner needs the existing WordPress and approved backlog,
            // otherwise a judgment about duplicate search intent would be guesswork.
            $inventory=[];
            $ids=get_posts(['post_type'=>'post','post_status'=>['publish','draft','future','pending','private'],
                'posts_per_page'=>10000,'fields'=>'ids']);
            foreach((array)$ids as $postId){
                $post=get_post((int)$postId);
                if(!$post)continue;
                $inventory[]=['post_id'=>(int)$postId,'title'=>(string)$post->post_title,
                    'slug'=>(string)$post->post_name,
                    'keyword'=>(string)get_post_meta((int)$postId,'_texterstellung_target_keyword',true)];
            }
            if(count((array)$ids)>=10000)throw new RuntimeException('SEO_INVENTORY_TOO_LARGE_NOT_COMPLETE');
            $approved=[];
            foreach((array)$s['orders'] as $order) {
                $approved[]=['order_id'=>(string)$order['id'],'keyword'=>(string)$order['target_keyword'],
                    'intent'=>(string)($order['intent']??''),'category'=>(string)$order['category'],
                    'article_type'=>(string)$order['article_type'],'status'=>(string)$order['status']];
            }
            $batchId='seo-'.gmdate('YmdHis').'-'.bin2hex(random_bytes(6));
            $batch=['contract'=>'TEXTERSTELLUNG_SINGLE_EDITOR_BATCH_V1','owner'=>'EXTERNAL_SINGLE_SEO_EDITOR',
                'batch_id'=>$batchId,'title_only'=>false,
                'instruction'=>'Einmal und ausschließlich hier entscheiden: Portaleignung, Suchintention, bestehende Suchabsicht, Kategorie, Artikelart und Lücken im Kategoriebaum. Pro Eintrag nur die Felder box, intent_summary, category_slug, article_type und matched_ref ergänzen. Bei BELEGT/KLAERUNG keine freie Freigabe; nicht nachgelagert erneut SEO prüfen.',
                'categories'=>$categories,'existing_wordpress_articles'=>$inventory,'approved_backlog'=>$approved,
                'inventory_has_full_wordpress_scope'=>count((array)$ids)<10000,
                'items'=>$items];
            $batch['source_sha256']=self::digest($batch);
            $s['seo_batches'][$batchId]=$batch;
            $s['active_seo_batch']=$batchId;
            foreach($items as $item) {
                $s['research'][$item['pool_key']]['status']='REDAKTION_EXTERN';
            }
            self::changed($s);return ['state'=>$s,'result'=>$batch];
        });
    }

    /** Import the one external editorial decision; no SEO reassessment afterward. */
    public static function seoImport(array $received): array {
        return self::mutate(static function(array $s)use($received) {
            $id=self::text($received['batch_id']??'');
            $frozen=$s['seo_batches'][$id]??null;
            if(!is_array($frozen)||($received['contract']??'')!=='TEXTERSTELLUNG_SINGLE_EDITOR_BATCH_V1')throw new RuntimeException('SEO_BATCH_UNKNOWN');
            $allowed=['box','intent_summary','category_slug','article_type','matched_ref'];
            $frozenHead=$frozen;$recvHead=$received;
            unset($frozenHead['items'],$recvHead['items']);
            if($frozenHead!==$recvHead)throw new RuntimeException('SEO_FROZEN_HEADER_CHANGED');
            $rows=$received['items']??null;
            if(!is_array($rows)||!array_is_list($rows)||count($rows)!==count($frozen['items']))throw new RuntimeException('SEO_ITEM_COUNT_CHANGED');
            $results=['total'=>count($rows),'approved'=>0,'covered'=>0,'held'=>0,'issues'=>[]];
            foreach($rows as $i=>$row){
                $orig=$frozen['items'][$i];
                $key=(string)$orig['pool_key'];
                try {
                    if(!is_array($row))throw new RuntimeException('SEO_DECISION_ROW_INVALID');
                    $check=$row;
                    foreach($allowed as $allowedKey)unset($check[$allowedKey]);
                    if($check!==$orig)throw new RuntimeException('SEO_RESEARCH_SOURCE_CHANGED');
                    $box=self::text($row['box']??'');
                    if(!in_array($box,['FREI','BELEGT','KLAERUNG'],true))throw new RuntimeException('SEO_BOX_NOT_FINAL');
                    $current=(string)($s['research'][$key]['status']??'');
                    if(!in_array($current,['REDAKTION_EXTERN','FREIGEGEBEN','BELEGT','KLAERUNG'],true))
                        throw new RuntimeException('SEO_SOURCE_STATUS_CHANGED');
                    if($current!=='REDAKTION_EXTERN' && $current!==($box==='FREI'?'FREIGEGEBEN':$box))
                        throw new RuntimeException('SEO_DECISION_CONFLICT_WITH_PRIOR_ACCEPTANCE');
                    if($box==='FREI') {
                        $cat=self::checkedCategory(self::text($row['category_slug']??''));
                        $type=self::text($row['article_type']??'');
                        $intent=self::text($row['intent_summary']??'');
                        if($type===''||$intent==='')throw new RuntimeException('SEO_FINAL_FIELDS_MISSING');
                        $orderId=self::enqueue($s,['source_id'=>'RESEARCH-'.$key,
                            'target_keyword'=>$orig['raw_query'],'category'=>$cat,
                            'article_type'=>$type,'intent'=>$intent,'title'=>''], 'RECHERCHE_FREIGEGEBEN');
                        $s['research'][$key]['status']='FREIGEGEBEN';
                        $s['research'][$key]['order_id']=$orderId;
                        ++$results['approved'];
                    }elseif($box==='BELEGT'){
                        $s['research'][$key]['status']='BELEGT';
                        $s['research'][$key]['matched_ref']=self::text($row['matched_ref']??'');
                        ++$results['covered'];
                    }else{
                        $s['research'][$key]['status']='KLAERUNG';
                        ++$results['held'];
                    }
                }catch(Throwable $e){
                    $results['issues'][]=['index'=>$i,'code'=>$e->getMessage()];
                    TXE_Diagnose::record('SEO_ITEM_HELD',['index'=>$i,'code'=>TXE_Diagnose::errorCode($e)]);
                    ++$results['held'];
                }
            }
            if(!$results['issues']){
                unset($s['seo_batches'][$id]);
                if(($s['active_seo_batch']??'')===$id)$s['active_seo_batch']='';
            }
            self::changed($s);
            return ['state'=>$s,'result'=>$results];
        });
    }

    /** Migration reads the exact old approval option, but never updates PSTE or PSERC data. */
    public static function loadLegacyApprovals(): array {
        self::access();
        $state=get_option('pste_mini_keyword_roundtrip_v1',[]);
        $proofs=is_array($state)?($state['seo_decisions']??[]):[];
        if(!is_array($proofs)||!count($proofs))throw new RuntimeException('NO_OLD_APPROVALS_FOUND_USE_APPROVAL_FILE');
        $items=[];$completed=(array)($state['completed']??[]);
        foreach($proofs as $key=>$proof){
            if(!is_array($proof)||($proof['box']??'')!=='FREI')continue;
            $title=self::text($proof['approved_title']??'');
            if($title==='')$title=self::text($completed[$key]['titles'][0]['title']??'');
            $raw=self::text($proof['raw_query']??'');
            // The original PSTE receipt is the only SEO authority, including its
            // original source hash. No new FREI decision is made on import.
            if (!PSTE_Mini_Workflow::hasStoredFinalFrei((string)$key,$raw)) continue;
            $items[]=[
                'box'=>'FREI','pool_key'=>(string)$key,'raw_query'=>$raw,
                'approved_title'=>$title,'intent_summary'=>self::text($proof['intent_summary']??''),
                'category_slug'=>self::text($proof['category_slug']??''),
                'article_type'=>self::text($proof['article_type']??''),
                'canonical_article_id'=>self::text($proof['canonical_article_id']??''),
                'plan_slot'=>self::text($proof['plan_slot']??''),
            ];
        }
        if(!$items)throw new RuntimeException('NO_FREE_OLD_APPROVALS');
        return self::ingest(['contract'=>'PSTE_MINI_SEO_DECISIONS_V1','items'=>$items]);
    }

    /** Technical handoff only: original PSTE is the sole owner of FREI decisions. */
    private static function syncOriginalFrei(): void {
        $original=get_option('pste_mini_keyword_roundtrip_v1',[]);
        if (!is_array($original) || empty($original['seo_decisions']))return;
        try {self::loadLegacyApprovals();}
        catch(RuntimeException $e) {
            if($e->getMessage()!=='NO_FREE_OLD_APPROVALS')throw $e;
        }
    }

    /** Full historical title-worker file shape. Only titles[0].title may be changed externally. */
    private static function originalTitleGovernance(): array {
        $file=__DIR__.'/contracts/intent-first-title-governance-v1.json';
        $v=json_decode((string)file_get_contents($file),true);
        if(!is_array($v)||($v['contract']??'')!=='PSTE_INTENT_FIRST_TITLE_GOVERNANCE_V1')throw new RuntimeException('TITLE_GOVERNANCE_NOT_AVAILABLE');
        return $v;
    }
    public static function exportTitleBatch(int $n=20): array {
        self::syncOriginalFrei();
        $n=max(1,min(50,$n));
        return self::mutate(static function(array $s)use($n){
            if(!empty($s['active_title_batch'])&&isset($s['title_batches'][$s['active_title_batch']])){
                // Repeated download is always the same frozen file.
                return ['state'=>self::bumpOnly($s),'result'=>$s['title_batches'][$s['active_title_batch']]];
            }
            $items=[];
            foreach($s['orders'] as $order){
                if(count($items)>=$n)break;
                if(($order['status']??'')!=='METADATEN_OFFEN'||self::text($order['title']??'')!=='')continue;
                foreach(['target_keyword','category','article_type','intent','article_id','plan_slot','source_id'] as $k){
                    if(self::text($order[$k]??'')==='')continue 2;
                }
                $raw=(string)$order['target_keyword'];$pool=(string)$order['source_id'];
                $rowId=(int)sprintf('%u',crc32($order['id']));
                if($rowId===0)$rowId=1;
                $intent=(string)$order['intent'];
                $items[]=[
                    'id'=>$rowId,'pool_key'=>$pool,'raw_query'=>$raw,
                    'source_sha256'=>hash('sha256',$rowId.'|'.$pool.'|'.$raw),
                    'decision'=>'JA','titles'=>[['intent'=>$intent,'title'=>'']],
                    'intent_slot'=>hash('sha256',$pool.'|'.$intent),
                    'seo_snapshot_sha256'=>hash('sha256',$pool.'|'.$raw.'|'.$order['category'].'|'.$order['article_type']),
                    'canonical_article_id'=>(string)$order['article_id'],
                    'plan_slot'=>(string)$order['plan_slot'],
                    'article_type'=>(string)$order['article_type'],
                    'category_slug'=>(string)$order['category'],
                ];
            }
            if(!$items)throw new RuntimeException('NO_APPROVED_TOPICS_NEED_TITLES');
            $batchId='mini-'.gmdate('YmdHis').'-'.substr(bin2hex(random_bytes(6)),0,12);
            $batch=['contract'=>'PSTE_RAW_KEYWORD_MINI_BATCH_V1','batch_id'=>$batchId,'created_utc'=>gmdate('c'),
                'title_only'=>true,
                'instruction'=>'Nur einen natuerlichen deutschen Titel fuer die fest freigegebene Suchabsicht schreiben. AUSSCHLIESSLICH items[*].titles[0].title aendern. Fachentscheid, Suchintention, Kategorie, Beitragsart und Reservierung sind bereits entschieden und du darfst sie NICHT aendern. Titel ohne Doppelpunkte oder Keyword-Schablonen, genau eine Hauptfrage. Keine neue SEO- oder Doppelungsentscheidung.',
                'title_governance'=>self::originalTitleGovernance(),
                'skipped_invalid_source_count'=>0,'items'=>$items];
            $s['title_batches'][$batchId]=$batch;$s['active_title_batch']=$batchId;
            self::changed($s);return ['state'=>$s,'result'=>$batch];
        });
    }
    private static function bumpOnly(array $s): array {self::changed($s);return $s;}

    /** Intake is strictly title-only; the original non-title fields are frozen. */
    public static function importTitleBatch(array $received): array {
        return self::mutate(static function(array $s)use($received){
            $id=self::text($received['batch_id']??'');
            $original=$s['title_batches'][$id]??null;
            if(!is_array($original)||($received['contract']??'')!=='PSTE_RAW_KEYWORD_MINI_BATCH_V1'||($original['contract']??'')!==$received['contract'])throw new RuntimeException('TITLE_WRONG_BATCH');
            $beforeHead=$original;$receivedHead=$received;
            unset($beforeHead['items'],$receivedHead['items']);
            if($beforeHead!==$receivedHead)throw new RuntimeException('TITLE_BATCH_HEADER_CHANGED');
            $before=$original['items'];$after=$received['items']??null;
            if(!is_array($after)||count($before)!==count($after)||!array_is_list($after))throw new RuntimeException('TITLE_ITEMS_CHANGED');
            $finished=0;$held=[];
            foreach($before as $i=>$frozen){
                $item=$after[$i]??null;
                try{
                    if(!is_array($item))throw new RuntimeException('TITLE_ROW_INVALID');
                    $unchanged=$item;$expected=$frozen;
                    unset($unchanged['titles'][0]['title'],$expected['titles'][0]['title']);
                    if($unchanged!==$expected)throw new RuntimeException('TITLE_FROZEN_FIELDS_CHANGED');
                    $title=self::text($item['titles'][0]['title']??'');
                    if($title===''||strlen($title)>300||preg_match('/[<>\\x00-\\x1F]/',$title))throw new RuntimeException('TITLE_TEXT_MISSING_OR_INVALID');
                    $owner='';
                    foreach($s['orders'] as $orderId=>$o){
                        if(($o['source_id']??'')===$frozen['pool_key'] && ($o['plan_slot']??'')===$frozen['plan_slot']){$owner=$orderId;break;}
                    }
                    if($owner==='')throw new RuntimeException('TITLE_ORDER_NOT_FOUND');
                    $old=(string)$s['orders'][$owner]['title'];
                    if($old!=='' && !hash_equals($old,$title))throw new RuntimeException('TITLE_ALREADY_FIXED');
                    $s['orders'][$owner]['title']=$title;
                    if(self::text($s['orders'][$owner]['category'])!==''&&self::text($s['orders'][$owner]['article_type'])!=='')$s['orders'][$owner]['status']='FREI';
                    $finished++;
                }catch(RuntimeException $e){$held[]=['index'=>$i,'reason'=>$e->getMessage()];TXE_Diagnose::record('TITLE_ITEM_HELD',['index'=>$i,'code'=>TXE_Diagnose::errorCode($e)]);}
            }
            $remaining=0;
            foreach($before as $row){
                foreach($s['orders'] as $o){if(($o['source_id']??'')===$row['pool_key']&&self::text($o['title']??'')===''){$remaining++;break;}}
            }
            if($remaining===0){unset($s['title_batches'][$id]);if(($s['active_title_batch']??'')===$id)$s['active_title_batch']='';}
            self::changed($s);return ['state'=>$s,'result'=>['titles'=>$finished,'held'=>$held,'pending'=>$remaining]];
        });
    }

    /** One bad article never stops independent valid articles. */
    public static function importDraftsIndividually(array $payload): array {
        self::access();
        $contract=self::text($payload['contract']??'');
        if(!in_array($contract,[self::IMPORT_CONTRACT,'SYSTEM4_WORDPRESS_HANDOFF_V1','SYSTEM4_7_ARTICLE_CHAT_HANDOFF_V1'],true))throw new RuntimeException('RETURN_CONTRACT_CHANGED');
        $rows=$payload['articles']??null;
        if(!is_array($rows)||!array_is_list($rows)||!count($rows)||count($rows)>50)throw new RuntimeException('RETURN_ARTICLES_INVALID');
        $out=['imported'=>0,'created'=>0,'draft_ids'=>[],'held'=>[]];
        $seenSlots=[];$seenSlugs=[];$seenTitles=[];
        foreach($rows as $i=>$row){
            try{
                $validated=PSERC_System4_Import::normalizePayload(['contract'=>$contract,'articles'=>[$row]]);
                if(empty($validated['ok']))throw new RuntimeException('ORIGINAL_PSERC_IMPORT_BLOCKED:'.(string)($validated['reason_codes'][0]??$validated['status']??'UNKNOWN'));
                $item=$validated['rows'][0];
                $slot=$item['plan_slot'];$slug=$item['slug'];$titleKey=sanitize_title($item['title']);
                if(isset($seenSlots[$slot])||isset($seenSlugs[$slug])||isset($seenTitles[$titleKey]))throw new RuntimeException('DUPLICATE_IN_RETURN_BATCH');
                $one=self::importDrafts(['contract'=>$contract,'articles'=>[$row]]);
                $seenSlots[$slot]=true;$seenSlugs[$slug]=true;$seenTitles[$titleKey]=true;
                $out['imported']+=(int)$one['imported'];$out['created']+=(int)$one['created'];
                $out['draft_ids']=array_merge($out['draft_ids'],(array)$one['draft_ids']);
            }catch(Throwable $e){
                $out['held'][]=['index'=>$i,'reason'=>$e->getMessage()];
                TXE_Diagnose::record('RETURN_ITEM_HELD', ['index'=>$i,'code'=>TXE_Diagnose::errorCode($e)]);
            }
        }
        return $out;
    }

    public static function coverage(): array {
        self::access();
        $state=self::state();$items=[];
        foreach((array)get_categories(['hide_empty'=>false]) as $term){
            $slug=(string)$term->slug;$count=0;
            foreach($state['orders'] as $order){if(($order['category']??'')===$slug && self::text($order['article_type']??'')!=='')$count++;}
            $items[]=['slug'=>$slug,'category'=>(string)$term->name,'existing'=>(int)($term->count??0),'planned'=>$count];
        }
        usort($items,static fn($a,$b)=>[$a['existing']+$a['planned'],$a['category']]<=>[$b['existing']+$b['planned'],$b['category']]);
        return $items;
    }

    private static function fileJson(string $field): array {
        $file=$_FILES[$field]??[];$tmp=(string)($file['tmp_name']??'');$size=(int)($file['size']??0);
        if($tmp===''||!is_uploaded_file($tmp)||$size<1||$size>self::MAX_UPLOAD)throw new RuntimeException('JSON_FILE_INVALID');
        $out=json_decode((string)file_get_contents($tmp),true);
        if(!is_array($out))throw new RuntimeException('JSON_INVALID');return $out;
    }
    private static function download(array $data,string $basename): void {
        TXE_Diagnose::record('OUTPUT_GENERATED', ['item_count'=>(int)($data['item_count']??count((array)($data['items']??[]))), 'batch_sha256'=>(string)($data['batch_sha256']??'')]);
        nocache_headers();header('Content-Type: application/json; charset=utf-8');header('Content-Disposition: attachment; filename="'.$basename.'"');
        echo wp_json_encode($data,JSON_PRETTY_PRINT|JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES|JSON_PRESERVE_ZERO_FRACTION);exit;
    }
    public static function handle(): void {
        try{
            self::access();$action=self::text($_POST['action']??'');
            if(!preg_match('/^txe_(quick|import_queue|title_return|export|redownload|redownload_batch|import_drafts|research|approve_research|export_titles|import_titles|load_legacy|seo_export|seo_import|credentials_save)$/',$action))throw new RuntimeException('ACTION_UNKNOWN');
            check_admin_referer($action);
            TXE_Diagnose::action($action);
            TXE_Diagnose::record('ACTION_STARTED');
            TXE_Diagnose::recordUpload();
            if($action==='txe_credentials_save') {
                PSTE_Credentials::saveFromAdmin(sanitize_text_field(wp_unslash($_POST['login']??'')),
                    (string)wp_unslash($_POST['password']??''));
                TXE_Diagnose::record('CREDENTIALS_UPDATED',['code'=>'PORTAL_LOCAL_SETTINGS']);
                self::redirect('DataForSEO Zugangsdaten für dieses Testportal gespeichert.');
            }
            if(in_array($action,['txe_seo_export','txe_seo_import','txe_approve_research'],true)) throw new RuntimeException('ORIGINAL_SEO_OWNER_ONLY');
            if($action==='txe_seo_export') {
                self::download(self::seoExport((int)($_POST['count']??20)),'texterstellung-redaktion-seo-auftrag.json');
            }
            if($action==='txe_seo_import') {
                $r=self::seoImport(self::fileJson('seo_file'));
                TXE_Diagnose::record('SEO_DECISION_INTAKE',['item_count'=>(int)$r['total'],'created'=>(int)$r['approved'],'held'=>(int)$r['held']]);
                self::redirect('Redaktionelle Entscheidungen übernommen: '.(int)$r['approved'].' frei, '.(int)$r['covered'].' belegt, '.(int)$r['held'].' offen.');
            }
            if($action==='txe_research') {
                if(empty($_POST['cost_ack']))throw new RuntimeException('DATAFORSEO_KOSTEN_NICHT_BESTAETIGT');
                $result=self::runResearch(sanitize_text_field(wp_unslash($_POST['seed']??'')),(int)($_POST['category_id']??0));
                TXE_Diagnose::record('RESEARCH_STARTED',['code'=>'ORIGINAL_PSTE_RESEARCH_JOB']);
                self::redirect('Original-Recherche gestartet. Google-Fragen und SEO werden im bestehenden PSTE-Job verarbeitet.');
            }
            if($action==='txe_approve_research') {
                $id=self::approveResearch(sanitize_text_field(wp_unslash($_POST['research_id']??'')),
                    sanitize_key(wp_unslash($_POST['category']??'')),
                    sanitize_text_field(wp_unslash($_POST['article_type']??'')),
                    sanitize_text_field(wp_unslash($_POST['intent']??'')));
                self::redirect('Einmalig freigegeben: '.$id.'. Titel kann extern erstellt werden.');
            }
            if($action==='txe_load_legacy'){
                $r=self::loadLegacyApprovals();
                self::redirect('Alte FREI-Freigaben nur lesend übernommen: '.(int)$r['total'].', davon '.(int)$r['held'].' ohne vollständige Daten.');
            }
            if($action==='txe_export_titles'){
                self::download(self::exportTitleBatch((int)($_POST['count']??20)),'texterstellung-titelauftrag.json');
            }
            if($action==='txe_import_titles'){
                $r=self::importTitleBatch(self::fileJson('title_file'));
                TXE_Diagnose::record('TITLE_BATCH_RESULT',['item_count'=>(int)($r['titles']??0),'held'=>count((array)($r['held']??[]))]);
                self::redirect('Titel zurück: '.(int)$r['titles'].', offen: '.(int)$r['pending'].', fehlerhafte Einzelantworten: '.count($r['held']));
            }

            if($action==='txe_quick'){
                $id=self::quick(['target_keyword'=>sanitize_text_field(wp_unslash($_POST['keyword']??'')),
                    'title'=>sanitize_text_field(wp_unslash($_POST['title']??'')),
                    'category'=>sanitize_key(wp_unslash($_POST['category']??'')),
                    'article_type'=>sanitize_text_field(wp_unslash($_POST['article_type']??'')), 'intent'=>sanitize_text_field(wp_unslash($_POST['intent']??''))]);
                self::redirect('Sofortauftrag gespeichert: '.$id);
            }
            if($action==='txe_title_return'){self::titleReturn(sanitize_text_field(wp_unslash($_POST['order_id']??'')),sanitize_text_field(wp_unslash($_POST['title']??'')));self::redirect('Externer Titel übernommen, keine zweite SEO-Entscheidung.');}
            if($action==='txe_import_queue'){ $r=self::ingest(self::fileJson('queue_file')); self::redirect('Freigaben: '.(int)$r['total'].' übernommen, '.(int)$r['held'].' wegen fehlender Pflichtangaben zurückgehalten.'); }
            if($action==='txe_export'){self::download(self::export((int)($_POST['count']??20)),'texterstellung-k0-export.json');}
            if($action==='txe_redownload'){self::download(self::lastBatch(),'texterstellung-k0-export-wiederholung.json');}
            if($action==='txe_redownload_batch'){self::download(self::redownloadBatch(sanitize_text_field(wp_unslash($_POST['batch_hash']??''))),'texterstellung-k0-export-charge.json');}
            if($action==='txe_import_drafts'){ $r=self::importDraftsIndividually(self::fileJson('draft_file'));TXE_Diagnose::record('IMPORT_RESULT',['imported'=>(int)$r['imported'],'created'=>(int)$r['created'],'held'=>count($r['held'])]);self::redirect('Entwürfe zugeordnet: '.(int)$r['imported'].', neu: '.(int)$r['created'].', angehaltene Einzelartikel: '.count($r['held'])); }
            throw new RuntimeException('ACTION_UNKNOWN');
        }catch(Throwable $e){ TXE_Diagnose::failure($e);self::redirect('STOP: '.$e->getMessage()); }
    }
    private static function redirect(string $note): void {
        if (!str_starts_with($note, 'STOP:')) TXE_Diagnose::record('ACTION_COMPLETED');
        $view=self::text($_POST['txe_return_view']??'uebersicht');
        if(!in_array($view,['uebersicht','recherche','redaktion','sofort','titel','k0','import','diagnose'],true))$view='uebersicht';
        $slug=$view==='uebersicht'?self::SLUG:self::SLUG.'-'.$view;
        wp_safe_redirect(add_query_arg(['page'=>$slug,'txe_notice'=>rawurlencode($note)],admin_url('admin.php')));exit;
    }
    public static function menu(): void {
        add_menu_page('Texterstellung (Test)','Texterstellung','manage_options',self::SLUG,
            [self::class,'page'],'dashicons-edit-page',27);
        foreach(self::sections() as $slug=>$label) {
            if($slug==='uebersicht'){
                add_submenu_page(self::SLUG,'Übersicht','Übersicht','manage_options',self::SLUG,[self::class,'page']);
                continue;
            }
            add_submenu_page(self::SLUG,$label,$label,'manage_options',self::SLUG.'-'.$slug,[self::class,'page']);
        }
    }
    private static function sections(): array {
        return ['uebersicht'=>'Übersicht','recherche'=>'Recherche','redaktion'=>'Redaktionsplan',
            'sofort'=>'Sofortartikel','titel'=>'Titelerstellung','k0'=>'K0-Export',
            'import'=>'Rückimport','diagnose'=>'Diagnose'];
    }
    private static function view(): string {
        $page=self::text($_GET['page']??self::SLUG);
        $view=str_starts_with($page,self::SLUG.'-')?substr($page,strlen(self::SLUG)+1):'uebersicht';
        return array_key_exists($view,self::sections())?$view:'uebersicht';
    }
    private static function sectionLink(string $view): string {
        return add_query_arg('page',$view==='uebersicht'?self::SLUG:self::SLUG.'-'.$view,admin_url('admin.php'));
    }
    private static function formStart(string $action,bool $file=false): void {
        echo '<form method="post" action="'.esc_url(admin_url('admin-post.php')).'"'.($file?' enctype="multipart/form-data"':'').'>';
        echo '<input type="hidden" name="action" value="txe_'.esc_attr($action).'">';
        echo '<input type="hidden" name="txe_return_view" value="'.esc_attr(self::view()).'">';
        wp_nonce_field('txe_'.$action);
    }
    public static function page(): void {
        if(!current_user_can('manage_options'))wp_die('Nicht erlaubt');
        $view=self::view();
        echo '<div class="wrap"><h1>Texterstellung <small style="font-size:13px">0.4.1 Originalrecherche – QA</small></h1>';
        if (!self::permitted()) {
            echo '<div class="notice notice-warning"><p><strong>Testmodus noch nicht freigeschaltet.</strong> Das Plugin ist installiert, aber es wird nichts recherchiert, exportiert oder importiert. Es sind keine WordPress-Konfigurationsänderungen erforderlich.</p></div>';
            echo '<h2>Diese Testinstallation einmalig bestätigen</h2><p>Prüfe die Adresse: <strong>'.esc_html(home_url('/')).'</strong>. Bestätige ausschließlich, wenn es sich um eine <strong>getrennte Testinstallation</strong> handelt. <strong>Niemals auf der Live-Website bestätigen.</strong></p>';
            echo '<form method="post" action="'.esc_url(admin_url('admin-post.php')).'">';
            echo '<input type="hidden" name="action" value="txe_testmode_confirm">';
            wp_nonce_field('txe_testmode_confirm');
            echo '<p><label><input type="checkbox" name="isolated_test_site" value="1" required> Ich bestätige: Diese WordPress-Installation ist ausschließlich zum Testen bestimmt.</label></p>';
            submit_button('Testmodus für diese Website freischalten', 'primary', 'submit', false);
            echo '</form></div>';
            return;
        }
        echo '<div class="notice notice-warning"><p><strong>Testmodus aktiv:</strong> Nur auf dieser bestätigten WordPress-Testinstallation verwenden. Kein Live-Betrieb. Website: '.esc_html(home_url('/')).'</p></div>';
        echo '<p>Ein Plugin, getrennte Worker: Recherche → einmalige Redaktion → externer Titel → K0 → Entwurfsimport. Keine alten Plugins werden verändert.</p>';
        echo '<nav class="nav-tab-wrapper" aria-label="Texterstellung Workflow">';
        foreach(self::sections() as $key=>$name) {
            echo '<a class="nav-tab '.($key===$view?'nav-tab-active':'').'" href="'.esc_url(self::sectionLink($key)).'">'.esc_html($name).'</a>';
        }
        echo '</nav>';
        if(isset($_GET['txe_notice']))echo '<div class="notice notice-info"><p>'.esc_html(sanitize_text_field(wp_unslash($_GET['txe_notice']))).'</p></div>';
        $s=self::state();
        $counts=[];foreach((array)$s['orders'] as $o){$k=(string)($o['status']??'UNBEKANNT');$counts[$k]=($counts[$k]??0)+1;}
        echo '<p><strong>Auftragsregal:</strong> '.count((array)$s['orders']).' · '.esc_html(wp_json_encode($counts)).'</p>';
        if($view==='uebersicht') {
            echo '<h2>Workflowübersicht</h2><p>Der spätere Ablauf ist hier in einem Plugin zusammengeführt. Jede Station ist links separat anwählbar.</p>';
            echo '<ol><li>Recherche: Original-Recherche samt Google-Fragen und SEO ausführen</li><li>Redaktionsplan: einmal entscheiden und Lücken in Kategorien sehen</li><li>Sofortartikel: Themen direkt ins Regal legen</li><li>Titelerstellung: Datei extern bearbeiten lassen</li><li>K0-Export: bis 50 freigegebene Themen reservieren und exportieren</li><li>Rückimport: K0-Texte als WordPress-Entwürfe einspielen</li><li>Diagnose: Fehlerbelege als JSON herunterladen</li></ol>';
            echo '<p><strong>Testgrenze:</strong> Recherche/Google-Fragen/SEO-Entscheidung kommen vollständig aus der unveränderten PSTE-Originalengine. Ein echter Ende-zu-Ende-Test steht aus. K0 bleibt extern.</p>';
            echo '<p><a class="button button-primary" href="'.esc_url(self::sectionLink('recherche')).'">Workflow starten</a> <a class="button" href="'.esc_url(self::sectionLink('diagnose')).'">Diagnose öffnen</a></p>';
        }
        if($view==='recherche') {
            echo '<h2>Originalrecherche PSTE</h2><p>DataForSEO, Google-Fragen, Kostenschutz und automatische Redaktion laufen ausschließlich über den unveränderten PSTE-Worker.</p>';
            echo '<p><a class="button" href="'.esc_url(admin_url('admin.php?page=portal-seo-topic-engine-settings')).'">Bestehende Recherche-Einstellungen / Migration</a></p>';
            if(!PSTE_Plugin::isReady()) echo '<div class="notice notice-warning"><p>Die originale PSTE-Migration ist noch nicht abgeschlossen. Bestehende Daten werden nicht verändert.</p></div>';
            self::formStart('credentials_save');
            echo '<p><input name="login" autocomplete="off" placeholder="DataForSEO Login" required> <input type="password" name="password" autocomplete="new-password" placeholder="Passwort" required></p>';
            submit_button('Zugangsdaten der Originalengine speichern','secondary','submit',false);echo '</form>';
            self::formStart('research');
            echo '<p>Ausgangsbegriff: <input required name="seed" placeholder="z.B. Pferdedecken"> Kategorie: <select name="category_id">';
            foreach((array)get_categories(['hide_empty'=>false]) as $term) echo '<option value="'.(int)$term->term_id.'">'.esc_html($term->name).'</option>';
            echo '</select> <label><input type="checkbox" name="cost_ack" value="1" required> Kostenpflichtige Originalrecherche starten</label></p>';
            submit_button('Originalrecherche starten','primary','submit',false);echo '</form>';
            if(PSTE_Plugin::isReady()){
                $original=self::originalTopicPool();
                echo '<h3>Bereits gespeicherte Originaldaten: '.(int)$original['total'].' Themen</h3>';
                $job=$original['job'];
                if(is_array($job))echo '<p>Aktueller Originalauftrag: '.esc_html((string)($job['status']??'UNBEKANNT')).'</p>';
                echo '<table class="widefat striped"><thead><tr><th>Thema</th><th>Gespeicherter Status</th><th>Kategorie</th></tr></thead><tbody>';
                foreach((array)($original['page']['items']??[]) as $item){
                    echo '<tr><td>'.esc_html(PSTE_Editorializer::sourceQuery($item)).'</td><td>'.esc_html((string)($item['pool_status']??'')).'</td><td>'.esc_html((string)($item['target_category_name']??'')).'</td></tr>';
                }
                echo '</tbody></table>';
            }
        }
        if($view==='redaktion') {
            echo '<h2>Originalredaktion (einziger SEO-Entscheider)</h2>';
            echo '<p><a class="button" href="'.esc_url(admin_url('admin.php?page=portal-seo-topic-engine-review')).'">Original-Themenprüfung öffnen</a></p>';
            if(PSTE_Plugin::isReady()){
                $count=PSTE_Repository::topicPoolCount();
                echo '<p>Gespeicherter Keyword-Pool: <strong>'.(int)$count.'</strong> Themen. Bestehende Entscheidungen bleiben im Originalspeicher.</p>';
                $coverage=PSTE_Analytics::coverage();
                echo '<table class="widefat striped"><thead><tr><th>Kategoriefamilie</th><th>Veröffentlicht</th><th>Geplant</th><th>Suchnachfrage</th></tr></thead><tbody>';
                foreach(array_slice($coverage,0,50) as $r)echo '<tr><td>'.esc_html((string)($r['category_name']??'')).'</td><td>'.(int)($r['published']??0).'</td><td>'.(int)($r['planned_pass']??0).'</td><td>'.esc_html((string)($r['candidate_volume']??0)).'</td></tr>';
                echo '</tbody></table>';
            }
            echo '<h3>Bereits freigegebene Altthemen übertragen</h3><p>Nur bestehende FREI-Entscheidungen, ohne neue fachliche Prüfung. Unvollständige Themen bleiben gesperrt.</p>';
            self::formStart('load_legacy');submit_button('Bestehende FREI-Freigaben übernehmen','secondary','submit',false);echo '</form>';
            echo '<h3>Vorhandenen K0-Auftrag einlesen</h3>';
            self::formStart('import_queue',true);echo '<input type="file" name="queue_file" accept=".json,application/json" required>';
            submit_button('Bestehenden Auftrag einlesen','secondary','submit',false);echo '</form>';
        }
        if($view==='titel') {
        echo '<h2>3. Externe Titelrunde – Originalformat</h2><p>Nur fest freigegebene Suchabsichten ohne Titel. Der externe Titelworker darf ausschließlich das Titelfeld ausfüllen.</p>';
        self::formStart('export_titles');echo 'Anzahl: <input type="number" name="count" min="1" max="50" value="20">';submit_button('Titeldatei exportieren','secondary','submit',false);echo '</form>';
        self::formStart('import_titles',true);echo '<input type="file" name="title_file" accept=".json,application/json" required>';submit_button('Titeldatei zurücknehmen','secondary','submit',false);echo '</form>';
        echo '<h2>Externen Titel einem wartenden Sofortauftrag zuordnen</h2>';
        self::formStart('title_return');echo '<input name="order_id" placeholder="Auftragsnummer" required> <input name="title" placeholder="Extern fertiggestellter Titel" required>';submit_button('Nur Titel zuordnen','secondary','submit',false);echo '</form>';
        }
        if($view==='sofort') {
        echo '<h2>Sofortartikel – einmalige redaktionelle Vorgabe</h2><p>Sofortartikel werden im selben Auftragsregal wie recherchierte Themen gespeichert.</p>';
        self::formStart('quick');
        echo '<p>Keyword: <input required name="keyword"> Titel (falls extern bereits vorhanden): <input name="title"></p>';
        echo '<p>Kategorie: <select name="category">';foreach((array)get_categories(['hide_empty'=>false]) as $c)echo '<option value="'.esc_attr($c->slug).'">'.esc_html($c->name).'</option>';echo '</select> Artikelart: <input name="article_type" required placeholder="z.B. Beratung"> Suchabsicht: <input name="intent" placeholder="z.B. Erklärung"></p>';
        submit_button('Freigegebenen Sofortauftrag in dieselbe Themenliste aufnehmen');echo '</form>';
        }
        if($view==='k0') {
        echo '<h2>Chargenexport zu K0</h2>';
        self::formStart('export');echo '<label>Anzahl <input type="number" name="count" value="20" min="1" max="50"></label> ';submit_button('Freie Aufträge entnehmen und JSON exportieren','primary','submit',false);echo '</form>';
        self::formStart('redownload');submit_button('Letzte reservierte Datei erneut herunterladen','secondary','submit',false);echo '</form>';
        $batches=[];foreach($s['orders'] as $o)if(!empty($o['batch']))$batches[$o['batch']]=true;
        if($batches){self::formStart('redownload_batch');echo '<label>Frühere Charge erneut herunterladen: <select name="batch_hash">';
            foreach(array_keys($batches) as $sha)echo '<option value="'.esc_attr($sha).'">'.esc_html(substr($sha,0,16)).'</option>';
            echo '</select></label>';submit_button('Diese vorhandene Charge herunterladen','secondary','submit',false);echo '</form>';}

        }
        if($view==='import') {
        echo '<h2>Unveränderte K0-Rückgabedatei als Entwurf importieren</h2>';
        self::formStart('import_drafts',true);echo '<input type="file" name="draft_file" accept=".json,application/json" required>';submit_button('Technisch zuordnen und als Entwurf importieren');echo '</form>';
        }
        if($view==='uebersicht') {
        echo '<h2>Auftragsübersicht nach Kategorie und Status</h2><p>Keine neue Qualitätsentscheidung.</p><table class="widefat striped"><thead><tr><th>Auftrag</th><th>Kategorie</th><th>Keyword</th><th>Status</th><th>Entwurf</th></tr></thead><tbody>';
        foreach(array_slice($s['orders'],-100,100,true) as $o){echo '<tr><td>'.esc_html($o['id']).'</td><td>'.esc_html($o['category']).'</td><td>'.esc_html($o['target_keyword']).'</td><td>'.esc_html($o['status']).'</td><td>'.esc_html((string)$o['post_id']).'</td></tr>';}
        echo '</tbody></table>';
        }
        if($view==='diagnose') {
            TXE_Diagnose::summaryHtml();
        }
        echo '</div>';
    }
}
register_activation_hook(__FILE__, [TXE_Workshop::class,'activate']);
add_action('plugins_loaded',[TXE_Workshop::class,'init']);
