# HOBBYRAUSCH – KONZEPT – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-08
STATUS: 3-SÄULEN-GRUNDKONZEPT FEST / REGELN 1.4 KISS / BATCH 001 + 002 FINAL = 32 VON 841 / BATCH 003 VORBEREITET / 1 DATAFORSEO-OVERVIEW OFFEN

## Rolle

Einzige aktuelle Zustandsautorität des Scopes `HOBBYRAUSCH_KONZEPT`.

## Aktueller belastbarer Stand

Marke:
**Hobby Depot**

Drei Säulen:
- CORE = Hauptportal;
- EDITORIAL = Magazin;
- DIRECTORY = HivePress / Anbieter.

Acht geschützte Hauptwelten:
**Gestalten · Fertigen · Technik · Forschen · Pflanzen · Tiere · Bewegen · Sammeln**

### Harte Ebenenregel

Die acht Hauptwelten sind die oberste fachliche CORE-Ebene.

`Hobbywelten` ist nur Übersichts-/Einstiegsseite bzw. View und NICHT Parent der acht Hauptwelten.

Beliebte Hobbys, ungewöhnlich, zuhause, günstig usw. sind ebenfalls Views/Filter/kuratierte Einstiege, keine zweite Taxonomie.

## Portfolioziel

Hobby Depot soll wirtschaftlich breiter werden, ohne zum beliebigen Massenportal zu explodieren.

Integrierte Mischung:
- große bekannte Hobbys = wirtschaftliche Anker;
- mittlere Hobbys = stabiles Rückgrat;
- Nischen-/ungewöhnliche Hobbys = SEO-Longtail + Differenzierung.

Diese Klassen verändern nicht die kanonische Identität und erzeugen keine Parallelstruktur.

Großer interner Hobbybestand ist erlaubt.
Die sichtbare Navigation bleibt klein und selektiv.

## Portalgrenze

Ein Thema wird regulär aufgenommen, wenn es:
- aktive/wiederholbare Freizeitpraxis ist;
- erlern-/vertiefbaren Tätigkeitsschwerpunkt besitzt;
- natürlich in eine der acht Welten passt;
- nicht nur durch erzwungene Zuordnung integrierbar ist.

Ein echtes Hobby außerhalb dieser natürlichen Passung erzeugt nicht automatisch eine neunte Welt.

## Rollen- und Größenlogik

Mögliche Rollen:
- ORIENTATION_UNIVERSE;
- HOBBY_HUB;
- EDITORIAL_TOPIC;
- ARTICLE_ONLY;
- FINDER_ONLY;
- OUT_OF_SCOPE.

Leaf-Kategorie:
- unter 4 zusammenlegen / keine eigene Leaf-Kategorie;
- 4 Grenzfall;
- ideal etwa 5–12 Beiträge;
- 13–14 oberhalb des Idealbereichs / prüfen;
- ab etwa 15 Teilung prüfen.

Hobby-Hub:
- typischer Zielbereich 3–6 tragfähige Leaf-Kategorien;
- 7–9 oberhalb des typischen Bereichs / prüfen;
- ab etwa 10 Macro-/Split-Prüfung.

Monetarisierung entscheidet nicht über Behalten/Löschen.
Nicht monetarisierbare gültige Themen bleiben für Magazin/SEO/Finder erhalten.

## Zentrale Hobby-Sammelstelle

Rohliste bleibt unveränderte Provenienzquelle.

Aktive Bewertungsbasis:
`/hobby rausch/HOBBY_DEPOT_HOBBY_MASTER_V2_20261007.json`

Current-Zeiger:
`KONZEPT/VORARBEITEN_HOBBYFINDER/HOBBY_MASTER_V2_CURRENT.md`

Bestand:
- 908 Rohzeilen;
- 844 exakte Namen;
- 841 kanonische Identitäten nach aktuellen Alias-Merges;
- 329 bestehende V1.12-Monetarisierungs-/CORE-Regeln übernommen;
- 286 DIRECT;
- 43 ASSISTED;
- 512 UNKNOWN, aber weiterhin erhalten;
- zusätzlich 19 Research-Queue-Kandidaten außerhalb der 841 aktuellen Identitäten;
- 0 Namens-/Alias-Kollisionen im aktuellen Intake-Check;
- Fotografie ist durch den Pilotbefund für eine provisorische Master-Aufnahme vorbereitet.

## Neue bekannte Hobby-Kandidaten

Research Queue:
Fotografie, Malen, Zeichnen, Nähen, Stricken, Häkeln, Holzwerken, Heimwerken, Wandern, Radfahren, Camping, Schwimmen, Klettern, Bouldern, Gärtnern, Gemüseanbau, Briefmarken sammeln, Angeln, Plane Spotting.

Nicht automatisch publizieren.
Sie durchlaufen dieselben Scope-/Größen-/Rollen-Gates wie die bisherigen Nischen.

## Maschinenlesbare Umsetzung

