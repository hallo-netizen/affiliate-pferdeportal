#!/usr/bin/env bash
set -euo pipefail
BASE=.github/v651/runner/run-v651-full-release-wrapper-v4.sh
[ "$(git hash-object "$BASE")" = "2dc891cab679dc352ab6308f771ea39b15cb6234" ] || { echo 'BLOCKED: V6.51 v4 wrapper blob mismatch'; exit 1; }
set +e
"$BASE"
rc=$?
set -e
if [ "$rc" -ne 0 ]; then
  D=V651_RELEASE_EVIDENCE/BLOCKED_REAL_GATE_DIAGNOSTIC
  PKG=/tmp/v651pkg/CODEX_V645_REALGATE_SOURCE_AND_EXACT_TASK_20260820
  mkdir -p "$D"
  if [ -d "$PKG/03_REAL_GATE" ]; then cp -a "$PKG/03_REAL_GATE" "$D/03_REAL_GATE"; fi
  if [ -d "$PKG/07_RUNNERS" ]; then cp -a "$PKG/07_RUNNERS" "$D/07_RUNNERS"; fi
  if [ -d "$PKG/CODEX_EVIDENCE_REAL_GATE" ]; then cp -a "$PKG/CODEX_EVIDENCE_REAL_GATE" "$D/CODEX_EVIDENCE_REAL_GATE"; fi
  if [ -d "$D" ]; then (cd "$D" && find . -type f -print0 | sort -z | xargs -0 sha256sum) > "$D/SHA256.txt"; fi
fi
exit "$rc"
