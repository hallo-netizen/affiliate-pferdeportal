#!/usr/bin/env python3
"""RC34 original-PHP gates: direct partner identity, no extra target writer,
same existing migration recognizes old original labels, existing admin reports
actual live DB states without reassigning a banner or using any tracking URL.
"""
from pathlib import Path
from zipfile import ZipFile
from tempfile import TemporaryDirectory
from subprocess import run
import re
R=Path("protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ")
P=R/"PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip"
with ZipFile(P) as z:
    assert z.testzip() is None and len(z.namelist())==36
    m=z.read("affiliate-portal-router/affiliate-portal-router.php").decode()
    o=z.read("affiliate-portal-router/includes/trait-ppar-output-objects.php").decode()
    c=z.read("affiliate-portal-router/includes/trait-ppar-creative-library.php").decode()
    assert "Version: 0.1.31-rc34" in m
    assert "ppar_hab_rc34_tarifcheck_reconcile_v1" in o
    assert "hab_rc34_tarifcheck_report()" in c
    assert "LOWER(partner_name) LIKE %s" in o
    assert "OR LOWER(destination_url) LIKE %s" in o
    assert "creative_library_destination_map','creative_library_general_fallback'" in o
    assert c.count("hab_rc34_tarifcheck_report()")==2
    def method(src,name):
        match=re.search(r"    (?:public|private|protected) function "+re.escape(name)+r"\s*\(",src)
        assert match,name
        end=src.index("\n    }\n",match.start())+7
        return src[match.start():end].replace("private function","public function",1)
    methods="\n".join(method(s,n) for s,n in [
        (o,"output_text"),
        (o,"output_comparison_banner_partner"),
        (o,"hb_rc31_reconcile_stored_tarifcheck_once"),
        (o,"output_store_banner_library_assignment"),
        (o,"output_banner_library_records"),
        (c,"hab_rc34_tarifcheck_report")
    ])
    harness=r'''<?php
define('ARRAY_A','ARRAY_A');
function is_admin(){return true;}
function current_user_can($x){return true;}
function absint($n){return abs((int)$n);}
function sanitize_key($v){return strtolower(preg_replace('/[^a-z0-9_-]/','',strtolower((string)$v)));}
function sanitize_text_field($v){return trim(strip_tags((string)$v));}
function esc_html($x){return htmlspecialchars((string)$x,ENT_QUOTES);}
function esc_url_raw($x){return (string)$x;}
function wp_strip_all_tags($x){return strip_tags((string)$x);}
function remove_accents($s){return str_replace(array('ä','ö','ü','ß'),array('ae','oe','ue','ss'),(string)$s);}
function wp_parse_url($url,$component=-1){return parse_url($url,$component);}
function wp_json_encode($x,$flags=0){return json_encode($x,$flags);}
function wp_date($format){return '13.11.2026 15:00';}
function get_post_status($id){return (int)$id===701?'publish':'draft';}
function get_option($name,$default=null){return $GLOBALS['options'][$name]??$default;}
function update_option($name,$value,$autoload=false){$GLOBALS['options'][$name]=$value;}
function ok($value,$message){if(!$value){fwrite(STDERR,"FAIL ".$message."\n");exit(2);}echo "PASS ".$message."\n";}
class PPAR_HB_Integration {}
class FakeDB {
 public $rows=array(),$obj=array(),$sqls=array(),$updates=array();
 public $prefix='wp_';
 public function prepare($sql,...$args){return vsprintf(str_replace(array('%s','%d'),array("'%s'",'%d'),$sql),$args);}
 public function get_results($sql,$format){$this->sqls[]=$sql;
     if(strpos($sql,'ppar_output_objects')!==false)return $this->obj;
     preg_match('/id>([0-9]+)/',$sql,$match);
     $start=(int)($match[1]??0);
     return array_slice(array_values(array_filter($this->rows,fn($r)=>(int)$r['id']>$start)),0,251);
 }
 public function update($table,$data,$where){$this->updates[]=array($table,$data,$where);return 1;}
}
$GLOBALS['wpdb']=new FakeDB();
$GLOBALS['options']=array();
class Actual {
 public function creative_library_table(){return 'wp_ppar_creative_library';}
 public function output_objects_table(){return 'wp_ppar_output_objects';}
 public function output_local_portal_key(){return 'wp-1-hab-und-bewahr-de';}
 public function output_assign_banner_targets_from_destination_once($row){
    $GLOBALS['mapped'][]=(int)$row['id'];
    return array('updated'=>1,'mapped'=>1,'targets'=>array(
     array('portal_key'=>'wp-1-hab-und-bewahr-de','state'=>'mapped',
       'target_key'=>'page:hausratversicherung','source'=>'hab_insurance_specific_verified')));
 }
 public function output_plan_creative($row,$materialize){
    $GLOBALS['planned'][]=(int)$row['id'];return array('active'=>1);
 }
 ACTUAL
}
$o=new Actual;
$verified=json_encode(array('_dimension_state'=>'verified','_image_sha256'=>str_repeat('c',64)));
$pending=json_encode(array('_dimension_state'=>'pending','_image_sha256'=>''));
function source_row($id,$name,$pid,$host,$payload,$map='[]') {
  return array('id'=>$id,'provider'=>'direct','creative_type'=>'banner',
    'partner_name'=>$name,'partner_external_id'=>$pid,
    'destination_url'=>$host,'title'=>'Hausrat '.$id,
    'identity_hash'=>str_repeat((string)$id,64),
    'topic_targets'=>$map,'topic_status'=>'auto_verified',
    'width'=>728,'height'=>90,'payload'=>$payload,
    'source_status'=>'active','availability_state'=>'active','review_status'=>'approved');
}
$a=source_row(1,'Tarifcheck','tarifcheck','https://tracking.example/test',$verified);
$b=source_row(2,'TC Direkt','tarifcheck','https://tracking.example/test',$verified);
$c=source_row(3,'Tarifcheck Deutschland','newprogram','https://tracking.example/test',$verified);
$d=source_row(4,'Partner','other','https://www.tarifcheck.de/hausrat',$verified);
$e=source_row(5,'Check24','check24','https://www.check24.de/hausrat',$verified);
ok($o->output_comparison_banner_partner($a)==='tarifcheck','Direct owner recognized');
ok($o->output_comparison_banner_partner($b)==='tarifcheck','Direct registered ID recognized despite different visible name');
ok($o->output_comparison_banner_partner($c)==='tarifcheck','Human legacy label recognized using same owner');
ok($o->output_comparison_banner_partner($d)==='tarifcheck','Real Tarifcheck destination recognized');
ok($o->output_comparison_banner_partner($e)==='check24','Unrelated insurer not mislabeled Tarifcheck');
$GLOBALS['wpdb']->rows=array($a,$b,$c,$d,$e);
$GLOBALS['mapped']=array();$GLOBALS['planned']=array();
$_GET['page']='affiliate-portal-creative-library';
$o->hb_rc31_reconcile_stored_tarifcheck_once();
ok($GLOBALS['mapped']===array(1,2,3,4),'Existing single rebind handles all four real partner evidence paths');
ok($GLOBALS['planned']===array(1,2,3,4),'Each matched verified original planned once, no second scheduler');
ok(str_contains($GLOBALS['wpdb']->sqls[0],'LOWER(partner_name) LIKE')
 && str_contains($GLOBALS['wpdb']->sqls[0],'LOWER(destination_url) LIKE'),
   'Actual SQL uses same broad query contract without missing legit partner names');
ok(!empty($GLOBALS['options']['ppar_hab_rc34_tarifcheck_reconcile_v1']['complete']),
   'Existing single run reaches deterministic complete state');
$o->hb_rc31_reconcile_stored_tarifcheck_once();
ok($GLOBALS['mapped']===array(1,2,3,4),'No duplicate recompute on next admin visit');

// One canonical stored assignment must never be rewritten by the fallback
// second writer, including the historic library-destination and general maps.
$classification=array('source'=>'creative_library_destination_map',
 'confidence'=>100,'target'=>array('key'=>'page:hausratversicherung','label'=>'Hausrat'));
$before=count($GLOBALS['wpdb']->updates);
$o->output_store_banner_library_assignment($a,array('key'=>'wp-1-hab-und-bewahr-de'),$classification,array('hub_after_cards'));
ok(count($GLOBALS['wpdb']->updates)===$before,'Shared secondary writer does NOT overwrite existing portal target map');
$classification['source']='hab_insurance_specific_verified';
$o->output_store_banner_library_assignment($a,array('key'=>'wp-1-hab-und-bewahr-de'),$classification,array('hub_after_cards'));
ok(count($GLOBALS['wpdb']->updates)===$before,'Insurance canonical map also never rewritten');

// Real observed stages, from saved DB not mock decision counters:
$map=json_encode(array(array('portal_key'=>'wp-1-hab-und-bewahr-de','state'=>'mapped',
 'target_key'=>'page:hausratversicherung','source'=>'hab_insurance_specific_verified')));
$pending_row=source_row(8,'Tarifcheck Deutschland','newprogram','https://tracking.example/test',$pending);
$mapped_row=source_row(9,'Tarifcheck','tarifcheck','https://tracking.example/test',$verified,$map);
$active_row=source_row(10,'Tarifcheck','tarifcheck','https://tracking.example/test',$verified,$map);
$GLOBALS['wpdb']->rows=array($pending_row,$mapped_row,$active_row);
$GLOBALS['wpdb']->obj=array(array('creative_identity_hash'=>str_repeat('1',64),
  'status'=>'published','campaign_post_id'=>701,'decision_reason'=>'','slot_id'=>'hub_after_cards'));
ob_start();
$o->hab_rc34_tarifcheck_report();
$html=ob_get_clean();
ok(str_contains($html,'3 Banner gefunden'),'Real status report counts existing provider rows');
ok(str_contains($html,'Bild offen: 1'),'Real report finds unfinished picture evidence');
ok(str_contains($html,'Ausgabe fehlt: 2'),'Real report shows missing materialized campaigns, not a fake success');
ok(str_contains($html,'Hausrat 9') && str_contains($html,'Zuordnung vorhanden, aber keine Ausgabe erzeugt'),
   'Per-original root blocker shown in user-readable German');
ok(!str_contains($html,'https://tracking.example/'),'Tracking URLs never exposed in log');
ok(isset($GLOBALS['options']['ppar_hab_rc34_tarifcheck_last_check']['counts']),
   'Aggregated error checkpoint retained in existing WP options, no new DB table');
echo "HAB_RC34_REAL_PHP_SINGLE_OWNER_AND_LIVE_STATUS_DIAG_PASS\n";
'''
    harness=harness.replace("ACTUAL",methods)
    with TemporaryDirectory() as td:
        p=Path(td)/"qa.php";p.write_text(harness)
        l=run(["php","-l",str(p)],capture_output=True,text=True)
        assert l.returncode==0,(l.stdout,l.stderr)
        r=run(["php",str(p)],capture_output=True,text=True)
        print(r.stdout)
        assert r.returncode==0,(r.stdout,r.stderr)
        assert "HAB_RC34_REAL_PHP_SINGLE_OWNER_AND_LIVE_STATUS_DIAG_PASS" in r.stdout
    with TemporaryDirectory() as td:
        ps=[n for n in z.namelist() if n.endswith(".php")]
        assert len(ps)==25
        for j,n in enumerate(ps):
            p=Path(td)/f"{j}.php";p.write_bytes(z.read(n))
            l=run(["php","-l",str(p)],capture_output=True,text=True)
            assert l.returncode==0,(n,l.stderr)
print("HAB_RC34_25_PHP_LINT_PASS")