Gebunden:
- `../SEO_KATEGORIEN/HOBBY_MASTER_V2_ASSESSMENT_RULES_20261007.json`
- `../SEO_KATEGORIEN/HOBBY_MASTER_V2_BATCH_001_RESULTS_20261007.json`
- `../SEO_KATEGORIEN/HOBBY_MASTER_V2_RESEARCH_INTAKE_20261007.json`
- `../SEO_KATEGORIEN/HOBBY_MASTER_V2_INTAKE_DELTA_001_20261007.json`

Damit ist die frühere Lücke zwischen Konzeptregel und tatsächlicher maschinenlesbarer Entscheidung geschlossen.

Wichtig:
Fehlende Evidenz führt zu `EVIDENCE_REQUIRED`, nicht zu einer geratenen Rollen- oder Weltzuordnung.

Batch 001 ist autoritativ final:
- `../SEO_KATEGORIEN/HOBBY_MASTER_V2_BATCH_001_FINAL_ASSESSMENT_20261007.json`;
- 16/16 geschlossen;
- 7 HOBBY_HUB;
- 3 ORIENTATION_UNIVERSE;
- 6 EDITORIAL_TOPIC;
- 0 unresolved;
- 0 Strukturwrites.

## Nachprüfung gegen das vollständige Konzept

Nachgezogen:
- nicht die Gesamtzahl eines Hobbys zählt, sondern jede unterste Kategorie einzeln;
- Ziel pro unterster Kategorie: 5–12 eigenständige Artikelintents;
- kleine valide Hobbys dürfen in stärkeren Übersichts-/Leaf-/Magazinstrukturen zusammengefasst werden, ohne ihre Hobby-Identität zu verlieren;
- neue Zwischenkategorien werden erst im späteren Gesamt-Delta gebaut;
- Fachlogik definiert und zählt die eigenständigen Artikelintents; DataForSEO validiert Nachfrage, Synonyme, Core-Keywords und Intent-Überschneidung, kann Dubletten zusammenführen, erzeugt aber weder Struktur noch zusätzliche Artikelintents und löscht keinen fachlich eigenständigen Intent nur wegen einer fehlenden exakten Longtail-Zeile.

Konzeptaudit:
`../SEO_KATEGORIEN/HOBBY_MASTER_V2_CONCEPT_AUDIT_20261007.md`

## Reales Batch-001-Ergebnis – historische Evidence

Der echte WordPress-/DataForSEO-Lauf wurde ausgeführt und bleibt als Evidence erhalten:
- 263 fachlich vorgeschlagene Artikelintents;
- 106 exakte Keyword-Overview-Zeilen im ersten Aufruf;
- anschließend historische Depth-Aufrufe;
- insgesamt 39 Provider-Aufrufe;
- ca. 0.9738 USD historische Kosten;
- 0 Strukturwrites.

Wichtig:
Die damaligen Zwischenbewertungen aus V1.12.1–V1.12.4 sind durch die KISS-Regel 1.4 für Content Capacity fachlich überholt.
Sie bleiben nur Fehler-/Evidence-Historie und dürfen nicht als aktueller Rollenbefund verwendet werden.

## KISS-Korrektur nach vollständiger Fehlerkettenprüfung

Die reale DataForSEO-Evidence ist vollständig vorhanden.

Die wiederholte technische Schleife hatte drei aufeinanderfolgende Fehlinterpretationen:
- fehlende exakte DataForSEO-Zeile wurde zu stark als fehlender Content behandelt;
- danach wurden Keyword-Ideas-Rohzeilen fälschlich als zusätzliche Artikel gezählt;
- anschließend wurden fachlich definierte Artikel noch zu stark von einem lexikalischen Provider-Match abhängig gemacht.

Verbindlich ab Regelvertrag 1.4:

1. **Fachlogik bestimmt die Content Capacity.**
   Gezählt werden fachlich eigenständige Nutzer-/Suchintents pro unterster Kategorie.

2. **DataForSEO ist der Abgleich.**
   Es liefert Nachfrage, Primärkeyword, Synonyme, Core Keyword und Intent-Überschneidung.

3. **DataForSEO darf deduplizieren.**
   Wenn zwei fachliche Seeds nach echter Core-Keyword-/Synonym-Evidence dasselbe meinen, zählen sie einmal.

4. **Fehlende exakte Longtail-Zeile löscht keinen Artikelintent.**
   Nur dessen SEO-Metriken bleiben offen.

5. **Provider-Rohzeilen erzeugen keine Artikel.**
   Keyword Ideas/Suggestions sind im Normalweg keine automatische Content-Capacity-Stufe.

Damit entspricht der Ablauf wieder dem Grundprinzip:
**fachlich prüfen, wie viele Einzelbeiträge die unterste Kategorie trägt → DataForSEO abgleichen → danach Rolle/Größe entscheiden.**

