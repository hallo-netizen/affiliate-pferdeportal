# HOBBYRAUSCH – DESIGN-SPEZIFIKATION 1.0

STAND: 2026-10-10
STATUS: VERBINDLICHER DESIGNRAHMEN / UMSETZUNG NOCH NICHT FREIGEGEBEN

## 1. Zielbild

Hobbyrausch/Hobby Depot ist ein hochwertiges, helles, freundliches Informations- und Entdeckungsportal mit integrierten Affiliate- und Werbeflächen.

Die Monetarisierung ist Hauptintention des Geschäftsmodells, darf gestalterisch aber niemals den Eindruck einer Werbe-, Coupon- oder Vergleichsportal-Maschine erzeugen.

Leitbild:
**Information zuerst sichtbar – Monetarisierung intelligent eingebettet.**

## 2. Harte Designgrundsätze

1. Zentrale Steuerung aus Performance- und Wartungsgründen.
2. Gleiche Ebene = gleicher Template-Bauplan.
3. Die Ebenen unterscheiden sich in Dichte und Schwerpunkt, nicht in ihrer Designsprache.
4. Keine individuelle Seitengestaltung pro Kategorie/Hobby.
5. Leere Affiliate-/Banner-/Mietwerbe-Slots werden vollständig unsichtbar gerendert und erzeugen keinen Leerraum.
6. Jede Kategorie-/Hubseite besitzt oben einen redaktionellen Einleitungstext.
7. Erste Kategorien-/Weltenebene erhält hochwertige eigene Bildmotive.
8. Bildsprache portalweit: hell, freundlich, menschlich; auf jedem redaktionellen Hauptbild mindestens ein Mensch, mindestens jedoch sichtbar tätige Hände.
9. Keine sterile Produktfreisteller-Bildsprache als Portal-Hauptästhetik.
10. Design darf Affiliateprodukte integrieren, aber Content-Hierarchie, Lesbarkeit und Vertrauen haben visuell Vorrang.

## 3. Visuelle Richtung

Ausgangsbasis sind die zwei freigegebenen Hobby-Depot-Entwürfe vom 01.10.2026.

Verbindliche Synthese:
- warme, eigenständige Petrol/Charcoal/Creme-Richtung aus Entwurf 1;
- klare Raster-, Karten- und Navigationsordnung aus Entwurf 2;
- insgesamt heller und freundlicher als beide Hero-Beispiele;
- keine dominante dunkle Bildstimmung im Contentbereich;
- dunkler Header/Footer als stabiler Rahmen ist erlaubt.

### Farbprinzip
- Deep Charcoal: Header, Footer, starke Typografie
- Petrol/Türkis: Hauptakzent, CTA, aktive Zustände
- Cream/Off White: Hauptflächen
- Stone/Sand Beige: Sekundärflächen
- optional ein frischer blauer Mikroakzent ausschließlich für Finder/Tools/Interaktion, nicht als gleichwertige Markenfarbe

## 4. Typografie

Ziel: hochwertig + hobbytypisch + etwas charaktervoller, ohne verspielt/kitschig zu werden.

Empfohlene Richtung:
- Display/Headlines: **Bricolage Grotesque** oder gleichwertige charaktervolle Grotesk
- Fließtext/UI: **Inter** oder gleichwertige neutrale Sans

Performance-Regel:
- maximal 2 Schriftfamilien;
- nur tatsächlich benötigte Schnitte;
- keine dekorative Handschrift als Standardschrift;
- handschriftliche Akzente nur als seltenes grafisches Markenmotiv, nicht als UI-/Fließtext.

## 5. Bildsystem

### Pflicht
- helles Tageslicht / warme Innenräume
- echte Tätigkeit statt Pose
- Mensch im Motiv; mindestens Hände im aktiven Tun
- Materialität sichtbar: Werkzeug, Textur, Werkstoff, Projekt
- freundliche, glaubwürdige Situationen
- keine Stockfoto-Meetingästhetik
- keine künstlich düsteren Werkstattwelten

### Ebenen
- Startseite: große emotionale Hobby-Szene
- Hub 1: individuelles starkes Weltmotiv
- Hub 2: thematisches Tätigkeitsmotiv
- Hub 3: kompakteres Tätigkeitsmotiv oder Menschen/Hände-Detail
- Kategorie: ruhigeres fachliches Bild
- Beitrag: artikelspezifisches Motiv

### Bildkonsistenz
Feste Seitenverhältnisse pro Komponente; keine frei wechselnden Formate.

