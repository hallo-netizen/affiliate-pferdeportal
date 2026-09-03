#!/usr/bin/env bash
set -euo pipefail
WORK="${GITHUB_WORKSPACE:-$(pwd)}"
E="$WORK/V653_RELEASE_EVIDENCE"
BASE_RUNNER="$WORK/.github/v652/runner/run-v652-full-release-wrapper-v19.sh"
PATCH="$WORK/.github/v653/patches/01_article_product_portal_standard.patch"
ARCH_TEST="$WORK/.github/v653/tests/test_article_product_architecture_v653.php"
FUNC_TEST="$WORK/.github/v653/tests/test_article_product_portal_standard_v653.php"
REAL_PRODUCT_TEST="$WORK/.github/v653/tests/real_article_product_v653.php"
INSTALL="$WORK/affiliate-zentrale_v6.53.0_ARTICLE_PRODUCT_PORTAL_STANDARD_REALGATE.zip"
MASTER="$WORK/MASTER_AFFILIATE_ZENTRALE_V6_53_0_ARTICLE_PRODUCT_PORTAL_STANDARD_REALGATE_20260823.zip"
rm -rf "$E" /tmp/v653-base-master /tmp/v653-source /tmp/v653-fresh /tmp/v653-wp-source /tmp/v653-wp-zip /tmp/v653-real-gate
rm -f "$INSTALL" "$MASTER"
mkdir -p "$E"

stage(){ printf '\n===== %s =====\n' "$1" | tee -a "$E/STAGE_LOG.txt"; }

stage '1 BINDING + COMPLETE V6.52 PREDECESSOR RELEASE WORKFLOW FROM ZERO'
[ "$(git hash-object "$BASE_RUNNER")" = "66e92f190d65cc46ac0d0bd175506b3a9b8a2e3a" ] || { echo 'BLOCKED: V6.52 final runner blob drift'; exit 1; }
chmod +x "$BASE_RUNNER"
"$BASE_RUNNER" > "$E/01_v652_full_predecessor.log" 2>&1
cat "$E/01_v652_full_predecessor.log" | tail -80
V652_INSTALL="$WORK/affiliate-zentrale_v6.52.0_CORE_CRON_SELFPUMP_ROOTFIX_REALGATE.zip"
V652_MASTER="$WORK/MASTER_AFFILIATE_ZENTRALE_V6_52_0_CORE_CRON_SELFPUMP_ROOTFIX_REALGATE_20260822.zip"
test -f "$V652_INSTALL" -a -f "$V652_MASTER"
echo 'e8090b31c853031bbc65492845672d5e2ab1268452ac7c944e3459873a7684b2  '"$V652_INSTALL" | sha256sum -c -
echo '517b0939fe042ace8ab093efc86f754d340c80cb5ba543ff10d61b087fbc7778  '"$V652_MASTER" | sha256sum -c -
unzip -t "$V652_INSTALL" > "$E/01_v652_install_integrity.log"
unzip -t "$V652_MASTER" > "$E/01_v652_master_integrity.log"
unzip -q "$V652_MASTER" -d /tmp/v653-base-master
BASE=/tmp/v653-base-master/master-v652/03_SOURCE/affiliate-portal-router
test -f "$BASE/pferdeportal-affiliate-router.php"

stage '2 EXACT PRE-FIX RED COUNTERPROOF'
set +e
PPAR_TEST_PLUGIN_DIR="$BASE" PPAR_V653_FINAL=1 php "$ARCH_TEST" > "$E/02_prefx_red.log" 2>&1
red_rc=$?
set -e
cat "$E/02_prefx_red.log"
[ "$red_rc" -ne 0 ]
grep -Fxq 'ASSERTIONS=14 FAIL=11' "$E/02_prefx_red.log"

