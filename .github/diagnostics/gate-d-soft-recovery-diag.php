<?php
/* Test-only diagnostic. Never shipped. It reproduces Gate D and dumps the exact
 * durable run before/after migration and after the first real worker tick. */
require '/tmp/v645pkg/CODEX_V645_REALGATE_SOURCE_AND_EXACT_TASK_20260820/03_REAL_GATE/lib.php';

function dmp($label, $value) {
    echo "===== {$label} =====\n";
    echo wp_json_encode($value, JSON_PRETTY_PRINT|JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE) . "\n";
}

rg_settings_business_only();
$uuid='v645-realdb-soft-recovery-diag';
$sel=array(
    'status'=>'failed','phase'=>'failed','failure_reason'=>'business_recovery_incomplete',
    'stats'=>array('business'=>array(
        'errors'=>array(array('item_id'=>'soft-1','code'=>'ebay_business_materialization_not_active')),
        'verification'=>array('expected'=>44,'materialized'=>43,'errors'=>1),
    )),
);
$run=array(
    'schema'=>'1.0','build'=>'6.44.0-business-materialization-gapfill-rootfix-20260820',
    'run_uuid'=>$uuid,'status'=>'failed','phase'=>'failed','finished_at'=>1000,
    'owner'=>'','lease_expires_at'=>0,'worker_transport'=>'admin_ajax',
    'progress_contract_version'=>'2.0','error_code'=>'business_recovery_incomplete',
    'error_message'=>'business_recovery_incomplete',
    'phase_state'=>array('maintenance'=>array('cursor'=>50),'refresh'=>array('last_id'=>2000),'selection'=>$sel),
    'coverage'=>array('covered'=>37),'gapfill'=>array('attempts'=>0,'missing'=>array()),
    'errors'=>array(array('code'=>'business_recovery_incomplete','at'=>1000,'details'=>array('phase'=>'business_materialize','build'=>'6.44.0-business-materialization-gapfill-rootfix-20260820'))),
    'start_manifest'=>array('x'=>1),'end_manifest'=>array('bad'=>1),'recovery_history'=>array(),
);
rg_reset_run($run);
update_option(Pferdeportal_Affiliate_Router::OPTION_EBAY_SELECTION_STATE,$sel,false);
dmp('SEEDED_RUN',rg_run());
$p=rg_plugin();
$p->maybe_migrate_ebay_business_materialization_v6440();
dmp('AFTER_MIGRATION',rg_run());
$retval=rg_tick();
dmp('TICK_RETURN',$retval);
dmp('AFTER_TICK_RUN',rg_run());
dmp('AFTER_TICK_SELECTION',get_option(Pferdeportal_Affiliate_Router::OPTION_EBAY_SELECTION_STATE,array()));

// Control: identical realistic failed V6.44 run, but with the immutable
// config_snapshot that every compatible canonical V6.44 start/adoption creates.
$control=$run;
$control['run_uuid']=$uuid.'-control';
$control['config_snapshot']=array(
    'seller_routes'=>array('private'=>0,'business'=>1),
    'settings'=>array(
        'enabled'=>1,'private_enabled'=>0,'business_enabled'=>1,
        'business_active_cap'=>1000,'business_candidate_pool_per_concept'=>10,
        'business_reserve_per_concept'=>2,'business_max_same_seller_per_block'=>1,
    ),
);
$control['errors'][0]['at']=1001;
$control['finished_at']=1001;
rg_reset_run($control);
update_option(Pferdeportal_Affiliate_Router::OPTION_EBAY_SELECTION_STATE,$sel,false);
dmp('CONTROL_SEEDED_RUN',rg_run());
$p->maybe_migrate_ebay_business_materialization_v6440();
dmp('CONTROL_AFTER_MIGRATION',rg_run());
$retval2=rg_tick();
dmp('CONTROL_TICK_RETURN',$retval2);
dmp('CONTROL_AFTER_TICK_RUN',rg_run());
dmp('CONTROL_AFTER_TICK_SELECTION',get_option(Pferdeportal_Affiliate_Router::OPTION_EBAY_SELECTION_STATE,array()));
