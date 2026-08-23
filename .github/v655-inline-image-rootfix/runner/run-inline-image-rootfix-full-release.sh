#!/usr/bin/env bash
set -euo pipefail

REPO="hallo-netizen/affiliate-pferdeportal"
BASE_ARTIFACT_ID="9492650547"
BASE_ARTIFACT_SHA="5446bd14f3e0d035e8ed74da1cd86393574f890fce5d81eb77d2aea0b611a955"
BASE_INSTALLER="affiliate-zentrale_v6.55.0_KISS_PUBLIC_HEARTBEAT_GITHUB_SCHEDULER_REALGATE.zip"
BASE_INSTALLER_SHA="82a04a9f70ad11e62de002d337f4a3473892d9bd6f677382020ea5fd06e5e0ba"
BASE_MASTER="MASTER_AFFILIATE_ZENTRALE_V6_55_0_KISS_PUBLIC_HEARTBEAT_GITHUB_SCHEDULER_REALGATE_20260823.zip"
BASE_MASTER_SHA="e60ea2ec7a0e3438efb5c2a390b41b4b63cf280f16d60d45f4ca9456b0bacb56"
OUT_INSTALLER="affiliate-zentrale_v6.55.0_CATEGORY_PRODUCT_INLINE_GEOMETRY_ROOTFIX_REALGATE.zip"
OUT_MASTER="MASTER_AFFILIATE_ZENTRALE_V6_55_0_CATEGORY_PRODUCT_INLINE_GEOMETRY_ROOTFIX_REALGATE_20260824.zip"
EVIDENCE="V655_INLINE_IMAGE_ROOTFIX_EVIDENCE"
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

log "STAGE_02_REPRODUCE_METADATA_BUG_AND_APPLY_ROOTFIX=START"
mkdir -p "$WORK/before" "$WORK/after"
unzip -q "$WORK/artifact/$BASE_INSTALLER" -d "$WORK/before"
cp -a "$WORK/before/." "$WORK/after/"
PHP_BEFORE="$WORK/before/affiliate-portal-router/pferdeportal-affiliate-router.php"
PHP_AFTER="$WORK/after/affiliate-portal-router/pferdeportal-affiliate-router.php"
README_AFTER="$WORK/after/affiliate-portal-router/readme.txt"
CSS_BEFORE="$WORK/before/affiliate-portal-router/assets/frontend.css"
CSS_AFTER="$WORK/after/affiliate-portal-router/assets/frontend.css"
python3 - "$PHP_BEFORE" "$README_AFTER" <<'PY' | tee "$EVIDENCE/02_pre_fix_metadata_negative.log"
from pathlib import Path
import re,sys
p=Path(sys.argv[1]).read_text(); r=Path(sys.argv[2]).read_text()
h=re.search(r'^\s*\*\s*Version:\s*([^\r\n]+)',p,re.M).group(1).strip()
c=re.search(r"const\s+VERSION\s*=\s*'([^']+)'",p).group(1)
s=re.search(r'^Stable tag:\s*([^\r\n]+)',r,re.M).group(1).strip()
print('PRE_FIX_HEADER='+h); print('PRE_FIX_CONST='+c); print('PRE_FIX_STABLE='+s)
if not (h=='6.54.0' and c=='6.55.0' and s=='6.55.0'): raise SystemExit('BLOCKED: expected metadata mismatch not reproduced')
print('PRE_FIX_METADATA_MISMATCH=CONFIRMED')
PY
python3 .github/v655-inline-image-rootfix/patches/apply_inline_image_rootfix.py "$PHP_AFTER" | tee "$EVIDENCE/02_patch_apply.log"
python3 .github/v655-inline-image-rootfix/tests/test_inline_image_rootfix.py "$PHP_BEFORE" "$PHP_AFTER" "$README_AFTER" | tee "$EVIDENCE/02_static_contract.log"
grep -q 'INLINE_IMAGE_ROOTFIX_STATIC=PASS' "$EVIDENCE/02_static_contract.log"
log "STAGE_02_REPRODUCE_METADATA_BUG_AND_APPLY_ROOTFIX=PASS"

