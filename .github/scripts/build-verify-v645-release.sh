#!/usr/bin/env bash
set -euo pipefail

WORK="${GITHUB_WORKSPACE:-$(pwd)}"
E="$WORK/V645_RELEASE_EVIDENCE"
SOURCE_E="$WORK/V645_EVIDENCE"
PKG="/tmp/v645pkg/CODEX_V645_REALGATE_SOURCE_AND_EXACT_TASK_20260820"
SRC="$PKG/02_SOURCE_V645/affiliate-portal-router"
INSTALL="$WORK/affiliate-zentrale_v6.45.0_CANONICAL_RUN_PERSISTENCE_RACE_ROOTFIX_REALGATE.zip"
FRESH=/tmp/v645-install-fresh
ZIPTEST=/tmp/v645-ziptest
WP2=/tmp/wordpress-v645-zip
MASTER_DIR=/tmp/master-v645
MASTER="$WORK/MASTER_AFFILIATE_ZENTRALE_V6_45_0_CANONICAL_RUN_PERSISTENCE_RACE_ROOTFIX_REALGATE_20260820.zip"

rm -rf "$E" "$FRESH" "$ZIPTEST" "$WP2" "$MASTER_DIR"
rm -f "$INSTALL" "$MASTER"
mkdir -p "$E"

# PRE-BUILD DECISION: execute the complete hardened source + real production-path gate.
chmod +x "$WORK/.github/scripts/run-v645-realgate-ci.sh" "$WORK/.github/scripts/verify-v645-full-evidence.sh"
"$WORK/.github/scripts/verify-v645-full-evidence.sh" | tee "$E/prebuild_hard_gate.log"
grep -Fxq 'HARD_VERIFICATION=PASS' "$SOURCE_E/HARD_VERIFICATION.txt"
grep -Fxq 'SOURCE_GATES=PASS' "$SOURCE_E/HARD_VERIFICATION.txt"
grep -Fxq 'REAL_GATES_A_H=PASS' "$SOURCE_E/HARD_VERIFICATION.txt"
grep -Fxq 'PRODUCTION_SOURCE_UNCHANGED=PASS' "$SOURCE_E/HARD_VERIFICATION.txt"

cat > "$E/PRE_BUILD_DECISION.txt" <<'EOT'
DECISION=A_PASS
REASON=All mandatory source, historical, regression, counterproof, real WordPress/MariaDB A-H, and immutable-source checks passed before build.
BUILD_ALLOWED=YES
EOT

# Build only now, from the exact hash-verified production source.
(cd "$PKG/02_SOURCE_V645" && sha256sum -c SOURCE_SHA256.txt) > "$E/source_sha256_immediately_prebuild.txt"
(cd "$PKG/02_SOURCE_V645" && zip -qr "$INSTALL" affiliate-portal-router)
unzip -t "$INSTALL" > "$E/install_zip_integrity_initial.txt"
sha256sum "$INSTALL" > "$E/install_zip_sha256.txt"

# Fresh-unpack identity: exact file set and exact bytes.
mkdir -p "$FRESH"
unzip -q "$INSTALL" -d "$FRESH"
(
  cd "$SRC" && find . -type f -print0 | sort -z | xargs -0 sha256sum
) > "$E/source_tree_sha256.txt"
(
  cd "$FRESH/affiliate-portal-router" && find . -type f -print0 | sort -z | xargs -0 sha256sum
) > "$E/fresh_unpack_tree_sha256.txt"
diff -u "$E/source_tree_sha256.txt" "$E/fresh_unpack_tree_sha256.txt" > "$E/source_vs_fresh_unpack.diff"
test ! -s "$E/source_vs_fresh_unpack.diff"
source_count=$(find "$SRC" -type f | wc -l | tr -d ' ')
fresh_count=$(find "$FRESH/affiliate-portal-router" -type f | wc -l | tr -d ' ')
test "$source_count" = "$fresh_count"
echo "SOURCE_FILE_COUNT=$source_count" > "$E/file_counts.txt"
echo "FRESH_UNPACK_FILE_COUNT=$fresh_count" >> "$E/file_counts.txt"

