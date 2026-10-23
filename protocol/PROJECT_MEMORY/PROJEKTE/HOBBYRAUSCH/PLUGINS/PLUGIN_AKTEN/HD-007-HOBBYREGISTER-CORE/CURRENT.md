# HD-007 – HOBBYREGISTER CORE – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-23
STATUS: **1.2.12 BILDSTATUS ZENTRAL + 14 FINAL-MASTER / LOCAL HARD PASS**

Plugin-ID:
`HD-007-HOBBYREGISTER-CORE`

Artefakt:
`HOBBY_DEPOT_HOBBYREGISTER_CORE_HD007_V1.2.12_FULL_BILDSTATUS_14_MASTER.zip`

SHA-256:
`0dc95757c44424e70111c9dde5644e94a7b881fc44d8127b81d950af469a978d`

## Grundlage / Regression-Schutz
1.2.12 basiert direkt auf dem zuletzt bestandenen 1.2.10-Stand.
Am Layout-/Routingcode wurde außer den Versionsmarkern nichts geändert.

Erhalten und geprüft:
- derselbe Hobby-Depot-Container wie 1.2.10;
- `hd-content-v150616`;
- `hd-portal-section`;
- `hd-breadcrumb-wrap`;
- 862/862 Detailseiten;
- Registerübersicht;
- 57 Traits;
- 862 Artikel.

## Bilder
Verbindlicher Vertrag:
- 1 Hobby = 1 finales Masterbild;
- dasselbe Bild für Hero und Beitrag;
- 3:2;
- finales WebP 1500×1000;
- Dubletten/Fehlversuche zählen nicht.

Stand:
- DONE/verifiziert: 14;
- OPEN: 848;
- davon 382 vorhandene CORE-Bilder einzeln prüfen;
- davon 466 neue Master erzeugen.

Zentrale Autorität:
`BILDSTATUS_CURRENT.md`

Vollständige 862er Liste:
Library `/Hobby Depot/Hobbyregister/HOBBYREGISTER_BILDSTATUS_CURRENT.json`
und im Plugin `data/hobby-image-production-status-v1.json`.

## QA
- 14/14 finale Master physisch im Plugin;
- pro DONE-Hobby genau eine ausgewählte Datei;
- alle 14 Master als WebP 1500×1000;
- 862/862 Datenzeilen im Bildstatus;
- 862/862 Detailseiten lokal gerendert;
- Registerindex PASS;
- PHP-Lint PASS;
- Fresh-Unpack PASS.

## EXAKT EINE NEXT ACTION
**1.2.12 über den bestehenden Ordner `hd-hobbyregister-core` kopieren/überschreiben. Danach mit anderen Hobbyregister-/Glossararbeiten fortfahren; die Bildproduktion kann später exakt aus `BILDSTATUS_CURRENT` wieder aufgenommen werden.**
