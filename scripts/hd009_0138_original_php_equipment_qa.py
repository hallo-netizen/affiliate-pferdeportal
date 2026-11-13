#!/usr/bin/env python3
"""Create executable QA from exact HD009 0.1.38 PHP methods + real HD007 records."""
from pathlib import Path
from zipfile import ZipFile
import json,re,sys

source=Path(sys.argv[1]);dest=Path(sys.argv[2])
with ZipFile(source) as z:
    trait=z.read('affiliate-portal-router/includes/trait-ppar-idealo.php').decode('utf8')
    main=z.read('affiliate-portal-router/hobby-depot-affiliate-router.php').decode('utf8')
def method(src,name):
    m=re.search(r'^    (?:private|public|protected) function '+re.escape(name)+r'\(',src,re.M)
    assert m, "Missing exact original "+name
    e=re.search(r'^    (?:private|public|protected) function ',src[m.end():],re.M)
    return src[m.start():m.end()+e.start()] if e else src[m.start():]

functions='\n'.join(method(trait,n) for n in [
    'idealo_match_normalize',
    'idealo_match_stem',
    'idealo_match_tokens',
    'idealo_match_primary_tokens',
    'idealo_match_distinct_tokens',
    'idealo_match_specific_equipment_stem',
    'idealo_match_index',
    'idealo_text_has_root',
    'idealo_match_blocked',
    'idealo_match_context_score',
    'idealo_match_feed_row_to_concept'
])
functions+='\n'+method(main,'hd_idealo_category_title_relevant')

# Use the real, versioned HD007 registry as sole equipment data source.
reg=Path(sys.argv[3])
with ZipFile(reg) as z:
    data=json.loads(z.read('hd-hobbyregister-core/data/hobby-register.json'))
records=data['records']
values=list(records.values()) if isinstance(records,dict) else records
names=['Airbrush','Airbrush-Modellbau','Buchbinden','Münzen','3D-Druck']
examples={str(r.get('canonical_name') or ''):r for r in values if isinstance(r,dict) and (r.get('canonical_name') in names)}
assert 'Airbrush' in examples and examples['Airbrush']['result_profile']['what_do_you_need'].startswith('Airbrushpistole')
assert 'Airbrush-Modellbau' in examples and 'Münzen' in examples
serialized=json.dumps(examples,ensure_ascii=False)

php=r'''<?php
error_reporting(E_ALL);ini_set('display_errors','1');
class WP_Error {
  private $c;
  function __construct($c,$m){$this->c=$c;}
  function get_error_code(){return $this->c;}
}
function is_wp_error($x){return $x instanceof WP_Error;}
function remove_accents($x){return strtr((string)$x,array('ü'=>'u','ö'=>'o','ä'=>'a','ß'=>'ss'));}
function wp_strip_all_tags($x){return strip_tags((string)$x);}
function sanitize_key($x){return preg_replace('/[^a-z0-9_\-]/','',strtolower((string)$x));}
function sanitize_title($x){return strtolower(preg_replace('/[^a-z0-9\-]/','',(string)$x));}
$GLOBALS['real_hobby_records']=json_decode('__REAL_HD007_JSON__',true,512,JSON_THROW_ON_ERROR);
function hd_hobbyregister_get_by_name($name){return $GLOBALS['real_hobby_records'][$name]??null;}

class RealHD009MatcherQA {
  private $catalog;
  function __construct($catalog){$this->catalog=$catalog;}
  private function idealo_portal_supply_catalog(){return $this->catalog;}
__ORIGINAL_METHODS__
  function match($row){return $this->idealo_match_feed_row_to_concept($row);}
  function equipped($name){return $this->idealo_match_specific_equipment_stem($name);}
  function relevant($title,$name){return $this->hd_idealo_category_title_relevant($title,array('primary_name'=>$name,'primary_slug'=>strtolower($name)));}
}
function ck($ok,$label){static $i=0;$i++;if(!$ok){fwrite(STDERR,"FAIL $i: $label\n");exit(1);}echo "PASS $i: $label\n";}
$targets=array();
foreach(array('Airbrush','Airbrush-Modellbau','Buchbinden','Münzen','3D-Druck') as $key){
  $id='concept-'.sanitize_key(str_replace(' ','-',$key));
  $targets[$id]=array('id'=>$id,'title'=>$key,'target_pages'=>array(array('hub'=>'Gestalten','main_hub'=>'Gestalten')));
}
$catalog=array('_idealo_required_concepts'=>$targets,'hard_negative_markers'=>array());
$q=new RealHD009MatcherQA($catalog);
ck($q->equipped('Airbrush')!=='','Actual HD007 Airbrush first equipment is a safe compound');
ck($q->equipped('Buchbinden')==='','Generic Papier excluded even if it occurs in feed');
ck($q->equipped('Münzen')==='','Generic sichere Aufbewahrung excluded');
ck($q->equipped('Airbrush-Modellbau')==='','Unrelated first noun Modell excluded');
ck($q->equipped('3D-Druck')==='','No unvalidated multiword-hobby equipment matching');
function row($name){return array('product_title'=>$name,'main_category'=>'Hobby Technik','sub_category'=>'Airbrush Zubehör');}
$x=$q->match(row('Airbrushpistole 0,3 mm Profi'));
ck($x['status']==='matched' && $x['concept']['title']==='Airbrush','Real source matcher recognizes actual HD007 equipment term');
ck($q->relevant('Airbrushpistole 0,3 mm Profi','Airbrush'),'Original unchanged final public output gate also accepts correct Airbrush compound');
$x=$q->match(row('Kari Traa Damen Malene Cape thyme'));
ck($x['status']!=='matched','Malene clothing not mapped');
$x=$q->match(row('Bogner Schurwollpullover Malene'));
ck($x['status']!=='matched','Malene pullover not mapped');
$x=$q->match(row('Gründl Cotton Quick Batik'));
ck($x['status']!=='matched','Batik yarn not mapped');
$x=$q->match(row('Kompressor 50 Liter'));
ck($x['status']!=='matched','Generic compressor not linked to Airbrush alone');
$x=$q->match(row('Farben 1 Liter'));
ck($x['status']!=='matched','Generic colors not linked to Airbrush alone');
$x=$q->match(row('Airbrush Anfänger Set'));
ck($x['status']==='matched' && $x['concept']['title']==='Airbrush','Previously matched exact hobby title remains matched');
$x=$q->match(row('Buchbinden Zubehör Werkzeug'));
ck($x['status']==='matched' && $x['concept']['title']==='Buchbinden','Existing simple hobby matcher remains functional');
ck(!$q->relevant('Kari Traa Malene Cape','Airbrush'),'Original final render gate blocks unrelated fashion');
echo "REAL_HD007_EQUIPMENT_ORIGINAL_MATCHER_TESTS_PASS\n";
'''.replace('__ORIGINAL_METHODS__',functions)
# JSON is escaped for a PHP single quote literal.
encoded=serialized.replace('\\','\\\\').replace("'","\\'").replace('\n',' ')
php=php.replace('__REAL_HD007_JSON__',encoded)
dest.parent.mkdir(parents=True,exist_ok=True)
dest.write_text(php)
print('ACTUAL_ORIGINAL_METHOD_COUNT',12,'REAL_HD007_NAMES',list(examples.keys()))
print('RUNTIME_PHP_SIZE',len(php))
