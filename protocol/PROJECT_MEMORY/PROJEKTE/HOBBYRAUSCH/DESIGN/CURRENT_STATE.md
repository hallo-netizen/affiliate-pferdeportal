# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-24
STATUS: **HD-003 1.50.731 / HD-007 1.2.16 / REGISTER-SUCHFELD BREITENFIX / LIVE OFFEN**

Zielvertrag:
**ZV-HOBBYRAUSCH-DESIGN-001 Fassung 5.5 / 2026-10-19**

## HD-003

HD-003 steht auf 1.50.731. Die 1200-px-Body-Achse aus 1.50.730 bleibt unverändert; Header und Footer bleiben unberührt.

## Hobbyregister / HD-007

Die früheren Zwischenstände mit eigenen Breitenwerten 1050/1180/1200 px sind verworfen.

Seit HD-007 1.2.10 verwendet das Hobbyregister die echten Hobby-Depot-Containerklassen aus HD-003:
- `hd-content-v150616`;
- `hd-portal-section`;
- `hd-breadcrumb-wrap`.

Lokaler Chromium-Vergleich gegen Hobby-Depot-Kategorie:
1600 / 1440 / 1366 / 1180 / 1024 / 761 / 760 / 390 px → linke Kante, rechte Kante und Gesamtbreite jeweils **0 px Differenz**.

Der Nutzer bestätigte diesen sichtbaren Breitenstand anschließend live mit **„pass“**.

HD-007 1.2.15 verändert den zentralen 1200-px-Containerstand nicht.

## Profil-Hero / Inhalt

- Hobbytitel als H1;
- kurzer gruppenspezifischer Claim;
- grüne Schreibschrift + gelber Brush;
- 862/862 Detailprofile;
- 57/57 Traits;
- 862 statische Artikel mit je 8 Abschnitten;
- Sidebar-Überschrift `Selbe Hobbygruppe`;
- unterer Detail-Banner entfernt.

## Bilder

Der laufende Hobbyregister-Bildstatus ist technische HD-007-Arbeit und wird nicht hier dupliziert.

Aktuelle technische Autorität:
`../PLUGINS/PLUGIN_AKTEN/HD-007-HOBBYREGISTER-CORE/CURRENT.md`

## EXAKT EINE NEXT ACTION

**Hobbyregister-Layout nicht weiter verändern. Nur bei einer neuen sichtbaren Designbeanstandung erneut im DESIGN-Scope arbeiten; Bild-/Pluginarbeit über HD-007 führen.**


## 24.10.2026 – zentrale Body-Breite 1200 px
- HD-003 auf 1.50.730.
- Hobby-Depot-Inhaltsachse zentral auf maximal 1200 px gesetzt.
- Header und Footer behalten ihre bisherige 1440-px-Variable und ihre Geometrie.
- Native ListingHive-/WordPress-Inhaltsseiten werden ebenfalls auf dieselbe 1200-px-Außenachse zentriert.
- Glossar-Übersicht, Glossar-Einzelseite und Hobbyregister wurden gegen die zentrale Achse geprüft; die historische feste 1240-px-Glossar-Einzelseite wird zentral auf 1200 px gekappt.
- Browservergleich 1.50.729 → 1.50.730 bei 1600 / 1366 / 1024 / 760 / 390 px: Headerbreite Delta 0 px, Footerbreite Delta 0 px.
- Finales ZIP erneut entpackt und daraus geprüft: PASS.
- Artefakt: `HOBBY_DEPOT_HD003_CYBERDUCK_1.50.730_BODY_1200_HEADER_FOOTER_UNBERUEHRT_HARDPASS.zip`
- SHA-256: `b31c2528ad049d9974104cd8de35b39cf69bf701efe429104c8c4218bd798279`


## 24.10.2026 – Magazinlink / Hobbyregister / Bereichssuchen
- Hobbymagazin-Kachel „Wissen & Glossar“ führt jetzt kanonisch auf `/magazin/wissen-glossar/`.
- Hobbyregister HD-007 1.2.15 basiert auf dem tatsächlichen 1.2.14-Bildstand.
- Register-Banner steht auf Registerübersicht, Suche, Buchstabe, Hobbygruppe und Pagination direkt zwischen Suche/A–Z und „Hobbygruppen entdecken“.
- Register-Hero: Schreibschrift + handgezeichneter Brush auf Übersicht und Einzelprofil.
- Einzelprofil-Hero auf dieselbe flache Höhe wie Registerübersicht vereinheitlicht: 238 px Desktop / 190 px mobil.
- Registersuche: AJAX-Vorschau ab 2 Zeichen, maximal 8 Treffer, ausschließlich aus den 862 Hobbyregister-Datensätzen.
- Glossarsuche HDG 1.0.25: AJAX-Vorschau ab 2 Zeichen, maximal 8 Treffer, ausschließlich veröffentlichte `hdg_term`; normale Posts und Drafts werden verworfen.
- Daten unverändert: Hobbyregister 862 Hobbys / 57 Traits / 862 Artikel × 8 Abschnitte; Glossar 308 Begriffe / 13 Batches.
- Bundle: `HOBBY_DEPOT_DESIGN_SEARCH_BUNDLE_20261024_HD003_1.50.731_HD007_1.2.15_HDG_1.0.25_HARDPASS.zip`
- SHA-256: `581736924531499b589a8349fba3b8bf42ef3ffb3755c0043be35a568d1ef4c8`


## 24.10.2026 – HD-007 1.2.16 Suchfeld-Breitenfix
- Live-Screenshot zeigte: Suchzeile selbst war breit, das Input blieb jedoch auf Browser-Standardbreite.
- Ursache: am Input fehlte `width:100%`; die Grid-Spalte war korrekt.
- Korrektur ausschließlich im Register:
  - Input 100 % der verfügbaren Suchspalte;
  - sichtbares Label „Hobby suchen“ entfernt;
  - Placeholder „Hobby suchen …“;
  - AJAX-Vorschau unverändert.
- Browser-Geometrietest 1600 / 1024 / 760 / 390 px PASS.
- Artefakt: `HOBBY_DEPOT_HOBBYREGISTER_CORE_HD007_V1.2.16_SEARCH_WIDTH_HARDPASS.zip`
- SHA-256: `3e5f46b1c2a7183df1b49d987ee8712c7c059eda18507de31de6d2a782cab78a`
