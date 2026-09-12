# GLOSSAR – HOBBYRAUM

STAND: 2026-09-12
STATUS: AKTIV

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**  
Der einzige aktuelle Arbeitsraum des Büros GLOSSAR.

**HIER BIST DU RICHTIG, WENN …**  
die öffentliche Glossarstruktur, das WordPress-Backend oder die Glossar-Ausgabe im bestehenden Pferde-Atelier-Design vorbereitet oder geprüft wird.

**DU DARFST …**  
den aktuellen Design-/WordPress-Bestand lesen, die kleinstmögliche Glossar-Erweiterung definieren und isoliert auf diesem Hobbyraum-Branch vorbereiten.

**DU DARFST NICHT …**  
`main` verändern, eine zweite Glossar-Faktendatenbank bauen, normale Beiträge/Seiten pro Begriff erzwingen, ungeprüft in DESIGN/TEXT/AFFILIATE schreiben oder vor Positiv-/Negativprüfung ein Plugin ausgeben.

**ALS NÄCHSTES …**  
`CURRENT_STATE.md` lesen → relevanten DESIGN-/WordPress-Bestand frisch prüfen → kleinste Backend-/Frontend-Erweiterung festlegen.

## AKTUELLER AUFTRAG

Das neue Büro GLOSSAR vollständig einrichten und danach die technisch kleinste WordPress-Umsetzung vorbereiten.

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

## GEBUNDENE FACHGRENZEN

- Fachbegriffe/Fakten/Quellen: `../WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/`
- Darstellung/Designplugin: `../DESIGN/`
- SEO-/Kannibalisierungsregeln bei Bedarf: `../TEXT/`
- Glossarbüro: öffentliche Struktur, Kurzfassung, SEO-Felder, WordPress-Konzept und Abnahme.

## SEO-ENTSCHEIDUNG

Gewünschter KISS-Weg:
- eigener SEO-Titel je Glossarbegriff;
- eigene Meta-Description je Glossarbegriff;
- Erzeugung nach festem Glossar-Schema;
- keine manuelle Yoast-Pflege pro Begriff;
- keine direkten Writes in Yoast-interne Datenbankfelder;
- vorhandene Yoast-Ausgabe soll nur über offiziell vorgesehene Schnittstellen überschrieben werden, sofern die installierte Yoast-Version dies nach frischer Prüfung unterstützt.

Die konkrete technische Bindung ist vor Umsetzung gegen den installierten Bestand zu prüfen.

## NEXT ACTION

1. aktuellen DESIGN-Stand und vorhandenes Designplugin lesen;
2. vorhandene Kategorietext-Speicherung/-Ausgabe prüfen;
3. daraus die kleinstmögliche Glossar-Backendstruktur ableiten;
4. separat Frontend-Ausgabe definieren: Glossar-Start → Oberbegriffe → aufklappbare Begriffe, kein Bildzwang;
5. Positiv-/Negativtests festlegen;
6. erst danach technischen Kandidaten bauen.

## HARTE REGEL

**Noch kein Plugin ausgeben.**

Erst Bestand prüfen, dann genau einen KISS-Kandidaten. Keine Plugin-Serie.

## RÜCKGABEWEG

Bei belastbarer Architektur:
- `CURRENT_STATE.md` nachziehen;
- betroffene Nachbarbüros nur über klaren Integrationsauftrag anfassen;
- technischer Kandidat bleibt isoliert bis Positiv-/Negativprüfung.

Bei Konflikt mit bestehendem Designplugin:
- STOP;
- keine Ersatzarchitektur erfinden;
- kleinsten Konflikt gegen DESIGN-Originalquellen klären.

## VERWEISE

- Bürostand: `CURRENT_STATE.md`
- Bürotür: `START_HERE.md`
- Fachdatenbank: `../WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/START_HERE.md`
- DESIGN: `../DESIGN/START_HERE.md`
- TEXT/SEO: `../TEXT/START_HERE.md`
- Fehler: `protocol/PROJECT_MEMORY/FEHLERREGISTER.md`
- Warum: `protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md`
- Ziel: `protocol/PROJECT_MEMORY/ZIELVERTRAEGE/REGISTER.md`
