<?php
if (!defined('ABSPATH')) { fwrite(STDERR,"NO_WP\n"); exit(2); }
if (!class_exists('Pferdeportal_Affiliate_Router')) { fwrite(STDERR,"NO_ROUTER\n"); exit(3); }
$o=Pferdeportal_Affiliate_Router::instance();
function hist_call($o,$name,...$args){$m=new ReflectionMethod($o,$name);$m->setAccessible(true);return $m->invokeArgs($o,$args);}
function hist_counts($cands){
  $x=array();
  foreach((array)$cands as $cand){
    $c=is_array($cand)&&isset($cand['campaign'])?$cand['campaign']:$cand;
    if(!is_array($c))continue;
    $n=sanitize_key((string)($c['network']??'unknown'));
    $x[$n]=($x[$n]??0)+1;
  }
  ksort($x); return $x;
}
$targets=array(
  186=>'reithelme',187=>'reithandschuhe',188=>'reitstiefel',189=>'sicherheitswesten',
  190=>'gerten',191=>'sporen',174=>'halfter-und-stricke-stallhalfter'
);
$fail=array(); $selected=array();
foreach($targets as $pid=>$slug){
  $ctx=hist_call($o,'get_content_context',$pid);
  $slots=array();
  foreach(array(1,2,3) as $i){
    $slot='category_product_'.$i;
    $ctx['slot_type']=$slot;
    $sel=hist_call($o,'select_campaign_for_slot',$ctx,$slot,'');
    $c=is_array($sel)&&is_array($sel['campaign']??null)?$sel['campaign']:array();
    $keys=array_values((array)($c['automation_target_keys']??array()));
    $provider=sanitize_key((string)($c['network']??''));
    $ok=$c && in_array('page:'.$slug,$keys,true);
    if(!$ok)$fail[]='TOPIC_TARGET_BREAK:'.$slug.':'.$slot;
    $slots[]=array('slot'=>$slot,'post_id'=>absint($c['post_id']??0),'provider'=>$provider,'title'=>(string)($c['title']??''),'exact_target'=>$ok);
  }
  $selected[$slug]=$slots;
}

/* Historical eBay/idealo eligibility under Reithelme, measured only up to the
   already-proven common external control gate. This deliberately does NOT
   pretend the current compliance veto is open. */
$page_id=186; $slot='category_product_1'; $needle='page:reithelme';
$ctx=hist_call($o,'get_content_context',$page_id); $ctx['slot_type']=$slot;
$all=hist_call($o,'get_campaigns'); $exact=array();
foreach((array)$all as $c){
  if(!is_array($c)||empty($c['active'])||sanitize_key((string)($c['creative_type']??''))!=='product')continue;
  if(!in_array($needle,(array)($c['automation_target_keys']??array()),true))continue;
  $exact[]=$c;
}
$pre=array(); $first_fail=array();
foreach($exact as $c){
  $net=sanitize_key((string)($c['network']??'unknown'));
  $checks=array(
    'complete'=>hist_call($o,'campaign_is_complete',$c),
    'current'=>hist_call($o,'rule_is_current',$c),
    'program'=>hist_call($o,'campaign_program_allows_delivery',$c),
    'seller'=>hist_call($o,'otto_awin_product_campaign_seller_ready',$c),
    'slot'=>hist_call($o,'campaign_slot_allowed',$c,$slot),
  );
  $rank=$checks['slot']?hist_call($o,'campaign_match_rank',$c,$ctx):null;
  $checks['rank']=is_array($rank);
  if($net==='ebay'){
    $checks['source_base']=hist_call($o,'ebay_business_campaign_source_allows_delivery_base',$c);
    $pid=absint($c['post_id']??0);
    $checks['checkpoint']=$pid>0?hist_call($o,'ebay_public_checkpoint_allows_business_campaign',$pid):false;
    $checks['source_full']=hist_call($o,'ebay_business_campaign_source_allows_delivery',$c);
  } else {
    $checks['source_base']=true; $checks['checkpoint']=true; $checks['source_full']=true;
  }
  $checks['image']=hist_call($o,'product_campaign_public_image_ready',$c);
  $ok=!in_array(false,$checks,true);
  if($ok){
    $pre[]=array('campaign'=>$c,'specificity'=>(int)($rank['specificity']??0),'matches'=>(int)($rank['matches']??0),'priority'=>(int)($c['priority']??0));
  } elseif(!isset($first_fail[$net])){
    foreach($checks as $stage=>$v){if(!$v){$first_fail[$net]=array('stage'=>$stage,'post_id'=>absint($c['post_id']??0),'title'=>(string)($c['title']??''));break;}}
  }
}
$pre_counts=hist_counts($pre);
$mode=sanitize_key((string)hist_call($o,'idealo_output_mode'));
$control=hist_call($o,'control_provider_gate','ebay',hist_call($o,'output_local_portal_key'));
$control_code=is_wp_error($control)?$control->get_error_code():'PASS';
echo 'HISTORY_SELECTED='.wp_json_encode($selected,JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE)."\n";
echo 'HISTORY_EXACT_COUNTS='.wp_json_encode(hist_counts($exact),JSON_UNESCAPED_SLASHES)."\n";
echo 'HISTORY_PRECONTROL_ELIGIBLE='.wp_json_encode($pre_counts,JSON_UNESCAPED_SLASHES)."\n";
echo 'HISTORY_PRECONTROL_FIRST_FAIL='.wp_json_encode($first_fail,JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE)."\n";
echo 'HISTORY_IDEALO_MODE='.$mode."\n";
echo 'HISTORY_EBAY_CONTROL='.$control_code."\n";
if(($pre_counts['ebay']??0)<1)$fail[]='EBAY_PRECONTROL_ELIGIBILITY_BREAK';
if(($pre_counts['idealo']??0)<1)$fail[]='IDEALO_PRECONTROL_ELIGIBILITY_BREAK';
if($mode==='idealo_only')$fail[]='IDEALO_ONLY_MODE_BREAK';
if($fail){foreach(array_values(array_unique($fail)) as $f)fwrite(STDERR,'FAIL_'.$f."\n");exit(1);}
echo "HISTORY_PROBE_PASS\n";
