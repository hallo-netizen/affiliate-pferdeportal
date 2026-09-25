#!/usr/bin/env bash
set -euo pipefail
BASE=.github/v651/runner/run-v651-full-release-wrapper-v3.sh
[ "$(git hash-object "$BASE")" = "54e873e36ed7290d320c4f76c232e851ede18f6f" ] || { echo 'BLOCKED: V6.51 v3 wrapper blob mismatch'; exit 1; }
[ "$(git hash-object .github/v651/runner/09_real_gate_version_parameterization_runner.patch)" = "df34f3ad40cfeebb083a76eea3f968c26df5604d" ] || { echo 'BLOCKED: real-gate version parameterization patch blob mismatch'; exit 1; }
[ "$(git hash-object .github/v651/runner/10_real_ah_v651_successor_runner.patch)" = "9e4bf451f3c8f448a61c603cc7f30116fc7c44f4" ] || { echo 'BLOCKED: real A-H V6.51 successor patch blob mismatch'; exit 1; }
[ "$(git hash-object .github/v651/runner/11_real_ah_runtime_seed_contract_runner.patch)" = "3681b80c8819cd01c1db9e3de9b7185fd536a238" ] || { echo 'BLOCKED: real A-H runtime seed patch blob mismatch'; exit 1; }
[ "$(git hash-object .github/v651/runner/12_real_v649_checkpoint_successor_runner.patch)" = "84ac4eaa0796f429041d03dfd56bc85dda2992e4" ] || { echo 'BLOCKED: real V6.49 checkpoint successor patch blob mismatch'; exit 1; }
[ "$(git hash-object .github/v651/runner/13_real_db_reset_isolation_runner.patch)" = "cbf75091f866054e0757b8559972e21cc01c73e4" ] || { echo 'BLOCKED: real DB reset isolation patch blob mismatch'; exit 1; }
[ "$(git hash-object .github/v652/patches/01_core_cron_selfpump_rootfix.patch)" = "a51ba6c66bb0ebd995051edcf6d0362453ed79b2" ] || { echo 'BLOCKED: V6.52 production patch blob mismatch'; exit 1; }
[ "$(git hash-object .github/v652/manifests/STEP1_SOURCE_SHA256.txt)" = "1eccdacb02aa4d2498d2d132d44d326ed2df6735" ] || { echo 'BLOCKED: V6.52 step1 manifest blob mismatch'; exit 1; }
[ "$(git hash-object .github/v652/tests/test_background_selfpump_v652.php)" = "15627e04d129cd07b3399ed0cf1e1d37a383efa4" ] || { echo 'BLOCKED: V6.52 self-pump test blob mismatch'; exit 1; }
TMP=/tmp/run-v652-full-release-wrapper-v11-expanded.sh
python3 - <<'PY'
from pathlib import Path
src=Path('.github/v651/runner/run-v651-full-release-wrapper-v3.sh').read_text()
needle="echo '0e8ac3fa514ac9cf9e25bbe095f84bafa2ea5d002ad7c8aed0995eea9931e698  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -\\n\\nphp -l"
insert="""echo '0e8ac3fa514ac9cf9e25bbe095f84bafa2ea5d002ad7c8aed0995eea9931e698  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -
[ \"$(git hash-object .github/v651/runner/09_real_gate_version_parameterization_runner.patch)\" = \"df34f3ad40cfeebb083a76eea3f968c26df5604d\" ] || { echo 'BLOCKED: real-gate version parameterization patch blob mismatch'; exit 1; }
patch -p0 --forward --batch < .github/v651/runner/09_real_gate_version_parameterization_runner.patch
echo '5b024809f96d1fa1e61461aa6aca35e8ab60bcfa3a9c531a77bf3d21c6623721  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -
[ \"$(git hash-object .github/v651/runner/10_real_ah_v651_successor_runner.patch)\" = \"9e4bf451f3c8f448a61c603cc7f30116fc7c44f4\" ] || { echo 'BLOCKED: real A-H V6.51 successor patch blob mismatch'; exit 1; }
patch -p0 --forward --batch < .github/v651/runner/10_real_ah_v651_successor_runner.patch
echo '625b5549e9742dd3b619af55ea1a8a1a33e50cb6c6f7762f4f51ecf89b0d61e1  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -
[ \"$(git hash-object .github/v651/runner/11_real_ah_runtime_seed_contract_runner.patch)\" = \"3681b80c8819cd01c1db9e3de9b7185fd536a238\" ] || { echo 'BLOCKED: real A-H runtime seed patch blob mismatch'; exit 1; }
patch -p0 --forward --batch < .github/v651/runner/11_real_ah_runtime_seed_contract_runner.patch
echo 'dacce5b47155af5722688ccbecb2d58cb9d51131c5747d04c38d96cc30e02ff7  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -
[ \"$(git hash-object .github/v651/runner/12_real_v649_checkpoint_successor_runner.patch)\" = \"84ac4eaa0796f429041d03dfd56bc85dda2992e4\" ] || { echo 'BLOCKED: real V6.49 checkpoint successor patch blob mismatch'; exit 1; }
patch -p0 --forward --batch < .github/v651/runner/12_real_v649_checkpoint_successor_runner.patch
echo '61706d7d596ab61de03f18e331d7d922ea48c50958fb083893cf92dfed14bf74  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -
[ \"$(git hash-object .github/v651/runner/13_real_db_reset_isolation_runner.patch)\" = \"cbf75091f866054e0757b8559972e21cc01c73e4\" ] || { echo 'BLOCKED: real DB reset isolation patch blob mismatch'; exit 1; }
patch -p0 --forward --batch < .github/v651/runner/13_real_db_reset_isolation_runner.patch
echo '391ef9fe9cfff8c907dc2d4964775665adc3c7b48d5240521812f56e24b273b8  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -
cat .github/v652/runner/14_v652_gate_runner.patch.b64.* > /tmp/v652-gate-runner.patch.b64
echo '24493d0e3a28f21dd2ade2896b58f33b8e21090b47d54a783146ded128fff9ad  /tmp/v652-gate-runner.patch.b64' | sha256sum -c -
base64 -d /tmp/v652-gate-runner.patch.b64 > /tmp/v652-gate-runner.patch
echo '196ac087f7b9bb07892b74f204f1c0c42016dd4fbd6e0b6ca5b339965f36d87e  /tmp/v652-gate-runner.patch' | sha256sum -c -
patch -p0 --forward --batch < /tmp/v652-gate-runner.patch
echo '4d142e919eadde2143faad380617f9d43317a6bdcd652d70d415a8aff55476b4  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -

php -l"""
if needle not in src:
    raise SystemExit('BLOCKED: v3 real-gate insertion anchor missing')
