#!/usr/bin/env bash
set -euo pipefail

REPO="hallo-netizen/affiliate-pferdeportal"
BASE_ARTIFACT_ID="9492650547"
BASE_ARTIFACT_SHA="5446bd14f3e0d035e8ed74da1cd86393574f890fce5d81eb77d2aea0b611a955"
BASE_INSTALLER="affiliate-zentrale_v6.55.0_KISS_PUBLIC_HEARTBEAT_GITHUB_SCHEDULER_REALGATE.zip"
BASE_INSTALLER_SHA="82a04a9f70ad11e62de002d337f4a3473892d9bd6f677382020ea5fd06e5e0ba"
BASE_MASTER="MASTER_AFFILIATE_ZENTRALE_V6_55_0_KISS_PUBLIC_HEARTBEAT_GITHUB_SCHEDULER_REALGATE_20260823.zip"
BASE_MASTER_SHA="e60ea2ec7a0e3438efb5c2a390b41b4b63cf280f16d60d45f4ca9456b0bacb56"
OUT_INSTALLER="affiliate-zentrale_v6.55.0_CATEGORY_PRODUCT_IMAGE_CACHE_ROOTFIX_REALGATE.zip"
OUT_MASTER="MASTER_AFFILIATE_ZENTRALE_V6_55_0_CATEGORY_PRODUCT_IMAGE_CACHE_ROOTFIX_REALGATE_20260823.zip"
EVIDENCE="V655_IMAGE_CACHE_ROOTFIX_EVIDENCE"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
mkdir -p "$EVIDENCE"
: > "$EVIDENCE/STAGE_LOG.txt"
log(){ printf '%s\n' "$*" | tee -a "$EVIDENCE/STAGE_LOG.txt"; }
sha(){ sha256sum "$1" | awk '{print $1}'; }

log "STAGE_01_PINNED_V655_BASELINE=START"
ART="$WORK/V655_FINAL_VERIFIED_RELEASE.zip"
gh api "repos/$REPO/actions/artifacts/$BASE_ARTIFACT_ID/zip" > "$ART"
[ "$(sha "$ART")" = "$BASE_ARTIFACT_SHA" ]
unzip -q "$ART" -d "$WORK/artifact"
[ "$(sha "$WORK/artifact/$BASE_INSTALLER")" = "$BASE_INSTALLER_SHA" ]
[ "$(sha "$WORK/artifact/$BASE_MASTER")" = "$BASE_MASTER_SHA" ]
grep -q 'FINAL_RELEASE_GATE=PASS' "$WORK/artifact/V655_RELEASE_EVIDENCE/FINAL_DECISION.txt"
printf '%s  %s\n' "$BASE_ARTIFACT_SHA" V655_FINAL_VERIFIED_RELEASE.zip > "$EVIDENCE/01_baseline_hashes.txt"
printf '%s  %s\n' "$BASE_INSTALLER_SHA" "$BASE_INSTALLER" >> "$EVIDENCE/01_baseline_hashes.txt"
printf '%s  %s\n' "$BASE_MASTER_SHA" "$BASE_MASTER" >> "$EVIDENCE/01_baseline_hashes.txt"
log "STAGE_01_PINNED_V655_BASELINE=PASS"

