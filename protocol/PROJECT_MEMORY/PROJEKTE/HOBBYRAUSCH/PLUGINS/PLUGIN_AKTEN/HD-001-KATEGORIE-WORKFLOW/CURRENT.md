# HD-001 – KATEGORIE-WORKFLOW – CURRENT

STAND: 2026-09-28
STATUS: V1.8.4 HOBBY-DEPOT-PILOT GEBAUT / 225-TEST-PASS / LIVE-TEST ALS NÄCHSTES

## Aktueller Pilotstand

Plugin:
`Affiliate-Portal Kategorie-Workflow V1.8.4 Hobby Depot Pilot`

Installer:
`AFFILIATE_PORTAL_KATEGORIE_WORKFLOW_V1.8.4_HOBBY_DEPOT_PILOT.zip`

Installer SHA-256:
`547ed0fd488975ecfa10b6a66fd10909b9f7760b1204337a78b6300d460660f7`

## Neu in V1.8.4

- Unterpunkt `Kategorien -> Protokoll`;
- verständliche PASS/BLOCKED-Historie;
- DataForSEO-Einzelkosten im Log;
- Konzept-, Research-, Dry-Run-, Deployment-, Readback- und Rollback-Zusammenfassungen;
- JSON-Export des Protokolls;
- bestätigtes Leeren;
- Zugangsdaten/Auth-/Tokenwerte werden nicht protokolliert.

## Tests

- vollständige Regression 225/225 PASS;
- Fresh-Unpack 225/225 PASS;
- PHP-Lint 17/17 PASS;
- Produktionsscan Pferde-Atelier-Bindung: 0 Treffer.

## Testinput

`HOBBY_DEPOT_TESTLABOR_KATEGORIE_KONZEPT_20260928.json`

Nur für kontrollierten Wegwerf-Test; keine produktive Struktur.

## NEXT ACTION

V1.8.4 über die bestehende Installation aktualisieren. Danach:
1. `Kategorien -> Protokoll` öffnen;
2. DataForSEO-Verbindungstest ausführen;
3. Testlabor-Konzept kostenlos vorprüfen;
4. erst danach Paid-Calls bestätigen.
