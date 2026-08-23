#!/usr/bin/env bash
set -euo pipefail
WORK="${GITHUB_WORKSPACE:-$(pwd)}"
E="$WORK/V655_RELEASE_EVIDENCE"
PATCHER="$WORK/.github/v655/patches/apply_v655_patch.py"
ARCH="$WORK/.github/v655/tests/test_kiss_public_heartbeat_architecture_v655.php"
REAL="$WORK/.github/v655/tests/real_public_heartbeat_v655.php"
PARITY="$WORK/.github/v654/tests/test_v654_untouched_workflow_parity.php"
PRODUCT="$WORK/.github/v654/tests/test_article_product_regression_v654.php"
PRODUCT_FUNC="$WORK/.github/v653/tests/test_article_product_portal_standard_v653.php"
REAL_PRODUCT="$WORK/.github/v654/tests/real_article_product_v654.php"
SCHED="$WORK/.github/v655/templates/pferde-atelier-ebay-heartbeat.yml"
INSTALL="$WORK/affiliate-zentrale_v6.55.0_KISS_PUBLIC_HEARTBEAT_GITHUB_SCHEDULER_REALGATE.zip"
MASTER="$WORK/MASTER_AFFILIATE_ZENTRALE_V6_55_0_KISS_PUBLIC_HEARTBEAT_GITHUB_SCHEDULER_REALGATE_20260823.zip"
rm -rf "$E" /tmp/v655-* /tmp/master-v655
rm -f "$INSTALL" "$MASTER"
mkdir -p "$E"
stage(){ printf '\n===== %s =====\n' "$1" | tee -a "$E/STAGE_LOG.txt"; }

stage '1 IMMUTABLE V6.54 FINAL BINDING'
ART=/tmp/v655-v654-final.zip; ARTDIR=/tmp/v655-v654-artifact
mkdir -p "$ARTDIR"
command -v gh >/dev/null || { echo 'BLOCKED gh missing'; exit 1; }
gh api repos/hallo-netizen/affiliate-pferdeportal/actions/artifacts/9492368681/zip > "$ART"
echo '11f4b4665742bbc0dda1b75221bfa4c1c10c2a94612fd2a9edfb5cb7f11f1383  '"$ART" | sha256sum -c -
unzip -t "$ART" > "$E/01_v654_artifact_integrity.log"
unzip -q "$ART" -d "$ARTDIR"
V654_INSTALL="$ARTDIR/affiliate-zentrale_v6.54.0_KISS_EXTERNAL_TICK_SKIP_REALGATE.zip"
V654_MASTER="$ARTDIR/MASTER_AFFILIATE_ZENTRALE_V6_54_0_KISS_EXTERNAL_TICK_SKIP_REALGATE_20260823.zip"
echo '2ac4b5453fc9076f2439853a3ba25fee45689b48d9655022efdf5d8c91c12a31  '"$V654_INSTALL" | sha256sum -c -
echo '5cdcda55c2f868a99e0093d82bd76dcdee15c50fd8eb1686f0ec54e76df57877  '"$V654_MASTER" | sha256sum -c -
grep -Fxq 'FINAL_RELEASE_GATE=PASS' "$ARTDIR/V654_RELEASE_EVIDENCE/FINAL_DECISION.txt"
unzip -q "$V654_MASTER" -d /tmp/v655-base-master
BASE=/tmp/v655-base-master/master-v654/03_SOURCE/affiliate-portal-router
test -f "$BASE/pferdeportal-affiliate-router.php"
grep -Fq "const VERSION = '6.54.0';" "$BASE/pferdeportal-affiliate-router.php"
cat > "$E/01_binding.txt" <<EOF
V654_ARTIFACT_ID=9492368681
V654_ARTIFACT_SHA256=11f4b4665742bbc0dda1b75221bfa4c1c10c2a94612fd2a9edfb5cb7f11f1383
V654_INSTALLER_SHA256=2ac4b5453fc9076f2439853a3ba25fee45689b48d9655022efdf5d8c91c12a31
V654_MASTER_SHA256=5cdcda55c2f868a99e0093d82bd76dcdee15c50fd8eb1686f0ec54e76df57877
V654_FINAL_RELEASE_GATE=PASS
EOF

