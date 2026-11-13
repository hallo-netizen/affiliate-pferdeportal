#!/usr/bin/env python3
"""Test ACTUAL PHP code that turns a centrally classified Tarifcheck banner
into an ACTIVE WordPress campaign and retains all its exact descendant keys.
RC31 previously tested mapping but not the complete real campaign publication.
"""
from pathlib import Path
from zipfile import ZipFile
from subprocess import run
from tempfile import TemporaryDirectory
import re
Z=Path("protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ/PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip")
with ZipFile(Z) as z:
    assert z.testzip() is None
    src=z.read("affiliate-portal-router/includes/trait-ppar-output-objects.php").decode()
    def method(name):
        m=re.search(r"    private function "+re.escape(name)+r"\(",src)
        assert m,name
        e=src.index("\n    }\n",m.start())+7
        return src[m.start():e].replace("private function","public function",1)
    code="\n".join(method(n) for n in [
        "output_auto_contract_banner_allowed",
        "output_row_matches_slot_rule",
        "output_row_image_hash",
        "output_campaign_target_key",
        "output_save_local_campaign"
    ])
    harness=r'''<?php
function sanitize_key($x){return strtolower(preg_replace('/[^a-z0-9_-]/','',strtolower((string)$x)));}
function sanitize_text_field($x){return trim(strip_tags((string)$x));}
function sanitize_textarea_field($x){return trim(strip_tags((string)$x));}
function absint($x){return max(0,(int)$x);}
function esc_url_raw($x){return (string)$x;}
function wp_http_validate_url($u){return str_starts_with($u,'https://');}
function update_post_meta($id,$key,$value){$GLOBALS['postmeta'][$id][$key]=$value;}
function delete_post_meta($id,$key){unset($GLOBALS['postmeta'][$id][$key]);}
function sanitize_title($x){return sanitize_key($x);}
function ok($c,$n){if(!$c){fwrite(STDERR,"FAIL ".$n."\n");exit(9);}echo "PASS ".$n."\n";}
define('ARRAY_A','ARRAY_A');
class FakeDB {
 public $saved=array();public $prefix='wp_';
 public function prepare($sql,...$args){return vsprintf(str_replace(array('%d','%s'),array('%d',"'%s'"),$sql),$args);}
 public function get_row($sql,$type){return array('object_key'=>str_repeat('a',60),'campaign_post_id'=>0,'id'=>77);}
 public function update($table,$data,$where){$this->saved[]=array('table'=>$table,'data'=>$data,'where'=>$where);return 1;}
}
$GLOBALS['wpdb']=new FakeDB();
class TestedActual {
 public function output_objects_table(){return 'wp_ppar_output_objects';}
 public function central_blank_campaign(){return array('priority'=>0,'active'=>false);}
 public function output_otto_awin_auto_allowed($row,$classification,$type){return false;}
 public function output_auto_category_large_banner_allowed($row,$classification,$slot,$output_type){return false;}
 public function output_otto_product_placements($target,$slot){return array();}
 public function save_campaign_record($campaign,$campaign_id=0){$GLOBALS['campaign']=$campaign;return 777;}
 public function affiliate_normalize_product_identifiers($identifiers){return array();}
 public function output_allows_provisional_ebay_product_asset($r){return false;}
 ACTUAL_METHODS
}
$o=new TestedActual();
$payload=array('_dimension_state'=>'verified','_image_sha256'=>str_repeat('b',64));
$row=array('id'=>222,'provider'=>'manual','partner_name'=>'Tarifcheck',
 'partner_external_id'=>'tc123','creative_type'=>'banner',
 'title'=>'Hausratversicherung','description'=>'','identity_hash'=>str_repeat('c',64),
 'external_id'=>'tc-house-001',
 'destination_url'=>'https://www.tarifcheck.de/hausratversicherung',
 'tracking_url'=>'https://www.tarifcheck.de/link/123',
 'image_url'=>'https://www.tarifcheck.de/banner.png',
 'width'=>728,'height'=>90,'payload'=>json_encode($payload),
 'source_status'=>'active','availability_state'=>'active'
);
$classification=array('status'=>'ready',
 'source'=>'hab_insurance_specific_verified','confidence'=>100,
 'reason'=>'HB_INSURANCE_CANONICAL:hab_insurance_specific_verified',
 'target'=>array('id'=>102,'type'=>'page','key'=>'page:102',
  'slug'=>'hausratversicherung','label'=>'Hausratversicherung','context'=>'insurance_r3'),
 '_ppar_banner_target_keys'=>array('page:hausratversicherung','category:hausrat-vergleichen'),
 '_ppar_banner_compatible_slots'=>array('product_after_category_tiles'),
);
$slot=array('slot_id'=>'product_after_category_tiles','rule'=>array(
 'creative_type'=>'banner','target_types'=>array('page'),
 'target_contexts'=>array('insurance_r3'),
 'ratio_min'=>5,'ratio_max'=>12,'min_width'=>468,'min_height'=>60,'upscale_max'=>1.1));
ok($o->output_auto_contract_banner_allowed($row,$classification,$slot,'portal_banner'),
   'Original technical gate accepts actual verified 728x90 Tarifcheck banner in target context');
$r=$o->output_save_local_campaign(77,$row,$classification,$slot,'portal_banner');
ok(is_array($r)&&($r['active']??null)===true,'Actual campaign created ACTIVE not a draft');
ok($GLOBALS['campaign']['active']===true && $GLOBALS['campaign']['source']==='output_object_v4',
   'Same central source, no second manual campaign');
ok($GLOBALS['campaign']['auto_topic_reason']==='HB_INSURANCE_CANONICAL:hab_insurance_specific_verified',
   'Canonical one-owner proof survives ACTUAL campaign write');
ok($GLOBALS['campaign']['automation_target_keys']===array('page:hausratversicherung','category:hausrat-vergleichen'),
   'Actual campaign write retains own R3 and lower WP category');
ok($GLOBALS['campaign']['url']===$row['tracking_url'] && $GLOBALS['campaign']['image_url']===$row['image_url'],
   'Original tracking link and image URL retained exactly');
ok($GLOBALS['campaign']['placements']===array('product_after_category_tiles'),
   'Existing design slot used, no altered front-end placement');
ok($GLOBALS['wpdb']->saved[0]['data']['status']==='published',
   'Output object itself becomes published, not just active in memory');
$unverified=$row;$payload['_dimension_state']='pending';
$unverified['payload']=json_encode($payload);
$r2=$o->output_save_local_campaign(77,$unverified,$classification,$slot,'portal_banner');
ok($r2['active']===false,'Unverified image is NEVER published, safety remains');
echo "HAB_RC33_REAL_CAMPAIGN_MATERIALIZATION_PASS\n";
'''
    harness=harness.replace("ACTUAL_METHODS",code)
    with TemporaryDirectory() as d:
        php=Path(d)/"real.php"
        php.write_text(harness)
        lint=run(["php","-l",str(php)],capture_output=True,text=True)
        assert lint.returncode==0,(lint.stdout,lint.stderr)
        r=run(["php",str(php)],capture_output=True,text=True)
        print(r.stdout)
        assert r.returncode==0,(r.stdout,r.stderr)
print("HAB_RC33_MATERIALIZATION_QA_PASS")
