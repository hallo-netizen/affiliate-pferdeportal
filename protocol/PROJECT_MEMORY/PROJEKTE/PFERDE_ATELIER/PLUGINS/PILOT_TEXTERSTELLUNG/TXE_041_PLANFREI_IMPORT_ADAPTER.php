<?php
if (!defined('ABSPATH')) { return; }

/**
 * Finished article package -> WordPress draft importer.
 *
 * Core rule: the importer owns only WordPress draft creation, exact article assignment
 * and editorial-runtime readback. Upstream proof metadata (LT/PPM/test/signing payloads)
 * is deliberately not a second quality gate here.
 */
final class PSERC_System4_Import {
    public const ACTION='pserc_import_system4_drafts';
    public const NONCE_ACTION='pserc_import_system4_drafts_nonce';
    public const LEGACY_7_CONTRACT='SYSTEM4_7_ARTICLE_CHAT_HANDOFF_V1';
    public const LEGACY_CONTRACT='SYSTEM4_WORDPRESS_HANDOFF_V1';
    public const CONTRACT='PFERDE_ATELIER_WORDPRESS_IMPORT_V1';
    public const RESULT_CONTRACT='PSERC_SYSTEM4_WORDPRESS_IMPORT_RESULT_V1';
    private const MAX_PACKAGE_BYTES=12582912;
    private const POST_STATUSES=['publish','draft','pending','private','future'];
    private static array $categoryCache=[];
    private static ?array $collisionIndex=null;

    public static function init(): void {
        if(function_exists('add_action'))add_action('admin_post_'.self::ACTION,[self::class,'handle']);
    }

    public static function renderPanel(): void {
        $action=function_exists('admin_url')?admin_url('admin-post.php'):'admin-post.php';
        echo '<hr id="pserc-system4-import"><h2>Artikel → WordPress-Entwürfe</h2>';
        echo '<div class="notice notice-info inline"><p><strong>Direktimport '.esc_html(defined('PSERC_BUILD')?PSERC_BUILD:'UNKNOWN').':</strong> Importiert fertige Artikel als Entwürfe und verbucht ihre Planplätze anschließend im bestehenden PPM-6.7.9-Redaktionsplan. Neue schlanke Importdateien und die bisherigen System-4-Dateien werden akzeptiert. Veröffentlichung bleibt gesperrt.</p></div>';
        echo '<form method="post" enctype="multipart/form-data" action="'.esc_url($action).'">';
        echo '<input type="hidden" name="action" value="'.esc_attr(self::ACTION).'">';
        if(function_exists('wp_nonce_field'))wp_nonce_field(self::NONCE_ACTION);
        echo '<p><label for="pserc-system4-package"><strong>Artikeldatei (.json)</strong></label><br><input id="pserc-system4-package" type="file" name="pserc_system4_package" accept="application/json,.json" required></p>';
        if(function_exists('submit_button'))submit_button('Artikeldatei prüfen &amp; Entwürfe importieren','primary','submit',false);else echo '<button type="submit">Artikeldatei prüfen &amp; Entwürfe importieren</button>';
        echo '</form>';
    }

    public static function handle(): void {
        if(!function_exists('current_user_can')||!current_user_can('manage_options'))self::emit(self::blocked('PSERC_SYSTEM4_CAPABILITY_BLOCKED'));
        if(function_exists('check_admin_referer'))check_admin_referer(self::NONCE_ACTION);else self::emit(self::blocked('PSERC_SYSTEM4_NONCE_API_MISSING'));
        self::emit(self::importPayload(self::decodeUpload()));
    }

