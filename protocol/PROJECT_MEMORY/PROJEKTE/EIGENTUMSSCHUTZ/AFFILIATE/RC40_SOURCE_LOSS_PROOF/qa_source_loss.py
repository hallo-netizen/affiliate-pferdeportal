#!/usr/bin/env python3
"""Forensic proof, not new plugin: exercise RC40's ORIGINAL PHP HTML-import
parser, full original normalization, and source-first reader in that order.
Demonstrate whether a banner title stored only on the <a> tag survives.
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
    c=z.read("affiliate-portal-router/includes/trait-ppar-creative-library.php").decode()
    assert "creative_library_read_original_banner_once" in c
    def extract(name):
        p=re.search(r"private\s+function\s+"+re.escape(name)+r"\s*\(",c)
        assert p,("Cannot find REAL method",name)
        start=c.index("{",p.end());depth=0
        for end in range(start,len(c)):
            if c[end]=="{":depth+=1
            if c[end]=="}":
                depth-=1
                if depth==0:return c[p.start():end+1].replace("private function","public function",1)
        raise AssertionError(name)
    methods="\n".join(extract(name) for name in (
        "creative_library_html_attr",
        "creative_library_aliases",
        "creative_library_normalize_key",
        "creative_library_detect_mapping",
        "creative_library_mapped_value",
        "creative_library_parse_html_codes",
        "creative_library_declared_dimensions",
        "creative_library_destination_from_tracking",
        "creative_library_normalize_type",
        "creative_library_normalize_status",
        "creative_library_read_original_banner_once",
        "creative_library_normalize_row",
    ))
    # This must be the exact unchanged source; no testing a rewritten importer.
    assert "sanitize_text_field((string) $value)" in methods
    assert "$this->creative_library_read_original_banner_once($normalized)" in methods
php=r'''<?php
error_reporting(E_ERROR|E_PARSE);
function sanitize_text_field($s){return trim(preg_replace('/\s+/u',' ',strip_tags((string)$s)));}
function sanitize_textarea_field($s){return sanitize_text_field($s);}
function sanitize_key($s){return strtolower(preg_replace('/[^a-z0-9_\-]/','',strtolower((string)$s)));}
function wp_strip_all_tags($s){return strip_tags((string)$s);}
function esc_url_raw($s){return (string)$s;}
function wp_http_validate_url($s){return str_starts_with((string)$s,'https://');}
function wp_json_encode($a,$flags=0){return json_encode($a,$flags);}
function wp_parse_url($u,$part=-1){return $part===-1?parse_url((string)$u):parse_url((string)$u,$part);}
function absint($v){return abs((int)$v);}
function remove_accents($v){return (string)$v;}
function is_wp_error($v){return $v instanceof WP_Error;}
class WP_Error{
  public function __construct($code,$message){$this->code=$code;$this->message=$message;}
  public string $code; public string $message;
}
function ok($v,$why){if(!$v){fwrite(STDERR,"FAIL: $why\n");exit(12);}echo "PASS $why\n";}
class RealPlugin{
  public function creative_library_resolve_tracking_destination_import($url){
    return array('url'=>$url,'source'=>'tracking_checked');
  }
  METHODS
}
$o=new RealPlugin;
function process_original($o,$html){
  $p=$o->creative_library_parse_html_codes($html);
  if(is_wp_error($p))throw new Exception($p->message);
  if(count($p['rows'])!==1)throw new Exception('Wrong parser row count');
  $context=array('provider'=>'direct','partner_external_id'=>'tarifcheck',
                 'partner_name'=>'Tarifcheck','source_kind'=>'banner');
  $row=$o->creative_library_normalize_row($p['rows'][0],$p['mapping'],$context);
  if(is_wp_error($row))throw new Exception($row->message);
  return $row;
}
$href='https://a.partner-versicherung.de/click.php?partner_id=DEMO&ad_id=111';
$img='https://a.partner-versicherung.de/assets/generic-300x250.png';
$source='<a href="'.$href.'" title="Hausratversicherung"><img src="'.$img.'" title="" alt="" width="300" height="250"></a>';
$parsed=$o->creative_library_parse_html_codes($source);
ok(str_contains($parsed['rows'][0]['html'],'title="Hausratversicherung"'),
  'Original HTML arrives complete in real parser');
$normalized=process_original($o,$source);
$payload=json_decode((string)$normalized['payload'],true);
ok($normalized['title']==='Tarifcheck Banner',
  'Importer creates meaningless Tarifcheck Banner placeholder');
ok(!str_contains((string)($payload['html']??''),'<a')
  && !str_contains((string)($payload['html']??''),'title='),
  'Original markup and anchor-title attribute are DESTROYED at source persistence');
ok(($payload['_source_read_version']??0)===1,
  'RC40 irrevocably marks this source as already read');
ok(trim((string)($payload['_source_evidence']['text']??''))==='',
  'First source read cannot recover insurance from discarded anchor title');
ok($normalized['tracking_url']===$href && $normalized['image_url']===$img,
  'The stored link and image URL survive: evidence gap is specific');
$rerun=$o->creative_library_read_original_banner_once($normalized);
ok($rerun['payload']===$normalized['payload'],
  'Later RC40 rebind skips read and cannot reconstruct deleted original attributes');

// Other metadata do survive when a field was individually parsed.
$explicit='<a href="'.$href.'"><img src="'.$img.'" title="Hausratversicherung" alt="" width="300" height="250"></a>';
$row2=process_original($o,$explicit);
$proof2=json_decode((string)$row2['payload'],true);
ok(str_contains((string)$proof2['_source_evidence']['text'],'Hausratversicherung'),
  'Original IMG title separately parsed before destruction survives');
$deep='<a href="'.$href.'&deep=hausratversicherung"><img src="'.$img.'" title="" alt="" width="300" height="250"></a>';
$row3=process_original($o,$deep);
$proof3=json_decode((string)$row3['payload'],true);
ok(str_contains((string)$proof3['_source_evidence']['destination'],'hausratversicherung'),
  'Original deep= insurance link survives');
echo "RC40_ACTUAL_PHP_FULL_IMPORT_SOURCE_LOSS_PROVEN\n";
'''
assert php.count("  METHODS")==1
php=php.replace("  METHODS",methods)
with TemporaryDirectory() as tmp:
    f=Path(tmp)/"real_import.php"
    f.write_text(php)
    lint=run(["php","-l",str(f)],capture_output=True,text=True)
    assert lint.returncode==0,lint.stderr
    v=run(["php",str(f)],capture_output=True,text=True)
    print(v.stdout)
    if v.returncode:print(v.stderr)
    assert v.returncode==0,(v.stdout,v.stderr)
    assert "RC40_ACTUAL_PHP_FULL_IMPORT_SOURCE_LOSS_PROVEN" in v.stdout
print("NO_NEW_PLUGIN_RELEASE_NO_LIVE_DATA_INVENTED")
