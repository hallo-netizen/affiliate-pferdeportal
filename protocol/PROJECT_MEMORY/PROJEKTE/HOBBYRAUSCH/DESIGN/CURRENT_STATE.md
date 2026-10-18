# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-18
STATUS: **1.50.685 HUB2-STAND NUTZERSEITIG AUF DEN ERSTEN BLICK OK / 1.50.686 KETTENHEMDFLECHTEN-PILOT FÜR NÄCHSTE EBENE GEBAUT / LOKAL POSITIV+NEGATIV+RESPONSIVE PASS / WORDPRESS-READBACK OFFEN**

Zielvertrag: **ZV-HOBBYRAUSCH-DESIGN-001 Fassung 5.0 / 2026-10-18**

## PILOT NÄCHSTE EBENE – KETTENHEMDFLECHTEN

Nutzerentscheidung für die Detailprüfung:
- auf dieser tieferen Ebene **kein Hero-Bild**;
- oben kompakter, mittig geführter Textkopf mit Icon und H1;
- hochwertiger Text nach den bestehenden 150–200-Wörter-Regeln;
- nur ein kurzer Teil sichtbar, Rest über kleinen Chevron aufklappbar;
- darunter Unterkategorien kompakter;
- Desktop testweise **4er-Raster**;
- Affiliate-Produkte und Banner nicht mehr als großer Block erst am Seitenende, sondern früher zwischen den Inhalten;
- Beitragsvorschauen bleiben enthalten.

## KANDIDAT 1.50.686

Artefakt:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.686_KETTENHEMDFLECHTEN_MIXED_LEVEL_PILOT.zip`

SHA-256:
`0fef7c270977c01e986adf82ee00f56b5602f699e12799fb18cfc1c28b919e4d`

Nur die Seite `kettenhemdflechten` ist als Pilot verändert.

### Aufbau

1. Breadcrumb
2. Ketten-/Ring-Icon
3. H1 `Kettenhemdflechten`
4. 162-Wörter-Fachtext:
   - 45 Wörter sichtbar
   - 117 Wörter aufklappbar
   - kein Hero-Bild
5. erste 4 Unterkategorien im 4er-Raster
6. drei vorhandene `category_product_1..3`-Affiliateplätze
7. restliche 4 Unterkategorien im 4er-Raster
8. Banner `product_after_category_tiles`
9. drei Beitragsvorschauen
10. vorhandener Werbe-/Dienstleisterplatz danach

Unterkategorien:
- Einstieg & Grundlagen
- Ausrüstung & Kosten
- Vergleich & Kaufberatung
- Formen & Übergänge
- Grundmuster
- Projekte & Finish
- Ringe & Werkzeuge
- FAQ / Häufige Fragen

Für alle acht sind kurze konkrete Orientierungszeilen gebunden.

## QA

- aus exakter 1.50.685-Basis gebaut;
- PHP **102/102 PASS**;
- ZIP PASS;
- aktive Main-/Klassen-/Templatekette vollständig V150686;
- Front-/Contenttemplate positiv mit V150686 PASS;
- Negativtest mit ausschließlich V150685 scheitert erwartungsgemäß;
- echter Kettenhemd-Renderpfad: PASS;
- kein Hero im Pilot;
- genau 1 H1;
- 8/8 Unterkategorien;
- Reihenfolge `4 Themen → Produkte → 4 Themen → Banner → Beiträge` PASS;
- 3 vorhandene Kategorie-Produktplätze eingebunden;
- Standard-Kategorie-Intro wird im Pilot nicht zusätzlich gerendert;
- Browser 1440 / 1024 / 390: kein horizontaler Overflow;
- Desktop 4 Karten pro Reihe, Tablet 2, Mobil 1;
- Delta zu 1.50.685: **1 bestehende Datei geändert + 3 neue Dateien + 0 entfernt**;
- ZIP-Roundtrip **1142/1142 byte-identisch**.

## EXAKT EINE NEXT ACTION

**1.50.686 installieren und ausschließlich Kettenhemdflechten prüfen: Kopfbereich ohne Hero, Textkompaktheit, 4er-Raster und die neue Mischung aus Kategorien / Produkten / Banner / Beiträgen.**

## NICHT ANFASSEN

- noch keine Übertragung auf die übrigen Seiten dieser Ebene;
- Hub2-Heroes nicht erneut ändern;
- Kategoriebaum nicht ändern;
- keine zusätzlichen Affiliate-Slots erfinden.
