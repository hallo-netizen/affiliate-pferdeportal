# ZV-HOBBYRAUSCH-DESIGN-001 – HOBBY DEPOT PORTALDESIGN

STATUS: AKTIV
FASSUNG: 3.8 / 2026-10-12

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
- Der akzeptierte Buch-&-Papier-Stand **1.50.645** ist die verbindliche **visuelle Vorlage** für alle Hub2-Seiten.
- Breadcrumb oben.
- kompakter Split-Hero innerhalb der normalen Body-Breite;
- links Claim + H1 + Text, rechts das bereits vorhandene Kategorie-Vorschaubild;
- Hero-Bild läuft weich in Weiß aus und verändert beim Öffnen des Texts seine Größe nicht;
- kein neues separates Hero-Asset erzeugen.
- über der H1 steht ein kurzer individueller, natürlicher Claim in derselben Schreibschrift-/Brush-Optik.

### Textregel
Verbindliche Quelle:
`protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/DESIGN/TEXTREGELN_PFERDEATELIER_KOPIE_20261012.md`

Es werden **nur die redaktionellen Textregeln** aus Pferdeatelier übernommen, nicht dessen UI:
- ca. 150–200 Wörter;
- natürliches normales Deutsch;
- themenspezifische Substanz;
- keine Generator-/Padding-Sprache;
- keine generische Schlussformel;
- fachliche, praktische Orientierung;
- nur reale vorhandene Unterthemen nennen.

Hobby-Depot-Darstellung bleibt wie Buch & Papier:
**sichtbarer Lead → `Mehr zu <Kategorie> erfahren` → restlicher Text im Aufklapper.**
Kein zusätzlicher zweiter Erklärungstext unterhalb des Aufklappers.

### Unterkategoriekarten
- jede tatsächlich vorhandene direkte Unterkategorie erhält eine **Fotokarte**;
- kein Rückfall auf die frühere Icon-Wüste;
- Buch & Papier behält seine fünf akzeptierten Motive;
- bei allen anderen Hub2-Seiten müssen die Fotos innerhalb derselben Seite unterschiedlich sein;
- echtes Featured Image der Zielseite hat Vorrang;
- wenn keines vorhanden ist, wird ein noch unbenutztes vorhandenes kontrolliertes Foto derselben Hobbywelt verwendet;
- das Eltern-/Hero-Motiv darf nicht als Universalbild für alle Kindkarten wiederholt werden;
- jede Karte erhält unter dem Titel eine kurze sinnvolle Orientierungszeile wie bei Buch & Papier;
- Bilder exakt im vorhandenen Ebene-1-Kartenrahmen: Margin 0, Padding 0, Foto-Radius 0, Overflow hidden, Object-fit cover;
- Desktop 3 Karten nebeneinander; unvollständige letzte Reihe linksbündig;
- Affiliate-Banner darf den freien Restplatz der letzten 3er-Reihe füllen; bei voller Reihe eigene Bannerzeile.

### Reihenfolge darunter
- konkrete `category_product_1..3`-Produkte;
- **3** passende Beiträge mit Beitragsbild;
- genau ein direkt verkaufbarer Werbeplatz;
- **kein** zusätzlicher redaktioneller Seitenendtext auf Hub2;
- öffentlich leere Affiliate-Flächen unsichtbar; eingeloggte Arbeitsvorschau erlaubt;
- je tiefer die Seite, desto konkreter die Produktbelegung; nicht einfach mehr Produkte.

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
Kein Live-PASS ohne echten WordPress-Readback.\n