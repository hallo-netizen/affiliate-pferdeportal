# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-10
STATUS: **1.50.593 + 1.50.594 VERWORFEN / 1.50.595 ROOTFIX LOCAL HARD PASS / WORDPRESS-LIVE OFFEN**

## Aktueller belastbarer Stand

Verbindliches Designkonzept:
`DESIGN_SPEZIFIKATION_1_0_20261010.md`.

Freigegebene visuelle Basis:
der vom Nutzer bevorzugte Hobby-Depot-Startseitenentwurf inklusive Affiliate-Produktbereich, Affiliate-Banner und direkt vermietbarer Werbefläche. Das Grundkonzept wird nicht erneut umgebaut.

## Freigegebene Marke

Logo:
- **Variante 3 / verfeinerte Header-Fassung**;
- offener gemalter Halbkreis/Bogen oberhalb der Wortmarke;
- handschriftliches `dein` optisch mittig;
- `HOBBY DEPOT` einzeilig;
- mehr Luft zwischen Bogen, `dein`, Wortmarke und Claim;
- Schriftfarbe warmes Dunkelgrau statt Schwarz.

Claim:
**Hobbys. Ideen. Möglichkeiten.**

Desktop-Portalzeile:
**Inspiration, Wissen & Empfehlungen rund ums Hobby.**

Mobile:
keine zusätzliche Topbar-Zeile.

## Harte Portalregeln

- Affiliate-/Informationsportal, kein Shop.
- Kein Warenkorb, Checkout, Shop-Merkliste, allgemeiner Shop-Login, Newsletter- oder Community-Bereich im Header.
- Hauptnavigation nur aus realen Portalbereichen: **Hobbywelten, Hobbyfinder, Magazin, Anbieter**.
- CORE-Welten exakt: **Gestalten, Fertigen, Technik, Forschen, Pflanzen, Tiere, Bewegen, Sammeln**.
- Namen und direkte Kinder werden aus WordPress/HD-001 gelesen; keine zweite Taxonomie.
- helle, freundliche Bilder; bei redaktionellen Hauptmotiven Mensch oder mindestens tätige Hände.
- gleiche Ebene = zentraler Bauplan.
- unbelegte Produkt-, Banner- und Mietwerbeplätze vollständig unsichtbar.

## Technischer Umsetzungsstand

Arbeitsbasis:
**Affiliate Portal Template Kit 1.50.592** – aktueller bereitgestellter Pferdeatelier-Stand vom 10.10.2026.

Hobby-Kandidat:
**1.50.594**.

Umgesetzt:
- getrenntes Designprofil `hobby_depot`;
- Pferde-spezifische Init-/Globalhooks werden im Hobby-Profil nicht registriert;
- freigegebenes Variante-3-Logo als Asset;
- Desktop-Topbar / Mobile-Ausblendung;
- Suche;
- dynamische reale Navigation und Mega-Menüs;
- kompakter Startseiten-Hero;
- acht reale Welten;
- Hobbyfinder/Magazin/realer Wissens-/Ratgeberzugang;
- Affiliate-Produkte;
- Affiliate-Banner;
- direkt vermietete Werbefläche;
- leere Monetarisierungsslots ohne Wrapper/Leerraum;
- responsive 4×2 → 2×4 Weltendarstellung.

Keine Kategorie-/SEO-Struktur wird geschrieben oder synchronisiert.

## Korrektur 1.50.594

**1.50.593 ist verworfen.** Die reale WordPress-Ausgabe wich sichtbar vom freigegebenen Startseitenentwurf ab. Ursache: die erste Hobby-Profilumsetzung übernahm nur grobe Strukturmerkmale, nicht die tatsächlichen Proportionen und Dichten des freigegebenen Mockups.

1.50.594 setzt deshalb den freigegebenen Entwurf ohne Konzeptwechsel enger nach:
- Contentbreite 1440 px;
- kompakter Hero;
- 8 Welten in einer Desktop-Zeile;
- 4 × 2 Welten mobil;
- drei kompakte redaktionelle Teaser;
- drei horizontale Affiliate-Produktplätze;
- flacher Affiliate-Banner;
- separate Mietwerbefläche;
- Headerproportionen/Logo/Suche/Navi wie im freigegebenen Entwurf;
- Theme-Container der Startseite neutralisiert, damit Astra das Layout nicht wieder einengt.

