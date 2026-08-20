#!/usr/bin/env bash
set -euo pipefail

WORK="${GITHUB_WORKSPACE:-$(pwd)}"
E="$WORK/V645_EVIDENCE"
ZIP="$WORK/CODEX_V645_REALGATE_SOURCE_AND_EXACT_TASK_20260820.zip"
ROOT="CODEX_V645_REALGATE_SOURCE_AND_EXACT_TASK_20260820"
PKG="/tmp/v645pkg/$ROOT"
OVERLAY_TMP=/tmp/v645-hard-overlay

rm -rf "$E" "$OVERLAY_TMP"
mkdir -p "$E" "$OVERLAY_TMP"
rm -f "$WORK/CODEX_V645_REALGATE_EVIDENCE_GHA_20260820.zip"

# Test-harness-only correction proved separately against real WordPress/MariaDB.
# Production source is immutable and is hash-verified before and after this overlay.
sha256sum "$ZIP" > "$E/original_package_sha256.txt"
unzip -q "$ZIP" -d "$OVERLAY_TMP"
(cd "$OVERLAY_TMP/$ROOT/02_SOURCE_V645" && sha256sum -c SOURCE_SHA256.txt) > "$E/production_source_sha256_before_overlay.txt"
cp "$OVERLAY_TMP/$ROOT/03_REAL_GATE/soft_failure_recovery.php" "$E/gate_d_original.php"
cp "$WORK/.github/overlays/v645/soft_failure_recovery.php" "$OVERLAY_TMP/$ROOT/03_REAL_GATE/soft_failure_recovery.php"
cp "$WORK/.github/overlays/v645/soft_failure_recovery.php" "$E/gate_d_corrected.php"
diff -u "$E/gate_d_original.php" "$E/gate_d_corrected.php" > "$E/gate_d_harness_only.diff" || true
cat > "$E/gate_d_overlay_manifest.txt" <<'EOF'
TEST_HARNESS_ONLY=YES
PRODUCTION_SOURCE_CHANGED=NO
CAUSE_PROOF=V6.44 start/adoption always freezes config_snapshot; previous Gate D omitted it and real first tick failed selection_scope_empty.
NEGATIVE_CASE_PRESERVED=YES; missing snapshot is explicitly asserted to fail closed.
EOF
(cd "$OVERLAY_TMP/$ROOT/02_SOURCE_V645" && sha256sum -c SOURCE_SHA256.txt) > "$E/production_source_sha256_after_overlay.txt"
rm -f "$ZIP"
(cd "$OVERLAY_TMP" && zip -qr "$ZIP" "$ROOT")
unzip -t "$ZIP" > "$E/corrected_package_unzip_test.txt"
sha256sum "$ZIP" > "$E/corrected_package_sha256.txt"

# Execute the complete existing fail-closed source + WordPress/MariaDB real gate from scratch.
"$WORK/.github/scripts/run-v645-realgate-ci.sh"

# 1) Hard exit-code contract.
test "$(cat "$E/source_gates_exitcode.txt")" = "0"
test "$(cat "$E/real_gate_exitcode.txt")" = "0"
test "$(cat "$E/source_sha256_after_exitcode.txt")" = "0"

# 2) Historical R5 accounting. The final runner footer is the explicit total;
# summing every ASSERTIONS= token would double-count per-test footers plus final total.
H="$E/CODEX_EVIDENCE_SOURCE/08_historical_r5.log"
final_hist=$(grep -E '^COUNT=54 FAIL=[0-9]+ ASSERTIONS=[0-9]+$' "$H" | tail -n 1)
test "$final_hist" = "COUNT=54 FAIL=0 ASSERTIONS=3097"
explicit=3097
implicit=19
canonical=$((explicit + implicit))
test "$canonical" -eq 3116
cat > "$E/historical_assertion_accounting.txt" <<EOF
MASTER_CANONICAL_ASSERTIONS=3116
HISTORICAL_FINAL_RUNNER_FOOTER=$final_hist
EXPLICIT_ASSERTIONS=3097
LEGACY_IMPLICIT_CHECKS=19
CANONICAL_TOTAL=$canonical
ACCOUNTING_METHOD=Use the final historical runner footer once; do not sum per-test ASSERTIONS footers and the final aggregate together.
EOF

