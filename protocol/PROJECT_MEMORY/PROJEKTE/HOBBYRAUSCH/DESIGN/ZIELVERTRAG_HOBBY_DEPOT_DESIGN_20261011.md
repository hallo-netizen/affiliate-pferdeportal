# ZV-HOBBYRAUSCH-DESIGN-001 – HOBBY DEPOT PORTALDESIGN

STATUS: AKTIV
FASSUNG: 2.4 / 2026-10-12

## Header / Navigation
- Logo unverändert und linksbündig.
- Header als 2-Spalten-System: links Logo; rechts Suchfeld + Navigation.
- Suchfeld auf Höhe der HOBBY-DEPOT-Wortmarke.
- Navigation rechts direkt an der unteren Headerkante.
- Ab 761 px: alle 8 Welten in exakt einer horizontalen Zeile und auf derselben Baseline, einschließlich Sammeln.
- <761 px: Mobilmenü.
- Navigationsicons entfallen; Text + Pfeil bleiben.
- Flyouts per Hover/Fokus/Klick und viewport-sicher.

## Acht Hauptwelten – Hero
- Jede Hauptwelt besitzt einen eigenen, natürlichen Hero-Text.
- direkte Ansprache mit `du`.
- keine Schablonensätze wie `X bündelt die wichtigsten Themen …`.
- Text sagt in einfachen Worten, was der Nutzer dort findet und wie er einsteigen kann.
- alle acht Texte inhaltlich verschieden.
- kein zusätzlicher `Mehr über <Welt> erfahren`-Accordion auf diesen Hauptwelten.

## Acht Hauptwelten – Text am Seitenende
- jede Hauptwelt endet mit einem längeren eigenständigen redaktionellen Text;
- klare, natürliche Zwischenüberschriften;
- direkte Ansprache;
- keine Keyword-/SEO-Textwüste;
- der Text erklärt Auswahl, Einstieg und Unterschiede der Bereiche;
- einzelne semantisch passende Textlinks verweisen ausschließlich auf tatsächlich vorhandene direkte Unterkategorien;
- Linkziel und Linktext müssen inhaltlich übereinstimmen.

## Hub-/Unterkategorie-Bilder
- alle 65 direkten Unterkategorien der acht Hauptwelten besitzen kontrollierte 600×320-Motive;
- ein klarer Hauptgegenstand oder eine klare Tätigkeit;
- größere/engere Ausschnitte;
- ruhiger Hintergrund;
- deutlich weniger Nebenmotive und Detailrauschen;
- keine identischen oder visuell nahezu identischen Motive im aktiven 65er-Bestand;
- kontrolliertes Designasset hat bei diesen 65 Karten Vorrang vor WordPress Featured Images;
- kein Parent-/Hero-Bild als Universalersatz.

## Karten
- natürliche Überschrift: `Weiter in <Welt>` / `Weitere Kategorien`.
- Kartentitel 15 px.
- Untertitel 12 px nur mit echtem Orientierungswert.
- kein generischer Fülltext.

## Monetarisierung im Kategorienraster
- Affiliate-Produkte stehen nicht zwischen Unterkategorie-Reihen.
- Nur ein Affiliate-Banner darf die letzte unvollständige 3er-Reihe ergänzen:
  - Rest 1 Kategorie → Banner 2 Kartenbreiten;
  - Rest 2 Kategorien → Banner 1 Kartenbreite;
  - Rest 0 → Banner als volle eigene Zeile.
- Produkte außerhalb des Kategorie-Rasters als natives Empfehlungsmodul.
- öffentlich leer unsichtbar; eingeloggt leer sichtbar.

## Bestehende Bindungen
- Direktwerbung: maximal ein Platz, ein Foto, Brush-Headline, heller CTA.
- keine Taxonomie-/Workflow-/Provideränderung durch Design.
- HD-001/HD-004 bleiben Kategorie-/Runtime-Autorität.
- Affiliate-Zentrale bleibt Monetarisierungsautorität.

## PASS
Kein Live-PASS ohne echten WordPress-Readback.

Lokaler Pflichtcheck:
- PHP/ZIP;
- 65/65 Bildpfade, 600×320;
- 65/65 unterschiedliche Datei-Hashes;
- Perceptual-Hash gegen visuelle Duplikate;
- Featured-Image-Override-Test;
- 8 unterschiedliche Hero-Texte;
- 8 Langtexte mit validierten Zielkategorie-Links;
- kein `Mehr über … erfahren` auf Hauptwelten;
- Navigation 1600/1200/1024/900/800/761: 8 Items eine Baseline, Sammeln eingeschlossen, kein horizontaler Overflow;
- 760 Mobile;
- Flyout Sammeln viewport-sicher.
