#!/usr/bin/env bash
set -euo pipefail

ROOT=protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/GLOSSAR

# Build the already hard-tested 0.2.5 source first. 0.2.6 is derived only from
# that exact source; no second source truth is allowed.
bash "$ROOT/exact-0.2.5-test/01_build.sh"
rm -rf /tmp/uge025-tested /tmp/uge026
cp -a /tmp/u/universal-glossary-engine /tmp/uge025-tested
mkdir -p /tmp/uge026
cp -a /tmp/uge025-tested /tmp/uge026/universal-glossary-engine
P=/tmp/uge026/universal-glossary-engine

python3 - <<'PY'
from pathlib import Path
p=Path('/tmp/uge026/universal-glossary-engine/universal-glossary-engine.php')
s=p.read_text()
if s.count('Version: 0.2.5') != 1: raise SystemExit('plugin header 0.2.5 mismatch')
if s.count("define('UGE_VERSION', '0.2.5');") != 1: raise SystemExit('UGE_VERSION 0.2.5 mismatch')
s=s.replace('Version: 0.2.5','Version: 0.2.6')
s=s.replace("define('UGE_VERSION', '0.2.5');","define('UGE_VERSION', '0.2.6');")
p.write_text(s)

p=Path('/tmp/uge026/universal-glossary-engine/includes/class-uge-core.php')
s=p.read_text()
if s.count("const REWRITE_SCHEMA_VERSION = '4';") != 1: raise SystemExit('rewrite schema 4 mismatch')
s=s.replace("const REWRITE_SCHEMA_VERSION = '4';","const REWRITE_SCHEMA_VERSION = '5';")
p.write_text(s)
PY

# Candidate delta is intentionally tiny: plugin version + rewrite schema only.
grep -q 'Version: 0.2.6' "$P/universal-glossary-engine.php"
grep -q "define('UGE_VERSION', '0.2.6');" "$P/universal-glossary-engine.php"
grep -q "const REWRITE_SCHEMA_VERSION = '5';" "$P/includes/class-uge-core.php"
! grep -R "Version: 0.2.5" "$P/universal-glossary-engine.php"

# The three already proven frontend repairs must survive unchanged into 0.2.6.
F="$P/includes/class-uge-frontend.php"
grep -Fq 'body.uge-glossary-home #primary{margin-top:0!important}' "$F"
grep -Fq 'var(--pftk-breadcrumb-axis-width,900px)' "$F"
grep -Fq 'aspect-ratio:16/9!important' "$F"
! grep -Fq 'height:240px!important' "$F"

find "$P" -name '*.php' -print0 | xargs -0 -n1 php -l

# Hard delta guard: no file except main plugin and core may differ from tested 0.2.5.
python3 - <<'PY'
from pathlib import Path
import hashlib
A=Path('/tmp/uge025-tested'); B=Path('/tmp/uge026/universal-glossary-engine')
allowed={'universal-glossary-engine.php','includes/class-uge-core.php'}
files=sorted({str(p.relative_to(A)) for p in A.rglob('*') if p.is_file()} | {str(p.relative_to(B)) for p in B.rglob('*') if p.is_file()})
changed=[]
for rel in files:
    a=A/rel; b=B/rel
    if not a.exists() or not b.exists(): changed.append(rel); continue
    if hashlib.sha256(a.read_bytes()).digest()!=hashlib.sha256(b.read_bytes()).digest(): changed.append(rel)
assert set(changed)==allowed, changed
print('UGE026_DELTA_GUARD_PASS', changed)
PY

echo UGE026_BUILD_LINT_DELTA_PASS
