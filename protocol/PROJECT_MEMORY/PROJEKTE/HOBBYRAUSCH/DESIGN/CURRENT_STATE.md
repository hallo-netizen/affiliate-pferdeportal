# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-11-01
STATUS: **HD-003 1.50.785 AUFGEFUNDEN / CAMPUS-ARTEFAKT UND LIVE-PASS BLOCKED**

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
- ältere Campus-Deklaration vom 24.10.: **1.50.744**; neuer aufgespürter Dateieintrag 1.50.785, echter Byte-Readback noch nicht möglich;
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


## Favicon / HD-003 Nachholcheck 01.11.2026

- 1.50.785-Vollplugin-Dateieintrag vorhanden, in `/hobby rausch/`, nicht im autoritativen Campus-`ISOLIERTE_PLUGINS`-Zielordner.
- Die Originalbogen-/H-D-Vorschau ist als vorhandenes Bild lesbar; keine Neugenerierung und kein fremder Schrift-Ersatz.
- Prüfbericht 1.50.785 spricht von 11 PHP-Syntax-PASS und ZIP-Integrität, **nicht** von nachgeprüfter Liveinstallation.
- Aktueller Rohdateizugriff gescheitert; kein neues unabhängiges Unzip/Hash und kein Campus-CURRENT.zip. Details stehen ausschließlich in der HD-003-Plugin-Current und deren MANIFEST.
- Anzeigenmarkt-/Kategoriearbeit bleibt bis zum Plugin-Wiederöffnen unverändert; keine Rücksetzung auf eine alte 1.50.744-Datei.

## EXAKT EINE NEXT ACTION

**Das echte HD-003-Vollplugin 1.50.785 erneut als Rohdatei abrufen und unabhängig prüfen; anschließend nur bei nachgewiesenem PASS in der bestehenden Campus-Pluginakte sichern.** Erst danach Favicon live und Anzeigenmarktänderungen prüfen.
