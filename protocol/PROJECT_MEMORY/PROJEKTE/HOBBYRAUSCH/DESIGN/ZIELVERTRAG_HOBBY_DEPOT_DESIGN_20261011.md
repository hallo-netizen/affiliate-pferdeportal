# ZV-HOBBYRAUSCH-DESIGN-001 – HOBBY DEPOT PORTALDESIGN

STATUS: AKTIV  
FASSUNG: 1.6 / 2026-10-11  
GELTUNGSBEREICH: HOBBYRAUSCH / DESIGN / WORDPRESS-DARSTELLUNG

## Ziel
Hobby Depot bleibt ein hochwertiges, helles Informations- und Inspirationsportal mit integrierter Monetarisierung – kein Shop.

ListingHive bleibt technische Theme-Basis. Das Hobby-Depot-Designplugin ist visuell autoritativ.

## Header / Navigation
- Logo bleibt unverändert, aber **lesbar groß**.
- Desktop/Tablet-Logo darf nicht auf Miniaturgröße schrumpfen.
- Topbar-Inhalt unverändert; dunkler Footer-Farbton.
- Hauptheader creme/off-white.
- Desktopnavigation zeigt immer die 8 Welten.
- >1180 px: 8 Welten in einer Reihe.
- 761–1180 px: 8 Welten sichtbar in 4×2, **kein Hamburger**, kein Abschneiden.
- <761 px: Hamburger/Mobilmenü.
- Navigation hat Luft zur unteren Trennlinie; keine Überlappung.
- keine Anzeige im Header.

## Typografie
Keine globale Verkleinerung:
- Navigation 14 px;
- Hub-Intro 16 px;
- Kategorietext 15 px;
- Unterkategorie-Titel 15 px;
- Unterkategorie-Kurztext 11 px;
- Hub-H1 unverändert.

## Erste Welt-/Hubebene
- Hero: Weltbild + Titel + kurzer Lead.
- darunter **kein zweiter offener Fließtext**.
- Zusatzwissen vollständig im HTML, standardmäßig unter `Mehr über <Welt> erfahren` geschlossen.
- Aufklappbereich über die volle Inhaltsbreite, **weißer/neutraler Hintergrund**, keine wechselnden Farbboxen.
- Text mit echten Absätzen.
- `Was du hier findest` innerhalb des Aufklappbereichs, ebenfalls ohne separate Farbbox.

## Unterkategorie-Karten
- obere Hubs dürfen Fotos verwenden.
- jedes Foto einheitliches Querformat **600×320 / 1,875:1**.
- echtes Child-Featured-Image hat Vorrang.
- Gestalten besitzt 7 eindeutige passende Fallbackmotive.
- niemals dasselbe Parent-/Weltbild mehrfach als Ersatz in derselben Reihe.
- fehlendes Bild = lieber ohne Bild als falsche Wiederholung.

### Rasterregel
Desktop nutzt 6 Spalten und vollständige Reihen:
- 1 → 1
- 2 → 2
- 3 → 3
- 4 → 2+2
- 5 → 3+2
- 6 → 3+3
- 7 → **3+2+2**
- 8 → 3+3+2
- 10 → 3+3+2+2
usw.

Tablet: 2 Spalten, bei ungerader Zahl letzte Karte volle Breite.  
Mobile: 1 Spalte.

## Monetarisierung

### Affiliate
Affiliate-Banner und Produkte gehören **in den normalen Kategorie-/Hubfluss**, nicht als isolierte Blöcke ganz unten.
- direkt innerhalb des Bereichs `Nächste Ebene` integriert;
- Banner als native Partnerzeile;
- Produkte als native Partnerkarten im gleichen Rhythmus;
- Kennzeichnung `Anzeige · Partner`;
- öffentlich leer unsichtbar;
- eingeloggt leer sichtbar.

### Direkt verkaufbarer Werbeplatz
- maximal einer;
- direkt nach dem Kategorie-/Partnerbereich;
- **ein einziges Foto**;
- Text über dem Foto;
- Headline `Hier könnte Ihre Werbung stehen.` auf hellem Pinselstrich;
- CTA `Werbemöglichkeiten & Preise`;
- CTA hell und kontrastreich, nie dunkel auf dunklem Foto.

## Startseite
Bestehender freigegebener Stand bleibt gebunden:
- Logo unverändert;
- Topbar-Inhalt unverändert;
- Hero-Headline `Entdecke dein nächstes Hobby.`;
- Bildspruch bleibt;
- 8 Hauptwelten;
- max. ein verkaufbarer Werbeplatz;
- Affiliate leer öffentlich unsichtbar.

## Architekturgrenzen
- HD-001 bleibt Struktur-/Kategorieautorität.
- Affiliate-Zentrale bleibt Provider-/Monetarisierungsautorität.
- Designplugin rendert Darstellung/Slotposition.
- keine neue Taxonomie.
- kein Pagebuilder-Sonderweg.

## PASS-Bedingung
PASS erst wenn:
- Fresh ZIP/PHP;
- Desktop 1600 / mittlere Breite 1024 / Mobile 390 ohne horizontalen Overflow;
- Navigation sichtbar bei 1024;
- Logo bei 1024 klar lesbar;
- Header/Breadcrumb ohne Überlappung;
- Gestalten 7/7 unterschiedliche Querformatbilder;
- Desktop-Raster 7 = 3+2+2;
- Hub-Aufklapptext mit echten Absätzen und ohne Farbbox-Wechsel;
- Affiliate innerhalb `Nächste Ebene`;
- Direktwerbung ein Foto + Brush + heller CTA;
- Live-Readback.

Lokaler PASS ist niemals Live-PASS.