log "STAGE_02_LIVE_ROOTCAUSE_NEGATIVE_AND_PATCH=START"
mkdir -p "$WORK/before" "$WORK/after"
unzip -q "$WORK/artifact/$BASE_INSTALLER" -d "$WORK/before"
cp -a "$WORK/before/." "$WORK/after/"
CSS_BEFORE="$WORK/before/affiliate-portal-router/assets/frontend.css"
CSS_AFTER="$WORK/after/affiliate-portal-router/assets/frontend.css"
PHP_BEFORE="$WORK/before/affiliate-portal-router/pferdeportal-affiliate-router.php"
PHP_AFTER="$WORK/after/affiliate-portal-router/pferdeportal-affiliate-router.php"
grep -q "plugins_url('assets/frontend.css', __FILE__)" "$PHP_BEFORE"
python3 - "$PHP_BEFORE" <<'PY' | tee "$EVIDENCE/02_pre_fix_cache_negative.log"
from pathlib import Path
import sys
s=Path(sys.argv[1]).read_text()
anchor="""        wp_enqueue_style(\n            'ppar-frontend',\n            plugins_url('assets/frontend.css', __FILE__),\n            array(),\n            self::VERSION\n        );"""
if s.count(anchor)!=1: raise SystemExit('BLOCKED: expected static CSS cache key not found exactly once')
print('PRE_FIX_STATIC_CSS_CACHE_KEY=CONFIRMED')
PY
python3 .github/v655-image-cache-rootfix/patches/apply_image_cache_rootfix.py "$CSS_AFTER" "$PHP_AFTER" | tee "$EVIDENCE/02_patch_apply.log"
python3 .github/v655-image-cache-rootfix/tests/test_image_cache_rootfix.py "$CSS_BEFORE" "$CSS_AFTER" "$PHP_BEFORE" "$PHP_AFTER" | tee "$EVIDENCE/02_contract.log"
grep -q 'IMAGE_CACHE_ROOTFIX_CONTRACT=PASS' "$EVIDENCE/02_contract.log"
log "STAGE_02_LIVE_ROOTCAUSE_NEGATIVE_AND_PATCH=PASS"

log "STAGE_03_EXACT_TWO_FILE_PRODUCTION_SCOPE=START"
(diff -qr "$WORK/before/affiliate-portal-router" "$WORK/after/affiliate-portal-router" || true) > "$EVIDENCE/03_production_scope.diff"
[ "$(grep -c '^Files .* differ$' "$EVIDENCE/03_production_scope.diff" || true)" -eq 2 ]
grep -q 'assets/frontend.css' "$EVIDENCE/03_production_scope.diff"
grep -q 'pferdeportal-affiliate-router.php' "$EVIDENCE/03_production_scope.diff"
! grep '^Files .* differ$' "$EVIDENCE/03_production_scope.diff" | grep -Ev 'assets/frontend.css|pferdeportal-affiliate-router.php' | grep -q .
printf 'PRODUCTION_FILES_CHANGED=2\nFILE_1=affiliate-portal-router/assets/frontend.css\nFILE_2=affiliate-portal-router/pferdeportal-affiliate-router.php\nPHP_DELTA=CSS_CACHE_BUSTER_ONLY\nDESIGNPLUGIN_CHANGED=0\nEBAY_RUNTIME_CHANGED=0\nSCHEDULER_CHANGED=0\nBANNER_SLOT_CHANGED=0\n' | tee "$EVIDENCE/03_scope_gate.log"
log "STAGE_03_EXACT_TWO_FILE_PRODUCTION_SCOPE=PASS"

log "STAGE_04_STATIC_AND_REGRESSION=START"
find "$WORK/after/affiliate-portal-router" -type f -name '*.php' -print0 | sort -z | xargs -0 -n1 php -l > "$EVIDENCE/04_php_lint.log"
PPAR_TEST_PLUGIN_DIR="$WORK/after/affiliate-portal-router" php .github/v655/tests/test_kiss_public_heartbeat_architecture_v655.php | tee "$EVIDENCE/04_v655_architecture.log"
grep -q 'ASSERTIONS=23 FAIL=0' "$EVIDENCE/04_v655_architecture.log"
python3 - "$WORK/before/affiliate-portal-router" "$WORK/after/affiliate-portal-router" <<'PY' | tee "$EVIDENCE/04_other_files_parity.log"
from pathlib import Path
import hashlib,sys
b,a=map(Path,sys.argv[1:]); allowed={'assets/frontend.css','pferdeportal-affiliate-router.php'}; bad=[]; count=0
for p in sorted(b.rglob('*')):
    if not p.is_file(): continue
    rel=p.relative_to(b).as_posix()
    if rel in allowed: continue
    q=a/rel
    if not q.is_file() or hashlib.sha256(p.read_bytes()).digest()!=hashlib.sha256(q.read_bytes()).digest(): bad.append(rel)
    count+=1
