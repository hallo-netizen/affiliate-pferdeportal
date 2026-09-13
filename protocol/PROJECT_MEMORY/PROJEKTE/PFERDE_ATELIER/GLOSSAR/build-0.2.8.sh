#!/usr/bin/env bash
set -euo pipefail
R=protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/GLOSSAR
bash "$R/build-0.2.8-rc1.sh"
rm -rf /tmp/uge028
mkdir -p /tmp/uge028
cp -a /tmp/uge028rc1/universal-glossary-engine /tmp/uge028/universal-glossary-engine
P=/tmp/uge028/universal-glossary-engine
python3 - <<'PY'
from pathlib import Path
p=Path('/tmp/uge028/universal-glossary-engine/universal-glossary-engine.php')
s=p.read_text()
assert s.count('Version: 0.2.8-rc1')==1
assert s.count("define('UGE_VERSION', '0.2.8-rc1');")==1
s=s.replace('Version: 0.2.8-rc1','Version: 0.2.8')
s=s.replace("define('UGE_VERSION', '0.2.8-rc1');","define('UGE_VERSION', '0.2.8');")
p.write_text(s)
PY
grep -q 'Version: 0.2.8' "$P/universal-glossary-engine.php"
grep -q "define('UGE_VERSION', '0.2.8');" "$P/universal-glossary-engine.php"
grep -q "const REWRITE_SCHEMA_VERSION = '6';" "$P/includes/class-uge-core.php"
! grep -q '0.2.8-rc1' "$P/universal-glossary-engine.php"
find "$P" -name '*.php' -print0 | xargs -0 -n1 php -l
python3 - <<'PY'
from pathlib import Path
import hashlib
A=Path('/tmp/uge028rc1/universal-glossary-engine')
B=Path('/tmp/uge028/universal-glossary-engine')
files=sorted({str(p.relative_to(A)) for p in A.rglob('*') if p.is_file()}|{str(p.relative_to(B)) for p in B.rglob('*') if p.is_file()})
changed=[]
for rel in files:
 a=A/rel;b=B/rel
 if not a.exists() or not b.exists() or hashlib.sha256(a.read_bytes()).digest()!=hashlib.sha256(b.read_bytes()).digest(): changed.append(rel)
assert changed==['universal-glossary-engine.php'],changed
print('UGE028_FINAL_ONLY_VERSION_DELTA_PASS',changed)
PY
echo UGE028_FINAL_BUILD_PASS
