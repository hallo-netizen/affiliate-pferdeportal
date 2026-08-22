#!/usr/bin/env bash
set -euo pipefail
BASE=.github/v652/runner/run-v652-full-release-wrapper-v16.sh
[ "$(git hash-object "$BASE")" = "2476596629357e1f7eab4a19f5e6f3cc388db15c" ] || { echo 'BLOCKED: V6.52 v16 wrapper blob mismatch'; exit 1; }
[ "$(git hash-object .github/v652/runner/patch_v652_selfpump_harness_clean.py)" = "c4782bb4a4cb3f950efde9a8aaadfaea1994e742" ] || { echo 'BLOCKED: V6.52 clean selfpump harness patcher blob mismatch'; exit 1; }
TMP=/tmp/run-v652-full-release-wrapper-v18-generated.sh
python3 - "$BASE" "$TMP" <<'PY'
from pathlib import Path
import sys
s=Path(sys.argv[1]).read_text()
old="new=\"python3 .github/v652/runner/patch_v652_real_selfpump_seed_http.py .github/v651_gate/run-v651-full-release.sh\\\\necho 'd4d9db1bf30b975cd478b168bb46a464b8b1e5a31ef7660cff5b6e7f67863a14  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -\""
new="new=\"python3 .github/v652/runner/patch_v652_real_selfpump_seed_http.py .github/v651_gate/run-v651-full-release.sh\\\\npython3 .github/v652/runner/patch_v652_selfpump_harness_clean.py .github/v651_gate/run-v651-full-release.sh\\\\necho '9b977cf8e83823a9d873536d6e2ab5ae9dcbbdcc233d20d5e7a45047cd8405b9  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -\""
if s.count(old)!=1:
    raise SystemExit('BLOCKED: V6.52 v16 final-gate injection anchor not found exactly once')
Path(sys.argv[2]).write_text(s.replace(old,new,1))
PY
bash -n "$TMP"
chmod +x "$TMP"
"$TMP"
