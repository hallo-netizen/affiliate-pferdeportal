# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-12
STATUS: **1.50.638 LOCAL HARD PASS / WORDPRESS-LIVE PILOT BUCH & PAPIER OFFEN**

## Kandidat
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.638_HOBBY_DEPOT_BUCH_PAPIER_PILOT_PHOTO_PRODUCT_FIRST_LOCALPASS.zip`

SHA-256:
`44f32edd6158b5b82452c837ffe1534008b6cbfb50e7c7da6fcd72da319e0f7a`

Library:
`/hobby rausch/AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.638_HOBBY_DEPOT_BUCH_PAPIER_PILOT_PHOTO_PRODUCT_FIRST_LOCALPASS.zip`

## Pilot-Scope
**Ausschließlich Hub2 `Buch & Papier`.**

Änderungen:
- Claim: `Papier kann mehr.`;
- 5 Unterkategorie-Karten mit klaren kleinen Fotos statt Icons;
- 2-spaltiges Kartenraster Desktop, 1-spaltig unter 1000 px;
- kurze individuelle Unterzeilen;
- Produkte direkt nach den Unterkategorien;
- danach genau 3 größere Beitragskarten;
- danach Affiliate-Banner;
- danach genau ein verkaufbarer Werbeplatz;
- **kein Seitenendtext** auf diesem Pilot-Hub2.

## Neue Pilotbilder
- Buchbinden;
- Marmorpapier;
- Papierherstellung;
- Stempel schnitzen;
- Zines herstellen.

Alle:
- 600×320 WebP;
- klare Einzelmotive;
- zusammen nur **66.054 Bytes**;
- lazy loading im Kartenpfad.

## Freeze / unverändert
- alle bereits vorhandenen Assets aus 1.50.637 byteidentisch;
- nur 5 neue Pilotbilder ergänzt;
- Header/Nav unverändert;
- Hero-Dateien unverändert;
- Ebene 1 unverändert;
- alle anderen Hub2-Seiten bleiben auf der 1.50.637-Logik;
- keine Taxonomie-/Architekturänderung;
- Affiliate-Slots unverändert (`category_product_1..3`, `hub_after_cards`).

## Lokal geprüft / simuliert
- PHP **28/28 PASS**;
- ZIP-Integrität PASS;
- aktive V150638-Klasse/Templates PASS;
- Pilot-Gate ausschließlich `buch-papier`;
- 1440 / 1024 / 760:
  - horizontaler Overflow 0;
  - Reihenfolge: Kategorien → Produkte → Beiträge → Banner → Werbeplatz;
  - kein Seitenendtext;
  - alle 8 simulierten Bilder geladen;
- 5/5 Pilotbilder 600×320;
- bestehende Asset-Dateien geändert: **0**.

## EXAKT EINE NEXT ACTION
**1.50.638 installieren und live ausschließlich `Fertigen → Buch & Papier` prüfen. Erst nach Live-PASS Entscheidung über Rollout auf weitere Hub2-Seiten.**
