#!/usr/bin/env python3
"""RC22 PHP/real-design regression, true WordPress-stylesheet version test.
Require 3/2/1 live public browser display before releasing the new complete ZIP.
"""
from pathlib import Path
from zipfile import ZipFile
import subprocess,tempfile,re,hashlib
root=Path("protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ")
p=root/"PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip"
with ZipFile(p) as z:
 assert z.testzip() is None and len(z.namelist())==36
 phpnames=[n for n in z.namelist() if n.endswith(".php")]
 assert len(phpnames)==25
 main=z.read("affiliate-portal-router/affiliate-portal-router.php").decode()
 readme=z.read("affiliate-portal-router/readme.txt").decode()
 css=z.read("affiliate-portal-router/assets/frontend.css").decode()
 assert main.count("Version: 0.1.19-rc22")==1
 assert "Stable tag: 0.1.19-rc22" in readme
 assert "'-hb-rc16-20261108'" not in main
 assert "'-hb-plugin-' . (string) (get_file_data(__FILE__, array('Version' => 'Version'), 'plugin')['Version'] ?? '')" in main
 assert "grid-template-columns:repeat(3,minmax(0,1fr))" in css
 with tempfile.TemporaryDirectory() as tmp:
    for i,name in enumerate(phpnames):
        f=Path(tmp)/str(i);f.write_bytes(z.read(name))
        r=subprocess.run(["php","-l",str(f)],capture_output=True,text=True)
        assert r.returncode==0,(name,r.stdout,r.stderr)
    # Exercise the exact native WordPress header-reading expression (with a faithful mock of get_file_data).
    body=r"""<?php
/** Version: 0.1.19-rc22 */
function get_file_data($file, $headers, $context='') {
  $body=file_get_contents($file);preg_match('/Version:\s*(\S+)/',$body,$m);
  return array('Version'=>$m[1] ?? '');
}
class Tested {
  const VERSION='6.72.211';
  public function asset_version() {
    return self::VERSION . '-hb-plugin-' . (string) (get_file_data(__FILE__, array('Version' => 'Version'), 'plugin')['Version'] ?? '');
  }
}
$v=(new Tested())->asset_version();
if($v!=='6.72.211-hb-plugin-0.1.19-rc22'){echo "FAIL ".$v;exit(1);}
echo 'PASS WP ASSET VERSION: '.$v.PHP_EOL;
"""
    fixture=Path(tmp)/"fixture.php";fixture.write_text(body)
    t=subprocess.run(["php",str(fixture)],capture_output=True,text=True)
    assert t.returncode==0,t.stdout+t.stderr
    print(t.stdout.strip())
    # RC21 11 real bridge/Design integration tests, runtime with upgraded main header.
    original=(root/"AFFILIATE/IMPLEMENTIERUNG_RC21_CATEGORY_CARDS/qa_rc21.py").read_text()
    updated=original.replace("0.1.18-rc21","0.1.19-rc22")
    assert updated!=original
    qa=Path(tmp)/"actual_original_design_and_affiliate_bridge_qa.py";qa.write_text(updated)
    q=subprocess.run(["python3",str(qa)],capture_output=True,text=True)
    assert q.returncode==0,q.stdout+q.stderr
    print(q.stdout.strip())
 print("RC22_PHP_LINT_PASS",len(phpnames))
 print("RC22_CSS_CACHE_QA_PASS")
 print("RC22_SHA256",hashlib.sha256(p.read_bytes()).hexdigest())
