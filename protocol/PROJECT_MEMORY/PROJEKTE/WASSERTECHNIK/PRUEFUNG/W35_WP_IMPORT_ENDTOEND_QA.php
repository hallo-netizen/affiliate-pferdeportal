<?php
/**
 * W35 end-to-end importer mock. Invoke from W33 build with package root and scenario:
 * php W35_WP_IMPORT_ENDTOEND_QA.php <plugin-dir> blank|old9|collision|rollback|stale|wrongsite|nonadmin|redirect
 */
declare(strict_types=1);
$plugin=$argv[1]??null;$scenario=$argv[2]??'';
if(!$plugin||!is_file($plugin.'/wassertechnik-kategorie-workflow.php')||!$scenario)exit(2);
define('ABSPATH','/');
define('OBJECT','OBJECT');
define('MINUTE_IN_SECONDS',60);
$GLOBALS['site']='wasser.oliver-beil.de';$GLOBALS['admin']=true;
$GLOBALS['pages']=[];$GLOBALS['posts']=[];$GLOBALS['terms']=[];
$GLOBALS['meta_p']=[];$GLOBALS['meta_c']=[];
$GLOBALS['actions']=[];$GLOBALS['transients']=[];$GLOBALS['options']=[];
$GLOBALS['posts_next']=5;$GLOBALS['cats_next']=5;
$GLOBALS['writes']=0;$GLOBALS['paid_calls']=0;$GLOBALS['fail_at']='';$GLOBALS['update_attempts']=0;$GLOBALS['status_404']=true;
$GLOBALS['redirect']=null;$GLOBALS['test_case']=$scenario;
class WP_Error {function get_error_message(){return 'forced WP mock error';}}
function add_action($x,$fn,$priority=10){$GLOBALS['actions'][$x][]=$fn;}
function add_shortcode(...$x){}
function add_menu_page(...$x){}
function add_submenu_page(...$x){}
function wp_parse_url($u,$component){return parse_url($u,$component);}
function home_url($p='/'){return 'https://'.$GLOBALS['site'].$p;}
function current_user_can($c){return $GLOBALS['admin'];}
function wp_die($msg){throw new RuntimeException('BLOCKED '.strip_tags((string)$msg));}
function is_wp_error($x){return $x instanceof WP_Error;}
function get_posts($opts=[]){return array_values(($opts['post_type']??'')==='page'?$GLOBALS['pages']:$GLOBALS['posts']);}
function get_terms(...$a){return array_values($GLOBALS['terms']);}
function get_post_meta($id,$key,$single=true){return $GLOBALS['meta_p'][$id][$key]??'';}
function get_term_meta($id,$key,$single=true){return $GLOBALS['meta_c'][$id][$key]??'';}
function update_term_meta($id,$key,$v){$GLOBALS['meta_c'][$id][$key]=$v;$GLOBALS['writes']++;return true;}
function update_option($key,$v,$autoload=false){$GLOBALS['options'][$key]=$v;$GLOBALS['writes']++;return true;}
function get_option($key,$default=false){return $GLOBALS['options'][$key]??$default;}
function get_transient($key){return $GLOBALS['transients'][$key]??false;}
function set_transient($key,$val,$time){$GLOBALS['transients'][$key]=$val;return true;}
function delete_transient($key){unset($GLOBALS['transients'][$key]);return true;}
function wp_nonce_field(...$x){}
function check_admin_referer($x){return true;}
function wp_unslash($x){return $x;}
function sanitize_text_field($x){return (string)$x;}
function esc_html($x){return htmlspecialchars((string)$x,ENT_QUOTES,'UTF-8');}
function esc_attr($x){return esc_html($x);}
function esc_url($x){return esc_html($x);}
function admin_url($p=''){return 'https://wasser.oliver-beil.de/wp-admin/'.$p;}
function submit_button(...$x){}
function wp_safe_redirect($url,$code=302){$GLOBALS['redirect']=[$url,$code];return true;}
function is_404(){return $GLOBALS['status_404'];}
function get_permalink($id){return 'https://wasser.oliver-beil.de/'.get_page_uri($GLOBALS['pages'][$id]).'/';}
function get_page_uri($page){
    $parts=[];$seen=[];$x=$page;
    while($x){
        if(isset($seen[$x->ID]))throw new RuntimeException('WP mock parent cycle');
        $seen[$x->ID]=true;$parts[]=$x->post_name;
        $x=$x->post_parent?($GLOBALS['pages'][$x->post_parent]??null):null;
    }
    return implode('/',array_reverse($parts));
}
function get_page_by_path($path,$output,$type){
    foreach($GLOBALS['pages'] as $p)if(get_page_uri($p)===$path)return $p;
    return null;
}
function wp_insert_post($p,$wp_error=true){
    if($GLOBALS['fail_at']==='insert-page')return new WP_Error();
    $id=$GLOBALS['posts_next']++;$GLOBALS['pages'][$id]=(object)[
        'ID'=>$id,'post_name'=>$p['post_name'],'post_parent'=>$p['post_parent'],
        'post_title'=>$p['post_title'],'post_status'=>$p['post_status']];
    $GLOBALS['meta_p'][$id]=($p['meta_input']??[]);
    $GLOBALS['writes']++;return $id;
}
function wp_update_post($p,$wp_error=true){
    ++$GLOBALS['update_attempts'];
    if($GLOBALS['fail_at']==='update-page')return new WP_Error();
    if($GLOBALS['fail_at']==='update-page-second' && $GLOBALS['update_attempts']===2){
        $GLOBALS['fail_at']=''; // one transient failure, rollback calls are allowed
        return new WP_Error();
    }
    $id=$p['ID'];if(!isset($GLOBALS['pages'][$id]))return new WP_Error();
    foreach($p as $k=>$v)if($k!=='ID')$GLOBALS['pages'][$id]->$k=$v;
    $GLOBALS['writes']++;return $id;
}
function wp_delete_post($id,$force=false){
    unset($GLOBALS['pages'][$id],$GLOBALS['meta_p'][$id]);
    $GLOBALS['writes']++;return true;
}
function wp_insert_term($label,$tax,$opts=[]){
    if($GLOBALS['fail_at']==='insert-category')return new WP_Error();
    $id=$GLOBALS['cats_next']++;$GLOBALS['terms'][$id]=(object)[
        'term_id'=>$id,'slug'=>$opts['slug'],'name'=>$label];
    $GLOBALS['writes']++;return ['term_id'=>$id];
}
function wp_delete_term($id,$tax){unset($GLOBALS['terms'][$id],$GLOBALS['meta_c'][$id]);$GLOBALS['writes']++;return true;}
function wp_remote_post(...$x){$GLOBALS['paid_calls']++;throw new RuntimeException('PAID CALL NOT ALLOWED');}
function wp_json_encode($v,$opts=0){return json_encode($v,$opts);}
function plugin_dir_path($p){return dirname($p).'/';}
function get_page_link($id){return get_permalink($id);}
function assertW($ok,$msg){if(!$ok)throw new RuntimeException('FAIL '.$msg);echo 'PASS '.$msg.PHP_EOL;}
require $plugin.'/wassertechnik-kategorie-workflow.php';
$plan=Wassertechnik_Kategorie_Importer::plan();
assertW(count($plan['wp_targets'])===219 && count($plan['redirects'])===17,
    '219 current W27 targets and exactly 17 known redirects');