## 6. Globaler Seitenrahmen

Alle Seitentypen teilen:
- denselben Header;
- dieselbe Suche;
- dasselbe Mega-Menü;
- dieselbe Content-Maxbreite;
- dieselben Spacing-Tokens;
- dieselben Kartenradien/Schatten;
- dieselben Buttonformen;
- denselben Introblock;
- dieselbe Affiliate-Slot-Familie;
- denselben Footer.

## 7. Header + Mega-Menü

### Header
Desktop:
- Logo/Wordmark links;
- Claim direkt beim Markenbereich;
- große Portalsuche zentral;
- keine Shop-Icons, kein Warenkorb, keine Shop-Merkliste, kein allgemeiner Shop-Login;
- Hauptnavigation darunter bzw. integriert.

### Hauptnavigation – nur reale Portalbereiche
Die Navigationsbezeichnungen werden ausschließlich aus der bestehenden Hobbyrausch-Struktur abgeleitet. Keine erfundenen Shop- oder Sammelbegriffe.

Kernzugänge:
- Hobbywelten
- Hobbyfinder
- Magazin
- Anbieter

Zusätzliche statische Informationsseiten wie „Über uns“ dürfen separat geführt werden, sind aber keine Kategorieersatzstruktur.

### Mega-Menü „Hobbywelten“
Die acht geschützten CORE-Welten heißen exakt:
- Gestalten
- Fertigen
- Technik
- Forschen
- Pflanzen
- Tiere
- Bewegen
- Sammeln

Die direkten Kinder werden nicht im Designplugin umbenannt oder doppelt gepflegt, sondern serverseitig aus der aktuellen WordPress-/HD-001-Struktur gelesen. Gleiches gilt für spätere Änderungen innerhalb der autoritativen Kategorienstruktur.

Hobbywelten ist die Übersichts-/View-Seite und nicht Parent dieser acht ROOT-Welten.

### Hobbyfinder / Magazin
Hobbyfinder und Magazin verwenden ebenfalls ausschließlich die realen Bezeichnungen aus der bestehenden Struktur. Insbesondere werden keine Visualisierungs-Platzhalter wie „Kreativ“, „Modellbau“, „Fotografie“, „Natur“ oder vergleichbare Fantasiekategorien in die Produktivdarstellung übernommen.

### Performance
Mega-Menü und Kategorie-/Weltenkacheln werden serverseitig aus dem zentralen Ziel-/Navigationsbestand erzeugt; keine individuellen Menükopien und keine hart codierte zweite Taxonomie je Seite.
## 8. Affiliate-/Werbesystem

Es gibt drei Monetarisierungstypen:
1. Produktflächen
2. Banner
3. vermietete Werbeflächen / Sponsorenflächen

### Harte Leerregel
Ist ein Slot unbelegt:
- kein HTML-Wrapper mit Höhe;
- kein Platzhalter;
- kein Abstand;
- keine Überschrift;
- kein leeres Grid-Element.

### Gestaltung
Affiliateelemente nutzen dieselbe Designfamilie wie redaktionelle Karten.
Sie dürfen sich durch kleine Kennzeichnung/CTA unterscheiden, nicht durch schrille Fremdoptik.

### Kennzeichnung
- Affiliateprodukt: z. B. „Empfehlung“, „Passende Ausstattung“
- bezahlte Mietfläche: klar als „Anzeige“ oder „Partner“ kennzeichnen
- keine Verschleierung von bezahlter Werbung

### Priorität
Contentfluss bleibt auch bei vollständig belegten Slots dominant.

## 9. Templatefamilie

### A. Startseite
Ziel: Marke, Entdeckung, Orientierung, Inspiration, erste Monetarisierung.

Reihenfolge:
1. Header + Suche
2. heller emotionaler Hero mit Mensch/Händen
3. Nutzenleiste
4. „Beliebte Hobby-Welten“
5. kurzer Portal-Einleitungstext
6. Inspirations-/Hobbyfinder-Block
7. optional Produkt-Slot START_PRODUCT_1
8. Magazin-/Ratgeberblock
9. optional Banner START_BANNER_1
10. Community/Vertrauen
11. optional Mietfläche START_RENTAL_1
12. Footer

### B. Hub Ebene 1 – Hauptwelt
Ziel: große Orientierung.

