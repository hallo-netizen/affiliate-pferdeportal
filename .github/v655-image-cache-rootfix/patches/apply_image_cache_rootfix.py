#!/usr/bin/env python3
from pathlib import Path
import hashlib, sys

CSS_EXPECTED = "8814070315f59e617e46d3e83bd3ab5880292e58cddc4644d6f0f6aa2a4dbd78"
PHP_EXPECTED = "d0175a72bc2f31f7b426d948157928a84f96440a5471c9929f8a8029b93b0a5f"
MARKER = "V6.55 image-cache rootfix: einheitliche sichtbare Bildgroesse"
CSS_SUFFIX = r'''

/* V6.55 image-cache rootfix: einheitliche sichtbare Bildgroesse fuer die drei Produktvorschlaege.
   Der CSS-Hash im Enqueue sorgt dafuer, dass genau diese Regel nach Plugin-Update sicher neu geladen wird. */
.ppar-slot-category_product_1 .ppar-banner-image-wrap,
.ppar-slot-category_product_2 .ppar-banner-image-wrap,
.ppar-slot-category_product_3 .ppar-banner-image-wrap {
    box-sizing: border-box !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 150px !important;
    height: 150px !important;
    min-width: 150px !important;
    min-height: 150px !important;
    max-width: 150px !important;
    max-height: 150px !important;
    margin: 0 auto !important;
    padding: 0 !important;
    overflow: hidden !important;
    background: #fff !important;
}

.ppar-slot-category_product_1 .ppar-banner-image,
.ppar-slot-category_product_2 .ppar-banner-image,
.ppar-slot-category_product_3 .ppar-banner-image {
    box-sizing: border-box !important;
    display: block !important;
    width: 150px !important;
    height: 150px !important;
    min-width: 150px !important;
    min-height: 150px !important;
    max-width: 150px !important;
    max-height: 150px !important;
    margin: 0 !important;
    padding: 0 !important;
    border-radius: 0 !important;
    object-fit: cover !important;
    object-position: center center !important;
}
'''
PHP_OLD = """        wp_enqueue_style(\n            'ppar-frontend',\n            plugins_url('assets/frontend.css', __FILE__),\n            array(),\n            self::VERSION\n        );"""
PHP_NEW = """        $frontend_css_path = __DIR__ . '/assets/frontend.css';\n        $frontend_css_ver = self::VERSION;\n        if (is_readable($frontend_css_path)) {\n            $frontend_css_hash = hash_file('sha256', $frontend_css_path);\n            if (is_string($frontend_css_hash) && $frontend_css_hash !== '') {\n                $frontend_css_ver .= '-' . substr($frontend_css_hash, 0, 12);\n            }\n        }\n        wp_enqueue_style(\n            'ppar-frontend',\n            plugins_url('assets/frontend.css', __FILE__),\n            array(),\n            $frontend_css_ver\n        );"""

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

if len(sys.argv) != 3:
    raise SystemExit("usage: apply_image_cache_rootfix.py <frontend.css> <pferdeportal-affiliate-router.php>")
css = Path(sys.argv[1]); php = Path(sys.argv[2])
css_raw = css.read_bytes(); php_raw = php.read_bytes()
if sha(css_raw) != CSS_EXPECTED:
    raise SystemExit(f"BLOCKED: frontend.css baseline drift: {sha(css_raw)}")
if sha(php_raw) != PHP_EXPECTED:
    raise SystemExit(f"BLOCKED: main PHP baseline drift: {sha(php_raw)}")
css_text = css_raw.decode('utf-8'); php_text = php_raw.decode('utf-8')
if MARKER in css_text:
    raise SystemExit('BLOCKED: image-cache rootfix already present')
if php_text.count(PHP_OLD) != 1:
    raise SystemExit(f"BLOCKED: frontend CSS enqueue anchor count={php_text.count(PHP_OLD)}")
css.write_text(css_text + CSS_SUFFIX, encoding='utf-8')
php.write_text(php_text.replace(PHP_OLD, PHP_NEW, 1), encoding='utf-8')
print('IMAGE_CACHE_ROOTFIX_PATCH=PASS')
print('CSS_BEFORE_SHA256=' + CSS_EXPECTED)
print('CSS_AFTER_SHA256=' + sha(css.read_bytes()))
print('PHP_BEFORE_SHA256=' + PHP_EXPECTED)
print('PHP_AFTER_SHA256=' + sha(php.read_bytes()))
