#!/usr/bin/env bash
set -euo pipefail
REPO='hallo-netizen/affiliate-pferdeportal'
BASE_ARTIFACT_ID='9509755514'
BASE_ARTIFACT_SHA='0ae7fb7ccdfbe5c559afa9d2c8343939b818de37e6075dbb9ae289a7d3d5bbd0'
BASE_INSTALLER='affiliate-zentrale_v6.55.0_CATEGORY_PRODUCT_CONTAIN_ROOTFIX_REALGATE.zip'
BASE_INSTALLER_SHA='c180c9477423bfdc982d03e6bcb0a2fc6f621e89f99d141c75edc2a5a5134a22'
BASE_MASTER='MASTER_AFFILIATE_ZENTRALE_V6_55_0_CATEGORY_PRODUCT_CONTAIN_ROOTFIX_REALGATE_20260824.zip'
BASE_MASTER_SHA='99770309efc9d885bb4b17430662faa20ce29d8723c05528700209ced764df3f'
OUT_INSTALLER='affiliate-zentrale_v6.56.0_SAFE_GAP_CHURN_REVALIDATION_ROOTFIX_REALGATE.zip'
OUT_MASTER='MASTER_AFFILIATE_ZENTRALE_V6_56_0_SAFE_GAP_CHURN_REVALIDATION_ROOTFIX_REALGATE_20260827.zip'
E='V656_RELEASE_EVIDENCE'
W="$(mktemp -d)"; HTTP_PID=''
cleanup(){ [ -z "${HTTP_PID:-}" ] || kill "$HTTP_PID" 2>/dev/null || true; rm -rf "$W"; }
trap cleanup EXIT
rm -rf "$E" "$OUT_INSTALLER" "$OUT_MASTER"; mkdir -p "$E"; : > "$E/STAGE_LOG.txt"
log(){ printf '%s\n' "$*" | tee -a "$E/STAGE_LOG.txt"; }
sha(){ sha256sum "$1" | awk '{print $1}'; }

log STAGE_01_BINDING_BASELINE_START
ART="$W/base-artifact.zip"; gh api "repos/$REPO/actions/artifacts/$BASE_ARTIFACT_ID/zip" > "$ART"
[ "$(sha "$ART")" = "$BASE_ARTIFACT_SHA" ]; unzip -q "$ART" -d "$W/art"
[ "$(sha "$W/art/$BASE_INSTALLER")" = "$BASE_INSTALLER_SHA" ]; [ "$(sha "$W/art/$BASE_MASTER")" = "$BASE_MASTER_SHA" ]
grep -Fxq 'FINAL_RELEASE_GATE=PASS' "$W/art/V655_CONTAIN_ROOTFIX_EVIDENCE/FINAL_DECISION.txt"
SCHED_JSON="$W/scheduler.json"; gh api "repos/$REPO/contents/.github/workflows/pferde-atelier-ebay-heartbeat.yml?ref=main" > "$SCHED_JSON"
python3 - "$SCHED_JSON" <<'PY' | tee "$E/01_scheduler_gate.txt"
import json,sys
j=json.load(open(sys.argv[1])); assert j['sha']=='bcdb8eeb90ac3f4664fceccc2e977345a0b8f190',j['sha']; print('MAIN_RESILIENT_SCHEDULER_PIN=PASS')
PY
printf '%s  %s\n%s  %s\n%s  %s\n' "$BASE_ARTIFACT_SHA" base-artifact.zip "$BASE_INSTALLER_SHA" "$BASE_INSTALLER" "$BASE_MASTER_SHA" "$BASE_MASTER" > "$E/01_baseline_sha256.txt"
log STAGE_01_BINDING_BASELINE_PASS

log STAGE_02_LIVE_SIGNATURE_NEGATIVE_START
mkdir -p "$W/before" "$W/after"; unzip -q "$W/art/$BASE_INSTALLER" -d "$W/before"; cp -a "$W/before/." "$W/after/"
python3 - "$W/v650-fixture.json" <<'PY'
import json,sys
stats=[]
for i in range(311):
 c=f'f{i+1:03d}'
 if i<91: stats.append({'concept':c,'received':1,'accepted':1})
 elif i<217: stats.append({'concept':c,'received':0,'accepted':0})
 else: stats.append({'concept':c,'received':1,'accepted':0})
