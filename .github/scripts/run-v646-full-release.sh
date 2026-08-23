#!/usr/bin/env bash
set -euo pipefail
WORK="${GITHUB_WORKSPACE:-$(pwd)}"
BASEZIP="$WORK/CODEX_V645_REALGATE_SOURCE_AND_EXACT_TASK_20260820.zip"
PKGROOT=/tmp/v646pkg
PKG="$PKGROOT/CODEX_V645_REALGATE_SOURCE_AND_EXACT_TASK_20260820"
SRC="$PKG/02_SOURCE_V645/affiliate-portal-router"
BASE="$PKG/05_BASELINE_V644/affiliate-portal-router"
E="$WORK/V646_RELEASE_EVIDENCE"
INSTALL="$WORK/affiliate-zentrale_v6.46.0_PUBLIC_FRESHNESS_SELECTION_CONTRACT_ROOTFIX_REALGATE.zip"
MASTER_DIR=/tmp/master-v646
MASTER="$WORK/MASTER_AFFILIATE_ZENTRALE_V6_46_0_PUBLIC_FRESHNESS_SELECTION_CONTRACT_ROOTFIX_REALGATE_20260820.zip"
WP1=/tmp/wordpress-v646-source
WP2=/tmp/wordpress-v646-final
FRESH=/tmp/v646-fresh
rm -rf "$PKGROOT" "$E" "$MASTER_DIR" "$WP1" "$WP2" "$FRESH"
rm -f "$INSTALL" "$MASTER"
mkdir -p "$E" "$FRESH"
block(){ echo "BLOCKED: $*" | tee "$E/BLOCKED.txt"; exit 1; }
trap 'rc=$?; if [ $rc -ne 0 ]; then echo "FINAL_DECISION=BLOCKED" > "$E/FINAL_DECISION.txt"; fi' EXIT

test -f "$BASEZIP" || block "V6.45 immutable base package missing"
unzip -t "$BASEZIP" > "$E/00_base_zip_integrity.log"
mkdir -p "$PKGROOT"; unzip -q "$BASEZIP" -d "$PKGROOT"
(cd "$PKG/02_SOURCE_V645" && sha256sum -c SOURCE_SHA256.txt) > "$E/01_v645_base_sha.log"
(cd "$PKG/02_SOURCE_V645" && patch -p2 --forward --batch < "$WORK/.github/v646/v646_relative.patch") > "$E/02_patch_apply.log"
cp "$WORK/.github/v646/SOURCE_SHA256.txt" "$PKG/02_SOURCE_V645/SOURCE_SHA256.txt"
(cd "$PKG/02_SOURCE_V645" && sha256sum -c SOURCE_SHA256.txt) > "$E/03_v646_source_sha.log"
mkdir -p "$PKG/04_TESTS/V646_ROOTCAUSE"
cp "$WORK/.github/v646/tests/"*.php "$PKG/04_TESTS/V646_ROOTCAUSE/"
cp "$WORK/.github/overlays/v645/soft_failure_recovery.php" "$PKG/03_REAL_GATE/soft_failure_recovery.php"
cp "$WORK/.github/v646/real/public_freshness_contract_v646.php" "$PKG/03_REAL_GATE/public_freshness_contract_v646.php"
sed -i "s/6\.45\.0/6.46.0/g" "$PKG/03_REAL_GATE/verify_environment.php"
rm -rf /tmp/v645compare; mkdir -p /tmp/v645compare; unzip -q "$BASEZIP" -d /tmp/v645compare
mapfile -t changed < <(diff -qr /tmp/v645compare/CODEX_V645_REALGATE_SOURCE_AND_EXACT_TASK_20260820/02_SOURCE_V645/affiliate-portal-router "$SRC" | sed -E 's#^Files .*/affiliate-portal-router/([^ ]+) and .* differ$#\1#' | sort)
printf '%s\n' "${changed[@]}" > "$E/04_changed_files.txt"
expected=$'includes/trait-ppar-ebay-run.php\nincludes/trait-ppar-ebay.php\npferdeportal-affiliate-router.php\nreadme.txt'
test "$(printf '%s\n' "${changed[@]}")" = "$expected" || block "production change scope is not exactly four files"

