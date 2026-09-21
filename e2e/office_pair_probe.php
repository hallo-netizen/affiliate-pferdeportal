<?php
if (!defined('ABSPATH')) { exit(2); }
$o=Pferdeportal_Affiliate_Router::instance();
function dbgcall($o,$name,...$args){$m=new ReflectionMethod($o,$name);$m->setAccessible(true);return $m->invokeArgs($o,$args);}
$ctx=dbgcall($o,'get_content_context',186);$ctx['slot_type']='category_product_2';
$out=array();
foreach(dbgcall($o,'get_campaigns') as $c){
  if(!is_array($c))continue;
  $id=absint($c['post_id']??0);
  if(!in_array($id,array(16283,16299),true))continue;
  $rank=dbgcall($o,'campaign_match_rank',$c,$ctx);
  $out[$id]=array(
    'title'=>(string)($c['title']??''),
    'network'=>(string)($c['network']??''),
    'priority'=>absint($c['priority']??0),
    'targets'=>array_values((array)($c['automation_target_keys']??array())),
    'keywords'=>array_values((array)($c['keywords']??array())),
    'rank'=>$rank,
  );
}
echo 'PAIR='.wp_json_encode($out,JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE)."\n";
