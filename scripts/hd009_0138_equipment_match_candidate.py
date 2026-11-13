#!/usr/bin/env python3
"""HD009 0.1.38 candidate: original HD007 equipment information in original Idealo matcher.

Intentionally very narrow:
- read an existing registered hobby's *first, topic-prefixed, specific* equipment noun
- never accept generic "Kompressor", "Farben", "Leder" or "Aufbewahrung" alone
- do not change any provider, feed credentials, staging/DB layer or frontend
- existing 0.1.37 final relevance check must still independently pass
- no claim that an uninspected live private iPN feed contains the relevant product
"""
from pathlib import Path
from zipfile import ZipFile
import io,hashlib,sys
office=Path('protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE')
source=office/'CURRENT.zip'
sha=lambda b:hashlib.sha256(b).hexdigest()
expected='34b870ad459e9b075a5c8c0aedc335939a72f6689d03216bcfd4134798c73503'
assert sha(source.read_bytes())==expected,'Wrong HD009 0.1.37 full baseline: abort'
main='affiliate-portal-router/hobby-depot-affiliate-router.php'
trait='affiliate-portal-router/includes/trait-ppar-idealo.php'
with ZipFile(source) as z:
    assert z.testzip() is None and len(z.namelist())==41
    infos=z.infolist()
    files={i.filename:z.read(i.filename) for i in infos}
s=files[trait].decode('utf8')
def replace_once(before,after,label):
    global s
    assert s.count(before)==1,f'ABORT {label}: anchor count {s.count(before)}'
    s=s.replace(before,after,1)

helper=r'''    /**
     * Narrow equipment evidence already maintained by HD007, not new text or
     * copied keyword lists. For now only single-word hobby roots followed by
     * a longer, explicit equipment-specific compound are accepted.
     *
     * Airbrush -> Airbrushpistole; never Airbrush -> Kompressor alone.
     * This cannot make articles appear if the actual feed has no such goods.
     */
    private function idealo_match_specific_equipment_stem($hobby_title) {
        if (!function_exists('hd_hobbyregister_get_by_name')) { return ''; }
        $hobby_title=trim((string)$hobby_title);
        if ($hobby_title==='') { return ''; }
        $record=hd_hobbyregister_get_by_name($hobby_title);
        if (!is_array($record)) { return ''; }
        $need=trim((string)($record['result_profile']['what_do_you_need']??''));
        if ($need==='') { return ''; }
        $parts=preg_split('/[,;|]/u',$need,2);
        $first=trim((string)($parts[0]??''));
        $root=$this->idealo_match_normalize($hobby_title);
        $equipment=$this->idealo_match_normalize($first);
        // No generic or ambiguous nouns; no stemming creates a product category.
        if (!preg_match('/^[a-z0-9]{5,}$/D',$root)
            || !preg_match('/^[a-z0-9]{9,}$/D',$equipment)) { return ''; }
        if (strpos($equipment,$root)!==0
            || strlen($equipment)-strlen($root)<4) { return ''; }
        return $this->idealo_match_stem($equipment);
    }

'''
replace_once('    private function idealo_match_index() {',helper+'    private function idealo_match_index() {','Insert HD007 read-only equipment helper')

replace_once('        $concepts = array(); $index = array();',
             '        $concepts = array(); $index = array(); $equipment_owners = array();',
             'Initialize global equipment uniqueness')
replace_once(
"""            $entry = array('id'=>$id,'title'=>(string)($concept['title']??''),'stems'=>$stems,'hub_stems'=>array_keys($hub),'main_stems'=>array_keys($main),'rel_stems'=>$rel,'main_hub'=>(string)($first_page['main_hub']??''),'hub'=>(string)($first_page['hub']??''),'target_pages'=>(array)($concept['target_pages']??array()));""",
"""            $equipment_stem=$this->idealo_match_specific_equipment_stem((string)($concept['title']??''));
            $entry = array('id'=>$id,'title'=>(string)($concept['title']??''),'stems'=>$stems,'hub_stems'=>array_keys($hub),'main_stems'=>array_keys($main),'rel_stems'=>$rel,'main_hub'=>(string)($first_page['main_hub']??''),'hub'=>(string)($first_page['hub']??''),'target_pages'=>(array)($concept['target_pages']??array()),'equipment_stem'=>$equipment_stem);
            if ($equipment_stem!=='') {
                if (!isset($equipment_owners[$equipment_stem])) { $equipment_owners[$equipment_stem]=array(); }
                $equipment_owners[$equipment_stem][$id]=true;
            }""",
"Add verified equipment evidence to original concept")

