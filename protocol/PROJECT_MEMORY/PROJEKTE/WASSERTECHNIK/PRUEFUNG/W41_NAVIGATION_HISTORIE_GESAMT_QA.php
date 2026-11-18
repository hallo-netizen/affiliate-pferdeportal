<?php
declare(strict_types=1);
define('ABSPATH','/'); define('OBJECT','OBJECT');
$GLOBALS['items']=[]; $GLOBALS['owners']=[]; $GLOBALS['writes']=0;$GLOBALS['reads']=0;$GLOBALS['point_reads']=0;
function add_shortcode(...$args){} function add_action(...$args){} function add_submenu_page(...$args){}
function current_user_can($cap){return true;} function is_admin(){return false;}
function esc_html($s){return htmlspecialchars((string)$s,ENT_QUOTES,'UTF-8');}
function esc_url($s){return htmlspecialchars((string)$s,ENT_QUOTES,'UTF-8');}
function wp_die($s){throw new RuntimeException((string)$s);}
function get_page_by_path($path,$obj,$type){$GLOBALS['point_reads']++;return $GLOBALS['items'][$path]??null;}
function get_posts($opts=[]){
    $GLOBALS['reads']++;$out=[];
    foreach($GLOBALS['items'] as $uri=>$row){
        if(isset($out[(int)$row->ID]))continue;
        $p=clone $row;$p->mock_uri=$uri;
        $out[(int)$row->ID]=$p;
    }
    return array_values($out);
}
function get_page_uri($p){return (string)($p->mock_uri??'');}
function is_wp_error($x){return false;}
function get_post_meta($id,$key,$single){return $GLOBALS['owners'][$id]??'';}
function get_permalink($id){return 'https://wasser.oliver-beil.de/produkt-'.$id.'/';}
function has_shortcode($content,$tag){return str_contains((string)$content,'['.$tag.']');}
function wp_insert_post(...$args){$GLOBALS['writes']++;throw new RuntimeException('Unexpected WP write');}
function wp_remote_post(...$args){$GLOBALS['writes']++;throw new RuntimeException('Unexpected paid API');}
$root=rtrim($argv[1]??'', '/');
if(!is_file($root.'/includes/class-wassertechnik-navigation.php'))throw new RuntimeException('Expected built plugin root');
require $root.'/includes/class-wassertechnik-navigation.php';
$plan=json_decode((string)file_get_contents($root.'/ASSETS/W32_wassertechnik-navigation.json'),true,512,JSON_THROW_ON_ERROR);
$wp=json_decode((string)file_get_contents($root.'/ASSETS/W35_wordpress_importplan_219.json'),true,512,JSON_THROW_ON_ERROR);
$paths=[];foreach($wp['wp_targets'] as $r)if($r['kind']==='page')$paths[$r['owner_id']]=$r['path'];
$n=0;foreach($plan['existing_w4_pages'] as $p){
 $id=++$n; $obj=(object)['ID'=>$id,'post_status'=>'publish'];
 $GLOBALS['items'][$paths[$p['owner_id']]]=$obj;
 $GLOBALS['items'][$p['wordpress_path']]=$obj;
 $GLOBALS['owners'][$id]=$p['owner_id'];
}
function assert_w41($good,$name){
 if(!$good)throw new RuntimeException('W41 FAIL: '.$name);
 echo 'PASS W41 '.$name.PHP_EOL;
}
$beforeReads=$GLOBALS['reads'];
$menu=Wassertechnik_W32_Navigation::render();
assert_w41($GLOBALS['reads']===$beforeReads+1 && $GLOBALS['point_reads']===0,
    'W42 one published-page read for 79 original products, zero per-product lookups');
assert_w41(substr_count($menu,'<summary>')===8,'seven consumer menu roots plus specialist');
assert_w41(substr_count($menu,'<a href=')===79,'all 79 actual original owners linked exactly once');
assert_w41(str_contains($menu,'Pool &amp; Teichtechnik'),'pool root persists without invented product links');
assert_w41(count($plan['hauptbereiche'])===7 && $plan['wp_buy_menu_count']===71
    && $plan['wp_industry_count']===8,'seven purchasers and independent eight specialist products');
$first=$plan['existing_w4_pages'][0];
$GLOBALS['items'][$paths[$first['owner_id']]]->post_status='draft';
assert_w41(substr_count(Wassertechnik_W32_Navigation::render(),'<a href=')===78,'draft product never linked');
$GLOBALS['items'][$paths[$first['owner_id']]]->post_status='publish';
$GLOBALS['owners'][1]='FOREIGN';
assert_w41(substr_count(Wassertechnik_W32_Navigation::render(),'<a href=')===78,'wrong owner never linked');
$GLOBALS['owners'][1]=$first['owner_id'];
$GLOBALS['items']['foreign-other-product']=(object)['ID'=>900,'post_status'=>'publish'];
$GLOBALS['owners'][900]=$first['owner_id'];
assert_w41(substr_count(Wassertechnik_W32_Navigation::render(),'<a href=')===78,
    'W42 duplicate owner never linked even if duplicate page is foreign');
unset($GLOBALS['items']['foreign-other-product'],$GLOBALS['owners'][900]);
$GLOBALS['post']=(object)['post_content'=>'[wassertechnik_fachnavigation]'];
ob_start();Wassertechnik_W32_Navigation::auto_render();$dup=ob_get_clean();
assert_w41($dup==='','page shortcode prevents automatic duplicate');
$GLOBALS['post']=(object)['post_content'=>''];
ob_start();Wassertechnik_W32_Navigation::auto_render();$shown=ob_get_clean();
assert_w41(str_contains($shown,'wassertechnik-fachnavigation'),'frontend receives navigation at body open');
ob_start();Wassertechnik_W32_Navigation::auto_render();$again=ob_get_clean();
assert_w41($again==='','automatic front navigation prints only once');
assert_w41($GLOBALS['writes']===0,'zero WordPress or DataForSEO writes');
echo 'PASS W41 NAVIGATION: 10/10'.PHP_EOL;