# Fresh-unpack syntax/JSON/version checks.
find "$FRESH/affiliate-portal-router" -type f -name '*.php' -print0 | sort -z | while IFS= read -r -d '' f; do php -l "$f"; done > "$E/fresh_unpack_php_lint.log"
php -r '$files=$argv; foreach($files as $f){json_decode(file_get_contents($f),true); if(json_last_error()!==JSON_ERROR_NONE){fwrite(STDERR,"JSON_FAIL $f ".json_last_error_msg()."\n"); exit(1);} echo "JSON_OK $f\n";}' \
  "$FRESH/affiliate-portal-router/assets/ebay-portal-catalog-v2.json" \
  "$FRESH/affiliate-portal-router/assets/portal-structure-v279.json" > "$E/fresh_unpack_json.log"
grep -Fq 'Version: 6.45.0' "$FRESH/affiliate-portal-router/pferdeportal-affiliate-router.php"

# Run ALL source/historical/regression gates again against the actual fresh-unpacked installer content.
cp -a "$PKG" "$ZIPTEST"
rm -rf "$ZIPTEST/02_SOURCE_V645/affiliate-portal-router"
cp -a "$FRESH/affiliate-portal-router" "$ZIPTEST/02_SOURCE_V645/affiliate-portal-router"
(
  cd "$ZIPTEST" && 07_RUNNERS/run_source_gates.sh
) > "$E/final_zip_source_gates.log" 2>&1
cp -a "$ZIPTEST/CODEX_EVIDENCE_SOURCE" "$E/FINAL_ZIP_SOURCE_EVIDENCE"
grep -Fxq 'COUNT=10 FAIL=0 ASSERTIONS=78' "$E/FINAL_ZIP_SOURCE_EVIDENCE/04_v645_rootcause.log"
grep -Fxq 'COUNT=11 FAIL=0 ASSERTIONS=363' "$E/FINAL_ZIP_SOURCE_EVIDENCE/05_v643_regression.log"
grep -Fxq 'COUNT=4 FAIL=0 ASSERTIONS=70' "$E/FINAL_ZIP_SOURCE_EVIDENCE/06_v644_functional.log"
grep -Fxq 'COUNT=54 FAIL=0 ASSERTIONS=3097' "$E/FINAL_ZIP_SOURCE_EVIDENCE/08_historical_r5.log"

# Reset the already-proved real database to an empty WordPress schema for a second, fresh FINAL-ZIP install.
wp db reset --yes --path=/tmp/wordpress-v645 --allow-root > "$E/final_zip_db_reset.log" 2>&1

# Fresh WordPress 7.0.1; install and activate FROM THE FINAL INSTALL ZIP, not copied source.
mkdir -p "$WP2"
wp core download --version=7.0.1 --path="$WP2" --force --allow-root > "$E/final_zip_wp_setup.log" 2>&1
wp config create --path="$WP2" --dbname=v645gate --dbuser=wp --dbpass=wppass --dbhost=127.0.0.1:3306 --skip-check --allow-root >> "$E/final_zip_wp_setup.log" 2>&1
wp core install --path="$WP2" --url=http://v645zip.test --title='V645 Final ZIP Gate' --admin_user=gateadmin --admin_password='GateOnly-20260820!' --admin_email=gate@example.invalid --skip-email --allow-root >> "$E/final_zip_wp_setup.log" 2>&1
wp plugin install "$INSTALL" --activate --path="$WP2" --allow-root >> "$E/final_zip_wp_setup.log" 2>&1
wp plugin status affiliate-portal-router --path="$WP2" --allow-root > "$E/final_zip_plugin_status_before.log"
grep -Fq 'Status: Active' "$E/final_zip_plugin_status_before.log"
grep -Fq 'Version: 6.45.0' "$E/final_zip_plugin_status_before.log"

