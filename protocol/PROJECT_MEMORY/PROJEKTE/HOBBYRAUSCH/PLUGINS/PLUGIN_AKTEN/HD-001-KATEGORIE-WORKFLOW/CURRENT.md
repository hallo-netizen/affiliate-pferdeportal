# HD-001 – KATEGORIE-WORKFLOW – CURRENT

STAND: 2026-09-26
STATUS: V1.8.3 HOBBY-DEPOT-PILOT GEBAUT / LOKAL PASS / UPDATE BEREIT

## Aktueller Pilotstand

Plugin:
`Affiliate-Portal Kategorie-Workflow V1.8.3 Hobby Depot Pilot`

Installer:
`AFFILIATE_PORTAL_KATEGORIE_WORKFLOW_V1.8.3_HOBBY_DEPOT_PILOT.zip`

Installer SHA-256:
`eb442048c0853ccbf19111ce028bd0c44faf57631c22cbae37db3102c3905960`

## Änderung gegenüber V1.8.2

- eigener Hauptmenüpunkt `Kategorien` im WordPress-Backend;
- nicht mehr unter `Werkzeuge`;
- interne Rückleitungen auf den neuen Hauptmenüpunkt angepasst;
- bestehende DataForSEO-/Grundeinstellungen bleiben erhalten.

## Datenübernahme

V1.8.3 verwendet unverändert dieselben WordPress-Optionsschlüssel:
- `apkw_dataforseo_login`
- `apkw_dataforseo_password`
- `apkw_default_location_name`
- `apkw_default_language_code`

Daher werden bei einem normalen Update von V1.8.2 auf V1.8.3 bereits eingetragene Zugangsdaten, Standort und Sprache direkt weiterverwendet.

Keine Zugangsdaten werden in das ZIP kopiert oder exportiert.

## Tests

- 223/223 PASS
- PHP-Lint 16/16 PASS
- kein Pferde-/Pferde-Atelier-Bezug im Produktions-PHP

## NEXT ACTION

V1.8.3 über die bestehende V1.8.2-Installation aktualisieren. Danach prüfen:
1. Hauptmenüpunkt `Kategorien` sichtbar;
2. bestehende DataForSEO-Eingaben noch vorhanden;
3. Verbindungstest PASS.
