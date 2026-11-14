<?php
if (!defined('ABSPATH')) { exit; }
/** One approved ADD-only structure import; no public-side, journal, affiliate or SEO writes. */
final class Wassertechnik_Kategorie_Importer {
    private const TARGET_HOST = 'wasser.oliver-beil.de';
    private const MANIFEST = 'assets/wassertechnik-wp-import-plan.json';
    private const LOCK_KEY = 'wassertechnik_import_015_lock';
    private const REPORT_KEY = 'wassertechnik_import_015_report';

    public static function boot(): void {
        add_action('admin_menu', [self::class, 'menu']);
        add_action('admin_post_wassertechnik_import_apply', [self::class, 'apply']);
    }
    private static function authorized(): bool {
        return current_user_can('manage_options') && strtolower((string)parse_url(home_url(), PHP_URL_HOST)) === self::TARGET_HOST;
    }
    private static function plan() {
        $file = plugin_dir_path(__DIR__) . self::MANIFEST;
        if (!is_readable($file)) return new WP_Error('wt_manifest', 'Freigegebene W6-Importliste fehlt.');
        $raw = file_get_contents($file);
        $data = json_decode($raw, true);
        if (!is_array($data) || ($data['schema'] ?? '') !== 'wassertechnik-w6-import-v1' || !isset($data['entries']) || !is_array($data['entries'])) return new WP_Error('wt_manifest', 'Ungültiger Importplan.');
        $rows = $data['entries'];
        if (count($rows) !== 218) return new WP_Error('wt_count', 'W6-Importliste nicht vollständig.');
        $owners=[]; $pagepaths=[]; $cats=[]; $numPages=0; $numCats=0;
        foreach ($rows as $r) {
            if (!is_array($r) || empty($r['owner_id']) || !in_array(($r['kind'] ?? ''), ['page','category'], true)) return new WP_Error('wt_owner', 'Ungültiger Datensatz.');
            $owner=(string)$r['owner_id'];
            if (isset($owners[$owner])) return new WP_Error('wt_duplicate_owner', 'Doppelte Owner-ID.');
            $owners[$owner] = true;
            if ($r['kind'] === 'page') {
                $path=(string)($r['path'] ?? '');
                if (!$path || !preg_match('~^[a-z0-9-]+(?:/[a-z0-9-]+)*$~D', $path) || isset($pagepaths[$path])) return new WP_Error('wt_pagepath', 'Ungültiger oder doppelter Seitenpfad.');
                $pagepaths[$path] = true; ++$numPages;
            } else {
                $slug=(string)($r['slug'] ?? '');
                if (!$slug || !preg_match('/^[a-z0-9-]+$/D', $slug) || isset($cats[$slug])) return new WP_Error('wt_slug', 'Ungültiger oder doppelter Kategorie-Slug.');
                $cats[$slug] = true; ++$numCats;
            }
        }
        if ($numPages !== 113 || $numCats !== 105) return new WP_Error('wt_counts', '113 Seiten und 105 Kategorien erforderlich.');
        foreach ($rows as $r) {
            if ($r['kind'] === 'page' && !empty($r['parent_path']) && !isset($pagepaths[$r['parent_path']])) return new WP_Error('wt_parent', 'Eine übergeordnete Seite fehlt.');
            if ($r['kind'] === 'category' && !isset($pagepaths[$r['product_path'] ?? ''])) return new WP_Error('wt_product', 'Eine übergeordnete Produktseite fehlt.');
        }
        usort($rows, static function($a,$b) {
            if ($a['kind'] !== $b['kind']) return $a['kind'] === 'page' ? -1 : 1;
            if ($a['kind'] === 'category') return strcmp($a['slug'], $b['slug']);
            $depth = substr_count($a['path'],'/') <=> substr_count($b['path'],'/');
            return $depth ?: strcmp($a['path'],$b['path']);
        });
        return ['entries'=>$rows, 'digest'=>hash('sha256',$raw)];
    }
    private static function inventory(array $rows) {
        $allPages=get_posts(['post_type'=>'page','post_status'=>'any','posts_per_page'=>-1,'suppress_filters'=>true]);
        $allTerms=get_terms(['taxonomy'=>'category','hide_empty'=>false]);
        if (is_wp_error($allTerms) || !is_array($allPages) || !is_array($allTerms)) return new WP_Error('wt_inventory', 'WordPress-Bestand nicht lesbar.');
        $pages=[]; $terms=[]; $owners=[];
        foreach($allPages as $p){
            $uri=get_page_uri($p); if(isset($pages[$uri])) return new WP_Error('wt_existing_page_duplicate', 'WordPress enthält doppelte Seitenpfade.');
            $owner=(string)get_post_meta($p->ID,'_wt_owner_id',true);
            if($owner && isset($owners['p:'.$owner])) return new WP_Error('wt_existing_owner_duplicate', 'Doppelte importierte Seiten-ID.');
            $pages[$uri]=['id'=>(int)$p->ID,'owner'=>$owner]; if($owner)$owners['p:'.$owner]=$uri;
        }
        foreach($allTerms as $term){
            if(isset($terms[$term->slug])) return new WP_Error('wt_existing_category_duplicate','WordPress enthält doppelte Kategorie-Slugs.');
            $owner=(string)get_term_meta($term->term_id,'_wt_owner_id',true);
            if($owner && isset($owners['c:'.$owner])) return new WP_Error('wt_existing_owner_duplicate','Doppelte importierte Kategorie-ID.');
            $terms[$term->slug]=['id'=>(int)$term->term_id,'owner'=>$owner]; if($owner)$owners['c:'.$owner]=$term->slug;
        }
        $pending=0; $existing=0; $conflicts=[];
        foreach($rows as $r){
            $isPage=$r['kind']==='page'; $key=$isPage?$r['path']:$r['slug'];
            $entry=$isPage?($pages[$key]??null):($terms[$key]??null);
            $idKey=($isPage?'p:':'c:').$r['owner_id'];
            if($entry){ if($entry['owner']!==$r['owner_id'])$conflicts[]=$key;else$existing++; }
            elseif(isset($owners[$idKey]))$conflicts[]=$key;
            else $pending++;
        }
        return ['pending'=>$pending,'existing'=>$existing,'conflicts'=>$conflicts,'pages'=>$pages,'terms'=>$terms];
    }
    public static function menu(): void {
        add_submenu_page('wassertechnik-kategorie','W4-Strukturimport','W4-Strukturimport','manage_options','wassertechnik-import',[self::class,'screen']);
    }
    public static function screen(): void {
        if(!current_user_can('manage_options'))wp_die('Administratorrechte erforderlich.');
        echo '<div class="wrap"><h1>Wassertechnik – Gesamtimport W6 (113 Seiten, 105 Kategorien)</h1>';
        if(!self::authorized()){echo '<p><strong>GESPERRT:</strong> nicht die gebundene Wassertechnik-Website.</p></div>';return;}
        $plan=self::plan();if(is_wp_error($plan)){echo '<p>'.esc_html($plan->get_error_message()).'</p></div>';return;}
        $inv=self::inventory($plan['entries']);if(is_wp_error($inv)){echo '<p>'.esc_html($inv->get_error_message()).'</p></div>';return;}
        echo '<p>Das ist ein einzelner ADD-only-Strukturimport: keine veröffentlichten Artikel, keine SEO-Kosten, keine fremden Seiten.</p>';
        echo '<p><strong>Bereits zugeordnet:</strong> '.(int)$inv['existing'].' · <strong>Noch anzulegen:</strong> '.(int)$inv['pending'].' · <strong>Konflikte:</strong> '.count($inv['conflicts']).'</p>';
        if($inv['conflicts']){echo '<p><strong>GESPERRT:</strong> vorhandene WordPress-Objekte passen nicht zu W6. '.esc_html(implode(', ',array_slice($inv['conflicts'],0,10))).'</p></div>';return;}
        if(get_transient(self::LOCK_KEY)){echo '<p>Ein Importlauf ist bereits aktiv. Keine doppelte Ausführung.</p></div>';return;}
        if(!$inv['pending']){echo '<p><strong>Fertig.</strong> Alle 218 WordPress-Ziele sind durch Owner zugeordnet.</p></div>';return;}
        echo '<form method="post" action="'.esc_url(admin_url('admin-post.php')).'">';
        wp_nonce_field('wassertechnik_import_015_approval');
        echo '<input type="hidden" name="action" value="wassertechnik_import_apply">';
        echo '<input type="hidden" name="plan_digest" value="'.esc_attr($plan['digest']).'">';
        echo '<p><label><input type="checkbox" name="approval" value="yes" required> Ich gebe die einmalige ADD-only-Anlage fehlender Wassertechnik-Seiten und Kategorien ausdrücklich frei.</label></p>';
        submit_button('W6-Struktur einmalig übernehmen','primary','submit',false);
        echo '</form></div>';
    }
    public static function apply(): void {
        if(!self::authorized())wp_die('Import nur für berechtigte Admins auf gebundener Wassertechnik-Site.');
        check_admin_referer('wassertechnik_import_015_approval');
        if(($_POST['approval'] ?? '')!=='yes')wp_die('Keine ausdrückliche Importfreigabe.');
        $plan=self::plan();if(is_wp_error($plan))wp_die(esc_html($plan->get_error_message()));
        $posted=sanitize_text_field(wp_unslash($_POST['plan_digest'] ?? ''));
        if(!hash_equals($plan['digest'],$posted))wp_die('Die Importvorlage wurde seit der Vorschau geändert.');
        if(get_transient(self::LOCK_KEY))wp_die('Import gesperrt: anderer Lauf aktiv.');
        set_transient(self::LOCK_KEY,1,15*MINUTE_IN_SECONDS);
        $addedPages=[];$addedTerms=[];$error=null;
        try {
            $inv=self::inventory($plan['entries']);
            if(is_wp_error($inv))throw new RuntimeException($inv->get_error_message());
            if($inv['conflicts'])throw new RuntimeException('Bestehende WordPress-Pfade/Kategorien kollidieren: keine Änderung.');
            $pageIds=[];foreach($inv['pages'] as $path=>$a)$pageIds[$path]=$a['id'];
            foreach($plan['entries'] as $r){
                if($r['kind']!=='page')continue;
                $path=$r['path'];if(isset($inv['pages'][$path]))continue;
                $parent=$r['parent_path']??'';
                if($parent&&!isset($pageIds[$parent]))throw new RuntimeException('Elternseite nicht gefunden: '.$parent);
                $parts=explode('/',$path);$slug=end($parts);
                $id=wp_insert_post(['post_type'=>'page','post_status'=>'draft','post_title'=>$r['title'],'post_name'=>$slug,'post_parent'=>$parent? $pageIds[$parent]:0,'post_content'=>'','comment_status'=>'closed','ping_status'=>'closed','meta_input'=>['_wt_owner_id'=>$r['owner_id']]],true);
                if(is_wp_error($id) || !$id)throw new RuntimeException('Seitenanlage fehlgeschlagen: '.$path);
                $addedPages[]=(int)$id;$pageIds[$path]=(int)$id;
            }
            foreach($plan['entries'] as $r){
                if($r['kind']!=='category')continue;
                $slug=$r['slug'];if(isset($inv['terms'][$slug]))continue;
                $prod=$r['product_path'];if(!isset($pageIds[$prod]))throw new RuntimeException('Produktbezug fehlt: '.$prod);
                $t=wp_insert_term($r['title'],'category',['slug'=>$slug,'description'=>'Wassertechnik-Produktbereich: '.$prod]);
                if(is_wp_error($t) || empty($t['term_id']))throw new RuntimeException('Kategorienanlage fehlgeschlagen: '.$slug);
                $termId=(int)$t['term_id'];$addedTerms[]=$termId;
                update_term_meta($termId,'_wt_owner_id',$r['owner_id']);
                update_term_meta($termId,'_wt_product_page_id',$pageIds[$prod]);
            }
            // Exactly one source-of-truth readback after the write run.
            $check=self::inventory($plan['entries']);
            if(is_wp_error($check)||$check['pending']!==0||$check['conflicts'])throw new RuntimeException('WP-Rücklesung stimmt nicht mit 218 Zielen überein.');
            update_option(self::REPORT_KEY,['completed_utc'=>gmdate('c'),'created_pages'=>count($addedPages),'created_categories'=>count($addedTerms),'total'=>218],false);
        } catch (Throwable $e) { $error=$e->getMessage();
            foreach(array_reverse($addedTerms) as $termId)wp_delete_term($termId,'category');
            foreach(array_reverse($addedPages) as $id)wp_delete_post($id,true);
        }
        delete_transient(self::LOCK_KEY);
        if($error)wp_die(esc_html('Import abgebrochen, nur neu angelegte Objekte dieses Laufs zurückgenommen: '.$error));
        wp_safe_redirect(admin_url('admin.php?page=wassertechnik-import'));exit;
    }
}