# Real A-H again against the final ZIP-installed plugin using the corrected TEST-ONLY Gate D fixture.
(
  cd "$ZIPTEST" && WP_ROOT="$WP2" WP="$(command -v wp)" 07_RUNNERS/run_real_gate_from_existing_wordpress.sh
) > "$E/final_zip_real_gate.log" 2>&1
cp -a "$ZIPTEST/CODEX_EVIDENCE_REAL_GATE" "$E/FINAL_ZIP_REAL_GATE_EVIDENCE"
grep -Fq 'ENVIRONMENT_OK WP=7.0.1 PHP=8.4.' "$E/FINAL_ZIP_REAL_GATE_EVIDENCE/01-verify_environment.php.log"
grep -Fq 'DB=11.4.' "$E/FINAL_ZIP_REAL_GATE_EVIDENCE/01-verify_environment.php.log"
grep -Fq 'LIVE800_OK ticks=39 transport=839 cursor=311' "$E/FINAL_ZIP_REAL_GATE_EVIDENCE/02-live800_resume.php.log"
grep -Fxq 'NEGATIVE_LIMITS_OK' "$E/FINAL_ZIP_REAL_GATE_EVIDENCE/03-negative_limits.php.log"
grep -Fxq 'STALE_CAS_OK' "$E/FINAL_ZIP_REAL_GATE_EVIDENCE/04-stale_cas.php.log"
grep -Fxq 'SOFT_RECOVERY_OK' "$E/FINAL_ZIP_REAL_GATE_EVIDENCE/05-soft_failure_recovery.php.log"
grep -Fq 'CONCURRENT_LEASE_OK acquired=1 rejected=4' "$E/FINAL_ZIP_REAL_GATE_EVIDENCE/08_assert_concurrent.log"
grep -Fq 'CONCURRENT_TICK_BURST_OK' "$E/FINAL_ZIP_REAL_GATE_EVIDENCE/11_assert_tick_burst.log"
grep -Fq 'CHECKPOINT_RESUME_OK' "$E/FINAL_ZIP_REAL_GATE_EVIDENCE/12-continue_concurrent_checkpoint.php.log"
grep -Fxq 'DB_SANITY_PASS' "$E/FINAL_ZIP_REAL_GATE_EVIDENCE/13_db_sanity.log"

# Final installer immutability and archive checks AFTER all installer tests.
unzip -t "$INSTALL" > "$E/install_zip_integrity_after_all_tests.txt"
sha256sum "$INSTALL" > "$E/install_zip_sha256_after_all_tests.txt"
diff -u "$E/install_zip_sha256.txt" "$E/install_zip_sha256_after_all_tests.txt" > "$E/install_zip_hash_stability.diff"
test ! -s "$E/install_zip_hash_stability.diff"
rm -rf "$FRESH/final_reunpack" && mkdir -p "$FRESH/final_reunpack"
unzip -q "$INSTALL" -d "$FRESH/final_reunpack"
(
  cd "$FRESH/final_reunpack/affiliate-portal-router" && find . -type f -print0 | sort -z | xargs -0 sha256sum
) > "$E/final_reunpack_tree_sha256.txt"
diff -u "$E/source_tree_sha256.txt" "$E/final_reunpack_tree_sha256.txt" > "$E/source_vs_final_reunpack.diff"
test ! -s "$E/source_vs_final_reunpack.diff"

cat > "$E/REAL_GATE_FINAL_MATRIX.txt" <<'EOT'
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
Finale Installations-ZIP real A-H getestet: PASS
EOT

# Release report required by MASTER. Mock/stub disclosure is explicit.
cat > "$E/RELEASE_REPORT.md" <<'EOT'
# V6.45.0 RELEASE REPORT

