#!/usr/bin/env bash
set -euo pipefail
BASE=.github/v652/runner/run-v652-full-release-wrapper-v15.sh
[ "$(git hash-object "$BASE")" = "cd77f4b34e0baed67249f9ad2de3a767a6d5381a" ] || { echo 'BLOCKED: V6.52 v15 wrapper blob mismatch'; exit 1; }
[ "$(git hash-object .github/v652/runner/patch_v652_real_selfpump_seed_http.py)" = "992482c848b357e76765c16a2562ef2eca94462c" ] || { echo 'BLOCKED: V6.52 real HTTP selfpump patcher blob mismatch'; exit 1; }
TMP=/tmp/run-v652-full-release-wrapper-v16-generated.sh
python3 - "$BASE" "$TMP" <<'PY'
from pathlib import Path
import sys
s=Path(sys.argv[1]).read_text()
needle='bash -n "$TMP"\nchmod +x "$TMP"\n"$TMP"\n'
replacement=r'''bash -n "$TMP"
python3 - "$TMP" <<'PYV652V16'
from pathlib import Path
import sys
p=Path(sys.argv[1]); s=p.read_text()
old="echo '423ef244ed065a7733832054c83a5d4b5c957c833f574bd74ea0740f0390ee64  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -"
new="python3 .github/v652/runner/patch_v652_real_selfpump_seed_http.py .github/v651_gate/run-v651-full-release.sh\\necho 'd4d9db1bf30b975cd478b168bb46a464b8b1e5a31ef7660cff5b6e7f67863a14  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -"
if s.count(old) != 1:
    raise SystemExit('BLOCKED: V6.52 v15 final-gate hash anchor not found exactly once')
p.write_text(s.replace(old,new,1))
PYV652V16
bash -n "$TMP"
chmod +x "$TMP"
"$TMP"
'''
if s.count(needle) != 1:
    raise SystemExit('BLOCKED: V6.52 v15 execution block not found exactly once')
Path(sys.argv[2]).write_text(s.replace(needle,replacement,1))
PY
bash -n "$TMP"
chmod +x "$TMP"
"$TMP"
