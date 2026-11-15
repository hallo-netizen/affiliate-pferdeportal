<?php
/**
 * 0.4.13: ONE approval covers old 227, 104 original pages published,
 * 68 new pages published and the approved follow-up 16+48.
 * Same existing WordPress writers and state, no API or cron.
 */
if (!defined('ABSPATH')) exit;
final class Robotik_V78_Gesamtabschluss {
    private const STATE='robotik_v78_gesamtabschluss_state';
    private const LOCK='robotik_v78_gesamtabschluss_lock';
    private const MANIFEST=__DIR__.'/../assets/robotik-v62-sollvorschau.json';

    public static function boot():void {
        add_action('admin_menu',[self::class,'menu'],40);
        add_action('admin_post_robotik_v78_start',[self::class,'start']);
        add_action('admin_post_robotik_v78_export',[self::class,'export']);
        add_action('admin_post_robotik_v78_resume',[self::class,'resume']);
        add_action('wp_ajax_robotik_v78_tick',[self::class,'tick']);
    }
    public static function menu():void {
        // One visible workflow; historical endpoints remain for safe compatibility.
        remove_submenu_page('robotik-kategorie','robotik-v63-delta');
        remove_submenu_page('robotik-kategorie','robotik-v65-publish');
        add_submenu_page('robotik-kategorie','Robotik – Gesamtabschluss',
            'Gesamtabschluss (einmalig)','manage_options','robotik-v78-gesamtabschluss',
            [self::class,'screen']);
    }
    private static function authorized():void {
        if(!current_user_can('manage_options'))
            throw new RuntimeException('Nur Administratoren duerfen diesen Ablauf starten.');
    }
    private static function manifest():string {
        if(!is_readable(self::MANIFEST))throw new RuntimeException('Verbindlicher V62-Fachplan fehlt.');
        return (string)hash_file('sha256',self::MANIFEST);
    }
    private static function currentPhase():string {
        $v77=get_option('robotik_v77_fachnachtrag_state',[]);
        $v65=get_option('robotik_v65_publication_state',[]);
        $v63=get_option('robotik_v63_delta_state',[]);
        if(is_array($v77)&&isset($v77['status']))return 'nachtrag';
        if(is_array($v65)&&isset($v65['status']))return 'veroeffentlichen';
        if(is_array($v63)&&($v63['status']??'')==='COMPLETE_SAFE_DELTA_WITH_16_HOLDS')return 'altseiten';
        return 'uebernehmen';
    }
    private static function redirect():void {
        wp_safe_redirect(admin_url('admin.php?page=robotik-v78-gesamtabschluss'));exit;
    }
    private static function initialCheck():array {
        self::authorized();
        $v63=get_option('robotik_v63_delta_state',[]);
        $v65=get_option('robotik_v65_publication_state',[]);
        $v77=get_option('robotik_v77_fachnachtrag_state',[]);
        if(!is_array($v63)||!is_array($v65)||!is_array($v77))
            throw new RuntimeException('Nicht lesbarer WordPress-Laufzustand.');
        if(isset($v65['status']) && ($v63['status']??'')!=='COMPLETE_SAFE_DELTA_WITH_16_HOLDS')
            throw new RuntimeException('Veroeffentlichung liegt vor, 227er Abschluss aber nicht.');
        if(isset($v77['status']) && ($v65['status']??'')!=='COMPLETE')
            throw new RuntimeException('Fachnachtrag liegt vor, alte 68er Veroeffentlichung aber nicht.');
        if(!isset($v63['status'])) {
            $p=Robotik_V63_Delta::prepare();
            if($p['errors'] || (int)$p['task_count']!==227 || (int)$p['task_done']!==0 ||
               (int)$p['task_remaining']!==227)
                throw new RuntimeException('Kein sicherer Originalstart. Vorhandene Objekte nicht erneut anlegen: '.implode(' | ',array_slice($p['errors'],0,2)));
            $status='NICHT_GESTARTET';$index=0;
        }else{
            $status=(string)$v63['status'];$index=(int)($v63['index']??0);
            if(!in_array($status,['WRITING','BLOCKED','COMPLETE_SAFE_DELTA_WITH_16_HOLDS'],true) ||
               (int)($v63['total']??0)!==227 || $index<0 || $index>227)
                throw new RuntimeException('Der alte 227er Auftrag hat einen unbekannten Zustand.');
            if($status==='COMPLETE_SAFE_DELTA_WITH_16_HOLDS'&&
                ((int)($v63['verified']??0)!==227 || $index!==227))
                throw new RuntimeException('Fehlender alter Abschlussnachweis.');
            if($status==='BLOCKED') {
                // Do NOT un-block here: the same original resumeSaved() owns that check.
                $p=Robotik_V63_Delta::prepare();
                if($p['errors'])throw new RuntimeException('Der alte Originalauftrag hat Livekonflikte: '.implode(' | ',array_slice($p['errors'],0,2)));
            }
        }
        return ['phase'=>self::currentPhase(),'legacy_index'=>$index,
            'legacy_state'=>$status,'manifest'=>self::manifest()];
    }
    public static function start():void {
        self::authorized();check_admin_referer('robotik_v78_start');
        if(empty($_POST['robotik_v78_approve']))
            wp_die('Einmalige Gesamtfreigabe fehlt.');
        $prior=get_option(self::STATE,[]);
        if(is_array($prior)&&isset($prior['status']))
            wp_die('Gesamtfreigabe existiert bereits. Kein zweiter Auftrag.');
        try{$p=self::initialCheck();}catch(Throwable $e){wp_die(esc_html($e->getMessage()));}
        $token=(string)($_POST['robotik_v78_token']??'');
        $expected=hash('sha256',$p['manifest'].'|'.$p['legacy_state'].'|'.$p['legacy_index'].'|'.$p['phase']);
        if($token===''||!hash_equals($expected,$token))
            wp_die('WordPress-Stand seit der Vorschau veraendert: keine Freigabe.');
        update_option(self::STATE,[
            'status'=>'RUNNING','phase'=>$p['phase'],'authorized_once'=>true,'manifest'=>$p['manifest'],
            'error'=>'','started_utc'=>gmdate('c'),
            'scope'=>'227 Importaufgaben + 104 alte Seiten publizieren + 68 neue Seiten publizieren + 64 Fachnachtragsobjekte',
            'no_google_calls'=>true,'no_industry_change'=>true],false);
        self::redirect();
    }
    public static function resume():void {
        self::authorized();check_admin_referer('robotik_v78_resume');
        $s=get_option(self::STATE,[]);
        if(!is_array($s)||($s['status']??'')!=='BLOCKED' || empty($s['authorized_once']))
            wp_die('Kein einmalig freigegebener Gesamtauftrag zum Fortsetzen.');
        try{
            if(!hash_equals((string)($s['manifest']??''),self::manifest()))
                throw new RuntimeException('Der freigegebene Sollplan wurde geaendert.');
        }catch(Throwable $e){wp_die(esc_html($e->getMessage()));}
        // Original phase handles actual inventory/recovery checks only once.
        $s['status']='RUNNING';$s['error']='';
        update_option(self::STATE,$s,false);
        self::redirect();
    }
    private static function stageImport():string {
        $s=get_option('robotik_v63_delta_state',[]);
        if(!is_array($s))throw new RuntimeException('V63-Zustand nicht lesbar.');
        if(!isset($s['status'])) {
            $p=Robotik_V63_Delta::prepare();
            if($p['errors']||(int)$p['task_count']!==227||(int)$p['task_done']!==0||
               (int)$p['task_remaining']!==227)
                throw new RuntimeException('Der 227er Originalbestand ist nicht mehr unveraendert.');
            update_option('robotik_v63_delta_state',[
                'status'=>'WRITING','index'=>0,'total'=>227,'created_pages'=>0,'created_categories'=>0,
                'existing_pages_preserved'=>$p['prior_wp_page_ids'],'existing_terms_preserved'=>$p['prior_wp_term_ids'],
                'manifest_sha256'=>self::manifest(),'error'=>'','started'=>gmdate('c')],false);
            $s=get_option('robotik_v63_delta_state',[]);
        }
        if(($s['status']??'')==='BLOCKED'){
            Robotik_V63_Delta::resumeSaved();
            $s=get_option('robotik_v63_delta_state',[]);
        }
        if(($s['status']??'')==='WRITING')$s=Robotik_V63_Delta::advance();
        if(($s['status']??'')==='BLOCKED')
            throw new RuntimeException('Alte 227er Uebernahme gestoppt: '.($s['error']??'Unbekannter Konflikt'));
        if(($s['status']??'')==='COMPLETE_SAFE_DELTA_WITH_16_HOLDS'){
            if((int)($s['verified']??0)!==227||(int)($s['index']??0)!==227)
                throw new RuntimeException('Alter 227er Readback fehlt.');
            return 'altseiten';
        }
        if(($s['status']??'')!=='WRITING')throw new RuntimeException('Unbekannter alter Importstatus.');
        return 'uebernehmen';
    }
    private static function stageOldPages():string {
        // The original V65 preview requires all 104 old pages published.
        // V78 version 0.4.12 missed that existing phase entirely.
        $p=Robotik_Publish::preview();
        if(empty($p['valid']) || (int)($p['expected']??0)!==104 ||
           (int)($p['counts']['draft']??-1)+(int)($p['counts']['publish']??-1)!==104 ||
           count((array)($p['ids']??[]))!==104)
            throw new RuntimeException('104 Originalseiten nicht eindeutig: '.
                implode(' | ',array_slice((array)($p['errors']??[]),0,3)));
        $s=get_option('robotik_first_publish_state_v1',[]);
        if(!is_array($s))throw new RuntimeException('104er Veroeffentlichungszustand nicht lesbar.');
        if(!isset($s['status'])) {
            if((int)$p['counts']['publish']===104)return 'veroeffentlichen';
            $s=['status'=>'WRITING','index'=>0,'total'=>104,
                'published'=>0,'already_published'=>0,'verified'=>0,'error'=>'',
                'ids'=>array_values($p['ids']),'token'=>$p['token'],
                'started_at'=>gmdate('c')];
            update_option('robotik_first_publish_state_v1',$s,false);
        }
        if(($s['status']??'')==='BLOCKED') {
            $ids=array_values((array)($p['ids']??[]));
            if((int)($s['total']??0)!==104 || (int)($s['index']??-1)<0 ||
               (int)($s['index']??-1)>104 || $ids!==(array)($s['ids']??[]))
                throw new RuntimeException('104er Seiten weichen vom gespeicherten Lauf ab.');
            $s['status']='WRITING';$s['error']='';
            update_option('robotik_first_publish_state_v1',$s,false);
        }
        if(($s['status']??'')==='WRITING')$s=Robotik_Publish::advance();
        if(($s['status']??'')==='BLOCKED')
            throw new RuntimeException('104er Veroeffentlichung gestoppt: '.($s['error']??'Konflikt'));
        if(($s['status']??'')==='COMPLETE') {
            if((int)($s['verified']??0)!==104 || (int)($s['index']??0)!==104)
                throw new RuntimeException('104er Abschluss ist unvollstaendig.');
            $after=Robotik_Publish::preview();
            if(empty($after['valid']) || (int)$after['counts']['publish']!==104)
                throw new RuntimeException('104 alte Seiten sind nicht oeffentlich.');
            return 'veroeffentlichen';
        }
        if(($s['status']??'')!=='WRITING')
            throw new RuntimeException('Unbekannter alter 104er Status.');
        return 'altseiten';
    }
    private static function stagePublication():string {
        $s=get_option('robotik_v65_publication_state',[]);
        if(!is_array($s))throw new RuntimeException('V65-Zustand nicht lesbar.');
        // Correct a V78 0.4.12 run paused at this phase after V63 completed.
        if(!isset($s['status'])) {
            $old=Robotik_Publish::preview();
            if(empty($old['valid']))throw new RuntimeException('104 Altseiten nicht eindeutig.');
            if((int)($old['counts']['publish']??0)!==104)return 'altseiten';
        }
        if(!isset($s['status'])) {
            $p=Robotik_V65_Publication::preview(); // one existing decision/owner
            if(empty($p['ready'])||count((array)($p['items']??[]))!==68)
                throw new RuntimeException('Originale 68 Seiten nicht freigabefaehig: '.($p['notice']??''));
            if((int)$p['drafts']===0 && (int)$p['published']===68) {
                $s=['status'=>'COMPLETE','index'=>68,'total'=>68,'verified'=>68,
                    'completed_at'=>gmdate('c'),'already_published'=>68,'published'=>0];
            }else{
                $s=['status'=>'WRITING','index'=>0,'total'=>68,'items'=>$p['items'],
                    'published'=>0,'already_published'=>0,'error'=>'','started_at'=>gmdate('c')];
            }
            update_option('robotik_v65_publication_state',$s,false);
        }
        if(($s['status']??'')==='BLOCKED'){
            Robotik_V65_Publication::resumeSaved();
            $s=get_option('robotik_v65_publication_state',[]);
        }
        if(($s['status']??'')==='WRITING')$s=Robotik_V65_Publication::advance();
        if(($s['status']??'')==='BLOCKED')
            throw new RuntimeException('Vertraute 68er Veroeffentlichung gestoppt: '.($s['error']??'Unbekannter Konflikt'));
        if(($s['status']??'')==='COMPLETE'){
            if((int)($s['verified']??0)!==68||(int)($s['index']??0)!==68)
                throw new RuntimeException('68er Veroeffentlichungsabschluss fehlt.');
            return 'nachtrag';
        }
        if(($s['status']??'')!=='WRITING')throw new RuntimeException('Unbekannter 68er Veroeffentlichungsstatus.');
        return 'veroeffentlichen';
    }
    private static function stageFollowup():string {
        $s=get_option('robotik_v77_fachnachtrag_state',[]);
        if(!is_array($s))throw new RuntimeException('64er Status nicht lesbar.');
        if(!isset($s['status'])) {
            $p=Robotik_V77_Fachnachtrag::plan();
            if($p['errors']||(int)count($p['tasks'])!==64||(int)$p['done']!==0||(int)$p['remaining']!==64)
                throw new RuntimeException('Fachnachtrag nicht sauber, keine doppelten Inhalte: '.implode(' | ',array_slice($p['errors'],0,2)));
            $s=['status'=>'WRITING','index'=>0,'total'=>64,
                'prior_pages'=>$p['prior_pages'],'prior_terms'=>$p['prior_terms'],
                'manifest'=>self::manifest(),'error'=>'','started'=>gmdate('c')];
            update_option('robotik_v77_fachnachtrag_state',$s,false);
        }
        if(($s['status']??'')==='BLOCKED'){
            Robotik_V77_Fachnachtrag::resumeSaved();
            $s=get_option('robotik_v77_fachnachtrag_state',[]);
        }
        if(($s['status']??'')==='WRITING')$s=Robotik_V77_Fachnachtrag::advance();
        if(($s['status']??'')==='BLOCKED')
            throw new RuntimeException('64er Fachnachtrag gestoppt: '.($s['error']??'Unbekannter Konflikt'));
        if(($s['status']??'')==='COMPLETE'){
            if((int)($s['verified']??0)!==64||(int)($s['index']??0)!==64)
                throw new RuntimeException('Nachtrag-Endnachweis 64/64 fehlt.');
            return 'abgeschlossen';
        }
        if(($s['status']??'')!=='WRITING')throw new RuntimeException('Unbekannter Fachnachtragstatus.');
        return 'nachtrag';
    }
    public static function advance():array {
        self::authorized();
        $state=get_option(self::STATE,[]);
        if(!is_array($state)||($state['status']??'')!=='RUNNING')
            return is_array($state)?$state:['status'=>'BLOCKED'];
        if(!add_option(self::LOCK,time(),'','no')){
            $age=(int)get_option(self::LOCK,0);
            if($age>0 && time()-$age>180)delete_option(self::LOCK);
            return $state+['busy'=>true];
        }
        try {
            if(empty($state['authorized_once'])||
               !hash_equals((string)$state['manifest'],self::manifest()))
                throw new RuntimeException('Freigabe oder Originalfachplan geaendert.');
            switch($state['phase']){
                case 'uebernehmen':$new=self::stageImport();break;
                case 'altseiten':$new=self::stageOldPages();break;
                case 'veroeffentlichen':$new=self::stagePublication();break;
                case 'nachtrag':$new=self::stageFollowup();break;
                default:throw new RuntimeException('Unbekannte Ablaufphase.');
            }
            $state['phase']=$new;
            if($new==='abgeschlossen') {
                $state['status']='COMPLETE';
                $state['finished_utc']=gmdate('c');
                $state['verified']=['original_import'=>227,'original_published_pages'=>104,'new_published_pages'=>68,
                    'approved_followup_pages'=>16,'approved_followup_categories'=>48,
                    'manifest_page_positions'=>188,'manifest_wp_categories'=>296];
            }
            update_option(self::STATE,$state,false);
        }catch(Throwable $e){
            $state['status']='BLOCKED';$state['error']=$e->getMessage();
            update_option(self::STATE,$state,false);
        }finally{delete_option(self::LOCK);}
        return $state;
    }
    public static function tick():void {
        self::authorized();check_ajax_referer('robotik_v78_tick');
        $s=self::advance();
        $totals=['uebernehmen'=>227,'altseiten'=>104,'veroeffentlichen'=>68,'nachtrag'=>64];
        $sources=['uebernehmen'=>'robotik_v63_delta_state','altseiten'=>'robotik_first_publish_state_v1','veroeffentlichen'=>'robotik_v65_publication_state',
            'nachtrag'=>'robotik_v77_fachnachtrag_state'];
        $phase=$s['phase']??'uebernehmen';
        $sub=get_option($sources[$phase]??'robotik_v77_fachnachtrag_state',[]);
        wp_send_json_success(['status'=>$s['status']??'BLOCKED','phase'=>$phase,
            'done'=>(int)($sub['index']??0),'total'=>(int)($totals[$phase]??64),
            'error'=>(string)($s['error']??''),'busy'=>!empty($s['busy'])]);
    }
    public static function export():void {
        self::authorized();check_admin_referer('robotik_v78_export');
        $s=get_option(self::STATE,[]);
        if(!is_array($s)||($s['status']??'')!=='COMPLETE')
            wp_die('Ein zusammenfassender Abschlussbericht steht erst nach den 64 letzten Aufgaben bereit.');
        $report=['schema'=>'robotik-v78-einmaliger-gesamtabschluss-v1','date_utc'=>gmdate('c'),
            'status'=>$s['status'],'approved_once'=>!empty($s['authorized_once']),
            'started_utc'=>$s['started_utc']??null,'finished_utc'=>$s['finished_utc']??null,
            'verified'=>$s['verified']??null,'manifest_sha256'=>$s['manifest'],
            'phase_states'=>[
                'import'=>get_option('robotik_v63_delta_state',[]),
                'original_pages_publication'=>get_option('robotik_first_publish_state_v1',[]),
                'publication'=>get_option('robotik_v65_publication_state',[]),
                'followup'=>get_option('robotik_v77_fachnachtrag_state',[])],
            'old_google_url_hold_cleared_editorially'=>16,
            'google_api_requests_by_this_workflow'=>0,'second_writer'=>false,
            'additional_v76_type_candidates_not_imported'=>11];
        nocache_headers();header('Content-Type: application/json; charset=UTF-8');
        header('Content-Disposition: attachment; filename="robotik-gesamtabschluss-'.gmdate('Ymd-His').'.json"');
        echo wp_json_encode($report,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES|JSON_PRETTY_PRINT);exit;
    }
    public static function screen():void {
        self::authorized();$s=get_option(self::STATE,[]);
        echo '<div class="wrap"><h1>Robotik – gesamter Kategorieabschluss</h1>';
        echo '<p><strong>Ein Plugin, eine Freigabe, ein automatischer Ablauf:</strong> bestehenden 227er Import abschliessen, 104 vorhandene Seiten oeffentlich machen, 68 neue Seiten veroeffentlichen und 16 weitere Typseiten mit 48 Rubriken ohne Google-Sperre nachtragen. Bereits Erledigtes bleibt erhalten. Gewerbe/Industrie werden nicht erweitert.</p>';
        if(!is_array($s)||!isset($s['status'])){
            try{$p=self::initialCheck();}catch(Throwable $e){$p=['error'=>$e->getMessage()];}
            if(!empty($p['error']))echo '<div class="notice notice-error"><p>'.esc_html($p['error']).'</p></div>';
            else{
                echo '<p><strong>Vorhandener Import:</strong> '.(int)$p['legacy_index'].'/227 · Status '.esc_html($p['legacy_state']).'</p>';
                $token=hash('sha256',$p['manifest'].'|'.$p['legacy_state'].'|'.$p['legacy_index'].'|'.$p['phase']);
                echo '<form method="post" action="'.esc_url(admin_url('admin-post.php')).'">';
                wp_nonce_field('robotik_v78_start');
                echo '<input type="hidden" name="action" value="robotik_v78_start">';
                echo '<input type="hidden" name="robotik_v78_token" value="'.esc_attr($token).'">';
                echo '<p><label><input type="checkbox" name="robotik_v78_approve" value="1" required> Ich genehmige einmalig alle noch fehlenden Teile des bestehenden Kategorieplans einschließlich Veröffentlichung der 104 alten, 68 weiteren und 16 zusätzlichen Fachseiten; auch leere Seiten dürfen sichtbar werden.</label></p>';
                submit_button('Gesamten Robotik-Kategorieablauf EINMAL abschliessen','primary');echo '</form>';
            }
        }else{
            $st=(string)$s['status'];
            echo '<p id="robotik-v78-progress"><strong>Gesamtstatus: </strong>'.esc_html($st).' · '.esc_html((string)($s['phase']??'')).'</p>';
            if($st==='BLOCKED'){
                echo '<div class="notice notice-error"><p>Der automatische Ablauf wurde bei einem realen Konflikt gestoppt: '.esc_html((string)($s['error']??'')).'. Der gespeicherte Stand bleibt erhalten, kein erneuter Start.</p></div>';
                echo '<form method="post" action="'.esc_url(admin_url('admin-post.php')).'">';
                wp_nonce_field('robotik_v78_resume');
                echo '<input type="hidden" name="action" value="robotik_v78_resume">';
                submit_button('Gespeicherten Gesamtauftrag nach Fehlerbehebung fortsetzen','secondary');
                echo '</form>';
            }
            if($st==='RUNNING'){
                $nonce=wp_create_nonce('robotik_v78_tick');
                echo '<p>Der Ablauf setzt alle bereits freigegebenen Schritte nacheinander fort. Diese Seite waehrend der Ausfuehrung offen halten.</p>';
                echo '<script>(function(){var n='.wp_json_encode($nonce).',p=document.getElementById("robotik-v78-progress");function go(){var d=new FormData();d.append("action","robotik_v78_tick");d.append("_ajax_nonce",n);fetch(ajaxurl,{method:"POST",credentials:"same-origin",body:d}).then(r=>r.json()).then(j=>{if(!j.success)throw Error("WP-Antwort");var a=j.data;p.textContent=a.status+" · "+a.phase+" "+a.done+"/"+a.total+(a.error?" · "+a.error:"");if(a.status==="RUNNING")setTimeout(go,a.busy?800:100);else location.reload();}).catch(e=>{p.textContent="Verbindung unterbrochen. Seite neu laden setzt denselben gespeicherten Auftrag fort.";});}go();})();</script>';
            }
            if($st==='COMPLETE'){
                echo '<div class="notice notice-success"><p>Einmaliger Gesamtabschluss vollstaendig. Bestehender 227er Import, 104 alte veroeffentlichte Seiten, 68 neue veroeffentlichte Seiten und 64er Fachnachtrag wurden abgeschlossen.</p></div>';
                echo '<form method="post" action="'.esc_url(admin_url('admin-post.php')).'">';
                wp_nonce_field('robotik_v78_export');
                echo '<input type="hidden" name="action" value="robotik_v78_export">';
                submit_button('EINEN Gesamtabschlussbericht als JSON herunterladen','secondary');echo '</form>';
            }
        }
        echo '</div>';
    }
}
