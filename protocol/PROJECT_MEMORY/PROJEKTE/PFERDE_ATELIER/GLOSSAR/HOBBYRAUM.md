# GLOSSAR – HOBBYRAUM

STAND: 2026-09-13
STATUS: AKTIV / 0.2.6 TECHNISCH HARDTEST PASS / LIVE-READBACK OFFEN

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**  
Der einzige aktuelle Arbeitsraum des Büros GLOSSAR.

**HIER BIST DU RICHTIG, WENN …**  
die Pferde-Atelier-Anwendung des allgemeinen Glossar-Cores vorbereitet, technisch geprüft oder real zurückgelesen wird.

**DU DARFST …**  
die Pferde-Konfiguration prüfen, Fachquellen aus der Wissensdatenbank binden und den allgemeinen Glossar-Core isoliert bzw. über den gebundenen WordPress-Updateweg testen.

**DU DARFST NICHT …**  
`main` verändern, eine zweite Glossar-Faktendatenbank bauen, normale Beiträge/Seiten pro Begriff erzwingen, Pferde-Fachlogik in den allgemeinen Core schreiben, das bestehende Designplugin umbauen, den getesteten 0.2.6-ZIP nachträglich verändern oder vor realem Readback einen Pferde-LIVE-PASS behaupten.

**ALS NÄCHSTES …**  
exakt den hashgebundenen 0.2.6-Kandidaten über den geprüften WordPress-Updateweg installieren und sofort die vier gemeldeten Frontendfehler plus negative Regressionen real prüfen.

## AKTUELLER AUFTRAG

Keine neue Funktion bauen.

Der technische Kandidat ist hart geprüft. Jetzt ausschließlich reale Pferde-Atelier-Abnahme des exakt geprüften Pakets.

## ARBEITSORT

Isolierter Glossar-Branch:
`hobbyroom/glossar-026-upgrade-hardtest-20260913`

Technisch getesteter Commit:
`e5f8c8ce1839a69f3e6fb712bd4a3d4a3e8ad059`

Autoritativer Run:
`34748541630`

`main` bleibt unangetastet.

## GEBUNDENER KANDIDAT

Plugin:
`Universal Glossary Engine 0.2.6`

Rewrite-Schema:
`5`

Innerer Plugin-ZIP SHA-256:
`e0717db3aa247edc30b0fe84a261aa59037050d593e3432a6fb460f6d96f3b09`

Actions-Artefakt-ID:
`10314822840`

Technisches Testprotokoll:
`../../../ALLGEMEINGUELTIGE_BAUSTEINE/GLOSSAR/TESTPROTOKOLL_0.2.6_20260913.md`

Fehlerquelle Pferde-Anwendung:
`FEHLERQUELLEN.md`

## HARTER PRÜFSTAND

Fresh-Install Job `103700782149` → PASS.

Echter WordPress-In-place-Updateweg Job `103700782306` → PASS.

Gated Package Job `103700913568` → PASS.

Lokaler Check des exakt erzeugten Actions-Artefakts → PASS.

Positiv/negativ belegt:
- Version 0.2.6 / Schema 5;
- echte Einzelbegriffsseiten statt nur HTTP 200;
- absichtlich defekte 0.2.5-Rewrite-Regel ergibt 404;
- echter WordPress-Updater 0.2.5 → 0.2.6;
- erster neuer Request migriert Schema 4 → 5 und repariert Route;
- unbekannter Begriff 404;
- Entwurf 404;
- Legacy-URL 301;
- Kategorie und gleichnamiger Begriff getrennt;
- AJAX ungültiger Nonce negativ;
- normale Beiträge unverändert;
- Daten/Konfiguration bleiben erhalten;
- Deaktivieren/Reaktivieren ohne Routingverlust;
- Hero-Abstand;
- responsive Hero-Darstellung;
- Breadcrumb-Achse;
- komplette alte Regressionen nach Upgrade erneut PASS;
- lokales ZIP/Hash/Delta/PHP-Lint positiv und negativ PASS.

## DIE VIER REAL ZU PRÜFENDEN PUNKTE

1. Abstand vom Hero nach oben.
2. Hero-Bild responsive auf schmalem Bildschirm.
3. Links auf alle Einzelbegriffe: Seite darf nicht weiß sein; echter Titel und Inhalt müssen sichtbar sein.
4. Kategorie-Breadcrumb: Position und Darstellung gemäß Pferde-Atelier-Standard.

## NEGATIV-READBACK IM PFERDE ATELIER

Zusätzlich zwingend nach Installation:
- nicht vorhandener Glossarbegriff bleibt 404;
- Entwurf bleibt öffentlich nicht erreichbar;
- normale WordPress-Beiträge bleiben unverändert;
- Glossar-Kategorie und gleichnamiger Einzelbegriff bleiben getrennt;
- keine zweite Breadcrumb-Ausgabe;
- keine globale Layoutverschiebung außerhalb Glossar.

## INSTALLATIONSWEG

Nur der bereits hart geprüfte Weg:
WordPress-Pluginupdate/Überschreiben von vorhandener 0.2.5 mit dem exakt hashgebundenen 0.2.6-ZIP.

Nicht:
- Dateien manuell einzeln austauschen;
- anderes 0.2.6-Paket bauen;
- erneut 0.2.5 unter verändertem Inhalt verwenden.

## RÜCKGABELOGIK

Bei realem PASS:
- `FEHLERQUELLEN.md` auf LIVE PASS/CLOSED aktualisieren, soweit tatsächlich bewiesen;
- `CURRENT_STATE.md` auf neuen realen Stand ziehen;
- erst dann weitere Integrationsarbeit.

Bei realem FAIL:
- exakt ersten Fehler dokumentieren;
- Kandidat bleibt BLOCKED;
- kein neues Plugin ausgeben, bevor minimaler Fix wieder Fresh + In-place + Positiv/Negativ + lokaler ZIP-Kontrolle bestanden hat.

## DANACH OFFEN

Erst nach realem Pferde-Readback:
- aktueller Astra+Yoast-Kombinationstest, soweit für endgültigen Release gebunden;
- realer Campus-Wissensdatenbankimport;
- größerer Bestand/Performance;
- separates zweites reales Portal.

## HARTE REGEL

**Technischer Hardtest-PASS ist noch kein Pferde-Atelier-LIVE-PASS.**

Keine weitere Codeänderung vor dem realen Readback.

## VERWEISE

- Bürostand: `CURRENT_STATE.md`
- Bürotür: `START_HERE.md`
- Fehler: `FEHLERQUELLEN.md`
- Seitenkonzept: `SEITENKONZEPT_V1.md`
- Allgemeiner Core: `../../../ALLGEMEINGUELTIGE_BAUSTEINE/GLOSSAR/START_HERE.md`
- Testprotokoll: `../../../ALLGEMEINGUELTIGE_BAUSTEINE/GLOSSAR/TESTPROTOKOLL_0.2.6_20260913.md`
- Dauerhafte Entscheidung: `../../../ALLGEMEINGUELTIGE_BAUSTEINE/GLOSSAR/ENTSCHEIDUNG_20260912.md`
- Fachdatenbank: `../WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/START_HERE.md`
- DESIGN: `../DESIGN/START_HERE.md`
- TEXT/SEO: `../TEXT/START_HERE.md`
- Zentrales Fehlerregister: `protocol/PROJECT_MEMORY/FEHLERREGISTER.md`
