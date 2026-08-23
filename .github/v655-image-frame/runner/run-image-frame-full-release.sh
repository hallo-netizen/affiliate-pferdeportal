#!/usr/bin/env bash
set -euo pipefail

REPO="hallo-netizen/affiliate-pferdeportal"
BASE_ARTIFACT_ID="9492650547"
BASE_ARTIFACT_SHA="5446bd14f3e0d035e8ed74da1cd86393574f890fce5d81eb77d2aea0b611a955"
BASE_INSTALLER="affiliate-zentrale_v6.55.0_KISS_PUBLIC_HEARTBEAT_GITHUB_SCHEDULER_REALGATE.zip"
BASE_INSTALLER_SHA="82a04a9f70ad11e62de002d337f4a3473892d9bd6f677382020ea5fd06e5e0ba"
BASE_MASTER="MASTER_AFFILIATE_ZENTRALE_V6_55_0_KISS_PUBLIC_HEARTBEAT_GITHUB_SCHEDULER_REALGATE_20260823.zip"
BASE_MASTER_SHA="e60ea2ec7a0e3438efb5c2a390b41b4b63cf280f16d60d45f4ca9456b0bacb56"
OUT_INSTALLER="affiliate-zentrale_v6.55.0_CATEGORY_PRODUCT_VISIBLE_IMAGE_SIZE_ONLY_REALGATE.zip"
OUT_MASTER="MASTER_AFFILIATE_ZENTRALE_V6_55_0_CATEGORY_PRODUCT_VISIBLE_IMAGE_SIZE_ONLY_REALGATE_20260823.zip"
EVIDENCE="V655_VISIBLE_IMAGE_SIZE_RELEASE_EVIDENCE"
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
cp "$WORK/artifact/V655_RELEASE_EVIDENCE/FINAL_DECISION.txt" "$EVIDENCE/01_v655_baseline_final_decision.txt"
printf '%s  %s\n' "$BASE_ARTIFACT_SHA" "V655_FINAL_VERIFIED_RELEASE.zip" > "$EVIDENCE/01_baseline_hashes.txt"
printf '%s  %s\n' "$BASE_INSTALLER_SHA" "$BASE_INSTALLER" >> "$EVIDENCE/01_baseline_hashes.txt"
printf '%s  %s\n' "$BASE_MASTER_SHA" "$BASE_MASTER" >> "$EVIDENCE/01_baseline_hashes.txt"
log "STAGE_01_PINNED_V655_BASELINE=PASS"

log "STAGE_02_PREFX_NEGATIVE_AND_PATCH=START"
mkdir -p "$WORK/before" "$WORK/after"
unzip -q "$WORK/artifact/$BASE_INSTALLER" -d "$WORK/before"
cp -a "$WORK/before/." "$WORK/after/"
CSS_BEFORE="$WORK/before/affiliate-portal-router/assets/frontend.css"
CSS_AFTER="$WORK/after/affiliate-portal-router/assets/frontend.css"
if grep -q 'V6.55 CSS-only: einheitliche sichtbare Bildgroesse' "$CSS_BEFORE"; then
  echo 'BLOCKED: pre-fix baseline already contains visible-image fix' >&2; exit 1
fi
echo 'PRE_FIX_RED=PASS' | tee "$EVIDENCE/02_pre_fix_negative.log"
python3 .github/v655-image-frame/patches/apply_category_product_image_frame.py "$CSS_AFTER" | tee "$EVIDENCE/02_patch_apply.log"
python3 .github/v655-image-frame/tests/test_category_product_image_frame.py "$CSS_BEFORE" "$CSS_AFTER" | tee "$EVIDENCE/02_visible_image_contract.log"
grep -q 'CATEGORY_PRODUCT_VISIBLE_IMAGE_SIZE_CONTRACT=PASS' "$EVIDENCE/02_visible_image_contract.log"
log "STAGE_02_PREFX_NEGATIVE_AND_PATCH=PASS"

log "STAGE_03_ONE_PRODUCTION_FILE_SCOPE=START"
(diff -qr "$WORK/before/affiliate-portal-router" "$WORK/after/affiliate-portal-router" || true) > "$EVIDENCE/03_production_scope.diff"
[ "$(grep -c '^Files .* differ$' "$EVIDENCE/03_production_scope.diff" || true)" -eq 1 ]
grep -q 'assets/frontend.css' "$EVIDENCE/03_production_scope.diff"
! grep -Ev 'assets/frontend.css|^$' "$EVIDENCE/03_production_scope.diff" | grep -q .
printf 'PRODUCTION_FILES_CHANGED=1\nONLY=affiliate-portal-router/assets/frontend.css\nDESIGNPLUGIN_CHANGED=0\nPHP_CHANGED=0\nEBAY_RUNTIME_CHANGED=0\nBANNER_SLOT_CHANGED=0\n' | tee "$EVIDENCE/03_scope_gate.log"
log "STAGE_03_ONE_PRODUCTION_FILE_SCOPE=PASS"

