# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-11
STATUS: **1.50.614 LOCAL HARD PASS / HUB-TEXTSYSTEM + BALANCIERTES RASTER + NATIVE MONETARISIERUNG IMPLEMENTIERT / WORDPRESS-LIVE OFFEN**

## Autoritative Bindungen

Zielvertrag:
`ZIELVERTRAG_HOBBY_DEPOT_DESIGN_20261011.md`

Fehlerquelle:
`FEHLERQUELLEN.md`

Technische Plugin-Current:
`../PLUGINS/PLUGIN_AKTEN/HD-003-DESIGN-TEMPLATE-KIT/CURRENT.md`

Theme-Unterbau:
**ListingHive**.

## 1.50.614 – sichtbarer Designstand

### Header / Navigation
- Logo unverändert;
- Topbar-Inhalt unverändert;
- Topbar jetzt dunkel im Footer-Farbton `#29383f`;
- Hauptheader bleibt creme;
- Desktopnavigation auf der unteren Logo-/Claimachse weiter abgesenkt;
- Mobile erhält keine künstliche Absenkung.

### Kategorietexte
Übernommenes Pferdeatelier-Prinzip:
- vorhandene manuelle Introtexte zuerst;
- sonst deterministische Erzeugung aus Titel, Ebene, realen Kindern und Themenprofil;
- keine Strukturänderung;
- Texte ab ca. 130 Wörtern:
  - sichtbarer Lead ca. 55 Wörter;
  - `Mehr erfahren`;
  - sichtbarer Abschlussblock `Was du hier findest`;
- vollständiger Text bereits im initialen HTML;
- kurze Texte bleiben offen.

Hub1 verwendet das System ebenfalls.

**Beispieltext Gestalten** ist im Kandidaten fest als Referenz enthalten und nennt die realen direkten Kinder:
Malen & Zeichnen, Druck & Fotografie, Schrift & Lettering, Papierkunst, Textilgestaltung, Oberfläche & Deko, Miniaturen & Szenen.

### Unterkategorien – ungerade Zahlen
Desktop:
- 6-Spalten-Basis;
- normale Karte spannt 2 Spalten = 3 pro Reihe;
- Rest 2 → letzte zwei je 3 Spalten = 50/50;
- Rest 1 → letzte Karte volle Reihe;
- keine leeren Rasterlöcher.

Tablet:
2 Spalten.

Mobile:
1 Spalte.

### Monetarisierung
Reihenfolge auf Hub-/Kategoriepfad:
1. Breadcrumb;
2. Titel/Hero;
3. Kategorietext;
4. nächste Ebene;
5. Direktwerbung;
6. Beitragsvorschau;
7. Affiliate-Banner;
8. Affiliate-Produkte.

Direktwerbung:
- maximal ein Modul;
- bewusst hoch direkt nach den Unterkategorien;
- öffentlich auch unverkauft sichtbar;
- Headline: **„Hier könnte Ihre Werbung stehen.“**;
- CTA: **„Werbemöglichkeiten & Preise“**;
- rechte Bildcollage aus kontrollierten Hobby-Depot-Weltmotiven;
- kein technisch wirkender Leerplatz.

Affiliate:
- Banner nativ integriert, nur kleine Kennzeichnung `Anzeige · Partner`;
- Produktbereich als native Kartenfläche, ebenfalls klar gekennzeichnet;
- öffentlich leer unsichtbar;
- eingeloggt leer sichtbar.

### Welt-/Hubbilder
Unverändert:
- 8 kontrollierte 1400×620-Motive;
- Startkarte und Welt-Hub identische Quelle;
- Personen/Hände gemischt;
- Tiere rahmenlos und fachlich passend.

## Kandidat

`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.614_HOBBY_DEPOT_NATIVE_HUB_MONETIZATION_LOCALPASS.zip`

SHA-256:
`57c371a32a2cc4c84edbfef0819e017ca15fc5007f27a228180e44de8edbda58`

Library:
`/hobby rausch/AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.614_HOBBY_DEPOT_NATIVE_HUB_MONETIZATION_LOCALPASS.zip`

## Lokaler Hardtest

PASS:
- ZIP-Integrität;
- Fresh PHP **10/10**;
- keine 1.50.613-Renderer-/Assetreferenz im Hobby-Depot-Releasepfad;
- 8/8 Weltbilder 1400×620;
- Logo bytes identisch zum freigegebenen Vorgängerstand;
- Pferdeatelier-Introregel mit langem Testtext:
  - Lead vorhanden;
  - `Mehr erfahren` vorhanden;
  - `Was du hier findest` vorhanden;
  - Textanfang und Textende vollständig erhalten;
- Gestalten-Beispieltext im Code vorhanden;
- 6-Spalten-Restklassen für 1/2 vorhanden;
- Direktwerbung vor Beitragsvorschau;
- Affiliate-Banner nach Beitragsvorschau;
- Affiliate-Produkte danach;
- CTA `Werbemöglichkeiten & Preise`;
- dunkle Topbar;
- Desktopnavigation real tiefer;
- Startseite nutzt dasselbe neue Direktwerbemodul.

## Erster offener Blocker

**WordPress-Live-Abnahme von 1.50.614.**

Prüfen:
1. Topbar dunkel und ruhig;
2. Navigation tatsächlich auf unterster Claim-/Logoachse;
3. Gestalten: Textaufteilung Lead / Mehr erfahren / Was du hier findest;
4. Gestalten mit 7 Unterkategorien: letzte Karte füllt sauber die letzte Reihe;
5. Direktwerbemodul direkt nach Unterkategorien sichtbar;
6. Werbe-CTA führt zu Werbemöglichkeiten/Kontakt;
7. Affiliate-Banner und Produkte optisch integriert;
8. Startseiten-Direktwerbung sichtbar;
9. Tablet/Mobile.

## EXAKT EINE NEXT ACTION

**1.50.614 installieren und Startseite + Gestalten live prüfen.**

Erst nach diesem Live-Readback werden Text-/Raster-/Monetarisierungsregeln als endgültig für die tieferen Ebenen abgenommen.