stage '2 PRE-FIX RED + V6.54 PROTECTED BASELINE'
set +e
PPAR_TEST_PLUGIN_DIR="$BASE" php "$ARCH" > "$E/02_prefx_red.log" 2>&1
red=$?
set -e
cat "$E/02_prefx_red.log"
[ "$red" -ne 0 ]
grep -Fxq 'ASSERTIONS=23 FAIL=16' "$E/02_prefx_red.log"
PPAR_TEST_PLUGIN_DIR="$BASE" php "$PRODUCT" | tee "$E/02_product_baseline.log"
PPAR_TEST_PLUGIN_DIR="$BASE" php "$PRODUCT_FUNC" | tee "$E/02_product_functional_baseline.log"
grep -Fxq 'PRODUCT_REGRESSION_ASSERTIONS=11 FAIL=0' "$E/02_product_baseline.log"
grep -Fxq 'ASSERTIONS=14 FAIL=0' "$E/02_product_functional_baseline.log"

stage '3 APPLY ONE ATOMIC V6.55 KISS ROOTFIX + SCOPE'
mkdir -p /tmp/v655-source
cp -a "$BASE" /tmp/v655-source/affiliate-portal-router
python3 "$PATCHER" /tmp/v655.patch | tee "$E/03_patch_decode.log"
echo 'afaca48f14f94087c2fbe8b8a846a7e85ce2b489558223e3b185276106b0d865  /tmp/v655.patch' | sha256sum -c -
( cd /tmp/v655-source && patch -p1 --dry-run --batch < /tmp/v655.patch ) > "$E/03_patch_dryrun.log"
( cd /tmp/v655-source && patch -p1 --batch < /tmp/v655.patch ) > "$E/03_patch_apply.log"
SRC=/tmp/v655-source/affiliate-portal-router
diff -qr "$BASE" "$SRC" > "$E/03_scope.diff" || true
cat "$E/03_scope.diff"
python3 - "$E/03_scope.diff" <<'PY' | tee "$E/03_scope_gate.log"
from pathlib import Path
import re,sys
expected={'pferdeportal-affiliate-router.php','includes/trait-ppar-ebay-run.php','includes/trait-ppar-ebay.php','readme.txt'}
seen=set()
for line in Path(sys.argv[1]).read_text().splitlines():
    if not line.strip(): continue
    m=re.search(r'/affiliate-portal-router/(.+?) and ',line)
    if not m: raise SystemExit('BLOCKED unexpected scope: '+line)
    seen.add(m.group(1))
if seen != expected: raise SystemExit(f'BLOCKED scope {sorted(seen)} expected {sorted(expected)}')
print('PRODUCTION_SCOPE=PASS files=4 design_plugin_changes=0')
PY
grep -Fxq 'PRODUCTION_SCOPE=PASS files=4 design_plugin_changes=0' "$E/03_scope_gate.log"

stage '4 COMPLETE MODIFIED-SOURCE WORKFLOW GATE'
find "$SRC" -type f -name '*.php' -print0 | sort -z | xargs -0 -n1 php -l > "$E/04_php_lint.log"
php -r '$f=array_slice($argv,1);foreach($f as $x){json_decode(file_get_contents($x),true);if(json_last_error()){fwrite(STDERR,"JSON_FAIL $x\n");exit(1);}echo "JSON_OK $x\n";}' "$SRC/assets/ebay-portal-catalog-v2.json" "$SRC/assets/portal-structure-v279.json" > "$E/04_json.log"
PPAR_TEST_PLUGIN_DIR="$SRC" php "$ARCH" | tee "$E/04_architecture.log"
PPAR_BASE_PLUGIN_DIR="$BASE" PPAR_TEST_PLUGIN_DIR="$SRC" php "$PARITY" | tee "$E/04_workflow_parity.log"
PPAR_TEST_PLUGIN_DIR="$SRC" php "$PRODUCT" | tee "$E/04_product_regression.log"
PPAR_TEST_PLUGIN_DIR="$SRC" php "$PRODUCT_FUNC" | tee "$E/04_product_functional.log"
grep -Fxq 'ASSERTIONS=23 FAIL=0' "$E/04_architecture.log"
grep -Fxq 'PARITY_ASSERTIONS=55 FAIL=0' "$E/04_workflow_parity.log"
grep -Fxq 'PRODUCT_REGRESSION_ASSERTIONS=11 FAIL=0' "$E/04_product_regression.log"
grep -Fxq 'ASSERTIONS=14 FAIL=0' "$E/04_product_functional.log"

