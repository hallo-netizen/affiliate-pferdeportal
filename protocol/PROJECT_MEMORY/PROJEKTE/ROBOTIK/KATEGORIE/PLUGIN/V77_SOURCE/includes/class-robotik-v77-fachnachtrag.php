<?php
/**
 * V77: second, approved phase of the SAME V63 category writer.
 * Requires real 227/227 import and 68/68 prior publication.
 * Never replays old tasks, never needs Google URLs, never edits legacy objects.
 */
if (!defined('ABSPATH')) exit;
final class Robotik_V77_Fachnachtrag {
    private const STATE='robotik_v77_fachnachtrag_state';
    private const SHARED_LOCK='robotik_v63_delta_lock';
    private const TOTAL=64;
    private const MARKER='_robotik_kategorie_node_id';
    public static function boot():void {
        add_action('admin_post_robotik_v77_start',[self::class,'start']);
        add_action('admin_post_robotik_v77_resume',[self::class,'resume']);
        add_action('wp_ajax_robotik_v77_tick',[self::class,'tick']);
    }
    private static function guard():void {
        if(!current_user_can('manage_options'))throw new RuntimeException('Nur Administratoren.');
    }
    private static function prereq():void {
        $import=get_option('robotik_v63_delta_state',[]);
        if(!is_array($import)||($import['status']??'')!=='COMPLETE_SAFE_DELTA_WITH_16_HOLDS' ||
            (int)($import['verified']??0)!==227 || (int)($import['index']??0)!==227)
            throw new RuntimeException('Zuerst laufenden Import 227/227 abschliessen. Kein neuer Import.');
        $pub=get_option('robotik_v65_publication_state',[]);
        if(!is_array($pub)||($pub['status']??'')!=='COMPLETE' || (int)($pub['verified']??0)!==68)
            throw new RuntimeException('Zuerst die bestehenden 68 neuen Seiten fertig veroeffentlichen.');
    }
    public static function plan():array {
        self::guard();self::prereq();
        $p=Robotik_V63_Delta::prepare();
        if($p['errors'] || (int)$p['task_done']!==227 || (int)$p['task_remaining']!==0)
            throw new RuntimeException('Der bestehende 227er-Livebestand ist nicht gueltig: '.implode(' | ',array_slice($p['errors'],0,3)));
        $source=Robotik_Kategorie_Gesamtvorschau::source();
        $inv=$p['inventory'];$rows=$p['page_rows'];$termrows=$p['term_rows'];
        $byPath=[];$byId=[];
        foreach($source['pages'] as $x){$byPath[implode(' / ',$x['path'])]=$x;$byId[$x['source_id']]=$x;}
        $wpSlugs=[];foreach($inv['pages']['items'] as $x) $wpSlugs[(int)$x['parent_id'].'|'.$x['slug']][]= (int)$x['id'];
        $termSlugs=[];$termNames=[];
        foreach($inv['categories']['items'] as $x) {
            $termSlugs[(string)$x['slug']]=true;
            $termNames[(string)$x['name']]=true;
        }
        $pages=[];$cats=[];$seenPages=[];$seenCats=[];$done=0;$errors=[];
        foreach($source['pages'] as $x) {
            if(empty($x['review_hold'])||!empty($x['legacy']))continue;
            $id=(string)$x['source_id'];$r=$rows[$id]??[];
            $parentPath=array_slice($x['path'],0,-1);
            $parent=$parentPath?($byPath[implode(' / ',$parentPath)]['source_id']??null):null;
            $parentWp=(int)($p['page_ids'][$parent]??0);
            $slug=sanitize_title((string)$x['title']);
            if(!$parentWp||$slug==='')$errors[]='Elternseite oder Slug fehlt: '.$id;
            $task=['kind'=>'page','source_id'=>$id,'parent_source_id'=>$parent,'title'=>$x['title'],
                   'slug'=>$slug,'role'=>$x['role'],'path'=>$x['path']];
            $key=$parentWp.'|'.$slug;
            if(isset($seenPages[$key]))$errors[]='Doppelter Seitenslug im Nachtrag: '.$id;
            $seenPages[$key]=true;
            if(($r['status']??'')==='CONFIRMED_META_AND_PATH') {
                $wpid=(int)($p['page_ids'][$id]??0);$wp=get_post($wpid);
                if(!$wp||$wp->post_type!=='page'||$wp->post_title!==$x['title']||
                   $wp->post_name!==$slug||(int)$wp->post_parent!==$parentWp||
                   !in_array($wp->post_status,['draft','publish'],true)||
                   (string)get_post_meta($wpid,self::MARKER,true)!==$id||
                   (string)get_post_meta($wpid,'_robotik_page_role',true)!==(string)$x['role'])
                    $errors[]='Nachtragsseite weicht ab: '.$id;
                if($wp && $wp->post_status==='publish')$done++;
            } elseif(($r['status']??'')==='NEW_PAGE_PROPOSAL_NOT_WRITTEN') {
                if(!empty($wpSlugs[$key]))$errors[]='Seiten-Slug bereits vorhanden: '.$id;
            } else $errors[]='Unbekannte Nachtragsseite: '.$id.' / '.($r['status']??'?');
            $pages[]=$task;
        }
        foreach($source['content_categories'] as $x) {
            if(empty($x['review_hold']))continue;
            $id=(string)$x['source_id'];$r=$termrows[$id]??[];
            $owner=(string)$x['owner_id'];
            if(!isset($byId[$owner])||empty($byId[$owner]['review_hold']))$errors[]='Nicht zugeordnete Rubrik: '.$id;
            $name=implode(' / ',$x['owner_path']).' – '.$x['short_label'];
            $slug=sanitize_title(implode(' ',$x['owner_path']).' '.$x['short_label']);
            if($slug===''||count((array)$x['topics'])<3)$errors[]='Rubrik ohne drei Stoffrichtungen: '.$id;
            if(isset($seenCats[$slug]))$errors[]='Doppelter Rubrikslug: '.$id;
            $seenCats[$slug]=true;
            $task=['kind'=>'category','source_id'=>$id,'parent_source_id'=>$owner,'name'=>$name,
                   'short_label'=>$x['short_label'],'slug'=>$slug,'topics'=>$x['topics'],'path'=>$x['owner_path']];
            if(($r['status']??'')==='CONFIRMED_TERM_META') {
                $tid=(int)($p['term_ids'][$id]??0);$term=get_term($tid,'category');
                $ownerWp=(int)($p['page_ids'][$owner]??0);
                if(!$term||is_wp_error($term)||$term->slug!==$slug||$term->name!==$name||
                   (int)$term->parent!==0||!$ownerWp||
                   (string)get_term_meta($tid,self::MARKER,true)!==$id||
                   (int)get_term_meta($tid,'_robotik_product_page_id',true)!==$ownerWp)
                    $errors[]='Nachtragsrubrik weicht ab: '.$id;
                $done++;
            } elseif(($r['status']??'')==='NEW_TERM_PROPOSAL_NOT_WRITTEN') {
                if(isset($termSlugs[$slug])||isset($termNames[$name]))$errors[]='Rubrik-Name/Slug existiert: '.$id;
            } else $errors[]='Unbekannte Nachtragsrubrik: '.$id.' / '.($r['status']??'?');
            $cats[]=$task;
        }
        usort($pages,static function($a,$b){$na=count($a['path']);$nb=count($b['path']);return $na===$nb?strcmp($a['source_id'],$b['source_id']):($na<=>$nb);});
        usort($cats,static fn($a,$b)=>strcmp($a['source_id'],$b['source_id']));
        if(count($pages)!==16||count($cats)!==48)$errors[]='Nachtrag muss 16 Seiten und 48 Rubriken enthalten.';
        return ['errors'=>$errors,'tasks'=>array_merge($pages,$cats),'done'=>$done,'remaining'=>self::TOTAL-$done,
                'token'=>$p['token'],'page_ids'=>$p['page_ids'],'term_ids'=>$p['term_ids'],
                'prior_pages'=>$p['prior_wp_page_ids'],'prior_terms'=>$p['prior_wp_term_ids']];
    }
    private static function back():void {wp_safe_redirect(admin_url('admin.php?page=robotik-v63-delta'));exit;}
    public static function start():void {
        self::guard();check_admin_referer('robotik_v77_start');
        if(empty($_POST['robotik_v77_approve']))wp_die('Ausdrueckliche Freigabe fuer 16 Seiten und 48 Rubriken fehlt.');
        $old=get_option(self::STATE,[]);
        if(is_array($old)&&isset($old['status']))wp_die('Ein Nachtrag existiert bereits. Kein zweiter Start.');
        try{$p=self::plan();}catch(Throwable $e){wp_die(esc_html($e->getMessage()));}
        if($p['errors']||$p['done']!==0||$p['remaining']!==self::TOTAL ||
           !hash_equals((string)$p['token'],(string)($_POST['robotik_v77_token']??'')))
            wp_die('Nachtragsvorschau geaendert. Nichts geschrieben.');
        update_option(self::STATE,['status'=>'WRITING','index'=>0,'total'=>self::TOTAL,
            'prior_pages'=>$p['prior_pages'],'prior_terms'=>$p['prior_terms'],
            'manifest'=>hash_file('sha256',__DIR__.'/../assets/robotik-v62-sollvorschau.json'),
            'error'=>'','started'=>gmdate('c')],false);
        self::back();
    }
    public static function resume():void {
        self::guard();check_admin_referer('robotik_v77_resume');
        $s=get_option(self::STATE,[]);
        if(!is_array($s)||($s['status']??'')!=='BLOCKED'||(int)($s['total']??0)!==self::TOTAL)
            wp_die('Kein sicher gespeicherter Nachtrag zum Fortsetzen.');
        try{$p=self::plan();}catch(Throwable $e){wp_die(esc_html($e->getMessage()));}
        if($p['errors']||$p['done']<(int)$s['index'])wp_die('Abweichender Livebestand: nicht wiederholen.');
        $s['status']='WRITING';$s['error']='';update_option(self::STATE,$s,false);self::back();
    }
    public static function advance():array {
        $s=get_option(self::STATE,[]);
        if(!is_array($s)||($s['status']??'')!=='WRITING')return is_array($s)?$s:['status'=>'BLOCKED'];
        if(!add_option(self::SHARED_LOCK,time(),'','no'))
            return ['status'=>'WRITING','index'=>(int)$s['index'],'total'=>self::TOTAL,'busy'=>true];
        try {
            if(!hash_equals((string)$s['manifest'],(string)hash_file('sha256',__DIR__.'/../assets/robotik-v62-sollvorschau.json')))
                throw new RuntimeException('Sollplan wurde geaendert.');
            $p=self::plan();
            if($p['errors']||count($p['tasks'])!==self::TOTAL)throw new RuntimeException('Nachtrag nicht mehr eindeutig: '.implode(' | ',$p['errors']));
            $pages=$p['page_ids'];$terms=$p['term_ids'];
            $end=min(self::TOTAL,(int)$s['index']+8);
            while((int)$s['index']<$end) {
                $t=$p['tasks'][(int)$s['index']];
                Robotik_V63_Delta::createOne($t,$pages,$terms);
                if($t['kind']==='page') {
                    $wpid=(int)($pages[$t['source_id']]??0);
                    $wp=get_post($wpid);
                    if(!$wp||!in_array($wp->post_status,['draft','publish'],true))
                        throw new RuntimeException('Roboterseite fehlt: '.$t['source_id']);
                    if($wp->post_status==='draft') {
                        $result=wp_update_post(['ID'=>$wpid,'post_status'=>'publish'],true);
                        if(is_wp_error($result)||(int)$result!==$wpid)throw new RuntimeException('Seite nicht veroeffentlicht: '.$t['source_id']);
                    }
                    $after=get_post($wpid);
                    if(!$after||$after->post_status!=='publish'||$after->post_name!==$t['slug']||
                       (string)get_post_meta($wpid,self::MARKER,true)!==$t['source_id'])
                        throw new RuntimeException('Readback nach Veroeffentlichung fehlgeschlagen: '.$t['source_id']);
                }
                $s['index']++;update_option(self::STATE,$s,false);
            }
            if((int)$s['index']===self::TOTAL) {
                $q=self::plan();
                if($q['errors']||$q['done']!==self::TOTAL||(int)count($q['page_ids'])!==188||
                   (int)count($q['term_ids'])!==296||
                   array_diff((array)$s['prior_pages'],$q['prior_pages']) ||
                   array_diff((array)$s['prior_terms'],$q['prior_terms']))
                    throw new RuntimeException('Endkontrolle 16/48 oder alter Bestand nicht vollstaendig.');
                $s['status']='COMPLETE';$s['verified']=self::TOTAL;$s['completed']=gmdate('c');
                update_option(self::STATE,$s,false);
            }
        }catch(Throwable $e){$s['status']='BLOCKED';$s['error']=$e->getMessage();update_option(self::STATE,$s,false);}
        finally{delete_option(self::SHARED_LOCK);}
        return $s;
    }
    public static function tick():void {
        self::guard();check_ajax_referer('robotik_v77_tick');
        $s=self::advance();
        wp_send_json_success(['status'=>$s['status']??'BLOCKED','index'=>(int)($s['index']??0),
            'total'=>self::TOTAL,'error'=>$s['error']??'','busy'=>!empty($s['busy'])]);
    }
    public static function screenPart():void {
        self::guard();$s=get_option(self::STATE,[]);
        echo '<hr><h2>Fachlich freigegebener Nachtrag: 16 Seiten + 48 Rubriken</h2>';
        echo '<p>Ohne Google-Adressen, im selben WordPress-Kategorie-Plugin. Bestehende 227 Aufgaben bleiben erhalten. Gewerbe/Industrie unangetastet.</p>';
        try{$p=self::plan();}catch(Throwable $e){$p=['errors'=>[$e->getMessage()]];}
        if(!empty($p['errors']))echo '<div class="notice notice-warning"><p>'.esc_html(implode(' | ',array_slice($p['errors'],0,3))).'</p></div>';
        if(empty($s['status'])&&empty($p['errors'])&&$p['remaining']===self::TOTAL) {
            echo '<form method="post" action="'.esc_url(admin_url('admin-post.php')).'">';
            wp_nonce_field('robotik_v77_start');
            echo '<input type="hidden" name="action" value="robotik_v77_start">';
            echo '<input type="hidden" name="robotik_v77_token" value="'.esc_attr($p['token']).'">';
            echo '<label><input type="checkbox" name="robotik_v77_approve" value="1" required> 16 gepruefte neue Typseiten veroeffentlichen und 48 flache WP-Kategorien anlegen. Keine bestehenden Seiten aendern.</label>';
            submit_button('Fachnachtrag einmalig abschliessen','primary');echo '</form>';
        }
        if(!empty($s['status'])) {
            echo '<p id="robotik-v77-state">'.esc_html((string)$s['status']).' · '.(int)($s['index']??0).' / 64</p>';
            if(!empty($s['error']))echo '<div class="notice notice-error"><p>'.esc_html((string)$s['error']).'</p></div>';
            if($s['status']==='WRITING') {
                $nonce=wp_create_nonce('robotik_v77_tick');
                echo '<script>(function(){var n='.wp_json_encode($nonce).',el=document.getElementById("robotik-v77-state");function go(){var d=new FormData();d.append("action","robotik_v77_tick");d.append("_ajax_nonce",n);fetch(ajaxurl,{method:"POST",credentials:"same-origin",body:d}).then(r=>r.json()).then(j=>{if(!j.success)throw Error("WP Antwort");var a=j.data;el.textContent=a.status+" · "+a.index+" / 64"+(a.error?" · "+a.error:"");if(a.status==="WRITING")setTimeout(go,a.busy?800:0);else location.reload();}).catch(e=>{el.textContent="Unterbrechung: gespeicherter Lauf bleibt erhalten.";});}go();})();</script>';
            }
            if($s['status']==='BLOCKED'){
                echo '<form method="post" action="'.esc_url(admin_url('admin-post.php')).'">';
                wp_nonce_field('robotik_v77_resume');
                echo '<input type="hidden" name="action" value="robotik_v77_resume">';
                submit_button('Gespeicherten Nachtrag sicher fortsetzen','secondary');echo '</form>';
            }
            if($s['status']==='COMPLETE')echo '<div class="notice notice-success"><p>16/16 Seiten sichtbar, 48/48 Rubriken angelegt. Gesamtplan 188 Seiten/296 Rubriken im Live-Readback geprueft.</p></div>';
        }
    }
}
