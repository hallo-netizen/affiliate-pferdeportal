# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-18
STATUS: **LIVE 1.50.677 / 1.50.678 GEBAUT / LOCAL-HARD-PASS ZURÜCKGEZOGEN / VISUELLE E2E-PRÜFUNG OFFEN / KEIN LIVE-UPLOAD**

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

PASS (nur Code/Paket):
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

## Abschluss-Nachprüfung des bisherigen Local-PASS

Die vorhandenen lokalen 1.50.678-Screenshots wurden erneut direkt geprüft.

Befund:
- Claim im Visual-Harness oben sichtbar angeschnitten;
- Hero-Bild im Harness nicht tatsächlich geladen/gerendert;
- damit wurde der reale Bild/Text-Übergang nicht belastbar visuell geprüft;
- dokumentierte lokale Positiv- UND Negativ-E2E-Prüfung des realen Pfads fehlt.

**1.50.678 ist deshalb noch kein freigegebener Upload-/Deploymentkandidat.**

## ERSTER OFFENER BLOCKER

Belastbare lokale visuelle E2E-Simulation mit tatsächlich geladenem Hero-Bild fehlt. Dabei ist zu klären, ob das angeschnittene Claim ein echter CSS-Fehler oder ein Harnessfehler ist.

## EXAKT EINE NEXT ACTION

**1.50.678 im echten lokalen Plugin-Renderweg mit geladenem Audio-Hero positiv und negativ simulieren; Claim, H1, Kurzsatz, dynamische Beigezone, Bildübergang und Responsive-Breiten prüfen. Erst bei vollständigem PASS darf die Installation in WordPress empfohlen werden.**

## NICHT ANFASSEN

- keine anderen Kategorien;
- keine neuen Bilder;
- Mega-Menü nicht erneut umbauen;
- Kategoriebaum nicht ändern;
- Audio-Langtext und Karten nicht erneut schreiben;
- keine neue Architektur.