    /** Testable import core. No dependency on PSERC plan/snapshot rebuild state. */
    public static function importPayload(array $payload): array {
        $normalized=self::normalizePayload($payload);
        if(empty($normalized['ok']))return $normalized;
        $rows=(array)$normalized['rows'];
        $sourceContract=(string)$normalized['source_contract'];
        $batchSha=(string)$normalized['batch_sha256'];
        // No separate editorial production plan: the existing order/WordPress readback is authoritative.

        // One full preflight before the first WordPress write.
        $prepared=[];
        foreach($rows as $i=>$row){
            $category=self::resolveCategory((string)$row['category']);
            if(empty($category['ok']))return self::blocked((string)$category['reason'],['index'=>$i,'category'=>(string)$row['category']]);
            $duplicate=self::findCollision((string)$row['plan_slot'],(string)$row['slug'],(string)$row['title']);
            if($duplicate!==null){
                if(($duplicate['type']??'')!=='plan_slot')return self::blocked('PSERC_SYSTEM4_WORDPRESS_COLLISION',['index'=>$i,'collision'=>$duplicate]);
                $existing=self::classifyPlanSlotCollision((int)($duplicate['post_id']??0),$row,(int)$category['term_id']);
                if(empty($existing['ok']))return self::blocked('PSERC_SYSTEM4_WORDPRESS_COLLISION',['index'=>$i,'collision'=>array_merge($duplicate,['existing'=>$existing])]);
                $prepared[]=['row'=>$row,'term_id'=>(int)$category['term_id'],'existing'=>$existing];
                continue;
            }
            $prepared[]=['row'=>$row,'term_id'=>(int)$category['term_id'],'existing'=>null];
        }

        $created=[];$existingFulfilled=[];$existingReused=[];$readback=[];
        foreach($prepared as $i=>$item){
            $row=(array)$item['row'];$termId=(int)$item['term_id'];$existing=is_array($item['existing']??null)?(array)$item['existing']:null;
            if($existing!==null){
                $postId=(int)$existing['post_id'];$status=(string)$existing['post_status'];$contentHash=(string)$existing['content_sha256'];
                $rb=['ok'=>true,'post_id'=>$postId,'post_status'=>$status,'plan_slot'=>(string)$row['plan_slot'],'article_id'=>(string)$row['article_id'],'content_sha256'=>$contentHash,'category_term_id'=>$termId,'existing_mode'=>(string)$existing['mode'],'publish_allowed'=>false];
                $readback[]=$rb;
                if($existing['mode']==='PUBLISHED_SLOT_ALREADY_FULFILLED')$existingFulfilled[]=$postId;else $existingReused[]=$postId;
                continue;
            }

            $meta=self::postMeta($row,$sourceContract,$batchSha);
            $postarr=[
                'post_title'=>(string)$row['title'],
                'post_content'=>(string)$row['body'],
                'post_name'=>(string)$row['slug'],
                'post_status'=>'draft',
                'post_type'=>'post',
                'post_category'=>[$termId],
                'meta_input'=>$meta,
            ];
            if(!function_exists('wp_insert_post')){self::rollback($created);return self::blocked('PSERC_SYSTEM4_WORDPRESS_INSERT_API_MISSING',['rolled_back_count'=>count($created)]);}
            $postId=wp_insert_post(function_exists('wp_slash')?wp_slash($postarr):$postarr,true);
            if((function_exists('is_wp_error')&&is_wp_error($postId))||(int)$postId<=0){self::rollback($created);return self::blocked('PSERC_SYSTEM4_WORDPRESS_INSERT_FAILED',['index'=>$i,'rolled_back_count'=>count($created)]);}
            $postId=(int)$postId;$created[]=$postId;
            $rb=self::readback($postId,$row,$termId,$meta);
            if(empty($rb['ok'])){self::rollback($created);return self::blocked('PSERC_SYSTEM4_WORDPRESS_READBACK_MISMATCH',['index'=>$i,'readback'=>$rb,'rolled_back_count'=>count($created)]);}
            $readback[]=$rb;
        }


        return [
            'ok'=>true,'contract'=>self::RESULT_CONTRACT,'status'=>'PSERC_SYSTEM4_WORDPRESS_DRAFT_IMPORT_PASS',
            'source_contract'=>$sourceContract,'input_mode'=>(string)$normalized['input_mode'],'batch_sha256'=>$batchSha,'article_count'=>count($prepared),
            'created_post_ids'=>$created,'existing_fulfilled_post_ids'=>$existingFulfilled,'existing_reused_post_ids'=>$existingReused,
            'readback'=>$readback,'redaktionsplan_runtime_sync'=>null,'redaktionsplan_read_attempted'=>false,'redaktionsplan_write_attempted'=>false,
            'publish_allowed'=>false,'plugin_version'=>defined('PSERC_VERSION')?(string)PSERC_VERSION:'UNKNOWN','plugin_build'=>defined('PSERC_BUILD')?(string)PSERC_BUILD:'UNKNOWN',
        ];
    }

