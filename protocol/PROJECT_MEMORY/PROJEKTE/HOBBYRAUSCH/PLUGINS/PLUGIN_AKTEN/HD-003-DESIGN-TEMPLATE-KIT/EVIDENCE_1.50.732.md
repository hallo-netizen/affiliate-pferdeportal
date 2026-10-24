# HD-003 – EVIDENCE 1.50.732

STAND: 2026-10-24
STATUS: LOCAL HARD PASS / LIVE OFFEN

Artefakt:
`HOBBY_DEPOT_HD003_CYBERDUCK_1.50.732_HOBBYFINDER_BANNER_MAINSEARCH_4BEREICHE_HARDPASS.zip`

SHA-256:
`67082fab2becb01fc44d69caa059cbd69327d8ceef74308248556a5bea4fd516`

## Hobbyfinder
- „Passende Themen“ stammt aus Magazin-`journal_cat`, nicht aus Finderantworten oder Matchscore.
- Primär Registry-Unterknoten der Hobbyfinder-Seite; Fallback `alleine`, `gruppe`, `zu-zweit`.
- Reihenfolge 1.50.732: Hero/Intro → `journal_banner` → Finder → Unterthemen.
- „Zur Startseite“ / „Neu starten“ unverändert.

## Hauptsuche
- AJAX ab 2 Zeichen; Debounce 180 ms; AbortController.
- vier Gruppen: Hobbys, Magazin, Glossar, Anzeigen.
- Hobbys nur 862er Register.
- Magazin nur veröffentlichte Posts mit `journal_cat`.
- Glossar nur veröffentlichte `hdg_term`.
- Anzeigen nur `hp_listing_category` / `hp_listing`.
- gruppierte Vollergebnisseite mit denselben vier Gruppen.

## QA
- Positiv-/Negativ-Harness PASS.
- Fremde WP-Seite erscheint nicht: PASS.
- Client-AJAX-Vorschau Chromium PASS.
- 1600 / 1024 / 760 / 390 px Ergebnislayer PASS.
- Fresh-Unpack bytegleich: 936 Dateien.
- PHP 11/11 PASS.
- ZIP CRC PASS.
