#!/usr/bin/env bash
set -euo pipefail
WORK="${GITHUB_WORKSPACE:-$(pwd)}"
E="$WORK/V654_RELEASE_EVIDENCE"
PATCHER="$WORK/.github/v654/patches/apply_v654_patch.py"
ARCH="$WORK/.github/v654/tests/test_kiss_external_tick_architecture_v654.php"
PARITY="$WORK/.github/v654/tests/test_v654_untouched_workflow_parity.php"
PRODUCT="$WORK/.github/v654/tests/test_article_product_regression_v654.php"
REAL="$WORK/.github/v654/tests/real_external_tick_v654.php"
REAL_PRODUCT="$WORK/.github/v654/tests/real_article_product_v654.php"
V653_FUNC="$WORK/.github/v653/tests/test_article_product_portal_standard_v653.php"
INSTALL="$WORK/affiliate-zentrale_v6.54.0_KISS_EXTERNAL_TICK_SKIP_REALGATE.zip"
MASTER="$WORK/MASTER_AFFILIATE_ZENTRALE_V6_54_0_KISS_EXTERNAL_TICK_SKIP_REALGATE_20260823.zip"
rm -rf "$E" /tmp/v654-* /tmp/master-v654
rm -f "$INSTALL" "$MASTER"
mkdir -p "$E"
stage(){ printf '\n===== %s =====\n' "$1" | tee -a "$E/STAGE_LOG.txt"; }

stage '1 IMMUTABLE V6.53 MASTER BINDING'
ART=/tmp/v654-v653-final.zip; ARTDIR=/tmp/v654-v653-artifact
mkdir -p "$ARTDIR"
command -v gh >/dev/null || { echo 'BLOCKED gh missing'; exit 1; }
gh api repos/hallo-netizen/affiliate-pferdeportal/actions/artifacts/9491717325/zip > "$ART"
echo '9fd5769b4de6278bad5f9cee1de0abbb54a15e8eb3cc8dc12b8ff2d30434d7c0  '"$ART" | sha256sum -c -
unzip -t "$ART" > "$E/01_v653_artifact_integrity.log"
unzip -q "$ART" -d "$ARTDIR"
V653_INSTALL="$ARTDIR/affiliate-zentrale_v6.53.0_ARTICLE_PRODUCT_PORTAL_STANDARD_REALGATE.zip"
V653_MASTER="$ARTDIR/MASTER_AFFILIATE_ZENTRALE_V6_53_0_ARTICLE_PRODUCT_PORTAL_STANDARD_REALGATE_20260823.zip"
echo '76fa167f806b7cd6bf7cef087f789a00da7da6ee24514afaaddf74feb42978c2  '"$V653_INSTALL" | sha256sum -c -
echo '82c4bb2affbc575443619269069dc2e8cd9f00f56151da070a4cae01cf8961e5  '"$V653_MASTER" | sha256sum -c -
grep -Fxq 'FINAL_RELEASE_GATE=PASS' "$ARTDIR/V653_RELEASE_EVIDENCE/FINAL_DECISION.txt"
unzip -q "$V653_MASTER" -d /tmp/v654-base-master
BASE=/tmp/v654-base-master/master-v653/03_SOURCE/affiliate-portal-router
test -f "$BASE/pferdeportal-affiliate-router.php"
grep -Fq "const VERSION = '6.53.0';" "$BASE/pferdeportal-affiliate-router.php"
cat > "$E/01_binding.txt" <<EOF
V653_ARTIFACT_ID=9491717325
V653_ARTIFACT_SHA256=9fd5769b4de6278bad5f9cee1de0abbb54a15e8eb3cc8dc12b8ff2d30434d7c0
V653_INSTALLER_SHA256=76fa167f806b7cd6bf7cef087f789a00da7da6ee24514afaaddf74feb42978c2
V653_MASTER_SHA256=82c4bb2affbc575443619269069dc2e8cd9f00f56151da070a4cae01cf8961e5
V653_FINAL_RELEASE_GATE=PASS
EOF

