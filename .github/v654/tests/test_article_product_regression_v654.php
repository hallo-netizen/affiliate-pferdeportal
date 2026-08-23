<?php
$root=getenv('PPAR_TEST_PLUGIN_DIR')?:'';if(!$root){exit(2);}
$trait=file_get_contents($root.'/includes/trait-ppar-article-plans.php');$main=file_get_contents($root.'/pferdeportal-affiliate-router.php');$css=file_get_contents($root.'/assets/frontend.css');
$n=0;$f=0;function a654($v,$m){global$n,$f;$n++;if(!$v){$f++;echo"FAIL $m\n";}else echo"PASS $m\n";}
a654(strpos($trait,'private function article_plan_render_product_card_markup')!==false,'dedicated product renderer preserved');
a654(strpos($trait,"render_banner(\$banner, \$post_id, \$this->get_content_context(\$post_id), \$group, 'post_bottom_products')")===false,'plan product no generic banner');
a654(strpos($main,"render_banner(\$banner, \$post_id, \$context, \$group, 'post_bottom_products')")===false,'legacy article product no generic banner');
foreach(['ppar-article-product-link','ppar-article-product-media','ppar-article-product-body','ppar-article-product-cta'] as $c){a654(strpos($trait,$c)!==false,'markup_'.$c);}
a654(strpos($css,'.ppar-article-product-card .ppar-banner-')===false,'css decoupled from banner');
a654(strpos($css,'object-fit: contain;')!==false,'product image contain');
a654(strpos($css,'border-color: #C89214;')!==false&&strpos($css,'background: #35422A;')!==false,'portal color contract');
a654(strpos($css,'text-decoration: none !important;')!==false,'no inherited underline');
echo"PRODUCT_REGRESSION_ASSERTIONS=$n FAIL=$f\n";exit($f?1:0);
