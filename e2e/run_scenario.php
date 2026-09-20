<?php
if (!defined('ABSPATH')) { exit(2); }
$scenario=getenv('AFF_E2E_SCENARIO') ?: 'healthy';
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
if($scenario==='idealo_only'||$scenario==='live_damage'){
    $state=get_option('ppar_network_idealo_v1',array());
    $state['enabled']=1;$state['output_mode']='idealo_only';$state['link_strategy']='products';$state['last_import_at']=time();
    update_option('ppar_network_idealo_v1',$state,false);
}
if($scenario==='missing_exact_reithelme'||$scenario==='live_damage')e2e_clear_exact_for_slug('reithelme',0);
if($scenario==='one_exact_stallhalfter'||$scenario==='live_damage')e2e_clear_exact_for_slug('halfter-und-stricke-stallhalfter',1);
echo 'SCENARIO_MUTATED='.$scenario."\n";
