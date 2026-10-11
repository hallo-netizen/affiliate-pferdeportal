# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-11
STATUS: **1.50.613 LOCAL HARD PASS / STARTSEITEN-FEINSCHLIFF + ERSTE HUBEBENE IMPLEMENTIERT / WORDPRESS-LIVE OFFEN**

## Autoritative Bindungen

Zielvertrag:
`ZIELVERTRAG_HOBBY_DEPOT_DESIGN_20261011.md`

Fehlerquelle:
`FEHLERQUELLEN.md`

Technische Plugin-Current:
`../PLUGINS/PLUGIN_AKTEN/HD-003-DESIGN-TEMPLATE-KIT/CURRENT.md`

Theme-Unterbau:
**ListingHive**.

## Startseite 1.50.613

Unverändert:
- Logo;
- Topbar-Inhalt;
- 8 Hauptwelten;
- Hero-Bildschriftzug.

Neu/finalisiert:
- Desktopnavigation weitere **14 px nach unten** auf die optische unterste Claim-/Textachse;
- Hobbyfinder / Magazin / Wissen & Glossar verwenden einheitlich denselben Creme-Hintergrund `#f5f1e9`;
- öffentlicher direkt verkaufbarer Werbeplatz ist fest sichtbar und trägt **„Hier könnte Ihre Werbung stehen.“**;
- maximal ein Direktwerbeplatz;
- Direktwerbeplatz steht unmittelbar nach der Dreiergruppe Hobbyfinder/Magazin/Wissen, damit er nicht faktisch „verschwindet“;
- Affiliate-Banner/Produkte öffentlich leer unsichtbar, eingeloggt leer sichtbar.

## Erste CORE-/Hubebene

Für:
**Gestalten, Fertigen, Technik, Forschen, Pflanzen, Tiere, Bewegen, Sammeln**.

Implementiert:
- eigenes Hobby-Depot-Contenttemplate;
- Breadcrumb;
- oberer Text/Intro analog zum Portalprinzip des Pferdeatelier-Templates;
- Hub-Hero;
- Hub-Hero verwendet **exakt dasselbe kontrollierte 1400×620-Weltasset wie die Startseitenkarte**;
- vollständige direkte Kindebene als Kacheln;
- Affiliate-Bannerplatz;
- Beitragsvorschau;
- drei Affiliate-Produktplätze;
- genau ein direkt verkaufbarer Werbeplatz.

## Weitere fachliche Ebenen

Das 1.50.613-Contenttemplate ist bereits für `hub2`, `category`, `leaf` und WordPress-Kategoriearchive wiederverwendbar:

- Breadcrumb;
- Titel/Intro;
- vorhandene nächste Ebene;
- Banner;
- Beitragsvorschau;
- Produkte;
- Direktwerbeplatz.

Für normale Seiten/Beiträge außerhalb des eigenen CORE-Templates wird der universelle obere Breadcrumb-/Introbereich eingebunden; Startseite bleibt breadcrumbfrei.

## Breadcrumb-Regel

Startseite:
**kein Breadcrumb**.

Alle übrigen unterstützten Seiten/Kategorien:
- gemeinsame Position/Achse;
- Startseite → reale Parentkette → aktuelle Seite;
- aktuelle Seite nicht verlinkt.

## Bilder

Weiterhin verbindlich:
- 8 kontrollierte Weltassets;
- je 1400×620;
- Startkarte und Welt-Hub teilen exakt dieselbe Bildquelle;
- Männer/Frauen/aktive Hände gemischt;
- kein Weltmotiv ohne mindestens Person oder aktive Hände;
- Tiere ohne Rahmen, kein allgemeines Haustiermotiv.

## Kandidat

`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.613_HOBBY_DEPOT_HUB1_BREADCRUMB_MONETIZATION_LOCALPASS.zip`

SHA-256:
`56aa6f55542570d2383bd6fff92aaddcf155cf103cf14faccf80994636250d34`

## Lokaler Hardtest

PASS:
- ZIP-Integrität;
- PHP **10/10**;
- Homepage öffentlicher Direktwerbeplatz vorhanden;
- Homepage Direktwerbeplatz exakt 1;
- öffentlich leere Affiliateplätze unsichtbar;
- eingeloggt leere Affiliateplätze sichtbar;
- alle drei Editorialkarten gleicher Creme-Hintergrund;
- Navigation reale CSS-Absenkung 14 px;
- Hub1-Breadcrumb;
- Hub1-Hero nutzt kontrolliertes Startseiten-Weltasset;
- direkte nächste Ebene sichtbar;
- Hub1 Banner-Arbeitsplatz;
- Hub1 Beitragsvorschau;
- Hub1 Produktplätze;
- Hub1 Direktwerbeplatz exakt 1;
- Kategorie-Breadcrumb;
- Kategorie Banner/Produkte/Beiträge;
- Kategorie Direktwerbeplatz exakt 1.

## Erster offener Blocker

**WordPress-Live-Abnahme von 1.50.613.**

Prüfen:
1. Navigation jetzt tatsächlich bündig mit der untersten Logo-/Claimzeile;
2. Dreiergruppe Hobbyfinder/Magazin/Wissen einheitlich creme;
3. sichtbarer Startseiten-Werbeplatz;
4. eine Weltseite, bevorzugt `Gestalten`: Breadcrumb, Hero, direkte Kindebene;
5. Hub-Banner/Produkte eingeloggt und öffentlich;
6. Beitragsvorschau;
7. genau ein Direktwerbeplatz;
8. Desktop/Tablet/Mobile.

## EXAKT EINE NEXT ACTION

**1.50.613 installieren und Startseite + eine erste Welt-Hubseite live prüfen.**

Bei Live-PASS wird derselbe bereits implementierte Contenttemplate-Pfad auf die restlichen Ebenen weiter abgenommen, nicht neu erfunden.