log "STAGE_04_FULL_STATIC_AND_SUCCESSOR_REGRESSION=START"
find "$WORK/after/affiliate-portal-router" -type f -name '*.php' -print0 | sort -z | xargs -0 -n1 php -l > "$EVIDENCE/04_php_lint.log"
python3 - "$WORK/after/affiliate-portal-router" <<'PY' | tee "$EVIDENCE/04_json.log"
from pathlib import Path
import json,sys
root=Path(sys.argv[1]); n=0
for p in root.rglob('*.json'):
    json.loads(p.read_text()); n+=1
print(f'JSON_FILES_VALID={n}')
PY
PPAR_TEST_PLUGIN_DIR="$WORK/after/affiliate-portal-router" php .github/v655/tests/test_kiss_public_heartbeat_architecture_v655.php | tee "$EVIDENCE/04_v655_architecture.log"
grep -q 'ASSERTIONS=23 FAIL=0' "$EVIDENCE/04_v655_architecture.log"
python3 - "$WORK/before/affiliate-portal-router" "$WORK/after/affiliate-portal-router" <<'PY' | tee "$EVIDENCE/04_non_css_parity.log"
from pathlib import Path
import hashlib,sys
b,a=map(Path,sys.argv[1:]); bad=[]; count=0
for p in sorted(b.rglob('*')):
    if not p.is_file(): continue
    rel=p.relative_to(b)
    if rel.as_posix()=='assets/frontend.css': continue
    q=a/rel
    if not q.is_file() or hashlib.sha256(p.read_bytes()).digest()!=hashlib.sha256(q.read_bytes()).digest(): bad.append(str(rel))
    count+=1
extra=[str(p.relative_to(a)) for p in a.rglob('*') if p.is_file() and not (b/p.relative_to(a)).exists()]
if bad or extra: raise SystemExit(f'NON_CSS_PARITY_FAIL bad={bad} extra={extra}')
print(f'NON_CSS_FILES_BYTE_IDENTICAL={count}')
print('NON_CSS_PARITY=PASS')
PY
log "STAGE_04_FULL_STATIC_AND_SUCCESSOR_REGRESSION=PASS"

log "STAGE_05_BUILD_AND_FRESH_UNPACK=START"
rm -f "$OUT_INSTALLER"
( cd "$WORK/after" && zip -X -qr "$GITHUB_WORKSPACE/$OUT_INSTALLER" affiliate-portal-router )
unzip -t "$OUT_INSTALLER" > "$EVIDENCE/05_installer_ziptest.log"
mkdir -p "$WORK/fresh"; unzip -q "$OUT_INSTALLER" -d "$WORK/fresh"
diff -qr "$WORK/after/affiliate-portal-router" "$WORK/fresh/affiliate-portal-router" > "$EVIDENCE/05_source_vs_fresh.diff"
python3 .github/v655-image-frame/tests/test_category_product_image_frame.py "$CSS_BEFORE" "$WORK/fresh/affiliate-portal-router/assets/frontend.css" | tee "$EVIDENCE/05_fresh_visible_image_contract.log"
grep -q 'CATEGORY_PRODUCT_VISIBLE_IMAGE_SIZE_CONTRACT=PASS' "$EVIDENCE/05_fresh_visible_image_contract.log"
PPAR_TEST_PLUGIN_DIR="$WORK/fresh/affiliate-portal-router" php .github/v655/tests/test_kiss_public_heartbeat_architecture_v655.php | tee "$EVIDENCE/05_fresh_v655_architecture.log"
grep -q 'ASSERTIONS=23 FAIL=0' "$EVIDENCE/05_fresh_v655_architecture.log"
sha "$OUT_INSTALLER" | tee "$EVIDENCE/05_installer_sha256.txt"
log "STAGE_05_BUILD_AND_FRESH_UNPACK=PASS"

