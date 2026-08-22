<?php
// Real WordPress/MariaDB delta gate. Reuse the complete V6.49 real fixture first,
// then exercise only the expressly changed V6.50 terminal coverage contract.
require __DIR__.'/public_coverage_target_bridge_v649.php';
$stage=getenv('PPAR_V650_STAGE')?:'final';
$settings=array('business_enabled'=>1,'private_enabled'=>0);

// Recreate the actual live shape: 91 public-safe families and 220 missing.
$keep=array_slice($required,0,91);$keep_map=array_fill_keys($keep,true);$missing=array_values(array_diff($required,$keep));sort($missing,SORT_STRING);
foreach($required as $concept){$wpdb->update($output_table,array('status'=>isset($keep_map[$concept])?'published':'draft'),array('id'=>$object_ids_by_concept[$concept]));}
v649_clear_campaign_cache($p);$partial=v649_call($p,'ebay_run_public_business_coverage');
rg_assert(absint($partial['required']??0)===311&&absint($partial['covered']??0)===91&&count((array)($partial['missing']??array()))===220,'V6.50 real DB starts from exact 91/311 public shape');

$uuid='v650-real-safe-gap-'.sanitize_key($stage);
$selection=array(
 'version'=>'2.0','status'=>'complete','phase'=>'complete','reason'=>'canonical_gapfill','owner'=>'run:'.$uuid,
 'selection_scope'=>'business','business_target_mode'=>'gapfill','business_target_concepts'=>$missing,'business_active'=>array(),
 'stats'=>array('business'=>array('scanned'=>0,'active'=>0,'reserve'=>0,'candidate'=>0,'deactivated'=>0,'materialized'=>0,'errors'=>array()))
);
$run=rg_base_run($uuid,2100,2100);$run['build']=Pferdeportal_Affiliate_Router::EBAY_RUNTIME_BUILD;$run['status']='running';$run['phase']='coverage_verify';
$run['config_snapshot']['seller_routes']=array('private'=>0,'business'=>1);$run['config_snapshot']['settings']['business_enabled']=1;$run['config_snapshot']['settings']['private_enabled']=0;
$run['phase_state']['selection']=$selection;$run['coverage']=$partial;$run['gapfill']=array('attempts'=>1,'missing'=>$missing);$run['errors']=array();$run['end_manifest']=array();
rg_reset_run($run);v649_call($p,'ebay_run_tick_coverage',rg_run(),$settings);$after=rg_run();
rg_assert(($after['status']??'')==='running'&&($after['phase']??'')==='public_verify','V6.50 proven real supply gaps advance to public_verify instead of terminal source failure');
rg_assert(($after['coverage']['contract_status']??'')==='complete_with_safe_supply_gaps'&&absint($after['coverage']['open_gap_count']??0)===220,'V6.50 real coverage persists exact 220 open safe gaps');
$exceptions=(array)($after['coverage']['exceptions']??array());$safe=true;foreach($missing as $id){$e=$exceptions[$id]??array();if(($e['code']??'')!=='safe_supply_gap_open'||absint($e['approved']??1)!==0||absint($e['public']??1)!==0){$safe=false;break;}}
rg_assert($safe,'V6.50 real open gaps are all explicitly non-approved and non-public');
v649_call($p,'ebay_run_tick_public_verify',rg_run(),$settings);$done=rg_run();
rg_assert(($done['status']??'')==='completed'&&($done['end_manifest']['business']['contract_status']??'')==='complete_with_safe_supply_gaps','V6.50 real public gate completes only with explicit safe-gap manifest');
rg_assert(absint($done['gapfill']['attempts']??0)===1&&($done['run_uuid']??'')===$uuid,'V6.50 safe-gap completion preserves same UUID and exactly one gapfill');

// Counterproof: if terminal selection says a safe candidate exists for a missing
// family, missing public output is a technical invariant failure, never a gap.
$bad=$run;$bad['run_uuid']='v650-real-invariant-'.$stage;$bad['phase_state']['selection']['owner']='run:'.$bad['run_uuid'];$bad['phase_state']['selection']['business_active']=array('selected-proof'=>array('concept'=>$missing[0],'rank'=>1));
rg_reset_run($bad);v649_call($p,'ebay_run_tick_coverage',rg_run(),$settings);$failed=rg_run();
rg_assert(($failed['status']??'')==='failed'&&($failed['error_code']??'')==='business_gapfill_public_invariant_failed','V6.50 real selected-but-not-public family remains hard fail-closed invariant');

