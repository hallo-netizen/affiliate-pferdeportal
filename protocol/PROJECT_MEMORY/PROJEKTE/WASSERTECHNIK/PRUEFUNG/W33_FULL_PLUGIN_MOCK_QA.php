<?php
declare(strict_types=1);
/* Offline WordPress mock, no I/O to live WordPress, no network. */
$root=$argv[1]??'';
if (!$root || !is_file($root.'/wassertechnik-kategorie-workflow.php')) exit(2);
define('ABSPATH','/');
define('OBJECT','OBJECT');
$GLOBALS['actions']=[];$GLOBALS['shortcodes']=[];$GLOBALS['writes']=0;$GLOBALS['http']=0;
$GLOBALS['site']='wasser.oliver-beil.de';$GLOBALS['admin']=true;$GLOBALS['pages']=[];$GLOBALS['owners']=[];
$GLOBALS['wp_snapshot_pages']=[
    (object)['ID'=>2,'post_name'=>'beispielseite','post_status'=>'publish'],
    (object)['ID'=>3,'post_name'=>'datenschutzerklaerung','post_status'=>'draft']
];
$GLOBALS['wp_snapshot_posts']=[(object)['ID'=>1,'post_name'=>'hallo-welt','post_status'=>'publish']];
$GLOBALS['wp_snapshot_categories']=[(object)['term_id'=>1,'slug'=>'allgemein']];
function add_action($h,$cb,$priority=10){$GLOBALS['actions'][$h][]=$cb;}
function add_shortcode($n,$cb){$GLOBALS['shortcodes'][$n]=$cb;}
function add_menu_page(...$args){}
function add_submenu_page(...$args){}
function home_url($path='/'){return 'https://'.$GLOBALS['site'].$path;}
function wp_parse_url($url,$component){return parse_url($url,$component);}
function current_user_can($right){return $GLOBALS['admin'];}
function wp_die($s){throw new RuntimeException('WP_DIE: '.$s);}
function get_page_by_path($path,$output,$posttype){return $GLOBALS['pages'][$path]??null;}
function get_post_meta($id,$key,$single){return $GLOBALS['owners'][$id]??'';}
function get_permalink($id){return 'https://wasser.oliver-beil.de/page/'.$id.'/';}
function esc_html($s){return htmlspecialchars((string)$s,ENT_QUOTES,'UTF-8');}
function esc_url($s){return htmlspecialchars((string)$s,ENT_QUOTES,'UTF-8');}
function wp_json_encode($v,$opts=0){return json_encode($v,$opts);}
function update_option(...$x){$GLOBALS['writes']++;throw new RuntimeException('WordPress option write');}
function wp_insert_post(...$x){$GLOBALS['writes']++;throw new RuntimeException('WordPress page write');}
function wp_insert_term(...$x){$GLOBALS['writes']++;throw new RuntimeException('WordPress category write');}
function wp_remote_post(...$x){$GLOBALS['http']++;throw new RuntimeException('Paid SEO network request');}
function plugin_dir_path($file){return dirname($file).DIRECTORY_SEPARATOR;}
function get_posts(...$x){$opts=$x[0]??[];return ($opts['post_type']??'')==='page'?$GLOBALS['wp_snapshot_pages']:$GLOBALS['wp_snapshot_posts'];}
function get_terms(...$x){return $GLOBALS['wp_snapshot_categories'];}
function get_page_uri($p){return $p->post_name;}
function get_term_meta($id,$key,$single){return '';}
function is_wp_error($x){return false;}
function get_transient(...$x){return false;}
function get_option(...$x){return false;}
function wp_is_post_revision(...$x){return false;}
$assert=function($ok,$msg){if(!$ok)throw new RuntimeException("FAILED: ".$msg);echo "PASS ".$msg.PHP_EOL;};
require $root.'/wassertechnik-kategorie-workflow.php';
$assert(Wassertechnik_Kategorie_Workflow::VERSION==='0.1.8','same plugin identity, updated version');
$homepage=file_get_contents($root.'/wassertechnik-kategorie-workflow.php');
$assert(str_contains($homepage,'Fachplan W27:') && !str_contains($homepage,'Aktueller Fachplan W4:'),'one current 7-area homepage, no old 8-area claim');
$readme=file_get_contents($root.'/README.txt');
$assert(str_contains($readme,'NICHT INSTALLIEREN') && str_contains($readme,'0.1.8'),'README status and version match real source');
$assert(class_exists('Wassertechnik_Kategorie_Importer'),'old importer source retained');
$assert(!isset($GLOBALS['actions']['admin_post_wassertechnik_import_apply']),
        'old 9-root importer DISABLED by default');
$assert(count($GLOBALS['shortcodes'])===1,'one read-only shortcode');
$assert(class_exists('Wassertechnik_W34_Inventory_Readback'),'one internal WP read-only inventory component');
$inventory=Wassertechnik_W34_Inventory_Readback::inspect();
$assert($inventory['wp_pages_total']===2 && $inventory['wp_pages_published']===1 &&
        $inventory['wp_pages_drafts']===1 && $inventory['wp_posts_total']===1 &&
        $inventory['wp_categories_total']===1,'original WP snapshot 2 pages/1 post/1 category');
$assert($inventory['w6_owners_total']===218 &&
        $inventory['w6_already_owned']===0 && $inventory['w6_missing']===218 &&
        $inventory['w6_conflicts']===0,'single preflight against existing original 218 W6 references');
$assert($inventory['safe_to_write']===false &&
        $inventory['w6_nine_root_import_enabled']===false,'one inventory cannot activate old 9-root import');
