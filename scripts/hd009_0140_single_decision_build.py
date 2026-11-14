#!/usr/bin/env python3
"""HD009 0.1.40: ONE thematic decision in existing Idealo feed matcher.

Based on complete archived 0.1.39 candidate; never change CURRENT.
Uses HD007's real equipment list, including context-bound related items.
No late public HTML topical re-evaluation. Other provider rules unchanged.
"""
from pathlib import Path
from zipfile import ZipFile
import hashlib, io, sys

src=Path(sys.argv[1]); dest=Path(sys.argv[2])
sha=lambda b:hashlib.sha256(b).hexdigest()
assert sha(src.read_bytes())=="94528a6c572c77891c1b5faa8824018d5fd389a731b029607dbad2cc4dc45c7c", "Unexpected 0.1.39 candidate"
main="affiliate-portal-router/hobby-depot-affiliate-router.php"
trait="affiliate-portal-router/includes/trait-ppar-idealo.php"
with ZipFile(src) as z:
    assert z.testzip() is None and len(z.namelist())==41
    infos=z.infolist()
    data={x.filename:z.read(x.filename) for x in infos}

s=data[trait].decode("utf-8")
def replace_exact(old,new,label):
    global s
    assert s.count(old)==1, f"{label} anchor count {s.count(old)}"
    s=s.replace(old,new,1)

helper=r'''    /**
     * Context-supported, not merely a name similarity: get equipment nouns
     * ONLY from HD007's already published real requirements text.
     * Generic terms are admissible only together with the hobby-specific
     * PRODUCT CATEGORY in the same feed row; never on their own.
     */
    private function idealo_match_related_equipment_stems($hobby_title) {
        if (!function_exists('hd_hobbyregister_get_by_name')) { return array(); }
        $record=hd_hobbyregister_get_by_name(trim((string)$hobby_title));
        if (!is_array($record)) { return array(); }
        $need=trim((string)($record['result_profile']['what_do_you_need']??''));
        if ($need==='') { return array(); }
        $out=array();
        foreach (array_slice((array)preg_split('/[,;|]+|\s+(?:oder|und|sowie)\s+/ui',$need),0,12) as $phrase) {
            // Last substantive noun of each source item:
            // "geeigneten Arbeitsplatz" -> Arbeitsplatz.
            $tokens=$this->idealo_match_tokens((string)$phrase);
            if (!$tokens) { continue; }
            $word=(string)end($tokens);
            $stem=$this->idealo_match_stem($word);
            if (strlen($stem)<4 || in_array($stem,array('hobb','material','ausrust','ausruest','geeignet','zubehor','zubehoer'),true)) { continue; }
            $out[$stem]=true;
        }
        return array_keys($out);
    }

'''
replace_exact("    private function idealo_match_index() {",helper+"    private function idealo_match_index() {","single decision equipment helper")
replace_exact("'equipment_terms'=>$equipment_terms);",
              "'equipment_terms'=>$equipment_terms,'related_equipment_stems'=>$this->idealo_match_related_equipment_stems((string)($concept['title']??'')));",
              "stored per-concept evidence from existing HD007")
