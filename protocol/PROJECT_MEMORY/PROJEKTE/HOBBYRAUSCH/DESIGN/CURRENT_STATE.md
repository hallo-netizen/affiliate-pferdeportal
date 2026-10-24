# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-24
STATUS: **HD-003 1.50.736 / SERVICE-SEITEN FEINKORREKTUR / LIVE OFFEN**

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


## 24.10.2026 – HD-003 1.50.732 Hobbyfinder + Hauptsuche
- Hobbyfinder-Block „Passende Themen“ aus dem oberen Ablauf entfernt und nach den eigentlichen Finder verschoben.
- Der Block ist redaktionell, nicht Ergebnis des Finder-Scores: Registry-`journal_cat`-Kinder, Fallback `alleine` / `gruppe` / `zu-zweit`.
- Oben steht stattdessen die vorhandene Magazin-Bannerfläche `journal_banner`.
- Topnav „Zur Startseite“ / „Neu starten“ bleibt unverändert.
- globale Hauptsuche jetzt als eigene AJAX-Vorschau analog zum Pferdeatelier-Prinzip.
- Hobby-Depot-Viererstruktur: Hobbys · Magazin · Glossar · Anzeigen.
- gruppierte Ergebnis-Vollseite mit identischer Viererstruktur.
- Bereichssuchen in Hobbyregister/Glossar bleiben davon getrennt.
- Artefakt: `HOBBY_DEPOT_HD003_CYBERDUCK_1.50.732_HOBBYFINDER_BANNER_MAINSEARCH_4BEREICHE_HARDPASS.zip`
- SHA-256: `67082fab2becb01fc44d69caa059cbd69327d8ceef74308248556a5bea4fd516`


## 24.10.2026 – HD-003 1.50.733 Suchlayer nicht mehr abgeschnitten
- Live-Screenshot: vierteilige Hauptsuche lief im geteilten Browser rechts aus dem Viewport.
- Ergebnislayer wird nun dynamisch auf maximal 1180 px Breite gesetzt und mit 16 px Abstand innerhalb des aktuellen Browserfensters gehalten.
- Vier-Bereich-Suchlogik unverändert.
- Artefakt: `HOBBY_DEPOT_HD003_CYBERDUCK_1.50.733_MAINSEARCH_VIEWPORT_FIX_HARDPASS.zip`
- SHA-256: `d0268782c88e17c5665ee71ae38d564c6600c01e7a6da38e8ce48151f612a9b2`


## 24.10.2026 – HD-003 1.50.734 Suchergebnisseite
- Flyout funktionierte, Enter-Ergebnisseite nicht.
- Ursache: Ergebnisseiten-Renderer gab HTML zurück, das Template gab diesen Rückgabewert nicht aus.
- Jetzt echte gruppierte Seite für Teilbegriffe wie „Holz“ mit denselben vier Bereichen wie das Flyout.
- Routing der eigenen Hauptsuche zusätzlich unabhängig von `is_search()` gehärtet.
- Artefakt: `HOBBY_DEPOT_HD003_CYBERDUCK_1.50.734_SEARCH_RESULTS_PAGE_HARDPASS.zip`
- SHA-256: `dd275eb536801e7a34bec1aac338fe6c6a6473bd3edf21d93516eba4a9307543`


## 24.10.2026 – HD-003 1.50.735 Service-/Footer-Seiten
- Einheitlicher Bild-Hero für Impressum, Disclaimer, Datenschutz, Werbebedingungen, Werben, Preise, Kontakt und FAQ.
- Grüner „Hobby Depot“-Kicker entfernt.
- Titelrahmen entfernt.
- Preise: Tabellen auf volle Inhaltsbreite, Kubio-/Block-Wrapper um Tabellen neutralisiert.
- Preise + Disclaimer: fette Zwischenüberschriften mit sauberem Absatz darüber/darunter.
- vorhandenes neutrales WebP wiederverwendet, kein neues Asset.
- Artefakt: `HOBBY_DEPOT_HD003_CYBERDUCK_1.50.735_SERVICE_PAGES_DESIGN_LOCALPASS.zip`
- SHA-256: `105a806d132aac186313c3e95e87e2791dfe9a31926d2924d4f4553a78d6045a`
- QA: PHP 11/11, ZIP/Fresh-Unpack bytegleich; Live-Sichtprüfung nach Upload offen.


## 24.10.2026 – HD-003 1.50.736
- Service-Hero bleibt, aber Abstand zum eigentlichen Inhalt auf 18 px Desktop / 16 px mobil reduziert.
- Preise: Tabellen vollständig über die Inhaltsbreite; verschachtelte Kubio-Hüllen werden mitgezogen.
- Preise: echte sichtbare Abschnittsüberschriften mit sauberem oberen/unteren Abstand.
- Disclaimer: importierte Fett-Zeilen mit `<br>` als saubere Abschnittsüberschriften formatiert.
- Validiert gegen den echten übernommenen Preise-/Disclaimer-Inhalt aus dem Footer-Umzug.
- Artefakt: `HOBBY_DEPOT_HD003_CYBERDUCK_1.50.736_SERVICE_PAGES_LAYOUT_HARDPASS.zip`
- SHA-256: `9f395cc4481e758a675536ab592ac2e686a53d2513ad729f92a22e6c7a678a38`
- QA: PHP 11/11 PASS, ZIP/Fresh-Unpack 936 Dateien bytegleich.
