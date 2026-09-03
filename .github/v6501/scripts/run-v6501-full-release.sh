#!/usr/bin/env bash
set -euo pipefail
WORK="${GITHUB_WORKSPACE:-$(pwd)}"
E="$WORK/V6501_RELEASE_EVIDENCE"
V650="$WORK/.github/v650"
V6501="$WORK/.github/v6501"
V647="${V647_HARNESS_ROOT:-/tmp/v647-harness/.github/v647}"
V648="${V648_HARNESS_ROOT:-/tmp/v648-harness/.github/v648}"
V649="${V649_HARNESS_ROOT:-/tmp/v649-harness/.github/v649}"
PKGZIP="$WORK/CODEX_V645_REALGATE_SOURCE_AND_EXACT_TASK_20260820.zip"
PKGROOT=/tmp/v6501pkg
PKG="$PKGROOT/CODEX_V645_REALGATE_SOURCE_AND_EXACT_TASK_20260820"
BASE="$PKG/05_BASELINE_V644/affiliate-portal-router"
BINDROOT=/tmp/v649-binding-6501
BINDMASTER="$BINDROOT/master-v649"
V649BASE="$BINDMASTER/03_SOURCE/affiliate-portal-router"
RECON=/tmp/v6501-reconstructed
RECON_PARENT="$RECON/CODEX_V645_REALGATE_SOURCE_AND_EXACT_TASK_20260820/02_SOURCE_V645"
RECONSRC="$RECON_PARENT/affiliate-portal-router"
V647BASE=/tmp/v647-approved-source-6501
V648BASE=/tmp/v648-approved-source-6501
V650BASE=/tmp/v650-approved-source
SRCROOT=/tmp/v6501-source
SRC="$SRCROOT/affiliate-portal-router"
FRESH=/tmp/v6501-fresh
WP=/tmp/wordpress-v6501
INSTALL="$WORK/affiliate-zentrale_v6.50.1_SAFE_GAP_STALE_PROOF_ROOTFIX_REALGATE.zip"
MASTER_DIR=/tmp/master-v6501
MASTER="$WORK/MASTER_AFFILIATE_ZENTRALE_V6_50_1_SAFE_GAP_STALE_PROOF_ROOTFIX_REALGATE_20260822.zip"
rm -rf "$E" "$PKGROOT" "$BINDROOT" "$RECON" "$V647BASE" "$V648BASE" "$V650BASE" "$SRCROOT" "$FRESH" "$WP" "$MASTER_DIR" /tmp/v649-artifact-6501
rm -f "$INSTALL" "$MASTER"
mkdir -p "$E" "$PKGROOT" "$BINDROOT" "$RECON" "$SRCROOT" "$FRESH"
block(){ echo "BLOCKED: $*" | tee "$E/BLOCKED.txt"; exit 1; }
trap 'rc=$?; if [ $rc -ne 0 ]; then echo "FINAL_DECISION=BLOCKED" > "$E/FINAL_DECISION.txt"; fi' EXIT
: "${GH_TOKEN:?GH_TOKEN required}"
V649_ART=/tmp/V649_FINAL_VERIFIED_RELEASE_6501.zip
curl -fsSL -H "Authorization: Bearer $GH_TOKEN" -H "Accept: application/vnd.github+json" "https://api.github.com/repos/hallo-netizen/affiliate-pferdeportal/actions/artifacts/9445946958/zip" -o "$V649_ART" || block "cannot retrieve verified V6.49 release artifact"
unzip -t "$V649_ART" > "$E/00_v649_artifact_zip.log" || block "V6.49 artifact ZIP invalid"
unzip -q "$V649_ART" -d /tmp/v649-artifact-6501
V649_MASTER_ZIP=/tmp/v649-artifact-6501/MASTER_AFFILIATE_ZENTRALE_V6_49_0_PUBLIC_COVERAGE_TARGET_BRIDGE_ROOTFIX_REALGATE_20260821.zip
echo '1337992a300590883549777d70444ffe76b30104a14b366955ab47411d7d3927  /tmp/v649-artifact-6501/MASTER_AFFILIATE_ZENTRALE_V6_49_0_PUBLIC_COVERAGE_TARGET_BRIDGE_ROOTFIX_REALGATE_20260821.zip' | sha256sum -c - > "$E/01_v649_master_hash.log" 2>&1 || block "binding V6.49 MASTER mismatch"
unzip -q "$V649_MASTER_ZIP" -d "$BINDROOT"
(cd "$BINDMASTER" && sha256sum -c MASTER_SHA256.txt) > "$E/02_v649_master_manifest.log" 2>&1 || block "binding V6.49 MASTER manifest mismatch"
(cd "$V649BASE" && sha256sum -c "$V649/manifests/FINAL_TREE_SHA256.txt") > "$E/03_v649_source_manifest.log" 2>&1 || block "binding V6.49 source mismatch"
test -f "$PKGZIP" || block "immutable V6.45 package missing"
echo '6695085486f38680a203c31e0b5408aee378c907a31ce65204f88ab38b9fbbf4  CODEX_V645_REALGATE_SOURCE_AND_EXACT_TASK_20260820.zip' | (cd "$WORK" && sha256sum -c -) > "$E/04_v645_package_hash.log" 2>&1 || block "V6.45 package mismatch"
unzip -q "$PKGZIP" -d "$PKGROOT"; unzip -q "$PKGZIP" -d "$RECON"
mkdir -p "$PKG/04_TESTS/V646_ROOTCAUSE"; cp "$WORK/.github/v646/tests/"*.php "$PKG/04_TESTS/V646_ROOTCAUSE/"
(cd "$RECON_PARENT" && patch -p2 --forward --batch < "$WORK/.github/v646/v646_relative.patch") > "$E/05_reconstruct_v646.log" 2>&1 || block "V6.46 reconstruction failed"
(cd "$RECON_PARENT" && sha256sum -c "$WORK/.github/v646/SOURCE_SHA256.txt") >> "$E/05_reconstruct_v646.log" 2>&1 || block "V6.46 manifest failed"
for p in 01_resolver.patch 02_recovery.patch 03_version_hook_readme.patch; do (cd "$RECON_PARENT" && patch -p0 --forward --batch < "$V647/patches/$p") >> "$E/06_reconstruct_v647.log" 2>&1 || block "V6.47 reconstruction failed"; done
(cd "$RECON_PARENT" && sha256sum -c "$V647/manifests/SOURCE_SHA256.txt") >> "$E/06_reconstruct_v647.log" 2>&1 || block "V6.47 manifest failed"
cp -a "$RECONSRC" "$V647BASE"
(cd "$RECONSRC" && patch -p0 --forward --batch < "$V648/patches/01_canonical_refresh_authority.patch") > "$E/07_reconstruct_v648.log" 2>&1 || block "V6.48 reconstruction failed"
(cd "$RECONSRC" && patch -p1 --forward --batch < "$V648/patches/02_version_readme.patch") >> "$E/07_reconstruct_v648.log" 2>&1 || block "V6.48 version patch failed"
(cd "$RECONSRC" && sha256sum -c "$V648/manifests/FINAL_TREE_SHA256.txt") >> "$E/07_reconstruct_v648.log" 2>&1 || block "V6.48 manifest failed"
cp -a "$RECONSRC" "$V648BASE"
cp -a "$V649BASE" "$V650BASE"
for pp in 01_coverage_gap_contract_core.patch 02_v649_same_uuid_gap_migration.patch 03_version_hook_readme.patch; do (cd "$V650BASE" && patch -p1 --forward --batch < "$V650/patches/$pp") >> "$E/08_reconstruct_v650.log" 2>&1 || block "V6.50 reconstruction failed at $pp"; done
(cd "$V650BASE" && sha256sum -c "$V6501/manifests/V650_MASTER_SOURCE_SHA256.txt") > "$E/09_v650_binding_master_source.log" 2>&1 || block "reconstructed V6.50 differs from binding MASTER source"
cp -a "$V650BASE" "$SRC"
run_files(){ local out="$1" src="$2"; shift 2; :>"$out"; local fail=0 count=0 assertions=0 rc f; for f in "$@"; do count=$((count+1)); echo "===== $(basename "$f") =====" >>"$out"; set +e; USE_ZEND_ALLOC=0 PPAR_TEST_PLUGIN_DIR="$src" PPAR_BASELINE_PLUGIN_DIR="$BASE" PPAR_V647_BASELINE_DIR="$V647BASE" PPAR_V648_BASELINE_DIR="$V648BASE" PPAR_V649_BASELINE_DIR="$V649BASE" PPAR_V650_BASELINE_DIR="$V650BASE" PPAR_TEST_MASTER_ROOT="$PKG" timeout 120 php "$f" >>"$out" 2>&1; rc=$?; set -e; echo "__TEST_EXIT__=$rc $(basename "$f")" >>"$out"; [ $rc -eq 0 ] || fail=$((fail+1)); done; assertions=$(grep -oE 'ASSERTIONS=[0-9]+' "$out"|cut -d= -f2|awk '{s+=$1}END{print s+0}'); echo "COUNT=$count FAIL=$fail ASSERTIONS=$assertions" | tee -a "$out"; [ $fail -eq 0 ]; }
run_dir(){ local d="$1" out="$2" src="$3"; mapfile -d '' fs < <(find "$d" -maxdepth 1 -type f -name '*.php' -print0|sort -z); run_files "$out" "$src" "${fs[@]}"; }
contract_red(){ local src="$1" out="$2"; mkdir -p "$out"; local f rc; f="$PKG/04_TESTS/V643_REGRESSION/test_canonical_full_progress_e2e_v6421.php"; set +e; PPAR_TEST_PLUGIN_DIR="$src" php "$f" > "$out/v643_canonical_old_contract.log" 2>&1; rc=$?; set -e; [ $rc -ne 0 ] && grep -Fxq 'ASSERTIONS=40 FAIL=2' "$out/v643_canonical_old_contract.log" || return 1; f="$PKG/04_TESTS/V643_REGRESSION/test_live_82_311_gapfill_v6420.php"; set +e; PPAR_TEST_PLUGIN_DIR="$src" php "$f" > "$out/v643_live82_old_contract.log" 2>&1; rc=$?; set -e; [ $rc -ne 0 ] && grep -Fxq 'ASSERTIONS=10 FAIL=3' "$out/v643_live82_old_contract.log" || return 1; f="$PKG/04_TESTS/V644_ROOTCAUSE/test_business_soft_failure_canonical_workflow_v644.php"; set +e; PPAR_TEST_PLUGIN_DIR="$src" php "$f" > "$out/v644_soft_old_contract.log" 2>&1; rc=$?; set -e; [ $rc -ne 0 ] && grep -Fxq 'ASSERTIONS=49 FAIL=2' "$out/v644_soft_old_contract.log" || return 1; echo 'OLD_CONTRACT_EXPECTED_RED=PASS' > "$out/RESULT.txt"; }
old_regression(){ local src="$1" p="$2" tmp rc; mkdir -p "$E/$p"; run_files "$E/$p/v648.log" "$src" "$V648/tests/test_canonical_component_authority_v648.php" "$V648/tests/test_canonical_refresh_negatives_v648.php" "$V648/tests/test_canonical_refresh_recovery_v648.php" "$V648/tests/test_dynamic_rule_resolver_v648.php" "$V648/tests/test_real_canonical_lifecycle_recovery_v648.php" "$V648/tests/test_real_component_save_contract_v648.php" || return 1; grep -Fxq 'COUNT=6 FAIL=0 ASSERTIONS=59' "$E/$p/v648.log" || return 1; run_files "$E/$p/v647.log" "$src" "$V647/tests/test_dynamic_rule_resolver_v647.php" "$V647/tests/test_dynamic_rule_recovery_v647.php" || return 1; grep -Fxq 'COUNT=2 FAIL=0 ASSERTIONS=22' "$E/$p/v647.log" || return 1; tmp=$(mktemp -d); find "$PKG/04_TESTS/V646_ROOTCAUSE" -maxdepth 1 -type f -name '*.php' ! -name 'test_architecture_v646.php' -exec cp {} "$tmp/" \;; run_dir "$tmp" "$E/$p/v646.log" "$src" || { rm -rf "$tmp"; return 1; }; rm -rf "$tmp"; grep -Fxq 'COUNT=3 FAIL=0 ASSERTIONS=14' "$E/$p/v646.log" || return 1; tmp=$(mktemp -d); find "$PKG/04_TESTS/V645_ROOTCAUSE" -maxdepth 1 -type f -name '*.php' ! -name 'test_architecture_v645.php' -exec cp {} "$tmp/" \;; run_dir "$tmp" "$E/$p/v645.log" "$src" || { rm -rf "$tmp"; return 1; }; rm -rf "$tmp"; grep -Fxq 'COUNT=9 FAIL=0 ASSERTIONS=67' "$E/$p/v645.log" || return 1; tmp=$(mktemp -d); find "$PKG/04_TESTS/V643_REGRESSION" -maxdepth 1 -type f -name '*.php' ! -name 'test_canonical_full_progress_e2e_v6421.php' ! -name 'test_live_82_311_gapfill_v6420.php' -exec cp {} "$tmp/" \;; run_dir "$tmp" "$E/$p/v643_unaffected.log" "$src" || { rm -rf "$tmp"; return 1; }; rm -rf "$tmp"; grep -Fxq 'COUNT=9 FAIL=0 ASSERTIONS=313' "$E/$p/v643_unaffected.log" || return 1; tmp=$(mktemp -d); find "$PKG/04_TESTS/V644_ROOTCAUSE" -maxdepth 1 -type f -name '*.php' ! -name 'test_architecture_v644.php' ! -name 'test_business_soft_failure_canonical_workflow_v644.php' -exec cp {} "$tmp/" \;; run_dir "$tmp" "$E/$p/v644_unaffected.log" "$src" || { rm -rf "$tmp"; return 1; }; rm -rf "$tmp"; grep -Fxq 'COUNT=3 FAIL=0 ASSERTIONS=21' "$E/$p/v644_unaffected.log" || return 1; contract_red "$src" "$E/$p/OLD_CONTRACT_RED" || return 1; run_files "$E/$p/v650_contract_successors.log" "$src" "$V650/tests/test_canonical_full_progress_e2e_v650_contract.php" "$V650/tests/test_live_82_311_gapfill_v650_contract.php" "$V650/tests/test_business_soft_failure_canonical_workflow_v650_contract.php" || return 1; grep -Fxq 'COUNT=3 FAIL=0 ASSERTIONS=99' "$E/$p/v650_contract_successors.log" || return 1; set +e; USE_ZEND_ALLOC=0 PPAR_TEST_PLUGIN_DIR="$src" PPAR_BASELINE_PLUGIN_DIR="$BASE" PPAR_TEST_MASTER_ROOT="$PKG" php "$PKG/04_TESTS/V644_POSTMORTEM/test_v644_release_gate_gaps.php" > "$E/$p/postmortem.log" 2>&1; rc=$?; set -e; [ $rc -ne 0 ] && [ "$(grep -c '^FAIL ' "$E/$p/postmortem.log")" -eq 2 ] || return 1; run_dir "$PKG/04_TESTS/HISTORICAL_R5_54" "$E/$p/historical.log" "$src" || return 1; grep -Fxq 'COUNT=54 FAIL=0 ASSERTIONS=3097' "$E/$p/historical.log" || return 1; }
source_gate(){ local src="$1" p="$2" stage="$3" manifest="$4"; mkdir -p "$E/$p"; (cd "$src" && sha256sum -c "$manifest") > "$E/$p/manifest.log" 2>&1 || return 1; find "$src" -type f -name '*.php' -print0|sort -z|xargs -0 -n1 php -l > "$E/$p/php_lint.log" || return 1; php -r 'foreach(array_slice($argv,1)as$f){json_decode(file_get_contents($f),true);if(json_last_error()){exit(1);}}' "$src/assets/ebay-portal-catalog-v2.json" "$src/assets/portal-structure-v279.json" || return 1; run_files "$E/$p/v649_coverage.log" "$src" "$V649/tests/test_actual_public_coverage_v649.php" || return 1; grep -Fxq 'COUNT=1 FAIL=0 ASSERTIONS=345' "$E/$p/v649_coverage.log" || return 1; run_files "$E/$p/v649_recovery.log" "$src" "$V649/tests/test_v648_same_uuid_coverage_recovery_v649.php" "$V649/tests/test_v648_live_91_311_tail_v649.php" || return 1; grep -Fxq 'COUNT=2 FAIL=0 ASSERTIONS=28' "$E/$p/v649_recovery.log" || return 1; set +e; PPAR_TEST_PLUGIN_DIR="$src" PPAR_LIVE_COVERAGE_FIXTURE="$V650/fixtures/live_v648_311_coverage_fixture.json" PPAR_EXPECT_V650_MIGRATION=1 php "$V650/tests/test_coverage_gap_contract_v650.php" > "$E/$p/v650_old_migration_contract.log" 2>&1; rc=$?; set -e; [ $rc -ne 0 ] && grep -Fxq 'ASSERTIONS=32 FAIL=5' "$E/$p/v650_old_migration_contract.log" || return 1; set +e; PPAR_TEST_PLUGIN_DIR="$src" PPAR_LIVE_COVERAGE_FIXTURE="$V650/fixtures/live_v648_311_coverage_fixture.json" PPAR_EXPECT_V650_MIGRATION=1 php "$V6501/tests/test_coverage_gap_contract_v6501.php" > "$E/$p/v6501_contract.log" 2>&1; rc=$?; set -e; [ $rc -eq 0 ] && grep -Fxq 'ASSERTIONS=41 FAIL=0' "$E/$p/v6501_contract.log" || return 1; set +e; PPAR_TEST_PLUGIN_DIR="$src" PPAR_V650_BASELINE_DIR="$V650BASE" PPAR_V6501_STAGE="$stage" php "$V6501/tests/test_architecture_v6501.php" > "$E/$p/v6501_arch.log" 2>&1; rc=$?; set -e; [ $rc -eq 0 ] || return 1; if [ "$stage" = step1 ]; then grep -Fxq 'ASSERTIONS=18 FAIL=0' "$E/$p/v6501_arch.log" || return 1; else grep -Fxq 'ASSERTIONS=20 FAIL=0' "$E/$p/v6501_arch.log" || return 1; fi; old_regression "$src" "$p" || return 1; echo SOURCE_GATE=PASS > "$E/$p/RESULT.txt"; }
(cd "$SRC" && patch -p1 --forward --batch < "$V6501/patches/01_safe_gap_stale_proof_rootfix.patch") > "$E/10_apply_rootfix.log" 2>&1 || block "V6.50.1 rootfix patch failed"
source_gate "$SRC" STEP1 step1 "$V6501/manifests/STEP1_SOURCE_SHA256.txt" || block "complete source workflow failed after rootfix"
cp "$WORK/.github/overlays/v645/soft_failure_recovery.php" "$PKG/03_REAL_GATE/soft_failure_recovery.php"
cp "$WORK/.github/v646/real/public_freshness_contract_v646.php" "$PKG/03_REAL_GATE/public_freshness_contract_v646.php"
cp "$V647/real/dynamic_rule_recovery_v647.php" "$PKG/03_REAL_GATE/dynamic_rule_recovery_v647.php"
cp "$V648/real/canonical_refresh_authority_v648.php" "$PKG/03_REAL_GATE/canonical_refresh_authority_v648.php"
cp "$V649/real/public_coverage_target_bridge_v649.php" "$PKG/03_REAL_GATE/public_coverage_target_bridge_v649.php"
cp "$V6501/real/coverage_gap_recovery_drift_v6501.php" "$PKG/03_REAL_GATE/coverage_gap_recovery_drift_v6501.php"
setup_wp_once(){ if [ ! -f "$WP/wp-load.php" ]; then mkdir -p "$WP"; wp core download --version=7.0.1 --path="$WP" --force --allow-root >/dev/null; wp config create --path="$WP" --dbname=v6501gate --dbuser=wp --dbpass=wppass --dbhost=127.0.0.1:3306 --skip-check --allow-root >/dev/null; else wp db reset --yes --path="$WP" --allow-root >/dev/null; fi; wp core install --path="$WP" --url=http://v6501.test --title='V6501 Gate' --admin_user=gateadmin --admin_password='GateOnly-20260822!' --admin_email=gate@example.invalid --skip-email --allow-root >/dev/null; }
real_gate(){ local src="$1" stage="$2" p="$3" expected_version="$4"; mkdir -p "$E/$p"; setup_wp_once; rm -rf "$WP/wp-content/plugins/affiliate-portal-router"; cp -a "$src" "$WP/wp-content/plugins/affiliate-portal-router"; wp plugin activate affiliate-portal-router --path="$WP" --allow-root >/dev/null; python3 - "$PKG/03_REAL_GATE/verify_environment.php" "$expected_version" <<'PY'
import re,sys
p=sys.argv[1];v=sys.argv[2];s=open(p).read();s=re.sub(r"Pferdeportal_Affiliate_Router::VERSION==='[0-9.]+'",f"Pferdeportal_Affiliate_Router::VERSION==='{v}'",s);s=re.sub(r"tested plugin version is [0-9.]+",f"tested plugin version is {v}",s);open(p,'w').write(s)
PY
 wp eval 'global $wpdb; echo "WP=".get_bloginfo("version")." PHP=".PHP_VERSION." DB=".$wpdb->get_var("SELECT VERSION()")." VERSION=".Pferdeportal_Affiliate_Router::VERSION."\n";' --path="$WP" --allow-root > "$E/$p/00_environment.log"; grep -Fq 'WP=7.0.1 PHP=8.4.' "$E/$p/00_environment.log" && grep -Fq 'DB=11.4.' "$E/$p/00_environment.log" && grep -Fq "VERSION=$expected_version" "$E/$p/00_environment.log" || return 1; rm -rf "$PKG/CODEX_EVIDENCE_REAL_GATE"; (cd "$PKG" && WP_ROOT="$WP" WP="$(command -v wp)" 07_RUNNERS/run_real_gate_from_existing_wordpress.sh) > "$E/$p/01_A_H.log" 2>&1 || return 1; cp -a "$PKG/CODEX_EVIDENCE_REAL_GATE" "$E/$p/A_H"; wp eval-file "$PKG/03_REAL_GATE/public_freshness_contract_v646.php" --path="$WP" --allow-root > "$E/$p/02_v646.log" 2>&1 || return 1; grep -Fxq 'PUBLIC_FRESHNESS_V646_OK' "$E/$p/02_v646.log" || return 1; wp eval-file "$PKG/03_REAL_GATE/dynamic_rule_recovery_v647.php" --path="$WP" --allow-root > "$E/$p/03_v647.log" 2>&1 || return 1; grep -Fxq 'DYNAMIC_RULE_RECOVERY_V647_OK' "$E/$p/03_v647.log" || return 1; wp eval-file "$PKG/03_REAL_GATE/canonical_refresh_authority_v648.php" --path="$WP" --allow-root > "$E/$p/04_v648.log" 2>&1 || return 1; grep -Fxq 'CANONICAL_REFRESH_AUTHORITY_V648_OK' "$E/$p/04_v648.log" || return 1; PPAR_V6501_STAGE="$stage" wp eval-file "$PKG/03_REAL_GATE/coverage_gap_recovery_drift_v6501.php" --path="$WP" --allow-root > "$E/$p/05_v6501.log" 2>&1 || return 1; grep -Fq "COVERAGE_GAP_RECOVERY_DRIFT_V6501_OK stage=$stage" "$E/$p/05_v6501.log" || return 1; echo REAL_GATE=PASS > "$E/$p/RESULT.txt"; }
real_gate "$SRC" step1 REAL_STEP1 6.50.0 || block "real WordPress/MariaDB complete workflow failed after rootfix"
python3 - "$SRC/pferdeportal-affiliate-router.php" "$SRC/readme.txt" <<'PY'
import sys
main,read=sys.argv[1:]
s=open(main).read().replace(' * Version: 6.50.0',' * Version: 6.50.1').replace("const VERSION = '6.50.0';","const VERSION = '6.50.1';").replace("6.50.0-coverage-gap-contract-rootfix-20260821","6.50.1-safe-gap-stale-proof-rootfix-20260822")
open(main,'w').write(s)
r=open(read).read();r=r.replace('Affiliate-Zentrale 6.50.0 – COVERAGE GAP CONTRACT ROOTFIX\nStable tag: 6.50.0','Affiliate-Zentrale 6.50.1 – SAFE GAP STALE PROOF ROOTFIX\nStable tag: 6.50.1\n\nKorrektur 6.50.1\n- Upgrade-Recovery verwirft veraltete abgeleitete Gap-/Selection-Beweise und berechnet die aktuelle BUSINESS-Coverage im bestehenden kanonischen Workflow neu.\n- Gleiche Run-UUID und Upstream-Quellenbelege bleiben erhalten; Qualitäts-, Sicherheits-, PRIVATE- und Providerregeln bleiben unverändert.')
open(read,'w').write(r)
PY
(cd "$SRC" && find . -type f -print0|sort -z|xargs -0 sha256sum) > "$E/11_FINAL_SOURCE_SHA256.txt"
source_gate "$SRC" FINAL_SOURCE final "$E/11_FINAL_SOURCE_SHA256.txt" || block "complete source workflow failed after release metadata"
real_gate "$SRC" final REAL_FINAL 6.50.1 || block "real WordPress/MariaDB complete workflow failed after release metadata"
mapfile -t changed < <(diff -qr "$V650BASE" "$SRC" | sed -E 's#^Files .*/affiliate-portal-router/([^ ]+) and .* differ$#\1#' | sort); printf '%s\n' "${changed[@]}" > "$E/12_changed_files_v650_to_v6501.txt"; test "$(printf '%s\n' "${changed[@]}")" = $'includes/trait-ppar-ebay-run.php\npferdeportal-affiliate-router.php\nreadme.txt' || block "production scope is not exactly three files"; diff -ruN "$V650BASE" "$SRC" > "$E/13_v650_to_v6501.diff" || true
(cd "$SRCROOT" && zip -qr "$INSTALL" affiliate-portal-router); unzip -t "$INSTALL" > "$E/14_install_integrity_before.log" || block "installer ZIP invalid"; sha256sum "$INSTALL" > "$E/15_install_sha256_before.txt"; unzip -q "$INSTALL" -d "$FRESH"; (cd "$SRC" && find . -type f -print0|sort -z|xargs -0 sha256sum) > "$E/16_source_tree.sha"; (cd "$FRESH/affiliate-portal-router" && find . -type f -print0|sort -z|xargs -0 sha256sum) > "$E/17_fresh_tree.sha"; diff -u "$E/16_source_tree.sha" "$E/17_fresh_tree.sha" > "$E/18_source_vs_fresh.diff" || block "Fresh-Unpack differs from approved source"; source_gate "$FRESH/affiliate-portal-router" FINAL_ZIP_SOURCE final "$E/11_FINAL_SOURCE_SHA256.txt" || block "complete source workflow failed against Fresh-Unpack"; real_gate "$FRESH/affiliate-portal-router" final FINAL_ZIP_REAL 6.50.1 || block "real WordPress/MariaDB workflow failed against Fresh-Unpack"; wp plugin status affiliate-portal-router --path="$WP" --allow-root > "$E/19_final_plugin_status.log"; grep -Fq 'Status: Active' "$E/19_final_plugin_status.log" && grep -Fq 'Version: 6.50.1' "$E/19_final_plugin_status.log" || block "final ZIP activation/version failed"
setup_wp_once; rm -rf "$WP/wp-content/plugins/affiliate-portal-router"; cp -a "$FRESH/affiliate-portal-router" "$WP/wp-content/plugins/affiliate-portal-router"; wp plugin activate affiliate-portal-router --path="$WP" --allow-root >/dev/null; PPAR_V6501_STAGE=final wp eval-file "$PKG/03_REAL_GATE/coverage_gap_recovery_drift_v6501.php" --path="$WP" --allow-root > "$E/20_postgreen_drift_counterproof.log" 2>&1 || block "post-green drift counterproof failed"; grep -Fq 'COVERAGE_GAP_RECOVERY_DRIFT_V6501_OK stage=final' "$E/20_postgreen_drift_counterproof.log" || block "post-green marker missing"; unzip -t "$INSTALL" > "$E/21_install_integrity_after.log"; sha256sum "$INSTALL" > "$E/22_install_sha256_after.txt"; diff -u "$E/15_install_sha256_before.txt" "$E/22_install_sha256_after.txt" > "$E/23_install_hash_stability.diff" || block "installer changed during final tests"
cat > "$E/REAL_GATE_FINAL_MATRIX.txt" <<'EOF'
Binding V6.50 MASTER source byte identity: PASS
Step 1 recovery rootfix complete source/historical workflow: PASS
Step 1 WordPress 7.0.1 / PHP 8.4 / MariaDB 11.4 complete workflow: PASS
Step 2 version/readme complete source/historical workflow: PASS
Step 2 WordPress 7.0.1 / PHP 8.4 / MariaDB 11.4 complete workflow: PASS
Fresh-Unpack source parity and complete source/historical workflow: PASS
Fresh-Unpack WordPress/MariaDB complete workflow: PASS
Independent post-green migration+time-drift counterproof: PASS
Historical R5 54/54 · 3097 assertions per stage: PASS
V6.49 public coverage 345 + recovery 28 assertions per stage: PASS
V6.48 6/6 · 59; V6.47 2/2 · 22; V6.46 3/3 · 14; V6.45 9/9 · 67: PASS
V6.43 unaffected 9/9 · 313; V6.44 unaffected 3/3 · 21: PASS
Old terminal REDs 40/2 + 10/3 + 49/2 reproduced: PASS
V6.50 successor contract 3/3 · 99 assertions per stage: PASS
Old V6.50 stale migration expectation exact RED 32/5 reproduced: PASS
V6.50.1 migration+drift contract 41/41 per stage: PASS
Real A-H incl PRIVATE/retry/resume/concurrency per stage: PASS
Selected-winner missing-public invariant remains hard fail: PASS
Installer hash stability: PASS
Production scope V6.50 -> V6.50.1 exactly 3 files: PASS
External eBay production-live E2E after V6.50.1 install: OPEN_NOT_CLAIMED
main changed/merged: NO
EOF
cat > "$E/FEHLERKATALOG_V6_50_1.md" <<'EOF'
# FEHLERKATALOG V6.50.1
V6.50 wurde live durch `business_safe_gap_new_missing_family` widerlegt. Ursache: die V6.49→V6.50 Upgrade-Recovery übernahm einen alten terminalen Gap-/Selection-Beweis und sprang direkt zu `public_verify`. Bei zeitlich veränderter BUSINESS-Coverage konnte die Familienmenge trotz gleicher 91/311-Zahl abweichen.
V6.50.1 korrigiert ausschließlich diesen bestehenden Recovery-Pfad: gleiche UUID und Upstream-Quellenbelege bleiben, abgeleitete Discovery-/Selection-/Coverage-/Gapfill-Beweise werden verworfen, danach wird im bestehenden `coverage_verify` und maximal einem bestehenden kanonischen Gapfill neu geprüft. Keine Qualitäts-, Sicherheits-, PRIVATE-, Awin-, Provider-, Design- oder Contentregel wurde geändert.
Die bisherige Prüflücke wurde geschlossen: Migration und Zeitdrift werden jetzt zusammen getestet. Der alte V6.50-Migrationstest bleibt unverändert als exakter RED-Gegenbeweis (32 Assertions / 5 alte Erwartungen rot).
EOF
cat > "$E/ARBEITSPROTOKOLL_V6_50_1.md" <<'EOF'
# ARBEITSPROTOKOLL V6.50.1
1. Bindende V6.50 MASTER vollständig geprüft und deren Source als alleinige Baseline festgelegt.
2. Live-V6.50-Fehler `business_safe_gap_new_missing_family` gegen Recovery→Coverage→Gapfill→Public-Verify vollständig zurückverfolgt.
3. Rootfix nur im bestehenden Recovery-Pfad. Danach kompletter Source-/Historienworkflow und kompletter WP/MariaDB-Workflow.
4. Danach ausschließlich Version/Build/README auf 6.50.1. Danach kompletter Workflow erneut.
5. Installer erst danach gebaut; Fresh-Unpack byteidentisch geprüft; kompletter Workflow erneut gegen Fresh-Unpack.
6. Unabhängiger Migration+Zeitdrift-Gegenbeweis nach allen Gates wiederholt.
7. main nicht verändert/merged. Arbeitsbranch v6501-safe-gap-stale-proof-rootcause-20260821, Draft PR #7.
EOF
cat > "$E/FINAL_DECISION.txt" <<'EOF'
FINAL_DECISION=LOCAL_AND_REAL_WORKFLOW_PASS_LIVE_E2E_OPEN
VERSION=6.50.1
INSTALLER=affiliate-zentrale_v6.50.1_SAFE_GAP_STALE_PROOF_ROOTFIX_REALGATE.zip
MASTER=MASTER_AFFILIATE_ZENTRALE_V6_50_1_SAFE_GAP_STALE_PROOF_ROOTFIX_REALGATE_20260822.zip
LIVE_EBAY_E2E=OPEN_NOT_CLAIMED
EOF
rm -rf "$MASTER_DIR"; mkdir -p "$MASTER_DIR/master-v6501"/{00_READ_ME_FIRST,01_MASTER_BINDING,02_INSTALL,03_SOURCE,04_TESTS_AND_REALGATE,05_REPORT,06_WORKLOG,07_ERROR_CATALOG,08_GITHUB,09_DIFF_AND_HASHES}; M="$MASTER_DIR/master-v6501"; cp "$V650/HARTER_GESAMTWORKFLOW_PRUEFVERTRAG.md" "$M/01_MASTER_BINDING/HARTER_PRUEF_BUILD_UND_FREIGABEVERTRAG.md"; cat > "$M/01_MASTER_BINDING/V650_BINDING_REFERENCE.txt" <<'EOF'
Binding predecessor MASTER: MASTER_AFFILIATE_ZENTRALE_V6_50_0_COVERAGE_GAP_CONTRACT_ROOTFIX_REALGATE_20260821.zip
Binding authority: exact V6.50 MASTER source manifest included in this release evidence.
Priority: MASTER > current source > evidenced GitHub history > chat > assumption.
V6.50 live release status: FAIL / superseded only by this tested rootfix.
EOF
cp "$INSTALL" "$M/02_INSTALL/"; cp -a "$SRC" "$M/03_SOURCE/affiliate-portal-router"; cp -a "$E/." "$M/04_TESTS_AND_REALGATE/"; cp "$E/REAL_GATE_FINAL_MATRIX.txt" "$M/05_REPORT/RELEASE_REPORT.md"; cp "$E/ARBEITSPROTOKOLL_V6_50_1.md" "$M/06_WORKLOG/"; cp "$E/FEHLERKATALOG_V6_50_1.md" "$M/07_ERROR_CATALOG/"; cat > "$M/08_GITHUB/GITHUB_RELEASE_GATE.md" <<EOF
Arbeitsbranch: v6501-safe-gap-stale-proof-rootcause-20260821
PR: #7 Draft / nicht gemergt
Workflow SHA: ${GITHUB_SHA:-local}
main verändert/merged: NEIN
EOF
cp "$E/12_changed_files_v650_to_v6501.txt" "$E/13_v650_to_v6501.diff" "$E/15_install_sha256_before.txt" "$E/22_install_sha256_after.txt" "$E/11_FINAL_SOURCE_SHA256.txt" "$M/09_DIFF_AND_HASHES/"; cp "$E/REAL_GATE_FINAL_MATRIX.txt" "$M/00_READ_ME_FIRST/"; cat > "$M/00_READ_ME_FIRST/INSTALLATION_FREIGEGEBEN.txt" <<'EOF'
V6.50.1
LOKALER + ISOLIERTER REALER GESAMTWORKFLOW PASS – EXTERNER LIVE-eBay-E2E NOCH OFFEN.
Installationsdatei: affiliate-zentrale_v6.50.1_SAFE_GAP_STALE_PROOF_ROOTFIX_REALGATE.zip
EOF
(cd "$M" && find . -type f ! -name 'MASTER_SHA256.txt' ! -name 'MASTER_MANIFEST_VERIFIED.txt' -print0|sort -z|xargs -0 sha256sum) > "$M/MASTER_SHA256.txt"; (cd "$M" && sha256sum -c MASTER_SHA256.txt) > "$M/MASTER_MANIFEST_VERIFIED.txt" || block "MASTER internal manifest failed"; (cd "$MASTER_DIR" && zip -qr "$MASTER" master-v6501); unzip -t "$MASTER" > "$E/24_master_zip_integrity.log" || block "MASTER ZIP invalid"; sha256sum "$MASTER" > "$E/25_master_sha256.txt"; rm -rf /tmp/master-v6501-fresh; mkdir -p /tmp/master-v6501-fresh; unzip -q "$MASTER" -d /tmp/master-v6501-fresh; (cd /tmp/master-v6501-fresh/master-v6501 && sha256sum -c MASTER_SHA256.txt) > "$E/26_master_fresh_manifest.log" 2>&1 || block "fresh MASTER manifest failed"; (cd /tmp/master-v6501-fresh/master-v6501/03_SOURCE/affiliate-portal-router && find . -type f -print0|sort -z|xargs -0 sha256sum) > "$E/27_master_source.sha"; diff -u "$E/16_source_tree.sha" "$E/27_master_source.sha" > "$E/28_master_source_parity.diff" || block "MASTER embedded source differs"; rm -rf /tmp/v6501-embedded; mkdir -p /tmp/v6501-embedded; unzip -q /tmp/master-v6501-fresh/master-v6501/02_INSTALL/affiliate-zentrale_v6.50.1_SAFE_GAP_STALE_PROOF_ROOTFIX_REALGATE.zip -d /tmp/v6501-embedded; (cd /tmp/v6501-embedded/affiliate-portal-router && find . -type f -print0|sort -z|xargs -0 sha256sum) > "$E/29_embedded_installer.sha"; diff -u "$E/16_source_tree.sha" "$E/29_embedded_installer.sha" > "$E/30_embedded_installer_parity.diff" || block "MASTER installer differs"; sha256sum "$INSTALL" > "$E/31_final_install_sha256.txt"; diff -u "$E/22_install_sha256_after.txt" "$E/31_final_install_sha256.txt" > "$E/32_final_install_hash_stability.diff" || block "installer changed after MASTER build"; echo FINAL_RELEASE_GATE=PASS > "$E/33_FINAL_RELEASE_GATE.txt"