j={'source_file_sha256':'466b99665bb96b12d34ba7c02a3af80c4ca2ebeb68d8b14db02c50f34507b1a1','build':'6.48.0-canonical-refresh-authority-rootfix-20260821','run_uuid':'110e36b0-ad6b-4202-96d6-43604da654b6','received':3137,'accepted':350,'review_pending':632,'hard_blocked':985,'profile_stats':stats}
json.dump(j,open(sys.argv[1],'w'))
PY
PPAR_TEST_PLUGIN_DIR="$W/before/affiliate-portal-router" PPAR_LIVE_COVERAGE_FIXTURE="$W/v650-fixture.json" PPAR_EXPECT_V650_MIGRATION=1 php .github/v6501/tests/test_coverage_gap_contract_v6501.php | tee "$E/02_v6501_historical_before.log"
grep -q 'FAIL=0' "$E/02_v6501_historical_before.log"
PPAR_TEST_PLUGIN_DIR="$W/before/affiliate-portal-router" php .github/v656/tests/test_live_failure_before_v656.php | tee "$E/02_exact_live_negative.log"
grep -Fxq 'LIVE_V655_NEW_MISSING_NEGATIVE=CONFIRMED' "$E/02_exact_live_negative.log"
log STAGE_02_LIVE_SIGNATURE_NEGATIVE_PASS

log STAGE_03_ROOTFIX_APPLY_AND_FULL_STATIC_START
python3 .github/v656/patches/apply_v656_safe_gap_churn.py "$W/after/affiliate-portal-router" | tee "$E/03_patch.log"
grep -Fxq 'V656_SAFE_GAP_CHURN_PATCH=PASS' "$E/03_patch.log"
find "$W/after/affiliate-portal-router" -type f -name '*.php' -print0 | sort -z | xargs -0 -n1 php -l > "$E/03_php_lint.log"
PPAR_TEST_PLUGIN_DIR="$W/after/affiliate-portal-router" php .github/v656/tests/test_business_gap_churn_v656.php | tee "$E/03_churn.log"; grep -Fxq 'ASSERTIONS=20 FAIL=0' "$E/03_churn.log"
PPAR_TEST_PLUGIN_DIR="$W/after/affiliate-portal-router" php .github/v656/tests/test_architecture_v656.php | tee "$E/03_architecture.log"; grep -Fxq 'ASSERTIONS=32 FAIL=0' "$E/03_architecture.log"
PPAR_TEST_PLUGIN_DIR="$W/after/affiliate-portal-router" PPAR_LIVE_COVERAGE_FIXTURE="$W/v650-fixture.json" PPAR_EXPECT_V650_MIGRATION=1 php .github/v6501/tests/test_coverage_gap_contract_v6501.php | tee "$E/03_v6501_historical_after.log"; grep -q 'FAIL=0' "$E/03_v6501_historical_after.log"
(diff -qr "$W/before/affiliate-portal-router" "$W/after/affiliate-portal-router" || true) > "$E/03_scope.diff"
python3 - "$E/03_scope.diff" <<'PY' | tee "$E/03_scope_gate.txt"
import re,sys
s=open(sys.argv[1]).read().splitlines(); changed=[]
for l in s:
 m=re.match(r'Files .*/affiliate-portal-router/(.+) and .*/affiliate-portal-router/(.+) differ$',l)
 if m: changed.append(m.group(1))
expected=sorted(['includes/trait-ppar-ebay-run.php','includes/trait-ppar-ebay.php','pferdeportal-affiliate-router.php','readme.txt'])
assert sorted(changed)==expected,(changed,expected)
print('PRODUCTION_SCOPE_EXACT_4=PASS')
PY
[ "$(sha "$W/before/affiliate-portal-router/assets/frontend.css")" = "$(sha "$W/after/affiliate-portal-router/assets/frontend.css")" ]
[ "$(sha "$W/before/affiliate-portal-router/includes/trait-ppar-article-plans.php")" = "$(sha "$W/after/affiliate-portal-router/includes/trait-ppar-article-plans.php")" ]
log STAGE_03_ROOTFIX_APPLY_AND_FULL_STATIC_PASS