stage '2 PRE-FIX RED + V6.53 PRODUCT BASELINE'
set +e
PPAR_TEST_PLUGIN_DIR="$BASE" php "$ARCH" > "$E/02_prefx_red.log" 2>&1
red=$?
set -e
cat "$E/02_prefx_red.log"
[ "$red" -ne 0 ]
grep -Fxq 'ASSERTIONS=31 FAIL=28' "$E/02_prefx_red.log"
PPAR_TEST_PLUGIN_DIR="$BASE" php "$PRODUCT" | tee "$E/02_product_baseline.log"
PPAR_TEST_PLUGIN_DIR="$BASE" php "$V653_FUNC" | tee "$E/02_product_functional_baseline.log"
grep -Fxq 'PRODUCT_REGRESSION_ASSERTIONS=11 FAIL=0' "$E/02_product_baseline.log"
grep -Fxq 'ASSERTIONS=14 FAIL=0' "$E/02_product_functional_baseline.log"

stage '3 APPLY ONE ATOMIC V6.54 KISS ROOTFIX + SCOPE'
mkdir -p /tmp/v654-source
cp -a "$BASE" /tmp/v654-source/affiliate-portal-router
python3 "$PATCHER" /tmp/v654.patch | tee "$E/03_patch_decode.log"
echo '9c4bad55218afbbfa34d5ceaf6bab78f646624ae2040cd908a6056991b45f917  /tmp/v654.patch' | sha256sum -c -
( cd /tmp/v654-source && patch -p1 --dry-run --batch < /tmp/v654.patch ) > "$E/03_patch_dryrun.log"
( cd /tmp/v654-source && patch -p1 --batch < /tmp/v654.patch ) > "$E/03_patch_apply.log"
SRC=/tmp/v654-source/affiliate-portal-router
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
PPAR_TEST_PLUGIN_DIR="$SRC" php "$V653_FUNC" | tee "$E/04_product_functional.log"
grep -Fxq 'ASSERTIONS=31 FAIL=0' "$E/04_architecture.log"
grep -Fxq 'PARITY_ASSERTIONS=55 FAIL=0' "$E/04_workflow_parity.log"
grep -Fxq 'PRODUCT_REGRESSION_ASSERTIONS=11 FAIL=0' "$E/04_product_regression.log"
grep -Fxq 'ASSERTIONS=14 FAIL=0' "$E/04_product_functional.log"

setup_wp(){
  local path="$1" version="$2" url="$3" log="$4"
  rm -rf "$path"; mkdir -p "$path"
  if [ -n "${WP_RESET_ROOT:-}" ]; then wp db reset --yes --path="$WP_RESET_ROOT" --allow-root >> "$log" 2>&1; fi
  wp core download --version="$version" --path="$path" --force --allow-root >> "$log" 2>&1
  wp config create --path="$path" --dbname=v654gate --dbuser=wp --dbpass=wppass --dbhost=127.0.0.1:3306 --skip-check --force --allow-root >> "$log" 2>&1
  wp core install --path="$path" --url="$url" --title=V654 --admin_user=admin --admin_password=pass --admin_email=a@example.invalid --skip-email --allow-root >> "$log" 2>&1
}

stage '5 REAL WORDPRESS 7.0.1 / PHP 8.4 / MARIADB 11.4 SOURCE + HTTP'
WP1=/tmp/v654-wp-source
setup_wp "$WP1" 7.0.1 http://127.0.0.1:8089 "$E/05_wp_setup.log"
rm -rf "$WP1/wp-content/plugins/affiliate-portal-router"; cp -a "$SRC" "$WP1/wp-content/plugins/affiliate-portal-router"
wp plugin activate affiliate-portal-router --path="$WP1" --allow-root >> "$E/05_wp_setup.log" 2>&1
wp eval-file "$REAL" --path="$WP1" --allow-root | tee "$E/05_real_external_tick.log"
wp eval-file "$REAL_PRODUCT" --path="$WP1" --allow-root | tee "$E/05_real_product.log"
grep -Fq 'REAL_EXTERNAL_TICK_V654_ASSERTIONS=' "$E/05_real_external_tick.log"; grep -Fq 'FAIL=0' "$E/05_real_external_tick.log"
grep -Fxq 'REAL_ARTICLE_PRODUCT_V654=PASS' "$E/05_real_product.log"
KEY=$(wp option get ppar_ebay_external_tick_key_v1 --path="$WP1" --allow-root)
wp server --host=127.0.0.1 --port=8089 --path="$WP1" > "$E/05_wp_server.log" 2>&1 & SERVER_PID=$!
trap 'kill $SERVER_PID 2>/dev/null || true' EXIT
for i in $(seq 1 30); do curl -sS "http://127.0.0.1:8089/" >/dev/null 2>&1 && break; sleep 1; done
BAD_STATUS=$(curl -sS -o "$E/05_http_bad.json" -w '%{http_code}' "http://127.0.0.1:8089/?rest_route=/affiliate-zentrale/v1/ebay/tick&key=wrong")
[ "$BAD_STATUS" = 403 ]
curl -fsS "http://127.0.0.1:8089/?rest_route=/affiliate-zentrale/v1/ebay/tick&key=$KEY" > "$E/05_http_good.json"
grep -Fq '"status":"idle"' "$E/05_http_good.json"
kill $SERVER_PID 2>/dev/null || true; wait $SERVER_PID 2>/dev/null || true; trap - EXIT
echo 'REAL_HTTP_EXTERNAL_TICK=PASS' | tee "$E/05_http_result.log"

