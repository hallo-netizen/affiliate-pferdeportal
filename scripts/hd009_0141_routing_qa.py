#!/usr/bin/env python3
"""Execute exact original campaign_match_rank from final HD009 ZIP.

Confirm one placement resolver: exactly stored product-page target; related
non-topic article products never spill into a generic auto-verified fallback.
Historical eBay article fallback remains unchanged.
"""
from pathlib import Path
from zipfile import ZipFile
import re,sys
source=Path(sys.argv[1]);dest=Path(sys.argv[2])
with ZipFile(source) as z:
    main=z.read('affiliate-portal-router/hobby-depot-affiliate-router.php').decode('utf-8')
assert 'hd_idealo_product_targets_exact_hobby_page' not in main, "late parallel target checker still exists"
match=re.search(r'^    private function campaign_match_rank\(',main,re.M)
assert match,'Exact original placement method not found'
rest=main[match.end():]
next_method=re.search(r'^    (?:private|public|protected) function ',rest,re.M)
method=main[match.start():match.end()+next_method.start()] if next_method else main[match.start():]
assert method.count("Gespeichertes genaues Idealo-Hobbyziel.")==1
assert "$verified_ebay || $verified_idealo" not in method
php=r'''<?php
error_reporting(E_ALL);ini_set('display_errors','1');
function sanitize_key($x){return preg_replace('/[^a-z0-9_\-]/','',strtolower((string)$x));}
function sanitize_title($x){return strtolower(preg_replace('/[^a-z0-9\-]/','',(string)$x));}
function sanitize_text_field($x){return strip_tags((string)$x);}
class RealOriginalProductRankQA {
  private function slot_required_creative_type($slot){return in_array($slot,array('category_product_1','category_product_2','category_product_3','post_bottom_products'),true)?'product':'banner';}
  private function automation_campaign_exact_target_rank($c,$x){return null;}
  private function banner_destination_semantic_rank($c,$x){return null;}
  private function banner_runtime_page_topic_rank($c,$x){return null;}
  private function glossary_campaign_runtime_semantic_rank($c,$x){return null;}
  private function glossary_partner_inherited_exact_rank($c,$x){return null;}
  private function category_large_banner_slot($x){return false;}
__METHOD__
  function test($c,$x){return $this->campaign_match_rank($c,$x);}
}
function ck($pass,$what){static $n=0;$n++;if(!$pass){fwrite(STDERR,"FAIL $n: $what\n");exit(1);}echo "PASS $n: $what\n";}
$w=new RealOriginalProductRankQA();
$prod=array(
 'network'=>'idealo','source'=>'idealo_product_feed_v1',
 'assignment_mode'=>'page_tree','quality_manual_status'=>'auto_verified',
 'product_identity_source'=>'gtin','product_gtins'=>array('4006381333931'),
 'automation_target_keys'=>array('page:airbrush','page:malen-zeichnen'),
 'match_descendants'=>false,'placements'=>array('category_product_1','post_bottom_products')
);
$ctx=array('post_type'=>'page','slot_type'=>'category_product_1','primary_slug'=>'airbrush','slugs'=>array('airbrush'),'post_id'=>11);
$r=$w->test($prod,$ctx);
ck(is_array($r)&&$r['specificity']===500,'Direct Airbrush product matched exactly once at one placement resolver');
$ctx['primary_slug']='modellbau';$ctx['slugs']=array('modellbau');
ck($w->test($prod,$ctx)===null,'Unrelated hobby page must not inherit Idealo product via broad parent keys');
$ctx['primary_slug']='malen-zeichnen';$ctx['slugs']=array('malen-zeichnen');
$r=$w->test($prod,$ctx);
ck(is_array($r)&&$r['specificity']===500,'Intentionally stored related parent page remains allowed by the same resolver');
$ctx['primary_slug']='airbrush';$ctx['slot_type']='category_product_3';
$r=$w->test($prod,$ctx);
ck(is_array($r)&&$r['specificity']===500,'Third card slot uses exactly the same single decision');

$ctx=array('post_type'=>'post','slot_type'=>'post_bottom_products','post_id'=>100,'slugs'=>array(),'term_ids'=>array(),'haystack'=>'');
$unrelated=$prod;$unrelated['automation_target_keys']=array('page:airbrush');
ck($w->test($unrelated,$ctx)===null,'Idealo product cannot appear on wholly unrelated article via generic fallback');
$ebay=$unrelated;$ebay['network']='ebay';$ebay['source']='output_object_v4';
$r=$w->test($ebay,$ctx);
ck(is_array($r)&&$r['specificity']===200,'Original eBay verified article fallback unchanged');
echo "SINGLE_PRODUCT_TARGET_RANK_AND_NO_RECHECK_TESTS_PASS\n";
'''.replace('__METHOD__',method)
dest.parent.mkdir(exist_ok=True,parents=True);dest.write_text(php)
print('ORIGINAL_PLACEMENT_METHOD_BYTES',len(method))
