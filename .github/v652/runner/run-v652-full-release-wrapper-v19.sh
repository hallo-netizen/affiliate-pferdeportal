#!/usr/bin/env bash
set -euo pipefail
BASE=.github/v652/runner/run-v652-full-release-wrapper-v18.sh
[ "$(git hash-object "$BASE")" = "70c645d564ae925c85540cc51dff99b8999ec844" ] || { echo 'BLOCKED: V6.52 v18 wrapper blob mismatch'; exit 1; }
[ "$(git hash-object .github/v652/runner/patch_v652_final_arch_legacy_red.py)" = "7f5c5a6ec7fd97896dc0ed170787efc2ddcd32ee" ] || { echo 'BLOCKED: V6.52 final legacy-red patcher blob mismatch'; exit 1; }
[ "$(git hash-object .github/v652/runner/patch_v652_lock_failclosed_release_gate.py)" = "b0a9c13c2042f8483cb0e09ea32670118e5c6d8e" ] || { echo 'BLOCKED: V6.52 lock failclosed release-gate patcher blob mismatch'; exit 1; }
[ "$(git hash-object .github/v652/runner/patch_v652_real_ah_transport_isolation.py)" = "48b9aff196ff357a74d01530d391a569c26d0dd8" ] || { echo 'BLOCKED: V6.52 real A-H transport-isolation patcher blob mismatch'; exit 1; }
TMP=/tmp/run-v652-full-release-wrapper-v19-generated.sh
python3 - "$BASE" "$TMP" <<'PY'
from pathlib import Path
import sys
s=Path(sys.argv[1]).read_text()
old="echo '9b977cf8e83823a9d873536d6e2ab5ae9dcbbdcc233d20d5e7a45047cd8405b9  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -"
sep=chr(92)*4+'n'
new=(
    "python3 .github/v652/runner/patch_v652_final_arch_legacy_red.py .github/v651_gate/run-v651-full-release.sh"
    + sep +
    "python3 .github/v652/runner/patch_v652_lock_failclosed_release_gate.py .github/v651_gate/run-v651-full-release.sh"
    + sep +
    "python3 .github/v652/runner/patch_v652_real_ah_transport_isolation.py .github/v651_gate/run-v651-full-release.sh"
    + sep +
    "echo '28e7a2fe2d8c5c0fb7533ee0e8bc130636c447f559f7283f6e211f9d64fb912e  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -"
)
if s.count(old)!=1:
    raise SystemExit('BLOCKED: V6.52 v18 final-gate checksum anchor not found exactly once')
Path(sys.argv[2]).write_text(s.replace(old,new,1))
PY
bash -n "$TMP"
chmod +x "$TMP"
"$TMP"
