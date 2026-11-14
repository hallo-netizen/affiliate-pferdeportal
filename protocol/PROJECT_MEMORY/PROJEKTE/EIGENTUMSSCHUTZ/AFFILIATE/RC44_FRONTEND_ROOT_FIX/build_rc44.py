#!/usr/bin/env python3
"""RC44: proven causes only in ORIGINAL Hab Affiliate-Zentrale.
One old owner chooses correct R3/R2 scope and real R2 slot.
A finished clickable original image needs no duplicate "Mehr erfahren".
Uses EXACT live RC43 ZIP from the canonical HAB-004 office.
"""
from pathlib import Path
from hashlib import sha256
from io import BytesIO
from zipfile import ZipFile
R=Path("protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ")
P=R/"PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip"
old=P.read_bytes()
assert sha256(old).hexdigest()=="7e9a92fa2ee5ac93c6dce8bd4924858d661478921b6768c2103172845ed9e2e8","Exact approved RC43 archive required"
B="affiliate-portal-router/"
MAIN=B+"affiliate-portal-router.php"
OUT=B+"includes/trait-ppar-output-objects.php"
README=B+"readme.txt"
def once(s,a,b):
    assert s.count(a)==1,("Source mismatch",s.count(a),a[:250])
    return s.replace(a,b,1)
with ZipFile(BytesIO(old)) as z:
    assert z.testzip() is None and len(z.namelist())==36
    data={x.filename:z.read(x.filename) for x in z.infolist()}
    o=data[OUT].decode()
    o=once(o,
        "'hundeversicherung'=>'haftpflicht-und-rechtsschutz',",
        "'hundeversicherung'=>'hundehaftpflichtversicherung',")
    o=once(o,
        """        // Exact WP IDs and ancestry from the verified HB tree, not name matching
        // after the initial unique banner type is selected.
        $allowed=array();
        foreach($eligible as $key=>$item) {""",
        """        // Broad named R2 products must NEVER be sprayed onto unrelated
        // R3 pages such as Tierkrankenversicherung or Rechtsschutz.
        // Only the genuine general insurance creative may cover R1 descendants.
        // Keep exact R3 products on their own R3 and its genuine leaf children.
        $r2_exact_owner_only=$anchor!==$root
            && $original_deep!==''
            && isset($fixed_original_deep_to_existing_wp_slug[$original_deep])
            && (string)($nodes[$anchor]['parent']??'')===$root;
        // Exact WP IDs and ancestry from the verified HB tree, not name matching
        // after the initial unique banner type is selected.
        $allowed=array();
        foreach($eligible as $key=>$item) {
            if($r2_exact_owner_only && $key!==$anchor)continue;""")
    # Only the already proven slot compatibility owner decides, once.
    o=once(o,
        """        $priority = $creative_type === 'product'""",
        """        // Hab insurance R2 uses its LIVE HUB slot. Former priority selected
        // product_after_category_tiles for hub2 instead, leaving the R2
        // hub_after_cards surface empty. Never re-check source/format later.
        // Any user's manual approved slot was already honored above.
        if($hb_verified_insurance_target && $target_context==='hub2'
           && isset($matches['hub_after_cards'])){
            return array('slot_id'=>'hub_after_cards','rule'=>$matches['hub_after_cards']);
        }
        $priority = $creative_type === 'product'""")
    o=once(o,"$option='ppar_hab_rc43_tarifcheck_reconcile_v1';",
              "$option='ppar_hab_rc44_tarifcheck_reconcile_v1';")
    data[OUT]=o.encode()
    m=data[MAIN].decode()
    m=once(m,
        """                '</a>' .
                '<!--ppar-overview-cta-v67280-->' .
                '<div class="ppar-overview-wide-banner-cta-wrap"><a class="ppar-overview-wide-banner-cta" href="' . esc_url($url) . '" target="' . esc_attr($target) . '" rel="' . esc_attr($rel) . '">Mehr erfahren</a></div>';""",
        """                '</a>';""")
    m=once(m,"Version: 0.1.40-rc43","Version: 0.1.41-rc44")
    data[MAIN]=m.encode()
    rd=data[README].decode()
    rd=once(rd,"Stable tag: 0.1.40-rc43","Stable tag: 0.1.41-rc44")
    data[README]=rd.encode()
    touched={MAIN,OUT,README}
    assert all(data[n]==z.read(n) for n in z.namelist() if n not in touched)
    buff=BytesIO()
    with ZipFile(buff,"w") as new:
        for info in z.infolist():new.writestr(info,data[info.filename])
    result=buff.getvalue()
with ZipFile(BytesIO(result)) as z:
    assert z.testzip() is None and len(z.namelist())==36
    assert b"ppar_hab_rc44_tarifcheck_reconcile_v1" in z.read(OUT)
    assert b"0.1.41-rc44" in z.read(MAIN)
    assert b"ppar-overview-wide-banner-cta-wrap" not in z.read(MAIN)
P.write_bytes(result)
print("RC44_PROVEN_SINGLE_OWNER_EXACT_R2_HUB_SLOT_NO_DUPLICATE_CTA_BUILD_PASS",len(result),sha256(result).hexdigest())