stage '5 GITHUB SCHEDULER TEMPLATE CONTRACT'
python3 - "$SCHED" <<'PY' | tee "$E/05_scheduler_contract.log"
from pathlib import Path
import sys
s=Path(sys.argv[1]).read_text()
checks={
'schedule_5min':"cron: '*/5 * * * *'" in s,
'five_ticks':'for n in 1 2 3 4 5' in s,
'sleep_60':'sleep 60' in s,
'post':'--request POST' in s,
'no_secret':'?key=' not in s and 'secrets.' not in s,
'correct_url':"https://pferde-atelier.de/wp-json/affiliate-zentrale/v1/ebay/tick" in s,
'concurrency':'cancel-in-progress: false' in s,
}
for k,v in checks.items(): print(('PASS ' if v else 'FAIL ')+k)
if not all(checks.values()): raise SystemExit(1)
print('SCHEDULER_CONTRACT_ASSERTIONS=7 FAIL=0')
PY

action_setup_wp(){
  local path="$1" version="$2" url="$3" log="$4"
  rm -rf "$path"; mkdir -p "$path"
  if [ -n "${WP_RESET_ROOT:-}" ]; then wp db reset --yes --path="$WP_RESET_ROOT" --allow-root >> "$log" 2>&1; fi
  wp core download --version="$version" --path="$path" --force --allow-root >> "$log" 2>&1
  wp config create --path="$path" --dbname=v655gate --dbuser=wp --dbpass=wppass --dbhost=127.0.0.1:3306 --skip-check --force --allow-root >> "$log" 2>&1
  wp core install --path="$path" --url="$url" --title=V655 --admin_user=admin --admin_password=pass --admin_email=a@example.invalid --skip-email --allow-root >> "$log" 2>&1
}

stage '6 REAL WORDPRESS 7.0.1 / PHP 8.4 / MARIADB 11.4 SOURCE + HTTP'
WP1=/tmp/v655-wp-source
action_setup_wp "$WP1" 7.0.1 http://127.0.0.1:8091 "$E/06_wp_setup.log"
rm -rf "$WP1/wp-content/plugins/affiliate-portal-router"; cp -a "$SRC" "$WP1/wp-content/plugins/affiliate-portal-router"
wp plugin activate affiliate-portal-router --path="$WP1" --allow-root >> "$E/06_wp_setup.log" 2>&1
wp eval-file "$REAL" --path="$WP1" --allow-root | tee "$E/06_real_public_heartbeat.log"
wp eval-file "$REAL_PRODUCT" --path="$WP1" --allow-root | tee "$E/06_real_product.log"
grep -Fq 'REAL_PUBLIC_HEARTBEAT_V655_ASSERTIONS=' "$E/06_real_public_heartbeat.log"; grep -Fq 'FAIL=0' "$E/06_real_public_heartbeat.log"
grep -Fxq 'REAL_ARTICLE_PRODUCT_V654=PASS' "$E/06_real_product.log"
wp option delete ppar_ebay_external_tick_rate_lock_v1 --path="$WP1" --allow-root >/dev/null 2>&1 || true
wp server --host=127.0.0.1 --port=8091 --path="$WP1" > "$E/06_wp_server.log" 2>&1 & SERVER_PID=$!
trap 'kill $SERVER_PID 2>/dev/null || true' EXIT
READY=0
for i in $(seq 1 30); do if curl -sS "http://127.0.0.1:8091/" >/dev/null 2>&1; then READY=1; break; fi; sleep 1; done
[ "$READY" = 1 ]
GET_STATUS=$(curl -sS -o "$E/06_http_get.json" -w '%{http_code}' "http://127.0.0.1:8091/wp-json/affiliate-zentrale/v1/ebay/tick")
[ "$GET_STATUS" = 404 ] || [ "$GET_STATUS" = 405 ]
POST1=$(curl -sS -o "$E/06_http_post1.json" -w '%{http_code}' --request POST "http://127.0.0.1:8091/wp-json/affiliate-zentrale/v1/ebay/tick")
[ "$POST1" = 200 ]
php -r '$d=json_decode(file_get_contents($argv[1]),true);if(!is_array($d)||!isset($d["status"])){exit(1);}echo "POST1_STATUS=".$d["status"]."\n";' "$E/06_http_post1.json" | tee "$E/06_http_post1_status.log"
POST2=$(curl -sS -o "$E/06_http_post2.json" -w '%{http_code}' --request POST "http://127.0.0.1:8091/wp-json/affiliate-zentrale/v1/ebay/tick")
[ "$POST2" = 200 ]
grep -Fq '"status":"throttled"' "$E/06_http_post2.json"
kill $SERVER_PID 2>/dev/null || true; wait $SERVER_PID 2>/dev/null || true; trap - EXIT
echo 'REAL_HTTP_PUBLIC_HEARTBEAT=PASS' | tee "$E/06_http_result.log"

