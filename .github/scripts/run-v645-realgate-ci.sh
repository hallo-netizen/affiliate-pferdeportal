#!/usr/bin/env bash
set -u -o pipefail

WORK="${GITHUB_WORKSPACE:-$(pwd)}"
E="$WORK/V645_EVIDENCE"
ZIP="$WORK/CODEX_V645_REALGATE_SOURCE_AND_EXACT_TASK_20260820.zip"
UNPACK=/tmp/v645pkg
PKG="$UNPACK/CODEX_V645_REALGATE_SOURCE_AND_EXACT_TASK_20260820"
WP_ROOT=/tmp/wordpress-v645
mkdir -p "$E"

SRC_RC=NOT_RUN
REAL_RC=NOT_RUN
FINAL_REASON="uninitialized"

write_final() {
  local decision
  if [ "$SRC_RC" = "0" ] && [ "$REAL_RC" = "0" ]; then
    decision="REAL-GATE-EVIDENCE VOLLSTAENDIG – NO INSTALL RELEASE YET"
  else
    decision="BLOCKED – NICHT INSTALLIEREN"
  fi
  cat > "$E/FINAL_DECISION.md" <<EOF
# V6.45 isolated real-gate result

**$decision**

Source-gate exit: $SRC_RC
Real-gate exit: $REAL_RC
Reason: $FINAL_REASON

No production source was modified by this runner. No install ZIP was built.
EOF
}

finalize() {
  set +e
  if [ -d "$PKG/02_SOURCE_V645" ]; then
    (cd "$PKG/02_SOURCE_V645" && sha256sum -c SOURCE_SHA256.txt) > "$E/source_sha256_after.txt" 2>&1
    echo $? > "$E/source_sha256_after_exitcode.txt"
  fi
  write_final
  cd "$WORK" || return
  rm -f CODEX_V645_REALGATE_EVIDENCE_GHA_20260820.zip
  zip -qr CODEX_V645_REALGATE_EVIDENCE_GHA_20260820.zip V645_EVIDENCE
  unzip -t CODEX_V645_REALGATE_EVIDENCE_GHA_20260820.zip > "$E/evidence_zip_integrity.txt" 2>&1
  sha256sum CODEX_V645_REALGATE_EVIDENCE_GHA_20260820.zip > "$E/evidence_zip_sha256.txt"
}
trap finalize EXIT

block() {
  FINAL_REASON="$1"
  echo "BLOCKED: $FINAL_REASON" | tee -a "$E/block_reason.txt"
  exit 1
}

# Immutable package + exact source identity.
[ -f "$ZIP" ] || block "V6.45 package missing"
unzip -t "$ZIP" > "$E/package_unzip_test.txt" 2>&1 || block "package archive integrity failed"
sha256sum "$ZIP" > "$E/package_sha256.txt"
rm -rf "$UNPACK" && mkdir -p "$UNPACK"
unzip -q "$ZIP" -d "$UNPACK" || block "package unpack failed"
[ -d "$PKG/02_SOURCE_V645/affiliate-portal-router" ] || block "exact V6.45 source directory missing"
(
  cd "$PKG/02_SOURCE_V645" && sha256sum -c SOURCE_SHA256.txt
) | tee "$E/source_sha256_before.txt"
[ "${PIPESTATUS[0]}" -eq 0 ] || block "source SHA256 identity failed before tests"

# Mandatory source / historical regression gate.
set +e
(
  cd "$PKG" && 07_RUNNERS/run_source_gates.sh
) > "$E/source_gates_console.log" 2>&1
SRC_RC=$?
set -e
printf '%s\n' "$SRC_RC" > "$E/source_gates_exitcode.txt"
cp -a "$PKG/CODEX_EVIDENCE_SOURCE" "$E/" 2>/dev/null || true

# Correct historical assertion accounting: MASTER says 3116 canonical assertions.
# The legacy runner can only sum 3097 explicit ASSERTIONS footers because three
# historical tests omit that footer; those three contain 19 implicit checks.
{
  echo "MASTER_CANONICAL_ASSERTIONS=3116"
  if [ -f "$E/CODEX_EVIDENCE_SOURCE/08_historical_r5.log" ]; then
    raw=$(grep -oE 'ASSERTIONS=[0-9]+' "$E/CODEX_EVIDENCE_SOURCE/08_historical_r5.log" | cut -d= -f2 | awk '{s+=$1} END{print s+0}')
    echo "EXPLICIT_ASSERTION_FOOTER_SUM=$raw"
  fi
  echo "LEGACY_IMPLICIT_ASSERTIONS=19"
  echo "EXPECTED_EXPLICIT_PLUS_IMPLICIT=3116"
  echo "NOTE=Accounting only. No historical assertion is removed, weakened, or reinterpreted."
} > "$E/historical_assertion_accounting.txt"