replace_once(
"""        if (!$concepts || count($concepts) !== count((array)$catalog['_idealo_required_concepts'])) { return $cache = new WP_Error('idealo_match_index_incomplete', 'Matcher konnte nicht alle Hobby-Depot-Recherchekonzepte binden.'); }""",
"""        // Only unique first-equipment compounds may become extra index keys.
        // If two hobbies claim the same specific equipment, reject it for both.
        foreach ($equipment_owners as $stem=>$owners) {
            if (count($owners)!==1) {
                foreach (array_keys($owners) as $id) {
                    if (isset($concepts[$id])) { $concepts[$id]['equipment_stem']=''; }
                }
                continue;
            }
            $id=(string)array_key_first($owners);
            if (!isset($index[$stem])) { $index[$stem]=array(); }
            $index[$stem][$id]=true;
        }
        if (!$concepts || count($concepts) !== count((array)$catalog['_idealo_required_concepts'])) { return $cache = new WP_Error('idealo_match_index_incomplete', 'Matcher konnte nicht alle Hobby-Depot-Recherchekonzepte binden.'); }""",
"Only unique real equipment phrases can match")

replace_once(
"""        foreach ($required as $stem) {
            if (!isset($title_stems[$stem])) { return 0; }
        }""",
"""        $all_required=true;
        foreach ($required as $stem) {
            if (!isset($title_stems[$stem])) { $all_required=false; break; }
        }
        if (!$all_required) {
            $equipment_stem=(string)($concept['equipment_stem']??'');
            if ($equipment_stem==='' || !isset($title_stems[$equipment_stem])) { return 0; }
        }""",
"Context check allows only verified equipment alternative")

replace_once(
"""            $all=true; foreach ((array)$concept['stems'] as $stem) { if (!isset($product_stems[$stem])) { $all=false; break; } } if (!$all) { continue; }""",
"""            $all=true; foreach ((array)$concept['stems'] as $stem) { if (!isset($product_stems[$stem])) { $all=false; break; } }
            $equipment=(string)($concept['equipment_stem']??'');
            $equipment_match=$equipment!=='' && isset($product_stems[$equipment]);
            if (!$all && !$equipment_match) { continue; }""",
"Accept only exact equipment stem as alternative to hobby name")

replace_once(
"""            $score=($phrase_title?160:0)+(count((array)$concept['stems'])*55)+min(24,$hubhits*8)+min(12,$mainhits*4)+($relhits*20)+($context*35);""",
"""            $score=($phrase_title?160:0)+($equipment_match&&!$all?160:0)+(count((array)$concept['stems'])*55)+min(24,$hubhits*8)+min(12,$mainhits*4)+($relhits*20)+($context*35);""",
"Add strong verified specific gear evidence without weakening ranking")

files[trait]=s.encode('utf8')
header=files[main].decode('utf8')
assert '0.1.37' in header
files[main]=header.replace('0.1.37','0.1.38').encode('utf8')
with ZipFile(source) as z:
    diff=[name for name in files if files[name]!=z.read(name)]
    assert set(diff)=={main,trait},diff
out=Path(sys.argv[1] if len(sys.argv)>1 else '/tmp/HOBBY_DEPOT_HD009_0.1.38_EQUIPMENT_MATCH_CANDIDATE.zip')
out.parent.mkdir(parents=True,exist_ok=True)
buf=io.BytesIO()
with ZipFile(buf,'w') as z:
    for entry in infos:z.writestr(entry,files[entry.filename])
out.write_bytes(buf.getvalue())
with ZipFile(out) as z:
    assert z.testzip() is None and len(z.namelist())==41
    assert b'Version: 0.1.38' in z.read(main)
print('CANDIDATE_HD009_0.1.38_SHA256',sha(out.read_bytes()))
print('FILES_CHANGED_EXACTLY',diff)
print('CANDIDATE_SIZE',out.stat().st_size)
