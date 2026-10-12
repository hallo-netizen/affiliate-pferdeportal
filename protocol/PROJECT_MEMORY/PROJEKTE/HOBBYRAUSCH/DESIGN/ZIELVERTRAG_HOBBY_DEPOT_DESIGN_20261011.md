# ZV-HOBBYRAUSCH-DESIGN-001 – HOBBY DEPOT PORTALDESIGN

STATUS: AKTIV
FASSUNG: 3.5 / 2026-10-12

## Header / Navigation
- Logo unverändert und linksbündig.
- Header als 2-Spalten-System: links Logo; rechts Suchfeld + Navigation.
- Suchfeld auf Höhe der HOBBY-DEPOT-Wortmarke.
- `Hobbys. Ideen. Möglichkeiten.` steht exakt mittig unter der HOBBY-DEPOT-Wortmarke bzw. exakt in deren Breite; kein seitlicher Versatz.
- Die sichtbare Unterkante des Claims und die Unterkante/Baseline der Hauptnavigation bilden eine gemeinsame horizontale Linie.
- Für diese Linie wird das Logo vertikal positioniert; die Navigation wird nicht erneut nach unten verschoben.
- Ab 761 px: alle 8 Welten in exakt einer horizontalen Zeile und auf derselben Baseline, einschließlich Sammeln.
- <761 px: Mobilmenü.
- Navigationsicons entfallen; Text + Pfeil bleiben.
- Flyouts per Hover/Fokus/Klick und viewport-sicher.
- Der live bestätigte Header-/Navigationsstand ist eingefroren.

## Acht Hauptwelten – Hero
- Jede Hauptwelt besitzt einen eigenen, natürlichen Hero-Text.
- direkte Ansprache mit `du`.
- keine Schablonensätze.
- Text sagt in einfachen Worten, was der Nutzer dort findet.
- alle acht Texte inhaltlich verschieden.
- kein `Mehr über <Welt> erfahren`-Accordion auf Hauptwelten.
- Hero-Bilder Ebene 1 bleiben unverändert.

## Acht Hauptwelten – Text am Seitenende
- jede Hauptwelt endet mit einem längeren eigenständigen redaktionellen Text;
- klare, natürliche Zwischenüberschriften;
- direkte Ansprache;
- keine Keyword-/SEO-Textwüste;
- interne Links sparsam: **maximal 3 pro Hauptwelt, maximal einer pro Abschnitt**;
- nur semantisch passende reale Zielkategorien.

## Hub-/Unterkategorie-Bilder Ebene 1
- alle 65 direkten Unterkategorien besitzen kontrollierte Motive;
- Thema auf den ersten Blick verständlich;
- kein unnötiger Lupen-/Makroeindruck;
- ruhiges Bildumfeld;
- keine wiederverwendeten Szenenfamilien;
- kein Rückfall auf alte mehrfach verwendete Featured Images;
- kein Passepartout/Bild-im-Bild.
- Stand 1.50.634 wird vorerst akzeptiert und nicht weiter verändert.

