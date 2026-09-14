# GLOSSAR – HOBBYRAUM

STAND: 2026-09-14
STATUS: **AKTIV**

## AKTUELLER AUFTRAG

Glossar-Plugin auf einen einfachen, kontrollierten JSON-Importweg umbauen – konzeptionell analog zum `Pferde Atelier – Pferderassen Manager 0.2.0`.

## VERBINDLICHER ARBEITSWEG

`WDB Glossar-Aktenschrank -> Chat erstellt fertige Glossarbeiträge nach Textregeln -> JSON-Batch -> Glossar-Importer validiert -> WordPress-Draft -> definierter Readback -> gesonderte Freigabe`

Fachautorität:
`../WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/`

## NICHT MEHR AKTIV

Die frühere autonome Produktionsstrecke
`PSTE Discovery -> Retained/Planning -> Research-Paket -> Cron/Loopback -> Auto-Publish`
ist **abgelöst**.

Core 1.3.5–1.3.8 bleibt technische Historie. Insbesondere ist **1.3.8 nicht mehr NEXT ACTION** und wird nicht weiter zum Produktionssystem ausgebaut.

## NEXT ACTION

1. bestehenden Glossar-Core gegen den Pferderassen-Manager-0.2.0-Vertrag vergleichen;
2. kleinsten Umbau auf JSON-Importer definieren;
3. festen versionierten Batchvertrag festlegen – keine Feldnamen/Batchgrenze raten, sondern gegen WDB + bestehende `uge_term`-Felder binden;
4. gültige `term-*`-WDB-ID erzwingen;
5. Textregeln erzwingen: 150–200 Wörter, keine H2/H3, 0 Bodylinks;
6. Relations- und Portalzielbindung prüfen;
7. Write nur als Draft;
8. definierte WordPress-Felder real readbacken;
9. Mismatch/Dublette/ungültige Relation fail-closed; erforderlichen Rollback testen;
10. normale Posts/Pages negativ gegen Veränderung testen;
11. exakte fertige ZIP positiv/negativ/regressiv testen;
12. erst danach echter WordPress-Import eines kleinen JSON-Testbatches.

## LIVE PASS – NICHT ANFASSEN

- Glossar-Einzelbegriffe öffnen;
- 0 Links im Fließtext;
- dünne Ockerlinie rechts;
- Glossar-Breadcrumb Abstand;
- Glossar-Hero;
- eigene Suchwelt `Glossar` in der Hauptsuche.

## PRODUKTIONSSICHERHEIT

- Produktion scharf: AUS.
- Auto-Publish: AUS.
- der neue Importer wird Draft-first gebaut.
- kein bestehender `CURRENT.zip` darf vor vollständiger Quell-/Releasebindung als neuer aktueller Pluginstand ersetzt werden.

## BRANCH / RÜCKGABEWEG

Campus-/Fachdokumentation:
`hobbyroom/glossar-livefail-red-green-20260913`

Technische Pluginbytes dürfen erst nach exakter Baseline-/Quellbindung als neuer Kandidat gebaut werden. Ergebnis zurück ins Fachbüro mit Testreport; PLUGINS-Büro erhält nur den zentralen Vorgang/Artefaktstatus.

## NICHT ANFASSEN

- Pferderassen gehören nicht ins Glossar;
- keine zweite Glossar-Fachdatenbank;
- keine Wiederbelebung von Cron-/Loopback-/Planning-Komplexität ohne neuen ausdrücklichen Auftrag;
- keine Auto-Publish-Freigabe;
- bestätigtes Glossar-Single-Design nicht nebenbei umbauen.

## VERWEISE

- Stand: `CURRENT_STATE.md`
- Fehler: `FEHLERQUELLEN.md`
- Regeln: `PRODUKTIONSREGELN.md`
- Entscheidungen/Warum: `ENTSCHEIDUNGEN_20260914.md`
- Fachdaten: `../WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/START_HERE.md`
