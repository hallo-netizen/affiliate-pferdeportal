# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-24
STATUS: **HD-003 1.50.744 DEKLARIERT / ARTEFAKT-RECOVERY BLOCKED / LIVE OFFEN**

Zielvertrag:
`ZIELVERTRAG_HOBBY_DEPOT_DESIGN_20261011.md`  
**ZV-HOBBYRAUSCH-DESIGN-001 / Fassung 5.5 / 2026-10-19**

Plugin-Current:
`../PLUGINS/PLUGIN_AKTEN/HD-003-DESIGN-TEMPLATE-KIT/CURRENT.md`

Fehlerautorität:
`FEHLERQUELLEN.md` → `HRD-078`

Historie / WAS+WARUM:
`../PLUGINS/UPDATEPROTOKOLL.md` → `PU-20261024-001`

## AKTUELLER BELASTBARER STAND
- deklarierter HD-003-Stand: **1.50.744**;
- Anzeigenmarkt-Startseite ist als **Root-only**-Ausbaustand dokumentiert;
- Zielreihenfolge: Breadcrumb → Banner → eigener Anzeigenmarkt-Hero → reine Anzeigen-Suche → 8 Fotokacheln → „Aktuelle Anzeigen“ → nativer HivePress-Anzeigenbestand;
- doppelte native HivePress-Root-Oberfläche soll auf Root nicht erscheinen;
- zweite/Kategorieebene bleibt vorerst nativ und ist noch nicht gestaltet;
- Live-PASS für 1.50.744 ist **nicht** belegt.

## ERSTER OFFENER BLOCKER
Das in der Plugin-Current dokumentierte 1.50.744-ZIP ist im Abschluss-Frischecheck nicht als Byte-Artefakt auffindbar. Deshalb kein erneuter Hash-/Fresh-Unpack-PASS und kein isolierter `CURRENT.zip`-Sync.

## NICHT ANFASSEN
- zentrale Hobby-Depot-Body-Achse: 1200 px;
- Header/Footer-Achse: 1440 px;
- Hobbyregister-Layout HD-007 nicht nebenbei verändern;
- Glossar- und Register-Core nicht löschen; beide bleiben Runtime-Komponenten;
- keine neue Service-Template-/Kubio-Runtime-Architektur.

## EXAKT EINE NEXT ACTION
**Das exakte HD-003-1.50.744-Artefakt wiederherstellen und SHA-verifizieren; erst danach die Anzeigenmarkt-Arbeit fortsetzen.**
