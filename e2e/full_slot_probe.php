<?php
if (!defined('ABSPATH')) { exit(2); }
$o=Pferdeportal_Affiliate_Router::instance();
function fs_call($o,$name,...$args){$m=new ReflectionMethod($o,$name);$m->setAccessible(true);return $m->invokeArgs($o,$args);}
$ctx=fs_call($o,'get_content_context',186);
echo 'MODE='.fs_call($o,'idealo_output_mode')."\n";
echo 'LINK='.fs_call($o,'idealo_link_strategy')."\n";
foreach(array('category_product_1','category_product_2','category_product_3') as $slot){
  $cctx=$ctx;$cctx['slot_type']=$slot;
  $ranked=fs_call($o,'ranked_campaigns_for_slot',$cctx,$slot,'');
  $strict=fs_call($o,'category_product_strict_relevance_tier_v672104',$ranked,$slot);
  echo 'SLOT='.$slot.' RANKED_COUNT='.count($ranked).' STRICT_COUNT='.count($strict)."\n";
  $i=0;
  foreach($strict as $cand){
    $c=is_array($cand['campaign']??null)?$cand['campaign']:array();
    echo 'CAND='.wp_json_encode(array(
      'pos'=>$i,
      'post_id'=>absint($c['post_id']??0),
      'id'=>(string)($c['id']??''),
      'network'=>(string)($c['network']??''),
      'name'=>(string)($c['name']??''),
      'specificity'=>(int)($cand['specificity']??0),
      'matches'=>(int)($cand['matches']??0),
      'priority'=>(int)($cand['priority']??($c['priority']??0)),
      'gtins'=>array_values((array)($c['product_gtins']??array())),
      'surface'=>method_exists($o,'idealo_campaign_surface_kind') && sanitize_key((string)($c['network']??''))==='idealo' ? fs_call($o,'idealo_campaign_surface_kind',$c) : '',
      'standalone'=>sanitize_key((string)($c['network']??''))==='idealo' ? (fs_call($o,'idealo_standalone_campaign_allowed',$c,$slot)?1:0) : 1,
    ),JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE)."\n";
    $i++; if($i>=12)break;
  }
  $sel=fs_call($o,'select_campaign_for_slot',$cctx,$slot,'');
  $sc=is_array($sel)&&is_array($sel['campaign']??null)?$sel['campaign']:array();
  echo 'SELECT='.$slot.':'.absint($sc['post_id']??0).':'.sanitize_key((string)($sc['network']??''))."\n";
}
