# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-11
STATUS: **1.50.615 LOCAL HARD PASS / HUBFOTOS + RESPONSIVE NAVIGATION + BESTEHENDE HUBLOGIK IMPLEMENTIERT / WORDPRESS-LIVE OFFEN**

## Autoritative Bindungen

Zielvertrag:
`ZIELVERTRAG_HOBBY_DEPOT_DESIGN_20261011.md`

Fehlerquelle:
`FEHLERQUELLEN.md`

Technische Plugin-Current:
`../PLUGINS/PLUGIN_AKTEN/HD-003-DESIGN-TEMPLATE-KIT/CURRENT.md`

Theme-Unterbau:
**ListingHive**.

## 1.50.615 – sichtbarer Designstand

### Header / Navigation
- Logo unverändert;
- Vollnavigation nur noch oberhalb 1320 px;
- 761–1320 px: rechtzeitiger Hamburger-/Dropdownmodus statt abgeschnittener 8-Welten-Zeile;
- Dropdown 4-spaltig, unter 980 px 2-spaltig;
- Mobile unter 761 px unverändert kompakt;
- kein horizontaler Navigationsbeschnitt bei mittleren Breiten;
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

### Fotos auf den oberen Hubebenen

- `hub1` und `hub2` erhalten kompakte Bildkanten in den Unterkategorie-Karten.
- echtes Child-Featured-Image gewinnt;
- fehlt es, nutzt die Karte einen unterschiedlichen Crop des kontrollierten Weltmotivs;
- dieselbe Weltdatei wird dabei browserseitig gecacht, also keine unnötigen Zusatzdownloads;
- tiefere `category`-/Leafebenen bleiben ohne Bildzwang.

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

`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.615_HOBBY_DEPOT_PHOTO_HUB_RESPONSIVE_NAV_LOCALPASS.zip`

SHA-256:
`17d03f5704d8f140a86f4bbbdc4109cf564522a663660d0bd333be456dc3fda6`

Library:
`/hobby rausch/AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.615_HOBBY_DEPOT_PHOTO_HUB_RESPONSIVE_NAV_LOCALPASS.zip`

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

**WordPress-Live-Abnahme von 1.50.615.**

Prüfen:
1. Navigation bei ca. 900–1250 px schaltet vollständig ins Menü und wird nicht rechts abgeschnitten;
2. Gestalten-Unterkategorien zeigen kompakte Fotos;
3. eigenes Child-Bild gewinnt vor Welt-Crop;
4. tiefe Kategorieebenen bleiben ruhiger ohne Bildzwang;
5. Topbar dunkel und ruhig;
6. Navigation auf großer Desktopbreite auf unterster Claim-/Logoachse;
7. Gestalten: Textaufteilung Lead / Mehr erfahren / Was du hier findest;
8. Gestalten mit 7 Unterkategorien: letzte Karte füllt sauber die letzte Reihe;
9. Direktwerbemodul direkt nach Unterkategorien sichtbar;
10. Affiliate-Banner und Produkte optisch integriert;
11. Startseiten-Direktwerbung sichtbar;
12. Tablet/Mobile.

## EXAKT EINE NEXT ACTION

**1.50.615 installieren und Startseite + Gestalten bei Desktop, mittlerer Breite und Mobile live prüfen.**

Erst nach diesem Live-Readback werden Text-/Raster-/Monetarisierungsregeln als endgültig für die tieferen Ebenen abgenommen.
