#!/usr/bin/env python3
"""Actual fully packed PHP read-only admin export test: 160 stored source-shaped
records, real verified WordPress tree and stored output objects, NO DB writes.
No access to user's private WordPress database is claimed.
"""
import re,sys,json,os
from pathlib import Path
from zipfile import ZipFile
from tempfile import TemporaryDirectory
from subprocess import run
R=Path('protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ')
P=R/'PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip'
with ZipFile(P) as z:
    assert z.testzip() is None and len(z.namelist())==36
    c=z.read('affiliate-portal-router/includes/trait-ppar-creative-library.php').decode()
    m=z.read('affiliate-portal-router/affiliate-portal-router.php').decode()
    assert "Version: 0.1.39-rc42" in m
    assert m.count("admin_post_ppar_hab_tarifcheck_source_export")==1
    assert c.count("function hb_tarifcheck_source_export()")==1
    assert c.count("Tarifcheck-Bestand einmalig als JSON exportieren")==1
    assert "current_user_can('manage_options')" in c
    assert "check_admin_referer('ppar_hab_tarifcheck_source_export')" in c
    assert "source_hash" in c and "source_evidence_saved" in c
    assert "stored_output_objects" in c
    assert "verified_nodes" in c
    assert "wp_json_encode" in c
    assert "$wpdb->update(" not in c[c.index('function hb_tarifcheck_source_export()'):c.index("public function render_creative_library_page()")]
    assert "$wpdb->insert(" not in c[c.index('function hb_tarifcheck_source_export()'):c.index("public function render_creative_library_page()")]
    assert "$wpdb->delete(" not in c[c.index('function hb_tarifcheck_source_export()'):c.index("public function render_creative_library_page()")]
    start=c.index("public function hb_tarifcheck_source_export()")
    p=c.index("{",start);depth=0;end=None
    for j in range(p,len(c)):
        if c[j]=="{":depth+=1
        if c[j]=="}":
            depth-=1
            if depth==0:end=j+1;break
    assert end is not None
    method=c[start:end]