stage '3 APPLY ONE ATOMIC PRODUCT-PORTAL-STANDARD ROOTFIX'
mkdir -p /tmp/v653-source
cp -a "$BASE" /tmp/v653-source/affiliate-portal-router
( cd /tmp/v653-source && patch -p1 --dry-run --batch < "$PATCH" ) > "$E/03_patch_dryrun.log"
( cd /tmp/v653-source && patch -p1 --forward --batch < "$PATCH" ) > "$E/03_patch_apply.log"
SRC=/tmp/v653-source/affiliate-portal-router
diff -qr "$BASE" "$SRC" > "$E/03_scope.diff" || true
cat "$E/03_scope.diff"
python3 - "$E/03_scope.diff" <<'PY'
from pathlib import Path
import sys,re
lines=[x.strip() for x in Path(sys.argv[1]).read_text().splitlines() if x.strip()]
expected={'assets/frontend.css','includes/trait-ppar-article-plans.php','pferdeportal-affiliate-router.php','readme.txt'}
seen=set()
for line in lines:
    m=re.search(r'/affiliate-portal-router/(.+?) and ',line)
    if not m: raise SystemExit('BLOCKED unexpected scope line: '+line)
    seen.add(m.group(1))
if seen!=expected: raise SystemExit(f'BLOCKED production scope mismatch seen={sorted(seen)} expected={sorted(expected)}')
print('PRODUCTION_SCOPE=PASS files=4 design_plugin_changes=0')
PY
grep -Fq "const EBAY_RUNTIME_BUILD = '6.52.0-core-cron-selfpump-rootfix-20260822';" "$SRC/pferdeportal-affiliate-router.php"

stage '4 COMPLETE MODIFIED-SOURCE GATE'
find "$SRC" -type f -name '*.php' -print0 | sort -z | xargs -0 -n1 php -l > "$E/04_php_lint.log"
php -r '$files=array_slice($argv,1);foreach($files as $f){json_decode(file_get_contents($f),true);if(json_last_error()!==JSON_ERROR_NONE){fwrite(STDERR,"JSON_FAIL $f ".json_last_error_msg()."\n");exit(1);}echo "JSON_OK $f\n";}' "$SRC/assets/ebay-portal-catalog-v2.json" "$SRC/assets/portal-structure-v279.json" > "$E/04_json.log"
PPAR_TEST_PLUGIN_DIR="$SRC" PPAR_V653_FINAL=1 php "$ARCH_TEST" | tee "$E/04_architecture.log"
PPAR_TEST_PLUGIN_DIR="$SRC" php "$FUNC_TEST" | tee "$E/04_functional.log"
grep -Fxq 'ASSERTIONS=14 FAIL=0' "$E/04_architecture.log"
grep -Fxq 'ASSERTIONS=14 FAIL=0' "$E/04_functional.log"

run_successor_tree(){
  local root="$1" out="$2" src="$3"
  : > "$out"; local total=0 fail=0 assertions=0
  while IFS= read -r -d '' f; do
    total=$((total+1)); echo "===== ${f#$root/} =====" >> "$out"
    set +e
    PPAR_TEST_PLUGIN_DIR="$src" php "$f" >> "$out" 2>&1
    rc=$?
    set -e
    echo "__TEST_EXIT__ $rc" >> "$out"
    [ "$rc" -eq 0 ] || fail=$((fail+1))
  done < <(find "$root" -type f -name '*.php' -print0 | sort -z)
  assertions=$(grep -oE 'ASSERTIONS=[0-9]+' "$out" | cut -d= -f2 | awk '{s+=$1} END{print s+0}')
  echo "TOTAL=$total FAIL=$fail ASSERTIONS=$assertions" | tee -a "$out"
  [ "$fail" -eq 0 ]
}
TESTROOT=/tmp/v653-base-master/master-v652/04_TESTS_AND_REALGATE
run_successor_tree "$TESTROOT/STEP1" "$E/04_successor_step1.log" "$SRC"
run_successor_tree "$TESTROOT/FINAL_SOURCE" "$E/04_successor_final_source.log" "$SRC"
run_successor_tree "$TESTROOT/FINAL_ZIP_SOURCE" "$E/04_successor_final_zip_source.log" "$SRC"
grep -Fq 'TOTAL=20 FAIL=0' "$E/04_successor_step1.log"
grep -Fq 'TOTAL=20 FAIL=0' "$E/04_successor_final_source.log"
grep -Fq 'TOTAL=20 FAIL=0' "$E/04_successor_final_zip_source.log"

