<?php
/**
 * Robotik V84: a single, explicitly approved 16-page/32-category delta.
 * Uses the already installed V63 createOne() writer and original WP identities.
 * No new plugin, no Google calls, no second taxonomy, no cron or new table.
 */
if (!defined('ABSPATH')) exit;

final class Robotik_V84_Kategorien_Nachtrag {
    private const STATE = 'robotik_v84_kategorien_nachtrag_state';
    private const LOCK = 'robotik_v63_delta_lock';
    private const SOURCE = __DIR__.'/../assets/robotik-v84-delta.json';
    private const TOTAL = 48;
    private const MARKER = '_robotik_kategorie_node_id';

    public static function boot(): void {
        add_action('admin_post_robotik_v84_start', [self::class,'start']);
        add_action('admin_post_robotik_v84_resume', [self::class,'resume']);
        add_action('wp_ajax_robotik_v84_tick', [self::class,'tick']);
    }

    private static function requireAdmin(): void {
        if (!current_user_can('manage_options')) throw new RuntimeException('Nur Administratoren duerfen den Fachnachtrag ausfuehren.');
    }

    private static function sourceHash(): string {
        if (!is_readable(self::SOURCE)) throw new RuntimeException('Der 48er-Fachplan fehlt.');
        return (string)hash_file('sha256',self::SOURCE);
    }

    private static function source(): array {
        $src=json_decode((string)file_get_contents(self::SOURCE),true);
        if (!is_array($src) || ($src['schema']??'')!=='robotik-v84-approved-delta-v1' ||
            count((array)($src['tasks']??[]))!==self::TOTAL)
            throw new RuntimeException('Der redaktionell festgelegte Fachplan ist unvollstaendig.');
        $tasks=$src['tasks'];
        $pageCount=count(array_filter($tasks,static fn($x)=>($x['kind']??'')==='page'));
        $catCount=count(array_filter($tasks,static fn($x)=>($x['kind']??'')==='category'));
        if ($pageCount!==16 || $catCount!==32)
            throw new RuntimeException('Fachplan hat nicht genau 16 Seiten und 32 Kategorien.');
        usort($tasks, static function($a,$b):int {
            if ($a['kind']!==$b['kind']) return $a['kind']==='page'?-1:1;
            return strcmp((string)$a['source_id'],(string)$b['source_id']);
        });
        return $tasks;
    }

    private static function original(): array {
        $all=get_option('robotik_v78_gesamtabschluss_state',[]);
        $v77=get_option('robotik_v77_fachnachtrag_state',[]);
        if (!is_array($all) || ($all['status']??'')!=='COMPLETE' ||
            !is_array($v77) || ($v77['status']??'')!=='COMPLETE' ||
            (int)($v77['verified']??0)!==64)
            throw new RuntimeException('Zuerst den alten Gesamtabschluss 227/104/68/64 vollstaendig beenden. Keine Wiederholung.');
        $p=Robotik_V63_Delta::prepare();
        if (!empty($p['errors']) || (int)($p['task_done']??0)!==227 ||
            (int)($p['task_remaining']??-1)!==0 ||
            count((array)($p['page_ids']??[]))!==188 ||
            count((array)($p['term_ids']??[]))!==296)
            throw new RuntimeException('Der vorhandene 188-Seiten-/296-Kategorien-Bestand ist nicht sicher nachgewiesen: '.
                implode(' | ',array_slice((array)($p['errors']??[]),0,2)));
        return $p;
    }