stage '6 BUILD INSTALLER + FRESH PARITY'
( cd /tmp/v654-source && zip -qr "$INSTALL" affiliate-portal-router )
unzip -t "$INSTALL" > "$E/06_install_integrity.log"
sha256sum "$INSTALL" > "$E/06_install_sha256.txt"
mkdir -p /tmp/v654-fresh; unzip -q "$INSTALL" -d /tmp/v654-fresh
FRESH=/tmp/v654-fresh/affiliate-portal-router
( cd "$SRC" && find . -type f -print0 | sort -z | xargs -0 sha256sum ) > "$E/06_source_tree.sha"
( cd "$FRESH" && find . -type f -print0 | sort -z | xargs -0 sha256sum ) > "$E/06_fresh_tree.sha"
diff -u "$E/06_source_tree.sha" "$E/06_fresh_tree.sha" > "$E/06_source_vs_fresh.diff"
test ! -s "$E/06_source_vs_fresh.diff"

stage '7 COMPLETE FRESH-UNPACK WORKFLOW GATE'
find "$FRESH" -type f -name '*.php' -print0 | sort -z | xargs -0 -n1 php -l > "$E/07_php_lint.log"
PPAR_TEST_PLUGIN_DIR="$FRESH" php "$ARCH" | tee "$E/07_architecture.log"
PPAR_BASE_PLUGIN_DIR="$BASE" PPAR_TEST_PLUGIN_DIR="$FRESH" php "$PARITY" | tee "$E/07_workflow_parity.log"
PPAR_TEST_PLUGIN_DIR="$FRESH" php "$PRODUCT" | tee "$E/07_product_regression.log"
PPAR_TEST_PLUGIN_DIR="$FRESH" php "$V653_FUNC" | tee "$E/07_product_functional.log"
grep -Fxq 'ASSERTIONS=31 FAIL=0' "$E/07_architecture.log"
grep -Fxq 'PARITY_ASSERTIONS=55 FAIL=0' "$E/07_workflow_parity.log"
grep -Fxq 'PRODUCT_REGRESSION_ASSERTIONS=11 FAIL=0' "$E/07_product_regression.log"
grep -Fxq 'ASSERTIONS=14 FAIL=0' "$E/07_product_functional.log"

stage '8 REAL WORDPRESS 7.0.1 FROM FINAL INSTALLER'
WP2=/tmp/v654-wp-zip
WP_RESET_ROOT="$WP1" setup_wp "$WP2" 7.0.1 http://v654-zip.local "$E/08_wp_setup.log"
wp plugin install "$INSTALL" --activate --force --path="$WP2" --allow-root >> "$E/08_wp_setup.log" 2>&1
wp eval-file "$REAL" --path="$WP2" --allow-root | tee "$E/08_real_external_tick.log"
wp eval-file "$REAL_PRODUCT" --path="$WP2" --allow-root | tee "$E/08_real_product.log"
grep -Fq 'FAIL=0' "$E/08_real_external_tick.log"; grep -Fxq 'REAL_ARTICLE_PRODUCT_V654=PASS' "$E/08_real_product.log"

