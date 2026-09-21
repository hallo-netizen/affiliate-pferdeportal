<?php
if (!defined('ABSPATH')) { fwrite(STDERR,"NO_WP\n"); exit(2); }
if (!class_exists('Pferdeportal_Affiliate_Router')) { fwrite(STDERR,"NO_ROUTER\n"); exit(3); }
$o=Pferdeportal_Affiliate_Router::instance();
function hist_call($o,$name,...$args){$m=new ReflectionMethod($o,$name);$m->setAccessible(true);return $m->invokeArgs($o,$args);}
$targets=array(
  186=>'reithelme',187=>'reithandschuhe',188=>'reitstiefel',189=>'sicherheitswesten',
  190=>'gerten',191=>'sporen',174=>'halfter-und-stricke-stallhalfter'
);
$fail=array(); $out=array();
foreach($targets as $pid=>$slug){
  $ctx=hist_call($o,'get_content_context',$pid);
  $providers=array(); $slots=array();
  foreach(array(1,2,3) as $i){
    $slot='category_product_'.$i;
    $ctx['slot_type']=$slot;
    $sel=hist_call($o,'select_campaign_for_slot',$ctx,$slot,'');
    $c=is_array($sel)&&is_array($sel['campaign']??null)?$sel['campaign']:array();
    $keys=array_values((array)($c['automation_target_keys']??array()));
    $provider=sanitize_key((string)($c['network']??''));
    $title=(string)($c['title']??'');
    $ok=$c && in_array('page:'.$slug,$keys,true);
    if(!$ok)$fail[]='TOPIC_TARGET_BREAK:'.$slug.':'.$slot;
    if($provider!=='')$providers[$provider]=1;
    $slots[]=array('slot'=>$slot,'post_id'=>absint($c['post_id']??0),'provider'=>$provider,'title'=>$title,'exact_target'=>$ok);
  }
  if($slug==='reithelme' && (!isset($providers['ebay']) || !isset($providers['idealo']))){
    $fail[]='REITHELME_PROVIDER_MIX_BREAK';
  }
  $out[$slug]=$slots;
}
echo 'HISTORY_SELECTED='.wp_json_encode($out,JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE)."\n";
if($fail){foreach(array_values(array_unique($fail)) as $f)fwrite(STDERR,'FAIL_'.$f."\n");exit(1);}
echo "HISTORY_PROBE_PASS\n";
