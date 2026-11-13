#!/usr/bin/env python3
"""RC25 proof: full ZIP PHP lint + real updated method integration tests."""
import subprocess
import tempfile
from pathlib import Path
from zipfile import ZipFile

p=Path("protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ/PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip")
with ZipFile(p) as z:
    assert z.testzip() is None and len(z.namelist())==36
    trait=z.read("affiliate-portal-router/includes/trait-ppar-idealo.php").decode("utf8")
    assert trait.count("last_catalog_signature")==2
    assert trait.count("if ($catalog_changed)")==1
    assert trait.count("&& !$catalog_changed)")==1
    assert "last_feed_reject_stats" in trait
    a=trait.index("    private function idealo_refresh_remote_feed(")
    b=trait.index("\n    public function idealo_sync_dispatch(",a)
    method=trait[a:b]
    assert "idealo_download_feed_to_temp($download_settings)" in method
    assert method.index("$catalog_changed")<method.index("Feed und Produktzuordnung unverändert")
    assert method.index("$result=$this->idealo_import_feed_file")<method.index("$s['last_catalog_signature']=$catalog_signature")
    with tempfile.TemporaryDirectory() as td:
        php_files=[x for x in z.namelist() if x.endswith(".php")]
        assert len(php_files)==25, len(php_files)
        for name in php_files:
            dest=Path(td)/name
            dest.parent.mkdir(parents=True,exist_ok=True)
            dest.write_bytes(z.read(name))
            r=subprocess.run(["php","-l",str(dest)],capture_output=True,text=True)
            assert r.returncode==0,(name,r.stdout,r.stderr)
        php='''<?php
class WP_Error { public function get_error_message(){return "simulated";} }
function is_wp_error($v){return $v instanceof WP_Error;}
function absint($v){return abs((int)$v);}
function wp_json_encode($x){return json_encode($x);}
function sanitize_text_field($x){return trim((string)$x);}
function update_option($k,$s,$autoload=false){$GLOBALS["settings"]=$s;}
function check($v,$msg){if(!$v){fwrite(STDERR,"FAIL: ".$msg."\\n");exit(1);}echo "PASS: ".$msg."\\n";}
class TestIdealo {
    const OPTION_NETWORK_IDEALO="existing_provider_option";
    public function run(){return $this->idealo_refresh_remote_feed(true);}
    private function idealo_settings(){return $GLOBALS["settings"];}
    private function idealo_match_index(){return array("concepts"=>array(
        "a"=>array("id"=>"a","title"=>$GLOBALS["mapping_version"],"target_pages"=>array("one"))
    ));}
    private function idealo_find_feed_metadata($s){return array(
        "last_file_hash"=>"SAME-PARTNER-FEED","last_updated_at"=>0,
        "number_of_products"=>2901, "advertiser_name"=>"idealo"
    );}
    private function idealo_download_feed_to_temp($s){
        $GLOBALS["download_count"]++;
        $GLOBALS["download_settings"]=$s;
        if(!empty($GLOBALS["simulate_error"]))return new WP_Error();
        return array("status"=>"downloaded","path"=>"/tmp/unused-rc25-mock",
           "etag"=>"NEW-ETAG","last_modified"=>"");
    }
    private function idealo_import_feed_file($p,$label){$GLOBALS["import_count"]++;return array("status"=>"success");}
''' + method + '''
}
$GLOBALS["settings"]=array("last_remote_file_hash"=>"SAME-PARTNER-FEED",
    "last_import_at"=>1000,"feed_etag"=>"OLD-ETAG",
    "feed_last_modified"=>"OLD-MODIFIED","last_import_count"=>1799);
$GLOBALS["mapping_version"]="RC25-mapping-A";
$GLOBALS["download_count"]=0;
$GLOBALS["import_count"]=0;
$w=new TestIdealo();
$r=$w->run();
check(!is_wp_error($r) && $GLOBALS["import_count"]===1,
 "Old feed with missing mapping signature is re-matched once");
check(($GLOBALS["download_settings"]["feed_etag"]??"?")===""
   && ($GLOBALS["download_settings"]["feed_last_modified"]??"?")==="",
 "Old ETag and Last-Modified do not block mandatory reimport");
$first=$GLOBALS["settings"]["last_catalog_signature"]??"";
check(strlen($first)===64,"Mapping signature stored only after import success");
$r=$w->run();
check(($r["status"]??"")==="unchanged" && $GLOBALS["download_count"]===1,
 "Unchanged feed AND mapping do not repeat download");
$GLOBALS["mapping_version"]="RC25-mapping-B";
$r=$w->run();
check($GLOBALS["import_count"]===2 && $GLOBALS["download_count"]===2
  && $GLOBALS["settings"]["last_catalog_signature"]!==$first,
 "Another mapping change triggers exactly one new matching pass");
$good=$GLOBALS["settings"]["last_catalog_signature"];
$GLOBALS["mapping_version"]="RC25-mapping-C";
$GLOBALS["simulate_error"]=true;
$r=$w->run();
check(is_wp_error($r) && $GLOBALS["settings"]["last_catalog_signature"]===$good,
 "Failed download keeps last successful state and retries later");
echo "HAB_RC25_MAPPING_REFRESH_BEHAVIOUR_PASS\\n";
'''
        h=Path(td)/"harness.php"
        h.write_text(php)
        run=subprocess.run(["php",str(h)],capture_output=True,text=True)
        print(run.stdout)
        assert run.returncode==0,run.stderr
        print("HAB_RC25_ALL_PHP_LINT_PASS",len(php_files))
print("HAB_RC25_TEST_PASS")
