#!/usr/bin/env python3
from pathlib import Path
import re, sys, json

if len(sys.argv) != 4:
    raise SystemExit('usage: test_inline_image_rootfix.py <before.php> <after.php> <readme.txt>')
before=Path(sys.argv[1]); after=Path(sys.argv[2]); readme=Path(sys.argv[3])
bs=before.read_text(encoding='utf-8'); a=after.read_text(encoding='utf-8'); rt=readme.read_text(encoding='utf-8')
checks=[]
def ok(c,n):
    checks.append((bool(c),n)); print(('PASS ' if c else 'FAIL ')+n)
def header_version(s):
    m=re.search(r'^\s*\*\s*Version:\s*([^\r\n]+)',s,re.M); return m.group(1).strip() if m else ''
def const_version(s):
    m=re.search(r"const\s+VERSION\s*=\s*'([^']+)'",s); return m.group(1) if m else ''
def runtime_build(s):
    m=re.search(r"const\s+EBAY_RUNTIME_BUILD\s*=\s*'([^']+)'",s); return m.group(1) if m else ''
def stable_tag(s):
    m=re.search(r'^Stable tag:\s*([^\r\n]+)',s,re.M); return m.group(1).strip() if m else ''

ok(header_version(bs)=='6.54.0','pre_fix_wordpress_header_wrong_reproduced')
ok(const_version(bs)=='6.55.0','pre_fix_internal_version_655')
ok(stable_tag(rt)=='6.55.0','readme_top_stable_tag_655')
ok(header_version(a)=='6.55.0','post_fix_wordpress_header_655')
ok(const_version(a)=='6.55.0','post_fix_internal_version_655')
ok(header_version(a)==const_version(a)==stable_tag(rt),'metadata_three_way_consistency')
ok(runtime_build(a)==runtime_build(bs),'ebay_runtime_build_unchanged')
ok("preg_match('/^category_product_[123]$/'" in a,'category_product_123_only_guard')
ok('data-ppar-category-product-image-frame="150"' in a,'actual_markup_frame_marker')
for token in ('width:150px!important','height:150px!important','min-width:150px!important','min-height:150px!important','max-width:150px!important','max-height:150px!important'):
    ok(a.count(token)>=2,'inline_'+token.replace(':','_').replace('!','').replace(';',''))
ok('object-fit:cover!important' in a,'inline_cover')
ok('object-position:center center!important' in a,'inline_center')
new_guard=a[a.index('$category_product_slot'):a.index("if ($url === '')",a.index('$category_product_slot'))]
ok('product_after_category_tiles' not in new_guard,'banner_slot_not_in_new_guard')

normalized=a.replace(' * Version: 6.55.0',' * Version: 6.54.0',1)
insert="""        $category_product_slot = $creative_type === 'product' && preg_match('/^category_product_[123]$/', sanitize_key((string)$slot_type));
        $category_product_wrap_attr = $category_product_slot
            ? ' data-ppar-category-product-image-frame="150" style="box-sizing:border-box!important;display:flex!important;flex:0 0 150px!important;align-items:center!important;justify-content:center!important;width:150px!important;height:150px!important;min-width:150px!important;min-height:150px!important;max-width:150px!important;max-height:150px!important;margin:0 auto!important;padding:0!important;overflow:hidden!important;background:#fff!important;line-height:0!important"'
            : '';
        $category_product_image_attr = $category_product_slot
            ? ' style="box-sizing:border-box!important;display:block!important;width:150px!important;height:150px!important;min-width:150px!important;min-height:150px!important;max-width:150px!important;max-height:150px!important;margin:0!important;padding:0!important;border-radius:0!important;object-fit:cover!important;object-position:center center!important"'
            : '';
"""
changed="""            $out .= '<span class="ppar-banner-image-wrap"' . $category_product_wrap_attr . '><img class="ppar-banner-image"' . $category_product_image_attr . ' src="' . esc_url($image_url) . '" alt="' . esc_attr($title !== '' ? $title : $button) . '" loading="lazy"></span>';"""
base="""            $out .= '<span class="ppar-banner-image-wrap"><img class="ppar-banner-image" src="' . esc_url($image_url) . '" alt="' . esc_attr($title !== '' ? $title : $button) . '" loading="lazy"></span>';"""
ok(normalized.count(insert)==1,'exact_inline_block_once')
normalized=normalized.replace(insert,'',1)
ok(normalized.count(changed)==1,'exact_changed_markup_once')
normalized=normalized.replace(changed,base,1)
ok(normalized==bs,'all_other_php_bytes_preserved')

wrap_style='box-sizing:border-box!important;display:flex!important;flex:0 0 150px!important;align-items:center!important;justify-content:center!important;width:150px!important;height:150px!important;min-width:150px!important;min-height:150px!important;max-width:150px!important;max-height:150px!important;margin:0 auto!important;padding:0!important;overflow:hidden!important;background:#fff!important;line-height:0!important'
img_style='box-sizing:border-box!important;display:block!important;width:150px!important;height:150px!important;min-width:150px!important;min-height:150px!important;max-width:150px!important;max-height:150px!important;margin:0!important;padding:0!important;border-radius:0!important;object-fit:cover!important;object-position:center center!important'
ok(wrap_style in a,'exact_wrap_style_present')
ok(img_style in a,'exact_image_style_present')

failed=[n for p,n in checks if not p]
print(f'ASSERTIONS={len(checks)} FAIL={len(failed)}')
if failed:
    print('FAILED='+','.join(failed)); raise SystemExit(1)
print('INLINE_IMAGE_ROOTFIX_STATIC=PASS')