Lokale Prüfungen:
- PHP-Lint komplett PASS;
- alte Hobby-Profilklasse entfernt;
- echte 8 Weltnamen PASS;
- Shop-/Community-/Newsletter-Begriffe im Hobby-Renderer 0;
- Leerregel Affiliate PASS;
- ZIP-Integrität PASS;
- lokaler statischer Rendervergleich gegen den freigegebenen Entwurf durchgeführt.

Kandidat:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.594_HOBBY_DEPOT_DESIGN_PARITY_LOCALPASS.zip`

SHA-256:
`f3e6773c0cb2dcbb9a9a4e7ce386524d31c80e88d65101c80f13104c84503c7b`

## Erster offener Blocker

**WordPress-Live-Abnahme des globalen Rahmens und der Startseite.**

Kein LIVE-PASS wird vor dieser Abnahme behauptet.

## EXAKT EINE NEXT ACTION

Den vollständigen **1.50.594**-Kandidaten in der Hobby-Depot-WordPress-Instanz installieren/aktualisieren und **Header + Startseite Desktop/Mobile** gegen den freigegebenen Entwurf prüfen.

Erst nach diesem PASS wird Hub Ebene 1 aus demselben unveränderten Designsystem abgeleitet.


## ROOTCAUSE 1.50.594 – 2026-10-10

Der Live-Screenshot belegt den Fehler eindeutig:
- WordPress/Twenty Twenty-Five rendert weiterhin **Blog**;
- der Beitrag **TEST** bleibt der eigentliche Loop-Inhalt;
- die Hobby-Depot-Startseite wird nur innerhalb dieses Beitragsinhalts ausgegeben;
- der Twenty-Twenty-Five-Footer bleibt aktiv.

Ursache im Quellcode 1.50.594:
Die Startseite wurde über `the_content` in den bestehenden WordPress-Front-/Blogloop eingeschoben. CSS konnte deshalb die Theme-/Loop-Architektur nicht zuverlässig ersetzen.

**1.50.594 ist verworfen.**

## 1.50.595 – ROOTFIX

Kein Redesign. Ausschließlich Ursachenbehebung:
- kein Homepage-`the_content`-Einschub mehr;
- Root-/Frontpage wird über `template_include` als vollständiges Plugin-Fronttemplate übernommen;
- eigener Hobby-Header + Startseitenrenderer + eigener Hobby-Footer;
- Twenty-Twenty-Five Header/Footer-Templateparts im Hobby-Profil werden unterdrückt;
- Nicht-Frontseiten bleiben vom Fronttemplate unberührt.

Lokaler Nachweis:
- PHP-Lint 9/9 PASS;
- Fronttemplate POSITIV PASS;
- Nicht-Frontseite NEGATIV PASS;
- kein alter `front_page_content`-Hook PASS;
- kein Blog-/TEST-Loop im Fronttemplate PASS;
- Blocktheme Header/Footer-Unterdrückung PASS;
- vollständiger Render Header + Main + Footer PASS;
- frischer ZIP-Unpack + CRC PASS.

Kandidat:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.595_HOBBY_DEPOT_FRONT_TEMPLATE_ROOTFIX_LOCALPASS.zip`

SHA-256:
`721eacf41b85a7eaa96114443564ce3bd264d580f148ae56674dbecbe536ef92`

NEXT ACTION:
Nur 1.50.595 installieren und den Root-Aufruf `https://hobby-depot.de/` prüfen. Erwartung: kein „Blog“, kein Theme-Postwrapper, kein Twenty-Twenty-Five-Footer; Hobby-Header und Startseite bilden den Seitenrahmen.


## DETAILFIX 1.50.596 – 2026-10-10

**1.50.595 bleibt Rootfix-Basis; 1.50.596 ändert ausschließlich die vom Nutzer benannten Detailpunkte. Kein Konzeptumbau.**

