# HD-007 – HOBBYREGISTER CORE – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-24
STATUS: **1.2.16 / REGISTER-SUCHFELD BREITENFIX / AJAX UNVERÄNDERT / LIVE OFFEN**

Plugin-ID:
`HD-007-HOBBYREGISTER-CORE`

Basis:
**1.2.14** war der tatsächliche jüngste Bildstand vor dieser Änderung.

Aktuelles Artefakt:
`HOBBY_DEPOT_HOBBYREGISTER_CORE_HD007_V1.2.16_SEARCH_WIDTH_HARDPASS.zip`

SHA-256:
`3e5f46b1c2a7183df1b49d987ee8712c7c059eda18507de31de6d2a782cab78a`

Pluginroot:
`hd-hobbyregister-core/`

## Datenstand unverändert
- 862/862 Hobbys;
- 57/57 Traits;
- 862 statische Artikel, jeweils 8 Abschnitte;
- 24 final verifizierte Masterbilder aus 1.2.14 bleiben erhalten;
- Bildstatus-/Auditdateien bleiben erhalten.

## 1.2.15
- Register-Banner zwischen Suche/A–Z und Hobbygruppen.
- Schreibschrift + Brush auf Übersicht und Einzelprofil.
- Einzelprofil-Hero 238 px Desktop / 190 px mobil.
- exklusive Register-AJAX-Suche.

## 1.2.16
- sichtbare Überschrift „Hobby suchen“ entfernt;
- Placeholder im Eingabefeld: „Hobby suchen …“;
- Eingabefeld erhält `width:100%` und füllt wieder die komplette verfügbare Suchspalte bis zum Suchbutton;
- AJAX-Suche aus 1.2.15 funktional unverändert.

## QA
- echter 862er Datenbestand geladen: PASS;
- Register-Render: Suche → Banner → Hobbygruppen Reihenfolge PASS;
- Einzelprofil-Render inkl. Brush/Claim und flacher Hero-Höhe PASS;
- serverseitiger AJAX-Endpunkt: nur Register-URLs PASS;
- Client-Suchskript mit simuliertem Fetch: PASS;
- Render-Test: keine sichtbare Label-Zeile, Placeholder PASS, aria-label PASS;
- Browser-Geometrietest bei 1600 / 1024 / 760 / 390 px: Inputbreite = komplette verfügbare Feldbreite, PASS;
- Daten und Assets byteidentisch zu 1.2.15;
- Fresh-Unpack bytegleich zum getesteten Stand;
- PHP 4/4 PASS; ZIP CRC PASS; exakt ein Root `hd-hobbyregister-core/`.

## EXAKT EINE NEXT ACTION
**Nur den kanonischen Serverordner `hd-hobbyregister-core` mit dem Bundle-Ordner überschreiben. Keine `-2`/`-3`-Kopie neu erzeugen.**