replace_exact(
"""        $candidate_ids = array(); foreach (array_keys($product_stems) as $stem) { foreach ((array)($mi['index'][$stem]??array()) as $id=>$true) { $candidate_ids[$id]=true; } }
        if (!$candidate_ids) { return array('status'=>'none'); }""",
"""        $candidate_ids = array(); foreach (array_keys($product_stems) as $stem) { foreach ((array)($mi['index'][$stem]??array()) as $id=>$true) { $candidate_ids[$id]=true; } }
        // Also consider the original feed CATEGORY as concrete evidence;
        // a generic tool may only be related when this category names the hobby.
        foreach ($this->idealo_match_tokens((string)($row['main_category']??'').' '.(string)($row['sub_category']??'')) as $token) {
            $stem=$this->idealo_match_stem($token);
            foreach ((array)($mi['index'][$stem]??array()) as $id=>$true) { $candidate_ids[$id]=true; }
        }
        if (!$candidate_ids) { return array('status'=>'none'); }""",
"early product+category index")
replace_exact(
"""        $category_stems=array(); foreach ($this->idealo_match_tokens($main_n.' '.$sub_n) as $token) { $category_stems[]=$this->idealo_match_stem($token); }""",
"""        $category_stems=array(); foreach ($this->idealo_match_tokens($main_n.' '.$sub_n) as $token) { $category_stems[]=$this->idealo_match_stem($token); }
        foreach (preg_split('/\s+/',$this->idealo_match_normalize($main_n.' '.$sub_n)) as $short) {
            if (strlen((string)$short)===2 && preg_match('/^(?:[a-z]{2}|[0-9][a-z])$/',(string)$short)) {
                $category_stems[]=(string)$short;
            }
        }
        $category_qualified=array_fill_keys($category_stems,true);""",
"category evidence only once")
replace_exact(
"""            if (!$all && !$equipment_match) { continue; }
            $context=$this->idealo_match_context_score($concept,$title_n,$main_n,$sub_n,$mi['catalog']); if ($context<=0) { $context_rejected=true; continue; }""",
"""            $related_match=false;
            if (!$all && !$equipment_match) {
                // One category-plus-product decision; no fuzzy similarity.
                $category_proves_hobby=true;
                foreach ((array)$concept['stems'] as $stem) {
                    if (!isset($category_qualified[$stem])) { $category_proves_hobby=false; break; }
                }
                if ($category_proves_hobby) {
                    foreach ((array)($concept['related_equipment_stems']??array()) as $stem) {
                        if (isset($product_stems[(string)$stem])) { $related_match=true; break; }
                    }
                }
            }
            if (!$all && !$equipment_match && !$related_match) { continue; }
            $context=$related_match ? 2 : $this->idealo_match_context_score($concept,$title_n,$main_n,$sub_n,$mi['catalog']);
            if ($context<=0) { $context_rejected=true; continue; }""",
"one central eligibility outcome")
replace_exact(
"""$score=($phrase_title?160:0)+($equipment_match&&!$all?160:0)+""",
"""$score=($phrase_title?160:0)+($equipment_match&&!$all?160:0)+($related_match?140:0)+""",
"rank context-supported equipment")
data[trait]=s.encode("utf-8")

m=data[main].decode("utf-8")
old_gate="""        // Final shared output gate: checked here, not only in a preferred
        // candidate route. Product source labels may change across versions.
        // No image placeholder may stand in for a missing real product photo.
        if ($category_product_slot && $creative_type==='product' && $network==='idealo'
            && sanitize_key((string)($context['post_type']??''))==='page'
            && ($image_url==='' || !$this->hd_idealo_category_title_relevant($title,$context))) {
            return '';
        }
"""
assert m.count(old_gate)==1, "The historical duplicate final relevance gate changed"
m=m.replace(old_gate,"        // Idealo relevance was decided exactly once at feed import, before storing its target.\n",1)
old_fact="""if (count($facts)<2 && $this->hd_idealo_category_title_relevant($title,$context)) {"""
new_fact="""if (count($facts)<2 && trim((string)($context['primary_name']??''))!=='') {"""
assert m.count(old_fact)==1, "No re-evaluation in product description"
m=m.replace(old_fact,new_fact,1)
# The old method is no longer used anywhere. Remove it rather than keep a
# second conflicting source of relevance that a future caller can revive.
start=m.index("    private function hd_idealo_category_title_relevant(")
end=m.index("    private function render_banner(",start)
old_method=m[start:end]
assert "private function hd_idealo_category_title_relevant(" in old_method
assert m.count("hd_idealo_category_title_relevant(")==1, "Old topical decision has other callers"
m=m[:start]+m[end:]
assert "hd_idealo_category_title_relevant" not in m
assert m.count("Version: 0.1.39")==1
m=m.replace("Version: 0.1.39","Version: 0.1.40",1)
# Other mentions of 0.1.39 are historical in the code, do not change them.
data[main]=m.encode("utf-8")

with ZipFile(src) as z:
    diff=[name for name in data if data[name]!=z.read(name)]
    assert set(diff)=={trait,main}, diff
buf=io.BytesIO()
with ZipFile(buf,"w") as z:
    for entry in infos: z.writestr(entry,data[entry.filename])
dest.parent.mkdir(parents=True,exist_ok=True)
dest.write_bytes(buf.getvalue())
with ZipFile(dest) as z:
    assert z.testzip() is None and len(z.namelist())==41
    assert b"Version: 0.1.40" in z.read(main)
    assert b"related_equipment_stems" in z.read(trait)
    assert b"hd_idealo_category_title_relevant" not in z.read(main)
print("HD009_0140_SHA256",sha(dest.read_bytes()),"BYTES",dest.stat().st_size,"FILES_CHANGED",diff)
