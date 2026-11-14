#!/usr/bin/env python3
"""RC40 acceptance: exact packed PHP, ONE source read then ONE target owner.
No synthetic success is reported as actual private WP banner coverage.
"""
from pathlib import Path
from zipfile import ZipFile
from tempfile import TemporaryDirectory
from subprocess import run
import sys
R=Path("protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ")
P=R/"PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip"
with ZipFile(P) as z:
    assert z.testzip() is None and len(z.namelist())==36
    cre=z.read("affiliate-portal-router/includes/trait-ppar-creative-library.php").decode()
    out=z.read("affiliate-portal-router/includes/trait-ppar-output-objects.php").decode()
    main=z.read("affiliate-portal-router/affiliate-portal-router.php").decode()
    assert "Version: 0.1.37-rc40" in main
    assert "ppar_hab_rc40_tarifcheck_reconcile_v1" in out
    assert "function creative_library_read_original_banner_once(" in cre
    assert "_source_read_version" in cre
    assert "if($type==='banner')" in cre
    assert out.count("creative_library_read_original_banner_once($row)") == 1
    assert "destination_url'=>$destination," in out
    assert "if(is_array($source_evidence)" in out
    # No extra frontend table/routing code. Our changes are only original
    # source reading and original one-owner logic, not a public classifier.
    assert "RC40" not in z.read("affiliate-portal-router/assets/frontend.css").decode()
