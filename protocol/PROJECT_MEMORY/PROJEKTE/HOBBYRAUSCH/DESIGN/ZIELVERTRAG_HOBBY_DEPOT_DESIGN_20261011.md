# ZV-HOBBYRAUSCH-DESIGN-001 – HOBBY DEPOT PORTALDESIGN

STATUS: AKTIV  
FASSUNG: 1.5 / 2026-10-11  
GELTUNGSBEREICH: HOBBYRAUSCH / DESIGN / WORDPRESS-DARSTELLUNG

## Ziel

Hobby Depot wird als hochwertiges, helles Informations- und Inspirationsportal mit integrierter Affiliate-Monetarisierung umgesetzt – ausdrücklich **nicht als Shop**.

Technische Theme-Basis ist **ListingHive**. Das Hobby-Depot-Designplugin ist für Markenrahmen, Header, Footer, Startseite und die Hub-/Contenttemplates visuell autoritativ.

## Marke / Header

- Logo bleibt unverändert die freigegebene Variante 3.
- Topbar-Inhalt bleibt unverändert: **Inspiration, Wissen & Empfehlungen rund ums Hobby.**
- Topbar dunkel im Footer-Farbton.
- Body weiß.
- Hauptheader warmes Creme/Off-White.
- Suche weiß.
- keine Anzeige im Header.
- Desktopnavigation zeigt exakt: Gestalten · Fertigen · Technik · Forschen · Pflanzen · Tiere · Bewegen · Sammeln.
- Navigation sitzt unterhalb der Suche, aber **mit sichtbarer Luft zur unteren Trennlinie**; keine Berührung/Überlappung.
- Mega-Menü pro CORE-Welt, nur direkte Kinder, ohne Hover-Lücke.
- Die Desktop-Vollnavigation darf niemals horizontal abgeschnitten werden.
- Bis einschließlich **1560 px** schaltet der Header frühzeitig auf Menü/Dropdown; erst darüber bleibt die komplette 8-Welten-Zeile offen sichtbar.

## Startseite

- Hero-Headline: **„Entdecke dein nächstes Hobby.“**
- Bildschriftzug bleibt: **„Mehr Zeit für das, was dich begeistert.“**
- Hero links weiß, feiner 1-px-Rahmen, sichtbarer Abstand nach oben.
- alle 8 Hauptwelten zusätzlich zur Navigation als Weltkarten.
- Desktop 4×2; Mobile 2×4.
- Hobbyfinder / Magazin / Wissen & Glossar mit identischem Creme-Hintergrund.
- Affiliate-Banner nur real öffentlich sichtbar; leer nur eingeloggt.
- Affiliate-Produkte nur real öffentlich sichtbar; leer nur eingeloggt.
- genau ein direkt verkaufbarer Werbeplatz; öffentlich auch unverkauft sichtbar.
- keine Werbefläche im Header.

## Typografie

Der Hub-/Navigations-Fix darf die freigegebenen Schriftgrößen **nicht verkleinern**. Referenz bleiben die Werte aus 1.50.614/1.50.615:
- Desktop-Navigation 14 px;
- Hub-Intro 16 px;
- redaktioneller Kategorietext 15 px;
- Unterkategorie-Titel 15 px;
- Unterkategorie-Kurztext 11 px;
- Hub-H1 clamp(38px, 4.3vw, 60px).

## Erste CORE-Ebene / Welt-Hubs

- Hero verwendet exakt das Weltmotiv der Startseitenkarte.
- Hero enthält bereits Titel + kompakten Einleitungstext.
- Deshalb **kein zweiter offen sichtbarer Fließtextblock direkt unter dem Hero**.
- Zusatzwissen bleibt vollständig im initialen HTML, aber standardmäßig eingeklappt unter **„Mehr über <Welt> erfahren“**.
- Der Block **„Was du hier findest“** liegt innerhalb dieser Aufklappfläche.
- darunter vollständiger Verweis auf die tatsächlich vorhandene nächste Ebene.

## Fotos auf oberen Hubebenen

- Auf `hub1` und `hub2` dürfen Unterkategorie-Karten kompakte Fotos tragen.
- echtes gepflegtes Child-Featured-Image hat Vorrang.
- Es ist **nicht erlaubt**, bei fehlendem Bild einfach dasselbe Parent-/Weltbild auf allen Karten zu wiederholen.
- Für Gestalten bestehen sieben eigene, unterschiedliche Fallbackmotive passend zu:
  - Druck & Fotografie
  - Malen & Zeichnen
  - Miniaturen & Szenen
  - Oberfläche & Deko
  - Papierkunst
  - Schrift & Lettering
  - Textilgestaltung
- Für andere Hubs ohne echtes Child-Bild bleibt die jeweilige Karte vorerst bewusst ohne Fotokante statt ein falsches/dupliziertes Motiv zu zeigen.
- tiefe Kategorie-/Leafebenen bleiben text-/iconorientiert.

## Unterkategorie-Raster

Desktop:
- 6-Spalten-Basis;
- regulär 3 Karten pro Reihe;
- Rest 2 = 50/50;
- Rest 1 = volle letzte Reihe;
- keine leeren Rasterlöcher.

Tablet:
2 Spalten.

Mobile:
1 Spalte.

## Monetarisierung

Reihenfolge:
1. Breadcrumb
2. Hero
3. kompakte Zusatzinfo
4. nächste Ebene
5. direkt verkaufbarer Werbeplatz
6. Beitragsvorschau
7. Affiliate-Banner
8. Affiliate-Produkte

### Direkt verkaufbarer Werbeplatz
- maximal einer pro Seite/Kategorie/Beitrag;
- direkt nach den Unterkategorien;
- **ein einziges Foto**, keine 4er-Collage;
- Text liegt **über dem Foto**;
- Headline **„Hier könnte Ihre Werbung stehen.“** liegt auf einem auffälligen hellen Brush-/Pinselstrich;
- CTA **„Werbemöglichkeiten & Preise“**;
- verkauft klar als Anzeige/Werbung.

### Affiliate
- optisch nativ in den Content integriert;
- kleine Kennzeichnung **Anzeige · Partner**;
- öffentlich leer unsichtbar;
- eingeloggt leer sichtbar.

## Bilder

- 8 Weltmotive als kontrollierte hochauflösende 1400×620-Assets.
- dieselbe Quelle für Startseitenkarte und Welt-Hero.
- keine doppelten Motive innerhalb derselben Kartenreihe.
- Männer/Frauen/Hände sichtbar gemischt.
- Tiere fachlich passend und rahmenlos.

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
- keine individuellen Pagebuilder-Seiten.
- ListingHive bleibt technische Grundhaut.

## PASS-Bedingung

PASS erst wenn:
- Fresh-Unpack/ZIP/PHP positiv;
- Schriftgrößen gegen 1.50.614/615 unverändert;
- Nav mit Luft zur Trennlinie;
- Navigation bei mittleren Breiten ohne Beschnitt;
- Hub1 ohne doppelten offenen Text;
- Gestalten 7/7 unterschiedliche Kartenbilder;
- kein generischer Parentbild-Fallback;
- Direktwerbung exakt 1 Foto + Brushstroke-Headline;
- genau-ein-Werbeplatz-Regel;
- Desktop/Tablet/Mobile;
- Live-Readback in WordPress.

Lokaler PASS ist niemals Live-PASS.
