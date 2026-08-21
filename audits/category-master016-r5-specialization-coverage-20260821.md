# Kategorie-Workflow MASTER 016-R5 / V1.7.0 – allgemeingültige Spezialisierungs-Coverage

Datum: 2026-08-21
Branch: `category-master016-r5-specialization-coverage-20260821`
Basis: `category-master016-r4-target-binding-20260821`
Status: `LOCAL FULL ARTIFACT HARD PASS / LIVE R5 DATAFORSEO-WORDPRESS-E2E NOT EXECUTED`

## Root Cause
Der bisherige Workflow konnte einen spezialisierten Suchraum verlieren, obwohl ein allgemeiner Parent oder Standalone-Core vorhanden bzw. ausgeschlossen war. Außerdem war die feste Mindestanzahl gebundener Longtails als Kategorie-Gate fachlich zu starr. Ein erster R5-Zwischenansatz mit kombinierten Cluster-Seeds wurde verworfen, weil ein Multi-Seed-Providerrequest keine exakte Tiefenabdeckung jedes einzelnen Themenankers garantiert.

## Endgültiger allgemeingültiger R5-Vertrag
- Keine feste Beitrags-/Longtail-Mindestzahl als Kategorie-Gate.
- Für **jeden aktiven Content-Knoten** exakt sein gebundenes Primärkeyword einzeln über `dataforseo_labs/google/keyword_suggestions/live` vertiefen.
- Gültige frühere exakte Node-/Leaf-Suggestions dürfen wiederverwendet werden; Primärkeyword-/Requeständerung invalidiert nur den betroffenen Nachweis.
- Neue Calls max. 20 je Batch; Claim/Resume; erfolgreiche Nodes werden nicht erneut bezahlt; 0 Wiederholung von Global-Coverage und abgeschlossenem Cluster-Research.
- Jeder vom Primärkeyword verschiedene vom Provider zurückgegebene Suchbegriff bleibt Spezialisierungskandidat. Kein Themen-/Branchenwörterbuch, keine Fachliste, kein lexikalischer Kandidatenfilter, kein Top-N-Abschneiden.
- Parent-/Standalone-Entscheidungen kaskadieren nicht auf Spezialisierungen.
- Jeder Kandidat braucht vor READY/FINAL eine explizite Entscheidung `CATEGORY`, `ARTICLE_ONLY`, `COVERED_BY_PARENT` oder `OUT_OF_SCOPE`; fehlend/`DEFERRED` blockiert.
- Kategorie-Workflow besitzt keine finale Beitragstitel-Autorität. Einzelbeitragsrecherche, Redaktionsplan und finale Titel bleiben downstream.
- R3 Paid-Claim-Recovery/GZIP und R4 Deployment-Target-Binding bleiben unverändert erhalten.
- `APKW_CONTENT_WRITE_CAPABILITY=false`; keine Kategorie-/Beitrags-/Menü-Writes im 14-Stufen-Kern.

## R4 -> R5 Produktionsdelta
Exakt 7 Produktions-/Schema-Dateien geändert:
1. `affiliate-portal-kategorie-workflow.php`
2. `includes/class-apkw-admin.php`
3. `includes/class-apkw-research-evidence.php`
4. `includes/class-apkw-research.php`
5. `includes/class-apkw-validator.php`
6. `schema-category-v1.4.json`
7. `schema-research-v1.4.json`

## Harte Prüfungen
- Active Source: 171/171 PASS
- Fresh Source-ZIP: 171/171 PASS
- Fresh Installer: 171/171 PASS
- MASTER-embedded Source: 171/171 PASS
- MASTER-embedded Source-ZIP Fresh-Unpack: 171/171 PASS
- MASTER-embedded Installer Fresh-Unpack: 171/171 PASS
- Final Fresh-MASTER Source: 171/171 PASS
- aus Final Fresh-MASTER erneut entpackte Source-/Installer-ZIPs: jeweils 171/171 PASS
- internes Source-SHA-Manifest: 43/43 PASS
- vollständiges MASTER-SHA-Manifest nach Fresh-Unpack: 518/518 PASS
- aktiver MASTER-Konfliktaudit: 11/11 aktive Dateien, 140/140 Regeln ACTIVE, 14/14 Workflow, 0 Findings
- PHP-Lint: 10/10 PASS
- JSON: 14/14 PASS
- verbotene Portal-Write-APIs: 0 Treffer
- externe Produktionsendpunkte: exakt 4 erlaubte Endpunkte
- Themen-/Branchen-Hardcodes im Produktionscode: 0 Treffer
- Source <-> Fresh Source <-> Fresh Installer <-> MASTER Source: 0 Diff
- externe und MASTER-eingebettete Source-/Installer-ZIPs byteidentisch

## Artefakte / SHA-256
- Source ZIP `QUELLCODE_KATEGORIE_WORKFLOW_V1.7.0_MASTER016_R5_SPECIALIZATION_COVERAGE_ROOTFIX.zip`
  - `9bead599aef1dc086dd182cd20d79dd6517ca2509b7d7a1e9eaa1b4343b0ecb5`
- Installer `AFFILIATE_PORTAL_KATEGORIE_WORKFLOW_V1.7.0_MASTER016_R5_SPECIALIZATION_COVERAGE_ROOTFIX.zip`
  - `9f0cc1bb0af1dcd53c028a456abf10e951048b765dd07fb13703e18ec5831b7e`
- Vollständiger MASTER `ALLGEMEINGUELTIGER_KATEGORIE_MASTER_016_R5_WORKFLOW_HARDLOCK.zip`
  - `e54898cfb3ba2476eca8651b2e0e4569148a2122b7940676e9641d3b25132367`

## Live-Abgrenzung
Lokaler Artefakt-Endvertrag ist vollständig PASS. Ein echter WordPress/DataForSEO-R5-Lauf wurde mit V1.7.0 noch nicht ausgeführt und wird nicht behauptet. Die Live-Kette beginnt erst nach Installation dieses exakten Installers im bestehenden gebundenen Projektlauf.

`main` bleibt unverändert. Kein Merge.