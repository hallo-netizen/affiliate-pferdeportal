# HD-003 – HOBBY DEPOT DESIGN / TEMPLATE KIT – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-18
STATUS: **1.50.679 LIVE-VERSUCH FATAL / 1.50.680 RELEASEKETTEN-FIX GEBAUT / LOKAL POSITIV+NEGATIV PASS / WORDPRESS-READBACK OFFEN**

## Kandidat

`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.680_HOBBY_DEPOT_RELEASE_CHAIN_FATAL_FIX.zip`

SHA-256:
`ed34fece94970fc5be1ddd9c4116f1cb5029360a99515484a2656f19b307b40a`

## Fehler 1.50.679

Aktive 1.50.679-Profilklasse routete noch auf die 1.50.678-Templates. Diese riefen die 1.50.678-Profilklasse auf. Dadurch entstand der reale WordPress-Fatal.

## Fix 1.50.680

Nur die Versionskette repariert:
- Main 1.50.680;
- Profilklasse V150680;
- Route Front → Template V150680;
- Route Content → Template V150680;
- beide Templates rufen ausschließlich Profilklasse V150680.

Unverändert:
- 69 Hub2-Texte;
- Hero-/Fullbleed-Logik;
- 901 Bildassets;
- Mega-Menü;
- Kategoriebaum.

## QA

- PHP 87/87 PASS;
- ZIP PASS;
- Front-Route real PASS;
- Content-Route real PASS;
- Fronttemplate real mit V150680 PASS;
- Contenttemplate real mit V150680 PASS;
- Negativtest mit ausschließlich V150679 scheitert an V150680 wie erwartet;
- Delta zu 1.50.679: 1 Datei geändert, 3 Dateien neu, 0 entfernt;
- 901/901 Bildassets identisch.

## EXAKT EINE NEXT ACTION

**1.50.680 installieren und realen WordPress-Frontend-Readback durchführen.**