$GLOBALS['wp_snapshot_pages'][0]->post_name='wasseraufbereitung';
$conflict=Wassertechnik_W34_Inventory_Readback::inspect();
$assert($conflict['w6_conflicts']===1 && !$conflict['safe_to_write'],'foreign page collision blocked in same inventory');
$GLOBALS['wp_snapshot_pages'][0]->post_name='beispielseite';
$GLOBALS['site']='other-host.example';
try{Wassertechnik_W34_Inventory_Readback::inspect();throw new RuntimeException('Foreign site accepted');}
catch(RuntimeException $e){$assert($e->getMessage()!=='Foreign site accepted','WP inventory blocks foreign host');}
$GLOBALS['site']='wasser.oliver-beil.de';
$GLOBALS['admin']=false;
try{Wassertechnik_W34_Inventory_Readback::inspect();throw new RuntimeException('Visitor accepted');}
catch(RuntimeException $e){$assert($e->getMessage()!=='Visitor accepted','WP inventory blocks non-admin');}
$GLOBALS['admin']=true;
ob_start();Wassertechnik_W34_Inventory_Readback::screen();$inventoryHtml=ob_get_clean();
$assert(str_contains($inventoryHtml,'218') && str_contains($inventoryHtml,'veröffentlicht'),'one admin readback display');
$old=Wassertechnik_DataForSEO::build_preflight();
[$origin,$keywords,$owners]=Wassertechnik_PaidResearch::planned();
$assert(count($keywords)===218,'old 218 SEO keywords intact');
$assert(($old['unique_keywords']??null)===218,'old preflight exactly 218');
$assert(($old['fingerprint']??null)==='9570a11250f6d3684f52af69239a9af2090a292ba1646dafde76380c471b3462',
        'old SEO fingerprint unchanged');
$h=Wassertechnik_W30_Seo_Handoff::read($root.'/assets/wassertechnik-w28-seo-handoff.json');
$assert($h['anzahl']===81 && $h['rubriken']===90,'real W28: 81 new, 90 rubrics');
$assert(count(array_unique(array_column($h['produkte'],'register_id')))==81,'81 distinct canonical IDs');
$assert(count(array_filter($h['produkte'],fn($x)=>($x['wp_seitenfreigabe']??null)!==false))===0,'no new WordPress page approvals');
ob_start();Wassertechnik_Seo81_Preview::screen();$html=ob_get_clean();
$assert(substr_count($html,'<tr>')===82,'81 rows in original WP admin preview');
$GLOBALS['site']='another.site';
try{Wassertechnik_Seo81_Preview::payload();throw new RuntimeException('wrong host accepted');}
catch(RuntimeException $e){$assert($e->getMessage()!=='wrong host accepted','wrong WP host blocked');}
$GLOBALS['site']='wasser.oliver-beil.de';
$GLOBALS['admin']=false;
try{Wassertechnik_Seo81_Preview::screen();throw new RuntimeException('non-admin accepted');}
catch(RuntimeException $e){$assert($e->getMessage()!=='non-admin accepted','non-admin blocked');}
$GLOBALS['admin']=true;
$nav=Wassertechnik_W32_Navigation::plan();
$assert(count($nav['hauptbereiche'])===7 && count($nav['existing_w4_pages'])===79,'W27 seven current areas and 79 old owners');
$assert(array_sum(array_column($nav['hauptbereiche'],'existing_menu'))===71,'71 old consumer owner links');
$assert(array_sum(array_column($nav['hauptbereiche'],'new_not_approved'))===81,'81 pending research candidates in navigation data');
$assert(count(array_filter($nav['existing_w4_pages'],fn($x)=>!$x['menu']))===8,'8 industry owners excluded from buyer navigation');
$idx=1;
foreach($nav['existing_w4_pages'] as $p){
    $GLOBALS['pages'][$p['wordpress_path']]=(object)['ID'=>$idx,'post_status'=>'publish'];
    $GLOBALS['owners'][$idx]=$p['owner_id'];++$idx;
}
$menu=Wassertechnik_W32_Navigation::render();
$assert(substr_count($menu,'<li>')===71,'71 real owner-matching published links');
$assert(!str_contains($menu,'<h3>Pool & Teichtechnik</h3>'),'no fake empty Pool landing');
$first=$nav['existing_w4_pages'][0];
$GLOBALS['pages'][$first['wordpress_path']]->post_status='draft';
$assert(substr_count(Wassertechnik_W32_Navigation::render(),'<li>')===70,'draft page never linked');
$GLOBALS['pages'][$first['wordpress_path']]->post_status='publish';
$GLOBALS['owners'][1]='NOT_THE_OWNER';
$assert(substr_count(Wassertechnik_W32_Navigation::render(),'<li>')===70,'wrong owner never linked');
$GLOBALS['owners'][1]=$first['owner_id'];
$manifest=json_decode(file_get_contents($root.'/assets/wassertechnik-wp-import-plan.json'),true,512,JSON_THROW_ON_ERROR);
$assert($manifest['schema']==='wassertechnik-w6-import-v1','old W6 manifest labeled as legacy');
$assert(count($manifest['entries'])===218,'113 old pages + 105 categories remain in legacy manifest');
$assert(count(array_filter($manifest['entries'],fn($x)=>$x['kind']==='page'))===113,'113 legacy pages preserved');
$assert(count(array_filter($manifest['entries'],fn($x)=>$x['kind']==='category'))===105,'105 legacy content categories preserved');
$assert($GLOBALS['writes']===0 && $GLOBALS['http']===0,'no WordPress mutations / no paid DataForSEO calls');
echo "PASS W33 FULL OFFLINE REGRESSION: existing SEO, new SEO read, navigation, legacy manifest locked".PHP_EOL;
