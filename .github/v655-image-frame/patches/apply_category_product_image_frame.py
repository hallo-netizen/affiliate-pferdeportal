#!/usr/bin/env python3
from pathlib import Path
import hashlib, sys

EXPECTED = "8814070315f59e617e46d3e83bd3ab5880292e58cddc4644d6f0f6aa2a4dbd78"
SUFFIX = r'''

/* V6.55 CSS-only: einheitliche sichtbare Bildgroesse fuer die drei Produktvorschlaege auf Produkt-/Kategorieseiten.
   Ausschliesslich die Produktbildflaeche wird vereinheitlicht; Auswahl, Inhalte, Karten- und Buttondesign bleiben unveraendert. */
.ppar-slot-category_product_1 .ppar-banner-image-wrap,
.ppar-slot-category_product_2 .ppar-banner-image-wrap,
.ppar-slot-category_product_3 .ppar-banner-image-wrap {
    box-sizing: border-box !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 150px !important;
    height: 150px !important;
    max-width: 100% !important;
    max-height: 150px !important;
    margin: 0 auto !important;
    padding: 0 !important;
    overflow: hidden !important;
    background: #fff !important;
}

.ppar-slot-category_product_1 .ppar-banner-image,
.ppar-slot-category_product_2 .ppar-banner-image,
.ppar-slot-category_product_3 .ppar-banner-image {
    display: block !important;
    width: 150px !important;
    height: 150px !important;
    min-width: 150px !important;
    min-height: 150px !important;
    max-width: 150px !important;
    max-height: 150px !important;
    margin: 0 !important;
    padding: 0 !important;
    object-fit: cover !important;
    object-position: center center !important;
}
'''

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

if len(sys.argv) != 2:
    raise SystemExit("usage: apply_category_product_image_frame.py <frontend.css>")
path = Path(sys.argv[1])
raw = path.read_bytes()
if sha(raw) != EXPECTED:
    raise SystemExit(f"BLOCKED: frontend.css baseline drift: {sha(raw)}")
text = raw.decode("utf-8")
if "V6.55 CSS-only: einheitliche sichtbare Bildgroesse" in text:
    raise SystemExit("BLOCKED: visible-image patch already present")
path.write_text(text + SUFFIX, encoding="utf-8")
print("CATEGORY_PRODUCT_VISIBLE_IMAGE_SIZE_PATCH=PASS")
print("BEFORE_SHA256=" + EXPECTED)
print("AFTER_SHA256=" + sha(path.read_bytes()))
