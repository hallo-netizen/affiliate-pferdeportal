#!/usr/bin/env python3
"""Functional tests against the actual new PHP helper methods extracted from the ZIP.
Isolated WordPress mocks: no I/O or paid provider calls.
"""
from pathlib import Path
from zipfile import ZipFile
import subprocess,re,json,tempfile
p=Path('protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ/PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip')
with ZipFile(p) as z:
    assert z.testzip() is None and len(z.namelist())==36
    source=z.read('affiliate-portal-router/affiliate-portal-router.php').decode()
    amazon=z.read('affiliate-portal-router/includes/trait-ppar-hb-amazon.php').decode()
    assert 'Version: 0.1.16-rc19' in source
    assert 'core:world:insurance' not in amazon
    assert 'Feuerfeste Dokumententasche Versicherungsunterlagen' not in amazon
    assert 'function hb_insurance_campaign_allowed' in source
    assert 'if ($hb_insurance_scope === \'insurance\') { return \'\'; }' in source
    assert source.count('hb_insurance_original_wide_allowed(')>=2
    assert 'hb_insurance_campaign_allowed($campaign,$context' in source
def extract(name):
    m=re.search(r'private function '+name+r'\s*\(',source)
    assert m,name
    start=m.start()
    brace=source.index('{',m.end())
    depth=0
    for i in range(brace,len(source)):
        if source[i]=='{':depth+=1
        elif source[i]=='}':
            depth-=1
            if depth==0:
                return source[start:i+1].replace('private function','public function',1)
    raise AssertionError(name)
methods="\n\n".join(extract(x) for x in [
    'hb_insurance_scope','hb_insurance_campaign_allowed','hb_insurance_original_wide_allowed'
])
# Synthetic complete intended hierarchy: 1 R1, 5 R2, 46 R3, 323 WordPress categories.
nodes={}
root='core:world:insurance'
nodes[root]={'id':root,'type':'page','wp_id':1000,'parent':''}
for i in range(5):
    key=f'ins:r2:{i}'
    nodes[key]={'id':key,'type':'page','wp_id':1001+i,'parent':root}
for i in range(46):
    key=f'ins:r3:{i}'
    nodes[key]={'id':key,'type':'page','wp_id':2000+i,'parent':f'ins:r2:{i%5}'}
for i in range(323):
    key=f'ins:term:{i}'
    nodes[key]={'id':key,'type':'category','wp_id':3000+i,'parent':f'ins:r3:{i%46}'}
