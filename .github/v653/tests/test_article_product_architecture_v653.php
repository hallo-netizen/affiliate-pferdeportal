<?php
$root=getenv('PPAR_TEST_PLUGIN_DIR');
if(!$root){fwrite(STDERR,"missing PPAR_TEST_PLUGIN_DIR\n");exit(2);}
$trait=file_get_contents($root.'/includes/trait-ppar-article-plans.php');
$main=file_get_contents($root.'/pferdeportal-affiliate-router.php');
$css=file_get_contents($root.'/assets/frontend.css');
$f=0;$n=0;function a($v,$m){global$f,$n;$n++;echo($v?'PASS ':'FAIL ').$m."\n";if(!$v)$f++;}
a(strpos($trait,'private function article_plan_render_product_card_markup')!==false,'dedicated article product renderer exists');
a(strpos($trait,"render_banner(\$banner, \$post_id, \$this->get_content_context(\$post_id), \$group, 'post_bottom_products')")===false,'plan renderer no longer reuses generic banner renderer');
a(strpos($main,"render_banner(\$banner, \$post_id, \$context, \$group, 'post_bottom_products')")===false,'legacy article product block no longer reuses generic banner renderer');
a(strpos($trait,'ppar-article-product-link')!==false,'product renderer emits dedicated link class');
a(strpos($trait,'ppar-article-product-media')!==false,'product renderer emits dedicated media class');
a(strpos($trait,'ppar-article-product-body')!==false,'product renderer emits dedicated body class');
a(strpos($trait,'ppar-article-product-cta')!==false,'product renderer emits dedicated CTA class');
a(strpos($css,'.ppar-article-product-card .ppar-banner-')===false,'article product CSS is decoupled from generic banner classes');
a(strpos($css,'object-fit: contain;')!==false,'product image uses non-distorting contain geometry');
a(strpos($css,'border-color: #C89214;')!==false && strpos($css,'background: #35422A;')!==false,'portal ochre/olive interaction contract exists');
a(strpos($css,'text-decoration: none !important;')!==false,'product card text never inherits global underline hover');
a(strpos($main,"const EBAY_RUNTIME_BUILD = '6.52.0-core-cron-selfpump-rootfix-20260822';")!==false,'unrelated eBay runtime build remains byte-contract unchanged');
if(getenv('PPAR_V653_FINAL')==='1'){
  a(strpos($main,' * Version: 6.53.0')!==false && strpos($main,"const VERSION = '6.53.0';")!==false,'release version is 6.53.0');
  $read=file_get_contents($root.'/readme.txt');
  a(strpos($read,'Stable tag: 6.53.0')!==false,'readme stable tag is 6.53.0');
}
echo "ASSERTIONS=$n FAIL=$f\n";exit($f?1:0);
