# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-15
STATUS: **SEITE ERREICHBAR / TEMPLATE-KIT 1.50.650 EINGEFROREN / 1.50.661 VERWORFEN WEGEN FALSCHEM INSTALLATIONSWEG / 1.50.662 IN-PLACE-UPDATE VON 1.50.660 LOKAL E2E PASS / LIVE-VISUALPRÜFUNG OFFEN**

## Harte Sperre
Keine Änderungen an Template-Kit-PHP, Routing, Templates, CSS, Mapping, Karten, Seitenstruktur oder Architektur.

## Aktiver Grundstand
Affiliate Portal Template Kit **1.50.650** bleibt unangetastet.

## Verworfen
- 1.50.651
- Repair Installer 1.50.657
- Recovery 1.50.658
- Hero Images ONLY 1.50.659
- Hero Replace ONLY 1.50.660 als finaler Bildstand für die 30 live verworfenen Heroes
- Hero Replace 30 ONLY 1.50.661: funktionaler Bildpatch, aber **falscher Pluginordner**, daher separate Neuinstallation statt Überinstallation von 1.50.660

## Aktueller Kandidat
`HOBBY_DEPOT_HERO_REPLACE_ONLY_1.50.662.zip`

SHA-256:
`6bf59929a201f3a0731ff7ea52ff33c3a47186835ff694c8715bdc134238b904`

## Installationsweg 1.50.662
1.50.662 verwendet **exakt denselben Pluginordner und dieselbe Hauptdatei wie 1.50.660**:
- Ordner: `hobby-depot-hero-replace-only-150660`
- Hauptdatei: `hobby-depot-hero-replace-only-150660.php`

Damit erkennt WordPress den Upload als **Überinstallation/Ersetzung des vorhandenen 1.50.660-Plugins**, nicht als separates Plugin.

## Wirkung
- exakt 30 neue 600×220-Hero-Dateien;
- nur die 30 Nutzer-Hard-Reject-Kategorien;
- vorhandenes 65er-Mapping wird nur gelesen, niemals geschrieben;
- übrige 35 Hero-Zieldateien unverändert;
- Template-Kit: 0 PHP-Diffs;
- Templates/Routing/CSS/Karten/Architektur unverändert.

## Lokaler E2E-Nachweis – echter In-Place-Overwrite-Pfad
Ausgangslage:
- echtes 1.50.650 Template-Kit;
- 1.50.660 als aktives Helper-Plugin simuliert;
- dessen 65er-Austausch zunächst erfolgreich ausgeführt.

Dann:
- vorhandenen 1.50.660-Pluginordner durch 1.50.662 ersetzt;
- **aktive Plugin-Dateireferenz blieb exakt gleich**;
- Aktivierungs-Hook bewusst NICHT erneut ausgelöst;
- 1.50.662 führte den 30er-Austausch einmalig über `admin_init` aus.

Ergebnis:
- PASS;
- exakt 30 Hero-Zieldateien geändert;
- exakt 35 Hero-Zieldateien unverändert;
- Mapping byte-identisch;
- alle 55 Template-Kit-PHP-Dateien byte-identisch;
- keine .tmp/.bak-Reste.

## EXAKT EINE NEXT ACTION
**1.50.662 über das vorhandene 1.50.660-Plugin installieren/ersetzen. Keine separate Installation von 1.50.661.**
