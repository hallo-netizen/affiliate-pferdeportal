#!/usr/bin/env python3
"""Generate PHP integration tests from *literal* complete HD003 1.50.814 methods."""
from pathlib import Path
from zipfile import ZipFile
import re,sys
source=Path(sys.argv[1])
dest=Path(sys.argv[2])
with ZipFile(source) as z:
    text=z.read('affiliate-portal-template-kit/includes/class-hobby-depot-profile-v150709.php').decode('utf8')
pattern=re.compile(r'^\s*(?:private|public|protected)\s+static\s+function\s+[A-Za-z_][A-Za-z_0-9]*\s*\(',re.M)
def method(name):
    m=re.search(r'^\s*(?:private|public|protected)\s+static\s+function\s+'+re.escape(name)+r'\s*\(',text,re.M)
    assert m,name
    e=pattern.search(text,m.end())
    return text[m.start():e.start()] if e else text[m.start():]
methods=[
 'is_real_affiliate','affiliate_slot',
 'logged_in_preview','affiliate_preview_placeholder',
 'integrated_affiliate_components',
 'inline_partner_product','render_category_level_product_row_v150687',
 'render_leaf_category_products_v150750','render_products'
]
functions='\n'.join(method(n) for n in methods)
php=r'''<?php
error_reporting(E_ALL);
ini_set('display_errors','1');
function is_user_logged_in(){return $GLOBALS['signed_in'];}
function shortcode_exists($shortcode){return $shortcode==='pp_affiliate_slot';}
function do_shortcode($shortcode){
    preg_match('/\btype="([^"]+)"/',(string)$shortcode,$m);
    return $GLOBALS['cards'][$m[1]??'']??'';
}
function esc_attr($s){return htmlspecialchars((string)$s,ENT_QUOTES);}
function esc_html($s){return htmlspecialchars((string)$s,ENT_QUOTES);}
function esc_url($s){return htmlspecialchars((string)$s,ENT_QUOTES);}
function sanitize_title($s){return strtolower(preg_replace('/[^a-zA-Z0-9\-]+/','-',(string)$s));}
function wp_strip_all_tags($s){return strip_tags((string)$s);}
function is_wp_error($e){return false;}
class MockHD003 {
__METHODS__
    public static function row($products){return self::render_category_level_product_row_v150687(array('products'=>$products));}
    public static function products($type){return self::integrated_affiliate_components($type,'Airbrush');}
    public static function homepage(){return self::render_products();}
    public static function leaf($parts){return self::render_leaf_category_products_v150750($parts);}
}
function check($condition,$note){static $i=0;$i++;if(!$condition){fwrite(STDERR,"FAIL $i $note\n");exit(1);}echo "PASS $i $note\n";}
function stubProduct($id){
   return '<div class="ppar-affiliate-slot"><article class="ppar-affiliate-content" data-real-card="'.$id.'"><a href="https://example.com/product/'.$id.'"><img src="https://example.com/real-'.$id.'.jpg" alt="Echtes Produkt"><b>Airbrushpistole '.$id.'</b></a></article></div>';
}
foreach(array(true,false) as $logged){
   $GLOBALS['signed_in']=$logged;
   $GLOBALS['cards']=array();
   $parts=MockHD003::products('category');
   check(count($parts['products'])===0,'Empty CATEGORY has zero products, visitor/admin='.($logged?'admin':'public'));
   $row=MockHD003::row($parts['products']);
   check($row==='','Empty CATEGORY renders no Empfehlungen section, admin/public');
   check(MockHD003::leaf($parts)==='','Empty LEAF renders no supplier columns, admin/public');
   check(MockHD003::homepage()==='','Empty HOME product feed is hidden, admin/public');
   $GLOBALS['cards']=array('category_product_2'=>stubProduct(2));
   $parts=MockHD003::products('category');
   check(count($parts['products'])===1,'Exactly one real product in CATEGORY');
   $row=MockHD003::row($parts['products']);
   check(substr_count($row,'hd-next-partner-product')===1,'One exact real full card, never three');
   check(strpos($row,'real-card="2"')!==false,'Real shortcoded product HTML unmodified');
   check(strpos($row,'hd-affiliate-preview')===false,'No fake preview in one card');
   check(strpos($row,'<span>Anzeige</span>')!==false,'Exactly one section Advertisement label');
   check(strpos(MockHD003::leaf($parts),'data-provider="ebay"')!==false,'Leaf retains original 1-provider column');
   $GLOBALS['cards']=array('category_product_1'=>stubProduct(1),
          'category_product_2'=>stubProduct(2),'category_product_3'=>stubProduct(3));
   $parts=MockHD003::products('category');
   check(count($parts['products'])===3,'Three real products preserved');
   $row=MockHD003::row($parts['products']);
   check(substr_count($row,'hd-next-partner-product')===3,'Three real categories = three cards');
   check(substr_count($row,'data-real-card=')===3,'Every original card preserved');
   check(substr_count($row,'<span>Anzeige</span>')===1,'One disclosure for three cards');
   check(strpos($row,'Platz aktuell nicht belegt')===false,'No placeholders in 3-product grid');
   $GLOBALS['cards']=array('hub_product_1'=>stubProduct(4));
   $html=MockHD003::homepage();
   check(substr_count($html,'data-real-card=')===1,'Home retains one true card');
   check(strpos($html,'hd-affiliate-preview')===false,'Homepage has no product admin placeholder');
   $GLOBALS['cards']=array('category_product_1'=>'<div class="hd-affiliate-preview">placeholder</div>');
   $parts=MockHD003::products('category');
   check(count($parts['products'])===0,'Missing or preview response excluded by original affiliate parser');
}
echo "HD003_REAL_METHODS_ADMIN_PUBLIC_ZERO_ONE_THREE_QA_PASS\n";
'''.replace('__METHODS__',functions)
dest.parent.mkdir(parents=True,exist_ok=True)
dest.write_text(php)
print('EXTRACTED_METHODS',methods)
print('REAL_PHP_QA_SIZE',len(php))
