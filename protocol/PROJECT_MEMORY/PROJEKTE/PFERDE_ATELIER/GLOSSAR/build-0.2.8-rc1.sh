#!/usr/bin/env bash
set -euo pipefail
R=protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/GLOSSAR

# Rebuild exact rejected 0.2.7 baseline from the already bound source chain.
SRC="$R/exact-0.2.6-test/01_build.sh"
sed -e 's/0\.2\.6/0.2.7/g' -e 's/UGE026/UGE027/g' -e 's/uge026/uge027/g' "$SRC" > /tmp/uge027-build.sh
chmod +x /tmp/uge027-build.sh
bash /tmp/uge027-build.sh

test -f /tmp/uge027/universal-glossary-engine/universal-glossary-engine.php
rm -rf /tmp/uge028rc1
cp -a /tmp/uge027 /tmp/uge028rc1
P=/tmp/uge028rc1/universal-glossary-engine

python3 - <<'PY'
from pathlib import Path

# Unique internal RC version.
p=Path('/tmp/uge028rc1/universal-glossary-engine/universal-glossary-engine.php')
s=p.read_text()
assert s.count('Version: 0.2.7') == 1
assert s.count("define('UGE_VERSION', '0.2.7');") == 1
s=s.replace('Version: 0.2.7','Version: 0.2.8-rc1')
s=s.replace("define('UGE_VERSION', '0.2.7');","define('UGE_VERSION', '0.2.8-rc1');")
p.write_text(s)

# Force rewrite rebuild from every previously handed schema-5 package.
p=Path('/tmp/uge028rc1/universal-glossary-engine/includes/class-uge-core.php')
s=p.read_text()
assert s.count("const REWRITE_SCHEMA_VERSION = '5';") == 1
s=s.replace("const REWRITE_SCHEMA_VERSION = '5';","const REWRITE_SCHEMA_VERSION = '6';")
p.write_text(s)

# Minimal visible frontend repairs.
p=Path('/tmp/uge028rc1/universal-glossary-engine/includes/class-uge-frontend.php')
s=p.read_text()
old='''<form class="uge-search-form" method="get" action="%s" data-uge-ajax="%s" data-uge-nonce="%s"><label class="screen-reader-text" for="uge-search-input">Glossar durchsuchen</label><input id="uge-search-input" type="search" name="glossar_s" value="%s" placeholder="Begriff suchen …" autocomplete="off"><button type="submit">Suchen</button><span class="uge-search-status" aria-live="polite"></span></form><div class="uge-search-suggestions" hidden></div>'''
new='''<form class="uge-search-form" method="get" action="%s" data-uge-ajax="%s" data-uge-nonce="%s"><label class="screen-reader-text" for="uge-search-input">Glossar durchsuchen</label><input id="uge-search-input" type="search" name="glossar_s" value="%s" placeholder="Begriff suchen …" autocomplete="off"><button type="submit">Suchen</button><span class="uge-search-status" aria-live="polite"></span><div class="uge-search-suggestions" hidden></div></form>'''
assert s.count(old) == 1, 'search DOM baseline mismatch'
s=s.replace(old,new)

# Hero uses the actual 1400x560 image ratio (5:2) at every width instead of a
# fixed 360px desktop/tablet height and a separate 16:9 mobile crop.
old_css='.uge-hero{position:relative;min-height:360px;overflow:hidden;border-radius:0;background:#31412d;color:#fff;margin-bottom:28px}'
new_css='.uge-hero{position:relative;aspect-ratio:5/2;min-height:0;overflow:hidden;border-radius:0;background:#31412d;color:#fff;margin-bottom:28px}'
assert s.count(old_css) == 1, 'hero base CSS mismatch'
s=s.replace(old_css,new_css)
old_mobile='.uge-hero{display:flex;min-height:0;flex-direction:column}.uge-hero-image{position:relative!important;order:1;width:100%!important;max-width:100%!important;height:auto!important;aspect-ratio:16/9!important;object-fit:cover!important;object-position:right center!important}'
new_mobile='.uge-hero{display:flex;min-height:0;aspect-ratio:auto;flex-direction:column}.uge-hero-image{position:relative!important;order:1;width:100%!important;max-width:100%!important;height:auto!important;aspect-ratio:5/2!important;object-fit:cover!important;object-position:right center!important}'
assert s.count(old_mobile) == 1, 'hero mobile CSS mismatch'
s=s.replace(old_mobile,new_mobile)
p.write_text(s)
PY

# Positive identity / migration guards.
grep -q 'Version: 0.2.8-rc1' "$P/universal-glossary-engine.php"
grep -q "define('UGE_VERSION', '0.2.8-rc1');" "$P/universal-glossary-engine.php"
grep -q "const REWRITE_SCHEMA_VERSION = '6';" "$P/includes/class-uge-core.php"
! grep -q 'Version: 0.2.7' "$P/universal-glossary-engine.php"

# Fix guards: suggestions must be inside form, hero cannot retain old fixed rules.
python3 - <<'PY'
from pathlib import Path
s=Path('/tmp/uge028rc1/universal-glossary-engine/includes/class-uge-frontend.php').read_text()
assert '</form><div class="uge-search-suggestions"' not in s
assert '<div class="uge-search-suggestions" hidden></div></form>' in s
assert '.uge-hero{position:relative;min-height:360px' not in s
assert 'aspect-ratio:16/9!important' not in s
assert '.uge-hero{position:relative;aspect-ratio:5/2;min-height:0;' in s
PY

find "$P" -name '*.php' -print0 | xargs -0 -n1 php -l

# RC may differ from exact 0.2.7 only in version, rewrite schema and frontend.
python3 - <<'PY'
from pathlib import Path
import hashlib
A=Path('/tmp/uge027/universal-glossary-engine')
B=Path('/tmp/uge028rc1/universal-glossary-engine')
allowed={'universal-glossary-engine.php','includes/class-uge-core.php','includes/class-uge-frontend.php'}
files=sorted({str(p.relative_to(A)) for p in A.rglob('*') if p.is_file()} | {str(p.relative_to(B)) for p in B.rglob('*') if p.is_file()})
changed=[]
for rel in files:
    a=A/rel; b=B/rel
    if not a.exists() or not b.exists() or hashlib.sha256(a.read_bytes()).digest()!=hashlib.sha256(b.read_bytes()).digest():
        changed.append(rel)
assert set(changed)==allowed, changed
print('UGE028RC1_MINIMAL_DELTA_PASS',changed)
PY

echo UGE028RC1_BUILD_PASS
