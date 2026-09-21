<?php
if (!defined('ABSPATH')) exit(2);
$o=Pferdeportal_Affiliate_Router::instance();
$m=new ReflectionMethod($o,'category_product_provider_mix_v672133');$m->setAccessible(true);
function cand($id,$provider,$spec,$matches,$priority=89){
  return array('campaign'=>array('id'=>$id,'network'=>$provider,'priority'=>$priority),'specificity'=>$spec,'matches'=>$matches,'priority'=>$priority,'reason'=>'test');
}
function providers($rows){$out=array();foreach($rows as $r){$out[]=sanitize_key((string)($r['campaign']['network']??''));}return $out;}

$two=array(
 cand('e1','ebay',520,3,89),
 cand('e2','ebay',520,3,89),
 cand('e3','ebay',520,3,89),
 cand('i1','idealo',520,3,89)
);
$r=$m->invoke($o,$two,'category_product_1');
echo 'TWO_PROVIDER='.wp_json_encode(providers($r))."\n";
if(array_slice(providers($r),0,3)!==array('ebay','idealo','ebay')){fwrite(STDERR,"FAIL_TWO_PROVIDER\n");exit(10);}

$three=array(
 cand('e1','ebay',520,3,89),
 cand('e2','ebay',520,3,89),
 cand('i1','idealo',520,3,89),
 cand('a1','amazon_future',520,3,89),
 cand('e3','ebay',520,3,89)
);
$r=$m->invoke($o,$three,'category_product_1');
echo 'THREE_PROVIDER='.wp_json_encode(providers($r))."\n";
if(array_slice(providers($r),0,3)!==array('ebay','idealo','amazon_future')){fwrite(STDERR,"FAIL_THREE_PROVIDER\n");exit(11);}

$weaker=array(
 cand('e1','ebay',520,3,89),
 cand('e2','ebay',520,3,89),
 cand('e3','ebay',520,3,89),
 cand('i1','idealo',520,2,99)
);
$r=$m->invoke($o,$weaker,'category_product_1');
echo 'WEAKER_PROVIDER='.wp_json_encode(providers($r))."\n";
if(array_slice(providers($r),0,3)!==array('ebay','ebay','ebay')){fwrite(STDERR,"FAIL_WEAKER_PROVIDER_PROMOTED\n");exit(12);}

$r=$m->invoke($o,$two,'hub_product_1');
echo 'NON_CATEGORY='.wp_json_encode(providers($r))."\n";
if(providers($r)!==providers($two)){fwrite(STDERR,"FAIL_NON_CATEGORY_CHANGED\n");exit(13);}

echo "GENERIC_PROVIDER_MIX_PASS\n";
