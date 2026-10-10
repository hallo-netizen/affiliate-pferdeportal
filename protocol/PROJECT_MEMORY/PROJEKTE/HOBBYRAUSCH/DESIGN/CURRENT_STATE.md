# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-10
STATUS: **GLOBALER RAHMEN + STARTSEITE 1.50.593 LOCAL HARD PASS / WORDPRESS-LIVE OFFEN**

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
**1.50.593**.

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

## Lokale Abnahme

**PASS**
- PHP-Lint 8/8;
- Hobby-Profil-Bootstrap PASS;
- Pferde-Profil-Negativtest PASS;
- Render-POS/NEG PASS;
- echte Weltnamen PASS;
- Shop-/Community-/Newsletter-UI negativ PASS;
- leere Affiliateplätze unsichtbar PASS;
- belegte Produktplätze 3/3 PASS;
- belegter Startbanner PASS;
- Paket-Fresh-Unpack + PHP-Lint 8/8 PASS;
- keine entfernte Basisdatei; gegenüber 1.50.592 nur Hauptdatei geändert + Hobby-Profil/Assets ergänzt.

Kandidat:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.593_HOBBY_DEPOT_STAGE1_LOCALPASS.zip`

SHA-256:
`3b5ef12e367ca0616278f92686cc5efccb71d45778056d289410c7d44bac3edd`

## Erster offener Blocker

**WordPress-Live-Abnahme des globalen Rahmens und der Startseite.**

Kein LIVE-PASS wird vor dieser Abnahme behauptet.

## EXAKT EINE NEXT ACTION

Den vollständigen 1.50.593-Kandidaten in der Hobby-Depot-WordPress-Instanz installieren/aktualisieren und **Header + Startseite Desktop/Mobile** live prüfen.

Erst nach diesem PASS wird Hub Ebene 1 aus demselben unveränderten Designsystem abgeleitet.
