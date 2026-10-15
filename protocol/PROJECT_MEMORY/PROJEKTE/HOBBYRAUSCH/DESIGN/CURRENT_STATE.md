# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-15
STATUS: **SEITE ERREICHBAR / TEMPLATE-KIT 1.50.650 EINGEFROREN / 1.50.662 VERWORFEN WEGEN ADMIN_INIT-GATE / 1.50.663 FRONTEND-IN-PLACE-UPDATE LOKAL E2E PASS / LIVE-VISUALPRÜFUNG OFFEN**

## Harte Sperre
Keine Änderungen an Template-Kit-PHP, Routing, Templates, CSS, Mapping, Karten, Seitenstruktur oder Architektur.

## Aktiver Grundstand
Affiliate Portal Template Kit **1.50.650** bleibt unangetastet.

## Fehler 1.50.662
1.50.662 führte den 30er-Austausch nach In-Place-Overwrite nur über `admin_init` aus.
Wenn nach der Überinstallation direkt eine Frontend-Seite geprüft wurde, lief der Austausch nicht.
Die vorherige Cache-Erklärung war damit falsch und ist verworfen.

## Aktueller Kandidat
`HOBBY_DEPOT_HERO_REPLACE_ONLY_1.50.663.zip`

SHA-256:
`3009b23d0cae38cfb36d3f7c20507879df33139202c4789399d4b8987db948f1`

## Update-Identität
Wie 1.50.660/1.50.662:
- Ordner: `hobby-depot-hero-replace-only-150660`
- Hauptdatei: `hobby-depot-hero-replace-only-150660.php`

Damit echtes In-Place-Update/Überinstallation.

## Änderung gegenüber 1.50.662
Nur der One-Shot-Ausführungshook des separaten Hero-Helper-Plugins:
- vorher: `admin_init`
- jetzt: `plugins_loaded`

Damit läuft der Austausch beim **allerersten folgenden WordPress-Request**, auch bei direkter Frontend-Prüfung.

## Wirkung
- exakt 30 neue 600×220-Hero-Dateien;
- nur die 30 Nutzer-Hard-Reject-Kategorien;
- bestehendes 65er-Mapping wird nur gelesen;
- übrige 35 Hero-Zieldateien unverändert;
- Template-Kit-PHP 0 Änderungen;
- Templates/Routing/CSS/Karten/Architektur unverändert.

## Lokaler Frontend-E2E-Nachweis
Ausgang:
- pristine Template-Kit 1.50.650;
- 1.50.660-Bildzustand hergestellt;
- aktiver Helperpfad in-place durch 1.50.663 ersetzt;
- **kein Activation Hook**;
- **kein admin_init**;
- nur echter Frontend-Lebenszykluspunkt `plugins_loaded`.

Ergebnis:
- Status PASS;
- APPLIED=1;
- exakt 30 erwartete Hero-Dateien geändert;
- 35 unverändert;
- Mapping byte-identisch;
- 0 Template-Kit-PHP-Diffs.

## EXAKT EINE NEXT ACTION
**1.50.663 über das vorhandene Hero-Replace-Plugin überinstallieren und danach direkt eine betroffene Frontend-Seite aufrufen.**
