# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-11
STATUS: **1.50.616 LOCAL HARD PASS / HUB-DOPPELTEXT ENTFERNT / 7 UNIQUE GESTALTEN-BILDER / EINZELBILD-WERBUNG / NAV KORRIGIERT / WORDPRESS-LIVE OFFEN**

## Autoritative Bindungen

Zielvertrag:
`ZIELVERTRAG_HOBBY_DEPOT_DESIGN_20261011.md`

Fehlerquelle:
`FEHLERQUELLEN.md`

Technische Plugin-Current:
`../PLUGINS/PLUGIN_AKTEN/HD-003-DESIGN-TEMPLATE-KIT/CURRENT.md`

Theme-Unterbau:
**ListingHive**.

## 1.50.616 – Änderungen

### Navigation
- Desktop-Offset von 22 px auf **8 px** reduziert;
- dadurch keine Berührung mit der unteren Trennlinie;
- Vollnavigation nur oberhalb **1560 px**;
- 761–1560 px Menü/Dropdown;
- unter 980 px zweispaltiges Dropdown;
- Mobile separat.

### Typografie
Geprüft gegen 1.50.614:
- Desktopnavigation 14 px unverändert;
- Hubintro 16 px unverändert;
- Kategorietext 15 px unverändert;
- Unterkategorie-Titel 15 px unverändert;
- Unterkategorie-Kurztext 11 px unverändert;
- Hub-H1 unverändert.

Es wurde **keine globale Schriftverkleinerung** vorgenommen.

### Erste Hubebene
- Hero bleibt Titel + sichtbarer Kurztext.
- zweiter sichtbarer Lead darunter entfernt.
- Zusatztext jetzt standardmäßig geschlossen:
  **„Mehr über <Welt> erfahren“**.
- voller Text bleibt im initialen HTML.
- `Was du hier findest` liegt innerhalb des Aufklappbereichs.

### Unterkategorie-Bilder
Gestalten:
- 7/7 eigene unterschiedliche Fallbackbilder;
- jeweils 600×320 WEBP;
- passend zu den 7 direkten Unterkategorien.

Priorität:
1. echtes Child-Featured-Image;
2. bei Gestalten passendes eigenes Fallbackasset;
3. sonst keine Fotokante.

Der alte generische Parent-Weltbild-Fallback wurde entfernt. Damit kann nicht mehr siebenmal dieselbe Person/dasselbe Weltbild erscheinen.

### Verkaufbare Werbung
- exakt **1 Foto**;
- eigenes Ad-Asset 1400×420;
- Text liegt über dem Foto;
- Headline `Hier könnte Ihre Werbung stehen.`;
- hinter der Headline auffälliger heller CSS-Pinselstrich;
- CTA `Werbemöglichkeiten & Preise`;
- Position weiter direkt nach den Unterkategorien.

## Kandidat

`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.616_HOBBY_DEPOT_HUB_CLEANUP_AD_BRUSH_NAV_FIX_LOCALPASS.zip`

SHA-256:
`6ae738653de1dd1677bc4e6a5e58540cc7efddc6ccd5ddf8f28a2b5bbda5e0cd`

Library:
`/hobby rausch/AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.616_HOBBY_DEPOT_HUB_CLEANUP_AD_BRUSH_NAV_FIX_LOCALPASS.zip`

## Lokaler Hardtest

PASS:
- ZIP-Integrität;
- PHP **10/10**;
- 7/7 Gestalten-Bilder vorhanden;
- 7/7 unterschiedliche SHA-256;
- 7/7 exakt 600×320;
- Direktwerbebild exakt 1400×420;
- Direktwerbung genau 1 `<img>`;
- generischer Parent-Weltbild-Fallback entfernt;
- Hub1-Zusatztext geschlossen statt doppelt offen;
- Brushstroke-CSS vorhanden;
- Breakpoint 1560 vorhanden;
- Nav-Offset 8 px;
- relevante Schriftgrößen gegen 1.50.614 unverändert.

## Erster offener Blocker

**WordPress-Live-Abnahme von 1.50.616.**

## EXAKT EINE NEXT ACTION

**1.50.616 installieren und Gestalten bei voller Desktopbreite, Side-by-Side-Breite und Mobile live prüfen.**
