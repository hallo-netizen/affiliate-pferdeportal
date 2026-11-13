#!/usr/bin/env python3
"""HD009 0.1.37: common last-render Idealo relevance gate + factual bullet facts.

Build full plugin from exact 0.1.36 CURRENT. No new tables, front-end calls,
feed changes, altered Amazon/eBay flows, or WordPress core.
"""
from pathlib import Path
from zipfile import ZipFile
import hashlib,io,sys
office=Path('protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE')
base=office/'CURRENT.zip'
sha=lambda x:hashlib.sha256(x).hexdigest()
expected='c5207290e535aaad03f26713d4e39b59836475e63cfeff9d57dc04a53944ca68'
assert sha(base.read_bytes())==expected,'Abort: original HD009 0.1.36 source checksum mismatch'
name='affiliate-portal-router/hobby-depot-affiliate-router.php'
with ZipFile(base) as z:
    assert z.testzip() is None and len(z.namelist())==41
    infos=z.infolist()
    data={i.filename:z.read(i.filename) for i in infos}
s=data[name].decode('utf8')
def exact(old,new,label):
    global s
    assert s.count(old)==1,f'{label} anchor exists {s.count(old)} times'
    s=s.replace(old,new,1)
# Selection step only checks exact target for idealo; don't make business-type
# source values a loophole. Product factual verification occurs at LAST output.
start=s.index('    private function hd_idealo_product_targets_exact_hobby_page(')
end=s.index('    private function category_product_shared_rank_base(',start)
assert s.count('private function hd_idealo_product_targets_exact_hobby_page(')==1
existing=s[start:end]
assert 'idealo_product_feed_v1' in existing and 'idealo_match_distinct_tokens' in existing
replacement=r'''    /**
     * Already-existing exact target check; every Idealo product source uses
     * it, including previously materialized campaigns. No child inheritance.
     */
    private function hd_idealo_product_targets_exact_hobby_page($campaign, $context, $slot_type) {
        if (!preg_match('/^category_product_[123]$/', sanitize_key((string)$slot_type))) { return true; }
        if (sanitize_key((string)($campaign['network']??''))!=='idealo') { return true; }
        if (sanitize_key((string)($context['post_type']??''))!=='page') { return true; }
        $slug=sanitize_title((string)($context['primary_slug']??''));
        if ($slug==='') { return false; }
        $target='page:'.$slug;
        foreach ((array)($campaign['automation_target_keys']??array()) as $key) {
            if ((string)$key===$target) { return true; }
        }
        return false;
    }

'''
s=s[:start]+replacement+s[end:]

# Last and only topical check, after ranking, directly before rendered product
# HTML: a stale cached/alternate output path cannot let non-topic Idealo
# merchandise appear on any Hobby *page*.
topical=r'''    /** Public-safe text evidence, no API/DB access and no fuzzy substring. */
    private function hd_idealo_category_title_relevant($title,$context) {
        $title=trim(wp_strip_all_tags((string)$title));
        $topic=trim((string)($context['primary_name']??''));
        if ($topic==='') { $topic=str_replace('-', ' ',sanitize_title((string)($context['primary_slug']??''))); }
        if ($title==='' || $topic==='') { return false; }
        $need=$this->idealo_match_distinct_tokens($topic,true);
        if (!$need) { return false; }
        $found=array();
        foreach ($this->idealo_match_tokens($title) as $word) {
            $found[$this->idealo_match_stem($word)]=true;
        }
        foreach ($need as $word) {
            if (!isset($found[$this->idealo_match_stem($word)])) { return false; }
        }
        return true;
    }

'''
exact("    private function render_banner($banner, $post_id, $context, $group, $slot_type) {",
      topical+"    private function render_banner($banner, $post_id, $context, $group, $slot_type) {",
      "insert final common output check")
