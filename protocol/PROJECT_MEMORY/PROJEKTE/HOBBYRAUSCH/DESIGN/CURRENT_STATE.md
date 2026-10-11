# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-11
STATUS: **LISTINGHIVE AKTIV / STARTSEITE 1.50.611 LOCAL HARD PASS / WORDPRESS-LIVE OFFEN**

## Autoritative Bindungen

Zielvertrag:
`ZIELVERTRAG_HOBBY_DEPOT_DESIGN_20261011.md`

Fehlerquelle:
`FEHLERQUELLEN.md`

Technische Plugin-Current:
`../PLUGINS/PLUGIN_AKTEN/HD-003-DESIGN-TEMPLATE-KIT/CURRENT.md`

Aktiver Theme-Unterbau:
**ListingHive**.

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

Aktueller Headervertrag 1.50.610:
- Logo unverändert: freigegebenes Asset `logo-variant3-v150600.png`;
- Topbar-Inhalt unverändert: **Inspiration, Wissen & Empfehlungen rund ums Hobby.**;
- Topbar mittig;
- Body weiß;
- Header warmes Off-White `#f5f1e9` und dadurch sichtbar vom Body getrennt;
- Suche weiß;
- **keine Anzeige im Header**;
- Hauptnavigation Hover = Petrol + feine Unterstreichung ohne Layoutsprung.

## Mega-Menü

**JA – pro CORE-Welt**, niemals ein einziges riesiges Gesamtmenü.

- nur direkte Kinder der jeweiligen Welt;
- 5–6 Kinder: eine Spalte;
- 7+ Kinder: zwei Spalten;
- Abschlusslink „Alle <Welt>-Themen →“;
- Desktop Hoverweg Trigger → Unterpunkt ohne vertikale Lücke;
- Tablet/Mobile Accordion/Click;
- Unterkategorien 14 px / stärker;
- Weltüberschrift 16 px / stärker.

## Startseite – verbindliche Reihenfolge

1. Header + Suche + 8 CORE-Welten
2. Hero
3. 8 Weltkarten
4. Hobbyfinder / Magazin / Wissen & Glossar
5. Affiliate-Banner
6. Beliebte Themen aus realen Magazin-SEITEN
7. Affiliate-Produkte
8. genau ein direkt verkaufbarer Werbeplatz
9. Footer

Affiliate-Produkte/Banner:
öffentlich leer vollständig unsichtbar; **eingeloggt** leere Arbeitsplätze sichtbar.

Direkt verkaufbarer Werbeplatz:
**maximal einer pro Seite/Kategorie/Beitrag**, öffentlich auch unverkauft sichtbar als „Werbeplatz verfügbar / Hier werben“.

## Hero

Der freigegebene Bildschriftzug
**„Mehr Zeit für das, was dich begeistert.“**
bleibt erhalten.

1.50.610 verwendet dafür zwei kontrollierte Safe-Crops:
- Desktop 1370×620;
- Tablet/Mobile 1240×620.

Unterhalb 1100 px wird der Hero gestapelt, damit Bildschriftzug und CTAs nicht abgeschnitten werden.

## Weltbilder

1.50.610 ersetzt die alten weichen/teilweise mockup-basierten Weltbilder vollständig.

Neu:
- 8/8 unterschiedliche native Ausgangsbilder;
- alle 8 Ausgabemotive exakt **1400×620**;
- gleiche Bildquelle für Startseitenkarte und späteren Welt-/Kategorie-Hero vorgesehen;
- `Gestalten`: Kreativatelier / Malen, Druck, Papier, Textil, Miniaturen;
- `Fertigen`: Werkstatt / Holz, Leder, Buch/Papier, Guss/Formen, Keramik;
- `Technik`: Elektronik, Robotik, RC, 3D-Druck, Retro, Drohne, Audio;
- `Forschen`: Mikroskopie, Naturproben, Messen, Teleskop, Wetter/Umwelt;
- `Pflanzen`: Bonsai, Zimmerpflanzen, Orchideen, Sukkulenten, Hydroponik, Saatgut, essbare Pflanzen;
- `Tiere`: Aquaristik, Terraristik, Insekten/Futtertiere, Imkerei/Bestäuber; **kein Rahmen**, kein Hund/Haustier;
- `Bewegen`: Wandern, Wasser, Klettern/Seil, Bike, Wind/Kite;
- `Sammeln`: Münzen, Papier/Briefmarken, Technik/Medien, Spielzeug, Naturfunde.