    public static function plan(): array {
        self::requireAdmin();
        $p=self::original();
        $tasks=self::source();
        $pages=$p['page_ids']; $terms=$p['term_ids'];
        $seenIds=[]; $seenPageSlugs=[]; $seenTermSlugs=[]; $seenTermNames=[];
        $errors=[]; $done=0;
        $posts=get_posts(['post_type'=>'page','post_status'=>['publish','draft','private','pending'],
            'posts_per_page'=>-1,'suppress_filters'=>true]);
        $taxonomy=get_terms(['taxonomy'=>'category','hide_empty'=>false]);
        if (!is_array($posts) || is_wp_error($taxonomy) || !is_array($taxonomy))
            throw new RuntimeException('WordPress-Seiten oder Kategorien koennen nicht vollstaendig gelesen werden.');

        $existingPages=[];$pageSlugs=[];$allPageIds=[];
        foreach ($posts as $post) {
            $id=(int)$post->ID;$allPageIds[]=$id;
            $parent=(int)$post->post_parent;$slug=(string)$post->post_name;
            $pageSlugs[$parent.'|'.$slug][]=$id;
            $marker=(string)get_post_meta($id,self::MARKER,true);
            if (str_starts_with($marker,'v84_')) {
                if (isset($existingPages[$marker]))
                    $errors[]='Doppelte Robotik-Seitenkennung '.$marker;
                $existingPages[$marker]=$post;
            }
        }
        $existingTerms=[];$termSlugs=[];$termNames=[];$allTermIds=[];
        foreach ($taxonomy as $term) {
            $id=(int)$term->term_id;$allTermIds[]=$id;
            $name=(string)$term->name; $slug=(string)$term->slug;
            $termSlugs[$slug][]=$id;
            $termNames[function_exists('mb_strtolower')?mb_strtolower($name,'UTF-8'):strtolower($name)][]=$id;
            $marker=(string)get_term_meta($id,self::MARKER,true);
            if (str_starts_with($marker,'v84_')) {
                if (isset($existingTerms[$marker]))
                    $errors[]='Doppelte Robotik-Rubrikenkennung '.$marker;
                $existingTerms[$marker]=$term;
            }
        }
        foreach ($tasks as &$task) {
            $id=(string)$task['source_id'];
            if (!preg_match('/^v84_[a-z0-9_]+$/',$id) || isset($seenIds[$id])) {
                $errors[]='Ungueltige oder doppelte Aufgabenkennung '.$id;continue;
            }
            $seenIds[$id]=true;
            if ($task['kind']==='page') {
                $parentKey=(string)$task['parent_source_id'];
                $parentWp=(int)($pages[$parentKey]??0);
                $slug=sanitize_title((string)$task['title']);
                if (!$parentWp || !$slug || strlen($slug)>160 ||
                    (string)($task['role']??'')!=='product')
                    $errors[]='Unzulaessige Seite oder Elternseite '.$id;
                $task['slug']=$slug;
                $key=$parentWp.'|'.$slug;
                if (isset($seenPageSlugs[$key]))$errors[]='Zweimal derselbe Seitenpfad '.$id;
                $seenPageSlugs[$key]=true;
                if (isset($existingPages[$id])) {
                    $found=$existingPages[$id];$wpid=(int)$found->ID;
                    if ((int)$found->post_parent!==$parentWp || $found->post_name!==$slug ||
                        $found->post_title!==(string)$task['title'] ||
                        !in_array($found->post_status,['draft','publish'],true) ||
                        (string)get_post_meta($wpid,'_robotik_page_role',true)!=='product')
                        $errors[]='Bereits angelegte Fachseite wurde veraendert: '.$id;
                    else {
                        $pages[$id]=$wpid;
                        if ($found->post_status==='publish')$done++;
                    }
                }elseif (!empty($pageSlugs[$key])) {
                    $errors[]='WordPress-Seitenpfad bereits durch anderes Objekt belegt: '.$id;
                }
            } else {
                $owner=(string)$task['parent_source_id'];
                // Every category belongs to its unique new type page, NEVER a second taxonomy level.
                if (!isset($seenIds[$owner]) || !str_starts_with($owner,'v84_') ||
                    !isset($pages[$owner]) && !in_array($owner,
                      array_column(array_filter($tasks,static fn($v)=>($v['kind']??'')==='page'),'source_id'),true))
                    $errors[]='Kategorie ohne neue Robotertyp-Seite: '.$id;
                $name=implode(' / ',(array)$task['owner_path']).' – '.(string)$task['short_label'];
                $slug=sanitize_title(implode(' ',(array)$task['owner_path']).' '.(string)$task['short_label']);
                if (!$slug || strlen($slug)>180 || count((array)($task['topics']??[]))<3)
                    $errors[]='Unvollstaendige Themenkategorie '.$id;
                $task['name']=$name;$task['slug']=$slug;
                if (isset($seenTermSlugs[$slug]) || isset($seenTermNames[$name]))
                    $errors[]='Doppelte Themenrubrik im selben Paket: '.$id;
                $seenTermSlugs[$slug]=true; $seenTermNames[$name]=true;
                if (isset($existingTerms[$id])) {
                    $found=$existingTerms[$id];$termId=(int)$found->term_id;
                    $pageId=(int)($pages[$owner]??0);
                    if ($found->name!==$name || $found->slug!==$slug ||
                        (int)$found->parent!==0 || !$pageId ||
                        (int)get_term_meta($termId,'_robotik_product_page_id',true)!==$pageId ||
                        (string)get_term_meta($termId,'_robotik_short_label',true)!==(string)$task['short_label'])
                        $errors[]='Bereits angelegte Themenkategorie veraendert: '.$id;
                    else {$terms[$id]=$termId;$done++;}
                }elseif (isset($termSlugs[$slug]) || isset($termNames[
                    function_exists('mb_strtolower')?mb_strtolower($name,'UTF-8'):strtolower($name)]))
                    $errors[]='Rubrikname/-slug bereits fuer anderes WordPress-Objekt verwendet: '.$id;
            }
        }
        unset($task);
        if (count($seenIds)!==self::TOTAL)
            $errors[]='Die 48 neuen WordPress-Aufgaben sind nicht eindeutig.';
        return ['errors'=>array_values(array_unique($errors)),'tasks'=>$tasks,
            'done'=>$done,'remaining'=>self::TOTAL-$done,'page_ids'=>$pages,'term_ids'=>$terms,
            'original_page_ids'=>$p['prior_wp_page_ids'],'original_term_ids'=>$p['prior_wp_term_ids'],
            'manifest'=>self::sourceHash()];
    }