## Ursache
Der V6.44-Produktionsstand konnte bei konkurrierender kanonischer Run-Persistenz einen fortgeschrittenen Worker-/Lease-/Cursor-Zustand durch einen veralteten Whole-Run-Snapshot überschreiben. Zusätzlich fehlte ein harter, am realen 311-Familien-Manifest abgeleiteter selection_prepare-Terminierungsvertrag für den echten Workerpfad.

## Änderung
Nur drei Produktionsdateien gegenüber V6.44: pferdeportal-affiliate-router.php, includes/trait-ppar-ebay-run.php, readme.txt. V6.45 führt atomaren Whole-Run-CAS/Lease-Schutz und bounded/monotone selection_prepare-Fortschrittsregeln im kanonischen Runpfad ein.

## Nicht geändert
Keine Titel-/Text-/Prompt-/SEO-/Design-/HTML-/Beitragsart-/Kategorien-/Produktfachentscheidung wurde verändert. Provider-/Artikel-/Frontend-Fachlogik außerhalb des technischen Run-/Persistenzpfads blieb unverändert.

## Prüfmatrix
Source-Rootcause/Race, historische Regression, kompletter kanonischer Gesamtworkflow, positive/negative Terminierung, persistierte Resume-Zustände, stale CAS, Soft-Failure-Recovery, echte parallele Lease-Konkurrenz, echter paralleler Worker-Burst, Checkpoint-Resume sowie finaler ZIP-Re-Test wurden ausgeführt.

## Mock-/Stub-Offenlegung
Die V6.43-Gesamtworkflow-Regression und Teile der historischen Source-Suite verwenden WordPress-/Provider-/Daten-Fixtures. Sie werden NICHT als Real-Gate gewertet. Das Real-Gate A-H lief separat mit echter Plugin-Klasse, echtem kanonischem Worker, echter WordPress Options API, echtem wpdb und MariaDB 11.4. Der Gate-D-Testharness wurde ausschließlich so korrigiert, dass er einen tatsächlich erreichbaren V6.44 config_snapshot-Zustand erzeugt; der frühere fehlende-Snapshot-Zustand bleibt als fail-closed Negativtest erhalten. Produktionscode wurde dafür nicht geändert.

## Paketprüfung
Die endgültige Installations-ZIP wurde nach dem Build frisch entpackt, byteweise per SHA-256 gegen Source verglichen, PHP/JSON geprüft, anschließend wurden sämtliche Source-/historischen Gates erneut gegen ihren Inhalt ausgeführt und die ZIP selbst in einer zweiten frischen WordPress-7.0.1-/MariaDB-11.4-Umgebung installiert und durch Real-Gate A-H geprüft. Danach wurde die ZIP erneut auf Integrität, SHA-256-Stabilität und Source-Identität geprüft.

## Ergebnis
PASS – INSTALLATION FREIGEGEBEN
EOT

# Build MASTER only after the final installer itself passed every required re-test.
mkdir -p "$MASTER_DIR/00_READ_ME_FIRST" "$MASTER_DIR/01_MASTER_BINDING" "$MASTER_DIR/02_INSTALL" "$MASTER_DIR/03_SOURCE" "$MASTER_DIR/04_PREBUILD_REAL_GATE_EVIDENCE" "$MASTER_DIR/05_FINAL_INSTALLER_EVIDENCE" "$MASTER_DIR/06_DIFF_AND_HASHES" "$MASTER_DIR/07_REPORT"
cp "$E/REAL_GATE_FINAL_MATRIX.txt" "$MASTER_DIR/00_READ_ME_FIRST/REAL_GATE_FINAL_MATRIX.txt"
cp "$PKG/01_MASTER_BINDING/HARTER_PRUEF_BUILD_UND_FREIGABEVERTRAG.md" "$MASTER_DIR/01_MASTER_BINDING/"
cp "$PKG/01_MASTER_BINDING/MASTER_AFFILIATE_ZENTRALE_V6_44_0_LIVE_FAIL_HARD_CONTRACT_POSTMORTEM_BLOCKED_20260820.zip" "$MASTER_DIR/01_MASTER_BINDING/"
cp "$INSTALL" "$MASTER_DIR/02_INSTALL/"
cp -a "$SRC" "$MASTER_DIR/03_SOURCE/affiliate-portal-router"
cp -a "$SOURCE_E"/. "$MASTER_DIR/04_PREBUILD_REAL_GATE_EVIDENCE/"
cp -a "$E"/. "$MASTER_DIR/05_FINAL_INSTALLER_EVIDENCE/"
cp -a "$PKG/06_DIFF_AND_HASHES"/. "$MASTER_DIR/06_DIFF_AND_HASHES/"
cp "$E/RELEASE_REPORT.md" "$MASTER_DIR/07_REPORT/"

