# HD-003 – HOBBY DEPOT DESIGN / TEMPLATE KIT – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-18
STATUS: **1.50.684 HERO-VISUELL FAIL / 1.50.685 GEBAUT / KERAMIK-&-GLAS PFLICHTTEST + RELEASEKETTE PASS / WORDPRESS-READBACK OFFEN**

## Kandidat

`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.685_HERO_SCENE_VISIBILITY_FIX.zip`

SHA-256:
`a72b7baa257b09d3fc2f4112bdcb25e03bdbe8d6d120ae0d60764ee53f6c7b1e`

## Scope

Nur Hub2-Hero:
- Masterbilder unverändert;
- Bildfeld 72 % statt 70 %;
- Übergangsüberdeckung stark reduziert;
- Szene horizontal erhalten;
- nur vertikaler Crop;
- kein Upscaling;
- Mobil gleicher Masterausschnitt.

## QA

- PHP 99/99 PASS;
- Front-/Contentroute V150685 PASS;
- beide Templates positiv PASS;
- Negativtest gegen V150684 erwartungsgemäß FAIL;
- 69/69 Hub2-Render PASS;
- 276/276 Desktop-Geometriechecks PASS;
- 49/49 Browserfälle PASS;
- Keramik & Glas explizit 1440/1180/1024/901/900/760/390 PASS;
- ZIP PASS;
- Roundtrip 1139/1139 PASS;
- Delta: 1 geändert / 3 neu / 0 entfernt.

## EXAKT EINE NEXT ACTION

**1.50.685 installieren und Keramik & Glas real abnehmen.**