stage '5 REAL WORDPRESS 7.0.1 / PHP 8.4 / MARIADB 11.4 FULL A-H ON MODIFIED SOURCE'
WP1=/tmp/v653-wp-source
mkdir -p "$WP1"
wp core download --version=7.0.1 --path="$WP1" --force --allow-root > "$E/05_wp_setup.log" 2>&1
wp config create --path="$WP1" --dbname=v653gate --dbuser=wp --dbpass=wppass --dbhost=127.0.0.1:3306 --skip-check --force --allow-root >> "$E/05_wp_setup.log" 2>&1
wp db reset --yes --path="$WP1" --allow-root >> "$E/05_wp_setup.log" 2>&1 || true
wp core install --path="$WP1" --url=http://v653-source.local --title=V653 --admin_user=admin --admin_password=pass --admin_email=a@example.invalid --skip-email --allow-root >> "$E/05_wp_setup.log" 2>&1
rm -rf "$WP1/wp-content/plugins/affiliate-portal-router"
cp -a "$SRC" "$WP1/wp-content/plugins/affiliate-portal-router"
wp plugin activate affiliate-portal-router --path="$WP1" --allow-root >> "$E/05_wp_setup.log" 2>&1
rm -rf /tmp/v653-real-gate && cp -a "$TESTROOT/REAL_FINAL/V651_REAL_AH_ROOT" /tmp/v653-real-gate
python3 - <<'PY'
from pathlib import Path
p=Path('/tmp/v653-real-gate/03_REAL_GATE/verify_environment.php')
s=p.read_text().replace("Pferdeportal_Affiliate_Router::VERSION==='6.52.0'","Pferdeportal_Affiliate_Router::VERSION==='6.53.0'").replace('tested plugin version is 6.52.0','tested plugin version is 6.53.0')
p.write_text(s)
PY
WP_ROOT="$WP1" WP="$(command -v wp)" bash /tmp/v653-real-gate/07_RUNNERS/run_real_gate_from_existing_wordpress.sh > "$E/05_real_AH.log" 2>&1
cat "$E/05_real_AH.log" | tail -80
grep -Fxq 'REAL_GATE_COMPLETE' "$E/05_real_AH.log"
wp eval-file "$REAL_PRODUCT_TEST" --path="$WP1" --allow-root | tee "$E/05_real_product.log"
grep -Fxq 'REAL_ARTICLE_PRODUCT_V653=PASS' "$E/05_real_product.log"

stage '6 BUILD INSTALLER + FRESH-UNPACK PARITY'
( cd /tmp/v653-source && zip -qr "$INSTALL" affiliate-portal-router )
unzip -t "$INSTALL" > "$E/06_install_integrity.log"
sha256sum "$INSTALL" > "$E/06_install_sha256.txt"
mkdir -p /tmp/v653-fresh
unzip -q "$INSTALL" -d /tmp/v653-fresh
FRESH=/tmp/v653-fresh/affiliate-portal-router
( cd "$SRC" && find . -type f -print0 | sort -z | xargs -0 sha256sum ) > "$E/06_source_tree.sha"
( cd "$FRESH" && find . -type f -print0 | sort -z | xargs -0 sha256sum ) > "$E/06_fresh_tree.sha"
diff -u "$E/06_source_tree.sha" "$E/06_fresh_tree.sha" > "$E/06_source_vs_fresh.diff"
test ! -s "$E/06_source_vs_fresh.diff"

