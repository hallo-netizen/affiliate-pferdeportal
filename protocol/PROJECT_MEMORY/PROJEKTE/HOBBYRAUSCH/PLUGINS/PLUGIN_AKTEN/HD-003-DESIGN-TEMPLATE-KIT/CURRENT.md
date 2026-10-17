# HD-003 – HOBBY DEPOT DESIGN / TEMPLATE KIT – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-17
STATUS: **1.50.671 LIVE FATAL / 1.50.672 RELEASE-CHAIN-FIX LOCAL HARD PASS / LIVE OFFEN**

## Fehler 1.50.671

Exakt AF-026 wiederholt:
- geladen: Hobby_Depot_Profile_V150671;
- geroutet: Templates v150670;
- Template-Aufruf: Hobby_Depot_Profile_V150670;
- Klasse nicht vorhanden;
- Frontend-Fatal reproduziert.

## Einziger Kandidat

AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.672_HOBBY_DEPOT_RELEASE_CHAIN_FATAL_FIX_HARDPASS.zip
SHA-256: f66e0cb03301dfd8658aeb7de4ebcff059bceb9da0760b048e9be6fa40d8c78d

## Korrektur

Nur Release-Kette:
- Main 1.50.672;
- Profilklasse 1.50.672;
- Profil-RELEASE 1.50.672;
- Fronttemplate 1.50.672;
- Contenttemplate 1.50.672;
- aktive Referenzen konsistent.

Keine Bild-/Mega-Änderung gegenüber 1.50.671.

## Harte QA

- AF-026 7/7 PASS;
- 1.50.671 negativer Fatal 1:1 reproduziert;
- 1.50.672 Fronttemplate ausgeführt PASS;
- 1.50.672 Contenttemplate ausgeführt PASS;
- Dirty-Overlay 1.50.671 -> 1.50.672 PASS;
- PHP 63/63;
- 901/901 Assets byte-identisch zu 1.50.671;
- ZIP PASS;
- Roundtrip 1031/1031 identisch.

## EXAKT EINE NEXT ACTION

**1.50.672 installieren und zuerst den kritischen Frontend-Fehler prüfen.**
