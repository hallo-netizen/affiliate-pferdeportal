<?php
/**
 * Robotik V63: one guarded write path for the verified, non-HOLD V62 delta.
 * 16 disputed type pages and their 48 categories are NEVER written by this release.
 * No API, Cron, publication, deletion, existing-object edits, or navigation changes.
 */
if (!defined('ABSPATH')) { exit; }

final class Robotik_V63_Delta {
    private const STATE = 'robotik_v63_delta_state';
    private const LOCK = 'robotik_v63_delta_lock';
    private const MARKER = '_robotik_kategorie_node_id';
    private const BATCH = 8;
    private const EXPECTED_PAGES = 68;
    private const EXPECTED_TERMS = 159;
    private const EXPECTED_HOLDS = 16;
    private const EXPECTED_HELD_TERMS = 48;

    public static function boot(): void {
        add_action('admin_menu',[self::class,'menu'],32);
        add_action('admin_post_robotik_v63_delta_start',[self::class,'start']);
        add_action('wp_ajax_robotik_v63_delta_tick',[self::class,'ajax_tick']);
        add_action('admin_post_robotik_v63_delta_result',[self::class,'export']);
    }
    public static function menu(): void {
        add_submenu_page('robotik-kategorie','Robotik – geprüfte Gesamtübernahme','Gesamtübernahme (geschützt)',
            'manage_options','robotik-v63-delta',[self::class,'screen']);
    }
    private static function authorized(): void {
        if(!current_user_can('manage_options'))throw new RuntimeException('Administratorrechte fehlen.');
    }
    private static function key(array $path): string {
        return implode(' / ',array_map(static fn($v):string => trim((string)$v),$path));
    }
    private static function seal(array $source,array $inventory,array $comparison):string {
        $pages=[];
        foreach((array)$inventory['pages']['items'] as $p){
            $id=(int)$p['id'];$pages[]=[$id,(int)$p['parent_id'],(string)$p['title'],(string)$p['slug'],(string)$p['status'],
                (string)get_post_meta($id,self::MARKER,true)];
        }
        $terms=[];
        foreach((array)$inventory['categories']['items'] as $t){
            $id=(int)$t['id'];$terms[]=[$id,(int)$t['parent_id'],(string)$t['name'],(string)$t['slug'],
                (string)get_term_meta($id,self::MARKER,true),(string)get_term_meta($id,'_robotik_product_page_id',true)];
        }
        usort($pages,static fn($a,$b)=>$a[0]<=>$b[0]);usort($terms,static fn($a,$b)=>$a[0]<=>$b[0]);
        return hash('sha256',wp_json_encode([
            'manifest_sha256'=>hash_file('sha256',__DIR__.'/../assets/robotik-v62-sollvorschau.json'),
            'site_url'=>$inventory['site_url'], 'pages'=>$pages,'terms'=>$terms,
            'comparisons'=>$comparison['comparison_counts'],
        ],JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES));
    }
    /** One central WP-inventory reading + one central comparison, shared by preview, start and checks. */
    public static function prepare():array {
        self::authorized();
        $source=Robotik_Kategorie_Gesamtvorschau::source();
        $inventory=Robotik_Kategorie_Inventory::collect();
        $cmp=Robotik_Kategorie_Gesamtvorschau::collect($inventory,$source);
        $errors=[];
        if(empty($cmp['site_inventory_complete']))$errors[]='WordPress-Bestandsaufnahme unvollstaendig.';
        if(($cmp['plan_counts']['worlds']??0)!==8 || count($cmp['pages'])!==188 || count($cmp['content_categories'])!==296)
            $errors[]='Acht-Welten-Quellprofil unvollstaendig.';
        foreach((array)$inventory['issues'] as $issue){
            if(in_array($issue['area']??'',['WP_SEITEN','WP_KATEGORIEN'],true))$errors[]='WordPress-Hierarchiepruefung: '.($issue['detail']??'Fehler');
        }
        $counts=$cmp['comparison_counts'];
        foreach(['old_page_id_verified'=>104,'legacy_term_id_verified'=>89,'old_page_unmatched'=>0,'legacy_term_unmatched'=>0,
            'legacy_term_conflicts'=>0,'page_identity_or_path_conflicts'=>0,'page_exact_path_unlinked'=>0] as $k=>$expected){
            if((int)($counts[$k]??-1)!==$expected)$errors[]='Geschuetzter Altbestand nicht unveraendert: '.$k;
        }
        $bypath=[];$pbyid=[];$prow=[];$trow=[];
        foreach($source['pages'] as $p){$bypath[self::key($p['path'])]=$p;$pbyid[$p['source_id']]=$p;}
        foreach($cmp['pages'] as $p){$prow[$p['source_id']]=$p;}
        foreach($cmp['content_categories'] as $t){$trow[$t['source_id']]=$t;}
        $wpPages=[];$wpTerms=[];$siblingSlugs=[];$existingTermSlugs=[];$existingTermNames=[];
        foreach($inventory['pages']['items'] as $p){
            $wpPages[(int)$p['id']]=$p;
            $siblingSlugs[(int)$p['parent_id'].'|'.(string)$p['slug']][]=(int)$p['id'];
        }
        foreach($inventory['categories']['items'] as $t){
            $wpTerms[(int)$t['id']]=$t;
            $existingTermSlugs[(string)$t['slug']][]=(int)$t['id'];
            $existingTermNames[function_exists('mb_strtolower')?mb_strtolower((string)$t['name'],'UTF-8'):strtolower((string)$t['name'])][]=(int)$t['id'];
        }
        $pageIds=[];$termIds=[];$held=[];$heldTermIds=[];$tasks=[];$newSiblings=[];$newCatSlugs=[];$newCatNames=[];
        foreach($source['pages'] as $p){
            $id=(string)$p['source_id'];$result=$prow[$id]??null;
            if(!$result){$errors[]='Seitenidentitaet fehlt: '.$id;continue;}
            if(!empty($p['legacy'])){
                if(($result['status']??'')==='CONFIRMED_META_AND_PATH')$pageIds[$id]=(int)$result['wp_id_confirmed'];
                continue;
            }
            if(!empty($p['review_hold'])){
                $held[]=$id;
                if(($result['status']??'')!=='NEW_PAGE_PROPOSAL_NOT_WRITTEN')$errors[]='Gesperrte Seite bereits veraendert: '.$id;
                continue;
            }
            $parentPath=array_slice($p['path'],0,-1);
            $parentId=$parentPath?($bypath[self::key($parentPath)]['source_id']??null):null;
            if($parentPath && !$parentId){$errors[]='Seiteneltern fehlen: '.$id;continue;}
            $slug=sanitize_title((string)$p['title']);
            if($slug===''||strlen($slug)>160)$errors[]='Ungueltiger Seiten-Slug: '.$id;
            $task=['kind'=>'page','source_id'=>$id,'parent_source_id'=>$parentId,'title'=>$p['title'],
                'slug'=>$slug,'role'=>$p['role'],'path'=>$p['path']];
            $status=$result['status']??'';
            if($status==='CONFIRMED_META_AND_PATH'){
                $wpid=(int)$result['wp_id_confirmed'];$live=$wpPages[$wpid]??null;
                if(!$live || $live['slug']!==$slug || $live['status']!=='draft')$errors[]='Bereits angelegte neue Seite abweichend: '.$id;
                else $pageIds[$id]=$wpid;
            }elseif($status!=='NEW_PAGE_PROPOSAL_NOT_WRITTEN')$errors[]='Neue Seite hat Konflikt: '.$id.' '.$status;
            if($status==='NEW_PAGE_PROPOSAL_NOT_WRITTEN'){
                $sib=(string)($parentId??'ROOT').'|'.$slug;
                if(isset($newSiblings[$sib]))$errors[]='Doppelter Seiten-Slug im gleichen Zweig: '.$sib;
                $newSiblings[$sib]=true;
            }
            $tasks[]=$task;
        }
        if(count($held)!==self::EXPECTED_HOLDS)$errors[]='SEO-HOLD-Anzahl veraendert.';
        foreach($tasks as $t){
            $id=$t['source_id'];$r=$prow[$id];
            if(($r['status']??'')!=='NEW_PAGE_PROPOSAL_NOT_WRITTEN')continue;
            $parentId=$t['parent_source_id'];
            if($parentId!==null && isset($pageIds[$parentId])){
                $sibling=(int)$pageIds[$parentId].'|'.$t['slug'];
                if(isset($siblingSlugs[$sibling]))$errors[]='WordPress-Seiten-Slug im Elternzweig schon belegt: '.$id;
            }elseif($parentId===null && isset($siblingSlugs['0|'.$t['slug']])){
                $errors[]='WordPress-Hauptseiten-Slug schon belegt: '.$id;
            }
        }
        foreach($source['content_categories'] as $cat){
            $id=(string)$cat['source_id'];$r=$trow[$id]??null;
            if(!$r){$errors[]='Inhaltsrubrik fehlt: '.$id;continue;}
            if(($cat['source']??'')==='ALTPLAN_0_4_7'){
                if(($r['status']??'')==='CONFIRMED_TERM_META')$termIds[$id]=(int)$r['wp_id_confirmed'];
                continue;
            }
            if(!empty($cat['review_hold'])){
                $heldTermIds[]=$id;
                if(($r['status']??'')!=='NEW_TERM_PROPOSAL_NOT_WRITTEN')$errors[]='Gesperrte Rubrik bereits veraendert: '.$id;
                continue;
            }
            $owner=(string)$cat['owner_id'];
            if(!isset($pbyid[$owner]) || $pbyid[$owner]['role']!=='product' || !empty($pbyid[$owner]['review_hold'])){
                $errors[]='Inhaltsrubrik ohne freigegebenen Robotertyp: '.$id;continue;
            }
            $name=implode(' / ',$cat['owner_path']).' – '.$cat['short_label'];
            $slug=sanitize_title(implode(' ',$cat['owner_path']).' '.$cat['short_label']);
            if($slug===''||strlen($slug)>180 || count((array)$cat['topics'])<3)$errors[]='Inhaltsrubrik-Plan ungueltig: '.$id;
            $task=['kind'=>'category','source_id'=>$id,'parent_source_id'=>$owner,'name'=>$name,
                'short_label'=>$cat['short_label'],'slug'=>$slug,'topics'=>$cat['topics'],'path'=>$cat['owner_path']];
            $norm=function_exists('mb_strtolower')?mb_strtolower($name,'UTF-8'):strtolower($name);
            $status=$r['status']??'';
            if($status==='CONFIRMED_TERM_META'){
                $wpid=(int)$r['wp_id_confirmed'];$term=$wpTerms[$wpid]??null;
                if(!$term || $term['slug']!==$slug || $term['name']!==$name || (int)$term['parent_id']!==0 ||
                    !isset($pageIds[$owner]) || (int)get_term_meta($wpid,'_robotik_product_page_id',true)!==$pageIds[$owner]){
                    $errors[]='Bereits angelegte Rubrik weicht vom Ziel ab: '.$id;
                }else $termIds[$id]=$wpid;
            }elseif($status==='NEW_TERM_PROPOSAL_NOT_WRITTEN'){
                if(isset($existingTermSlugs[$slug])||isset($newCatSlugs[$slug]))$errors[]='WordPress-Kategorie-Slug doppelt: '.$slug;
                if(isset($existingTermNames[$norm])||isset($newCatNames[$norm]))$errors[]='WordPress-Kategorie-Name doppelt: '.$name;
                $newCatSlugs[$slug]=true;$newCatNames[$norm]=true;
            }else $errors[]='Neue Rubrik hat Konflikt: '.$id.' '.$status;
            $tasks[]=$task;
        }
        if(count($heldTermIds)!==self::EXPECTED_HELD_TERMS)$errors[]='48 Rubriken der 16 SEO-HOLDs nicht geschuetzt.';
        // The second check is structural, not a second editorial or SEO decision.
        foreach($tasks as $t){
            $parent=$t['parent_source_id'];if($parent===null)continue;
            if(!isset($pbyid[$parent]))$errors[]='Fehlender Eltern-Knoten: '.$t['source_id'];
        }
        usort($tasks,static function($a,$b){
            if($a['kind']!==$b['kind'])return $a['kind']==='page'?-1:1;
            if($a['kind']==='page' && count($a['path'])!==count($b['path']))return count($a['path'])<=>count($b['path']);
            return strcmp($a['source_id'],$b['source_id']);
        });
        if(count(array_filter($tasks,static fn($t)=>$t['kind']==='page'))!==self::EXPECTED_PAGES ||
            count(array_filter($tasks,static fn($t)=>$t['kind']==='category'))!==self::EXPECTED_TERMS)$errors[]='Geschuetzter Deltaumfang unerwartet.';
        $done=0;$todo=0;
        foreach($tasks as $t){
            if(isset($trow[$t['source_id']]) && $t['kind']==='category'){
                $isDone=($trow[$t['source_id']]['status']??'')==='CONFIRMED_TERM_META';
            }else{$isDone=($prow[$t['source_id']]['status']??'')==='CONFIRMED_META_AND_PATH';}
            if($isDone)$done++;else $todo++;
        }
        return [
            'schema'=>'robotik-v63-safe-delta-v1','site_url'=>$inventory['site_url'],
            'mode'=>'PREFLIGHT_READ_ONLY','errors'=>array_values(array_unique($errors)),
            'token'=>self::seal($source,$inventory,$cmp),
            'existing_pages'=>count($inventory['pages']['items']),
            'existing_categories'=>count($inventory['categories']['items']),
            'page_ids'=>$pageIds,'term_ids'=>$termIds,
            'held_ids'=>$held,'held_term_ids'=>$heldTermIds,
            'task_count'=>count($tasks),'task_done'=>$done,'task_remaining'=>$todo,
            'new_pages'=>self::EXPECTED_PAGES,'new_terms'=>self::EXPECTED_TERMS,
            'hold_pages'=>self::EXPECTED_HOLDS,'hold_terms'=>self::EXPECTED_HELD_TERMS,
            'tasks'=>$tasks,
            'prior_wp_page_ids'=>array_column($inventory['pages']['items'],'id'),
            'prior_wp_term_ids'=>array_column($inventory['categories']['items'],'id'),
        ];
    }
    private static function location():void {
        wp_safe_redirect(admin_url('admin.php?page=robotik-v63-delta'));exit;
    }
    public static function start():void {
        self::authorized();check_admin_referer('robotik_v63_delta_start');
        if(empty($_POST['robotik_v63_approve']))wp_die('Ausdrueckliche Schreibfreigabe fehlt.');
        $prior=get_option(self::STATE,[]);
        if(is_array($prior)&&isset($prior['status']))wp_die('Geschuetzter Import wurde bereits gestartet oder abgeschlossen. Kein neuer Lauf.');
        try{$p=self::prepare();}catch(Throwable $e){wp_die('Keine sichere Freigabe: '.$e->getMessage());}
        $token=(string)($_POST['robotik_v63_token']??'');
        if($p['errors'] || $token==='' || !hash_equals($p['token'],$token) || $p['task_remaining']!==227)
            wp_die('Bestand seit Anzeige geaendert oder noch nicht sauber: erst neue Gesamtvorschau oeffnen.');
        $state=['status'=>'WRITING','index'=>0,'total'=>227,'created_pages'=>0,'created_categories'=>0,
            'existing_pages_preserved'=>$p['prior_wp_page_ids'],'existing_terms_preserved'=>$p['prior_wp_term_ids'],
            'manifest_sha256'=>hash_file('sha256',__DIR__.'/../assets/robotik-v62-sollvorschau.json'),
            'error'=>'','started'=>gmdate('c')];
        update_option(self::STATE,$state,false);self::location();
    }
    private static function createOne(array $task,array &$pages,array &$terms):string {
        $id=$task['source_id'];
        if($task['kind']==='page'){
            if(isset($pages[$id]))return 'existing';
            $parentId=$task['parent_source_id'];$pid=$parentId===null?0:(int)($pages[$parentId]??0);
            if($parentId!==null && !$pid)throw new RuntimeException('Elternseite fehlt: '.$id);
            $post=wp_insert_post(['post_type'=>'page','post_status'=>'draft','post_title'=>$task['title'],
                'post_name'=>$task['slug'],'post_parent'=>$pid,'post_content'=>''],true);
            if(is_wp_error($post)||!$post)throw new RuntimeException('Seite konnte nicht angelegt werden: '.$id);
            $wpid=(int)$post;
            update_post_meta($wpid,self::MARKER,$id);
            update_post_meta($wpid,'_robotik_page_role',$task['role']);
            $read=get_post($wpid);
            if(!$read || $read->post_status!=='draft' || $read->post_title!==$task['title'] ||
                $read->post_name!==$task['slug'] || (int)$read->post_parent!==$pid ||
                (string)get_post_meta($wpid,self::MARKER,true)!==$id)
                throw new RuntimeException('WordPress-Seitenreadback ungueltig: '.$id);
            $pages[$id]=$wpid;return 'page';
        }
        if(isset($terms[$id]))return 'existing';
        $pid=(int)($pages[$task['parent_source_id']]??0);
        if(!$pid)throw new RuntimeException('Rubrik ohne Produktseite: '.$id);
        $term=wp_insert_term($task['name'],'category',['slug'=>$task['slug'],'parent'=>0]);
        if(is_wp_error($term)||empty($term['term_id']))throw new RuntimeException('Inhaltsrubrik nicht angelegt: '.$id);
        $tid=(int)$term['term_id'];
        update_term_meta($tid,self::MARKER,$id);
        update_term_meta($tid,'_robotik_short_label',$task['short_label']);
        update_term_meta($tid,'_robotik_product_page_id',$pid);
        update_term_meta($tid,'_robotik_article_directions',wp_json_encode($task['topics'],JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES));
        $read=get_term($tid,'category');
        if(!$read || is_wp_error($read) || $read->slug!==$task['slug'] || $read->name!==$task['name'] ||
            (string)get_term_meta($tid,self::MARKER,true)!==$id ||
            (int)get_term_meta($tid,'_robotik_product_page_id',true)!==$pid)
            throw new RuntimeException('WordPress-Kategoriereadback ungueltig: '.$id);
        $terms[$id]=$tid;return 'category';
    }
    public static function advance():array {
        $state=get_option(self::STATE,[]);
        if(!is_array($state)||($state['status']??'')!=='WRITING')return is_array($state)?$state:['status'=>'BLOCKED'];
        if(!add_option(self::LOCK,time(),'','no')){
            $locked=(int)get_option(self::LOCK,0);
            if($locked>0 && time()-$locked>180){delete_option(self::LOCK);}
            return ['status'=>'WRITING','index'=>(int)$state['index'],'total'=>(int)$state['total'],'busy'=>true];
        }
        try{
            if(!hash_equals((string)$state['manifest_sha256'],(string)hash_file('sha256',__DIR__.'/../assets/robotik-v62-sollvorschau.json')))
                throw new RuntimeException('Verbindliches Sollprofil seit Start veraendert.');
            $p=self::prepare();if($p['errors'])throw new RuntimeException('WordPress-Bestand geaendert: '.implode(' | ',array_slice($p['errors'],0,3)));
            $tasks=$p['tasks'];
            if(count($tasks)!==(int)$state['total'])throw new RuntimeException('Importumfang veraendert.');
            $pages=$p['page_ids'];$terms=$p['term_ids'];
            $end=min((int)$state['total'],(int)$state['index']+self::BATCH);
            while((int)$state['index']<$end){
                $task=$tasks[(int)$state['index']];
                $out=self::createOne($task,$pages,$terms);
                if($out==='page')$state['created_pages']++;
                if($out==='category')$state['created_categories']++;
                $state['index']++;update_option(self::STATE,$state,false);
            }
            if((int)$state['index']===(int)$state['total']){
                $read=self::prepare();
                if($read['errors']||$read['task_remaining']!==0 || $read['task_done']!==227)
                    throw new RuntimeException('Gesamtreadback unvollstaendig oder WordPress-Konflikt.');
                if(count($read['held_ids'])!==16||count($read['held_term_ids'])!==48)
                    throw new RuntimeException('SEO-HOLD nicht erhalten.');
                $allPageIds=array_flip($read['prior_wp_page_ids']);
                $allTermIds=array_flip($read['prior_wp_term_ids']);
                foreach($state['existing_pages_preserved'] as $id)if(!isset($allPageIds[$id]))throw new RuntimeException('Alte Seite fehlt: '.$id);
                foreach($state['existing_terms_preserved'] as $id)if(!isset($allTermIds[$id]))throw new RuntimeException('Alte Kategorie fehlt: '.$id);
                $state['status']='COMPLETE_SAFE_DELTA_WITH_16_HOLDS';
                $state['verified']=227;
                $state['completed']=gmdate('c');
                update_option(self::STATE,$state,false);
            }
        }catch(Throwable $e){$state['status']='BLOCKED';$state['error']=$e->getMessage();update_option(self::STATE,$state,false);}
        finally{delete_option(self::LOCK);}
        return $state;
    }
    public static function ajax_tick():void {
        self::authorized();check_ajax_referer('robotik_v63_delta_tick');
        $state=self::advance();wp_send_json_success(['status'=>$state['status']??'BLOCKED',
            'index'=>(int)($state['index']??0),'total'=>(int)($state['total']??0),
            'created_pages'=>(int)($state['created_pages']??0),'created_categories'=>(int)($state['created_categories']??0),
            'error'=>(string)($state['error']??''),'busy'=>!empty($state['busy'])]);
    }
    public static function export():void {
        self::authorized();check_admin_referer('robotik_v63_delta_result');
        $state=get_option(self::STATE,[]);
        $p=self::prepare();
        $report=['schema'=>'robotik-v63-safe-delta-readback-v1','date_utc'=>gmdate('c'),
            'site_url'=>$p['site_url'],'state'=>$state,'audit'=>[
                'errors'=>$p['errors'],'total_tasks'=>$p['task_count'],'completed_tasks'=>$p['task_done'],
                'remaining_tasks'=>$p['task_remaining'],'new_pages_target'=>68,'new_terms_target'=>159,
                'blocked_seo_pages'=>$p['hold_pages'],'blocked_seo_categories'=>$p['hold_terms'],
                'preexisting_pages_preserved'=>count((array)($state['existing_pages_preserved']??[])),
                'preexisting_categories_preserved'=>count((array)($state['existing_terms_preserved']??[]))],
            'new_page_ids'=>array_intersect_key($p['page_ids'],array_flip(array_column(array_filter($p['tasks'],static fn($t)=>$t['kind']==='page'),'source_id'))),
            'new_category_ids'=>array_intersect_key($p['term_ids'],array_flip(array_column(array_filter($p['tasks'],static fn($t)=>$t['kind']==='category'),'source_id'))),
            'seo_hold_page_ids'=>$p['held_ids'],'seo_hold_category_ids'=>$p['held_term_ids']];
        nocache_headers();header('Content-Type: application/json; charset=UTF-8');
        header('Content-Disposition: attachment; filename="robotik-v63-gesamtreadback-'.gmdate('Ymd-His').'.json"');
        echo wp_json_encode($report,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES|JSON_PRETTY_PRINT);exit;
    }
    public static function screen():void {
        self::authorized();$state=get_option(self::STATE,[]);
        echo '<div class="wrap"><h1>Robotik – geschuetzte Gesamtuebernahme</h1>';
        echo '<p>Einmalige geschuetzte Uebernahme aus dem bereits abgeglichenen Acht-Welten-Plan. Bestehende Seiten und Kategorien bleiben unveraendert; neue Seiten nur als Entwurf. Keine Veroeffentlichung, keine SEO-Gebuehren, keine Magazin-/HivePress-Aenderungen.</p>';
        try{$p=self::prepare();}catch(Throwable $e){$p=['errors'=>[$e->getMessage()],'task_remaining'=>0,'task_done'=>0];}
        if(!empty($p['errors']))echo '<div class="notice notice-error"><p>'.esc_html(implode(' | ',array_slice($p['errors'],0,5))).'</p></div>';
        echo '<p><strong>Neue Seiten:</strong> 68 sicher freigegeben · <strong>Inhaltsrubriken:</strong> 159 · <strong>SEO-geschuetzt:</strong> 16 Seiten und 48 Rubriken. Die alte Importfunktion 104/89 nicht verwenden.</p>';
        echo '<p><strong>Aktueller Live-Abgleich:</strong> '.(int)($p['task_done']??0).' / 227 erfuellt; '.(int)($p['task_remaining']??0).' / 227 noch offen.</p>';
        if(!is_array($state)||!isset($state['status'])){
            if(empty($p['errors']) && ($p['task_remaining']??-1)===227){
                echo '<form action="'.esc_url(admin_url('admin-post.php')).'" method="post">';wp_nonce_field('robotik_v63_delta_start');
                echo '<input type="hidden" name="action" value="robotik_v63_delta_start">';
                echo '<input type="hidden" name="robotik_v63_token" value="'.esc_attr($p['token']).'">';
                echo '<p><label><input type="checkbox" name="robotik_v63_approve" value="1" required> Ich gebe ausschliesslich die 68 sicheren Entwurfsseiten und 159 Kategorien zur Anlage frei. Die 16 HOLD-Seiten und 48 Rubriken bleiben gesperrt.</label></p>';
                submit_button('Gesamten sicheren Block EINMAL uebernehmen','primary');echo '</form>';
            }
        }else{
            $status=(string)($state['status']??'BLOCKED');
            echo '<p><strong>Importstatus:</strong> <span id="robotik-v63-state">'.esc_html($status).' · '.(int)($state['index']??0).' / 227 · Seiten angelegt '.(int)($state['created_pages']??0).' · Kategorien angelegt '.(int)($state['created_categories']??0).'</span></p>';
            if(!empty($state['error']))echo '<div class="notice notice-error"><p>'.esc_html($state['error']).'</p></div>';
            if($status==='COMPLETE_SAFE_DELTA_WITH_16_HOLDS')echo '<div class="notice notice-success"><p>227 von 227 sicheren Aenderungen erstellt und zurueckgelesen. 16 SEO-HOLDs und 48 Rubriken weiterhin nicht importiert.</p></div>';
            if($status==='WRITING'){
                $nonce=wp_create_nonce('robotik_v63_delta_tick');
                echo '<script>(function(){var n='.wp_json_encode($nonce).',i=document.getElementById("robotik-v63-state");function go(){var d=new FormData();d.append("action","robotik_v63_delta_tick");d.append("_ajax_nonce",n);fetch(ajaxurl,{method:"POST",credentials:"same-origin",body:d}).then(r=>r.json()).then(j=>{if(!j.success)throw Error("WP verweigert Anfrage");var a=j.data;i.textContent=a.status+" · "+a.index+" / "+a.total+" · Seiten "+a.created_pages+" · Kategorien "+a.created_categories+(a.error?" · "+a.error:"");if(a.status==="WRITING")setTimeout(go,a.busy?800:0);else location.reload();}).catch(e=>{i.textContent="Verbindung unterbrochen: "+e.message+". Seite neu laden setzt gespeicherten Lauf fort.";});}go();})();</script>';
            }
        }
        echo '<form action="'.esc_url(admin_url('admin-post.php')).'" method="post">';wp_nonce_field('robotik_v63_delta_result');
        echo '<input type="hidden" name="action" value="robotik_v63_delta_result">';
        submit_button('EINEN Gesamtbericht als JSON herunterladen','secondary');echo '</form>';
        echo '</div>';
    }
}