stage '7 COMPLETE FRESH-INSTALL SOURCE/HISTORICAL GATE'
find "$FRESH" -type f -name '*.php' -print0 | sort -z | xargs -0 -n1 php -l > "$E/07_php_lint.log"
PPAR_TEST_PLUGIN_DIR="$FRESH" PPAR_V653_FINAL=1 php "$ARCH_TEST" | tee "$E/07_architecture.log"
PPAR_TEST_PLUGIN_DIR="$FRESH" php "$FUNC_TEST" | tee "$E/07_functional.log"
run_successor_tree "$TESTROOT/STEP1" "$E/07_successor_step1.log" "$FRESH"
run_successor_tree "$TESTROOT/FINAL_SOURCE" "$E/07_successor_final_source.log" "$FRESH"
run_successor_tree "$TESTROOT/FINAL_ZIP_SOURCE" "$E/07_successor_final_zip_source.log" "$FRESH"
grep -Fq 'TOTAL=20 FAIL=0' "$E/07_successor_step1.log"
grep -Fq 'TOTAL=20 FAIL=0' "$E/07_successor_final_source.log"
grep -Fq 'TOTAL=20 FAIL=0' "$E/07_successor_final_zip_source.log"

stage '8 REAL WORDPRESS 7.0.1 FULL A-H FROM FINAL ZIP'
wp db reset --yes --path="$WP1" --allow-root > "$E/08_db_reset.log" 2>&1
WP2=/tmp/v653-wp-zip
mkdir -p "$WP2"
wp core download --version=7.0.1 --path="$WP2" --force --allow-root > "$E/08_wp_setup.log" 2>&1
wp config create --path="$WP2" --dbname=v653gate --dbuser=wp --dbpass=wppass --dbhost=127.0.0.1:3306 --skip-check --force --allow-root >> "$E/08_wp_setup.log" 2>&1
wp core install --path="$WP2" --url=http://v653-zip.local --title=V653ZIP --admin_user=admin --admin_password=pass --admin_email=a@example.invalid --skip-email --allow-root >> "$E/08_wp_setup.log" 2>&1
wp plugin install "$INSTALL" --activate --force --path="$WP2" --allow-root >> "$E/08_wp_setup.log" 2>&1
rm -rf /tmp/v653-real-gate-zip && cp -a /tmp/v653-real-gate /tmp/v653-real-gate-zip
WP_ROOT="$WP2" WP="$(command -v wp)" bash /tmp/v653-real-gate-zip/07_RUNNERS/run_real_gate_from_existing_wordpress.sh > "$E/08_real_AH.log" 2>&1
cat "$E/08_real_AH.log" | tail -80
grep -Fxq 'REAL_GATE_COMPLETE' "$E/08_real_AH.log"
wp eval-file "$REAL_PRODUCT_TEST" --path="$WP2" --allow-root | tee "$E/08_real_product.log"
grep -Fxq 'REAL_ARTICLE_PRODUCT_V653=PASS' "$E/08_real_product.log"

stage '9 WORDPRESS 6.8.3 COMPATIBILITY + REAL PRODUCT RENDER'
wp db reset --yes --path="$WP2" --allow-root > "$E/09_db_reset.log" 2>&1
WP3=/tmp/v653-wp-683
rm -rf "$WP3"; mkdir -p "$WP3"
wp core download --version=6.8.3 --path="$WP3" --force --allow-root > "$E/09_wp_setup.log" 2>&1
wp config create --path="$WP3" --dbname=v653gate --dbuser=wp --dbpass=wppass --dbhost=127.0.0.1:3306 --skip-check --force --allow-root >> "$E/09_wp_setup.log" 2>&1
wp core install --path="$WP3" --url=http://v653-683.local --title=V653WP683 --admin_user=admin --admin_password=pass --admin_email=a@example.invalid --skip-email --allow-root >> "$E/09_wp_setup.log" 2>&1
wp plugin install "$INSTALL" --activate --force --path="$WP3" --allow-root >> "$E/09_wp_setup.log" 2>&1
wp eval-file "$REAL_PRODUCT_TEST" --path="$WP3" --allow-root | tee "$E/09_real_product_683.log"
grep -Fxq 'REAL_ARTICLE_PRODUCT_V653=PASS' "$E/09_real_product_683.log"

