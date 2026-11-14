#!/usr/bin/env python3
"""Execute one original matcher decision against true HD007 gear records."""
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
    'idealo_match_specific_equipment_tokens',
    'idealo_match_related_equipment_stems',
    'idealo_match_index',
    'idealo_text_has_root',
    'idealo_match_blocked',
    'idealo_match_context_score',
    'idealo_match_feed_row_to_concept'
])

# Use the real, versioned HD007 registry as sole equipment data source.
reg=Path(sys.argv[3])
with ZipFile(reg) as z:
    data=json.loads(z.read('hd-hobbyregister-core/data/hobby-register.json'))
records=data['records']
values=list(records.values()) if isinstance(records,dict) else records
names=['Airbrush','Airbrush-Modellbau','Buchbinden','Münzen','3D-Druck','Aeroponik','Häkeln','Drechseln','Robotik','CB-Funk','RC-Offroad']
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
  function equipped($name){return $this->idealo_match_specific_equipment_tokens($name);}
}
function ck($ok,$label){static $i=0;$i++;if(!$ok){fwrite(STDERR,"FAIL $i: $label\n");exit(1);}echo "PASS $i: $label\n";}
$targets=array();
foreach(array('Airbrush','Airbrush-Modellbau','Buchbinden','Münzen','3D-Druck','Aeroponik','Häkeln','Drechseln','Robotik','CB-Funk','RC-Offroad') as $key){
  $id='concept-'.sanitize_key(str_replace(' ','-',$key));
  $targets[$id]=array('id'=>$id,'title'=>$key,'target_pages'=>array(array('hub'=>'Gestalten','main_hub'=>'Gestalten')));
}
$catalog=array('_idealo_required_concepts'=>$targets,'hard_negative_markers'=>array());
$q=new RealHD009MatcherQA($catalog);
ck(count($q->equipped('Airbrush'))===1,'Actual HD007 Airbrush first equipment is a safe compound');
ck($q->equipped('Buchbinden')===array(),'Generic Papier excluded even if it occurs in feed');
ck($q->equipped('Münzen')===array(),'Generic sichere Aufbewahrung excluded');
ck($q->equipped('Airbrush-Modellbau')===array(),'Unrelated first noun Modell excluded');
ck(count($q->equipped('3D-Druck'))===2,'Real 3D-Drucker from HD007 allows exact two-token matching');
ck(count($q->equipped('Aeroponik'))===2,'Aeroponik-System named hyphenated compound');
ck(count($q->equipped('Häkeln'))===1,'Häkelnadel is a real hobby compound');
ck(count($q->equipped('Drechseln'))===1,'Drechselbank from hobby form');
ck($q->equipped('Robotik')===array(),'Mixed robot kit or individual parts is ambiguous and excluded');
ck(count($q->equipped('CB-Funk'))===2,'CB-Funkgerät requires both CB and Funkgerät: not generic Funkgerät');
ck(count($q->equipped('RC-Offroad'))===2,'RC-Offroadfahrzeug requires both RC and Offroadfahrzeug');

function row($name){return array('product_title'=>$name,'main_category'=>'Hobby Technik','sub_category'=>'Airbrush Zubehör');}
$x=$q->match(row('Airbrushpistole 0,3 mm Profi'));
ck($x['status']==='matched' && $x['concept']['title']==='Airbrush','Real source matcher recognizes actual HD007 equipment term');
$x=$q->match(row('Kari Traa Damen Malene Cape thyme'));
ck($x['status']!=='matched','Malene clothing not mapped');
$x=$q->match(row('Bogner Schurwollpullover Malene'));
ck($x['status']!=='matched','Malene pullover not mapped');
$x=$q->match(row('Gründl Cotton Quick Batik'));
ck($x['status']!=='matched','Batik yarn not mapped');
$x=$q->match(row('Kompressor 50 Liter'));
ck($x['status']==='matched' && $x['concept']['title']==='Airbrush','Airbrush category plus real HD007 Kompressor is related');
$x=$q->match(row('Farben 1 Liter'));
ck($x['status']==='matched' && $x['concept']['title']==='Airbrush','Airbrush category plus original HD007 Farben is related');
$x=$q->match(row('Airbrush Anfänger Set'));
ck($x['status']==='matched' && $x['concept']['title']==='Airbrush','Previously matched exact hobby title remains matched');
$x=$q->match(row('Buchbinden Zubehör Werkzeug'));
ck($x['status']==='matched' && $x['concept']['title']==='Buchbinden','Existing simple hobby matcher remains functional');