1. Breadcrumb
2. Hero mit eigenem Weltfoto
3. H1 + redaktioneller Introtext
4. Raster aller direkten Ebene-2-Kinder
5. hervorgehobene Hobbys/Entdeckungen
6. optional HUB1_PRODUCT_1
7. passende Ratgeber
8. optional HUB1_BANNER_1
9. weiterführende Inspiration
10. Footer

Die Hub-1-Ebene ist die bildstärkste Ebene nach der Startseite.

### C. Hub Ebene 2
Ziel: strukturiertes Themencluster.

1. Breadcrumb
2. kompakter Hero/Bildkopf
3. H1 + Intro
4. Raster der Kinder/Hobbys
5. thematische Orientierung/Topbeiträge
6. optional HUB2_PRODUCT_1
7. optional HUB2_BANNER_1
8. Related/Weiterentdecken

### D. Hub Ebene 3
Ziel: konkrete Auswahl vor der Content-Kategorie.

1. Breadcrumb
2. kompakter Bildkopf
3. H1 + Intro
4. konkrete Hobby-/Unterthemenkarten
5. Einstiegs-/Praxisbeiträge
6. optional HUB3_PRODUCT_1
7. optional HUB3_BANNER_1
8. Related

Hub 3 bleibt visuell klar Teil derselben Familie; nur Dichte und Bildhöhe nehmen ab.

### E. Kategorieebene
Ziel: redaktionelles Themenarchiv mit Nutzwert und kontextueller Monetarisierung.

1. Breadcrumb
2. H1
3. verpflichtender Einleitungstext
4. optional ruhiges Kategorienbild
5. Beitragsgrid/-liste
6. optional CATEGORY_PRODUCT_1 nach erstem redaktionellen Block
7. weitere Beiträge
8. optional CATEGORY_BANNER_1
9. Related Kategorien/Hobbys
10. optional CATEGORY_RENTAL_1

Keine Affiliatefläche darf oberhalb von H1 + Einleitung den redaktionellen Einstieg verdrängen.

### F. Beitragsebene
Ziel: maximale Lesbarkeit, Vertrauen, kontextuelle Conversion.

1. Breadcrumb
2. Kategorie/Label
3. H1
4. kurze Einleitung
5. Hero-/Beitragsbild mit Mensch/Händen
6. Artikelkörper
7. optional ARTICLE_PRODUCT_1 an fachlich passender erster Stelle
8. Artikelkörper
9. optional ARTICLE_BANNER_1
10. Vergleich/Empfehlungen nur bei inhaltlicher Relevanz
11. Fazit / nächste Schritte
12. Related Content
13. optional ARTICLE_RENTAL_1

Affiliateblöcke dürfen nie automatisch einen Absatz semantisch zerreißen.

## 10. Karten- und Komponentenfamilie

Einheitliche Grundkarten:
- Bild oben oder links je Breakpoint
- klare Überschrift
- maximal kurze Teaser
- Pfeil/CTA als sekundäres Signal
- gleiche Radien und Schatten
- keine unterschiedlich gestalteten Karten pro Welt

Varianten:
- Navigation Card
- Editorial Card
- Product Card
- Partner/Ad Card
- Feature Card

Alle Varianten stammen aus denselben Design-Tokens.

## 11. Responsives Verhalten

Desktop:
- großzügige Mehrspaltenraster
- Mega-Menü voll

Tablet:
- Raster reduziert
- Menü komprimiert

Mobile:
- keine horizontalen Pflichtkarussells für Kernnavigation
- stabile 1–2-Spalten-Logik
- Affiliateplätze dürfen den ersten sichtbaren Content nicht dominieren
- leere Slots bleiben vollständig entfernt

## 12. Performancevertrag

- zentrale Templates, keine individuellen Pagebuilder-Seiten;
- serverseitige bedingte Slot-Ausgabe;
- nur benötigte CSS-/JS-Module;
- feste responsive Bildgrößen;
- WebP/AVIF sofern Pipeline verfügbar;
- lazy loading unterhalb Above-the-fold;
- Fonts sparsam und lokal/cachefreundlich;
- keine Animation ohne UX-Nutzen;
- kein JS zur bloßen Layoutkorrektur, wenn CSS/Markup ursächlich sauber lösbar ist.

## 13. Technische Architekturgrenze

Das Designplugin darf:
- Templates rendern;
- Design-Tokens verwalten;
- Header/Mega-Menü/Footer ausgeben;
- Ebene erkennen und das passende Template wählen;
- zentrale Slotpositionen bereitstellen;
- leere Slots unterdrücken;
- Bilder/Intro/Child-Grid/Contentblöcke darstellen.

