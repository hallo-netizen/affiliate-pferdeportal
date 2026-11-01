# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-11-01
STATUS: **1.50.783 LAUT BETREIBER IN WORDPRESS AKTIV / 1.50.785 NUR AUFGEFUNDEN / CAMPUS-ARTEFAKT UND LIVETEST BLOCKED**

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
Der aufgefundene 1.50.785-Kandidat ist weiterhin nicht als echte ZIP unabhängig wiedergeöffnet und nicht in der isolierten Campus-Ablage gesichert. WordPress meldet 1.50.783 als aktiv; ihr realer Dateibestand ist noch nicht mit 1.50.785 verglichen.

## NICHT ANFASSEN
- zentrale Hobby-Depot-Body-Achse: 1200 px;
- Header/Footer-Achse: 1440 px;
- Hobbyregister-Layout HD-007 nicht nebenbei verändern;
- Glossar- und Register-Core nicht löschen; beide bleiben Runtime-Komponenten;
- keine neue Service-Template-/Kubio-Runtime-Architektur.


## WordPress-Version und Favicon / Nachholcheck 01.11.2026

- Die Betreiber-Pluginliste beweist als übermittelte Admin-Ansicht: **Affiliate Portal Template Kit 1.50.783 aktiv**. 1.50.785 steht nicht in dieser Liste und darf nicht als installiert behauptet werden. Ein eigener authentifizierter Server-Readback wurde nicht ausgeführt.

- 1.50.785-Vollplugin-Dateieintrag vorhanden, in `/hobby rausch/`, nicht im autoritativen Campus-`ISOLIERTE_PLUGINS`-Zielordner.
- Die Originalbogen-/H-D-Vorschau ist als vorhandenes Bild lesbar; keine Neugenerierung und kein fremder Schrift-Ersatz.
- Prüfbericht 1.50.785 spricht von 11 PHP-Syntax-PASS und ZIP-Integrität, **nicht** von nachgeprüfter Liveinstallation.
- Aktueller Rohdateizugriff gescheitert; kein neues unabhängiges Unzip/Hash und kein Campus-CURRENT.zip. Details stehen ausschließlich in der HD-003-Plugin-Current und deren MANIFEST.
- Anzeigenmarkt-/Kategoriearbeit bleibt bis zum Plugin-Wiederöffnen unverändert; keine Rücksetzung auf eine alte 1.50.744-Datei.

## EXAKT EINE NEXT ACTION

**Das tatsächlich aktive HD-003 1.50.783 und das aufgefundene 1.50.785-Vollplugin als echte Roh-ZIPs verifizieren und vergleichen.** Erst nach unabhängigem PASS in den Campus übernehmen und Favicon/Anzeigenmarkt live beurteilen; nicht ungeprüft überinstallieren.
