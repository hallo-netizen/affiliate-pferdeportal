#!/usr/bin/env python3
from pathlib import Path
import re, sys

if len(sys.argv) != 4:
    raise SystemExit('usage: test_contain_rootfix.py <before.php> <after.php> <after_readme>')
b = Path(sys.argv[1]).read_text(encoding='utf-8')
a = Path(sys.argv[2]).read_text(encoding='utf-8')
r = Path(sys.argv[3]).read_text(encoding='utf-8')
checks=[]
def ok(c,n):
    checks.append((bool(c),n)); print(('PASS ' if c else 'FAIL ')+n)

ok(' * Version: 6.54.0' in b,'pre_header_654')
ok(' * Version: 6.55.0' in a,'post_header_655')
ok("const VERSION = '6.55.0';" in a,'const_655')
ok(a.count('data-ppar-category-product-image-frame=\\"150\\"')==1,'single_frame_attr_template')
ok(a.count('data-ppar-category-product-image-fit=\\"contain\\"')==1,'single_contain_attr_template')
ok('object-fit:contain!important' in a,'contain_present')
ok('object-fit:cover!important' not in a,'cover_absent_from_rootfix')
ok('object-position:center center!important' in a,'centered')
for token in ('width:150px!important','height:150px!important','min-width:150px!important','min-height:150px!important','max-width:150px!important','max-height:150px!important'):
    ok(token in a,'geometry_'+re.sub('[^a-z0-9]+','_',token.lower()).strip('_'))
ok("preg_match('/^category_product_[123]$/', sanitize_key((string)$slot_type))" in a,'scope_only_three_category_product_slots')
ok("$creative_type === 'product'" in a,'scope_only_product_creatives')
ok('frontend.css' in b and 'frontend.css' in a,'frontend_enqueue_still_present')
ok('Stable tag: 6.55.0' in r,'stable_tag_655')
ok(r.count('\nStable tag: ')==1,'exactly_one_canonical_stable_tag')
ok('Historical stable tag: 6.48.0' in r,'historical_stable_tag_demoted')
# no accidental runtime build change
rb=re.search(r"const EBAY_RUNTIME_BUILD = '([^']+)'",b).group(1)
ra=re.search(r"const EBAY_RUNTIME_BUILD = '([^']+)'",a).group(1)
ok(rb==ra,'runtime_build_unchanged')
failed=[n for p,n in checks if not p]
print(f'ASSERTIONS={len(checks)} FAIL={len(failed)}')
if failed: raise SystemExit(1)
print('CONTAIN_ROOTFIX_STATIC=PASS')
