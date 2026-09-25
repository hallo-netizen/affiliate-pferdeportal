#!/usr/bin/env bash
set -euo pipefail
BASE=.github/v652/runner/run-v652-full-release-wrapper-v14.sh
[ "$(git hash-object "$BASE")" = "3fbc116704b33573cb801fb8a4b815d650c7c56e" ] || { echo 'BLOCKED: V6.52 v14 wrapper blob mismatch'; exit 1; }
TMP=/tmp/run-v652-full-release-wrapper-v15-generated.sh
python3 - "$BASE" "$TMP" <<'PY'
from pathlib import Path
import sys
s=Path(sys.argv[1]).read_text()
old='replacement="python3 /tmp/transform_v651_gate_to_v652.py .github/v651_gate/run-v651-full-release.sh\\necho \'e63287d0766ff1b6bde32b089027c649f2734e4ddc68241af10a6c03adc7f9c0  .github/v651_gate/run-v651-full-release.sh\' | sha256sum -c -"'
new='replacement="python3 /tmp/transform_v651_gate_to_v652.py .github/v651_gate/run-v651-full-release.sh\\npython3 -c \'from pathlib import Path; p=Path(\\\".github/v651_gate/run-v651-full-release.sh\\\"); s=p.read_text(); assert s.count(\\\"ASSERTIONS=12 FAIL=0\\\")==1 and s.count(\\\"ASSERTIONS=15 FAIL=0\\\")==1; p.write_text(s.replace(\\\"ASSERTIONS=12 FAIL=0\\\",\\\"ASSERTIONS=16 FAIL=0\\\",1).replace(\\\"ASSERTIONS=15 FAIL=0\\\",\\\"ASSERTIONS=19 FAIL=0\\\",1))\'\\necho \'423ef244ed065a7733832054c83a5d4b5c957c833f574bd74ea0740f0390ee64  .github/v651_gate/run-v651-full-release.sh\' | sha256sum -c -"'
if s.count(old) != 1:
    raise SystemExit('BLOCKED: exact V6.52 v14 transform insertion not found once')
Path(sys.argv[2]).write_text(s.replace(old,new,1))
PY
bash -n "$TMP"
chmod +x "$TMP"
"$TMP"