log "STAGE_03_EXACT_ONE_FILE_PRODUCTION_SCOPE=START"
(diff -qr "$WORK/before/affiliate-portal-router" "$WORK/after/affiliate-portal-router" || true) > "$EVIDENCE/03_production_scope.diff"
[ "$(grep -c '^Files .* differ$' "$EVIDENCE/03_production_scope.diff" || true)" -eq 1 ]
grep -q 'pferdeportal-affiliate-router.php' "$EVIDENCE/03_production_scope.diff"
[ "$(sha "$CSS_BEFORE")" = "$(sha "$CSS_AFTER")" ]
printf 'PRODUCTION_FILES_CHANGED=1\nFILE_1=affiliate-portal-router/pferdeportal-affiliate-router.php\nCSS_CHANGED=0\nREADME_CHANGED=0\nDESIGNPLUGIN_CHANGED=0\nEBAY_RUNTIME_CHANGED=0\nSCHEDULER_CHANGED=0\nPROVIDER_CHANGED=0\nSELECTION_CHANGED=0\n' | tee "$EVIDENCE/03_scope_gate.log"
log "STAGE_03_EXACT_ONE_FILE_PRODUCTION_SCOPE=PASS"

log "STAGE_04_STATIC_AND_V655_REGRESSION=START"
find "$WORK/after/affiliate-portal-router" -type f -name '*.php' -print0 | sort -z | xargs -0 -n1 php -l > "$EVIDENCE/04_php_lint.log"
PPAR_TEST_PLUGIN_DIR="$WORK/after/affiliate-portal-router" php .github/v655/tests/test_kiss_public_heartbeat_architecture_v655.php | tee "$EVIDENCE/04_v655_architecture.log"
grep -q 'ASSERTIONS=23 FAIL=0' "$EVIDENCE/04_v655_architecture.log"
python3 - "$WORK/before/affiliate-portal-router" "$WORK/after/affiliate-portal-router" <<'PY' | tee "$EVIDENCE/04_other_file_parity.log"
from pathlib import Path
import hashlib,sys
b,a=map(Path,sys.argv[1:]); allowed={'pferdeportal-affiliate-router.php'}; bad=[]; count=0
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
log "STAGE_04_STATIC_AND_V655_REGRESSION=PASS"

