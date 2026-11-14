#!/usr/bin/env python3
"""RC39 KISS: fixed source aliases and parent branch fallback inside the
existing ONE Hab insurance import decision, never post-publication.
Build only from the fully verified RC38 archive; no unrelated portal edits.
"""
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile
from hashlib import sha256
R=Path("protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ")
P=R/"PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip"
raw=P.read_bytes()
assert sha256(raw).hexdigest()=="ff37c53a3d15479b7ac93be49fc6f4689238e08d5ccc471b24d06cdaff732d46","Exact RC38 required"
B="affiliate-portal-router/"
OUT=B+"includes/trait-ppar-output-objects.php"
MAIN=B+"affiliate-portal-router.php"
README=B+"readme.txt"
def one(text,old,new):
    n=text.count(old)
    assert n==1,("unexpected source",n,old[:200])
    return text.replace(old,new,1)
with ZipFile(BytesIO(raw)) as source:
    assert source.testzip() is None and len(source.namelist())==36
    contents={x.filename:source.read(x.filename) for x in source.infolist()}
    o=contents[OUT].decode()
    # Stable named, proved words only, no guessed URL target / IDs / extra checker.
    # Original evidence tiers and first-party deep links are unchanged.
    o=one(o,
        """        $all=preg_replace('/versicherungen\\b/u','versicherung',implode(' ', $evidence));
        // Never allow credit, shopping, energy, or financing masquerading as insurance.""",
        """        $all=preg_replace('/versicherungen\\b/u','versicherung',implode(' ', $evidence));
        // Fixed, reversible synonyms for EXISTING named insurance pages.
        // No blanket assumption that a Tarifcheck banner is insurance.
        // Append only to the SAME evidence string used below.
        $fixed_aliases=array(
            'kfz versicherung'=>array('autoversicherung','kraftfahrzeugversicherung'),
            'autoversicherung'=>array('kfz versicherung'),
            'kraftfahrzeugversicherung'=>array('kfz versicherung','autoversicherung'),
            'privathaftpflicht'=>array('privathaftpflichtversicherung'),
            'private haftpflicht'=>array('privathaftpflichtversicherung'),
            'pkv'=>array('private krankenversicherung'),
            'private krankenversicherung'=>array('pkv'),
            'bu versicherung'=>array('berufsunfahigkeitsversicherung'),
            'berufsunfahigkeit'=>array('berufsunfahigkeitsversicherung'),
            'hausrat'=>array('hausratversicherung'),
            'wohngebaude'=>array('wohngebaudeversicherung'),
            'wohngebaeude'=>array('wohngebaudeversicherung'),
            'grundbesitzer haftpflicht'=>array('haus und grundbesitzerhaftpflichtversicherung'),
        );
        $original_all=$all;
        foreach($fixed_aliases as $literal=>$expanded){
            if(preg_match('/(?<![a-z0-9])'.preg_quote($literal,'/').'(?![a-z0-9])/u',$original_all)){
                foreach($expanded as $variant)$all.=' '.$this->output_text($variant);
            }
        }
        // Never allow credit, shopping, energy, or financing masquerading as insurance.""")
    # Existing exact R2/R3 full phrase match remains FIRST priority. If
    # it fails, follow category labels and nearest actual parent in same tree.
    old="""        $anchor='';
        if($candidate_matches) {"""
    new="""        // One fixed owner decision: if an exact R3 page is missing, a
        // verified insurance leaf may anchor its REAL parent R2. The approved
        // parent then supplies its existing subtree; never a guessed WP ID.
        if(!$candidate_matches){
            foreach($eligible as $leaf_key=>$item){
                $leaf=$item['node'];
                if(($leaf['type']??'')!=='category')continue;
                $full=(string)($leaf['name']??'');
                $prefix=explode(':',$full,2)[0];
                $prefix=$this->output_text($prefix);
                $leaf_slug=$this->output_text(str_replace(array('-','_'),' ',(string)($leaf['slug']??'')));
                // The label must identify a concrete product, not generic
                // advice, a rate, FAQ or generic insurance marketing.
                $terms=array_values(array_unique(array_filter(array($prefix,$leaf_slug))));
                $supported=false;
                foreach($terms as $phrase){
                    if(strlen($phrase)<8 || in_array($phrase,array('versicherung','versicherungen','beratung','faq','kosten','leistungen'),true))continue;
                    if(preg_match('/(?<![a-z0-9])'.preg_quote($phrase,'/').'(?![a-z0-9])/u',$all)){
                        $supported=true;break;
                    }
                }
                if(!$supported)continue;
                $parent=(string)($leaf['parent']??'');
                $seen=array();
                while($parent!=='' && isset($eligible[$parent]) && !isset($seen[$parent])){
                    $seen[$parent]=true;
                    $p=$eligible[$parent]['node'];
                    if(($p['type']??'')==='page' && $parent!==$root){
                        $candidate_matches[$parent]=array('depth'=>$eligible[$parent]['depth'],'length'=>strlen($prefix));
                        break;
                    }
                    $parent=(string)($p['parent']??'');
                }
            }
        }
        // Fixed equivalent owner for a proven insurance product whose R3
        // and identifying leaf are missing. Accept ONLY an already-existing
        // relevant R2 title in the active WordPress category snapshot.
        if(!$candidate_matches){
            $parent_groups=array(
                'hausratversicherung'=>array('haus werte','hausrat gebaude','wohnen bauen','sachversicherungen'),
                'wohngebaudeversicherung'=>array('haus werte','hausrat gebaude','wohnen bauen','sachversicherungen'),
                'autoversicherung'=>array('fahrzeuge reisen','mobilitat freizeit','mobilitat','kfz versicherungen'),
                'motorradversicherung'=>array('fahrzeuge reisen','mobilitat freizeit','mobilitat','kfz versicherungen'),
                'privathaftpflichtversicherung'=>array('haftpflicht rechtsschutz','haftung gemeinschaft','haftung recht','haftpflichtversicherungen'),
                'rechtsschutzversicherung'=>array('haftpflicht rechtsschutz','haftung gemeinschaft','haftung recht','rechtsschutz'),
                'private krankenversicherung'=>array('krankenversicherung vorsorge','gesundheit vorsorge'),
                'berufsunfahigkeitsversicherung'=>array('krankenversicherung vorsorge','gesundheit vorsorge'),
            );
            foreach($parent_groups as $product=>$parent_names){
                if(!preg_match('/(?<![a-z0-9])'.preg_quote($product,'/').'(?![a-z0-9])/u',$all))continue;
                foreach($eligible as $key=>$item){
                    $node=$item['node'];
                    if(($node['type']??'')!=='page' || (string)($node['parent']??'')!==$root)continue;
                    $label=$this->output_text((string)($node['name']??''));
                    $slug=$this->output_text((string)($node['slug']??''));
                    if(in_array($label,$parent_names,true) || in_array($slug,$parent_names,true)){
                        $candidate_matches[$key]=array('depth'=>$item['depth'],'length'=>strlen($product));
                    }
                }
            }
        }
        $anchor='';
        if($candidate_matches) {"""
    o=one(o,old,new)
    o=one(o,"$option='ppar_hab_rc38_tarifcheck_reconcile_v1';",
            "$option='ppar_hab_rc39_tarifcheck_reconcile_v1';")
    contents[OUT]=o.encode()
    m=contents[MAIN].decode()
    m=one(m,"Version: 0.1.35-rc38","Version: 0.1.36-rc39")
    contents[MAIN]=m.encode()
    rd=contents[README].decode()
    rd=one(rd,"Stable tag: 0.1.35-rc38","Stable tag: 0.1.36-rc39")
    contents[README]=rd.encode()
    touched={OUT,MAIN,README}
    assert all(contents[n]==source.read(n) for n in source.namelist() if n not in touched)
    buf=BytesIO()
    with ZipFile(buf,"w") as new:
        for info in source.infolist():new.writestr(info,contents[info.filename])
    result=buf.getvalue()
with ZipFile(BytesIO(result)) as z:
    assert z.testzip() is None and len(z.namelist())==36
    assert b"ppar_hab_rc39_tarifcheck_reconcile_v1" in z.read(OUT)
P.write_bytes(result)
print("RC39_ONE_SOURCE_FIXED_OWNER_BUILD_PASS",len(result),sha256(result).hexdigest())
