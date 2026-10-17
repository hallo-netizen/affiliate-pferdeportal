<?php
error_reporting(E_ALL);
define('ABSPATH','/tmp/');
$mode=$argv[1]??'positive';$_POST['_wpnonce']=$mode==='unauthorized'?'bad':'valid';
class PSTE_Plugin {public static function assertReady():void{}}
class PSTE_Auth {public static function assertAdmin($action,$nonce){if($action!=='pste_sandbox_recheck_internal'||$nonce!=='valid')throw new RuntimeException('PSTE_ADMIN_FORBIDDEN');}}
class PSTE_Semantic_Review_Sandbox {public static bool $forced=false;public static function refreshInternalStructureBacklog(bool $force=false):array {self::$forced=$force;return ['status'=>($GLOBALS['mode']??'')==='partial'?'PARTIAL_FAILURE':'IN_PROGRESS','checked'=>7,'changed'=>3,'failed'=>($GLOBALS['mode']??'')==='partial'?1:0,'provider_calls'=>0];}}
class PSTE_Sandbox_Maintenance_Health {public static array $events=[];public static function recordAttempt($name){self::$events[]='ATTEMPT';}public static function recordSuccess($name,$report){self::$events[]='SUCCESS';}public static function recordProgress($name,$report){self::$events[]='PROGRESS';}public static function recordFailure($name,$error,$report=[]){self::$events[]='FAILURE';}}
$GLOBALS['mode']=$mode;$GLOBALS['last_redirect']='';
function admin_url($path=''){return 'https://wp.test/wp-admin/'.$path;}
function wp_safe_redirect($url){$GLOBALS['last_redirect']=$url;}
function set_transient($k,$v,$t){$GLOBALS['set_transient']=$v;}
register_shutdown_function(function(){
 $data=['mode'=>$GLOBALS['mode'],'force'=>PSTE_Semantic_Review_Sandbox::$forced,'events'=>PSTE_Sandbox_Maintenance_Health::$events,'redirect'=>$GLOBALS['last_redirect']];
 file_put_contents('/mnt/data/seo_work/manual_post_'.$GLOBALS['mode'].'.json',json_encode($data));
 echo json_encode($data)."\n";
});
require (getenv('PSTE_SOURCE_DIR')?:'/mnt/data/seo_work/modified/Portal SEO Topic Engine').'/includes/class-pste-admin.php';
PSTE_Admin::sandboxRecheckInternal();