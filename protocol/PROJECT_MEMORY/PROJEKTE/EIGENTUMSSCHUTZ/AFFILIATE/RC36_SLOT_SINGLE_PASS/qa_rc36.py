#!/usr/bin/env python3
"""Original packed PHP: 4 banner formats, 4 contexts, real slot and frontend checks."""
from pathlib import Path
from zipfile import ZipFile
from tempfile import TemporaryDirectory
from subprocess import run
import re
R=Path('protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ')
Z=R/'PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip'
with ZipFile(Z) as z:
    assert z.testzip() is None and len(z.namelist())==36
    m=z.read('affiliate-portal-router/affiliate-portal-router.php').decode()
    o=z.read('affiliate-portal-router/includes/trait-ppar-output-objects.php').decode()
    b=z.read('affiliate-portal-router/includes/class-ppar-hab-bewahr-bridge.php').decode()
    css=z.read('affiliate-portal-router/assets/frontend.css').decode()
    assert 'Version: 0.1.33-rc36' in m
    assert 'ppar_hab_rc36_tarifcheck_reconcile_v1' in o
    assert '[data-ppar-slot="product_after_category_tiles"] .ppar-banner-image' in css
    assert '[data-ppar-slot="hub_after_cards"] .ppar-banner-image' in css
    def method(src,name):
        p=re.search(r'    (?:public|private|protected)(?:\s+static)? function '+re.escape(name)+r'\s*\(',src)
        assert p,name
        e=src.index('\n    }\n',p.start())+7
        return src[p.start():e].replace('private function ','public function ',1)
    bridge=method(b,'slot_matrix')
    output='\n'.join(method(o,x) for x in ['output_row_matches_slot_rule','output_format_slot','output_auto_contract_banner_allowed'])
    runtime=method(m,'campaign_matches_contract_slot_rule')
    harness=r'''<?php
function absint($x){return abs((int)$x);}
function sanitize_key($x){return strtolower(preg_replace('/[^a-z0-9_\-]/','',strtolower((string)$x)));}
function sanitize_text_field($x){return trim(strip_tags((string)$x));}
function esc_url_raw($x){return (string)$x;}
function wp_http_validate_url($x){return str_starts_with((string)$x,'https://');}
function is_wp_error($x){return $x instanceof WP_Error;}
function ok($c,$s){if(!$c){fwrite(STDERR,"FAIL $s\n");exit(8);}echo "PASS $s\n";}
class WP_Error {private $text;public function __construct($a,$b){$this->text=$b;}public function get_error_message(){return $this->text;}}
class PPAR_HB_Integration {
 public static function verified_nodes(){return array('core:world:insurance'=>array('id'=>'core:world:insurance'));}
 BRIDGE
}
class Actual {
 public function output_slot_matrix($portal){return PPAR_HB_Integration::slot_matrix(array(),$portal,'');}
 public function hb_insurance_scope($ctx){
   $id=absint(($ctx['post_type']??'')==='category' ? (($ctx['term_ids']??array())[0]??0) : ($ctx['post_id']??0));
   return in_array($id,array(100,110,111,112),true)?'insurance':'other';
 }
 public function output_portal_decision($a,$b){return array();}
 public function output_allows_provisional_ebay_product_asset($r){return false;}
 public function control_slot_gate($p,$s){return true;}
 public function output_row_image_hash($row){return str_repeat('a',64);}
 public function article_banner_dimensions($x){
   $d=explode('x',(string)($x['dimensions']??'0x0'));
   return array((int)$d[0],(int)($d[1]??0),'measured');
 }
 public function runtime_contract_slot_rule($slot){
   $m=$this->output_slot_matrix(array('adapter'=>'wordpress_local'));
   return $m[$slot]??array();
 }
 OUTPUT
 RUNTIME
}
$o=new Actual();
$portal=array('adapter'=>'wordpress_local','local'=>true,'key'=>'hab');
$target1=array('type'=>'page','id'=>100,'context'=>'hub1');
$target2=array('type'=>'page','id'=>110,'context'=>'hub2');
$target3=array('type'=>'page','id'=>111,'context'=>'leaf');
$target4=array('type'=>'category','id'=>112,'context'=>'leaf_category');
$targetOther=array('type'=>'page','id'=>900,'context'=>'leaf');
foreach(array(array(728,90),array(468,60),array(300,250),array(125,125)) as $dim){
  $row=array('creative_type'=>'banner','width'=>$dim[0],'height'=>$dim[1],
             'identity_hash'=>str_repeat('b',64),'provider'=>'manual',
             'source_status'=>'active','availability_state'=>'active',
             'tracking_url'=>'https://www.tarifcheck.de/test',
             'payload'=>json_encode(array('_dimension_state'=>'verified','_image_sha256'=>str_repeat('a',64))));
  foreach(array($target1,$target2,$target3,$target4) as $target){
    $slot=$o->output_format_slot($row,$portal,$target,'banner');
    ok(!is_wp_error($slot),"Real insurance slot ".$dim[0]."x".$dim[1]." target ".$target['id']);
    $want=$target['id']===100?'hub_after_cards':'product_after_category_tiles';
    ok($slot['slot_id']===$want,'Actual design slot identity');
    $class=array('status'=>'ready','target'=>$target);
    ok($o->output_auto_contract_banner_allowed($row,$class,$slot,'portal_banner'),'Actual materializer allows verified size');
  }
  if($dim[0]<=300){
    $no=$o->output_format_slot($row,$portal,$targetOther,'banner');
    ok(is_wp_error($no),'Unrelated physical world unchanged for square/rectangle');
  }
}
foreach(array(array(160,600),array(120,600),array(1,1)) as $dim){
 $row=array('creative_type'=>'banner','width'=>$dim[0],'height'=>$dim[1],
            'identity_hash'=>str_repeat('d',64));
 ok(is_wp_error($o->output_format_slot($row,$portal,$target3,'banner')),'Tall/tiny formats have no invented category slot');
}
$canonical=array('source'=>'output_object_v4','creative_type'=>'banner',
   'auto_topic_reason'=>'HB_INSURANCE_CANONICAL:hab_insurance_specific_verified',
   'placements'=>array('hub_after_cards','product_after_category_tiles'),
   'dimensions'=>'125x125','render_mode'=>'image_link',
   'image_url'=>'https://www.tarifcheck.de/b.png');
ok($o->campaign_matches_contract_slot_rule($canonical,'product_after_category_tiles'),
   'Public runtime consumes stored category format without redecision');
ok($o->campaign_matches_contract_slot_rule($canonical,'hub_after_cards'),
   'Public runtime consumes stored hub format without redecision');
ok(!$o->campaign_matches_contract_slot_rule($canonical,'journal_banner'),
   'Public runtime does not invent journal placements');
$old=$canonical;$old['source']='manual';
ok(!$o->campaign_matches_contract_slot_rule($old,'product_after_category_tiles'),
   'Classic physical-world geometry check unchanged');
echo "RC36_REAL_ORIGINAL_PHP_FORMAT_TO_PUBLIC_PASS\n";
'''
    harness=harness.replace('BRIDGE',bridge).replace('OUTPUT',output).replace('RUNTIME',runtime)
    with TemporaryDirectory() as td:
        p=Path(td)/'qa.php';p.write_text(harness)
        l=run(['php','-l',str(p)],capture_output=True,text=True)
        assert l.returncode==0,(l.stdout,l.stderr)
        res=run(['php',str(p)],capture_output=True,text=True)
        print(res.stdout)
        assert res.returncode==0,(res.stdout,res.stderr)
        assert 'RC36_REAL_ORIGINAL_PHP_FORMAT_TO_PUBLIC_PASS' in res.stdout
    with TemporaryDirectory() as td:
        names=[n for n in z.namelist() if n.endswith('.php')]
        assert len(names)==25
        for i,name in enumerate(names):
            p=Path(td)/f'{i}.php';p.write_bytes(z.read(name))
            v=run(['php','-l',str(p)],capture_output=True,text=True)
            assert v.returncode==0,(name,v.stderr)
print('RC36_ALL_25_PACKED_PHP_LINT_PASS')