log STAGE_04_BUILD_FRESH_UNPACK_REPEAT_START
( cd "$W/after" && zip -X -qr "$GITHUB_WORKSPACE/$OUT_INSTALLER" affiliate-portal-router )
unzip -t "$OUT_INSTALLER" > "$E/04_installer_ziptest.txt"; mkdir -p "$W/fresh"; unzip -q "$OUT_INSTALLER" -d "$W/fresh"
diff -qr "$W/after/affiliate-portal-router" "$W/fresh/affiliate-portal-router" > "$E/04_source_fresh.diff"
PPAR_TEST_PLUGIN_DIR="$W/fresh/affiliate-portal-router" php .github/v656/tests/test_business_gap_churn_v656.php | tee "$E/04_churn_fresh.log"; grep -Fxq 'ASSERTIONS=20 FAIL=0' "$E/04_churn_fresh.log"
PPAR_TEST_PLUGIN_DIR="$W/fresh/affiliate-portal-router" php .github/v656/tests/test_architecture_v656.php | tee "$E/04_architecture_fresh.log"; grep -Fxq 'ASSERTIONS=32 FAIL=0' "$E/04_architecture_fresh.log"
PPAR_TEST_PLUGIN_DIR="$W/fresh/affiliate-portal-router" PPAR_LIVE_COVERAGE_FIXTURE="$W/v650-fixture.json" PPAR_EXPECT_V650_MIGRATION=1 php .github/v6501/tests/test_coverage_gap_contract_v6501.php | tee "$E/04_v6501_fresh.log"; grep -q 'FAIL=0' "$E/04_v6501_fresh.log"
sha "$OUT_INSTALLER" | tee "$E/04_installer_sha256.txt"
log STAGE_04_BUILD_FRESH_UNPACK_REPEAT_PASS

setup_wp(){ local ver="$1" path="$2" pref="$3" tag="$4"; rm -rf "$path"; mkdir -p "$path"; wp core download --version="$ver" --path="$path" --force --quiet; wp config create --path="$path" --dbname=v656 --dbuser=wp --dbpass=wppass --dbhost=127.0.0.1:3306 --dbprefix="$pref" --skip-check --force; wp core install --path="$path" --url="http://v656-${pref}.test" --title=V656 --admin_user=admin --admin_password='AdminPass-656!' --admin_email=test@example.com --skip-email; wp plugin install "$GITHUB_WORKSPACE/$OUT_INSTALLER" --path="$path" --activate --force; wp eval-file "$GITHUB_WORKSPACE/.github/v656/tests/real_wordpress_v656.php" --path="$path" | tee "$E/${tag}_real.log"; grep -q 'FAIL=0' "$E/${tag}_real.log"; }
log STAGE_05_REAL_WORDPRESS_701_START; setup_wp 7.0.1 "$W/wp701" w7_ 05_wp701; log STAGE_05_REAL_WORDPRESS_701_PASS
log STAGE_06_REAL_WORDPRESS_683_START; setup_wp 6.8.3 "$W/wp683" w68_ 06_wp683; log STAGE_06_REAL_WORDPRESS_683_PASS

