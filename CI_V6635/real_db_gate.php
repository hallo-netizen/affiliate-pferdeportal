<?php
$mode = getenv('GATE_MODE') ?: 'positive';
$uuid='74b8372b-f481-493b-8485-1e98188ef02c';
$proof=array('owner'=>'run:'.$uuid,'business_target_concepts'=>array('concept-a'),'selected_concepts'=>array(),'created_at'=>1000);
$run=array(
 'schema'=>'1.0','build'=>'6.63.4-live-observed-gap-proof-recovery-rootfix-20260828','run_uuid'=>$uuid,'status'=>'failed','phase'=>'failed','finished_at'=>2000,'worker_transport'=>'external_tick','resume_reason'=>'private_public_revalidated','progress_seq'=>20,'progress_contract_version'=>'3.1',
 'config_snapshot'=>array('seller_routes'=>array('private'=>1,'business'=>1),'settings'=>array()),
 'phase_state'=>array('discovery'=>array('status'=>'completed','cursor'=>3159),'selection'=>array('status'=>'complete','phase'=>'complete','prepare_private_scanned'=>545,'prepare_private_leaf_index'=>8)),
 'gapfill'=>array('attempts'=>2,'missing'=>array('concept-a'),'selection_proof'=>$proof),
 'checkpoint_candidate'=>array('business_campaign_ids'=>array(501,502),'private_listing_ids'=>array(101,102)),
 'private_public_revalidation'=>array('status'=>'complete','attempts'=>1,'completed_at'=>1900),
 'recovery_history'=>array(array('reason'=>'business_gap_proof_regeneration','error_code'=>'business_safe_gap_proof_missing','migration_key'=>'prior')),
 'errors'=>array(array('code'=>'private_public_gate_failed','at'=>2000,'details'=>array('phase'=>'public_verify','build'=>'6.63.4-live-observed-gap-proof-recovery-rootfix-20260828','invalid'=>array(101=>'source_stale'),'public'=>250))),
 'error_code'=>'private_public_gate_failed','error_message'=>'PRIVATE-Public-Gate ist fehlgeschlagen.'
);
function gate_fail($m){fwrite(STDERR,"FAIL $m\n");exit(1);} function gate_pass($m){echo "PASS $m\n";}
$admin=get_user_by('login','admin'); if(!$admin) gate_fail('admin_missing'); wp_set_current_user($admin->ID);
add_filter('pre_http_request', function($pre,$args,$url){return array('headers'=>array(),'body'=>'','response'=>array('code'=>202,'message'=>'Accepted'),'cookies'=>array(),'filename'=>null);},10,3);
update_option(Pferdeportal_Affiliate_Router::OPTION_EBAY_RUN_STATE,$run,false);
if($mode==='negative'){
 do_action('admin_init');
 $r=get_option(Pferdeportal_Affiliate_Router::OPTION_EBAY_RUN_STATE,array());
 if(($r['status']??'')!=='failed'||($r['error_code']??'')!=='private_public_gate_failed'||($r['run_uuid']??'')!==$uuid) gate_fail('v6634_exact_live_terminal_negative');
 gate_pass('v6634_exact_live_terminal_negative');
 global $wpdb; $raw=$wpdb->get_var($wpdb->prepare("SELECT option_value FROM {$wpdb->options} WHERE option_name=%s",Pferdeportal_Affiliate_Router::OPTION_EBAY_RUN_STATE)); if(!$raw) gate_fail('v6634_real_mariadb_persisted'); gate_pass('v6634_real_mariadb_persisted'); exit(0);
}
if(Pferdeportal_Affiliate_Router::VERSION!=='6.63.5') gate_fail('version_6635'); gate_pass('version_6635');
$o=Pferdeportal_Affiliate_Router::instance(); $o->maybe_recover_ebay_private_public_freshness_v6635();
$r=get_option(Pferdeportal_Affiliate_Router::OPTION_EBAY_RUN_STATE,array());
if(($r['status']??'')!=='running'||($r['phase']??'')!=='selection_prepare') gate_fail('same_live_state_reopened'); gate_pass('same_live_state_reopened');
if(($r['run_uuid']??'')!==$uuid) gate_fail('same_uuid_preserved'); gate_pass('same_uuid_preserved');
if(($r['phase_state']['discovery']['cursor']??0)!==3159) gate_fail('discovery_preserved'); gate_pass('discovery_preserved');
if(($r['checkpoint_candidate']['business_campaign_ids']??array())!==array(501,502)) gate_fail('business_candidates_preserved'); gate_pass('business_candidates_preserved');
if(($r['gapfill']['selection_proof']??array())!==$proof) gate_fail('business_proof_preserved'); gate_pass('business_proof_preserved');
if(($r['resume_reason']??'')!=='private_public_freshness_revalidation') gate_fail('recovery_reason'); gate_pass('recovery_reason');
$before=count((array)($r['recovery_history']??array())); $o->maybe_recover_ebay_private_public_freshness_v6635(); $r2=get_option(Pferdeportal_Affiliate_Router::OPTION_EBAY_RUN_STATE,array()); if(count((array)($r2['recovery_history']??array()))!==$before) gate_fail('idempotent_second_recovery'); gate_pass('idempotent_second_recovery');
global $wpdb; $raw=$wpdb->get_var($wpdb->prepare("SELECT option_value FROM {$wpdb->options} WHERE option_name=%s",Pferdeportal_Affiliate_Router::OPTION_EBAY_RUN_STATE)); if(!$raw||strpos($raw,$uuid)===false) gate_fail('v6635_real_mariadb_persisted'); gate_pass('v6635_real_mariadb_persisted');
echo "REAL_DB_GATE_PASS\n";
