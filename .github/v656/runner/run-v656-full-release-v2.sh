#!/usr/bin/env bash
set -euo pipefail
BASE='.github/v656/runner/run-v656-full-release.sh'
[ "$(git hash-object "$BASE")" = 'dc20deaf8111776157d8267a83be1bb58baf90da' ] || { echo 'BLOCKED: V6.56 base runner drift'; exit 1; }
TMP='/tmp/run-v656-full-release-v2.sh'
sed "s#^E='V656_RELEASE_EVIDENCE'$#E=\"\$GITHUB_WORKSPACE/V656_RELEASE_EVIDENCE\"#" "$BASE" > "$TMP"
grep -Fxq 'E="$GITHUB_WORKSPACE/V656_RELEASE_EVIDENCE"' "$TMP"
bash -n "$TMP"
chmod +x "$TMP"
exec "$TMP"