extra=[p.relative_to(a).as_posix() for p in a.rglob('*') if p.is_file() and not (b/p.relative_to(a)).exists()]
if bad or extra: raise SystemExit(f'OTHER_FILE_PARITY_FAIL bad={bad} extra={extra}')
print(f'OTHER_PRODUCTION_FILES_BYTE_IDENTICAL={count}')
print('OTHER_FILE_PARITY=PASS')
PY
log "STAGE_04_STATIC_AND_REGRESSION=PASS"

log "STAGE_05_BUILD_AND_FRESH_UNPACK=START"
rm -f "$OUT_INSTALLER"
( cd "$WORK/after" && zip -X -qr "$GITHUB_WORKSPACE/$OUT_INSTALLER" affiliate-portal-router )
unzip -t "$OUT_INSTALLER" > "$EVIDENCE/05_installer_ziptest.log"
mkdir -p "$WORK/fresh"; unzip -q "$OUT_INSTALLER" -d "$WORK/fresh"
diff -qr "$WORK/after/affiliate-portal-router" "$WORK/fresh/affiliate-portal-router" > "$EVIDENCE/05_source_vs_fresh.diff"
python3 .github/v655-image-cache-rootfix/tests/test_image_cache_rootfix.py "$CSS_BEFORE" "$WORK/fresh/affiliate-portal-router/assets/frontend.css" "$PHP_BEFORE" "$WORK/fresh/affiliate-portal-router/pferdeportal-affiliate-router.php" | tee "$EVIDENCE/05_fresh_contract.log"
grep -q 'IMAGE_CACHE_ROOTFIX_CONTRACT=PASS' "$EVIDENCE/05_fresh_contract.log"
PPAR_TEST_PLUGIN_DIR="$WORK/fresh/affiliate-portal-router" php .github/v655/tests/test_kiss_public_heartbeat_architecture_v655.php | tee "$EVIDENCE/05_fresh_v655_architecture.log"
grep -q 'ASSERTIONS=23 FAIL=0' "$EVIDENCE/05_fresh_v655_architecture.log"
sha "$OUT_INSTALLER" | tee "$EVIDENCE/05_installer_sha256.txt"
log "STAGE_05_BUILD_AND_FRESH_UNPACK=PASS"

setup_wp(){
  local version="$1" path="$2" prefix="$3" logprefix="$4"
  rm -rf "$path"; mkdir -p "$path"
  wp core download --version="$version" --path="$path" --force --quiet
  wp config create --path="$path" --dbname=v655cachefix --dbuser=wp --dbpass=wppass --dbhost=127.0.0.1:3306 --dbprefix="$prefix" --skip-check --force
  wp core install --path="$path" --url="http://cachefix-${prefix}.test" --title="Image Cache Rootfix" --admin_user=admin --admin_password='AdminPass-655!' --admin_email=test@example.com --skip-email
  wp plugin install "$GITHUB_WORKSPACE/$OUT_INSTALLER" --path="$path" --activate --force
  wp eval-file "$GITHUB_WORKSPACE/.github/v655/tests/real_article_product_v655.php" --path="$path" | tee "$EVIDENCE/${logprefix}_real_article_product.log"
  wp eval-file "$GITHUB_WORKSPACE/.github/v655/tests/real_public_heartbeat_v655.php" --path="$path" | tee "$EVIDENCE/${logprefix}_real_public_heartbeat.log"
  grep -q 'REAL_ARTICLE_PRODUCT_V655=PASS' "$EVIDENCE/${logprefix}_real_article_product.log"
  grep -q 'REAL_PUBLIC_HEARTBEAT_V655_ASSERTIONS=18 FAIL=0' "$EVIDENCE/${logprefix}_real_public_heartbeat.log"
  wp eval '$css=WP_PLUGIN_DIR."/affiliate-portal-router/assets/frontend.css"; do_action("wp_enqueue_scripts"); $styles=wp_styles(); $actual=isset($styles->registered["ppar-frontend"])?(string)$styles->registered["ppar-frontend"]->ver:""; $expected=Pferdeportal_Affiliate_Router::VERSION."-".substr(hash_file("sha256",$css),0,12); echo "CSS_ASSET_VERSION_ACTUAL=$actual\nCSS_ASSET_VERSION_EXPECTED=$expected\n"; if($actual!==$expected){echo "CSS_ASSET_CACHE_BUSTER=FAIL\n"; exit(1);} echo "CSS_ASSET_CACHE_BUSTER=PASS\n";' --path="$path" | tee "$EVIDENCE/${logprefix}_css_cache_buster.log"
  grep -q 'CSS_ASSET_CACHE_BUSTER=PASS' "$EVIDENCE/${logprefix}_css_cache_buster.log"
}