// Migration is introduced in step2. It may reopen only the exact V6.49 terminal
// signature and must preserve all completed component state under the same UUID.
if($stage==='step1'){
 rg_assert(!method_exists($p,'maybe_migrate_ebay_safe_supply_gap_v6500'),'step1 real gate has no V6.49 safe-gap migration yet');
}else{
 $m_uuid='v650-real-migrate-'.$stage;$m_sel=$selection;$m_sel['owner']='run:'.$m_uuid;
 $m=rg_base_run($m_uuid,2200,2200);$m['build']='6.49.0-public-coverage-target-bridge-rootfix-20260821';$m['status']='failed';$m['phase']='failed';$m['finished_at']=2201;$m['error_code']='insufficient_safe_sources';$m['error_message']='old terminal';
 $m['config_snapshot']['seller_routes']=array('private'=>0,'business'=>1);$m['config_snapshot']['settings']['business_enabled']=1;$m['phase_state']=array('refresh'=>array('status'=>'completed','sentinel'=>'KEEP_REFRESH'),'discovery'=>array('status'=>'completed','sentinel'=>'KEEP_DISCOVERY'),'selection'=>$m_sel);
 $m['coverage']=$partial;$m['gapfill']=array('attempts'=>1,'missing'=>$missing);$m['errors']=array(array('code'=>'insufficient_safe_sources','at'=>2201,'details'=>array('phase'=>'coverage_verify','build'=>$m['build'])));$m['end_manifest']=array('old'=>1);
 rg_reset_run($m);$before=rg_run();$p->maybe_migrate_ebay_safe_supply_gap_v6500();$mig=rg_run();
 rg_assert(($mig['run_uuid']??'')===$m_uuid&&($mig['status']??'')==='running'&&($mig['phase']??'')==='public_verify','V6.50 real migration reopens only proven V6.49 safe-gap failure on same UUID');
 rg_assert(($mig['phase_state']??array())===($before['phase_state']??array())&&($mig['gapfill']??array())===($before['gapfill']??array()),'V6.50 real migration preserves completed refresh/discovery/selection and gapfill state byte-for-byte');
 v649_call($p,'ebay_run_tick_public_verify',rg_run(),$settings);$migdone=rg_run();
 rg_assert(($migdone['status']??'')==='completed'&&absint($migdone['end_manifest']['business']['open_gap_count']??0)===220,'V6.50 migrated real V6.49 UUID completes with exact 220 non-public gaps');
}

// Follow-up canonical coverage: when external supply later becomes safe/public,
// the next run closes the old gaps without any special recovery loop.
foreach($missing as $concept){$wpdb->update($output_table,array('status'=>'published'),array('id'=>$object_ids_by_concept[$concept]));}
v649_clear_campaign_cache($p);$full=v649_call($p,'ebay_run_public_business_coverage');
rg_assert(absint($full['covered']??0)===311&&empty($full['missing']),'V6.50 follow-up real DB can close all previously open gaps');
$f_uuid='v650-real-followup-'.$stage;$follow=rg_base_run($f_uuid,2300,2300);$follow['build']=Pferdeportal_Affiliate_Router::EBAY_RUNTIME_BUILD;$follow['status']='running';$follow['phase']='coverage_verify';$follow['config_snapshot']['seller_routes']=array('private'=>0,'business'=>1);$follow['config_snapshot']['settings']['business_enabled']=1;$follow['gapfill']=array('attempts'=>0,'missing'=>array());$follow['coverage']=array();$follow['errors']=array();
rg_reset_run($follow);v649_call($p,'ebay_run_tick_coverage',rg_run(),$settings);rg_assert((rg_run()['phase']??'')==='public_verify','V6.50 follow-up full supply advances normally without gapfill');v649_call($p,'ebay_run_tick_public_verify',rg_run(),$settings);$followdone=rg_run();
rg_assert(($followdone['status']??'')==='completed'&&($followdone['end_manifest']['business']['contract_status']??'')==='complete'&&absint($followdone['end_manifest']['business']['open_gap_count']??-1)===0,'V6.50 follow-up run closes coverage gaps back to normal complete contract');

echo "COVERAGE_GAP_CONTRACT_V650_OK stage={$stage}\n";
