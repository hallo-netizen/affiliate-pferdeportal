#!/usr/bin/env python3
from pathlib import Path
from zipfile import ZipFile
from io import BytesIO
from hashlib import sha256
R=Path('protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ')
P=R/'PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip'
raw=P.read_bytes()
assert sha256(raw).hexdigest()=='8bcb3f60ddccfd6aaca547ff356cc0edb4602a22333c919cb42908c073461b64','Require exact RC35 ZIP'
B='affiliate-portal-router/'
main=B+'affiliate-portal-router.php'
out=B+'includes/trait-ppar-output-objects.php'
css=B+'assets/frontend.css'
readme=B+'readme.txt'
def one(src,old,new):
    n=src.count(old)
    assert n==1,('source unexpectedly changed',n,old[:180])
    return src.replace(old,new,1)
with ZipFile(BytesIO(raw)) as original:
    assert original.testzip() is None and len(original.namelist())==36
    files={x.filename:original.read(x.filename) for x in original.infolist()}
    o=files[out].decode()
    o=one(o,
    '''        $target_context = sanitize_key((string) ($target['context'] ?? ''));
        $matches = array();''',
    '''        $target_context = sanitize_key((string) ($target['context'] ?? ''));
        // One existing import-time format decision, after the ONLY topic
        // assignment. No new theme/partner choices during public rendering.
        $hb_verified_insurance_target = $creative_type === 'banner'
            && !empty($portal['local'])
            && method_exists($this, 'hb_insurance_scope')
            && $this->hb_insurance_scope(array(
                'post_type'=>$target_type,
                'post_id'=>absint($target['id']??0),
                'term_ids'=>$target_type==='category'
                    ? array(absint($target['id']??0)) : array(),
            ))==='insurance';
        $hb_compact_original = $hb_verified_insurance_target
            && (($width===125 && $height===125)
                || ($width>=300 && $height>=250 && $ratio>=1.0 && $ratio<=1.4));
        $matches = array();''')
    o=one(o,
    '''        foreach ($matrix as $slot_id => $rule) {
            if (!is_array($rule) || sanitize_key((string) ($rule['creative_type'] ?? '')) !== $creative_type) { continue; }''',
    '''        foreach ($matrix as $slot_id => $rule) {
            if (!is_array($rule) || sanitize_key((string) ($rule['creative_type'] ?? '')) !== $creative_type) { continue; }
            // Existing page/category slots, original 300x250 or 125x125.
            // No stretching, no new slot, no tall skyscraper allowed.
            if ($hb_compact_original && in_array(sanitize_key((string)$slot_id),
                array('hub_after_cards','product_after_category_tiles'),true)) {
                $rule=array_merge($rule,array(
                    'ratio_min'=>0.8,'ratio_max'=>1.4,
                    'min_width'=>125,'min_height'=>125,
                    'crop'=>'contain','upscale_max'=>1.0,
                ));
            }''')
    marker='''                if ($output_type === 'portal_banner'
                    && $status === 'ready'
                    && sanitize_key((string) ($classification['source'] ?? '')) !== 'manual_fixed_target') {'''
    o=one(o,marker,
    '''                // One stored insurance target may span real R2/R3/leaf
                // render surfaces. Save the compatible ORIGINAL slot names.
                if ($output_type === 'portal_banner' && $status === 'ready'
                    && in_array(sanitize_key((string)($classification['source']??'')),array(
                        'hab_insurance_specific_verified','hab_insurance_general_verified'),true)
                    && in_array(sanitize_key((string)($slot['slot_id']??'')),array(
                        'hub_after_cards','product_after_category_tiles'),true)) {
                    $compatible_banner_slots=array_values(array_unique(array_merge(
                        (array)$compatible_banner_slots,
                        array('hub_after_cards','product_after_category_tiles'))));
                }

'''+marker)
    o=one(o,"$option='ppar_hab_rc35_tarifcheck_reconcile_v1';","$option='ppar_hab_rc36_tarifcheck_reconcile_v1';")
    files[out]=o.encode()
    m=files[main].decode()
    m=one(m,
    '''    private function campaign_matches_contract_slot_rule($campaign, $slot_type) {
        $rule = $this->runtime_contract_slot_rule($slot_type);''',
    '''    private function campaign_matches_contract_slot_rule($campaign, $slot_type) {
        if (is_array($campaign)
            && sanitize_key((string)($campaign['source']??''))==='output_object_v4'
            && sanitize_key((string)($campaign['creative_type']??''))==='banner'
            && strpos((string)($campaign['auto_topic_reason']??''),
                 'HB_INSURANCE_CANONICAL:hab_insurance_')===0) {
            // Read the ONE stored approved format/placement, not a new
            // second topic/format choice. Security gates stay unchanged.
            $places=array_map('sanitize_key',(array)($campaign['placements']??array()));
            return in_array(sanitize_key((string)$slot_type),$places,true)
                && trim((string)($campaign['image_url']??''))!==''
                && sanitize_key((string)($campaign['render_mode']??'image_link'))==='image_link'
                && (bool)preg_match('/^[1-9][0-9]*x[1-9][0-9]*$/',
                                    (string)($campaign['dimensions']??''));
        }
        $rule = $this->runtime_contract_slot_rule($slot_type);''')
    m=one(m,'Version: 0.1.32-rc35','Version: 0.1.33-rc36')
    files[main]=m.encode()
    c=files[css].decode()
    c=one(c,
    '''/* HAB RC19: native insurer rectangles and small squares; no stretched banners. */
.ppar-hb-insurance-slot[data-ppar-slot="post_inline_banner"] .ppar-banner-image,''',
    '''/* Insurance only: real category and article slots display intrinsic
   125x125 / 300x250 as contained art, without layout change elsewhere. */
.ppar-hb-insurance-slot[data-ppar-slot="hub_after_cards"] .ppar-banner-image,
.ppar-hb-insurance-slot[data-ppar-slot="product_after_category_tiles"] .ppar-banner-image,
.ppar-hb-insurance-slot[data-ppar-slot="post_inline_banner"] .ppar-banner-image,''')
    files[css]=c.encode()
    rd=files[readme].decode()
    rd=one(rd,'Stable tag: 0.1.32-rc35','Stable tag: 0.1.33-rc36')
    files[readme]=rd.encode()
    changed={main,out,css,readme}
    assert all(files[n]==original.read(n) for n in original.namelist() if n not in changed)
    buf=BytesIO()
    with ZipFile(buf,'w') as z:
        for x in original.infolist():z.writestr(x,files[x.filename])
    new=buf.getvalue()
with ZipFile(BytesIO(new)) as z:
    assert z.testzip() is None and len(z.namelist())==36
    assert b'0.1.33-rc36' in z.read(main)
    assert b'ppar_hab_rc36_tarifcheck_reconcile_v1' in z.read(out)
P.write_bytes(new)
print('HAB_RC36_SINGLE_IMPORT_FORMAT_BUILD_PASS',len(new),sha256(new).hexdigest())
