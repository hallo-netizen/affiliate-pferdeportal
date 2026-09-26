# HOBBY DEPOT – KATEGORIE-WORKFLOW – TECHNISCHER AUDIT 2026-09-26

## Auftrag

Den vorhandenen allgemeingültigen Kategorie-Workflow als Basis für Hobby Depot prüfen, Pferde-Atelier-spezifische Bindungen ausschließen, technischen Installationsstand klären und die Hobby-Depot-Pilotstrecke vorbereiten.

## Autoritative Allgemeinbasis

Modul:
`ALLGEMEINGUELTIGE_BAUSTEINE/KATEGORIENMODELL`

Belegter Stand:
- MASTER 016 – R10/R9 Runtime Deployment
- Plugin V1.8.0
- Installer SHA-256: `4c98847e96b091955436230b721a39b5049132037546367a810d4ed642f40845`
- Source SHA-256: `1d17566f309f460e48255b78357912cf5e18b1eba2eed7654516e79c8f9fa7fd`
- MASTER SHA-256: `2e6990847c5bc32176f87c6f4b006ccdd0f3f57891c176ed5a6874edfdff942c`

## Allgemeingültigkeit

Der belegte V1.8.0-Kern ist ausdrücklich projektneutral ausgelegt.

Unterstützt:
- Content → WordPress `category`
- Marketplace/HivePress → `hp_listing_category`
- Journal → nur explizit gebundene reale Taxonomie
- WordPress-Seiten
- DataForSEO-Research
- SEO-Nachfrage-/Intent-/Kannibalisierungsprüfungen
- concept_id-basierte Baselines und Deltas
- Dry-Run → Apply → Readback
- kein Auto-Delete
- keine stillen Remaps
- keine automatische Taxonomieerzeugung

Fachentscheidungen eines Portals dürfen nicht auf ein anderes Portal vererbt werden.

## Pferde-Atelier-Abgrenzung

NICHT für Hobby Depot übernehmen:
- Pferde-Kategorien, IDs, Slugs, URLs oder Textplanpositionen;
- Pferde-Reparaturpakete 004–007;
- Pferde-Breadcrumb-Nacharbeiten;
- die am 22.09.2026 dokumentierte 1.8.1-PARENT_TOPIC_GAP-Pferde-Testkette als neue Hobby-Depot-Basis.

Hobby Depot startet auf der letzten belegten allgemeingültigen Releasebasis V1.8.0.

## Technischer Frischetest 26.09.2026

Eigener technischer Arbeitsbranch:
`hobbydepot/category-workflow-v1-20260926`

Startpunkt:
`de13db58bc20ca544700fd733d2a1a7c0c3f9668`
= Abschlussstand des allgemeinen R10-Archivs vor den späteren Pferde-spezifischen 1.8.1-Arbeiten.

Ein GitHub-Hardtest hat den im Branch vorhandenen Root-Master real entpackt.

Ergebnis:
Der dort vorhandene Root-ZIP
`ALLGEMEINGUELTIGER_KATEGORIE_MASTER_016_WORKFLOW_HARDLOCK (1).zip`
ist NICHT der belegte R10/R9-Master mit V1.8.0-Installer. Er enthält ältere Pluginstände bis V1.6.1 und historische Werkzeuge, aber nicht den gebundenen V1.8.0-Installer.

Damit darf aus diesem Root-ZIP kein V1.8.0-Installer rekonstruiert oder erfunden werden.

## Aktueller Blocker

Die exakt hashgebundenen vollständigen Bytes von V1.8.0 Source/Installer sind in den aktuell erreichbaren GitHub-Dateien nicht vorhanden.

Die Campus-Inventarakten verweisen auf ein früheres Library-Archiv, dessen angegebener Pfad in der aktuell erreichbaren Library nicht auflösbar ist.

## Technische Konsequenz

Noch KEINE Installation aus einem alten oder rekonstruierten Pluginstand.

Sobald der exakte V1.8.0-Installer oder Source mit passendem SHA wieder gebunden ist:

1. vollständiger Pferde-String-/Projektbindungs-Scan über alle Plugin-Dateien;
2. PHP-Lint;
3. gebundene Regression;
4. Installation auf Hobby Depot;
5. DataForSEO-Verbindungstest;
6. WordPress-/HivePress-Inventur;
7. Dry-Run ohne Writes;
8. genau ein kontrollierter Test-Apply;
9. neuer Request + Readback;
10. erst dann Inhalts-/Kategorieproduktion.

## Hobby-Depot-Inhaltsbindung

Planungsinput:
`../KONZEPT/VORARBEITEN_HOBBYFINDER/`

Insbesondere:
`KATEGORIEPLUGIN_HANDOFF.md`

Die Rohliste ist Forschungsinput. Ihre Zwischenüberschriften sind KEINE freigegebene Taxonomie.
