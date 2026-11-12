#!/usr/bin/env python3
"""Real existing Hab PHP multi-provider builder + Amazon ASIN verifier.
Tests source-backed idealo photograph metadata plus authentic 3-provider HTML
with exact-GTIN controls. Synthetic data, never claimed as public real result.
"""
from zipfile import ZipFile
from pathlib import Path
from tempfile import TemporaryDirectory
from subprocess import run
import re
root=Path("protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ")
p=root/"PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip"
with ZipFile(p) as z:
 a=z.read("affiliate-portal-router/includes/trait-ppar-hb-amazon.php").decode()
 i=z.read("affiliate-portal-router/includes/trait-ppar-idealo.php").decode()
 def extract(src,name):
    hit=re.search(r"(?:private|public) function "+re.escape(name)+r"\s*\(",src)
    assert hit,name
    b=src.find("{",hit.end()); d=0
    for k in range(b,len(src)):
      if src[k]=="{":d+=1
      elif src[k]=="}":
        d-=1
        if d==0:return src[hit.start():k+1].replace("private function","public function",1)
    raise ValueError(name)
 methods="\n".join([
   extract(a,"hb_amazon_direct_url"),
   extract(a,"hb_amazon_campaign_verified_asin"),
   extract(a,"hb_amazon_add_offer"),
   extract(i,"multiprovider_matching_offers_for_banner"),
   extract(i,"multiprovider_render_offer_buttons"),
 ])
 payload=r'''<?php
function absint($x){return max(0,(int)$x);}
function sanitize_key($x){return preg_replace('/[^a-z0-9_\-]/','',strtolower((string)$x));}
function esc_url($s){return htmlspecialchars((string)$s,ENT_QUOTES);}
function esc_attr($s){return htmlspecialchars((string)$s,ENT_QUOTES);}
function esc_html($s){return htmlspecialchars((string)$s,ENT_QUOTES);}
function get_post($id){return (object)array('ID'=>$id);}
function expect($yes,$text){if(!$yes){fwrite(STDERR,"FAIL ".$text.PHP_EOL);exit(3);} echo "PASS ".$text.PHP_EOL;}
class HabProductCard {
  public $real;
  public $extras=array();
  METHODS
  public function hb_amazon_settings(){return array('enabled'=>true);}
  public function hb_amazon_ready($settings=null){return true;}
  public function hb_amazon_tag($settings=null){return 'test-hab-21';}
  public function campaign_from_post($post){return $this->real;}
  public function idealo_output_mode(){return 'automatic';}
  public function idealo_link_strategy(){return 'hybrid';}
  public function multiprovider_runtime_tracking_url($u,$network=''){return $u;}
  public function multiprovider_campaign_gtins($campaign){return $campaign['product_gtins']??array();}
  public function multiprovider_exact_gtin_candidate_pool($gtins,$context,$slot){return $this->extras;}
  public function campaign_is_complete($campaign){return true;}
  public function campaign_program_allows_delivery($c){return true;}
  public function campaign_source_allows_delivery($c){return true;}
  public function campaign_slot_allowed($c,$slot){return true;}
  public function multiprovider_campaigns_share_exact_gtin($x,$y){return count(array_intersect($x['product_gtins']??array(),$y['product_gtins']??array()))>0;}
  public function campaign_match_rank($campaign,$context){return true;}
  public function campaign_control_allows_delivery($campaign,$slot){return true;}
  public function campaign_health_allows_delivery($c){return true;}
  public function multiprovider_offer_label($n){return 'Bei '.ucfirst($n).' ansehen';}
}
$t=new HabProductCard();
$t->real=array(
 'post_id'=>101,'network'=>'idealo','source'=>'idealo_product_feed_v1','active'=>true,'creative_type'=>'product',
 'title'=>'ABUS Schließzylinder 30/30','product_identity_source'=>'gtin',
 'product_gtins'=>array('4001234567890'),'product_asins'=>array('B000TEST10'),
 'image_url'=>'https://cdn.idealo.com/test-verified-image.png',
 'url'=>'https://ipn.idealo.de/ts/test?id=1'
);
$ebay=array('post_id'=>102,'network'=>'ebay','source'=>'ebay_business','active'=>true,'creative_type'=>'product',
 'product_gtins'=>array('4001234567890'),'url'=>'https://www.ebay.de/itm/1234567890');
$t->extras=array($ebay);
$banner=array('campaign_post_id'=>101,'url'=>$t->real['url'],'network'=>'idealo','image_url'=>$t->real['image_url']);
$offers=$t->multiprovider_matching_offers_for_banner($banner,array('post_id'=>0),'category_product_1');
$keys=array_column($offers,'network');
expect($keys===array('ebay','idealo','amazon'),'same exact GTIN: eBay, idealo, Amazon are three provider buttons');
$html=$t->multiprovider_render_offer_buttons($offers,'banner');
expect(substr_count($html,'class="ppar-banner-offer-button"')===3,'real original renderer emits three clickable merchant buttons');
expect(strpos($html,'amazon.de/dp/B000TEST10?tag=test-hab-21')!==false,'Amazon button from exactly verified feed ASIN, no fake product photo');
expect($t->real['image_url']==='https://cdn.idealo.com/test-verified-image.png','real provider picture field is retained as card identity, Amazon is only CTA');
$t->extras=array(array_merge($ebay,array('product_gtins'=>array('4001234567899'))));
$offers=$t->multiprovider_matching_offers_for_banner($banner,array('post_id'=>0),'category_product_1');
expect(array_column($offers,'network')===array('idealo','amazon'),'nonmatching eBay GTIN never shares a product');
$t->real['product_asins']=array();
$t->extras=array();
$offers=$t->multiprovider_matching_offers_for_banner($banner,array('post_id'=>0),'category_product_1');
expect(array_column($offers,'network')===array('idealo'),'without verified ASIN no invented Amazon button');
echo 'HAB_REAL_METHOD_MULTIPROVIDER_QA_PASS: 6 functional tests, source-backed image/GTIN/ASIN'.PHP_EOL;
'''.replace("METHODS",methods)
 with TemporaryDirectory() as td:
   f=Path(td)/"qa.php";f.write_text(payload)
   lint=run(["php","-l",str(f)],capture_output=True,text=True)
   assert lint.returncode==0,lint.stdout+lint.stderr
   out=run(["php",str(f)],capture_output=True,text=True)
   assert out.returncode==0,out.stdout+out.stderr
   print(out.stdout)
