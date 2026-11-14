#!/usr/bin/env python3
"""Full original-PHP RC44 acceptance: all 160 actual product groups;
negative foreign sibling, real HUB2 vs R3 slot; one fully clickable banner
without redundant CTA. Previous RC42 export security and format QA reused.
No assertions about live page visibility until installed and observed.
"""
from pathlib import Path
from zipfile import ZipFile
from tempfile import TemporaryDirectory
from subprocess import run
import re,sys
R=Path("protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ")
P=R/"PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip"
with ZipFile(P) as z:
    assert len(z.namelist())==36 and z.testzip() is None
    o=z.read("affiliate-portal-router/includes/trait-ppar-output-objects.php").decode()
    m=z.read("affiliate-portal-router/affiliate-portal-router.php").decode()
    assert "Version: 0.1.41-rc44" in m
    assert "ppar_hab_rc44_tarifcheck_reconcile_v1" in o
    assert "'hundeversicherung'=>'hundehaftpflichtversicherung'" in o
    assert "if($r2_exact_owner_only && $key!==$anchor)continue;" in o
    assert "&& isset($matches['hub_after_cards'])" in o
    assert "ppar-overview-wide-banner-link" in m
    assert "ppar-overview-wide-banner-cta-wrap" not in m
    assert "<!--ppar-overview-cta-v67280-->" not in m
    assert "ppar-affiliate-label" in m and "Anzeige" in m

# Reuse the COMPLETE ORIGINAL RC43 PHP owner QA, changing exactly the TWO
# expected outcomes whose prior semantics were proven wrong in the screenshot.
old=(R/"AFFILIATE/RC43_REAL_DEEP_OWNER/qa_rc43.py").read_text()
assert old.count("'hundeversicherung'=>765")==1
old=old.replace("'hundeversicherung'=>765","'hundeversicherung'=>786")
assert old.count("0.1.40-rc43")>=1
old=old.replace("0.1.40-rc43","0.1.41-rc44")
old=old.replace("ppar_hab_rc43_tarifcheck_reconcile_v1",
                "ppar_hab_rc44_tarifcheck_reconcile_v1")
original_check="""ok($p['target']['id']===765
 && in_array('page:hundehaftpflichtversicherung',$p['path_target_keys'],true)
 && !in_array('page:private-rentenversicherung',$p['path_target_keys'],true),
 'General Haftpflicht reaches only corresponding R2 subtree, not Vorsorge');"""
new_check="""ok($p['target']['id']===765
 && count($p['path_target_keys'])===1
 && in_array('page:haftpflicht-und-rechtsschutz',$p['path_target_keys'],true)
 && !in_array('page:tierkrankenversicherung',$p['path_target_keys'],true)
 && !in_array('page:rechtsschutzversicherung',$p['path_target_keys'],true),
 'Generic Haftpflicht R2 appears ONLY on its parent; no Tierkranken or Rechtsschutz leakage');"""
assert old.count(original_check)==1
old=old.replace(original_check,new_check)
anchor="echo \"RC43_ACTUAL_160_DEEP_SOURCE_PHRASES_ALL_CENTRAL_OWNER_PASS\\n\";"
assert old.count(anchor)==1
extra=r'''
// Source visual confirmation from real screenshot: Hundeversicherung
// 728x90 displays Hundehaftpflicht; it MUST NOT appear on Tierkranken.
$dog=banner('tarifcheck/','Tarifcheck Banner');
$dog['tracking_url']='https://a.partner-versicherung.de/click.php?deep=hundeversicherung';
$dog['payload']=json_encode(array('_destination_source'=>'tracking_checked',
 '_source_read_version'=>2,'title_source'=>'manual_missing',
 '_source_evidence'=>array('destination'=>'hundeversicherung','provider'=>'','text'=>'','image_hint'=>'')));
$dogPlan=$o->hb_rc31_insurance_banner_plan($dog,$portal,$GLOBALS['targets'],array('page','category'));
ok($dogPlan['status']==='ready' && $dogPlan['target']['id']===786
 && in_array('page:hundehaftpflichtversicherung',$dogPlan['path_target_keys'],true)
 && !in_array('page:tierkrankenversicherung',$dogPlan['path_target_keys'],true),
 'Actual Hundehaftpflicht source maps to R3 786 and NEVER to Tierkranken 815');

// R2 types without their own true R3 belong to their genuine R2 ONLY.
// Never classify Riester as private health or unrelated insurance.
$riester=$dog;
$riester['payload']=json_encode(array('_destination_source'=>'tracking_checked',
 '_source_read_version'=>2,'title_source'=>'manual_missing',
 '_source_evidence'=>array('destination'=>'riester-rente','provider'=>'','text'=>'','image_hint'=>'')));
$r2=$o->hb_rc31_insurance_banner_plan($riester,$portal,$GLOBALS['targets'],array('page','category'));
ok($r2['status']==='ready' && $r2['target']['id']===766
 && count($r2['path_target_keys'])===1
 && in_array('page:krankenversicherung-und-vorsorge',$r2['path_target_keys'],true)
 && !in_array('page:private-krankenversicherung',$r2['path_target_keys'],true),
 'R2 Riester remains R2 only, not unconnected R3 private health');
echo "RC44_R2_ONLY_AND_HUNDEHAFTPFLICHT_R3_GUARD_PASS\n";
'''
old=old.replace(anchor,extra+"\n"+anchor,1)
with TemporaryDirectory() as td:
    p=Path(td)/"qa_rc43_on_rc44.py"
    p.write_text(old)
    q=run([sys.executable,str(p)],capture_output=True,text=True)
    print(q.stdout[-12000:])
    if q.returncode:print(q.stderr[-6500:])
    assert q.returncode==0,(q.stdout[-11000:],q.stderr[-6500:])
    assert "RC44_R2_ONLY_AND_HUNDEHAFTPFLICHT_R3_GUARD_PASS" in q.stdout
    assert "RC43_ACTUAL_160_DEEP_SOURCE_PHRASES_ALL_CENTRAL_OWNER_PASS" in q.stdout

