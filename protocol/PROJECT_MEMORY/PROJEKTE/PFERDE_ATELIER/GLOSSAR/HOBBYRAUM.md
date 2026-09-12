# GLOSSAR – HOBBYRAUM

STAND: 2026-09-12
STATUS: AKTIV / UNIVERSAL-CORE-KONZEPT

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**  
Der einzige aktuelle Arbeitsraum des Büros GLOSSAR.

**HIER BIST DU RICHTIG, WENN …**  
die Pferde-Atelier-Anwendung des allgemeinen Glossar-Cores vorbereitet oder geprüft wird.

**DU DARFST …**  
die Pferde-Konfiguration definieren, Fachquellen aus der Wissensdatenbank binden und den allgemeinen Glossar-Core isoliert gegen das Pferde-Atelier testen.

**DU DARFST NICHT …**  
`main` verändern, eine zweite Glossar-Faktendatenbank bauen, normale Beiträge/Seiten pro Begriff erzwingen, Pferde-Fachlogik in den allgemeinen Core schreiben, das bestehende Designplugin zur Glossar-Engine umbauen oder vor Positiv-/Negativprüfung ein Plugin ausgeben.

**ALS NÄCHSTES …**  
allgemeinen Core-Vertrag lesen → Pferde-Konfiguration festlegen → V1-Prototyp isoliert bauen und testen.

## AKTUELLER AUFTRAG

Das Pferde Atelier als erste reale Anwendung von `MOD-008 – Universal Glossar Engine` vorbereiten.

Bestätigter Live-Ausgangspunkt:
- WordPress-Seite `Glossar` ist vom Nutzer angelegt;
- sie ist bereits verlinkt;
- keine weiteren WordPress-Seiten pro Glossarbegriff anlegen.

## ARBEITSORT

Campus-Basis:
`hobbyroom/project-memory-campus-v1-20260905`

Isolierter Glossar-Hobbyraum-Branch:
`hobbyroom/glossar-office-20260912-v2`

`main` bleibt unangetastet.

## ALLGEMEINER CORE

Autorität:
`../../ALLGEMEINGUELTIGE_BAUSTEINE/GLOSSAR/START_HERE.md`
→ `CURRENT_STATE.md`
→ `HOBBYRAUM.md`

Kern bleibt neutral.

## PFERDE-KONFIGURATION

Nur hier bzw. in einer späteren separaten Projektkonfigurationsdatei:
- Glossar-Hauptseite;
- URL-Basis;
- Pferde-Oberbegriffe;
- SEO-Titel-Schema;
- Meta-Description-Schema;
- Text-/Pflichtfeldregeln;
- Designklassen;
- Importquelle Wissensdatenbank.

## GEBUNDENE FACHGRENZEN

- Fachbegriffe/Fakten/Quellen: `../WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/`
- Darstellung: Glossar-Core + projektspezifische Designklassen; bestehendes DESIGN-Plugin bleibt unangetastet
- SEO-/Kannibalisierungsregeln bei Bedarf: `../TEXT/`
- Glossarbüro: öffentliche Struktur, Kurzfassung, SEO-Schema, Pferde-Konfiguration und Abnahme.

## SEO-ENTSCHEIDUNG

- eigener SEO-Titel je Glossarbegriff;
- eigene Meta-Description je Glossarbegriff;
- Erzeugung nach festem Pferde-Glossar-Schema;
- keine manuelle Yoast-Pflege pro Begriff;
- keine direkten Writes in Yoast-interne Datenbankfelder;
- Core funktioniert auch ohne Yoast;
- bei aktivem Yoast nur offizielle Filter/Schnittstellen verwenden;
- keine doppelten Meta-Tags.

## NEXT ACTION

1. V1-Datenvertrag des allgemeinen Core technisch festlegen;
2. Pferde-Konfiguration als separate Konfigurationsschicht definieren;
3. neutralen Zweitportal-Testdatensatz definieren;
4. V1-Prototyp isoliert bauen;
5. positiv/negativ prüfen;
6. erst bei Gesamt-PASS einen installierbaren Kandidaten erzeugen.

## PARALLELENTWICKLUNG

Aktuell NICHT erforderlich.

Wenn der Zweitportaltest eine echte unkonfigurierbare Projektspezifik beweist:
Core beibehalten + kleiner Projektadapter.
Kein zweiter vollständiger Plugin-Fork.

## HARTE REGEL

**Noch kein Plugin ausgeben.**

Erst Core + Pferde-Konfiguration + neutrale Zweitkonfiguration testen. Keine Plugin-Serie.

## RÜCKGABEWEG

Bei PASS:
- Projekt-CURRENT_STATE nachziehen;
- MOD-008-Prüfgrad nachziehen;
- erst dann einen einzigen installierbaren Kandidaten bereitstellen.

Bei FAIL:
- erster echter Fehler;
- kein Parallelplugin;
- kleinster KISS-Fix;
- komplette Positiv-/Negativprüfung wiederholen.

## VERWEISE

- Bürostand: `CURRENT_STATE.md`
- Bürotür: `START_HERE.md`
- Allgemeiner Core: `../../ALLGEMEINGUELTIGE_BAUSTEINE/GLOSSAR/START_HERE.md`
- Fachdatenbank: `../WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/START_HERE.md`
- DESIGN: `../DESIGN/START_HERE.md`
- TEXT/SEO: `../TEXT/START_HERE.md`
- Fehler: `protocol/PROJECT_MEMORY/FEHLERREGISTER.md`
- Warum: `protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md`
- Ziel: `protocol/PROJECT_MEMORY/ZIELVERTRAEGE/REGISTER.md`
