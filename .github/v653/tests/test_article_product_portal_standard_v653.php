<?php
error_reporting(E_ALL);
define('ABSPATH','/tmp/');
function sanitize_key($v){return preg_replace('/[^a-z0-9_\-]/','',strtolower((string)$v));}
function sanitize_text_field($v){return trim(strip_tags((string)$v));}
function esc_url($v){return htmlspecialchars((string)$v,ENT_QUOTES,'UTF-8');}
function esc_attr($v){return htmlspecialchars((string)$v,ENT_QUOTES,'UTF-8');}
function esc_html($v){return htmlspecialchars((string)$v,ENT_QUOTES,'UTF-8');}
$root=getenv('PPAR_TEST_PLUGIN_DIR'); if(!$root){fwrite(STDERR,"missing PPAR_TEST_PLUGIN_DIR\n"); exit(2);} require $root.'/includes/trait-ppar-article-plans.php';
class ProductCardHarness {
    use PPAR_Article_Plans_Trait;
    private function build_subid($post_id,$context,$group,$slot){return 'sub-'.(int)$post_id;}
    private function apply_subid_to_url($url,$subid,$param){return $url;}
    public function renderCard($banner){
        return $this->article_plan_render_product_card_markup($banner,42,['primary_slug'=>'hafer','primary_name'=>'Hafer'],['id'=>'ebay'],'post_bottom_products');
    }
}
$f=0;$n=0;function ck($v,$m){global$f,$n;$n++;echo ($v?'PASS ':'FAIL ').$m."\n";if(!$v)$f++;}
$h=new ProductCardHarness();
$html=$h->renderCard([
  'mode'=>'image_link','url'=>'https://example.invalid/product','image_url'=>'https://example.invalid/p.jpg',
  'title'=>'Hafer für Pferde','description'=>'Kurze Produktbeschreibung','price'=>'20.99','currency'=>'EUR','availability'=>'available','button_text'=>'Mehr erfahren','target'=>'_blank'
]);
ck(strpos($html,'class="ppar-article-product-link"')!==false,'dedicated product link markup exists');
ck(strpos($html,'class="ppar-article-product-media"')!==false,'dedicated product media markup exists');
ck(strpos($html,'class="ppar-article-product-image"')!==false,'dedicated product image markup exists');
ck(strpos($html,'class="ppar-article-product-body"')!==false,'dedicated product body markup exists');
ck(strpos($html,'class="ppar-article-product-title"')!==false,'dedicated product title markup exists');
ck(strpos($html,'class="ppar-article-product-description"')!==false,'dedicated product description markup exists');
ck(strpos($html,'class="ppar-article-product-meta"')!==false,'dedicated product meta markup exists');
ck(strpos($html,'class="ppar-article-product-price"')!==false,'dedicated product price markup exists');
ck(strpos($html,'class="ppar-article-product-availability">Verfügbar')!==false,'provider availability is localized');
ck(strpos($html,'class="ppar-article-product-cta"')!==false,'dedicated product CTA markup exists');
ck(strpos($html,'ppar-banner-')===false,'generic banner markup is absent from article product card');
ck(strpos($html,'sponsored nofollow noopener noreferrer')!==false,'affiliate rel contract preserved');
$empty=$h->renderCard(['mode'=>'image_link','url'=>'','title'=>'x']);
ck($empty==='','missing URL fails closed');
$html2=$h->renderCard(['mode'=>'html','url'=>'https://example.invalid','title'=>'x']);
ck($html2==='','raw HTML creative is not embedded into product card contract');
echo "ASSERTIONS=$n FAIL=$f\n";exit($f?1:0);
