#!/usr/bin/env python3
"""Build only HAB-004 RC21, compact category product cards matching the existing
Pferde Atelier 3-card slot principle. No changes to design, articles or other portals."""
from pathlib import Path
from io import BytesIO
from zipfile import ZipFile
import hashlib
root=Path("protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ")
archive=root/"PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip"
raw=archive.read_bytes()
sha=lambda value:hashlib.sha256(value).hexdigest()
assert sha(raw)=="532d3ef2552c44cc9652881e1ff943ad7bcd8ddd93fb779f5dab1d55a08b8d97", "Unexpected Hab RC20 base"
prefix="affiliate-portal-router/"
bridge=prefix+"includes/class-ppar-hab-bewahr-bridge.php"
main=prefix+"affiliate-portal-router.php"
css=prefix+"assets/frontend.css"
readme=prefix+"readme.txt"
def once(text,old,new):
    count=text.count(old)
    assert count==1,("unexpected replacement count",count,old[:170])
    return text.replace(old,new,1)
with ZipFile(BytesIO(raw)) as orig:
    assert orig.testzip() is None and len(orig.namelist())==36
    files={i.filename:orig.read(i.filename) for i in orig.infolist()}
    b=files[bridge].decode("utf8")
    needle="    private static function area($html, $node_id, $kind) {"
    helper=r'''    /**
     * Compact product grid in the EXISTING Hab category product filter.
     * One clearly marked recommendation area, zero extra queries.
     * The original router still selects products and verified provider offers.
     */
    private static function category_product_grid_markup($html) {
        $html=is_string($html)?trim($html):'';
        if ($html==='') { return ''; }
        return '<div class="ppar-hb-category-product-group" data-hab-affiliate-category-grid="1">'
            .'<div class="ppar-hb-category-product-adlabel">Anzeige</div>'
            .'<div class="ppar-hb-category-products-grid">'.$html.'</div></div>';
    }

'''
    b=once(b,needle,helper+needle)
    # Current leaf-category output is the three concatenated original product slots.
    b=once(b,"""            return $output;
        }
        if (($node['type'] ?? '') !== 'page') { return ''; }""",
    """            return self::category_product_grid_markup($output);
        }
        if (($node['type'] ?? '') !== 'page') { return ''; }""")
    # Keep banners, world hubs, posts, editorial and special contexts unchanged.
    b=once(b,"""        return Portal_Affiliate_Router::instance()->hab_bw_area_slot($id,$kind,(string)$node['id']);
    }
    public static function world_banner""",
    """        $result=Portal_Affiliate_Router::instance()->hab_bw_area_slot($id,$kind,(string)$node['id']);
        if ($kind!=='products' || (string)($node['pillar'] ?? '')!=='core'
            || strpos((string)($node['id'] ?? ''),'core:world:')===0) { return $result; }
        return self::category_product_grid_markup($result);
    }
    public static function world_banner""")
    files[bridge]=b.encode("utf8")
    s=files[main].decode("utf8")
    s=once(s,"Version: 0.1.17-rc20","Version: 0.1.18-rc21")
    # Hab-only original category-product slots formerly enforce 416/360/210px
    # even for cards without an image. No impact to non-category slot rules.
    s=once(s,
      "display:grid!important;grid-template-rows:56px minmax(360px,1fr)!important;width:100%!important;height:auto!important;min-height:416px!important;",
      "display:flex!important;flex-direction:column!important;grid-template-rows:none!important;width:100%!important;height:100%!important;min-height:0!important;")
    s=once(s,
      "display:grid!important;grid-template-rows:150px minmax(210px,1fr)!important;align-items:stretch!important;width:100%!important;height:auto!important;min-height:360px!important;",
      "display:grid!important;grid-template-rows:150px auto!important;align-items:stretch!important;width:100%!important;height:auto!important;min-height:0!important;")
    s=once(s,
      "width:100%!important;min-height:152px!important\"')",
      "width:100%!important;min-height:0!important\"')")
    files[main]=s.encode("utf8")
    style=files[css].decode("utf8")
    assert "ppar-hb-category-products-grid" not in style
    style+=r'''

/* HAB-004 RC21 – Existing category recommendations: compact horse-derived
   3/2/1 real product cards. Scoped ONLY to the HB category filter wrapper.
   Provider buttons stay on the original exact-product campaign; no fake
   images, invented matches, price data, or duplicate banner engine. */
.ppar-hb-category-product-group {
  display:block!important; box-sizing:border-box!important;
  width:100%!important; max-width:100%!important;
  margin:0!important; padding:0!important;
}
.ppar-hb-category-product-adlabel {
  font:600 10px/1.35 Arial,sans-serif!important;
  letter-spacing:.065em!important; text-transform:uppercase!important;
  color:#6b7470!important; margin:0 0 10px!important;
}
.ppar-hb-category-products-grid {
  display:grid!important; grid-template-columns:repeat(3,minmax(0,1fr))!important;
  align-items:stretch!important; gap:14px!important;
  box-sizing:border-box!important; width:100%!important;
  margin:0!important; padding:0!important;
}
.ppar-hb-category-products-grid > .ppar-affiliate-slot {
  display:flex!important; flex-direction:column!important;
  box-sizing:border-box!important; width:100%!important; max-width:100%!important;
  min-width:0!important; height:100%!important; min-height:0!important;
  margin:0!important; padding:14px!important;
  border:1px solid #d1d9d4!important; border-radius:11px!important;
  background:#fff!important; box-shadow:none!important; overflow:hidden!important;
  grid-template-rows:none!important;
}
.ppar-hb-category-products-grid > .ppar-affiliate-slot > .ppar-affiliate-label {
  display:none!important;
}
.ppar-hb-category-products-grid > .ppar-affiliate-slot > .ppar-affiliate-disclosure {
  font-size:10px!important; margin:0 0 8px!important;
}
.ppar-hb-category-products-grid > .ppar-affiliate-slot > .ppar-affiliate-content {
  display:flex!important; flex:1 1 auto!important; flex-direction:column!important;
  box-sizing:border-box!important; min-height:0!important; width:100%!important;
  margin:0!important; padding:0!important;
}
.ppar-hb-category-products-grid .ppar-banner-link[data-ppar-category-product-card="1"] {
  display:flex!important; flex-direction:column!important;
  flex:1 1 auto!important; width:100%!important;
  height:auto!important; min-height:0!important;
  grid-template-rows:none!important; box-sizing:border-box!important;
  margin:0!important; padding:0!important; gap:12px!important;
  text-decoration:none!important;
}
.ppar-hb-category-products-grid .ppar-banner-image-wrap {
  display:flex!important; align-items:center!important; justify-content:center!important;
  max-width:100%!important; background:#fff!important;
}
.ppar-hb-category-products-grid .ppar-banner-text[data-ppar-category-product-text="1"] {
  display:flex!important; flex:1 1 auto!important; flex-direction:column!important;
  gap:10px!important; width:100%!important;
  height:auto!important; min-height:0!important; margin:0!important;
  padding:0!important; box-sizing:border-box!important;
}
.ppar-hb-category-products-grid .ppar-banner-title {
  font-size:13px!important; line-height:1.45!important; font-weight:600!important;
  overflow-wrap:anywhere!important; margin:0!important; padding:0!important;
}
.ppar-hb-category-products-grid .ppar-banner-actions {
  display:flex!important; flex-direction:column!important; gap:7px!important;
  margin-top:auto!important; width:100%!important;
}
.ppar-hb-category-products-grid .ppar-banner-button,
.ppar-hb-category-products-grid .ppar-banner-offer-button {
  display:flex!important; justify-content:center!important; align-items:center!important;
  box-sizing:border-box!important; width:100%!important;
  min-height:34px!important; border:1px solid #829c8d!important;
  border-radius:7px!important; padding:7px 9px!important;
  background:#f6f9f7!important; color:#254b3e!important;
  font:600 12px/1.35 Arial,sans-serif!important;
  text-decoration:none!important; text-align:center!important;
  white-space:normal!important;
}
.ppar-hb-category-products-grid .ppar-banner-button:hover,
.ppar-hb-category-products-grid .ppar-banner-offer-button:hover,
.ppar-hb-category-products-grid .ppar-banner-offer-button:focus-visible {
  background:#e4ede7!important; color:#193b30!important;
}
@media (max-width:900px) {
  .ppar-hb-category-products-grid {grid-template-columns:repeat(2,minmax(0,1fr))!important;}
}
@media (max-width:620px) {
  .ppar-hb-category-products-grid {grid-template-columns:minmax(0,1fr)!important;gap:12px!important;}
  .ppar-hb-category-products-grid > .ppar-affiliate-slot {padding:14px!important;}
}
'''
    files[css]=style.encode("utf8")
    rm=files[readme].decode("utf8")
    rm=once(rm,"Stable tag: 0.1.17-rc20","Stable tag: 0.1.18-rc21")
    files[readme]=rm.encode("utf8")
    changed={bridge,main,css,readme}
    for item in orig.namelist():
        if item not in changed:assert files[item] == orig.read(item)
    output=BytesIO()
    with ZipFile(output,"w") as dest:
        for member in orig.infolist():dest.writestr(member,files[member.filename])
    product=output.getvalue()
with ZipFile(BytesIO(product)) as verified:
    assert verified.testzip() is None and len(verified.namelist())==36
    assert verified.read(bridge).count(b'ppar-hb-category-products-grid') == 1
    assert b'grid-template-rows:56px minmax(360px,1fr)!important' not in verified.read(main)
    assert b'Version: 0.1.18-rc21' in verified.read(main)
    assert b'multiprovider_matching_offers_for_banner' in verified.read(main)
archive.write_bytes(product)
print("HAB RC21 ZIP",len(product),"SHA256",sha(product),"CRC PASS",len(files),"files")
print("CHANGED",",".join(x.removeprefix(prefix) for x in sorted(changed)))
