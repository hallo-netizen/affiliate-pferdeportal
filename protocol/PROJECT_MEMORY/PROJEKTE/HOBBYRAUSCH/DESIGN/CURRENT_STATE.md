# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-17
STATUS: **1.50.671 LIVE FATAL / URSACHE EXAKT REPRODUZIERT / 1.50.672 RELEASE-CHAIN-FIX LOCAL HARD PASS / LIVE-PRÜFUNG OFFEN**

## Exakter Fehler 1.50.671

- Main-Plugin lud Hobby_Depot_Profile_V150671.
- Das Profil routete auf hobby-depot-front-v150670.php und hobby-depot-content-v150670.php.
- Beide Templates riefen Hobby_Depot_Profile_V150670 auf.
- Diese Klasse war im 1.50.671-Paket nicht vorhanden.
- Reproduzierter Fatal: Class "Hobby_Depot_Profile_V150670" not found.

Das ist exakt die Wiederholung von AF-026.

## 1.50.672

Nur die Release-Kette wurde korrigiert:
- Plugin-Header/Version 1.50.672;
- aktives Profil V150672;
- Profil-RELEASE 1.50.672;
- Front- und Contenttemplate v150672;
- beide Templates rufen nur Hobby_Depot_Profile_V150672 auf;
- keine aktive Stale-Referenz auf 1.50.670 oder 1.50.671.

**Bilder und Mega-Menü sind gegenüber 1.50.671 byte-identisch.**

## Harte Simulation

Negativ 1.50.671:
- Fronttemplate: Fatal exakt reproduziert;
- Contenttemplate: Fatal exakt reproduziert.

Positiv 1.50.672:
- Hauptplugin lädt;
- Profilklasse lädt;
- Front-Route zeigt auf 1.50.672;
- Fronttemplate ausgeführt: PASS;
- Contenttemplate ausgeführt: PASS;
- Dirty-Overlay 1.50.671 -> 1.50.672: beide Templates PASS.

AF-026 Release-Chain-Gate: 7/7 PASS.

## Paket-QA

Artefakt: AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.672_HOBBY_DEPOT_RELEASE_CHAIN_FATAL_FIX_HARDPASS.zip
SHA-256: f66e0cb03301dfd8658aeb7de4ebcff059bceb9da0760b048e9be6fa40d8c78d

- PHP 63/63 PASS;
- Assets gegenüber 1.50.671: 901/901 byte-identisch;
- Asset-Diffs: 0;
- gleicher Pluginordner affiliate-portal-template-kit;
- gleiche Main-Datei pferde-template-kit.php;
- ZIP-Test PASS;
- Roundtrip 1031/1031 byte-identisch.

## Bild-/Mega-Scope

Unverändert zu 1.50.671:
- Hero-Master 1600×853;
- Preview 600×320 daraus abgeleitet;
- keine Collagen;
- nur die bereits freigegebenen 19 Bildbereiche;
- alle anderen Kategorien unangetastet;
- Mega-Menü bis 10 Bereiche direkt in zwei Reihen.

## EXAKT EINE NEXT ACTION

**1.50.672 über 1.50.671 installieren und zuerst nur eine normale Hobby-Depot-Seite im Frontend öffnen. Wenn kein kritischer Fehler erscheint, anschließend die bereits benannten Bildbereiche prüfen.**
