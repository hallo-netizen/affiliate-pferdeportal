<?php
declare(strict_types=1);
define('ABSPATH','/');
define('OBJECT','OBJECT');
$GLOBALS['writes']=0;$GLOBALS['page_state']=[];$GLOBALS['admin']=true;
function add_shortcode(...$a){}
function add_action(...$a){}
function add_submenu_page(...$a){}
function current_user_can($s){return $GLOBALS['admin'];}
function wp_die($s){throw new RuntimeException($s);}
function esc_html($s){return htmlspecialchars($s,ENT_QUOTES,'UTF-8');}
function esc_url($s){return htmlspecialchars($s,ENT_QUOTES,'UTF-8');}
function get_page_by_path($path,$object,$type){return $GLOBALS['page_state'][$path]??null;}
function get_post_meta($id,$key,$single){return $GLOBALS['owners'][$id]??'';}
function get_permalink($id){return 'https://wasser.oliver-beil.de/wp/'.$id.'/';}
function wp_update_post(...$a){$GLOBALS['writes']++;throw new RuntimeException('WRITE');}
function wp_insert_post(...$a){$GLOBALS['writes']++;throw new RuntimeException('WRITE');}
function wp_remote_post(...$a){$GLOBALS['writes']++;throw new RuntimeException('API');}
require __DIR__.'/../PLUGINS/QUELLCODE/W32_class-wassertechnik-navigation.php';
$file=__DIR__.'/../PLUGINS/ASSETS/W32_wassertechnik-navigation.json';
$original=file_get_contents($file);
if($original===false)throw new RuntimeException('Real W32 asset missing');
$real=json_decode($original,true,512,JSON_THROW_ON_ERROR);
if(count($real['existing_w4_pages'])!==79||count($real['hauptbereiche'])!==7)throw new RuntimeException('Real source counts failed');
if(array_sum(array_column($real['hauptbereiche'],'existing_menu'))!==71||array_sum(array_column($real['hauptbereiche'],'new_not_approved'))!==81)throw new RuntimeException('Real group counts failed');
$assert=function($condition,$note){if(!$condition)throw new RuntimeException('FAIL '.$note);echo 'PASS '.$note.PHP_EOL;};
foreach($real['existing_w4_pages'] as $i=>$p){
 $id=$i+1;
 $GLOBALS['page_state'][$p['wordpress_path']]=(object)['ID'=>$id,'post_status'=>'publish'];
 $GLOBALS['owners'][$id]=$p['owner_id'];
}
try{
 $assert(count(Wassertechnik_W32_Navigation::plan()['existing_w4_pages'])===79,'79 original owner paths');
 $markup=Wassertechnik_W32_Navigation::render();
 $assert(substr_count($markup,'<li>')===71,'71 unique buyer links');
 $assert(!str_contains($markup,'<h3>Pool & Teichtechnik</h3>'),'no empty pool top navigation');
 $first=$real['existing_w4_pages'][0];
 $GLOBALS['page_state'][$first['wordpress_path']]->post_status='draft';
 $assert(substr_count(Wassertechnik_W32_Navigation::render(),'<li>')===70,'draft link not emitted');
 $GLOBALS['page_state'][$first['wordpress_path']]->post_status='publish';
 $GLOBALS['owners'][1]='OTHER';
 $assert(substr_count(Wassertechnik_W32_Navigation::render(),'<li>')===70,'wrong WordPress owner not linked');
 $GLOBALS['owners'][1]=$first['owner_id'];
 $GLOBALS['admin']=false;
 try{Wassertechnik_W32_Navigation::admin_screen();throw new RuntimeException('admin allowed');}catch(RuntimeException $e){$assert($e->getMessage()==='Administratorrechte erforderlich.','admin-only preview');}
 $GLOBALS['admin']=true;
 ob_start();Wassertechnik_W32_Navigation::admin_screen();$admin=ob_get_clean();
 $assert(str_contains($admin,'81 neue Produkte'),'81 new without approval shown');
 $assert($GLOBALS['writes']===0,'zero WordPress writes and API calls');
 rename($file,$file.'.tmp');
 try{$assert(Wassertechnik_W32_Navigation::render()==='','missing asset fails closed');}
 finally{rename($file.'.tmp',$file);}
 echo 'PASS W32: 79 W4, 71 buyers, 8 industry, 7 planned groups, 81 research items; no write'.PHP_EOL;
}catch(Throwable $e){file_put_contents($file,$original);throw $e;}