setup_wp(){
  local version="$1" path="$2" prefix="$3" logprefix="$4"
  rm -rf "$path"; mkdir -p "$path"
  wp core download --version="$version" --path="$path" --force --quiet
  wp config create --path="$path" --dbname=v655imageframe --dbuser=wp --dbpass=wppass --dbhost=127.0.0.1:3306 --dbprefix="$prefix" --skip-check --force
  wp core install --path="$path" --url="http://imageframe-${prefix}.test" --title="Visible Image Size Gate" --admin_user=admin --admin_password='AdminPass-655!' --admin_email=test@example.com --skip-email
  wp plugin install "$GITHUB_WORKSPACE/$OUT_INSTALLER" --path="$path" --activate --force
  wp eval-file "$GITHUB_WORKSPACE/.github/v655/tests/real_article_product_v655.php" --path="$path" | tee "$EVIDENCE/${logprefix}_real_article_product.log"
  wp eval-file "$GITHUB_WORKSPACE/.github/v655/tests/real_public_heartbeat_v655.php" --path="$path" | tee "$EVIDENCE/${logprefix}_real_public_heartbeat.log"
  grep -q 'REAL_ARTICLE_PRODUCT_V655=PASS' "$EVIDENCE/${logprefix}_real_article_product.log"
  grep -q 'REAL_PUBLIC_HEARTBEAT_V655_ASSERTIONS=18 FAIL=0' "$EVIDENCE/${logprefix}_real_public_heartbeat.log"
}

log "STAGE_06_REAL_WORDPRESS_7_0_1=START"
setup_wp 7.0.1 "$WORK/wp701" wp7_ 06_wp701
log "STAGE_06_REAL_WORDPRESS_7_0_1=PASS"

log "STAGE_07_REAL_WORDPRESS_6_8_3=START"
setup_wp 6.8.3 "$WORK/wp683" wp68_ 07_wp683
log "STAGE_07_REAL_WORDPRESS_6_8_3=PASS"

log "STAGE_08_MASTER_AND_PARITY=START"
MASTER_ROOT="$WORK/master/master-v655-visible-image-size-only"
mkdir -p "$MASTER_ROOT"/{00_READ_ME_FIRST,01_MASTER_BINDING,02_INSTALL,03_SOURCE,04_TESTS_AND_REALGATE,05_REPORT,06_WORKLOG,07_ERROR_CATALOG,08_GITHUB,09_DIFF_AND_HASHES,10_PREDECESSOR_MASTER}
cat > "$MASTER_ROOT/00_READ_ME_FIRST/INSTALLATION_FREIGEGEBEN.txt" <<EOF
V6.55.0 CATEGORY PRODUCT VISIBLE IMAGE SIZE ONLY
Functional production delta: exactly one file, affiliate-portal-router/assets/frontend.css.
Exactly category_product_1/2/3 use one visible 150x150 px image area, centered, object-fit cover. This guarantees equal visible photo size without distortion; edge cropping is possible by definition of cover.
The banner slot product_after_category_tiles is untouched.
No PHP, eBay runtime, scheduler, provider, selection, content, card, button or design-plugin change.
Baseline: final verified V6.55 artifact SHA-256 $BASE_ARTIFACT_SHA.
EOF
cat > "$MASTER_ROOT/01_MASTER_BINDING/V655_FINAL_BASELINE_REFERENCE.txt" <<EOF
V655_FINAL_VERIFIED_RELEASE artifact id: $BASE_ARTIFACT_ID
artifact sha256: $BASE_ARTIFACT_SHA
installer sha256: $BASE_INSTALLER_SHA
master sha256: $BASE_MASTER_SHA
The baseline FINAL_RELEASE_GATE=PASS is preserved as predecessor evidence. This visible-image-size release changes only frontend.css and reruns scoped/full successor and real-WordPress gates.
EOF
cp "$OUT_INSTALLER" "$MASTER_ROOT/02_INSTALL/$OUT_INSTALLER"
cp -a "$WORK/after/affiliate-portal-router" "$MASTER_ROOT/03_SOURCE/affiliate-portal-router"
cp -a "$EVIDENCE/." "$MASTER_ROOT/04_TESTS_AND_REALGATE/"
cp .github/v655-image-frame/WORKLOG.md "$MASTER_ROOT/06_WORKLOG/ARBEITSPROTOKOLL_VISIBLE_IMAGE_SIZE_ONLY_20260823.md"
cp .github/v655-image-frame/ERROR_CATALOG.md "$MASTER_ROOT/07_ERROR_CATALOG/FEHLERKATALOG_VISIBLE_IMAGE_SIZE_ONLY_20260823.md"
cat > "$MASTER_ROOT/05_REPORT/RELEASE_REPORT.md" <<EOF
# Release report – V6.55.0 category product visible image size only