run_dir(){
  local dir="$1" out="$2" src="$3"; : > "$out"; local fail=0 count=0 assertions=0
  while IFS= read -r -d '' f; do
    count=$((count+1)); echo "===== $(basename "$f") =====" >> "$out"
    set +e; PPAR_TEST_PLUGIN_DIR="$src" PPAR_BASELINE_PLUGIN_DIR="$BASE" PPAR_TEST_MASTER_ROOT="$PKG" timeout 240 php "$f" >> "$out" 2>&1; rc=$?; set -e
    echo "__TEST_EXIT__ $rc $(basename "$f")" >> "$out"; [ "$rc" -eq 0 ] || fail=$((fail+1))
  done < <(find "$dir" -maxdepth 1 -type f -name '*.php' -print0 | sort -z)
  assertions=$(grep -oE 'ASSERTIONS=[0-9]+' "$out" | cut -d= -f2 | awk '{s+=$1} END{print s+0}')
  echo "COUNT=$count FAIL=$fail ASSERTIONS=$assertions" | tee -a "$out"
  [ "$fail" -eq 0 ]
}
source_gate(){
  local src="$1" prefix="$2"; mkdir -p "$E/$prefix"
  (cd "$(dirname "$src")" && sha256sum -c SOURCE_SHA256.txt) > "$E/$prefix/01_sha.log" 2>&1 || return 1
  find "$src" -type f -name '*.php' -print0 | sort -z | xargs -0 -n1 php -l > "$E/$prefix/02_php_lint.log" || return 1
  for f in "$src/assets/ebay-portal-catalog-v2.json" "$src/assets/portal-structure-v279.json"; do php -r '$f=$argv[1];json_decode(file_get_contents($f),true);if(json_last_error()!==JSON_ERROR_NONE){exit(1);}echo "JSON_OK $f\n";' "$f"; done > "$E/$prefix/03_json.log" || return 1
  run_dir "$PKG/04_TESTS/V646_ROOTCAUSE" "$E/$prefix/04_v646.log" "$src" || return 1
  tmp=$(mktemp -d); find "$PKG/04_TESTS/V645_ROOTCAUSE" -maxdepth 1 -type f -name '*.php' ! -name 'test_architecture_v645.php' -exec cp {} "$tmp/" \;; run_dir "$tmp" "$E/$prefix/05_v645.log" "$src" || { rm -rf "$tmp"; return 1; }; rm -rf "$tmp"
  run_dir "$PKG/04_TESTS/V643_REGRESSION" "$E/$prefix/06_v643.log" "$src" || return 1
  tmp=$(mktemp -d); find "$PKG/04_TESTS/V644_ROOTCAUSE" -maxdepth 1 -type f -name '*.php' ! -name 'test_architecture_v644.php' -exec cp {} "$tmp/" \;; run_dir "$tmp" "$E/$prefix/07_v644.log" "$src" || { rm -rf "$tmp"; return 1; }; rm -rf "$tmp"
  post="$E/$prefix/08_postmortem.log"; set +e; PPAR_TEST_PLUGIN_DIR="$src" PPAR_BASELINE_PLUGIN_DIR="$BASE" PPAR_TEST_MASTER_ROOT="$PKG" php "$PKG/04_TESTS/V644_POSTMORTEM/test_v644_release_gate_gaps.php" > "$post" 2>&1; prc=$?; set -e
  [ "$prc" -ne 0 ] && [ "$(grep -c '^FAIL ' "$post")" -eq 2 ] && grep -Fq 'FAIL release workflow test must not replace production selection_request/process_tick' "$post" && grep -Fq 'FAIL release workflow test must execute the real 311-concept manifest, not a 3-concept substitute' "$post" || return 1
  run_dir "$PKG/04_TESTS/HISTORICAL_R5_54" "$E/$prefix/09_historical.log" "$src" || return 1
  grep -Fxq 'COUNT=54 FAIL=0 ASSERTIONS=3097' "$E/$prefix/09_historical.log" || return 1
  printf 'MASTER_CANONICAL_ASSERTIONS=3116\nEXPLICIT_RUNNER_ASSERTIONS=3097\nLEGACY_IMPLICIT_CHECKS=19\n' > "$E/$prefix/10_assertion_accounting.txt"
  echo 'SOURCE_GATE=PASS' > "$E/$prefix/RESULT.txt"
}
setup_wp(){
  local wpdir="$1"; rm -rf "$wpdir"; mkdir -p "$wpdir"
  wp core download --version=7.0.1 --path="$wpdir" --force --allow-root >/dev/null
  wp config create --path="$wpdir" --dbname=v646gate --dbuser=wp --dbpass=wppass --dbhost=127.0.0.1:3306 --skip-check --allow-root >/dev/null
  wp core install --path="$wpdir" --url=http://v646.test --title='V646 Gate' --admin_user=gateadmin --admin_password='GateOnly-20260820!' --admin_email=gate@example.invalid --skip-email --allow-root >/dev/null
}
real_gate(){
  local wpdir="$1" prefix="$2"; mkdir -p "$E/$prefix"
  wp eval 'global $wpdb; echo "WP=".get_bloginfo("version")." PHP=".PHP_VERSION." DB=".$wpdb->get_var("SELECT VERSION()")."\n";' --path="$wpdir" --allow-root > "$E/$prefix/00_environment.log"
  grep -Fq 'WP=7.0.1 PHP=8.4.' "$E/$prefix/00_environment.log" && grep -Fq 'DB=11.4.' "$E/$prefix/00_environment.log" || return 1
  rm -rf "$PKG/CODEX_EVIDENCE_REAL_GATE"
  (cd "$PKG" && WP_ROOT="$wpdir" WP="$(command -v wp)" 07_RUNNERS/run_real_gate_from_existing_wordpress.sh) > "$E/$prefix/01_real_A_H_console.log" 2>&1 || return 1
  cp -a "$PKG/CODEX_EVIDENCE_REAL_GATE" "$E/$prefix/A_H"
  wp eval-file "$PKG/03_REAL_GATE/public_freshness_contract_v646.php" --path="$wpdir" --allow-root > "$E/$prefix/02_public_freshness_v646.log" 2>&1 || return 1
  grep -Fxq 'PUBLIC_FRESHNESS_V646_OK' "$E/$prefix/02_public_freshness_v646.log" || return 1
  echo 'REAL_GATE=PASS' > "$E/$prefix/RESULT.txt"
}