stage '10 BUILD MASTER + MANIFEST + FINAL PARITY'
MASTERDIR=/tmp/master-v653/master-v653
rm -rf /tmp/master-v653; mkdir -p "$MASTERDIR"/{00_READ_ME_FIRST,01_MASTER_BINDING,02_INSTALL,03_SOURCE,04_TESTS_AND_REALGATE,05_REPORT,06_WORKLOG,07_ERROR_CATALOG,08_GITHUB,09_DIFF_AND_HASHES}
cp "$INSTALL" "$MASTERDIR/02_INSTALL/"
cp -a "$SRC" "$MASTERDIR/03_SOURCE/affiliate-portal-router"
cp -a "$E"/. "$MASTERDIR/04_TESTS_AND_REALGATE/"
cp "$PATCH" "$MASTERDIR/09_DIFF_AND_HASHES/01_article_product_portal_standard.patch"
cp "$E/03_scope.diff" "$MASTERDIR/09_DIFF_AND_HASHES/02_production_scope.diff"
cp "$E/06_install_sha256.txt" "$MASTERDIR/09_DIFF_AND_HASHES/03_installer_sha256.txt"
cp "$WORK/.github/v653/WORKLOG.md" "$MASTERDIR/06_WORKLOG/ARBEITSPROTOKOLL_V6_53_0.md"
cp "$WORK/.github/v653/ERROR_CATALOG.md" "$MASTERDIR/07_ERROR_CATALOG/FEHLERKATALOG_V6_53_0.md"
cat > "$MASTERDIR/01_MASTER_BINDING/V652_BINDING_REFERENCE.txt" <<EOF
V6.52 MASTER SHA-256: 517b0939fe042ace8ab093efc86f754d340c80cb5ba543ff10d61b087fbc7778
V6.52 Installer SHA-256: e8090b31c853031bbc65492845672d5e2ab1268452ac7c944e3459873a7684b2
Binding priority: MASTER > current source > proven GitHub history > chat > assumption
EOF
cat > "$MASTERDIR/00_READ_ME_FIRST/INSTALLATION_FREIGEGEBEN.txt" <<'EOF'
V6.53.0 ARTICLE PRODUCT PORTAL STANDARD
Scope: exclusively Affiliate-Zentrale article-bottom product rendering/markup/CSS + release metadata.
Design plugin: unchanged / outside production scope.
eBay runtime build: unchanged from V6.52; this design-only release does not invalidate or migrate an eBay run.
EOF
cat > "$MASTERDIR/05_REPORT/RELEASE_REPORT.md" <<EOF
# Release V6.53.0

