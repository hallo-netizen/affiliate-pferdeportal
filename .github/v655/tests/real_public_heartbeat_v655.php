<?php
if(!defined('ABSPATH')){fwrite(STDERR,"WordPress required\n");exit(2);}
$GLOBALS['t']=0;$GLOBALS['f']=0;
function t($c,$n){$GLOBALS['t']++;if(!$c){$GLOBALS['f']++;echo "FAIL $n\n";}else echo "PASS $n\n";}
function priv($o,$n,...$a){$r=new ReflectionMethod($o,$n);$r->setAccessible(true);return $r->invokeArgs($o,$a);}
function data_of($r){return $r instanceof WP_REST_Response?$r->get_data():$r;}
$p=Pferdeportal_Affiliate_Router::instance();
t(Pferdeportal_Affiliate_Router::VERSION==='6.55.0','version');
t(Pferdeportal_Affiliate_Router::EBAY_RUNTIME_BUILD==='6.55.0-kiss-public-heartbeat-github-scheduler-20260823','runtime_build');
do_action('rest_api_init');$routes=rest_get_server()->get_routes();$route='/'.Pferdeportal_Affiliate_Router::EBAY_EXTERNAL_TICK_REST_NAMESPACE.Pferdeportal_Affiliate_Router::EBAY_EXTERNAL_TICK_REST_ROUTE;
t(isset($routes[$route]),'route_exists');
$url=priv($p,'ebay_external_tick_url');t(strpos($url,'?key=')===false&&strpos($url,'key=')===false,'url_no_key');
$settings=$p->ebay_settings_defaults();$settings['enabled']=true;$settings['private_enabled']=true;$settings['business_enabled']=true;$settings['last_sync']=array('finished_at'=>time());$settings['last_refresh']=array('finished_at'=>time());update_option(Pferdeportal_Affiliate_Router::OPTION_NETWORK_EBAY,$settings,false);
$runKey=priv($p,'ebay_run_option_key');$checkpointKey=priv($p,'ebay_public_checkpoint_option_key');delete_option($runKey);delete_option(Pferdeportal_Affiliate_Router::OPTION_EBAY_EXTERNAL_TICK_RATE_LOCK);
$req=new WP_REST_Request('POST',$route);$idle=data_of($p->handle_ebay_external_tick($req));t(($idle['status']??'')==='idle','public_post_idle');t(empty(get_option($runKey,array())),'idle_no_run');
$th=data_of($p->handle_ebay_external_tick($req));t(($th['status']??'')==='throttled','immediate_second_tick_throttled');
update_option(Pferdeportal_Affiliate_Router::OPTION_EBAY_EXTERNAL_TICK_RATE_LOCK,time()-46,false);
$settings['last_sync']=array('finished_at'=>time()-4*HOUR_IN_SECONDS);update_option(Pferdeportal_Affiliate_Router::OPTION_NETWORK_EBAY,$settings,false);
t(priv($p,'ebay_external_tick_due_operation',$settings)==='sync','sync_due');
$checkpoint=array('schema'=>'1.0','status'=>'safe','checkpoint_id'=>'proof-safe','business_campaign_ids'=>array(11),'private_listing_ids'=>array(21),'updated_at'=>time());update_option($checkpointKey,$checkpoint,false);
$old=array('schema'=>'1.0','build'=>'6.54-old','run_uuid'=>'old','status'=>'running','phase'=>'reconcile_local','started_at'=>time()-30,'updated_at'=>time()-30,'phase_state'=>array(),'errors'=>array(),'checkpoint_base_id'=>'proof-safe','owner'=>'','lease_expires_at'=>0);update_option($runKey,$old,false);$p->maybe_close_incompatible_ebay_run_for_checkpoint_restart();$closed=get_option($runKey,array());t(($closed['status']??'')==='failed'&&($closed['error_code']??'')==='run_build_changed_restart_required','old_build_closed');t(get_option($checkpointKey,array())===$checkpoint,'checkpoint_preserved');
update_option(Pferdeportal_Affiliate_Router::OPTION_EBAY_EXTERNAL_TICK_RATE_LOCK,time()-46,false);$failed=data_of($p->handle_ebay_external_tick($req));t(($failed['status']??'')==='failed'&&absint($failed['restart_required']??0)===1,'failed_no_auto_restart');t(!array_key_exists('run_uuid',$failed)&&!array_key_exists('error_code',$failed),'public_failed_response_minimal');
delete_option($runKey);update_option(Pferdeportal_Affiliate_Router::OPTION_EBAY_EXTERNAL_TICK_RATE_LOCK,time()-46,false);
$one=array('schema'=>'1.0','build'=>Pferdeportal_Affiliate_Router::EBAY_RUNTIME_BUILD,'run_uuid'=>'one-package-proof','status'=>'running','phase'=>'test_unknown_phase','operation'=>'sync','remote_subphase'=>'discovery','started_at'=>time(),'updated_at'=>time(),'finished_at'=>0,'owner'=>'','lease_expires_at'=>0,'worker_transport'=>'external_tick','resume_reason'=>'','resume_at'=>0,'no_progress_count'=>0,'last_progress_at'=>time(),'progress_seq'=>0,'last_transport_tick_at'=>0,'transport_tick_count'=>0,'work_block_started_at'=>time(),'work_block_tick_count'=>0,'progress_contract_version'=>priv($p,'ebay_run_progress_contract_version'),'phase_state'=>array(),'coverage'=>array(),'errors'=>array(),'skipped_item_errors_count'=>0,'skipped_item_errors'=>array(),'checkpoint_base_id'=>'proof-safe');update_option($runKey,$one,false);
$r1=data_of($p->handle_ebay_external_tick($req));$after=get_option($runKey,array());t(($after['status']??'')==='failed'&&($after['error_code']??'')==='canonical_phase_unknown','system_invariant_still_terminal');t(absint($after['transport_tick_count']??0)===1,'accepted_http_tick_one_package');
$r2=data_of($p->handle_ebay_external_tick($req));t(($r2['status']??'')==='throttled','second_immediate_does_not_run');$after2=get_option($runKey,array());t(absint($after2['transport_tick_count']??0)===1,'no_second_package');
t(priv($p,'ebay_business_materialization_error_is_recoverable',new WP_Error('ebay_business_import_failed','x'))===true,'candidate_error_skippable');t(priv($p,'ebay_business_materialization_error_is_recoverable',new WP_Error('storage_unavailable','x'))===false,'storage_failure_hard');
delete_option($runKey);delete_option($checkpointKey);delete_option(Pferdeportal_Affiliate_Router::OPTION_EBAY_EXTERNAL_TICK_RATE_LOCK);
echo "REAL_PUBLIC_HEARTBEAT_V655_ASSERTIONS={$GLOBALS['t']} FAIL={$GLOBALS['f']}\n";exit($GLOBALS['f']?1:0);
