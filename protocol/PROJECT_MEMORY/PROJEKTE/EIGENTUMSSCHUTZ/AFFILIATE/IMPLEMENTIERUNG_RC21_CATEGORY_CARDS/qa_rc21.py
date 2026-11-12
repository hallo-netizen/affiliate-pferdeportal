#!/usr/bin/env python3
"""Read-only end-to-end PHP simulation: verified WP category -> existing Design
hook -> existing Hab affiliate bridge -> exactly 3 compact product slots.
Also check source-scope constraints and original multi-provider code retention.
"""
import re,subprocess,tempfile,hashlib
from pathlib import Path
from zipfile import ZipFile
root=Path("protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ/PLUGINS/ISOLIERTE_PLUGINS")
with ZipFile(root/"HAB-004-AFFILIATE/CURRENT.zip") as z, ZipFile(root/"HAB-001-DESIGN/CURRENT.zip") as dz:
 assert z.testzip() is None and len(z.namelist())==36
 assert dz.testzip() is None and len(dz.namelist())==432
 php_files=[n for n in z.namelist() if n.endswith(".php")]
 assert len(php_files)==25,("wrong PHP count",len(php_files))
 with tempfile.TemporaryDirectory() as td:
    for i,name in enumerate(php_files):
        file=Path(td)/f"src{i}.php"
        file.write_bytes(z.read(name))
        lint=subprocess.run(["php","-l",str(file)],capture_output=True,text=True)
        assert lint.returncode==0,(name,lint.stdout,lint.stderr)
 bridge=z.read("affiliate-portal-router/includes/class-ppar-hab-bewahr-bridge.php").decode()
 router=z.read("affiliate-portal-router/affiliate-portal-router.php").decode()
 idealo=z.read("affiliate-portal-router/includes/trait-ppar-idealo.php").decode()
 css=z.read("affiliate-portal-router/assets/frontend.css").decode()
 design=dz.read("hab-bewahr-design-vorschau/includes/area-design-prototype.php").decode()
 assert "Version: 0.1.18-rc21" in router
 assert "ppar-hb-category-products-grid" in bridge and css
 assert "grid-template-columns:repeat(3,minmax(0,1fr))" in css
 assert "grid-template-columns:repeat(2,minmax(0,1fr))" in css
 assert "grid-template-columns:minmax(0,1fr)" in css
 assert "min-height:416px!important" not in router
 assert "grid-template-rows:150px minmax(210px,1fr)!important" not in router
 assert "multiprovider_matching_offers_for_banner" in router
 assert "multiprovider_render_offer_buttons($offers, 'banner')" in router
 assert "multiprovider_campaigns_share_exact_gtin" in idealo
 assert "multiprovider_offer_label" in idealo
 assert "Preisvergleich" in idealo and "Amazon" in idealo
 assert "hb_insurance_scope" in router
 assert "hb_amazon_category_search_fallback" in router
 assert "hab_bw_article_slot" in router
 assert "function hbdp_area_product_markup" in design
 def fn(src,name):
    m=re.search(r"(?:private|public)?\s*(?:static\s+)?function\s+"+re.escape(name)+r"\s*\(",src)
    assert m,name
    op=src.find("{",m.end())
    level=0
    for i in range(op,len(src)):
        if src[i]=="{":level+=1
        if src[i]=="}":
            level-=1
            if level==0:return src[m.start():i+1].replace("private static function","public static function",1).replace("private function","public function",1)
    raise ValueError(name)
 methods="\n".join(fn(bridge,n) for n in ("category_product_grid_markup","area","area_products","area_banner","world_banner"))
 design_method=fn(design,"hbdp_area_product_markup")
 harness=r'''<?php
function absint($n){return max(0,(int)$n);}
function get_post_status($id){return "publish";}
function apply_filters($tag,$value,$node){return PPAR_HB_Integration::area_products($value,$node);}
function wp_kses_post($s){return $s;}
class Portal_Affiliate_Router {
 public static $empty=false;
 public static function instance(){return new self();}
 public function provide_leaf_category_affiliate_slot_html($h,$id,$slot){
   if (self::$empty) return "";
   if ($slot==="product_after_category_tiles") return "<div class='existing-ad'>BANNER</div>";
   return '<div class="ppar-affiliate-slot" data-ppar-slot="'.$slot.'"><div class="ppar-affiliate-label">Anzeige</div><div class="ppar-affiliate-content"><a href="https://www.amazon.de/dp/B000000001">Schließzylinder '.htmlspecialchars($slot).'</a></div></div>';
 }
 public function hab_bw_area_slot($id,$kind,$node){
   if ($kind==="banner") return "<div>EXISTING BANNER</div>";
   if (self::$empty) return "";
   return '<div class="ppar-affiliate-slot" data-ppar-slot="category_product_1"><a href="https://www.amazon.de/dp/B000000001">Schloss</a></div>';
 }
}
class PPAR_HB_Integration {
 public static function verified_nodes(){
   return array(
    "leaf"=>array("id"=>"leaf","wp_id"=>120,"type"=>"category","pillar"=>"core"),
    "area"=>array("id"=>"core:c22:area:test","wp_id"=>220,"type"=>"page","pillar"=>"core"),
    "world"=>array("id"=>"core:world:einbruch","wp_id"=>320,"type"=>"page","pillar"=>"core"),
    "editorial"=>array("id"=>"editorial:test","wp_id"=>420,"type"=>"page","pillar"=>"editorial"),
    "insurance"=>array("id"=>"ins:leaf","wp_id"=>520,"type"=>"category","pillar"=>"core")
   );
 }
 METHODS
}
DESIGN_METHOD
function check($condition,$message){if(!$condition){fwrite(STDERR,"FAIL ".$message.PHP_EOL);exit(2);}}
$leaf=PPAR_HB_Integration::area_products("","leaf");
check(substr_count($leaf,'data-ppar-slot="category_product_')===3,'three real product slots');
check(substr_count($leaf,'ppar-hb-category-products-grid')===1,'single group');
check(substr_count($leaf,'ppar-hb-category-product-adlabel')===1,'one group ad label');
check(strpos($leaf,'Schließzylinder category_product_1')!==false,'real product name retained');
check(strpos($leaf,'https://www.amazon.de/dp/')!==false,'original provider URL retained');
$from_design=hbdp_area_product_markup(array('id'=>'leaf'));
check($from_design===$leaf,'Design filter path');
$page=PPAR_HB_Integration::area_products("","core:c22:area:test");
check(strpos($page,'ppar-hb-category-products-grid')!==false,'R3/R2 page categories grouped');
$world=PPAR_HB_Integration::area_products("","core:world:einbruch");
check(strpos($world,'ppar-hb-category-products-grid')===false,'world hub unchanged');
$editorial=PPAR_HB_Integration::area_products("","editorial:test");
check(strpos($editorial,'ppar-hb-category-products-grid')===false,'editorial page unchanged');
$banner=PPAR_HB_Integration::area_banner("","leaf");
check($banner==="<div class='existing-ad'>BANNER</div>",'banner untouched');
$booked=PPAR_HB_Integration::area_products("<div>EXISTING BOOKING</div>","leaf");
check($booked==="<div>EXISTING BOOKING</div>",'booked markup priority');
Portal_Affiliate_Router::$empty=true;
$empty=PPAR_HB_Integration::area_products("","leaf");
check($empty==='','empty does not create fake card');
echo "HAB_RC21_CATEGORY_DESIGN_QA_PASS 11 independent cases, 3/2/1 responsive, 25 PHP LINT, 36 ZIP CRC, 432 DESIGN CRC\n";
'''
 harness=harness.replace("METHODS",methods).replace("DESIGN_METHOD",design_method)
 with tempfile.TemporaryDirectory() as td:
   path=Path(td)/"qa.php";path.write_text(harness)
   lint=subprocess.run(["php","-l",str(path)],capture_output=True,text=True)
   assert lint.returncode==0,lint.stdout+lint.stderr
   res=subprocess.run(["php",str(path)],capture_output=True,text=True)
   assert res.returncode==0,res.stdout+res.stderr
   print(res.stdout.strip())
 print("HAB_RC21_RELEASE_SHA256",hashlib.sha256((root/"HAB-004-AFFILIATE/CURRENT.zip").read_bytes()).hexdigest())