base=(R/"AFFILIATE/RC31_INSURANCE_CASCADE/qa_rc31.py").read_text()
assert "0.1.28-rc31" in base
base=base.replace("0.1.28-rc31","0.1.37-rc40")
base=base.replace("ppar_hab_rc31_tarifcheck_reconcile_v1","ppar_hab_rc40_tarifcheck_reconcile_v1")
# Extract exact methods from completed package into original real-PHP harness
needle="    harness=r'''<?php"
assert base.count(needle)==1
extraction=r'''
    creative=z.read("affiliate-portal-router/includes/trait-ppar-creative-library.php").decode()
    def method_from_creative(name):
        import re
        p=re.search(r"(?:private|public|protected)(?:\s+static)?\s+function\s+"+re.escape(name)+r"\s*\(",creative)
        assert p,name
        start=creative.index("{",p.end());depth=0
        for end in range(start,len(creative)):
            if creative[end]=="{":depth+=1
            if creative[end]=="}":
                depth-=1
                if depth==0:return creative[p.start():end+1].replace("private function","public function",1)
        raise AssertionError(name)
    for name in ("creative_library_html_attr","creative_library_parse_html_codes",
                 "creative_library_read_original_banner_once"):
        methods+="\n"+method_from_creative(name)
'''
base=base.replace(needle,extraction+needle)
# Include required context method but NOT a mock parser or classifier.
needle2="  METHODS"
assert base.count(needle2)==1
base=base.replace(needle2,"  public function creative_library_detect_mapping($columns){return array();}\n"+needle2)
# Unit verification of only-one write to the original WordPress table.
old="public $rows=array(),$saved=array(),$prefix='wp_';"
assert base.count(old)==1
base=base.replace(old,"public $rows=array(),$saved=array(),$prefix='wp_',$updates=0;")
old="    $id=(int)$where['id']; $this->saved[$id]=$values;"
assert base.count(old)==1
base=base.replace(old,"    $this->updates++; $id=(int)$where['id']; $this->saved[$id]=$values;")
insert="$motor=banner('motorradversicherung/','Motorradversicherung vergleichen');"
assert base.count(insert)==1
php=r'''
// 160 STRUCTURE-REAL HTML sources, with one equivalent stored source for all
// 80 previously ambiguous cases. All pass the same original read and decision.
$codes='';
for($i=0;$i<160;$i++) {
 $href='https://a.partner-versicherung.de/click.php?partner_id=EXAMPLE&ad_id='.$i;
 $alt='';$anchor='';$filename='banner'.($i%7);
 if($i<40){$href.='&deep=hausratversicherung';}
 elseif($i<80){$alt='Hausratversicherung';}
 elseif($i<120){$anchor='Hausratversicherung';}
 $codes.='<a href="'.htmlspecialchars($href,ENT_QUOTES).'" target="_blank">'
   .$anchor.'<img src="https://a.partner-versicherung.de/images/'.$filename.'.png"'
   .' title="" alt="'.$alt.'" width="300" height="250"></a>'."\n";
}
$parsed=$o->creative_library_parse_html_codes($codes,160);
ok(is_array($parsed) && count($parsed['rows'])===160,
   'Actual HTML reader extracted 160 original source-shaped codes FIRST');
$recognized=0;$unidentified=0;$reasonCounts=array();
foreach($parsed['rows'] as $i=>$src) {
 $row=banner('none/','Tarifcheck Banner');
 $row['tracking_url']=$src['tracking_url'];
 $row['destination_url']=$src['tracking_url'];
 $row['image_url']=$src['image_source'];
 $row['payload']=json_encode(array(
  '_destination_source'=>'tracking_checked',
  'html'=>$src['html'],
  'alt_text'=>$src['alt_text'],
  'creative_title'=>$src['creative_title'],
  '_dimension_state'=>'verified'));
 $read=$o->creative_library_read_original_banner_once($row);
 $saved=json_decode((string)$read['payload'],true);
 if(($saved['_source_read_version']??0)!==1
    || !is_array($saved['_source_evidence']??null)){
   fwrite(STDERR,"FAIL source read missing");exit(90);
 }
 // Reconcile never re-reads the same original once stored.
 if($read['payload']!==$o->creative_library_read_original_banner_once($read)['payload']){
   fwrite(STDERR,"FAIL second source read");exit(91);
 }
 if($i>=120 && ($saved['title_source']??'')!=='manual_missing'){
   fwrite(STDERR,"FAIL dummy Tarifcheck Banner treated as original title");exit(92);
 }
 $plan=$o->hb_rc31_insurance_banner_plan($read,$portal,$GLOBALS['targets'],array('page','category'));
 if(($plan['status']??'')==='ready'){
   $recognized++;
   if(($plan['target']['id']??0)!==111){fwrite(STDERR,"FAIL wrong insurance branch");exit(93);}
 }else{
   $unidentified++;
   $why=(string)($plan['reason']??'unknown');
   $reasonCounts[$why]=($reasonCounts[$why]??0)+1;
 }
}
ok($recognized===120 && $unidentified===40,
 '160 sources: 40 link deep + 40 image alt + 40 anchor text are mapped; 40 anonymous remain blocked');
ok(($reasonCounts['No verified insurance creative evidence']??0)===40,
 'Unidentifiable creative correctly reports lack of ORIGINAL evidence, not fictitious title');
echo "RC40_SOURCE_FIRST_160_HTML_REAL_PHP_PASS\n";

// A single image filename can be a true weak product hint, but no generic
// 'banner-300x250.png' may claim to identify the product by size alone.
$image=banner('none/','Tarifcheck Banner');
$image['tracking_url']='https://a.partner-versicherung.de/click.php?ad_id=199';
$image['destination_url']=$image['tracking_url'];
$image['image_url']='https://a.partner-versicherung.de/img/hausratversicherung-300x250.png';
$image['payload']=json_encode(array('_destination_source'=>'tracking_checked'));
$image=$o->creative_library_read_original_banner_once($image);
$imgPlan=$o->hb_rc31_insurance_banner_plan($image,$portal,$GLOBALS['targets'],array('page','category'));
ok($imgPlan['status']==='ready' && $imgPlan['target']['id']===111,
  'Original image filename is read before insurance decision, if explicit');
$unknown=banner('none/','Tarifcheck Banner');
$unknown['tracking_url']='https://a.partner-versicherung.de/click.php?ad_id=200';
$unknown['destination_url']=$unknown['tracking_url'];
$unknown['image_url']='https://a.partner-versicherung.de/img/banner-300x250.png';
$unknown['payload']=json_encode(array('_destination_source'=>'tracking_checked'));
$unknown=$o->creative_library_read_original_banner_once($unknown);
$unkPlan=$o->hb_rc31_insurance_banner_plan($unknown,$portal,$GLOBALS['targets'],array('page','category'));
ok($unkPlan['status']==='blocked','Generic image file and anonymous link remain blocked');

// One source read, one owner, one DB write; only the resulting target is
// persisted. The validated target path is then only consumed by frontend.
$tracked=banner('none/','Tarifcheck Banner');
$tracked['id']=899;
$tracked['tracking_url']='https://a.partner-versicherung.de/click.php?deep=hausratversicherung';
$tracked['destination_url']=$tracked['tracking_url'];
$tracked['payload']=json_encode(array('_destination_source'=>'tracking_checked'));
$GLOBALS['wpdb']->updates=0;
$single=$o->output_assign_banner_targets_from_destination_once($tracked);
ok($single['updated']===1 && $single['mapped']===1,'One entire read-map-save operation succeeds');
ok($GLOBALS['wpdb']->updates===1,'ONLY ONE stored database update, not an intermediate destination overwrite');
$stored=json_decode((string)($GLOBALS['wpdb']->saved[899]['payload']??''),true);
ok(($stored['_source_read_version']??0)===1 && count($single['targets'])===1,
 'Original evidence and single chosen WP target saved together, no second decision');
echo "RC40_SINGLE_CENTRAL_OWNER_WRITE_ONCE_PASS\n";
'''
base=base.replace(insert,php+"\n"+insert,1)
with TemporaryDirectory() as td:
    f=Path(td)/"qa_rc40_original_php.py";f.write_text(base)
    v=run([sys.executable,str(f)],capture_output=True,text=True)
    print(v.stdout[-12500:])
    if v.returncode:print(v.stderr[-6000:])
    assert v.returncode==0,(v.stdout[-8000:],v.stderr[-5000:])
    assert "RC40_SOURCE_FIRST_160_HTML_REAL_PHP_PASS" in v.stdout
    assert "RC40_SINGLE_CENTRAL_OWNER_WRITE_ONCE_PASS" in v.stdout
# Recheck all RC39 owner aliases, missing R3/category, hierarchy, real format
# sizes, and the RC37 diagnostic behavior, not only the new happy path.
qa=(R/"AFFILIATE/RC39_FIXED_BRANCH_OWNER/qa_rc39.py").read_text()
assert "0.1.36-rc39" in qa and "ppar_hab_rc39_tarifcheck_reconcile_v1" in qa
qa=qa.replace("0.1.36-rc39","0.1.37-rc40")
qa=qa.replace("ppar_hab_rc39_tarifcheck_reconcile_v1","ppar_hab_rc40_tarifcheck_reconcile_v1")
with TemporaryDirectory() as td:
    f=Path(td)/"qa_rc39_on_rc40.py";f.write_text(qa)
    v=run([sys.executable,str(f)],capture_output=True,text=True)
    print(v.stdout[-4000:])
    if v.returncode:print(v.stderr[-5000:])
    assert v.returncode==0,(v.stdout[-7000:],v.stderr[-5000:])
print("RC40_ALL_ORIGINAL_PHP_SOURCE_FIRST_AND_OLD_RC23_RC39_OWNER_PASS")
