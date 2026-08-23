<?php
if(!defined('ABSPATH')){fwrite(STDERR,"WordPress required\n");exit(2);}
$GLOBALS['v654_tests']=0;$GLOBALS['v654_fails']=0;
function t($cond,$name){$GLOBALS['v654_tests']++;if(!$cond){$GLOBALS['v654_fails']++;echo "FAIL $name\n";}else echo "PASS $name\n";}
function priv($obj,$name,...$args){$r=new ReflectionMethod($obj,$name);$r->setAccessible(true);return $r->invokeArgs($obj,$args);}
function data_of($response){return $response instanceof WP_REST_Response?$response->get_data():$response;}

$plugin=Pferdeportal_Affiliate_Router::instance();
t(Pferdeportal_Affiliate_Router::VERSION==='6.54.0','version');
t(Pferdeportal_Affiliate_Router::EBAY_RUNTIME_BUILD==='6.54.0-kiss-external-tick-skip-20260823','runtime_build');

do_action('rest_api_init');
$routes=rest_get_server()->get_routes();
$route='/'.Pferdeportal_Affiliate_Router::EBAY_EXTERNAL_TICK_REST_NAMESPACE.Pferdeportal_Affiliate_Router::EBAY_EXTERNAL_TICK_REST_ROUTE;
t(isset($routes[$route]),'rest_route_exists');

$key=priv($plugin,'ebay_external_tick_key');
t(is_string($key)&&strlen($key)>=32,'secret_key_generated');
t(hash_equals($key,(string)get_option(Pferdeportal_Affiliate_Router::OPTION_EBAY_EXTERNAL_TICK_KEY,'')),'secret_key_persisted');

$bad=new WP_REST_Request('GET',$route);$bad->set_param('key','wrong');
$badRes=$plugin->handle_ebay_external_tick($bad);
t(is_wp_error($badRes)&&$badRes->get_error_code()==='ebay_external_tick_forbidden','bad_key_rejected');
t(is_wp_error($badRes)&&absint(($badRes->get_error_data()?:array())['status']??0)===403,'bad_key_403');

$settings=$plugin->ebay_settings_defaults();
$settings['enabled']=true;$settings['private_enabled']=true;$settings['business_enabled']=true;
$settings['last_sync']=array('finished_at'=>time());$settings['last_refresh']=array('finished_at'=>time());
update_option(Pferdeportal_Affiliate_Router::OPTION_NETWORK_EBAY,$settings,false);

t(priv($plugin,'ebay_external_tick_due_operation',$settings)==='','fresh_cycle_idle');
$s=$settings;$s['last_sync']=array('finished_at'=>time()-4*HOUR_IN_SECONDS);t(priv($plugin,'ebay_external_tick_due_operation',$s)==='sync','three_hour_sync_due');
$s=$settings;$s['last_refresh']=array('finished_at'=>time()-2*HOUR_IN_SECONDS);t(priv($plugin,'ebay_external_tick_due_operation',$s)==='refresh','hourly_refresh_due');

$runKey=priv($plugin,'ebay_run_option_key');
$checkpointKey=priv($plugin,'ebay_public_checkpoint_option_key');
$checkpoint=array('schema'=>'1.0','status'=>'safe','checkpoint_id'=>'proof-safe','business_campaign_ids'=>array(11,12),'private_listing_ids'=>array(21,22),'updated_at'=>time());
update_option($checkpointKey,$checkpoint,false);
$oldRun=array('schema'=>'1.0','build'=>'6.53-old-test','run_uuid'=>'old-build-proof','status'=>'running','phase'=>'reconcile_local','started_at'=>time()-30,'updated_at'=>time()-30,'phase_state'=>array(),'errors'=>array(),'checkpoint_base_id'=>'proof-safe','owner'=>'','lease_expires_at'=>0);
update_option($runKey,$oldRun,false);
$plugin->maybe_close_incompatible_ebay_run_for_checkpoint_restart();
$closed=get_option($runKey,array());
t(($closed['status']??'')==='failed'&&($closed['error_code']??'')==='run_build_changed_restart_required','old_build_closed_fail_safe');
t(get_option($checkpointKey,array())===$checkpoint,'safe_checkpoint_unchanged_on_build_close');

$good=new WP_REST_Request('GET',$route);$good->set_param('key',$key);
$failedResponse=data_of($plugin->handle_ebay_external_tick($good));
t(is_array($failedResponse)&&($failedResponse['status']??'')==='failed'&&absint($failedResponse['restart_required']??0)===1,'failed_run_requires_manual_restart');
t(($failedResponse['run_uuid']??'')==='old-build-proof','failed_run_uuid_not_replaced');

delete_option($runKey);
$idle=data_of($plugin->handle_ebay_external_tick($good));
t(is_array($idle)&&($idle['status']??'')==='idle','authenticated_fresh_tick_idle');
t(empty(get_option($runKey,array())),'idle_tick_does_not_create_run');