    /** Normalize both old proof-heavy packages and the new compact article package into one small internal shape. */
    public static function normalizePayload(array $payload): array {
        $contract=trim((string)($payload['contract']??''));
        if(!in_array($contract,[self::CONTRACT,self::LEGACY_CONTRACT,self::LEGACY_7_CONTRACT],true))return self::blocked('PSERC_SYSTEM4_CONTRACT_INVALID',['actual'=>$contract]);
        $rawRows=$payload['articles']??null;if(!is_array($rawRows)||count($rawRows)<1)return self::blocked('PSERC_SYSTEM4_ARTICLES_EMPTY');
        $compact=$contract===self::CONTRACT;$rows=[];$seenSlots=[];$seenSlugs=[];$seenIds=[];
        foreach(array_values($rawRows) as $i=>$raw){
            if(!is_array($raw))return self::blocked('PSERC_SYSTEM4_ARTICLE_INVALID',['index'=>$i]);
            if($compact){
                $articleId=trim((string)($raw['article_id']??''));
                $slug=trim((string)($raw['slug']??''));
            }else{
                $pc=is_array($raw['production_context']??null)?(array)$raw['production_context']:[];
                $pi=is_array($pc['production_plan_item']??null)?(array)$pc['production_plan_item']:[];
                $runtime=is_array($pi['runtime_order']??null)?(array)$pi['runtime_order']:[];
                $articleId=trim((string)($pi['canonical_article_id']??''));
                $slug=trim((string)($runtime['slug']??''));
            }
            $row=[
                'article_id'=>$articleId,'plan_slot'=>trim((string)($raw['plan_slot']??'')),'title'=>trim((string)($raw['title']??'')),
                'slug'=>$slug,'target_keyword'=>trim((string)($raw['target_keyword']??'')),'category'=>trim((string)($raw['category']??'')),
                'article_type'=>trim((string)($raw['article_type']??'')),'body'=>(string)($raw['body']??''),
            ];
            foreach(['article_id','plan_slot','title','slug','target_keyword','category','article_type','body'] as $field)if(trim((string)$row[$field])==='')return self::blocked('PSERC_SYSTEM4_ARTICLE_FIELD_INVALID',['index'=>$i,'field'=>$field]);
            if(!self::sha($row['plan_slot']))return self::blocked('PSERC_SYSTEM4_PLAN_SLOT_INVALID',['index'=>$i]);
            try{$expected=PSERC_Plan_Slot_Identity::tokenFromCanonicalId($row['article_id']);}catch(Throwable $e){return self::blocked('PSERC_SYSTEM4_CANONICAL_ARTICLE_ID_INVALID',['index'=>$i]);}
            if(!hash_equals($expected,$row['plan_slot']))return self::blocked('PSERC_SYSTEM4_CANONICAL_PLAN_SLOT_MISMATCH',['index'=>$i]);
            $sanitized=function_exists('sanitize_title')?(string)sanitize_title($row['slug']):self::fallbackSanitizeTitle($row['slug']);
            if($sanitized!==$row['slug'])return self::blocked('PSERC_SYSTEM4_POST_SLUG_NOT_CANONICAL',['index'=>$i,'slug'=>$row['slug'],'sanitized'=>$sanitized]);
            if(isset($seenSlots[$row['plan_slot']]))return self::blocked('PSERC_SYSTEM4_PLAN_SLOT_DUPLICATE',['index'=>$i]);$seenSlots[$row['plan_slot']]=true;
            if(isset($seenSlugs[$row['slug']]))return self::blocked('PSERC_SYSTEM4_POST_SLUG_DUPLICATE',['index'=>$i]);$seenSlugs[$row['slug']]=true;
            if(isset($seenIds[$row['article_id']]))return self::blocked('PSERC_SYSTEM4_ARTICLE_ID_DUPLICATE',['index'=>$i]);$seenIds[$row['article_id']]=true;
            $row['content_sha256']=hash('sha256',$row['body']);$rows[]=$row;
        }
        $canonical=['contract'=>self::CONTRACT,'articles'=>$rows];
        $batchSha=PSERC_Stable_Json::hash($canonical);
        return ['ok'=>true,'status'=>'PSERC_SYSTEM4_PAYLOAD_VALID','rows'=>$rows,'article_count'=>count($rows),'source_contract'=>$contract,'input_mode'=>$compact?'COMPACT_V1':'LEGACY_COMPATIBILITY','batch_sha256'=>$batchSha,'publish_allowed'=>false];
    }

