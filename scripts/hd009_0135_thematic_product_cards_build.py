#!/usr/bin/env python3
"""HD009 0.1.35 – block inherited irrelevant idealo product cards and Malene/Malen.
Full WordPress plugin from SHA-locked 0.1.34 comparison candidate.
"""
from pathlib import Path
from zipfile import ZipFile
import hashlib,io,sys

base=Path("protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE")
old=base/"CANDIDATES/HOBBY_DEPOT_HD009_0.1.34_FEEDVERGLEICH.zip"
expected="131298bc6dfa2344ae3a3c898372344d9cda56c12f98835c1482834a0ab34c3e"
sha=lambda data:hashlib.sha256(data).hexdigest()
assert sha(old.read_bytes())==expected,"Original 0.1.34 candidate differs – ABORT"
out=Path(sys.argv[1] if len(sys.argv)>1 else "/tmp/HOBBY_DEPOT_HD009_0.1.35_THEMATIC_PRODUCT_CARDS.zip")
main_name="affiliate-portal-router/hobby-depot-affiliate-router.php"
trait_name="affiliate-portal-router/includes/trait-ppar-idealo.php"
with ZipFile(old) as z:
    assert len(z.namelist())==41 and z.testzip() is None
    infos=z.infolist()
    files={i.filename:z.read(i.filename) for i in infos}
    main=files[main_name].decode()
    trait=files[trait_name].decode()
def exact(s,a,b,what):
    n=s.count(a);assert n==1,f"{what}: expected one source anchor, got {n}"
    return s.replace(a,b,1)

# Root-cause 1: "Malene" was stemmed to the German verb "malen",
# so fashion garments from feed 2747 entered the hobby catalogue.
# Keep valid "Teleskope" -> "Teleskop" but never invent the extra
# infinitive by dropping 'e' from a personal-name-like -ene ending.
trait=exact(trait,
"""            if ($suffix === 's' && substr($token, -2) === 'ss') { continue; }""",
"""            if ($suffix === 's' && substr($token, -2) === 'ss') { continue; }
            // "Malene" is not an inflection of "Malen".
            // Do not turn arbitrary "-ene" tokens into a German infinitive.
            if ($suffix === 'e' && substr($token, -3) === 'ene') { continue; }""",
"Malene/Malen morphological collision")

# Root-cause 2: materialized exact product offers include hub + parent
# target keys. Generic page-tree ranking accepts them on ALL descendants.
# For concrete idealo products in numbered category slots on actual Hobby
# pages only the page's own exact key constitutes sufficient evidence.
# Other providers, banners, article slots and combined GTIN remain unchanged.
method=r'''    /**
     * Source-safe filter for concrete idealo cards on Hobby Depot category *pages*.
     * Parent-world/page keys can help navigate, but do not prove relevance
     * for a child page's individual product recommendations.
     *
     * Read only: no database, API, image lookups or new data source.
     */
    private function hd_idealo_product_targets_exact_hobby_page($campaign, $context, $slot_type) {
        if (!preg_match('/^category_product_[123]$/', sanitize_key((string)$slot_type))) {
            return true;
        }
        if (sanitize_key((string)($campaign['network']??'')) !== 'idealo'
            || sanitize_key((string)($campaign['source']??'')) !== 'idealo_product_feed_v1') {
            return true;
        }
        if (sanitize_key((string)($context['post_type']??'')) !== 'page') {
            return true;
        }
        $slug=sanitize_title((string)($context['primary_slug']??''));
        if ($slug==='') { return false; }
        $target='page:'.$slug;
        foreach ((array)($campaign['automation_target_keys']??array()) as $raw_key) {
            if ((string)$raw_key===$target) { return true; }
        }
        return false;
    }

'''
main=exact(main,
"    private function category_product_shared_rank_base($context) {",
method+"    private function category_product_shared_rank_base($context) {",
"insert source-specific page exact target guard")
main=exact(main,
"""            $campaign = $this->ranked_campaign_from_post_cached($posts[$position]);
            if (!is_array($campaign)) { continue; }
            $runtime_campaign = $campaign;""",
"""            $campaign = $this->ranked_campaign_from_post_cached($posts[$position]);
            if (!is_array($campaign)) { continue; }
            if (!$this->hd_idealo_product_targets_exact_hobby_page($campaign, $rank_context, $slot_type)) {
                continue;
            }
            $runtime_campaign = $campaign;""",
"fast shared category product path")
main=exact(main,
"""            $runtime_campaign = $campaign;
            $runtime_campaign['_ppar_runtime_normalized_slot_type'] = 1;
            if (empty($runtime_campaign['_ppar_runtime_normalized'])) {""",
"""            if (!$this->hd_idealo_product_targets_exact_hobby_page($campaign, $rank_context, $slot_type)) {
                continue;
            }
            $runtime_campaign = $campaign;
            $runtime_campaign['_ppar_runtime_normalized_slot_type'] = 1;
            if (empty($runtime_campaign['_ppar_runtime_normalized'])) {""",
"uncached fallback category path")

assert main.count("0.1.34")>=1
main=main.replace("0.1.34","0.1.35")
files[main_name]=main.encode()
files[trait_name]=trait.encode()
with ZipFile(old) as z:
    changed=[n for n in files if files[n]!=z.read(n)]
    assert set(changed)=={main_name,trait_name},changed
buf=io.BytesIO()
with ZipFile(buf,'w') as z:
    for info in infos:z.writestr(info,files[info.filename])
out.parent.mkdir(parents=True,exist_ok=True)
out.write_bytes(buf.getvalue())
with ZipFile(out) as z:
    assert len(z.namelist())==41 and z.testzip() is None
    assert b"Version: 0.1.35" in z.read(main_name)
print('INPUT_SHA',expected,'OUTPUT_SHA',sha(out.read_bytes()),'BYTES',out.stat().st_size)
print('ONLY_TWO_EXISTING_PHP_CHANGED',changed)
