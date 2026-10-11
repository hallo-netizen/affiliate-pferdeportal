# ZV-HOBBYRAUSCH-DESIGN-001 – HOBBY DEPOT PORTALDESIGN

STATUS: AKTIV  
FASSUNG: 1.2 / 2026-10-11  
GELTUNGSBEREICH: HOBBYRAUSCH / DESIGN / WORDPRESS-DARSTELLUNG

## Ziel

Hobby Depot wird als hochwertiges, helles Informations- und Inspirationsportal mit integrierter Affiliate-Monetarisierung umgesetzt – ausdrücklich **nicht als Shop**.

Technische Theme-Basis ist **ListingHive**. Das Hobby-Depot-Designplugin ist für Markenrahmen, Header, Footer, Startseite und die Hub-/Contenttemplates visuell autoritativ.

## Marke / Header

- Logo bleibt unverändert die freigegebene Variante 3.
- Topbar-Inhalt bleibt unverändert: **Inspiration, Wissen & Empfehlungen rund ums Hobby.**
- Body weiß.
- Header warmes Creme/Off-White.
- Suche weiß.
- keine Anzeige im Header.
- Desktopnavigation zeigt exakt: Gestalten · Fertigen · Technik · Forschen · Pflanzen · Tiere · Bewegen · Sammeln.
- Navigation sitzt optisch auf der **untersten Claim-/Logo-Textachse**, nicht zu hoch.
- Hobbyfinder, Magazin und Anbieter gehören in den Footer.
- Mega-Menü pro CORE-Welt, nur direkte Kinder, ohne Hover-Lücke.

## Startseite

- Hero-Headline: **„Entdecke dein nächstes Hobby.“**
- Bildschriftzug bleibt: **„Mehr Zeit für das, was dich begeistert.“**
- Hero links weiß, feiner 1-px-Rahmen, sichtbarer Abstand nach oben.
- alle 8 Hauptwelten zusätzlich zur Navigation als Weltkarten.
- Desktop 4×2; Mobile 2×4.
- Hobbyfinder / Magazin / Wissen & Glossar bilden eine gemeinsame Dreiergruppe und benutzen **denselben Creme-Hintergrund**; keine unterschiedliche Schattierungsfarbe.
- Affiliate-Banner nur real öffentlich sichtbar; leer nur eingeloggt als Arbeitsplatz.
- Affiliate-Produkte nur real öffentlich sichtbar; leer nur eingeloggt als Arbeitsplätze.
- genau **ein** direkt verkaufbarer Werbeplatz; öffentlich auch unverkauft sichtbar mit **„Hier könnte Ihre Werbung stehen.“ / „Werbeplatz verfügbar“**.
- keine Werbefläche im Header.

## Bilder

- 8 Weltmotive als kontrollierte hochauflösende 1400×620-Assets.
- dieselbe kontrollierte Bildquelle wird auf der Startseiten-Weltkarte und als Hero der jeweiligen ersten Welt-/Hubebene benutzt.
- keine doppelten Motive auf derselben Seite.
- mindestens Person oder aktive Hände sichtbar.
- Männer/Frauen/Hände sichtbar gemischt; keine Wiederholung derselben Person als Serienmotiv.
- Tiere fachlich: Aquaristik, Terraristik, Insekten/Futtertiere, Imkerei/Bestäuber; kein Hund-/Haustierclaim, kein dekorativer Rahmen.

## Universelle Seiten-/Kategorie-Regeln

Diese Regeln gelten für die gesamte fachliche Portalhierarchie, nicht nur für die Startseite.

### Breadcrumb
- jede Seite/Kategorie außer der Startseite besitzt einen Breadcrumb;
- immer dieselbe horizontale Achse und Position;
- reale Parent-/Child-Hierarchie verwenden;
- aktuelle Seite nicht anklicken.

### Oberer Textbereich
- jede Seite/Kategorie besitzt oben einen klaren Titel-/Introbereich analog zum bewährten Pferdeatelier-Prinzip;
- vorhandene autoritative Introtexte/Metafelder verwenden;
- keine zweite Inhaltsautorität erzeugen.

### Erste CORE-Ebene / Welt-Hubs
- Gestalten, Fertigen, Technik, Forschen, Pflanzen, Tiere, Bewegen, Sammeln erhalten einen Hero;
- Hero verwendet exakt das jeweils freigegebene Weltmotiv der Startseite;
- darunter vollständiger Verweis auf die tatsächlich vorhandene nächste Kategorie-/Seitenebene.

### Jede fachliche Hub-/Kategorieebene
Strukturell vorgesehen:
1. Breadcrumb;
2. Titel/Intro;
3. Verweis auf vorhandene nächste Ebene;
4. Affiliate-Bannerplatz;
5. Beitragsvorschau;
6. Affiliate-Produkte;
7. maximal ein direkt verkaufbarer Werbeplatz.

Öffentlich leere Affiliate-Banner/Produkte bleiben unsichtbar. Eingeloggt sind leere Arbeitsplätze sichtbar. Der direkt verkaufbare Werbeplatz bleibt öffentlich auch unverkauft sichtbar.

## SEO-Meta

Kein zusätzliches SEO-Plugin erforderlich:
- Meta-Titel/Description per Seitentyp-Schablone;
- sinnvoller automatischer Fallback;
- individuelle Overrides;
- keine zweite Taxonomie-/Inhaltsautorität.

## Architekturgrenzen

- HD-001 bleibt Struktur-/Kategorieautorität.
- Affiliate-Zentrale bleibt Monetarisierungs-/Providerautorität.
- Designplugin rendert Darstellung und Slotpositionen.
- keine zweite Taxonomie.
- keine individuelle Pagebuilder-Seite pro Kategorie.
- ListingHive bleibt technische Grundhaut, nicht zweite Designautorität.

## PASS-Bedingung

PASS erst wenn:
- Fresh-Unpack/ZIP/PHP positiv;
- öffentlicher/eingeloggter Affiliatezustand positiv und negativ;
- genau-ein-Werbeplatz-Regel;
- Desktop/Tablet/Mobile;
- Breadcrumb-/Parentkette;
- erste Welt-Hubs verwenden exakt ihre Startseitenbilder;
- reale nächste Ebene vollständig sichtbar;
- Live-Readback in WordPress.

Lokaler PASS ist niemals Live-PASS.
