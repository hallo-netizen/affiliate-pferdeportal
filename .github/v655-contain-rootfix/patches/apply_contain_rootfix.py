#!/usr/bin/env python3
from pathlib import Path
import hashlib, sys

PHP_EXPECTED = "d0175a72bc2f31f7b426d948157928a84f96440a5471c9929f8a8029b93b0a5f"
HEADER_OLD = " * Version: 6.54.0"
HEADER_NEW = " * Version: 6.55.0"
HIST_STABLE_OLD = "Stable tag: 6.48.0"
HIST_STABLE_NEW = "Historical stable tag: 6.48.0"
ANCHOR = """        $creative_type = sanitize_key((string)($banner['creative_type'] ?? 'banner'));

        if ($url === '') {
            return '';
        }

        $target = (($banner['target'] ?? '_blank') === '_self') ? '_self' : '_blank';
        $rel = $target === '_blank' ? 'sponsored nofollow noopener noreferrer' : 'sponsored nofollow';
        $out = '<a class=\"ppar-banner-link\" href=\"' . esc_url($url) . '\" target=\"' . esc_attr($target) . '\" rel=\"' . esc_attr($rel) . '\">';
        if ($image_url !== '') {
            $out .= '<span class=\"ppar-banner-image-wrap\"><img class=\"ppar-banner-image\" src=\"' . esc_url($image_url) . '\" alt=\"' . esc_attr($title !== '' ? $title : $button) . '\" loading=\"lazy\"></span>';
        }
"""
REPLACEMENT = """        $creative_type = sanitize_key((string)($banner['creative_type'] ?? 'banner'));
        $category_product_slot = $creative_type === 'product' && preg_match('/^category_product_[123]$/', sanitize_key((string)$slot_type));
        $category_product_wrap_attr = $category_product_slot
            ? ' data-ppar-category-product-image-frame=\"150\" style=\"box-sizing:border-box!important;display:flex!important;flex:0 0 150px!important;align-items:center!important;justify-content:center!important;width:150px!important;height:150px!important;min-width:150px!important;min-height:150px!important;max-width:150px!important;max-height:150px!important;margin:0 auto!important;padding:0!important;overflow:hidden!important;background:#fff!important;line-height:0!important\"'
            : '';
        $category_product_image_attr = $category_product_slot
            ? ' data-ppar-category-product-image-fit=\"contain\" style=\"box-sizing:border-box!important;display:block!important;width:150px!important;height:150px!important;min-width:150px!important;min-height:150px!important;max-width:150px!important;max-height:150px!important;margin:0!important;padding:0!important;border-radius:0!important;object-fit:contain!important;object-position:center center!important\"'
            : '';

        if ($url === '') {
            return '';
        }

        $target = (($banner['target'] ?? '_blank') === '_self') ? '_self' : '_blank';
        $rel = $target === '_blank' ? 'sponsored nofollow noopener noreferrer' : 'sponsored nofollow';
        $out = '<a class=\"ppar-banner-link\" href=\"' . esc_url($url) . '\" target=\"' . esc_attr($target) . '\" rel=\"' . esc_attr($rel) . '\">';
        if ($image_url !== '') {
            $out .= '<span class=\"ppar-banner-image-wrap\"' . $category_product_wrap_attr . '><img class=\"ppar-banner-image\"' . $category_product_image_attr . ' src=\"' . esc_url($image_url) . '\" alt=\"' . esc_attr($title !== '' ? $title : $button) . '\" loading=\"lazy\"></span>';
        }
"""

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

if len(sys.argv) != 3:
    raise SystemExit('usage: apply_contain_rootfix.py <pferdeportal-affiliate-router.php> <readme.txt>')
p = Path(sys.argv[1]); r = Path(sys.argv[2])
raw = p.read_bytes(); rs = r.read_text(encoding='utf-8')
if sha(raw) != PHP_EXPECTED:
    raise SystemExit('BLOCKED: baseline php drift '+sha(raw))
s = raw.decode('utf-8')
if s.count(HEADER_OLD) != 1 or s.count(HEADER_NEW) != 0:
    raise SystemExit('BLOCKED: plugin header baseline unexpected')
if s.count(ANCHOR) != 1:
    raise SystemExit('BLOCKED: render anchor count='+str(s.count(ANCHOR)))
if rs.count(HIST_STABLE_OLD) != 1:
    raise SystemExit('BLOCKED: historical stable-tag baseline unexpected')
s = s.replace(HEADER_OLD, HEADER_NEW, 1).replace(ANCHOR, REPLACEMENT, 1)
rs = rs.replace(HIST_STABLE_OLD, HIST_STABLE_NEW, 1)
p.write_text(s, encoding='utf-8'); r.write_text(rs, encoding='utf-8')
print('CONTAIN_ROOTFIX_PATCH=PASS')
print('PHP_AFTER_SHA256='+sha(p.read_bytes()))
print('README_AFTER_SHA256='+sha(r.read_bytes()))
