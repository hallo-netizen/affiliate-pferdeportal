#!/usr/bin/env bash
set -euo pipefail

WORK="${GITHUB_WORKSPACE:-$(pwd)}"
ART="$WORK/V645_FINAL_ARTIFACT"
E="$WORK/V645_COUNTERPROOF_EVIDENCE"
PKGZIP="$WORK/CODEX_V645_REALGATE_SOURCE_AND_EXACT_TASK_20260820.zip"
PKGROOT=/tmp/v645-counterproof-pkg/CODEX_V645_REALGATE_SOURCE_AND_EXACT_TASK_20260820
INSTALL="$ART/affiliate-zentrale_v6.45.0_CANONICAL_RUN_PERSISTENCE_RACE_ROOTFIX_REALGATE.zip"
MASTER="$ART/MASTER_AFFILIATE_ZENTRALE_V6_45_0_CANONICAL_RUN_PERSISTENCE_RACE_ROOTFIX_REALGATE_20260820.zip"
EXPECTED_INSTALL_SHA=591a029a2ec72c4e55b42bd82bff9e796bd1ac3b4ac0a974220d122d9bdd3c06
EXPECTED_MASTER_SHA=7f58aaaab1ce95fead62540b97fd535fd68eba7ed00940f41217497fab1c034e
WP=/tmp/wordpress-v645-counterproof
INSTALL_UNPACK=/tmp/v645-counterproof-install
MASTER_UNPACK=/tmp/v645-counterproof-master

rm -rf "$E" /tmp/v645-counterproof-pkg "$WP" "$INSTALL_UNPACK" "$MASTER_UNPACK"
mkdir -p "$E" /tmp/v645-counterproof-pkg "$INSTALL_UNPACK" "$MASTER_UNPACK"

cat > "$E/COUNTERPROOF_PLAN.md" <<'EOF'
# V6.45 post-release counterproof

This run intentionally tries to falsify the already-green release candidate AFTER the complete release workflow succeeded.

Realistic adversarial cases exercised again against the exact final installer:
1. persisted 311-family resume across many bounded worker ticks;
2. no-progress / hard-limit termination;
3. stale whole-run CAS after newer persisted state exists;
4. soft-failure recovery with same run UUID and preserved immutable config snapshot;
5. corrupted missing-snapshot state must fail closed with selection_scope_empty;
6. five-way concurrent lease acquisition must produce exactly one winner;
7. five-way concurrent worker burst must not duplicate canonical progress;
8. persisted checkpoint must resume monotonically to completion;
9. complete historical/source regression is rerun before the real counterproof;
10. exact final installer and MASTER remain byte/hash stable and mutually identical where required.

Any failure means BLOCKED. No production source or installer is modified by this workflow.
EOF

# Exact release artifact identity from the successful final-release run.
test -f "$INSTALL"
test -f "$MASTER"
actual_install=$(sha256sum "$INSTALL" | awk '{print $1}')
actual_master=$(sha256sum "$MASTER" | awk '{print $1}')
test "$actual_install" = "$EXPECTED_INSTALL_SHA"
test "$actual_master" = "$EXPECTED_MASTER_SHA"
printf 'INSTALL_SHA=%s\nMASTER_SHA=%s\n' "$actual_install" "$actual_master" > "$E/exact_release_hashes.txt"
unzip -t "$INSTALL" > "$E/install_integrity.txt"
unzip -t "$MASTER" > "$E/master_integrity.txt"

# Reconstruct only the immutable test package; production plugin bytes come from the exact final installer.
unzip -q "$PKGZIP" -d /tmp/v645-counterproof-pkg
cp "$WORK/.github/overlays/v645/soft_failure_recovery.php" "$PKGROOT/03_REAL_GATE/soft_failure_recovery.php"
unzip -q "$INSTALL" -d "$INSTALL_UNPACK"
rm -rf "$PKGROOT/02_SOURCE_V645/affiliate-portal-router"
cp -a "$INSTALL_UNPACK/affiliate-portal-router" "$PKGROOT/02_SOURCE_V645/affiliate-portal-router"
(cd "$PKGROOT/02_SOURCE_V645" && sha256sum -c SOURCE_SHA256.txt) > "$E/final_installer_matches_release_source.txt"

# Full source + historical regression AGAIN, now after final release success.
(cd "$PKGROOT" && 07_RUNNERS/run_source_gates.sh) > "$E/source_gates_counterproof.log" 2>&1
cp -a "$PKGROOT/CODEX_EVIDENCE_SOURCE" "$E/SOURCE_EVIDENCE"
grep -Fxq 'COUNT=10 FAIL=0 ASSERTIONS=78' "$E/SOURCE_EVIDENCE/04_v645_rootcause.log"
grep -Fxq 'COUNT=11 FAIL=0 ASSERTIONS=363' "$E/SOURCE_EVIDENCE/05_v643_regression.log"
grep -Fxq 'COUNT=4 FAIL=0 ASSERTIONS=70' "$E/SOURCE_EVIDENCE/06_v644_functional.log"
grep -Fxq 'POSTMORTEM_DIAGNOSTIC_EXPECTED_GAP_CONFIRMED' "$E/SOURCE_EVIDENCE/07_v644_postmortem_gap_diagnostic.log"
grep -Fxq 'COUNT=54 FAIL=0 ASSERTIONS=3097' "$E/SOURCE_EVIDENCE/08_historical_r5.log"

