<?php
if (!defined('ABSPATH')) { exit; }
/** W34: ONE read-only WordPress inventory; no imports, URLs, SEO calls, or writes. */
final class Wassertechnik_W34_Inventory_Readback {
    private const SITE = 'wasser.oliver-beil.de';
    private const MANIFEST = 'assets/wassertechnik-wp-import-plan.json';
    private static function allowed(): bool {
        return current_user_can('manage_options')
            && strtolower((string)wp_parse_url(home_url('/'), PHP_URL_HOST)) === self::SITE;
    }
    public static function boot(): void {
        add_action('admin_menu', [self::class, 'menu'], 40);
    }
    public static function menu(): void {
        add_submenu_page('wassertechnik-kategorie', 'WordPress-Gesamtbestand',
            'WordPress-Gesamtbestand', 'manage_options',
            'wassertechnik-w34-bestand', [self::class, 'screen']);
    }
    public static function inspect(): array {
        if (!self::allowed()) throw new RuntimeException('Nur Administratoren der Wassertechnik-Website.');
        $file = dirname(__DIR__) . '/' . self::MANIFEST;
        if (!is_readable($file)) throw new RuntimeException('W6-Referenzliste fehlt.');
        $raw = file_get_contents($file);
        $data = json_decode((string)$raw, true);
        if (!is_array($data) || ($data['schema'] ?? '') !== 'wassertechnik-w6-import-v1'
            || !is_array($data['entries'] ?? null) || count($data['entries']) !== 218) {
            throw new RuntimeException('Unvollständige WP-Referenzliste.');
        }
        $wpPages = get_posts(['post_type'=>'page', 'post_status'=>'any',
            'posts_per_page'=>-1, 'suppress_filters'=>true]);
        $wpPosts = get_posts(['post_type'=>'post', 'post_status'=>'any',
            'posts_per_page'=>-1, 'suppress_filters'=>true]);
        $wpTerms = get_terms(['taxonomy'=>'category','hide_empty'=>false]);
        if (!is_array($wpPages) || !is_array($wpPosts) || !is_array($wpTerms)
            || is_wp_error($wpPages) || is_wp_error($wpPosts) || is_wp_error($wpTerms)) {
            throw new RuntimeException('WordPress-Gesamtbestand unvollständig.');
        }
        $all = []; $owners = []; $duplicate = [];
        foreach ($wpPages as $p) {
            $path = trim((string)get_page_uri($p), '/');
            if (isset($all['p:'.$path])) $duplicate[]='p:'.$path;
            $owner=(string)get_post_meta((int)$p->ID, '_wt_owner_id', true);
            $all['p:'.$path] = ['owner'=>$owner, 'id'=>(int)$p->ID, 'status'=>(string)$p->post_status];
            if ($owner) {
                if (isset($owners['p:'.$owner])) $duplicate[]='owner-p:'.$owner;
                $owners['p:'.$owner]=$path;
            }
        }
        foreach ($wpTerms as $term) {
            $slug=(string)$term->slug;
            if (isset($all['c:'.$slug])) $duplicate[]='c:'.$slug;
            $owner=(string)get_term_meta((int)$term->term_id, '_wt_owner_id', true);
            $all['c:'.$slug]=['owner'=>$owner, 'id'=>(int)$term->term_id, 'status'=>'term'];
            if ($owner) {
                if (isset($owners['c:'.$owner])) $duplicate[]='owner-c:'.$owner;
                $owners['c:'.$owner]=$slug;
            }
        }
        $mapped=0; $missing=0; $conflicts=[];
        $uniqueTargets=[];
        foreach ($data['entries'] as $r) {
            if (!is_array($r) || !in_array(($r['kind'] ?? ''), ['page','category'], true)
                || !is_string($r['owner_id'] ?? null)) {
                throw new RuntimeException('Defekte einzelne Referenzzeile.');
            }
            $prefix=$r['kind']==='page'?'p:':'c:';
            $key=(string)($r['kind']==='page'?($r['path']??''):($r['slug']??''));
            $oid=$prefix.$r['owner_id'];
            if ($key==='' || isset($uniqueTargets[$prefix.$key])) {
                throw new RuntimeException('Doppelte/fehlende Referenzziele.');
            }
            $uniqueTargets[$prefix.$key]=true;
            if (isset($all[$prefix.$key])) {
                if ($all[$prefix.$key]['owner']!==$r['owner_id']) {
                    $conflicts[]=$prefix.$key; // no adoption of foreign pages
                } else {
                    ++$mapped;
                }
            } elseif (isset($owners[$oid])) {
                $conflicts[]='owner_moved:'.$oid; // no creation of duplicate owner
            } else {
                ++$missing;
            }
        }
        if ($duplicate) $conflicts=array_merge($conflicts, $duplicate);
        return [
            'status'=>'NUR_LESEN_ALTIMPORT_GESPERRT',
            'website'=>home_url('/'),
            'wp_pages_total'=>count($wpPages),
            'wp_pages_published'=>count(array_filter($wpPages, static fn($p)=>(string)$p->post_status==='publish')),
            'wp_pages_drafts'=>count(array_filter($wpPages, static fn($p)=>(string)$p->post_status==='draft')),
            'wp_posts_total'=>count($wpPosts),
            'wp_categories_total'=>count($wpTerms),
            'w6_owners_total'=>218,
            'w6_already_owned'=>$mapped,
            'w6_missing'=>$missing,
            'w6_conflicts'=>count($conflicts),
            'w6_conflict_examples'=>array_slice(array_unique($conflicts),0,10),
            'w6_nine_root_import_enabled'=>false,
            'safe_to_write'=>false
        ];
    }
    public static function screen(): void {
        if (!self::allowed()) wp_die('Administratorrechte bzw. Website nicht korrekt.');
        echo '<div class="wrap"><h1>Wassertechnik – eine schreibfreie Gesamtbestandsaufnahme</h1>';
        try {
            $report=self::inspect();
            echo '<p>WordPress-Seiten: '.(int)$report['wp_pages_total']
                .' (veröffentlicht: '.(int)$report['wp_pages_published']
                .', Entwürfe: '.(int)$report['wp_pages_drafts']
                .'); Beiträge: '.(int)$report['wp_posts_total']
                .'; Kategorien: '.(int)$report['wp_categories_total'].'.</p>';
            echo '<p>218 bisherige W6-Owner: '.(int)$report['w6_already_owned']
                .' zugeordnet, '.(int)$report['w6_missing'].' fehlen, '
                .(int)$report['w6_conflicts'].' Konflikte.</p>';
            echo '<p><strong>Keine Übernahme:</strong> Die alte Neuner-Hierarchie ist gesperrt; das aktuelle Fachkonzept hat sieben Bereiche. Dieser Vorgang hat ausschließlich gelesen.</p>';
        } catch (Throwable $e) {
            echo '<p><strong>GESPERRT:</strong> '.esc_html($e->getMessage()).'</p>';
        }
        echo '</div>';
    }
}
