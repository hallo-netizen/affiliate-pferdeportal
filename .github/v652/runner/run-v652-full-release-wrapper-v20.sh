#!/usr/bin/env bash
set -euo pipefail
BASE=.github/v652/runner/run-v652-full-release-wrapper-v19.sh
[ "$(git hash-object "$BASE")" = "66e92f190d65cc46ac0d0bd175506b3a9b8a2e3a" ] || { echo 'BLOCKED: V6.52 v19 wrapper blob mismatch'; exit 1; }
[ "$(git hash-object .github/v652/runner/patch_v652_lock_failclosed_release_gate.py)" = "b0a9c13c2042f8483cb0e09ea32670118e5c6d8e" ] || { echo 'BLOCKED: V6.52 lock failclosed release-gate patcher blob mismatch'; exit 1; }
TMP=/tmp/run-v652-full-release-wrapper-v20-generated.sh
python3 - "$BASE" "$TMP" <<'PY'
from pathlib import Path
import sys
s=Path(sys.argv[1]).read_text()
old="python3 .github/v652/runner/patch_v652_final_arch_legacy_red.py .github/v651_gate/run-v651-full-release.sh\\\\necho 'b75ea0cf44dc80ba26433dd9c444368ea0cc6c4b8da5d92da0ec1a2cdfb85d6e  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -"
new="python3 .github/v652/runner/patch_v652_final_arch_legacy_red.py .github/v651_gate/run-v651-full-release.sh\\\\npython3 .github/v652/runner/patch_v652_lock_failclosed_release_gate.py .github/v651_gate/run-v651-full-release.sh\\\\necho 'f89bb521fe2fa0e05cfdda51ee8eb90d39d4ec8d5aebf8f6470015b4e15cb763  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -"
if s.count(old)!=1:
    raise SystemExit('BLOCKED: V6.52 v19 final-gate payload anchor not found exactly once')
Path(sys.argv[2]).write_text(s.replace(old,new,1))
PY
bash -n "$TMP"
chmod +x "$TMP"
"$TMP"
