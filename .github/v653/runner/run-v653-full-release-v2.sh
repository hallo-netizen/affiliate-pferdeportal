#!/usr/bin/env bash
set -euo pipefail
BASE=.github/v653/runner/run-v653-full-release.sh
[ "$(git hash-object "$BASE")" = "e34b1905ed9b7b34cadcc28639dd4819ebb82ce9" ] || { echo 'BLOCKED: V6.53 base release runner blob drift'; exit 1; }
TMP=/tmp/run-v653-full-release-v2-generated.sh
python3 - "$BASE" "$TMP" <<'PY'
from pathlib import Path
import sys
s=Path(sys.argv[1]).read_text()
old='[ "$(git hash-object "$BASE_RUNNER")" = "66e92f190d65cc46ac0d0bd175506b3a9b8a2e3a" ] || { echo \'BLOCKED: V6.52 final runner blob drift\'; exit 1; }'
new='[ "$(git hash-object "$BASE_RUNNER")" = "d8b76717e2056958b9b61eb8db55641f27fc627a" ] || { echo \'BLOCKED: V6.52 final runner blob drift\'; exit 1; }'
if s.count(old)!=1:
    raise SystemExit('BLOCKED: V6.53 predecessor-runner hash anchor not found exactly once')
Path(sys.argv[2]).write_text(s.replace(old,new,1))
PY
bash -n "$TMP"
chmod +x "$TMP"
"$TMP"