Das Designplugin darf NICHT:
- Kategorie-/SEO-Wahrheit neu erfinden;
- Parents ändern;
- eigene parallele Taxonomie erzeugen;
- Affiliateprovider auswählen/ranken;
- Produktfeeds verwalten;
- Artikeltexte umschreiben.

HD-001 bleibt Strukturautorität.
Affiliate-Zentrale bleibt Monetarisierungs-/Providerautorität.
Designplugin ist Renderer.

## 14. Pferdeatelier-Basisplugin

Quellbasis im allgemeinen Pluginbestand:
`pferde-template-kit_V1.50.421.php`

Sie wird im Hobbyrausch-Designbüro zunächst unverändert als ORIGINAL-Evidence abgelegt.

Vor einer Hobbyrausch-Version müssen entfernt/ersetzt werden:
- Pferde-Atelier Branding/Logo/Taglines;
- pferdespezifische URLs und Navigationsannahmen;
- Pferde-spezifische Taxonomie-/Templatefälle;
- pferdespezifische Assets;
- pferdespezifische CSS-Namensräume, soweit ohne Funktionsverlust sauber generalisierbar;
- projektspezifische Texte/Labels;
- pferdespezifische Sonderfälle der Seitenebenen.

Erhalten werden nur nach Prüfung:
- zentrale Template-/Renderer-Architektur;
- zentrale Header/Footer/Navigation-Steuerung;
- slotbasierte Affiliate-Integration;
- bedingtes Ausblenden leerer Flächen;
- bewährte responsive Karten-/Grid-Mechanik;
- Performance-/Caching-Grundprinzipien.

Keine Funktion wird blind übernommen.

## 15. Abnahmereihenfolge

1. Designsystem / Tokens
2. Header + Mega-Menü + Footer
3. Startseite
4. Hub Ebene 1
5. Hub Ebene 2
6. Hub Ebene 3
7. Kategorie
8. Beitrag
9. Affiliate-Slot-Regression leer/1/mehrfach belegt
10. Responsive Browser-Hardtest
11. Performance-/DOM-/CSS-Prüfung
12. erst danach finales Pluginrelease

Jede neue Ebene wird gegen bereits freigegebene Komponenten gebaut; kein Redesign von null.

## 16. Nächster konkreter Schritt

**Startseite + globaler Rahmen als erster visueller Prototyp.**

Dabei werden zugleich festgelegt:
- endgültige Schriftkombination;
- finale Farbwerte;
- Header;
- Suche;
- Mega-Menü-Grundstil;
- Kartenstil;
- Buttons;
- Bildsprache;
- erste unsichtbar-schaltbare Affiliate-Slots.

Erst nach PASS wird Hub Ebene 1 daraus abgeleitet.


## 17. Freigabestand Startseite / Header-Nachtrag 2026-10-10

Der zuletzt visualisierte Startseitenentwurf ist als **gestalterische Startbasis freigegeben**.

### Logo
- das gezeigte Logo ist **nicht freigegeben**;
- bis zur gesonderten Logoentscheidung wird ausschließlich ein neutraler Logo-/Wordmark-Platzhalter verwendet;
- keine technische oder gestalterische Abhängigkeit an das provisorische Signet bauen;
- Logo muss später zentral austauschbar sein, ohne Header-/Layoutumbau.

### Claim
Im Kopfbereich wird ein eigener zentral steuerbarer Claim-Platz vorgesehen.

Desktop:
- kompakte einzeilige Claim-Zone im oberen Marken-/Headerbereich;
- sichtbar, aber deutlich kleiner als Suche und Hauptnavigation;
- Claim darf die Headerhöhe nur minimal erhöhen;
- Claimtext zentral austauschbar.

Mobile:
- Claim darf nicht zu einer dritten dominanten Headerzeile führen;
- entweder kurze einzeilige Fassung oder responsive Ausblendung zugunsten des Hero-Claims;
- keine Verdopplung desselben Claims direkt hintereinander.

### Freigegebene Startseitenstruktur
1. Header inkl. Claim-Platz, Suche und Navigation
2. kompakter Hero ohne Werbung
3. 8 reale Hobby-Welten
4. Hobbyfinder
5. Magazin/Ratgeber
6. Affiliate-Produkte – nur bei realer Belegung
7. Affiliate-Banner – nur bei realer Belegung
8. weiterführende redaktionelle Inhalte
9. direkt vermietete Werbefläche – nur bei realer Belegung
10. Footer

