#!/usr/bin/env bash
set -euo pipefail
BASE='.github/v656/runner/run-v656-full-release.sh'
EXPECTED='dc20deaf8111776157d8267a83be1bb58baf90da'
[ "$(git hash-object "$BASE")" = "$EXPECTED" ] || { echo 'BLOCKED: V6.56 base runner drift'; exit 1; }
TMP='/tmp/v656-release-v3.sh'
python3 - "$BASE" "$TMP" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1])
s=p.read_text()
a="E='V656_RELEASE_EVIDENCE'"
b='E="$GITHUB_WORKSPACE/V656_RELEASE_EVIDENCE"'
if s.count(a)!=1:
    raise SystemExit('BLOCKED evidence-path anchor drift')
s=s.replace(a,b,1)
a='cp "$E/FINAL_DECISION.txt" "$MD/05_EVIDENCE/FINAL_DECISION.txt"; rm -f "$MD/07_DIFF_AND_HASHES/MASTER_MANIFEST_SHA256.txt" "$OUT_MASTER";'
b='rm -rf "$MD/05_EVIDENCE"; mkdir -p "$MD/05_EVIDENCE"; cp -a "$E/." "$MD/05_EVIDENCE/"; rm -f "$MD/07_DIFF_AND_HASHES/MASTER_MANIFEST_SHA256.txt" "$OUT_MASTER";'
if s.count(a)!=1:
    raise SystemExit('BLOCKED final-evidence anchor drift')
s=s.replace(a,b,1)
Path(sys.argv[2]).write_text(s)
PY
bash -n "$TMP"
grep -Fq 'GITHUB_WORKSPACE/V656_RELEASE_EVIDENCE' "$TMP"
grep -Fq 'cp -a "$E/." "$MD/05_EVIDENCE/"' "$TMP"
chmod +x "$TMP"
exec "$TMP"