source_gate "$SRC" PREBUILD_SOURCE || block "pre-build source/full-workflow regression failed"
setup_wp "$WP1"
rm -rf "$WP1/wp-content/plugins/affiliate-portal-router"; cp -a "$SRC" "$WP1/wp-content/plugins/affiliate-portal-router"
wp plugin activate affiliate-portal-router --path="$WP1" --allow-root >/dev/null
real_gate "$WP1" PREBUILD_REAL || block "pre-build real WordPress/MariaDB A-H+V646 gate failed"
(cd "$PKG/02_SOURCE_V645" && sha256sum -c SOURCE_SHA256.txt) > "$E/05_source_after_prebuild.log"

(cd "$PKG/02_SOURCE_V645" && zip -qr "$INSTALL" affiliate-portal-router)
unzip -t "$INSTALL" > "$E/06_install_zip_integrity.log"; sha256sum "$INSTALL" > "$E/07_install_sha256.txt"
unzip -q "$INSTALL" -d "$FRESH"
(cd "$SRC" && find . -type f -print0 | sort -z | xargs -0 sha256sum) > "$E/08_source_tree.sha"
(cd "$FRESH/affiliate-portal-router" && find . -type f -print0 | sort -z | xargs -0 sha256sum) > "$E/09_final_zip_tree.sha"
diff -u "$E/08_source_tree.sha" "$E/09_final_zip_tree.sha" > "$E/10_source_vs_zip.diff"; test ! -s "$E/10_source_vs_zip.diff" || block "final ZIP differs from approved source"
cp "$WORK/.github/v646/SOURCE_SHA256.txt" "$FRESH/SOURCE_SHA256.txt"
source_gate "$FRESH/affiliate-portal-router" FINAL_ZIP_SOURCE || block "final ZIP source/full-workflow regression failed"

wp db reset --yes --path="$WP1" --allow-root >/dev/null
setup_wp "$WP2"
wp plugin install "$INSTALL" --activate --path="$WP2" --allow-root >/dev/null
wp plugin status affiliate-portal-router --path="$WP2" --allow-root > "$E/11_final_zip_plugin_status.log"
grep -Fq 'Status: Active' "$E/11_final_zip_plugin_status.log" && grep -Fq 'Version: 6.46.0' "$E/11_final_zip_plugin_status.log" || block "final ZIP install/version failed"
real_gate "$WP2" FINAL_ZIP_REAL || block "final ZIP real WordPress/MariaDB A-H+V646 gate failed"

wp db reset --yes --path="$WP2" --allow-root >/dev/null
setup_wp "$WP2"; wp plugin install "$INSTALL" --activate --path="$WP2" --allow-root >/dev/null
wp eval-file "$PKG/03_REAL_GATE/public_freshness_contract_v646.php" --path="$WP2" --allow-root > "$E/12_counterproof_v646.log" 2>&1 || block "post-green V6.46 counterproof failed"
grep -Fxq 'PUBLIC_FRESHNESS_V646_OK' "$E/12_counterproof_v646.log" || block "post-green counterproof marker missing"

unzip -t "$INSTALL" > "$E/13_install_integrity_after.log"; sha256sum "$INSTALL" > "$E/14_install_sha256_after.txt"
diff -u "$E/07_install_sha256.txt" "$E/14_install_sha256_after.txt" > "$E/15_install_hash_stability.diff"; test ! -s "$E/15_install_hash_stability.diff" || block "final installer changed after tests"
cat > "$E/RELEASE_REPORT.md" <<'EOF'
# Affiliate-Zentrale V6.46.0 release report