Alle acht Hashes unterschiedlich.

## Startseiten-Vollständigkeit 1.50.610

- 8/8 Weltkarten;
- 3/3 redaktionelle Mittelkarten;
- 5 reale Magazin-Themenseiten;
- kein TEST-Fallback;
- breiter Affiliate-Bannerplatz;
- drei Affiliate-Produktplätze;
- Admin-/Login-Vorschau für leere Affiliateplätze;
- genau ein verkaufbarer Werbeplatz;
- Meta-Titel/Description-KISS-Schicht mit optionalem Override;
- kein Shop-/Community-/Newsletter-Noise.

## Kandidat

`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.611_HOBBY_DEPOT_HERO_HEADER_FINAL_LOCALPASS.zip`

SHA-256:
`3f5c74845c1264823a5ca70c09d90fdc0d2ec4815858f6bd9eb84a29f73b2668`

## Lokaler Hardtest

PASS:
- ZIP-Integrität;
- Fresh-Unpack PHP 9/9;
- öffentlich leer: Produkte unsichtbar;
- öffentlich leer: Affiliate-Banner unsichtbar;
- eingeloggt leer: 3 Produktplätze sichtbar;
- eingeloggt leer: 1 Bannerplatz sichtbar;
- belegte Affiliate-Inhalte sichtbar;
- unverkaufter Werbeplatz öffentlich sichtbar;
- Werbeplatz pro Request maximal 1;
- gebuchter Werbeplatz ersetzt Verfügbarkeitsplatz;
- Logo unverändert;
- Topbar-Inhalt unverändert + mittig;
- keine Anzeige im Header;
- Body weiß / Header warm-off-white;
- Hero-Schriftzug Desktop/Mobile erhalten;
- 8/8 Weltkarten;
- 8/8 Weltbilder 1400×620, unterschiedlich;
- Tiere ohne dekorativen Rahmen;
- Reihenfolge Banner → Magazin/Themen → Produkte;
- kein horizontaler Konzeptumbau;
- ListingHive-Shell-Unterdrückung bleibt.

## Feinschliff 1.50.611

- linke Hero-Textfläche weiß;
- Hero 1 px fein gerahmt;
- Desktop 22 px Luft über dem Hero, Mobile 14 px;
- Navigation Desktop 10 px nach unten auf die optische Claim-Achse;
- Headline links: **„Entdecke dein nächstes Hobby.“**;
- Bildspruch bleibt unverändert: **„Mehr Zeit für das, was dich begeistert.“**.

## Erster offener Blocker

**WordPress-Live-Abnahme von 1.50.610.**

Besonders prüfen:
1. Logo lädt real;
2. Hero-Bildschriftzug Desktop/Tablet/Mobile vollständig sichtbar;
3. echte Bildschärfe der 8 neuen Weltmotive;
4. Headerabsetzung weißer Body / warmes Off-White;
5. Adminsicht leere Affiliateplätze;
6. öffentlicher unverkaufter Werbeplatz;
7. breite Bannerfläche;
8. vollständige Startseite Desktop/Tablet/Mobile;
9. Mega-Menü-Unterpunkte.

## EXAKT EINE NEXT ACTION

**1.50.611 in Hobby Depot installieren und die vollständige Startseite Desktop/Tablet/Mobile live prüfen.**

Erst nach Startseiten-LIVE-PASS beginnt Hub Ebene 1.
