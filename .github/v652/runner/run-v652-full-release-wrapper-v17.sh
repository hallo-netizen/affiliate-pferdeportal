#!/usr/bin/env bash
set -euo pipefail
BASE=.github/v652/runner/run-v652-full-release-wrapper-v16.sh
[ "$(git hash-object "$BASE")" = "2476596629357e1f7eab4a19f5e6f3cc388db15c" ] || { echo 'BLOCKED: V6.52 v16 wrapper blob mismatch'; exit 1; }
[ "$(git hash-object .github/v652/runner/patch_v652_selfpump_harness_clean.py)" = "c4782bb4a4cb3f950efde9a8aaadfaea1994e742" ] || { echo 'BLOCKED: V6.52 selfpump harness patcher blob mismatch'; exit 1; }
TMP=/tmp/run-v652-full-release-wrapper-v17-generated.sh
python3 - "$BASE" "$TMP" <<'PY'
from pathlib import Path
import sys
s=Path(sys.argv[1]).read_text()
needle='bash -n "$TMP"\nchmod +x "$TMP"\n"$TMP"\n'
replacement='bash -n "$TMP"\npython3 .github/v652/runner/patch_v652_selfpump_harness_clean.py "$TMP"\nbash -n "$TMP"\nchmod +x "$TMP"\n"$TMP"\n'
if s.count(needle)!=1:
    raise SystemExit('BLOCKED: V6.52 v16 execution block not found exactly once')
Path(sys.argv[2]).write_text(s.replace(needle,replacement,1))
PY
bash -n "$TMP"
chmod +x "$TMP"
"$TMP"
