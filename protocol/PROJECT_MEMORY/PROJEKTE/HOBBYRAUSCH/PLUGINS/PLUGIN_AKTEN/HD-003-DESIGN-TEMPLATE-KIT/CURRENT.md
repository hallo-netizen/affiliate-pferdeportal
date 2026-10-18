# HD-003 – HOBBY DEPOT DESIGN / TEMPLATE KIT – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-18
STATUS: **LIVE 1.50.677 / 1.50.678 GEBAUT / VISUELLE E2E-PRÜFUNG OFFEN / KEIN RELEASE-PASS**

## Kandidat

AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.678_HOBBY_DEPOT_DYNAMIC_TEXTSAFE_HERO_HARDPASS.zip

SHA-256:
33e35ef638c3564b03343deda6d420f20a85bb387949d017cc75f1d2d9f629f5

## Scope

Nur Audio & HiFi im aktuellen Pilot:
- Beige-/Textbereich dynamisch nach Schriftblockbreite;
- Desktop H1 ohne Umbruch;
- Kurzzeile ohne Umbruch;
- Schriftblock ca. 10 px höher;
- Bild bleibt fullbleed und nutzt automatisch den verbleibenden Raum.

Keine anderen Kategorien geändert.
Keine Bilddatei geändert.

## Performance

- CSS-only;
- kein JS;
- keine DOM-Laufzeitmessung;
- kein Zusatzrequest;
- keine neue Datenabfrage.

## QA

Code/Paket:
- PHP 81/81 PASS;
- Release-Kette PASS;
- 901 Assets unverändert;
- Plugin-Wurzel korrekt;
- ZIP PASS;
- Roundtrip 1050/1050.

## OFFENER TESTBLOCKER

Die vorhandene lokale Visual-Simulation ist nicht als Hard-PASS verwertbar:
- Claim im Testbild angeschnitten;
- Hero-Bild im Harness nicht geladen;
- Positiv-/Negativ-E2E des realen Renderpfads nicht vollständig dokumentiert.

## EXAKT EINE NEXT ACTION

**1.50.678 vollständig lokal mit real geladenem Hero-Bild positiv/negativ simulieren. Vorher kein Upload in WordPress.**
