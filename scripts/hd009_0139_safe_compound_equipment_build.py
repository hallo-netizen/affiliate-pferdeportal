#!/usr/bin/env python3
"""HD009 0.1.39. Only real HD007 hobby+equipment-derived product forms.
Build from fully verified 0.1.38 candidate, with original 0.1.37 CURRENT unchanged.
No new product/ad concepts; no runtime HTTP, SQL, WordPress tables, feed or admin UI.
"""
from zipfile import ZipFile
from pathlib import Path
import hashlib,io,sys
source=Path(sys.argv[1])
out=Path(sys.argv[2])
sha=lambda b:hashlib.sha256(b).hexdigest()
assert sha(source.read_bytes())=='08ffe170601928b45c645809f6738bcc501bba8ea91b813bf1a4d808ee865573'
trait='affiliate-portal-router/includes/trait-ppar-idealo.php'
main='affiliate-portal-router/hobby-depot-affiliate-router.php'
with ZipFile(source) as z:
    assert z.testzip() is None and len(z.namelist())==41
    infos=z.infolist();data={i.filename:z.read(i.filename) for i in infos}
s=data[trait].decode()
def once(old,new,tag):
    global s
    assert s.count(old)==1,f'{tag}: count {s.count(old)}'
    s=s.replace(old,new,1)

start=s.index('    private function idealo_match_specific_equipment_stem(')
end=s.index('    private function idealo_match_index()',start)
s=s[:start]+r'''    /**
     * Source is the already-reviewed HD007 original hobby-register.
     * Only the actual FIRST equipment item, when it is an unambiguous
     * morphological hobby compound (Airbrushpistole / 3D-Drucker), is allowed.
     * No generic tools, new keyword datasets, or fuzzy/brand matching.
     * Returns an array of exact *stemmed product title tokens* or [].
     */
    private function idealo_match_specific_equipment_tokens($hobby_title) {
        if (!function_exists('hd_hobbyregister_get_by_name')) { return array(); }
        $hobby_title=trim((string)$hobby_title);
        if ($hobby_title==='') { return array(); }
        $row=hd_hobbyregister_get_by_name($hobby_title);
        if (!is_array($row)) { return array(); }
        $need=trim((string)($row['result_profile']['what_do_you_need']??''));
        if ($need==='') { return array(); }
        // A conjunction here joins different independent tools; never map
        // a combined/alternative or a sentence as one equipment identity.
        $first=trim((string)(preg_split('/[,;|]/u',$need,2)[0]??''));
        if ($first==='' || preg_match('/\b(?:oder|und|sowie|mit|ohne|etwas|geeignet(?:e|er|es|en)?)\b/ui',$first)) {
            return array();
        }
        $name_norm=$this->idealo_match_normalize($hobby_title);
        $item_norm=$this->idealo_match_normalize($first);
        $root=preg_replace('/[^a-z0-9]/','',$name_norm);
        $item=preg_replace('/[^a-z0-9]/','',$item_norm);
        if (strlen($root)<5 || strlen($item)<7) { return array(); }
        $variants=array($root);
        if (substr($root,-2)==='en' && strlen($root)>=8) { $variants[]=substr($root,0,-2); }
        if (substr($root,-1)==='n' && strlen($root)>=8) { $variants[]=substr($root,0,-1); }
        $match=false;
        foreach ($variants as $variant) {
            $extra=strlen($item)-strlen($variant);
            $min_extra=(preg_match('/[0-9]/',$variant) ? 2 : 4);
            if (strlen($variant)>=5 && $extra>=$min_extra && strpos($item,$variant)===0) {
                $match=true;break;
            }
        }
        if (!$match) { return array(); }
        $terms=$this->idealo_match_tokens($first);
        if (!$terms || count($terms)>3) { return array(); }
        $stems=array();
        foreach ($terms as $t) {
            $stem=$this->idealo_match_stem($t);
            if ($stem==='') { return array(); }
            $stems[]=$stem;
        }
        return array_values(array_unique($stems));
    }

'''+s[end:]
once("$equipment_owners = array();","$equipment_owners = array();","Existing ownership index only")
# The preceding intentional no-op guards source place. Replace single lines
once(
"""            $equipment_stem=$this->idealo_match_specific_equipment_stem((string)($concept['title']??''));""",
"""            $equipment_terms=$this->idealo_match_specific_equipment_tokens((string)($concept['title']??''));
            $equipment_key=implode('|',$equipment_terms);""",
"Equipment token array")
once(
"""'equipment_stem'=>$equipment_stem);""",
"""'equipment_terms'=>$equipment_terms);""",
"Equipment context array")
once(
"""            if ($equipment_stem!=='') {
                if (!isset($equipment_owners[$equipment_stem])) { $equipment_owners[$equipment_stem]=array(); }
                $equipment_owners[$equipment_stem][$id]=true;
            }""",
"""            if ($equipment_key!=='') {
                if (!isset($equipment_owners[$equipment_key])) { $equipment_owners[$equipment_key]=array(); }
                $equipment_owners[$equipment_key][$id]=true;
            }""",
"Unique equipment token phrase owners")
once(
"""        foreach ($equipment_owners as $stem=>$owners) {
            if (count($owners)!==1) {
                foreach (array_keys($owners) as $id) {
                    if (isset($concepts[$id])) { $concepts[$id]['equipment_stem']=''; }
                }
                continue;
            }
            $id=(string)array_key_first($owners);
            if (!isset($index[$stem])) { $index[$stem]=array(); }
            $index[$stem][$id]=true;
        }""",
"""        foreach ($equipment_owners as $key=>$owners) {
            if (count($owners)!==1) {
                foreach (array_keys($owners) as $id) {
                    if (isset($concepts[$id])) { $concepts[$id]['equipment_terms']=array(); }
                }
                continue;
            }
            $id=(string)array_key_first($owners);
            $parts=(array)($concepts[$id]['equipment_terms']??array());
            $stem=(string)end($parts);
            if ($stem==='') { continue; }
            if (!isset($index[$stem])) { $index[$stem]=array(); }
            $index[$stem][$id]=true;
        }""",
"Reject duplicate equipment phrase and index rarest last token")
once(
"""            $equipment_stem=(string)($concept['equipment_stem']??'');
            if ($equipment_stem==='' || !isset($title_stems[$equipment_stem])) { return 0; }""",
"""            $terms=(array)($concept['equipment_terms']??array());
            if (!$terms) { return 0; }
            foreach ($terms as $term) {
                if (!isset($title_stems[(string)$term])) { return 0; }
            }""",
"Exact complete equipment phrase tokens required in context")
once(
"""            $equipment=(string)($concept['equipment_stem']??'');
            $equipment_match=$equipment!=='' && isset($product_stems[$equipment]);""",
"""            $terms=(array)($concept['equipment_terms']??array());
            $equipment_match=!empty($terms);
            foreach ($terms as $term) {
                if (!isset($product_stems[(string)$term])) { $equipment_match=false; break; }
            }""",
"Exact complete equipment phrase tokens required in candidate")
data[trait]=s.encode()
m=data[main].decode()
start=m.index('    private function hd_idealo_category_title_relevant(')
end=m.index('    private function render_banner(',start)
a=m[start:end]
old="""        foreach ($need as $word) {
            $stem=$this->idealo_match_stem($word);
            if (isset($found[$stem])) { continue; }
            // A literal compound such as Airbrushpistole is relevant.
            // One-letter Malene/Malen substrings remain rejected.
            $compound=false;
            foreach (array_keys($found) as $term) {
                if (strlen($stem)>=5 && strpos($term,$stem)===0
                    && strlen($term)-strlen($stem)>=4) { $compound=true; break; }
            }
            if (!$compound) { return false; }
        }
        return true;"""