if [ "$SRC_RC" -ne 0 ]; then
  # Diagnostic only: do not turn a failure into PASS. Re-run the six known
  # <5s planner checks against the unchanged V6.44 baseline on the SAME runner.
  T="$PKG/04_TESTS/HISTORICAL_R5_54"
  B="$PKG/05_BASELINE_V644/affiliate-portal-router"
  O="$E/v644_baseline_perf_diagnostic.log"
  : > "$O"
  files=(
    test_full_catalog_article_products_v636.php
    test_business_all_311_three_plan.php
    test_full_catalog_real_titles_v638.php
    test_business_all_311_three_plan_v620.php
    test_full_catalog_two_phase_e2e.php
    test_full_catalog_public_coverage.php
  )
  for f in "${files[@]}"; do
    echo "===== $f =====" >> "$O"
    set +e
    PPAR_TEST_PLUGIN_DIR="$B" PPAR_BASELINE_PLUGIN_DIR="$B" PPAR_TEST_MASTER_ROOT="$PKG" timeout 180 php "$T/$f" >> "$O" 2>&1
    rc=$?
    set -e
    echo "__BASELINE_EXIT__ $rc $f" >> "$O"
  done
  block "mandatory source/historical gate failed; real DB gate intentionally not started"
fi

# Real environment proof BEFORE WordPress setup.
{
  uname -a
  php -v
  php -m
  wp --info
  php -r '$m=new mysqli("127.0.0.1","wp","wppass","v645gate",3306); if($m->connect_errno){fwrite(STDERR,$m->connect_error."\n"); exit(1);} echo "DB_CLIENT_SERVER_INFO=".$m->server_info."\n"; $r=$m->query("SELECT VERSION() v")->fetch_assoc(); echo "DB_SELECT_VERSION=".$r["v"]."\n";'
} > "$E/ENVIRONMENT_PRE_WP.txt" 2>&1 || block "real MariaDB/mysqli environment not usable"

# Fresh isolated WordPress 7.0.1 + exact V6.45 source.
rm -rf "$WP_ROOT" && mkdir -p "$WP_ROOT"
set +e
{
  wp core download --version=7.0.1 --path="$WP_ROOT" --force --allow-root
  wp config create --path="$WP_ROOT" --dbname=v645gate --dbuser=wp --dbpass=wppass --dbhost=127.0.0.1:3306 --skip-check --allow-root
  wp core install --path="$WP_ROOT" --url=http://v645.test --title='V645 Real Gate' --admin_user=gateadmin --admin_password='GateOnly-20260820!' --admin_email=gate@example.invalid --skip-email --allow-root
  rm -rf "$WP_ROOT/wp-content/plugins/affiliate-portal-router"
  cp -a "$PKG/02_SOURCE_V645/affiliate-portal-router" "$WP_ROOT/wp-content/plugins/affiliate-portal-router"
  wp plugin activate affiliate-portal-router --path="$WP_ROOT" --allow-root
} > "$E/wp_setup.log" 2>&1
wp_rc=$?
set -e
[ "$wp_rc" -eq 0 ] || block "fresh WordPress 7.0.1 / plugin activation failed"

{
  echo "WORDPRESS_VERSION=$(wp core version --path="$WP_ROOT" --allow-root)"
  echo "PHP_VERSION=$(php -r 'echo PHP_VERSION;')"
  echo "MYSQLI_LOADED=$(php -r 'echo extension_loaded("mysqli")?"yes":"no";')"
  wp eval 'global $wpdb; echo "DB_VERSION=".$wpdb->get_var("SELECT VERSION()")."\n"; echo "OPTIONS_TABLE=".$wpdb->options."\n";' --path="$WP_ROOT" --allow-root
  wp plugin status affiliate-portal-router --path="$WP_ROOT" --allow-root
} > "$E/ENVIRONMENT.txt" 2>&1 || block "post-install environment proof failed"

# Exact real-gate A-H; no mocks/stubs/SQLite and no production system.
set +e
(
  cd "$PKG" && WP_ROOT="$WP_ROOT" WP="$(command -v wp)" 07_RUNNERS/run_real_gate_from_existing_wordpress.sh
) > "$E/real_gate_console.log" 2>&1
REAL_RC=$?
set -e
printf '%s\n' "$REAL_RC" > "$E/real_gate_exitcode.txt"
cp -a "$PKG/CODEX_EVIDENCE_REAL_GATE" "$E/" 2>/dev/null || true
[ "$REAL_RC" -eq 0 ] || block "real WordPress/MariaDB gate A-H failed"

# Final DB/plugin sanity independent of the runner's own final checks.
{
  wp eval 'global $wpdb; $v=$wpdb->get_var("SELECT 1"); if((string)$v!=="1"){fwrite(STDERR,"DB_SANITY_FAIL\n"); exit(1);} echo "DB_SANITY_PASS\n";' --path="$WP_ROOT" --allow-root
  wp plugin status affiliate-portal-router --path="$WP_ROOT" --allow-root
  wp eval '$r=get_option(Pferdeportal_Affiliate_Router::OPTION_EBAY_RUN_STATE,array()); echo wp_json_encode($r,JSON_PRETTY_PRINT|JSON_UNESCAPED_SLASHES)."\n";' --path="$WP_ROOT" --allow-root > "$E/final_run_state.json"
} > "$E/final_sanity.log" 2>&1 || block "independent final DB/plugin sanity failed"

FINAL_REASON="all mandatory source gates and real gates A-H executed successfully; evidence only, no installation release"
exit 0
