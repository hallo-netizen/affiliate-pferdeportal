#!/usr/bin/env python3
from pathlib import Path
import sys, hashlib

if len(sys.argv) != 5:
    raise SystemExit('usage: test_image_cache_rootfix.py <before.css> <after.css> <before.php> <after.php>')
bcss=Path(sys.argv[1]).read_text(encoding='utf-8')
acss=Path(sys.argv[2]).read_text(encoding='utf-8')
bphp=Path(sys.argv[3]).read_text(encoding='utf-8')
aphp=Path(sys.argv[4]).read_text(encoding='utf-8')
checks=[]
def ok(cond,name):
    checks.append((bool(cond),name)); print(('PASS ' if cond else 'FAIL ')+name)

marker='V6.55 image-cache rootfix: einheitliche sichtbare Bildgroesse'
ok(marker not in bcss,'pre_fix_marker_absent')
ok(marker in acss,'post_fix_marker_present')
ok(acss.startswith(bcss),'css_baseline_preserved')
suffix=acss[len(bcss):]
ok(suffix.count(marker)==1,'single_image_rule_block')
for slot in ('category_product_1','category_product_2','category_product_3'):
    ok(f'.ppar-slot-{slot} .ppar-banner-image-wrap' in suffix,f'{slot}_wrapper')
    ok(f'.ppar-slot-{slot} .ppar-banner-image' in suffix,f'{slot}_image')
ok('product_after_category_tiles' not in suffix,'banner_slot_untouched')
ok('width: 150px !important;' in suffix and 'height: 150px !important;' in suffix,'fixed_150_square')
ok('min-width: 150px !important;' in suffix and 'min-height: 150px !important;' in suffix,'cannot_shrink')
ok('max-width: 150px !important;' in suffix and 'max-height: 150px !important;' in suffix,'cannot_grow')
ok('object-fit: cover !important;' in suffix,'cover_fills_visible_area')
ok('object-position: center center !important;' in suffix,'cover_centered')
ok('ppar-article-product' not in suffix,'article_products_untouched')
ok('ppar-start-partner' not in suffix,'partner_cards_untouched')
ok('ppar-ebay-remote-image' not in suffix,'private_images_untouched')
ok(suffix.count('category_product_1')==suffix.count('category_product_2')==suffix.count('category_product_3'),'no_first_slot_special_case')

old="""        wp_enqueue_style(\n            'ppar-frontend',\n            plugins_url('assets/frontend.css', __FILE__),\n            array(),\n            self::VERSION\n        );"""
new="""        $frontend_css_path = __DIR__ . '/assets/frontend.css';\n        $frontend_css_ver = self::VERSION;\n        if (is_readable($frontend_css_path)) {\n            $frontend_css_hash = hash_file('sha256', $frontend_css_path);\n            if (is_string($frontend_css_hash) && $frontend_css_hash !== '') {\n                $frontend_css_ver .= '-' . substr($frontend_css_hash, 0, 12);\n            }\n        }\n        wp_enqueue_style(\n            'ppar-frontend',\n            plugins_url('assets/frontend.css', __FILE__),\n            array(),\n            $frontend_css_ver\n        );"""
ok(bphp.count(old)==1,'pre_fix_static_css_version_anchor')
ok(aphp.count(old)==0,'old_css_version_anchor_removed')
ok(aphp.count(new)==1,'exact_cache_buster_replacement')
ok("hash_file('sha256', $frontend_css_path)" in aphp,'content_hash_cache_buster')
ok("substr($frontend_css_hash, 0, 12)" in aphp,'short_hash_cache_key')
ok("'ppar-frontend',\n            plugins_url('assets/frontend.css', __FILE__),\n            array(),\n            $frontend_css_ver" in aphp,'style_uses_css_hash_version')
expected_php=bphp.replace(old,new,1)
ok(aphp==expected_php,'php_delta_exactly_enqueue_cache_buster')
# JS remains on the unchanged plugin version; no unrelated asset behavior is touched.
ok("plugins_url('assets/frontend.js', __FILE__),\n            array(),\n            self::VERSION," in aphp,'js_enqueue_unchanged')
# Prove CSS version changes when CSS bytes change while plugin version can remain unchanged.
base_hash=hashlib.sha256(bcss.encode()).hexdigest()[:12]
new_hash=hashlib.sha256(acss.encode()).hexdigest()[:12]
ok(base_hash!=new_hash,'css_content_change_changes_hash')
ok('6.55.0-'+base_hash != '6.55.0-'+new_hash,'cache_key_changes_without_plugin_version_bump')
ok(acss.count('{')==acss.count('}'),'css_braces_balanced')
failed=[n for p,n in checks if not p]
print(f'ASSERTIONS={len(checks)} FAIL={len(failed)}')
if failed: raise SystemExit(1)
print('IMAGE_CACHE_ROOTFIX_CONTRACT=PASS')
print('CSS_AFTER_SHA256='+hashlib.sha256(acss.encode()).hexdigest())
print('PHP_AFTER_SHA256='+hashlib.sha256(aphp.encode()).hexdigest())