Umgesetzt:
- Hauptnavigation = reale erste CORE-Ebene exakt: **Gestalten, Fertigen, Technik, Forschen, Pflanzen, Tiere, Bewegen, Sammeln**.
- **Hobbyfinder, Magazin, Anbieter** aus Hauptnavigation entfernt und im Footer geführt.
- Startseiten-Mittelteil wieder vollständig strukturell gebunden: 3 redaktionelle Teaser + Affiliate-Produkte + Affiliate-Banner + Beliebte Themen + Mietwerbefläche.
- Monetarisierungsregel unverändert: unbelegt = vollständig unsichtbar; belegt = sichtbar.
- falsche dekorative Pinselstriche an Hero/Abschnittsüberschriften entfernt.
- Variante-3-Logo unverändert in Form; Petrol des Halbkreises aufgehellt/freundlicher.
- Mobile bleibt derselbe zentrale Renderer; 8 Welten = 4×2.

Lokaler Hardtest:
- PHP-Lint 9/9 PASS.
- synthetischer WordPress-Render POSITIV/NEGATIV PASS.
- Header 8/8 reale Welten PASS.
- Footer Hobbyfinder/Magazin/Anbieter PASS.
- Header ohne Hobbyfinder/Magazin/Anbieter/Community/Newsletter/Warenkorb PASS.
- leere Affiliate-Slots unsichtbar PASS.
- belegte Affiliate-Slots 3 Produkte + Banner + Mietfläche PASS.
- Brush-Deko entfernt/deaktiviert PASS.
- Fronttemplate ohne Theme-get_header/get_footer PASS.
- frischer ZIP-Unpack + CRC + PHP-Lint PASS.

Kandidat:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.596_HOBBY_DEPOT_DETAILFIX_LOCALPASS.zip`

SHA-256:
`eb4bd734d358cf5240ec92dfd7cffd43027b7c64c275b383357524221b510d94`

EXAKT EINE NEXT ACTION:
1.50.596 installieren und Header + Startseite live prüfen. Keine weitere Designänderung vor diesem Readback.


## HOMEPAGE-REFINEMENT 1.50.597 – 2026-10-10

Kein Konzeptwechsel. Umsetzung der zuletzt freigegebenen Detailrichtung:

- **8 CORE-Welten bleiben vorerst vollständig sichtbar**, jetzt als **4 × 2** auf Desktop statt 8 Mini-Karten in einer Reihe.
- Startseiten-Weltkarten deutlich größer; Bilder größer.
- Untertitel in den Weltkarten entfernt; **Welttitel deutlich stärker und lesbarer**.
- Für jede CORE-Welt existiert jetzt eine **stabile eigene Icon-Identität**.
- Dieselben Icons erscheinen in Hauptnavigation und Weltkarten und sind technisch als wiederverwendbare API angelegt, damit sie auf Hub-/Kategorie-/Beitragsebene denselben roten Faden bilden können.
- Box-Radien reduziert; Buttons dürfen weiterhin pillenförmig bleiben.
- Mobile Weltkarten: 2 Spalten, ohne Untertitel.
- Affiliate-/Werbelogik unverändert: leer = vollständig unsichtbar; belegt = sichtbar.

CORE-Welten unverändert:
**Gestalten, Fertigen, Technik, Forschen, Pflanzen, Tiere, Bewegen, Sammeln**.

Kandidat:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.597_HOBBY_DEPOT_ICONS_GRID_LOCALPASS.zip`

SHA-256:
`8f4b1e6da2a5569529584cc1af70bdd92cececbc3f3091519a4ec9f440994a3d`

Lokaler Hardtest:
- PHP 9/9 PASS;
- 8/8 Weltkarten PASS;
- 8/8 Header-Icons PASS;
- 8/8 Weltkarten-Icons PASS;
- Untertitel der Weltkarten entfernt PASS;
- Desktop 4×2 PASS;
- Mobile 2-spaltig PASS;
- reduzierte Box-Radien PASS;
- Affiliate leer NEGATIV PASS;
- Affiliate belegt POSITIV PASS;
- keine Shop-/Community-/Newsletter-UI PASS;
- ZIP-CRC PASS.

NEXT ACTION:
1.50.597 installieren und Startseite Desktop/Mobile live prüfen. Entscheidung, ob später nur 4 statt 8 Weltkarten auf der Startseite gezeigt werden, bleibt bewusst offen und erfordert keinen Systemumbau.