Erfundene Portalbereiche wie eine allgemeine "Community" sind nicht Bestandteil des freigegebenen Hobbyrausch-Bestands und dürfen nicht als Navigations-/Startseitenbereich eingebaut werden.

### Monetarisierungs-Trennung
Die drei Monetarisierungsarten bleiben in Layout und Technik klar getrennt:
- konkrete Affiliate-Produkte;
- Affiliate-Banner/Creatives;
- direkt vermietete Werbeflächen.

Alle drei folgen der harten Leerregel: **unbelegt = vollständig unsichtbar, ohne Restabstand**.


## 18. HARD RULE – AFFILIATE-PORTAL, KEIN SHOP

Hobbyrausch/Hobby Depot ist **kein eigener Shop**. Das Frontend darf deshalb keine Shop-UX vortäuschen.

Verboten im globalen Header und in der allgemeinen Portalnavigation:
- Warenkorb;
- Checkout;
- Merkliste/Wishlist als Shopfunktion;
- Kundenkonto/Shop-Login;
- Bestellstatus;
- Produktbestand;
- Shop-Kategoriesprache, sofern sie nicht rein redaktionell gemeint ist.

Affiliate-Produkte sind redaktionell kuratierte externe Empfehlungen. Ein Klick führt zum jeweiligen Partner/Anbieter; es gibt keinen eigenen Kaufprozess.

HivePress-/Anbieterfunktionen sind eine eigene Portal-Säule und dürfen nicht als allgemeine Shop-Konto-UX in den Hauptheader gezogen werden. Falls später ein Anbieter-Login gebraucht wird, wird er separat und bewusst gestaltet.

### Header-Grundstruktur
- Logo / Wordmark
- Claim direkt beim Markenbereich
- prominente Portalsuche
- echte Portalnavigation aus dem freigegebenen Hobbyrausch-Bestand
- keine Shop-Icons

### Navigationssprache
Die Navigation wird aus dem realen Portalbestand abgeleitet, nicht aus Shopmustern.
Kernzugänge:
- Hobbywelten
- Hobbyfinder
- Magazin / Inspiration
- Anbieter / HivePress, wenn im jeweiligen Stand sichtbar vorgesehen
- weitere echte Portalbereiche laut Strukturautorität

Keine erfundenen Bereiche wie Community, Shop, Warenkorb oder Merkliste.


## 19. VERBINDLICHER HEADER-CLAIM

Freigegebener Claim unter dem Logo:

**Hobbys. Ideen. Möglichkeiten.**

Regeln:
- auf allen Seitentypen im Marken-/Headerbereich;
- nicht identisch mit der Hero-Headline der Startseite;
- klein, ruhig und markenhaft;
- zentral austauschbar;
- auf Mobile kompakt darstellen, ohne den Header unnötig zu erhöhen.

## 20. PORTALIDENTITÄT IM HEADER – KEIN SHOP-EINDRUCK

Weil der Markenname „Hobby Depot“ allein auch als Handels-/Shopname gelesen werden kann, wird der Portalcharakter aktiv im Header kommuniziert – jedoch ohne defensiven Hinweis „kein Shop“.

### Desktop
Zusätzliche sehr schmale Portalzeile oberhalb oder unmittelbar am Hauptheader, ca. 28–30 px:
**Inspiration, Wissen & Empfehlungen rund ums Hobby.**

Sie ist deutlich kleiner als Markenclaim, Suche und Navigation und darf den Header nicht optisch aufblasen.

Der Markenclaim unter dem Logo bleibt:
**Hobbys. Ideen. Möglichkeiten.**

### Mobile
Keine zusätzliche eigenständige dritte Headerzeile. Die Portalzeile wird responsiv ausgeblendet oder in eine kurze Microcopy innerhalb des Menüs/Headers überführt.

### Affiliate-Sprache
Damit der Portalcharakter auch in Monetarisierungsflächen erhalten bleibt:
- CTA „Zum Anbieter“, „Mehr erfahren“, „Empfehlung ansehen“ statt „Kaufen“;
- Affiliateprodukt als redaktionelle Empfehlung darstellen;
- bezahlte Fläche klar „Anzeige“/„Partner“ kennzeichnen;
- kein Warenkorb-, Bestand-, Checkout- oder Shop-Wording.

So wird der Unterschied zum Shop über Sprache, Navigation und Seitenstruktur vermittelt, nicht über einen störenden Warnhinweis.
