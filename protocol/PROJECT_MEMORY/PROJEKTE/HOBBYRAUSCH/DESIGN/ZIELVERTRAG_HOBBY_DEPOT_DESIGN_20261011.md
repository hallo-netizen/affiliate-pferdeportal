# ZV-HOBBYRAUSCH-DESIGN-001 – HOBBY DEPOT PORTALDESIGN

STATUS: AKTIV  
FASSUNG: 1.7 / 2026-10-11

## Header / Navigation
- Logo unverändert.
- Logo in jeder Ansicht linksbündig.
- Logo niemals durch feste Max-Höhe verzerren; natürliches Seitenverhältnis bleibt erhalten.
- Logo liegt oberhalb der Weltnavigation.
- Navigation sitzt sichtbar tiefer in einer eigenen unteren Headerzeile, aber ohne Berührung mit der Trennlinie.
- >1180 px: 8 Welten in einer Reihe.
- 761–1180 px: 8 Welten sichtbar 4×2.
- <761 px: Hamburger/Mobilmenü.
- Mega-/Flyout-Menüs sind am jeweils ausgelösten Weltpunkt verankert; kein links versetztes Flyout.
- Topbar-Inhalt unverändert.
- keine Anzeige im Header.

## Erste Welt-/Hubebene
- Hero: Weltbild + Titel + kurzer Lead.
- Aufklapptext darf **keine bereits im Hero sichtbaren Sätze wiederholen**.
- `Mehr über <Welt> erfahren` bleibt standardmäßig geschlossen.
- Aufklappbereich volle Inhaltsbreite, neutral/weiß.
- echte Absätze.
- `Was du hier findest` ohne separate Farbbox.

## Unterkategorie-Karten
- obere Hubs mit Bildern.
- alle Bilder Querformat.
- Bildfläche **kompakt als Thumbnail in der Karte**, nicht als großflächige halbe Seitenhöhe.
- einheitliche Bildfläche je Raster.
- Gestalten 7 unterschiedliche passende Motive.
- echtes Child-Featured-Image gewinnt.
- kein mehrfacher Parentbild-Fallback.

### Ungerade Zahlen
Desktop:
- Grundraster 3 Karten pro Reihe.
- ohne Monetarisierung wird Rest 2 als 2+2 bzw. Rest 1 als volle letzte Karte behandelt.
- wenn Affiliate-Produkte vorhanden sind, dürfen diese **im selben Raster** fehlende Plätze einer ungeraden letzten Reihe füllen.
- Kategoriehierarchie und Werbung bleiben durch `Anzeige · Partner` eindeutig unterscheidbar.

Tablet: 2 Spalten.  
Mobile: 1 Spalte.

## Monetarisierung

### Affiliate
Affiliate ist nicht als eigener Block unter die Seite zu hängen.
- Banner liegt als native, volle Partnerzeile **innerhalb des Bereichs Nächste Ebene**, nach der ersten Kategorienreihe.
- Produktwerbung erscheint als native Karten **im selben Kartenraster** und kann freie Plätze der letzten Reihe auffüllen.
- klar `Anzeige · Partner` kennzeichnen.
- öffentlich leer unsichtbar.
- eingeloggt leer sichtbar.
- keine zusätzliche Standalone-Banner-/Produktsektion danach.

### Direkt verkaufbarer Werbeplatz
- maximal einer.
- direkt nach Kategorie-/Partnerbereich.
- ein Foto.
- neuer, auffälliger visueller Aufbau:
  - dunkler lesbarer Bildverlauf,
  - Headline direkt auf echtem farbigen Brushstroke,
  - heller kontrastreicher CTA.
- `Hier könnte Ihre Werbung stehen.`
- `Werbemöglichkeiten & Preise`
- kein dunkler Button auf dunklem Foto.

## Startseite
Bestehende gebundene Regeln bleiben unverändert:
- Logo unverändert;
- Topbar unverändert;
- Hero-Headline `Entdecke dein nächstes Hobby.`;
- Bildspruch bleibt;
- 8 Hauptwelten;
- max. ein verkaufbarer Werbeplatz;
- Affiliate leer öffentlich unsichtbar.

## Architektur
- HD-001/HD-004 bleiben Kategorie-/Runtime-Autorität außerhalb dieses Designplugins.
- Affiliate-Zentrale bleibt Provider-/Monetarisierungsautorität.
- Designplugin rendert nur Darstellung/Slotposition.
- keine zweite Taxonomie.
- kein Pagebuilder-Sonderweg.

## PASS
Kein Live-PASS ohne echten WordPress-Readback.
