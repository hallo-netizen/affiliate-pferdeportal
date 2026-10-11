# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-11
STATUS: **1.50.621 LOCAL HARD PASS / WORDPRESS-LIVE OFFEN**

## Kandidat
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.621_HOBBY_DEPOT_HEADER_ALIGNMENT_LOCALPASS.zip`

SHA-256:
`a51f986d945ca87e85de4ff367c73ed3e09772e48b25bd5308ad53bcc72be226`

Library:
`/hobby rausch/AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.621_HOBBY_DEPOT_HEADER_ALIGNMENT_LOCALPASS.zip`

## Delta 1.50.621
Nur Header-Mikrofix, Rest von 1.50.620 bewusst unverändert.

- Logoasset byteidentisch zu 1.50.620.
- Halbkreis/dein, HOBBY DEPOT und Claim werden aus demselben Asset getrennt geclippt und mit mehr Abstand dargestellt.
- Suchfeld vertikal auf HOBBY-DEPOT-Wortmarkenlinie.
- Header insgesamt kompakter.
- Navigation auf die unterste Headerlinie gesetzt.
- alle 8 Navigationspunkte identische Höhe/Baseline; Sammeln ausdrücklich geprüft.
- Flyouts bleiben erhalten.

## Lokale Browser-Simulation
Playwright/Chromium mit gerendertem Plugin-Header:
- 1600 px: overflow 0; Header 191 px; alle 8 Navitems top/bottom 169/196.
- 1024 px: overflow 0; Header 191 px; alle 8 Navitems top/bottom 169/196.
- 960 px: overflow 0; 4×2-Navigation; Reihe 1 = 158/189, Reihe 2 inkl. Sammeln = 192/223.
- 800 px: wie 960, overflow 0.
- Flyout Pflanzen 1024 px: sichtbar und im Viewport.
- Flyout Sammeln 960 px: sichtbar und im Viewport.

## Fresh-Prüfung
- PHP 10/10 PASS.
- ZIP-Integrität PASS.
- Logo SHA unverändert: `c3e5b999fa9d84cbacf964d057e4cc7f519c51b17c6bc8a0fff0e3cebb14a171`.
- aktiver Renderer/Templates ausschließlich 1.50.621.

## EXAKT EINE NEXT ACTION
**1.50.621 installieren und nur den Header live prüfen.**