$x=$q->match(row('FDM 3D Drucker mit Zubehör'));
ck($x['status']==='matched' && $x['concept']['title']==='3D-Druck','3D Drucker from real HD007 maps to 3D-Druck');
$x=$q->match(row('Aeroponik-System für Pflanzen'));
ck($x['status']==='matched' && $x['concept']['title']==='Aeroponik','Aeroponik-System hyphenated exact equipment');
$x=$q->match(row('Häkelnadel 3 mm'));
ck($x['status']==='matched' && $x['concept']['title']==='Häkeln','Häkelnadel matches original reviewed hobby gear');
$x=$q->match(row('Drechselbank 600W'));
ck($x['status']==='matched' && $x['concept']['title']==='Drechseln','Drechselbank matches verified equipment term');

$x=$q->match(row('Funkgerät mit Akku'));
ck($x['status']!=='matched','Generic Funkgerät never assigned to CB-Funk');
$x=$q->match(row('CB Funkgerät mit Akku'));
ck($x['status']==='matched' && $x['concept']['title']==='CB-Funk','Literal CB qualifier and Funkgerät match their actual HD007 equipment');
$x=$q->match(row('Offroadfahrzeug Modellauto'));
ck($x['status']!=='matched','Generic Offroadfahrzeug never assigned to RC-Offroad');
$x=$q->match(row('RC Offroadfahrzeug 1:16'));
ck($x['status']==='matched' && $x['concept']['title']==='RC-Offroad','Exact source-backed RC Offroad vehicle');
$x=$q->match(row('Normaler 3D Farbdrucker ohne Druckausrüstung'));
ck($x['status']!=='matched','Do not infer 3D Drucker from different Farbdrucker token');

// A product category PLUS actual listed HD007 equipment is sufficient.
// Neither factor alone permits unrelated products.
$x=$q->match(array('product_title'=>'Kompressor 50 Liter','main_category'=>'Technik','sub_category'=>'Werkstattausrüstung'));
ck($x['status']!=='matched','Generic compressor WITHOUT Airbrush category rejected');
$x=$q->match(array('product_title'=>'Papier 120g','main_category'=>'Bürobedarf','sub_category'=>'Papier'));
ck($x['status']!=='matched','Generic paper WITHOUT Buchbinden category rejected');
$x=$q->match(array('product_title'=>'Papier 120g','main_category'=>'Buchbinden Zubehör','sub_category'=>'Bastelpapier'));
ck($x['status']==='matched' && $x['concept']['title']==='Buchbinden','Buchbinden category plus real HD007 Papier accepted');
$x=$q->match(array('product_title'=>'Filament PETG 1kg','main_category'=>'3D Druck Zubehör','sub_category'=>'Filament'));
ck($x['status']==='matched' && $x['concept']['title']==='3D-Druck','3D Druck category plus listed Filament accepted');
$x=$q->match(array('product_title'=>'Kari Traa Damen Malene Cape','main_category'=>'Airbrush Zubehör','sub_category'=>'Farben'));
ck($x['status']!=='matched','Fashion rejected even when a wrong category says Airbrush');
$x=$q->match(array('product_title'=>'Reinigungsmittel für Spritzpistolen','main_category'=>'Airbrush Zubehör','sub_category'=>'Reinigung'));
ck($x['status']==='matched' && $x['concept']['title']==='Airbrush','Topic-specific cleaning equipment accepted via HD007 list');
echo "HD009_0140_SINGLE_DECISION_ORIGINAL_MATCHER_TESTS_PASS\n";
'''.replace('__ORIGINAL_METHODS__',functions)
# JSON is escaped for a PHP single quote literal.
encoded=serialized.replace('\\','\\\\').replace("'","\\'").replace('\n',' ')
php=php.replace('__REAL_HD007_JSON__',encoded)
dest.parent.mkdir(parents=True,exist_ok=True)
dest.write_text(php)
print('ACTUAL_ORIGINAL_METHOD_COUNT',12,'REAL_HD007_NAMES',list(examples.keys()))
print('RUNTIME_PHP_SIZE',len(php))
