#!/usr/bin/env bash
set -euo pipefail
BASE=.github/v651/runner/run-v651-full-release-wrapper-v8.sh
[ "$(git hash-object "$BASE")" = "7369dab4ca1496177237772762e4b46fd985962b" ] || { echo 'BLOCKED: V6.51 v8 wrapper blob mismatch'; exit 1; }
[ "$(git hash-object .github/v652/patches/01_core_cron_selfpump_rootfix.patch)" = "a51ba6c66bb0ebd995051edcf6d0362453ed79b2" ] || { echo 'BLOCKED: V6.52 production patch blob mismatch'; exit 1; }
[ "$(git hash-object .github/v652/manifests/STEP1_SOURCE_SHA256.txt)" = "1eccdacb02aa4d2498d2d132d44d326ed2df6735" ] || { echo 'BLOCKED: V6.52 step1 manifest blob mismatch'; exit 1; }
[ "$(git hash-object .github/v652/tests/test_background_selfpump_v652.php)" = "15627e04d129cd07b3399ed0cf1e1d37a383efa4" ] || { echo 'BLOCKED: V6.52 self-pump test blob mismatch'; exit 1; }
TMP=/tmp/run-v652-full-release-wrapper-v9-generated.sh
python3 - <<'PY'
from pathlib import Path
src=Path('.github/v651/runner/run-v651-full-release-wrapper-v8.sh').read_text()
needle="echo '391ef9fe9cfff8c907dc2d4964775665adc3c7b48d5240521812f56e24b273b8  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -\\n\\nphp -l"
insert="echo '391ef9fe9cfff8c907dc2d4964775665adc3c7b48d5240521812f56e24b273b8  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -\\ncat .github/v652/runner/14_v652_gate_runner.patch.b64.* > /tmp/v652-gate-runner.patch.b64\\necho '24493d0e3a28f21dd2ade2896b58f33b8e21090b47d54a783146ded128fff9ad  /tmp/v652-gate-runner.patch.b64' | sha256sum -c -\\nbase64 -d /tmp/v652-gate-runner.patch.b64 > /tmp/v652-gate-runner.patch\\necho '196ac087f7b9bb07892b74f204f1c0c42016dd4fbd6e0b6ca5b339965f36d87e  /tmp/v652-gate-runner.patch' | sha256sum -c -\\npatch -p0 --forward --batch < /tmp/v652-gate-runner.patch\\necho '4d142e919eadde2143faad380617f9d43317a6bdcd652d70d415a8aff55476b4  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -\\n\\nphp -l"
if needle not in src:
    raise SystemExit('BLOCKED: V6.52 post-V6.51 gate insertion anchor missing')
src=src.replace(needle,insert,1)
src=src.replace('TMP=/tmp/run-v651-full-release-wrapper-v8-expanded.sh','TMP=/tmp/run-v652-full-release-wrapper-v9-expanded.sh',1)
src=src.replace('D=V651_RELEASE_EVIDENCE/BLOCKED_DIAGNOSTIC_V8','D=V652_RELEASE_EVIDENCE/BLOCKED_DIAGNOSTIC_V9',1)
src=src.replace('/tmp/v651-source/affiliate-portal-router','/tmp/v652-source/affiliate-portal-router')
Path('/tmp/run-v652-full-release-wrapper-v9-generated.sh').write_text(src)
PY
bash -n "$TMP"
chmod +x "$TMP"
set +e
"$TMP"
rc=$?
set -e
if [ "$rc" -ne 0 ]; then
  D=V652_RELEASE_EVIDENCE/BLOCKED_DIAGNOSTIC_V9_OUTER
  mkdir -p "$D"
  [ ! -d /tmp/v652-source/affiliate-portal-router ] || cp -a /tmp/v652-source/affiliate-portal-router "$D/affiliate-portal-router"
  [ ! -f .github/v651_gate/run-v651-full-release.sh ] || cp .github/v651_gate/run-v651-full-release.sh "$D/run-v652-full-release.final.sh"
  (cd "$D" && find . -type f -print0 | sort -z | xargs -0 sha256sum) > "$D/SHA256.txt" || true
fi
exit "$rc"