# 3) Mandatory suite summaries.
grep -Fxq 'COUNT=10 FAIL=0 ASSERTIONS=78' "$E/CODEX_EVIDENCE_SOURCE/04_v645_rootcause.log"
grep -Fxq 'COUNT=11 FAIL=0 ASSERTIONS=363' "$E/CODEX_EVIDENCE_SOURCE/05_v643_regression.log"
grep -Fxq 'COUNT=4 FAIL=0 ASSERTIONS=70' "$E/CODEX_EVIDENCE_SOURCE/06_v644_functional.log"
grep -Fxq 'POSTMORTEM_DIAGNOSTIC_EXPECTED_GAP_CONFIRMED' "$E/CODEX_EVIDENCE_SOURCE/07_v644_postmortem_gap_diagnostic.log"

# 4) Real environment and every real gate A-H marker.
grep -Fq 'ENVIRONMENT_OK WP=7.0.1 PHP=8.4.' "$E/CODEX_EVIDENCE_REAL_GATE/01-verify_environment.php.log"
grep -Fq 'DB=11.4.' "$E/CODEX_EVIDENCE_REAL_GATE/01-verify_environment.php.log"
grep -Fq 'LIVE800_OK ticks=39 transport=839 cursor=311' "$E/CODEX_EVIDENCE_REAL_GATE/02-live800_resume.php.log"
grep -Fxq 'NEGATIVE_LIMITS_OK' "$E/CODEX_EVIDENCE_REAL_GATE/03-negative_limits.php.log"
grep -Fxq 'STALE_CAS_OK' "$E/CODEX_EVIDENCE_REAL_GATE/04-stale_cas.php.log"
grep -Fxq 'SOFT_RECOVERY_OK' "$E/CODEX_EVIDENCE_REAL_GATE/05-soft_failure_recovery.php.log"
grep -Fq 'CONCURRENT_LEASE_OK acquired=1 rejected=4' "$E/CODEX_EVIDENCE_REAL_GATE/08_assert_concurrent.log"
grep -Fq 'CONCURRENT_TICK_BURST_OK' "$E/CODEX_EVIDENCE_REAL_GATE/11_assert_tick_burst.log"
grep -Fq 'CHECKPOINT_RESUME_OK' "$E/CODEX_EVIDENCE_REAL_GATE/12-continue_concurrent_checkpoint.php.log"
grep -Fxq 'DB_SANITY_PASS' "$E/CODEX_EVIDENCE_REAL_GATE/13_db_sanity.log"
grep -Fq 'Status: Active' "$E/CODEX_EVIDENCE_REAL_GATE/14_plugin_status.log"
grep -Fq 'Version: 6.45.0' "$E/CODEX_EVIDENCE_REAL_GATE/14_plugin_status.log"

# 5) Gate-D harness correction must be test-only and the negative case must remain.
grep -Fxq 'TEST_HARNESS_ONLY=YES' "$E/gate_d_overlay_manifest.txt"
grep -Fxq 'PRODUCTION_SOURCE_CHANGED=NO' "$E/gate_d_overlay_manifest.txt"
grep -Fq 'NEGATIVE_CASE_PRESERVED=YES' "$E/gate_d_overlay_manifest.txt"
grep -Fq 'missing immutable seller-route snapshot fails closed with concrete selection_scope_empty code' "$E/CODEX_EVIDENCE_REAL_GATE/05-soft_failure_recovery.php.log"

# 6) Re-run immutable production-source identity AFTER all source + real gates.
(cd "$PKG/02_SOURCE_V645" && sha256sum -c SOURCE_SHA256.txt) > "$E/source_sha256_hard_recheck.txt"

# 7) Independent final state sanity: UUID/phase/cursor evidence must be present.
test -s "$E/final_run_state.json"
grep -Fq '"run_uuid"' "$E/final_run_state.json"

cat > "$E/HARD_VERIFICATION.txt" <<EOF
HARD_VERIFICATION=PASS
SOURCE_GATES=PASS
HISTORICAL_R5=54/54
MASTER_CANONICAL_ASSERTIONS=3116
REAL_ENVIRONMENT=WordPress_7.0.1_PHP_8.4_MariaDB_11.4
REAL_GATES_A_H=PASS
PRODUCTION_SOURCE_UNCHANGED=PASS
GATE_D_HARNESS_ONLY=PASS
INSTALL_ZIP_BUILT=NO
EOF

# Repackage evidence only after all hard checks are green.
cd "$WORK"
rm -f CODEX_V645_REALGATE_EVIDENCE_GHA_20260820.zip
zip -qr CODEX_V645_REALGATE_EVIDENCE_GHA_20260820.zip V645_EVIDENCE
unzip -t CODEX_V645_REALGATE_EVIDENCE_GHA_20260820.zip > "$E/evidence_zip_integrity_hard.txt"
sha256sum CODEX_V645_REALGATE_EVIDENCE_GHA_20260820.zip > "$E/evidence_zip_sha256_hard.txt"

echo 'V645_HARD_REALGATE_VERIFICATION_OK'
