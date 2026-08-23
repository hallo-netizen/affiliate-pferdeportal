<?php
$root=getenv('PPAR_TEST_PLUGIN_DIR')?:'';
if($root===''||!is_dir($root)){fwrite(STDERR,"PPAR_TEST_PLUGIN_DIR missing\n");exit(2);}
$main=file_get_contents($root.'/pferdeportal-affiliate-router.php');
$run=file_get_contents($root.'/includes/trait-ppar-ebay-run.php');
$ebay=file_get_contents($root.'/includes/trait-ppar-ebay.php');
$readme=file_get_contents($root.'/readme.txt');
$tests=0;$fails=0;
function ok($c,$n){global $tests,$fails;$tests++;if(!$c){$fails++;echo "FAIL $n\n";}else echo "PASS $n\n";}
function body($src,$needle){$p=strpos($src,$needle);if($p===false)return '';$b=strpos($src,'{',$p);$d=0;for($i=$b,$l=strlen($src);$i<$l;$i++){if($src[$i]==='{')$d++;elseif($src[$i]==='}'&&--$d===0)return substr($src,$b+1,$i-$b-1);}return '';}
$handler=body($run,'public function handle_ebay_external_tick');
$url=body($run,'private function ebay_external_tick_url');
$admit=body($run,'private function ebay_external_tick_admit');
$register=body($run,'public function register_ebay_external_tick_route');
$worker=body($run,'public function run_ebay_canonical_worker');
ok(strpos($main,"const VERSION = '6.55.0';")!==false,'version_655');
ok(strpos($main,"const EBAY_RUNTIME_BUILD = '6.55.0-kiss-public-heartbeat-github-scheduler-20260823';")!==false,'runtime_build_655');
ok(strpos($main,'OPTION_EBAY_EXTERNAL_TICK_RATE_LOCK')!==false,'rate_lock_constant');
ok(strpos($register,"'methods'=>'POST'")!==false,'heartbeat_post_only');
ok(strpos($register,"'permission_callback'=>'__return_true'")!==false,'public_trigger_only');
ok(strpos($url,'rest_url(')!==false && strpos($url,'add_query_arg')===false && strpos($url,"'key'")===false,'heartbeat_url_has_no_secret');
ok(strpos($run,'private function ebay_external_tick_key')===false,'secret_generator_removed');
ok(strpos($handler,'get_param')===false && strpos($handler,'hash_equals')===false && strpos($handler,'forbidden')===false,'handler_has_no_shared_secret');
ok(strpos($admit,'< 45')!==false && strpos($admit,'add_option(')!==false,'durable_45s_rate_gate');
ok(strpos($handler,"'status'=>'throttled'")!==false,'throttle_response');
ok(substr_count($handler,'run_ebay_canonical_worker()')===1,'one_package_per_accepted_tick');
ok(strpos($handler,'ebay_external_tick_due_operation')!==false,'due_operation_preserved');
ok(strpos($handler,"'restart_required'=>1")!==false,'failed_run_no_auto_restart');
ok(strpos($handler,"'run_uuid'")===false,'public_response_hides_run_uuid');
ok(strpos($handler,"'error_code'")===false,'public_response_hides_error_code');
ok(strpos($worker,'while(')===false && strpos($worker,'for(')===false && strpos($worker,'foreach(')===false,'canonical_worker_still_bounded');
ok(strpos($worker,'wp_schedule')===false && strpos($worker,'spawn_cron')===false && strpos($worker,'wp_remote_')===false,'worker_no_self_transport');
ok(strpos($ebay,'kein zusätzlicher externer Account ist erforderlich')!==false,'ui_no_external_account');
ok(strpos($ebay,'Heartbeat-URL enthält keinen Geheimschlüssel')!==false,'ui_no_secret');
ok(strpos($ebay,'POST-Ticks')!==false,'ui_post_only');
ok(strpos($readme,'KISS PUBLIC HEARTBEAT + GITHUB SCHEDULER')!==false,'readme_v655');
ok(strpos($readme,'je 45 Sekunden')!==false,'readme_rate_gate');
ok(strpos($readme,'Kandidatbezogene Einzelfehler')!==false,'readme_skip_contract');
echo "ASSERTIONS=$tests FAIL=$fails\n";exit($fails?1:0);
