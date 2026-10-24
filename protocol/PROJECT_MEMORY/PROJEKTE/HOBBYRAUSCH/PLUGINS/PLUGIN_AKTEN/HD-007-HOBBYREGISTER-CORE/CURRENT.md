# HD-007 – HOBBYREGISTER CORE – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-24
STATUS: **1.2.15 / REGISTER-DESIGN + BEREICHSSUCHE HARD PASS / LIVE OFFEN**

Plugin-ID:
`HD-007-HOBBYREGISTER-CORE`

Basis:
**1.2.14** war der tatsächliche jüngste Bildstand vor dieser Änderung.

Aktuelles Bundle:
`HOBBY_DEPOT_DESIGN_SEARCH_BUNDLE_20261024_HD003_1.50.731_HD007_1.2.15_HDG_1.0.25_HARDPASS.zip`

SHA-256:
`581736924531499b589a8349fba3b8bf42ef3ffb3755c0043be35a568d1ef4c8`

Pluginroot:
`hd-hobbyregister-core/`

## Datenstand unverändert
- 862/862 Hobbys;
- 57/57 Traits;
- 862 statische Artikel, jeweils 8 Abschnitte;
- 24 final verifizierte Masterbilder aus 1.2.14 bleiben erhalten;
- Bildstatus-/Auditdateien bleiben erhalten.

## 1.2.15
- Register-Banner vom bisherigen Platz verschoben: direkt zwischen Suche/A–Z und „Hobbygruppen entdecken“;
- derselbe Bannerplatz gilt automatisch für Übersicht, Suche, Buchstabe, Hobbygruppe und Pagination;
- Registerübersicht und Einzelprofil erhalten die Schreibschrift mit demselben Brush-Asset;
- Einzelprofil-Hero: 238 px Desktop / 190 px mobil, damit identisch flach wie die Registerübersicht;
- Bereichssuche mit AJAX-Vorschau ab 2 Zeichen, max. 8 Treffer;
- Suchquelle ausschließlich die 862 Hobbyregister-Datensätze; keine Seiten, Magazinbeiträge oder Glossarbegriffe.

## QA
- echter 862er Datenbestand geladen: PASS;
- Register-Render: Suche → Banner → Hobbygruppen Reihenfolge PASS;
- Einzelprofil-Render inkl. Brush/Claim und flacher Hero-Höhe PASS;
- serverseitiger AJAX-Endpunkt: nur Register-URLs PASS;
- Client-Suchskript mit simuliertem Fetch: PASS;
- Fresh-Unpack bytegleich zum getesteten Stand;
- Gesamtbundle PHP 22/22 PASS.

## EXAKT EINE NEXT ACTION
**Nur den kanonischen Serverordner `hd-hobbyregister-core` mit dem Bundle-Ordner überschreiben. Keine `-2`/`-3`-Kopie neu erzeugen.**
