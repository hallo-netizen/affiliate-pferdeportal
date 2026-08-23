<?php
$root=getenv('PPAR_TEST_PLUGIN_DIR')?:'';
if($root===''||!is_dir($root)){fwrite(STDERR,"PPAR_TEST_PLUGIN_DIR missing\n");exit(2);}
$main=file_get_contents($root.'/pferdeportal-affiliate-router.php');
$run=file_get_contents($root.'/includes/trait-ppar-ebay-run.php');
$ebay=file_get_contents($root.'/includes/trait-ppar-ebay.php');
$readme=file_get_contents($root.'/readme.txt');
$tests=0;$fails=0;
function ok($cond,$name){global $tests,$fails;$tests++;if(!$cond){$fails++;echo "FAIL $name\n";}else{echo "PASS $name\n";}}
function body_of($src,$needle){
  $p=strpos($src,$needle);if($p===false)return '';
  $b=strpos($src,'{',$p);if($b===false)return '';
  $depth=0;$len=strlen($src);
  for($i=$b;$i<$len;$i++){
    if($src[$i]==='{')$depth++;
    elseif($src[$i]==='}'){$depth--;if($depth===0)return substr($src,$b+1,$i-$b-1);}
  }
  return '';
}
$handler=body_of($run,'public function handle_ebay_external_tick');
$schedule=body_of($run,'private function ebay_run_schedule_worker');
$worker=body_of($run,'public function run_ebay_canonical_worker');
$recover=body_of($ebay,'private function ebay_business_materialization_error_is_recoverable');
$apply=body_of($ebay,'private function ebay_selection_apply_business_batch');
$retire=body_of($ebay,'public function retire_ebay_legacy_cron_transport');
$start=body_of($run,'private function ebay_run_start');

ok(strpos($main,"const VERSION = '6.54.0';")!==false,'version_654');
ok(strpos($main,"const EBAY_RUNTIME_BUILD = '6.54.0-kiss-external-tick-skip-20260823';")!==false,'runtime_build_654');
ok(strpos($main,'OPTION_EBAY_EXTERNAL_TICK_KEY')!==false && strpos($main,'EBAY_EXTERNAL_TICK_REST_NAMESPACE')!==false,'external_tick_constants');
ok(strpos($main,"add_action('rest_api_init', array(\$this, 'register_ebay_external_tick_route'))")!==false,'rest_route_registered');
ok(strpos($main,"add_action(self::EBAY_CRON_HOOK")===false && strpos($main,"add_action(self::EBAY_REFRESH_CRON_HOOK")===false && strpos($main,"add_action(self::EBAY_WORKER_HOOK")===false && strpos($main,"add_action(self::EBAY_REFRESH_WORKER_HOOK")===false,'canonical_legacy_cron_actions_removed');
ok(strpos($main,"add_action('init', array(\$this, 'retire_ebay_legacy_cron_transport'), 22)")!==false,'legacy_transport_retired_on_init');
ok(substr_count($retire,'wp_clear_scheduled_hook(')>=4 && strpos($retire,'EBAY_WORKER_HOOK')!==false && strpos($retire,'EBAY_REFRESH_WORKER_HOOK')!==false,'legacy_hooks_cleared');
ok($schedule!=='' && strpos($schedule,'wp_schedule')===false && strpos($schedule,'spawn_cron')===false && strpos($schedule,'wp_remote_')===false,'schedule_worker_is_noop_transport');
ok(strpos($run,'private function ebay_external_tick_key')!==false && strpos($run,'hash_equals($expected')!==false,'authenticated_tick_key');
ok(strpos($handler,"status'=>'failed'")!==false && strpos($handler,"'restart_required'=>1")!==false,'failed_run_not_auto_restarted');
ok(strpos($handler,'ebay_external_tick_due_operation')!==false && strpos($handler,'ebay_run_start(false, $operation)')!==false,'due_cycle_autostart');
ok(substr_count($handler,'run_ebay_canonical_worker()')===1,'one_canonical_package_per_http_tick');
ok(strpos($handler,"'transport'=>'external_tick'")!==false,'tick_response_external_transport');
ok(strpos($run,'3 * HOUR_IN_SECONDS')!==false && strpos($run,'HOUR_IN_SECONDS')!==false,'three_hour_and_hourly_due_contract');
ok(strpos($start,"'worker_transport'=>'external_tick'")!==false && strpos($start,"'transport'=>'external_tick'")!==false,'new_run_external_transport');
ok(strpos($start,"'skipped_item_errors_count'=>0")!==false && strpos($start,"'skipped_item_errors'=>array()")!==false,'skip_audit_initialized');
ok(strpos($worker,'while(')===false && strpos($worker,'for(')===false && strpos($worker,'foreach(')===false,'canonical_coordinator_no_outer_loop');
ok(strpos($worker,'ebay_run_schedule_worker(')===false && strpos($worker,'wp_schedule')===false && strpos($worker,'spawn_cron')===false && strpos($worker,'wp_remote_')===false,'canonical_worker_no_self_transport');
ok(strpos($run,'ebay_run_record_nested_skipped_item_errors')!==false && strpos($worker,'ebay_run_record_nested_skipped_item_errors($fresh)')!==false,'durable_skip_audit_called');
ok(strpos($run,"count(\$log)>500?array_slice(\$log,-500):\$log")!==false,'skip_audit_bounded');
ok(strpos($recover,"ebay_creative_library_missing")!==false && strpos($recover,"storage_unavailable")!==false && strpos($recover,"database_unavailable")!==false,'global_business_failures_excluded_from_skip');
ok(strpos($recover,'return !in_array')!==false,'candidate_business_errors_recoverable');
ok(strpos($apply,'ebay_business_source_row_item')!==false && strpos($apply,'ebay_business_selection_record_soft_failure($state,$stats,$item_id,$item->get_error_code()')!==false,'business_source_error_skipped');
ok(strpos($apply,'ebay_business_quality_assess')!==false && strpos($apply,'$quality->get_error_code()')!==false,'business_quality_error_skipped');
ok(strpos($apply,'business_selection_commit_failed')!==false,'business_commit_failure_still_hard');
ok(strpos($run,"fatal_private=array('storage_unavailable','database_unavailable'")!==false,'private_global_failure_not_counted_as_skip');
ok(strpos($run,"'completed_with_skips'")!==false && strpos($run,"'status']='completed'")!==false,'completed_with_skips_supported');
ok(strpos($ebay,'Fertig (mit übersprungenen Fehlern)')!==false,'ui_completed_with_skips');
ok(strpos($ebay,'Externer Taktgeber:')!==false && strpos($ebay,'einmal pro Minute')!==false,'ui_external_tick_setup');
ok(strpos($ebay,"'transport'=>'wp_cron'")===false && strpos($ebay,"'worker_result'=>'wp_cron'")===false,'ui_no_false_wp_cron_transport');
ok(strpos($readme,'KISS EXTERNAL TICK + SKIP')!==false && strpos($readme,'Kandidatbezogene Einzelfehler')!==false,'readme_contract');

echo "ASSERTIONS=$tests FAIL=$fails\n";
exit($fails?1:0);
