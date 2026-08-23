<?php
require __DIR__.'/lib.php';
rg_settings_business_only();
$uuid='v645-realdb-soft-recovery';
$sel=array(
    'status'=>'failed','phase'=>'failed','failure_reason'=>'business_recovery_incomplete',
    'stats'=>array('business'=>array(
        'errors'=>array(array('item_id'=>'soft-1','code'=>'ebay_business_materialization_not_active')),
        'verification'=>array('expected'=>44,'materialized'=>43,'errors'=>1),
    )),
);

// Reachable V6.44 canonical persisted state: start/adoption always freezes the
// immutable config_snapshot. Start from the shared canonical run fixture so this
// real-gate cannot accidentally omit required durable run fields again.
$run=rg_base_run($uuid);
$run['build']='6.44.0-business-materialization-gapfill-rootfix-20260820';
$run['status']='failed';
$run['phase']='failed';
$run['finished_at']=1000;
$run['error_code']='business_recovery_incomplete';
$run['error_message']='business_recovery_incomplete';
$run['phase_state']=array(
    'maintenance'=>array('cursor'=>50),
    'refresh'=>array('last_id'=>2000),
    'selection'=>$sel,
);
$run['coverage']=array('covered'=>37);
$run['gapfill']=array('attempts'=>0,'missing'=>array());
$run['errors']=array(array(
    'code'=>'business_recovery_incomplete','at'=>1000,
    'details'=>array('phase'=>'business_materialize','build'=>'6.44.0-business-materialization-gapfill-rootfix-20260820'),
));
$run['start_manifest']=array('x'=>1);
$run['end_manifest']=array('bad'=>1);
$run['recovery_history']=array();

rg_reset_run($run);
update_option(Pferdeportal_Affiliate_Router::OPTION_EBAY_SELECTION_STATE,$sel,false);
$p=rg_plugin();
$p->maybe_migrate_ebay_business_materialization_v6440();
$a=rg_run();
rg_assert(($a['run_uuid']??'')===$uuid,'soft candidate failure recovery keeps exact failed-run UUID');
rg_assert(($a['status']??'')==='running' && ($a['phase']??'')==='selection_prepare','proven soft candidate failure reopens only at derived selection boundary');
rg_assert(($a['phase_state']['maintenance']??array())===array('cursor'=>50) && ($a['phase_state']['refresh']??array())===array('last_id'=>2000),'soft recovery preserves prior source/refresh progress');
rg_assert(($a['phase_state']['selection']??array())===array(),'soft recovery clears only derived selection tail');
rg_assert(($a['config_snapshot']??array())===($run['config_snapshot']??array()),'soft recovery preserves immutable V6.44 seller-route/settings snapshot');
rg_assert(get_option(Pferdeportal_Affiliate_Router::OPTION_EBAY_SELECTION_STATE,array())===array(),'legacy selection state is cleared only after successful real DB CAS');
$once=$a;
$p->maybe_migrate_ebay_business_materialization_v6440();
rg_assert(rg_run()===$once,'soft recovery migration is idempotent in real WordPress DB');

// Resume one real bounded package from the recovered persisted state.
rg_tick();
$b=rg_run();
rg_assert(($b['run_uuid']??'')===$uuid,'recovered failed run keeps same UUID through first real selector package');
rg_assert(($b['status']??'')==='running' && ($b['phase']??'')==='selection_prepare','recovered failed run remains in bounded selection_prepare after first package');
rg_assert(absint($b['phase_state']['selection']['prepare_business_index']??0)===8,'recovered failed run resumes real selector at first 8-family checkpoint');
rg_assert(absint($b['transport_tick_count']??0)===1 && absint($b['phase_tick_count']??0)===1,'recovered first package advances transport and phase tick exactly once');

// Negative proof for the exact invalid fixture that caused the previous false
// Gate-D failure: a corrupted canonical run without config_snapshot must fail
// closed with the concrete scope error; it must never be treated as progress.
$bad=$run;
$bad_uuid=$uuid.'-missing-snapshot';
$bad['run_uuid']=$bad_uuid;
unset($bad['config_snapshot']);
$bad['finished_at']=1001;
$bad['errors'][0]['at']=1001;
rg_reset_run($bad);
update_option(Pferdeportal_Affiliate_Router::OPTION_EBAY_SELECTION_STATE,$sel,false);
$p->maybe_migrate_ebay_business_materialization_v6440();
rg_tick();
$bad_after=rg_run();
rg_assert(($bad_after['run_uuid']??'')===$bad_uuid,'missing-snapshot negative case preserves original run UUID');
rg_assert(($bad_after['status']??'')==='failed' && ($bad_after['error_code']??'')==='selection_scope_empty','missing immutable seller-route snapshot fails closed with concrete selection_scope_empty code');

echo "SOFT_RECOVERY_OK\n";
