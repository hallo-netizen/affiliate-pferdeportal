<?php
if (!class_exists('Pferdeportal_Affiliate_Router')) { fwrite(STDERR,"FAIL plugin class not loaded\n"); exit(1); }
function v653_assert($cond,$msg){ if(!$cond){fwrite(STDERR,"FAIL $msg\n");exit(1);} echo "PASS $msg\n"; }
$p=Pferdeportal_Affiliate_Router::instance();
$m=new ReflectionMethod($p,'article_plan_render_product_card_markup');$m->setAccessible(true);
$banner=array(
 'mode'=>'image_link','url'=>'https://example.invalid/product','image_url'=>'https://example.invalid/p.jpg',
 'title'=>'Hafer für Pferde','description'=>'Kurze Produktbeschreibung','price'=>'20.99','currency'=>'EUR','availability'=>'available','button_text'=>'Mehr erfahren','target'=>'_blank'
);
$html=$m->invoke($p,$banner,1,array('primary_slug'=>'hafer','primary_name'=>'Hafer'),array('id'=>'ebay'),'post_bottom_products');
v653_assert(strpos($html,'ppar-article-product-link')!==false,'real WordPress renders dedicated product link');
v653_assert(strpos($html,'ppar-article-product-media')!==false,'real WordPress renders dedicated product media');
v653_assert(strpos($html,'ppar-article-product-body')!==false,'real WordPress renders dedicated product body');
v653_assert(strpos($html,'ppar-article-product-cta')!==false,'real WordPress renders dedicated product CTA');
v653_assert(strpos($html,'ppar-banner-')===false,'real WordPress product card is decoupled from generic banner markup');
v653_assert(strpos($html,'Verfügbar')!==false,'real WordPress localizes availability label');
v653_assert(Pferdeportal_Affiliate_Router::VERSION==='6.53.0','real WordPress loads V6.53.0');
v653_assert(Pferdeportal_Affiliate_Router::EBAY_RUNTIME_BUILD==='6.52.0-core-cron-selfpump-rootfix-20260822','eBay runtime build stays unchanged');
echo "REAL_ARTICLE_PRODUCT_V653=PASS\n";
