<?php
if (!defined('ABSPATH')) { exit; }
/**
 * WT001 W35: ONE owner-safe 7-consumer-root/1-specialist-root WP import.
 * Data alone never performs a write. Admin nonce + one explicit approval for any write.
 */
final class Wassertechnik_Kategorie_Importer {
    private const HOST = 'wasser.oliver-beil.de';
    private const PLAN = 'ASSETS/W35_wordpress_importplan_219.json';
    private const LOCK = 'wassertechnik_w35_single_apply_lock';
    private const REPORT = 'wassertechnik_w35_single_apply_report';

    public static function boot(): void {
        add_action('admin_menu', [self::class, 'menu'], 40);
        add_action('admin_post_wassertechnik_w35_apply', [self::class, 'apply']);
        add_action('template_redirect', [self::class, 'redirect_legacy'], 1);
    }
    private static function authorized(): bool {
        return current_user_can('manage_options')
            && strtolower((string)wp_parse_url(home_url('/'), PHP_URL_HOST)) === self::HOST;
    }
    public static function plan(): array {
        $file=dirname(__DIR__).'/' . self::PLAN;
        if (!is_readable($file)) throw new RuntimeException('W35-Freigabedatei fehlt.');
        $raw=file_get_contents($file);
        $j=json_decode((string)$raw,true);
        if (!is_array($j) || ($j['schema'] ?? null)!=='wassertechnik-w35-one-time-wp-import-v1'
            || ($j['status']??null)!=='NUR_GESAMTPLAN_KEIN_WORDPRESS_SCHREIBEN'
            || !is_array($j['wp_targets'] ?? null) || count($j['wp_targets'])!==219
            || !is_array($j['redirects'] ?? null) || count($j['redirects'])!==17) {
            throw new RuntimeException('W35-Zielbestand ist nicht eindeutig.');
        }
        $id=[];$pp=[];$ct=[];$pages=[];$cats=[];$legacy=[];$moves=[];
        foreach($j['wp_targets'] as $r) {
            if(!is_array($r) || !in_array($r['kind'] ?? '', ['page','category'],true)
                || !is_string($r['owner_id'] ?? null) || ($r['owner_id']??'')===''
                || isset($id[$r['owner_id']])) throw new RuntimeException('Ungültige/doppelte Owner.');
            $id[$r['owner_id']]=true;
            if($r['kind']==='page') {
                $path=$r['path']??'';
                if(!is_string($path)||!preg_match('~^[a-z0-9-]+(?:/[a-z0-9-]+)*$~D',$path)
                   ||isset($pp[$path]))throw new RuntimeException('Ungültiger/doppelter Seitenpfad.');
                $pp[$path]=true; $pages[$r['owner_id']]=$r;
                $was=$r['legacy_path']??null;
                if($was!==null){
                    if(!is_string($was)||isset($legacy[$was]))throw new RuntimeException('Doppelter alter Pfad.');
                    $legacy[$was]=true;
                    if($was!==$path)$moves[$was]=$path;
                }
            }else{
                $slug=$r['slug']??'';
                if(!is_string($slug)||!preg_match('/^[a-z0-9-]+$/D',$slug)||isset($ct[$slug]))
                    throw new RuntimeException('Ungültiger/doppelter Kategorie-Slug.');
                $ct[$slug]=true;$cats[$r['owner_id']]=$r;
            }
        }
        if(count($pages)!==114||count($cats)!==105||count($moves)!==17)
            throw new RuntimeException('W35-Anzahl falsch: 114 Seiten, 105 Kategorien, 17 historische Pfade.');
        $roots=[];$industry=0;$pool=0;
        foreach($pages as $r){
            if($r['parent_owner_id']!==null && !isset($pages[$r['parent_owner_id']]))
                throw new RuntimeException('Elternseitenbezug nicht vorhanden.');
            if($r['parent_owner_id']===null) {
                $roots[]=$r['path'];
                if($r['path']==='industrie-grossanlagen')++$industry;
                if($r['path']==='pool-teichtechnik' && $r['owner_id']==='wt_main_pool_w27')++$pool;
            }
        }
        foreach($cats as $r)if(!isset($pages[$r['product_owner_id'] ?? '']))
            throw new RuntimeException('Kategorie ohne Produkt-Owner.');
        if(count($roots)!==8||$industry!==1||$pool!==1)
            throw new RuntimeException('7 Hauptbereiche + 1 Spezialzugang erforderlich.');
        foreach($j['redirects'] as $red) {
            if(!is_array($red)||($moves[$red['from']??'']??null)!==($red['to']??null))
                throw new RuntimeException('Redirect ist nicht aus einer realen 17er-Seitenverschiebung abgeleitet.');
            if(($pages[$red['owner_id']??'']['path']??null)!==$red['to'])
                throw new RuntimeException('Redirect hat falsche Owner-ID.');
        }
        $j['_source_sha256']=hash('sha256',(string)$raw);
        return $j;
    }
    private static function inventory(array $plan): array {
        $existingPages=get_posts(['post_type'=>'page','post_status'=>'any','posts_per_page'=>-1,
            'suppress_filters'=>true]);
        $existingTerms=get_terms(['taxonomy'=>'category','hide_empty'=>false]);
        if(!is_array($existingPages)||!is_array($existingTerms)||
            is_wp_error($existingPages)||is_wp_error($existingTerms))
            throw new RuntimeException('WordPress-Gesamtbestand kann nicht gelesen werden.');
        $paths=[];$pageOwners=[];$terms=[];$termOwners=[];$errors=[];
        foreach($existingPages as $p) {
            $key=trim((string)get_page_uri($p),'/');
            $id=(int)$p->ID;$owner=(string)get_post_meta($id,'_wt_owner_id',true);
            if(isset($paths[$key]))$errors[]='Doppelter WP-Pfad: '.$key;
            $row=['id'=>$id,'owner'=>$owner,'path'=>$key,'parent'=>(int)$p->post_parent,
                  'title'=>(string)$p->post_title,'status'=>(string)$p->post_status];
            $paths[$key]=$row;
            if($owner){
                if(isset($pageOwners[$owner]))$errors[]='Doppelter Seiten-Owner: '.$owner;
                $pageOwners[$owner]=$row;
            }
        }
        foreach($existingTerms as $t) {
            $key=(string)$t->slug;$owner=(string)get_term_meta((int)$t->term_id,'_wt_owner_id',true);
            if(isset($terms[$key]))$errors[]='Doppelter Kategorie-Slug: '.$key;
            $row=['id'=>(int)$t->term_id,'slug'=>$key,'owner'=>$owner];
            $terms[$key]=$row;
            if($owner){
                if(isset($termOwners[$owner]))$errors[]='Doppelter Kategorie-Owner: '.$owner;
                $termOwners[$owner]=$row;
            }
        }
        $missingPages=[];$missingCats=[];$changes=[];$ownerIds=[];
        foreach($plan['wp_targets'] as $r) {
            $owner=$r['owner_id'];
            if($r['kind']==='page'){
                $row=$pageOwners[$owner]??null;
                $new=$r['path'];$old=$r['legacy_path'];
                if($row){
                    $ownerIds[$owner]=$row['id'];
                    if($row['path']!==$new && $row['path']!==$old)
                        $errors[]='Owner-Pfad wurde unerwartet geändert: '.$owner;
                    if(isset($paths[$new]) && $paths[$new]['id']!==$row['id'])
                        $errors[]='Neue Zieladresse ist fremd belegt: '.$new;
                    if($old!==null && isset($paths[$old]) && $paths[$old]['id']!==$row['id'])
                        $errors[]='Alte Adresse ist fremd belegt: '.$old;
                    if($row['path']!==$new || $row['title']!==$r['title'])$changes[]=$owner;
                }else{
                    if(isset($paths[$new]) || ($old!==null && isset($paths[$old]))) {
                        $errors[]='Unzugeordnete Seite nicht überschreiben: '.$owner;
                    }
                    $missingPages[]=$owner;
                }
            }else{
                $row=$termOwners[$owner]??null;
                $slug=$r['slug'];
                if($row){
                    if($row['slug']!==$slug)$errors[]='Kategorie-Owner verschoben: '.$owner;
                }else{
                    if(isset($terms[$slug]))$errors[]='Fremde Beitragskategorie: '.$slug;
                    $missingCats[]=$owner;
                }
            }
        }
        $fingerprint=[];
        foreach($paths as $path=>$a)$fingerprint[]='p|'.$path.'|'.$a['id'].'|'.$a['owner'].'|'.$a['parent'].'|'.$a['title'].'|'.$a['status'];
        foreach($terms as $slug=>$a)$fingerprint[]='c|'.$slug.'|'.$a['id'].'|'.$a['owner'];
        sort($fingerprint,SORT_STRING);
        return [
            'conflicts'=>array_values(array_unique($errors)),
            'missing_pages'=>$missingPages,'missing_categories'=>$missingCats,
            'updates'=>$changes,'owner_ids'=>$ownerIds,
            'fingerprint'=>hash('sha256',implode("\n",$fingerprint)),
            'pages'=>$paths,'terms'=>$terms
        ];
    }
    private static function view_data(): array {
        if(!self::authorized())throw new RuntimeException('Administratorrechte und Zielsite erforderlich.');
        $plan=self::plan();$state=self::inventory($plan);
        return [$plan,$state];
    }
    public static function menu(): void {
        add_submenu_page('wassertechnik-kategorie','W35 – einmalige Zielstruktur',
            'W35 – Zielstruktur','manage_options','wassertechnik-w35-once',[self::class,'screen']);
    }
    public static function screen(): void {
        if(!self::authorized())wp_die('Nur Wassertechnik-Administratoren.');
        echo '<div class="wrap"><h1>Wassertechnik: 7 Hauptbereiche + 1 Fachzugang</h1>';
        try{[$plan,$state]=self::view_data();}catch(Throwable $e){
            echo '<p><strong>GESPERRT:</strong> '.esc_html($e->getMessage()).'</p></div>';return;
        }
        echo '<p>Eine Gesamtentscheidung: 114 Seiten (davon eine leere Pool-Hub-Seite als Entwurf), 105 Beitragskategorien. Alle 218 bestehenden W6-Owner werden beibehalten. 81 neue Produkte werden NICHT angelegt.</p>';
        echo '<p><strong>Bereits vorhanden:</strong> '.(219-count($state['missing_pages'])-count($state['missing_categories']))
            .' · <strong>Fehlende Seiten:</strong> '.count($state['missing_pages'])
            .' · <strong>Fehlende Kategorien:</strong> '.count($state['missing_categories'])
            .' · <strong>Bestehende Anpassungen:</strong> '.count($state['updates'])
            .' · <strong>Konflikte:</strong> '.count($state['conflicts']).'</p>';
        if($state['conflicts']){
            echo '<p><strong>GESPERRT:</strong> '.esc_html(implode(' | ',array_slice($state['conflicts'],0,6))).'</p></div>';return;
        }
        if(get_transient(self::LOCK)){echo '<p>Anderer Import aktiv – keine zweite Ausführung.</p></div>';return;}
        $pending=count($state['missing_pages'])+count($state['missing_categories'])+count($state['updates']);
        if(!$pending){echo '<p>Alle Zielobjekte vorhanden. Keine erneute Übernahme erforderlich.</p></div>';return;}
        echo '<p>17 alte Pfade erhalten bei tatsächlich durchgeführter Umordnung permanente 301-Weiterleitungen. Keine Website-Änderung ohne diese eine ausdrückliche Freigabe.</p>';
        echo '<form action="'.esc_url(admin_url('admin-post.php')).'" method="post">';
        wp_nonce_field('wassertechnik_w35_once');
        echo '<input type="hidden" name="action" value="wassertechnik_w35_apply">';
        echo '<input type="hidden" name="plan_sha" value="'.esc_attr($plan['_source_sha256']).'">';
        echo '<input type="hidden" name="wp_sha" value="'.esc_attr($state['fingerprint']).'">';
        echo '<p><label><input type="checkbox" required name="approval" value="yes"> Ich gebe exakt diesen einmaligen WordPress-Strukturimport samt gegebenenfalls notwendiger Umordnung ausdrücklich frei.</label></p>';
        submit_button('Einmaligen ADD-only-/Umordnungsimport ausführen','primary','submit',false);
        echo '</form></div>';
    }
    public static function apply(): void {
        if(!self::authorized())wp_die('Falsche Website oder keine Administratorrechte.');
        check_admin_referer('wassertechnik_w35_once');
        if(($_POST['approval']??null)!=='yes')wp_die('Ausdrückliche Gesamtfreigabe fehlt.');
        if(get_transient(self::LOCK))wp_die('Ein Importlauf ist bereits aktiv.');
        try{[$plan,$state]=self::view_data();}catch(Throwable $e){wp_die(esc_html($e->getMessage()));}
        $planSha=sanitize_text_field(wp_unslash($_POST['plan_sha']??''));
        $wpSha=sanitize_text_field(wp_unslash($_POST['wp_sha']??''));
        if(!hash_equals($plan['_source_sha256'],$planSha)
            || !hash_equals($state['fingerprint'],$wpSha))
            wp_die('Plan oder WordPress-Bestand wurde seit der Einmalvorschau verändert.');
        if($state['conflicts'])wp_die('WordPress-Owner oder Adressen kollidieren. Keine Änderung.');
        set_transient(self::LOCK,1,15*MINUTE_IN_SECONDS);
        $madePages=[];$madeCats=[];$oldPages=[];$error=null;
        try {
            $wantedPages=[];$wantedCats=[];
            foreach($plan['wp_targets'] as $r) {
                if($r['kind']==='page')$wantedPages[$r['owner_id']]=$r;
                else $wantedCats[$r['owner_id']]=$r;
            }
            $ids=$state['owner_ids'];
            $ordered=array_values($wantedPages);
            usort($ordered,static function($a,$b){
                $depth=substr_count($a['path'],'/')<=>substr_count($b['path'],'/');
                return $depth?:strcmp($a['path'],$b['path']);
            });
            // Parent IDs are the only placement decision. Descendants follow an existing moved parent.
            foreach($ordered as $r) {
                $oid=$r['owner_id'];
                if(isset($ids[$oid]))continue;
                $parent=$r['parent_owner_id'];
                if($parent!==null && !isset($ids[$parent]))throw new RuntimeException('Eltern-ID fehlt: '.$parent);
                $slug=basename(str_replace('/','/',$r['path']));
                $post=wp_insert_post([
                    'post_type'=>'page','post_status'=>'draft',
                    'post_title'=>$r['title'],'post_name'=>$slug,'post_content'=>'',
                    'post_parent'=>$parent===null?0:$ids[$parent],
                    'comment_status'=>'closed','ping_status'=>'closed',
                    'meta_input'=>['_wt_owner_id'=>$oid]
                ],true);
                if(is_wp_error($post)||!$post)throw new RuntimeException('Seitenanlage fehlgeschlagen: '.$oid);
                $ids[$oid]=(int)$post;$madePages[]=(int)$post;
            }
            // Update only existing pages. Two old roots can move; other descendants keep their IDs.
            foreach($ordered as $r) {
                $oid=$r['owner_id'];
                if(in_array($ids[$oid],$madePages,true))continue;
                $old=$state['pages'][$r['legacy_path']??'']??$state['pages'][$r['path']]??null;
                if(!$old || $old['owner']!==$oid || $old['id']!==$ids[$oid])
                    throw new RuntimeException('Bestehender Owner unerwartet geändert: '.$oid);
                $parent=$r['parent_owner_id'];
                $parentId=$parent===null?0:($ids[$parent]??0);
                if($parent!==null && !$parentId)throw new RuntimeException('Neue Eltern-ID fehlt: '.$oid);
                if($old['parent']!==$parentId || $old['title']!==$r['title']) {
                    $oldPages[]=['id'=>$old['id'],'parent'=>$old['parent'],'title'=>$old['title']];
                    $res=wp_update_post([
                        'ID'=>$old['id'],'post_parent'=>$parentId,'post_title'=>$r['title']
                    ],true);
                    if(is_wp_error($res)||!$res)throw new RuntimeException('Seitenumordnung fehlgeschlagen: '.$oid);
                }
            }
            foreach($wantedCats as $oid=>$r) {
                if(!in_array($oid,$state['missing_categories'],true))continue;
                if(!isset($ids[$r['product_owner_id']]))throw new RuntimeException('Produktseite fehlt für Kategorie.');
                $t=wp_insert_term($r['title'],'category',['slug'=>$r['slug'],
                    'description'=>'Wassertechnik-Produktseite: '.$r['product_path']]);
                if(is_wp_error($t)||empty($t['term_id']))throw new RuntimeException('Kategorieanlage fehlgeschlagen: '.$oid);
                $id=(int)$t['term_id'];$madeCats[]=$id;
                update_term_meta($id,'_wt_owner_id',$oid);
                update_term_meta($id,'_wt_product_page_id',$ids[$r['product_owner_id']]);
            }
            // Exactly one readback after the write run; no additional semantic/SEO decisions.
            $after=self::inventory($plan);
            if($after['conflicts'] || $after['missing_pages'] || $after['missing_categories'])
                throw new RuntimeException('Gesamt-WordPress-Rücklesung weicht ab.');
            foreach($wantedPages as $oid=>$r) {
                $row=$after['pages'][$r['path']]??null;
                if(!$row || $row['owner']!==$oid || $row['title']!==$r['title'])
                    throw new RuntimeException('Owner-/Pfad-/Titel-Rücklesung weicht ab: '.$oid);
            }
            update_option(self::REPORT,[
                'run_time'=>gmdate('c'),'created_pages'=>count($madePages),
                'created_categories'=>count($madeCats),
                'updated_pages'=>count($oldPages),'total'=>219
            ],false);
        }catch(Throwable $e){
            $error=$e->getMessage();
            foreach(array_reverse($madeCats) as $id)wp_delete_term($id,'category');
            foreach(array_reverse($oldPages) as $p)
                wp_update_post(['ID'=>$p['id'],'post_parent'=>$p['parent'],'post_title'=>$p['title']],true);
            foreach(array_reverse($madePages) as $id)wp_delete_post($id,true);
        }
        delete_transient(self::LOCK);
        if($error)wp_die(esc_html('Gesamtvorgang abgebrochen; neu angelegte und direkt geänderte Objekte zurückgenommen: '.$error));
        wp_safe_redirect(admin_url('admin.php?page=wassertechnik-w35-once'));exit;
    }
    public static function redirect_legacy(): void {
        if(strtolower((string)wp_parse_url(home_url('/'),PHP_URL_HOST))!==self::HOST
           ||!function_exists('is_404')||!is_404())return;
        try{$plan=self::plan();}catch(Throwable $e){return;}
        $request=(string)($_SERVER['REQUEST_URI']??'');
        $path=trim((string)wp_parse_url($request,PHP_URL_PATH),'/');
        foreach($plan['redirects'] as $r) {
            if($r['from']!==$path)continue;
            $target=get_page_by_path($r['to'],OBJECT,'page');
            if(!$target || $target->post_status!=='publish'
               || (string)get_post_meta((int)$target->ID,'_wt_owner_id',true)!==$r['owner_id'])return;
            $url=get_permalink((int)$target->ID);
            if($url){wp_safe_redirect($url,301);exit;}
            return;
        }
    }
}