    private static function postMeta(array $row,string $sourceContract,string $batchSha): array {
        return [
            '_pserc_system4_import'=>'1',
            '_pserc_system4_contract'=>$sourceContract,
            '_pserc_system4_batch_sha256'=>$batchSha,
            '_pserc_system4_plan_slot'=>(string)$row['plan_slot'],
            '_pserc_import_article_id'=>(string)$row['article_id'],
            '_pserc_system4_content_sha256'=>(string)$row['content_sha256'],
            '_pserc_system4_article_type'=>(string)$row['article_type'],
            '_pserc_system4_target_keyword'=>(string)$row['target_keyword'],
            '_pserc_publish_blocked'=>'1',
            '_ppm679_normal_draft'=>'1',
            '_ppm679_canonical_article_id'=>(string)$row['article_id'],
            '_ppm679_plan_slot_sha256'=>(string)$row['plan_slot'],
            '_ppm679_content_hash'=>(string)$row['content_sha256'],
            '_ppm679_article_type'=>(string)$row['article_type'],
            '_ppm679_publish_blocked'=>'1',
            '_ppm679_category_slug'=>(string)$row['category'],
        ];
    }

    private static function resolveCategory(string $slug): array {
        if(isset(self::$categoryCache[$slug]))return self::$categoryCache[$slug];
        $term=function_exists('get_term_by')?get_term_by('slug',$slug,'category'):false;
        if(!is_object($term)||!isset($term->term_id)||(int)$term->term_id<=0)return self::$categoryCache[$slug]=['ok'=>false,'reason'=>'PSERC_SYSTEM4_CATEGORY_NOT_FOUND'];
        if((string)($term->slug??'')!==$slug)return self::$categoryCache[$slug]=['ok'=>false,'reason'=>'PSERC_SYSTEM4_CATEGORY_IDENTITY_MISMATCH'];
        return self::$categoryCache[$slug]=['ok'=>true,'term_id'=>(int)$term->term_id];
    }

    private static function classifyPlanSlotCollision(int $postId,array $row,int $termId): array {
        if($postId<=0||!function_exists('get_post')||!function_exists('get_post_meta'))return ['ok'=>false,'reason'=>'EXISTING_POST_READ_UNAVAILABLE','post_id'=>$postId];
        $post=get_post($postId,ARRAY_A);if(!is_array($post))return ['ok'=>false,'reason'=>'EXISTING_POST_MISSING','post_id'=>$postId];
        $storedSlot=self::firstMeta($postId,['_pserc_system4_plan_slot','_ppm679_plan_slot_sha256']);
        if($storedSlot===''||!hash_equals($storedSlot,(string)$row['plan_slot']))return ['ok'=>false,'reason'=>'EXISTING_SLOT_NOT_BOUND','post_id'=>$postId];
        $storedId=self::firstMeta($postId,['_pserc_import_article_id','_ppm679_canonical_article_id']);
        if($storedId!==''&&!hash_equals($storedId,(string)$row['article_id']))return ['ok'=>false,'reason'=>'EXISTING_SLOT_ARTICLE_ID_CONFLICT','post_id'=>$postId,'existing_article_id'=>$storedId];
        $status=(string)($post['post_status']??'');$contentHash=hash('sha256',(string)($post['post_content']??''));
        if($status==='publish')return ['ok'=>true,'mode'=>'PUBLISHED_SLOT_ALREADY_FULFILLED','post_id'=>$postId,'post_status'=>$status,'content_sha256'=>$contentHash];
        if($status==='draft'&&hash_equals($contentHash,(string)$row['content_sha256'])&&(string)($post['post_title']??'')===(string)$row['title']&&(string)($post['post_name']??'')===(string)$row['slug']){
            $cats=function_exists('wp_get_post_categories')?array_values(array_map('intval',(array)wp_get_post_categories($postId))):[];sort($cats);$expected=[$termId];sort($expected);
            if($cats!==$expected)return ['ok'=>false,'reason'=>'EXISTING_DRAFT_CATEGORY_DRIFT','post_id'=>$postId];
            return ['ok'=>true,'mode'=>'IDENTICAL_DRAFT_REUSED','post_id'=>$postId,'post_status'=>$status,'content_sha256'=>$contentHash];
        }
        return ['ok'=>false,'reason'=>'EXISTING_SLOT_CONTENT_OR_STATUS_CONFLICT','post_id'=>$postId,'post_status'=>$status,'existing_content_sha256'=>$contentHash,'incoming_content_sha256'=>(string)$row['content_sha256']];
    }

    private static function firstMeta(int $postId,array $keys): string {foreach($keys as $key){$v=(string)get_post_meta($postId,(string)$key,true);if($v!=='')return $v;}return '';}

