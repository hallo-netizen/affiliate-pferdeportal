#!/usr/bin/env bash
set -euo pipefail
R=protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/GLOSSAR
bash "$R/build-0.2.9-rc2.sh"
rm -rf /tmp/uge029
cp -a /tmp/uge029rc2 /tmp/uge029
P=/tmp/uge029/universal-glossary-engine
python3 - <<'PY'
from pathlib import Path
p=Path('/tmp/uge029/universal-glossary-engine/universal-glossary-engine.php')
s=p.read_text()
assert s.count('Version: 0.2.9-rc2')==1
assert s.count("define('UGE_VERSION', '0.2.9-rc2');")==1
s=s.replace('Version: 0.2.9-rc2','Version: 0.2.9')
s=s.replace("define('UGE_VERSION', '0.2.9-rc2');","define('UGE_VERSION', '0.2.9');")
p.write_text(s)
PY
grep -q 'Version: 0.2.9' "$P/universal-glossary-engine.php"
grep -q "define('UGE_VERSION', '0.2.9');" "$P/universal-glossary-engine.php"
grep -q "const REWRITE_SCHEMA_VERSION = '7';" "$P/includes/class-uge-core.php"
! grep -q '0.2.9-rc2' "$P/universal-glossary-engine.php"
find "$P" -name '*.php' -print0 | xargs -0 -n1 php -l
python3 - <<'PY'
from pathlib import Path
import hashlib
A=Path('/tmp/uge029rc2/universal-glossary-engine');B=Path('/tmp/uge029/universal-glossary-engine')
changed=[]
for rel in sorted({str(p.relative_to(A)) for p in A.rglob('*') if p.is_file()}|{str(p.relative_to(B)) for p in B.rglob('*') if p.is_file()}):
 a=A/rel;b=B/rel
 if hashlib.sha256(a.read_bytes()).digest()!=hashlib.sha256(b.read_bytes()).digest(): changed.append(rel)
assert changed==['universal-glossary-engine.php'],changed
print('UGE029_FINAL_VERSION_ONLY_DELTA_PASS',changed)
PY
echo UGE029_FINAL_BUILD_PASS