log STAGE_07_VISUAL_AND_RENDER_REGRESSION_START
mkdir -p "$W/visual-assets"; cat > "$W/visual-assets/landscape.svg" <<'SVG'
<svg xmlns="http://www.w3.org/2000/svg" width="300" height="200"><rect width="300" height="200" fill="#ffeb3b"/><rect x="4" y="4" width="292" height="192" fill="none" stroke="#ff0000" stroke-width="8"/></svg>
SVG
cat > "$W/visual-assets/portrait.svg" <<'SVG'
<svg xmlns="http://www.w3.org/2000/svg" width="200" height="300"><rect width="200" height="300" fill="#00bcd4"/><rect x="4" y="4" width="192" height="292" fill="none" stroke="#00aa00" stroke-width="8"/></svg>
SVG
cat > "$W/visual-assets/square.svg" <<'SVG'
<svg xmlns="http://www.w3.org/2000/svg" width="300" height="300"><rect width="300" height="300" fill="#00ffff"/><rect x="4" y="4" width="292" height="292" fill="none" stroke="#ff00ff" stroke-width="8"/></svg>
SVG
python3 -m http.server 8765 --bind 127.0.0.1 --directory "$W/visual-assets" > "$E/07_http.log" 2>&1 & HTTP_PID=$!; sleep 1
PPAR_VISUAL_BASE='http://127.0.0.1:8765' wp eval-file "$GITHUB_WORKSPACE/.github/v655-contain-rootfix/tests/emit_visual_fixture.php" --path="$W/wp701" > "$W/fragments.html"
cat > "$W/visual.html" <<'HTML'
<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;padding:0}.g{display:grid;grid-template-columns:150px 150px 150px;gap:20px}.visual-slot{width:150px;height:150px;overflow:hidden}.visual-slot>.ppar-banner-link{display:block!important;width:150px!important;height:150px!important}.ppar-banner-text{display:none!important}.ppar-banner-image-wrap{display:flex!important;width:92px!important;height:110px!important;overflow:hidden!important}.ppar-banner-image{width:92px!important;height:110px!important;object-fit:cover!important;object-position:left top!important}.visual-slot:first-child .ppar-banner-image-wrap{width:61px!important;height:137px!important}.visual-slot:first-child .ppar-banner-image{width:61px!important;height:137px!important;object-fit:cover!important;object-position:left top!important}</style></head><body><div class="g">
HTML
cat "$W/fragments.html" >> "$W/visual.html"; cat >> "$W/visual.html" <<'HTML'
</div><pre id="r"></pre><script>addEventListener('load',()=>{let a=[...document.querySelectorAll('.visual-slot img')].map(i=>{let r=i.getBoundingClientRect(),s=getComputedStyle(i);return [r.width,r.height,s.objectFit,s.objectPosition,i.naturalWidth,i.naturalHeight]});let p=JSON.stringify(a)==='[[150,150,"contain","50% 50%",300,200],[150,150,"contain","50% 50%",200,300],[150,150,"contain","50% 50%",300,300]]';document.body.dataset.pass=p?'1':'0';document.querySelector('#r').textContent=JSON.stringify(a)});</script></body></html>
HTML
CHROME="$(command -v google-chrome || command -v google-chrome-stable || command -v chromium || true)"; [ -n "$CHROME" ]
"$CHROME" --headless --no-sandbox --disable-gpu --disable-dev-shm-usage --allow-file-access-from-files --virtual-time-budget=3000 --dump-dom "file://$W/visual.html" > "$E/07_visual_dom.html" 2> "$E/07_chrome.err"
grep -q 'data-pass="1"' "$E/07_visual_dom.html"; kill "$HTTP_PID" 2>/dev/null || true; wait "$HTTP_PID" 2>/dev/null || true; HTTP_PID=''
echo VISUAL_CONTAIN_REAL_BROWSER=PASS | tee "$E/07_visual_gate.txt"
log STAGE_07_VISUAL_AND_RENDER_REGRESSION_PASS

