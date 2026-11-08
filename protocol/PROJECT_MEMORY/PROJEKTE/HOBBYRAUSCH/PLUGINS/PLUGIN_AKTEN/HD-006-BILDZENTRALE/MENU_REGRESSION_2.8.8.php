<?php
/** HD006 menu-path anti-regression, WordPress menu simulated against REAL plugin class. */
define('ABSPATH','/tmp/wordpress/');
$GLOBALS['actions']=[];$GLOBALS['filters']=[];$GLOBALS['menu']=[];
function add_action($h,$cb,$priority=10,$args=1){$GLOBALS['actions'][]=[$h,$priority,$cb];}
function add_filter($h,$cb,$priority=10,$args=1){$GLOBALS['filters'][]=[$h,$priority,$cb];}
function get_option($k,$d=false){if($k==='hdbz_prompt_rules_version')return 'hobby-depot-1.1';if($k==='hdbz_general_schema_version')return '4';return $d;}
function wp_strip_all_tags($s){return strip_tags($s);}
function add_menu_page($title,$label,$cap,$slug,$callback,$icon='',$position=null){
    $GLOBALS['menu'][]=[$label,$cap,$slug,$title,$callback,$position];return 'toplevel_page_'.$slug;
}
function ok($pass,$name){static $n=0;$n++;echo ($pass?'PASS':'FAIL')." [$n] ".$name."\n";if(!$pass)exit(1);}
require $argv[1];
ok(class_exists('HDBZ_Plugin'),'Real plugin class loaded');
ok(count(array_filter($GLOBALS['actions'],fn($a)=>$a[0]==='admin_menu'))===2,'Own and late admin-menu hooks');
$mapping=function(){echo 'mapping';};
function verify_pair($mapping,$tag){
    $menu=$GLOBALS['menu'];ok(count($menu)===2,$tag.' both menus');
    $by=[];foreach($menu as $item){$by[$item[2]]=$item;}
    ok(count($by)===2,$tag.' distinct slugs');
    ok(isset($by['hdbz-bilder-erstellen']),$tag.' creation URL');
    ok(isset($by['hobby-depot-bildzentrale']),$tag.' mapping URL');
    ok($by['hdbz-bilder-erstellen'][0]==='Bilder erstellen',$tag.' creation label');
    ok($by['hobby-depot-bildzentrale'][0]==='Bilder zuordnen',$tag.' mapping label');
    ok($by['hdbz-bilder-erstellen'][4]===[HDBZ_Plugin::class,'render_page'],$tag.' creation callback');
    ok($by['hobby-depot-bildzentrale'][4]===$mapping,$tag.' original mapping callback');
}
$GLOBALS['menu']=[];
add_menu_page('Mapping','Bildzentrale','manage_options','hobby-depot-bildzentrale',$mapping);
HDBZ_Plugin::admin_menu();HDBZ_Plugin::clarify_legacy_assignment_menu();
verify_pair($mapping,'mapping-first');
$GLOBALS['menu']=[];
HDBZ_Plugin::admin_menu();
add_menu_page('Mapping','Bildzentrale','manage_options','hobby-depot-bildzentrale',$mapping);
HDBZ_Plugin::clarify_legacy_assignment_menu();
verify_pair($mapping,'creator-first');
HDBZ_Plugin::clarify_legacy_assignment_menu();
ok($GLOBALS['menu'][1][0]==='Bilder zuordnen','Idempotent');
$GLOBALS['menu']=[];HDBZ_Plugin::admin_menu();HDBZ_Plugin::clarify_legacy_assignment_menu();
ok(count($GLOBALS['menu'])===1 && $GLOBALS['menu'][0][0]==='Bilder erstellen','Mapping absent');
$GLOBALS['menu']=[];HDBZ_Plugin::admin_menu();add_menu_page('Other','Bildzentrale','manage_options','third-party',$mapping);
HDBZ_Plugin::clarify_legacy_assignment_menu();
ok($GLOBALS['menu'][1][0]==='Bildzentrale','Other menu untouched');
$GLOBALS['menu']=[];HDBZ_Plugin::admin_menu();add_menu_page('Mapping','Bildverwaltung – fertig','manage_options','hobby-depot-bildzentrale',$mapping);
HDBZ_Plugin::clarify_legacy_assignment_menu();
ok($GLOBALS['menu'][1][0]==='Bildverwaltung – fertig','Existing distinct label unchanged');
$main=file_get_contents($argv[1]);
ok(!str_contains($main,'page=hobby-depot-bildzentrale'),'Old creation redirects eliminated');
ok(str_contains($main,"self::ADMIN_MENU_SLUG, 'hdbz_tab'"),'Tabs go to creation');
ok(str_contains($main,"rest_url('hobby-depot-bildzentrale/v1/magnific-webhook')"),'Webhook URL unchanged');
ok(str_contains($main,"register_rest_route('hobby-depot-bildzentrale/v1'"),'REST route unchanged');
ok(substr_count($main,'hobby-depot-bildzentrale/v1')===3,'All 3 REST/Webhook occurrences unchanged');
echo "ALL 27 TESTS PASS\n";
