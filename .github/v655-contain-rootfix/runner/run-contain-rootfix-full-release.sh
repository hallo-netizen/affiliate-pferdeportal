#!/usr/bin/env bash
set -euo pipefail

REPO="hallo-netizen/affiliate-pferdeportal"
BASE_ARTIFACT_ID="9492650547"
BASE_ARTIFACT_SHA="5446bd14f3e0d035e8ed74da1cd86393574f890fce5d81eb77d2aea0b611a955"
BASE_INSTALLER="affiliate-zentrale_v6.55.0_KISS_PUBLIC_HEARTBEAT_GITHUB_SCHEDULER_REALGATE.zip"
BASE_INSTALLER_SHA="82a04a9f70ad11e62de002d337f4a3473892d9bd6f677382020ea5fd06e5e0ba"
BASE_MASTER="MASTER_AFFILIATE_ZENTRALE_V6_55_0_KISS_PUBLIC_HEARTBEAT_GITHUB_SCHEDULER_REALGATE_20260823.zip"
BASE_MASTER_SHA="e60ea2ec7a0e3438efb5c2a390b41b4b63cf280f16d60d45f4ca9456b0bacb56"
OUT_INSTALLER="affiliate-zentrale_v6.55.0_CATEGORY_PRODUCT_CONTAIN_ROOTFIX_REALGATE.zip"
OUT_MASTER="MASTER_AFFILIATE_ZENTRALE_V6_55_0_CATEGORY_PRODUCT_CONTAIN_ROOTFIX_REALGATE_20260824.zip"
EVIDENCE="V655_CONTAIN_ROOTFIX_EVIDENCE"
WORK="$(mktemp -d)"
HTTP_PID=""
cleanup(){ if [ -n "${HTTP_PID:-}" ]; then kill "$HTTP_PID" 2>/dev/null || true; fi; rm -rf "$WORK"; }
trap cleanup EXIT
mkdir -p "$EVIDENCE"; : > "$EVIDENCE/STAGE_LOG.txt"
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

log "STAGE_02_REPRODUCE_LIVE_FAILS_AND_PATCH=START"
mkdir -p "$WORK/before" "$WORK/after"
unzip -q "$WORK/artifact/$BASE_INSTALLER" -d "$WORK/before"
cp -a "$WORK/before/." "$WORK/after/"
PHP_BEFORE="$WORK/before/affiliate-portal-router/pferdeportal-affiliate-router.php"
PHP_AFTER="$WORK/after/affiliate-portal-router/pferdeportal-affiliate-router.php"
README_BEFORE="$WORK/before/affiliate-portal-router/readme.txt"
README_AFTER="$WORK/after/affiliate-portal-router/readme.txt"
CSS_BEFORE="$WORK/before/affiliate-portal-router/assets/frontend.css"
CSS_AFTER="$WORK/after/affiliate-portal-router/assets/frontend.css"
python3 - "$PHP_BEFORE" "$README_BEFORE" <<'PY' | tee "$EVIDENCE/02_pre_fix_negative.log"
from pathlib import Path
import re,sys
p=Path(sys.argv[1]).read_text(); r=Path(sys.argv[2]).read_text()
h=re.search(r'^\s*\*\s*Version:\s*([^\r\n]+)',p,re.M).group(1).strip()
c=re.search(r"const\s+VERSION\s*=\s*'([^']+)'",p).group(1)
st=re.findall(r'^Stable tag:\s*([^\r\n]+)',r,re.M)
print('PRE_HEADER='+h); print('PRE_CONST='+c); print('PRE_STABLE_TAGS='+repr(st))
if h!='6.54.0' or c!='6.55.0' or st!=['6.55.0','6.48.0']: raise SystemExit('BLOCKED: live metadata fail not reproduced')
print('PRE_METADATA_FAIL=CONFIRMED')
PY
python3 .github/v655-contain-rootfix/patches/apply_contain_rootfix.py "$PHP_AFTER" "$README_AFTER" | tee "$EVIDENCE/02_patch_apply.log"
python3 .github/v655-contain-rootfix/tests/test_contain_rootfix.py "$PHP_BEFORE" "$PHP_AFTER" "$README_AFTER" | tee "$EVIDENCE/02_static_contract.log"
grep -q 'CONTAIN_ROOTFIX_STATIC=PASS' "$EVIDENCE/02_static_contract.log"
log "STAGE_02_REPRODUCE_LIVE_FAILS_AND_PATCH=PASS"

