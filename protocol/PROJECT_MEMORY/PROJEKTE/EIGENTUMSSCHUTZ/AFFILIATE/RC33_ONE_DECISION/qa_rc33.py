#!/usr/bin/env python3
"""Execute actual saved-map reader, single-writer, actual campaign target rank,
insurance page safety gate, RC31 branch resolver and 60-row auto-migration.
No simulation of plugin logic with guessed outcome functions.
"""
from pathlib import Path
from tempfile import TemporaryDirectory
from subprocess import run
from zipfile import ZipFile
from hashlib import sha256
import re

R=Path("protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ")
Z=R/"PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip"
with ZipFile(Z) as z:
    assert z.testzip() is None and len(z.namelist())==36
    main=z.read("affiliate-portal-router/affiliate-portal-router.php").decode()
    o=z.read("affiliate-portal-router/includes/trait-ppar-output-objects.php").decode()
    auto=z.read("affiliate-portal-router/includes/trait-ppar-automation-suite.php").decode()
    assert "Version: 0.1.30-rc33" in main
    assert main.count("private function hb_insurance_banner_rank(")==1
    assert main.count("private function hb_insurance_campaign_allowed(")==1
    assert "HB_INSURANCE_CANONICAL:" in o
    assert "hab_insurance_specific_verified" in o
    assert "ppar_hab_rc33_tarifcheck_reconcile_v1" in o
    assert "&& !($this->hb_insurance_scope($rank_context)" not in main
    assert "if($hb_scope==='insurance')return $this->hb_insurance_banner_rank" in main

    def method(src,name):
        m=re.search(r"    (?:private|public|protected)(?: static)? function "+re.escape(name)+r"\s*\(",src)
        assert m,name
        start=m.start()
        end=src.index("\n    }\n",start)+7
        result=src[start:end]
        assert result.count("function "+name+"(")==1
        return result.replace("private function","public function",1)
    definitions={
      "main":[
        "hb_insurance_scope",
        "hb_insurance_banner_rank",
        "hb_insurance_campaign_allowed",
        "campaign_match_rank",
      ],
      "out":[
        "output_banner_library_records",
        "output_banner_stored_destination_classification",
        "output_store_banner_library_assignment",
        "output_resolve_target_key",
        "output_target_key_matches",
        "output_target_identity_keys",
        "output_campaign_target_key",
      ],
      "auto":[
        "automation_campaign_exact_target_rank_uncached",
        "automation_normalize_target_key",
      ]
    }
    actual="\n".join(method({"main":main,"out":o,"auto":auto}[kind],name)
                     for kind,names in definitions.items() for name in names)
    harness=r'''<?php
function absint($n){return abs((int)$n);}
function sanitize_key($s){return strtolower(preg_replace('/[^a-zA-Z0-9_-]/','',strtolower((string)$s)));}
function sanitize_text_field($s){return trim(strip_tags((string)$s));}
function wp_strip_all_tags($s){return strip_tags((string)$s);}
function remove_accents($s){return str_replace(array('ä','ü','ö','ß'),array('ae','ue','oe','ss'),(string)$s);}
function esc_url_raw($s){return (string)$s;}
function is_wp_error($x){return false;}
function ok($v,$label){if(!$v){fwrite(STDERR,"FAIL ".$label."\n");exit(8);}echo "PASS ".$label."\n";}
define('ARRAY_A','ARRAY_A');
class FakeWPDB {
  public $updates=array();
  public function update($table,$data,$where){$this->updates[]=array($table,$data,$where);return 1;}
}
$GLOBALS['wpdb']=new FakeWPDB();
$GLOBALS['nodes']=array(
 'core:world:insurance'=>array('id'=>'core:world:insurance','parent'=>'','type'=>'page','wp_id'=>100,'name'=>'Versicherungen'),
 'ins:r2:sach'=>array('id'=>'ins:r2:sach','parent'=>'core:world:insurance','type'=>'page','wp_id'=>101,'name'=>'Sachversicherungen'),
 'ins:r3:hausrat'=>array('id'=>'ins:r3:hausrat','parent'=>'ins:r2:sach','type'=>'page','wp_id'=>102,'name'=>'Hausratversicherung'),
 'ins:leaf:hausrat'=>array('id'=>'ins:leaf:hausrat','parent'=>'ins:r3:hausrat','type'=>'category','wp_id'=>103,'name'=>'Hausrat Rat'),
 'ins:r2:fahr'=>array('id'=>'ins:r2:fahr','parent'=>'core:world:insurance','type'=>'page','wp_id'=>104,'name'=>'Fahrzeuge'),
 'ins:r3:moto'=>array('id'=>'ins:r3:moto','parent'=>'ins:r2:fahr','type'=>'page','wp_id'=>105,'name'=>'Motorradversicherung'),
 'out:world'=>array('id'=>'out:world','parent'=>'','type'=>'page','wp_id'=>200,'name'=>'Wassermelder'),
);
$GLOBALS['targets']=array(
 array('id'=>100,'type'=>'page','key'=>'page:100','slug'=>'versicherungen','label'=>'Versicherungen'),
 array('id'=>101,'type'=>'page','key'=>'page:101','slug'=>'sachversicherungen','label'=>'Sachversicherungen'),
 array('id'=>102,'type'=>'page','key'=>'page:102','slug'=>'hausratversicherung','label'=>'Hausratversicherung'),
 array('id'=>103,'type'=>'category','key'=>'category:103','slug'=>'hausrat-vergleichen','label'=>'Hausrat vergleichen'),
 array('id'=>104,'type'=>'page','key'=>'page:104','slug'=>'fahrzeuge','label'=>'Fahrzeuge'),
 array('id'=>105,'type'=>'page','key'=>'page:105','slug'=>'motorradversicherung','label'=>'Motorradversicherung'),
 array('id'=>200,'type'=>'page','key'=>'page:200','slug'=>'wassermelder','label'=>'Wassermelder'),
);
class PPAR_HB_Integration {public static function verified_nodes(){return $GLOBALS['nodes'];}}
class TestedActual {
  public $automation_exact_target_rank_request_cache=array();
  public function ranked_campaigns_request_cache_allowed(){return false;}
  public function ranked_campaign_sanitize_key_request_cached($s){return sanitize_key($s);}
  public function output_portal_targets($p){return $GLOBALS['targets'];}
  public function creative_library_table(){return 'wp_ppar_creative_library';}
  public function output_banner_destination_source($r){return 'provider_explicit';}
  public function automation_campaign_exact_target_rank($campaign,$context){
    // Delegate to the actual 9KB WordPress production routine.
    return $this->automation_campaign_exact_target_rank_uncached($campaign,$context);
  }
  public function slot_required_creative_type($s){return 'banner';}
  ACTUAL_METHODS
}
$a=new TestedActual();
$portal=array('key'=>'hab','local'=>true);
$record=array('portal_key'=>'hab','state'=>'mapped','source'=>'hab_insurance_specific_verified',
 'level'=>'verified_branch','target_key'=>'page:102','confidence'=>100,
 'path_target_keys'=>array('page:hausratversicherung','category:hausrat-vergleichen'),
 'target_label'=>'Hausratversicherung');
$row=array('id'=>99,'creative_type'=>'banner','partner_name'=>'Tarifcheck',
  'title'=>'Hausratversicherung','topic_targets'=>json_encode(array($record)),
  'destination_url'=>'https://www.tarifcheck.de/hausratversicherung');
$stored=$a->output_banner_stored_destination_classification($row,$portal);
ok(is_array($stored)&&$stored['status']==='ready','Actual saved classification reads existing source');
ok($stored['source']==='hab_insurance_specific_verified','Exact original single owner survives read');
ok(count($stored['_ppar_banner_target_keys'])===2,'Exact page and leaf target keys survive read');
ok(strpos($stored['reason'],'HB_INSURANCE_CANONICAL:')===0,'Verifiable marker for read-only display');
$a->output_store_banner_library_assignment($row,$portal,$stored,array('product_after_category_tiles'));
ok(count($GLOBALS['wpdb']->updates)===0,'Second writer cannot erase original subcategory target map');
ok($row['topic_targets']===json_encode(array($record)),'Original stored creative never edited');

$campaign=array(
 'source'=>'output_object_v4','creative_type'=>'banner',
 'assignment_mode'=>'page_tree','auto_topic_reason'=>$stored['reason'],
 'automation_target_keys'=>$stored['_ppar_banner_target_keys'],
 'title'=>'Hausratversicherung', 'network'=>'manual'
);
$hausrat=array('post_type'=>'page','post_id'=>102,'hb_verified_node_id'=>'ins:r3:hausrat',
 'primary_slug'=>'hausratversicherung','slot_type'=>'product_after_category_tiles',
 'slugs'=>array('versicherungen','sachversicherungen','hausratversicherung'));
$hausratLeaf=array('post_type'=>'category_archive','post_id'=>0,'term_ids'=>array(103),
 'primary_slug'=>'hausrat-vergleichen','slot_type'=>'category_recommendation',
 'slugs'=>array('versicherungen','sachversicherungen','hausratversicherung','hausrat-vergleichen'));
$moto=array('post_type'=>'page','post_id'=>105,'hb_verified_node_id'=>'ins:r3:moto',
 'primary_slug'=>'motorradversicherung','slot_type'=>'product_after_category_tiles',
 'slugs'=>array('versicherungen','fahrzeuge','motorradversicherung'));
$out=array('post_type'=>'page','post_id'=>200,'hb_verified_node_id'=>'out:world',
 'primary_slug'=>'wassermelder','slot_type'=>'product_after_category_tiles','slugs'=>array('wassermelder'));
$mixed=array('post_type'=>'post','post_id'=>301,'term_ids'=>array(103,200),
 'primary_slug'=>'mixed','slot_type'=>'post_inline_banner','slugs'=>array('mixed'));
ok($a->hb_insurance_scope($hausrat)==='insurance','Original HB actual scope says Hausrat insurance');
ok($a->hb_insurance_scope($hausratLeaf)==='insurance','Original HB actual scope says leaf insurance');
ok($a->hb_insurance_scope($out)==='other','Original HB actual scope says physical products outside insurance');
ok(is_array($a->campaign_match_rank($campaign,$hausrat)),'Actual banner matcher allows genuine R3');
ok(is_array($a->campaign_match_rank($campaign,$hausratLeaf)),'Actual banner matcher allows its leaf');
ok($a->campaign_match_rank($campaign,$moto)===null,'Actual matcher rejects sibling motorcycle insurance');
ok($a->campaign_match_rank($campaign,$out)===null,'Actual matcher rejects physical Wassermelder category');
ok(!$a->hb_insurance_campaign_allowed($campaign,$moto,$moto['slot_type']),'Actual final renderer rejects sibling too');
ok($a->hb_insurance_campaign_allowed($campaign,$hausrat,$hausrat['slot_type']),'Actual final renderer allows exact R3');
$changed_title=$campaign;$changed_title['title']='Irgendein Werbetext';
ok(is_array($a->campaign_match_rank($changed_title,$hausrat)),
 'Changing title never triggers a second categorization');
$fake=$campaign;$fake['auto_topic_reason']='Gespeicherte Ziel-URL-Zuordnung';
ok($a->campaign_match_rank($fake,$hausrat)===null,
 'Legacy/noncanonical banner cannot sneak past exact approved mapping');
$other_source=$campaign;$other_source['source']='manual_campaign';
ok($a->campaign_match_rank($other_source,$hausrat)===null,
 'Second manual campaign owner not authorized to override central creative');
$product=$campaign;$product['creative_type']='product';
ok($a->campaign_match_rank($product,$hausrat)===null,
 'Physical product has no insurance banner permission');
$general=$campaign;$general['auto_topic_reason']='HB_INSURANCE_CANONICAL:hab_insurance_general_verified';
$general['automation_target_keys']=array('page:versicherungen','page:hausratversicherung',
 'category:hausrat-vergleichen','page:motorradversicherung');
ok(is_array($a->campaign_match_rank($general,$moto)) && is_array($a->campaign_match_rank($general,$hausrat)),
 'Genuine generic insurance comparison works across ALL explicitly saved insurance branches');

$old=$record;$old['source']='tarifcheck_insurance_all_insurance_categories';
$row['topic_targets']=json_encode(array($old));
$before=$a->output_banner_stored_destination_classification($row,$portal);
ok(($before['status']??'')==='review',
 'Previous overly broad blanket insurance map cannot render before reconciliation');
echo "HAB_RC33_ACTUAL_PHP_CENTRAL_AUTHORITY_E2E_PASS\n";
'''
    harness=harness.replace("ACTUAL_METHODS",actual)
    with TemporaryDirectory() as td:
        p=Path(td)/"smoke.php"
        p.write_text(harness)
        a=run(["php","-l",str(p)],capture_output=True,text=True)
        assert a.returncode==0,(a.stdout,a.stderr)
        r=run(["php",str(p)],capture_output=True,text=True)
        print(r.stdout)
        assert r.returncode==0,(r.stdout,r.stderr)
        code=r.stdout
        assert "HAB_RC33_ACTUAL_PHP_CENTRAL_AUTHORITY_E2E_PASS" in code

    # Prior original full RC31 contract (R1/R2/R3, 65 campaign originals) must
    # still pass with ONLY the new proof/version/one-time cursor adjusted.
    previous=(R/"AFFILIATE/RC31_INSURANCE_CASCADE/qa_rc31.py").read_text()
    previous=previous.replace("Version: 0.1.28-rc31","Version: 0.1.30-rc33")
    previous=previous.replace("ppar_hab_rc31_tarifcheck_reconcile_v1","ppar_hab_rc33_tarifcheck_reconcile_v1")
    with TemporaryDirectory() as td:
        prev=Path(td)/"previous.py"
        prev.write_text(previous)
        r=run(["python3",str(prev)],capture_output=True,text=True)
        print(r.stdout)
        assert r.returncode==0,(r.stdout,r.stderr)

    print("HAB_RC33_REGRESSION_RC31_PLUS_CANONICAL_E2E_PASS",sha256(Z.read_bytes()).hexdigest())
