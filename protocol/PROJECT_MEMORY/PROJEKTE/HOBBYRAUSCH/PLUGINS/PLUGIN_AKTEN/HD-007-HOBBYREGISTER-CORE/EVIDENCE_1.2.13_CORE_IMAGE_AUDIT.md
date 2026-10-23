# HD-007 – CORE-BILDPRÜFUNG 1.2.13

STAND: 2026-10-23
STATUS: LOCAL HARD PASS / LIVE OFFEN

## Auftrag
382 vorhandene CORE-Bildkandidaten ohne neue Bilderzeugung darauf prüfen, ob sie zum jeweiligen Hobby passen und als gemeinsames Bild für Hero + Beitrag technisch geeignet sind.

## Geprüfter Umfang
- 382/382 CORE-Zuordnungen geprüft
- 212/212 tatsächlich unterschiedliche Bilddateien visuell geprüft
- jede Hobby-Zuordnung separat bewertet

## Ergebnis
- Inhaltlich passend: 81
- Inhaltlich nicht passend: 301
- Technisch als gemeinsames 1500×1000-Master ohne Hochskalieren geeignet: 0
- Technisch nicht ausreichend: 382

Grund: Die vorhandenen CORE-Dateien liegen maximal bei 2071×760 px; kein Kandidat erreicht die erforderliche Höhe von 1000 px für das verbindliche 3:2-Master 1500×1000.

## Konsequenz
- 14 bereits erzeugte, geprüfte 1500×1000-Master bleiben DONE.
- 81 CORE-Bilder: Motiv PASS, aber höhere Originalquelle suchen oder neu erzeugen.
- 301 CORE-Bilder: Motiv nicht eindeutig passend; neues Masterbild erforderlich.
- Keine CORE-Datei wurde fälschlich als final markiert.

## Plugin
`HOBBY_DEPOT_HOBBYREGISTER_CORE_HD007_V1.2.13_FULL_CORE_BILDPRUEFUNG.zip`

SHA-256:
`67a052dd1f648fd8e1550c326f8efe2ad5c55b4aa75e51397ad0c7ceefcd4d0d`

## Regression-QA
- 862/862 Detailseiten PASS
- Registerübersicht PASS
- 57 Traits je Hobby unverändert
- 862 Artikel unverändert
- Hobby-Depot-Container/Breite aus bestandenem 1.2.10-Stamm erhalten
- PHP-Lint PASS
- Fresh-Unpack PASS