log "STAGE_03_EXACT_SCOPE=START"
(diff -qr "$WORK/before/affiliate-portal-router" "$WORK/after/affiliate-portal-router" || true) > "$EVIDENCE/03_production_scope.diff"
[ "$(grep -c '^Files .* differ$' "$EVIDENCE/03_production_scope.diff" || true)" -eq 2 ]
grep -q 'pferdeportal-affiliate-router.php' "$EVIDENCE/03_production_scope.diff"
grep -q 'readme.txt' "$EVIDENCE/03_production_scope.diff"
[ "$(sha "$CSS_BEFORE")" = "$(sha "$CSS_AFTER")" ]
printf 'PRODUCTION_FILES_CHANGED=2\nFILE_1=affiliate-portal-router/pferdeportal-affiliate-router.php\nFILE_2=affiliate-portal-router/readme.txt\nFRONTEND_CSS_CHANGED=0\nDESIGNPLUGIN_CHANGED=0\nEBAY_RUNTIME_CHANGED=0\nSCHEDULER_CHANGED=0\nPROVIDER_CHANGED=0\nSELECTION_CHANGED=0\nARTICLE_PRODUCT_CHANGED=0\n' | tee "$EVIDENCE/03_scope_gate.log"
log "STAGE_03_EXACT_SCOPE=PASS"

log "STAGE_04_STATIC_AND_EXISTING_V655_WORKFLOW=START"
find "$WORK/after/affiliate-portal-router" -type f -name '*.php' -print0 | sort -z | xargs -0 -n1 php -l > "$EVIDENCE/04_php_lint.log"
PPAR_TEST_PLUGIN_DIR="$WORK/after/affiliate-portal-router" php .github/v655/tests/test_kiss_public_heartbeat_architecture_v655.php | tee "$EVIDENCE/04_v655_architecture.log"
grep -q 'ASSERTIONS=23 FAIL=0' "$EVIDENCE/04_v655_architecture.log"
python3 - "$WORK/before/affiliate-portal-router" "$WORK/after/affiliate-portal-router" <<'PY' | tee "$EVIDENCE/04_other_file_parity.log"
from pathlib import Path
import hashlib,sys
b,a=map(Path,sys.argv[1:]); allowed={'pferdeportal-affiliate-router.php','readme.txt'}; bad=[]; count=0
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
log "STAGE_04_STATIC_AND_EXISTING_V655_WORKFLOW=PASS"

log "STAGE_05_BUILD_AND_FRESH_UNPACK=START"
rm -f "$OUT_INSTALLER"
( cd "$WORK/after" && zip -X -qr "$GITHUB_WORKSPACE/$OUT_INSTALLER" affiliate-portal-router )
unzip -t "$OUT_INSTALLER" > "$EVIDENCE/05_installer_ziptest.log"
mkdir -p "$WORK/fresh"; unzip -q "$OUT_INSTALLER" -d "$WORK/fresh"
diff -qr "$WORK/after/affiliate-portal-router" "$WORK/fresh/affiliate-portal-router" > "$EVIDENCE/05_source_vs_fresh.diff"
python3 .github/v655-contain-rootfix/tests/test_contain_rootfix.py "$PHP_BEFORE" "$WORK/fresh/affiliate-portal-router/pferdeportal-affiliate-router.php" "$WORK/fresh/affiliate-portal-router/readme.txt" | tee "$EVIDENCE/05_fresh_static.log"
grep -q 'CONTAIN_ROOTFIX_STATIC=PASS' "$EVIDENCE/05_fresh_static.log"
PPAR_TEST_PLUGIN_DIR="$WORK/fresh/affiliate-portal-router" php .github/v655/tests/test_kiss_public_heartbeat_architecture_v655.php | tee "$EVIDENCE/05_fresh_architecture.log"
grep -q 'ASSERTIONS=23 FAIL=0' "$EVIDENCE/05_fresh_architecture.log"
sha "$OUT_INSTALLER" | tee "$EVIDENCE/05_installer_sha256.txt"
log "STAGE_05_BUILD_AND_FRESH_UNPACK=PASS"

