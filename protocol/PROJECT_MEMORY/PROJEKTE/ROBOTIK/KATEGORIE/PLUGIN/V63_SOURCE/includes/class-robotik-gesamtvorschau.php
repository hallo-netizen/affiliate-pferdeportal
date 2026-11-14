<?php
/**
 * Robotik V62: Ausdruecklich nur lesender SOLL-/WordPress-IST-Abgleich.
 * Weder WP-Inhalte noch Plugin-Optionen werden beschrieben. Importer bleibt unveraendert.
 */
if (!defined('ABSPATH')) { exit; }

final class Robotik_Kategorie_Gesamtvorschau {
    private const MANIFEST = __DIR__ . '/../assets/robotik-v62-sollvorschau.json';
    private const META = '_robotik_kategorie_node_id';
    private const MANIFEST_SHA256 = '9acdedb78c04ddc431d891dc5495b01b93796568952b5442ff36a3817ec4cb29';

    public static function boot(): void {
        add_action('admin_post_robotik_v62_preview_export', [self::class, 'export']);
        add_action('admin_menu', [self::class, 'menu'], 31);
    }
    public static function menu(): void {
        add_submenu_page('robotik-kategorie', 'Robotik Gesamtvorschau', 'Gesamtvorschau (nur lesend)', 'manage_options', 'robotik-gesamtvorschau', [self::class, 'screen']);
    }
    public static function source(): array {
        if (!is_readable(self::MANIFEST)) throw new RuntimeException('V62-Sollprofil fehlt. Keine alte Importliste als Ersatz.');
        if (!hash_equals(self::MANIFEST_SHA256,(string)hash_file('sha256',self::MANIFEST))) throw new RuntimeException('V62-Sollprofil seit Freigabe geaendert. Nur-lesende Vorschau blockiert.');
        $raw=file_get_contents(self::MANIFEST);
        $data=json_decode($raw, true);
        if (!is_array($data) || ($data['schema']??'')!=='robotik-wp-preview-soll-v62-v1'
            || ($data['mode']??'')!=='READ_ONLY_PREVIEW_NO_WRITES'
            || count((array)($data['pages']??[]))!==188
            || count((array)($data['content_categories']??[]))!==296
            || count((array)($data['editorial_priority_phrases']??[]))!==26
            || count((array)($data['holds']??[]))!==16) {
            throw new RuntimeException('V62-Sollprofil unvollstaendig; nichts freigeben.');
        }
        $ids=[];$paths=[];$owners=[];$types=0;$groups=0;
        foreach ($data['pages'] as $p) {
            if (!is_array($p)||empty($p['source_id'])||empty($p['path'])||!is_array($p['path'])) throw new RuntimeException('Seitenziel unvollstaendig.');
            $id=(string)$p['source_id'];$path=implode(' > ', $p['path']);
            if (isset($ids[$id])||isset($paths[$path])) throw new RuntimeException('Doppelter Seiten-Identifier oder Seitenpfad im Sollprofil.');
            $ids[$id]=true;$paths[$path]=true;
            if (($p['role']??'')==='product') {$types++;$owners[$id]=true;}
            elseif(($p['role']??'')==='group') {$groups++;} else throw new RuntimeException('Unbekannte Seitenrolle.');
        }
        if ($types!==141||$groups!==47) throw new RuntimeException('Seitenrollenzahlen stimmen nicht.');
        $catids=[];$oldcats=0;
        foreach ($data['content_categories'] as $c) {
            $id=(string)($c['source_id']??'');
            if ($id===''||isset($catids[$id])||!isset($owners[$c['owner_id']??''])||count((array)($c['topics']??[]))<3) throw new RuntimeException('Unklare Inhaltskategorie oder Besitzer.');
            $catids[$id]=true;
            if(($c['source']??'')==='ALTPLAN_0_4_7')$oldcats++;
        }
        if ($oldcats!==89) throw new RuntimeException('Bisheriger Kategorienbestand falsch.');
        return $data;
    }
    private static function pathKey(array $parts): string {
        // WordPress-Umlauttitel unveraendert; kein raten von Slugs/IDs.
        return implode(' / ',array_map(static function($v){return function_exists('mb_strtolower')?mb_strtolower(trim((string)$v),'UTF-8'):strtolower(trim((string)$v));},$parts));
    }
    private static function sitePaths(array $pages): array {
        $byId=[];$paths=[];$issues=[];
        foreach ($pages as $p) {
            $id=(int)($p['id']??0);
            if ($id>0)$byId[$id]=$p;
        }
        foreach($byId as $id=>$post) {
            $seen=[];$walk=$id;$arr=[];$bad='';
            while($walk>0) {
                if(isset($seen[$walk])){$bad='Zyklische Elternbeziehung: '.$id;break;}
                $seen[$walk]=true;
                if(!isset($byId[$walk])){$bad='Elternseite nicht in Bestandsaufnahme: '.$id.' -> '.$walk;break;}
                array_unshift($arr,(string)$byId[$walk]['title']);
                $walk=(int)($byId[$walk]['parent_id']??0);
            }
            if($bad!==''){$issues[]=$bad;continue;}
            $key=self::pathKey($arr);
            $paths[$key][]=$id;
        }
        return [$paths,$issues];
    }
    private static function markerIndex(array $items, bool $isPage): array {
        $out=[];
        foreach($items as $x) {
            $id=(int)($x['id']??0);if(!$id)continue;
            $m=$isPage?get_post_meta($id,self::META,true):get_term_meta($id,self::META,true);
            if(is_string($m)&&$m!=='')$out[$m][]=$id;
        }
        return $out;
    }
    public static function collect(?array $liveInventory = null, ?array $preloadedSource = null): array {
        if(!current_user_can('manage_options'))throw new RuntimeException('Keine Berechtigung.');
        $source=$preloadedSource ?? self::source();
        $inventory=$liveInventory ?? Robotik_Kategorie_Inventory::collect();
        $isComplete=!empty($inventory['pages']['complete']) && !empty($inventory['categories']['complete']);
        [$pagePaths,$pathIssues]=self::sitePaths((array)($inventory['pages']['items']??[]));
        $pageMarkers=self::markerIndex((array)($inventory['pages']['items']??[]),true);
        $catMarkers=self::markerIndex((array)($inventory['categories']['items']??[]),false);
        $wpPages=[];foreach((array)($inventory['pages']['items']??[]) as $p)$wpPages[$p['id']]=$p;
        $wpCats=[];foreach((array)($inventory['categories']['items']??[]) as $p)$wpCats[$p['id']]=$p;
        $wpCatsSlug=[];foreach($wpCats as $p)$wpCatsSlug[(string)$p['slug']][]=$p['id'];
        $counts=['old_page_id_verified'=>0,'old_page_unmatched'=>0,'page_exact_path_unlinked'=>0,'page_identity_or_path_conflicts'=>0,'new_page_candidates'=>0,'new_pages_found_unlinked'=>0,'legacy_term_id_verified'=>0,'legacy_term_unmatched'=>0,'legacy_term_conflicts'=>0,'new_term_candidates'=>0];
        $pages=[];
        foreach($source['pages'] as $p) {
            $legacy=!empty($p['legacy']);$marker=$pageMarkers[$p['source_id']]??[];$path=self::pathKey($p['path']);$matches=$pagePaths[$path]??[];
            $row=['source_id'=>$p['source_id'],'path'=>$p['path'],'role'=>$p['role'],'origin'=>$p['origin'],'review_hold'=>$p['review_hold'],'legacy'=>$legacy,'status'=>'','wp_id_confirmed'=>null,'wp_candidate_ids'=>[]];
            if(count($marker)>1) {$row['status']='CONFLICT_DUPLICATE_META';$row['wp_candidate_ids']=$marker;$counts['page_identity_or_path_conflicts']++;}
            elseif(count($marker)===1){
                $id=$marker[0];$x=$wpPages[$id]??null;
                if(!$x) {$row['status']='CONFLICT_MISSING_WP_ID';$counts['page_identity_or_path_conflicts']++;}
                elseif(in_array($id,$matches,true) && (string)$x['title']===(string)$p['title']){$row['status']='CONFIRMED_META_AND_PATH';$row['wp_id_confirmed']=$id;if($legacy)$counts['old_page_id_verified']++;}
                else {$row['status']='REVIEW_META_PATH_OR_TITLE_CHANGED';$row['wp_id_confirmed']=$id;$counts['page_identity_or_path_conflicts']++;}
            }elseif(count($matches)>1){$row['status']='CONFLICT_DUPLICATE_PATH';$row['wp_candidate_ids']=$matches;$counts['page_identity_or_path_conflicts']++;}
            elseif(count($matches)===1){$row['status']='REVIEW_EXACT_PATH_UNLINKED';$row['wp_candidate_ids']=$matches;$counts['page_exact_path_unlinked']++;if(!$legacy)$counts['new_pages_found_unlinked']++;}
            else{
                $row['status']=$legacy?'OLD_PLAN_NOT_VERIFIED_IN_LIVE_WP':'NEW_PAGE_PROPOSAL_NOT_WRITTEN';
                if($legacy)$counts['old_page_unmatched']++;else $counts['new_page_candidates']++;
            }
            $pages[]=$row;
        }
        $categories=[];
        foreach($source['content_categories'] as $c) {
            $legacy=$c['source']==='ALTPLAN_0_4_7';$markers=$catMarkers[$c['source_id']]??[];
            $row=['source_id'=>$c['source_id'],'owner_id'=>$c['owner_id'],'owner_path'=>$c['owner_path'],'short_label'=>$c['short_label'],'legacy'=>$legacy,'review_hold'=>$c['review_hold'],'status'=>'','wp_id_confirmed'=>null,'wp_candidate_ids'=>[]];
            if(count($markers)>1){$row['status']='CONFLICT_DUPLICATE_TERM_META';$row['wp_candidate_ids']=$markers;$counts['legacy_term_conflicts']++;}
            elseif(count($markers)===1){
                $id=$markers[0];$found=$wpCats[$id]??null;
                if(!$found || ($legacy && ($found['slug']??'')!==$c['original_slug'])){$row['status']='REVIEW_TERM_META_SLUG_MISMATCH';$row['wp_id_confirmed']=$id;$counts['legacy_term_conflicts']++;}
                else{$row['status']='CONFIRMED_TERM_META';$row['wp_id_confirmed']=$id;if($legacy)$counts['legacy_term_id_verified']++;}
            }elseif($legacy){
                $slug=(string)$c['original_slug'];$matches=$wpCatsSlug[$slug]??[];
                $row['status']=$matches?'REVIEW_TERM_SLUG_EXISTS_NO_META':'OLD_TERM_NOT_VERIFIED_IN_LIVE_WP';
                $row['wp_candidate_ids']=$matches;$counts['legacy_term_unmatched']++;
            }else{$row['status']='NEW_TERM_PROPOSAL_NOT_WRITTEN';$counts['new_term_candidates']++;}
            $categories[]=$row;
        }
        $issues=array_merge($pathIssues,(array)($inventory['issues']??[]));
        $issues[]= ['area'=>'SEO','detail'=>'16 SEO-HOLD-Paare nicht anhand verwertbarer Google-Ziel-URLs bestaetigt.'];
        $issues[]= ['area'=>'WORKFLOW','detail'=>'Der alte Erstimport bleibt auf 104/89. Dieses V62-Profil ist eine schreibfreie Vorschau, KEINE Importfreigabe.'];
        if(!$isComplete)$issues[]=['area'=>'LIVE','detail'=>'WordPress-Inventur unvollstaendig: aus fehlenden Treffern keine sichere Neuanlage ableiten.'];
        return ['schema'=>'robotik-v62-live-preview-v1','date_utc'=>gmdate('c'),'plugin_version'=>Robotik_Kategorie_Workflow::VERSION,
            'mode'=>'READ_ONLY_NO_WRITES_NO_API','site_url'=>home_url('/'),'plan_counts'=>$source['counts'],'site_inventory_complete'=>$isComplete,
            'live_counts'=>['pages'=>$inventory['pages']['count']??null,'categories'=>$inventory['categories']['count']??null,'posts'=>$inventory['posts']['count']??null,'hivepress_categories'=>$inventory['hivepress_listing_categories']['count']??null,'hivepress_listings'=>$inventory['hivepress_listings']['count']??null],
            'comparison_counts'=>$counts,'pages'=>$pages,'content_categories'=>$categories,
            'editorial_keyword_candidates'=>$source['editorial_priority_phrases'],'seo_holds'=>$source['holds'],
            'issues'=>$issues,'write_authorized'=>false,'import_profile_updated'=>false,'auto_actions_performed'=>0,
            'notes'=>'Unmarkierte Titel-/Pfadtreffer sind Kandidaten, nicht nachgewiesene Identitaeten. Neue Slugs werden NICHT erfunden. Kein neuer Import und keine SEO-Freigabe.'];
    }
    public static function export(): void {
        if(!current_user_can('manage_options'))wp_die('Keine Berechtigung.');
        check_admin_referer('robotik_v62_preview_export');
        try{$v=self::collect();}catch(Throwable $e){wp_die(esc_html($e->getMessage()));}
        nocache_headers();
        header('Content-Type: application/json; charset=UTF-8');
        header('Content-Disposition: attachment; filename="robotik-v62-wordpress-gesamtvorschau-'.gmdate('Ymd-His').'.json"');
        echo wp_json_encode($v,JSON_PRETTY_PRINT|JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE);exit;
    }
    public static function screen(): void {
        if(!current_user_can('manage_options'))wp_die('Keine Berechtigung.');
        echo '<div class="wrap"><h1>Robotik – gesamte WordPress-Vorschau</h1><p><strong>Nur lesend.</strong> V62-Soll gegen aktuelle WP-Seiten und Kategorien. Kein Import, keine Veraenderung von Inhalten, URLs oder Navigation, keine bezahlte API. Alte 104/89 bleiben im bisherigen Importer unveraendert.</p>';
        try{
            $v=self::collect();$c=$v['comparison_counts'];
            echo '<p><strong>SOLL:</strong> 188 Seiten (47 Gruppen, 141 Robotertypen), 296 individuelle Inhaltsrubriken. Davon eine neu benoetigte Hauptwelt Humanoide. 16 SEO-Faelle bleiben offen.</p>';
            echo '<p><strong>LIVE:</strong> '.(int)$v['live_counts']['pages'].' Seiten, '.(int)$v['live_counts']['categories'].' Kategorien, '.(int)$v['live_counts']['posts'].' Beitraege; Inventur '.($v['site_inventory_complete']?'vollstaendig':'NICHT vollstaendig').'.</p>';
            echo '<p>Alte Seiten anhand Originalkennung und Pfad belegt: <strong>'.(int)$c['old_page_id_verified'].'</strong> / 104. Alte Kategorien belegt: <strong>'.(int)$c['legacy_term_id_verified'].'</strong> / 89.</p>';
            echo '<p>Neue Seitenpositionen ohne eindeutigen bestehenden Treffer: <strong>'.(int)$c['new_page_candidates'].'</strong>, neue Inhaltsrubriken als Entwurf: <strong>'.(int)$c['new_term_candidates'].'</strong>. Offen: '.(int)$c['page_identity_or_path_conflicts'].' Seitenkonflikte und '.(int)$c['legacy_term_conflicts'].' Kategorienkonflikte. <strong>Diese Zahlen sind keine Freigabe zum Anlegen.</strong></p>';
            echo '<form method="post" action="'.esc_url(admin_url('admin-post.php')).'"><input type="hidden" name="action" value="robotik_v62_preview_export">';wp_nonce_field('robotik_v62_preview_export');submit_button('EINEN Gesamtbericht als JSON herunterladen (nur lesend)','secondary','submit',false);echo '</form>';
            echo '<h2>Was noch nicht freigegeben ist</h2><p>16 ungelöste Suchabsichts-Ueberschneidungen; aktuelle Live-Zuordnung; echte Neuanlagen/Slugs. Keine automatische Uebernahme in den alten Importplan.</p>';
            foreach(array_slice($v['issues'],0,5) as $issue){$msg=is_array($issue)?(($issue['detail']??$issue['area']??'')):(string)$issue;echo '<p>'.esc_html((string)$msg).'</p>';}
        }catch(Throwable $e){echo '<div class="notice notice-error"><p>'.esc_html($e->getMessage()).'</p></div>';}
        echo '</div>';
    }
}