    private static function back(): void {
        wp_safe_redirect(admin_url('admin.php?page=robotik-v78-gesamtabschluss'));exit;
    }
    public static function start():void {
        self::requireAdmin();check_admin_referer('robotik_v84_start');
        if (empty($_POST['robotik_v84_approve']))wp_die('Einmalige Fachfreigabe fehlt.');
        $prior=get_option(self::STATE,[]);
        if (is_array($prior) && isset($prior['status']))wp_die('Ein Fachnachtrag existiert bereits. Keine zweite Freigabe.');
        try {$p=self::plan();}catch(Throwable $e){wp_die(esc_html($e->getMessage()));}
        $expected=hash('sha256',$p['manifest'].'|'.implode(',',array_map('intval',$p['original_page_ids'])).
            '|'.implode(',',array_map('intval',$p['original_term_ids'])));
        if ($p['errors'] || $p['done']!==0 || $p['remaining']!==self::TOTAL ||
            !hash_equals($expected,(string)($_POST['robotik_v84_token']??'')))
            wp_die('WordPress-Bestand oder einmaliger Nachtragsplan hat sich veraendert. Nichts angelegt.');
        update_option(self::STATE,['status'=>'WRITING','index'=>0,'total'=>self::TOTAL,
            'authorized_once'=>true,'manifest'=>$p['manifest'],
            'prior_pages'=>$p['original_page_ids'],'prior_terms'=>$p['original_term_ids'],
            'created_pages'=>0,'created_categories'=>0,'error'=>'','started'=>gmdate('c')],false);
        self::back();
    }

    private static function resumeSaved():void {
        $s=get_option(self::STATE,[]);
        if (!is_array($s)||($s['status']??'')!=='BLOCKED' || empty($s['authorized_once']) ||
            (int)($s['total']??0)!==self::TOTAL ||
            !hash_equals((string)($s['manifest']??''),self::sourceHash()))
            throw new RuntimeException('Kein sicher wiederaufnehmbarer 48er-Fachnachtrag.');
        $p=self::plan();
        if ($p['errors'] || $p['done']<(int)$s['index'] ||
            array_diff((array)($s['prior_pages']??[]),$p['original_page_ids']) ||
            array_diff((array)($s['prior_terms']??[]),$p['original_term_ids']))
            throw new RuntimeException('Bereits vorhandene Robotik-Objekte weichen ab; nichts doppelt schreiben.');
        $s['status']='WRITING';$s['error']='';update_option(self::STATE,$s,false);
    }
    public static function resume():void {
        self::requireAdmin();check_admin_referer('robotik_v84_resume');
        try{self::resumeSaved();}catch(Throwable $e){wp_die(esc_html($e->getMessage()));}
        self::back();
    }