    /** @return array<string,mixed>|null */
    private static function findCollision(string $slot,string $slug,string $title): ?array {
        $index=self::collisionIndex();
        if(isset($index['slot'][$slot]))return ['type'=>'plan_slot','value'=>$slot,'post_id'=>(int)$index['slot'][$slot]];
        if(isset($index['slug'][$slug]))return ['type'=>'slug','value'=>$slug,'post_id'=>(int)$index['slug'][$slug]];
        $needle=function_exists('sanitize_title')?(string)sanitize_title($title):self::fallbackSanitizeTitle($title);
        if($needle!==''&&isset($index['title'][$needle]))return ['type'=>'title','value'=>$title,'post_id'=>(int)$index['title'][$needle]];
        return null;
    }

    /** Build one read-only collision index for the whole import instead of rescanning WordPress per article. */
    private static function collisionIndex(): array {
        if(self::$collisionIndex!==null)return self::$collisionIndex;
        $out=['slot'=>[],'slug'=>[],'title'=>[]];global $wpdb;$rows=null;
        if(isset($wpdb)&&is_object($wpdb)&&!empty($wpdb->posts)&&!empty($wpdb->postmeta)&&method_exists($wpdb,'get_results')){
            $statusSql="'".implode("','",array_map(static fn($v)=>str_replace("'","''",$v),self::POST_STATUSES))."'";
            $sql="SELECT p.ID,p.post_title,p.post_name,pm.meta_key,pm.meta_value FROM {$wpdb->posts} p LEFT JOIN {$wpdb->postmeta} pm ON pm.post_id=p.ID AND pm.meta_key IN ('_pserc_system4_plan_slot','_ppm679_plan_slot_sha256') WHERE p.post_type='post' AND p.post_status IN ({$statusSql}) ORDER BY p.ID ASC";
            $rows=$wpdb->get_results($sql,defined('ARRAY_A')?ARRAY_A:'ARRAY_A');
        }
        if(is_array($rows)){
            foreach($rows as $row){
                if(is_object($row))$row=(array)$row;$id=(int)($row['ID']??0);if($id<=0)continue;
                $slug=(string)($row['post_name']??'');if($slug!==''&&!isset($out['slug'][$slug]))$out['slug'][$slug]=$id;
                $title=function_exists('sanitize_title')?(string)sanitize_title((string)($row['post_title']??'')):self::fallbackSanitizeTitle((string)($row['post_title']??''));if($title!==''&&!isset($out['title'][$title]))$out['title'][$title]=$id;
                $slot=(string)($row['meta_value']??'');if(in_array((string)($row['meta_key']??''),['_pserc_system4_plan_slot','_ppm679_plan_slot_sha256'],true)&&self::sha($slot)&&!isset($out['slot'][$slot]))$out['slot'][$slot]=$id;
            }
        }elseif(function_exists('get_posts')){
            $ids=get_posts(['post_type'=>'post','post_status'=>self::POST_STATUSES,'numberposts'=>-1,'fields'=>'ids','suppress_filters'=>true]);
            foreach((array)$ids as $postId){
                $postId=(int)$postId;$post=function_exists('get_post')?get_post($postId,ARRAY_A):null;if(!is_array($post))continue;
                $slug=(string)($post['post_name']??'');if($slug!==''&&!isset($out['slug'][$slug]))$out['slug'][$slug]=$postId;
                $title=function_exists('sanitize_title')?(string)sanitize_title((string)($post['post_title']??'')):self::fallbackSanitizeTitle((string)($post['post_title']??''));if($title!==''&&!isset($out['title'][$title]))$out['title'][$title]=$postId;
                $slot=self::firstMeta($postId,['_pserc_system4_plan_slot','_ppm679_plan_slot_sha256']);if(self::sha($slot)&&!isset($out['slot'][$slot]))$out['slot'][$slot]=$postId;
            }
        }
        return self::$collisionIndex=$out;
    }

