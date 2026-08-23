#!/usr/bin/env bash
set -euo pipefail
BASE=.github/v653/runner/run-v653-full-release.sh
[ "$(git hash-object "$BASE")" = "e34b1905ed9b7b34cadcc28639dd4819ebb82ce9" ] || { echo 'BLOCKED: V6.53 base release runner blob drift'; exit 1; }
TMP=/tmp/run-v653-full-release-v4-generated.sh
python3 - "$BASE" "$TMP" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]); s=p.read_text()
start_marker="stage '1 BINDING + COMPLETE V6.52 PREDECESSOR RELEASE WORKFLOW FROM ZERO'"
end_marker="stage '2 EXACT PRE-FIX RED COUNTERPROOF'"
if s.count(start_marker)!=1 or s.count(end_marker)!=1:
    raise SystemExit('BLOCKED: V6.53 stage boundary drift')
i=s.index(start_marker); j=s.index(end_marker)
replacement=r'''stage '1 BINDING TO IMMUTABLE VERIFIED V6.52 RELEASE ARTIFACT'
ART=/tmp/V652_FINAL_VERIFIED_RELEASE.zip
ARTDIR=/tmp/v652-final-verified-release
rm -rf "$ARTDIR" /tmp/v653-base-master
rm -f "$ART"
mkdir -p "$ARTDIR"
command -v gh >/dev/null || { echo 'BLOCKED: GitHub CLI unavailable for immutable predecessor artifact'; exit 1; }
gh api repos/hallo-netizen/affiliate-pferdeportal/actions/artifacts/9489291638/zip > "$ART"
echo '1a691c0ef5930a462e7ac8176e051c30b219066e9f14dfab4a91440a2391389b  '"$ART" | sha256sum -c -
unzip -t "$ART" > "$E/01_v652_artifact_integrity.log"
unzip -q "$ART" -d "$ARTDIR"
V652_INSTALL="$ARTDIR/affiliate-zentrale_v6.52.0_CORE_CRON_SELFPUMP_ROOTFIX_REALGATE.zip"
V652_MASTER="$ARTDIR/MASTER_AFFILIATE_ZENTRALE_V6_52_0_CORE_CRON_SELFPUMP_ROOTFIX_REALGATE_20260822.zip"
test -f "$V652_INSTALL" -a -f "$V652_MASTER"
echo 'e8090b31c853031bbc65492845672d5e2ab1268452ac7c944e3459873a7684b2  '"$V652_INSTALL" | sha256sum -c -
echo '517b0939fe042ace8ab093efc86f754d340c80cb5ba543ff10d61b087fbc7778  '"$V652_MASTER" | sha256sum -c -
grep -Fxq 'FINAL_RELEASE_GATE=PASS' "$ARTDIR/V652_RELEASE_EVIDENCE/41_FINAL_RELEASE_GATE.txt"
grep -Fxq 'EXTERNAL_EBAY_PROVIDER_LIVE_E2E=OPEN_NOT_CLAIMED' "$ARTDIR/V652_RELEASE_EVIDENCE/FINAL_DECISION.txt"
unzip -t "$V652_INSTALL" > "$E/01_v652_install_integrity.log"
unzip -t "$V652_MASTER" > "$E/01_v652_master_integrity.log"
unzip -q "$V652_MASTER" -d /tmp/v653-base-master
BASE=/tmp/v653-base-master/master-v652/03_SOURCE/affiliate-portal-router
test -f "$BASE/pferdeportal-affiliate-router.php"
cat > "$E/01_v652_binding.txt" <<EOF
V652_ARTIFACT_ID=9489291638
V652_ARTIFACT_SHA256=1a691c0ef5930a462e7ac8176e051c30b219066e9f14dfab4a91440a2391389b
V652_INSTALLER_SHA256=e8090b31c853031bbc65492845672d5e2ab1268452ac7c944e3459873a7684b2
V652_MASTER_SHA256=517b0939fe042ace8ab093efc86f754d340c80cb5ba543ff10d61b087fbc7778
V652_FINAL_RELEASE_GATE=PASS
V652_EXTERNAL_EBAY_PROVIDER_LIVE_E2E=OPEN_NOT_CLAIMED
EOF

'''
s=s[:i]+replacement+s[j:]
# All real-gate stages use the same isolated database required by the inherited V6.52 A-H harness.
if s.count('v653gate') < 3:
    raise SystemExit('BLOCKED: expected V6.53 test DB anchors missing')
s=s.replace('v653gate','v651gate')
p.write_text(s)
PY
bash -n "$TMP"
chmod +x "$TMP"
"$TMP"
