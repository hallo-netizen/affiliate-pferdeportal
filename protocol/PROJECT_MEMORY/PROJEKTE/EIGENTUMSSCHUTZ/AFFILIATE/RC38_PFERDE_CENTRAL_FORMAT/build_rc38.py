#!/usr/bin/env python3
"""RC38: ONE central import-time format decision for verified Hab insurance.
Pferde-Atelier principle: only the existing target owner assigns a real slot;
stored placement is read afterwards, never reclassified or resized upwards.
No new tables, jobs, slots, or independent secondary banner logic.
"""
from pathlib import Path
from io import BytesIO
from hashlib import sha256
from zipfile import ZipFile

R=Path('protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ')
P=R/'PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip'
raw=P.read_bytes()
assert sha256(raw).hexdigest()=='1270b6a5c384c701f0c7f3487fc0770e1283aba8a04db787b76377f186fa099e','Require real RC37'
B='affiliate-portal-router/'
OUT=B+'includes/trait-ppar-output-objects.php'
MAIN=B+'affiliate-portal-router.php'
CSS=B+'assets/frontend.css'
README=B+'readme.txt'
def one(text,old,new):
    assert text.count(old)==1,('source differs; stop!',text.count(old),old[:130])
    return text.replace(old,new,1)
with ZipFile(BytesIO(raw)) as original:
    assert original.testzip() is None and len(original.namelist())==36
    files={info.filename:original.read(info.filename) for info in original.infolist()}
    o=files[OUT].decode()
    o=one(o,
        """        $hb_compact_original = $hb_verified_insurance_target
            && (($width===125 && $height===125)
                || ($width>=300 && $height>=250 && $ratio>=1.0 && $ratio<=1.4));""",
        """        // Original verified source dimensions. One central quality floor;
        // width and height NEVER become render-upscale requirements.
        $hb_original_flexible = $hb_verified_insurance_target
            && $width>=120 && $height>=60 && $ratio>=0.2 && $ratio<=12.0;""")
    o=one(o,
        """            // Existing page/category slots, original 300x250 or 125x125.
            // No stretching, no new slot, no tall skyscraper allowed.
            if ($hb_compact_original && in_array(sanitize_key((string)$slot_id),
                array('hub_after_cards','product_after_category_tiles'),true)) {
                $rule=array_merge($rule,array(
                    'ratio_min'=>0.8,'ratio_max'=>1.4,
                    'min_width'=>125,'min_height'=>125,
                    'crop'=>'contain','upscale_max'=>1.0,
                ));
            }""",
        """            // Use EXISTING insurance banner surfaces only. Aspect ratio
            // and intrinsic dimensions are handled once, at this source.
            // No resize-up, crop, new layout or semantic decision downstream.
            if ($hb_original_flexible && in_array(sanitize_key((string)$slot_id),
                array('start_after_topics','hub_after_cards','product_after_category_tiles'),true)) {
                $rule=array_merge($rule,array(
                    'ratio_min'=>0.2,'ratio_max'=>12.0,
                    'min_width'=>0,'min_height'=>0,
                    'crop'=>'contain','upscale_max'=>1.0,
                    '_hb_original_format_approved'=>true,
                ));
            }""")
    # Keep the existing safety checks. A format that the ONE central format
    # owner already approved must not be rejudged on shape in campaign write.
    o=one(o,
        """            || !$this->output_row_matches_slot_rule($row, $rule, 'banner')) {
            return false;
        }
        $payload = json_decode((string) ($row['payload'] ?? ''), true);""",
        """            || (empty($rule['_hb_original_format_approved'])
                && !$this->output_row_matches_slot_rule($row, $rule, 'banner'))) {
            return false;
        }
        $payload = json_decode((string) ($row['payload'] ?? ''), true);""")

    # The original global-compatible-slots function is for GENERAL fallback,
    # not an additional shape decider after exact verified Hab insurance.
    o=one(o,
        """                $compatible_banner_slots = $output_type === 'portal_banner'
                    ? $this->output_banner_compatible_slots($row,$portal)
                    : array();

                $target = is_array($classification['target'] ?? null) ? $classification['target'] : array();""",
        """                // For a ready Hab Tarifcheck original the chosen format
                // is decided below once by output_format_slot; the old global
                // compatible-slot scan is reserved for all other workflows.
                $hb_single_original = $output_type==='portal_banner'
                    && !empty($portal['local'])
                    && class_exists('PPAR_HB_Integration')
                    && $this->output_comparison_banner_partner($row)==='tarifcheck'
                    && sanitize_key((string)($classification['status']??''))==='ready';
                $compatible_banner_slots = $output_type === 'portal_banner' && !$hb_single_original
                    ? $this->output_banner_compatible_slots($row,$portal)
                    : array();

                $target = is_array($classification['target'] ?? null) ? $classification['target'] : array();""")

    # Remove RC36's duplicate placement mutation, replacing it with the
    # chosen format's saved position list – no second measuring pass.
    old="""                    // Existing R2 and R3/leaf slot surfaces share the same
                    // stored, once-verified insurance format decision.
                    if (in_array(sanitize_key((string)($classification['source']??'')),array(
                        'hab_insurance_specific_verified','hab_insurance_general_verified'),true)
                        && in_array(sanitize_key((string)($slot['slot_id']??'')),array(
                            'hub_after_cards','product_after_category_tiles'),true)) {
                        $compatible_banner_slots=array_values(array_unique(array_merge(
                            (array)$compatible_banner_slots,
                            array('hub_after_cards','product_after_category_tiles'))));
                    }
                    $classification['_ppar_banner_compatible_slots']=$compatible_banner_slots;"""
    new="""                    // ONE already-selected format. Save existing ancestor /
                    // descendant surfaces as part of that SAME decision.
                    if ($hb_single_original && !empty($slot['rule']['_hb_original_format_approved'])) {
                        $compatible_banner_slots=array_values(array_unique(array(
                            sanitize_key((string)($slot['slot_id']??'')),
                            'hub_after_cards','product_after_category_tiles',
                        )));
                    } elseif ($hb_single_original) {
                        // Credit/non-insurance Tarifcheck keeps original
                        // global compatibility logic untouched.
                        $compatible_banner_slots=$this->output_banner_compatible_slots($row,$portal);
                    }
                    $classification['_ppar_banner_compatible_slots']=$compatible_banner_slots;"""
    o=one(o,old,new)
    o=one(o,"$option='ppar_hab_rc37_tarifcheck_reconcile_v1';",
            "$option='ppar_hab_rc38_tarifcheck_reconcile_v1';")
    files[OUT]=o.encode()

    m=files[MAIN].decode()
    # These old shape fallback shortcuts may continue only for historic
    # uncategorized banners. A verified canonical banner always uses the
    # previously stored placement, not a post-hoc format test.
    for method in ('hb_insurance_original_wide_allowed','hb_insurance_original_inline_allowed'):
        anchor='    private function '+method+'($banner, $slot_type, $context) {'
        m=one(m,anchor,
        anchor+"""
        if(is_array($banner)
            && sanitize_key((string)($banner['source']??''))==='output_object_v4'
            && strpos((string)($banner['auto_topic_reason']??''),
                'HB_INSURANCE_CANONICAL:hab_insurance_')===0){
            // Already decided. Only campaign_slot_allowed() may read the
            // stored placement for canonical insurance creatives.
            return false;
        }""")
    m=one(m,'Version: 0.1.34-rc37','Version: 0.1.35-rc38')
    files[MAIN]=m.encode()

    c=files[CSS].decode()
    # The Pferde Atelier original intrinsic image sizing principle is
    # explicitly honored for BOTH normal and wide banner image markup.
    css=r'''
/* HAB RC38: once-approved insurance creative displays only at intrinsic or
   SMALLER size, without crop or new layout slots. Applies to 120x60, 234x60,
   120x600, 160x600, and older originals alike. No resize-up at any viewport. */
.ppar-hb-insurance-slot[data-ppar-slot] .ppar-banner-image,
.ppar-hb-insurance-slot[data-ppar-slot] .ppar-overview-wide-banner-image{
  display:block!important;
  width:auto!important;height:auto!important;
  min-width:0!important;min-height:0!important;
  max-width:100%!important;max-height:420px!important;
  object-fit:contain!important;object-position:center!important;
  margin-left:auto!important;margin-right:auto!important;
}
.ppar-hb-insurance-slot[data-ppar-slot] .ppar-overview-wide-banner-link{
  display:flex!important;align-items:center!important;justify-content:center!important;
  max-width:100%!important;height:auto!important;
}
'''
    assert "HAB RC38" not in c
    files[CSS]=(c.rstrip()+"\n"+css).encode()
    rd=files[README].decode()
    rd=one(rd,'Stable tag: 0.1.34-rc37','Stable tag: 0.1.35-rc38')
    files[README]=rd.encode()
    changed={OUT,MAIN,CSS,README}
    assert all(files[n]==original.read(n) for n in original.namelist() if n not in changed)
    b=BytesIO()
    with ZipFile(b,'w') as dst:
        for i in original.infolist():dst.writestr(i,files[i.filename])
    out=b.getvalue()
with ZipFile(BytesIO(out)) as check:
    assert check.testzip() is None and len(check.namelist())==36
    assert b"0.1.35-rc38" in check.read(MAIN)
    assert b"_hb_original_format_approved" in check.read(OUT)
    assert b"max-height:420px!important" in check.read(CSS)
P.write_bytes(out)
print("RC38_PFERDE_SINGLE_OWNER_NON_UPSCALING_BUILD_PASS",len(out),sha256(out).hexdigest())
