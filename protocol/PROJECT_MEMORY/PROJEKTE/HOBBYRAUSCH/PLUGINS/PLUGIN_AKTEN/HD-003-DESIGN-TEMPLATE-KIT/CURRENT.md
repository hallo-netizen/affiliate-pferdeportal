# HD-003 – HOBBY DEPOT DESIGN / TEMPLATE KIT – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-15
STATUS: **TEMPLATE-KIT 1.50.650 BLEIBT AKTIV UND UNANGETASTET / HERO-HELPER 1.50.663 IST IN-PLACE-UPDATE / FRONTEND-E2E PASS**

## Aktiver Grundstand
Affiliate Portal Template Kit **1.50.650**.

## Nicht verwenden
1.50.651, Repair Installer 1.50.657, Recovery 1.50.658, Hero 1.50.659, 1.50.660 als finaler Bildstand, 1.50.661, 1.50.662.

## Aktueller Hero-Helper
`HOBBY_DEPOT_HERO_REPLACE_ONLY_1.50.663.zip`

SHA-256:
`3009b23d0cae38cfb36d3f7c20507879df33139202c4789399d4b8987db948f1`

Update-Identität unverändert:
- `hobby-depot-hero-replace-only-150660/`
- `hobby-depot-hero-replace-only-150660.php`

## Wirkung
- 30 verworfene Heroes ersetzen;
- 35 übrige Heroes unverändert;
- Mapping unverändert;
- Template-Kit-PHP unverändert;
- Routing/Templates/CSS/Karten/Architektur unverändert.

## Frontend-E2E
Aktiven Vorgänger in-place überschrieben, Activation Hook nicht ausgelöst, admin_init nicht ausgelöst, erster Folge-Request = Frontend/plugins_loaded:
- 30 geändert;
- 35 unverändert;
- Mapping unverändert;
- 0 PHP-Diffs;
- PASS.

## NEXT ACTION
**1.50.663 überinstallieren; anschließend direkt betroffene Frontend-Seite prüfen.**


## Nachprüfung 2026-10-15 – 1.50.663 Positiv/Negativ
Nach Nutzerforderung vollständig nachgeholt: **14/14 Tests PASS**.

Positiv:
- echter Frontend-In-Place-Pfad ohne Activation Hook und ohne admin_init: exakt 30 erwartete Hero-Dateien geändert;
- 35 übrige Hero-Dateien unverändert;
- Mapping unverändert;
- 30/30 Zielbilder identisch zum Payload;
- Wiederholungsaufruf erzeugt keine zusätzliche Änderung.

Negativ – jeweils sauberer ABORT ohne weitere Template-Kit-Änderung:
- Template-Kit-Hauptdatei fehlt;
- falsche Template-Kit-Version;
- Mapping nicht exakt 65;
- benötigter Hero-Slug fehlt;
- Pfad-Traversal im Mapping;
- doppelte Hero-Zieldatei;
- Payload nur 29 Dateien;
- falsche Payload-Dimension;
- gemappte Zieldatei fehlt.

Zusätzlich PASS:
- ZIP-Integrität;
- PHP-Syntax;
- Pluginordner + Main-Dateipfad identisch zu 1.50.660 für echte Überinstallation.
