#!/usr/bin/env bash
set -euo pipefail
BASE=.github/v652/runner/run-v652-full-release-wrapper-v12.sh
[ "$(git hash-object "$BASE")" = "141280f70b077be77c5933c10a7709679b39aa5c" ] || { echo 'BLOCKED: V6.52 v12 wrapper blob mismatch'; exit 1; }
TMP=/tmp/v652-materialize-v651-after13.sh
python3 - "$BASE" "$TMP" <<'PY'
from pathlib import Path
import sys
s=Path(sys.argv[1]).read_text()
start='[ "$(git hash-object .github/v652/runner/14_v652_gate_runner.patch.b64.00)" = "ec2ba24e08af1ea4782640596dd9b6aca5027630" ]'
end="echo '4d142e919eadde2143faad380617f9d43317a6bdcd652d70d415a8aff55476b4  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -"
i=s.find(start); j=s.find(end,i)
if i < 0 or j < 0:
    raise SystemExit('BLOCKED: V6.52 obsolete post13 block not found exactly')
j += len(end)
replacement="mkdir -p V652_GATE_MATERIALIZED_DIAGNOSTIC\ncp .github/v651_gate/run-v651-full-release.sh V652_GATE_MATERIALIZED_DIAGNOSTIC/run-v651-full-release.after13.sh\nsha256sum V652_GATE_MATERIALIZED_DIAGNOSTIC/run-v651-full-release.after13.sh > V652_GATE_MATERIALIZED_DIAGNOSTIC/SHA256.txt\nexit 0"
Path(sys.argv[2]).write_text(s[:i]+replacement+s[j:])
PY
bash -n "$TMP"
chmod +x "$TMP"
"$TMP"
test -s V652_GATE_MATERIALIZED_DIAGNOSTIC/run-v651-full-release.after13.sh