# Master manifest and embedded-installer identity.
embedded="$MASTER_DIR/02_INSTALL/$(basename "$INSTALL")"
sha256sum "$INSTALL" "$embedded" > "$E/standalone_vs_master_embedded_installer_sha256.txt"
test "$(sha256sum "$INSTALL" | awk '{print $1}')" = "$(sha256sum "$embedded" | awk '{print $1}')"
(
  cd "$MASTER_DIR"
  find . -type f ! -name 'MASTER_SHA256.txt' -print0 | sort -z | xargs -0 sha256sum > MASTER_SHA256.txt
)
(cd "$MASTER_DIR" && sha256sum -c MASTER_SHA256.txt) > "$E/master_manifest_prepack_verified.txt"
(cd "$(dirname "$MASTER_DIR")" && zip -qr "$MASTER" "$(basename "$MASTER_DIR")")
unzip -t "$MASTER" > "$E/master_zip_integrity.txt"
sha256sum "$MASTER" > "$E/master_zip_sha256.txt"

# Fresh-unpack the exact final MASTER and verify its complete manifest plus embedded installer again.
MASTER_FRESH=/tmp/master-v645-fresh
rm -rf "$MASTER_FRESH" && mkdir -p "$MASTER_FRESH"
unzip -q "$MASTER" -d "$MASTER_FRESH"
MF="$MASTER_FRESH/$(basename "$MASTER_DIR")"
(cd "$MF" && sha256sum -c MASTER_SHA256.txt) > "$E/master_fresh_manifest_verified.txt"
(
  cd "$MF"
  find . -type f ! -name 'MASTER_SHA256.txt' -printf '%p\n' | sort
) > "$E/master_fresh_files_actual.txt"
awk '{sub(/^[0-9a-fA-F]+  /,""); print}' "$MF/MASTER_SHA256.txt" | sort > "$E/master_fresh_files_manifested.txt"
diff -u "$E/master_fresh_files_manifested.txt" "$E/master_fresh_files_actual.txt" > "$E/master_file_set.diff"
test ! -s "$E/master_file_set.diff"
test "$(sha256sum "$INSTALL" | awk '{print $1}')" = "$(sha256sum "$MF/02_INSTALL/$(basename "$INSTALL")" | awk '{print $1}')"
unzip -t "$MF/02_INSTALL/$(basename "$INSTALL")" > "$E/master_embedded_installer_integrity.txt"

cat > "$E/FINAL_RELEASE_DECISION.txt" <<EOT
DECISION=PASS
INSTALLER=$(basename "$INSTALL")
MASTER=$(basename "$MASTER")
SOURCE_FILE_COUNT=$source_count
SOURCE_VS_INSTALLER=BYTE_IDENTICAL
SOURCE_GATES_ON_FINAL_ZIP=PASS
REAL_A_H_ON_FINAL_ZIP=PASS
MASTER_MANIFEST=PASS
MASTER_EMBEDDED_INSTALLER_IDENTICAL=PASS
RESULT=PASS – INSTALLATION FREIGEGEBEN
EOT

echo 'V645_FINAL_RELEASE_VERIFIED_OK'
