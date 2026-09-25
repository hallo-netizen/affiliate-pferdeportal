#!/usr/bin/env bash
set -euo pipefail
BASE=.github/v652/runner/run-v652-full-release-wrapper-v12.sh
[ "$(git hash-object "$BASE")" = "141280f70b077be77c5933c10a7709679b39aa5c" ] || { echo 'BLOCKED: V6.52 v12 wrapper blob mismatch'; exit 1; }
[ "$(git hash-object .github/v652/patches/01_core_cron_selfpump_rootfix.patch)" = "0e85087deca8875b244e466126e8fe5ffcf7ca49" ] || { echo 'BLOCKED: V6.52 production rootfix blob mismatch'; exit 1; }
[ "$(git hash-object .github/v652/manifests/STEP1_SOURCE_SHA256.txt)" = "476f1146ba563ce4b93429bdef90f69da12e5778" ] || { echo 'BLOCKED: V6.52 step1 manifest blob mismatch'; exit 1; }
[ "$(git hash-object .github/v652/tests/test_background_selfpump_v652.php)" = "28bf164355b678ce5920ffd7e7056904fba61030" ] || { echo 'BLOCKED: V6.52 transport test blob mismatch'; exit 1; }
TARGET_CHECK=/tmp/v652-gate-target.check.sh
base64 -d .github/v652/runner/v652_gate_target.sh.gz.b64 | gzip -d > "$TARGET_CHECK"
echo '29ac323e8fb8762dd4163942fdf477bd3f48280060e1c67e66e395213f60974c  /tmp/v652-gate-target.check.sh' | sha256sum -c -
TMP=/tmp/run-v652-full-release-wrapper-v13-generated.sh
python3 - "$BASE" "$TMP" <<'PY'
from pathlib import Path
import sys
src=Path(sys.argv[1]).read_text()
start='[ "$(git hash-object .github/v652/runner/14_v652_gate_runner.patch.b64.00)" = "ec2ba24e08af1ea4782640596dd9b6aca5027630" ]'
end="echo '4d142e919eadde2143faad380617f9d43317a6bdcd652d70d415a8aff55476b4  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -"
i=src.find(start); j=src.find(end,i)
if i < 0 or j < 0:
    raise SystemExit('BLOCKED: V6.52 v12 obsolete gate-chunk block not found exactly')
j += len(end)
replacement=r'''base64 -d .github/v652/runner/v652_gate_target.sh.gz.b64 | gzip -d > .github/v651_gate/run-v651-full-release.sh
echo '29ac323e8fb8762dd4163942fdf477bd3f48280060e1c67e66e395213f60974c  .github/v651_gate/run-v651-full-release.sh' | sha256sum -c -'''
Path(sys.argv[2]).write_text(src[:i]+replacement+src[j:])
PY
bash -n "$TMP"
chmod +x "$TMP"
set +e
"$TMP"
rc=$?
set -e
if [ "$rc" -ne 0 ]; then
  D=V652_RELEASE_EVIDENCE/BLOCKED_DIAGNOSTIC_V13
  mkdir -p "$D"
  [ ! -d /tmp/v652-source/affiliate-portal-router ] || cp -a /tmp/v652-source/affiliate-portal-router "$D/affiliate-portal-router"
  [ ! -f .github/v651_gate/run-v651-full-release.sh ] || cp .github/v651_gate/run-v651-full-release.sh "$D/run-v652-full-release.final.sh"
  (cd "$D" && find . -type f -print0 | sort -z | xargs -0 sha256sum) > "$D/SHA256.txt" || true
fi
exit "$rc"