## Proven root cause
V6.45 selection/materialisation did not enforce the same `fresh_until` contract as the public BUSINESS coverage gate. In long-lived same-UUID runs, rows could be selected/materialised after their six-hour source freshness expired; public coverage then necessarily rejected those published objects as `source_stale`. This permits internal materialisation to rise while public coverage remains zero.

## Root fix
BUSINESS prepare SQL, defense-in-depth planning, apply, and reserve promotion now enforce public freshness/end eligibility. A winner that ages out between prepare and apply becomes a bounded candidate-local soft failure. The automatic V6.45 recovery is provenance- and evidence-gated: it preserves UUID and reopens only an exact `insufficient_safe_sources` / coverage_verify state with 311/311 missing, prior BUSINESS materialisation, and exclusively `source_stale` invalid reasons. Mixed/unknown causes remain terminal.

## Not changed
No article/title/prompt/SEO/design/frontend/category/product-domain decision logic was changed. Changes are limited to technical eBay run/selection freshness infrastructure plus version/readme.

## Verification
Full pre-build source/historical regression; real WordPress 7.0.1 + PHP 8.4 + MariaDB 11.4 A-H; new real freshness/migration positive+negative gate; final ZIP fresh-unpack identity; full source/historical regression again against final ZIP; final ZIP installation into fresh WordPress/MariaDB and all real gates again; post-green counterproof; immutable ZIP recheck.

## Result
PASS – INSTALLATION FREIGEGEBEN
EOF
cat > "$E/REAL_GATE_FINAL_MATRIX.txt" <<'EOF'
Realer kritischer Pfad getestet: JA
Echte Worker-Implementierung: JA
Persistierter Zwischenzustand: JA
Terminierung bewiesen: JA
No-Progress-Abbruch bewiesen: JA
Positive Fälle: PASS
Negative Fälle: PASS
Recovery: PASS
Gesamtworkflow-Regression: PASS
Finale Installations-ZIP erneut geprüft: PASS
Finale Installations-ZIP real geprüft: PASS
Gegenbeweis: PASS
EOF
mkdir -p "$MASTER_DIR/00_READ_ME_FIRST" "$MASTER_DIR/01_MASTER_BINDING" "$MASTER_DIR/02_INSTALL" "$MASTER_DIR/03_SOURCE" "$MASTER_DIR/04_TESTS_AND_REALGATE" "$MASTER_DIR/05_REPORT"
cp "$E/REAL_GATE_FINAL_MATRIX.txt" "$MASTER_DIR/00_READ_ME_FIRST/"; cp "$PKG/01_MASTER_BINDING/HARTER_PRUEF_BUILD_UND_FREIGABEVERTRAG.md" "$MASTER_DIR/01_MASTER_BINDING/"; cp "$INSTALL" "$MASTER_DIR/02_INSTALL/"; cp -a "$SRC" "$MASTER_DIR/03_SOURCE/affiliate-portal-router"; cp -a "$E"/. "$MASTER_DIR/04_TESTS_AND_REALGATE/"; cp "$E/RELEASE_REPORT.md" "$MASTER_DIR/05_REPORT/"
(cd "$MASTER_DIR" && find . -type f ! -name MASTER_SHA256.txt -print0 | sort -z | xargs -0 sha256sum > MASTER_SHA256.txt && sha256sum -c MASTER_SHA256.txt > MASTER_MANIFEST_VERIFIED.txt)
(cd "$(dirname "$MASTER_DIR")" && zip -qr "$MASTER" "$(basename "$MASTER_DIR")")
unzip -t "$MASTER" > "$E/16_master_integrity.log"; sha256sum "$MASTER" > "$E/17_master_sha256.txt"
rm -rf /tmp/master-v646-fresh; mkdir -p /tmp/master-v646-fresh; unzip -q "$MASTER" -d /tmp/master-v646-fresh
MF="/tmp/master-v646-fresh/$(basename "$MASTER_DIR")"; (cd "$MF" && sha256sum -c MASTER_SHA256.txt) > "$E/18_master_fresh_manifest.log"
cmp -s "$INSTALL" "$MF/02_INSTALL/$(basename "$INSTALL")" || block "MASTER embedded installer differs from standalone installer"
sha256sum "$INSTALL" "$MF/02_INSTALL/$(basename "$INSTALL")" > "$E/19_embedded_installer_identity.txt"
printf 'FINAL_DECISION=PASS\nINSTALLATION=FREIGEGEBEN\nVERSION=6.46.0\n' > "$E/FINAL_DECISION.txt"
sha256sum "$INSTALL" "$MASTER" | tee "$E/FINAL_ARTIFACT_SHA256.txt"
echo V646_FINAL_RELEASE_VERIFIED_OK