log "STAGE_06_REAL_WORDPRESS_7_0_1=START"
setup_wp 7.0.1 "$WORK/wp701" wp7_ 06_wp701
log "STAGE_06_REAL_WORDPRESS_7_0_1=PASS"

log "STAGE_07_REAL_WORDPRESS_6_8_3=START"
setup_wp 6.8.3 "$WORK/wp683" wp68_ 07_wp683
log "STAGE_07_REAL_WORDPRESS_6_8_3=PASS"

log "STAGE_08_MASTER_AND_PARITY=START"
MASTER_ROOT="$WORK/master/master-v655-image-cache-rootfix"
mkdir -p "$MASTER_ROOT"/{00_READ_ME_FIRST,01_MASTER_BINDING,02_INSTALL,03_SOURCE,04_TESTS_AND_REALGATE,05_REPORT,06_WORKLOG,07_ERROR_CATALOG,08_GITHUB,09_DIFF_AND_HASHES,10_PREDECESSOR_MASTER}
cat > "$MASTER_ROOT/00_READ_ME_FIRST/INSTALLATION_FREIGEGEBEN.txt" <<EOF
V6.55.0 CATEGORY PRODUCT IMAGE CACHE ROOTFIX
Production delta exactly two files: frontend.css plus the CSS enqueue block in pferdeportal-affiliate-router.php.
The three category product images are fixed to 150x150 cover; the CSS asset version includes the CSS SHA-256 prefix so changed CSS cannot retain the old cache key.
No other PHP behavior, eBay runtime, scheduler, provider, product selection, text, card/button design, banner or design-plugin change.
EOF
cat > "$MASTER_ROOT/01_MASTER_BINDING/V655_FINAL_BASELINE_REFERENCE.txt" <<EOF
V655_FINAL_VERIFIED_RELEASE artifact id: $BASE_ARTIFACT_ID
artifact sha256: $BASE_ARTIFACT_SHA
installer sha256: $BASE_INSTALLER_SHA
master sha256: $BASE_MASTER_SHA
EOF
cp "$OUT_INSTALLER" "$MASTER_ROOT/02_INSTALL/$OUT_INSTALLER"
cp -a "$WORK/after/affiliate-portal-router" "$MASTER_ROOT/03_SOURCE/affiliate-portal-router"
cp -a "$EVIDENCE/." "$MASTER_ROOT/04_TESTS_AND_REALGATE/"
cp .github/v655-image-cache-rootfix/WORKLOG.md "$MASTER_ROOT/06_WORKLOG/ARBEITSPROTOKOLL_IMAGE_CACHE_ROOTFIX_20260823.md"
cp .github/v655-image-cache-rootfix/ERROR_CATALOG.md "$MASTER_ROOT/07_ERROR_CATALOG/FEHLERKATALOG_IMAGE_CACHE_ROOTFIX_20260823.md"
cat > "$MASTER_ROOT/05_REPORT/RELEASE_REPORT.md" <<EOF
# Release report – V6.55 image cache rootfix ONLY