log STAGE_08_MASTER_BUILD_PARITY_START
MD="$W/master"; mkdir -p "$MD/00_READ_ME_FIRST" "$MD/01_PREDECESSOR" "$MD/02_INSTALLER" "$MD/03_SOURCE" "$MD/04_TESTS" "$MD/05_EVIDENCE" "$MD/06_HISTORY" "$MD/07_DIFF_AND_HASHES" "$MD/08_GITHUB"
cat > "$MD/00_READ_ME_FIRST/V656_RELEASE_STATUS.txt" <<EOF
Affiliate-Zentrale V6.56.0 SAFE-GAP CHURN REVALIDATION ROOTFIX
Binding predecessor: $BASE_MASTER
Production scope: exactly 4 Affiliate files.
Main scheduler: unchanged/pinned.
Live provider E2E after installation is operational proof, not fabricated by CI.
EOF
cp "$W/art/$BASE_MASTER" "$MD/01_PREDECESSOR/"; cp "$OUT_INSTALLER" "$MD/02_INSTALLER/"; cp -a "$W/after/affiliate-portal-router" "$MD/03_SOURCE/"; cp -a .github/v656 "$MD/04_TESTS/"; cp -a "$E/." "$MD/05_EVIDENCE/"; cp .github/v656/ERROR_CATALOG.md .github/v656/WORKLOG.md "$MD/06_HISTORY/"; cp "$E/03_scope.diff" "$MD/07_DIFF_AND_HASHES/production_scope.diff"; printf '%s\n' 'v656-business-safe-gap-churn-revalidation-rootfix-20260827' > "$MD/08_GITHUB/branch.txt"
( cd "$MD" && find . -type f ! -path './07_DIFF_AND_HASHES/MASTER_MANIFEST_SHA256.txt' -print0 | sort -z | xargs -0 sha256sum > 07_DIFF_AND_HASHES/MASTER_MANIFEST_SHA256.txt && sha256sum -c 07_DIFF_AND_HASHES/MASTER_MANIFEST_SHA256.txt > /dev/null )
( cd "$MD" && zip -X -qr "$GITHUB_WORKSPACE/$OUT_MASTER" . ); unzip -t "$OUT_MASTER" > "$E/08_master_ziptest.txt"
mkdir -p "$W/masterfresh"; unzip -q "$OUT_MASTER" -d "$W/masterfresh"; (cd "$W/masterfresh" && sha256sum -c 07_DIFF_AND_HASHES/MASTER_MANIFEST_SHA256.txt > "$E/08_master_manifest_verify.txt")
cmp -s "$OUT_INSTALLER" "$W/masterfresh/02_INSTALLER/$OUT_INSTALLER"; diff -qr "$W/fresh/affiliate-portal-router" "$W/masterfresh/03_SOURCE/affiliate-portal-router" > "$E/08_master_source_parity.diff"
sha "$OUT_MASTER" | tee "$E/08_master_sha256.txt"
log STAGE_08_MASTER_BUILD_PARITY_PASS

log STAGE_09_FINAL_COUNTERPROOF_FROM_MASTER_START
MP="$W/masterfresh/03_SOURCE/affiliate-portal-router"
PPAR_TEST_PLUGIN_DIR="$MP" php "$W/masterfresh/04_TESTS/v656/tests/test_business_gap_churn_v656.php" | tee "$E/09_churn_master.log"; grep -Fxq 'ASSERTIONS=20 FAIL=0' "$E/09_churn_master.log"
PPAR_TEST_PLUGIN_DIR="$MP" php "$W/masterfresh/04_TESTS/v656/tests/test_architecture_v656.php" | tee "$E/09_arch_master.log"; grep -Fxq 'ASSERTIONS=32 FAIL=0' "$E/09_arch_master.log"
PPAR_TEST_PLUGIN_DIR="$MP" PPAR_LIVE_COVERAGE_FIXTURE="$W/v650-fixture.json" PPAR_EXPECT_V650_MIGRATION=1 php .github/v6501/tests/test_coverage_gap_contract_v6501.php | tee "$E/09_historical_master.log"; grep -q 'FAIL=0' "$E/09_historical_master.log"
rm -rf "$W/wp-final"; mkdir -p "$W/wp-final"; wp core download --version=7.0.1 --path="$W/wp-final" --force --quiet; wp config create --path="$W/wp-final" --dbname=v656 --dbuser=wp --dbpass=wppass --dbhost=127.0.0.1:3306 --dbprefix=wf_ --skip-check --force; wp core install --path="$W/wp-final" --url=http://v656-final.test --title=V656Final --admin_user=admin --admin_password='AdminPass-656!' --admin_email=test@example.com --skip-email; wp plugin install "$W/masterfresh/02_INSTALLER/$OUT_INSTALLER" --path="$W/wp-final" --activate --force; wp eval-file "$W/masterfresh/04_TESTS/v656/tests/real_wordpress_v656.php" --path="$W/wp-final" | tee "$E/09_real_master_installer.log"; grep -q 'FAIL=0' "$E/09_real_master_installer.log"
log STAGE_09_FINAL_COUNTERPROOF_FROM_MASTER_PASS

