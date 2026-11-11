#!/usr/bin/env python3
"""Build HAB-004 RC19 from exactly approved HAB-004 RC18, insurance-only routing.
No new DB tables, frontend HTTP calls, category writes, or external plugin changes.
"""
from pathlib import Path
from zipfile import ZipFile
from io import BytesIO
import hashlib
root=Path('protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ')
archive=root/'PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip'
original=archive.read_bytes()
hash_sha=lambda b:hashlib.sha256(b).hexdigest()
assert hash_sha(original)=='a98063820d1564bf7cc7312c4c232369ac198bbaa49fbb6b173f76cd5096da89', 'Unknown RC18 base; no overwrite'
prefix='affiliate-portal-router/'
main=prefix+'affiliate-portal-router.php'
amazon=prefix+'includes/trait-ppar-hb-amazon.php'
css=prefix+'assets/frontend.css'
readme=prefix+'readme.txt'
def replace_one(s,old,new):
    count=s.count(old)
    assert count==1,('ANCHOR_MISMATCH',old[:100],count)
    return s.replace(old,new,1)
helper=r'''
    /**
     * HAB-004 RC19: classify the already verified, active category tree.
     * All five R2, 46 R3 and flat WP category leaves inherit the insurance root.
     * No additional WordPress query; the existing snapshot is request-cached.
     */
    private function hb_insurance_scope($context) {
        static $memo = array();
        static $ancestry = null;
        if (!is_array($context) || !class_exists('PPAR_HB_Integration')) { return 'other'; }
        $nodes = PPAR_HB_Integration::verified_nodes();
        $root = 'core:world:insurance';
        if (!is_array($nodes) || !isset($nodes[$root])) { return 'other'; }
        if ($ancestry === null) {
            $ancestry = array();
            foreach ($nodes as $key => $row) {
                $at = $row;
                $seen = array();
                $result = 'other';
                for ($i = 0; $i < 18 && is_array($at) && !empty($at['id']); $i++) {
                    $id = (string)$at['id'];
                    if (isset($seen[$id])) { break; }
                    $seen[$id] = true;
                    if ($id === $root) { $result = 'insurance'; break; }
                    $at = $nodes[(string)($at['parent'] ?? '')] ?? array();
                }
                $ancestry[$key] = $result;
            }
        }
        $type = sanitize_key((string)($context['post_type'] ?? ''));
        $post_id = absint($context['post_id'] ?? 0);
        $term_ids = array_values(array_unique(array_filter(array_map('absint', (array)($context['term_ids'] ?? array())))));
        $verified_id = (string)($context['hb_verified_node_id'] ?? '');
        $fingerprint = md5($type.'|'.$post_id.'|'.$verified_id.'|'.implode(',', $term_ids));
        if (isset($memo[$fingerprint])) { return $memo[$fingerprint]; }
        $insurance = false; $other = false;
        $is_term = in_array($type, array('post','category','category_archive'), true);
        foreach ($nodes as $key => $row) {
            if ($is_term) {
                if (($row['type'] ?? '') !== 'category' ||
                    !in_array(absint($row['wp_id'] ?? 0), $term_ids, true)) { continue; }
            } else {
                if (($row['type'] ?? '') !== 'page' ||
                    (($verified_id !== '' && $key !== $verified_id) &&
                      ($post_id < 1 || absint($row['wp_id'] ?? 0) !== $post_id))) { continue; }
                if ($verified_id === '' && ($post_id < 1 || absint($row['wp_id'] ?? 0) !== $post_id)) { continue; }
            }
            if (($ancestry[$key] ?? 'other') === 'insurance') { $insurance = true; }
            else { $other = true; }
        }
        return $memo[$fingerprint] = ($insurance && $other ? 'mixed' : ($insurance ? 'insurance' : 'other'));
    }

    /**
     * Only an existing, approved insurance-network banner with evidence of
     * actual destination / topic may fill an insurance slot. No generic shop,
     * financing, product or global low-rank fallback is allowed.
     */
    private function hb_insurance_campaign_allowed($campaign, $context, $slot_type) {
        $scope = $this->hb_insurance_scope($context);
        if ($scope === 'other') { return true; }
        if ($scope !== 'insurance' || !is_array($campaign)) { return false; }
        $creative = sanitize_key((string)($campaign['creative_type'] ?? ''));
        $network = sanitize_key((string)($campaign['network'] ?? ''));
        if ($creative !== 'banner' || !in_array($network, array('direct','awin','adcell'), true)) { return false; }
        $slot = sanitize_key((string)$slot_type);
        if (preg_match('/(?:^|_)(?:product|products)(?:_|$)/', $slot) && $slot !== 'product_after_category_tiles') { return false; }
        $labels = array();
        foreach (array('name','title','partner','source','description') as $field) {
            $value = $campaign[$field] ?? '';
            if (is_scalar($value) && $value !== '') { $labels[]=(string)$value; }
        }
        $identity = strtolower(remove_accents(implode(' ', $labels)));
        if (preg_match('/(?:girokonto|baufinanzierung|kreditkarte|kreditvergleich|kreditrechner|stromtarif|gastarif|dsl-vertrag|shopping)/', $identity)) { return false; }
        if (!preg_match('/(?:tarifcheck|versicherung|insurance|haftpflicht|rechtsschutz|hausrat|wohngebaude|kfz|motorrad|pflegezusatz|berufsunfahigkeit|rente|unfall|pkv|firmenschutz)/', $identity)) { return false; }
        if (sanitize_key((string)($campaign['assignment_mode'] ?? '')) === 'fallback') { return false; }
        $post_id = absint($context['post_id'] ?? 0);
        $type = sanitize_key((string)($context['post_type'] ?? ''));
        $page_id = absint($campaign['page_id'] ?? 0);
        if ($page_id > 0 && $type === 'page' && $page_id === $post_id) { return true; }
        // An actually approved, general insurance comparison may cover all
        // descendants, but never general finance or one named sub-insurance
        // masquerading as a universal insurance advertisement.
        if ($page_id > 0 && !empty($campaign['match_descendants'])
            && class_exists('PPAR_HB_Integration')) {
            $verified_nodes=PPAR_HB_Integration::verified_nodes();
            $root_id=absint($verified_nodes['core:world:insurance']['wp_id']??0);
            $general=(bool)preg_match('/(?:versicherungsvergleich|versicherungen vergleichen|versicherungsarten|versicherungsschutz vergleichen)/',$identity);
            $special=(bool)preg_match('/(?:hausrat|wohngebaude|motorrad|kfz|haftpflicht|rechtsschutz|pflegezusatz|berufsunfahigkeit|kranken|pkv|renten|risikoleben|tierhalter|gewerbe|firmenversicherung)/',$identity);
            if ($page_id===$root_id && $general && !$special) { return true; }
        }
        $slugs = array_map('sanitize_key', (array)($context['slugs'] ?? array()));
        if (array_intersect((array)($campaign['match_slugs'] ?? array()), $slugs)) { return true; }
        $term_ids = array_map('absint', (array)($context['term_ids'] ?? array()));
        if (array_intersect((array)($campaign['match_term_ids'] ?? array()), $term_ids)) { return true; }
        $context_target_keys = array_merge(
            array((string)($context['semantic_primary_target_key'] ?? '')),
            (array)($context['semantic_ancestor_target_keys'] ?? array())
        );
        if (array_intersect((array)($campaign['automation_target_keys'] ?? array()), $context_target_keys)) { return true; }
        // Existing posts can inherit a campaign booked on their actual
        // verified R3 parent, never from an unrelated or guessed title.
        if ($type === 'post' && $page_id > 0 && $term_ids && class_exists('PPAR_HB_Integration')) {
            $nodes = PPAR_HB_Integration::verified_nodes();
            foreach ($nodes as $node) {
                if (($node['type'] ?? '') !== 'category' || !in_array(absint($node['wp_id'] ?? 0), $term_ids, true)) { continue; }
                $at = $node; $seen = array();
                for ($i = 0; $i < 18 && is_array($at) && !empty($at['id']); $i++) {
                    $key = (string)$at['id'];
                    if (isset($seen[$key])) { break; }
                    $seen[$key] = true;
                    if (($at['type'] ?? '') === 'page' && absint($at['wp_id'] ?? 0) === $page_id) { return true; }
                    $at = $nodes[(string)($at['parent'] ?? '')] ?? array();
                }
            }
        }
        return false;
    }

    /** RC19 narrowly permits the real 728x90 / 468x60 Tarifcheck originals in
     * the existing insurer wide slots. All six old worlds retain old geometry. */
    /** Actual 300x250 rectangle and 125x125 small square in insurance
     * article/glossary slots, preserving their original dimensions. */
    /**
     * Guaranteed in-house topic card for an empty existing insurance banner
     * slot. Not an affiliate creative: only current verified WordPress pages.
     */
    private function hb_insurance_house_banner($context, $slot_type) {
        if ($this->hb_insurance_scope($context) !== 'insurance'
            || !class_exists('PPAR_HB_Integration')) { return ''; }
        $slot=sanitize_key((string)$slot_type);
        $slots=array('hub_after_cards','product_after_category_tiles',
            'category_recommendation','post_inline_banner',
            'glossary_single_banner','glossary_single_desktop_banner',
            'glossary_single_mobile_banner');
        if (!in_array($slot,$slots,true)) { return ''; }
        $nodes=PPAR_HB_Integration::verified_nodes();
        $root='core:world:insurance';
        if (!is_array($nodes) || empty($nodes[$root]['wp_id'])) {return '';}
        $current=array();
        $post_id=absint($context['post_id'] ?? 0);
        $verified=(string)($context['hb_verified_node_id'] ?? '');
        if ($verified!=='' && !empty($nodes[$verified])) { $current=$nodes[$verified]; }
        if (!$current && $post_id > 0 && sanitize_key((string)($context['post_type'] ?? ''))==='page') {
            foreach ($nodes as $node) {
                if (($node['type']??'')==='page' && absint($node['wp_id']??0)===$post_id) {
                    $current=$node;break;
                }
            }
        }
        if (!$current) {
            $terms=array_map('absint',(array)($context['term_ids']??array()));
            foreach ($nodes as $node) {
                if (($node['type']??'')==='category'
                    && in_array(absint($node['wp_id']??0),$terms,true)) {
                    $current=$node;break;
                }
            }
        }
        $target=$nodes[$root];
        $current_id=(string)($current['id']??'');
        if ($current_id===$root) {
            foreach ($nodes as $node) {
                if (($node['type']??'')==='page' && ($node['parent']??'')===$root) {
                    $target=$node;break;
                }
            }
        } elseif ($current_id!=='') {
            $cursor=$current;$seen=array();
            for ($i=0;$i<18 && !empty($cursor['id']);$i++) {
                $key=(string)$cursor['id'];
                if (isset($seen[$key])) {break;}
                $seen[$key]=true;
                if (($cursor['parent']??'')===$root && ($cursor['type']??'')==='page') {
                    $target=$cursor;break;
                }
                $cursor=$nodes[(string)($cursor['parent']??'')]??array();
            }
            if (absint($target['wp_id']??0)===$post_id) { $target=$nodes[$root]; }
        }
        $link=function_exists('get_permalink') ? get_permalink(absint($target['wp_id'])) : '';
        if (!is_string($link) || $link==='') {return '';}
        $topic=sanitize_text_field((string)($target['name']??'Versicherungen'));
        $wide=in_array($slot,array('hub_after_cards','product_after_category_tiles','category_recommendation'),true);
        $class=$wide?'ppar-hb-insurance-own-wide':'ppar-hb-insurance-own-compact';
        return '<div class="ppar-affiliate-slot ppar-hb-insurance-own '.$class.'" data-ppar-slot="'.esc_attr($slot).'">'
            .'<span class="ppar-hb-insurance-own-label">Eigener Themenhinweis</span>'
            .'<a class="ppar-hb-insurance-own-link" href="'.esc_url($link).'">'
            .'<strong>Versicherungsschutz passend auswählen</strong>'
            .'<span>Informationen und Vergleiche zum Themenbereich '.esc_html($topic).'</span>'
            .'<span class="ppar-hb-insurance-own-cta">Zum Themenbereich</span>'
            .'</a></div>';
    }

    private function hb_insurance_original_inline_allowed($banner, $slot_type, $context) {
        $slot=sanitize_key((string)$slot_type);
        if ($this->hb_insurance_scope($context)!=='insurance'
            || !in_array($slot,array('post_inline_banner','glossary_single_desktop_banner',
                                     'glossary_single_mobile_banner','glossary_single_banner'),true)
            || !is_array($banner) || empty($banner['image_url'])
            || sanitize_key((string)($banner['creative_type']??''))!=='banner'
            || sanitize_key((string)($banner['render_mode']??'image_link'))==='html') { return false; }
        list($width,$height,$source)=$this->article_banner_dimensions($banner);
        $w=absint($width);$h=absint($height);
        if ($source==='fallback' || $w<125 || $h<125) {return false;}
        return ($w>=300 && $h>=250 && $w/$h>=1.0 && $w/$h<=1.4)
            || ($w===125 && $h===125);
    }

    private function hb_insurance_original_wide_allowed($banner, $slot_type, $context) {
        if ($this->hb_insurance_scope($context) !== 'insurance'
            || !$this->overview_wide_banner_slot($slot_type)
            || !is_array($banner) || empty($banner['image_url'])
            || sanitize_key((string)($banner['creative_type'] ?? '')) !== 'banner'
            || sanitize_key((string)($banner['mode'] ?? 'image_link')) === 'html') { return false; }
        list($width, $height, $source) = $this->article_banner_dimensions($banner);
        $w=absint($width); $h=absint($height);
        if ($source === 'fallback' || $w < 468 || $h < 60 || $h > 180) { return false; }
        $ratio=$w/$h;
        return $ratio>=5.0 && $ratio<=12.0;
    }

'''
with ZipFile(BytesIO(original)) as src:
    assert len(src.namelist())==36 and src.testzip() is None
    original_map={f.filename:src.read(f.filename) for f in src.infolist()}
    s=original_map[main].decode('utf-8')
    s=replace_one(s, "Version: 0.1.15-rc18", "Version: 0.1.16-rc19")
    # New methods are private and affect only verified insurance descendants.
    s=replace_one(s, "    /** Read the existing approved article campaigns. No demo items or HTTP. */", helper+"    /** Read the existing approved article campaigns. No demo items or HTTP. */")
    # The insurance article uses the existing banner selector, not a stale
    # hybrid plan that may contain an Amazon/physical-product campaign.
    anchor="        if (get_post_type($post_id)!=='post' || get_post_status($post_id)!=='publish') { return ''; }\n        // The live Hab template owns placement"
    new="        if (get_post_type($post_id)!=='post' || get_post_status($post_id)!=='publish') { return ''; }\n        $insurance_scope=$this->hb_insurance_scope($this->get_content_context($post_id));\n        if ($insurance_scope !== 'other') {\n            return $insurance_scope === 'insurance' && $kind === 'banner'\n                ? $this->render_affiliate_slot($post_id,'post_inline_banner','primary_product','')\n                : ($kind === 'products' ? '<!-- HAB insurance: no product cards or demo products -->' : '');\n        }\n        // The live Hab template owns placement"
    s=replace_one(s,anchor,new)
    # Existing Hab area slots must not run post-selection Amazon product fallback.
    anchor="        if ($type==='') { return ''; }\n        if ($kind==='banner'"
    new="        if ($type==='') { return ''; }\n        if ($kind==='products' && $this->hb_insurance_scope($context)!=='other') { return '<!-- HAB insurance: no physical product cards -->'; }\n        if ($kind==='banner'"
    s=replace_one(s,anchor,new)
    # Guard all assigned and automatically selected campaigns and all their
    # no-campaign fallbacks, without altering unrelated portal ranking.
    anchor="    private function render_affiliate_slot_for_context($content_id, $context, $slot_type, $intent, $forced_group_id = '') {\n        if ($this->is_enabled()) {"
    new="    private function render_affiliate_slot_for_context($content_id, $context, $slot_type, $intent, $forced_group_id = '') {\n        $hb_insurance_scope = $this->hb_insurance_scope($context);\n        if ($hb_insurance_scope === 'mixed') { return ''; }\n        if ($hb_insurance_scope === 'insurance' && (preg_match('/^(?:category|hub|journal)_product_[123]$/', sanitize_key((string)$slot_type)) || sanitize_key((string)$slot_type)==='post_bottom_products')) { return ''; }\n        if ($this->is_enabled()) {"
    s=replace_one(s,anchor,new)
    anchor="            if ($selection && !empty($selection['campaign'])) {\n                list($group, $banner) = $this->campaign_to_group_banner($selection['campaign']);"
    new="            if ($selection && !empty($selection['campaign'])\n                && !$this->hb_insurance_campaign_allowed($selection['campaign'],$context,$slot_type)) { $selection=null; }\n            if ($selection && !empty($selection['campaign'])) {\n                list($group, $banner) = $this->campaign_to_group_banner($selection['campaign']);"
    s=replace_one(s,anchor,new)
    anchor="        // When no real campaign exists, show only a tracked Amazon search link\n        // for an explicitly known Hab product-family category."
    new="        // RC19: no Amazon, physical-product, placeholder, or unapproved\n        // partner fallback anywhere inside insurance; no fabricated ads.\n        if ($hb_insurance_scope === 'insurance') { return $this->hb_insurance_house_banner($context,$slot_type); }\n        // When no real campaign exists, show only a tracked Amazon search link\n        // for an explicitly known Hab product-family category."
    s=replace_one(s,anchor,new)
    # The original generic banner-selection gate excludes ALL manually entered
    # direct campaigns from automatic selection, allowing Creative Library only.
    # For the specifically scoped insurer world, allow a verified approved
    # direct/Awin/ADCELL campaign through the existing ranker. Everywhere else
    # the original Creative Library-only rule remains unchanged.
    anchor="""            if ($required_type === 'banner' && $forced_campaign_id_norm === ''
                && (string)($runtime_campaign['source'] ?? '') !== 'output_object_v4') { continue; }"""
    fixed="""            if ($required_type === 'banner' && $forced_campaign_id_norm === ''
                && (string)($runtime_campaign['source'] ?? '') !== 'output_object_v4'
                && !($this->hb_insurance_scope($rank_context)==='insurance'\n                     && $this->hb_insurance_campaign_allowed($runtime_campaign,$rank_context,$slot_type))) { continue; }"""
    s=replace_one(s,anchor,fixed)
    # Format validation still runs for every campaign. In the insurance world
    # alone it may accept genuine 728x90 or 468x60 originals at wide slots.
    anchor="                if (!$this->campaign_slot_allowed($runtime_campaign, $slot_type)) { continue; }"
    fixed="                if (!$this->campaign_slot_allowed($runtime_campaign, $slot_type)\n                    && !$this->hb_insurance_original_wide_allowed($runtime_campaign,$slot_type,$rank_context)\n                    && !$this->hb_insurance_original_inline_allowed($runtime_campaign,$slot_type,$rank_context)) { continue; }"
    s=replace_one(s,anchor,fixed)
    # Candidate ranking is filtered BEFORE choosing the first campaign, so
    # one unrelated brand never displaces an eligible lower-ranked insurer.
    anchor="    private function campaign_match_rank($campaign, $context) {\n        $mode ="
    new="    private function campaign_match_rank($campaign, $context) {\n        if (!$this->hb_insurance_campaign_allowed($campaign,$context,(string)($context['slot_type'] ?? ''))) { return null; }\n        $mode ="
    s=replace_one(s,anchor,new)
    # Extra ranking tier for a documented and approved "all insurances"
    # programme on the root; never make a generic partner beat an exact match.
    anchor="        $mode = isset($campaign['_ppar_norm_assignment_mode'])"
    pre_rank="        // General approved insurance umbrella campaign only as a lower-ranked\\n        // genuine partner alternative; exact topic campaigns always beat it.\\n        if ($this->hb_insurance_scope($context)==='insurance') {\\n            $name=strtolower(remove_accents((string)($campaign['name']??'').' '.(string)($campaign['title']??'')));\\n            $nodes=class_exists('PPAR_HB_Integration')?PPAR_HB_Integration::verified_nodes():array();\\n            $root_page=absint($nodes['core:world:insurance']['wp_id']??0);\\n            if ($root_page>0 && absint($campaign['page_id']??0)===$root_page\\n                && !empty($campaign['match_descendants'])\\n                && preg_match('/(?:versicherungsvergleich|versicherungen vergleichen|versicherungsarten|versicherungsschutz vergleichen)/',$name)\\n                && !preg_match('/(?:hausrat|wohngebaude|motorrad|kfz|haftpflicht|rechtsschutz|pflegezusatz|berufsunfahigkeit|pkv|tierhalter|firmenversicherung)/',$name)) {\\n                return array('specificity'=>125,'matches'=>1,'reason'=>'Allgemeiner bestätigter Versicherungsvergleich, nach konkreten Angeboten.');\\n            }\\n        }\\n"
    s=replace_one(s,anchor,pre_rank+anchor)
    # Existing overview banners required original >=800 px; genuine 728x90
    # and 468x60 partner banners become eligible ONLY within insurance root.
    anchor="if ($image_url === '' || !$this->overview_wide_banner_campaign_eligible($banner, $slot_type)) { return ''; }"
    new="if ($image_url === '' || !($this->hb_insurance_original_wide_allowed($banner, $slot_type, $context) || $this->overview_wide_banner_campaign_eligible($banner, $slot_type))) { return ''; }"
    s=replace_one(s,anchor,new)
    # Add a class only for insurance output, so existing six-world CSS stays
    # identical. No additional stylesheet or front-end network call.
    anchor="                        if ($is_overview_wide_banner_slot) { $classes[] = 'ppar-overview-wide-banner-slot'; }"
    fixed="                        if ($hb_insurance_scope==='insurance') { $classes[]='ppar-hb-insurance-slot'; }\n"+anchor
    s=replace_one(s,anchor,fixed)
    # Eliminate the historical insurance-document-bag disguised as an Amazon
    # insurance recommendation. Other six worlds and their image identities
    # remain identical.
    t=original_map[amazon].decode('utf-8')
    t=replace_one(t,"            array('/versicherung|haftpflicht|rechtsschutz|vorsorge/','Feuerfeste Dokumententasche Versicherungsunterlagen'),\n","")
    t=replace_one(t,"            'core:world:insurance'=>'Feuerfeste Dokumententasche Versicherungsunterlagen',\n","")
    t=replace_one(t,"            'core:world:insurance'=>'hb-amazon-kategorie-tresore.webp',\n","")
    # The original HB house generator can only produce six physical-protection worlds.
    # Keep original house banners; only insurer article/glossary creatives are
    # constrained to intrinsic aspect and no upscaling.
    original_map[css] += b"""
/* HAB RC19: native insurer rectangles and small squares; no stretched banners. */
.ppar-hb-insurance-slot[data-ppar-slot="post_inline_banner"] .ppar-banner-image,
.ppar-hb-insurance-slot[data-ppar-slot^="glossary_single"] .ppar-banner-image{
    display:block!important;width:auto!important;height:auto!important;
    max-width:100%!important;max-height:250px!important;
    object-fit:contain!important;margin:0 auto!important;
}

/* Empty insurer ad slots: internal non-commercial thematic banner. */
.ppar-hb-insurance-own{display:block;box-sizing:border-box;background:#edf2ed;
border:1px solid #cbd9cd;border-radius:9px;padding:12px 16px;color:#203d31;max-width:100%;overflow:hidden}
.ppar-hb-insurance-own-label{display:block;font-size:11px;letter-spacing:.02em;color:#496354;margin-bottom:6px}
.ppar-hb-insurance-own-link{display:flex;flex-wrap:wrap;align-items:center;gap:6px 14px;
text-decoration:none!important;color:inherit!important}
.ppar-hb-insurance-own-link strong{font-size:17px;font-weight:700}
.ppar-hb-insurance-own-link span{font-size:14px}
.ppar-hb-insurance-own-cta{margin-left:auto;border:1px solid #8ea993;padding:6px 12px;
border-radius:5px;font-weight:600;white-space:nowrap}
.ppar-hb-insurance-own-link:hover .ppar-hb-insurance-own-cta{background:#d9e7db}
.ppar-hb-insurance-own-compact .ppar-hb-insurance-own-link{display:flex;flex-direction:column;align-items:flex-start}
.ppar-hb-insurance-own-compact .ppar-hb-insurance-own-cta{margin-left:0}
@media(max-width:600px){.ppar-hb-insurance-own-link{flex-direction:column;align-items:flex-start}
.ppar-hb-insurance-own-cta{margin-left:0}}
"""
    original_map[main]=s.encode('utf-8')
    original_map[amazon]=t.encode('utf-8')
    original_map[readme]=replace_one(original_map[readme].decode('utf-8'),"Stable tag: 0.1.15-rc18","Stable tag: 0.1.16-rc19").encode('utf-8')
    assert s.count("hb_insurance_campaign_allowed(")==4
    assert "core:world:insurance'=>'hb-amazon-kategorie-tresore.webp'" not in t
    assert "Feuerfeste Dokumententasche Versicherungsunterlagen" not in t
    changed={main,amazon,css,readme}
    for n in src.namelist():
        if n not in changed:assert original_map[n]==src.read(n)
    out=BytesIO()
    with ZipFile(out,'w') as dest:
        for member in src.infolist():
            dest.writestr(member,original_map[member.filename])
    payload=out.getvalue()
with ZipFile(BytesIO(payload)) as test:
    assert test.testzip() is None and len(test.namelist())==36
archive.write_bytes(payload)
print('HAB-004-RC19 CREATED',len(payload),'SHA256',hash_sha(payload),'FILES',len(original_map),'CHANGED',sorted(x.replace(prefix,'') for x in changed))