$legacy=array(Pferdeportal_Affiliate_Router::EBAY_CRON_HOOK,Pferdeportal_Affiliate_Router::EBAY_REFRESH_CRON_HOOK,Pferdeportal_Affiliate_Router::EBAY_REFRESH_WORKER_HOOK,Pferdeportal_Affiliate_Router::EBAY_WORKER_HOOK);
foreach($legacy as $hook){wp_clear_scheduled_hook($hook);wp_schedule_single_event(time()+300,$hook);t((bool)wp_next_scheduled($hook),'legacy_hook_fixture_'.$hook);}
wp_clear_scheduled_hook(Pferdeportal_Affiliate_Router::EBAY_MEDIA_CLEANUP_HOOK);wp_schedule_single_event(time()+300,Pferdeportal_Affiliate_Router::EBAY_MEDIA_CLEANUP_HOOK);
$plugin->retire_ebay_legacy_cron_transport();
foreach($legacy as $hook){t(!wp_next_scheduled($hook),'legacy_hook_retired_'.$hook);}
t((bool)wp_next_scheduled(Pferdeportal_Affiliate_Router::EBAY_MEDIA_CLEANUP_HOOK),'media_housekeeping_not_mistaken_for_canonical_transport');
wp_clear_scheduled_hook(Pferdeportal_Affiliate_Router::EBAY_MEDIA_CLEANUP_HOOK);

t(priv($plugin,'ebay_business_materialization_error_is_recoverable',new WP_Error('ebay_business_import_failed','x'))===true,'business_candidate_import_skippable');
t(priv($plugin,'ebay_business_materialization_error_is_recoverable',new WP_Error('ebay_business_concept_missing','x'))===true,'business_candidate_concept_skippable');
t(priv($plugin,'ebay_business_materialization_error_is_recoverable',new WP_Error('ebay_creative_library_missing','x'))===false,'creative_library_failure_hard');
t(priv($plugin,'ebay_business_materialization_error_is_recoverable',new WP_Error('storage_unavailable','x'))===false,'storage_failure_hard');

$auditRun=array('schema'=>'1.0','build'=>Pferdeportal_Affiliate_Router::EBAY_RUNTIME_BUILD,'run_uuid'=>'skip-audit','status'=>'running','phase'=>'selection_prepare','phase_state'=>array('selection'=>array('stats'=>array('business'=>array('recoverable_errors'=>array(array('item_id'=>'B1','code'=>'ebay_business_import_failed','concept'=>'sattel'))),'private'=>array('errors'=>array(array('item_id'=>'P1','code'=>'private_raw_missing'),array('code'=>'storage_unavailable')))))),'skipped_item_errors_count'=>0,'skipped_item_errors'=>array(),'owner'=>'','lease_expires_at'=>0,'errors'=>array());
update_option($runKey,$auditRun,false);
$recorded=priv($plugin,'ebay_run_record_nested_skipped_item_errors',$auditRun);
t(absint($recorded['skipped_item_errors_count']??0)===2,'two_candidate_errors_audited');
t(count((array)($recorded['skipped_item_errors']??array()))===2,'skip_audit_has_details');
$recordedAgain=priv($plugin,'ebay_run_record_nested_skipped_item_errors',$recorded);
t(absint($recordedAgain['skipped_item_errors_count']??0)===2,'skip_audit_deduplicated');

$progress=priv($plugin,'ebay_run_progress_contract_version');
$one=array('schema'=>'1.0','build'=>Pferdeportal_Affiliate_Router::EBAY_RUNTIME_BUILD,'run_uuid'=>'one-package-proof','status'=>'running','phase'=>'test_unknown_phase','operation'=>'sync','remote_subphase'=>'discovery','started_at'=>time(),'updated_at'=>time(),'finished_at'=>0,'owner'=>'','lease_expires_at'=>0,'worker_transport'=>'external_tick','resume_reason'=>'','resume_at'=>0,'no_progress_count'=>0,'last_progress_at'=>time(),'progress_seq'=>0,'last_transport_tick_at'=>0,'transport_tick_count'=>0,'work_block_started_at'=>time(),'work_block_tick_count'=>0,'progress_contract_version'=>$progress,'phase_state'=>array(),'coverage'=>array(),'errors'=>array(),'skipped_item_errors_count'=>0,'skipped_item_errors'=>array(),'checkpoint_base_id'=>'proof-safe');
update_option($runKey,$one,false);
$r1=data_of($plugin->handle_ebay_external_tick($good));$after1=get_option($runKey,array());
t(($after1['status']??'')==='failed'&&($after1['error_code']??'')==='canonical_phase_unknown','system_invariant_failure_still_terminal');
t(absint($after1['transport_tick_count']??0)===1,'one_http_tick_equals_one_canonical_tick');
$r2=data_of($plugin->handle_ebay_external_tick($good));$after2=get_option($runKey,array());
t(absint($after2['transport_tick_count']??0)===1,'failed_run_second_tick_does_not_run_again');
t(($r2['status']??'')==='failed'&&absint($r2['restart_required']??0)===1,'failed_run_not_auto_restarted_by_scheduler');

delete_option($runKey);delete_option($checkpointKey);
// Restore an explicitly fresh enabled fixture for the subsequent real HTTP process.
update_option(Pferdeportal_Affiliate_Router::OPTION_NETWORK_EBAY,$settings,false);
t(!empty((array)get_option(Pferdeportal_Affiliate_Router::OPTION_NETWORK_EBAY,array())),'http_fixture_persisted');
echo "REAL_EXTERNAL_TICK_V654_ASSERTIONS={$GLOBALS['v654_tests']} FAIL={$GLOBALS['v654_fails']}\n";
exit($GLOBALS['v654_fails']?1:0);