## Kategorieebene 2 / Hub2
- Breadcrumb oben.
- über der H1 steht ein kurzer **individueller Claim pro Kategorie**, kein generisches `Themenbereich`;
- H1 + natürlicher, gut lesbarer Orientierungstext direkt oben; auf Hub2 ca. 150–190 Wörter Gesamttext nach dem bewährten Kategorie-Textprinzip;
- ein gut lesbarer Lead bleibt direkt sichtbar; die weitere Vertiefung wird im selben oberen Bereich über `Mehr zu <Kategorie> erfahren` aufklappbar;
- Standard für Ebene 2 bleibt ohne großes Hero-Foto. Der Pilot `Buch & Papier` darf als geprüfte Ausnahme einen **kompakten Split-Hero mit bereits vorhandenem Kategorie-Vorschaubild** verwenden; kein separates neues Hero-Asset.
- der lange Erklärungstext steht nicht oben, sondern am Seitenende.
- direkte nächste Ebene vollständig sichtbar verlinken.
- kleine Kartenfotos nur als Orientierung in den Verweisen; kein zweites großes Hero. Wo kein sinnvolles Kartenfoto vorhanden ist, thematisch passende unterschiedliche Icons statt eines identischen Welticons verwenden.
- Affiliate-Banner als eigener Bereich **nach** der nächsten Ebene, nicht als Füller zwischen Kategorien.
- danach passende Artikelvorschau; auf Hub2 bis zu vier Beiträge mit Beitragsbild;
- für reine Designtests dürfen klar markierte private `[TEST]`-Beiträge eingeloggten Admins als Vorschau-Fallback angezeigt werden, wenn noch keine gleichnamige Beitragskategorie existiert; reale öffentliche Beitragslogik bleibt davon unberührt.
- danach konkrete Affiliate-Produkte passend zum aktuellen Hub2-Kontext.
- danach genau ein direkt verkaufbarer Werbeplatz.
- danach längerer redaktioneller Erklärungstext.
- je tiefer die Seite, desto konkreter die Produktbelegung; nicht einfach mehr Produkte, sondern stärker thematisch passende Produkte.
- Hub2 verwendet dafür die konkreteren `category_product_1..3`-Slots.
- öffentlich leere Affiliate-Banner/Produkte unsichtbar; eingeloggte Arbeitsvorschau erlaubt.

## Karten
- natürliche Überschrift `Weiter in <Thema>` / `Weitere Kategorien`.
- Kartentitel 15 px.
- Untertitel nur mit echtem Orientierungswert.
- kein generischer Fülltext.

## Monetarisierung
- Affiliate-Produkte nie zwischen Unterkategorie-Reihen.
- Banner und Affiliate-Produkte sind getrennte Slottypen.
- Direktwerbung ist ebenfalls getrennt und maximal ein Platz pro Seite.
- Affiliate-Zentrale bleibt Monetarisierungsautorität.

## Bestehende Bindungen
- keine Taxonomie-/Workflow-/Provideränderung durch Design.
- HD-001/HD-004 bleiben Kategorie-/Runtime-Autorität.
- keine neue Architektur.

## PASS
Kein Live-PASS ohne echten WordPress-Readback.


## Pilot Hub2 – Buch & Papier / 1.50.641
Noch **keine portalweite Regel**, sondern Live-Pilot:
- kurze klare Fotos für direkte Unterkategorien statt Icon-Wüste;
- Desktop 3-spaltige Fotokarten, Tablet 2-spaltig, Mobil 1-spaltig;
- Kachelbilder verwenden dieselben sichtbaren Maße wie Ebene 1: Desktop 200×107, Tablet 165×88, Mobil 145×78;
- Claim `Papier kann mehr.` mit schreibschriftartigem System-Fontstack und dynamischem CSS-Pinselstrich als wiederkehrendem Gestaltungsmotiv;
- Reihenfolge: Unterkategorien → konkrete Produkte → 3 Beiträge → Affiliate-Banner → verkaufbarer Werbeplatz;
- kein langer Seitenendtext auf diesem Hub2;
- Split-Hero sitzt vollständig innerhalb derselben Body-Breite wie die folgenden Inhaltsabschnitte;
- Hero-Foto nutzt das vorhandene 600×320-Kategorieasset und läuft weich in Weiß aus;
- Aufklapptext darf die Bildhöhe/-breite nicht verändern;
- Performance: 5 Pilotfotos zusammen ca. 66 KB; Split-Hero verwendet zusätzlich ein bereits vorhandenes 45,9-KB-Kategorieasset, kein neues Hero-Bild;
- andere Hub2-Seiten bleiben unverändert, bis der Pilot live abgenommen ist.

- Claim-Unterstrich: Variante-1-Charakter, beige Sekundärfarbe, länger/geschwungener/natürlicher, mit deutlichem Abstand zur Schrift; Schriftgröße selbst unverändert.
- Hero-Bild: rechte Ecken 2 px.
- Kategorie-Karten: maximal 2 px Rundung.
- Kategorie-Bilder müssen exakt innerhalb des Kartenrahmens bleiben; kein Überstand, keine sichtbare Lücke, kein zusätzlicher Innenrahmen.
