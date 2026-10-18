# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-18
STATUS: **LIVE 1.50.677 / DYNAMISCHER TEXTSICHERER HERO 1.50.678 LOCAL HARD PASS / LIVE OFFEN**

Zielvertrag: **ZV-HOBBYRAUSCH-DESIGN-001 Fassung 4.6 / 2026-10-18**

## Reales Live-Ergebnis 1.50.677

- Bildanteil mit starrem 3/4-Ziel zu aggressiv;
- H1 konnte bei breitem Fenster umbrechen;
- Textblock soll als Ganzes etwas höher;
- Kurzzeile bleibt einzeilig;
- Beige-Bereich soll sich sinnvoll an die tatsächliche Textbreite anpassen statt überall starr gleich breit zu sein.

## 1.50.678 – zentrale dynamische Fullbleed-Regel

Performance:
- reine CSS-Lösung;
- kein JavaScript;
- keine Laufzeitmessung;
- kein zusätzlicher Bildrequest;
- keine neue Datenbank-/Frontend-Abfrage.

Mechanik:
- bestehendes Hero-Bild bleibt fullbleed über 100 %;
- Beige-/Textbereich folgt der tatsächlichen Breite des Schriftblocks;
- auf Desktop min. 35 %, max. 48 %;
- bei 901–1180 px min. 42 %, max. 58 %;
- der Übergang ins Bild hängt als reiner CSS-Verlauf direkt an diesem dynamischen Textbereich;
- H1, Claim und Kurzzeile bleiben auf Desktop nowrap;
- kompletter Schriftblock ca. 10 px höher über angepasste Innenabstände;
- <=900 px bleibt die stabile gestapelte Variante.

Die zentrale Klasse ist weiterhin nur an Audio & HiFi gebunden, bis der Pilot live bestätigt ist.

Unverändert:
- 901/901 Assets;
- alle anderen Kategorien;
- Mega-Menü;
- Kategoriebaum;
- Audio-Langtext und Karten.

## QA

Artefakt:
AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.678_HOBBY_DEPOT_DYNAMIC_TEXTSAFE_HERO_HARDPASS.zip

SHA-256:
33e35ef638c3564b03343deda6d420f20a85bb387949d017cc75f1d2d9f629f5

PASS:
- PHP 81/81;
- aktive Release-Kette vollständig 1.50.678;
- keine aktive 1.50.677-Routen-/Klassenreferenz;
- H1 nowrap auf Desktop;
- Kurzzeile nowrap;
- dynamische Copy-Zone mit min/max Grenzen;
- 901/901 Assets identisch;
- WordPress-Pluginwurzel korrekt;
- ZIP-Test PASS;
- Roundtrip 1050/1050 byte-identisch.

## EXAKT EINE NEXT ACTION

**1.50.678 über 1.50.677 installieren und Audio & HiFi breit sowie halbbreit prüfen.**
