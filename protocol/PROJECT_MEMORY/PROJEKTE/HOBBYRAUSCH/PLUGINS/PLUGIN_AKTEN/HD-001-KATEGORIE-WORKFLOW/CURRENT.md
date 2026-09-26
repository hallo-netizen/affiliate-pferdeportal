# HD-001 – KATEGORIE-WORKFLOW – CURRENT

STAND: 2026-09-26
STATUS: V1.8.2 HOBBY-DEPOT-PILOT GEBAUT / LOKAL PASS / LIVE-TEST ALS NÄCHSTES

## Rolle

Einzige aktuelle Pluginwahrheit für HD-001.

## Aktueller Pilotstand

Plugin:
`Affiliate-Portal Kategorie-Workflow V1.8.2 Hobby Depot Pilot`

Installer:
`AFFILIATE_PORTAL_KATEGORIE_WORKFLOW_V1.8.2_HOBBY_DEPOT_PILOT.zip`

Installer SHA-256:
`21e835920a9141a6383278a4463395adcffb1f3107e035cda721560f40c31133`

Source:
`QUELLCODE_KATEGORIE_WORKFLOW_V1.8.2_HOBBY_DEPOT_PILOT.zip`

Source SHA-256:
`8b44ef81b07ca140a4cb864de733bdfa5d54493ab64c7248fb55769b8400cc51`

Technischer Pilotinput:
`HOBBY_DEPOT_KATEGORIE_PILOT_KONZEPT.json`

## Was V1.8.2 neu kann

- Konzept-/Seed-Eingabe als Startpunkt;
- kostenloser Preflight vor jedem bezahlten DataForSEO-Lauf;
- SEO-gestützter Erstentwurf für Content/Hobby-Struktur, Marketplace/HivePress und Magazin;
- keine neue Struktur ohne positive gebundene SEO-Evidenz;
- vorhandene Keyword-/Intent-/Ownership-/Kannibalisierungs-/Coverage-/Affiliate-Fit-Gates bleiben aktiv;
- WordPress-Seiten können nach FINAL als Entwurf angelegt/aktualisiert werden;
- WordPress-Kategorien, HivePress `hp_listing_category` und gebundene Journal-Taxonomien bleiben unterstützt;
- gemischtes Deployment Seiten + Taxonomien;
- Dry-Run → explizites Apply → Readback → Rollback;
- Idempotenz und Live-Drift-Blockade;
- logische Parent-Bindung auch über unterschiedliche WordPress-Objekttypen.

## Harte Tests

- bestehende Suite + neue Tests: 223/223 PASS;
- Fresh-Unpack-Installer: 223/223 PASS;
- PHP-Lint: 16/16 PASS;
- kein Pferde-/Pferde-Atelier-Bezug im Produktions-PHP;
- negativer SEO-Test: keine positive Marketplace-Evidenz → keine erfundene Marketplace-Kategorie;
- Slug-Konflikt → vor Write BLOCKED;
- Rollback gemischtes Deployment PASS;
- zweiter identischer Lauf → 0 neue Writes.

## Herkunft / unveränderte Basis

V1.8.2 baut auf der byteverifizierten allgemeinen V1.8.0-R10-Basis auf.

Historisch dokumentiert ist zusätzlich V1.8.1 mit allgemeinem `PARENT_TOPIC_GAP`-Gate.
Die exakten V1.8.1-Bytes sind nicht gebunden; dieses Gate ist im aktuellen V1.8.2-Pilot noch NICHT als Codeport übernommen.

## Artefaktablage

Persistente Spiegelung:
`/Campus-Archiv/PROJEKTE/HOBBYRAUSCH/PLUGINS/HD-001-KATEGORIE-WORKFLOW/`

## Erster offener Punkt

Noch kein echter Hobby-Depot-WordPress-/DataForSEO-Live-Test ausgeführt.

## NEXT ACTION

V1.8.2 Pilot auf Hobby Depot installieren und zunächst nur aktivieren + DataForSEO-Verbindungstest ausführen. Danach Konzept-Preflight ohne bezahlte Recherche prüfen; erst anschließend kontrollierten SEO-Testlauf starten.