stage '9 WORDPRESS 6.8.3 COMPATIBILITY FROM FINAL INSTALLER'
WP3=/tmp/v654-wp-683
WP_RESET_ROOT="$WP2" setup_wp "$WP3" 6.8.3 http://v654-683.local "$E/09_wp_setup.log"
wp plugin install "$INSTALL" --activate --force --path="$WP3" --allow-root >> "$E/09_wp_setup.log" 2>&1
wp eval-file "$REAL" --path="$WP3" --allow-root | tee "$E/09_real_external_tick.log"
wp eval-file "$REAL_PRODUCT" --path="$WP3" --allow-root | tee "$E/09_real_product.log"
grep -Fq 'FAIL=0' "$E/09_real_external_tick.log"; grep -Fxq 'REAL_ARTICLE_PRODUCT_V654=PASS' "$E/09_real_product.log"

stage '10 BUILD MASTER + MANIFEST + FINAL PARITY'
MD=/tmp/master-v654/master-v654
mkdir -p "$MD"/{00_READ_ME_FIRST,01_MASTER_BINDING,02_INSTALL,03_SOURCE,04_TESTS_AND_REALGATE,05_REPORT,06_WORKLOG,07_ERROR_CATALOG,08_GITHUB,09_DIFF_AND_HASHES}
cp "$INSTALL" "$MD/02_INSTALL/"
cp -a "$SRC" "$MD/03_SOURCE/affiliate-portal-router"
cp -a "$E"/. "$MD/04_TESTS_AND_REALGATE/"
cp -a "$WORK/.github/v654/tests" "$MD/04_TESTS_AND_REALGATE/V654_TESTS"
cp /tmp/v654.patch "$MD/09_DIFF_AND_HASHES/01_kiss_external_tick_skip.patch"
cp "$E/03_scope.diff" "$MD/09_DIFF_AND_HASHES/02_production_scope.diff"
cp "$E/06_install_sha256.txt" "$MD/09_DIFF_AND_HASHES/03_installer_sha256.txt"
cp "$WORK/.github/v654/WORKLOG.md" "$MD/06_WORKLOG/ARBEITSPROTOKOLL_V6_54_0.md"
cp "$WORK/.github/v654/ERROR_CATALOG.md" "$MD/07_ERROR_CATALOG/FEHLERKATALOG_V6_54_0.md"
cat > "$MD/01_MASTER_BINDING/V653_BINDING_REFERENCE.txt" <<EOF
V6.53 Artifact ID: 9491717325
V6.53 Artifact SHA-256: 9fd5769b4de6278bad5f9cee1de0abbb54a15e8eb3cc8dc12b8ff2d30434d7c0
V6.53 Installer SHA-256: 76fa167f806b7cd6bf7cef087f789a00da7da6ee24514afaaddf74feb42978c2
V6.53 MASTER SHA-256: 82c4bb2affbc575443619269069dc2e8cd9f00f56151da070a4cae01cf8961e5
Binding priority: MASTER > current source > proven GitHub history > chat > assumption
EOF
cat > "$MD/00_READ_ME_FIRST/INSTALLATION_FREIGEGEBEN.txt" <<'EOF'
V6.54.0 KISS EXTERNAL TICK + SKIP
Canonical eBay fach work is advanced only by the authenticated external REST heartbeat, one bounded package per request.
Legacy eBay WP-Cron/self-pump transport is retired.
Candidate-local errors may be skipped/audited; global storage/checkpoint/runtime/invariant failures remain fail-closed.
Design plugin unchanged. V6.53 article-product rendering preserved.
EXTERNAL_EBAY_PROVIDER_LIVE_E2E remains OPEN_NOT_CLAIMED until the real Pferde Atelier provider run after installation.
EOF
cat > "$MD/05_REPORT/RELEASE_REPORT.md" <<EOF
# Release V6.54.0

