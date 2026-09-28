# HD-001 – KATEGORIE-WORKFLOW – CURRENT

STAND: 2026-09-28
STATUS: V1.8.5 HOBBY-DEPOT-SIMPLE GEBAUT / REDUZIERTE UI / LIVE-UPDATE ALS NÄCHSTES

## Aktueller Stand

Plugin:
`Affiliate-Portal Kategorie-Workflow V1.8.5 Hobby Depot Simple`

Installer:
`AFFILIATE_PORTAL_KATEGORIE_WORKFLOW_V1.8.5_HOBBY_DEPOT_SIMPLE.zip`

Installer SHA-256:
`332e50db94771b808aac067e2f198ebc32e9141012566c1da785f3ada294282e`

Source:
`QUELLCODE_KATEGORIE_WORKFLOW_V1.8.5_HOBBY_DEPOT_SIMPLE.zip`

Source SHA-256:
`fa8653a76884ff16c6dc12b1b90c0fd0c5d1fb12a52970361c14cc780294f261`

## Vereinfachung ohne Funktionsabbau

Standardansicht zeigt nur:
- DataForSEO-Status und Verbindungstest;
- Sicherheitsstatus;
- Protokoll-Link;
- Konzeptdatei laden und kostenlos prüfen;
- bestätigten SEO-Erstentwurf.

Eingeklappt, aber vollständig erhalten:
- sichtbare Erstprüfung;
- Global Coverage;
- sichtbare Global-Gap-Prüfung;
- Detailresearch;
- Spezialisierungs-Tiefenprüfung;
- optionale Blatt-Evidenz;
- read-only Gesamtprüfung;
- technische Zielbindung;
- sichtbare Finalprüfung;
- FINAL_APPROVED;
- Deployment-Dry-Run;
- Apply;
- Readback;
- Rollback;
- Drift-Schutz und Idempotenz.

Keine Gate-, Qualitäts-, Research- oder Deployment-Logik wurde entfernt.

## Installer-Reduktion

Installationspaket enthält nur Runtime-Dateien/Schemas/Beispiel/README/SHA256SUMS.
Tests und Audit-Dokumente bleiben im Quellpaket.

Größe:
- V1.8.4 Installer: ca. 209 KB
- V1.8.5 Installer: ca. 107 KB

## Tests

- Source Vollsuite: 227/227 PASS;
- Fresh-Unpack-Installer mit identischem Test-Runner: 227/227 PASS;
- Source PHP-Lint: 17/17 PASS;
- Installer Runtime PHP-Lint: 16/16 PASS;
- Runtime-Parität Source↔Installer: 21/21 Dateien byteidentisch.

## Testinput

`HOBBY_DEPOT_TESTLABOR_KATEGORIE_KONZEPT_20260928.json`

## NEXT ACTION

V1.8.5 über V1.8.4 installieren. Danach nur prüfen, ob die reduzierte Hauptansicht erscheint; anschließend DataForSEO-Verbindungstest starten.
