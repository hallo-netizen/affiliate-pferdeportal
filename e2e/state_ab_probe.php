<?php
if (!defined('ABSPATH')) exit(2);
$o=Pferdeportal_Affiliate_Router::instance();
function abcall($o,$n,...$a){$m=new ReflectionMethod($o,$n);$m->setAccessible(true);return $m->invokeArgs($o,$a);}
function exacts($o,$slug){
  $r=['total'=>0,'ebay'=>0,'idealo'=>0];
  foreach((array)abcall($o,'get_campaigns') as $c){
    if(!is_array($c)||empty($c['active'])||sanitize_key((string)($c['creative_type']??''))!=='product')continue;
    if(!in_array('page:'.$slug,(array)($c['automation_target_keys']??[]),true))continue;
    $n=sanitize_key((string)($c['network']??'')); if(!isset($r[$n]))continue;
    $r['total']++;$r[$n]++;
  }
  return $r;
}
foreach([186=>'reithelme',174=>'halfter-und-stricke-stallhalfter'] as $pid=>$slug){
  echo 'EXACT_'.$slug.'='.wp_json_encode(exacts($o,$slug))."\n";
  $ctx=abcall($o,'get_content_context',$pid);
  $rows=[];
  foreach([1,2,3] as $i){
    $slot='category_product_'.$i; $cctx=$ctx; $cctx['slot_type']=$slot;
    $sel=abcall($o,'select_campaign_for_slot',$cctx,$slot,'');
    $c=is_array($sel)&&is_array($sel['campaign']??null)?$sel['campaign']:[];
    $rows[]=['id'=>absint($c['post_id']??0),'provider'=>sanitize_key((string)($c['network']??'')),'title'=>(string)($c['title']??'')];
  }
  echo 'SELECT_'.$slug.'='.wp_json_encode($rows,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";
}
$i=get_option('ppar_network_idealo_v1',[]);
echo 'IDEALO_MODE='.sanitize_key((string)($i['output_mode']??''))."\n";
$e=get_option('ppar_network_ebay_v1',[]);
echo 'EBAY_ENABLED='.(!empty($e['enabled'])?'1':'0')."\n";
