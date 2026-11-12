#!/usr/bin/env python3
"""Execute actual Hab idealo settings PHP with simulated WordPress options.
No connection, secret, page, product, DB or provider mutation.
"""
from zipfile import ZipFile
from pathlib import Path
from tempfile import TemporaryDirectory
from subprocess import run
import re
root=Path("protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ/PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE")
with ZipFile(root/"CURRENT.zip") as z:
 assert z.testzip() is None and len(z.namelist())==36
 adapter=z.read("affiliate-portal-router/includes/trait-ppar-idealo.php").decode("utf8")
 boot=z.read("affiliate-portal-router/affiliate-portal-router.php").decode("utf8")
 assert "Version: 0.1.17-rc20" in boot
 assert "=== '568313' ||" not in adapter
 assert "=== '568313')" in adapter
 assert "Feed 2901 is allowed with Hab's own adspace" in adapter
 # PHP lint all 25 files, not only edited file
 with TemporaryDirectory() as d:
  for name in z.namelist():
   if name.endswith(".php"):
    target=Path(d)/Path(name).name; target.write_bytes(z.read(name))
    pr=run(["php","-l",str(target)],capture_output=True,text=True)
    assert pr.returncode==0,(name,pr.stdout,pr.stderr)
 def extract(name):
  start=re.search(r"(?:private|public) function "+name+r"\s*\(",adapter)
  assert start,name
  brace=adapter.index("{",start.end())
  depth=0
  for i in range(brace,len(adapter)):
   if adapter[i]=="{":depth+=1
   elif adapter[i]=="}":
    depth-=1
    if depth==0:
     return adapter[start.start():i+1].replace("private function","public function",1)
  raise ValueError(name)
 needed=["idealo_settings_defaults","idealo_settings","idealo_sanitize_output_mode","idealo_sanitize_link_strategy"]
 functions="\n".join(extract(x) for x in needed)
 code="""<?php
 function get_option($key,$fallback){return $GLOBALS['fixture_options'];}
 function sanitize_key($v){return preg_replace('/[^a-z0-9_\\-]/','',strtolower((string)$v));}
 class TestedHabIdealo {
   const OPTION_NETWORK_IDEALO = 'example';
   FUNCTIONS
 }
 function check_case($name,$adspace,$feed,$enabled,$wantEnabled) {
   $GLOBALS['fixture_options']=array('adspace_id'=>$adspace,'feed_id'=>$feed,'enabled'=>$enabled,'api_key'=>'dummy','auto_refresh'=>true);
   $o=(new TestedHabIdealo())->idealo_settings();
   if ((bool)$o['enabled'] !== $wantEnabled) {fwrite(STDERR,'FAILED '.$name.PHP_EOL);exit(3);}
   echo 'PASS '.$name.PHP_EOL;
 }
 check_case('Hab own adspace 568944 plus shared feed 2901', '568944', '2901', true, true);
 check_case('Hab own adspace 568944 plus other feed 2747', '568944', '2747', true, true);
 check_case('Foreign Pferde Atelier adspace 568313 plus feed 2901', '568313', '2901', true, false);
 check_case('Foreign Pferde Atelier adspace 568313 plus feed 2747', '568313', '2747', true, false);
 check_case('Disabled remains disabled', '568944', '2901', false, false);
 echo 'HAB IDEALO RC20: 5 FUNCTIONAL CASES PASS'.PHP_EOL;
 """.replace("FUNCTIONS",functions)
 with TemporaryDirectory() as td:
  f=Path(td)/"test.php"; f.write_text(code,encoding="utf8")
  lint=run(["php","-l",str(f)],capture_output=True,text=True)
  assert lint.returncode==0,lint.stdout+lint.stderr
  result=run(["php",str(f)],capture_output=True,text=True)
  assert result.returncode==0,result.stdout+result.stderr
  print(result.stdout)
