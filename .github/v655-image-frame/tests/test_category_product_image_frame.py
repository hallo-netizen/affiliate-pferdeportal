#!/usr/bin/env python3
from pathlib import Path
import sys, hashlib

if len(sys.argv) != 3:
    raise SystemExit("usage: test_category_product_image_frame.py <before.css> <after.css>")
before = Path(sys.argv[1]).read_text(encoding="utf-8")
after = Path(sys.argv[2]).read_text(encoding="utf-8")
checks = []
def ok(cond, name):
    checks.append((bool(cond), name))
    print(("PASS " if cond else "FAIL ") + name)

marker = "V6.55 CSS-only: feste Bildgeometrie fuer Produktvorschlaege auf Produkt-/Kategorieseiten."
ok(marker not in before, "pre_fix_marker_absent")
ok(marker in after, "post_fix_marker_present")
ok(after.startswith(before), "css_baseline_preserved_byte_for_byte")
suffix = after[len(before):]
ok(suffix.count(marker) == 1, "single_scoped_fix_block")
for slot in ["product_after_category_tiles", "category_product_1", "category_product_2", "category_product_3"]:
    ok((f".ppar-slot-{slot} .ppar-banner-image-wrap") in suffix, f"{slot}_wrapper_scoped")
    ok((f".ppar-slot-{slot} .ppar-banner-image") in suffix, f"{slot}_image_scoped")
ok("height: 150px !important;" in suffix, "fixed_150px_frame")
ok("width: 150px !important;" in suffix, "fixed_150px_image_width")
ok("object-fit: contain !important;" in suffix, "no_crop_contain")
ok("object-position: center center !important;" in suffix, "centered_image")
ok("align-items: center !important;" in suffix and "justify-content: center !important;" in suffix, "centered_frame")
ok("overflow: hidden !important;" in suffix, "frame_overflow_bounded")
ok("ppar-article-product" not in suffix, "article_product_layout_untouched")
ok("ppar-start-partner" not in suffix, "partner_banner_layout_untouched")
ok("ppar-ebay-remote-image" not in suffix, "hivepress_private_image_layout_untouched")
ok(after.count("{") == after.count("}"), "css_braces_balanced")
failed = [n for passed,n in checks if not passed]
print(f"ASSERTIONS={len(checks)} FAIL={len(failed)}")
if failed:
    raise SystemExit(1)
print("CATEGORY_PRODUCT_IMAGE_FRAME_CONTRACT=PASS")
print("AFTER_SHA256=" + hashlib.sha256(after.encode()).hexdigest())