- Live screenshot disproved prior two image installers.
- Root cause: frontend.css cache key remained self::VERSION while plugin version stayed 6.55.0.
- Production delta exactly two files: assets/frontend.css and pferdeportal-affiliate-router.php.
- PHP delta only creates deterministic CSS content-hash asset version; JS enqueue unchanged.
- category_product_1/2/3 share identical 150x150 cover rule; no first-slot exception.
- Banner, article products, HivePress PRIVATE images, eBay runtime, scheduler, provider, selection and designplugin untouched.
- WordPress 7.0.1 and 6.8.3 real CSS asset cache-buster proof required PASS.
EOF
cat > "$MASTER_ROOT/08_GITHUB/BRANCH_AND_SCOPE.txt" <<EOF
work branch: v655-category-product-image-cache-rootfix-20260823
main: unchanged
production files changed: exactly 2
EOF
diff -u "$CSS_BEFORE" "$CSS_AFTER" > "$MASTER_ROOT/09_DIFF_AND_HASHES/frontend_css.diff" || true
diff -u "$PHP_BEFORE" "$PHP_AFTER" > "$MASTER_ROOT/09_DIFF_AND_HASHES/css_enqueue_php.diff" || true
cp "$WORK/artifact/$BASE_MASTER" "$MASTER_ROOT/10_PREDECESSOR_MASTER/$BASE_MASTER"
printf '%s  %s\n' "$(sha "$OUT_INSTALLER")" "$OUT_INSTALLER" > "$MASTER_ROOT/09_DIFF_AND_HASHES/installer_sha256.txt"
( cd "$MASTER_ROOT" && find . -type f ! -name MASTER_MANIFEST_SHA256.txt -print0 | sort -z | xargs -0 sha256sum > MASTER_MANIFEST_SHA256.txt )
( cd "$MASTER_ROOT" && sha256sum -c MASTER_MANIFEST_SHA256.txt ) > "$EVIDENCE/08_master_manifest_verify.log"
rm -f "$OUT_MASTER"
( cd "$WORK/master" && zip -X -qr "$GITHUB_WORKSPACE/$OUT_MASTER" master-v655-image-cache-rootfix )
unzip -t "$OUT_MASTER" > "$EVIDENCE/08_master_ziptest.log"
rm -rf "$WORK/mastercheck"; mkdir -p "$WORK/mastercheck"; unzip -q "$OUT_MASTER" -d "$WORK/mastercheck"
diff -qr "$WORK/after/affiliate-portal-router" "$WORK/mastercheck/master-v655-image-cache-rootfix/03_SOURCE/affiliate-portal-router" > "$EVIDENCE/08_source_vs_master.diff"
rm -rf "$WORK/masterinstaller"; mkdir -p "$WORK/masterinstaller"; unzip -q "$WORK/mastercheck/master-v655-image-cache-rootfix/02_INSTALL/$OUT_INSTALLER" -d "$WORK/masterinstaller"
diff -qr "$WORK/after/affiliate-portal-router" "$WORK/masterinstaller/affiliate-portal-router" > "$EVIDENCE/08_source_vs_master_installer.diff"
sha "$OUT_MASTER" | tee "$EVIDENCE/08_master_sha256.txt"
log "STAGE_08_MASTER_AND_PARITY=PASS"

log "STAGE_09_FINAL_COUNTERPROOF=START"
rm -rf "$WORK/finalcheck"; mkdir -p "$WORK/finalcheck"; unzip -q "$OUT_INSTALLER" -d "$WORK/finalcheck"
python3 .github/v655-image-cache-rootfix/tests/test_image_cache_rootfix.py "$CSS_BEFORE" "$WORK/finalcheck/affiliate-portal-router/assets/frontend.css" "$PHP_BEFORE" "$WORK/finalcheck/affiliate-portal-router/pferdeportal-affiliate-router.php" | tee "$EVIDENCE/09_final_contract.log"
grep -q 'IMAGE_CACHE_ROOTFIX_CONTRACT=PASS' "$EVIDENCE/09_final_contract.log"
diff -qr "$WORK/after/affiliate-portal-router" "$WORK/finalcheck/affiliate-portal-router" > "$EVIDENCE/09_final_source_parity.diff"
printf 'FINAL_DECISION=AUTOMATIC_RELEASE_PIPELINE_FINAL_PASS\nFINAL_RELEASE_GATE=PASS\nPRODUCTION_FILES_CHANGED=2\nCSS_GEOMETRY_ROOTFIX=PASS\nCSS_CONTENT_HASH_CACHE_BUSTER=PASS\nCATEGORY_PRODUCT_SLOTS_ONLY=PASS\nFIRST_SLOT_SPECIAL_CASE=NONE\nDESIGNPLUGIN_CHANGED=0\nEBAY_RUNTIME_CHANGED=0\nSCHEDULER_CHANGED=0\n' | tee "$EVIDENCE/FINAL_DECISION.txt"
log "STAGE_09_FINAL_COUNTERPROOF=PASS"
log "FINAL_RELEASE_GATE=PASS"