Path('/tmp/run-v652-full-release-wrapper-v11-expanded.sh').write_text(src.replace(needle,insert,1))
PY
bash -n "$TMP"
chmod +x "$TMP"
set +e
"$TMP"
rc=$?
set -e
if [ "$rc" -ne 0 ]; then
  D=V652_RELEASE_EVIDENCE/BLOCKED_DIAGNOSTIC_V11
  PKG=/tmp/v651pkg/CODEX_V645_REALGATE_SOURCE_AND_EXACT_TASK_20260820
  mkdir -p "$D"
  [ ! -d "$PKG/03_REAL_GATE" ] || cp -a "$PKG/03_REAL_GATE" "$D/03_REAL_GATE"
  [ ! -d "$PKG/07_RUNNERS" ] || cp -a "$PKG/07_RUNNERS" "$D/07_RUNNERS"
  [ ! -d "$PKG/CODEX_EVIDENCE_REAL_GATE" ] || cp -a "$PKG/CODEX_EVIDENCE_REAL_GATE" "$D/CODEX_EVIDENCE_REAL_GATE"
  [ ! -d /tmp/v652-source/affiliate-portal-router ] || cp -a /tmp/v652-source/affiliate-portal-router "$D/affiliate-portal-router"
  [ ! -f .github/v651_gate/run-v651-full-release.sh ] || cp .github/v651_gate/run-v651-full-release.sh "$D/run-v652-full-release.final.sh"
  (cd "$D" && find . -type f -print0 | sort -z | xargs -0 sha256sum) > "$D/SHA256.txt" || true
fi
exit "$rc"