exact("""        $category_product_slot = (bool) preg_match('/^category_product_[123]$/', sanitize_key((string)$slot_type));
        $category_product_wrap_attr = $category_product_slot""",
"""        $category_product_slot = (bool) preg_match('/^category_product_[123]$/', sanitize_key((string)$slot_type));
        // Final shared output gate: checked here, not only in a preferred
        // candidate route. Product source labels may change across versions.
        // No image placeholder may stand in for a missing real product photo.
        if ($category_product_slot && $creative_type==='product' && $network==='idealo'
            && sanitize_key((string)($context['post_type']??''))==='page'
            && ($image_url==='' || !$this->hd_idealo_category_title_relevant($title,$context))) {
            return '';
        }
        $category_product_wrap_attr = $category_product_slot""",
      "actual render_banner guard")

# Replace conditional title-only facts with a grounded 2–3 bullet scheme.
# Some iPN feeds have no descriptions; absence of mm/color must NOT suppress
# the entire summary. Never invent material or capabilities.
a=s.index('    private function hd_category_card_title_facts(')
b=s.index('    private function hd_idealo_category_title_relevant(',a)
old=s[a:b]
assert '$facts' in old and 'preg_match' in old and 'return array_slice' in old
new=r'''    /**
     * Small "Auf einen Blick" summary sourced ONLY from actually present data.
     * Price/provider/subject are described as such, not fictional specs.
     */
    private function hd_category_card_title_facts($title,$context=array(),$network='',$price='',$currency='EUR') {
        $title=trim(wp_strip_all_tags((string)$title));
        if ($title==='') { return array(); }
        $facts=array();
        // Product type and numeric specification have priority.
        if (preg_match('/\b(airbrushpistole|airbrushkompressor|spritzpistole|reinigungsset|teleskop|kompressor|pinselset|farbset)\b/ui',$title,$m)) {
            $facts[]='Produktart: '.$m[1];
        } elseif (preg_match('/\bairbrush[\s-]*(pistole|kompressor|set|farbe|reiniger)\b/ui',$title,$m)) {
            $facts[]='Produktart: Airbrush '.$m[1];
        }
        if (preg_match('/(?<![0-9])([0-9]{1,3}(?:[.,][0-9]{1,2})?)\s*(mm|ml|cm|kg|g)\b/ui',$title,$m)) {
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
        // Every other fallback is clearly identified as *topic, price or
        // source*, not a claimed special feature. Only use topic if the
        // product title independently contains the hobby words.
        if (count($facts)<2 && $this->hd_idealo_category_title_relevant($title,$context)) {
            $topic=trim((string)($context['primary_name']??''));
            if ($topic==='') { $topic=str_replace('-', ' ',sanitize_title((string)($context['primary_slug']??''))); }
            if ($topic!=='') { $facts[]='Thema: '.$topic; }
        }
        if (count($facts)<2 && trim((string)$price)!=='') {
            $facts[]='Preis: '.trim((string)$price).' '.strtoupper(substr(sanitize_text_field((string)$currency),0,3));
        }
        if (count($facts)<2 && in_array(sanitize_key((string)$network),array('idealo','amazon','ebay','otto'),true)) {
            $facts[]='Anbieter: '.ucfirst(sanitize_key((string)$network));
        }
        return array_slice(array_values(array_unique($facts)),0,3);
    }

'''
s=s[:a]+new+s[b:]
exact("""                $facts=$this->hd_category_card_title_facts($title);""",
"""                $facts=$this->hd_category_card_title_facts($title,$context,$network,$price,$currency);""",
"render existing bullet block with real context and recorded price/provider")
assert s.count("0.1.36")>=1
s=s.replace("0.1.36","0.1.37")
data[name]=s.encode('utf8')
with ZipFile(base) as z:
    diff=[i for i in data if data[i]!=z.read(i)]
    assert diff==[name],diff
buf=io.BytesIO()
with ZipFile(buf,'w') as z:
    for i in infos:z.writestr(i,data[i.filename])
out=Path(sys.argv[1] if len(sys.argv)>1 else '/tmp/HOBBY_DEPOT_HD009_0.1.37_RELEVANT_FACTS.zip')
out.parent.mkdir(parents=True,exist_ok=True)
out.write_bytes(buf.getvalue())
with ZipFile(out) as z:
    assert z.testzip() is None and len(z.namelist())==41
    assert b"Version: 0.1.37" in z.read(name)
print('BUILD_HD009_0.1.37',sha(out.read_bytes()),out.stat().st_size,'DIFF',diff)
