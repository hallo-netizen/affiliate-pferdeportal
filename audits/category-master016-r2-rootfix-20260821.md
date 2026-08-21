# Kategorie-Workflow MASTER 016-R2 / V1.6.2 – Real-Run-Rootfix Audit

Datum: 2026-08-21
Branch: `category-master016-r2-rootfix-20260821`
Basis: `category-master016-hardstand-20260820`
Status: `LOCAL FULL ARTIFACT HARD PASS / V1.6.2 PAID LEAF RUN NICHT BEHAUPTET`

## Verbindlicher Stand
- Contract-ID bleibt `ALLGEMEINGUELTIGER_KATEGORIE_MASTER_016_WORKFLOW_HARDLOCK` wegen In-Flight-Signaturkompatibilität des laufenden MASTER016-Runs.
- Master-Revision: `016-R2`
- Plugin: `affiliate-portal-kategorie-workflow` V1.6.2
- Workflow: exakt 14 Hauptstufen; kontrollierter Blatt-Fallback bleibt Unterstufe von Stufe 10.
- aktive Regeln: 126/126 `ACTIVE`
- Master ZIP: `ALLGEMEINGUELTIGER_KATEGORIE_MASTER_016_R2_WORKFLOW_HARDLOCK.zip`
- Master SHA-256: `954f83208e2e80d5b68470de05bb46211f19fb55ad54234cea54e84eb142c12e`
- Installer SHA-256: `eac5ad15aa9f7688b32c99518faa0387f2459300452d4a827d9e98a7c2723992`
- Source ZIP SHA-256: `fd9399332b2a4f44ed70a323374586e4a0abef5c2cca3863718f416d67d6fb71`

## Reale Root Causes
Der reale Gaumen-Atelier-Detailresearch erzeugte ein 69.553.705-Byte-Research-Paket. Im bereits bezahlten Clusterresearch hatten 93 von 107 aktiven Content-Leaves weniger als 3 node-gebundene Longtail-Kandidaten. Ein kombinierter `keyword_ideas/live`-Cluster-Call garantiert also trotz Leaf-Seeds keine node-spezifische Negativ-/Positivabdeckung. Zusätzlich konnte V1.6.1 das eigene 69,55-MB-Folgepaket wegen des Uploadlimits nicht wieder einlesen.

## Rootfix
- kostenloser Blatt-Evidenzpreflight nach regulärem Detailresearch;
- gezielt `keyword_suggestions/live` nur für Content-Leaves mit `<3` gebundenen Longtails;
- maximal 20 Leaves je Paid-Batch;
- maximal 1 Paid Call je `concept_id` pro gebundener Research-Linie;
- 0 erneute Global-Coverage-Aufrufe;
- 0 erneute Cluster-Keyword-Ideas-Aufrufe;
- gezielte Evidenz ausschließlich am exakten Leaf;
- `.json.gz`-Upload max. 20 MB komprimiert / 128 MB dekomprimiert;
- Hash/HMAC/Master-/Projekt-/Research-Bindung wird nach Dekompression unverändert geprüft;
- bestehende V1.6.1 MASTER016-Signaturkette bleibt verifizierbar.

## Geänderte Produktionsdateien gegenüber V1.6.1
Exakt 6:
1. `affiliate-portal-kategorie-workflow.php`
2. `includes/class-apkw-admin.php`
3. `includes/class-apkw-dataforseo.php`
4. `includes/class-apkw-research-evidence.php`
5. `includes/class-apkw-research.php`
6. `schema-research-v1.4.json`

Keine Portal-Content-, Design-, Prompt-, Titel-, Beitragsarten- oder Textmaschinenlogik wurde geändert.

## Prüfungen
- aktive Source: 134/134 PASS
- Fresh Source ZIP: 134/134 PASS
- Fresh Installer ZIP: 134/134 PASS
- Master-embedded Source: 134/134 PASS
- Master-embedded Installer: 134/134 PASS
- PHP-Lint: 10/10 PASS
- JSON-Parse: PASS
- Source↔Installer: 0 Diff-Zeilen
- Content-Write-Scan: 0 Treffer in 9 Produktions-PHP-Dateien
- Produktionsendpunkte exakt: `user_data`, `keyword_ideas/live`, `keyword_overview/live`, `keyword_suggestions/live`
- aktiver Master-Conflict-Audit: PASS; 10 aktive normative Dateien; 14/14 Workflowstufen; 126/126 Regeln ACTIVE
- Master SHA-Manifest: 410/410 PASS nach Fresh-Unpack
- externe und Master-eingebettete Source-/Installer-ZIPs byteidentisch
- Master-/Installer-/Source-ZIP-Integrität PASS

## Codex
MASTER016-R2 enthält einen expliziten Codex-Auditauftrag für den Fall einer unabhängigen Codeprüfung. Codex ist für diesen lokalen Rootfix nicht erforderlich, weil Root Cause, Implementierung und vollständige Regression lokal reproduzierbar PASS sind. Falls Codex später eingesetzt wird, darf es nur den eingefrorenen V1.6.2-Source-/Masterstand prüfen; keine eigenmächtigen Fach-, Kategorie-, Content- oder Workflowänderungen.

## Abgrenzung
`main` bleibt unverändert. Kein Merge. Keine API-Keys, WordPress-Datenbank, Medien oder Secrets werden in GitHub gespeichert. Das reale Gaumen-Research-Paket wird nicht in GitHub abgelegt; im Audit stehen nur technische Triggerdaten und Hash-/Prüfnachweise.