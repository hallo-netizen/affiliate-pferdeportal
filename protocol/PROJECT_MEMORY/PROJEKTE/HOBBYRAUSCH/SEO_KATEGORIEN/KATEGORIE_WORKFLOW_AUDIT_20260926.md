# HOBBY DEPOT – KATEGORIE-WORKFLOW – TECHNISCHER AUDIT 2026-09-26

## Verifizierte Originalbasis

Vom Nutzer bereitgestellt und bytegenau geprüft:

- `QUELLCODE_KATEGORIE_WORKFLOW_V1.8.0_MASTER016_R10_R9_RUNTIME_DEPLOYMENT.zip`
  - SHA-256: `1d17566f309f460e48255b78357912cf5e18b1eba2eed7654516e79c8f9fa7fd`
- `ALLGEMEINGUELTIGER_KATEGORIE_MASTER_016_R10_R9_RUNTIME_DEPLOYMENT.zip`
  - SHA-256: `2e6990847c5bc32176f87c6f4b006ccdd0f3f57891c176ed5a6874edfdff942c`
- `R10_FINALER_ABSCHLUSSSTATUS_20260822.md`
  - SHA-256: `9faf2a8e624ebf638a3e80010ccfd16d651d425f71c8dfcd2b6adf5df71e3dc1`

Aus dem verifizierten MASTER extrahierter Installer:

- `AFFILIATE_PORTAL_KATEGORIE_WORKFLOW_V1.8.0_MASTER016_R10_R9_RUNTIME_DEPLOYMENT.zip`
  - SHA-256: `4c98847e96b091955436230b721a39b5049132037546367a810d4ed642f40845`

Damit sind Source, MASTER und Installer exakt an die R10-Releaseidentitäten gebunden.

## Frischer Test 26.09.2026

Auf frisch entpacktem Source:
- 216/216 PASS

Auf frisch aus MASTER extrahiertem Installer:
- 216/216 PASS

PHP-Lint:
- alle 15 PHP-Dateien PASS

Projektbindungs-Scan:
- keine Pferde-/Pferde-Atelier-Bindung in Produktions-PHP oder aktiven Schemas
- Test-/Dokudateien enthalten historische Gaumen-Testevidenz und einen Negativtestbegriff `pferd`; das ist keine Produktionsbindung

## Was V1.8.0 bereits kann

### DataForSEO
- Verbindungstest über `appendix/user_data`
- Keyword Ideas
- Keyword Suggestions
- Keyword Overview
- Markt/Sprache projektbezogen
- Paid-Research mit Preflight/Bestätigung und Claim/Resume-Schutz

### Struktur-/Konzeptworkflow
14 Stufen:
MASTER LOCK → PROJECT CONTRACT → INITIAL TREE → INITIAL VISIBLE REVIEW → FREE PREFLIGHT → GLOBAL COVERAGE → GLOBAL GAP DECISION → GLOBAL GAP VISIBLE REVIEW → DETAIL PREFLIGHT → DETAIL RESEARCH → DATA-INFORMED CORRECTION → READ-ONLY TOTAL AUDIT → FINAL VISIBLE REVIEW → FINAL VALIDATION.

Das Plugin besitzt:
- SEO-Nachfrageevidenz
- Search-Intent-Prüfung
- Keyword-Ownership
- Kannibalisierungsprüfung
- Global-/Cluster-Coverage
- Spezialisierungs-/Residual-Coverage
- Affiliate-Fit
- persistente Baseline/Deltas
- concept_id als stabile Identität

Wichtig:
DataForSEO liefert Evidenz, aber erfindet nicht autonom den INITIAL TREE.
Der erste Strukturentwurf muss als Projekt-/Strukturpaket vorliegen; danach führt das Plugin Research, Lückenprüfung und datenbasierte Korrektur durch.

### WordPress/HivePress-Ausgabe
Post-FINAL-Writer unterstützt in V1.8.0:
- WordPress `category`
- HivePress `hp_listing_category`
- explizit gebundene Journal-Taxonomie
- parent-first CREATE/UPDATE
- signierter Dry-Run
- explizites Apply
- Readback
- Rollback
- Idempotenz
- Live-Drift-Blockade
- persistente concept_id↔term_id-Bindung

## Kritische Grenze

Der V1.8.0 Post-FINAL-Writer schreibt ausschließlich Taxonomie-Terme.

`wordpress_page` wird im Inventar/Comparator gelesen und kann als Strukturziel geprüft werden, aber `APKW_DeploymentWriter` akzeptiert beim Schreiben nur `wordpress_taxonomy`.

**V1.8.0 erzeugt also keine WordPress-Seiten.**

Ebenfalls nicht enthalten:
- WordPress-Menüs
- autonome Hintergrund-Paid-Calls

## Neuester Entwicklungsstand danach

Belegt ist zusätzlich V1.8.1 vom 22.09.2026:
- allgemeines `PARENT_TOPIC_GAP`-Gate
- 220/220 PASS
- PHP-Lint 15/15 PASS
- Fresh-ZIP 220/220 PASS
- ZIP SHA-256 `1915922977b3d803b25ed9458e5eb40ae7dd30c37f9d3c763720d5e47b25ac6b`
- noch nicht live installiert

Kein belegter V1.8.2+-Stand gefunden.

Die V1.8.1-ZIP-Bytes sind derzeit nicht gebunden. Deshalb bleibt V1.8.0 die neueste vollständig byteverifizierte Basis.

## Ablage

Exakte V1.8.0-Artefakte wurden zusätzlich persistent gespiegelt unter:

- `/Campus-Archiv/PROJEKTE/HOBBYRAUSCH/SEO_KATEGORIEN/HD-001-KATEGORIE-WORKFLOW/`
- `/Campus-Archiv/PROJEKTE/HOBBYRAUSCH/PLUGINS/HD-001-KATEGORIE-WORKFLOW/`

## Erster offener Punkt

Vor Installation auf Hobby Depot entscheiden/entwickeln:
1. fehlende WordPress-Seitenerzeugung ergänzen;
2. allgemeines V1.8.1-PARENT_TOPIC_GAP-Gate übernehmen;
3. danach komplette Regression als neue Hobby-Depot-Version;
4. erst dann Installation → DataForSEO → Dry-Run → Test-Apply → Readback.