stage '7 BUILD INSTALLER + FRESH PARITY'
( cd /tmp/v655-source && zip -qr "$INSTALL" affiliate-portal-router )
unzip -t "$INSTALL" > "$E/07_install_integrity.log"
sha256sum "$INSTALL" > "$E/07_install_sha256.txt"
mkdir -p /tmp/v655-fresh; unzip -q "$INSTALL" -d /tmp/v655-fresh
FRESH=/tmp/v655-fresh/affiliate-portal-router
( cd "$SRC" && find . -type f -print0 | sort -z | xargs -0 sha256sum ) > "$E/07_source_tree.sha"
( cd "$FRESH" && find . -type f -print0 | sort -z | xargs -0 sha256sum ) > "$E/07_fresh_tree.sha"
diff -u "$E/07_source_tree.sha" "$E/07_fresh_tree.sha" > "$E/07_source_vs_fresh.diff"
test ! -s "$E/07_source_vs_fresh.diff"

stage '8 COMPLETE FRESH-UNPACK WORKFLOW GATE'
find "$FRESH" -type f -name '*.php' -print0 | sort -z | xargs -0 -n1 php -l > "$E/08_php_lint.log"
PPAR_TEST_PLUGIN_DIR="$FRESH" php "$ARCH" | tee "$E/08_architecture.log"
PPAR_BASE_PLUGIN_DIR="$BASE" PPAR_TEST_PLUGIN_DIR="$FRESH" php "$PARITY" | tee "$E/08_workflow_parity.log"
PPAR_TEST_PLUGIN_DIR="$FRESH" php "$PRODUCT" | tee "$E/08_product_regression.log"
PPAR_TEST_PLUGIN_DIR="$FRESH" php "$PRODUCT_FUNC" | tee "$E/08_product_functional.log"
grep -Fxq 'ASSERTIONS=23 FAIL=0' "$E/08_architecture.log"
grep -Fxq 'PARITY_ASSERTIONS=55 FAIL=0' "$E/08_workflow_parity.log"
grep -Fxq 'PRODUCT_REGRESSION_ASSERTIONS=11 FAIL=0' "$E/08_product_regression.log"
grep -Fxq 'ASSERTIONS=14 FAIL=0' "$E/08_product_functional.log"

stage '9 REAL WORDPRESS 7.0.1 FROM FINAL INSTALLER'
WP2=/tmp/v655-wp-zip
WP_RESET_ROOT="$WP1" action_setup_wp "$WP2" 7.0.1 http://v655-zip.local "$E/09_wp_setup.log"
wp plugin install "$INSTALL" --activate --force --path="$WP2" --allow-root >> "$E/09_wp_setup.log" 2>&1
wp eval-file "$REAL" --path="$WP2" --allow-root | tee "$E/09_real_public_heartbeat.log"
wp eval-file "$REAL_PRODUCT" --path="$WP2" --allow-root | tee "$E/09_real_product.log"
grep -Fq 'FAIL=0' "$E/09_real_public_heartbeat.log"; grep -Fxq 'REAL_ARTICLE_PRODUCT_V654=PASS' "$E/09_real_product.log"

stage '10 WORDPRESS 6.8.3 COMPATIBILITY FROM FINAL INSTALLER'
WP3=/tmp/v655-wp-683
WP_RESET_ROOT="$WP2" action_setup_wp "$WP3" 6.8.3 http://v655-683.local "$E/10_wp_setup.log"
wp plugin install "$INSTALL" --activate --force --path="$WP3" --allow-root >> "$E/10_wp_setup.log" 2>&1
wp eval-file "$REAL" --path="$WP3" --allow-root | tee "$E/10_real_public_heartbeat.log"
wp eval-file "$REAL_PRODUCT" --path="$WP3" --allow-root | tee "$E/10_real_product.log"
grep -Fq 'FAIL=0' "$E/10_real_public_heartbeat.log"; grep -Fxq 'REAL_ARTICLE_PRODUCT_V654=PASS' "$E/10_real_product.log"

