# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-11
STATUS: **1.50.617 LOCAL HARD PASS / LIVE OFFEN**

## Aktueller Kandidat
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.617_HOBBY_DEPOT_HUB_GRID_NAV_AFFILIATE_INTEGRATED_LOCALPASS.zip`

SHA-256:
`5f6e5ddf30662a10ecdfc37b35aaca82ad0ba578d59cde20b463d11314624764`

Library:
`/hobby rausch/AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.617_HOBBY_DEPOT_HUB_GRID_NAV_AFFILIATE_INTEGRATED_LOCALPASS.zip`

## 1.50.617

Header:
- Logo Desktop 286 px / mittlere Breite 278 px / Mobile 230 px im lokalen Readback;
- >1180 px Navigation 8×1;
- 761–1180 px Navigation sichtbar 4×2;
- <761 px Hamburger;
- kein horizontaler Overflow;
- 18 px Abstand Headerende → Breadcrumb bei Desktop/Mid.

Hub1:
- Hero bleibt;
- Zusatztext standardmäßig geschlossen;
- Aufklappbereich volle Inhaltsbreite;
- transparenter/weißer Hintergrund;
- echte Absatzstruktur;
- `Was du hier findest` ohne eigene Farbbox.

Gestalten-Karten:
- 7/7 unterschiedliche Bilder;
- alle 600×320;
- alle lokal als 1,88:1 gerendert;
- Desktop-Raster bei 7 = **3 + 2 + 2**;
- Druck & Fotografie besitzt wieder ein Bild;
- echter Child-Featured-Image-Pfad bleibt vorrangig.

Affiliate:
- Banner + Produkte innerhalb `Nächste Ebene` integriert;
- keine separaten Standalone-Produkt-/Bannerblöcke danach;
- öffentlich leer unsichtbar / eingeloggt leer sichtbar unverändert.

Direktwerbung:
- ein Foto als Hintergrund;
- Brush-Headline;
- heller CTA;
- direkt nach dem Kategorie-/Partnerbereich.

Typografie:
- Navigation 14 px;
- Hub-Intro 16 px;
- Unterkategorie-Titel 15 px;
- Unterkategorie-Text 11 px;
- keine globale Verkleinerung.

## Lokaler Hardtest
- PHP **10/10 PASS**
- ZIP PASS
- Desktop 1600 PASS
- Mid 1024 PASS
- Mobile 390 PASS
- horizontal overflow = 0 PASS
- Nav sichtbar Mid PASS
- Logo lesbar Mid PASS
- Header/Breadcrumb Abstand PASS
- 7 unique Fotos PASS
- 7 Querformate PASS
- 3/2/2-Raster PASS
- Intro-Absätze PASS
- Intro-Hintergrund transparent PASS
- Affiliate integriert PASS
- Direktwerbung Einzelbild/Brush/heller Button PASS

## Erster offener Blocker
**WordPress-Live-Abnahme von 1.50.617.**

## EXAKT EINE NEXT ACTION
**1.50.617 installieren und Gestalten bei normaler Breite, Side-by-Side und Mobile live prüfen.**
