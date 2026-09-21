<?php
if (!defined('ABSPATH')) { fwrite(STDERR,"NO_WP\n"); exit(2); }
if (!class_exists('Pferdeportal_Affiliate_Router')) { fwrite(STDERR,"NO_ROUTER\n"); exit(3); }
$o=Pferdeportal_Affiliate_Router::instance();
function office_call($o,$name,...$args){$m=new ReflectionMethod($o,$name);$m->setAccessible(true);return $m->invokeArgs($o,$args);}
$ctx=office_call($o,'get_content_context',186);
$want=array(
 'category_product_1'=>array('id'=>15921,'provider'=>'ebay'),
 'category_product_2'=>array('id'=>16283,'provider'=>'idealo'),
 'category_product_3'=>array('id'=>15986,'provider'=>'ebay'),
);
$got=array(); $fail=array();
foreach($want as $slot=>$expected){
  $cctx=$ctx; $cctx['slot_type']=$slot;
  $sel=office_call($o,'select_campaign_for_slot',$cctx,$slot,'');
  $c=is_array($sel)&&is_array($sel['campaign']??null)?$sel['campaign']:array();
  $id=absint($c['post_id']??0); $provider=sanitize_key((string)($c['network']??''));
  $html=office_call($o,'render_affiliate_slot_for_context',186,$cctx,$slot,'');
  $real=is_string($html) && $html!=='' && stripos($html,'Produktvorschau')===false;
  $got[$slot]=array('id'=>$id,'provider'=>$provider,'real_card'=>$real);
  if($id!==$expected['id'])$fail[]=$slot.':ID:'.$id;
  if($provider!==$expected['provider'])$fail[]=$slot.':PROVIDER:'.$provider;
  if(!$real)$fail[]=$slot.':NOT_REAL_CARD';
}

$pair=array();
$pairctx=$ctx; $pairctx['slot_type']='category_product_2';
foreach(office_call($o,'get_campaigns') as $pc){
  if(!is_array($pc))continue;
  $pid=absint($pc['post_id']??0);
  if(!in_array($pid,array(16283,16299),true))continue;
  $pair[$pid]=array(
    'title'=>(string)($pc['title']??''),
    'network'=>sanitize_key((string)($pc['network']??'')),
    'priority'=>absint($pc['priority']??0),
    'targets'=>array_values((array)($pc['automation_target_keys']??array())),
    'keywords'=>array_values((array)($pc['keywords']??array())),
    'rank'=>office_call($o,'campaign_match_rank',$pc,$pairctx),
  );
}
echo 'OFFICE_PAIR='.wp_json_encode($pair,JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE)."\n";

$ids=array_column($got,'id');
if(count(array_unique($ids))!==3)$fail[]='NOT_3_DISTINCT';
echo 'OFFICE_PASS_GOT='.wp_json_encode($got,JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE)."\n";
if($fail){foreach($fail as $f)fwrite(STDERR,'OFFICE_PASS_FAIL_'.$f."\n");exit(1);}
echo "OFFICE_PASS_EXACT_3_OF_3\n";