stage '11 BUILD MASTER + MANIFEST + FINAL PARITY'
MD=/tmp/master-v655/master-v655
mkdir -p "$MD"/{00_READ_ME_FIRST,01_MASTER_BINDING,02_INSTALL,03_SOURCE,04_TESTS_AND_REALGATE,05_REPORT,06_WORKLOG,07_ERROR_CATALOG,08_GITHUB,09_DIFF_AND_HASHES,10_SCHEDULER}
cp "$INSTALL" "$MD/02_INSTALL/"
cp -a "$SRC" "$MD/03_SOURCE/affiliate-portal-router"
cp -a "$E"/. "$MD/04_TESTS_AND_REALGATE/"
cp -a "$WORK/.github/v655/tests" "$MD/04_TESTS_AND_REALGATE/V655_TESTS"
cp /tmp/v655.patch "$MD/09_DIFF_AND_HASHES/01_kiss_public_heartbeat.patch"
cp "$E/03_scope.diff" "$MD/09_DIFF_AND_HASHES/02_production_scope.diff"
cp "$E/07_install_sha256.txt" "$MD/09_DIFF_AND_HASHES/03_installer_sha256.txt"
cp "$WORK/.github/v655/WORKLOG.md" "$MD/06_WORKLOG/ARBEITSPROTOKOLL_V6_55_0.md"
cp "$WORK/.github/v655/ERROR_CATALOG.md" "$MD/07_ERROR_CATALOG/FEHLERKATALOG_V6_55_0.md"
cp "$SCHED" "$MD/10_SCHEDULER/pferde-atelier-ebay-heartbeat.yml"
cat > "$MD/01_MASTER_BINDING/V654_BINDING_REFERENCE.txt" <<EOF
V6.54 Artifact ID: 9492368681
V6.54 Artifact SHA-256: 11f4b4665742bbc0dda1b75221bfa4c1c10c2a94612fd2a9edfb5cb7f11f1383
V6.54 Installer SHA-256: 2ac4b5453fc9076f2439853a3ba25fee45689b48d9655022efdf5d8c91c12a31
V6.54 MASTER SHA-256: 5cdcda55c2f868a99e0093d82bd76dcdee15c50fd8eb1686f0ec54e76df57877
Binding priority: MASTER > current source > proven GitHub history > chat > assumption
EOF
cat > "$MD/00_READ_ME_FIRST/INSTALLATION_FREIGEGEBEN.txt" <<'EOF'
V6.55.0 KISS PUBLIC HEARTBEAT + GITHUB SCHEDULER
No extra external cron account is required.
The heartbeat endpoint is POST-only, contains no shared secret and can only advance already-authorized canonical work.
A durable 45-second admission gate bounds repeated requests; Lease/CAS/checkpoint remain authoritative.
Candidate-local errors remain skippable/audited; global storage/checkpoint/runtime/invariant failures remain fail-closed.
The GitHub scheduler workflow is separately prepared for main but MUST NOT be merged without explicit user approval.
EXTERNAL_EBAY_PROVIDER_LIVE_E2E remains OPEN_NOT_CLAIMED until real Pferde Atelier execution.
EOF
cat > "$MD/05_REPORT/RELEASE_REPORT.md" <<EOF
# Release V6.55.0

