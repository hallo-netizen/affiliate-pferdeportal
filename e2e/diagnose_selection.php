<?php
if (!defined('ABSPATH')) { fwrite(STDERR,"NO_WP\n"); exit(2); }
if (!class_exists('Pferdeportal_Affiliate_Router')) { fwrite(STDERR,"NO_ROUTER\n"); exit(3); }
$o=Pferdeportal_Affiliate_Router::instance();
function e2e_call($o,$name,...$args){
    $m=new ReflectionMethod($o,$name); $m->setAccessible(true); return $m->invokeArgs($o,$args);
}
function e2e_counts($cands){
    $x=array();
    foreach((array)$cands as $cand){
        $c=is_array($cand)&&isset($cand['campaign'])?$cand['campaign']:$cand;
        if(!is_array($c))continue;
        $n=sanitize_key((string)($c['network']??'unknown'));
        $x[$n]=($x[$n]??0)+1;
    }
    ksort($x); return $x;
}
$page_id=186; $slot='category_product_1'; $needle='page:reithelme';
$ctx=e2e_call($o,'get_content_context',$page_id); $ctx['slot_type']=$slot;
$all=e2e_call($o,'get_campaigns');
$exact=array();
foreach((array)$all as $c){
    if(!is_array($c)||empty($c['active'])||sanitize_key((string)($c['creative_type']??''))!=='product')continue;
    if(!in_array($needle,(array)($c['automation_target_keys']??array()),true))continue;
    $exact[]=$c;
}
echo 'DIAG_MODE='.sanitize_key((string)e2e_call($o,'idealo_output_mode'))."\n";
echo 'DIAG_EXACT_COUNTS='.wp_json_encode(e2e_counts($exact),JSON_UNESCAPED_SLASHES)."\n";
$stageNames=array('complete','current','program','seller','slot','rank','control','health','source_base','checkpoint','source_full','image');
$pass=array(); foreach($stageNames as $s)$pass[$s]=array();
$failFirst=array();
$rankedPre=array();
foreach($exact as $c){
    $net=sanitize_key((string)($c['network']??'unknown')); $pid=absint($c['post_id']??0);
    $checks=array();
    $checks['complete']=e2e_call($o,'campaign_is_complete',$c);
    $checks['current']=e2e_call($o,'rule_is_current',$c);
    $checks['program']=e2e_call($o,'campaign_program_allows_delivery',$c);
    $checks['seller']=e2e_call($o,'otto_awin_product_campaign_seller_ready',$c);
    $checks['slot']=e2e_call($o,'campaign_slot_allowed',$c,$slot);
    $rank=$checks['slot']?e2e_call($o,'campaign_match_rank',$c,$ctx):null;
    $checks['rank']=is_array($rank);
    $checks['control']=$checks['rank']?e2e_call($o,'campaign_control_allows_delivery',$c,$slot):false;
    $checks['health']=$checks['control']?e2e_call($o,'campaign_health_allows_delivery',$c):false;
    if($net==='ebay'){
        $checks['source_base']=e2e_call($o,'ebay_business_campaign_source_allows_delivery_base',$c);
        $checks['checkpoint']=$pid>0?e2e_call($o,'ebay_public_checkpoint_allows_business_campaign',$pid):false;
        $checks['source_full']=e2e_call($o,'ebay_business_campaign_source_allows_delivery',$c);
    } else {
        $checks['source_base']=true; $checks['checkpoint']=true; $checks['source_full']=true;
    }
    $checks['image']=e2e_call($o,'product_campaign_public_image_ready',$c);
    foreach($stageNames as $s){ if(!empty($checks[$s]))$pass[$s][$net]=($pass[$s][$net]??0)+1; }
    foreach($checks as $s=>$ok){ if(!$ok && !isset($failFirst[$net])){$failFirst[$net]=array('stage'=>$s,'post_id'=>$pid,'title'=>(string)($c['title']??''),'contract'=>(string)get_post_meta($pid,'_ppar_ebay_business_match_contract',true),'hash'=>(string)get_post_meta($pid,'_ppar_creative_identity_hash',true)); break;}}
    if($checks['complete']&&$checks['current']&&$checks['program']&&$checks['seller']&&$checks['slot']&&$checks['rank']&&$checks['control']&&$checks['health']){
        $rankedPre[]=array('campaign'=>$c,'specificity'=>(int)$rank['specificity'],'matches'=>(int)$rank['matches'],'priority'=>(int)($c['priority']??0),'reason'=>(string)$rank['reason']);
    }
}
usort($rankedPre,function($a,$b){foreach(array('specificity','matches','priority') as $k){if($a[$k]!==$b[$k])return $a[$k]>$b[$k]?-1:1;}return strcmp((string)($a['campaign']['id']??''),(string)($b['campaign']['id']??''));});
$afterEbay=e2e_call($o,'ebay_filter_ranked_product_candidates_provider_cohort',$rankedPre);
$afterStrategy=e2e_call($o,'multiprovider_filter_candidates_by_strategy',$afterEbay);
$imageReady=array_values(array_filter($afterStrategy,function($cand)use($o){$c=is_array($cand)?($cand['campaign']??null):null;return is_array($c)&&e2e_call($o,'product_campaign_public_image_ready',$c);}));
$final=e2e_call($o,'ranked_campaigns_for_slot',$ctx,$slot,'');
echo 'DIAG_STAGE_PASS='.wp_json_encode($pass,JSON_UNESCAPED_SLASHES)."\n";
echo 'DIAG_FIRST_FAIL='.wp_json_encode($failFirst,JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE)."\n";
echo 'DIAG_PRE_FILTER='.wp_json_encode(e2e_counts($rankedPre),JSON_UNESCAPED_SLASHES)."\n";
echo 'DIAG_AFTER_EBAY_FILTER='.wp_json_encode(e2e_counts($afterEbay),JSON_UNESCAPED_SLASHES)."\n";
echo 'DIAG_AFTER_STRATEGY='.wp_json_encode(e2e_counts($afterStrategy),JSON_UNESCAPED_SLASHES)."\n";
echo 'DIAG_AFTER_IMAGE='.wp_json_encode(e2e_counts($imageReady),JSON_UNESCAPED_SLASHES)."\n";
echo 'DIAG_FINAL='.wp_json_encode(e2e_counts($final),JSON_UNESCAPED_SLASHES)."\n";
$top=array();
foreach(array_slice($final,0,12) as $cand){$c=$cand['campaign'];$top[]=array('post_id'=>absint($c['post_id']??0),'network'=>sanitize_key((string)($c['network']??'')),'specificity'=>(int)($cand['specificity']??0),'title'=>(string)($c['title']??''));}
echo 'DIAG_TOP='.wp_json_encode($top,JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE)."\n";