    public static function advance():array {
        $s=get_option(self::STATE,[]);
        if (!is_array($s)||($s['status']??'')!=='WRITING')
            return is_array($s)?$s:['status'=>'BLOCKED','error'=>'Kein gestarteter Auftrag.'];
        if (!add_option(self::LOCK,time(),'','no')) {
            $age=(int)get_option(self::LOCK,0);
            if($age>0 && time()-$age>180) delete_option(self::LOCK);
            return $s+['busy'=>true];
        }
        try {
            if (empty($s['authorized_once']) ||
                !hash_equals((string)($s['manifest']??''),self::sourceHash()))
                throw new RuntimeException('Die einmalig freigegebene Fachquelle wurde veraendert.');
            $p=self::plan();
            if ($p['errors'] || count($p['tasks'])!==self::TOTAL)
                throw new RuntimeException('Ein Konflikt im WordPress-Bestand: '.implode(' | ',array_slice($p['errors'],0,3)));
            $pages=$p['page_ids'];$terms=$p['term_ids'];
            // V63 owns the only page/category writer; the same WP publish operation as V77.
            $last=min(self::TOTAL,(int)$s['index']+8);
            while ((int)$s['index']<$last) {
                $task=$p['tasks'][(int)$s['index']];
                $created=Robotik_V63_Delta::createOne($task,$pages,$terms);
                if ($task['kind']==='page') {
                    $wpid=(int)($pages[$task['source_id']]??0);$post=get_post($wpid);
                    if(!$post || !in_array($post->post_status,['draft','publish'],true))
                        throw new RuntimeException('Robotertyp-Seite nicht vorhanden: '.$task['source_id']);
                    if ($post->post_status==='draft') {
                        $out=wp_update_post(['ID'=>$wpid,'post_status'=>'publish'],true);
                        if(is_wp_error($out)||(int)$out!==$wpid)
                            throw new RuntimeException('Robotertyp-Seite konnte nicht publiziert werden: '.$task['source_id']);
                    }
                    $read=get_post($wpid);
                    if (!$read || $read->post_status!=='publish' ||
                        (string)get_post_meta($wpid,self::MARKER,true)!==$task['source_id'])
                        throw new RuntimeException('Neue Typseite ist nicht live: '.$task['source_id']);
                }
                if ($created==='page')$s['created_pages']++;
                if ($created==='category')$s['created_categories']++;
                $s['index']++;update_option(self::STATE,$s,false);
            }
            if ((int)$s['index']===self::TOTAL) {
                $proof=self::plan();
                if ($proof['errors'] || $proof['done']!==self::TOTAL ||
                    array_diff((array)$s['prior_pages'],$proof['original_page_ids']) ||
                    array_diff((array)$s['prior_terms'],$proof['original_term_ids']))
                    throw new RuntimeException('48er-Endabgleich oder urspruengliche WordPress-Objekte fehlerhaft.');
                $s['status']='COMPLETE';$s['verified']=self::TOTAL;$s['completed']=gmdate('c');
                update_option(self::STATE,$s,false);
            }
        } catch (Throwable $e) {
            $s['status']='BLOCKED';$s['error']=$e->getMessage();update_option(self::STATE,$s,false);
        } finally {delete_option(self::LOCK);}
        return $s;
    }

    public static function tick():void {
        self::requireAdmin();check_ajax_referer('robotik_v84_tick');
        $s=self::advance();
        wp_send_json_success(['status'=>$s['status']??'BLOCKED',
            'done'=>(int)($s['index']??0),'total'=>self::TOTAL,
            'error'=>$s['error']??'','busy'=>!empty($s['busy'])]);
    }