- No new external cron account required.
- Public POST-only heartbeat URL with no shared secret and no operation/provider parameters.
- Durable 45-second rate admission before fach work.
- One accepted heartbeat = at most one canonical package.
- GitHub scheduler template: 5-minute schedule, five one-minute bounded POST ticks, concurrency protected.
- Terminal failed run never auto-restarts.
- Candidate-local errors remain durably audited/skipped; global failures remain hard.
- Production scope: exactly 4 Affiliate-Zentrale files; Designplugin 0.
- Pre-fix architecture counterproof: 23 assertions / 16 FAIL.
- Post-fix architecture: 23/23 PASS.
- Unchanged workflow function parity: 55/55 PASS.
- V6.54 product regression static: 11/11 PASS; functional 14/14 PASS.
- Real WordPress 7.0.1/PHP 8.4/MariaDB 11.4 + real HTTP POST/GET/throttle: PASS.
- Fresh-unpack parity + repeated complete tests: PASS.
- Real WordPress 7.0.1 final ZIP: PASS.
- WordPress 6.8.3 final ZIP: PASS.
- Source/Fresh/Master/Master-Installer parity: PASS.
- Scheduler merge to default branch remains an explicit operational approval step, not silently performed.
- EXTERNAL_EBAY_PROVIDER_LIVE_E2E=OPEN_NOT_CLAIMED.
EOF
cat > "$MD/08_GITHUB/GITHUB_RELEASE_GATE.md" <<EOF
Branch: ${GITHUB_HEAD_REF:-${GITHUB_REF_NAME:-unknown}}
Commit: ${GITHUB_SHA:-unknown}
Workflow run: ${GITHUB_RUN_ID:-unknown}
main was not modified or merged by this workflow.
EOF
( cd "$MD" && find . -type f ! -name MASTER_MANIFEST_SHA256.txt -print0 | sort -z | xargs -0 sha256sum ) > "$MD/MASTER_MANIFEST_SHA256.txt"
( cd "$MD" && sha256sum -c MASTER_MANIFEST_SHA256.txt ) > "$E/11_master_manifest_verify.log"
( cd /tmp/master-v655 && zip -qr "$MASTER" master-v655 )
unzip -t "$MASTER" > "$E/11_master_integrity.log"
sha256sum "$MASTER" > "$E/11_master_sha256.txt"
rm -rf /tmp/v655-master-check /tmp/v655-master-install; mkdir -p /tmp/v655-master-check /tmp/v655-master-install
unzip -q "$MASTER" -d /tmp/v655-master-check
unzip -q /tmp/v655-master-check/master-v655/02_INSTALL/$(basename "$INSTALL") -d /tmp/v655-master-install
( cd /tmp/v655-master-check/master-v655/03_SOURCE/affiliate-portal-router && find . -type f -print0 | sort -z | xargs -0 sha256sum ) > "$E/11_master_source_tree.sha"
( cd /tmp/v655-master-install/affiliate-portal-router && find . -type f -print0 | sort -z | xargs -0 sha256sum ) > "$E/11_master_installer_tree.sha"
diff -u "$E/07_source_tree.sha" "$E/11_master_source_tree.sha" > "$E/11_source_vs_master.diff"
diff -u "$E/07_source_tree.sha" "$E/11_master_installer_tree.sha" > "$E/11_source_vs_master_installer.diff"
test ! -s "$E/11_source_vs_master.diff"; test ! -s "$E/11_source_vs_master_installer.diff"

stage '12 AUTOMATIC FINAL RELEASE GATE'
cat > "$E/FINAL_DECISION.txt" <<EOF
FINAL_DECISION=AUTOMATIC_RELEASE_PIPELINE_FINAL_PASS
FINAL_RELEASE_GATE=PASS
VERSION=6.55.0
PRODUCTION_SCOPE_FILES=4
DESIGN_PLUGIN_CHANGED=0
PREFX_RED_ASSERTIONS=23
PREFX_RED_FAIL=16
POSTFIX_ARCH_ASSERTIONS=23
POSTFIX_ARCH_FAIL=0
UNTOUCHED_WORKFLOW_PARITY_ASSERTIONS=55
UNTOUCHED_WORKFLOW_PARITY_FAIL=0
SCHEDULER_CONTRACT_ASSERTIONS=7
SCHEDULER_CONTRACT_FAIL=0
PRODUCT_REGRESSION_STATIC=11_PASS
PRODUCT_REGRESSION_FUNCTIONAL=14_PASS
REAL_WP701_SOURCE_PUBLIC_HEARTBEAT=PASS
REAL_HTTP_PUBLIC_HEARTBEAT=PASS
FRESH_UNPACK_PARITY=PASS
REAL_WP701_FINAL_ZIP=PASS
REAL_WP683_FINAL_ZIP=PASS
SOURCE_FRESH_MASTER_PARITY=PASS
SCHEDULER_MAIN_MERGE=EXPLICIT_APPROVAL_REQUIRED_NOT_PERFORMED
EXTERNAL_EBAY_PROVIDER_LIVE_E2E=OPEN_NOT_CLAIMED
EOF
cat "$E/FINAL_DECISION.txt"
echo 'FINAL_RELEASE_GATE=PASS'