- Root cause: article-bottom product recommendations reused generic banner markup/classes and therefore inherited banner geometry and global link-decoration behavior.
- Fix: dedicated .ppar-article-product-* markup and CSS contract; generic banner renderer removed from both article-product render paths.
- Production files changed: exactly 4 inside Affiliate-Zentrale.
- Design plugin changed: 0.
- eBay runtime build changed: 0.
- Pre-fix counterproof: 14 assertions / 11 FAIL.
- Post-fix architecture: 14/14 PASS.
- Post-fix functional markup: 14/14 PASS.
- V6.52 predecessor automatic full release workflow rerun from zero: PASS.
- Modified-source successor trees: 60 tests across STEP1/FINAL_SOURCE/FINAL_ZIP_SOURCE, all PASS.
- Real WordPress 7.0.1/PHP 8.4/MariaDB 11.4 A-H on modified source: PASS.
- Fresh-unpack successor trees: 60 tests, all PASS.
- Real WordPress 7.0.1 A-H from final installer ZIP: PASS.
- WordPress 6.8.3 real product renderer: PASS.
- Source/Fresh-Unpack parity: PASS.
EOF
cat > "$MASTERDIR/08_GITHUB/GITHUB_RELEASE_GATE.md" <<EOF
Branch: ${GITHUB_REF_NAME:-unknown}
Commit: ${GITHUB_SHA:-unknown}
Workflow run: ${GITHUB_RUN_ID:-unknown}
main was not modified or merged by this workflow.
EOF
( cd "$MASTERDIR" && find . -type f ! -name 'MASTER_MANIFEST_SHA256.txt' -print0 | sort -z | xargs -0 sha256sum ) > "$MASTERDIR/MASTER_MANIFEST_SHA256.txt"
( cd "$MASTERDIR" && sha256sum -c MASTER_MANIFEST_SHA256.txt ) > "$E/10_master_manifest_verify.log"
( cd /tmp/master-v653 && zip -qr "$MASTER" master-v653 )
unzip -t "$MASTER" > "$E/10_master_integrity.log"
sha256sum "$MASTER" > "$E/10_master_sha256.txt"
rm -rf /tmp/v653-master-check /tmp/v653-master-install
mkdir -p /tmp/v653-master-check /tmp/v653-master-install
unzip -q "$MASTER" -d /tmp/v653-master-check
unzip -q /tmp/v653-master-check/master-v653/02_INSTALL/$(basename "$INSTALL") -d /tmp/v653-master-install
( cd /tmp/v653-master-check/master-v653/03_SOURCE/affiliate-portal-router && find . -type f -print0 | sort -z | xargs -0 sha256sum ) > "$E/10_master_source_tree.sha"
( cd /tmp/v653-master-install/affiliate-portal-router && find . -type f -print0 | sort -z | xargs -0 sha256sum ) > "$E/10_master_installer_tree.sha"
diff -u "$E/06_source_tree.sha" "$E/10_master_source_tree.sha" > "$E/10_source_vs_master.diff"
diff -u "$E/06_source_tree.sha" "$E/10_master_installer_tree.sha" > "$E/10_source_vs_master_installer.diff"
test ! -s "$E/10_source_vs_master.diff" && test ! -s "$E/10_source_vs_master_installer.diff"

stage '11 AUTOMATIC FINAL RELEASE GATE'
cat > "$E/FINAL_DECISION.txt" <<EOF
FINAL_DECISION=AUTOMATIC_RELEASE_PIPELINE_FINAL_PASS
FINAL_RELEASE_GATE=PASS
VERSION=6.53.0
PRODUCTION_SCOPE_FILES=4
DESIGN_PLUGIN_CHANGED=0
EBAY_RUNTIME_BUILD_CHANGED=0
PREFX_RED_ASSERTIONS=14
PREFX_RED_FAIL=11
POSTFIX_ARCH_ASSERTIONS=14
POSTFIX_ARCH_FAIL=0
POSTFIX_FUNCTIONAL_ASSERTIONS=14
POSTFIX_FUNCTIONAL_FAIL=0
V652_FULL_PREDECESSOR_GATE=PASS
MODIFIED_SOURCE_SUCCESSOR_TESTS=60_PASS
MODIFIED_SOURCE_REAL_WP701_AH=PASS
FRESH_UNPACK_SUCCESSOR_TESTS=60_PASS
FRESH_INSTALL_REAL_WP701_AH=PASS
REAL_WP683_PRODUCT_RENDER=PASS
SOURCE_FRESH_MASTER_PARITY=PASS
EOF
cat "$E/FINAL_DECISION.txt"

echo 'FINAL_RELEASE_GATE=PASS'
