#!/usr/bin/env python3
"""Execute the ACTUAL RC30 source PHP functions, not a reimplementation.
Verify single advertisement label and source-backed bullet facts inside all
three actual category-product slots, while preserving controls elsewhere.
"""
from pathlib import Path
from zipfile import ZipFile
from tempfile import TemporaryDirectory
from subprocess import run
import hashlib,re

R=Path("protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ")
P=R/"PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip"
with ZipFile(P) as z:
    assert z.testzip() is None and len(z.namelist())==36
    main=z.read("affiliate-portal-router/affiliate-portal-router.php").decode()
    bridge=z.read("affiliate-portal-router/includes/class-ppar-hab-bewahr-bridge.php").decode()
    css=z.read("affiliate-portal-router/assets/frontend.css").decode()
    assert "Version: 0.1.27-rc30" in main
    assert "ppar-hb-category-product-adlabel" in bridge
    assert "ppar-hb-product-fact::before" in css
    assert "padding-left:13px!important" in css
    assert "font-size:12px!important" in css
    assert "border-radius:1px!important" in css
    assert main.count("The existing HB recommendation grid owns ONE")==1

    def func(s,name):
        m=re.search(r"(?:public|private|protected)(?:\s+static)?\s+function\s+"+re.escape(name)+r"\s*\(",s)
        assert m,name
        i=s.index("{",m.end())
        depth=0
        for j in range(i,len(s)):
            if s[j]=='{':depth+=1
            elif s[j]=='}':
                depth-=1
                if depth==0:return s[m.start():j+1].replace("private static function","public static function",1).replace("private function","public function",1)
        raise AssertionError(name)
    render_banner=func(main,"render_banner")
    render_slot=func(main,"render_affiliate_slot_for_context")
    group=func(bridge,"category_product_grid_markup")
    harness=r'''<?php
function absint($x){return max(0,(int)$x);}
function sanitize_key($x){return strtolower(preg_replace('/[^a-z0-9_-]/','',strtolower((string)$x)));}
function sanitize_html_class($x){return sanitize_key($x);}
function sanitize_text_field($x){return trim(strip_tags((string)$x));}
function esc_html($x){return htmlspecialchars((string)$x, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');}
function esc_attr($x){return esc_html($x);}
function esc_url($x){return esc_html($x);}
function get_option($key,$default=''){return $key==='ppar_disclosure_text' ? 'Anzeige' : $default;}
function ok($v,$message){if(!$v){fwrite(STDERR,"FAIL: ".$message."\n");exit(1);}echo "PASS: ".$message."\n";}
class PPAR_HB_Integration {
   GROUP
}
class TestedActualRouter {
  public $offer=array();
  public function is_enabled(){return true;}
  public function hb_insurance_scope($ctx){return 'other';}
  public function hb_insurance_campaign_allowed($campaign,$context){return true;}
  public function assignment_selection_for_slot($context,$slot){return array('handled'=>false);}
  public function select_campaign_for_slot($context,$slot,$forced=''){return array('campaign'=>$this->offer);}
  public function campaign_to_group_banner($campaign){return array(array('id'=>'real-idealo'),$campaign);}
  public function get_disclosure_html($content_id){return '<div class="ppar-affiliate-disclosure">Anzeige</div>';}
  public function debug_comment(){return '';}
  public function build_subid(){return 'test';}
  public function apply_subid_to_url($url){return $url;}
  public function overview_wide_banner_slot($slot){return false;}
  public function category_large_banner_slot($slot){return false;}
  public function multiprovider_matching_offers_for_banner(){return array();}
  public function render_placeholder_slot($slot){return '';}
  BANNER
  SLOT
}
$router=new TestedActualRouter();
$router->offer=array(
 'creative_type'=>'product', 'network'=>'idealo', 'mode'=>'image_link',
 'url'=>'https://www.idealo.de/preisvergleich/Test',
 'image_url'=>'https://cdn.idealo.com/example.jpg',
 'title'=>'ABUS Türschloss Schließzylinder A93 NG 30/45 (86176)',
 'description'=>'Marke: ABUS · Maße: 30/45 · Art.-Nr.: 86176',
 'button_text'=>'Bei idealo vergleichen',
 'availability'=>'Verfügbar',
);
$ctx=array('primary_slug'=>'c22-haustuerschloesser-dd9773fd40',
 'primary_name'=>'Haustürschlösser','post_type'=>'category_archive');
$parts='';
foreach(array(1,2,3) as $i){
 $parts.=$router->render_affiliate_slot_for_context('term_123',$ctx,"category_product_$i",'primary_product');
}
$out=PPAR_HB_Integration::category_product_grid_markup($parts);
ok(substr_count($out,'ppar-hb-category-product-adlabel')===1,'One outer recommendation label');
ok(substr_count($out,'>Anzeige<')===1,'EXACTLY ONE visible Anzeige; none per card');
ok(strpos($out,'ppar-affiliate-disclosure')===false,'No duplicate card disclosure or reserved blank row');
ok(substr_count($out,'class="ppar-hb-product-fact"')===9,'Three real source facts per card in each of 3 cards');
ok(substr_count($out,'ppar-hb-product-facts')===3,'Each idealo card has its own compact facts list');
ok(strpos($out,'Marke: ABUS')!==false && strpos($out,'Maße: 30/45')!==false && strpos($out,'Art.-Nr.: 86176')!==false,
   'Exact original genuine brand, dimensions and model used with no invented data');
ok(strpos($out,'https://cdn.idealo.com/example.jpg')!==false,'Real product photo URL preserved');
ok(substr_count($out,'Bei idealo vergleichen')===3,'Each real original provider CTA remains');
ok(substr_count($out,'ppar-banner-availability')===3,'Existing availability remains');
$router->offer['description']='Marke: VisorTech · Art.-Nr.: NX4349';
$two=$router->render_affiliate_slot_for_context('term_123',$ctx,'category_product_1','primary_product');
ok(substr_count($two,'class="ppar-hb-product-fact"')===2,'Only two available facts yields two bullet lines, never fabricate third');
$router->offer['network']='manual';
$manual=$router->render_affiliate_slot_for_context('term_123',$ctx,'category_product_1','primary_product');
ok(strpos($manual,'ppar-hb-product-facts')===false && strpos($manual,'Marke: VisorTech · Art.-Nr.: NX4349')!==false,
   'Only idealo product descriptions restructured; other partner markup unchanged');
$router->offer['network']='idealo';
$router->offer['creative_type']='banner';
$banner=$router->render_affiliate_slot_for_context('term_123',$ctx,'product_after_category_tiles','primary_product');
ok(substr_count($banner,'>Anzeige<')>=1,'Other banner advertisements still marked; do not change legal label outside grid');
$router->offer['creative_type']='product';
$router->offer['description']='Marke: <script>alert(1)</script> · Maße: 30/45';
$secure=$router->render_affiliate_slot_for_context('term_123',$ctx,'category_product_1','primary_product');
ok(strpos($secure,'<script>')===false && strpos($secure,'&lt;script&gt;')!==false,
   'Vendor-provided product facts HTML-escaped; no injections');
echo "HAB_RC30_REAL_PHP_SINGLE_LABEL_AND_FACTS_QA_PASS\n";
'''
    harness=harness.replace("GROUP",group).replace("BANNER",render_banner).replace("SLOT",render_slot)
    with TemporaryDirectory() as d:
        php_names=[n for n in z.namelist() if n.endswith(".php")]
        assert len(php_names)==25
        for k,n in enumerate(php_names):
            p=Path(d)/(str(k)+".php")
            p.write_bytes(z.read(n))
            r=run(["php","-l",str(p)],capture_output=True,text=True)
            assert r.returncode==0,(n,r.stdout,r.stderr)
        f=Path(d)/"qa.php";f.write_text(harness)
        r=run(["php","-l",str(f)],capture_output=True,text=True)
        assert r.returncode==0,(r.stdout,r.stderr)
        r=run(["php",str(f)],capture_output=True,text=True)
        print(r.stdout)
        assert r.returncode==0,(r.stdout,r.stderr)
    print("HAB_RC30_25_PHP_LINT_PASS",hashlib.sha256(P.read_bytes()).hexdigest())
print("HAB_RC30_QA_PASS")
