# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-11
STATUS: **LISTINGHIVE AKTIV / STARTSEITE 1.50.601 LOCAL HARD PASS / WORDPRESS-LIVE OFFEN**

## Aktueller belastbarer Stand

Theme-Basis:
**ListingHive** für die gesamte WordPress-Seite.

Visuelle Autorität:
Hobby-Depot-Designplugin.

Kein Shop:
kein Warenkorb, Checkout, Shop-Merkliste, allgemeiner Shop-Login, Newsletter oder Community im globalen Header.

## Header

Desktop-Hauptnavigation = reale erste CORE-Ebene:
**Gestalten, Fertigen, Technik, Forschen, Pflanzen, Tiere, Bewegen, Sammeln**.

Hobbyfinder, Magazin und Anbieter stehen im Footer.

Aktueller Headervertrag:
- bewusst **hell**, nicht dunkel;
- statt Reinweiß ein warmes, sehr helles Off-White;
- feine Unterkante + sehr leichter Schatten zur Trennung vom Content;
- Suche bleibt weiß;
- Topbar-Text mittig, stärker, 13 px;
- Topbar ohne Zusatzlinks;
- Hauptnavigation Hover = Petrol + feine Unterstreichung ohne Layoutsprung.

## Mega-Menü

**JA – pro CORE-Welt**, niemals ein einziges riesiges Gesamtmenü.

- nur direkte Kinder der jeweiligen Welt;
- 5–6 Kinder: eine Spalte;
- 7+ Kinder: zwei Spalten;
- Abschlusslink „Alle <Welt>-Themen →“;
- Desktop Hoverweg Trigger → Unterpunkt ohne vertikale Lücke;
- Tablet/Mobile Accordion/Click;
- Unterkategorien ab 1.50.601: **14 px / ca. 680 Gewicht**, mehr vertikale Luft;
- Weltüberschrift 16 px / stärker.

## Startseite – verbindliche Reihenfolge

1. Header + Suche + 8 CORE-Welten
2. Hero
3. 8 Weltkarten
4. Hobbyfinder / Magazin / Wissen & Glossar
5. Affiliate-Produkte – nur real belegt
6. Affiliate-Banner – nur real belegt
7. Beliebte Themen aus realen Magazin-SEITEN
8. Mietwerbung – nur real belegt
9. Footer

Keine Fake-Füller für unbelegte Affiliateplätze.

## Bilder

Harte Regel:
- auf derselben Startseite **kein Bild doppelt**;
- Weltbilder müssen zum realen Themenumfang passen;
- „Tiere“ darf nicht als allgemeine Hunde-/Haustierwelt dargestellt werden, da die echte Struktur Aquaristik, Terraristik, Insekten, Wirbellose, Imkerei, Zucht/Futtertiere und Gehegegestaltung umfasst;
- das Tiere-Icon ist deshalb kein Pfoten-/Hundesymbol mehr, sondern Aquarium/Terrarium-orientiert.

1.50.601 benutzt für die Startseiten-Welten kontrollierte, unterschiedliche lokale Assets statt beliebiger WordPress-Featured-Images, damit weder Duplikate noch kleine fremde Thumbnails in das Raster rutschen.

WICHTIG:
Die bisherigen Fotoquellen stammen teilweise aus früheren Visualisierungsassets und besitzen trotz 1400×620 nicht überall echte native Detailauflösung. 1.50.601 schärft/optimiert diese Quellen, behauptet aber **keine künstlich erfundene echte Fotoauflösung**. Falls der Live-Readback noch sichtbar weich ist, werden vor Hub-1 die betroffenen Weltbilder als echte hochauflösende Originalmotive ersetzt.

Editorial-Karten verwenden keine wiederholten Weltfotos mehr, sondern eigene scharfe Vektor-Illustrationen/Icons.

## Startseiten-Vollständigkeit 1.50.601

Behoben:
- dritte Karte **Wissen & Glossar** kommt aus der realen Seite `/magazin/wissen-glossar/`;
- „Beliebte Themen“ liest reale Magazin-SEITEN statt WordPress-Kategorien;
- kein TEST-Post-Fallback mehr;
- reale Themen:
  - Hobby-Ideen & Inspiration
  - Ungewöhnliche & skurrile Hobbys
  - Wissen & Glossar
  - Zeit, Budget & Platz
  - Vergleiche & Alternativen

## Kandidat

`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.601_HOBBY_DEPOT_HOMEPAGE_COMPLETION_VISUAL_POLISH_LOCALPASS.zip`

SHA-256:
`6b9fff2fa237d09d7cef2f31a2db7a50619d97cc6314a665265dbb08832dd952`

## Lokaler Hardtest

PASS:
- PHP 9/9;
- leerer Affiliatezustand NEGATIV;
- belegter Affiliatezustand POSITIV;
- 8/8 reale Welten;
- 3/3 redaktionelle Mittelkarten;
- 5/5 reale Magazin-Themenseiten;
- kein TEST-Fallback;
- kein Community/Newsletter/Shop-Noise;
- ListingHive-Shell-Unterdrückung;
- Hero-CTAs 16 Breiten 320–1600 px;
- kein horizontaler Overflow;
- Mega-Menü Hover bis Unterpunkt;
- vertikale Hover-Lücke 0 px;
- Untermenü-Typografie 14 px/stärker;
- Topbar mittig/stärker;
- Header warm-hell abgesetzt;
- 8 Weltbilddateien unterschiedlich und 1400×620;
- ZIP-CRC;
- frischer ZIP-Unpack + PHP-Lint.

## Erster offener Blocker

**WordPress-Live-Abnahme von 1.50.601.**

Besonders hart prüfen:
1. tatsächliche Bildschärfe auf realem Display;
2. Headerabsetzung;
3. Topbar;
4. Mega-Menü-Unterkategorien;
5. vollständiger Mittel-/Magazinbereich.

## EXAKT EINE NEXT ACTION

1.50.601 installieren und die vollständige Startseite Desktop/Tablet/Mobile live prüfen.

Erst nach Startseiten-LIVE-PASS beginnt Hub Ebene 1.
