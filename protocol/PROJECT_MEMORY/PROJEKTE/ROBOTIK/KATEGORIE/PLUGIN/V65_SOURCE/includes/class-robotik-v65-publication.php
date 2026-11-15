<?php
/**
 * Publish only the 68 validated V63 new pages once the 227-object delta has passed its
 * independent live readback. No new taxonomy, no old-page mutation, no SEO-HOLD writes.
 * User explicitly approves publication of existing empty draft pages.
 */
if (!defined('ABSPATH')) { exit; }
final class Robotik_V65_Publication {
    private const STATE = 'robotik_v65_publication_state';
    private const IMPORT = 'robotik_v63_delta_state';
    private const LOCK = 'robotik_v65_publication_lock';
    private const MARKER = '_robotik_kategorie_node_id';
    private const BATCH = 10;
    public static function boot():void {
        add_action('admin_menu',[self::class,'menu'],33);
        add_action('admin_post_robotik_v65_publish_start',[self::class,'start']);
        add_action('admin_post_robotik_v65_publish_resume',[self::class,'resume']);
        add_action('wp_ajax_robotik_v65_publish_tick',[self::class,'tick']);
    }
    public static function menu():void {
        add_submenu_page('robotik-kategorie','Neue Robotik-Seiten veröffentlichen','Neue Seiten sichtbar machen',
            'manage_options','robotik-v65-publish',[self::class,'screen']);
    }
    private static function authorized():void {
        if (!current_user_can('manage_options')) throw new RuntimeException('Nur Administratoren koennen veröffentlichen.');
    }
    public static function preview():array {
        self::authorized();
        $import=get_option(self::IMPORT,[]);
        if (!is_array($import) || ($import['status']??'')!=='COMPLETE_SAFE_DELTA_WITH_16_HOLDS' ||
            (int)($import['verified']??0)!==227 || (int)($import['index']??0)!==227) {
            return ['ready'=>false,'notice'=>'Zuerst die bestehende geschuetzte Gesamtuebernahme 227/227 beenden; nichts parallel veroeffentlichen.'];
        }
        $p=Robotik_V63_Delta::prepare();
        if ($p['errors'] || (int)$p['task_done']!==227 || (int)$p['task_remaining']!==0 ||
            count($p['held_ids'])!==16 || count($p['held_term_ids'])!==48 || count($p['term_ids'])!==248) {
            throw new RuntimeException('Live-Abgleich 227/227 oder 16 SEO-Sperren nicht mehr gueltig.');
        }
        $legacy=Robotik_Publish::preview();
        if (empty($legacy['valid']) || (int)($legacy['counts']['publish']??0)!==104) {
            throw new RuntimeException('Zuerst die vorhandenen 104 Seiten im bisherigen Veröffentlichungsmenue abschliessen.');
        }
        $manifest=Robotik_Kategorie_Gesamtvorschau::source();
        $items=[]; $seen=[]; $published=0; $drafts=0;
        foreach($manifest['pages'] as $node){
            if (!empty($node['legacy']) || !empty($node['review_hold'])) continue;
            $source=(string)$node['source_id']; $id=(int)($p['page_ids'][$source]??0);
            if (!$id || isset($seen[$id])) throw new RuntimeException('Importierte neue Seite nicht eindeutig: '.$source);
            $seen[$id]=true;
            $wp=get_post($id);
            if (!$wp || $wp->post_type!=='page' || !in_array($wp->post_status,['draft','publish'],true) ||
                (string)get_post_meta($id,self::MARKER,true)!==$source ||
                (string)get_post_meta($id,'_robotik_page_role',true)!==(string)$node['role'] ||
                $wp->post_title!==(string)$node['title'] || $wp->post_name!==sanitize_title((string)$node['title'])) {
                throw new RuntimeException('Seite geaendert/fehlt: '.$source);
            }
            if ($wp->post_status==='publish')$published++;else $drafts++;
            $items[]=['id'=>$id,'source_id'=>$source,'slug'=>$wp->post_name,'parent'=>(int)$wp->post_parent,'role'=>$node['role']];
        }
        if (count($items)!==68 || count($seen)!==68) throw new RuntimeException('Sicherer neuer Seitenumfang ungueltig.');
        $fingerprint=hash('sha256',wp_json_encode([$items,hash_file('sha256',__DIR__.'/../assets/robotik-v62-sollvorschau.json')],JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE));
        return ['ready'=>true,'items'=>$items,'drafts'=>$drafts,'published'=>$published,'token'=>$fingerprint];
    }
    private static function redirect():void {
        wp_safe_redirect(admin_url('admin.php?page=robotik-v65-publish'));exit;
    }
    public static function start():void {
        self::authorized();check_admin_referer('robotik_v65_publish_start');
        if(empty($_POST['robotik_v65_approve']))wp_die('Ausdrueckliche Veroeffentlichungsfreigabe fehlt.');
        $old=get_option(self::STATE,[]);
        if(is_array($old) && !empty($old['status']))wp_die('Veroeffentlichung bereits gestartet: kein zweiter Lauf.');
        try{$p=self::preview();}catch(Throwable $e){wp_die(esc_html($e->getMessage()));}
        if(empty($p['ready']) || empty($p['drafts']) || !hash_equals((string)$p['token'],(string)($_POST['robotik_v65_token']??'')))
            wp_die('Live-Bestand geaendert oder 227er Import nicht abgeschlossen. Keine Aktion.');
        update_option(self::STATE,['status'=>'WRITING','index'=>0,'total'=>68,'items'=>$p['items'],
            'published'=>0,'already_published'=>0,'error'=>'','started_at'=>gmdate('c')],false);
        self::redirect();
    }
    public static function resumeSaved():void {
        $s=get_option(self::STATE,[]);
        if(!is_array($s)||($s['status']??'')!=='BLOCKED'||count((array)($s['items']??[]))!==68)
            throw new RuntimeException('Kein gesicherter 68er-Veroeffentlichungslauf.');
        $p=self::preview();
        $old=array_map(static fn($x)=>[$x['id'],$x['source_id']],$s['items']);
        $now=array_map(static fn($x)=>[$x['id'],$x['source_id']],$p['items']??[]);
        if(empty($p['ready'])||$old!==$now)
            throw new RuntimeException('WordPress-Seiten weichen vom gespeicherten Veroeffentlichungsauftrag ab.');
        $s['status']='WRITING';$s['error']='';update_option(self::STATE,$s,false);
    }
    public static function resume():void {
        self::authorized();check_admin_referer('robotik_v65_publish_resume');
        try{self::resumeSaved();}catch(Throwable $e){wp_die(esc_html($e->getMessage()));}
        self::redirect();
    }
    public static function advance():array {
        $state=get_option(self::STATE,[]);
        if(!is_array($state)||($state['status']??'')!=='WRITING')return is_array($state)?$state:['status'=>'BLOCKED'];
        if(!add_option(self::LOCK,time(),'','no')) {
            $age=(int)get_option(self::LOCK,0);
            if($age>0&&time()-$age>180)delete_option(self::LOCK);
            return ['status'=>'WRITING','index'=>(int)$state['index'],'total'=>68,'busy'=>true];
        }
        try {
            $import=get_option(self::IMPORT,[]);
            if (($import['status']??'')!=='COMPLETE_SAFE_DELTA_WITH_16_HOLDS' || (int)($import['verified']??0)!==227)
                throw new RuntimeException('Geschuetzter Import nicht mehr abgeschlossen.');
            $items=(array)($state['items']??[]);
            if(count($items)!==68)throw new RuntimeException('Veroeffentlichungsplan beschaedigt.');
            $stop=min(68,(int)$state['index']+self::BATCH);
            while((int)$state['index']<$stop){
                $x=$items[(int)$state['index']]; $id=(int)$x['id'];$p=get_post($id);
                if(!$p || $p->post_type!=='page' || !in_array($p->post_status,['draft','publish'],true) ||
                    (string)get_post_meta($id,self::MARKER,true)!==(string)$x['source_id'] ||
                    (string)get_post_meta($id,'_robotik_page_role',true)!==(string)$x['role'] ||
                    $p->post_name!==(string)$x['slug'] || (int)$p->post_parent!==(int)$x['parent']) {
                    throw new RuntimeException('Seite nicht unveraendert: '.$id);
                }
                if ($p->post_status==='draft') {
                    $result=wp_update_post(['ID'=>$id,'post_status'=>'publish'],true);
                    if(is_wp_error($result)||(int)$result!==$id)throw new RuntimeException('Veroeffentlichung gescheitert: '.$id);
                    $after=get_post($id);
                    if(!$after || $after->post_status!=='publish' || $after->post_name!==$x['slug'] ||
                        (int)$after->post_parent!==(int)$x['parent']) throw new RuntimeException('Live-Kontrolle nach Veroeffentlichung gescheitert: '.$id);
                    $state['published']++;
                } else $state['already_published']++;
                $state['index']++;
                update_option(self::STATE,$state,false);
            }
            if ((int)$state['index']===68){
                $check=self::preview();
                if(empty($check['ready']) || (int)$check['published']!==68 || (int)$check['drafts']!==0)
                    throw new RuntimeException('Endkontrolle: Nicht alle 68 neuen Seiten sichtbar.');
                $state['status']='COMPLETE'; $state['verified']=68; $state['completed_at']=gmdate('c');
                unset($state['items']);update_option(self::STATE,$state,false);
            }
        }catch(Throwable $e){$state['status']='BLOCKED';$state['error']=$e->getMessage();update_option(self::STATE,$state,false);}
        finally{delete_option(self::LOCK);}
        return $state;
    }
    public static function tick():void {
        self::authorized();check_ajax_referer('robotik_v65_publish_tick');
        $s=self::advance();wp_send_json_success(['status'=>$s['status']??'BLOCKED','index'=>$s['index']??0,
            'total'=>$s['total']??0,'error'=>$s['error']??'','busy'=>!empty($s['busy'])]);
    }
    public static function screen():void {
        self::authorized();$state=get_option(self::STATE,[]);
        echo '<div class="wrap"><h1>Robotik – 68 neue Seiten sichtbar machen</h1>';
        echo '<p>Nur vorhandene, nach 227/227 gepruefte Robotik-Entwurfsseiten. Die weiteren 16 fachlich freigegebenen Seiten und 48 Rubriken folgen in einer eigenen gesicherten Fortsetzungsphase. Fremde Seiten bleiben unangetastet. WordPress-Kategorien selbst sind bereits angelegt und muessen nicht publiziert werden.</p>';
        // The 68-page phase is complete: do not revalidate the old 248-term
        // pre-followup count after the 16+48 phase has legitimately finished.
        if(($state['status']??'')==='COMPLETE'){
            echo '<div class="notice notice-success"><p>68/68 bisherige neue Seiten veroeffentlicht. Die weiteren 16 Fachseiten werden im geschuetzten Nachtrag derselben Kategorie-Gesamtuebernahme bearbeitet.</p></div>';
            echo '</div>'; return;
        }
        try{$p=self::preview();}catch(Throwable $e){$p=['ready'=>false,'notice'=>$e->getMessage()];}
        if(!empty($p['notice']))echo '<div class="notice notice-warning"><p>'.esc_html($p['notice']).'</p></div>';
        if(!empty($p['ready'])){
            echo '<p><strong>Live:</strong> '.(int)$p['published'].'/68 neuere Seiten veroeffentlicht, '.(int)$p['drafts'].' Entwuerfe. Alte 104 Seiten bereits veroeffentlicht.</p>';
            if(empty($state['status']) && (int)$p['drafts']>0){
                echo '<form method="post" action="'.esc_url(admin_url('admin-post.php')).'">';
                wp_nonce_field('robotik_v65_publish_start');
                echo '<input type="hidden" name="action" value="robotik_v65_publish_start">';
                echo '<input type="hidden" name="robotik_v65_token" value="'.esc_attr($p['token']).'">';
                echo '<label><input type="checkbox" name="robotik_v65_approve" value="1" required> 68 gepruefte neue Seiten oeffentlich freigeben (auch ohne fertige Fachartikel). 16 weitere Fachseiten folgen im selben geschuetzten Workflow.</label>';
                submit_button('Einmalig alle neuen Seiten veroeffentlichen','primary');echo '</form>';
            }
        }
        if(!empty($state['status'])){
            echo '<p id="robotik-v65-progress">'.esc_html((string)$state['status']).' · '.(int)($state['index']??0).' / 68</p>';
            if(!empty($state['error']))echo '<div class="notice notice-error"><p>'.esc_html($state['error']).'</p></div>';
            if(($state['status']??'')==='WRITING'){
                $nonce=wp_create_nonce('robotik_v65_publish_tick');
                echo '<script>(function(){var n='.wp_json_encode($nonce).';var el=document.getElementById("robotik-v65-progress");function tick(){var d=new FormData();d.append("action","robotik_v65_publish_tick");d.append("_ajax_nonce",n);fetch(ajaxurl,{method:"POST",credentials:"same-origin",body:d}).then(r=>r.json()).then(j=>{if(!j.success)throw Error("WP-Antwort");var s=j.data;el.textContent=s.status+" · "+s.index+" / "+s.total+(s.error?" · "+s.error:"");if(s.status==="WRITING")setTimeout(tick,s.busy?600:0);else location.reload();}).catch(e=>{el.textContent="Unterbrochen: Seite neu laden, um den gespeicherten Lauf fortzusetzen.";});}tick();})();</script>';
            }
            if(($state['status']??'')==='BLOCKED'){echo '<form method="post" action="'.esc_url(admin_url('admin-post.php')).'">';wp_nonce_field('robotik_v65_publish_resume');echo '<input type="hidden" name="action" value="robotik_v65_publish_resume">';submit_button('Gespeicherten Lauf sicher fortsetzen','secondary');echo '</form>';}
            if(($state['status']??'')==='COMPLETE')echo '<div class="notice notice-success"><p>68/68 neue Seiten sichtbar. Insgesamt 172 freigegebene Robotik-Seiten, 16 SEO-HOLDs weiterhin gesperrt.</p></div>';
        }
        echo '</div>';
    }
}