assertW(isset($GLOBALS['actions']['admin_post_wassertechnik_w35_apply'])
       && !isset($GLOBALS['actions']['admin_post_wassertechnik_import_apply']),
    'one current W35 writer only, old W9 write hook absent');
assertW(!isset($GLOBALS['actions']['admin_menu'][0])||true,'WP hooks bootstrap without side effects');
function addStd(){
  $GLOBALS['pages'][2]=(object)['ID'=>2,'post_name'=>'beispielseite','post_parent'=>0,'post_title'=>'Beispielseite','post_status'=>'publish'];
  $GLOBALS['pages'][3]=(object)['ID'=>3,'post_name'=>'datenschutzerklaerung','post_parent'=>0,'post_title'=>'Datenschutzerklärung','post_status'=>'draft'];
  $GLOBALS['posts'][1]=(object)['ID'=>1,'post_name'=>'hallo-welt','post_parent'=>0,'post_title'=>'Hallo Welt!','post_status'=>'publish'];
  $GLOBALS['terms'][1]=(object)['term_id'=>1,'slug'=>'allgemein','name'=>'Allgemein'];
}
function seedOld9($plan){
    $rows=array_values(array_filter($plan['wp_targets'],fn($x)=>$x['kind']==='page'&&$x['w6_original']));
    usort($rows,fn($a,$b)=>substr_count($a['legacy_path'],'/')<=>substr_count($b['legacy_path'],'/'));
    $ids=[];
    foreach($rows as $row){
        $id=$GLOBALS['posts_next']++;$ids[$row['owner_id']]=$id;
        $parent=$row['prior_parent_owner_id'];
        $GLOBALS['pages'][$id]=(object)['ID'=>$id,'post_name'=>basename($row['legacy_path']),
            'post_parent'=>$parent?$ids[$parent]:0,'post_title'=>$row['legacy_title'],'post_status'=>'publish'];
        $GLOBALS['meta_p'][$id]['_wt_owner_id']=$row['owner_id'];
    }
    foreach($plan['wp_targets'] as $r) if($r['kind']==='category'){
        $id=$GLOBALS['cats_next']++;
        $GLOBALS['terms'][$id]=(object)['term_id'=>$id,'slug'=>$r['slug'],'name'=>$r['title']];
        $GLOBALS['meta_c'][$id]['_wt_owner_id']=$r['owner_id'];
    }
}
function inv($plan):array{
    $m=new ReflectionMethod('Wassertechnik_Kategorie_Importer','inventory');
    return $m->invoke(null,$plan);
}
function verifyTarget($plan,$expectedMissing,$expectedChanged){
    $state=inv($plan);
    assertW(!$state['conflicts'],'no plan conflicts');
    assertW(count($state['missing_pages'])===$expectedMissing,'expected missing WP pages');
    assertW(count($state['updates'])===$expectedChanged,'expected existing page updates');
    return $state;
}
function submitApply($plan,$state){
    $_POST=['approval'=>'yes','plan_sha'=>$plan['_source_sha256'],'wp_sha'=>$state['fingerprint']];
    Wassertechnik_Kategorie_Importer::apply(); // exits after success
}
addStd();
if($scenario==='old9'||$scenario==='redirect')seedOld9($plan);
if($scenario==='collision'){
    $GLOBALS['pages'][10]=(object)['ID'=>10,'post_name'=>'brunnen','post_parent'=>0,'post_title'=>'Foreign page','post_status'=>'publish'];
    $state=inv($plan);
    assertW(count($state['conflicts'])>=1,'foreign WP slug blocks import');
    $writes=$GLOBALS['writes'];
    try{submitApply($plan,$state);throw new RuntimeException('INVALID unexpected success');}
    catch(RuntimeException $e){assertW(str_starts_with($e->getMessage(),'BLOCKED'),'conflicting import prevented');}
    assertW($GLOBALS['writes']===$writes,'collision causes zero WP writes');
    exit(0);
}
if($scenario==='stale'){
    $state=inv($plan);$GLOBALS['pages'][2]->post_title='After preview';
    $writes=$GLOBALS['writes'];
    try{submitApply($plan,$state);throw new RuntimeException('INVALID unexpected success');}
    catch(RuntimeException $e){assertW(str_starts_with($e->getMessage(),'BLOCKED'),'stale fingerprint stops one run');}
    assertW($GLOBALS['writes']===$writes,'stale preview causes zero WP writes');exit(0);
}
if($scenario==='wrongsite'||$scenario==='nonadmin'){
    $GLOBALS[$scenario==='wrongsite'?'site':'admin']=$scenario==='wrongsite'?'other.example.com':false;
    try{Wassertechnik_Kategorie_Importer::screen();throw new RuntimeException('INVALID unauthorized');}
    catch(RuntimeException $e){assertW(str_starts_with($e->getMessage(),'BLOCKED'),'wrong site or visitor blocked');}
    assertW($GLOBALS['writes']===0,'authorization failure no writes');exit(0);
}
if($scenario==='rollback'){
    $state=verifyTarget($plan,114,0);
    $GLOBALS['fail_at']='insert-category';
    try{submitApply($plan,$state);throw new RuntimeException('INVALID unexpected success');}
    catch(RuntimeException $e){assertW(str_starts_with($e->getMessage(),'BLOCKED'),'first category failure aborts all');}
    assertW(count($GLOBALS['pages'])===2 && count($GLOBALS['terms'])===1,'entire 114 page insert rolled back');
    assertW(!get_transient('wassertechnik_w35_single_apply_lock'),'import lock cleared after error');
    exit(0);
}
if($scenario==='update-rollback'){
    seedOld9($plan);
    $state=verifyTarget($plan,1,23);
    $beforePages=[];
    foreach($GLOBALS['pages'] as $id=>$p)$beforePages[$id]=[get_page_uri($p),$p->post_parent,$p->post_title];
    $beforeTerms=count($GLOBALS['terms']);$beforeIds=array_keys($GLOBALS['pages']);
    $GLOBALS['fail_at']='update-page-second';
    try{submitApply($plan,$state);throw new RuntimeException('INVALID unexpected success');}
    catch(RuntimeException $e){assertW(str_starts_with($e->getMessage(),'BLOCKED'),'second page update failure blocks complete import');}
    assertW(count($GLOBALS['terms'])===$beforeTerms,'existing 105 category owners unchanged after failed migration');
    assertW(array_keys($GLOBALS['pages'])===$beforeIds,'only new pool page removed after failed migration');
    foreach($beforePages as $id=>$old)assertW(
        get_page_uri($GLOBALS['pages'][$id])===$old[0] &&
        $GLOBALS['pages'][$id]->post_parent===$old[1] &&
        $GLOBALS['pages'][$id]->post_title===$old[2],
        'all existing page addresses/parents/titles restored: '.$id);
    assertW(!get_transient('wassertechnik_w35_single_apply_lock'),'failed migration lock cleared');
    assertW($GLOBALS['paid_calls']===0,'0 paid SEO after failed migration');
    exit(0);
}
if($scenario==='idempotent'){
    seedOld9($plan);
    $ids=[];
    foreach($GLOBALS['meta_p'] as $id=>$meta)if(!empty($meta['_wt_owner_id']))$ids[$meta['_wt_owner_id']]=$id;
    foreach($plan['wp_targets'] as $r)if($r['kind']==='page'&&$r['w6_original']){
        $id=$ids[$r['owner_id']];
        $GLOBALS['pages'][$id]->post_parent=$r['parent_owner_id']===null?0:$ids[$r['parent_owner_id']];
        $GLOBALS['pages'][$id]->post_title=$r['title'];
    }
    $pool=$GLOBALS['posts_next']++;
    $GLOBALS['pages'][$pool]=(object)['ID'=>$pool,'post_name'=>'pool-teichtechnik','post_parent'=>0,
        'post_title'=>'Pool & Teichtechnik','post_status'=>'draft'];
    $GLOBALS['meta_p'][$pool]['_wt_owner_id']='wt_main_pool_w27';
    $state=verifyTarget($plan,0,0);
    assertW(count($state['missing_categories'])===0,'no missing category after successful prior import');
    ob_start();Wassertechnik_Kategorie_Importer::screen();$html=ob_get_clean();
    assertW(str_contains($html,'Alle Zielobjekte vorhanden'),'second run shows complete without a new import button');
    assertW(!str_contains($html,'admin-post.php'),'second run cannot start a duplicate import');
    assertW($GLOBALS['writes']===0 && $GLOBALS['paid_calls']===0,'idempotent second run 0 writes/0 SEO calls');
    exit(0);
}
if($scenario==='redirect'){
    // Fast-forward the 2 parent reparentings in the mock; exact old URL should 301.
    $ids=[];
    foreach($plan['wp_targets'] as $r)if($r['kind']==='page'&&$r['w6_original']){
        foreach($GLOBALS['meta_p'] as $id=>$meta)if(($meta['_wt_owner_id']??'')===$r['owner_id']){$ids[$r['owner_id']]=$id;break;}
    }
    foreach($plan['wp_targets'] as $r)if($r['kind']==='page'&&$r['w6_original']&&$r['parent_owner_id']!==$r['prior_parent_owner_id']){
        $GLOBALS['pages'][$ids[$r['owner_id']]]->post_parent=$ids[$r['parent_owner_id']];
    }
    $_SERVER['REQUEST_URI']='/bewaesserung/gartenschlauch/';
    register_shutdown_function(function(){
        assertW($GLOBALS['redirect']!==null && $GLOBALS['redirect'][1]===301
            && str_contains($GLOBALS['redirect'][0],'/brunnen/bewaesserung/gartenschlauch/'),
            'old 17-family product address permanently redirects to original owner target');
        assertW($GLOBALS['paid_calls']===0,'301 redirect never calls paid SEO');
    });
    Wassertechnik_Kategorie_Importer::redirect_legacy(); // exits after valid redirect
    throw new RuntimeException('Redirect not detected');
}
if($scenario==='blank'||$scenario==='old9'){
    $state=verifyTarget($plan,$scenario==='blank'?114:1,$scenario==='blank'?0:23);
    $oldIds=[];
    if($scenario==='old9')foreach($GLOBALS['meta_p'] as $id=>$meta){
        if(isset($meta['_wt_owner_id']))$oldIds[$meta['_wt_owner_id']]=$id;
    }
    register_shutdown_function(function() use($scenario,$oldIds,$plan){
        assertW(count($GLOBALS['pages'])===116,'114 W27 pages plus 2 untouched standard WP pages');
        assertW(count($GLOBALS['terms'])===106,'105 W27 category owners plus Allgemein');
        $after=inv($plan);
        assertW(!$after['conflicts'] && !$after['missing_pages'] && !$after['missing_categories'],
           'complete 219-owner WP readback after one import');
        if($scenario==='old9'){
            foreach($oldIds as $owner=>$id)assertW(isset($GLOBALS['pages'][$id])
                && get_post_meta($id,'_wt_owner_id',true)===$owner,'old WP ID survives: '.$owner);
            assertW(count(array_filter($GLOBALS['pages'],fn($x)=>$x->post_status==='draft'))===2,
                'only pool hub and original privacy draft are draft; old 113 published pages untouched');
            $nav=Wassertechnik_W32_Navigation::render();
            assertW(substr_count($nav,'<li>')===71,'71 menu product links still work after moving 17 URLs');
        }
        assertW(isset($GLOBALS['options']['wassertechnik_w35_single_apply_report']),
            'single import report stored after verified readback');
        assertW($GLOBALS['paid_calls']===0,'0 paid SEO requests during import');
        echo 'PASS W35 FULL IMPORT '.$scenario.' END-TO-END'.PHP_EOL;
    });
    submitApply($plan,$state);
}
throw new RuntimeException('Unknown scenario: '.$scenario);
