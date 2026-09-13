#!/usr/bin/env bash
set -euo pipefail
R=protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/GLOSSAR
bash "$R/build-0.2.9-rc1.sh"
rm -rf /tmp/uge029rc2
cp -a /tmp/uge029rc1 /tmp/uge029rc2
P=/tmp/uge029rc2/universal-glossary-engine
python3 - <<'PY'
from pathlib import Path
p=Path('/tmp/uge029rc2/universal-glossary-engine/universal-glossary-engine.php')
s=p.read_text()
assert s.count('Version: 0.2.9-rc1')==1
assert s.count("define('UGE_VERSION', '0.2.9-rc1');")==1
s=s.replace('Version: 0.2.9-rc1','Version: 0.2.9-rc2')
s=s.replace("define('UGE_VERSION', '0.2.9-rc1');","define('UGE_VERSION', '0.2.9-rc2');")
p.write_text(s)

p=Path('/tmp/uge029rc2/universal-glossary-engine/includes/class-uge-core.php')
s=p.read_text()
old="        if (is_admin() || wp_doing_ajax() || empty($_SERVER['REQUEST_URI'])) { return; }\n        $cfg = UGE_Config::get();\n"
new="        if (is_admin() || wp_doing_ajax() || empty($_SERVER['REQUEST_URI'])) { return; }\n        // Native authenticated draft preview must stay under WordPress control.\n        if (isset($_GET['preview']) || isset($_GET['preview_id']) || isset($_GET['preview_nonce'])) { return; }\n        $cfg = UGE_Config::get();\n"
# Only bind_explicit_request gets this bypass; redirect_legacy keeps its own guard.
pos=s.index('public static function bind_explicit_request')
sub=s[pos:]
assert sub.count(old)>=1
sub=sub.replace(old,new,1)
s=s[:pos]+sub
p.write_text(s)
PY

grep -q 'Version: 0.2.9-rc2' "$P/universal-glossary-engine.php"
grep -q "define('UGE_VERSION', '0.2.9-rc2');" "$P/universal-glossary-engine.php"
grep -q "isset(\$_GET\['preview'\])" "$P/includes/class-uge-core.php"
find "$P" -name '*.php' -print0 | xargs -0 -n1 php -l
python3 - <<'PY'
from pathlib import Path
import hashlib
A=Path('/tmp/uge029rc1/universal-glossary-engine');B=Path('/tmp/uge029rc2/universal-glossary-engine')
changed=[]
for rel in sorted({str(p.relative_to(A)) for p in A.rglob('*') if p.is_file()}|{str(p.relative_to(B)) for p in B.rglob('*') if p.is_file()}):
 a=A/rel;b=B/rel
 if hashlib.sha256(a.read_bytes()).digest()!=hashlib.sha256(b.read_bytes()).digest(): changed.append(rel)
assert changed==['includes/class-uge-core.php','universal-glossary-engine.php'],changed
print('UGE029RC2_DELTA_PASS',changed)
PY
echo UGE029RC2_BUILD_PASS