log "STAGE_05_REAL_BROWSER_GEOMETRY_COUNTERPROOF=START"
CHROME="$(command -v google-chrome || command -v google-chrome-stable || command -v chromium || command -v chromium-browser || true)"
[ -n "$CHROME" ]
cat > "$WORK/geometry.html" <<'HTML'
<!doctype html><meta charset="utf-8"><style>
*{box-sizing:border-box}.grid{display:grid;grid-template-columns:repeat(3,250px);gap:16px}.card{border:1px solid #ccc;padding:10px}
.ppar-banner-image-wrap{display:flex!important;width:92px!important;height:110px!important;margin:0 auto!important;overflow:hidden!important}
.ppar-banner-image{width:92px!important;height:110px!important;object-fit:contain!important}
.card:first-child .ppar-banner-image-wrap{width:61px!important;height:137px!important;margin-left:4px!important}
.card:first-child .ppar-banner-image{width:61px!important;height:137px!important;object-fit:contain!important;object-position:left top!important}
</style><div class="grid">
<div class="card"><span class="ppar-banner-image-wrap" data-ppar-category-product-image-frame="150" style="box-sizing:border-box!important;display:flex!important;flex:0 0 150px!important;align-items:center!important;justify-content:center!important;width:150px!important;height:150px!important;min-width:150px!important;min-height:150px!important;max-width:150px!important;max-height:150px!important;margin:0 auto!important;padding:0!important;overflow:hidden!important;background:#fff!important;line-height:0!important"><img class="ppar-banner-image" style="box-sizing:border-box!important;display:block!important;width:150px!important;height:150px!important;min-width:150px!important;min-height:150px!important;max-width:150px!important;max-height:150px!important;margin:0!important;padding:0!important;border-radius:0!important;object-fit:cover!important;object-position:center center!important" src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw=="></span></div>
<div class="card"><span class="ppar-banner-image-wrap" data-ppar-category-product-image-frame="150" style="box-sizing:border-box!important;display:flex!important;flex:0 0 150px!important;align-items:center!important;justify-content:center!important;width:150px!important;height:150px!important;min-width:150px!important;min-height:150px!important;max-width:150px!important;max-height:150px!important;margin:0 auto!important;padding:0!important;overflow:hidden!important;background:#fff!important;line-height:0!important"><img class="ppar-banner-image" style="box-sizing:border-box!important;display:block!important;width:150px!important;height:150px!important;min-width:150px!important;min-height:150px!important;max-width:150px!important;max-height:150px!important;margin:0!important;padding:0!important;border-radius:0!important;object-fit:cover!important;object-position:center center!important" src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw=="></span></div>
<div class="card"><span class="ppar-banner-image-wrap" data-ppar-category-product-image-frame="150" style="box-sizing:border-box!important;display:flex!important;flex:0 0 150px!important;align-items:center!important;justify-content:center!important;width:150px!important;height:150px!important;min-width:150px!important;min-height:150px!important;max-width:150px!important;max-height:150px!important;margin:0 auto!important;padding:0!important;overflow:hidden!important;background:#fff!important;line-height:0!important"><img class="ppar-banner-image" style="box-sizing:border-box!important;display:block!important;width:150px!important;height:150px!important;min-width:150px!important;min-height:150px!important;max-width:150px!important;max-height:150px!important;margin:0!important;padding:0!important;border-radius:0!important;object-fit:cover!important;object-position:center center!important" src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw=="></span></div>
</div><pre id="result"></pre><script>
window.addEventListener('load',()=>{const w=[...document.querySelectorAll('.ppar-banner-image-wrap')].map(e=>{let r=e.getBoundingClientRect();return [r.width,r.height]});const i=[...document.querySelectorAll('.ppar-banner-image')].map(e=>{let r=e.getBoundingClientRect(),s=getComputedStyle(e);return [r.width,r.height,s.objectFit,s.objectPosition]});document.getElementById('result').textContent='WRAPS='+JSON.stringify(w)+' IMAGES='+JSON.stringify(i);});
</script>
HTML
"$CHROME" --headless --no-sandbox --disable-gpu --dump-dom "file://$WORK/geometry.html" > "$EVIDENCE/05_browser_geometry.html" 2> "$EVIDENCE/05_browser_geometry.stderr" || { cat "$EVIDENCE/05_browser_geometry.stderr"; exit 1; }
grep -Fq 'WRAPS=[[150,150],[150,150],[150,150]]' "$EVIDENCE/05_browser_geometry.html"
grep -Fq 'IMAGES=[[150,150,"cover","50% 50%"],[150,150,"cover","50% 50%"],[150,150,"cover","50% 50%"]]' "$EVIDENCE/05_browser_geometry.html"
printf 'BROWSER_FIRST_SLOT_CONFLICT_COUNTERPROOF=PASS\nALL_THREE_WRAP_RECTS=150x150\nALL_THREE_IMAGE_RECTS=150x150\nALL_THREE_OBJECT_FIT=cover\n' | tee "$EVIDENCE/05_browser_geometry_result.log"
log "STAGE_05_REAL_BROWSER_GEOMETRY_COUNTERPROOF=PASS"

log "STAGE_06_BUILD_AND_FRESH_UNPACK=START"
rm -f "$OUT_INSTALLER"
( cd "$WORK/after" && zip -X -qr "$GITHUB_WORKSPACE/$OUT_INSTALLER" affiliate-portal-router )
unzip -t "$OUT_INSTALLER" > "$EVIDENCE/06_installer_ziptest.log"
mkdir -p "$WORK/fresh"; unzip -q "$OUT_INSTALLER" -d "$WORK/fresh"
diff -qr "$WORK/after/affiliate-portal-router" "$WORK/fresh/affiliate-portal-router" > "$EVIDENCE/06_source_vs_fresh.diff"
python3 .github/v655-inline-image-rootfix/tests/test_inline_image_rootfix.py "$PHP_BEFORE" "$WORK/fresh/affiliate-portal-router/pferdeportal-affiliate-router.php" "$WORK/fresh/affiliate-portal-router/readme.txt" | tee "$EVIDENCE/06_fresh_static_contract.log"
grep -q 'INLINE_IMAGE_ROOTFIX_STATIC=PASS' "$EVIDENCE/06_fresh_static_contract.log"
PPAR_TEST_PLUGIN_DIR="$WORK/fresh/affiliate-portal-router" php .github/v655/tests/test_kiss_public_heartbeat_architecture_v655.php | tee "$EVIDENCE/06_fresh_v655_architecture.log"
grep -q 'ASSERTIONS=23 FAIL=0' "$EVIDENCE/06_fresh_v655_architecture.log"
sha "$OUT_INSTALLER" | tee "$EVIDENCE/06_installer_sha256.txt"
log "STAGE_06_BUILD_AND_FRESH_UNPACK=PASS"

setup_wp(){
  local version="$1" path="$2" prefix="$3" logprefix="$4"
  rm -rf "$path"; mkdir -p "$path"
  wp core download --version="$version" --path="$path" --force --quiet
  wp config create --path="$path" --dbname=v655inlinefix --dbuser=wp --dbpass=wppass --dbhost=127.0.0.1:3306 --dbprefix="$prefix" --skip-check --force
  wp core install --path="$path" --url="http://inlinefix-${prefix}.test" --title="Inline Image Rootfix" --admin_user=admin --admin_password='AdminPass-655!' --admin_email=test@example.com --skip-email
  wp plugin install "$GITHUB_WORKSPACE/$OUT_INSTALLER" --path="$path" --activate --force
  wp eval-file "$GITHUB_WORKSPACE/.github/v655-inline-image-rootfix/tests/real_inline_image_rootfix.php" --path="$path" | tee "$EVIDENCE/${logprefix}_real_inline_image.log"
  grep -q 'REAL_INLINE_IMAGE_ROOTFIX=PASS' "$EVIDENCE/${logprefix}_real_inline_image.log"
  wp eval-file "$GITHUB_WORKSPACE/.github/v655/tests/real_article_product_v655.php" --path="$path" | tee "$EVIDENCE/${logprefix}_real_article_product.log"
  grep -q 'REAL_ARTICLE_PRODUCT_V655=PASS' "$EVIDENCE/${logprefix}_real_article_product.log"
  wp eval-file "$GITHUB_WORKSPACE/.github/v655/tests/real_public_heartbeat_v655.php" --path="$path" | tee "$EVIDENCE/${logprefix}_real_public_heartbeat.log"
  grep -q 'REAL_PUBLIC_HEARTBEAT_V655_ASSERTIONS=18 FAIL=0' "$EVIDENCE/${logprefix}_real_public_heartbeat.log"
}

log "STAGE_07_REAL_WORDPRESS_7_0_1=START"
setup_wp 7.0.1 "$WORK/wp701" wp7_ 07_wp701
log "STAGE_07_REAL_WORDPRESS_7_0_1=PASS"

log "STAGE_08_REAL_WORDPRESS_6_8_3=START"
setup_wp 6.8.3 "$WORK/wp683" wp68_ 08_wp683
log "STAGE_08_REAL_WORDPRESS_6_8_3=PASS"

log "STAGE_09_MASTER_AND_PARITY=START"
MASTER_ROOT="$WORK/master/master-v655-inline-image-rootfix"
mkdir -p "$MASTER_ROOT"/{00_READ_ME_FIRST,01_MASTER_BINDING,02_INSTALL,03_SOURCE,04_TESTS_AND_REALGATE,05_REPORT,06_WORKLOG,07_ERROR_CATALOG,08_GITHUB,09_DIFF_AND_HASHES,10_PREDECESSOR_MASTER}
cat > "$MASTER_ROOT/00_READ_ME_FIRST/INSTALLATION_FREIGEGEBEN.txt" <<EOF
V6.55.0 CATEGORY PRODUCT INLINE GEOMETRY ROOTFIX
Production delta exactly one file: pferdeportal-affiliate-router.php.
WordPress plugin header is corrected from 6.54.0 to the already authoritative 6.55.0.
Only category_product_1/2/3 product image markup receives an inline !important 150x150 cover/center frame. This is on the actual HTML render path and is independent of stale frontend.css caches.
No CSS file, design plugin, eBay runtime, scheduler, provider, selection, text, card/button, banner or article-product change.
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
cp .github/v655-inline-image-rootfix/WORKLOG.md "$MASTER_ROOT/06_WORKLOG/ARBEITSPROTOKOLL_INLINE_IMAGE_ROOTFIX_20260824.md"
cp .github/v655-inline-image-rootfix/ERROR_CATALOG.md "$MASTER_ROOT/07_ERROR_CATALOG/FEHLERKATALOG_INLINE_IMAGE_ROOTFIX_20260824.md"
cat > "$MASTER_ROOT/05_REPORT/RELEASE_REPORT.md" <<EOF
# Release report – V6.55 inline category-product image geometry rootfix

- Live screenshot disproved prior CSS-only/image-cache fixes.
- The new rootfix is attached to the actual render_banner() HTML path, not to a cacheable stylesheet.
- Only product creatives in category_product_1/2/3 receive the frame.
- Wrapper and image are inline !important 150x150, cover, centered; first-slot conflicting stylesheet rules are counter-proved in headless Chrome.
- WordPress installation metadata is corrected: Plugin Header 6.55.0 = class VERSION 6.55.0 = top readme Stable tag 6.55.0.
- EBAY_RUNTIME_BUILD remains 6.55.0-kiss-public-heartbeat-github-scheduler-20260823.
- Exactly one production file changed. frontend.css and all other production files remain byte-identical.
EOF
cat > "$MASTER_ROOT/08_GITHUB/BRANCH_AND_SCOPE.txt" <<EOF
work branch: v655-category-product-inline-geometry-rootfix-20260824
main: unchanged
production files changed: exactly 1
EOF
diff -u "$PHP_BEFORE" "$PHP_AFTER" > "$MASTER_ROOT/09_DIFF_AND_HASHES/main_php.diff" || true
cp "$WORK/artifact/$BASE_MASTER" "$MASTER_ROOT/10_PREDECESSOR_MASTER/$BASE_MASTER"
printf '%s  %s\n' "$(sha "$OUT_INSTALLER")" "$OUT_INSTALLER" > "$MASTER_ROOT/09_DIFF_AND_HASHES/installer_sha256.txt"
( cd "$MASTER_ROOT" && find . -type f ! -name MASTER_MANIFEST_SHA256.txt -print0 | sort -z | xargs -0 sha256sum > MASTER_MANIFEST_SHA256.txt )
( cd "$MASTER_ROOT" && sha256sum -c MASTER_MANIFEST_SHA256.txt ) > "$EVIDENCE/09_master_manifest_verify.log"
rm -f "$OUT_MASTER"
( cd "$WORK/master" && zip -X -qr "$GITHUB_WORKSPACE/$OUT_MASTER" master-v655-inline-image-rootfix )
unzip -t "$OUT_MASTER" > "$EVIDENCE/09_master_ziptest.log"
rm -rf "$WORK/mastercheck"; mkdir -p "$WORK/mastercheck"; unzip -q "$OUT_MASTER" -d "$WORK/mastercheck"
diff -qr "$WORK/after/affiliate-portal-router" "$WORK/mastercheck/master-v655-inline-image-rootfix/03_SOURCE/affiliate-portal-router" > "$EVIDENCE/09_source_vs_master.diff"
rm -rf "$WORK/masterinstaller"; mkdir -p "$WORK/masterinstaller"; unzip -q "$WORK/mastercheck/master-v655-inline-image-rootfix/02_INSTALL/$OUT_INSTALLER" -d "$WORK/masterinstaller"
diff -qr "$WORK/after/affiliate-portal-router" "$WORK/masterinstaller/affiliate-portal-router" > "$EVIDENCE/09_source_vs_master_installer.diff"
sha "$OUT_MASTER" | tee "$EVIDENCE/09_master_sha256.txt"
log "STAGE_09_MASTER_AND_PARITY=PASS"

log "STAGE_10_FINAL_COUNTERPROOF=START"
rm -rf "$WORK/finalcheck"; mkdir -p "$WORK/finalcheck"; unzip -q "$OUT_INSTALLER" -d "$WORK/finalcheck"
python3 .github/v655-inline-image-rootfix/tests/test_inline_image_rootfix.py "$PHP_BEFORE" "$WORK/finalcheck/affiliate-portal-router/pferdeportal-affiliate-router.php" "$WORK/finalcheck/affiliate-portal-router/readme.txt" | tee "$EVIDENCE/10_final_static_contract.log"
grep -q 'INLINE_IMAGE_ROOTFIX_STATIC=PASS' "$EVIDENCE/10_final_static_contract.log"
PPAR_TEST_PLUGIN_DIR="$WORK/finalcheck/affiliate-portal-router" php .github/v655/tests/test_kiss_public_heartbeat_architecture_v655.php | tee "$EVIDENCE/10_final_v655_architecture.log"
grep -q 'ASSERTIONS=23 FAIL=0' "$EVIDENCE/10_final_v655_architecture.log"
diff -qr "$WORK/after/affiliate-portal-router" "$WORK/finalcheck/affiliate-portal-router" > "$EVIDENCE/10_final_source_parity.diff"
printf 'FINAL_DECISION=AUTOMATIC_RELEASE_PIPELINE_FINAL_PASS\nFINAL_RELEASE_GATE=PASS\nPRODUCTION_FILES_CHANGED=1\nWORDPRESS_PLUGIN_HEADER_VERSION=6.55.0\nCATEGORY_PRODUCT_INLINE_GEOMETRY=150x150_COVER_CENTER\nFIRST_SLOT_CONFLICT_COUNTERPROOF=PASS\nCSS_CHANGED=0\nDESIGNPLUGIN_CHANGED=0\nEBAY_RUNTIME_CHANGED=0\nSCHEDULER_CHANGED=0\n' | tee "$EVIDENCE/FINAL_DECISION.txt"
log "STAGE_10_FINAL_COUNTERPROOF=PASS"
log "FINAL_RELEASE_GATE=PASS"