new="""        $topic_match=true;
        foreach ($need as $word) {
            $stem=$this->idealo_match_stem($word);
            if (isset($found[$stem])) { continue; }
            // Original direct title match: preserve known safe compound rule.
            $compound=false;
            foreach (array_keys($found) as $term) {
                if (strlen($stem)>=5 && strpos($term,$stem)===0
                    && strlen($term)-strlen($stem)>=4) { $compound=true; break; }
            }
            if (!$compound) { $topic_match=false; break; }
        }
        if ($topic_match) { return true; }
        // Reuse the *same* actual reviewed HD007 first equipment identity
        // that may have matched an imported campaign. Never accept generic
        // items. No database/HTTP lookups; the HD007 get-by-name API is local.
        $terms=$this->idealo_match_specific_equipment_tokens($topic);
        if (!$terms) { return false; }
        foreach ($terms as $term) {
            if (!isset($found[$term])) { return false; }
        }
        return true;"""
assert a.count(old)==1
m=m[:start]+a.replace(old,new)+m[end:]
assert '0.1.38' in m
m=m.replace('0.1.38','0.1.39')
data[main]=m.encode()
with ZipFile(source) as z:
    diff=[n for n in data if data[n]!=z.read(n)]
    assert set(diff)=={main,trait},diff
buf=io.BytesIO()
with ZipFile(buf,'w') as z:
    for i in infos:z.writestr(i,data[i.filename])
out.parent.mkdir(parents=True,exist_ok=True)
out.write_bytes(buf.getvalue())
with ZipFile(out) as z:
    assert z.testzip() is None and len(z.namelist())==41
    assert b'Version: 0.1.39' in z.read(main)
print('HD009_0139_SHA256',sha(out.read_bytes()),'BYTES',out.stat().st_size,'DIFF',diff)
