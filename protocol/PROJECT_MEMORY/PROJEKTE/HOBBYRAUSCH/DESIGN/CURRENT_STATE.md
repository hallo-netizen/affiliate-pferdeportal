# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-11
STATUS: **LISTINGHIVE AKTIV / STARTSEITE 1.50.600 LOCAL HARD PASS / WORDPRESS-LIVE OFFEN**

## Aktueller belastbarer Stand

Verbindliches Designkonzept:
`DESIGN_SPEZIFIKATION_1_0_20261010.md`.

Theme-Basis für die gesamte WordPress-Seite:
**ListingHive**.

Das Hobby-Depot-Designplugin bleibt für Markenrahmen, Header, Footer, Startseite und die nachfolgenden Hub-/Contenttemplates visuell autoritativ.

## Harte Bindungen

- Affiliate-/Informationsportal, **kein Shop**.
- Kein Warenkorb, Checkout, Shop-Merkliste, allgemeiner Shop-Login, Newsletter oder Community im globalen Header.
- Hauptnavigation = reale erste CORE-Ebene:
  **Gestalten, Fertigen, Technik, Forschen, Pflanzen, Tiere, Bewegen, Sammeln**.
- **Hobbyfinder, Magazin, Anbieter** gehören in den Footer.
- Kategorienamen/Unterpunkte werden aus WordPress/HD-001 gelesen; keine zweite Taxonomie.
- Icons = einheitliches Petrol und pro Welt stabil wiederverwendbar bis Hub/Kategorie/Beitrag.
- Affiliate-Produkte, Affiliate-Banner und Mietwerbung bleiben getrennte Slottypen.
- Unbelegt = vollständig unsichtbar, ohne Wrapper/Leerraum.
- Keine erneute Änderung des freigegebenen Startseiten-Grundkonzepts.

## Logo

Freigegebener Arbeitsstand:
- Variante 3;
- offener gemalter Halbkreis;
- `dein` höher in den Halbkreis gezogen;
- `HOBBY DEPOT` Anthrazit/Dunkelgrau;
- Claim in eigenständiger leichterer Typowirkung und Petrol:
  **Hobbys. Ideen. Möglichkeiten.**

## Mega-Menü – Entscheidung

**JA**, aber ausschließlich als ruhiges **Mega-Menü pro CORE-Welt**:
- Desktop: nur direkte Kinder der jeweiligen Welt;
- bei vielen Kindern 2 Spalten;
- kein riesiges Gesamtmenü über alle 8 Welten;
- Abschlusslink `Alle <Welt>-Themen →`;
- keine vertikale Hover-Lücke;
- Mausweg Trigger → Unterpunkt muss stabil bleiben;
- Navigationstext erhält Hover: Petrol + 2-px-Unterstreichung ohne Layoutbewegung;
- Tablet/Mobile: kontrolliertes Menü/Accordion statt Hover.

## Startseite – vollständig vor Hub-Arbeit

1. Header + Suche + 8 CORE-Welten
2. Hero mit zwei responsiven CTAs
3. 8 Weltkarten (4×2 Desktop / 2 Spalten Mobile)
4. Hobbyfinder / Magazin / Wissen & Glossar
5. Affiliate-Produkte, nur bei realer Belegung
6. Affiliate-Banner, nur bei realer Belegung
7. Beliebte Themen aus realen Magazin-Kategorien
8. Mietwerbefläche, nur bei realer Belegung
9. Footer mit Hobbyfinder / Magazin / Anbieter

## Bildschärfe – Rootcause und Vertrag

Die verbleibende Unschärfe kam **nicht mehr primär von CSS oder WordPress-`srcset`**, sondern von den bisherigen lokalen Fallback-Dateien selbst: sie waren aus kleinen Mockup-Ausschnitten hochskaliert.

1.50.600:
- WordPress Featured Images werden aus dem **Full-Original** mit nativem `srcset/sizes` ausgegeben;
- kein `medium_large` im Hobby-Profil;
- lokale Welt-Fallbacks wurden neu aufgebaut und liegen mit **1400×620** vor;
- vorhandene bessere Quellen wurden ersetzt/geschärft;
- die **kanonischen endgültigen Weltbilder** werden die echten hochauflösenden Hub-1-Featured-Images. Sobald diese gesetzt sind, verwendet die Startseite sie automatisch.

Damit wird keine CSS-Schärfung als Ersatz für fehlende Quelldetails behauptet.

## Kandidat 1.50.600

`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.600_HOBBY_DEPOT_HOMEPAGE_COMPLETE_MEGA_HOVER_IMAGESOURCE_LOCALPASS.zip`

SHA-256:
`c828edff9ef61232f2e6bf472de7cbf81b373c8d6bfc82279bf4bdefa70defdc`

## Lokaler Hardtest

**PASS**
- PHP-Lint komplett 9/9;
- Strukturtest PASS;
- leerer Monetarisierungszustand NEGATIV PASS;
- belegter Monetarisierungszustand POSITIV PASS;
- vollständige Startseitenreihenfolge PASS;
- 8 reale Welten PASS;
- reale Magazin-Themen PASS;
- Shop-/Community-/Newsletter-Noise NEGATIV PASS;
- ListingHive-Shell-Unterdrückung PASS;
- Hero-CTAs bei **16 Breiten 320–1600 px** sichtbar und innerhalb des Hero PASS;
- kein horizontaler Overflow bei diesen 16 Breiten PASS;
- Mega-Menü Trigger → Unterpunkt Hover PASS;
- gemessene vertikale Hover-Lücke = **0 px**;
- Schrift-Hover Petrol + Unterstreichung PASS;
- Welt-Fallbackdateien mindestens 1400×620 PASS;
- ZIP-CRC PASS;
- frischer ZIP-Unpack + PHP-Lint PASS.

## Erster offener Blocker

**WordPress-Live-Abnahme von 1.50.600 auf ListingHive.**

Kein LIVE-PASS wird vor dem realen Readback behauptet.

## EXAKT EINE NEXT ACTION

1.50.600 installieren und die **komplette Startseite Desktop/Tablet/Mobile inklusive Mega-Menü** live prüfen.

Nach LIVE-PASS beginnt **Hub Ebene 1**. Kein weiterer Startseiten-Konzeptumbau.
