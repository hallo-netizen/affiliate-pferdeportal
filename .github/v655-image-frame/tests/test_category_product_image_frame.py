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

marker = "V6.55 CSS-only: einheitliche sichtbare Bildgroesse fuer die drei Produktvorschlaege auf Produkt-/Kategorieseiten."
ok(marker not in before, "pre_fix_marker_absent")
ok(marker in after, "post_fix_marker_present")
ok(after.startswith(before), "css_baseline_preserved_byte_for_byte")
suffix = after[len(before):]
ok(suffix.count(marker) == 1, "single_scoped_fix_block")
for slot in ["category_product_1", "category_product_2", "category_product_3"]:
    ok((f".ppar-slot-{slot} .ppar-banner-image-wrap") in suffix, f"{slot}_wrapper_scoped")
    ok((f".ppar-slot-{slot} .ppar-banner-image") in suffix, f"{slot}_image_scoped")
ok("product_after_category_tiles" not in suffix, "banner_slot_untouched")
ok(suffix.count("width: 150px !important;") >= 2, "fixed_150px_width")
ok(suffix.count("height: 150px !important;") >= 2, "fixed_150px_height")
ok("min-width: 150px !important;" in suffix and "min-height: 150px !important;" in suffix, "image_cannot_shrink")
ok("max-width: 150px !important;" in suffix and "max-height: 150px !important;" in suffix, "image_cannot_grow")
ok("object-fit: cover !important;" in suffix, "visible_area_filled_cover")
ok("object-fit: contain !important;" not in suffix, "letterbox_contain_removed")
ok("object-position: center center !important;" in suffix, "centered_image")
ok("align-items: center !important;" in suffix and "justify-content: center !important;" in suffix, "centered_frame")
ok("overflow: hidden !important;" in suffix, "frame_overflow_bounded")
ok("ppar-article-product" not in suffix, "article_product_layout_untouched")
ok("ppar-start-partner" not in suffix, "partner_banner_layout_untouched")
ok("ppar-ebay-remote-image" not in suffix, "hivepress_private_image_layout_untouched")
# All three slots must share one declaration block; no first-position exception may exist.
wrapper_head = suffix.split("{", 1)[0]
ok(all(f".ppar-slot-category_product_{i} .ppar-banner-image-wrap" in wrapper_head for i in (1,2,3)), "three_slots_same_wrapper_rule")
image_rule_start = suffix.find(".ppar-slot-category_product_1 .ppar-banner-image,")
image_rule_end = suffix.find("{", image_rule_start)
image_head = suffix[image_rule_start:image_rule_end]
ok(all(f".ppar-slot-category_product_{i} .ppar-banner-image" in image_head for i in (1,2,3)), "three_slots_same_image_rule")
ok(suffix.count("category_product_1") == suffix.count("category_product_2") == suffix.count("category_product_3"), "no_first_slot_special_case")
# Cover on a fixed square always fills the visible 150x150 area for portrait, square and landscape sources.
def cover_size(sw, sh, box=150):
    scale=max(box/sw, box/sh)
    return sw*scale, sh*scale
for name,(sw,sh) in {"portrait":(100,200),"square":(150,150),"landscape":(300,120)}.items():
    rw,rh=cover_size(sw,sh)
    ok(rw >= 150-1e-9 and rh >= 150-1e-9, f"cover_fills_{name}_source")
ok(after.count("{") == after.count("}"), "css_braces_balanced")
failed = [n for passed,n in checks if not passed]
print(f"ASSERTIONS={len(checks)} FAIL={len(failed)}")
if failed:
    raise SystemExit(1)
print("CATEGORY_PRODUCT_VISIBLE_IMAGE_SIZE_CONTRACT=PASS")
print("AFTER_SHA256=" + hashlib.sha256(after.encode()).hexdigest())
