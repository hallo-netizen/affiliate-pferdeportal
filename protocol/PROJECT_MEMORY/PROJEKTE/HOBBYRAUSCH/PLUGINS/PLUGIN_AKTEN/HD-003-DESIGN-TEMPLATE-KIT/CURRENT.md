# HD-003 – HOBBY DEPOT DESIGN / TEMPLATE KIT – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-24
STATUS: **1.50.733 / HAUPTSUCHE VIEWPORT-CLAMP / LOCAL HARD PASS / LIVE OFFEN**

Plugin-ID:
`HD-003-DESIGN-TEMPLATE-KIT`

Aktuelles Artefakt:
`HOBBY_DEPOT_HD003_CYBERDUCK_1.50.733_MAINSEARCH_VIEWPORT_FIX_HARDPASS.zip`

SHA-256:
`d0268782c88e17c5665ee71ae38d564c6600c01e7a6da38e8ce48151f612a9b2`

Pluginroot im Bundle:
`affiliate-portal-template-kit/`

## Aktueller Vertrag
- zentrale Hobby-Depot-Body-Achse max. 1200 px;
- Header und Footer behalten unverändert ihre bisherige 1440-px-Achse;
- Hobbymagazin „Wissen & Glossar“ verlinkt kanonisch auf `/magazin/wissen-glossar/`;
- Footer-Glossarlink verwendet ebenfalls die kanonische Route;
- keine sonstige Header-/Footer-Designänderung.

## QA
- Hobbymagazin-Toolkarte aus echtem Plugin gerendert: kanonischer Glossarlink PASS, alte `/glossar/`-Route dort nicht mehr vorhanden;
- 1200-px-Body-Regeln aus 1.50.730 weiterhin vorhanden;
- Header-/Footer-1440-Override weiterhin vorhanden;
- Gesamtbundle Fresh-Unpack und Source↔ZIP bytegleich;
- PHP im Gesamtbundle 22/22 PASS.

## EXAKT EINE NEXT ACTION
**Bundle serverseitig in die drei bestehenden kanonischen Pluginordner überschreiben; keine zusätzlichen Pluginordner anlegen.**


## 1.50.732 – Hobbyfinder + globale Hauptsuche
- Hobbyfinder: „Passende Themen“ war kein Finder-Ergebnis, sondern der allgemeine Magazin-Unterthemenblock.
- Auswahlquelle dieses Blocks: zuerst dem Hobbyfinder im zentralen Registry-Baum untergeordnete `journal_cat`-Knoten; Fallback `alleine`, `gruppe`, `zu-zweit`.
- Hobbyfinder-Reihenfolge jetzt: Hero/Intro → vorhandene `journal_banner`-Fläche → eigentlicher Finder → „Passende Themen“ als „Weiter entdecken“ unten.
- „Zur Startseite“ und „Neu starten“ im Finder unverändert.
- globale Header-Suche erhält eigenen AJAX-Transport ab 2 Zeichen, 180-ms-Debounce und AbortController.
- vier fachlich getrennte Ergebniswelten: HOBBYS | MAGAZIN | GLOSSAR | ANZEIGEN.
- HOBBYS: ausschließlich 862er Hobbyregister (inkl. Alias-Matching).
- MAGAZIN: ausschließlich veröffentlichte Posts mit `journal_cat`.
- GLOSSAR: ausschließlich veröffentlichte `hdg_term`.
- ANZEIGEN: ausschließlich `hp_listing_category` + veröffentlichte `hp_listing`.
- „Alle Suchergebnisse anzeigen“ führt auf eigene gruppierte Ergebnisseite mit denselben vier Bereichen.
- keine beliebigen WordPress-Seiten in der Vorschau.

## QA
- serverseitiger Positiv-/Negativtest aller vier Suchwelten PASS;
- normale beliebige WP-Seite als Negativfall ausgeschlossen PASS;
- Ajax-Client im Chromium mit simuliertem Fetch PASS;
- Responsive Ergebnislayer 1600 / 1024 / 760 / 390 px PASS;
- Hobbyfinder-Quellreihenfolge Banner → Finder → Unterthemen PASS;
- Fresh-Unpack Source↔ZIP bytegleich: 936 Dateien;
- PHP 11/11 PASS; ZIP CRC PASS.


## 1.50.733 – Hauptsuche bleibt vollständig im Browserfenster
- Live-Screenshot zeigte horizontales Abschneiden des vierteiligen Ajax-Ergebnislayers.
- Ursache: der breite Ergebnislayer war fest an der linken Kante des Suchformulars verankert.
- Korrektur: Ergebnislayer wird vor Anzeige und nach jeder Ajax-Antwort anhand des aktuellen Viewports neu positioniert und mit 16 px Sicherheitsrand eingeklemmt.
- Breite bleibt bis 1180 px erhalten; unter 760 px weiterhin 100 % des Suchformulars/einspaltig.
- Vier Suchwelten Hobbys / Magazin / Glossar / Anzeigen und deren Datenquellen unverändert.

## QA
- exakte Screenshot-Geometrie ca. 903 px Viewport / Suchformular links 267 px simuliert: Ergebnis 16–887 px, kein horizontaler Überlauf.
- Geometriesimulation zusätzlich 1648 / 1366 / 1024 / 761 px PASS.
- Positionierung läuft vor Loading-State, nach Ajax-Ergebnis und bei Resize.
- Fresh-Unpack: 936 Dateien Source↔ZIP bytegleich.
- PHP 11/11 PASS; ZIP CRC PASS.
