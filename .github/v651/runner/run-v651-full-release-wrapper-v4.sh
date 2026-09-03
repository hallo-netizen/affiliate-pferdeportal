#!/usr/bin/env bash
set -euo pipefail
BASE=.github/v651/runner/run-v651-full-release-wrapper-v3.sh
[ "$(git hash-object "$BASE")" = "54e873e36ed7290d320c4f76c232e851ede18f6f" ] || { echo 'BLOCKED: V6.51 v3 wrapper blob mismatch'; exit 1; }
[ "$(git hash-object .github/v651/runner/09_real_gate_version_parameterization_runner.patch)" = "df34f3ad40cfeebb083a76eea3f968c26df5604d" ] || { echo 'BLOCKED: real-gate version parameterization patch blob mismatch'; exit 1; }
TMP=/tmp/run-v651-full-release-wrapper-v4-expanded.sh
python3 - <<'PY'
from pathlib import Path
src=Path('.github/v651/runner/run-v651-full-release-wrapper-v3.sh').read_text()
needle="echo '0e8ac3fa514ac9cf9e25bbe095f84bafa2ea5d002ad7c8aed0995eea9931e698  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -\\n\\nphp -l"
insert="echo '0e8ac3fa514ac9cf9e25bbe095f84bafa2ea5d002ad7c8aed0995eea9931e698  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -\\n[ \\\"$(git hash-object .github/v651/runner/09_real_gate_version_parameterization_runner.patch)\\\" = \\\"df34f3ad40cfeebb083a76eea3f968c26df5604d\\\" ] || { echo 'BLOCKED: real-gate version parameterization patch blob mismatch'; exit 1; }\\npatch -p0 --forward --batch < .github/v651/runner/09_real_gate_version_parameterization_runner.patch\\necho '5b024809f96d1fa1e61461aa6aca35e8ab60bcfa3a9c531a77bf3d21c6623721  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -\\n\\nphp -l"
if needle not in src:
    raise SystemExit('BLOCKED: v3 real-gate insertion anchor missing')
Path('/tmp/run-v651-full-release-wrapper-v4-expanded.sh').write_text(src.replace(needle,insert,1))
PY
bash -n "$TMP"
chmod +x "$TMP"
exec "$TMP"
