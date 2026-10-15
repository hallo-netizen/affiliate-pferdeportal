# HD-003 – HOBBY DEPOT DESIGN / TEMPLATE KIT – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-15
STATUS: **TEMPLATE-KIT 1.50.650 BLEIBT AKTIV UND UNANGETASTET / HERO-HELPER 1.50.662 IST IN-PLACE-UPDATE VON 1.50.660 / LOKAL E2E PASS**

## Aktiver Grundstand
Affiliate Portal Template Kit **1.50.650**.

## Aktueller Hero-Helper
`HOBBY_DEPOT_HERO_REPLACE_ONLY_1.50.662.zip`

SHA-256:
`6bf59929a201f3a0731ff7ea52ff33c3a47186835ff694c8715bdc134238b904`

## Update-Identität
Gleich wie 1.50.660:
- Pluginordner: `hobby-depot-hero-replace-only-150660`
- Hauptdatei: `hobby-depot-hero-replace-only-150660.php`

Daher Überinstallation/Ersetzung statt zweitem Plugin.

## Wirkung
- ersetzt exakt 30 live verworfene Hero-Dateien;
- Mapping unverändert;
- übrige 35 Heroes unverändert;
- Template-Kit-PHP unverändert;
- Routing/Templates/CSS/Karten/Architektur unverändert.

## Lokaler Update-E2E
Bereits aktives 1.50.660 simuliert → Ordner in-place mit 1.50.662 ersetzt → Activation Hook NICHT erneut aufgerufen → one-shot admin_init führt Austausch aus:
- 30 geändert;
- 35 unverändert;
- Mapping unverändert;
- 0 PHP-Diffs;
- PASS.

## NEXT ACTION
**1.50.662 über das vorhandene 1.50.660 installieren/ersetzen.**
