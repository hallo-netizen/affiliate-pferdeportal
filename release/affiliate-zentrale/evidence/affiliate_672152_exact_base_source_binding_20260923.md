# Affiliate-Zentrale 6.72.152 – exakte Basis-Source-Bindung – 2026-09-23

Status: BASE_SOURCE_COMMITTED_GATE_PENDING

## Exakte Quelle
- Nutzer-Upload: `AFFILIATE_ZENTRALE_V6.72.152_LIVE_CORRECTIVE_BATCH_INSTALLIEREN.zip`
- SHA256: `32443719e5254ac82e0ebe290d7b52c6790f87951c3b2597874b6d477e80e95c`
- Pluginversion: `6.72.152`
- Dateien: `27`
- Source-Manifest SHA256: `719cd6ce7b435977b114af3a97ace544a3d8e6b1094fea1c87e785284a79f372`

## Git-Objekt-Nachweis
22 der 27 exakten Basisdateien waren bereits als Git-Blobs im Repository vorhanden.
Fünf fehlende Blob-Objekte wurden direkt aus dem Nutzer-Upload übertragen und jeweils gegen den vorab berechneten Git-Blob-SHA geprüft:
- `trait-ppar-automation-suite.php` -> `2b956530c04d3762d5a9f2b142f5a58cdfecf960`
- `trait-ppar-creative-library.php` -> `ff7f0a97911f2c0bcb2d962e4ec41fb4eb57b8e7`
- `trait-ppar-ebay.php` -> `124eeec5a506d88f7b85872e95d3562d0c9f4a15`
- `trait-ppar-output-objects.php` -> `4b7586e93ee61cff8f6553cafe9173f1b53b1eac`
- `pferdeportal-affiliate-router.php` -> `a36174ffbab0aace516ab3c167c178c4f0887fe4`

Alle fünf Git-SHAs: MATCH.

## Kategorie-Scope
Die Basis enthält noch die unveränderten bisherigen Kategoriebytes:
- `portal-structure-v279.json` SHA256 `b86a160e6b8cf720077830422ca6b574203ce171fdc65d357fe9c6bed039c2e0`
- `ebay-portal-catalog-v2.json` SHA256 `4eecef55a3033a4691f8a832eba5fb1657cdb15826ee47d366dccbaabfbb1fa2`

Die bereits hart getesteten Kategoriebytes werden erst nach Source-/Tree-Hash-PASS als exakt zwei erlaubte Deltas eingesetzt.
Kein WordPress-Write.