- Functional production delta: frontend.css only.
- Fixed slots: category_product_1, category_product_2, category_product_3 only.
- All three slots share the same CSS rule; no first-position special case.
- Visible image area: exactly 150x150 px; centered; object-fit cover; no distortion; edge cropping may occur.
- product_after_category_tiles banner slot untouched.
- Article product renderer untouched.
- Partner/banner slots untouched.
- HivePress PRIVATE remote image renderer untouched.
- PHP and eBay runtime byte-identical to final verified V6.55.
- WordPress 7.0.1 real gate PASS.
- WordPress 6.8.3 real gate PASS.
- Fresh-unpack parity PASS.
EOF
cat > "$MASTER_ROOT/08_GITHUB/BRANCH_AND_SCOPE.txt" <<EOF
work branch: v655-category-product-image-frame-only-20260823
PR: 15
main: not modified by this release workflow
production functional delta: affiliate-portal-router/assets/frontend.css only
EOF
diff -u "$CSS_BEFORE" "$CSS_AFTER" > "$MASTER_ROOT/09_DIFF_AND_HASHES/frontend_css_only.diff" || true
cp "$WORK/artifact/$BASE_MASTER" "$MASTER_ROOT/10_PREDECESSOR_MASTER/$BASE_MASTER"
printf '%s  %s\n' "$(sha "$OUT_INSTALLER")" "$OUT_INSTALLER" > "$MASTER_ROOT/09_DIFF_AND_HASHES/installer_sha256.txt"
( cd "$MASTER_ROOT" && find . -type f ! -name MASTER_MANIFEST_SHA256.txt -print0 | sort -z | xargs -0 sha256sum > MASTER_MANIFEST_SHA256.txt )
( cd "$MASTER_ROOT" && sha256sum -c MASTER_MANIFEST_SHA256.txt ) > "$EVIDENCE/08_master_manifest_verify.log"
rm -f "$OUT_MASTER"
( cd "$WORK/master" && zip -X -qr "$GITHUB_WORKSPACE/$OUT_MASTER" master-v655-visible-image-size-only )
unzip -t "$OUT_MASTER" > "$EVIDENCE/08_master_ziptest.log"
rm -rf "$WORK/mastercheck"; mkdir -p "$WORK/mastercheck"; unzip -q "$OUT_MASTER" -d "$WORK/mastercheck"
diff -qr "$WORK/after/affiliate-portal-router" "$WORK/mastercheck/master-v655-visible-image-size-only/03_SOURCE/affiliate-portal-router" > "$EVIDENCE/08_source_vs_master.diff"
rm -rf "$WORK/masterinstaller"; mkdir -p "$WORK/masterinstaller"; unzip -q "$WORK/mastercheck/master-v655-visible-image-size-only/02_INSTALL/$OUT_INSTALLER" -d "$WORK/masterinstaller"
diff -qr "$WORK/after/affiliate-portal-router" "$WORK/masterinstaller/affiliate-portal-router" > "$EVIDENCE/08_source_vs_master_installer.diff"
sha "$OUT_MASTER" | tee "$EVIDENCE/08_master_sha256.txt"
log "STAGE_08_MASTER_AND_PARITY=PASS"

log "STAGE_09_FINAL_COUNTERPROOF=START"
rm -rf "$WORK/finalcheck"; mkdir -p "$WORK/finalcheck"; unzip -q "$OUT_INSTALLER" -d "$WORK/finalcheck"
python3 .github/v655-image-frame/tests/test_category_product_image_frame.py "$CSS_BEFORE" "$WORK/finalcheck/affiliate-portal-router/assets/frontend.css" | tee "$EVIDENCE/09_final_visible_image_contract.log"
grep -q 'CATEGORY_PRODUCT_VISIBLE_IMAGE_SIZE_CONTRACT=PASS' "$EVIDENCE/09_final_visible_image_contract.log"
diff -qr "$WORK/after/affiliate-portal-router" "$WORK/finalcheck/affiliate-portal-router" > "$EVIDENCE/09_final_source_parity.diff"
printf 'FINAL_DECISION=AUTOMATIC_RELEASE_PIPELINE_FINAL_PASS\nFINAL_RELEASE_GATE=PASS\nPRODUCTION_DELTA=frontend.css_only\nVISIBLE_IMAGE_SIZE=150x150_cover\nCATEGORY_PRODUCT_SLOTS_ONLY=PASS\nFIRST_SLOT_SPECIAL_CASE=NONE\nBANNER_SLOT_CHANGED=0\nDESIGNPLUGIN_CHANGED=0\nPHP_CHANGED=0\nEBAY_RUNTIME_CHANGED=0\n' | tee "$EVIDENCE/FINAL_DECISION.txt"
log "STAGE_09_FINAL_COUNTERPROOF=PASS"
log "FINAL_RELEASE_GATE=PASS"
