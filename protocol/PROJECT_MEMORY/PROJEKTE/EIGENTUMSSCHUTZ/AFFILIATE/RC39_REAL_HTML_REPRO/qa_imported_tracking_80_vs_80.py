#!/usr/bin/env python3
"""NO PLUGIN RELEASE. Reproduce 80+80 from HTML-only source shape.
Use EXACT RC39 plugin original PHP methods in the repo's original RC31
real-code QA, adding the ORIGINAL PHP HTML parser from the package.
Synthetic affiliate URLs: only diagnostics; no claims about the user's
actual 160 private links.
"""
from pathlib import Path
from tempfile import TemporaryDirectory
from subprocess import run
from zipfile import ZipFile
import sys
R=Path("protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ")
Z=R/"PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip"
with ZipFile(Z) as z:
    assert z.testzip() is None and len(z.namelist())==36
    s=z.read("affiliate-portal-router/includes/trait-ppar-output-objects.php").decode()
    c=z.read("affiliate-portal-router/includes/trait-ppar-creative-library.php").decode()
    assert "ppar_hab_rc39_tarifcheck_reconcile_v1" in s
    assert "function creative_library_parse_html_codes(" in c
base=(R/"AFFILIATE/RC31_INSURANCE_CASCADE/qa_rc31.py").read_text()
base=base.replace("0.1.28-rc31","0.1.36-rc39").replace(
 "ppar_hab_rc31_tarifcheck_reconcile_v1",
 "ppar_hab_rc39_tarifcheck_reconcile_v1"
)
needle="    harness=r'''<?php"
assert base.count(needle)==1
newpython=r'''
    # Include the exact HTML extraction functions from the actual packed RC39.
    creative=z.read("affiliate-portal-router/includes/trait-ppar-creative-library.php").decode()
    def creative_method(name):
        import re
        pat=re.compile(r"(?:private|public|protected)(?:\s+static)?\s+function\s+"+re.escape(name)+r"\s*\(")
        mat=pat.search(creative)
        assert mat,name
        i=creative.index("{",mat.end())
        depth=0
        for j in range(i,len(creative)):
            if creative[j]=="{":depth+=1
            if creative[j]=="}":
                depth-=1
                if depth==0:
                    return creative[mat.start():j+1].replace("private function","public function",1)
        raise AssertionError(name)
    methods+="\n"+creative_method("creative_library_html_attr")
    methods+="\n"+creative_method("creative_library_parse_html_codes")
'''
base=base.replace(needle,newpython+needle)
classneedle="  METHODS"
assert base.count(classneedle)==1
base=base.replace(classneedle,
"  public function creative_library_detect_mapping($keys){return array();}\n"+classneedle)
insert_at="$motor=banner('motorradversicherung/','Motorradversicherung vergleichen');"
assert base.count(insert_at)==1
php=r'''
// ACTUAL unchanged HTML extraction and classification, 160 synthetic codes.
// 80 anchor URLs have identifiable 'deep=hausratversicherung', 80 do NOT.
// This distinguishes 'same categories but missing original metadata' from
// a bogus claim that synonym tables or parent fallback can invent source data.
$codes='';
for($i=1;$i<=160;$i++){
  $href='https://a.partner-versicherung.de/click.php?partner_id=DEMO&ad_id='.$i;
  if($i<=80)$href.='&deep=hausratversicherung';
  $codes.='<a href="'.htmlspecialchars($href,ENT_QUOTES).'" target="_blank">'
    .'<img src="https://a.partner-versicherung.de/assets/banner'.($i%8).'.png"'
    .' title="" alt="" width="300" height="250"></a>'."\n";
}
$raw=$o->creative_library_parse_html_codes($codes,160);
ok($raw['format']==='html' && count($raw['rows'])===160,
   'Original HTML parser successfully extracts all 160 synthetic anchor/image pairs');
$targeted=0;$untargeted=0;$failReasons=array();
foreach($raw['rows'] as $i=>$original) {
  ok($original['creative_title']==='' && $original['alt_text']==='',
     'Original banner title and alt remain EMPTY in HTML' );
  $row=banner('unknown/','Tarifcheck Banner');
  $row['destination_url']=$original['tracking_url'];
  $row['tracking_url']=$original['tracking_url'];
  $row['payload']=json_encode(array('_destination_source'=>'tracking_checked',
    'html'=>$original['html'],
    '_dimension_state'=>'verified'));
  $p=$o->hb_rc31_insurance_banner_plan($row,$portal,$GLOBALS['targets'],array('page','category'));
  if(($p['status']??'')==='ready') {
     $targeted++;
     ok(($p['target']['id']??0)===111,
      'Original HTML deep=hausratversicherung resolves to the REAL existing Hausrat R3');
  }else{
     $untargeted++;
     $why=(string)($p['reason']??'');
     $failReasons[$why]=($failReasons[$why]??0)+1;
  }
}
ok($targeted===80 && $untargeted===80,
   'RC39 reproduces exactly 80 matching / 80 blocked when HTML lacks product hints');
ok(($failReasons['No verified specific/general insurance']??0)===80,
   'The real original decision emits the screenshot reason 80 times');
echo "RC39_ORIGINAL_HTML_80_80_PROOF_PASS\n";

// The same 80 missing still fail even with more matching WP nodes:
// a fixed category table cannot rescue NO encoded product/category evidence.
$extra=array('id'=>'test:newpage','parent'=>'core:world:insurance',
 'type'=>'page','wp_id'=>987,'name'=>'Gebäude und Haushalt',
 'slug'=>'gebaeude-und-haushalt');
$GLOBALS['nodes'][$extra['id']]=$extra;
$GLOBALS['targets'][]=array('type'=>'page','id'=>987,'key'=>'page:987',
 'slug'=>$extra['slug'],'label'=>$extra['name'],'context'=>'page','depth'=>2);
$r=banner('unknown/','Tarifcheck Banner');
$r['tracking_url']='https://a.partner-versicherung.de/click.php?partner_id=DEMO&ad_id=161';
$r['destination_url']=$r['tracking_url'];
$r['payload']=json_encode(array('_destination_source'=>'tracking_checked',
 'html'=>'<a href="https://a.partner-versicherung.de/click.php?ad_id=161"><img src="https://a.partner-versicherung.de/img.png" alt=""></a>'));
$failure=$o->hb_rc31_insurance_banner_plan($r,$portal,$GLOBALS['targets'],array('page','category'));
ok($failure['status']==='blocked' && $failure['reason']==='No verified specific/general insurance',
 'Extra real WP parent category cannot identify anonymous product creative');
// Restore untouched fixture before the existing original regression.
unset($GLOBALS['nodes'][$extra['id']]);
array_pop($GLOBALS['targets']);
'''
# Avoid generating 80 repeated PASS lines for one noncritical invariant,
# still verify via one assert after the loop.
php=php.replace("""  ok($original['creative_title']==='' && $original['alt_text']==='',
     'Original banner title and alt remain EMPTY in HTML' );""",
"""  if($original['creative_title']!=='' || $original['alt_text']!==''){
    fwrite(STDERR,"Unexpected source HTML metadata"); exit(9);
  }""")
php=php.replace("""     ok(($p['target']['id']??0)===111,
      'Original HTML deep=hausratversicherung resolves to the REAL existing Hausrat R3');""",
"""     if(($p['target']['id']??0)!==111){fwrite(STDERR,"Wrong target in deep URL");exit(10);}""")
base=base.replace(insert_at,php+"\n"+insert_at)
with TemporaryDirectory() as td:
    f=Path(td)/"run_160_html_qa.py"
    f.write_text(base)
    p=run([sys.executable,str(f)],capture_output=True,text=True)
    print(p.stdout[-11000:])
    if p.returncode:print(p.stderr[-6000:])
    assert p.returncode==0,(p.stdout[-7000:],p.stderr[-7000:])
    assert "RC39_ORIGINAL_HTML_80_80_PROOF_PASS" in p.stdout
print("LOCAL_SIMULATION_VERIFIED__NO_NEW_PLUGIN_RELEASE")