setup_wp(){
  local version="$1" path="$2" prefix="$3" logprefix="$4"
  rm -rf "$path"; mkdir -p "$path"
  wp core download --version="$version" --path="$path" --force --quiet
  wp config create --path="$path" --dbname=v655contain --dbuser=wp --dbpass=wppass --dbhost=127.0.0.1:3306 --dbprefix="$prefix" --skip-check --force
  wp core install --path="$path" --url="http://contain-${prefix}.test" --title="Contain Rootfix" --admin_user=admin --admin_password='AdminPass-655!' --admin_email=test@example.com --skip-email
  wp plugin install "$GITHUB_WORKSPACE/$OUT_INSTALLER" --path="$path" --activate --force
  wp eval-file "$GITHUB_WORKSPACE/.github/v655-contain-rootfix/tests/real_contain_rootfix.php" --path="$path" | tee "$EVIDENCE/${logprefix}_real_contain.log"
  grep -q 'REAL_CONTAIN_ROOTFIX=PASS' "$EVIDENCE/${logprefix}_real_contain.log"
  wp eval-file "$GITHUB_WORKSPACE/.github/v655/tests/real_article_product_v655.php" --path="$path" | tee "$EVIDENCE/${logprefix}_real_article_product.log"
  grep -q 'REAL_ARTICLE_PRODUCT_V655=PASS' "$EVIDENCE/${logprefix}_real_article_product.log"
  wp eval-file "$GITHUB_WORKSPACE/.github/v655/tests/real_public_heartbeat_v655.php" --path="$path" | tee "$EVIDENCE/${logprefix}_real_public_heartbeat.log"
  grep -q 'REAL_PUBLIC_HEARTBEAT_V655_ASSERTIONS=18 FAIL=0' "$EVIDENCE/${logprefix}_real_public_heartbeat.log"
}

log "STAGE_06_REAL_WORDPRESS_7_0_1=START"
setup_wp 7.0.1 "$WORK/wp701" wp7_ 06_wp701
log "STAGE_06_REAL_WORDPRESS_7_0_1=PASS"

log "STAGE_07_REAL_WORDPRESS_6_8_3=START"
setup_wp 6.8.3 "$WORK/wp683" wp68_ 07_wp683
log "STAGE_07_REAL_WORDPRESS_6_8_3=PASS"

