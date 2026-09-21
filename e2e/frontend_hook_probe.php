<?php
if (!defined('ABSPATH')) { fwrite(STDERR,"NO_WP\n"); exit(2); }
if (!class_exists('Pferdeportal_Affiliate_Router')) { fwrite(STDERR,"NO_ROUTER\n"); exit(3); }
$targets=array(
 'reithelme'=>186,
 'reithandschuhe'=>187,
 'reitstiefel'=>188,
 'sicherheitswesten'=>189,
 'gerten'=>190,
 'sporen'=>191,
 'halfter-und-stricke-stallhalfter'=>174,
);
$fail=array();$all=array();
foreach($targets as $slug=>$page_id){
  $slots=array();
  foreach(array('category_product_1','category_product_2','category_product_3') as $slot){
    $html=apply_filters('pftk_leaf_page_affiliate_slot_html','',$page_id,$slot,array('contract'=>'1.0'));
    $provider='none';$low=strtolower((string)$html);
    if(strpos($low,'ebay.de')!==false||strpos($low,'rover.ebay')!==false)$provider='ebay';
    elseif(strpos($low,'idealo.de')!==false||strpos($low,'ipn.idealo')!==false)$provider='idealo';
    $real=is_string($html)&&$html!==''&&strpos($html,'data-ppar-category-product-card="1"')!==false;
    preg_match('/<strong class="ppar-banner-title">([^<]+)<\/strong>/s',(string)$html,$m);
    $title=isset($m[1])?html_entity_decode(trim($m[1]),ENT_QUOTES|ENT_HTML5,'UTF-8'):'';
    $slots[]=array('slot'=>$slot,'real'=>$real,'provider'=>$provider,'title'=>$title,'sha256'=>hash('sha256',(string)$html));
    if(!$real)$fail[]=$slug.':'.$slot.':NOT_REAL';
  }
  $all[$slug]=$slots;
}
foreach($all as $slug=>$slots){
  $providers=array_values(array_unique(array_column($slots,'provider')));
  if(count($slots)!==3)$fail[]=$slug.':COUNT';
  if(count(array_unique(array_column($slots,'sha256')))!==3)$fail[]=$slug.':NOT_DISTINCT_HTML';
}
foreach(array('reithelme','halfter-und-stricke-stallhalfter') as $slug){
  $providers=array_column($all[$slug],'provider');
  if(!in_array('ebay',$providers,true)||!in_array('idealo',$providers,true))$fail[]=$slug.':PROVIDER_MIX';
}
echo 'FRONTEND_HOOK_RESULT='.wp_json_encode($all,JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE)."\n";
if($fail){foreach($fail as $f)fwrite(STDERR,'FRONTEND_HOOK_FAIL_'.$f."\n");exit(1);}
echo "FRONTEND_HOOK_FULL_PASS\n";