cat > "$E/FINAL_DECISION.txt" <<EOF
FINAL_DECISION=AUTOMATIC_RELEASE_PIPELINE_FINAL_PASS
FINAL_RELEASE_GATE=PASS
VERSION=6.56.0
RUNTIME_BUILD=6.56.0-safe-gap-churn-revalidation-rootfix-20260827
PINNED_V655_PREDECESSOR=PASS
EXACT_LIVE_SIGNATURE_NEGATIVE=PASS
V6501_HISTORICAL_SAFE_GAP_REGRESSION=PASS
V656_CHURN_POSITIVE_NEGATIVE=PASS
V656_ARCHITECTURE=PASS
REAL_WORDPRESS_7_0_1=PASS
REAL_WORDPRESS_6_8_3=PASS
RESILIENT_MAIN_SCHEDULER_UNCHANGED=PASS
CHECKPOINT_RESTART_CONTRACT=PASS
CANDIDATE_SKIP_STORAGE_HARD_CONTRACT=PASS
CATEGORY_PRODUCT_CONTAIN_BROWSER=PASS
ARTICLE_PRODUCT_RENDERER=PASS
FRESH_UNPACK=PASS
SOURCE_INSTALLER_MASTER_PARITY=PASS
MASTER_MANIFEST=PASS
FINAL_MASTER_INSTALL_COUNTERPROOF=PASS
MAIN_PRODUCT_BRANCH_MERGE=NO
EXTERNAL_EBAY_PROVIDER_LIVE_E2E=OPEN_NOT_CLAIMED
EOF
cp "$E/FINAL_DECISION.txt" "$MD/05_EVIDENCE/FINAL_DECISION.txt"; rm -f "$MD/07_DIFF_AND_HASHES/MASTER_MANIFEST_SHA256.txt" "$OUT_MASTER"; (cd "$MD" && find . -type f ! -path './07_DIFF_AND_HASHES/MASTER_MANIFEST_SHA256.txt' -print0 | sort -z | xargs -0 sha256sum > 07_DIFF_AND_HASHES/MASTER_MANIFEST_SHA256.txt && sha256sum -c 07_DIFF_AND_HASHES/MASTER_MANIFEST_SHA256.txt >/dev/null && zip -X -qr "$GITHUB_WORKSPACE/$OUT_MASTER" .)
rm -rf "$W/master-final"; mkdir -p "$W/master-final"; unzip -q "$OUT_MASTER" -d "$W/master-final"; (cd "$W/master-final" && sha256sum -c 07_DIFF_AND_HASHES/MASTER_MANIFEST_SHA256.txt > "$E/FINAL_master_manifest_verify.txt"); cmp -s "$OUT_INSTALLER" "$W/master-final/02_INSTALLER/$OUT_INSTALLER"; diff -qr "$W/fresh/affiliate-portal-router" "$W/master-final/03_SOURCE/affiliate-portal-router" > "$E/FINAL_master_source_parity.diff"; grep -Fxq 'FINAL_RELEASE_GATE=PASS' "$W/master-final/05_EVIDENCE/FINAL_DECISION.txt"
sha "$OUT_INSTALLER" > "$E/FINAL_INSTALLER_SHA256.txt"; sha "$OUT_MASTER" > "$E/FINAL_MASTER_SHA256.txt"
echo "INSTALLER_SHA256=$(cat "$E/FINAL_INSTALLER_SHA256.txt")"; echo "MASTER_SHA256=$(cat "$E/FINAL_MASTER_SHA256.txt")"; echo FINAL_RELEASE_GATE=PASS