    private static function readback(int $postId,array $row,int $termId,array $meta): array {
        $post=function_exists('get_post')?get_post($postId,ARRAY_A):null;if(!is_array($post))return ['ok'=>false,'reason'=>'POST_MISSING','post_id'=>$postId];
        $mismatches=[];
        if((string)($post['post_status']??'')!=='draft')$mismatches[]='post_status';
        if((string)($post['post_type']??'')!=='post')$mismatches[]='post_type';
        if((string)($post['post_title']??'')!==(string)$row['title'])$mismatches[]='post_title';
        if((string)($post['post_name']??'')!==(string)$row['slug'])$mismatches[]='post_name';
        if(!hash_equals((string)$row['content_sha256'],hash('sha256',(string)($post['post_content']??''))))$mismatches[]='post_content_sha256';
        $cats=function_exists('wp_get_post_categories')?array_values(array_map('intval',(array)wp_get_post_categories($postId))):[];sort($cats);$expected=[$termId];sort($expected);if($cats!==$expected)$mismatches[]='post_category';
        foreach(['_pserc_system4_plan_slot','_pserc_import_article_id','_pserc_system4_article_type','_pserc_system4_target_keyword','_ppm679_canonical_article_id','_ppm679_plan_slot_sha256','_ppm679_publish_blocked'] as $key){$actual=function_exists('get_post_meta')?get_post_meta($postId,$key,true):null;if((string)$actual!==(string)($meta[$key]??''))$mismatches[]='meta:'.$key;}
        if($mismatches)return ['ok'=>false,'reason'=>'READBACK_MISMATCH','post_id'=>$postId,'mismatches'=>$mismatches];
        return ['ok'=>true,'post_id'=>$postId,'post_status'=>'draft','plan_slot'=>(string)$row['plan_slot'],'article_id'=>(string)$row['article_id'],'content_sha256'=>(string)$row['content_sha256'],'category_term_id'=>$termId,'publish_allowed'=>false];
    }

    /** @param list<int> $postIds */
    private static function rollback(array $postIds): void {if(!function_exists('wp_delete_post'))return;foreach(array_reverse($postIds) as $postId)wp_delete_post((int)$postId,true);}

    private static function decodeUpload(): array {
        $file=isset($_FILES['pserc_system4_package'])&&is_array($_FILES['pserc_system4_package'])?$_FILES['pserc_system4_package']:[];$tmp=(string)($file['tmp_name']??'');$size=(int)($file['size']??0);
        if($tmp===''||!is_file($tmp)||$size<1||$size>self::MAX_PACKAGE_BYTES)self::emit(self::blocked('PSERC_SYSTEM4_UPLOAD_INVALID',['size'=>$size,'max_bytes'=>self::MAX_PACKAGE_BYTES]));
        try{$payload=json_decode((string)file_get_contents($tmp),true,512,JSON_THROW_ON_ERROR);}catch(Throwable $e){self::emit(self::blocked('PSERC_SYSTEM4_UPLOAD_JSON_INVALID'));}
        if(!is_array($payload))self::emit(self::blocked('PSERC_SYSTEM4_UPLOAD_JSON_INVALID'));return $payload;
    }

    private static function fallbackSanitizeTitle(string $value): string {$value=function_exists('mb_strtolower')?mb_strtolower($value,'UTF-8'):strtolower($value);$value=preg_replace('/[^a-z0-9äöüß]+/u','-',$value);return trim((string)$value,'-');}
    private static function sha(string $value): bool{return (bool)preg_match('/^[a-f0-9]{64}$/',$value);}
    private static function blocked(string $reason,array $extra=[]): array{return array_merge(['ok'=>false,'contract'=>self::RESULT_CONTRACT,'status'=>'PSERC_SYSTEM4_WORDPRESS_IMPORT_BLOCKED','reason_codes'=>[$reason],'redaktionsplan_read_attempted'=>false,'redaktionsplan_write_attempted'=>false,'publish_allowed'=>false,'plugin_version'=>defined('PSERC_VERSION')?(string)PSERC_VERSION:'UNKNOWN','plugin_build'=>defined('PSERC_BUILD')?(string)PSERC_BUILD:'UNKNOWN'],$extra);}
    private static function emit(array $payload): void {$payload['emitted_at_utc']=gmdate('c');$payload['result_sha256']=PSERC_Stable_Json::hash($payload);if(!headers_sent()){if(function_exists('nocache_headers'))nocache_headers();header('Content-Type: application/json; charset=utf-8');header('Content-Disposition: attachment; filename="pserc-system4-import-result-'.substr((string)$payload['result_sha256'],0,16).'.json"');}echo function_exists('wp_json_encode')?wp_json_encode($payload,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES|JSON_PRETTY_PRINT|JSON_PRESERVE_ZERO_FRACTION):json_encode($payload,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES|JSON_PRETTY_PRINT|JSON_PRESERVE_ZERO_FRACTION);exit;}
}