Der vollständige reale Batch wurde mit V1.12.5 lokal neu gerechnet:
- 34 ideale Leafs;
- Buchbinden = vollständiger HOBBY_HUB_CANDIDATE;
- sechs weitere Hobbys liegen kapazitätsseitig im typischen Hubbereich, benötigen aber noch Scope-/Identitätsfreigabe;
- drei Macro-Reviews;
- ein Editorial-Thema;
- fünf Aggregation-Reviews;
- 0 Strukturwrites.

## Pilotbefund – historisch eingeordnet

Frühere Pilot-/Zwischenbefunde sind durch die finale Batch-001-Datei ersetzt, soweit sie Batch-001-Rollen betreffen.
Fotografie/Garten/Musizieren bleiben nur als separate frühere Konzeptbeispiele bestehen und sind nicht Teil von Batch 001.

## Autoritative Konzeptdateien

- `HOBBY_GROESSEN_ROLLENMODELL_20261007.md`
- `../SEO_KATEGORIEN/HOBBY_MASTER_V2_INTEGRATION_20261007.md`
- `../SEO_KATEGORIEN/HOBBY_MASTER_V2_PILOT_20261007.md`

## Technische Abgrenzung

Pluginversionen, technische Release-/Teststände und Live-Status ausschließlich aus:
- `PLUGINS/PLUGIN_AKTEN/HD-001-KATEGORIE-WORKFLOW/CURRENT.md`;
- `SEO_KATEGORIEN/CURRENT_STATE.md`.

## Batch 001 – fachlicher Abschluss

Einzige autoritative Abschlussdatei:
`../SEO_KATEGORIEN/HOBBY_MASTER_V2_BATCH_001_FINAL_ASSESSMENT_20261007.json`

Ergebnis:
- 7 HOBBY_HUB;
- 3 ORIENTATION_UNIVERSE;
- 6 EDITORIAL_TOPIC;
- 0 unresolved.

## Batch 002 – vorbereitet

Deterministische erste 16 noch nicht final bewerteten Master-Identitäten sind gebunden.

Fachvorbereitung:
- 51 Leafs;
- 304 eigenständige Artikelintents;
- 304 DataForSEO-Seeds;
- ein einziger Overview-Abgleich;
- keine automatische Tiefenrecherche.

Plan:
`../SEO_KATEGORIEN/HOBBY_MASTER_V2_BATCH_002_PREPARED_20261008.json`

## Batch 002 – fachlicher Abschluss

Autoritative Datei:
`../SEO_KATEGORIEN/HOBBY_MASTER_V2_BATCH_002_FINAL_ASSESSMENT_20261008.json`

Ergebnis:
- 11 HOBBY_HUB;
- 4 ORIENTATION_UNIVERSE;
- 1 EDITORIAL_TOPIC;
- 0 unresolved.

Ownership-Grundlinien:
- Amateurfunk = Orientierung; Satellitenfunk, Morsefunk und Funkpeilung besitzen ihre Spezialintents;
- CB-Funk bleibt separat;
- Software Defined Radio besitzt generische SDR-Hardware/Software/Decoding-Intents;
- Elektronikbasteln und Mikrocontroller-Projekte sind Orientierungswelten;
- Arduino und Raspberry-Pi-Projekte sind eigene Hubs;
- Robotik = Orientierung; Roboterbau, Heimrobotik und BattleBots-Modellbau besitzen ihre spezifischen Praxisintents.

Kumuliert:
32/841 final bewertet.

## Batch 003 – vorbereitet

Nächste 16 liegen im Drohnen-/RC-Block.

Vorbereitung:
- 59 Leafs;
- 325 eigenständige Artikelintents;
- 325 SEO-Seeds;
- ein einziger Overview-Abgleich;
- keine automatische Tiefenrecherche.

Plan:
`../SEO_KATEGORIEN/HOBBY_MASTER_V2_BATCH_003_PREPARED_20261008.json`

## BATCH 004 – VORBEREITET IM VORAUS

Nur Vorarbeit; **noch nicht ausführen**, solange Batch 003 nicht final ist.

Nächste 16:
RC-Drift, RC-Offroad, RC-Trial, RC-Rennsport, Modell-Dampfmaschinen, Stirlingmotoren, Modellmotorenbau, Modellmaschinenbau, Mini-CNC, CNC-Fräsen, Lasercutting, Lasergravieren, Resin-3D-Druck, 3D-Scanning, CAD als Hobby, Heimautomatisierung.

Vorbereitet:
- 16 Kandidaten;
- 54 Leafs;
- 310 fachlich unterschiedliche Artikelintents;
- 310 SEO-Seeds;
- exakt 1 späterer Overview;
- keine Depth-Recherche;
- 0 Strukturwrites.

Plan:
`HOBBY_MASTER_V2_BATCH_004_PREPARED_20261008.json`

## Erster offener Blocker

`HOBBY_MASTER_V2_BATCH_003_REAL_OVERVIEW_PENDING`

## EXAKT EINE NEXT ACTION

Batch 003 mit genau einem read-only DataForSEO-Overview abgleichen.
Danach Rollen/Ownership fachlich finalisieren.

Noch keine Strukturänderung.