    public static function screenPart():void {
        self::requireAdmin();
        $prior=get_option(self::STATE,[]);
        echo '<hr><h2>Einmalige 16 Robotertypen + 32 Rubriken</h2>';
        echo '<p>Abgeschlossene Grundlagenrecherche. Acht Hauptwelten bleiben unveraendert; nur 16 echte neue Typseiten und 32 individuelle Inhaltsrubriken. Drei Sonderthemen bleiben fuer Magazin/Register. Kein Google-Zwang oder zusaetzliches Plugin.</p>';
        if (!is_array($prior)||!isset($prior['status'])) {
            try {$p=self::plan();}catch(Throwable $e){$p=['errors'=>[$e->getMessage()]];}
            if (!empty($p['errors'])) {
                echo '<div class="notice notice-error"><p>'.esc_html(implode(' | ',array_slice($p['errors'],0,3))).'</p></div>';return;
            }
            $token=hash('sha256',$p['manifest'].'|'.implode(',',array_map('intval',$p['original_page_ids'])).
                '|'.implode(',',array_map('intval',$p['original_term_ids'])));
            echo '<p><strong>Sicherer Vorabstand:</strong> '.(int)$p['done'].' / 48 erstellt; 188 urspruengliche Seiten und 296 Rubriken nachgewiesen.</p>';
            echo '<form method="post" action="'.esc_url(admin_url('admin-post.php')).'">';
            wp_nonce_field('robotik_v84_start');
            echo '<input type="hidden" name="action" value="robotik_v84_start">';
            echo '<input type="hidden" name="robotik_v84_token" value="'.esc_attr($token).'">';
            echo '<p><label><input type="checkbox" required name="robotik_v84_approve" value="1"> Ich genehmige diesen EINEN abschliessenden Fachnachtrag (16 Typseiten und 32 flache Rubriken) einschliesslich Veroeffentlichung der Seiten. Die alten 188 Seiten und 296 Kategorien bleiben erhalten.</label></p>';
            submit_button('Alle 48 Fachergänzungen EINMAL ausführen','primary');echo '</form>';
        } else {
            $status=(string)($prior['status']??'');
            echo '<p id="robotik-v84-status"><strong>Fachnachtrag:</strong> '.esc_html($status).' · '.(int)($prior['index']??0).' / 48</p>';
            if ($status==='BLOCKED') {
                echo '<div class="notice notice-error"><p>'.esc_html($prior['error']??'Unbekannter WordPress-Konflikt').'</p></div>';
                echo '<form method="post" action="'.esc_url(admin_url('admin-post.php')).'">';
                wp_nonce_field('robotik_v84_resume');
                echo '<input type="hidden" name="action" value="robotik_v84_resume">';
                submit_button('Gespeicherten Lauf nach Fehlerbehebung fortsetzen','secondary');echo '</form>';
            }
            if ($status==='WRITING') {
                $nonce=wp_create_nonce('robotik_v84_tick');
                echo '<script>(function(){var n='.wp_json_encode($nonce).',p=document.getElementById("robotik-v84-status");function work(){var d=new FormData();d.append("action","robotik_v84_tick");d.append("_ajax_nonce",n);fetch(ajaxurl,{method:"POST",credentials:"same-origin",body:d}).then(r=>r.json()).then(j=>{if(!j.success)throw Error("WP-Antwort");var x=j.data;p.textContent=x.status+" · "+x.done+"/48"+(x.error?" · "+x.error:"");if(x.status==="WRITING")setTimeout(work,x.busy?700:100);else location.reload();}).catch(e=>{p.textContent="Verbindung unterbrochen. Seite neu laden setzt den gespeicherten Auftrag fort.";});}work();})();</script>';
            }
            if ($status==='COMPLETE')
                echo '<div class="notice notice-success"><p>48/48 vollstaendig: 16 neue Robotertypseiten veroeffentlicht, 32 Inhaltsrubriken zugeordnet, alter Bestand beibehalten. Das war der letzte Teil der Grundlagenkategorien.</p></div>';
        }
    }
}
