<?php
if (!defined('ABSPATH')) { exit(2); }
$scenario=getenv('AFF_E2E_SCENARIO') ?: 'healthy';
if ($scenario==='healthy') {
    $root=getenv('GITHUB_WORKSPACE');
    $previous='';
    foreach (array('108','109','110','111','112','113','114','115','116','117') as $v) {
        echo "===== HISTORY 6.72.$v =====\n";
        if ($v!=='108') {
            $plugin='/tmp/wp/wp-content/plugins/affiliate-portal-router';
            $zip='/tmp/history-zips/v6.72.'.$v.'.zip';
            $cmd='rm -rf '.escapeshellarg($plugin).' && unzip -q '.escapeshellarg($zip).' -d '.escapeshellarg('/tmp/wp/wp-content/plugins');
            passthru($cmd,$swap_rc);
            if ($swap_rc!==0) {
                file_put_contents('/tmp/aff-history-stop',"6.72.$v\n");
                fwrite(STDERR,"FAIL_HISTORY_INSTALL_6.72.$v\n");
                exit(20);
            }
        }
        $probe='wp eval-file '.escapeshellarg($root.'/e2e/history_probe.php').' --path=/tmp/wp';
        passthru($probe,$probe_rc);
        $http='python3 '.escapeshellarg($root.'/e2e/check_http.py').' healthy';
        passthru($http,$http_rc);
        if ($probe_rc!==0 || $http_rc!==0) {
            file_put_contents('/tmp/aff-history-stop',"6.72.$v\n");
            echo "FIRST_EXACT_HISTORY_BREAK=6.72.$v\n";
            if ($previous!=='') echo "FIRST_EXACT_HISTORY_DELTA=6.72.$previous->6.72.$v\n";
            else echo "BASELINE_6.72.108_FAILED_NO_LATER_DELTA_CLAIMED\n";
            passthru('wp db export '.escapeshellarg('/tmp/history-break-v'.$v.'.sql').' --path=/tmp/wp');
            exit(21);
        }
        echo "HISTORY_VERSION_PASS=6.72.$v\n";
        $previous=$v;
    }
    echo "HISTORY_108_TO_117_ALL_PASS\n";
} elseif (is_file('/tmp/aff-history-stop')) {
    echo "SCENARIO_SKIPPED_AFTER_FIRST_HISTORY_BREAK=$scenario\n";
    exit(0);
}
function e2e_clear_exact_for_slug($slug,$keep=0){
    $posts=get_posts(array('post_type'=>'ap_campaign','post_status'=>'any','numberposts'=>-1,'fields'=>'ids'));
    $kept=0;
    foreach($posts as $id){
        $c=get_post_meta($id,'ppar_campaign_data',true);
        if(!is_array($c)||empty($c['active'])||sanitize_key((string)($c['creative_type']??''))!=='product')continue;
        $keys=array_values((array)($c['automation_target_keys']??array()));
        $needle='page:'.$slug;
        if(!in_array($needle,$keys,true))continue;
        if($kept<$keep){$kept++;continue;}
        $c['automation_target_keys']=array_values(array_filter($keys,static fn($k)=>$k!==$needle));
        update_post_meta($id,'ppar_campaign_data',$c);
    }
}
if($scenario==='ebay_control_open'){
    update_option('ppar_ebay_deletion_state_v1',array(
        'challenge_answered_at'=>time()-60,
        'last_notification_at'=>time()-30,
        'last_notification_status'=>'verified',
        'last_notification_hash'=>str_repeat('a',64),
        'last_deleted_items'=>0,'last_deleted_creatives'=>0,'last_deleted_outputs'=>0,'last_error'=>'',
    ),false);
    $ebay=get_option('ppar_network_ebay_v1',array()); if(!is_array($ebay))$ebay=array();
    $ebay['enabled']=1; update_option('ppar_network_ebay_v1',$ebay,false);
    $access=get_option('ppar_provider_access_state_v1',array()); if(!is_array($access))$access=array();
    $access['ebay']=array('status'=>'connected','last_checked'=>time(),'message'=>'E2E diagnostic: control gate opened','updated_at'=>time());
    update_option('ppar_provider_access_state_v1',$access,false);
}
if($scenario==='idealo_only'||$scenario==='live_damage'){
    $state=get_option('ppar_network_idealo_v1',array());
    $state['enabled']=1;$state['output_mode']='idealo_only';$state['link_strategy']='products';$state['last_import_at']=time();
    update_option('ppar_network_idealo_v1',$state,false);
}
if($scenario==='missing_exact_reithelme'||$scenario==='live_damage')e2e_clear_exact_for_slug('reithelme',0);
if($scenario==='one_exact_stallhalfter'||$scenario==='live_damage')e2e_clear_exact_for_slug('halfter-und-stricke-stallhalfter',1);
echo 'SCENARIO_MUTATED='.$scenario."\n";
