#!/usr/bin/env python3
"""HAB RC30: EXACTLY one Anzeige per existing recommendation grid; actual
sourced product properties rendered in legible bullets, not one thin line.
No new data, no new systems, no category or merchant changes.
Base: verified RC29 ZIP. Change only main PHP, existing CSS, readme.
"""
from pathlib import Path
from zipfile import ZipFile
from io import BytesIO
from hashlib import sha256

ROOT=Path("protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ")
P=ROOT/"PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip"
raw=P.read_bytes()
assert sha256(raw).hexdigest()=="089a7dea5ccdd0e243e0a0116e52289bc904f97b3e2397f744b316d6063606f1","Only verified RC29 is allowed"
base="affiliate-portal-router/"
main=base+"affiliate-portal-router.php"
css=base+"assets/frontend.css"
readme=base+"readme.txt"
def once(s,a,b):
    n=s.count(a)
    assert n==1,("Anchor changed",n,a[:200])
    return s.replace(a,b,1)
with ZipFile(BytesIO(raw)) as z:
    assert z.testzip() is None and len(z.namelist())==36
    files={i.filename:z.read(i.filename) for i in z.infolist()}
    s=files[main].decode()
    s=once(s,"Version: 0.1.26-rc29","Version: 0.1.27-rc30")
    # ACTUAL live DOM: group label emitted exactly once by
    # PPAR_HB_Integration::category_product_grid_markup(). The first product
    # still emits a second <div class="ppar-affiliate-disclosure">Anzeige</div>.
    # Category-product slots are always grouped in the Hab DESIGN filter.
    # Suppress the per-product label at its SOURCE, not with a CSS bandaid.
    s=once(s,
        """                        if ($is_category_product_slot && $disclosure === '' && trim((string)get_option(self::OPTION_DISCLOSURE, '')) !== '') {
                            $disclosure = '<div class="ppar-affiliate-disclosure ppar-affiliate-disclosure--reserve" aria-hidden="true">&nbsp;</div>';
                        }""",
        """                        if ($is_category_product_slot) {
                            // The existing HB recommendation grid owns ONE
                            // visible disclosure: "Anzeige" above all cards.
                            // Never emit an additional notice in a product.
                            $disclosure = '';
                        }""")
    # The *real* product description already contains 2–3 factual properties
    # from the feed. Display as individual bullets, not a single minuscule
    # "Marke · Maße · Art.-Nr." string. Do not fabricate specifications.
    s=once(s,
        """            if ($description !== '') { $out .= '<span class="ppar-banner-description">' . esc_html($description) . '</span>'; }""",
        """            if ($description !== '') {
                if ($category_product_slot && $creative_type === 'product' && $network === 'idealo') {
                    $facts = preg_split('/\\s*·\\s*/u', trim((string)$description));
                    $facts = is_array($facts) ? array_values(array_filter(array_map('trim',$facts), static function($v){return $v!=='';})) : array();
                    if ($facts) {
                        $out .= '<span class="ppar-banner-description ppar-hb-product-facts">';
                        foreach (array_slice($facts,0,3) as $fact) {
                            $out .= '<span class="ppar-hb-product-fact">' . esc_html($fact) . '</span>';
                        }
                        $out .= '</span>';
                    }
                } else {
                    $out .= '<span class="ppar-banner-description">' . esc_html($description) . '</span>';
                }
            }""")
    files[main]=s.encode()
    st=files[css].decode()
    assert "/* HAB RC30" not in st
    st+=r'''

/* HAB RC30 – existing idealo category cards only: compact, readable FACTS.
   ONE group label is emitted by the existing HB category bridge.
   No changes to non-product banners, other providers, homepage or magazine. */
.ppar-hb-category-products-grid .ppar-hb-product-facts {
  display:block!important;
  color:#33483D!important;
  font-size:12px!important;
  line-height:1.42!important;
  font-weight:400!important;
  text-align:left!important;
  margin:7px 0 8px!important;
  padding:0!important;
}
.ppar-hb-category-products-grid .ppar-hb-product-fact {
  display:block!important;
  box-sizing:border-box!important;
  position:relative!important;
  padding-left:13px!important;
  margin:0 0 3px!important;
  text-align:left!important;
  overflow-wrap:anywhere!important;
}
.ppar-hb-category-products-grid .ppar-hb-product-fact::before {
  content:"•";
  display:block;
  position:absolute;
  left:1px;
  top:0;
  color:#33483D;
}
'''
    files[css]=st.encode()
    r=files[readme].decode()
    r=once(r,"Stable tag: 0.1.26-rc29","Stable tag: 0.1.27-rc30")
    files[readme]=r.encode()
    changed={main,css,readme}
    assert all(files[n]==z.read(n) for n in z.namelist() if n not in changed)
    out=BytesIO()
    with ZipFile(out,"w") as target:
        for item in z.infolist():target.writestr(item,files[item.filename])
    data=out.getvalue()
with ZipFile(BytesIO(data)) as verify:
    assert verify.testzip() is None and len(verify.namelist())==36
    assert b"ppar-hb-product-fact" in verify.read(main)
    assert b"$disclosure = '';" in verify.read(main)
P.write_bytes(data)
print("HAB_RC30_KISS_BUILD_PASS",len(data),sha256(data).hexdigest())