# Fresh WordPress 7.0.1 and MariaDB 11.4, install EXACT final ZIP.
rm -rf "$WP" && mkdir -p "$WP"
wp core download --version=7.0.1 --path="$WP" --force --allow-root > "$E/wp_setup.log" 2>&1
wp config create --path="$WP" --dbname=v645counter --dbuser=wp --dbpass=wppass --dbhost=127.0.0.1:3306 --skip-check --allow-root >> "$E/wp_setup.log" 2>&1
wp core install --path="$WP" --url=http://v645counter.test --title='V645 Counterproof' --admin_user=gateadmin --admin_password='GateOnly-20260820!' --admin_email=gate@example.invalid --skip-email --allow-root >> "$E/wp_setup.log" 2>&1
wp plugin install "$INSTALL" --activate --path="$WP" --allow-root >> "$E/wp_setup.log" 2>&1
wp plugin status affiliate-portal-router --path="$WP" --allow-root > "$E/plugin_status.log"
grep -Fq 'Status: Active' "$E/plugin_status.log"
grep -Fq 'Version: 6.45.0' "$E/plugin_status.log"

# Explicit post-success counterproof: full real A-H AGAIN against exact final installer.
(cd "$PKGROOT" && WP_ROOT="$WP" WP="$(command -v wp)" 07_RUNNERS/run_real_gate_from_existing_wordpress.sh) > "$E/real_counterproof.log" 2>&1
cp -a "$PKGROOT/CODEX_EVIDENCE_REAL_GATE" "$E/REAL_EVIDENCE"
grep -Fq 'ENVIRONMENT_OK WP=7.0.1 PHP=8.4.' "$E/REAL_EVIDENCE/01-verify_environment.php.log"
grep -Fq 'DB=11.4.' "$E/REAL_EVIDENCE/01-verify_environment.php.log"
grep -Fq 'LIVE800_OK ticks=39 transport=839 cursor=311' "$E/REAL_EVIDENCE/02-live800_resume.php.log"
grep -Fxq 'NEGATIVE_LIMITS_OK' "$E/REAL_EVIDENCE/03-negative_limits.php.log"
grep -Fxq 'STALE_CAS_OK' "$E/REAL_EVIDENCE/04-stale_cas.php.log"
grep -Fq 'missing immutable seller-route snapshot fails closed with concrete selection_scope_empty code' "$E/REAL_EVIDENCE/05-soft_failure_recovery.php.log"
grep -Fxq 'SOFT_RECOVERY_OK' "$E/REAL_EVIDENCE/05-soft_failure_recovery.php.log"
grep -Fq 'CONCURRENT_LEASE_OK acquired=1 rejected=4' "$E/REAL_EVIDENCE/08_assert_concurrent.log"
grep -Fq 'CONCURRENT_TICK_BURST_OK acquired=1 transport=1 cursor=8' "$E/REAL_EVIDENCE/11_assert_tick_burst.log"
grep -Fq 'CHECKPOINT_RESUME_OK start_transport=1 added=38 final_transport=39' "$E/REAL_EVIDENCE/12-continue_concurrent_checkpoint.php.log"
grep -Fxq 'DB_SANITY_PASS' "$E/REAL_EVIDENCE/13_db_sanity.log"

# Re-prove exact final MASTER and embedded installer identity AFTER the counterproof.
unzip -q "$MASTER" -d "$MASTER_UNPACK"
MR=$(find "$MASTER_UNPACK" -mindepth 1 -maxdepth 1 -type d | head -n1)
(cd "$MR" && sha256sum -c MASTER_SHA256.txt) > "$E/master_manifest_after_counterproof.txt"
EMBED=$(find "$MR/02_INSTALL" -maxdepth 1 -type f -name '*.zip' | head -n1)
cmp -s "$INSTALL" "$EMBED"
sha256sum "$INSTALL" "$EMBED" > "$E/embedded_installer_after_counterproof.txt"
test "$(sha256sum "$INSTALL" | awk '{print $1}')" = "$EXPECTED_INSTALL_SHA"
test "$(sha256sum "$MASTER" | awk '{print $1}')" = "$EXPECTED_MASTER_SHA"

cat > "$E/COUNTERPROOF_RESULT.txt" <<'EOF'
COUNTERPROOF=PASS
FULL_SOURCE_AND_HISTORICAL_REGRESSION=PASS
EXACT_FINAL_INSTALLER_REAL_A_H=PASS
STALE_CAS_COUNTEREXAMPLE=REJECTED
NO_PROGRESS_COUNTEREXAMPLE=REJECTED
SOFT_RECOVERY_COUNTEREXAMPLE=REJECTED
MISSING_SNAPSHOT_FAIL_CLOSED=PASS
FIVE_WAY_LEASE_RACE=PASS
FIVE_WAY_WORKER_BURST=PASS
CHECKPOINT_RESUME=PASS
FINAL_INSTALLER_HASH_STABLE=PASS
FINAL_MASTER_MANIFEST=PASS
MASTER_EMBEDDED_INSTALLER_IDENTICAL=PASS
PRODUCTION_SOURCE_CHANGED=NO
EOF

echo V645_POSTRELEASE_COUNTERPROOF_OK
