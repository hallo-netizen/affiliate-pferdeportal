<?php
// Standalone WordPress stub test. No live site used; production-like environment.
define('ABSPATH', '/test-wp/');
$GLOBALS['opts']=[];$GLOBALS['hooks']=[];$GLOBALS['menus']=[];
$GLOBALS['site']='https://oliver-beil.de/';
$GLOBALS['environment']='production';
$GLOBALS['is_admin']=true;
$GLOBALS['nonce_valid']=true;
function get_option($key,$default=false){return $GLOBALS['opts'][$key] ?? $default;}
function update_option($key,$value,$autoload=null){$before=$GLOBALS['opts'][$key]??null;$GLOBALS['opts'][$key]=$value;return $before!==$value;}
function home_url($path=''){return $GLOBALS['site'].$path;}
function admin_url($path=''){return 'https://oliver-beil.de/wp-admin/'.$path;}
function get_current_blog_id(){return 1;}
function wp_get_environment_type(){return $GLOBALS['environment'];}
function current_user_can($cap){return $GLOBALS['is_admin'];}
function add_action($hook,$callback,...$args){$GLOBALS['hooks'][$hook][]=$callback;}
function add_filter($hook,$callback,...$args){$GLOBALS['hooks'][$hook][]=$callback;}
function register_activation_hook($file,$callback){$GLOBALS['activate_callback']=$callback;}
function esc_html($v){return htmlspecialchars((string)$v,ENT_QUOTES,'UTF-8');}
function esc_attr($v){return htmlspecialchars((string)$v,ENT_QUOTES,'UTF-8');}
function esc_url($v){return htmlspecialchars((string)$v,ENT_QUOTES,'UTF-8');}
function wp_json_encode($v,...$args){return json_encode($v,...$args);}
function wp_nonce_field($action){echo '<input type="hidden" name="_wpnonce" value="testnonce">';}
function check_admin_referer($action){if(!$GLOBALS['nonce_valid'])throw new RuntimeException('BAD_NONCE');return true;}
function submit_button($title,$type='primary',$name='submit',$wrap=true){echo '<button type="submit">'.esc_html($title).'</button>';}
function wp_die($message){throw new RuntimeException('WP_DIE:'.(string)$message);}
function add_query_arg($a,$v=null,$url=''){
 if(is_array($a)){return ($v??'').'?'.http_build_query($a);}
 return ($url??'').'?'.urlencode((string)$a).'='.urlencode((string)$v);
}
function wp_safe_redirect($url){throw new RuntimeException('REDIRECT_OK:'.$url);}
function add_menu_page($title,$menu,$cap,$slug,$callback,$icon,$pos){$GLOBALS['menus'][]=['main',$menu,$slug];}
function add_submenu_page($parent,$title,$menu,$cap,$slug,$callback){$GLOBALS['menus'][]=['sub',$menu,$slug];}
function get_categories($args){return [(object)['slug'=>'pferdedecken','name'=>'Pferdedecken','count'=>0]];}
function get_term_by($key,$val,$taxonomy){return (object)['term_id'=>2,'slug'=>$val,'name'=>'Pferdedecken'];}
class wpdb_stub{
 function prepare($sql,...$args){return $sql.'|'.implode('|',$args);}
 function get_var($sql){return (str_contains($sql,'GET_LOCK')?'1':'1');}
}
$GLOBALS['wpdb']=new wpdb_stub;
function affirm($cond,$msg){if(!$cond)throw new RuntimeException('TEST_FAIL:'.$msg);echo "PASS: $msg\n";}
function fails($callable,$needle){try{$callable();}catch(Throwable $e){affirm(str_contains($e->getMessage(),$needle),'rejects '.$needle);return;}throw new RuntimeException('TEST_FAIL: expected '.$needle);}
require __DIR__.'/texterstellung/texterstellung.php';
$act=$GLOBALS['activate_callback'];
$act();affirm(true,'activation works with WP_ENVIRONMENT_TYPE=production and no wp-config edit');
TXE_Workshop::init();
affirm(isset($GLOBALS['hooks']['admin_post_txe_testmode_confirm']),'admin confirmation handler exists');
affirm(isset($GLOBALS['hooks']['admin_post_txe_diagnose_download']),'diagnostics registration preserved');
TXE_Workshop::menu();
affirm(count($GLOBALS['menus'])===9,'one main menu + eight submenus');
affirm($GLOBALS['menus'][0][1]==='Texterstellung','menu title Texterstellung');
affirm(!TXE_Workshop::permitted(),'unconfirmed site is locked');
$GLOBALS['environment']='staging';affirm(!TXE_Workshop::permitted(),'even WP staging requires explicit confirmation');$GLOBALS['environment']='production';
ob_start();TXE_Workshop::page();$html=ob_get_clean();
affirm(str_contains($html,'Testmodus für diese Website freischalten'),'admin onboarding button visible');
affirm(str_contains($html,'oliver-beil.de'),'site shown to administrator');
affirm(!str_contains($html,'Keyword-Recherche (DataForSEO)'),'workstation locked until confirmation');
fails(fn()=>TXE_Workshop::quick(['target_keyword'=>'test','title'=>'T','category'=>'pferdedecken','article_type'=>'Beratung']),'TESTENVIRONMENT_REQUIRED');
affirm(get_option(TXE_Workshop::OPTION,null)===null,'no production state written before confirmation');
$_POST=['isolated_test_site'=>'1'];$GLOBALS['is_admin']=false;
fails(fn()=>TXE_Workshop::confirmTestMode(),'TEXTERSTELLUNG_ADMIN_ONLY');
$GLOBALS['is_admin']=true;$_POST=[];fails(fn()=>TXE_Workshop::confirmTestMode(),'TESTSITE_CONFIRMATION_REQUIRED');
$_POST=['isolated_test_site'=>'1'];$GLOBALS['nonce_valid']=false;
fails(fn()=>TXE_Workshop::confirmTestMode(),'BAD_NONCE');
affirm(!TXE_Workshop::permitted(),'failed confirmation does not unlock processing');
$GLOBALS['nonce_valid']=true;
fails(fn()=>TXE_Workshop::confirmTestMode(),'REDIRECT_OK');
affirm(TXE_Workshop::permitted(),'valid admin confirmation unlocks only this site');
ob_start();TXE_Workshop::page();$html=ob_get_clean();
affirm(str_contains($html,'0.4.1'),'new version visible');
affirm(str_contains($html,'Testmodus aktiv'),'active site labelled test');
affirm(str_contains($html,'Workflowübersicht'),'full workflow visible after confirmation');
$id=TXE_Workshop::quick(['target_keyword'=>'Pferdedecke und Regen','title'=>'Pferdedecken bei Regen','category'=>'pferdedecken','article_type'=>'Beratung','intent'=>'Kaufberatung']);
affirm(str_starts_with($id,'TXE-'),'existing immediate order still works');
$s=get_option(TXE_Workshop::OPTION,[]);
affirm(count($s['orders']??[])===1,'one order saved with confirmed site');
affirm(($s['orders'][$id]['status']??'')==='FREI','order status unchanged');
$batch=TXE_Workshop::export(1);
affirm(($batch['contract']??'')===TXE_Workshop::K0_CONTRACT,'original K0 contract unchanged');
affirm(($batch['item_count']??0)===1,'one reserved article in K0 batch');
affirm(array_keys($batch['items'][0]??[])===['title','target_keyword','category','article_type','plan_slot'],'exact five K0 fields unchanged');
affirm(($batch['items'][0]['title']??'')==='Pferdedecken bei Regen','approved title preserved');
affirm(($GLOBALS['opts'][TXE_Workshop::OPTION]['orders'][$id]['status']??'')==='EXPORTIERT','single existing worker reserves job');
fails(fn()=>TXE_Workshop::export(1),'NO_APPROVED_READY_ARTICLES');
$repeat=TXE_Workshop::lastBatch();
affirm($repeat['batch_sha256']===$batch['batch_sha256'],'reserved file can be downloaded again');
$byHash=TXE_Workshop::redownloadBatch($batch['batch_sha256']);
affirm($byHash['batch_sha256']===$batch['batch_sha256'],'original batch identity unchanged');

$diag=TXE_Diagnose::snapshot();
affirm(($diag['plugin']['version']??'')==='0.4.1-test','diagnosis version updated');
affirm(($diag['environment']['test_mode_basis']??'')==='EXPLICIT_ADMIN_CONFIRMATION_NOT_ENVIRONMENT_DETECTION','diagnosis explains proof basis');
$GLOBALS['site']='https://an-dere-site.example/';
affirm(!TXE_Workshop::permitted(),'site clone/domain change relocks processing');
fails(fn()=>TXE_Workshop::quick(['target_keyword'=>'test','title'=>'T','category'=>'pferdedecken','article_type'=>'Beratung']),'TESTENVIRONMENT_REQUIRED');
$GLOBALS['site']='https://oliver-beil.de/';
affirm(TXE_Workshop::permitted(),'original test site remains authorized');
echo "ALL TESTS PASSED\n";
