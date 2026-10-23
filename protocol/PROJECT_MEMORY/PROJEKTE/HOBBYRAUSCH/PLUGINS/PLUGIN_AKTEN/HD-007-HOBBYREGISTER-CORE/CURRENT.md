# HD-007 – HOBBYREGISTER CORE – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-23
STATUS: **1.1.7 UI FIX LOCAL HARD PASS / LIVE LOAD STATE OFFEN**

Plugin-ID:
`HD-007-HOBBYREGISTER-CORE`

Artefakt:
`HOBBY_DEPOT_HOBBYREGISTER_CORE_HD007_V1.1.7_FULL_UI_FIX.zip`

SHA-256:
`790fd916f06a65d1b6736968148410470536aecedacfac5ce1b2fb5f24877f65`

Größe:
1,349,633 Bytes.

Hauptordner:
`hd-hobbyregister-core/`

## Diagnose Artikelverlust

1.1.6 rendert lokal weiterhin den vollständigen 3D-Druck-Artikel mit 8 Abschnitten.
Die Layoutänderung selbst entfernt den Artikel nicht.

Wenn live kein Artikel erscheint, ist der Live-Ladezustand von HD-007 nicht identisch zum geprüften Paket.
Ein möglicher konkreter Auslöser ist ein kurzfristig fehlender Pluginordner während eines Vollersatzes, wodurch WordPress das Plugin deaktivieren kann.

## 1.1.7

- aktiver A–Z-Buchstabe stark sichtbar;
- `Alle` als aktiver Zustand ohne Buchstabenfilter;
- aktive Gruppe deutlicher;
- gefiltert `X Hobbys` statt `X Treffer`;
- Pagination oben und unten;
- `Zur Register-Startseite` statt `Filter zurücksetzen`;
- Bodybreite / Hero-Fix aus 1.1.6 erhalten.

## E2E

`/hobbyregister/?hr_letter=S`
- aktive S-Markierung PASS;
- Count PASS;
- Pagination oben/unten PASS;
- Rücklink PASS.

`/hobbyregister/3d-druck/`
- kompletter Artikel PASS;
- erster und letzter Abschnitt PASS;
- 8 Abschnitte PASS;
- HTML ca. 24 KB.

PHP-Lint/Fresh-Unpack PASS.

Evidence:
`EVIDENCE_1.1.7.md`

## EXAKT EINE NEXT ACTION

**1.1.7 über den bestehenden aktiven Ordner `wp-content/plugins/hd-hobbyregister-core/` kopieren/überschreiben, ohne den Ordner vorher zu löschen. Danach prüfen, dass `Hobby Depot Hobbyregister Core` in WordPress weiterhin aktiv ist, und Registerstart + ein Profil neu laden.**