# Prove exact original, unmodified PHP slot owner uses the ACTIVE R2 hub
# surface, and R3 retains its category surface; no frontend redecision.
def method(source,name):
    p=re.search(r"(?:private|public)\s+function\s+"+re.escape(name)+r"\s*\(",source)
    assert p is not None,name
    start=source.index("{",p.end());depth=0
    for i in range(start,len(source)):
        if source[i]=="{":depth+=1
        elif source[i]=="}":
            depth-=1
            if depth==0:return source[p.start():i+1].replace("private function","public function",1)
    raise AssertionError(name)
source_php=method(o,"output_format_slot")
row_rule_php=method(o,"output_row_matches_slot_rule")
php=r'''<?php
error_reporting(E_ERROR|E_PARSE);
function sanitize_key($s){return strtolower(preg_replace('/[^a-z0-9_\-]/','',strtolower((string)$s)));}
function absint($n){return abs((int)$n);}
function is_wp_error($x){return $x instanceof WP_Error;}
class WP_Error {public function __construct($code,$message){$this->code=$code;$this->message=$message;}
 public $code,$message;}
function ok($value,$desc){if(!$value){fwrite(STDERR,"FAIL ".$desc."\n");exit(9);} echo "PASS ".$desc."\n";}
class OriginalSlotOwner {
 public function output_slot_matrix($portal){
  $base=array('creative_type'=>'banner','ratio_min'=>2.5,'ratio_max'=>12,
   'min_width'=>300,'min_height'=>60,'target_types'=>array('page'),
   'upscale_max'=>1.1,'crop'=>'contain');
  return array('product_after_category_tiles'=>array_merge($base,array(
      'target_contexts'=>array('hub2','leaf','category','leaf_category'))),
      'hub_after_cards'=>array_merge($base,array('target_contexts'=>array('hub1','hub2'))));
 }
 public function output_allows_provisional_ebay_product_asset($row){return false;}
 public function hb_insurance_scope($target){return 'insurance';}
 public function output_portal_decision($portal,$hash){return array();}
 public function control_slot_gate($portal,$slot){return true;}
 METHODS
}
$owner=new OriginalSlotOwner();
$banner=array('creative_type'=>'banner','width'=>728,'height'=>90,'identity_hash'=>'some-id');
$portal=array('local'=>true,'key'=>'wp-1-hab-und-bewahr-de');
$hub2=array('type'=>'page','id'=>765,'context'=>'hub2','label'=>'Haftpflicht & Rechtsschutz');
$leaf=array('type'=>'page','id'=>786,'context'=>'category','label'=>'Hundehaftpflichtversicherung');
$hub2Slot=$owner->output_format_slot($banner,$portal,$hub2,'banner');
ok(is_array($hub2Slot) && $hub2Slot['slot_id']==='hub_after_cards',
  'Existing insurance R2 selects its real hub_after_cards surface');
$leafSlot=$owner->output_format_slot($banner,$portal,$leaf,'banner');
ok(is_array($leafSlot) && $leafSlot['slot_id']==='product_after_category_tiles',
  'Existing R3 uses its real product_after_category_tiles surface');
$other=$portal;$other['local']=false;
$untouched=$owner->output_format_slot($banner,$other,$hub2,'banner');
ok(is_array($untouched) && $untouched['slot_id']==='product_after_category_tiles',
  'Non-Hab portal unchanged');
echo "RC44_REAL_PHP_R2_R3_SLOT_CORRECTION_PASS\n";
'''
php=php.replace(" METHODS",source_php+"\n"+row_rule_php)
with TemporaryDirectory() as td:
    f=Path(td)/"original_source_slot.php"
    f.write_text(php)
    check=run(["php","-l",str(f)],capture_output=True,text=True)
    assert check.returncode==0,check.stderr
    result=run(["php",str(f)],capture_output=True,text=True)
    print(result.stdout)
    if result.returncode:print(result.stderr)
    assert result.returncode==0,(result.stdout,result.stderr)
    assert "RC44_REAL_PHP_R2_R3_SLOT_CORRECTION_PASS" in result.stdout

# This is the original runtime image markup: the entire image is linked.
# No extra CTA is printed, other non-image blocks remain untouched.
start=m.index("if ($is_overview_wide_banner_slot)",m.index("private function",m.index("ppar-overview-wide-banner-link")-6000)) if False else m.index("ppar-overview-wide-banner-link")
section=m[max(0,start-1500):start+1300]
assert "href=\"' . esc_url($url)" in section
assert "<img class=\"ppar-overview-wide-banner-image\"" in section
assert "Mehr erfahren" not in section
assert "<!--ppar-overview-cta-v67280-->" not in section
print("RC44_ONE_CLICKABLE_IMAGE_NO_EXTRA_BUTTON_AND_AD_LABEL_PRESERVED_PASS")

with ZipFile(P) as z,TemporaryDirectory() as td:
    count=0
    for n in z.namelist():
        if not n.endswith(".php"):continue
        f=Path(td)/n.replace('/','_')
        f.write_bytes(z.read(n))
        r=run(["php","-l",str(f)],capture_output=True,text=True)
        assert r.returncode==0,(n,r.stderr)
        count+=1
    assert count>=25,count
print("RC44_FULL_25PHP_AND_ORIGINAL_PARTNER_QA_PASS",count)