log "STAGE_08_ACTUAL_RENDER_PATH_VISUAL_NO_CROP=START"
mkdir -p "$WORK/visual-assets"
cat > "$WORK/visual-assets/landscape.svg" <<'SVG'
<svg xmlns="http://www.w3.org/2000/svg" width="300" height="200"><rect width="300" height="200" fill="#ffeb3b"/><rect x="4" y="4" width="292" height="192" fill="none" stroke="#ff0000" stroke-width="8"/></svg>
SVG
cat > "$WORK/visual-assets/portrait.svg" <<'SVG'
<svg xmlns="http://www.w3.org/2000/svg" width="200" height="300"><rect width="200" height="300" fill="#00bcd4"/><rect x="4" y="4" width="192" height="292" fill="none" stroke="#00aa00" stroke-width="8"/></svg>
SVG
cat > "$WORK/visual-assets/square.svg" <<'SVG'
<svg xmlns="http://www.w3.org/2000/svg" width="300" height="300"><rect width="300" height="300" fill="#00ffff"/><rect x="4" y="4" width="292" height="292" fill="none" stroke="#ff00ff" stroke-width="8"/></svg>
SVG
python3 -m http.server 8765 --bind 127.0.0.1 --directory "$WORK/visual-assets" > "$EVIDENCE/08_http_server.log" 2>&1 & HTTP_PID=$!
sleep 1
PPAR_VISUAL_BASE='http://127.0.0.1:8765' wp eval-file "$GITHUB_WORKSPACE/.github/v655-contain-rootfix/tests/emit_visual_fixture.php" --path="$WORK/wp701" > "$WORK/rendered_fragments.html"
grep -q 'data-ppar-category-product-image-fit="contain"' "$WORK/rendered_fragments.html"
[ "$(grep -o 'data-ppar-category-product-image-fit="contain"' "$WORK/rendered_fragments.html" | wc -l)" -eq 3 ]
cat > "$WORK/visual.html" <<'HTML'
<!doctype html><html><head><meta charset="utf-8"><style>
html,body{margin:0;padding:0;background:#fff}.visual-grid{display:grid;grid-template-columns:150px 150px 150px;gap:20px;width:490px}.visual-slot{box-sizing:border-box;width:150px;height:150px;overflow:hidden;background:#fff}.visual-slot>.ppar-banner-link{display:block!important;box-sizing:border-box!important;width:150px!important;height:150px!important;margin:0!important;padding:0!important;background:#fff!important}.ppar-banner-text{display:none!important}
/* Deliberately hostile legacy/global rules. The actual product render must still win identically in slot 1/2/3. */
.ppar-banner-image-wrap{display:flex!important;width:92px!important;height:110px!important;margin:0 auto!important;overflow:hidden!important}.ppar-banner-image{width:92px!important;height:110px!important;object-fit:cover!important;object-position:left top!important}.visual-slot:first-child .ppar-banner-image-wrap{width:61px!important;height:137px!important;margin-left:4px!important}.visual-slot:first-child .ppar-banner-image{width:61px!important;height:137px!important;object-fit:cover!important;object-position:left top!important}
</style></head><body><div class="visual-grid">
HTML
cat "$WORK/rendered_fragments.html" >> "$WORK/visual.html"
cat >> "$WORK/visual.html" <<'HTML'
</div><pre id="result"></pre><script>
window.addEventListener('load',()=>{const imgs=[...document.querySelectorAll('.visual-slot img')];const rows=imgs.map(img=>{const r=img.getBoundingClientRect(),s=getComputedStyle(img),w=img.naturalWidth,h=img.naturalHeight,scale=Math.min(r.width/w,r.height/h);return {rect:[r.width,r.height],fit:s.objectFit,pos:s.objectPosition,natural:[w,h],visible:[Math.round(w*scale),Math.round(h*scale)]}});const pass=JSON.stringify(rows.map(x=>x.rect))==='[[150,150],[150,150],[150,150]]'&&rows.every(x=>x.fit==='contain'&&x.pos==='50% 50%')&&JSON.stringify(rows.map(x=>x.natural))==='[[300,200],[200,300],[300,300]]'&&JSON.stringify(rows.map(x=>x.visible))==='[[150,100],[100,150],[150,150]]';document.body.setAttribute('data-visual-pass',pass?'1':'0');document.getElementById('result').textContent=JSON.stringify(rows);});
</script></body></html>
HTML
CHROME="$(command -v google-chrome || command -v google-chrome-stable || command -v chromium || command -v chromium-browser || true)"; [ -n "$CHROME" ]
timeout 35s "$CHROME" --headless --no-sandbox --disable-gpu --disable-dev-shm-usage --force-device-scale-factor=1 --window-size=600,300 --virtual-time-budget=3000 --dump-dom "file://$WORK/visual.html" > "$EVIDENCE/08_visual_dom.html" 2> "$EVIDENCE/08_visual_dom.stderr"
grep -q 'data-visual-pass="1"' "$EVIDENCE/08_visual_dom.html"
timeout 35s "$CHROME" --headless --no-sandbox --disable-gpu --disable-dev-shm-usage --force-device-scale-factor=1 --window-size=600,300 --virtual-time-budget=3000 --screenshot="$EVIDENCE/08_visual.png" "file://$WORK/visual.html" > "$EVIDENCE/08_visual_screenshot.stdout" 2> "$EVIDENCE/08_visual_screenshot.stderr"
python3 .github/v655-contain-rootfix/tests/verify_visual_png.py "$EVIDENCE/08_visual.png" | tee "$EVIDENCE/08_visual_pixel_check.log"
grep -q 'NO_CROP_VISUAL_COUNTERPROOF=PASS' "$EVIDENCE/08_visual_pixel_check.log"
printf 'ACTUAL_RENDER_PATH=PASS\nFIRST_SLOT_HOSTILE_CONFLICT=PASS\nLANDSCAPE_FULL_SOURCE_VISIBLE=PASS\nPORTRAIT_FULL_SOURCE_VISIBLE=PASS\nSQUARE_FULL_SOURCE_VISIBLE=PASS\nOBJECT_FIT_CONTAIN=PASS\n' | tee "$EVIDENCE/08_visual_result.log"
log "STAGE_08_ACTUAL_RENDER_PATH_VISUAL_NO_CROP=PASS"

log "STAGE_09_MASTER_AND_PARITY=START"
MASTER_ROOT="$WORK/master/master-v655-contain-rootfix"
mkdir -p "$MASTER_ROOT"/{00_READ_ME_FIRST,01_MASTER_BINDING,02_INSTALL,03_SOURCE,04_TESTS_AND_REALGATE,05_REPORT,06_WORKLOG,07_ERROR_CATALOG,08_GITHUB,09_DIFF_AND_HASHES,10_PREDECESSOR_MASTER}
cat > "$MASTER_ROOT/00_READ_ME_FIRST/INSTALLATION_FREIGEGEBEN.txt" <<EOF
V6.55.0 CATEGORY PRODUCT CONTAIN ROOTFIX
Only the live-proven category product image rendering and inconsistent version metadata are corrected.
category_product_1/2/3 product images: fixed 150x150 media element, object-fit contain, centered, full source image visible without crop.
WordPress plugin header, class VERSION and canonical Stable tag are 6.55.0; historical Stable tag is no longer declared as canonical metadata.
No frontend.css, designplugin, eBay runtime, scheduler, provider, selection, article-product, text, card or button change.
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
cp .github/v655-contain-rootfix/WORKLOG.md "$MASTER_ROOT/06_WORKLOG/ARBEITSPROTOKOLL_CONTAIN_ROOTFIX_20260824.md"
cp .github/v655-contain-rootfix/ERROR_CATALOG.md "$MASTER_ROOT/07_ERROR_CATALOG/FEHLERKATALOG_CONTAIN_ROOTFIX_20260824.md"
cat > "$MASTER_ROOT/05_REPORT/RELEASE_REPORT.md" <<EOF
# Release report – V6.55 category product contain rootfix

- Prior frame/cache/cover attempts are invalidated by live screenshots.
- Actual render path now marks only product creatives in category_product_1/2/3.
- Fixed 150x150 image element uses object-fit: contain and center; full source remains visible.
- Browser test uses actual WordPress render output, deliberately hostile first-slot CSS, three source aspect ratios and pixel-level edge/letterbox verification.
- WordPress plugin header corrected to 6.55.0; readme has exactly one canonical Stable tag, 6.55.0.
- Production delta exactly two files: pferdeportal-affiliate-router.php and readme.txt.
- frontend.css/designplugin/eBay runtime/scheduler/provider/selection/article-product/text/card/button unchanged.
EOF
cat > "$MASTER_ROOT/08_GITHUB/BRANCH_AND_SCOPE.txt" <<EOF
work branch: v655-category-product-contain-rootfix-20260824
main: unchanged
production files changed: exactly 2
EOF
diff -u "$PHP_BEFORE" "$PHP_AFTER" > "$MASTER_ROOT/09_DIFF_AND_HASHES/main_php.diff" || true
diff -u "$README_BEFORE" "$README_AFTER" > "$MASTER_ROOT/09_DIFF_AND_HASHES/readme.diff" || true
cp "$WORK/artifact/$BASE_MASTER" "$MASTER_ROOT/10_PREDECESSOR_MASTER/$BASE_MASTER"
printf '%s  %s\n' "$(sha "$OUT_INSTALLER")" "$OUT_INSTALLER" > "$MASTER_ROOT/09_DIFF_AND_HASHES/installer_sha256.txt"
( cd "$MASTER_ROOT" && find . -type f ! -name MASTER_MANIFEST_SHA256.txt -print0 | sort -z | xargs -0 sha256sum > MASTER_MANIFEST_SHA256.txt )
( cd "$MASTER_ROOT" && sha256sum -c MASTER_MANIFEST_SHA256.txt ) > "$EVIDENCE/09_master_manifest_verify.log"
rm -f "$OUT_MASTER"; ( cd "$WORK/master" && zip -X -qr "$GITHUB_WORKSPACE/$OUT_MASTER" master-v655-contain-rootfix )
unzip -t "$OUT_MASTER" > "$EVIDENCE/09_master_ziptest.log"
rm -rf "$WORK/mastercheck"; mkdir -p "$WORK/mastercheck"; unzip -q "$OUT_MASTER" -d "$WORK/mastercheck"
diff -qr "$WORK/after/affiliate-portal-router" "$WORK/mastercheck/master-v655-contain-rootfix/03_SOURCE/affiliate-portal-router" > "$EVIDENCE/09_source_vs_master.diff"
rm -rf "$WORK/masterinstaller"; mkdir -p "$WORK/masterinstaller"; unzip -q "$WORK/mastercheck/master-v655-contain-rootfix/02_INSTALL/$OUT_INSTALLER" -d "$WORK/masterinstaller"
diff -qr "$WORK/after/affiliate-portal-router" "$WORK/masterinstaller/affiliate-portal-router" > "$EVIDENCE/09_source_vs_master_installer.diff"
sha "$OUT_MASTER" | tee "$EVIDENCE/09_master_sha256.txt"
log "STAGE_09_MASTER_AND_PARITY=PASS"

log "STAGE_10_FINAL_COUNTERPROOF=START"
rm -rf "$WORK/finalcheck"; mkdir -p "$WORK/finalcheck"; unzip -q "$OUT_INSTALLER" -d "$WORK/finalcheck"
python3 .github/v655-contain-rootfix/tests/test_contain_rootfix.py "$PHP_BEFORE" "$WORK/finalcheck/affiliate-portal-router/pferdeportal-affiliate-router.php" "$WORK/finalcheck/affiliate-portal-router/readme.txt" | tee "$EVIDENCE/10_final_static.log"
grep -q 'CONTAIN_ROOTFIX_STATIC=PASS' "$EVIDENCE/10_final_static.log"
PPAR_TEST_PLUGIN_DIR="$WORK/finalcheck/affiliate-portal-router" php .github/v655/tests/test_kiss_public_heartbeat_architecture_v655.php | tee "$EVIDENCE/10_final_architecture.log"
grep -q 'ASSERTIONS=23 FAIL=0' "$EVIDENCE/10_final_architecture.log"
grep -q 'NO_CROP_VISUAL_COUNTERPROOF=PASS' "$EVIDENCE/08_visual_pixel_check.log"
diff -qr "$WORK/after/affiliate-portal-router" "$WORK/finalcheck/affiliate-portal-router" > "$EVIDENCE/10_final_source_parity.diff"
printf 'FINAL_DECISION=AUTOMATIC_RELEASE_PIPELINE_FINAL_PASS\nFINAL_RELEASE_GATE=PASS\nPRODUCTION_FILES_CHANGED=2\nCATEGORY_PRODUCT_FIXED_FRAME=PASS\nOBJECT_FIT_CONTAIN=PASS\nFULL_SOURCE_NO_CROP_VISUAL=PASS\nFIRST_SLOT_HOSTILE_CONFLICT=PASS\nWORDPRESS_HEADER_VERSION_655=PASS\nCANONICAL_STABLE_TAG_655=PASS\nFRONTEND_CSS_CHANGED=0\nDESIGNPLUGIN_CHANGED=0\nEBAY_RUNTIME_CHANGED=0\nSCHEDULER_CHANGED=0\n' | tee "$EVIDENCE/FINAL_DECISION.txt"
log "STAGE_10_FINAL_COUNTERPROOF=PASS"
log "FINAL_RELEASE_GATE=PASS"
