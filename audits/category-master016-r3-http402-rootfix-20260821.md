# Kategorie-Workflow MASTER 016-R3 / V1.6.3 – HTTP402 / Paid-Claim-Recovery

Datum: 2026-08-21
Branch: `category-master016-r3-http402-rootfix-20260821`
Basis: `category-master016-r2-rootfix-20260821`
Status: `LOCAL FULL ARTIFACT HARD PASS / LIVE R3 RECOVERY NOT YET CLAIMED`

## Realer Trigger
Gaumen Atelier, Stufe 10 / 3B: kostenloser Blatt-Preflight 107 Content-Blätter, 93 Evidenzlücken, erster Paid-Batch 20, 0 Global-/Cluster-Wiederholungen. Nach Nutzerbestätigung antwortete DataForSEO mit HTTP 402. V1.6.2 hatte den persistenten Blatt-Batch-Claim bereits vor dem ersten externen Request gesetzt. Nach Aufladung/erneutem Versuch meldete derselbe gebundene Batch deshalb fälschlich „bereits verbraucht“.

## Root Cause
V1.6.2 modellierte „Paid-Step reserviert“ technisch wie „Paid-Step verbraucht“. Es gab keine getrennten Zustände für Reservierung, partiellen Erfolg, retrybaren Providerfehler und vollständigen Abschluss. Zusätzlich wurde bei Nicht-2xx vor der JSON-Auswertung geworfen, sodass DataForSEO-Subcode und Providertext verloren gingen.

## V1.6.3 Rootfix
- Claim-Zustände `RESERVED`, `FAILED_RETRYABLE`, `COMPLETED`.
- Erfolgreicher Blattfortschritt wird nach jedem einzelnen Paid-Call persistent an den exakten `concept_id` gebunden.
- Nach einem späteren Fehler wird beim Resume nur der noch nicht erfolgreiche Rest angefragt; bereits erfolgreiche `concept_id` werden nicht wiederholt oder erneut bezahlt.
- Vollständig abgeschlossene Batches und parallele Doppelstarts bleiben hart gesperrt.
- Ein V1.6.2-Legacy-Vorclaim ohne Status/Progress darf ausschließlich für exakt dieselbe `package_id` + denselben `research_content_sha256` einmalig in den neuen Claim-Vertrag migriert werden.
- DataForSEO HTTP-Fehler erhalten, soweit JSON vorhanden ist, HTTP-Code + Provider-Statuscode + Providertext.
- Keine Änderung an Kategorie-, Longtail-, Content-, Design-, Titel-, Beitragsarten- oder Textmaschinenlogik.
- Keine neue Global-Coverage und keine Wiederholung von Cluster-Keyword-Ideas.

## Produktionsdateien geändert gegenüber V1.6.2
1. `affiliate-portal-kategorie-workflow.php` – Version 1.6.3.
2. `includes/class-apkw-admin.php` – Claim-Zustandsmaschine, Legacy-Recovery, persistenter Einzelcall-Fortschritt, Resume/Complete/Fail.
3. `includes/class-apkw-dataforseo.php` – HTTP-Fehler mit Provider-Subcode/-Text.
4. `includes/class-apkw-research.php` – resumierbarer Leaf-Build mit bereits erfolgreichen Blattresultaten.

## Prüfungen
- aktive Source: 138/138 PASS
- Fresh Source ZIP: 138/138 PASS
- Fresh Installer ZIP: 138/138 PASS
- Master-embedded Source: 138/138 PASS
- Source ↔ Installer: 0 Diff
- PHP-Lint: PASS
- JSON-Parse: PASS
- Content-Write-Scan: 0 Treffer in Produktions-PHP
- externe Produktionsendpunkte: nur `user_data`, `keyword_ideas/live`, `keyword_overview/live`, `keyword_suggestions/live`
- aktive Regeln: 130/130 ACTIVE
- Workflow: unverändert 14/14
- Master-Manifest: 447/447 PASS nach Fresh-Unpack
- externe und Master-eingebettete Source-/Installer-ZIPs byteidentisch
- ZIP-Integrität: PASS

## Artefakte
- Installer `AFFILIATE_PORTAL_KATEGORIE_WORKFLOW_V1.6.3_MASTER016_R3_HTTP402_CLAIM_RECOVERY.zip`
  - SHA-256 `2ef80f19e22aedeecaca47801e7fe2c186965cad7b34d04b532a854ee1d843fb`
- Source `QUELLCODE_KATEGORIE_WORKFLOW_V1.6.3_MASTER016_R3_HTTP402_CLAIM_RECOVERY.zip`
  - SHA-256 `a34438ffc0778f6a3b74727f89db6763590bfc9d5f74e31fda7fcd0325b9f73b`
- Master `ALLGEMEINGUELTIGER_KATEGORIE_MASTER_016_R3_WORKFLOW_HARDLOCK.zip`
  - SHA-256 `b4b0af034fce9fefc7a519c77cb4adc3631f256b7418efdc9666929f38ebf452`

## Codex
Codex ist für diesen Rootfix nicht erforderlich. Falls später eine unabhängige Prüfung gewünscht wird, darf Codex nur den eingefrorenen V1.6.3-/MASTER016-R3-Stand gegen den im Master enthaltenen Auditauftrag prüfen; keine eigenmächtigen Fach-, Kategorie-, Content- oder Workflowänderungen.

`main` bleibt unverändert; kein Merge. Keine API-Keys, WordPress-Datenbank, Medien, Secrets oder reale Gaumen-Research-Pakete werden in GitHub gespeichert.