php=r'''<?php
error_reporting(E_ERROR|E_PARSE|E_WARNING);
define('ARRAY_A','ARRAY_A');
define('JSON_UNESCAPED_UNICODE',256);
function current_user_can($cap){return getenv('TEST_ALLOW')!=='0' && $cap==='manage_options';}
function check_admin_referer($name){if(getenv('TEST_NONCE')==='0')throw new Exception('BAD_NONCE');if($name!=='ppar_hab_tarifcheck_source_export')throw new Exception('WRONG_NONCE_ACTION');}
function wp_die($msg){throw new Exception((string)$msg);}
function home_url($s){$host=getenv('TEST_HOST');return 'https://'.($host?:'hab-und-bewahr.de').$s;}
function wp_parse_url($url,$field){return parse_url($url,$field);}
function absint($n){return abs((int)$n);}
function wp_json_encode($v,$flags=0){return json_encode($v,$flags);}
function nocache_headers(){}
class PPAR_HB_Integration {
 public static function verified_nodes(){
   return array(
    'core:world:insurance'=>array('parent'=>'','type'=>'page',
      'name'=>'Versicherung','slug'=>'versicherung','wp_id'=>101),
    'ins:r2:sach'=>array('parent'=>'core:world:insurance','type'=>'page',
      'name'=>'Haus und Werte','slug'=>'haus-und-werte','wp_id'=>110),
    'ins:r3:hausrat'=>array('parent'=>'ins:r2:sach','type'=>'page',
      'name'=>'Hausratversicherung','slug'=>'hausratversicherung','wp_id'=>111),
   );
 }
}
class DB {
 public $reads=0,$writes=0,$prepared=array();
 public function prepare($sql,...$args){$this->prepared[]=array($sql,$args);return $sql;}
 public function get_results($sql,$mode){
   $this->reads++;
   if(str_contains($sql,'FROM wp_creatives')){
      if(!str_contains($sql,"creative_type='banner'") || !str_contains($sql,"partner_external_id=%s")){
        throw new Exception('READ_ALL_PARTNERS_BUG');
      }
      $rows=array();
      for($i=1;$i<=160;$i++){
         $hash=str_repeat(dechex($i%16),64);
         $is_ready=$i<=80;
         $rows[]=array(
          'id'=>$i,'identity_hash'=>$hash,'provider'=>'manual','partner_name'=>'Tarifcheck',
          'partner_external_id'=>'tarifcheck','external_id'=>'import-'.$i,
          'source_hash'=>str_repeat('a',64),'title'=>'Tarifcheck Banner',
          'description'=>'','tags'=>'','image_url'=>'https://example.test/assets/'.($i%8).'.png',
          'destination_url'=>'https://a.partner-versicherung.de/click.php?aid='.$i,
          'tracking_url'=>'https://a.partner-versicherung.de/click.php?aid='.$i,
          'width'=>300,'height'=>250,'source_status'=>'active','availability_state'=>'active',
          'review_status'=>'review','selected'=>0,'content_scope'=>'unclassified',
          'topic_status'=>$is_ready?'auto_verified':'no_match',
          'topic_score'=>$is_ready?100:0,
          'topic_targets'=>$is_ready?'["page:111"]':'[]',
          'payload'=>json_encode(array(
            '_destination_source'=>'tracking_checked','_source_read_version'=>1,
            '_source_evidence'=>array('destination'=>'','provider'=>'',
                                      'text'=>$is_ready?'Hausratversicherung':'','image_hint'=>''),
            'title_source'=>'manual_missing',
            'html'=>'Hausratversicherung',
            'secret_access_token'=>'MUST_NOT_EXPORT',
            'provider_raw_json'=>'MUST_NOT_EXPORT',
          ))
         );
      }
      return $rows;
   }
   if(str_contains($sql,'FROM wp_output')){
      return array(array('id'=>50,'creative_identity_hash'=>str_repeat('1',64),
         'portal_key'=>'hab-und-bewahr','target_key'=>'page:111','slot_id'=>'hub_after_cards',
         'status'=>'published','campaign_post_id'=>449));
   }
   throw new Exception('UNKNOWN_SQL: '.$sql);
 }
 public function update(){ $this->writes++;throw new Exception('READ_ONLY_BROKEN_UPDATE');}
 public function insert(){ $this->writes++;throw new Exception('READ_ONLY_BROKEN_INSERT');}
 public function delete(){ $this->writes++;throw new Exception('READ_ONLY_BROKEN_DELETE');}
}
$GLOBALS['wpdb']=new DB;
register_shutdown_function(function(){
  $p=$GLOBALS['wpdb'];
  file_put_contents('php://stderr',"READ_CALLS={$p->reads};WRITE_CALLS={$p->writes}\n");
});
class OriginalPHP {
 public function creative_library_table(){return 'wp_creatives';}
 public function output_objects_table(){return 'wp_output';}
 METHOD
}
$o=new OriginalPHP;
try{$o->hb_tarifcheck_source_export();}
catch(Throwable $e){file_put_contents('php://stderr',"BLOCKED:".$e->getMessage()."\n");exit(23);}
'''
assert php.count(" METHOD")==1
php=php.replace(" METHOD",method)
# PHP predefined JSON_UNESCAPED_UNICODE is native and must not be redefined.
php=php.replace("define('JSON_UNESCAPED_UNICODE',256);\n","")
with TemporaryDirectory() as tmp:
    f=Path(tmp)/'original_hab_export.php'
    f.write_text(php)
    lint=run(['php','-l',str(f)],capture_output=True,text=True)
    assert lint.returncode==0,lint.stderr
    normal=run(['php',str(f)],capture_output=True,text=True)
    assert normal.returncode==0,(normal.stderr,normal.stdout[:400])
    assert "READ_CALLS=2;WRITE_CALLS=0" in normal.stderr,normal.stderr
    report=json.loads(normal.stdout)
    assert report['report']=='HAB_TARIFCHECK_STORED_SOURCE_READ_ONLY'
    assert report['count']==160 and len(report['banner_items'])==160
    assert len(report['category_tree'])==3 and report['category_tree_status']=='verified_nodes_read'
    assert len(report['stored_output_objects'])==1
    assert sum(v['topic_status']=='auto_verified' for v in report['banner_items'])==80
    assert sum(v['topic_status']=='no_match' for v in report['banner_items'])==80
    assert report['banner_items'][0]['source_evidence_saved']['html']=='Hausratversicherung'
    assert report['banner_items'][80]['source_evidence_saved']['_source_evidence']['text']==''
    assert report['banner_items'][0]['topic_targets']==['page:111']
    assert 'MUST_NOT_EXPORT' not in normal.stdout
    assert 'secret_access_token' not in normal.stdout
    assert 'provider_raw_json' not in normal.stdout
    assert report['read_only'] is True
    print('RC42_REAL_PHP_READONLY_160_BANNER_80_80_AND_CATEGORY_TREE_EXPORT_PASS',
          report['count'],len(report['category_tree']),len(report['stored_output_objects']))
    for kind,env in [('unauthorized',{'TEST_ALLOW':'0'}),('bad_nonce',{'TEST_NONCE':'0'}),('other_portal',{'TEST_HOST':'pferde-atelier.de'})]:
        v=run(['php',str(f)],capture_output=True,text=True,env={**os.environ,**env})
        assert v.returncode!=0,(kind,v.stdout,v.stderr)
        assert not v.stdout,(kind,"Unauthorized data exported!")
        assert "WRITE_CALLS=0" in v.stderr,(kind,v.stderr)
        print('RC42_SECURITY_DENY_PASS',kind)
# The old RC41 source-first and RC23-RC40 PHP regression ran before build.
# Here we lint EVERY real archived PHP source, preserving other portals.
with ZipFile(P) as z,TemporaryDirectory() as td:
    count=0
    for name in z.namelist():
        if not name.endswith('.php'):continue
        f=Path(td)/name.replace('/','_')
        f.write_bytes(z.read(name))
        result=run(['php','-l',str(f)],capture_output=True,text=True)
        assert result.returncode==0,(name,result.stdout,result.stderr)
        count+=1
    assert count>=25,count
    print('RC42_ALL_ORIGINAL_PLUGIN_PHP_LINT_PASS',count)
print('RC42_ONE_EXISTING_ADMIN_EXPORT_ZERO_WRITES_ZERO_BANNER_CHANGES_PASS')