other='core:world:einbruch-und-diebstahl'
nodes[other]={'id':other,'type':'page','wp_id':7000,'parent':''}
nodes['outside:term']={'id':'outside:term','type':'category','wp_id':7001,'parent':other}
fixture=json.dumps(nodes,ensure_ascii=False,separators=(',',':'))
harness=r'''<?php
function absint($v){return max(0,(int)$v);}
function sanitize_key($v){return strtolower(preg_replace('/[^a-z0-9_\-]/','',(string)$v));}
function remove_accents($v){return strtr((string)$v,array('ä'=>'a','ö'=>'o','ü'=>'u','Ä'=>'A','Ö'=>'O','Ü'=>'U','ß'=>'ss'));}
class PPAR_HB_Integration {
  public static $nodes=array();
  public static function verified_nodes(){return self::$nodes;}
}
class TestInsurance {
  METHODS_HERE
  public function overview_wide_banner_slot($s){return in_array($s,array('hub_after_cards','product_after_category_tiles','post_inline_banner'),true);}
  public function article_banner_dimensions($banner){return array((int)($banner['width']??0),(int)($banner['height']??0),'intrinsic');}
}
function expect($value,$msg){if(!$value){fwrite(STDERR,"FAIL ".$msg."\n");exit(2);}}
PPAR_HB_Integration::$nodes=json_decode('JSON_HERE',true);
$a=new TestInsurance();$checks=0;
foreach(PPAR_HB_Integration::$nodes as $k=>$n){
  if($k==='outside:term'||$k==='core:world:einbruch-und-diebstahl')continue;
  $type=$n['type']==='category'?'category_archive':'page';
  $ctx=array('post_type'=>$type,'post_id'=>$type==='page'?$n['wp_id']:0,'term_ids'=>$type==='category_archive'?array($n['wp_id']):array(),'hb_verified_node_id'=>$type==='page'?$k:'');
  expect($a->hb_insurance_scope($ctx)==='insurance','scope '.$k);$checks++;
  if($type==='category_archive'){
    $ctx['post_type']='post';$ctx['post_id']=88000+$n['wp_id'];
    expect($a->hb_insurance_scope($ctx)==='insurance','post scope '.$k);$checks++;
  }
}
$outside=array('post_type'=>'category_archive','term_ids'=>array(7001));
expect($a->hb_insurance_scope($outside)==='other','outside scope');$checks++;
$mixed=array('post_type'=>'post','post_id'=>88000,'term_ids'=>array(3000,7001));
expect($a->hb_insurance_scope($mixed)==='mixed','mixed scope');$checks++;
$insurance=array('post_type'=>'page','post_id'=>2000,'hb_verified_node_id'=>'ins:r3:0','slugs'=>array('hausratversicherung'));
$yes=array('network'=>'direct','creative_type'=>'banner','name'=>'Tarifcheck Hausratversicherung','page_id'=>2000,'assignment_mode'=>'page_tree');
expect($a->hb_insurance_campaign_allowed($yes,$insurance,'hub_after_cards'),'valid house insured');$checks++;
foreach(array('amazon','ebay','idealo','manual') as $network){
 $c=$yes;$c['network']=$network;
 expect(!$a->hb_insurance_campaign_allowed($c,$insurance,'hub_after_cards'),'blocked '.$network);$checks++;
}
$credit=$yes;$credit['name']='Tarifcheck Girokonto Kreditversicherung';
expect(!$a->hb_insurance_campaign_allowed($credit,$insurance,'hub_after_cards'),'finance blocked');$checks++;
$product=$yes;$product['creative_type']='product';
expect(!$a->hb_insurance_campaign_allowed($product,$insurance,'hub_after_cards'),'product blocked');$checks++;
$wrong=$yes;$wrong['page_id']=2050;
expect(!$a->hb_insurance_campaign_allowed($wrong,$insurance,'hub_after_cards'),'wrong R3');$checks++;
$fallback=$yes;$fallback['assignment_mode']='fallback';
expect(!$a->hb_insurance_campaign_allowed($fallback,$insurance,'hub_after_cards'),'generic fallback blocked');$checks++;
expect(!$a->hb_insurance_campaign_allowed($yes,$mixed,'hub_after_cards'),'mixed blocked');$checks++;
expect($a->hb_insurance_campaign_allowed($yes,$outside,'hub_after_cards'),'outside unchanged');$checks++;
$wide=array('creative_type'=>'banner','mode'=>'image_link','image_url'=>'https://approved.example/banner.png','width'=>728,'height'=>90);
echo 'WIDE_DIAG '.json_encode(array('scope'=>$a->hb_insurance_scope($insurance),'wide'=>$a->hb_insurance_original_wide_allowed($wide,$insurance,'hub_after_cards'),'image'=>$wide['image_url'],'mode'=>$wide['mode'],'w'=>$wide['width'],'h'=>$wide['height']))."\n";
expect($a->hb_insurance_original_wide_allowed($wide,$insurance,'hub_after_cards'),'728x90 accepted in insurance');$checks++;
expect(!$a->hb_insurance_original_wide_allowed($wide,$outside,'hub_after_cards'),'other world unchanged');$checks++;
$wide['width']=468;$wide['height']=60;
expect($a->hb_insurance_original_wide_allowed($wide,$insurance,'hub_after_cards'),'468x60 accepted');$checks++;
$wide['width']=300;$wide['height']=250;
expect(!$a->hb_insurance_original_wide_allowed($wide,$insurance,'hub_after_cards'),'300x250 not wide');$checks++;
echo "HAB_INSURANCE_RC19_TESTS_PASS ".$checks." / 1 R1 + 5 R2 + 46 R3 + 323 leaves + article + countercases\n";
'''.replace('METHODS_HERE',methods).replace('JSON_HERE',fixture.replace("\\","\\\\").replace("'","\\'"))
with tempfile.NamedTemporaryFile('w',suffix='.php',encoding='utf8') as tmp:
    tmp.write(harness);tmp.flush()
    lint=subprocess.run(['php','-l',tmp.name],capture_output=True,text=True)
    assert lint.returncode==0,lint.stdout+lint.stderr
    p=subprocess.run(['php',tmp.name],capture_output=True,text=True)
    assert p.returncode==0,p.stdout+p.stderr
    print(p.stdout.strip())