- KISS transport: authenticated external REST tick, one canonical package/request.
- Host/browser/WP-Cron independence for canonical eBay continuation.
- Automatic due-cycle selection: 3h sync, otherwise hourly inventory refresh.
- Terminal failed run never auto-restarts.
- Candidate-local BUSINESS/PRIVATE errors are durably audited/skipped; global failures remain hard.
- Production scope: exactly 4 Affiliate-Zentrale files; Designplugin 0.
- Pre-fix architecture counterproof: 31 assertions / 28 FAIL.
- Post-fix architecture: 31/31 PASS.
- Unchanged workflow function parity: 55/55 PASS.
- V6.53 product regression static: 11/11 PASS; functional 14/14 PASS.
- Real WordPress 7.0.1/PHP 8.4/MariaDB 11.4 source + real HTTP REST: PASS.
- Fresh-unpack parity + repeated complete tests: PASS.
- Real WordPress 7.0.1 final ZIP: PASS.
- WordPress 6.8.3 final ZIP: PASS.
- Source/Fresh/Master/Master-Installer parity: PASS.
- EXTERNAL_EBAY_PROVIDER_LIVE_E2E=OPEN_NOT_CLAIMED.
EOF
cat > "$MD/08_GITHUB/GITHUB_RELEASE_GATE.md" <<EOF
Branch: ${GITHUB_HEAD_REF:-${GITHUB_REF_NAME:-unknown}}
Commit: ${GITHUB_SHA:-unknown}
Workflow run: ${GITHUB_RUN_ID:-unknown}
main was not modified or merged by this workflow.
EOF
( cd "$MD" && find . -type f ! -name MASTER_MANIFEST_SHA256.txt -print0 | sort -z | xargs -0 sha256sum ) > "$MD/MASTER_MANIFEST_SHA256.txt"
( cd "$MD" && sha256sum -c MASTER_MANIFEST_SHA256.txt ) > "$E/10_master_manifest_verify.log"
( cd /tmp/master-v654 && zip -qr "$MASTER" master-v654 )
unzip -t "$MASTER" > "$E/10_master_integrity.log"
sha256sum "$MASTER" > "$E/10_master_sha256.txt"
rm -rf /tmp/v654-master-check /tmp/v654-master-install; mkdir -p /tmp/v654-master-check /tmp/v654-master-install
unzip -q "$MASTER" -d /tmp/v654-master-check
unzip -q /tmp/v654-master-check/master-v654/02_INSTALL/$(basename "$INSTALL") -d /tmp/v654-master-install
( cd /tmp/v654-master-check/master-v654/03_SOURCE/affiliate-portal-router && find . -type f -print0 | sort -z | xargs -0 sha256sum ) > "$E/10_master_source_tree.sha"
( cd /tmp/v654-master-install/affiliate-portal-router && find . -type f -print0 | sort -z | xargs -0 sha256sum ) > "$E/10_master_installer_tree.sha"
diff -u "$E/06_source_tree.sha" "$E/10_master_source_tree.sha" > "$E/10_source_vs_master.diff"
diff -u "$E/06_source_tree.sha" "$E/10_master_installer_tree.sha" > "$E/10_source_vs_master_installer.diff"
test ! -s "$E/10_source_vs_master.diff"; test ! -s "$E/10_source_vs_master_installer.diff"

stage '11 AUTOMATIC FINAL RELEASE GATE'
cat > "$E/FINAL_DECISION.txt" <<EOF
FINAL_DECISION=AUTOMATIC_RELEASE_PIPELINE_FINAL_PASS
FINAL_RELEASE_GATE=PASS
VERSION=6.54.0
PRODUCTION_SCOPE_FILES=4
DESIGN_PLUGIN_CHANGED=0
PREFX_RED_ASSERTIONS=31
PREFX_RED_FAIL=28
POSTFIX_ARCH_ASSERTIONS=31
POSTFIX_ARCH_FAIL=0
UNTOUCHED_WORKFLOW_PARITY_ASSERTIONS=55
UNTOUCHED_WORKFLOW_PARITY_FAIL=0
PRODUCT_REGRESSION_STATIC=11_PASS
PRODUCT_REGRESSION_FUNCTIONAL=14_PASS
REAL_WP701_SOURCE_EXTERNAL_TICK=PASS
REAL_HTTP_EXTERNAL_TICK=PASS
FRESH_UNPACK_PARITY=PASS
REAL_WP701_FINAL_ZIP=PASS
REAL_WP683_FINAL_ZIP=PASS
SOURCE_FRESH_MASTER_PARITY=PASS
EXTERNAL_EBAY_PROVIDER_LIVE_E2E=OPEN_NOT_CLAIMED
EOF
cat "$E/FINAL_DECISION.txt"
echo 'FINAL_RELEASE_GATE=PASS'
