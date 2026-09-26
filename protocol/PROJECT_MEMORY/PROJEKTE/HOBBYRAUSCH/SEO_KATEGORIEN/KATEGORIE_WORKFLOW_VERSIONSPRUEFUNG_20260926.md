# HOBBY DEPOT – KATEGORIE-WORKFLOW – VERSIONSPRÜFUNG 2026-09-26

## Ergebnis

Neuester belegter Entwicklungsstand:
**Affiliate-Portal Kategorie-Workflow 1.8.1**

Der vorherige allgemeingültige Release-/Archivstand ist:
**V1.8.0 / MASTER016-R10/R11**

## V1.8.1-Nachweis

Autoritative GitHub-Akte:
`audits/PFERDE_ATELIER_PARENT_TOPIC_GAP_TODO_20260922.md`
auf Branch
`category-master016-r10-r9-runtime-deployment-20260822`.

Dort belegt:
- Kandidat: Affiliate-Portal Kategorie-Workflow 1.8.1
- Änderung: allgemeines `PARENT_TOPIC_GAP`-Finalprüfungsgate + serverseitiges Bestätigungsgate + signierte Bestätigung
- keine automatische Strukturanlage allein aus der Erkennung
- Vollregression: 220/220 PASS
- PHP-Lint: 15/15 PASS
- installierbares ZIP nach Neu-Extraktion: 220/220 PASS
- ZIP SHA-256:
  `1915922977b3d803b25ed9458e5eb40ae7dd30c37f9d3c763720d5e47b25ac6b`
- LIVE: noch nicht installiert

Zusätzlich ist die neue Regel als allgemeingültige Regel für künftige Portale dokumentiert:
`audits/KATEGORIE_WORKFLOW_PARENT_TOPIC_GAP_RULE_20260922.md`.

## Keine spätere Version gefunden

Frisch geprüft:
- GitHub-Kategoriebranches
- Commit-Historie
- R11/R12-Branches
- Campus-/Pluginakten

Kein belegter V1.8.2-, V1.8.3- oder V1.9.0-Stand gefunden.

Damit ist **1.8.1 der neueste belegte Entwicklungsstand**.

## Wichtige Grenze

Der exakte Dateiname des V1.8.1-ZIP ist in den autoritativen Akten NICHT dokumentiert.
Dokumentiert sind Version, Tests und SHA-256.

Die ZIP-Bytes selbst sind in den aktuell erreichbaren GitHub-Bäumen ebenfalls nicht abgelegt.
Daher darf kein Dateiname geraten und kein 1.8.1-ZIP rekonstruiert werden.

## Vorheriger exakt benannter V1.8.0-Stand

Installer:
`AFFILIATE_PORTAL_KATEGORIE_WORKFLOW_V1.8.0_MASTER016_R10_R9_RUNTIME_DEPLOYMENT.zip`

Source:
`QUELLCODE_KATEGORIE_WORKFLOW_V1.8.0_MASTER016_R10_R9_RUNTIME_DEPLOYMENT.zip`

MASTER:
`ALLGEMEINGUELTIGER_KATEGORIE_MASTER_016_R10_R9_RUNTIME_DEPLOYMENT.zip`

## Technischer Funktionsstand

Belegt vorhanden:
- DataForSEO-Verbindungstest
- Keyword Ideas
- Keyword Suggestions
- Keyword Overview
- projektgebundene Markt-/Sprachkonfiguration
- WordPress-Seiten-/Taxonomie-Inventur
- SEO-Nachfragegate
- Search-Intent-Gate
- Affiliate-Fit-Gate
- Lossless-Coverage
- Research-Candidates
- Baseline-/Delta-Lifecycle
- Kannibalisierungs-/Ownership-Prüfpfad im Gesamtworkflow
- WordPress-`category`
- HivePress-`hp_listing_category`
- explizit gebundene Journal-Taxonomie
- Post-FINAL Dry-Run → explizites Apply → Readback/Rollback
- persistente `concept_id ↔ term_id`-Bindung
- V1.8.1 zusätzlich: allgemeines `PARENT_TOPIC_GAP`-Gate

Noch vor Hobby-Depot-Installation exakt aus dem V1.8.1-ZIP zu verifizieren:
- vollständiger Projekt-/Pferde-Stringscan
- tatsächliche Writer-Unterstützung für WordPress-Seitenanlage, nicht nur Seiten-Inventur
- exakter ZIP-Dateiname und Byteidentität gegen SHA-256
