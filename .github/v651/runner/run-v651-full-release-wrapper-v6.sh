#!/usr/bin/env bash
set -euo pipefail
BASE=.github/v651/runner/run-v651-full-release-wrapper-v3.sh
[ "$(git hash-object "$BASE")" = "54e873e36ed7290d320c4f76c232e851ede18f6f" ] || { echo 'BLOCKED: V6.51 v3 wrapper blob mismatch'; exit 1; }
[ "$(git hash-object .github/v651/runner/09_real_gate_version_parameterization_runner.patch)" = "df34f3ad40cfeebb083a76eea3f968c26df5604d" ] || { echo 'BLOCKED: real-gate version parameterization patch blob mismatch'; exit 1; }
[ "$(git hash-object .github/v651/runner/10_real_ah_v651_successor_runner.patch)" = "9e4bf451f3c8f448a61c603cc7f30116fc7c44f4" ] || { echo 'BLOCKED: real A-H V6.51 successor patch blob mismatch'; exit 1; }
TMP=/tmp/run-v651-full-release-wrapper-v6-expanded.sh
python3 - <<'PY'
from pathlib import Path
src=Path('.github/v651/runner/run-v651-full-release-wrapper-v3.sh').read_text()
needle="echo '0e8ac3fa514ac9cf9e25bbe095f84bafa2ea5d002ad7c8aed0995eea9931e698  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -\\n\\nphp -l"
insert="echo '0e8ac3fa514ac9cf9e25bbe095f84bafa2ea5d002ad7c8aed0995eea9931e698  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -\\n[ \\\"$(git hash-object .github/v651/runner/09_real_gate_version_parameterization_runner.patch)\\\" = \\\"df34f3ad40cfeebb083a76eea3f968c26df5604d\\\" ] || { echo 'BLOCKED: real-gate version parameterization patch blob mismatch'; exit 1; }\\npatch -p0 --forward --batch < .github/v651/runner/09_real_gate_version_parameterization_runner.patch\\necho '5b024809f96d1fa1e61461aa6aca35e8ab60bcfa3a9c531a77bf3d21c6623721  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -\\n[ \\\"$(git hash-object .github/v651/runner/10_real_ah_v651_successor_runner.patch)\\\" = \\\"9e4bf451f3c8f448a61c603cc7f30116fc7c44f4\\\" ] || { echo 'BLOCKED: real A-H V6.51 successor patch blob mismatch'; exit 1; }\\npatch -p0 --forward --batch < .github/v651/runner/10_real_ah_v651_successor_runner.patch\\necho '625b5549e9742dd3b619af55ea1a8a1a33e50cb6c6f7762f4f51ecf89b0d61e1  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -\\n\\nphp -l"
if needle not in src:
    raise SystemExit('BLOCKED: v3 real-gate insertion anchor missing')
Path('/tmp/run-v651-full-release-wrapper-v6-expanded.sh').write_text(src.replace(needle,insert,1))
PY
bash -n "$TMP"
chmod +x "$TMP"
set +e
"$TMP"
rc=$?
set -e
if [ "$rc" -ne 0 ]; then
  D=V651_RELEASE_EVIDENCE/BLOCKED_DIAGNOSTIC_V6
  PKG=/tmp/v651pkg/CODEX_V645_REALGATE_SOURCE_AND_EXACT_TASK_20260820
  mkdir -p "$D"
  [ ! -d "$PKG/03_REAL_GATE" ] || cp -a "$PKG/03_REAL_GATE" "$D/03_REAL_GATE"
  [ ! -d "$PKG/07_RUNNERS" ] || cp -a "$PKG/07_RUNNERS" "$D/07_RUNNERS"
  [ ! -d "$PKG/CODEX_EVIDENCE_REAL_GATE" ] || cp -a "$PKG/CODEX_EVIDENCE_REAL_GATE" "$D/CODEX_EVIDENCE_REAL_GATE"
  [ ! -d /tmp/v651-source/affiliate-portal-router ] || cp -a /tmp/v651-source/affiliate-portal-router "$D/affiliate-portal-router"
  [ ! -f .github/v651_gate/run-v651-full-release.sh ] || cp .github/v651_gate/run-v651-full-release.sh "$D/run-v651-full-release.final.sh"
  (cd "$D" && find . -type f -print0 | sort -z | xargs -0 sha256sum) > "$D/SHA256.txt" || true
fi
exit "$rc"
