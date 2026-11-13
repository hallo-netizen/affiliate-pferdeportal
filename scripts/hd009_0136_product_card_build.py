#!/usr/bin/env python3
"""HD009 0.1.36: safe exact title/page relevance, real title facts and vertical multiprovider card markup.
Input exact full 0.1.35 current. No changes to feed import / affiliate matching / APIs.
"""
from pathlib import Path
from zipfile import ZipFile
import io,hashlib,sys
office=Path('protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE')
original=office/'CURRENT.zip'
expected='c30b3381928454671a8784f99c6bd59aaec79c800b9d38925462fc9dd29fe246'
sha=lambda b:hashlib.sha256(b).hexdigest()
assert sha(original.read_bytes())==expected
name='affiliate-portal-router/hobby-depot-affiliate-router.php'
with ZipFile(original) as z:
 assert z.testzip() is None and len(z.namelist())==41
 infos=z.infolist();files={i.filename:z.read(i.filename) for i in infos}
s=files[name].decode()
def once(a,b,tag):
 global s
 assert s.count(a)==1,tag+' actual_count='+str(s.count(a))
 s=s.replace(a,b,1)
# Instead of permitting older stale products selected only by inherited target keys,
# require the currently displayed product title to be a *direct* title-term match
# for the hobby page. This is the same no-extra-network / no-new-table data available
# in the existing campaign and context. It is intentionally fail-closed.
once("""        $target='page:'.$slug;
        foreach ((array)($campaign['automation_target_keys']??array()) as $raw_key) {
            if ((string)$raw_key===$target) { return true; }
        }
        return false;""",
"""        $target='page:'.$slug;
        $has_direct_target=false;
        foreach ((array)($campaign['automation_target_keys']??array()) as $raw_key) {
            if ((string)$raw_key===$target) { $has_direct_target=true; break; }
        }
        if (!$has_direct_target) { return false; }
        // A stored URL/target is not proof that the concrete merchandise fits
        // the hobby. Historical imports contained false Malene/Malen matches.
        // Require original title tokens of the hobby to occur as real title
        // tokens in the saved provider product (not substring in a surname).
        $topic=trim((string)($context['primary_name']??''));
        $product=trim((string)($campaign['title']??''));
        if ($topic==='' || $product==='') { return false; }
        $needed=$this->idealo_match_distinct_tokens($topic,true);
        if (!$needed) { return false; }
        $supplied=array();
        foreach ($this->idealo_match_tokens($product) as $token) {
            $supplied[$this->idealo_match_stem($token)]=true;
        }
        foreach ($needed as $token) {
            if (!isset($supplied[$this->idealo_match_stem($token)])) { return false; }
        }
        return true;""","direct concrete relevance")
# layout must be vertical within the actual provider HTML, not CSS attempting
# to override the browser's !important inline grid-template.
once("""? ' data-ppar-category-product-card="1" style="box-sizing:border-box!important;display:grid!important;grid-template-rows:150px minmax(210px,1fr)!important;align-items:stretch!important;width:100%!important;height:auto!important;min-height:360px!important;max-height:none!important;overflow:hidden!important"'""",
"""? ' data-ppar-category-product-card="1" style="box-sizing:border-box!important;display:grid!important;grid-template-columns:minmax(0,1fr)!important;grid-template-rows:188px minmax(190px,1fr)!important;align-items:stretch!important;width:100%!important;height:100%!important;min-height:390px!important;max-height:none!important;overflow:hidden!important"'""",
"category vertical inline grid")

facts=r'''    /** Only claims literally present in the product title; no fabricated features. */
    private function hd_category_card_title_facts($title) {
        $title=trim(wp_strip_all_tags((string)$title));
        if ($title==='') { return array(); }
        $facts=array();
        // Exact numeric specification, only if explicitly named in the title.
        if (preg_match('/(?<![0-9])([0-9]{1,3}(?:[.,][0-9]{1,2})?)\s*(mm|ml)\b/ui',$title,$m)) {
            $facts[]='Angabe: '.$m[1].' '.$m[2];
        }
        if (preg_match('/\b(starterset|komplettset|set|kit)\b/ui',$title,$m)) {
            $facts[]='Ausführung: '.$m[1];
        }
        if (preg_match('/\b(schwarz|weiss|weiß|blau|rot|grün|gruen|braun|beige|silber|gold|grau|gelb)\b/ui',$title,$m)) {
            $facts[]='Farbe: '.$m[1];
        }
        if (preg_match('/\b(edelstahl|baumwolle|aluminium|kunststoff|acryl|leder)\b/ui',$title,$m)) {
            $facts[]='Material: '.$m[1];
        }
        // A literal, domain-specific type in an actual product name.
        if (preg_match('/\b(airbrushpistole|airbrushkompressor|kompressor|spritzpistole|reinigungsset)\b/ui',$title,$m)) {
            $facts[]='Produkttyp: '.$m[1];
        }
        return array_slice(array_values(array_unique($facts)),0,3);
    }

'''
once("    private function render_banner($banner, $post_id, $context, $group, $slot_type) {",
facts+"    private function render_banner($banner, $post_id, $context, $group, $slot_type) {",
"real verified short product summary")
once("""            if ($title !== '') { $out .= '<strong class="ppar-banner-title">' . esc_html($title) . '</strong>'; }
            if ($description !== '') { $out .= '<span class="ppar-banner-description">' . esc_html($description) . '</span>'; }""",
"""            if ($title !== '') { $out .= '<strong class="ppar-banner-title">' . esc_html($title) . '</strong>'; }
            if ($creative_type === 'product' && $category_product_slot) {
                $facts=$this->hd_category_card_title_facts($title);
                if ($facts) {
                    $out.='<span class="ppar-product-facts"><strong class="ppar-product-facts-heading">Auf einen Blick</strong>';
                    foreach ($facts as $fact) { $out.='<span class="ppar-product-fact">• '.esc_html($fact).'</span>'; }
                    $out.='</span>';
                }
            }
            if ($description !== '') { $out .= '<span class="ppar-banner-description">' . esc_html($description) . '</span>'; }""",
"facts after real title before actions")
assert s.count('0.1.35')>=1
s=s.replace('0.1.35','0.1.36')
files[name]=s.encode()
with ZipFile(original) as z:
 diff=[k for k in files if files[k]!=z.read(k)]
 assert diff==[name],diff
out=Path(sys.argv[1] if len(sys.argv)>1 else '/tmp/HOBBY_DEPOT_HD009_0.1.36_PRODUCT_RELEVANCE_AND_BUTTONS.zip')
out.parent.mkdir(exist_ok=True,parents=True)
b=io.BytesIO()
with ZipFile(b,'w') as z:
 for i in infos:z.writestr(i,files[i.filename])
out.write_bytes(b.getvalue())
with ZipFile(out) as z:
 assert z.testzip() is None and len(z.namelist())==41
 assert b'Version: 0.1.36' in z.read(name)
print('HD009_0.1.36_SHA',sha(out.read_bytes()),'BYTES',out.stat().st_size,'CHANGED',diff)
