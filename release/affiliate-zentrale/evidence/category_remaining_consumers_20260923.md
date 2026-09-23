# Kategorieintegration – verbleibende Verbraucher 2026-09-23

Rolle: Status-/Blockernachweis. Keine Kategorienquelle.

Einzige Kategorienquelle bleibt:
`CATEGORY_INTEGRATION_HOBBYRAUM/PFERDEPORTAL_KATEGORIEN/KATEGORIEN.tsv`.

## PPM 6.7.9

Abgeschlossen:
- 1149 Produktionskategorien
- 5745 Portalslots
- 5790 Gesamtslots
- signierter Kandidat SHA256 `cb64d1ee7fcf9c3bc4ff5aa9e2e8cb948763c2c2c1a7ad956b90f980da9e40fa`
- Build-Integrity PASS

Nicht erneut prüfen.

## PPA-013

Der exakte aktuelle Live-Vollstand ist weder im Repository noch in der aktuellen Library noch als Gesprächsdatei verfügbar.

Bekanntes offenes Delta:
- ausschließlich fünf kurze Kachelvorschauen.

Verboten:
- Rekonstruktion aus alten 1.50.3xx-ZIPs;
- Annahme, 1.50.558 oder 1.50.559 sei der aktuelle Vollstand;
- Rückbau des Performance-Helfers oder der bereits bestätigten Text/Icon/Exact-7-Änderungen.

Status: **BLOCKED_EXACT_CURRENT_FULL_SOURCE_NOT_AVAILABLE**.

## Affiliate 6.72.145

Belegter exakter Soll-Vollstand:
`AFFILIATE_ZENTRALE_V6.72.145_PERFORMANCE_BATCH_READ_ROOTFIX_HARDTEST.zip`
SHA256:
`a5d6bccb11d41005be0f0db40b2dcdb32b8e40e73a772411b44039adedc548de`.

Hardtest:
- Run `35646653332` SUCCESS
- Commit `9c084d95d8074e63129bd54a8836e93cb344d3cc`.

Aktuelle Prüfung:
- Library: Paket nicht vorhanden;
- Workflow-Run 35646653332: keine erhaltenen Artefakte;
- Hardtest-Commit: Paket nicht committed.

Das bereits geprüfte Kategorien-Delta für Portalstruktur/eBay-Katalog bleibt gültig. Es wird **nicht** in den veralteten Repo-Stand 6.72.105 rekonstruiert.

Status: **BLOCKED_EXACT_6_72_145_FULL_PACKAGE_NOT_AVAILABLE**.

## PSTE

Keine 25er-Hardcodierung erforderlich. Kategorien/Struktur werden dynamisch gelesen.

Status:
- **NO_CATEGORY_CODE_CHANGE_REQUIRED**
- erforderlich ist ein frischer Struktur-Readback gegen den aktuellen WordPress-Bestand.

## PSERC

Frischer vorhandener Metadaten-Snapshot:
`seo-redaktionsplan-metadaten-snapshot-6157fc4c4b9c110a28d9c89729d5cbecf31b94579ed77031fa9d63cf243ed4d6.json`

Darin:
- Compiler: **0.28.23**
- `portal_structure_category_count`: **1124**

Damit ist dieser Snapshot vor der 25er-Erweiterung gebunden und muss nach dem PSTE-Struktur-Refresh neu erzeugt werden.

Ziel:
- 1149 Produktionskategorien aus der zentralen `KATEGORIEN.tsv`
- keine neue Kategorienautorität
- keine manuelle 25er-Hardcodierung.

## WordPress

Keine Schreiboperation durchgeführt.
